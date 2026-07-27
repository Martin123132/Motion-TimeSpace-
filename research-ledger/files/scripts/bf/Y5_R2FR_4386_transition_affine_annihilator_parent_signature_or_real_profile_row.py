from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from topological_affine_first_moment_gate import affine_first_moment_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PARENT_DIR = POST / "source-intake" / "parent-action"

CHECKPOINT = "4386"
CLAIM_ID = "L-227"
MARKER = "PPC4161_TRANSITION_AFFINE_ANNIHILATOR_PARENT_SIGNATURE_OR_REAL_PROFILE_ROW_4386"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_AFFINE_ANNIHILATOR_PARENT_SIGNATURE_OR_REAL_PROFILE_ROW_4386"
DECISION = "DOUBLE_DIVERGENCE_IMPROVEMENT_ROUTE_DERIVED_SINGLE_DIVERGENCE_REJECTED_PARENT_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4387-Y5-R2FR-transition-double-divergence-improvement-parent-owner-or-boundary-row.md"

FORMAL_PATH = FORMAL / "402-PPC4161-transition-affine-annihilator-parent-signature-or-real-profile-row.md"
DOC_PATH = POST / "4386-Y5-R2FR-transition-affine-annihilator-parent-signature-or-real-profile-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4386_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
AFFINE_HELPER_PATH = SCRIPT_DIR / "topological_affine_first_moment_gate.py"
SMOKE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4386_IMPROVEMENT_AFFINE_SMOKE_INPUT.csv"
SMOKE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4386_IMPROVEMENT_AFFINE_SMOKE_OUTPUT.csv"
SMOKE_ACCEPTANCE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4386_IMPROVEMENT_AFFINE_SMOKE_ACCEPTANCE.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4386_00_4385_formal": (
        FORMAL / "401-PPC4161-transition-topological-first-moment-zero-proof-or-real-profile-import.md",
        "D_top-H in Ann(Aff_1(W_H)).",
        "4385 handoff: affine annihilator is the exact center-branch target.",
    ),
    "SRC4386_01_4385_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4385_NEXT_TARGET.csv",
        "4386-Y5-R2FR-transition-affine-annihilator-parent-signature-or-real-profile-row.md",
        "Explicit 4386 target.",
    ),
    "SRC4386_02_4385_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4385_AFFINE_THEOREMS.csv",
        "AF4385_5_parent_affine_annihilator_contract",
        "Parent affine-annihilator contract.",
    ),
    "SRC4386_03_4385_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4385_BOUNDARY_CONTRACT.csv",
        "BC4385_1_x",
        "Affine Laplacian boundary contract.",
    ),
    "SRC4386_04_143_boundary_gate": (
        FORMAL / "143-boundary-topological-backup-gate.md",
        "Exact superpotential",
        "Older warning: generic boundary/superpotential language is insufficient.",
    ),
    "SRC4386_05_299_superpotential": (
        FORMAL / "299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md",
        "The generic boundary/topological route fails as a derivation",
        "4283 result refusing generic superpotential promotion.",
    ),
    "SRC4386_06_191_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "EM/Poynting stress is already Hilbert-owned, not a hidden source.",
    ),
    "SRC4386_07_192_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "no-flux",
        "No-flux collar theorem source for boundary silence limits.",
    ),
    "SRC4386_08_2608_affine": (
        SOURCE_DIR / "P8_Y5_AFFINE_SOURCE_GATE_2608_SOURCE_ZERO_STATUS.csv",
        "SZ2608_0_F1",
        "Earlier affine-source obstruction remains unsigned.",
    ),
    "SRC4386_09_2220_improvement": (
        SOURCE_DIR / "P8_Y5_BRR545_2220_VALIDATION.csv",
        "trace-free improvement Khat route is real conditional math",
        "Trace-free improvement route exists as conditional math but was not birth-certified.",
    ),
    "SRC4386_10_helper": (
        AFFINE_HELPER_PATH,
        "def affine_first_moment_rows",
        "Affine residual runner reused for 4386 smoke.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def improvement_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "DD4386_0_double_divergence_affine_annihilator",
            "statement": "If D_top-H[f]=int_W f partial_i partial_j S^{ij} dV and the two Green boundary pairings vanish for every affine f, then D_top-H annihilates Aff_1(W_H).",
            "derivation": "Two integrations by parts give int f partial_i partial_j S^{ij}=int_boundary f n_i partial_j S^{ij}-int_boundary partial_i f n_j S^{ij}+int_W S^{ij} partial_i partial_j f. For affine f, partial_i partial_j f=0; boundary silence kills the rest.",
            "effect": "This is a concrete parent mechanism for the 4385 affine annihilator.",
            "status": "EXACT_THEOREM_DERIVED_PARENT_OWNER_MISSING",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DD4386_1_compact_support_corollary",
            "statement": "If S^{ij} and its first normal derivative have compact support inside W_H, the double-divergence residual automatically annihilates affine tests.",
            "derivation": "Compact interior support makes both boundary terms in DD4386_0 vanish.",
            "effect": "A compact improvement tensor is sufficient for Delta_M=0 and B_top=0 without requiring full profile equality.",
            "status": "EXACT_COROLLARY_PARENT_SUPPORT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DD4386_2_trace_laplacian_subcase",
            "statement": "The 4385 Laplacian route is the trace subcase S^{ij}=u_top delta^{ij}.",
            "derivation": "partial_i partial_j(u delta^{ij})=Delta u, so the affine boundary-pairing law reduces to the four Green pairings in 4385.",
            "effect": "Unifies the Laplacian route and a more general stress-improvement route.",
            "status": "EXACT_SUBCASE_IDENTIFIED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DD4386_3_single_divergence_counterexample",
            "statement": "A single divergence D=partial_i V^i is still insufficient for affine annihilation.",
            "derivation": "D[y^k]=int_boundary y^k V.n dS-int_W V^k dV, which need not vanish. The 4386 smoke counterexample keeps Delta_M=0 but produces B_top/R>0.",
            "effect": "Prevents downgrading the double-divergence route to generic superpotential language.",
            "status": "COUNTERPROOF_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DD4386_4_parent_owner_contract",
            "statement": "To claim the route, the parent action must identify rho_top-rho_H as partial_i partial_j S^{ij} with S^{ij} parent-owned before readout and affine-boundary silent on W_H.",
            "derivation": "DD4386_0 supplies the mathematics; source ownership, no post-readout recentering, and boundary silence are separate parent-action obligations.",
            "effect": "Turns the next missing piece into a precise birth certificate for S^{ij}, not a general source hunt.",
            "status": "CONTRACT_EXACT_PARENT_BIRTH_CERTIFICATE_MISSING",
            "valid_for_claim": "False",
        },
    ]


