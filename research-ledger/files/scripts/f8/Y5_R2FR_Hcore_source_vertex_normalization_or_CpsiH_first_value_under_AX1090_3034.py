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
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3034"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3034-Y5-R2FR-Hcore-source-vertex-normalization-or-CpsiH-first-value-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3034_00_3033_doc": ROOT / "3033-Y5-R2FR-single-source-vertex-or-common-linear-operator-under-AX1090.md",
    "SRC3034_01_3033_shapes": RESIDUALS / "P8_Y5_R2FR_3033_COEFFICIENT_SOURCE_SHAPE_ROWS.csv",
    "SRC3034_02_3033_unity": RESIDUALS / "P8_Y5_R2FR_3033_EQUALITY_CONDITION_ROW.csv",
    "SRC3034_03_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3034_04_3024_variation": RESIDUALS / "P8_Y5_R2FR_3024_VARIATION_DERIVATION.csv",
    "SRC3034_05_3026_extraction": RESIDUALS / "P8_Y5_R2FR_3026_SIGMAH_FPSI_EXTRACTION_CONTRACT.csv",
    "SRC3034_06_3027_template": RESIDUALS / "P8_Y5_R2FR_3027_PARAMETERIZED_KSCR_SOURCE_ROW_TEMPLATE.csv",
    "SRC3034_07_3029_K0": RESIDUALS / "P8_Y5_R2FR_3029_FIRST_COMPONENT_VALUE_ATTEMPT.csv",
    "SRC3034_08_3031_coefficients": RESIDUALS / "P8_Y5_R2FR_3031_LINEAR_SOURCE_COEFFICIENT_ROWS.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3034_SOURCE_REGISTER.csv",
    "normalization": RESIDUALS / "P8_Y5_R2FR_3034_HCORE_SOURCE_VERTEX_NORMALIZATION_AUDIT.csv",
    "component_tuple": RESIDUALS / "P8_Y5_R2FR_3034_CPSIH_COMPONENT_TUPLE_ROWS.csv",
    "sign_audit": RESIDUALS / "P8_Y5_R2FR_3034_SIGN_CONVENTION_AUDIT.csv",
    "first_value": RESIDUALS / "P8_Y5_R2FR_3034_CPSIH_FIRST_VALUE_ATTEMPT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3034_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3034_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3034_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3034_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3034_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "normalization_copy": PARENT_ACTION / "Hcore_source_vertex_normalization_audit_3034_NOT_SIGNED.csv",
    "component_copy": LOCAL_BOUNDS / "CpsiH_component_tuple_rows_3034_NONCLAIM.csv",
    "sign_copy": LOCAL_BOUNDS / "Hcore_sign_convention_audit_3034_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3034_K0_CN_JHrho_NEXT_NONCLAIM.csv",
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
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


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
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3034_00_3033_doc": "3033 handoff: single source vertex not signed; C_psiH shape exposed",
    "SRC3034_01_3033_shapes": "C_psiH and C_WH formula-shape rows",
    "SRC3034_02_3033_unity": "explicit A_source unity condition",
    "SRC3034_03_3024_ansatz": "minimal Hcore ansatz with + integral J_H psi_N",
    "SRC3034_04_3024_variation": "exterior variation without source",
    "SRC3034_05_3026_extraction": "K0 and kinetic trace extraction contract",
    "SRC3034_06_3027_template": "parameterized Hcore density/source-row template",
    "SRC3034_07_3029_K0": "conditional K0 normalization attempt",
    "SRC3034_08_3031_coefficients": "linear source coefficient placeholders",
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

