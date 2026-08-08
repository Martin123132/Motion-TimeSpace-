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

CHECKPOINT = "3027"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5
IDENTITY_COMBO_BOUND = 4.0 * BETA_BOUND_ABS

DOC = ROOT / "3027-Y5-R2FR-Hcore-kinetic-density-source-or-Cbeta-core-component-fill-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3027_00_3026_doc": ROOT / "3026-Y5-R2FR-coframe-measure-sigmaH-and-Hcore-kinetic-fpsi-extraction-contract-under-AX1090.md",
    "SRC3027_01_3026_contract": RESIDUALS / "P8_Y5_R2FR_3026_SIGMAH_FPSI_EXTRACTION_CONTRACT.csv",
    "SRC3027_02_3026_derivation": RESIDUALS / "P8_Y5_R2FR_3026_EXTRACTION_TO_LAMBDAN_DERIVATION.csv",
    "SRC3027_03_3026_parent_audit": RESIDUALS / "P8_Y5_R2FR_3026_PARENT_DENSITY_AVAILABILITY_AUDIT.csv",
    "SRC3027_04_3026_fill_template": RESIDUALS / "P8_Y5_R2FR_3026_KINETIC_DENSITY_FILL_TEMPLATE.csv",
    "SRC3027_05_3026_anisotropy": RESIDUALS / "P8_Y5_R2FR_3026_ANISOTROPIC_KINETIC_RESIDUAL_GUARD.csv",
    "SRC3027_06_3026_next": RESIDUALS / "P8_Y5_R2FR_3026_NEXT_TARGET.csv",
    "SRC3027_07_3025_bounds": RESIDUALS / "P8_Y5_R2FR_3025_C_BETA_CORE_BOUND_ROWS.csv",
    "SRC3027_08_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3027_09_3006_current_chain": RESIDUALS / "P8_Y5_R2FR_3006_PARENT_CURRENT_CHAIN_AUDIT.csv",
    "SRC3027_10_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3027_11_2923_hcore_checklist": RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv",
    "SRC3027_12_2749_ansatz": RESIDUALS / "P8_Y5_R2FR_2749_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
    "SRC3027_13_1256_reciprocal_hcore": RESIDUALS / "P8_Y5_R10_1256_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3027_SOURCE_REGISTER.csv",
    "hunt": RESIDUALS / "P8_Y5_R2FR_3027_HCORE_KINETIC_DENSITY_SOURCE_HUNT.csv",
    "candidate": RESIDUALS / "P8_Y5_R2FR_3027_PARAMETERIZED_KSCR_SOURCE_ROW_TEMPLATE.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3027_CBETACORE_COMPONENT_FILL_ROWS.csv",
    "validator": RESIDUALS / "P8_Y5_R2FR_3027_COMPONENT_ROW_VALIDATOR.csv",
    "anisotropy": RESIDUALS / "P8_Y5_R2FR_3027_ANISOTROPIC_AND_CROSS_TERM_FILL_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3027_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3027_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3027_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3027_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3027_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hunt_copy": PARENT_ACTION / "Hcore_kinetic_density_source_hunt_3027_NOT_FOUND.csv",
    "candidate_copy": PARENT_ACTION / "parameterized_Kscr_source_row_template_3027_NOT_PARENT_SOURCE.csv",
    "components_copy": LOCAL_BOUNDS / "Cbeta_core_component_fill_rows_3027_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3027_PARENT_LHCORE_DENSITY_OR_COMPONENT_VALUES_NEXT_NONCLAIM.csv",
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
    "SRC3027_00_3026_doc": "3026 handoff: extraction contract defined, parent kinetic density missing",
    "SRC3027_01_3026_contract": "sigma_H/f_psi extraction definitions",
    "SRC3027_02_3026_derivation": "lambda_N_core map derivation",
    "SRC3027_03_3026_parent_audit": "parent density availability audit",
    "SRC3027_04_3026_fill_template": "K0/sigma_H/f_psi/C_beta fill template",
    "SRC3027_05_3026_anisotropy": "anisotropic kinetic guard",
    "SRC3027_06_3026_next": "machine-readable 3027 target",
    "SRC3027_07_3025_bounds": "C_beta_core and identity-combo bounds",
    "SRC3027_08_3024_ansatz": "conditional minimal log-lapse ansatz",
    "SRC3027_09_3006_current_chain": "parent current-chain audit",
    "SRC3027_10_3007_grammar": "parent action grammar",
    "SRC3027_11_2923_hcore_checklist": "Hcore/Q_tau coefficient checklist",
    "SRC3027_12_2749_ansatz": "minimal parent action ansatz candidates",
    "SRC3027_13_1256_reciprocal_hcore": "reciprocal Hcore density, not log-lapse Hcore density",
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

