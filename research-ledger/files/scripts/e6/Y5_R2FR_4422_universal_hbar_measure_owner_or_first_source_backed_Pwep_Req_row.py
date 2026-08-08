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

from hbar_measure_value_gate import evaluate_owner_rows, evaluate_value_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
RAB_QUEUE = POST / "source-intake" / "rab-sector" / "acquisition-queue"
CORE = ROOT / "core-mts-framework"

CHECKPOINT = "4422"
CLAIM_ID = "L-263"
MARKER = "PPC4161_UNIVERSAL_HBAR_MEASURE_OWNER_OR_FIRST_SOURCE_BACKED_PWEP_REQ_ROW_4422"
PACKET_MARKER = "PPC4161_PACKET_UNIVERSAL_HBAR_MEASURE_OWNER_OR_FIRST_SOURCE_BACKED_PWEP_REQ_ROW_4422"
DECISION = "UNIVERSAL_HBAR_MEASURE_OWNER_NOT_PARENT_SIGNED_FIRST_VALUE_ROWS_STAGED_NONCLAIM"
NEXT_TARGET = "4423-Y5-R2FR-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"

FORMAL_PATH = FORMAL / "438-PPC4161-universal-hbar-measure-owner-or-first-source-backed-Pwep-Req-row.md"
DOC_PATH = POST / "4422-Y5-R2FR-universal-hbar-measure-owner-or-first-source-backed-Pwep-Req-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4422_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4422_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4422_DERIVATION_ROWS.csv"
OWNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4422_HBAR_MEASURE_OWNER_INPUT.csv"
OWNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4422_HBAR_MEASURE_OWNER_OUTPUT.csv"
VALUE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4422_FIRST_PREDICTION_VALUE_INPUT.csv"
VALUE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4422_FIRST_PREDICTION_VALUE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4422_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4422_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4422_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4422_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "hbar_measure_value_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4422_universal_hbar_measure_owner_or_first_source_backed_Pwep_Req_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4421 = SOURCE_DIR / "P8_Y5_R2FR_4421_NEXT_TARGET.csv"
FORMAL_437 = FORMAL / "437-PPC4161-single-phase-action-owner-from-MTS-time-flow-or-first-Deltaw-tau-Req-values.md"
CORE_TIME = CORE / "relativity" / "time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md"
CORE_FUNDAMENTAL = CORE / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
POST_2774 = POST / "2774-Y5-R2FR-parent-quantum-action-scale-normalization-or-WEP-tau-projection-under-AX1090.md"
POST_1389 = POST / "1389-Y5-R10-RAB-Delta-w-material-source-map-or-action-measure-owner-proof.md"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"
POST_3574 = POST / "3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md"
POST_1002 = POST / "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md"
RAB_COMMON_OWNER = RAB_QUEUE / "JR1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv"
RAB_ACTION = RAB_QUEUE / "JR1694_ACTION_MEASURE_OWNER_PROOF_GATE.csv"
RAB_AXIOM = RAB_QUEUE / "JR1698_OWNER_AXIOM_DERIVATION_TEST.csv"
RAB_TAU_DESCENT = RAB_QUEUE / "JR1733_DESCENT_LEMMA.csv"
RAB_TAU_LOCK = RAB_QUEUE / "JR1725_THEOREM_AUDIT.csv"


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
        {"source_id": "SRC4422_00_4421_next", "path": NEXT_4421, "needle": "4422-Y5-R2FR-universal-hbar-measure-owner-or-first-source-backed-Pwep-Req-row.md", "role": "4421 handoff."},
        {"source_id": "SRC4422_01_437_formal", "path": FORMAL_437, "needle": "MTS_TIME_PHASE_READY_HBAR_OWNER_OPEN", "role": "single phase-line seed and hbar gap."},
        {"source_id": "SRC4422_02_core_time", "path": CORE_TIME, "needle": "time is not an independent dimension", "role": "MTS time-flow primitive."},
        {"source_id": "SRC4422_03_core_action", "path": CORE_FUNDAMENTAL, "needle": "A_MTS", "role": "microscopic action/phase line source."},
        {"source_id": "SRC4422_04_common_owner", "path": RAB_COMMON_OWNER, "needle": "COM1687_4_measure_hbar", "role": "single hbar/path-integral measure gap."},
        {"source_id": "SRC4422_05_action_measure", "path": RAB_ACTION, "needle": "OWG1694_2_single_action_measure", "role": "action-measure owner proof gate."},
        {"source_id": "SRC4422_06_axiom_derivation", "path": RAB_AXIOM, "needle": "DER1698_2_single_density_owner", "role": "parent density/action-line owner countermodel."},
        {"source_id": "SRC4422_07_tau_descent", "path": RAB_TAU_DESCENT, "needle": "DCL1733_3_tau_projectable", "role": "tau projectability clause."},
        {"source_id": "SRC4422_08_tau_lock", "path": RAB_TAU_LOCK, "needle": "TSL1725_9_composite_theorem", "role": "one-generator lock clause."},
        {"source_id": "SRC4422_09_2774_hbar_wep", "path": POST_2774, "needle": "ASO2774_2_path_integral_measure", "role": "prior hbar/measure and WEP anchor audit."},
        {"source_id": "SRC4422_10_1389_material_map", "path": POST_1389, "needle": "AMP1389_6_theorem_if_signed", "role": "conditional owner theorem and material map."},
        {"source_id": "SRC4422_11_4378_req_moment", "path": POST_4378, "needle": "HARMONIC_NULL_MOMENT_ZERO_THEOREM", "role": "R_eq/topological moment route."},
        {"source_id": "SRC4422_12_3574_req_bzero", "path": POST_3574, "needle": "Pi_M J_H = J_M^top + dB_zero + R_eq", "role": "R_eq/B_zero exact decomposition."},
        {"source_id": "SRC4422_13_gate", "path": GATE_PATH, "needle": "def evaluate_owner_row", "role": "4422 hbar/value gate."},
        {"source_id": "SRC4422_14_generator", "path": GENERATOR_PATH, "needle": "UNIVERSAL_HBAR_MEASURE_OWNER_NOT_PARENT_SIGNED", "role": "4422 generator."},
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
            "derivation_id": "UHM4422_0_phase_line_not_hbar_owner",
            "claim": "A single MTS phase/action line is not by itself a universal hbar/measure theorem.",
            "derivation": "The psi/MTS action can define one phase variable, but a path weight exp(i S/hbar) still needs a parent-owned hbar and a quantum/statistical measure. Without those owners the same classical phase line permits exp(i sum_A S_A/hbar_A) or exp(i sum_A w_A S_A/hbar_parent).",
            "consequence": "4421's seed is real, but it cannot yet kill species source weights.",
            "status": "PHASE_LINE_READY_HBAR_MEASURE_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "UHM4422_1_exact_owner_contract",
            "claim": "If one parent hbar and one species-blind measure own all ordinary matter paths, species hbar_A/w_A is illegal.",
            "derivation": "Assume ordinary matter is represented by one connected parent matter functor with path weight exp(i S_ord/hbar_parent), one measure mu_parent, species-blind Jacobian, variation-before-readout, and no source-only coefficient object. Then replacing S_A by w_A S_A is equivalent to adding a species phase unit hbar_A=hbar_parent/w_A, which has no parent slot.",
            "consequence": "This is the cleanest theorem route to Delta_w_A=0, but it is conditional until the parent signs every premise.",
            "status": "EXACT_CONDITIONAL_THEOREM_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "UHM4422_2_countermodel_survives",
            "claim": "The countermodel survives if the parent does not own the measure.",
            "derivation": "A theory can keep the same isolated classical Euler-Lagrange equations while changing Hilbert source normalization and quantum/statistical weights through exp(i sum_A w_A S_A/hbar_parent), a species Jacobian J_A, or a source-only measure factor.",
            "consequence": "Classical EOM rescaling, covariance and a nice action line are not enough; the coupling problem is genuinely the measure/action-scale problem.",
            "status": "COUNTERMODEL_SURVIVES_WITHOUT_PARENT_MEASURE_OWNER",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "UHM4422_3_tau_req_dependency",
            "claim": "Even with hbar/measure ownership, local-GR scoring still needs tau and R_eq/B_zero closure.",
            "derivation": "WEP/PPN/Newton comparisons require the same observed time/source generator and the same Hilbert/current profile. Therefore tau projectability and Pi_M J_H=J_M^top+dB_zero+R_eq with R_eq/B_zero silent or bounded remain independent gates.",
            "consequence": "Universal hbar/measure would close the species source-weight leg, not the whole local branch by itself.",
            "status": "HBAR_ROUTE_DEPENDS_ON_TAU_REQ_BZERO",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "UHM4422_4_first_value_audit",
            "claim": "No source-backed MTS-side P_WEP or R_eq prediction value is found in the current local chain.",
            "derivation": "The corpus contains comparator anchors and normal forms, but the MTS-side numbers still require parent coefficients, projection functionals, material/source maps and official numeric sources.",
            "consequence": "Finite rows are staged as smoke/value contracts, not as evidence.",
            "status": "FIRST_VALUE_ROWS_STAGED_VALUES_MISSING_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def owner_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "HMO4422_0_phase_seed_from_4421",
            "branch": "MTS_time_flow_phase_line",
            "single_phase_line": True,
            "universal_hbar_parent": False,
            "common_path_integral_measure": False,
            "species_blind_measure_jacobian": False,
            "ordinary_matter_same_phase_bundle": False,
            "no_species_hbar_A": False,
            "action_density_line_owner": False,
            "hbar_measure_current_owner": False,
            "tau_projectable": False,
            "Req_route_ready": False,
            "source_path": str(FORMAL_437),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "4421 supplies the phase line seed only; hbar/measure ownership remains open.",
        },
        {
            "row_id": "HMO4422_1_prior_measure_owner_gap",
            "branch": "common_action_measure_current_owner_audit",
            "single_phase_line": True,
            "universal_hbar_parent": False,
            "common_path_integral_measure": False,
            "species_blind_measure_jacobian": False,
            "ordinary_matter_same_phase_bundle": True,
            "no_species_hbar_A": False,
            "action_density_line_owner": False,
            "hbar_measure_current_owner": False,
            "tau_projectable": False,
            "Req_route_ready": False,
            "source_path": str(RAB_COMMON_OWNER),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Prior owner audit names exactly this gap: single hbar/path-integral/statistical measure owner not derived.",
        },
        {
            "row_id": "HMO4422_2_tau_req_bottleneck_after_owner",
            "branch": "tau_projectability_and_Req_same_current_dependency",
            "single_phase_line": True,
            "universal_hbar_parent": True,
            "common_path_integral_measure": True,
            "species_blind_measure_jacobian": True,
            "ordinary_matter_same_phase_bundle": True,
            "no_species_hbar_A": True,
            "action_density_line_owner": True,
            "hbar_measure_current_owner": True,
            "tau_projectable": False,
            "Req_route_ready": False,
            "source_path": str(RAB_TAU_DESCENT),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Hypothetical owner closes source weights but tau projectability and R_eq/B_zero remain unsigned.",
        },
        {
            "row_id": "HMO4422_3_future_universal_hbar_measure_contract",
            "branch": "future_parent_hbar_measure_owner_contract",
            "single_phase_line": True,
            "universal_hbar_parent": True,
            "common_path_integral_measure": True,
            "species_blind_measure_jacobian": True,
            "ordinary_matter_same_phase_bundle": True,
            "no_species_hbar_A": True,
            "action_density_line_owner": True,
            "hbar_measure_current_owner": True,
            "tau_projectable": True,
            "Req_route_ready": True,
            "source_path": str(RAB_ACTION),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact future contract only. It becomes claimable only if the parent action signs every clause.",
        },
    ]


