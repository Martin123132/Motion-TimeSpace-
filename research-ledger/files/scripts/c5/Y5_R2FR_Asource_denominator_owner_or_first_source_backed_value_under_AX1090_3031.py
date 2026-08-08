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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3031"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3031-Y5-R2FR-Asource-denominator-owner-or-first-source-backed-value-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3031_00_3030_doc": ROOT / "3030-Y5-R2FR-clock-lapse-constraint-package-or-first-Asource-row-under-AX1090.md",
    "SRC3031_01_3030_asource_schema": RESIDUALS / "P8_Y5_R2FR_3030_ASOURCE_FIRST_ROW_SCHEMA.csv",
    "SRC3031_02_3030_validator": RESIDUALS / "P8_Y5_R2FR_3030_ASOURCE_ROW_VALIDATOR.csv",
    "SRC3031_03_3030_next": RESIDUALS / "P8_Y5_R2FR_3030_NEXT_TARGET.csv",
    "SRC3031_04_3022_psin_owner": RESIDUALS / "P8_Y5_R2FR_3022_PSIN_HAMILTONIAN_OWNER_AUDIT.csv",
    "SRC3031_05_3024_lambdan_map": RESIDUALS / "P8_Y5_R2FR_3024_LAMBDAN_CORE_COEFFICIENT_MAP.csv",
    "SRC3031_06_2921_source_mass": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
    "SRC3031_07_2921_pg_bridge": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3031_08_2923_source_template": RESIDUALS / "P8_Y5_R2FR_2923_SOURCE_MASS_ROW_TEMPLATE.csv",
    "SRC3031_09_2924_source_attempt": RESIDUALS / "P8_Y5_R2FR_2924_SOURCE_MASS_FIRST_ROW_ATTEMPT.csv",
    "SRC3031_10_2945_denominator": RESIDUALS / "P8_Y5_R2FR_2945_DENOMINATOR_BLOCKER_ROWS.csv",
    "SRC3031_11_2947_mhref_runner": RESIDUALS / "P8_Y5_R2FR_2947_MHREF_PIM_FIRST_ROW_RUNNER_ROWS.csv",
    "SRC3031_12_2947_import_guards": RESIDUALS / "P8_Y5_R2FR_2947_CHARGE_IMPORT_GUARDS.csv",
    "SRC3031_13_3006_htau_rows": RESIDUALS / "P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv",
    "SRC3031_14_3006_sector_charge": RESIDUALS / "P8_Y5_R2FR_3006_SECTOR_CHARGE_OWNER_ROWS.csv",
    "SRC3031_15_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3031_16_3008_coupling_guard": RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv",
    "SRC3031_17_3017_ward_attempt": RESIDUALS / "P8_Y5_R2FR_3017_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "SRC3031_18_hamiltonian_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "SRC3031_19_worldtube_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3031_SOURCE_REGISTER.csv",
    "ratio_theorem": RESIDUALS / "P8_Y5_R2FR_3031_ASOURCE_RATIO_THEOREM_ATTEMPT.csv",
    "denominator_audit": RESIDUALS / "P8_Y5_R2FR_3031_DENOMINATOR_OWNER_AUDIT.csv",
    "coefficient_rows": RESIDUALS / "P8_Y5_R2FR_3031_LINEAR_SOURCE_COEFFICIENT_ROWS.csv",
    "candidate_values": RESIDUALS / "P8_Y5_R2FR_3031_ASOURCE_CANDIDATE_VALUE_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3031_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3031_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3031_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3031_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3031_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "denominator_copy": PARENT_ACTION / "A_source_denominator_owner_audit_3031_NOT_SIGNED.csv",
    "ratio_copy": LOCAL_BOUNDS / "A_source_coefficient_ratio_law_3031_NONCLAIM.csv",
    "candidate_copy": LOCAL_BOUNDS / "A_source_candidate_value_rows_3031_NONCLAIM.csv",
    "coefficient_copy": LOCAL_BOUNDS / "linear_source_coefficient_rows_3031_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3031_LINEAR_SOURCE_COEFFICIENT_EQUALITY_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3031_00_3030_doc": "3030 handoff: A_source row staged and clock/lapse not signed",
    "SRC3031_01_3030_asource_schema": "strict A_source acquisition schema",
    "SRC3031_02_3030_validator": "A_source validator showing denominator/source bridge missing",
    "SRC3031_03_3030_next": "3031 target selection",
    "SRC3031_04_3022_psin_owner": "psi_N parent owner blocker",
    "SRC3031_05_3024_lambdan_map": "minimal Hcore/lambda_N coefficient relation",
    "SRC3031_06_2921_source_mass": "parent source-mass identity audit",
    "SRC3031_07_2921_pg_bridge": "Poisson/Gauss/orbital bridge audit",
    "SRC3031_08_2923_source_template": "source mass row acceptance template",
    "SRC3031_09_2924_source_attempt": "EH reference and MTS source-mass first row attempt",
    "SRC3031_10_2945_denominator": "denominator blocker rows",
    "SRC3031_11_2947_mhref_runner": "M_H_ref/PiM first-row runner requirements",
    "SRC3031_12_2947_import_guards": "no EH import, no orbital GM and no cancellation guards",
    "SRC3031_13_3006_htau_rows": "H_tau extraction and M_H_ref feed rows",
    "SRC3031_14_3006_sector_charge": "sector charge ownership matrix",
    "SRC3031_15_3007_grammar": "minimal parent action grammar",
    "SRC3031_16_3008_coupling_guard": "coupling guard rows",
    "SRC3031_17_3017_ward_attempt": "source-current Ward owner attempt",
    "SRC3031_18_hamiltonian_contract": "Hamiltonian source-measure contract",
    "SRC3031_19_worldtube_theorem": "worldtube source-measure theorem",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

