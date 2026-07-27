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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1923"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1923-Y5-R2FR-parent-operator-domain-no-hidden-visible-hom-or-residual-prior-pack.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1922_next": OUT / "P8_Y5_PARENT_QLOC_1922_NEXT_TARGET.csv",
    "1922_doc": ROOT / "1922-Y5-R2FR-EM-hidden-F2-unique-owner-or-finite-alpha-row.md",
    "1912_axioms": OUT / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
    "1913_typing": OUT / "P8_Y5_PARENT_QLOC_1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
    "1049_rule": OUT / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
    "1049_symmetry": OUT / "P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
    "1049_priors": OUT / "P8_Y5_R10_1049_RESIDUAL_PRIOR_SLOTS.csv",
    "1050_product": OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
    "1050_obstructions": OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv",
    "1051_no_mixed": OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
    "1051_scalar": OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
    "1091_theorem": OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
    "1091_obstructions": OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_OBSTRUCTION_LEDGER.csv",
    "1091_finite": OUT / "P8_Y5_R10_1091_FINITE_RESIDUAL_ROUTE_MAP.csv",
    "1091_claims": OUT / "P8_Y5_R10_1091_CLAIM_GATES.csv",
    "1091_validation": OUT / "P8_Y5_BRR545_1091_VALIDATION.csv",
}

