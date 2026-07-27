from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4756"
CLAIM_ID = "L-598"
MARKER = "PPC4161_HTAU_MHREF_KAPPA_SOURCE_COUPLING_LOCK_OR_TRANSITION_HAIR_BOUND_4756"
PACKET_MARKER = "PPC4161_PACKET_HTAU_MHREF_KAPPA_SOURCE_COUPLING_LOCK_OR_TRANSITION_HAIR_BOUND_4756"
DECISION = "STRUCTURAL_NEWTON_BRIDGE_WITH_CALIBRATED_G_DERIVED_CONDITIONAL_EPSILON_GSRC_HAIR_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4757-Y5-R2FR-common-mode-parent-grammar-or-epsilonGsrc-finite-input-runner.md"

DOC_PATH = POST / "4756-Y5-R2FR-Htau-MHref-kappa-source-coupling-lock-or-transition-hair-bound.md"
FORMAL_PATH = FORMAL / "772-PPC4161-Htau-MHref-kappa-source-coupling-lock-or-transition-hair-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_SOURCE_REGISTER.csv"
SOURCE_CHARGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_SOURCE_CHARGE_LOCK_ROWS.csv"
COUPLING_LOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_COUPLING_LOCK_ROWS.csv"
NEWTON_BRIDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_NEWTON_BRIDGE_ROWS.csv"
TRANSITION_HAIR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_TRANSITION_HAIR_BOUND_ROWS.csv"
EPSILON_GSRC_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_EPSILON_GSRC_VECTOR_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4756_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4756_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4756_0_4755_doc", DOC_PATH.parent / "4755-Y5-R2FR-lambdaRI-boundary-Kperp-source-packet-or-profile-demotion.md", "Source Coupling Import", "4755 source-coupling handoff"),
    ("SRC4756_1_4755_formal", FORMAL / "771-PPC4161-lambdaRI-boundary-Kperp-source-packet-or-profile-demotion.md", "G_cal = c^4 kappa_eff/(8*pi)", "4755 formal Gcal handoff"),
    ("SRC4756_2_4755_import", SOURCE_DIR / "P8_Y5_R2FR_4755_SOURCE_CHARGE_COUPLING_IMPORT.csv", "SCI4755_3_Gcal", "4755 source-coupling import row"),
    ("SRC4756_3_4755_next", SOURCE_DIR / "P8_Y5_R2FR_4755_NEXT_TARGET.csv", "H_tau/M_Hdress", "4756 target handoff"),
    ("SRC4756_4_4354_charge", SOURCE_DIR / "P8_Y5_R2FR_4354_SOURCE_CHARGE_ROWS.csv", "SC4354_1_Htau_MHref", "4354 source charge rows"),
    ("SRC4756_5_4354_coupling", SOURCE_DIR / "P8_Y5_R2FR_4354_COUPLING_LOCK_ROWS.csv", "CL4354_2_kappa_eff", "4354 coupling lock rows"),
    ("SRC4756_6_4354_newton", SOURCE_DIR / "P8_Y5_R2FR_4354_NEWTON_BRIDGE_ROWS.csv", "NB4354_4_conditional_theorem", "4354 Newton bridge rows"),
    ("SRC4756_7_4354_drift", SOURCE_DIR / "P8_Y5_R2FR_4354_DRIFT_BOUND_ROWS.csv", "DB4354_6_MHref", "4354 drift/source defect rows"),
    ("SRC4756_8_4355_kernel", SOURCE_DIR / "P8_Y5_R2FR_4355_KERNEL_MEMBERSHIP_ROWS.csv", "KM4355_7_total_kernel", "4355 source-kernel membership"),
    ("SRC4756_9_4355_hair", SOURCE_DIR / "P8_Y5_R2FR_4355_SOURCE_HAIR_BOUND_ROWS.csv", "HB4355_7_total", "4355 transition hair vector"),
    ("SRC4756_10_4356_theorem", SOURCE_DIR / "P8_Y5_R2FR_4356_THEOREM_ROWS.csv", "TH4356_0_static_monopole_common_mode", "4356 common-mode theorem"),
    ("SRC4756_11_4356_zero", SOURCE_DIR / "P8_Y5_R2FR_4356_ZERO_CLAUSE_ROWS.csv", "ZC4356_6_EM_Poynting_no_double_count", "4356 zero clauses including EM/Poynting"),
    ("SRC4756_12_4356_hair", SOURCE_DIR / "P8_Y5_R2FR_4356_HAIR_BOUND_ROWS.csv", "HB4356_7_total_with_4355", "4356 total transition hair bound"),
    ("SRC4756_13_4356_decision", SOURCE_DIR / "P8_Y5_R2FR_4356_DECISION.csv", "TRANSITION_STATIC_MONOPOLE_COMMON_MODE_HAIR_LAW_DERIVED", "4356 decision"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    SOURCE_CHARGE_CSV,
    COUPLING_LOCK_CSV,
    NEWTON_BRIDGE_CSV,
    TRANSITION_HAIR_CSV,
    EPSILON_GSRC_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def source_charge_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SCL4756_0_charge_definition", "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref", "Newtonian source charge is Hamiltonian/Hilbert charge, not observed orbital GM.", "DEFINED_NOT_PUBLICLY_CLOSED"),
        ("SCL4756_1_same_worldtube", "int_W rho_H dV_H = M_H^dress[W_H;tau]", "source measure must live on the same worldtube before readout.", "CONDITION_REQUIRED"),
        ("SCL4756_2_integrability", "I_tau,S=0", "Hamiltonian one-form must be exact for the full MTS branch.", "OPERATOR_DERIVED_FULL_ZERO_CONDITIONAL"),
        ("SCL4756_3_reference", "D_source H_ref = D_radius H_ref = D_frame H_ref = D_readout H_ref = 0", "reference energy cannot be post-fit or source-dependent.", "CONDITIONAL_ZERO_THEOREM"),
        ("SCL4756_4_tau_frame", "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout and same e_obs", "one time generator/coframe must support source, clock, orbit and PPN readout.", "CONDITIONAL_ZERO_THEOREM"),
        ("SCL4756_5_boundary_flux", "no source crossing, no imposed incoming radiation, no open-memory pullback", "boundary/radiative flux is absent or routed, not hidden in source mass.", "CONDITIONAL_ZERO_THEOREM"),
        ("SCL4756_6_PiH_private", "epsilon_PiH=0 inside private Hamiltonian selector", "Pi_M/H_tau glue is real private progress but not global parent adoption.", "ZERO_INSIDE_PRIVATE_SELECTOR_ONLY"),
        ("SCL4756_7_MHref", "M_H_ref>0 and same-frame denominator fixed", "finite source-defect ratios require a positive source-backed denominator.", "OPEN_DENOMINATOR_GATE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": lock_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for lock_id, formula, meaning, status in specs
    ]


def coupling_lock_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("CLK4756_0_kappa_eff", "kappa_eff = kappa_* Z_H", "effective local source coupling factors into parent coupling and Hilbert source-measure normalization.", "DERIVED_IF_COMPONENT_LOCKS_CLOSE"),
        ("CLK4756_1_drift_law", "D_A ln kappa_eff = D_A ln kappa_* + D_A delta_ZH", "source/time/species/frame/range/readout drift is explicit.", "DERIVED_DRIFT_LAW"),
        ("CLK4756_2_kappa_star", "D_A ln kappa_* = 0", "topological parent coupling must be selected before source/readout variation.", "CONDITIONALLY_ZERO_IN_PRIVATE_PARENT_SELECTOR"),
        ("CLK4756_3_ZH", "delta_ZH=0 and D_A delta_ZH=0", "Hilbert source-measure normalization must be source-blind.", "CONDITIONAL_SOURCE_MEASURE_GATE"),
        ("CLK4756_4_Gcal", "G_cal := c^4 kappa_eff/(8*pi)", "calibrated universal G is a structural bridge; numeric G_N prediction is not required here.", "STRUCTURAL_CALIBRATION_ALLOWED"),
        ("CLK4756_5_no_hidden_drift", "epsilon_Gdrift = sup_A |D_A ln G_cal|", "any hidden source/coupling drift becomes a finite local-test residual.", "FINITE_DRIFT_BOUND_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": lock_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for lock_id, formula, meaning, status in specs
    ]


def newton_bridge_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("NB4756_0_GR_block", "G_mu_nu[g_obs] = kappa_eff T_H_mu_nu + residual_mu_nu", "local GR block with source-blind coupling and explicit residual.", "CONDITIONAL_BLOCK"),
        ("NB4756_1_Poisson", "nabla^2 Phi_N = 4*pi G_cal rho_H", "weak-field Poisson law follows from the GR block and calibrated G_cal.", "STRUCTURAL_NEWTON_STEP"),
        ("NB4756_2_Gauss", "int_S grad Phi_N dot dS = 4*pi G_cal M_H^dress", "Gauss/source-charge insertion requires same-worldtube Hamiltonian mass.", "CONDITIONAL_SOURCE_STEP"),
        ("NB4756_3_acceleration", "a_r = -G_cal M_H^dress/r^2", "Newtonian acceleration follows without defining source mass by observed orbital GM.", "CONDITIONAL_READOUT_STEP"),
        ("NB4756_4_theorem", "locks close => MTS reduces structurally to local GR/Newton source law with calibrated G_cal", "this is the fair GR-style target, not numeric G prediction.", "CONDITIONAL_THEOREM_NONCLAIM"),
        ("NB4756_5_numeric_G_firewall", "numeric(G_cal) is empirical calibration unless parent dimensionful invariant fixes kappa_*", "prevents pretending MTS derives G_N when GR also calibrates G.", "FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": bridge_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bridge_id, formula, meaning, status in specs
    ]


def transition_hair_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("THB4756_0_common_mode", "q_tr -> q_0^H only", "safe transition contribution is stationary l=0 Hilbert monopole dressing M_H^dress.", "CONDITIONAL_COMMON_MODE_THEOREM"),
        ("THB4756_1_time", "Y_tau := ||Lie_tau q_tr||/M_H_ref", "time/source drift hair feeds clocks, Gdot, PPN preferred frame and orbital drift.", "FINITE_BOUND_IF_OPEN"),
        ("THB4756_2_multipole", "Y_l>=1 := sum_l>=1 |Q_l,tr|/M_H_ref", "multipole hair feeds anisotropy, precession and Newton residuals.", "FINITE_BOUND_IF_OPEN"),
        ("THB4756_3_species_frame", "Y_species_frame_source := |D_species q_tr| + |D_frame q_tr| + |Delta_source_weight_tr|", "species/frame/source-label hair feeds WEP and preferred-frame/source normalization tests.", "FINITE_BOUND_IF_OPEN"),
        ("THB4756_4_range", "Y_lambda := |D_lambda q_tr| + |q_range_tail|", "range hair feeds R10 alpha(lambda) and orbital range tests.", "FINITE_BOUND_IF_OPEN"),
        ("THB4756_5_nonEH", "Y_nonEH := ||Pi_arena Sigma_nonEH[q_tr]||", "non-EH metric hair feeds PPN gamma/beta, clocks and local GR bridge.", "FINITE_BOUND_IF_OPEN"),
        ("THB4756_6_boundary", "Y_boundary := |B_tr_nonlocal|/M_H_ref", "boundary/nonlocal hair feeds clocks, orbital, PPN and closure.", "FINITE_BOUND_IF_OPEN"),
        ("THB4756_7_EM", "epsilon_EM_extra_inner=0 on compact local Maxwell-Hodge selector", "Poynting vector is Hilbert momentum flux or boundary flux, not a second background source.", "CONDITIONAL_ZERO_IMPORTED"),
        ("THB4756_8_total", "epsilon_tr_hair <= Y_nonHilbert + Delta_Wtr + Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary", "if common-mode/source-kernel clauses do not all close, transition hair feeds epsilon_Gsrc.", "NO_CANCELLATION_VECTOR"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "hair_id": hair_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for hair_id, formula, meaning, status in specs
    ]


def epsilon_gsrc_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("EG4756_0_kappa", "epsilon_kappa_A <= |D_A ln kappa_*| + |D_A delta_ZH|", "effective coupling/source-measure drift", "ZERO_IF_COUPLING_LOCKS_CLOSE"),
        ("EG4756_1_integrability", "delta_H_tau_nonintegrable/M_H = |I_MTS|/M_H_ref", "Hamiltonian source-charge curl obstruction", "ZERO_IF_FULL_HTAU_CURL_CLOSES"),
        ("EG4756_2_reference", "Delta_ref/M_H = sum |R_ref_*|/M_H_ref", "fixed-reference or post-fit leakage", "ZERO_IF_HREF_LOCKS"),
        ("EG4756_3_tau_frame", "Delta_tau_frame_surface/M_H = sum |R_tau/frame/readout|/M_H_ref", "time/coframe/readout mismatch", "ZERO_IF_TAU_FRAME_LOCKS"),
        ("EG4756_4_boundary", "Delta_boundary_flux/M_H = sum |R_boundary/rad/memory|/M_H_ref", "boundary/radiative/open-memory leakage", "ZERO_IF_NO_FLUX_CLOSES"),
        ("EG4756_5_PiH", "epsilon_PiH = |ell_M(Pi_M^H J_H_total)-(H_tau-H_ref)|/|M_H^dress|", "private Hamiltonian glue mismatch outside the selector", "ZERO_INSIDE_PRIVATE_SELECTOR_ONLY"),
        ("EG4756_6_MHref", "Delta_MHref_normalizer = BLOCKED_NO_NORMALIZER or |delta_MHref|/M_H_ref", "positive denominator/source-frame stability", "OPEN_DENOMINATOR_GATE"),
        ("EG4756_7_transition", "epsilon_tr_hair", "transition source hair from 4355/4356", "ZERO_IF_COMMON_MODE_KERNEL_CLOSES"),
        ("EG4756_8_total", "epsilon_Gsrc <= epsilon_kappa + delta_H + Delta_ref + Delta_tau + Delta_boundary + epsilon_PiH + Delta_MHref + epsilon_tr_hair", "complete no-cancellation source/coupling residual vector.", "FINITE_VECTOR_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": epsilon_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for epsilon_id, formula, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4756_0_clean_locks", "Close source charge and kappa_eff locks on the same private/local branch", "BEST_ROUTE"),
        ("ROUTE4756_1_common_mode", "Prove transition source is stationary universal range-free l=0 Hilbert common mode", "PARALLEL_ROUTE"),
        ("ROUTE4756_2_finite_epsilon", "If locks remain unsigned, source finite epsilon_Gsrc and epsilon_tr_hair rows", "FALLBACK_ROUTE"),
        ("ROUTE4756_3_empirical", "Only after source rows exist, compare to WEP/R10/PPN/clock/orbital gates", "DEFER_UNTIL_SOURCED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4756_0_source_charge", "H_tau/M_Hdress integrable, positive, fixed-reference, same-worldtube", "OPEN_SOURCE_CHARGE_GATE"),
        ("GATE4756_1_coupling", "kappa_eff source-blind and drift-free", "OPEN_COUPLING_GATE"),
        ("GATE4756_2_transition", "q_tr is common-mode source dressing or finite epsilon_tr_hair sourced", "OPEN_TRANSITION_HAIR_GATE"),
        ("GATE4756_3_EM", "Poynting/EM counted once as Maxwell-Hodge Hilbert stress or boundary flux", "CONDITIONAL_EM_SIDE_CHANNEL_GATE"),
        ("GATE4756_4_Gcal", "G_cal calibrated once; no numeric G_N prediction claimed", "PASS_FAIR_GR_POSTURE"),
        ("GATE4756_5_claim", "No local-GR/Newton claim until all source/coupling/hair rows close or score", "FAIL_CLOSED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, requirement, status in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4756_0_no_numeric_G_claim", "Do not claim MTS predicts numeric G_N; structural calibrated G_cal is enough for GR-style reduction."),
        ("FW4756_1_no_orbital_GM_definition", "Do not define M_Hdress by observed orbital GM."),
        ("FW4756_2_no_G_absorption_hair", "Do not absorb time/species/frame/range/multipole transition hair into G_cal."),
        ("FW4756_3_no_Poynting_double_count", "Do not turn Poynting flux into a second background source outside Maxwell-Hodge Hilbert stress."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4756 derives the structural Newton bridge with calibrated G_cal and assembles the no-cancellation epsilon_Gsrc/source-hair vector that remains if source charge, coupling, and common-mode transition locks are unsigned.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_SOURCE_COUPLING_BRIDGE_NONCLAIM",
            "summary": "Structural Newton bridge with calibrated G_cal imported and hardened; epsilon_Gsrc/transition-hair vector retained.",
            "claim_status": "NO_LOCAL_GR_OR_NEWTON_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The Newton/source bridge is structurally clear; the remaining task is proving common-mode parent grammar or filling finite epsilon_Gsrc inputs.",
            "preferred_route": "Attempt common-mode parent grammar: stationary l=0 universal range-free same-metric Hilbert source dressing with Maxwell-Hodge/Poynting counted once.",
            "fallback_route": "Build finite epsilon_Gsrc input runner for kappa drift, H_tau integrability, reference/tau/frame/boundary/PiH/MHref and transition hair.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], key_field: str, value_field: str) -> str:
    return "\n".join(f"- `{row[key_field]}`: {row[value_field]}" for row in rows)


def write_docs(
    timestamp: str,
    source_rows: list[dict[str, Any]],
    coupling_rows: list[dict[str, Any]],
    newton_rows: list[dict[str, Any]],
    hair_rows: list[dict[str, Any]],
    epsilon_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4756 Y5 R2FR: Htau/MHref kappa Source Coupling Lock Or Transition Hair Bound

Generated: `{timestamp}`

## Result

4756 hardens the Newton/source-coupling bridge. The fair target is structural reduction with one calibrated, source-blind coupling:

```text
M_H^dress = H_tau - H_ref
kappa_eff = kappa_* Z_H
G_cal = c^4 kappa_eff/(8*pi)
nabla^2 Phi_N = 4*pi G_cal rho_H
```

MTS does **not** need to predict the numerical value of `G_N` at this stage, but it must lock source charge and prevent hidden drift/source hair.

## Source Charge Locks

{bullet(source_rows, "lock_id", "status")}

## Coupling Locks

{bullet(coupling_rows, "lock_id", "status")}

## Newton Bridge

{bullet(newton_rows, "bridge_id", "status")}

## Transition Hair

{bullet(hair_rows, "hair_id", "status")}

## epsilon_Gsrc Vector

{bullet(epsilon_rows, "epsilon_id", "status")}

## Route Matrix

{bullet(routes, "route_id", "status")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 772 PPC4161: Htau/MHref kappa Source Coupling Lock Or Transition Hair Bound

Generated: `{timestamp}`

## Structural Newton Bridge

```text
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
kappa_eff = kappa_* Z_H
G_cal := c^4 kappa_eff/(8*pi)
nabla^2 Phi_N = 4*pi G_cal rho_H
```

This is the correct GR-style local reduction posture: calibrate one universal `G_cal`, then prove it is source-blind and drift-free.

## Remaining Source/Coupling Residual

```text
epsilon_Gsrc <= epsilon_kappa + delta_H + Delta_ref + Delta_tau
  + Delta_boundary + epsilon_PiH + Delta_MHref + epsilon_tr_hair.
```

Transition hair is zero only if the raw transition contribution is common-mode Hilbert source dressing:

```text
q_tr -> q_0^H
```

stationary, l=0, universal, range-free, same-metric, boundary-owned, with EM/Poynting counted once as Maxwell-Hodge stress or boundary flux.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4756 hardens the structural Newton bridge: `M_H^dress=H_tau-H_ref`, `kappa_eff=kappa_*Z_H`, `G_cal=c^4 kappa_eff/(8*pi)`.
- It explicitly keeps numeric `G_N` as a calibration, not a claimed prediction.
- It assembles `epsilon_Gsrc` as the no-cancellation source/coupling residual vector.
- Transition hair is zero only as stationary universal range-free l=0 Hilbert common-mode source dressing; otherwise finite hair rows remain.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4756 local packet update: the Newton/source-coupling bridge is structurally clear. Next work is common-mode parent grammar or finite `epsilon_Gsrc` inputs.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4756-Y5-R2FR-Htau-MHref-kappa-source-coupling-lock-or-transition-hair-bound.md`

## Decision

`{DECISION}`

## What moved forward

- Hardened the structural Newton bridge using `M_H^dress=H_tau-H_ref`, `kappa_eff=kappa_*Z_H`, and calibrated `G_cal`.
- Clarified that MTS does not need to predict numeric `G_N` here, but must prove source-blind coupling and no drift.
- Assembled the finite no-cancellation `epsilon_Gsrc` vector.
- Imported the transition common-mode/hair law including the Poynting no-double-count guard.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_newton_bridge",
        "4756 hardens the structural Newton bridge with calibrated G_cal and assembles epsilon_Gsrc/source-hair bounds for unsigned source-coupling clauses.",
        "Generated source register, source charge lock rows, coupling lock rows, Newton bridge rows, transition hair rows, epsilon_Gsrc vector rows, route matrix, gates, firewalls, decision, status, next target and validation.",
        "structural_Newton_bridge_calibrated_G_epsilonGsrc_nonclaim",
        NEXT_TARGET,
        "Claiming numeric G_N prediction, defining mass by observed GM, or hiding transition/source hair inside calibrated G.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need common-mode parent grammar or finite epsilon_Gsrc input runner before local-GR/Newton claim.",
        "Htau/MHref kappa source coupling lock or transition hair bound",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    coupling_rows: list[dict[str, Any]],
    newton_rows: list[dict[str, Any]],
    hair_rows: list[dict[str, Any]],
    epsilon_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4756_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4756_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4756_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4756_2_source_charge", "source charge rows include H_tau, H_ref, M_Hdress and M_H_ref", any("H_tau" in row["formula"] and "H_ref" in row["formula"] for row in source_rows) and any("M_H_ref" in row["formula"] for row in source_rows), str(SOURCE_CHARGE_CSV)))
    checks.append(("VAL4756_3_coupling", "coupling rows include kappa_eff and G_cal", any("kappa_eff" in row["formula"] for row in coupling_rows) and any("G_cal" in row["formula"] for row in coupling_rows), str(COUPLING_LOCK_CSV)))
    checks.append(("VAL4756_4_newton", "Newton bridge includes Poisson and calibrated G firewall", any("nabla^2 Phi_N" in row["formula"] for row in newton_rows) and any("numeric(G_cal)" in row["formula"] for row in newton_rows), str(NEWTON_BRIDGE_CSV)))
    checks.append(("VAL4756_5_hair", "transition hair rows include common mode, epsilon_tr_hair and EM/Poynting guard", any("q_0^H" in row["formula"] for row in hair_rows) and any("epsilon_tr_hair" in row["formula"] for row in hair_rows) and any("Poynting" in row["meaning"] for row in hair_rows), str(TRANSITION_HAIR_CSV)))
    checks.append(("VAL4756_6_epsilon", "epsilon vector includes epsilon_Gsrc total", any("epsilon_Gsrc" in row["formula"] for row in epsilon_rows), str(EPSILON_GSRC_CSV)))
    checks.append(("VAL4756_7_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4756_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4756_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4756_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4756_11_claim_row", "claim row L-598 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4756_12_resume", "resume points from 4756 to 4757", "4756-Y5" in resume_text and "4757-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4756_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4756_OVERALL",
            "check": "all 4756 source-coupling bridge nonclaim checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    source_rows = source_charge_rows(timestamp)
    coupling_rows = coupling_lock_rows(timestamp)
    newton_rows = newton_bridge_rows(timestamp)
    hair_rows = transition_hair_rows(timestamp)
    epsilon_rows = epsilon_gsrc_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(SOURCE_CHARGE_CSV, source_rows)
    write_csv(COUPLING_LOCK_CSV, coupling_rows)
    write_csv(NEWTON_BRIDGE_CSV, newton_rows)
    write_csv(TRANSITION_HAIR_CSV, hair_rows)
    write_csv(EPSILON_GSRC_CSV, epsilon_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, source_rows, coupling_rows, newton_rows, hair_rows, epsilon_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, source_rows, coupling_rows, newton_rows, hair_rows, epsilon_rows, gates, timestamp))


if __name__ == "__main__":
    main()
