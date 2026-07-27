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
from sigma_s_constraint_origin_gate import evaluate_origin_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4395"
CLAIM_ID = "L-236"
MARKER = "PPC4161_TRANSITION_RS_FIRST_SOURCE_ROW_OR_SIGMAS_PARENT_ORIGIN_PROOF_4395"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_RS_FIRST_SOURCE_ROW_OR_SIGMAS_PARENT_ORIGIN_PROOF_4395"
DECISION = "SIGMAS_PARENT_ORIGIN_PROOF_FAILS_RS_SOURCE_ROW_GATE_BUILT"
NEXT_TARGET = "4396-Y5-R2FR-transition-first-real-RS-profile-row-or-boundary-zero-mode-source.md"

FORMAL_PATH = FORMAL / "411-PPC4161-transition-RS-first-source-row-or-sigma-constraint-parent-origin-proof.md"
DOC_PATH = POST / "4395-Y5-R2FR-transition-RS-first-source-row-or-sigma-constraint-parent-origin-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4395_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

ORIGIN_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4395_SIGMA_CONSTRAINT_ORIGIN_INPUT.csv"
ORIGIN_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4395_SIGMA_CONSTRAINT_ORIGIN_OUTPUT.csv"
SOURCE_ROW_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4395_RS_SOURCE_ROW_GATE_INPUT.csv"
SOURCE_ROW_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4395_RS_SOURCE_ROW_GATE_OUTPUT.csv"
BOUND_DRY_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4395_RS_BOUND_RUNNER_DRY_INPUT.csv"
BOUND_DRY_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4395_RS_BOUND_RUNNER_DRY_OUTPUT.csv"
ORIGIN_RUNNER_PATH = SCRIPT_DIR / "sigma_s_constraint_origin_gate.py"
SOURCE_ROW_GATE_PATH = SCRIPT_DIR / "sigma_s_RS_source_row_gate.py"
BOUND_RUNNER_PATH = SCRIPT_DIR / "sigma_s_RS_bound_runner.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4395_0_4394_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4394_NEXT_TARGET.csv",
        "4395-Y5-R2FR-transition-RS-first-source-row-or-sigma-constraint-parent-origin-proof.md",
        "4394 handoff requiring either parent-origin proof or a first R_S source row.",
    ),
    "SRC4395_1_4394_origin": (
        SOURCE_DIR / "P8_Y5_R2FR_4394_SIGMA_CONSTRAINT_ORIGIN_OUTPUT.csv",
        "ORIG4394_2_first_class_constraint_route",
        "4394 origin gate output showing object-language and constraint-rank clauses remain unsigned.",
    ),
    "SRC4395_2_4394_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4394_RS_BOUND_OUTPUT.csv",
        "RS4394_0_missing_first_real_row",
        "4394 bound output identifying the missing first real R_S source row.",
    ),
    "SRC4395_3_1022_quotient": (
        POST / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
        "VQC1022_6_degree_count",
        "Quotient/vertical route records degree count as unchecked, not a proof.",
    ),
    "SRC4395_4_1038_omega": (
        POST / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
        "MISSING_DEGREE_COUNT",
        "Parent Omega/DCX closure audit keeps parent symplectic, boundary, cocycle and degree count unsigned.",
    ),
    "SRC4395_5_1078_object_language": (
        POST / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md",
        "OBJECT_LANGUAGE_NOT_SIGNED",
        "Object-language proof stack explicitly leaves the parent object-language owner unsigned.",
    ),
    "SRC4395_6_source_row_gate": (
        SOURCE_ROW_GATE_PATH,
        "def evaluate_source_rows",
        "New executable gate for first real R_S source rows.",
    ),
    "SRC4395_7_bound_runner": (
        BOUND_RUNNER_PATH,
        "def evaluate_bound_rows",
        "Existing R_S bound runner, now tightened so any refusal reason blocks claims.",
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


def origin_proof_audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "RS4395_ORIGIN_0_object_language",
            "route": "parent_object_language_constraint_sector",
            "attempt": "Use parent object-language typing to make lambda_S(Delta_h sigma_S-delta rho_topH) an allowed before-readout constraint sector.",
            "result": "FAIL_CURRENT_CORPUS",
            "blocking_clause": "OBJECT_LANGUAGE_NOT_SIGNED",
            "derivation_or_reason": "1078 explicitly says the object-language grammar remains a desired contract, not a parent-derived theorem. That leaves sigma/lambda as a useful template rather than an owned sector.",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RS4395_ORIGIN_1_first_class_rank",
            "route": "first_class_constraint_degree_count",
            "attempt": "Treat sigma/lambda as a first-class local constraint whose multiplier removes a nonphysical pair rather than adding fitted matter.",
            "result": "FAIL_CURRENT_CORPUS",
            "blocking_clause": "MISSING_PARENT_OMEGA_DCX_BOUNDARY_COCYCLE_DEGREE_COUNT",
            "derivation_or_reason": "1022 and 1038 require parent Omega, D C_X, all-field vertical generator, differentiable boundary charge, zero cocycle and reduced degree count. Those clauses are named but not signed.",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RS4395_ORIGIN_2_current_owner",
            "route": "conserved_current_or_source_owner",
            "attempt": "Derive R_S=0 because rho_top-rho_H and Delta_h sigma_S are two expressions for one conserved parent source.",
            "result": "FAIL_CURRENT_CORPUS",
            "blocking_clause": "RESIDUAL_DENSITY_PARENT_OWNER_UNSIGNED",
            "derivation_or_reason": "The sigma action template defines the desired equality, but no source ledger yet proves the residual density is parent-owned before readout rather than chosen after readout.",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RS4395_ORIGIN_3_no_fake_theorem_zero",
            "route": "claim_hygiene",
            "attempt": "Allow theorem-zero only when a source row carries PARENT_SIGNED authority and local geometry certificates.",
            "result": "GATE_INSTALLED",
            "blocking_clause": "THEOREM_ZERO_AUTHORITY_NOT_PARENT_SIGNED",
            "derivation_or_reason": "The new source-row gate and tightened bound runner reject closure-only theorem-zero rows even when the arithmetic would otherwise pass.",
            "valid_for_claim": "False",
        },
    ]


