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

CHECKPOINT = "4838"
CLAIM_ID = "L-680"
MARKER = "PPC4161_KAPPA_G_SOURCE_NORMALIZATION_NEWTONIAN_LIMIT_GATE_4838"
PACKET_MARKER = "PPC4161_PACKET_KAPPA_G_SOURCE_NORMALIZATION_NEWTONIAN_LIMIT_GATE_4838"
DECISION = "KAPPA_G_SOURCE_NEWTON_LIMIT_UNSIGNED_SOURCE_DENOMINATOR_STAGED_NONCLAIM"
NEXT_TARGET = "4839-Y5-R2FR-Hilbert-source-current-descent-or-first-MHref-source-row.md"

DOC_PATH = POST / "4838-Y5-R2FR-kappa-G-source-normalization-Newtonian-limit-gate.md"
FORMAL_PATH = FORMAL / "854-PPC4161-kappa-G-source-normalization-Newtonian-limit-gate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "kappa_G_source_Newton_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4838_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4838_KAPPA_G_NEWTON_ZERO_AUDIT.csv"
CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4838_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4838_NEWTON_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4838_NEWTON_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4838_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4838_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4838_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4838_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4838_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4837_doc": POST / "4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md",
    "4719_doc": POST / "4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md",
    "4778_doc": POST / "4778-Y5-R2FR-Hamiltonian-mass-source-functional-runner-or-E00-bound-input.md",
    "4825_doc": POST / "4825-Y5-R2FR-BY5-source-functor-zero-or-first-source-normalization-row.md",
    "4825_output": SOURCE_DIR / "P8_Y5_R2FR_4825_BY5_SOURCE_FUNCTOR_RUNNER_OUTPUT.csv",
    "4826_output": SOURCE_DIR / "P8_Y5_R2FR_4826_PIM_COMMUTATOR_RUNNER_OUTPUT.csv",
    "kappa_status": SOURCE_DIR / "P8_local_GR_kappa_G_Newtonian_gate_status.csv",
    "hilbert_denominator": SOURCE_DIR / "P8_local_GR_Hilbert_source_denominator_status.csv",
    "pim_htau": SOURCE_DIR / "P8_local_GR_PiM_Htau_zero_mechanism_status.csv",
    "kappa_contract": SOURCE_DIR / "P8_Y5_R2FR_3530_KAPPA_G_CONTRACT.csv",
    "poisson_gates": SOURCE_DIR / "P8_Y5_R2FR_3530_POISSON_PPN_GATES.csv",
    "denominator_bounds": SOURCE_DIR / "P8_Y5_R2FR_3531_NEWTON_DENOMINATOR_BOUND_ROWS.csv",
    "poisson_chain": SOURCE_DIR / "P8_Y5_R2FR_3499_POISSON_NEWTON_THEOREM_CHAIN.csv",
    "gref_signature": SOURCE_DIR / "P8_Y5_R2FR_3500_CONSTANT_GREF_SIGNATURE.csv",
    "kappa_gref": SOURCE_DIR / "P8_Y5_R2FR_3511_KAPPA_GREF_ACTION_LINE_LOCK_THEOREM.csv",
    "hilbert_current": SOURCE_DIR / "P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv",
    "pim_identity": SOURCE_DIR / "P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv",
    "density_qbasic": SOURCE_DIR / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
    "em_source": SOURCE_DIR / "P8_Y5_R2FR_3620_MAXWELL_SOURCE_CALIBRATION_GATE.csv",
    "source_runner": SOURCE_DIR / "P8_Y5_R2FR_3639_SOURCE_NORMALIZATION_RUNNER_ROWS.csv",
    "poisson_calibration": SOURCE_DIR / "P8_Y5_R2FR_3754_POISSON_CALIBRATION_ROWS.csv",
    "kappa_theorem": SOURCE_DIR / "P8_Y5_R2FR_3755_KAPPA_THEOREM_ROWS.csv",
    "kappa_coeffs": SOURCE_DIR / "P8_Y5_R2FR_3768_KAPPA_RESIDUAL_COEFFICIENTS.csv",
    "newton_gm": SOURCE_DIR / "P8_Y5_R2FR_3772_NEWTON_GM_RESIDUAL_COEFFICIENTS.csv",
    "newton_hamiltonian": SOURCE_DIR / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv",
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
        ("SRC4838_00_resume", SOURCES["resume"], "4838-Y5-R2FR-kappa-G-source-normalization-Newtonian-limit-gate.md", "4837 handoff to kappa/G/Newton gate."),
        ("SRC4838_01_4837_doc", SOURCES["4837_doc"], "EM_STRESS_POYNTING_ALPHA_NORMAL_FORM_UNSIGNED_SOURCE_ROW_STAGED_NONCLAIM", "EM stress must be included once, not dropped or double-counted."),
        ("SRC4838_02_4719_poisson", SOURCES["4719_doc"], "LFE4719_3_Poisson_equation_with_residual", "linearized EH to Poisson bridge."),
        ("SRC4838_03_4778_mass", SOURCES["4778_doc"], "RC4778_1_mass_residual", "Hamiltonian mass/source residual runner."),
        ("SRC4838_04_4825_BY5", SOURCES["4825_doc"], "B_Y5_trace", "BY5 source-normalization tail."),
        ("SRC4838_05_4825_output", SOURCES["4825_output"], "RUN4825_3_live_BY5_bound_missing", "live BY5 source row remains blocked."),
        ("SRC4838_06_4826_output", SOURCES["4826_output"], "RUN4826_3_live_bound_missing", "PiM commutator live bound remains blocked."),
        ("SRC4838_07_kappa_status", SOURCES["kappa_status"], "STAT3530_0_kappa", "kappa/G policy and Newton gate status."),
        ("SRC4838_08_hilbert_denominator", SOURCES["hilbert_denominator"], "STAT3531_0_denominator", "Hilbert source denominator status."),
        ("SRC4838_09_pim_htau", SOURCES["pim_htau"], "STAT3532_0_RPiM", "PiM/Htau zero mechanism status."),
        ("SRC4838_10_kappa_contract", SOURCES["kappa_contract"], "KG3530_0_EH_coefficient", "EH coefficient and calibrated G contract."),
        ("SRC4838_11_poisson_gates", SOURCES["poisson_gates"], "PNG3530_2_Newton_Poisson", "Newton/Poisson gate."),
        ("SRC4838_12_denominator_bounds", SOURCES["denominator_bounds"], "HSDB3531_0_Gdot_denominator", "denominator bound targets."),
        ("SRC4838_13_poisson_chain", SOURCES["poisson_chain"], "PNC3499_2_EH_00_to_Poisson", "EH 00 to Poisson theorem chain."),
        ("SRC4838_14_gref_signature", SOURCES["gref_signature"], "GREF3500_2_no_orbital_absorption", "no orbital GM absorption guard."),
        ("SRC4838_15_kappa_gref", SOURCES["kappa_gref"], "KGL3511_2_product_lock_identity", "G_ref/product lock identity."),
        ("SRC4838_16_hilbert_current", SOURCES["hilbert_current"], "HC3558_2_closure_sufficient_conditions", "Hilbert source current closure."),
        ("SRC4838_17_pim_identity", SOURCES["pim_identity"], "PIA3559_1_identity_chainmap_zero", "typed PiM identity-chainmap route."),
        ("SRC4838_18_density_qbasic", SOURCES["density_qbasic"], "HDQ3561_1_pullback_density_theorem", "Hilbert density q-basic pullback route."),
        ("SRC4838_19_em_source", SOURCES["em_source"], "MCG3620_2_unique_F2", "EM stress/source calibration gate."),
        ("SRC4838_20_source_runner", SOURCES["source_runner"], "SNR3639_1_no_cancellation", "source-normalization no-cancellation guard."),
        ("SRC4838_21_poisson_calibration", SOURCES["poisson_calibration"], "PC3754_2_poisson_coefficient", "Poisson coefficient law."),
        ("SRC4838_22_kappa_theorem", SOURCES["kappa_theorem"], "KT3755_2_bianchi_arbitrary_source", "Bianchi route for kappa derivative silence."),
        ("SRC4838_23_kappa_coeffs", SOURCES["kappa_coeffs"], "KRC3768_1_epsilon_kappa", "kappa residual coefficient row."),
        ("SRC4838_24_newton_gm", SOURCES["newton_gm"], "NGR3772_1_active_inertial", "active/inertial source mass residual."),
        ("SRC4838_25_newton_hamiltonian", SOURCES["newton_hamiltonian"], "NSH3772_0_same_action_NR_expansion", "same-action Newton source theorem."),
        ("SRC4838_26_runner", SOURCES["runner"], "def evaluate_row", "4838 executable runner."),
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


