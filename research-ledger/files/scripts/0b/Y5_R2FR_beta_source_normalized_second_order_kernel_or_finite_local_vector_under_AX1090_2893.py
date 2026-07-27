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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2893-Y5-R2FR-beta-source-normalized-second-order-kernel-or-finite-local-vector-under-AX1090.md"

SRC_2892_DOC = ROOT / "2892-Y5-R2FR-parent-action-source-neutrality-generator-or-closure-demotion-under-AX1090.md"
SRC_2892_NEXT = RESIDUALS / "P8_Y5_R2FR_2892_NEXT_TARGET.csv"
SRC_DELTA_BETA = RESIDUALS / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv"
SRC_1885_DOC = ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md"
SRC_1885_VECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_1885_BETA_RESIDUAL_VECTOR_CONTRACT.csv"
SRC_1886_NO_SLOT = RESIDUALS / "P8_Y5_PARENT_QLOC_1886_NO_SOURCE_ONLY_SLOT_PROOF_AUDIT.csv"
SRC_1585_LEDGER = RESIDUALS / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv"
SRC_BETA_ENVELOPE = RESIDUALS / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv"
SRC_BETA_ROUTE = RESIDUALS / "P8_Y5_BETA_QLOC_ROUTE_UPDATE.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2893_SOURCE_REGISTER.csv",
    "law": RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv",
    "zero": RESIDUALS / "P8_Y5_R2FR_2893_BETA_ZERO_THEOREM_ATTEMPT.csv",
    "finite": RESIDUALS / "P8_Y5_R2FR_2893_FINITE_BETA_VECTOR_ROW_NONCLAIM.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_2893_BETA_ENVELOPE_UPDATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2893_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2893_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2893_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2893_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2893_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2893_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "law_copy": BETA_DOCS / "RAB_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW_2893_NONCLAIM.csv",
    "finite_copy": LOCAL_BOUNDS / "RAB_FINITE_BETA_VECTOR_ROW_2893_NONCLAIM.csv",
    "source_slot_copy": SOURCE_WEIGHT / "RAB_BETA_SOURCE_NO_SOURCE_SLOT_UPDATE_2893_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2893_fill_A_B_source_or_beta_vector_NEXT.csv",
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
        ("SRC2893_0_2892_doc", SRC_2892_DOC, "Status: `Y5_R2FR_2892;NEXT2892_0_2893", "2892 handoff and selected beta target"),
        ("SRC2893_1_2892_next", SRC_2892_NEXT, "NEXT2892_0_2893;derive the beta/source-normalized", "explicit 2893 target and shortcut bans"),
        ("SRC2893_2_delta_beta_law", SRC_DELTA_BETA, "DB525_2_extract_beta;beta_eff = B/A^2;DB525_3_beta_residual", "source-normalized beta coefficient derivation"),
        ("SRC2893_3_1885_doc", SRC_1885_DOC, "BETA_GATE_NOT_DERIVED_CURRENT_CORPUS;B_source/A_source^2 - 1", "beta gate and residual vector prior checkpoint"),
        ("SRC2893_4_1885_vector", SRC_1885_VECTOR, "BRC1885_0_delta_beta_source;B_source/A_source^2 - 1", "component contract for finite beta vector"),
        ("SRC2893_5_1886_no_slot", SRC_1886_NO_SLOT, "NSS1886_7_verdict;NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "no-source-only slot obstruction"),
        ("SRC2893_6_1585_beta_ledger", SRC_1585_LEDGER, "BRL1585_0_delta_beta_source;MISSING_A_B_SOURCE_EQUATION_OR_EH_MASS_FAMILY_OWNER", "missing A/B source equation and no-cancellation ledger"),
        ("SRC2893_7_beta_envelope", SRC_BETA_ENVELOPE, "ENV531_3_q_loc;provisional_same_normalization_only_not_claimable", "provisional q_loc beta budget guard"),
        ("SRC2893_8_beta_route", SRC_BETA_ROUTE, "A_source_B_source_required_after_525;still_blocked_current_beta_inputs_missing", "existing route update requiring A/B coefficients"),
        ("SRC2893_9_local_beta_bound", SRC_LOCAL_BOUNDS, "Will_2014_PPN_beta_table;7.8e-05", "external beta comparator anchor only"),
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


def coefficient_law_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BSL2893_0_parent_potential",
            "Define W as the parent weak-field source potential before measured-GM calibration.",
            "g_00=-1+2 A_source W/c^2 - 2 B_source W^2/c^4 + O(c^-6)",
            "A_source is the first-order active source amplitude and B_source is the quadratic response.",
            "definition_only",
        ),
        (
            "BSL2893_1_measured_U",
            "The observed Newtonian potential is the first-order calibrated potential.",
            "U := A_source W, with A_source != 0 on the local branch",
            "W=U/A_source; first-order GM absorption is a convention, not a second-order pass.",
            "definition_only",
        ),
        (
            "BSL2893_2_extract_beta",
            "Substitute W=U/A_source and compare with PPN beta grammar.",
            "g_00=-1+2U/c^2 - 2(B_source/A_source^2)U^2/c^4 + O(c^-6)",
            "beta_eff = B_source/A_source^2",
            "derived_kinematic_law",
        ),
        (
            "BSL2893_3_source_residual",
            "The source-normalized beta residual is the failure of the quadratic response to square the first-order source amplitude.",
            "delta_beta_source = B_source/A_source^2 - 1",
            "beta_source zero iff B_source=A_source^2 in the same observed U convention.",
            "derived_kinematic_law_coefficients_unfilled",
        ),
        (
            "BSL2893_4_linear_guard",
            "Linear leakage cannot be hidden by redefining G unless the second-order coefficient tracks the square.",
            "A_source=1+a1 eps, B_source=1+b1 eps => beta_eff-1=(b1-2a1)eps+O(eps^2)",
            "a measured-GM denominator only removes a1; it does not remove b1-2a1.",
            "derived_guard",
        ),
        (
            "BSL2893_5_no_smuggling",
            "A GR/EH exterior may set B_source=A_source^2, but only after the parent action owns that one-parameter source family.",
            "EH import => beta_eff=1 is a closure/control lane, not a current MTS derivation.",
            "no beta=1 from gamma, no q_R_hat closure, no Schwarzschild import.",
            "claim_blocker",
        ),
    ]
    return [
        add_common(
            {
                "law_id": law_id,
                "statement": statement,
                "math_form": math_form,
                "result": result,
                "current_status": status,
                "A_source_status": "MISSING_PARENT_COEFFICIENT_OR_THEOREM_ZERO",
                "B_source_status": "MISSING_PARENT_COEFFICIENT_OR_THEOREM_ZERO",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for law_id, statement, math_form, result, status in specs
    ]


def zero_theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BZ2893_0_source_square_law",
            "B_source=A_source^2 in the measured U convention",
            "would set delta_beta_source=0",
            "UNSIGNED",
            "no source-normalized second-order parent field equation gives A_source and B_source",
        ),
        (
            "BZ2893_1_EH_operator_owner",
            "same parent action owns an EH-like second-order local operator with no retained R11/non-EH U2 source",
            "would remove delta_beta_operator",
            "UNSIGNED",
            "R11 operator coefficient vector or EH no-hair owner is missing",
        ),
        (
            "BZ2893_2_conservation_bianchi",
            "projected Ward/Bianchi identity carries the same Hilbert source through O(U2)",
            "would block source-current drift and denominator hair",
            "UNSIGNED",
            "projected conservation and measured-GM scorecard remain missing",
        ),
        (
            "BZ2893_3_no_source_only_slot",
            "ordinary matter grammar forbids w_A(X)S_A and source-only kappa_A(X)T_A slots",
            "would remove hidden beta/source weight leakage",
            "UNSIGNED",
            "1886 leaves this as a contract, not a parent theorem",
        ),
        (
            "BZ2893_4_q_loc_boundary",
            "q_loc U2 projection and boundary/domain quadratic stresses vanish or are source-backed finite rows",
            "would remove delta_beta_q_loc and delta_beta_boundary_domain",
            "UNSIGNED",
            "q_loc value is provisional same-normalization only; boundary/domain zero is absent",
        ),
        (
            "BZ2893_5_readout",
            "observed coframe/isotropic PPN readout is the same through O(U2)",
            "would remove delta_beta_readout",
            "UNSIGNED",
            "terminal public coframe/readout theorem is only first-order/conditional in the current branch",
        ),
        (
            "BZ2893_6_verdict",
            "parent beta zero theorem",
            "beta_eff=1 and Delta_beta_total_abs=0",
            "NOT_DERIVED_CURRENT_CORPUS",
            "the A/B source square law and the operator/source/readout silence package are not parent-signed",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for theorem_id, clause, consequence, status, blocker in specs:
        rows.append(
            add_common(
                {
                    "theorem_id": theorem_id,
                    "required_clause": clause,
                    "would_imply": consequence,
                    "current_status": status,
                    "current_blocker": blocker,
                    "condition_satisfied": False,
                    "parent_signed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def finite_vector_rows() -> list[dict[str, Any]]:
    specs = [
        ("FBR2893_0_delta_beta_source", "delta_beta_source", "B_source/A_source^2 - 1", "MISSING_NUMERIC_A_SOURCE_AND_B_SOURCE_OR_PARENT_SQUARE_THEOREM", "MISSING", "dimensionless", "must derive/source A_source and B_source"),
        ("FBR2893_1_delta_beta_operator", "delta_beta_operator", "second-order non-EH/R11 operator contribution", "MISSING_R11_COEFFICIENT_VECTOR_OR_EH_NOHAIR", "MISSING", "dimensionless", "cannot be inferred from first-order gamma"),
        ("FBR2893_2_delta_beta_q_loc", "delta_beta_q_loc", "physical U2 projection of P_loc(nabla Gamma_eff-div Khat)", "MISSING_U2_NORMALIZATION_AND_ALPHA3_PROJECTION_GUARD", "7.432631961576971e-06_PROVISIONAL_SAME_NORMALIZATION_ONLY", "dimensionless", "not source-backed; do not include in scored beta row yet"),
        ("FBR2893_3_delta_beta_boundary_domain", "delta_beta_boundary_domain", "boundary/domain/projector quadratic stress beta projection", "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP", "MISSING", "dimensionless", "needs no-flux/no-hair theorem or finite coefficient"),
        ("FBR2893_4_delta_beta_readout", "delta_beta_readout", "second-order source metric to observed isotropic PPN readout mismatch", "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2", "MISSING", "dimensionless", "terminal coframe/readout must be same convention as U"),
        ("FBR2893_5_epsilon_SN", "epsilon_SN", "(mu_obs-G_eff M_H)/(G_eff M_H)", "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD", "MISSING", "dimensionless", "measured-GM denominator cannot absorb relative/source weights"),
        ("FBR2893_6_Delta_beta_total_abs", "Delta_beta_total_abs", "sum_abs(all active finite beta components)", "ALL_COMPONENTS_NUMERIC_OR_THEOREM_ZERO_WITH_SOURCE_PATHS", "NOT_EVALUATED", "dimensionless", "no cancellation credit; compare only after all rows are real"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, formula, missing, current_value, units, next_action in specs:
        rows.append(
            add_common(
                {
                    "row_id": row_id,
                    "symbol": symbol,
                    "formula_or_map": formula,
                    "current_value": current_value,
                    "missing_for_claim": missing,
                    "units": units,
                    "beta_bound_abs": "7.8e-05",
                    "no_cancellation_policy": "sum absolute active components; cancellation gets zero credit unless parent identity proves it",
                    "source_path": "MISSING_SOURCE_BACKED_THEOREM_OR_NUMERIC_COMPONENT_ROW",
                    "next_action": next_action,
                    "numeric_source_present": False,
                    "parent_signed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def envelope_rows() -> list[dict[str, Any]]:
    specs = [
        ("BEU2893_0_law", "source-normalized beta law", "beta_eff=B_source/A_source^2", "DERIVED_KINEMATIC_LAW", "not a prediction until A_source and B_source are parent-signed or sourced"),
        ("BEU2893_1_zero_condition", "source square condition", "B_source=A_source^2", "EXACT_TARGET_UNSIGNED", "this is the cleanest beta theorem target"),
        ("BEU2893_2_vector", "finite beta vector", "Delta_beta_total_abs=sum_abs(delta_beta_source,delta_beta_operator,delta_beta_q_loc,delta_beta_boundary_domain,delta_beta_readout,epsilon_SN)", "STAGED_NONCLAIM", "components missing or provisional"),
        ("BEU2893_3_q_loc_guard", "q_loc beta budget", "abs(delta_beta_q_loc)_provisional=7.432631961576971e-06", "PROVISIONAL_NOT_SCORABLE", "same-normalization and alpha3 projection guards unresolved"),
        ("BEU2893_4_bound", "local beta comparator", "abs(beta-1) <= 7.8e-05", "BOUND_AVAILABLE_PREDICTION_MISSING", "bound is a judge, not an MTS prediction"),
        ("BEU2893_5_local_gr", "local GR/Newton reduction", "gamma plus q_R_hat work is not enough without beta/source/readout/vector closure", "STILL_BLOCKED", "go after A_source/B_source next"),
    ]
    return [
        add_common(
            {
                "update_id": update_id,
                "object": obj,
                "formula_or_fact": formula,
                "current_status": status,
                "meaning": meaning,
                "beta_bound_abs": "7.8e-05",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for update_id, obj, formula, status, meaning in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2893_0_law", "source-normalized beta coefficient law is written", "PASS_NONCLAIM", "beta_eff=B_source/A_source^2 and delta_beta_source=B_source/A_source^2-1"),
        ("GATE2893_1_no_gamma_shortcut", "beta is not inferred from gamma/q_R_hat", "PASS_GUARD", "first-order reciprocal profile cannot determine U2 coefficient"),
        ("GATE2893_2_A_B_source", "A_source and B_source are parent-derived or source-backed", "FAIL", "no parent source equation or numeric row supplies them"),
        ("GATE2893_3_beta_zero", "B_source=A_source^2 plus all U2 residual channels vanish", "FAIL", "the square law and silence package are unsigned"),
        ("GATE2893_4_finite_vector", "all beta residual components are numeric/source-backed or theorem-zero", "FAIL", "source/operator/boundary/readout/epsilon_SN are missing and q_loc is provisional"),
        ("GATE2893_5_bound_score", "Delta_beta_total_abs can be compared to 7.8e-05", "FAIL", "vector is not executable; comparator only is not a prediction"),
        ("GATE2893_6_local_gr", "local GR/Newton PPN branch closes", "FAIL", "beta/source/readout/conservation gates remain open"),
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
                "runner_id": "RUN2893_0_beta_source_normalized_kernel_runner",
                "status": "REFUSED_CLAIM_RUN_LAW_ONLY",
                "accepted_formula_laws": 1,
                "accepted_parent_zero_theorems": 0,
                "accepted_finite_rows": 0,
                "beta_bound_abs": "7.8e-05",
                "reason": "coefficient law is derived, but A_source/B_source, operator, q_loc U2, boundary, readout and epsilon_SN components are not all parent-signed or source-backed",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2893_0_law", "KEEP_BETA_SOURCE_NORMALIZATION_LAW", "it is exact and blocks the fake GM-absorption beta win", "use beta_eff=B_source/A_source^2 as the second-order coupling target"),
        ("DEC2893_1_zero", "DO_NOT_CLAIM_BETA_ZERO", "B_source=A_source^2 is not parent-signed and residual channels remain live", "keep beta=1 as conditional target only"),
        ("DEC2893_2_q_loc", "KEEP_QLOC_PROVISIONAL_ONLY", "the q_loc number is interesting but not same-arena/source/readout validated and has alpha3 warning", "do not insert it into the scored vector"),
        ("DEC2893_3_next", "MOVE_TO_FILL_A_B_SOURCE_COEFFICIENTS", "delta_beta_source is now the front-door missing coefficient, not vague coupling talk", "derive/fill A_source and B_source from parent source-normalized equation next"),
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
                "next_id": "NEXT2893_0_2894",
                "status": "selected_primary",
                "target_doc": "2894-Y5-R2FR-fill-A-B-source-coefficients-or-beta-vector-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_fill_A_B_source_coefficients_or_beta_vector_source_row_under_AX1090_2894.py",
                "mission": "derive A_source and B_source from the parent source-normalized second-order field equation; if that fails, stage strict finite A/B coefficient rows and keep beta nonclaim",
                "forbidden_shortcuts": "no measured-GM absorption as beta proof; no beta=1 from gamma; no Schwarzschild import; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2893_1_held_q_loc_u2",
                "status": "held_until_A_B_or_alpha3_context",
                "target_doc": "2894b-Y5-R2FR-q-loc-U2-normalization-alpha3-guard.md",
                "target_script": "scripts/Y5_R2FR_q_loc_U2_normalization_alpha3_guard_2894b.py",
                "mission": "return to q_loc U2 only after A/B source convention is fixed or if alpha3 projection becomes the dominant blocker",
                "forbidden_shortcuts": "do not score provisional q_loc number before same-arena U2/readout/projection proof",
                "selected": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2893_0_law_copy", OUTPUTS["law"], BRANCH_OUTPUTS["law_copy"], "beta-source copy of source-normalized coefficient law"),
        ("BR2893_1_finite_copy", OUTPUTS["finite"], BRANCH_OUTPUTS["finite_copy"], "local-bounds copy of finite beta vector row contract"),
        ("BR2893_2_source_slot_copy", OUTPUTS["zero"], BRANCH_OUTPUTS["source_slot_copy"], "source-weight copy of beta zero theorem obstruction/no-source-slot update"),
        ("BR2893_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
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
        "condition_satisfied",
        "numeric_source_present",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    law = rows_by_name["law"]
    zero = rows_by_name["zero"]
    finite = rows_by_name["finite"]
    envelope = rows_by_name["envelope"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    finite_symbols = {row["symbol"] for row in finite}
    required_symbols = {
        "delta_beta_source",
        "delta_beta_operator",
        "delta_beta_q_loc",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "epsilon_SN",
        "Delta_beta_total_abs",
    }
    source_row = next(row for row in finite if row["symbol"] == "delta_beta_source")
    qloc_row = next(row for row in finite if row["symbol"] == "delta_beta_q_loc")
    total_row = next(row for row in finite if row["symbol"] == "Delta_beta_total_abs")

    checks = [
        ("VAL2893_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2893_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2893_2_beta_law", any(row["result"] == "beta_eff = B_source/A_source^2" for row in law), "source-normalized beta coefficient law is written"),
        ("VAL2893_3_delta_beta_source_law", source_row["formula_or_map"] == "B_source/A_source^2 - 1", "delta_beta_source law is the active source coefficient target"),
        ("VAL2893_4_zero_refused", zero[-1]["current_status"] == "NOT_DERIVED_CURRENT_CORPUS" and all(row["condition_satisfied"] is False for row in zero), "parent beta-zero theorem is not adopted"),
        ("VAL2893_5_finite_vector_complete", required_symbols.issubset(finite_symbols), "finite beta vector contains all active components"),
        ("VAL2893_6_finite_vector_missing", "MISSING" in source_row["missing_for_claim"] and total_row["current_value"] == "NOT_EVALUATED", "finite beta vector remains blocked rather than fabricated"),
        ("VAL2893_7_qloc_provisional_guard", "PROVISIONAL" in qloc_row["current_value"] and qloc_row["finite_value_present"] is False, "q_loc provisional number is not promoted"),
        ("VAL2893_8_no_cancellation", all("sum absolute" in row["no_cancellation_policy"] for row in finite), "no-cancellation policy is carried by every finite component row"),
        ("VAL2893_9_beta_bound_anchor", any(row["object"] == "local beta comparator" and row["beta_bound_abs"] == "7.8e-05" for row in envelope), "local beta bound is comparator-only"),
        ("VAL2893_10_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2893_11_runner_refused", runner[0]["status"] == "REFUSED_CLAIM_RUN_LAW_ONLY" and runner[0]["runner_ready"] is False, "runner refuses claim run"),
        ("VAL2893_12_next_target_2894", next_target[0]["next_id"] == "NEXT2893_0_2894" and next_target[0]["selected"] is True, "2894 A/B source coefficient target selected"),
        ("VAL2893_13_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2893_14_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2893_15_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2893_16_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2893_17_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2893_18_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2893_19_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2893_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2893 derived the source-normalized beta coefficient law beta_eff=B_source/A_source^2, refused beta=1 without parent A/B square-law ownership, staged a strict finite beta vector, and selected A_source/B_source coefficient derivation for 2894.",
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
    text = f"""# 2893 - Y5 R2FR Beta Source-Normalized Second-Order Kernel Or Finite Local Vector Under AX1090

Status: `Y5_R2FR_2893_beta_source_law_derived_A_B_unfilled_finite_vector_staged_2894_next`

## Private Verdict

2893 makes the second-order coupling problem sharper.

The usable derivation is not `beta=1`. It is the source-normalized coefficient law:

`g_00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(c^-6)`, with observed `U=A_source W`, gives `beta_eff=B_source/A_source^2`.

Therefore `delta_beta_source=B_source/A_source^2-1`. Measured-GM calibration can absorb the first-order amplitude, but it cannot fake the second-order square law. The clean local-GR beta route is now exact: derive `B_source=A_source^2` in the same parent source/readout convention, and also kill the operator, `q_loc`, boundary, readout, and source-normalization residual channels.

Current MTS does not yet own that package. So 2893 refuses beta/local-GR claims, stages the finite no-cancellation beta vector, keeps the provisional `q_loc` budget nonclaim, and moves the next attack to deriving or sourcing `A_source` and `B_source`.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Beta Source-Normalized Coefficient Law

{md_table(rows_by_name["law"], ["law_id", "statement", "math_form", "result", "current_status", "valid_for_claim"])}

## Beta Zero Theorem Attempt

{md_table(rows_by_name["zero"], ["theorem_id", "required_clause", "would_imply", "current_status", "current_blocker", "condition_satisfied", "valid_for_claim"])}

## Finite Beta Vector Row

{md_table(rows_by_name["finite"], ["row_id", "symbol", "formula_or_map", "current_value", "missing_for_claim", "beta_bound_abs", "valid_for_claim"])}

## Beta Envelope Update

{md_table(rows_by_name["envelope"], ["update_id", "object", "formula_or_fact", "current_status", "meaning", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_formula_laws", "accepted_parent_zero_theorems", "accepted_finite_rows", "reason", "runner_ready", "valid_for_claim"])}

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
        "law": coefficient_law_rows(),
        "zero": zero_theorem_rows(),
        "finite": finite_vector_rows(),
        "envelope": envelope_rows(),
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
    overall = next(row for row in validation if row["validation_id"] == "VAL2893_OVERALL")
    print(f"VAL2893_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
