from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3826"
BRANCH = "MTS_R2FR_Y5_COMPACT_EXTERIOR_SOURCE_KERNEL_CLOSURE_SCORECARD_3826"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3826-Y5-R2FR-compact-exterior-source-kernel-closure-scorecard.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3825 = PCW / "3825-Y5-R2FR-boundary-reference-primitive-and-MHref-denominator-zero-or-first-source-row.md"
CSV_3825_RESID = OUT / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv"
CSV_3825_FIRST = OUT / "P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv"
CSV_3825_GATES = OUT / "P8_Y5_R2FR_3825_CLAIM_GATES.csv"
CSV_3824_RESID = OUT / "P8_Y5_R2FR_3824_R_EQ_BOUNDARY_RESIDUAL_ROWS.csv"
CSV_3823_RESID = OUT / "P8_Y5_R2FR_3823_PIM_TOTAL_RESIDUAL_ROWS.csv"
CSV_3822_LEDGER = OUT / "P8_Y5_R2FR_3822_LOCAL_ARENA_SOURCE_LEDGER.csv"
CSV_3822_TEST = OUT / "P8_Y5_R2FR_3822_LOCAL_TEST_READY_SOURCE_ROWS.csv"
CSV_3821_RESID = OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_RESIDUAL_ROWS.csv"
CSV_3820_RESID = OUT / "P8_Y5_R2FR_3820_ACTIVE_MASS_RESIDUAL_ROWS.csv"
CSV_3818_RESID = OUT / "P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3826_SOURCE_REGISTER.csv",
    "scorecard": OUT / "P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv",
    "arena_matrix": OUT / "P8_Y5_R2FR_3826_ARENA_CLOSURE_MATRIX.csv",
    "residual_bundle": OUT / "P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv",
    "roadmap": OUT / "P8_Y5_R2FR_3826_ZERO_OR_SOURCE_ROW_ROADMAP.csv",
    "gates": OUT / "P8_Y5_R2FR_3826_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3826_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3826_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3826_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3826_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3826_0_3825_doc", P_3825, "First Source-Ready Rows"),
    ("SRC3826_1_3825_residual_total", CSV_3825_RESID, "R3825_4_total"),
    ("SRC3826_2_3825_first_source_rows", CSV_3825_FIRST, "FSR3825_0_B_zero_flux"),
    ("SRC3826_3_3825_claim_gate", CSV_3825_GATES, "GATE3825_5_claim_ready_boundary_bundle"),
    ("SRC3826_4_3824_R_eq_total", CSV_3824_RESID, "R3824_5_total"),
    ("SRC3826_5_3823_PiM_total", CSV_3823_RESID, "R3823_6_total"),
    ("SRC3826_6_3822_local_arena_ledger", CSV_3822_LEDGER, "ARENA3822_0_R10_lab"),
    ("SRC3826_7_3822_local_test_rows", CSV_3822_TEST, "LTR3822_0_R10_alpha_lambda"),
    ("SRC3826_8_3821_stress_virial_total", CSV_3821_RESID, "R3821_5_total"),
    ("SRC3826_9_3820_active_mass_total", CSV_3820_RESID, "R3820_5_total"),
    ("SRC3826_10_3818_EH_Poisson_residual", CSV_3818_RESID, "R3818_5_total"),
    ("SRC3826_11_3818_Poisson_derivation", CSV_3818_POISSON, "POI3818_0_linearized_00"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_compact_exterior_source_kernel_scorecard",
                "claim_use": "provenance_only_not_public_claim",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def kernel_clause_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "KSC3826_0_EH_to_Poisson",
            "kernel_clause": "linearized Einstein-Hilbert 00 equation must reduce to Poisson with the same source normalization",
            "status": "ZERO_ROUTE_CONDITIONAL",
            "zero_route": "3818 supplies the weak-field algebra route when the EH owner and normalization are fixed",
            "finite_row": "R3818_5_total",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital;EM",
            "claim_blocker": "MISSING_EH_OWNER_SOURCE_LOCK_OR_VISIBLE_G_NORMALIZATION_CERTIFICATE",
            "source_artifact": rel(CSV_3818_RESID),
            "next_action": "keep as kernel clause; do not use orbital GM fits as independent source mass",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_1_active_mass_selector",
            "kernel_clause": "the compact source must select active gravitational mass rather than fitted product GM by hand",
            "status": "ZERO_ROUTE_CONDITIONAL_OR_SOURCE_ROW_REQUIRED",
            "zero_route": "3820 Komar/Tolman branch identifies the active-mass candidate in stationary weak-field limit",
            "finite_row": "R3820_5_total",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital",
            "claim_blocker": "MISSING_INDEPENDENT_SOURCE_LEDGER_VALUES_AND_SELECTOR_CERTIFICATE",
            "source_artifact": rel(CSV_3820_RESID),
            "next_action": "bind source rows to lab/astronomical source definitions without importing fitted mu=GM as source evidence",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_2_closed_system_stress_virial",
            "kernel_clause": "pressure and binding stresses must cancel or be bounded for closed stationary compact sources",
            "status": "ZERO_ROUTE_CONDITIONAL_OR_BOUND",
            "zero_route": "3821 gives the closed total-source stress-virial cancellation route",
            "finite_row": "R3821_5_total",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital",
            "claim_blocker": "MISSING_CLOSED_SOURCE_OR_PRESSURE_BINDING_BOUND_ROW_PER_ARENA",
            "source_artifact": rel(CSV_3821_RESID),
            "next_action": "for non-closed or finite apparatus systems emit pressure/binding residual instead of claiming equality",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_3_local_arena_source_ledger",
            "kernel_clause": "every local test arena must have independent source rows rather than placeholders or post-fit products",
            "status": "SOURCE_ROW_READY_NONCLAIM",
            "zero_route": "none; this is evidence plumbing not a theorem zero",
            "finite_row": "ARENA3822_0_R10_lab through ARENA3822_5_EM",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital;EM",
            "claim_blocker": "MISSING_NUMERIC_PARENT_OWNED_SOURCE_VALUES",
            "source_artifact": rel(CSV_3822_LEDGER),
            "next_action": "convert priority rows into dry-run smoke inputs while keeping valid_for_claim=false",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_4_PiM_commutator",
            "kernel_clause": "the matter/source projector Pi_M must commute with d on the fixed compact exterior worldtube",
            "status": "ZERO_ROUTE_CONDITIONAL",
            "zero_route": "3823 fixed total-system worldtube and homology class make dPi_M_total=0 on the exterior annulus",
            "finite_row": "R3823_6_total",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital;EM",
            "claim_blocker": "MISSING_FIXED_DOMAIN_AND_ARENA_PROJECTOR_NATURALITY_SIGNATURES",
            "source_artifact": rel(CSV_3823_RESID),
            "next_action": "keep moving-domain/readout-mask terms explicit as residuals",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_5_topological_Hilbert_equality",
            "kernel_clause": "Pi_M J_H must equal the matter topological current plus exact boundary and R_eq residual",
            "status": "ZERO_ROUTE_CONDITIONAL",
            "zero_route": "3824 same compact Hilbert worldtube/source measure/Poincare dual closes R_eq conditionally",
            "finite_row": "R3824_5_total",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital;EM",
            "claim_blocker": "MISSING_SAME_OBJECT_DE_RHAM_AND_BOUNDARY_PRIMITIVE_SIGNATURES",
            "source_artifact": rel(CSV_3824_RESID),
            "next_action": "do not collapse R_eq into zero unless same-object clauses are signed",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_6_boundary_reference_MHref",
            "kernel_clause": "boundary/reference flux and M_H_ref denominator must vanish or be source-bounded before local GR claims",
            "status": "SOURCE_ROW_READY_NONCLAIM",
            "zero_route": "3825 gives conditional routes B_zero_flux=0, Delta_symp=0, and M_H_ref>0",
            "finite_row": "R3825_4_total",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital;EM",
            "claim_blocker": "MISSING_BOUNDARY_EXACTNESS_REFERENCE_LOCK_AND_MHREF_NUMERIC_ROW",
            "source_artifact": rel(CSV_3825_RESID),
            "next_action": "fill first source-ready boundary/MHref rows before any pass/fail local claim",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_7_PPN_readout_tail",
            "kernel_clause": "metric readout and local post-Newtonian residual vector must descend without arena-tuned coefficients",
            "status": "BLOCKED_NEXT_PROOF",
            "zero_route": "not yet parent-signed in the current compact-exterior chain",
            "finite_row": "R_PPN_readout_tail",
            "feeds_arenas": "PPN;clock;orbital;WEP",
            "claim_blocker": "MISSING_METRIC_READOUT_DESCENT_AND_GAMMA_BETA_RESIDUAL_BOUNDS",
            "source_artifact": rel(CSV_3822_TEST),
            "next_action": "3827 should dry-run local arenas and identify the first PPN/readout source rows",
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "KSC3826_8_compact_exterior_kernel_total",
            "kernel_clause": "R_kernel_total = R_EH_owner + R_Poisson_norm + R_active_mass_total + R_stress_virial_total + R_PiM_total + R_eq_boundary_total + R_boundary_MHref_total + R_source_ledger + R_PPN_readout_tail",
            "status": "INTEGRATED_NONCLAIM_SCORECARD",
            "zero_route": "all components must be zero-routed or source-bounded at the same compact exterior domain and source measure",
            "finite_row": "R_kernel_total_3826",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital;EM",
            "claim_blocker": "CLAIM_BLOCKED_UNTIL_ALL_COMPONENT_ROWS_ARE_PARENT_SIGNED_OR_NUMERIC_SOURCE_BACKED",
            "source_artifact": rel(OUTPUTS["scorecard"]),
            "next_action": "build first local dry-run smoke runner from this scorecard",
            "timestamp_utc": timestamp,
        },
    ]


