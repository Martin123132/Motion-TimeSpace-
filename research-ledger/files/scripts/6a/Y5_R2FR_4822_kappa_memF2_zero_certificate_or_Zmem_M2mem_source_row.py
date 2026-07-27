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

CHECKPOINT = "4822"
CLAIM_ID = "L-664"
MARKER = "PPC4161_KAPPA_MEMF2_ZERO_CERTIFICATE_OR_ZMEM_M2MEM_SOURCE_ROW_4822"
DECISION = "KAPPA_ZERO_UNSIGNED_ZMEM_M2MEM_FINITE_CHAIN_RUNNER_STAGED_NONCLAIM"
NEXT_TARGET = "4823-Y5-R2FR-rho-mem-Qboundary-zero-or-first-source-density-row.md"

DOC_PATH = POST / "4822-Y5-R2FR-kappa-memF2-zero-certificate-or-Zmem-M2mem-source-row.md"
FORMAL_PATH = FORMAL / "838-PPC4161-kappa-memF2-zero-certificate-or-Zmem-M2mem-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "kappa_memF2_Zmem_M2mem_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4822_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4822_KAPPA_ZERO_CERTIFICATE_AUDIT.csv"
AMPLITUDE_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4822_ZMEM_M2MEM_AMPLITUDE_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4822_KAPPA_ZMEM_M2MEM_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4822_KAPPA_ZMEM_M2MEM_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4822_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4822_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4822_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4822_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4822_VALIDATION.csv"

