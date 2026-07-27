from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1055-alpha-owner-matter-functor-contract-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1055_PARENT_ACTION_CONTRACT_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1055_0_1054_next", "source-intake/mts_residuals/P8_Y5_R10_1054_NEXT_TARGET.csv", "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md", "1054 handoff."),
        ("SRC1055_1_1054_zero", "source-intake/mts_residuals/P8_Y5_R10_1054_FORMAL_ZERO_PROOF_ATTEMPT.csv", "FP1054_6_verdict", "conditional zero proof status."),
        ("SRC1055_2_1054_clauses", "source-intake/mts_residuals/P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv", "ZC1054_2_alpha_owner", "unsigned zero-theorem clauses."),
        ("SRC1055_3_990_contract", "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_3_EM_lock", "compact parent action contract clauses."),
        ("SRC1055_4_979_spine", "source-intake/mts_residuals/P8_Y5_R10_979_PARENT_ACTION_SPINE_CLAUSE.csv", "PASC979_2_parent_action_functional", "parent action spine and constant-sector projection."),
        ("SRC1055_5_764_alpha_owner", "source-intake/mts_residuals/P8_Y5_R10_764_ALPHA_EM_OWNER_AUDIT.csv", "AEO764_2_parent_vertical_generator_norm", "alpha owner candidates."),
        ("SRC1055_6_905_alpha_inputs", "source-intake/mts_residuals/P8_Y5_R10_905_PARENT_ALPHA_INPUT_OWNER_MATRIX.csv", "PAO905_5_alpha_row", "parent alpha input owner matrix."),
        ("SRC1055_7_1044_matter_pullback", "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv", "MPD1044_7_exact_theorem_if_signed", "matter pullback exact conditional theorem."),
        ("SRC1055_8_1045_matter_signature", "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_6_verdict", "parent matter functor signature audit."),
        ("SRC1055_9_955_minimal_matter", "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv", "MMA955_6_verdict", "minimal matter action source-coupling lemma."),
        ("SRC1055_10_953_source_functor", "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", "NSF953_5_verdict", "source-label forgetting theorem attempt."),
        ("SRC1055_11_1050_product_functor", "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv", "PFT1050_5_verdict", "product functor theorem status."),
        ("SRC1055_12_1049_operator_rule", "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv", "OCR1049_5_verdict", "operator classification rule."),
        ("SRC1055_13_1051_alpha_closure", "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", "AOR1051_3_verdict", "alpha owner/radiative closure blocker."),
        ("SRC1055_14_980_no_marker", "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", "NMF980_7_verdict", "no-marker obstruction."),
        ("SRC1055_15_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate bound curve for smoke only."),
        ("SRC1055_16_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "existing R10 runner and schema."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "PAC1055_0_configuration_and_quotient",
            "contract_clause": "parent configuration is fibered over fixed visible constant sectors and quotient readout",
            "minimal_form": "Phi in C_parent, q_loc: C_parent -> Q_obs, pi_const: C_parent -> Theta_rep x Level_EM x K_grav, and V_X subset ker(Dq_loc) cap ker(Dpi_const)",
            "would_buy": "local hidden/relaxation motion cannot move observed geometry or constants",
            "construction_status": "CONTRACT_FORM_READY_NOT_DERIVED",
            "missing_for_derivation": "deeper MTS construction of q_loc, pi_const, and allowed vertical distribution",
            "adoptable_as_axiom": "true_private_contract_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PAC1055_1_EM_owner",
            "contract_clause": "observed EM connection and kinetic normalization are owned by fixed representation/topological data",
            "minimal_form": "S_EM = -1/(4 g_*^2(ell_EM)) int sqrt(-g_obs(q)) F_Q^2 + S_int[A_Q,J_Q(theta_A)], with Lie_v ell_EM=0 and no f(Xhat)F_Q^2 slot",
            "would_buy": "Lie_v alpha_EM=0, b_alpha=0, and no alpha-marker source coupling",
            "construction_status": "CLEAN_CONTRACT_NOT_PARENT_DERIVED",
            "missing_for_derivation": "vertical-generator norm/topological-level inheritance for g_* and current normalization",
            "adoptable_as_axiom": "true_private_contract_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PAC1055_2_matter_functor",
            "contract_clause": "ordinary matter descends through observed coframe and fixed representation constants",
            "minimal_form": "S_matter = sum_A S_A[Psi_A,e_obs(q),omega(e_obs(q)),A_Q,theta_A] with Lie_v theta_A=0",
            "would_buy": "partial_Xhat ln m_A^eff = 0, no shadow-frame matter charge, no hidden mass/readout marker",
            "construction_status": "EXACT_CONDITIONAL_MATTER_PULLBACK_NOT_PARENT_SIGNED",
            "missing_for_derivation": "parent matter bundle/category and fixed/gauge vertical lift for all ordinary species",
            "adoptable_as_axiom": "true_private_contract_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PAC1055_3_no_mixed_coefficients",
            "contract_clause": "allowed visible coefficients are only functions of q_loc or fixed representation/topological data",
            "minimal_form": "Allowed[Coeff(O_vis)] subset O(Q_obs) x Theta_rep x Level_EM; Hom(C_hid,Coeff(O_vis)) is absent",
            "would_buy": "forbids f_X F^2, m_A(Xhat), y_A(Xhat), B_A(Xhat), and clock_i(Xhat)",
            "construction_status": "POWERFUL_AXIOM_IF_UNSIGNED",
            "missing_for_derivation": "hidden invariant algebra triviality or parent operator-classification theorem",
            "adoptable_as_axiom": "true_private_contract_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PAC1055_4_source_label_forgetting",
            "contract_clause": "gravitational source is total Hilbert matter source with no source-only species prefactors",
            "minimal_form": "T_total = sum_A 2/sqrt(-g_obs) delta S_A/delta g_obs; source functor Obj(C_matter)->T_total, not Obj(C_matter)->(T_A,A)",
            "would_buy": "relative source weights and WEP/R10 beta_source_alpha slots are structurally unavailable",
            "construction_status": "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED",
            "missing_for_derivation": "parent category must forget species labels before source coupling selection",
            "adoptable_as_axiom": "true_private_contract_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PAC1055_5_radiative_readout_closure",
            "contract_clause": "renormalized/effective/readout maps preserve quotient and constant-sector ownership",
            "minimal_form": "S_vis^eff and clock/readout maps remain in Alg[q_loc,Theta_rep,Level_EM] with no generated Xhat coefficient maps",
            "would_buy": "tree-level zero survives EFT and clock reductions",
            "construction_status": "REQUIRED_CLOSURE_AXIOM_NOT_DERIVED",
            "missing_for_derivation": "RG/readout theorem or explicit retained residual priors",
            "adoptable_as_axiom": "true_private_contract_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PAC1055_6_single_parent_action",
            "contract_clause": "one parent variational object owns geometry, EM, matter, source, and readout",
            "minimal_form": "S_parent = S_geom[Phi] + S_hidden[Phi] + S_EM[q(Phi),A_Q,ell_EM] + sum_A S_A[Psi_A,q(Phi),A_Q,theta_A] + S_boundary[q(Phi)]",
            "would_buy": "prevents post-hoc insertion of separate source/readout closures after local tests",
            "construction_status": "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS",
            "missing_for_derivation": "derivation from MTS primitives rather than adoption as a discipline contract",
            "adoptable_as_axiom": "true_private_contract_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def adoption_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "ADG1055_0_derivation_not_minimality",
            "gate": "do not use aesthetic minimality as proof",
            "status": "ACTIVE_BLOCK",
            "reason": "absence of f_X or m_A(Xhat) in a written action is not a derivation unless the parent operator domain forbids them",
            "promotion_requirement": "derive parent operator classification or explicitly mark the contract as an axiom",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "ADG1055_1_alpha_owner",
            "gate": "alpha_EM owner",
            "status": "BEST_ROUTE_NOT_PROVED",
            "reason": "compact U(1) supports charges but does not by itself own the continuous Maxwell kinetic coefficient",
            "promotion_requirement": "derive g_* from vertical generator norm, topological level, index, or fixed parent metric on the gauge fibre",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "ADG1055_2_matter_functor",
            "gate": "matter constants/readout fixed representation data",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "matter pullback theorem works but the parent matter bundle and constant superselection are not constructed",
            "promotion_requirement": "derive the matter category and vertical lift from parent action data",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "ADG1055_3_source_label_forgetting",
            "gate": "species-blind source functor",
            "status": "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
            "reason": "same-action Hilbert source helps, but constant relative prefactors remain legal unless source-only slots are forbidden",
            "promotion_requirement": "parent category forgets species labels before gravitational source coupling selection",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "ADG1055_4_radiative_closure",
            "gate": "EFT/readout closure",
            "status": "UNSIGNED",
            "reason": "tree-level sequestering can be reopened by loops or effective clock/readout maps",
            "promotion_requirement": "RG/readout closure theorem or retained sourced residual priors",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def theorem_consequence_rows() -> list[dict[str, str]]:
    return [
        {
            "consequence_id": "TC1055_0_alpha",
            "if_contract_signed": "Lie_v alpha_EM = 0",
            "derivation": "alpha_EM = alpha_*(ell_EM) and Lie_v ell_EM=0",
            "would_close": "b_alpha and alpha clock/WEP coefficient drift",
            "current_status": "CONDITIONAL_ONLY",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consequence_id": "TC1055_1_matter_masses",
            "if_contract_signed": "partial_Xhat ln m_A^eff = 0 for ordinary matter",
            "derivation": "m_A and binding/readout constants live in theta_A, not C_hid",
            "would_close": "mass, binding, clock, and material marker beta rows",
            "current_status": "CONDITIONAL_ONLY",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consequence_id": "TC1055_2_beta_source_alpha",
            "if_contract_signed": "beta_source_alpha = 0",
            "derivation": "alpha source marker cannot be built from hidden or species-label data",
            "would_close": "WEP alpha/Coulomb product target without tuning",
            "current_status": "CONDITIONAL_ONLY",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consequence_id": "TC1055_3_R10_alpha_marker",
            "if_contract_signed": "beta_s beta_t alpha-marker branch = 0",
            "derivation": "source/test alpha charges vanish before the finite Yukawa comparison",
            "would_close": "R10 alpha-marker branch, leaving only independently retained non-alpha tails",
            "current_status": "CONDITIONAL_ONLY_TAILS_RETAINED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consequence_id": "TC1055_4_local_GR",
            "if_contract_signed": "one source-current route becomes cleaner",
            "derivation": "same matter action and species-blind source functor support a universal Hilbert source",
            "would_close": "part of WEP/Newton source normalization, not the full PPN/GR reduction",
            "current_status": "CONDITIONAL_PARTIAL_ONLY",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CE1055_0_gauge_kinetic_function",
            "legal_if_contract_unsigned": "f(Xhat)F_Q^2",
            "why_legal": "gauge and diffeomorphism invariance allow scalar gauge kinetic functions",
            "source": "SBT1049_1_gauge_invariance; MD642_4_alpha_constant",
            "blocked_by": "PAC1055_1_EM_owner plus PAC1055_3_no_mixed_coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1055_1_hidden_invariant_scalar",
            "legal_if_contract_unsigned": "c(I_hid) O_vis",
            "why_legal": "one nonconstant invariant scalar can feed continuous visible coefficient spaces",
            "source": "NMF980_2_scalar_obstruction_lemma",
            "blocked_by": "hidden invariant algebra triviality or parent no-mixed coefficient rule",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1055_2_shadow_matter_frame",
            "legal_if_contract_unsigned": "A_A(Xhat)^2 g_obs or m_A(Xhat) psi_bar psi",
            "why_legal": "ordinary covariance does not forbid an extra matter-frame or mass function",
            "source": "MFS1045_4_no_shadow_frame; OCR1049_2_product_sequestration",
            "blocked_by": "PAC1055_2_matter_functor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1055_3_relative_source_weight",
            "legal_if_contract_unsigned": "S_matter=sum_A w_A S_A or F((T_A,A))=kappa_A T_A",
            "why_legal": "Ward symmetry, additivity, and covariance allow constant relative weights unless labels are forgotten",
            "source": "MMA955_3_relative_prefactor; NSF953_3_additivity_limit",
            "blocked_by": "PAC1055_4_source_label_forgetting",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1055_4_readout_regeneration",
            "legal_if_contract_unsigned": "loop/readout-induced f_X F^2 or clock_Xhat map",
            "why_legal": "bare action sequestering is not automatically stable under effective reductions",
            "source": "PFT1050_3_radiative_readout_closure; AOR1051_3_verdict",
            "blocked_by": "PAC1055_5_radiative_readout_closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1055_0_contract_constructed",
            "decision": "minimal parent action contract is constructible",
            "because": "the needed action schema can be written in one quotient/constant-sector variational object",
            "effect": "gives an exact route to beta_source_alpha=0 if adopted or derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1055_1_not_derivation_yet",
            "decision": "the contract is not yet derived from deeper MTS primitives",
            "because": "alpha kinetic owner, hidden-visible hom ban, matter category, source-label forgetting, and radiative closure are still clauses",
            "effect": "cannot claim WEP/R10/local-GR pass from this contract",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1055_2_best_next",
            "decision": "attack the alpha owner directly through vertical-generator norm or topological level inheritance",
            "because": "alpha_EM ownership is the most central clause for beta_source_alpha=0 and clock/WEP/R10 alpha consistency",
            "effect": "next target narrows to a derivation rather than another axiom",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1055_0_contract_adoption",
            "claim": "parent action contract is derived",
            "gate_pass": "false",
            "reason": "contract is constructible but currently axiom-level/private discipline, not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1055_1_alpha_owner",
            "claim": "alpha_EM is parent-owned and vertically constant",
            "gate_pass": "false",
            "reason": "gauge kinetic normalization owner is not derived from vertical generator norm/topology",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1055_2_matter_functor",
            "claim": "matter constants/readout descend as fixed representation data",
            "gate_pass": "false",
            "reason": "matter category and vertical lift remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1055_3_beta_source_alpha_zero",
            "claim": "beta_source_alpha=0",
            "gate_pass": "false",
            "reason": "follows from the contract only conditionally; contract is not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1055_4_WEP_R10",
            "claim": "WEP/R10 alpha branch passes",
            "gate_pass": "false",
            "reason": "requires derived zero theorem or full numeric finite branch inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
            "objective": "try to derive the EM gauge kinetic normalization owner from a parent vertical-generator norm, topological level, index, or compact fibre metric; if it fails, keep b_alpha as a product-prior branch",
            "include": "A_Q normalization, charge-current normalization, F_Q^2 coefficient, generator rescaling degeneracy, compact U1 limits, topological/index route, consequence for b_alpha and beta_source_alpha",
            "exclude": "declaring alpha fixed by taste, unit-rescaling, cancellation, tau unity shortcut, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "parent_action_contract_template",
        "curve_id": "MTS_1055_parent_action_contract_nonclaim",
        "lambda_value": "MISSING_DERIVED_ZERO_OR_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_PARENT_DERIVED_ALPHA_OWNER_OR_FINITE_BRANCH",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "contract route would set alpha-marker beta_s beta_t=0 only if parent action contract is derived; finite route still needs K_X^R10 beta_s beta_t",
        "derivation_status": "template_invalid_contract_constructed_but_not_derived",
        "formula_reference": "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "assumptions": "nonclaim placeholder; no axiom promoted as proof; no unit-rescaling; no cancellation",
        "valid_for_claim": "false",
        "notes": "Runner must refuse this row until the parent action contract is derived or a full finite alpha(lambda) prediction is sourced.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1055_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject parent-action contract placeholder until derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def refusal_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1055_0_contract",
            "object": "parent action contract",
            "current_status": "CONTRACT_CONSTRUCTED_NOT_DERIVED",
            "refusal_status": "blocked_for_claim",
            "failure_reasons": "alpha owner, matter functor, no-mixed hom, source label forgetting, and radiative closure remain unsigned",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1055_1_R10_runner",
            "object": "R10 parent-action contract smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={status.get('valid_mts_rows')}; valid_bound_rows={status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_time = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    adoption_rows: list[dict[str, str]],
    consequence_rows: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )

    source_ok = all(flag(row.get("exists", "")) and flag(row.get("needle_found", "")) for row in source_rows)
    add("V1055_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    contract_written = len(contract_rows) >= 7 and all(row.get("valid_for_claim") == "false" for row in contract_rows)
    add("V1055_2_contract_written_nonclaim", contract_written, "parent action contract clauses are written and remain nonclaim")
    alpha_clause = any(row.get("contract_id") == "PAC1055_1_EM_owner" and "g_*" in row.get("minimal_form", "") for row in contract_rows)
    matter_clause = any(row.get("contract_id") == "PAC1055_2_matter_functor" and "S_matter" in row.get("minimal_form", "") for row in contract_rows)
    add("V1055_3_alpha_and_matter_clauses_present", alpha_clause and matter_clause, "alpha owner and matter functor clauses are explicit")
    adoption_blocked = adoption_rows and all(row.get("claim_allowed") == "false" for row in adoption_rows)
    add("V1055_4_adoption_gates_blocked", adoption_blocked, "axiom/adoption gates block public claims")
    consequences_conditional = consequence_rows and all(row.get("current_status", "").startswith("CONDITIONAL") for row in consequence_rows)
    add("V1055_5_consequences_conditional", consequences_conditional, "beta_source_alpha and WEP/R10 consequences are conditional only")
    counterexamples_retained = len(counterexamples) >= 5 and all(row.get("valid_for_claim") == "false" for row in counterexamples)
    add("V1055_6_counterexamples_retained", counterexamples_retained, "known counterexamples remain retained")
    template_schema = set(MTS_REQUIRED_COLUMNS).issubset(set(template_rows[0].keys())) if template_rows else False
    template_nonclaim = template_schema and all(row.get("valid_for_claim") == "false" for row in template_rows)
    add("V1055_7_mts_template_schema_nonclaim", template_nonclaim, "MTS template has runner schema and no claim-valid rows")
    runner_refused = runner_status.get("valid_mts_rows") == 0 and runner_status.get("claim_allowed") is False
    add("V1055_8_runner_smoke_refuses_claim", runner_refused, "existing R10 runner refuses the 1055 placeholder rows")
    claims_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1055_9_claim_gates_blocked", claims_blocked, "all contract/alpha/matter/beta/WEP/R10 claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1056-Y5-R10-alpha-owner")
    add("V1055_10_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1055_11_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1055_12_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(
        0,
        {
            "check_id": "V1055_SUMMARY",
            "result": "pass" if summary_pass else "fail",
            "detail": "1055 alpha-owner and matter-functor parent action contract validation summary",
            "generated_utc": stamp(),
        },
    )
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    adoption_rows: list[dict[str, str]],
    consequence_rows: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    decisions: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows_: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1055 Y5 R10 alpha owner and matter functor parent action contract",
            "",
            "**Progress:** the minimal parent-action contract is now written explicitly. If this contract were derived from MTS primitives, it would make `alpha_EM`, masses, binding terms, and readout constants fixed quotient/representation data and would force `beta_source_alpha=0`.",
            "",
            "**Current verdict:** useful but not claim-grade. The contract is constructible and mathematically strong, but at this stage it is an action-domain axiom/discipline clause, not a derivation from deeper MTS.",
            "",
            "**Sharp next target:** derive the EM owner first. The central question is whether `g_EM`/`alpha_EM` comes from a fixed parent vertical-generator norm, topological level, index, or compact fibre metric, rather than being an inserted constant.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Parent action contract candidate",
            md_table(contract_rows, ["contract_id", "contract_clause", "minimal_form", "would_buy", "construction_status", "missing_for_derivation", "valid_for_claim"]),
            "",
            "## Adoption gates",
            md_table(adoption_rows, ["gate_id", "gate", "status", "reason", "promotion_requirement", "claim_allowed"]),
            "",
            "## Theorem consequences if signed",
            md_table(consequence_rows, ["consequence_id", "if_contract_signed", "derivation", "would_close", "current_status", "claim_allowed"]),
            "",
            "## Counterexample ledger",
            md_table(counterexamples, ["counterexample_id", "legal_if_contract_unsigned", "why_legal", "source", "blocked_by", "valid_for_claim"]),
            "",
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "effect", "claim_allowed", "valid_for_claim"]),
            "",
            "## MTS R10 smoke template",
            md_table(template_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            "",
            "## Runner smoke status",
            md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "",
            "## Placeholder refusal runner",
            md_table(refusal_rows_, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "",
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    contract_rows = parent_contract_rows()
    adoption_rows = adoption_gate_rows()
    consequence_rows = theorem_consequence_rows()
    counterexamples = counterexample_rows()
    decisions = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()
    template_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1055_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "adoption": OUT / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
        "consequences": OUT / "P8_Y5_R10_1055_THEOREM_CONSEQUENCES.csv",
        "counterexamples": OUT / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv",
        "decisions": OUT / "P8_Y5_R10_1055_DECISION_LEDGER.csv",
        "mts_template": MTS_TEMPLATE,
        "runner_smoke": OUT / "P8_Y5_R10_1055_RUNNER_SMOKE_STATUS.csv",
        "placeholder_refusal": OUT / "P8_Y5_R10_1055_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1055_CLAIM_GATES.csv",
        "next_target": OUT / "P8_Y5_R10_1055_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1055_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["contract"], contract_rows)
    write_csv(outputs["adoption"], adoption_rows)
    write_csv(outputs["consequences"], consequence_rows)
    write_csv(outputs["counterexamples"], counterexamples)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["mts_template"], template_rows, MTS_REQUIRED_COLUMNS)

    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    smoke_rows = runner_smoke_rows(runner_status)
    refusal_rows_ = refusal_rows(runner_status)
    write_csv(outputs["runner_smoke"], smoke_rows)
    write_csv(outputs["placeholder_refusal"], refusal_rows_)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        contract_rows,
        adoption_rows,
        consequence_rows,
        counterexamples,
        template_rows,
        runner_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        contract_rows,
        adoption_rows,
        consequence_rows,
        counterexamples,
        decisions,
        template_rows,
        smoke_rows,
        refusal_rows_,
        claim_rows,
        validation_rows,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
