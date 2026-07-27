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

CHECKPOINT = "3025"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5
COMBO_BOUND_ABS = 4.0 * BETA_BOUND_ABS
SIGMA_OVER_A_BOUND_IF_FZERO = 2.0 * BETA_BOUND_ABS

DOC = ROOT / "3025-Y5-R2FR-parent-sign-sigmaH-fpsi-cancellation-or-bound-input-rows-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3025_00_3024_doc": ROOT / "3024-Y5-R2FR-minimal-Hcore-action-ansatz-or-lambdaN-core-numeric-intake-under-AX1090.md",
    "SRC3025_01_3024_coeff": RESIDUALS / "P8_Y5_R2FR_3024_LAMBDAN_CORE_COEFFICIENT_MAP.csv",
    "SRC3025_02_3024_bound": RESIDUALS / "P8_Y5_R2FR_3024_KINETIC_SLOPE_BOUND_TRANSLATION.csv",
    "SRC3025_03_3024_next": RESIDUALS / "P8_Y5_R2FR_3024_NEXT_TARGET.csv",
    "SRC3025_04_3023_hcore": RESIDUALS / "P8_Y5_R2FR_3023_HCORE_ACTION_BLOCK_AUDIT.csv",
    "SRC3025_05_3022_owner": RESIDUALS / "P8_Y5_R2FR_3022_PSIN_HAMILTONIAN_OWNER_AUDIT.csv",
    "SRC3025_06_3020_lapse": RESIDUALS / "P8_Y5_R2FR_3020_LAPSE_COEFFICIENT_MAP.csv",
    "SRC3025_07_2930_coeff": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv",
    "SRC3025_08_2920_square": RESIDUALS / "P8_Y5_R2FR_2920_PARENT_SQUARE_LAW_AUDIT.csv",
    "SRC3025_09_2924_reduction": RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
    "SRC3025_10_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3025_11_3007_variation": RESIDUALS / "P8_Y5_R2FR_3007_SECTOR_VARIATION_LEDGER.csv",
    "SRC3025_12_min_parent_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3025_13_hamiltonian_measure": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "SRC3025_14_1009_parent_current": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "SRC3025_15_1012_source_norm": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
    "SRC3025_16_1015_hilbert_equality": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
}

PARENT_SEARCH_IDS = [
    "SRC3025_04_3023_hcore",
    "SRC3025_05_3022_owner",
    "SRC3025_06_3020_lapse",
    "SRC3025_07_2930_coeff",
    "SRC3025_08_2920_square",
    "SRC3025_09_2924_reduction",
    "SRC3025_10_3007_grammar",
    "SRC3025_11_3007_variation",
    "SRC3025_12_min_parent_blocks",
    "SRC3025_13_hamiltonian_measure",
    "SRC3025_14_1009_parent_current",
    "SRC3025_15_1012_source_norm",
    "SRC3025_16_1015_hilbert_equality",
]

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3025_SOURCE_REGISTER.csv",
    "hunt": RESIDUALS / "P8_Y5_R2FR_3025_PARENT_COEFFICIENT_HUNT.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_3025_CANCELLATION_SIGNATURE_AUDIT.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3025_C_BETA_CORE_BOUND_ROWS.csv",
    "inputs": RESIDUALS / "P8_Y5_R2FR_3025_SIGMAH_FPSI_INPUT_REQUIREMENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3025_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3025_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3025_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3025_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3025_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "signature_copy": PARENT_ACTION / "sigmaH_fpsi_parent_signature_audit_3025_NOT_SIGNED.csv",
    "bounds_copy": LOCAL_BOUNDS / "C_beta_core_bound_rows_3025_NONCLAIM.csv",
    "inputs_copy": LOCAL_BOUNDS / "sigmaH_fpsi_input_requirements_3025_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3025_COFREFRAME_KINETIC_EXPANSION_EXTRACTION_NEXT_NONCLAIM.csv",
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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def count_hits(pattern: str, paths: list[Path]) -> int:
    target = pattern.lower()
    return sum(read_text(path).lower().count(target) for path in paths)


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
    "SRC3025_00_3024_doc": "3024 handoff: conditional Hcore ansatz and lambda_N_core map",
    "SRC3025_01_3024_coeff": "lambda_N_core coefficient map and zero condition",
    "SRC3025_02_3024_bound": "bound translation for C_beta_core",
    "SRC3025_03_3024_next": "machine-readable 3025 target",
    "SRC3025_04_3023_hcore": "Hcore action block audit still not filled",
    "SRC3025_05_3022_owner": "psi_N owner audit",
    "SRC3025_06_3020_lapse": "lapse/log-lapse coefficient map",
    "SRC3025_07_2930_coeff": "A_source/B_source source coefficient ledger",
    "SRC3025_08_2920_square": "parent square-law audit",
    "SRC3025_09_2924_reduction": "MTS-to-EH reduction contract",
    "SRC3025_10_3007_grammar": "parent action grammar and coframe/readout clauses",
    "SRC3025_11_3007_variation": "sector variation ledger",
    "SRC3025_12_min_parent_blocks": "minimal parent local-GR action block list",
    "SRC3025_13_hamiltonian_measure": "Hamiltonian source-measure contract",
    "SRC3025_14_1009_parent_current": "parent current chain contract",
    "SRC3025_15_1012_source_norm": "source-normalization owner theorem attempt",
    "SRC3025_16_1015_hilbert_equality": "topological-Hilbert equality/source measure attempt",
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

