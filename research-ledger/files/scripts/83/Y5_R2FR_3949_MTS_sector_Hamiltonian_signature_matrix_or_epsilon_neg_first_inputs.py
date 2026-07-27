from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3949"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3949-Y5-R2FR-MTS-sector-Hamiltonian-signature-matrix-or-epsilon-neg-first-inputs.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3949_SOURCE_REGISTER.csv",
    "matrix": SRC / "P8_Y5_R2FR_3949_MTS_HAMILTONIAN_SIGNATURE_MATRIX.csv",
    "epsilon_rows": SRC / "P8_Y5_R2FR_3949_EPSILON_NEG_SECTOR_INPUT_ROWS.csv",
    "promotion": SRC / "P8_Y5_R2FR_3949_SECTOR_PROMOTION_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3949_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3949_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3949_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3949_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3949_VALIDATION.csv",
}

NEXT_DOC = "3950-Y5-R2FR-Gamma-Khat-positive-auxiliary-signature-or-epsilon-nonminimal-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3950_Gamma_Khat_positive_auxiliary_signature_or_epsilon_nonminimal_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3949_00_3948_next", SRC / "P8_Y5_R2FR_3948_NEXT_TARGET.csv", "NEXT3948_0", "3948 selected MTS sector signature matrix target"),
        ("SRC3949_01_3948_contract", SRC / "P8_Y5_R2FR_3948_PARENT_HAMILTONIAN_NO_GHOST_CONTRACT.csv", "HNC3948_1_kinetic_matrix", "positive kinetic matrix contract"),
        ("SRC3949_02_3948_audit_GK", SRC / "P8_Y5_R2FR_3948_SECTOR_HAMILTONIAN_SIGN_AUDIT.csv", "AUD3948_2_Gamma_Khat", "Gamma/Khat sector audit"),
        ("SRC3949_03_3948_schema", SRC / "P8_Y5_R2FR_3948_EPSILON_NEG_FIRST_INPUT_SCHEMA.csv", "INP3948_6_no_ghost", "parent no-ghost input schema"),
        ("SRC3949_04_3947_bound", SRC / "P8_Y5_R2FR_3947_TOTAL_HILBERT_POSITIVE_ENERGY_THEOREM.csv", "PET3947_3_positive_energy_or_bound_theorem", "M_EH sign-bound theorem"),
        ("SRC3949_05_symbol_map_GK", SRC / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "Gamma_eff", "MTS symbol map for Gamma_eff"),
        ("SRC3949_06_symbol_map_scale", SRC / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "L_cg / ell_tr", "MTS symbol map for transition scale"),
        ("SRC3949_07_FV_GK", SRC / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv", "FV512_2_Gamma_Khat_q", "first-variation gate for Gamma/Khat/q_loc"),
        ("SRC3949_08_FV_domain", SRC / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv", "FV512_3_domain_selector", "first-variation gate for domain selector"),
        ("SRC3949_09_KK_GK", SRC / "P8_MTS_SYMBOL_KEEP_KILL_RULES.csv", "KK512_2_Gamma_Khat", "keep/kill rule for Gamma/Khat"),
        ("SRC3949_10_KK_memory", SRC / "P8_MTS_SYMBOL_KEEP_KILL_RULES.csv", "KK512_4_memory", "keep/kill rule for memory"),
        ("SRC3949_11_decision", SRC / "P8_MTS_SYMBOL_MATCH_DECISION.csv", "D512_1", "prior symbol-match decision"),
        ("SRC3949_12_GK_action", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_B_positive_auxiliary_fields", "positive auxiliary field candidate"),
        ("SRC3949_13_GK_repair", SRC / "P8_GK_METRIC_RESPONSE_REPAIR_OPTIONS.csv", "RO515_B_auxiliary_positive_field", "Gamma/Khat repair route"),
        ("SRC3949_14_chi_Qcoh", SRC / "P8_local_GR_chiD_Qcoh_local_zero_status.csv", "STAT3536_1_Qcoh", "chi/Qcoh local-zero status"),
        ("SRC3949_15_q_nohair", SRC / "P8_q_retained_zero_conditions_CONTRACT.csv", "Q3_positive_source_free_nohair", "positive source-free no-hair condition"),
        ("SRC3949_16_validation", SRC / "P8_Y5_BRR545_3948_VALIDATION.csv", "VAL3948_18_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:900]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SIG3949_0_metric", "g_obs/g_readout", "EH spin-2/readout metric", "A511_0_EH_core;A511_6_metric_readout", "GR_REDUCED_PHASE_SPACE_POSITIVE_CONDITIONAL", "not applicable except constraints", "second order", "baseline_positive_conditional", "not epsilon_neg", "CONDITIONAL_BASELINE_NOT_FULL_MTS_PROOF"),
        ("SIG3949_1_kappa", "kappa_eff/A_3", "topological coupling sector", "A511_1_kappa_topological", "NO_PROPAGATING_KINETIC_IF_TOPOLOGICAL", "constraint fixes d kappa=0", "topological first order constraint", "zero local energy if adopted", "source_norm_shift if not adopted", "CONDITIONAL_ZERO_ROUTE"),
        ("SIG3949_2_Gamma_Khat", "Gamma_eff/K_hat/q_loc", "local residual stress/connection sector", "A511_3_extra_field_silence;A511_5_boundary_reference", "MISSING_GK_KINETIC_SIGNATURE", "MISSING_GK_HESSIAN_OR_BOUNDARY_EXACTNESS", "candidate second order/boundary", "positive auxiliary candidate only", "epsilon_nonminimal_counterterm", "CONCRETE_EPSILON_ROW_REQUIRED"),
        ("SIG3949_3_domain_projector", "chi_D/Qcoh/u/h/X/P_loc", "domain/projector/selector sector", "A511_4_domain_projector_selector", "MISSING_SELECTOR_CONSTRAINT_SIGNATURE", "conditional local-zero but parent unsigned", "algebraic/constraint preferred; kinetic dangerous", "zero if algebraic constraint signed", "epsilon_parent_exchange", "CONCRETE_EPSILON_ROW_REQUIRED"),
        ("SIG3949_4_memory", "memory/B_mem/U_mem/I_M", "memory/nonlocal activation sector", "A511_3_extra_field_silence;A511_4_domain_projector_selector", "MISSING_MEMORY_KERNEL_SIGNATURE", "MISSING_POSITIVE_KERNEL_OR_DOUBLE_ZERO", "nonlocal/auxiliary unknown", "positive kernel or double-zero needed", "epsilon_material_unsigned", "CONCRETE_EPSILON_ROW_REQUIRED"),
        ("SIG3949_5_mass_projector", "Pi_M/Q_M/M_eff/M_source", "mass projector/source charge readout", "A511_6_metric_readout;worldtube source-measure glue", "not propagating field", "first variation must vanish", "projector/readout", "zero if Pi_M=Pi_EH and dPi_M=0", "epsilon_source_norm_shift", "CONCRETE_EPSILON_ROW_REQUIRED"),
        ("SIG3949_6_Maxwell", "A_mu/F_mu_nu/T_EM", "descended Maxwell field stress", "A511_2_universal_matter;3906 Maxwell bridge", "POSITIVE_IF_MAXWELL_DESCENT_SIGNED", "no tachyon for Maxwell; domain still needed", "second order gauge with constraints", "E_pos if descent/domain signed", "epsilon_closed not epsilon_neg for flux", "POSITIVE_ROUTE_DESCENT_UNSIGNED"),
        ("SIG3949_7_matter_binding", "matter/binding/stabilizer", "ordinary matter plus binding support", "A511_2_universal_matter;3821 total stress", "ordinary positive matter plus bounded binding", "virial/closed total source needed", "matter EFT", "E_pos plus epsilon_binding_neg", "epsilon_binding_neg", "CONCRETE_EPSILON_ROW_REQUIRED"),
        ("SIG3949_8_material_theta", "theta/material/source labels", "material response and source normalization", "source normalization/superselection sector", "MISSING_THETA_SIGNATURE", "missing material response descent", "algebraic/material EFT", "zero if source-normalization superselected", "epsilon_material_unsigned;epsilon_source_norm_shift", "CONCRETE_EPSILON_ROW_REQUIRED"),
        ("SIG3949_9_boundary_counterterm", "boundary/reference/counterterm", "boundary and improvement energy", "A511_5_boundary_reference", "not propagating if fixed/topological", "fixed/source-blind or bounded below", "boundary/exact/topological", "zero or bounded if fixed branch signed", "epsilon_nonminimal_counterterm;epsilon_closed", "CONCRETE_EPSILON_ROW_REQUIRED"),
        ("SIG3949_10_transition_scale", "L_cg/ell_tr", "activation/transition scale", "FP511_8 local-cosmology transition control", "not direct Hamiltonian field unless promoted", "derive from mass-gap/spectrum/source compactness", "derived scale", "no energy if derived parameter", "unification branch-switch residual", "OPEN_DERIVED_SCALE_ROUTE"),
    ]
    return [
        {
            "row_id": row_id,
            "MTS_symbols": symbols,
            "sector": sector,
            "action_placement": action_placement,
            "kinetic_signature": kinetic,
            "Hessian_or_gap_status": hessian,
            "derivative_order": derivative_order,
            "positive_energy_route": route,
            "epsilon_neg_bucket": bucket,
            "current_status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbols, sector, action_placement, kinetic, hessian, derivative_order, route, bucket, status in data
    ]


def epsilon_input_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("EPN3949_0_GK_nonminimal", "epsilon_nonminimal_counterterm", "Gamma_eff/K_hat/q_loc", "|E_GK_unsigned + E_Khat_boundary_unsigned|/E_pos", "dimensionless", "P8_GK_STRESS_ACTION_CANDIDATES.csv;P8_GK_METRIC_RESPONSE_REPAIR_OPTIONS.csv", "GK514/RO515 positive auxiliary candidate", "MISSING_GK_COEFFICIENTS_AND_SIGN_MATRIX"),
        ("EPN3949_1_domain_projector", "epsilon_parent_exchange", "chi_D/Qcoh/u/h/X/P_loc", "|E_selector_stress + E_projector_exchange|/E_pos", "dimensionless", "P8_local_GR_chiD_Qcoh_local_zero_status.csv;P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv", "domain-selector local-zero conditional route", "MISSING_SELECTOR_SIGNATURE_AND_LOCAL_ZERO_OWNER"),
        ("EPN3949_2_memory_kernel", "epsilon_material_unsigned", "memory/B_mem/U_mem/I_M", "|E_memory_unsigned|/E_pos", "dimensionless", "P8_MTS_SYMBOL_KEEP_KILL_RULES.csv;P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "memory must be action-owned double-zero/positive kernel", "MISSING_MEMORY_KERNEL_POSITIVITY"),
        ("EPN3949_3_mass_projector", "epsilon_source_norm_shift", "Pi_M/Q_M/M_eff/M_source", "|delta E_source_norm_or_projector|/E_pos", "dimensionless", "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv;P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv", "dressed Hamiltonian/Noether charge route", "MISSING_PIM_FIRST_VARIATION_ZERO"),
        ("EPN3949_4_binding", "epsilon_binding_neg", "matter/binding/stabilizer", "|E_binding_neg + E_stabilizer_unsigned|/E_pos", "dimensionless", "P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv;P8_Y5_R2FR_3820_PRESSURE_BINDING_CORRECTION_LAW.csv", "closed total-system stress/virial route", "MISSING_BINDING_STABILIZER_BOUND"),
        ("EPN3949_5_theta_material", "epsilon_material_unsigned", "theta/material/source labels", "|E_material_theta_unsigned|/E_pos", "dimensionless", "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv;P8_Y5_R2FR_3777_EM_FIELD_ENERGY_SOURCE_MAP.csv", "material response/source-label descent route", "MISSING_MATERIAL_THETA_SOURCE_BOUND"),
    ]
    return [
        {
            "row_id": row_id,
            "target_symbol": symbol,
            "sector_owner": owner,
            "formula": formula,
            "units": units,
            "source_paths": source_paths,
            "owner_route": owner_route,
            "current_value": current_value,
            "row_type": "CONCRETE_EPSILON_NEG_SOURCE_ROW_NONNUMERIC",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, owner, formula, units, source_paths, owner_route, current_value in data
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PRO3949_0_matrix_exists", "MTS sector signature matrix covers main local-GR sectors", "PASS_PRIVATE_MATRIX"),
        ("PRO3949_1_positive_sector", "at least one sector can be parent-signed positive/zero", "CONDITIONAL_ONLY_NO_PUBLIC_CLAIM"),
        ("PRO3949_2_epsilon_rows", "unsigned sectors converted to source-owned epsilon_neg rows", "PASS_NONNUMERIC_ROWS"),
        ("PRO3949_3_GK", "Gamma/Khat/q_loc promoted positive or bounded", "BLOCKED_GK_SIGNATURE_MISSING"),
        ("PRO3949_4_selector", "chi/Qcoh/domain selector promoted positive/zero or bounded", "BLOCKED_SELECTOR_SIGNATURE_MISSING"),
        ("PRO3949_5_memory", "memory kernel promoted positive/double-zero or bounded", "BLOCKED_MEMORY_KERNEL_MISSING"),
        ("PRO3949_6_MEH", "M_EH sign test can score", "NOT_SCORE_READY"),
        ("PRO3949_7_claim", "local GR/source-coupling claim", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3949_0_matrix_built",
            "decision": "use a field-by-field MTS Hamiltonian signature matrix as the active no-ghost interface",
            "effect": "positive-energy work now targets concrete MTS symbols instead of abstract parent-action clauses",
            "claim_status": "PRIVATE_MATRIX_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3949_1_epsilon_rows",
            "decision": "convert unsigned high-risk sectors into concrete nonnumeric epsilon_neg rows",
            "effect": "Gamma/Khat, selector, memory, Pi_M, binding, and theta/material sectors now have units, owners, formulas, and source paths",
            "claim_status": "BOUND_INPUT_ROWS_CREATED_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3949_2_next",
            "decision": "attack Gamma/Khat first",
            "effect": "it is the central local residual sector and has the strongest positive-auxiliary candidate route from GK514/RO515",
            "claim_status": "NEXT_GK_SIGNATURE_OR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3949_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3949_1_matrix", "gate": "MTS sector matrix", "requirement": "main MTS local-GR sectors mapped to Hamiltonian signature status", "status": "PASS_PRIVATE_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3949_2_epsilon_rows", "gate": "epsilon_neg source rows", "requirement": "unsigned sectors have owner/formula/unit/source-path rows", "status": "PASS_NONNUMERIC_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3949_3_no_ghost", "gate": "parent no-ghost theorem", "requirement": "field-by-field signs filled and Hamiltonian-Hilbert ownership proved", "status": "BLOCKED_SIGNATURE_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3949_4_MEH", "gate": "M_EH sign test", "requirement": "E_pos and epsilon_neg+epsilon_closed<1 or parent Z_energy_condition", "status": "BLOCKED_NOT_SCORE_READY", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3949_5_local_GR", "gate": "local-GR/source-coupling claim", "requirement": "M_EH sign plus local residual envelope below bounds", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3949_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "try to derive the Gamma_eff/K_hat/q_loc sector from a positive auxiliary action with kinetic/Hessian signs and Hilbert-stress ownership, or convert it into the first epsilon_nonminimal_counterterm bound row",
            "success_condition": "Gamma/Khat either gets a parent-owned positive signature and double-zero/local no-hair condition, or EPN3949_0 gains a concrete bound/value-ready row with units, owner, and source path",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3949 builds the first field-by-field MTS Hamiltonian signature matrix and converts unsigned sectors into concrete nonnumeric epsilon_neg source rows",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3949 - MTS Sector Hamiltonian Signature Matrix Or Epsilon-Neg First Inputs

Timestamp: `{timestamp}`

## Result

3949 builds the first field-by-field Hamiltonian signature matrix for the local-GR source-energy route.

It maps actual MTS sectors:

- `Gamma_eff/K_hat/q_loc`;
- `chi_D/Qcoh/u/h/X/P_loc`;
- `memory/B_mem/U_mem/I_M`;
- `Pi_M/Q_M/M_eff/M_source`;
- Maxwell, matter/binding, material/theta, boundary/counterterm and transition scale sectors.

## Main Advance

Unsigned sectors now have concrete nonnumeric `epsilon_neg` rows with:

- target symbol;
- sector owner;
- formula;
- units;
- source paths;
- owner route;
- current missing value.

That means the next work can derive or fill a sector instead of repeating “missing positive energy.”

## Current Verdict

- Progress: MTS sector signature matrix exists.
- Progress: high-risk sectors are converted into bound-input rows.
- Blocker: no sector beyond conditional EH/topological routes is public-claim positive yet.
- Blocker: `Gamma_eff/K_hat/q_loc` remains the central unresolved local residual.
- Public claim: blocked.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3949_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3949_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3949_MTS_HAMILTONIAN_SIGNATURE_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3949_EPSILON_NEG_SECTOR_INPUT_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3949_SECTOR_PROMOTION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3949_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3949_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3949 - MTS Sector Hamiltonian Signature Matrix

Timestamp: `{timestamp}`

- Built the first field-by-field MTS Hamiltonian signature matrix for local-GR source-energy positivity.
- Covered sectors: `g_obs`, `kappa/A_3`, `Gamma_eff/K_hat/q_loc`, `chi_D/Qcoh/u/h/X/P_loc`, memory, `Pi_M/Q_M`, Maxwell, matter/binding, material/theta, boundary/counterterm, and `L_cg/ell_tr`.
- Converted unsigned high-risk sectors into concrete nonnumeric `epsilon_neg` rows with formulas, units, owners, source paths, and missing-value status.
- Key unresolved sector: `Gamma_eff/K_hat/q_loc`, because it carries the central local residual and has the best positive-auxiliary candidate route.
- Claim status: private nonclaim; matrix is an attack surface, not proof of local GR.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3949 - MTS Sector Hamiltonian Signature Matrix"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matrix = matrix_rows(timestamp)
    epsilon_rows = epsilon_input_rows(timestamp)
    promotion = promotion_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (matrix, epsilon_rows, promotion, decisions, claim_gate, next_target)
    matrix_symbols = " ".join(row["MTS_symbols"] for row in matrix)
    epsilon_symbols = {row["target_symbol"] for row in epsilon_rows}
    promotion_statuses = {row["status"] for row in promotion}
    concrete_rows = [row for row in epsilon_rows if row["row_type"] == "CONCRETE_EPSILON_NEG_SOURCE_ROW_NONNUMERIC" and row["units"] and row["source_paths"]]
    checks = [
        ("VAL3949_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3949_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3949_02_matrix_size", len(matrix) >= 10, "signature matrix has broad sector coverage"),
        ("VAL3949_03_matrix_GK", "Gamma_eff/K_hat/q_loc" in matrix_symbols, "Gamma/Khat/q_loc sector included"),
        ("VAL3949_04_matrix_domain", "chi_D/Qcoh" in matrix_symbols, "domain/Qcoh sector included"),
        ("VAL3949_05_matrix_memory", "memory/B_mem" in matrix_symbols, "memory sector included"),
        ("VAL3949_06_matrix_Maxwell", "A_mu/F_mu_nu/T_EM" in matrix_symbols, "Maxwell sector included"),
        ("VAL3949_07_epsilon_rows", len(concrete_rows) >= 6 and {"epsilon_nonminimal_counterterm", "epsilon_parent_exchange", "epsilon_material_unsigned", "epsilon_source_norm_shift", "epsilon_binding_neg"}.issubset(epsilon_symbols), "concrete nonnumeric epsilon rows emitted"),
        ("VAL3949_08_epsilon_GK", any(row["row_id"] == "EPN3949_0_GK_nonminimal" for row in epsilon_rows), "Gamma/Khat epsilon row emitted"),
        ("VAL3949_09_promotion_gate", "PASS_PRIVATE_MATRIX" in promotion_statuses and "BLOCKED_NONCLAIM" in promotion_statuses, "promotion gate passes private matrix and blocks claim"),
        ("VAL3949_10_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public/local-GR claim"),
        ("VAL3949_11_next_3950", next_target[0]["next_doc"] == NEXT_DOC and "Gamma_eff" in next_target[0]["target"], "next target selects Gamma/Khat"),
        ("VAL3949_12_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3949_13_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3949_14_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3949_15_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3949_16_spine_written", SPINE_PATH.exists() and "3949 - MTS Sector Hamiltonian" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3949_17_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3949_18_script_compiles", True, "script compiles"),
        ("VAL3949_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["matrix"], matrix_rows(timestamp))
    write_csv(OUTPUTS["epsilon_rows"], epsilon_input_rows(timestamp))
    write_csv(OUTPUTS["promotion"], promotion_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3949 validation failed: {failed}")
    print(f"3949 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
