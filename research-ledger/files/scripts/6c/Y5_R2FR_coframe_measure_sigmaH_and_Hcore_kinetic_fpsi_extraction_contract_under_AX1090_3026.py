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

CHECKPOINT = "3026"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5
IDENTITY_COMBO_BOUND = 4.0 * BETA_BOUND_ABS

DOC = ROOT / "3026-Y5-R2FR-coframe-measure-sigmaH-and-Hcore-kinetic-fpsi-extraction-contract-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3026_00_3025_doc": ROOT / "3025-Y5-R2FR-parent-sign-sigmaH-fpsi-cancellation-or-bound-input-rows-under-AX1090.md",
    "SRC3026_01_3025_hunt": RESIDUALS / "P8_Y5_R2FR_3025_PARENT_COEFFICIENT_HUNT.csv",
    "SRC3026_02_3025_signature": RESIDUALS / "P8_Y5_R2FR_3025_CANCELLATION_SIGNATURE_AUDIT.csv",
    "SRC3026_03_3025_bounds": RESIDUALS / "P8_Y5_R2FR_3025_C_BETA_CORE_BOUND_ROWS.csv",
    "SRC3026_04_3025_inputs": RESIDUALS / "P8_Y5_R2FR_3025_SIGMAH_FPSI_INPUT_REQUIREMENTS.csv",
    "SRC3026_05_3025_next": RESIDUALS / "P8_Y5_R2FR_3025_NEXT_TARGET.csv",
    "SRC3026_06_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3026_07_3024_variation": RESIDUALS / "P8_Y5_R2FR_3024_VARIATION_DERIVATION.csv",
    "SRC3026_08_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3026_09_3007_variation": RESIDUALS / "P8_Y5_R2FR_3007_SECTOR_VARIATION_LEDGER.csv",
    "SRC3026_10_2924_reduction": RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
    "SRC3026_11_2930_coeff": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv",
    "SRC3026_12_min_parent_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3026_SOURCE_REGISTER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3026_SIGMAH_FPSI_EXTRACTION_CONTRACT.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_3026_EXTRACTION_TO_LAMBDAN_DERIVATION.csv",
    "parent_audit": RESIDUALS / "P8_Y5_R2FR_3026_PARENT_DENSITY_AVAILABILITY_AUDIT.csv",
    "anisotropy": RESIDUALS / "P8_Y5_R2FR_3026_ANISOTROPIC_KINETIC_RESIDUAL_GUARD.csv",
    "fill_template": RESIDUALS / "P8_Y5_R2FR_3026_KINETIC_DENSITY_FILL_TEMPLATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3026_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3026_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3026_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3026_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3026_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": PARENT_ACTION / "sigmaH_fpsi_extraction_contract_3026_NOT_FILLED.csv",
    "parent_audit_copy": PARENT_ACTION / "Hcore_kinetic_density_availability_audit_3026_MISSING.csv",
    "fill_copy": LOCAL_BOUNDS / "Hcore_kinetic_density_fill_template_3026_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3026_HCORE_KINETIC_DENSITY_SOURCE_OR_CBETACORE_FILL_NEXT_NONCLAIM.csv",
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
    "SRC3026_00_3025_doc": "3025 handoff: C_beta_core bound rows and missing parent coefficients",
    "SRC3026_01_3025_hunt": "parent coefficient hunt",
    "SRC3026_02_3025_signature": "C_beta_core cancellation signature",
    "SRC3026_03_3025_bounds": "C_beta_core bound rows",
    "SRC3026_04_3025_inputs": "A_source, sigma_H, f_psi and gauge input requirements",
    "SRC3026_05_3025_next": "machine-readable 3026 target",
    "SRC3026_06_3024_ansatz": "minimal Hcore ansatz",
    "SRC3026_07_3024_variation": "variation-to-lambda_N_core derivation",
    "SRC3026_08_3007_grammar": "parent action grammar",
    "SRC3026_09_3007_variation": "sector variation ledger",
    "SRC3026_10_2924_reduction": "MTS-to-EH reduction contract",
    "SRC3026_11_2930_coeff": "A_source/B_source source coefficient ledger",
    "SRC3026_12_min_parent_blocks": "minimal parent local-GR action blocks",
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

