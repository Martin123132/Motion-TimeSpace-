from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_sigma_s_action_gate import evaluate_sigma_s_action_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4393"
CLAIM_ID = "L-234"
MARKER = "PPC4161_TRANSITION_SIGMAS_PARENT_ACTION_SIGNATURE_OR_FIRST_RESIDUAL_BOUND_ROW_4393"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SIGMAS_PARENT_ACTION_SIGNATURE_OR_FIRST_RESIDUAL_BOUND_ROW_4393"
DECISION = "SIGMAS_CONSTRAINT_ACTION_AND_MULTIPLIER_NULL_LEMMA_DERIVED_PARENT_ORIGIN_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4394-Y5-R2FR-transition-sigmaS-constraint-origin-or-RS-bound-runner.md"

FORMAL_PATH = FORMAL / "409-PPC4161-transition-sigmaS-parent-action-signature-or-first-residual-bound-row.md"
DOC_PATH = POST / "4393-Y5-R2FR-transition-sigmaS-parent-action-signature-or-first-residual-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4393_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
GATE_RUNNER_PATH = SCRIPT_DIR / "parent_sigma_s_action_gate.py"
GATE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_GATE_INPUT.csv"
GATE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_GATE_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4393_0_4392_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4392_NEXT_TARGET.csv",
        "4393-Y5-R2FR-transition-sigmaS-parent-action-signature-or-first-residual-bound-row.md",
        "Explicit 4393 handoff.",
    ),
    "SRC4393_1_4392_sigma": (
        SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_THEOREMS.csv",
        "SIGS4392_0_trace_electric_owner",
        "Trace-electric sigma owner route.",
    ),
    "SRC4393_2_4392_green_guard": (
        SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_THEOREMS.csv",
        "SIGS4392_2_green_inverse_no_free_claim",
        "Green inverse is not a proof guard.",
    ),
    "SRC4393_3_4392_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4392_BOUND_ROWS.csv",
        "SBND4392_0_residual_mismatch",
        "First residual mismatch bound object.",
    ),
    "SRC4393_4_observer_contract": (
        POST / "10-observer-map-symplectic-contract.md",
        "a genuine constraint whose multiplier has a parent origin",
        "Constraint-origin guard already written in the motion-load branch.",
    ),
    "SRC4393_5_nonprop_constraint": (
        POST / "07-nonpropagating-reciprocity-constraint.md",
        "S_constraint = integral lambda_R R_AB.",
        "Prior nonpropagating multiplier pattern.",
    ),
    "SRC4393_6_4391_static": (
        SOURCE_DIR / "P8_Y5_R2FR_4391_PARENT_U_S_THEOREMS.csv",
        "UST4391_2_static_time_silence_lemma",
        "Static branch needed for pressure/aniso silence.",
    ),
    "SRC4393_7_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN",
        "Boundary/no-flux private selector.",
    ),
    "SRC4393_8_185_hilbert": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H^munu",
        "Hilbert source density object.",
    ),
    "SRC4393_9_gate_runner": (
        GATE_RUNNER_PATH,
        "REQUIRED_FIELDS",
        "Executable parent sigma action gate.",
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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "SACT4393_0_parent_constraint_signature",
            "statement": "A parent sigma_S owner can be written as a nonpropagating local constraint S_{sigma lambda}=int_W sqrt(h) lambda_S(Delta_h sigma_S - delta rho_topH), with delta rho_topH:=rho_top-rho_H defined before readout.",
            "derivation": "Variation with respect to lambda_S gives Delta_h sigma_S=delta rho_topH. Then S^{ij}=c^2h^{ij}sigma_S supplies the 4392 electric-U density owner. This is an action signature, not a late Green solve, only if delta rho_topH and the W_H/tau/h data are parent-owned.",
            "effect": "Turns the sigma_S route into an explicit parent-action candidate.",
            "status": "CONSTRAINT_ACTION_TEMPLATE_DERIVED_PARENT_ORIGIN_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SACT4393_1_integrated_by_parts_form",
            "statement": "The same constraint can be written without second derivatives as S_{sigma lambda}=int_W sqrt(h)(-D_i lambda_S D^i sigma_S - lambda_S delta rho_topH)+boundary.",
            "derivation": "Integrate lambda_S Delta_h sigma_S by parts on the tau-slice. This exposes the exact boundary pairings and the operator whose kernel/zero mode must be fixed.",
            "effect": "Makes boundary, zero-mode, and metric/projector payloads explicit rather than hidden.",
            "status": "BOUNDARY_VISIBLE_FORM_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SACT4393_2_multiplier_null_lemma",
            "statement": "If the sigma constraint uses an elliptic positive Laplacian on the compact local collar, lambda_S has anchored boundary data or fixed zero mode, and no source term appears in the sigma variation, then lambda_S=0 on shell.",
            "derivation": "Variation with respect to sigma_S gives Delta_h lambda_S=0 plus boundary terms. Dirichlet lambda_S=0, or a gauge-fixed zero-mean Neumann branch with no homogeneous mode, forces lambda_S=0 by the elliptic uniqueness/energy identity int |D lambda_S|^2=boundary.",
            "effect": "If parent-signed, the constraint can impose the density identity without leaving a multiplier stress payload.",
            "status": "CONDITIONAL_MULTIPLIER_NULL_LEMMA_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SACT4393_3_metric_variation_payload",
            "statement": "Metric/coframe variation of the constraint vanishes only on the clean multiplier-null branch; otherwise lambda_S, D lambda_S, boundary motion, projector variation, and delta rho_topH variation become real stress payloads.",
            "derivation": "The Hilbert variation of sqrt(h), h^{ij}, D_i, W_H, and delta rho_topH is multiplied by lambda_S or its derivatives after integration by parts. The clean branch can kill these only if lambda_S and boundary/corner terms vanish before variation is used for readout.",
            "effect": "Prevents the constraint action from smuggling hidden pressure/curvature stress.",
            "status": "PAYLOAD_CONDITION_DERIVED_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SACT4393_4_late_multiplier_no_go",
            "statement": "Adding lambda_S(Delta sigma_S-delta rho) after seeing the residual is a closure axiom, not derivation.",
            "derivation": "A late equality multiplier can enforce any desired residual identity. To count, the sigma/lambda sector must be in the parent object language with source, boundary, and tau data fixed before local profile or PPN readout.",
            "effect": "Keeps the construction honest: parent-origin first, claim later.",
            "status": "NO_GO_LATE_EQUALITY_MULTIPLIER",
            "valid_for_claim": "False",
        },
    ]