hunt_rows = [
    base(
        {
            "hunt_id": "HUNT3027_0_3026_contract",
            "candidate_source": "3026 extraction contract",
            "candidate_formula": "Kscr_N^{ij}=(-2/C_N) partial L_Hcore/partial(partial_i psi_N partial_j psi_N)",
            "classification": "EXTRACTION_CONTRACT_NOT_SOURCE",
            "why_rejected_or_retained": "defines how to read the density but does not supply L_Hcore",
            "can_compute_sigma_fpsi": False,
        }
    ),
    base(
        {
            "hunt_id": "HUNT3027_1_3024_ansatz",
            "candidate_source": "3024 minimal static Hcore ansatz",
            "candidate_formula": "S_N=-C_N/2 int K_N^{ij}(u,psi_N) partial_i psi_N partial_j psi_N + int J_H psi_N + boundary",
            "classification": "CONDITIONAL_TEMPLATE_NOT_CORPUS_PARENT_SOURCE",
            "why_rejected_or_retained": "usable as a parameterized template, not as parent evidence for values",
            "can_compute_sigma_fpsi": False,
        }
    ),
    base(
        {
            "hunt_id": "HUNT3027_2_3007_grammar",
            "candidate_source": "3007 parent action grammar",
            "candidate_formula": "S_parent^loc sector grammar with coframe/projector/source terms",
            "classification": "GRAMMAR_PROXY_NOT_DENSITY",
            "why_rejected_or_retained": "lists sectors and variation contracts but no psi_N kinetic density",
            "can_compute_sigma_fpsi": False,
        }
    ),
    base(
        {
            "hunt_id": "HUNT3027_3_2923_Hcore_checklist",
            "candidate_source": "2923 Hcore/Q_tau checklist",
            "candidate_formula": "H_core or L_MTS_core field list, derivative order, normalization, source term",
            "classification": "CHECKLIST_SAYS_PARENT_ACTION_BLOCK_MISSING",
            "why_rejected_or_retained": "confirms the missing object instead of filling it",
            "can_compute_sigma_fpsi": False,
        }
    ),
    base(
        {
            "hunt_id": "HUNT3027_4_1256_reciprocal_Hcore",
            "candidate_source": "1256 reciprocal Hcore density",
            "candidate_formula": "H_R = int sqrt(h)[1/2 Z_R h^{ij} D_i R_AB D_j R_AB + ...]",
            "classification": "FOREIGN_FIELD_DENSITY_NOT_PSI_N",
            "why_rejected_or_retained": "valid reciprocal/R_AB scaffold, but it differentiates R_AB rather than psi_N",
            "can_compute_sigma_fpsi": False,
        }
    ),
    base(
        {
            "hunt_id": "HUNT3027_5_EH_anchor",
            "candidate_source": "EH/GR comparator and 2749 EH ansatz",
            "candidate_formula": "S_EH[g_obs]+S_matter",
            "classification": "REFERENCE_ONLY_NOT_MTS_PROOF",
            "why_rejected_or_retained": "would import GR beta rather than derive the MTS Hcore density",
            "can_compute_sigma_fpsi": False,
        }
    ),
    base(
        {
            "hunt_id": "HUNT3027_6_verdict",
            "candidate_source": "current corpus",
            "candidate_formula": "source-backed L_Hcore[psi_N,u,e_obs,Pi_M,Z]",
            "classification": "NOT_FOUND",
            "why_rejected_or_retained": "no source-backed parent log-lapse kinetic density exists yet",
            "can_compute_sigma_fpsi": False,
        }
    ),
]

