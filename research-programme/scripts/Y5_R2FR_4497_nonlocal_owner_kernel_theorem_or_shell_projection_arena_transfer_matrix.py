from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4497"
CLAIM_ID = "L-339"
MARKER = "PPC4161_NONLOCAL_OWNER_KERNEL_THEOREM_OR_SHELL_PROJECTION_ARENA_TRANSFER_MATRIX_4497"
PACKET_MARKER = "PPC4161_PACKET_NONLOCAL_OWNER_KERNEL_THEOREM_OR_SHELL_PROJECTION_ARENA_TRANSFER_MATRIX_4497"
DECISION = "CONDITIONAL_KERNEL_THEOREM_DERIVED_BUT_PARENT_SIGNATURE_UNSIGNED_TRANSFER_MATRIX_STAGED_NONCLAIM"
NEXT_TARGET = "4498-Y5-R2FR-shell-projection-arena-operator-source-fill-or-owner-kernel-parent-signature.md"

FORMAL_PATH = FORMAL / "513-PPC4161-nonlocal-owner-kernel-theorem-or-shell-projection-arena-transfer-matrix.md"
DOC_PATH = POST / "4497-Y5-R2FR-nonlocal-owner-kernel-theorem-or-shell-projection-arena-transfer-matrix.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4497_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4497_SOURCE_REGISTER.csv"
CLAUSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4497_KERNEL_THEOREM_CLAUSES.csv"
PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4497_CONDITIONAL_KERNEL_PROOF.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4497_SHELL_PROJECTION_ARENA_TRANSFER_MATRIX.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4497_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4497_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4497_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4497_DECISION.csv"