parent_paths = [SOURCE_PATHS[source_id] for source_id in PARENT_SEARCH_IDS]
sigma_hits = count_hits("sigma_H", parent_paths)
fpsi_hits = count_hits("f_psi", parent_paths) + count_hits("fpsi", parent_paths)
zero_hits = count_hits("2 sigma_H/A_source + f_psi", parent_paths)

hunt_rows = [
    base(
        {
            "hunt_id": "HUNT3025_0_A_source",
            "target": "A_source",
            "search_result": "MENTIONED_BUT_NOT_PARENT_SIGNED",
            "evidence": "2930 SCL2930_0 marks A_source as MISSING_PARENT_LINEAR_COEFFICIENT_MAP; 3023/3022 require positive same-frame denominator",
            "found_numeric_value": False,
            "found_parent_theorem": False,
            "required_next": "extract A_source from Hcore/source denominator or keep bound rows nonclaim",
        }
    ),
    base(
        {
            "hunt_id": "HUNT3025_1_sigma_H",
            "target": "sigma_H",
            "search_result": "NO_PARENT_COEFFICIENT_ROW_FOUND",
            "evidence": f"parent-search exact sigma_H hits excluding 3024 formula source = {sigma_hits}",
            "found_numeric_value": False,
            "found_parent_theorem": False,
            "required_next": "derive from coframe/measure/projector expansion in the observed source branch",
        }
    ),
    base(
        {
            "hunt_id": "HUNT3025_2_f_psi",
            "target": "f_psi",
            "search_result": "NO_PARENT_KINETIC_SLOPE_ROW_FOUND",
            "evidence": f"parent-search exact f_psi/fpsi hits excluding 3024 formula source = {fpsi_hits}",
            "found_numeric_value": False,
            "found_parent_theorem": False,
            "required_next": "derive from the parent log-lapse kinetic density or create a sourced coefficient row",
        }
    ),
    base(
        {
            "hunt_id": "HUNT3025_3_coframe_proxy",
            "target": "coframe/readout proxy for sigma_H",
            "search_result": "PROXY_CLAUSES_PRESENT_COEFFICIENT_ABSENT",
            "evidence": "3007, 1009 and 1012 mention same observed coframe/readout, but no first-order expansion coefficient sigma_H",
            "found_numeric_value": False,
            "found_parent_theorem": False,
            "required_next": "define sigma_H as a derivative/extraction functional of the parent coframe density",
        }
    ),
    base(
        {
            "hunt_id": "HUNT3025_4_kinetic_proxy",
            "target": "Hcore kinetic proxy for f_psi",
            "search_result": "GRAMMAR_PRESENT_KINETIC_SLOPE_ABSENT",
            "evidence": "3007 has action grammar and variation grammar, but no owned Hcore log-lapse kinetic metric K_N(psi_N)",
            "found_numeric_value": False,
            "found_parent_theorem": False,
            "required_next": "write the extraction contract for f_psi from K_N^{ij}",
        }
    ),
    base(
        {
            "hunt_id": "HUNT3025_5_cancellation_identity",
            "target": "2 sigma_H/A_source + f_psi = 0",
            "search_result": "IDENTITY_NOT_FOUND_OUTSIDE_3024_DERIVATION",
            "evidence": f"parent-search exact cancellation hits excluding 3024 formula source = {zero_hits}",
            "found_numeric_value": False,
            "found_parent_theorem": False,
            "required_next": "prove the identity from a parent action or disallow cancellation credit",
        }
    ),
    base(
        {
            "hunt_id": "HUNT3025_6_verdict",
            "target": "parent-signed core beta cancellation",
            "search_result": "NOT_SIGNED",
            "evidence": "A_source remains unsigned; sigma_H and f_psi have no parent rows; cancellation identity is absent",
            "found_numeric_value": False,
            "found_parent_theorem": False,
            "required_next": "stage C_beta_core as a strict nonclaim bound-input family",
        }
    ),
]

