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
from lambda_curvature_source_gate import read_csv, write_csv  # noqa: E402
from ricci_uu_source_bound_runner import evaluate_bound_rows, evaluate_equation_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4402"
CLAIM_ID = "L-243"
MARKER = "PPC4161_TRANSITION_RICCI_UU_LOCAL_VACUUM_EQUATION_OR_FIRST_REAL_ETRACE_BOUND_ROW_4402"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_RICCI_UU_LOCAL_VACUUM_EQUATION_OR_FIRST_REAL_ETRACE_BOUND_ROW_4402"
DECISION = "RICCI_UU_TRACE_REVERSAL_LAW_DERIVED_LAMBDA_RESIDUALS_EXPOSED_SOURCE_BOUND_RUNNER_READY"
NEXT_TARGET = "4403-Y5-R2FR-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"

FORMAL_PATH = FORMAL / "418-PPC4161-transition-Ricci-uu-local-vacuum-equation-or-first-real-Etrace-bound-row.md"
DOC_PATH = POST / "4402-Y5-R2FR-transition-Ricci-uu-local-vacuum-equation-or-first-real-Etrace-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4402_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

RICCI_RUNNER_PATH = SCRIPT_DIR / "ricci_uu_source_bound_runner.py"
LAMBDA_GATE_PATH = SCRIPT_DIR / "lambda_curvature_source_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4402_transition_Ricci_uu_local_vacuum_equation_or_first_real_Etrace_bound_row.py"

