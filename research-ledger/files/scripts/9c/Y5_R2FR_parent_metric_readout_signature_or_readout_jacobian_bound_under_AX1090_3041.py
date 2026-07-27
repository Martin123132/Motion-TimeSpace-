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

CHECKPOINT = "3041"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3041-Y5-R2FR-parent-metric-readout-signature-or-readout-jacobian-bound-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3041_00_3040_doc": ROOT / "3040-Y5-R2FR-single-potential-readout-theorem-or-two-channel-residual-bound-under-AX1090.md",
    "SRC3041_01_3040_theorem": RESIDUALS / "P8_Y5_R2FR_3040_SINGLE_POTENTIAL_READOUT_THEOREM_ATTEMPT.csv",
    "SRC3041_02_3040_jacobian": RESIDUALS / "P8_Y5_R2FR_3040_WEAK_FIELD_READOUT_JACOBIAN_AUDIT.csv",
    "SRC3041_03_3040_pullback": RESIDUALS / "P8_Y5_R2FR_3040_PULLBACK_FACTOR_LAW.csv",
    "SRC3041_04_3040_bound": RESIDUALS / "P8_Y5_R2FR_3040_TWO_CHANNEL_RESIDUAL_BOUND_SCHEMA.csv",
    "SRC3041_05_pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "SRC3041_06_newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
    "SRC3041_07_min_parent": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3041_08_eh_reduction": RESIDUALS / "P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv",
    "SRC3041_09_symbol_map": RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
    "SRC3041_10_first_variation": RESIDUALS / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
    "SRC3041_11_constant_gm_zero": RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
    "SRC3041_12_constant_gm_gate": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
    "SRC3041_13_worldtube_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "SRC3041_14_lock": RESIDUALS / "P8_Y5_R2FR_3036_LOCK_CLAUSE_MATRIX.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3041_SOURCE_REGISTER.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_3041_PARENT_METRIC_READOUT_SIGNATURE_AUDIT.csv",
    "proof": RESIDUALS / "P8_Y5_R2FR_3041_SIGNATURE_PROOF_ATTEMPT.csv",
    "residual": RESIDUALS / "P8_Y5_R2FR_3041_READOUT_JACOBIAN_RESIDUAL_BOUND_SCHEMA.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3041_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3041_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3041_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3041_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3041_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3041_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "signature_copy": PARENT_ACTION / "parent_metric_readout_signature_audit_3041_NOT_SIGNED.csv",
    "proof_copy": PARENT_ACTION / "metric_readout_signature_proof_attempt_3041_CONDITIONAL_NONCLAIM.csv",
    "residual_copy": LOCAL_BOUNDS / "readout_jacobian_residual_bound_schema_3041_NONCLAIM.csv",
    "countermodel_copy": LOCAL_BOUNDS / "metric_readout_countermodel_ledger_3041_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3041_W_EQUALS_PHI_OR_DREADOUT_BOUND_NEXT_NONCLAIM.csv",
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
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3041_00_3040_doc": "3040 handoff to parent metric readout signature",
    "SRC3041_01_3040_theorem": "single-potential theorem attempt rows",
    "SRC3041_02_3040_jacobian": "weak-field readout Jacobian audit",
    "SRC3041_03_3040_pullback": "pullback factor law",
    "SRC3041_04_3040_bound": "two-channel residual bound schema",
    "SRC3041_05_pg_contract": "Poisson/Gauss same-frame weak-field contracts",
    "SRC3041_06_newton_stack": "source-normalized Newton branch stack",
    "SRC3041_07_min_parent": "minimum local-GR parent action blocks",
    "SRC3041_08_eh_reduction": "EH reduction requirements",
    "SRC3041_09_symbol_map": "MTS symbol to local-GR action map",
    "SRC3041_10_first_variation": "MTS symbol first-variation gates",
    "SRC3041_11_constant_gm_zero": "constant GM zero theorem attempt",
    "SRC3041_12_constant_gm_gate": "constant GM derivative hair gate",
    "SRC3041_13_worldtube_theorem": "worldtube source-measure theorem",
    "SRC3041_14_lock": "source-readout lock matrix",
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