def arena_matrix_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "arena_id": "ARENA3826_0_R10",
            "arena": "R10 short-range alpha(lambda)",
            "required_kernel_clauses": "KSC3826_0;KSC3826_1;KSC3826_3;KSC3826_4;KSC3826_5;KSC3826_6",
            "current_status": "DRY_RUN_ONLY",
            "claim_allowed": False,
            "first_usable_mode": "schema/interpolation/failure-mode smoke",
            "blocking_inputs": "numeric MTS alpha numerator; boundary/MHref rows; parent-owned source scale; real bound curve",
            "next_test_action": "feed 3822/3825 nonclaim rows into a 3827 dry-run and require claim=false",
            "timestamp_utc": timestamp,
        },
        {
            "arena_id": "ARENA3826_1_WEP",
            "arena": "weak equivalence principle composition tests",
            "required_kernel_clauses": "KSC3826_1;KSC3826_2;KSC3826_3;KSC3826_4;KSC3826_7",
            "current_status": "BOUND_INPUT_REQUIRED",
            "claim_allowed": False,
            "first_usable_mode": "residual-vector schema only",
            "blocking_inputs": "composition source normalizer; material stress closure; readout-map descent",
            "next_test_action": "separate source-independent WEP rows from material-dependent residual coefficients",
            "timestamp_utc": timestamp,
        },
        {
            "arena_id": "ARENA3826_2_PPN",
            "arena": "local PPN gamma/beta and preferred-frame residuals",
            "required_kernel_clauses": "KSC3826_0;KSC3826_1;KSC3826_2;KSC3826_4;KSC3826_5;KSC3826_7",
            "current_status": "BLOCKED_NEXT_PROOF",
            "claim_allowed": False,
            "first_usable_mode": "PPN residual vector ledger",
            "blocking_inputs": "metric readout descent; gamma/beta residual coefficients; independent source mass",
            "next_test_action": "derive or source-bound R_PPN_readout_tail before claiming local GR recovery",
            "timestamp_utc": timestamp,
        },
        {
            "arena_id": "ARENA3826_3_clock",
            "arena": "clock redshift and local time transport",
            "required_kernel_clauses": "KSC3826_1;KSC3826_2;KSC3826_3;KSC3826_6;KSC3826_7",
            "current_status": "SOURCE_ROW_READY_NONCLAIM",
            "claim_allowed": False,
            "first_usable_mode": "clock tau row dry-run",
            "blocking_inputs": "clock readout transport; boundary/reference lock; H_tau-H_ref row",
            "next_test_action": "tie tau_clock to the same compact exterior source kernel rather than a separate local-time ansatz",
            "timestamp_utc": timestamp,
        },
        {
            "arena_id": "ARENA3826_4_orbital",
            "arena": "orbital systems and Newtonian limit",
            "required_kernel_clauses": "KSC3826_0;KSC3826_1;KSC3826_2;KSC3826_4;KSC3826_5;KSC3826_7",
            "current_status": "PRODUCT_ONLY_GM_GUARD",
            "claim_allowed": False,
            "first_usable_mode": "anti-circularity audit",
            "blocking_inputs": "independent M and G split; source selector; PPN/readout tail",
            "next_test_action": "only use orbital mu=GM as validation output, never as the source-normalization input",
            "timestamp_utc": timestamp,
        },
        {
            "arena_id": "ARENA3826_5_EM",
            "arena": "electromagnetic stress and Poynting/wave coupling",
            "required_kernel_clauses": "KSC3826_2;KSC3826_3;KSC3826_4;KSC3826_5;KSC3826_6",
            "current_status": "EXTENSION_NONCLAIM",
            "claim_allowed": False,
            "first_usable_mode": "stress-current ledger",
            "blocking_inputs": "same-current ownership; Poynting flux boundary term; radiative readout naturality",
            "next_test_action": "treat Poynting/vector-wave route as a source-stress extension, not a shortcut around local GR",
            "timestamp_utc": timestamp,
        },
    ]


