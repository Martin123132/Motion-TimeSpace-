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

CHECKPOINT = "4823"
CLAIM_ID = "L-665"
MARKER = "PPC4161_RHOMEM_QBOUNDARY_ZERO_OR_FIRST_SOURCE_DENSITY_ROW_4823"
DECISION = "RHOMEM_QBOUNDARY_CHANNEL_RUNNER_STAGED_FINITE_SOURCE_ROUTE_NONCLAIM"
NEXT_TARGET = "4824-Y5-R2FR-Bmem-Jmem-Qboundary-component-zero-or-first-values.md"

DOC_PATH = POST / "4823-Y5-R2FR-rho-mem-Qboundary-zero-or-first-source-density-row.md"
FORMAL_PATH = FORMAL / "839-PPC4161-rho-mem-Qboundary-zero-or-first-source-density-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "rho_mem_Qboundary_source_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4823_SOURCE_REGISTER.csv"
CHANNEL_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4823_RHOMEM_CHANNEL_ZERO_AUDIT.csv"
SOURCE_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4823_SOURCE_DENSITY_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4823_RHOMEM_QBOUNDARY_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4823_RHOMEM_QBOUNDARY_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4823_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4823_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4823_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4823_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4823_VALIDATION.csv"

PATHS = {
    "resume": RESUME_PATH,
    "4822_doc": POST / "4822-Y5-R2FR-kappa-memF2-zero-certificate-or-Zmem-M2mem-source-row.md",
    "4822_output": SOURCE_DIR / "P8_Y5_R2FR_4822_KAPPA_ZMEM_M2MEM_RUNNER_OUTPUT.csv",
    "4621_rho_audit": SOURCE_DIR / "P8_Y5_R2FR_4621_RHOMEM_SOURCE_CHANNEL_AUDIT.csv",
    "4621_identity": SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv",
    "4622_decomp": SOURCE_DIR / "P8_Y5_R2FR_4622_RHOMEM_CHANNEL_DECOMPOSITION.csv",
    "4622_poynting": SOURCE_DIR / "P8_Y5_R2FR_4622_EM_POYNTING_ZERO_AND_BOUND_RULES.csv",
    "4622_couplings": SOURCE_DIR / "P8_Y5_R2FR_4622_COUPLING_COEFFICIENT_ROWS_NONCLAIM.csv",
    "4622_bound_feed": SOURCE_DIR / "P8_Y5_R2FR_4622_BOUND_FEED_ROWS.csv",
    "4669_doc": POST / "4669-Y5-R2FR-Bmem-Jmem-Qboundary-ZM-source-normalization-zero-or-first-body-charge-row.md",
    "4669_matrix": SOURCE_DIR / "P8_Y5_R2FR_4669_BJQ_ZM_ZERO_ATTEMPT_MATRIX.csv",
    "4669_contract": SOURCE_DIR / "P8_Y5_R2FR_4669_FIRST_BODY_CHARGE_SOURCE_ROW_CONTRACT.csv",
    "4514_Bmem": SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv",
    "4515_source": SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv",
    "4596_Jmem": SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv",
    "4596_coeff": SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv",
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
        ("SRC4823_00_resume", PATHS["resume"], "4823-Y5-R2FR-rho-mem-Qboundary", "4822 selected this target."),
        ("SRC4823_01_4822_doc", PATHS["4822_doc"], "source or kill `rho_mem` and `q_boundary_mem`", "4822 handoff."),
        ("SRC4823_02_4822_output", PATHS["4822_output"], "RUN4822_6_live_finite_chain_missing", "4822 live finite chain missing source terms."),
        ("SRC4823_03_4621_rho", PATHS["4621_rho_audit"], "RHO4621_3_Poynting_flux", "4621 source-channel audit."),
        ("SRC4823_04_4621_identity", PATHS["4621_identity"], "MPI4621_2_nohair_zero", "positive-operator no-hair gate."),
        ("SRC4823_05_4622_decomp", PATHS["4622_decomp"], "RDEC4622_5_hidden", "rho_mem channel decomposition."),
        ("SRC4823_06_4622_poynting", PATHS["4622_poynting"], "EMP4622_1_poynting_volume_to_boundary", "Poynting volume/boundary guard."),
        ("SRC4823_07_4622_couplings", PATHS["4622_couplings"], "COUP4622_0_beta_R", "coupling coefficient rows."),
        ("SRC4823_08_4622_bound_feed", PATHS["4622_bound_feed"], "BF4622_0_rho_norm", "rho and boundary norm formulas."),
        ("SRC4823_09_4669_doc", PATHS["4669_doc"], "rho_mem = B_mem_eff R_obs + J_mem_live", "4669 reduced body-charge gate."),
        ("SRC4823_10_4669_matrix", PATHS["4669_matrix"], "ZAT4669_13_total", "4669 zero attempt matrix."),
        ("SRC4823_11_4669_contract", PATHS["4669_contract"], "FBC4669_5_Q", "4669 first body-charge source row contract."),
        ("SRC4823_12_4514_Bmem", PATHS["4514_Bmem"], "BMV4514_6_combined", "B_mem_eff component vector."),
        ("SRC4823_13_4515_source", PATHS["4515_source"], "SCV4515_4_total_density_source", "rho_mem total density source row."),
        ("SRC4823_14_4596_Jmem", PATHS["4596_Jmem"], "J4596_5_live_total", "J_mem live current vector."),
        ("SRC4823_15_4596_coeff", PATHS["4596_coeff"], "CO4596_6_Qboundary", "Q_boundary first coefficient row."),
        ("SRC4823_16_runner", PATHS["runner"], "def evaluate_row", "4823 executable runner."),
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


def channel_audit(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "channel_id": "RZ4823_0_curvature",
            "piece": "beta_R R_obs / B_mem_eff",
            "zero_route": "parent beta_R=0, parent source-root/branch extremum, or source-free local exterior without importing GR as proof",
            "current_result": "CONDITIONAL_UNSIGNED",
            "finite_input": "beta_R_abs and R_obs_norm",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "channel_id": "RZ4823_1_matter_trace",
            "piece": "beta_T T_obs / C_mem T",
            "zero_route": "strict exterior vacuum or q-basic matter descent with no explicit memory dependence",
            "current_result": "PRIVATE_PARTIAL_ZERO_NOT_TOTAL",
            "finite_input": "beta_T_abs and T_obs_norm",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "channel_id": "RZ4823_2_em_invariant",
            "piece": "beta_F F_Q^2 + beta_G F_Q starF_Q",
            "zero_route": "typed coefficient-domain exclusion, parity/selection rule, or null radiation invariants; static EM is not zero",
            "current_result": "LIVE_FOR_STATIC_EM",
            "finite_input": "beta_F_abs, beta_G_abs, F2_norm, FstarF_norm",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "channel_id": "RZ4823_3_poynting",
            "piece": "beta_S div S_EM or beta_S S_EM.n boundary flux",
            "zero_route": "stationary source-free collar or no-radiative/no-current flux boundary condition",
            "current_result": "RUNNER_GUARDED_NO_DOUBLE_COUNT",
            "finite_input": "choose one of divS_norm or S_boundary_flux_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "channel_id": "RZ4823_4_wave_stress",
            "piece": "beta_gw rho_gw_eff",
            "zero_route": "beta_gw=0, local wave envelope absent, or parent projection removes averaged wave stress",
            "current_result": "LIVE_UNLESS_SOURCE_ABSENT",
            "finite_input": "beta_gw_abs and rho_gw_eff_norm",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "channel_id": "RZ4823_5_hidden_current",
            "piece": "J_hidden / J_mem_live",
            "zero_route": "no retained non-Hilbert/current channel plus stationary exchange and boundary/readout neutrality",
            "current_result": "LIVE_CURRENT_NOT_CLOSED",
            "finite_input": "J_hidden_norm or component current vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "channel_id": "RZ4823_6_boundary",
            "piece": "Q_boundary_mem plus any converted Poynting flux",
            "zero_route": "fixed no-flux/topological boundary class with no linked source-normalization boundary charge",
            "current_result": "BOUNDARY_ZERO_UNSIGNED",
            "finite_input": "Q_boundary_mem_abs and optional beta_S_abs*S_boundary_flux_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_contract(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "RSC4823_0_zero",
            "quantity": "rho_mem=q_boundary_mem=0",
            "formula": "all rho channels and boundary channels zero in the same branch",
            "required_inputs": "six source zero clauses, three boundary zero clauses, source/units/same-branch/object-language signed",
            "status": "conditional_only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "RSC4823_1_rho_norm",
            "quantity": "rho_mem_norm_abs",
            "formula": "sum |beta_i| |source_i| + |J_hidden|, with Poynting assigned to volume or boundary but not both",
            "required_inputs": "beta/source norms and Poynting mode",
            "status": "runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "RSC4823_2_q_boundary",
            "quantity": "q_boundary_mem_norm_abs",
            "formula": "Q_boundary_mem_abs plus converted beta_S_abs S_boundary_flux_abs when Poynting is boundary-mode",
            "required_inputs": "Q_boundary value/zero and boundary flux value/zero",
            "status": "runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "RSC4823_3_feed_4822",
            "quantity": "Delta_v_m_mem_bound_abs",
            "formula": "C_omega (rho_mem_norm_abs + q_boundary_mem_norm_abs)/min(Z_mem_min,M2_mem_min)",
            "required_inputs": "RSC4823_1, RSC4823_2, Z_mem_min, M2_mem_min, C_omega",
            "status": "feed_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def numeric_source_row(row_id: str, route_type: str, poynting_mode: str, timestamp: str) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": f"{poynting_mode} Poynting assignment smoke",
        "source_path": str(PATHS["4622_bound_feed"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": True,
        "beta_R_abs": 0.1,
        "R_obs_norm": 2.0,
        "beta_T_abs": 0.2,
        "T_obs_norm": 3.0,
        "beta_F_abs": 0.05,
        "F2_norm": 4.0,
        "beta_G_abs": 0.01,
        "FstarF_norm": 5.0,
        "beta_gw_abs": 0.03,
        "rho_gw_eff_norm": 6.0,
        "J_hidden_norm": 0.07,
        "beta_S_abs": 0.2,
        "poynting_mode": poynting_mode,
        "divS_norm": 0.5 if poynting_mode == "volume" else 0.0,
        "S_boundary_flux_abs": 0.5 if poynting_mode == "boundary" else 0.0,
        "Q_boundary_mem_abs": 0.04,
        "timestamp_utc": timestamp,
    }


def runner_input(timestamp: str) -> list[dict[str, Any]]:
    zero_base = {
        "route_type": "source_zero",
        "source_path": str(PATHS["4622_decomp"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": False,
        "parent_object_language_signed": False,
        "curvature_zero": False,
        "matter_trace_zero": False,
        "em_invariant_zero": False,
        "poynting_zero": False,
        "wave_stress_zero": False,
        "hidden_current_zero": False,
        "boundary_flux_zero": False,
        "boundary_reference_neutral": False,
        "no_incoming_flux": False,
    }
    live_missing = {
        "route_type": "source_bound",
        "source_path": str(PATHS["4622_bound_feed"]),
        "source_signed": False,
        "units_signed": False,
        "same_branch_signed": False,
        "beta_R_abs": "MISSING_PARENT_VALUE",
        "R_obs_norm": "MISSING_PROFILE",
        "beta_T_abs": "MISSING_PARENT_VALUE",
        "T_obs_norm": "MISSING_PROFILE",
        "beta_F_abs": "MISSING_PARENT_VALUE",
        "F2_norm": "MISSING_FIELD_NORM",
        "beta_G_abs": "MISSING_PARENT_VALUE",
        "FstarF_norm": "MISSING_FIELD_NORM",
        "beta_gw_abs": "MISSING_PARENT_VALUE",
        "rho_gw_eff_norm": "MISSING_WAVE_PROFILE",
        "J_hidden_norm": "MISSING_HIDDEN_CURRENT",
        "beta_S_abs": "MISSING_PARENT_VALUE",
        "poynting_mode": "MISSING_MODE",
        "divS_norm": "MISSING_OR_ZERO",
        "S_boundary_flux_abs": "MISSING_OR_ZERO",
        "Q_boundary_mem_abs": "MISSING_BOUNDARY_VALUE",
    }
    amplitude = numeric_source_row("RUN4823_6_amplitude_feed_smoke_pass", "amplitude_feed", "boundary", timestamp)
    amplitude.update({"Z_mem_min": 2.0, "M2_mem_min": 8.0, "C_omega": 1.5})
    double_count = numeric_source_row("RUN4823_7_poynting_double_slot_fails", "source_bound", "boundary", timestamp)
    double_count.update({"divS_norm": 0.5, "notes": "both poynting slots populated"})
    forbidden = numeric_source_row("RUN4823_8_forbidden_bound_backfit", "amplitude_feed", "boundary", timestamp)
    forbidden.update({"Z_mem_min": 2.0, "M2_mem_min": 8.0, "C_omega": 1.5, "notes": "BOUND_AS_SOURCE / FIT_TO_BOUND control"})
    return [
        {
            "row_id": "RUN4823_0_live_source_zero_missing",
            "route": "live total source/boundary zero audit",
            **zero_base,
            "notes": "live zero route lacks componentwise signed clauses",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4823_1_conditional_source_zero_pass",
            "route": "conditional total source/boundary zero theorem",
            **zero_base,
            "same_branch_signed": True,
            "parent_object_language_signed": True,
            "curvature_zero": True,
            "matter_trace_zero": True,
            "em_invariant_zero": True,
            "poynting_zero": True,
            "wave_stress_zero": True,
            "hidden_current_zero": True,
            "boundary_flux_zero": True,
            "boundary_reference_neutral": True,
            "no_incoming_flux": True,
            "notes": "control only: all source and boundary channels are signed zero",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4823_2_forbidden_GR_import_zero",
            "route": "forbidden GR-local-vacuum import",
            **zero_base,
            "same_branch_signed": True,
            "parent_object_language_signed": True,
            "curvature_zero": True,
            "matter_trace_zero": True,
            "em_invariant_zero": True,
            "poynting_zero": True,
            "wave_stress_zero": True,
            "hidden_current_zero": True,
            "boundary_flux_zero": True,
            "boundary_reference_neutral": True,
            "no_incoming_flux": True,
            "notes": "GR_IMPORT control: cannot prove local GR by importing local GR",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4823_3_live_source_bound_missing",
            "route": "live rho/qboundary source row",
            **live_missing,
            "notes": "live finite source row is still missing parent/source values",
            "timestamp_utc": timestamp,
        },
        numeric_source_row("RUN4823_4_boundary_poynting_source_bound_pass", "source_bound", "boundary", timestamp),
        numeric_source_row("RUN4823_5_volume_poynting_source_bound_pass", "source_bound", "volume", timestamp),
        amplitude,
        double_count,
        forbidden,
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "The memory source/boundary obstruction is now a channelwise source-density runner; exact zero remains unsigned, but finite rho/qboundary rows can feed 4822 without cancellation or Poynting double count.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4823_0_total_zero",
            "claim": "rho_mem=q_boundary_mem=0 gives Delta_v m_mem=0.",
            "required": "all source and boundary channels zero in the same parent branch",
            "current_status": "blocked_unsigned",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4823_1_finite_source",
            "claim": "rho_mem and q_boundary_mem finite bound can feed 4822.",
            "required": "all beta/source/J/Q/poynting inputs numeric, sourced, same-branch, and unit-signed",
            "current_status": "runner_ready_live_values_missing",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4823_2_poynting_guard",
            "claim": "Poynting is counted exactly once.",
            "required": "choose volume divergence, boundary flux, or zero mode; never both volume and boundary",
            "current_status": "guard_active",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PRIVATE_NONCLAIM",
            "result": "rho_mem/q_boundary source decomposition advanced to executable channel runner",
            "missing": "beta_R,beta_T,beta_F,beta_G,beta_S,beta_gw; source profiles; J_hidden; Q_boundary_mem; Z/M/C_omega for amplitude feed",
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The runner now names the exact first component values/zeros needed: B_mem_eff, J_mem_live, and Q_boundary_mem.",
            "first_question": "Can the B_mem/J_mem/Qboundary component vectors be killed by a parent source-functor/no-flux theorem, or must finite component values be filled?",
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
            "claim": "rho_mem_Qboundary_zero_or_first_source_density_row",
            "current_evidence": "4823 converts rho_mem and q_boundary_mem into a channelwise exact-zero-or-finite-source runner with a Poynting single-count guard.",
            "status": "rho_qboundary_channel_runner_private_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "source/boundary channel zeros unsigned; finite beta/source/J/Q values missing",
            "sector": "local_gr_EM_source_coupling",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "risk": "smoke rows pass but live source rows remain not source-backed",
            "title": "rho_mem/Qboundary zero or first source density row",
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
    return f"""# 4823 - rho_mem/Qboundary Zero Or First Source Density Row

Generated UTC: `{timestamp}`

Marker: `{MARKER}`

## Result

4823 pushes the 4822 finite-chain gate down one level. The local memory source is no longer a single foggy symbol:

```text
rho_mem = beta_R R_obs + beta_T T_obs + beta_F F_Q^2 + beta_G F_Q starF_Q
        + beta_S div S_EM or boundary beta_S S_EM.n
        + beta_gw rho_gw_eff + J_hidden

q_boundary_mem = Q_boundary_mem + optional converted Poynting boundary flux
```

The exact local plateau route is now explicit:

```text
rho_mem = 0 and q_boundary_mem = 0
```

only if every source channel and boundary channel is zero in the same parent branch. That is not signed by the current corpus. Static EM is especially important: Poynting silence does not kill `F_Q^2`; it only handles the flux/divergence channel.

The finite route is useful: the runner now computes `rho_mem_norm_abs`, `q_boundary_mem_norm_abs`, and the amplitude feed

```text
Delta_v m_mem <= C_omega (rho_mem_norm_abs + q_boundary_mem_norm_abs)/min(Z_mem_min,M2_mem_min).
```

## Source Register

{md_table(source_rows, ["source_id", "exists", "needle_found", "role"])}

## Channel Zero Audit

{md_table(audit_rows, ["channel_id", "piece", "current_result", "finite_input"])}

## Source Density Contract

{md_table(contract_rows, ["contract_id", "quantity", "formula", "status"])}

## Runner Output

{md_table(output_rows, ["row_id", "runner_status", "rho_mem_norm_abs", "q_boundary_mem_norm_abs", "Delta_v_m_mem_bound_abs", "missing_for_claim"])}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`
"""


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    statuses = {row["row_id"]: row["runner_status"] for row in output_rows}
    checks = [
        ("VAL4823_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL4823_01_needles_found", all(row["needle_found"] for row in source_rows), "all source needles found"),
        ("VAL4823_02_live_zero_blocked", statuses.get("RUN4823_0_live_source_zero_missing") == "BLOCKED_RHOMEM_QBOUNDARY_ZERO_CLAUSES", "live zero route remains blocked"),
        ("VAL4823_03_conditional_zero_pass", statuses.get("RUN4823_1_conditional_source_zero_pass") == "RHOMEM_QBOUNDARY_ZERO_PASS_NONCLAIM", "conditional total zero control passes"),
        ("VAL4823_04_forbidden_GR_fails", statuses.get("RUN4823_2_forbidden_GR_import_zero") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "GR import zero shortcut fails"),
        ("VAL4823_05_live_bound_blocked", statuses.get("RUN4823_3_live_source_bound_missing") == "BLOCKED_RHOMEM_QBOUNDARY_SOURCE_INPUTS", "live finite source row blocked"),
        ("VAL4823_06_boundary_poynting_pass", statuses.get("RUN4823_4_boundary_poynting_source_bound_pass") == "RHOMEM_QBOUNDARY_SOURCE_BOUND_PASS_NONCLAIM", "boundary Poynting source bound smoke passes"),
        ("VAL4823_07_volume_poynting_pass", statuses.get("RUN4823_5_volume_poynting_source_bound_pass") == "RHOMEM_QBOUNDARY_SOURCE_BOUND_PASS_NONCLAIM", "volume Poynting source bound smoke passes"),
        ("VAL4823_08_amplitude_feed_pass", statuses.get("RUN4823_6_amplitude_feed_smoke_pass") == "RHOMEM_QBOUNDARY_AMPLITUDE_FEED_PASS_NONCLAIM", "amplitude feed smoke passes"),
        ("VAL4823_09_double_slot_fails", statuses.get("RUN4823_7_poynting_double_slot_fails") == "BLOCKED_RHOMEM_QBOUNDARY_SOURCE_INPUTS", "Poynting double-slot row fails"),
        ("VAL4823_10_forbidden_backfit_fails", statuses.get("RUN4823_8_forbidden_bound_backfit") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "bound-backfit route fails"),
        ("VAL4823_11_no_claim_allowed", all(str(row.get("claim_allowed", "")).lower() == "false" for row in output_rows), "runner never allows a claim"),
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
    audit_rows = channel_audit(timestamp)
    contract_rows = source_contract(timestamp)
    input_rows = runner_input(timestamp)
    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(CHANNEL_AUDIT, audit_rows)
    write_csv(SOURCE_CONTRACT, contract_rows)
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
        "PPC4161 4823 rho/qboundary source channel runner",
        f"`{MARKER}`. The local memory source is decomposed into curvature, trace, EM scalar invariant, Poynting, wave-stress, hidden-current, and boundary channels. Exact zero is unsigned; finite source rows now feed the 4822 amplitude gate with a no-double-count Poynting guard. Decision: `{DECISION}`.",
    )
    append_section(
        PACKET_PATH,
        "4823 rho/qboundary source channel runner",
        f"`{MARKER}` turns the `rho_mem`/`q_boundary_mem` bottleneck into a source-density runner. Live claims remain blocked; smoke rows prove channel arithmetic, amplitude feeding, and anti-circular failures. Next: `{NEXT_TARGET}`.",
    )
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4823-Y5-R2FR-rho-mem-Qboundary-zero-or-first-source-density-row.md`
Marker: `{MARKER}`

## Where we are

4823 made the memory source/boundary bottleneck executable:

```text
rho_mem = beta_R R_obs + beta_T T_obs + beta_F F_Q^2 + beta_G F_Q starF_Q
        + beta_S div S_EM or boundary beta_S S_EM.n
        + beta_gw rho_gw_eff + J_hidden
q_boundary_mem = Q_boundary_mem + optional converted Poynting boundary flux
Delta_v m_mem <= C_omega (rho_mem_norm_abs + q_boundary_mem_norm_abs)/min(Z_mem_min,M2_mem_min)
```

## Live blockers

- Exact `rho_mem=q_boundary_mem=0` is not parent-signed.
- Static EM scalar invariant channels remain live unless `beta_F/beta_G` are killed or sourced.
- Poynting is now guarded as volume, boundary, or zero; it cannot be counted twice.
- Live finite rows still need `B_mem_eff`, `J_mem_live`, `Q_boundary_mem`, source profiles, units, and same-branch source paths.

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
        print(f"4823 generated with {len(failed)} validation failures")
        return 1
    print(f"4823 generated: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
