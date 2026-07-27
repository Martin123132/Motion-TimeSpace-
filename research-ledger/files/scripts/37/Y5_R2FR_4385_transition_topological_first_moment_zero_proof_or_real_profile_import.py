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

CHECKPOINT = "4385"
CLAIM_ID = "L-226"
MARKER = "PPC4161_TRANSITION_TOPOLOGICAL_FIRST_MOMENT_ZERO_PROOF_OR_REAL_PROFILE_IMPORT_4385"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_TOPOLOGICAL_FIRST_MOMENT_ZERO_PROOF_OR_REAL_PROFILE_IMPORT_4385"
DECISION = "AFFINE_FIRST_MOMENT_THEOREM_DERIVED_PARENT_SIGNATURE_UNSIGNED_RUNNER_BUILT_NONCLAIM"
NEXT_TARGET = "4386-Y5-R2FR-transition-affine-annihilator-parent-signature-or-real-profile-row.md"

FORMAL_PATH = FORMAL / "401-PPC4161-transition-topological-first-moment-zero-proof-or-real-profile-import.md"
DOC_PATH = POST / "4385-Y5-R2FR-transition-topological-first-moment-zero-proof-or-real-profile-import.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4385_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
HELPER_PATH = SCRIPT_DIR / "topological_affine_first_moment_gate.py"
SMOKE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4383_CENTER_LOCK_SMOKE_INPUT.csv"
AFFINE_SMOKE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4385_AFFINE_FIRST_MOMENT_SMOKE.csv"
AFFINE_ACCEPTANCE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4385_AFFINE_SMOKE_ACCEPTANCE.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4385_00_4384_formal": (
        FORMAL / "400-PPC4161-transition-parent-center-functional-proof-or-real-profile-import.md",
        "PPC4161_TRANSITION_PARENT_CENTER_FUNCTIONAL_PROOF_OR_REAL_PROFILE_IMPORT_4384",
        "4384 handoff: B_top is the live first-moment residual.",
    ),
    "SRC4385_01_4384_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4384_NEXT_TARGET.csv",
        "4385-Y5-R2FR-transition-topological-first-moment-zero-proof-or-real-profile-import.md",
        "Explicit 4385 target.",
    ),
    "SRC4385_02_4384_proof": (
        SOURCE_DIR / "P8_Y5_R2FR_4384_PARENT_CENTER_FUNCTIONAL_PROOF.csv",
        "CFP4384_2_first_moment_equivalence",
        "Exact equivalence c_top-c_H=B_top with equal monopoles.",
    ),
    "SRC4385_03_4384_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4384_FIRST_MOMENT_RESIDUAL.csv",
        "FMR4384_0_vector_first_moment",
        "Residual row to close or source.",
    ),
    "SRC4385_04_4377_moment_gate": (
        FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md",
        "MOM4377_2_dipole",
        "Older full moment gate; 4385 narrows the center branch to affine tests.",
    ),
    "SRC4385_05_4381_laplacian": (
        FORMAL / "397-PPC4161-transition-topological-defect-normal-form-or-profile-quadrature-runner.md",
        "NF4381_2_laplacian_boundary_silent",
        "Laplacian boundary-silent route specialized to affine tests.",
    ),
    "SRC4385_06_4382_center_zero": (
        FORMAL / "398-PPC4161-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md",
        "COT4382_2_center_lock_zero",
        "Center-lock zero kills the separated-center envelope.",
    ),
    "SRC4385_07_4383_formal": (
        FORMAL / "399-PPC4161-transition-parent-center-lock-or-first-real-profile-input-pack.md",
        "PPC4161_TRANSITION_PARENT_CENTER_LOCK_OR_FIRST_REAL_PROFILE_INPUT_PACK_4383",
        "Center-lock contract and smoke input pack.",
    ),
    "SRC4385_08_4383_smoke": (
        SMOKE_INPUT_PATH,
        "SMOKE4383_shifted_centers",
        "Synthetic smoke profile used to verify affine gate detects shifts.",
    ),
    "SRC4385_09_helper": (
        HELPER_PATH,
        "def affine_first_moment_rows",
        "Reusable affine first-moment runner added in 4385.",
    ),
    "SRC4385_10_validator": (
        SCRIPT_DIR / "topological_profile_import_validator.py",
        "def validate_import",
        "Existing validator remains the real-profile provenance gate.",
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


def affine_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "AF4385_0_affine_test_space_reduction",
            "statement": "For the center-offset branch, full profile equality is stronger than needed. If delta rho_top annihilates the affine test space span{1,y^1,y^2,y^3}, then Delta_M=0 and B_top=0.",
            "derivation": "B_top^i=M_H^{-1}<y^i,delta rho_top>. The constant test gives equal monopole. The three coordinate tests give the vector first moment. Therefore affine annihilation is exactly the center-lock condition.",
            "effect": "Narrows the next proof target from all compact test functions to four affine tests for the separated-center branch.",
            "status": "EXACT_THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AF4385_1_inversion_even_zero_monopole",
            "statement": "If delta rho_top(c+z)=delta rho_top(c-z) on a parent center c and int delta rho_top dV=0, then B_top=0 about c.",
            "derivation": "Write y=c+z. The c term is killed by the zero monopole and int z delta rho_top(z)dV=0 by oddness of z times an inversion-even density.",
            "effect": "Gives a symmetry route weaker than full radiality: parity-even zero-monopole defects are center-safe.",
            "status": "EXACT_SUFFICIENT_CONDITION_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AF4385_2_radial_zero_monopole",
            "statement": "If delta rho_top=F(|y-c_H|) and int delta rho_top dV=0, then B_top=0.",
            "derivation": "The radial case is inversion-even. Equivalently, angular integration kills int r n_i F(r)dOmega and the zero monopole kills the c_H term.",
            "effect": "Recovers the 4381 radial shell theorem as a direct first-moment zero proof.",
            "status": "EXACT_SUFFICIENT_CONDITION_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AF4385_3_laplacian_linear_boundary_silence",
            "statement": "If delta rho_top=Delta u_top and the Green boundary pairings vanish for 1,y^1,y^2,y^3, then Delta_M=0 and B_top=0.",
            "derivation": "Green identity gives <phi,Delta u>=boundary(phi,u) because Delta 1=Delta y^i=0. Zero boundary pairings for the affine tests kill the monopole and vector first moment.",
            "effect": "Specializes the harmonic-null route to the minimal center-offset contract.",
            "status": "EXACT_SUFFICIENT_CONDITION_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AF4385_4_exact_divergence_rejection",
            "statement": "A generic exact divergence delta rho_top=div V does not by itself imply B_top=0.",
            "derivation": "<y^i,div V>=int_boundary y^i V.n dS - int_W V^i dV. This can be nonzero even when the total divergence charge is boundary-controlled.",
            "effect": "Prevents smuggling first-moment silence from closed/exact/topological language alone.",
            "status": "COUNTERPROOF_GENERIC_DIVERGENCE_INSUFFICIENT",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AF4385_5_parent_affine_annihilator_contract",
            "statement": "The exact parent contract for this branch is D_top-H in Ann(Aff_1(W_H)), where D_top-H acts on test functions by <f,rho_top-rho_H>.",
            "derivation": "Ann(Aff_1) is precisely the kernel of the monopole plus center first-moment readout. It is finite-dimensional and does not require proving rho_top=rho_H as distributions.",
            "effect": "Next derivation target becomes a parent-owned affine-annihilator signature or a real profile row, not all-profile equality.",
            "status": "CONTRACT_EXACT_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": "False",
        },
    ]


