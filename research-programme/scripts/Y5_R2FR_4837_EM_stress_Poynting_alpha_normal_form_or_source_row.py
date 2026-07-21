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

CHECKPOINT = "4837"
CLAIM_ID = "L-679"
MARKER = "PPC4161_EM_STRESS_POYNTING_ALPHA_NORMAL_FORM_OR_SOURCE_ROW_4837"
PACKET_MARKER = "PPC4161_PACKET_EM_STRESS_POYNTING_ALPHA_NORMAL_FORM_OR_SOURCE_ROW_4837"
DECISION = "EM_STRESS_POYNTING_ALPHA_NORMAL_FORM_UNSIGNED_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4838-Y5-R2FR-kappa-G-source-normalization-Newtonian-limit-gate.md"

DOC_PATH = POST / "4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md"
FORMAL_PATH = FORMAL / "853-PPC4161-EM-stress-Poynting-alpha-normal-form-or-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "em_stress_poynting_alpha_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4837_SOURCE_REGISTER.csv"
EM_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4837_EM_STRESS_POYNTING_ALPHA_AUDIT.csv"
EM_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4837_EM_SOURCE_ROW_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4837_EM_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4837_EM_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4837_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4837_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4837_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4837_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4837_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4836_doc": POST / "4836-Y5-R2FR-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md",
    "637_doc": POST / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
    "1057_doc": POST / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md",
    "1397_doc": POST / "1397-Y5-R10-RAB-unique-Maxwell-F2-proof-or-lambdaA-source-row.md",
    "990_doc": POST / "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md",
    "poynting": SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
    "hodge": SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
    "unique_status": SOURCE_DIR / "P8_EM_unique_F2_or_calibrated_alpha_status.csv",
    "visible_status": SOURCE_DIR / "P8_EM_visible_EM_first_owner_branch_status.csv",
    "scalar_status": SOURCE_DIR / "P8_EM_scalar_gauge_coupling_owner_status.csv",
    "current_alpha": SOURCE_DIR / "P8_EM_current_source_Ward_alpha_source_residual.csv",
    "alpha_runner": SOURCE_DIR / "P8_EM_alpha_coupling_bound_runner_results.csv",
    "alpha_source_runner": SOURCE_DIR / "P8_EM_alpha_source_bound_runner_results.csv",
    "hodge_flow": SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
    "local_interface": SOURCE_DIR / "P8_local_GR_calibrated_alpha_source_interface_status.csv",
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
        ("SRC4837_00_resume", SOURCES["resume"], "4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md", "4836 selected this EM target."),
        ("SRC4837_01_4836_doc", SOURCES["4836_doc"], "DEC4836_3_next", "EM stress/Poynting handoff."),
        ("SRC4837_02_637_alpha", SOURCES["637_doc"], "CS637_1_em_charge_alpha", "alpha/charge blocker."),
        ("SRC4837_03_1057_unique", SOURCES["1057_doc"], "UMS1057_2_no_independent_F2", "unique Maxwell F2 blocker."),
        ("SRC4837_04_1057_alpha", SOURCES["1057_doc"], "AC1057_0_if_unique", "conditional alpha zero route."),
        ("SRC4837_05_1397_verdict", SOURCES["1397_doc"], "UMF1397_7_current_verdict", "lambda_A fallback verdict."),
        ("SRC4837_06_1397_lambda", SOURCES["1397_doc"], "LAM1397_0_lambda_A", "standalone Maxwell counterterm source row."),
        ("SRC4837_07_990_contract", SOURCES["990_doc"], "PAC990_3_EM_lock", "minimal parent action EM lock contract."),
        ("SRC4837_08_poynting_stress", SOURCES["poynting"], "EMF3502_0_minimal_bound_field_stress", "Maxwell stress/Poynting component."),
        ("SRC4837_09_poynting_flux", SOURCES["poynting"], "EMF3502_1_radiative_poynting_flux", "Poynting flux blocker."),
        ("SRC4837_10_poynting_XF2", SOURCES["poynting"], "EMF3502_2_nonminimal_XF2", "nonminimal XF2 blocker."),
        ("SRC4837_11_hodge", SOURCES["hodge"], "EMB3503_0_Delta_Hodge_EM", "Hodge/constitutive owner."),
        ("SRC4837_12_current_norm", SOURCES["hodge"], "EMB3503_3_C_JQ", "charge-current normalization."),
        ("SRC4837_13_unique_status", SOURCES["unique_status"], "STAT3528_1_calibrated_alpha", "calibrated alpha baseline."),
        ("SRC4837_14_visible_status", SOURCES["visible_status"], "STAT3525_1_reduction", "EM residual narrowing."),
        ("SRC4837_15_scalar_identity", SOURCES["scalar_status"], "STAT3526_0_identity", "CXF2 alpha identity."),
        ("SRC4837_16_current_alpha", SOURCES["current_alpha"], "CSR3508_1_b_alpha_X", "Ward alpha residual."),
        ("SRC4837_17_alpha_runner", SOURCES["alpha_runner"], "ARUN3507_0_alpha_clock", "alpha bound runner blocked row."),
        ("SRC4837_18_alpha_source_runner", SOURCES["alpha_source_runner"], "ASRUN3508_0_z_g_alpha", "source alpha bound runner blocked row."),
        ("SRC4837_19_hodge_flow", SOURCES["hodge_flow"], "DHB3504_0_Delta_Hodge_EM", "Hodge flow bound vector."),
        ("SRC4837_20_local_interface", SOURCES["local_interface"], "STAT3529_1_EM_stress", "calibrated Maxwell stress interface."),
        ("SRC4837_21_runner", SOURCES["runner"], "def evaluate_row", "4837 executable runner."),
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


