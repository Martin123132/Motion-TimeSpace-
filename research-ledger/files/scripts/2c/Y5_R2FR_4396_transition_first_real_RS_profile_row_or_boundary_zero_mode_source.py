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

from sigma_s_RS_bound_runner import evaluate_bound_rows, read_csv, write_csv  # noqa: E402
from sigma_s_RS_source_row_gate import evaluate_source_rows  # noqa: E402
from sigma_s_boundary_zero_mode_gate import evaluate_boundary_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4396"
CLAIM_ID = "L-237"
MARKER = "PPC4161_TRANSITION_FIRST_REAL_RS_PROFILE_ROW_OR_BOUNDARY_ZERO_MODE_SOURCE_4396"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_FIRST_REAL_RS_PROFILE_ROW_OR_BOUNDARY_ZERO_MODE_SOURCE_4396"
DECISION = "ELLIPTIC_RS_ZERO_MECHANISM_DERIVED_SOURCE_BACKED_ROW_STILL_PARENT_UNSIGNED"
NEXT_TARGET = "4397-Y5-R2FR-transition-parent-source-owner-for-delta-rho-topH-or-finite-RS-profile-norm.md"

FORMAL_PATH = FORMAL / "412-PPC4161-transition-first-real-RS-profile-row-or-boundary-zero-mode-source.md"
DOC_PATH = POST / "4396-Y5-R2FR-transition-first-real-RS-profile-row-or-boundary-zero-mode-source.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4396_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

BOUNDARY_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4396_BOUNDARY_ZERO_MODE_INPUT.csv"
BOUNDARY_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4396_BOUNDARY_ZERO_MODE_OUTPUT.csv"
SOURCE_ROW_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4396_RS_SOURCE_ROW_GATE_INPUT.csv"
SOURCE_ROW_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4396_RS_SOURCE_ROW_GATE_OUTPUT.csv"
BOUND_DRY_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4396_RS_BOUND_RUNNER_DRY_INPUT.csv"
BOUND_DRY_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4396_RS_BOUND_RUNNER_DRY_OUTPUT.csv"

