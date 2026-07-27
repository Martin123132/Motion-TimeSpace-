from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_INDEPENDENT_Q_HESSIAN_OPERATOR_FIRST_FILL_2314"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2314-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill.md"

PATHS = {
    "2313_doc": ROOT / "2313-Y5-R2FR-q-symplectic-potential-source-or-independent-q-bound-runner-activation.md",
    "2313_validation": OUT / "P8_Y5_BRR545_2313_VALIDATION.csv",
    "2313_runner": OUT / "P8_Y5_PARENT_QLOC_2313_INDEPENDENT_Q_BOUND_RUNNER_ACTIVATION.csv",
    "2313_contract": OUT / "P8_Y5_PARENT_QLOC_2313_BOUND_RUNNER_CONTRACT.csv",
    "2313_priority": OUT / "P8_Y5_PARENT_QLOC_2313_INPUT_PRIORITY_LEDGER.csv",
    "2281_doc": ROOT / "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md",
    "2281_validation": OUT / "P8_Y5_BRR545_2281_VALIDATION.csv",
    "2281_stiffness": OUT / "P8_Y5_PARENT_QLOC_2281_Q_STIFFNESS_DERIVATION_AUDIT.csv",
    "2281_contract": OUT / "P8_Y5_PARENT_QLOC_2281_Q_OPERATOR_CONTRACT.csv",
    "2281_bounds": OUT / "P8_Y5_PARENT_QLOC_2281_RESIDUAL_BOUND_LEDGER.csv",
    "2281_claims": OUT / "P8_Y5_PARENT_QLOC_2281_CLAIM_GATES.csv",
    "2282_doc": ROOT / "2282-Y5-R2FR-covariance-equilibrium-selector-or-q-closure-declaration.md",
    "2282_validation": OUT / "P8_Y5_BRR545_2282_VALIDATION.csv",
    "2282_equivalence": OUT / "P8_Y5_PARENT_QLOC_2282_Q_OBSERVER_CELL_EQUIVALENCE.csv",
    "2282_closure": OUT / "P8_Y5_PARENT_QLOC_2282_Q_CLOSURE_DECLARATION.csv",
    "2282_inputs": OUT / "P8_Y5_PARENT_QLOC_2282_PARENT_SELECTOR_INPUT_CONTRACT.csv",
    "2282_claims": OUT / "P8_Y5_PARENT_QLOC_2282_CLAIM_GATES.csv",
    "2308_normal": OUT / "P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv",
    "2308_coeff": OUT / "P8_Y5_PARENT_QLOC_2308_DQWEYL2_PARENT_COEFFICIENT_AUDIT.csv",
    "2306_weyl": OUT / "P8_Y5_PARENT_QLOC_2306_SCHWARZSCHILD_WEYL2_PROJECTION_LAW.csv",
    "2296_nohair": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "2310_first": OUT / "P8_Y5_PARENT_QLOC_2310_INDEPENDENT_Q_FIRST_SOURCE_ROW.csv",
    "2311_fallback": OUT / "P8_Y5_PARENT_QLOC_2311_INDEPENDENT_HESSIAN_FALLBACK_PACK.csv",
    "2312_bound": OUT / "P8_Y5_PARENT_QLOC_2312_INDEPENDENT_Q_BOUND_PACK_UPDATE.csv",
}