def boundary_pairing_rows() -> List[Dict[str, str]]:
    return [
        {
            "pairing_id": "BP4386_0_constant",
            "test_function": "f=1",
            "boundary_pairing": "int_boundary n_i partial_j S^{ij} dS",
            "zero_requirement": "boundary flux of partial_j S^{ij} vanishes",
            "kills": "Delta_M_top_H",
            "status": "FORMULA_EXACT_PARENT_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "pairing_id": "BP4386_1_linear_k",
            "test_function": "f=y^k",
            "boundary_pairing": "int_boundary y^k n_i partial_j S^{ij} dS - int_boundary n_j S^{kj} dS",
            "zero_requirement": "linear weighted derivative flux cancels S^{kj} traction flux",
            "kills": "B_top^k",
            "status": "FORMULA_EXACT_PARENT_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "pairing_id": "BP4386_2_compact_support",
            "test_function": "all f in Aff_1",
            "boundary_pairing": "S^{ij}|boundary=0 and n_i partial_j S^{ij}|boundary=0",
            "zero_requirement": "compact support or support-separated collar",
            "kills": "Delta_M_top_H and B_top",
            "status": "SUFFICIENT_CONDITION_EXACT_PARENT_SUPPORT_MISSING",
            "valid_for_claim": "False",
        },
    ]


