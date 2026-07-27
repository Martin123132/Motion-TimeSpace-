from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2179"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2179-Y5-R2FR-parent-v-field-action-normalization-and-beta-quadratic-zero-or-finite-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2179_SOURCE_REGISTER.csv",
    "action_audit": OUT / "P8_Y5_PARENT_QLOC_2179_V_ACTION_COEFFICIENT_AUDIT.csv",
    "normalization_law": OUT / "P8_Y5_PARENT_QLOC_2179_SOURCE_NORMALIZATION_LAW.csv",
    "beta_audit": OUT / "P8_Y5_PARENT_QLOC_2179_BETA_KAPPA_AUDIT.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2179_DELTA_V_KAPPA_FINITE_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2179_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2179_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2179_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2179_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2179_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2179_DELTA_V_KAPPA_FINITE_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2179_V_ACTION_COEFFICIENT_AUDIT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "V_ACTION_NORMALIZATION_KAPPA_2179_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2179_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2179-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2179*",
        "*P8_Y5_BRR545_2179*",
        "*Y5_R2FR_parent_v_field_action_normalization_and_beta_quadratic_zero_or_finite_row_2179*",
        "*JR2179*",
        "*V_ACTION_NORMALIZATION_KAPPA_2179*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2178_handoff",
            ROOT / "2178-Y5-R2FR-constraint-before-readout-ordering-and-v-PPN-source-convention-or-readout-lock.md",
            ["NEXT2178_0_2179", "PARENT_V_ACTION_NORMALIZATION_AND_BETA_ZERO_NEXT"],
            "2178 selects parent v action normalization and beta-zero as the next gate.",
        ),
        (
            "2178_validation",
            OUT / "P8_Y5_BRR545_2178_VALIDATION.csv",
            ["VAL2178_OVERALL", "PASS"],
            "2178 validation passed before 2179 continues the chain.",
        ),
        (
            "2177_v_readout",
            ROOT / "2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md",
            ["EXACT_V_ONLY_RECONSTRUCTION_AFTER_CONSTRAINT", "T=exp(v/2)"],
            "2177 supplies the constrained v-only readout used by 2179.",
        ),
        (
            "1885_beta_guard",
            ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
            ["NO_GAMMA_ONLY_PROMOTION", "BETA_GATE_NOT_DERIVED_CURRENT_CORPUS"],
            "1885 blocks gamma-only beta promotion and keeps the beta vector live.",
        ),
        (
            "1886_source_slot",
            ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
            ["NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"],
            "1886 blocks hidden source-weight absorption into measured G.",
        ),
        (
            "1012_source_norm",
            ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            ["Y5 source-normalization remains retained residual", "Newton_Poisson_orbit"],
            "1012 supplies the older measured-GM/source-normalization obstruction family.",
        ),
        (
            "observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["T^2 = 1 - 2U/c^2", "beta - 1 = 0"],
            "observer contract states the Newton and beta requirements.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def action_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VAC2179_0_general_action",
            "weak-field v action template",
            "L_v=-K_v (grad v)^2 - C_v rho c^2 v plus possible nonlinear/source/boundary corrections.",
            "EXACT_TEMPLATE",
            "K_v and C_v are the two parent coefficients that set Newton normalization.",
        ),
        (
            "VAC2179_1_target_coefficients",
            "2178 target coefficients",
            "The Newton contract is K_v=c^4/(32piG) and C_v=1/2.",
            "TARGET_FROM_2178",
            "these values give laplacian(v)=8piG rho/c^2.",
        ),
        (
            "VAC2179_2_parent_origin_test",
            "parent origin of K_v and C_v",
            "The current corpus derives K_v and C_v from MTS parent primitives rather than from GR import or measured-G fitting.",
            "MISSING_PARENT_KV_CV_ORIGIN",
            "source normalization remains a live residual.",
        ),
        (
            "VAC2179_3_no_absorption_rule",
            "no measured-G absorption",
            "A mismatch in C_v/K_v cannot be absorbed into measured GM unless it is a universal derivative-silent common mode with species/range/time/frame guards.",
            "NO_ABSORPTION_GUARD_RETAINED",
            "1886 and 1012 keep calibration shortcuts blocked.",
        ),
        (
            "VAC2179_4_pure_branch",
            "pure quadratic/linear source branch",
            "If only -K_v(grad v)^2 and -C_v rho c^2 v survive, and K_v,C_v hit the target ratio, then delta_v_source_norm=0.",
            "PURE_QUADRATIC_LINEAR_SOURCE_CONDITIONAL",
            "this is a clean theorem shape but not parent-signed.",
        ),
        (
            "VAC2179_5_current_verdict",
            "current action status",
            "No parent-signed MTS source currently fixes K_v, C_v, no-source-only slots, boundary terms and conservation together.",
            "NOT_DERIVED_CURRENT_CORPUS",
            "do not claim Newton or local GR.",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for audit_id, object_name, statement, status, implication in specs
    ]


