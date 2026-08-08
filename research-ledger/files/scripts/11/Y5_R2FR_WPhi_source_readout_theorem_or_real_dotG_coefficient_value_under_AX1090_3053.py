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

CHECKPOINT = "3053"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3053-Y5-R2FR-WPhi-source-readout-theorem-or-real-dotG-coefficient-value-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3053_00_3052_doc": ROOT / "3052-Y5-R2FR-source-frame-readout-lock-for-Gref-WPhi-or-dotG-numeric-coefficient-runner-under-AX1090.md",
    "SRC3053_01_3052_readout_gates": RESIDUALS / "P8_Y5_R2FR_3052_READOUT_LOCK_GATE_EVALUATION.csv",
    "SRC3053_02_3052_aw_status": RESIDUALS / "P8_Y5_R2FR_3052_AW_NEWTON_LOCK_STATUS.csv",
    "SRC3053_03_3052_dotg_runner": RESIDUALS / "P8_Y5_R2FR_3052_DOTG_NUMERIC_COEFFICIENT_RUNNER_RESULTS.csv",
    "SRC3053_04_3052_next": RESIDUALS / "P8_Y5_R2FR_3052_NEXT_TARGET.csv",
    "SRC3053_05_3050_spine": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
    "SRC3053_06_3050_gref": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "SRC3053_07_3042_WPhi": PARENT_ACTION / "W_equals_Phi_parent_readout_theorem_3042_NOT_SIGNED.csv",
    "SRC3053_08_3040_single_potential": PARENT_ACTION / "single_potential_readout_theorem_3040_CONDITIONAL_NOT_SIGNED.csv",
    "SRC3053_09_3041_parent_metric": PARENT_ACTION / "parent_metric_readout_signature_audit_3041_NOT_SIGNED.csv",
    "SRC3053_10_3036_source_lock": PARENT_ACTION / "source_readout_lock_theorem_attempt_3036_NOT_SIGNED.csv",
    "SRC3053_11_3037_minimum_lock": PARENT_ACTION / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
    "SRC3053_12_3038_source_normal": PARENT_ACTION / "common_source_functional_normal_form_3038_NOT_SIGNED.csv",
    "SRC3053_13_3045_aw_law": RESIDUALS / "P8_Y5_R2FR_3045_AW_COEFFICIENT_RATIO_LAW.csv",
    "SRC3053_14_3045_coeff_map": PARENT_ACTION / "linear_source_normalization_coefficient_map_3045_NOT_SIGNED.csv",
    "SRC3053_15_dotg_target": DOTG_TARGET,
    "SRC3053_16_2933_dotg_bound": RESIDUALS / "P8_Y5_R2FR_2933_COUPLING_BOUND_SOURCE_ACQUISITION.csv",
    "SRC3053_17_2933_dotg_projection": PARENT_ACTION / "DotG_to_kappa_projection_gate_2933_NONCLAIM.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3053_SOURCE_REGISTER.csv",
    "wphi_theorem": RESIDUALS / "P8_Y5_R2FR_3053_WPHI_UNIQUENESS_THEOREM_ATTEMPT.csv",
    "hilbert_audit": RESIDUALS / "P8_Y5_R2FR_3053_HILBERT_SOURCE_READOUT_AUDIT.csv",
    "premise_gates": RESIDUALS / "P8_Y5_R2FR_3053_PREMISE_SIGNATURE_GATES.csv",
    "dotg_requirement": RESIDUALS / "P8_Y5_R2FR_3053_DOTG_REAL_VALUE_REQUIREMENT.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3053_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3053_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3053_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3053_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3053_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "wphi_theorem_copy": PARENT_ACTION / "WPhi_uniqueness_theorem_attempt_3053_CONDITIONAL_NOT_SIGNED.csv",
    "hilbert_audit_copy": PARENT_ACTION / "Hilbert_source_readout_audit_3053_NOT_SIGNED.csv",
    "premise_gates_copy": PARENT_ACTION / "WPhi_premise_signature_gates_3053_NOT_SIGNED.csv",
    "dotg_requirement_copy": LOCAL_BOUNDS / "dotG_real_value_requirement_3053_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3053_W_DEFINITION_PARENT_OWNER_OR_DOTG_COEFFICIENT_NEXT_NONCLAIM.csv",
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
        "signed_for_current_MTS",
        "gate_passes_for_current_MTS",
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