signature_rows = [
    base(
        {
            "signature_id": "MRS3041_0_parent_metric",
            "signature_piece": "parent observed metric/coframe",
            "required_identity": "one g_obs/e_obs owns matter, source variation, clocks, rods, orbits and the local metric equation",
            "current_evidence": "symbol map and Newton stack contain the same-frame target",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "missing_for_claim": "MISSING_q_TO_e_obs_PARENT_FUNCTOR; MISSING_SOURCE_VARIATION_FRAME_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3041_06_newton_stack"]),
        }
    ),
    base(
        {
            "signature_id": "MRS3041_1_g00_phi",
            "signature_piece": "weak-field metric potential",
            "required_identity": "g_00=-1+2 Phi/c^2 in the observed branch with declared sign convention",
            "current_evidence": "PG2 and SN5 state the GR-style weak-field form",
            "current_status": "CONDITIONAL_FORMULA_PRESENT",
            "missing_for_claim": "MISSING_PARENT_SIGNATURE_FOR_g00_BRANCH; MISSING_SIGN_CONVENTION_AUDIT",
            "source_path": str(SOURCE_PATHS["SRC3041_05_pg_contract"]),
        }
    ),
    base(
        {
            "signature_id": "MRS3041_2_lapse_psi",
            "signature_piece": "lapse/Hcore readout",
            "required_identity": "N=sqrt(1-2 Phi/c^2) and psi_N=-log(N)=Phi/c^2+O(Phi^2/c^4)",
            "current_evidence": "3040 derives the first-order Taylor algebra if g_00 branch is signed",
            "current_status": "FIRST_ORDER_ALGEBRA_CONDITIONAL",
            "missing_for_claim": "MISSING_PARENT_SIGNED_g00_TO_N_READOUT",
            "source_path": str(SOURCE_PATHS["SRC3041_01_3040_theorem"]),
        }
    ),
    base(
        {
            "signature_id": "MRS3041_3_W_equals_Phi",
            "signature_piece": "W/Phi identification",
            "required_identity": "W is the same Phi that appears in g_00, not a post-fit Poisson/orbital potential",
            "current_evidence": "PG branch uses Phi for Poisson/Gauss and 3040 shows W=Phi would give r_W=1",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_W_EQUALS_PHI_PARENT_READOUT; MISSING_NO_ORBITAL_GM_IMPORT_CERTIFICATE",
            "source_path": str(SOURCE_PATHS["SRC3041_05_pg_contract"]),
        }
    ),
    base(
        {
            "signature_id": "MRS3041_4_single_pairing",
            "signature_piece": "one source pairing",
            "required_identity": "rho_H pairs once with phi_g before psi_N/W readout coordinates are introduced",
            "current_evidence": "3038/3040 identify this as the needed route",
            "current_status": "MISSING",
            "missing_for_claim": "MISSING_SINGLE_PAIRING_PARENT_ACTION; MISSING_NO_TWO_CHANNEL_SOURCE_SLOT_THEOREM",
            "source_path": str(SOURCE_PATHS["SRC3041_14_lock"]),
        }
    ),
    base(
        {
            "signature_id": "MRS3041_5_single_hessian",
            "signature_piece": "one scalar kinetic Hessian",
            "required_identity": "C_NK0 and O_W are one Hessian H_phi pulled back through psi_N and W/c^2 readouts",
            "current_evidence": "3040 gives pullback algebra but current corpus has separate operator shapes",
            "current_status": "MISSING_HESSIAN_OWNER",
            "missing_for_claim": "MISSING_PARENT_KINETIC_HESSIAN; MISSING_RANK_ONE_SCALAR_BLOCK; MISSING_UNIT_MAP",
            "source_path": str(SOURCE_PATHS["SRC3041_03_3040_pullback"]),
        }
    ),
    base(
        {
            "signature_id": "MRS3041_6_signature_verdict",
            "signature_piece": "full parent metric readout signature",
            "required_identity": "MRS3041_0 through MRS3041_5 are signed in one parent branch before source fitting",
            "current_evidence": "only conditional pieces exist; W=Phi, source pairing and Hessian remain unsigned",
            "current_status": "PARENT_SIGNATURE_NOT_SIGNED",
            "missing_for_claim": "MISSING_FULL_SIGNATURE_PACKAGE",
            "source_path": str(SOURCE_PATHS["SRC3041_00_3040_doc"]),
        }
    ),
]