def parent_signature_audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "PSA4386_0_source_object",
            "required_signature": "rho_top-rho_H = partial_i partial_j S^{ij} as a parent density identity",
            "evidence_now": "4385 gives affine target; earlier improvement/Khat routes are conditional but not tied to this topological density residual.",
            "status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_PARENT_DENSITY_IMPROVEMENT_IDENTITY",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PSA4386_1_owner_before_readout",
            "required_signature": "S^{ij} is defined on W_H before local/orbital readout and cannot be recentered/fitted after scoring",
            "evidence_now": "3037/3055 and 4384 keep source-readout/topological-profile ownership conditional.",
            "status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_PRE_READOUT_IMPROVEMENT_OWNER",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PSA4386_2_boundary_silence",
            "required_signature": "boundary pairings BP4386_0/BP4386_1 vanish on the local collar",
            "evidence_now": "192 no-flux is useful only for support-separated collars; 4283 rejected generic superpotential promotion.",
            "status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_AFFINE_BOUNDARY_SILENCE",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PSA4386_3_visible_EM_guard",
            "required_signature": "Maxwell/Poynting energy is not reintroduced as an extra topological residual",
            "evidence_now": "191 already Hilbert-owns EM/Poynting stress inside the compact selector.",
            "status": "SUPPORTED_GUARD_NOT_TOPOLOGICAL_PROOF",
            "missing_for_claim": "does not by itself identify D_top-H as double divergence",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PSA4386_4_verdict",
            "required_signature": "all parent owner and boundary clauses signed",
            "evidence_now": "The double-divergence theorem is derived, but the parent birth certificate is not present.",
            "status": "PARENT_SIGNATURE_UNSIGNED",
            "missing_for_claim": "proceed to 4387 parent owner/boundary row",
            "valid_for_claim": "False",
        },
    ]


