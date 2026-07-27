from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from projective_boundary_readout_guard_gate import (  # noqa: E402
    evaluate_guard_rows,
    evaluate_p4_projective_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4414"
CLAIM_ID = "L-255"
MARKER = "PPC4161_TRANSITION_PROJECTIVE_BOUNDARY_READOUT_GUARD_OR_FIRST_P4_ROW_4414"
PACKET_MARKER = "PPC4161_PACKET_PROJECTIVE_BOUNDARY_READOUT_GUARD_OR_FIRST_P4_ROW_4414"
DECISION = "PROJECTIVE_RUU_GEOMETRIC_ZERO_AND_BRANCH_GUARDS_CLOSED_SELECTOR_SOURCE_READOUT_OPEN_NONCLAIM"
NEXT_TARGET = "4415-Y5-R2FR-transition-owned-coframe-LC-selector-or-source-readout-kernel-fill.md"

FORMAL_PATH = FORMAL / "430-PPC4161-transition-projective-boundary-readout-guard-or-first-P4-row.md"
DOC_PATH = POST / "4414-Y5-R2FR-transition-projective-boundary-guard-for-spin-torsion-zero-or-first-P4-row-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4414_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4414_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4414_DERIVATION_ROWS.csv"
GUARD_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4414_PROJECTIVE_BOUNDARY_GUARD_INPUT.csv"
GUARD_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4414_PROJECTIVE_BOUNDARY_GUARD_OUTPUT.csv"
P4_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4414_P4_PROJECTIVE_RUU_INPUT.csv"
P4_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4414_P4_PROJECTIVE_RUU_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4414_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4414_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4414_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4414_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "projective_boundary_readout_guard_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4414_transition_projective_boundary_guard_for_spin_torsion_zero_or_first_P4_row_fill.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4413 = SOURCE_DIR / "P8_Y5_R2FR_4413_NEXT_TARGET.csv"
FORMAL_429 = FORMAL / "429-PPC4161-transition-spin-torsion-algebraic-zero-parent-signature-or-first-P4-Ruu-row.md"
POST_1963 = POST / "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md"
POST_2119 = POST / "2119-Y5-R2FR-projective-invariance-certificate-or-MICROSCOPE-numeric-kernel-acquisition.md"
POST_2378 = POST / "2378-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md"
POST_1959 = POST / "1959-Y5-R2FR-torsion-boundary-readout-current-silence-or-envelope.md"
POST_2118 = POST / "2118-Y5-R2FR-source-readout-Gamma-silence-or-explicit-exception-kernels.md"
POST_2099 = POST / "2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md"
POST_1960 = POST / "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4414_00_4413_next": (
        NEXT_4413,
        "4414-Y5-R2FR-transition-projective-boundary-guard-for-spin-torsion-zero-or-first-P4-row-fill.md",
        "4413 selected projective/boundary/readout guard.",
    ),
    "SRC4414_01_4413_formal": (
        FORMAL_429,
        "remaining guard is projective trace plus boundary/readout torsion-current silence",
        "4413 handoff identifies the live guard.",
    ),
    "SRC4414_02_1963_owned_coframe": (
        POST_1963,
        "independent observed connection",
        "minimal owned-coframe branch excludes Gamma_ind.",
    ),
    "SRC4414_03_2119_projective": (
        POST_2119,
        "inside that branch by variable absence",
        "projective trace already branch-zero candidate.",
    ),
    "SRC4414_04_2378_private_projective": (
        POST_2378,
        "Projective trace is zero only inside the private owned-coframe + SRNG branch",
        "private projective zero and affine fallback.",
    ),
    "SRC4414_05_1959_boundary": (
        POST_1959,
        "boundary/source-worldtube current is zero only if parent boundary flux",
        "boundary/readout current silence clauses.",
    ),
    "SRC4414_06_2118_source_readout": (
        POST_2118,
        "source, clocks, light, orbit, boundary/domain and projective trace",
        "source/readout Gamma silence contract.",
    ),
    "SRC4414_07_2099_projective_map": (
        POST_2099,
        "DGM2099_6_projective",
        "DeltaGamma projective component map.",
    ),
    "SRC4414_08_1960_projective_caveat": (
        POST_1960,
        "projective freedom is harmless only if all matter/source/readout sectors",
        "projective caveat in LC proof.",
    ),
    "SRC4414_09_gate": (
        GATE_PATH,
        "def evaluate_guard_rows",
        "new projective/boundary/readout gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    body = text(path)
    if not body or needle not in body:
        return False, -1
    line = body[: body.index(needle)].count("\n") + 1
    return True, line


def bool_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "PBR4414_0_projective_Ruu_blindness",
            "claim": "A pure projective shift has no symmetric Ruu contribution.",
            "derivation": "For Gamma'^lambda_{mu nu}=Gamma^lambda_{mu nu}+delta^lambda_mu A_nu, the Ricci change is an antisymmetric curl in the projective one-form, so delta R_(mu nu)=0 and u^mu u^nu delta R_(mu nu)=0.",
            "consequence": "The projective P4 row has a geometric zero for symmetric R_uu/focusing, provided no matter/source/readout trace coupling reintroduces A_mu.",
            "status": "DERIVED_GEOMETRIC_RUU_ZERO_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PBR4414_1_owned_coframe_projective_absence",
            "claim": "Inside the owned-coframe/LC branch, projective trace is absent by variable signature.",
            "derivation": "The branch variables are e_obs, MTS fields, matter fields and owned gauge data, with omega_obs=omega_LC[e_obs]. There is no Gamma_ind or projective trace variable to vary.",
            "consequence": "The projective current is zero by variable absence inside this branch, not by fitted smallness.",
            "status": "BRANCH_PROOF_READY_SELECTOR_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PBR4414_2_boundary_torsion_current",
            "claim": "Boundary torsion current is zero only for metric/LC boundary functionals fixed before readout.",
            "derivation": "If B_boundary=B[e_obs,K_LC[e_obs]] and the induced coframe/worldtube support is fixed before readout, there is no independent torsion/projective boundary argument; otherwise boundary/improvement current must be retained.",
            "consequence": "The branch guard can close for metric-LC boundary terms, but affine/torsional boundary terms become P4 rows.",
            "status": "CONDITIONAL_BRANCH_GUARD_CLOSED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PBR4414_3_readout_torsion_current",
            "claim": "Clock/light/orbit readout torsion current vanishes only when readout is downstream of the same metric coframe support.",
            "derivation": "If clocks use proper time of g_obs, photons use the null cone of g_obs plus owned EM data, and orbits use LC geodesic/Poisson readout on the same worldtube, no independent torsion readout current exists.",
            "consequence": "Readout is branch-silent; source/readout exception kernels stay live outside that support contract.",
            "status": "CONDITIONAL_BRANCH_GUARD_CLOSED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PBR4414_4_public_selector_residue",
            "claim": "4414 lowers the guard but does not make a public local-GR claim.",
            "derivation": "Projective Ruu blindness and branch boundary/readout silence do not prove the parent must select the owned-coframe/LC branch or exclude affine/source/readout counterbranches.",
            "consequence": "The live blocker is now parent branch selection or source/readout kernel acquisition, not an unanalysed projective Ruu term.",
            "status": "SELECTOR_OR_KERNEL_NEXT",
            "valid_for_claim": False,
        },
    ]