BOUNDARY_GATE_PATH = SCRIPT_DIR / "sigma_s_boundary_zero_mode_gate.py"
SOURCE_ROW_GATE_PATH = SCRIPT_DIR / "sigma_s_RS_source_row_gate.py"
BOUND_RUNNER_PATH = SCRIPT_DIR / "sigma_s_RS_bound_runner.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SIGMA_THEOREMS_4392 = SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_THEOREMS.csv"
STATIC_THEOREMS_4391 = SOURCE_DIR / "P8_Y5_R2FR_4391_PARENT_U_S_THEOREMS.csv"
ACTION_THEOREMS_4393 = SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4396_0_4395_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4395_NEXT_TARGET.csv",
        "4396-Y5-R2FR-transition-first-real-RS-profile-row-or-boundary-zero-mode-source.md",
        "4395 handoff demanding a first source-backed R_S profile row or boundary/zero-mode theorem.",
    ),
    "SRC4396_1_4395_source_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4395_RS_SOURCE_ROW_GATE_OUTPUT.csv",
        "RS4395_0_missing_source_row",
        "4395 source-row gate result proving the missing row was not yet sourced.",
    ),
    "SRC4396_2_4392_sigma_route": (
        SIGMA_THEOREMS_4392,
        "SIGS4392_0_trace_electric_owner",
        "Trace-electric sigma_S owner route and R_S fallback definition.",
    ),
    "SRC4396_3_4392_green_guard": (
        SIGMA_THEOREMS_4392,
        "SIGS4392_2_green_inverse_no_free_claim",
        "No-free-Green-inverse guard for domain, boundary and zero-mode dependence.",
    ),
    "SRC4396_4_4393_action": (
        ACTION_THEOREMS_4393,
        "SACT4393_0_parent_constraint_signature",
        "Sigma/lambda action candidate giving Delta_h sigma_S=delta rho_topH if parent-owned.",
    ),
    "SRC4396_5_4393_multiplier": (
        ACTION_THEOREMS_4393,
        "SACT4393_2_multiplier_null_lemma",
        "Conditional multiplier-null lemma used to silence lambda stress.",
    ),
    "SRC4396_6_4391_tau": (
        STATIC_THEOREMS_4391,
        "UST4391_0_tau_coframe_u_candidate",
        "Tau/coframe U candidate for the same local readout frame.",
    ),
    "SRC4396_7_boundary_gate": (
        BOUNDARY_GATE_PATH,
        "def evaluate_boundary_rows",
        "New executable boundary/zero-mode certificate gate.",
    ),
    "SRC4396_8_source_gate": (
        SOURCE_ROW_GATE_PATH,
        "def evaluate_source_rows",
        "Existing first-real-R_S source-row gate.",
    ),
    "SRC4396_9_bound_runner": (
        BOUND_RUNNER_PATH,
        "def evaluate_bound_rows",
        "Existing tightened R_S bound runner.",
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


def elliptic_derivation_rows() -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "ED4396_0_RS_zero_identity",
            "statement": "On one parent-owned local tau slice W_H, if delta rho_topH:=rho_top-rho_H and sigma_S obey Delta_h sigma_S=delta rho_topH as a parent constraint, then R_S:=delta rho_topH-Delta_h sigma_S is zero pointwise as a distribution on W_H.",
            "derivation": "This is direct substitution, but it is only physical if both terms use the same h, W_H, tau/coframe and density measure before readout.",
            "new_information": "R_S=0 is not a fit; it is an elliptic constraint identity with a same-support requirement.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "ED4396_1_boundary_zero_mode_law",
            "statement": "The Poisson operator needs either a Dirichlet anchor, or a Neumann/closed-domain compatibility condition plus zero-mean gauge fixing; otherwise a constant/harmonic zero mode remains physically unowned.",
            "derivation": "For Dirichlet data, elliptic uniqueness fixes sigma_S. For Neumann data, Delta_h has constants in its kernel and solvability requires int_W delta rho_topH sqrt(h)=int_boundary n^i D_i sigma_S dA; a zero-mean condition then removes the remaining kernel.",
            "new_information": "The boundary/zero-mode issue is now an exact certificate condition, not a vague missing item.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "ED4396_2_multiplier_null_law",
            "statement": "If variation with respect to sigma_S gives Delta_h lambda_S=0 and lambda_S has zero Dirichlet data or zero-mean Neumann gauge with no homogeneous mode, then lambda_S=0 and the multiplier stress payload is silent.",
            "derivation": "Multiply Delta_h lambda_S=0 by lambda_S and integrate by parts: int_W |D lambda_S|^2 sqrt(h) equals the boundary pairing. With anchored boundary or fixed zero mode and silent boundary pairing, D lambda_S=0 and the fixed mode gives lambda_S=0.",
            "new_information": "This gives the exact local suppression law for the lambda payload.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "ED4396_3_claim_ceiling",
            "statement": "The above is still not a local-GR claim until delta rho_topH, W_H, h, tau/coframe, boundary data, zero mode and kernel stress are parent-owned before readout.",
            "derivation": "4392 and 4393 already reject post-readout Green solves. 4396 adds the exact boundary theorem but not the parent owner of the density source.",
            "new_information": "The remaining hard target is now narrowed to parent source ownership or a finite R_S profile norm.",
            "valid_for_claim": "False",
        },
    ]