ratio_theorem_rows = [
    base(
        {
            "theorem_id": "RATIO3031_0_setup",
            "statement": "compare psi_N and W/c^2 in the same local source-normalized branch",
            "mathematical_form": "L_loc psi_N = C_psiH rho_H + R_psi; L_loc(W/c^2)=C_WH rho_H + R_W",
            "premises": "same operator, same source density/current, same boundary class, compact support, residuals controlled",
            "result": "setup only",
            "status": "CONDITIONAL_FORMAL_SETUP",
            "passes_for_claim": False,
        }
    ),
    base(
        {
            "theorem_id": "RATIO3031_1_uniqueness",
            "statement": "if residuals vanish and boundary data agree, elliptic uniqueness fixes the ratio",
            "mathematical_form": "L_loc(psi_N - (C_psiH/C_WH) W/c^2)=0 with zero boundary data",
            "premises": "C_WH nonzero, same Green operator, no harmonic/source-shadow mode",
            "result": "psi_N=(C_psiH/C_WH) W/c^2 + O(W^2)",
            "status": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "passes_for_claim": False,
        }
    ),
    base(
        {
            "theorem_id": "RATIO3031_2_Asource_law",
            "statement": "A_source is not a free fit if both source coefficients are parent-owned",
            "mathematical_form": "A_source = C_psiH / C_WH",
            "premises": "C_psiH and C_WH are source-backed finite parent coefficients in the same frame",
            "result": "exact coefficient-ratio law",
            "status": "DERIVED_FORMULA_NONNUMERIC",
            "passes_for_claim": False,
        }
    ),
    base(
        {
            "theorem_id": "RATIO3031_3_unity_condition",
            "statement": "A_source=1 is allowed only as a theorem, not as a convention",
            "mathematical_form": "A_source=1 iff C_psiH=C_WH under the same source/boundary normalization",
            "premises": "parent action forces identical linear source coefficient for psi_N and W/c^2",
            "result": "unity condition isolated",
            "status": "UNITY_REQUIRES_COEFFICIENT_EQUALITY_NOT_SIGNED",
            "passes_for_claim": False,
        }
    ),
    base(
        {
            "theorem_id": "RATIO3031_4_current_verdict",
            "statement": "current corpus does not yet provide the numerator or denominator coefficient",
            "mathematical_form": "C_psiH=MISSING; C_WH=MISSING_PARENT_GREF_SOURCE_BRIDGE; A_source=MISSING",
            "premises": "3022, 2921, 2945, 3006, 3030 blockers remain active",
            "result": "ratio theorem retained, no claim",
            "status": "ASOURCE_RATIO_NOT_NUMERIC_OR_CLAIMABLE",
            "passes_for_claim": False,
        }
    ),
]