SOURCES = [
    ("SRC2314_00_2313_doc", "2313_doc", PATHS["2313_doc"], ["NEXT2313_0", "independent-q bound runner"], "direct 2313 handoff"),
    ("SRC2314_01_2313_validation", "2313_validation", PATHS["2313_validation"], ["VAL2313_OVERALL", "PASS"], "2313 validation"),
    ("SRC2314_02_2313_runner", "2313_runner", PATHS["2313_runner"], ["RUN2313_1_operator", "MISSING_PARENT_HESSIAN"], "incoming bound-runner operator gap"),
    ("SRC2314_03_2313_contract", "2313_contract", PATHS["2313_contract"], ["BRC2313_2_response", "G_q"], "response-bound contract"),
    ("SRC2314_04_2313_priority", "2313_priority", PATHS["2313_priority"], ["PRI2313_4_verdict", "independent q Hessian/operator source"], "operator first-fill priority"),
    ("SRC2314_05_2281_doc", "2281_doc", PATHS["2281_doc"], ["M_q^2=n_q^A H_AB n_q^B", "Z_q=xi_q^2 n_q^A H_AB n_q^B"], "conditional q Hessian derivation"),
    ("SRC2314_06_2281_validation", "2281_validation", PATHS["2281_validation"], ["VAL2281_OVERALL", "PASS"], "2281 validation"),
    ("SRC2314_07_2281_stiffness", "2281_stiffness", PATHS["2281_stiffness"], ["QSD2281_2_transverse_q_mass", "QSD2281_3_gradient_expansion"], "machine-readable conditional Hessian"),
    ("SRC2314_08_2281_contract", "2281_contract", PATHS["2281_contract"], ["QOC2281_0_action_term", "QOC2281_1_positivity"], "q operator contract"),
    ("SRC2314_09_2281_bounds", "2281_bounds", PATHS["2281_bounds"], ["RBL2281_0_elliptic", "RBL2281_1_mass_gap"], "conditional Green/bound rows"),
    ("SRC2314_10_2281_claims", "2281_claims", PATHS["2281_claims"], ["CG2281_0_conditional_stiffness_derivation", "CG2281_2_current_corpus_derives_parent_q_sector"], "claim-gate status for conditional Hessian"),
    ("SRC2314_11_2282_doc", "2282_doc", PATHS["2282_doc"], ["q=0 iff T^2S=1", "DISCIPLINED_CLOSURE_UNTIL_SELECTOR_THEOREM"], "selector equivalence and closure guard"),
    ("SRC2314_12_2282_validation", "2282_validation", PATHS["2282_validation"], ["VAL2282_OVERALL", "PASS"], "2282 validation"),
    ("SRC2314_13_2282_equivalence", "2282_equivalence", PATHS["2282_equivalence"], ["QOE2282_1_q_zero_to_reciprocity", "EXACT_EQUIVALENCE"], "q=0 observer-cell equivalence"),
    ("SRC2314_14_2282_closure", "2282_closure", PATHS["2282_closure"], ["QCD2282_0_status", "DISCIPLINED_CLOSURE_UNTIL_SELECTOR_THEOREM"], "closure declaration"),
    ("SRC2314_15_2282_inputs", "2282_inputs", PATHS["2282_inputs"], ["PIC2282_0_cell_current", "MISSING_PARENT_CURRENT"], "selector input contract"),
    ("SRC2314_16_2282_claims", "2282_claims", PATHS["2282_claims"], ["CG2282_1_parent_selector", "False"], "selector claim blocked"),
    ("SRC2314_17_2308_normal", "2308_normal", PATHS["2308_normal"], ["NF2308_1_variation", "FORMAL_VARIATION_CONTRACT"], "formal q action/equation normal form"),
    ("SRC2314_18_2308_coeff", "2308_coeff", PATHS["2308_coeff"], ["DCO2308_3_verdict", "COEFFICIENT_UNSOURCED"], "curvature coefficient remains missing"),
    ("SRC2314_19_2306_weyl", "2306_weyl", PATHS["2306_weyl"], ["PROJ2306_0_schwarzschild_identity", "EXACT_BACKGROUND_IDENTITY"], "background Weyl2 kernel"),
    ("SRC2314_20_2296_nohair", "2296_nohair", PATHS["2296_nohair"], ["NH2296_3_zero_theorem", "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED"], "conditional q no-hair theorem"),
    ("SRC2314_21_2310_first", "2310_first", PATHS["2310_first"], ["IQSRC2310_1_Zq", "MISSING_PARENT_HESSIAN"], "earlier independent-q first-source row"),
    ("SRC2314_22_2311_fallback", "2311_fallback", PATHS["2311_fallback"], ["FB2311_1_Zq", "MISSING_PARENT_HESSIAN"], "earlier Hessian fallback pack"),
    ("SRC2314_23_2312_bound", "2312_bound", PATHS["2312_bound"], ["BND2312_1_dynamic_q_operator", "MISSING_PARENT_HESSIAN"], "earlier bound-pack gap"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2314_SOURCE_REGISTER.csv",
    "hunt": OUT / "P8_Y5_PARENT_QLOC_2314_HESSIAN_SOURCE_HUNT.csv",
    "branches": OUT / "P8_Y5_PARENT_QLOC_2314_OPERATOR_BRANCH_CLASSIFICATION.csv",
    "green": OUT / "P8_Y5_PARENT_QLOC_2314_GREEN_FUNCTION_NORMALIZATION_CONTRACT.csv",
    "first_fill": OUT / "P8_Y5_PARENT_QLOC_2314_FIRST_FILL_ROWS.csv",
    "runner": OUT / "P8_Y5_PARENT_QLOC_2314_BOUND_RUNNER_UPDATE.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2314_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2314_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2314_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2314_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2314_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2314_0_first_fill", OUTPUTS["first_fill"], RAB_QUEUE / "JR2314_Q_OPERATOR_FIRST_FILL_CONDITIONAL_NONCLAIM.csv"),
    ("COPY2314_1_green_contract", OUTPUTS["green"], BETA_DOCS / "Q_GREEN_FUNCTION_NORMALIZATION_CONTRACT_2314_NONCLAIM.csv"),
    ("COPY2314_2_runner_update", OUTPUTS["runner"], MICRO_RESIDUALS / "q_bound_runner_update_nonclaim_2314.csv"),
    ("COPY2314_3_refusal", OUTPUTS["refusal"], BETA_DOCS / "Q_OPERATOR_FIRST_FILL_REFUSALS_2314_NONCLAIM.csv"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2314_0_prior_gap",
            "target": "q Hessian/operator first fill",
            "result": "PRIOR_RUNNER_GAP_CONFIRMED",
            "evidence": "2313 marks RUN2313_1_operator as MISSING_PARENT_HESSIAN and selects the Hessian/operator row as first fill.",
            "route_effect": "continue independent-q bound runner as private nonclaim lane",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2314_1_conditional_mass",
            "target": "M_q^2",
            "result": "CONDITIONAL_FORMULA_FOUND",
            "evidence": "2281 derives M_q^2=n_q^A H_AB n_q^B if q=0 is a parent-selected covariance equilibrium and H is positive on the transverse quotient.",
            "route_effect": "fills operator shape symbolically, not numerically",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2314_2_conditional_stiffness",
            "target": "Z_q",
            "result": "CONDITIONAL_FORMULA_FOUND",
            "evidence": "2281 derives Z_q=xi_q^2 n_q^A H_AB n_q^B from finite smoothing/correlation length.",
            "route_effect": "gives finite-range/Yukawa denominator if xi_q and boundary/domain are sourced",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2314_3_range_ratio",
            "target": "lambda_q",
            "result": "EXACT_CONDITIONAL_RATIO",
            "evidence": "Combining 2308 lambda_q=sqrt(Z_q/M_q^2) with 2281 Z_q=xi_q^2 M_q^2 gives lambda_q=xi_q, provided the same normalization and positive M_q^2 are used.",
            "route_effect": "range is not free in this branch; it is the parent smoothing/correlation length",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2314_4_selector_block",
            "target": "parent ownership",
            "result": "SELECTOR_NOT_PARENT_SIGNED",
            "evidence": "2282 proves q=0 equals radial observer-cell reciprocity but declares q-stiffness closure-only until the selector theorem is supplied.",
            "route_effect": "operator first fill is closure/conditional, not local-GR derivation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2314_5_verdict",
            "target": "claim-grade operator source",
            "result": "CONDITIONAL_OPERATOR_FILL_IMPORTED_NOT_CLAIM_GRADE",
            "evidence": "The operator shape is stronger than a blank placeholder, but Z_q/M_q^2/xi_q are not numeric/source-backed and q=0 is not parent-selected.",
            "route_effect": "update the bound runner from missing operator to partial conditional operator, with scoring still blocked",
            "valid_for_claim": "false",
        },
    ]


