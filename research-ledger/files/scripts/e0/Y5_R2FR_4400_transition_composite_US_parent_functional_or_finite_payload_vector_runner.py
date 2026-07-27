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

from composite_us_parent_functional_gate import evaluate_composite_rows, read_csv, write_csv  # noqa: E402
from finite_payload_vector_runner import evaluate_payload_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4400"
CLAIM_ID = "L-241"
MARKER = "PPC4161_TRANSITION_COMPOSITE_US_PARENT_FUNCTIONAL_OR_FINITE_PAYLOAD_VECTOR_RUNNER_4400"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_COMPOSITE_US_PARENT_FUNCTIONAL_OR_FINITE_PAYLOAD_VECTOR_RUNNER_4400"
DECISION = "COMPOSITE_SIGMA_U_ROUTE_REDUCES_OVERCONSTRAINT_BUT_GENERATES_CURVATURE_SOURCED_LAMBDA_PAYLOAD"
NEXT_TARGET = "4401-Y5-R2FR-transition-curvature-sourced-lambda-payload-bound-or-parent-cancellation.md"

FORMAL_PATH = FORMAL / "416-PPC4161-transition-composite-US-parent-functional-or-finite-payload-vector-runner.md"
DOC_PATH = POST / "4400-Y5-R2FR-transition-composite-US-parent-functional-or-finite-payload-vector-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4400_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

COMPOSITE_GATE_PATH = SCRIPT_DIR / "composite_us_parent_functional_gate.py"
PAYLOAD_RUNNER_PATH = SCRIPT_DIR / "finite_payload_vector_runner.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4400_transition_composite_US_parent_functional_or_finite_payload_vector_runner.py"

COMPOSITE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4400_COMPOSITE_US_GATE_INPUT.csv"
COMPOSITE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4400_COMPOSITE_US_GATE_OUTPUT.csv"
PAYLOAD_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4400_FINITE_PAYLOAD_VECTOR_INPUT.csv"
PAYLOAD_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4400_FINITE_PAYLOAD_VECTOR_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