denominator_audit_rows = [
    base(
        {
            "audit_id": "DEN3031_0_theta_Qtau",
            "object": "theta_MTS/Q_tau^MTS",
            "required_condition": "one parent action supplies theta_MTS, Q_tau and constraint terms for all retained sectors",
            "current_status": "MISSING_PARENT_THETA_QTAU",
            "blocks": "H_tau, M_H_ref, C_WH",
            "evidence": "3006 HTE3006_0..3; 2947 RUN2947_0",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_1_MHref",
            "object": "M_H_ref",
            "required_condition": "M_H_ref=H_tau[S]-H_ref is positive, finite, same-frame and source-backed",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "blocks": "A_source denominator",
            "evidence": "3006 HTE3006_7; 2945 DEN2945_0; 2947 RUN2947_1",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_2_JH_Htau_bridge",
            "object": "J_H/H_tau/worldtube equality",
            "required_condition": "Hilbert source current, Hamiltonian charge and worldtube support are the same parent source object",
            "current_status": "MISSING_HILBERT_TO_HTAU_MAP",
            "blocks": "same source for C_psiH and C_WH",
            "evidence": "2921 PG2921_1; 2924 SMFA2924_2; 3006 SEC3006_8; HSM541_2",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_3_Gref",
            "object": "G_ref/kappa_MTS",
            "required_condition": "constant universal coupling with no source, species, range or frame drift",
            "current_status": "CONDITIONAL_ROUTE_NOT_PARENT_ADOPTED",
            "blocks": "C_WH and source-normalized W",
            "evidence": "2921 PG2921_7; 2945 DEN2945_5; HSM541_6",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_4_W_owner",
            "object": "W/c^2 source potential",
            "required_condition": "Poisson/Gauss equation for W is parent-owned before orbital readout",
            "current_status": "CONDITIONAL_FROM_EH_ONLY_PREMISES",
            "blocks": "C_WH",
            "evidence": "2921 PG2921_3..5; HSM541_5",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_5_psin_numerator",
            "object": "psi_N linear source equation",
            "required_condition": "parent Hcore/lapse variation gives L_loc psi_N = C_psiH rho_H with units and source path",
            "current_status": "MISSING_PARENT_ACTION_BLOCK",
            "blocks": "C_psiH",
            "evidence": "3022 PHO3022_1; 3024 ansatz conditional; 3030 clock/lapse package not signed",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_6_same_operator_boundary",
            "object": "operator and boundary equality",
            "required_condition": "psi_N and W/c^2 use the same L_loc, same branch boundary data and no harmonic mode",
            "current_status": "MISSING_OPERATOR_BOUNDARY_MATCH",
            "blocks": "ratio theorem promotion",
            "evidence": "3030 CPK3030_7; 2921 PSM2921_6; 3007 G3007_9",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_7_no_extra_source_channels",
            "object": "extra/source-shadow channels",
            "required_condition": "no boundary, projector, domain, memory, non-Hilbert or source-only prefactor contributes to C_psiH or C_WH",
            "current_status": "COUPLING_GUARD_NOT_CLOSED",
            "blocks": "source-normalized Newton and PPN followthrough",
            "evidence": "2921 PSM2921_7; 3008 CG3008_2..6; 3017 WARD3017_2..8",
            "passes_denominator": False,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_8_anti_circularity",
            "object": "no EH-only or orbital-GM import",
            "required_condition": "A_source is not set by GR reference charge, measured orbital GM, fitted H_ref or convention-only A_source=1",
            "current_status": "GUARD_PRESENT_VALUE_MISSING",
            "blocks": "claim promotion, not schema staging",
            "evidence": "2923 SMT2923_5; 2947 GUARD2947_0..4; 3030 ASR3030_1 rejected",
            "passes_denominator": True,
        }
    ),
    base(
        {
            "audit_id": "DEN3031_9_verdict",
            "object": "A_source denominator owner",
            "required_condition": "DEN3031_0 through DEN3031_8 all pass together",
            "current_status": "DENOMINATOR_OWNER_NOT_DERIVED",
            "blocks": "A_source numeric/source-backed value",
            "evidence": "aggregate 3031 denominator audit",
            "passes_denominator": False,
        }
    ),
]