def boundary_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "contract_id": "BC4385_0_constant",
            "test_function": "phi=1",
            "boundary_formula": "<1,Delta u_top>=int_boundary partial_n u_top dS",
            "zero_requirement": "int_boundary partial_n u_top dS=0",
            "kills": "Delta_M_top_H",
            "status": "FORMULA_EXACT_PARENT_BOUNDARY_INPUT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "BC4385_1_x",
            "test_function": "phi=x",
            "boundary_formula": "<x,Delta u_top>=int_boundary (x partial_n u_top - u_top n_x)dS",
            "zero_requirement": "int_boundary (x partial_n u_top - u_top n_x)dS=0",
            "kills": "B_top_x",
            "status": "FORMULA_EXACT_PARENT_BOUNDARY_INPUT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "BC4385_2_y",
            "test_function": "phi=y",
            "boundary_formula": "<y,Delta u_top>=int_boundary (y partial_n u_top - u_top n_y)dS",
            "zero_requirement": "int_boundary (y partial_n u_top - u_top n_y)dS=0",
            "kills": "B_top_y",
            "status": "FORMULA_EXACT_PARENT_BOUNDARY_INPUT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "BC4385_3_z",
            "test_function": "phi=z",
            "boundary_formula": "<z,Delta u_top>=int_boundary (z partial_n u_top - u_top n_z)dS",
            "zero_requirement": "int_boundary (z partial_n u_top - u_top n_z)dS=0",
            "kills": "B_top_z",
            "status": "FORMULA_EXACT_PARENT_BOUNDARY_INPUT_MISSING",
            "valid_for_claim": "False",
        },
    ]