proof_rows = [
    base(
        {
            "proof_id": "PROOF3041_0_lapse",
            "attempt": "derive psi_N from signed g_00",
            "formal_step": "if g_00=-N^2=-1+2Phi/c^2, then N=sqrt(1-2Phi/c^2) and -log(N)=Phi/c^2+O(Phi^2/c^4)",
            "result": "ALGEBRA_DERIVED_CONDITIONAL_ON_g00",
            "why_not_claim": "g_00/Phi observed branch is not parent-signed",
        }
    ),
    base(
        {
            "proof_id": "PROOF3041_1_W",
            "attempt": "derive W=Phi",
            "formal_step": "identify W as the same weak-field metric potential whose gradient drives slow-particle motion and whose Laplacian is sourced by rho_H",
            "result": "NOT_DERIVED",
            "why_not_claim": "W can remain a Poisson/Gauss or orbital readout calibrated after source fitting",
        }
    ),
    base(
        {
            "proof_id": "PROOF3041_2_pairing",
            "attempt": "derive one source pairing",
            "formal_step": "replace rho_H(a_H psi_N+a_W W/c^2) with rho_H a_phi Phi/c^2 before readout coordinates",
            "result": "NOT_DERIVED",
            "why_not_claim": "no parent action row forbids two local source slots",
        }
    ),
    base(
        {
            "proof_id": "PROOF3041_3_hessian",
            "attempt": "derive one Hessian pullback",
            "formal_step": "show H_phi is the local rank-one scalar Hessian whose coordinate pullbacks produce C_NK0 and O_W",
            "result": "NOT_DERIVED",
            "why_not_claim": "existing rows provide separate Hcore/W coefficient shapes, not one parent Hessian",
        }
    ),
    base(
        {
            "proof_id": "PROOF3041_4_prefactor",
            "attempt": "close first-order prefactor",
            "formal_step": "if W=Phi, psi_N=Phi/c^2+O(2), one pairing and one Hessian hold, then r_H=r_W=1 and Xi_H/C_WH=1",
            "result": "CONDITIONAL_THEOREM_ONLY",
            "why_not_claim": "at least three required parent signatures remain unsigned and R_lock/PPN are open",
        }
    ),
    base(
        {
            "proof_id": "PROOF3041_5_verdict",
            "attempt": "parent-sign metric readout signature from current corpus",
            "formal_step": "collect all signature pieces in one branch",
            "result": "FAIL_CURRENT_SIGNATURE_CLAIM",
            "why_not_claim": "current corpus gives a promising conditional route but not a full parent theorem",
        }
    ),
]

