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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2894-Y5-R2FR-fill-A-B-source-coefficients-or-beta-vector-source-row-under-AX1090.md"

SRC_2893_DOC = ROOT / "2893-Y5-R2FR-beta-source-normalized-second-order-kernel-or-finite-local-vector-under-AX1090.md"
SRC_2893_NEXT = RESIDUALS / "P8_Y5_R2FR_2893_NEXT_TARGET.csv"
SRC_2893_LAW = RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv"
SRC_2893_VECTOR = RESIDUALS / "P8_Y5_R2FR_2893_FINITE_BETA_VECTOR_ROW_NONCLAIM.csv"
SRC_527_DOC = ROOT / "527-Y5-fill-A-B-from-source-equation-or-demote-beta-to-residual.md"
SRC_528_DOC = ROOT / "528-Y5-EH-family-mass-parameter-route-or-beta-residual-fill.md"
SRC_529_DOC = ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md"
SRC_523_DOC = ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md"
SRC_439_DOC = ROOT / "439-EH-only-exterior-parent-premise-ladder.md"
SRC_440_DOC = ROOT / "440-metric-only-second-order-sector-reduction-attempt.md"
SRC_BETA_INPUT = RESIDUALS / "P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv"
SRC_GAUSS_CHAIN = RESIDUALS / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv"
SRC_SOURCE_SCORE = RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"
SRC_EH_GATES = RESIDUALS / "P8_Y5_EH_FAMILY_PREMISE_GATES.csv"
SRC_R11_STATUS = RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2894_SOURCE_REGISTER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2894_AB_SOURCE_EQUATION_EXTRACTION_CONTRACT.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_2894_CURRENT_CORPUS_AB_AUDIT.csv",
    "abrow": RESIDUALS / "P8_Y5_R2FR_2894_AB_COEFFICIENT_ROW_NONCLAIM.csv",
    "ehroute": RESIDUALS / "P8_Y5_R2FR_2894_EH_MASS_FAMILY_ROUTE_UPDATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2894_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2894_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2894_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2894_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2894_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2894_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": BETA_DOCS / "RAB_AB_SOURCE_EQUATION_EXTRACTION_CONTRACT_2894_NONCLAIM.csv",
    "abrow_copy": LOCAL_BOUNDS / "RAB_AB_COEFFICIENT_ROW_2894_NONCLAIM.csv",
    "ehroute_copy": BETA_DOCS / "RAB_EH_MASS_FAMILY_ROUTE_UPDATE_2894_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2894_R11_beta_or_EH_nohair_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2894_0_2893_doc", SRC_2893_DOC, "Status: `Y5_R2FR_2893;A_source and B_source", "2893 beta law and A/B handoff"),
        ("SRC2894_1_2893_next", SRC_2893_NEXT, "NEXT2893_0_2894;derive A_source and B_source", "explicit 2894 target"),
        ("SRC2894_2_2893_law", SRC_2893_LAW, "BSL2893_2_extract_beta;beta_eff = B_source/A_source^2", "current beta coefficient law"),
        ("SRC2894_3_2893_vector", SRC_2893_VECTOR, "FBR2893_0_delta_beta_source;MISSING_NUMERIC_A_SOURCE_AND_B_SOURCE", "current finite beta vector row"),
        ("SRC2894_4_527_doc", SRC_527_DOC, "AB527_3_parent_nonlinear_completion_route;D527_1_current_source_equation_missing", "older A/B source-equation attempt"),
        ("SRC2894_5_528_doc", SRC_528_DOC, "EH528_1_AB_square_from_mass_parameter;EHG528_3_measured_GM_mu_lock", "EH mass-family route"),
        ("SRC2894_6_529_doc", SRC_529_DOC, "SCEH529_1_EH_only_exterior;BL529_0_R11_operator", "source-calibrated EH proof stack"),
        ("SRC2894_7_523_doc", SRC_523_DOC, "CAL523_8_second_order_PPN_source_stability;SRC523_10_second_order_PPN_source", "measured-GM and second-order source stability"),
        ("SRC2894_8_439_doc", SRC_439_DOC, "P8_constant_source_normalization;P9_weak_field_PPN_completion", "EH-only premise ladder"),
        ("SRC2894_9_440_doc", SRC_440_DOC, "R11 coefficient data;operator_filter_written", "metric-only second-order reduction attempt"),
        ("SRC2894_10_beta_input", SRC_BETA_INPUT, "BETA526_0_source_AB;MISSING_A_SOURCE", "A/B coefficient fill template"),
        ("SRC2894_11_gauss_chain", SRC_GAUSS_CHAIN, "CAL523_8_second_order_PPN_source_stability;not_derived", "calibration chain machine row"),
        ("SRC2894_12_source_score", SRC_SOURCE_SCORE, "SRC523_10_second_order_PPN_source;unfilled", "source-normalization residual scorecard"),
        ("SRC2894_13_eh_gates", SRC_EH_GATES, "EHG528_0_EH_only_exterior;fail_for_current_claim", "EH family premise gates"),
        ("SRC2894_14_r11_status", SRC_R11_STATUS, "source_normalization_operator;template_only_retained_core_blocker", "R11 executable vector status"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ABX2894_0_frame",
            "observed second-order frame",
            "g_00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(c^-6), in the same observed metric/coframe used by matter, clocks, light, and slow orbits",
            "without this, A/B are gauge/readout labels rather than physical PPN coefficients",
            "MISSING_SAME_READOUT_THROUGH_O_U2",
        ),
        (
            "ABX2894_1_linear_projection",
            "linear source coefficient extraction",
            "E_00^(1)[A_source W]=S_H^(1)[Pi_M J_H]+R_1, so A_source is the normalized projection of S_H^(1)+R_1 onto W",
            "fixes the first-order active source amplitude in the measured-GM convention",
            "MISSING_PARENT_LINEAR_SOURCE_PROJECTION_OR_R1_ZERO",
        ),
        (
            "ABX2894_2_quadratic_projection",
            "quadratic source coefficient extraction",
            "E_00^(1)[-2 B_source W^2]+N_EH[A_source W,A_source W]=S_H^(2)+R_2",
            "extracts B_source only after the second-order parent equation and nonlinear metric operator are known",
            "MISSING_PARENT_SECOND_ORDER_SOURCE_EQUATION",
        ),
        (
            "ABX2894_3_square_condition",
            "beta-safe source square law",
            "B_source=A_source^2 iff the quadratic residual projection Delta_B_source:=B_source-A_source^2 vanishes in the same W/U convention",
            "then delta_beta_source=0 before other beta components are added",
            "MISSING_DELTA_B_SOURCE_ZERO_THEOREM",
        ),
        (
            "ABX2894_4_residual_exposure",
            "finite fallback",
            "delta_beta_source=(B_source/A_source^2)-1 and Delta_beta_total_abs=sum_abs(delta_beta_source,delta_beta_R11,delta_beta_q_loc,delta_beta_boundary_domain,delta_beta_readout,epsilon_SN)",
            "if A/B are not derived, beta stays as a scored residual vector, not a closure assumption",
            "MISSING_NUMERIC_AB_OR_THEOREM_ZERO",
        ),
        (
            "ABX2894_5_input_contract",
            "minimum accepted A/B source row",
            "row must include W convention, E_00^(1), E_00^(2), source support, A_source, B_source, units, source_path, readout map, no-cancellation flags",
            "prevents a fitted or reference GR row from becoming MTS evidence",
            "MISSING_EXECUTABLE_PARENT_SOURCE_ROW",
        ),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "target": target,
                "math_form": math_form,
                "meaning": meaning,
                "current_gap": gap,
                "contract_written": True,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for contract_id, target, math_form, meaning, gap in specs
    ]


def audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("ABA2894_0_source_equation", "explicit second-order parent source equation exists", "FAIL", "2893/527/528/529 expose the need but no E_00^(2) source equation with coefficients is present"),
        ("ABA2894_1_EH_family", "EH one-parameter mass family can supply B=A^2", "FAIL_CURRENT_CLAIM", "528/529 keep EH-only exterior, no-hair, and same readout unsigned"),
        ("ABA2894_2_measured_mu", "EH/source parameter equals observed orbital GM", "FAIL_CURRENT_CLAIM", "523 scorecard and Gauss/orbital chain are unfilled"),
        ("ABA2894_3_R11_silence", "non-EH/R11 quadratic operator sources are zero or bounded", "FAIL_CURRENT_CLAIM", "R11 executable vector remains template-only"),
        ("ABA2894_4_q_loc_boundary_readout", "q_loc, boundary/domain, and readout U2 channels are silent", "FAIL_CURRENT_CLAIM", "q_loc is provisional; boundary/domain/readout finite rows are missing"),
        ("ABA2894_5_AB_numeric", "A_source and B_source can be evaluated", "FAIL", "A_source=MISSING_A_SOURCE and B_source=MISSING_B_SOURCE in current machine rows"),
        ("ABA2894_6_beta_claim", "beta=1/local PPN can be claimed from A/B", "FAIL_CLOSED", "A/B extraction failed and full beta vector is not executable"),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "question": question,
                "result": result,
                "evidence": evidence,
                "claim_effect": "blocks_A_B_and_beta_claim",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for audit_id, question, result, evidence in specs
    ]


