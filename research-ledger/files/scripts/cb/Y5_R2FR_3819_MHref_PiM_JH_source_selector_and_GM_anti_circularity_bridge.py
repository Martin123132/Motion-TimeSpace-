from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3819"
BRANCH = "MTS_R2FR_Y5_MHREF_PIM_JH_SOURCE_SELECTOR_AND_GM_ANTI_CIRCULARITY_BRIDGE_3819"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3818 = PCW / "3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md"
P_1006 = PCW / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"
P_1013 = PCW / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
P_1016 = PCW / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
P_3772 = PCW / "3772-Y5-R2FR-source-Hamiltonian-normalization-or-Newton-active-passive-GM-bound.md"

CSV_3817_THEOREM = OUT / "P8_Y5_R2FR_3817_HILBERT_STRESS_PRESERVATION_THEOREM.csv"
CSV_3818_GUARDS = OUT / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv"
CSV_3818_RESID = OUT / "P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv"
CSV_1006_CLAIM = OUT / "P8_Y5_R10_1006_CLAIM_GATE.csv"
CSV_1006_SCHEMA = OUT / "P8_Y5_R10_1006_DENOMINATOR_SOURCE_SCHEMA.csv"
CSV_1013_FLUX = OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv"
CSV_1013_OBS = OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv"
CSV_1016_CONTRACT = OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"
CSV_3772_THEOREM = OUT / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv"
CSV_3772_ATTEMPT = OUT / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_ZERO_ATTEMPT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3819_SOURCE_REGISTER.csv",
    "selector": OUT / "P8_Y5_R2FR_3819_SOURCE_SELECTOR_THEOREM.csv",
    "active_mass": OUT / "P8_Y5_R2FR_3819_ACTIVE_MASS_LAW.csv",
    "pim": OUT / "P8_Y5_R2FR_3819_PIM_JH_CLOSURE_AUDIT.csv",
    "gm": OUT / "P8_Y5_R2FR_3819_GM_ANTI_CIRCULARITY_CONTRACT.csv",
    "residuals": OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv",
    "gates": OUT / "P8_Y5_R2FR_3819_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3819_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3819_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3819_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3819_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3819_0_3818_doc", P_3818, "Source Normalization Gate"),
    ("SRC3819_1_3818_guards", CSV_3818_GUARDS, "SNG3818_1_PiM_JH"),
    ("SRC3819_2_3818_residuals", CSV_3818_RESID, "R3818_2_GM_calibration"),
    ("SRC3819_3_1006_doc", P_1006, "positive same-frame M_H_ref theorem attempted"),
    ("SRC3819_4_1006_claim", CSV_1006_CLAIM, "CG1006_1_orbital_GM_substitution"),
    ("SRC3819_5_1006_schema", CSV_1006_SCHEMA, "MHS1006_2_anti_circularity"),
    ("SRC3819_6_1013_doc", P_1013, "compact-exterior closure"),
    ("SRC3819_7_1013_flux", CSV_1013_FLUX, "PFC1013_8_verdict"),
    ("SRC3819_8_1013_obstruction", CSV_1013_OBS, "OBS1013_7_calibration_PPN_tail"),
    ("SRC3819_9_1016_doc", P_1016, "source worldtube"),
    ("SRC3819_10_1016_contract", CSV_1016_CONTRACT, "PSC1016_5_dressed_source_charge"),
    ("SRC3819_11_3772_doc", P_3772, "GM degeneracy"),
    ("SRC3819_12_3772_theorem", CSV_3772_THEOREM, "NSH3772_5_GM_degeneracy_guard"),
    ("SRC3819_13_3772_attempt", CSV_3772_ATTEMPT, "NZA3772_6_Hamiltonian_charge_equals_Hilbert_mass"),
    ("SRC3819_14_3817_hilbert", CSV_3817_THEOREM, "HSP3817_1_Hilbert_stress_preserved"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def base_row(timestamp: str) -> dict[str, str]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows(timestamp: str) -> list[dict[str, str]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base_row(timestamp),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "exists": str(exists),
                "needle_found": str(needle in text),
                "source_role": "source-normalization bridge input",
            }
        )
    return rows


