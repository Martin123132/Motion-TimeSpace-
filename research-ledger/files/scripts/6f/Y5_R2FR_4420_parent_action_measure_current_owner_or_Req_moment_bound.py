from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from action_measure_req_gate import evaluate_bound_rows, evaluate_owner_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4420"
CLAIM_ID = "L-261"
MARKER = "PPC4161_PARENT_ACTION_MEASURE_CURRENT_OWNER_OR_REQ_MOMENT_BOUND_4420"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_MEASURE_CURRENT_OWNER_OR_REQ_MOMENT_BOUND_4420"
DECISION = "ACTION_OWNER_REDUCED_TO_SINGLE_PHASE_HBAR_MEASURE_FUNCTOR_AND_REQ_CONTRACT_NONCLAIM"
NEXT_TARGET = "4421-Y5-R2FR-single-phase-action-owner-from-MTS-time-flow-or-first-Deltaw-tau-Req-values.md"

FORMAL_PATH = FORMAL / "436-PPC4161-parent-action-measure-current-owner-or-Req-moment-bound.md"
DOC_PATH = POST / "4420-Y5-R2FR-parent-action-measure-current-owner-or-Req-moment-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4420_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4420_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4420_DERIVATION_ROWS.csv"
OWNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4420_ACTION_MEASURE_OWNER_INPUT.csv"
OWNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4420_ACTION_MEASURE_OWNER_OUTPUT.csv"
BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4420_DELTAW_TAU_REQ_BOUND_INPUT.csv"
BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4420_DELTAW_TAU_REQ_BOUND_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4420_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4420_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4420_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4420_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "action_measure_req_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4420_parent_action_measure_current_owner_or_Req_moment_bound.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4419 = SOURCE_DIR / "P8_Y5_R2FR_4419_NEXT_TARGET.csv"
FORMAL_435 = FORMAL / "435-PPC4161-transition-NoSourceOnlySpeciesSlot-or-topological-mass-current-origin.md"
POST_2774 = POST / "2774-Y5-R2FR-parent-quantum-action-scale-normalization-or-WEP-tau-projection-under-AX1090.md"
POST_1389 = POST / "1389-Y5-R10-RAB-Delta-w-material-source-map-or-action-measure-owner-proof.md"
POST_1412 = POST / "1412-Y5-R10-RAB-ordinary-matter-functor-exhaustion-or-finite-residual-vector.md"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"
POST_3574 = POST / "3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md"
POST_2901 = POST / "2901-Y5-R2FR-parent-q-observed-stack-kernel-nullness-or-current-escape-bound-under-AX1090.md"
POST_2773 = POST / "2773-Y5-R2FR-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width-under-AX1090.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists():
        return 0
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if needle in line:
            return index
    return 0


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4420_00_4419_next",
            "path": NEXT_4419,
            "needle": "4420-Y5-R2FR-parent-action-measure-current-owner-or-Req-moment-bound.md",
            "role": "4419 handoff into action-measure/current-owner or finite R_eq branch.",
        },
        {
            "source_id": "SRC4420_01_435_formal",
            "path": FORMAL_435,
            "needle": "PAC4419_0_single_action_measure",
            "role": "current parent-action source coupling contract.",
        },
        {
            "source_id": "SRC4420_02_2774_action_scale",
            "path": POST_2774,
            "needle": "ASO2774_5_verdict",
            "role": "parent action-scale/hbar owner obstruction.",
        },
        {
            "source_id": "SRC4420_03_1389_owner_theorem",
            "path": POST_1389,
            "needle": "AMP1389_6_theorem_if_signed",
            "role": "conditional Delta_w/beta zero theorem.",
        },
        {
            "source_id": "SRC4420_04_1412_functor",
            "path": POST_1412,
            "needle": "OrdinaryMatterFunctorExhaustion is not proved",
            "role": "ordinary matter functor exhaustion failure and residual vector.",
        },
        {
            "source_id": "SRC4420_05_4378_harmonic_null",
            "path": POST_4378,
            "needle": "delta rho_top=Delta u_top",
            "role": "conditional harmonic-null moment-zero theorem for topological profile defects.",
        },
        {
            "source_id": "SRC4420_06_3574_req",
            "path": POST_3574,
            "needle": "Pi_M J_H = J_M^top + dB_zero + R_eq",
            "role": "R_eq decomposition and same-current topological obstruction.",
        },
        {
            "source_id": "SRC4420_07_2901_kernel",
            "path": POST_2901,
            "needle": "presymplectic-null",
            "role": "parent q/kernel CPS charge and matter-invisibility certificate.",
        },
        {
            "source_id": "SRC4420_08_2773_source_scalar",
            "path": POST_2773,
            "needle": "common action-scale normalization",
            "role": "source-scalar exclusion requires action-scale ownership.",
        },
        {
            "source_id": "SRC4420_09_gate",
            "path": GATE_PATH,
            "needle": "def evaluate_owner_row",
            "role": "4420 action-measure/R_eq bound gate.",
        },
    ]


