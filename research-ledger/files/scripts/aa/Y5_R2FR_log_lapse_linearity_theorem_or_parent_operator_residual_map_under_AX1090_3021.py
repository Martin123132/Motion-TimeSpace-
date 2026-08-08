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

CHECKPOINT = "3021"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5

DOC = ROOT / "3021-Y5-R2FR-log-lapse-linearity-theorem-or-parent-operator-residual-map-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3021_00_3020_doc": ROOT / "3020-Y5-R2FR-second-order-parent-field-equation-coefficient-map-or-beta-square-law-rejection-under-AX1090.md",
    "SRC3021_01_3020_lapse_map": RESIDUALS / "P8_Y5_R2FR_3020_LAPSE_COEFFICIENT_MAP.csv",
    "SRC3021_02_3020_ownership": RESIDUALS / "P8_Y5_R2FR_3020_PARENT_ACTION_OWNERSHIP_AUDIT.csv",
    "SRC3021_03_3020_residuals": RESIDUALS / "P8_Y5_R2FR_3020_SECOND_ORDER_RESIDUAL_OPERATOR_LEDGER.csv",
    "SRC3021_04_3020_next": RESIDUALS / "P8_Y5_R2FR_3020_NEXT_TARGET.csv",
    "SRC3021_05_2749_doc": ROOT / "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md",
    "SRC3021_06_2749_ward_ppn": RESIDUALS / "P8_Y5_R2FR_2749_WARD_PPN_GATE.csv",
    "SRC3021_07_3007_doc": ROOT / "3007-Y5-R2FR-minimal-parent-action-sector-grammar-or-sector-variation-ledger-under-AX1090.md",
    "SRC3021_08_3007_variations": RESIDUALS / "P8_Y5_R2FR_3007_SECTOR_VARIATION_LEDGER.csv",
    "SRC3021_09_3008_doc": ROOT / "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence-or-explicit-residual-split-under-AX1090.md",
    "SRC3021_10_3008_coupling": RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv",
    "SRC3021_11_3009_symbol_match": RESIDUALS / "P8_Y5_R2FR_3009_REAL_SYMBOL_MATCH_AUDIT.csv",
    "SRC3021_12_3010_live_gate": RESIDUALS / "P8_Y5_R2FR_3010_LIVE_RESPONSE_COMPONENT_GATE.csv",
    "SRC3021_13_2930_coefficients": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv",
    "SRC3021_14_2920_square_audit": RESIDUALS / "P8_Y5_R2FR_2920_PARENT_SQUARE_LAW_AUDIT.csv",
    "SRC3021_15_2893_beta_law": RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3021_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3021_LOG_LAPSE_LINEARITY_THEOREM_ATTEMPT.csv",
    "operator_map": RESIDUALS / "P8_Y5_R2FR_3021_PARENT_OPERATOR_RESIDUAL_MAP.csv",
    "lambda_ledger": RESIDUALS / "P8_Y5_R2FR_3021_LAMBDA_N_RESIDUAL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3021_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3021_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3021_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3021_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3021_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "log_lapse_linearity_theorem_attempt_3021_NOT_SIGNED.csv",
    "operator_copy": LOCAL_BOUNDS / "parent_operator_residual_map_3021_NONCLAIM.csv",
    "lambda_copy": LOCAL_BOUNDS / "lambda_N_residual_ledger_3021_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3021_PsiN_HAMILTONIAN_OWNER_OR_LAMBDAN_BOUND_NEXT_NONCLAIM.csv",
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
    "SRC3021_00_3020_doc": "3020 handoff: lambda_N=0 log-lapse target",
    "SRC3021_01_3020_lapse_map": "lapse coefficient map and beta square condition",
    "SRC3021_02_3020_ownership": "parent ownership blockers for lambda_N",
    "SRC3021_03_3020_residuals": "second-order residual ledger",
    "SRC3021_04_3020_next": "machine-readable 3021 target",
    "SRC3021_05_2749_doc": "EH control lane and non-adoption warning",
    "SRC3021_06_2749_ward_ppn": "conditional beta=1 gate not adopted as MTS proof",
    "SRC3021_07_3007_doc": "minimal parent sector grammar",
    "SRC3021_08_3007_variations": "variation ledger for all retained sectors",
    "SRC3021_09_3008_doc": "q_loc action route and hidden coupling guard",
    "SRC3021_10_3008_coupling": "matter/source coupling guard rows",
    "SRC3021_11_3009_symbol_match": "Gamma/Khat live symbol match failure",
    "SRC3021_12_3010_live_gate": "no live response component yet",
    "SRC3021_13_2930_coefficients": "A_source/B_source coefficient ledger",
    "SRC3021_14_2920_square_audit": "parent square law not proved",
    "SRC3021_15_2893_beta_law": "source-normalized beta extraction grammar",
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

