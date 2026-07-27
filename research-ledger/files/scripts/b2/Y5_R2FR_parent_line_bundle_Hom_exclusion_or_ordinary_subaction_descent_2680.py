from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2680"
BRANCH_ID = "Y5_R2FR_PARENT_LINE_BUNDLE_HOM_EXCLUSION_OR_ORDINARY_SUBACTION_DESCENT_2680"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2680-Y5-R2FR-parent-line-bundle-Hom-exclusion-or-ordinary-subaction-descent.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2680_SOURCE_REGISTER.csv",
    "hom_audit": RESIDUALS / "P8_Y5_R2FR_2680_HOM_EXCLUSION_DERIVATION_AUDIT.csv",
    "line_bundle_contract": RESIDUALS / "P8_Y5_R2FR_2680_PARENT_LINE_BUNDLE_OBJECT_LANGUAGE_CONTRACT_NONCLAIM.csv",
    "countermodel_rows": RESIDUALS / "P8_Y5_R2FR_2680_SUBACTION_HOM_COUNTERMODEL_ROWS_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2680_HOM_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2680_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2680_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2680_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2680_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2680_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_hom": WEP_COEFF / "parent_line_bundle_Hom_exclusion_audit_nonclaim_2680.csv",
    "microscope_contract": WEP_COEFF / "parent_line_bundle_object_language_contract_nonclaim_2680.csv",
    "microscope_countermodels": WEP_COEFF / "subaction_Hom_countermodel_rows_nonclaim_2680.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "PARENT_LINE_BUNDLE_HOM_COUNTERMODELS_2680_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "parent_line_bundle_Hom_countermodels_2680_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2680_2679_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2679_NEXT_TARGET.csv",
        "required_needles": ["NEXT2679_0_selected", "parent-line-bundle-Hom-exclusion", "ordinary subaction descent"],
        "purpose": "confirms the selected 2680 target",
    },
    {
        "source_id": "SRC2680_2679_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2679_ACTION_DENSITY_LINE_OWNER_AUDIT.csv",
        "required_needles": ["ADO2679_4_no_source_prefactor_hom", "HOM_EXCLUSION_NOT_PARENT_DERIVED", "ADO2679_8_verdict"],
        "purpose": "imports the action-line/Hom blocker from 2679",
    },
    {
        "source_id": "SRC2680_2679_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv",
        "required_needles": ["LOT2679_0_parent_density_line", "LOT2679_2_scalar_endomorphism_collapse", "LOT2679_6_verdict"],
        "purpose": "imports the line-owner contract clauses",
    },
    {
        "source_id": "SRC2680_2679_RESIDUALS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2679_EDGE_ACTION_LINE_RESIDUAL_ROWS_NONCLAIM.csv",
        "required_needles": ["ELR2679_0_action_line_weight", "ELR2679_6_no_cancellation_envelope", "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED"],
        "purpose": "imports nonclaim residual vector from 2679",
    },
    {
        "source_id": "SRC2680_NO_SOURCE_PREF",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv",
        "required_needles": ["NST1479_0_target", "NST1479_1_conditional_typing", "NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
        "purpose": "primary no-source-prefactor theorem attempt",
    },
    {
        "source_id": "SRC2680_TYPED_GRAMMAR",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv",
        "required_needles": ["TNG1470_0_target", "TNG1470_1_type_theorem", "TNG1470_3_no_extension", "TNG1470_5_verdict"],
        "purpose": "typed visible-action grammar and no-extension route",
    },
    {
        "source_id": "SRC2680_COEFF_HOM",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv",
        "required_needles": ["CDH1480_0_target", "CDH1480_1_trivial_hidden_algebra", "CDH1480_3_scalar_counterexample", "CDH1480_5_verdict"],
        "purpose": "coefficient-domain Hom exclusion plus live scalar obstruction",
    },
    {
        "source_id": "SRC2680_COEFF_HOM_GATES",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_reduction_gates_1480.csv",
        "required_needles": ["GATE1480_0_Hom_conditional", "GATE1480_1_Hom_refused", "GATE1480_2_obstructions_retained"],
        "purpose": "confirms Hom theorem-zero refused",
    },
    {
        "source_id": "SRC2680_ORDINARY_SUBACTION",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv",
        "required_needles": ["OMSCC1488_0_target", "OMSCC1488_2_vertical_blindness", "OMSCC1488_3_prefactor_countermodel", "NOT_CLOSED_WA_RESIDUAL_LOCKED"],
        "purpose": "ordinary subaction descent and prefactor countermodel",
    },
    {
        "source_id": "SRC2680_AX1090",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv",
        "required_needles": ["AXRED1441_1_no_hidden_visible_hom", "NOT_REDUCED", "AXRED1441_3_fixed_constants", "AXRED1441_4_variation_order"],
        "purpose": "confirms no-hidden-visible Hom and fixed-constant reductions are unsigned",
    },
    {
        "source_id": "SRC2680_AXIOM_REFUSAL",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/axiom_adoption_refusal_nonclaim_1486.csv",
        "required_needles": ["AX1090_1_no_hidden_visible_hom", "REFUSED_CLOSURE_ONLY_AXIOM", "AX1090_3_fixed_constant_sector"],
        "purpose": "keeps strong Hom/no-hidden clauses as targets rather than adopted axioms",
    },
    {
        "source_id": "SRC2680_SOURCE_FACTOR",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv",
        "required_needles": ["SIGN1461_0_source_factorization", "source_label_forgetting_signed", "REFUSE_DELTA_Q_ZERO_IMPORT_WRITE_CMSM_SCAFFOLD"],
        "purpose": "source/readout label forgetting remains unsigned",
    },
    {
        "source_id": "SRC2680_CURRENT_OWNER",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv",
        "required_needles": ["CSO1453_1_hilbert_variation", "CSO1453_5_pre_variation_weight", "CSO1453_7_verdict"],
        "purpose": "same-action current owner does not kill pre-action weights",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def hom_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "HOM2680_0_target",
            "claim_piece": "parent line-bundle Hom exclusion",
            "candidate_statement": "Hom_parent(species/hidden/readout labels, active source-prefactor scalars) is empty or common-constant because ordinary matter coefficients live in the quotient-visible line-bundle algebra.",
            "proof_move": "derive source-prefactor absence from the parent quotient/category object language rather than imposing WEP/EEP",
            "current_evidence": "2679 and 1479 state the exact target, but parent grammar and line-bundle owner are unsigned",
            "current_status": "TARGET_SHARPENED_NOT_PARENT_DERIVED",
            "blocking_clauses": "parent coefficient algebra; quotient-visible domain; forbidden source-prefactor target; no-extension; radiative/readout closure",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_ACTION_DENSITY_LINE_OWNER_AUDIT.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
                ]
            ),
            "exact_conditional": "false",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "test quotient pullback, trivial-hidden-algebra, and forbidden-target routes separately",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_1_quotient_pullback_lemma",
            "claim_piece": "visible coefficients factor through q_obs",
            "candidate_statement": "If every active coefficient c in S_ord is c = q_obs^* c_bar with c_bar in O(Q_obs, theta_rep), then vertical/hidden/source-label derivatives of c vanish.",
            "proof_move": "chain rule: D_v c = D c_bar[D q_obs(v)] = 0 for v in ker(Dq_obs)",
            "current_evidence": "typed grammar and ordinary-subaction files provide the conditional shape",
            "current_status": "EXACT_CONDITIONAL_LEMMA",
            "blocking_clauses": "q_obs, coefficient domain, and matter lift are not parent-signed on the full local branch",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
                ]
            ),
            "exact_conditional": "true",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "construct the parent quotient-visible coefficient algebra or retain source-prefactor rows",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_2_trivial_hidden_algebra_route",
            "claim_piece": "hidden invariant algebra is trivial",
            "candidate_statement": "If O(C_hid)^inv = R, any hidden-to-source scalar coefficient is a common constant and cannot generate relative Delta_w_AB.",
            "proof_move": "collapse hidden scalar endomorphisms to global calibration constants",
            "current_evidence": "CDH1480_1 records this as an exact conditional theorem",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_clauses": "hidden invariant algebra triviality is not proven in the current corpus",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "exact_conditional": "true",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "prove trivial invariant algebra or do not use this route",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_3_forbidden_target_route",
            "claim_piece": "active source-prefactor target absent",
            "candidate_statement": "Even if a hidden/source scalar exists, Coeff_source-prefactor is not an admissible target object in the parent coefficient algebra.",
            "proof_move": "forbid the target rather than tuning maps into it",
            "current_evidence": "CDH1480_2 and NST1479_2 identify this as the strongest conditional route",
            "current_status": "POWERFUL_CONDITIONAL_NOT_REDUCED",
            "blocking_clauses": "coefficient-target exhaustion is not derived from MTS primitives",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
                ]
            ),
            "exact_conditional": "true",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "derive coefficient target exhaustion next",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_4_species_representation_constant_route",
            "claim_piece": "species labels are representation constants, not source coefficients",
            "candidate_statement": "Species labels may select fixed representation data theta_A, but cannot define active source-weight maps A -> R_+.",
            "proof_move": "move allowed species dependence into measured nongravitational constants already in L_A, not into gravitational source prefactors",
            "current_evidence": "AX1090 fixed constants are only partially contracted, not reduced; 1479 keeps this as a grammar target",
            "current_status": "REPRESENTATION_ROUTE_UNSIGNED",
            "blocking_clauses": "fixed mass/charge/clock/material owner is incomplete; EM/mass constants are not parent-signed",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/axiom_adoption_refusal_nonclaim_1486.csv")),
                ]
            ),
            "exact_conditional": "true",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "do not hide source weights inside representation constants",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_5_ordinary_subaction_descent",
            "claim_piece": "ordinary subaction descends through q_obs and A_ord",
            "candidate_statement": "S_ord[Psi_A,e_obs(q(Phi)),theta_A] is defined before source/readout and has one first-variation current chain.",
            "proof_move": "if Dq(v)=0 and matter lift is owned, then delta_v S_ord=0 up to gauge/boundary terms",
            "current_evidence": "OMSCC1488_2 gives the exact conditional vertical-blindness route",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_clauses": "matter bundle, vertical lift, single density line and boundary class are not parent signed",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
            "exact_conditional": "true",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "keep ordinary subaction descent as a theorem target, not a pass",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_6_readout_radiative_closure",
            "claim_piece": "Hom exclusion survives effective action and readout",
            "candidate_statement": "S_eff and readout maps preserve the same coefficient domain; no loop, counterterm, calibration or source-worldtube map reintroduces source-prefactor targets.",
            "proof_move": "extend bare object-language exclusion to observed effective coefficients",
            "current_evidence": "TNG1470_4 and CDH1480_4 mark this closure as unsigned",
            "current_status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "blocking_clauses": "effective/readout closure; no-extension; no-spurion return",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
                ]
            ),
            "exact_conditional": "false",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "retain radiative/readout source-tail residuals",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_7_scalar_counterexample",
            "claim_piece": "nonconstant invariant scalar obstruction",
            "candidate_statement": "If an invariant scalar I_hid with dI != 0 is admissible and Coeff_source exists, c(I_hid) O_source is a legal relative source term.",
            "proof_move": "retain the counterexample unless trivial-hidden-algebra or forbidden-target route is parent-signed",
            "current_evidence": "CDH1480_3 explicitly proves this counterexample",
            "current_status": "COUNTEREXAMPLE_ACTIVE",
            "blocking_clauses": "no trivial invariant algebra; no forbidden coefficient target; no readout closure",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "exact_conditional": "true",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "treat scalar counterexample as the decisive failure mode for claims",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "HOM2680_8_verdict",
            "claim_piece": "Hom exclusion closes coupling slot",
            "candidate_statement": "quotient-visible coefficient algebra + forbidden source-prefactor target + ordinary subaction descent + readout closure would remove w_A as an admissible object",
            "proof_move": "attempt to parent-sign the object-language theorem",
            "current_evidence": "all exact conditionals exist, but the coefficient algebra/target exhaustion and readout closure remain unsigned",
            "current_status": "HOM_EXCLUSION_NOT_PARENT_DERIVED",
            "blocking_clauses": "coefficient target exhaustion; scalar invariant obstruction; ordinary subaction descent; readout/radiative closure",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv")),
                ]
            ),
            "exact_conditional": "true",
            "countermodel_active": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "valid_for_claim": "false",
            "next_action": "target coefficient-algebra exhaustion directly in 2681",
            "timestamp_utc": stamp(),
        },
    ]