def source_rows() -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        out.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return out


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "AMO4420_0_phase_hbar_owner_lemma",
            "claim": "A species action weight is equivalent to a species action quantum unless one parent phase/action owner forbids it.",
            "derivation": "The quantum/statistical phase of matter sector A is exp(i w_A S_A/hbar_parent). If w_A is not a measured coupling or field normalization, this is the same observable phase role as exp(i S_A/hbar_A) with hbar_A=hbar_parent/w_A. Therefore a relative w_A is killed only by a single parent action phase and universal hbar/action-clock owner.",
            "consequence": "The coupling problem is now tied to MTS time/phase ownership, not a loose phenomenological source factor.",
            "status": "DERIVED_REDUCTION_TO_SINGLE_PHASE_HBAR_OWNER",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "AMO4420_1_current_owner_limit",
            "claim": "Variation-before-readout cannot remove a pre-variation species action scale by itself.",
            "derivation": "Hilbert stress is T_A proportional to delta(w_A S_A)/delta g. If w_A is already inside S_matter, current ownership merely carries the same w_A into T_H. Thus current owner must be combined with object-language exclusion, universal action measure, and species-blind measure/coframe descent.",
            "consequence": "This blocks the fake route where a Hilbert current is declared universal after the source weight has already been inserted.",
            "status": "DERIVED_CURRENT_OWNER_NOT_ENOUGH",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "REQ4420_0_harmonic_null_transfer",
            "claim": "R_eq profile defects are harmless only under harmonic-null/boundary-silent conditions.",
            "derivation": "Using Pi_M J_H=J_M^top+dB_zero+R_eq, a closed topological current gives d(Pi_M J_H)=dR_eq plus boundary terms. If R_eq=Delta u with boundary-silent u, Green identities kill exterior harmonic moments; otherwise dipole/quadrupole and annulus-flux rows must be bounded.",
            "consequence": "The same-current route and finite source-profile route now share the same R_eq moment object.",
            "status": "DERIVED_REQ_MOMENT_GATE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "AMR4420_0_joint_contract",
            "claim": "Local calibrated Newton source coupling closes if phase-owner and R_eq contracts both close.",
            "derivation": "Single phase/hbar/measure owner kills relative Delta_w and beta source weights; same-current R_eq=0 plus zero boundary flux gives d(Pi_M J_H)=0. Together with the 4418 Poisson/Gauss theorem, this supplies the first-order Newton source leg without orbital-GM backfill.",
            "consequence": "4420 identifies the next real proof: derive a single MTS action phase/time-flow owner and R_eq=0, or score finite Delta_w/tau/R_eq rows.",
            "status": "JOINT_THEOREM_EXACT_PARENT_SIGNATURE_OPEN",
            "valid_for_claim": False,
        },
    ]