FORMAL_512 = FORMAL / "512-PPC4161-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md"
POST_4496 = POST / "4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md"
STATUS_4496 = SOURCE_DIR / "P8_Y5_R2FR_4496_STATUS.csv"
COMPARATOR_4496 = SOURCE_DIR / "P8_Y5_R2FR_4496_SHELL_PROJECTION_COMPARATOR.csv"
THEOREM_4496 = SOURCE_DIR / "P8_Y5_R2FR_4496_TERMINAL_PROJECTION_THEOREM_AUDIT.csv"
NEXT_4496 = SOURCE_DIR / "P8_Y5_R2FR_4496_NEXT_TARGET.csv"
POST_4284 = POST / "4284-Y5-R2FR-real-transition-shell-profile-calculator-and-threshold-comparator.md"
SUPPRESSION_4284 = SOURCE_DIR / "P8_Y5_R2FR_4284_SUPPRESSION_REQUIREMENTS.csv"
POST_4277 = POST / "4277-Y5-R2FR-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"
POST_511 = FORMAL / "511-PPC4161-Ward-cohomology-public-projection-theorem-or-CDeltaKTF-closure-comparator.md"
GATE_4496 = SCRIPT_DIR / "Y5_R2FR_4496_real_DeltaKTF_shell_profile_inputs_or_terminal_projection_parent_theorem.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4497_00_formal512", "4496 formal handoff", FORMAL_512, "generic DeltaKTF / transition shell:", "states standard matter descent does not erase the generic shell"),
        ("SRC4497_01_post4496", "4496 post mirror", POST_4496, "standard matter-interface descent is conditionally derived", "private mirror for 4496"),
        ("SRC4497_02_status4496", "4496 status", STATUS_4496, "parent_nonlocal_owner_kernel_or_explicit_shell_projection_factor", "sharpest open clause"),
        ("SRC4497_03_comparator4496", "4496 shell comparator", COMPARATOR_4496, "COMP4284_0_bare", "real imported shell PPN suppression factors"),
        ("SRC4497_04_theorem4496", "4496 theorem audit", THEOREM_4496, "TPT4496_3_nonlocal_owner_kernel", "best remaining theorem target"),
        ("SRC4497_05_next4496", "4496 next target", NEXT_4496, "4497-Y5-R2FR-nonlocal-owner-kernel-theorem-or-shell-projection-arena-transfer-matrix.md", "selected target"),
        ("SRC4497_06_post4284", "4284 shell result", POST_4284, "fails by 2.2821012202909584e+16", "real shell profile failure"),
        ("SRC4497_07_suppression4284", "4284 suppression requirement", SUPPRESSION_4284, "REQ4284_2_nonlocal", "nonlocal projector requirement"),
        ("SRC4497_08_post4277", "4277 matter descent", POST_4277, "STANDARD_BRANCH_MATTER_INTERFACE_DESCENT_DERIVES_GX_ZERO_CONDITIONAL_NONCLAIM", "quotient matter descent template"),
        ("SRC4497_09_formal511", "4495 support-separated collar", POST_511, "support-separated compact local collar: conditional zero survives", "conditional collar zero, not generic shell"),
        ("SRC4497_10_script4496", "4496 generator", GATE_4496, "CHECKPOINT = \"4496\"", "reproducible predecessor script"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def clause_rows() -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "K4497_0_parent_quotient_owner",
            "clause": "one parent quotient owns public local response",
            "mathematical_statement": "there is q:P->B and F_loc = Fbar_loc o q for the public local metric/clock/orbital response through the stated order",
            "status": "TEMPLATE_FROM_4277_NOT_SIGNED_FOR_GENERIC_SHELL",
            "evidence": "4277 supplies this pattern for ordinary matter descent",
            "missing_parent_signature": "the same descent has not been shown for DeltaKTF transition-shell source response",
            "consequence_if_signed": "all q-vertical shell variations are public-response silent",
            "valid_for_claim": False,
        },
        {
            "clause_id": "K4497_1_shell_verticality",
            "clause": "DeltaKTF shell is vertical",
            "mathematical_statement": "Delta Phi_shell in ker(Dq), equivalently Dq[Delta Phi_shell]=0",
            "status": "UNSIGNED",
            "evidence": "4496 identifies this as the missing kernel membership",
            "missing_parent_signature": "no current parent row proves DeltaKTF is a q-kernel direction",
            "consequence_if_signed": "D(Fbar_loc o q)[Delta Phi_shell]=0",
            "valid_for_claim": False,
        },
        {
            "clause_id": "K4497_2_boundary_silence",
            "clause": "no boundary re-entry",
            "mathematical_statement": "any exact current or integration-by-parts remainder has zero local boundary/readout flux",
            "status": "SIGNED_ONLY_FOR_SUPPORT_SEPARATED_COLLAR_NOT_GENERIC_SHELL",
            "evidence": "4495 has a support-separated collar zero; 4496 refuses to extend it to the generic shell",
            "missing_parent_signature": "generic transition-shell boundary/local projection silence is not proved",
            "consequence_if_signed": "no hidden exact term re-enters P_metric_loc",
            "valid_for_claim": False,
        },
        {
            "clause_id": "K4497_3_no_representative_coefficients",
            "clause": "no representative-level shell coefficients",
            "mathematical_statement": "C_DeltaKTF, epsilon_shell, and arena-specific tau_shell are not free representative data once q is fixed",
            "status": "UNSIGNED",
            "evidence": "4494/4496 show closure coefficients are otherwise required",
            "missing_parent_signature": "need parent action/Noether identity forbidding representative Weyl/disformal/source coefficients",
            "consequence_if_signed": "explicit tiny projection coefficients become unnecessary",
            "valid_for_claim": False,
        },
        {
            "clause_id": "K4497_4_arena_transfer_fallback",
            "clause": "if kernel proof is unsigned, use explicit arena transfer",
            "mathematical_statement": "epsilon_shell^arena <= allowance_arena / raw_shell_response_arena",
            "status": "ACTIVE_FALLBACK",
            "evidence": "4496 imports real PPN factor 4.381926581996672e-17 for bare shell",
            "missing_parent_signature": "arena transfer operators for J2, clocks, orbital, R10 and EM stress are not all sourced",
            "consequence_if_signed": "nonclaim rows become scoreable once source paths and units exist",
            "valid_for_claim": False,
        },
    ]