PARENT_US_4391 = SOURCE_DIR / "P8_Y5_R2FR_4391_PARENT_U_S_THEOREMS.csv"
SIGMA_THEOREMS_4392 = SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_THEOREMS.csv"
SIGMA_ACTION_4393 = SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv"
WARD_OUTPUT_4398 = SOURCE_DIR / "P8_Y5_R2FR_4398_WARD_EXCHANGE_OUTPUT.csv"
PARENT_EQUATION_OUTPUT_4399 = SOURCE_DIR / "P8_Y5_R2FR_4399_PARENT_US_EQUATION_OUTPUT.csv"
FINITE_CONTRACT_4399 = SOURCE_DIR / "P8_Y5_R2FR_4399_FINITE_PAYLOAD_CONTRACT.csv"
NEXT_4399 = SOURCE_DIR / "P8_Y5_R2FR_4399_NEXT_TARGET.csv"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4400_0_4399_next": (
        NEXT_4399,
        "4400-Y5-R2FR-transition-composite-US-parent-functional-or-finite-payload-vector-runner.md",
        "4399 handoff to composite U/S or finite payload runner.",
    ),
    "SRC4400_1_4399_parent_equation": (
        PARENT_EQUATION_OUTPUT_4399,
        "PEQ4399_2_composite_U_parent_functional",
        "4399 parent equation output identifying the composite route.",
    ),
    "SRC4400_2_4399_payload_contract": (
        FINITE_CONTRACT_4399,
        "FP4399_2_Ward_exchange",
        "4399 finite-payload contract to make the fallback executable.",
    ),
    "SRC4400_3_4391_parent_us": (
        PARENT_US_4391,
        "UST4391_1_transverse_S_parent_sector_contract",
        "4391 tau/coframe and transverse S parent-sector contract.",
    ),
    "SRC4400_4_4392_sigma": (
        SIGMA_THEOREMS_4392,
        "SIGS4392_0_trace_electric_owner",
        "4392 trace-electric sigma owner construction.",
    ),
    "SRC4400_5_4393_constraint": (
        SIGMA_ACTION_4393,
        "SACT4393_2_multiplier_null_lemma",
        "4393 sigma/lambda constraint and multiplier-null lemma.",
    ),
    "SRC4400_6_4398_ward": (
        WARD_OUTPUT_4398,
        "WG4398_0_noether_formula_ready",
        "4398 Ward exchange formula and finite payload warning.",
    ),
    "SRC4400_7_composite_gate": (
        COMPOSITE_GATE_PATH,
        "def evaluate_composite_rows",
        "New composite U/S parent-functional gate.",
    ),
    "SRC4400_8_payload_runner": (
        PAYLOAD_RUNNER_PATH,
        "def evaluate_payload_rows",
        "New finite payload vector runner.",
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
            "derivation_id": "CUS4400_0_composite_variation_not_independent_U",
            "statement": "If U or S is a composite parent functional U[Phi,g,tau,e] rather than an independent multiplier, the dangerous independent delta U equation is removed.",
            "derivation": "For S_U[Phi]=1/2 int sqrt(-g) U^{mu alpha nu beta}[Phi] R_{mu alpha nu beta}, variation gives delta S_U/delta Phi^A = 1/2 sqrt(-g) R_{mu alpha nu beta} delta U^{mu alpha nu beta}/delta Phi^A plus metric/coframe terms. There is no arbitrary delta U, so the 4399 curvature projection R=0 is not an independent Euler equation.",
            "new_information": "Composite U/S is a real way past the 4399 curvature-multiplier no-go.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "CUS4400_1_sigma_trace_candidate_functional",
            "statement": "The least-new-object composite candidate is the 4391-4393 trace-electric route: u=tau_obs/sqrt(-g(tau_obs,tau_obs)), S^{ij}=c^2 h^{ij} sigma_S, and U built from u and S.",
            "derivation": "4391 supplies the tau/coframe u and spatial S contract; 4392 gives c^-2 D_iD_j S^{ij}=Delta_h sigma_S; 4393 gives the parent constraint template Delta_h sigma_S=delta rho_topH. Together they make the density slot match R_S if the same support and parent source clauses are signed.",
            "new_information": "The composite route is not vague now: its minimal variable content is {tau_obs, h, sigma_S, lambda_S, delta rho_topH}.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "CUS4400_2_curvature_sourced_lambda_obstruction",
            "statement": "Coupling the sigma constraint to the composite U.R action spoils the old free multiplier-null lemma unless the curvature source cancels or is bounded.",
            "derivation": "For S_tot=int_W sqrt(h) lambda_S(Delta_h sigma_S-delta rho_topH)+1/2 int_M sqrt(-g) U[sigma_S]R, variation with respect to sigma_S gives Delta_h^dagger lambda_S = -1/2 Pi_W[(sqrt(-g)/sqrt(h)) R_{mu alpha nu beta} partial U^{mu alpha nu beta}/partial sigma_S] plus boundary and projector terms. In the trace-electric candidate this source contains c^2 h^{ij}R_{0i0j} plus projection terms, so lambda_S is generally curvature-sourced rather than automatically zero.",
            "new_information": "This is the new hard target: either parent-cancel this curvature source, or bound the induced lambda/stress payload.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "CUS4400_3_no_cancellation_payload_vector",
            "statement": "If the curvature-sourced lambda term is not parent-cancelled, the local branch must be judged by an absolute finite-payload vector rather than by hidden cancellations.",
            "derivation": "Define Delta_loc = |R_S| + |J_U| + |Pi_pressure| + |Pi_curv_boundary| + |Pi_lambda_kernel| + |Pi_EM_overlap| + |Pi_lambda_curv_source| in normalized arena units. The runner accepts only sourced, same-support, nonnegative rows with no cancellation and Delta_loc below a declared threshold.",
            "new_information": "The fallback is executable and includes the new lambda-curvature-source component.",
            "valid_for_claim": "False",
        },
    ]


