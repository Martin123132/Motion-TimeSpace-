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

from finite_payload_vector_runner import evaluate_payload_rows  # noqa: E402
from lambda_curvature_source_gate import (  # noqa: E402
    evaluate_bound_rows,
    evaluate_cancellation_rows,
    evaluate_ricci_zero_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4401"
CLAIM_ID = "L-242"
MARKER = "PPC4161_TRANSITION_CURVATURE_SOURCED_LAMBDA_PAYLOAD_BOUND_OR_PARENT_CANCELLATION_4401"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_CURVATURE_SOURCED_LAMBDA_PAYLOAD_BOUND_OR_PARENT_CANCELLATION_4401"
DECISION = "TRACE_ELECTRIC_LAMBDA_SOURCE_IS_RICCI_UU_BOUND_LAW_READY_PARENT_VACUUM_EQUATION_UNSIGNED"
NEXT_TARGET = "4402-Y5-R2FR-transition-Ricci-uu-local-vacuum-equation-or-first-real-Etrace-bound-row.md"

FORMAL_PATH = FORMAL / "417-PPC4161-transition-curvature-sourced-lambda-payload-bound-or-parent-cancellation.md"
DOC_PATH = POST / "4401-Y5-R2FR-transition-curvature-sourced-lambda-payload-bound-or-parent-cancellation.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4401_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

LAMBDA_GATE_PATH = SCRIPT_DIR / "lambda_curvature_source_gate.py"
PAYLOAD_RUNNER_PATH = SCRIPT_DIR / "finite_payload_vector_runner.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4401_transition_curvature_sourced_lambda_payload_bound_or_parent_cancellation.py"

CANCEL_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_PARENT_CANCELLATION_INPUT.csv"
CANCEL_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_PARENT_CANCELLATION_OUTPUT.csv"
RICCI_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_RICCI_ZERO_GATE_INPUT.csv"
RICCI_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_RICCI_ZERO_GATE_OUTPUT.csv"
BOUND_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_LAMBDA_CURVATURE_BOUND_INPUT.csv"
BOUND_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_LAMBDA_CURVATURE_BOUND_OUTPUT.csv"
PAYLOAD_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_FINITE_PAYLOAD_VECTOR_INPUT.csv"
PAYLOAD_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4401_FINITE_PAYLOAD_VECTOR_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4400 = SOURCE_DIR / "P8_Y5_R2FR_4400_NEXT_TARGET.csv"
DERIVATIONS_4400 = SOURCE_DIR / "P8_Y5_R2FR_4400_COMPOSITE_US_DERIVATIONS.csv"
COMPOSITE_OUTPUT_4400 = SOURCE_DIR / "P8_Y5_R2FR_4400_COMPOSITE_US_GATE_OUTPUT.csv"
PAYLOAD_OUTPUT_4400 = SOURCE_DIR / "P8_Y5_R2FR_4400_FINITE_PAYLOAD_VECTOR_OUTPUT.csv"
SIGMA_ACTION_4393 = SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv"
WARD_OUTPUT_4398 = SOURCE_DIR / "P8_Y5_R2FR_4398_WARD_EXCHANGE_OUTPUT.csv"
FORMAL_4400 = FORMAL / "416-PPC4161-transition-composite-US-parent-functional-or-finite-payload-vector-runner.md"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4401_0_4400_next": (
        NEXT_4400,
        "4401-Y5-R2FR-transition-curvature-sourced-lambda-payload-bound-or-parent-cancellation.md",
        "4400 handoff to parent cancellation or elliptic bound.",
    ),
    "SRC4401_1_4400_derivation": (
        DERIVATIONS_4400,
        "CUS4400_2_curvature_sourced_lambda_obstruction",
        "4400 derivation of curvature-sourced lambda obstruction.",
    ),
    "SRC4401_2_4400_composite_gate": (
        COMPOSITE_OUTPUT_4400,
        "COMPOSITE_SIGMA_U_CURVATURE_SOURCED_LAMBDA_OBSTRUCTION",
        "4400 gate detecting the sigma-U curvature source.",
    ),
    "SRC4401_3_4400_payload_runner": (
        PAYLOAD_OUTPUT_4400,
        "FPV4400_1_numeric_schema_smoke_nonclaim",
        "4400 finite payload vector runner output.",
    ),
    "SRC4401_4_4393_constraint": (
        SIGMA_ACTION_4393,
        "SACT4393_2_multiplier_null_lemma",
        "4393 multiplier-null lemma before curvature coupling.",
    ),
    "SRC4401_5_4398_ward": (
        WARD_OUTPUT_4398,
        "WG4398_0_noether_formula_ready",
        "4398 Ward formula and source/payload warning.",
    ),
    "SRC4401_6_formal_4400": (
        FORMAL_4400,
        "c^2 h^{ij} R_{0i0j}",
        "4400 formal equation whose trace-electric source is refined here.",
    ),
    "SRC4401_7_lambda_gate": (
        LAMBDA_GATE_PATH,
        "def evaluate_bound_rows",
        "New lambda curvature-source cancellation/Ricci/bound gate.",
    ),
    "SRC4401_8_payload_runner": (
        PAYLOAD_RUNNER_PATH,
        "def evaluate_payload_rows",
        "Finite payload vector runner reused with lambda-curvature score.",
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
            "derivation_id": "LCS4401_0_trace_electric_source_is_Ricci_uu",
            "statement": "For the trace-electric composite S^{ij}=c^2 h^{ij} sigma_S, the curvature source in the sigma equation is the normal Ricci trace R_{uu}, not the full Weyl tidal tensor.",
            "derivation": "In the local rest frame of u, the electric U projector gives U.R = k_E S^{ij}R_{0i0j}, with k_E a convention factor fixed by the U normalization and the 1/2 action prefactor. Since h^{ij}R_{0i0j}=R_{mu nu}u^mu u^nu up to sign convention and extrinsic/projector terms, partial(U.R)/partial sigma_S = k_E c^2 R_{uu}. The bound route only needs the absolute coefficient K_E.",
            "new_information": "The obstruction is narrower than 4400 made it sound: it is a Ricci-normal/matter-source payload, not a generic Weyl-tide payload.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "LCS4401_1_local_vacuum_zero_condition",
            "statement": "If the parent local-vacuum metric equation signs R_{uu}=0 on the same tau/coframe support, with projector and boundary terms silent, the curvature-sourced lambda equation reduces back to the 4393 homogeneous elliptic equation.",
            "derivation": "The sigma equation is Delta_h^dagger lambda_S = -K_E c^2 R_{uu}+B_projector+B_boundary. On a local vacuum collar where R_{uu}=0, B_projector=0 or bounded, and the same boundary/zero-mode clauses of 4393 hold, lambda_S is zero or bounded by the remaining explicit payloads.",
            "new_information": "The cleanest route is now a parent Ricci-vacuum equation, not an arbitrary cancellation counterterm.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "LCS4401_2_no_free_counterterm_cancellation",
            "statement": "A parent cancellation is only legitimate if it is the same parent variation, has the exact opposite kernel, introduces no tuned coefficient, keeps the U density owner alive, and cancels boundary/Ward/EM side terms.",
            "derivation": "Adding an opposite -U[sigma]R term trivially cancels the lambda source but also deletes the improvement mechanism or adds an unsourced tuned coefficient. Such a move is not a derivation; it is a counterterm unless the parent source-owner sector independently forces it.",
            "new_information": "The cancellation route is tightly gated and current sources do not pass it.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "LCS4401_3_elliptic_lambda_payload_bound",
            "statement": "If R_{uu} is not proven zero, the branch has a finite bound law: ||lambda_S||_2 <= C_P^2 ||F_E||_2, ||D lambda_S||_2 <= C_P ||F_E||_2, and ||lambda_S||_{H2} <= C_E ||F_E||_2.",
            "derivation": "For Delta_h lambda_S = F_E with Dirichlet or zero-mean Neumann/mixed anchored data, multiply by lambda_S and use Poincare plus elliptic regularity. The induced normalized stress payload is bounded by K_lambda K_projection (C_P^2+C_P+C_E)||F_E||_2.",
            "new_information": "The fallback is now a calculable source row: provide ||R_{uu}|| or F_E on W_H and domain constants, and the runner computes the lambda-curvature payload.",
            "valid_for_claim": "False",
        },
    ]


