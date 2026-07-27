from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3272-Y5-R2FR-parent-visible-coefficient-algebra-construction-or-first-real-coupling-row-under-AX1090.md"

SRC_3271_DOC = ROOT / "3271-Y5-R2FR-hidden-visible-hom-typing-proof-or-coupling-coefficient-bound-pack-under-AX1090.md"
SRC_3271_FIBER = OUT / "P8_Y5_R2FR_3271_QUOTIENT_FIBER_DESCENT_THEOREM.csv"
SRC_3271_PROOF = OUT / "P8_Y5_R2FR_3271_HIDDEN_VISIBLE_TYPING_PROOF_MATRIX.csv"
SRC_3271_ENV = OUT / "P8_Y5_R2FR_3271_COEFFICIENT_ENVELOPES_NONCLAIM.csv"
SRC_3271_PACK = OUT / "P8_Y5_R2FR_3271_COUPLING_BOUND_PACK_NONCLAIM.csv"
SRC_3271_NEXT = OUT / "P8_Y5_R2FR_3271_NEXT_TARGET.csv"
SRC_990 = OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv"
SRC_1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
SRC_1078_OL = OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv"
SRC_1088 = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
SRC_1090_AXIOM = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
SRC_1104_SIG = OUT / "P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv"
SRC_2659_RED = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv"
SRC_2659_ODT = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
SRC_3265_DELTA = OUT / "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3272_SOURCE_REGISTER.csv",
    "construction": OUT / "P8_Y5_R2FR_3272_AORD_CONSTRUCTION_ATTEMPT.csv",
    "selection": OUT / "P8_Y5_R2FR_3272_FIRST_COUPLING_ROW_SELECTION.csv",
    "selected_row": OUT / "P8_Y5_R2FR_3272_SELECTED_ALPHA_EM_COUPLING_ROW_NONCLAIM.csv",
    "row_schema": OUT / "P8_Y5_R2FR_3272_FIRST_COUPLING_ROW_SCHEMA.csv",
    "runner_inputs": OUT / "P8_Y5_R2FR_3272_ALPHA_EM_RUNNER_INPUTS_NONCLAIM.csv",
    "runner_results": OUT / "P8_Y5_R2FR_3272_ALPHA_EM_BOUND_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3272_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3272_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3272_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3272_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def compact(value: str, limit: int = 320) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    hits: list[str] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 220)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3271_DOC, "3271 handoff", ["NEXT3271", "A_ord", "strict no-cancellation"]),
        (SRC_3271_FIBER, "3271 quotient/fibre theorem", ["QFT3271_2", "QFT3271_4"]),
        (SRC_3271_PROOF, "3271 proof matrix", ["RED3271_1", "RED3271_3", "RED3271_5"]),
        (SRC_3271_ENV, "3271 coefficient envelopes", ["ENV3271_0", "ENV3271_1", "source_weight"]),
        (SRC_3271_PACK, "3271 coupling bound pack", ["PACK3271_0", "PACK3271_3"]),
        (SRC_3271_NEXT, "3271 selected next target", ["NEXT3271_0_3272"]),
        (SRC_990, "minimal parent action contract", ["PAC990_2", "PAC990_3", "PAC990_4"]),
        (SRC_1055, "parent action contract candidate", ["PAC1055_3", "PAC1055_6", "CONTRACT"]),
        (SRC_1078_OL, "object-language proof attempt", ["OL1078", "OBJECT_LANGUAGE", "NOT_PARENT"]),
        (SRC_1088, "minimal ordinary matter signature", ["MOMS1088", "source weights", "signature"]),
        (SRC_1090_AXIOM, "AX1090 missing axiom ledger", ["AX1090_1", "AX1090_3"]),
        (SRC_1104_SIG, "ordinary-sector signature ledger", ["SIG1104_5", "SIG1104_10"]),
        (SRC_2659_RED, "visible algebra reduction matrix", ["RED2659_0", "RED2659_7"]),
        (SRC_2659_ODT, "operator-domain theorem attempt", ["ODT2659_1", "ODT2659_6"]),
        (SRC_3265_DELTA, "two-arena DD bound source", ["MICROSCOPE", "Delta_Qe_prime"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3272_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def envelope(envelope_id: str) -> dict[str, str]:
    return next(row for row in read_csv(SRC_3271_ENV) if row["envelope_id"] == envelope_id)


def construction_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "AORD3272_0_candidate_definition",
            "construction_piece": "candidate visible coefficient algebra",
            "candidate_form": "A_ord := q* A_Q tensor A_fixed, with ordinary coefficients only in quotient-visible fields plus fixed representation/topological data",
            "source_basis": "3271 QFT3271_2; 2659 ODT2659_1; 1055 PAC1055_3",
            "result": "FORMALLY_SUFFICIENT",
            "why_not_parent_signed": "this defines the needed domain but does not derive why the parent MTS action forbids extra hidden targets",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "AORD3272_1_parent_action_owner",
            "construction_piece": "one parent ordinary-matter action object",
            "candidate_form": "S_ord[Psi,e_obs(q),A_Q,theta_rep] before empirical readout/material projection",
            "source_basis": "990 PAC990_2; 1055 PAC1055_6; 1104 SIG1104_0",
            "result": "CONTRACT_AVAILABLE_NOT_DERIVED",
            "why_not_parent_signed": "the corpus supplies a schema/checklist but not a primitive construction from MTS variables",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "AORD3272_2_fixed_data_owner",
            "construction_piece": "fixed representation/topological constant sector",
            "candidate_form": "alpha_EM, masses, charges, clocks and material labels sit in A_fixed, not hidden coordinate functions",
            "source_basis": "1055 PAC1055_1-3; 1104 SIG1104_2-3; 3271 RED3271_2",
            "result": "UNSIGNED_CONSTANT_SECTOR",
            "why_not_parent_signed": "EM kinetic normalization, matter spectrum owner, and clock/readout ownership remain independent proof debts",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "AORD3272_3_hidden_target_exclusion",
            "construction_piece": "exclude Hom(A_hid,Coeff_vis) target slots",
            "candidate_form": "hidden scalars may exist but have no typed morphism into F2, mass, binding, source-weight, clock, or frame coefficients",
            "source_basis": "1090 AX1090_1; 1104 SIG1104_5; 3271 QFT3271_3",
            "result": "COUNTEREXAMPLE_STILL_ACTIVE",
            "why_not_parent_signed": "a surviving hidden scalar can still build c0+epsilon I unless the target slot is forbidden by parent syntax",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "AORD3272_4_construction_verdict",
            "construction_piece": "construct A_ord from current corpus",
            "candidate_form": "A_ord=q*A_Q tensor A_fixed",
            "source_basis": "all AORD3272 rows",
            "result": "NOT_CONSTRUCTED_FROM_PARENT_PRIMITIVES",
            "why_not_parent_signed": "3272 must move to finite coupling row instead of repeating the theorem contract",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def selection_rows() -> list[dict[str, Any]]:
    alpha_bound = float(envelope("ENV3271_0_pure_alpha_no_cancellation")["bound_value"])
    hatm_bound = float(envelope("ENV3271_1_pure_hatm_no_cancellation")["bound_value"])
    # Higher is better. Sourceability favours rows with a concrete numeric envelope and a clear first plug-in coefficient.
    rows = [
        {
            "candidate_id": "SEL3272_0_alpha_EM",
            "coefficient": "b_alpha or C_e",
            "strict_bound": fmt(alpha_bound),
            "sourceability_0to5": 5,
            "local_GR_relevance_0to5": 3,
            "maxwell_EM_relevance_0to5": 5,
            "runnable_now_0to5": 5,
            "main_missing": "MTS parent prediction for b_alpha/C_e or theorem-zero alpha owner",
            "selected": "true",
            "selection_reason": "first real row because it has a tight numeric DD envelope, direct EM meaning, and a simple plug-in scalar coefficient",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "SEL3272_1_D_hatm_mass",
            "coefficient": "D_hatm=C_hatm-C_g",
            "strict_bound": fmt(hatm_bound),
            "sourceability_0to5": 3,
            "local_GR_relevance_0to5": 4,
            "maxwell_EM_relevance_0to5": 1,
            "runnable_now_0to5": 4,
            "main_missing": "matter spectrum/binding ownership and parent D_hatm prediction",
            "selected": "false",
            "selection_reason": "very tight but harder to tie to a clean parent coefficient first",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "SEL3272_2_source_weight",
            "coefficient": "Delta_w_AB or qbar_source_label",
            "strict_bound": envelope("ENV3271_3_source_weight_epsilon")["bound_value"],
            "sourceability_0to5": 2,
            "local_GR_relevance_0to5": 5,
            "maxwell_EM_relevance_0to5": 2,
            "runnable_now_0to5": 2,
            "main_missing": "source/species coupling law and tau/source projection, not just eta envelope",
            "selected": "false",
            "selection_reason": "more central to Newton/source coupling, but not the first runnable scalar row",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "SEL3272_3_frame_readout",
            "coefficient": "c_g, b_dis, b_clock",
            "strict_bound": "NO_DD_BOUND_DO_NOT_PROJECT",
            "sourceability_0to5": 1,
            "local_GR_relevance_0to5": 5,
            "maxwell_EM_relevance_0to5": 1,
            "runnable_now_0to5": 1,
            "main_missing": "PPN/clock/orbital transfer map and frame/readout theorem",
            "selected": "false",
            "selection_reason": "important but must not be forced into DD alpha/mass basis",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["score"] = (
            int(row["sourceability_0to5"])
            + int(row["local_GR_relevance_0to5"])
            + int(row["maxwell_EM_relevance_0to5"])
            + int(row["runnable_now_0to5"])
        )
    return rows


def selected_alpha_row() -> list[dict[str, Any]]:
    env = envelope("ENV3271_0_pure_alpha_no_cancellation")
    return [
        {
            "row_id": "ALPHA3272_0_first_real_coupling_row",
            "coefficient": "C_e := L_X ln alpha_EM or equivalent b_alpha projection",
            "sector": "EM/Maxwell/fine-structure/WEP-DD",
            "bound_value": env["bound_value"],
            "bound_units": env["bound_units"],
            "bound_type": "pure single-channel no-cancellation DD envelope",
            "limiting_arena": env["limiting_arena"],
            "bound_source": str(SRC_3265_DELTA),
            "material_source_row": env["source_row"],
            "prediction_value": "MISSING_MTS_PARENT_COEFFICIENT",
            "prediction_source": "MISSING_PARENT_ALPHA_OWNER_OR_NUMERIC_COEFFICIENT",
            "claim_rule": "claim only if numeric prediction is sourced and abs(prediction_value)<=bound_value, or alpha owner theorem-zero is parent-signed",
            "current_status": "REAL_BOUND_ROW_READY_PREDICTION_MISSING",
            "valid_for_claim": "false",
        }
    ]


def row_schema() -> list[dict[str, Any]]:
    return [
        {"field": "row_id", "required": "true", "type": "string", "meaning": "stable row identifier", "valid_for_claim": "false"},
        {"field": "coefficient", "required": "true", "type": "string", "meaning": "MTS coefficient being tested", "valid_for_claim": "false"},
        {"field": "bound_value", "required": "true", "type": "positive_float", "meaning": "absolute allowed coefficient under stated assumptions", "valid_for_claim": "false"},
        {"field": "prediction_value", "required": "true for claim", "type": "float_or_MISSING", "meaning": "MTS parent-predicted coefficient", "valid_for_claim": "false"},
        {"field": "prediction_source", "required": "true for claim", "type": "path_or_theorem_id", "meaning": "source of the parent prediction or theorem-zero", "valid_for_claim": "false"},
        {"field": "claim_rule", "required": "true", "type": "string", "meaning": "non-negotiable promotion rule", "valid_for_claim": "false"},
    ]


def runner_inputs() -> list[dict[str, Any]]:
    bound = float(envelope("ENV3271_0_pure_alpha_no_cancellation")["bound_value"])
    return [
        {
            "case_id": "ARUN3272_0_missing_prediction_refusal",
            "prediction_value": "MISSING",
            "bound_value": fmt(bound),
            "prediction_source": "MISSING",
            "expected": "REFUSE_OR_FAIL",
            "valid_for_claim": "false",
        },
        {
            "case_id": "ARUN3272_1_theorem_zero_smoke",
            "prediction_value": "0",
            "bound_value": fmt(bound),
            "prediction_source": "CONDITIONAL_ALPHA_OWNER_THEOREM_ZERO_SMOKE_NOT_PARENT_SIGNED",
            "expected": "PASS_NUMERIC_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "ARUN3272_2_half_bound_smoke",
            "prediction_value": fmt(0.5 * bound),
            "bound_value": fmt(bound),
            "prediction_source": "SMOKE_NUMERIC_NONCLAIM",
            "expected": "PASS_NUMERIC_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "ARUN3272_3_twice_bound_fail",
            "prediction_value": fmt(2.0 * bound),
            "bound_value": fmt(bound),
            "prediction_source": "SMOKE_NUMERIC_NONCLAIM",
            "expected": "FAIL_BOUND",
            "valid_for_claim": "false",
        },
    ]


def runner_results() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runner_inputs():
        if row["prediction_value"] == "MISSING" or row["prediction_source"] == "MISSING":
            abs_prediction = "MISSING"
            ratio = "MISSING"
            pass_bound = "false"
            result = "REFUSE_OR_FAIL"
        else:
            prediction = float(row["prediction_value"])
            bound = float(row["bound_value"])
            abs_prediction = fmt(abs(prediction))
            ratio = fmt(abs(prediction) / bound if bound else float("inf"))
            pass_bound = bool_str(abs(prediction) <= bound)
            result = "PASS_NUMERIC_NONCLAIM" if abs(prediction) <= bound else "FAIL_BOUND"
        rows.append(
            {
                "case_id": row["case_id"],
                "prediction_value": row["prediction_value"],
                "bound_value": row["bound_value"],
                "abs_prediction": abs_prediction,
                "prediction_over_bound": ratio,
                "prediction_source": row["prediction_source"],
                "pass_bound": pass_bound,
                "result": result,
                "expected": row["expected"],
                "expectation_met": bool_str(result == row["expected"]),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gates() -> list[dict[str, Any]]:
    construction = {row["attempt_id"]: row for row in construction_rows()}
    runner = {row["case_id"]: row for row in runner_results()}
    return [
        {
            "gate_id": "G3272_0_Aord_constructed",
            "gate": "parent visible coefficient algebra A_ord is constructed from MTS primitives",
            "passed": "false",
            "reason": construction["AORD3272_4_construction_verdict"]["result"],
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3272_1_first_row_selected",
            "gate": "first finite coupling row is selected rather than repeating the theorem contract",
            "passed": "true",
            "reason": "alpha/EM selected as first runnable scalar coefficient row",
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3272_2_real_bound_present",
            "gate": "selected alpha/EM row has a real numeric DD envelope",
            "passed": bool_str(float(selected_alpha_row()[0]["bound_value"]) > 0),
            "reason": selected_alpha_row()[0]["bound_value"],
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3272_3_missing_prediction_refused",
            "gate": "runner refuses missing MTS parent prediction",
            "passed": bool_str(runner["ARUN3272_0_missing_prediction_refusal"]["result"] == "REFUSE_OR_FAIL"),
            "reason": runner["ARUN3272_0_missing_prediction_refusal"]["result"],
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3272_4_fail_case_caught",
            "gate": "runner catches coefficient twice the bound",
            "passed": bool_str(runner["ARUN3272_3_twice_bound_fail"]["result"] == "FAIL_BOUND"),
            "reason": runner["ARUN3272_3_twice_bound_fail"]["result"],
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3272_5_local_GR",
            "gate": "local GR/Newton/Maxwell/PPN promotion",
            "passed": "false",
            "reason": "3272 creates one executable alpha/EM coupling row; source, EH, Bianchi, PPN and readout gates remain open",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3272_0_Aord_result",
            "verdict": "AORD_NOT_CONSTRUCTED_MOVE_TO_FIRST_ROW",
            "what_moved": "3272 tested the parent visible coefficient algebra construction against current parent-action sources and confirmed it is still a contract, not a derived object.",
            "next_action": "Do not repeat A_ord prose until a new parent construction exists.",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3272_1_first_row",
            "verdict": "ALPHA_EM_FIRST_REAL_COUPLING_ROW_READY",
            "what_moved": "The first executable finite coupling row now has a real numeric bound and a runner: |C_e| <= 1.389797711495e-12 under pure alpha/no-cancellation assumptions.",
            "next_action": "Either derive alpha owner theorem-zero or supply a sourced MTS prediction for C_e/b_alpha; otherwise proceed to D_hatm or source-weight row.",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3272_0_3273",
            "selected": "primary",
            "target_doc": "3273-Y5-R2FR-alpha-owner-theorem-zero-or-source-backed-Ce-prediction-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3273_alpha_owner_theorem_zero_or_source_backed_Ce_prediction.py",
            "objective": "Try one last derivation route for alpha owner theorem-zero: unique Maxwell kinetic owner plus fixed charge generator plus no independent F2/readout/radiative return. If it fails, require a sourced numeric C_e/b_alpha prediction and run it against ALPHA3272_0.",
            "guardrail": "Do not claim from the bound alone; the missing object is the MTS prediction or theorem-zero, not the experimental pressure.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def output_csvs_parse() -> bool:
    return all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def validation_rows() -> list[dict[str, Any]]:
    sources = source_register()
    runner = runner_results()
    gates = promotion_gates()
    validations = [
        {
            "check_id": "VAL3272_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3272_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3272_2_outputs_parse",
            "check": "all 3272 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3272_3_Aord_not_falsely_signed",
            "check": "A_ord construction verdict remains not parent-signed",
            "passed": bool_str(construction_rows()[-1]["parent_signed"] == "false"),
            "detail": construction_rows()[-1]["result"],
        },
        {
            "check_id": "VAL3272_4_alpha_selected",
            "check": "alpha/EM selected as first coupling row",
            "passed": bool_str(any(row["candidate_id"] == "SEL3272_0_alpha_EM" and row["selected"] == "true" for row in selection_rows())),
            "detail": selected_alpha_row()[0]["row_id"],
        },
        {
            "check_id": "VAL3272_5_runner_expectations",
            "check": "alpha/EM bound runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['case_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3272_6_claim_gates_false",
            "check": "no 3272 gate allows local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3272_7_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3272_8_overall",
            "check": "3272 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3272_8_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    sources = read_csv(OUTPUTS["sources"])
    construction = read_csv(OUTPUTS["construction"])
    selection = read_csv(OUTPUTS["selection"])
    alpha = read_csv(OUTPUTS["selected_row"])
    runner = read_csv(OUTPUTS["runner_results"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3272 - Parent visible coefficient algebra construction or first real coupling row under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3272` tries to construct `A_ord=q*A_Q⊗A_fixed` from current parent-action sources.
- The construction is formally sufficient but still not parent-derived from MTS primitives, so the theorem route is not promoted.
- Per the 3271 guardrail, `3272` therefore moves to the first executable finite coupling row instead of repeating the contract.
- Selected first row: alpha/EM coefficient `C_e := L_X ln alpha_EM`, with strict pure-channel envelope `|C_e| <= {selected_alpha_row()[0]["bound_value"]}`.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## A_ord Construction Attempt
{md_table(construction, ["attempt_id", "construction_piece", "candidate_form", "source_basis", "result", "why_not_parent_signed", "parent_signed", "valid_for_claim"])}

## First Coupling Row Selection
{md_table(selection, ["candidate_id", "coefficient", "strict_bound", "sourceability_0to5", "local_GR_relevance_0to5", "maxwell_EM_relevance_0to5", "runnable_now_0to5", "score", "selected", "selection_reason", "valid_for_claim"])}

## Selected Alpha/EM Coupling Row
{md_table(alpha, ["row_id", "coefficient", "sector", "bound_value", "bound_units", "bound_type", "limiting_arena", "prediction_value", "prediction_source", "claim_rule", "current_status", "valid_for_claim"])}

## Alpha/EM Bound Runner
{md_table(runner, ["case_id", "prediction_value", "bound_value", "abs_prediction", "prediction_over_bound", "prediction_source", "pass_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "next_action", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_key = {
        "sources": source_register(),
        "construction": construction_rows(),
        "selection": selection_rows(),
        "selected_row": selected_alpha_row(),
        "row_schema": row_schema(),
        "runner_inputs": runner_inputs(),
        "runner_results": runner_results(),
        "promotion": promotion_gates(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