theorem_attempt = [
    base(
        {
            "theorem_id": "LLT3021_0_definition",
            "claim_tested": "log-lapse beta variable",
            "formal_statement": "psi_N=-log N=A_source W/c^2+lambda_N W^2/c^4+O(W^3)",
            "derived_result": "beta_eff=1-lambda_N/A_source^2 plus retained extra-sector residuals",
            "current_status": "KINEMATIC_EQUIVALENCE_FROM_3020",
            "parent_signed": False,
            "missing_for_claim": "MISSING_PARENT_EQUATION_FOR_psi_N",
        }
    ),
    base(
        {
            "theorem_id": "LLT3021_1_sufficient_linearity_theorem",
            "claim_tested": "lambda_N=0 sufficient theorem",
            "formal_statement": "if the same-gauge parent equation gives psi_N=A_source W/c^2+O(W^3), then lambda_N=0 and B_source=A_source^2",
            "derived_result": "valid theorem contract",
            "current_status": "CONDITIONAL_THEOREM_CONTRACT",
            "parent_signed": False,
            "missing_for_claim": "MISSING_PARENT_HAMILTONIAN_OR_FIELD_EQUATION_NORMAL_FORM",
        }
    ),
    base(
        {
            "theorem_id": "LLT3021_2_operator_source_test",
            "claim_tested": "no independent quadratic log-lapse source",
            "formal_statement": "L_N[psi_N-A_source W/c^2] has no O(W^2), |grad W|^2, rho_H W, boundary, operator, readout or source-current term",
            "derived_result": "this is the exact parent equation test for lambda_N=0",
            "current_status": "TEST_WRITTEN_NOT_SOURCED",
            "parent_signed": False,
            "missing_for_claim": "MISSING_L_N_OPERATOR; MISSING_SECOND_ORDER_SOURCE_TERM_AUDIT",
        }
    ),
    base(
        {
            "theorem_id": "LLT3021_3_EH_control_lane",
            "claim_tested": "GR/EH control has beta=1",
            "formal_statement": "EH weak-field core can realize the same log-lapse behavior after source/readout ownership",
            "derived_result": "control lane only",
            "current_status": "CONDITIONAL_UNSIGNED_NOT_MTS_ADOPTION",
            "parent_signed": False,
            "missing_for_claim": "MISSING_EH_BLOCK_MATCH_TO_MTS_PRIMITIVES; MISSING_SOURCE_READOUT_OWNERSHIP",
        }
    ),
    base(
        {
            "theorem_id": "LLT3021_4_parent_action_search",
            "claim_tested": "current MTS sources sign log-lapse linearity",
            "formal_statement": "look for parent-owned psi_N equation, Hamiltonian constraint or second-order field equation setting lambda_N=0",
            "derived_result": "not found in current cited corpus",
            "current_status": "PARENT_SIGNATURE_MISSING",
            "parent_signed": False,
            "missing_for_claim": "MISSING_PSI_N_HAMILTONIAN_OWNER",
        }
    ),
    base(
        {
            "theorem_id": "LLT3021_5_verdict",
            "claim_tested": "MTS derives beta square law through log-lapse linearity",
            "formal_statement": "lambda_N=0 plus no extra beta residual families",
            "derived_result": "not proved; lambda_N retained as explicit residual",
            "current_status": "LOG_LAPSE_THEOREM_NOT_SIGNED",
            "parent_signed": False,
            "missing_for_claim": "MISSING_lambda_N_ZERO_THEOREM; MISSING_EXTRA_RESIDUAL_SILENCE",
        }
    ),
]

