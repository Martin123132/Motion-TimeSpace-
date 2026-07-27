from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4668"
CLAIM_ID = "L-510"
BRANCH = "MTS_R2FR_Y5_CMEM_FINAL_ZERO_TO_BODY_CHARGE_SOURCE_CHARGE_GATE_4668"
MARKER = "PPC4161_CMEM_FINAL_ZERO_TO_BODY_CHARGE_SOURCE_CHARGE_GATE_4668"
PACKET_MARKER = "PPC4161_PACKET_CMEM_FINAL_ZERO_TO_BODY_CHARGE_SOURCE_CHARGE_GATE_4668"
DECISION = "CMEM_FINAL_ZERO_INSERTED_BODY_CHARGE_REDUCED_TO_BJQ_ZM_SOURCE_CHARGE_GATE_NONCLAIM"
NEXT_TARGET = "4669-Y5-R2FR-Bmem-Jmem-Qboundary-ZM-source-normalization-zero-or-first-body-charge-row.md"

DOC_PATH = POST / "4668-Y5-R2FR-Cmem-final-zero-to-body-charge-source-charge-gate.md"
FORMAL_PATH = FORMAL / "684-PPC4161-Cmem-final-zero-to-body-charge-source-charge-gate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4667 = POST / "4667-Y5-R2FR-Cmem-boundary-owner-or-nonHilbert-split-bound.md"
FORMAL_683 = FORMAL / "683-PPC4161-Cmem-boundary-owner-or-nonHilbert-split-bound.md"
CSV_4667_FINAL = SOURCE_DIR / "P8_Y5_R2FR_4667_FINAL_CMEM_UPDATE.csv"
CSV_4667_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4667_STATUS.csv"
CSV_4667_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4667_VALIDATION.csv"
CSV_4667_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4667_NEXT_TARGET.csv"

CSV_4505_GREEN = SOURCE_DIR / "P8_Y5_R2FR_4505_BODY_CHARGE_GREEN_FUNCTION_LAW.csv"
CSV_4506_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
CSV_4514_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv"
CSV_4595_MEM = SOURCE_DIR / "P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv"
CSV_4596_ENV = SOURCE_DIR / "P8_Y5_R2FR_4596_BODY_CHARGE_ENVELOPE_UPDATE.csv"
CSV_4596_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv"
CSV_4600_BODY = SOURCE_DIR / "P8_Y5_R2FR_4600_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv"
CSV_4601_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4601_BODY_CHARGE_SCORE_VECTOR.csv"
CSV_4625_TRACE = SOURCE_DIR / "P8_Y5_R2FR_4625_TRACE_CHARGE_DERIVATION_ROWS.csv"

