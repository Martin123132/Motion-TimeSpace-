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

DOC = ROOT / "2837-Y5-R2FR-RAB-ownership-selector-auxiliary-representative-or-finite-field-under-AX1090.md"

SRC_2836_NEXT = RESIDUALS / "P8_Y5_R2FR_2836_NEXT_TARGET.csv"
SRC_2836_VERT = RESIDUALS / "P8_Y5_R2FR_2836_RAB_VERTICALITY_THEOREM_ATTEMPT.csv"
SRC_2836_FINITE = RESIDUALS / "P8_Y5_R2FR_2836_FINITE_RAB_SOURCE_VECTOR_CARRYOVER_NONCLAIM.csv"
SRC_2260_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_PARENT_PROTECTION_CONTRACT.csv"
SRC_2260_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_CONDITIONAL_THEOREM.csv"
SRC_2260_QUEUE = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_LIVE_RESIDUAL_ACQUISITION_QUEUE.csv"
SRC_1257 = ROOT / "1257-Y5-R10-ZR-lambdaR-selector-from-parent-primitives.md"
SRC_1256 = ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md"
SRC_2288 = BETA_DOCS / "RAB_AUXILIARY_OR_FINITE_ZQ_2288_NONCLAIM.csv"
SRC_2236 = BETA_DOCS / "RAB_AUXILIARY_GRAMMAR_2236_NONCLAIM.csv"
SRC_2261 = BETA_DOCS / "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2837_SOURCE_REGISTER.csv",
    "selector": RESIDUALS / "P8_Y5_R2FR_2837_RAB_OWNERSHIP_SELECTOR.csv",
    "branch": RESIDUALS / "P8_Y5_R2FR_2837_BRANCH_ROUTING_LEDGER.csv",
    "requirements": RESIDUALS / "P8_Y5_R2FR_2837_OWNERSHIP_REQUIREMENTS.csv",
    "finite": RESIDUALS / "P8_Y5_R2FR_2837_FINITE_RESIDUAL_ACQUISITION_CARRYOVER_NONCLAIM.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2837_OWNERSHIP_GUARDS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2837_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2837_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2837_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2837_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2837_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_copy": LOCAL_BOUNDS / "RAB_finite_residual_acquisition_carryover_2837_NONCLAIM.csv",
    "selector_copy": SOURCE_WEIGHT / "RAB_ownership_selector_2837_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2837_second_class_auxiliary_block_or_finite_residual_NEXT.csv",
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
        ("SRC2837_0_2836_next", SRC_2836_NEXT, "NEXT2836_0_2837", "2836 selected RAB ownership selector"),
        ("SRC2837_1_2836_verticality", SRC_2836_VERT, "VT2836_1_actual_RAB_direction;VT2836_4_joint_verdict", "2836 verticality verdict"),
        ("SRC2837_2_2836_finite", SRC_2836_FINITE, "FR2836_2_QR_body;FR2836_3_PiR;FR2836_5_total", "2836 finite source-vector carryover"),
        ("SRC2837_3_2260_contract", SRC_2260_CONTRACT, "CON2260_0_parent_sorts;CON2260_1_action_image;CON2260_6_joint_contract", "2260 parent protection contract"),
        ("SRC2837_4_2260_theorem", SRC_2260_THEOREM, "THM2260_0_statement;THM2260_1_variation;THM2260_3_verdict", "2260 conditional second-class theorem"),
        ("SRC2837_5_2260_queue", SRC_2260_QUEUE, "ACQ2260_1_ZR;ACQ2260_3_JR;ACQ2260_4_BR", "2260 finite residual acquisition queue"),
        ("SRC2837_6_1257", SRC_1257, "THM1257_0_conditional_ZR_selector;ROUTE1257_0_clean_zero;ROUTE1257_1_kinetic_bound", "1257 ownership/ZR selector"),
        ("SRC2837_7_1256", SRC_1256, "BR1256_0_nonprop_constraint;BR1256_1_kinetic_finite_hair;BR1256_2_massive_suppressed_hair", "1256 variational branch audit"),
        ("SRC2837_8_2288", SRC_2288, "AUX2288_1_vR_first_class;AUX2288_2_second_class;AUX2288_3_finite_escape", "2288 auxiliary/finite selector"),
        ("SRC2837_9_2236", SRC_2236, "FALL2236_0_ZR;FALL2236_3_BR;FALL2236_4_projection", "2236 finite coefficient fallback"),
        ("SRC2837_10_2261", SRC_2261, "CON2261_0_parent_sorts;CON2261_1_action_image;CON2261_6_joint_contract", "2261 primitive derivation audit"),
        ("SRC2837_11_10", SRC_10, "R_AB = ln(T^2 S);a genuine constraint whose multiplier has a parent origin", "observer-map contract"),
    ]
    return [source_row(*spec) for spec in specs]