def zero_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("KGN4838_0_EH_operator", "EH/linearized operator", "G_mu_nu=kappa_eff T_H_mu_nu + E_mu_nu with E_mu_nu=0 or bounded", "CONDITIONAL_TEMPLATE", "parent EH operator or E00/PPN residual row"),
        ("KGN4838_1_kappa", "kappa/G_ref constant", "kappa_eff in parent global/superselection sector or Bianchi arbitrary-source theorem", "ROUTE_EXISTS_UNSIGNED", "parent coupling owner and no readout absorption"),
        ("KGN4838_2_product_lock", "G_eff product lock", "D ln G_eff = D ln G_ref + D ln w_common + D ln ell_J + source terms", "EXACT_IDENTITY_ACTIVE", "source scale terms zero/bounded"),
        ("KGN4838_3_Hilbert_source", "Hilbert source current", "T_H and rho_H from the same q_obs-descended matter+EM action", "CONDITIONAL_UNSIGNED", "same-frame source descent and EM included once"),
        ("KGN4838_4_MHref", "M_H_ref positive denominator", "M_H_ref before orbital GM fitting", "LIVE_GAP", "worldtube/source-measure selector or finite MHref residual"),
        ("KGN4838_5_PiM_Htau", "PiM/H_tau reference lock", "typed PiM identity plus H_tau integrability and no-flux closure", "PARTIAL_ROUTE_UNSIGNED", "commutator/reference-lock/source-support residuals"),
        ("KGN4838_6_no_GM_launder", "no measured GM absorption", "mu_obs=G_ref M_H(1+epsilon_mu), not a hidden definition of M_H or G_ref", "GUARD_ACTIVE", "independent source mass/current and coupling rows"),
        ("KGN4838_7_Poisson_Gauss", "Newtonian limit/readout", "nabla^2 Phi=4*pi*G_eff rho_H + Delta_Poisson; a=-grad Phi", "DERIVED_CONDITIONAL", "source denominator plus PPN residual vector must be controlled"),
        ("KGN4838_8_EM_once", "EM stress included exactly once", "ordinary stationary EM stress belongs in T_H; Poynting/readout residual retained", "OPEN_FROM_4837", "EM normal form or finite source row"),
    ]
    return [
        {
            "clause_id": clause_id,
            "object": obj,
            "mathematical_form": form,
            "current_result": result,
            "needed_signature_or_input": needed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, obj, form, result, needed in rows
    ]


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("KGS4838_0_zero", "Newton/local-GR source residual zero", "all kappa/source/Poisson/PPN clauses signed in same branch", "conditional_only"),
        ("KGS4838_1_source_denominator", "source_denominator_residual_abs", "delta_kappa+delta_Gref+delta_MHref+delta_PiM_Htau+delta_worldtube+delta_EM_stress+delta_nonHilbert+delta_source_prefactor", "runner_ready_values_missing"),
        ("KGS4838_2_Newton_Poisson", "Newton_Poisson_residual_abs", "source_denominator_residual_abs + delta_Poisson_operator", "runner_ready_values_missing"),
        ("KGS4838_3_PPN_local", "PPN_local_residual_abs", "Newton_Poisson_residual_abs + delta_PPN_vector", "runner_ready_values_missing"),
        ("KGS4838_4_projection", "qbar/alpha/BY5 feed", "qbar=P_Newton_qbar*PPN_local; alpha=K_source*Qbar_source_XH*qbar; BY5=tau*qbar", "runner_ready_values_missing"),
        ("KGS4838_5_poisson_coefficient", "G_eff coefficient residual", "delta_kappa+delta_ZH+delta_GN_readout plus E00/MH terms", "runner_ready_values_missing"),
        ("KGS4838_6_next", "Hilbert source-current descent", "attack T_H/rho_H/M_H_ref ownership directly", "next_target"),
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


def signed_flags() -> dict[str, str]:
    flags = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
        "EH_or_linearized_operator_signed": "true",
        "Hilbert_source_current_signed": "true",
        "kappa_constant_or_parent_owned_signed": "true",
        "Gref_to_GN_readout_signed": "true",
        "MHref_positive_same_frame_signed": "true",
        "PiM_Htau_chainmap_signed": "true",
        "worldtube_support_signed": "true",
        "EM_stress_included_once_signed": "true",
        "no_nonHilbert_bypass_signed": "true",
        "no_source_prefactor_signed": "true",
        "Poisson_Gauss_limit_signed": "true",
        "PPN_residual_vector_zero_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    return flags


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    base_flags = {"source_signed": "true", "units_signed": "true", "same_branch_signed": "true", "no_cancellation_guard": "true"}
    return [
        {
            "row_id": "RUN4838_0_live_Newton_zero_missing",
            "route_type": "newton_zero",
            "route": "live kappa/G/source/Newton zero audit",
            "source_path": str(SOURCES["poisson_gates"]),
            "equation_ref": "PNG3530_1_source_denominator;PNG3530_2_Newton_Poisson",
            "notes": "live corpus has conditional Poisson bridge but not signed source denominator/Product-lock/PPN closure",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4838_1_conditional_Newton_zero_pass",
            "route_type": "newton_zero",
            "route": "conditional same-branch Newton source theorem",
            "source_path": str(SOURCES["poisson_calibration"]),
            "equation_ref": "PC3754_2_poisson_coefficient",
            "notes": "nonclaim theorem-shape smoke row",
            "timestamp_utc": timestamp,
            **signed_flags(),
        },
        {
            "row_id": "RUN4838_2_live_Newton_bound_missing",
            "route_type": "newton_source_bound",
            "route": "live finite Newton source residual row",
            "source_path": str(SOURCES["denominator_bounds"]),
            "equation_ref": "HSDB3531_0_Gdot_denominator;HSDB3531_1_WEP_source_denominator;HSDB3531_2_orbital_GM_guard",
            "notes": "source denominator residual schema exists but numeric parent-owned coefficients remain missing",
            "timestamp_utc": timestamp,
            **base_flags,
        },
        {
            "row_id": "RUN4838_3_direct_Newton_source_bound_smoke_pass",
            "route_type": "newton_source_bound",
            "route": "direct finite Newton source residual smoke",
            "source_path": str(SOURCES["poisson_chain"]),
            "equation_ref": "PNC3499_2_EH_00_to_Poisson;PNC3499_3_orbit_readout",
            "notes": "nonclaim arithmetic smoke for source denominator, Poisson and PPN residual feed",
            "timestamp_utc": timestamp,
            **base_flags,
            "delta_kappa_abs": "0.001",
            "delta_Gref_abs": "0.0007",
            "delta_MHref_abs": "0.0012",
            "delta_PiM_Htau_abs": "0.0015",
            "delta_worldtube_abs": "0.0006",
            "delta_EM_stress_abs": "0.0008",
            "delta_nonHilbert_abs": "0.0011",
            "delta_source_prefactor_abs": "0.0009",
            "delta_Poisson_operator_abs": "0.0013",
            "delta_PPN_vector_abs": "0.0014",
            "P_Newton_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_Newton_abs": "2.0",
        },
        {
            "row_id": "RUN4838_4_poisson_coefficient_smoke_pass",
            "route_type": "poisson_coefficient_bound",
            "route": "finite Poisson coefficient residual smoke",
            "source_path": str(SOURCES["poisson_calibration"]),
            "equation_ref": "PC3754_2_poisson_coefficient",
            "notes": "nonclaim arithmetic smoke for G_eff coefficient and E00/MH residual feed",
            "timestamp_utc": timestamp,
            **base_flags,
            "delta_kappa_abs": "0.0016",
            "delta_ZH_abs": "0.0009",
            "delta_GN_readout_abs": "0.0007",
            "delta_E00_abs": "0.0011",
            "delta_MH_abs": "0.0008",
            "P_Newton_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_Newton_abs": "2.0",
        },
        {
            "row_id": "RUN4838_5_forbidden_measured_GM_source",
            "route_type": "newton_zero",
            "route": "forbidden measured-GM source closure",
            "source_path": str(SOURCES["gref_signature"]),
            "equation_ref": "GREF3500_2_no_orbital_absorption",
            "notes": "MEASURED_GM_AS_SOURCE cannot define both M_H and G_ref",
            "timestamp_utc": timestamp,
            **signed_flags(),
        },
        {
            "row_id": "RUN4838_6_forbidden_calibrated_G_derived",
            "route_type": "newton_zero",
            "route": "forbidden calibrated-G derivation",
            "source_path": str(SOURCES["kappa_contract"]),
            "equation_ref": "KG3530_2_calibrated_GN",
            "notes": "CALIBRATED_G_AS_DERIVED is not allowed; calibrated baseline is not parent derivation",
            "timestamp_utc": timestamp,
            **signed_flags(),
        },
        {
            "row_id": "RUN4838_7_forbidden_source_prefactor_ignored",
            "route_type": "newton_source_bound",
            "route": "forbidden source prefactor deletion",
            "source_path": str(SOURCES["kappa_gref"]),
            "equation_ref": "KGL3511_2_product_lock_identity",
            "notes": "SOURCE_PREFACTOR_IGNORED would erase the product-lock obstruction",
            "timestamp_utc": timestamp,
            **base_flags,
        },
        {
            "row_id": "RUN4838_8_forbidden_PiM_Htau_assertion",
            "route_type": "newton_zero",
            "route": "forbidden PiM/Htau assertion",
            "source_path": str(SOURCES["pim_htau"]),
            "equation_ref": "STAT3532_0_RPiM;STAT3532_1_RHtau",
            "notes": "PIM_HTAU_BY_ASSERTION cannot replace the chainmap/integrability proof",
            "timestamp_utc": timestamp,
            **signed_flags(),
        },
        {
            "row_id": "RUN4838_9_forbidden_GR_import",
            "route_type": "newton_zero",
            "route": "forbidden GR import",
            "source_path": str(SOURCES["4719_doc"]),
            "equation_ref": "LFE4719_3_Poisson_equation_with_residual",
            "notes": "GR_IMPORT cannot substitute for a parent-owned EH/source branch",
            "timestamp_utc": timestamp,
            **signed_flags(),
        },
        {
            "row_id": "RUN4838_10_forbidden_cancellation",
            "route_type": "newton_source_bound",
            "route": "forbidden cancellation of source components",
            "source_path": str(SOURCES["source_runner"]),
            "equation_ref": "SNR3639_1_no_cancellation",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot set the source denominator to zero",
            "timestamp_utc": timestamp,
            **base_flags,
        },
    ]


def run_runner() -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    return read_csv(RUNNER_OUTPUT)


def row_by_id(rows: list[dict[str, str]], row_id: str) -> dict[str, str]:
    return next(row for row in rows if row.get("row_id") == row_id)


def status_csv(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "status": "private_nonclaim_gate_installed",
            "live_claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4838_0_policy",
            "decision": "Do not demand numerical derivation of G; demand one parent-owned coupling/source branch.",
            "effect": "keeps the GR/Newton comparison fair without laundering measured GM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4838_1_gate",
            "decision": "Newton/Poisson pass is blocked until the source denominator and PPN residual vector are signed or bounded.",
            "effect": "local-GR claim remains false but the missing object is now executable",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4838_2_next",
            "decision": NEXT_TARGET,
            "effect": "attack Hilbert source-current descent and M_H_ref owner directly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4838_0_no_G_claim", "no decimal value of G derived", "PASS_POLICY_GUARD", "GR also calibrates coupling; MTS must derive ownership/universality, not invent a dimensionful number"),
        ("CG4838_1_no_GM_launder", "measured GM cannot close source denominator", "PASS_GUARD", "M_H and G_ref must be independent before readout"),
        ("CG4838_2_live_zero", "live Newton zero route", "BLOCKED_UNSIGNED", "same-branch source denominator/PPN clauses are not signed"),
        ("CG4838_3_live_bound", "live source-bound route", "BLOCKED_MISSING_NUMERIC_INPUTS", "finite residual coefficients are not source-backed"),
        ("CG4838_4_smoke", "runner arithmetic", "PASS_NONCLAIM", "direct and coefficient smoke rows compute as expected"),
        ("CG4838_5_local_GR", "local GR/Newton claim", "NOT_ALLOWED", "no model pass while zero or live source-bound rows are blocked"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, meaning in rows
    ]


def validate(timestamp: str, sources: list[dict[str, Any]], outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "passed": bool(passed),
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4838_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4838_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all source needles found")
    add("VAL4838_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4838_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    input_rows = read_csv(RUNNER_INPUT)
    add("VAL4838_04_output_count", len(outputs) == len(input_rows), f"outputs={len(outputs)} inputs={len(input_rows)}")
    add("VAL4838_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "runner hard-codes nonclaim rows")
    live_zero = row_by_id(outputs, "RUN4838_0_live_Newton_zero_missing")
    add("VAL4838_06_live_zero_blocked", live_zero["runner_status"] == "BLOCKED_NEWTON_SOURCE_ZERO_CLAUSES", live_zero["missing_for_claim"])
    live_bound = row_by_id(outputs, "RUN4838_2_live_Newton_bound_missing")
    add("VAL4838_07_live_bound_blocked", live_bound["runner_status"] == "BLOCKED_NEWTON_SOURCE_BOUND_INPUTS", live_bound["missing_for_claim"])
    smoke = row_by_id(outputs, "RUN4838_3_direct_Newton_source_bound_smoke_pass")
    add("VAL4838_08_direct_smoke_values", all([
        close_to(smoke["source_denominator_residual_abs"], 0.0078),
        close_to(smoke["Newton_Poisson_residual_abs"], 0.0091),
        close_to(smoke["PPN_local_residual_abs"], 0.0105),
        close_to(smoke["qbar_XT_Newton_feed_abs"], 0.0105),
        close_to(smoke["alpha_source_abs"], 0.0002323125),
        close_to(smoke["BY5_Newton_feed_abs"], 0.021),
    ]), "direct smoke row computes source, Poisson, PPN, qbar, alpha and BY5 feed")
    coeff = row_by_id(outputs, "RUN4838_4_poisson_coefficient_smoke_pass")
    add("VAL4838_09_coefficient_smoke_values", all([
        close_to(coeff["G_eff_coefficient_residual_abs"], 0.0032),
        close_to(coeff["Newton_Poisson_residual_abs"], 0.0051),
        close_to(coeff["alpha_source_abs"], 0.0001128375),
    ]), "Poisson coefficient smoke row computes expected values")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4838_5_") or row["row_id"].startswith("RUN4838_6_") or row["row_id"].startswith("RUN4838_7_") or row["row_id"].startswith("RUN4838_8_") or row["row_id"].startswith("RUN4838_9_") or row["row_id"].startswith("RUN4838_10_")]
    add("VAL4838_10_forbidden_routes_fail", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "all forbidden shortcuts fail")
    add("VAL4838_11_next_target_recorded", NEXT_TARGET in read_text(NEXT_TARGET_CSV) and NEXT_TARGET in read_text(RESUME_PATH), "next target recorded in CSV and resume")
    cleanup_pycache()
    add("VAL4838_12_no_pycache_left", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def compile_ok(path: Path) -> bool:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError:
        return False
    return True


def write_next_target(timestamp: str) -> None:
    write_csv(
        NEXT_TARGET_CSV,
        [
            {
                "checkpoint": CHECKPOINT,
                "next_target": NEXT_TARGET,
                "reason": "4838 isolates the Newton bridge as a source-current/M_H_ref ownership problem.",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        ],
    )


def write_resume(timestamp: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4838-Y5-R2FR-kappa-G-source-normalization-Newtonian-limit-gate.md`
Marker: `{MARKER}`

## Where we are

4838 turns the GR/Newton bridge into an explicit kappa/G/source-normalization gate:

```text
G_eff = kappa_eff c^4/(8*pi)
nabla^2 Phi = 4*pi G_eff rho_H + Delta_Poisson
source_denominator =
  delta_kappa + delta_Gref + delta_MHref + delta_PiM_Htau
  + delta_worldtube + delta_EM_stress + delta_nonHilbert
  + delta_source_prefactor
PPN_local = source_denominator + delta_Poisson_operator + delta_PPN_vector
qbar_XT_Newton = P_Newton qbar * PPN_local
```

## Live blockers

- `G` is allowed as a calibrated local coupling, just as in GR; MTS must derive universal parent ownership and no readout laundering.
- The clean Poisson bridge exists conditionally, but the live source denominator is not yet signed.
- `M_H_ref`, same-frame Hilbert source current, `Pi_M/H_tau`, worldtube support, EM stress-in-once, and the PPN residual vector remain open.
- Measured `GM`, calibrated `G`, cancellation, GR import, ignored source prefactors, and asserted `Pi_M/H_tau` closure are forbidden.

## Next target

`{NEXT_TARGET}`
""",
    )


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4838 Y5 R2FR kappa G source normalization Newtonian limit gate

**Status:** 4838 makes the local GR/Newton bridge precise. The Poisson coefficient route is available conditionally,

```text
G_eff = kappa_eff c^4/(8*pi)
nabla^2 Phi = 4*pi G_eff rho_H + Delta_Poisson
```

but MTS still cannot claim a local-GR/Newton pass until `rho_H/M_H_ref`, `Pi_M/H_tau`, worldtube support, EM stress inclusion, and the PPN residual vector are parent-signed or source-bounded.

**Decision:** `{DECISION}`.

## Core derivation

The fair target is not to derive the decimal value of Newton's constant. GR also carries a measured coupling. The competitive MTS target is sharper:

```text
kappa_eff parent-owned or superselected
G_ref = kappa_eff c^4/(8*pi)
T_H, rho_H, M_H_ref from the same observed matter+EM source action
mu_obs = G_ref M_H (1 + epsilon_mu), with epsilon_mu explicit
```

Then the weak-field `00` equation gives the Newton coefficient, while all deviations are forced into named residuals:

```text
source_denominator_residual =
  delta_kappa + delta_Gref + delta_MHref + delta_PiM_Htau
  + delta_worldtube + delta_EM_stress + delta_nonHilbert
  + delta_source_prefactor

Newton_Poisson_residual = source_denominator_residual + delta_Poisson_operator
PPN_local_residual = Newton_Poisson_residual + delta_PPN_vector
qbar_XT_Newton_feed = P_Newton_qbar PPN_local_residual
alpha_source = K_source Qbar_source_XH qbar_XT_Newton_feed
```

## Source Register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Zero Audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## Runner Contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner Output

{md_table(outputs, ["row_id", "runner_status", "source_denominator_residual_abs", "Newton_Poisson_residual_abs", "PPN_local_residual_abs", "qbar_XT_Newton_feed_abs", "alpha_source_abs", "BY5_Newton_feed_abs", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- The old complaint "G/source coupling is missing" is now an executable gate with zero and finite-residual branches.
- `G_eff=kappa_eff c^4/(8*pi)` is treated as the conditional GR/Newton coefficient bridge, not as a fake derivation of the measured number `G`.
- The source-denominator failure is narrowed to same-frame Hilbert source descent, `M_H_ref`, `Pi_M/H_tau`, worldtube support, EM stress, non-Hilbert bypass and PPN residual ownership.
- Smoke rows pass only as nonclaim arithmetic. Live zero and live source-bound rows remain blocked.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 854 PPC4161 kappa G source normalization Newtonian limit gate

Checkpoint: `{DOC_PATH}`

4838 turns the GR/Newton reduction demand into a precise source-normalization contract. The local Poisson coefficient follows conditionally from the EH weak-field bridge with `G_eff=kappa_eff c^4/(8*pi)`, but MTS cannot claim local GR/Newton until the same-frame Hilbert source current and `M_H_ref` denominator are parent-owned or source-bounded.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "kappa_G_source_normalization_Newtonian_limit_gate",
        "current_evidence": "4838 converts the kappa/G/Newton bridge into an executable zero-or-finite source-denominator runner; live local-GR/Newton rows remain blocked.",
        "status": "kappa_G_Newton_source_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "same-frame Hilbert source current, M_H_ref, PiM/Htau, worldtube support, EM stress, non-Hilbert bypass and PPN residual vector remain unsigned or missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live source-denominator values are not source-backed",
        "title": "Kappa G source normalization Newtonian limit gate",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID not in existing:
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(claim_row.keys()))
            writer.writerow(claim_row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4838 kappa/G/source Newton gate

`{MARKER}`. The GR/Newton bridge is now typed correctly: MTS does not need to derive the decimal value of `G`, but it must derive or bound one parent-owned coupling and one same-frame Hilbert source denominator before readout. Live local-GR/Newton remains blocked; the source-denominator and PPN residual feeds are executable. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4838 kappa/G source normalization Newtonian limit gate

`{PACKET_MARKER}`. `{MARKER}` narrows the local-GR route to the source-current denominator rather than another vague coupling gap. The next useful attack is `{NEXT_TARGET}`.""",
    )


def cleanup_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    audit = zero_audit(timestamp)
    contract = contract_rows(timestamp)
    inputs = runner_inputs(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT, audit)
    write_csv(CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)
    write_csv(STATUS_CSV, status_csv(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_next_target(timestamp)
    write_resume(timestamp)

    outputs = run_runner()
    cleanup_pycache()
    validations = validate(timestamp, sources, outputs)
    write_csv(VALIDATION_CSV, validations)
    write_docs(timestamp, sources, audit, contract, outputs, validations)
    update_formal_registers(timestamp)
    cleanup_pycache()

    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"4838 validation failed: {failed}")
    print(f"4838 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()