def normalization_law_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SNL2179_0_variation",
            "general variation",
            "Varying L_v=-K_v(grad v)^2-C_v rho c^2 v gives 2K_v laplacian(v)-C_v rho c^2=0.",
            "EXACT_EULER_LAGRANGE",
            "all source-normalization debt is now in the ratio C_v/K_v.",
        ),
        (
            "SNL2179_1_poisson_ratio",
            "Poisson coefficient",
            "laplacian(v)=(C_v c^2/(2K_v)) rho.",
            "EXACT_COEFFICIENT_LAW",
            "compare directly against 8piG rho/c^2.",
        ),
        (
            "SNL2179_2_delta_definition",
            "delta_v_source_norm",
            "delta_v_source_norm=(C_v c^4/(16piG K_v))-1.",
            "EXACT_NORMALIZATION_RESIDUAL",
            "Newton requires delta_v_source_norm=0.",
        ),
        (
            "SNL2179_3_target_check",
            "2178 coefficient check",
            "K_v=c^4/(32piG) and C_v=1/2 give delta_v_source_norm=0.",
            "PASS_CONDITIONAL_TARGET",
            "the algebra is consistent.",
        ),
        (
            "SNL2179_4_parent_status",
            "parent theorem status",
            "K_v and C_v have no parent-signed source path in the current corpus.",
            "MISSING_PARENT_SOURCE_PATH",
            "delta_v_source_norm remains finite-or-zero theorem debt.",
        ),
    ]
    return [
        base_row(
            law_id=law_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for law_id, object_name, statement, status, implication in specs
    ]


def beta_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BKA2179_0_kappa_definition",
            "quadratic v tail",
            "v=-2x+kappa_v x^2+O(x^3), with x=U/c^2.",
            "EXACT_PARAMETERIZATION_FROM_2178",
            "kappa_v is the local beta drift variable.",
        ),
        (
            "BKA2179_1_beta_law",
            "beta relation",
            "beta=1+kappa_v/2.",
            "EXACT_BETA_LAW_FROM_2178",
            "local beta requires kappa_v=0 or a sourced finite prediction.",
        ),
        (
            "BKA2179_2_pure_linear_branch",
            "pure exterior Poisson branch",
            "If the exterior v equation is strictly laplacian(v)=0 outside the source with v(infinity)=0 and mass monopole fixed, then v=-2GM/(c^2 r) and kappa_v=0.",
            "EXACT_CONDITIONAL_KAPPA_ZERO",
            "pure linear exterior dynamics would pass beta shape.",
        ),
        (
            "BKA2179_3_cubic_kinetic_test",
            "representative nonlinear kinetic term",
            "For L=-K_v(1+eta_v v)(grad v)^2 outside matter, the O(x^2) exterior equation gives kappa_v=-eta_v.",
            "EXACT_REPRESENTATIVE_NONLINEAR_DRIFT",
            "any parent cubic kinetic coefficient maps directly into beta unless zero/gauge/sourced.",
        ),
        (
            "BKA2179_4_source_quadratic_slot",
            "quadratic matter/source slot",
            "A rho c^2 v^2 source term or beta_w source weight can alter the observed mass normalization and beta tail unless the no-source-only slot theorem closes.",
            "MISSING_SOURCE_QUADRATIC_ZERO",
            "1885/1886 remain active blockers.",
        ),
        (
            "BKA2179_5_boundary_readout_slot",
            "boundary/readout quadratic slot",
            "Boundary, projector, endpoint or coframe second-order terms can contribute to kappa_v even if the bulk Poisson equation is linear.",
            "MISSING_BOUNDARY_READOUT_ZERO",
            "kappa_v must be carried as an absolute residual unless all slots close.",
        ),
        (
            "BKA2179_6_current_verdict",
            "kappa_v theorem status",
            "Current corpus does not parent-sign eta_v=0, quadratic source silence, boundary silence, readout gauge or source conservation.",
            "KAPPA_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "beta remains blocked.",
        ),
    ]
    return [
        base_row(
            beta_id=beta_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for beta_id, object_name, statement, status, implication in specs
    ]


def residual_rows() -> list[dict[str, Any]]:
    specs = [
        ("VFR2179_0_Kv", "K_v", "weak-field v kinetic coefficient in -K_v(grad v)^2", "MISSING_PARENT_VALUE_OR_SOURCE_PATH", "energy_density_length2_or_declared", "Newton;PPN;local_GR"),
        ("VFR2179_1_Cv", "C_v", "linear source coefficient in -C_v rho c^2 v", "MISSING_PARENT_VALUE_OR_SOURCE_PATH", "dimensionless", "Newton;PPN;WEP;clock"),
        ("VFR2179_2_delta_norm", "delta_v_source_norm", "C_v c^4/(16piG K_v)-1", "MISSING_KV_CV_THEOREM_OR_NUMERIC_VALUE", "dimensionless", "Newton;PPN;orbital"),
        ("VFR2179_3_eta", "eta_v", "cubic kinetic coefficient in representative -K_v(1+eta_v v)(grad v)^2 branch", "MISSING_NONLINEAR_KINETIC_ZERO_OR_VALUE", "dimensionless", "PPN_beta;local_GR"),
        ("VFR2179_4_kappa", "kappa_v", "quadratic weak-field drift v=-2U/c^2+kappa_v U^2/c^4", "MISSING_KAPPA_ZERO_OR_VALUE", "dimensionless", "PPN_beta;local_GR"),
        ("VFR2179_5_source_quad", "beta_w_or_C2_v", "quadratic source/action-weight contribution to v source normalization and beta", "MISSING_NO_SOURCE_ONLY_SLOT_OR_VALUE", "dimensionless_or_declared", "WEP;PPN;R10;clock"),
        ("VFR2179_6_boundary", "epsilon_v_boundary_beta", "boundary/projector/readout contribution to kappa_v", "MISSING_BOUNDARY_READOUT_ZERO_OR_BOUND", "dimensionless_beta_projection", "orbital;light_time;PPN"),
        ("VFR2179_7_conservation", "epsilon_v_conservation", "Bianchi-like source conservation failure for the same v source", "MISSING_CONSERVATION_IDENTITY_OR_BOUND", "dimensionless_divergence_norm", "local_GR;PPN;cosmology"),
        ("VFR2179_8_total", "epsilon_v_action_abs", "absolute no-cancellation envelope for source normalization and beta residuals", "MISSING_COMPONENT_VALUES", "declared_common_norm", "all_local_arenas"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            status=status,
            units=units,
            observable_link=observable_link,
            value="MISSING_NUMERIC_VALUE",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
            no_cancellation_policy=True,
        )
        for row_id, symbol, definition, status, units, observable_link in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2179_0_Kv_Cv", "K_v and C_v parent normalized", "UNSIGNED", "source-normalized Newton remains blocked"),
        ("CG2179_1_delta_norm", "delta_v_source_norm=0 theorem", "UNSIGNED", "only exact conditional coefficient law exists"),
        ("CG2179_2_kappa", "kappa_v=0 theorem or finite row", "UNSIGNED", "beta remains blocked"),
        ("CG2179_3_source_slot", "no quadratic/source-only matter slot", "UNSIGNED", "1886 source seam remains active"),
        ("CG2179_4_conservation", "same source obeys conservation/Bianchi identity", "UNSIGNED", "field-theory status incomplete"),
        ("CG2179_5_conditional_win", "pure quadratic/linear branch would pass Newton and beta shape", "CONDITIONAL_PASS", "good theorem target but not parent-signed"),
        ("CG2179_6_verdict", "local Newton/GR claim", "BLOCKED_NONCLAIM", "2179 derives coefficient laws and residual rows, not a claim"),
    ]
    return [
        base_row(
            gate_id=gate_id,
            gate=gate,
            status=status,
            implication=implication,
        )
        for gate_id, gate, status, implication in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2179_0_gain_source_law",
            "KV_CV_NORMALIZATION_LAW_DERIVED",
            "delta_v_source_norm=(C_v c^4/(16piG K_v))-1, so the Newton source problem is reduced to a precise parent coefficient ratio.",
            "selected",
        ),
        (
            "DEC2179_1_gain_beta_law",
            "KAPPA_BETA_AND_ETA_MAP_DERIVED",
            "beta=1+kappa_v/2, and the representative cubic kinetic coefficient gives kappa_v=-eta_v.",
            "selected",
        ),
        (
            "DEC2179_2_conditional_win",
            "PURE_BRANCH_WOULD_CLOSE_LOCAL_SHAPE",
            "pure quadratic kinetic plus linear universal source gives delta_v_source_norm=0 and kappa_v=0 if K_v,C_v have the target values.",
            "selected",
        ),
        (
            "DEC2179_3_no_claim",
            "PARENT_COEFFICIENTS_AND_SOURCE_SLOTS_UNSIGNED",
            "K_v, C_v, eta_v, quadratic source weights, boundary/readout silence and conservation are not parent-signed.",
            "selected",
        ),
        (
            "DEC2179_4_next",
            "MASS_CURRENT_TO_V_SOURCE_COEFFICIENT_GLUE_NEXT",
            "the next derivation should connect Pi_M J_H/source-measure glue to K_v,C_v and eta_v=0, or fill finite rows.",
            "selected",
        ),
    ]
    return [
        base_row(
            decision_id=decision_id,
            decision=decision,
            rationale=rationale,
            selection_status=status,
        )
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2179_0_2180",
            selection_status="selected",
            target_file="2180-Y5-R2FR-PiM-JH-mass-current-to-v-source-coefficient-glue-or-delta-kappa-fill.md",
            target_script="scripts/Y5_R2FR_PiM_JH_mass_current_to_v_source_coefficient_glue_or_delta_kappa_fill_2180.py",
            objective="derive how the parent mass-current/source-measure chain fixes K_v, C_v, universal matter coupling and eta_v=0 for the constrained v branch, or fill delta_v_source_norm/kappa_v finite rows",
            success_condition="Pi_M J_H/source-measure glue yields the target C_v/K_v ratio, no source-only quadratic slot, conservation identity and kappa_v=0; otherwise finite rows are source-backed and nonclaim",
            do_not_do="do not absorb source mismatch into measured GM without common-mode guards, do not import EH, do not claim beta from gamma",
        ),
        base_row(
            route_id="NEXT2179_1_finite_parallel",
            selection_status="held_parallel",
            target_file="2180b-Y5-R2FR-delta-v-source-norm-and-kappa-finite-row-acquisition.md",
            target_script="scripts/Y5_R2FR_delta_v_source_norm_and_kappa_finite_row_acquisition_2180b.py",
            objective="if derivation fails, acquire source-backed finite rows for delta_v_source_norm, eta_v and kappa_v with PPN/Newton projection",
            success_condition="at least one finite row has numeric value, units, source path, convention and remains nonclaim until the full envelope closes",
            do_not_do="do not score symbolic placeholders or cancellation-only rows",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["action_audit"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["normalization_law"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2179_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2179_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    action_statuses = {row["status"] for row in rows_by_name["action_audit"]}
    action_pass = "PURE_QUADRATIC_LINEAR_SOURCE_CONDITIONAL" in action_statuses and "MISSING_PARENT_KV_CV_ORIGIN" in action_statuses
    validations.append(base_row(validation_id="VAL2179_02_action_audit", status="PASS" if action_pass else "FAIL", detail="K_v/C_v target branch is exact conditional but not parent-origin signed"))

    law_statuses = {row["status"] for row in rows_by_name["normalization_law"]}
    law_pass = "EXACT_NORMALIZATION_RESIDUAL" in law_statuses and "PASS_CONDITIONAL_TARGET" in law_statuses
    validations.append(base_row(validation_id="VAL2179_03_normalization_law", status="PASS" if law_pass else "FAIL", detail="delta_v_source_norm law derived and target coefficients checked"))

    beta_statuses = {row["status"] for row in rows_by_name["beta_audit"]}
    beta_pass = "EXACT_BETA_LAW_FROM_2178" in beta_statuses and "EXACT_REPRESENTATIVE_NONLINEAR_DRIFT" in beta_statuses and "KAPPA_ZERO_NOT_DERIVED_CURRENT_CORPUS" in beta_statuses
    validations.append(base_row(validation_id="VAL2179_04_beta_audit", status="PASS" if beta_pass else "FAIL", detail="kappa/beta law and representative eta_v drift derived; zero not claimed"))

    residual_rows_local = rows_by_name["residual_rows"]
    residuals_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in residual_rows_local)
    validations.append(base_row(validation_id="VAL2179_05_residual_rows", status="PASS" if residuals_ok else "FAIL", detail=f"delta_v/kappa finite rows={len(residual_rows_local)} remain score_ready=false"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2179_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in claim_statuses and "CONDITIONAL_PASS" in claim_statuses else "FAIL", detail="local Newton/GR claim remains blocked despite exact coefficient laws"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2179_07_decision", status="PASS" if "MASS_CURRENT_TO_V_SOURCE_COEFFICIENT_GLUE_NEXT" in decision_text else "FAIL", detail="decision selects Pi_M J_H/source-measure glue next"))

    validations.append(base_row(validation_id="VAL2179_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2180" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2180 mass-current to v-source coefficient glue target selected"))

    validations.append(base_row(validation_id="VAL2179_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2179_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2179_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2179_artifacts()
    validations.append(base_row(validation_id="VAL2179_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2179 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2179_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2179_OVERALL", status="PASS" if overall else "FAIL", detail="2179 derives K_v/C_v source-normalization law and kappa_v beta drift map while keeping Newton/local-GR blocked"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2179 - Y5/R2FR Parent V Field Action Normalization And Beta Quadratic Zero Or Finite Row

## Current Verdict

2179 gets the next useful piece: the Newton problem is now a **coefficient-ratio theorem**, not a vague local-GR wish.

Take the weak-field parent template:

`L_v=-K_v (grad v)^2 - C_v rho c^2 v`.

Variation gives:

`2K_v laplacian(v)-C_v rho c^2=0`,

so:

`laplacian(v)=(C_v c^2/(2K_v)) rho`.

Against the 2178 target `laplacian(v)=8piG rho/c^2`, the exact residual is:

`delta_v_source_norm=(C_v c^4/(16piG K_v))-1`.

The target values `K_v=c^4/(32piG)` and `C_v=1/2` make this vanish. That is clean. But current MTS does **not** yet derive those coefficients from the parent action, so Newton is not claimed.

The beta side also sharpens. From 2178:

`beta=1+kappa_v/2`.

For a representative nonlinear kinetic correction:

`L=-K_v(1+eta_v v)(grad v)^2`,

the exterior weak-field equation gives:

`kappa_v=-eta_v`.

So beta is not a mystery bucket anymore. If the parent action contains a cubic kinetic coefficient, a quadratic source slot, or a boundary/readout quadratic tail, it must be zero, gauge-owned, or finite-and-tested. Gamma cannot save it.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## V Action Coefficient Audit

{md_table(rows_by_name["action_audit"], ["audit_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Source Normalization Law

{md_table(rows_by_name["normalization_law"], ["law_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Beta Kappa Audit

{md_table(rows_by_name["beta_audit"], ["beta_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Delta V / Kappa Finite Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## Claim Gate

{md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is a good step because it reduces a philosophical gap to named coefficients:

1. `K_v` must be parent-derived with the correct normalization;
2. `C_v` must be parent-derived as a universal matter coupling;
3. `eta_v`, quadratic source weights, and boundary/readout quadratic terms must be zero, gauge, or finite;
4. `delta_v_source_norm` and `kappa_v` are now the live local-GR residuals.

The next move should not be another coframe pass. It should connect the parent mass-current/source-measure chain, especially the older `Pi_M J_H` obstruction, to `K_v`, `C_v`, and `eta_v=0`. If that chain closes, we are genuinely closer to derived Newton/GR. If it does not, the finite-row empirical branch is unavoidable.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "action_audit": action_audit_rows(),
        "normalization_law": normalization_law_rows(),
        "beta_audit": beta_audit_rows(),
        "residual_rows": residual_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "action_audit", "normalization_law", "beta_audit", "residual_rows", "claim_gate", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
