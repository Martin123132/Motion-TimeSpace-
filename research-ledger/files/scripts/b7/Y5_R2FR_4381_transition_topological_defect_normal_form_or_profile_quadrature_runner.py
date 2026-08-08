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

from profile_topological_moment_quadrature import compute_moment_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PARENT_DIR = POST / "source-intake" / "parent-action"

CHECKPOINT = "4381"
CLAIM_ID = "L-222"
MARKER = "PPC4161_TRANSITION_TOPOLOGICAL_DEFECT_NORMAL_FORM_OR_PROFILE_QUADRATURE_RUNNER_4381"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_TOPOLOGICAL_DEFECT_NORMAL_FORM_OR_PROFILE_QUADRATURE_RUNNER_4381"
DECISION = "NORMAL_FORM_THEOREMS_SHARPENED_PROFILE_QUADRATURE_RUNNER_BUILT_AND_SMOKE_TESTED_NONCLAIM"
NEXT_TARGET = "4382-Y5-R2FR-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md"

FORMAL_PATH = FORMAL / "397-PPC4161-transition-topological-defect-normal-form-or-profile-quadrature-runner.md"
DOC_PATH = POST / "4381-Y5-R2FR-transition-topological-defect-normal-form-or-profile-quadrature-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4381_VALIDATION.csv"
RUNNER_PATH = SCRIPT_DIR / "profile_topological_moment_quadrature.py"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SMOKE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4381_PROFILE_QUADRATURE_SMOKE_INPUT.csv"
SMOKE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4381_PROFILE_QUADRATURE_SMOKE_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4381_00_4380_formal": (
        FORMAL / "396-PPC4161-transition-topological-moment-source-intake-or-l0-parent-symmetry-signature.md",
        "PPC4161_TRANSITION_TOPOLOGICAL_MOMENT_SOURCE_INTAKE_OR_L0_PARENT_SYMMETRY_SIGNATURE_4380",
        "4380 handoff: center guard refined and source-intake sweep failed closed.",
    ),
    "SRC4381_01_4380_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4380_NEXT_TARGET.csv",
        "4381-Y5-R2FR-transition-topological-defect-normal-form-or-profile-quadrature-runner.md",
        "Explicit 4381 target.",
    ),
    "SRC4381_02_4380_center": (
        SOURCE_DIR / "P8_Y5_R2FR_4380_CENTER_GUARD_REFINEMENT.csv",
        "CGR4380_1_separate_profile_centers",
        "Separate-center countermodel that motivates the runner.",
    ),
    "SRC4381_03_4380_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4380_L0_PARENT_SIGNATURE_CONTRACT.csv",
        "L0PC4380_6_verdict",
        "Parent l=0 signature remains unsigned.",
    ),
    "SRC4381_04_4379_l0": (
        SOURCE_DIR / "P8_Y5_R2FR_4379_L0_SYMMETRY_THEOREM.csv",
        "L0S4379_0_statement",
        "Centered l=0 zero-monopole theorem.",
    ),
    "SRC4381_05_4378_harmonic": (
        SOURCE_DIR / "P8_Y5_R2FR_4378_HARMONIC_NULL_THEOREM.csv",
        "HN4378_1_laplacian_null_sufficient_condition",
        "Laplacian-null theorem route.",
    ),
    "SRC4381_06_4378_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv",
        "E_1^top := (8pi/3)",
        "Existing 4378 E_l normalization constants.",
    ),
    "SRC4381_07_4377_gate": (
        FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md",
        "M_lm^top-H := int_W delta rho_top r^l Y_lm dV_H = 0",
        "Moment gate being made executable.",
    ),
    "SRC4381_08_4294_kernel": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube",
        "Safe source-kernel branch remains conditional.",
    ),
    "SRC4381_09_4356_common": (
        FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "TH4356_0_static_monopole_common_mode",
        "Common-mode theorem remains conditional for raw transition shells.",
    ),
    "SRC4381_10_runner": (
        RUNNER_PATH,
        "def compute_moment_rows",
        "Reusable profile quadrature runner added in 4381.",
    ),
    "SRC4381_11_parent_lock": (
        PARENT_DIR / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
        "MSRL3037_6_verdict",
        "Minimum source-readout lock remains contract-only.",
    ),
    "SRC4381_12_hilbert_descent": (
        PARENT_DIR / "Hilbert_source_descent_theorem_attempt_3055_NOT_SIGNED.csv",
        "HSD3055_5_verdict",
        "Hilbert source descent remains promising but unsigned.",
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


def normal_form_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "NF4381_0_direct_radial_zero_monopole",
            "normal_form": "delta rho_top(y)=F(|y-c|), int delta rho_top dV=0",
            "proof_or_counterproof": "By Newton shell theorem or angular orthogonality of Y_lm, all l>=1 exterior harmonic moments vanish and the monopole is zero.",
            "effect_if_parent_signed": "set E_l^top=0 for exterior Newton/orbital l>=1 topological scoring",
            "current_parent_status": "CONDITIONAL_EXACT_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NF4381_1_common_center_isotropy",
            "normal_form": "rho_top=f_top(r), rho_H=f_H(r) around same parent center and equal total charge",
            "proof_or_counterproof": "their difference is radial and has zero monopole, so NF4381_0 applies.",
            "effect_if_parent_signed": "same-center isotropic topological/Hilbert profiles become exterior-silent without requiring pointwise equality",
            "current_parent_status": "CENTER_AND_ISOTROPY_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NF4381_2_laplacian_boundary_silent",
            "normal_form": "delta rho_top=Delta u_top with Green boundary silence",
            "proof_or_counterproof": "Green identity from 4378 kills every harmonic moment.",
            "effect_if_parent_signed": "stronger exterior-harmonic-null closure route",
            "current_parent_status": "LAPLACIAN_SIGNATURE_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NF4381_3_separate_center_countermodel",
            "normal_form": "rho_top=f(|y-c_top|), rho_H=f(|y-c_H|), c_top != c_H",
            "proof_or_counterproof": "Expanding in b=c_top-c_H gives delta rho approximately -b dot grad rho_H, producing a dipole proportional to M_H b.",
            "effect_if_parent_signed": "forbids treating equal monopoles or separate spherical profiles as exterior-silent",
            "current_parent_status": "COUNTERMODEL_ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NF4381_4_runner_fallback",
            "normal_form": "finite sampled/analytic rho_H and rho_top profiles on same W_H",
            "proof_or_counterproof": "compute M_lm and E_l^top directly; no cancellation or source-centering shortcut is assumed.",
            "effect_if_parent_signed": "turns missing moment rows into executable source-acquisition rows",
            "current_parent_status": "RUNNER_BUILT_VALUES_REQUIRE_REAL_PROFILE_INPUT",
            "valid_for_claim": "False",
        },
    ]


