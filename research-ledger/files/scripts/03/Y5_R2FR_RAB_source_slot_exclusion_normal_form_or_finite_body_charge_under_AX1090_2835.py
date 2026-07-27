from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2835-Y5-R2FR-RAB-source-slot-exclusion-normal-form-or-finite-body-charge-under-AX1090.md"

SRC_2834_NEXT = RESIDUALS / "P8_Y5_R2FR_2834_NEXT_TARGET.csv"
SRC_2834_THEOREM = RESIDUALS / "P8_Y5_R2FR_2834_RECIPROCAL_SOURCE_SILENCE_THEOREM_ATTEMPT.csv"
SRC_2834_MATCHING = RESIDUALS / "P8_Y5_R2FR_2834_SOURCE_MATCHING_AND_PIR_LEDGER.csv"
SRC_2834_FINITE = RESIDUALS / "P8_Y5_R2FR_2834_FINITE_QR_SOURCE_BODY_ACQUISITION_ROWS_NONCLAIM.csv"
SRC_1629_DOC = ROOT / "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md"
SRC_1768_DOC = ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md"
SRC_2250 = BETA_DOCS / "RAB_SOURCE_SIGNATURE_BODY_CHARGE_2250_NONCLAIM.csv"
SRC_2251 = BETA_DOCS / "RAB_SOURCE_SLOT_BRR_CRT_QR_2251_NONCLAIM.csv"
SRC_2252 = BETA_DOCS / "RAB_PARENT_SLOT_NORMAL_FORM_2252_NONCLAIM.csv"
SRC_2261 = BETA_DOCS / "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv"
SRC_1884_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_SOURCE_DESCENT_PREMISE_MATRIX.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2835_SOURCE_REGISTER.csv",
    "normal_form": RESIDUALS / "P8_Y5_R2FR_2835_RAB_SOURCE_SLOT_NORMAL_FORM_ATTEMPT.csv",
    "object_language": RESIDUALS / "P8_Y5_R2FR_2835_OBJECT_LANGUAGE_AND_ACTION_SCALE_AUDIT.csv",
    "finite_vector": RESIDUALS / "P8_Y5_R2FR_2835_RAB_FINITE_SOURCE_VECTOR_INSTANCE_NONCLAIM.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2835_SOURCE_SLOT_GUARDS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2835_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2835_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2835_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2835_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2835_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_copy": LOCAL_BOUNDS / "RAB_finite_source_vector_instance_2835_NONCLAIM.csv",
    "normal_form_copy": SOURCE_WEIGHT / "RAB_source_slot_normal_form_attempt_2835_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2835_RAB_VERTICALITY_OR_OBJECT_LANGUAGE_OWNER_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2835_0_2834_next", SRC_2834_NEXT, "NEXT2834_0_2835", "2834 selected RAB source-slot exclusion"),
        ("SRC2835_1_2834_theorem", SRC_2834_THEOREM, "TH2834_1_matter_functor_silence;TH2834_2_boundary_functor_silence;TH2834_5_current_verdict", "2834 source silence theorem status"),
        ("SRC2835_2_2834_matching", SRC_2834_MATCHING, "SM2834_0_boundary_variation;SM2834_3_absolute_source_vector", "2834 source matching and absolute vector"),
        ("SRC2835_3_2834_finite", SRC_2834_FINITE, "FQR2834_0_QR_body;FQR2834_1_PiR;FQR2834_2_JR;FQR2834_4_total_abs", "2834 finite source-body rows"),
        ("SRC2835_4_1629", SRC_1629_DOC, "RSE1629_7_verdict;OBS1629_0_parent_object_language;OBS1629_3_boundary_PiR", "1629 source-slot exclusion prior audit"),
        ("SRC2835_5_1768", SRC_1768_DOC, "ANF1768_0_parent_action_partition;ANF1768_5_forbidden_source_map;SCL1768_2_nonminimal_coupling", "1768 parent action normal-form signature"),
        ("SRC2835_6_2250", SRC_2250, "ACQ2250_2_QR_body;ACQ2250_3_PiR;ACQ2250_4_total", "2250 body/PiR source vector rows"),
        ("SRC2835_7_2251", SRC_2251, "ACQ2251_3_QR_body;ACQ2251_4_PiR;ACQ2251_6_total_abs", "2251 source-slot finite acquisition rows"),
        ("SRC2835_8_2252", SRC_2252, "SLOT2252_7_boundary_PiR;MISSING_PIR_ZERO_OR_BOUND", "2252 parent slot normal form boundary PiR row"),
        ("SRC2835_9_2261", SRC_2261, "CON2261_2_matter_functor;CON2261_3_boundary_functor;CON2261_6_joint_contract", "2261 primitive derivation audit"),
        ("SRC2835_10_1884", SRC_1884_MATRIX, "SDM1884_2_source_silence;SDM1884_3_matter_action_descent;SDM1884_4_measure_connection_descent", "1884 source silence/matter descent premise matrix"),
    ]
    return [source_row(*spec) for spec in specs]


