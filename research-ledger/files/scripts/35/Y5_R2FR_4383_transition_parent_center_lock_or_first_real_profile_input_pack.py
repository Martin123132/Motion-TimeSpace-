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

from topological_center_lock_input_runner import compute_profile_center_rows, envelope_score_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PARENT_DIR = POST / "source-intake" / "parent-action"

CHECKPOINT = "4383"
CLAIM_ID = "L-224"
MARKER = "PPC4161_TRANSITION_PARENT_CENTER_LOCK_OR_FIRST_REAL_PROFILE_INPUT_PACK_4383"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PARENT_CENTER_LOCK_OR_FIRST_REAL_PROFILE_INPUT_PACK_4383"
DECISION = "PARENT_CENTER_LOCK_CONTRACT_DERIVED_INPUT_RUNNER_BUILT_AND_SMOKE_TESTED_REAL_VALUES_MISSING_NONCLAIM"
NEXT_TARGET = "4384-Y5-R2FR-transition-parent-center-functional-proof-or-real-profile-import.md"

FORMAL_PATH = FORMAL / "399-PPC4161-transition-parent-center-lock-or-first-real-profile-input-pack.md"
DOC_PATH = POST / "4383-Y5-R2FR-transition-parent-center-lock-or-first-real-profile-input-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4383_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
ENVELOPE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4382_CENTER_OFFSET_ENVELOPE_ROWS.csv"
RUNNER_PATH = SCRIPT_DIR / "topological_center_lock_input_runner.py"
SMOKE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4383_CENTER_LOCK_SMOKE_INPUT.csv"
SMOKE_CENTERS_PATH = SOURCE_DIR / "P8_Y5_R2FR_4383_CENTER_LOCK_SMOKE_CENTERS.csv"
SMOKE_SCORES_PATH = SOURCE_DIR / "P8_Y5_R2FR_4383_CENTER_LOCK_SMOKE_SCORES.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4383_00_4382_formal": (
        FORMAL / "398-PPC4161-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md",
        "PPC4161_TRANSITION_TOPOLOGICAL_PROFILE_SOURCE_ACQUISITION_OR_PARENT_NORMAL_FORM_SIGNATURE_4382",
        "4382 handoff: parent normal form unsigned, center-offset envelope derived.",
    ),
    "SRC4383_01_4382_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4382_NEXT_TARGET.csv",
        "4383-Y5-R2FR-transition-parent-center-lock-or-first-real-profile-input-pack.md",
        "Explicit 4383 target.",
    ),
    "SRC4383_02_4382_envelope": (
        ENVELOPE_PATH,
        "CENTER_OFFSET_ENVELOPE_READY_VALUES_MISSING",
        "Envelope rows to be scored by b/R.",
    ),
    "SRC4383_03_4382_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4382_CENTER_OFFSET_THEOREMS.csv",
        "COT4382_0_dipole_shift_bound",
        "Center-offset theorem feeding this checkpoint.",
    ),
    "SRC4383_04_4381_runner": (
        SCRIPT_DIR / "profile_topological_moment_quadrature.py",
        "def compute_moment_rows",
        "Moment quadrature runner remains available for real profiles.",
    ),
    "SRC4383_05_runner": (
        RUNNER_PATH,
        "def envelope_score_rows",
        "Center-lock input runner added in 4383.",
    ),
    "SRC4383_06_3037_lock": (
        PARENT_DIR / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
        "MSRL3037_6_verdict",
        "Minimum source-readout lock remains unsigned.",
    ),
    "SRC4383_07_3055_descent": (
        PARENT_DIR / "Hilbert_source_descent_theorem_attempt_3055_NOT_SIGNED.csv",
        "HSD3055_5_verdict",
        "Hilbert source descent remains unsigned.",
    ),
    "SRC4383_08_4377_gate": (
        FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md",
        "M_lm^top-H := int_W delta rho_top r^l Y_lm dV_H = 0",
        "Moment-gate pressure remains the local-GR firewall.",
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


def parent_center_lock_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "PCL4383_0_center_functional_definition",
            "statement": "Define the parent source center c[P,W_H,J_H] before readout as the unique first-moment center of the parent-owned source current on W_H.",
            "proof_or_requirement": "c^i := M_H^{-1} int_W y^i rho_parent dV in a fixed parent collar; uniqueness requires positive M_H, fixed W_H and no post-readout recentering.",
            "effect_if_signed": "gives one center object available to both Hilbert and topological representatives",
            "current_status": "DEFINITION_CONTRACT_READY_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PCL4383_1_factorization_lock",
            "statement": "If rho_H and rho_top are both profile representatives of the same parent source current and both factor through c[P,W_H,J_H] before readout, then c_H=c_top=c and b=0.",
            "proof_or_requirement": "Both centers are evaluations of the same functional on the same source current and worldtube, so their difference is identically zero.",
            "effect_if_signed": "collapses every 4382 center-offset envelope row to zero",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PCL4383_2_readout_order_guard",
            "statement": "Center lock must occur before local test readout; post-hoc coordinate centering cannot be used to set b=0.",
            "proof_or_requirement": "If readout chooses separate coordinates for rho_H and rho_top after the profiles exist, the physical difference delta rho_top can still carry dipole moments.",
            "effect_if_signed": "prevents fake b=0 from coordinate convention",
            "current_status": "GUARD_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PCL4383_3_current_verdict",
            "statement": "Current corpus has the exact center-lock contract, but not the parent signature that makes rho_H and rho_top factor through one center functional.",
            "proof_or_requirement": "3037/3055 remain NOT_SIGNED; 4382 already found no real profile input.",
            "effect_if_signed": "local topological separated-center branch would close for exterior Newton/orbital scoring",
            "current_status": "CENTER_LOCK_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def input_pack_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "contract_id": "IPC4383_0_profile_rows",
            "required_input": "CSV rows with profile_id, x, y, z, volume_weight, rho_H, rho_top, R",
            "runner_use": "topological_center_lock_input_runner.py computes c_H, c_top, b/R",
            "acceptance_rule": "real source/profile provenance; no synthetic labels; positive M_H/M_top; parent-owned radius and worldtube",
            "status": "RUNNER_READY_REAL_INPUT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IPC4383_1_envelope_scores",
            "required_input": "4382 envelope rows and computed b/R",
            "runner_use": "scores predicted |delta a|/|a_N| envelope for each support and l",
            "acceptance_rule": "numeric delta_N must be provided before pass/fail promotion",
            "status": "SCORER_READY_DELTA_N_MISSING",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IPC4383_2_center_lock_zero",
            "required_input": "parent theorem setting b=0 before readout",
            "runner_use": "all b/R score rows collapse to zero",
            "acceptance_rule": "must be a parent signature, not coordinate centering after the fact",
            "status": "THEOREM_ROUTE_READY_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IPC4383_3_quadrature_fallback",
            "required_input": "same profile rows can also feed profile_topological_moment_quadrature.py",
            "runner_use": "computes direct M_lm/E_l^top rather than center-offset envelope",
            "acceptance_rule": "use direct quadrature for non-spherical profiles; use center envelope as conservative separated-center diagnostic",
            "status": "FALLBACK_READY_REAL_INPUT_MISSING",
            "valid_for_claim": "False",
        },
    ]


