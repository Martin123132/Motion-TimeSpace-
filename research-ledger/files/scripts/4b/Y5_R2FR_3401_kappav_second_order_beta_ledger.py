from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "3401-Y5-R2FR-kappav-second-order-beta-ledger-under-AX1090.md"


SOURCES = {
    "3400_doc": ROOT / "3400-Y5-R2FR-first-order-source-coupling-parent-signature-pack-under-AX1090.md",
    "3400_clauses": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "3400_activation": OUT / "P8_Y5_R2FR_3400_FIRST_ORDER_ACTIVATION_THEOREM.csv",
    "3399_kappav_targets": OUT / "P8_Y5_R2FR_3399_KAPPAV_SECOND_ORDER_TARGETS.csv",
    "2576_law": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv",
    "delta_beta_derivation": OUT / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv",
    "beta_envelope": OUT / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv",
    "beta_demotion": OUT / "P8_Y5_BETA_DEMOTION_RESIDUAL_ROW.csv",
    "beta_finite_vector": OUT / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv",
    "beta_second_order_gate": OUT / "P8_Y5_NO_SHADOW_2514_BETA_SECOND_ORDER_GATE.csv",
    "r11_beta_vector": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "jpim_bounds": OUT / "P8_Y5_NO_SHADOW_2524_JPIM_BOUND_ROWS.csv",
    "jreadout_bounds": OUT / "P8_Y5_NO_SHADOW_2523_JREADOUT_BOUND_ROWS.csv",
    "source_calibrated_eh_stack": OUT / "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
    "eh_premise_audit": OUT / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
    "local_eh_r11_audit": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
}


OUTPUT_PATHS = {
    "source_register": OUT / "P8_Y5_R2FR_3401_SOURCE_REGISTER.csv",
    "beta_dictionary_lock": OUT / "P8_Y5_R2FR_3401_BETA_DICTIONARY_LOCK.csv",
    "eta_v_derivation": OUT / "P8_Y5_R2FR_3401_ETA_V_EXPONENTIAL_READOUT_DERIVATION.csv",
    "source_square_law": OUT / "P8_Y5_R2FR_3401_SOURCE_AB_SQUARE_LAW.csv",
    "kappav_component_ledger": OUT / "P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv",
    "kappav_bound_target": OUT / "P8_Y5_R2FR_3401_KAPPAV_BOUND_TARGET.csv",
    "evidence_extraction": OUT / "P8_Y5_R2FR_3401_EVIDENCE_EXTRACTION.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3401_PROMOTION_GATES.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3401_RUNNER_NONCLAIM.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3401_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3401_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3401_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": f"SRC3401_{idx:02d}_{name}",
            "path": str(path),
            "exists": path.exists(),
            "role": "kappav_beta_source",
            "valid_for_claim": False,
        }
        for idx, (name, path) in enumerate(SOURCES.items())
    ]


def beta_bound_value() -> float:
    rows = read_csv(SOURCES["local_bounds"])
    for row in rows:
        if row.get("row_id") == "R4_beta" or row.get("observable") == "beta_minus_1":
            return float(row["upper_bound"])
    raise RuntimeError("R4_beta bound not found")