residual_rows = [
    base(
        {
            "residual_id": "DREAD3041_0_g00",
            "quantity": "D_g00",
            "definition": "deviation from g_00=-1+2Phi/c^2 in the observed branch",
            "required_input": "parent metric readout signature or finite weak-field readout coefficient",
            "current_status": "MISSING_PARENT_VALUE",
            "claim_rule": "zero by theorem or bounded below Newton/PPN readout threshold",
        }
    ),
    base(
        {
            "residual_id": "DREAD3041_1_WPhi",
            "quantity": "D_WPhi",
            "definition": "W/Phi - 1 in the same observed weak-field branch",
            "required_input": "W=Phi theorem or finite bound with source path and units",
            "current_status": "MISSING_W_EQUALS_PHI_VALUE",
            "claim_rule": "zero by parent readout theorem or included in delta_prefactor envelope",
        }
    ),
    base(
        {
            "residual_id": "DREAD3041_2_pairing",
            "quantity": "D_pairing",
            "definition": "residual from rho_H pairing with two source slots rather than one phi_g",
            "required_input": "single source-pairing proof or finite a_H/a_W bound",
            "current_status": "MISSING_SINGLE_PAIRING_PROOF",
            "claim_rule": "zero only if two-channel source slot is parent-forbidden",
        }
    ),
    base(
        {
            "residual_id": "DREAD3041_3_hessian",
            "quantity": "D_hessian",
            "definition": "residual from C_NK0 and O_W not being one H_phi pullback",
            "required_input": "parent Hessian owner or finite operator mismatch bound",
            "current_status": "MISSING_HESSIAN_OWNER",
            "claim_rule": "zero by one-Hessian theorem or finite absolute bound",
        }
    ),
    base(
        {
            "residual_id": "DREAD3041_4_frame",
            "quantity": "D_frame_source",
            "definition": "source variation and matter/orbital readout do not use one e_obs",
            "required_input": "same-frame source variation theorem or frame residual value",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "claim_rule": "cannot be hidden inside W=Phi or measured GM",
        }
    ),
    base(
        {
            "residual_id": "DREAD3041_5_total",
            "quantity": "D_readout_total_abs",
            "definition": "abs(D_g00)+abs(D_WPhi)+abs(D_pairing)+abs(D_hessian)+abs(D_frame_source)",
            "required_input": "all component rows in a common convention",
            "current_status": "NOT_COMPUTED",
            "claim_rule": "absolute envelope only; no tuned cancellation",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3041_0_orbital_W",
            "countermodel": "W is a Poisson/orbital potential chosen after measured GM calibration, not the metric Phi",
            "effect": "r_W is not parent-owned and first-order coupling closure is imported",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3041_1_two_source_slots",
            "countermodel": "rho_H couples to both psi_N and W/c^2 with independent vertices even in one frame",
            "effect": "lapse algebra passes but Xi_H/C_WH remains free",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3041_2_hessian_split",
            "countermodel": "psi_N and W/c^2 read the same Phi but use different kinetic/operator normalizations",
            "effect": "one-potential readout does not imply one coefficient",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3041_3_first_order_only",
            "countermodel": "first-order signature closes but beta/gamma or R_lock residuals survive",
            "effect": "Newton-looking pass is not local GR",
            "status": "GUARDRAIL",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3041_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "3041 is source-backed to 3040 and local-GR source stack rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3041_1_signature_audit",
            "gate": "metric readout signature audit covers g00, psi, W, source pairing, Hessian and frame",
            "result": all(
                any(row["signature_piece"] == piece for row in signature_rows)
                for piece in [
                    "weak-field metric potential",
                    "lapse/Hcore readout",
                    "W/Phi identification",
                    "one source pairing",
                    "one scalar kinetic Hessian",
                    "parent observed metric/coframe",
                ]
            ),
            "notes": "full signature not signed",
        }
    ),
    base(
        {
            "gate_id": "GATE3041_2_lapse_conditional",
            "gate": "lapse algebra remains conditionally derived",
            "result": any(row["result"] == "ALGEBRA_DERIVED_CONDITIONAL_ON_g00" for row in proof_rows),
            "notes": "useful but not sufficient",
        }
    ),
    base(
        {
            "gate_id": "GATE3041_3_parent_signature_signed",
            "gate": "full parent metric readout signature is signed",
            "result": False,
            "notes": "W=Phi, one source pairing and Hessian are not derived",
        }
    ),
    base(
        {
            "gate_id": "GATE3041_4_residual_schema",
            "gate": "D_readout residual schema exists",
            "result": any(row["quantity"] == "D_readout_total_abs" for row in residual_rows),
            "notes": "fallback remains nonclaim",
        }
    ),
    base(
        {
            "gate_id": "GATE3041_5_countermodels",
            "gate": "live countermodels are retained",
            "result": any(row["status"] == "LIVE_BLOCKER" for row in countermodel_rows),
            "notes": "prevents W=Phi axiom smuggling",
        }
    ),
    base(
        {
            "gate_id": "GATE3041_6_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no local-GR/Newton/PPN/R10 claim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3041_0_signature",
            "question": "is the parent metric readout signature signed by the current corpus?",
            "answer": "NO",
            "reason": "lapse algebra is conditional, but W=Phi, one source pairing, one Hessian pullback and same-frame source variation are not parent-derived",
            "next_action": "attack W=Phi as the first hard sub-signature or use D_WPhi/D_readout bound rows",
        }
    ),
    base(
        {
            "decision_id": "DEC3041_1_best_route",
            "question": "which missing clause should be attacked first?",
            "answer": "W=Phi parent readout",
            "reason": "without W=Phi, r_W is not parent-owned and the single-potential prefactor closure cannot even start; source pairing and Hessian then follow",
            "next_action": "3042 should prove W is the metric Phi in the same observed branch, or produce a D_WPhi bound schema",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3041_0_3042",
            "next_checkpoint": "3042-Y5-R2FR-W-equals-Phi-parent-readout-or-DWPhi-bound-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_W_equals_Phi_parent_readout_or_DWPhi_bound_under_AX1090_3042.py",
            "mission": "prove W is the same Phi appearing in g_00=-1+2Phi/c^2 in the observed branch, or stage a finite D_WPhi readout-Jacobian bound",
            "starting_equation": "Xi_H/C_WH = r_H/r_W + sign_unit_residual; r_H=1 from conditional lapse algebra, r_W=1 only if W=Phi",
            "do_not_repeat": "do not assume W=Phi from Poisson notation or orbital GM calibration; do not promote first-order closure without source pairing/Hessian/R_lock",
            "claim_policy": "no first-order Newton source prefactor claim until W=Phi, source pairing, Hessian and R_lock are signed or bounded",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "signature": signature_rows,
    "proof": proof_rows,
    "residual": residual_rows,
    "countermodels": countermodel_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["signature"], BRANCH_OUTPUTS["signature_copy"])
shutil.copyfile(OUTPUTS["proof"], BRANCH_OUTPUTS["proof_copy"])
shutil.copyfile(OUTPUTS["residual"], BRANCH_OUTPUTS["residual_copy"])
shutil.copyfile(OUTPUTS["countermodels"], BRANCH_OUTPUTS["countermodel_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for parent metric readout signature route",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for output_key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for output_key, path in OUTPUTS.items() if output_key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + signature_rows
    + proof_rows
    + residual_rows
    + countermodel_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3041_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3041_02_signature_audit",
            "passed": bool(gates[1]["result"]),
            "requirement": "metric readout signature audit covers required pieces",
            "evidence": OUTPUTS["signature"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_03_lapse_conditional",
            "passed": bool(gates[2]["result"]),
            "requirement": "conditional lapse algebra row exists",
            "evidence": OUTPUTS["proof"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_04_signature_not_claimed",
            "passed": any(row["current_status"] == "PARENT_SIGNATURE_NOT_SIGNED" for row in signature_rows),
            "requirement": "parent metric readout signature is not claim-promoted",
            "evidence": OUTPUTS["signature"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_05_residual_schema",
            "passed": bool(gates[4]["result"]),
            "requirement": "D_readout residual bound schema exists",
            "evidence": OUTPUTS["residual"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_06_countermodels",
            "passed": bool(gates[5]["result"]),
            "requirement": "live countermodels are retained",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_07_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3041 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3041_08_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_09_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3041_10_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3041_11_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3042-"),
            "requirement": "next target selects W=Phi parent readout or D_WPhi bound",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3041_12_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3041 - Parent Metric Readout Signature Or Readout-Jacobian Bound under AX1090

Status: `Y5_R2FR_3041_parent_metric_readout_signature_not_signed_WPhi_next`

## Verdict

3041 tries to parent-sign the metric readout package needed by 3040:

`g_00=-1+2Phi/c^2`, `psi_N=-log(N)=Phi/c^2+O(2)`, `W=Phi`, one source pairing, and one Hessian pullback.

The good news: the lapse algebra is clean. If the observed weak-field metric branch is signed, then

`g_00=-N^2=-1+2Phi/c^2 -> psi_N=-log(N)=Phi/c^2+O(Phi^2/c^4)`.

The bad-but-useful news: the current corpus still does **not** parent-sign the full readout signature. In particular, `W=Phi`, one source pairing, one Hessian pullback, and same-frame source variation remain conditional or missing.

So 3041 does not claim Newton/local GR. It reduces the next hard subproblem to `W=Phi`: if `W` is not the metric `Phi`, then `r_W` is not parent-owned and the 3040 first-order prefactor closure cannot be promoted.

## Parent Metric Readout Signature Audit

{md_table(signature_rows, ["signature_id", "signature_piece", "required_identity", "current_status", "missing_for_claim"])}

## Signature Proof Attempt

{md_table(proof_rows, ["proof_id", "attempt", "formal_step", "result", "why_not_claim"])}

## Readout-Jacobian Residual Bound Schema

{md_table(residual_rows, ["residual_id", "quantity", "definition", "required_input", "current_status", "claim_rule"])}

## Countermodel Ledger

{md_table(countermodel_rows, ["countermodel_id", "countermodel", "effect", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "do_not_repeat", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print("3041 verdict: metric readout signature not signed; W=Phi parent readout selected next.")