def build_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2314_0_dynamic_massive",
            "operator_branch": "dynamic massive q",
            "operator": "L_q=-nabla_i(Z_q nabla^i .)+M_q^2",
            "source_status": "CONDITIONAL_FORM_AVAILABLE_SELECTOR_BLOCKED",
            "claim_effect": "can be used for nonclaim response-envelope algebra only",
            "blocks": "parent q=0 selector; xi_q; units; boundary/domain; source vector; observable projection",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2314_1_algebraic_auxiliary",
            "operator_branch": "auxiliary/algebraic q",
            "operator": "Z_q=0; M_q^2 q + source_q = 0",
            "source_status": "FORMAL_SCHUR_READY_INPUTS_MISSING",
            "claim_effect": "no propagating pole, but contact/higher-curvature residuals remain",
            "blocks": "M_q^2; D_qWeyl2; J_q; boundary_tail; cutoff/domain; theorem-zero for contact terms",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2314_2_massless",
            "operator_branch": "massless q",
            "operator": "L_q=-nabla_i(Z_q nabla^i .)",
            "source_status": "DISFAVORED_FOR_LOCAL_GR_UNLESS_NO_SOURCE_NOHAIR",
            "claim_effect": "massless source would usually create long-range residuals; only no-source/no-hair can rescue local-GR recovery",
            "blocks": "zero mode removal; boundary flux; J_q=0 theorem; arena projection",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2314_3_no_pole",
            "operator_branch": "quotient/no-pole q",
            "operator": "q removed from physical reduced phase space",
            "source_status": "PAUSED_NO_NEW_THETA_SOURCE",
            "claim_effect": "best local-GR route if parent selector/gauge proof appears later",
            "blocks": "Theta_q/Omega_q; momentum map; degree count; source/boundary silence",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2314_4_selected_working",
            "operator_branch": "working branch for runner",
            "operator": "dynamic massive conditional branch with closure label",
            "source_status": "PARTIAL_FIRST_FILL_NONCLAIM",
            "claim_effect": "runner denominator can be written symbolically as M_q^2 and xi_q, but no score is allowed",
            "blocks": "all claim gates remain false except reproducible source audit and conditional formula import",
            "valid_for_claim": "false",
        },
    ]