def abrow_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "row_id": "ABR2894_0_current_MTS_AB_source_row",
                "route_type": "finite_AB_source_coefficient_row",
                "W_convention": "parent weak-field source potential before measured-GM normalization",
                "A_source": "MISSING_A_SOURCE",
                "B_source": "MISSING_B_SOURCE",
                "beta_eff": "NOT_EVALUATED",
                "delta_beta_source": "NOT_EVALUATED",
                "Delta_B_source": "MISSING_B_SOURCE_MINUS_A_SOURCE_SQUARED",
                "units": "dimensionless",
                "source_equation_path": "MISSING_PARENT_E00_1_AND_E00_2_SOURCE_EQUATION",
                "readout_convention": "MISSING_SAME_OBSERVED_PPN_READOUT_THROUGH_O_U2",
                "no_cancellation_policy": "A/B source row cannot cancel against R11/q_loc/boundary/readout; total vector uses sum_abs",
                "current_status": "AB_SOURCE_ROW_BLOCKED_NONCLAIM",
                "missing_for_claim": "MISSING_A_SOURCE;MISSING_B_SOURCE;MISSING_SECOND_ORDER_SOURCE_EQUATION;MISSING_EH_OR_R11_SILENCE;MISSING_MEASURED_GM_CALIBRATION",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "row_id": "ABR2894_1_EH_reference_not_evidence",
                "route_type": "EH_mass_family_reference",
                "W_convention": "reference GR/EH target only",
                "A_source": "A_mu",
                "B_source": "A_mu^2",
                "beta_eff": "1",
                "delta_beta_source": "0",
                "Delta_B_source": "0",
                "units": "dimensionless",
                "source_equation_path": "REFERENCE_ONLY_REQUIRES_PARENT_EH_MASS_FAMILY_PROOF",
                "readout_convention": "reference isotropic PPN readout",
                "no_cancellation_policy": "not an MTS prediction row",
                "current_status": "REFERENCE_TARGET_ONLY_NOT_ACCEPTED_FOR_SCORING",
                "missing_for_claim": "MISSING_PARENT_EH_ONLY_EXTERIOR_AND_MEASURED_MU_LOCK",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def ehroute_rows() -> list[dict[str, Any]]:
    specs = [
        ("EHU2894_0_clean_route", "EH mass family remains the clean beta derivation", "one measured parameter mu controls both U and U^2, giving B=A^2", "CONDITIONAL_TARGET_RETAINED"),
        ("EHU2894_1_current_failure", "current branch does not yet satisfy the route", "EH-only exterior, measured mu, no quadratic leakage, and same readout are still open", "FAIL_CURRENT_CLAIM"),
        ("EHU2894_2_no_shortcut", "measured-GM absorption alone is not enough", "first-order A can be calibrated away but B/A^2 remains physical", "OVERCLAIM_BLOCKED"),
        ("EHU2894_3_best_next", "R11/EH no-hair is the highest-leverage next fork", "without EH-only or executable R11 beta vector, A/B source extraction cannot become a prediction", "NEXT_TARGET"),
    ]
    return [
        add_common(
            {
                "route_update_id": update_id,
                "route": route,
                "statement": statement,
                "current_status": status,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for update_id, route, statement, status in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2894_0_contract", "A/B extraction contract is written", "PASS_NONCLAIM", "linear and quadratic source-equation projections are now explicit"),
        ("GATE2894_1_source_equation", "parent E_00^(2) source equation exists with coefficients", "FAIL", "no current source path supplies it"),
        ("GATE2894_2_AB_values", "A_source and B_source are numeric or theorem-zero", "FAIL", "both remain missing"),
        ("GATE2894_3_square_law", "B_source=A_source^2 is derived", "FAIL", "requires EH mass family or parent nonlinear source square theorem"),
        ("GATE2894_4_reference_guard", "EH/GR reference row is not accepted as MTS evidence", "PASS_GUARD", "reference target remains nonclaim"),
        ("GATE2894_5_vector", "finite beta vector can be scored", "FAIL", "A/B source row and other components are missing/provisional"),
        ("GATE2894_6_local_gr", "local GR/Newton/PPN branch closes", "FAIL", "A/B, R11, measured-GM, q_loc, boundary, and readout gates remain open"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2894_0_AB_source_coefficient_extractor",
                "status": "REFUSED_MISSING_PARENT_SOURCE_EQUATION",
                "accepted_extraction_contracts": 1,
                "accepted_AB_rows": 0,
                "accepted_reference_rows": 0,
                "reason": "A/B extraction contract is formalized, but no parent E_00^(1)/E_00^(2) source equation, measured-GM lock, EH-only route, or executable R11 vector supplies A_source and B_source",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2894_0_contract", "KEEP_AB_EXTRACTION_CONTRACT", "it converts the beta source problem into a source-equation coefficient test", "use it as the required input shape for any future A/B claim"),
        ("DEC2894_1_current_AB", "DO_NOT_FILL_A_B_FROM_REFERENCE_ROWS", "GR/EH reference values are not current MTS evidence", "keep current A/B row missing"),
        ("DEC2894_2_beta", "KEEP_BETA_NONCLAIM", "delta_beta_source cannot be evaluated and the total beta vector cannot be scored", "no beta/local-GR promotion"),
        ("DEC2894_3_next", "MOVE_TO_R11_BETA_OR_EH_NOHAIR_FORK", "A/B extraction needs EH-only/no-hair or executable R11 beta vector before source coefficients become meaningful", "derive EH no-hair or fill first R11 beta row next"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "accepted_for_scoring": False,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2894_0_2895",
                "status": "selected_primary",
                "target_doc": "2895-Y5-R2FR-R11-beta-component-vector-or-EH-nohair-theorem-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_R11_beta_component_vector_or_EH_nohair_theorem_under_AX1090_2895.py",
                "mission": "try to derive EH/no-hair silence for beta-relevant R11 operator families; if it fails, stage the first executable R11 beta component rows with source paths and no-cancellation guards",
                "forbidden_shortcuts": "no EH import; no beta=1 from reference family; no source-normalization absorption; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2894_1_held_measured_GM",
                "status": "held_parallel_blocker",
                "target_doc": "2895b-Y5-R2FR-measured-mu-lock-reentry-after-R11.md",
                "target_script": "scripts/Y5_R2FR_measured_mu_lock_reentry_after_R11_2895b.py",
                "mission": "return to measured-GM/mu lock after the R11/EH operator status is no longer template-only",
                "forbidden_shortcuts": "do not use measured GM to erase beta source square law",
                "selected": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2894_0_contract_copy", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"], "beta-source copy of A/B extraction contract"),
        ("BR2894_1_abrow_copy", OUTPUTS["abrow"], BRANCH_OUTPUTS["abrow_copy"], "local-bounds copy of current nonclaim A/B coefficient rows"),
        ("BR2894_2_ehroute_copy", OUTPUTS["ehroute"], BRANCH_OUTPUTS["ehroute_copy"], "beta-source copy of EH mass-family route update"),
        ("BR2894_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    contract = rows_by_name["contract"]
    audit = rows_by_name["audit"]
    abrow = rows_by_name["abrow"]
    ehroute = rows_by_name["ehroute"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    current_ab = next(row for row in abrow if row["row_id"] == "ABR2894_0_current_MTS_AB_source_row")
    reference = next(row for row in abrow if row["row_id"] == "ABR2894_1_EH_reference_not_evidence")

    checks = [
        ("VAL2894_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2894_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2894_2_contract_written", any(row["contract_id"] == "ABX2894_2_quadratic_projection" for row in contract), "quadratic A/B extraction contract is written"),
        ("VAL2894_3_current_a_missing", current_ab["A_source"] == "MISSING_A_SOURCE" and current_ab["B_source"] == "MISSING_B_SOURCE", "current A/B coefficient row remains missing"),
        ("VAL2894_4_reference_guard", reference["current_status"] == "REFERENCE_TARGET_ONLY_NOT_ACCEPTED_FOR_SCORING" and reference["accepted_for_scoring"] is False, "EH reference row is not evidence"),
        ("VAL2894_5_audit_fail_closed", all("FAIL" in row["result"] for row in audit), "current corpus A/B audit fails closed"),
        ("VAL2894_6_eh_route_retained", any(row["current_status"] == "CONDITIONAL_TARGET_RETAINED" for row in ehroute), "EH mass-family route is retained as conditional target"),
        ("VAL2894_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2894_8_runner_refused", runner[0]["status"] == "REFUSED_MISSING_PARENT_SOURCE_EQUATION" and runner[0]["runner_ready"] is False, "runner refuses missing parent source equation"),
        ("VAL2894_9_next_target_2895", next_target[0]["next_id"] == "NEXT2894_0_2895" and next_target[0]["selected"] is True, "2895 R11/EH no-hair fork selected"),
        ("VAL2894_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2894_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2894_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2894_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2894_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2894_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2894_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2894_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2894 wrote the A/B source-equation extraction contract, refused to fill A_source or B_source from EH reference rows, kept beta nonclaim, and selected the R11 beta/EH no-hair fork for 2895.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2894 - Y5 R2FR Fill A/B Source Coefficients Or Beta Vector Source Row Under AX1090

Status: `Y5_R2FR_2894_AB_extraction_contract_written_current_AB_missing_R11_EH_nohair_2895_next`

## Private Verdict

2894 does the A/B hunt properly.

The result is not a numeric `A_source` or `B_source`; the current corpus still does not contain the parent second-order source equation needed to extract them. The useful advance is the exact contract:

`E_00^(1)[A_source W]=S_H^(1)+R_1` fixes the linear source amplitude, while `E_00^(1)[-2 B_source W^2]+N_EH[A_source W,A_source W]=S_H^(2)+R_2` fixes the quadratic coefficient.

The beta-safe condition is now `B_source=A_source^2`, equivalently `Delta_B_source:=B_source-A_source^2=0`, in the same observed PPN readout and measured-GM convention.

Current MTS cannot claim that yet. EH reference rows show the target but are not evidence. The live route is to close EH/no-hair or provide an executable R11 beta vector; otherwise `delta_beta_source` remains a nonclaim residual row.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## A/B Source Equation Extraction Contract

{md_table(rows_by_name["contract"], ["contract_id", "target", "math_form", "meaning", "current_gap", "valid_for_claim"])}

## Current Corpus A/B Audit

{md_table(rows_by_name["audit"], ["audit_id", "question", "result", "evidence", "claim_effect", "valid_for_claim"])}

## A/B Coefficient Row

{md_table(rows_by_name["abrow"], ["row_id", "route_type", "A_source", "B_source", "beta_eff", "delta_beta_source", "current_status", "valid_for_claim"])}

## EH Mass Family Route Update

{md_table(rows_by_name["ehroute"], ["route_update_id", "route", "statement", "current_status", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_extraction_contracts", "accepted_AB_rows", "accepted_reference_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "contract": contract_rows(),
        "audit": audit_rows(),
        "abrow": abrow_rows(),
        "ehroute": ehroute_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2894_OVERALL")
    print(f"VAL2894_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