operator_map = [
    base(
        {
            "operator_id": "OPM3021_0_core_log_lapse",
            "source_family": "core lapse/Hamiltonian equation",
            "operator_statement": "L_N psi_N = A_source L_W W/c^2 + S_N^(2)/c^4 + O(W^3)",
            "lambda_projection": "lambda_N = coefficient of L_N^{-1}[S_N^(2)] along W^2",
            "current_status": "OPERATOR_FORM_REQUIRED_NOT_OWNED",
            "needed_for_zero": "derive S_N^(2)=0 in the observed/source-normalized branch",
        }
    ),
    base(
        {
            "operator_id": "OPM3021_1_grad_self_source",
            "source_family": "quadratic gradient/self-energy",
            "operator_statement": "S_N^(2) may contain C_grad |grad W|^2 or equivalent self-energy terms",
            "lambda_projection": "lambda_N_grad",
            "current_status": "MISSING_COEFFICIENT_OR_CANCELLATION_THEOREM",
            "needed_for_zero": "show coefficient cancels in psi_N gauge or keep finite value",
        }
    ),
    base(
        {
            "operator_id": "OPM3021_2_extra_operator",
            "source_family": "R11/R2/fR/scalar/vector/tensor/auxiliary sector",
            "operator_statement": "extra sector stress or operator hair shifts the O(W^2) lapse equation",
            "lambda_projection": "lambda_N_operator",
            "current_status": "MISSING_OPERATOR_NOHAIR_OR_COEFFICIENT",
            "needed_for_zero": "sector no-hair theorem or finite beta projection row",
        }
    ),
    base(
        {
            "operator_id": "OPM3021_3_Gamma_Khat",
            "source_family": "Gamma/Khat/q_loc response mismatch",
            "operator_statement": "Delta_K or q_loc source can feed the second-order lapse/readout equation",
            "lambda_projection": "lambda_N_DeltaK",
            "current_status": "MISSING_LIVE_RESPONSE_COMPONENT",
            "needed_for_zero": "live Khat=K_metric certificate or bound interface values",
        }
    ),
    base(
        {
            "operator_id": "OPM3021_4_source_current_coupling",
            "source_family": "kappa_MTS, ell_J, source-prefactor, non-Hilbert current",
            "operator_statement": "hidden source/coupling drift can enter W and psi_N differently",
            "lambda_projection": "lambda_N_source_current",
            "current_status": "MISSING_COUPLING_DESCENT",
            "needed_for_zero": "same-frame matter/source descent and constant coupling/source-current owner",
        }
    ),
    base(
        {
            "operator_id": "OPM3021_5_boundary_readout",
            "source_family": "boundary/reference/readout/PPN gauge",
            "operator_statement": "fixed-reference and observed-coframe transfer can generate apparent lambda_N",
            "lambda_projection": "lambda_N_readout_boundary",
            "current_status": "MISSING_READOUT_AND_BOUNDARY_OU2_MAP",
            "needed_for_zero": "fixed-before-readout theorem and boundary/reference silence",
        }
    ),
    base(
        {
            "operator_id": "OPM3021_6_verdict",
            "source_family": "total parent operator map",
            "operator_statement": "lambda_N_total=sum of core, gradient, extra, DeltaK, source-current and readout projections",
            "lambda_projection": "lambda_N_total",
            "current_status": "TOTAL_NOT_SCORE_READY",
            "needed_for_zero": "every source family theorem-zero or finite-bounded; no cancellation credit",
        }
    ),
]

lambda_ledger = [
    base(
        {
            "lambda_id": "LNL3021_0_core",
            "symbol": "lambda_N_core",
            "definition": "independent quadratic log-lapse term from the core parent lapse/Hamiltonian equation",
            "beta_projection": "-lambda_N_core/A_source^2",
            "current_status": "MISSING_PARENT_PSI_N_EQUATION",
            "valid_zero_now": False,
            "next_action": "identify the parent equation owner for psi_N",
        }
    ),
    base(
        {
            "lambda_id": "LNL3021_1_operator",
            "symbol": "lambda_N_operator",
            "definition": "extra operator/sector contribution to the log-lapse quadratic coefficient",
            "beta_projection": "-lambda_N_operator/A_source^2",
            "current_status": "MISSING_OPERATOR_NOHAIR_OR_COEFFICIENT",
            "valid_zero_now": False,
            "next_action": "derive no-hair or source finite coefficient rows",
        }
    ),
    base(
        {
            "lambda_id": "LNL3021_2_DeltaK",
            "symbol": "lambda_N_DeltaK",
            "definition": "Gamma/Khat metric-response mismatch contribution",
            "beta_projection": "-lambda_N_DeltaK/A_source^2",
            "current_status": "MISSING_LIVE_RESPONSE_COMPONENT",
            "valid_zero_now": False,
            "next_action": "close live response component or carry bound interface",
        }
    ),
    base(
        {
            "lambda_id": "LNL3021_3_source_current",
            "symbol": "lambda_N_source_current",
            "definition": "source-current/coupling leakage contribution",
            "beta_projection": "-lambda_N_source_current/A_source^2",
            "current_status": "MISSING_COUPLING_DESCENT",
            "valid_zero_now": False,
            "next_action": "prove matter/source descent and constant kappa/ell_J",
        }
    ),
    base(
        {
            "lambda_id": "LNL3021_4_readout_boundary",
            "symbol": "lambda_N_readout_boundary",
            "definition": "readout, boundary/reference, and PPN gauge contribution",
            "beta_projection": "-lambda_N_readout_boundary/A_source^2",
            "current_status": "MISSING_READOUT_BOUNDARY_OU2",
            "valid_zero_now": False,
            "next_action": "derive fixed-before-readout and reference silence",
        }
    ),
    base(
        {
            "lambda_id": "LNL3021_5_total",
            "symbol": "lambda_N_total_abs",
            "definition": "absolute no-cancellation sum of log-lapse residual families",
            "beta_projection": "Delta_beta_abs >= sum_abs(lambda_N_i/A_source^2) unless each is zero/bounded",
            "current_status": "TOTAL_NOT_SCORE_READY",
            "valid_zero_now": False,
            "next_action": "3022 should find psi_N owner or emit lambda_N bound inputs",
        }
    ),
]