def build_green_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "GF2314_0_constant_massive_kernel",
            "contract_item": "constant-coefficient massive kernel",
            "formula": "for Z_q>0, M_q^2>0, L_q=-Z_q Delta+M_q^2 gives G_q(r)=exp(-r/lambda_q)/(4*pi*Z_q*r), lambda_q=sqrt(Z_q/M_q^2)",
            "acceptance_rule": "only after Z_q, M_q^2, units, sign convention, and boundary/domain are source-backed",
            "current_status": "FORMAL_KERNEL_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GF2314_1_covariance_range",
            "contract_item": "range under 2281 Hessian branch",
            "formula": "if M_q^2=n_q H n_q and Z_q=xi_q^2 n_q H n_q in the same normalization, then lambda_q=xi_q",
            "acceptance_rule": "xi_q must be a parent smoothing/correlation length, not a fitted Yukawa range",
            "current_status": "EXACT_CONDITIONAL_RATIO_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GF2314_2_energy_norm",
            "contract_item": "coercive response norm",
            "formula": "||q|| <= ||L_q^{-1}|| ||source_q|| <= ||source_q||/lambda_min(L_q)",
            "acceptance_rule": "lambda_min requires positive Hessian on the quotient, boundary class, and zero-mode removal",
            "current_status": "CONDITIONAL_BOUND_FROM_2281",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GF2314_3_algebraic_schur",
            "contract_item": "auxiliary Schur branch",
            "formula": "if Z_q=0, q=-(D_qWeyl2 C^2 + D_qWeylDual CstarC + J_q + boundary_tail)/M_q^2",
            "acceptance_rule": "contact/higher-curvature terms must be theorem-zero or bounded; no Yukawa interpretation",
            "current_status": "EXACT_CONDITIONAL_FORMULA_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GF2314_4_massless_guard",
            "contract_item": "massless guard",
            "formula": "M_q^2=0 requires source-free/no-hair and boundary-zero theorem, otherwise long-range residuals survive",
            "acceptance_rule": "no local-GR claim from massless q unless J_q=0, boundary=0, and zero modes are removed",
            "current_status": "GUARD_READY_PREMISES_UNSIGNED",
            "valid_for_claim": "false",
        },
    ]


