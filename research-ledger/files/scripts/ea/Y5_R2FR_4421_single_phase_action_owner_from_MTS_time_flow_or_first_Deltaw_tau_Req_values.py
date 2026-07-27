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

from single_phase_time_owner_gate import evaluate_phase_owner_rows, evaluate_value_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
RAB_QUEUE = POST / "source-intake" / "rab-sector" / "acquisition-queue"
CORE = ROOT / "core-mts-framework"

CHECKPOINT = "4421"
CLAIM_ID = "L-262"
MARKER = "PPC4161_SINGLE_PHASE_ACTION_OWNER_FROM_MTS_TIME_FLOW_OR_FIRST_VALUES_4421"
PACKET_MARKER = "PPC4161_PACKET_SINGLE_PHASE_ACTION_OWNER_FROM_MTS_TIME_FLOW_OR_FIRST_VALUES_4421"
DECISION = "MTS_TIME_FLOW_SUPPLIES_PHASE_LINE_SEED_HBAR_MEASURE_TAU_REQ_STILL_OPEN_NONCLAIM"
NEXT_TARGET = "4422-Y5-R2FR-universal-hbar-measure-owner-or-first-source-backed-Pwep-Req-row.md"

FORMAL_PATH = FORMAL / "437-PPC4161-single-phase-action-owner-from-MTS-time-flow-or-first-Deltaw-tau-Req-values.md"
DOC_PATH = POST / "4421-Y5-R2FR-single-phase-action-owner-from-MTS-time-flow-or-first-Deltaw-tau-Req-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4421_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4421_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4421_DERIVATION_ROWS.csv"
PHASE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4421_SINGLE_PHASE_OWNER_INPUT.csv"
PHASE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4421_SINGLE_PHASE_OWNER_OUTPUT.csv"
VALUE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4421_FIRST_VALUE_INPUT.csv"
VALUE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4421_FIRST_VALUE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4421_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4421_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4421_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4421_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "single_phase_time_owner_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4421_single_phase_action_owner_from_MTS_time_flow_or_first_Deltaw_tau_Req_values.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4420 = SOURCE_DIR / "P8_Y5_R2FR_4420_NEXT_TARGET.csv"
FORMAL_436 = FORMAL / "436-PPC4161-parent-action-measure-current-owner-or-Req-moment-bound.md"
CORE_TIME = CORE / "relativity" / "time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md"
CORE_ACTION = CORE / "action-principle" / "the-motion-timespace-action-principle.md"
CORE_FUNDAMENTAL = CORE / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
POST_PHASE = POST / "2423-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md"
POST_TAU = POST / "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md"
POST_HEURISTIC = POST / "00-martin-fork-heuristics-private.md"
RAB_TAU_DESCENT = RAB_QUEUE / "JR1733_DESCENT_LEMMA.csv"
RAB_TAU_LOCK = RAB_QUEUE / "JR1725_THEOREM_AUDIT.csv"
RAB_ACTION = RAB_QUEUE / "JR1694_ACTION_MEASURE_OWNER_PROOF_GATE.csv"
RAB_COMMON_OWNER = RAB_QUEUE / "JR1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv"


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
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4421_00_4420_next", "path": NEXT_4420, "needle": "4421-Y5-R2FR-single-phase-action-owner-from-MTS-time-flow-or-first-Deltaw-tau-Req-values.md", "role": "4420 handoff into single phase owner or finite values."},
        {"source_id": "SRC4421_01_436_formal", "path": FORMAL_436, "needle": "AMO4420_0_phase_hbar_owner_lemma", "role": "phase/hbar owner reduction from 4420."},
        {"source_id": "SRC4421_02_core_time", "path": CORE_TIME, "needle": "time is not an independent dimension", "role": "MTS time-flow/exchange primitive."},
        {"source_id": "SRC4421_03_core_action", "path": CORE_ACTION, "needle": "time is the rate of curvature-exchange", "role": "MTS action-principle time-flow statement."},
        {"source_id": "SRC4421_04_fundamental_action", "path": CORE_FUNDAMENTAL, "needle": "A_MTS[ψ]", "role": "microscopic MTS action/psi phase-line seed."},
        {"source_id": "SRC4421_05_phase_lock_demoted", "path": POST_PHASE, "needle": "PHASE_LOCK_DEMOTED", "role": "free phase-locking is not enough."},
        {"source_id": "SRC4421_06_tau_identity", "path": POST_TAU, "needle": "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit", "role": "same tau identity remains unsigned."},
        {"source_id": "SRC4421_07_private_time_heuristic", "path": POST_HEURISTIC, "needle": "field phase/oscillation rate", "role": "private fork discipline separating clock, phase and traversal time."},
        {"source_id": "SRC4421_08_tau_projectable", "path": RAB_TAU_DESCENT, "needle": "DCL1733_3_tau_projectable", "role": "tau projectability through q contract."},
        {"source_id": "SRC4421_09_one_generator", "path": RAB_TAU_LOCK, "needle": "TSL1725_9_composite_theorem", "role": "one-generator tau lock contract."},
        {"source_id": "SRC4421_10_action_measure", "path": RAB_ACTION, "needle": "OWG1694_2_single_action_measure", "role": "single action measure proof gate."},
        {"source_id": "SRC4421_11_common_owner", "path": RAB_COMMON_OWNER, "needle": "COM1687_4_measure_hbar", "role": "single hbar/path-integral measure owner gap."},
        {"source_id": "SRC4421_12_gate", "path": GATE_PATH, "needle": "def evaluate_phase_owner_row", "role": "4421 single phase owner gate."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        rows.append(
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
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "SPT4421_0_time_flow_phase_line",
            "claim": "MTS time-flow language supplies a candidate single phase/action line, not yet a universal hbar theorem.",
            "derivation": "Core MTS identifies time with curvature-motion exchange and writes a microscopic psi action. If the same parent exchange parameter owns action accumulation for every ordinary matter representation, then S/hbar is one phase line. This is the correct route from Martin's traversal/process-time instinct to source-coupling discipline.",
            "consequence": "The coupling theorem should be attacked through single action-phase ownership, not by fitting source weights.",
            "status": "MTS_PHASE_LINE_SEED_DERIVED_HBAR_OWNER_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SPT4421_1_species_hbar_no_go",
            "claim": "Species hbar_A or w_A is an extra phase clock.",
            "derivation": "If all ordinary matter lives on one action phase line, exp(i w_A S_A/hbar_parent)=exp(i S_A/hbar_A) with hbar_A=hbar_parent/w_A introduces a species clock/phase unit. That violates the single parent phase owner unless hbar_A is measured matter data or a common calibration.",
            "consequence": "A signed single-phase owner would set relative Delta_w_AB=0 without burying it in measured G.",
            "status": "EXACT_IF_SINGLE_PHASE_OWNER_SIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SPT4421_2_clock_phase_split_guard",
            "claim": "Local proper time, phase/action time and traversal/process time must not be conflated.",
            "derivation": "MTS can use a background phase/traversal owner only if observable clock time still reduces to SR/GR and tau_source=tau_charge=tau_clock=tau_orbit is parent-locked where tests require it. Otherwise the phase owner becomes a hidden time-rescaling residual.",
            "consequence": "The next theorem needs tau projectability and one-generator lock, not just a slogan about time flow.",
            "status": "CLOCK_PHASE_SPLIT_GUARD_DERIVED_TAU_LOCK_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SPT4421_3_phase_lock_demoted",
            "claim": "Phase-locking distributions are not the single-phase owner.",
            "derivation": "Prior phase-lock work already demoted random/even/odd lock distributions: they may describe q-residual operators or memory kernels, but not universal action measure ownership. The owner must be a parent action/measure/phase object.",
            "consequence": "No local-GR/Newton source claim can be made from phase-lock language alone.",
            "status": "NO_PHASE_LOCK_SHORTCUT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VAL4421_0_first_values_status",
            "claim": "The finite branch has one real comparator anchor but no MTS prediction values yet.",
            "derivation": "The WEP product comparator 2.8e-15 can be carried forward as a bound anchor. The MTS-side values Delta_w_TiPt, tau_WEP and R_eq moments/B_zero_flux remain missing or theorem-conditional.",
            "consequence": "4422 should either prove universal hbar/measure ownership or fill the first source-backed prediction row.",
            "status": "COMPARATOR_ONLY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def phase_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SPO4421_0_MTS_time_flow_seed",
            "branch": "curvature_motion_exchange_time_flow",
            "parent_time_flow_unique": True,
            "phase_action_line_defined": True,
            "single_hbar_phase_unit": False,
            "universal_quantum_statistical_measure": False,
            "ordinary_matter_same_phase_bundle": False,
            "no_species_hbar_or_action_clock": False,
            "tau_projectable_through_q": False,
            "clock_phase_traversal_split_respected": True,
            "species_blind_measure_jacobian": False,
            "variation_before_readout": False,
            "hilbert_current_same_action": False,
            "Req_same_current_route": False,
            "source_path": str(CORE_TIME),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Core MTS supplies a time-flow/exchange seed, but not a universal hbar/measure/source-current owner.",
        },
        {
            "row_id": "SPO4421_1_action_principle_seed",
            "branch": "psi_action_phase_line_seed",
            "parent_time_flow_unique": True,
            "phase_action_line_defined": True,
            "single_hbar_phase_unit": False,
            "universal_quantum_statistical_measure": False,
            "ordinary_matter_same_phase_bundle": False,
            "no_species_hbar_or_action_clock": False,
            "tau_projectable_through_q": False,
            "clock_phase_traversal_split_respected": True,
            "species_blind_measure_jacobian": False,
            "variation_before_readout": True,
            "hilbert_current_same_action": False,
            "Req_same_current_route": False,
            "source_path": str(CORE_FUNDAMENTAL),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Microscopic psi action gives an action line seed; ordinary matter hbar/measure owner is still not derived.",
        },
        {
            "row_id": "SPO4421_2_tau_lock_bottleneck",
            "branch": "one_generator_tau_projectability",
            "parent_time_flow_unique": True,
            "phase_action_line_defined": True,
            "single_hbar_phase_unit": True,
            "universal_quantum_statistical_measure": False,
            "ordinary_matter_same_phase_bundle": True,
            "no_species_hbar_or_action_clock": True,
            "tau_projectable_through_q": False,
            "clock_phase_traversal_split_respected": True,
            "species_blind_measure_jacobian": False,
            "variation_before_readout": True,
            "hilbert_current_same_action": True,
            "Req_same_current_route": False,
            "source_path": str(RAB_TAU_LOCK),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Even if hbar owner is granted, tau/source/clock/orbit projectability remains unsigned.",
        },
        {
            "row_id": "SPO4421_3_future_single_phase_contract",
            "branch": "future_parent_single_phase_owner_contract",
            "parent_time_flow_unique": True,
            "phase_action_line_defined": True,
            "single_hbar_phase_unit": True,
            "universal_quantum_statistical_measure": True,
            "ordinary_matter_same_phase_bundle": True,
            "no_species_hbar_or_action_clock": True,
            "tau_projectable_through_q": True,
            "clock_phase_traversal_split_respected": True,
            "species_blind_measure_jacobian": True,
            "variation_before_readout": True,
            "hilbert_current_same_action": True,
            "Req_same_current_route": True,
            "source_path": str(RAB_COMMON_OWNER),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact future contract: if parent signs all clauses, species hbar_A/w_A is illegal and the source leg can close. Nonclaim because input_valid=false.",
        },
    ]