def owner_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "owner_id": "AOC4420_0_phase_hbar_owner_attempt",
            "branch": "single_phase_action_clock_route",
            "single_parent_action_phase": True,
            "universal_hbar_parent": False,
            "common_variational_measure": False,
            "species_blind_measure_jacobian": False,
            "variation_before_readout": True,
            "hilbert_current_from_same_action": True,
            "ordinary_matter_functor_exhausted": False,
            "connected_matter_coproduct_or_no_direct_sum_weights": False,
            "derivative_silence_of_common_mode": False,
            "no_hidden_source_scalar": True,
            "same_current_req_route_ready": False,
            "source_path": str(POST_2774),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "4420 reduces w_A to a single action-phase/hbar owner problem; universal hbar and measure owner remain unsigned.",
        },
        {
            "owner_id": "AOC4420_1_functor_exhaustion_bottleneck",
            "branch": "ordinary_matter_functor_exhaustion_route",
            "single_parent_action_phase": True,
            "universal_hbar_parent": True,
            "common_variational_measure": True,
            "species_blind_measure_jacobian": True,
            "variation_before_readout": True,
            "hilbert_current_from_same_action": True,
            "ordinary_matter_functor_exhausted": False,
            "connected_matter_coproduct_or_no_direct_sum_weights": False,
            "derivative_silence_of_common_mode": False,
            "no_hidden_source_scalar": True,
            "same_current_req_route_ready": False,
            "source_path": str(POST_1412),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Even granting action/measure owner, ordinary matter functor exhaustion and derivative silence are still not parent-derived.",
        },
        {
            "owner_id": "AOC4420_2_future_full_owner_contract",
            "branch": "future_action_measure_current_req_contract",
            "single_parent_action_phase": True,
            "universal_hbar_parent": True,
            "common_variational_measure": True,
            "species_blind_measure_jacobian": True,
            "variation_before_readout": True,
            "hilbert_current_from_same_action": True,
            "ordinary_matter_functor_exhausted": True,
            "connected_matter_coproduct_or_no_direct_sum_weights": True,
            "derivative_silence_of_common_mode": True,
            "no_hidden_source_scalar": True,
            "same_current_req_route_ready": True,
            "source_path": str(POST_1389),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact future contract: if parent signs all clauses, Delta_w/beta/R_eq source leg closes. Nonclaim because input_valid=false.",
        },
    ]


def bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "ARB4420_0_WEP_product_bound",
            "residual": "P_WEP_relative_source_weight",
            "arena": "MICROSCOPE_WEP",
            "normal_form": "P_WEP=abs(Delta_w_TiPt*tau_WEP)",
            "Delta_w_AB": "SCHEMA_DELTA_W_TIPT_THEOREM_ZERO_OR_NUMERIC_WIDTH_REQUIRED",
            "tau_WEP": "SCHEMA_TAU_WEP_SOURCE_ORBIT_READOUT_PROJECTION_REQUIRED",
            "R_eq_moment": "SCHEMA_NOT_PRIMARY_FOR_WEP_PRODUCT",
            "B_zero_flux": "SCHEMA_NOT_PRIMARY_FOR_WEP_PRODUCT",
            "source_worldtube_response": "SCHEMA_EARTH_SOURCE_PROFILE_IN_PARENT_BASIS_REQUIRED",
            "material_response": "SCHEMA_TIPT_MATERIAL_RESPONSE_REQUIRED",
            "comparator_bound": "2.8e-15",
            "source_path": str(POST_2774),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "MICROSCOPE bound anchor exists in prior work, but Delta_w and tau_WEP are not sourced as prediction inputs.",
        },
        {
            "bound_id": "ARB4420_1_Req_moment_bound",
            "residual": "R_eq_harmonic_moment",
            "arena": "NEWTON_PPN_ORBITAL_SOURCE_PROFILE",
            "normal_form": "delta a_l/a_N <= E_l^top*(R/r)^l with E_l^top from compact-test or multipole moment of R_eq",
            "Delta_w_AB": "SCHEMA_NOT_PRIMARY_FOR_REQ_MOMENT",
            "tau_WEP": "SCHEMA_NOT_PRIMARY_FOR_REQ_MOMENT",
            "R_eq_moment": "SCHEMA_M1M_OR_M2M_OR_COMPACT_TEST_BOUND_REQUIRED",
            "B_zero_flux": "SCHEMA_BOUNDARY_SILENCE_OR_FLUX_BOUND_REQUIRED",
            "source_worldtube_response": "SCHEMA_FIXED_WORLDTUBE_SUPPORT_REQUIRED",
            "material_response": "SCHEMA_NOT_PRIMARY_FOR_REQ_MOMENT",
            "comparator_bound": "SCHEMA_ARENA_DELTA_N_OR_PPN_BOUND_REQUIRED",
            "source_path": str(POST_4378),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Harmonic-null theorem is conditional; no real R_eq moment values are present.",
        },
        {
            "bound_id": "ARB4420_2_Bzero_flux_bound",
            "residual": "B_zero_flux",
            "arena": "SOURCE_FLUX_GDOT_RADIAL_NEWTON",
            "normal_form": "epsilon_Bzero_flux=abs(int_boundary dB_zero)/abs(M_eff)",
            "Delta_w_AB": "SCHEMA_NOT_PRIMARY_FOR_BZERO",
            "tau_WEP": "SCHEMA_NOT_PRIMARY_FOR_BZERO",
            "R_eq_moment": "SCHEMA_COUPLED_TO_REQ_DECOMPOSITION",
            "B_zero_flux": "SCHEMA_ZERO_FLUX_THEOREM_OR_NUMERIC_BOUND_REQUIRED",
            "source_worldtube_response": "SCHEMA_SOURCE_BOUNDARY_SUPPORT_REQUIRED",
            "material_response": "SCHEMA_NOT_PRIMARY_FOR_BZERO",
            "comparator_bound": "SCHEMA_GDOT_RADIAL_OR_ORBIT_BOUND_REQUIRED",
            "source_path": str(POST_3574),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Boundary exact improvement is named but neither theorem-zero nor bounded.",
        },
    ]