def guard_input_rows() -> List[Dict[str, object]]:
    base_false = {
        "input_valid": False,
        "valid_for_claim": False,
    }
    return [
        {
            "guard_id": "PBG4414_0_owned_coframe_lc_branch",
            "branch": "owned_coframe_lc_branch",
            "no_independent_connection": True,
            "gamma_equals_lc": True,
            "projective_mode_absent": True,
            "projective_mode_pure_trace": False,
            "symmetric_ricci_projective_blind": True,
            "projective_fixed_before_coupling": True,
            "all_sector_projective_invariant": False,
            "boundary_functional_metric_lc_only": True,
            "boundary_variation_fixed_induced_coframe": True,
            "boundary_improvement_fixed_before_readout": True,
            "no_boundary_torsion_current": True,
            "clock_light_orbit_metric_only": True,
            "no_readout_torsion_current": True,
            "same_tau_coframe_worldtube_support": True,
            "parent_branch_selector_signed": False,
            "affine_counterbranch_excluded": False,
            "source_path": str(POST_1963),
            "notes": "Branch guard closes by variable absence/fixed LC boundary/readout, but the parent selector is not signed.",
            **base_false,
        },
        {
            "guard_id": "PBG4414_1_pure_projective_ruu_geometry",
            "branch": "affine_pure_projective_geometry_only",
            "no_independent_connection": False,
            "gamma_equals_lc": False,
            "projective_mode_absent": False,
            "projective_mode_pure_trace": True,
            "symmetric_ricci_projective_blind": True,
            "projective_fixed_before_coupling": True,
            "all_sector_projective_invariant": False,
            "boundary_functional_metric_lc_only": False,
            "boundary_variation_fixed_induced_coframe": False,
            "boundary_improvement_fixed_before_readout": False,
            "no_boundary_torsion_current": False,
            "clock_light_orbit_metric_only": False,
            "no_readout_torsion_current": False,
            "same_tau_coframe_worldtube_support": False,
            "parent_branch_selector_signed": False,
            "affine_counterbranch_excluded": False,
            "source_path": str(POST_2099),
            "notes": "Pure projective trace is geometrically Ruu-blind, but boundary/readout/source trace couplings remain outside this row.",
            **base_false,
        },
        {
            "guard_id": "PBG4414_2_affine_source_readout_counterbranch",
            "branch": "affine_source_readout_counterbranch",
            "no_independent_connection": False,
            "gamma_equals_lc": False,
            "projective_mode_absent": False,
            "projective_mode_pure_trace": True,
            "symmetric_ricci_projective_blind": True,
            "projective_fixed_before_coupling": False,
            "all_sector_projective_invariant": False,
            "boundary_functional_metric_lc_only": False,
            "boundary_variation_fixed_induced_coframe": False,
            "boundary_improvement_fixed_before_readout": False,
            "no_boundary_torsion_current": False,
            "clock_light_orbit_metric_only": False,
            "no_readout_torsion_current": False,
            "same_tau_coframe_worldtube_support": False,
            "parent_branch_selector_signed": False,
            "affine_counterbranch_excluded": False,
            "source_path": str(POST_2118),
            "notes": "If source/readout sectors couple to the trace mode, projective Ruu blindness is insufficient.",
            **base_false,
        },
        {
            "guard_id": "PBG4414_3_future_public_signature_schema",
            "branch": "future_parent_signed_owned_coframe_lc_branch",
            "no_independent_connection": True,
            "gamma_equals_lc": True,
            "projective_mode_absent": True,
            "projective_mode_pure_trace": False,
            "symmetric_ricci_projective_blind": True,
            "projective_fixed_before_coupling": True,
            "all_sector_projective_invariant": True,
            "boundary_functional_metric_lc_only": True,
            "boundary_variation_fixed_induced_coframe": True,
            "boundary_improvement_fixed_before_readout": True,
            "no_boundary_torsion_current": True,
            "clock_light_orbit_metric_only": True,
            "no_readout_torsion_current": True,
            "same_tau_coframe_worldtube_support": True,
            "parent_branch_selector_signed": True,
            "affine_counterbranch_excluded": True,
            "source_path": str(GATE_PATH),
            "notes": "Executable public-signature schema; deliberately nonclaim until parent source rows are real.",
            **base_false,
        },
    ]