normalization_rows = [
    base(
        {
            "audit_id": "HSN3034_0_parent_action_shape",
            "object": "Hcore log-lapse source block",
            "candidate_formula": "S_N=-C_N/2 int K_N^{ij} partial_i psi_N partial_j psi_N + int J_H psi_N + boundary",
            "derivation_step": "use the 3024 ansatz as a conditional parent-action candidate, not as an adopted MTS action",
            "source_path": str(SOURCE_PATHS["SRC3034_03_3024_ansatz"]),
            "status": "CONDITIONAL_SHAPE_ONLY_NOT_PARENT_ADOPTED",
            "passes": False,
            "missing_for_claim": "MISSING_PARENT_ACTION_TERM; MISSING_FIELD_PRIMITIVE_ID; MISSING_SOURCE_DENSITY_OWNER",
        }
    ),
    base(
        {
            "audit_id": "HSN3034_1_variation_with_source",
            "object": "Euler equation including source",
            "candidate_formula": "C_N partial_i(K_N^{ij} partial_j psi_N) + J_H = 0",
            "derivation_step": "vary kinetic term, integrate by parts, retain the + int J_H psi_N source sign",
            "source_path": str(SOURCE_PATHS["SRC3034_03_3024_ansatz"]),
            "status": "DERIVED_FOR_ANSATZ_SIGN_CONVENTION_PENDING",
            "passes": False,
            "missing_for_claim": "MISSING_PARENT_SIGN_CONVENTION; MISSING_BOUNDARY_CLASS; MISSING_J_H_SOURCE_SIGN",
        }
    ),
    base(
        {
            "audit_id": "HSN3034_2_linear_isotropic_limit",
            "object": "linear Hcore source coefficient",
            "candidate_formula": "C_N K0 Delta psi_N + J_H = 0 -> Delta psi_N = -J_H/(C_N K0)",
            "derivation_step": "set K_N^{ij}=K0 delta^{ij} at u=psi_N=0 and ignore higher derivative/source-shadow terms",
            "source_path": str(SOURCE_PATHS["SRC3034_05_3026_extraction"]),
            "status": "FORMULA_DERIVED_INPUTS_UNSIGNED",
            "passes": False,
            "missing_for_claim": "MISSING_K0_VALUE; MISSING_C_N_NORMALIZATION; MISSING_SOURCE_SHADOW_ZERO",
        }
    ),
    base(
        {
            "audit_id": "HSN3034_3_source_density_bridge",
            "object": "J_H to rho_H bridge",
            "candidate_formula": "J_H = JHrho rho_H",
            "derivation_step": "define the source coefficient that turns the Hcore current into the same density used by W/c^2",
            "source_path": str(SOURCE_PATHS["SRC3034_01_3033_shapes"]),
            "status": "BRIDGE_REQUIRED_NOT_SOURCED",
            "passes": False,
            "missing_for_claim": "MISSING_JHrho; MISSING_RHO_H_UNITS; MISSING_PARENT_SOURCE_CURRENT_ID",
        }
    ),
    base(
        {
            "audit_id": "HSN3034_4_CpsiH_formula",
            "object": "C_psiH formula",
            "candidate_formula": "C_psiH = -JHrho/(C_N K0)",
            "derivation_step": "substitute J_H=JHrho rho_H into the linear isotropic Euler equation",
            "source_path": str(SOURCE_PATHS["SRC3034_01_3033_shapes"]),
            "status": "STRICT_FORMULA_ONLY_NONCLAIM",
            "passes": False,
            "missing_for_claim": "MISSING_JHrho; MISSING_C_N; MISSING_K0; MISSING_SIGN_CONVENTION",
        }
    ),
    base(
        {
            "audit_id": "HSN3034_5_unity_condition",
            "object": "A_source=1 normalization condition",
            "candidate_formula": "-JHrho/(C_N K0) = 4*pi*G_ref/c^2",
            "derivation_step": "match C_psiH to the conditional W/c^2 Poisson/Gauss coefficient C_WH",
            "source_path": str(SOURCE_PATHS["SRC3034_02_3033_unity"]),
            "status": "UNITY_CONDITION_EXPLICIT_NOT_SIGNED",
            "passes": False,
            "missing_for_claim": "MISSING_G_REF_OWNER; MISSING_JHrho_OWNER; MISSING_NO_EH_IMPORT_CERTIFICATE",
        }
    ),
    base(
        {
            "audit_id": "HSN3034_6_verdict",
            "object": "Hcore source-vertex normalization",
            "candidate_formula": "parent action fixes JHrho/(C_N K0) with source sign",
            "derivation_step": "3034 does not find a parent-signed normalization or numeric first value",
            "source_path": str(SOURCE_PATHS["SRC3034_06_3027_template"]),
            "status": "NOT_CLOSED_MOVE_TO_K0_CN_JHrho_TARGET",
            "passes": False,
            "missing_for_claim": "MISSING_PARENT_HCORE_DENSITY_ADOPTION; MISSING_COMPONENT_VALUES; MISSING_SIGN",
        }
    ),
]