promotion_gates = [
    base({"gate_id": "GATE3021_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed audit"}),
    base({"gate_id": "GATE3021_1_kinematic_target", "gate": "lambda_N=0 target is exact", "result": True, "notes": "from 3020 beta/log-lapse map"}),
    base({"gate_id": "GATE3021_2_conditional_theorem", "gate": "sufficient log-lapse linearity theorem is written", "result": True, "notes": "psi_N=A_source W/c^2+O(W^3) would force beta square law"}),
    base({"gate_id": "GATE3021_3_parent_signature", "gate": "MTS parent signs psi_N equation with lambda_N=0", "result": False, "notes": "no parent Hamiltonian/field equation owner found in cited corpus"}),
    base({"gate_id": "GATE3021_4_beta_score", "gate": "MTS beta can be scored", "result": False, "notes": "lambda_N and extra residual families missing or unsigned"}),
    base({"gate_id": "GATE3021_5_local_GR_claim", "gate": "local GR/Newton claimable", "result": False, "notes": "gamma coefficients, beta log-lapse, alpha3/source-current and readout/source bridge remain incomplete"}),
]

decision = [
    base(
        {
            "decision_id": "DEC3021_0_theorem_contract",
            "decision": "log-lapse linearity is the right theorem target",
            "rationale": "it is equivalent to the beta square law in the same source-normalized branch",
            "consequence": "future work can hunt one parent equation owner instead of broad beta prose",
        }
    ),
    base(
        {
            "decision_id": "DEC3021_1_no_current_proof",
            "decision": "do not promote lambda_N=0",
            "rationale": "EH control exists but MTS parent does not own the psi_N Hamiltonian equation or residual silence",
            "consequence": "lambda_N is retained as an explicit beta residual",
        }
    ),
    base(
        {
            "decision_id": "DEC3021_2_next",
            "decision": "select psi_N Hamiltonian owner or lambda_N bound input as next target",
            "rationale": "the missing object is now the source equation for psi_N or finite coefficients for lambda_N families",
            "consequence": "3022 should either identify the parent equation owner or build source-ready bound rows",
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3021_0_3022",
            "target_doc": "3022-Y5-R2FR-psiN-Hamiltonian-owner-or-lambdaN-bound-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_psiN_Hamiltonian_owner_or_lambdaN_bound_input_under_AX1090_3022.py",
            "mission": "find the parent Hamiltonian/field-equation owner for psi_N=-log N and test whether its O(W^2) source vanishes; if not, emit source-ready finite lambda_N bound-input rows",
            "success_condition": "either psi_N=A_source W/c^2+O(W^3) is parent-signed, or lambda_N_core/operator/DeltaK/source-current/readout residuals are explicit nonclaim bound inputs",
            "forbidden": "no EH/Schwarzschild import as MTS proof; no measured-GM shortcut; no gamma-only pass; no hidden cancellation; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["theorem"], theorem_attempt)
write_csv(OUTPUTS["operator_map"], operator_map)
write_csv(OUTPUTS["lambda_ledger"], lambda_ledger)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("theorem_copy", "theorem"),
    ("operator_copy", "operator_map"),
    ("lambda_copy", "lambda_ledger"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3021_{len(branch_rows)}",
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
claim_rows = source_register + theorem_attempt + operator_map + lambda_ledger + promotion_gates + decision + next_target

validation_rows = [
    {"validation_id": "VAL3021_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3021_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3021_02_theorem_contract", "passed": any(row["theorem_id"] == "LLT3021_1_sufficient_linearity_theorem" and row["current_status"] == "CONDITIONAL_THEOREM_CONTRACT" for row in theorem_attempt), "requirement": "log-lapse linearity theorem contract is written", "evidence": OUTPUTS["theorem"].name},
    {"validation_id": "VAL3021_03_parent_not_signed", "passed": any(row["theorem_id"] == "LLT3021_5_verdict" and row["current_status"] == "LOG_LAPSE_THEOREM_NOT_SIGNED" for row in theorem_attempt) and any(row["gate_id"] == "GATE3021_3_parent_signature" and not boolish(row["result"]) for row in promotion_gates), "requirement": "lambda_N=0 is not promoted to parent-signed proof", "evidence": f"{OUTPUTS['theorem'].name}; {OUTPUTS['gates'].name}"},
    {"validation_id": "VAL3021_04_operator_map_present", "passed": any(row["operator_id"] == "OPM3021_6_verdict" for row in operator_map) and any(row["source_family"] == "core lapse/Hamiltonian equation" for row in operator_map), "requirement": "parent operator residual map includes core and total rows", "evidence": OUTPUTS["operator_map"].name},
    {"validation_id": "VAL3021_05_lambda_ledger_present", "passed": any(row["symbol"] == "lambda_N_core" for row in lambda_ledger) and any(row["symbol"] == "lambda_N_total_abs" for row in lambda_ledger), "requirement": "lambda_N residual ledger includes core and total rows", "evidence": OUTPUTS["lambda_ledger"].name},
    {"validation_id": "VAL3021_06_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3021 generated ledgers"},
    {"validation_id": "VAL3021_07_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3021 generated ledgers"},
    {"validation_id": "VAL3021_08_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3021_09_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3021_10_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3021_11_next_target_selected", "passed": next_target[0]["target_doc"].startswith("3022-Y5-R2FR-psiN-Hamiltonian-owner"), "requirement": "next target selects psiN Hamiltonian owner or lambdaN bound input", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3021_99_overall",
        "passed": overall_pass,
        "requirement": "all 3021 validation checks pass",
        "evidence": "aggregate of VAL3021_00 through VAL3021_11",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3021 - Log-Lapse Linearity Theorem Or Parent Operator Residual Map under AX1090

Status: `Y5_R2FR_3021_log_lapse_theorem_contract_written_lambdaN_not_signed_3022_next`

## Verdict

3021 tests the sharp beta theorem from 3020.

The target is:

`psi_N=-log N=A_source W/c^2+O(W^3)`.

Equivalently, in

`psi_N=-log N=A_source W/c^2+lambda_N W^2/c^4+O(W^3)`,

the required theorem is

`lambda_N=0`.

If the parent owns that equation in the same source-normalized observed branch, then `B_source=A_source^2` and the beta square law follows.

The theorem contract is clean: the parent lapse/Hamiltonian equation must have no independent `O(W^2)`, `|grad W|^2`, source-current, extra-operator, boundary, denominator, or readout term in `psi_N` after the common source potential `W` is fixed.

Current MTS does not yet sign that parent equation. EH/GR remains a control lane, not an MTS derivation. The parent grammar is staged but unsigned, the source denominator is unowned, Gamma/Khat response is not live, and coupling/readout guards remain open.

So 3021 keeps the route alive but does not claim beta, PPN, Newton, or local GR. The live object is now the explicit residual `lambda_N_total_abs`.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Log-Lapse Linearity Theorem Attempt

{md_table(theorem_attempt, ["theorem_id", "claim_tested", "formal_statement", "derived_result", "current_status", "parent_signed", "missing_for_claim"])}

## Parent Operator Residual Map

{md_table(operator_map, ["operator_id", "source_family", "operator_statement", "lambda_projection", "current_status", "needed_for_zero"])}

## Lambda_N Residual Ledger

{md_table(lambda_ledger, ["lambda_id", "symbol", "definition", "beta_projection", "current_status", "valid_zero_now", "next_action"])}

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
- `{OUTPUTS["theorem"]}`
- `{OUTPUTS["operator_map"]}`
- `{OUTPUTS["lambda_ledger"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["theorem_copy"]}`
- `{BRANCH_OUTPUTS["operator_copy"]}`
- `{BRANCH_OUTPUTS["lambda_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass without parent-signed `lambda_N=0` or source-backed finite `lambda_N` residuals below the comparator.
- No EH/Schwarzschild import as MTS proof.
- No measured-`GM` absorption shortcut.
- No gamma-only local-GR or PPN pass.
- No hidden cancellation across residual families.
- No `alpha3` pass without source-current/no-flux theorem-zero or an ultratight bound.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
