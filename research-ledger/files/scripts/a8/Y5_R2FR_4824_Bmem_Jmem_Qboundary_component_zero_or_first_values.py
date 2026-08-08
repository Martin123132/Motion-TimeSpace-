from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4824"
CLAIM_ID = "L-666"
MARKER = "PPC4161_BMEM_JMEM_QBOUNDARY_COMPONENT_ZERO_OR_FIRST_VALUES_4824"
DECISION = "BJQ_COMPONENT_VECTOR_RUNNER_STAGED_FIRST_VALUES_NONCLAIM"
NEXT_TARGET = "4825-Y5-R2FR-BY5-source-functor-zero-or-first-source-normalization-row.md"

DOC_PATH = POST / "4824-Y5-R2FR-Bmem-Jmem-Qboundary-component-zero-or-first-values.md"
FORMAL_PATH = FORMAL / "840-PPC4161-Bmem-Jmem-Qboundary-component-zero-or-first-values.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "Bmem_Jmem_Qboundary_component_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4824_SOURCE_REGISTER.csv"
COMPONENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4824_BJQ_COMPONENT_ZERO_AUDIT.csv"
VALUE_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4824_BJQ_FIRST_VALUE_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4824_BJQ_COMPONENT_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4824_BJQ_COMPONENT_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4824_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4824_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4824_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4824_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4824_VALIDATION.csv"

PATHS = {
    "resume": RESUME_PATH,
    "4823_doc": POST / "4823-Y5-R2FR-rho-mem-Qboundary-zero-or-first-source-density-row.md",
    "4823_output": SOURCE_DIR / "P8_Y5_R2FR_4823_RHOMEM_QBOUNDARY_RUNNER_OUTPUT.csv",
    "4514_Bmem": SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv",
    "4514_bound": SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv",
    "4515_theorem": SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv",
    "4515_source": SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv",
    "4596_Jmem": SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv",
    "4596_coeff": SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv",
    "4595_bound": SOURCE_DIR / "P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv",
    "4601_score": SOURCE_DIR / "P8_Y5_R2FR_4601_BODY_CHARGE_SCORE_VECTOR.csv",
    "4669_doc": POST / "4669-Y5-R2FR-Bmem-Jmem-Qboundary-ZM-source-normalization-zero-or-first-body-charge-row.md",
    "4669_matrix": SOURCE_DIR / "P8_Y5_R2FR_4669_BJQ_ZM_ZERO_ATTEMPT_MATRIX.csv",
    "4669_contract": SOURCE_DIR / "P8_Y5_R2FR_4669_FIRST_BODY_CHARGE_SOURCE_ROW_CONTRACT.csv",
    "4669_results": SOURCE_DIR / "P8_Y5_R2FR_4669_RUNNER_RESULTS.csv",
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
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4824_00_resume", PATHS["resume"], "4824-Y5-R2FR-Bmem-Jmem-Qboundary", "4823 selected this target."),
        ("SRC4824_01_4823_doc", PATHS["4823_doc"], "B_mem_eff", "4823 names B/J/Q live source values."),
        ("SRC4824_02_4823_output", PATHS["4823_output"], "RUN4823_3_live_source_bound_missing", "4823 live source row remains blocked."),
        ("SRC4824_03_4514_Bmem", PATHS["4514_Bmem"], "BMV4514_6_combined", "B_mem_eff component vector."),
        ("SRC4824_04_4514_bound", PATHS["4514_bound"], "BCB4514_3_amplitude", "body-charge insertion bound."),
        ("SRC4824_05_4515_theorem", PATHS["4515_theorem"], "SFT4515_2_Y5_measured_GM", "source-functor/Y5 zero route."),
        ("SRC4824_06_4515_source", PATHS["4515_source"], "SCV4515_3_Qboundary_mem", "Qboundary source route."),
        ("SRC4824_07_4596_Jmem", PATHS["4596_Jmem"], "J4596_5_live_total", "J_mem live vector."),
        ("SRC4824_08_4596_coeff", PATHS["4596_coeff"], "CO4596_6_Qboundary", "first body-charge coefficient rows."),
        ("SRC4824_09_4595_bound", PATHS["4595_bound"], "MEM4595_2_amplitude", "memory body-charge amplitude law."),
        ("SRC4824_10_4601_score", PATHS["4601_score"], "BCV4601_03", "body-charge score vector."),
        ("SRC4824_11_4669_doc", PATHS["4669_doc"], "rho_mem = B_mem_eff R_obs + J_mem_live", "4669 reduced B/J/Q gate."),
        ("SRC4824_12_4669_matrix", PATHS["4669_matrix"], "ZAT4669_11_Jmem_live", "4669 zero attempt matrix."),
        ("SRC4824_13_4669_contract", PATHS["4669_contract"], "FBC4669_5_Q", "first source row contract."),
        ("SRC4824_14_4669_results", PATHS["4669_results"], "RUN4669_3_Jmem", "4669 runner handoff."),
        ("SRC4824_15_runner", PATHS["runner"], "def evaluate_row", "4824 executable runner."),
    ]


