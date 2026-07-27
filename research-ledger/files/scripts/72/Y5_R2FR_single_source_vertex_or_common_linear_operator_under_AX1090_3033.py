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

CHECKPOINT = "3033"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3033-Y5-R2FR-single-source-vertex-or-common-linear-operator-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3033_00_3032_doc": ROOT / "3032-Y5-R2FR-linear-source-coefficient-equality-or-finite-Asource-ratio-under-AX1090.md",
    "SRC3033_01_3032_equality": RESIDUALS / "P8_Y5_R2FR_3032_COEFFICIENT_EQUALITY_PROOF_ATTEMPT.csv",
    "SRC3033_02_3032_countermodels": RESIDUALS / "P8_Y5_R2FR_3032_COEFFICIENT_EQUALITY_COUNTERMODEL_LEDGER.csv",
    "SRC3033_03_3032_finite_rows": RESIDUALS / "P8_Y5_R2FR_3032_FINITE_COEFFICIENT_INPUT_ROWS.csv",
    "SRC3033_04_3032_next": RESIDUALS / "P8_Y5_R2FR_3032_NEXT_TARGET.csv",
    "SRC3033_05_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3033_06_3024_variation": RESIDUALS / "P8_Y5_R2FR_3024_VARIATION_DERIVATION.csv",
    "SRC3033_07_3022_psin_owner": RESIDUALS / "P8_Y5_R2FR_3022_PSIN_HAMILTONIAN_OWNER_AUDIT.csv",
    "SRC3033_08_2921_pg_bridge": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3033_09_2921_source_mass": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
    "SRC3033_10_3008_coupling": RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv",
    "SRC3033_11_3017_ward": RESIDUALS / "P8_Y5_R2FR_3017_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "SRC3033_12_3006_htau": RESIDUALS / "P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv",
    "SRC3033_13_3031_ratio": RESIDUALS / "P8_Y5_R2FR_3031_ASOURCE_RATIO_THEOREM_ATTEMPT.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3033_SOURCE_REGISTER.csv",
    "source_vertex": RESIDUALS / "P8_Y5_R2FR_3033_SINGLE_SOURCE_VERTEX_AUDIT.csv",
    "common_operator": RESIDUALS / "P8_Y5_R2FR_3033_COMMON_LINEAR_OPERATOR_AUDIT.csv",
    "coefficient_shapes": RESIDUALS / "P8_Y5_R2FR_3033_COEFFICIENT_SOURCE_SHAPE_ROWS.csv",
    "equality_condition": RESIDUALS / "P8_Y5_R2FR_3033_EQUALITY_CONDITION_ROW.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3033_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3033_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3033_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3033_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3033_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "vertex_copy": PARENT_ACTION / "single_source_vertex_audit_3033_NOT_SIGNED.csv",
    "operator_copy": LOCAL_BOUNDS / "common_linear_operator_audit_3033_NONCLAIM.csv",
    "coefficient_copy": LOCAL_BOUNDS / "coefficient_source_shape_rows_3033_NONCLAIM.csv",
    "equality_copy": LOCAL_BOUNDS / "A_source_equality_condition_3033_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3033_HCORE_VERTEX_NORMALIZATION_NEXT_NONCLAIM.csv",
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
    "SRC3033_00_3032_doc": "3032 handoff: coefficient equality not signed",
    "SRC3033_01_3032_equality": "3032 equality proof blocker clauses",
    "SRC3033_02_3032_countermodels": "live unequal-coefficient countermodels",
    "SRC3033_03_3032_finite_rows": "finite C_psiH/C_WH intake templates",
    "SRC3033_04_3032_next": "3033 target selection",
    "SRC3033_05_3024_ansatz": "Hcore ansatz with J_H psi_N source vertex",
    "SRC3033_06_3024_variation": "Hcore variation and exterior equation",
    "SRC3033_07_3022_psin_owner": "psi_N owner blockers",
    "SRC3033_08_2921_pg_bridge": "Poisson/Gauss bridge rows",
    "SRC3033_09_2921_source_mass": "parent source-mass identity audit",
    "SRC3033_10_3008_coupling": "coupling guard rows",
    "SRC3033_11_3017_ward": "source-current Ward owner attempt",
    "SRC3033_12_3006_htau": "H_tau/M_H_ref extraction blockers",
    "SRC3033_13_3031_ratio": "A_source coefficient-ratio theorem",
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