def cancellation_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "CAN4401_0_existing_parent_source_owner_search",
            "route": "current_sources_parent_cancellation",
            "parent_counter_source_declared": "False",
            "same_parent_variation": "False",
            "opposite_kernel_exact": "False",
            "no_new_tuned_coefficient": "False",
            "does_not_cancel_density_owner": "True",
            "boundary_terms_cancel": "False",
            "Ward_EM_guard": "False",
            "parent_authority": "MISSING_PARENT_SIGNED_COUNTER_SOURCE",
            "source_path": str(COMPOSITE_OUTPUT_4400),
            "input_valid_for_claim": "False",
            "notes": "Existing rows expose the obstruction but do not contain a signed opposite parent source.",
        },
        {
            "candidate_id": "CAN4401_1_trivial_negative_U_counterterm_trap",
            "route": "add_minus_U_sigma_R_by_hand",
            "parent_counter_source_declared": "True",
            "same_parent_variation": "True",
            "opposite_kernel_exact": "True",
            "no_new_tuned_coefficient": "False",
            "does_not_cancel_density_owner": "False",
            "boundary_terms_cancel": "False",
            "Ward_EM_guard": "False",
            "parent_authority": "NO_AUTHORITY_TRIVIAL_COUNTERTERM",
            "source_path": str(FORMAL_4400),
            "input_valid_for_claim": "False",
            "notes": "This cancels the source only by deleting or tuning the improvement action; it is not a derivation.",
        },
        {
            "candidate_id": "CAN4401_2_future_source_owner_cancellation_certificate",
            "route": "same_parent_stress_improvement_sector_opposite_kernel",
            "parent_counter_source_declared": "True",
            "same_parent_variation": "False",
            "opposite_kernel_exact": "False",
            "no_new_tuned_coefficient": "False",
            "does_not_cancel_density_owner": "True",
            "boundary_terms_cancel": "False",
            "Ward_EM_guard": "False",
            "parent_authority": "MISSING_PARENT_SIGNED_SOURCE_OWNER_CANCELLATION",
            "source_path": str(WARD_OUTPUT_4398),
            "input_valid_for_claim": "False",
            "notes": "Allowed future route, but it needs a real parent source-owner derivation.",
        },
    ]