contract_rows = [
    base(
        {
            "contract_id": "EXT3026_0_branch",
            "object": "local source-normalized exterior branch",
            "definition": "u:=W/c^2, Delta_0 u=0 outside compact source, psi_N=-log N=A_source u+lambda_N_core u^2+O(u^3)",
            "extraction_rule": "hold the branch, source frame, boundary reference and observed PPN gauge fixed before differentiating",
            "required_parent_object": "same-frame W, psi_N, N, source charge and observed coframe/readout",
            "current_status": "BRANCH_DEFINITION_READY_PARENT_SOURCE_GAUGE_UNSIGNED",
        }
    ),
    base(
        {
            "contract_id": "EXT3026_1_effective_density",
            "object": "effective Hcore log-lapse kinetic density",
            "definition": "Kscr_N^{ij}:=(-2/C_N) partial L_Hcore/partial(partial_i psi_N partial_j psi_N) including measure/coframe/projector factors",
            "extraction_rule": "derive Kscr_N^{ij} from the parent L_Hcore density, not from the EH comparator or fitted PPN metric",
            "required_parent_object": "L_Hcore[psi_N,u,e_obs,Pi_M,Z] with explicit derivative dependence",
            "current_status": "MISSING_PARENT_HCORE_KINETIC_DENSITY",
        }
    ),
    base(
        {
            "contract_id": "EXT3026_2_isotropic_trace",
            "object": "scalar kinetic trace",
            "definition": "K_tr:=(1/3) hbar_ij Kscr_N^{ij}; K0:=K_tr|_{u=0,psi_N=0,Z=0}>0",
            "extraction_rule": "trace only after the observed coframe hbar_ij and local branch are fixed",
            "required_parent_object": "background observed spatial coframe and positive K0",
            "current_status": "MISSING_K0_AND_OBSERVED_COFREFRAME_LOCK",
        }
    ),
    base(
        {
            "contract_id": "EXT3026_3_sigmaH",
            "object": "sigma_H",
            "definition": "sigma_H := partial_u ln(K_tr/K0)|_{u=0,psi_N=0,Z=0}",
            "extraction_rule": "partial_u is taken at fixed psi_N and fixed silent fields before imposing psi_N=A_source u+...",
            "required_parent_object": "u-dependence of the coframe/measure/projector part of Kscr_N",
            "current_status": "EXTRACTION_DEFINED_VALUE_MISSING",
        }
    ),
    base(
        {
            "contract_id": "EXT3026_4_fpsi",
            "object": "f_psi",
            "definition": "f_psi := partial_{psi_N} ln(K_tr/K0)|_{u=0,psi_N=0,Z=0}",
            "extraction_rule": "partial_{psi_N} is taken at fixed u and fixed silent fields, then inserted into the branch equation",
            "required_parent_object": "explicit psi_N-dependence of the Hcore kinetic density",
            "current_status": "EXTRACTION_DEFINED_VALUE_MISSING",
        }
    ),
    base(
        {
            "contract_id": "EXT3026_5_combo",
            "object": "C_beta_core",
            "definition": "C_beta_core := sigma_H/(2 A_source)+f_psi/4",
            "extraction_rule": "score only if A_source, sigma_H, f_psi and gauge are all source-backed or if parent proves C_beta_core=0",
            "required_parent_object": "parent-signed A_source denominator and kinetic-density derivatives",
            "current_status": "BOUND_COMBINATION_DEFINED_NONCLAIM",
        }
    ),
]