def selector_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "selector_id": "SST3819_0_fixed_arena_first",
            "status": "EXACT_CONDITIONAL_SELECTOR_ORDER",
            "statement": "Choose the observed metric/coframe, time generator tau, reference H_ref, source worldtube W_src, and linking surfaces before fitting any orbital mu=GM.",
            "derived_form": "arena=(g_obs,e_obs,tau,H_ref,W_src,[S_link]) fixed first",
            "failure_if_unsigned": "source normalization can be absorbed into a readout fit",
        },
        {
            "selector_id": "SST3819_1_worldtube_from_current_support",
            "status": "EXACT_CONDITIONAL_WORLDTUBE_DEFINITION",
            "statement": "The source region is selected by the support of the same-frame Hilbert/Hamiltonian source current, not by a fitted gravitational radius.",
            "derived_form": "W_src=closure(supp J_H[tau,e_obs]) with homology class [S_link] around W_src",
            "failure_if_unsigned": "mass support and orbital readout can chase each other",
        },
        {
            "selector_id": "SST3819_2_dressed_Hamiltonian_source_mass",
            "status": "EXACT_CONDITIONAL_CHARGE_DEFINITION",
            "statement": "The mass entering Poisson is the dressed Hamiltonian charge of W_src in the fixed arena, including matter, binding, improvement and boundary/reference terms.",
            "derived_form": "M_H_ref(W)=c^-2*(H_tau[W,S_link]-H_ref)",
            "failure_if_unsigned": "bare rest mass, boundary energy, and readout mass are silently mixed",
        },
        {
            "selector_id": "SST3819_3_positive_mass_condition",
            "status": "DERIVED_CONDITIONAL_POSITIVITY_LAW",
            "statement": "M_H_ref is nonnegative if the tau-Hamiltonian density obeys the branch energy condition, H_ref is the fixed vacuum/reference minimum, and boundary/improvement terms do not over-subtract.",
            "derived_form": "M_H_ref>=0, strict if W_src carries nonzero positive Hamiltonian charge",
            "failure_if_unsigned": "negative denominators or sign flips remain possible",
        },
        {
            "selector_id": "SST3819_4_orbital_GM_forbidden_as_input",
            "status": "EXACT_ANTI_CIRCULARITY_RULE",
            "statement": "An orbital mu_fit can test the product G_ref*M_H_ref, but cannot define M_H_ref for that same test.",
            "derived_form": "M_H_ref != mu_fit/G_ref for any claim using mu_fit as evidence",
            "failure_if_unsigned": "Newton recovery becomes tautological",
        },
        {
            "selector_id": "SST3819_5_selector_verdict",
            "status": "PARTIAL_ADVANCE_NOT_CLOSED",
            "statement": "The selector law is now explicit enough to prevent GM laundering, but parent-signed tau/H_ref/Pi_M/source-current ownership is still required.",
            "derived_form": "selector usable as contract; not a Newton/local-GR claim",
            "failure_if_unsigned": "retain finite source-normalization residuals",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def active_mass_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "law_id": "AML3819_0_Komar_Tolman_stationary_selector",
            "status": "EXACT_CONDITIONAL_STATIONARY_ACTIVE_MASS_FORM",
            "formula": "M_tau=(2/c^2)*int_Sigma (T_mn-0.5*T*g_mn)n^m tau^n dSigma + M_boundary_reference",
            "meaning": "For a stationary branch this is the active source charge associated with tau, not an arbitrary fitted mass.",
            "scope": "requires stationary/asymptotic or finite-domain tau, boundary reference, and same-frame total Hilbert stress",
        },
        {
            "law_id": "AML3819_1_slow_weak_limit",
            "status": "EXACT_CONDITIONAL_LIMIT",
            "formula": "M_tau=int rho_rest d^3x + O(v^2/c^2,p/c^2,binding/c^2,boundary/c^2,nonEH)",
            "meaning": "The Newtonian mass follows as the slow weak limit only after pressure, kinetic, binding, boundary and non-EH terms are retained or bounded.",
            "scope": "ordinary cold sources may make corrections tiny; compact/relativistic sources cannot drop them",
        },
        {
            "law_id": "AML3819_2_Poisson_density_refinement",
            "status": "SOURCE_DENSITY_REFINEMENT",
            "formula": "rho_H in nabla^2 Phi=4*pi*G_ref*rho_H must mean the selected active Hamiltonian/Tolman density, not whichever density best fits mu",
            "meaning": "3818's Poisson algebra is preserved, but the source symbol is now sharpened.",
            "scope": "if rho_H is taken as T_00/c^2, pressure/binding residual R_pressure_binding must be retained",
        },
        {
            "law_id": "AML3819_3_passive_inertial_link",
            "status": "CARRIED_EXACT_CONDITIONAL_FROM_3772",
            "formula": "same descended matter action => m_passive/m_inertial=1 + retained residuals",
            "meaning": "This keeps Newton's inertial/passive side connected to the same source branch.",
            "scope": "still depends on source action descent and theta/coupling silence",
        },
        {
            "law_id": "AML3819_4_active_mass_verdict",
            "status": "DERIVED_CONDITIONAL_NOT_NUMERICALLY_CLOSED",
            "formula": "M_active=M_H_ref if stationary active charge, boundary reference, and slow-limit residuals are signed",
            "meaning": "The active-mass route is viable and sharper than a placeholder, but not yet claim-grade.",
            "scope": "feeds 3820 Komar/Tolman and independent-source ledger",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def pim_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "audit_id": "PIM3819_0_exact_product_identity",
            "status": "EXACT_OBSTRUCTION_IDENTITY",
            "condition": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "result": "Flux closure is not a vibe-check: it fails only through current nonconservation, projector commutator, boundary flux, anomaly, or readout-dependence terms.",
            "residual_symbol": "R_PiM_commutator",
        },
        {
            "audit_id": "PIM3819_1_current_conservation_feed",
            "status": "CONDITIONAL_FROM_3817",
            "condition": "nabla_mu T_total^mu_nu=0 and same tau/coframe source current",
            "result": "Pi_M dJ_H can vanish if the 3817 Ward/Bianchi total-current contract is parent-signed.",
            "residual_symbol": "C_Bianchi_total",
        },
        {
            "audit_id": "PIM3819_2_projector_fixedness",
            "status": "OPEN_REQUIRED_ZERO",
            "condition": "[d,Pi_M]J_H=0",
            "result": "This is the main unsolved technical zero: Pi_M must be a fixed parent charge map, not a radius/readout-dependent mask.",
            "residual_symbol": "R_PiM_commutator",
        },
        {
            "audit_id": "PIM3819_3_compact_exterior_flux",
            "status": "OPEN_REQUIRED_ZERO_OR_BOUND",
            "condition": "int_annulus d(Pi_M J_H)=0 or finite epsilon_radial_Meff",
            "result": "Radiation, non-EH, boundary and frame tails must be absent or bounded before inverse-square mass closure is claimed.",
            "residual_symbol": "R_flux_leak",
        },
        {
            "audit_id": "PIM3819_4_closure_verdict",
            "status": "NOT_CLOSED_BUT_NOW_EXACTLY_LOCALIZED",
            "condition": "PIM3819_1 through PIM3819_3 all signed",
            "result": "Pi_M closure remains blocked; the next proof should target projector fixedness plus active-mass source density, not re-list generic missing data.",
            "residual_symbol": "R_PiM_JH_flux",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def gm_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "contract_id": "GM3819_0_observable_split",
            "status": "EXACT_DEGENERACY_LAW",
            "rule": "mu_fit=G_ref*M_H_ref*(1+delta_readout+delta_boundary+delta_range+delta_nonEH+delta_orbit)",
            "acceptance": "a test must split the product or state that only mu is tested",
            "blocked_action": "do not infer M_H_ref=mu_fit/G_ref and then claim Newton source recovery",
        },
        {
            "contract_id": "GM3819_1_independent_mass_inputs",
            "status": "SOURCE_LEDGER_REQUIRED",
            "rule": "claim-grade M_H_ref needs non-orbital source evidence: lab mass/calorimetry/composition/density-volume or a parent Hamiltonian charge calculation",
            "acceptance": "source path, units, uncertainty, frame, tau/reference and no orbital-mu reuse",
            "blocked_action": "do not use ephemeris GM as the mass denominator for the same arena",
        },
        {
            "contract_id": "GM3819_2_allowed_orbital_use",
            "status": "SAFE_USE_RULE",
            "rule": "orbital data may constrain residuals in mu_fit, range dependence, PPN/readout tails, or ratios once source normalization is separately fixed",
            "acceptance": "the row labels orbital evidence as product evidence, not source-mass evidence",
            "blocked_action": "do not mark local GR/Newton passed from orbital agreement alone",
        },
        {
            "contract_id": "GM3819_3_dimensionless_cross_arena_use",
            "status": "PREFERRED_NEXT_TEST_ROUTE",
            "rule": "use WEP, R10, clock, PPN and orbital ratios as cross-arena constraints on the same source-normalization vector",
            "acceptance": "one shared residual vector; no per-arena refitting",
            "blocked_action": "do not tune G_eff or source mass separately in each arena",
        },
        {
            "contract_id": "GM3819_4_verdict",
            "status": "PASS_GUARD_NOT_PHYSICS_CLAIM",
            "rule": "GM circularity is now guarded explicitly; the physics claim remains blocked until M_H_ref/Pi_M are independently owned",
            "acceptance": "3820 builds the active-mass/source-ledger route",
            "blocked_action": "do not publish Newton/local-GR pass from this checkpoint",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def residual_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        ("R3819_0_selector_owner", "R_selector_owner", "fixed arena/tau/worldtube/source selector residual", "norm(delta selector) or Boolean closure failure", "dimensionless_or_structural", "TAU_HREF_WORLDTUBE_NOT_PARENT_SIGNED"),
        ("R3819_1_active_mass_density", "R_active_density", "difference between selected active Hamiltonian/Tolman density and simplified T_00/c^2 density", "||rho_H-rho_active||/rho_ref", "dimensionless", "PRESSURE_BINDING_BOUNDARY_TERMS_NOT_BOUNDED"),
        ("R3819_2_PiM_commutator", "R_PiM_commutator", "projector commutator obstruction to d(Pi_M J_H)=0", "||[d,Pi_M]J_H|| in source annulus", "current_flux_units_or_dimensionless_after_norm", "PIM_FIXEDNESS_NOT_PROVED"),
        ("R3819_3_worldtube_boundary", "R_worldtube_boundary", "boundary/reference/improvement flux across linking surfaces", "|int_S delta B_tau|/M_ref", "dimensionless", "BOUNDARY_REFERENCE_LOCK_OPEN"),
        ("R3819_4_GM_anti_circularity", "R_GM_anti_circularity", "unresolved split between G_ref, source mass, and observed mu", "|delta ln mu-delta ln G_ref-delta ln M_H_ref|", "dimensionless", "INDEPENDENT_SOURCE_LEDGER_MISSING"),
        ("R3819_5_pressure_binding", "R_pressure_binding", "pressure, kinetic, internal and binding corrections to Newtonian density", "O(v^2/c^2,p/c^2,binding/c^2)", "dimensionless", "ACTIVE_MASS_LIMIT_NOT_NUMERICALLY_BOUNDED"),
        ("R3819_6_total", "R_source_normalization_total", "total source-normalization obstruction for Newton/local GR", "R_selector_owner+R_active_density+R_PiM_commutator+R_worldtube_boundary+R_GM_anti_circularity+R_pressure_binding", "dimensionless_after_norm", "LOCAL_GR_NEWTON_SOURCE_NORMALIZATION_BLOCKED"),
    ]
    return [
        {
            **base_row(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": bound_formula,
            "units": units,
            "current_status": status,
            "exit_requirement": "theorem-zero in one branch or source-backed numeric/component bound",
        }
        for residual_id, symbol, definition, bound_formula, units, status in rows
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in grouped["sources"])
    rows = [
        ("GATE3819_0_sources", "PASS_NONCLAIM" if sources_pass else "FAIL", "all source paths and needles present" if sources_pass else "missing source path or needle"),
        ("GATE3819_1_selector_contract", "PASS_NONCLAIM", "source selector theorem emitted, but parent signatures remain open"),
        ("GATE3819_2_active_mass_law", "PASS_NONCLAIM", "Komar/Tolman active-mass route derived conditionally; pressure/binding/boundary terms retained"),
        ("GATE3819_3_PiM_flux_closure", "BLOCKED", "Pi_M commutator/fixedness and compact exterior flux not proved"),
        ("GATE3819_4_GM_anti_circularity", "PASS_GUARD", "orbital GM laundering forbidden explicitly"),
        ("GATE3819_5_Newton_claim", "BLOCKED", "Newton claim waits on M_H_ref/Pi_M/source-ledger closure"),
        ("GATE3819_6_local_GR_claim", "BLOCKED", "local GR claim waits on source normalization plus PPN/readout residuals"),
    ]
    return [
        {
            **base_row(timestamp),
            "gate_id": gate_id,
            "gate_status": status,
            "claim_allowed": "false",
            "detail": detail,
        }
        for gate_id, status, detail in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC3819_0_not_a_dead_end",
            "decision": "Keep the local GR/Newton branch alive.",
            "rationale": "The EH-to-Poisson algebra is clean and the source-selector route now has exact conditional forms; the remaining gap is ownership/calibration, not a contradiction.",
            "next_action": "derive/bound stationary active mass and build independent source ledger",
        },
        {
            "decision_id": "DEC3819_1_do_not_use_orbital_GM_as_mass",
            "decision": "Orbital GM is product evidence only.",
            "rationale": "Using mu_fit/G_ref as M_H_ref would make Newton recovery circular.",
            "next_action": "tag every source row by independent_source, product_only, or residual_constraint",
        },
        {
            "decision_id": "DEC3819_2_next_target",
            "decision": "Move to Komar/Tolman active mass and independent source ledger.",
            "rationale": "This attacks the actual missing bridge instead of circling generic missing rows.",
            "next_action": "3820",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def next_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "target_doc": "3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md",
            "target_script": "scripts/Y5_R2FR_3820_Komar_Tolman_active_mass_and_independent_source_ledger.py",
            "objective": "Derive or bound the stationary Komar/Tolman active-mass route, pressure/binding corrections, and an independent source-mass ledger that avoids orbital-GM circularity.",
            "success_gate": "Either M_H_ref becomes a parent-owned active charge with bounded slow-limit corrections and independent source inputs, or the remaining source-normalization residual vector is finite and ready for empirical scoring.",
            "avoid": "do not claim Newton/local GR; do not use orbital GM as source mass; do not drop pressure/binding/boundary terms; do not edit formalization-workbench; do not use GitHub",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "status": "PASS_NONCLAIM_SOURCE_SELECTOR_ACTIVE_MASS_AND_GM_GUARD_BUILT",
            "summary": "3819 derives the conditional source-selector/active-mass bridge, blocks orbital GM laundering, and selects 3820 Komar/Tolman plus independent source ledger.",
        }
    ]


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_markdown(grouped: dict[str, list[dict[str, str]]]) -> None:
    text = f"""# 3819 - MHref, PiM JH Source Selector, And GM Anti-Circularity Bridge

## Status

`PASS_NONCLAIM_SOURCE_SELECTOR_ACTIVE_MASS_AND_GM_GUARD_BUILT`

This checkpoint does not claim Newton, local GR, PPN, R10, clock, orbital, or source-normalization closure. It does something narrower and useful: it turns the source-mass problem into an exact contract rather than a vague missing-data complaint.

## Source Selector Theorem

{md_table(grouped["selector"], ["selector_id", "status", "statement", "derived_form", "failure_if_unsigned"])}

## Active Mass Law

{md_table(grouped["active_mass"], ["law_id", "status", "formula", "meaning", "scope"])}

## PiM JH Closure Audit

{md_table(grouped["pim"], ["audit_id", "status", "condition", "result", "residual_symbol"])}

## GM Anti-Circularity Contract

{md_table(grouped["gm"], ["contract_id", "status", "rule", "acceptance", "blocked_action"])}

## Finite Fallbacks

{md_table(grouped["residuals"], ["residual_id", "symbol", "definition", "bound_formula", "current_status"])}

## Claim Gates

{md_table(grouped["gates"], ["gate_id", "gate_status", "claim_allowed", "detail"])}

## Next Target

`3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md`

Target: derive or bound the stationary Komar/Tolman active-mass route, pressure/binding corrections, and an independent source ledger so `M_H_ref` is not secretly `mu_fit/G_ref`.

## Machine Outputs

{md_table(grouped["status"], ["status", "summary"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3818",
        "# Local GR Coupling Spine - Current State After 3819",
    )
    paragraph = (
        "`3819` derives the next source-normalization bridge: choose the observed arena, `tau`, `H_ref`, `W_src`, and linking surfaces before orbital fitting; define "
        "`M_H_ref=c^-2*(H_tau[W,S_link]-H_ref)` as a dressed Hamiltonian/active mass charge; refine the Poisson source toward the Komar/Tolman active density; and forbid "
        "the circular move `M_H_ref=mu_fit/G_ref` for the same orbital test. The branch is alive, not claimed: `Pi_M` fixedness, pressure/binding/boundary terms, and independent source inputs remain the live gap.\n\n"
    )
    if "`3819` derives the next source-normalization bridge" not in text:
        marker = "`3818` derives the exact conditional EH-to-Poisson coefficient bridge:"
        index = text.find(marker)
        if index != -1:
            line_end = text.find("\n\n", index)
            if line_end != -1:
                text = text[: line_end + 2] + paragraph + text[line_end + 2 :]
    old_target = """`3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md`