def composite_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "CUSG4400_0_sigma_trace_composite_U_candidate",
            "route": "sigma_trace_electric_S_into_composite_U",
            "parent_functional_declared": "True",
            "base_parent_fields_declared": "True",
            "functional_derivative_written": "True",
            "no_independent_U_variation": "True",
            "sigma_constraint_coupled": "True",
            "multiplier_null_survives_curvature_coupling": "False",
            "curvature_sourced_lambda_bound_declared": "False",
            "same_tau_coframe_support": "True",
            "density_projection_matches_R_S": "True",
            "Phi_equations_owned": "False",
            "Ward_exchange_closes_on_shell": "False",
            "boundary_flux_terms_declared": "False",
            "pressure_curvature_payload_declared": "True",
            "EM_double_count_guard": "False",
            "finite_payload_fallback_declared": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_SIGMA_U_COMPOSITE_FUNCTIONAL",
            "source_path": str(SIGMA_THEOREMS_4392),
            "input_valid_for_claim": "False",
            "notes": "Best minimal composite route, but the sigma equation receives a curvature source from U[sigma]R.",
        },
        {
            "candidate_id": "CUSG4400_1_formal_composite_template",
            "route": "generic_U_of_Phi_parent_functional_template",
            "parent_functional_declared": "True",
            "base_parent_fields_declared": "True",
            "functional_derivative_written": "True",
            "no_independent_U_variation": "True",
            "sigma_constraint_coupled": "False",
            "multiplier_null_survives_curvature_coupling": "False",
            "curvature_sourced_lambda_bound_declared": "False",
            "same_tau_coframe_support": "False",
            "density_projection_matches_R_S": "False",
            "Phi_equations_owned": "False",
            "Ward_exchange_closes_on_shell": "False",
            "boundary_flux_terms_declared": "False",
            "pressure_curvature_payload_declared": "False",
            "EM_double_count_guard": "False",
            "finite_payload_fallback_declared": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_GENERIC_COMPOSITE_FUNCTIONAL",
            "source_path": str(PARENT_EQUATION_OUTPUT_4399),
            "input_valid_for_claim": "False",
            "notes": "Generic route avoids independent U variation but lacks density projection and dynamics.",
        },
        {
            "candidate_id": "CUSG4400_2_post_readout_green_inverse_trap",
            "route": "post_readout_sigma_Green_inverse_as_if_parent_functional",
            "parent_functional_declared": "False",
            "base_parent_fields_declared": "False",
            "functional_derivative_written": "False",
            "no_independent_U_variation": "False",
            "sigma_constraint_coupled": "True",
            "multiplier_null_survives_curvature_coupling": "False",
            "curvature_sourced_lambda_bound_declared": "False",
            "same_tau_coframe_support": "False",
            "density_projection_matches_R_S": "True",
            "Phi_equations_owned": "False",
            "Ward_exchange_closes_on_shell": "False",
            "boundary_flux_terms_declared": "False",
            "pressure_curvature_payload_declared": "False",
            "EM_double_count_guard": "False",
            "finite_payload_fallback_declared": "True",
            "parent_authority": "NO_AUTHORITY_POST_READOUT_GREEN_INVERSE",
            "source_path": str(SIGMA_THEOREMS_4392),
            "input_valid_for_claim": "False",
            "notes": "Late Green inversion remains useful for bounds only; it is not a parent derivation.",
        },
    ]