coefficient_rows = [
    base(
        {
            "coefficient_id": "COEF3031_0_C_psiH",
            "symbol": "C_psiH",
            "definition": "source coefficient in L_loc psi_N = C_psiH rho_H + R_psi",
            "expected_units": "operator_units_per_mass_density",
            "numeric_value": "MISSING_C_PSIH",
            "source_path": str(SOURCE_PATHS["SRC3031_04_3022_psin_owner"]),
            "source_path_exists": SOURCE_PATHS["SRC3031_04_3022_psin_owner"].exists(),
            "status": "MISSING_PARENT_PSI_N_SOURCE_COEFFICIENT",
            "required_exit": "parent Hcore/lapse variation with source term and units",
        }
    ),
    base(
        {
            "coefficient_id": "COEF3031_1_C_WH",
            "symbol": "C_WH",
            "definition": "source coefficient in L_loc(W/c^2)=C_WH rho_H + R_W",
            "expected_units": "operator_units_per_mass_density",
            "numeric_value": "MISSING_C_WH",
            "source_path": str(SOURCE_PATHS["SRC3031_07_2921_pg_bridge"]),
            "source_path_exists": SOURCE_PATHS["SRC3031_07_2921_pg_bridge"].exists(),
            "status": "MISSING_PARENT_W_SOURCE_COEFFICIENT",
            "required_exit": "parent Poisson/Gauss bridge with G_ref and M_H_ref, not EH-only or orbital GM",
        }
    ),
    base(
        {
            "coefficient_id": "COEF3031_2_R_psi",
            "symbol": "R_psi",
            "definition": "nonlinear, boundary, frame, source-shadow or extra-sector residual in the psi_N equation",
            "expected_units": "same_as_Lpsi",
            "numeric_value": "MISSING_R_PSI_BOUND_OR_ZERO",
            "source_path": str(SOURCE_PATHS["SRC3031_16_3008_coupling_guard"]),
            "source_path_exists": SOURCE_PATHS["SRC3031_16_3008_coupling_guard"].exists(),
            "status": "MISSING_RESIDUAL_ZERO_OR_BOUND",
            "required_exit": "theorem-zero or finite residual row before ratio promotion",
        }
    ),
    base(
        {
            "coefficient_id": "COEF3031_3_R_W",
            "symbol": "R_W",
            "definition": "source-normalization residual in the W/c^2 Poisson/Gauss equation",
            "expected_units": "same_as_LW",
            "numeric_value": "MISSING_R_W_BOUND_OR_ZERO",
            "source_path": str(SOURCE_PATHS["SRC3031_06_2921_source_mass"]),
            "source_path_exists": SOURCE_PATHS["SRC3031_06_2921_source_mass"].exists(),
            "status": "MISSING_RESIDUAL_ZERO_OR_BOUND",
            "required_exit": "no extra source channels, radial hair, derivative hair or finite source-mass residual rows",
        }
    ),
    base(
        {
            "coefficient_id": "COEF3031_4_ratio",
            "symbol": "C_psiH_over_C_WH",
            "definition": "dimensionless coefficient ratio that equals A_source when residuals and boundary mismatch vanish",
            "expected_units": "dimensionless",
            "numeric_value": "MISSING_RATIO_NUMERIC",
            "source_path": str(OUTPUTS["ratio_theorem"]),
            "source_path_exists": True,
            "status": "FORMULA_DERIVED_NUMERIC_VALUE_MISSING",
            "required_exit": "finite C_psiH and C_WH with nonzero denominator or parent equality proof",
        }
    ),
]