def value_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "value_id": "FVR4421_0_WEP_product_anchor",
            "quantity": "P_WEP_relative_source_weight",
            "arena": "MICROSCOPE_WEP",
            "normal_form": "P_WEP=abs(Delta_w_TiPt*tau_WEP)",
            "predicted_value": "MISSING_DELTA_W_TIPT_TIMES_TAU_WEP",
            "comparator_value": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(POST_TAU),
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "projection_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Real comparator anchor only; no MTS prediction value.",
        },
        {
            "value_id": "FVR4421_1_Req_moment_value",
            "quantity": "R_eq_harmonic_moment",
            "arena": "Newton_PPN_orbital_source_profile",
            "normal_form": "delta a_l/a_N <= E_l^top*(R/r)^l",
            "predicted_value": "MISSING_R_EQ_M1M_M2M_OR_COMPACT_TEST_BOUND",
            "comparator_value": "SCHEMA_ARENA_DELTA_N_OR_PPN_BOUND_REQUIRED",
            "units": "dimensionless",
            "source_path": str(POST_PHASE),
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "projection_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "No R_eq moment value found in current corpus.",
        },
        {
            "value_id": "FVR4421_2_Bzero_flux_value",
            "quantity": "B_zero_flux",
            "arena": "source_flux_Gdot_radial_Newton",
            "normal_form": "epsilon_Bzero_flux=abs(int_boundary dB_zero)/abs(M_eff)",
            "predicted_value": "MISSING_B_ZERO_FLUX_THEOREM_OR_BOUND",
            "comparator_value": "SCHEMA_GDOT_RADIAL_OR_ORBIT_BOUND_REQUIRED",
            "units": "dimensionless",
            "source_path": str(POST_TAU),
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "projection_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Boundary/time source row remains schema-only.",
        },
    ]