def payload_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "payload_id": "FPV4400_0_missing_real_payload_vector",
            "target": "local_GR_Newton_PPN",
            "R_S_score": "MISSING_R_S_PROFILE_NORM",
            "J_U_score": "MISSING_WARD_PAYLOAD_NORM",
            "pressure_aniso_score": "MISSING_PRESSURE_PAYLOAD",
            "curvature_boundary_score": "MISSING_CURVATURE_BOUNDARY_PAYLOAD",
            "lambda_kernel_score": "MISSING_LAMBDA_KERNEL_PAYLOAD",
            "EM_overlap_score": "MISSING_EM_OVERLAP_GUARD",
            "lambda_curvature_source_score": "MISSING_LAMBDA_CURVATURE_SOURCE",
            "delta_threshold": "MISSING_ARENA_THRESHOLD",
            "source_path": "MISSING_SOURCE_PATH",
            "same_support_certificate": "MISSING_SUPPORT_CERTIFICATE",
            "no_cancellation_guard": "False",
            "input_valid_for_claim": "False",
            "notes": "Live evidence is still absent; this row must block.",
        },
        {
            "payload_id": "FPV4400_1_numeric_schema_smoke_nonclaim",
            "target": "runner_schema_only",
            "R_S_score": "0.001",
            "J_U_score": "0.0015",
            "pressure_aniso_score": "0.001",
            "curvature_boundary_score": "0.001",
            "lambda_kernel_score": "0.0005",
            "EM_overlap_score": "0.0002",
            "lambda_curvature_source_score": "0.001",
            "delta_threshold": "0.01",
            "source_path": str(GENERATOR_PATH),
            "same_support_certificate": str(GENERATOR_PATH),
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row proving the absolute-sum runner accepts clean numeric schema but refuses input_valid=false.",
        },
        {
            "payload_id": "FPV4400_2_numeric_threshold_fail_nonclaim",
            "target": "runner_threshold_fail",
            "R_S_score": "0.02",
            "J_U_score": "0.01",
            "pressure_aniso_score": "0.01",
            "curvature_boundary_score": "0.01",
            "lambda_kernel_score": "0.01",
            "EM_overlap_score": "0.01",
            "lambda_curvature_source_score": "0.02",
            "delta_threshold": "0.01",
            "source_path": str(GENERATOR_PATH),
            "same_support_certificate": str(GENERATOR_PATH),
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row proving a sourced numeric payload above threshold fails.",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    gates = {
        "composite_US_parent_functional": "the best composite route is written but parent Phi equations, Ward closure, EM guard, and curvature-sourced lambda handling are unsigned",
        "sigma_multiplier_null": "the old lambda_S=0 lemma does not survive coupling to U[sigma]R unless the new curvature source cancels or is bounded",
        "finite_payload_vector": "runner exists, but no real sourced same-support payload vector has been supplied",
        "local_GR_Newton_PPN": "local GR/Newton/PPN remain blocked until parent cancellation or finite payload vector passes",
        "R10_clock_orbital": "short-range, clock, and orbital claims remain blocked because the same local payload inputs are missing",
    }
    return [
        {
            "gate_id": f"CG4400_{index}_{arena}",
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
            "decision_id": "DEC4400_0",
            "decision": DECISION,
            "summary": "4400 makes the composite U/S fork executable and derives the next real obstruction. Composite U/S[Phi] avoids the 4399 independent-curvature-multiplier no-go, and the minimal sigma trace-electric candidate is now explicit. But once the sigma constraint is coupled to U[sigma]R, the sigma variation sources lambda_S by an electric-curvature term, so the old multiplier-null lemma is no longer free. The branch now needs either parent cancellation of that curvature source or a finite lambda-curvature payload bound. A no-cancellation finite payload vector runner has been installed for the fallback route.",
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
            "summary": "composite U/S route written; curvature-sourced lambda obstruction derived; finite payload runner installed.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4400_0",
            "target": NEXT_TARGET,
            "question": "Can the curvature-sourced lambda_S term be parent-cancelled, or must it be bounded as part of the finite payload vector?",
            "preferred_route": "try parent cancellation first by checking whether the same parent stress-improvement sector that owns delta rho_topH also contributes an opposite sigma equation source.",
            "fallback_route": "derive an elliptic estimate ||lambda_S|| <= C_Delta ||Pi_W(R.dU/dsigma)|| and convert it into a local PPN/R10 payload row.",
            "avoid": "reusing the 4393 multiplier-null lemma after adding U[sigma]R without accounting for the curvature source.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    composite_output: List[Dict[str, str]],
    payload_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 416 PPC4161 transition: composite U/S parent functional or finite payload vector runner

Marker: `{MARKER}`

## Result

4400 is not another missing-list pass. It does two forward things:

1. writes the actual composite `U/S[Phi]` route that avoids the 4399 pure-linear overconstraint;
2. derives the next obstruction created by that route: the sigma/lambda multiplier is curvature-sourced once `U[sigma_S]R` is included.

The minimal composite candidate is

`u^mu = tau_obs^mu / sqrt(-g_obs(tau_obs,tau_obs))`

`S^{{ij}} = c^2 h^{{ij}} sigma_S`

with the electric `U[u,S]` from the 4390-4391 branch and the sigma constraint from 4393.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"

    text += "\n## Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"

    text += """## The New Local Equation

Start from the combined local candidate

`S_tot = int_W sqrt(h) lambda_S(Delta_h sigma_S - delta rho_topH) + 1/2 int_M sqrt(-g) U[sigma_S]^{mu alpha nu beta} R_{mu alpha nu beta}`.

Varying `sigma_S` gives

`Delta_h^dagger lambda_S = -1/2 Pi_W[(sqrt(-g)/sqrt(h)) R_{mu alpha nu beta} partial U^{mu alpha nu beta}/partial sigma_S] + boundary/projector terms`.

For the trace-electric candidate this contains

`c^2 h^{ij} R_{0i0j}`

up to projection and connection payloads. That means `lambda_S=0` is no longer automatic. The route is still alive, but it now has an honest next target: parent-cancel or bound this curvature source.

## Composite Gate Output

"""
    for row in composite_output:
        text += f"- `{row['candidate_id']}`: functional_ready=`{row['functional_ready']}`, projection_ready=`{row['projection_ready']}`, dynamics_ready=`{row['dynamics_ready']}`, lambda_safe=`{row['lambda_safe']}`, curvature_sourced_lambda_obstruction=`{row['curvature_sourced_lambda_obstruction']}`, certificate_ready=`{row['composite_certificate_ready']}`, status=`{row['current_status']}`.\n"

    text += "\n## Finite Payload Runner Output\n\n"
    for row in payload_output:
        text += f"- `{row['payload_id']}`: schema_ready=`{row['schema_ready']}`, support_ready=`{row['support_ready']}`, total_payload_score=`{row['total_payload_score']}`, threshold=`{row['delta_threshold']}`, claim_allowed=`{row['claim_allowed']}`, status=`{row['current_status']}`.\n"

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
        f"""# 4400 Y5 R2FR: composite U/S parent functional or finite payload vector runner

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
## 4400 local spine update: composite U/S route and curvature-sourced lambda payload

Marker: `{MARKER}`

Spine update: the composite route `U/S[Phi]` is now the preferred local-GR branch because it avoids the pure independent `U.R` curvature-multiplier no-go. The minimal candidate uses the existing tau/coframe flow plus `S^{{ij}}=c^2h^{{ij}}sigma_S`. However, coupling this to `U[sigma_S]R` sources the sigma multiplier equation by an electric-curvature term, so `lambda_S=0` is not free anymore. The spine must now either derive parent cancellation of that source or pass a finite absolute payload vector.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4400 packet update: composite route executable, lambda-curvature payload exposed

Marker: `{PACKET_MARKER}`

Packet update: 4400 installs the composite U/S parent-functional gate and a no-cancellation finite payload vector runner. It also derives the exact reason the sigma/lambda branch cannot reuse the multiplier-null lemma after adding `U[sigma_S]R`: the sigma equation gains a curvature source.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4400 makes the composite U/S fork executable and derives the next real obstruction. Composite U/S[Phi] avoids the 4399 independent-curvature-multiplier no-go, and the minimal trace-electric sigma candidate is explicit: u from tau/coframe, S^{ij}=c^2 h^{ij} sigma_S, and U[u,S]. But coupling the sigma constraint to U[sigma]R sources the lambda_S equation by an electric-curvature term, so the earlier multiplier-null lemma is not automatically available. A finite no-cancellation payload vector runner is installed. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4400 source register, composite derivation rows, composite U/S gate input/output, finite payload vector input/output, claim gates, decision, status, next target and validation CSV.",
            "composite_US_route_written_curvature_sourced_lambda_payload_exposed_nonclaim",
            "Parent-cancel the curvature-sourced lambda term or derive/source a finite payload bound for it.",
            "Reusing lambda_S=0 after adding U[sigma]R, claiming from a post-readout Green inverse, or hiding payload cancellations.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4400_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4400_COMPOSITE_US_DERIVATIONS.csv")
    composite_output = read_csv(COMPOSITE_OUTPUT_PATH)
    payload_output = read_csv(PAYLOAD_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4400_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4400_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4400_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4400_2_composite_variation_written", any(row["derivation_id"] == "CUS4400_0_composite_variation_not_independent_U" for row in derivations), "composite variation route written")
    add("VAL4400_3_sigma_candidate_written", any(row["derivation_id"] == "CUS4400_1_sigma_trace_candidate_functional" for row in derivations), "sigma trace candidate written")
    add("VAL4400_4_lambda_obstruction_written", any(row["derivation_id"] == "CUS4400_2_curvature_sourced_lambda_obstruction" for row in derivations), "curvature-sourced lambda obstruction derived")
    add("VAL4400_5_payload_vector_written", any(row["derivation_id"] == "CUS4400_3_no_cancellation_payload_vector" for row in derivations), "finite payload vector definition written")
    add("VAL4400_6_composite_gate_nonclaim", all(row["valid_for_claim"] == "False" for row in composite_output), "composite gate remains nonclaim")
    add("VAL4400_7_sigma_obstruction_detected", any(row["candidate_id"] == "CUSG4400_0_sigma_trace_composite_U_candidate" and row["curvature_sourced_lambda_obstruction"] == "True" for row in composite_output), "sigma composite obstruction detected")
    add("VAL4400_8_payload_schema_smoke_ready", any(row["payload_id"] == "FPV4400_1_numeric_schema_smoke_nonclaim" and row["schema_ready"] == "True" and row["payload_within_threshold"] == "True" for row in payload_output), "numeric smoke row computes below threshold")
    add("VAL4400_9_payload_threshold_fail_detected", any(row["payload_id"] == "FPV4400_2_numeric_threshold_fail_nonclaim" and row["current_status"] == "FINITE_PAYLOAD_VECTOR_FAILS_THRESHOLD" for row in payload_output), "threshold fail row detected")
    add("VAL4400_10_missing_payload_blocked", any(row["payload_id"] == "FPV4400_0_missing_real_payload_vector" and row["schema_ready"] == "False" for row in payload_output), "missing real payload row blocked")
    add("VAL4400_11_payload_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in payload_output), "payload runner rows remain nonclaim")
    add("VAL4400_12_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4400_13_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4400_14_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4400_15_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4400_16_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4400_17_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4400_18_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4400_19_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4400_20_composite_gate_exists", COMPOSITE_GATE_PATH.exists() and "def evaluate_composite_rows" in read_text(COMPOSITE_GATE_PATH), "composite gate exists")
    add("VAL4400_21_payload_runner_exists", PAYLOAD_RUNNER_PATH.exists() and "def evaluate_payload_rows" in read_text(PAYLOAD_RUNNER_PATH), "payload runner exists")
    add("VAL4400_22_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = derivation_rows()
    composite_inputs = composite_input_rows()
    payload_inputs = payload_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_paths: List[Path] = [COMPOSITE_INPUT_PATH, PAYLOAD_INPUT_PATH]
    write_csv(COMPOSITE_INPUT_PATH, composite_inputs)
    composite_output = evaluate_composite_rows(COMPOSITE_INPUT_PATH)
    write_csv(COMPOSITE_OUTPUT_PATH, composite_output)
    csv_paths.append(COMPOSITE_OUTPUT_PATH)

    write_csv(PAYLOAD_INPUT_PATH, payload_inputs)
    payload_output = evaluate_payload_rows(PAYLOAD_INPUT_PATH)
    write_csv(PAYLOAD_OUTPUT_PATH, payload_output)
    csv_paths.append(PAYLOAD_OUTPUT_PATH)

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4400_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4400_COMPOSITE_US_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4400_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4400_DECISION.csv": decisions,
        "P8_Y5_R2FR_4400_STATUS.csv": statuses,
        "P8_Y5_R2FR_4400_NEXT_TARGET.csv": next_targets,
    }

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, derivations, composite_output, payload_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