NEEDLES = {
    "1922_next": ["NEXT1922_0_primary", "parent operator-domain/no-hidden-visible-hom"],
    "1922_doc": ["NEXT1922_0_primary", "VAL1922_OVERALL"],
    "1912_axioms": ["AX1912_6_no_shadow_hidden_hom", "MISSING_AXIOM_NOT_ADOPTED"],
    "1913_typing": ["QTM1913_5_no_hidden_hom", "MISSING_AXIOM_NOT_ADOPTED"],
    "1049_rule": ["OCR1049_5_verdict", "FAIL_CURRENT_CLAIM_RESIDUAL_PRIORS_REQUIRED"],
    "1049_symmetry": ["SBT1049_0_diffeomorphism_covariance", "SBT1049_5_radiative_readout_closure"],
    "1049_priors": ["RP1049_0_b_alpha", "RP1049_5_qbar_constants_abs_prior"],
    "1050_product": ["PFT1050_5_verdict", "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED"],
    "1050_obstructions": ["OBS1050_0_scalar_invariant", "OBS1050_4_radiative_readout"],
    "1051_no_mixed": ["NMM1051_5_verdict", "FAIL_CURRENT_CLAIM_FIRST_PRIOR_CHAIN_REQUIRED"],
    "1051_scalar": ["ISO1051_0_hidden_scalar_I", "ISO1051_3_domain_marker"],
    "1091_theorem": ["ODH1091_6_verdict", "THEOREM_NOT_DERIVED_CURRENT_CORPUS"],
    "1091_obstructions": ["OBS1091_0_invariant_scalar", "OBS1091_4_readout_regeneration"],
    "1091_finite": ["FR1091_0_b_alpha", "FR1091_5_qbar_source_label"],
    "1091_claims": ["CG1091_0_operator_domain", "CG1091_1_MOMS"],
    "1091_validation": ["V1091_1_theorem_not_derived", "V1091_SUMMARY"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1923_SOURCE_REGISTER.csv",
    "proof_audit": OUT / "P8_Y5_PARENT_QLOC_1923_OPERATOR_DOMAIN_NO_HIDDEN_VISIBLE_PROOF_AUDIT.csv",
    "obstruction_ledger": OUT / "P8_Y5_PARENT_QLOC_1923_HIDDEN_INVARIANT_OBSTRUCTION_LEDGER.csv",
    "prior_pack": OUT / "P8_Y5_PARENT_QLOC_1923_RESIDUAL_PRIOR_PACK_NONCLAIM.csv",
    "guard": OUT / "P8_Y5_PARENT_QLOC_1923_NO_SHORTCUT_GUARD.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1923_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1923_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1923_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1923_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1923_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["proof_audit"], SOURCE_WEIGHT_DOCS / "OPERATOR_DOMAIN_NO_HIDDEN_VISIBLE_PROOF_AUDIT_1923_NONCLAIM.csv"),
    (OUTPUTS["prior_pack"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1923_RESIDUAL_PRIOR_PACK_NONCLAIM.csv"),
    (OUTPUTS["prior_pack"], QUEUE / "JR1923_RESIDUAL_PRIOR_PACK_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1923_CLAIM_GATE.csv"),
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
                "needed_for": "1923 parent operator-domain no-hidden-visible-hom or residual-prior pack",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ODH1923_0_target",
            "claim_piece": "parent operator-domain/no-hidden-visible-hom theorem",
            "formal_statement": "Hom(C_hid,Coeff(O_vis)) is absent or constant for visible EM, mass, source, and clock operators before fitting.",
            "current_status": "TARGET_SHARP",
            "source_anchor": "NEXT1922_0_primary; ODH1091_0_target; NMM1051_0_target",
            "missing_for_claim": "parent operator-domain construction and hidden invariant algebra classification",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ODH1923_1_trivial_invariant_algebra",
            "claim_piece": "hidden invariant algebra triviality",
            "formal_statement": "If O(C_hid)^inv=R, then every hidden-to-visible scalar coefficient is constant.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "source_anchor": "ODH1091_1_trivial_invariant_algebra; NMM1051_1_trivial_hidden_algebra_case",
            "missing_for_claim": "proof that the active MTS hidden/local sector has no nonconstant invariant scalar",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ODH1923_2_scalar_counterexample",
            "claim_piece": "surviving scalar obstruction",
            "formal_statement": "If I_hid is invariant and dI_hid is nonzero, c_I=c0+epsilon I_hid gives a natural visible coefficient map.",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "source_anchor": "ODH1091_2_scalar_obstruction; NMM1051_2_scalar_counterexample; ISO1051_0_hidden_scalar_I",
            "missing_for_claim": "scalar no-hair/triviality, exact shift, or parent product-sequester theorem",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ODH1923_3_symmetry_limits",
            "claim_piece": "ordinary symmetry insufficiency",
            "formal_statement": "Diffeomorphism covariance and visible gauge invariance allow scalar coefficients such as f_X F_Q^2 and m_A(X) psi_bar psi.",
            "current_status": "INSUFFICIENT_SYMMETRY",
            "source_anchor": "ODH1091_3_symmetry_limits; SBT1049_0_diffeomorphism_covariance; SBT1049_1_gauge_invariance",
            "missing_for_claim": "stronger shift/sequester/product-domain theorem",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ODH1923_4_product_functor_limit",
            "claim_piece": "product functor/sequester route",
            "formal_statement": "Visible action as a q-pullback plus hidden sector product would forbid mixed coefficient maps if parent-signed and stable under readout.",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_anchor": "PFT1050_5_verdict; ODH1091_4_product_functor_limit",
            "missing_for_claim": "parent product category, source label-forgetting, and radiative/readout closure",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ODH1923_5_verdict",
            "claim_piece": "1923 operator-domain verdict",
            "formal_statement": "The parent operator-domain/no-hidden-visible-hom theorem is not derived in the current corpus; finite residual priors remain live.",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_PRIOR_PACK_STAGED",
            "source_anchor": "ODH1923_1_trivial_invariant_algebra through ODH1923_4_product_functor_limit",
            "missing_for_claim": "hidden invariant triviality, parent product/sequester, source label-forgetting, and radiative/readout closure",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    specs = [
        ("OBS1923_0_invariant_scalar", "nonconstant hidden invariant scalar", "I_hid -> f_X(I_hid)F_Q^2 or m_A(I_hid)psi_bar psi", "O(C_hid)^inv=R, exact shift/no-hair, or product functor parent signature"),
        ("OBS1923_1_alpha_owner", "visible EM normalization owner unsigned", "g_EM or alpha_EM as independent visible coefficient", "parent charge-generator norm/topological level plus radiative closure"),
        ("OBS1923_2_matter_spectrum", "ordinary matter spectrum/constants not parent-owned", "m_A(I), y_A(I), B_A(I), Lambda_QCD(I)", "parent matter category plus fixed representation/superselection theorem"),
        ("OBS1923_3_source_labels", "source-label forgetting not parent-signed", "F((T_A,A))=kappa_A T_A", "parent source functor to total Hilbert source before species labels"),
        ("OBS1923_4_readout_regeneration", "radiative/effective/readout re-entry", "loop-induced f_X F^2 or clock readout X dependence", "effective-action/readout functor closure or retained source-backed priors"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": obstruction_id,
            "obstruction": obstruction,
            "example": example,
            "needed_to_kill": needed,
            "status": "LIVE_NONCLAIM_OBSTRUCTION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for obstruction_id, obstruction, example, needed in specs
    ]


def prior_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("RPP1923_0_b_alpha", "b_alpha", "EM/gauge kinetic/readout alpha channel", "MISSING_PRIOR_WIDTH_OR_THEOREM_ZERO", "clock;WEP;R10;EM spectra"),
        ("RPP1923_1_b_mu", "b_mu", "dimensionless mass-ratio coefficient", "MISSING_MASS_RATIO_PRIOR_OR_THEOREM_ZERO", "clock;WEP;composition"),
        ("RPP1923_2_b_mA", "b_mA", "material/species mass and binding response", "MISSING_COMPOSITION_MATRIX_OR_THEOREM_ZERO", "WEP;R10;Newton_GM;clock"),
        ("RPP1923_3_b_nuc", "b_nuc", "nuclear/QCD/electromagnetic binding response", "MISSING_NUCLEAR_SENSITIVITY_PRIOR", "WEP;R10;clock"),
        ("RPP1923_4_b_clock_i", "b_clock_i", "direct clock/readout coefficient not already alpha/mass/nuclear", "MISSING_CLOCK_READOUT_MODEL", "clock comparison;redshift/LPI"),
        ("RPP1923_5_qbar_source_label", "qbar_source_label", "source/species label leakage", "MISSING_LABEL_FORGETTING_OR_SOURCE_WEIGHT_PRIOR", "WEP;R10;source_charge"),
        ("RPP1923_6_lambda_F2", "lambda_F2", "independent hidden-visible F_Q^2 counterterm", "MISSING_NO_EXTRA_F2_OR_NUMERIC_COEFFICIENT", "clock;WEP;R10;EM"),
        ("RPP1923_7_qbar_constants_abs", "qbar_constants_abs_prior", "absolute no-cancellation envelope across constant/source/readout couplings", "MISSING_COMPONENT_PRIORS", "WEP;R10;clock;PPN;local_GR"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, definition, value, links in specs:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "symbol": symbol,
                "residual_definition": definition,
                "candidate_value": value,
                "prior_shape": "log_abs_or_theorem_zero" if "abs" not in symbol else "sum_abs_components_no_cancellation",
                "source_path": "MISSING_PARENT_THEOREM_OR_SOURCE_BACKED_PRIOR",
                "source_row_id": "MISSING_SOURCE_ROW_ID",
                "required_inputs": "parent theorem-zero or numeric prior width; Xhat normalization; arena projection; no-cancellation policy",
                "observable_links": links,
                "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def guard_rows() -> list[dict[str, Any]]:
    guards = [
        ("G1923_0_covariance", "use diffeomorphism covariance to ban hidden-visible coefficients", "FORBIDDEN_COVARIANT_SCALAR_COEFFICIENTS_EXIST"),
        ("G1923_1_gauge", "use visible gauge invariance to ban scalar gauge kinetic functions", "FORBIDDEN_GAUGE_INVARIANCE_ALLOWS_F2"),
        ("G1923_2_minimality", "omit mixed operators from a draft action and call them impossible", "FORBIDDEN_MINIMALITY_NOT_OPERATOR_DOMAIN"),
        ("G1923_3_product_axiom", "adopt product functor/sequester as if parent-derived", "FORBIDDEN_CLOSURE_ONLY_UNLESS_SIGNED"),
        ("G1923_4_readout", "ignore EFT/readout re-entry after bare-action sequester", "FORBIDDEN_RADIATIVE_READOUT_CLOSURE_UNSIGNED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "forbidden_move": move,
            "policy": policy,
            "reason": "operator-domain silence must be derived from the parent category/action, not inferred from aesthetic absence",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for guard_id, move, policy in guards
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1923_0_operator_domain",
            "requirement": "no-hidden-visible-hom theorem parent-derived",
            "status": "FAIL_SCALAR_OBSTRUCTION_SURVIVES",
            "evidence": "ODH1923_2_scalar_counterexample; ODH1923_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1923_1_prior_pack",
            "requirement": "residual priors are source-backed or theorem-zero",
            "status": "FAIL_ROWS_SCHEMA_ONLY",
            "evidence": "RPP1923_0_b_alpha through RPP1923_7_qbar_constants_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1923_2_guard",
            "requirement": "shortcuts refused",
            "status": "PASS_GUARD_ONLY",
            "evidence": "G1923_0_covariance through G1923_4_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1923_3_local_tests",
            "requirement": "operator-domain route supports local-GR/WEP/R10/clock scoring",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1923_0_operator_domain; CG1923_1_prior_pack",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1923_0_theorem_result",
            "decision": "OPERATOR_DOMAIN_THEOREM_NOT_DERIVED",
            "why": "hidden invariant scalar obstruction survives and product/radiative closure are unsigned",
            "next_action": "retain residual-prior pack as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1923_1_prior_pack",
            "decision": "RESIDUAL_PRIOR_PACK_STAGED_NONCLAIM",
            "why": "eight live coefficient families now have source-ready rows and no-cancellation status",
            "next_action": "no scoring until theorem-zero or numeric/source-backed widths exist",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1923_2_next_route",
            "decision": "MOVE_TO_HIDDEN_INVARIANT_TRIVIALITY",
            "why": "the no-hidden-visible theorem reduces to whether the active hidden/local sector has nonconstant invariants",
            "next_action": "1924 should try O(C_hid)^inv=R, exact shift/no-hair, or profile-zero theorem; otherwise retain scalar prior rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1923_0_primary",
            "selection_status": "selected",
            "target_doc": "1924-Y5-R2FR-hidden-invariant-algebra-triviality-or-scalar-prior-rows.md",
            "target_script": "scripts/Y5_R2FR_hidden_invariant_algebra_triviality_or_scalar_prior_rows_1924.py",
            "objective": "try to prove the hidden/local invariant algebra is trivial, or that exact shift/no-hair/profile-zero removes scalar coefficient maps; otherwise stage scalar-prior rows",
            "success_condition": "O(C_hid)^inv=R or equivalent parent-signed theorem closes the scalar obstruction, or scalar prior rows preserve every surviving invariant channel",
            "do_not": "do not assume product sequestering, Xhat=0, exact shift, or no-hair unless signed by the current parent/local branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1923_0_gain",
            "area": "operator-domain theorem",
            "summary": "1923 shows the shared coupling theorem is exact as a target but currently blocked by surviving hidden invariant scalars.",
            "status": "BOXED_WITH_PRIOR_PACK",
            "what_it_means": "this is a high-leverage bottleneck, not a dead end",
            "next": "hidden invariant algebra triviality",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1923_1_safety",
            "area": "claim discipline",
            "summary": "covariance, gauge invariance, minimality, product axiom, and bare-action sequestering shortcuts are refused.",
            "status": "SHORTCUT_GUARD_ACTIVE",
            "what_it_means": "we do not smuggle local GR or EM-lock through missing operator assumptions",
            "next": "prove invariant triviality or source priors",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1923_2_next",
            "area": "derivation strategy",
            "summary": "The next best attack is hidden invariant algebra triviality, because it would remove the scalar counterexample at the root.",
            "status": "NEXT_ATTACK_SELECTED",
            "what_it_means": "we move from operator-domain contract to the actual algebraic obstruction",
            "next": "1924 hidden invariant algebra",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "proof_audit": proof_audit_rows(),
        "obstruction_ledger": obstruction_rows(),
        "prior_pack": prior_pack_rows(),
        "guard": guard_rows(),
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
    rows.append({"validation_id": "VAL1923_00_sources", "status": "PASS" if all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    proof = parse_csv(OUTPUTS["proof_audit"])
    verdict = next(r for r in proof if r["audit_id"] == "ODH1923_5_verdict")
    rows.append({"validation_id": "VAL1923_01_proof_audit", "status": "PASS" if verdict["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_PRIOR_PACK_STAGED" and all(r["proof_pass"] == "False" for r in proof) else "FAIL", "detail": "operator-domain theorem remains unsigned", "valid_for_claim": False, "claim_allowed": False})
    obstructions = parse_csv(OUTPUTS["obstruction_ledger"])
    rows.append({"validation_id": "VAL1923_02_obstructions", "status": "PASS" if len(obstructions) == 5 and all(r["status"] == "LIVE_NONCLAIM_OBSTRUCTION" for r in obstructions) else "FAIL", "detail": "hidden invariant obstruction ledger retained", "valid_for_claim": False, "claim_allowed": False})
    priors = parse_csv(OUTPUTS["prior_pack"])
    rows.append({"validation_id": "VAL1923_03_prior_pack", "status": "PASS" if len(priors) == 8 and all(r["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" and r["valid_for_claim"] == "False" for r in priors) else "FAIL", "detail": "eight residual-prior schemas staged as nonclaim", "valid_for_claim": False, "claim_allowed": False})
    guards = parse_csv(OUTPUTS["guard"])
    rows.append({"validation_id": "VAL1923_04_guard", "status": "PASS" if len(guards) == 5 and all(r["status"] == "ACTIVE" for r in guards) else "FAIL", "detail": "operator-domain shortcuts forbidden", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(r for r in gates if r["gate_id"] == "CG1923_3_local_tests")
    rows.append({"validation_id": "VAL1923_05_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL", "detail": "operator-domain route supports no scoring claim", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1923_06_decision", "status": "PASS" if any(r["decision"] == "MOVE_TO_HIDDEN_INVARIANT_TRIVIALITY" for r in decisions) else "FAIL", "detail": "hidden invariant algebra route selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1923_07_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1924-Y5-R2FR-hidden-invariant") else "FAIL", "detail": "1924 hidden invariant algebra route selected", "valid_for_claim": False, "claim_allowed": False})
    generated = [p for k, p in OUTPUTS.items() if k != "validation"]
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
    rows.append({"validation_id": "VAL1923_08_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1923_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1923_10_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1923_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1923-") or "_1923" in path.name or "1923_" in path.name or "Y5_R2FR_parent_operator_domain" in path.name)
    rows.append({"validation_id": "VAL1923_12_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1923_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append({"validation_id": "VAL1923_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1923 parent operator-domain no-hidden-visible-hom or residual-prior pack", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("\n", " ").replace("|", "\\|") for h in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1923 - Parent Operator-Domain No-Hidden-Visible-Hom Or Residual-Prior Pack

## Purpose

This checkpoint attacks the shared coupling bottleneck: derive a parent operator-domain/no-hidden-visible-hom theorem forbidding hidden/local variables from feeding visible EM, mass, source-weight, and clock coefficients, or stage a residual-prior pack without claiming a pass.

## Result

- The theorem target is exact and high leverage.
- It is not derived in the current corpus because a nonconstant hidden invariant scalar remains a live counterexample.
- Product/sequester and trivial invariant algebra routes are useful but remain unsigned.
- Eight nonclaim residual-prior rows preserve the live coefficient families.
- The next target is hidden invariant algebra triviality, because that is the root obstruction.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Operator-Domain Proof Audit

{markdown_table(rows_by_name["proof_audit"])}

## Hidden Invariant Obstruction Ledger

{markdown_table(rows_by_name["obstruction_ledger"])}

## Residual-Prior Pack

{markdown_table(rows_by_name["prior_pack"])}

## No-Shortcut Guard

{markdown_table(rows_by_name["guard"])}

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
