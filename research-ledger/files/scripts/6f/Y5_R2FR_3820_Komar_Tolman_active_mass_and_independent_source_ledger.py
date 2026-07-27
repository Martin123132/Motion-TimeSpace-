from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3820"
BRANCH = "MTS_R2FR_Y5_KOMAR_TOLMAN_ACTIVE_MASS_AND_INDEPENDENT_SOURCE_LEDGER_3820"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3819 = PCW / "3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md"
P_3818 = PCW / "3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md"
P_3817 = PCW / "3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md"
P_3772 = PCW / "3772-Y5-R2FR-source-Hamiltonian-normalization-or-Newton-active-passive-GM-bound.md"
P_1016 = PCW / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"

CSV_3819_ACTIVE = OUT / "P8_Y5_R2FR_3819_ACTIVE_MASS_LAW.csv"
CSV_3819_SELECTOR = OUT / "P8_Y5_R2FR_3819_SOURCE_SELECTOR_THEOREM.csv"
CSV_3819_GM = OUT / "P8_Y5_R2FR_3819_GM_ANTI_CIRCULARITY_CONTRACT.csv"
CSV_3819_RESID = OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3817_HILBERT = OUT / "P8_Y5_R2FR_3817_HILBERT_STRESS_PRESERVATION_THEOREM.csv"
CSV_3772_THEOREM = OUT / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv"
CSV_1016_CONTRACT = OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3820_SOURCE_REGISTER.csv",
    "komar": OUT / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv",
    "corrections": OUT / "P8_Y5_R2FR_3820_PRESSURE_BINDING_CORRECTION_LAW.csv",
    "ledger": OUT / "P8_Y5_R2FR_3820_INDEPENDENT_SOURCE_LEDGER_TEMPLATE.csv",
    "split": OUT / "P8_Y5_R2FR_3820_GM_SPLIT_TEST_CONTRACT.csv",
    "residuals": OUT / "P8_Y5_R2FR_3820_ACTIVE_MASS_RESIDUAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3820_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3820_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3820_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3820_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3820_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3820_0_3819_doc", P_3819, "Komar/Tolman active-mass route"),
    ("SRC3820_1_3819_active", CSV_3819_ACTIVE, "AML3819_0_Komar_Tolman_stationary_selector"),
    ("SRC3820_2_3819_selector", CSV_3819_SELECTOR, "SST3819_2_dressed_Hamiltonian_source_mass"),
    ("SRC3820_3_3819_gm", CSV_3819_GM, "GM3819_1_independent_mass_inputs"),
    ("SRC3820_4_3819_residual", CSV_3819_RESID, "R3819_5_pressure_binding"),
    ("SRC3820_5_3818_doc", P_3818, "EH To Poisson"),
    ("SRC3820_6_3818_poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
    ("SRC3820_7_3817_doc", P_3817, "Hilbert stress"),
    ("SRC3820_8_3817_hilbert", CSV_3817_HILBERT, "HSP3817_3_same_current_total_stress"),
    ("SRC3820_9_3772_doc", P_3772, "GM degeneracy"),
    ("SRC3820_10_3772_theorem", CSV_3772_THEOREM, "NSH3772_4_three_mass_identity"),
    ("SRC3820_11_1016_contract", CSV_1016_CONTRACT, "PSC1016_5_dressed_source_charge"),
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
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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
                "source_role": "Komar/Tolman active mass and source ledger input",
            }
        )
    return rows


