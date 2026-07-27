from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1928"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1928-Y5-R2FR-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1927_next": OUT / "P8_Y5_PARENT_QLOC_1927_NEXT_TARGET.csv",
    "1927_doc": ROOT / "1927-Y5-R2FR-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md",
    "1927_validation": OUT / "P8_Y5_BRR545_1927_VALIDATION.csv",
    "1099_em_theorem": OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
    "1099_exclusion": OUT / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
    "1099_counterexamples": OUT / "P8_Y5_R10_1099_COUNTEREXAMPLE_LEDGER.csv",
    "1099_alpha_rows": OUT / "P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv",
    "1099_claims": OUT / "P8_Y5_R10_1099_CLAIM_GATES.csv",
    "1099_runner": OUT / "P8_Y5_R10_1099_PRODUCT_RUNNER_STATUS.csv",
    "1099_next": OUT / "P8_Y5_R10_1099_NEXT_TARGET.csv",
    "1100_tq_theorem": OUT / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
    "1100_tq_signature": OUT / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
    "1100_decomposition": OUT / "P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv",
    "1100_claims": OUT / "P8_Y5_R10_1100_CLAIM_GATES.csv",
    "1100_next": OUT / "P8_Y5_R10_1100_NEXT_TARGET.csv",
}

NEEDLES = {
    "1927_next": ["NEXT1927_0_primary", "unique EM kinetic owner"],
    "1927_doc": ["STAT1927_0_gain", "VAL1927_OVERALL"],
    "1927_validation": ["VAL1927_OVERALL", "PASS"],
    "1099_em_theorem": ["UEM1099_3_verdict", "NO_EXTRA_F2_THEOREM_NOT_PROMOTED"],
    "1099_exclusion": ["EXC1099_0_diffeomorphism", "EXC1099_5_radiative"],
    "1099_counterexamples": ["CX1099_0_lambda_A", "CX1099_2_readout"],
    "1099_alpha_rows": ["ASR1099_0_theorem_zero_candidate", "ASR1099_4_R10_projection"],
    "1099_claims": ["CG1099_0_no_extra_F2", "CG1099_2_WEP_R10_transfer"],
    "1099_runner": ["valid_prediction_rows", "reject missing alpha owner"],
    "1099_next": ["NEXT1099_0_1100", "parent charge-generator owner"],
    "1100_tq_theorem": ["TQT1100_0_exact_conditional", "TQT1100_4_verdict"],
    "1100_tq_signature": ["TQS1100_0_parent_TQ_object", "TQS1100_6_verdict"],
    "1100_decomposition": ["Z1100_0_parent_piece", "Z1100_4_total"],
    "1100_claims": ["CG1100_0_TQ_signature", "CG1100_2_finite_products"],
    "1100_next": ["NEXT1100_0_1101", "level, index, monopole"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1928_SOURCE_REGISTER.csv",
    "em_owner_audit": OUT / "P8_Y5_PARENT_QLOC_1928_EM_OWNER_NO_EXTRA_F2_AUDIT.csv",
    "exclusion_audit": OUT / "P8_Y5_PARENT_QLOC_1928_NO_EXTRA_F2_EXCLUSION_LEDGER.csv",
    "alpha_rows": OUT / "P8_Y5_PARENT_QLOC_1928_ALPHA_COEFFICIENT_ROWS_NONCLAIM.csv",
    "tq_signature_inputs": OUT / "P8_Y5_PARENT_QLOC_1928_TQ_SIGNATURE_INPUT_PACK_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1928_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1928_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1928_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1928_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1928_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["em_owner_audit"], SOURCE_WEIGHT_DOCS / "EM_OWNER_NO_EXTRA_F2_AUDIT_1928_NONCLAIM.csv"),
    (OUTPUTS["alpha_rows"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1928_ALPHA_COEFFICIENT_ROWS_NONCLAIM.csv"),
    (OUTPUTS["alpha_rows"], QUEUE / "JR1928_ALPHA_COEFFICIENT_SOURCE_ROW_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1928_CLAIM_GATE.csv"),
]


def ensure_dirs() -> None:
    for path in [OUT, SOURCE_WEIGHT_DOCS, MICROSCOPE_COEFFS, QUEUE, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in NEEDLES[key] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1928 unique EM kinetic owner no-extra-F2 theorem or alpha coefficient source row",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def em_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEM1928_0_target",
            "claim_piece": "unique EM kinetic owner",
            "mathematical_statement": "S_EM=-(C_P/4) int mu_obs <F_Q T_Q,F_Q T_Q>_P with T_Q, C_P, and <T_Q,T_Q>_P fixed by parent representation/norm data.",
            "source_anchor": "NEXT1927_0_primary; UEM1099_0_target",
            "current_status": "TARGET_SHARP",
            "missing_for_claim": "parent-signed T_Q owner, fixed charge lattice, unique gauge inner product, no independent F_Q^2 owner",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEM1928_1_chain_rule",
            "claim_piece": "alpha vertical derivative vanishes under owner signature",
            "mathematical_statement": "If e_eff, F_Q^2 normalization, and readout factors descend through q or fixed representation data, Dq[v_X]=0 gives b_alpha=Lie_v ln alpha_EM=0.",
            "source_anchor": "UEM1099_1_chain_rule; TQT1100_0_exact_conditional",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "owner/readout clauses must be signed rather than chosen by convention",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEM1928_2_counterterm",
            "claim_piece": "hidden scalar gauge-kinetic counterterm",
            "mathematical_statement": "DeltaS=-(1/4)int f_X(Xhat)F_Q^2 creates Lie_v ln g_EM^-2 even when q is fixed.",
            "source_anchor": "UEM1099_2_counterterm; CX1099_1_fX; Z1100_2_hidden_counterterm",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "missing_for_claim": "operator-domain exhaustion, product/sequester theorem, exact shift theorem, and radiative closure",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEM1928_3_lambda_counterterm",
            "claim_piece": "independent visible Maxwell normalization",
            "mathematical_statement": "lambda_A F_Q^2 is a legal independent visible kinetic counterterm unless the parent visible-operator domain forbids it.",
            "source_anchor": "CX1099_0_lambda_A; TQT1100_3_lambda_countermodel; Z1100_1_constant_counterterm",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "missing_for_claim": "unique parent curvature subblock and no independent observed F_Q^2 owner",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEM1928_4_radiative_readout",
            "claim_piece": "alpha readout/radiative closure",
            "mathematical_statement": "Even tree-level no-extra-F2 is insufficient unless loops, thresholds, clocks, and readout maps preserve the same parent owner.",
            "source_anchor": "EXC1099_5_radiative; CX1099_2_readout; TQS1100_5_readout_radiative_guard",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "missing_for_claim": "renormalized/readout alpha map must factor only through q or fixed representation data",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEM1928_5_verdict",
            "claim_piece": "1928 no-extra-F2 verdict",
            "mathematical_statement": "unique EM kinetic owner/no-extra-F2 would imply b_alpha=0, but current MTS does not yet derive the owner signature or exclude legal counterterms.",
            "source_anchor": "UEM1928_1_chain_rule through UEM1928_4_radiative_readout",
            "current_status": "NO_EXTRA_F2_THEOREM_NOT_PROMOTED_ALPHA_ROWS_STAGED",
            "missing_for_claim": "T_Q owner, fixed norm/level, no-extra-F2 domain exhaustion, current owner, and radiative/readout closure",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def exclusion_rows() -> list[dict[str, Any]]:
    specs = [
        ("EXC1928_0_diffeomorphism", "diffeomorphism covariance", "f_X(Xhat)F_Q^2", "DOES_NOT_FORBID", "term is a scalar density if Xhat is a scalar/local representative"),
        ("EXC1928_1_U1_gauge", "visible U(1) gauge invariance", "f_X(Xhat)F_Q^2", "DOES_NOT_FORBID", "F_Q^2 is gauge invariant and scalar coefficients are allowed"),
        ("EXC1928_2_unit_rescaling", "unit convention", "alpha_EM variation", "FORBIDDEN_AS_PROOF", "alpha_EM is dimensionless; unit choices cannot remove physical variation"),
        ("EXC1928_3_exact_shift", "exact hidden shift symmetry", "non-derivative f_X(Xhat)F_Q^2", "WOULD_FORBID_IF_PARENT_SIGNED", "current profile/projection branch has not proved exact shift survives"),
        ("EXC1928_4_product_functor", "visible-hidden product/sequester functor", "all hidden-visible coefficient maps", "WOULD_FORBID_IF_PARENT_SIGNED", "strong route, but parent product/sequester remains unsigned"),
        ("EXC1928_5_radiative", "radiative/readout closure", "loop/readout induced alpha coefficient", "UNSIGNED", "tree-level no-extra-F2 is insufficient without closure"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "principle": principle,
            "operator_tested": operator,
            "result": result,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for audit_id, principle, operator, result, reason in specs
    ]


def alpha_rows() -> list[dict[str, Any]]:
    specs = [
        ("ALP1928_0_theorem_zero_candidate", "b_alpha", "0_if_UEM1928_theorem_signed_else_MISSING", "dimensionless vertical derivative", "UEM1928_5_verdict", "THEOREM_ZERO_NOT_SIGNED", "clock;WEP;R10;EM"),
        ("ALP1928_1_clock_product_bound", "abs(b_alpha*tau_clock_time)", "2.1000000000000000e-18", "yr^-1", "ASR1099_1_clock_product", "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM", "clock"),
        ("ALP1928_2_WEP_alpha_product_target", "abs(P_WEP_alpha)", "4.7977805227320001e-05", "dimensionless", "ASR1099_2_WEP_alpha_product_target; DWP1094_3_direct_product_bound", "SOURCE_BACKED_TARGET_NONCLAIM", "MICROSCOPE_WEP"),
        ("ALP1928_3_DD_alpha_threshold", "abs(c_alpha_DD)", "8.3202449332435330e-10", "dimensionless", "ASR1099_3_DD_alpha_threshold; FCP1927_0_c_alpha_DD", "THRESHOLD_ONLY_NO_MTS_COEFFICIENT", "WEP;clock;R10;EM"),
        ("ALP1928_4_R10_projection", "P_R10_alpha(lambda)", "MISSING_KX_BETA_SOURCE_BETA_TEST_TAU_R10", "dimensionless", "ASR1099_4_R10_projection", "R10_PROJECTION_INPUTS_MISSING", "R10_short_range"),
        ("ALP1928_5_total_alpha_norm", "Z_A", "C_P N_Q + lambda_A + f_X + delta_lambda_rad + readout", "symbolic normalization ledger", "Z1100_4_total", "FINITE_BRANCH_RETAINED", "clock;WEP;R10;EM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "value_or_bound": value,
            "units": units,
            "source_anchor": source_anchor,
            "status": status,
            "observable_arenas": arenas,
            "usable_as_standalone_alpha": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for row_id, quantity, value, units, source_anchor, status, arenas in specs
    ]


def tq_signature_rows() -> list[dict[str, Any]]:
    specs = [
        ("TQI1928_0_parent_TQ_object", "T_Q is a parent-action object, not post-readout EM label", "PARTIAL_TEMPLATE_ONLY", "TQS1100_0_parent_TQ_object"),
        ("TQI1928_1_fixed_charge_lattice", "charge labels live in fixed compact representation lattice", "PARTIAL_INTEGER_LABELS_BASE_UNIT_UNSIGNED", "TQS1100_1_fixed_charge_lattice"),
        ("TQI1928_2_fixed_generator_norm", "fibre norm N_Q=<T_Q,T_Q>_P is fixed and nonrescalable", "NOT_PARENT_SIGNED", "TQS1100_2_fixed_generator_norm"),
        ("TQI1928_3_unique_curvature_norm", "observed F_Q^2 is the only Maxwell kinetic subblock", "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "TQS1100_3_unique_curvature_norm"),
        ("TQI1928_4_same_current_owner", "matter current normalization is Noether current of same T_Q owner", "NOT_PARENT_SIGNED", "TQS1100_4_same_current_owner"),
        ("TQI1928_5_readout_radiative_guard", "readout and effective action preserve same parent owner", "UNSIGNED", "TQS1100_5_readout_radiative_guard"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": input_id,
            "required_signature": required,
            "current_status": status,
            "source_anchor": source_anchor,
            "status_policy": "required before b_alpha=0 can be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for input_id, required, status, source_anchor in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1928_0_no_extra_F2",
            "requirement": "no-extra-F2 theorem forces b_alpha=0",
            "status": "FAIL_THEOREM_NOT_PROMOTED",
            "evidence": "UEM1928_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1928_1_counterterms",
            "requirement": "lambda_A F_Q^2 and f_X(Xhat)F_Q^2 are excluded",
            "status": "FAIL_COUNTEREXAMPLES_RETAINED",
            "evidence": "UEM1928_2_counterterm; UEM1928_3_lambda_counterterm",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1928_2_standalone_alpha",
            "requirement": "standalone b_alpha or c_alpha is zero/bounded as an MTS prediction",
            "status": "FAIL_STANDALONE_ALPHA_MISSING",
            "evidence": "ALP1928_0_theorem_zero_candidate; ALP1928_3_DD_alpha_threshold",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1928_3_WEP_R10_transfer",
            "requirement": "clock alpha bound transfers to WEP/R10",
            "status": "FAIL_TRANSFER_INPUTS_MISSING",
            "evidence": "ALP1928_2_WEP_alpha_product_target; ALP1928_4_R10_projection",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1928_4_local_claims",
            "requirement": "alpha sector supports local-GR/WEP/R10/clock claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1928_0_no_extra_F2; CG1928_1_counterterms; CG1928_2_standalone_alpha; CG1928_3_WEP_R10_transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1928_0_no_extra_F2_result",
            "decision": "NO_EXTRA_F2_THEOREM_NOT_PROMOTED",
            "why": "ordinary covariance and U(1) gauge invariance do not forbid f_X F^2; exact shift/product sequester and radiative/readout closure remain unsigned",
            "next_action": "derive a parent T_Q/gauge-norm signature or keep alpha products finite and nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1928_1_alpha_rows_result",
            "decision": "ALPHA_COEFFICIENT_ROWS_STAGED_NONCLAIM",
            "why": "clock/WEP/DD thresholds exist, but no standalone MTS alpha coefficient or theorem-zero exists",
            "next_action": "use rows as private gates only until alpha owner is derived or externally sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1928_2_next_route",
            "decision": "MOVE_TO_PARENT_TQ_GAUGE_NORM_SIGNATURE",
            "why": "the missing alpha owner is now specifically T_Q object, fixed charge lattice, nonrescalable gauge norm, unique F2 domain, current owner, and readout guard",
            "next_action": "1929 should derive parent T_Q owner/fixed charge lattice/gauge norm signature or keep alpha product rows finite",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1928_0_primary",
            "selection_status": "selected",
            "target_doc": "1929-Y5-R2FR-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
            "target_script": "scripts/Y5_R2FR_parent_TQ_owner_fixed_charge_lattice_and_gauge_norm_signature_1929.py",
            "objective": "derive the parent charge-generator owner, fixed charge lattice, and single gauge-norm signature needed for the no-extra-F2 theorem; otherwise keep b_alpha/product rows finite and nonclaim",
            "success_condition": "parent-signed T_Q object, nonrescalable norm/level, unique F2 subblock, same current owner, and readout/radiative guard",
            "do_not": "do not use compact U1 alone as alpha proof, unit rescaling, standalone b_alpha from clock products, or WEP/R10 transfer without tau/source maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1928_0_gain",
            "area": "alpha coupling route",
            "summary": "1928 proves the easy exclusions are not enough: covariance and U(1) gauge invariance permit f_X F^2, so alpha needs a stronger parent owner theorem.",
            "status": "COUNTERTERM_OBSTRUCTION_SHARP",
            "what_it_means": "alpha cannot be killed by convention or ordinary gauge symmetry",
            "next": "parent T_Q/gauge-norm signature",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1928_1_safety",
            "area": "test discipline",
            "summary": "Alpha rows remain product-level and nonclaim: clock product, WEP threshold, DD threshold, and R10 projection are not promoted to standalone b_alpha.",
            "status": "NONCLAIM_ALPHA_ROWS_ONLY",
            "what_it_means": "no clock-to-WEP/R10 transfer without source/tau maps",
            "next": "derive T_Q owner or source alpha coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "em_owner_audit": em_owner_audit_rows(),
        "exclusion_audit": exclusion_rows(),
        "alpha_rows": alpha_rows(),
        "tq_signature_inputs": tq_signature_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
    }


def copy_branch_artifacts() -> None:
    for source, destination in BRANCH_COPIES:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = parse_csv(OUTPUTS["source_register"])
    rows.append({"validation_id": "VAL1928_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    audit = parse_csv(OUTPUTS["em_owner_audit"])
    verdict = next(row for row in audit if row["audit_id"] == "UEM1928_5_verdict")
    rows.append({"validation_id": "VAL1928_01_no_extra_F2_verdict", "status": "PASS" if verdict["current_status"] == "NO_EXTRA_F2_THEOREM_NOT_PROMOTED_ALPHA_ROWS_STAGED" and all(row["proof_pass"] == "False" for row in audit) else "FAIL", "detail": "no-extra-F2 theorem not promoted", "valid_for_claim": False, "claim_allowed": False})
    exclusions = parse_csv(OUTPUTS["exclusion_audit"])
    rows.append({"validation_id": "VAL1928_02_exclusion_audit", "status": "PASS" if any(row["result"] == "DOES_NOT_FORBID" for row in exclusions) and any(row["result"] == "FORBIDDEN_AS_PROOF" for row in exclusions) else "FAIL", "detail": "ordinary covariance/U1 fail and unit-rescaling forbidden as proof", "valid_for_claim": False, "claim_allowed": False})
    alpha = parse_csv(OUTPUTS["alpha_rows"])
    numeric_values = [row["value_or_bound"] for row in alpha if row["value_or_bound"] in {"2.1000000000000000e-18", "4.7977805227320001e-05", "8.3202449332435330e-10"}]
    numeric_ok = all(float(value) > 0 for value in numeric_values)
    rows.append({"validation_id": "VAL1928_03_alpha_rows", "status": "PASS" if len(alpha) == 6 and len(numeric_values) == 3 and numeric_ok and all(row["valid_prediction_row"] == "False" for row in alpha) else "FAIL", "detail": "six alpha rows staged with three numeric nonclaim bounds and no valid prediction rows", "valid_for_claim": False, "claim_allowed": False})
    tq = parse_csv(OUTPUTS["tq_signature_inputs"])
    rows.append({"validation_id": "VAL1928_04_TQ_inputs", "status": "PASS" if len(tq) == 6 and any(row["current_status"] == "NOT_PARENT_SIGNED" for row in tq) and any(row["current_status"] == "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL" for row in tq) else "FAIL", "detail": "TQ/gauge norm input pack remains unsigned", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(row for row in gates if row["gate_id"] == "CG1928_4_local_claims")
    rows.append({"validation_id": "VAL1928_05_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL", "detail": "alpha local/WEP/R10/clock claim remains blocked", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1928_06_decision", "status": "PASS" if any(row["decision"] == "MOVE_TO_PARENT_TQ_GAUGE_NORM_SIGNATURE" for row in decisions) else "FAIL", "detail": "parent TQ/gauge-norm route selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1928_07_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1929-Y5-R2FR-parent-TQ-owner") else "FAIL", "detail": "1929 parent TQ owner target selected", "valid_for_claim": False, "claim_allowed": False})
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = True
    claim_safe = True
    for path in generated:
        try:
            parsed = parse_csv(path)
            csv_ok = csv_ok and bool(parsed)
            for row in parsed:
                if row.get("valid_for_claim", "False") != "False" or row.get("claim_allowed", "False") != "False":
                    claim_safe = False
        except Exception:
            csv_ok = False
    rows.append({"validation_id": "VAL1928_08_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1928_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1928_10_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1928_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1928-") or "_1928" in path.name or "1928_" in path.name or "Y5_R2FR_unique_EM" in path.name)
    rows.append({"validation_id": "VAL1928_12_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1928_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL1928_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1928 unique EM kinetic owner no-extra-F2 theorem or alpha coefficient source row", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1928 - Unique EM Kinetic Owner No-Extra-F2 Theorem Or Alpha Coefficient Source Row

## Purpose

This checkpoint attacks the alpha coupling leg. It tries to prove that the electromagnetic kinetic term has one parent owner, so no hidden scalar `f_X(Xhat)F_Q^2` or independent `lambda_A F_Q^2` can generate alpha variation. If that theorem is not parent-signed, it keeps alpha product/source rows nonclaim.

## Result

- The owner-signature theorem remains exact as a conditional: if `T_Q`, the gauge norm, the current owner, and readout closure are fixed parent data, then `b_alpha=0`.
- Ordinary diffeomorphism covariance and visible `U(1)` gauge invariance do not forbid `f_X(Xhat)F_Q^2`.
- Unit rescaling is explicitly forbidden as an alpha proof because alpha is dimensionless.
- Alpha rows are staged as nonclaim: clock product, WEP target, DD threshold, R10 projection, and full alpha-normalization ledger.
- The next target is the parent `T_Q` owner, fixed charge lattice, and gauge-norm signature.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## EM Owner No-Extra-F2 Audit

{markdown_table(rows_by_name["em_owner_audit"])}

## No-Extra-F2 Exclusion Ledger

{markdown_table(rows_by_name["exclusion_audit"])}

## Alpha Coefficient Rows

{markdown_table(rows_by_name["alpha_rows"])}

## TQ Signature Input Pack

{markdown_table(rows_by_name["tq_signature_inputs"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["snapshot"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