signature_rows = [
    base(
        {
            "signature_id": "SIG3025_0_formula",
            "object": "core beta residual combination",
            "mathematical_form": "C_beta_core = sigma_H/(2 A_source)+f_psi/4",
            "condition_for_zero": "C_beta_core=0",
            "equivalent_identity": "2 sigma_H/A_source + f_psi = 0",
            "current_status": "DERIVED_BY_3024_NOT_PARENT_SIGNED",
            "promotion_policy": "may be used as theorem-zero only if parent action signs A_source, sigma_H, f_psi and the identity before fitting",
        }
    ),
    base(
        {
            "signature_id": "SIG3025_1_no_posthoc_cancellation",
            "object": "cancellation discipline",
            "mathematical_form": "do not score sigma_H and f_psi by tuned cancellation unless identity is derived",
            "condition_for_zero": "identity must be structural, not fitted",
            "equivalent_identity": "same source-normalized observed branch, same denominator, same gauge",
            "current_status": "GUARD_ACTIVE",
            "promotion_policy": "without identity, score abs(C_beta_core) as a single sourced combination or score conservative component envelopes",
        }
    ),
    base(
        {
            "signature_id": "SIG3025_2_GR_like_reference",
            "object": "GR-like morphology",
            "mathematical_form": "A_source=1, sigma_H=1, f_psi=-2 -> C_beta_core=0",
            "condition_for_zero": "reference morphology only",
            "equivalent_identity": "2*1/1 + (-2) = 0",
            "current_status": "REFERENCE_ONLY_NOT_MTS_PROOF",
            "promotion_policy": "cannot be imported; MTS must derive the values",
        }
    ),
]