def em_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("EM4837_0_calibrated_identity", "calibrated Maxwell stress", "delta S_EM/dg -> T_EM and S_Poynting=E cross B on observed geometry", "USABLE_CONDITIONAL_IDENTITY", "observed Hodge/current gates remain"),
        ("EM4837_1_hodge", "observed EM Hodge/coframe", "*_EM = *_obs[e_obs(q)]", "OPEN_BLOCKER", "parent observed Hodge/constitutive signature"),
        ("EM4837_2_unique_F2", "unique Maxwell kinetic owner", "S_EM = -1/4 (C_P N_Q) int F_Q^2 with no lambda_A F_Q^2", "FAILS_CURRENT_CORPUS", "operator-domain exhaustion or retain lambda_A"),
        ("EM4837_3_XF2", "nonminimal hidden-visible EM operator", "C_XF2 = D_X ln(lambda_A/e_obs^2) = -D_X ln alpha_EM", "EXACT_IDENTITY_NOT_ZERO", "zero theorem or finite alpha derivative source row"),
        ("EM4837_4_charge_current", "charge-current normalization", "A -> lambda A and J -> J/lambda ambiguity fixed by same parent owner", "OPEN_BLOCKER", "T_Q/current/charge lattice owner"),
        ("EM4837_5_poynting", "radiative/background Poynting flux", "Phi_EM_rad = integral_boundary S_Poynting dot n dA", "OPEN_BLOCKER", "stationary isolated zero theorem or flux bound"),
        ("EM4837_6_exchange", "matter-EM internal exchange", "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda cancels matter Lorentz exchange in total stress", "CONDITIONAL_TOTAL_STRESS_ZERO", "same matter+EM parent action/current"),
        ("EM4837_7_alpha_baseline", "calibrated alpha branch", "alpha_EM can be fixed as local measured input, not MTS-predicted", "SAFE_BASELINE_NONCLAIM", "nonzero C_XF2 branch must be scored"),
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