def selector_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SEL2837_0_first_class_representative",
            "first-class representative/gauge-null",
            "R_AB shifts are q-vertical gauge directions with Dq_R[v_R]=0 off shell.",
            "AUX2288_1_vR_first_class;VT2836_0_exact_kernel_condition",
            "REJECT_CURRENT_PROMOTION",
            "pure R_AB shifts fail compatibility-surface tangency; compatibility-preserving shifts are not q-vertical in current evidence.",
            "do not use first-class magic to set J_R/Pi_R/Q_R zero",
            False,
        ),
        (
            "SEL2837_1_second_class_auxiliary",
            "second-class/algebraic auxiliary block",
            "R_AB and Lambda_R enter algebraically; E_Lambda fixes R_AB=C_AB[Q], E_R solves Lambda_R=0 if J_R,B_R,readout_regen vanish.",
            "AUX2288_2_second_class;THM2260_1_variation;CON2260_1_action_image",
            "BEST_CONDITIONAL_ROUTE_RETAINED",
            "requires parent-signed auxiliary block, source silence, boundary silence, readout stability and operator exclusion.",
            "continue zero-proof only if this block is parent-derived",
            False,
        ),
        (
            "SEL2837_2_constrained_nonpropagating",
            "parent-constrained nonpropagating variable",
            "A genuine parent multiplier/constraint enforces R_AB=0 or R_AB=C_AB before readout.",
            "BR1256_0_nonprop_constraint;ROUTE1257_0_clean_zero;R_AB = ln(T^2 S)",
            "CLEAN_ROUTE_UNSIGNED",
            "lambda_R origin, Dirac/constraint closure, matter compatibility and boundary silence remain missing.",
            "cannot claim local GR until constraint is parent-owned",
            False,
        ),
        (
            "SEL2837_3_physical_finite_field",
            "physical finite residual field",
            "R_AB is independent or derivative/source constructors survive; retain Z_R/M_R^2/J_R/B_R and arena projection rows.",
            "AUX2288_3_finite_escape;ROUTE1257_1_kinetic_bound;BR1256_2_massive_suppressed_hair",
            "MANDATORY_IF_PROTECTIONS_FAIL",
            "current parent does not prove auxiliary/constrained ownership, so finite branch remains live.",
            "source or bound finite residuals before empirical scoring",
            True,
        ),
        (
            "SEL2837_4_current_verdict",
            "current R_AB ownership selector",
            "Current evidence selects no theorem-zero ownership; it retains second-class auxiliary as best conditional and finite physical residual as mandatory fallback.",
            "THM2260_3_verdict;VT2836_4_joint_verdict;AUX2288_3_finite_escape",
            "UNDECIDED_OWNERSHIP_FINITE_BRANCH_RETAINED",
            "no route is parent-signed strongly enough to kill the finite source vector.",
            "next: try to parent-sign second-class auxiliary block or move to finite coefficients",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "selector_id": row_id,
                "ownership_option": option,
                "statement": statement,
                "source_anchors": anchors,
                "status": status,
                "proof_or_blocker": blocker,
                "routing_effect": effect,
                "finite_branch_retained": finite,
                "ownership_closed": False,
                "control_only": True,
            }
        )
        for row_id, option, statement, anchors, status, blocker, effect, finite in specs
    ]