component_rows = [
    base(
        {
            "tuple_id": "CPT3034_0_CpsiH_formula",
            "symbol": "C_psiH",
            "component_role": "linear Hcore source coefficient",
            "available_value": "-JHrho/(C_N K0)",
            "required_to_promote": "numeric or parent-owned JHrho, C_N, K0 and sign convention",
            "source_path": str(SOURCE_PATHS["SRC3034_01_3033_shapes"]),
            "status": "FORMULA_ONLY_NONCLAIM",
        }
    ),
    base(
        {
            "tuple_id": "CPT3034_1_JHrho",
            "symbol": "JHrho",
            "component_role": "Hcore current to source-density coupling",
            "available_value": "MISSING_JHrho",
            "required_to_promote": "parent source-current normalization or sourced finite coefficient row",
            "source_path": str(SOURCE_PATHS["SRC3034_03_3024_ansatz"]),
            "status": "MISSING_PARENT_INPUT",
        }
    ),
    base(
        {
            "tuple_id": "CPT3034_2_C_N",
            "symbol": "C_N",
            "component_role": "Hcore kinetic normalization",
            "available_value": "MISSING_C_N",
            "required_to_promote": "parent kinetic coefficient and units",
            "source_path": str(SOURCE_PATHS["SRC3034_06_3027_template"]),
            "status": "MISSING_PARENT_INPUT",
        }
    ),
    base(
        {
            "tuple_id": "CPT3034_3_K0",
            "symbol": "K0",
            "component_role": "background isotropic kinetic trace",
            "available_value": "K0_norm=1 is convention-only if positivity/constancy and C_N absorption are signed",
            "required_to_promote": "parent K0 positivity, constancy, and normalization gauge",
            "source_path": str(SOURCE_PATHS["SRC3034_07_3029_K0"]),
            "status": "CONDITIONAL_CONVENTION_NOT_SOURCED",
        }
    ),
    base(
        {
            "tuple_id": "CPT3034_4_sign_Hcore",
            "symbol": "sign_Hcore",
            "component_role": "relative kinetic/source sign",
            "available_value": "MISSING_SIGN_CONVENTION",
            "required_to_promote": "parent orientation of source term and comparison potential",
            "source_path": str(SOURCE_PATHS["SRC3034_03_3024_ansatz"]),
            "status": "MISSING_PARENT_INPUT",
        }
    ),
    base(
        {
            "tuple_id": "CPT3034_5_source_current_id",
            "symbol": "J_H",
            "component_role": "parent source current identity",
            "available_value": "conditional ansatz current only",
            "required_to_promote": "MTS primitive current or Hilbert/source-current derivation",
            "source_path": str(SOURCE_PATHS["SRC3034_08_3031_coefficients"]),
            "status": "MISSING_PARENT_CURRENT_ID",
        }
    ),
    base(
        {
            "tuple_id": "CPT3034_6_boundary_class",
            "symbol": "boundary_H",
            "component_role": "operator inverse and integration-by-parts class",
            "available_value": "fixed boundary assumed",
            "required_to_promote": "source worldtube and asymptotic boundary conditions matching W/c^2 branch",
            "source_path": str(SOURCE_PATHS["SRC3034_04_3024_variation"]),
            "status": "MISSING_BOUNDARY_OWNER",
        }
    ),
    base(
        {
            "tuple_id": "CPT3034_7_CpsiH_numeric",
            "symbol": "C_psiH_numeric",
            "component_role": "first claim-capable numeric coefficient",
            "available_value": "MISSING_NUMERIC_VALUE",
            "required_to_promote": "all tuple components finite, sourced, units-declared, and sign-fixed",
            "source_path": str(SOURCE_PATHS["SRC3034_01_3033_shapes"]),
            "status": "NO_NUMERIC_FIRST_VALUE",
        }
    ),
]