def boundary_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "BZM4396_0_dirichlet_or_zero_mean_mechanism",
            "route": "elliptic_boundary_zero_mode_mechanism",
            "laplacian_operator_declared": "True",
            "W_H_domain_parent_owned": "False",
            "tau_coframe_same_as_readout": "False",
            "source_density_parent_owned": "False",
            "sigma_boundary_condition_signed": "True",
            "zero_mode_fixed_or_compatibility_signed": "True",
            "lambda_boundary_condition_signed": "True",
            "lambda_zero_mode_fixed": "True",
            "boundary_variation_silent": "False",
            "kernel_stress_zero_or_bounded": "False",
            "no_post_readout_green_solve": "True",
            "parent_authority": "CONDITIONAL_ELLIPTIC_MECHANISM_NOT_PARENT_SIGNED",
            "source_path": str(ACTION_THEOREMS_4393),
            "input_valid_for_claim": "False",
            "notes": "The mathematical zero-mode mechanism is derived, but support/source/boundary ownership is not parent-signed.",
        },
        {
            "candidate_id": "BZM4396_1_neumann_compatibility_trap",
            "route": "neumann_or_closed_domain_without_compatibility",
            "laplacian_operator_declared": "True",
            "W_H_domain_parent_owned": "False",
            "tau_coframe_same_as_readout": "False",
            "source_density_parent_owned": "False",
            "sigma_boundary_condition_signed": "False",
            "zero_mode_fixed_or_compatibility_signed": "False",
            "lambda_boundary_condition_signed": "False",
            "lambda_zero_mode_fixed": "False",
            "boundary_variation_silent": "False",
            "kernel_stress_zero_or_bounded": "False",
            "no_post_readout_green_solve": "True",
            "parent_authority": "NO_PARENT_AUTHORITY",
            "source_path": str(SIGMA_THEOREMS_4392),
            "input_valid_for_claim": "False",
            "notes": "This row proves the gate catches unsupported Neumann/closed-domain zero-mode claims.",
        },
        {
            "candidate_id": "BZM4396_2_parent_signature_template",
            "route": "future_parent_signed_boundary_certificate_template",
            "laplacian_operator_declared": "True",
            "W_H_domain_parent_owned": "False",
            "tau_coframe_same_as_readout": "False",
            "source_density_parent_owned": "False",
            "sigma_boundary_condition_signed": "True",
            "zero_mode_fixed_or_compatibility_signed": "True",
            "lambda_boundary_condition_signed": "True",
            "lambda_zero_mode_fixed": "True",
            "boundary_variation_silent": "False",
            "kernel_stress_zero_or_bounded": "False",
            "no_post_readout_green_solve": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_BOUNDARY_ZERO_MODE_OWNER",
            "source_path": str(ACTION_THEOREMS_4393),
            "input_valid_for_claim": "False",
            "notes": "Template row showing exactly what must be parent-signed in 4397 or later.",
        },
    ]


def source_row_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "RS4396_0_source_backed_conditional_constraint_zero",
            "target": "conditional_R_S_zero_from_sigma_constraint",
            "theorem_zero": "True",
            "theorem_zero_authority": "CONDITIONAL_SIGMA_CONSTRAINT_NOT_PARENT_SIGNED",
            "R_S_weighted_norm": "0.0",
            "R_S_units": "theorem_zero_dimensionless",
            "M_H": "1.0",
            "M_H_units": "dimensionless_normalized_mass",
            "K_N": "1.0",
            "lambda_stress_score": "0.0",
            "kernel_stress_score": "0.0",
            "delta_threshold": "1e-12",
            "source_path": str(ACTION_THEOREMS_4393),
            "source_row_id": "SACT4393_0_parent_constraint_signature",
            "equation_ref": "Delta_h sigma_S = delta rho_topH; R_S := delta rho_topH - Delta_h sigma_S",
            "W_H_geometry_source": str(SIGMA_THEOREMS_4392),
            "same_tau_coframe_certificate": str(STATIC_THEOREMS_4391),
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
            "notes": "First source-backed conditional R_S=0 row; blocked because authority is conditional, not parent-signed.",
        },
        {
            "candidate_id": "RS4396_1_boundary_zero_mode_conditional_zero",
            "target": "conditional_boundary_zero_mode_R_S_zero",
            "theorem_zero": "True",
            "theorem_zero_authority": "CONDITIONAL_BOUNDARY_ZERO_MODE_NOT_PARENT_SIGNED",
            "R_S_weighted_norm": "0.0",
            "R_S_units": "theorem_zero_dimensionless",
            "M_H": "1.0",
            "M_H_units": "dimensionless_normalized_mass",
            "K_N": "1.0",
            "lambda_stress_score": "0.0",
            "kernel_stress_score": "0.0",
            "delta_threshold": "1e-12",
            "source_path": str(BOUNDARY_OUTPUT_PATH),
            "source_row_id": "BZM4396_0_dirichlet_or_zero_mean_mechanism",
            "equation_ref": "elliptic uniqueness plus fixed zero mode gives R_S=0 only if source/support are parent-owned",
            "W_H_geometry_source": str(SIGMA_THEOREMS_4392),
            "same_tau_coframe_certificate": str(STATIC_THEOREMS_4391),
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
            "notes": "Boundary/zero-mode theorem row sourced to the new gate output; nonclaim until parent source/support clauses close.",
        },
        {
            "candidate_id": "RS4396_2_finite_profile_norm_still_missing",
            "target": "finite_R_S_profile_norm",
            "theorem_zero": "False",
            "theorem_zero_authority": "NONE",
            "R_S_weighted_norm": "MISSING_NUMERIC_PROFILE_NORM",
            "R_S_units": "MISSING_R_S_UNITS",
            "M_H": "MISSING_M_H",
            "M_H_units": "MISSING_M_H_UNITS",
            "K_N": "MISSING_K_N",
            "lambda_stress_score": "MISSING_LAMBDA_STRESS_SCORE",
            "kernel_stress_score": "MISSING_KERNEL_STRESS_SCORE",
            "delta_threshold": "MISSING_DELTA_THRESHOLD",
            "source_path": str(SIGMA_THEOREMS_4392),
            "source_row_id": "SIGS4392_4_residual_mismatch_bound",
            "equation_ref": "finite profile norm of R_S on W_H not yet computed",
            "W_H_geometry_source": str(SIGMA_THEOREMS_4392),
            "same_tau_coframe_certificate": str(STATIC_THEOREMS_4391),
            "no_cancellation_guard": "False",
            "input_valid_for_claim": "False",
            "notes": "Finite-profile fallback remains a real numeric target, not a claim.",
        },
    ]


