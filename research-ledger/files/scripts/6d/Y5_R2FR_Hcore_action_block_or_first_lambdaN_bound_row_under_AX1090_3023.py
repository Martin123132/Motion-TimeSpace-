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

CHECKPOINT = "3023"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5

DOC = ROOT / "3023-Y5-R2FR-Hcore-action-block-or-first-lambdaN-bound-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3023_00_3022_doc": ROOT / "3022-Y5-R2FR-psiN-Hamiltonian-owner-or-lambdaN-bound-input-under-AX1090.md",
    "SRC3023_01_3022_owner": RESIDUALS / "P8_Y5_R2FR_3022_PSIN_HAMILTONIAN_OWNER_AUDIT.csv",
    "SRC3023_02_3022_bound_inputs": RESIDUALS / "P8_Y5_R2FR_3022_LAMBDAN_BOUND_INPUT_ROWS.csv",
    "SRC3023_03_3022_translation": RESIDUALS / "P8_Y5_R2FR_3022_BETA_BOUND_TRANSLATION.csv",
    "SRC3023_04_3022_next": RESIDUALS / "P8_Y5_R2FR_3022_NEXT_TARGET.csv",
    "SRC3023_05_3021_lambda": RESIDUALS / "P8_Y5_R2FR_3021_LAMBDA_N_RESIDUAL_LEDGER.csv",
    "SRC3023_06_3020_lapse": RESIDUALS / "P8_Y5_R2FR_3020_LAPSE_COEFFICIENT_MAP.csv",
    "SRC3023_07_2923_doc": ROOT / "2923-Y5-R2FR-first-source-mass-row-template-and-Hcore-coefficient-checklist-under-AX1090.md",
    "SRC3023_08_2923_hcore": RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv",
    "SRC3023_09_2924_doc": ROOT / "2924-Y5-R2FR-parent-Hcore-coefficient-map-or-finite-source-mass-first-row-fill-under-AX1090.md",
    "SRC3023_10_2924_eh_anchor": RESIDUALS / "P8_Y5_R2FR_2924_EH_ANCHOR_COEFFICIENT_MAP.csv",
    "SRC3023_11_2924_reduction": RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
    "SRC3023_12_2924_bridge": RESIDUALS / "P8_Y5_R2FR_2924_GAUSS_POISSON_BRIDGE_CHECK.csv",
    "SRC3023_13_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3023_14_3007_variation": RESIDUALS / "P8_Y5_R2FR_3007_SECTOR_VARIATION_LEDGER.csv",
    "SRC3023_15_2578_coupling": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COUPLING_BASELINE_GATE.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3023_SOURCE_REGISTER.csv",
    "hcore_audit": RESIDUALS / "P8_Y5_R2FR_3023_HCORE_ACTION_BLOCK_AUDIT.csv",
    "lambda_schema": RESIDUALS / "P8_Y5_R2FR_3023_FIRST_LAMBDAN_BOUND_ROW_SCHEMA.csv",
    "row_validator": RESIDUALS / "P8_Y5_R2FR_3023_LAMBDAN_ROW_VALIDATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3023_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3023_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3023_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3023_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3023_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hcore_copy": PARENT_ACTION / "Hcore_action_block_audit_3023_NOT_FILLED.csv",
    "lambda_schema_copy": LOCAL_BOUNDS / "first_lambdaN_bound_row_schema_3023_NONCLAIM.csv",
    "validator_copy": LOCAL_BOUNDS / "lambdaN_row_validator_3023_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3023_MINIMAL_HCORE_ANSATZ_OR_LAMBDAN_NUMERIC_INTAKE_NEXT_NONCLAIM.csv",
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
    "SRC3023_00_3022_doc": "3022 handoff: Hcore action block or first lambda_N bound row",
    "SRC3023_01_3022_owner": "psi_N owner audit",
    "SRC3023_02_3022_bound_inputs": "lambda_N bound-input family rows",
    "SRC3023_03_3022_translation": "beta comparator translation and A_source guard",
    "SRC3023_04_3022_next": "machine-readable 3023 target",
    "SRC3023_05_3021_lambda": "lambda_N residual ledger",
    "SRC3023_06_3020_lapse": "lapse coefficient map",
    "SRC3023_07_2923_doc": "Hcore/Q_tau checklist checkpoint",
    "SRC3023_08_2923_hcore": "Hcore/Q_tau coefficient checklist",
    "SRC3023_09_2924_doc": "parent Hcore coefficient map attempt",
    "SRC3023_10_2924_eh_anchor": "EH anchor coefficient map, nonclaim",
    "SRC3023_11_2924_reduction": "MTS-to-EH reduction contract",
    "SRC3023_12_2924_bridge": "Gauss/Poisson bridge check",
    "SRC3023_13_3007_grammar": "minimal parent action grammar",
    "SRC3023_14_3007_variation": "sector variation ledger",
    "SRC3023_15_2578_coupling": "coupling baseline gate",
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

