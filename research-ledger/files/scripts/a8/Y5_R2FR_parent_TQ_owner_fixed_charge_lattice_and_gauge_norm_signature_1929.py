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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1929"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1929-Y5-R2FR-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1928_next": OUT / "P8_Y5_PARENT_QLOC_1928_NEXT_TARGET.csv",
    "1928_doc": ROOT / "1928-Y5-R2FR-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
    "1928_validation": OUT / "P8_Y5_BRR545_1928_VALIDATION.csv",
    "1928_alpha_rows": OUT / "P8_Y5_PARENT_QLOC_1928_ALPHA_COEFFICIENT_ROWS_NONCLAIM.csv",
    "1100_tq_theorem": OUT / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
    "1100_tq_signature": OUT / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
    "1100_decomposition": OUT / "P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv",
    "1100_claims": OUT / "P8_Y5_R10_1100_CLAIM_GATES.csv",
    "1100_validation": OUT / "P8_Y5_BRR545_1100_VALIDATION.csv",
    "1101_theorem": OUT / "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv",
    "1101_candidates": OUT / "P8_Y5_R10_1101_GAUGE_NORM_OWNER_CANDIDATE_AUDIT.csv",
    "1101_no_go": OUT / "P8_Y5_R10_1101_COUPLING_QUANTIZATION_NO_GO_LEDGER.csv",
    "1101_alpha_route": OUT / "P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv",
    "1101_predictions": OUT / "P8_Y5_R10_1101_ALPHA_PRODUCT_PREDICTION_NONCLAIM.csv",
    "1101_bounds": OUT / "P8_Y5_R10_1101_ALPHA_PRODUCT_BOUND_IMPORT.csv",
    "1101_claims": OUT / "P8_Y5_R10_1101_CLAIM_GATES.csv",
    "1101_next": OUT / "P8_Y5_R10_1101_NEXT_TARGET.csv",
}