source_vertex_rows = [
    base(
        {
            "vertex_id": "SV3033_0_Hcore_vertex_shape",
            "object": "Hcore psi_N source vertex",
            "candidate_formula": "S_N contains + integral J_H psi_N",
            "source_path": str(SOURCE_PATHS["SRC3033_05_3024_ansatz"]),
            "equation_ref": "ANZ3024_2",
            "current_status": "SOURCE_VERTEX_SHAPE_PRESENT_CONDITIONAL_ANSATZ",
            "passes_vertex": False,
            "missing_for_claim": "MISSING_PARENT_ACTION_TERM; MISSING_J_H_NORMALIZATION; MISSING_C_N_K0_UNITS",
        }
    ),
    base(
        {
            "vertex_id": "SV3033_1_W_vertex_shape",
            "object": "W/c^2 Poisson source vertex",
            "candidate_formula": "nabla^2 Phi=(kappa_eff c^4/2) rho_H = 4 pi G_eff rho_H",
            "source_path": str(SOURCE_PATHS["SRC3033_08_2921_pg_bridge"]),
            "equation_ref": "PG2921_3",
            "current_status": "POISSON_SOURCE_SHAPE_PRESENT_CONDITIONAL_EH_ONLY_PREMISES",
            "passes_vertex": False,
            "missing_for_claim": "MISSING_PARENT_W_EQUATION; MISSING_G_REF; MISSING_M_H_REF; MISSING_NO_EH_IMPORT_PROOF",
        }
    ),
    base(
        {
            "vertex_id": "SV3033_2_single_parent_vertex",
            "object": "one parent source vertex feeds both equations",
            "candidate_formula": "S_source = integral J_H * V(psi_N,W/c^2) with partial_psi V|0 = partial_W V|0",
            "source_path": str(SOURCE_PATHS["SRC3033_01_3032_equality"]),
            "equation_ref": "EQ3032_4",
            "current_status": "MISSING_SINGLE_SOURCE_VERTEX_OWNER",
            "passes_vertex": False,
            "missing_for_claim": "MISSING_PARENT_SOURCE_VERTEX; MISSING_NO_INDEPENDENT_PSI_WEIGHT; MISSING_NO_HIDDEN_FRAME",
        }
    ),
    base(
        {
            "vertex_id": "SV3033_3_no_source_weight",
            "object": "no independent source-only prefactor",
            "candidate_formula": "forbid J_H[(1+epsilon_psi)psi_N + W/c^2]",
            "source_path": str(SOURCE_PATHS["SRC3033_11_3017_ward"]),
            "equation_ref": "WARD3017_2; CM3032_0",
            "current_status": "COUNTERMODEL_SURVIVES",
            "passes_vertex": False,
            "missing_for_claim": "MISSING_NO_SOURCE_PREFACTOR_PARENT_CLAUSE",
        }
    ),
    base(
        {
            "vertex_id": "SV3033_4_verdict",
            "object": "single source vertex theorem",
            "candidate_formula": "C_psiH and C_WH share one parent source vertex",
            "source_path": str(SOURCE_PATHS["SRC3033_02_3032_countermodels"]),
            "equation_ref": "CM3032_0..3",
            "current_status": "SINGLE_SOURCE_VERTEX_NOT_SIGNED",
            "passes_vertex": False,
            "missing_for_claim": "SOURCE_VERTEX_COUNTERMODELS_LIVE",
        }
    ),
]