def claim_gate_rows(owner_rows_out: Sequence[Mapping[str, str]], bound_rows_out: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    owner = {row["owner_id"]: row for row in owner_rows_out}
    bounds = {row["bound_id"]: row for row in bound_rows_out}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owner_rows_out) and not any(
        row.get("valid_for_claim") == "True" for row in bound_rows_out
    )
    return [
        {
            "gate_id": "CG4420_0_phase_hbar_reduction",
            "claim": "relative w_A reduces to species action-phase/hbar ownership",
            "passed": True,
            "valid_for_claim": False,
            "detail": "derivation row AMO4420_0 writes the exact phase/action-clock obstruction.",
        },
        {
            "gate_id": "CG4420_1_universal_hbar_measure_owner",
            "claim": "universal hbar/action-measure owner is parent-signed",
            "passed": False,
            "valid_for_claim": False,
            "detail": "AOC4420_0 remains PHASE_OWNER_PRESENT_UNIVERSAL_HBAR_OPEN.",
        },
        {
            "gate_id": "CG4420_2_functor_exhaustion",
            "claim": "ordinary matter functor exhaustion and derivative silence close",
            "passed": owner["AOC4420_1_functor_exhaustion_bottleneck"].get("current_status")
            == "ACTION_MEASURE_READY_FUNCTOR_EXHAUSTION_OPEN",
            "valid_for_claim": False,
            "detail": "functor exhaustion is the next obstruction after action/measure assumptions.",
        },
        {
            "gate_id": "CG4420_3_future_owner_contract",
            "claim": "future full action/current/R_eq contract is executable",
            "passed": owner["AOC4420_2_future_full_owner_contract"].get("current_status")
            == "ACTION_MEASURE_CURRENT_OWNER_CONTRACT_READY_NONCLAIM",
            "valid_for_claim": False,
            "detail": "full contract row closes internally but is nonclaim through input_valid=false.",
        },
        {
            "gate_id": "CG4420_4_bound_pack_ready",
            "claim": "finite Delta_w/tau/R_eq bound pack is schema-ready",
            "passed": bounds["ARB4420_0_WEP_product_bound"].get("current_status")
            == "ACTION_REQ_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM"
            and bounds["ARB4420_1_Req_moment_bound"].get("current_status")
            == "ACTION_REQ_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "detail": "finite branch is staged but not score-ready.",
        },
        {
            "gate_id": "CG4420_5_local_GR_Newton_claim",
            "claim": "calibrated Newton/local-GR source coupling is public",
            "passed": False,
            "valid_for_claim": False,
            "detail": "single phase/hbar owner, functor exhaustion, R_eq=0 and boundary silence remain unsigned.",
        },
        {
            "gate_id": "CG4420_6_no_claim_outputs",
            "claim": "4420 generated no claim-ready row",
            "passed": no_claims,
            "valid_for_claim": False,
            "detail": "4420 is a theorem-reduction and finite-branch staging checkpoint.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4420_0",
            "decision": DECISION,
            "summary": "4420 advances the source-coupling proof by deriving the phase/action-clock meaning of the surviving w_A countermodel: w_A S_A/hbar_parent is equivalent to a species hbar_A unless a single parent action phase and universal hbar/measure owner forbids it. Current MTS still lacks that signed owner, ordinary matter functor exhaustion, and R_eq/boundary/worldtube equality. The finite fallback is staged as Delta_w/tau_WEP/R_eq/B_zero rows rather than fitted-G language.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4420_0_best_result",
            "status": "W_A_REDUCED_TO_SINGLE_PHASE_HBAR_OWNER",
            "detail": "The coupling obstruction now points directly at MTS time/phase/action ownership.",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT4420_1_open_theorem",
            "status": "UNIVERSAL_HBAR_MEASURE_FUNCTOR_REQ_OPEN",
            "detail": "Need parent-signed single action phase, universal hbar/measure, ordinary functor exhaustion, and R_eq=0/boundary silence.",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT4420_2_fallback",
            "status": "DELTAW_TAU_REQ_BOUNDS_STAGED_NONCLAIM",
            "detail": "If theorem proof fails, score finite WEP/source and R_eq moment rows with real values only.",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4420_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive a single parent action phase/hbar owner from MTS time-flow/phase primitives; in parallel, prepare first real finite values for Delta_w*tau_WEP and R_eq moment/B_zero rows if the theorem route remains unsigned.",
            "derive_first": "show the MTS parent has one phase/action clock and one variational measure for all ordinary matter representations, so species hbar_A or w_A is not a legal object.",
            "fallback": "fill source-backed nonclaim values or bounded intervals for P_WEP=Delta_w*tau_WEP, R_eq dipole/quadrupole moments, B_zero_flux and source-worldtube response.",
            "avoid": "setting tau_WEP=1; treating classical EOM rescaling as action-scale proof; using total charge as R_eq profile equality; hiding relative weights in measured G.",
            "valid_for_claim": False,
        }
    ]


