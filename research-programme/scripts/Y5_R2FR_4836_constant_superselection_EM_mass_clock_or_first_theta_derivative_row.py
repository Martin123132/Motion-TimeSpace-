from __future__ import annotations

import csv
import math
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4836"
CLAIM_ID = "L-678"
MARKER = "PPC4161_CONSTANT_SUPERSELECTION_EM_MASS_CLOCK_OR_FIRST_THETA_DERIVATIVE_ROW_4836"
PACKET_MARKER = "PPC4161_PACKET_CONSTANT_SUPERSELECTION_EM_MASS_CLOCK_OR_FIRST_THETA_DERIVATIVE_ROW_4836"
DECISION = "CONSTANT_SUPERSELECTION_UNSIGNED_FIRST_THETA_DERIVATIVE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md"

DOC_PATH = POST / "4836-Y5-R2FR-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md"
FORMAL_PATH = FORMAL / "852-PPC4161-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "constant_superselection_theta_derivative_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4836_SOURCE_REGISTER.csv"
THETA_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4836_CONSTANT_SUPERSELECTION_AUDIT.csv"
THETA_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4836_THETA_DERIVATIVE_ROW_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4836_THETA_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4836_THETA_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4836_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4836_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4836_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4836_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4836_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4835_doc": POST / "4835-Y5-R2FR-matter-quotient-constant-sector-or-first-qbarXT-source-row.md",
    "637_doc": POST / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
    "621_doc": POST / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
    "622_doc": POST / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
    "621_priors": SOURCE_DIR / "P8_Y5_R10_621_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "621_arenas": SOURCE_DIR / "P8_Y5_R10_621_ARENA_PRIOR_SCHEMA.csv",
    "622_contract": SOURCE_DIR / "P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
    "622_smoke": SOURCE_DIR / "P8_Y5_R10_622_SMOKE_PRIOR_ROWS.csv",
    "2611_chain": SOURCE_DIR / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv",
    "2611_premise": SOURCE_DIR / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv",
    "2611_interface": SOURCE_DIR / "P8_Y5_MATTER_DESCENT_GATE_2611_AMATTER_BOUND_INTERFACE.csv",
    "2587_contract": SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "4835_output": SOURCE_DIR / "P8_Y5_R2FR_4835_QBARXT_RUNNER_OUTPUT.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def as_float(value: Any) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return math.nan