def p4_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "P4PJ4414_0_projective_ruu_geometric_zero",
            "p4_component": "torsion_trace_projective_mode",
            "arena": "local_Ruu_symmetric_Ricci",
            "residual_symbol": "u^mu u^nu delta R_(mu nu)[A_projective]",
            "source_coefficient": 0,
            "coefficient_units": "dimensionless_geometric_identity",
            "uu_projection": 0,
            "symmetric_ricci_projection": 0,
            "antisymmetric_ricci_projection": 1,
            "support_certificate": "pure_projective_shift_only_same_connection_decomposition",
            "observable_map": "symmetric_Ruu_focusing_blind_to_antisymmetric_projective_curl",
            "comparator_bound": 0,
            "no_cancellation_guard": True,
            "source_path": str(POST_2099),
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Geometric zero covers Ruu only; source, WEP, clock, and readout trace couplings still need zero theorem or finite kernel.",
        },
        {
            "row_id": "P4PJ4414_1_source_readout_projective_kernel",
            "p4_component": "projective_trace_source_readout_current",
            "arena": "WEP_CLOCK_SOURCE_ORBITAL",
            "residual_symbol": "P_projective[source,clock,WEP,orbit]",
            "source_coefficient": "MISSING_TRACE_COUPLING_NORMALIZATION",
            "coefficient_units": "MISSING_PROJECTIVE_CURRENT_UNITS",
            "uu_projection": "MISSING_NOT_RUU_ONLY",
            "symmetric_ricci_projection": "MISSING_NOT_RUU_ONLY",
            "antisymmetric_ricci_projection": "MISSING_TRACE_CURRENT_MAP",
            "support_certificate": "MISSING_SOURCE_READOUT_SUPPORT",
            "observable_map": "MISSING_WEP_CLOCK_SOURCE_PROJECTIVE_KERNEL",
            "comparator_bound": "MISSING_BOUND",
            "no_cancellation_guard": False,
            "source_path": str(POST_2118),
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "This is the real affine fallback row if source/readout trace coupling survives.",
        },
        {
            "row_id": "P4PJ4414_2_boundary_torsion_current_kernel",
            "p4_component": "boundary_improvement_torsion_current",
            "arena": "local_boundary_worldtube",
            "residual_symbol": "P_boundary[J_boundary+J_improvement]",
            "source_coefficient": "MISSING_BOUNDARY_CURRENT_NORMALIZATION",
            "coefficient_units": "MISSING_BOUNDARY_CURRENT_UNITS",
            "uu_projection": "MISSING_BOUNDARY_TO_RUU_PROJECTION",
            "symmetric_ricci_projection": "MISSING_BOUNDARY_TO_SYM_RICCI",
            "antisymmetric_ricci_projection": "MISSING_BOUNDARY_ANTISYM_GUARD",
            "support_certificate": "MISSING_WORLDTUBE_BOUNDARY_SUPPORT",
            "observable_map": "MISSING_BOUNDARY_TO_PPN_OR_RUU_MAP",
            "comparator_bound": "MISSING_BOUND",
            "no_cancellation_guard": False,
            "source_path": str(POST_1959),
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Boundary/improvement current remains a finite kernel outside metric-LC fixed-boundary branch.",
        },
    ]