def normal_form_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NF2835_0_target",
            "R_AB source-slot exclusion theorem",
            "ParentGenerate excludes independent R_AB source-only slots, R_AB matter vertices, and boundary Pi_R slots before variation.",
            "RSE1629_0_target;ANF1768_0_parent_action_partition;CON2261_6_joint_contract",
            "TARGET_SHARP",
            "exact theorem target is known",
            "would set J_R/Pi_R/Q_R_body source branch to theorem-zero if all subclauses close",
            False,
        ),
        (
            "NF2835_1_matter_functor",
            "matter/source descent",
            "S_matter descends through Q/Psi/e_obs only, so delta S_matter/delta R_AB=0.",
            "CON2261_2_matter_functor;TH2834_1_matter_functor_silence;SDM1884_3_matter_action_descent",
            "CONDITIONAL_KERNEL_NOT_ACTIVATED",
            "R_AB is not proved vertical/basic-invisible to the actual observed coframe before matter coupling.",
            "J_R remains live as finite source-current row",
            False,
        ),
        (
            "NF2835_2_boundary_functor",
            "boundary/source-worldtube descent",
            "Boundary and source-worldtube terms descend through Q-boundary data only, so B_R=Pi_R=Q_R_body=0.",
            "CON2261_3_boundary_functor;SLOT2252_7_boundary_PiR;TH2834_2_boundary_functor_silence",
            "NOT_DERIVED",
            "No exact/proper R_AB boundary charge calculation or physical source-boundary class is signed.",
            "Pi_R and Q_R_body remain live finite rows",
            False,
        ),
        (
            "NF2835_3_object_language",
            "typed object language exclusion",
            "R_AB belongs to auxiliary/representative data or finite residual sector, not ordinary matter/source syntax.",
            "OBS1629_0_parent_object_language;CON2261_0_parent_sorts;ANF1768_5_forbidden_source_map",
            "NOT_PARENT_DERIVED",
            "current normal forms are signatures/guardrails rather than a completed primitive grammar.",
            "must prove R_AB ownership directly",
            False,
        ),
        (
            "NF2835_4_action_scale",
            "action-scale/measure owner",
            "No inert R_AB source-only multiplier or action-scale prefactor can be inserted before variation.",
            "RSE1629_4_action_scale_owner;OBS1629_1_action_scale;ANF1768_3_nonminimal_term_owner",
            "UNSIGNED",
            "action-scale/measure multipliers can hide source charge while preserving familiar equation shapes.",
            "epsilon_RAB_source remains live",
            False,
        ),
        (
            "NF2835_5_verdict",
            "current source-slot normal form",
            "R_AB source-slot exclusion is parent-derived and J_R=Pi_R=Q_R_body=0.",
            "RSE1629_7_verdict;CON2261_6_joint_contract;ACQ2251_6_total_abs",
            "NOT_DERIVED_CURRENT_CORPUS",
            "object language, R_AB verticality, action-scale owner, boundary silence and tail exclusion are unsigned.",
            "keep finite source vector staged and move to R_AB ownership/verticality",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "normal_form_id": row_id,
                "target": target,
                "statement": statement,
                "source_anchors": anchors,
                "status": status,
                "proof_or_blocker": blocker,
                "effect_or_fallback": effect,
                "normal_form_closed": closed,
                "control_only": True,
            }
        )
        for row_id, target, statement, anchors, status, blocker, effect, closed in specs
    ]