def parent_normal_form_audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "PNF4381_0_radial_defect_owner",
            "required_parent_signature": "raw topological/Hamiltonian profile defect is a scalar radial zero-monopole function on a parent-owned source collar",
            "evidence_now": "4380/4381 theorem route is exact, but no parent file signs the raw defect normal form",
            "status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_TOPOLOGICAL_DEFECT_NORMAL_FORM",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PNF4381_1_common_center_isotropy",
            "required_parent_signature": "rho_top and rho_H share a source center and isotropy group before readout",
            "evidence_now": "186 supports same-worldtube charge; 4377/4380 reject this as profile/moment proof",
            "status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_COMMON_CENTER_PROFILE_OWNER",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PNF4381_2_boundary_silence",
            "required_parent_signature": "no boundary/collar flux projects into compact l>=1 density moments",
            "evidence_now": "4378 gives exact condition; 4356 keeps boundary-owned clause conditional",
            "status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_BOUNDARY_LGE1_SILENCE",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PNF4381_3_source_readout_lock",
            "required_parent_signature": "profile center and profile representative fixed before local readout/test fitting",
            "evidence_now": "3037/3055 source-readout lock and Hilbert descent are not signed",
            "status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_SOURCE_READOUT_LOCK_PARENT_PROOF",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PNF4381_4_verdict",
            "required_parent_signature": "one of NF4381_0, NF4381_1, or NF4381_2 is parent-owned",
            "evidence_now": "none is signed in current corpus",
            "status": "PARENT_NORMAL_FORM_UNSIGNED",
            "missing_for_claim": "MISSING_REAL_PARENT_SIGNATURE_OR_REAL_PROFILE_INPUT",
            "valid_for_claim": "False",
        },
    ]