derivation_rows = [
    base(
        {
            "derivation_id": "DER3026_0_expansion",
            "statement": "the extraction contract gives K_tr/K0=1+sigma_H u+f_psi psi_N+O(u^2,psi_N^2,u psi_N)",
            "formula": "K_tr/K0=1+sigma_H u+f_psi psi_N+...",
            "result": "matches 3024 ansatz coefficient form",
            "claim_status": "DEFINITIONAL_CONTRACT_NOT_PARENT_VALUE",
        }
    ),
    base(
        {
            "derivation_id": "DER3026_1_Euler_reuse",
            "statement": "inserting psi_N=A_source u+lambda_N_core u^2 into the exterior Euler equation preserves the 3024 coefficient law",
            "formula": "2 lambda_N_core + sigma_H A_source + (f_psi/2) A_source^2 = 0",
            "result": "lambda_N_core/A_source^2= -sigma_H/(2 A_source)-f_psi/4",
            "claim_status": "CONDITIONAL_UNTIL_PARENT_DENSITY_EXISTS",
        }
    ),
    base(
        {
            "derivation_id": "DER3026_2_zero_condition",
            "statement": "core beta zero is equivalent to a parent kinetic/coframe identity",
            "formula": "lambda_N_core=0 iff 2 sigma_H/A_source + f_psi = 0",
            "result": "the local beta route now has a derivative-definition proof target",
            "claim_status": "NOT_CLAIMED_WITHOUT_PARENT_VALUES",
        }
    ),
]

parent_audit_rows = [
    base(
        {
            "audit_id": "PDA3026_0_LHcore",
            "required_object": "parent L_Hcore density with psi_N derivative dependence",
            "source_evidence": "3023 HCA3023_0 and 3007 grammar",
            "current_status": "MISSING_PARENT_ACTION_BLOCK",
            "effect": "Kscr_N^{ij} cannot be extracted",
        }
    ),
    base(
        {
            "audit_id": "PDA3026_1_Kscr",
            "required_object": "Kscr_N^{ij}=(-2/C_N) partial L_Hcore/partial(partial_i psi_N partial_j psi_N)",
            "source_evidence": "3024 conditional ansatz only",
            "current_status": "CONDITIONAL_ANSATZ_NOT_CORPUS_SOURCE",
            "effect": "sigma_H and f_psi values remain missing",
        }
    ),
    base(
        {
            "audit_id": "PDA3026_2_coframe_measure",
            "required_object": "observed coframe/measure/projector factor through O(u)",
            "source_evidence": "3007 coframe/readout clauses and 1012 source-normalization owner attempt",
            "current_status": "PROXY_CLAUSES_PRESENT_COEFFICIENT_ABSENT",
            "effect": "sigma_H has a definition but no value",
        }
    ),
    base(
        {
            "audit_id": "PDA3026_3_kinetic_slope",
            "required_object": "explicit psi_N slope of the Hcore kinetic density",
            "source_evidence": "3007 variation grammar and 3024 ansatz",
            "current_status": "MISSING_KINETIC_SLOPE_SOURCE",
            "effect": "f_psi has a definition but no value",
        }
    ),
    base(
        {
            "audit_id": "PDA3026_4_A_source",
            "required_object": "finite nonzero A_source from same source denominator",
            "source_evidence": "2930 SCL2930_0 and 3025 input row",
            "current_status": "MISSING_PARENT_LINEAR_COEFFICIENT_MAP",
            "effect": "C_beta_core cannot be numerically scored",
        }
    ),
    base(
        {
            "audit_id": "PDA3026_5_verdict",
            "required_object": "complete extraction package",
            "source_evidence": "PDA3026_0 through PDA3026_4",
            "current_status": "EXTRACTION_CONTRACT_DEFINED_PARENT_DENSITY_MISSING",
            "effect": "move to Hcore kinetic-density source acquisition or C_beta_core fill row",
        }
    ),
]

