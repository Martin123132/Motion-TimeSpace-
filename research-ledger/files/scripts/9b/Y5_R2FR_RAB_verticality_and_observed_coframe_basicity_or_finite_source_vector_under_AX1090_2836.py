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

DOC = ROOT / "2836-Y5-R2FR-RAB-verticality-and-observed-coframe-basicity-or-finite-source-vector-under-AX1090.md"

SRC_2835_NEXT = RESIDUALS / "P8_Y5_R2FR_2835_NEXT_TARGET.csv"
SRC_2835_NORMAL = RESIDUALS / "P8_Y5_R2FR_2835_RAB_SOURCE_SLOT_NORMAL_FORM_ATTEMPT.csv"
SRC_2835_OBJECT = RESIDUALS / "P8_Y5_R2FR_2835_OBJECT_LANGUAGE_AND_ACTION_SCALE_AUDIT.csv"
SRC_2835_FINITE = RESIDUALS / "P8_Y5_R2FR_2835_RAB_FINITE_SOURCE_VECTOR_INSTANCE_NONCLAIM.csv"
SRC_2261 = BETA_DOCS / "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv"
SRC_2260_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_PARENT_PROTECTION_CONTRACT.csv"
SRC_2260_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_CONDITIONAL_THEOREM.csv"
SRC_2260_STATUS = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_PROTECTION_STATUS_AUDIT.csv"
SRC_2260_QUEUE = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_LIVE_RESIDUAL_ACQUISITION_QUEUE.csv"
SRC_637_Q = RESIDUALS / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv"
SRC_637_OBS = RESIDUALS / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv"
SRC_863 = RESIDUALS / "P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv"
SRC_943 = RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
SRC_519 = RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2836_SOURCE_REGISTER.csv",
    "verticality": RESIDUALS / "P8_Y5_R2FR_2836_RAB_VERTICALITY_THEOREM_ATTEMPT.csv",
    "coframe": RESIDUALS / "P8_Y5_R2FR_2836_OBSERVED_COFRAME_BASICITY_AUDIT.csv",
    "chain": RESIDUALS / "P8_Y5_R2FR_2836_MATTER_CHAIN_RULE_LEDGER.csv",
    "finite": RESIDUALS / "P8_Y5_R2FR_2836_FINITE_RAB_SOURCE_VECTOR_CARRYOVER_NONCLAIM.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2836_VERTICALITY_GUARDS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2836_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2836_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2836_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2836_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2836_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_copy": LOCAL_BOUNDS / "RAB_finite_source_vector_carryover_2836_NONCLAIM.csv",
    "verticality_copy": SOURCE_WEIGHT / "RAB_verticality_theorem_attempt_2836_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2836_RAB_ownership_selector_OR_finite_residual_NEXT.csv",
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
        ("SRC2836_0_2835_next", SRC_2835_NEXT, "NEXT2835_0_2836", "2835 selected RAB verticality/coframe-basicity"),
        ("SRC2836_1_2835_normal", SRC_2835_NORMAL, "NF2835_1_matter_functor;NF2835_5_verdict", "2835 normal-form blocker"),
        ("SRC2836_2_2835_object", SRC_2835_OBJECT, "OBJ2835_0_parent_sorts;OBJ2835_1_action_image", "2835 object-language audit"),
        ("SRC2836_3_2835_finite", SRC_2835_FINITE, "FV2835_3_QR_body;FV2835_4_PiR;FV2835_6_total", "2835 finite RAB source vector"),
        ("SRC2836_4_2261", SRC_2261, "CON2261_2_matter_functor;CON2261_6_joint_contract", "2261 primitive derivation audit"),
        ("SRC2836_5_2260_contract", SRC_2260_CONTRACT, "CON2260_2_matter_functor;CON2260_6_joint_contract", "2260 parent protection contract"),
        ("SRC2836_6_2260_theorem", SRC_2260_THEOREM, "THM2260_0_statement;THM2260_3_verdict", "2260 conditional theorem"),
        ("SRC2836_7_2260_status", SRC_2260_STATUS, "PROT2260_0_JR;PROT2260_4_joint", "2260 protection status audit"),
        ("SRC2836_8_2260_queue", SRC_2260_QUEUE, "ACQ2260_3_JR;ACQ2260_4_BR", "2260 live residual queue"),
        ("SRC2836_9_637_q", SRC_637_Q, "QM637_2_vertical_kernel", "quotient vertical kernel condition"),
        ("SRC2836_10_637_obs", SRC_637_OBS, "OF637_1_chain_rule;OF637_2_counterexample_filter", "observed functor chain rule"),
        ("SRC2836_11_863", SRC_863, "CZT863_0_chain_rule_zero;CZT863_5_zero_verdict", "coframe zero theorem conditional"),
        ("SRC2836_12_943", SRC_943, "CFC943_0_parent_quotient_map;CFC943_1_observed_coframe_descent;CFC943_7_contract_verdict", "coframe coupling contract"),
        ("SRC2836_13_519", SRC_519, "UOC519_0_single_coframe_field;UOC519_5_no_conformal_disformal_shadow_frame", "same coframe parent clause"),
        ("SRC2836_14_10", SRC_10, "R_AB = ln(T^2 S);theta_0 = T c dt;theta_1 = sqrt(S) dr", "observer-map definition showing R_AB moves coframe unless quotient-signed"),
    ]
    return [source_row(*spec) for spec in specs]