bound_rows = [
    base(
        {
            "bound_id": "CBR3025_0_C_beta_core",
            "quantity": "C_beta_core",
            "definition": "sigma_H/(2 A_source)+f_psi/4",
            "required_for_claim": "numeric/source-backed A_source, sigma_H, f_psi or parent-signed zero identity",
            "bound_formula": f"abs(C_beta_core) <= {BETA_BOUND_ABS}",
            "numeric_bound": BETA_BOUND_ABS,
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SIGMAH_FPSI_SOURCE",
            "current_status": "NONCLAIM_BOUND_INPUT",
        }
    ),
    base(
        {
            "bound_id": "CBR3025_1_identity_combo",
            "quantity": "2 sigma_H/A_source + f_psi",
            "definition": "four times C_beta_core",
            "required_for_claim": "same as CBR3025_0",
            "bound_formula": f"abs(2 sigma_H/A_source + f_psi) <= {COMBO_BOUND_ABS:.6g}",
            "numeric_bound": COMBO_BOUND_ABS,
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SIGMAH_FPSI_SOURCE",
            "current_status": "NONCLAIM_BOUND_INPUT",
        }
    ),
    base(
        {
            "bound_id": "CBR3025_2_flat_coframe_special",
            "quantity": "f_psi if sigma_H=0",
            "definition": "flat/silent coframe special case only",
            "required_for_claim": "parent-signed sigma_H=0 plus sourced f_psi",
            "bound_formula": f"abs(f_psi) <= {COMBO_BOUND_ABS:.6g}",
            "numeric_bound": COMBO_BOUND_ABS,
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SIGMAH_ZERO_AND_FPSI_SOURCE",
            "current_status": "SPECIAL_CASE_NONCLAIM",
        }
    ),
    base(
        {
            "bound_id": "CBR3025_3_zero_kinetic_slope_special",
            "quantity": "sigma_H/A_source if f_psi=0",
            "definition": "zero kinetic slope special case only",
            "required_for_claim": "parent-signed f_psi=0 plus sourced sigma_H/A_source",
            "bound_formula": f"abs(sigma_H/A_source) <= {SIGMA_OVER_A_BOUND_IF_FZERO:.6g}",
            "numeric_bound": SIGMA_OVER_A_BOUND_IF_FZERO,
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_FPSI_ZERO_AND_SIGMAH_SOURCE",
            "current_status": "SPECIAL_CASE_NONCLAIM",
        }
    ),
]

input_rows = [
    base(
        {
            "input_id": "INP3025_0_A_source",
            "symbol": "A_source",
            "meaning": "first-order source-normalized log-lapse/source coefficient",
            "required_source": "Hcore/source denominator with positive same-frame M_H_ref and no orbital-GM import",
            "current_status": "MISSING_PARENT_LINEAR_COEFFICIENT_MAP",
            "claim_effect": "C_beta_core cannot be scored",
        }
    ),
    base(
        {
            "input_id": "INP3025_1_sigma_H",
            "symbol": "sigma_H",
            "meaning": "first-order coframe/measure/projection drift in the Hcore kinetic density",
            "required_source": "observed coframe/measure/projector expansion in the local source-normalized branch",
            "current_status": "MISSING_PARENT_COFREFRAME_MEASURE_COEFFICIENT",
            "claim_effect": "zero condition cannot be signed",
        }
    ),
    base(
        {
            "input_id": "INP3025_2_f_psi",
            "symbol": "f_psi",
            "meaning": "explicit log-lapse kinetic coupling slope",
            "required_source": "parent Hcore kinetic metric/density expansion with variation",
            "current_status": "MISSING_PARENT_KINETIC_SLOPE",
            "claim_effect": "zero condition cannot be signed",
        }
    ),
    base(
        {
            "input_id": "INP3025_3_gauge",
            "symbol": "observed PPN/source gauge",
            "meaning": "same branch for psi_N, W, source charge, clocks and readout",
            "required_source": "fixed readout/coframe/source frame through O(W^2)",
            "current_status": "MISSING_OBSERVED_SOURCE_NORMALIZED_GAUGE",
            "claim_effect": "comparison to beta bound remains schema-only",
        }
    ),
]

