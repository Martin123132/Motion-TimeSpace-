from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from topological_center_offset_envelope import center_offset_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PARENT_DIR = POST / "source-intake" / "parent-action"

CHECKPOINT = "4382"
CLAIM_ID = "L-223"
MARKER = "PPC4161_TRANSITION_TOPOLOGICAL_PROFILE_SOURCE_ACQUISITION_OR_PARENT_NORMAL_FORM_SIGNATURE_4382"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_TOPOLOGICAL_PROFILE_SOURCE_ACQUISITION_OR_PARENT_NORMAL_FORM_SIGNATURE_4382"
DECISION = "PARENT_NORMAL_FORM_UNSIGNED_PROFILE_SOURCE_MISSING_CENTER_OFFSET_ENVELOPE_DERIVED_NONCLAIM"
NEXT_TARGET = "4383-Y5-R2FR-transition-parent-center-lock-or-first-real-profile-input-pack.md"

FORMAL_PATH = FORMAL / "398-PPC4161-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md"
DOC_PATH = POST / "4382-Y5-R2FR-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4382_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
BOUNDS_PATH = SOURCE_DIR / "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv"
ENVELOPE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4382_CENTER_OFFSET_ENVELOPE_ROWS.csv"
RUNNER_PATH = SCRIPT_DIR / "topological_center_offset_envelope.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4382_00_4381_formal": (
        FORMAL / "397-PPC4161-transition-topological-defect-normal-form-or-profile-quadrature-runner.md",
        "PPC4161_TRANSITION_TOPOLOGICAL_DEFECT_NORMAL_FORM_OR_PROFILE_QUADRATURE_RUNNER_4381",
        "4381 handoff: normal-form theorem bundle and quadrature runner.",
    ),
    "SRC4382_01_4381_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4381_NEXT_TARGET.csv",
        "4382-Y5-R2FR-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md",
        "Explicit 4382 target.",
    ),
    "SRC4382_02_4381_normal": (
        SOURCE_DIR / "P8_Y5_R2FR_4381_NORMAL_FORM_THEOREMS.csv",
        "NF4381_3_separate_center_countermodel",
        "Separate-center dipole countermodel.",
    ),
    "SRC4382_03_4381_parent_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4381_PARENT_NORMAL_FORM_AUDIT.csv",
        "PNF4381_4_verdict",
        "Parent normal-form route remains unsigned.",
    ),
    "SRC4382_04_4381_runner": (
        SCRIPT_DIR / "profile_topological_moment_quadrature.py",
        "def compute_moment_rows",
        "Reusable profile quadrature runner.",
    ),
    "SRC4382_05_4381_smoke_output": (
        SOURCE_DIR / "P8_Y5_R2FR_4381_PROFILE_QUADRATURE_SMOKE_OUTPUT.csv",
        "SMOKE4381_shifted_equal_monopoles",
        "Executable evidence that separated centers create moments.",
    ),
    "SRC4382_06_4378_bounds": (
        BOUNDS_PATH,
        "TB4378_SUP4371_0_Sun_Mercury_average_dipole",
        "Topological multipole geometry score rows.",
    ),
    "SRC4382_07_4379_template": (
        SOURCE_DIR / "P8_Y5_R2FR_4379_NUMERIC_MOMENT_INPUT_TEMPLATE.csv",
        "MISSING_MOMENT_VALUE",
        "Current topological moment rows are still input templates.",
    ),
    "SRC4382_08_4380_sweep": (
        SOURCE_DIR / "P8_Y5_R2FR_4380_SOURCE_INTAKE_SWEEP.csv",
        "NO_VALID_TOPOLOGICAL_MOMENT_INPUT_FOUND",
        "No valid source-backed profile input found in 4380.",
    ),
    "SRC4382_09_3037_lock": (
        PARENT_DIR / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
        "MSRL3037_6_verdict",
        "Source-readout lock remains contract-only.",
    ),
    "SRC4382_10_3055_descent": (
        PARENT_DIR / "Hilbert_source_descent_theorem_attempt_3055_NOT_SIGNED.csv",
        "HSD3055_5_verdict",
        "Hilbert source descent remains unsigned.",
    ),
    "SRC4382_11_offset_runner": (
        RUNNER_PATH,
        "def center_offset_rows",
        "Center-offset envelope helper added in 4382.",
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


def normal_form_signature_attempt_rows() -> List[Dict[str, str]]:
    return [
        {
            "attempt_id": "NFS4382_0_direct_radial_defect",
            "target_signature": "delta rho_top=F(|y-c|) with zero monopole",
            "derivation_attempt": "Would follow if the raw topological/Hamiltonian profile defect has no parent vector/tensor/source-label/boundary orientation and its scalar representative is fixed by a single radius around the source collar.",
            "current_result": "NOT_DERIVED",
            "why_not_closed": "No current parent file proves that the raw defect representative is scalar-radial rather than a generic closed/topological density representative.",
            "next_needed": "parent field-list/source-center lock or explicit profile input",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NFS4382_1_common_center_isotropy",
            "target_signature": "rho_top and rho_H share same parent center/isotropy before subtraction",
            "derivation_attempt": "Would follow from a single source-readout lock where Hilbert and topological representatives are both functors of the same worldtube center and no post-readout recentering is allowed.",
            "current_result": "NOT_DERIVED",
            "why_not_closed": "3037 and 3055 keep the minimum source-readout lock and Hilbert descent unsigned.",
            "next_needed": "prove parent center functional c[W_H,J_H] is shared by topological and Hilbert densities",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NFS4382_2_laplacian_null",
            "target_signature": "delta rho_top=Delta u_top with Green boundary silence",
            "derivation_attempt": "Would follow from a parent boundary/cohomology Hodge representative whose compact scalar part is exact-Laplacian and has silent Green boundary term.",
            "current_result": "NOT_DERIVED",
            "why_not_closed": "4378 supplies the theorem but not the raw topological representative signature.",
            "next_needed": "derive Hodge/Laplacian representative or keep envelope/profile rows",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NFS4382_3_best_available_progress",
            "target_signature": "if normal form remains unsigned, bound the separate-center failure mode",
            "derivation_attempt": "Use shift multipole law for equal-monopole separated centers to bound b/R directly.",
            "current_result": "CENTER_OFFSET_ENVELOPE_DERIVED",
            "why_not_closed": "b/R and delta_N still need source/test values before claim promotion.",
            "next_needed": "source parent center-offset bound or observational/theory delta_N for each arena",
            "valid_for_claim": "False",
        },
    ]


def profile_source_acquisition_rows() -> List[Dict[str, str]]:
    return [
        {
            "acquisition_id": "ACQ4382_0_real_profile_pair",
            "needed_source": "rho_H/rho_top profile pair on same W_H",
            "current_location": "not found in current source-intake rows",
            "action_taken": "kept profile quadrature runner ready; no synthetic row promoted",
            "status": "MISSING_REAL_PROFILE_INPUT",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "acquisition_id": "ACQ4382_1_parent_normal_form",
            "needed_source": "parent proof of radial/common-center/Laplacian normal form",
            "current_location": "3037/3055/4381 audits remain unsigned",
            "action_taken": "formal signature attempt split into exact clauses",
            "status": "MISSING_PARENT_SIGNATURE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "acquisition_id": "ACQ4382_2_center_offset_bound",
            "needed_source": "bound on b/R between topological and Hilbert centers",
            "current_location": "new 4382 envelope rows",
            "action_taken": "derived C_l laws and applied them to every 4378 support row",
            "status": "ENVELOPE_READY_VALUES_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "acquisition_id": "ACQ4382_3_delta_N",
            "needed_source": "arena tolerance delta_N for each support row",
            "current_location": "4378 formulas carry delta_N symbolically",
            "action_taken": "kept pass formulas symbolic rather than fabricating tolerances",
            "status": "MISSING_DELTA_N_NUMERIC_VALUE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def center_offset_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "COT4382_0_dipole_shift_bound",
            "statement": "For two equal-monopole spherical profiles whose centers differ by b, the l=1 topological moment obeys E_1^top <= 4 sqrt(pi) (b/R) in the 4378 convention.",
            "derivation": "M_1m=M_H b Y_1m(bhat); sum_m |Y_1m| <= 3/(2 sqrt(pi)); E_1^top=(8pi/3) sum|M_1m|/(M_H R).",
            "effect": "Every 4378 dipole row gets |delta a|/|a_N| <= geometry_factor * 4 sqrt(pi) * b/R.",
            "status": "EXACT_CONSERVATIVE_BOUND",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "COT4382_1_quadrupole_shift_bound",
            "statement": "For the same separated-center spherical branch, E_2^top <= 6 sqrt(pi) (b/R)^2 conservatively.",
            "derivation": "M_2m=M_H b^2 Y_2m(bhat); sum_m |Y_2m| <= 5/(2 sqrt(pi)); E_2^top=(12pi/5) sum|M_2m|/(M_H R^2).",
            "effect": "Every 4378 quadrupole row gets |delta a|/|a_N| <= geometry_factor * 6 sqrt(pi) * (b/R)^2.",
            "status": "EXACT_CONSERVATIVE_BOUND",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "COT4382_2_center_lock_zero",
            "statement": "If parent center lock sets b=0 before readout, all separated-center envelope rows collapse to zero.",
            "derivation": "COT4382_0 and COT4382_1 are powers of b/R; b=0 kills the envelope.",
            "effect": "Connects parent center-lock proof directly to topological moment safety.",
            "status": "CONDITIONAL_PARENT_LOCK_ROUTE",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4382_0_normal_form",
            "claim_tested": "topological exterior moments vanish by parent normal form",
            "required_inputs": "NFS4382_0, NFS4382_1 or NFS4382_2 derived as current-MTS parent signature",
            "status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4382_1_profile_input",
            "claim_tested": "real quadrature profile row can be scored",
            "required_inputs": "rho_H/rho_top source profiles with parent center and units",
            "status": "BLOCKED_REAL_PROFILE_INPUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4382_2_center_offset_envelope",
            "claim_tested": "separated-center failure mode is below arena bound",
            "required_inputs": "numeric b/R bound and numeric delta_N tolerance for each arena",
            "status": "ENVELOPE_READY_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4382_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "topological branch plus remaining source-shadow/readout/boundary/non-Hilbert residuals closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4382_0",
            "decision": DECISION,
            "summary": (
                "4382 attempts the parent normal-form signature and keeps it unsigned: no current parent file proves radial defect, common-center isotropy, or Laplacian-null representative for the raw topological/Hamiltonian density. "
                "Instead of stopping there, it derives the separated-center envelope law. Dipole leakage obeys E_1^top <= 4 sqrt(pi) b/R and quadrupole leakage obeys E_2^top <= 6 sqrt(pi) (b/R)^2, then applies these laws to every 4378 Sun/Mercury/Venus/Earth/Mars and Earth/Moon support row. "
                "The result is a concrete required center-lock/profile-input interface, not a claim."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The next useful object is now specific: either prove b=0 by parent center lock or supply the first real b/R or rho_H/rho_top profile input.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4382_0_normal_form",
            "object": "parent normal-form proof",
            "status": "ATTEMPTED_NOT_DERIVED",
            "note": "radial/common-center/Laplacian routes remain unsigned for raw topological profile defect.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4382_1_center_offset",
            "object": "separated-center envelope",
            "status": "DERIVED_AND_APPLIED",
            "note": "all 4378 dipole/quadrupole rows now have b/R envelope formulas.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4382_2_values",
            "object": "numeric claim values",
            "status": "MISSING",
            "note": "b/R, delta_N and real profile values are not sourced yet.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4382_3_next",
            "object": "next target",
            "status": "CENTER_LOCK_OR_REAL_PROFILE_INPUT_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4382_0",
            "target": NEXT_TARGET,
            "question": "Can the parent lock the topological/Hilbert profile centers together, or can a real profile/offset value be supplied?",
            "preferred_route": "derive parent center lock b=0 before readout from source-readout descent and Hilbert/topological profile ownership.",
            "fallback_route": "fill first b/R or rho_H/rho_top profile input and run the center-offset/profile quadrature rows.",
            "avoid": "claiming from symbolic envelope rows, synthetic smoke data, old q_loc surrogates, total charge or metric-nullity.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    signature_attempts: List[Dict[str, str]],
    acquisition: List[Dict[str, str]],
    offset_theorems: List[Dict[str, str]],
    offset_rows: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: topological profile source acquisition or parent normal-form signature

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4382 tries the proof route first. The raw parent signature is still not signed: the current corpus does not prove that `delta rho_top` is radial zero-monopole, common-center isotropic, or Laplacian-null with boundary silence.

But 4382 does **not** stop at "missing." It derives a conservative analytic envelope for the key failure mode exposed by 4381:

```text
E_1^top <= 4 sqrt(pi) (b/R)
E_2^top <= 6 sqrt(pi) (b/R)^2
```

where `b` is the separation between the Hilbert and topological profile centers and `R` is the source support radius. Applying this to the 4378 score law gives:

```text
|delta a_l|/|a_N| <= geometry_factor_l * C_l * (b/R)^l.
```

So the next physics input is no longer vague. Either parent-center lock gives `b=0`, or a real `b/R`/profile row must be sourced and scored.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Parent Normal-Form Signature Attempt

{md_table(signature_attempts, ["attempt_id", "target_signature", "derivation_attempt", "current_result", "why_not_closed", "next_needed"])}

## Profile Source Acquisition

{md_table(acquisition, ["acquisition_id", "needed_source", "current_location", "action_taken", "status"])}

## Center-Offset Envelope Theorems

{md_table(offset_theorems, ["theorem_id", "statement", "derivation", "effect", "status"])}

## Center-Offset Envelope Rows

{md_table(offset_rows, ["envelope_id", "support_id", "multipole_l", "geometry_factor_s_l", "center_offset_constant_C_l", "deltaa_over_a_coeff", "envelope_law", "pass_formula", "current_status"])}

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
    text = f"""# 4382: topological profile source acquisition or parent normal-form signature

Marker: `{MARKER}`

## What changed

- Tried the parent normal-form proof route and kept it unsigned rather than overclaiming.
- Derived the center-offset envelope `E_1^top <= 4 sqrt(pi)b/R`, `E_2^top <= 6 sqrt(pi)(b/R)^2`.
- Applied that envelope to every 4378 topological support row.
- Converted the next target into a precise demand: parent-center lock `b=0`, or first real `b/R` / profile input.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4382 Transition topological profile source acquisition or parent normal-form signature

Marker: `{MARKER}`

4382 attempts the topological parent normal-form route and leaves it unsigned: no current parent file proves the raw `delta rho_top` is radial zero-monopole, common-center isotropic, or Laplacian-null. The checkpoint then derives the separated-center envelope:

```text
E_1^top <= 4 sqrt(pi) b/R,
E_2^top <= 6 sqrt(pi) (b/R)^2.
```

Applied to the 4378 rows, this turns the topology/profile problem into a concrete center-lock bound. Either the parent proves `b=0` before readout, or a real `b/R`/profile input must be supplied and scored.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4382 packet update: separated-center envelope derived

Marker: `{PACKET_MARKER}`

Packet update: the topological profile branch now has a center-offset envelope. If parent center lock proves `b=0`, the separated-center leakage rows vanish. If not, every 4378 support row now has a required `b/R` formula through `E_1^top <= 4 sqrt(pi)b/R` and `E_2^top <= 6 sqrt(pi)(b/R)^2`. No claim fires until `b/R`, `delta_N`, or real `rho_H/rho_top` profiles are sourced.
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
                "4382 attempts the parent normal-form signature for the topological profile defect and keeps it unsigned: current files do not prove radial zero-monopole, common-center isotropic, or Laplacian-null ownership for raw delta rho_top. "
                "It then derives a concrete separated-center envelope: E_1^top <= 4 sqrt(pi) b/R and E_2^top <= 6 sqrt(pi)(b/R)^2, applying those laws to every 4378 topological support row. "
                "This converts the next missing item into a precise center-lock/source-input demand: prove b=0 before readout, or supply a real b/R or rho_H/rho_top profile. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4382 source register, parent normal-form signature attempt, profile acquisition rows, center-offset theorem rows, envelope rows, claim gates, decision, status, next target and validation CSV.",
            "parent_normal_form_unsigned_center_offset_envelope_derived_nonclaim",
            "Derive parent center lock b=0 or fill the first real b/R/profile source input.",
            "Claiming from symbolic envelope rows, synthetic smoke data, old q_loc surrogates, total charge, metric-nullity or post-hoc centering.",
        ],
    )


def validation_rows(csv_paths: List[Path], offset_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4382_SOURCE_REGISTER.csv")
    signatures = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4382_PARENT_NORMAL_FORM_SIGNATURE_ATTEMPT.csv")
    acquisition = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4382_PROFILE_SOURCE_ACQUISITION.csv")
    offset_theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4382_CENTER_OFFSET_THEOREMS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4382_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4382_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4382_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4382_2_signature_attempt_fail_closed",
        any(row["attempt_id"] == "NFS4382_3_best_available_progress" and row["current_result"] == "CENTER_OFFSET_ENVELOPE_DERIVED" for row in signatures)
        and all(row["valid_for_claim"] == "False" for row in signatures),
        "normal-form attempts fail closed while deriving envelope fallback",
    )
    add(
        "VAL4382_3_acquisition_missing",
        any(row["acquisition_id"] == "ACQ4382_0_real_profile_pair" and row["status"] == "MISSING_REAL_PROFILE_INPUT" for row in acquisition),
        "real profile pair remains missing",
    )
    add(
        "VAL4382_4_offset_theorems",
        any("4 sqrt(pi)" in row["statement"] for row in offset_theorems)
        and any("6 sqrt(pi)" in row["statement"] for row in offset_theorems),
        "dipole and quadrupole center-offset theorems recorded",
    )
    add(
        "VAL4382_5_offset_rows_count",
        len(offset_rows) == len(read_csv(BOUNDS_PATH)),
        "center-offset envelope rows cover every 4378 bound row",
    )
    add(
        "VAL4382_6_offset_coefficients_positive",
        all(float(row["deltaa_over_a_coeff"]) > 0 for row in offset_rows),
        "all envelope coefficients are positive",
    )
    add("VAL4382_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4382_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4382_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4382_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4382_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4382_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4382_13_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4382_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4382_15_runner_script_exists", RUNNER_PATH.exists() and "def center_offset_rows" in read_text(RUNNER_PATH), "center-offset runner script exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    signature_attempts = normal_form_signature_attempt_rows()
    acquisition = profile_source_acquisition_rows()
    offset_theorems = center_offset_theorem_rows()
    offset_rows = center_offset_rows(read_csv(BOUNDS_PATH))
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4382_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4382_PARENT_NORMAL_FORM_SIGNATURE_ATTEMPT.csv": signature_attempts,
        "P8_Y5_R2FR_4382_PROFILE_SOURCE_ACQUISITION.csv": acquisition,
        "P8_Y5_R2FR_4382_CENTER_OFFSET_THEOREMS.csv": offset_theorems,
        "P8_Y5_R2FR_4382_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4382_DECISION.csv": decisions,
        "P8_Y5_R2FR_4382_STATUS.csv": statuses,
        "P8_Y5_R2FR_4382_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)
    write_csv(ENVELOPE_PATH, offset_rows)
    csv_paths.append(ENVELOPE_PATH)

    write_formal_doc(sources, signature_attempts, acquisition, offset_theorems, offset_rows, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths, offset_rows))


if __name__ == "__main__":
    main()