def proof_rows() -> List[Dict[str, object]]:
    return [
        {
            "proof_id": "P4497_0_define_public_response",
            "step": "Define the local observable response",
            "equation": "O_loc[Phi] = F_loc[Phi] = Fbar_loc(q(Phi)) + B_boundary[Phi]",
            "depends_on": "K4497_0_parent_quotient_owner;K4497_2_boundary_silence",
            "conclusion": "public response can only see quotient data plus boundary re-entry",
            "signed_by_parent": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "P4497_1_take_shell_variation",
            "step": "Vary in the transition-shell direction",
            "equation": "delta_shell O_loc = D Fbar_loc|q(Phi) [Dq(Delta Phi_shell)] + delta_shell B_boundary",
            "depends_on": "chain rule on quotient map",
            "conclusion": "all possible leakage is kernel failure or boundary failure",
            "signed_by_parent": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "P4497_2_apply_verticality",
            "step": "Apply verticality",
            "equation": "Dq(Delta Phi_shell)=0",
            "depends_on": "K4497_1_shell_verticality",
            "conclusion": "bulk public response vanishes",
            "signed_by_parent": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "P4497_3_apply_boundary_silence",
            "step": "Apply boundary silence",
            "equation": "delta_shell B_boundary=0",
            "depends_on": "K4497_2_boundary_silence",
            "conclusion": "no exact-current or shell-edge term returns to the public metric",
            "signed_by_parent": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "P4497_4_conditional_kernel_theorem",
            "step": "Conditional theorem",
            "equation": "K4497_0 & K4497_1 & K4497_2 & K4497_3 => P_metric_loc(DeltaKTF_shell)=0",
            "depends_on": "all kernel clauses",
            "conclusion": "epsilon_shell=0 would follow without tuning, but only if the parent signs the clauses",
            "signed_by_parent": False,
            "valid_for_claim": False,
        },
    ]


def comparator_map() -> Dict[str, Dict[str, str]]:
    return {row["source_comparator_id"]: row for row in read_csv(COMPARATOR_4496)}


