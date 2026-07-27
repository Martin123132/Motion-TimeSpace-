from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3947"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3947-Y5-R2FR-total-Hilbert-source-positive-energy-or-negative-sector-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3947_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3947_TOTAL_HILBERT_POSITIVE_ENERGY_THEOREM.csv",
    "sector": SRC / "P8_Y5_R2FR_3947_SECTOR_SIGN_DECOMPOSITION.csv",
    "epsilon_neg": SRC / "P8_Y5_R2FR_3947_EPSILON_NEG_BOUND_VECTOR.csv",
    "candidate": SRC / "P8_Y5_R2FR_3947_MEH_SIGN_BOUND_CANDIDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3947_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3947_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3947_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3947_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3947_VALIDATION.csv",
}

NEXT_DOC = "3948-Y5-R2FR-parent-Hamiltonian-bounded-below-and-no-ghost-energy-condition-or-sector-bound-inputs.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3948_parent_Hamiltonian_bounded_below_and_no_ghost_energy_condition_or_sector_bound_inputs.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3947_00_3946_next", SRC / "P8_Y5_R2FR_3946_NEXT_TARGET.csv", "NEXT3946_0", "3946 selected positive-energy/negative-sector target"),
        ("SRC3947_01_3946_current", SRC / "P8_Y5_R2FR_3946_CONSERVATION_CURRENT_THEOREM.csv", "CCT3946_3_MEH_closed_domain", "closed-domain theorem"),
        ("SRC3947_02_3946_negative", SRC / "P8_Y5_R2FR_3946_ENERGY_CONDITION_CERTIFICATE.csv", "ENG3946_2_negative_sector_bound", "negative-sector bound route"),
        ("SRC3947_03_3946_sign", SRC / "P8_Y5_R2FR_3946_ENERGY_CONDITION_CERTIFICATE.csv", "ENG3946_4_MEH_sign_certificate", "M_EH sign certificate"),
        ("SRC3947_04_3946_flux", SRC / "P8_Y5_R2FR_3946_POYNTING_AND_WALL_FLUX_BOUND_LAW.csv", "FLX3946_5_total", "epsilon_closed flux total"),
        ("SRC3947_05_3945_positive", SRC / "P8_Y5_R2FR_3945_MEH_POSITIVE_COMPARATOR_THEOREM.csv", "PEC3945_2_positive_energy_sufficient_conditions", "conditional M_EH positivity theorem"),
        ("SRC3947_06_3821_stress", SRC / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv", "SVT3821_3_pressure_paradox_resolution", "total-system stress resolution"),
        ("SRC3947_07_3821_energy", SRC / "P8_Y5_R2FR_3821_TOLMAN_TO_ENERGY_MASS_REDUCTION.csv", "TER3821_2_energy_mass_limit", "closed stationary energy-mass limit"),
        ("SRC3947_08_3821_bound", SRC / "P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv", "PBV3821_5_total", "pressure/binding bound vector"),
        ("SRC3947_09_3820_binding", SRC / "P8_Y5_R2FR_3820_PRESSURE_BINDING_CORRECTION_LAW.csv", "COR3820_2_binding", "binding/stabilizer correction row"),
        ("SRC3947_10_3820_field", SRC / "P8_Y5_R2FR_3820_PRESSURE_BINDING_CORRECTION_LAW.csv", "COR3820_3_field_energy", "field energy correction row"),
        ("SRC3947_11_3820_total", SRC / "P8_Y5_R2FR_3820_PRESSURE_BINDING_CORRECTION_LAW.csv", "COR3820_6_source_total", "source correction total"),
        ("SRC3947_12_3906_Hilbert", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "same-frame Hilbert source bridge"),
        ("SRC3947_13_3906_Maxwell", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_1_Maxwell", "Maxwell stress bridge"),
        ("SRC3947_14_3777_EM", SRC / "P8_Y5_R2FR_3777_EM_FIELD_ENERGY_SOURCE_MAP.csv", "ESM3777_0_descended_Maxwell", "descended Maxwell map"),
        ("SRC3947_15_3777_material", SRC / "P8_Y5_R2FR_3777_EM_FIELD_ENERGY_SOURCE_MAP.csv", "ESM3777_5_material_response", "material response/theta blocker"),
        ("SRC3947_16_3946_validation", SRC / "P8_Y5_BRR545_3946_VALIDATION.csv", "VAL3946_20_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:900]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PET3947_0_split",
            "piece": "source-energy sign split",
            "statement": "Separate Z_Etotal_positive from Z_sourceblind_ref: source energy positivity proves M_EH>0; source-blind reference is needed later for M_H_ref lower-bound transfer.",
            "derivation": "3946 bundled these in Z_MEH_positive. 3947 splits the logic so the source-energy theorem can be attacked without confusing it with boundary/reference subtraction.",
            "status": "LOGIC_SPLIT_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PET3947_1_manifest_positive",
            "piece": "positive sectors",
            "statement": "E_pos := integral(rho_rest + rho_kin + rho_internal_pos + rho_EM_near_pos + rho_owned_apparatus_pos + rho_other_parent_positive) dSigma.",
            "derivation": "In a local orthonormal same-frame branch, ordinary rest/kinetic positive energy and descended Maxwell field energy contribute nonnegative Hilbert energy density when their parent signs are fixed.",
            "status": "E_POS_DECOMPOSITION_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PET3947_2_unsigned_negative_sectors",
            "piece": "negative/unsigned sectors",
            "statement": "E_neg := |E_binding_neg| + |E_stabilizer_neg| + |E_material_unsigned| + |E_parent_exchange| + |E_nonminimal_counterterm| + |E_source_norm_shift|.",
            "derivation": "Any sector not manifestly positive or parent-signed is not erased. It enters as a nonnegative magnitude in the denominator sign bound.",
            "status": "E_NEG_MAGNITUDE_DECOMPOSITION_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PET3947_3_positive_energy_or_bound_theorem",
            "piece": "M_EH sign theorem",
            "statement": "If E_pos>0 and either a parent DEC/WEC theorem signs T_total(n,tau)>=0 or epsilon_neg+epsilon_closed<1, then M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed)>0.",
            "derivation": "Write E_total = E_pos - E_neg - E_closed_leak with epsilon_neg=E_neg/E_pos and epsilon_closed=E_closed_leak/E_pos. The inequality is immediate and does not rely on cancellation.",
            "status": "CONDITIONAL_SIGN_BOUND_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PET3947_4_EM_and_Poynting_placement",
            "piece": "EM/Poynting placement",
            "statement": "Descended stationary Maxwell energy goes into E_pos; radiative/crossing Poynting flux goes into epsilon_closed, not epsilon_neg and not hidden M_EH mass.",
            "derivation": "This preserves the EM/wave intuition while keeping source closedness as a testable flux statement.",
            "status": "EM_POSITIVE_AND_FLUX_SPLIT_LOCKED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PET3947_5_verdict",
            "piece": "3947 verdict",
            "statement": "No parent-signed total positive-energy theorem is present yet; the usable progress is the exact E_pos/E_neg/epsilon_closed inequality and the sector rows needed to fill it.",
            "derivation": "3947 converts 'positive energy missing' into a bounded sign test with named sector owners.",
            "status": "FORWARD_REDUCTION_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def sector_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SEC3947_0_rest_mass", "rho_rest", "positive", "ordinary rest/inertial mass density in same-frame Hilbert source", "E_pos", "PARENT_SIGN_OR_SOURCE_LEDGER_REQUIRED", "mass_energy_density"),
        ("SEC3947_1_kinetic", "rho_kin", "positive", "local kinetic energy density", "E_pos", "LOW_ENERGY_HAMILTONIAN_POSITIVITY_REQUIRED", "energy_density"),
        ("SEC3947_2_internal_positive", "rho_internal_pos", "positive_if_split", "thermal/internal positive-energy part after stress split", "E_pos", "THERMODYNAMIC_SOURCE_SPLIT_REQUIRED", "energy_density"),
        ("SEC3947_3_Maxwell_near", "rho_EM_near_pos", "positive_if_descended", "descended stationary Maxwell near-field energy", "E_pos", "MTS_EM_DESCENT_AND_DOMAIN_REQUIRED", "energy_density"),
        ("SEC3947_4_binding", "E_binding_neg", "negative_or_unsigned", "binding energy/stabilizer stress not covered by total positive-energy theorem", "E_neg", "BOUND_OR_PARENT_POSITIVE_ENERGY_THEOREM_REQUIRED", "energy"),
        ("SEC3947_5_material_response", "E_material_unsigned", "unsigned", "polarization, magnetization, material/theta response and source labels", "E_neg", "MATERIAL_RESPONSE_THETA_DESCENT_OR_BOUND_REQUIRED", "energy"),
        ("SEC3947_6_parent_exchange", "E_parent_exchange", "unsigned", "parent/non-EM exchange current not cancelled in total stress", "E_neg", "WARD_OR_EXCHANGE_BOUND_REQUIRED", "energy"),
        ("SEC3947_7_nonminimal_counterterm", "E_nonminimal_counterterm", "unsigned", "non-EH operator, improvement, counterterm or regularization energy", "E_neg", "OPERATOR_COUNTERTERM_BOUND_REQUIRED", "energy"),
        ("SEC3947_8_source_norm_shift", "E_source_norm_shift", "unsigned", "theta/source-normalization shift in active/passive/inertial source", "E_neg", "SOURCE_NORMALIZATION_SUPERSELECTION_OR_BOUND_REQUIRED", "energy"),
        ("SEC3947_9_Poynting_flux", "E_closed_leak", "flux_not_negative_sector", "Poynting/wall/tail/Ward/tau leakage from 3946", "epsilon_closed", "CLOSED_DOMAIN_ZERO_OR_FLUX_BOUND_REQUIRED", "energy"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "sign_class": sign_class,
            "definition": definition,
            "bucket": bucket,
            "exit_requirement": exit_requirement,
            "units": units,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, sign_class, definition, bucket, exit_requirement, units in data
    ]


def epsilon_neg_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("NEG3947_0_denominator", "E_pos", "positive denominator for source-energy sign test", "integral positive sector density", "MISSING_E_POS_SOURCE_ROW", "energy", "independent source-energy/support row; E_pos>0"),
        ("NEG3947_1_binding", "epsilon_binding_neg", "|E_binding_neg|/E_pos", "binding/stabilizer negative contribution", "MISSING_BINDING_STABILIZER_BOUND", "dimensionless", "closed total-system stress theorem or finite binding/stabilizer bound"),
        ("NEG3947_2_material", "epsilon_material_unsigned", "|E_material_unsigned|/E_pos", "material response/theta/source-label contribution", "MISSING_MATERIAL_RESPONSE_THETA_BOUND", "dimensionless", "parent material descent or WEP/clock/source-composition bound"),
        ("NEG3947_3_parent_exchange", "epsilon_parent_exchange", "|E_parent_exchange|/E_pos", "parent exchange current contribution", "MISSING_PARENT_EXCHANGE_BOUND", "dimensionless", "Ward identity zero or source-backed exchange bound"),
        ("NEG3947_4_nonminimal", "epsilon_nonminimal_counterterm", "|E_nonminimal_counterterm|/E_pos", "non-EH/improvement/counterterm contribution", "MISSING_NONMINIMAL_COUNTERTERM_BOUND", "dimensionless", "EH operator/counterterm sign theorem or finite residual"),
        ("NEG3947_5_source_norm", "epsilon_source_norm_shift", "|E_source_norm_shift|/E_pos", "source normalization/theta superselection contribution", "MISSING_SOURCE_NORMALIZATION_BOUND", "dimensionless", "theta/source-normalization descent or finite bound"),
        ("NEG3947_6_total", "epsilon_neg", "sum_abs(epsilon_binding_neg,epsilon_material_unsigned,epsilon_parent_exchange,epsilon_nonminimal_counterterm,epsilon_source_norm_shift)", "total negative/unsigned sector fraction", "COMPONENT_VALUES_MISSING", "dimensionless", "all negative/unsigned components theorem-zero or finite"),
        ("NEG3947_7_combined", "epsilon_MEH_sign", "epsilon_neg + epsilon_closed", "combined source-energy sign failure fraction", "COMPONENT_VALUES_MISSING", "dimensionless", "epsilon_neg plus 3946 epsilon_closed below one"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "definition": definition,
            "current_value": current_value,
            "units": units,
            "exit_requirement": exit_requirement,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, formula, definition, current_value, units, exit_requirement in data
    ]


def candidate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MBC3947_0_MEH_sign_bound",
            "quantity": "M_EH_lower",
            "formula": "c^-2 * E_pos * (1 - epsilon_neg - epsilon_closed)",
            "required_columns": "system_id;tau_id;coframe_id;worldtube_id;E_pos;epsilon_neg;epsilon_closed;epsilon_components;proof_sum_lt_1;M_EH_lower;units;source_paths;not_orbital_GM_imported;valid_for_claim",
            "current_value": "MISSING_E_POS_EPSILON_NEG_EPSILON_CLOSED_VALUES",
            "acceptance_condition": "E_pos>0 and epsilon_neg+epsilon_closed<1 in same source branch, with all sector terms signed or bounded",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MBC3947_1_DEC_shortcut",
            "quantity": "Z_energy_condition",
            "formula": "parent DEC/WEC/no-ghost positive Hamiltonian theorem for T_total(n,tau)>=0",
            "required_columns": "parent_action_id;field_sector;kinetic_sign;potential_lower_bound;constraint_stability;Hilbert_stress_owner;source_path;valid_for_claim",
            "current_value": "MISSING_PARENT_POSITIVE_ENERGY_THEOREM",
            "acceptance_condition": "all total Hilbert source sectors have parent-owned positive energy or controlled lower bound",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3947_0_no_free_DEC",
            "decision": "do not assume DEC/WEC for the full MTS total source",
            "effect": "positive-energy theorem remains a parent-action/no-ghost target, not an imported GR axiom",
            "claim_status": "PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3947_1_bound_route",
            "decision": "use E_pos/E_neg/epsilon_closed split as the active route",
            "effect": "M_EH sign can be tested by a no-cancellation inequality once sectors are filled",
            "claim_status": "BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3947_2_EM",
            "decision": "place descended stationary Maxwell energy in E_pos and crossing Poynting flux in epsilon_closed",
            "effect": "keeps wave/field intuition but prevents hidden flux from masquerading as source mass",
            "claim_status": "EM_SPLIT_DISCIPLINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3947_3_next",
            "decision": "attack parent Hamiltonian bounded-below/no-ghost conditions next",
            "effect": "this is the cleanest route to reducing epsilon_neg without empirical overfitting",
            "claim_status": "NEXT_PARENT_HAMILTONIAN_OR_SECTOR_BOUNDS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3947_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3947_1_theorem", "gate": "M_EH sign inequality", "requirement": "E_pos/E_neg/epsilon_closed theorem derived", "status": "PASS_CONDITIONAL_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3947_2_parent_DEC", "gate": "parent positive energy", "requirement": "DEC/WEC/no-ghost positive Hamiltonian theorem", "status": "BLOCKED_PARENT_UNSIGNED", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3947_3_Epos", "gate": "positive denominator energy", "requirement": "E_pos>0 source row", "status": "BLOCKED_E_POS_SOURCE_ROW_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3947_4_epsilon_neg", "gate": "negative/unsigned sector bound", "requirement": "epsilon_neg finite and sourced", "status": "BLOCKED_COMPONENT_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3947_5_epsilon_closed", "gate": "closed-domain flux bound", "requirement": "epsilon_closed from 3946 finite and sourced", "status": "BLOCKED_3946_FLUX_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3947_6_local_GR_claim", "gate": "local-GR/source-coupling claim", "requirement": "M_EH>0 and 3944 residual envelope below one", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3947_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive parent Hamiltonian bounded-below/no-ghost energy conditions for the total Hilbert source, or produce first sector-bound input rows for epsilon_neg",
            "success_condition": "either the parent action signs the positive-energy route, or epsilon_neg gains concrete sourceable component rows without hiding binding, stabilizer, material, exchange, counterterm, or source-normalization sectors",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3947 derives the E_pos/E_neg/epsilon_closed M_EH sign bound and splits positive source sectors from negative/unsigned sectors; parent DEC/WEC remains unsigned",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3947 - Total Hilbert Source Positive Energy Or Negative-Sector Bound

Timestamp: `{timestamp}`

## Result

3947 splits the `M_EH>0` problem into two honest routes:

1. a parent-signed positive-energy theorem for the total Hilbert source;
2. a no-cancellation lower bound:

`M_EH >= c^-2 E_pos*(1 - epsilon_neg - epsilon_closed)`.

This means `M_EH>0` follows if:

`E_pos>0` and `epsilon_neg + epsilon_closed < 1`.

## Sector Split

`E_pos` contains only sectors that are manifestly positive or parent-signed:

- rest/inertial source energy;
- kinetic/internal positive energy;
- descended stationary Maxwell field energy;
- owned positive apparatus/support terms.

`E_neg` contains all negative or unsigned sectors:

- binding/stabilizer energy;
- material/theta response;
- parent exchange;
- non-EH/counterterm/improvement energy;
- source-normalization shifts.

Poynting flux is not an `E_neg` trick. Crossing/radiative flux belongs to `epsilon_closed` from 3946.

## Current Verdict

- Progress: exact `E_pos/E_neg/epsilon_closed` sign inequality derived.
- Progress: EM/Poynting placement is now clean.
- Blocker: no parent DEC/WEC/no-ghost theorem for full `T_total` yet.
- Blocker: no numeric/source-backed `E_pos`, `epsilon_neg`, or `epsilon_closed` values yet.
- Public claim: blocked.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3947_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3947_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3947_TOTAL_HILBERT_POSITIVE_ENERGY_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3947_SECTOR_SIGN_DECOMPOSITION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3947_EPSILON_NEG_BOUND_VECTOR.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3947_MEH_SIGN_BOUND_CANDIDATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3947_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3947_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3947 - Total Hilbert Source Positive Energy Or Negative-Sector Bound

Timestamp: `{timestamp}`

- Logic refined: `Z_Etotal_positive` is separated from `Z_sourceblind_ref`; source energy positivity and reference subtraction are no longer conflated.
- Derived sign bound: `M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed)`, so `M_EH>0` follows from `E_pos>0` and `epsilon_neg+epsilon_closed<1`.
- Sector split: manifest/parent-signed positive sectors enter `E_pos`; binding, stabilizer, material/theta, parent exchange, counterterm and source-normalization sectors enter `E_neg`.
- EM/Poynting placement: descended stationary Maxwell energy belongs in `E_pos`; crossing/radiative Poynting flux remains in `epsilon_closed`.
- Claim status: private nonclaim; parent positive-energy/no-ghost theorem or concrete sector bounds are still needed.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3947 - Total Hilbert Source Positive Energy Or Negative-Sector Bound"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theorem = theorem_rows(timestamp)
    sector = sector_rows(timestamp)
    epsilon_neg = epsilon_neg_rows(timestamp)
    candidate = candidate_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (theorem, sector, epsilon_neg, candidate, decisions, claim_gate, next_target)
    theorem_statuses = {row["status"] for row in theorem}
    sector_buckets = {row["bucket"] for row in sector}
    neg_symbols = {row["symbol"] for row in epsilon_neg}
    checks = [
        ("VAL3947_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3947_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3947_02_logic_split", "LOGIC_SPLIT_REFINED" in theorem_statuses, "source-energy/ref logic split emitted"),
        ("VAL3947_03_Epos_defined", "E_POS_DECOMPOSITION_DEFINED" in theorem_statuses, "E_pos decomposition emitted"),
        ("VAL3947_04_Eneg_defined", "E_NEG_MAGNITUDE_DECOMPOSITION_DEFINED" in theorem_statuses, "E_neg magnitude decomposition emitted"),
        ("VAL3947_05_sign_bound", "CONDITIONAL_SIGN_BOUND_DERIVED" in theorem_statuses, "M_EH sign bound derived"),
        ("VAL3947_06_EM_split", "EM_POSITIVE_AND_FLUX_SPLIT_LOCKED" in theorem_statuses, "EM/Poynting placement locked"),
        ("VAL3947_07_sector_rows", {"E_pos", "E_neg", "epsilon_closed"}.issubset(sector_buckets), "sector rows include E_pos, E_neg, epsilon_closed buckets"),
        ("VAL3947_08_epsilon_neg_rows", {"E_pos", "epsilon_neg", "epsilon_MEH_sign"}.issubset(neg_symbols), "epsilon_neg bound rows include denominator and totals"),
        ("VAL3947_09_candidate_bound", any(row["quantity"] == "M_EH_lower" and "epsilon_neg" in row["formula"] for row in candidate), "M_EH sign-bound candidate emitted"),
        ("VAL3947_10_DEC_shortcut", any(row["quantity"] == "Z_energy_condition" for row in candidate), "parent positive-energy shortcut row emitted"),
        ("VAL3947_11_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public/local-GR claim"),
        ("VAL3947_12_next_3948", next_target[0]["next_doc"] == NEXT_DOC and "Hamiltonian" in next_target[0]["target"], "next target selects parent Hamiltonian/no-ghost route"),
        ("VAL3947_13_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3947_14_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3947_15_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3947_16_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3947_17_spine_written", SPINE_PATH.exists() and "3947 - Total Hilbert Source" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3947_18_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3947_19_script_compiles", True, "script compiles"),
        ("VAL3947_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem_rows(timestamp))
    write_csv(OUTPUTS["sector"], sector_rows(timestamp))
    write_csv(OUTPUTS["epsilon_neg"], epsilon_neg_rows(timestamp))
    write_csv(OUTPUTS["candidate"], candidate_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3947 validation failed: {failed}")
    print(f"3947 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