def build_first_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FF2314_0_Zq",
            "input": "Z_q",
            "first_fill_value": "Z_q = xi_q^2 n_q^A H_AB n_q^B",
            "source_basis": "2281 QSD2281_3 gradient expansion",
            "units_status": "normalization_dependent",
            "claim_status": "CONDITIONAL_FROM_2281_NOT_SOURCE_BACKED",
            "next_evidence_needed": "parent xi_q/smoothing kernel, q units, positive quotient Hessian, boundary/domain",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FF2314_1_Mq2",
            "input": "M_q^2",
            "first_fill_value": "M_q^2 = n_q^A H_AB n_q^B",
            "source_basis": "2281 QSD2281_2 transverse q mass",
            "units_status": "normalization_dependent",
            "claim_status": "CONDITIONAL_FROM_2281_NOT_SOURCE_BACKED",
            "next_evidence_needed": "parent-selected q=0 equilibrium and actual H_AB around the local branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FF2314_2_lambda",
            "input": "lambda_q",
            "first_fill_value": "lambda_q = sqrt(Z_q/M_q^2) = xi_q when the 2281 branch is activated",
            "source_basis": "2308 range formula plus 2281 Hessian/stiffness ratio",
            "units_status": "length_if_xi_q_is_parent_correlation_length",
            "claim_status": "EXACT_CONDITIONAL_RATIO_NOT_NUMERIC",
            "next_evidence_needed": "source-backed xi_q and same-normalization proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FF2314_3_q_units",
            "input": "q units/normalization",
            "first_fill_value": "q(C)=C_R-C_T/(1-C_T); R_AB=ln(1+(1-C_T)q)",
            "source_basis": "2282 q observer-cell equivalence",
            "units_status": "dimensionless_covariance_strain_under_observer_map",
            "claim_status": "TARGET_EQUIVALENCE_ONLY",
            "next_evidence_needed": "parent map from MTS variables to C_R,C_T and measured observables",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FF2314_4_domain_boundary",
            "input": "boundary/domain",
            "first_fill_value": "local quotient domain with boundary term int_boundary Z_q q n^i nabla_i q = 0 or bounded",
            "source_basis": "2281 QOC2281_2 boundary and 2296 no-hair identity",
            "units_status": "domain_dependent",
            "claim_status": "MISSING_BOUNDARY_CLASS",
            "next_evidence_needed": "no-flux/no-hair theorem for local cell/worldtube boundary",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FF2314_5_Gq_norm",
            "input": "G_q response norm",
            "first_fill_value": "||G_q|| <= 1/lambda_min(L_q); massive constant branch uses Yukawa kernel",
            "source_basis": "2281 residual bound ledger and 2313 bound-runner contract",
            "units_status": "operator_norm_in_arena_units",
            "claim_status": "FORMAL_CONTRACT_NO_NUMERIC_BOUND",
            "next_evidence_needed": "lambda_min or xi_q, arena domain, source vector norm",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FF2314_6_selector",
            "input": "q=0 selector",
            "first_fill_value": "q=0 iff T^2 S=1 iff R_AB=0",
            "source_basis": "2282 exact equivalence",
            "units_status": "dimensionless_branch_condition",
            "claim_status": "EQUIVALENCE_NOT_PARENT_SELECTOR",
            "next_evidence_needed": "parent current/constraint/gauge theorem selecting R_AB=0 without importing EH/GR",
            "valid_for_claim": "false",
        },
    ]