dotg_rows_before = rows(DOTG_TARGET)

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

wphi_theorem_rows = [
    base(
        {
            "theorem_id": "WPHI3053_0_metric_phi_poisson",
            "theorem_piece": "metric weak-field potential",
            "premise": "the observed metric branch has g_00=-1+2*Phi_metric/c^2 and G_ref := kappa_eff*c^4/(8*pi)",
            "derivation": "linear weak-field limit of G_munu=kappa_eff*T_munu gives nabla^2 Phi_metric = 4*pi*G_ref*rho_obs",
            "result": "Phi_metric is the observed metric Poisson potential if the 3050 G_ref/readout branch is active",
            "current_status": "CONDITIONAL_FROM_3050_NOT_ACTIVE",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_ACTIVE_PARENT_READOUT_FRAME; MISSING_PARENT_SIGNATURE_FOR_WEAK_FIELD_BRANCH",
            "source_path": str(SOURCE_PATHS["SRC3053_06_3050_gref"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3053_1_W_parent_definition",
            "theorem_piece": "W source definition",
            "premise": "W is parent-owned as the solution of nabla^2 W = 4*pi*G_ref*rho_obs on the same local domain",
            "derivation": "this is a required parent definition/adoption clause, not something obtained from data fitting",
            "result": "W and Phi_metric obey the same elliptic equation only if this definition is signed",
            "current_status": "MISSING_PARENT_OWNED_W_DEFINITION",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_W_DEFINITION_IN_PARENT_ACTION; MISSING_NO_ORBITAL_IMPORT_CERTIFICATE",
            "source_path": str(SOURCE_PATHS["SRC3053_07_3042_WPhi"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3053_2_uniqueness_step",
            "theorem_piece": "elliptic uniqueness",
            "premise": "Phi_metric and W share the same operator, source density, coefficient, domain and boundary/asymptotic data",
            "derivation": "Delta := W-Phi_metric then satisfies nabla^2 Delta = 0 with zero boundary/asymptotic data; maximum principle gives Delta=0",
            "result": "W = Phi_metric",
            "current_status": "MATH_VALID_IF_PREMISES_SIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_SAME_SOURCE_DENSITY; MISSING_SAME_BOUNDARY_DATA; MISSING_NO_SECOND_SOURCE_CHANNEL",
            "source_path": str(SOURCE_PATHS["SRC3053_13_3045_aw_law"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3053_3_second_channel_guard",
            "theorem_piece": "no hidden W-channel",
            "premise": "the parent action contains no independent W source coefficient, residual source term, disformal representative term or orbital-calibrated denominator",
            "derivation": "otherwise W-Phi_metric is sourced or rescaled and uniqueness no longer yields equality",
            "result": "A_W cannot be hidden in an extra readout coefficient",
            "current_status": "UNSIGNED_GUARD",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_NO_REPRESENTATIVE_W_COEFFICIENT; MISSING_BOUNDARY_LOCAL_PROJECTION_SILENCE",
            "source_path": str(SOURCE_PATHS["SRC3053_14_3045_coeff_map"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3053_4_verdict",
            "theorem_piece": "WPhi theorem verdict",
            "premise": "all prior WPhi premises are parent-signed",
            "derivation": "same Poisson problem plus elliptic uniqueness",
            "result": "conditional theorem shape is good, but current MTS cannot claim W=Phi_metric yet",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_OWNED_W_DEFINITION; MISSING_HILBERT_SOURCE_READOUT_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3053_01_3052_readout_gates"]),
        }
    ),
]

hilbert_audit_rows = [
    base(
        {
            "audit_id": "HS3053_0_minimal_matter_metric",
            "readout_clause": "S_matter = S_matter[g_obs, psi] with no independent W, kappa, species, clock or orbital metric",
            "why_needed": "only then does the observed source for the weak-field equation come from the same functional that clocks and matter follow",
            "mathematical_result": "T_obs_munu := -2/sqrt(-g_obs) * delta S_matter[g_obs,psi]/delta g_obs^munu",
            "current_status": "STANDARD_IF_ADOPTED_NOT_PARENT_SIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_MATTER_ACTION_DESCENT",
            "source_path": str(SOURCE_PATHS["SRC3053_10_3036_source_lock"]),
        }
    ),
    base(
        {
            "audit_id": "HS3053_1_nonrelativistic_source",
            "readout_clause": "rho_obs is the nonrelativistic limit of T_obs_00/c^2 in the same observed frame",
            "why_needed": "Poisson source density must not be imported from an orbital or fitted mass convention after the fact",
            "mathematical_result": "nabla^2 Phi_metric = 4*pi*G_ref*rho_obs uses the Hilbert-source density",
            "current_status": "CONDITIONAL_ONLY",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_SOURCE_DENSITY_DESCENT; MISSING_OBSERVED_FRAME_CERTIFICATE",
            "source_path": str(SOURCE_PATHS["SRC3053_12_3038_source_normal"]),
        }
    ),
    base(
        {
            "audit_id": "HS3053_2_no_species_charge",
            "readout_clause": "all matter species couple to the same g_obs and no composition label enters G_ref or W",
            "why_needed": "otherwise local Newton recovery immediately becomes WEP-sensitive and must be bounded instead of derived",
            "mathematical_result": "source universality is a theorem premise, not an empirical patch",
            "current_status": "UNSIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_UNIVERSAL_MATTER_COUPLING_SIGNATURE",
            "source_path": str(SOURCE_PATHS["SRC3053_11_3037_minimum_lock"]),
        }
    ),
    base(
        {
            "audit_id": "HS3053_3_same_frame_clocks_orbits_sources",
            "readout_clause": "g_obs := g_matter := g_source := g_clock := g_orbit",
            "why_needed": "Newtonian orbits, clock readout, source mass and metric Phi must use the same frame before A_W can be called one",
            "mathematical_result": "removes frame-source drift from A_W and dln_Geff_dt",
            "current_status": "CONDITIONAL_CLAUSE_EXISTS_NOT_ACTIVE",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_ACTIVE_PARENT_SINGLE_FRAME_GATE",
            "source_path": str(SOURCE_PATHS["SRC3053_01_3052_readout_gates"]),
        }
    ),
    base(
        {
            "audit_id": "HS3053_4_verdict",
            "readout_clause": "Hilbert source readout for observed Newtonian matter",
            "why_needed": "without it, W=Phi can still be symbolically neat but physically unowned",
            "mathematical_result": "T_obs readout is acceptable as a parent contract but not yet a signed MTS theorem",
            "current_status": "NOT_SIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_SOURCE_READOUT_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3053_10_3036_source_lock"]),
        }
    ),
]

premise_gate_rows = [
    base(
        {
            "gate_id": "GATE3053_0_same_observed_frame",
            "requirement": "one observed metric/coframe for matter, source, clocks, orbits and weak-field Phi",
            "proof_value": "prevents frame drift and readout denominators",
            "current_status": "BLOCKED_NOT_ACTIVE",
            "gate_passes_for_current_MTS": "false",
            "blocker": "single-frame/coframe adoption is conditional only",
            "source_path": str(SOURCE_PATHS["SRC3053_01_3052_readout_gates"]),
        }
    ),
    base(
        {
            "gate_id": "GATE3053_1_W_parent_owner",
            "requirement": "W is parent-defined as the same local Poisson/metric potential, not an empirical orbital helper",
            "proof_value": "turns W=Phi_metric from an axiom into a uniqueness theorem premise",
            "current_status": "BLOCKED_MISSING_PARENT_OWNER",
            "gate_passes_for_current_MTS": "false",
            "blocker": "W definition is not signed in the parent action",
            "source_path": str(SOURCE_PATHS["SRC3053_07_3042_WPhi"]),
        }
    ),
    base(
        {
            "gate_id": "GATE3053_2_same_source_coefficient",
            "requirement": "both W and Phi_metric use 4*pi*G_ref as source coefficient",
            "proof_value": "forces A_W = kappa_eff*c^4/(8*pi*G_ref)",
            "current_status": "CONDITIONAL_GREF_LOCK_NOT_ACTIVE",
            "gate_passes_for_current_MTS": "false",
            "blocker": "G_ref lock exists as candidate but readout activation remains unsigned",
            "source_path": str(SOURCE_PATHS["SRC3053_06_3050_gref"]),
        }
    ),
    base(
        {
            "gate_id": "GATE3053_3_same_source_density",
            "requirement": "rho_obs for W equals the Hilbert-source density sourcing Phi_metric",
            "proof_value": "prevents hidden source rescaling",
            "current_status": "BLOCKED_SOURCE_DESCENT_UNSIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "Hilbert source readout remains a contract, not a theorem",
            "source_path": str(SOURCE_PATHS["SRC3053_10_3036_source_lock"]),
        }
    ),
    base(
        {
            "gate_id": "GATE3053_4_same_boundary_data",
            "requirement": "W and Phi_metric share local boundary/asymptotic data after the same normalization",
            "proof_value": "lets harmonic uniqueness collapse W-Phi_metric to zero",
            "current_status": "UNSIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "boundary/local projection silence is not parent-proven",
            "source_path": str(SOURCE_PATHS["SRC3053_13_3045_aw_law"]),
        }
    ),
    base(
        {
            "gate_id": "GATE3053_5_no_second_channel",
            "requirement": "no independent W residual, representative Weyl/disformal term or source-channel coefficient survives",
            "proof_value": "prevents W=Phi from failing by a hidden sourced residual",
            "current_status": "UNSIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "no-second-channel guard not derived",
            "source_path": str(SOURCE_PATHS["SRC3053_14_3045_coeff_map"]),
        }
    ),
    base(
        {
            "gate_id": "GATE3053_6_hilbert_source",
            "requirement": "T_obs is exactly the Hilbert variation of S_matter[g_obs,psi]",
            "proof_value": "ties source density to the parent action rather than fitted mass bookkeeping",
            "current_status": "BLOCKED_NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "matter action descent remains unsigned",
            "source_path": str(SOURCE_PATHS["SRC3053_12_3038_source_normal"]),
        }
    ),
    base(
        {
            "gate_id": "GATE3053_7_dotg_real_value_fallback",
            "requirement": "if WPhi/Hilbert gates fail, provide a real numeric or theorem-zero dln_Geff_dt coefficient",
            "proof_value": "lets local coupling branch be bounded instead of handwaved",
            "current_status": "BLOCKED_NO_REAL_VALUE",
            "gate_passes_for_current_MTS": "false",
            "blocker": "current dotG rows are placeholders and must not be scored",
            "source_path": str(SOURCE_PATHS["SRC3053_15_dotg_target"]),
        }
    ),
]

dotg_requirement_rows = [
    base(
        {
            "requirement_id": "DOTGREQ3053_0_existing_rows_audit",
            "target_file": str(DOTG_TARGET),
            "current_row_count": len(dotg_rows_before),
            "requirement": "do not append another placeholder dotG row",
            "accepted_value_form": "numeric yr^-1 parent prediction, or a parent theorem forcing zero",
            "current_status": "PLACEHOLDERS_PRESENT_NO_3053_APPEND",
            "valid_for_claim": "false",
            "reason": "3052 already proved the runner blocks on missing numeric coefficients",
        }
    ),
    base(
        {
            "requirement_id": "DOTGREQ3053_1_real_coefficient_contract",
            "target_file": str(DOTG_TARGET),
            "current_row_count": len(dotg_rows_before),
            "requirement": "derive dln_Geff_dt = D_t ln(kappa_eff*c^4/(8*pi)) + D_t ln Z_readout in the observed frame",
            "accepted_value_form": "explicit numeric coefficient with units yr^-1 and source path for every term",
            "current_status": "MISSING_PARENT_SCALAR_KAPPA_OR_ZERO_THEOREM",
            "valid_for_claim": "false",
            "reason": "no parent dynamics currently provide D_t kappa_eff or Z_readout drift",
        }
    ),
    base(
        {
            "requirement_id": "DOTGREQ3053_2_zero_theorem_contract",
            "target_file": str(DOTG_TARGET),
            "current_row_count": len(dotg_rows_before),
            "requirement": "if topological kappa route is adopted, prove d kappa_eff = 0 and D_t ln Z_readout = 0 locally",
            "accepted_value_form": "derived zero with source-frame theorem path",
            "current_status": "PARTIAL_DKAPPA_CANDIDATE_READOUT_ZERO_UNSIGNED",
            "valid_for_claim": "false",
            "reason": "topological d kappa_eff candidate exists but readout-source frame theorem is unsigned",
        }
    ),
    base(
        {
            "requirement_id": "DOTGREQ3053_3_bound_inversion_guard",
            "target_file": str(DOTG_TARGET),
            "current_row_count": len(dotg_rows_before),
            "requirement": "external dotG/G bound must not be used as the MTS prediction",
            "accepted_value_form": "prediction first, empirical comparator second",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": "false",
            "reason": "a bound can reject or constrain a coefficient, but cannot define it",
        }
    ),
    base(
        {
            "requirement_id": "DOTGREQ3053_4_verdict",
            "target_file": str(DOTG_TARGET),
            "current_row_count": len(dotg_rows_before),
            "requirement": "real dotG fallback if WPhi theorem cannot be signed",
            "accepted_value_form": "not available in current corpus",
            "current_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "false",
            "reason": "next branch should own W in the parent action before inventing a numeric drift coefficient",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3053_0_WPhi",
            "claim": "W = Phi_metric is proven for current MTS",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "uniqueness proof is valid only if unsigned parent premises are adopted",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3053_1_Hilbert_source",
            "claim": "T_obs Hilbert source readout is active",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "S_matter[g_obs,psi] descent and single-frame matter coupling are not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3053_2_AW",
            "claim": "A_W=1 and Newton normalization are claimable",
            "status": "NO_BLOCKED_BY_PREMISE_GATES",
            "claim_active": "false",
            "reason": "W/Phi/source/G_ref gates do not pass for current MTS",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3053_3_dotG",
            "claim": "dln_Geff_dt has a scored real value",
            "status": "NO_REAL_VALUE",
            "claim_active": "false",
            "reason": "3053 refuses another placeholder coefficient",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3053_4_local_GR",
            "claim": "local GR/Newton recovery is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "the readout theorem has been sharpened but not signed",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3053_0_theorem_shape",
            "question": "Can W=Phi_metric be derived rather than assumed?",
            "answer": "YES_CONDITIONALLY",
            "reason": "if W and Phi_metric are the same Poisson problem with the same source, coefficient and boundary data, uniqueness forces equality",
            "action": "record conditional theorem but do not claim it for current MTS",
        }
    ),
    base(
        {
            "decision_id": "DEC3053_1_current_claim",
            "question": "Does current MTS sign the theorem premises?",
            "answer": "NO",
            "reason": "W parent ownership, Hilbert source density, no-second-channel and same-boundary clauses remain unsigned",
            "action": "keep A_W/Newton/local-GR inactive",
        }
    ),
    base(
        {
            "decision_id": "DEC3053_2_dotg_fallback",
            "question": "Can 3053 fill a real dotG coefficient?",
            "answer": "NO",
            "reason": "the corpus contains bounds and placeholder rows, not a parent-predicted coefficient or theorem-zero readout drift",
            "action": "do not append placeholder; require parent coefficient derivation",
        }
    ),
    base(
        {
            "decision_id": "DEC3053_3_next",
            "question": "Best next attack?",
            "answer": "OWN_W_IN_PARENT_ACTION_FIRST",
            "reason": "this is less speculative than guessing a dotG number and directly attacks the local GR/Newton hinge",
            "action": "build 3054 W-definition parent owner or dotG parent coefficient derivation",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3053_0_3054",
            "next_checkpoint": "3054-Y5-R2FR-W-definition-parent-owner-or-dotG-parent-coefficient-derivation-under-AX1090.md",
            "script": "scripts/Y5_R2FR_W_definition_parent_owner_or_dotG_parent_coefficient_derivation_under_AX1090_3054.py",
            "mission": "try to parent-own W as the unique observed weak-field metric potential; if that fails, derive a real parent dln_Geff_dt coefficient rather than adding placeholders",
            "starting_equation": "W=Phi_metric follows if both are the same Poisson problem with the same Hilbert source, G_ref coefficient, domain and boundary data",
            "claim_policy": "no Newton/local-GR claim until the W owner and Hilbert-source gates are parent-signed or a real dotG coefficient is scored",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["wphi_theorem"], wphi_theorem_rows)
write_csv(OUTPUTS["hilbert_audit"], hilbert_audit_rows)
write_csv(OUTPUTS["premise_gates"], premise_gate_rows)
write_csv(OUTPUTS["dotg_requirement"], dotg_requirement_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["wphi_theorem"], BRANCH_OUTPUTS["wphi_theorem_copy"])
copy_csv(OUTPUTS["hilbert_audit"], BRANCH_OUTPUTS["hilbert_audit_copy"])
copy_csv(OUTPUTS["premise_gates"], BRANCH_OUTPUTS["premise_gates_copy"])
copy_csv(OUTPUTS["dotg_requirement"], BRANCH_OUTPUTS["dotg_requirement_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3053 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["wphi_theorem"],
    OUTPUTS["hilbert_audit"],
    OUTPUTS["premise_gates"],
    OUTPUTS["dotg_requirement"],
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

validation_rows = [
    base({"validation_id": "VAL3053_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3053_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3053_02_wphi_theorem_conditional", "passed": any(row["theorem_id"] == "WPHI3053_2_uniqueness_step" for row in wphi_theorem_rows) and wphi_theorem_rows[-1]["current_status"] == "CONDITIONAL_NOT_SIGNED", "requirement": "W=Phi uniqueness theorem is derived only conditionally", "evidence": OUTPUTS["wphi_theorem"].name}),
    base({"validation_id": "VAL3053_03_hilbert_audit_not_signed", "passed": len(hilbert_audit_rows) >= 5 and all(row["signed_for_current_MTS"] == "false" for row in hilbert_audit_rows), "requirement": "Hilbert source readout audit exists and remains unsigned", "evidence": OUTPUTS["hilbert_audit"].name}),
    base({"validation_id": "VAL3053_04_premise_gates_block", "passed": len(premise_gate_rows) >= 8 and all(row["gate_passes_for_current_MTS"] == "false" for row in premise_gate_rows), "requirement": "all theorem premise gates block current claims", "evidence": OUTPUTS["premise_gates"].name}),
    base({"validation_id": "VAL3053_05_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3053" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3053 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3053_06_dotg_requirement_nonclaim", "passed": all(str(row["valid_for_claim"]).lower() == "false" for row in dotg_requirement_rows), "requirement": "dotG real-value requirement remains nonclaim", "evidence": OUTPUTS["dotg_requirement"].name}),
    base({"validation_id": "VAL3053_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active/signature flags"}),
    base({"validation_id": "VAL3053_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "all 3053 claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3053_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3053_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3053_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3053_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3054-"), "requirement": "next target selects W parent owner or real dotG parent coefficient", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3053_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3053 - WPhi Source-Readout Theorem or Real dotG Coefficient Value

Status: `Y5_R2FR_3053_WPhi_uniqueness_conditional_source_readout_unsigned_dotG_real_value_missing_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3053 gets a real mathematical foothold:

`nabla^2 Phi_metric = 4*pi*G_ref*rho_obs`

`nabla^2 W = 4*pi*G_ref*rho_obs`

If both equations are parent-owned in the same observed frame, with the same Hilbert source density and the same boundary/asymptotic data, then:

`Delta := W - Phi_metric`

`nabla^2 Delta = 0`

with zero boundary/asymptotic data, so elliptic uniqueness gives:

`W = Phi_metric`

That is the good news. The bad news is precise: current MTS still has not signed the parent-owned W definition, Hilbert source readout, no-second-channel guard, or boundary/local projection silence. So 3053 proves the shape of the theorem, not the active local-GR claim.

The fallback dotG path is also kept honest: no new placeholder was appended. A real row must be a numeric parent prediction in `yr^-1`, or a theorem-zero for both `d kappa_eff` and readout drift.

## WPhi Uniqueness Theorem Attempt

{md_table(wphi_theorem_rows, ["theorem_id", "theorem_piece", "premise", "derivation", "result", "current_status", "missing_for_claim"])}

## Hilbert Source Readout Audit

{md_table(hilbert_audit_rows, ["audit_id", "readout_clause", "why_needed", "mathematical_result", "current_status", "missing_for_claim"])}

## Premise Signature Gates

{md_table(premise_gate_rows, ["gate_id", "requirement", "proof_value", "current_status", "gate_passes_for_current_MTS", "blocker"])}

## dotG Real-Value Requirement

{md_table(dotg_requirement_rows, ["requirement_id", "requirement", "accepted_value_form", "current_status", "valid_for_claim", "reason"])}

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
    raise SystemExit(f"3053 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: WPhi theorem conditional; Hilbert source unsigned; dotG real value missing nonclaim")