candidate_rows = [
    base(
        {
            "candidate_id": "KSRC3027_0_parameterized_density",
            "row_type": "source_row_template_not_parent_source",
            "density_template": "L_Hcore^N = -C_N/2 sqrt(hbar) K0[(1+sigma_H u+f_psi psi_N) hbar^{ij}+K_TF^{ij}] partial_i psi_N partial_j psi_N + J_H psi_N + L_boundary",
            "extracts": "K0, sigma_H, f_psi, K_TF^{ij}, J_H/source silence, boundary convention",
            "required_to_promote": "real parent source path; field list; derivative order; C_N normalization; source term; fixed boundary; gauge; values or zero theorems",
            "current_status": "TEMPLATE_ONLY_NONCLAIM",
        }
    ),
    base(
        {
            "candidate_id": "KSRC3027_1_identity_form",
            "row_type": "cancellation_target",
            "density_template": "parent density must imply 2 sigma_H/A_source + f_psi = 0 or bounded C_beta_core",
            "extracts": "C_beta_core",
            "required_to_promote": "identity derived from L_Hcore before fitting, or numeric component values below bound",
            "current_status": "TARGET_ONLY_NONCLAIM",
        }
    ),
]

component_rows = [
    base(
        {
            "component_id": "COMP3027_0_A_source",
            "symbol": "A_source",
            "component_contribution": "denominator for C_sigma=sigma_H/(2 A_source)",
            "required_source": "parent Hcore/source denominator with positive same-frame M_H_ref and no orbital-GM import",
            "value_status": "MISSING_PARENT_LINEAR_COEFFICIENT_MAP",
            "units": "dimensionless",
            "bound_or_gate": "finite nonzero and same source-normalized gauge",
            "source_path": "MISSING_PARENT_SOURCE",
        }
    ),
    base(
        {
            "component_id": "COMP3027_1_K0",
            "symbol": "K0",
            "component_contribution": "normalizes K_tr and derivative extraction",
            "required_source": "positive finite K_tr|0 from L_Hcore",
            "value_status": "MISSING_VALUE",
            "units": "same as K_tr",
            "bound_or_gate": "K0>0",
            "source_path": "MISSING_PARENT_SOURCE",
        }
    ),
    base(
        {
            "component_id": "COMP3027_2_sigma_H",
            "symbol": "sigma_H",
            "component_contribution": "C_sigma=sigma_H/(2 A_source)",
            "required_source": "partial_u ln(K_tr/K0)|0",
            "value_status": "MISSING_VALUE_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "bound_or_gate": "included in abs(C_sigma)+abs(C_f)+abs(C_aniso)+abs(C_gauge)<=7.8e-05 unless parent identity",
            "source_path": "MISSING_PARENT_SOURCE",
        }
    ),
    base(
        {
            "component_id": "COMP3027_3_f_psi",
            "symbol": "f_psi",
            "component_contribution": "C_f=f_psi/4",
            "required_source": "partial_{psi_N} ln(K_tr/K0)|0",
            "value_status": "MISSING_VALUE_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "bound_or_gate": "included in abs(C_sigma)+abs(C_f)+abs(C_aniso)+abs(C_gauge)<=7.8e-05 unless parent identity",
            "source_path": "MISSING_PARENT_SOURCE",
        }
    ),
    base(
        {
            "component_id": "COMP3027_4_C_beta_core",
            "symbol": "C_beta_core",
            "component_contribution": "sigma_H/(2 A_source)+f_psi/4",
            "required_source": "computed from sourced A_source, sigma_H, f_psi or parent zero identity",
            "value_status": "NOT_SCORE_READY",
            "units": "dimensionless",
            "bound_or_gate": f"abs(C_beta_core)<={BETA_BOUND_ABS}",
            "source_path": "MISSING_PARENT_SOURCE",
        }
    ),
    base(
        {
            "component_id": "COMP3027_5_identity_combo",
            "symbol": "2 sigma_H/A_source + f_psi",
            "component_contribution": "4*C_beta_core",
            "required_source": "same as C_beta_core",
            "value_status": "NOT_SCORE_READY",
            "units": "dimensionless",
            "bound_or_gate": f"abs(2 sigma_H/A_source+f_psi)<={IDENTITY_COMBO_BOUND:.6g}",
            "source_path": "MISSING_PARENT_SOURCE",
        }
    ),
]