def verticality_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VT2836_0_exact_kernel_condition",
            "vertical kernel condition",
            "If v_R is tangent to the parent quotient-null orbit, then Dq_R[v_R]=0.",
            "QM637_2_vertical_kernel;CFC943_0_parent_quotient_map",
            "EXACT_CONDITIONAL",
            "requires parent to identify actual R_AB variation as quotient-null",
            "would activate matter chain-rule zero",
            True,
        ),
        (
            "VT2836_1_actual_RAB_direction",
            "actual R_AB direction",
            "v_R changes R_AB=ln(T^2 S), with observer coframe theta_0=T c dt and theta_1=sqrt(S)dr.",
            "R_AB = ln(T^2 S);theta_0 = T c dt;theta_1 = sqrt(S) dr",
            "OBSERVABLE_IN_CURRENT_SCAFFOLD",
            "in the current observer-map scaffold R_AB moves rods/clocks unless quotient/basicity is parent-signed",
            "cannot call R_AB invisible from old variables alone",
            False,
        ),
        (
            "VT2836_2_observed_coframe_basicity",
            "observed coframe basicity",
            "e_obs(Phi)=Obs_e(q_R(Phi)) and DObs_e(Dq_R[v_R])=0.",
            "CFC943_1_observed_coframe_descent;CZT863_0_chain_rule_zero;OF637_0_observed_geometry",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "observed coframe descent is a contract, not a current parent derivation for R_AB",
            "matter metric variation zero remains unavailable",
            False,
        ),
        (
            "VT2836_3_no_shadow_counterexample",
            "hidden coframe/readout channel",
            "If e_hat=exp(F(R_AB))e_obs or any R_AB-dependent source frame affects matter, then R_AB is observable/finite-coupled.",
            "OF637_2_counterexample_filter;UOC519_5_no_conformal_disformal_shadow_frame;CFC943_6_no_shadow_frame_rule",
            "COUNTEREXAMPLE_FILTER_ACTIVE",
            "filter classifies such channels but does not prove F'(R_AB)=0",
            "hidden channels must remain finite source-vector terms",
            False,
        ),
        (
            "VT2836_4_joint_verdict",
            "R_AB verticality theorem",
            "Current parent proves Dq_R[v_R]=0 and e_obs=Obs(q_R(Phi)) for actual R_AB before matter coupling.",
            "CON2261_6_joint_contract;THM2260_3_verdict;NF2835_5_verdict",
            "NOT_DERIVED_CURRENT_CORPUS",
            "R_AB ownership/basicity is the missing common premise",
            "finite RAB source vector remains live",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "verticality_id": row_id,
                "target": target,
                "statement": statement,
                "source_anchors": anchors,
                "status": status,
                "proof_or_blocker": blocker,
                "effect_or_fallback": effect,
                "conditional_piece_proved": conditional,
                "verticality_closed": False,
                "control_only": True,
            }
        )
        for row_id, target, statement, anchors, status, blocker, effect, conditional in specs
    ]