def value_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "value_id": "PV4422_0_PWEP_anchor_not_prediction",
            "quantity": "P_WEP_relative_source_weight",
            "arena": "MICROSCOPE_WEP",
            "normal_form": "P_WEP=abs(Delta_w_TiPt*tau_WEP)",
            "predicted_value": "MISSING_DELTA_W_TIPT_TIMES_TAU_WEP",
            "prediction_source": str(FORMAL_437),
            "projection_source": str(POST_2774),
            "comparator_value": "2.8e-15",
            "comparator_source": str(POST_2774),
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_COEFFICIENT_SOURCE_PATH",
            "official_numeric_source": "MISSING_OFFICIAL_MICROSCOPE_BOUND_SOURCE_PATH",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Comparator anchor only; the MTS-side product remains missing.",
        },
        {
            "value_id": "PV4422_1_Req_harmonic_moment_schema",
            "quantity": "R_eq_harmonic_moment",
            "arena": "Newton_PPN_orbital_source_profile",
            "normal_form": "delta a_l/a_N <= E_l^top*(R/r)^l",
            "predicted_value": "MISSING_R_EQ_M1M_M2M_SOURCE_PROFILE_VALUE",
            "prediction_source": str(POST_4378),
            "projection_source": "MISSING_ARENA_PROJECTION_SOURCE_PATH",
            "comparator_value": "SCHEMA_ARENA_DELTA_N_OR_PPN_BOUND_REQUIRED",
            "comparator_source": str(POST_4378),
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_REQ_COEFFICIENT_SOURCE_PATH",
            "official_numeric_source": "MISSING_OFFICIAL_PPN_OR_ORBIT_BOUND_SOURCE_PATH",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Normal form exists; no numeric topological moment or comparator bound is sourced.",
        },
        {
            "value_id": "PV4422_2_Bzero_flux_schema",
            "quantity": "B_zero_flux",
            "arena": "source_flux_Gdot_radial_Newton",
            "normal_form": "epsilon_Bzero_flux=abs(int_boundary dB_zero)/abs(M_eff)",
            "predicted_value": "MISSING_B_ZERO_FLUX_THEOREM_OR_BOUND",
            "prediction_source": str(POST_3574),
            "projection_source": "MISSING_SOURCE_WORLDTUBE_BOUNDARY_PROJECTION_SOURCE_PATH",
            "comparator_value": "SCHEMA_GDOT_RADIAL_OR_ORBIT_BOUND_REQUIRED",
            "comparator_source": str(POST_3574),
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_BZERO_COEFFICIENT_SOURCE_PATH",
            "official_numeric_source": "MISSING_OFFICIAL_GDOT_OR_ORBIT_BOUND_SOURCE_PATH",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "B_zero residual normal form exists; no source-backed flux value is present.",
        },
    ]


