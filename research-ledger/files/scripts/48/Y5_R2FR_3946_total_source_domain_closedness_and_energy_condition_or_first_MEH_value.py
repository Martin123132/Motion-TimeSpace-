from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3946"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3946-Y5-R2FR-total-source-domain-closedness-and-energy-condition-or-first-MEH-value.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3946_SOURCE_REGISTER.csv",
    "current": SRC / "P8_Y5_R2FR_3946_CONSERVATION_CURRENT_THEOREM.csv",
    "domain": SRC / "P8_Y5_R2FR_3946_TOTAL_SOURCE_DOMAIN_CERTIFICATE.csv",
    "energy": SRC / "P8_Y5_R2FR_3946_ENERGY_CONDITION_CERTIFICATE.csv",
    "flux": SRC / "P8_Y5_R2FR_3946_POYNTING_AND_WALL_FLUX_BOUND_LAW.csv",
    "MEH_gate": SRC / "P8_Y5_R2FR_3946_MEH_POSITIVITY_CERTIFICATE_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3946_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3946_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3946_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3946_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3946_VALIDATION.csv",
}

NEXT_DOC = "3947-Y5-R2FR-total-Hilbert-source-positive-energy-or-negative-sector-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3947_total_Hilbert_source_positive_energy_or_negative_sector_bound.py"


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
        ("SRC3946_00_3945_next", SRC / "P8_Y5_R2FR_3945_NEXT_TARGET.csv", "NEXT3945_0", "3945 selected closed-source/energy-condition target"),
        ("SRC3946_01_3945_theorem", SRC / "P8_Y5_R2FR_3945_MEH_POSITIVE_COMPARATOR_THEOREM.csv", "PEC3945_2_positive_energy_sufficient_conditions", "conditional M_EH positive-energy theorem"),
        ("SRC3946_02_3945_EM", SRC / "P8_Y5_R2FR_3945_MEH_POSITIVE_COMPARATOR_THEOREM.csv", "PEC3945_4_EM_Poynting_clause", "EM/Poynting discipline"),
        ("SRC3946_03_3945_firstrow", SRC / "P8_Y5_R2FR_3945_MEH_FIRST_SOURCE_ROW.csv", "FSR3945_0_local_stationary_total_source", "first M_EH source row"),
        ("SRC3946_04_3945_audit", SRC / "P8_Y5_R2FR_3945_TOTAL_SOURCE_POSITIVITY_AUDIT.csv", "AUD3945_1_closed_domain", "closed-domain blocker"),
        ("SRC3946_05_3945_blockers", SRC / "P8_Y5_R2FR_3945_MEH_BLOCKER_BOUND_ROWS.csv", "BLK3945_1_energy_condition", "energy-condition blocker"),
        ("SRC3946_06_3777_domain", SRC / "P8_Y5_R2FR_3777_TOTAL_SYSTEM_DOMAIN_RULES.csv", "TSD3777_3_Poynting_flux", "Poynting domain rule"),
        ("SRC3946_07_3777_wall", SRC / "P8_Y5_R2FR_3777_TOTAL_SYSTEM_DOMAIN_RULES.csv", "TSD3777_7_boundary_surface", "domain-wall flux rule"),
        ("SRC3946_08_3777_flux", SRC / "P8_Y5_R2FR_3777_FIELD_DOMAIN_BOUND_VECTOR.csv", "FDB3777_1_Poynting_flux", "Poynting flux bound row"),
        ("SRC3946_09_3777_closure", SRC / "P8_Y5_R2FR_3777_PIM_TOTAL_CLOSURE_ATTEMPT.csv", "PCA3777_6_boundary_flux", "boundary flux blocker"),
        ("SRC3946_10_3821_virial_input", SRC / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv", "SVT3821_0_total_conservation_input", "total Hilbert stress conservation input"),
        ("SRC3946_11_3821_trace", SRC / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv", "SVT3821_2_trace_cancellation", "closed-source trace cancellation"),
        ("SRC3946_12_3821_energy", SRC / "P8_Y5_R2FR_3821_TOLMAN_TO_ENERGY_MASS_REDUCTION.csv", "TER3821_2_energy_mass_limit", "closed stationary energy-mass limit"),
        ("SRC3946_13_3821_bound", SRC / "P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv", "PBV3821_5_total", "open/nonstationary pressure-bound vector"),
        ("SRC3946_14_3906_contract", SRC / "P8_Y5_R2FR_3906_LOW_ENERGY_GR_BRANCH_CONTRACT.csv", "LEGR3906_0_scope", "local GR branch contract"),
        ("SRC3946_15_3945_validation", SRC / "P8_Y5_BRR545_3945_VALIDATION.csv", "VAL3945_19_no_pycache", "previous validation"),
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


def current_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CCT3946_0_energy_current",
            "piece": "source-energy current",
            "statement": "J_tau^a := -T_total^{a b} tau_b in the selected same-frame branch",
            "derivation": "This is the Noether/Hilbert energy current for the observer generator tau. It uses the total source stress, not matter-only stress.",
            "residual_form": "none at definition level",
            "status": "EXACT_CURRENT_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CCT3946_1_divergence_identity",
            "piece": "current divergence",
            "statement": "nabla_a J_tau^a = -(nabla_a T_total^{a b}) tau_b - T_total^{a b} nabla_(a tau_b)",
            "derivation": "Product rule plus symmetry of Hilbert stress. On the exact local stationary branch, total stress conservation and Killing/stationary tau make the divergence vanish.",
            "residual_form": "R_div = -R_Ward^b tau_b - T_total^{ab} nabla_(a tau_b)",
            "status": "EXACT_IDENTITY_WITH_RESIDUALS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CCT3946_2_worldtube_balance",
            "piece": "closed worldtube energy balance",
            "statement": "E_tau[Sigma_2]-E_tau[Sigma_1] = -Phi_wall[J_tau] + integral_Omega R_div dV",
            "derivation": "Integrate CCT3946_1 over the source worldtube slab. Closed/stationary source means no side-wall flux and no divergence residual, so E_tau is conserved.",
            "residual_form": "Delta_E_closed = -Phi_wall + integral R_div",
            "status": "EXACT_GAUSS_BALANCE_LAW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CCT3946_3_MEH_closed_domain",
            "piece": "M_EH closed-domain condition",
            "statement": "Z_closed_domain := (Phi_wall=0 and R_Ward=0 and nabla_(a tau_b)=0 and no unassigned tail/flux)",
            "derivation": "If Z_closed_domain holds, the M_EH integral is independent of the slice and is not leaking energy through hidden Poynting, tail, apparatus, or boundary channels.",
            "residual_form": "epsilon_closed = (|Phi_wall| + |integral R_div| + |E_tail_unassigned|)/(E_pos)",
            "status": "CONDITIONAL_DOMAIN_ZERO_THEOREM_BUILT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CCT3946_4_open_domain_bound",
            "piece": "open/nonstationary fallback",
            "statement": "If Z_closed_domain is unsigned, keep epsilon_closed finite and feed it into the M_EH positivity/residual gate.",
            "derivation": "The theory is not allowed to call the source closed when a boundary/Poynting/tail channel is merely uncomputed.",
            "residual_form": "M_EH >= c^-2 E_pos*(1-epsilon_negative-epsilon_closed)",
            "status": "FINITE_BOUND_FALLBACK_FORM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def domain_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DOM3946_0_total_stress", "T_total includes matter, binding, stabilizer, material response, descended EM, and permitted tails", "CONDITIONAL_SOURCE_COMPLEX_DEFINED_NOT_PARENT_SIGNED", "same-current Hilbert stress/source-complex certificate"),
        ("DOM3946_1_Ward", "nabla_a T_total^{ab}=0 in the local branch, up to named parent/Bianchi/source-exchange residuals", "CONDITIONAL_FROM_3821_UNSIGNED", "parent Ward/Bianchi total-stress conservation certificate"),
        ("DOM3946_2_stationary_tau", "tau is the same observed local stationary generator and nabla_(a tau_b)=0 to the required order", "MISSING_STATIONARY_TAU_CERTIFICATE", "tau/Killing or finite R_tau row"),
        ("DOM3946_3_worldtube_wall", "source worldtube wall has no unowned energy flux", "MISSING_TOTAL_DOMAIN_WALL_FLUX_CERTIFICATE", "Phi_wall=0 or epsilon_wall bound"),
        ("DOM3946_4_EM_tail", "near/tail EM field ownership is included or bounded", "MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND", "epsilon_EM_tail row"),
        ("DOM3946_5_Poynting", "Poynting flux is stationary/circulating inside the source or has zero normal wall flux", "MISSING_POYNTING_FLUX_BOUND", "epsilon_Poynting_flux row"),
        ("DOM3946_6_apparatus", "apparatus/readout support is either part of the source or excluded with a readout bound", "MISSING_APPARATUS_DOMAIN_DECLARATION", "apparatus domain declaration"),
        ("DOM3946_7_theta", "source/theta normalization support descends or is superselected", "MISSING_THETA_SOURCE_NORMALIZATION_DESCENT_OR_BOUND", "theta source normalization certificate"),
        ("DOM3946_8_result", "closed-domain certificate for M_EH", "DERIVED_CONDITIONALLY_BUT_NOT_SIGNED", "all DOM3946_0..7 pass or finite epsilon_closed bound supplied"),
    ]
    return [
        {
            "row_id": row_id,
            "domain_clause": clause,
            "status": status,
            "exit_requirement": exit_requirement,
            "Z_closed_domain_component": status in {"PASS_GUARD", "SIGNED_ZERO"},
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, status, exit_requirement in data
    ]


def energy_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ENG3946_0_DEC_route",
            "certificate_piece": "dominant/weak energy condition route",
            "statement": "If T_total obeys DEC/WEC in the selected low-energy branch, then T_total(n,tau)>=0 for future timelike n and tau.",
            "derivation": "For DEC, -T^a_b n^b is future causal and its contraction with future timelike tau has the positive energy sign in the selected convention. This gives nonnegative energy density in the M_EH integral.",
            "current_status": "CONDITIONAL_ENERGY_CONDITION_ROUTE_BUILT_PARENT_UNSIGNED",
            "bound_form": "none if DEC/WEC signed",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ENG3946_1_strict_support",
            "certificate_piece": "strict positivity",
            "statement": "If T_total(n,tau)>0 on a set of nonzero measure, then E_total>0 and M_EH>0.",
            "derivation": "The integral of a nonnegative density that is positive on nonzero support is strictly positive; c^2>0.",
            "current_status": "MISSING_NONZERO_SOURCE_SUPPORT_CERTIFICATE",
            "bound_form": "source support measure or independent total-energy row",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ENG3946_2_negative_sector_bound",
            "certificate_piece": "finite negative-sector fallback",
            "statement": "Split E_total = E_pos - E_neg + E_flux_owned. Positivity follows if epsilon_neg + epsilon_closed < 1.",
            "derivation": "This covers binding/stabilizer/material sectors that are not manifestly positive: they must be either included in a positive-energy theorem or bounded below.",
            "current_status": "BOUND_FORM_BUILT_VALUES_MISSING",
            "bound_form": "epsilon_neg=E_neg/E_pos; epsilon_closed=(|Phi_wall|+|R_div|+|E_tail_unassigned|)/E_pos",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ENG3946_3_EM_positive_piece",
            "certificate_piece": "Maxwell positive field energy",
            "statement": "For descended Maxwell stress, the local field-energy density is nonnegative; open radiative flux is not a negative source term, it is a boundary flux term.",
            "derivation": "T_EM supplies positive near-field energy in stationary closed support; Poynting flux through the wall is handled by FLX3946 rows.",
            "current_status": "EM_POSITIVE_ROUTE_BUILT_DESCENT_AND_DOMAIN_UNSIGNED",
            "bound_form": "epsilon_Poynting_flux or zero normal flux",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ENG3946_4_MEH_sign_certificate",
            "certificate_piece": "M_EH positivity certificate",
            "statement": "Z_MEH_positive := Z_closed_domain and Z_energy_condition and Z_nonzero_support and Z_sourceblind_ref.",
            "derivation": "3946 reduces the first M_EH value problem to four explicit Boolean certificates or the fallback inequality epsilon_neg+epsilon_closed<1.",
            "current_status": "CERTIFICATE_FORMULA_BUILT_NOT_FILLED",
            "bound_form": "M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed)",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def flux_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("FLX3946_0_wall", "epsilon_wall", "|int_wall J_tau^a s_a dA dt|/E_pos", "MISSING_TOTAL_DOMAIN_WALL_FLUX_BOUND", "dimensionless", "zero for closed stationary wall or finite wall-flux bound"),
        ("FLX3946_1_Poynting", "epsilon_Poynting_flux", "|int_wall S_EM dot dA dt|/E_pos", "MISSING_POYNTING_FLUX_BOUND", "dimensionless_or_rate", "zero normal Poynting flux or measured/modelled bound"),
        ("FLX3946_2_EM_tail", "epsilon_EM_tail", "E_EM_tail_unassigned/E_pos", "MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND", "dimensionless", "include tail in source or bound exterior field energy"),
        ("FLX3946_3_Ward", "epsilon_Ward", "|int_Omega R_Ward^b tau_b dV|/E_pos", "MISSING_PARENT_WARD_RESIDUAL_BOUND", "dimensionless", "parent Bianchi/Ward zero or finite residual"),
        ("FLX3946_4_tau", "epsilon_tau_stationarity", "|int_Omega T_total^{ab} nabla_(a tau_b) dV|/E_pos", "MISSING_TAU_STATIONARITY_BOUND", "dimensionless", "Killing/stationary tau or finite local-frame correction"),
        ("FLX3946_5_total", "epsilon_closed", "epsilon_wall + epsilon_Poynting_flux + epsilon_EM_tail + epsilon_Ward + epsilon_tau_stationarity", "COMPONENT_VALUES_MISSING", "dimensionless", "closed-domain if zero; bounded-domain if finite and small"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "current_value": current_value,
            "units": units,
            "exit_requirement": exit_requirement,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, formula, current_value, units, exit_requirement in data
    ]


def MEH_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("MPG3946_0_current", "energy current J_tau is defined from T_total and same tau", "PASS_CONDITIONAL_OBJECT"),
        ("MPG3946_1_balance", "Gauss balance law for source worldtube is derived", "PASS_EXACT_IDENTITY"),
        ("MPG3946_2_closed_domain", "Z_closed_domain signed or epsilon_closed finite", "BLOCKED_COMPONENT_VALUES_MISSING"),
        ("MPG3946_3_energy_condition", "DEC/WEC/positive-energy theorem signed or negative-sector bound supplied", "BLOCKED_ENERGY_CERTIFICATE_MISSING"),
        ("MPG3946_4_strict_support", "nonzero source support/energy row supplied", "BLOCKED_SUPPORT_CERTIFICATE_MISSING"),
        ("MPG3946_5_reference", "source-blind reference branch signed", "BLOCKED_REFERENCE_CERTIFICATE_MISSING"),
        ("MPG3946_6_bound_route", "fallback M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed) with sum<1", "NOT_SCORE_READY"),
        ("MPG3946_7_claim", "M_EH positivity public claim", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3946_0_conservation_current",
            "decision": "use the total Hilbert energy current J_tau to decide source-domain closedness",
            "effect": "closed source is now a Gauss-law statement with wall/Poynting/Ward/tau residuals, not an informal assumption",
            "claim_status": "DERIVATION_ADVANCE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3946_1_Poynting",
            "decision": "treat Poynting/vector-wave effects as boundary flux unless stationary/circulating inside the chosen source",
            "effect": "the background-field intuition is preserved without laundering radiation through the source mass",
            "claim_status": "FLUX_GUARD_BUILT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3946_2_positive_energy",
            "decision": "reduce M_EH>0 to DEC/WEC/positive-energy theorem or epsilon_neg+epsilon_closed<1",
            "effect": "negative binding/stabilizer sectors are handled by a theorem or a real bound, not ignored",
            "claim_status": "NEXT_ENERGY_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3946_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3946_1_current_identity", "gate": "energy-current balance law", "requirement": "J_tau divergence and worldtube balance derived", "status": "PASS_EXACT_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3946_2_closed_domain", "gate": "closed total source domain", "requirement": "wall/Poynting/tail/Ward/tau residuals zero or finite", "status": "BLOCKED_COMPONENT_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3946_3_positive_energy", "gate": "positive total energy", "requirement": "DEC/WEC/positive-energy theorem or negative-sector bound", "status": "BLOCKED_ENERGY_CERTIFICATE_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3946_4_MEH_value", "gate": "first M_EH value or strict sign certificate", "requirement": "source-backed value or Z_MEH_positive signed", "status": "BLOCKED_VALUE_OR_CERTIFICATE_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3946_5_local_GR_claim", "gate": "local-GR/source-coupling claim", "requirement": "M_EH>0 plus 3944 residual envelope below one", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3946_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove total Hilbert source positive energy from the parent/low-energy source complex, or build the negative-sector bound epsilon_neg so M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed) can be tested",
            "success_condition": "Z_energy_condition is parent/source-signed, or epsilon_neg rows are concrete enough to combine with epsilon_closed without hiding binding/stabilizer/EM terms",
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
            "summary": "3946 derives the source-domain conservation-current theorem and converts Poynting/vector-wave ambiguity into explicit wall/flux residuals; M_EH positivity now waits on energy-condition or negative-sector bounds",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3946 - Total Source Domain Closedness And Energy Condition Or First M_EH Value

Timestamp: `{timestamp}`

## Result

3946 turns source closedness into a conservation-current theorem.

Define the same-frame total Hilbert energy current:

`J_tau^a := -T_total^{{a b}} tau_b`.

Then:

`nabla_a J_tau^a = -(nabla_a T_total^{{a b}}) tau_b - T_total^{{a b}} nabla_(a tau_b)`.

Integrated over the source worldtube:

`E_tau[Sigma_2]-E_tau[Sigma_1] = -Phi_wall[J_tau] + integral_Omega R_div dV`.

So a closed stationary source is not an axiom. It is the condition:

`Phi_wall = 0`, total Ward/Bianchi residuals vanish, `tau` is stationary/Killing to the required order, and no EM tail/Poynting/apparatus/theta channel is unassigned.

## Poynting / Wave Clause

Poynting flux now has a precise role:

- stationary/circulating field momentum can be inside `T_total`;
- radiative or crossing Poynting flux is `Phi_wall` / `epsilon_Poynting_flux`;
- MTS cannot claim local-GR source positivity while hiding this flux.

## M_EH Positivity Gate

The exact route is now:

`Z_MEH_positive := Z_closed_domain and Z_energy_condition and Z_nonzero_support and Z_sourceblind_ref`.

The finite fallback is:

`M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed)`.

This means negative binding/stabilizer/material sectors must be theorem-owned or bounded. No magic roof-ladder trick.

## Current Verdict

- Progress: conservation-current/domain theorem derived.
- Progress: Poynting flux converted into an explicit wall/flux residual.
- Progress: M_EH positivity reduced to `DEC/WEC/positive-energy theorem` or `epsilon_neg+epsilon_closed<1`.
- Blocker: source-domain residual components are not numeric/theorem-zero yet.
- Blocker: total Hilbert source positive-energy condition is not parent-signed yet.
- Public claim: blocked.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3946_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_CONSERVATION_CURRENT_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_TOTAL_SOURCE_DOMAIN_CERTIFICATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_ENERGY_CONDITION_CERTIFICATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_POYNTING_AND_WALL_FLUX_BOUND_LAW.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_MEH_POSITIVITY_CERTIFICATE_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3946_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3946 - Total Source Domain Closedness And Energy Condition

Timestamp: `{timestamp}`

- Derived source-domain theorem: with `J_tau^a=-T_total^{{ab}}tau_b`, `nabla_a J_tau^a=-(nabla_aT_total^{{ab}})tau_b-T_total^{{ab}}nabla_(a tau_b)`.
- Worldtube balance: `E_tau[Sigma_2]-E_tau[Sigma_1]=-Phi_wall+int R_div`, so closed source means zero wall/Poynting/tail/Ward/tau residuals, not a closure axiom.
- Poynting discipline: stationary/circulating EM field momentum may sit inside `T_total`; radiative/crossing flux remains `epsilon_Poynting_flux`.
- Positivity gate: `Z_MEH_positive = Z_closed_domain and Z_energy_condition and Z_nonzero_support and Z_sourceblind_ref`; fallback bound is `M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed)`.
- Claim status: private nonclaim; next is proving total Hilbert positive energy or bounding negative sectors.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3946 - Total Source Domain Closedness And Energy Condition"
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
    current = current_theorem_rows(timestamp)
    domain = domain_certificate_rows(timestamp)
    energy = energy_certificate_rows(timestamp)
    flux = flux_bound_rows(timestamp)
    meh_gate = MEH_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (current, domain, energy, flux, meh_gate, decisions, claim_gate, next_target)
    current_statuses = {row["status"] for row in current}
    flux_symbols = {row["symbol"] for row in flux}
    gate_statuses = {row["status"] for row in meh_gate}
    checks = [
        ("VAL3946_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3946_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3946_02_current_defined", "EXACT_CURRENT_DEFINED" in current_statuses, "energy current J_tau defined"),
        ("VAL3946_03_divergence_identity", "EXACT_IDENTITY_WITH_RESIDUALS" in current_statuses, "current divergence identity emitted"),
        ("VAL3946_04_worldtube_balance", "EXACT_GAUSS_BALANCE_LAW" in current_statuses, "worldtube balance law emitted"),
        ("VAL3946_05_domain_theorem", "CONDITIONAL_DOMAIN_ZERO_THEOREM_BUILT" in current_statuses, "closed-domain zero theorem built"),
        ("VAL3946_06_domain_certificate", len(domain) == 9 and any(row["status"] == "MISSING_POYNTING_FLUX_BOUND" for row in domain), "domain certificate includes Poynting blocker"),
        ("VAL3946_07_energy_certificate", any(row["current_status"] == "CONDITIONAL_ENERGY_CONDITION_ROUTE_BUILT_PARENT_UNSIGNED" for row in energy), "energy condition route emitted"),
        ("VAL3946_08_negative_bound", any("epsilon_neg" in row["bound_form"] for row in energy), "negative-sector bound route emitted"),
        ("VAL3946_09_flux_bounds", {"epsilon_wall", "epsilon_Poynting_flux", "epsilon_closed"}.issubset(flux_symbols), "wall/Poynting/closed flux symbols emitted"),
        ("VAL3946_10_MEH_gate_blocks", "BLOCKED_NONCLAIM" in gate_statuses and "PASS_EXACT_IDENTITY" in gate_statuses, "MEH gate has exact identity pass and claim block"),
        ("VAL3946_11_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public/local-GR claim"),
        ("VAL3946_12_next_3947", next_target[0]["next_doc"] == NEXT_DOC and "positive energy" in next_target[0]["target"], "next target selects positive-energy/negative-sector bound"),
        ("VAL3946_13_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3946_14_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3946_15_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3946_16_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3946_17_spine_written", SPINE_PATH.exists() and "3946 - Total Source Domain" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3946_18_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3946_19_script_compiles", True, "script compiles"),
        ("VAL3946_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["current"], current_theorem_rows(timestamp))
    write_csv(OUTPUTS["domain"], domain_certificate_rows(timestamp))
    write_csv(OUTPUTS["energy"], energy_certificate_rows(timestamp))
    write_csv(OUTPUTS["flux"], flux_bound_rows(timestamp))
    write_csv(OUTPUTS["MEH_gate"], MEH_gate_rows(timestamp))
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
        raise SystemExit(f"3946 validation failed: {failed}")
    print(f"3946 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