def arena_rows() -> List[Dict[str, object]]:
    comparators = comparator_map()
    bare = comparators.get("COMP4284_0_bare", {})
    u2 = comparators.get("COMP4284_1_U2", {})
    wide = comparators.get("COMP4284_2_wide", {})
    return [
        {
            "arena_id": "A4497_0_PPN_bare",
            "arena": "PPN/local metric",
            "transfer_quantity": "epsilon_shell_PPN_bare",
            "raw_response_source": "4496/4284 bare_transition_shell",
            "required_upper_bound": bare.get("required_projection_factor_to_pass", ""),
            "numeric_ready": bool(bare),
            "status": "REAL_IMPORTED_BOUND_FACTOR_NONCLAIM",
            "source_path": str(COMPARATOR_4496),
            "next_input": "derive kernel theorem or source epsilon_shell_PPN <= bound",
            "valid_for_claim": False,
        },
        {
            "arena_id": "A4497_1_PPN_U2",
            "arena": "PPN/local metric with U_B^2 suppression",
            "transfer_quantity": "epsilon_shell_PPN_U2",
            "raw_response_source": "4496/4284 U_B2_transition_shell",
            "required_upper_bound": u2.get("required_projection_factor_to_pass", ""),
            "numeric_ready": bool(u2),
            "status": "REAL_IMPORTED_BOUND_FACTOR_NONCLAIM",
            "source_path": str(COMPARATOR_4496),
            "next_input": "derive kernel theorem or source epsilon_shell_PPN_U2 <= bound",
            "valid_for_claim": False,
        },
        {
            "arena_id": "A4497_2_PPN_wide_shell",
            "arena": "PPN/local metric wide shell",
            "transfer_quantity": "epsilon_shell_PPN_wide",
            "raw_response_source": "4496/4284 wide_transition_shell_width_100",
            "required_upper_bound": wide.get("required_projection_factor_to_pass", ""),
            "numeric_ready": bool(wide),
            "status": "REAL_IMPORTED_BOUND_FACTOR_NONCLAIM",
            "source_path": str(COMPARATOR_4496),
            "next_input": "derive kernel theorem or source epsilon_shell_PPN_wide <= bound",
            "valid_for_claim": False,
        },
        {
            "arena_id": "A4497_3_J2_quadrupole",
            "arena": "J2/quadrupole orbital precession",
            "transfer_quantity": "epsilon_shell_J2",
            "raw_response_source": "DeltaKTF STF/quadrupole transfer branch",
            "required_upper_bound": "MISSING_ARENA_TRANSFER_OPERATOR",
            "numeric_ready": False,
            "status": "SOURCE_READY_BLOCKED",
            "source_path": "",
            "next_input": "source raw_shell_response_J2 and allowance_J2 in same normalization",
            "valid_for_claim": False,
        },
        {
            "arena_id": "A4497_4_clocks",
            "arena": "clock/redshift/fine-structure readout",
            "transfer_quantity": "epsilon_shell_clock",
            "raw_response_source": "shared local source-leg / clock readout rows",
            "required_upper_bound": "MISSING_CLOCK_SHELL_TRANSFER",
            "numeric_ready": False,
            "status": "SOURCE_READY_BLOCKED",
            "source_path": "",
            "next_input": "source tau_clock/readout projection from parent or keep bound row nonclaim",
            "valid_for_claim": False,
        },
        {
            "arena_id": "A4497_5_orbital",
            "arena": "orbital dynamics / ephemeris",
            "transfer_quantity": "epsilon_shell_orbital",
            "raw_response_source": "local metric shell response projected to orbital elements",
            "required_upper_bound": "MISSING_ORBITAL_TRANSFER_OPERATOR",
            "numeric_ready": False,
            "status": "SOURCE_READY_BLOCKED",
            "source_path": "",
            "next_input": "source mapping from shell metric residual to orbital residual vector",
            "valid_for_claim": False,
        },
        {
            "arena_id": "A4497_6_R10",
            "arena": "R10/fifth-force alpha(lambda)",
            "transfer_quantity": "epsilon_shell_R10",
            "raw_response_source": "R10 alpha row plus shell projection",
            "required_upper_bound": "MISSING_R10_SHELL_ALPHA_OPERATOR",
            "numeric_ready": False,
            "status": "SOURCE_READY_BLOCKED",
            "source_path": "",
            "next_input": "source K_X Qbar_XH qbar_XT tau_R10 or prove shell kernel zero",
            "valid_for_claim": False,
        },
        {
            "arena_id": "A4497_7_EM_Poynting",
            "arena": "EM stress / Poynting-vector route",
            "transfer_quantity": "epsilon_shell_EM_stress",
            "raw_response_source": "possible EM stress-energy projection of motion/background field",
            "required_upper_bound": "MISSING_EM_STRESS_TRANSFER_OPERATOR",
            "numeric_ready": False,
            "status": "SOURCE_READY_BLOCKED_INCLUDED_FOR_ROUTE_DISCIPLINE",
            "source_path": "",
            "next_input": "derive whether Poynting/EM stress descends through the same quotient or has an independent vertex",
            "valid_for_claim": False,
        },
    ]