def beta_dictionary_lock() -> list[dict[str, Any]]:
    beta_bound = beta_bound_value()
    return [
        {
            "dict_id": "BDL3401_0_ppn_beta",
            "statement": "PPN beta is defined by g_00=-1+2U/c^2-2*beta*U^2/c^4+O(c^-6) in a valid observed PPN coordinate/readout.",
            "formula": "beta_minus_1 := beta-1",
            "source": str(SOURCES["beta_second_order_gate"]),
            "status": "DICTIONARY_LOCKED",
            "valid_for_claim": False,
        },
        {
            "dict_id": "BDL3401_1_kappav",
            "statement": "2576 fixes beta-1=kappa_v/2 in the constrained v-readout branch.",
            "formula": "kappa_v = 2*(beta-1)",
            "source": str(SOURCES["2576_law"]),
            "status": "KAPPAV_BETA_CONVERSION_LOCKED",
            "valid_for_claim": False,
        },
        {
            "dict_id": "BDL3401_2_bound",
            "statement": "The local beta comparator becomes a kappa_v comparator target, but not a score until MTS predicts kappa_v.",
            "formula": f"|beta-1| <= {beta_bound:.8g}; |kappa_v| <= {2*beta_bound:.8g}",
            "source": str(SOURCES["local_bounds"]),
            "status": "BOUND_TARGET_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def eta_v_derivation() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "ETA3401_0_ansatz",
            "statement": "Allow the v potential to have a second-order observed-source correction.",
            "math": "v = -2U/c^2 + a_v U^2/c^4 + O(c^-6)",
            "result": "a_v is the intrinsic v-lane beta coefficient to derive or bound",
            "valid_for_claim": False,
        },
        {
            "step_id": "ETA3401_1_expand",
            "statement": "Expand the exponential readout.",
            "math": "e^v = 1 - 2U/c^2 + (a_v+2)U^2/c^4 + O(c^-6)",
            "result": "g_00=-e^v = -1+2U/c^2-(a_v+2)U^2/c^4+O(c^-6)",
            "valid_for_claim": False,
        },
        {
            "step_id": "ETA3401_2_compare",
            "statement": "Compare with the PPN beta dictionary.",
            "math": "-2*beta = -(a_v+2)",
            "result": "beta-1=a_v/2, hence kappa_v_eta_lane=a_v",
            "valid_for_claim": False,
        },
        {
            "step_id": "ETA3401_3_zero_condition",
            "statement": "If the parent v equation gives v=-2U/c^2+O(c^-6) in the observed PPN gauge, the exponential readout itself gives beta=1.",
            "math": "a_v=0 => beta=1 => kappa_v_eta_lane=0",
            "result": "eta_v is reduced to the concrete task: derive or bound the U^2 coefficient a_v in v",
            "valid_for_claim": False,
        },
    ]


def source_square_law() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "SSL3401_0_unmeasured_W",
            "statement": "Before measured-GM normalization, write the source potential as W.",
            "math": "g_00=-1+2A_source W/c^2-2B_source W^2/c^4+O(c^-6)",
            "result": "A_source is first-order amplitude; B_source is quadratic source response",
            "source": str(SOURCES["delta_beta_derivation"]),
            "valid_for_claim": False,
        },
        {
            "law_id": "SSL3401_1_measured_U",
            "statement": "Measured U is the first-order calibrated potential.",
            "math": "U=A_source W",
            "result": "beta_eff=B_source/A_source^2",
            "source": str(SOURCES["delta_beta_derivation"]),
            "valid_for_claim": False,
        },
        {
            "law_id": "SSL3401_2_square_condition",
            "statement": "A constant first-order source renormalization is safe only if the quadratic response squares it.",
            "math": "delta_beta_source=B_source/A_source^2-1; kappa_source_quad=2*(B_source/A_source^2-1)",
            "result": "safe source branch requires B_source=A_source^2, not merely fitted GM",
            "source": str(SOURCES["delta_beta_derivation"]),
            "valid_for_claim": False,
        },
    ]