def line_bundle_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "LBH2680_0_Aord_line_object",
            "clause": "parent ordinary action line",
            "formal_requirement": "A_ord is a parent line object over the quotient-visible local base; ordinary L_A are A_ord-valued densities before readout.",
            "if_signed": "relative action-line choices become nonobjects unless they are common End(A_ord) constants",
            "current_status": "NOT_PARENT_CONSTRUCTED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "construct A_ord from the parent quotient/category primitives",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LBH2680_1_coefficient_algebra",
            "clause": "quotient-visible coefficient algebra",
            "formal_requirement": "Allowed active coefficients are generated by O(Q_obs), fixed representation data theta_rep, gauge/current data already inside L_A, and universal constants.",
            "if_signed": "species/hidden/readout labels cannot generate new gravitational source scalars",
            "current_status": "COEFFICIENT_ALGEBRA_UNSIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "prove coefficient-domain exhaustion rather than list allowed examples",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LBH2680_2_source_prefactor_target_absent",
            "clause": "no active source-prefactor target",
            "formal_requirement": "Coeff_source-prefactor is not an admissible target object; Hom(C_hid/species/readout, Coeff_source-prefactor)=empty_or_common.",
            "if_signed": "w_A, kappa_A and c_A source-normalization scalars are ill-typed",
            "current_status": "TARGET_FORBIDDEN_ROUTE_UNSIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "derive target absence from parent object language",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LBH2680_3_species_as_representation",
            "clause": "species labels are not source functions",
            "formal_requirement": "A species label chooses theta_A and field representation, not a scalar source-weight map A -> R_+.",
            "if_signed": "material constants remain in nongravitational matter terms, not in active source normalization",
            "current_status": "FIXED_CONSTANT_OWNER_INCOMPLETE",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "separate allowed representation constants from forbidden source scalars",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LBH2680_4_ordinary_subaction_descent",
            "clause": "ordinary subaction descends through q_obs",
            "formal_requirement": "S_ord depends on parent fields only through e_obs(q(Phi)), matter fields, gauge/current data and fixed theta_A before source/readout.",
            "if_signed": "vertical/local hidden variations cannot change S_ord except gauge/boundary terms",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "parent-sign q_obs, matter lift, line object and boundary class together",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LBH2680_5_no_extension_readout_closure",
            "clause": "no extension after readout or radiative correction",
            "formal_requirement": "S_eff, source-worldtube, detector/readout and counterterm maps cannot enlarge coefficient domains with hidden/source labels.",
            "if_signed": "bare Hom exclusion transfers to observed WEP/R10/clock/local arenas",
            "current_status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "keep readout/radiative tails as residuals",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LBH2680_6_verdict",
            "clause": "Hom exclusion theorem closure",
            "formal_requirement": "All clauses LBH2680_0..5 are parent-signed in the same branch",
            "if_signed": "Delta_w_AB, epsilon_L and active source-prefactor rows become theorem-zero/common-calibration candidates",
            "current_status": "CONTRACT_READY_PROOF_NOT_CLOSED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "attack coefficient-algebra exhaustion in 2681",
            "timestamp_utc": stamp(),
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HCR2680_0_hidden_scalar_prefactor",
            "symbol": "c(I_hid)",
            "countermodel_or_residual": "nonconstant hidden invariant scalar feeds an active source operator",
            "formula_or_contract": "DeltaS = [c0 + epsilon I_hid] O_source unless hidden invariants are trivial or Coeff_source is forbidden",
            "arena_links": "WEP;R10;clock;PPN;local-GR",
            "status": "COUNTERMODEL_ACTIVE_NONCLAIM",
            "units": "dimensionless or declared source coefficient",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove trivial invariant algebra or target absence",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "HCR2680_1_species_source_weight",
            "symbol": "w_A",
            "countermodel_or_residual": "species label selects a pre-variation action/source weight",
            "formula_or_contract": "S_ord = sum_A w_A S_A gives correct matter EOM but T_source = sum_A w_A T_A",
            "arena_links": "WEP;Newton-source;R10;local-GR",
            "status": "PREFactor_COUNTERMODEL_ACTIVE",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove no source-only species target or keep Delta_w_AB residual",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "HCR2680_2_readout_label_prefactor",
            "symbol": "sigma_label_AB",
            "countermodel_or_residual": "source/readout relabels matter after parent variation and recreates a source scalar",
            "formula_or_contract": "sigma_label_AB=0 only if source-label forgetting and no-spurion-return are signed",
            "arena_links": "WEP;clock/readout;source-worldtube",
            "status": "SOURCE_LABEL_REENTRY_OPEN",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive readout/source factorization or bound label reentry",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "HCR2680_3_effective_readout_regeneration",
            "symbol": "C_eff_source_tail",
            "countermodel_or_residual": "radiative/readout/counterterm map regenerates source-prefactor coefficient",
            "formula_or_contract": "bare Hom exclusion is insufficient unless S_eff and readout maps preserve coefficient-domain exclusion",
            "arena_links": "EM;clock;R10;WEP",
            "status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "units": "declared per effective coefficient",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "stage effective/readout closure or residual source rows",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "HCR2680_4_line_bundle_leak",
            "symbol": "epsilon_Aord",
            "countermodel_or_residual": "ordinary subactions do not share a single parent line object",
            "formula_or_contract": "epsilon_Aord=0 only if A_ord exists and all L_A are A_ord-valued densities",
            "arena_links": "source-normalization;WEP;local-GR",
            "status": "PARENT_LINE_OBJECT_MISSING",
            "units": "line-norm or dimensionless after convention",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "construct A_ord or keep epsilon_Aord finite",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "HCR2680_5_subaction_descent_leak",
            "symbol": "delta_v_Sord",
            "countermodel_or_residual": "ordinary subaction has hidden/vertical dependence not killed by q_obs",
            "formula_or_contract": "delta_v S_ord=0 only if matter bundle, observed coframe, lift and boundary class descend through q_obs",
            "arena_links": "local-GR;PPN;WEP",
            "status": "ORDINARY_SUBACTION_DESCENT_UNSIGNED",
            "units": "action variation / declared source-normalized dimensionless projection",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "parent-sign ordinary subaction descent or keep finite projection row",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "HCR2680_6_absolute_envelope",
            "symbol": "epsilon_Hom_total",
            "countermodel_or_residual": "absolute no-cancellation Hom/source-prefactor envelope",
            "formula_or_contract": "abs(epsilon_Hom_total)>=abs(c(I_hid))+abs(Delta_w_AB)+abs(sigma_label_AB)+abs(C_eff_source_tail)+abs(epsilon_Aord)+abs(delta_v_Sord)",
            "arena_links": "all local source arenas",
            "status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "units": "dimensionless/envelope after source normalization",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_EDGE_ACTION_LINE_RESIDUAL_ROWS_NONCLAIM.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "score only if each component is theorem-zero or source-backed numeric",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "HCR2680_7_acquisition_template",
            "symbol": "K_Hom * tau_arena * epsilon_Hom_total",
            "countermodel_or_residual": "future arena projection of Hom/source-prefactor residual",
            "formula_or_contract": "arena residual can be compared to a bound only after K_Hom, tau_arena, units, source path and no-cancellation clause are filled",
            "arena_links": "WEP;R10;PPN;clock;orbital",
            "status": "ACQUISITION_TEMPLATE_NONCLAIM",
            "units": "declared per arena",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_reduction_gates_1480.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "fill only after theorem route fails and projection inputs are sourced",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(audit_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], countermodel_rows_: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        rows.append(
            {
                "runner_id": f"RUN2680_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "hom_derivation_audit",
                "has_parent_zero": row["theorem_zero_promoted"],
                "has_numeric_bound": "false",
                "countermodel_active": row["countermodel_active"],
                "has_existing_source_path": as_bool(all(Path(path).exists() for path in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_HOM_EXCLUSION_UNSIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in contract_rows:
        rows.append(
            {
                "runner_id": f"RUN2680_{row['contract_id']}",
                "target_id": row["contract_id"],
                "stage": "line_bundle_contract",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "countermodel_active": "true",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_CONTRACT_NOT_PARENT_SIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in countermodel_rows_:
        rows.append(
            {
                "runner_id": f"RUN2680_{row['row_id']}",
                "target_id": row["row_id"],
                "stage": "countermodel_or_bound_row",
                "has_parent_zero": row["parent_zero_available"],
                "has_numeric_bound": row["has_numeric_value"],
                "countermodel_active": "true",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_COUNTERMODEL_ROW_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2680_0_exact_conditionals",
            "claim": "quotient pullback / forbidden target / subaction descent lemmas are useful",
            "status": "PASS_EXACT_CONDITIONAL_ONLY",
            "blocking_rows": "HOM2680_1_quotient_pullback_lemma;HOM2680_3_forbidden_target_route;HOM2680_5_ordinary_subaction_descent",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2680_1_Hom_exclusion",
            "claim": "Hom into active source prefactor is absent/common",
            "status": "FAIL_PARENT_COEFFICIENT_ALGEBRA_UNSIGNED",
            "blocking_rows": "HOM2680_3_forbidden_target_route;LBH2680_1_coefficient_algebra;LBH2680_2_source_prefactor_target_absent",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2680_2_scalar_counterexample",
            "claim": "nonconstant hidden invariant scalar obstruction is removed",
            "status": "FAIL_COUNTEREXAMPLE_ACTIVE",
            "blocking_rows": "HOM2680_7_scalar_counterexample;HCR2680_0_hidden_scalar_prefactor",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2680_3_ordinary_subaction",
            "claim": "ordinary subaction descends and is vertical-blind",
            "status": "FAIL_SUBACTION_DESCENT_UNSIGNED",
            "blocking_rows": "HOM2680_5_ordinary_subaction_descent;LBH2680_4_ordinary_subaction_descent;HCR2680_5_subaction_descent_leak",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2680_4_residual_scoring",
            "claim": "Hom/source-prefactor residual vector can be scored",
            "status": "FAIL_COMPONENTS_MISSING_NUMERIC_OR_THEOREM_ZERO",
            "blocking_rows": "HCR2680_0_hidden_scalar_prefactor;HCR2680_1_species_source_weight;HCR2680_6_absolute_envelope",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2680_5_local_GR",
            "claim": "local GR/PPN can use Hom exclusion to silence source coupling",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "HOM2680_8_verdict;CG2680_1_Hom_exclusion;CG2680_2_scalar_counterexample;CG2680_4_residual_scoring",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2680_0_derivation_attempt",
            "question": "Can 2680 derive the no-source-prefactor Hom exclusion?",
            "result": "not_yet",
            "reason": "exact conditional routes exist, but coefficient target exhaustion and readout/radiative closure are not parent-signed",
            "action": "do not promote Delta_w_AB=0 or local-GR source silence",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2680_1_good_news",
            "question": "What improved?",
            "result": "decisive failure mode isolated",
            "reason": "the live counterexample is now precise: nonconstant hidden/source scalar into an active source-prefactor target",
            "action": "target coefficient-target absence directly",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2680_2_fallback",
            "question": "What if the Hom proof fails?",
            "result": "finite source-prefactor residual vector",
            "reason": "c(I_hid), w_A, sigma_label, C_eff_tail, epsilon_Aord and delta_v_Sord are explicit nonclaim rows",
            "action": "source numeric rows only if theorem route fails and arena projections are real",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2680_3_next_route",
            "question": "Best next derivation target?",
            "result": "quotient_coefficient_algebra_exhaustion",
            "reason": "forbidding the active source-prefactor target is less smuggly than assuming source universality",
            "action": "select 2681",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2680_0_selected",
            "kind": "selected",
            "target_doc": "2681-Y5-R2FR-quotient-coefficient-algebra-exhaustion-or-source-prefactor-residual-row.md",
            "target_script": "scripts/Y5_R2FR_quotient_coefficient_algebra_exhaustion_or_source_prefactor_residual_row_2681.py",
            "purpose": "try to prove the parent coefficient algebra has no active source-prefactor target; if not, keep c(I_hid), w_A and readout-tail rows as finite nonclaim residuals",
            "acceptance_gate": "coefficient algebra generated only by quotient observables, fixed representation data, in-action gauge/current data and universal constants; no source-prefactor target; no scalar invariant/readout extension",
            "forbidden_shortcuts": "assuming EEP/WEP; deleting scalar counterexample; using classical EOM scaling; importing Delta_w=0; bound inversion; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2680_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2680_1_progress",
            "field": "coupling_problem",
            "value": "reduced to parent coefficient-algebra target exhaustion plus scalar-invariant counterexample",
            "status": "sharpened_not_claimed",
            "note": "the best route is now coefficient-target absence, not another WEP-facing patch",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2680_2_next",
            "field": "next_derivation",
            "value": "quotient_coefficient_algebra_exhaustion",
            "status": "selected",
            "note": "prove no active source-prefactor target or stage finite rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2680_0_hom",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["hom_audit"]),
            "destination": str(BRANCH_OUTPUTS["microscope_hom"]),
            "contents": "Hom exclusion derivation audit retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2680_1_contract",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["line_bundle_contract"]),
            "destination": str(BRANCH_OUTPUTS["microscope_contract"]),
            "contents": "parent line-bundle object-language contract retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2680_2_countermodels",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["countermodel_rows"]),
            "destination": str(BRANCH_OUTPUTS["microscope_countermodels"]),
            "contents": "Hom/subaction countermodel rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2680_3_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["countermodel_rows"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight Hom/source-prefactor countermodels retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2680_4_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["countermodel_rows"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local bound Hom/source-prefactor countermodels retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_sources_exist_and_needles_found", "passed": as_bool(source_ok), "details": "all cited source paths exist and required needles are present"})

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_nonclaim_guard", "passed": as_bool(all_nonclaim), "details": "all generated rows carry valid_for_claim=false"})

    verdict_blocks = any(row["audit_id"] == "HOM2680_8_verdict" and row["current_status"] == "HOM_EXCLUSION_NOT_PARENT_DERIVED" for row in rows["hom_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_Hom_verdict_blocks_claim", "passed": as_bool(verdict_blocks), "details": "Hom exclusion theorem is not promoted"})

    conditional_kept = any(row["audit_id"] == "HOM2680_1_quotient_pullback_lemma" and row["exact_conditional"] == "true" for row in rows["hom_audit"]) and any(row["audit_id"] == "HOM2680_3_forbidden_target_route" and row["exact_conditional"] == "true" for row in rows["hom_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_exact_conditionals_retained", "passed": as_bool(conditional_kept), "details": "quotient pullback and forbidden-target lemmas are retained as conditionals"})

    counterexample_retained = any(row["audit_id"] == "HOM2680_7_scalar_counterexample" and row["current_status"] == "COUNTEREXAMPLE_ACTIVE" for row in rows["hom_audit"]) and any(row["row_id"] == "HCR2680_0_hidden_scalar_prefactor" and row["status"] == "COUNTERMODEL_ACTIVE_NONCLAIM" for row in rows["countermodel_rows"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_scalar_counterexample_retained", "passed": as_bool(counterexample_retained), "details": "nonconstant invariant scalar counterexample stays active"})

    contract_verdict = any(row["contract_id"] == "LBH2680_6_verdict" and row["current_status"] == "CONTRACT_READY_PROOF_NOT_CLOSED" for row in rows["line_bundle_contract"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_contract_ready_not_closed", "passed": as_bool(contract_verdict), "details": "line-bundle object-language contract is ready but not parent-signed"})

    residual_ids = {row["row_id"] for row in rows["countermodel_rows"]}
    residuals_complete = {"HCR2680_0_hidden_scalar_prefactor", "HCR2680_1_species_source_weight", "HCR2680_3_effective_readout_regeneration", "HCR2680_5_subaction_descent_leak", "HCR2680_6_absolute_envelope"}.issubset(residual_ids)
    residuals_nonclaim = all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in rows["countermodel_rows"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_countermodel_rows_complete_nonclaim", "passed": as_bool(residuals_complete and residuals_nonclaim), "details": "Hom/subaction countermodel rows exist and remain nonclaim"})

    gates_ok = any(row["gate_id"] == "CG2680_5_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and any(row["gate_id"] == "CG2680_0_exact_conditionals" and row["status"] == "PASS_EXACT_CONDITIONAL_ONLY" for row in rows["claim_gates"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_claim_gates_correct", "passed": as_bool(gates_ok), "details": "conditionals acknowledged while local-GR remains blocked"})

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_runner_refuses_unsigned_rows", "passed": as_bool(runner_refuses), "details": "runner refuses scoring without parent zero or numeric residuals"})

    next_selected = any(row["target_id"] == "NEXT2680_0_selected" and "2681-Y5-R2FR-quotient-coefficient-algebra-exhaustion-or-source-prefactor-residual-row.md" in row["target_doc"] for row in rows["next_target"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_next_target_selected", "passed": as_bool(next_selected), "details": "next target selects quotient coefficient-algebra exhaustion"})

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_csv_parse", "passed": as_bool(csv_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results))})

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_branch_copies_parse", "passed": as_bool(branch_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse))})

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_formalization_write_guard", "passed": as_bool(formalization_guard), "details": "generated path allowlist excludes formalization-workbench"})

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_pycache_absent_at_validation_time", "passed": as_bool(pycache_absent), "details": "scripts/__pycache__ absent when validation rows were produced"})

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2680_pycache_absent_at_validation_time")
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2680_OVERALL", "passed": as_bool(overall), "details": "2680 keeps the Hom/source-prefactor exclusion conditional, preserves the scalar counterexample, and selects coefficient-algebra exhaustion next"})
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} - Parent Line-Bundle Hom Exclusion Or Ordinary Subaction Descent",
        "",
        "## Private Verdict",
        "",
        "2680 gets us to the algebraic throat of the coupling problem. The clean route is real: if active coefficients are generated only by quotient observables, fixed representation data, in-action gauge/current data and universal constants, then a species/hidden/readout Hom into an active source-prefactor target is not an object of the theory.",
        "",
        "But that is still a conditional theorem. The current corpus has not parent-signed the coefficient algebra, has not forbidden the source-prefactor target, and has not closed radiative/readout extension. The scalar counterexample remains decisive: if an invariant hidden scalar `I_hid` is admissible and `Coeff_source` exists, then `c(I_hid) O_source` is a legal coupling slot.",
        "",
        "Therefore no `Delta_w_AB=0`, no WEP pass, no R10/local-GR pass, and no source-universality claim are made here. The next non-circular attack is coefficient-algebra exhaustion: prove the source-prefactor target is absent, or keep the source-prefactor residual vector explicit.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Hom Exclusion Derivation Audit",
        "",
        markdown_table(rows["hom_audit"]),
        "",
        "## Parent Line-Bundle Object-Language Contract",
        "",
        markdown_table(rows["line_bundle_contract"]),
        "",
        "## Subaction/Hom Countermodel Rows",
        "",
        markdown_table(rows["countermodel_rows"]),
        "",
        "## Runner Results",
        "",
        markdown_table(rows["runner_results"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(rows["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision_ledger"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next_target"]),
        "",
        "## Project Status",
        "",
        markdown_table(rows["project_status"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branch_copies"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["source_register"] = source_register_rows()
    rows["hom_audit"] = hom_audit_rows()
    rows["line_bundle_contract"] = line_bundle_contract_rows()
    rows["countermodel_rows"] = countermodel_rows()
    rows["runner_results"] = runner_results_rows(rows["hom_audit"], rows["line_bundle_contract"], rows["countermodel_rows"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "hom_audit",
        "line_bundle_contract",
        "countermodel_rows",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["microscope_hom"], rows["hom_audit"])
    write_csv(BRANCH_OUTPUTS["microscope_contract"], rows["line_bundle_contract"])
    write_csv(BRANCH_OUTPUTS["microscope_countermodels"], rows["countermodel_rows"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["countermodel_rows"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["countermodel_rows"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