def object_language_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "OBJ2835_0_parent_sorts",
            "typed parent sorts",
            "Q, auxiliary/representative A_R=(R_AB,Lambda_R), Psi, fixed theta/top and boundary data are separated.",
            "PARTIAL_SUPPORT_NOT_DERIVED",
            "CON2261_0_parent_sorts",
            "derive R_AB as vertical representative data in ker(Dq_R) or retain it finite",
        ),
        (
            "OBJ2835_1_action_image",
            "parent action image",
            "S_parent lies in ParentGenerate[Q,theta,top,Psi] plus a signed algebraic auxiliary block for R_AB.",
            "NOT_DERIVED",
            "CON2261_1_action_image",
            "construct the auxiliary block from primitive observer-cell current rather than appending closure",
        ),
        (
            "OBJ2835_2_no_source_only_scalar",
            "no inert source-only R_AB scalar",
            "No epsilon_RAB_source, action-scale, measure or source-only Hom prefactor exists outside the action grammar.",
            "UNSIGNED",
            "OBS1629_1_action_scale;ACQ2251_2_epsilon_RAB_source",
            "prove action-scale/measure owner or keep prior-width row",
        ),
        (
            "OBJ2835_3_no_boundary_slot",
            "no independent boundary Pi_R slot",
            "Boundary grammar admits only proper/exact/silent R_AB boundary pairing, or a declared finite residual.",
            "NOT_DERIVED",
            "SLOT2252_7_boundary_PiR;ACQ2251_4_PiR",
            "derive exact boundary charge or source Pi_R bound",
        ),
        (
            "OBJ2835_4_no_hidden_tail",
            "no hidden readout/history/projector tail",
            "Readout and reduction cannot regenerate R_AB source support after variation.",
            "GUARDRAIL_NOT_THEOREM",
            "CON2261_4_readout_closure;ACQ2251_5_tail_source_vector",
            "prove readout functor commutes with R_AB elimination/projection or source tail rows",
        ),
    ]
    return [
        nonclaim(
            {
                "object_clause_id": row_id,
                "clause": clause,
                "required_statement": statement,
                "current_status": status,
                "source_anchors": anchors,
                "next_needed": next_needed,
                "clause_closed": False,
                "control_only": True,
            }
        )
        for row_id, clause, statement, status, anchors, next_needed in specs
    ]