sign_rows = [
    base(
        {
            "sign_id": "SIGN3034_0_kinetic_variation",
            "object": "kinetic term sign",
            "formula": "delta[-C_N/2 int K partial psi partial psi] -> +C_N partial_i(K^{ij} partial_j psi) delta psi",
            "status": "ALGEBRAIC_FOR_ANSATZ",
            "claim_effect": "sets the left-side sign if the ansatz is adopted",
            "missing_for_claim": "MISSING_PARENT_ACTION_ADOPTION",
        }
    ),
    base(
        {
            "sign_id": "SIGN3034_1_source_variation",
            "object": "source term sign",
            "formula": "delta[+ int J_H psi_N] -> +J_H delta psi_N",
            "status": "CONVENTION_VISIBLE_NOT_PARENT_SIGNED",
            "claim_effect": "with the visible sign, Delta psi_N=-J_H/(C_N K0)",
            "missing_for_claim": "MISSING_PARENT_SOURCE_ORIENTATION",
        }
    ),
    base(
        {
            "sign_id": "SIGN3034_2_potential_comparison",
            "object": "W/c^2 comparison sign",
            "formula": "Delta(W/c^2)=+4*pi*G_ref rho_H/c^2 on the conditional branch",
            "status": "COMPARATOR_CONDITIONAL",
            "claim_effect": "unity requires the Hcore sign to match the chosen W convention",
            "missing_for_claim": "MISSING_PARENT_W_SIGN_AND_G_REF_OWNER",
        }
    ),
    base(
        {
            "sign_id": "SIGN3034_3_verdict",
            "object": "relative sign of C_psiH/C_WH",
            "formula": "sign[-JHrho/(C_N K0)] = sign[4*pi*G_ref/c^2]",
            "status": "RELATIVE_SIGN_NOT_CLOSED",
            "claim_effect": "blocks A_source=1 promotion even before numeric values",
            "missing_for_claim": "MISSING_JHrho_SIGN; MISSING_C_N_K0_POSITIVITY; MISSING_W_CONVENTION",
        }
    ),
]