def origin_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "ORIG4395_0_object_language_retry",
            "origin_route": "parent_object_language_constraint_sector",
            "nonpropagating_constraint_family_identified": "True",
            "parent_object_language_signed": "False",
            "origin_principle_derived": "False",
            "residual_density_parent_owned": "False",
            "sigma_lambda_added_before_readout": "False",
            "constraint_rank_or_gauge_count_checked": "False",
            "boundary_zero_mode_owner_signed": "False",
            "same_tau_coframe_signed": "False",
            "no_GR_import_or_fit": "True",
            "no_late_multiplier": "True",
            "source_path": str(POST / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"),
        },
        {
            "candidate_id": "ORIG4395_1_first_class_degree_count_retry",
            "origin_route": "first_class_constraint_degree_count",
            "nonpropagating_constraint_family_identified": "True",
            "parent_object_language_signed": "False",
            "origin_principle_derived": "False",
            "residual_density_parent_owned": "False",
            "sigma_lambda_added_before_readout": "False",
            "constraint_rank_or_gauge_count_checked": "False",
            "boundary_zero_mode_owner_signed": "False",
            "same_tau_coframe_signed": "False",
            "no_GR_import_or_fit": "True",
            "no_late_multiplier": "True",
            "source_path": str(POST / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"),
        },
    ]


def source_row_schema_rows() -> List[Dict[str, str]]:
    return [
        {
            "field": "candidate_id",
            "meaning": "unique R_S source-row id",
            "claim_requirement": "nonempty and stable",
            "valid_for_claim": "False",
        },
        {
            "field": "R_S_weighted_norm",
            "meaning": "weighted norm of rho_top-rho_H-Delta_h sigma_S on W_H or theorem-zero value",
            "claim_requirement": "positive numeric finite value or zero with PARENT_SIGNED theorem-zero authority",
            "valid_for_claim": "False",
        },
        {
            "field": "source_path/source_row_id/equation_ref",
            "meaning": "traceable local source of the residual, not a vibe row",
            "claim_requirement": "path exists and row/equation ids are not MISSING",
            "valid_for_claim": "False",
        },
        {
            "field": "W_H_geometry_source and same_tau_coframe_certificate",
            "meaning": "same local body, same tau/coframe, same spatial domain used by M_H, K_N and sigma_S",
            "claim_requirement": "existing certificate paths before the row can feed a claim",
            "valid_for_claim": "False",
        },
        {
            "field": "no_cancellation_guard",
            "meaning": "lambda stress and kernel stress are absolute-summed with R_S rather than cancelled",
            "claim_requirement": "true",
            "valid_for_claim": "False",
        },
    ]


