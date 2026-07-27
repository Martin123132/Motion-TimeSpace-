from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3063"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3063-Y5-R2FR-extra-field-double-zero-proof-or-Delta-kST-component-bound-runner-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3063_00_3062_doc": ROOT / "3062-Y5-R2FR-EH-operator-dominance-and-extra-field-silence-or-Delta-kST-input-fill-under-AX1090.md",
    "SRC3063_01_3062_EH_attempt": RESIDUALS / "P8_Y5_R2FR_3062_EH_OPERATOR_DOMINANCE_ATTEMPT.csv",
    "SRC3063_02_3062_extra_audit": RESIDUALS / "P8_Y5_R2FR_3062_EXTRA_FIELD_SILENCE_AUDIT.csv",
    "SRC3063_03_3062_delta_inputs": RESIDUALS / "P8_Y5_R2FR_3062_DELTA_KST_INPUT_ROWS_NONCLAIM.csv",
    "SRC3063_04_3062_next": RESIDUALS / "P8_Y5_R2FR_3062_NEXT_TARGET.csv",
    "SRC3063_05_local_action_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3063_06_double_zero_matrix": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_DOUBLE_ZERO_STATUS_MATRIX.csv",
    "SRC3063_07_leakage_residuals": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_LEAKAGE_RESIDUAL_ROWS.csv",
    "SRC3063_08_operator_inventory": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_OPERATOR_INVENTORY.csv",
    "SRC3063_09_extra_response_certificate": RESIDUALS / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv",
    "SRC3063_10_extra_sector_audit": RESIDUALS / "P8_Y5_R2FR_2925_EXTRA_SECTOR_SILENCE_AUDIT.csv",
    "SRC3063_11_hilbert": RESIDUALS / "P8_Y5_R2FR_3053_HILBERT_SOURCE_READOUT_AUDIT.csv",
    "SRC3063_12_absorption": RESIDUALS / "P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv",
    "SRC3063_13_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3063_SOURCE_REGISTER.csv",
    "double_zero_attempt": RESIDUALS / "P8_Y5_R2FR_3063_EXTRA_DOUBLE_ZERO_PROOF_ATTEMPT.csv",
    "sector_status": RESIDUALS / "P8_Y5_R2FR_3063_EXTRA_SECTOR_COMPONENT_STATUS.csv",
    "component_runner": RESIDUALS / "P8_Y5_R2FR_3063_DELTA_KST_COMPONENT_BOUND_RUNNER_NONCLAIM.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3063_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3063_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3063_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3063_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3063_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "double_zero_attempt_copy": PARENT_ACTION / "extra_field_double_zero_proof_attempt_3063_NOT_SIGNED.csv",
    "sector_status_copy": LOCAL_BOUNDS / "extra_sector_component_status_3063_NONCLAIM.csv",
    "component_runner_copy": LOCAL_BOUNDS / "Delta_kST_component_bound_runner_3063_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3063_GammaKhat_q_loc_double_zero_or_component_bound_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: as_str(output_row.get(key, "")) for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, str] | dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "proof_signed",
        "theorem_zero",
        "bound_ready",
        "ready_for_numeric_run",
    }
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        values = []
        for column in columns:
            value = as_str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def status_pass(value: str) -> bool:
    return value.strip().lower() in {"signed", "proved", "zero", "closed", "parent_signed", "theorem_zero"}


def status_quality(value: str) -> str:
    lowered = value.strip().lower()
    if status_pass(value):
        return "SIGNED"
    if "candidate" in lowered or "conditional" in lowered:
        return "CANDIDATE_ONLY"
    if "open" in lowered:
        return "OPEN"
    if "not_signed" in lowered or "unsigned" in lowered:
        return "NOT_SIGNED"
    return "UNRESOLVED"


dotg_rows_before = rows(DOTG_TARGET)
double_zero_source_rows = rows(SOURCE_PATHS["SRC3063_06_double_zero_matrix"])
leakage_rows = rows(SOURCE_PATHS["SRC3063_07_leakage_residuals"])