def quadrature_schema_rows() -> List[Dict[str, str]]:
    return [
        {
            "field": "profile_id",
            "required": "True",
            "meaning": "groups sample rows into one source profile comparison",
            "units": "text",
            "valid_for_claim_rule": "must be stable and source-backed",
        },
        {
            "field": "x,y,z,volume_weight",
            "required": "True",
            "meaning": "sample coordinates and integration weight on W_H",
            "units": "declared source units",
            "valid_for_claim_rule": "grid/domain and volume convention must be documented",
        },
        {
            "field": "rho_H,rho_top",
            "required": "True",
            "meaning": "ordinary Hilbert and topological density representatives on the same samples",
            "units": "mass per volume or signed mass if volume_weight=1",
            "valid_for_claim_rule": "both profiles must be parent/source-backed, not fitted to kill moments",
        },
        {
            "field": "M_H,R,center_x,center_y,center_z",
            "required": "True for claim rows",
            "meaning": "normalization mass, support radius, and parent-owned center",
            "units": "mass and length",
            "valid_for_claim_rule": "center fixed before readout; M_H/R not imported from orbital GM to hide residuals",
        },
        {
            "field": "input_valid_for_claim",
            "required": "True for promotion",
            "meaning": "upstream source/profile provenance flag",
            "units": "boolean",
            "valid_for_claim_rule": "4381 smoke rows keep this false",
        },
    ]


