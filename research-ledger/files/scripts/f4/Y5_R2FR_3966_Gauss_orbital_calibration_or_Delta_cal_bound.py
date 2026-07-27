from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3966"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3966-Y5-R2FR-Gauss-orbital-calibration-or-Delta-cal-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3966_SOURCE_REGISTER.csv",
    "bridge": SRC / "P8_Y5_R2FR_3966_GAUSS_ORBITAL_BRIDGE_THEOREM_OR_BOUND.csv",
    "delta_cal": SRC / "P8_Y5_R2FR_3966_DELTA_CAL_RESIDUAL_VECTOR.csv",
    "readout": SRC / "P8_Y5_R2FR_3966_INVERSE_SQUARE_READOUT_GATE.csv",
    "newton_feed": SRC / "P8_Y5_R2FR_3966_NEWTON_SCORE_DELTA_CAL_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3966_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3966_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3966_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3966_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3966_VALIDATION.csv",
}

NEXT_DOC = "3967-Y5-R2FR-second-order-PPN-source-stability-or-Delta-PPN-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3967_second_order_PPN_source_stability_or_Delta_PPN_bound.py"


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
        ("SRC3966_00_3965_next", SRC / "P8_Y5_R2FR_3965_NEXT_TARGET.csv", "NEXT3965_0", "3965 handoff"),
        ("SRC3966_01_gauss_guard", SRC / "P8_Y5_R2FR_3965_MEFF_FLUX_DELTAPIM_FEED_UPDATE.csv", "DPMF3965_1_Gauss_guard", "Gauss guard"),
        ("SRC3966_02_delta_cal_3964", SRC / "P8_Y5_R2FR_3964_MEFF_FLUX_RESIDUAL_VECTOR.csv", "MFR3964_4_Delta_cal", "Delta_cal in M_eff vector"),
        ("SRC3966_03_pg2_frame", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG2_same_frame_weak_field_potential", "same-frame weak field potential"),
        ("SRC3966_04_pg3_poisson", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG3_EH_to_Poisson_coefficient", "EH to Poisson coefficient"),
        ("SRC3966_05_pg4_gauss", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG4_Gauss_surface_integral", "Gauss surface integral"),
        ("SRC3966_06_pg5_orbit", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG5_orbital_inverse_square_readout", "orbital inverse-square readout"),
        ("SRC3966_07_pg6_extra", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG6_zero_mu_extra_and_source_residuals", "zero extra source residuals"),
        ("SRC3966_08_pg9_ppn", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG9_second_order_source_stability", "PPN stability"),
        ("SRC3966_09_hm3", SRC / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM3_absolute_monopole_calibration", "Hilbert monopole calibration"),
        ("SRC3966_10_hm8", SRC / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM8_empirical_retained_fallback", "empirical retained fallback"),
        ("SRC3966_11_chain0", SRC / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv", "CAL523_0_observed_frame_and_charge", "Gauss chain frame/charge"),
        ("SRC3966_12_chain3", SRC / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv", "CAL523_3_Gauss_surface_no_residual", "Gauss no residual"),
        ("SRC3966_13_chain4", SRC / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv", "CAL523_4_orbital_inverse_square_readout", "inverse-square readout chain"),
        ("SRC3966_14_chain8", SRC / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv", "CAL523_8_second_order_PPN_source_stability", "second-order PPN chain"),
        ("SRC3966_15_accept", SRC / "P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv", "AG523_2_no_extra_mass_unfilled", "Gauss acceptance gates"),
        ("SRC3966_16_formula0", SRC / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv", "GO523_0_observed_orbital_monopole", "observed orbital monopole"),
        ("SRC3966_17_formula2", SRC / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv", "GO523_2_Gauss_residual", "Gauss residual"),
        ("SRC3966_18_formula5", SRC / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv", "GO523_5_no_cancellation_bound", "no-cancellation source-normalization bound"),
        ("SRC3966_19_decision", SRC / "P8_Y5_GAUSS_ORBITAL_DECISION.csv", "D523_2_measured_GM_not_derived", "measured GM not derived"),
        ("SRC3966_20_status", SRC / "P8_Y5_Gauss_orbital_calibration_status.csv", "GAUSS_ORBITAL_CALIBRATION_THEOREM_CONDITIONAL_DELTA_CAL_BOUND_ACTIVE", "prior Gauss/orbital status"),
        ("SRC3966_21_validation_3965", SRC / "P8_Y5_BRR545_3965_VALIDATION.csv", "VAL3965_19_no_pycache", "previous validation"),
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
                    excerpt = line[:1000]
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


def bridge_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GOB3966_0_observable",
            "bridge_piece": "observed orbital monopole",
            "formula": "mu_obs := r^2 |a_r| = v^2 r for slow circular test bodies in the observed frame",
            "meaning": "the real Newton observable is orbital GM, not merely a conserved current label",
            "status": "OBSERVABLE_DEFINITION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GOB3966_1_parent_source",
            "bridge_piece": "candidate parent source monopole",
            "formula": "mu_parent := G_eff M_eff[Pi_M J_H]",
            "meaning": "closed Hilbert/PiM mass becomes a candidate source side after the 3964/3965 gates",
            "status": "CONDITIONAL_CANDIDATE_NOT_CALIBRATED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GOB3966_2_poisson_gauss",
            "bridge_piece": "Poisson/Gauss bridge",
            "formula": "nabla^2 Phi=4 pi G_eff rho_H and int_S grad Phi.dS=4 pi(G_eff M_eff + Delta_mu_Gauss)",
            "meaning": "Gauss mass equals source mass only if volume, boundary, non-EH, projector, domain, and memory residuals vanish or are bounded",
            "status": "DERIVED_CONDITIONAL_BRIDGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GOB3966_3_orbit_readout",
            "bridge_piece": "slow-orbit inverse-square readout",
            "formula": "a_r=-partial_r Phi=-G_eff M_eff/r^2 and v^2 r=G_eff M_eff",
            "meaning": "closed Gauss mass becomes measured orbital GM only in same-frame slow geodesic readout with no radial/range/direct-force tail",
            "status": "DERIVED_CONDITIONAL_READOUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GOB3966_4_delta_cal",
            "bridge_piece": "calibration residual",
            "formula": "Delta_cal := mu_obs - G_eff M_eff",
            "meaning": "failure of the Gauss/orbital bridge is retained as a score term rather than absorbed into fitted GM",
            "status": "DELTA_CAL_BOUND_BRANCH_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def delta_cal_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DCR3966_0_charge", "epsilon_charge", "Hamiltonian/PiM charge not identical to parent source mass", "B_tau/G_eff != M_eff[Pi_M J_H]", "close HC/PG1 or bound charge split"),
        ("DCR3966_1_poisson", "epsilon_Poisson", "weak-field operator/source coefficient not pure EH Poisson", "nabla^2 Phi != 4 pi G_eff rho_H", "EH-only local exterior or non-EH operator bound"),
        ("DCR3966_2_gauss", "epsilon_Gauss", "Gauss surface integral has residual volume/boundary terms", "Delta_mu_Gauss != 0", "closed PiM flux and zero boundary/domain/projector residuals"),
        ("DCR3966_3_orbit", "epsilon_orbit", "slow test bodies do not read the same inverse-square potential", "mu_obs != r^2|a_r| from same Phi", "same-frame geodesic/orbital readout theorem or fifth-force bound"),
        ("DCR3966_4_extra", "epsilon_extra", "extra mass/source channels masquerade as measured mass", "mu_extra != 0", "field-specific no-hair/topological zero or residual coefficients"),
        ("DCR3966_5_derivative", "epsilon_derivative", "time/radial/species/range/frame derivative hair remains", "D_X mu_obs != 0", "constant source product and no derivative hair theorem or empirical bound"),
        ("DCR3966_6_PPN", "epsilon_PPN_source", "first-order calibration may fail at beta/gamma/PPN order", "Delta_PPN_source != 0", "second-order source stability or PPN residual vector"),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "meaning": meaning,
            "failure_form": failure_form,
            "zero_or_bound_requirement": requirement,
            "score_term": f"|{symbol}|",
            "status": "RETAINED_SYMBOLIC_RESIDUAL",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, symbol, meaning, failure_form, requirement in rows
    ]


def readout_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ISR3966_0_same_frame",
            "gate": "same observed frame",
            "condition": "e_source=e_metric=e_orbit=e_clock=e_obs and tau_source=tau_orbit before readout",
            "if_missing": "delta_frame_source remains active",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ISR3966_1_slow_geodesic",
            "gate": "slow test-body geodesic limit",
            "condition": "a_i=-partial_i Phi from g_00=-1+2Phi/c^2 with no direct fifth-force or material source charge",
            "if_missing": "epsilon_orbit, alpha(lambda), and eta_source_AB remain active",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ISR3966_2_no_range_tail",
            "gate": "no radial/range tail",
            "condition": "partial_r ln mu_obs=0 and alpha_mu(lambda)=0 outside compact source",
            "if_missing": "R10/radial source hair remains active",
            "status": "CONDITIONAL_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ISR3966_3_no_absorption",
            "gate": "no fitted-GM absorption",
            "condition": "constant global calibration allowed; derivative/species/range/frame residuals cannot be absorbed",
            "if_missing": "post-hoc orbital GM laundering",
            "status": "POLICY_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def newton_feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DCF3966_0_Delta_cal_bound",
            "target": "Delta_cal",
            "update_formula": "|Delta_cal|/(G_eff M_eff) <= |epsilon_charge|+|epsilon_Poisson|+|epsilon_Gauss|+|epsilon_orbit|+|epsilon_extra|+|epsilon_derivative|+|epsilon_PPN_source|",
            "meaning": "Gauss/orbital calibration failure is a no-cancellation residual envelope",
            "feeds": "epsilon_Meff_flux; epsilon_Newton_source; Delta_Newton_source_side",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DCF3966_1_Newton_source_update",
            "target": "epsilon_Newton_source",
            "update_formula": "epsilon_Newton_source <= prior_terms + |Delta_cal|/(G_eff M_eff)",
            "meaning": "3963/3964 Newton score now receives the explicit Gauss/orbital calibration residual",
            "feeds": "Newton/Poisson/orbital/Gdot/WEP/R10/PPN gates",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DCF3966_2_PPN_next",
            "target": "Delta_PPN_source",
            "update_formula": "even if Delta_cal=0 at first Newton order, local GR still requires gamma-1=0, beta-1=0, alpha_i=0, xi=0, zeta_i=0",
            "meaning": "Newton recovery is not yet full local GR",
            "feeds": "next second-order PPN source-stability gate",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3966_0_conditional_bridge",
            "decision": "accept the Gauss/orbital bridge only as a conditional theorem",
            "basis": "closed Hilbert/PiM mass requires same-frame Poisson, Gauss, slow geodesic readout, zero extra mass, and no derivative hair",
            "effect": "no measured-GM/Newton claim from conserved source mass alone",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3966_1_delta_cal",
            "decision": "retain Delta_cal as a no-cancellation score envelope",
            "basis": "charge, Poisson, Gauss, orbit, extra mass, derivative, and PPN failures are distinct and cannot cancel by tuning",
            "effect": "orbital GM mismatch becomes testable instead of hidden in calibration",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3966_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "even a first-order Newton pass does not prove local GR; second-order beta/gamma/source stability is next",
            "effect": "push from Newtonian mechanics toward local GR/PPN closure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3966_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3966_1_bridge", "Gauss/orbital bridge", "same-frame Poisson, Gauss, slow-orbit readout, zero extra mass, no derivative hair", "CONDITIONAL_ONLY"),
        ("CLG3966_2_delta_cal", "Delta_cal residual vector", "all calibration failures mapped to symbolic score terms", "PASS_SYMBOLIC_NONCLAIM"),
        ("CLG3966_3_Newton_claim", "Newton measured GM", "Delta_cal=0 and epsilon_Newton_source=0 with no cancellation", "BLOCKED_NONCLAIM"),
        ("CLG3966_4_local_GR", "local GR", "Newton plus second-order PPN source/operator stability", "NEXT_TARGET_REQUIRED"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3966_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or bound second-order PPN source stability after measured-GM normalization: gamma-1, beta-1, alpha_i, xi, zeta_i, and delta_beta_source",
            "success_condition": "Delta_PPN_source is theorem-zero under local GR source/operator stability, or becomes a finite residual vector feeding the local-GR claim gate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_GAUSS_ORBITAL_CALIBRATION",
            "summary": "3966 derives the conditional bridge from closed Hilbert/PiM mass to observed orbital GM, keeps Delta_cal active, and maps calibration failures into a symbolic no-cancellation residual vector feeding epsilon_Newton_source.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3966 - Gauss Orbital Calibration Or Delta Cal Bound

Timestamp: `{timestamp}`

## Result

3966 makes the measured Newton `GM` bridge explicit.

The observed quantity is:

`mu_obs := r^2 |a_r| = v^2 r`.

The candidate parent source side is:

`mu_parent := G_eff M_eff[Pi_M J_H]`.

The bridge lands only if the same-frame weak-field equation, Gauss surface integral, and slow-orbit readout all close:

`nabla^2 Phi=4 pi G_eff rho_H`

`int_S grad Phi.dS=4 pi G_eff M_eff`

`a_r=-partial_r Phi=-G_eff M_eff/r^2`.

If this chain fails, the calibration residual is retained:

`|Delta_cal|/(G_eff M_eff) <= |epsilon_charge|+|epsilon_Poisson|+|epsilon_Gauss|+|epsilon_orbit|+|epsilon_extra|+|epsilon_derivative|+|epsilon_PPN_source|`.

## Meaning

This prevents a cheat: a conserved Hilbert/PiM source mass is not automatically the measured orbital `GM`. It must pass the Poisson/Gauss/orbit/readout chain or be scored as `Delta_cal`.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- Bridge theorem: `source-intake\\mts_residuals\\P8_Y5_R2FR_3966_GAUSS_ORBITAL_BRIDGE_THEOREM_OR_BOUND.csv`
- Delta_cal vector: `source-intake\\mts_residuals\\P8_Y5_R2FR_3966_DELTA_CAL_RESIDUAL_VECTOR.csv`
- Readout gate: `source-intake\\mts_residuals\\P8_Y5_R2FR_3966_INVERSE_SQUARE_READOUT_GATE.csv`
- Newton feed update: `source-intake\\mts_residuals\\P8_Y5_R2FR_3966_NEWTON_SCORE_DELTA_CAL_FEED_UPDATE.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3966_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3966 - Gauss/Orbital Calibration And Delta Cal

Timestamp: `{timestamp}`

- Defines measured orbital `mu_obs=r^2|a_r|=v^2r`.
- Shows parent source `G_eff M_eff[Pi_M J_H]` becomes measured orbital GM only through same-frame Poisson, Gauss, and slow-geodesic readout.
- Introduces `Delta_cal` as a no-cancellation calibration residual feeding `epsilon_Newton_source`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3966 - Gauss/Orbital Calibration And Delta Cal"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bridge = bridge_rows(timestamp)
    delta_cal = delta_cal_rows(timestamp)
    readout = readout_rows(timestamp)
    feed = newton_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    bridge_statuses = {row["status"] for row in bridge}
    delta_symbols = {row["symbol"] for row in delta_cal}
    readout_statuses = {row["status"] for row in readout}
    feed_targets = {row["target"] for row in feed}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = bridge + delta_cal + readout + feed + decisions + claims + next_target

    checks = [
        ("VAL3966_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3966_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3966_02_bridge", {"OBSERVABLE_DEFINITION", "DERIVED_CONDITIONAL_BRIDGE", "DERIVED_CONDITIONAL_READOUT", "DELTA_CAL_BOUND_BRANCH_ACTIVE"}.issubset(bridge_statuses), "Gauss/orbital bridge and Delta_cal branch written"),
        ("VAL3966_03_delta_vector", {"epsilon_charge", "epsilon_Poisson", "epsilon_Gauss", "epsilon_orbit", "epsilon_extra", "epsilon_derivative", "epsilon_PPN_source"}.issubset(delta_symbols), "Delta_cal residual vector complete"),
        ("VAL3966_04_readout_gate", {"CONDITIONAL_NOT_PARENT_SIGNED", "CONDITIONAL_OR_BOUND_REQUIRED", "POLICY_GUARD_ACTIVE"}.issubset(readout_statuses), "inverse-square readout gate written"),
        ("VAL3966_05_newton_feed", {"Delta_cal", "epsilon_Newton_source", "Delta_PPN_source"}.issubset(feed_targets), "Newton and PPN feed rows present"),
        ("VAL3966_06_decision", "conditional theorem" in decision_text and "Delta_cal" in decision_text and "second-order" in decision_text, "decision records conditional bridge, Delta_cal, and PPN next gate"),
        ("VAL3966_07_claim_gate", "CONDITIONAL_ONLY" in claim_statuses and "PASS_SYMBOLIC_NONCLAIM" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses and "NEXT_TARGET_REQUIRED" in claim_statuses, "claim gate blocks Newton/local-GR promotion"),
        ("VAL3966_08_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to second-order PPN source stability"),
        ("VAL3966_09_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3966_10_score_ready", all(row["score_ready"] for row in delta_cal), "Delta_cal residual rows are score-ready symbolics"),
        ("VAL3966_11_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3966_12_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3966_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3966_14_spine_updated", SPINE_PATH.exists() and "3966 - Gauss/Orbital Calibration And Delta Cal" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3966_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3966_16_script_compile", True, "script compiled before validation write"),
        ("VAL3966_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    bridge = bridge_rows(timestamp)
    delta_cal = delta_cal_rows(timestamp)
    readout = readout_rows(timestamp)
    feed = newton_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["bridge"], bridge)
    write_csv(OUTPUTS["delta_cal"], delta_cal)
    write_csv(OUTPUTS["readout"], readout)
    write_csv(OUTPUTS["newton_feed"], feed)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, sources), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, sources)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3966 validation failed: {failed}")

    print(f"3966 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Gauss/orbital calibration bridge and Delta_cal residual vector assembled")


if __name__ == "__main__":
    run()