operator_rows = [
    base(
        {
            "operator_id": "OP3033_0_psi_operator_shape",
            "object": "psi_N linear operator",
            "candidate_formula": "L_psi psi_N := partial_i(K_N^{ij} partial_j psi_N) at linear order",
            "source_path": str(SOURCE_PATHS["SRC3033_06_3024_variation"]),
            "equation_ref": "VAR3024_0",
            "current_status": "OPERATOR_SHAPE_PRESENT_CONDITIONAL_ANSATZ",
            "passes_operator": False,
            "missing_for_claim": "MISSING_PARENT_K_N; MISSING_C_N_K0_NORMALIZATION; MISSING_BOUNDARY_CLASS",
        }
    ),
    base(
        {
            "operator_id": "OP3033_1_W_operator_shape",
            "object": "W/c^2 linear operator",
            "candidate_formula": "L_W(W/c^2) := nabla^2(W/c^2)",
            "source_path": str(SOURCE_PATHS["SRC3033_08_2921_pg_bridge"]),
            "equation_ref": "PG2921_3",
            "current_status": "OPERATOR_SHAPE_PRESENT_CONDITIONAL_BRIDGE",
            "passes_operator": False,
            "missing_for_claim": "MISSING_PARENT_POISSON_GAUSS_BRIDGE; MISSING_G_REF; MISSING_M_H_REF",
        }
    ),
    base(
        {
            "operator_id": "OP3033_2_common_operator_condition",
            "object": "same normalized operator",
            "candidate_formula": "L_psi=L_W after K_N^{ij}->K0 delta^{ij}, C_N K0 normalization, same boundary and no harmonic mode",
            "source_path": str(SOURCE_PATHS["SRC3033_01_3032_equality"]),
            "equation_ref": "EQ3032_1",
            "current_status": "MISSING_OPERATOR_BOUNDARY_MATCH",
            "passes_operator": False,
            "missing_for_claim": "MISSING_K0_C_N_OWNER; MISSING_OPERATOR_NORMALIZATION; MISSING_HARMONIC_MODE_GUARD",
        }
    ),
    base(
        {
            "operator_id": "OP3033_3_verdict",
            "object": "common linear operator theorem",
            "candidate_formula": "L_psi=L_W is parent-signed",
            "source_path": str(SOURCE_PATHS["SRC3033_03_3032_finite_rows"]),
            "equation_ref": "FIN3032_0; FIN3032_1",
            "current_status": "COMMON_OPERATOR_NOT_SIGNED",
            "passes_operator": False,
            "missing_for_claim": "OPERATOR_NORMALIZATION_COUNTERMODEL_LIVE",
        }
    ),
]

coefficient_shape_rows = [
    base(
        {
            "shape_id": "CSH3033_0_C_psiH_shape",
            "symbol": "C_psiH",
            "source_backed_shape": "Delta psi_N = - J_H/(C_N K0) on the linear isotropic ansatz branch",
            "coefficient_formula": "C_psiH = - JHrho/(C_N K0) if J_H=JHrho*rho_H",
            "units": "operator_units_per_mass_density after JHrho, C_N and K0 are declared",
            "source_path": str(SOURCE_PATHS["SRC3033_05_3024_ansatz"]),
            "equation_ref": "ANZ3024_2 plus linearized VAR3024_0",
            "status": "SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM",
            "missing_for_claim": "MISSING_JHrho; MISSING_C_N; MISSING_K0; MISSING_SIGN_CONVENTION; MISSING_PARENT_ACTION_ADOPTION",
        }
    ),
    base(
        {
            "shape_id": "CSH3033_1_C_WH_shape",
            "symbol": "C_WH",
            "source_backed_shape": "Delta(W/c^2)=4*pi*G_ref*rho_H/c^2 on the conditional Poisson/Gauss branch",
            "coefficient_formula": "C_WH = 4*pi*G_ref/c^2 = kappa_eff*c^2/2 if Phi=W",
            "units": "operator_units_per_mass_density after G_ref and source density units are declared",
            "source_path": str(SOURCE_PATHS["SRC3033_08_2921_pg_bridge"]),
            "equation_ref": "PG2921_3",
            "status": "SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM",
            "missing_for_claim": "MISSING_G_REF; MISSING_M_H_REF; MISSING_PARENT_POISSON_BRIDGE; MISSING_NO_EH_IMPORT_CERTIFICATE",
        }
    ),
    base(
        {
            "shape_id": "CSH3033_2_delta_A_shape",
            "symbol": "delta_A_source",
            "source_backed_shape": "delta_A_source = C_psiH/C_WH - 1",
            "coefficient_formula": "delta_A_source = -JHrho*c^2/(4*pi*G_ref*C_N*K0) - 1",
            "units": "dimensionless",
            "source_path": str(SOURCE_PATHS["SRC3033_13_3031_ratio"]),
            "equation_ref": "RATIO3031_2; CSH3033_0; CSH3033_1",
            "status": "FORMULA_SHAPE_DERIVED_INPUTS_MISSING",
            "missing_for_claim": "MISSING_JHrho; MISSING_G_REF; MISSING_C_N; MISSING_K0; MISSING_RESIDUAL_ENVELOPE",
        }
    ),
]

