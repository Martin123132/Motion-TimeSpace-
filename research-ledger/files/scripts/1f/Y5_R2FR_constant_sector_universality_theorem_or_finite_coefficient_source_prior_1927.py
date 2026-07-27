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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1927"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1927-Y5-R2FR-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1926_next": OUT / "P8_Y5_PARENT_QLOC_1926_NEXT_TARGET.csv",
    "1926_doc": ROOT / "1926-Y5-R2FR-direct-WEP-product-source-pack-or-parent-Xhat-action-clause.md",
    "1926_validation": OUT / "P8_Y5_BRR545_1926_VALIDATION.csv",
    "1926_source_pack": OUT / "P8_Y5_PARENT_QLOC_1926_DIRECT_WEP_SOURCE_PACK_NONCLAIM.csv",
    "1097_theorem": OUT / "P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
    "1097_channels": OUT / "P8_Y5_R10_1097_CONSTANT_CHANNEL_AUDIT.csv",
    "1097_requirements": OUT / "P8_Y5_R10_1097_SOURCE_PRIOR_REQUIREMENTS.csv",
    "1097_validation": OUT / "P8_Y5_BRR545_1097_VALIDATION.csv",
    "1097_next": OUT / "P8_Y5_R10_1097_NEXT_TARGET.csv",
    "1098_owner": OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
    "1098_vertices": OUT / "P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv",
    "1098_theorem": OUT / "P8_Y5_R10_1098_ACTION_SIGNATURE_THEOREM.csv",
    "1098_requirements": OUT / "P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
    "1098_claims": OUT / "P8_Y5_R10_1098_CLAIM_GATES.csv",
    "1098_next": OUT / "P8_Y5_R10_1098_NEXT_TARGET.csv",
}