def residual_bundle_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "R3826_0_EH_owner_Poisson_norm",
            "symbol": "R_EH_owner + R_Poisson_norm",
            "source_clause": "KSC3826_0_EH_to_Poisson",
            "zero_or_bound_status": "conditional_zero_route_from_3818",
            "must_not_cancel_against": "orbital_mu_fit; arena_tuned_G; fitted_alpha",
            "feeds_arenas": "all_local",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_1_active_mass_total",
            "symbol": "R_active_mass_total",
            "source_clause": "KSC3826_1_active_mass_selector",
            "zero_or_bound_status": "conditional_active_mass_selector_or_source_row",
            "must_not_cancel_against": "post_fit_mass_proxy",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_2_stress_virial_total",
            "symbol": "R_stress_virial_total",
            "source_clause": "KSC3826_2_closed_system_stress_virial",
            "zero_or_bound_status": "closed_stationary_zero_or_pressure_binding_bound",
            "must_not_cancel_against": "unmodelled_apparatus_stress",
            "feeds_arenas": "R10;WEP;PPN;clock;orbital;EM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_3_source_ledger",
            "symbol": "R_source_ledger",
            "source_clause": "KSC3826_3_local_arena_source_ledger",
            "zero_or_bound_status": "source_rows_exist_but_nonclaim",
            "must_not_cancel_against": "placeholder_parent_coefficients",
            "feeds_arenas": "all_local",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_4_PiM_total",
            "symbol": "R_PiM_total",
            "source_clause": "KSC3826_4_PiM_commutator",
            "zero_or_bound_status": "conditional_fixed_worldtube_zero_or_projector_bound",
            "must_not_cancel_against": "moving_domain_or_readout_mask",
            "feeds_arenas": "all_local",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_5_R_eq_boundary_total",
            "symbol": "R_eq_boundary_total",
            "source_clause": "KSC3826_5_topological_Hilbert_equality",
            "zero_or_bound_status": "conditional_same_object_zero_or_boundary_bound",
            "must_not_cancel_against": "boundary_primitive_without_source",
            "feeds_arenas": "all_local",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_6_boundary_MHref_total",
            "symbol": "R_boundary_MHref_total",
            "source_clause": "KSC3826_6_boundary_reference_MHref",
            "zero_or_bound_status": "first_source_ready_nonclaim",
            "must_not_cancel_against": "unsigned_reference_lock_or_missing_denominator",
            "feeds_arenas": "all_local",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_7_PPN_readout_tail",
            "symbol": "R_PPN_readout_tail",
            "source_clause": "KSC3826_7_PPN_readout_tail",
            "zero_or_bound_status": "blocked_next_proof",
            "must_not_cancel_against": "arena_specific_metric_readout",
            "feeds_arenas": "PPN;clock;orbital;WEP",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "R3826_8_kernel_total",
            "symbol": "R_kernel_total_3826",
            "source_clause": "KSC3826_8_compact_exterior_kernel_total",
            "zero_or_bound_status": "integrated_nonclaim_until_all_rows_close",
            "must_not_cancel_against": "any_cross-arena_tuned_term",
            "feeds_arenas": "all_local",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def roadmap_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "priority": 1,
            "roadmap_id": "ROAD3826_0_dry_run_runner",
            "target": "3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md",
            "route": "turn the integrated 3826 scorecard into a dry-run runner for R10/WEP/PPN/clock/orbital/EM",
            "success_condition": "every arena runs schema/failure-mode checks and claim_allowed remains false where inputs are missing",
            "risk": "low; implementation plumbing not a physics claim",
            "timestamp_utc": timestamp,
        },
        {
            "priority": 2,
            "roadmap_id": "ROAD3826_1_boundary_MHref_fill",
            "target": "boundary/reference and M_H_ref source fill",
            "route": "populate FSR3825 rows with real source-backed values or theorem-zero signatures",
            "success_condition": "B_zero_flux, Delta_symp, and M_H_ref rows become valid_for_claim only with signed source paths",
            "risk": "medium; this is where local finite-range tails can hide",
            "timestamp_utc": timestamp,
        },
        {
            "priority": 3,
            "roadmap_id": "ROAD3826_2_PPN_readout_tail",
            "target": "derive or bound R_PPN_readout_tail",
            "route": "force gamma/beta/preferred-frame residuals to descend from the same compact exterior source kernel",
            "success_condition": "PPN arena has explicit residual vector and no arena-tuned readout coefficients",
            "risk": "high; this is the local-GR proof edge",
            "timestamp_utc": timestamp,
        },
        {
            "priority": 4,
            "roadmap_id": "ROAD3826_3_source_ledger_numbers",
            "target": "source-backed local arena numeric rows",
            "route": "source independent lab/clock/orbital/EM inputs without importing fitted outcomes as inputs",
            "success_condition": "claim-valid rows require positive numeric values, units, provenance, and no MISSING markers",
            "risk": "medium; evidence acquisition can expose missing theory coefficients",
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3826_0_sources_exist",
            "gate": "all 3818-3825 source artifacts exist and needles resolve",
            "status": "PASS",
            "claim_allowed": False,
            "reason": "provenance is present for scorecard construction only",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3826_1_kernel_scorecard_complete",
            "gate": "integrated compact-exterior source-kernel scorecard emitted",
            "status": "PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "scorecard identifies residuals; it does not close them",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3826_2_arena_matrix_complete",
            "gate": "R10/WEP/PPN/clock/orbital/EM arenas present",
            "status": "PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "all arenas remain dry-run, source-row, or blocked proof modes",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3826_3_local_GR_Newton_claim",
            "gate": "local GR/Newton recovery claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "R_PPN_readout_tail and source-backed boundary/MHref rows remain open",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3826_4_no_GM_smuggling",
            "gate": "orbital mu=GM is not used as source-mass input",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "orbital arena is product-only validation until independent M and G split is supplied",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3826_5_3827_selected",
            "gate": "next target selects dry-run smoke runner instead of another passive missing-ledger",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "3827 turns the ladder into runnable schema/failure-mode tests",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3826_0_not_claim_ready",
            "decision": "do not claim R10, WEP, PPN, clock, orbital, EM, Newton, or local GR pass from 3826",
            "basis": "3826 integrates the chain but keeps every open residual explicit",
            "consequence": "the next legitimate move is dry-run testing plus source-row fill, not public claim language",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3826_1_testing_now_allowed",
            "decision": "move toward testing in dry-run mode",
            "basis": "the closure scorecard now defines the required input rows and failure modes",
            "consequence": "3827 can run local arena gates without pretending the physics is already closed",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3826_2_best_physics_target",
            "decision": "prioritize R_PPN_readout_tail and boundary/MHref source rows after the smoke runner",
            "basis": "these are the two blockers between compact exterior source kernel and local GR/Newton reduction",
            "consequence": "the project stops circling and gets a concrete red/amber/green test dashboard",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3826_0",
            "next_checkpoint": "3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md",
            "script": "scripts/Y5_R2FR_3827_local_kernel_scorecard_to_first_smoke_test_runner.py",
            "objective": "run the 3826 compact-exterior source-kernel scorecard as dry-run local arena checks for R10/WEP/PPN/clock/orbital/EM, with explicit claim=false failure modes and a priority source-fill queue",
            "reason": "testing should start now in nonclaim dry-run mode so missing source rows become actionable inputs rather than repeated prose blockers",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_INTEGRATED_SCORECARD",
            "claim": "no local GR/Newton/R10/WEP/PPN/clock/orbital/EM claim",
            "summary": "3826 integrates the 3818-3825 compact-exterior source-kernel clauses into one closure scorecard and selects a runnable 3827 dry-run runner.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    scorecard: list[dict[str, object]],
    arenas: list[dict[str, object]],
    residuals: list[dict[str, object]],
    roadmap: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3826 — Compact Exterior Source-Kernel Closure Scorecard

Private checkpoint. This is not a local-GR/Newton/R10/WEP/PPN/clock/orbital/EM claim. It is the integrated gate that turns the 3818–3825 derivation ladder into one compact-exterior source-kernel checklist.

Generated: `{timestamp}`

## Core Kernel

The working residual is

`R_kernel_total = R_EH_owner + R_Poisson_norm + R_active_mass_total + R_stress_virial_total + R_PiM_total + R_eq_boundary_total + R_boundary_MHref_total + R_source_ledger + R_PPN_readout_tail`.

The important upgrade is that the open terms are now one object. If a future local test passes, it must pass through this kernel rather than borrowing a separate closure story for each arena.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Kernel Clause Scorecard

{markdown_table(scorecard, ["clause_id", "status", "finite_row", "claim_blocker", "next_action"])}

## Arena Closure Matrix

{markdown_table(arenas, ["arena_id", "arena", "current_status", "claim_allowed", "blocking_inputs", "next_test_action"])}

## Residual Bundle

{markdown_table(residuals, ["residual_id", "symbol", "zero_or_bound_status", "must_not_cancel_against", "claim_allowed"])}

## Zero-Or-Source-Row Roadmap

{markdown_table(roadmap, ["priority", "roadmap_id", "target", "success_condition", "risk"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3826 is progress because it stops the local branch being a pile of separate partial derivations. It says exactly what must close before MTS can honestly claim local Newton/GR recovery:

- the EH/Poisson normalization must stay source-owned;
- active mass and stress-virial closure must not borrow fitted `GM`;
- `Pi_M`, `R_eq`, boundary/reference, and `M_H_ref` must use the same compact exterior source kernel;
- `R_PPN_readout_tail` must be derived or source-bounded;
- every arena must keep `claim_allowed=false` until its source rows are real.

Next target: `3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3825", "Current State After 3826", 1)
    paragraph = (
        "`3826` integrates the 3818-3825 compact-exterior source-kernel chain into one scorecard: "
        "`R_kernel_total = R_EH_owner + R_Poisson_norm + R_active_mass_total + R_stress_virial_total + "
        "R_PiM_total + R_eq_boundary_total + R_boundary_MHref_total + R_source_ledger + R_PPN_readout_tail`. "
        "This is still nonclaim, but it converts the local-GR/Newton problem from scattered proof fragments into a runnable closure matrix: "
        "R10/WEP/PPN/clock/orbital/EM all remain `claim_allowed=false` until source-backed rows and the PPN/readout tail close.\n\n"
    )
    anchor = "`3825` converts the boundary/reference"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3826-Y5-R2FR-compact-exterior-source-kernel-closure-scorecard.md`

Target: integrate the PiM commutator, `R_eq`, boundary/reference, `M_H_ref`, stress-virial and local arena rows into one compact-exterior source-kernel closure scorecard.

This is the best next move because the individual source-kernel clauses now have zero routes or finite rows; the project needs one integrated gate to show exactly what remains before local Newton/GR testing."""
    new_gate = """`3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md`

Target: run the 3826 compact-exterior source-kernel scorecard as dry-run local arena checks for R10/WEP/PPN/clock/orbital/EM, with explicit `claim_allowed=false` failure modes and a priority source-fill queue.

This is the best next move because testing can now start safely in nonclaim mode: the runner should show which arenas are schema-ready, which fail from missing source rows, and which physics residuals block local Newton/GR recovery."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3826_ARENA_CLOSURE_MATRIX.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3826_ZERO_OR_SOURCE_ROW_ROADMAP.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3826_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3826 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3826 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    scorecard: list[dict[str, object]],
    arenas: list[dict[str, object]],
    residuals: list[dict[str, object]],
    roadmap: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL3826_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3826_1_scorecard_size",
        "kernel scorecard has integrated clauses",
        len(scorecard) >= 9 and any(row["clause_id"] == "KSC3826_8_compact_exterior_kernel_total" for row in scorecard),
        f"{len(scorecard)} scorecard rows",
    )
    required_arena_ids = {
        "ARENA3826_0_R10",
        "ARENA3826_1_WEP",
        "ARENA3826_2_PPN",
        "ARENA3826_3_clock",
        "ARENA3826_4_orbital",
        "ARENA3826_5_EM",
    }
    arena_ids = {str(row["arena_id"]) for row in arenas}
    add(
        "VAL3826_2_arena_coverage",
        "R10/WEP/PPN/clock/orbital/EM arenas are covered",
        required_arena_ids.issubset(arena_ids),
        "; ".join(sorted(arena_ids)),
    )
    add(
        "VAL3826_3_no_claims",
        "no scorecard, arena, residual, or gate row allows a claim",
        all(not bool(row.get("claim_allowed")) for row in arenas + residuals + gates),
        "claim_allowed remains false throughout generated claim-bearing rows",
    )
    add(
        "VAL3826_4_residual_total",
        "integrated R_kernel_total row exists",
        any(row["residual_id"] == "R3826_8_kernel_total" for row in residuals),
        "R3826_8_kernel_total present",
    )
    add(
        "VAL3826_5_3827_next",
        "next target is actionable dry-run smoke runner",
        any("3827" in str(row["target"]) for row in roadmap),
        "3827 dry-run runner selected",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3826_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3826_7_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "R_kernel_total" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = [path for path in FWB.rglob("*3826*") if path.is_file()] if FWB.exists() else []
    add(
        "VAL3826_8_formalization_clean",
        "formalization-workbench has no 3826 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3826 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3826_9_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    scorecard = kernel_clause_rows(timestamp)
    arenas = arena_matrix_rows(timestamp)
    residuals = residual_bundle_rows(timestamp)
    roadmap = roadmap_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["scorecard"], scorecard)
    write_csv(OUTPUTS["arena_matrix"], arenas)
    write_csv(OUTPUTS["residual_bundle"], residuals)
    write_csv(OUTPUTS["roadmap"], roadmap)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, scorecard, arenas, residuals, roadmap, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, scorecard, arenas, residuals, roadmap, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_INTEGRATED_SCORECARD")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