hcore_audit = [
    base(
        {
            "audit_id": "HCA3023_0_action_block",
            "target": "H_core or L_MTS_core",
            "required_content": "field list; derivative order; normalization; source term; gauge/constraint class; boundary term",
            "current_status": "MISSING_PARENT_ACTION_BLOCK",
            "source_evidence": "2923 HC2923_0",
            "can_own_psiN_now": False,
            "effect": "no parent equation for psi_N",
        }
    ),
    base(
        {
            "audit_id": "HCA3023_1_variation",
            "target": "delta L_MTS_core",
            "required_content": "delta L=E delta Phi+dTheta with explicit theta and constraints",
            "current_status": "MISSING_THETA_QTAU_EXTRACTION",
            "source_evidence": "2923 HC2923_3; 3007 variation ledger",
            "can_own_psiN_now": False,
            "effect": "Hamiltonian charge cannot source W or psi_N",
        }
    ),
    base(
        {
            "audit_id": "HCA3023_2_EH_anchor",
            "target": "EH/ADM reference action",
            "required_content": "S_EH coefficient map and ADM/Komar source-mass pattern",
            "current_status": "REFERENCE_FILLED_NOT_MTS_REDUCTION",
            "source_evidence": "2924 EHA2924 rows",
            "can_own_psiN_now": False,
            "effect": "valid target morphology, not an MTS proof",
        }
    ),
    base(
        {
            "audit_id": "HCA3023_3_reduction_morphism",
            "target": "MTS -> EH + silent/bounded sectors",
            "required_content": "metric readout, constant kappa, EH core reduction, matter descent, extra-sector silence, projector silence, fixed boundary, Htau integrability, worldtube glue",
            "current_status": "REDUCTION_MORPHISM_NOT_DERIVED",
            "source_evidence": "2924 RED2924_0 through RED2924_10",
            "can_own_psiN_now": False,
            "effect": "cannot import EH beta/log-lapse equation",
        }
    ),
    base(
        {
            "audit_id": "HCA3023_4_source_denominator",
            "target": "A_source denominator",
            "required_content": "positive same-frame M_H_ref and G_ref with no orbital-GM import",
            "current_status": "MISSING_MHREF_DENOMINATOR",
            "source_evidence": "2923 HC2923_5; 3022 BBT3022_2",
            "can_own_psiN_now": False,
            "effect": "finite lambda_N rows cannot be score-ready",
        }
    ),
    base(
        {
            "audit_id": "HCA3023_5_coupling_baseline",
            "target": "kappa_MTS/G_ref/ell_J/PiM/reference package",
            "required_content": "fixed together by parent action before readout",
            "current_status": "COUPLING_BASELINE_IDENTITY_NOT_DERIVED",
            "source_evidence": "2578 COG2578_4",
            "can_own_psiN_now": False,
            "effect": "lambda_N_source_current remains active",
        }
    ),
    base(
        {
            "audit_id": "HCA3023_6_verdict",
            "target": "Hcore supplies psi_N owner",
            "required_content": "HCA3023_0 through HCA3023_5 close together",
            "current_status": "HCORE_ACTION_BLOCK_NOT_FILLED",
            "source_evidence": "aggregate audit",
            "can_own_psiN_now": False,
            "effect": "emit first lambda_N_core bound-row schema",
        }
    ),
]

