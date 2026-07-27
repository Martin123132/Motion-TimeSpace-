from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sigma_s_owner_gate import evaluate_sigma_s_owner_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4392"
CLAIM_ID = "L-233"
MARKER = "PPC4161_TRANSITION_SIGMAS_RESIDUAL_OWNER_OR_ELECTRIC_U_BOUND_ROW_4392"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SIGMAS_RESIDUAL_OWNER_OR_ELECTRIC_U_BOUND_ROW_4392"
DECISION = "SIGMAS_TRACE_ELECTRIC_OWNER_ROUTE_DERIVED_GREEN_INVERSE_GUARDED_OWNER_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4393-Y5-R2FR-transition-sigmaS-parent-action-signature-or-first-residual-bound-row.md"

FORMAL_PATH = FORMAL / "408-PPC4161-transition-sigmaS-residual-owner-or-electric-U-bound-row.md"
DOC_PATH = POST / "4392-Y5-R2FR-transition-sigmaS-residual-owner-or-electric-U-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4392_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
GATE_RUNNER_PATH = SCRIPT_DIR / "sigma_s_owner_gate.py"
GATE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_OWNER_GATE_INPUT.csv"
GATE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_OWNER_GATE_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4392_0_4391_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4391_NEXT_TARGET.csv",
        "4392-Y5-R2FR-transition-sigmaS-residual-owner-or-electric-U-bound-row.md",
        "Explicit 4392 handoff.",
    ),
    "SRC4392_1_4391_S_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4391_PARENT_U_S_THEOREMS.csv",
        "UST4391_4_remaining_owner",
        "S-sector ownership is the named remaining target.",
    ),
    "SRC4392_2_4386_trace": (
        SOURCE_DIR / "P8_Y5_R2FR_4386_DOUBLE_DIVERGENCE_THEOREMS.csv",
        "DD4386_2_trace_laplacian_subcase",
        "Trace/Laplacian subcase of the double-divergence route.",
    ),
    "SRC4392_3_4387_density": (
        SOURCE_DIR / "P8_Y5_R2FR_4387_IMPROVEMENT_OWNER_THEOREMS.csv",
        "IO4387_1_newtonian_density_projection",
        "Weak-static density projection for U/S.",
    ),
    "SRC4392_4_4378_laplacian": (
        SOURCE_DIR / "P8_Y5_R2FR_4378_HARMONIC_NULL_THEOREM.csv",
        "HN4378_1_laplacian_null_sufficient_condition",
        "Earlier Laplacian-null condition now becomes sigma_S owner route.",
    ),
    "SRC4392_5_4381_normal": (
        FORMAL / "397-PPC4161-transition-topological-defect-normal-form-or-profile-quadrature-runner.md",
        "NF4381_2_laplacian_boundary_silent",
        "Normal-form theorem route for Laplacian boundary-silent defects.",
    ),
    "SRC4392_6_4390_projection": (
        SOURCE_DIR / "P8_Y5_R2FR_4390_COMPONENT_PROJECTIONS.csv",
        "PROJ4390_0_electric_U",
        "Electric U projection row.",
    ),
    "SRC4392_7_4391_static": (
        SOURCE_DIR / "P8_Y5_R2FR_4391_STATIC_TIME_GATE_OUTPUT.csv",
        "STATIC_TIME_GATE_BLOCKED_CLAUSES_OPEN",
        "Static-time branch remains gated.",
    ),
    "SRC4392_8_gate_runner": (
        GATE_RUNNER_PATH,
        "REQUIRED_FIELDS",
        "Executable sigma/S owner gate.",
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
            "theorem_id": "SIGS4392_0_trace_electric_owner",
            "statement": "If the parent supplies a scalar sigma_S with rho_top-rho_H = Delta_h sigma_S on the local tau-slice, then the electric-U branch can take S^{ij}=c^2 h^{ij} sigma_S and obtains c^-2 D_iD_j S^{ij}=rho_top-rho_H up to explicit connection/curvature terms.",
            "derivation": "In the local weak-static orthonormal frame, D_iD_j(c^2 delta^{ij} sigma_S)/c^2 = Delta sigma_S. This is exactly the 4386 trace Laplacian subcase, but placed inside the 4390/4391 electric U projector instead of scalar phiR.",
            "effect": "This is the cleanest S-owner construction route found so far.",
            "status": "EXACT_CONDITIONAL_SIGMAS_OWNER_ROUTE_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SIGS4392_1_laplacian_null_weld",
            "statement": "The sigma_S route is the same mathematical object as the 4378/4381 Laplacian-null topological-profile route, now reinterpreted as the electric-U density owner.",
            "derivation": "4378 proved delta rho_top=Delta u_top with Green boundary silence kills exterior harmonic moments. Set sigma_S=u_top and S^{ij}=c^2 h^{ij}sigma_S to feed the same defect through the electric-U stress-improvement channel.",
            "effect": "Connects two previously separate ladders: exterior multipole silence and local affine double-divergence closure.",
            "status": "ROUTES_WELDED_PARENT_SIGNATURE_STILL_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SIGS4392_2_green_inverse_no_free_claim",
            "statement": "Solving sigma_S=Delta_h^{-1}(rho_top-rho_H) after the residual is known is a representation theorem, not a parent derivation.",
            "derivation": "A Green inverse depends on domain, boundary conditions, zero-mode convention, and metric/coframe data. If inserted after readout it can always manufacture an S for many residuals, and its metric/domain variation creates projector/boundary stress payloads.",
            "effect": "Allows Green inverse as a bound or construction tool but blocks it as claim evidence.",
            "status": "NO_FREE_GREEN_INVERSE_GUARD_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SIGS4392_3_general_S_kernel_warning",
            "statement": "A general symmetric S^{ij} has a nonunique kernel under D_iD_j; TT/transverse, boundary, and affine-zero modes must be fixed by the parent action or bounded.",
            "derivation": "D_iD_j(S^{ij}+K^{ij})=D_iD_jS^{ij} whenever D_iD_jK^{ij}=0, but K can still carry stress, boundary traction, or metric variation payload.",
            "effect": "Prevents hiding physical tensor hair in the nonunique S kernel.",
            "status": "S_KERNEL_PAYLOAD_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "SIGS4392_4_residual_mismatch_bound",
            "statement": "If the sigma/S owner is unsigned, the physical bound quantity is R_S := rho_top-rho_H - c^-2D_iD_jS^{ij}, plus time, curvature, Ward, and boundary leakage.",
            "derivation": "Substitute the failed owner identity into the Newton/PPN source equations. The mismatch has the same Green-transfer status as earlier source-profile residuals and must be scored rather than ignored.",
            "effect": "Defines the fallback as a finite residual-bound row, not a dead end.",
            "status": "FALLBACK_BOUND_OBJECT_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def candidate_rows() -> List[Dict[str, str]]:
    script_path = str(Path(__file__).resolve())
    return [
        {
            "candidate_id": "SCAND4392_0_parent_sigmaS_laplacian",
            "branch": "parent_sigmaS_laplacian_owner",
            "residual_density_defined": "True",
            "sigma_or_s_parent_field_signed": "False",
            "laplacian_or_double_divergence_identity_signed": "False",
            "pre_readout_lock_signed": "False",
            "green_operator_parent_owned": "False",
            "zero_mode_gauge_fixed": "False",
            "affine_boundary_pairings_pass": "False",
            "static_tau_silence_pass": "False",
            "curvature_payload_zero_or_bounded": "False",
            "ward_conservation_owned": "False",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
        {
            "candidate_id": "SCAND4392_1_green_inverse_after_readout",
            "branch": "post_readout_green_inverse",
            "residual_density_defined": "True",
            "sigma_or_s_parent_field_signed": "False",
            "laplacian_or_double_divergence_identity_signed": "True",
            "pre_readout_lock_signed": "False",
            "green_operator_parent_owned": "False",
            "zero_mode_gauge_fixed": "False",
            "affine_boundary_pairings_pass": "False",
            "static_tau_silence_pass": "False",
            "curvature_payload_zero_or_bounded": "False",
            "ward_conservation_owned": "False",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
        {
            "candidate_id": "SCAND4392_2_general_S_kernel",
            "branch": "general_symmetric_S_owner",
            "residual_density_defined": "True",
            "sigma_or_s_parent_field_signed": "False",
            "laplacian_or_double_divergence_identity_signed": "False",
            "pre_readout_lock_signed": "False",
            "green_operator_parent_owned": "False",
            "zero_mode_gauge_fixed": "False",
            "affine_boundary_pairings_pass": "False",
            "static_tau_silence_pass": "False",
            "curvature_payload_zero_or_bounded": "False",
            "ward_conservation_owned": "False",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
    ]


def route_rows() -> List[Dict[str, str]]:
    return [
        {
            "route_id": "ROUTE4392_0_parent_sigmaS",
            "route": "parent signs rho_top-rho_H=Delta_h sigma_S before readout",
            "advantage": "closes S owner, affine double divergence, and exterior harmonic-null topological profile in one stroke",
            "risk": "current parent signature not found; boundary/zero-mode/static/Ward clauses still needed",
            "status": "BEST_NEXT_ROUTE_OPEN",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4392_1_green_inverse_bound",
            "route": "use sigma_S=Green[rho_top-rho_H] only as a bound construction",
            "advantage": "gives finite residual and boundary/projection quantities to score",
            "risk": "post-readout inverse is not derivation evidence",
            "status": "BOUND_TOOL_ONLY",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4392_2_general_S",
            "route": "general symmetric tensor S^{ij}",
            "advantage": "more flexible than trace sigma route",
            "risk": "large kernel can hide TT/boundary stress unless parent-fixed",
            "status": "KERNEL_GAUGE_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "SBND4392_0_residual_mismatch",
            "quantity": "R_S=rho_top-rho_H-c^-2D_iD_jS^{ij}",
            "needed_input": "norm/profile or theorem-zero for R_S on W_H",
            "arena": "Newton/PPN/source profile",
            "source_path": "MISSING_SIGMAS_RESIDUAL_MISMATCH_ROW",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "SBND4392_1_green_boundary",
            "quantity": "sigma_S and normal derivative boundary pairings",
            "needed_input": "affine Green boundary silence or finite pairings",
            "arena": "affine center/topological moments",
            "source_path": "MISSING_SIGMAS_BOUNDARY_PAIRINGS",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "SBND4392_2_zero_mode",
            "quantity": "kernel/zero-mode of Delta_h or D_iD_j",
            "needed_input": "parent gauge/normalization fixing constant, harmonic, and TT kernel pieces",
            "arena": "stress/PPN/boundary",
            "source_path": "MISSING_SIGMAS_ZERO_MODE_GAUGE",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "SBND4392_3_static_time",
            "quantity": "L_tau sigma_S or L_tau S^{ij}",
            "needed_input": "static certificate or finite time-leak bound",
            "arena": "PPN pressure/aniso",
            "source_path": "MISSING_SIGMAS_STATIC_TIME_ROW",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "SBND4392_4_curvature_ward",
            "quantity": "curvature commutator plus nabla_mu DeltaT_U^{mu nu}",
            "needed_input": "curvature remainder bound and U/S equation Ward identity or exchange current",
            "arena": "Bianchi/local GR",
            "source_path": "MISSING_SIGMAS_CURVATURE_WARD_ROW",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "local_GR": "sigma/S owner route derived but parent identity and payload gates unsigned",
        "Newton": "R_S mismatch and Green boundary pairings lack theorem-zero or source rows",
        "PPN": "S kernel, time leakage, pressure/aniso and curvature/Ward payloads remain open",
        "clock": "static tau lock from 4391 remains unsigned",
        "EM_Maxwell": "EM guard is supported but does not supply sigma/S owner identity",
        "R10_WEP": "residual owner/coupling projection rows remain nonclaim",
    }
    return [
        {
            "gate_id": f"CG4392_{index}_{arena}",
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
            "decision_id": "DEC4392_0",
            "decision": DECISION,
            "summary": "4392 derives the trace-electric sigma_S owner route: if the parent signs rho_top-rho_H=Delta_h sigma_S before readout, then S^{ij}=c^2h^{ij}sigma_S supplies the electric-U density owner and welds the old Laplacian-null topological moment theorem into the local-GR route. It also proves that post-readout Green inversion is only a bound tool, not a derivation.",
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
            "summary": "sigma_S is now the best concrete S-owner route, but parent action signature, zero-mode/boundary/static/Ward clauses remain open.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4392_0",
            "target": NEXT_TARGET,
            "question": "Can a parent action or constraint actually sign rho_top-rho_H=Delta_h sigma_S before readout, including zero-mode, boundary, static and Ward clauses?",
            "preferred_route": "construct the parent sigma_S action/constraint signature, not merely the Green inverse.",
            "fallback_route": "fill the first R_S residual mismatch row and sigma_S boundary/static/curvature/Ward bounds.",
            "avoid": "using Green inversion after seeing rho_top-rho_H as proof, hiding tensor kernel modes, or claiming from exterior moment silence alone.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    gate_output: List[Dict[str, str]],
    routes: List[Dict[str, str]],
    bounds: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 408 PPC4161 transition: sigmaS residual owner or electric-U bound row

Marker: `{MARKER}`

## Result

4392 finds the cleanest `S^{{ij}}` owner route so far:

`rho_top-rho_H = Delta_h sigma_S`,

then in the electric-U branch:

`S^{{ij}} = c^2 h^{{ij}} sigma_S`,

so:

`c^-2 D_iD_j S^{{ij}} = rho_top-rho_H`

up to explicit curvature/connection/boundary payloads.

This welds the older Laplacian-null topological theorem into the newer electric-U field-theory branch. But the key guard is also derived: `sigma_S=Green[rho_top-rho_H]` after readout is not proof. It is only a representation/bound tool unless the Green operator, zero modes, boundary conditions, and S sector are parent-owned before readout.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Theorem Rows\n\n"
    for row in theorems:
        text += f"### {row['theorem_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- Status: `{row['status']}`\n\n"
    text += "## Sigma/S Owner Gate\n\n"
    for row in gate_output:
        text += f"- `{row['candidate_id']}`: pass=`{row['sigma_s_owner_pass']}`, owner_identity_ready=`{row['owner_identity_ready']}`, closed `{row['closed_clause_count']}/{row['total_clause_count']}`, failed `{row['failed_clauses']}`.\n"
    text += "\n## Routes\n\n"
    for row in routes:
        text += f"- `{row['route_id']}`: {row['route']} — status `{row['status']}`.\n"
    text += "\n## Bound Rows\n\n"
    for row in bounds:
        text += f"- `{row['bound_id']}`: `{row['quantity']}` in `{row['arena']}` needs {row['needed_input']}.\n"
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
        f"""# 4392 Y5 R2FR: sigmaS residual owner or electric-U bound row

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
## 4392 local spine update: sigmaS electric owner route

Marker: `{MARKER}`

Spine update: `sigma_S` is now the preferred concrete owner candidate for the electric-U `S^ij` sector. If the parent signs `rho_top-rho_H=Delta_h sigma_S`, then `S^ij=c^2h^ij sigma_S` supplies the needed density owner and connects the Laplacian-null topological profile theorem to local affine closure. This remains nonclaim because a post-readout Green inverse is not a derivation, and parent zero-mode, boundary, static, curvature and Ward clauses remain open.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4392 packet update: sigmaS residual owner fork

Marker: `{PACKET_MARKER}`

Packet update: the electric-U route now reduces to a sharper parent signature: derive `rho_top-rho_H=Delta_h sigma_S` before readout. If signed, this gives `S^ij=c^2h^ij sigma_S` and welds exterior harmonic-null safety to the local double-divergence owner. If unsigned, the retained object is `R_S=rho_top-rho_H-c^-2D_iD_jS^ij` plus boundary, zero-mode, static, curvature and Ward rows.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4392 derives the trace-electric sigma_S owner route for the electric-U branch. If the parent signs rho_top-rho_H=Delta_h sigma_S before readout, then S^{ij}=c^2 h^{ij} sigma_S gives c^-2D_iD_jS^{ij}=rho_top-rho_H in the local weak-static branch, up to explicit curvature/connection/boundary payloads. This welds the older Laplacian-null topological moment theorem into the electric-U local-GR route. A no-free-Green-inverse guard is also derived: solving sigma_S=Delta_h^{-1}(rho_top-rho_H) after readout is a representation/bound tool, not a parent derivation. No local-GR/Newton/PPN/clock/orbital/R10 claim fires.",
            "4392 source register, sigma/S theorem rows, owner gate input/output, route rows, bound rows, claim gates, decision, status, next target and validation CSV.",
            "sigmaS_trace_electric_owner_route_derived_parent_signature_unsigned_nonclaim",
            "Construct a parent sigma_S action/constraint signature or fill first residual mismatch, boundary, zero-mode, static, curvature and Ward bound rows.",
            "Using post-readout Green inversion as proof, hiding S-kernel stress, ignoring boundary/zero-mode payload, or claiming from exterior moment silence alone.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4392_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_THEOREMS.csv")
    gate_output = read_csv(GATE_OUTPUT_PATH)
    routes = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4392_ROUTE_ROWS.csv")
    bounds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4392_BOUND_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4392_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4392_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4392_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4392_2_sigma_route_derived", any(row["theorem_id"] == "SIGS4392_0_trace_electric_owner" for row in theorems), "trace-electric sigma route staged")
    add("VAL4392_3_green_guard", any(row["theorem_id"] == "SIGS4392_2_green_inverse_no_free_claim" for row in theorems), "no-free-Green-inverse guard staged")
    add("VAL4392_4_owner_gate_fails_closed", all(row["sigma_s_owner_pass"] == "False" and row["valid_for_claim"] == "False" for row in gate_output), "owner candidates fail closed")
    add("VAL4392_5_parent_route_open", any(row["route_id"] == "ROUTE4392_0_parent_sigmaS" for row in routes), "parent sigmaS route row present")
    add("VAL4392_6_bound_rows_nonclaim", len(bounds) >= 5 and all(row["valid_for_claim"] == "False" and "MISSING" in row["source_path"] for row in bounds), "bound rows staged nonclaim")
    add("VAL4392_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4392_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4392_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4392_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4392_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4392_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4392_13_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4392_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4392_15_runner_exists", GATE_RUNNER_PATH.exists() and "def evaluate_sigma_s_owner_rows" in read_text(GATE_RUNNER_PATH), "sigma/S owner gate runner exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = theorem_rows()
    gate_inputs = candidate_rows()
    routes = route_rows()
    bounds = bound_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4392_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4392_SIGMA_S_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4392_ROUTE_ROWS.csv": routes,
        "P8_Y5_R2FR_4392_BOUND_ROWS.csv": bounds,
        "P8_Y5_R2FR_4392_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4392_DECISION.csv": decisions,
        "P8_Y5_R2FR_4392_STATUS.csv": statuses,
        "P8_Y5_R2FR_4392_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [GATE_INPUT_PATH]
    write_csv(GATE_INPUT_PATH, gate_inputs)
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    gate_output = evaluate_sigma_s_owner_rows(GATE_INPUT_PATH)
    write_csv(GATE_OUTPUT_PATH, gate_output)
    csv_paths.append(GATE_OUTPUT_PATH)

    write_formal_doc(sources, theorems, gate_output, routes, bounds, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