def bound_dry_input_rows(source_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    fields = [
        "candidate_id",
        "target",
        "theorem_zero",
        "theorem_zero_authority",
        "R_S_weighted_norm",
        "M_H",
        "K_N",
        "lambda_stress_score",
        "kernel_stress_score",
        "delta_threshold",
        "source_path",
        "equation_ref",
        "no_cancellation_guard",
        "input_valid_for_claim",
    ]
    return [{field: row.get(field, "") for field in fields} for row in source_rows]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "elliptic_R_S_zero": "mechanism derived, but source/support/boundary ownership is not parent-signed",
        "source_backed_R_S_row": "conditional rows now cite real sources, but theorem-zero authority is not PARENT_SIGNED",
        "finite_profile_bound": "numeric R_S weighted norm, M_H, K_N and stress bounds are not computed",
        "Newton_local_GR": "R_S zero or finite bound is not claim-valid, so local Newton/GR reduction remains open",
        "PPN_clock_R10_WEP": "tau/coframe/static/source coupling clauses remain upstream nonclaim",
    }
    return [
        {
            "gate_id": f"CG4396_{index}_{arena}",
            "arena": arena,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (arena, reason) in enumerate(reasons.items())
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4396_0",
            "decision": DECISION,
            "summary": "4396 derives the exact elliptic route for R_S suppression: if Delta_h sigma_S=delta rho_topH is a parent-owned constraint on one W_H/tau/coframe support, with boundary/zero-mode compatibility and multiplier-null boundary data, then R_S=0 and lambda stress vanishes. The first source-backed conditional R_S=0 rows are now generated from 4392/4393/4391 sources, but they remain nonclaim because the parent source/support owner is unsigned.",
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
            "summary": "elliptic boundary/zero-mode mechanism derived; source-backed conditional R_S rows exist but are not claim-valid.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4396_0",
            "target": NEXT_TARGET,
            "question": "Can we parent-own delta rho_topH as one pre-readout source, or compute a finite R_S profile norm on a declared W_H support?",
            "preferred_route": "attempt parent source-owner derivation for delta rho_topH using variation-before-readout and topological/Hilbert source definitions.",
            "fallback_route": "choose one concrete W_H/tau/coframe support and compute or bound a finite R_S weighted norm, M_H, K_N, lambda stress and kernel stress.",
            "avoid": "using conditional R_S=0 rows as evidence before PARENT_SIGNED source/support authority exists.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    boundary_output: List[Dict[str, str]],
    source_output: List[Dict[str, str]],
    bound_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 412 PPC4161 transition: first real R_S profile row or boundary zero-mode source

Marker: `{MARKER}`

## Result

4396 derives the boundary/zero-mode mechanism instead of merely saying it is missing.

Let

`R_S := delta rho_topH - Delta_h sigma_S`

on one declared local support `W_H` with one tau/coframe and one spatial metric `h`. If the parent action owns `Delta_h sigma_S=delta rho_topH` before readout, then `R_S=0` pointwise. The nontrivial part is not the algebra; it is the certificate that the Laplacian, source density, domain, boundary data, zero mode, lambda multiplier and kernel stress all belong to the same parent object.

The checkpoint creates the first source-backed conditional `R_S=0` rows from the existing 4392/4393/4391 ledgers, and the gates correctly keep them nonclaim because their authority is conditional rather than `PARENT_SIGNED`.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Elliptic Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"
    text += "## Boundary/Zero-Mode Gate Output\n\n"
    for row in boundary_output:
        text += f"- `{row['candidate_id']}`: elliptic_ready=`{row['elliptic_ready']}`, support_ready=`{row['support_ready']}`, source_owner_ready=`{row['source_owner_ready']}`, certificate_ready=`{row['boundary_certificate_ready']}`, authority=`{row['theorem_zero_authority']}`.\n"
    text += "\n## R_S Source-Row Gate Output\n\n"
    for row in source_output:
        text += f"- `{row['candidate_id']}`: schema_ready=`{row['schema_ready']}`, source_ready=`{row['source_ready']}`, ready_for_bound_runner=`{row['ready_for_bound_runner']}`, valid=`{row['valid_for_claim']}`, reasons=`{row['refusal_reasons']}`.\n"
    text += "\n## Bound Runner Dry Output\n\n"
    for row in bound_output:
        text += f"- `{row['candidate_id']}`: pass_bound=`{row['pass_bound']}`, valid=`{row['valid_for_claim']}`, total=`{row['total_score']}`, reasons=`{row['refusal_reasons']}`.\n"
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
        f"""# 4396 Y5 R2FR: first real R_S profile row or boundary zero-mode source

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
## 4396 local spine update: elliptic R_S suppression law

Marker: `{MARKER}`

Spine update: the local `R_S` suppression condition is now exact. On one parent-owned support `W_H`, if `Delta_h sigma_S=delta rho_topH` is owned before readout and boundary/zero-mode conditions close, then `R_S=delta rho_topH-Delta_h sigma_S=0`; if `Delta_h lambda_S=0` with anchored boundary or fixed zero mode, then `lambda_S=0` and multiplier stress is silent. Current rows are source-backed but conditional, so the next hard target is parent-owning `delta rho_topH` or computing a finite weighted `R_S` norm.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4396 packet update: boundary zero-mode R_S law

Marker: `{PACKET_MARKER}`

Packet update: 4396 derives the elliptic boundary/zero-mode law for `R_S` and writes source-backed conditional rows. No local-GR claim fires because `PARENT_SIGNED` source/support authority is still missing.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4396 derives the exact elliptic local suppression condition for R_S. On one declared W_H/tau/coframe support, if the parent action owns Delta_h sigma_S=delta rho_topH before readout, with boundary/zero-mode compatibility and multiplier-null boundary data, then R_S=delta rho_topH-Delta_h sigma_S is zero and lambda_S stress is silent. The checkpoint creates source-backed conditional R_S=0 rows from 4392/4393/4391 sources and an executable boundary/zero-mode gate, but no local-GR/Newton/PPN/R10 claim fires because parent source/support authority is not signed.",
            "4396 source register, elliptic derivation rows, boundary zero-mode gate input/output, R_S source-row gate input/output, bound-runner dry input/output, claim gates, decision, status, next target and validation CSV.",
            "elliptic_RS_zero_mechanism_derived_source_backed_conditional_nonclaim",
            "Parent-own delta rho_topH as one pre-readout source or compute a finite R_S profile norm on a declared W_H support.",
            "Using conditional theorem-zero as evidence, ignoring Neumann compatibility, hiding zero modes, treating post-readout Green inversion as derivation, or cancelling lambda/kernel stress.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4396_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4396_ELLIPTIC_DERIVATIONS.csv")
    boundary_output = read_csv(BOUNDARY_OUTPUT_PATH)
    source_output = read_csv(SOURCE_ROW_OUTPUT_PATH)
    bound_output = read_csv(BOUND_DRY_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4396_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4396_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4396_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4396_2_elliptic_identity_written", any(row["derivation_id"] == "ED4396_0_RS_zero_identity" for row in derivations), "R_S zero identity derived")
    add("VAL4396_3_zero_mode_law_written", any(row["derivation_id"] == "ED4396_1_boundary_zero_mode_law" for row in derivations), "boundary zero-mode law derived")
    add("VAL4396_4_multiplier_law_written", any(row["derivation_id"] == "ED4396_2_multiplier_null_law" for row in derivations), "multiplier-null law derived")
    add("VAL4396_5_boundary_gate_nonclaim", all(row["valid_for_claim"] == "False" for row in boundary_output), "boundary certificates remain nonclaim")
    add("VAL4396_6_boundary_gate_elliptic_ready", any(row["candidate_id"] == "BZM4396_0_dirichlet_or_zero_mean_mechanism" and row["elliptic_ready"] == "True" for row in boundary_output), "elliptic mechanism row is ready")
    add("VAL4396_7_source_rows_source_backed", any(row["candidate_id"] == "RS4396_0_source_backed_conditional_constraint_zero" and row["schema_ready"] == "True" and row["source_ready"] == "True" for row in source_output), "first conditional R_S row is source-backed")
    add("VAL4396_8_source_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in source_output), "source-row gate keeps rows nonclaim")
    add("VAL4396_9_bound_runner_rejects_conditional_zero", any(row["candidate_id"] == "RS4396_0_source_backed_conditional_constraint_zero" and "THEOREM_ZERO_AUTHORITY_NOT_PARENT_SIGNED" in row["refusal_reasons"] for row in bound_output), "bound runner rejects conditional theorem-zero")
    add("VAL4396_10_bound_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in bound_output), "bound dry outputs remain nonclaim")
    add("VAL4396_11_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4396_12_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4396_13_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4396_14_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4396_15_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4396_16_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4396_17_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4396_18_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4396_19_boundary_gate_exists", BOUNDARY_GATE_PATH.exists() and "def evaluate_boundary_rows" in read_text(BOUNDARY_GATE_PATH), "boundary gate exists")
    add("VAL4396_20_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = elliptic_derivation_rows()
    boundary_inputs = boundary_input_rows()
    source_inputs = source_row_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4396_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4396_ELLIPTIC_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4396_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4396_DECISION.csv": decisions,
        "P8_Y5_R2FR_4396_STATUS.csv": statuses,
        "P8_Y5_R2FR_4396_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [BOUNDARY_INPUT_PATH, SOURCE_ROW_INPUT_PATH, BOUND_DRY_INPUT_PATH]
    write_csv(BOUNDARY_INPUT_PATH, boundary_inputs)
    boundary_output = evaluate_boundary_rows(BOUNDARY_INPUT_PATH)
    write_csv(BOUNDARY_OUTPUT_PATH, boundary_output)

    write_csv(SOURCE_ROW_INPUT_PATH, source_inputs)
    source_output = evaluate_source_rows(SOURCE_ROW_INPUT_PATH)
    write_csv(SOURCE_ROW_OUTPUT_PATH, source_output)

    bound_inputs = bound_dry_input_rows(source_inputs)
    write_csv(BOUND_DRY_INPUT_PATH, bound_inputs)
    bound_output = evaluate_bound_rows(BOUND_DRY_INPUT_PATH)
    write_csv(BOUND_DRY_OUTPUT_PATH, bound_output)
    csv_paths.extend([BOUNDARY_OUTPUT_PATH, SOURCE_ROW_OUTPUT_PATH, BOUND_DRY_OUTPUT_PATH])

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, derivations, boundary_output, source_output, bound_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