equality_condition_rows = [
    base(
        {
            "condition_id": "COND3033_0_Asource_unity_condition",
            "statement": "A_source=1 requires the Hcore source normalization to equal the Poisson/Gauss source normalization",
            "mathematical_condition": "-JHrho/(C_N K0) = 4*pi*G_ref/c^2",
            "equivalent_condition": "JHrho = -4*pi*G_ref*C_N*K0/c^2 up to sign convention",
            "current_status": "EQUALITY_CONDITION_EXPLICIT_NOT_SIGNED",
            "claim_allowed_now": False,
            "next_input_needed": "parent sign convention plus JHrho, C_N, K0 and G_ref owner rows",
        }
    )
]

gate_rows = [
    base({"gate_id": "GATE3033_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed audit only"}),
    base({"gate_id": "GATE3033_1_Hcore_shape", "gate": "C_psiH equation-shape row is source-backed", "result": True, "notes": "3024 ansatz gives + integral J_H psi_N and linearized source coefficient shape"}),
    base({"gate_id": "GATE3033_2_Poisson_shape", "gate": "C_WH equation-shape row is source-backed", "result": True, "notes": "2921 Poisson/Gauss row gives conditional source coefficient shape"}),
    base({"gate_id": "GATE3033_3_single_vertex", "gate": "single source vertex is parent-signed", "result": False, "notes": "independent source-weight countermodel survives"}),
    base({"gate_id": "GATE3033_4_common_operator", "gate": "common linear operator is parent-signed", "result": False, "notes": "K0/C_N/operator/boundary normalization missing"}),
    base({"gate_id": "GATE3033_5_Asource_unity", "gate": "A_source=1 is claimable", "result": False, "notes": "equality condition is explicit but not signed"}),
    base({"gate_id": "GATE3033_6_local_GR_claim", "gate": "local GR/Newton reduction is claimable", "result": False, "notes": "coefficient equality, denominator and residual envelope remain open"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3033_0_vertex",
            "decision": "do not promote the single source vertex theorem",
            "rationale": "Hcore and Poisson source shapes are separately visible but not one parent vertex",
            "consequence": "C_psiH=C_WH remains unproved",
        }
    ),
    base(
        {
            "decision_id": "DEC3033_1_formula_shapes",
            "decision": "retain C_psiH and C_WH source-backed formula shapes as nonclaim inputs",
            "rationale": "this is concrete progress beyond missing placeholders without pretending the constants are known",
            "consequence": "the next pass can attack JHrho, C_N, K0 and G_ref directly",
        }
    ),
    base(
        {
            "decision_id": "DEC3033_2_equality_condition",
            "decision": "make the unity condition explicit",
            "rationale": "A_source=1 now reduces to -JHrho/(C_N K0)=4*pi*G_ref/c^2, up to sign convention",
            "consequence": "3034 should target Hcore source-vertex normalization and sign",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3033_0_3034",
            "target_doc": "3034-Y5-R2FR-Hcore-source-vertex-normalization-or-CpsiH-first-value-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_Hcore_source_vertex_normalization_or_CpsiH_first_value_under_AX1090_3034.py",
            "mission": "derive or source JHrho, C_N, K0 and sign convention in the Hcore source vertex; if that fails, keep C_psiH as a formula-only nonclaim row and move to finite bounds",
            "success_condition": "C_psiH becomes a parent-owned finite coefficient or the exact missing Hcore normalization tuple is isolated",
            "forbidden": "no EH-only coefficient import; no orbital-GM denominator; no convention-only A_source=1; no cancellation; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

for key, output_rows in {
    "sources": source_register,
    "source_vertex": source_vertex_rows,
    "common_operator": operator_rows,
    "coefficient_shapes": coefficient_shape_rows,
    "equality_condition": equality_condition_rows,
    "gates": gate_rows,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[key], output_rows)

copy_plan = {
    "vertex_copy": OUTPUTS["source_vertex"],
    "operator_copy": OUTPUTS["common_operator"],
    "coefficient_copy": OUTPUTS["coefficient_shapes"],
    "equality_copy": OUTPUTS["equality_condition"],
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
                "vertex_copy": "parent-action branch copy of single source vertex audit",
                "operator_copy": "local-bound branch copy of common operator audit",
                "coefficient_copy": "local-bound branch copy of coefficient formula-shape rows",
                "equality_copy": "local-bound branch copy of explicit A_source unity condition",
                "next_copy": "RAB acquisition queue handoff",
            }[copy_id],
        }
    )
    for copy_id, source_path in copy_plan.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

claim_rows = source_register + source_vertex_rows + operator_rows + coefficient_shape_rows + equality_condition_rows + gate_rows + decision_rows + next_rows + branch_rows
generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
csv_paths_before_validation = [path for key, path in OUTPUTS.items() if key != "validation"]


def missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(as_str(value) for value in row.values())


validation_rows = [
    {"validation_id": "VAL3033_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": "P8_Y5_R2FR_3033_SOURCE_REGISTER.csv"},
    {"validation_id": "VAL3033_01_csv_parse", "passed": all(csv_ok(path) for path in csv_paths_before_validation), "requirement": "generated CSV rows parse cleanly", "evidence": "all 3033 CSV artifacts except validation import with csv.DictReader"},
    {"validation_id": "VAL3033_02_vertex_rejected", "passed": any(row["current_status"] == "SINGLE_SOURCE_VERTEX_NOT_SIGNED" and not boolish(row["passes_vertex"]) for row in source_vertex_rows), "requirement": "single source vertex fails closed", "evidence": "P8_Y5_R2FR_3033_SINGLE_SOURCE_VERTEX_AUDIT.csv"},
    {"validation_id": "VAL3033_03_operator_rejected", "passed": any(row["current_status"] == "COMMON_OPERATOR_NOT_SIGNED" and not boolish(row["passes_operator"]) for row in operator_rows), "requirement": "common operator fails closed", "evidence": "P8_Y5_R2FR_3033_COMMON_LINEAR_OPERATOR_AUDIT.csv"},
    {"validation_id": "VAL3033_04_coefficient_shapes_present", "passed": {"C_psiH", "C_WH", "delta_A_source"}.issubset({row["symbol"] for row in coefficient_shape_rows}), "requirement": "C_psiH, C_WH and delta_A_source formula-shape rows exist", "evidence": "P8_Y5_R2FR_3033_COEFFICIENT_SOURCE_SHAPE_ROWS.csv"},
    {"validation_id": "VAL3033_05_equality_condition_explicit", "passed": any("-JHrho/(C_N K0)" in row["mathematical_condition"] for row in equality_condition_rows), "requirement": "A_source unity condition is explicit", "evidence": "P8_Y5_R2FR_3033_EQUALITY_CONDITION_ROW.csv"},
    {"validation_id": "VAL3033_06_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if missing_marker(row)), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all generated 3033 claim-control rows"},
    {"validation_id": "VAL3033_07_branch_copies_exist", "passed": all(path.exists() for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies and acquisition queue exist", "evidence": "P8_Y5_R2FR_3033_BRANCH_COPIES.csv"},
    {"validation_id": "VAL3033_08_outputs_scoped", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3033_09_formalization_not_targeted", "passed": all(not under(path, FORMALIZATION) for path in generated_paths), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3033_10_no_shortcuts", "passed": any("no convention-only A_source=1" in row["forbidden"] and "no orbital-GM denominator" in row["forbidden"] for row in next_rows), "requirement": "shortcut guards remain active", "evidence": "P8_Y5_R2FR_3033_NEXT_TARGET.csv"},
    {"validation_id": "VAL3033_11_next_target_selected", "passed": any(boolish(row["selected"]) and "3034" in row["target_doc"] for row in next_rows), "requirement": "next target selects Hcore source-vertex normalization", "evidence": "P8_Y5_R2FR_3033_NEXT_TARGET.csv"},
]

overall = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append({"validation_id": "VAL3033_99_overall", "passed": overall, "requirement": "all 3033 validation checks pass", "evidence": "aggregate of VAL3033_00 through VAL3033_11"})
validation_rows = [base(row) for row in validation_rows]
write_csv(OUTPUTS["validation"], validation_rows)

doc_sections = [
    "# 3033 - Single Source Vertex Or Common Linear Operator under AX1090",
    "",
    "Status: `Y5_R2FR_3033_single_vertex_not_signed_coefficient_shapes_sourced_3034_next`",
    "",
    "## Verdict",
    "",
    "3033 attacks the shortest route to `A_source=1`: prove that the `psi_N` and `W/c^2` equations come from one parent source vertex and one common normalized linear operator.",
    "",
    "That proof does **not** close yet. The Hcore source shape and Poisson/Gauss source shape are both visible, but they are not yet one parent-owned vertex and not yet one parent-owned operator.",
    "",
    "The useful gain is concrete: `C_psiH` is no longer an empty name. The 3024 ansatz gives the nonclaim formula-shape",
    "",
    "`C_psiH = -JHrho/(C_N K0)` if `J_H=JHrho rho_H`,",
    "",
    "while the conditional Poisson/Gauss branch gives",
    "",
    "`C_WH = 4*pi*G_ref/c^2`.",
    "",
    "So the unity condition is now explicit: `A_source=1` requires `-JHrho/(C_N K0)=4*pi*G_ref/c^2`, up to sign convention. This is not a claim, but it is a sharp next derivation target.",
    "",
    "## Single Source Vertex Audit",
    "",
    md_table(source_vertex_rows, ["vertex_id", "object", "current_status", "passes_vertex", "missing_for_claim"]),
    "",
    "## Common Linear Operator Audit",
    "",
    md_table(operator_rows, ["operator_id", "object", "current_status", "passes_operator", "missing_for_claim"]),
    "",
    "## Coefficient Source Shape Rows",
    "",
    md_table(coefficient_shape_rows, ["shape_id", "symbol", "coefficient_formula", "status", "missing_for_claim"]),
    "",
    "## Equality Condition",
    "",
    md_table(equality_condition_rows, ["condition_id", "statement", "mathematical_condition", "current_status", "next_input_needed"]),
    "",
    "## Source Register",
    "",
    md_table(source_register, ["source_id", "exists", "role", "status"]),
    "",
    "## Promotion Gates",
    "",
    md_table(gate_rows, ["gate_id", "gate", "result", "notes"]),
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

print(f"Wrote 3033 checkpoint: {DOC}")
print(f"Overall validation: {overall}")