def build_doc(
    sources: Sequence[Mapping[str, object]],
    owner_out: Sequence[Mapping[str, str]],
    bound_out: Sequence[Mapping[str, str]],
    gates: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 436 PPC4161 parent action-measure current owner or R_eq moment bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4420 makes the coupling target sharper:

- A relative species action weight `w_A` is equivalent to a species-dependent action quantum `hbar_A` unless MTS has one parent action phase/hbar owner.
- A Hilbert current owner alone cannot erase `w_A`; if `w_A` entered before variation, Hilbert stress carries it.
- The topological source route is now the same finite object: `R_eq` moments and `B_zero` boundary flux.
- The theorem path needs one signed package: single phase/hbar owner, common measure, ordinary matter functor exhaustion, derivative silence, and same-current `R_eq=0`.
- The fallback rows are staged as `Delta_w*tau_WEP`, `R_eq` moments and `B_zero_flux`, not as fitted `G`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Action Owner Gate

{table(owner_out)}

## Delta-w / tau / R_eq Bound Gate

{table(bound_out)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4420 - parent action-measure current owner or R_eq moment bound

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Derived the phase/action-clock interpretation of the surviving `w_A` countermodel.
- Separated current ownership from action-scale ownership: variation-before-readout is necessary but not enough.
- Integrated the topological profile route through `R_eq` moment and `B_zero` finite rows.
- Kept local-GR/Newton/WEP/PPN claims false until parent action phase/hbar owner and same-current equality close.

## Decision

{table(decision_rows())}

## Next target

{table(next_rows())}
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{section.rstrip()}\n{end}\n"
    if start in existing and end in existing:
        before = existing.split(start)[0]
        after = existing.split(end, 1)[1].lstrip("\n")
        write_text(path, before + block + after)
    else:
        sep = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + sep + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = rows[0].keys() if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "4420 derives the phase/action-clock interpretation of the remaining source-coupling countermodel: a relative w_A in w_A S_A/hbar_parent is equivalent to a species hbar_A unless a single parent action phase/hbar/measure owner forbids it. Current MTS has not parent-signed that owner, ordinary matter functor exhaustion, or R_eq/boundary/worldtube equality, so the branch remains nonclaim with finite Delta_w/tau_WEP/R_eq rows staged.",
            "current_evidence": "4420 source register, derivation rows, action-owner output, Delta_w/tau/R_eq bound output, claim gates, decision, status, next target and validation CSV.",
            "status": "wA_reduced_to_single_phase_hbar_owner_req_bound_pack_nonclaim",
            "next_test": "Derive single parent action phase/hbar owner from MTS time-flow primitives or fill source-backed Delta_w*tau_WEP and R_eq/B_zero finite rows.",
            "key_risk": "Mistaking classical EOM rescaling for action-scale proof, setting tau_WEP=1, using total charge for profile equality, or hiding source weights in measured G.",
            "sector": "local_gr",
            "evidence": "4420 source register, derivation rows, action-owner output, Delta_w/tau/R_eq bound output, claim gates, decision, status, next target and validation CSV.",
            "next_action": "Derive single parent action phase/hbar owner from MTS time-flow primitives or fill source-backed Delta_w*tau_WEP and R_eq/B_zero finite rows.",
            "risk": "Mistaking classical EOM rescaling for action-scale proof, setting tau_WEP=1, using total charge for profile equality, or hiding source weights in measured G.",
        }
    )
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4420 local spine update: source weights become an action-phase problem