def ricci_zero_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "RZ4401_0_trace_electric_source_classified",
            "route": "hij_R0i0j_equals_Ricci_uu",
            "trace_electric_identified_as_Ricci_uu": "True",
            "local_vacuum_domain_declared": "False",
            "parent_metric_equation_Ricci_uu_zero": "False",
            "matter_support_excluded_or_bounded": "False",
            "projector_extrinsic_terms_bounded": "False",
            "boundary_zero_mode_fixed": "False",
            "parent_authority": "MISSING_PARENT_SIGNED_RICCI_ZERO_EQUATION",
            "source_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Source classification is derived here; zero certificate is not.",
        },
        {
            "candidate_id": "RZ4401_1_local_vacuum_template",
            "route": "parent_local_vacuum_Ricci_uu_zero",
            "trace_electric_identified_as_Ricci_uu": "True",
            "local_vacuum_domain_declared": "True",
            "parent_metric_equation_Ricci_uu_zero": "False",
            "matter_support_excluded_or_bounded": "True",
            "projector_extrinsic_terms_bounded": "True",
            "boundary_zero_mode_fixed": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_LOCAL_VACUUM_RICCI_EQUATION",
            "source_path": str(FORMAL_4400),
            "input_valid_for_claim": "False",
            "notes": "This is the serious local-vacuum route: close R_uu=0 from parent metric equations.",
        },
        {
            "candidate_id": "RZ4401_2_matter_or_lab_payload_branch",
            "route": "Ricci_uu_nonzero_matter_payload",
            "trace_electric_identified_as_Ricci_uu": "True",
            "local_vacuum_domain_declared": "False",
            "parent_metric_equation_Ricci_uu_zero": "False",
            "matter_support_excluded_or_bounded": "False",
            "projector_extrinsic_terms_bounded": "True",
            "boundary_zero_mode_fixed": "True",
            "parent_authority": "MISSING_MATTER_SOURCE_BOUND",
            "source_path": str(BOUND_OUTPUT_PATH),
            "input_valid_for_claim": "False",
            "notes": "Matter/lab domains require a finite R_uu or F_E source norm.",
        },
    ]