validator_rows = [
    base(
        {
            "rule_id": "VALR3027_0_source_path",
            "rule": "a component row is not score-ready unless source_path is real and not MISSING_*",
            "current_result": "FAIL_CURRENT_ROWS",
            "claim_effect": "all component rows remain nonclaim",
        }
    ),
    base(
        {
            "rule_id": "VALR3027_1_no_EH_import",
            "rule": "EH/GR comparator rows cannot provide sigma_H, f_psi, or Kscr_N values for MTS",
            "current_result": "PASS_GUARD",
            "claim_effect": "prevents hidden GR smuggling",
        }
    ),
    base(
        {
            "rule_id": "VALR3027_2_no_reciprocal_substitution",
            "rule": "R_AB reciprocal Hcore density cannot stand in for psi_N log-lapse kinetic density",
            "current_result": "PASS_GUARD",
            "claim_effect": "keeps fields unmixed",
        }
    ),
    base(
        {
            "rule_id": "VALR3027_3_no_cancellation",
            "rule": "sigma_H and f_psi cannot cancel unless the identity is parent-derived before fitting",
            "current_result": "PASS_GUARD",
            "claim_effect": "otherwise use absolute component envelope or a sourced C_beta_core row",
        }
    ),
    base(
        {
            "rule_id": "VALR3027_4_anisotropy",
            "rule": "scalar beta trace does not pass unless K_TF and cross/silent terms are zero or bounded",
            "current_result": "FAIL_MISSING_ANISOTROPY_INPUTS",
            "claim_effect": "beta/local PPN remains blocked",
        }
    ),
]

anisotropy_rows = [
    base(
        {
            "anisotropy_id": "ANI3027_0_KTF_background",
            "symbol": "K_TF^{ij}|0",
            "definition": "trace-free background kinetic tensor",
            "required_value": "zero theorem or numeric norm",
            "bound_or_gate": "must vanish for isotropic scalar beta extraction",
            "current_status": "MISSING_VALUE_OR_THEOREM_ZERO",
        }
    ),
    base(
        {
            "anisotropy_id": "ANI3027_1_KTF_u",
            "symbol": "partial_u K_TF^{ij}|0",
            "definition": "u-slope of trace-free kinetic tensor",
            "required_value": "zero theorem or preferred-frame/xi bound row",
            "bound_or_gate": "cannot hide in C_beta_core scalar trace",
            "current_status": "MISSING_VALUE_OR_THEOREM_ZERO",
        }
    ),
    base(
        {
            "anisotropy_id": "ANI3027_2_KTF_psi",
            "symbol": "partial_psi K_TF^{ij}|0",
            "definition": "log-lapse slope of trace-free kinetic tensor",
            "required_value": "zero theorem or PPN anisotropy bound row",
            "bound_or_gate": "blocks scalar-only beta promotion",
            "current_status": "MISSING_VALUE_OR_THEOREM_ZERO",
        }
    ),
    base(
        {
            "anisotropy_id": "ANI3027_3_cross_silent",
            "symbol": "partial_Z ln K_tr and cross terms",
            "definition": "silent/domain/memory cross-coupling into kinetic density",
            "required_value": "double-zero/no-linear-source theorem or component bounds",
            "bound_or_gate": "prevents cosmology/domain memory from leaking into local beta",
            "current_status": "MISSING_SILENT_FIELD_DOUBLE_ZERO_BINDING",
        }
    ),
]

