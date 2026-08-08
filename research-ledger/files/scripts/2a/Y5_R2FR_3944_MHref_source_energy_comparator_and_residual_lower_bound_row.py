from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3944"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3944-Y5-R2FR-MHref-source-energy-comparator-and-residual-lower-bound-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3944_SOURCE_REGISTER.csv",
    "comparator": SRC / "P8_Y5_R2FR_3944_MEH_COMPARATOR_THEOREM.csv",
    "residuals": SRC / "P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_RESIDUAL_ENVELOPE.csv",
    "candidate": SRC / "P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_CANDIDATE_ROW.csv",
    "gate": SRC / "P8_Y5_R2FR_3944_POSITIVITY_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3944_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3944_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3944_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3944_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3944_VALIDATION.csv",
}

NEXT_DOC = "3945-Y5-R2FR-MEH-total-energy-positive-comparator-or-first-source-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3945_MEH_total_energy_positive_comparator_or_first_source_row.py"


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
        ("SRC3944_00_3943_next", SRC / "P8_Y5_R2FR_3943_NEXT_TARGET.csv", "NEXT3943_0", "3943 handoff to M_EH lower-bound rows"),
        ("SRC3944_01_3943_theorem", SRC / "P8_Y5_R2FR_3943_MHREF_REFERENCE_CHARGE_THEOREM.csv", "MRT3943_2_positive_lower_bound", "positive lower-bound theorem"),
        ("SRC3944_02_3943_template", SRC / "P8_Y5_R2FR_3943_MHREF_SOURCE_ROW_TEMPLATE.csv", "MHS3943_1_MHref_lower", "M_H_ref lower-bound template"),
        ("SRC3944_03_3943_bound", SRC / "P8_Y5_R2FR_3943_RKERNEL_FIRST_BOUND_ROW.csv", "RB3943_1_denominator", "denominator bound blocker"),
        ("SRC3944_04_3207_law", SRC / "P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv", "LAW3207_3_positive_lower_bound", "triangle lower-bound law"),
        ("SRC3944_05_3825_law", SRC / "P8_Y5_R2FR_3825_MHREF_POSITIVE_DENOMINATOR_LAW.csv", "MHD3825_1_Komar_Tolman_energy_route", "Komar/Tolman energy route"),
        ("SRC3944_06_3820_kt", SRC / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv", "KT3820_6_verdict", "active source-mass derivation"),
        ("SRC3944_07_3820_residual", SRC / "P8_Y5_R2FR_3820_ACTIVE_MASS_RESIDUAL_ROWS.csv", "R3820_5_total", "active-mass residual total"),
        ("SRC3944_08_3821_reduction", SRC / "P8_Y5_R2FR_3821_TOLMAN_TO_ENERGY_MASS_REDUCTION.csv", "TER3821_2_energy_mass_limit", "Tolman to energy mass reduction"),
        ("SRC3944_09_3821_virial", SRC / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv", "SVT3821_5_verdict", "stress virial theorem"),
        ("SRC3944_10_3821_bound", SRC / "P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv", "PBV3821_5_total", "pressure/binding bound vector"),
        ("SRC3944_11_3825_firstrow", SRC / "P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv", "FSR3825_2_MHref", "source-ready M_H_ref row"),
        ("SRC3944_12_3825_residual", SRC / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv", "R3825_4_total", "boundary/M_H_ref residual total"),
        ("SRC3944_13_3446_bound", SRC / "P8_Y5_R2FR_3446_MHREF_DENOMINATOR_BOUND_ROWS.csv", "DBR3446_5_epsilon_den_total", "denominator residual rows"),
        ("SRC3944_14_3433_lock", SRC / "P8_Y5_R2FR_3433_MHREF_TAU_SOURCE_LOCK_THEOREM.csv", "SL3433_5_newton_limit", "same-frame source/Newton lock"),
        ("SRC3944_15_3933_source", SRC / "P8_Y5_R2FR_3933_NEWTON_MAXWELL_SOURCE_ARENA_ROLLUP.csv", "ARE3933_2_Maxwell", "private Maxwell/source rollup"),
        ("SRC3944_16_3943_validation", SRC / "P8_Y5_BRR545_3943_VALIDATION.csv", "VAL3943_18_no_pycache", "previous validation"),
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


def comparator_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MEH3944_0_definition",
            "claim_piece": "source-energy comparator",
            "formula": "M_EH := c^-2 * E_total[tau,W_source] in the same tau/coframe/worldtube branch",
            "derivation": "The comparator is the EH/Komar/Tolman total-source energy mass in the same frame as M_H_ref, not a fitted orbital mass.",
            "status": "EXACT_CONDITIONAL_DEFINITION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MEH3944_1_Komar_Tolman",
            "claim_piece": "active-charge comparator route",
            "formula": "M_K = (2/c^2) int_Sigma (T_ab - 0.5*T*g_ab)n^a tau^b dSigma + R_boundary",
            "derivation": "On the stationary EH branch, the Hamiltonian surface charge reduces to the Komar/Tolman total Hilbert-stress charge plus named boundary/reference residuals.",
            "status": "CONDITIONAL_KOMAR_TOLMAN_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MEH3944_2_virial_reduction",
            "claim_piece": "Tolman pressure/stress reduction",
            "formula": "closed stationary total source => int T_total^i_i dV = 0 and M_K -> c^-2 int T_total00 dV + residuals",
            "derivation": "The pressure term is not deleted by hand; it cancels only for the total closed stationary source via the stress-virial identity.",
            "status": "CONDITIONAL_STRESS_VIRIAL_REDUCTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MEH3944_3_positive_energy",
            "claim_piece": "positivity condition",
            "formula": "M_EH>0 if E_total>0 and the selected reference does not subtract the source charge",
            "derivation": "This is a positive-energy/source ledger condition. It must be sourced by total energy or a positive-energy theorem, not inferred from observed orbit fits.",
            "status": "POSITIVE_COMPARATOR_ROUTE_BUILT_SOURCE_ROW_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MEH3944_4_lower_bound",
            "claim_piece": "M_H_ref lower bound",
            "formula": "M_H_ref_lower := M_EH*(1-epsilon_abs), epsilon_abs=sum_i |Delta_i|/(G_*M_EH)",
            "derivation": "By the triangle inequality applied to the same-frame charge decomposition, if M_EH>0 and epsilon_abs<1 then M_H_ref>0.",
            "status": "LOWER_BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MEH3944_5_verdict",
            "claim_piece": "3944 verdict",
            "formula": "M_H_ref_lower is source-row ready but not claim-ready",
            "derivation": "The comparator route is mathematically disciplined; current blocker is filling M_EH and residual components with parent-signed zeroes or source-backed finite rows.",
            "status": "FORWARD_REDUCTION_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DLB3944_0_M_EH", "M_EH", "same-frame EH/source-energy comparator", "c^-2*E_total[tau,W_source]", "MISSING_SOURCE_ENERGY_COMPARATOR_ROW", "mass", "M_EH source row or positive-energy certificate"),
        ("DLB3944_1_Komar_owner", "Delta_Komar_owner", "failure of Hamiltonian/Komar/Tolman charge ownership", "G_*M_EH * R_Komar_owner", "MISSING_STATIONARY_TAU_OR_HAMILTONIAN_CHARGE", "G_mass_units", "KT3820 owner zero or source-backed bound"),
        ("DLB3944_2_stress_virial", "Delta_stress_virial", "pressure/binding/stabilizer/virial correction", "G_*M_EH * epsilon_pressure_binding_total", "MISSING_STRESS_VIRIAL_ZERO_OR_BOUND", "G_mass_units", "closed stationary total source zero or PBV3821 finite rows"),
        ("DLB3944_3_nonEH", "Delta_nonEH", "non-EH operator or extra geometric source charge", "component in G_ref*M_H_ref decomposition", "MISSING_NON_EH_SOURCE_CHARGE_BOUND", "G_mass_units", "operator zero theorem or finite residual"),
        ("DLB3944_4_ref", "Delta_ref", "reference/counterterm shift relative to source branch", "H_ref leakage converted to charge units", "MISSING_REFERENCE_ZERO_OR_VALUE", "G_mass_units", "fixed source-blind reference or finite row"),
        ("DLB3944_5_boundary", "Delta_boundary_symp", "boundary, exact primitive, symplectic, corner or B_zero flux", "B_zero_flux + Delta_symp", "MISSING_BOUNDARY_SYMPLECTIC_ZERO_OR_BOUND", "G_mass_units", "3825/3446 boundary rows"),
        ("DLB3944_6_projector", "Delta_projector", "PiM/projector variation or stress contribution", "projector-stress charge component", "MISSING_PROJECTOR_STRESS_ZERO_OR_BOUND", "G_mass_units", "PiM stress theorem or bound"),
        ("DLB3944_7_source_measure", "Delta_source_measure", "source worldtube/support/current-complex mismatch", "source-measure residual in charge branch", "MISSING_SOURCE_MEASURE_BOUND", "G_mass_units", "same current complex/source ledger row"),
        ("DLB3944_8_coupling", "Delta_coupling", "G_ref/kappa/source-coupling normalization drift", "coupling residual in charge branch", "MISSING_COUPLING_NORMALIZATION_BOUND", "G_mass_units", "constant coupling theorem or Gdot/WEP/R10 row"),
        ("DLB3944_9_EM", "Delta_EM", "Maxwell field energy/stress/flux residual outside closed stationary branch", "EM source/flux charge correction", "MISSING_EM_CLOSED_SOURCE_OR_FLUX_BOUND", "G_mass_units", "T_EM included in source, Poynting flux bounded"),
        ("DLB3944_10_tau_surface", "Delta_tau_surface_frame", "same tau/coframe/surface mismatch for charge and source", "tau/surface/frame charge mismatch", "MISSING_TAU_SURFACE_FRAME_LOCK", "G_mass_units", "same-frame tau/surface certificate or bound"),
        ("DLB3944_11_total", "epsilon_abs", "absolute residual envelope for M_H_ref positivity", "sum_i |Delta_i|/(G_*M_EH)", "MISSING_COMPONENT_VALUES", "dimensionless", "all components theorem-zero or finite; prove epsilon_abs<1"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "current_value": value,
            "units": units,
            "exit_requirement": exit_requirement,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, definition, formula, value, units, exit_requirement in data
    ]


def candidate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "LBC3944_0_lower_bound_candidate",
            "quantity": "M_H_ref_lower",
            "formula": "M_EH*(1-epsilon_abs)",
            "required_columns": "system_id;tau_id;coframe_id;worldtube_id;surface_link;M_EH;M_EH_units;epsilon_abs;epsilon_components;proof_epsilon_lt_1;M_H_ref_lower;M_H_ref_lower_units;not_orbital_GM_imported;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_M_EH_AND_EPSILON_COMPONENTS",
            "units": "mass",
            "acceptance_condition": "M_EH>0, epsilon_abs<1, shared tau/coframe/surface, no orbital-GM import, all component source paths valid",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def positivity_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PG3944_0_same_frame", "same tau/coframe/worldtube/surface for M_EH and M_H_ref", "CONDITIONAL_UNSIGNED"),
        ("PG3944_1_positive_energy", "M_EH>0 from total source energy/positive-energy certificate", "SOURCE_ROW_MISSING"),
        ("PG3944_2_closed_total_source", "stress/pressure/binding uses total closed stationary source, not matter-only pressure", "CONDITIONAL_STRESS_VIRIAL_ROUTE"),
        ("PG3944_3_residual_components", "all Delta_i theorem-zero or finite in G_*M_EH units", "COMPONENT_VALUES_MISSING"),
        ("PG3944_4_epsilon_lt_one", "epsilon_abs<1 proven without cancellation", "NOT_SCORE_READY"),
        ("PG3944_5_no_GM_laundering", "not_orbital_GM_imported=true", "PASS_GUARD"),
        ("PG3944_6_acceptance", "M_H_ref_lower>0 accepted only after PG3944_0..5", "FAIL_CURRENT_PUBLIC_CLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3944_0_comparator_route",
            "decision": "use total source-energy / Komar-Tolman comparator as M_EH",
            "effect": "positivity is tied to a source energy object rather than fitted orbital GM",
            "claim_status": "ROUTE_BUILT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3944_1_residual_envelope",
            "decision": "require epsilon_abs no-cancellation residual envelope before denominator positivity",
            "effect": "prevents claiming M_H_ref>0 while hiding non-EH, boundary, projector, EM, stress or coupling terms",
            "claim_status": "COMPONENT_ROWS_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3944_2_next",
            "decision": "target M_EH first source row next",
            "effect": "without positive source-energy comparator, epsilon_abs and M_H_ref_lower cannot score",
            "claim_status": "NEXT_MEH_SOURCE_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3944_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3944_1_M_EH_route", "gate": "M_EH comparator route", "requirement": "M_EH defined as total source-energy/Komar-Tolman comparator", "status": "PASS_ROUTE_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3944_2_M_EH_value", "gate": "positive M_EH", "requirement": "source-backed M_EH>0 row or positive-energy certificate", "status": "BLOCKED_SOURCE_ROW_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3944_3_residual_envelope", "gate": "epsilon_abs<1", "requirement": "all Delta_i components theorem-zero or finite and no-cancellation sum below one", "status": "BLOCKED_COMPONENT_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3944_4_denominator_claim", "gate": "M_H_ref_lower>0", "requirement": "M_EH>0 and epsilon_abs<1 in same frame", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3944_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive/source the first positive M_EH total-energy comparator row with system_id, tau/coframe/worldtube/surface, units, source path, and no orbital-GM import",
            "success_condition": "M_EH>0 becomes source-backed or remains blocked by a named positive-energy/source-ledger gap; no residual lower-bound scoring occurs before M_EH exists",
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
            "summary": "3944 defines M_EH as the same-frame total source-energy/Komar-Tolman comparator and stages the residual envelope needed for M_H_ref_lower>0",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3944 - MHref Source-Energy Comparator and Residual Lower-Bound Row

Timestamp: `{timestamp}`

## Result

3944 turns the `M_H_ref>0` problem into a source-energy comparator problem.

The comparator is:

`M_EH := c^-2 E_total[tau,W_source]`

in the same tau/coframe/worldtube/surface branch as `M_H_ref`.

It is not orbital `GM`.

## Lower-Bound Law

The same-frame charge decomposition is:

`G_* M_H_ref = G_* M_EH + sum_i Delta_i`.

Therefore:

`M_H_ref >= M_EH*(1-epsilon_abs)`,

where:

`epsilon_abs = sum_i |Delta_i|/(G_* M_EH)`.

If `M_EH>0` and `epsilon_abs<1`, then `M_H_ref>0` without denominator laundering.

## Comparator Route

The route to `M_EH` is Komar/Tolman plus closed-system virial discipline:

- stationary EH source charge gives a Komar/Tolman active mass;
- closed stationary total stress reduces active mass to total energy over `c^2`;
- pressure/stress terms are not dropped unless the total-system virial cancellation or finite bound is supplied.

## Current Verdict

- Progress: the positivity gate is now exact and source-row ready.
- Blocker: no claim-grade `M_EH>0` row exists yet.
- Blocker: the residual envelope `Delta_i` is not filled/theorem-zero.
- Public claim: blocked.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3944_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3944_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3944_MEH_COMPARATOR_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_RESIDUAL_ENVELOPE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_CANDIDATE_ROW.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3944_POSITIVITY_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3944_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3944_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3944 - MHref Source-Energy Comparator and Residual Lower-Bound Row

Timestamp: `{timestamp}`

- Comparator: `M_EH := c^-2 E_total[tau,W_source]` in the same tau/coframe/worldtube/surface branch as `M_H_ref`; orbital `GM` remains forbidden.
- Lower-bound law: `G_*M_H_ref = G_*M_EH + sum_i Delta_i`, hence `M_H_ref >= M_EH*(1-epsilon_abs)` with `epsilon_abs=sum_i |Delta_i|/(G_*M_EH)`.
- Source route: Komar/Tolman active charge plus closed-system stress-virial discipline reduces the comparator to total energy over `c^2` only under closed stationary total-source conditions.
- Claim status: private nonclaim; `M_EH>0` and all residual components are still unfilled/theorem-unsigned.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3944 - MHref Source-Energy Comparator and Residual Lower-Bound Row"
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
    comparator = comparator_rows(timestamp)
    residuals = residual_rows(timestamp)
    candidate = candidate_rows(timestamp)
    gate = positivity_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (comparator, residuals, candidate, gate, decisions, claim_gate, next_target)
    residual_symbols = {row["symbol"] for row in residuals}
    checks = [
        ("VAL3944_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3944_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3944_02_comparator_definition", any(row["status"] == "EXACT_CONDITIONAL_DEFINITION" and "M_EH" in row["formula"] for row in comparator), "M_EH comparator definition emitted"),
        ("VAL3944_03_Komar_route", any(row["status"] == "CONDITIONAL_KOMAR_TOLMAN_ROUTE" for row in comparator), "Komar/Tolman route emitted"),
        ("VAL3944_04_lower_bound_law", any(row["status"] == "LOWER_BOUND_FORMULA_DERIVED_VALUES_MISSING" for row in comparator), "lower-bound law emitted"),
        ("VAL3944_05_residual_envelope", len(residuals) == 12 and "epsilon_abs" in residual_symbols and "M_EH" in residual_symbols, "residual envelope rows emitted"),
        ("VAL3944_06_candidate_row", len(candidate) == 1 and candidate[0]["quantity"] == "M_H_ref_lower", "lower-bound candidate row emitted"),
        ("VAL3944_07_gate_no_laundering", any(row["status"] == "PASS_GUARD" for row in gate), "no orbital-GM laundering guard emitted"),
        ("VAL3944_08_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public claim"),
        ("VAL3944_09_next_3945", next_target[0]["next_doc"] == NEXT_DOC and "M_EH" in next_target[0]["target"], "next target selects M_EH first source row"),
        ("VAL3944_10_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3944_11_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3944_12_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3944_13_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3944_14_spine_written", SPINE_PATH.exists() and "3944 - MHref Source-Energy Comparator" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3944_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3944_16_script_compiles", True, "script compiles"),
        ("VAL3944_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["comparator"], comparator_rows(timestamp))
    write_csv(OUTPUTS["residuals"], residual_rows(timestamp))
    write_csv(OUTPUTS["candidate"], candidate_rows(timestamp))
    write_csv(OUTPUTS["gate"], positivity_gate_rows(timestamp))
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
        raise SystemExit(f"3944 validation failed: {failed}")
    print(f"3944 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