source_register = [
    base(
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "parse_ok": csv_ok(path) if path.suffix.lower() == ".csv" and path.exists() else "",
            "row_count": len(rows(path)) if path.suffix.lower() == ".csv" and path.exists() else "",
            "role": source_id.split("_", 2)[-1],
            "status": "PRESENT" if path.exists() else "MISSING_BLOCKER",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

double_zero_attempt_rows = [
    base(
        {
            "clause_id": "DZ3063_0_fixed_point_chart",
            "clause": "same local fixed-point chart Phi^A=Phi0 is used by all extra fields and readout maps",
            "required_signature": "q-map, readout, source and boundary sectors use the same branch and denominator",
            "current_status": "MISSING_SAME_BRANCH_CERTIFICATE",
            "proof_signed": "false",
            "would_buy": "prevents sector-by-sector closures from being stitched across incompatible gauges",
            "blocking_gap": "extra-response certificate says same-branch denominator is missing",
            "source_path": str(SOURCE_PATHS["SRC3063_09_extra_response_certificate"]),
        }
    ),
    base(
        {
            "clause_id": "DZ3063_1_value_zero_C0",
            "clause": "extra coupling values vanish at the local fixed point",
            "required_signature": "C_X(Phi0)=0 for every extra sector that can source local metric response",
            "current_status": "NOT_SIGNED_OR_OPEN_BY_SECTOR",
            "proof_signed": "false",
            "would_buy": "removes constant extra stress/source offsets",
            "blocking_gap": "2580 status matrix retains not_signed/open/candidate_only rows",
            "source_path": str(SOURCE_PATHS["SRC3063_06_double_zero_matrix"]),
        }
    ),
    base(
        {
            "clause_id": "DZ3063_2_derivative_zero_dC",
            "clause": "extra coupling first derivatives vanish at the local fixed point",
            "required_signature": "D_A C_X(Phi0)=0 after constraints, quotient modes and representative gauge are removed",
            "current_status": "NOT_SIGNED_OR_OPEN_BY_SECTOR",
            "proof_signed": "false",
            "would_buy": "kills the first-order Delta_extra_linear term in Delta_kST",
            "blocking_gap": "no parent-signed coupling derivative theorem exists for GK/PiM/domain/readout sectors",
            "source_path": str(SOURCE_PATHS["SRC3063_06_double_zero_matrix"]),
        }
    ),
    base(
        {
            "clause_id": "DZ3063_3_extremum_dV",
            "clause": "extra potential/current functional has a local extremum",
            "required_signature": "D_A V(Phi0)=0 or Euler/Helmholtz equation forces the same condition in the observed branch",
            "current_status": "GK_HELMHOLTZ_AND_SOURCE_GLUE_UNSIGNED",
            "proof_signed": "false",
            "would_buy": "prevents q_loc or source-measure hair from generating local force residuals",
            "blocking_gap": "Gamma/Khat/q_loc and source glue are marked as hard blockers",
            "source_path": str(SOURCE_PATHS["SRC3063_10_extra_sector_audit"]),
        }
    ),
    base(
        {
            "clause_id": "DZ3063_4_positive_gap",
            "clause": "linearized extra operator is positive/self-adjoint or topological/constraint-closed",
            "required_signature": "M_AB and derivative pieces have a positive gap on the compact local collar after gauge quotient",
            "current_status": "FORMAL_CANDIDATE_ONLY_OR_OPEN",
            "proof_signed": "false",
            "would_buy": "turns small perturbations into bounded short-range nonpropagating residuals",
            "blocking_gap": "operator domain and gap/closure entries are not parent-certified",
            "source_path": str(SOURCE_PATHS["SRC3063_09_extra_response_certificate"]),
        }
    ),
    base(
        {
            "clause_id": "DZ3063_5_boundary_silence",
            "clause": "local boundary/projector/reference terms carry no force, source or metric-response flux",
            "required_signature": "no-flux boundary condition plus P_loc commutator zero in the same branch",
            "current_status": "OPEN",
            "proof_signed": "false",
            "would_buy": "kills Delta_boundary_projector and hidden source-charge leakage",
            "blocking_gap": "boundary/reference/projector sectors are open and no local collar boundary data is supplied",
            "source_path": str(SOURCE_PATHS["SRC3063_07_leakage_residuals"]),
        }
    ),
    base(
        {
            "clause_id": "DZ3063_6_physical_lock",
            "clause": "the abstract double-zero variables equal the measured PPN/local residual variables",
            "required_signature": "Z^A is locked to gamma, beta, alpha_i, xi, Gdot, R10/R11 and source-mass residuals in one observed frame",
            "current_status": "NOT_DERIVED",
            "proof_signed": "false",
            "would_buy": "prevents a formal zero in bookkeeping variables from being mistaken for a physical local-GR zero",
            "blocking_gap": "PPN/local residual lock is explicitly not derived",
            "source_path": str(SOURCE_PATHS["SRC3063_09_extra_response_certificate"]),
        }
    ),
    base(
        {
            "clause_id": "DZ3063_7_verdict",
            "clause": "all clauses DZ3063_0 through DZ3063_6 pass in the same branch",
            "required_signature": "parent-signed local extra-field double-zero theorem",
            "current_status": "NOT_PROVED_CURRENT_CORPUS",
            "proof_signed": "false",
            "would_buy": "sets Delta_extra_linear=0",
            "blocking_gap": "too many clauses are unsigned; use component-bound fallback",
            "source_path": str(OUTPUTS["double_zero_attempt"]),
        }
    ),
]

sector_status_rows: list[dict[str, Any]] = []
for source_row in double_zero_source_rows:
    c0 = source_row.get("C0_status", "")
    dc = source_row.get("dC_status", "")
    gap = source_row.get("gap_or_closure_status", "")
    boundary = source_row.get("boundary_status", "")
    passes = all(status_pass(value) for value in [c0, dc, gap, boundary])
    status_pack = ";".join(status_quality(value) for value in [c0, dc, gap, boundary])
    sector_status_rows.append(
        base(
            {
                "sector_id": source_row.get("sector_id", ""),
                "parent_sector": source_row.get("parent_sector", ""),
                "C0_status": c0,
                "dC_status": dc,
                "gap_or_closure_status": gap,
                "boundary_status": boundary,
                "status_quality_pack": status_pack,
                "double_zero_passes": str(passes).lower(),
                "proof_signed": "false",
                "feeds_Delta_kST": "true" if source_row.get("parent_sector", "") in {"Gamma/Khat/q_loc", "response/memory doublet", "domain/projector selector", "metric/readout protection", "PiM/source-measure projector", "boundary/reference/exact/topological"} else "parallel_or_indirect",
                "priority": source_row.get("priority", ""),
                "promotion_status": source_row.get("promotion_status", ""),
                "reason": source_row.get("reason", "current evidence inventory only"),
                "source_path": str(SOURCE_PATHS["SRC3063_06_double_zero_matrix"]),
            }
        )
    )

component_specs = [
    {
        "component_id": "DKCB3063_0_total",
        "Delta_component": "Delta_kST_component_envelope",
        "sector": "all",
        "residual_symbols": "Delta_EH_operator;Delta_extra_linear;Delta_source_anisotropy;Delta_gauge_readout;Delta_boundary_projector",
        "bound_formula": "abs(Delta_kST)<=sum_i abs(Delta_i) with no-cancellation policy",
        "missing_numeric_inputs": "ALL_COMPONENT_NUMERIC_INPUTS_MISSING",
        "observable_targets": "PPN_gamma;local_GR;Newton_transfer",
        "source_path": str(SOURCE_PATHS["SRC3063_03_3062_delta_inputs"]),
    },
    {
        "component_id": "DKCB3063_1_GK",
        "Delta_component": "Delta_extra_GK_linear",
        "sector": "Gamma/Khat/q_loc",
        "residual_symbols": "epsilon_C0_GammaKhat;epsilon_dC_GammaKhat;q_loc^nu",
        "bound_formula": "abs(eta_GK)*(abs(epsilon_C0_GammaKhat)+abs(epsilon_dC_GammaKhat)+abs(q_loc_projection))/max(M_GK^2,M_floor^2)",
        "missing_numeric_inputs": "MISSING_eta_GK;MISSING_epsilon_C0_GammaKhat;MISSING_epsilon_dC_GammaKhat;MISSING_q_loc_projection;MISSING_M_GK",
        "observable_targets": "PPN_gamma;local_force;source_mass",
        "source_path": str(SOURCE_PATHS["SRC3063_07_leakage_residuals"]),
    },
    {
        "component_id": "DKCB3063_2_memory",
        "Delta_component": "Delta_extra_memory_linear",
        "sector": "response/memory doublet",
        "residual_symbols": "epsilon_C0_memory_response;epsilon_dC_memory_response",
        "bound_formula": "abs(eta_mem)*(abs(epsilon_C0_memory_response)+abs(epsilon_dC_memory_response))/max(M_mem^2,M_floor^2)",
        "missing_numeric_inputs": "MISSING_eta_mem;MISSING_memory_epsilons;MISSING_M_mem;MISSING_same_branch_lock",
        "observable_targets": "clock;PPN_gamma;source_normalization",
        "source_path": str(SOURCE_PATHS["SRC3063_09_extra_response_certificate"]),
    },
    {
        "component_id": "DKCB3063_3_domain",
        "Delta_component": "Delta_domain_projector",
        "sector": "domain/projector selector",
        "residual_symbols": "epsilon_domain_projector_stress;P_loc_commutator",
        "bound_formula": "abs(eta_D)*(abs(epsilon_domain_projector_stress)+abs(P_loc_commutator))",
        "missing_numeric_inputs": "MISSING_eta_D;MISSING_projector_stress;MISSING_P_loc_commutator;MISSING_boundary_condition",
        "observable_targets": "PPN_preferred_frame;WEP;branch_switching",
        "source_path": str(SOURCE_PATHS["SRC3063_07_leakage_residuals"]),
    },
    {
        "component_id": "DKCB3063_4_readout",
        "Delta_component": "Delta_gauge_readout",
        "sector": "metric/readout protection",
        "residual_symbols": "epsilon_readout_gauge_owner;epsilon_metric_readout_linear",
        "bound_formula": "abs(epsilon_readout_gauge_owner)+abs(epsilon_metric_readout_linear) after no-disformal and gauge lock",
        "missing_numeric_inputs": "MISSING_readout_gauge_owner;MISSING_metric_readout_linear;MISSING_no_disformal_proof;MISSING_gauge_lock",
        "observable_targets": "PPN_beta;PPN_gamma;light_time;orbital",
        "source_path": str(SOURCE_PATHS["SRC3063_08_operator_inventory"]),
    },
    {
        "component_id": "DKCB3063_5_PiM",
        "Delta_component": "Delta_source_anisotropy",
        "sector": "PiM/source-measure projector",
        "residual_symbols": "epsilon_PiM_value;epsilon_DPiM;I_commutator;R_eq_integral",
        "bound_formula": "abs(epsilon_PiM_value)+abs(epsilon_DPiM)+abs(I_commutator)+abs(R_eq_integral)",
        "missing_numeric_inputs": "MISSING_PiM_value;MISSING_DPiM;MISSING_I_commutator;MISSING_R_eq_integral;MISSING_Hilbert_source_descent",
        "observable_targets": "Newton_source_normalization;R10;R11;measured_GM",
        "source_path": str(SOURCE_PATHS["SRC3063_07_leakage_residuals"]),
    },
    {
        "component_id": "DKCB3063_6_boundary",
        "Delta_component": "Delta_boundary_projector",
        "sector": "boundary/reference/exact/topological",
        "residual_symbols": "epsilon_boundary_reference_zero;B_zero_flux;Delta_boundary_coupling",
        "bound_formula": "abs(epsilon_boundary_reference_zero)+abs(B_zero_flux)+abs(Delta_boundary_coupling)",
        "missing_numeric_inputs": "MISSING_boundary_reference_zero;MISSING_B_zero_flux;MISSING_Delta_boundary_coupling;MISSING_local_collar_data",
        "observable_targets": "Newton;PPN;R10;orbital",
        "source_path": str(SOURCE_PATHS["SRC3063_07_leakage_residuals"]),
    },
]

component_runner_rows = [
    base(
        {
            **component,
            "candidate_value": "MISSING_COMPONENT_INPUTS",
            "units": "dimensionless_or_declared_per_component",
            "ready_for_numeric_run": "false",
            "bound_ready": "false",
            "claim_policy": "no claim until every term is theorem-zero or source-backed numeric with units and same-branch denominator",
        }
    )
    for component in component_specs
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3063_0_extra_double_zero",
            "claim": "extra-field double-zero theorem is parent-signed",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "C0/dC/gap/boundary/branch/physical-lock clauses remain unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3063_1_Delta_extra_linear_zero",
            "claim": "Delta_extra_linear=0",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "zero follows only after all double-zero and boundary clauses pass",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3063_2_component_bounds_ready",
            "claim": "Delta_kST component bounds are numeric/source-backed",
            "status": "NO_SCHEMA_ONLY",
            "claim_active": "false",
            "reason": "3063 writes the runner schema but every component still has missing numeric inputs",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3063_3_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "NO",
            "claim_active": "false",
            "reason": "extra-sector double zero is not proved and EH/source/gauge gates remain upstream blockers",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3063_0_broad_proof",
            "question": "Did the broad extra-field double-zero theorem close?",
            "answer": "NO",
            "reason": "the source status matrix contains not_signed/open/candidate_only rows, not a parent signature",
            "action": "keep Delta_extra_linear live",
        }
    ),
    base(
        {
            "decision_id": "DEC3063_1_runner",
            "question": "Can we at least run numeric bounds now?",
            "answer": "NO",
            "reason": "the component rows are missing coefficients, norms, masses/gaps and same-branch denominators",
            "action": "runner is schema-only and nonclaim",
        }
    ),
    base(
        {
            "decision_id": "DEC3063_2_best_next",
            "question": "Best next target?",
            "answer": "ATTACK_GK_QLOC_FIRST",
            "reason": "Gamma/Khat/q_loc is highest priority, directly feeds local force/PPN/source-mass residuals, and has the clearest double-zero form",
            "action": "try to prove the GK Helmholtz/Euler double-zero before broad inventory work",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3063_0_3064",
            "next_checkpoint": "3064-Y5-R2FR-GammaKhat-q_loc-double-zero-proof-or-GK-component-bound-runner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_GammaKhat_q_loc_double_zero_proof_or_GK_component_bound_runner_under_AX1090_3064.py",
            "mission": "try to parent-sign the Gamma/Khat/q_loc double zero and q_loc projection silence; if not, build the GK component bound rows",
            "starting_equation": "Delta_extra_GK_linear ~ eta_GK*(epsilon_C0_GammaKhat + epsilon_dC_GammaKhat + q_loc_projection)/M_GK^2",
            "claim_policy": "no local-GR/PPN claim unless q_loc and GK coupling residuals are theorem-zero or source-backed numeric and bounded",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["double_zero_attempt"], double_zero_attempt_rows)
write_csv(OUTPUTS["sector_status"], sector_status_rows)
write_csv(OUTPUTS["component_runner"], component_runner_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["double_zero_attempt"], BRANCH_OUTPUTS["double_zero_attempt_copy"])
copy_csv(OUTPUTS["sector_status"], BRANCH_OUTPUTS["sector_status_copy"])
copy_csv(OUTPUTS["component_runner"], BRANCH_OUTPUTS["component_runner_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3063 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["double_zero_attempt"],
    OUTPUTS["sector_status"],
    OUTPUTS["component_runner"],
    OUTPUTS["claim_status"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
    *BRANCH_OUTPUTS.values(),
]

all_output_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_output_rows.extend(rows(path))

generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
formalization_generated_hits = [path for path in generated_paths if FORMALIZATION.exists() and under(path, FORMALIZATION)]
dotg_rows_after = rows(DOTG_TARGET)

all_proof_unsigned = all(row["proof_signed"] == "false" for row in double_zero_attempt_rows)
sector_rows_nonclaim = all(row["proof_signed"] == "false" and row["valid_for_claim"] == "false" for row in sector_status_rows)
component_rows_nonclaim = all(row["ready_for_numeric_run"] == "false" and row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in component_runner_rows)
component_missing_markers = all("MISSING" in row["missing_numeric_inputs"] or "MISSING" in row["candidate_value"] for row in component_runner_rows)
all_claims_inactive = all(str(row["claim_active"]).lower() == "false" for row in claim_rows)
has_gk_next = "GammaKhat" in next_rows[0]["next_checkpoint"] or "GammaKhat" in next_rows[0]["script"]

validation_rows = [
    base({"validation_id": "VAL3063_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3063_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3063_02_double_zero_unsigned", "passed": all_proof_unsigned, "requirement": "double-zero proof remains unsigned while clauses are open", "evidence": OUTPUTS["double_zero_attempt"].name}),
    base({"validation_id": "VAL3063_03_sector_rows_nonclaim", "passed": sector_rows_nonclaim and len(sector_status_rows) >= 5, "requirement": "sector status rows are nonclaim and cover the inventory", "evidence": OUTPUTS["sector_status"].name}),
    base({"validation_id": "VAL3063_04_component_runner_nonclaim", "passed": component_rows_nonclaim and component_missing_markers, "requirement": "component-bound runner rows are schema-only with missing-input markers", "evidence": OUTPUTS["component_runner"].name}),
    base({"validation_id": "VAL3063_05_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3063_06_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3063" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3063 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3063_07_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3063_08_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3063_09_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3063_10_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3064-") and has_gk_next, "requirement": "next target selects Gamma/Khat/q_loc double-zero proof or GK component runner", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3063_11_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3063 - Extra-Field Double-Zero Proof or Delta kST Component Bound Runner

Status: `Y5_R2FR_3063_extra_double_zero_not_signed_Delta_kST_component_runner_schema_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3063 tries the ambitious route:

`Delta_extra_linear = 0`

by proving a shared extra-field double-zero theorem:

`C_X(Phi0)=0`, `D_A C_X(Phi0)=0`, `D_A V_X(Phi0)=0`, positive/gapped operator, and boundary/projector silence in the same observed branch.

That theorem is **not signed** by the current corpus. The status matrix still contains `not_signed`, `open`, `candidate_only`, and `conditional` rows. So 3063 does not promote extra silence into a local-GR claim.

Instead, it builds the nonclaim component runner:

`abs(Delta_kST) <= sum_i abs(Delta_i)`

with no-cancellation policy and explicit missing-input markers. This is useful because it tells us exactly which coefficients must be derived or bounded next.

## Double-Zero Proof Attempt

{md_table(double_zero_attempt_rows, ["clause_id", "clause", "required_signature", "current_status", "proof_signed", "would_buy", "blocking_gap"])}

## Extra Sector Status

{md_table(sector_status_rows, ["sector_id", "parent_sector", "C0_status", "dC_status", "gap_or_closure_status", "boundary_status", "double_zero_passes", "feeds_Delta_kST", "priority"])}

## Delta kST Component Bound Runner

{md_table(component_runner_rows, ["component_id", "Delta_component", "sector", "residual_symbols", "bound_formula", "candidate_value", "missing_numeric_inputs", "ready_for_numeric_run"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "parse_ok", "row_count", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "row_count", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3063 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: extra double-zero not signed; Delta_kST component runner schema nonclaim")