candidate_value_rows = [
    base(
        {
            "candidate_id": "ASRC3031_0_ratio_law",
            "symbol": "A_source",
            "candidate_value": "C_psiH/C_WH",
            "derivation": "elliptic uniqueness on same source/operator/boundary branch",
            "status": "DERIVED_FORMULA_NONNUMERIC_NOT_CLAIM",
            "valid_if": "C_psiH, C_WH, R_psi, R_W, M_H_ref, G_ref and source bridge are parent-owned",
            "missing_for_claim": "MISSING_C_PSIH; MISSING_C_WH; MISSING_M_H_REF; MISSING_SOURCE_BRIDGE; MISSING_RESIDUAL_ZERO_OR_BOUND",
        }
    ),
    base(
        {
            "candidate_id": "ASRC3031_1_unity_condition",
            "symbol": "A_source",
            "candidate_value": "1",
            "derivation": "C_psiH=C_WH under identical parent source coefficient",
            "status": "CONDITIONAL_UNITY_NOT_SIGNED",
            "valid_if": "parent action forces coefficient equality before readout",
            "missing_for_claim": "MISSING_PARENT_COEFFICIENT_EQUALITY_THEOREM",
        }
    ),
    base(
        {
            "candidate_id": "ASRC3031_2_finite_bound_fallback",
            "symbol": "A_source",
            "candidate_value": "MISSING_FINITE_SOURCE_BACKED_VALUE",
            "derivation": "finite numerator/denominator coefficient row if equality theorem fails",
            "status": "ACQUISITION_ROW_REQUIRED",
            "valid_if": "both coefficients are numeric/source-backed, same-frame and no orbital-GM import",
            "missing_for_claim": "MISSING_FINITE_C_PSIH; MISSING_FINITE_C_WH",
        }
    ),
]

