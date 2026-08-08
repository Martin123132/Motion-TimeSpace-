from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3828"
BRANCH = "MTS_R2FR_Y5_PPN_READOUT_TAIL_DESCENT_OR_FIRST_RESIDUAL_VECTOR_BOUND_3828"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3828-Y5-R2FR-PPN-readout-tail-descent-or-first-residual-vector-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3827 = PCW / "3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md"
CSV_3827_PPN = OUT / "P8_Y5_R2FR_3827_PPN_READOUT_TAIL_FIRST_ROWS.csv"
CSV_3827_SMOKE = OUT / "P8_Y5_R2FR_3827_SMOKE_RUN_RESULTS.csv"
CSV_3827_QUEUE = OUT / "P8_Y5_R2FR_3827_PRIORITY_SOURCE_FILL_QUEUE.csv"
CSV_3827_FAIL = OUT / "P8_Y5_R2FR_3827_FAILURE_MODE_LEDGER.csv"
CSV_3827_VALIDATION = OUT / "P8_Y5_BRR545_3827_VALIDATION.csv"
CSV_3826_SCORECARD = OUT / "P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv"
CSV_3826_RESIDUALS = OUT / "P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3828_SOURCE_REGISTER.csv",
    "ansatz": OUT / "P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv",
    "zero_theorem": OUT / "P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv",
    "residual_bound": OUT / "P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv",
    "readout_gates": OUT / "P8_Y5_R2FR_3828_LOCAL_GR_READOUT_CLAUSE_GATES.csv",
    "gates": OUT / "P8_Y5_R2FR_3828_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3828_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3828_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3828_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3828_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3828_0_3827_doc", P_3827, "Local Kernel Scorecard To First Smoke-Test Runner"),
    ("SRC3828_1_3827_ppn_rows", CSV_3827_PPN, "PPN3827_0_gamma_minus_one"),
    ("SRC3828_2_3827_smoke", CSV_3827_SMOKE, "SMOKE3827_PPN"),
    ("SRC3828_3_3827_queue", CSV_3827_QUEUE, "QUEUE3827_0_PPN_readout_tail"),
    ("SRC3828_4_3827_failure", CSV_3827_FAIL, "FAIL3827_2_PPN_readout_tail"),
    ("SRC3828_5_3827_validation", CSV_3827_VALIDATION, "VAL3827_6_priority_next"),
    ("SRC3828_6_3826_scorecard", CSV_3826_SCORECARD, "KSC3826_7_PPN_readout_tail"),
    ("SRC3828_7_3826_residuals", CSV_3826_RESIDUALS, "R3826_7_PPN_readout_tail"),
    ("SRC3828_8_3818_Poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
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
                "role": "input_for_PPN_readout_tail_derivation_or_bound",
                "claim_use": "derivation_contract_only_not_claim",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def ansatz_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "ansatz_id": "ANS3828_0_Newtonian_temporal",
            "sector": "Newtonian temporal metric",
            "readout_form": "g00_obs = -1 + 2 C_t Phi - 2 B_t Phi^2 + r00_2 + r00_4",
            "GR_value_after_Newton_calibration": "C_t=1; B_t=1",
            "meaning": "C_t fixes the Newtonian potential normalization and B_t fixes the second-order GR self-coupling",
            "source_status": "C_t anchored by 3818 Poisson bridge; B_t not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ansatz_id": "ANS3828_1_spatial_curvature",
            "sector": "spatial curvature readout",
            "readout_form": "gij_obs = delta_ij (1 + 2 C_s Phi) + rij_2",
            "GR_value_after_Newton_calibration": "C_s=C_t",
            "meaning": "C_s/C_t is the PPN gamma channel after the Newtonian force has fixed C_t",
            "source_status": "C_s=C_t not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ansatz_id": "ANS3828_2_vector_preferred_frame",
            "sector": "vector/preferred-frame readout",
            "readout_form": "g0i_obs = C_V1 V_i + C_V2 W_i + r0i",
            "GR_value_after_Newton_calibration": "no extra preferred-frame vector hair",
            "meaning": "nonzero arena-specific vector coefficients feed alpha1/alpha2 preferred-frame residuals",
            "source_status": "C_V1=C_V2=0 not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ansatz_id": "ANS3828_3_clock_readout",
            "sector": "clock/time transport",
            "readout_form": "d tau_obs/dt = 1 - C_tau Phi + r_tau",
            "GR_value_after_Newton_calibration": "C_tau=C_t",
            "meaning": "clock redshift must be the same source-kernel readout as g00, not a separate local-time ansatz",
            "source_status": "C_tau=C_t not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ansatz_id": "ANS3828_4_orbital_acceleration",
            "sector": "Newtonian/orbital acceleration",
            "readout_form": "a_obs = - C_acc grad Phi + r_acc",
            "GR_value_after_Newton_calibration": "C_acc=C_t with mu=GM used only as validation output",
            "meaning": "orbital dynamics may check the source kernel but cannot define the source normalization by fitted mu",
            "source_status": "C_acc=C_t requires independent source lock and GM anti-smuggling guard",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_condition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "condition_id": "ZPPN3828_0_same_source_potential",
            "zero_condition": "Phi is the same compact-exterior source potential in g00, gij, g0i, clock, and orbital readouts",
            "mathematical_role": "prevents arena-specific potentials from hiding fitted coefficients",
            "required_signature": "single source map q -> Phi with fixed Pi_M and R_eq/boundary clauses",
            "current_status": "PARTIAL_FROM_3818_3826",
            "if_unsigned": "retain R_source_ledger + R_PPN_readout_tail",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "ZPPN3828_1_gamma_lock",
            "zero_condition": "C_s = C_t",
            "mathematical_role": "sets gamma_MTS - 1 = 0 up to spatial residual rij_2/Phi",
            "required_signature": "parent readout naturality or diffeomorphic metric descent locks spatial and temporal scalar coefficients",
            "current_status": "UNSIGNED",
            "if_unsigned": "delta_gamma_bound = abs(C_s/C_t - 1) + eps_spatial/Phi",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "ZPPN3828_2_beta_lock",
            "zero_condition": "B_t = C_t^2",
            "mathematical_role": "sets beta_MTS - 1 = 0 after Newtonian calibration",
            "required_signature": "second-order source self-coupling descends from the same parent action as the first-order Poisson term",
            "current_status": "UNSIGNED",
            "if_unsigned": "delta_beta_bound = abs(B_t/C_t^2 - 1) + eps_temporal4/Phi^2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "ZPPN3828_3_no_preferred_frame_hair",
            "zero_condition": "C_V1 = C_V2 = 0 and r0i has no arena-fixed vector remainder",
            "mathematical_role": "blocks alpha1/alpha2 preferred-frame residuals",
            "required_signature": "local Lorentz/frame descent plus no representative-dependent vector coefficient",
            "current_status": "UNSIGNED",
            "if_unsigned": "alpha_pref_bound = abs(C_V1) + abs(C_V2) + eps_vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "ZPPN3828_4_clock_orbital_lock",
            "zero_condition": "C_tau = C_acc = C_t",
            "mathematical_role": "ties clock redshift and Newtonian acceleration to the same metric source readout",
            "required_signature": "clock transport and force law are projections of the same compact-exterior metric, not independent ansatz branches",
            "current_status": "UNSIGNED",
            "if_unsigned": "delta_clock_orbital_bound = abs(C_tau/C_t-1) + abs(C_acc/C_t-1) + eps_tau + eps_acc",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "ZPPN3828_5_no_GM_input_smuggling",
            "zero_condition": "fitted orbital mu=GM is never used to set C_t, C_acc, M_source, or G",
            "mathematical_role": "keeps Newtonian recovery from becoming circular",
            "required_signature": "independent source normalization or parent-derived coupling constant",
            "current_status": "GUARD_ACTIVE_NOT_CLOSED",
            "if_unsigned": "orbital rows stay validation-output only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_vector_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "RPPN3828_0_gamma",
            "observable": "gamma-1",
            "residual_formula": "delta_gamma = C_s/C_t - 1 + eps_spatial/Phi",
            "zero_if": "C_s=C_t and eps_spatial/Phi -> 0 on the local exterior domain",
            "bound_if_unsigned": "abs(delta_gamma) <= abs(C_s/C_t - 1) + abs(eps_spatial/Phi)",
            "source_status": "FIRST_BOUND_FORMULA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "RPPN3828_1_beta",
            "observable": "beta-1",
            "residual_formula": "delta_beta = B_t/C_t^2 - 1 + eps_temporal4/Phi^2",
            "zero_if": "B_t=C_t^2 and eps_temporal4/Phi^2 -> 0 on the local exterior domain",
            "bound_if_unsigned": "abs(delta_beta) <= abs(B_t/C_t^2 - 1) + abs(eps_temporal4/Phi^2)",
            "source_status": "FIRST_BOUND_FORMULA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "RPPN3828_2_preferred_frame",
            "observable": "alpha1, alpha2",
            "residual_formula": "delta_alpha_pref = C_V1 V_i + C_V2 W_i + eps_vector",
            "zero_if": "C_V1=C_V2=0 and eps_vector -> 0",
            "bound_if_unsigned": "alpha_pref_norm <= abs(C_V1) + abs(C_V2) + norm(eps_vector)",
            "source_status": "FIRST_BOUND_FORMULA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "RPPN3828_3_clock",
            "observable": "clock redshift/time transport",
            "residual_formula": "delta_tau = C_tau/C_t - 1 + eps_tau + R_boundary_MHref",
            "zero_if": "C_tau=C_t, eps_tau -> 0, and boundary/MHref row closes",
            "bound_if_unsigned": "abs(delta_tau) <= abs(C_tau/C_t - 1) + abs(eps_tau) + abs(R_boundary_MHref)",
            "source_status": "FIRST_BOUND_FORMULA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "RPPN3828_4_orbital",
            "observable": "Newtonian/orbital acceleration",
            "residual_formula": "delta_acc = C_acc/C_t - 1 + eps_acc + R_GM_guard",
            "zero_if": "C_acc=C_t, eps_acc -> 0, and independent source normalization replaces fitted mu input",
            "bound_if_unsigned": "abs(delta_acc) <= abs(C_acc/C_t - 1) + abs(eps_acc) + abs(R_GM_guard)",
            "source_status": "FIRST_BOUND_FORMULA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "RPPN3828_5_total",
            "observable": "R_PPN_readout_tail",
            "residual_formula": "R_PPN_readout_tail = {delta_gamma, delta_beta, delta_alpha_pref, delta_tau, delta_acc}",
            "zero_if": "ZPPN3828_0 through ZPPN3828_5 all close on the same compact exterior source kernel",
            "bound_if_unsigned": "norm(R_PPN_readout_tail) <= weighted norm of the five residual bounds above",
            "source_status": "INTEGRATED_FIRST_VECTOR_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def readout_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "RGATE3828_0_gamma",
            "gate": "gamma channel",
            "condition": "C_s=C_t",
            "status": "BLOCKED_PARENT_SIGNATURE_REQUIRED",
            "claim_allowed": False,
            "next_action": "derive scalar readout lock from parent metric descent",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "RGATE3828_1_beta",
            "gate": "beta channel",
            "condition": "B_t=C_t^2",
            "status": "BLOCKED_SECOND_ORDER_COUPLING_REQUIRED",
            "claim_allowed": False,
            "next_action": "derive nonlinear self-coupling owner from parent action",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "RGATE3828_2_preferred_frame",
            "gate": "preferred-frame channel",
            "condition": "C_V1=C_V2=0",
            "status": "BLOCKED_FRAME_DESCENT_REQUIRED",
            "claim_allowed": False,
            "next_action": "prove no vector hair or emit finite vector source rows",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "RGATE3828_3_clock_orbital",
            "gate": "clock/orbital readout lock",
            "condition": "C_tau=C_acc=C_t",
            "status": "BLOCKED_READOUT_LOCK_REQUIRED",
            "claim_allowed": False,
            "next_action": "tie clock/orbital projections to same metric source readout",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "RGATE3828_4_total",
            "gate": "local GR/Newton readout tail",
            "condition": "all scalar, vector, clock, orbital, and GM guard gates close",
            "status": "BLOCKED_BUT_NOW_FORMULATED",
            "claim_allowed": False,
            "next_action": "3829 should attack scalar readout locks first",
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3828_0_derivation_attempt",
            "gate": "PPN readout-tail derivation/bound emitted",
            "status": "PASS_NONCLAIM_BOUND_FORM",
            "claim_allowed": False,
            "reason": "zero conditions and finite residual vector formulas are explicit",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3828_1_local_GR_Newton_claim",
            "gate": "local GR/Newton recovery",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "C_s=C_t, B_t=C_t^2, vector hair zero, and clock/orbital locks are not parent-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3828_2_PPN_claim",
            "gate": "PPN gamma/beta/preferred-frame pass",
            "status": "BLOCKED_FIRST_VECTOR_BOUND_ONLY",
            "claim_allowed": False,
            "reason": "formulas exist but no numeric/source-backed coefficient bounds exist",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3828_3_no_GM_smuggling",
            "gate": "GM anti-circularity retained",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "orbital mu remains output validation only",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3828_4_next_target",
            "gate": "next target selects scalar readout lock derivation",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "gamma and beta scalar locks are the cleanest route under least scrutiny",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3828_0_partial_derivation_success",
            "decision": "R_PPN_readout_tail is no longer opaque",
            "basis": "3828 expresses it as gamma, beta, preferred-frame, clock, and orbital residual formulas",
            "consequence": "the project now has a concrete readout-tail target instead of a generic local-GR blocker",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3828_1_no_local_GR_claim",
            "decision": "do not claim local GR/Newton recovery",
            "basis": "the scalar and vector coefficient locks remain unsigned",
            "consequence": "3828 is a real forward step but still a nonclaim derivation contract",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3828_2_best_next_attack",
            "decision": "attack scalar readout locks before vector/EM extensions",
            "basis": "C_s=C_t and B_t=C_t^2 are the minimum path to gamma and beta; they are more central than Poynting/EM extension rows",
            "consequence": "3829 should try to derive the scalar locks from parent metric/action descent or emit coefficient-bound rows",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3828_0",
            "next_checkpoint": "3829-Y5-R2FR-scalar-readout-lock-Ct-Cs-Bt-owner-or-bound-fill.md",
            "script": "scripts/Y5_R2FR_3829_scalar_readout_lock_Ct_Cs_Bt_owner_or_bound_fill.py",
            "objective": "try to derive the scalar readout locks C_s=C_t and B_t=C_t^2 from parent metric/action descent, or emit first coefficient-bound rows for gamma and beta",
            "reason": "3828 shows these two locks are the least-optional bridge between MTS source coupling and local PPN/GR recovery",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_PPN_READOUT_TAIL_BOUND_FORM",
            "claim": "no PPN/local-GR/Newton claim",
            "summary": "3828 derives the first symbolic residual-vector bound for R_PPN_readout_tail and selects scalar readout locks as the next proof target.",
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
    ansatz: list[dict[str, object]],
    zero_conditions: list[dict[str, object]],
    residuals: list[dict[str, object]],
    readout_gates: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3828 — PPN Readout Tail Descent Or First Residual-Vector Bound

Private checkpoint. This attempts the derivation route first. It does not claim local GR/Newton recovery.

Generated: `{timestamp}`

## Result

3828 converts the opaque blocker `R_PPN_readout_tail` into a residual vector:

`R_PPN_readout_tail = {{delta_gamma, delta_beta, delta_alpha_pref, delta_tau, delta_acc}}`.

Using `Phi=U/c^2` and a Newtonian temporal calibration, the minimal readout ansatz is:

`g00_obs = -1 + 2 C_t Phi - 2 B_t Phi^2 + r00_2 + r00_4`

`gij_obs = delta_ij (1 + 2 C_s Phi) + rij_2`

`g0i_obs = C_V1 V_i + C_V2 W_i + r0i`.

GR/PPN recovery then requires the scalar locks `C_s=C_t` and `B_t=C_t^2`, no preferred-frame vector hair, and clock/orbital projections tied to the same source readout.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Readout Ansatz

{markdown_table(ansatz, ["ansatz_id", "sector", "readout_form", "GR_value_after_Newton_calibration", "source_status"])}

## Zero Conditions

{markdown_table(zero_conditions, ["condition_id", "zero_condition", "mathematical_role", "current_status", "if_unsigned"])}

## Residual Vector Bound

{markdown_table(residuals, ["residual_id", "observable", "residual_formula", "zero_if", "bound_if_unsigned"])}

## Readout Gates

{markdown_table(readout_gates, ["gate_id", "gate", "condition", "status", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is closer to derivation than the previous blocker state. We still cannot claim local GR, but we now know exactly what must be proved:

- `C_s=C_t` gives `gamma -> 1`;
- `B_t=C_t^2` gives `beta -> 1`;
- `C_V1=C_V2=0` kills preferred-frame tails;
- `C_tau=C_acc=C_t` ties clocks and Newtonian acceleration to the same metric readout;
- fitted orbital `mu=GM` remains a validation output, not the source normalization.

Next target: `3829-Y5-R2FR-scalar-readout-lock-Ct-Cs-Bt-owner-or-bound-fill.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3827", "Current State After 3828", 1)
    paragraph = (
        "`3828` turns the opaque `R_PPN_readout_tail` blocker into a concrete residual vector "
        "`{delta_gamma, delta_beta, delta_alpha_pref, delta_tau, delta_acc}`. Under the minimal PPN readout ansatz "
        "`g00=-1+2 C_t Phi-2 B_t Phi^2+...`, `gij=delta_ij(1+2 C_s Phi)+...`, and `g0i=C_V1 V_i+C_V2 W_i+...`, "
        "local GR requires `C_s=C_t`, `B_t=C_t^2`, no preferred-frame vector hair, and clock/orbital locks to the same `C_t`. "
        "These are not yet parent-signed, so 3828 is a nonclaim derivation contract, but the local-GR target is now mathematically sharp.\n\n"
    )
    anchor = "`3827` runs"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3828-Y5-R2FR-PPN-readout-tail-descent-or-first-residual-vector-bound.md`

Target: derive or cleanly bound `R_PPN_readout_tail` for `gamma-1`, `beta-1`, preferred-frame, clock, and orbital residuals using the same compact exterior source kernel, without arena-tuned readout coefficients.

This is the best next move because 3827 shows the dry-run machinery is working and the readout tail is the critical proof edge between the compact source kernel and local Newton/GR recovery."""
    new_gate = """`3829-Y5-R2FR-scalar-readout-lock-Ct-Cs-Bt-owner-or-bound-fill.md`

Target: try to derive the scalar readout locks `C_s=C_t` and `B_t=C_t^2` from parent metric/action descent, or emit first coefficient-bound rows for `gamma` and `beta`.

This is the best next move because 3828 shows these two scalar locks are the least-optional bridge between MTS source coupling and local PPN/GR recovery."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3828_LOCAL_GR_READOUT_CLAUSE_GATES.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3828_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3828 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3828 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    ansatz: list[dict[str, object]],
    zero_conditions: list[dict[str, object]],
    residuals: list[dict[str, object]],
    readout_gates: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in ansatz + zero_conditions + residuals + readout_gates)
    add(
        "VAL3828_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3828_1_ansatz_channels",
        "ansatz covers temporal, spatial, vector, clock, and orbital channels",
        all(token in all_text for token in ["C_t", "C_s", "C_V1", "C_tau", "C_acc"]),
        "required coefficient symbols present",
    )
    add(
        "VAL3828_2_zero_conditions",
        "zero theorem includes scalar locks, vector silence, clock/orbital lock, and GM guard",
        all(token in all_text for token in ["C_s = C_t", "B_t = C_t^2", "C_V1 = C_V2 = 0", "C_tau = C_acc = C_t", "mu=GM"]),
        "zero-condition tokens present",
    )
    add(
        "VAL3828_3_residual_vector",
        "residual vector covers gamma, beta, preferred-frame, clock, orbital, and total rows",
        len(residuals) == 6 and any(row["residual_id"] == "RPPN3828_5_total" for row in residuals),
        f"{len(residuals)} residual rows",
    )
    add(
        "VAL3828_4_no_claims",
        "all ansatz, zero, residual, readout gate, and claim gate rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in ansatz + zero_conditions + residuals + readout_gates + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3828_5_local_GR_blocked",
        "local GR/Newton gate remains blocked",
        any(row["gate_id"] == "GATE3828_1_local_GR_Newton_claim" and row["status"] == "BLOCKED" for row in gates),
        "local-GR claim blocked",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3828_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3828_7_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "C_s=C_t" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3828*", "P8_Y5_BRR545_3828*", "*Y5_R2FR_3828*", "3828-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3828_8_formalization_clean",
        "formalization-workbench has no 3828 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3828 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3828_9_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    ansatz = ansatz_rows(timestamp)
    zero_conditions = zero_condition_rows(timestamp)
    residuals = residual_vector_rows(timestamp)
    readout_gates = readout_gate_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["ansatz"], ansatz)
    write_csv(OUTPUTS["zero_theorem"], zero_conditions)
    write_csv(OUTPUTS["residual_bound"], residuals)
    write_csv(OUTPUTS["readout_gates"], readout_gates)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, ansatz, zero_conditions, residuals, readout_gates, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, ansatz, zero_conditions, residuals, readout_gates, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_PPN_READOUT_TAIL_BOUND_FORM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