def komar_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "derivation_id": "KT3820_0_stationary_charge_owner",
            "status": "EXACT_CONDITIONAL_GEOMETRIC_CHARGE",
            "statement": "If the observed local branch has a fixed stationary time generator tau and a fixed reference, the active source mass is the Hamiltonian/Noether charge of tau, not an orbital fit parameter.",
            "formula": "M_H_ref(W)=c^-2*(H_tau[W,S]-H_ref)",
            "requires": "single observed frame, fixed tau, fixed H_ref, fixed W_src and S_link",
            "failure_mode": "selector/readout circularity",
        },
        {
            "derivation_id": "KT3820_1_Komar_surface_to_EH_volume",
            "status": "EXACT_CONDITIONAL_EH_IDENTITY",
            "statement": "On an EH branch with stationary tau, the surface charge equals the Tolman/Komar volume integral of total Hilbert stress plus boundary/reference residuals.",
            "formula": "M_K=(2/c^2)*int_Sigma (T_ab-0.5*T*g_ab)n^a tau^b dSigma + R_boundary",
            "requires": "EH normal form, Bianchi/Ward total stress, stationary tau, controlled boundary",
            "failure_mode": "R_EH_owner or R_worldtube_boundary survives",
        },
        {
            "derivation_id": "KT3820_2_perfect_fluid_active_density",
            "status": "EXACT_CONDITIONAL_MATTER_LIMIT",
            "statement": "For a static perfect-fluid sector in the same frame, the active density entering the Tolman mass has pressure weight, schematically rho_active=rho_energy+3p/c^2 before closed-system stress cancellations.",
            "formula": "rho_KT = rho_energy + 3*p/c^2 + rho_anisotropic_stress + rho_binding_boundary",
            "requires": "matter model, pressure/stress tensor, total-system domain",
            "failure_mode": "pressure/binding terms are dropped without proof",
        },
        {
            "derivation_id": "KT3820_3_closed_system_warning",
            "status": "NO_PRESSURE_ONLY_CLAIM",
            "statement": "The pressure term cannot be read as an isolated extra source unless container, binding, field and boundary stresses are included; otherwise the source mass is not a closed-system charge.",
            "formula": "M_closed = int(rho_energy + stress_trace/c^2 + binding_boundary_terms)dV",
            "requires": "total Hilbert source domain, not sector-only matter labels",
            "failure_mode": "Tolman pressure paradox / missing stabilizing stresses",
        },
        {
            "derivation_id": "KT3820_4_slow_weak_Newton_limit",
            "status": "EXACT_CONDITIONAL_SLOW_LIMIT",
            "statement": "For cold, weakly bound, slowly moving closed sources, the active charge reduces to ordinary rest-plus-internal energy over c^2 up to explicit retained corrections.",
            "formula": "M_H_ref = M_rest + E_internal/c^2 + E_binding/c^2 + E_field/c^2 + Delta_stress/c^2 + R_boundary + R_nonEH",
            "requires": "small v^2/c^2, p/(rho c^2), binding/(Mc^2), field tails, nonEH residuals",
            "failure_mode": "Newton mass limit not numerically bounded",
        },
        {
            "derivation_id": "KT3820_5_Poisson_source_replacement",
            "status": "DERIVED_CONDITIONAL_SOURCE_REFINEMENT",
            "statement": "The Poisson source symbol from 3818 is refined to the selected active density; using bare density is allowed only after the correction vector is zeroed or bounded.",
            "formula": "nabla^2 Phi = 4*pi*G_ref*(rho_KT + delta_rho_source)",
            "requires": "3818 EH-to-Poisson bridge plus KT3820 source charge",
            "failure_mode": "R_active_density and R_pressure_binding remain",
        },
        {
            "derivation_id": "KT3820_6_verdict",
            "status": "VIABLE_NOT_CLAIMED",
            "statement": "The source-mass route is no longer only a placeholder: it has a concrete Komar/Tolman active-charge derivation path, but closure waits on stress/binding cancellation or source-backed bounds.",
            "formula": "M_H_ref = M_KT + R_active_density + R_pressure_binding + R_boundary + R_nonEH",
            "requires": "3821 stress-virial or finite-bound pass",
            "failure_mode": "no Newton/local-GR claim",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def correction_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("COR3820_0_pressure_trace", "epsilon_pressure", "pressure/stress-trace correction to active mass", "int(3p/c^2 + anisotropic_trace/c^2)dV / M_ref", "dimensionless", "derive closed-system cancellation or bound p/(rho c^2)"),
        ("COR3820_1_kinetic_internal", "epsilon_kin_int", "kinetic and internal energy correction", "(E_kin+E_internal)/(M_ref*c^2)", "dimensionless", "source-backed thermodynamic or virial bound"),
        ("COR3820_2_binding", "epsilon_binding", "binding/stabilizing stress correction", "E_binding/(M_ref*c^2) plus stabilizer stress trace", "dimensionless", "closed total-system stress ledger"),
        ("COR3820_3_field_energy", "epsilon_field", "EM/Poynting/field energy admitted to total Hilbert source", "E_field/(M_ref*c^2) plus tail flux", "dimensionless", "same-current EM/source domain gate"),
        ("COR3820_4_boundary_reference", "epsilon_boundary_ref", "boundary, exact improvement, and H_ref subtraction residual", "Delta B_tau/(M_ref*c^2)", "dimensionless", "fixed reference and surface class"),
        ("COR3820_5_nonEH_operator", "epsilon_nonEH", "non-EH metric operator/source correction", "||DeltaE_res|| source-equivalent norm", "dimensionless_after_norm", "EH owner theorem-zero or numeric operator bound"),
        ("COR3820_6_source_total", "epsilon_source_total", "total active-source correction vector", "sum_abs(epsilon_pressure,epsilon_kin_int,epsilon_binding,epsilon_field,epsilon_boundary_ref,epsilon_nonEH)", "dimensionless", "all correction terms zeroed or bounded in one shared ledger"),
    ]
    return [
        {
            **base_row(timestamp),
            "correction_id": correction_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "units": units,
            "exit_requirement": exit_requirement,
            "current_status": "FINITE_BOUND_REQUIRED",
        }
        for correction_id, symbol, definition, formula, units, exit_requirement in specs
    ]