def claim_gate_rows(owner_out: Sequence[Mapping[str, str]], value_out: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    owners = {row["row_id"]: row for row in owner_out}
    values = {row["value_id"]: row for row in value_out}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owner_out) and not any(
        row.get("valid_for_claim") == "True" for row in value_out
    )
    return [
        {"gate_id": "CG4422_0_phase_line_retained", "claim": "4421 phase-line seed is retained", "passed": owners["HMO4422_0_phase_seed_from_4421"].get("current_status") == "PHASE_LINE_READY_HBAR_MEASURE_OPEN", "valid_for_claim": False, "detail": "seed survives but does not become hbar ownership."},
        {"gate_id": "CG4422_1_measure_countermodel_alive", "claim": "species hbar_A/w_A countermodel is killed", "passed": False, "valid_for_claim": False, "detail": "countermodel survives until parent hbar/measure owner is signed."},
        {"gate_id": "CG4422_2_future_contract_executable", "claim": "universal hbar/measure contract is executable", "passed": owners["HMO4422_3_future_universal_hbar_measure_contract"].get("current_status") == "UNIVERSAL_HBAR_MEASURE_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "all clauses can be represented, but input_valid=false keeps it nonclaim."},
        {"gate_id": "CG4422_3_tau_req_dependency", "claim": "hbar owner alone closes local GR", "passed": False, "valid_for_claim": False, "detail": "tau projectability and R_eq/B_zero route still need derivation or finite values."},
        {"gate_id": "CG4422_4_PWEP_anchor", "claim": "P_WEP row has an MTS prediction value", "passed": values["PV4422_0_PWEP_anchor_not_prediction"].get("current_status") == "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM", "valid_for_claim": False, "detail": "2.8e-15 remains a comparator anchor, not an MTS prediction."},
        {"gate_id": "CG4422_5_Req_schema", "claim": "R_eq row has a source-backed value", "passed": values["PV4422_1_Req_harmonic_moment_schema"].get("current_status") == "PREDICTION_SCHEMA_READY_VALUES_MISSING_NONCLAIM", "valid_for_claim": False, "detail": "normal form exists; numeric moment/projection/bound do not."},
        {"gate_id": "CG4422_6_no_claim_outputs", "claim": "4422 generated no claim-ready row", "passed": no_claims, "valid_for_claim": False, "detail": "checkpoint is a theorem gate plus first-value schema."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4422_0",
            "decision": DECISION,
            "summary": "4422 tries the derivation route and gets a sharper result: one MTS phase/action line is a real route, but universal hbar/measure ownership is not forced by that line alone. The exact conditional theorem is now explicit: one parent hbar, one species-blind path/statistical measure, one ordinary-matter action-density owner, no source-only coefficient slot, and tau/R_eq closure would kill species hbar_A/w_A. Current corpus does not parent-sign those clauses. The finite fallback rows are staged, but P_WEP, R_eq and B_zero still lack MTS-side numeric/source-backed predictions.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4422_0_best_result", "status": "EXACT_CONDITIONAL_HBAR_MEASURE_OWNER_THEOREM_READY", "detail": "The theorem form is clean: species hbar_A/w_A is illegal only under one parent hbar/measure/action-density owner.", "valid_for_claim": False},
        {"status_id": "STAT4422_1_missing_parent_signature", "status": "PARENT_HBAR_MEASURE_OWNER_NOT_SIGNED", "detail": "Prior audits still list the single hbar/path-integral/statistical measure owner as not derived.", "valid_for_claim": False},
        {"status_id": "STAT4422_2_first_values", "status": "PWEP_REQ_BZERO_VALUES_STAGED_NONCLAIM", "detail": "Rows exist for first finite values, but parent coefficients, projections and official numeric sources remain missing.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4422_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive the action-density line/measure owner from parent MTS syntax; if it fails, fill the first actual source-backed P_WEP or R_eq value row.",
            "derive_first": "prove ordinary matter has one parent action-density line and species-blind measure/Hom structure, so hbar_A/w_A has no object-language slot.",
            "fallback": "fill a real MTS-side value for Delta_w_TiPt*tau_WEP, an R_eq dipole/quadrupole/topological moment, or B_zero flux with parent coefficients, projection source and official comparator source.",
            "avoid": "declaring the phase line itself to be hbar ownership; using comparator anchors as predictions; setting tau_WEP=1; hiding source weights in fitted G.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], owner_out: Sequence[Mapping[str, str]], value_out: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 438 PPC4161 universal hbar measure owner or first source-backed P_WEP/R_eq row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4422 makes the bottleneck more mathematical rather than just repeating that something is missing:

- A single MTS phase/action line is a real route, but it is not automatically a universal `hbar`/measure theorem.
- The exact owner theorem is now explicit: one parent `hbar`, one species-blind path/statistical measure, one ordinary-matter action-density owner, no source-only coefficient slot, plus tau/`R_eq` closure.
- If that owner theorem is parent-signed, species `hbar_A` / `w_A` is illegal rather than fitted away.
- Without it, the countermodel `exp(i sum_A w_A S_A/hbar_parent)` still changes source normalization and quantum/statistical weights while preserving isolated classical EOM form.
- First finite value rows are staged for `P_WEP`, `R_eq`, and `B_zero`, but they remain nonclaim because MTS-side prediction values are not source-backed yet.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Hbar / Measure Owner Gate

{table(owner_out)}

## First Prediction Value Gate

{table(value_out)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4422 - universal hbar/measure owner or first source-backed P_WEP/R_eq row

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Converted the universal `hbar`/measure issue into an exact executable theorem gate.
- Proved the useful conditional: `hbar_A/w_A` is forbidden only if one parent `hbar`, measure, action-density line and species-blind Jacobian are signed.
- Kept the surviving countermodel explicit, so the theory cannot accidentally smuggle coupling closure through classical EOM rescaling.
- Staged first finite prediction-value rows for `P_WEP`, `R_eq`, and `B_zero` while keeping them nonclaim.

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
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4422 derives the exact conditional universal hbar/measure owner theorem: species hbar_A/w_A is illegal only if one parent hbar, one species-blind path/statistical measure, one ordinary-matter action-density owner, no source-only coefficient slot, and tau/R_eq closure are parent-signed. Current MTS has not signed those clauses, and first finite P_WEP/R_eq/B_zero value rows remain nonclaim.",
        "current_evidence": "4422 source register, derivation rows, hbar-measure owner output, first prediction-value output, claim gates, decision, status, next target and validation CSV.",
        "status": "conditional_hbar_measure_owner_theorem_ready_parent_unsigned_first_values_staged_nonclaim",
        "next_test": "Derive the action-density line/measure owner from parent MTS syntax, or fill a real source-backed MTS P_WEP/R_eq/B_zero prediction value.",
        "key_risk": "Promoting a phase line into hbar ownership; treating comparator anchors as predictions; using classical EOM rescaling to erase source weights; hiding source weights in fitted G.",
        "sector": "local_gr",
        "evidence": "4422 source register, derivation rows, hbar-measure owner output, first prediction-value output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Derive the action-density line/measure owner from parent MTS syntax, or fill a real source-backed MTS P_WEP/R_eq/B_zero prediction value.",
        "risk": "Promoting a phase line into hbar ownership; treating comparator anchors as predictions; using classical EOM rescaling to erase source weights; hiding source weights in fitted G.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4422 local spine update: hbar/measure owner theorem made exact

4422 takes the source-coupling bottleneck seriously. The single MTS phase/action line survives, but it does not itself derive universal `hbar` or the quantum/statistical measure. The exact theorem now says species `hbar_A/w_A` is forbidden only if the parent owns one `hbar`, one species-blind measure/Jacobian, one ordinary-matter action-density line, no source-only coefficient slot, and the tau/`R_eq` source route. This is a cleaner roof ladder, not a roof claim: the parent signatures are still unsigned and the first finite `P_WEP`/`R_eq`/`B_zero` value rows are staged nonclaim.
"""
    packet_section = f"""## 4422 packet update: universal hbar/measure contract

`{PACKET_MARKER}`

Private packet result: the coupling gap is now sharply localized. MTS needs a parent action-density/measure owner, not another verbal phase-lock. If that owner closes, species source weights become illegal phase-clock replicas. If not, the finite branch must fill source-backed `P_WEP`, `R_eq`, or `B_zero` values.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    owners = {row["row_id"]: row for row in rows_from(OWNER_OUTPUT)}
    values = {row["value_id"]: row for row in rows_from(VALUE_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owners.values()) and not any(row.get("valid_for_claim") == "True" for row in values.values())
    checks = [
        ("VAL4422_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4422_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4422_2_phase_seed_status", owners["HMO4422_0_phase_seed_from_4421"].get("current_status") == "PHASE_LINE_READY_HBAR_MEASURE_OPEN", "phase line retained without hbar owner promotion"),
        ("VAL4422_3_prior_gap_status", owners["HMO4422_1_prior_measure_owner_gap"].get("current_status") == "PHASE_LINE_READY_HBAR_MEASURE_OPEN", "prior measure owner gap remains active"),
        ("VAL4422_4_tau_req_status", owners["HMO4422_2_tau_req_bottleneck_after_owner"].get("current_status") == "HBAR_MEASURE_OWNER_READY_TAU_REQ_OPEN", "tau/R_eq dependency is separated from hbar owner"),
        ("VAL4422_5_future_contract_status", owners["HMO4422_3_future_universal_hbar_measure_contract"].get("current_status") == "UNIVERSAL_HBAR_MEASURE_CONTRACT_READY_NONCLAIM", "future hbar/measure owner contract executable nonclaim"),
        ("VAL4422_6_PWEP_anchor_status", values["PV4422_0_PWEP_anchor_not_prediction"].get("current_status") == "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM", "P_WEP comparator anchor is not promoted to prediction"),
        ("VAL4422_7_Req_schema_status", values["PV4422_1_Req_harmonic_moment_schema"].get("current_status") == "PREDICTION_SCHEMA_READY_VALUES_MISSING_NONCLAIM", "R_eq schema staged without value claim"),
        ("VAL4422_8_Bzero_schema_status", values["PV4422_2_Bzero_flux_schema"].get("current_status") == "PREDICTION_SCHEMA_READY_VALUES_MISSING_NONCLAIM", "B_zero schema staged without value claim"),
        ("VAL4422_9_no_claim_outputs", no_claims, "no generated row is claim-ready"),
        ("VAL4422_10_claim_gates", any(row["gate_id"] == "CG4422_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gates explicitly block public claim"),
        ("VAL4422_11_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-263"),
        ("VAL4422_12_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4422_13_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4422_14_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4422_15_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4422_16_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4422_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(OWNER_INPUT, owner_input_rows())
    write_csv(VALUE_INPUT, value_input_rows())
    write_csv(OWNER_OUTPUT, evaluate_owner_rows(OWNER_INPUT))
    write_csv(VALUE_OUTPUT, evaluate_value_rows(VALUE_INPUT))
    owner_output = rows_from(OWNER_OUTPUT)
    value_output = rows_from(VALUE_OUTPUT)
    claim_gates = claim_gate_rows(owner_output, value_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), owner_output, value_output, claim_gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
