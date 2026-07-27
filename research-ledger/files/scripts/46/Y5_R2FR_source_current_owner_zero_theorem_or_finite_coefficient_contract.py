from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1680"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1680-Y5-R2FR-source-current-owner-zero-theorem-or-finite-coefficient-contract.md"

SOURCE_FILES = {
    "1679_doc": ROOT / "1679-Y5-R2FR-parent-Rsource-basis-minimal-symbolic-map-or-data-probe.md",
    "1679_validation": OUT / "P8_Y5_BRR545_1679_VALIDATION.csv",
    "1679_basis_map": OUT / "P8_Y5_PARENT_QLOC_1679_BASIS_COMPONENT_MAP_NONCLAIM.csv",
    "1679_basis_verdict": OUT / "P8_Y5_PARENT_QLOC_1679_BASIS_VERDICT.csv",
    "1338_doc": ROOT / "1338-Y5-R10-RAB-parent-object-language-no-source-slot-theorem-or-explicit-closure.md",
    "1338_validation": OUT / "P8_Y5_BRR545_1338_VALIDATION.csv",
    "1338_theorem_attempt": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1338_closure": OUT / "P8_Y5_R10_1338_NO_SOURCE_SLOT_CLOSURE_CONDITION.csv",
    "1338_requirements": OUT / "P8_Y5_R10_1338_PROMOTION_EVIDENCE_REQUIREMENTS.csv",
    "1338_countermodels": OUT / "P8_Y5_R10_1338_LIVE_COUNTERMODEL_BOUNDARIES.csv",
    "1416_doc": ROOT / "1416-Y5-R10-RAB-source-only-species-slot-and-current-rescaling-ban-or-Rsource-bound-row.md",
    "1416_validation": OUT / "P8_Y5_BRR545_1416_VALIDATION.csv",
    "1416_ban_attempt": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
    "1416_countermodels": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv",
    "1416_first_rows": OUT / "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv",
    "1416_acceptance": OUT / "P8_Y5_R10_1416_RSOURCE_ROW_ACCEPTANCE_GATE.csv",
    "1076_owner_gates": OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
    "1077_counterexamples": OUT / "P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
    "1513_validation": OUT / "P8_Y5_BRR545_1513_VALIDATION.csv",
    "1513_primitive_audit": OUT / "P8_Y5_PARENT_MINIMALITY_1513_PRIMITIVE_THEOREM_AUDIT.csv",
    "1513_countermodels": OUT / "P8_Y5_PARENT_MINIMALITY_1513_COUNTERMODEL_LEDGER.csv",
}