def em_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("EMC4837_0_zero", "EM residual zero", "observed Hodge + minimal Maxwell action + unique F2 + charge-current owner + alpha superselection + no Poynting flux", "conditional_only"),
        ("EMC4837_1_stress", "Maxwell stress residual", "epsilon_EM_bound + Delta_Hodge_EM + w_EM + C_JQ + epsilon_internal_exchange", "runner_ready"),
        ("EMC4837_2_alpha", "alpha drift residual", "C_XF2 + w_EM + C_JQ + C_EM_readout", "runner_ready"),
        ("EMC4837_3_poynting", "Poynting flux residual", "Phi_EM_rad/(G_ref M_H) or window-normalized flux row", "runner_ready"),
        ("EMC4837_4_alpha_identity", "b_alpha identity", "b_alpha = 2 z_g - z_lambda plus readout; absolute bound uses 2|z_g|+|z_lambda|+|C_readout|", "runner_ready"),
        ("EMC4837_5_next", "kappa/G/Newton source gate", "return to source-current normalization and Newtonian Poisson denominator", "next_target"),
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
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero = {
        "observed_hodge_coframe_signed": "true",
        "minimal_maxwell_action_signed": "true",
        "unique_F2_parent_owner_signed": "true",
        "fixed_charge_current_normalization_signed": "true",
        "alpha_superselection_signed": "true",
        "no_nonminimal_XF2_signed": "true",
        "poynting_boundary_flux_zero_signed": "true",
        "matter_EM_exchange_total_stress_signed": "true",
        "readout_radiative_closure_signed": "true",
        "no_unit_rescaling_alpha_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    direct = {
        "epsilon_EM_bound_abs": "0.001",
        "Delta_Hodge_EM_abs": "0.002",
        "w_EM_abs": "0.001",
        "C_XF2_abs": "0.0015",
        "C_JQ_abs": "0.0005",
        "Phi_EM_rad_abs": "0.0004",
        "C_EM_readout_abs": "0.0006",
        "epsilon_internal_exchange_abs": "0.0003",
        "P_EM_qbar_abs": "1.0",
        "Qbar_source_XH_bound_abs": "0.01475",
        "K_source_abs": "1.5",
        "tau_BY5_EM_abs": "2.0",
    }
    alpha = {
        "z_g_abs": "0.0002",
        "z_lambda_abs": "0.001",
        "C_EM_readout_abs": "0.0003",
        "K_alpha_clock_abs": "0.2",
        "tau_clock_abs": "0.5",
        "beta_source_alpha_abs": "0.3",
        "tau_WEP_abs": "0.4",
        "P_alpha_qbar_abs": "1.0",
        "Qbar_source_XH_bound_abs": "0.01475",
        "K_source_abs": "1.5",
        "tau_BY5_alpha_abs": "2.0",
    }
    return [
        {
            "row_id": "RUN4837_0_live_EM_zero_missing",
            "route_type": "em_zero",
            "route": "live EM stress Poynting alpha zero audit",
            "source_path": str(SOURCES["local_interface"]),
            "equation_ref": "STAT3529_1_EM_stress;STAT3528_0_unique_F2;STAT3526_2_live_blocker",
            "notes": "current MTS has calibrated Maxwell bookkeeping but not joint Hodge/F2/current/alpha/Poynting ownership",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4837_1_conditional_EM_zero_pass",
            "route_type": "em_zero",
            "route": "conditional parent signed EM normal form",
            "source_path": str(SOURCES["poynting"]),
            "equation_ref": "EMF3502_0_minimal_bound_field_stress;EMF3502_5_matter_EM_internal_exchange",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4837_2_live_EM_bound_missing",
            "route_type": "em_residual_bound",
            "route": "live EM source row missing",
            "source_path": str(SOURCES["hodge"]),
            "equation_ref": "EMB3503_0_Delta_Hodge_EM;EMB3503_2_C_XF2;EMB3503_4_Phi_EM_rad",
            "notes": "source row schema exists but live coefficients are not source-backed",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4837_3_direct_EM_bound_smoke_pass",
            "route_type": "em_residual_bound",
            "route": "direct finite EM stress Poynting alpha smoke",
            "source_path": str(SOURCES["poynting"]),
            "equation_ref": "EMF3502_0_minimal_bound_field_stress;EMF3502_1_radiative_poynting_flux;EMF3502_2_nonminimal_XF2",
            "notes": "nonclaim arithmetic smoke for Maxwell stress, Poynting flux and alpha drift residuals",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4837_4_alpha_identity_smoke_pass",
            "route_type": "alpha_identity_bound",
            "route": "finite alpha identity product smoke",
            "source_path": str(SOURCES["current_alpha"]),
            "equation_ref": "CSR3508_1_b_alpha_X",
            "notes": "nonclaim arithmetic smoke for b_alpha=2z_g-zlambda plus readout absolute envelope",
            **base,
            **alpha,
            "timestamp_utc": timestamp,
        },
        *forbidden_rows(timestamp, base, zero, direct, alpha),
    ]