4420 moves the coupling branch forward by identifying the exact meaning of the surviving `w_A`: unless MTS signs one parent action phase and universal `hbar`/measure owner, `w_A S_A/hbar_parent` is equivalent to a species-dependent action quantum `hbar_A`. A Hilbert current owner is not enough if the weight enters before variation. The clean theorem now asks for one phase/hbar/measure owner plus ordinary matter functor exhaustion and same-current `R_eq=0`; the finite fallback is explicit `Delta_w*tau_WEP`, `R_eq` moment and `B_zero_flux` rows.
"""
    packet_section = f"""## 4420 packet update: action phase owner target

`{PACKET_MARKER}`

Private packet result: calibrated source coupling has been reduced to a time/phase/action-owner theorem. If all ordinary matter sectors descend from one parent action phase with one `hbar`/measure owner, then species source weights are not legal independent objects. Current packet remains nonclaim because universal hbar/measure ownership, functor exhaustion and `R_eq`/boundary equality are unsigned.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    owner = {row["owner_id"]: row for row in rows_from(OWNER_OUTPUT)}
    bounds = {row["bound_id"]: row for row in rows_from(BOUND_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owner.values()) and not any(
        row.get("valid_for_claim") == "True" for row in bounds.values()
    )
    checks = [
        ("VAL4420_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4420_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        (
            "VAL4420_2_phase_owner_open",
            owner["AOC4420_0_phase_hbar_owner_attempt"].get("current_status") == "PHASE_OWNER_PRESENT_UNIVERSAL_HBAR_OPEN",
            "phase owner route now points at universal hbar/measure",
        ),
        (
            "VAL4420_3_functor_open",
            owner["AOC4420_1_functor_exhaustion_bottleneck"].get("current_status")
            == "ACTION_MEASURE_READY_FUNCTOR_EXHAUSTION_OPEN",
            "functor exhaustion remains open after action/measure assumptions",
        ),
        (
            "VAL4420_4_future_contract_nonclaim",
            owner["AOC4420_2_future_full_owner_contract"].get("current_status")
            == "ACTION_MEASURE_CURRENT_OWNER_CONTRACT_READY_NONCLAIM",
            "future full owner contract is executable nonclaim",
        ),
        (
            "VAL4420_5_wep_schema",
            bounds["ARB4420_0_WEP_product_bound"].get("current_status")
            == "ACTION_REQ_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "WEP product finite branch schema ready but values missing",
        ),
        (
            "VAL4420_6_req_schema",
            bounds["ARB4420_1_Req_moment_bound"].get("current_status")
            == "ACTION_REQ_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "R_eq moment finite branch schema ready but values missing",
        ),
        ("VAL4420_7_no_claim_outputs", no_claims, "no generated row is claim-ready"),
        (
            "VAL4420_8_claim_gates",
            any(row["gate_id"] == "CG4420_6_no_claim_outputs" and row["passed"] == "True" for row in gates),
            "claim gates explicitly block public claim",
        ),
        ("VAL4420_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-261"),
        ("VAL4420_10_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4420_11_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4420_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4420_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4420_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4420_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
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
    write_csv(OWNER_INPUT, owner_input_rows())
    write_csv(BOUND_INPUT, bound_input_rows())
    write_csv(OWNER_OUTPUT, evaluate_owner_rows(OWNER_INPUT))
    write_csv(BOUND_OUTPUT, evaluate_bound_rows(BOUND_INPUT))
    owner_output = rows_from(OWNER_OUTPUT)
    bound_output = rows_from(BOUND_OUTPUT)
    claim_gates = claim_gate_rows(owner_output, bound_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), owner_output, bound_output, claim_gates))
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
