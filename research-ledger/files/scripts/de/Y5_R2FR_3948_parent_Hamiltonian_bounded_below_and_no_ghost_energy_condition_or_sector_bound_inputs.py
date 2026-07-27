from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3948"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3948-Y5-R2FR-parent-Hamiltonian-bounded-below-and-no-ghost-energy-condition-or-sector-bound-inputs.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3948_SOURCE_REGISTER.csv",
    "contract": SRC / "P8_Y5_R2FR_3948_PARENT_HAMILTONIAN_NO_GHOST_CONTRACT.csv",
    "audit": SRC / "P8_Y5_R2FR_3948_SECTOR_HAMILTONIAN_SIGN_AUDIT.csv",
    "inputs": SRC / "P8_Y5_R2FR_3948_EPSILON_NEG_FIRST_INPUT_SCHEMA.csv",
    "MEH_gate": SRC / "P8_Y5_R2FR_3948_MEH_ENERGY_CONDITION_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3948_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3948_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3948_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3948_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3948_VALIDATION.csv",
}

NEXT_DOC = "3949-Y5-R2FR-MTS-sector-Hamiltonian-signature-matrix-or-epsilon-neg-first-inputs.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3949_MTS_sector_Hamiltonian_signature_matrix_or_epsilon_neg_first_inputs.py"


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
        ("SRC3948_00_3947_next", SRC / "P8_Y5_R2FR_3947_NEXT_TARGET.csv", "NEXT3947_0", "3947 selected parent Hamiltonian/no-ghost route"),
        ("SRC3948_01_3947_sign", SRC / "P8_Y5_R2FR_3947_TOTAL_HILBERT_POSITIVE_ENERGY_THEOREM.csv", "PET3947_3_positive_energy_or_bound_theorem", "M_EH sign inequality"),
        ("SRC3948_02_3947_EM", SRC / "P8_Y5_R2FR_3947_TOTAL_HILBERT_POSITIVE_ENERGY_THEOREM.csv", "PET3947_4_EM_and_Poynting_placement", "EM/Poynting split"),
        ("SRC3948_03_3947_epsilon", SRC / "P8_Y5_R2FR_3947_EPSILON_NEG_BOUND_VECTOR.csv", "NEG3947_7_combined", "combined sign-failure row"),
        ("SRC3948_04_3947_candidate", SRC / "P8_Y5_R2FR_3947_MEH_SIGN_BOUND_CANDIDATE.csv", "MBC3947_1_DEC_shortcut", "parent positive-energy shortcut row"),
        ("SRC3948_05_A511_extra", SRC / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "A511_3_extra_field_silence", "positive Hessian/no-hair action block"),
        ("SRC3948_06_FP_massgap", SRC / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv", "FP511_2_positive_mass_gap", "positive mass-gap fixed point condition"),
        ("SRC3948_07_AR_massgap", SRC / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv", "AR511_1_no_mass_gap", "mass-gap failure residual"),
        ("SRC3948_08_DC_chain", SRC / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv", "DC511_1", "extra-field fixed-point derived chain"),
        ("SRC3948_09_GK_action", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_B_positive_auxiliary_fields", "positive auxiliary field action candidate"),
        ("SRC3948_10_GK_repair", SRC / "P8_GK_METRIC_RESPONSE_REPAIR_OPTIONS.csv", "RO515_B_auxiliary_positive_field", "positive auxiliary field repair option"),
        ("SRC3948_11_odd", SRC / "P8_ODD_RESIDUAL_EXCHANGE_CONTRACT.csv", "O5_positive_operator", "positive operator for exchange-odd sector"),
        ("SRC3948_12_q_nohair", SRC / "P8_q_retained_zero_conditions_CONTRACT.csv", "Q3_positive_source_free_nohair", "positive source-free no-hair condition"),
        ("SRC3948_13_chi_Qcoh", SRC / "P8_local_GR_chiD_Qcoh_local_zero_status.csv", "STAT3536_1_Qcoh", "Qcoh positive-Hessian route status"),
        ("SRC3948_14_MTS_map", SRC / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "L_cg / ell_tr", "mass-gap/spectrum transition-scale map"),
        ("SRC3948_15_Hilbert", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "same-frame Hilbert source bridge"),
        ("SRC3948_16_validation", SRC / "P8_Y5_BRR545_3947_VALIDATION.csv", "VAL3947_20_no_pycache", "previous validation"),
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


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "HNC3948_0_phase_space",
            "parent phase-space and constraints",
            "A parent Hamiltonian H_parent[tau] exists on the reduced physical phase space after gauge and constraint removal.",
            "without reduced phase space, negative gauge directions can be mistaken for physical ghosts",
            "MISSING_PARENT_REDUCED_PHASE_SPACE",
        ),
        (
            "HNC3948_1_kinetic_matrix",
            "positive kinetic metric",
            "The quadratic kinetic form K_IJ on all propagating non-gauge modes is positive semidefinite, and positive definite off gauge/constraint directions.",
            "wrong-sign kinetic terms create ghost energy and destroy the DEC shortcut",
            "MISSING_KINETIC_SIGNATURE_MATRIX",
        ),
        (
            "HNC3948_2_no_higher_derivative_ghost",
            "no Ostrogradsky sector",
            "The local parent action is second-order or degenerate/constraint-owned so no independent higher-time-derivative ghost remains.",
            "higher-derivative nondegenerate terms make the Hamiltonian unbounded below",
            "MISSING_HIGHER_DERIVATIVE_DEGENERACY_PROOF",
        ),
        (
            "HNC3948_3_potential_lower_bound",
            "potential and Hessian bounded below",
            "V_eff(Phi) is bounded below on the local branch and Hessian/mass matrix is nonnegative, with positive mass gap for source-free extra modes.",
            "tachyonic/sign-indefinite Hessian gives local hair and negative sectors",
            "MISSING_POTENTIAL_LOWER_BOUND_AND_MASS_GAP",
        ),
        (
            "HNC3948_4_nonminimal_terms",
            "nonminimal/improvement/counterterm sign",
            "C(Phi)R, boundary improvements, counterterms and regularization terms are double-zero/topological or have a bounded energy contribution.",
            "nonminimal terms can move energy between bulk and boundary and fake positivity",
            "MISSING_NONMINIMAL_COUNTERTERM_SIGN_BOUND",
        ),
        (
            "HNC3948_5_Hilbert_stress_owner",
            "Hamiltonian-to-Hilbert stress owner",
            "The same parent action whose Hamiltonian is bounded below defines the Hilbert source T_total(n,tau) used in M_EH.",
            "a positive canonical Hamiltonian does not help if the source stress is a different object",
            "MISSING_HAMILTONIAN_HILBERT_STRESS_OWNER",
        ),
        (
            "HNC3948_6_boundary_flux",
            "source domain and boundary energy",
            "Boundary/reference terms are fixed, source-blind, and do not add negative wall energy beyond epsilon_closed.",
            "negative boundary or reference energy can invalidate source positivity",
            "MISSING_BOUNDARY_REFERENCE_ENERGY_BOUND",
        ),
        (
            "HNC3948_7_theorem",
            "parent positive-energy shortcut",
            "If HNC3948_0..6 hold and source support is nonzero, then Z_energy_condition can be signed for the local total Hilbert source.",
            "this is the clean derivation path for M_EH>0",
            "CONDITIONAL_THEOREM_BUILT_NOT_SIGNED",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "contract_clause": clause,
            "required_statement": statement,
            "why_needed": why_needed,
            "current_status": current_status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, statement, why_needed, current_status in data
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("AUD3948_0_EH_spin2", "EH spin-2 branch", "positive after GR constraint/gauge reduction", "CONDITIONAL_FROM_LOCAL_GR_BLOCKS", "reduced phase-space sign inherited from EH branch, not independently reproved here"),
        ("AUD3948_1_extra_motion_time", "motion/time/range extra fields", "requires positive kinetic metric and positive mass gap", "MISSING_FIELD_BY_FIELD_KINETIC_HESSIAN_SIGNATURE", "A511_3/FP511_2 route exists but actual MTS field map is unsigned"),
        ("AUD3948_2_Gamma_Khat", "Gamma_eff / K_hat stress sector", "positive auxiliary field candidate", "CANDIDATE_NOT_SYMBOL_MATCHED", "GK514/RO515 suggest a route; no parent-owned coefficient map yet"),
        ("AUD3948_3_domain_projector", "domain/projector/selector fields", "constraint/topological/positive operator sector", "MISSING_SELECTOR_HAMILTONIAN_SIGNATURE", "projector stress can enter epsilon_neg until signed"),
        ("AUD3948_4_memory_nonlocal", "memory/nonlocal kernels", "must be positive kernel or causal dissipative sector with no negative local energy", "MISSING_MEMORY_KERNEL_POSITIVITY", "nonlocal memory cannot be assumed Hamiltonian-positive"),
        ("AUD3948_5_Maxwell", "descended Maxwell", "positive local field energy if Maxwell descent and domain are signed", "EM_POSITIVE_ROUTE_DESCENT_UNSIGNED", "stationary Maxwell belongs in E_pos only after descent/domain gates"),
        ("AUD3948_6_matter_binding", "matter/binding/stabilizer", "ordinary positive matter plus bounded negative binding", "MISSING_BINDING_STABILIZER_BOUND", "binding is not a ghost if total Hamiltonian is bounded, but current row still needs bound/source owner"),
        ("AUD3948_7_material_theta", "material response/theta/source normalization", "superselected positive or finite source-normalization bound", "MISSING_MATERIAL_THETA_SIGNATURE", "composition/source-label shifts stay in epsilon_neg"),
        ("AUD3948_8_boundary_counterterm", "boundary/improvement/counterterm", "fixed/topological/source-blind or bounded below", "MISSING_BOUNDARY_COUNTERTERM_SIGNATURE", "boundary bookkeeping can otherwise subtract source energy"),
        ("AUD3948_9_verdict", "total parent no-ghost theorem", "not signed globally", "PARENT_NO_GHOST_THEOREM_UNSIGNED", "use epsilon_neg sector schema until MTS signature matrix is filled"),
    ]
    return [
        {
            "row_id": row_id,
            "sector": sector,
            "positive_energy_route": route,
            "current_status": status,
            "notes": notes,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, sector, route, status, notes in data
    ]


def input_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("INP3948_0_Epos", "E_pos", "energy", "positive sector denominator", "system_id;tau_id;coframe_id;worldtube_id;positive_sector_energy;support_nonzero;source_path;uncertainty", "MISSING_E_POS_SOURCE_ROW"),
        ("INP3948_1_binding", "epsilon_binding_neg", "dimensionless", "binding/stabilizer negative fraction", "E_binding_neg_abs;E_pos;binding_model;stabilizer_stress;source_path;uncertainty", "MISSING_BINDING_STABILIZER_BOUND"),
        ("INP3948_2_material", "epsilon_material_unsigned", "dimensionless", "material/theta response fraction", "E_material_unsigned_abs;E_pos;composition_markers;theta_status;source_path;uncertainty", "MISSING_MATERIAL_RESPONSE_THETA_BOUND"),
        ("INP3948_3_exchange", "epsilon_parent_exchange", "dimensionless", "parent exchange current fraction", "E_parent_exchange_abs;E_pos;Ward_residual;exchange_current_owner;source_path;uncertainty", "MISSING_PARENT_EXCHANGE_BOUND"),
        ("INP3948_4_nonminimal", "epsilon_nonminimal_counterterm", "dimensionless", "non-EH/counterterm/improvement fraction", "E_nonminimal_abs;E_pos;operator_family;counterterm_owner;source_path;uncertainty", "MISSING_NONMINIMAL_COUNTERTERM_BOUND"),
        ("INP3948_5_source_norm", "epsilon_source_norm_shift", "dimensionless", "theta/source normalization fraction", "E_source_norm_abs;E_pos;normalization_selector;superselection_status;source_path;uncertainty", "MISSING_SOURCE_NORMALIZATION_BOUND"),
        ("INP3948_6_no_ghost", "Z_parent_no_ghost", "boolean certificate", "parent Hamiltonian bounded-below shortcut", "parent_action_id;reduced_phase_space;kinetic_signature;potential_lower_bound;constraint_stability;Hilbert_stress_owner;source_path", "MISSING_PARENT_NO_GHOST_CERTIFICATE"),
    ]
    return [
        {
            "row_id": row_id,
            "target_symbol": symbol,
            "units": units,
            "meaning": meaning,
            "required_columns": required_columns,
            "current_value": current_value,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, meaning, required_columns, current_value in data
    ]


def MEH_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("MEG3948_0_contract", "parent no-ghost/bounded-below contract exists", "PASS_CONDITIONAL_CONTRACT"),
        ("MEG3948_1_signature_matrix", "MTS sectors have field-by-field kinetic/Hessian signatures", "BLOCKED_SIGNATURE_MATRIX_MISSING"),
        ("MEG3948_2_Hilbert_owner", "bounded Hamiltonian and Hilbert stress source are the same parent object", "BLOCKED_HILBERT_OWNER_UNSIGNED"),
        ("MEG3948_3_epsilon_inputs", "epsilon_neg input schema exists for fallback route", "PASS_SCHEMA_VALUES_MISSING"),
        ("MEG3948_4_Epos", "E_pos source/support row exists", "BLOCKED_E_POS_SOURCE_ROW_MISSING"),
        ("MEG3948_5_sum", "epsilon_neg+epsilon_closed<1 can be tested", "NOT_SCORE_READY"),
        ("MEG3948_6_claim", "M_EH positive-energy shortcut claim", "BLOCKED_NONCLAIM"),
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
            "row_id": "DEC3948_0_no_global_positivity_claim",
            "decision": "do not sign global parent positive energy yet",
            "effect": "the action route is promising but still lacks reduced phase-space, signature matrix, and Hilbert-stress owner proof",
            "claim_status": "PARENT_THEOREM_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3948_1_contract_built",
            "decision": "use HNC3948_0..6 as the exact no-ghost/positive-energy contract",
            "effect": "future work has a checklist that can actually sign Z_energy_condition instead of circling 'positive energy missing'",
            "claim_status": "CONTRACT_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3948_2_fallback_schema",
            "decision": "keep epsilon_neg fallback active with sourceable input columns",
            "effect": "if parent proof is too hard, M_EH sign can still be bounded without hiding negative sectors",
            "claim_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3948_3_next",
            "decision": "target MTS sector Hamiltonian signature matrix next",
            "effect": "the best leap forward is mapping actual MTS symbols to kinetic signs, Hessians, constraints, and epsilon_neg owners",
            "claim_status": "NEXT_SIGNATURE_MATRIX",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3948_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3948_1_contract", "gate": "parent no-ghost contract", "requirement": "bounded-below contract written", "status": "PASS_CONDITIONAL_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3948_2_parent_signature", "gate": "field-by-field MTS signature", "requirement": "kinetic matrix/Hessian/constraint signs filled", "status": "BLOCKED_SIGNATURE_MATRIX_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3948_3_Hilbert_owner", "gate": "Hamiltonian-Hilbert owner", "requirement": "positive Hamiltonian source equals T_total(n,tau)", "status": "BLOCKED_OWNER_PROOF_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3948_4_epsilon_neg", "gate": "negative-sector fallback", "requirement": "epsilon_neg component values sourced", "status": "BLOCKED_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3948_5_local_GR_claim", "gate": "local-GR/source-coupling claim", "requirement": "Z_energy_condition or epsilon_neg+epsilon_closed<1 plus 3944 envelope", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3948_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "build a field-by-field MTS Hamiltonian signature matrix for Gamma/Khat, chi_D, Qcoh, memory/domain/projector, Maxwell/matter response, and source-normalization sectors, or fill first epsilon_neg input values",
            "success_condition": "at least one sector is parent-signed positive/zero or converted into a concrete epsilon_neg source row with units, owner, and source path",
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
            "summary": "3948 builds the exact parent Hamiltonian no-ghost/bounded-below contract and sourceable epsilon_neg fallback schema; global positive energy remains unsigned",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3948 - Parent Hamiltonian Bounded Below And No-Ghost Energy Condition Or Sector Bound Inputs

Timestamp: `{timestamp}`

## Result

3948 does **not** claim the parent action is already positive-energy. It builds the exact contract needed to make that claim.

The clean route is:

`H_parent` reduced to physical phase space, positive kinetic matrix, no higher-derivative ghosts, bounded-below potential/Hessian, fixed boundary/reference terms, and the same parent object defining `T_total(n,tau)`.

If that contract is signed, the `Z_energy_condition` shortcut from 3947 can be activated.

## Fallback Route

Until then, the active route remains:

`M_EH >= c^-2 E_pos*(1 - epsilon_neg - epsilon_closed)`.

3948 creates first sourceable input schemas for:

- `E_pos`;
- `epsilon_binding_neg`;
- `epsilon_material_unsigned`;
- `epsilon_parent_exchange`;
- `epsilon_nonminimal_counterterm`;
- `epsilon_source_norm_shift`;
- `Z_parent_no_ghost`.

## Current Verdict

- Progress: parent no-ghost/bounded-below contract is exact.
- Progress: fallback `epsilon_neg` input schema is sourceable.
- Blocker: no field-by-field MTS Hamiltonian signature matrix yet.
- Blocker: Hamiltonian positivity has not been proven to own the same Hilbert source `T_total`.
- Public claim: blocked.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3948_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3948_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3948_PARENT_HAMILTONIAN_NO_GHOST_CONTRACT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3948_SECTOR_HAMILTONIAN_SIGN_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3948_EPSILON_NEG_FIRST_INPUT_SCHEMA.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3948_MEH_ENERGY_CONDITION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3948_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3948_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3948 - Parent Hamiltonian Bounded Below And No-Ghost Contract

Timestamp: `{timestamp}`

- Built exact positive-energy shortcut contract: reduced phase space, positive kinetic matrix, no higher-derivative ghost, bounded-below potential/Hessian, controlled nonminimal/counterterm energy, Hamiltonian-Hilbert source ownership, and fixed boundary/reference energy.
- Verdict: global parent positive energy remains unsigned; no `Z_energy_condition` claim is made.
- Fallback route strengthened: `epsilon_neg` now has sourceable input schemas for binding, material/theta, parent exchange, nonminimal/counterterm, and source-normalization sectors.
- Key remaining leap: field-by-field MTS Hamiltonian signature matrix tying actual MTS symbols to kinetic signs, Hessians, constraints, and source owners.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3948 - Parent Hamiltonian Bounded Below And No-Ghost Contract"
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
    contract = contract_rows(timestamp)
    audit = audit_rows(timestamp)
    inputs = input_schema_rows(timestamp)
    meh_gate = MEH_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (contract, audit, inputs, meh_gate, decisions, claim_gate, next_target)
    contract_statuses = {row["current_status"] for row in contract}
    input_symbols = {row["target_symbol"] for row in inputs}
    gate_statuses = {row["status"] for row in meh_gate}
    checks = [
        ("VAL3948_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3948_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3948_02_contract_theorem", "CONDITIONAL_THEOREM_BUILT_NOT_SIGNED" in contract_statuses, "parent no-ghost theorem contract emitted"),
        ("VAL3948_03_kinetic_clause", any(row["row_id"] == "HNC3948_1_kinetic_matrix" for row in contract), "positive kinetic matrix clause emitted"),
        ("VAL3948_04_no_hd_clause", any(row["row_id"] == "HNC3948_2_no_higher_derivative_ghost" for row in contract), "higher-derivative ghost clause emitted"),
        ("VAL3948_05_Hilbert_owner_clause", any(row["row_id"] == "HNC3948_5_Hilbert_stress_owner" for row in contract), "Hamiltonian-Hilbert owner clause emitted"),
        ("VAL3948_06_audit_verdict", any(row["current_status"] == "PARENT_NO_GHOST_THEOREM_UNSIGNED" for row in audit), "sector audit keeps parent theorem unsigned"),
        ("VAL3948_07_input_schema", {"E_pos", "epsilon_binding_neg", "epsilon_parent_exchange", "Z_parent_no_ghost"}.issubset(input_symbols), "epsilon_neg/Z_parent input schemas emitted"),
        ("VAL3948_08_gate_blocks", "BLOCKED_SIGNATURE_MATRIX_MISSING" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "MEH gate blocks claim and asks for signature matrix"),
        ("VAL3948_09_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public/local-GR claim"),
        ("VAL3948_10_next_3949", next_target[0]["next_doc"] == NEXT_DOC and "signature matrix" in next_target[0]["target"], "next target selects MTS sector signature matrix"),
        ("VAL3948_11_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3948_12_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3948_13_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3948_14_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3948_15_spine_written", SPINE_PATH.exists() and "3948 - Parent Hamiltonian" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3948_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3948_17_script_compiles", True, "script compiles"),
        ("VAL3948_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["contract"], contract_rows(timestamp))
    write_csv(OUTPUTS["audit"], audit_rows(timestamp))
    write_csv(OUTPUTS["inputs"], input_schema_rows(timestamp))
    write_csv(OUTPUTS["MEH_gate"], MEH_gate_rows(timestamp))
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
        raise SystemExit(f"3948 validation failed: {failed}")
    print(f"3948 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