def close_to(value: Any, target: float, tolerance: float = 1e-14) -> bool:
    number = as_float(value)
    return math.isfinite(number) and abs(number - target) <= tolerance


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4836_00_resume", SOURCES["resume"], "4836-Y5-R2FR-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md", "4835 selected this constants target."),
        ("SRC4836_01_4835_doc", SOURCES["4835_doc"], "DEC4835_2_next", "constant superselection handoff."),
        ("SRC4836_02_637_descent", SOURCES["637_doc"], "CO637_0_descent_criterion", "theta descent criterion."),
        ("SRC4836_03_637_alpha", SOURCES["637_doc"], "CS637_1_em_charge_alpha", "EM charge/alpha blocker."),
        ("SRC4836_04_637_mass", SOURCES["637_doc"], "CS637_2_particle_masses", "mass-ratio blocker."),
        ("SRC4836_05_621_normal", SOURCES["621_doc"], "NMF621_3_constant_triviality", "normal-form constant clause."),
        ("SRC4836_06_621_alpha", SOURCES["621_doc"], "CP621_1_alpha_EM", "alpha derivative prior."),
        ("SRC4836_07_621_clocks", SOURCES["621_doc"], "AP621_3_clocks_EM", "clock/EM arena dependency."),
        ("SRC4836_08_622_contract", SOURCES["622_doc"], "PMC622_4_constant_superselection", "parent constant contract."),
        ("SRC4836_09_622_map_alpha", SOURCES["622_doc"], "MAP622_1_constants_alpha", "alpha prior map."),
        ("SRC4836_10_622_mass", SOURCES["622_doc"], "SP622_2_mass_ratio", "mass prior smoke row."),
        ("SRC4836_11_621_priors_alpha", SOURCES["621_priors"], "CP621_1_alpha_EM", "source CSV alpha derivative."),
        ("SRC4836_12_621_priors_mass", SOURCES["621_priors"], "CP621_2_mass_ratios", "source CSV mass derivative."),
        ("SRC4836_13_621_arenas", SOURCES["621_arenas"], "AP621_3_clocks_EM", "source CSV clocks/EM arena."),
        ("SRC4836_14_622_contract_csv", SOURCES["622_contract"], "PMC622_4_constant_superselection", "contract CSV constants."),
        ("SRC4836_15_622_smoke_alpha", SOURCES["622_smoke"], "SP622_1_alpha_EM", "alpha placeholder row."),
        ("SRC4836_16_622_smoke_mass", SOURCES["622_smoke"], "SP622_2_mass_ratio", "mass placeholder row."),
        ("SRC4836_17_2611_chain", SOURCES["2611_chain"], "CR2611_2_constants", "matter descent constants term."),
        ("SRC4836_18_2611_premise", SOURCES["2611_premise"], "PRE2611_3_constants", "constant premise audit."),
        ("SRC4836_19_2611_interface", SOURCES["2611_interface"], "AM2611_2_A_theta", "A_theta bound interface."),
        ("SRC4836_20_2587_contract", SOURCES["2587_contract"], "MCA2587_2_minimal_matter_terms", "minimal matter syntax."),
        ("SRC4836_21_4835_output", SOURCES["4835_output"], "RUN4835_4_direct_qbarXT_smoke_pass", "upstream qbarXT feed."),
        ("SRC4836_22_runner", SOURCES["runner"], "def evaluate_row", "4836 executable runner."),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theta_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("TSC4836_0_descent", "theta descent criterion", "theta_A is silent iff fixed representation data or theta_A=theta_bar_A(q(Phi)); Dq[v_X]=0 gives Lie_v theta_A=0", "MATH_CONDITIONAL_PASS", "parent classification of each theta_A"),
        ("TSC4836_1_alpha", "fine-structure/charge", "d_ln_alpha_EM_dXhat = Lie_v alpha_EM / alpha_EM", "OPEN_BLOCKER", "derive alpha_EM as quotient/topological representation datum or source derivative row"),
        ("TSC4836_2_mass", "mass ratios", "d_ln_mu_i_dXhat = Lie_v(m_i/m_ref)/(m_i/m_ref)", "OPEN_BLOCKER", "derive mass-ratio representation theorem or source derivative row"),
        ("TSC4836_3_clock", "clock ratios", "d_ln_nu_clock = K_alpha d_ln_alpha + K_mu d_ln_mu + K_nuc d_ln_nuclear", "BOUND_INTERFACE_READY", "clock sensitivities plus sourced primitive derivatives"),
        ("TSC4836_4_dimensionless_guard", "unit-choice guard", "only dimensionless constants/ratios count; bare c,hbar,G or unit rescalings cannot prove zero", "GUARD_ACTIVE", "dimensionless source rows"),
        ("TSC4836_5_A_theta", "A_theta matter residual", "A_theta <= ||J_theta||_* (S_alpha|dlnalpha|+S_mass|dlnmu|+S_clock|dlnnu_clock|+S_material|dlnmaterial|)", "RUNNER_READY_VALUES_MISSING", "source-backed derivative and sensitivity coefficients"),
        ("TSC4836_6_source_test", "same source/test constants", "source and test body must use the same theta branch before WEP/R10/local-GR claims", "OPEN_BLOCKER", "same-branch certificate"),
        ("TSC4836_7_G_guard", "Newton constant/calibration guard", "dimensionful measured G or orbital GM is not a theta-zero proof; kappa/source-current branch must own it separately", "GUARD_ACTIVE", "future kappa/source-current derivation"),
    ]
    return [
        {
            "clause_id": clause_id,
            "object": obj,
            "formula": formula,
            "current_result": result,
            "needed_signature_or_input": needed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, obj, formula, result, needed in rows
    ]


def theta_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("THC4836_0_zero", "b_theta=0", "representation category + theta superselection + quotient/topological alpha + mass-ratio theorem + clock ratio theorem", "conditional_only"),
        ("THC4836_1_vector", "D_v ln theta", "(d_ln_alpha_EM_dXhat, d_ln_mass_ratio_dXhat, d_ln_clock_ratio_dXhat, d_ln_material_standard_dXhat)", "first_source_row_schema"),
        ("THC4836_2_clock", "clock sensitivity projection", "d_ln_nu_clock <= K_alpha d_ln_alpha + K_mass d_ln_mu + K_nuclear d_ln_nuclear", "runner_ready"),
        ("THC4836_3_A_theta", "A_theta_matter", "||J_theta||_* ||D_v ln theta||_sensitivity", "runner_ready_values_missing"),
        ("THC4836_4_qbar", "qbar_XT theta feed", "P_theta_qbar A_theta -> alpha_source=K Qbar qbar_theta", "runner_ready_values_missing"),
        ("THC4836_5_next", "EM stress/Poynting alpha branch", "derive Maxwell stress/charge normal form or source d_ln_alpha row", "next_target"),
    ]
    return [
        {
            "contract_id": contract_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, quantity, definition, status in rows
    ]


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "source_signed": "true",
        "dimensionless_units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero = {
        "representation_category_signed": "true",
        "theta_superselection_signed": "true",
        "vertical_theta_derivative_zero_signed": "true",
        "alpha_EM_quotient_or_topological_signed": "true",
        "mass_ratios_representation_signed": "true",
        "clock_ratios_from_same_theta_signed": "true",
        "no_X_running_coupling_slot_signed": "true",
        "no_unit_rescaling_of_dimensionless_observables_signed": "true",
        "no_material_marker_theta_signed": "true",
        "no_clock_readout_absorption_signed": "true",
        "same_theta_for_source_and_test_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    direct = {
        "J_theta_norm_abs": "2.0",
        "d_ln_alpha_EM_dXhat_abs": "0.0015",
        "S_alpha_abs": "1.0",
        "d_ln_mass_ratio_dXhat_abs": "0.0005",
        "S_mass_abs": "1.0",
        "d_ln_clock_ratio_dXhat_abs": "0.0004",
        "S_clock_abs": "0.5",
        "d_ln_material_standard_dXhat_abs": "0.0002",
        "S_material_abs": "1.0",
        "P_theta_qbar_abs": "1.0",
        "Qbar_source_XH_bound_abs": "0.01475",
        "K_source_abs": "1.5",
        "tau_BY5_theta_abs": "2.0",
    }
    clock = {
        "J_theta_norm_abs": "2.0",
        "d_ln_alpha_EM_dXhat_abs": "0.0015",
        "clock_K_alpha_abs": "0.2",
        "d_ln_mass_ratio_dXhat_abs": "0.0005",
        "clock_K_mass_abs": "0.1",
        "d_ln_nuclear_ratio_dXhat_abs": "0.0001",
        "clock_K_nuclear_abs": "0.5",
        "S_alpha_abs": "1.0",
        "S_mass_abs": "1.0",
        "S_clock_abs": "0.5",
        "d_ln_material_standard_dXhat_abs": "0.0002",
        "S_material_abs": "1.0",
        "P_theta_qbar_abs": "1.0",
        "Qbar_source_XH_bound_abs": "0.01475",
        "K_source_abs": "1.5",
        "tau_BY5_theta_abs": "2.0",
    }
    doc_637 = str(SOURCES["637_doc"])
    doc_622 = str(SOURCES["622_doc"])
    prior_621 = str(SOURCES["621_priors"])
    interface_2611 = str(SOURCES["2611_interface"])
    return [
        {
            "row_id": "RUN4836_0_live_theta_zero_missing",
            "route_type": "theta_zero",
            "route": "live constant superselection zero audit",
            "source_path": doc_637,
            "equation_ref": "CO637_0_descent_criterion;CS637_1_em_charge_alpha;CS637_2_particle_masses",
            "notes": "current MTS has the descent criterion but lacks parent-signed alpha_EM, mass-ratio and clock constant classification",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_1_conditional_theta_zero_pass",
            "route_type": "theta_zero",
            "route": "conditional parent signed theta superselection",
            "source_path": doc_622,
            "equation_ref": "PMC622_4_constant_superselection",
            "notes": "nonclaim theorem-shape smoke row for b_theta zero",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_2_live_theta_bound_missing",
            "route_type": "theta_direct_bound",
            "route": "live first theta derivative row missing",
            "source_path": prior_621,
            "equation_ref": "CP621_1_alpha_EM;CP621_2_mass_ratios",
            "notes": "schema exists but source-backed derivative coefficients are not filled",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_3_direct_theta_bound_smoke_pass",
            "route_type": "theta_direct_bound",
            "route": "direct finite theta derivative smoke",
            "source_path": interface_2611,
            "equation_ref": "AM2611_2_A_theta",
            "notes": "nonclaim arithmetic smoke for A_theta and qbar theta feed",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_4_clock_sensitivity_smoke_pass",
            "route_type": "theta_clock_sensitivity_bound",
            "route": "clock sensitivity finite theta derivative smoke",
            "source_path": str(SOURCES["621_arenas"]),
            "equation_ref": "AP621_3_clocks_EM",
            "notes": "nonclaim arithmetic smoke deriving d_ln_clock from alpha, mass and nuclear sensitivities",
            **base,
            **clock,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_5_forbidden_constants_asserted_silent",
            "route_type": "theta_zero",
            "route": "forbidden constants silent by assertion",
            "source_path": doc_637,
            "equation_ref": "CO637_0_descent_criterion",
            "notes": "CONSTANTS_SILENT_BY_ASSERTION cannot close alpha_EM, mass or clock constants",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_6_forbidden_unit_rescaling",
            "route_type": "theta_zero",
            "route": "forbidden unit rescaling zero",
            "source_path": doc_637,
            "equation_ref": "CS637_1_em_charge_alpha",
            "notes": "UNIT_RESCALING_AS_ZERO cannot change dimensionless alpha_EM or mass ratios",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_7_forbidden_bare_dimensionful_constant",
            "route_type": "theta_direct_bound",
            "route": "forbidden bare dimensionful constant",
            "source_path": prior_621,
            "equation_ref": "CP621_1_alpha_EM",
            "notes": "BARE_DIMENSIONFUL_CONSTANT cannot be used as a physical theta derivative",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_8_forbidden_clock_readout_absorption",
            "route_type": "theta_clock_sensitivity_bound",
            "route": "forbidden clock readout absorption",
            "source_path": str(SOURCES["621_arenas"]),
            "equation_ref": "AP621_3_clocks_EM",
            "notes": "CLOCK_READOUT_ABSORPTION cannot hide clock sensitivity coefficients",
            **base,
            **clock,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_9_forbidden_measured_GM_source",
            "route_type": "theta_direct_bound",
            "route": "forbidden measured GM source",
            "source_path": doc_622,
            "equation_ref": "PMC622_4_constant_superselection",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize alpha_EM or mass-ratio derivative rows",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_10_forbidden_source_test_split_ignored",
            "route_type": "theta_zero",
            "route": "forbidden source/test split ignored",
            "source_path": doc_622,
            "equation_ref": "PMC622_4_constant_superselection",
            "notes": "SOURCE_TEST_SPLIT_IGNORED cannot close WEP/R10 theta branch",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_11_forbidden_charge_normalization_cheat",
            "route_type": "theta_direct_bound",
            "route": "forbidden charge normalization cheat",
            "source_path": doc_637,
            "equation_ref": "CS637_1_em_charge_alpha",
            "notes": "CHARGE_NORMALIZATION_CHEAT cannot erase the fine-structure derivative",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_12_forbidden_cancellation",
            "route_type": "theta_clock_sensitivity_bound",
            "route": "forbidden cancellation of unknown theta components",
            "source_path": str(SOURCES["621_arenas"]),
            "equation_ref": "AP621_3_clocks_EM",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot make theta residuals small",
            **base,
            **clock,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4836_13_forbidden_GR_import",
            "route_type": "theta_zero",
            "route": "forbidden GR import of constants",
            "source_path": doc_622,
            "equation_ref": "PMC622_4_constant_superselection",
            "notes": "GR_IMPORT cannot replace parent MTS constant superselection",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4836_0_zero", "Constant superselection has a clean conditional theorem but is not live-signed.", "If theta_A is fixed representation data or descends through q, Lie_v theta_A=0; current corpus has not classified alpha_EM, mass ratios and clocks that way.", "keep b_theta zero nonclaim", False),
        ("DEC4836_1_bound", "The first theta derivative source row is executable.", "If superselection fails, alpha_EM, mass-ratio, clock-ratio and material-standard derivatives feed A_theta and then qbar_XT.", "source or theorem-zero each theta derivative", False),
        ("DEC4836_2_guard", "Dimensionful constants and measured GM cannot be used as shortcuts.", "Only dimensionless observables/ratios can test constant variation; kappa/Newton-G ownership belongs to the separate source-current branch.", "do not use unit rescaling or measured GM as proof", False),
        ("DEC4836_3_next", "The next target should attack EM stress/Poynting/alpha.", "alpha_EM is the sharpest constant-sector bridge into Maxwell/EM stress and the user's Poynting-vector intuition.", NEXT_TARGET, False),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, because, next_action, valid_for_claim in rows
    ]


def claim_gates(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4836_0_runner_installed", "constant superselection/theta derivative gate is executable", True, "runner computes theta-zero, direct derivative and clock-sensitivity routes", False),
        ("CG4836_1_zero_unsigned", "b_theta is theorem-zero for live MTS", False, "alpha_EM, mass ratios, clocks and material standards are not parent-classified", False),
        ("CG4836_2_bound_ready", "finite theta derivative source row is staged", True, "smoke rows compute A_theta, qbar theta feed, alpha and BY5", False),
        ("CG4836_3_dimensionless_guard", "unit-choice and measured-G shortcuts fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4836_4_no_local_claim", "local GR/Newton/R10/WEP/clock/EM claims remain blocked", True, "no runner row allows a claim", False),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in rows
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "claim_id": CLAIM_ID,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive EM/Maxwell stress and Poynting/alpha normal form or stage first alpha derivative source row",
            "include": "Maxwell stress tensor, Poynting vector, gauge coupling/fine-structure constant, charge normalization, dimensionless alpha derivative, source paths, units",
            "exclude": "charge normalization cheat, unit rescaling zero, clock readout absorption, measured GM denominator, cancellation, GR import",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def run_runner() -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    return read_csv(RUNNER_OUTPUT)


def validate(timestamp: str, outputs: list[dict[str, str]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    expected = {
        "RUN4836_0_live_theta_zero_missing": "BLOCKED_THETA_ZERO_CLAUSES",
        "RUN4836_1_conditional_theta_zero_pass": "THETA_ZERO_PASS_NONCLAIM",
        "RUN4836_2_live_theta_bound_missing": "BLOCKED_DIRECT_THETA_DERIVATIVE_INPUTS",
        "RUN4836_3_direct_theta_bound_smoke_pass": "DIRECT_THETA_DERIVATIVE_BOUND_PASS_NONCLAIM",
        "RUN4836_4_clock_sensitivity_smoke_pass": "CLOCK_SENSITIVITY_THETA_BOUND_PASS_NONCLAIM",
        "RUN4836_5_forbidden_constants_asserted_silent": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_6_forbidden_unit_rescaling": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_7_forbidden_bare_dimensionful_constant": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_8_forbidden_clock_readout_absorption": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_9_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_10_forbidden_source_test_split_ignored": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_11_forbidden_charge_normalization_cheat": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_12_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4836_13_forbidden_GR_import": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    direct = by_id.get("RUN4836_3_direct_theta_bound_smoke_pass", {})
    clock = by_id.get("RUN4836_4_clock_sensitivity_smoke_pass", {})
    forbidden_ids = [row_id for row_id in expected if "_forbidden_" in row_id]
    checks = [
        ("VAL4836_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4836_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4836_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4836_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4836_04_live_zero_blocked", by_id["RUN4836_0_live_theta_zero_missing"]["runner_status"] == "BLOCKED_THETA_ZERO_CLAUSES", "live b_theta zero remains blocked"),
        ("VAL4836_05_live_bound_blocked", by_id["RUN4836_2_live_theta_bound_missing"]["runner_status"] == "BLOCKED_DIRECT_THETA_DERIVATIVE_INPUTS", "live theta derivative row remains missing"),
        ("VAL4836_06_direct_smoke_pass", close_to(direct.get("theta_log_residual_abs"), 0.0024) and close_to(direct.get("A_theta_matter_abs"), 0.0048) and close_to(direct.get("qbar_XT_theta_feed_abs"), 0.0048) and close_to(direct.get("alpha_source_abs"), 0.0001062) and close_to(direct.get("BY5_theta_feed_abs"), 0.0096), "direct theta smoke computes A_theta and qbar feed"),
        ("VAL4836_07_clock_smoke_pass", close_to(clock.get("clock_ratio_bound_abs"), 0.0004) and close_to(clock.get("theta_log_residual_abs"), 0.0024) and close_to(clock.get("A_theta_matter_abs"), 0.0048), "clock sensitivity smoke derives same theta envelope"),
        ("VAL4836_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in forbidden_ids), "forbidden shortcuts fail closed"),
        ("VAL4836_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4836_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4836_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
    ]
    return [
        {
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def write_docs(
    timestamp: str,
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    outputs: list[dict[str, str]],
    decision_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    doc = f"""# 4836 Y5 R2FR constant superselection EM mass clock or first theta derivative row

**Status:** 4836 narrows the coupling problem to the constant sector. The exact local-zero route is now explicit: `theta_A` is silent only when it is fixed representation/superselection data or descends through the parent quotient. If that is not parent-signed, the theory must retain dimensionless derivative rows for `alpha_EM`, mass ratios, clock ratios and material standards.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, WEP, clock, EM, Maxwell-stress, source-charge, constant-zero, or calibrated-coupling claim is allowed from 4836.

## Core derivation

```text
theta_A = theta_bar_A(q(Phi)) or fixed representation data
Dq[v_X] = 0
=> Lie_v theta_A = D theta_bar_A(Dq[v_X]) = 0

If not parent-signed:

D_v ln theta =
  (d ln alpha_EM/dXhat,
   d ln mass_ratio/dXhat,
   d ln clock_ratio/dXhat,
   d ln material_standard/dXhat)

d ln clock_ratio <= K_alpha d ln alpha_EM
                    + K_mass d ln mass_ratio
                    + K_nuclear d ln nuclear_ratio

A_theta <= ||J_theta||_* (
  S_alpha |d ln alpha_EM|
  + S_mass |d ln mass_ratio|
  + S_clock |d ln clock_ratio|
  + S_material |d ln material_standard|
)

qbar_XT_theta_feed = P_theta_qbar A_theta
alpha_source = K_source Qbar_source_XH_bound qbar_XT_theta_feed
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Constant-sector audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## Theta derivative contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "theta_log_residual_abs", "clock_ratio_bound_abs", "A_theta_matter_abs", "qbar_XT_theta_feed_abs", "alpha_source_abs", "BY5_theta_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 852 PPC4161 constant superselection EM mass clock or first theta derivative row

Checkpoint: `{DOC_PATH}`

4836 separates a true constant-zero theorem from a boundable residual row. If `theta_A` is quotient-descended or fixed representation data, `Lie_v theta_A=0`. Otherwise `alpha_EM`, mass-ratio, clock-ratio and material-standard derivatives feed `A_theta`, then `qbar_XT`.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "constant_superselection_EM_mass_clock_or_first_theta_derivative_row",
        "current_evidence": "4836 proves the conditional constant-superselection route and stages an executable dimensionless theta-derivative bound row; live alpha_EM/mass/clock coefficients remain missing.",
        "status": "constant_superselection_theta_derivative_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "alpha_EM, mass-ratio, clock-ratio and material-standard constants are not parent-classified as quotient/topological representation data",
        "sector": "local_gr_Newton_Maxwell_EM_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live theta derivatives are not source-backed",
        "title": "Constant superselection EM/mass/clock or first theta derivative row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    if CLAIMS_PATH.exists():
        rows = read_csv(CLAIMS_PATH)
        if any(existing.get("claim_id") == CLAIM_ID for existing in rows):
            return
        fields = list(rows[0].keys()) if rows else list(row.keys())
        for key in row:
            if key not in fields:
                fields.append(key)
        rows.append(row)
        with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def update_spine_and_packet(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4836 constant superselection / theta derivative gate

`{MARKER}`. The constant-sector coupling fork is now explicit. `b_theta=0` requires parent-signed quotient/topological/representation ownership of `alpha_EM`, mass ratios, clock ratios and material standards. Without that, a dimensionless `D_v ln theta` source row feeds `A_theta`, `qbar_XT`, and the local coupling bound. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4836 constant superselection EM/mass/clock or first theta derivative row

`{MARKER}` blocks the constants-by-unit-choice shortcut. The allowed proof is quotient/superselection descent; the allowed fallback is a dimensionless derivative row for `alpha_EM`, mass ratios, clock ratios and material standards. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4836-Y5-R2FR-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md`
Marker: `{MARKER}`

## Where we are

4836 made the constant-sector coupling fork executable:

```text
theta_A = theta_bar_A(q(Phi)) or fixed representation data
Dq[v_X]=0
=> Lie_v theta_A=0

If not signed:
A_theta <= ||J_theta||_* (
  S_alpha |d ln alpha_EM|
  + S_mass |d ln mass_ratio|
  + S_clock |d ln clock_ratio|
  + S_material |d ln material_standard|
)

qbar_XT_theta_feed = P_theta_qbar A_theta
alpha_source = K_source Qbar_source_XH_bound qbar_XT_theta_feed
```

## Live blockers

- `b_theta=0` is conditional only: `alpha_EM`, mass ratios, clocks and material standards are not parent-classified as quotient/topological representation data.
- The first finite theta derivative row is executable, but live values for `d_ln_alpha_EM_dXhat`, `d_ln_mass_ratio_dXhat`, clock sensitivities and material-standard derivatives remain missing.
- Dimensionful constants, unit rescalings, measured/orbital `GM`, clock readout absorption, charge-normalization tricks, cancellation and GR import are forbidden.
- Newton's `G`/source calibration is not solved here; it belongs to the separate kappa/source-current branch once the Hilbert current is owned.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = theta_audit(timestamp)
    contract = theta_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(THETA_AUDIT, audit)
    write_csv(THETA_CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)
    outputs = run_runner()
    decision_rows = decisions(timestamp)
    gate_rows = claim_gates(timestamp)
    write_csv(DECISION_CSV, decision_rows)
    write_csv(CLAIM_GATES, gate_rows)
    write_csv(STATUS_CSV, status_rows(timestamp))
    write_csv(NEXT_TARGET_CSV, next_target_rows(timestamp))
    validation = validate(timestamp, outputs, sources)
    write_csv(VALIDATION_CSV, validation)
    write_docs(timestamp, sources, audit, contract, outputs, decision_rows, validation)
    update_claims(timestamp)
    update_spine_and_packet(timestamp)
    update_resume(timestamp)
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        print(f"4836 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