def acceptance_rows(smoke_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    by_id = {row["profile_id"]: row for row in smoke_rows}
    locked = by_id["SMOKE4383_center_locked"]
    shifted = by_id["SMOKE4383_shifted_centers"]
    shifted_b_over_r = float(shifted["B_top_norm_over_R"])
    return [
        {
            "accept_id": "ASM4385_0_center_locked_zero",
            "tested_output": "SMOKE4383_center_locked",
            "value": locked["B_top_norm_over_R"],
            "threshold": "1e-12",
            "passed": str(locked["monopole_zero"] == "True" and locked["linear_affine_zero"] == "True"),
            "interpretation": "identical center-locked profiles have zero affine residual",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "ASM4385_1_shifted_detected",
            "tested_output": "SMOKE4383_shifted_centers",
            "value": shifted["B_top_norm_over_R"],
            "threshold": "> 1e-3",
            "passed": str(shifted["monopole_zero"] == "True" and shifted["linear_affine_zero"] == "False" and shifted_b_over_r > 1.0e-3),
            "interpretation": "equal-monopole shifted profiles have finite B_top/R",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "ASM4385_2_smoke_nonclaim",
            "tested_output": "all smoke rows",
            "value": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in smoke_rows)),
            "threshold": "True",
            "passed": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in smoke_rows)),
            "interpretation": "synthetic rows remain nonclaim even when numerically scoreable",
            "valid_for_claim": "False",
        },
    ]