def smoke_input_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    axes_r1 = [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
    axes_r2 = [(2.0, 0.0, 0.0), (-2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, -2.0, 0.0), (0.0, 0.0, 2.0), (0.0, 0.0, -2.0)]
    for idx, point in enumerate(axes_r1):
        rows.append(smoke_row("SMOKE4381_radial_zero_shell", "radial zero-monopole signed shell", point, 0.0, 1.0, idx, 6.0, 2.0))
    for idx, point in enumerate(axes_r2, start=len(rows)):
        rows.append(smoke_row("SMOKE4381_radial_zero_shell", "radial zero-monopole signed shell", point, 0.0, -1.0, idx, 6.0, 2.0))
    shift = 0.25
    for idx, point in enumerate(axes_r1):
        rows.append(smoke_row("SMOKE4381_shifted_equal_monopoles", "separately centered equal-monopole profiles", point, 1.0, 0.0, idx, 6.0, 1.25))
    for idx, point in enumerate(axes_r1):
        shifted = (point[0] + shift, point[1], point[2])
        rows.append(smoke_row("SMOKE4381_shifted_equal_monopoles", "separately centered equal-monopole profiles", shifted, 0.0, 1.0, idx + 100, 6.0, 1.25))
    return rows


def smoke_row(
    profile_id: str,
    label: str,
    point: Tuple[float, float, float],
    rho_h: float,
    rho_top: float,
    sample_index: int,
    m_h: float,
    support_radius: float,
) -> Dict[str, str]:
    return {
        "profile_id": profile_id,
        "profile_label": label,
        "sample_id": f"{profile_id}_{sample_index:03d}",
        "source_body": "synthetic_nonclaim",
        "arena": "runner_smoke_only",
        "x": f"{point[0]:.16e}",
        "y": f"{point[1]:.16e}",
        "z": f"{point[2]:.16e}",
        "volume_weight": "1.0",
        "rho_H": f"{rho_h:.16e}",
        "rho_top": f"{rho_top:.16e}",
        "M_H": f"{m_h:.16e}",
        "R": f"{support_radius:.16e}",
        "center_x": "0.0",
        "center_y": "0.0",
        "center_z": "0.0",
        "source_profile_path": "SYNTHETIC_SMOKE_NOT_PHYSICAL",
        "input_valid_for_claim": "False",
        "valid_for_claim": "False",
        "claim_allowed": "False",
    }


def smoke_acceptance_rows(output_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    by_key = {(row["profile_id"], row["multipole_l"]): row for row in output_rows}
    radial_l1 = float(by_key[("SMOKE4381_radial_zero_shell", "1")]["E_l_top_4378"])
    radial_l2 = float(by_key[("SMOKE4381_radial_zero_shell", "2")]["E_l_top_4378"])
    shifted_l1 = float(by_key[("SMOKE4381_shifted_equal_monopoles", "1")]["E_l_top_4378"])
    radial_m0 = abs(float(by_key[("SMOKE4381_radial_zero_shell", "0")]["M_delta"]))
    shifted_m0 = abs(float(by_key[("SMOKE4381_shifted_equal_monopoles", "0")]["M_delta"]))
    return [
        {
            "accept_id": "QSM4381_0_radial_l1_zero",
            "tested_output": "SMOKE4381_radial_zero_shell,l=1",
            "value": f"{radial_l1:.16e}",
            "threshold": "1e-12",
            "passed": str(radial_l1 < 1e-12),
            "interpretation": "radial zero-monopole shell has no dipole moment",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "QSM4381_1_radial_l2_zero",
            "tested_output": "SMOKE4381_radial_zero_shell,l=2",
            "value": f"{radial_l2:.16e}",
            "threshold": "1e-12",
            "passed": str(radial_l2 < 1e-12),
            "interpretation": "cubic symmetric signed shell is quadrupole silent in the runner",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "QSM4381_2_shifted_l1_detected",
            "tested_output": "SMOKE4381_shifted_equal_monopoles,l=1",
            "value": f"{shifted_l1:.16e}",
            "threshold": "> 1e-3",
            "passed": str(shifted_l1 > 1e-3),
            "interpretation": "separately centered equal-monopole profiles produce a measurable dipole",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "QSM4381_3_monopoles_zero",
            "tested_output": "both l=0 rows",
            "value": f"radial={radial_m0:.16e}; shifted={shifted_m0:.16e}",
            "threshold": "1e-12",
            "passed": str(radial_m0 < 1e-12 and shifted_m0 < 1e-12),
            "interpretation": "same total charge is preserved while dipole may still appear",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "QSM4381_4_all_runner_rows_nonclaim",
            "tested_output": "all smoke output rows",
            "value": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in output_rows)),
            "threshold": "True",
            "passed": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in output_rows)),
            "interpretation": "smoke data cannot be promoted as evidence",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4381_0_parent_normal_form",
            "claim_tested": "topological moments vanish by parent normal form",
            "required_inputs": "NF4381_0, NF4381_1 or NF4381_2 parent-signed for raw topological defect",
            "status": "BLOCKED_PARENT_NORMAL_FORM_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4381_1_profile_quadrature",
            "claim_tested": "finite source-backed E_l^top row can be scored",
            "required_inputs": "real rho_H/rho_top profile CSV or analytic profile with valid provenance and parent-owned center",
            "status": "RUNNER_READY_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4381_2_smoke_rows",
            "claim_tested": "smoke output can be used as empirical evidence",
            "required_inputs": "physical source profiles, not synthetic smoke",
            "status": "FORBIDDEN_SYNTHETIC_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4381_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "topological moment closure plus remaining source-shadow/readout/boundary/non-Hilbert residuals closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4381_0",
            "decision": DECISION,
            "summary": (
                "4381 turns the 4380 fork into two executable routes. The proof route is now a normal-form theorem bundle: direct radial zero-monopole defect, common-center isotropy plus charge equality, or Laplacian boundary-silent defect. "
                "The fallback route is now a real CSV quadrature runner for l<=2 spherical moments using the 4378 E_l^top conventions. Smoke tests show the runner kills a radial zero-monopole shell and detects a dipole from separately centered equal-monopole profiles. Current MTS parent normal form and real profile inputs remain missing, so all claim gates stay false."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "We can now either sign a parent normal form or feed a real rho_H/rho_top profile into the runner; no more vibes-only moment rows.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4381_0_normal_form",
            "object": "topological defect proof route",
            "status": "EXACT_THEOREMS_READY_PARENT_UNSIGNED",
            "note": "radial zero-monopole/common-center/laplacian routes are mathematically sharp but not signed for raw MTS defect.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4381_1_runner",
            "object": "profile quadrature fallback",
            "status": "RUNNER_BUILT_AND_SMOKE_TESTED",
            "note": "profile_topological_moment_quadrature.py computes l<=2 M_lm and E_l^top rows.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4381_2_inputs",
            "object": "real profile inputs",
            "status": "MISSING",
            "note": "no claim-valid rho_H/rho_top source profile has been ingested.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4381_3_next",
            "object": "next work",
            "status": "SOURCE_ACQUISITION_OR_SIGNATURE_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4381_0",
            "target": NEXT_TARGET,
            "question": "Can a real parent normal-form signature or a real source profile be supplied for delta rho_top?",
            "preferred_route": "prove raw topological defect is radial zero-monopole/common-center isotropic/laplacian-null from parent source construction.",
            "fallback_route": "ingest first real rho_H/rho_top profile or conservative analytic envelope and run profile_topological_moment_quadrature.py.",
            "avoid": "using synthetic smoke output, old q_loc surrogates, total charge, metric-nullity or post-hoc centering as evidence.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    normal_forms: List[Dict[str, str]],
    parent_audit: List[Dict[str, str]],
    schema: List[Dict[str, str]],
    smoke_acceptance: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: topological defect normal form or profile quadrature runner

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4381 stops treating the remaining topological moment problem as a sentence in a ledger. It gives two usable paths.

Proof path:

```text
delta rho_top=F(r), int delta rho_top dV=0
or
rho_top=f_top(r), rho_H=f_H(r) around the same parent center with equal charge
or
delta rho_top=Delta u_top with Green boundary silence
=> M_lm=0 for exterior Newton l>=1.
```

Fallback path:

```text
post-checkpoint-work/scripts/profile_topological_moment_quadrature.py
```

The runner ingests sampled `rho_H` and `rho_top` profiles, computes `M_lm` for `l<=2`, and reports `E_l^top` in the 4378 convention. Its smoke test does exactly what we need: a radial zero-monopole signed shell is moment-silent, while separately centered equal-monopole profiles trigger a dipole even though their total charge matches.

No physical claim fires from 4381. The smoke rows are synthetic and nonclaim; current parent normal-form ownership is unsigned.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Normal Form Theorems

{md_table(normal_forms, ["theorem_id", "normal_form", "proof_or_counterproof", "effect_if_parent_signed", "current_parent_status"])}

## Parent Normal Form Audit

{md_table(parent_audit, ["audit_id", "required_parent_signature", "evidence_now", "status", "missing_for_claim"])}

## Quadrature Schema

{md_table(schema, ["field", "required", "meaning", "units", "valid_for_claim_rule"])}

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
    text = f"""# 4381: topological defect normal form or profile quadrature runner

Marker: `{MARKER}`

## What changed

- Wrote the normal-form theorem bundle for the topological defect route.
- Added `profile_topological_moment_quadrature.py`, a reusable l<=2 moment runner.
- Generated synthetic smoke input/output to verify radial zero-monopole silence and shifted-profile dipole detection.
- Kept all rows nonclaim until a parent normal form or real source profile is supplied.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4381 Transition topological defect normal form or profile quadrature runner

Marker: `{MARKER}`

4381 makes the topological-moment fork executable. The proof route is the exact normal-form bundle: radial zero-monopole defect, common-center isotropic `rho_top/rho_H` with equal charge, or Laplacian-null defect with Green boundary silence. The fallback route is now a real runner, `post-checkpoint-work/scripts/profile_topological_moment_quadrature.py`, which computes `l<=2` spherical moments and `E_l^top` in the 4378 convention from sampled `rho_H/rho_top` profiles.

Smoke verification: synthetic radial zero-monopole input gives zero l=1/l=2 moments; separately centered equal-monopole profiles give a nonzero dipole. This confirms that total charge is not enough and that the next missing payload is either a parent normal-form signature or a real source profile.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4381 packet update: topological moment fork becomes executable

Marker: `{PACKET_MARKER}`

Packet update: the topological profile branch now has a reusable computation path. If the parent signs radial/common-center/Laplacian normal form, `E_l^top=0` for exterior Newton moments. If not, `profile_topological_moment_quadrature.py` ingests real `rho_H/rho_top` profiles and computes l<=2 moment rows. Synthetic smoke rows are explicitly nonclaim.
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
                "4381 turns the topological moment fork into executable proof or data routes. The proof route is a normal-form theorem bundle: direct radial zero-monopole delta rho_top, common-center isotropic rho_top/rho_H with equal charge, or Laplacian-null boundary-silent defect each kills exterior l>=1 moments if parent-signed. "
                "The fallback route is a reusable profile quadrature runner that computes l<=2 spherical moments and E_l^top in the 4378 convention from sampled rho_H/rho_top profiles. Smoke tests verify radial zero-monopole silence and shifted-profile dipole detection. Parent normal-form ownership and real source profiles remain missing, so no local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4381 source register, normal-form theorem rows, parent audit, quadrature schema, synthetic smoke input/output, smoke acceptance, claim gates, decision, status, next target and validation CSV.",
            "normal_form_theorems_profile_quadrature_runner_smoke_tested_nonclaim",
            "Parent-sign topological defect normal form or ingest first real rho_H/rho_top source profile through the quadrature runner.",
            "Using synthetic smoke rows, old q_loc surrogates, same total charge, metric-nullity or post-hoc centering as empirical evidence.",
        ],
    )


def validation_rows(csv_paths: List[Path], output_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4381_SOURCE_REGISTER.csv")
    normal_forms = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4381_NORMAL_FORM_THEOREMS.csv")
    parent_audit = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4381_PARENT_NORMAL_FORM_AUDIT.csv")
    smoke_acceptance = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4381_QUADRATURE_SMOKE_ACCEPTANCE.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4381_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4381_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4381_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4381_2_normal_forms_present",
        any(row["theorem_id"] == "NF4381_0_direct_radial_zero_monopole" for row in normal_forms)
        and any(row["theorem_id"] == "NF4381_3_separate_center_countermodel" for row in normal_forms),
        "normal-form theorem and countermodel rows present",
    )
    add(
        "VAL4381_3_parent_unsigned",
        any(row["audit_id"] == "PNF4381_4_verdict" and row["status"] == "PARENT_NORMAL_FORM_UNSIGNED" for row in parent_audit),
        "parent normal-form route remains unsigned",
    )
    add(
        "VAL4381_4_runner_outputs",
        len(output_rows) == 6
        and {row["profile_id"] for row in output_rows} == {"SMOKE4381_radial_zero_shell", "SMOKE4381_shifted_equal_monopoles"},
        "runner produced l=0,1,2 rows for two smoke profiles",
    )
    add(
        "VAL4381_5_smoke_acceptance",
        all(row["passed"] == "True" for row in smoke_acceptance),
        "smoke acceptance rows all pass",
    )
    add("VAL4381_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add(
        "VAL4381_7_output_nonclaim",
        all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in output_rows),
        "runner smoke output rows are nonclaim",
    )
    add("VAL4381_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4381_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4381_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4381_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4381_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4381_13_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4381_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4381_15_runner_script_exists", RUNNER_PATH.exists() and "def compute_moment_rows" in read_text(RUNNER_PATH), "runner script exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    normal_forms = normal_form_theorem_rows()
    parent_audit = parent_normal_form_audit_rows()
    schema = quadrature_schema_rows()
    smoke_rows = smoke_input_rows()
    write_csv(SMOKE_INPUT_PATH, smoke_rows)
    output_rows = compute_moment_rows(SMOKE_INPUT_PATH)
    write_csv(SMOKE_OUTPUT_PATH, output_rows)
    smoke_acceptance = smoke_acceptance_rows(output_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4381_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4381_NORMAL_FORM_THEOREMS.csv": normal_forms,
        "P8_Y5_R2FR_4381_PARENT_NORMAL_FORM_AUDIT.csv": parent_audit,
        "P8_Y5_R2FR_4381_QUADRATURE_SCHEMA.csv": schema,
        "P8_Y5_R2FR_4381_QUADRATURE_SMOKE_ACCEPTANCE.csv": smoke_acceptance,
        "P8_Y5_R2FR_4381_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4381_DECISION.csv": decisions,
        "P8_Y5_R2FR_4381_STATUS.csv": statuses,
        "P8_Y5_R2FR_4381_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [SMOKE_INPUT_PATH, SMOKE_OUTPUT_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, normal_forms, parent_audit, schema, smoke_acceptance, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths, output_rows))


if __name__ == "__main__":
    main()