def claim_gate_rows(guard_output: List[Mapping[str, str]], p4_output: List[Mapping[str, str]]) -> List[Dict[str, object]]:
    status_by_guard = {row["guard_id"]: row["current_status"] for row in guard_output}
    status_by_p4 = {row["row_id"]: row["current_status"] for row in p4_output}
    return [
        {
            "gate_id": "CG4414_0_projective_Ruu_geometry",
            "claim": "pure projective trace has zero symmetric Ruu contribution",
            "passed": status_by_p4.get("P4PJ4414_0_projective_ruu_geometric_zero") == "P4_PROJECTIVE_RUU_GEOMETRIC_ZERO_NONCLAIM",
            "valid_for_claim": False,
            "detail": "geometric identity only; not a source/readout trace-coupling claim",
        },
        {
            "gate_id": "CG4414_1_branch_guard",
            "claim": "owned-coframe/LC projective-boundary-readout guard closes inside the branch",
            "passed": status_by_guard.get("PBG4414_0_owned_coframe_lc_branch")
            == "PROJECTIVE_BOUNDARY_READOUT_GUARD_BRANCH_READY_SELECTOR_OPEN",
            "valid_for_claim": False,
            "detail": "selector remains open, so branch-ready is nonclaim",
        },
        {
            "gate_id": "CG4414_2_public_spin_torsion_zero",
            "claim": "spin/torsion survivor is publicly zero",
            "passed": False,
            "valid_for_claim": False,
            "detail": "parent branch selector and affine/source-readout counterbranch exclusion remain unsigned",
        },
        {
            "gate_id": "CG4414_3_projective_source_kernel_score",
            "claim": "affine projective source/readout fallback is score-ready",
            "passed": False,
            "valid_for_claim": False,
            "detail": "trace-coupling normalization, support and comparator bounds are missing",
        },
        {
            "gate_id": "CG4414_4_local_GR_Newton_PPN",
            "claim": "local GR/Newton/PPN pass follows",
            "passed": False,
            "valid_for_claim": False,
            "detail": "4414 closes a subguard only; it does not close EH/source/GM/PPN residual stack",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4414_0",
            "decision": DECISION,
            "summary": "4414 derives the pure-projective Ruu blindness identity and closes projective/boundary/readout torsion-current silence inside the owned-coframe/LC branch. The public result remains blocked because parent branch selection and affine/source-readout counterbranch exclusion are not signed.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "best_result": "projective_Ruu_geometric_zero_plus_owned_coframe_branch_guard_ready",
            "still_missing": "parent_owned_coframe_LC_selector; affine_counterbranch_exclusion; source_readout_projective_kernel; boundary_current_kernel",
            "valid_for_claim": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4414_0",
            "target": NEXT_TARGET,
            "objective": "Decide whether the parent MTS action selects the owned-coframe/LC branch strongly enough to make the 4414 branch guard public; if not, fill the first source/readout projective kernel row.",
            "derive_first": "parent selector: q(Phi)->e_obs, no Gamma_ind, no affine/source/readout trace coupling, same boundary/worldtube support, and counterbranch exclusion.",
            "fallback": "fill projective/source-readout or boundary-current kernel with coefficient, units, support, observable projection and comparator bound.",
            "avoid": "claiming local GR from pure projective Ruu blindness; hiding source/readout trace coupling; cancelling boundary and projective rows without identity.",
            "valid_for_claim": False,
        }
    ]