lambda_schema = [
    base(
        {
            "row_id": "LNR3023_0_first_lambda_N_core_schema",
            "row_type": "lambda_N_core_bound_input",
            "symbol": "lambda_N_core",
            "definition": "independent quadratic log-lapse coefficient from the core parent lapse/Hamiltonian equation",
            "beta_projection": "abs(lambda_N_core/A_source^2)",
            "acceptance_formula": "abs(lambda_N_core/A_source^2) <= 7.8e-05",
            "A_source": "MISSING_A_SOURCE_PARENT_DENOMINATOR",
            "lambda_N_value": "MISSING_LAMBDA_N_CORE_VALUE_OR_ZERO_THEOREM",
            "units": "dimensionless_if_psi_N_expansion_uses_W/c^2",
            "gauge": "MISSING_OBSERVED_SOURCE_NORMALIZED_GAUGE",
            "denominator": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "source_path": "MISSING_PARENT_HCORE_OR_BOUND_SOURCE",
            "theorem_zero": False,
            "numeric_value_present": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
    base(
        {
            "row_id": "LNR3023_1_theorem_zero_alternative",
            "row_type": "lambda_N_core_zero_theorem",
            "symbol": "lambda_N_core",
            "definition": "psi_N=A_source W/c^2+O(W^3) in same source-normalized branch",
            "beta_projection": "zero if theorem signed",
            "acceptance_formula": "parent-signed theorem replaces numeric bound",
            "A_source": "MISSING_A_SOURCE_PARENT_DENOMINATOR",
            "lambda_N_value": "0_only_if_parent_signed",
            "units": "dimensionless",
            "gauge": "same observed PPN/source gauge",
            "denominator": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "source_path": "MISSING_PARENT_THEOREM_SOURCE",
            "theorem_zero": False,
            "numeric_value_present": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ),
]

row_validator = [
    base(
        {
            "rule_id": "VR3023_0_A_source",
            "rule": "A_source must be finite, nonzero, parent-owned and not imported from orbital GM",
            "current_result": "FAIL_MISSING_A_SOURCE",
            "claim_effect": "lambda_N row remains schema only",
        }
    ),
    base(
        {
            "rule_id": "VR3023_1_lambda_value",
            "rule": "lambda_N_core must be numeric with source path or theorem-zero",
            "current_result": "FAIL_MISSING_VALUE",
            "claim_effect": "no beta score",
        }
    ),
    base(
        {
            "rule_id": "VR3023_2_units_gauge",
            "rule": "units, expansion convention, observed gauge and source frame must be declared",
            "current_result": "FAIL_MISSING_GAUGE",
            "claim_effect": "no row comparison",
        }
    ),
    base(
        {
            "rule_id": "VR3023_3_no_cancellation",
            "rule": "component cannot be cancelled against other lambda_N families without a parent identity",
            "current_result": "PASS_GUARD",
            "claim_effect": "keeps componentwise beta discipline",
        }
    ),
    base(
        {
            "rule_id": "VR3023_4_claim_flags",
            "rule": "valid_for_claim and claim_allowed must remain false while any required field is missing",
            "current_result": "PASS_NONCLAIM",
            "claim_effect": "safe private schema",
        }
    ),
]

promotion_gates = [
    base({"gate_id": "GATE3023_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed audit"}),
    base({"gate_id": "GATE3023_1_Hcore_owner", "gate": "Hcore action block owns psi_N", "result": False, "notes": "Hcore action block and variation remain missing"}),
    base({"gate_id": "GATE3023_2_lambda_schema", "gate": "first lambda_N_core bound-row schema emitted", "result": True, "notes": "schema is source-ready but nonnumeric and nonclaim"}),
    base({"gate_id": "GATE3023_3_lambda_score", "gate": "lambda_N_core can be scored", "result": False, "notes": "A_source, lambda_N value/theorem, gauge and denominator missing"}),
    base({"gate_id": "GATE3023_4_beta_score", "gate": "MTS beta can be scored", "result": False, "notes": "lambda_N and other beta residual families remain open"}),
    base({"gate_id": "GATE3023_5_local_GR_claim", "gate": "local GR/Newton claimable", "result": False, "notes": "Hcore, gamma, beta, alpha3, source bridge and readout still incomplete"}),
]

decision = [
    base(
        {
            "decision_id": "DEC3023_0_Hcore",
            "decision": "Hcore action block not filled",
            "rationale": "existing rows provide an EH anchor and checklist, not a parent MTS action block with variation",
            "consequence": "psi_N owner remains unsigned",
        }
    ),
    base(
        {
            "decision_id": "DEC3023_1_lambda_row",
            "decision": "emit first lambda_N_core bound-row schema",
            "rationale": "the beta wound is now precise enough to be staged as an input row",
            "consequence": "future work can either fill the row or prove lambda_N_core=0",
        }
    ),
    base(
        {
            "decision_id": "DEC3023_2_next",
            "decision": "select minimal Hcore ansatz or lambda_N numeric intake",
            "rationale": "the next useful move is either a real parent action ansatz with variation or the first bounded residual input",
            "consequence": "3024 should choose/derive a minimal Hcore action block before broader testing",
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3023_0_3024",
            "target_doc": "3024-Y5-R2FR-minimal-Hcore-action-ansatz-or-lambdaN-core-numeric-intake-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_minimal_Hcore_action_ansatz_or_lambdaN_core_numeric_intake_under_AX1090_3024.py",
            "mission": "choose the minimal Hcore action ansatz that could own psi_N and test its variation; if absent, keep lambda_N_core as the first finite bound-input row with required fields explicit",
            "success_condition": "either a parent Hcore action block supplies field list, variation and psi_N equation, or lambda_N_core remains a strict nonclaim row with every missing field named",
            "forbidden": "no EH import as MTS proof; no orbital-GM denominator; no hidden cancellation; no local-GR/Newton claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["hcore_audit"], hcore_audit)
write_csv(OUTPUTS["lambda_schema"], lambda_schema)
write_csv(OUTPUTS["row_validator"], row_validator)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("hcore_copy", "hcore_audit"),
    ("lambda_schema_copy", "lambda_schema"),
    ("validator_copy", "row_validator"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3023_{len(branch_rows)}",
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
claim_rows = source_register + hcore_audit + lambda_schema + row_validator + promotion_gates + decision + next_target

validation_rows = [
    {"validation_id": "VAL3023_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3023_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3023_02_Hcore_fail_closed", "passed": any(row["audit_id"] == "HCA3023_6_verdict" and row["current_status"] == "HCORE_ACTION_BLOCK_NOT_FILLED" for row in hcore_audit), "requirement": "Hcore owner audit fails closed", "evidence": OUTPUTS["hcore_audit"].name},
    {"validation_id": "VAL3023_03_lambda_schema_present", "passed": any(row["row_id"] == "LNR3023_0_first_lambda_N_core_schema" for row in lambda_schema), "requirement": "first lambda_N_core bound-row schema exists", "evidence": OUTPUTS["lambda_schema"].name},
    {"validation_id": "VAL3023_04_validator_blocks_claim", "passed": any(row["rule_id"] == "VR3023_0_A_source" and row["current_result"].startswith("FAIL") for row in row_validator) and any(row["rule_id"] == "VR3023_4_claim_flags" and row["current_result"] == "PASS_NONCLAIM" for row in row_validator), "requirement": "validator blocks claim while missing A_source/value/gauge", "evidence": OUTPUTS["row_validator"].name},
    {"validation_id": "VAL3023_05_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3023 generated ledgers"},
    {"validation_id": "VAL3023_06_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3023 generated ledgers"},
    {"validation_id": "VAL3023_07_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3023_08_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3023_09_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3023_10_next_target_selected", "passed": next_target[0]["target_doc"].startswith("3024-Y5-R2FR-minimal-Hcore-action-ansatz"), "requirement": "next target selects minimal Hcore ansatz or lambdaN intake", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3023_99_overall",
        "passed": overall_pass,
        "requirement": "all 3023 validation checks pass",
        "evidence": "aggregate of VAL3023_00 through VAL3023_10",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3023 - Hcore Action Block Or First LambdaN Bound Row under AX1090

Status: `Y5_R2FR_3023_Hcore_action_block_not_filled_first_lambdaN_schema_emitted_3024_next`

## Verdict

3023 tries the highest-leverage beta route: make `H_core/L_MTS_core` own the equation for `psi_N=-log N`.

That does not close here.

The EH/ADM anchor gives the target morphology, but the MTS parent action block is still missing the field list, derivative order, source term, gauge/constraint class, boundary convention, variation, `Theta_MTS/Q_tau^MTS`, positive same-frame `M_H_ref`, and the reduction morphism to `EH + silent/bounded residuals`.

So `psi_N` is still not parent-owned, and `lambda_N=0` is not claimable.

The useful output is the first strict `lambda_N_core` bound-row schema:

`abs(lambda_N_core/A_source^2) <= 7.8e-05`,

with `A_source`, `lambda_N_core`, source path, units, gauge, and denominator all required before any score.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Hcore Action Block Audit

{md_table(hcore_audit, ["audit_id", "target", "required_content", "current_status", "source_evidence", "effect"])}

## First LambdaN Bound Row Schema

{md_table(lambda_schema, ["row_id", "row_type", "symbol", "beta_projection", "acceptance_formula", "A_source", "lambda_N_value", "gauge", "denominator", "source_path"])}

## LambdaN Row Validator

{md_table(row_validator, ["rule_id", "rule", "current_result", "claim_effect"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "target_script", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["hcore_audit"]}`
- `{OUTPUTS["lambda_schema"]}`
- `{OUTPUTS["row_validator"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["hcore_copy"]}`
- `{BRANCH_OUTPUTS["lambda_schema_copy"]}`
- `{BRANCH_OUTPUTS["validator_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass without parent-signed `lambda_N=0` or source-backed finite `lambda_N` residuals below the comparator.
- No finite `lambda_N` score without parent-owned `A_source`.
- No EH/Schwarzschild import as MTS proof.
- No orbital-`GM` denominator.
- No hidden cancellation across residual families.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