CSV_4012_CHARGE = SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv"
CSV_4012_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4012_CHARGE_GLUE_FINITE_ROWS.csv"
CSV_4171_POISSON = SOURCE_DIR / "P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv"
CSV_4171_BRANCH = SOURCE_DIR / "P8_Y5_R2FR_4171_BRANCH_DECISION.csv"
CSV_4171_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4171_CLAIM_FIREWALL.csv"
CSV_4212_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4212_THEOREM_STATUS.csv"
CSV_4212_CURL = SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv"
CSV_4278_LEFT = SOURCE_DIR / "P8_Y5_R2FR_4278_LEFT_HAND_EH_NEWTON_DERIVATION.csv"
CSV_4278_GATE = SOURCE_DIR / "P8_Y5_R2FR_4278_LEFT_HAND_OPERATOR_GATE.csv"
CSV_4303_LOCK = SOURCE_DIR / "P8_Y5_R2FR_4303_VISIBLE_HILBERT_M_LOCK_SILENCE_THEOREM.csv"
CSV_4354_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4354_SOURCE_CHARGE_ROWS.csv"
CSV_4440_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_CHARGE_CLOSURE_OUTPUT.csv"
CSV_4465_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4465_SOURCE_CHARGE_DERIVATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4668_SOURCE_REGISTER.csv"
INSERTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_CMEM_TO_BODY_CHARGE_INSERTION.csv"
BRIDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_BODY_SOURCE_CHARGE_BRIDGE_GATE.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_REDUCED_BODY_CHARGE_RESIDUAL_VECTOR.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4668_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4668_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4668_00_4667_next", CSV_4667_NEXT, "4668-Y5-R2FR-Cmem-final-zero-to-body-charge-source-charge-gate.md", "4667 selected body/source charge bridge."),
        ("SRC4668_01_4667_final_zero", CSV_4667_FINAL, "CFU4667_4_final_zero", "final Cmem zero input."),
        ("SRC4668_02_4667_status", CSV_4667_STATUS, "C_MEM_FINAL_LIVE_ZERO_PRIVATE_BRANCH", "4667 status."),
        ("SRC4668_03_4667_validation", CSV_4667_VALIDATION, "VAL4667_OVERALL", "4667 validation."),
        ("SRC4668_04_doc4667", DOC_4667, "C_mem^final_live = 0", "4667 prose zero."),
        ("SRC4668_05_formal683", FORMAL_683, "body-charge/source-charge", "formal 4667 handoff."),
        ("SRC4668_06_4505_green", CSV_4505_GREEN, "BC4505_2_absolute_bound", "Green-function amplitude law."),
        ("SRC4668_07_4506_memory", CSV_4506_INPUT, "BCIN4506_0_memory_density", "memory body-charge input row."),
        ("SRC4668_08_4506_zero_switch", CSV_4506_INPUT, "BCIN4506_2_zero_switch", "body charge zero switch."),
        ("SRC4668_09_4514_amplitude", CSV_4514_BOUND, "BCB4514_3_amplitude", "body charge amplitude bound."),
        ("SRC4668_10_4514_nohair", CSV_4514_BOUND, "BCB4514_4_nohair", "body charge nohair criterion."),
        ("SRC4668_11_4595_density", CSV_4595_MEM, "MEM4595_0_density", "memory source density."),
        ("SRC4668_12_4595_amplitude", CSV_4595_MEM, "MEM4595_2_amplitude", "memory amplitude bound."),
        ("SRC4668_13_4595_poynting", CSV_4595_MEM, "MEM4595_3_poynting_guard", "Poynting channel guard."),
        ("SRC4668_14_4596_env", CSV_4596_ENV, "BU4596_1_memory_amplitude", "body-charge envelope before Cmem closure."),
        ("SRC4668_15_4596_coeff", CSV_4596_COEFF, "CO4596_6_Qboundary", "first body-charge coefficient rows."),
        ("SRC4668_16_4600_body", CSV_4600_BODY, "BU4600_1_memory", "final Cmem body-charge bound before 4667 zero."),
        ("SRC4668_17_4600_boundary", CSV_4600_BODY, "BU4600_3_boundary_separation", "C boundary vs Green boundary separation."),
        ("SRC4668_18_4601_Bmem", CSV_4601_VECTOR, "BCV4601_03", "B_mem_eff still missing."),
        ("SRC4668_19_4601_Cmem", CSV_4601_VECTOR, "BCV4601_04", "C_mem score vector row."),
        ("SRC4668_20_4601_Jmem", CSV_4601_VECTOR, "BCV4601_05", "J_mem score vector row."),
        ("SRC4668_21_4601_Qboundary", CSV_4601_VECTOR, "BCV4601_06", "Q_boundary score vector row."),
        ("SRC4668_22_4625_trace", CSV_4625_TRACE, "QDER4625_0_gauss_law", "trace charge is a Green/source flux."),
        ("SRC4668_23_4012_same_charge", CSV_4012_CHARGE, "CHG4012_4_same_charge_equality", "Pi_M/H_tau source equality theorem."),
        ("SRC4668_24_4012_vector", CSV_4012_CHARGE, "CHG4012_6_charge_glue_finite_vector", "charge glue finite vector."),
        ("SRC4668_25_4012_finite", CSV_4012_FINITE, "CGLUE4012_0_master", "finite charge glue residual vector."),
        ("SRC4668_26_4171_poisson", CSV_4171_POISSON, "PG4171_2_poisson", "private Poisson readout."),
        ("SRC4668_27_4171_branch", CSV_4171_BRANCH, "BD4171_0_Newton", "private Newton branch decision."),
        ("SRC4668_28_4171_firewall", CSV_4171_FIREWALL, "FW4171_3_no_numeric_G", "Newton constant firewall."),
        ("SRC4668_29_4212_status", CSV_4212_STATUS, "TH4212_2_full_MTS_integrability", "H_tau integrability remains conditional."),
        ("SRC4668_30_4212_curl", CSV_4212_CURL, "IC4212_9_total", "curl residual vector."),
        ("SRC4668_31_4278_newton", CSV_4278_LEFT, "LHD4278_4_Poisson_readout", "left-hand EH Newton readout."),
        ("SRC4668_32_4278_gate", CSV_4278_GATE, "OPG4278_1_effective_GR_residual_fork", "left-hand residual fork."),
        ("SRC4668_33_4303_lock", CSV_4303_LOCK, "VHS4303_5_verdict", "visible Hilbert source silence not parent signed."),
        ("SRC4668_34_4354_full_source", CSV_4354_SOURCE, "SC4354_9_full_source_charge", "source-charge branch contract."),
        ("SRC4668_35_4354_MHref", CSV_4354_SOURCE, "SC4354_7_MHref_positive", "M_H_ref positive gate."),
        ("SRC4668_36_4440_clean", CSV_4440_SOURCE, "SC4440_1_future_full_private_source_charge", "future full private source-charge branch."),
        ("SRC4668_37_4465_common_mode", CSV_4465_SOURCE, "DER4465_4_common_mode_warning", "universal WEP charge not local-GR enough."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def insertion_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("INS4668_0_import", "C_mem^final_live", "C_mem^final_live=0", "4667 strict private branch", "memory trace leakage is removed from the body-charge source density"),
        ("INS4668_1_density_before", "rho_mem_before", "rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live", "4595;4600", "body-charge density before insertion"),
        ("INS4668_2_density_after", "rho_mem_reduced", "rho_mem = B_mem_eff R_obs + J_mem_live", "INS4668_0", "trace-coupling term is gone; curvature/source-normalization and live current remain"),
        ("INS4668_3_charge_after", "Q_mem0_reduced", "Q_mem0 = 4*pi int_0^R dr r^2 [B_mem_eff R_obs + J_mem_live] sinh(r/lambda_mem)/(r/lambda_mem) + Q_boundary_mem", "4505;4506", "source charge is now a B/J/Q problem, not a Cmem problem"),
        ("INS4668_4_amplitude_after", "A_mem_reduced", "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)", "4514;4595;4600", "finite body-charge envelope after Cmem closure"),
        ("INS4668_5_zero_switch", "A_mem_zero_condition", "positive Z_mem,M2_mem plus B_mem_eff=J_mem_live=Q_boundary_mem=0", "4514 nohair;4506 zero switch", "exact body-charge zero route after Cmem closure"),
        ("INS4668_6_not_enough", "C_mem_zero_not_local_GR", "C_mem^final_live=0 does not set B_mem_eff, J_mem_live, Q_boundary_mem, Z_mem, M2_mem, Pi_M/H_tau or M_H_ref", "4601;4012;4354", "prevents the fake victory route"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "insertion_id": row[0],
            "object": row[1],
            "formula": row[2],
            "source_basis": row[3],
            "meaning": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def bridge_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BRG4668_0_body_charge", "memory body charge", "A_mem=0 iff reduced body charge and Green boundary charge vanish with positive operator", "INS4668_5", "BODY_CHARGE_ZERO_CONTRACT"),
        ("BRG4668_1_same_source_object", "body charge feeds same source charge", "Pi_M^C J_H = J_M_top + dB_zero and M_H[Pi_M^C J_H]=H_tau[S]-H_ref", "CHG4012_4; SC4354_2", "SOURCE_CHARGE_EQUALITY_CONTRACT"),
        ("BRG4668_2_positive_denominator", "M_H_ref", "M_H_ref=H_tau-H_ref is positive, same-frame, fixed and not orbital-GM-defined", "SC4354_7; FW4171_1", "DENOMINATOR_GATE"),
        ("BRG4668_3_integrability", "H_tau", "Hamiltonian one-form exactness: I_tau,S=0 for all allowed local variations", "TH4212_2; IC4212_9", "INTEGRABILITY_GATE"),
        ("BRG4668_4_Poisson", "Newton/Poisson readout", "G_00^lin=kappa_eff T_00 -> nabla^2 Phi_N=4*pi G_cal rho_H", "PG4171_2; LHD4278_4", "POISSON_PRIVATE_BRANCH"),
        ("BRG4668_5_universal_G", "calibrated G", "G_cal=c^4 kappa_eff/(8*pi); numerical G_N is empirical calibration unless parent scale is derived", "PG4171_1; FW4171_3", "NO_NUMERIC_G_CLAIM"),
        ("BRG4668_6_common_mode_guard", "WEP is not enough", "composition-universal charge can pass WEP while common-mode fifth-force/source-normalization survives", "DER4465_4", "COMMON_MODE_FIREWALL"),
        ("BRG4668_7_claim_gate", "local GR/Newton/PPN/R10", "requires INS4668_5 plus BRG4668_1..6 and residual EFT/PPN gates in the same branch", "4278;4012;4354", "NONCLAIM_GATE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": row[0],
            "object": row[1],
            "condition_or_formula": row[2],
            "source_basis": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RES4668_0_master", "epsilon_body_source_4668", "|A_mem| + epsilon_charge_4012 + ||E_res||_PPN", "combined body-charge/source-charge residual after Cmem closure", "4012;4278;4667"),
        ("RES4668_1_Bmem", "B_mem_eff", "||B_mem_eff||||R_obs|| weighted by Green kernel", "curvature/source-normalization source vector remains live", "BCV4601_03"),
        ("RES4668_2_Jmem", "J_mem_live", "||J_mem_live|| weighted by Green kernel", "direct/Poynting/non-Hilbert/current leakage not removed by Cmem zero", "BCV4601_05; MEM4595_3"),
        ("RES4668_3_Qboundary", "Q_boundary_mem", "||Q_boundary_mem||/(4*pi||Z_mem||)", "Green-function boundary charge separate from C_mem^boundary bookkeeping", "BU4600_3_boundary_separation"),
        ("RES4668_4_ZM", "Z_mem,M2_mem,lambda_mem", "positive Z_mem and M2_mem with lambda_mem=sqrt(Z_mem/M2_mem)", "operator denominator/range must be parent-signed or source-backed", "BCV4601_00;BCV4601_01;BCV4601_02"),
        ("RES4668_5_charge_glue", "epsilon_charge_4012", "|C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|", "same-source charge mismatch vector", "CGLUE4012_0_master"),
        ("RES4668_6_MHref", "M_H_ref", "positive same-frame denominator and no fitted/orbital GM substitution", "normalizer gate for every source-charge residual", "SC4354_7"),
        ("RES4668_7_source_row_contract", "first_body_charge_source_row", "system_id;Z_mem;M2_mem;lambda_mem;B_mem_eff;R_obs_profile;J_mem_live;Q_boundary_mem;M_H_ref;PiM_Htau_gate;G_cal_rule;units;source_path;valid_for_claim", "next source-backed row schema", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": row[0],
            "quantity": row[1],
            "formula_or_contract": row[2],
            "meaning": row[3],
            "source": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4668_0_Cmem_insert", "C_mem^final_live insertion", "PASS_REDUCES_BODY_CHARGE_ENVELOPE", "C_mem trace term is removed from rho_mem and A_mem on the strict private branch."),
        ("RUN4668_1_body_charge_zero", "A_mem=0", "FAIL_CLOSED_TO_BJQ_ZM_GATE", "B_mem_eff, J_mem_live, Q_boundary_mem and positive Z/M operator data remain required."),
        ("RUN4668_2_source_charge", "Pi_M/H_tau/source charge equality", "FAIL_CLOSED_TO_CHARGE_GLUE_GATE", "same-charge theorem is conditional; M_H_ref/integrability/reference/tau/boundary gates remain."),
        ("RUN4668_3_Newton_private", "Poisson/Newton route", "CONDITIONAL_PRIVATE_ROUTE_RETAINED", "4171/4278 private Poisson bridge remains usable only after source charge and residual EFT gates close."),
        ("RUN4668_4_public_claim", "local GR/Newton/PPN/R10 claim", "NONCLAIM_STILL_BLOCKED", "Cmem zero is a major input but not a full source-normalized Einstein/Newton theorem."),
        ("RUN4668_5_next", "next channel", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "object": row[1],
            "result": row[2],
            "detail": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4668_0_no_Cmem_magic", "Do not infer body-charge zero or local GR from C_mem^final_live=0 alone.", "ACTIVE"),
        ("CTRL4668_1_no_boundary_confusion", "C_mem^boundary bookkeeping is separate from Q_boundary_mem Green-function boundary charge.", "ACTIVE"),
        ("CTRL4668_2_no_poynting_erasure", "Poynting/radiative current is Hilbert-owned or explicit J/Q flux; never silently deleted.", "ACTIVE"),
        ("CTRL4668_3_no_orbital_GM_laundering", "Observed orbital GM, fitted acceleration or measured numerical G cannot define M_H_ref or source mass.", "ACTIVE"),
        ("CTRL4668_4_no_WEP_only_claim", "Composition-universal charge/WEP pass is not enough; common-mode source charge can survive.", "ACTIVE"),
        ("CTRL4668_5_no_EH_borrowing", "EH/Poisson identities are branch readouts only after MTS source charge and residual EFT gates close.", "ACTIVE"),
        ("CTRL4668_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "guard": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4668_0",
            "decision": DECISION,
            "summary": (
                "4668 inserts the 4667 result C_mem^final_live=0 into the memory body-charge Green-function law. "
                "The body-charge source density reduces from rho_mem=B_mem_eff R_obs+C_mem^final_live T+J_mem_live to rho_mem=B_mem_eff R_obs+J_mem_live, and the amplitude bound loses the trace-coupling term. "
                "That is a real simplification, but not a local-GR claim: exact A_mem=0 still requires B_mem_eff=0, J_mem_live=0, Q_boundary_mem=0 and positive Z_mem/M2_mem in the same branch, and the resulting source must also pass the Pi_M/H_tau/M_H_ref/source-charge equality and Poisson/G normalization gates. "
                "The next target is therefore the B/J/Q/ZM source-normalization row or zero theorem, not another pass over Cmem."
            ),
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "decision": DECISION,
            "Cmem_status": "C_MEM_FINAL_LIVE_ZERO_INSERTED",
            "body_charge_status": "REDUCED_TO_BMEM_JMEM_QBOUNDARY_ZM_GATE",
            "source_charge_status": "PI_M_HTAU_MHREF_CHARGE_GLUE_GATE_OPEN",
            "newton_status": "PRIVATE_POISSON_ROUTE_RETAINED_CONDITIONAL",
            "local_GR_status": "NONCLAIM_SOURCE_NORMALIZATION_REMAINS",
            "selected_next_channel": "B_mem_eff / J_mem_live / Q_boundary_mem / ZM source-normalization",
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After Cmem insertion, the remaining memory body-charge obstruction is exactly B_mem_eff, J_mem_live, Q_boundary_mem and positive Z/M operator normalization plus source-charge glue.",
            "derive_route": "try to prove B_mem_eff=J_mem_live=Q_boundary_mem=0 and Z_mem,M2_mem>0 on the same strict private branch, then pass it through Pi_M/H_tau/M_H_ref and Poisson/G normalization.",
            "fallback_route": "if any zero theorem fails, fill the first source-backed body-charge row with finite B/J/Q/ZM values, units, profiles, source paths, and no-cancellation guards.",
            "avoid": "reopening solved Cmem channels, claiming local GR from Cmem zero, borrowing orbital GM, or hiding current/boundary flux in calibrated G.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    insertions: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + insertions + bridge + residuals + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        INSERTION_CSV,
        BRIDGE_CSV,
        RESIDUAL_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
        VALIDATION_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    checks = [
        ("VAL4668_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4668_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4668_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4668_03_density_reduced", any(row["insertion_id"] == "INS4668_2_density_after" for row in insertions), "rho_mem reduced row present"),
        ("VAL4668_04_amplitude_reduced", any(row["insertion_id"] == "INS4668_4_amplitude_after" for row in insertions), "A_mem reduced bound present"),
        ("VAL4668_05_zero_switch", any(row["insertion_id"] == "INS4668_5_zero_switch" for row in insertions), "body-charge zero switch present"),
        ("VAL4668_06_source_bridge", any(row["bridge_id"] == "BRG4668_1_same_source_object" for row in bridge), "same source charge bridge present"),
        ("VAL4668_07_residual_master", any(row["residual_id"] == "RES4668_0_master" for row in residuals), "reduced residual master present"),
        ("VAL4668_08_no_Cmem_magic", any(row["control_id"] == "CTRL4668_0_no_Cmem_magic" for row in controls), "no-Cmem-magic control present"),
        ("VAL4668_09_nonclaim_runner", any(row["run_id"] == "RUN4668_4_public_claim" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local claim remains blocked"),
        ("VAL4668_10_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4668_11_next_BJQZM", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is B/J/Q/ZM source normalization"),
        ("VAL4668_12_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4668_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4668 Cmem final-zero insertion to body/source charge gate passed" if passed_all else "4668 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    insertions: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4668 - Cmem final zero to body-charge/source-charge gate

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4668 inserts the 4667 strict-branch result:

`C_mem^final_live = 0`

into the memory body-charge Green-function law.

Before insertion:

`rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live`.

After insertion:

`rho_mem = B_mem_eff R_obs + J_mem_live`.

So the exterior memory amplitude bound becomes:

`|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)`.

Therefore the body-charge route is now sharply reduced:

`A_mem = 0`

only if `B_mem_eff=0`, `J_mem_live=0`, `Q_boundary_mem=0`, and the memory operator has positive same-branch `Z_mem,M2_mem`.

That still does not prove local GR/Newton/PPN/R10. The zero body-charge must also be the same physical source charge:

`M_H[Pi_M^C J_H] = H_tau[S] - H_ref`,

with positive same-frame `M_H_ref`, integrable `H_tau`, fixed reference/tau/coframe, no orbital-GM laundering, and the private Poisson/Gauss normalization.

So the next actual target is not more Cmem. It is the `B_mem_eff / J_mem_live / Q_boundary_mem / Z_mem,M2_mem` source-normalization gate.

## Source Register

{table(sources)}

## Cmem To Body-Charge Insertion

{table(insertions)}

## Body / Source Charge Bridge Gate

{table(bridge)}

## Reduced Body-Charge Residual Vector

{table(residuals)}

## Runner Results

{table(runners)}

## Controls

{table(controls)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(nexts)}

## Validation

{table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4668 inserts the 4667 result C_mem^final_live=0 into the memory body-charge Green-function law. The body-charge density reduces from rho_mem=B_mem_eff R_obs+C_mem^final_live T+J_mem_live to rho_mem=B_mem_eff R_obs+J_mem_live, and the A_mem bound loses the trace-coupling term. Exact A_mem=0 still requires B_mem_eff=0, J_mem_live=0, Q_boundary_mem=0 and positive Z_mem/M2_mem in the same branch, followed by Pi_M/H_tau/M_H_ref/source-charge and Poisson/G normalization gates.",
        "Generated source register, Cmem-to-body-charge insertion, body/source charge bridge gate, reduced residual vector, runner, controls, decision, status, next target and validation.",
        "Cmem_final_zero_inserted_body_charge_reduced_to_BJQ_ZM_source_charge_gate_nonclaim",
        NEXT_TARGET,
        "Claiming body-charge zero from Cmem zero alone, confusing C_mem^boundary with Q_boundary_mem, erasing Poynting/radiative J_mem, borrowing orbital GM or measured numerical G, or treating WEP/common-mode charge as a local-GR source-normalization proof.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until B_mem_eff, J_mem_live, Q_boundary_mem, Z/M, Pi_M/H_tau, M_H_ref and residual EFT/PPN gates are same-branch derived or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4668 inserts `C_mem^final_live=0` into the memory body-charge law. The trace-source part is removed, so `rho_mem` reduces to `B_mem_eff R_obs + J_mem_live` and the `A_mem` bound reduces to the `B/J/Q_boundary/ZM` gate. This is a genuine simplification, but not a local-GR claim: the remaining route must prove or source-fill `B_mem_eff`, `J_mem_live`, `Q_boundary_mem`, positive `Z_mem,M2_mem`, `Pi_M/H_tau`, `M_H_ref`, and Poisson/G normalization in the same branch.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4668` inserts the closed `C_mem` vector into the body-charge/source-charge bridge and reduces the next target to `B_mem_eff / J_mem_live / Q_boundary_mem / Z_mem,M2_mem` source normalization. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    insertions = insertion_rows(timestamp)
    bridge = bridge_rows(timestamp)
    residuals = residual_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, insertions, bridge, residuals, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INSERTION_CSV, insertions)
    write_csv(BRIDGE_CSV, bridge)
    write_csv(RESIDUAL_CSV, residuals)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, insertions, bridge, residuals, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4668 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