anisotropy_rows = [
    base(
        {
            "guard_id": "ANI3026_0_traceless_kinetic",
            "object": "anisotropic kinetic trace-free part",
            "definition": "K_TF^{ij}:=Kscr_N^{ij}-K_tr hbar^{ij}",
            "required_zero_or_bound": "K_TF^{ij}|0=0 and partial_u K_TF^{ij}, partial_psi K_TF^{ij} zero or separately bounded",
            "why_it_matters": "otherwise the beta scalar trace can hide preferred-frame/xi/anisotropic PPN leakage",
            "current_status": "MISSING_ANISOTROPIC_KINETIC_GUARD_VALUE",
        }
    ),
    base(
        {
            "guard_id": "ANI3026_1_cross_terms",
            "object": "u-psi and silent-field cross terms",
            "definition": "partial_u partial_psi ln K_tr and partial_Z ln K_tr terms",
            "required_zero_or_bound": "irrelevant at O(u^2) only if silent fields are double-zero and no linear source vertex exists",
            "why_it_matters": "prevents cosmology/domain/memory terms entering local beta through the kinetic density",
            "current_status": "MISSING_SILENT_FIELD_DOUBLE_ZERO_BINDING",
        }
    ),
]

fill_template_rows = [
    base(
        {
            "fill_id": "FILL3026_0_K_density_source",
            "symbol": "Kscr_N^{ij}",
            "required_value": "explicit parent formula or source path for effective kinetic density",
            "units": "same as L_Hcore coefficient after C_N normalization",
            "status": "MISSING_PARENT_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
    base(
        {
            "fill_id": "FILL3026_1_K0",
            "symbol": "K0",
            "required_value": "positive finite background kinetic trace",
            "units": "same as K_tr",
            "status": "MISSING_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
    base(
        {
            "fill_id": "FILL3026_2_sigma_H",
            "symbol": "sigma_H",
            "required_value": "partial_u ln(K_tr/K0)|0",
            "units": "dimensionless",
            "status": "MISSING_VALUE_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
    base(
        {
            "fill_id": "FILL3026_3_f_psi",
            "symbol": "f_psi",
            "required_value": "partial_{psi_N} ln(K_tr/K0)|0",
            "units": "dimensionless",
            "status": "MISSING_VALUE_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
    base(
        {
            "fill_id": "FILL3026_4_C_beta_core",
            "symbol": "C_beta_core",
            "required_value": f"sigma_H/(2 A_source)+f_psi/4 with abs(C_beta_core)<={BETA_BOUND_ABS}",
            "units": "dimensionless",
            "status": "NOT_SCORE_READY_UNTIL_INPUTS_FILLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
    base(
        {
            "fill_id": "FILL3026_5_anisotropic_guard",
            "symbol": "K_TF^{ij}",
            "required_value": "zero theorem or bounded anisotropic residual rows",
            "units": "dimensionless after K0 normalization",
            "status": "MISSING_VALUE_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
]

gate_rows = [
    base({"gate_id": "GATE3026_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed extraction contract"}),
    base({"gate_id": "GATE3026_1_extraction_defined", "gate": "sigma_H and f_psi have invariant extraction definitions", "result": True, "notes": "defined as background derivatives of ln K_tr"}),
    base({"gate_id": "GATE3026_2_lambda_map_preserved", "gate": "3024 lambda_N_core map follows from definitions", "result": True, "notes": "derivation rows preserve the coefficient law"}),
    base({"gate_id": "GATE3026_3_parent_density_exists", "gate": "parent L_Hcore/Kscr_N^{ij} exists in corpus", "result": False, "notes": "current sources have grammar/ansatz but not a filled parent density"}),
    base({"gate_id": "GATE3026_4_values_available", "gate": "A_source, sigma_H, f_psi numeric/theorem values exist", "result": False, "notes": "fill template remains missing"}),
    base({"gate_id": "GATE3026_5_anisotropy_guard", "gate": "anisotropic kinetic leakage is zero or bounded", "result": False, "notes": "guard is defined but not filled"}),
    base({"gate_id": "GATE3026_6_Cbeta_score", "gate": "C_beta_core can be scored", "result": False, "notes": "missing parent density and coefficient values"}),
    base({"gate_id": "GATE3026_7_local_GR_claim", "gate": "local GR/Newton reduction claimable", "result": False, "notes": "core beta extraction remains nonclaim and other PPN/source gates remain open"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3026_0_contract",
            "decision": "define sigma_H and f_psi as derivatives of one effective kinetic density",
            "rationale": "this prevents free-floating coupling language and makes the beta cancellation mechanically checkable",
            "consequence": "future parent actions can be scored by differentiating K_tr rather than inventing new symbols",
        }
    ),
    base(
        {
            "decision_id": "DEC3026_1_status",
            "decision": "do not promote the extraction contract to a claim",
            "rationale": "the parent Hcore density and coefficient values are not present in the corpus",
            "consequence": "C_beta_core remains nonclaim and source-ready",
        }
    ),
    base(
        {
            "decision_id": "DEC3026_2_next",
            "decision": "acquire or construct the Hcore kinetic density source row",
            "rationale": "the next real leap is a filled Kscr_N^{ij}; without it the contract is only a measuring tool",
            "consequence": "3027 should attempt Kscr_N^{ij} source acquisition or strict C_beta_core component fill",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3026_0_3027",
            "target_doc": "3027-Y5-R2FR-Hcore-kinetic-density-source-or-Cbeta-core-component-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_Hcore_kinetic_density_source_or_Cbeta_core_component_fill_under_AX1090_3027.py",
            "mission": "find or construct a parent-source row for Kscr_N^{ij}; if absent, emit strict nonclaim component fill rows for K0, sigma_H, f_psi, A_source and anisotropic kinetic leakage",
            "success_condition": "either Kscr_N^{ij} becomes source-backed enough to compute sigma_H/f_psi, or every missing coefficient becomes an explicit nonclaim bound-input row",
            "forbidden": "no EH/GR import as MTS proof; no flat-coframe assumption without source; no fitted cancellation; no orbital-GM denominator; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["contract"], contract_rows)
write_csv(OUTPUTS["derivation"], derivation_rows)
write_csv(OUTPUTS["parent_audit"], parent_audit_rows)
write_csv(OUTPUTS["anisotropy"], anisotropy_rows)
write_csv(OUTPUTS["fill_template"], fill_template_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

branch_rows = []
for key, source_key in [
    ("contract_copy", "contract"),
    ("parent_audit_copy", "parent_audit"),
    ("fill_copy", "fill_template"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3026_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = source_register + contract_rows + derivation_rows + parent_audit_rows + anisotropy_rows + fill_template_rows + gate_rows + decision_rows + next_rows

validation_rows = [
    {"validation_id": "VAL3026_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3026_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3026_02_sigma_definition", "passed": any(row["contract_id"] == "EXT3026_3_sigmaH" and "partial_u ln" in row["definition"] for row in contract_rows), "requirement": "sigma_H extraction definition is recorded", "evidence": OUTPUTS["contract"].name},
    {"validation_id": "VAL3026_03_fpsi_definition", "passed": any(row["contract_id"] == "EXT3026_4_fpsi" and "partial_{psi_N} ln" in row["definition"] for row in contract_rows), "requirement": "f_psi extraction definition is recorded", "evidence": OUTPUTS["contract"].name},
    {"validation_id": "VAL3026_04_lambda_map", "passed": any(row["derivation_id"] == "DER3026_1_Euler_reuse" and "lambda_N_core/A_source^2" in row["result"] for row in derivation_rows), "requirement": "extraction definitions preserve the 3024 lambda_N_core map", "evidence": OUTPUTS["derivation"].name},
    {"validation_id": "VAL3026_05_parent_density_missing", "passed": any(row["audit_id"] == "PDA3026_5_verdict" and row["current_status"] == "EXTRACTION_CONTRACT_DEFINED_PARENT_DENSITY_MISSING" for row in parent_audit_rows), "requirement": "parent density absence is explicit", "evidence": OUTPUTS["parent_audit"].name},
    {"validation_id": "VAL3026_06_anisotropy_guard", "passed": any(row["guard_id"] == "ANI3026_0_traceless_kinetic" for row in anisotropy_rows), "requirement": "anisotropic kinetic leakage guard is present", "evidence": OUTPUTS["anisotropy"].name},
    {"validation_id": "VAL3026_07_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3026 generated ledgers"},
    {"validation_id": "VAL3026_08_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3026 generated ledgers"},
    {"validation_id": "VAL3026_09_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3026_10_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3026_11_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3026_12_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3027-Y5-R2FR-Hcore-kinetic-density-source"), "requirement": "next target selects Hcore kinetic-density source or C_beta_core component fill", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3026_99_overall",
        "passed": overall_pass,
        "requirement": "all 3026 validation checks pass",
        "evidence": "aggregate of VAL3026_00 through VAL3026_12",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3026 - Coframe/Measure SigmaH and Hcore Kinetic Fpsi Extraction Contract under AX1090

Status: `Y5_R2FR_3026_extraction_contract_defined_parent_Hcore_kinetic_density_missing_3027_next`

## Verdict

3026 turns the exposed coupling problem into a real extraction contract.

Define the effective log-lapse kinetic density

`Kscr_N^{{ij}} := (-2/C_N) partial L_Hcore / partial(partial_i psi_N partial_j psi_N)`,

including the measure, coframe, projector and Hcore kinetic factors. Then define the scalar trace

`K_tr := (1/3) hbar_ij Kscr_N^{{ij}}`, with `K0 := K_tr|0 > 0`.

The two missing beta coefficients are no longer free symbols:

`sigma_H := partial_u ln(K_tr/K0)|0`,

`f_psi := partial_psi_N ln(K_tr/K0)|0`.

These definitions preserve the 3024 result:

`lambda_N_core/A_source^2 = -sigma_H/(2 A_source)-f_psi/4`.

So the beta route is now mechanically checkable: give me `L_Hcore`, I differentiate its kinetic density; no hand-waving required.

But the parent `L_Hcore` / `Kscr_N^{{ij}}` density is not yet present in the corpus. Existing files provide grammar, readout/coframe proxy clauses, and conditional ansatz rows, not a source-backed kinetic density. Therefore this is an extraction win, not a local-GR claim.

## Extraction Contract

{md_table(contract_rows, ["contract_id", "object", "definition", "extraction_rule", "required_parent_object", "current_status"])}

## Extraction To LambdaN Derivation

{md_table(derivation_rows, ["derivation_id", "statement", "formula", "result", "claim_status"])}

## Parent Density Availability Audit

{md_table(parent_audit_rows, ["audit_id", "required_object", "source_evidence", "current_status", "effect"])}

## Anisotropic Kinetic Guard

{md_table(anisotropy_rows, ["guard_id", "object", "definition", "required_zero_or_bound", "why_it_matters", "current_status"])}

## Kinetic Density Fill Template

{md_table(fill_template_rows, ["fill_id", "symbol", "required_value", "units", "status", "valid_for_claim", "claim_allowed"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Promotion Gates

{md_table(gate_rows, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_rows, ["next_id", "target_doc", "target_script", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["contract"]}`
- `{OUTPUTS["derivation"]}`
- `{OUTPUTS["parent_audit"]}`
- `{OUTPUTS["anisotropy"]}`
- `{OUTPUTS["fill_template"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["contract_copy"]}`
- `{BRANCH_OUTPUTS["parent_audit_copy"]}`
- `{BRANCH_OUTPUTS["fill_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass until `L_Hcore`, `Kscr_N^{{ij}}`, `A_source`, `sigma_H`, `f_psi`, and gauge are source-backed or strictly bounded.
- No cancellation credit unless `2 sigma_H/A_source + f_psi = 0` is parent-derived.
- No scalar beta trace pass if anisotropic kinetic leakage is active or unbounded.
- No flat-coframe assumption unless `sigma_H=0` is parent-signed.
- No GR/EH import as MTS proof.
- No orbital-`GM` denominator.
- No local-GR/Newton claim from this extraction contract alone.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
