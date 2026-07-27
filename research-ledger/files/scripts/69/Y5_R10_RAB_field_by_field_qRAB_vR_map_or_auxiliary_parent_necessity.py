from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1271"
TITLE = "1271-Y5-R10-RAB-field-by-field-qRAB-vR-map-or-auxiliary-parent-necessity"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FIELD_MAP_PATH = OUT_DIR / f"{PACK_ID}_FIELD_BY_FIELD_QRAB_VR_MAP.csv"
INVARIANCE_TEST_PATH = OUT_DIR / f"{PACK_ID}_OBSERVED_INVARIANCE_TEST.csv"
AUX_NECESSITY_PATH = OUT_DIR / f"{PACK_ID}_AUXILIARY_PARENT_NECESSITY_TARGET.csv"
ROUTE_DECISION_PATH = OUT_DIR / f"{PACK_ID}_ROUTE_DECISION_AFTER_FIELD_MAP.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1271_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def validate_intake_row(path: Path, intake_class: str, row: dict[str, str]) -> dict[str, object]:
    row_id = row.get("row_id") or row.get("template_id") or row.get("coefficient_symbol") or "MISSING_ROW_ID"
    required_columns = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
        "valid_for_claim",
        "claim_allowed",
    ]
    missing_columns = [column for column in required_columns if column not in row]
    source_raw = str(row.get("source_path", "")).strip()
    anchor = str(row.get("source_anchor", "")).strip()
    source = None if not source_raw or source_raw.startswith("MISSING_") else source_path(source_raw)
    source_exists = bool(source and source.exists())
    anchor_found = bool(source_exists and anchor and not anchor.startswith("MISSING_") and anchor in read_text(source))
    reasons: list[str] = []
    if intake_class == "docs":
        reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
    if missing_columns:
        reasons.append("MISSING_REQUIRED_COLUMNS:" + ";".join(missing_columns))
    if contains_missing_marker(row):
        reasons.append("MISSING_MARKER_PRESENT")
    if source is None:
        reasons.append("SOURCE_PATH_MISSING_OR_PLACEHOLDER")
    elif not source_exists:
        reasons.append("SOURCE_PATH_NOT_FOUND")
    if not anchor or anchor.startswith("MISSING_"):
        reasons.append("SOURCE_ANCHOR_MISSING_OR_PLACEHOLDER")
    elif source_exists and not anchor_found:
        reasons.append("SOURCE_ANCHOR_NOT_FOUND")
    if str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(row.get("claim_allowed", "")).strip().lower() == "true":
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    return {
        "scan_id": f"SCAN1271_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": "REJECT" if reasons else "ACCEPT_NONCLAIM_SOURCE_READY",
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": not reasons,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def scan_rab_intake() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for intake_class in ["docs", "raw", "accepted"]:
        directory = RAB_INTAKE_DIR / intake_class
        directory.mkdir(parents=True, exist_ok=True)
        for path in sorted(directory.glob("*.csv")):
            for row in read_csv(path):
                results.append(validate_intake_row(path, intake_class, row))
    return results


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        FIELD_MAP_PATH,
        INVARIANCE_TEST_PATH,
        AUX_NECESSITY_PATH,
        ROUTE_DECISION_PATH,
        VALIDATOR_RESCAN_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1271_0_1270_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1270_NEXT_TARGET.csv",
            "needle": "NEXT1270_0_1271",
            "purpose": "handoff to field-by-field q_RAB/v_R map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_1_1270_dq",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1270_DQ_KERNEL_TEST_MATRIX.csv",
            "needle": "DQ1270_0_full_metric_readout",
            "purpose": "full metric readout countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_2_1270_route",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1270_RAB_ROUTE_SELECTION_AFTER_QUOTIENT_TEST.csv",
            "needle": "ROUTE1270_1_auxiliary_compatibility",
            "purpose": "auxiliary route selected after quotient test",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_3_1268_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
            "needle": "CAC1268_1_constraint_action",
            "purpose": "candidate second-class compatibility action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_4_observer_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "observer_map_contract_written_not_satisfied",
            "purpose": "observer-cell contract and R_AB local-GR target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_5_nonprop",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "S_constraint = integral lambda_R R_AB",
            "purpose": "nonpropagating constraint route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_6_phase_volume",
            "local_path": "08-phase-volume-reciprocity-origin.md",
            "needle": "phase_volume_reciprocity_motivated_not_parent_derived",
            "purpose": "phase-volume motivation for parent necessity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_7_hamiltonian_cell",
            "local_path": "09-hamiltonian-radial-cell-derivation.md",
            "needle": "hamiltonian_radial_cell_sharpened_not_parent_derived",
            "purpose": "radial-cell parent theorem remains unproved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_8_1238_residual",
            "local_path": "1238-Y5-R10-first-class-RAB-constraint-or-local-GR-closure-benchmark-scorecard.md",
            "needle": "RV1238_0_QR",
            "purpose": "finite residual Q_R remains live if route fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1271_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite-ZR validator currently accepts no rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    field_map = [
        {
            "map_id": "FMAP1271_0_lapse_A",
            "field_or_readout": "A=T^2=-g_tt/c^2",
            "candidate_vR_action": "delta ln A = a eta_R",
            "observed_in_q": True,
            "Dq_vR": "a eta_R in full metric readout",
            "status": "FAILS_IF_A_OBSERVED",
            "reason": "clock rates/redshift and Newtonian potential see A",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_1_radial_B",
            "field_or_readout": "B=S=g_rr",
            "candidate_vR_action": "delta ln B = (1-a) eta_R",
            "observed_in_q": True,
            "Dq_vR": "(1-a) eta_R in full metric readout",
            "status": "FAILS_IF_B_OBSERVED",
            "reason": "radial rulers, light bending, and PPN gamma see B",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_2_RAB",
            "field_or_readout": "R_AB=ln(A B)=ln(T^2 S)",
            "candidate_vR_action": "delta R_AB = eta_R",
            "observed_in_q": "depends_on_parent_readout",
            "Dq_vR": "nonzero unless q excludes reciprocal strain before readout",
            "status": "TARGET_NOT_VERTICAL_BY_DEFAULT",
            "reason": "R_AB controls AB=1/PPN-gamma-like local reciprocity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_3_angular_radius",
            "field_or_readout": "r^2 dOmega^2",
            "candidate_vR_action": "delta r = 0",
            "observed_in_q": True,
            "Dq_vR": "0 for this component",
            "status": "PASS_TRIVIAL_COMPONENT_ONLY",
            "reason": "angular sector can stay fixed while A/B still move",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_4_clock_readout",
            "field_or_readout": "proper time / clock redshift",
            "candidate_vR_action": "depends on delta T = 0.5 delta ln A",
            "observed_in_q": True,
            "Dq_vR": "nonzero if a != 0",
            "status": "FAILS_GENERICALLY",
            "reason": "clock sector forbids hiding lapse changes in a vertical fibre",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_5_radial_ruler",
            "field_or_readout": "proper radial distance / radial coframe",
            "candidate_vR_action": "depends on delta sqrt(S)=0.5 delta ln B",
            "observed_in_q": True,
            "Dq_vR": "nonzero if a != 1",
            "status": "FAILS_GENERICALLY",
            "reason": "radial routing cannot be quotient-hidden if rulers see S",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_6_null_cone",
            "field_or_readout": "radial null speed c T/sqrt(S)",
            "candidate_vR_action": "delta ln(T/sqrtS)=0.5 a eta_R - 0.5(1-a) eta_R",
            "observed_in_q": True,
            "Dq_vR": "zero only at a=1/2, but then A and B still individually move",
            "status": "PARTIAL_CANCELLATION_NOT_FULL_VERTICALITY",
            "reason": "one observable can be protected by tuning split, not the whole field map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_7_matter_action",
            "field_or_readout": "matter measure/coframe/connection",
            "candidate_vR_action": "inherits changes from A/B unless matter factors through a reduced coframe after constraint",
            "observed_in_q": True,
            "Dq_vR": "unsigned/nonzero in current corpus",
            "status": "MATTER_DESCENT_NOT_SIGNED",
            "reason": "matter descent is a separate AP1265/compatibility clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_8_boundary_charge",
            "field_or_readout": "Q_R/B_R/Pi_R^n boundary data",
            "candidate_vR_action": "boundary variation can carry reciprocal charge",
            "observed_in_q": "boundary_dependent",
            "Dq_vR": "not proved zero",
            "status": "BOUNDARY_SILENCE_NOT_SIGNED",
            "reason": "cell-current work leaves Q_R hair unless constraint/no-flux is proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "FMAP1271_9_aux_reduced_readout",
            "field_or_readout": "readout after parent-signed auxiliary elimination",
            "candidate_vR_action": "no independent v_R remains after E_Lambda/E_R solve the auxiliary pair",
            "observed_in_q": "after_elimination",
            "Dq_vR": "not applicable; variable eliminated before q",
            "status": "BEST_NONSMUGGLING_ROUTE_IF_PARENT_SIGNED",
            "reason": "this avoids pretending an observed metric component is gauge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    invariance_test = [
        {
            "test_id": "INV1271_0_all_observed_fields",
            "criterion": "Dq_RAB[v_R]=0 for A, B, clocks, radial rulers, matter coframe, null cone, and boundary data",
            "result": "FAIL",
            "evidence": "A/B/clock/ruler rows fail unless q excludes them or auxiliary elimination runs first",
            "noncircular": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "INV1271_1_split_tuning",
            "criterion": "choose a split parameter a to hide all observed changes",
            "result": "FAIL",
            "evidence": "a can cancel one composite such as T/sqrt(S), but not A and B simultaneously when both are observed",
            "noncircular": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "INV1271_2_class_quotient",
            "criterion": "declare q_RAB=[A,B]/R_AB so Dq[v_R]=0",
            "result": "CIRCULAR",
            "evidence": "works by definition only; needs parent primitive proof before readout",
            "noncircular": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "INV1271_3_auxiliary_elimination",
            "criterion": "remove R_AB before observed readout by parent-owned compatibility equation",
            "result": "PASS_CONDITIONAL",
            "evidence": "1268 action candidate gives exact variational mechanism if parent necessity/source silence closes",
            "noncircular": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    aux_necessity = [
        {
            "target_id": "AUXN1271_0_radial_cell_principle",
            "needed_theorem": "the parent primitive action contains a radial observer-cell compatibility condition",
            "candidate_form": "C_R := ln(T^2 S) or R_AB-C_AB[q(Phi),theta,top]",
            "why_needed": "prevents R_AB from being an observed propagating/local strain",
            "current_status": "MOTIVATED_NOT_DERIVED",
            "source_hint": "08/09 phase-volume and Hamiltonian-cell work",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "target_id": "AUXN1271_1_multiplier_necessity",
            "needed_theorem": "Lambda_R is required by the parent variational principle, not appended after the fact",
            "candidate_form": "S_R = int mu_parent Lambda_R C_R",
            "why_needed": "turns closure into a real auxiliary compatibility equation",
            "current_status": "OPEN",
            "source_hint": "07 nonpropagating route plus 1268 compatibility action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "target_id": "AUXN1271_2_no_direct_R_source",
            "needed_theorem": "matter/boundary/readout do not source R_AB in E_R",
            "candidate_form": "delta_R(S_matter+B_R+S_eff)=0",
            "why_needed": "E_R then sets Lambda_R=0 instead of leaving finite residual force",
            "current_status": "OPEN",
            "source_hint": "AP1265_2/3/4 remaining gaps",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "target_id": "AUXN1271_3_no_kinetic_owner",
            "needed_theorem": "parent grammar has no D R_AB kinetic constructor",
            "candidate_form": "no G_vert(DR_AB,D R_AB) or h^{ij}D_iR_ABD_jR_AB",
            "why_needed": "prevents finite Z_R from re-entering",
            "current_status": "OPEN",
            "source_hint": "1269 AP1265_1 blocked theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "target_id": "AUXN1271_4_theorem_target",
            "needed_theorem": "parent-signed auxiliary compatibility theorem",
            "candidate_form": "AUXN1271_0..3 jointly imply eliminate R_AB,Lambda_R before readout; Z_R=J_R=B_R=0 on protected branch",
            "why_needed": "cleanest current route to derived local reciprocity/Newton-GR limit",
            "current_status": "EXACT_TARGET_NOT_CLOSED",
            "source_hint": "next target should attack parent necessity directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    route_decision = [
        {
            "route_id": "RD1271_0_quotient_route",
            "route": "non-circular field-by-field q_RAB/v_R map",
            "status": "REJECT_CURRENT_PROMOTION",
            "reason": "observed A/B/clock/ruler/matter variables do not remain invariant",
            "next_action": "only revisit if a parent primitive q_RAB readout is derived before metric variables are declared observed",
            "selected": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "RD1271_1_auxiliary_route",
            "route": "parent-signed auxiliary compatibility",
            "status": "SELECTED_NEXT_DERIVATION_TARGET",
            "reason": "removes R_AB before readout without hiding observable A/B changes",
            "next_action": "derive parent necessity of Lambda_R C_R from radial observer-cell/action principle",
            "selected": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "RD1271_2_finite_route",
            "route": "finite Z_R/J_R/B_R/tau residual row",
            "status": "FALLBACK_ONLY_NO_ROW",
            "reason": "validator accepts no raw/accepted source-backed rows",
            "next_action": "source real coefficients only if auxiliary parent necessity fails",
            "selected": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1271_0_qRAB_vertical",
            "claim": "field-by-field q_RAB/v_R map proves R_AB verticality",
            "status": "BLOCKED",
            "reason": "A/B/clock/ruler/matter readouts are not invariant under generic v_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1271_1_auxiliary_parent_necessity",
            "claim": "auxiliary compatibility block is parent-necessary",
            "status": "BLOCKED",
            "reason": "target is now precise but radial-cell variational principle is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1271_2_finite_row",
            "claim": "finite-ZR source row is accepted",
            "status": "BLOCKED",
            "reason": "no raw/accepted source-ready row exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1271_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "quotient, auxiliary, and finite-residual branches are not claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1271_0_field_map_result",
            "decision": "reject the q_RAB/v_R quotient route in its current form",
            "because": "there is no non-circular field-by-field invariance map for observed metric/coframe/matter data",
            "status": "QUOTIENT_ROUTE_BLOCKED",
            "next_action": "stop spending cycles on generic quotient borrowing for R_AB",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1271_1_best_route",
            "decision": "make auxiliary parent necessity the next target",
            "because": "the compatibility action can eliminate R_AB before readout if the parent action requires it",
            "status": "AUXILIARY_ROUTE_SELECTED",
            "next_action": "derive Lambda_R C_R from a radial observer-cell variational principle or demote to finite residual sourcing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1271_2_finite_discipline",
            "decision": "do not create finite rows without source-backed validator acceptance",
            "because": "templates are still placeholders and no coefficient source exists",
            "status": "VALIDATOR_DISCIPLINE_MAINTAINED",
            "next_action": "keep residual branch ready but unscored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1271_0_1272",
            "target_file": "1272-Y5-R10-RAB-auxiliary-parent-necessity-from-radial-cell-variational-principle-or-finite-source-row.md",
            "target_script": "scripts/Y5_R10_RAB_auxiliary_parent_necessity_from_radial_cell_variational_principle_or_finite_source_row.py",
            "task": "try to derive the Lambda_R C_R compatibility block from a radial observer-cell variational principle using the motion/time/space primitives; if that fails, keep theorem-zero blocked and only prepare source-backed finite residual acquisition",
            "success_condition": "parent necessity of Lambda_R ln(T^2S) is derived without closure smuggling, or finite residual sourcing remains the only live path with no accepted placeholder rows",
            "do_not": "do not define q_RAB to hide observed A/B after the fact, and do not claim local GR from the conditional auxiliary action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (FIELD_MAP_PATH, field_map),
        (INVARIANCE_TEST_PATH, invariance_test),
        (AUX_NECESSITY_PATH, aux_necessity),
        (ROUTE_DECISION_PATH, route_decision),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    field_map_has_failures = any("FAILS" in str(row["status"]) for row in field_map)
    all_invariance_not_passed = all(row["result"] != "PASS" for row in invariance_test if row["test_id"] != "INV1271_3_auxiliary_elimination")
    aux_target_ready = any(row["target_id"] == "AUXN1271_4_theorem_target" and row["current_status"] == "EXACT_TARGET_NOT_CLOSED" for row in aux_necessity)
    route_selected = any(row["route_id"] == "RD1271_1_auxiliary_route" and str(row["selected"]).lower() == "true" for row in route_decision)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    claim_gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_generated_rows = [
        *source_register,
        *field_map,
        *invariance_test,
        *aux_necessity,
        *route_decision,
        *validator_rescan,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1271_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1271_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1271_2_field_map_failures",
            "field-by-field q_RAB/v_R map records observed readout failures",
            field_map_has_failures,
            f"field_map_rows={len(field_map)}",
        ),
        validation_row(
            "VAL1271_3_no_noncircular_quotient",
            "non-circular quotient invariance does not pass",
            all_invariance_not_passed,
            "all direct quotient tests fail or are circular; auxiliary route is conditional",
        ),
        validation_row(
            "VAL1271_4_aux_target_ready",
            "auxiliary parent-necessity theorem target is explicit",
            aux_target_ready,
            "AUXN1271_4_theorem_target=EXACT_TARGET_NOT_CLOSED",
        ),
        validation_row(
            "VAL1271_5_route_selected",
            "auxiliary route is selected as next derivation target",
            route_selected,
            "RD1271_1_auxiliary_route selected=True",
        ),
        validation_row(
            "VAL1271_6_validator_rescan",
            "finite-ZR validator still rejects docs and has no live rows",
            docs_rejected and no_live_rows,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1271_7_claim_gates",
            "all claim gates remain blocked",
            claim_gates_blocked,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1271_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1271_9_next_target_1272",
            "next target routes to auxiliary parent necessity or finite source row",
            next_target[0]["next_id"] == "NEXT1271_0_1272",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1271_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1271_11_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1271_12_overall",
            "overall 1271 validation",
            overall_pass,
            "1271 rejects the non-circular field-by-field q_RAB/v_R route, selects auxiliary parent necessity as the next derivation target, and keeps finite-ZR rows locked behind the validator",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1271 rejects the remaining non-circular quotient route for `R_AB`. A field-by-field `q_RAB/v_R` map cannot keep the observed lapse `A=T^2`, radial metric `B=S`, clocks, radial rulers, matter geometry, and boundary data invariant while also changing `R_AB=ln(AB)`.

**Main progress:** this prevents a very tempting cheat: calling `R_AB` vertical after the local-GR target is known. The clean route is now narrowed to parent-signed auxiliary compatibility: derive why the parent action must contain `Lambda_R C_R`, then prove no matter, boundary, kinetic, or readout source survives.

**No-claim guard:** no `q_RAB` quotient theorem, `Z_R=0`, local-GR/Newton, R10, PPN, clock, orbital, or finite-`Z_R` row is claimed. The finite branch remains validator-locked.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Field-by-Field q_RAB/v_R Map
{markdown_table(field_map, ["map_id", "field_or_readout", "candidate_vR_action", "observed_in_q", "Dq_vR", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Observed Invariance Test
{markdown_table(invariance_test, ["test_id", "criterion", "result", "evidence", "noncircular", "valid_for_claim", "claim_allowed"])}

## Auxiliary Parent Necessity Target
{markdown_table(aux_necessity, ["target_id", "needed_theorem", "candidate_form", "why_needed", "current_status", "source_hint", "valid_for_claim", "claim_allowed"])}

## Route Decision After Field Map
{markdown_table(route_decision, ["route_id", "route", "status", "reason", "next_action", "selected", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