def gate_rows(clauses: Sequence[Mapping[str, object]], arenas: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    unsigned = [row["clause_id"] for row in clauses if row.get("status") not in {"ACTIVE_FALLBACK"} and str(row.get("status")).find("UNSIGNED") >= 0]
    non_numeric = [row["arena_id"] for row in arenas if str(row.get("numeric_ready")).lower() != "true"]
    return [
        {
            "gate_id": "CG4497_0_kernel_theorem_parent_signed",
            "gate": "nonlocal owner/kernel theorem can zero generic shell",
            "passed": False,
            "blocking_rows": ";".join(unsigned),
            "claim_allowed": False,
            "detail": "conditional theorem is mathematically clean but parent signatures are unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4497_1_ppn_transfer_bound_ready",
            "gate": "PPN shell projection has numeric imported factor",
            "passed": True,
            "blocking_rows": "",
            "claim_allowed": False,
            "detail": "numeric factors exist, but no sourced epsilon_shell value or zero theorem exists",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4497_2_all_arena_transfer_ready",
            "gate": "J2/PPN/clocks/orbital/R10/EM all have source-normalized transfer operators",
            "passed": False,
            "blocking_rows": ";".join(non_numeric),
            "claim_allowed": False,
            "detail": "only PPN factors are numeric; other arena operators are source-ready but blocked",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4497_3_local_GR_promotion",
            "gate": "local GR/Newton recovery from generic shell safety",
            "passed": False,
            "blocking_rows": "CG4497_0_kernel_theorem_parent_signed;CG4497_2_all_arena_transfer_ready",
            "claim_allowed": False,
            "detail": "do not promote local GR until kernel theorem or all arena transfers close",
            "valid_for_claim": False,
        },
    ]


def status_rows(arenas: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    ppn = [row for row in arenas if row.get("arena_id") == "A4497_0_PPN_bare"]
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "conditional_kernel_theorem": "DERIVED_AS_CONTRACT_NOT_PARENT_SIGNED",
            "ppn_bare_required_epsilon": ppn[0].get("required_upper_bound") if ppn else "",
            "local_GR_claim": False,
            "sharpest_open_clause": "prove DeltaKTF_shell in ker(Dq) and boundary silence, or source epsilon_shell arena operators",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4497_0",
            "target": NEXT_TARGET,
            "preferred_route": "try parent signature for DeltaKTF_shell in ker(Dq) plus boundary silence",
            "fallback_route": "fill shell projection arena operators row-by-row starting with PPN then J2/orbital",
            "do_not_do": "treat the conditional theorem as a local-GR claim before parent signatures are sourced",
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "what_moved_forward": "4497 converts the shell issue into an exact conditional quotient-kernel theorem and an arena transfer matrix",
            "what_remains_blocked": "the parent has not yet signed DeltaKTF shell verticality, generic boundary silence, or arena transfer operators beyond PPN",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def body(
    sources: Sequence[Mapping[str, object]],
    clauses: Sequence[Mapping[str, object]],
    proofs: Sequence[Mapping[str, object]],
    arenas: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4497 — Nonlocal Owner Kernel Theorem Or Shell Projection Arena Transfer Matrix

Marker: `{MARKER}`
Claim: `{CLAIM_ID}`
Decision: `{DECISION}`
Generated: `{STAMP}`

## Result

This checkpoint takes the leap that 4496 selected. The clean mathematical route is now explicit:

If the public local response descends through a parent quotient `q`, the generic `DeltaKTF` transition-shell variation is vertical (`Delta Phi_shell in ker(Dq)`), and boundary/exact-current terms are silent, then

`P_metric_loc(DeltaKTF_shell) = 0`.

That is a real conditional theorem, not just a vibe. But it is not yet a project claim, because the current corpus has not parent-signed the two dangerous clauses: generic shell verticality and generic shell boundary silence. So 4497 also stages the non-tuned fallback: explicit arena transfer coefficients `epsilon_shell^arena`.

## Short Derivation

Let the public observable/local metric response be

`O_loc[Phi] = F_loc[Phi] = Fbar_loc(q(Phi)) + B_boundary[Phi]`.

For a shell variation,

`delta_shell O_loc = D Fbar_loc|q(Phi)[Dq(Delta Phi_shell)] + delta_shell B_boundary`.

Therefore the shell is locally silent only if `Dq(Delta Phi_shell)=0` and `delta_shell B_boundary=0`. This is the exact contract a parent action must satisfy.

## Kernel Clauses

{table(clauses)}

## Conditional Proof Ledger

{table(proofs)}

## Shell Projection Arena Transfer Matrix

{table(arenas)}

## Claim Gates

{table(gates)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def update_claims_register() -> None:
    row = (
        f"{CLAIM_ID},local_gr_newton_r10_shell_kernel,"
        "\"4497 derives the exact conditional quotient-kernel theorem for generic DeltaKTF shell silence and stages the arena transfer matrix; parent signatures remain unsigned, so no local-GR/Newton/R10 claim is promoted.\","
        "\"4497 kernel clauses, conditional proof ledger, shell projection arena transfer matrix, claim gates, status and validation.\","
        f"private_conditional_kernel_theorem_nonclaim,{NEXT_TARGET},"
        "\"treating conditional quotient-kernel theorem as parent-signed shell safety.\","
        f"local_gr_newton_r10_shell_kernel,{FORMAL_PATH},{NEXT_TARGET},"
        "\"prove DeltaKTF_shell in ker(Dq) plus generic boundary silence, or source explicit epsilon_shell arena operators\"\n"
    )
    existing = text(CLAIMS_PATH)
    if CLAIM_ID not in existing:
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(row)


def append_section_once(path: Path, marker: str, title: str, summary: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{summary}\n"
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(addition)


def validate(
    sources: Sequence[Mapping[str, object]],
    clauses: Sequence[Mapping[str, object]],
    proofs: Sequence[Mapping[str, object]],
    arenas: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    kernel_row = [row for row in proofs if row.get("proof_id") == "P4497_4_conditional_kernel_theorem"]
    ppn_row = [row for row in arenas if row.get("arena_id") == "A4497_0_PPN_bare"]
    add("VAL4497_0_sources_exist_and_needles_found", all(row.get("exists") is True and row.get("needle_found") is True for row in sources), "every source path exists and needles are found")
    add("VAL4497_1_conditional_kernel_theorem_written", bool(kernel_row) and "P_metric_loc" in str(kernel_row[0].get("equation")), "conditional quotient-kernel theorem written")
    add("VAL4497_2_parent_signatures_unsigned", any("UNSIGNED" in str(row.get("status")) for row in clauses), "generic shell clauses remain unsigned")
    add("VAL4497_3_ppn_numeric_factor_imported", bool(ppn_row) and float(ppn_row[0]["required_upper_bound"]) < 1.0e-16, str(ppn_row[0].get("required_upper_bound")) if ppn_row else "missing")
    add("VAL4497_4_arena_matrix_has_blocked_non_ppn_rows", len(arenas) >= 8 and any(row.get("numeric_ready") is False for row in arenas), "PPN numeric rows plus source-ready blocked arena rows")
    add("VAL4497_5_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4497_6_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4497_7_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET, NEXT_TARGET)
    add(
        "VAL4497_8_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, clauses, proofs, arenas, gates, statuses, next_targets]
            for row in group
        ),
        "all generated rows are private/nonclaim",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4497_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4497_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4497_11_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-339")
    add("VAL4497_12_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4497 markers")
    add("VAL4497_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    clauses = clause_rows()
    proofs = proof_rows()
    arenas = arena_rows()
    gates = gate_rows(clauses, arenas)
    statuses = status_rows(arenas)
    next_targets = next_rows()
    decisions = decision_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CLAUSE_CSV, clauses)
    write_csv(PROOF_CSV, proofs)
    write_csv(ARENA_CSV, arenas)
    write_csv(GATE_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    doc = body(sources, clauses, proofs, arenas, gates, statuses, next_targets, decisions)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4497 Nonlocal Owner Kernel Theorem Or Shell Projection Arena Transfer Matrix",
        "4497 makes the shell rescue route exact: if public local response descends through the parent quotient, the generic DeltaKTF shell is q-vertical, and boundary/exact-current terms are silent, then the local metric projection vanishes. The theorem is conditional, not parent-signed; the fallback is now an explicit arena transfer matrix with PPN numeric factors imported from 4496 and J2/clocks/orbital/R10/EM rows blocked until transfer operators are sourced.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4497 Packet Integration",
        "The packet now separates the mathematical kernel theorem from project ownership. Kernel silence is derivable under exact quotient and boundary clauses, but local-GR/Newton/R10 promotion remains blocked until those clauses are parent-signed or the arena transfer matrix is filled with sourced epsilon_shell coefficients.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [SOURCE_REGISTER, CLAUSE_CSV, PROOF_CSV, ARENA_CSV, GATE_CSV, STATUS_CSV, NEXT_CSV, DECISION_CSV]
    validations = validate(sources, clauses, proofs, arenas, gates, statuses, next_targets, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