def bound_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "LCB4401_0_missing_live_Etrace_bound",
            "arena": "local_GR_Newton_PPN",
            "F_E_norm": "MISSING_RICCI_UU_OR_E_TRACE_NORM",
            "C_poincare": "MISSING_DOMAIN_CONSTANT",
            "C_elliptic_H2": "MISSING_ELLIPTIC_CONSTANT",
            "K_lambda_stress": "MISSING_STRESS_PROJECTION",
            "K_projection": "MISSING_ARENA_PROJECTION",
            "arena_threshold": "MISSING_ARENA_THRESHOLD",
            "boundary_condition": "MISSING_BOUNDARY_CONDITION",
            "zero_mode_fixed": "False",
            "boundary_flux_silent": "False",
            "source_path": "MISSING_SOURCE_PATH",
            "support_certificate_path": "MISSING_SUPPORT_CERTIFICATE",
            "input_valid_for_claim": "False",
            "notes": "Live bound still needs a real R_uu/F_E norm and domain constants.",
        },
        {
            "bound_id": "LCB4401_1_numeric_elliptic_bound_smoke_nonclaim",
            "arena": "runner_schema_only",
            "F_E_norm": "0.001",
            "C_poincare": "1.0",
            "C_elliptic_H2": "2.0",
            "K_lambda_stress": "1.0",
            "K_projection": "1.0",
            "arena_threshold": "0.01",
            "boundary_condition": "zero_mean_Neumann",
            "zero_mode_fixed": "True",
            "boundary_flux_silent": "True",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row proving the elliptic payload formula computes cleanly.",
        },
        {
            "bound_id": "LCB4401_2_numeric_elliptic_bound_fail_nonclaim",
            "arena": "runner_threshold_fail",
            "F_E_norm": "0.01",
            "C_poincare": "2.0",
            "C_elliptic_H2": "4.0",
            "K_lambda_stress": "2.0",
            "K_projection": "1.0",
            "arena_threshold": "0.005",
            "boundary_condition": "Dirichlet",
            "zero_mode_fixed": "True",
            "boundary_flux_silent": "True",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row proving a too-large curvature source fails.",
        },
    ]