def forbidden_rows(timestamp: str, base: dict[str, str], zero: dict[str, str], direct: dict[str, str], alpha: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {"row_id": "RUN4837_5_forbidden_unique_F2_aesthetic", "route_type": "em_zero", "route": "forbidden unique F2 by aesthetic", "source_path": str(SOURCES["1057_doc"]), "equation_ref": "UMS1057_2_no_independent_F2", "notes": "UNIQUE_F2_BY_AESTHETIC cannot ban lambda_A F_Q^2", **base, **zero, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_6_forbidden_hodge_assertion", "route_type": "em_zero", "route": "forbidden Hodge match by assertion", "source_path": str(SOURCES["hodge"]), "equation_ref": "EMB3503_0_Delta_Hodge_EM", "notes": "HODGE_MATCH_BY_ASSERTION cannot prove *_EM=*_obs", **base, **zero, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_7_forbidden_dropped_XF2", "route_type": "em_residual_bound", "route": "forbidden dropped XF2", "source_path": str(SOURCES["scalar_status"]), "equation_ref": "STAT3526_0_identity", "notes": "DROPPED_XF2 cannot erase the alpha drift throat", **base, **direct, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_8_forbidden_calibrated_alpha_derived", "route_type": "em_zero", "route": "forbidden calibrated alpha as derived", "source_path": str(SOURCES["unique_status"]), "equation_ref": "STAT3528_1_calibrated_alpha", "notes": "CALIBRATED_ALPHA_AS_DERIVED is not a parent alpha proof", **base, **zero, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_9_forbidden_poynting_ignored", "route_type": "em_residual_bound", "route": "forbidden Poynting flux ignored", "source_path": str(SOURCES["poynting"]), "equation_ref": "EMF3502_1_radiative_poynting_flux", "notes": "POYNTING_FLUX_IGNORED cannot close boundary energy flow", **base, **direct, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_10_forbidden_charge_norm_cheat", "route_type": "alpha_identity_bound", "route": "forbidden charge normalization cheat", "source_path": str(SOURCES["hodge"]), "equation_ref": "EMB3503_3_C_JQ", "notes": "CHARGE_NORMALIZATION_CHEAT cannot fix A/J/alpha together", **base, **alpha, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_11_forbidden_unit_rescaling", "route_type": "alpha_identity_bound", "route": "forbidden unit rescaling alpha zero", "source_path": str(SOURCES["637_doc"]), "equation_ref": "CS637_1_em_charge_alpha", "notes": "UNIT_RESCALING_AS_ZERO cannot change dimensionless alpha_EM", **base, **alpha, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_12_forbidden_measured_GM_source", "route_type": "em_residual_bound", "route": "forbidden measured GM source", "source_path": str(SOURCES["local_interface"]), "equation_ref": "STAT3529_3_next", "notes": "MEASURED_GM_AS_SOURCE cannot normalize EM source residuals", **base, **direct, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_13_forbidden_cancellation", "route_type": "em_residual_bound", "route": "forbidden cancellation of unknown EM components", "source_path": str(SOURCES["hodge"]), "equation_ref": "EMB3503_2_C_XF2", "notes": "CANCEL_UNKNOWN_COMPONENTS cannot make EM residuals small", **base, **direct, "timestamp_utc": timestamp},
        {"row_id": "RUN4837_14_forbidden_GR_import", "route_type": "em_zero", "route": "forbidden GR import of Maxwell stress", "source_path": str(SOURCES["990_doc"]), "equation_ref": "DEP990_0_EM_not_GR", "notes": "GR_IMPORT cannot replace parent MTS EM normal form", **base, **zero, "timestamp_utc": timestamp},
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4837_0_identity", "Calibrated Maxwell stress/Poynting is usable as a conditional bookkeeping identity.", "The corpus already records variation of calibrated Maxwell action as a source interface, but Hodge/current/F2 gates remain.", "use EM stress in local source ledger only with residual gates visible", False),
        ("DEC4837_1_zero", "The live EM zero theorem is not signed.", "Unique F2 fails current corpus, C_XF2 is an exact alpha throat, charge-current normalization and Poynting flux remain open.", "retain EM source row", False),
        ("DEC4837_2_alpha", "Alpha may be calibrated locally but not claimed derived.", "This lets Maxwell/GR source bookkeeping proceed honestly while any nonzero C_XF2 branch must face clock/WEP/R10 bounds.", "do not sell calibrated alpha as a prediction", False),
        ("DEC4837_3_next", "Return to kappa/G/source normalization and Newtonian limit.", "EM is now fenced; the decisive GR/Newton denominator is the Hilbert source-current/kappa/G branch.", NEXT_TARGET, False),
    ]
    return [{"decision_id": i, "decision": d, "because": b, "next_action": n, "valid_for_claim": v, "timestamp_utc": timestamp} for i, d, b, n, v in rows]