EQUATION_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4402_RICCI_UU_EQUATION_INPUT.csv"
EQUATION_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4402_RICCI_UU_EQUATION_OUTPUT.csv"
BOUND_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4402_RICCI_UU_SOURCE_BOUND_INPUT.csv"
BOUND_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4402_RICCI_UU_SOURCE_BOUND_OUTPUT.csv"
LAMBDA_BOUND_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4402_LAMBDA_BOUND_FROM_RICCI_INPUT.csv"
LAMBDA_BOUND_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4402_LAMBDA_BOUND_FROM_RICCI_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_NEXT_TARGET.csv"
DERIVATIONS_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_LAMBDA_SOURCE_DERIVATIONS.csv"
RICCI_GATE_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_RICCI_ZERO_GATE_OUTPUT.csv"
BOUND_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_LAMBDA_CURVATURE_BOUND_OUTPUT.csv"
FORMAL_294 = FORMAL / "294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md"
FORMAL_181 = FORMAL / "181-PPC4161-kappa-G-normalization-gate.md"
FORMAL_187 = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_247 = FORMAL / "247-PPC4161-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4402_0_4401_next": (
        NEXT_4401,
        "4402-Y5-R2FR-transition-Ricci-uu-local-vacuum-equation-or-first-real-Etrace-bound-row.md",
        "4401 handoff to Ricci_uu local-vacuum equation or first E_trace bound.",
    ),
    "SRC4402_1_4401_derivation": (
        DERIVATIONS_4401,
        "LCS4401_0_trace_electric_source_is_Ricci_uu",
        "4401 source classification as Ricci_uu.",
    ),
    "SRC4402_2_4401_ricci_gate": (
        RICCI_GATE_4401,
        "RICCI_TRACE_SOURCE_IDENTIFIED_PARENT_VACUUM_EQUATION_UNSIGNED",
        "4401 Ricci-zero gate showing parent metric equation unsigned.",
    ),
    "SRC4402_3_4401_bound": (
        BOUND_4401,
        "LCB4401_1_numeric_elliptic_bound_smoke_nonclaim",
        "4401 elliptic lambda bound output.",
    ),
    "SRC4402_4_294_left_hand": (
        FORMAL_294,
        "G_mu_nu[g_obs] + Lambda_eff g_mu_nu",
        "4278 left-hand EH/Newton residual equation.",
    ),
    "SRC4402_5_181_kappa": (
        FORMAL_181,
        "G_mu_nu(g_obs) = kappa_eff T^H_mu_nu + residual_mu_nu",
        "kappa/G normalization gate with residual tensor.",
    ),
    "SRC4402_6_187_newton": (
        FORMAL_187,
        "G_munu = kappa_eff T_H_munu",
        "Poisson/Gauss/Newton readout inside private branch.",
    ),
    "SRC4402_7_194_coupling": (
        FORMAL_194,
        "D_A ln kappa_eff = 0",
        "calibrated source-coupling constancy condition.",
    ),
    "SRC4402_8_247_scorecard": (
        FORMAL_247,
        "G_munu[g_obs] = kappa_eff T_H_munu",
        "local GR scorecard conditional branch.",
    ),
    "SRC4402_9_ricci_runner": (
        RICCI_RUNNER_PATH,
        "def evaluate_bound_rows",
        "New Ricci_uu source-bound runner.",
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
            "derivation_id": "RUU4402_0_trace_reversal_from_EH_residual_equation",
            "statement": "From the conditional local equation G_munu + Lambda_eff g_munu = kappa_eff T_H_munu + E_res_munu, the Ricci-normal source is trace-reversed, not simply G_uu.",
            "derivation": "In four dimensions, trace gives -R + 4 Lambda_eff = kappa_eff T_H + E_res. Therefore R_munu = kappa_eff(T_H_munu - 1/2 g_munu T_H) + (E_res_munu - 1/2 g_munu E_res) + Lambda_eff g_munu. Contracting with u^mu u^nu gives the source for the 4401 lambda equation.",
            "new_information": "The lambda source depends on matter trace, residual trace, and Lambda_eff; these cannot be silently dropped.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "RUU4402_1_exact_local_vacuum_zero_requires_Lambda_and_residual_silence",
            "statement": "Even in local matter vacuum, R_uu=0 only follows if Lambda_eff and the residual tensor vanish or are bounded below the arena tolerance on the same support.",
            "derivation": "Set T_H_munu=0 in the trace-reversed equation. Then R_uu = E_res_uu - 1/2 g_uu E_res + Lambda_eff g_uu. For a unit timelike u this is not exactly zero unless the residual and local Lambda terms are zero or explicitly negligible.",
            "new_information": "The next obstruction is no longer broad local GR; it is the local Lambda/residual payload.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "RUU4402_2_absolute_Etrace_source_bound",
            "statement": "A no-cancellation source bound is |F_E| <= K_E c^2 [kappa_eff(|T_uu|+1/2|T|)+|E_uu|+1/2|E|+|Lambda_eff|+|B_proj|].",
            "derivation": "Apply the triangle inequality to the trace-reversed R_uu expression and then multiply by the absolute trace-electric coefficient K_E c^2 from 4401. This produces a first real source-row schema for the lambda curvature runner.",
            "new_information": "If parent zero cannot be derived, the exact quantities needed for the first E_trace/Ricci_uu row are now named.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "RUU4402_3_EH_import_guard",
            "statement": "The trace-reversal law can be used only inside the conditional EH/EC selector branch or as a bound template; it is not a proof that MTS has derived local GR.",
            "derivation": "The existing PPC4161 chain treats EH/Newton/PPN as a private selector branch with residual EFT forks. Therefore the Ricci_uu zero row needs the selector, same Hilbert source, kappa constancy, residual silence, local Lambda silence, and same tau/coframe support.",
            "new_information": "The route stays honest: conditional GR infrastructure is separated from parent MTS derivation.",
            "valid_for_claim": "False",
        },
    ]