promotion_gate_rows = [
    base(
        {
            "gate_id": "GATE3031_0_sources",
            "gate": "every cited local source path exists",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "source-backed audit only",
        }
    ),
    base(
        {
            "gate_id": "GATE3031_1_ratio_theorem_written",
            "gate": "A_source ratio theorem is explicit",
            "result": True,
            "notes": "A_source=C_psiH/C_WH under same-operator/source/boundary premises",
        }
    ),
    base(
        {
            "gate_id": "GATE3031_2_denominator_owner",
            "gate": "H_tau/M_H_ref/J_H/G_ref denominator is parent-owned",
            "result": False,
            "notes": "theta/Q_tau, M_H_ref, source bridge and G_ref remain unsigned",
        }
    ),
    base(
        {
            "gate_id": "GATE3031_3_numerator_owner",
            "gate": "psi_N linear source coefficient C_psiH is parent-owned",
            "result": False,
            "notes": "psi_N/Hcore/lapse source equation remains unsigned",
        }
    ),
    base(
        {
            "gate_id": "GATE3031_4_unity_claim",
            "gate": "A_source=1 is claimable",
            "result": False,
            "notes": "C_psiH=C_WH is not parent-signed",
        }
    ),
    base(
        {
            "gate_id": "GATE3031_5_numeric_Asource",
            "gate": "A_source has finite source-backed numeric value",
            "result": False,
            "notes": "ratio formula exists, numeric coefficients do not",
        }
    ),
    base(
        {
            "gate_id": "GATE3031_6_local_GR_claim",
            "gate": "local GR/Newton reduction is claimable",
            "result": False,
            "notes": "A_source is still nonclaim and second-order/PPN followthrough remains open",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3031_0_ratio",
            "decision": "retain A_source=C_psiH/C_WH as the correct coupling law",
            "rationale": "it makes A_source derivable from parent source coefficients instead of fitted or convention-set",
            "consequence": "future work should prove coefficient equality or fill both coefficients",
        }
    ),
    base(
        {
            "decision_id": "DEC3031_1_unity",
            "decision": "do not claim A_source=1",
            "rationale": "unity follows only if the parent action gives identical source coefficients for psi_N and W/c^2",
            "consequence": "A_source=1 remains a target theorem, not a normalization shortcut",
        }
    ),
    base(
        {
            "decision_id": "DEC3031_2_denominator",
            "decision": "treat denominator ownership as still unresolved",
            "rationale": "M_H_ref, H_tau, J_H/H_tau, G_ref and source-shadow guards are all still unsigned",
            "consequence": "no source-backed A_source numeric row yet",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3031_0_3032",
            "target_doc": "3032-Y5-R2FR-linear-source-coefficient-equality-or-finite-Asource-ratio-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_linear_source_coefficient_equality_or_finite_Asource_ratio_under_AX1090_3032.py",
            "mission": "try to prove C_psiH=C_WH from the parent variation; if not, produce the first finite nonclaim coefficient rows for C_psiH and C_WH",
            "success_condition": "A_source=1 becomes a parent-signed theorem or A_source=C_psiH/C_WH becomes a finite source-backed nonclaim value with all missing guards explicit",
            "forbidden": "no EH-only coefficient import; no orbital-GM denominator; no convention-only A_source=1; no cancellation; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

for key, output_rows in {
    "sources": source_register,
    "ratio_theorem": ratio_theorem_rows,
    "denominator_audit": denominator_audit_rows,
    "coefficient_rows": coefficient_rows,
    "candidate_values": candidate_value_rows,
    "gates": promotion_gate_rows,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[key], output_rows)

copy_plan = {
    "denominator_copy": OUTPUTS["denominator_audit"],
    "ratio_copy": OUTPUTS["ratio_theorem"],
    "candidate_copy": OUTPUTS["candidate_values"],
    "coefficient_copy": OUTPUTS["coefficient_rows"],
    "next_copy": OUTPUTS["next"],
}

for copy_key, source_path in copy_plan.items():
    shutil.copyfile(source_path, BRANCH_OUTPUTS[copy_key])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(BRANCH_OUTPUTS[copy_id]),
            "source_exists": source_path.exists(),
            "copy_exists": BRANCH_OUTPUTS[copy_id].exists(),
            "purpose": {
                "denominator_copy": "parent-action branch copy of A_source denominator owner audit",
                "ratio_copy": "local-bound branch copy of coefficient-ratio theorem",
                "candidate_copy": "local-bound branch copy of A_source candidate value rows",
                "coefficient_copy": "local-bound branch copy of linear source coefficient rows",
                "next_copy": "RAB acquisition queue handoff",
            }[copy_id],
        }
    )
    for copy_id, source_path in copy_plan.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

claim_rows = (
    source_register
    + ratio_theorem_rows
    + denominator_audit_rows
    + coefficient_rows
    + candidate_value_rows
    + promotion_gate_rows
    + decision_rows
    + next_rows
    + branch_rows
)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
csv_paths_before_validation = [path for key, path in OUTPUTS.items() if key != "validation"]


def missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(as_str(value) for value in row.values())


validation_rows = [
    {
        "validation_id": "VAL3031_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": "P8_Y5_R2FR_3031_SOURCE_REGISTER.csv",
    },
    {
        "validation_id": "VAL3031_01_csv_parse",
        "passed": all(csv_ok(path) for path in csv_paths_before_validation),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all 3031 CSV artifacts except validation import with csv.DictReader",
    },
    {
        "validation_id": "VAL3031_02_ratio_theorem",
        "passed": any(row["mathematical_form"] == "A_source = C_psiH / C_WH" for row in ratio_theorem_rows),
        "requirement": "A_source coefficient-ratio law is written",
        "evidence": "P8_Y5_R2FR_3031_ASOURCE_RATIO_THEOREM_ATTEMPT.csv",
    },
    {
        "validation_id": "VAL3031_03_denominator_rejected",
        "passed": any(row["current_status"] == "DENOMINATOR_OWNER_NOT_DERIVED" and not boolish(row["passes_denominator"]) for row in denominator_audit_rows),
        "requirement": "denominator owner fails closed",
        "evidence": "P8_Y5_R2FR_3031_DENOMINATOR_OWNER_AUDIT.csv",
    },
    {
        "validation_id": "VAL3031_04_coefficients_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in coefficient_rows),
        "requirement": "linear source coefficient rows remain nonclaim",
        "evidence": "P8_Y5_R2FR_3031_LINEAR_SOURCE_COEFFICIENT_ROWS.csv",
    },
    {
        "validation_id": "VAL3031_05_unity_not_claimed",
        "passed": any(row["candidate_value"] == "1" and "NOT_SIGNED" in row["status"] for row in candidate_value_rows),
        "requirement": "A_source=1 is not claim-promoted",
        "evidence": "P8_Y5_R2FR_3031_ASOURCE_CANDIDATE_VALUE_ROWS.csv",
    },
    {
        "validation_id": "VAL3031_06_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if missing_marker(row)),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all generated 3031 claim-control rows",
    },
    {
        "validation_id": "VAL3031_07_branch_copies_exist",
        "passed": all(path.exists() for path in BRANCH_OUTPUTS.values()),
        "requirement": "branch copies and acquisition queue exist",
        "evidence": "P8_Y5_R2FR_3031_BRANCH_COPIES.csv",
    },
    {
        "validation_id": "VAL3031_08_outputs_scoped",
        "passed": all(under(path, ROOT) for path in generated_paths),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3031_09_formalization_not_targeted",
        "passed": all(not under(path, FORMALIZATION) for path in generated_paths),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3031_10_no_orbital_GM_shortcut",
        "passed": any("orbital-GM" in row["forbidden"] for row in next_rows),
        "requirement": "no orbital-GM denominator shortcut is retained",
        "evidence": "P8_Y5_R2FR_3031_NEXT_TARGET.csv",
    },
    {
        "validation_id": "VAL3031_11_next_target_selected",
        "passed": any(boolish(row["selected"]) and "3032" in row["target_doc"] for row in next_rows),
        "requirement": "next target selects coefficient equality or finite ratio",
        "evidence": "P8_Y5_R2FR_3031_NEXT_TARGET.csv",
    },
]

overall = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3031_99_overall",
        "passed": overall,
        "requirement": "all 3031 validation checks pass",
        "evidence": "aggregate of VAL3031_00 through VAL3031_11",
    }
)
validation_rows = [base(row) for row in validation_rows]
write_csv(OUTPUTS["validation"], validation_rows)

