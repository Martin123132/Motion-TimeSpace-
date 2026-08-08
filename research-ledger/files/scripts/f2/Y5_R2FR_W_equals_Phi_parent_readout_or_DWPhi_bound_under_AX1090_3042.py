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

CHECKPOINT = "3042"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3042-Y5-R2FR-W-equals-Phi-parent-readout-or-DWPhi-bound-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3042_00_3041_doc": ROOT / "3041-Y5-R2FR-parent-metric-readout-signature-or-readout-jacobian-bound-under-AX1090.md",
    "SRC3042_01_3041_signature": RESIDUALS / "P8_Y5_R2FR_3041_PARENT_METRIC_READOUT_SIGNATURE_AUDIT.csv",
    "SRC3042_02_3041_proof": RESIDUALS / "P8_Y5_R2FR_3041_SIGNATURE_PROOF_ATTEMPT.csv",
    "SRC3042_03_3041_residual": RESIDUALS / "P8_Y5_R2FR_3041_READOUT_JACOBIAN_RESIDUAL_BOUND_SCHEMA.csv",
    "SRC3042_04_3040_pullback": RESIDUALS / "P8_Y5_R2FR_3040_PULLBACK_FACTOR_LAW.csv",
    "SRC3042_05_pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "SRC3042_06_newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
    "SRC3042_07_symbol_map": RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
    "SRC3042_08_charge_attempt": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
    "SRC3042_09_charge_residual": RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
    "SRC3042_10_calibration": RESIDUALS / "P8_CALIBRATION_LOCK_ATTEMPT.csv",
    "SRC3042_11_constant_gm_gate": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
    "SRC3042_12_min_parent": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3042_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3042_W_EQUALS_PHI_PARENT_READOUT_THEOREM_ATTEMPT.csv",
    "dictionary": RESIDUALS / "P8_Y5_R2FR_3042_W_SYMBOL_RETIREMENT_DICTIONARY_CANDIDATE.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_3042_DWPHI_BOUND_SCHEMA.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3042_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3042_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3042_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3042_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3042_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3042_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "W_equals_Phi_parent_readout_theorem_3042_NOT_SIGNED.csv",
    "dictionary_copy": PARENT_ACTION / "W_symbol_retirement_dictionary_3042_CANDIDATE_NONCLAIM.csv",
    "bound_copy": LOCAL_BOUNDS / "D_WPhi_bound_schema_3042_NONCLAIM.csv",
    "countermodel_copy": LOCAL_BOUNDS / "W_Phi_countermodel_ledger_3042_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3042_W_SYMBOL_RETIREMENT_OR_DWPHI_BOUND_NEXT_NONCLAIM.csv",
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
    "SRC3042_00_3041_doc": "3041 handoff: W=Phi or D_WPhi bound",
    "SRC3042_01_3041_signature": "metric readout signature audit",
    "SRC3042_02_3041_proof": "W=Phi proof attempt status",
    "SRC3042_03_3041_residual": "D_WPhi residual schema",
    "SRC3042_04_3040_pullback": "readout Jacobian pullback factor law",
    "SRC3042_05_pg_contract": "Poisson/Gauss contract using Phi",
    "SRC3042_06_newton_stack": "source-normalized Newton stack",
    "SRC3042_07_symbol_map": "MTS symbol to local-GR action map",
    "SRC3042_08_charge_attempt": "charge/current equality and Gauss calibration attempt",
    "SRC3042_09_charge_residual": "charge/current residual decomposition",
    "SRC3042_10_calibration": "calibration lock attempt",
    "SRC3042_11_constant_gm_gate": "constant GM derivative hair gate",
    "SRC3042_12_min_parent": "minimum local-GR parent action blocks",
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