def smoke_input_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    base = 10.0
    for index, (x_value, delta) in enumerate([(-2.0, 1.0), (-1.0, -2.0), (0.0, 2.0), (1.0, -2.0), (2.0, 1.0)]):
        rows.append(
            {
                "profile_id": "SMOKE4386_double_divergence_affine_silent",
                "profile_label": "synthetic second-difference improvement profile",
                "sample_id": f"SMOKE4386_dd_{index:03d}",
                "source_body": "synthetic_nonclaim",
                "arena": "affine_improvement_smoke_only",
                "x": f"{x_value:.16e}",
                "y": "0.0000000000000000e+00",
                "z": "0.0000000000000000e+00",
                "volume_weight": "1.0",
                "rho_H": f"{base:.16e}",
                "rho_top": f"{base + delta:.16e}",
                "R": "2.0000000000000000e+00",
                "source_profile_path": "SYNTHETIC_SMOKE_NOT_PHYSICAL",
                "input_valid_for_claim": "False",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    for index, (x_value, delta) in enumerate([(-2.0, -1.0), (-1.0, 0.0), (0.0, 0.0), (1.0, 0.0), (2.0, 1.0)]):
        rows.append(
            {
                "profile_id": "SMOKE4386_single_divergence_counterexample",
                "profile_label": "synthetic first-difference counterexample profile",
                "sample_id": f"SMOKE4386_sd_{index:03d}",
                "source_body": "synthetic_nonclaim",
                "arena": "affine_improvement_smoke_only",
                "x": f"{x_value:.16e}",
                "y": "0.0000000000000000e+00",
                "z": "0.0000000000000000e+00",
                "volume_weight": "1.0",
                "rho_H": f"{base:.16e}",
                "rho_top": f"{base + delta:.16e}",
                "R": "2.0000000000000000e+00",
                "source_profile_path": "SYNTHETIC_SMOKE_NOT_PHYSICAL",
                "input_valid_for_claim": "False",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def smoke_acceptance_rows(output_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    by_id = {row["profile_id"]: row for row in output_rows}
    dd = by_id["SMOKE4386_double_divergence_affine_silent"]
    sd = by_id["SMOKE4386_single_divergence_counterexample"]
    return [
        {
            "accept_id": "SIA4386_0_double_divergence_silent",
            "tested_output": "SMOKE4386_double_divergence_affine_silent",
            "value": dd["B_top_norm_over_R"],
            "threshold": "1e-12",
            "passed": str(dd["monopole_zero"] == "True" and dd["linear_affine_zero"] == "True"),
            "interpretation": "second-difference/double-divergence-like profile kills the affine residual",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "SIA4386_1_single_divergence_detected",
            "tested_output": "SMOKE4386_single_divergence_counterexample",
            "value": sd["B_top_norm_over_R"],
            "threshold": "> 1e-3",
            "passed": str(sd["monopole_zero"] == "True" and sd["linear_affine_zero"] == "False" and float(sd["B_top_norm_over_R"]) > 1.0e-3),
            "interpretation": "zero-monopole first-difference profile still has a first moment",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "SIA4386_2_smoke_nonclaim",
            "tested_output": "all smoke rows",
            "value": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in output_rows)),
            "threshold": "True",
            "passed": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in output_rows)),
            "interpretation": "synthetic demonstration cannot become evidence",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4386_0_double_divergence_theorem",
            "claim_tested": "D_top-H annihilates affine tests by double-divergence improvement",
            "required_inputs": "parent-owned S^{ij}, rho_top-rho_H=partial_i partial_j S^{ij}, affine boundary pairings zero",
            "status": "THEOREM_EXACT_PARENT_OWNER_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4386_1_single_divergence",
            "claim_tested": "generic divergence/superpotential is enough",
            "required_inputs": "would require int V^k and boundary-weighted flux cancellation",
            "status": "REJECTED_COUNTEREXAMPLE_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4386_2_real_profile",
            "claim_tested": "real profile row closes B_top/R",
            "required_inputs": "validator-clean rho_H/rho_top row; not synthetic smoke",
            "status": "RUNNER_READY_REAL_PROFILE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4386_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "topological affine branch plus higher moments/rest/readout/local projection closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4386_0",
            "decision": DECISION,
            "summary": (
                "4386 finds the cleanest mechanism so far for the affine-annihilator gap: if the topological/Hilbert residual density is a parent-owned double divergence partial_i partial_j S^{ij}, then it kills constants and linear test functions whenever the affine boundary pairings vanish. "
                "This is strictly stronger than generic divergence/superpotential language and avoids the previously rejected shortcut: a single divergence can have zero total charge but nonzero first moment. The synthetic smoke confirms this boundary: a second-difference profile has B_top/R=0, while a first-difference counterexample has nonzero B_top/R. "
                "The route is not claimed, because current files do not birth-certify S^{ij} as the actual rho_top-rho_H owner or prove the required boundary silence."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The next useful attack is a parent birth certificate for S^{ij} or a real boundary/profile row; not another generic superpotential sweep.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4386_0_mechanism",
            "object": "double-divergence improvement",
            "status": "EXACT_AFFINE_ANNIHILATOR_MECHANISM_DERIVED",
            "note": "partial_i partial_j S^{ij} kills Aff_1 under affine boundary silence.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4386_1_shortcut",
            "object": "single divergence/superpotential",
            "status": "REJECTED",
            "note": "zero monopole does not guarantee zero first moment.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4386_2_parent",
            "object": "S^{ij} owner and boundary silence",
            "status": "UNSIGNED",
            "note": "Need parent density identity and boundary pairings, or real profile input.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4386_3_next",
            "object": "next target",
            "status": "IMPROVEMENT_OWNER_OR_BOUNDARY_ROW_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4386_0",
            "target": NEXT_TARGET,
            "question": "Can the parent action identify rho_top-rho_H as a double-divergence improvement with silent affine boundary pairings, or must we fill boundary/profile rows?",
            "preferred_route": "derive S^{ij} from a parent stress-improvement/topological density birth certificate tied to rho_top-rho_H before readout.",
            "fallback_route": "create source-backed boundary-pairing rows BP4386_0/BP4386_1 or import a real profile through the affine runner.",
            "avoid": "generic superpotential claims, single-divergence shortcuts, total-charge-only arguments, synthetic smoke promotion, or post-readout profile recentering.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    boundary: List[Dict[str, str]],
    audit: List[Dict[str, str]],
    smoke_output: List[Dict[str, str]],
    smoke_acceptance: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: affine annihilator parent signature or real profile row

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4386 takes the affine target from 4385 and finds the best concrete mechanism:

```text
rho_top-rho_H = partial_i partial_j S^{{ij}}.
```

For any affine test function `f in span{{1,x,y,z}}`,

```text
partial_i partial_j f = 0.
```

Therefore two integrations by parts give affine annihilation if the boundary pairings vanish:

```text
int_W f partial_i partial_j S^{{ij}} dV
= int_boundary f n_i partial_j S^{{ij}} dS
- int_boundary partial_i f n_j S^{{ij}} dS.
```

So this route is not the old hand-wavy "superpotential" escape. It is a specific double-divergence improvement route with exact boundary obligations. A single divergence remains insufficient.

No local-GR/Newton/PPN/clock/orbital claim fires. The parent has not yet signed `S^{{ij}}` as the owner of `rho_top-rho_H`, and the boundary pairings are not source-backed.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Double-Divergence Theorems

{md_table(theorems, ["theorem_id", "statement", "derivation", "effect", "status"])}

## Boundary Pairing Contract

{md_table(boundary, ["pairing_id", "test_function", "boundary_pairing", "zero_requirement", "kills", "status"])}

## Parent Signature Audit

{md_table(audit, ["audit_id", "required_signature", "evidence_now", "status", "missing_for_claim"])}

## Improvement Smoke Output

{md_table(smoke_output, ["profile_id", "Delta_M_top_H", "B_top_x", "B_top_norm_over_R", "monopole_zero", "linear_affine_zero", "valid_for_claim", "current_status"])}

## Smoke Acceptance

{md_table(smoke_acceptance, ["accept_id", "tested_output", "value", "threshold", "passed", "interpretation"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4386: affine annihilator parent signature or real profile row

Marker: `{MARKER}`

## What changed

- Derived the double-divergence improvement route `rho_top-rho_H=partial_i partial_j S^{{ij}}`.
- Proved why it kills affine tests under boundary silence.
- Kept the single-divergence/superpotential shortcut rejected.
- Added synthetic smoke showing double-difference affine silence versus single-difference first-moment leakage.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4386 Transition affine annihilator parent signature or real profile row

Marker: `{MARKER}`

4386 identifies the strongest current mechanism for the 4385 affine-annihilator gap:

```text
rho_top-rho_H = partial_i partial_j S^{{ij}}.
```

Because affine tests have zero second derivative, this double-divergence residual annihilates `span{{1,x,y,z}}` once the explicit boundary pairings vanish. This is narrower and stronger than generic superpotential language, and it preserves the earlier rejection of single-divergence shortcuts.

The parent signature is still unsigned: `S^{{ij}}` must be born from the parent action as the actual owner of `rho_top-rho_H`, before readout, with affine boundary silence.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4386 packet update: double-divergence affine mechanism

Marker: `{PACKET_MARKER}`

Packet update: the affine first-moment gate can be closed if the topological/Hilbert residual density is parent-owned as a double divergence `partial_i partial_j S^{{ij}}` with silent affine boundary pairings. Generic exact divergence/superpotential language remains insufficient. Claim remains blocked until the parent action supplies the `S^{{ij}}` birth certificate or real boundary/profile rows.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4386 derives a concrete mechanism for the 4385 affine-annihilator gap: if rho_top-rho_H is a parent-owned double divergence partial_i partial_j S^{ij}, then constants and linear coordinate tests are killed under explicit affine boundary silence, because affine functions have zero second derivative. "
                "This preserves the rejection of generic divergence/superpotential shortcuts: a single divergence can have zero monopole but nonzero first moment. Synthetic smoke confirms the boundary between the mechanisms while remaining nonclaim. "
                "The parent action has not yet birth-certified S^{ij} as the actual topological/Hilbert residual owner and the boundary pairings are not source-backed, so no local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4386 source register, double-divergence theorem rows, boundary-pairing contract, parent signature audit, smoke input/output/acceptance, claim gates, decision, status, next target and validation CSV.",
            "double_divergence_improvement_route_derived_parent_unsigned_nonclaim",
            "Parent-birth-certify S^{ij} or fill source-backed affine boundary/profile rows.",
            "Generic superpotential claims, single-divergence shortcuts, total-charge-only arguments, synthetic smoke promotion, or post-readout profile recentering.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4386_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4386_DOUBLE_DIVERGENCE_THEOREMS.csv")
    audit = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4386_PARENT_SIGNATURE_AUDIT.csv")
    smoke = read_csv(SMOKE_OUTPUT_PATH)
    acceptance = read_csv(SMOKE_ACCEPTANCE_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4386_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4386_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4386_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add(
        "VAL4386_2_double_divergence_theorem",
        any(row["theorem_id"] == "DD4386_0_double_divergence_affine_annihilator" and row["status"] == "EXACT_THEOREM_DERIVED_PARENT_OWNER_MISSING" for row in theorems),
        "double-divergence affine theorem recorded",
    )
    add(
        "VAL4386_3_single_divergence_rejected",
        any(row["theorem_id"] == "DD4386_3_single_divergence_counterexample" for row in theorems),
        "single-divergence shortcut rejected",
    )
    add(
        "VAL4386_4_parent_unsigned",
        any(row["audit_id"] == "PSA4386_4_verdict" and row["status"] == "PARENT_SIGNATURE_UNSIGNED" for row in audit),
        "parent signature remains blocked honestly",
    )
    add(
        "VAL4386_5_smoke_boundary",
        any(row["profile_id"] == "SMOKE4386_double_divergence_affine_silent" and row["linear_affine_zero"] == "True" for row in smoke)
        and any(row["profile_id"] == "SMOKE4386_single_divergence_counterexample" and row["linear_affine_zero"] == "False" for row in smoke),
        "smoke distinguishes double divergence from single divergence",
    )
    add("VAL4386_6_acceptance_passed", all(row["passed"] == "True" for row in acceptance), "all smoke acceptance checks passed")
    add("VAL4386_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4386_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4386_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4386_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4386_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4386_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4386_13_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4386_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = improvement_theorem_rows()
    boundary = boundary_pairing_rows()
    audit = parent_signature_audit_rows()
    smoke_input = smoke_input_rows()
    write_csv(SMOKE_INPUT_PATH, smoke_input)
    smoke_output = affine_first_moment_rows(SMOKE_INPUT_PATH, 1.0e-12)
    write_csv(SMOKE_OUTPUT_PATH, smoke_output)
    smoke_acceptance = smoke_acceptance_rows(smoke_output)
    write_csv(SMOKE_ACCEPTANCE_PATH, smoke_acceptance)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4386_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4386_DOUBLE_DIVERGENCE_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4386_BOUNDARY_PAIRINGS.csv": boundary,
        "P8_Y5_R2FR_4386_PARENT_SIGNATURE_AUDIT.csv": audit,
        "P8_Y5_R2FR_4386_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4386_DECISION.csv": decisions,
        "P8_Y5_R2FR_4386_STATUS.csv": statuses,
        "P8_Y5_R2FR_4386_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [SMOKE_INPUT_PATH, SMOKE_OUTPUT_PATH, SMOKE_ACCEPTANCE_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorems, boundary, audit, smoke_output, smoke_acceptance, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