def branch_rows_ledger() -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE2837_0_auxiliary_zero",
            "if second-class auxiliary block is parent-signed",
            "continue zero-proof route: R_AB algebraically eliminated before readout",
            "parent action image; Lambda_R origin; J_R=0; B_R/Pi_R=0; readout_regen=0; no derivative constructors",
            "HELD_CONDITIONAL",
        ),
        (
            "ROUTE2837_1_nonprop_constraint",
            "if parent constraint/multiplier is signed",
            "R_AB=0 closure becomes theorem candidate",
            "constraint algebra; Dirac closure; matter/boundary compatibility; no GR AB=1 import",
            "HELD_CONDITIONAL",
        ),
        (
            "ROUTE2837_2_finite_kinetic",
            "if R_AB independent and massless/long-range",
            "retain finite q_Rhat/source-vector branch and require Z_R,Q_R,J_R,B_R values",
            "Z_R; source charge; boundary class; PPN/R10/clock/orbital projections",
            "LIVE_FALLBACK",
        ),
        (
            "ROUTE2837_3_massive_suppressed",
            "if R_AB independent with positive mass gap",
            "derive local range suppression but still source M_R^2/Z_R and source/no-flux conditions",
            "M_R^2; Z_R; scale separation; source silence or finite body charge",
            "LIVE_FALLBACK",
        ),
    ]
    return [
        nonclaim(
            {
                "route_id": row_id,
                "condition": condition,
                "route": route,
                "required_evidence": required,
                "status": status,
                "selected_as_claim": False,
                "control_only": True,
            }
        )
        for row_id, condition, route, required, status in specs
    ]


def requirements_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2837_0_field_list", "typed parent field list", "classify R_AB as auxiliary representative, constrained variable, or physical field", "MISSING_PARENT_FIELD_STATUS", "CON2260_0_parent_sorts;CON2261_0_parent_sorts"),
        ("REQ2837_1_aux_block", "algebraic auxiliary block", "parent image contains Lambda_R(R_AB-C_AB[Q]) and no derivative R_AB constructors", "MISSING_PARENT_ACTION_IMAGE", "CON2260_1_action_image;THM2260_2_operator"),
        ("REQ2837_2_source_protection", "source protection", "J_R=0, B_R/Pi_R=0 and readout_regen=0 jointly", "UNSIGNED_SOURCE_BOUNDARY_READOUT", "PROT2260_0_JR;PROT2260_1_BR;PROT2260_2_readout"),
        ("REQ2837_3_finite_coefficients", "finite coefficients", "if field route remains live, source Z_R, M_R^2, J_R, B_R and tau projections", "MISSING_SOURCE_BACKED_INPUT", "FALL2236_0_ZR;FALL2236_1_MR2;FALL2236_2_JR;FALL2236_3_BR"),
        ("REQ2837_4_no_GR_import", "no GR import", "do not use Schwarzschild AB=1 or desired local GR behavior to pick ownership", "GUARD_ACTIVE", "R_AB = ln(T^2 S);NEXT2836_0_2837"),
    ]
    return [
        nonclaim(
            {
                "requirement_id": row_id,
                "requirement": requirement,
                "required_statement": statement,
                "current_status": status,
                "source_anchors": anchors,
                "requirement_closed": False,
                "control_only": True,
            }
        )
        for row_id, requirement, statement, status, anchors in specs
    ]