def finite_payload_input_rows(lambda_smoke_score: str) -> List[Dict[str, str]]:
    return [
        {
            "payload_id": "FPV4401_0_lambda_bound_insert_smoke_nonclaim",
            "target": "runner_schema_from_elliptic_lambda_bound",
            "R_S_score": "0.001",
            "J_U_score": "0.001",
            "pressure_aniso_score": "0.001",
            "curvature_boundary_score": "0.001",
            "lambda_kernel_score": "0.001",
            "EM_overlap_score": "0.001",
            "lambda_curvature_source_score": lambda_smoke_score,
            "delta_threshold": "0.02",
            "source_path": str(BOUND_OUTPUT_PATH),
            "same_support_certificate": str(BOUND_OUTPUT_PATH),
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
            "notes": "Consumes the 4401 elliptic lambda-curvature score inside the existing finite payload runner; still nonclaim because input rows are smoke data.",
        }
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    gates = {
        "trace_electric_source": "source narrowed to Ricci_uu, but parent local-vacuum Ricci equation is unsigned",
        "parent_cancellation": "no nontrivial same-parent opposite-kernel cancellation certificate exists",
        "lambda_curvature_bound": "elliptic bound law is executable, but no real R_uu/F_E norm and domain constants are sourced",
        "local_GR_Newton_PPN": "local GR/Newton/PPN remain blocked until Ricci_uu zero or finite payload vector passes with real inputs",
        "R10_clock_orbital": "lab/clock/orbital branches need matter-domain R_uu/F_E source bounds before claim",
    }
    return [
        {
            "gate_id": f"CG4401_{index}_{arena}",
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
            "decision_id": "DEC4401_0",
            "decision": DECISION,
            "summary": "4401 improves the local branch materially: the curvature-sourced lambda obstruction is identified as a Ricci-normal source R_uu, not a generic Weyl tidal source. That means the local-vacuum route is sharper: if parent equations derive R_uu=0 on the same support, the lambda equation returns to the homogeneous 4393 case. No current source signs that parent Ricci-vacuum equation or a nontrivial cancellation, so 4401 also installs an elliptic bound runner: ||lambda|| and its payload are bounded by domain constants times ||F_E||. This is still nonclaim, but it turns the obstruction into a real source-row problem.",
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
            "summary": "trace-electric lambda source classified as Ricci_uu; parent cancellation blocked; elliptic payload bound runner ready.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4401_0",
            "target": NEXT_TARGET,
            "question": "Can MTS derive the local-vacuum Ricci_uu=0 condition on the same tau/coframe support, or must the first real E_trace/Ricci_uu bound row be sourced?",
            "preferred_route": "try deriving parent local-vacuum Ricci_uu=0 from the metric/source coupling, because it would restore the clean homogeneous lambda branch outside matter.",
            "fallback_route": "source or compute ||F_E||, domain constants and projection coefficients for matter/lab support and pass them through the elliptic payload runner.",
            "avoid": "treating Weyl/tidal curvature as the obstruction after the trace projection has narrowed it to Ricci_uu.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    cancellation_output: List[Dict[str, str]],
    ricci_output: List[Dict[str, str]],
    bound_output: List[Dict[str, str]],
    payload_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 417 PPC4161 transition: curvature-sourced lambda payload bound or parent cancellation

Marker: `{MARKER}`

## Result

4401 moves the obstruction forward. The bad news is that no honest parent cancellation is currently signed. The good news is better: the trace-electric sigma route does not source `lambda_S` with arbitrary tidal curvature. It sources it with the normal Ricci trace `R_uu`.

So the next local-GR question is sharper:

`R_uu = 0` in the same local-vacuum tau/coframe support, or else a finite matter/lab `R_uu` payload bound.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"

    text += "\n## Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"

    text += """## Exact Local Source Form

Using the electric projector route, the local rest-frame contraction has the form

`U.R = k_E S^{ij}R_{0i0j}`

where `k_E` is a convention factor fixed by the normalization of `U` and the `1/2` action prefactor. With `S^{ij}=c^2h^{ij}sigma_S`,

`partial(U.R)/partial sigma_S = k_E c^2 h^{ij}R_{0i0j}`.

But `h^{ij}R_{0i0j}` is the normal Ricci trace `R_{mu nu}u^mu u^nu`, up to sign and projector/extrinsic conventions. Therefore the lambda equation is

`Delta_h^dagger lambda_S = -K_E c^2 R_uu + B_projector + B_boundary`.

That is a much better-shaped obstruction than a full Weyl tidal source.

## Parent Cancellation Gate

"""
    for row in cancellation_output:
        text += f"- `{row['candidate_id']}`: algebra_ready=`{row['algebra_ready']}`, nontrivial_ready=`{row['nontrivial_ready']}`, trivial_counterterm_trap=`{row['trivial_counterterm_trap']}`, certificate_ready=`{row['cancellation_certificate_ready']}`, status=`{row['current_status']}`.\n"

    text += "\n## Ricci-Zero Gate\n\n"
    for row in ricci_output:
        text += f"- `{row['candidate_id']}`: source_classified=`{row['source_classified']}`, vacuum_ready=`{row['vacuum_ready']}`, metric_ready=`{row['metric_ready']}`, certificate_ready=`{row['ricci_zero_certificate_ready']}`, status=`{row['current_status']}`.\n"

    text += "\n## Elliptic Payload Bound\n\n"
    text += "`Pi_lambdaE <= K_lambda K_projection (C_P^2 + C_P + C_E)||F_E||_2`\n\n"
    for row in bound_output:
        text += f"- `{row['bound_id']}`: schema_ready=`{row['schema_ready']}`, boundary_ready=`{row['boundary_ready']}`, payload_score=`{row['lambda_curvature_payload_score']}`, threshold=`{row['arena_threshold']}`, status=`{row['current_status']}`.\n"

    text += "\n## Finite Payload Vector Insert\n\n"
    for row in payload_output:
        text += f"- `{row['payload_id']}`: schema_ready=`{row['schema_ready']}`, total_payload_score=`{row['total_payload_score']}`, threshold=`{row['delta_threshold']}`, status=`{row['current_status']}`.\n"

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
        f"""# 4401 Y5 R2FR: curvature-sourced lambda payload bound or parent cancellation

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
## 4401 local spine update: lambda source is Ricci-normal, not generic tide

Marker: `{MARKER}`

Spine update: the trace-electric `S^{{ij}}=c^2h^{{ij}}sigma_S` composite branch sources the sigma multiplier by `R_uu`, not by arbitrary Weyl curvature. This makes the local-vacuum target sharper: derive `R_uu=0` from parent metric/source coupling on the same tau/coframe support, or bound the finite matter/lab `R_uu` payload with the new elliptic runner.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4401 packet update: Ricci source and elliptic lambda payload

Marker: `{PACKET_MARKER}`

Packet update: 4401 rejects free counterterm cancellation, classifies the trace-electric lambda source as `R_uu`, and installs a source-row elliptic bound for the remaining multiplier stress payload.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4401 refines the 4400 curvature-sourced lambda obstruction. In the trace-electric composite branch S^{ij}=c^2h^{ij}sigma_S, the source is h^{ij}R_0i0j, i.e. the normal Ricci trace R_uu up to sign/projector conventions, not generic Weyl tidal curvature. Thus a parent local-vacuum R_uu=0 equation would restore the homogeneous lambda branch; otherwise the new elliptic runner bounds the lambda payload by domain constants times ||F_E||. No nontrivial parent cancellation, local-GR/Newton/PPN/R10/clock/orbital claim is made.",
            "4401 source register, lambda-source derivations, parent cancellation gate, Ricci-zero gate, elliptic lambda bound runner, finite payload vector insert, claim gates, decision, status, next target and validation CSV.",
            "trace_electric_lambda_source_is_Ricci_uu_elliptic_bound_ready_nonclaim",
            "Derive parent local-vacuum Ricci_uu=0 on the same support or source a real F_E/Ricci_uu payload row.",
            "Treating full Weyl/tidal curvature as the source, adding a tuned counterterm, or claiming lambda_S=0 without Ricci-zero/bound evidence.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4401_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4401_LAMBDA_SOURCE_DERIVATIONS.csv")
    cancellation_output = read_csv(CANCEL_OUTPUT_PATH)
    ricci_output = read_csv(RICCI_OUTPUT_PATH)
    bound_output = read_csv(BOUND_OUTPUT_PATH)
    payload_output = read_csv(PAYLOAD_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4401_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4401_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4401_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4401_2_ricci_source_derived", any(row["derivation_id"] == "LCS4401_0_trace_electric_source_is_Ricci_uu" for row in derivations), "trace-electric source classified as Ricci_uu")
    add("VAL4401_3_vacuum_zero_condition_written", any(row["derivation_id"] == "LCS4401_1_local_vacuum_zero_condition" for row in derivations), "local-vacuum zero condition written")
    add("VAL4401_4_counterterm_guard_written", any(row["derivation_id"] == "LCS4401_2_no_free_counterterm_cancellation" for row in derivations), "counterterm guard written")
    add("VAL4401_5_elliptic_bound_written", any(row["derivation_id"] == "LCS4401_3_elliptic_lambda_payload_bound" for row in derivations), "elliptic bound law written")
    add("VAL4401_6_cancellation_nonclaim", all(row["valid_for_claim"] == "False" for row in cancellation_output), "cancellation gate remains nonclaim")
    add("VAL4401_7_trivial_counterterm_trap_detected", any(row["candidate_id"] == "CAN4401_1_trivial_negative_U_counterterm_trap" and row["trivial_counterterm_trap"] == "True" for row in cancellation_output), "trivial counterterm trap detected")
    add("VAL4401_8_ricci_classification_detected", any(row["candidate_id"] == "RZ4401_0_trace_electric_source_classified" and row["source_classified"] == "True" for row in ricci_output), "Ricci source classification gate detects source")
    add("VAL4401_9_vacuum_template_unsigned", any(row["candidate_id"] == "RZ4401_1_local_vacuum_template" and row["current_status"] == "RICCI_TRACE_SOURCE_IDENTIFIED_PARENT_VACUUM_EQUATION_UNSIGNED" for row in ricci_output), "vacuum template blocks on parent metric equation")
    add("VAL4401_10_bound_smoke_ready", any(row["bound_id"] == "LCB4401_1_numeric_elliptic_bound_smoke_nonclaim" and row["schema_ready"] == "True" and row["payload_within_threshold"] == "True" for row in bound_output), "elliptic bound smoke row computes")
    add("VAL4401_11_bound_fail_detected", any(row["bound_id"] == "LCB4401_2_numeric_elliptic_bound_fail_nonclaim" and row["current_status"] == "LAMBDA_CURVATURE_PAYLOAD_BOUND_FAILS_THRESHOLD" for row in bound_output), "elliptic threshold fail row detected")
    add("VAL4401_12_bound_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in bound_output), "bound rows remain nonclaim")
    add("VAL4401_13_payload_insert_computes", any(row["payload_id"] == "FPV4401_0_lambda_bound_insert_smoke_nonclaim" and row["schema_ready"] == "True" for row in payload_output), "finite payload vector consumes lambda bound score")
    add("VAL4401_14_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4401_15_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4401_16_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4401_17_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4401_18_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4401_19_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4401_20_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4401_21_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4401_22_gate_script_exists", LAMBDA_GATE_PATH.exists() and "def evaluate_ricci_zero_rows" in read_text(LAMBDA_GATE_PATH), "lambda curvature gate exists")
    add("VAL4401_23_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = derivation_rows()
    cancellation_inputs = cancellation_input_rows()
    ricci_inputs = ricci_zero_input_rows()
    bound_inputs = bound_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_paths: List[Path] = [CANCEL_INPUT_PATH, RICCI_INPUT_PATH, BOUND_INPUT_PATH]

    write_csv(CANCEL_INPUT_PATH, cancellation_inputs)
    cancellation_output = evaluate_cancellation_rows(CANCEL_INPUT_PATH)
    write_csv(CANCEL_OUTPUT_PATH, cancellation_output)
    csv_paths.append(CANCEL_OUTPUT_PATH)

    write_csv(RICCI_INPUT_PATH, ricci_inputs)
    ricci_output = evaluate_ricci_zero_rows(RICCI_INPUT_PATH)
    write_csv(RICCI_OUTPUT_PATH, ricci_output)
    csv_paths.append(RICCI_OUTPUT_PATH)

    write_csv(BOUND_INPUT_PATH, bound_inputs)
    bound_output = evaluate_bound_rows(BOUND_INPUT_PATH)
    write_csv(BOUND_OUTPUT_PATH, bound_output)
    csv_paths.append(BOUND_OUTPUT_PATH)

    lambda_smoke_score = next(
        row["lambda_curvature_payload_score"]
        for row in bound_output
        if row["bound_id"] == "LCB4401_1_numeric_elliptic_bound_smoke_nonclaim"
    )
    payload_inputs = finite_payload_input_rows(lambda_smoke_score)
    write_csv(PAYLOAD_INPUT_PATH, payload_inputs)
    payload_output = evaluate_payload_rows(PAYLOAD_INPUT_PATH)
    write_csv(PAYLOAD_OUTPUT_PATH, payload_output)
    csv_paths.extend([PAYLOAD_INPUT_PATH, PAYLOAD_OUTPUT_PATH])

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4401_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4401_LAMBDA_SOURCE_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4401_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4401_DECISION.csv": decisions,
        "P8_Y5_R2FR_4401_STATUS.csv": statuses,
        "P8_Y5_R2FR_4401_NEXT_TARGET.csv": next_targets,
    }

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(
        sources,
        derivations,
        cancellation_output,
        ricci_output,
        bound_output,
        payload_output,
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