def ledger_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "ledger_id": "LED3820_0_lab_source_mass",
            "arena": "R10_WEP_lab",
            "allowed_source_evidence": "weighed source masses, composition/density-volume, calibration certificate, geometry files, uncertainty",
            "forbidden_evidence": "force-law fit converted into mass using assumed G",
            "source_status": "TEMPLATE_ONLY_NO_NUMERIC_SOURCE_ATTACHED",
            "what_it_tests": "short-range or equivalence residuals after source mass is fixed independently",
        },
        {
            "ledger_id": "LED3820_1_clock_source_body",
            "arena": "clock_redshift_Gdot_local",
            "allowed_source_evidence": "geodetic/geophysical mass model with uncertainty and independent clock potential model",
            "forbidden_evidence": "same clock/gravity residual used to define source mass",
            "source_status": "TEMPLATE_ONLY_NO_NUMERIC_SOURCE_ATTACHED",
            "what_it_tests": "G_eff/time-source residuals without absorbing source normalization",
        },
        {
            "ledger_id": "LED3820_2_solar_system_body",
            "arena": "orbital_PPN",
            "allowed_source_evidence": "independent mass model where available, density/radius/composition priors, external G_ref policy",
            "forbidden_evidence": "ephemeris mu=GM as the mass denominator for the same Newton claim",
            "source_status": "PRODUCT_ONLY_UNTIL_INDEPENDENT_MASS_LEDGER_EXISTS",
            "what_it_tests": "mu residual, PPN/readout tails, or ratios after independent source constraint",
        },
        {
            "ledger_id": "LED3820_3_galaxy_baryons",
            "arena": "SPARC_ETG_galaxy",
            "allowed_source_evidence": "photometry, gas mass, stellar M/L priors, distance/inclination uncertainty",
            "forbidden_evidence": "rotation curve residual used to set the same baryonic source mass without prior",
            "source_status": "EMPIRICAL_PILLAR_BUT_NOT_LOCAL_GR_PROOF",
            "what_it_tests": "galaxy phenomenology/source-response pillar, not the local Newton source-normalization proof alone",
        },
        {
            "ledger_id": "LED3820_4_EM_field_stress",
            "arena": "EM_stress_Poynting",
            "allowed_source_evidence": "same-current Hilbert stress plus Poynting/domain flux ledger",
            "forbidden_evidence": "matter-only labels when field energy has exterior support",
            "source_status": "CONDITIONAL_FROM_3792_3817_STYLE_GATES",
            "what_it_tests": "whether EM stress is included in total active source consistently",
        },
        {
            "ledger_id": "LED3820_5_cosmology_density",
            "arena": "FLRW_CMB_BAO_SN",
            "allowed_source_evidence": "density parameters with stated priors and covariance; separate background fit branch",
            "forbidden_evidence": "late-time expansion residual used to define the same source density being tested",
            "source_status": "SEPARATE_ROBUSTNESS_BRANCH_REQUIRED",
            "what_it_tests": "cosmological source/coupling consistency, not local GR closure by itself",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def gm_split_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "split_id": "GST3820_0_product_law",
            "status": "EXACT_TEST_ACCOUNTING",
            "formula": "delta_ln_mu = delta_ln_G_ref + delta_ln_M_H_ref + delta_readout + delta_range + delta_PPN + delta_boundary",
            "test_use": "orbital data constrain the product side unless M_H_ref is independently fixed",
            "claim_guard": "no Newton source-normalization claim from product-only data",
        },
        {
            "split_id": "GST3820_1_independent_mass_gate",
            "status": "REQUIRED_FOR_CLAIM",
            "formula": "M_H_ref = M_source_independent*(1+epsilon_source_total)",
            "test_use": "independent source ledger feeds Poisson/Gauss before orbital residual evaluation",
            "claim_guard": "valid_for_claim=false until numeric source rows and correction bounds exist",
        },
        {
            "split_id": "GST3820_2_cross_arena_guard",
            "status": "NO_PER_ARENA_TUNING",
            "formula": "same epsilon_source_total vector must feed R10, WEP, PPN, clocks, orbital and EM stress",
            "test_use": "lets MTS win by coherent field-theory accounting, not by refitting each arena",
            "claim_guard": "one shared residual vector or no claim",
        },
        {
            "split_id": "GST3820_3_observable_allowed",
            "status": "SAFE_ORBITAL_USAGE",
            "formula": "mu_fit/mu_pred - 1 constrains delta_readout+delta_range+delta_PPN+delta_boundary after source ledger",
            "test_use": "orbital data remain useful but cannot define their own denominator",
            "claim_guard": "mark orbital rows product_evidence unless source ledger is independent",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def residual_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("R3820_0_Komar_owner", "R_Komar_owner", "failure of tau-Hamiltonian/Komar charge ownership", "|M_H_ref-M_K|/M_ref", "MISSING_STATIONARY_TAU_OR_HAMILTONIAN_CHARGE"),
        ("R3820_1_Tolman_density", "R_Tolman_density", "active-density difference from naive T00/c^2 density", "||rho_KT-rho_T00||/rho_ref", "PRESSURE_STRESS_TRACE_NOT_ZEROED"),
        ("R3820_2_stress_virial", "R_stress_virial", "closed-system stress/binding cancellation residual", "|int stress_trace + binding/stabilizer terms|/(M_ref*c^2)", "CLOSED_SYSTEM_STRESS_LEDGER_MISSING"),
        ("R3820_3_source_ledger", "R_source_ledger", "lack of independent non-orbital source mass evidence", "Boolean or sigma_M/M_ref", "NO_NUMERIC_INDEPENDENT_SOURCE_ROWS"),
        ("R3820_4_mu_split", "R_mu_split", "unresolved split between G_ref, M_H_ref and observed mu", "|delta_ln_mu-delta_ln_G_ref-delta_ln_M_H_ref|", "ORBITAL_PRODUCT_ONLY"),
        ("R3820_5_total", "R_active_mass_total", "total active-mass source-normalization residual", "R_Komar_owner+R_Tolman_density+R_stress_virial+R_source_ledger+R_mu_split", "NEWTON_LOCAL_GR_SOURCE_NORMALIZATION_BLOCKED"),
    ]
    return [
        {
            **base_row(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "units": "dimensionless_after_norm",
            "current_status": status,
            "exit_requirement": "prove zero in a branch or attach numeric/source-backed bound",
        }
        for residual_id, symbol, definition, formula, status in specs
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in grouped["sources"])
    rows = [
        ("GATE3820_0_sources", "PASS_NONCLAIM" if sources_pass else "FAIL", "all source paths and needles present" if sources_pass else "missing source path or needle"),
        ("GATE3820_1_Komar_Tolman_derivation", "PASS_NONCLAIM", "active mass route derived conditionally from stationary EH/Hilbert stress"),
        ("GATE3820_2_pressure_binding", "BLOCKED_BOUND_REQUIRED", "pressure, binding, field and boundary terms retained rather than dropped"),
        ("GATE3820_3_independent_source_ledger", "BLOCKED_INPUT_REQUIRED", "ledger schema exists but no numeric independent source rows are attached"),
        ("GATE3820_4_GM_smuggling", "PASS_GUARD", "orbital GM remains product evidence, not source mass evidence"),
        ("GATE3820_5_Newton_claim", "BLOCKED", "Newton claim waits on stress cancellation/bounds and source ledger"),
        ("GATE3820_6_local_GR_claim", "BLOCKED", "local GR claim waits on source normalization plus PPN/readout closure"),
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
            "decision_id": "DEC3820_0_active_mass_route_alive",
            "decision": "Keep pursuing local GR/Newton derivation through active Hamiltonian/Tolman mass.",
            "rationale": "The source mass is now a proper charge with a known stationary volume/surface identity, not an arbitrary M parameter.",
            "next_action": "prove closed-system stress cancellation or attach finite correction bounds",
        },
        {
            "decision_id": "DEC3820_1_pressure_is_not_optional",
            "decision": "Do not drop pressure, binding, field or boundary terms.",
            "rationale": "Tolman/Komar active mass weights total stress; dropping terms would be another closure axiom.",
            "next_action": "3821 stress-virial cancellation branch",
        },
        {
            "decision_id": "DEC3820_2_source_ledger_needed",
            "decision": "Build independent source rows before using orbital data as a pass/fail test.",
            "rationale": "This prevents the hidden circular move M=mu/G.",
            "next_action": "separate independent_source from product_evidence rows",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def next_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "target_doc": "3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md",
            "target_script": "scripts/Y5_R2FR_3821_closed_system_stress_virial_cancellation_or_pressure_binding_bound.py",
            "objective": "Try to prove the closed-system stress/virial cancellation that reduces the Komar/Tolman active mass to ordinary source energy over c^2, or emit finite pressure/binding/field/boundary correction bounds.",
            "success_gate": "Either pressure/binding/stabilizer terms cancel in a closed stationary source branch, or each correction term is bounded with a source-ready unit and no claim gate opens.",
            "avoid": "do not claim Newton/local GR; do not drop pressure/stress by assumption; do not use orbital GM as source mass; do not edit formalization-workbench; do not use GitHub",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "status": "PASS_NONCLAIM_KOMAR_TOLMAN_ACTIVE_MASS_AND_SOURCE_LEDGER_BUILT",
            "summary": "3820 derives the conditional Komar/Tolman active-mass route, installs pressure/binding correction laws, creates an independent source ledger template, and selects 3821 stress-virial cancellation or finite bound.",
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
    text = f"""# 3820 - Komar/Tolman Active Mass And Independent Source Ledger

## Status

`PASS_NONCLAIM_KOMAR_TOLMAN_ACTIVE_MASS_AND_SOURCE_LEDGER_BUILT`

This checkpoint advances the local Newton/GR source problem one notch: `M_H_ref` is treated as a stationary active Hamiltonian/Komar/Tolman charge with explicit correction terms, not as `mu_fit/G_ref`. It remains nonclaim because pressure, binding, field, boundary and independent-source rows still need proof or bounds.

## Komar/Tolman Active-Mass Derivation

{md_table(grouped["komar"], ["derivation_id", "status", "statement", "formula", "requires", "failure_mode"])}

## Pressure And Binding Correction Law

{md_table(grouped["corrections"], ["correction_id", "symbol", "definition", "bound_formula", "exit_requirement"])}

## Independent Source Ledger Template

{md_table(grouped["ledger"], ["ledger_id", "arena", "allowed_source_evidence", "forbidden_evidence", "source_status"])}

## GM Split Test Contract

{md_table(grouped["split"], ["split_id", "status", "formula", "test_use", "claim_guard"])}

## Finite Residual Rows

{md_table(grouped["residuals"], ["residual_id", "symbol", "definition", "bound_formula", "current_status"])}

## Claim Gates

{md_table(grouped["gates"], ["gate_id", "gate_status", "claim_allowed", "detail"])}

## Next Target

`3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md`

Target: prove the closed-system stress/virial cancellation that reduces Komar/Tolman active mass to ordinary source energy over `c^2`, or keep pressure/binding/field/boundary corrections finite and source-ready.

## Machine Outputs

{md_table(grouped["status"], ["status", "summary"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3819",
        "# Local GR Coupling Spine - Current State After 3820",
    )
    paragraph = (
        "`3820` turns the source-mass gap into a concrete active-charge route: on a stationary EH branch with fixed `tau`, `H_ref`, source worldtube, and linking surfaces, "
        "`M_H_ref` is identified conditionally with a Komar/Tolman Hamiltonian charge, `M_K=(2/c^2) int (T_ab-0.5*T*g_ab)n^a tau^b dSigma` plus boundary/reference residuals. "
        "It sharpens the Poisson source to active density rather than bare `T00/c^2`, installs explicit pressure, binding, field, boundary, non-EH and source-ledger correction terms, and keeps orbital `GM` as product evidence only. "
        "Newton/local GR is closer but still nonclaim until closed-system stress cancellation or finite source-backed correction bounds are proved.\n\n"
    )
    if "`3820` turns the source-mass gap" not in text:
        marker = "`3819` derives the next source-normalization bridge:"
        index = text.find(marker)
        if index != -1:
            line_end = text.find("\n\n", index)
            if line_end != -1:
                text = text[: line_end + 2] + paragraph + text[line_end + 2 :]
    old_target = """`3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md`

Target: derive or bound the stationary Komar/Tolman active-mass route, pressure/binding corrections, and an independent source-mass ledger that avoids orbital-GM circularity. If not closed, keep `R_active_density`, `R_pressure_binding`, and `R_GM_anti_circularity` finite and source-ready.

This is the best next move because 3819 no longer lets the project hide behind generic missing source rows: the remaining question is whether `M_H_ref` can be owned as an active Hamiltonian charge with independently sourced mass inputs.
"""
    new_target = """`3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md`

Target: try to prove the closed-system stress/virial cancellation that reduces Komar/Tolman active mass to ordinary source energy over `c^2`, or emit finite pressure/binding/field/boundary correction bounds.

This is the best next move because 3820 makes the source charge real enough to see the next danger: pressure/stress terms cannot be hand-waved away without either a virial/closed-system theorem or a bound.
"""
    text = text.replace(old_target, new_target)
    artifacts = [
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3820_PRESSURE_BINDING_CORRECTION_LAW.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3820_INDEPENDENT_SOURCE_LEDGER_TEMPLATE.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3820_GM_SPLIT_TEST_CONTRACT.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3820_ACTIVE_MASS_RESIDUAL_ROWS.csv",
        "source-intake\\mts_residuals\\P8_Y5_BRR545_3820_VALIDATION.csv",
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
    add("doc_written", DOC_PATH.exists() and "Komar/Tolman Active-Mass Derivation" in read_text(DOC_PATH), "3820 markdown document written")
    add("komar_derivation_written", any(row["derivation_id"] == "KT3820_1_Komar_surface_to_EH_volume" for row in grouped["komar"]), "Komar/Tolman EH volume identity emitted")
    add("pressure_terms_retained", any(row["symbol"] == "epsilon_pressure" for row in grouped["corrections"]), "pressure/stress correction retained")
    add("source_ledger_written", any(row["ledger_id"] == "LED3820_2_solar_system_body" for row in grouped["ledger"]), "independent source ledger template emitted")
    add("all_ledger_nonclaim", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in grouped["ledger"]), "ledger rows remain nonclaim until sourced")
    add("gm_split_guard", any(row["split_id"] == "GST3820_0_product_law" for row in grouped["split"]), "GM product split law emitted")
    add("residual_total_row", any(row["symbol"] == "R_active_mass_total" for row in grouped["residuals"]), "total active mass residual emitted")
    add("claim_gates_closed", all(row.get("claim_allowed") == "false" for row in grouped["gates"]), "no claim gate allows a claim")
    add("newton_claim_blocked", any(row["gate_id"] == "GATE3820_5_Newton_claim" and row["gate_status"] == "BLOCKED" for row in grouped["gates"]), "Newton claim remains blocked")
    add("next_target_selected", grouped["next"][0]["target_doc"].startswith("3821-Y5"), "3821 stress-virial target selected")
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    add("spine_updated", "Current State After 3820" in spine_text and "3821-Y5-R2FR-closed-system" in spine_text, "live spine updated to 3820 and 3821 target")
    fwb_hits = list(FWB.rglob("*3820*")) if FWB.exists() else []
    add("formalization_clean", len(fwb_hits) == 0, "no 3820 files written under formalization-workbench")
    add("pycache_removed", not (PCW / "scripts" / "__pycache__").exists(), "scripts __pycache__ removed")
    bad_chars = "\ufffd" in read_text(DOC_PATH) or "\ufffd" in read_text(Path(__file__)) or "\ufffd" in spine_text
    add("bad_chars_clean", not bad_chars, "new doc/script/spine contain no mojibake replacement characters")
    return rows


def main() -> None:
    timestamp = now_utc()
    grouped: dict[str, list[dict[str, str]]] = {}
    grouped["sources"] = source_rows(timestamp)
    grouped["komar"] = komar_rows(timestamp)
    grouped["corrections"] = correction_rows(timestamp)
    grouped["ledger"] = ledger_rows(timestamp)
    grouped["split"] = gm_split_rows(timestamp)
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