def finite_rows() -> list[dict[str, Any]]:
    specs = [
        ("FIN2837_0_ZR", "Z_R", "finite gradient coefficient for R_AB", "MISSING_SOURCE_BACKED_INPUT", "FALL2236_0_ZR;ACQ2260_1_ZR"),
        ("FIN2837_1_MR2", "M_R^2", "mass gap/screening scale", "MISSING_SOURCE_BACKED_INPUT", "FALL2236_1_MR2;ACQ2260_2_MR2"),
        ("FIN2837_2_JR", "J_R", "direct matter/source coupling to R_AB", "MISSING_SOURCE_BACKED_INPUT", "FALL2236_2_JR;ACQ2260_3_JR"),
        ("FIN2837_3_BR", "B_R/Pi_R^n", "boundary reciprocal charge/flux", "MISSING_SOURCE_BACKED_INPUT", "FALL2236_3_BR;ACQ2260_4_BR"),
        ("FIN2837_4_projection", "tau_R10/tau_PPN/tau_clock/tau_orbital", "arena projection from finite R_AB residual", "MISSING_ARENA_PROJECTION", "FALL2236_4_projection;ACQ2260_5_tau_R10;ACQ2260_6_tau_PPN"),
        ("FIN2837_5_source_vector", "RAB_source_vector_abs", "2836 finite source-vector carryover", "SCHEMA_READY_VALUES_MISSING", "FR2836_5_total"),
    ]
    return [
        nonclaim(
            {
                "finite_id": row_id,
                "symbol": symbol,
                "meaning": meaning,
                "current_status": status,
                "source_anchors": anchors,
                "numeric_value_present": False,
                "source_backed": False,
                "theorem_zero": False,
                "control_only": True,
            }
        )
        for row_id, symbol, meaning, status, anchors in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2837_0_no_desire", "do not choose auxiliary ownership because it helps local GR", "ownership must come from parent primitive grammar", "zero route remains conditional"),
        ("GUARD2837_1_no_first_class_magic", "first-class promotion is rejected in current evidence", "pure R_AB shifts fail compatibility-surface tangency", "do not claim q-vertical gauge null"),
        ("GUARD2837_2_second_class_joint", "second-class route needs all protections jointly", "source, boundary, readout and operator exclusions are indivisible", "no partial local-GR credit"),
        ("GUARD2837_3_finite_retained", "finite branch is mandatory if protections fail", "physical/derivative/source constructors would make R_AB testable", "keep acquisition rows live"),
        ("GUARD2837_4_no_GR_import", "do not import GR AB=1", "R_AB=0 is the target, not a premise", "no Schwarzschild shortcut"),
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
    ownership_open = not any(row["ownership_closed"] for row in rows["selector"])
    requirements_open = not any(row["requirement_closed"] for row in rows["requirements"])
    finite_nonclaim = all(not row["numeric_value_present"] and not row["source_backed"] and not row["theorem_zero"] for row in rows["finite"])
    guards_active = all(row["guard_active"] for row in rows["guards"])
    specs = [
        ("GATE2837_0_sources", "all 2837 source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2837_1_auxiliary", "R_AB auxiliary/representative ownership is parent-signed", False, "BLOCKED", "parent field list/action image/source protections are unsigned"),
        ("GATE2837_2_first_class", "R_AB is first-class q-vertical gauge-null", False, "BLOCKED", "current evidence rejects first-class promotion"),
        ("GATE2837_3_finite", "finite branch acquisition rows remain staged", finite_nonclaim, "PASS_INTERNAL_NONCLAIM" if finite_nonclaim else "BLOCKED", "finite rows exist but are value-missing"),
        ("GATE2837_4_guards", "ownership guards are active", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "no desire/first-class/GR-import shortcut accepted"),
        ("GATE2837_5_open", "ownership requirements remain open and unclaimed", ownership_open and requirements_open, "PASS_NONCLAIM" if ownership_open and requirements_open else "BLOCKED", "2837 selects no theorem-zero route"),
        ("GATE2837_6_local_gr", "local GR/Newton reduction is derived", False, "BLOCKED", "ownership selector has not closed zero/finite/boundary gates"),
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
        ("DEC2837_0_selector", "Do not select theorem-zero ownership yet.", "OWNERSHIP_UNDECIDED", "auxiliary/constrained route is best conditional but not parent-signed; first-class route is rejected.", "keep finite branch live"),
        ("DEC2837_1_best_route", "Best zero route is second-class auxiliary, not first-class gauge magic.", "SECOND_CLASS_CONDITIONAL", "2288 retains second-class compatibility elimination as the clean conditional route.", "try to parent-sign auxiliary block and protections"),
        ("DEC2837_2_finite", "Finite residual branch remains mandatory fallback.", "FINITE_BRANCH_RETAINED", "if auxiliary protections fail, Z_R/M_R^2/J_R/B_R/tau rows must be sourced and tested.", "build 2838 second-class auxiliary block proof or finite residual decision"),
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
                "next_id": "NEXT2837_0_2838",
                "status": "selected_primary",
                "target_doc": "2838-Y5-R2FR-second-class-auxiliary-block-parent-signature-or-finite-RAB-residual-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_second_class_auxiliary_block_parent_signature_or_finite_RAB_residual_under_AX1090_2838.py",
                "mission": "try to parent-sign the second-class auxiliary block R_AB,Lambda_R: action image, no derivative constructors, source/boundary/readout protections; if not, promote finite residual acquisition queue without scoring",
                "acceptance": "must cite 2837 selector, 2260 theorem, 2288 second-class row and finite coefficient rows; no R_AB=0/J_R=0/Pi_R=0 claim unless all protections close jointly",
                "forbidden": "do not use first-class gauge language; do not pick second-class route just because it recovers GR; do not drop finite branch",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2837_0_finite_copy", OUTPUTS["finite"], BRANCH_OUTPUTS["finite_copy"], "local-bounds copy of finite residual acquisition carryover"),
        ("BR2837_1_selector_copy", OUTPUTS["selector"], BRANCH_OUTPUTS["selector_copy"], "source-weight copy of RAB ownership selector"),
        ("BR2837_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for second-class auxiliary block or finite residual"),
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
        ("VAL2837_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2837_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2837_2_ownership_unclaimed", not any(row["ownership_closed"] for row in rows_by_name["selector"]), "RAB ownership remains unclaimed"),
        ("VAL2837_3_requirements_open", not any(row["requirement_closed"] for row in rows_by_name["requirements"]), "ownership requirements remain open"),
        ("VAL2837_4_finite_nonclaim", all(not row["numeric_value_present"] and not row["source_backed"] and not row["theorem_zero"] for row in rows_by_name["finite"]), "finite residual rows remain nonclaim"),
        ("VAL2837_5_guards_active", all(row["guard_active"] for row in rows_by_name["guards"]), "all ownership guards are active"),
        ("VAL2837_6_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows source silence or local GR"),
        ("VAL2837_7_no_numeric_predictions", no_numeric_prediction_insertions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2837_8_next_target_2838", any(row["next_id"] == "NEXT2837_0_2838" and row["selected"] for row in rows_by_name["next"]), "second-class auxiliary block selected next"),
        ("VAL2837_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2837_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2837_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2837_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2837_13_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim or claim_allowed flag is true"),
        ("VAL2837_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2837_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2837_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2837_OVERALL",
            "passed": overall,
            "detail": "2837 classifies RAB ownership routes, rejects current first-class promotion, retains second-class auxiliary as best conditional, keeps finite residual acquisition mandatory if protections fail, and selects second-class auxiliary block parent signature next.",
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
    content = f"""# 2837 - Y5 R2FR RAB Ownership Selector: Auxiliary, Representative, Or Finite Field Under AX1090

Status: `Y5_R2FR_2837_ownership_undecided_second_class_conditional_finite_retained`

## Private Verdict

2837 classifies the `R_AB` ownership routes without pretending one is proved.

Current selector:

```text
first-class / gauge-null: rejected by current evidence
second-class auxiliary block: best conditional zero route
parent constraint / multiplier: clean but unsigned
physical finite field: mandatory fallback if protections fail
```

So we do **not** pick `R_AB` as auxiliary just because it would give local GR. The honest state is: second-class auxiliary elimination is the best route to try next, but finite `Z_R/M_R^2/J_R/B_R/tau` rows remain live until the parent action signs the auxiliary block plus source, boundary, readout, and operator protections jointly.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## RAB Ownership Selector

{markdown_table(rows["selector"], ["selector_id", "ownership_option", "status", "proof_or_blocker", "routing_effect", "finite_branch_retained", "ownership_closed", "valid_for_claim"])}

## Branch Routing Ledger

{markdown_table(rows["branch"], ["route_id", "condition", "route", "required_evidence", "status", "selected_as_claim", "valid_for_claim"])}

## Ownership Requirements

{markdown_table(rows["requirements"], ["requirement_id", "requirement", "required_statement", "current_status", "requirement_closed", "valid_for_claim"])}

## Finite Residual Acquisition Carryover

{markdown_table(rows["finite"], ["finite_id", "symbol", "meaning", "current_status", "numeric_value_present", "valid_for_claim"])}

## Ownership Guards

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
    rows["selector"] = selector_rows()
    rows["branch"] = branch_rows_ledger()
    rows["requirements"] = requirements_rows()
    rows["finite"] = finite_rows()
    rows["guards"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "selector", "branch", "requirements", "finite", "guards", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2837_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2837_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