first_value_rows = [
    base(
        {
            "attempt_id": "CVAL3034_0_CpsiH_formula_value",
            "symbol": "C_psiH",
            "attempted_value": "-JHrho/(C_N K0)",
            "derivation": "linear isotropic variation of the 3024 Hcore ansatz including the source term",
            "status": "FORMULA_VALUE_ONLY_NOT_NUMERIC",
            "missing_for_claim": "MISSING_JHrho; MISSING_C_N; MISSING_K0; MISSING_SIGN_CONVENTION; MISSING_UNITS",
        }
    ),
    base(
        {
            "attempt_id": "CVAL3034_1_CpsiH_unity_target",
            "symbol": "C_psiH_if_A_source_unity",
            "attempted_value": "4*pi*G_ref/c^2",
            "derivation": "only if parent action signs JHrho=-4*pi*G_ref*C_N*K0/c^2 up to convention",
            "status": "TARGET_CONDITION_ONLY_NONCLAIM",
            "missing_for_claim": "MISSING_PARENT_EQUALITY_THEOREM; MISSING_G_REF_OWNER",
        }
    ),
    base(
        {
            "attempt_id": "CVAL3034_2_K0_absorption",
            "symbol": "K0_norm",
            "attempted_value": "1",
            "derivation": "can be a convention if K0 is positive, finite and branch-constant and C_N absorbs it",
            "status": "CONVENTION_ONLY_NOT_PHYSICAL_VALUE",
            "missing_for_claim": "MISSING_K0_POSITIVITY_AND_CONSTANCY; MISSING_C_N_NORMALIZATION_SOURCE",
        }
    ),
    base(
        {
            "attempt_id": "CVAL3034_3_product_ratio",
            "symbol": "JHrho_over_CN_K0",
            "attempted_value": "MISSING_NUMERIC_RATIO",
            "derivation": "physical A_source depends on the ratio, not separately on arbitrary rescalings of C_N and K0",
            "status": "RATIO_TARGET_IDENTIFIED",
            "missing_for_claim": "MISSING_SOURCE_BRIDGE_OR_FINITE_BOUND_ROW",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3034_0_sources",
            "gate": "every cited local source path exists",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "required before using 3034 as a private checkpoint",
        }
    ),
    base(
        {
            "gate_id": "GATE3034_1_variation_written",
            "gate": "Hcore variation with source term is explicitly written",
            "result": any("C_N K0 Delta psi_N + J_H = 0" in row["candidate_formula"] for row in normalization_rows),
            "notes": "derives formula shape only",
        }
    ),
    base(
        {
            "gate_id": "GATE3034_2_CpsiH_tuple",
            "gate": "C_psiH tuple lists JHrho, C_N, K0 and sign",
            "result": all(
                any(row["symbol"] == symbol for row in component_rows)
                for symbol in ["JHrho", "C_N", "K0", "sign_Hcore"]
            ),
            "notes": "tuple is nonclaim until components are parent-signed",
        }
    ),
    base(
        {
            "gate_id": "GATE3034_3_numeric_value",
            "gate": "first numeric C_psiH value exists",
            "result": False,
            "notes": "no numeric JHrho/(C_N K0) source found",
        }
    ),
    base(
        {
            "gate_id": "GATE3034_4_sign",
            "gate": "relative Hcore/W sign is parent-signed",
            "result": False,
            "notes": "visible ansatz sign is algebraic but not parent-adopted",
        }
    ),
    base(
        {
            "gate_id": "GATE3034_5_claim_control",
            "gate": "no output row is claim-promoted",
            "result": True,
            "notes": "all 3034 rows stay valid_for_claim=false and claim_allowed=false",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3034_0_zero_or_value",
            "question": "can 3034 close C_psiH or A_source=1 directly?",
            "answer": "NO",
            "reason": "the coupling ratio is now formula-sharp, but JHrho, C_N, K0 and sign convention are not parent-signed",
            "next_action": "try to own the product C_N K0 and the source bridge JHrho, or move to finite nonclaim bounds",
        }
    ),
    base(
        {
            "decision_id": "DEC3034_1_best_route",
            "question": "what is the least-scrutiny route next?",
            "answer": "derive the ratio, not separate arbitrary normalizations",
            "reason": "K0 can be absorbed into C_N by convention, so the physical target is JHrho/(C_N K0) with source units and sign fixed",
            "next_action": "3035: K0-C_N normalization or JHrho source bridge",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3034_0_3035",
            "next_checkpoint": "3035-Y5-R2FR-K0-CN-normalization-or-JHrho-source-bridge-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_K0_CN_normalization_or_JHrho_source_bridge_under_AX1090_3035.py",
            "mission": "derive the parent-owned ratio JHrho/(C_N K0), or stage finite source-backed nonclaim rows for the local branch",
            "starting_equation": "C_psiH=-JHrho/(C_N K0); A_source=1 needs -JHrho/(C_N K0)=4*pi*G_ref/c^2 up to sign convention",
            "claim_policy": "no local-GR, R10, WEP, PPN, clock, orbital or A_source claim unless the tuple is finite, sourced, sign-fixed and validated",
        }
    )
]