def route_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "route_id": "RG4385_0_affine_annihilator",
            "route": "Parent proves D_top-H annihilates Aff_1(W_H)",
            "what_it_closes": "Delta_M=0 and B_top=0, hence separated-center envelope branch",
            "current_status": "EXACT_CONTRACT_PARENT_SIGNATURE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "RG4385_1_symmetry",
            "route": "Parent proves inversion-even or radial zero-monopole defect about c_H",
            "what_it_closes": "B_top=0 by parity/angular cancellation",
            "current_status": "EXACT_THEOREM_PARENT_SYMMETRY_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "RG4385_2_laplacian_boundary",
            "route": "Parent proves Laplacian representative with silent affine boundary pairings",
            "what_it_closes": "Delta_M=0 and B_top=0 through Green identity",
            "current_status": "EXACT_THEOREM_BOUNDARY_INPUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "RG4385_3_real_profile",
            "route": "Import source-backed rho_H/rho_top profile and compute affine residual",
            "what_it_closes": "empirical/profile value for B_top/R if input is real and validator-clean",
            "current_status": "RUNNER_READY_REAL_PROFILE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4385_0_affine_theorem",
            "claim_tested": "B_top=0 follows from affine test-space annihilation",
            "required_inputs": "D_top-H annihilates span{1,x,y,z} as a parent-signed density operator",
            "status": "THEOREM_EXACT_PARENT_SIGNATURE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4385_1_boundary_route",
            "claim_tested": "Laplacian topological residual has silent affine boundary pairings",
            "required_inputs": "delta rho_top=Delta u_top plus four boundary integral zeros",
            "status": "BOUNDARY_CONTRACT_EXACT_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4385_2_real_profile",
            "claim_tested": "real profile rows compute B_top/R=0",
            "required_inputs": "validator-clean real rho_H/rho_top source profile with input_valid_for_claim=true",
            "status": "RUNNER_READY_REAL_PROFILE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4385_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "affine branch plus higher topological/rest/readout/local-projection gates closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4385_0",
            "decision": DECISION,
            "summary": (
                "4385 proves the minimal first-moment law for the separated-center branch. Full distributional profile equality is not required to kill b; it is enough for the residual density operator D_top-H to annihilate the four-dimensional affine test space {1,x,y,z}. "
                "Radial or inversion-even zero-monopole defects are exact sufficient conditions, and the Laplacian route only needs Green boundary silence for the same affine tests. A generic exact divergence is rejected as insufficient. "
                "The parent signature remains unsigned, so 4385 adds an affine first-moment runner that computes Delta_M, B_top and B_top/R from profile rows and verifies the existing smoke profiles: locked rows give zero, shifted equal-monopole rows are detected."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The least-circular next move is to parent-sign the affine annihilator or feed one real profile row through the validator and affine runner.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4385_0_theorem",
            "object": "B_top",
            "status": "MINIMAL_AFFINE_ZERO_LAW_DERIVED",
            "note": "B_top=0 is exactly the three linear affine tests once the monopole is matched.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4385_1_parent",
            "object": "D_top-H parent signature",
            "status": "UNSIGNED",
            "note": "Need parent action/readout proof that D_top-H annihilates Aff_1(W_H), or real profile rows.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4385_2_runner",
            "object": "topological_affine_first_moment_gate.py",
            "status": "BUILT_AND_SMOKE_TESTED",
            "note": "Computes Delta_M, B_top vector and B_top/R from sampled profile rows.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4385_3_next",
            "object": "next target",
            "status": "AFFINE_PARENT_SIGNATURE_OR_REAL_ROW_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4385_0",
            "target": NEXT_TARGET,
            "question": "Can the parent action sign D_top-H in Ann(Aff_1(W_H)), or can a first real rho_H/rho_top profile row be imported?",
            "preferred_route": "derive the affine annihilator from parent translation/no-marker/source-center symmetry or Laplacian affine boundary silence.",
            "fallback_route": "import one real source-backed profile through the validator, then compute Delta_M and B_top/R with topological_affine_first_moment_gate.py.",
            "avoid": "requiring full profile equality when only center lock is being tested; or claiming from total charge, generic exact divergence, synthetic smoke, or post-readout recentering.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    boundary: List[Dict[str, str]],
    smoke: List[Dict[str, str]],
    acceptance: List[Dict[str, str]],
    routes: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: topological first-moment zero proof or real profile import

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4385 makes the center branch smaller and sharper.

4384 reduced the obstruction to:

```text
B_top^i := M_H^-1 int_W y^i (rho_top-rho_H)dV.
```

4385 proves that full profile equality is overkill for this branch. Define the residual distribution:

```text
D_top-H[f] := int_W f(y)(rho_top-rho_H)(y)dV.
```

Then the center-offset branch closes exactly if:

```text
D_top-H[1] = 0,
D_top-H[x] = D_top-H[y] = D_top-H[z] = 0.
```

So the proof target is now finite:

```text
D_top-H in Ann(Aff_1(W_H)).
```

That is the clean leap forward: not all-profile equality, not vibes, not total charge. A four-test affine annihilator kills `B_top`.

4385 also builds `topological_affine_first_moment_gate.py` so real profile rows can be scored directly for `Delta_M`, `B_top`, and `B_top/R`.

No physical local-GR/Newton/PPN/clock/orbital claim fires because the parent affine-annihilator signature is not signed and the only scored profile rows here are synthetic smoke rows.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Affine First-Moment Theorems

{md_table(theorems, ["theorem_id", "statement", "derivation", "effect", "status"])}

## Laplacian Boundary Contract

{md_table(boundary, ["contract_id", "test_function", "boundary_formula", "zero_requirement", "kills", "status"])}

## Affine Smoke Output

{md_table(smoke, ["profile_id", "M_H", "M_top", "Delta_M_top_H", "B_top_x", "B_top_norm_over_R", "monopole_zero", "linear_affine_zero", "valid_for_claim", "current_status"])}

## Smoke Acceptance

{md_table(acceptance, ["accept_id", "tested_output", "value", "threshold", "passed", "interpretation"])}

## Route Gates

{md_table(routes, ["route_id", "route", "what_it_closes", "current_status", "claim_allowed"])}

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
    text = f"""# 4385: topological first-moment zero proof or real profile import

Marker: `{MARKER}`

## What changed

- Derived the finite affine condition for `B_top=0`: annihilate `1,x,y,z`.
- Proved radial/inversion-even zero-monopole and affine Laplacian-boundary routes.
- Rejected generic exact divergence as insufficient for first-moment silence.
- Added `topological_affine_first_moment_gate.py` and smoke-tested it on locked vs shifted profiles.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4385 Transition topological first-moment zero proof or real profile import

Marker: `{MARKER}`

4385 narrows the center-offset branch from full topological/Hilbert profile equality to a finite affine annihilator. With `D_top-H[f]=int_W f(rho_top-rho_H)dV`, the branch only requires:

```text
D_top-H[1]=0,
D_top-H[x]=D_top-H[y]=D_top-H[z]=0.
```

This is exactly `D_top-H in Ann(Aff_1(W_H))` and it gives `B_top=0`. Radial or inversion-even zero-monopole defects and Laplacian residuals with silent affine boundary pairings are exact sufficient conditions. A generic exact divergence is not sufficient. The parent affine signature is still unsigned, and real profile rows remain missing.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4385 packet update: affine first-moment branch

Marker: `{PACKET_MARKER}`

Packet update: the topological center-offset branch now has a finite parent contract. Instead of full profile equality, require the residual density operator `D_top-H` to annihilate the affine test space `Aff_1(W_H)=span{{1,x,y,z}}`. This kills the monopole and `B_top` exactly. Claim remains blocked until this affine-annihilator signature is parent-signed or a real validator-clean profile row computes `B_top/R`.
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
                "4385 derives the minimal affine first-moment law for the topological center branch. Full distributional profile equality is stronger than needed to kill the separated-center residual: if D_top-H[f]=int f(rho_top-rho_H)dV annihilates the affine test space span{1,x,y,z}, then Delta_M=0 and B_top=0. "
                "Radial or inversion-even zero-monopole defects are exact sufficient conditions, and a Laplacian residual only needs Green boundary silence for the same affine tests. A generic exact divergence is explicitly rejected as insufficient. "
                "A reusable affine first-moment runner now computes Delta_M, B_top and B_top/R from profile rows; smoke tests detect shifted equal-monopole profiles while keeping all rows nonclaim. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4385 source register, affine theorem rows, boundary contract, affine smoke output, smoke acceptance, route gates, claim gates, decision, status, next target and validation CSV.",
            "affine_first_moment_theorem_parent_signature_unsigned_runner_nonclaim",
            "Parent-sign D_top-H in Ann(Aff_1(W_H)) or import a real validator-clean rho_H/rho_top profile row.",
            "Claiming from total charge, generic exact divergence, synthetic smoke, post-readout recentering, or full-profile equality when only center lock is tested.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4385_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4385_AFFINE_THEOREMS.csv")
    boundary = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4385_BOUNDARY_CONTRACT.csv")
    smoke = read_csv(AFFINE_SMOKE_PATH)
    acceptance = read_csv(AFFINE_ACCEPTANCE_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4385_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4385_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4385_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4385_2_affine_theorem",
        any(row["theorem_id"] == "AF4385_0_affine_test_space_reduction" and row["status"] == "EXACT_THEOREM_DERIVED_NOT_PARENT_SIGNED" for row in theorems),
        "affine test-space reduction recorded",
    )
    add(
        "VAL4385_3_boundary_contract",
        len(boundary) == 4 and {row["test_function"] for row in boundary} == {"phi=1", "phi=x", "phi=y", "phi=z"},
        "four affine Laplacian boundary contracts recorded",
    )
    add(
        "VAL4385_4_divergence_rejected",
        any(row["theorem_id"] == "AF4385_4_exact_divergence_rejection" for row in theorems),
        "generic divergence shortcut rejected",
    )
    add(
        "VAL4385_5_smoke_detects_shift",
        any(row["profile_id"] == "SMOKE4383_center_locked" and row["linear_affine_zero"] == "True" for row in smoke)
        and any(row["profile_id"] == "SMOKE4383_shifted_centers" and row["linear_affine_zero"] == "False" for row in smoke),
        "affine runner distinguishes locked and shifted smoke profiles",
    )
    add("VAL4385_6_acceptance_passed", all(row["passed"] == "True" for row in acceptance), "all smoke acceptance checks passed")
    add("VAL4385_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4385_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4385_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4385_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4385_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4385_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4385_13_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4385_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4385_15_helper_script", HELPER_PATH.exists() and "def affine_first_moment_rows" in read_text(HELPER_PATH), "affine helper exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = affine_theorem_rows()
    boundary = boundary_contract_rows()
    smoke = affine_first_moment_rows(SMOKE_INPUT_PATH, 1.0e-12)
    write_csv(AFFINE_SMOKE_PATH, smoke)
    acceptance = acceptance_rows(smoke)
    write_csv(AFFINE_ACCEPTANCE_PATH, acceptance)
    routes = route_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4385_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4385_AFFINE_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4385_BOUNDARY_CONTRACT.csv": boundary,
        "P8_Y5_R2FR_4385_ROUTE_GATES.csv": routes,
        "P8_Y5_R2FR_4385_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4385_DECISION.csv": decisions,
        "P8_Y5_R2FR_4385_STATUS.csv": statuses,
        "P8_Y5_R2FR_4385_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [AFFINE_SMOKE_PATH, AFFINE_ACCEPTANCE_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorems, boundary, smoke, acceptance, routes, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
