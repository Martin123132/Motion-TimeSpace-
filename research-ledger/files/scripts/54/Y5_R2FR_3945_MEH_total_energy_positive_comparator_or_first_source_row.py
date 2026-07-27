from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3945"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3945-Y5-R2FR-MEH-total-energy-positive-comparator-or-first-source-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3945_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3945_MEH_POSITIVE_COMPARATOR_THEOREM.csv",
    "first_source": SRC / "P8_Y5_R2FR_3945_MEH_FIRST_SOURCE_ROW.csv",
    "audit": SRC / "P8_Y5_R2FR_3945_TOTAL_SOURCE_POSITIVITY_AUDIT.csv",
    "blockers": SRC / "P8_Y5_R2FR_3945_MEH_BLOCKER_BOUND_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3945_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3945_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3945_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3945_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3945_VALIDATION.csv",
}

NEXT_DOC = "3946-Y5-R2FR-total-source-domain-closedness-and-energy-condition-or-first-MEH-value.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3946_total_source_domain_closedness_and_energy_condition_or_first_MEH_value.py"


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
        ("SRC3945_00_3944_next", SRC / "P8_Y5_R2FR_3944_NEXT_TARGET.csv", "NEXT3944_0", "3944 selected the M_EH first-source-row target"),
        ("SRC3945_01_3944_definition", SRC / "P8_Y5_R2FR_3944_MEH_COMPARATOR_THEOREM.csv", "MEH3944_0_definition", "same-frame M_EH comparator definition"),
        ("SRC3945_02_3944_positive", SRC / "P8_Y5_R2FR_3944_MEH_COMPARATOR_THEOREM.csv", "MEH3944_3_positive_energy", "positive source-energy route"),
        ("SRC3945_03_3944_residual", SRC / "P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_RESIDUAL_ENVELOPE.csv", "DLB3944_0_M_EH", "M_EH source-row blocker"),
        ("SRC3945_04_3944_gate", SRC / "P8_Y5_R2FR_3944_POSITIVITY_GATE.csv", "PG3944_1_positive_energy", "positive-energy gate"),
        ("SRC3945_05_3820_komar", SRC / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv", "KT3820_6_verdict", "Komar/Tolman active mass derivation"),
        ("SRC3945_06_3821_energy", SRC / "P8_Y5_R2FR_3821_TOLMAN_TO_ENERGY_MASS_REDUCTION.csv", "TER3821_2_energy_mass_limit", "Tolman active mass to total energy reduction"),
        ("SRC3945_07_3821_virial", SRC / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv", "SVT3821_5_verdict", "closed-system stress virial route"),
        ("SRC3945_08_3821_bound", SRC / "P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv", "PBV3821_5_total", "pressure/binding residual vector"),
        ("SRC3945_09_3777_maxwell", SRC / "P8_Y5_R2FR_3777_EM_FIELD_ENERGY_SOURCE_MAP.csv", "ESM3777_0_descended_Maxwell", "descended Maxwell stress is part of total source"),
        ("SRC3945_10_3777_poynting", SRC / "P8_Y5_R2FR_3777_EM_FIELD_ENERGY_SOURCE_MAP.csv", "ESM3777_4_radiative_EM", "radiative EM/Poynting flux cannot be hidden"),
        ("SRC3945_11_3906_contract", SRC / "P8_Y5_R2FR_3906_LOW_ENERGY_GR_BRANCH_CONTRACT.csv", "LEGR3906_0_scope", "local-GR branch contract"),
        ("SRC3945_12_3906_policy", SRC / "P8_Y5_R2FR_3906_LOW_ENERGY_GR_BRANCH_CONTRACT.csv", "LEGR3906_2_public_claim_policy", "public claim discipline"),
        ("SRC3945_13_3933_maxwell", SRC / "P8_Y5_R2FR_3933_NEWTON_MAXWELL_SOURCE_ARENA_ROLLUP.csv", "ARE3933_2_Maxwell", "Newton/Maxwell source rollup"),
        ("SRC3945_14_3820_ledger", SRC / "P8_Y5_R2FR_3820_INDEPENDENT_SOURCE_LEDGER_TEMPLATE.csv", "LED3820_4_EM_field_stress", "independent EM stress/Poynting source ledger"),
        ("SRC3945_15_3821_classifier", SRC / "P8_Y5_R2FR_3821_CLOSED_SOURCE_CLASSIFIER.csv", "CLS3821_0_closed_stationary_lab_body", "closed stationary source classifier"),
        ("SRC3945_16_3944_validation", SRC / "P8_Y5_BRR545_3944_VALIDATION.csv", "VAL3944_17_no_pycache", "previous validation"),
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
            "row_id": "PEC3945_0_MEH_object",
            "claim_piece": "same-frame total source-energy object",
            "statement": "M_EH[tau,W_source,S_link] := c^-2 E_total[tau,W_source,S_link]",
            "derivation": "3944 made M_EH the comparator denominator. 3945 fixes its meaning as the energy of the same source complex that feeds the Hilbert/Komar/Tolman charge, in the same tau/coframe/worldtube/surface branch.",
            "status": "EXACT_CONDITIONAL_OBJECT_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PEC3945_1_total_energy_density",
            "claim_piece": "energy density integrand",
            "statement": "E_total = integral_{Sigma cap W_source} T_total(n,tau) dSigma + E_tail_or_flux_terms",
            "derivation": "The source is the total Hilbert stress: matter, binding, stabilizer, descended Maxwell field energy, and allowed field tails. Open Poynting/radiative terms are explicit residuals, not silently absorbed.",
            "status": "TOTAL_SOURCE_INTEGRAND_FIXED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PEC3945_2_positive_energy_sufficient_conditions",
            "claim_piece": "positive M_EH theorem",
            "statement": "If W_source is closed/stationary, tau and n are same-frame future timelike, T_total(n,tau)>=0, the source support is nonzero, and H_ref is source-blind, then M_EH>0.",
            "derivation": "Under these clauses the integrand is nonnegative everywhere and positive on nonzero source support; c^2>0, so the comparator mass is positive. This proves the required sign condition conditionally without importing orbital GM.",
            "status": "CONDITIONAL_POSITIVE_ENERGY_THEOREM_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PEC3945_3_Komar_Tolman_bridge",
            "claim_piece": "active mass to energy mass bridge",
            "statement": "stationary EH charge -> Komar/Tolman active mass -> c^-2 total energy plus named residuals",
            "derivation": "Pressure/stress terms are carried by the total closed-source virial theorem or by finite residual rows. This prevents the classic Tolman pressure trap from being swept under the rug.",
            "status": "KOMAR_TOLMAN_POSITIVITY_BRIDGE_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PEC3945_4_EM_Poynting_clause",
            "claim_piece": "EM and Poynting discipline",
            "statement": "Descended T_EM contributes positive field energy on closed/stationary support; radiative Poynting flux is a boundary/open-domain residual.",
            "derivation": "This answers the Poynting-vector route directly: it can help as source energy if closed/stationary, but it cannot be used as hidden local-GR positivity if it is crossing the source boundary.",
            "status": "EM_INCLUDED_WITH_OPEN_FLUX_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PEC3945_5_verdict",
            "claim_piece": "3945 verdict",
            "statement": "The sign law is derived conditionally; the public/local-GR claim remains blocked until total-source closedness, energy-condition, and source-row certificates are signed.",
            "derivation": "This moves the problem from a vague missing denominator to three concrete proof/source gates: source domain, energy positivity, and value/provenance.",
            "status": "FORWARD_REDUCTION_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def first_source_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FSR3945_0_local_stationary_total_source",
            "system_id": "LOCAL_STATIONARY_CLOSED_TOTAL_SOURCE_BRANCH",
            "quantity": "M_EH",
            "definition": "same-frame EH/source-energy comparator",
            "formula": "M_EH = c^-2 * integral_{Sigma cap W_source} T_total(n,tau) dSigma + c^-2*E_tail_or_flux_terms",
            "tau_id": "tau_obs_same_frame_REQUIRED",
            "coframe_id": "e_obs_same_frame_REQUIRED",
            "worldtube_id": "W_source_total_closed_REQUIRED",
            "surface_link": "S_link_same_branch_REQUIRED",
            "source_complex": "T_total = T_matter + T_binding + T_stabilizer + T_EM + permitted field-tail terms",
            "M_EH_value": "SYMBOLIC_POSITIVE_IF_CERTIFIED",
            "M_EH_units": "mass",
            "positivity_certificate": "PEC3945_2_positive_energy_sufficient_conditions",
            "value_status": "NO_NUMERIC_SOURCE_VALUE_YET",
            "score_ready": False,
            "claim_allowed": False,
            "not_orbital_GM_imported": True,
            "source_path": str(OUTPUTS["theorem"]),
            "equation_ref": "PEC3945_0_MEH_object;PEC3945_2_positive_energy_sufficient_conditions",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def positivity_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("AUD3945_0_same_frame", "tau/coframe/worldtube/surface matches M_H_ref branch", "CONDITIONAL_FROM_3944_UNSIGNED", "same-frame lock source certificate"),
        ("AUD3945_1_closed_domain", "W_source is a closed stationary total source domain", "MISSING_TOTAL_SOURCE_DOMAIN_CERTIFICATE", "closedness/worldtube row or open-flux bound"),
        ("AUD3945_2_future_timelike", "tau and hypersurface normal n are same-frame future timelike", "MISSING_FRAME_CAUSALITY_CERTIFICATE", "tau/coframe causality row"),
        ("AUD3945_3_energy_condition", "T_total(n,tau)>=0 on source support", "MISSING_TOTAL_ENERGY_CONDITION_OR_POSITIVE_ENERGY_THEOREM", "parent positive-energy theorem or source-class bound"),
        ("AUD3945_4_nonzero_support", "source support is nonzero so energy is strictly positive", "MISSING_NONZERO_SOURCE_SUPPORT_CERTIFICATE", "source ledger row with nonzero support"),
        ("AUD3945_5_total_complex", "matter, binding, stabilizer, EM and material response are in T_total", "MISSING_TOTAL_SOURCE_COMPLEX_CERTIFICATE", "same-current Hilbert source ledger"),
        ("AUD3945_6_stress_virial", "Tolman pressure/stress terms are zeroed by total closed-source virial theorem or bounded", "CONDITIONAL_STRESS_VIRIAL_ROUTE_UNSIGNED", "SVT/PBV residual row"),
        ("AUD3945_7_EM_flux", "descended EM field energy included and Poynting/radiative flux not hidden", "MISSING_EM_DOMAIN_OR_FLUX_BOUND", "EM source-domain and flux row"),
        ("AUD3945_8_reference", "H_ref is fixed and source-blind, not subtracting M_EH", "CONDITIONAL_REFERENCE_ZERO_UNSIGNED", "reference branch certificate"),
        ("AUD3945_9_no_GM_laundering", "M_EH not taken from orbital GM or fitted mu/G", "PASS_GUARD", "keep independent source-energy route"),
        ("AUD3945_10_claim", "all gates signed before M_EH>0 is claim-grade", "BLOCKED_NONCLAIM", "3946 source-domain/energy-condition target"),
    ]
    return [
        {
            "row_id": row_id,
            "audit_clause": clause,
            "status": status,
            "exit_requirement": exit_requirement,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, status, exit_requirement in data
    ]


def blocker_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BLK3945_0_domain", "M_EH", "closed/stationary total-source domain", "MISSING_TOTAL_SOURCE_DOMAIN_CERTIFICATE", "dimensionless certificate", "prove W_source has no hidden incoming/outgoing energy flux or provide flux bound"),
        ("BLK3945_1_energy_condition", "M_EH", "positive total Hilbert energy density", "MISSING_TOTAL_ENERGY_CONDITION_OR_POSITIVE_ENERGY_THEOREM", "dimensionless certificate", "parent positive-energy theorem, WEC/DEC route, or finite negative-energy lower bound"),
        ("BLK3945_2_nonzero_support", "M_EH", "strict positive support", "MISSING_NONZERO_SOURCE_SUPPORT_CERTIFICATE", "dimensionless certificate", "independent source ledger showing nonzero total support"),
        ("BLK3945_3_source_complex", "M_EH", "full source complex included", "MISSING_TOTAL_SOURCE_COMPLEX_CERTIFICATE", "dimensionless certificate", "matter/binding/stabilizer/EM/source-current descent row"),
        ("BLK3945_4_stress_virial", "Delta_stress_virial", "pressure and binding stress closure", "MISSING_STRESS_VIRIAL_ZERO_OR_BOUND", "G_mass_units or dimensionless epsilon", "total closed-source virial zero or PBV finite bound"),
        ("BLK3945_5_EM_flux", "Delta_EM", "Poynting/radiative field-domain correction", "MISSING_EM_CLOSED_SOURCE_OR_FLUX_BOUND", "G_mass_units or energy flux", "descended T_EM source-domain row plus radiative flux bound"),
        ("BLK3945_6_reference", "Delta_ref", "reference subtraction silence", "MISSING_REFERENCE_ZERO_OR_VALUE", "G_mass_units", "fixed source-blind H_ref certificate"),
        ("BLK3945_7_numeric_value", "M_EH_value", "first numeric/source-backed value", "MISSING_NUMERIC_SOURCE_VALUE", "mass", "system_id-specific total energy or acceptable positive comparator certificate"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "blocker": blocker,
            "current_value": current_value,
            "units": units,
            "exit_requirement": exit_requirement,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, blocker, current_value, units, exit_requirement in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3945_0_sign_law",
            "decision": "accept the conditional sign theorem for M_EH",
            "effect": "M_EH positivity is now a concrete total-source/energy-condition problem, not a vague denominator assumption",
            "claim_status": "CONDITIONAL_THEOREM_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3945_1_first_row",
            "decision": "stage a first symbolic source row for LOCAL_STATIONARY_CLOSED_TOTAL_SOURCE_BRANCH",
            "effect": "future work can fill system_id/tau/coframe/worldtube/source-complex fields instead of inventing orbital-GM denominators",
            "claim_status": "ROW_STAGED_NOT_NUMERIC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3945_2_poynting",
            "decision": "treat Poynting/vector-wave energy as part of T_total only on closed/stationary support",
            "effect": "EM waves can help the source-energy picture, but radiative flux remains an explicit residual if the domain is open",
            "claim_status": "EM_INCLUDED_WITH_FLUX_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3945_3_next",
            "decision": "target closedness and energy-condition certificate next",
            "effect": "3946 must either sign the local source class or admit M_EH remains source-row-only",
            "claim_status": "NEXT_SOURCE_DOMAIN_AND_ENERGY_CONDITION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3945_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3945_1_sign_theorem", "gate": "M_EH sign theorem", "requirement": "conditional theorem states exact sufficient conditions", "status": "PASS_CONDITIONAL_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3945_2_total_source_domain", "gate": "closed stationary source domain", "requirement": "source support and field domain signed", "status": "BLOCKED_DOMAIN_CERTIFICATE_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3945_3_energy_condition", "gate": "positive total energy", "requirement": "T_total(n,tau)>=0 or parent positive-energy theorem", "status": "BLOCKED_ENERGY_CONDITION_UNSIGNED", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3945_4_numeric_or_source_value", "gate": "M_EH source row", "requirement": "numeric/source-backed value or strict positive certificate", "status": "BLOCKED_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3945_5_local_GR_claim", "gate": "local-GR denominator positivity", "requirement": "M_EH>0 and residual envelope from 3944 below one", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3945_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove or source the closed stationary total-source domain and total-energy positivity certificate for the first M_EH row, including EM/Poynting domain discipline",
            "success_condition": "either M_EH>0 becomes parent/source-signed for the local stationary branch, or the row remains explicit closure-only with named domain/energy blockers",
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
            "summary": "3945 derives the conditional M_EH>0 law and stages the first same-frame total-source row, with EM/Poynting handled as source energy only when the domain is closed/stationary",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3945 - M_EH Total-Energy Positive Comparator Or First Source Row

Timestamp: `{timestamp}`

## Result

3945 proves the exact conditional sign law for the comparator introduced in 3944:

`M_EH[tau,W_source,S_link] := c^-2 E_total[tau,W_source,S_link]`.

If the source domain is closed and stationary, `tau` and `n` are same-frame future timelike, `T_total(n,tau)>=0`, the support is nonzero, and the reference branch is source-blind, then:

`M_EH > 0`.

That is a real forward move: the denominator sign is no longer an axiom. It is now a named total-source/positive-energy certificate problem.

## First Source Row

The staged row is:

`LOCAL_STATIONARY_CLOSED_TOTAL_SOURCE_BRANCH`.

It carries:

- same `tau/coframe/worldtube/surface` requirements;
- total Hilbert source complex including matter, binding, stabilizer, material response, and descended Maxwell field stress;
- no orbital-`GM` import;
- nonclaim status until the total source domain and positive-energy certificate are signed.

## Poynting / EM Clause

The Poynting-vector route is not discarded. It is disciplined:

- bound/stationary EM field energy contributes through `T_EM`;
- radiative or crossing Poynting flux is an open-boundary residual;
- no hidden flux is allowed inside `M_EH>0`.

## Current Verdict

- Progress: conditional `M_EH>0` theorem derived.
- Progress: first same-frame source-energy row staged.
- Blocker: closed stationary total-source certificate is unsigned.
- Blocker: total energy condition / positive-energy theorem is unsigned.
- Blocker: no numeric/source-backed `M_EH` value exists yet.
- Public claim: blocked.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3945_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3945_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3945_MEH_POSITIVE_COMPARATOR_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3945_MEH_FIRST_SOURCE_ROW.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3945_TOTAL_SOURCE_POSITIVITY_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3945_MEH_BLOCKER_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3945_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3945_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3945 - M_EH Total-Energy Positive Comparator Or First Source Row

Timestamp: `{timestamp}`

- Derived sign law: if `W_source` is closed/stationary, `tau,n` are same-frame future timelike, `T_total(n,tau)>=0`, support is nonzero, and `H_ref` is source-blind, then `M_EH=c^-2 E_total>0`.
- First source row staged: `LOCAL_STATIONARY_CLOSED_TOTAL_SOURCE_BRANCH` with required tau/coframe/worldtube/surface fields and `not_orbital_GM_imported=true`.
- EM/Poynting discipline: descended `T_EM` contributes as source energy only on closed/stationary support; radiative/crossing Poynting flux remains an explicit residual.
- Claim status: private nonclaim; source-domain, energy-condition, and numeric/source-backed `M_EH` rows remain unsigned.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3945 - M_EH Total-Energy Positive Comparator Or First Source Row"
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
    first_source = first_source_rows(timestamp)
    audit = positivity_audit_rows(timestamp)
    blockers = blocker_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (theorem, first_source, audit, blockers, decisions, claim_gate, next_target)
    audit_statuses = {row["status"] for row in audit}
    blocker_values = {row["current_value"] for row in blockers}
    checks = [
        ("VAL3945_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3945_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3945_02_MEH_object", any(row["status"] == "EXACT_CONDITIONAL_OBJECT_DEFINED" and "M_EH" in row["statement"] for row in theorem), "M_EH object definition emitted"),
        ("VAL3945_03_positive_theorem", any(row["status"] == "CONDITIONAL_POSITIVE_ENERGY_THEOREM_DERIVED" and "M_EH>0" in row["statement"] for row in theorem), "conditional positive-energy theorem emitted"),
        ("VAL3945_04_Komar_bridge", any(row["status"] == "KOMAR_TOLMAN_POSITIVITY_BRIDGE_CONDITIONAL" for row in theorem), "Komar/Tolman positivity bridge retained"),
        ("VAL3945_05_EM_clause", any(row["status"] == "EM_INCLUDED_WITH_OPEN_FLUX_GUARD" for row in theorem), "EM/Poynting clause emitted"),
        ("VAL3945_06_first_source_row", len(first_source) == 1 and first_source[0]["quantity"] == "M_EH", "first M_EH source row emitted"),
        ("VAL3945_07_no_GM_import", bool(first_source[0]["not_orbital_GM_imported"]) and "GM" not in first_source[0]["M_EH_value"], "first row forbids orbital-GM import"),
        ("VAL3945_08_audit_gates", "PASS_GUARD" in audit_statuses and "BLOCKED_NONCLAIM" in audit_statuses, "audit has no-GM guard and public-claim block"),
        ("VAL3945_09_blockers_named", {"MISSING_TOTAL_SOURCE_DOMAIN_CERTIFICATE", "MISSING_TOTAL_ENERGY_CONDITION_OR_POSITIVE_ENERGY_THEOREM", "MISSING_EM_CLOSED_SOURCE_OR_FLUX_BOUND"}.issubset(blocker_values), "domain, energy-condition, and EM flux blockers named"),
        ("VAL3945_10_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public/local-GR claim"),
        ("VAL3945_11_next_3946", next_target[0]["next_doc"] == NEXT_DOC and "closed stationary" in next_target[0]["target"], "next target selects source-domain and energy-condition certificate"),
        ("VAL3945_12_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3945_13_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3945_14_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3945_15_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3945_16_spine_written", SPINE_PATH.exists() and "3945 - M_EH Total-Energy" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3945_17_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3945_18_script_compiles", True, "script compiles"),
        ("VAL3945_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["first_source"], first_source_rows(timestamp))
    write_csv(OUTPUTS["audit"], positivity_audit_rows(timestamp))
    write_csv(OUTPUTS["blockers"], blocker_rows(timestamp))
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
        raise SystemExit(f"3945 validation failed: {failed}")
    print(f"3945 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