def claim_gates(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4837_0_runner_installed", "EM stress/Poynting/alpha gate is executable", True, "runner computes zero, direct residual, and alpha identity routes", False),
        ("CG4837_1_zero_unsigned", "EM residual is theorem-zero for live MTS", False, "Hodge, unique F2, charge-current, alpha and Poynting clauses are not jointly signed", False),
        ("CG4837_2_bound_ready", "finite EM source row is staged", True, "smoke rows compute EM total, qbar feed, alpha source and BY5", False),
        ("CG4837_3_shortcuts_fail", "aesthetic F2, Hodge assertion, dropped XF2, calibrated-alpha-as-derived, Poynting ignore, charge cheat, unit rescale, measured GM, cancellation and GR import fail closed", True, "forbidden rows fail in runner", False),
        ("CG4837_4_no_local_claim", "local GR/Newton/Maxwell-source claims remain blocked", True, "no runner row allows a claim", False),
    ]
    return [{"gate_id": i, "claim": c, "gate_pass": p, "reason": r, "claim_allowed": a, "valid_for_claim": False, "timestamp_utc": timestamp} for i, c, p, r, a in rows]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "marker": MARKER, "decision": DECISION, "claim_id": CLAIM_ID, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp}]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive or bound kappa/G source normalization and the Newtonian Poisson denominator after EM alpha is fenced",
            "include": "Hilbert source current, kappa, G_ref/G_N, source mass M_H, Poisson limit, calibrated EM stress contribution, PPN residual vector",
            "exclude": "measured GM substitution, orbital calibration as derivation, EM alpha shortcut, hidden source prefactor, cancellation, GR import",
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
        "RUN4837_0_live_EM_zero_missing": "BLOCKED_EM_STRESS_ALPHA_ZERO_CLAUSES",
        "RUN4837_1_conditional_EM_zero_pass": "EM_STRESS_ALPHA_ZERO_PASS_NONCLAIM",
        "RUN4837_2_live_EM_bound_missing": "BLOCKED_EM_RESIDUAL_BOUND_INPUTS",
        "RUN4837_3_direct_EM_bound_smoke_pass": "EM_RESIDUAL_BOUND_PASS_NONCLAIM",
        "RUN4837_4_alpha_identity_smoke_pass": "ALPHA_IDENTITY_BOUND_PASS_NONCLAIM",
        "RUN4837_5_forbidden_unique_F2_aesthetic": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_6_forbidden_hodge_assertion": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_7_forbidden_dropped_XF2": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_8_forbidden_calibrated_alpha_derived": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_9_forbidden_poynting_ignored": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_10_forbidden_charge_norm_cheat": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_11_forbidden_unit_rescaling": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_12_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_13_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4837_14_forbidden_GR_import": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    direct = by_id.get("RUN4837_3_direct_EM_bound_smoke_pass", {})
    alpha = by_id.get("RUN4837_4_alpha_identity_smoke_pass", {})
    forbidden_ids = [row_id for row_id in expected if "_forbidden_" in row_id]
    checks = [
        ("VAL4837_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4837_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4837_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4837_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4837_04_live_zero_blocked", by_id["RUN4837_0_live_EM_zero_missing"]["runner_status"] == "BLOCKED_EM_STRESS_ALPHA_ZERO_CLAUSES", "live EM zero remains blocked"),
        ("VAL4837_05_live_bound_blocked", by_id["RUN4837_2_live_EM_bound_missing"]["runner_status"] == "BLOCKED_EM_RESIDUAL_BOUND_INPUTS", "live EM source row remains missing"),
        ("VAL4837_06_direct_smoke_pass", close_to(direct.get("maxwell_stress_residual_abs"), 0.0048) and close_to(direct.get("poynting_flux_residual_abs"), 0.0004) and close_to(direct.get("alpha_drift_residual_abs"), 0.0036) and close_to(direct.get("EM_total_residual_abs"), 0.0088) and close_to(direct.get("alpha_source_abs"), 0.0001947), "direct EM smoke computes stress, Poynting and alpha envelope"),
        ("VAL4837_07_alpha_identity_smoke_pass", close_to(alpha.get("alpha_drift_residual_abs"), 0.0017) and close_to(alpha.get("EM_total_residual_abs"), 0.002074) and close_to(alpha.get("alpha_source_abs"), 0.00004588725), "alpha identity smoke computes b_alpha product envelope"),
        ("VAL4837_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in forbidden_ids), "forbidden shortcuts fail closed"),
        ("VAL4837_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4837_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4837_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
    ]
    return [{"validation_id": i, "result": "PASS" if p else "FAIL", "detail": d, "timestamp_utc": timestamp} for i, p, d in checks]


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], decision_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    doc = f"""# 4837 Y5 R2FR EM stress Poynting alpha normal form or source row

**Status:** 4837 fences the EM route. Calibrated Maxwell stress and the Poynting vector are usable as conditional source bookkeeping on the observed geometry, but MTS does not yet derive the full EM normal form. The live gates are observed Hodge/coframe ownership, unique Maxwell `F^2`, charge-current normalization, nonminimal `X F^2`, radiative/readout closure, and exterior Poynting flux.

**Decision:** `{DECISION}`.

**Claim ceiling:** no derived-alpha, Maxwell-source, local-GR, Newtonian, R10, WEP, clock, PPN, or calibrated-coupling claim is allowed from 4837.

## Core derivation

```text
S_EM = -1/4 integral mu_obs lambda_EM F_mu_nu F^mu_nu
delta_g S_EM -> T_EM
S_Poynting = E cross B

Zero route:
*_EM = *_obs[e_obs(q)]
lambda_EM = C_P N_Q with no lambda_A F_Q^2 and no f_X(Phi)F_Q^2
charge/current normalization fixed by same parent owner
Phi_EM_rad = integral_boundary S_Poynting dot n dA = 0

Fallback:
EM_total =
  (epsilon_EM_bound + Delta_Hodge_EM + w_EM + C_JQ + epsilon_internal_exchange)
  + Phi_EM_rad
  + (C_XF2 + w_EM + C_JQ + C_EM_readout)

qbar_XT_EM_feed = P_EM_qbar EM_total
alpha_source = K_source Qbar_source_XH_bound qbar_XT_EM_feed
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## EM audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## EM source-row contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "maxwell_stress_residual_abs", "poynting_flux_residual_abs", "alpha_drift_residual_abs", "EM_total_residual_abs", "qbar_XT_EM_feed_abs", "alpha_source_abs", "BY5_EM_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 853 PPC4161 EM stress Poynting alpha normal form or source row

Checkpoint: `{DOC_PATH}`

4837 turns the EM route into an owner-or-bound gate. Maxwell stress/Poynting can be used as calibrated bookkeeping only while Hodge, unique F2, charge-current normalization, XF2, readout and Poynting-flux residuals remain explicit.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "EM_stress_Poynting_alpha_normal_form_or_source_row",
        "current_evidence": "4837 stages an executable EM stress/Poynting/alpha owner-or-bound gate; calibrated Maxwell stress is usable as conditional bookkeeping but live EM normal-form clauses are unsigned.",
        "status": "EM_stress_Poynting_alpha_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "unique F2, Hodge/coframe, charge-current normalization, nonminimal XF2, readout and Poynting flux gates remain unsigned",
        "sector": "Maxwell_EM_source_coupling_local_GR_Newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live EM coefficients are not source-backed",
        "title": "EM stress Poynting alpha normal form or source row",
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
        f"""## PPC4161 4837 EM stress / Poynting / alpha gate

`{MARKER}`. The EM route is now fenced: calibrated Maxwell stress and Poynting flow may be used as conditional source bookkeeping, but derived Maxwell/alpha requires observed-Hodge ownership, unique `F^2`, charge-current normalization, no `X F^2`, readout closure and zero/bounded exterior Poynting flux. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4837 EM stress Poynting alpha normal form or source row

`{MARKER}` stops the alpha loop becoming a fake win. Alpha can be calibrated locally, but not claimed derived; nonzero `C_XF2` must enter the residual/vector branch. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md`
Marker: `{MARKER}`

## Where we are

4837 fenced the EM stress/Poynting/alpha route:

```text
S_EM = -1/4 integral mu_obs lambda_EM F^2
delta_g S_EM -> T_EM
S_Poynting = E cross B

EM_total =
  (epsilon_EM_bound + Delta_Hodge_EM + w_EM + C_JQ + epsilon_internal_exchange)
  + Phi_EM_rad
  + (C_XF2 + w_EM + C_JQ + C_EM_readout)

qbar_XT_EM_feed = P_EM_qbar EM_total
alpha_source = K_source Qbar_source_XH_bound qbar_XT_EM_feed
```

## Live blockers

- Maxwell stress/Poynting is usable as calibrated bookkeeping, not yet as a derived MTS prediction.
- Unique `F^2`, observed Hodge/coframe, charge-current normalization, `C_XF2`, readout/radiative closure and Poynting flux remain open.
- Calibrated `alpha_EM` is allowed as a baseline; derived `alpha_EM` is not claimed.
- Unit rescaling, charge-normalization cheats, ignored Poynting flux, dropped `X F^2`, measured/orbital `GM`, cancellation and GR import are forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = em_audit(timestamp)
    contract = em_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(EM_AUDIT, audit)
    write_csv(EM_CONTRACT, contract)
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
        print(f"4837 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