def claim_gate_rows(phase_out: Sequence[Mapping[str, str]], value_out: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    phase = {row["row_id"]: row for row in phase_out}
    values = {row["value_id"]: row for row in value_out}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in phase_out) and not any(
        row.get("valid_for_claim") == "True" for row in value_out
    )
    return [
        {"gate_id": "CG4421_0_time_phase_seed", "claim": "MTS time-flow gives a phase/action-line seed", "passed": phase["SPO4421_0_MTS_time_flow_seed"].get("current_status") == "MTS_TIME_PHASE_READY_HBAR_OWNER_OPEN", "valid_for_claim": False, "detail": "seed exists but hbar/measure owner remains open."},
        {"gate_id": "CG4421_1_phase_lock_shortcut_rejected", "claim": "free phase-locking is not promoted", "passed": True, "valid_for_claim": False, "detail": "2423 demotion is imported as a guard."},
        {"gate_id": "CG4421_2_tau_projectability", "claim": "tau source/charge/clock/orbit projectability is parent-signed", "passed": False, "valid_for_claim": False, "detail": "one-generator lock remains a contract."},
        {"gate_id": "CG4421_3_future_single_phase_contract", "claim": "future single-phase owner contract is executable", "passed": phase["SPO4421_3_future_single_phase_contract"].get("current_status") == "SINGLE_PHASE_ACTION_OWNER_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "contract row closes internally but remains nonclaim through input_valid=false."},
        {"gate_id": "CG4421_4_WEP_anchor", "claim": "WEP comparator anchor is carried forward without prediction claim", "passed": values["FVR4421_0_WEP_product_anchor"].get("current_status") == "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM", "valid_for_claim": False, "detail": "2.8e-15 is a comparator, not an MTS value."},
        {"gate_id": "CG4421_5_local_GR_Newton_claim", "claim": "single-phase owner proves local Newton/source coupling", "passed": False, "valid_for_claim": False, "detail": "universal hbar/measure, tau projectability and R_eq/Bzero remain unsigned."},
        {"gate_id": "CG4421_6_no_claim_outputs", "claim": "4421 generated no claim-ready row", "passed": no_claims, "valid_for_claim": False, "detail": "the checkpoint is a theorem-seed and finite-value intake gate."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4421_0",
            "decision": DECISION,
            "summary": "4421 confirms the promising route: MTS time-flow/traversal language and the psi action provide a real single phase-line seed. That is not enough to kill w_A yet. The missing parent signature is still universal hbar/quantum-statistical measure ownership, plus tau projectability and R_eq/B_zero same-current closure. The finite branch has a real WEP comparator anchor but no MTS Delta_w*tau or R_eq prediction value.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4421_0_best_result", "status": "MTS_TIME_FLOW_PHASE_LINE_SEED_FOUND", "detail": "MTS time-flow/action documents support the right theorem seed.", "valid_for_claim": False},
        {"status_id": "STAT4421_1_open_theorem", "status": "UNIVERSAL_HBAR_MEASURE_TAU_REQ_OPEN", "detail": "Need signed hbar/measure owner, tau projectability and R_eq/Bzero closure.", "valid_for_claim": False},
        {"status_id": "STAT4421_2_finite_branch", "status": "WEP_COMPARATOR_ANCHOR_ONLY_VALUES_MISSING", "detail": "2.8e-15 comparator retained; Delta_w*tau and R_eq values missing.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4421_0",
            "target": NEXT_TARGET,
            "objective": "Try to prove universal hbar/measure ownership from the single MTS action phase; if not, fill the first source-backed MTS prediction value for P_WEP or R_eq rather than just comparator anchors.",
            "derive_first": "show psi/MTS action phase fixes one hbar/measure for all ordinary matter representations and forbids species hbar_A/w_A.",
            "fallback": "source or bound Delta_w_TiPt*tau_WEP, R_eq dipole/quadrupole/compact-test moment, or B_zero_flux with units, path, projection and no-cancellation guard.",
            "avoid": "free phase-locking as proof; tau_WEP=1; total charge as profile equality; hidden species hbar; fitted G absorption.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], phase_out: Sequence[Mapping[str, str]], value_out: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 437 PPC4161 single phase action owner from MTS time-flow or first values

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4421 gets the useful result without overclaiming:

- MTS time-flow/traversal and the microscopic `psi` action supply a real single phase/action-line seed.
- That seed does **not** yet prove universal `hbar` or quantum-statistical measure ownership.
- A species `w_A` is now sharply interpreted as a species phase clock / `hbar_A` unless the parent forbids it.
- Free phase-lock distributions remain demoted; the owner must be a parent action/measure object.
- The finite branch carries one real WEP comparator anchor, but no MTS `Delta_w*tau_WEP` or `R_eq` value yet.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Single Phase Owner Gate

{table(phase_out)}

## First Value Gate

{table(value_out)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4421 - single phase action owner from MTS time-flow or first Delta-w/tau/R_eq values

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Converted MTS time-flow/traversal language into a precise single-phase owner seed.
- Kept universal `hbar`/measure and tau projectability unsigned.
- Preserved the WEP comparator anchor while refusing to call it an MTS prediction.
- Selected universal hbar/measure proof or first source-backed prediction row as the next target.

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
    fieldnames = rows[0].keys() if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "4421 shows MTS time-flow/traversal language and the microscopic psi action provide a real single phase/action-line seed for source coupling. It remains nonclaim because universal hbar/quantum-statistical measure ownership, tau projectability and R_eq/B_zero closure are not parent-signed; finite rows retain a WEP comparator anchor but no MTS Delta_w*tau or R_eq prediction value.",
            "current_evidence": "4421 source register, derivation rows, single-phase owner output, first-value output, claim gates, decision, status, next target and validation CSV.",
            "status": "mts_time_flow_phase_line_seed_hbar_measure_tau_req_open_nonclaim",
            "next_test": "Derive universal hbar/measure ownership from the MTS action phase, or fill the first source-backed MTS P_WEP/R_eq/B_zero prediction value.",
            "key_risk": "Treating phase-locking as owner proof, setting tau_WEP=1, conflating local clock time with phase/traversal time, or using comparator bounds as predictions.",
            "sector": "local_gr",
            "evidence": "4421 source register, derivation rows, single-phase owner output, first-value output, claim gates, decision, status, next target and validation CSV.",
            "next_action": "Derive universal hbar/measure ownership from the MTS action phase, or fill the first source-backed MTS P_WEP/R_eq/B_zero prediction value.",
            "risk": "Treating phase-locking as owner proof, setting tau_WEP=1, conflating local clock time with phase/traversal time, or using comparator bounds as predictions.",
        }
    )
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4421 local spine update: MTS time-flow gives the phase-line seed

4421 tests the Martin-style time-flow fork against the source-coupling problem. The useful result is real: MTS time as curvature-motion exchange plus the microscopic `psi` action gives a plausible single phase/action-line seed. That seed would kill species `hbar_A/w_A` only if the parent signs universal `hbar`/quantum-statistical measure ownership and keeps clock time, phase time and traversal/process time properly separated. The branch remains nonclaim; the finite side keeps the WEP comparator anchor but still lacks MTS-side `Delta_w*tau_WEP`, `R_eq` and `B_zero` values.
"""
    packet_section = f"""## 4421 packet update: single phase-line seed

`{PACKET_MARKER}`

Private packet result: the source-coupling owner has a concrete MTS route now. Time-flow/traversal language should be formalized as a single action phase line; then species source weights are species phase clocks unless parent-owned as measured matter data. Universal `hbar`/measure, tau projectability and `R_eq` equality remain open.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    phase = {row["row_id"]: row for row in rows_from(PHASE_OUTPUT)}
    values = {row["value_id"]: row for row in rows_from(VALUE_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in phase.values()) and not any(row.get("valid_for_claim") == "True" for row in values.values())
    checks = [
        ("VAL4421_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4421_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4421_2_time_phase_seed", phase["SPO4421_0_MTS_time_flow_seed"].get("current_status") == "MTS_TIME_PHASE_READY_HBAR_OWNER_OPEN", "MTS time-flow seed points to hbar owner gap"),
        ("VAL4421_3_action_seed", phase["SPO4421_1_action_principle_seed"].get("current_status") == "MTS_TIME_PHASE_READY_HBAR_OWNER_OPEN", "psi action seed points to hbar owner gap"),
        ("VAL4421_4_tau_bottleneck", phase["SPO4421_2_tau_lock_bottleneck"].get("current_status") in {"TIME_HBAR_READY_MATTER_PHASE_BUNDLE_OPEN", "DELTAW_ZERO_ROUTE_READY_TAU_PROJECTABILITY_OPEN", "MTS_TIME_PHASE_READY_HBAR_OWNER_OPEN"}, "tau/projectability bottleneck stays nonclaim"),
        ("VAL4421_5_future_contract", phase["SPO4421_3_future_single_phase_contract"].get("current_status") == "SINGLE_PHASE_ACTION_OWNER_CONTRACT_READY_NONCLAIM", "future single phase contract executable nonclaim"),
        ("VAL4421_6_WEP_anchor", values["FVR4421_0_WEP_product_anchor"].get("current_status") == "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM", "WEP comparator anchor retained without prediction"),
        ("VAL4421_7_no_claim_outputs", no_claims, "no generated row is claim-ready"),
        ("VAL4421_8_claim_gates", any(row["gate_id"] == "CG4421_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gates explicitly block public claim"),
        ("VAL4421_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-262"),
        ("VAL4421_10_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4421_11_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4421_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4421_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4421_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4421_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(PHASE_INPUT, phase_input_rows())
    write_csv(VALUE_INPUT, value_input_rows())
    write_csv(PHASE_OUTPUT, evaluate_phase_owner_rows(PHASE_INPUT))
    write_csv(VALUE_OUTPUT, evaluate_value_rows(VALUE_INPUT))
    phase_output = rows_from(PHASE_OUTPUT)
    value_output = rows_from(VALUE_OUTPUT)
    claim_gates = claim_gate_rows(phase_output, value_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), phase_output, value_output, claim_gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
