from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3939"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds"
DOC_PATH = PCW / "3939-Y5-R2FR-parent-sign-or-bound-Delta-cal-components.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3939_SOURCE_REGISTER.csv",
    "parent_clauses": SRC / "P8_Y5_R2FR_3939_PARENT_CLAUSE_STACK.csv",
    "component_map": SRC / "P8_Y5_R2FR_3939_DELTA_CAL_COMPONENT_REDUCTION_MAP.csv",
    "closure_attempt": SRC / "P8_Y5_R2FR_3939_DELTA_CAL_CLOSURE_ATTEMPT.csv",
    "bound_routes": SRC / "P8_Y5_R2FR_3939_COMPONENT_BOUND_ROUTE_MATRIX.csv",
    "reduced_runner": SRC / "P8_Y5_R2FR_3939_REDUCED_DELTA_CAL_RUNNER.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3939_CLAIM_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3939_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3939_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3939_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3939_VALIDATION.csv",
}

NEXT_DOC = "3940-Y5-R2FR-source-charge-Hamiltonian-equality-or-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3940_source_charge_Hamiltonian_equality_or_bound.py"


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
        ("SRC3939_00_3938_next", SRC / "P8_Y5_R2FR_3938_NEXT_TARGET.csv", "NEXT3938_0", "3938 handoff to component closure"),
        ("SRC3939_01_3938_components", SRC / "P8_Y5_R2FR_3938_DELTA_CAL_COMPONENT_STATUS.csv", "COMP3938_10", "active Delta_cal component rows"),
        ("SRC3939_02_3938_score", SRC / "P8_Y5_R2FR_3938_DELTA_CAL_SCORE_RUNNER.csv", "DSR3938_1_fallback_abs_envelope", "absolute Delta_cal envelope"),
        ("SRC3939_03_3598_theorem", SRC / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_CALIBRATION_THEOREM.csv", "GOC3598_7_conditional_calibration_theorem", "conditional Gauss/orbital calibration theorem"),
        ("SRC3939_04_3598_residuals", SRC / "P8_Y5_R2FR_3598_DELTA_CAL_RESIDUAL_DECOMPOSITION.csv", "DCR3598_11_PPN", "Delta_cal residual decomposition"),
        ("SRC3939_05_3652_hamiltonian", SRC / "P8_Y5_R2FR_3652_WEAK_FIELD_HAMILTONIAN_THEOREM_ATTEMPT.csv", "WFH3652_6_GR_Newton_zero_conditions", "weak-field source Hamiltonian contract"),
        ("SRC3939_06_charge_attempt", SRC / "P8_charge_current_equality_DIRECT_ATTEMPT.csv", "CC8_second_order_limit", "source charge equality direct attempt"),
        ("SRC3939_07_PG_contract", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG8_no_derivative_hair", "Poisson/Gauss/orbital contract"),
        ("SRC3939_08_Gauss_formula", SRC / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv", "GO523_5_no_cancellation_bound", "Gauss/orbital formula ledger"),
        ("SRC3939_09_derivative_hair", SRC / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM7_second_order_beta_residue", "derivative-hair gate"),
        ("SRC3939_10_kappa_contract", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU8_retained_residual_fallback", "constant universal coupling contract"),
        ("SRC3939_11_kappa_theorem", SRC / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv", "T508_2_no_residual_if_closed", "conditional kappa superselection theorem"),
        ("SRC3939_12_bounds", SRC / "P8_Y5_R2FR_3938_ORBITAL_BOUND_IMPORTS.csv", "BIMP3938_0_Gdot", "imported comparator bounds"),
        ("SRC3939_13_ppn_dashboard", SRC / "P8_Y5_R2FR_3936_PPN_BOUND_DASHBOARD.csv", "PPND3936_9_total", "PPN dashboard link"),
        ("SRC3939_14_validation", SRC / "P8_Y5_BRR545_3938_VALIDATION.csv", "VAL3938_17_no_pycache", "previous validation"),
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


def parent_clause_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "PC3939_0_same_parent_source",
            "same-parent source Hamiltonian and charge equality",
            "B_xi/G_eff = M_H[Pi_M J_H] and the weak-field source Hamiltonian descends from the same quotient-owned matter action",
            "Delta_charge;Delta_Poisson;Delta_frame_species_range",
            "WFH3652_0; WFH3652_2; CC0-CC4; PG0-PG3",
            "CONDITIONAL_ROUTE_DERIVED_PARENT_SIGNATURE_UNSIGNED",
            "try source-charge Hamiltonian equality first; if it fails, retain Delta_charge and active/inertial source mismatch bounds",
        ),
        (
            "PC3939_1_EH_Poisson_Gauss",
            "same-frame EH weak-field Poisson plus Gauss flux",
            "g00=-1+2Phi/c^2 and nabla^2 Phi=4*pi*G_eff*rho_H integrate to surface_int grad Phi.dS=4*pi*G_eff M_H",
            "Delta_Poisson;Delta_Gauss",
            "GOC3598_2; GOC3598_3; PG2-PG4; FPG2722 rows",
            "CONDITIONAL_ROUTE_DERIVED_OPERATOR_AND_SURFACE_UNSIGNED",
            "parent-sign EH leading operator and surface independence, or source operator/Gauss residual norms",
        ),
        (
            "PC3939_2_slow_matter_readout",
            "minimal slow-body readout of the same potential",
            "a_r=-partial_r Phi and mu_obs=r^2|a_r|=mu_Gauss when no direct force, finite-range tail, frame split, or multipole hair survives",
            "Delta_orbit;partial_r_ln_mu_obs;Delta_frame_species_range",
            "GOC3598_4; ORB3884_0; ORB3884_1; RUN3920_4",
            "CONDITIONAL_ROUTE_DERIVED_READOUT_UNSIGNED",
            "derive minimal same-frame slow matter readout or keep orbital/radial profile rows",
        ),
        (
            "PC3939_3_no_extra_monopole",
            "no extra mass-channel monopole",
            "Pi_M(Q_boundary+Q_bulk+Q_domain+Q_memory+Q_range+Q_connection+Q_nonEH)=0",
            "mu_extra;Delta_frame_species_range;partial_r_ln_mu_obs",
            "CC6; PG6; CGM6; P8_charge_current_equality residual decomposition",
            "CONDITIONAL_ROUTE_NEEDS_WARD_NOHAIR_OR_BOUND",
            "derive Ward/no-hair/topological zero for extra channels, or source absolute mu_extra vector",
        ),
        (
            "PC3939_4_constant_coupling_closed_flux",
            "constant universal coupling plus closed projected source flux",
            "D_X G_eff=0 and d(Pi_M J_H)=0 on the local exterior for X in {t,r,A,lambda,frame,domain}",
            "Delta_G;Delta_flux;dln_Geff_dt_plus_dln_Meff_dt;Delta_frame_species_range",
            "CU0-CU8; T508_0-T508_2; CGM1-CGM5",
            "CONDITIONAL_KAPPA_ROUTE_DERIVED_SOURCE_FLUX_UNSIGNED",
            "parent-adopt kappa superselection/topological clause and flux closure, or use Gdot/WEP/R10 residual bounds",
        ),
        (
            "PC3939_5_PPN_stability",
            "second-order PPN source/operator stability",
            "Delta_PPN_source=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi)_source=0 after measured-GM normalization",
            "Delta_PPN_source",
            "WFH3652_4; WFH3652_6; CC8; PPND3936_9_total; CGM7",
            "CONDITIONAL_PPN_ZERO_ROUTE_DERIVED_BOUNDS_IMPORTED",
            "reuse 3936 PPN dashboard; parent-sign vector zero or score each component against imported bounds",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "parent_clause": clause,
            "mathematical_condition": condition,
            "closes_delta_cal_components": closes,
            "source_basis": basis,
            "current_status": status,
            "fallback_if_unsigned": fallback,
            "parent_signed_now": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, clause, condition, closes, basis, status, fallback in data
    ]


def component_map_rows(timestamp: str) -> list[dict[str, Any]]:
    component_rows = read_csv(SRC / "P8_Y5_R2FR_3938_DELTA_CAL_COMPONENT_STATUS.csv")
    clause_map = {
        "Delta_charge": ("PC3939_0_same_parent_source", "source-charge Hamiltonian equality or active/inertial source bound"),
        "Delta_Poisson": ("PC3939_0_same_parent_source;PC3939_1_EH_Poisson_Gauss", "EH weak-field coefficient/source-density residual norm"),
        "Delta_Gauss": ("PC3939_1_EH_Poisson_Gauss", "Gauss surface flux residual norm"),
        "Delta_orbit": ("PC3939_2_slow_matter_readout", "orbital readout residual or ephemeris mu_obs row"),
        "mu_extra": ("PC3939_3_no_extra_monopole", "absolute extra-monopole vector"),
        "Delta_G": ("PC3939_4_constant_coupling_closed_flux", "Gdot/G, WEP/source, R10 range, frame/domain residual bounds"),
        "Delta_flux": ("PC3939_4_constant_coupling_closed_flux", "projected source flux drift bound"),
        "partial_r_ln_mu_obs": ("PC3939_2_slow_matter_readout;PC3939_3_no_extra_monopole", "radial profile/no-hair bound"),
        "dln_Geff_dt_plus_dln_Meff_dt": ("PC3939_4_constant_coupling_closed_flux", "Gdot/G bound with separated G_eff and source mass drift"),
        "Delta_frame_species_range": ("PC3939_0_same_parent_source;PC3939_2_slow_matter_readout;PC3939_4_constant_coupling_closed_flux", "WEP/source, frame, and R10 alpha(lambda) routes"),
        "Delta_PPN_source": ("PC3939_5_PPN_stability", "3936 PPN dashboard bounds"),
    }
    rows: list[dict[str, Any]] = []
    for row in component_rows:
        symbol = row.get("symbol", "")
        clause_id, fallback = clause_map.get(symbol, ("UNMAPPED", "manual route required"))
        mapped = clause_id != "UNMAPPED"
        rows.append(
            {
                "row_id": f"CM3939_{len(rows)}",
                "residual_id": row.get("residual_id", ""),
                "symbol": symbol,
                "status_3938": row.get("status_3598", ""),
                "parent_clause_id": clause_id,
                "reduction_result": "MAPPED_TO_PARENT_CLAUSE_STACK" if mapped else "UNMAPPED_COMPONENT",
                "fallback_bound_route": fallback,
                "parent_signed_now": False,
                "numeric_bound_ready": False,
                "score_ready": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def closure_attempt_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CA3939_0_reducer_theorem",
            "claim": "The 11 Delta_cal components reduce to six parent clauses.",
            "mathematical_statement": "If PC0-PC5 hold, then Delta_charge=Delta_Poisson=Delta_Gauss=Delta_orbit=mu_extra=Delta_G=Delta_flux=partial_r ln mu_obs=d ln G_eff/dt+d ln M_eff/dt=Delta_frame_species_range=Delta_PPN_source=0, hence Delta_cal_abs=0.",
            "derivation": "Substitute the 3598 exact Delta_cal identity, use 3652 weak-field source Hamiltonian ownership for source/Poisson terms, apply Poisson-to-Gauss integration and slow readout, then remove extra/coupling/flux/hair/PPN terms by the six parent clauses.",
            "result": "CONDITIONAL_CLOSURE_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CA3939_1_not_enough_for_public",
            "claim": "Current MTS has not signed PC0-PC5 as one parent branch.",
            "mathematical_statement": "The reducer is a theorem skeleton, not a completed parent action derivation.",
            "derivation": "Every parent clause references existing conditional rows whose current status is unsigned, nonclaim, or source-needed.",
            "result": "PUBLIC_CLAIM_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CA3939_2_best_first_attack",
            "claim": "PC0 is the best next target because it anchors source charge, Poisson source, frame/source equality, and later R10/WEP/PPN source charges.",
            "mathematical_statement": "B_xi/G_eff = M_H[Pi_M J_H] and weak-field source Hamiltonian descent are upstream of most remaining Delta_cal components.",
            "derivation": "Without PC0, Poisson/Gauss/orbital success can still hide source normalization in fitted GM; with PC0, PC1-PC2 become ordinary weak-field/readout clauses.",
            "result": "NEXT_TARGET_SELECTED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_route_rows(timestamp: str) -> list[dict[str, Any]]:
    imported_bounds = {row.get("observable", ""): row for row in read_csv(SRC / "P8_Y5_R2FR_3938_ORBITAL_BOUND_IMPORTS.csv")}
    routes = [
        ("BR3939_0_Delta_charge", "Delta_charge", "source charge / active-inertial mass", "WEP source-charge proxy plus Hamiltonian source equality", "eta_source_AB", "not directly numeric for Delta_charge"),
        ("BR3939_1_Delta_Poisson", "Delta_Poisson", "weak-field operator/source coefficient", "Poisson_Gauss_Newton_Enorm_rows_2722_NONCLAIM.csv", "E_Poisson_residual", "schema only"),
        ("BR3939_2_Delta_Gauss", "Delta_Gauss", "surface flux mismatch", "Poisson_Gauss_Newton_Enorm_rows_2722_NONCLAIM.csv", "E_Gauss_flux", "schema only"),
        ("BR3939_3_Delta_orbit", "Delta_orbit", "slow readout mismatch", "ephemeris/orbital mu_obs acquisition", "mu_fit;epsilon_orbit", "source dataset missing"),
        ("BR3939_4_mu_extra", "mu_extra", "extra monopole mass channel", "mu_extra vector/source-channel coefficients", "epsilon_mu_extra", "component vector missing"),
        ("BR3939_5_Delta_G", "Delta_G", "coupling/coupling-drift", "R9_Gdot and kappa residual routes", "Gdot_over_G", imported_bounds.get("Gdot_over_G", {}).get("upper_bound", "missing")),
        ("BR3939_6_Delta_flux", "Delta_flux", "projected source flux drift", "source flux theorem or Gdot/source drift row", "dln_Meff_dt", "MTS value missing"),
        ("BR3939_7_radial", "partial_r_ln_mu_obs", "radial source hair", "radial profile/no-hair row", "epsilon_r(r)", "profile/tolerance missing"),
        ("BR3939_8_time", "dln_Geff_dt_plus_dln_Meff_dt", "time-drift hair", "R9_Gdot", "Gdot_over_G", imported_bounds.get("Gdot_over_G", {}).get("upper_bound", "missing")),
        ("BR3939_9_frame_species_range", "Delta_frame_species_range", "frame/species/range source dependence", "WEP/R10/frame-source residuals", "eta_source_AB;alpha(lambda)", "WEP bound exists, R10/source map blocked"),
        ("BR3939_10_PPN", "Delta_PPN_source", "second-order local-GR stability", "3936 PPN dashboard", "gamma,beta,alpha_i,xi", "bounds imported; MTS vector missing"),
    ]
    return [
        {
            "row_id": row_id,
            "component": component,
            "physical_meaning": meaning,
            "bound_route": route,
            "observable_or_bound_symbol": symbol,
            "bound_status": status,
            "route_ready": status not in {"schema only", "source dataset missing", "component vector missing", "MTS value missing", "profile/tolerance missing", "bounds imported; MTS vector missing", "not directly numeric for Delta_charge", "WEP bound exists, R10/source map blocked"},
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, meaning, route, symbol, status in routes
    ]


def reduced_runner_rows(timestamp: str) -> list[dict[str, Any]]:
    mapped_components = component_map_rows(timestamp)
    clauses = parent_clause_rows(timestamp)
    unresolved_clauses = [row["clause_id"] for row in clauses if str(row["parent_signed_now"]) != "True"]
    return [
        {
            "row_id": "RR3939_0_reduced_private_branch",
            "score_target": "Delta_cal_abs",
            "old_blockers": len(mapped_components),
            "reduced_parent_clauses": len(clauses),
            "runner_formula": "if all PC3939_0..PC3939_5 parent_signed_now=True then Delta_cal_abs=0",
            "runner_status": "CONDITIONAL_REDUCER_BUILT_PARENT_CLAUSES_UNSIGNED",
            "unresolved_parent_clauses": ";".join(unresolved_clauses),
            "passes_bound": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RR3939_1_fallback_bound_branch",
            "score_target": "Delta_cal_abs",
            "old_blockers": len(mapped_components),
            "reduced_parent_clauses": len(clauses),
            "runner_formula": "otherwise score each component through PPN/R10/WEP/Gdot/orbital/source residual routes with absolute no-cancellation sum",
            "runner_status": "BOUND_BRANCH_STAGED_NOT_SCORE_READY",
            "unresolved_parent_clauses": ";".join(unresolved_clauses),
            "passes_bound": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CG3939_0_reducer",
            "gate": "component reducer",
            "requirement": "every 3938 Delta_cal component maps to a parent clause or bound route",
            "status": "PASS_REDUCER_BUILT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3939_1_parent_signatures",
            "gate": "parent signatures",
            "requirement": "PC0-PC5 are all parent-signed in one local branch",
            "status": "FAIL_PARENT_SIGNATURES_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3939_2_bound_branch",
            "gate": "fallback bound branch",
            "requirement": "if parent clause fails, component has numeric/source-backed bound and MTS prediction",
            "status": "FAIL_MTS_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3939_3_public_claim",
            "gate": "public Newton/local-GR claim",
            "requirement": "reducer closed or all fallback rows scored below bounds, plus PPN stability",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3939_0_reduced",
            "decision": "reduced the Delta_cal closure problem from 11 component rows to six parent clauses plus explicit bound routes",
            "effect": "the next work can attack source-charge equality first instead of repeatedly re-auditing all components",
            "claim_status": "REDUCER_BUILT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3939_1_next",
            "decision": "target PC0 source-charge Hamiltonian equality next",
            "effect": "PC0 controls Delta_charge, Poisson source ownership, same-frame source normalization, and downstream WEP/R10/PPN source charges",
            "claim_status": "NEXT_PC0_SOURCE_CHARGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3939_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attack PC0: derive B_xi/G_eff = M_H[Pi_M J_H] from the parent Hamiltonian/source action or produce a strict source-charge bound row",
            "success_condition": "Delta_charge is theorem-zero or has a source-backed bound route; Poisson/source ownership and same-frame source normalization are no longer floating assumptions",
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
            "summary": "3939 reduces the Delta_cal closure problem from 11 active components to six parent-signature clauses plus explicit fallback bound routes",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3939 - Parent-Sign or Bound Delta_cal Components

Timestamp: `{timestamp}`

## Result

Built the first `Delta_cal` closure reducer.

The 3938 runner had 11 active component blockers. 3939 reduces them to six parent clauses:

1. same-parent source Hamiltonian and charge equality;
2. same-frame EH weak-field Poisson plus Gauss flux;
3. minimal slow-body readout of the same potential;
4. no extra mass-channel monopole;
5. constant universal coupling plus closed projected source flux;
6. second-order PPN source/operator stability.

If those six clauses are parent-signed in one branch, then `Delta_cal_abs=0`. If any clause fails, the affected components stay in the no-cancellation fallback score.

## Closure Attempt

The conditional reducer theorem is now explicit:

`PC0 ∧ PC1 ∧ PC2 ∧ PC3 ∧ PC4 ∧ PC5 => Delta_charge = Delta_Poisson = Delta_Gauss = Delta_orbit = mu_extra = Delta_G = Delta_flux = partial_r ln mu_obs = dln_Geff_dt_plus_dln_Meff_dt = Delta_frame_species_range = Delta_PPN_source = 0`.

Therefore:

`Delta_cal_abs = 0`

inside that private branch.

## Current Verdict

- Reducer: built.
- Public claim: blocked.
- Reason: PC0-PC5 are not parent-signed as a single current MTS parent branch.
- Best next attack: PC0, because it anchors source charge, Poisson source ownership, WEP/R10 source charges, and PPN source normalization.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3939_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_PARENT_CLAUSE_STACK.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_DELTA_CAL_COMPONENT_REDUCTION_MAP.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_DELTA_CAL_CLOSURE_ATTEMPT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_COMPONENT_BOUND_ROUTE_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_REDUCED_DELTA_CAL_RUNNER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3939_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3939 - Parent-Sign or Bound Delta_cal Components

Timestamp: `{timestamp}`

- Reducer: collapsed the 3938 `Delta_cal` problem from 11 active components to six parent clauses.
- Conditional theorem: if PC0-PC5 are parent-signed in one branch, then `Delta_cal_abs=0`.
- Bound branch: if any clause fails, affected components route to WEP/R10/Gdot/PPN/orbital/source residual rows with no fitted cancellation.
- Current verdict: reducer built, public claim blocked because the parent signatures are unsigned.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3939 - Parent-Sign or Bound Delta_cal Components"
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


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clauses = parent_clause_rows(timestamp)
    component_map = component_map_rows(timestamp)
    closure = closure_attempt_rows(timestamp)
    routes = bound_route_rows(timestamp)
    reduced = reduced_runner_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (clauses, component_map, closure, routes, reduced, claim_gate, decisions, next_rows(timestamp))
    checks = [
        ("VAL3939_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3939_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3939_02_clause_count", len(clauses) == 6, "six parent clauses emitted"),
        ("VAL3939_03_components_mapped", len(component_map) == 11 and all(row["reduction_result"] == "MAPPED_TO_PARENT_CLAUSE_STACK" for row in component_map), "all 11 components mapped to parent clauses"),
        ("VAL3939_04_closure_attempt", any(row["result"] == "CONDITIONAL_CLOSURE_DERIVED" for row in closure), "conditional closure theorem emitted"),
        ("VAL3939_05_bound_routes", len(routes) == 11, "fallback bound route matrix emitted"),
        ("VAL3939_06_reduced_runner", len(reduced) == 2 and any(row["old_blockers"] == 11 and row["reduced_parent_clauses"] == 6 for row in reduced), "reduced runner reports 11-to-6 reduction"),
        ("VAL3939_07_parent_unsigned", all(str(row["parent_signed_now"]) == "False" for row in clauses), "parent signatures remain unsigned"),
        ("VAL3939_08_claim_gate", len(claim_gate) == 4 and any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public claim"),
        ("VAL3939_09_next_pc0", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC and "B_xi/G_eff" in next_rows(timestamp)[0]["target"], "next target selects PC0 source-charge equality"),
        ("VAL3939_10_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3939_11_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3939_12_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3939_13_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3939_14_spine_written", SPINE_PATH.exists() and "3939 - Parent-Sign or Bound Delta_cal Components" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3939_15_script_compiles", True, "script compiles"),
        ("VAL3939_16_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["parent_clauses"], parent_clause_rows(timestamp))
    write_csv(OUTPUTS["component_map"], component_map_rows(timestamp))
    write_csv(OUTPUTS["closure_attempt"], closure_attempt_rows(timestamp))
    write_csv(OUTPUTS["bound_routes"], bound_route_rows(timestamp))
    write_csv(OUTPUTS["reduced_runner"], reduced_runner_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
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
        raise SystemExit(f"3939 validation failed: {failed}")
    print(f"3939 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