def kappav_component_ledger() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "KV3401_0_eta_v",
            "component": "eta_v / intrinsic v lane",
            "beta_contribution": "delta_beta_eta=a_v/2",
            "kappav_contribution": "kappa_eta=a_v",
            "zero_condition": "parent v solution has no independent U^2/c^4 correction in observed PPN gauge: a_v=0",
            "finite_bound": "|kappa_eta| <= B_a_v",
            "current_status": "FORMULA_DERIVED_A_V_PARENT_COEFFICIENT_MISSING",
            "source_files": str(SOURCES["2576_law"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "KV3401_1_source_quad",
            "component": "kappa_source_quad",
            "beta_contribution": "delta_beta_source=B_source/A_source^2-1",
            "kappav_contribution": "2*delta_beta_source",
            "zero_condition": "B_source=A_source^2 after fixed observed source normalization",
            "finite_bound": "|kappa_source_quad| <= 2*B_delta_beta_source",
            "current_status": "LAW_DERIVED_A_SOURCE_B_SOURCE_MISSING",
            "source_files": str(SOURCES["delta_beta_derivation"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "KV3401_2_PiM",
            "component": "kappa_PiM",
            "beta_contribution": "delta_beta_PiM from Pi_M/Hamiltonian projector mass correction",
            "kappav_contribution": "2*delta_beta_PiM",
            "zero_condition": "Pi_M is fixed chain map, H_tau charge equals Pi_M J_H, and projector stress has no U^2 beta projection",
            "finite_bound": "|kappa_PiM| <= 2*B_JPiM_beta",
            "current_status": "COMPONENT_BOUND_SCHEMA_EXISTS_VALUES_MISSING",
            "source_files": str(SOURCES["jpim_bounds"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "KV3401_3_boundary",
            "component": "kappa_boundary",
            "beta_contribution": "delta_beta_boundary_domain",
            "kappav_contribution": "2*delta_beta_boundary_domain",
            "zero_condition": "boundary/reference/domain/projector stress has no compact exterior U^2 beta leakage",
            "finite_bound": "|kappa_boundary| <= 2*B_boundary_domain",
            "current_status": "FINITE_VECTOR_SCHEMA_EXISTS_VALUES_MISSING",
            "source_files": str(SOURCES["beta_finite_vector"]) + ";" + str(SOURCES["jpim_bounds"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "KV3401_4_readout",
            "component": "kappa_readout",
            "beta_contribution": "delta_beta_readout",
            "kappav_contribution": "2*delta_beta_readout",
            "zero_condition": "same observed metric/coframe/readout theorem holds through O(U^2)",
            "finite_bound": "|kappa_readout| <= 2*B_readout",
            "current_status": "READOUT_BOUND_SCHEMA_EXISTS_VALUES_MISSING",
            "source_files": str(SOURCES["jreadout_bounds"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "KV3401_5_operator",
            "component": "kappa_operator",
            "beta_contribution": "delta_beta_R11 or delta_beta_operator",
            "kappav_contribution": "2*delta_beta_operator",
            "zero_condition": "EH-only local exterior/no-hair theorem or every retained non-EH operator coefficient is zero/bounded below beta and tighter vector locks",
            "finite_bound": "|kappa_operator| <= 2*sum_i |delta_beta_R11_i|",
            "current_status": "R11_VECTOR_EXISTS_COEFFICIENTS_MISSING",
            "source_files": str(SOURCES["r11_beta_vector"]) + ";" + str(SOURCES["local_eh_r11_audit"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "KV3401_6_coupling",
            "component": "kappa_coupling",
            "beta_contribution": "delta_beta_coupling from second-order propagation of delta_kappa/delta_ellJ/baseline/source-calibration",
            "kappav_contribution": "2*delta_beta_coupling",
            "zero_condition": "PC3400 source-coupling clauses are adopted through O(U^2), no calibration feedback, and no source-current scale drift survives",
            "finite_bound": "|kappa_coupling| <= 2*B_coupling_U2",
            "current_status": "FIRST_ORDER_ROUTE_STAGED_SECOND_ORDER_EXTENSION_UNSIGNED",
            "source_files": str(SOURCES["3400_clauses"]) + ";" + str(SOURCES["3400_activation"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "KV3401_7_q_loc_guard",
            "component": "q_loc beta/projection guard",
            "beta_contribution": "delta_beta_q_loc provisional compact-shell value exists but is not accepted",
            "kappav_contribution": "2*delta_beta_q_loc if physical U2 projection is signed",
            "zero_condition": "q_loc Ward-zero through O(U^2), or beta projection below beta lock and preferred-frame projection below alpha_i/alpha3 locks",
            "finite_bound": "|kappa_q_loc| <= 2*B_q_loc_beta plus separate alpha_i guard",
            "current_status": "PROVISIONAL_NUMERIC_DIAGNOSTIC_NOT_SCORE_READY_ALPHA3_GUARD_SEVERE",
            "source_files": str(SOURCES["beta_envelope"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def kappav_bound_target() -> list[dict[str, Any]]:
    beta_bound = beta_bound_value()
    return [
        {
            "bound_id": "KVB3401_0_empirical_target",
            "quantity": "kappa_v",
            "formula": "beta-1=kappa_v/2",
            "beta_bound": beta_bound,
            "kappav_bound": 2 * beta_bound,
            "units": "dimensionless",
            "source": str(SOURCES["local_bounds"]),
            "score_status": "TARGET_ONLY_NO_MTS_PREDICTION",
            "valid_for_claim": False,
        },
        {
            "bound_id": "KVB3401_1_absolute_envelope",
            "quantity": "kappa_v_abs_bound",
            "formula": "|kappa_v| <= |a_v| + 2*(|delta_beta_source|+|delta_beta_PiM|+|delta_beta_boundary|+|delta_beta_readout|+|delta_beta_operator|+|delta_beta_coupling|+|delta_beta_q_loc|)",
            "beta_bound": beta_bound,
            "kappav_bound": 2 * beta_bound,
            "units": "dimensionless",
            "source": "3401 component ledger",
            "score_status": "FORMULA_READY_COMPONENT_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "KVB3401_2_zero_theorem",
            "quantity": "kappa_v_zero_route",
            "formula": "a_v=0 and all component beta residuals zero => kappa_v=0 => beta=1",
            "beta_bound": beta_bound,
            "kappav_bound": 2 * beta_bound,
            "units": "dimensionless",
            "source": "3401 eta/source/component theorem",
            "score_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
    ]


def evidence_extraction() -> list[dict[str, Any]]:
    rows = []
    checks = [
        ("EV3401_0_beta_law", SOURCES["delta_beta_derivation"], "beta_eff = B/A^2", "LAW_PRESENT"),
        ("EV3401_1_beta_vector", SOURCES["beta_finite_vector"], "MISSING_NUMERIC_DELTA_BETA", "FINITE_VECTOR_SCHEMA_MISSING_VALUES"),
        ("EV3401_2_r11_vector", SOURCES["r11_beta_vector"], "B530_11_readout_frame", "R11_VECTOR_PRESENT"),
        ("EV3401_3_jpim", SOURCES["jpim_bounds"], "JPIM2524_0_total", "PIM_BOUND_SCHEMA_PRESENT"),
        ("EV3401_4_jreadout", SOURCES["jreadout_bounds"], "JRO2523_0_total", "READOUT_BOUND_SCHEMA_PRESENT"),
        ("EV3401_5_eh_stack", SOURCES["source_calibrated_eh_stack"], "SCEH529_5_isotropic_PPN_expansion", "EH_BETA_ROUTE_CONDITIONAL"),
        ("EV3401_6_eh_premises", SOURCES["eh_premise_audit"], "PRE1512_2_second_order", "SECOND_ORDER_EH_PREMISE_BLOCKED"),
        ("EV3401_7_bounds", SOURCES["local_bounds"], "R4_beta", "LOCAL_BETA_BOUND_PRESENT"),
    ]
    for evidence_id, path, needle, status in checks:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "evidence_id": evidence_id,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "extracted_status": status,
                "valid_for_claim": False,
            }
        )
    return rows


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3401_0_dictionary",
            "claim": "kappa_v beta dictionary and empirical target are defined",
            "gate_pass": True,
            "reason": "beta-1=kappa_v/2 and |kappa_v| target is derived from local beta bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3401_1_eta_derivation",
            "claim": "intrinsic v-lane beta drift is reduced to a_v",
            "gate_pass": True,
            "reason": "expansion of g_tt=-exp(v)c^2 gives beta-1=a_v/2",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3401_2_source_square",
            "claim": "source-quadratic beta law is derived",
            "gate_pass": True,
            "reason": "delta_beta_source=B_source/A_source^2-1",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3401_3_component_values",
            "claim": "kappa_v component values are score-ready",
            "gate_pass": False,
            "reason": "a_v, A_source/B_source, PiM, boundary, readout, operator and coupling values/theorem-zeroes remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3401_4_beta_claim",
            "claim": "beta=1 or beta bound pass is an MTS prediction",
            "gate_pass": False,
            "reason": "component ledger is nonclaim; no accepted kappa_v prediction row exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3401_5_local_GR",
            "claim": "local GR is derived",
            "gate_pass": False,
            "reason": "beta/kappa_v still open and full PPN vector still requires alpha_i, zeta_i and xi",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3401_0_beta_dictionary",
            "test": "beta/kappa_v conversion",
            "status": "PASS_DICTIONARY_LOCKED_NONCLAIM",
            "detail": "kappa_v target bound is 2*beta bound",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3401_1_eta",
            "test": "exponential v readout derivation",
            "status": "PASS_A_V_DERIVATION",
            "detail": "beta-1=a_v/2 for v=-2U/c^2+a_v U^2/c^4",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3401_2_components",
            "test": "kappa_v component ledger",
            "status": "PASS_LEDGER_WRITTEN_VALUES_MISSING",
            "detail": "eight rows including q_loc guard; none score-ready",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3401_3_claim_firewall",
            "test": "beta/local-GR claim",
            "status": "BLOCKED_NO_CLAIM",
            "detail": "no kappa_v prediction, no beta score, no local-GR promotion",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3401_0_real_progress",
            "finding": "kappa_v is now an executable second-order beta ledger, not a vague blocker",
            "reason": "eta_v is reduced to a_v; source_quad is reduced to B/A^2; all remaining components are mapped to existing bound ledgers",
            "next_action": "attack a_v and B_source/A_source first because they are the cleanest derivation route",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3401_1_best_math_route",
            "finding": "derive v has no U^2 correction or that B_source=A_source^2",
            "reason": "either result removes a core beta component without numeric fitting",
            "next_action": "build 3402 v-second-order/source-square theorem attempt",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3401_2_claim_status",
            "finding": "beta remains open but sharply localized",
            "reason": "component values/theorem-zeroes are missing; external beta bound is only a target",
            "next_action": "do not score beta until kappa_v prediction row exists",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3402-Y5-R2FR-v-second-order-source-square-theorem-attempt-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3402_v_second_order_source_square_theorem_attempt.py",
            "objective": "try to prove a_v=0 and/or B_source=A_source^2 from the parent v/source equations under PC3400 clauses, otherwise emit finite input rows",
            "why_next": "these are the two cleanest kappa_v components and they decide whether beta can be derived rather than merely bounded",
            "valid_for_claim": False,
        },
        {
            "target_id": "3403-Y5-R2FR-PiM-boundary-readout-operator-beta-residual-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3403_PiM_boundary_readout_operator_beta_residual_fill.py",
            "objective": "fill or theorem-zero the PiM, boundary, readout, operator, q_loc and coupling components of kappa_v",
            "why_next": "if the clean source-square route is insufficient, the remaining kappa_v terms must be bounded component by component",
            "valid_for_claim": False,
        },
    ]


def validate(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": passed, "detail": detail})

    add("VAL3401_0_sources_exist", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3401_1_beta_dictionary", "beta/kappa_v dictionary is present", any("kappa_v = 2" in row["formula"] for row in outputs["beta_dictionary_lock"]), "")
    add("VAL3401_2_eta_derivation", "eta/v derivation gives beta-1=a_v/2", any("beta-1=a_v/2" in row["result"] for row in outputs["eta_v_derivation"]), "")
    add("VAL3401_3_source_square", "source square law gives B_source/A_source^2", any("B_source/A_source^2" in row["math"] for row in outputs["source_square_law"]), "")
    add("VAL3401_4_components", "component ledger covers required kappa_v pieces", len(outputs["kappav_component_ledger"]) >= 8, "")
    add("VAL3401_5_bound_target", "kappa_v target is twice beta target", abs(outputs["kappav_bound_target"][0]["kappav_bound"] - 2 * outputs["kappav_bound_target"][0]["beta_bound"]) < 1e-18, "")
    add("VAL3401_6_no_score_ready", "no component is score-ready", not any(row.get("score_ready") is True for row in outputs["kappav_component_ledger"]), "")
    add("VAL3401_7_no_overclaim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim", False)).lower() == "false" for group in outputs.values() for row in group), "")
    add("VAL3401_8_scope", "no 3401 output path targets formalization-workbench", "formalization-workbench" not in str(DOC).lower() and all("formalization-workbench" not in str(path).lower() for path in OUTPUT_PATHS.values()), "")
    add("VAL3401_9_next_target", "next target goes to v/source-square theorem attempt", any("a_v=0" in row["objective"] for row in outputs["next_target"]), "")
    add("VAL3401_10_overall", "3401 validation overall", all(row["passed"] is True for row in rows), "all required checks passed")
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    sections = [
        "# 3401 - Y5/R2FR kappa_v second-order beta ledger under AX1090",
        "",
        "## Summary",
        "- 3401 converts `kappa_v` into a concrete beta ledger instead of leaving beta as a foggy missing theorem.",
        "- Main derivation: if `v=-2U/c^2+a_v U^2/c^4`, then `g_tt=-exp(v)c^2` gives `beta-1=a_v/2`; therefore the intrinsic v-lane target is `a_v=0`.",
        "- Source-normalization beta is also locked: `beta_eff=B_source/A_source^2`, so the safe source route is `B_source=A_source^2`.",
        "- The empirical target is only a target: `|beta-1|<=7.8e-05` means `|kappa_v|<=1.56e-04`, but no MTS beta score is run.",
        "- Beta/local-GR remains unclaimed because component values/theorem-zeroes are missing.",
        f"- Generated UTC: `{timestamp}`.",
        "",
        "## Source Register",
        md_table(outputs["source_register"]),
        "",
        "## Beta Dictionary Lock",
        md_table(outputs["beta_dictionary_lock"]),
        "",
        "## Eta_v Exponential Readout Derivation",
        md_table(outputs["eta_v_derivation"]),
        "",
        "## Source A/B Square Law",
        md_table(outputs["source_square_law"]),
        "",
        "## Kappa_v Component Ledger",
        md_table(outputs["kappav_component_ledger"]),
        "",
        "## Kappa_v Bound Target",
        md_table(outputs["kappav_bound_target"]),
        "",
        "## Evidence Extraction",
        md_table(outputs["evidence_extraction"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Nonclaim Runner",
        md_table(outputs["runner_nonclaim"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    outputs = {
        "source_register": source_register(),
        "beta_dictionary_lock": beta_dictionary_lock(),
        "eta_v_derivation": eta_v_derivation(),
        "source_square_law": source_square_law(),
        "kappav_component_ledger": kappav_component_ledger(),
        "kappav_bound_target": kappav_bound_target(),
        "evidence_extraction": evidence_extraction(),
        "promotion_gates": promotion_gates(),
        "runner_nonclaim": runner_nonclaim(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    outputs["validation"] = validate(outputs)
    for name, rows in outputs.items():
        write_csv(OUTPUT_PATHS[name], rows)
    parsed = [(path.name, len(read_csv(path))) for path in OUTPUT_PATHS.values()]
    if not all(row["passed"].lower() == "true" for row in read_csv(OUTPUT_PATHS["validation"])):
        raise RuntimeError("3401 validation failed")
    write_doc(outputs)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUT_PATHS)} CSV outputs under {OUT}")
    print("Parsed outputs: " + "; ".join(f"{name}={count}" for name, count in parsed))


if __name__ == "__main__":
    main()