NEEDLES = {
    "1928_next": ["NEXT1928_0_primary", "parent charge-generator owner"],
    "1928_doc": ["STAT1928_0_gain", "VAL1928_OVERALL"],
    "1928_validation": ["VAL1928_OVERALL", "PASS"],
    "1928_alpha_rows": ["ALP1928_5_total_alpha_norm", "FINITE_BRANCH_RETAINED"],
    "1100_tq_theorem": ["TQT1100_0_exact_conditional", "TQT1100_4_verdict"],
    "1100_tq_signature": ["TQS1100_0_parent_TQ_object", "TQS1100_6_verdict"],
    "1100_decomposition": ["Z1100_0_parent_piece", "Z1100_4_total"],
    "1100_claims": ["CG1100_0_TQ_signature", "CG1100_2_finite_products"],
    "1100_validation": ["V1100_SUMMARY", "pass"],
    "1101_theorem": ["GFT1101_4_verdict", "GAUGE_NORM_OWNER_NOT_DERIVED"],
    "1101_candidates": ["GNO1101_0_fixed_fibre_metric", "GNO1101_6_unification_embedding"],
    "1101_no_go": ["NG1101_0_compact_U1", "NG1101_4_minimal_action"],
    "1101_alpha_route": ["ROUTE1101_2_finite_alpha_products", "BEST_IMMEDIATE_TEST_DISCIPLINE_ROUTE"],
    "1101_predictions": ["PRED1101_0_clock_alpha_missing_tau", "PRED1101_2_c_alpha_missing"],
    "1101_bounds": ["BOUND1101_0_clock_product", "BOUND1101_2_c_alpha_DD_threshold"],
    "1101_claims": ["CG1101_0_gauge_norm_owner", "CG1101_3_product_runner"],
    "1101_next": ["NEXT1101_0_1102", "alpha-product-first-input-fill"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1929_SOURCE_REGISTER.csv",
    "tq_signature_audit": OUT / "P8_Y5_PARENT_QLOC_1929_TQ_GAUGE_NORM_SIGNATURE_AUDIT.csv",
    "candidate_ledger": OUT / "P8_Y5_PARENT_QLOC_1929_GAUGE_OWNER_CANDIDATE_LEDGER.csv",
    "no_go_ledger": OUT / "P8_Y5_PARENT_QLOC_1929_COUPLING_QUANTIZATION_NO_GO_LEDGER.csv",
    "alpha_fallback": OUT / "P8_Y5_PARENT_QLOC_1929_ALPHA_PRODUCT_FALLBACK_ROWS_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1929_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1929_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1929_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1929_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1929_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["tq_signature_audit"], SOURCE_WEIGHT_DOCS / "TQ_GAUGE_NORM_SIGNATURE_AUDIT_1929_NONCLAIM.csv"),
    (OUTPUTS["alpha_fallback"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1929_ALPHA_PRODUCT_FALLBACK_ROWS_NONCLAIM.csv"),
    (OUTPUTS["alpha_fallback"], QUEUE / "JR1929_ALPHA_PRODUCT_FIRST_INPUT_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1929_CLAIM_GATE.csv"),
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
                "needed_for": "1929 parent TQ owner fixed charge lattice and gauge norm signature",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def tq_signature_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQS1929_0_exact_conditional",
            "claim_piece": "T_Q signature implies vertical alpha silence",
            "mathematical_statement": "If T_Q, N_Q, C_P, the charge lattice, current owner, and readout factors are fixed parent data, then D_v(C_P N_Q)=D_v n_A=D_v readout=0 and Dq[v]=0 gives b_alpha=0.",
            "source_anchor": "TQT1100_0_exact_conditional; GFT1101_0_target",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "signature clauses are not all parent-signed",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQS1929_1_compact_U1_limit",
            "claim_piece": "compact U1 fixed charge lattice",
            "mathematical_statement": "Compact U1 can fix relative integer labels n_A, but not the base unit Q_* or continuous Maxwell kinetic coefficient g_EM.",
            "source_anchor": "TQT1100_1_compact_U1_limit; NG1101_0_compact_U1",
            "current_status": "PARTIAL_SUCCESS_WITH_COUPLING_GAP",
            "obstruction": "charge quantization is not coupling quantization",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQS1929_2_rescaling_countermodel",
            "claim_piece": "missing norm owner",
            "mathematical_statement": "If N_Q is not parent-fixed, T_Q -> sT_Q can be compensated by A_Q/current/charge-label normalization, leaving the observed form but no unique alpha owner.",
            "source_anchor": "TQT1100_2_rescaling_countermodel; GFT1101_2_Ward_limit",
            "current_status": "COUNTERMODEL_RETAINED",
            "obstruction": "nonrescalable parent fibre norm is absent",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQS1929_3_lambda_countermodel",
            "claim_piece": "independent Maxwell kinetic counterterm",
            "mathematical_statement": "Even if C_P N_Q exists, S -> S - lambda_A/4 int F_Q^2 gives Z_A=C_P N_Q+lambda_A unless the parent visible-operator domain forbids independent F_Q^2.",
            "source_anchor": "TQT1100_3_lambda_countermodel; Z1100_1_constant_counterterm",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "obstruction": "operator-domain exhaustion/no-extra-F2 remains unsigned",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQS1929_4_signature_pack",
            "claim_piece": "parent T_Q/gauge-norm signature clauses",
            "mathematical_statement": "Need parent T_Q object, fixed charge lattice/base unit, fixed generator norm, unique curvature norm, same current owner, and readout/radiative guard.",
            "source_anchor": "TQS1100_0_parent_TQ_object through TQS1100_6_verdict",
            "current_status": "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED",
            "obstruction": "fixed lattice partial support exists, but norm, no-extra-F2, current owner, and readout/radiative guard remain unsigned",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQS1929_5_verdict",
            "claim_piece": "1929 parent T_Q/gauge-norm verdict",
            "mathematical_statement": "The parent T_Q owner, fixed charge lattice, and gauge-norm signature needed for no-extra-F2 are not derived in the current corpus.",
            "source_anchor": "TQS1929_0_exact_conditional through TQS1929_4_signature_pack",
            "current_status": "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED_ALPHA_PRODUCTS_RETAINED",
            "obstruction": "all candidate routes are conditional, label-only, current-only, or outside current corpus",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def candidate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GNO1929_0_fixed_fibre_metric", "fixed parent gauge-fibre metric", "would fix N_Q=<T_Q,T_Q>_P as nonrescalable parent data", "WOULD_WORK_IF_PARENT_DERIVED", "current corpus has norm analogies/contracts but no EM fibre metric source"),
        ("GNO1929_1_topological_level", "topological/Kac-Moody-like level", "would fix coefficient or generator norm entering g_EM^-2", "NO_EM_LEVEL_SOURCE", "level work targets memory/amplitude, not EM gauge-fibre norm"),
        ("GNO1929_2_Dirac_monopole", "monopole/Dirac quantization", "would constrain electric-magnetic charge products", "DOES_NOT_FIX_ELECTRIC_COUPLING_ALONE", "no parent monopole sector, magnetic unit, or gauge norm exists"),
        ("GNO1929_3_anomaly_cancellation", "anomaly/representation cancellation", "would constrain ordinary charge relations", "CHARGE_RELATIONS_ONLY_CURRENTLY", "does not supply continuous U1 kinetic coefficient"),
        ("GNO1929_4_Ward_identity", "Ward/Noether current normalization", "would own current normalization relative to transformation", "CURRENT_OWNER_SUPPORT_NOT_KINETIC_OWNER", "Maxwell kinetic coefficient remains rescalable without norm/level"),
        ("GNO1929_5_phase_current", "compact phase-current carrier", "would give theta_Q/J_Q parent phase-current and quantized charge unit", "USEFUL_ROUTE_NOT_ALPHA_NORM", "does not yet derive Maxwell kinetic norm or Lorentz/readout"),
        ("GNO1929_6_unification_embedding", "larger simple parent gauge embedding", "would inherit U1 normalization from larger nonabelian/simple parent norm", "NOT_IN_CURRENT_CORPUS", "needs parent group, breaking, running, and no-extra-F2 source"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": candidate_id,
            "candidate_owner": candidate_owner,
            "would_need_to_show": would_need,
            "current_status": status,
            "why_not_enough_now": why_not_enough,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        }
        for candidate_id, candidate_owner, would_need, status, why_not_enough in specs
    ]


def no_go_rows() -> list[dict[str, Any]]:
    specs = [
        ("NG1929_0_compact_U1", "compact U1 implies alpha is fixed", "compactness fixes representation labels after a base unit exists; it does not fix the continuous Maxwell kinetic coefficient", "use compact U1 as partial charge-lattice support only"),
        ("NG1929_1_rank_or_level_analogy", "import k=9/rank/index level as EM gauge norm", "existing level work is not an EM fibre-level theorem and rank is not a Ward identity", "demand an EM-specific differential complex or level source"),
        ("NG1929_2_Dirac_product", "Dirac quantization fixes electron charge or alpha", "it fixes a product under assumptions; no parent magnetic charge unit or gauge norm exists here", "treat monopole route as acquisition target, not evidence"),
        ("NG1929_3_Ward_current", "current conservation fixes the EM coupling", "current conservation survives rescaling of F2 coefficient and current units unless a common norm owner forbids it", "use Ward identity to own J_Q only, then separately prove kinetic norm"),
        ("NG1929_4_minimal_action", "write only parent F2 and set lambda_A=0 by minimality", "absence in a draft action is not operator-domain exhaustion; lambda_A and f_X F2 remain legal", "derive no-extra-F2 theorem or retain counterterm branch"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "no_go_id": no_go_id,
            "tempting_shortcut": shortcut,
            "why_rejected": why,
            "safe_replacement": replacement,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for no_go_id, shortcut, why, replacement in specs
    ]


def alpha_fallback_rows() -> list[dict[str, Any]]:
    specs = [
        ("AFP1929_0_clock_alpha_missing_tau", "clock", "P_clock_alpha", "MISSING_B_ALPHA_TAU_CLOCK_OR_GAUGE_NORM_ZERO", "yr^-1", "BOUND1101_0_clock_product", "2.1000000000000000e-18", "gauge norm theorem-zero or numeric b_alpha*tau_clock_time prediction"),
        ("AFP1929_1_WEP_alpha_missing_projection", "MICROSCOPE_WEP", "P_WEP_alpha", "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP", "dimensionless", "BOUND1101_1_WEP_alpha_product", "4.7977805227320001e-05", "beta_source_alpha; b_alpha or zero theorem; tau_WEP; material map"),
        ("AFP1929_2_c_alpha_missing", "MICROSCOPE_WEP", "c_alpha_DD", "MISSING_SOURCE_BACKED_C_ALPHA_OR_GAUGE_OWNER_ZERO", "dimensionless", "BOUND1101_2_c_alpha_DD_threshold", "8.3202449332435330e-10", "source-backed c_alpha_DD value or derived gauge norm zero"),
        ("AFP1929_3_total_alpha_norm", "alpha_normalization", "Z_A", "C_P N_Q + lambda_A + f_X + delta_lambda_rad + readout", "symbolic", "Z1100_4_total", "FINITE_BRANCH_RETAINED", "show nonparent terms vanish and parent piece is fixed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "prediction_id": prediction_id,
            "arena": arena,
            "product_symbol": symbol,
            "product_value": value,
            "product_units": units,
            "bound_source_row": bound_source_row,
            "bound_or_status": bound_or_status,
            "required_inputs": required,
            "derivation_status": "MISSING_MTS_PRODUCT_PREDICTION" if value.startswith("MISSING") else "FINITE_ALPHA_LEDGER_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for prediction_id, arena, symbol, value, units, bound_source_row, bound_or_status, required in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1929_0_TQ_signature",
            "requirement": "parent T_Q/gauge-norm signature is derived",
            "status": "FAIL_TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED",
            "evidence": "TQS1929_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1929_1_compactness",
            "requirement": "compact U1/charge quantization fixes alpha",
            "status": "FAIL_COUPLING_GAP_RETAINED",
            "evidence": "TQS1929_1_compact_U1_limit; NG1929_0_compact_U1",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1929_2_candidates",
            "requirement": "level/index/monopole/Ward/phase/unification route supplies gauge norm",
            "status": "FAIL_ALL_CANDIDATES_UNSIGNED_OR_INSUFFICIENT",
            "evidence": "GNO1929_0_fixed_fibre_metric through GNO1929_6_unification_embedding",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1929_3_alpha_products",
            "requirement": "finite alpha product predictions are score-ready",
            "status": "FAIL_VALID_PREDICTION_ROWS_ZERO",
            "evidence": "AFP1929_0_clock_alpha_missing_tau through AFP1929_2_c_alpha_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1929_4_local_alpha_claim",
            "requirement": "alpha sector supports local-GR/WEP/R10/clock claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1929_0_TQ_signature; CG1929_1_compactness; CG1929_2_candidates; CG1929_3_alpha_products",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1929_0_TQ_signature_result",
            "decision": "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED",
            "why": "compact U1 gives label support but not coupling normalization; fixed norm, unique F2 domain, current owner, and readout/radiative guard remain unsigned",
            "next_action": "do not claim b_alpha=0; keep alpha on finite product route",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1929_1_candidate_result",
            "decision": "GAUGE_NORM_OWNER_CANDIDATES_INSUFFICIENT",
            "why": "fixed fibre metric would work if derived, but level/index/monopole/Ward/anomaly/phase-current/unification routes do not yet fix the Maxwell kinetic norm",
            "next_action": "treat these as acquisition targets, not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1929_2_next_route",
            "decision": "MOVE_TO_ALPHA_PRODUCT_FIRST_INPUT_FILL",
            "why": "the derivation route is open but not currently supported; the most disciplined progress is to fill one finite alpha product input set without transfer shortcuts",
            "next_action": "1930 should derive tau_clock/Xhat normalization or WEP beta_source_alpha/tau_WEP/material projection",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1929_0_primary",
            "selection_status": "selected",
            "target_doc": "1930-Y5-R2FR-alpha-product-first-input-fill-tau-clock-Xhat-or-WEP-beta-source.md",
            "target_script": "scripts/Y5_R2FR_alpha_product_first_input_fill_tau_clock_Xhat_or_WEP_beta_source_1930.py",
            "objective": "fill the first scoreable finite-alpha product input set by deriving tau_clock/Xhat normalization or WEP beta_source_alpha/tau_WEP/material projection, while keeping claims blocked unless every input is numeric and source-backed",
            "success_condition": "one runner-valid alpha product row with real sourced inputs, or a precise blocker ledger naming the first missing input",
            "do_not": "do not use compact U1 as alpha proof, standalone b_alpha, clock-to-WEP transfer, tau=1 shortcut, invented coefficients, or local-GR/WEP/R10 claims",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1929_0_gain",
            "area": "EM alpha owner",
            "summary": "1929 separates charge quantization from coupling quantization: compact U1 supports integer labels, but does not fix the Maxwell kinetic norm.",
            "status": "COUPLING_GAP_EXPLICIT",
            "what_it_means": "alpha cannot be theorem-zeroed without a parent gauge norm or level/index/fibre metric owner",
            "next": "finite alpha product input fill",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1929_1_route",
            "area": "testing discipline",
            "summary": "The derivation route remains open, but the immediate robust route is to make one alpha product scoreable without transfer shortcuts.",
            "status": "FINITE_PRODUCT_ROUTE_SELECTED",
            "what_it_means": "we move from owner theorem hunting to filling tau/source/material inputs",
            "next": "tau_clock/Xhat or WEP beta-source projection",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "tq_signature_audit": tq_signature_audit_rows(),
        "candidate_ledger": candidate_rows(),
        "no_go_ledger": no_go_rows(),
        "alpha_fallback": alpha_fallback_rows(),
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
    rows.append({"validation_id": "VAL1929_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    audit = parse_csv(OUTPUTS["tq_signature_audit"])
    verdict = next(row for row in audit if row["audit_id"] == "TQS1929_5_verdict")
    rows.append({"validation_id": "VAL1929_01_TQ_signature", "status": "PASS" if verdict["current_status"] == "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED_ALPHA_PRODUCTS_RETAINED" and all(row["proof_pass"] == "False" for row in audit) else "FAIL", "detail": "TQ/gauge-norm signature not derived", "valid_for_claim": False, "claim_allowed": False})
    candidates = parse_csv(OUTPUTS["candidate_ledger"])
    rows.append({"validation_id": "VAL1929_02_candidates", "status": "PASS" if len(candidates) == 7 and any(row["current_status"] == "WOULD_WORK_IF_PARENT_DERIVED" for row in candidates) and any(row["current_status"] == "NOT_IN_CURRENT_CORPUS" for row in candidates) else "FAIL", "detail": "seven gauge-owner candidates retained as nonclaim", "valid_for_claim": False, "claim_allowed": False})
    no_go = parse_csv(OUTPUTS["no_go_ledger"])
    rows.append({"validation_id": "VAL1929_03_no_go", "status": "PASS" if len(no_go) == 5 and any(row["no_go_id"] == "NG1929_0_compact_U1" for row in no_go) and any(row["no_go_id"] == "NG1929_4_minimal_action" for row in no_go) else "FAIL", "detail": "five shortcut no-go rows retained", "valid_for_claim": False, "claim_allowed": False})
    alpha = parse_csv(OUTPUTS["alpha_fallback"])
    numeric_bounds = [row["bound_or_status"] for row in alpha if row["bound_or_status"] in {"2.1000000000000000e-18", "4.7977805227320001e-05", "8.3202449332435330e-10"}]
    numeric_ok = all(float(value) > 0 for value in numeric_bounds)
    rows.append({"validation_id": "VAL1929_04_alpha_fallback", "status": "PASS" if len(alpha) == 4 and len(numeric_bounds) == 3 and numeric_ok and all(row["valid_prediction_row"] == "False" for row in alpha) else "FAIL", "detail": "alpha fallback rows staged with no valid prediction rows", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(row for row in gates if row["gate_id"] == "CG1929_4_local_alpha_claim")
    rows.append({"validation_id": "VAL1929_05_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL", "detail": "alpha local/clock/WEP/R10 claim remains blocked", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1929_06_decision", "status": "PASS" if any(row["decision"] == "MOVE_TO_ALPHA_PRODUCT_FIRST_INPUT_FILL" for row in decisions) else "FAIL", "detail": "alpha product input-fill route selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1929_07_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1930-Y5-R2FR-alpha-product") else "FAIL", "detail": "1930 alpha product first-input target selected", "valid_for_claim": False, "claim_allowed": False})
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
    rows.append({"validation_id": "VAL1929_08_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1929_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1929_10_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1929_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1929-") or "_1929" in path.name or "1929_" in path.name or "Y5_R2FR_parent_TQ" in path.name)
    rows.append({"validation_id": "VAL1929_12_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1929_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL1929_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1929 parent TQ owner fixed charge lattice and gauge norm signature", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1929 - Parent TQ Owner Fixed Charge Lattice And Gauge Norm Signature

## Purpose

This checkpoint asks whether the electromagnetic charge generator `T_Q`, charge lattice, and Maxwell gauge norm are genuinely parent-owned. If the answer is yes, the no-extra-F2 theorem can kill `b_alpha`; if not, alpha must stay on the finite product route.

## Result

- The `T_Q`/gauge-norm theorem is exact as a conditional, but not promoted.
- Compact `U(1)` supports relative integer charge labels, but does not fix the continuous Maxwell kinetic coefficient.
- Ward/current, monopole, level/index, anomaly, phase-current, and unification routes are useful candidates or acquisition targets, not current alpha proofs.
- Alpha product fallback rows remain nonclaim with no valid prediction rows.
- The next target is first-input filling for finite alpha products: `tau_clock/Xhat` or WEP `beta_source_alpha/tau_WEP/material` projection.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## TQ Gauge-Norm Signature Audit

{markdown_table(rows_by_name["tq_signature_audit"])}

## Gauge Owner Candidate Ledger

{markdown_table(rows_by_name["candidate_ledger"])}

## Coupling Quantization No-Go Ledger

{markdown_table(rows_by_name["no_go_ledger"])}

## Alpha Product Fallback Rows

{markdown_table(rows_by_name["alpha_fallback"])}

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