PATHS = {
    "resume": RESUME_PATH,
    "4821_doc": POST / "4821-Y5-R2FR-parent-visible-EM-generator-signature-or-HXF2-first-source-row.md",
    "4620_doc": POST / "4620-Y5-R2FR-kappa-memF2-owner-zero-or-first-numeric-coefficient-row.md",
    "4620_zero": SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_ZERO_ROUTES.csv",
    "4620_numeric": SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv",
    "4619_theorem": SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_THEOREM.csv",
    "4619_source": SOURCE_DIR / "P8_Y5_R2FR_4619_KAPPA_MEMF2_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv",
    "4621_identity": SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv",
    "4621_zmem": SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv",
    "4621_amplitude": SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_AMPLITUDE_BOUND_ROWS.csv",
    "4628_hessian": SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv",
    "4817_schur": SOURCE_DIR / "P8_Y5_R2FR_4817_SECOND_VARIATION_SCHUR_DERIVATION.csv",
    "4506_operator": SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv",
    "4506_body": SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv",
    "4506_extremum": SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_EXTREMUM_TEST.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4822_00_resume", PATHS["resume"], "4822-Y5-R2FR-kappa-memF2", "4821 selected this gate."),
        ("SRC4822_01_4821_doc", PATHS["4821_doc"], "C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem", "4821 finite EM/memory handoff."),
        ("SRC4822_02_4620_doc", PATHS["4620_doc"], "kappa_memF2 := partial_m Z_Q_eff", "4620 defines the coefficient owner."),
        ("SRC4822_03_4620_zero", PATHS["4620_zero"], "KZ4620_4_countermodel", "4620 zero/countermodel audit."),
        ("SRC4822_04_4620_numeric", PATHS["4620_numeric"], "KNUM4620_0_first_numeric_template", "4620 first numeric coefficient row."),
        ("SRC4822_05_4619_theorem", PATHS["4619_theorem"], "FMO4619_3_finite_derivative_law", "4619 finite derivative law."),
        ("SRC4822_06_4619_source", PATHS["4619_source"], "KMF4619_0_kappa_memF2", "4619 kappa/Zmem/M2mem source placeholders."),
        ("SRC4822_07_4621_identity", PATHS["4621_identity"], "MPI4621_2_nohair_zero", "4621 no-hair/positive operator identity."),
        ("SRC4822_08_4621_zmem", PATHS["4621_zmem"], "ZMR4621_0_Zmem_min", "4621 source rows for Zmem/M2mem/source/boundary."),
        ("SRC4822_09_4621_amplitude", PATHS["4621_amplitude"], "AMB4621_2_Cmemory_feed", "4621 amplitude bound feeding C_memory_F2."),
        ("SRC4822_10_4628_hessian", PATHS["4628_hessian"], "HES4628_1_parent_hessian_definitions", "4628 parent Hessian definitions."),
        ("SRC4822_11_4817_schur", PATHS["4817_schur"], "SV4817_2_Schur_Z", "4817 Schur-complement positivity guard."),
        ("SRC4822_12_4506_operator", PATHS["4506_operator"], "MOP4506_0_quadratic_action", "4506 memory quadratic operator."),
        ("SRC4822_13_4506_body", PATHS["4506_body"], "BCIN4506_0_memory_density", "4506 memory body-source density."),
        ("SRC4822_14_4506_extremum", PATHS["4506_extremum"], "MEXT4506_1_branch_extremum", "4506 extremum route."),
        ("SRC4822_15_runner", PATHS["runner"], "def evaluate_row", "4822 executable runner."),
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


def zero_audit(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "KZ4822_0_typed_domain_zero",
            "route": "typed coefficient-domain exclusion",
            "test": "Coeff(F_Q^2) parent object language excludes m_mem/hidden scalar arguments.",
            "current_result": "NOT_PARENT_SIGNED",
            "blocker": "no parent-owned object-language certificate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "KZ4822_1_branch_extremum_zero",
            "route": "double-zero/extremum",
            "test": "Z_Q_eff(m)=Z_Q0+1/2 Z2 delta_m^2+... on the same branch, so partial_m Z_Q_eff|branch=0.",
            "current_result": "CONDITIONAL_NOT_EM_F2_SIGNED",
            "blocker": "no parent-selected EM coefficient functional with readout/radiative stability",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "KZ4822_2_shift_or_selection_symmetry",
            "route": "exact memory shift/selection symmetry",
            "test": "visible EM coefficients are even or derivative-only in m_mem.",
            "current_result": "NOT_PARENT_SIGNED",
            "blocker": "symmetry law and anomaly/readout closure missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "KZ4822_3_fixed_branch_firewall",
            "route": "fixed q-basic visible branch",
            "test": "fixed standard branch has no extra F2 slot.",
            "current_result": "PRIVATE_BRANCH_ONLY_NOT_GLOBAL",
            "blocker": "cannot combine standard branch zero with dynamic MTS amplitude rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "KZ4822_4_countermodel_retained",
            "route": "legal mixed scalar operator",
            "test": "DeltaS=-(1/4) int mu_obs kappa_memF2 delta_m F_Q^2 is covariant and U1 gauge invariant if the target slot exists.",
            "current_result": "COUNTERMODEL_PREVENTS_FAKE_ZERO",
            "blocker": "ordinary covariance/gauge symmetry does not kill kappa_memF2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def amplitude_contract(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "ZMC4822_0_lambda",
            "quantity": "lambda_mem",
            "formula": "lambda_mem = sqrt(Z_mem_min/M2_mem_min)",
            "required_inputs": "Z_mem_min>0; M2_mem_min>0; same-branch parent Hessian or Schur-reduced effective values",
            "status": "symbolic_law_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "ZMC4822_1_amplitude",
            "quantity": "Delta_v_m_mem_bound_abs",
            "formula": "Delta_v m_mem <= C_omega (||rho_mem|| + ||q_boundary_mem||)/min(Z_mem_min,M2_mem_min)",
            "required_inputs": "rho_mem norm or zero; boundary norm or zero; C_omega; units; same branch",
            "status": "finite_bound_runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "ZMC4822_2_Cmemory",
            "quantity": "C_memory_F2_abs",
            "formula": "|kappa_memF2| Delta_v_m_mem_bound_abs / Z_Q_eff_min",
            "required_inputs": "kappa_memF2_abs; Z_Q_eff_min>0; ZMC4822_1",
            "status": "finite_chain_runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "ZMC4822_3_qbar",
            "quantity": "qbar_EM_memory_abs",
            "formula": "K_qbar_EM_abs C_memory_F2_abs",
            "required_inputs": "arena projection K_qbar_EM_abs; ZMC4822_2",
            "status": "projection_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_input(timestamp: str) -> list[dict[str, Any]]:
    zero_base = {
        "route_type": "kappa_zero",
        "source_path": str(PATHS["4620_zero"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": False,
        "readout_radiative_closure_signed": False,
        "parent_object_language_signed": False,
        "typed_domain_zero": False,
        "fixed_branch_zero": False,
        "branch_extremum_zero": False,
        "symmetry_zero": False,
    }
    amp_missing = {
        "route_type": "memory_amplitude_bound",
        "source_path": str(PATHS["4621_amplitude"]),
        "source_signed": False,
        "units_signed": False,
        "same_branch_signed": False,
        "Z_mem_min": "MISSING_PARENT_VALUE",
        "M2_mem_min": "MISSING_PARENT_VALUE",
        "rho_mem_norm": "MISSING_SOURCE_ZERO_OR_BOUND",
        "q_boundary_mem_norm": "MISSING_BOUNDARY_ZERO_OR_BOUND",
        "C_omega": "MISSING_GEOMETRY_CONSTANT",
    }
    amp_smoke = {
        "route_type": "memory_amplitude_bound",
        "source_path": str(PATHS["4621_amplitude"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": True,
        "Z_mem_min": 2.0,
        "M2_mem_min": 8.0,
        "rho_mem_norm": 0.1,
        "q_boundary_mem_norm": 0.02,
        "C_omega": 1.5,
    }
    return [
        {
            "row_id": "RUN4822_0_live_kappa_zero_missing",
            "route": "live kappa zero audit",
            **zero_base,
            "notes": "live zero route has no parent signed exact-zero certificate",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4822_1_conditional_kappa_zero_pass",
            "route": "conditional exact zero theorem",
            **zero_base,
            "same_branch_signed": True,
            "readout_radiative_closure_signed": True,
            "parent_object_language_signed": True,
            "branch_extremum_zero": True,
            "notes": "control row only: if the exact clauses are signed, first-order memory/F2 vanishes",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4822_2_forbidden_standard_global",
            "route": "forbidden standard-branch globalization",
            **zero_base,
            "same_branch_signed": True,
            "readout_radiative_closure_signed": True,
            "parent_object_language_signed": True,
            "fixed_branch_zero": True,
            "notes": "STANDARD_BRANCH_AS_GLOBAL is forbidden even if the branch row is true",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4822_3_live_amplitude_missing",
            "route": "live Zmem/M2mem amplitude row",
            **amp_missing,
            "notes": "live row must stay blocked until parent-owned values or zeros exist",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4822_4_amplitude_smoke_pass",
            "route": "amplitude arithmetic smoke",
            **amp_smoke,
            "notes": "schema/arithmetic control, not a claim row",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4822_5_finite_chain_smoke_pass",
            "route": "finite C_memory/qbar chain smoke",
            "route_type": "finite_chain",
            "source_path": str(PATHS["4621_amplitude"]),
            "source_signed": True,
            "units_signed": True,
            "same_branch_signed": True,
            "Z_mem_min": 2.0,
            "M2_mem_min": 8.0,
            "rho_mem_norm": 0.1,
            "q_boundary_mem_norm": 0.02,
            "C_omega": 1.5,
            "kappa_memF2_abs": 0.02,
            "Z_Q_eff_min": 2.0,
            "K_qbar_EM_abs": 0.5,
            "notes": "finite route works when all parent values are supplied",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4822_6_live_finite_chain_missing",
            "route": "live finite chain",
            "route_type": "finite_chain",
            "source_path": str(PATHS["4619_source"]),
            "source_signed": False,
            "units_signed": False,
            "same_branch_signed": False,
            "Z_mem_min": "MISSING_PARENT_VALUE",
            "M2_mem_min": "MISSING_PARENT_VALUE",
            "rho_mem_norm": "MISSING_SOURCE_ZERO_OR_BOUND",
            "q_boundary_mem_norm": "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "C_omega": "MISSING_GEOMETRY_CONSTANT",
            "kappa_memF2_abs": "MISSING_NUMERIC_OR_ZERO",
            "Z_Q_eff_min": "MISSING_POSITIVE_DENOMINATOR",
            "K_qbar_EM_abs": "MISSING_ARENA_PROJECTION",
            "notes": "live finite chain remains blocked by missing source rows",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4822_7_forbidden_bound_backfit",
            "route": "forbidden bound-backfit row",
            "route_type": "finite_chain",
            "source_path": str(PATHS["4621_amplitude"]),
            "source_signed": True,
            "units_signed": True,
            "same_branch_signed": True,
            "Z_mem_min": 2.0,
            "M2_mem_min": 8.0,
            "rho_mem_norm": 0.1,
            "q_boundary_mem_norm": 0.02,
            "C_omega": 1.5,
            "kappa_memF2_abs": 0.02,
            "Z_Q_eff_min": 2.0,
            "K_qbar_EM_abs": 0.5,
            "notes": "BOUND_AS_SOURCE / FIT_TO_BOUND control must fail",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "The exact kappa_memF2=0 route is not parent-signed, but the finite Zmem/M2mem amplitude law is now executable and anti-circular.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4822_0_exact_zero",
            "claim": "kappa_memF2=0 removes first-order memory/F2 leakage.",
            "required": "one exact zero route plus same_branch, parent object language, and readout/radiative closure",
            "current_status": "blocked_unsigned",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4822_1_finite_bound",
            "claim": "finite C_memory_F2/qbar_EM_memory bound can be scored.",
            "required": "kappa_memF2, Z_Q_eff_min, Z_mem_min, M2_mem_min, rho/boundary norms or zeros, C_omega, K_qbar_EM",
            "current_status": "runner_ready_live_values_missing",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4822_2_anti_circularity",
            "claim": "no local/R10/PPN/clock/orbital pass from bounds fitted backwards.",
            "required": "no BOUND_AS_SOURCE, FIT_TO_BOUND, measured-G absorption, standard-branch globalization, or Poynting double count",
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
            "result": "derive-or-bound branch advanced to an executable finite-chain contract",
            "missing": "kappa_memF2; Z_Q_eff_min; Z_mem_min; M2_mem_min; rho_mem_norm or zero; q_boundary_mem_norm or zero; C_omega; K_qbar_EM",
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The finite route now bottlenecks on the memory source and boundary terms, not on the algebraic kappa/Zmem scaffold.",
            "first_question": "Can rho_mem and q_boundary_mem be killed by a same-branch source/boundary theorem, or must they become first source-density rows?",
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
            "claim": "kappa_memF2_zero_certificate_or_Zmem_M2mem_source_row",
            "current_evidence": "4822 converts the kappa_memF2/Zmem/M2mem memory-EM leakage problem into an executable exact-zero-or-finite-chain runner; live values remain unsigned.",
            "status": "kappa_zmem_m2mem_runner_private_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "no parent zero certificate; no kappa/ZQ/Zmem/M2mem/rho/boundary/K source rows",
            "sector": "local_gr_EM_source_coupling",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite smoke rows pass but live rows are not source-backed",
            "title": "kappa_memF2 zero certificate or Zmem/M2mem source row",
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


def build_doc(timestamp: str, source_rows: list[dict[str, Any]], zero_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> str:
    return f"""# 4822 - kappa_memF2 Zero Certificate Or Zmem/M2mem Source Row

Generated UTC: `{timestamp}`

Marker: `{MARKER}`

## Result

4822 is the point where the work stops merely saying "the coupling is missing" and turns it into a hard executable contract.

```text
kappa_memF2 := partial_m Z_Q_eff | branch
lambda_mem = sqrt(Z_mem_min/M2_mem_min)
Delta_v m_mem <= C_omega (||rho_mem|| + ||q_boundary_mem||)/min(Z_mem_min,M2_mem_min)
C_memory_F2 <= |kappa_memF2| Delta_v m_mem / Z_Q_eff_min
qbar_EM_memory <= K_qbar_EM C_memory_F2
```

The exact-zero route is still unsigned. Ordinary covariance and U1 gauge symmetry do not kill the mixed scalar/F2 operator. A real zero needs a parent object-language exclusion, a same-branch double-zero/extremum, or an exact selection symmetry that survives readout/radiative closure.

The useful move is now finite and testable: source or kill `rho_mem` and `q_boundary_mem`, then source `kappa_memF2`, `Z_Q_eff_min`, `Z_mem_min`, `M2_mem_min`, and `K_qbar_EM` from the parent/action branch. Bound fitting, measured-G absorption, standard-branch globalization, and Poynting double counting remain forbidden.

## Source Register

{md_table(source_rows, ["source_id", "exists", "needle_found", "role"])}

## kappa Zero Audit

{md_table(zero_rows, ["zero_id", "route", "current_result", "blocker"])}

## Zmem/M2mem Amplitude Contract

{md_table(contract_rows, ["contract_id", "quantity", "formula", "status"])}

## Runner Output

{md_table(output_rows, ["row_id", "runner_status", "lambda_mem", "Delta_v_m_mem_bound_abs", "C_memory_F2_abs", "qbar_EM_memory_abs", "missing_for_claim"])}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`
"""


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    statuses = {row["row_id"]: row["runner_status"] for row in output_rows}
    checks = [
        ("VAL4822_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL4822_01_needles_found", all(row["needle_found"] for row in source_rows), "all source needles found"),
        ("VAL4822_02_live_zero_blocked", statuses.get("RUN4822_0_live_kappa_zero_missing") == "BLOCKED_KAPPA_MEMF2_ZERO_CLAUSES", "live zero row remains blocked"),
        ("VAL4822_03_conditional_zero_pass", statuses.get("RUN4822_1_conditional_kappa_zero_pass") == "KAPPA_MEMF2_ZERO_PASS_NONCLAIM", "conditional exact-zero control passes"),
        ("VAL4822_04_forbidden_global_fails", statuses.get("RUN4822_2_forbidden_standard_global") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "standard-branch globalization fails"),
        ("VAL4822_05_live_amplitude_blocked", statuses.get("RUN4822_3_live_amplitude_missing") == "BLOCKED_ZMEM_M2MEM_AMPLITUDE_INPUTS", "live amplitude row blocked"),
        ("VAL4822_06_amplitude_smoke_pass", statuses.get("RUN4822_4_amplitude_smoke_pass") == "ZMEM_M2MEM_AMPLITUDE_BOUND_PASS_NONCLAIM", "amplitude smoke row passes"),
        ("VAL4822_07_finite_chain_smoke_pass", statuses.get("RUN4822_5_finite_chain_smoke_pass") == "KAPPA_ZMEM_M2MEM_FINITE_CHAIN_PASS_NONCLAIM", "finite chain smoke row passes"),
        ("VAL4822_08_live_finite_chain_blocked", statuses.get("RUN4822_6_live_finite_chain_missing") == "BLOCKED_KAPPA_ZMEM_M2MEM_FINITE_CHAIN_INPUTS", "live finite chain row blocked"),
        ("VAL4822_09_forbidden_backfit_fails", statuses.get("RUN4822_7_forbidden_bound_backfit") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "bound-backfit route fails"),
        ("VAL4822_10_no_claim_allowed", all(str(row.get("claim_allowed", "")).lower() == "false" for row in output_rows), "runner never allows a claim"),
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
    zero_rows = zero_audit(timestamp)
    contract_rows = amplitude_contract(timestamp)
    input_rows = runner_input(timestamp)
    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(ZERO_AUDIT, zero_rows)
    write_csv(AMPLITUDE_CONTRACT, contract_rows)
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

    doc = build_doc(timestamp, source_rows, zero_rows, contract_rows, output_rows)
    write_text(DOC_PATH, doc)
    write_text(FORMAL_PATH, doc)
    append_claim(timestamp)
    append_section(
        SPINE_PATH,
        "PPC4161 4822 kappa/Zmem/M2mem finite-chain gate",
        f"`{MARKER}`. Exact `kappa_memF2=0` is not parent-signed. The finite route is now executable: source or zero `rho_mem` and `q_boundary_mem`, then provide same-branch `kappa_memF2`, `Z_Q_eff_min`, `Z_mem_min`, `M2_mem_min`, and `K_qbar_EM`. Decision: `{DECISION}`.",
    )
    append_section(
        PACKET_PATH,
        "4822 kappa/Zmem/M2mem gate",
        f"`{MARKER}` records the memory/EM leakage law as an anti-circular runner. Live local-GR/Maxwell claims remain blocked; smoke rows prove only the arithmetic and failure modes. Next: `{NEXT_TARGET}`.",
    )
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4822-Y5-R2FR-kappa-memF2-zero-certificate-or-Zmem-M2mem-source-row.md`
Marker: `{MARKER}`

## Where we are

4822 made the memory/EM coupling gate executable:

```text
kappa_memF2 exact-zero route = unsigned
finite route = runner-ready
C_memory_F2 <= |kappa_memF2| Delta_v m_mem / Z_Q_eff_min
Delta_v m_mem <= C_omega (||rho_mem|| + ||q_boundary_mem||)/min(Z_mem_min,M2_mem_min)
```

## Live blockers

- No parent-signed exact-zero certificate for `kappa_memF2`.
- No same-branch numeric/source rows for `kappa_memF2`, `Z_Q_eff_min`, `Z_mem_min`, `M2_mem_min`, `rho_mem_norm`, `q_boundary_mem_norm`, `C_omega`, or `K_qbar_EM`.
- Bound-backfit, measured-G absorption, standard-branch globalization, and Poynting double count remain forbidden.

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
        print(f"4822 generated with {len(failed)} validation failures")
        return 1
    print(f"4822 generated: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