Target: derive or bound the source-normalization gate exposed by 3818: positive same-frame `M_H_ref`, parent-owned `Pi_M J_H` flux closure, source worldtube selector, and measured-GM anti-circularity. If not closed, emit finite `M_H_ref`/`PiM`/`GM` residual rows ready for empirical scoring.

This is the best next move because the EH-to-Poisson algebra is now clean conditionally; the remaining danger is laundering source normalization through fitted orbital `GM`.
"""
    new_target = """`3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md`

Target: derive or bound the stationary Komar/Tolman active-mass route, pressure/binding corrections, and an independent source-mass ledger that avoids orbital-GM circularity. If not closed, keep `R_active_density`, `R_pressure_binding`, and `R_GM_anti_circularity` finite and source-ready.

This is the best next move because 3819 no longer lets the project hide behind generic missing source rows: the remaining question is whether `M_H_ref` can be owned as an active Hamiltonian charge with independently sourced mass inputs.
"""
    text = text.replace(old_target, new_target)
    artifacts = [
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3819_SOURCE_SELECTOR_THEOREM.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3819_ACTIVE_MASS_LAW.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3819_PIM_JH_CLOSURE_AUDIT.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3819_GM_ANTI_CIRCULARITY_CONTRACT.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv",
        "source-intake\\mts_residuals\\P8_Y5_BRR545_3819_VALIDATION.csv",
    ]
    insertion = "".join(f"- `{artifact}`\n" for artifact in artifacts)
    if artifacts[0] not in text:
        text = text.replace("## Machine Artifacts\n\n", "## Machine Artifacts\n\n" + insertion)
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    cache = PCW / "scripts" / "__pycache__"
    if cache.exists() and cache.is_dir():
        shutil.rmtree(cache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if result else "FAIL",
                "detail": detail,
            }
        )

    add("sources_exist", all(row["exists"] == "True" for row in grouped["sources"]), "every cited source path exists")
    add("needles_found", all(row["needle_found"] == "True" for row in grouped["sources"]), "every cited source needle was found")
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            csv_ok = csv_ok and path.exists() and len(parse_csv(path)) > 0
        except Exception:
            csv_ok = False
    add("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse")
    add("doc_written", DOC_PATH.exists() and "GM Anti-Circularity Contract" in read_text(DOC_PATH), "3819 markdown document written")
    add("selector_theorem_written", any(row["selector_id"] == "SST3819_2_dressed_Hamiltonian_source_mass" for row in grouped["selector"]), "dressed source selector emitted")
    add("active_mass_law_written", any(row["law_id"] == "AML3819_0_Komar_Tolman_stationary_selector" for row in grouped["active_mass"]), "Komar/Tolman active mass law emitted")
    add("pim_obstruction_exact", any(row["audit_id"] == "PIM3819_0_exact_product_identity" for row in grouped["pim"]), "PiM product obstruction identity emitted")
    add("gm_guard_written", any(row["contract_id"] == "GM3819_0_observable_split" for row in grouped["gm"]), "GM anti-circularity guard emitted")
    add("residual_total_row", any(row["symbol"] == "R_source_normalization_total" for row in grouped["residuals"]), "total source normalization residual emitted")
    add("claim_gates_closed", all(row.get("claim_allowed") == "false" for row in grouped["gates"]), "no claim gate allows a claim")
    add("newton_claim_blocked", any(row["gate_id"] == "GATE3819_5_Newton_claim" and row["gate_status"] == "BLOCKED" for row in grouped["gates"]), "Newton claim remains blocked")
    add("next_target_selected", grouped["next"][0]["target_doc"].startswith("3820-Y5"), "3820 Komar/Tolman target selected")
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    add("spine_updated", "Current State After 3819" in spine_text and "3820-Y5-R2FR-Komar-Tolman" in spine_text, "live spine updated to 3819 and 3820 target")
    fwb_hits = list(FWB.rglob("*3819*")) if FWB.exists() else []
    add("formalization_clean", len(fwb_hits) == 0, "no 3819 files written under formalization-workbench")
    add("pycache_removed", not (PCW / "scripts" / "__pycache__").exists(), "scripts __pycache__ removed")
    bad_chars = "\ufffd" in read_text(DOC_PATH) or "\ufffd" in read_text(Path(__file__)) or "\ufffd" in spine_text
    add("bad_chars_clean", not bad_chars, "new doc/script/spine contain no mojibake replacement characters")
    return rows


def main() -> None:
    timestamp = now_utc()
    grouped: dict[str, list[dict[str, str]]] = {}
    grouped["sources"] = source_rows(timestamp)
    grouped["selector"] = selector_rows(timestamp)
    grouped["active_mass"] = active_mass_rows(timestamp)
    grouped["pim"] = pim_rows(timestamp)
    grouped["gm"] = gm_rows(timestamp)
    grouped["residuals"] = residual_rows(timestamp)
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["decisions"] = decision_rows(timestamp)
    grouped["next"] = next_rows(timestamp)
    grouped["status"] = status_rows(timestamp)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