def markdown_table(rows: Iterable[Mapping[str, object]]) -> str:
    materialized = [dict(row) for row in rows]
    if not materialized:
        return ""
    headers: List[str] = []
    for row in materialized:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in materialized:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source_register: List[Dict[str, object]],
    guard_output: List[Dict[str, str]],
    p4_output: List[Dict[str, str]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 430 PPC4161 transition: projective-boundary-readout guard or first P4 row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4414 makes a real narrowing move:

- A pure projective connection shift contributes only an antisymmetric Ricci curl, so the symmetric `R_uu = u^mu u^nu R_(mu nu)` slot is geometrically blind to it.
- Inside the owned-coframe/Levi-Civita branch, projective trace is absent by variable signature: `Gamma_ind` is not an argument and `omega_obs=omega_LC[e_obs]`.
- Boundary and readout torsion currents are silent inside the same branch only when boundary functionals, clock/light/orbit readouts and support/worldtube maps are metric-LC downstream objects fixed before readout.
- This is not a public local-GR claim. The parent selector and affine/source-readout counterbranch exclusion remain unsigned.

## Source Register

{markdown_table(source_register)}

## Derivation Rows

{markdown_table(rows_from(DERIVATION_ROWS))}

## Projective-Boundary-Readout Guard

{markdown_table(guard_output)}

## P4 Projective Ruu Rows

{markdown_table(p4_output)}

## Claim Gates

{markdown_table(claim_gates)}

## Decision

{markdown_table(decision_rows())}

## Next Target

{markdown_table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4414 - Y5/R2FR transition projective-boundary guard for spin-torsion zero or first P4 row fill

Private checkpoint for the local-GR route.

Main result: the projective trace is no longer an undifferentiated blocker for `R_uu`. A pure projective shift is symmetric-Ricci blind, and inside the owned-coframe/LC branch there is no independent projective variable. Boundary/readout torsion current silence also closes inside that same branch if the boundary/readout stack is metric-LC and fixed before readout.

Nonclaim rule: this does not prove public local GR. It lowers the blocker to parent branch selection and source/readout affine-counterbranch kernels.

- Formal mirror: `{FORMAL_PATH}`
- Gate: `{GATE_PATH}`
- Generator: `{GENERATOR_PATH}`
- Validation: `{VALIDATION_PATH}`
- Next: `{NEXT_TARGET}`
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    body = text(path)
    block = f"\n{start}\n{section.rstrip()}\n{end}\n"
    if start in body and end in body:
        prefix = body[: body.index(start)]
        suffix = body[body.index(end) + len(end) :]
        write_text(path, prefix.rstrip() + block + suffix.lstrip("\n"))
    else:
        write_text(path, body.rstrip() + "\n" + block)


def update_claims_register() -> None:
    CLAIMS_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["claim_id", "sector", "claim", "evidence", "status", "next_action", "risk"]
    rows: List[Dict[str, str]] = []
    if CLAIMS_PATH.exists():
        with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames:
                fieldnames = reader.fieldnames
            rows = [row for row in reader if row.get("claim_id") != CLAIM_ID]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "sector": "local_gr",
        "claim": "4414 derives a sharper projective/boundary/readout subguard. A pure projective shift is symmetric-Ricci/Ruu blind, and inside the owned-coframe/Levi-Civita branch the projective trace plus boundary/readout torsion currents are absent if boundary/readout are metric-LC downstream functionals fixed before readout. Public promotion remains blocked by parent branch selection and affine/source-readout counterbranch exclusion. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
        "current_evidence": "4414 source register, derivation rows, projective-boundary guard output, P4 projective Ruu rows, claim gates, decision, status, next target and validation CSV.",
        "evidence": "4414 source register, derivation rows, projective-boundary guard output, P4 projective Ruu rows, claim gates, decision, status, next target and validation CSV.",
        "status": "projective_ruu_geometric_zero_branch_guard_ready_nonclaim",
        "next_test": "Derive parent owned-coframe/LC selector and counterbranch exclusion, or fill the first source/readout projective kernel row.",
        "next_action": "Derive parent owned-coframe/LC selector and counterbranch exclusion, or fill the first source/readout projective kernel row.",
        "key_risk": "Claiming local GR from pure projective Ruu blindness; hiding source/readout trace coupling; ignoring boundary/improvement current outside the fixed metric-LC branch.",
        "risk": "Claiming local GR from pure projective Ruu blindness; hiding source/readout trace coupling; ignoring boundary/improvement current outside the fixed metric-LC branch.",
    }
    for key in claim_row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4414 local spine update: projective Ruu blindness and branch guard

4414 separates the projective trace problem from source/readout coupling. For a pure projective shift, `delta R_(mu nu)=0`, so the symmetric `R_uu` focusing slot is blind to the projective curl. Inside the owned-coframe/LC branch, the projective variable is absent entirely, and boundary/readout torsion-current silence closes when the boundary, clocks, light and orbits are all same-support metric-LC downstream functionals fixed before readout. This is forward progress: the spin/torsion survivor is now branch-guard-ready rather than projective-fogged. It is still nonclaim because the parent selector and affine/source-readout counterbranch are unsigned."""
    packet_section = """## 4414 packet update: projective trace is not the Ruu monster

The projective trace no longer blocks the `R_uu` route by itself. Its pure geometric curvature contribution is antisymmetric, so `u^mu u^nu R_(mu nu)` does not see it. The real danger is not that projective trace secretly curves `R_uu`; it is that source, WEP, clock, orbital or boundary/readout sectors might couple to the trace mode before the owned-coframe/LC branch is selected. Next move: prove the parent selector, or fill the first source/readout projective kernel row."""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    source_register = rows_from(SOURCE_REGISTER)
    guard_output = rows_from(GUARD_OUTPUT)
    p4_output = rows_from(P4_OUTPUT)
    claim_gates = rows_from(CLAIM_GATES)
    guard_status = {row["guard_id"]: row["current_status"] for row in guard_output}
    p4_status = {row["row_id"]: row["current_status"] for row in p4_output}
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in guard_output + p4_output + claim_gates)
    checks = [
        ("VAL4414_0_sources_exist", all(row["path_exists"] == "True" for row in source_register), "every cited source path exists"),
        ("VAL4414_1_source_needles_found", all(row["needle_found"] == "True" for row in source_register), "every cited source needle was found"),
        (
            "VAL4414_2_owned_coframe_branch_ready",
            guard_status.get("PBG4414_0_owned_coframe_lc_branch")
            == "PROJECTIVE_BOUNDARY_READOUT_GUARD_BRANCH_READY_SELECTOR_OPEN",
            "owned-coframe branch closes projective/boundary/readout guard but selector remains open",
        ),
        (
            "VAL4414_3_future_schema_nonclaim",
            guard_status.get("PBG4414_3_future_public_signature_schema")
            == "PROJECTIVE_BOUNDARY_READOUT_GUARD_SCHEMA_READY_NONCLAIM",
            "future public signature schema remains nonclaim",
        ),
        (
            "VAL4414_4_projective_ruu_zero",
            p4_status.get("P4PJ4414_0_projective_ruu_geometric_zero")
            == "P4_PROJECTIVE_RUU_GEOMETRIC_ZERO_NONCLAIM",
            "pure projective Ruu row is geometric zero nonclaim",
        ),
        (
            "VAL4414_5_fallback_rows_blocked",
            p4_status.get("P4PJ4414_1_source_readout_projective_kernel", "").endswith("MISSING_INPUT")
            and p4_status.get("P4PJ4414_2_boundary_torsion_current_kernel", "").endswith("MISSING_INPUT"),
            "source/readout and boundary fallback rows stay blocked until filled",
        ),
        ("VAL4414_6_no_claim_outputs", no_claims, "no generated gate row is valid for claim"),
        ("VAL4414_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-255"),
        ("VAL4414_8_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4414_9_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4414_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4414_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4414_12_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4414_13_decision", DECISION in text(DECISION_CSV), "decision CSV contains decision"),
        ("VAL4414_14_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": bool(passed),
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(GUARD_INPUT, guard_input_rows())
    write_csv(P4_INPUT, p4_input_rows())
    write_csv(GUARD_OUTPUT, evaluate_guard_rows(GUARD_INPUT))
    write_csv(P4_OUTPUT, evaluate_p4_projective_rows(P4_INPUT))
    guard_output = rows_from(GUARD_OUTPUT)
    p4_output = rows_from(P4_OUTPUT)
    claim_gates = claim_gate_rows(guard_output, p4_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    source_register = rows_from(SOURCE_REGISTER)
    write_text(FORMAL_PATH, build_doc(source_register, guard_output, p4_output, claim_gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(
        VALIDATION_PATH,
        validation_rows(
            {
                "formal": FORMAL_PATH,
                "post": DOC_PATH,
                "next": NEXT_CSV,
            }
        ),
    )


if __name__ == "__main__":
    main()