def coframe_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CB2836_0_coframe_definition",
            "observer coframe dependence",
            "theta_0=T c dt and theta_1=sqrt(S)dr, so R_AB=ln(T^2S) is coframe-visible before quotienting.",
            "VISIBLE_IN_SCAFFOLD",
            "10-observer-map-symplectic-contract.md",
        ),
        (
            "CB2836_1_basicity_condition",
            "basicity condition",
            "e_obs is basic iff Lie_{v_R}e_obs=0, equivalently e_obs=Obs_e(q_R(Phi)) with Dq_R[v_R]=0.",
            "CONDITIONAL_CONTRACT",
            "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        ),
        (
            "CB2836_2_matter_sensitivity",
            "matter sensitivity",
            "If Lie_{v_R}e_obs is nonzero, ordinary Hilbert matter sees R_AB and J_R need not vanish.",
            "LIVE_COUNTERCHANNEL",
            "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv",
        ),
        (
            "CB2836_3_no_marker_bypass",
            "constant/material marker bypass",
            "Even if metric/frame part descends, theta_A/m_A/q_A must be fixed or quotient-owned, else vertical matter charge survives.",
            "NOT_PARENT_SIGNED",
            "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv;P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        ),
        (
            "CB2836_4_boundary_basicity",
            "boundary coframe/source basicity",
            "Boundary and source-worldtube readout must also descend through q_R-boundary data before Pi_R/Q_R_body can vanish.",
            "NOT_DERIVED",
            "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv;P8_Y5_R2FR_2835_RAB_SOURCE_SLOT_NORMAL_FORM_ATTEMPT.csv",
        ),
    ]
    return [
        nonclaim(
            {
                "coframe_id": row_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "source_reference": source_ref,
                "basicity_closed": False,
                "control_only": True,
            }
        )
        for row_id, obj, statement, status, source_ref in specs
    ]


def chain_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CR2836_0_metric_chain",
            "metric/coframe chain rule",
            "delta_{v_R} S_matter = (delta Sbar/dE_obs) DObs_e(Dq_R[v_R])",
            "zero if Dq_R[v_R]=0 and e_obs descends",
            "OF637_1_chain_rule;CZT863_0_chain_rule_zero",
            "MISSING_PARENT_SIGNED_RAB_VERTICALITY",
        ),
        (
            "CR2836_1_constants_chain",
            "constants/material chain rule",
            "+ (partial Sbar/partial theta_A) delta_{v_R} theta_A",
            "zero only if material constants/markers are fixed or quotient-owned",
            "OF637_1_chain_rule;CFC943_3_constants_and_masses",
            "MISSING_NO_MARKER_NO_SPURION_CLAUSE",
        ),
        (
            "CR2836_2_connection_chain",
            "connection/non-Hilbert chain",
            "omega_m=omega[e_obs] or retained non-Hilbert current",
            "zero only if matter connection is induced by descended e_obs",
            "CFC943_4_connection_lock",
            "MISSING_CONNECTION_SOURCE_SILENCE",
        ),
        (
            "CR2836_3_boundary_chain",
            "boundary/source-worldtube chain",
            "delta_{v_R} B = DB(Dq_R_boundary[v_R]) plus explicit Pi_R if boundary is not basic",
            "zero only if boundary functor descends",
            "CON2261_3_boundary_functor;NF2835_2_boundary_functor",
            "MISSING_BOUNDARY_BASICITY_OR_PIR_BOUND",
        ),
    ]
    return [
        nonclaim(
            {
                "chain_id": row_id,
                "chain_piece": piece,
                "formula": formula,
                "zero_condition": zero_condition,
                "source_anchors": anchors,
                "missing_for_claim": missing,
                "chain_rule_ready": True,
                "zero_proved": False,
                "control_only": True,
            }
        )
        for row_id, piece, formula, zero_condition, anchors, missing in specs
    ]


