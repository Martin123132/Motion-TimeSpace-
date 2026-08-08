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

from topological_profile_import_validator import validate_import, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PARENT_DIR = POST / "source-intake" / "parent-action"

CHECKPOINT = "4384"
CLAIM_ID = "L-225"
MARKER = "PPC4161_TRANSITION_PARENT_CENTER_FUNCTIONAL_PROOF_OR_REAL_PROFILE_IMPORT_4384"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PARENT_CENTER_FUNCTIONAL_PROOF_OR_REAL_PROFILE_IMPORT_4384"
DECISION = "HILBERT_CENTER_PARENT_OWNED_CONDITIONALLY_TOPOLOGICAL_FIRST_MOMENT_REMAINS_OPEN_IMPORT_VALIDATOR_BUILT_NONCLAIM"
NEXT_TARGET = "4385-Y5-R2FR-transition-topological-first-moment-zero-proof-or-real-profile-import.md"

FORMAL_PATH = FORMAL / "400-PPC4161-transition-parent-center-functional-proof-or-real-profile-import.md"
DOC_PATH = POST / "4384-Y5-R2FR-transition-parent-center-functional-proof-or-real-profile-import.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4384_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
VALIDATOR_PATH = SCRIPT_DIR / "topological_profile_import_validator.py"
SMOKE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4383_CENTER_LOCK_SMOKE_INPUT.csv"
SMOKE_VALIDATION_PATH = SOURCE_DIR / "P8_Y5_R2FR_4384_PROFILE_IMPORT_VALIDATION_SMOKE.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4384_00_4383_formal": (
        FORMAL / "399-PPC4161-transition-parent-center-lock-or-first-real-profile-input-pack.md",
        "PPC4161_TRANSITION_PARENT_CENTER_LOCK_OR_FIRST_REAL_PROFILE_INPUT_PACK_4383",
        "4383 handoff: center-lock contract and input runner.",
    ),
    "SRC4384_01_4383_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4383_NEXT_TARGET.csv",
        "4384-Y5-R2FR-transition-parent-center-functional-proof-or-real-profile-import.md",
        "Explicit 4384 target.",
    ),
    "SRC4384_02_4383_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4383_PARENT_CENTER_LOCK_THEOREM.csv",
        "PCL4383_1_factorization_lock",
        "Center-lock theorem to sharpen.",
    ),
    "SRC4384_03_4383_runner": (
        SCRIPT_DIR / "topological_center_lock_input_runner.py",
        "def envelope_score_rows",
        "Center-lock input runner remains fallback.",
    ),
    "SRC4384_04_186_hamiltonian": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "It is the Hamiltonian/Hilbert charge map of the same source current and same worldtube.",
        "Parent-owned Hilbert source/worldtube chain.",
    ),
    "SRC4384_05_187_newton": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV = M_H^dress[W_H;tau].",
        "Hilbert density mass normalization.",
    ),
    "SRC4384_06_4377_moment_gate": (
        FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md",
        "M_1m^top-H := int_W delta rho_top r Y_1m dV_H",
        "Existing dipole/first-moment gate.",
    ),
    "SRC4384_07_3037_lock": (
        PARENT_DIR / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
        "MSRL3037_6_verdict",
        "Source-readout lock remains unsigned.",
    ),
    "SRC4384_08_3055_descent": (
        PARENT_DIR / "Hilbert_source_descent_theorem_attempt_3055_NOT_SIGNED.csv",
        "HSD3055_5_verdict",
        "Hilbert source descent remains unsigned.",
    ),
    "SRC4384_09_validator": (
        VALIDATOR_PATH,
        "def validate_import",
        "Real-profile import validator added in 4384.",
    ),
    "SRC4384_10_smoke_input": (
        SMOKE_INPUT_PATH,
        "SYNTHETIC_SMOKE_NOT_PHYSICAL",
        "Smoke input must be rejected by real import validator.",
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


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


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


def center_functional_rows() -> List[Dict[str, str]]:
    return [
        {
            "proof_id": "CFP4384_0_parent_Hilbert_center",
            "object": "Hilbert center c_H",
            "statement": "On a fixed parent worldtube W_H with positive M_H, c_H^i := M_H^{-1} int_W y^i rho_H dV is owned by the Hamiltonian/Hilbert source current before orbital readout.",
            "evidence_or_derivation": "186 fixes W_H and the Hamiltonian/Hilbert charge map from J_H_total; 187 fixes int_W rho_H dV=M_H^dress. Therefore the Hilbert first moment is a parent-source functional when the private packet clauses are adopted.",
            "status": "CONDITIONAL_PARENT_HILBERT_CENTER_OWNED",
            "remaining_blocker": "private packet adoption/global parent source descent still not a public local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CFP4384_1_topological_center_not_owned",
            "object": "topological center c_top",
            "statement": "c_top is parent-owned only if rho_top is a parent density representative on the same W_H before readout, not a post-readout/topological mask.",
            "evidence_or_derivation": "4377 keeps topological/rest profile equality and all moment gates open; 3037/3055 keep source-readout descent unsigned.",
            "status": "NOT_PARENT_SIGNED",
            "remaining_blocker": "MISSING_TOPOLOGICAL_PROFILE_DENSITY_OWNER",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CFP4384_2_first_moment_equivalence",
            "object": "center offset b",
            "statement": "If int_W(rho_top-rho_H)dV=0 and M_H>0, then c_top-c_H = M_H^{-1} int_W y(rho_top-rho_H)dV. Thus b=0 iff the vector first moment of delta rho_top vanishes.",
            "evidence_or_derivation": "Subtract the definitions of c_top and c_H using equal monopoles. This is exact and does not require full profile equality.",
            "status": "EXACT_THEOREM_DERIVED",
            "remaining_blocker": "MISSING_FIRST_MOMENT_ZERO_OR_REAL_PROFILE_INPUT",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CFP4384_3_scope_guard",
            "object": "what center lock does not prove",
            "statement": "b=0 closes only the separated-center dipole-envelope branch; it does not prove full rho_top=rho_H or kill quadrupole/higher anisotropic moments.",
            "evidence_or_derivation": "A centered zero-monopole distribution can still carry l>=2 moments unless radial/Laplacian/distributional equality clauses also hold.",
            "status": "FIREWALL_DERIVED",
            "remaining_blocker": "higher profile moments remain under 4378/4381 gates",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CFP4384_4_current_verdict",
            "object": "4384 proof status",
            "statement": "The Hilbert center is conditionally parent-owned; the topological center and first moment are the live missing payload.",
            "evidence_or_derivation": "Current corpus supports same-source Hamiltonian/Hilbert charge, but not topological profile-density ownership.",
            "status": "PARTIAL_PROOF_ADVANCE_NONCLAIM",
            "remaining_blocker": "prove first-moment zero or import real profile rows",
            "valid_for_claim": "False",
        },
    ]


def first_moment_residual_rows() -> List[Dict[str, str]]:
    return [
        {
            "residual_id": "FMR4384_0_vector_first_moment",
            "quantity": "B_top^i := M_H^{-1} int_W y^i (rho_top-rho_H)dV",
            "meaning": "center-offset vector c_top-c_H when monopoles match",
            "zero_route": "parent topological density shares Hilbert first moment; or delta rho_top is radial/Laplacian-null with silent boundary",
            "source_route": "compute from real rho_H/rho_top profile CSV using topological_center_lock_input_runner.py",
            "status": "FORMULA_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "FMR4384_1_center_offset_norm",
            "quantity": "b/R = ||B_top||/R",
            "meaning": "dimensionless offset used by 4382 envelope rows",
            "zero_route": "B_top=0",
            "source_route": "real profile import with positive M_H and parent-owned R",
            "status": "FORMULA_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "FMR4384_2_dipole_gate",
            "quantity": "|delta a_1|/|a_N| <= geometry_factor * 4 sqrt(pi) * ||B_top||/R",
            "meaning": "dipole branch score after first-moment residual is known",
            "zero_route": "B_top=0",
            "source_route": "4382 envelope rows plus imported b/R",
            "status": "SCORE_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def import_schema_rows() -> List[Dict[str, str]]:
    return [
        {
            "field": "profile_id",
            "required": "True",
            "units": "text",
            "purpose": "group samples for one source-profile comparison",
            "claim_rule": "must not be synthetic/smoke/surrogate",
        },
        {
            "field": "x,y,z,volume_weight",
            "required": "True",
            "units": "declared length and volume convention",
            "purpose": "compute first moments and direct multipoles",
            "claim_rule": "numeric, positive volume weights, fixed W_H",
        },
        {
            "field": "rho_H,rho_top",
            "required": "True",
            "units": "mass density or signed mass per sample if volume_weight=1",
            "purpose": "Hilbert/topological profile comparison",
            "claim_rule": "real source provenance for both density representatives",
        },
        {
            "field": "R,source_profile_path,input_valid_for_claim",
            "required": "True",
            "units": "length, path, boolean",
            "purpose": "normalization radius and provenance gate",
            "claim_rule": "R>0, paths declared, input_valid_for_claim true and no forbidden markers",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4384_0_Hilbert_center",
            "claim_tested": "Hilbert center is parent-owned in the private local packet",
            "required_inputs": "186/187 private packet clauses, fixed W_H, positive M_H",
            "status": "CONDITIONAL_PRIVATE_PACKET_READY_NOT_GLOBAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4384_1_topological_first_moment",
            "claim_tested": "b=0 / B_top=0 for topological profile branch",
            "required_inputs": "topological profile-density owner plus first-moment zero theorem, or real profile value b/R=0",
            "status": "BLOCKED_FIRST_MOMENT_ZERO_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4384_2_real_import",
            "claim_tested": "real profile import can be scored",
            "required_inputs": "validator valid_for_claim=true and source-backed profile rows",
            "status": "VALIDATOR_READY_REAL_INPUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4384_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "center/profile branch plus remaining source-shadow/readout/boundary/non-Hilbert residuals closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4384_0",
            "decision": DECISION,
            "summary": (
                "4384 partially proves the parent-center route: the Hilbert center c_H is conditionally parent-owned by the existing Hamiltonian/Hilbert worldtube chain, but the topological center is not signed. "
                "The remaining obstruction is sharpened to an exact first-moment residual B_top=M_H^{-1} int y(rho_top-rho_H)dV. With equal monopoles, b=||B_top||, so b=0 is equivalent to vector first-moment silence, not full profile equality. "
                "4384 also adds a real-profile import validator that rejects synthetic/smoke/placeholder inputs before the center-lock and quadrature runners can be promoted."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The next least-circular route is now first-moment zero: prove B_top=0 from topological density ownership or import a real profile.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4384_0_Hilbert_center",
            "object": "c_H",
            "status": "CONDITIONALLY_PARENT_OWNED",
            "note": "private Hamiltonian/Hilbert worldtube chain owns the Hilbert first moment if packet clauses are adopted.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4384_1_topological_center",
            "object": "c_top/B_top",
            "status": "OPEN",
            "note": "topological density representative and vector first moment remain unsigned.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4384_2_import",
            "object": "real profile import",
            "status": "VALIDATOR_BUILT_SMOKE_REJECTED",
            "note": "synthetic smoke rows are rejected as claim inputs; real profile rows still missing.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4384_3_next",
            "object": "next target",
            "status": "FIRST_MOMENT_ZERO_OR_PROFILE_IMPORT_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4384_0",
            "target": NEXT_TARGET,
            "question": "Can B_top=M_H^{-1} int y(rho_top-rho_H)dV be proved zero, or can real profile rows be imported?",
            "preferred_route": "derive topological first-moment silence from parent profile-density ownership, radial/Laplacian representative, or boundary first-moment cancellation.",
            "fallback_route": "validate/import real rho_H/rho_top profile rows, then run center-lock and profile-quadrature runners.",
            "avoid": "using synthetic smoke, total charge, post-readout centering, metric-nullity or same-worldtube charge as first-moment proof.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    center_rows: List[Dict[str, str]],
    residuals: List[Dict[str, str]],
    schema: List[Dict[str, str]],
    import_validation: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: parent center functional proof or real profile import

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4384 makes a real proof-side refinement:

```text
c_H^i := M_H^{-1} int_W y^i rho_H dV
```

is conditionally parent-owned by the existing Hamiltonian/Hilbert source chain in the private packet: `W_H`, `J_H_total`, `M_H^dress`, and `rho_H` are all fixed before orbital readout if the packet clauses are adopted.

The topological side is still not signed. But the obstruction is now exact:

```text
B_top^i := M_H^{-1} int_W y^i (rho_top-rho_H)dV,
c_top-c_H = B_top  when int_W(rho_top-rho_H)dV = 0.
```

So the next proof is not "make centers the same" in words. It is:

```text
B_top = 0
```

from a parent topological density owner, radial/Laplacian representative, or first-moment boundary cancellation. This closes the center-offset branch without claiming full profile equality.

4384 also adds a real-profile import validator. Synthetic smoke rows are rejected as claim inputs.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Parent Center Functional Proof

{md_table(center_rows, ["proof_id", "object", "statement", "evidence_or_derivation", "status", "remaining_blocker"])}

## First-Moment Residual

{md_table(residuals, ["residual_id", "quantity", "meaning", "zero_route", "source_route", "status"])}

## Real Profile Import Schema

{md_table(schema, ["field", "required", "units", "purpose", "claim_rule"])}

## Import Validator Smoke Result

{md_table(import_validation, ["profile_id", "row_count", "positive_masses", "source_paths_declared", "no_forbidden_markers", "input_valid_flags_true", "valid_for_scoring", "valid_for_claim", "claim_allowed"])}

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
    text = f"""# 4384: parent center functional proof or real profile import

Marker: `{MARKER}`

## What changed

- Proved the Hilbert center is conditionally parent-owned by the Hamiltonian/Hilbert source chain.
- Reduced the remaining topological center obstruction to the exact first-moment residual `B_top`.
- Added `topological_profile_import_validator.py` for real profile imports.
- Confirmed synthetic smoke rows are rejected as claim inputs.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4384 Transition parent center functional proof or real profile import

Marker: `{MARKER}`

4384 partially closes the center-functional route. The Hilbert center `c_H=M_H^{-1} int y rho_H dV` is conditionally parent-owned by the Hamiltonian/Hilbert worldtube chain when the private packet clauses are adopted. The topological center is not signed.

The live obstruction is now the first-moment residual:

```text
B_top := M_H^{-1} int_W y (rho_top-rho_H)dV.
```

With equal monopoles, `c_top-c_H=B_top`, so center lock is exactly `B_top=0`. This is weaker than full profile equality but strong enough to kill the separated-center envelope branch. A real-profile import validator was added and rejects synthetic/smoke rows.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4384 packet update: center lock reduced to first moment

Marker: `{PACKET_MARKER}`

Packet update: the Hilbert center is conditionally parent-owned by the Hamiltonian/Hilbert source chain. The topological branch is reduced to `B_top=M_H^{-1} int y(rho_top-rho_H)dV`. Proving `B_top=0` closes the separated-center envelope without requiring full profile equality; real profile rows must pass `topological_profile_import_validator.py` before scoring.
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
                "4384 partially proves the parent-center route: the Hilbert center c_H=M_H^{-1} int y rho_H dV is conditionally parent-owned by the Hamiltonian/Hilbert worldtube chain in the private packet. "
                "The topological center is not signed, but the remaining obstruction is sharpened to the exact first-moment residual B_top=M_H^{-1} int y(rho_top-rho_H)dV; with equal monopoles, c_top-c_H=B_top. "
                "Thus b=0 is equivalent to vector first-moment silence, weaker than full profile equality but enough to close the separated-center branch. A real-profile import validator is added and synthetic smoke rows are rejected. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4384 source register, parent center functional proof rows, first-moment residual rows, real profile import schema, validator smoke output, claim gates, decision, status, next target and validation CSV.",
            "Hilbert_center_parent_owned_conditionally_topological_first_moment_open_import_validator_nonclaim",
            "Prove B_top=0 or import real rho_H/rho_top profile rows through the validator and runners.",
            "Using synthetic smoke, total charge, post-readout centering, metric-nullity or same-worldtube charge as first-moment proof.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4384_SOURCE_REGISTER.csv")
    center = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4384_PARENT_CENTER_FUNCTIONAL_PROOF.csv")
    residuals = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4384_FIRST_MOMENT_RESIDUAL.csv")
    import_validation = read_csv(SMOKE_VALIDATION_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4384_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4384_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4384_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4384_2_Hilbert_center_partial",
        any(row["proof_id"] == "CFP4384_0_parent_Hilbert_center" and row["status"] == "CONDITIONAL_PARENT_HILBERT_CENTER_OWNED" for row in center),
        "Hilbert center partial proof recorded",
    )
    add(
        "VAL4384_3_first_moment_equivalence",
        any(row["proof_id"] == "CFP4384_2_first_moment_equivalence" and row["status"] == "EXACT_THEOREM_DERIVED" for row in center)
        and any(row["residual_id"] == "FMR4384_0_vector_first_moment" for row in residuals),
        "first-moment equivalence and residual rows recorded",
    )
    add(
        "VAL4384_4_validator_rejects_smoke",
        len(import_validation) >= 1
        and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in import_validation)
        and any(row["no_forbidden_markers"] == "False" for row in import_validation),
        "validator rejects synthetic smoke rows as claim inputs",
    )
    add("VAL4384_5_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4384_6_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4384_7_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4384_8_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4384_9_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4384_10_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4384_11_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4384_12_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4384_13_validator_script_exists", VALIDATOR_PATH.exists() and "def validate_import" in read_text(VALIDATOR_PATH), "validator script exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    center_rows = center_functional_rows()
    residuals = first_moment_residual_rows()
    schema = import_schema_rows()
    import_validation = validate_import(SMOKE_INPUT_PATH)
    write_csv(SMOKE_VALIDATION_PATH, import_validation)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4384_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4384_PARENT_CENTER_FUNCTIONAL_PROOF.csv": center_rows,
        "P8_Y5_R2FR_4384_FIRST_MOMENT_RESIDUAL.csv": residuals,
        "P8_Y5_R2FR_4384_REAL_PROFILE_IMPORT_SCHEMA.csv": schema,
        "P8_Y5_R2FR_4384_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4384_DECISION.csv": decisions,
        "P8_Y5_R2FR_4384_STATUS.csv": statuses,
        "P8_Y5_R2FR_4384_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [SMOKE_VALIDATION_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, center_rows, residuals, schema, import_validation, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