def smoke_input_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    axes = [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
    for idx, point in enumerate(axes):
        rows.append(profile_row("SMOKE4383_center_locked", "center-locked identical profiles", point, 1.0, 1.0, idx, 1.0))
    shift = 0.25
    for idx, point in enumerate(axes):
        rows.append(profile_row("SMOKE4383_shifted_centers", "shifted centers equal monopoles", point, 1.0, 0.0, idx, 1.25))
    for idx, point in enumerate(axes):
        shifted = (point[0] + shift, point[1], point[2])
        rows.append(profile_row("SMOKE4383_shifted_centers", "shifted centers equal monopoles", shifted, 0.0, 1.0, idx + 100, 1.25))
    return rows


def profile_row(
    profile_id: str,
    label: str,
    point: Tuple[float, float, float],
    rho_h: float,
    rho_top: float,
    sample_index: int,
    radius: float,
) -> Dict[str, str]:
    return {
        "profile_id": profile_id,
        "profile_label": label,
        "sample_id": f"{profile_id}_{sample_index:03d}",
        "source_body": "synthetic_nonclaim",
        "arena": "center_lock_smoke_only",
        "x": f"{point[0]:.16e}",
        "y": f"{point[1]:.16e}",
        "z": f"{point[2]:.16e}",
        "volume_weight": "1.0",
        "rho_H": f"{rho_h:.16e}",
        "rho_top": f"{rho_top:.16e}",
        "R": f"{radius:.16e}",
        "source_profile_path": "SYNTHETIC_SMOKE_NOT_PHYSICAL",
        "input_valid_for_claim": "False",
        "valid_for_claim": "False",
        "claim_allowed": "False",
    }


def smoke_acceptance_rows(center_rows: List[Dict[str, str]], score_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    centers = {row["profile_id"]: row for row in center_rows}
    locked_b = abs(float(centers["SMOKE4383_center_locked"]["b_over_R"]))
    shifted_b = float(centers["SMOKE4383_shifted_centers"]["b_over_R"])
    locked_scores = [abs(float(row["predicted_deltaa_over_a_envelope"])) for row in score_rows if row["profile_id"] == "SMOKE4383_center_locked"]
    shifted_scores = [float(row["predicted_deltaa_over_a_envelope"]) for row in score_rows if row["profile_id"] == "SMOKE4383_shifted_centers"]
    return [
        {
            "accept_id": "CSA4383_0_center_locked_zero",
            "tested_output": "SMOKE4383_center_locked b/R",
            "value": f"{locked_b:.16e}",
            "threshold": "1e-12",
            "passed": str(locked_b < 1e-12),
            "interpretation": "identical parent-centered profiles give b=0",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "CSA4383_1_shifted_detected",
            "tested_output": "SMOKE4383_shifted_centers b/R",
            "value": f"{shifted_b:.16e}",
            "threshold": "> 1e-3",
            "passed": str(shifted_b > 1e-3),
            "interpretation": "shifted profile centers produce a real b/R input",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "CSA4383_2_locked_scores_zero",
            "tested_output": "all center-locked envelope scores",
            "value": f"{max(locked_scores):.16e}",
            "threshold": "1e-12",
            "passed": str(max(locked_scores) < 1e-12),
            "interpretation": "b=0 collapses all envelope scores",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "CSA4383_3_shifted_scores_positive",
            "tested_output": "all shifted envelope scores",
            "value": f"{min(shifted_scores):.16e}",
            "threshold": "> 0",
            "passed": str(min(shifted_scores) > 0.0),
            "interpretation": "nonzero b/R creates finite envelope scores in every support row",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "CSA4383_4_all_nonclaim",
            "tested_output": "smoke center/score rows",
            "value": str(
                all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in center_rows)
                and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in score_rows)
            ),
            "threshold": "True",
            "passed": str(
                all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in center_rows)
                and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in score_rows)
            ),
            "interpretation": "synthetic smoke rows cannot be promoted",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4383_0_parent_center_lock",
            "claim_tested": "b=0 by parent center lock",
            "required_inputs": "PCL4383_0 and PCL4383_1 parent-signed, plus readout-order guard",
            "status": "BLOCKED_PARENT_CENTER_LOCK_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4383_1_real_profile_input",
            "claim_tested": "real b/R or profile input can be scored",
            "required_inputs": "non-synthetic profile CSV with provenance and positive mass/radius",
            "status": "RUNNER_READY_REAL_INPUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4383_2_delta_N",
            "claim_tested": "arena pass/fail from center envelope",
            "required_inputs": "numeric delta_N per support row",
            "status": "DELTA_N_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4383_3_local_GR",
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
            "decision_id": "DEC4383_0",
            "decision": DECISION,
            "summary": (
                "4383 derives the exact parent-center-lock contract: if Hilbert and topological profile representatives factor through one parent source-center functional before readout, then c_H=c_top and b=0, collapsing all 4382 center-offset envelope rows. "
                "The parent signature is not yet signed, so 4383 builds the fallback input runner. It computes c_H, c_top, b/R and all envelope scores from profile CSV rows. Synthetic smoke tests verify that identical centered profiles give b/R=0 while shifted equal-monopole profiles produce nonzero b/R and finite envelope scores. Real source inputs and delta_N values remain missing."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "We now need either the actual parent center functional proof or the first real profile import; both have executable acceptance gates.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4383_0_theorem",
            "object": "parent center-lock theorem",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "note": "b=0 follows if both profiles factor through one parent source-center functional before readout.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4383_1_runner",
            "object": "center-lock input runner",
            "status": "BUILT_AND_SMOKE_TESTED",
            "note": "computes c_H, c_top, b/R and all 4382 envelope scores.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4383_2_values",
            "object": "real values",
            "status": "MISSING",
            "note": "real profile rows and numeric delta_N values are not supplied yet.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4383_3_next",
            "object": "next target",
            "status": "CENTER_FUNCTIONAL_PROOF_OR_REAL_PROFILE_IMPORT_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4383_0",
            "target": NEXT_TARGET,
            "question": "Can the parent center functional c[P,W_H,J_H] be proved, or can real profile rows be imported?",
            "preferred_route": "prove the parent center functional and factorization lock from source-readout descent/Hilbert-topological profile ownership.",
            "fallback_route": "import first real profile CSV or conservative b/R value, then run topological_center_lock_input_runner.py and profile quadrature.",
            "avoid": "using synthetic smoke rows, coordinate recentering after readout, total charge, metric-nullity, or old q_loc surrogates.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorem_rows: List[Dict[str, str]],
    input_contract: List[Dict[str, str]],
    smoke_acceptance: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: parent center lock or first real profile input pack

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4383 derives the exact parent-center-lock contract:

```text
c[P,W_H,J_H] fixed before readout,
rho_H = F_H(P,c,W_H),
rho_top = F_top(P,c,W_H)
=> c_H = c_top = c
=> b = 0
=> every 4382 center-offset envelope row vanishes.
```

This is the clean route, but it is still conditional because the parent source-readout descent has not signed that both profile representatives factor through the same center functional.

So 4383 also builds the fallback input runner:

```text
post-checkpoint-work/scripts/topological_center_lock_input_runner.py
```

It ingests profile rows, computes `c_H`, `c_top`, `b/R`, then scores every 4382 envelope row. Smoke tests verify the fork: identical centered profiles produce `b/R=0`; shifted equal-monopole profiles produce finite `b/R` and finite envelope scores.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Parent Center-Lock Theorem

{md_table(theorem_rows, ["theorem_id", "statement", "proof_or_requirement", "effect_if_signed", "current_status"])}

## Input Pack Contract

{md_table(input_contract, ["contract_id", "required_input", "runner_use", "acceptance_rule", "status"])}

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
    text = f"""# 4383: parent center lock or first real profile input pack

Marker: `{MARKER}`

## What changed

- Derived the exact conditional parent-center-lock theorem: shared parent center before readout gives `b=0`.
- Built `topological_center_lock_input_runner.py` to compute `c_H`, `c_top`, `b/R`, and envelope scores.
- Smoke-tested centered and shifted profiles.
- Kept all outputs nonclaim until the parent signature or real profile inputs exist.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4383 Transition parent center lock or first real profile input pack

Marker: `{MARKER}`

4383 derives the parent-center-lock contract. If `rho_H` and `rho_top` both factor through one parent source-center functional `c[P,W_H,J_H]` before readout, then `c_H=c_top` and `b=0`, so the 4382 separated-center envelope rows vanish. The parent signature is still unsigned.

The fallback is now executable: `topological_center_lock_input_runner.py` computes profile centers, `b/R`, and all 4382 envelope scores from profile CSV rows. Smoke tests confirm centered profiles give zero scores and shifted equal-monopole profiles produce finite scores.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4383 packet update: center-lock theorem and input runner

Marker: `{PACKET_MARKER}`

Packet update: the topological profile branch now has an exact parent-center-lock route and an executable input fallback. Parent center lock makes `b=0`; otherwise `topological_center_lock_input_runner.py` computes `b/R` and all separated-center envelope scores from real profiles. Smoke rows are synthetic and nonclaim.
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
                "4383 derives the exact conditional parent-center-lock contract: if Hilbert and topological profile representatives factor through one parent source-center functional before readout, then c_H=c_top and b=0, collapsing every 4382 center-offset envelope row. "
                "The parent signature is not yet signed, so 4383 adds a fallback runner that computes c_H, c_top, b/R and all envelope scores from profile CSV rows. Synthetic smoke tests verify centered profiles produce b/R=0 while shifted equal-monopole profiles produce finite scores. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4383 source register, parent center-lock theorem rows, input pack contract, synthetic smoke input/centers/scores, smoke acceptance, claim gates, decision, status, next target and validation CSV.",
            "parent_center_lock_contract_input_runner_smoke_tested_nonclaim",
            "Prove the parent center functional/factorization lock or import first real profile rows through the runner.",
            "Using synthetic smoke rows, coordinate recentering after readout, total charge, metric-nullity, or old q_loc surrogates as evidence.",
        ],
    )


def validation_rows(csv_paths: List[Path], center_rows: List[Dict[str, str]], score_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4383_SOURCE_REGISTER.csv")
    theorem_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4383_PARENT_CENTER_LOCK_THEOREM.csv")
    input_contract = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4383_INPUT_PACK_CONTRACT.csv")
    acceptance = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4383_CENTER_LOCK_SMOKE_ACCEPTANCE.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4383_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4383_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4383_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4383_2_center_lock_theorem",
        any(row["theorem_id"] == "PCL4383_1_factorization_lock" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED" for row in theorem_rows),
        "center-lock conditional theorem recorded",
    )
    add(
        "VAL4383_3_input_contract_ready",
        any(row["contract_id"] == "IPC4383_0_profile_rows" and row["status"] == "RUNNER_READY_REAL_INPUT_MISSING" for row in input_contract),
        "profile input contract is runner-ready",
    )
    add(
        "VAL4383_4_center_rows",
        len(center_rows) == 2
        and {row["profile_id"] for row in center_rows} == {"SMOKE4383_center_locked", "SMOKE4383_shifted_centers"},
        "center runner produced two smoke center rows",
    )
    add(
        "VAL4383_5_score_rows",
        len(score_rows) == 20,
        "score runner produced 2 profile x 10 envelope rows",
    )
    add("VAL4383_6_smoke_acceptance", all(row["passed"] == "True" for row in acceptance), "all smoke acceptance rows pass")
    add("VAL4383_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add(
        "VAL4383_8_outputs_nonclaim",
        all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in center_rows)
        and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in score_rows),
        "runner smoke output rows are nonclaim",
    )
    add("VAL4383_9_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4383_10_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4383_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4383_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4383_13_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4383_14_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4383_15_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4383_16_runner_script_exists", RUNNER_PATH.exists() and "def envelope_score_rows" in read_text(RUNNER_PATH), "center-lock runner script exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorem_rows = parent_center_lock_theorem_rows()
    input_contract = input_pack_contract_rows()
    smoke_rows = smoke_input_rows()
    write_csv(SMOKE_INPUT_PATH, smoke_rows)
    center_rows = compute_profile_center_rows(SMOKE_INPUT_PATH)
    score_rows = envelope_score_rows(center_rows, read_csv(ENVELOPE_PATH))
    write_csv(SMOKE_CENTERS_PATH, center_rows)
    write_csv(SMOKE_SCORES_PATH, score_rows)
    smoke_acceptance = smoke_acceptance_rows(center_rows, score_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4383_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4383_PARENT_CENTER_LOCK_THEOREM.csv": theorem_rows,
        "P8_Y5_R2FR_4383_INPUT_PACK_CONTRACT.csv": input_contract,
        "P8_Y5_R2FR_4383_CENTER_LOCK_SMOKE_ACCEPTANCE.csv": smoke_acceptance,
        "P8_Y5_R2FR_4383_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4383_DECISION.csv": decisions,
        "P8_Y5_R2FR_4383_STATUS.csv": statuses,
        "P8_Y5_R2FR_4383_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [SMOKE_INPUT_PATH, SMOKE_CENTERS_PATH, SMOKE_SCORES_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorem_rows, input_contract, smoke_acceptance, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths, center_rows, score_rows))


if __name__ == "__main__":
    main()