def build_source_register(timestamp: str) -> list[dict[str, Any]]:
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


def component_audit(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "BJQ4824_0_B826",
            "piece": "B_826",
            "zero_route": "branch extremum/source-root signs R_m=0 with X_B fixed and m_L parent-owned",
            "current_result": "CONDITIONAL_UNSIGNED",
            "finite_input": "B826_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BJQ4824_1_BWeyl",
            "piece": "B_Weyl_vec",
            "zero_route": "all Weyl/metric-response components zero in the same branch",
            "current_result": "VECTOR_STAGED_NONCLAIM",
            "finite_input": "BWeyl_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BJQ4824_2_BY5",
            "piece": "B_Y5_trace",
            "zero_route": "single q-basic Hilbert-current source functor with no measured-G/source-normalization hair",
            "current_result": "LIVE_HIGHEST_PRIORITY_SOURCE_TAIL",
            "finite_input": "BY5_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BJQ4824_3_BY6",
            "piece": "B_Y6_trace",
            "zero_route": "extra stress topological/invisible/EH-owned metric response/exchange-even",
            "current_result": "LIVE_EXTRA_STRESS_TAIL",
            "finite_input": "BY6_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BJQ4824_4_Bboundary_readout",
            "piece": "B_src_boundary+B_src_readout",
            "zero_route": "source-functional boundary/reference and readout shifts have no linear memory response",
            "current_result": "CONDITIONAL_UNSIGNED",
            "finite_input": "Bsrc_boundary_abs and Bsrc_readout_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BJQ4824_5_Jmem",
            "piece": "J_source_kernel+J_EM_open+J_nonHilbert+J_dyn+J_boundary_readout",
            "zero_route": "strict source kernel plus no-flux EM collar, no non-Hilbert retained current, stationary exchange, boundary/readout neutrality",
            "current_result": "LIVE_CURRENT_NOT_CLOSED",
            "finite_input": "five J absolute component values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BJQ4824_6_Qboundary",
            "piece": "Q_boundary_mem",
            "zero_route": "fixed no-flux/topological boundary class with no linked source-normalization boundary charge",
            "current_result": "BOUNDARY_ZERO_UNSIGNED",
            "finite_input": "Q_boundary_mem_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def value_contract(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "BVC4824_0_zero",
            "quantity": "B_mem_eff=J_mem_live=Q_boundary_mem=0",
            "formula": "all B/J/Q components zero in the same branch, with absolute no-cancellation guard",
            "required_inputs": "component zero certificates, same branch, parent object language, units, source paths",
            "status": "conditional_only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BVC4824_1_Bmem",
            "quantity": "B_mem_eff_abs",
            "formula": "|B826|+|BWeyl|+|BY5|+|BY6|+|Bsrc_boundary|+|Bsrc_readout|",
            "required_inputs": "six B component values or zeros",
            "status": "runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BVC4824_2_Jmem",
            "quantity": "J_mem_live_abs",
            "formula": "|J_source_kernel|+|J_EM_open|+|J_nonHilbert|+|J_dyn_exchange|+|J_boundary_readout|",
            "required_inputs": "five J current values or zeros",
            "status": "runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BVC4824_3_Qboundary",
            "quantity": "Q_boundary_mem_abs",
            "formula": "absolute Green-function boundary charge, separate from closed Cmem boundary bookkeeping",
            "required_inputs": "zero-flux/topological theorem or finite boundary integral",
            "status": "runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BVC4824_4_rho_feed",
            "quantity": "rho_mem_reduced_abs",
            "formula": "B_mem_eff_abs R_obs_norm + Cmem_final_abs T_obs_norm + J_mem_live_abs",
            "required_inputs": "BVC4824_1, BVC4824_2, R/T profiles, and Cmem_final zero/value",
            "status": "feed_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def numeric_components(row_id: str, route_type: str, timestamp: str) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": "component arithmetic smoke",
        "source_path": str(PATHS["4669_contract"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": True,
        "no_cancellation_guard": True,
        "B826_abs": 0.01,
        "BWeyl_abs": 0.02,
        "BY5_abs": 0.03,
        "BY6_abs": 0.04,
        "Bsrc_boundary_abs": 0.05,
        "Bsrc_readout_abs": 0.06,
        "J_source_kernel_abs": 0.0,
        "J_EM_open_abs": 0.07,
        "J_nonHilbert_abs": 0.08,
        "J_dyn_exchange_abs": 0.09,
        "J_boundary_readout_abs": 0.10,
        "Q_boundary_mem_abs": 0.11,
        "timestamp_utc": timestamp,
    }


def runner_input(timestamp: str) -> list[dict[str, Any]]:
    zero_base = {
        "route_type": "component_zero",
        "source_path": str(PATHS["4669_matrix"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": False,
        "parent_object_language_signed": False,
        "no_cancellation_guard": False,
        "B826_zero": False,
        "BWeyl_zero": False,
        "BY5_zero": False,
        "BY6_zero": False,
        "Bsrc_boundary_zero": False,
        "Bsrc_readout_zero": False,
        "J_source_kernel_zero": False,
        "J_EM_open_zero": False,
        "J_nonHilbert_zero": False,
        "J_dyn_exchange_zero": False,
        "J_boundary_readout_zero": False,
        "Q_boundary_mem_zero": False,
        "boundary_reference_neutral": False,
        "no_incoming_flux": False,
    }
    missing_bound = {
        "route_type": "component_bound",
        "source_path": str(PATHS["4669_contract"]),
        "source_signed": False,
        "units_signed": False,
        "same_branch_signed": False,
        "no_cancellation_guard": False,
        "B826_abs": "MISSING_COMPONENT",
        "BWeyl_abs": "MISSING_COMPONENT",
        "BY5_abs": "MISSING_COMPONENT",
        "BY6_abs": "MISSING_COMPONENT",
        "Bsrc_boundary_abs": "MISSING_COMPONENT",
        "Bsrc_readout_abs": "MISSING_COMPONENT",
        "J_source_kernel_abs": "MISSING_COMPONENT",
        "J_EM_open_abs": "MISSING_COMPONENT",
        "J_nonHilbert_abs": "MISSING_COMPONENT",
        "J_dyn_exchange_abs": "MISSING_COMPONENT",
        "J_boundary_readout_abs": "MISSING_COMPONENT",
        "Q_boundary_mem_abs": "MISSING_BOUNDARY_VALUE",
    }
    rho_czero = numeric_components("RUN4824_5_rho_feed_Cmem_zero_smoke_pass", "rho_feed", timestamp)
    rho_czero.update({"R_obs_norm": 2.0, "Cmem_final_abs": 0.0, "T_obs_norm": 3.0})
    rho_cfinite = numeric_components("RUN4824_6_rho_feed_Cmem_finite_smoke_pass", "rho_feed", timestamp)
    rho_cfinite.update({"R_obs_norm": 2.0, "Cmem_final_abs": 0.05, "T_obs_norm": 3.0})
    forbidden_cancel = numeric_components("RUN4824_7_forbidden_cancellation_bound", "component_bound", timestamp)
    forbidden_cancel.update({"notes": "CANCEL_UNKNOWN_COMPONENTS control"})
    forbidden_g = numeric_components("RUN4824_8_forbidden_measured_G_absorption", "rho_feed", timestamp)
    forbidden_g.update({"R_obs_norm": 2.0, "Cmem_final_abs": 0.0, "T_obs_norm": 3.0, "notes": "MEASURED_G_ABSORPTION control"})
    return [
        {
            "row_id": "RUN4824_0_live_component_zero_missing",
            "route": "live B/J/Q exact zero audit",
            **zero_base,
            "notes": "live component zero route lacks same-branch parent signatures",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4824_1_conditional_component_zero_pass",
            "route": "conditional total B/J/Q zero theorem",
            **zero_base,
            "same_branch_signed": True,
            "parent_object_language_signed": True,
            "no_cancellation_guard": True,
            "B826_zero": True,
            "BWeyl_zero": True,
            "BY5_zero": True,
            "BY6_zero": True,
            "Bsrc_boundary_zero": True,
            "Bsrc_readout_zero": True,
            "J_source_kernel_zero": True,
            "J_EM_open_zero": True,
            "J_nonHilbert_zero": True,
            "J_dyn_exchange_zero": True,
            "J_boundary_readout_zero": True,
            "Q_boundary_mem_zero": True,
            "boundary_reference_neutral": True,
            "no_incoming_flux": True,
            "notes": "control only: every component is signed zero",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4824_2_forbidden_zero_by_cancellation",
            "route": "forbidden cancellation zero",
            **zero_base,
            "same_branch_signed": True,
            "parent_object_language_signed": True,
            "no_cancellation_guard": True,
            "B826_zero": True,
            "BWeyl_zero": True,
            "BY5_zero": True,
            "BY6_zero": True,
            "Bsrc_boundary_zero": True,
            "Bsrc_readout_zero": True,
            "J_source_kernel_zero": True,
            "J_EM_open_zero": True,
            "J_nonHilbert_zero": True,
            "J_dyn_exchange_zero": True,
            "J_boundary_readout_zero": True,
            "Q_boundary_mem_zero": True,
            "boundary_reference_neutral": True,
            "no_incoming_flux": True,
            "notes": "CANCEL_UNKNOWN_COMPONENTS shortcut is forbidden",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4824_3_live_component_bound_missing",
            "route": "live first B/J/Q value row",
            **missing_bound,
            "notes": "live finite component row still lacks parent/source values",
            "timestamp_utc": timestamp,
        },
        numeric_components("RUN4824_4_component_bound_smoke_pass", "component_bound", timestamp),
        rho_czero,
        rho_cfinite,
        forbidden_cancel,
        forbidden_g,
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "The reduced body-charge source is now an executable B/J/Q component vector. Exact zero remains unsigned; finite component rows can feed rho_mem without cancellation or fitted-G absorption.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4824_0_total_zero",
            "claim": "B_mem_eff=J_mem_live=Q_boundary_mem=0 kills the reduced body-charge source.",
            "required": "all B/J/Q components zero in the same parent branch",
            "current_status": "blocked_unsigned",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4824_1_first_values",
            "claim": "finite B/J/Q values can feed rho_mem and q_boundary_mem.",
            "required": "all component values numeric, sourced, unit-signed, same-branch, absolute-sum guarded",
            "current_status": "runner_ready_live_values_missing",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4824_2_source_normalization",
            "claim": "measured G/GM/source calibration cannot define B_Y5 or hide source tails.",
            "required": "parent source-functor descent or independent finite source-normalization row",
            "current_status": "guard_active_BY5_selected_next",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PRIVATE_NONCLAIM",
            "result": "B/J/Q component vector advanced to executable zero-or-first-value runner",
            "missing": "B826,BWeyl,BY5,BY6,Bsrc_boundary,Bsrc_readout,J_EM,J_nonHilbert,Jdyn,Jboundary,Qboundary source values or parent-zero certificates",
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4514 marks B_Y5_trace as the live highest-priority source-normalization tail; it is closest to Newton/Poisson/source calibration.",
            "first_question": "Can the single q-basic Hilbert-current source functor kill B_Y5 without measured-G absorption, or must BY5_abs become a finite source-normalization row?",
            "timestamp_utc": timestamp,
        }
    ]


def append_claim(timestamp: str) -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "Bmem_Jmem_Qboundary_component_zero_or_first_values",
            "current_evidence": "4824 converts B_mem_eff, J_mem_live, and Q_boundary_mem into an executable component zero-or-first-value runner.",
            "status": "BJQ_component_runner_private_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "B_Y5/source-normalization, retained J currents, and Qboundary remain unsigned/missing",
            "sector": "local_gr_EM_source_coupling",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "risk": "smoke rows pass but live component values are not source-backed",
            "title": "Bmem/Jmem/Qboundary component zero or first values",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def append_section(path: Path, heading: str, body: str) -> None:
    text = read_text(path)
    if MARKER in text:
        return
    suffix = "\n\n" if text and not text.endswith("\n") else "\n"
    write_text(path, text + suffix + f"## {heading}\n\n{body}\n")


def build_doc(timestamp: str, source_rows: list[dict[str, Any]], audit_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> str:
    return f"""# 4824 - Bmem/Jmem/Qboundary Component Zero Or First Values

Generated UTC: `{timestamp}`

Marker: `{MARKER}`

## Result

4824 pushes the reduced body-charge source down to the actual component vector:

```text
B_mem_eff = |B826| + |BWeyl| + |BY5| + |BY6| + |Bsrc_boundary| + |Bsrc_readout|
J_mem_live = |J_source_kernel| + |J_EM_open| + |J_nonHilbert| + |J_dyn_exchange| + |J_boundary_readout|
rho_mem_reduced = B_mem_eff R_obs + Cmem_final T_obs + J_mem_live
q_boundary_mem = Q_boundary_mem
```

The exact zero route is still conditional: every listed component must be zero in the same parent branch. No cancellation, fitted `G`, measured `GM`, or post-fit source normalization is allowed.

The useful progress is that the first-value route is executable. Smoke rows now calculate absolute `B_mem_eff`, `J_mem_live`, `Q_boundary_mem`, and the reduced `rho_mem` feed while forbidden cancellation and measured-G absorption fail closed.

## Source Register

{md_table(source_rows, ["source_id", "exists", "needle_found", "role"])}

## Component Audit

{md_table(audit_rows, ["component_id", "piece", "current_result", "finite_input"])}

## First Value Contract

{md_table(contract_rows, ["contract_id", "quantity", "formula", "status"])}

## Runner Output

{md_table(output_rows, ["row_id", "runner_status", "B_mem_eff_abs", "J_mem_live_abs", "Q_boundary_mem_abs", "rho_mem_reduced_abs", "missing_for_claim"])}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`
"""


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    statuses = {row["row_id"]: row["runner_status"] for row in output_rows}
    checks = [
        ("VAL4824_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL4824_01_needles_found", all(row["needle_found"] for row in source_rows), "all source needles found"),
        ("VAL4824_02_live_zero_blocked", statuses.get("RUN4824_0_live_component_zero_missing") == "BLOCKED_BJQ_COMPONENT_ZERO_CLAUSES", "live B/J/Q zero route remains blocked"),
        ("VAL4824_03_conditional_zero_pass", statuses.get("RUN4824_1_conditional_component_zero_pass") == "BJQ_COMPONENT_ZERO_PASS_NONCLAIM", "conditional B/J/Q zero control passes"),
        ("VAL4824_04_forbidden_zero_cancel_fails", statuses.get("RUN4824_2_forbidden_zero_by_cancellation") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "cancellation zero shortcut fails"),
        ("VAL4824_05_live_bound_blocked", statuses.get("RUN4824_3_live_component_bound_missing") == "BLOCKED_BJQ_COMPONENT_INPUTS", "live component-bound row blocked"),
        ("VAL4824_06_component_smoke_pass", statuses.get("RUN4824_4_component_bound_smoke_pass") == "BJQ_COMPONENT_BOUND_PASS_NONCLAIM", "component bound smoke passes"),
        ("VAL4824_07_rho_cmem_zero_pass", statuses.get("RUN4824_5_rho_feed_Cmem_zero_smoke_pass") == "BJQ_RHO_FEED_PASS_NONCLAIM", "rho feed with Cmem zero passes"),
        ("VAL4824_08_rho_cmem_finite_pass", statuses.get("RUN4824_6_rho_feed_Cmem_finite_smoke_pass") == "BJQ_RHO_FEED_PASS_NONCLAIM", "rho feed with finite Cmem passes"),
        ("VAL4824_09_forbidden_component_cancel_fails", statuses.get("RUN4824_7_forbidden_cancellation_bound") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "component cancellation route fails"),
        ("VAL4824_10_forbidden_measured_G_fails", statuses.get("RUN4824_8_forbidden_measured_G_absorption") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "measured-G absorption route fails"),
        ("VAL4824_11_no_claim_allowed", all(str(row.get("claim_allowed", "")).lower() == "false" for row in output_rows), "runner never allows a claim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]


def main() -> int:
    timestamp = now()
    source_rows = build_source_register(timestamp)
    audit_rows = component_audit(timestamp)
    contract_rows = value_contract(timestamp)
    input_rows = runner_input(timestamp)
    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(COMPONENT_AUDIT, audit_rows)
    write_csv(VALUE_CONTRACT, contract_rows)
    write_csv(RUNNER_INPUT, input_rows)

    py_compile.compile(str(RUNNER), doraise=True)
    subprocess.run(["python", str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    output_rows = read_csv(RUNNER_OUTPUT)

    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp))
    write_csv(NEXT_TARGET_CSV, next_target_rows(timestamp))
    validation = validation_rows(timestamp, source_rows, output_rows)
    write_csv(VALIDATION_CSV, validation)

    doc = build_doc(timestamp, source_rows, audit_rows, contract_rows, output_rows)
    write_text(DOC_PATH, doc)
    write_text(FORMAL_PATH, doc)
    append_claim(timestamp)
    append_section(
        SPINE_PATH,
        "PPC4161 4824 B/J/Q component runner",
        f"`{MARKER}`. The reduced source-normalization obstruction is now an absolute component vector for `B_mem_eff`, `J_mem_live`, and `Q_boundary_mem`; exact zero remains unsigned and finite component rows are runner-ready. Decision: `{DECISION}`.",
    )
    append_section(
        PACKET_PATH,
        "4824 B/J/Q component runner",
        f"`{MARKER}` turns the body-charge obstruction into component values with no cancellation and no measured-G absorption. Live claims remain blocked; smoke rows prove B/J/Q arithmetic and rho feed. Next: `{NEXT_TARGET}`.",
    )
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4824-Y5-R2FR-Bmem-Jmem-Qboundary-component-zero-or-first-values.md`
Marker: `{MARKER}`

## Where we are

4824 made the reduced B/J/Q source-normalization obstruction executable:

```text
B_mem_eff = |B826|+|BWeyl|+|BY5|+|BY6|+|Bsrc_boundary|+|Bsrc_readout|
J_mem_live = |J_source_kernel|+|J_EM_open|+|J_nonHilbert|+|J_dyn_exchange|+|J_boundary_readout|
rho_mem_reduced = B_mem_eff R_obs + Cmem_final T_obs + J_mem_live
q_boundary_mem = Q_boundary_mem
```

## Live blockers

- Exact B/J/Q zero is not parent-signed.
- `B_Y5_trace` is the highest-priority source-normalization tail.
- Retained non-Hilbert/dynamic/boundary-readout J currents remain live until theorem-zero or finite values exist.
- `Q_boundary_mem` remains separate from closed Cmem boundary bookkeeping.

## Next target

`{NEXT_TARGET}`
""",
    )

    py_compile.compile(str(Path(__file__)), doraise=True)
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        print(f"4824 generated with {len(failed)} validation failures")
        return 1
    print(f"4824 generated: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