def source_row_input_rows() -> List[Dict[str, str]]:
    script_path = str(Path(__file__).resolve())
    return [
        {
            "candidate_id": "RS4395_0_missing_source_row",
            "target": "first_real_R_S_profile",
            "theorem_zero": "False",
            "theorem_zero_authority": "MISSING_PARENT_SIGNED_RS_ZERO",
            "R_S_weighted_norm": "MISSING_R_S_WEIGHTED_NORM",
            "R_S_units": "MISSING_R_S_UNITS",
            "M_H": "MISSING_M_H",
            "M_H_units": "MISSING_M_H_UNITS",
            "K_N": "MISSING_K_N",
            "lambda_stress_score": "MISSING_LAMBDA_STRESS_SCORE",
            "kernel_stress_score": "MISSING_KERNEL_STRESS_SCORE",
            "delta_threshold": "MISSING_DELTA_THRESHOLD",
            "source_path": "MISSING_FIRST_RS_SOURCE_PATH",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "equation_ref": "MISSING_EQUATION_REF",
            "W_H_geometry_source": "MISSING_W_H_GEOMETRY_SOURCE",
            "same_tau_coframe_certificate": "MISSING_SAME_TAU_COFRAME_CERTIFICATE",
            "no_cancellation_guard": "False",
            "input_valid_for_claim": "False",
            "notes": "Deliberate blocker row: the first real R_S profile is not yet sourced.",
        },
        {
            "candidate_id": "RS4395_1_schema_smoke_nonclaim",
            "target": "source_row_schema_smoke",
            "theorem_zero": "False",
            "theorem_zero_authority": "NONE",
            "R_S_weighted_norm": "1e-9",
            "R_S_units": "same_units_as_M_H",
            "M_H": "1.0",
            "M_H_units": "same_units_as_R_S_norm",
            "K_N": "2e-2",
            "lambda_stress_score": "0.0",
            "kernel_stress_score": "0.0",
            "delta_threshold": "1e-6",
            "source_path": script_path,
            "source_row_id": "synthetic_schema_smoke_not_evidence",
            "equation_ref": "synthetic_schema_smoke_not_evidence",
            "W_H_geometry_source": script_path,
            "same_tau_coframe_certificate": script_path,
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
            "notes": "Schema and arithmetic smoke only; no physical source row.",
        },
        {
            "candidate_id": "RS4395_2_theorem_zero_authority_refusal",
            "target": "closure_only_theorem_zero_refusal",
            "theorem_zero": "True",
            "theorem_zero_authority": "CLOSURE_ONLY_NOT_PARENT_SIGNED",
            "R_S_weighted_norm": "0.0",
            "R_S_units": "theorem_zero_dimensionless",
            "M_H": "1.0",
            "M_H_units": "dimensionless_normalized_mass",
            "K_N": "1.0",
            "lambda_stress_score": "0.0",
            "kernel_stress_score": "0.0",
            "delta_threshold": "1e-12",
            "source_path": script_path,
            "source_row_id": "closure_only_zero_smoke",
            "equation_ref": "closure_only_zero_smoke",
            "W_H_geometry_source": script_path,
            "same_tau_coframe_certificate": script_path,
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "True",
            "notes": "Deliberate trap row: arithmetic passes but authority is not parent-signed.",
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
        "origin_proof": "object-language owner, parent Omega/DCX, boundary/cocycle, current owner and degree count remain unsigned",
        "first_R_S_source_row": "the new source-row gate finds only placeholder/smoke rows, not a real profile or parent theorem-zero row",
        "bound_runner": "dry-run rows are nonclaim and closure-only theorem-zero is now refused",
        "local_GR_Newton": "sigma/lambda origin and finite R_S payloads are not closed",
        "PPN_R10_clock_orbital": "no arena projection row with source-backed units exists yet",
    }
    return [
        {
            "gate_id": f"CG4395_{index}_{arena}",
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
            "decision_id": "DEC4395_0",
            "decision": DECISION,
            "summary": "4395 takes the requested leap at the sigma/lambda fork. The parent-origin proof is attempted against object-language and first-class degree-count sources, but the corpus still lacks the signed parent object language, parent Omega/DCX, boundary/cocycle, residual source owner, and degree count. Instead of looping, 4395 installs a first-real-R_S source-row gate and tightens the bound runner so closure-only theorem-zero rows cannot sneak through.",
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
            "summary": "parent-origin proof remains unsigned; first R_S source-row intake is now executable and refuses placeholder/closure-only rows.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4395_0",
            "target": NEXT_TARGET,
            "question": "Can we produce the first source-backed R_S profile row, or a parent-signed boundary/zero-mode theorem that sets R_S=0?",
            "preferred_route": "construct a concrete W_H geometry/tau/coframe certificate and compute or bound R_S on that same support.",
            "fallback_route": "try to derive the boundary zero-mode owner that would make theorem-zero authority genuinely PARENT_SIGNED.",
            "avoid": "another sigma/lambda origin paragraph without a row that passes the new source-row gate or a real parent-signed theorem-zero clause.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    audit: List[Dict[str, str]],
    origin_output: List[Dict[str, str]],
    source_output: List[Dict[str, str]],
    bound_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 411 PPC4161 transition: R_S first source row or sigma constraint parent-origin proof

Marker: `{MARKER}`

## Result

4395 tries the parent-origin proof first, then converts the failure into an executable source-row gate.

The proof attempt does not close. The current corpus contains the right route names, but not the signed parent object language, `Omega/DCX`, boundary/cocycle calculation, residual source owner, same-frame certificate, or degree count needed to say `sigma/lambda` is parent-owned.

The useful advance is operational:

`R_S = rho_top - rho_H - Delta_h sigma_S`

can now enter the local Newton/PPN branch only through a source-row gate that checks source paths, units, same-domain geometry, same tau/coframe certification, theorem-zero authority, and no-cancellation stress handling before the bound runner is allowed to matter.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Parent-Origin Proof Audit\n\n"
    for row in audit:
        text += f"### {row['audit_id']}\n\n- Route: `{row['route']}`\n- Attempt: {row['attempt']}\n- Result: `{row['result']}`\n- Blocking clause: `{row['blocking_clause']}`\n- Reason: {row['derivation_or_reason']}\n\n"
    text += "## Origin Gate Output\n\n"
    for row in origin_output:
        text += f"- `{row['candidate_id']}`: pass=`{row['origin_pass']}`, closed `{row['closed_clause_count']}/{row['total_clause_count']}`, failed `{row['failed_clauses']}`.\n"
    text += "\n## R_S Source-Row Gate Output\n\n"
    for row in source_output:
        text += f"- `{row['candidate_id']}`: schema_ready=`{row['schema_ready']}`, ready_for_bound_runner=`{row['ready_for_bound_runner']}`, valid=`{row['valid_for_claim']}`, reasons=`{row['refusal_reasons']}`.\n"
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
        f"""# 4395 Y5 R2FR: R_S first source row or sigma constraint parent-origin proof

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
## 4395 local spine update: first R_S source-row gate

Marker: `{MARKER}`

Spine update: the sigma/lambda parent-origin proof has now been tried against object-language and first-class degree-count routes and remains unsigned. The local branch therefore shifts from "argue the origin again" to "produce a row": a candidate `R_S=rho_top-rho_H-Delta_h sigma_S` input must carry source path, row/equation reference, units, same `W_H` geometry, same tau/coframe certificate, theorem-zero authority if zero, and absolute no-cancellation stress handling before it can feed the bound runner.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4395 packet update: R_S source-row gate

Marker: `{PACKET_MARKER}`

Packet update: 4395 does not claim local GR. It installs the source-row gate for the first real `R_S` profile/theorem-zero row and tightens the bound runner so closure-only theorem-zero authority blocks claims.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4395 attempts the sigma/lambda parent-origin proof through parent object-language and first-class degree-count routes. The proof remains unsigned because current ledgers do not supply the parent object-language owner, parent Omega/DCX, all-field vertical generator, boundary charge/cocycle, residual source owner, same tau/coframe certificate, or reduced degree count. The checkpoint converts that failure into progress by adding a first-real-R_S source-row gate for R_S=rho_top-rho_H-Delta_h sigma_S and tightening the bound runner so closure-only theorem-zero rows cannot pass just because the arithmetic is zero.",
            "4395 source register, origin proof audit, origin gate output, R_S source-row schema/input/output, bound-runner dry input/output, claim gates, decision, status, next target and validation CSV.",
            "sigmaS_parent_origin_unsigned_RS_source_row_gate_installed_nonclaim",
            "Produce a source-backed W_H/tau/coframe R_S profile row or a genuinely PARENT_SIGNED boundary/zero-mode theorem-zero row.",
            "Treating closure-only theorem-zero as proof, using synthetic rows as evidence, mixing support domains, allowing stress cancellation, or hiding the boundary zero mode.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4395_SOURCE_REGISTER.csv")
    audit = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4395_ORIGIN_PROOF_AUDIT.csv")
    origin_output = read_csv(ORIGIN_OUTPUT_PATH)
    source_output = read_csv(SOURCE_ROW_OUTPUT_PATH)
    bound_output = read_csv(BOUND_DRY_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4395_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4395_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4395_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4395_2_origin_audit_fails", all(row["valid_for_claim"] == "False" for row in audit), "origin proof audit remains nonclaim")
    add("VAL4395_3_origin_gate_fails_closed", all(row["origin_pass"] == "False" for row in origin_output), "origin retry rows fail closed")
    add("VAL4395_4_source_gate_rejects_missing", any(row["candidate_id"] == "RS4395_0_missing_source_row" and row["valid_for_claim"] == "False" for row in source_output), "source gate rejects missing first row")
    add("VAL4395_5_schema_smoke_nonclaim", any(row["candidate_id"] == "RS4395_1_schema_smoke_nonclaim" and row["schema_ready"] == "True" and row["valid_for_claim"] == "False" for row in source_output), "schema smoke parses but remains nonclaim")
    add("VAL4395_6_source_gate_rejects_nonparent_theorem", any(row["candidate_id"] == "RS4395_2_theorem_zero_authority_refusal" and "THEOREM_ZERO_AUTHORITY_NOT_PARENT_SIGNED" in row["refusal_reasons"] and row["valid_for_claim"] == "False" for row in source_output), "source gate rejects closure-only theorem-zero")
    add("VAL4395_7_bound_runner_rejects_nonparent_theorem", any(row["candidate_id"] == "RS4395_2_theorem_zero_authority_refusal" and "THEOREM_ZERO_AUTHORITY_NOT_PARENT_SIGNED" in row["refusal_reasons"] and row["valid_for_claim"] == "False" for row in bound_output), "bound runner refuses theorem-zero authority trap")
    add("VAL4395_8_bound_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in bound_output), "all bound dry outputs remain nonclaim")
    add("VAL4395_9_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4395_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4395_11_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4395_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4395_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4395_14_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4395_15_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4395_16_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4395_17_source_gate_exists", SOURCE_ROW_GATE_PATH.exists() and "def evaluate_source_rows" in read_text(SOURCE_ROW_GATE_PATH), "source-row gate exists")
    add("VAL4395_18_bound_runner_tightened", "not reasons" in read_text(BOUND_RUNNER_PATH), "bound runner blocks every refusal reason")
    add("VAL4395_19_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    audit = origin_proof_audit_rows()
    origin_inputs = origin_input_rows()
    source_schema = source_row_schema_rows()
    source_inputs = source_row_input_rows()
    bound_inputs = bound_dry_input_rows(source_inputs)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4395_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4395_ORIGIN_PROOF_AUDIT.csv": audit,
        "P8_Y5_R2FR_4395_RS_SOURCE_ROW_SCHEMA.csv": source_schema,
        "P8_Y5_R2FR_4395_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4395_DECISION.csv": decisions,
        "P8_Y5_R2FR_4395_STATUS.csv": statuses,
        "P8_Y5_R2FR_4395_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [ORIGIN_INPUT_PATH, SOURCE_ROW_INPUT_PATH, BOUND_DRY_INPUT_PATH]
    write_csv(ORIGIN_INPUT_PATH, origin_inputs)
    write_csv(SOURCE_ROW_INPUT_PATH, source_inputs)
    write_csv(BOUND_DRY_INPUT_PATH, bound_inputs)
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    origin_output = evaluate_origin_rows(ORIGIN_INPUT_PATH)
    source_output = evaluate_source_rows(SOURCE_ROW_INPUT_PATH)
    bound_output = evaluate_bound_rows(BOUND_DRY_INPUT_PATH)
    write_csv(ORIGIN_OUTPUT_PATH, origin_output)
    write_csv(SOURCE_ROW_OUTPUT_PATH, source_output)
    write_csv(BOUND_DRY_OUTPUT_PATH, bound_output)
    csv_paths.extend([ORIGIN_OUTPUT_PATH, SOURCE_ROW_OUTPUT_PATH, BOUND_DRY_OUTPUT_PATH])

    write_formal_doc(sources, audit, origin_output, source_output, bound_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