def finite_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_text = read_text(SRC_2835_FINITE)
    for row_id, symbol, anchor in [
        ("FR2836_0_JR", "J_R", "FV2835_1_CRT"),
        ("FR2836_1_epsilon", "epsilon_RAB_source", "FV2835_2_epsilon"),
        ("FR2836_2_QR_body", "Q_R_body", "FV2835_3_QR_body"),
        ("FR2836_3_PiR", "Pi_R", "FV2835_4_PiR"),
        ("FR2836_4_tail", "tail_R", "FV2835_5_tail"),
        ("FR2836_5_total", "RAB_source_vector_abs", "FV2835_6_total"),
    ]:
        rows.append(
            nonclaim(
                {
                    "finite_carryover_id": row_id,
                    "symbol": symbol,
                    "source_anchor": anchor,
                    "anchor_found": anchor in source_text,
                    "carryover_reason": "R_AB verticality/basicity is not parent-signed",
                    "required_before_score": "theorem-zero certificate or source-backed numeric bound in common normalization",
                    "theorem_zero": False,
                    "numeric_value_present": False,
                    "source_backed": False,
                    "control_only": True,
                }
            )
        )
    return rows


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2836_0_qshape", "q-shape forgetting is not observed-coframe basicity", "Dq[v]=0 for some map is not enough unless the actual matter/readout q_R and e_obs are signed", "blocks cheap verticality"),
        ("GUARD2836_1_same_frame", "same-frame language is not verticality", "one observed frame can still depend on R_AB", "must prove Lie_{v_R}e_obs=0"),
        ("GUARD2836_2_absence", "absence of explicit R_AB terms is not operator grammar proof", "legacy action omission is weaker than ParentGenerate exclusion", "operator/source slots remain live"),
        ("GUARD2836_3_boundary", "matter verticality does not kill boundary Pi_R", "Q_R=-Pi_R from source matching remains a separate boundary theorem", "Pi_R/Q_R_body stay live"),
        ("GUARD2836_4_local_gr", "verticality would not alone prove full local GR", "beta, preferred-frame, endpoint/readout, q_loc and LHS operator gates remain open", "no local-GR/Newton claim"),
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
    verticality_open = not any(row["verticality_closed"] for row in rows["verticality"])
    basicity_open = not any(row["basicity_closed"] for row in rows["coframe"])
    chain_ready = all(row["chain_rule_ready"] and not row["zero_proved"] for row in rows["chain"])
    finite_nonclaim = all(row["anchor_found"] and not row["theorem_zero"] and not row["numeric_value_present"] and not row["source_backed"] for row in rows["finite"])
    guards_active = all(row["guard_active"] for row in rows["guards"])
    specs = [
        ("GATE2836_0_sources", "all 2836 source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2836_1_verticality", "actual R_AB direction is proved vertical/basic", False, "BLOCKED", "R_AB moves observer coframe in current scaffold and quotient-basicity is unsigned"),
        ("GATE2836_2_chain_rule", "matter chain-rule zero is usable as claim", False, "BLOCKED", "chain rule is exact conditional but parent verticality/constants/boundary clauses are missing"),
        ("GATE2836_3_chain_ready", "chain-rule ledger is written without score", chain_ready, "PASS_INTERNAL_NONCLAIM" if chain_ready else "BLOCKED", "zero conditions are explicit"),
        ("GATE2836_4_finite", "finite source-vector carryover remains staged", finite_nonclaim, "PASS_INTERNAL_NONCLAIM" if finite_nonclaim else "BLOCKED", "all carryover rows are value-missing nonclaims"),
        ("GATE2836_5_guards", "verticality shortcut guards are active", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "no q-shape/same-frame/absence shortcut accepted"),
        ("GATE2836_6_open", "verticality and basicity remain unclaimed", verticality_open and basicity_open, "PASS_NONCLAIM" if verticality_open and basicity_open else "BLOCKED", "2836 does not overclaim source silence"),
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
        ("DEC2836_0_conditional", "The chain-rule theorem is mathematically clean.", "EXACT_CONDITIONAL_RETAINED", "if Dq_R[v_R]=0 and e_obs descends, direct matter variation vanishes.", "keep as parent-action contract"),
        ("DEC2836_1_no_claim", "The actual R_AB direction is not proved vertical.", "VERTICALITY_NOT_DERIVED", "R_AB=ln(T^2S) moves the observer coframe in the current scaffold.", "do not set J_R/Pi_R/Q_R_body to zero"),
        ("DEC2836_2_next", "Next decisive target is R_AB ownership selector.", "OWNERSHIP_SELECTOR_SELECTED", "R_AB must be classified as auxiliary representative, physical finite field, or constrained variable.", "derive ownership selector or commit to finite residual branch"),
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
                "next_id": "NEXT2836_0_2837",
                "status": "selected_primary",
                "target_doc": "2837-Y5-R2FR-RAB-ownership-selector-auxiliary-representative-or-finite-field-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_RAB_ownership_selector_auxiliary_representative_or_finite_field_under_AX1090_2837.py",
                "mission": "classify R_AB ownership: auxiliary/representative vertical data, parent-constrained variable, or physical finite residual field; use that selector to decide whether to continue zero-proof or finite source-vector route",
                "acceptance": "must cite 2836 verticality verdict, 2260 parent protection contract, 10 observer-map definition and 2835 finite source vector; no J_R/Pi_R/Q_R=0 claim unless ownership and boundary clauses are signed",
                "forbidden": "do not choose auxiliary ownership merely because it helps local GR; do not choose finite branch without preserving source-vector gates; do not import GR AB=1",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2836_0_finite_copy", OUTPUTS["finite"], BRANCH_OUTPUTS["finite_copy"], "local-bounds copy of finite RAB source-vector carryover"),
        ("BR2836_1_verticality_copy", OUTPUTS["verticality"], BRANCH_OUTPUTS["verticality_copy"], "source-weight copy of RAB verticality theorem attempt"),
        ("BR2836_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for ownership selector"),
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
        ("VAL2836_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2836_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2836_2_verticality_unclaimed", not any(row["verticality_closed"] for row in rows_by_name["verticality"]), "RAB verticality remains unclaimed"),
        ("VAL2836_3_basicity_unclaimed", not any(row["basicity_closed"] for row in rows_by_name["coframe"]), "observed coframe basicity remains unclaimed"),
        ("VAL2836_4_chain_ready_nonclaim", all(row["chain_rule_ready"] and not row["zero_proved"] for row in rows_by_name["chain"]), "chain-rule rows are ready but zero-unproved"),
        ("VAL2836_5_finite_carryover_nonclaim", all(row["anchor_found"] and not row["theorem_zero"] and not row["numeric_value_present"] and not row["source_backed"] for row in rows_by_name["finite"]), "finite carryover rows remain nonclaim"),
        ("VAL2836_6_guards_active", all(row["guard_active"] for row in rows_by_name["guards"]), "all verticality guards are active"),
        ("VAL2836_7_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows source silence or local GR"),
        ("VAL2836_8_no_numeric_predictions", no_numeric_prediction_insertions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2836_9_next_target_2837", any(row["next_id"] == "NEXT2836_0_2837" and row["selected"] for row in rows_by_name["next"]), "RAB ownership selector selected next"),
        ("VAL2836_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2836_11_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2836_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2836_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2836_14_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim or claim_allowed flag is true"),
        ("VAL2836_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2836_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2836_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2836_OVERALL",
            "passed": overall,
            "detail": "2836 attempts RAB verticality and observed-coframe basicity, keeps the chain-rule theorem as exact conditional, refuses to claim actual R_AB invisibility because R_AB moves the observer coframe unless parent-signed, carries over finite source-vector rows, and selects RAB ownership selector next.",
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
    content = f"""# 2836 - Y5 R2FR RAB Verticality And Observed Coframe Basicity Or Finite Source Vector Under AX1090

Status: `Y5_R2FR_2836_chain_rule_conditional_RAB_verticality_not_derived`

## Private Verdict

2836 proves the useful conditional, but not the actual `R_AB` theorem.

The clean theorem is:

```text
if Dq_R[v_R] = 0
and e_obs = Obs_e(q_R(Phi))
then delta_{{v_R}} S_matter = 0
```

That is real. But current `R_AB` is not automatically such a vertical variable. In the observer-map scaffold:

```text
R_AB = ln(T^2 S)
theta_0 = T c dt
theta_1 = sqrt(S) dr
```

So changing `R_AB` changes the local observer coframe unless the future parent action explicitly classifies that direction as quotient-representative/basic before matter coupling.

Result: no `J_R=0`, `Pi_R=0`, `Q_R=0`, local-GR, or Newton claim. The finite source vector stays live. The next target is an ownership selector: auxiliary representative, parent-constrained variable, or physical finite residual field.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## RAB Verticality Theorem Attempt

{markdown_table(rows["verticality"], ["verticality_id", "target", "status", "proof_or_blocker", "effect_or_fallback", "conditional_piece_proved", "verticality_closed", "valid_for_claim"])}

## Observed Coframe Basicity Audit

{markdown_table(rows["coframe"], ["coframe_id", "object", "statement", "current_status", "basicity_closed", "valid_for_claim"])}

## Matter Chain Rule Ledger

{markdown_table(rows["chain"], ["chain_id", "chain_piece", "formula", "zero_condition", "missing_for_claim", "chain_rule_ready", "zero_proved", "valid_for_claim"])}

## Finite RAB Source Vector Carryover

{markdown_table(rows["finite"], ["finite_carryover_id", "symbol", "source_anchor", "anchor_found", "carryover_reason", "numeric_value_present", "valid_for_claim"])}

## Verticality Guards

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
    rows["verticality"] = verticality_rows()
    rows["coframe"] = coframe_rows()
    rows["chain"] = chain_rows()
    rows["finite"] = finite_rows()
    rows["guards"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "verticality", "coframe", "chain", "finite", "guards", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2836_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2836_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