def equation_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "REQ4402_0_trace_reversal_formula",
            "route": "EH_residual_equation_trace_reversal",
            "EH_or_EC_selector_signed": "False",
            "trace_reversal_written": "True",
            "kappa_eff_constant": "True",
            "same_Hilbert_source": "True",
            "local_vacuum_T_zero": "False",
            "residual_tensor_zero_or_bounded": "False",
            "Lambda_eff_zero_or_bounded": "False",
            "same_tau_coframe_support": "False",
            "boundary_projector_silent": "False",
            "parent_authority": "MISSING_PARENT_SIGNED_EH_SELECTOR",
            "source_path": str(FORMAL_294),
            "input_valid_for_claim": "False",
            "notes": "Trace-reversal law is written, but this is not a local-vacuum zero certificate.",
        },
        {
            "candidate_id": "REQ4402_1_private_selector_vacuum_template",
            "route": "conditional_EH_selector_local_vacuum_Ricci_uu",
            "EH_or_EC_selector_signed": "False",
            "trace_reversal_written": "True",
            "kappa_eff_constant": "True",
            "same_Hilbert_source": "True",
            "local_vacuum_T_zero": "True",
            "residual_tensor_zero_or_bounded": "True",
            "Lambda_eff_zero_or_bounded": "True",
            "same_tau_coframe_support": "True",
            "boundary_projector_silent": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_LOCAL_EH_SELECTOR",
            "source_path": str(FORMAL_247),
            "input_valid_for_claim": "False",
            "notes": "This is the clean branch if the selector/residual/Lambda clauses become parent-signed.",
        },
        {
            "candidate_id": "REQ4402_2_effective_GR_import_trap",
            "route": "import_GR_vacuum_equation_without_parent_selector",
            "EH_or_EC_selector_signed": "False",
            "trace_reversal_written": "False",
            "kappa_eff_constant": "False",
            "same_Hilbert_source": "False",
            "local_vacuum_T_zero": "True",
            "residual_tensor_zero_or_bounded": "False",
            "Lambda_eff_zero_or_bounded": "False",
            "same_tau_coframe_support": "False",
            "boundary_projector_silent": "False",
            "parent_authority": "NO_AUTHORITY_EH_IMPORT_ONLY",
            "source_path": str(FORMAL_187),
            "input_valid_for_claim": "False",
            "notes": "Known GR vacuum equations are a reference pattern, not a parent MTS proof.",
        },
    ]


def ricci_bound_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "RUB4402_0_missing_live_Ricci_uu_source_bound",
            "arena": "local_GR_Newton_PPN",
            "kappa_eff_abs": "MISSING_KAPPA_EFF",
            "T_uu_norm": "MISSING_TUU",
            "T_trace_norm": "MISSING_TTRACE",
            "E_res_uu_norm": "MISSING_EUU",
            "E_res_trace_norm": "MISSING_ETRACE",
            "Lambda_eff_abs": "MISSING_LAMBDA_EFF",
            "projector_boundary_abs": "MISSING_PROJECTOR_BOUNDARY",
            "K_E_c2_abs": "MISSING_TRACE_ELECTRIC_COEFFICIENT",
            "F_E_threshold": "MISSING_THRESHOLD",
            "source_path": "MISSING_SOURCE_PATH",
            "support_certificate_path": "MISSING_SUPPORT_CERTIFICATE",
            "input_valid_for_claim": "False",
            "notes": "Live row needs real source/residual/Lambda/projector inputs.",
        },
        {
            "bound_id": "RUB4402_1_exact_zero_schema_nonclaim",
            "arena": "local_vacuum_zero_schema",
            "kappa_eff_abs": "1.0",
            "T_uu_norm": "0.0",
            "T_trace_norm": "0.0",
            "E_res_uu_norm": "0.0",
            "E_res_trace_norm": "0.0",
            "Lambda_eff_abs": "0.0",
            "projector_boundary_abs": "0.0",
            "K_E_c2_abs": "1.0",
            "F_E_threshold": "0.000001",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim zero schema row: shows exact zero would pass the arithmetic if parent-signed.",
        },
        {
            "bound_id": "RUB4402_2_small_residual_schema_nonclaim",
            "arena": "small_residual_bound_schema",
            "kappa_eff_abs": "1.0",
            "T_uu_norm": "0.0",
            "T_trace_norm": "0.0",
            "E_res_uu_norm": "0.001",
            "E_res_trace_norm": "0.002",
            "Lambda_eff_abs": "0.0005",
            "projector_boundary_abs": "0.0005",
            "K_E_c2_abs": "1.0",
            "F_E_threshold": "0.01",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row for a small residual/Lambda payload.",
        },
        {
            "bound_id": "RUB4402_3_large_residual_fail_nonclaim",
            "arena": "large_residual_fail_schema",
            "kappa_eff_abs": "1.0",
            "T_uu_norm": "0.0",
            "T_trace_norm": "0.0",
            "E_res_uu_norm": "0.02",
            "E_res_trace_norm": "0.02",
            "Lambda_eff_abs": "0.01",
            "projector_boundary_abs": "0.01",
            "K_E_c2_abs": "1.0",
            "F_E_threshold": "0.005",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim row proving the bound fails when residuals exceed tolerance.",
        },
    ]