doc_sections = [
    "# 3031 - A_source Denominator Owner Or First Source-Backed Value under AX1090",
    "",
    "Status: `Y5_R2FR_3031_Asource_ratio_law_derived_denominator_not_owned_3032_next`",
    "",
    "## Verdict",
    "",
    "3031 makes the useful derivation move: `A_source` should not be treated as a loose fit or a convention. On a fixed local branch, if `psi_N` and `W/c^2` are governed by the same parent linear operator, source current and boundary data, then uniqueness gives",
    "",
    "`A_source = C_psiH / C_WH`.",
    "",
    "So `A_source=1` is allowed only if the parent variation proves `C_psiH=C_WH`. That is the right theorem target.",
    "",
    "Current MTS does **not** yet close it. The denominator `H_tau/M_H_ref/J_H/G_ref` is still unsigned, and the numerator coefficient `C_psiH` from the `psi_N` equation is also missing. Therefore no source-backed numeric `A_source` row is claimable yet.",
    "",
    "## A_source Ratio Theorem Attempt",
    "",
    md_table(ratio_theorem_rows, ["theorem_id", "statement", "mathematical_form", "status", "result"]),
    "",
    "## Denominator Owner Audit",
    "",
    md_table(denominator_audit_rows, ["audit_id", "object", "current_status", "passes_denominator", "blocks"]),
    "",
    "## Linear Source Coefficient Rows",
    "",
    md_table(coefficient_rows, ["coefficient_id", "symbol", "numeric_value", "status", "required_exit"]),
    "",
    "## A_source Candidate Values",
    "",
    md_table(candidate_value_rows, ["candidate_id", "symbol", "candidate_value", "status", "missing_for_claim"]),
    "",
    "## Source Register",
    "",
    md_table(source_register, ["source_id", "exists", "role", "status"]),
    "",
    "## Promotion Gates",
    "",
    md_table(promotion_gate_rows, ["gate_id", "gate", "result", "notes"]),
    "",
    "## Decision Ledger",
    "",
    md_table(decision_rows, ["decision_id", "decision", "rationale", "consequence"]),
    "",
    "## Next Target",
    "",
    md_table(next_rows, ["next_id", "target_doc", "target_script", "mission", "success_condition"]),
    "",
    "## Validation",
    "",
    md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"]),
    "",
    "## Files Written",
    "",
]
doc_sections.extend(f"- `{path}`" for path in generated_paths if path.exists())
DOC.write_text("\n".join(doc_sections) + "\n", encoding="utf-8")

print(f"Wrote 3031 checkpoint: {DOC}")
print(f"Overall validation: {overall}")