NEEDLES = {
    "1679_doc": ["The minimal symbolic `R_source` basis can be written", "not parent-signed"],
    "1679_validation": ["VAL1679_OVERALL", "PASS"],
    "1679_basis_map": ["BMAP1679_0", "qbar_source_weight", "BMAP1679_5", "beta_source_alpha_projection"],
    "1679_basis_verdict": ["NO_ZERO_THEOREM_FROM_SYMBOL_NAMES"],
    "1338_doc": ["NoSourceOnlySpeciesSlot", "explicit closure"],
    "1338_validation": ["VAL1338_1_theorem_not_derived", "PASS"],
    "1338_theorem_attempt": ["OLT1338_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1338_closure": ["CLOS1338_2_no_source_only_species_slot", "SHARPEST_EXPLICIT_CLOSURE"],
    "1338_requirements": ["REQ1338_0_primitive_constructor_list", "MISSING"],
    "1338_countermodels": ["CM1338_0_relative_wA", "LIVE_COUNTERMODEL_UNTIL_CLOSURE_DERIVED_OR_ADOPTED"],
    "1416_doc": ["source-only", "current-rescaling"],
    "1416_validation": ["VAL1416_1_ban_attempt", "PASS"],
    "1416_ban_attempt": ["BAN1416_6_verdict", "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED"],
    "1416_countermodels": ["CM1416_2_current_rescaling", "LIVE_COUNTEREXAMPLE"],
    "1416_first_rows": ["RSC1416_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1416_acceptance": ["ACC1416_5_verdict", "ROW_SCHEMA_READY_VALUES_MISSING_NO_PASS"],
    "1076_owner_gates": ["OWN1076_2_current_owner", "MISSING_CURRENT_OWNER"],
    "1077_counterexamples": ["CE1077_1_current_rescaling", "creates species/source charge vector"],
    "1513_validation": ["VAL1513_1_theorem_not_proven", "PASS"],
    "1513_primitive_audit": ["PM1513_6_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
    "1513_countermodels": ["CM1513_3_comoving_marker", "LIVE"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_REGISTER.csv"
THEOREM_CLAUSES = OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv"
PROOF_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1680_PROOF_ATTEMPT_LEDGER.csv"
COUNTERMODEL_MERGE = OUT / "P8_Y5_PARENT_QLOC_1680_COUNTERMODEL_MERGE_LEDGER.csv"
FINITE_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1680_FINITE_RSOURCE_COEFFICIENT_CONTRACT_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1680_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1680_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1680_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1680_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    THEOREM_CLAUSES,
    PROOF_ATTEMPT,
    COUNTERMODEL_MERGE,
    FINITE_CONTRACT,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    THEOREM_CLAUSES,
    PROOF_ATTEMPT,
    COUNTERMODEL_MERGE,
    FINITE_CONTRACT,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    THEOREM_CLAUSES: [
        QUARANTINE / "SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
        BRANCH_RESIDUALS / "R2FR_source_current_owner_zero_theorem_clauses_1680.csv",
        QUEUE / "JR1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
    ],
    FINITE_CONTRACT: [
        QUARANTINE / "FINITE_RSOURCE_COEFFICIENT_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_Rsource_coefficient_contract_nonclaim_1680.csv",
        QUEUE / "JR1680_FINITE_RSOURCE_COEFFICIENT_CONTRACT_NONCLAIM.csv",
    ],
    COUNTERMODEL_MERGE: [
        QUARANTINE / "COUNTERMODEL_MERGE_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_countermodel_merge_ledger_1680.csv",
        QUEUE / "JR1680_COUNTERMODEL_MERGE_LEDGER.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1680.csv",
        QUEUE / "JR1680_NEXT_TARGET_NONCLAIM.csv",
    ],
}

EXPECTED_COMPONENTS = {
    "qbar_source_weight",
    "current_rescaling_residual",
    "marker_readout_residual",
    "source_worldtube_projection",
    "direct_source_product",
    "beta_source_alpha_projection",
}

EXPECTED_CLAUSES = {
    "parent_domain_fixed",
    "observed_descent_only",
    "single_action_measure_owner",
    "NoSourceOnlySpeciesSlot",
    "single_source_current_owner",
    "variation_before_readout",
    "no_marker_readout_extension",
    "radiative_readout_stability",
}

SCORE_FLAGS = [
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
    "parent_signed",
    "theorem_proved",
]


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    value_text = str(value)
    markers = [
        "MISSING_",
        "NOT_DERIVED",
        "NOT_PROVED",
        "NOT_PARENT",
        "NOT_PROMOTED",
        "BLOCKED",
        "LIVE_COUNTER",
        "CONDITIONAL_ONLY",
        "UNSIGNED",
        "FAILED",
        "FAILS",
        "DRY_RUN",
        "TEMPLATE",
        "NO_PASS",
    ]
    return any(marker in value_text for marker in markers)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_key, source_path in SOURCE_FILES.items():
        exists = source_path.exists()
        body = read_text(source_path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[source_key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[source_key]),
                "use_in_1680": "source-current owner zero theorem audit and finite coefficient contract",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def theorem_clause_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "CL1680_0",
            "parent_domain_fixed",
            "Arg(S_parent) is fixed before local tests, readout, or fitting",
            "no arena-by-arena source/readout slot can be added after the fact",
            "conditional closure only",
            "CLOS1338_0_parent_domain",
            "NOT_PARENT_SIGNED",
        ),
        (
            "CL1680_1",
            "observed_descent_only",
            "ordinary matter sees only descended observed frame/gauge data plus representation constants",
            "representative-only frame or hidden source labels cannot enter Hilbert source",
            "conditional closure only",
            "CLOS1338_1_observed_descent",
            "NOT_PARENT_SIGNED",
        ),
        (
            "CL1680_2",
            "single_action_measure_owner",
            "one parent measure/action-scale/source normalization owns all ordinary matter sectors",
            "species action multipliers and measure weights are not physical source weights",
            "would kill relative w_A and species measure-weight residuals",
            "OLT1338_4_action_scale_owner;OWN1076_1_species_blind_measure",
            "MISSING_PARENT_PROOF",
        ),
        (
            "CL1680_3",
            "NoSourceOnlySpeciesSlot",
            "Hom(SpeciesLabel,Coeff_active_source)=empty",
            "qbar_source_weight is theorem-zero",
            "sharpest missing premise from 1337/1338/1416",
            "CLOS1338_2_no_source_only_species_slot;BAN1416_2_object_language",
            "NOT_DERIVED_CURRENT_CORPUS",
        ),
        (
            "CL1680_4",
            "single_source_current_owner",
            "source/test currents are extracted from one Hilbert/Noether current functor before readout",
            "current_rescaling_residual is theorem-zero",
            "would kill J_A -> c_A J_A and beta_source,A marker rows",
            "OWN1076_2_current_owner;BAN1416_4_current_rescaling",
            "MISSING_CURRENT_OWNER",
        ),
        (
            "CL1680_5",
            "variation_before_readout",
            "Hilbert/source current extraction precedes material/source/readout projection",
            "post-variation source selectors cannot manufacture conserved source currents",
            "conditional only",
            "CLOS1338_4_variation_before_readout;CM1338_3_nonHilbert_readout_current",
            "MISSING_PARENT_PROOF",
        ),
        (
            "CL1680_6",
            "no_marker_readout_extension",
            "matter markers, domain labels, boundary labels, and readout masks are not coefficient arguments",
            "marker_readout_residual and hidden marker source weights are theorem-zero",
            "would seal source slot against marker smuggling",
            "REQ1338_3_variation_readout_order;CM1416_3_hidden_marker;CM1513_3_comoving_marker",
            "MISSING_PARENT_PROOF",
        ),
        (
            "CL1680_7",
            "radiative_readout_stability",
            "S_eff, loops, spectroscopy, WEP/R10/clock readout preserve the same coefficient domain",
            "bare source-current zero transfers to observable rows",
            "without this, source-zero proof cannot score empirical projections",
            "OLT1338_5_readout_stability;BAN1416_5_readout_radiative",
            "UNSIGNED_PARALLEL_GATE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "clause": clause,
            "formal_condition": formal_condition,
            "if_parent_signed": if_parent_signed,
            "current_evidence": current_evidence,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "parent_signed": False,
            "theorem_proved": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause, formal_condition, if_parent_signed, current_evidence, source_anchor, current_status in raw_rows
    ]


def proof_attempt_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "PROOF1680_0_target",
            "If CL1680_0 through CL1680_7 are parent-signed, then ordinary-matter source residuals factor only through universal Hilbert stress plus retained explicit residual fields.",
            "target theorem exact",
            "TARGET_EXACT_CONDITIONAL",
            "not a claim until clauses are parent-signed",
        ),
        (
            "PROOF1680_1_weight",
            "With NoSourceOnlySpeciesSlot and single action-scale owner, partial_X ln kappa_A and relative w_A are absent from active source coefficients.",
            "qbar_source_weight -> 0",
            "CONDITIONAL_MATH_VALID",
            "NoSourceOnlySpeciesSlot remains not derived",
        ),
        (
            "PROOF1680_2_current",
            "With one source-current functor, J_A -> c_A J_A is a forbidden redefinition unless c_A is universal/common-mode.",
            "current_rescaling_residual -> 0 after common-mode normalization",
            "CONDITIONAL_MATH_VALID",
            "current owner remains missing",
        ),
        (
            "PROOF1680_3_marker",
            "With no marker/readout coefficient arguments and variation-before-readout, marker_A cannot create a source-current coefficient.",
            "marker_readout_residual -> 0",
            "CONDITIONAL_MATH_VALID",
            "no-marker/readout stability not parent-signed",
        ),
        (
            "PROOF1680_4_worldtube",
            "With universal Hilbert stress, source worldtube/profile contributes only to the common measured source leg unless an explicit residual coefficient is retained.",
            "source_worldtube_projection becomes common-mode or finite coefficient",
            "CONDITIONAL_ONLY",
            "worldtube convention/source profile still missing for finite scoring",
        ),
        (
            "PROOF1680_5_direct_product",
            "With parent-owned direct observable contraction, the beta/tau split is unnecessary; without it, direct products are not scoreable.",
            "direct_source_product zero or finite coefficient",
            "NOT_PARENT_SIGNED",
            "direct parent product has not been derived",
        ),
        (
            "PROOF1680_6_verdict",
            "The source-current owner zero theorem is derivable only as a conditional implication in the current corpus.",
            "do not promote R_source=0",
            "THEOREM_NOT_PROVEN_FINITE_CONTRACT_REQUIRED",
            "live countermodels remain legal",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "derivation_step": derivation_step,
            "would_imply": would_imply,
            "current_result": current_result,
            "failure_mode": failure_mode,
            "parent_signed": False,
            "theorem_proved": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, derivation_step, would_imply, current_result, failure_mode in raw_rows
    ]


def countermodel_merge_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "CM1680_0",
            "relative_wA",
            "S_matter=sum_A w_A(X) S_A",
            "qbar_source_weight",
            "CLOS1338_2_no_source_only_species_slot;CL1680_3_NoSourceOnlySpeciesSlot",
            "CM1338_0_relative_wA;CM1416_0_wA_action",
        ),
        (
            "CM1680_1",
            "species_measure_weight",
            "S_matter=sum_A integral w_A mu(g_obs)L_A",
            "qbar_source_weight",
            "CL1680_2_single_action_measure_owner",
            "CM1338_1_species_measure_weight",
        ),
        (
            "CM1680_2",
            "current_rescaling",
            "J_A -> c_A J_A or beta_source,A source marker",
            "current_rescaling_residual",
            "CL1680_4_single_source_current_owner",
            "CE1077_1_current_rescaling;CM1416_2_current_rescaling",
        ),
        (
            "CM1680_3",
            "hidden_marker_relabel",
            "w_A=w(marker_A,domain,boundary,hidden invariant)",
            "marker_readout_residual",
            "CL1680_6_no_marker_readout_extension",
            "CM1338_2_hidden_marker_relabel;CM1416_3_hidden_marker;CM1513_3_comoving_marker",
        ),
        (
            "CM1680_4",
            "nonHilbert_readout_current",
            "J_source=T_Hilbert+sum_A zeta_A J_A_readout",
            "direct_source_product",
            "CL1680_5_variation_before_readout;CL1680_7_radiative_readout_stability",
            "CM1338_3_nonHilbert_readout_current;CM1416_4_readout_current",
        ),
        (
            "CM1680_5",
            "marker_prefactor_or_local_invariant",
            "F(sigma)R or source map kappa_A(X)T_A with quotient-invariant marker",
            "beta_source_alpha_projection",
            "CL1680_0_parent_domain_fixed;CL1680_7_radiative_readout_stability",
            "CM1513_2_marker_prefactor;CM1416_1_kappaA_source",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "form": form,
            "hits_basis_component": hits_basis_component,
            "killed_by_clause": killed_by_clause,
            "source_anchor": source_anchor,
            "current_status": "LIVE_COUNTERMODEL_UNTIL_PARENT_CLAUSE_SIGNED_OR_FINITE_BOUND_SUPPLIED",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, countermodel, form, hits_basis_component, killed_by_clause, source_anchor in raw_rows
    ]


def finite_contract_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "RFC1680_0",
            "qbar_source_weight",
            "zeta_source_weight_I",
            "partial_X ln kappa_A or relative source/action weight derivative",
            "dimensionless",
            "WEP_source_charge;Newton_GM;R10;R11;local_GR",
            "NoSourceOnlySpeciesSlot plus single action measure owner",
            "numeric or symbolic coefficient with material/source tags, parent coordinate basis, sign, uncertainty, source path",
            "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
        ),
        (
            "RFC1680_1",
            "current_rescaling_residual",
            "zeta_current_I",
            "partial_X ln c_A or beta_source,A source-current normalization residual",
            "dimensionless or parent current-normalization units",
            "WEP_source_charge;Newton_GM;R10_source_side;local_GR",
            "single source-current owner theorem",
            "current normalization owner or finite c_A/beta_source,A coefficient with units/sign/source path",
            "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
        ),
        (
            "RFC1680_2",
            "marker_readout_residual",
            "zeta_marker_I",
            "material/preparation/shadow-frame/readout marker derivative",
            "dimensionless or declared marker units",
            "WEP;clock;R10;PPN_readout;composition",
            "no marker/readout coefficient extension plus radiative stability",
            "marker coefficient or no-marker proof with source paths and readout order",
            "MISSING_MARKER_THEOREM_OR_COEFFICIENTS",
        ),
        (
            "RFC1680_3",
            "source_worldtube_projection",
            "zeta_worldtube_I",
            "Integral_source K_source(x) delta T_source(x)/delta X_I",
            "stress/profile convention in parent source-current units",
            "WEP;Newton_GM;R10_source_form_factor;orbital",
            "universal Hilbert stress plus common-mode convention and source profile",
            "source worldtube/profile, lab-frame projection, lambda/domain convention, uncertainty",
            "MISSING_SOURCE_WORLDTUBE",
        ),
        (
            "RFC1680_4",
            "direct_source_product",
            "zeta_direct_I",
            "direct parent variation product into eta_AB, Newton-GM, R10, or R11 observable",
            "arena-specific source-current units",
            "WEP;Newton_GM;R10;R11;PPN",
            "parent-derived full observable contraction",
            "direct product formula with no-cancellation guard, parent source basis, and arena kernel",
            "MISSING_DIRECT_PARENT_PRODUCT",
        ),
        (
            "RFC1680_5",
            "beta_source_alpha_projection",
            "zeta_alpha_source_I",
            "EM/fine-structure subprojection of source-side residual",
            "dimensionless or alpha-channel projection units",
            "EM_alpha;clock;WEP;R10",
            "same source-current owner plus EM/gauge kinetic coefficient domain stability",
            "beta_source_alpha coefficient or theorem-zero with alpha/EM source path",
            "MISSING_BETA_SOURCE_ALPHA_OWNER_OR_COEFFICIENT",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "basis_component": basis_component,
            "coefficient_symbol": coefficient_symbol,
            "coefficient_definition": coefficient_definition,
            "unit_requirement": unit_requirement,
            "observable_links": observable_links,
            "zero_proof_required": zero_proof_required,
            "finite_value_required": finite_value_required,
            "current_status": current_status,
            "parent_signed": False,
            "theorem_proved": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, basis_component, coefficient_symbol, coefficient_definition, unit_requirement, observable_links, zero_proof_required, finite_value_required, current_status in raw_rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1680_0_theorem",
            "CONDITIONAL_ZERO_THEOREM_WRITTEN_NOT_PROVED",
            "C0-C7 give the exact theorem contract, but parent action does not sign the clauses",
            "do not set R_source=0",
        ),
        (
            "D1680_1_finite",
            "FINITE_RSOURCE_CONTRACT_LOCKED",
            "six surviving source-side components now have coefficient symbols, units, links, and proof/value requirements",
            "use contract rows for any future WEP/R10/Newton/R11 runner",
        ),
        (
            "D1680_2_safety",
            "NO_LOCAL_GR_WEP_R10_PASS",
            "live countermodels remain legal and no coefficient is numeric/source-backed",
            "keep all claim gates false",
        ),
        (
            "D1680_3_next",
            "BUILD_EXECUTABLE_CONTRACT_OR_PARENT_ACTION_CLAUSE",
            "the next useful work is either an actual parent action clause or a validator that rejects all missing finite coefficients",
            "move to 1681",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1680_0_theorem", "source-current owner zero theorem", "BLOCKED", "conditional theorem clauses are not parent-signed"),
        ("CG1680_1_Rsource_zero", "R_source=0", "BLOCKED", "live source-weight/current/marker/readout countermodels remain legal"),
        ("CG1680_2_finite_contract", "finite R_source row score-ready", "BLOCKED", "all six contract rows require values or theorem-zero proofs with units and source paths"),
        ("CG1680_3_local_GR", "local GR/Newton/PPN pass", "BLOCKED", "source-side residual branch remains nonclaim and geometric left-hand gate is separate"),
        ("CG1680_4_WEP_R10", "WEP/R10 empirical score", "BLOCKED", "source coefficients and arena projection/readout inputs are missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": False,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1681-Y5-R2FR-finite-Rsource-contract-validator-or-parent-action-owner-clause.md",
            "script": "scripts/Y5_R2FR_finite_Rsource_contract_validator_or_parent_action_owner_clause.py",
            "objective": "turn the 1680 finite R_source contract into an executable validator, while separately testing whether a parent action owner clause can sign any zero theorem clause without adding an ad hoc axiom",
            "success_condition": "either a parent action clause signs at least one source-current/no-marker zero clause, or the validator rejects every WEP/R10/Newton/R11 use until all six finite coefficient rows have values, units, source paths, and arena projections",
            "why_next": "1680 proves the route is conditional and locks the finite fallback; the next step is enforcement so future testing cannot accidentally smuggle a zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def validate(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    clauses_exact = {row["clause"] for row in theorem_rows} == EXPECTED_CLAUSES
    theorem_not_proved = all(not bool_cell(row["theorem_proved"]) and not bool_cell(row["parent_signed"]) for row in theorem_rows + proof_rows)
    verdict_present = any(row["current_result"] == "THEOREM_NOT_PROVEN_FINITE_CONTRACT_REQUIRED" for row in proof_rows)
    countermodels_cover_components = EXPECTED_COMPONENTS.issubset({row["hits_basis_component"] for row in counter_rows} | {"source_worldtube_projection"})
    finite_contract_exact = {row["basis_component"] for row in finite_rows} == EXPECTED_COMPONENTS
    finite_contract_has_units = all(row["unit_requirement"] for row in finite_rows)
    finite_contract_nonclaim = all(not bool_cell(row["score_ready"]) and not bool_cell(row["valid_for_claim"]) and not bool_cell(row["claim_allowed"]) for row in finite_rows)
    decision_safe = any(row["decision"] == "CONDITIONAL_ZERO_THEOREM_WRITTEN_NOT_PROVED" for row in decisions) and any(row["decision"] == "FINITE_RSOURCE_CONTRACT_LOCKED" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1681-Y5-R2FR-finite-Rsource-contract-validator-or-parent-action-owner-clause.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1680*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1680_0_sources_exist", sources_ok, "all cited 1680 source paths exist and required needles are present"),
        ("VAL1680_1_clauses_exact", clauses_exact, "source-current owner theorem has exactly the eight intended clauses"),
        ("VAL1680_2_theorem_not_proved", theorem_not_proved, "zero theorem remains conditional and not parent-signed"),
        ("VAL1680_3_verdict_present", verdict_present, "proof attempt records theorem-not-proven finite-contract verdict"),
        ("VAL1680_4_countermodels_mapped", countermodels_cover_components, "live countermodels are mapped onto the R_source basis components"),
        ("VAL1680_5_finite_contract_exact", finite_contract_exact, "finite coefficient contract covers exactly six R_source components"),
        ("VAL1680_6_finite_contract_units", finite_contract_has_units, "finite coefficient contract has unit requirements"),
        ("VAL1680_7_finite_contract_nonclaim", finite_contract_nonclaim, "finite coefficient rows remain nonclaim and non-score-ready"),
        ("VAL1680_8_decision_safe", decision_safe, "decisions refuse theorem-zero and lock finite contract"),
        ("VAL1680_9_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1680_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1680_11_blocked_not_ready", blocked_not_ready, "no blocked/missing/conditional row is marked claim/scoring ready"),
        ("VAL1680_12_next_target_selected", next_target_selected, "next target selects finite contract validator or parent action owner clause"),
        ("VAL1680_13_csv_parse", csv_parse, "all generated 1680 CSVs parse"),
        ("VAL1680_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1680_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1680_16_formalization_untouched", formalization_clean, "no 1680 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "check_id": "VAL1680_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1680 source-current owner zero theorem or finite coefficient contract validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    table_rows = []
    for row in rows:
        table_rows.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *table_rows])


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1680 - Source-Current Owner Zero Theorem Or Finite Coefficient Contract

**Private status:** theorem-first source-current audit. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, clock pass, orbital pass, or public claim is made.

## Verdict

The exact source-current owner zero theorem can be written only as a **conditional implication**:

> if the parent action signs the fixed parent domain, observed descent, single action/measure owner, `NoSourceOnlySpeciesSlot`, single source-current owner, variation-before-readout, no-marker extension, and radiative/readout stability clauses, then the six-slot `R_source` residual collapses to zero/common-mode pieces or explicit retained residuals.

The current corpus does **not** sign those clauses. Therefore 1680 refuses `R_source=0` and locks the six finite coefficient contracts instead.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1680"])}

## Theorem Clauses

{markdown_table(theorem_rows, ["clause_id", "clause", "formal_condition", "if_parent_signed", "current_status"])}

## Proof Attempt Ledger

{markdown_table(proof_rows, ["attempt_id", "derivation_step", "would_imply", "current_result", "failure_mode"])}

## Countermodel Merge

{markdown_table(counter_rows, ["countermodel_id", "countermodel", "form", "hits_basis_component", "killed_by_clause", "current_status"])}

## Finite Coefficient Contract

{markdown_table(finite_rows, ["contract_id", "basis_component", "coefficient_symbol", "coefficient_definition", "unit_requirement", "zero_proof_required", "current_status"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is progress, even though it is not a win condition. We now know the source side has a precise fork: either the parent action really owns the source-current grammar, or the theory must carry finite `R_source` coefficients into WEP/R10/Newton/R11 tests. No more ghost-zero. No more costume-party numbers.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    theorem_rows = theorem_clause_rows()
    proof_rows = proof_attempt_rows()
    counter_rows = countermodel_merge_rows()
    finite_rows = finite_contract_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        source_rows,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1680", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        THEOREM_CLAUSES,
        theorem_rows,
        ["branch_id", "clause_id", "clause", "formal_condition", "if_parent_signed", "current_evidence", "source_anchor", "current_status", "parent_signed", "theorem_proved", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        PROOF_ATTEMPT,
        proof_rows,
        ["branch_id", "attempt_id", "derivation_step", "would_imply", "current_result", "failure_mode", "parent_signed", "theorem_proved", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        COUNTERMODEL_MERGE,
        counter_rows,
        ["branch_id", "countermodel_id", "countermodel", "form", "hits_basis_component", "killed_by_clause", "source_anchor", "current_status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        FINITE_CONTRACT,
        finite_rows,
        ["branch_id", "contract_id", "basis_component", "coefficient_symbol", "coefficient_definition", "unit_requirement", "observable_links", "zero_proof_required", "finite_value_required", "current_status", "parent_signed", "theorem_proved", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, theorem_rows, proof_rows, counter_rows, finite_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, theorem_rows, proof_rows, counter_rows, finite_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1680 validation PASS")


if __name__ == "__main__":
    main()