NEEDLES = {
    "1926_next": ["NEXT1926_0_primary", "constant-sector"],
    "1926_doc": ["STAT1926_1_missing", "VAL1926_OVERALL"],
    "1926_validation": ["VAL1926_OVERALL", "PASS"],
    "1926_source_pack": ["DSP1926_4_parent_coefficient_vector", "MISSING_PARENT_COEFFICIENT_VECTOR"],
    "1097_theorem": ["CSU1097_5_verdict", "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED"],
    "1097_channels": ["CHA1097_0_alpha", "CHA1097_5_species_constants"],
    "1097_requirements": ["FSR1097_0_parent_owner", "FSR1097_3_no_cancellation"],
    "1097_validation": ["V1097_SUMMARY", "pass"],
    "1097_next": ["NEXT1097_0_1098", "ordinary-constant owner"],
    "1098_owner": ["OCS1098_6_verdict", "OWNER_ACTION_SIGNATURE_NOT_DERIVED"],
    "1098_vertices": ["FV1098_1_scalar_F2", "FV1098_6_source_weight_X"],
    "1098_theorem": ["OCT1098_1_chain_rule", "OWNER_THEOREM_NOT_PROMOTED"],
    "1098_requirements": ["REQ1098_0_c_alpha", "REQ1098_2_c_common"],
    "1098_claims": ["CG1098_0_owner_signature", "CG1098_1_source_prior"],
    "1098_next": ["NEXT1098_0_1099", "unique EM kinetic owner"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1927_SOURCE_REGISTER.csv",
    "universality_audit": OUT / "P8_Y5_PARENT_QLOC_1927_CONSTANT_SECTOR_UNIVERSALITY_AUDIT.csv",
    "channel_ledger": OUT / "P8_Y5_PARENT_QLOC_1927_CONSTANT_CHANNEL_LEDGER.csv",
    "finite_priors": OUT / "P8_Y5_PARENT_QLOC_1927_FINITE_COEFFICIENT_PRIOR_ROWS_NONCLAIM.csv",
    "forbidden_vertices": OUT / "P8_Y5_PARENT_QLOC_1927_FORBIDDEN_VERTEX_REQUIREMENT_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1927_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1927_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1927_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1927_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1927_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["universality_audit"], SOURCE_WEIGHT_DOCS / "CONSTANT_SECTOR_UNIVERSALITY_AUDIT_1927_NONCLAIM.csv"),
    (OUTPUTS["finite_priors"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1927_FINITE_COEFFICIENT_PRIOR_ROWS_NONCLAIM.csv"),
    (OUTPUTS["finite_priors"], QUEUE / "JR1927_FINITE_COEFFICIENT_SOURCE_PRIOR_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1927_CLAIM_GATE.csv"),
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
                "needed_for": "1927 constant-sector universality theorem or finite coefficient source prior",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def universality_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSU1927_0_target",
            "claim_piece": "ordinary constant-sector universality",
            "mathematical_statement": "For every local vertical v in ker(Dq), Lie_v theta_A=0 for alpha, mass ratios, binding fractions, clock standards, source weights, and material response coefficients.",
            "source_anchor": "NEXT1926_0_primary; CSU1097_0_target",
            "current_status": "TARGET_SHARP",
            "proof_or_obstruction": "would theorem-zero the direct WEP coefficient vector c_I and upstream clock/R10 constant coefficients",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSU1927_1_descent_superselection",
            "claim_piece": "sufficient descent/superselection criterion",
            "mathematical_statement": "If theta_A(Phi)=theta_bar_A(q(Phi)) or theta_A is fixed discrete representation data, then Dq[v]=0 implies Lie_v theta_A=0.",
            "source_anchor": "CSU1097_1_descent_superselection; OCT1098_1_chain_rule",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "chain rule is solid, but the parent action has not signed the descent/superselection premise",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSU1927_2_dimensionless_guard",
            "claim_piece": "unit-rescaling guard",
            "mathematical_statement": "Lie_v ln alpha_EM, mass ratios, binding fractions, and clock ratios are dimensionless observables and cannot all be removed by units.",
            "source_anchor": "CSU1097_2_dimensionless_guard",
            "current_status": "PHYSICS_GUARD_PROVED",
            "proof_or_obstruction": "prevents sweeping constant drift into unit convention",
            "proof_pass": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSU1927_3_counterexample",
            "claim_piece": "hidden scalar coefficient counterexample",
            "mathematical_statement": "q(Phi) fixed but theta_A=theta_0 exp(epsilon I_hid) gives Lie_v theta_A != 0 if I_hid survives.",
            "source_anchor": "CSU1097_3_counterexample; OCS1098_1_unique_EM_owner",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "proof_or_obstruction": "metric descent alone does not forbid independent hidden-visible constant vertices",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSU1927_4_radiative_readout_closure",
            "claim_piece": "bare-action silence survives effective/readout reduction",
            "mathematical_statement": "Bare constant-sector silence must survive S_eff, counterterms, clocks, readout maps, and source-weight projections.",
            "source_anchor": "CSU1097_4_readout_radiative; OCS1098_5_radiative_readout_closure",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "proof_or_obstruction": "bare theorem cannot yet be promoted to observed WEP/clock/R10 silence",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSU1927_5_owner_signature",
            "claim_piece": "ordinary constant owner action signature",
            "mathematical_statement": "Parent action must forbid f_X F^2, m_A(Xhat), y_A(Xhat), binding response slots, clock readout slots, and source-only weights.",
            "source_anchor": "OCS1098_6_verdict; FV1098_1_scalar_F2 through FV1098_6_source_weight_X",
            "current_status": "OWNER_ACTION_SIGNATURE_NOT_DERIVED",
            "proof_or_obstruction": "forbidden vertices are still legal in current corpus unless an owner signature is added",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSU1927_6_verdict",
            "claim_piece": "1927 constant-sector universality verdict",
            "mathematical_statement": "ordinary constants/response coefficients are parent superselection data independent of hidden invariants",
            "source_anchor": "CSU1927_1_descent_superselection through CSU1927_5_owner_signature",
            "current_status": "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED_FINITE_PRIORS_STAGED",
            "proof_or_obstruction": "alpha owner, mass spectrum, binding response, source weights, species constants, hidden scalar, and radiative/readout closure remain unsigned",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def channel_ledger_rows() -> list[dict[str, Any]]:
    specs = [
        ("CH1927_0_alpha", "alpha_EM/gauge kinetic normalization", "b_alpha or c_alpha_DD", "RETAIN_FINITE_BRANCH", "unique EM kinetic owner and no-extra-F2 theorem unsigned", "clock;WEP;R10;EM spectra"),
        ("CH1927_1_mass_ratios", "mass ratios/Yukawa/Higgs sector", "b_mu,b_mA", "RETAIN_FINITE_BRANCH", "parent matter spectrum and material sensitivity theorem missing", "WEP;clock;R10;composition"),
        ("CH1927_2_QCD_binding", "QCD/nuclear/binding fractions", "b_nuc,c_surface_DD", "RETAIN_FINITE_BRANCH", "binding fractions are dimensionless and not unit-removable", "WEP;clock;nuclear spectra"),
        ("CH1927_3_clock", "clock transition ratios", "b_clock_i", "INHERITS_UPSTREAM_DEBT", "clock rows inherit alpha/mass/nuclear debts and tau_clock projection", "clock comparisons;redshift/LPI"),
        ("CH1927_4_source_weights", "source normalization/species weights", "kappa_A(Xhat),w_A(Xhat),qbar_source_weight", "RETAIN_FINITE_BRANCH", "one universal Hilbert source/current owner is not parent-signed", "WEP;Newton_GM;R10;PPN"),
        ("CH1927_5_species_constants", "species charge/constant labels", "theta_A(I_hid)", "NOT_UNIVERSALIZED", "GEN1092_5 species-constant generator debt survives", "WEP;clock;source charge"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "channel_id": channel_id,
            "constant_sector_channel": channel,
            "coefficient_symbol": coefficient,
            "current_status": status,
            "why_not_zero": why,
            "observable_arenas": arenas,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for channel_id, channel, coefficient, status, why, arenas in specs
    ]


def finite_prior_rows() -> list[dict[str, Any]]:
    specs = [
        ("FCP1927_0_c_alpha_DD", "c_alpha_DD", "8.3202449332435330e-10", "THR1095_0_alpha; PRI1096_0_alpha; REQ1098_0_c_alpha", "clock;WEP;R10;EM", "MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO"),
        ("FCP1927_1_c_surface_DD", "c_surface_DD", "6.9875016461438634e-11", "THR1095_1_surface; PRI1096_1_surface; REQ1098_1_c_surface", "WEP;clock;nuclear", "MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO"),
        ("FCP1927_2_c_common_abs", "c_common_abs_if_single_combined_scale", "6.4461422294339073e-11", "THR1095_2_combined_abs; PRI1096_2_common_abs; REQ1098_2_c_common", "WEP material vector", "MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO"),
        ("FCP1927_3_b_mu_mass_ratio", "b_mu_or_b_mA", "MISSING_THRESHOLD_OR_SOURCE", "CHA1097_1_mass_ratios", "WEP;clock;R10;composition", "MISSING_PARENT_MATTER_SPECTRUM_OR_SOURCE_PRIOR"),
        ("FCP1927_4_b_nuc_binding", "b_nuc_or_b_binding", "MISSING_THRESHOLD_OR_SOURCE", "CHA1097_2_QCD_binding", "WEP;clock;nuclear", "MISSING_BINDING_OWNER_OR_SOURCE_PRIOR"),
        ("FCP1927_5_b_clock_effective", "b_clock_i", "MISSING_CLOCK_PROJECTION_SOURCE", "CHA1097_3_clock", "clock comparisons;redshift/LPI", "MISSING_EFFECTIVE_READOUT_CLOSURE"),
        ("FCP1927_6_source_weight", "qbar_source_weight_or_kappa_A", "MISSING_SOURCE_WEIGHT_BOUND", "CHA1097_4_source_weights", "WEP;Newton_GM;R10;PPN", "MISSING_COMMON_HILBERT_SOURCE_OWNER"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "prior_id": prior_id,
            "coefficient": coefficient,
            "threshold_abs_or_placeholder": threshold,
            "source_anchor": source_anchor,
            "observable_arenas": arenas,
            "current_status": current_status,
            "source_path": "MISSING_EXTERNAL_COEFFICIENT_SOURCE_OR_PARENT_THEOREM",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "promotion_rule": "requires parent derivation, exact theorem-zero, or external source-backed coefficient value; threshold alone is not a prediction",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for prior_id, coefficient, threshold, source_anchor, arenas, current_status in specs
    ]


def forbidden_vertex_rows() -> list[dict[str, Any]]:
    specs = [
        ("FV1927_0_scalar_F2", "EM", "f_X(Xhat)F_Q^2 or lambda_A F_Q^2", "b_alpha,c_alpha", "FORBIDDEN_REQUIRED_BUT_CURRENTLY_LEGAL", "unique EM kinetic owner/no-extra-F2 theorem"),
        ("FV1927_1_mass_X", "matter", "m_A(Xhat) psi_bar_A psi_A", "b_mA", "FORBIDDEN_REQUIRED_BUT_CURRENTLY_LEGAL", "parent matter spectrum owner"),
        ("FV1927_2_yukawa_X", "matter", "y_A(Xhat) psi_A H psi_B", "b_mu,b_mA", "FORBIDDEN_REQUIRED_BUT_CURRENTLY_LEGAL", "parent Yukawa/Higgs owner"),
        ("FV1927_3_binding_X", "nuclear/binding", "Lambda_QCD(Xhat), B_A(Xhat), nuclear response slot", "b_nuc,c_surface", "FORBIDDEN_REQUIRED_BUT_CURRENTLY_LEGAL", "binding/QCD response owner"),
        ("FV1927_4_clock_readout_X", "clock/readout", "nu_i(Xhat), readout_X, Hodge/readout leakage", "b_clock_i", "FORBIDDEN_REQUIRED_BUT_CURRENTLY_LEGAL", "clock/readout descent and closure"),
        ("FV1927_5_source_weight_X", "source/WEP", "w_A(Xhat), kappa_A(Xhat), source-only material multiplier", "qbar_source,c_WEP", "FORBIDDEN_REQUIRED_BUT_CURRENTLY_LEGAL", "common Hilbert source/current owner"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "vertex_id": vertex_id,
            "sector": sector,
            "operator_or_slot": operator,
            "coefficient": coefficient,
            "current_status": status,
            "needed_owner_signature": needed,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for vertex_id, sector, operator, coefficient, status, needed in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1927_0_descent_theorem",
            "requirement": "constant-sector descent/superselection premise signed by parent action",
            "status": "FAIL_PREMISE_NOT_PARENT_SIGNED",
            "evidence": "CSU1927_1_descent_superselection; CSU1927_6_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1927_1_hidden_scalar_counterexample",
            "requirement": "hidden scalar coefficient counterexample eliminated",
            "status": "FAIL_COUNTEREXAMPLE_RETAINED",
            "evidence": "CSU1927_3_counterexample",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1927_2_forbidden_vertices",
            "requirement": "all hidden-visible constant vertices forbidden",
            "status": "FAIL_OWNER_SIGNATURE_NOT_DERIVED",
            "evidence": "FV1927_0_scalar_F2 through FV1927_5_source_weight_X",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1927_3_finite_priors",
            "requirement": "finite coefficient priors are source-backed prediction rows",
            "status": "FAIL_ROWS_SCHEMA_ONLY",
            "evidence": "FCP1927_0_c_alpha_DD through FCP1927_6_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1927_4_WEP_local_claim",
            "requirement": "WEP/local-GR/clock/R10 constant-sector claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1927_0_descent_theorem; CG1927_1_hidden_scalar_counterexample; CG1927_2_forbidden_vertices; CG1927_3_finite_priors",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1927_0_universality_result",
            "decision": "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED",
            "why": "the descent/superselection theorem is exact, but the parent action has not signed the constant-sector owner premises and the hidden scalar counterexample survives",
            "next_action": "retain finite coefficient priors and attack ordinary-constant owner action signature",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1927_1_priors_result",
            "decision": "FINITE_COEFFICIENT_PRIOR_ROWS_STAGED_NONCLAIM",
            "why": "thresholds exist for alpha/surface/common DD combinations, but no source-backed MTS coefficient values exist",
            "next_action": "use thresholds as private gates only; no prediction until coefficient values or zero theorem are sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1927_2_next_route",
            "decision": "MOVE_TO_UNIQUE_EM_KINETIC_OWNER",
            "why": "alpha is the most connected coefficient across clock, WEP, R10, and EM; proving no-extra-F2 would remove one major coupling leg cleanly",
            "next_action": "1928 should derive unique EM kinetic owner/no-extra-F2 or stage a source-backed alpha coefficient row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1927_0_primary",
            "selection_status": "selected",
            "target_doc": "1928-Y5-R2FR-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
            "target_script": "scripts/Y5_R2FR_unique_EM_kinetic_owner_no_extra_F2_theorem_or_alpha_coefficient_source_row_1928.py",
            "objective": "derive the unique EM kinetic owner/no-extra-F2 theorem forcing b_alpha=0, or stage an external source-backed alpha coefficient row against clock/WEP/R10 thresholds",
            "success_condition": "b_alpha=0 theorem from parent gauge normalization and radiative/readout closure, or a source-backed alpha coefficient prediction row",
            "do_not": "do not use unit rescaling of alpha, clock-only screening, tau_WEP=1, unsourced alpha priors, or WEP/local-GR claims",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1927_0_gain",
            "area": "coupling bottleneck",
            "summary": "1927 shows the direct WEP coupling bottleneck is the ordinary constant-sector owner, not merely a missing numeric fit.",
            "status": "BOTTLE_NECK_SHARPENED",
            "what_it_means": "we now know which parent action clauses must kill b_alpha, mass/binding response, source weights, and species constants",
            "next": "unique EM kinetic owner/no-extra-F2",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1927_1_safety",
            "area": "finite coefficient discipline",
            "summary": "Finite coefficient priors are staged only as source-ready schemas; numeric thresholds are not treated as MTS predictions.",
            "status": "NONCLAIM_PRIORS_ONLY",
            "what_it_means": "we avoid pair-cancellation and unsourced coupling priors",
            "next": "source or theorem-zero the alpha coefficient first",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "universality_audit": universality_audit_rows(),
        "channel_ledger": channel_ledger_rows(),
        "finite_priors": finite_prior_rows(),
        "forbidden_vertices": forbidden_vertex_rows(),
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
    rows.append({"validation_id": "VAL1927_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    audit = parse_csv(OUTPUTS["universality_audit"])
    verdict = next(row for row in audit if row["audit_id"] == "CSU1927_6_verdict")
    guard = next(row for row in audit if row["audit_id"] == "CSU1927_2_dimensionless_guard")
    rows.append({"validation_id": "VAL1927_01_universality_verdict", "status": "PASS" if verdict["current_status"] == "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED_FINITE_PRIORS_STAGED" else "FAIL", "detail": "constant-sector universality remains unpromoted", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1927_02_dimensionless_guard", "status": "PASS" if guard["proof_pass"] == "True" and guard["current_status"] == "PHYSICS_GUARD_PROVED" else "FAIL", "detail": "unit-rescaling guard retained as proved physics guard", "valid_for_claim": False, "claim_allowed": False})
    channels = parse_csv(OUTPUTS["channel_ledger"])
    rows.append({"validation_id": "VAL1927_03_channel_ledger", "status": "PASS" if len(channels) == 6 and any(row["current_status"] == "NOT_UNIVERSALIZED" for row in channels) else "FAIL", "detail": "six constant-sector channels remain explicit", "valid_for_claim": False, "claim_allowed": False})
    priors = parse_csv(OUTPUTS["finite_priors"])
    numeric_thresholds = [row for row in priors if row["threshold_abs_or_placeholder"] not in {"MISSING_THRESHOLD_OR_SOURCE", "MISSING_CLOCK_PROJECTION_SOURCE", "MISSING_SOURCE_WEIGHT_BOUND"}]
    numeric_ok = all(float(row["threshold_abs_or_placeholder"]) > 0 for row in numeric_thresholds)
    rows.append({"validation_id": "VAL1927_04_finite_priors", "status": "PASS" if len(priors) == 7 and len(numeric_thresholds) == 3 and numeric_ok and all(row["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" for row in priors) else "FAIL", "detail": "finite coefficient prior rows staged with three numeric thresholds and four missing-source rows", "valid_for_claim": False, "claim_allowed": False})
    vertices = parse_csv(OUTPUTS["forbidden_vertices"])
    rows.append({"validation_id": "VAL1927_05_forbidden_vertices", "status": "PASS" if len(vertices) == 6 and all(row["current_status"] == "FORBIDDEN_REQUIRED_BUT_CURRENTLY_LEGAL" for row in vertices) else "FAIL", "detail": "six forbidden hidden-visible vertex classes remain legal until parent owner signature", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(row for row in gates if row["gate_id"] == "CG1927_4_WEP_local_claim")
    rows.append({"validation_id": "VAL1927_06_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL", "detail": "constant-sector WEP/local/clock/R10 claim blocked", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1927_07_decision", "status": "PASS" if any(row["decision"] == "MOVE_TO_UNIQUE_EM_KINETIC_OWNER" for row in decisions) else "FAIL", "detail": "unique EM kinetic owner selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1927_08_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1928-Y5-R2FR-unique-EM-kinetic") else "FAIL", "detail": "1928 EM owner target selected", "valid_for_claim": False, "claim_allowed": False})
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
    rows.append({"validation_id": "VAL1927_09_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1927_10_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1927_11_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1927_12_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1927-") or "_1927" in path.name or "1927_" in path.name or "Y5_R2FR_constant_sector" in path.name)
    rows.append({"validation_id": "VAL1927_13_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1927_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL1927_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1927 constant-sector universality theorem or finite coefficient source prior", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1927 - Constant-Sector Universality Theorem Or Finite Coefficient Source Prior

## Purpose

This checkpoint attacks the coupling bottleneck directly: prove ordinary constants and response coefficients are parent superselection/descent data independent of hidden invariants, or keep finite coefficient priors nonclaim and source-ready.

## Result

- The descent/superselection theorem is exact as a conditional.
- The unit-rescaling escape is blocked for dimensionless constants and ratios.
- Constant-sector universality is not promoted because hidden scalar coefficient counterexamples and forbidden hidden-visible vertices remain live.
- Seven finite coefficient prior rows are staged as nonclaim, with three numeric threshold gates and four missing-source rows.
- The next target is unique EM kinetic owner/no-extra-F2, because alpha touches clock, WEP, R10, and EM tests.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Constant-Sector Universality Audit

{markdown_table(rows_by_name["universality_audit"])}

## Constant Channel Ledger

{markdown_table(rows_by_name["channel_ledger"])}

## Finite Coefficient Prior Rows

{markdown_table(rows_by_name["finite_priors"])}

## Forbidden Vertex Requirement Ledger

{markdown_table(rows_by_name["forbidden_vertices"])}

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