gate_rows = [
    base({"gate_id": "GATE3027_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed hunt ledger"}),
    base({"gate_id": "GATE3027_1_Kscr_source_found", "gate": "source-backed Kscr_N^{ij} found", "result": False, "notes": "only extraction contract, conditional template, grammar and foreign-field density found"}),
    base({"gate_id": "GATE3027_2_template_emitted", "gate": "parameterized Kscr source row template emitted", "result": True, "notes": "template is not parent source"}),
    base({"gate_id": "GATE3027_3_components_staged", "gate": "K0, A_source, sigma_H, f_psi, C_beta_core components staged", "result": True, "notes": "all nonclaim"}),
    base({"gate_id": "GATE3027_4_anisotropy_staged", "gate": "anisotropic/cross-term rows staged", "result": True, "notes": "all missing/nonclaim"}),
    base({"gate_id": "GATE3027_5_Cbeta_score", "gate": "C_beta_core can be scored", "result": False, "notes": "required component values and source path missing"}),
    base({"gate_id": "GATE3027_6_local_GR_claim", "gate": "local GR/Newton reduction claimable", "result": False, "notes": "Hcore density, component values, anisotropy, gamma/beta/source-current gates remain incomplete"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3027_0_source_hunt",
            "decision": "source-backed Kscr_N^{ij} not found",
            "rationale": "available rows are contracts/templates/comparators or reciprocal-field densities, not log-lapse parent Hcore",
            "consequence": "no sigma_H/f_psi computation and no beta claim",
        }
    ),
    base(
        {
            "decision_id": "DEC3027_1_component_fill",
            "decision": "emit strict component fill rows",
            "rationale": "the extraction map is ready, so missing values should now be finite row inputs rather than vague blockers",
            "consequence": "K0, A_source, sigma_H, f_psi, C_beta_core and anisotropy are explicit next inputs",
        }
    ),
    base(
        {
            "decision_id": "DEC3027_2_next",
            "decision": "attempt parent L_Hcore density construction from minimal action grammar",
            "rationale": "if the density can be written as a parent action block, the derivatives can be computed immediately",
            "consequence": "3028 should try the actual L_Hcore density adoption test, otherwise retain component values as bound inputs",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3027_0_3028",
            "target_doc": "3028-Y5-R2FR-parent-LHcore-density-adoption-test-or-Cbeta-component-values-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_parent_LHcore_density_adoption_test_or_Cbeta_component_values_under_AX1090_3028.py",
            "mission": "attempt to adopt or reject a minimal parent L_Hcore^N density with explicit field list, derivative order, source term, boundary convention and variation; if rejected, keep K0/A_source/sigma_H/f_psi/K_TF as strict nonclaim fill rows",
            "success_condition": "either L_Hcore^N becomes a parent action block eligible for variation and coefficient extraction, or the rejection names the exact missing premise and preserves bound inputs",
            "forbidden": "no EH/GR import as MTS proof; no reciprocal R_AB density substitution; no flat-coframe assumption without source; no fitted cancellation; no orbital-GM denominator; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["hunt"], hunt_rows)
write_csv(OUTPUTS["candidate"], candidate_rows)
write_csv(OUTPUTS["components"], component_rows)
write_csv(OUTPUTS["validator"], validator_rows)
write_csv(OUTPUTS["anisotropy"], anisotropy_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

branch_rows = []
for key, source_key in [
    ("hunt_copy", "hunt"),
    ("candidate_copy", "candidate"),
    ("components_copy", "components"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3027_{len(branch_rows)}",
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
claim_rows = source_register + hunt_rows + candidate_rows + component_rows + validator_rows + anisotropy_rows + gate_rows + decision_rows + next_rows

validation_rows = [
    {"validation_id": "VAL3027_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3027_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3027_02_hunt_fail_closed", "passed": any(row["hunt_id"] == "HUNT3027_6_verdict" and row["classification"] == "NOT_FOUND" for row in hunt_rows), "requirement": "Hcore kinetic source hunt fails closed", "evidence": OUTPUTS["hunt"].name},
    {"validation_id": "VAL3027_03_reciprocal_rejected", "passed": any(row["hunt_id"] == "HUNT3027_4_1256_reciprocal_Hcore" and row["classification"] == "FOREIGN_FIELD_DENSITY_NOT_PSI_N" for row in hunt_rows), "requirement": "reciprocal Hcore density is not substituted for psi_N density", "evidence": OUTPUTS["hunt"].name},
    {"validation_id": "VAL3027_04_candidate_template", "passed": any(row["candidate_id"] == "KSRC3027_0_parameterized_density" and "TEMPLATE_ONLY_NONCLAIM" in row["current_status"] for row in candidate_rows), "requirement": "parameterized Kscr source row template exists but is nonclaim", "evidence": OUTPUTS["candidate"].name},
    {"validation_id": "VAL3027_05_component_rows", "passed": all(any(row["component_id"] == required for row in component_rows) for required in ["COMP3027_0_A_source", "COMP3027_1_K0", "COMP3027_2_sigma_H", "COMP3027_3_f_psi", "COMP3027_4_C_beta_core"]), "requirement": "core component fill rows exist", "evidence": OUTPUTS["components"].name},
    {"validation_id": "VAL3027_06_anisotropy_rows", "passed": any(row["anisotropy_id"] == "ANI3027_0_KTF_background" for row in anisotropy_rows), "requirement": "anisotropic kinetic rows exist", "evidence": OUTPUTS["anisotropy"].name},
    {"validation_id": "VAL3027_07_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3027 generated ledgers"},
    {"validation_id": "VAL3027_08_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3027 generated ledgers"},
    {"validation_id": "VAL3027_09_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3027_10_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3027_11_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3027_12_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3028-Y5-R2FR-parent-LHcore-density-adoption-test"), "requirement": "next target selects parent L_Hcore density adoption test", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3027_99_overall",
        "passed": overall_pass,
        "requirement": "all 3027 validation checks pass",
        "evidence": "aggregate of VAL3027_00 through VAL3027_12",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3027 - Hcore Kinetic Density Source Or Cbeta Core Component Fill under AX1090

Status: `Y5_R2FR_3027_Kscr_source_not_found_component_fill_rows_staged_3028_next`

## Verdict

3027 searched for a real parent source row for the effective log-lapse kinetic density

`Kscr_N^{{ij}} = (-2/C_N) partial L_Hcore / partial(partial_i psi_N partial_j psi_N)`.

It was not found.

The corpus contains useful scaffolding: the 3026 extraction contract, the 3024 conditional ansatz, the 3007 parent-action grammar, the 2923 Hcore checklist, and even a 1256 reciprocal Hcore density. But none of these is a source-backed parent `L_Hcore[psi_N]` density for the log-lapse field.

The reciprocal/R_AB Hcore density is explicitly rejected as a substitute: it differentiates `R_AB`, not `psi_N`.

The useful output is therefore a strict fill pack:

- `A_source`
- `K0`
- `sigma_H`
- `f_psi`
- `C_beta_core`
- `K_TF^{{ij}}` and cross/silent kinetic leakage

All remain `valid_for_claim=false`.

## Hcore Kinetic Density Source Hunt

{md_table(hunt_rows, ["hunt_id", "candidate_source", "classification", "why_rejected_or_retained", "can_compute_sigma_fpsi"])}

## Parameterized Kscr Source Row Template

{md_table(candidate_rows, ["candidate_id", "row_type", "density_template", "extracts", "required_to_promote", "current_status"])}

## Cbeta Core Component Fill Rows

{md_table(component_rows, ["component_id", "symbol", "component_contribution", "required_source", "value_status", "bound_or_gate", "source_path"])}

## Component Row Validator

{md_table(validator_rows, ["rule_id", "rule", "current_result", "claim_effect"])}

## Anisotropic And Cross-Term Fill Rows

{md_table(anisotropy_rows, ["anisotropy_id", "symbol", "definition", "required_value", "bound_or_gate", "current_status"])}

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
- `{OUTPUTS["hunt"]}`
- `{OUTPUTS["candidate"]}`
- `{OUTPUTS["components"]}`
- `{OUTPUTS["validator"]}`
- `{OUTPUTS["anisotropy"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["hunt_copy"]}`
- `{BRANCH_OUTPUTS["candidate_copy"]}`
- `{BRANCH_OUTPUTS["components_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass until source-backed `L_Hcore`, `Kscr_N^{{ij}}`, `A_source`, `K0`, `sigma_H`, `f_psi`, gauge, and anisotropy rows exist or are theorem-zero.
- No cancellation credit unless `2 sigma_H/A_source + f_psi = 0` is parent-derived.
- No reciprocal `R_AB` kinetic density substitution for log-lapse `psi_N`.
- No EH/GR import as MTS proof.
- No flat-coframe assumption unless `sigma_H=0` is parent-signed.
- No orbital-`GM` denominator.
- No local-GR/Newton claim from this fill pack alone.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