def candidate_rows() -> List[Dict[str, str]]:
    script_path = str(Path(__file__).resolve())
    return [
        {
            "candidate_id": "PACT4393_0_sigma_lambda_constraint_template",
            "branch": "parent_sigma_lambda_constraint",
            "action_signature_written": "True",
            "parent_origin_signed": "False",
            "residual_density_object_parent_owned": "False",
            "sigma_pre_readout_lock": "False",
            "lambda_boundary_anchor_signed": "False",
            "elliptic_operator_positive_or_gauge_fixed": "False",
            "zero_mode_removed": "False",
            "multiplier_null_theorem_available": "True",
            "metric_variation_payload_zero_or_bounded": "False",
            "static_tau_silence_pass": "False",
            "affine_boundary_pairings_pass": "False",
            "ward_conservation_owned": "False",
            "no_late_green_inverse": "True",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
        {
            "candidate_id": "PACT4393_1_late_equality_multiplier",
            "branch": "late_closure_multiplier_forbidden",
            "action_signature_written": "False",
            "parent_origin_signed": "False",
            "residual_density_object_parent_owned": "False",
            "sigma_pre_readout_lock": "False",
            "lambda_boundary_anchor_signed": "False",
            "elliptic_operator_positive_or_gauge_fixed": "False",
            "zero_mode_removed": "False",
            "multiplier_null_theorem_available": "False",
            "metric_variation_payload_zero_or_bounded": "False",
            "static_tau_silence_pass": "False",
            "affine_boundary_pairings_pass": "False",
            "ward_conservation_owned": "False",
            "no_late_green_inverse": "False",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
        {
            "candidate_id": "PACT4393_2_first_RS_bound_fallback",
            "branch": "first_residual_bound_row",
            "action_signature_written": "False",
            "parent_origin_signed": "False",
            "residual_density_object_parent_owned": "True",
            "sigma_pre_readout_lock": "False",
            "lambda_boundary_anchor_signed": "False",
            "elliptic_operator_positive_or_gauge_fixed": "False",
            "zero_mode_removed": "False",
            "multiplier_null_theorem_available": "False",
            "metric_variation_payload_zero_or_bounded": "False",
            "static_tau_silence_pass": "False",
            "affine_boundary_pairings_pass": "False",
            "ward_conservation_owned": "False",
            "no_late_green_inverse": "True",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
    ]


def activation_clause_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "ACT4393_0_parent_origin",
            "clause": "sigma/lambda constraint sector belongs to the parent action before readout",
            "why_needed": "otherwise the multiplier is just a late closure rule",
            "current_status": "UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ACT4393_1_residual_object",
            "clause": "delta rho_topH is parent-defined from topological/Hilbert source objects on the same W_H",
            "why_needed": "the constraint must not target a post-fitted or frame-shifted residual",
            "current_status": "UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ACT4393_2_multiplier_null",
            "clause": "lambda_S=0 follows from elliptic uniqueness, boundary anchor, and zero-mode removal",
            "why_needed": "kills hidden stress from the constraint sector",
            "current_status": "CONDITIONAL_LEMMA_ONLY",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ACT4393_3_static_boundary",
            "clause": "static tau silence and affine Green boundary pairings pass in the same branch",
            "why_needed": "needed for PPN pressure/aniso and affine center closure",
            "current_status": "UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ACT4393_4_ward",
            "clause": "sigma/lambda constraint stress is conserved or has an explicit exchange current",
            "why_needed": "Bianchi consistency cannot be assumed for an externally fixed constraint",
            "current_status": "UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def residual_bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "RS4393_0_first_residual_bound",
            "quantity": "R_S=rho_top-rho_H-Delta_h sigma_S",
            "score_shape": "|delta a_RS|/|a_N| <= K_N(s) ||R_S||_weighted/M_H",
            "required_inputs": "source-backed R_S profile or theorem-zero, W_H geometry, M_H, support radius, Green/readout convention, no-cancellation guard",
            "source_path": "MISSING_FIRST_RS_PROFILE_OR_THEOREM_ZERO",
            "current_status": "BOUND_SCHEMA_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RS4393_1_multiplier_payload_bound",
            "quantity": "T_{lambda sigma}^{ij}, T_{lambda sigma}^{00}",
            "score_shape": "PPN stress projection from nonzero lambda_S or Dlambda_S",
            "required_inputs": "lambda_S norm, Dlambda_S norm, boundary/corner terms, projection matrix",
            "source_path": "MISSING_MULTIPLIER_STRESS_BOUND",
            "current_status": "BOUND_SCHEMA_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RS4393_2_zero_mode_bound",
            "quantity": "harmonic/constant sigma kernel and S-kernel modes",
            "score_shape": "kernel stress/boundary projection absolute-summed",
            "required_inputs": "kernel basis, parent gauge condition, amplitude bounds, boundary traction",
            "source_path": "MISSING_SIGMAS_KERNEL_BOUND",
            "current_status": "BOUND_SCHEMA_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "sigmaS_action": "constraint signature written but parent origin and residual object are unsigned",
        "multiplier_null": "lambda_S=0 lemma is conditional on boundary anchor, elliptic positivity and zero-mode removal",
        "local_GR": "static, boundary, curvature and Ward payloads remain open",
        "Newton": "R_S profile/theorem-zero row missing",
        "PPN": "constraint stress and kernel modes not bounded",
        "R10_WEP_clock": "same tau/source/readout projection remains dependent on upstream unsigned clauses",
    }
    return [
        {
            "gate_id": f"CG4393_{index}_{arena}",
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
            "decision_id": "DEC4393_0",
            "decision": DECISION,
            "summary": "4393 derives a concrete parent sigma_S constraint-action template and a multiplier-null lemma. This is the best action route so far: lambda_S can enforce Delta_h sigma_S=rho_top-rho_H without leaving stress if elliptic boundary/zero-mode clauses force lambda_S=0. It is not claimed because parent origin, residual object, boundary anchor, static branch, Ward and payload clauses are unsigned.",
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
            "summary": "sigma_S now has an explicit parent-action candidate; the next work is proving parent origin or running first R_S/multiplier payload bounds.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4393_0",
            "target": NEXT_TARGET,
            "question": "Can MTS justify the sigma/lambda constraint as a parent-origin sector with elliptic boundary/zero-mode clauses, or must R_S and multiplier stress be scored?",
            "preferred_route": "derive parent origin for the sigma/lambda constraint from the existing nonpropagating constraint/object-language stack.",
            "fallback_route": "implement the first R_S residual and multiplier-stress bound runner with strict source/profile inputs.",
            "avoid": "late equality multipliers, post-readout Green solves, Neumann zero-mode leakage, or ignoring constraint Hilbert stress.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    gate_output: List[Dict[str, str]],
    clauses: List[Dict[str, str]],
    bounds: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 409 PPC4161 transition: sigmaS parent action signature or first residual bound row

Marker: `{MARKER}`

## Result

4393 constructs the parent-action candidate instead of merely pointing at a missing source.

Clean branch:

`S_sigma_lambda = int_W sqrt(h) lambda_S (Delta_h sigma_S - delta rho_topH)`,

where:

`delta rho_topH := rho_top-rho_H`.

Variation with respect to `lambda_S` gives the desired owner identity:

`Delta_h sigma_S = delta rho_topH`.

Then 4392 gives:

`S^ij = c^2 h^ij sigma_S`, so `c^-2 D_iD_jS^ij = rho_top-rho_H`.

The important new theorem is the multiplier-null lemma: variation with respect to `sigma_S` gives `Delta_h lambda_S=0`; with anchored boundary data or a fixed zero-mode, elliptic uniqueness forces `lambda_S=0`. On that clean branch the constraint can impose the density identity without leaving hidden multiplier stress.

But this is not a claim. The constraint must have parent origin. A late `lambda_S` equality multiplier is explicitly forbidden.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Theorem Rows\n\n"
    for row in theorems:
        text += f"### {row['theorem_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- Status: `{row['status']}`\n\n"
    text += "## Action Gate\n\n"
    for row in gate_output:
        text += f"- `{row['candidate_id']}`: pass=`{row['sigma_s_action_pass']}`, signature_ready=`{row['signature_ready']}`, multiplier_safe=`{row['multiplier_safe']}`, closed `{row['closed_clause_count']}/{row['total_clause_count']}`, failed `{row['failed_clauses']}`.\n"
    text += "\n## Activation Clauses\n\n"
    for row in clauses:
        text += f"- `{row['clause_id']}`: {row['clause']} — status `{row['current_status']}`.\n"
    text += "\n## First Bound Rows\n\n"
    for row in bounds:
        text += f"- `{row['bound_id']}`: `{row['quantity']}` — {row['required_inputs']}.\n"
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
        f"""# 4393 Y5 R2FR: sigmaS parent action signature or first residual bound row

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
## 4393 local spine update: sigmaS constraint action

Marker: `{MARKER}`

Spine update: the sigmaS route now has an explicit parent-action candidate, `int sqrt(h) lambda_S(Delta_h sigma_S-delta rho_topH)`. The multiplier-null lemma says `lambda_S=0` on a compact anchored elliptic branch, so the constraint can impose `Delta_h sigma_S=rho_top-rho_H` without hidden multiplier stress if all parent-origin, boundary, zero-mode, static and Ward clauses are signed. The construction remains nonclaim because those clauses are not yet signed.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4393 packet update: sigmaS multiplier-null route

Marker: `{PACKET_MARKER}`

Packet update: 4393 advances the local-GR route by turning `sigma_S` into a possible parent constraint sector. The clean branch is a nonpropagating `lambda_S` constraint plus elliptic multiplier-null theorem. If parent-origin signed, it would close the sigmaS owner identity without adding stress. If unsigned, first fallback rows are `R_S`, multiplier stress, and sigma-kernel payload bounds.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4393 derives a concrete parent-action candidate for the sigma_S owner route: S_sigma_lambda=int_W sqrt(h) lambda_S(Delta_h sigma_S-delta rho_topH), where delta rho_topH=rho_top-rho_H is fixed before readout. Variation with respect to lambda_S gives Delta_h sigma_S=delta rho_topH, and the 4392 electric route then gives S^{ij}=c^2h^{ij}sigma_S. It also derives the multiplier-null lemma: variation with respect to sigma_S gives Delta_h lambda_S=0, so anchored boundary data or zero-mode fixing can force lambda_S=0 and remove hidden multiplier stress. This is a construction advance, not a claim, because parent origin, residual-object ownership, boundary anchor, static branch, Ward conservation and payload bounds remain unsigned.",
            "4393 source register, sigma action theorem rows, action gate input/output, activation clauses, first residual bound rows, claim gates, decision, status, next target and validation CSV.",
            "sigmaS_constraint_action_multiplier_null_lemma_parent_origin_unsigned_nonclaim",
            "Derive parent origin for the sigma/lambda constraint sector or implement first R_S and multiplier-stress bound runner with source-backed inputs.",
            "Late equality multiplier, post-readout Green solve, ignoring lambda stress, using Neumann zero modes without gauge fixing, or claiming local GR from the constraint template alone.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4393_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv")
    gate_output = read_csv(GATE_OUTPUT_PATH)
    clauses = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4393_ACTIVATION_CLAUSES.csv")
    bounds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4393_FIRST_BOUND_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4393_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4393_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4393_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4393_2_constraint_action", any(row["theorem_id"] == "SACT4393_0_parent_constraint_signature" for row in theorems), "constraint action theorem staged")
    add("VAL4393_3_multiplier_null", any(row["theorem_id"] == "SACT4393_2_multiplier_null_lemma" for row in theorems), "multiplier-null lemma staged")
    add("VAL4393_4_late_no_go", any(row["theorem_id"] == "SACT4393_4_late_multiplier_no_go" for row in theorems), "late multiplier no-go staged")
    add("VAL4393_5_action_gate_fails_closed", all(row["sigma_s_action_pass"] == "False" and row["valid_for_claim"] == "False" for row in gate_output), "action candidates fail closed")
    add("VAL4393_6_activation_clauses_nonclaim", len(clauses) >= 5 and all(row["valid_for_claim"] == "False" for row in clauses), "activation clauses staged nonclaim")
    add("VAL4393_7_bound_rows_nonclaim", len(bounds) >= 3 and all(row["valid_for_claim"] == "False" and "MISSING" in row["source_path"] for row in bounds), "first bound rows staged nonclaim")
    add("VAL4393_8_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4393_9_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4393_10_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4393_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4393_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4393_13_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4393_14_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4393_15_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4393_16_runner_exists", GATE_RUNNER_PATH.exists() and "def evaluate_sigma_s_action_rows" in read_text(GATE_RUNNER_PATH), "parent sigma action gate runner exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = theorem_rows()
    gate_inputs = candidate_rows()
    clauses = activation_clause_rows()
    bounds = residual_bound_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4393_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4393_ACTIVATION_CLAUSES.csv": clauses,
        "P8_Y5_R2FR_4393_FIRST_BOUND_ROWS.csv": bounds,
        "P8_Y5_R2FR_4393_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4393_DECISION.csv": decisions,
        "P8_Y5_R2FR_4393_STATUS.csv": statuses,
        "P8_Y5_R2FR_4393_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [GATE_INPUT_PATH]
    write_csv(GATE_INPUT_PATH, gate_inputs)
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    gate_output = evaluate_sigma_s_action_rows(GATE_INPUT_PATH)
    write_csv(GATE_OUTPUT_PATH, gate_output)
    csv_paths.append(GATE_OUTPUT_PATH)

    write_formal_doc(sources, theorems, gate_output, clauses, bounds, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