gate_rows = [
    base({"gate_id": "GATE3025_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed coefficient hunt"}),
    base({"gate_id": "GATE3025_1_A_source", "gate": "A_source parent signed", "result": False, "notes": "2930 and 3023 still mark denominator/linear coefficient missing"}),
    base({"gate_id": "GATE3025_2_sigma_H", "gate": "sigma_H parent signed", "result": False, "notes": "no parent coefficient row found"}),
    base({"gate_id": "GATE3025_3_f_psi", "gate": "f_psi parent signed", "result": False, "notes": "no parent kinetic slope row found"}),
    base({"gate_id": "GATE3025_4_zero_identity", "gate": "2 sigma_H/A_source + f_psi = 0 parent signed", "result": False, "notes": "identity only exists as 3024 derived target, not corpus source"}),
    base({"gate_id": "GATE3025_5_bound_rows", "gate": "C_beta_core bound rows staged", "result": True, "notes": "rows are source-ready but nonclaim"}),
    base({"gate_id": "GATE3025_6_beta_core_score", "gate": "core beta residual can be scored", "result": False, "notes": "missing parent values/gauge/source paths"}),
    base({"gate_id": "GATE3025_7_local_GR_claim", "gate": "local GR/Newton reduction claimable", "result": False, "notes": "core beta cancellation, total beta envelope, gamma, alpha3/source-current and source bridge remain incomplete"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3025_0_hunt",
            "decision": "parent-sign hunt fails",
            "rationale": "A_source is still missing and no parent rows for sigma_H/f_psi or their cancellation were found",
            "consequence": "do not claim lambda_N_core=0",
        }
    ),
    base(
        {
            "decision_id": "DEC3025_1_bounds",
            "decision": "stage C_beta_core bound rows",
            "rationale": "3024 gave an exact formula, so the fallback should be a precise coefficient-combination bound rather than vague beta language",
            "consequence": "the core beta wound becomes a finite input target",
        }
    ),
    base(
        {
            "decision_id": "DEC3025_2_next",
            "decision": "derive extraction definitions for sigma_H and f_psi",
            "rationale": "the corpus has coframe/readout and action grammar proxies, but not the derivative definitions that would turn them into coefficients",
            "consequence": "3026 should define and attempt the coframe/kinetic expansion extraction contract",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3025_0_3026",
            "target_doc": "3026-Y5-R2FR-coframe-measure-sigmaH-and-Hcore-kinetic-fpsi-extraction-contract-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_coframe_measure_sigmaH_and_Hcore_kinetic_fpsi_extraction_contract_under_AX1090_3026.py",
            "mission": "derive invariant extraction definitions for sigma_H and f_psi from the parent coframe/measure/projector density and Hcore kinetic metric; if extraction cannot be sourced, keep C_beta_core as strict nonclaim bound rows",
            "success_condition": "sigma_H and f_psi become parent-extractable coefficients with source paths, or the extraction contract names the exact missing parent density and kinetic metric",
            "forbidden": "no GR/EH import as MTS proof; no flat-coframe assumption unless sourced; no fitted cancellation; no orbital-GM denominator; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["hunt"], hunt_rows)
write_csv(OUTPUTS["signature"], signature_rows)
write_csv(OUTPUTS["bounds"], bound_rows)
write_csv(OUTPUTS["inputs"], input_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

branch_rows = []
for key, source_key in [
    ("signature_copy", "signature"),
    ("bounds_copy", "bounds"),
    ("inputs_copy", "inputs"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3025_{len(branch_rows)}",
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
claim_rows = source_register + hunt_rows + signature_rows + bound_rows + input_rows + gate_rows + decision_rows + next_rows

validation_rows = [
    {"validation_id": "VAL3025_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3025_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3025_02_hunt_records_missing", "passed": any(row["hunt_id"] == "HUNT3025_6_verdict" and row["search_result"] == "NOT_SIGNED" for row in hunt_rows), "requirement": "parent coefficient hunt fails closed", "evidence": OUTPUTS["hunt"].name},
    {"validation_id": "VAL3025_03_signature_formula", "passed": any(row["signature_id"] == "SIG3025_0_formula" and "sigma_H" in row["mathematical_form"] and "f_psi" in row["mathematical_form"] for row in signature_rows), "requirement": "C_beta_core signature is recorded", "evidence": OUTPUTS["signature"].name},
    {"validation_id": "VAL3025_04_bound_rows", "passed": any(row["bound_id"] == "CBR3025_0_C_beta_core" and float(row["numeric_bound"]) == BETA_BOUND_ABS for row in bound_rows) and any(row["bound_id"] == "CBR3025_1_identity_combo" and float(row["numeric_bound"]) == COMBO_BOUND_ABS for row in bound_rows), "requirement": "bound rows translate the beta comparator correctly", "evidence": OUTPUTS["bounds"].name},
    {"validation_id": "VAL3025_05_inputs_named", "passed": all(any(row["input_id"] == required for row in input_rows) for required in ["INP3025_0_A_source", "INP3025_1_sigma_H", "INP3025_2_f_psi", "INP3025_3_gauge"]), "requirement": "all required input coefficients are explicitly named", "evidence": OUTPUTS["inputs"].name},
    {"validation_id": "VAL3025_06_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3025 generated ledgers"},
    {"validation_id": "VAL3025_07_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3025 generated ledgers"},
    {"validation_id": "VAL3025_08_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3025_09_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3025_10_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3025_11_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3026-Y5-R2FR-coframe-measure-sigmaH"), "requirement": "next target selects coefficient extraction contract", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3025_99_overall",
        "passed": overall_pass,
        "requirement": "all 3025 validation checks pass",
        "evidence": "aggregate of VAL3025_00 through VAL3025_11",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3025 - Parent-Sign SigmaH/Fpsi Cancellation Or Bound Input Rows under AX1090

Status: `Y5_R2FR_3025_parent_signature_not_found_Cbeta_core_bound_rows_staged_3026_next`

## Verdict

3025 hunted for the parent signature behind the 3024 cancellation:

`lambda_N_core/A_source^2 = -sigma_H/(2 A_source)-f_psi/4`.

The parent-sign hunt does **not** close.

`A_source` is still not parent-owned, and no pre-3024 parent row supplies `sigma_H`, `f_psi`, or the identity

`2 sigma_H/A_source + f_psi = 0`.

So the local beta route is not dead, but it remains nonclaim. The useful result is now a strict coefficient-combination target:

`C_beta_core = sigma_H/(2 A_source)+f_psi/4`,

with

`abs(C_beta_core) <= {BETA_BOUND_ABS}`.

Equivalently:

`abs(2 sigma_H/A_source + f_psi) <= {COMBO_BOUND_ABS:.6g}`.

That is the next clean test object. No post-hoc cancellation credit is allowed unless the parent action derives the cancellation before fitting.

## Parent Coefficient Hunt

{md_table(hunt_rows, ["hunt_id", "target", "search_result", "evidence", "found_numeric_value", "found_parent_theorem", "required_next"])}

## Cancellation Signature Audit

{md_table(signature_rows, ["signature_id", "object", "mathematical_form", "condition_for_zero", "equivalent_identity", "current_status", "promotion_policy"])}

## Bound Rows

{md_table(bound_rows, ["bound_id", "quantity", "definition", "bound_formula", "units", "source_path", "current_status"])}

## Input Requirements

{md_table(input_rows, ["input_id", "symbol", "meaning", "required_source", "current_status", "claim_effect"])}

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
- `{OUTPUTS["signature"]}`
- `{OUTPUTS["bounds"]}`
- `{OUTPUTS["inputs"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["signature_copy"]}`
- `{BRANCH_OUTPUTS["bounds_copy"]}`
- `{BRANCH_OUTPUTS["inputs_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass until `A_source`, `sigma_H`, and `f_psi` are parent-signed or strictly bounded.
- No cancellation credit unless `2 sigma_H/A_source + f_psi = 0` is parent-derived.
- No flat-coframe assumption unless `sigma_H=0` is parent-signed.
- No GR/EH import as MTS proof.
- No orbital-`GM` denominator.
- No hidden cancellation across residual families.
- No local-GR/Newton claim from core beta alone.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