for name, output_rows in {
    "sources": source_register,
    "normalization": normalization_rows,
    "component_tuple": component_rows,
    "sign_audit": sign_rows,
    "first_value": first_value_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[name], output_rows)

shutil.copyfile(OUTPUTS["normalization"], BRANCH_OUTPUTS["normalization_copy"])
shutil.copyfile(OUTPUTS["component_tuple"], BRANCH_OUTPUTS["component_copy"])
shutil.copyfile(OUTPUTS["sign_audit"], BRANCH_OUTPUTS["sign_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for future intake",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + normalization_rows
    + component_rows
    + sign_rows
    + first_value_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3034_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3034_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3034_02_variation_with_source",
            "passed": any("C_N K0 Delta psi_N + J_H = 0" in row["candidate_formula"] for row in normalization_rows),
            "requirement": "source-inclusive Hcore variation is explicit",
            "evidence": OUTPUTS["normalization"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3034_03_CpsiH_formula",
            "passed": any(row["available_value"] == "-JHrho/(C_N K0)" for row in component_rows),
            "requirement": "C_psiH formula row exists",
            "evidence": OUTPUTS["component_tuple"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3034_04_tuple_missing_inputs",
            "passed": all(
                any(row["symbol"] == symbol and "MISSING" in row["status"] or row["symbol"] == symbol and "CONDITIONAL" in row["status"] for row in component_rows)
                for symbol in ["JHrho", "C_N", "K0", "sign_Hcore"]
            ),
            "requirement": "missing JHrho, C_N, K0 and sign remain explicit nonclaim blockers",
            "evidence": OUTPUTS["component_tuple"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3034_05_sign_not_promoted",
            "passed": any(row["status"] == "RELATIVE_SIGN_NOT_CLOSED" for row in sign_rows),
            "requirement": "sign convention remains blocked, not silently chosen",
            "evidence": OUTPUTS["sign_audit"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3034_06_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3034 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3034_07_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3034_08_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3034_09_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3034_10_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3035-"),
            "requirement": "next derivation target is selected",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3034_11_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3034 - Hcore Source Vertex Normalization Or CpsiH First Value under AX1090

Status: `Y5_R2FR_3034_CpsiH_formula_sharp_Hcore_normalization_not_signed_3035_next`

## Verdict

3034 tries the obvious leap: use the Hcore source vertex to turn the 3033 formula-shape into a claim-capable first value for `C_psiH`.

The derivation gets sharper, but it does **not** close. For the 3024 conditional Hcore ansatz,

`S_N=-C_N/2 int K_N^{{ij}} partial_i psi_N partial_j psi_N + int J_H psi_N + boundary`,

variation gives the source-inclusive Euler shape

`C_N partial_i(K_N^{{ij}} partial_j psi_N) + J_H = 0`.

On the linear isotropic branch this becomes

`C_N K0 Delta psi_N + J_H = 0`,

and if `J_H=JHrho rho_H`,

`C_psiH = -JHrho/(C_N K0)`.

That is progress: the missing local-GR coupling is no longer a fog bank. It is the tuple `(JHrho, C_N, K0, sign_Hcore, source_current_id, boundary_class, units)`. But none of those parent-normalization ingredients is signed strongly enough to claim `A_source=1`.

## Hcore Source Vertex Normalization Audit

{md_table(normalization_rows, ["audit_id", "object", "candidate_formula", "status", "passes", "missing_for_claim"])}

## CpsiH Component Tuple

{md_table(component_rows, ["tuple_id", "symbol", "component_role", "available_value", "status", "required_to_promote"])}

## Sign Convention Audit

{md_table(sign_rows, ["sign_id", "object", "formula", "status", "claim_effect", "missing_for_claim"])}

## First Value Attempt

{md_table(first_value_rows, ["attempt_id", "symbol", "attempted_value", "status", "missing_for_claim"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print("3034 verdict: C_psiH formula sharpened; JHrho, C_N, K0 and sign remain nonclaim blockers.")