theorem_rows = [
    base(
        {
            "theorem_id": "WPHI3042_0_target",
            "claim_piece": "W equals Phi parent readout theorem",
            "formal_statement": "W is the same parent-owned weak-field metric potential Phi appearing in g_00=-1+2Phi/c^2, before Poisson/Gauss/orbital calibration",
            "evidence": "3041 identifies this as the next sub-signature",
            "result": "TARGET_EXACT",
            "missing_for_claim": "MISSING_W_READOUT_DEFINITION_IN_PARENT_ACTION; MISSING_NO_ORBITAL_IMPORT_CERTIFICATE",
            "source_path": str(SOURCE_PATHS["SRC3042_00_3041_doc"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3042_1_metric_phi",
            "claim_piece": "metric Phi exists conditionally",
            "formal_statement": "PG2/SN5 use Phi in g_00=-1+2Phi/c^2 and the same-frame weak-field Poisson equation",
            "evidence": "existing rows state the conditional GR-style weak-field branch",
            "result": "CONDITIONAL_METRIC_PHI_PRESENT",
            "missing_for_claim": "MISSING_PARENT_SIGNATURE_FOR_g00_BRANCH; MISSING_SAME_FRAME_SOURCE_VARIATION",
            "source_path": str(SOURCE_PATHS["SRC3042_05_pg_contract"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3042_2_W_symbol",
            "claim_piece": "W symbol owner",
            "formal_statement": "W must be introduced as W:=Phi_metric in the local branch, not as a separate Poisson/orbital fit variable",
            "evidence": "3040/3041 use W as a readout target, but no parent-owned W:=Phi row is found",
            "result": "NOT_FOUND_AS_PARENT_DEFINITION",
            "missing_for_claim": "MISSING_W_SYMBOL_OWNER; MISSING_DICTIONARY_ROW; MISSING_DOMAIN_OF_VALIDITY",
            "source_path": str(SOURCE_PATHS["SRC3042_01_3041_signature"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3042_3_Gauss_not_enough",
            "claim_piece": "Poisson/Gauss Phi is not by itself W=Phi",
            "formal_statement": "a field satisfying a Poisson equation and matching orbital GM can still be a calibrated readout rather than the metric Phi",
            "evidence": "PG4/PG5 and charge-current rows mark Gauss/orbital calibration as not parent-derived",
            "result": "CALIBRATION_SHORTCUT_REJECTED",
            "missing_for_claim": "MISSING_GAUSS_SURFACE_IDENTITY; MISSING_ORBITAL_GM_NONCIRCULARITY; MISSING_CHARGE_CURRENT_EQUALITY",
            "source_path": str(SOURCE_PATHS["SRC3042_08_charge_attempt"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3042_4_safe_definition_route",
            "claim_piece": "symbol retirement route",
            "formal_statement": "retire independent W in the local GR branch and use Phi_metric as the sole first-order potential; then W=Phi is a dictionary, not a theorem",
            "evidence": "this avoids an artificial coupling slot but still requires proof that no older W-dependent row carried independent content",
            "result": "CANDIDATE_ROUTE_NOT_ADOPTED",
            "missing_for_claim": "MISSING_CORPUS_W_ALIAS_AUDIT; MISSING_NO_LOST_CONTENT_CERTIFICATE; MISSING_UPDATE_TO_CANONICAL_DICTIONARY",
            "source_path": str(SOURCE_PATHS["SRC3042_07_symbol_map"]),
        }
    ),
    base(
        {
            "theorem_id": "WPHI3042_5_verdict",
            "claim_piece": "3042 W=Phi verdict",
            "formal_statement": "current corpus does not derive W=Phi; it can be made safe only by an explicit W->Phi_metric dictionary/retirement or by retaining D_WPhi",
            "evidence": "conditional Phi rows exist, but W ownership is missing and calibration countermodels survive",
            "result": "W_EQUALS_PHI_NOT_SIGNED",
            "missing_for_claim": "MISSING_W_SYMBOL_RETIREMENT_OR_DWPHI_BOUND",
            "source_path": str(SOURCE_PATHS["SRC3042_02_3041_proof"]),
        }
    ),
]

dictionary_rows = [
    base(
        {
            "dictionary_id": "DICT3042_0_candidate",
            "symbol": "W",
            "canonical_replacement": "Phi_metric",
            "definition": "In the local first-order GR/Newton branch, W is not a fundamental/fitted field; W := Phi_metric where g_00=-1+2Phi_metric/c^2",
            "status": "CANDIDATE_DICTIONARY_NOT_ADOPTED",
            "guard": "only legal after corpus W-alias audit proves no independent W content is being erased",
        }
    ),
    base(
        {
            "dictionary_id": "DICT3042_1_chiW",
            "symbol": "chi_W",
            "canonical_replacement": "phi_g",
            "definition": "chi_W:=W/c^2 becomes phi_g:=Phi_metric/c^2 in the local first-order branch",
            "status": "CONDITIONAL_IF_DICT3042_0_SIGNED",
            "guard": "does not close source pairing, Hessian, R_lock or second-order PPN",
        }
    ),
    base(
        {
            "dictionary_id": "DICT3042_2_forbidden",
            "symbol": "W_fit or W_orbit",
            "canonical_replacement": "none",
            "definition": "A post-fit orbital/Gauss potential cannot be substituted for Phi_metric in the derivation",
            "status": "REJECTED_SHORTCUT",
            "guard": "would import measured GM and fake r_W=1",
        }
    ),
    base(
        {
            "dictionary_id": "DICT3042_3_audit_requirement",
            "symbol": "W occurrences",
            "canonical_replacement": "W_alias_audit",
            "definition": "Every local-branch W occurrence must be classified as Phi_metric alias, nonlocal/cosmology symbol, or independent residual",
            "status": "NEXT_REQUIRED_AUDIT",
            "guard": "no global rewrite until this audit is done",
        }
    ),
]

bound_rows = [
    base(
        {
            "bound_id": "DWP3042_0_value",
            "quantity": "D_WPhi",
            "definition": "W/Phi_metric - 1 in the same observed weak-field branch",
            "required_input": "W readout definition, Phi_metric definition, units, sign convention and source path",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_VALUE",
            "claim_rule": "zero only by parent dictionary/readout theorem; otherwise finite absolute bound",
        }
    ),
    base(
        {
            "bound_id": "DWP3042_1_calibration",
            "quantity": "D_cal_W",
            "definition": "residual if W is chosen by Gauss/orbital measured GM rather than parent metric readout",
            "required_input": "charge-current equality; Gauss surface identity; no orbital import certificate",
            "current_status": "MISSING_CALIBRATION_LOCK",
            "claim_rule": "must not be hidden inside G_ref or M_eff",
        }
    ),
    base(
        {
            "bound_id": "DWP3042_2_frame",
            "quantity": "D_frame_WPhi",
            "definition": "residual if W and Phi are read in different observed/source frames",
            "required_input": "same-frame source variation theorem or finite frame residual",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "claim_rule": "same-frame matter motion alone is insufficient",
        }
    ),
    base(
        {
            "bound_id": "DWP3042_3_operator",
            "quantity": "D_operator_WPhi",
            "definition": "residual if W obeys a different operator/source equation than metric Phi",
            "required_input": "EH-only local operator selection or R11 operator vector",
            "current_status": "R11_VECTOR_UNFILLED",
            "claim_rule": "operator mismatch counts in delta_prefactor envelope",
        }
    ),
    base(
        {
            "bound_id": "DWP3042_4_total",
            "quantity": "D_WPhi_total_abs",
            "definition": "abs(D_WPhi)+abs(D_cal_W)+abs(D_frame_WPhi)+abs(D_operator_WPhi)",
            "required_input": "all W/Phi components in common normalization",
            "current_status": "NOT_COMPUTED",
            "claim_rule": "absolute envelope only; no tuned cancellation",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3042_0_poisson_alias",
            "countermodel": "W is called the Poisson potential but is calibrated by Gauss/orbital data after fitting",
            "effect": "notation gives W=Phi by name while the value imports measured GM",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3042_1_frame_split",
            "countermodel": "Phi_metric is in the matter metric frame while W is in a source/Gauss frame",
            "effect": "r_W=1 in one frame does not close the observed prefactor",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3042_2_operator_split",
            "countermodel": "W satisfies a source-normalized Poisson equation with non-EH operator/residual terms",
            "effect": "W can match Phi in one limit but differ by R11/radial/source hair",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3042_3_symbol_rewrite_overreach",
            "countermodel": "retire W globally without checking nonlocal/cosmology/galaxy usages",
            "effect": "could destroy useful distinct empirical structure or hide a residual",
            "status": "GUARDRAIL",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3042_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "3042 is source-backed to W=Phi handoff and local calibration rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3042_1_theorem_attempt",
            "gate": "W=Phi theorem attempt exists",
            "result": any(row["theorem_id"] == "WPHI3042_0_target" for row in theorem_rows),
            "notes": "target exact",
        }
    ),
    base(
        {
            "gate_id": "GATE3042_2_theorem_signed",
            "gate": "W=Phi is parent-signed by current corpus",
            "result": False,
            "notes": "W symbol owner is missing and calibration countermodels survive",
        }
    ),
    base(
        {
            "gate_id": "GATE3042_3_dictionary_candidate",
            "gate": "W symbol retirement/dictionary candidate is staged",
            "result": any(row["dictionary_id"] == "DICT3042_0_candidate" for row in dictionary_rows),
            "notes": "not adopted until alias audit",
        }
    ),
    base(
        {
            "gate_id": "GATE3042_4_bound_schema",
            "gate": "D_WPhi bound schema exists",
            "result": any(row["quantity"] == "D_WPhi_total_abs" for row in bound_rows),
            "notes": "fallback fail-closed",
        }
    ),
    base(
        {
            "gate_id": "GATE3042_5_countermodels",
            "gate": "live countermodels are retained",
            "result": any(row["status"] == "LIVE_BLOCKER" for row in countermodel_rows),
            "notes": "prevents notation smuggling",
        }
    ),
    base(
        {
            "gate_id": "GATE3042_6_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no Newton/local-GR/PPN/R10 claim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3042_0_WPhi",
            "question": "does current corpus parent-sign W=Phi?",
            "answer": "NO",
            "reason": "Phi_metric appears conditionally in GR-style rows, but W has no parent-owned alias/definition row and can remain a calibrated Poisson/orbital readout",
            "next_action": "do not claim; run a W-symbol alias audit or retain D_WPhi",
        }
    ),
    base(
        {
            "decision_id": "DEC3042_1_best_route",
            "question": "what is the least risky next route?",
            "answer": "W-symbol retirement audit",
            "reason": "if all local-branch W usages are merely aliases for Phi_metric, we can remove a fake degree of freedom; if not, D_WPhi becomes a real residual",
            "next_action": "3043 should classify W usages and either adopt W:=Phi_metric locally or keep residual rows",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3042_0_3043",
            "next_checkpoint": "3043-Y5-R2FR-W-symbol-retirement-audit-or-DWPhi-first-bound-row-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_W_symbol_retirement_audit_or_DWPhi_first_bound_row_under_AX1090_3043.py",
            "mission": "classify every local-branch W occurrence as Phi_metric alias, nonlocal/cosmology symbol, or independent residual; then adopt a local dictionary or keep first D_WPhi bound row",
            "starting_equation": "D_WPhi = W/Phi_metric - 1; first-order prefactor uses Xi_H/C_WH = r_H/r_W + sign_unit_residual",
            "do_not_repeat": "do not infer W=Phi from Poisson notation, Gauss calibration, or orbital GM",
            "claim_policy": "no first-order source prefactor claim until W alias/dictionary, source pairing, Hessian and R_lock are signed or bounded",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "theorem": theorem_rows,
    "dictionary": dictionary_rows,
    "bound": bound_rows,
    "countermodels": countermodel_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"])
shutil.copyfile(OUTPUTS["dictionary"], BRANCH_OUTPUTS["dictionary_copy"])
shutil.copyfile(OUTPUTS["bound"], BRANCH_OUTPUTS["bound_copy"])
shutil.copyfile(OUTPUTS["countermodels"], BRANCH_OUTPUTS["countermodel_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for W/Phi readout route",
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
    + theorem_rows
    + dictionary_rows
    + bound_rows
    + countermodel_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3042_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3042_02_theorem_attempt",
            "passed": bool(gates[1]["result"]),
            "requirement": "W=Phi theorem attempt exists",
            "evidence": OUTPUTS["theorem"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_03_not_signed",
            "passed": any(row["result"] == "W_EQUALS_PHI_NOT_SIGNED" for row in theorem_rows),
            "requirement": "W=Phi is not claim-promoted",
            "evidence": OUTPUTS["theorem"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_04_dictionary_candidate",
            "passed": bool(gates[3]["result"]),
            "requirement": "W symbol retirement/dictionary candidate is staged",
            "evidence": OUTPUTS["dictionary"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_05_bound_schema",
            "passed": bool(gates[4]["result"]),
            "requirement": "D_WPhi bound schema exists",
            "evidence": OUTPUTS["bound"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_06_countermodels",
            "passed": bool(gates[5]["result"]),
            "requirement": "live countermodels are retained",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_07_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3042 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3042_08_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_09_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3042_10_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3042_11_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3043-"),
            "requirement": "next target selects W symbol retirement audit or first D_WPhi bound row",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3042_12_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3042 - W Equals Phi Parent Readout Or DWPhi Bound under AX1090

Status: `Y5_R2FR_3042_W_equals_Phi_not_signed_symbol_retirement_or_DWPhi_next`

## Verdict

3042 asks whether `W=Phi` is already parent-signed.

It is not.

The corpus has conditional GR-style rows for `Phi_metric`:

`g_00=-1+2Phi/c^2`, matter/orbits read `-grad Phi`, and the same-frame weak-field equation gives a Poisson/Gauss form.

But that does **not** prove `W=Phi`. A `W` that is introduced through Poisson notation, Gauss calibration, or orbital `GM` can still be a post-readout calibrated potential. That would fake `r_W=1`.

The clean route is therefore a dictionary/retirement audit: in the local first-order branch, either retire independent `W` and define

`W := Phi_metric`

before calibration, or retain

`D_WPhi = W/Phi_metric - 1`

as a nonclaim residual.

## W Equals Phi Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "claim_piece", "formal_statement", "result", "missing_for_claim"])}

## W Symbol Retirement Dictionary Candidate

{md_table(dictionary_rows, ["dictionary_id", "symbol", "canonical_replacement", "definition", "status", "guard"])}

## D_WPhi Bound Schema

{md_table(bound_rows, ["bound_id", "quantity", "definition", "required_input", "current_status", "claim_rule"])}

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
print("3042 verdict: W=Phi not signed; symbol-retirement audit or D_WPhi bound selected next.")