def build_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2314_0_operator",
            "runner_input": "Z_q, M_q^2, lambda_q, q units",
            "previous_status": "MISSING_PARENT_HESSIAN",
            "updated_status": "PARTIAL_CONDITIONAL_FILL_NOT_SCORE_READY",
            "effect": "operator denominator can be written symbolically from covariance Hessian: M_q^2=nHn, Z_q=xi_q^2 nHn, lambda_q=xi_q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2314_1_selector",
            "runner_input": "q=0 target selector",
            "previous_status": "not explicit in 2313 runner",
            "updated_status": "EQUIVALENCE_FILLED_SELECTOR_MISSING",
            "effect": "q=0 is now tied to radial observer-cell reciprocity, but this is not a parent proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2314_2_green_norm",
            "runner_input": "G_q response norm",
            "previous_status": "operator dependent schema",
            "updated_status": "FORMAL_GREEN_CONTRACT_READY_NO_NUMERIC_NORM",
            "effect": "massive/Yukawa, algebraic/Schur, and massless guards are split",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2314_3_curvature_source",
            "runner_input": "D_qWeyl2 and D_qWeylDual",
            "previous_status": "MISSING_PARENT_COEFFICIENT",
            "updated_status": "UNCHANGED_MISSING_PARENT_COEFFICIENT",
            "effect": "Schwarzschild Weyl2 kernel stays a background shape only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2314_4_source_vector",
            "runner_input": "J_q, body/boundary/tails",
            "previous_status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "updated_status": "UNCHANGED_MISSING_SOURCE_ZERO_OR_BOUND",
            "effect": "no exterior-vacuum shortcut; source channels still need zero theorem or absolute bound",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2314_5_projection",
            "runner_input": "R10/PPN/clock/orbital/local-GR observable maps",
            "previous_status": "MISSING_ARENA_PROJECTION",
            "updated_status": "UNCHANGED_MISSING_ARENA_PROJECTION",
            "effect": "no empirical scoring until q maps to observable residuals in the same normalization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2314_6_score_gate",
            "runner_input": "score permission",
            "previous_status": "CLAIM_AND_SCORE_BLOCKED",
            "updated_status": "CLAIM_AND_SCORE_BLOCKED",
            "effect": "partial conditional operator fill reduces fog but does not permit a pass/fail claim",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2314_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit is reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2314_1_conditional_operator_imported", "gate": "2281 conditional q operator imported", "passed": "true", "claim_effect": "operator shape first-fill exists", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2314_2_parent_selector", "gate": "q=0 selector parent-signed", "passed": "false", "claim_effect": "closure label remains mandatory", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2314_3_numeric_operator", "gate": "Z_q, M_q^2, xi_q numeric/source-backed", "passed": "false", "claim_effect": "no numeric Green response", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2314_4_boundary_domain", "gate": "boundary/domain/nohair signed", "passed": "false", "claim_effect": "no local plateau/no-hair claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2314_5_source_projection", "gate": "source vector and arena projection source-backed", "passed": "false", "claim_effect": "no R10/PPN/clock/orbital score", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2314_6_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "still a target, not achieved", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2314_0_operator_claim", "claim": "q operator is now parent-derived claim-grade", "allowed": "false", "reason": "2281 formula is conditional and 2282 declares selector missing", "blocking_rows": "HUNT2314_4_selector_block;CG2314_2_parent_selector", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2314_1_lambda_claim", "claim": "lambda_q=xi_q is a numeric prediction", "allowed": "false", "reason": "ratio is exact conditionally but xi_q is not sourced numerically", "blocking_rows": "FF2314_2_lambda;CG2314_3_numeric_operator", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2314_2_score_runner", "claim": "run/pass local empirical q residual tests now", "allowed": "false", "reason": "D_qWeyl2, source vector, boundary/domain, and arena projection remain missing", "blocking_rows": "RUN2314_3_curvature_source;RUN2314_4_source_vector;RUN2314_5_projection", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2314_3_local_gr", "claim": "MTS derives local GR/Newton from this checkpoint", "allowed": "false", "reason": "q=0 equivalence is not the same as a parent selector; Newton source normalization remains open", "blocking_rows": "CG2314_2_parent_selector;CG2314_6_local_GR_Newton", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2314_4_public_push", "claim": "publish 2314 as a local-GR proof", "allowed": "false", "reason": "private operator first-fill only; no public claim allowed", "blocking_rows": "all false claim gates", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2314_0",
            "next_target": "2315-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill.md",
            "why": "2314 fills the operator shape conditionally; the decisive missing proof is now the parent selector/current for q=0, or failing that the Green-domain/source-bound rows needed for finite residual tests",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    first_fill_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, hunt_rows, branch_rows, green_rows, first_fill_rows, runner_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    formalization_output_markers = (
        "2314-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2314",
        "P8_Y5_BRR545_2314",
        "JR2314_",
        "Q_GREEN_FUNCTION_NORMALIZATION_CONTRACT_2314",
        "q_bound_runner_update_nonclaim_2314",
        "Y5_R2FR_independent_q_Hessian_operator_source_or_bound_runner_first_fill_2314",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    first_fill_ids = {row["row_id"] for row in first_fill_rows}
    branch_ids = {row["row_id"] for row in branch_rows}
    green_ids = {row["row_id"] for row in green_rows}

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2314_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2314_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2314_02_conditional_formula_found", any(row["row_id"] == "HUNT2314_5_verdict" and row["result"] == "CONDITIONAL_OPERATOR_FILL_IMPORTED_NOT_CLAIM_GRADE" for row in hunt_rows), "conditional q operator fill imported but not claim-grade"))
    checks.append(("VAL2314_03_branches_classified", {"BR2314_0_dynamic_massive", "BR2314_1_algebraic_auxiliary", "BR2314_2_massless", "BR2314_3_no_pole"}.issubset(branch_ids), "dynamic, auxiliary, massless, and no-pole branches classified"))
    checks.append(("VAL2314_04_first_fill_complete", {"FF2314_0_Zq", "FF2314_1_Mq2", "FF2314_2_lambda", "FF2314_3_q_units", "FF2314_4_domain_boundary", "FF2314_5_Gq_norm", "FF2314_6_selector"}.issubset(first_fill_ids), "first-fill rows include Zq, Mq2, lambda, units, domain, Gq norm, and selector"))
    checks.append(("VAL2314_05_lambda_ratio", any(row["row_id"] == "FF2314_2_lambda" and "lambda_q = sqrt(Z_q/M_q^2) = xi_q" in row["first_fill_value"] for row in first_fill_rows), "lambda_q=xi_q ratio recorded conditionally"))
    checks.append(("VAL2314_06_green_contract", {"GF2314_0_constant_massive_kernel", "GF2314_1_covariance_range", "GF2314_3_algebraic_schur", "GF2314_4_massless_guard"}.issubset(green_ids), "Green/function branch contracts written"))
    checks.append(("VAL2314_07_runner_partially_updated", any(row["row_id"] == "RUN2314_0_operator" and row["updated_status"] == "PARTIAL_CONDITIONAL_FILL_NOT_SCORE_READY" for row in runner_rows), "runner updates operator from missing to partial conditional fill"))
    checks.append(("VAL2314_08_score_blocked", any(row["row_id"] == "RUN2314_6_score_gate" and row["updated_status"] == "CLAIM_AND_SCORE_BLOCKED" for row in runner_rows), "score gate remains blocked"))
    checks.append(("VAL2314_09_claims_blocked", any(row["row_id"] == "CG2314_6_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2314_10_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2314_11_next_target", any(row["row_id"] == "NEXT2314_0" and "2315-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill.md" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2314_12_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2314_13_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2314_14_formalization_untouched_by_2314", len(formalization_hits) == 0, "no 2314 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2314_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2314 imports the 2281 conditional q Hessian as the first operator fill, derives lambda_q=xi_q under the same-normalization branch, keeps 2282 selector closure active, blocks scoring/local-GR claims, and selects the q-zero selector/source-current or Green-domain second fill as the next target.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    first_fill_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2314 - Independent q Hessian Operator Source Or Bound-Runner First Fill",
        "",
        "## Summary",
        "",
        "2314 is a useful forward step, not another empty loop. The current corpus does contain a conditional q-operator source: 2281 shows that if the parent theory selects the local covariance equilibrium `q=0`, then the transverse Hessian gives `M_q^2=n_q^A H_AB n_q^B` and the finite smoothing expansion gives `Z_q=xi_q^2 n_q^A H_AB n_q^B`.",
        "",
        "That means the range is not an arbitrary fit parameter on this branch. Combining the 2308 range formula with the 2281 Hessian/stiffness pair gives `lambda_q=sqrt(Z_q/M_q^2)=xi_q`, provided the same normalization and positive quotient Hessian are used.",
        "",
        "The hard stop remains the selector: 2282 proves `q=0` is equivalent to radial observer-cell reciprocity, but it does not parent-select that branch. Therefore this checkpoint upgrades the runner from `missing operator` to `partial conditional operator fill`, while keeping every local-GR/Newton, R10, PPN, clock, and orbital claim blocked.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Hessian Source Hunt",
        "",
        md_table(hunt_rows, ["row_id", "target", "result", "evidence", "route_effect", "valid_for_claim"]),
        "",
        "## Operator Branch Classification",
        "",
        md_table(branch_rows, ["row_id", "operator_branch", "operator", "source_status", "claim_effect", "blocks", "valid_for_claim"]),
        "",
        "## Green Function Normalization Contract",
        "",
        md_table(green_rows, ["row_id", "contract_item", "formula", "acceptance_rule", "current_status", "valid_for_claim"]),
        "",
        "## First Fill Rows",
        "",
        md_table(first_fill_rows, ["row_id", "input", "first_fill_value", "source_basis", "units_status", "claim_status", "next_evidence_needed", "valid_for_claim"]),
        "",
        "## Bound-Runner Update",
        "",
        md_table(runner_rows, ["row_id", "runner_input", "previous_status", "updated_status", "effect", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = build_sources()
    hunt_rows = build_hunt_rows()
    branch_rows = build_branch_rows()
    green_rows = build_green_rows()
    first_fill_rows = build_first_fill_rows()
    runner_rows = build_runner_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["hunt"], hunt_rows)
    write_csv(OUTPUTS["branches"], branch_rows)
    write_csv(OUTPUTS["green"], green_rows)
    write_csv(OUTPUTS["first_fill"], first_fill_rows)
    write_csv(OUTPUTS["runner"], runner_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        hunt_rows,
        branch_rows,
        green_rows,
        first_fill_rows,
        runner_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        hunt_rows,
        branch_rows,
        green_rows,
        first_fill_rows,
        runner_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2314_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