def finite_vector_rows() -> list[dict[str, Any]]:
    specs = [
        ("FV2835_0_BRR", "B_RR", "mixed R_AB-observed-curvature vertex coefficient", "|B_RR| <= theorem_zero_or_source_backed_bound", "MISSING_NO_VERTEX_THEOREM_OR_NUMERIC_BOUND", "R10;PPN;local_GR", "ACQ2251_0_BRR"),
        ("FV2835_1_CRT", "C_RT", "mixed R_AB-Hilbert-source trace coefficient", "|C_RT| <= theorem_zero_or_source_backed_bound", "MISSING_SOURCE_SLOT_EXCLUSION_OR_NUMERIC_BOUND", "R10;WEP;PPN;orbital", "ACQ2251_1_CRT"),
        ("FV2835_2_epsilon", "epsilon_RAB_source", "inert source-only reciprocal scalar/prior width", "|epsilon_RAB_source| <= theorem_zero_or_source_backed_prior_width", "MISSING_SOURCE_ONLY_SCALAR_ZERO_OR_WIDTH", "WEP;R10;PPN;clock", "ACQ2251_2_epsilon_RAB_source"),
        ("FV2835_3_QR_body", "Q_R_body", "body/source-worldtube reciprocal charge", "|Q_R_body| <= int_body abs(W_R rho_R) dV + |Q_R_boundary|", "MISSING_BODY_NEUTRALITY_OR_NUMERIC_BODY_CHARGE", "R10;PPN;orbital;local_GR", "ACQ2251_3_QR_body"),
        ("FV2835_4_PiR", "Pi_R", "boundary reciprocal momentum/source support term", "|Pi_R| <= theorem_zero_or_source_backed_boundary_bound", "MISSING_PIR_ZERO_OR_BOUND", "boundary;R10;PPN;orbital", "ACQ2251_4_PiR"),
        ("FV2835_5_tail", "tail_R", "readout/history/projector/counterterm source-tail vector", "|tail_R| <= |C_readout_R| + ||K_history_R|| + ||Delta_projector_R|| + |C_counterterm_R|", "MISSING_TAIL_ZERO_OR_BOUNDS", "clock;orbital;PPN;local_GR", "ACQ2251_5_tail_source_vector"),
        ("FV2835_6_total", "RAB_source_vector_abs", "absolute no-cancellation source vector", "S_R_abs=|B_RR|+|C_RT|+|epsilon_RAB_source|+|Q_R_body|+|Pi_R|+|tail_R|", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas", "ACQ2251_6_total_abs"),
    ]
    return [
        nonclaim(
            {
                "finite_vector_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "formula_or_bound": formula,
                "current_status": status,
                "observable_link": arenas,
                "source_anchor": anchor,
                "theorem_zero": False,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, symbol, definition, formula, status, arenas, anchor in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2835_0_absence", "absence from old equations is not grammar exclusion", "R_AB not being displayed in a legacy action is weaker than proving ParentGenerate forbids it", "no source-slot zero from silence-by-omission"),
        ("GUARD2835_1_verticality", "matter functor silence needs actual R_AB verticality", "if R_AB moves e_obs, matter varies with it", "prove Dq_R[v_R]=0/e_obs basicity before J_R=0"),
        ("GUARD2835_2_boundary", "boundary Pi_R is independent until signed silent", "Q_R=-Pi_R makes boundary grammar decisive", "no Q_R=0 without boundary functor proof"),
        ("GUARD2835_3_scale", "action-scale/source-only prefactors remain dangerous", "classical equation shape can survive hidden pre-action weights", "epsilon_RAB_source stays in finite vector"),
        ("GUARD2835_4_absolute", "finite source-vector terms cannot cancel by assumption", "RAB_source_vector_abs uses absolute component sum", "no tuned body/boundary/tail cancellation"),
    ]
    return [
        nonclaim(
            {
                "guard_id": guard_id,
                "guard": guard,
                "because": because,
                "effect": effect,
                "guard_active": True,
                "control_only": True,
            }
        )
        for guard_id, guard, because, effect in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    normal_form_open = not any(row["normal_form_closed"] for row in rows["normal_form"])
    clauses_open = not any(row["clause_closed"] for row in rows["object_language"])
    finite_nonclaim = all(not row["theorem_zero"] and not row["numeric_value_present"] and not row["source_backed"] for row in rows["finite_vector"])
    guards_active = all(row["guard_active"] for row in rows["guards"])
    specs = [
        ("GATE2835_0_sources", "all 2835 source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2835_1_normal_form", "R_AB source-slot exclusion normal form is proved", False, "BLOCKED", "object language, verticality, action scale, boundary and tail clauses remain unsigned"),
        ("GATE2835_2_JR_zero", "J_R/Pi_R/Q_R_body theorem-zero is allowed", False, "BLOCKED", "source-slot exclusion is not closed"),
        ("GATE2835_3_finite_vector", "finite source-vector rows are staged without claims", finite_nonclaim, "PASS_INTERNAL_NONCLAIM" if finite_nonclaim else "BLOCKED", "source vector is complete but value-missing"),
        ("GATE2835_4_guards", "shortcut guards are active", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "no omission/verticality/boundary/action-scale/cancellation shortcut accepted"),
        ("GATE2835_5_open_rows", "normal-form/object clauses remain explicitly open", normal_form_open and clauses_open, "PASS_NONCLAIM" if normal_form_open and clauses_open else "BLOCKED", "2835 does not overclaim source silence"),
        ("GATE2835_6_local_gr", "local GR/Newton reduction is derived", False, "BLOCKED", "source-slot branch plus remaining PPN/local operator gates remain open"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2835_0_theorem", "R_AB source-slot exclusion is not derived.", "BLOCKED_BUT_SHARP", "the exact missing clauses are now object-language, R_AB verticality, action-scale, boundary and tail exclusion.", "do not set J_R/Pi_R/Q_R_body to zero"),
        ("DEC2835_1_best_next", "The next decisive target is R_AB ownership/verticality.", "NEXT_VERTICALITY_SELECTED", "matter functor silence cannot activate until actual R_AB direction is proved basic/invisible to observed coframe.", "derive Dq_R[v_R]=0 and e_obs=Obs(q_R(Phi)) or keep finite vector"),
        ("DEC2835_2_finite", "Finite fallback remains ready.", "SOURCE_VECTOR_STAGED_NONCLAIM", "B_RR, C_RT, epsilon_RAB_source, Q_R_body, Pi_R and tail_R rows are explicit.", "only score after theorem-zero certificates or source-backed numeric bounds"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2835_0_2836",
                "status": "selected_primary",
                "target_doc": "2836-Y5-R2FR-RAB-verticality-and-observed-coframe-basicity-or-finite-source-vector-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_RAB_verticality_and_observed_coframe_basicity_or_finite_source_vector_under_AX1090_2836.py",
                "mission": "try to prove the actual R_AB direction is vertical/basic before matter coupling, Dq_R[v_R]=0 and e_obs=Obs(q_R(Phi)); if not, keep finite RAB source-vector rows without scoring",
                "acceptance": "must cite 2261 matter_functor, 2835 normal-form blockers and 2834 source matching; no J_R=0/Pi_R=0/Q_R=0 claim unless verticality and boundary clauses are signed; no local-GR claim",
                "forbidden": "do not infer verticality from q-shape forgetting, same-frame language, WEP, or absence of explicit R_AB terms",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2835_0_finite_copy", OUTPUTS["finite_vector"], BRANCH_OUTPUTS["finite_copy"], "local-bounds copy of RAB finite source vector"),
        ("BR2835_1_normal_form_copy", OUTPUTS["normal_form"], BRANCH_OUTPUTS["normal_form_copy"], "source-weight copy of RAB source-slot normal-form attempt"),
        ("BR2835_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for verticality/coframe-basicity gate"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_prediction_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_value", "predicted_value", "coefficient_value", "alpha_bound", "lambda_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2835_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2835_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2835_2_normal_form_unclaimed", not any(row["normal_form_closed"] for row in rows_by_name["normal_form"]), "RAB source-slot normal form remains unclaimed"),
        ("VAL2835_3_object_clauses_open", not any(row["clause_closed"] for row in rows_by_name["object_language"]), "object-language clauses remain open"),
        ("VAL2835_4_finite_vector_nonclaim", all(not row["theorem_zero"] and not row["numeric_value_present"] and not row["source_backed"] for row in rows_by_name["finite_vector"]), "finite RAB source-vector rows remain nonclaims"),
        ("VAL2835_5_guards_active", all(row["guard_active"] for row in rows_by_name["guards"]), "all source-slot shortcut guards are active"),
        ("VAL2835_6_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows source silence or local GR"),
        ("VAL2835_7_no_numeric_predictions", no_numeric_prediction_insertions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2835_8_next_target_2836", any(row["next_id"] == "NEXT2835_0_2836" and row["selected"] for row in rows_by_name["next"]), "RAB verticality/coframe-basicity selected next"),
        ("VAL2835_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2835_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2835_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2835_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2835_13_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim or claim_allowed flag is true"),
        ("VAL2835_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2835_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2835_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2835_OVERALL",
            "passed": overall,
            "detail": "2835 attempts RAB source-slot exclusion normal form, keeps it unclaimed because object language, verticality, action-scale, boundary and tail clauses remain unsigned, stages the finite source vector, and selects RAB verticality/coframe-basicity next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2835 - Y5 R2FR RAB Source-Slot Exclusion Normal Form Or Finite Body Charge Under AX1090

Status: `Y5_R2FR_2835_source_slot_exclusion_not_derived_verticality_next`

## Private Verdict

2835 tries the source-slot exclusion route directly.

The target is exact now: prove the parent grammar does not allow ordinary matter, source worldtubes, boundary terms, action-scale factors, or readout tails to couple to `R_AB` before variation. If that closes, `J_R`, `Pi_R`, and `Q_R_body` can go to zero.

It does **not** close in the current corpus. The strongest blocker is actual `R_AB` ownership: if `R_AB` moves the observed coframe, matter can still source it. So the next theorem has to prove the real `R_AB` direction is vertical/basic before matter coupling, not merely absent from a display equation.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## RAB Source-Slot Normal Form Attempt

{markdown_table(rows["normal_form"], ["normal_form_id", "target", "status", "proof_or_blocker", "effect_or_fallback", "normal_form_closed", "valid_for_claim"])}

## Object Language And Action Scale Audit

{markdown_table(rows["object_language"], ["object_clause_id", "clause", "current_status", "source_anchors", "next_needed", "clause_closed", "valid_for_claim"])}

## Finite RAB Source Vector Instance

{markdown_table(rows["finite_vector"], ["finite_vector_id", "symbol", "definition", "formula_or_bound", "current_status", "observable_link", "numeric_value_present", "valid_for_claim"])}

## Source Slot Guards

{markdown_table(rows["guards"], ["guard_id", "guard", "because", "effect", "guard_active", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["normal_form"] = normal_form_rows()
    rows["object_language"] = object_language_rows()
    rows["finite_vector"] = finite_vector_rows()
    rows["guards"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "normal_form", "object_language", "finite_vector", "guards", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2835_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2835_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