def lambda_bound_input_rows(ricci_bound_output: List[Dict[str, str]]) -> List[Dict[str, str]]:
    small_row = next(row for row in ricci_bound_output if row["bound_id"] == "RUB4402_2_small_residual_schema_nonclaim")
    return [
        {
            "bound_id": "LCB4402_0_lambda_from_Ricci_small_residual_nonclaim",
            "arena": "lambda_bound_from_Ricci_source_schema",
            "F_E_norm": small_row["F_E_norm"],
            "C_poincare": "1.0",
            "C_elliptic_H2": "2.0",
            "K_lambda_stress": "1.0",
            "K_projection": "1.0",
            "arena_threshold": "0.02",
            "boundary_condition": "zero_mean_Neumann",
            "zero_mode_fixed": "True",
            "boundary_flux_silent": "True",
            "source_path": str(BOUND_OUTPUT_PATH),
            "support_certificate_path": str(BOUND_OUTPUT_PATH),
            "input_valid_for_claim": "False",
            "notes": "Consumes the 4402 Ricci_uu source-bound score inside the 4401 lambda elliptic runner.",
        }
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    gates = {
        "Ricci_uu_trace_reversal": "formula is derived, but selector and parent authority are unsigned",
        "local_vacuum_zero": "exact R_uu=0 requires residual tensor and Lambda_eff silence on the same support",
        "first_Etrace_bound_row": "runner is ready, but live source/residual/Lambda/projector rows are still missing",
        "lambda_payload": "lambda bound can consume Ricci source scores, but current rows are smoke/nonclaim",
        "local_GR_Newton_PPN": "local claims remain conditional on selector adoption or real residual bounds",
    }
    return [
        {
            "gate_id": f"CG4402_{index}_{arena}",
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
            "decision_id": "DEC4402_0",
            "decision": DECISION,
            "summary": "4402 derives the trace-reversed Ricci_uu law from the conditional local EH/residual equation. This clarifies that local-vacuum lambda silence needs more than T=0: Lambda_eff and residual tensor pieces must vanish or be bounded on the same tau/coframe support. A Ricci_uu source-bound runner now computes F_E from matter, residual, Lambda and projector terms, and the 4401 lambda elliptic runner can consume that score. No local-GR/Newton/PPN claim fires because selector authority and live residual/Lambda inputs remain unsigned.",
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
            "summary": "trace-reversed Ricci_uu law derived; Lambda/residual payload exposed; source-bound runner ready.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4402_0",
            "target": NEXT_TARGET,
            "question": "Can Lambda_eff and the local residual tensor be parent-zeroed on the same support, or must they be scored as the first real local cosmological/residual payload?",
            "preferred_route": "try deriving local Lambda_eff silence and residual tensor zero from the existing PPC4161 selector/residual EFT gates.",
            "fallback_route": "source finite Lambda_eff, E_res_uu, E_res_trace and projector-bound rows and run them through the Ricci_uu and lambda payload runners.",
            "avoid": "claiming R_uu=0 from matter vacuum alone while Lambda_eff or E_res terms remain open.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    equation_output: List[Dict[str, str]],
    ricci_bound_output: List[Dict[str, str]],
    lambda_bound_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 418 PPC4161 transition: Ricci_uu local-vacuum equation or first real Etrace bound row

Marker: `{MARKER}`

## Result

4402 derives the actual source equation needed after 4401.

Start from the conditional left-hand branch:

`G_munu[g_obs] + Lambda_eff g_munu = kappa_eff T_H_munu + E_res_munu`.

Trace reversal gives

`R_munu = kappa_eff(T_H_munu - 1/2 g_munu T_H) + (E_res_munu - 1/2 g_munu E_res) + Lambda_eff g_munu`.

Therefore the lambda source is not zero just because we are outside ordinary matter. In local matter vacuum,

`R_uu = E_res_uu - 1/2 g_uu E_res + Lambda_eff g_uu`.

So the next payload is sharply named: `Lambda_eff`, `E_res_uu`, `E_res_trace`, and projector/boundary terms.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"

    text += "\n## Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"

    text += "\n## Ricci Equation Gate\n\n"
    for row in equation_output:
        text += f"- `{row['candidate_id']}`: trace_reversal_ready=`{row['trace_reversal_ready']}`, vacuum_ready=`{row['vacuum_ready']}`, residual_ready=`{row['residual_ready']}`, selector_ready=`{row['selector_ready']}`, certificate_ready=`{row['ricci_equation_certificate_ready']}`, status=`{row['current_status']}`.\n"

    text += "\n## Ricci Source-Bound Runner\n\n"
    text += "`|F_E| <= K_E c^2 [kappa_eff(|T_uu|+1/2|T|)+|E_uu|+1/2|E|+|Lambda_eff|+|B_proj|]`\n\n"
    for row in ricci_bound_output:
        text += f"- `{row['bound_id']}`: schema_ready=`{row['schema_ready']}`, Ruu_abs_bound=`{row['Ruu_abs_bound']}`, F_E_norm=`{row['F_E_norm']}`, threshold=`{row['F_E_threshold']}`, status=`{row['current_status']}`.\n"

    text += "\n## Lambda Bound From Ricci Source\n\n"
    for row in lambda_bound_output:
        text += f"- `{row['bound_id']}`: schema_ready=`{row['schema_ready']}`, payload_score=`{row['lambda_curvature_payload_score']}`, threshold=`{row['arena_threshold']}`, status=`{row['current_status']}`.\n"

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
        f"""# 4402 Y5 R2FR: Ricci_uu local-vacuum equation or first real Etrace bound row

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
## 4402 local spine update: Ricci_uu trace reversal exposes Lambda/residual payload

Marker: `{MARKER}`

Spine update: the `R_uu` source from 4401 is now trace-reversed through the conditional local EH/residual equation. Matter vacuum alone is insufficient: exact `R_uu=0` also needs local `Lambda_eff` and residual tensor silence on the same tau/coframe support. The fallback is now executable as a Ricci source-bound row feeding the lambda elliptic payload runner.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4402 packet update: first Ricci_uu source-bound runner

Marker: `{PACKET_MARKER}`

Packet update: 4402 derives the trace-reversed `R_uu` source law and adds a runner for matter, residual, `Lambda_eff`, and projector-boundary contributions to the lambda curvature payload.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4402 derives the trace-reversed Ricci_uu law from the conditional local EH/residual equation G+Lambda_eff g=kappa_eff T_H+E_res. It shows that matter vacuum alone does not imply R_uu=0: local Lambda_eff and residual tensor terms must vanish or be bounded on the same tau/coframe support. A Ricci_uu source-bound runner now computes F_E from matter, residual, Lambda and projector terms and can feed the lambda elliptic payload runner. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4402 source register, trace-reversal derivations, Ricci equation gate, Ricci source-bound runner, lambda-bound-from-Ricci rows, claim gates, decision, status, next target and validation CSV.",
            "Ricci_uu_trace_reversal_law_and_source_bound_runner_ready_nonclaim",
            "Derive local Lambda_eff/residual silence or source real residual/Lambda/projector rows.",
            "Claiming R_uu=0 from matter vacuum alone, importing EH without selector authority, or dropping Lambda_eff/E_res traces.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4402_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4402_RICCI_UU_DERIVATIONS.csv")
    equation_output = read_csv(EQUATION_OUTPUT_PATH)
    ricci_bound_output = read_csv(BOUND_OUTPUT_PATH)
    lambda_bound_output = read_csv(LAMBDA_BOUND_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4402_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4402_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4402_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4402_2_trace_reversal_written", any(row["derivation_id"] == "RUU4402_0_trace_reversal_from_EH_residual_equation" for row in derivations), "trace reversal written")
    add("VAL4402_3_lambda_residual_exposed", any(row["derivation_id"] == "RUU4402_1_exact_local_vacuum_zero_requires_Lambda_and_residual_silence" for row in derivations), "Lambda/residual silence required")
    add("VAL4402_4_source_bound_written", any(row["derivation_id"] == "RUU4402_2_absolute_Etrace_source_bound" for row in derivations), "absolute source bound written")
    add("VAL4402_5_equation_gate_nonclaim", all(row["valid_for_claim"] == "False" for row in equation_output), "equation gate remains nonclaim")
    add("VAL4402_6_private_template_ready_unsigned", any(row["candidate_id"] == "REQ4402_1_private_selector_vacuum_template" and row["current_status"] == "RICCI_UU_FORMULA_READY_SELECTOR_OR_AUTHORITY_UNSIGNED" for row in equation_output), "private selector template ready but unsigned")
    add("VAL4402_7_zero_schema_computes", any(row["bound_id"] == "RUB4402_1_exact_zero_schema_nonclaim" and row["F_E_norm"] == "0" for row in ricci_bound_output), "exact zero schema computes")
    add("VAL4402_8_small_residual_computes", any(row["bound_id"] == "RUB4402_2_small_residual_schema_nonclaim" and row["schema_ready"] == "True" and row["within_threshold"] == "True" for row in ricci_bound_output), "small residual row computes")
    add("VAL4402_9_large_residual_fails", any(row["bound_id"] == "RUB4402_3_large_residual_fail_nonclaim" and row["current_status"] == "RICCI_UU_SOURCE_BOUND_FAILS_THRESHOLD" for row in ricci_bound_output), "large residual row fails threshold")
    add("VAL4402_10_ricci_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in ricci_bound_output), "Ricci bound rows remain nonclaim")
    add("VAL4402_11_lambda_consumes_ricci", any(row["bound_id"] == "LCB4402_0_lambda_from_Ricci_small_residual_nonclaim" and row["schema_ready"] == "True" for row in lambda_bound_output), "lambda bound consumes Ricci source score")
    add("VAL4402_12_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4402_13_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4402_14_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4402_15_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4402_16_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4402_17_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4402_18_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4402_19_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4402_20_runner_exists", RICCI_RUNNER_PATH.exists() and "def evaluate_bound_rows" in read_text(RICCI_RUNNER_PATH), "Ricci runner exists")
    add("VAL4402_21_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = derivation_rows()
    equation_inputs = equation_input_rows()
    ricci_bound_inputs = ricci_bound_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_paths: List[Path] = [EQUATION_INPUT_PATH, BOUND_INPUT_PATH]

    write_csv(EQUATION_INPUT_PATH, equation_inputs)
    equation_output = evaluate_equation_rows(EQUATION_INPUT_PATH)
    write_csv(EQUATION_OUTPUT_PATH, equation_output)
    csv_paths.append(EQUATION_OUTPUT_PATH)

    write_csv(BOUND_INPUT_PATH, ricci_bound_inputs)
    ricci_bound_output = evaluate_bound_rows(BOUND_INPUT_PATH)
    write_csv(BOUND_OUTPUT_PATH, ricci_bound_output)
    csv_paths.append(BOUND_OUTPUT_PATH)

    lambda_inputs = lambda_bound_input_rows(ricci_bound_output)
    write_csv(LAMBDA_BOUND_INPUT_PATH, lambda_inputs)
    lambda_bound_output = evaluate_lambda_bound_rows(LAMBDA_BOUND_INPUT_PATH)
    write_csv(LAMBDA_BOUND_OUTPUT_PATH, lambda_bound_output)
    csv_paths.extend([LAMBDA_BOUND_INPUT_PATH, LAMBDA_BOUND_OUTPUT_PATH])

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4402_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4402_RICCI_UU_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4402_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4402_DECISION.csv": decisions,
        "P8_Y5_R2FR_4402_STATUS.csv": statuses,
        "P8_Y5_R2FR_4402_NEXT_TARGET.csv": next_targets,
    }

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(
        sources,
        derivations,
        equation_output,
        ricci_bound_output,
        lambda_bound_output,
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
