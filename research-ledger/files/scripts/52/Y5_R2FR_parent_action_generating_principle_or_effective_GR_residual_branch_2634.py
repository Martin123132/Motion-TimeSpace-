from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2634-Y5-R2FR-parent-action-generating-principle-or-effective-GR-residual-branch.md"

PREFIX = "P8_Y5_PARENT_ACTION_GENERATOR_2634"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "principle_attempt": RESIDUALS / f"{PREFIX}_GENERATING_PRINCIPLE_ATTEMPT.csv",
    "proof_chain": RESIDUALS / f"{PREFIX}_PROOF_CHAIN_VERDICT.csv",
    "universal_gap": RESIDUALS / f"{PREFIX}_UNIVERSAL_PROPERTY_GAP.csv",
    "route_scorecard": RESIDUALS / f"{PREFIX}_ROUTE_SCORECARD.csv",
    "effective_branch": RESIDUALS / f"{PREFIX}_EFFECTIVE_GR_BRANCH_DEMOTION.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2634_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2634_00_2633_gate",
        "role": "current local-GR parent-normal-form gate",
        "path": ROOT / "2633-Y5-R2FR-parent-normal-form-DObs-EH-current-branch-synthesis-or-full-PPN-residual-fill.md",
        "needles": [
            "PARENT_NORMAL_FORM_GATE_WRITTEN_NOT_PASSED",
            "2634-Y5-R2FR-parent-action-generating-principle",
            "VAL2633_OVERALL",
        ],
    },
    {
        "source_id": "SRC2634_01_407_primitive_sketch",
        "role": "primitive relational quotient action sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needles": [
            "primitive_relational_quotient_action_sketch_written_candidate_parent_origin_formalized",
            "no_marker_theorem_derived",
            "Decision",
        ],
    },
    {
        "source_id": "SRC2634_02_422_no_cheat",
        "role": "matter/readout no-cheat contract",
        "path": ROOT / "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "needles": [
            "matter_functor_blindness_readout_after_variation_attempt_written_exact_no_cheat_contract",
            "parent_factorization_derived",
            "Decision",
        ],
    },
    {
        "source_id": "SRC2634_03_423_minimality",
        "role": "minimality/no-extension theorem attempt",
        "path": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "needles": [
            "parent_action_minimality_no_extension_attempt_written_fixed_spurions_excluded",
            "parent_universal_property_derived",
            "Decision",
        ],
    },
    {
        "source_id": "SRC2634_04_2609_primitive_package",
        "role": "current primitive minimality/invariant algebra gate",
        "path": ROOT / "2609-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
        "needles": [
            "primitive minimality remains unproved",
            "local invariant algebra not trivialized",
            "VAL2609_OVERALL",
        ],
    },
    {
        "source_id": "SRC2634_05_2618_action_normal_form",
        "role": "parent action normal-form signature and source-map owner rule",
        "path": ROOT / "2618-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": [
            "NORMAL_FORM_CONTRACT_WRITTEN",
            "SIGNATURE_READY_PARENT_UNSIGNED",
            "VAL2618_OVERALL",
        ],
    },
    {
        "source_id": "SRC2634_06_2619_GR_bridge",
        "role": "Einstein/Newton conditional bridge and residual pack",
        "path": ROOT / "2619-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "needles": [
            "CONDITIONAL_THEOREM_NOT_PARENT_PROOF",
            "DeltaE_munu remains live",
            "VAL2619_OVERALL",
        ],
    },
    {
        "source_id": "SRC2634_07_2622_lovelock_lock",
        "role": "Lovelock/R2FR relative theorem and parent hypothesis blocker",
        "path": ROOT / "2622-Y5-R2FR-Lovelock-hypothesis-audit-metric-only-second-order-or-residual-bounds.md",
        "needles": [
            "R2FR_AND_LOVELOCK_RELATIVE_THEOREMS_ARE_USEFUL",
            "PRIMITIVE_QUOTIENT_NO_MARKER_NO_TOWER_IS_NEXT",
            "VAL2622_OVERALL",
        ],
    },
    {
        "source_id": "SRC2634_08_2623_primitive_lock",
        "role": "primitive quotient/no-marker/no-tower theorem attempt",
        "path": ROOT / "2623-Y5-R2FR-primitive-quotient-no-natural-marker-no-integrated-out-tower-or-residual-bounds.md",
        "needles": [
            "PRIMITIVE_QUOTIENT_NO_MARKER_NO_TOWER_NOT_PROVEN",
            "PQT2623_3_no_extension_universal_property",
            "VAL2623_OVERALL",
        ],
    },
    {
        "source_id": "SRC2634_09_2624_readout_schema",
        "role": "readout-after-variation schema theorem",
        "path": ROOT / "2624-Y5-R2FR-readout-after-variation-parent-schema-theorem-or-generator-residual-bound.md",
        "needles": [
            "READOUT_THEOREM_CONDITIONAL_CLEAN",
            "FIELD_BY_FIELD_PARENT_DOMAIN_CERTIFICATE_IS_NEXT",
            "VAL2624_OVERALL",
        ],
    },
    {
        "source_id": "SRC2634_10_2625_domain_cert",
        "role": "field-by-field parent-domain certificate attempt",
        "path": ROOT / "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md",
        "needles": [
            "FIELD_DOMAIN_CERTIFICATE_DOES_NOT_CLOSE",
            "READOUT_ZERO_DEMOTED_TO_CLOSURE",
            "VAL2625_OVERALL",
        ],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


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
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["path"]
        text = read_text(path)
        exists = path.exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "timestamp_utc": now(),
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def principle_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "GPR2634_0_primitive_universal_property",
            "proposed_generating_clause": "Q_MTS is the primitive/minimal parent object generated by motion-time-space; admissible extensions are gauge, universal auxiliary, or stress-free topological only",
            "current_evidence": "407/423/2609/2623 state this as the needed theorem, not as a derived result",
            "status": "NOT_DERIVED",
            "if_it_closed": "forbids material marker extensions, scalar marker prefactors, and arbitrary hidden source slots",
            "remaining_gap": "MISSING_UNIVERSAL_PROPERTY_PROOF;MISSING_CATEGORY_OF_ALLOWED_MORPHISMS;MISSING_NO_NATURAL_MARKER_FUNCTOR",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GPR2634_1_closed_parent_domain",
            "proposed_generating_clause": "Conf_parent and Args(S_parent) are closed before variation; readout/projection/fitted masks are maps from solution space to observables",
            "current_evidence": "2624 gives clean schema; 2625 says field-domain certificate does not close",
            "status": "CLOSURE_DISCIPLINE_READY_NOT_PARENT_SIGNED",
            "if_it_closed": "removes post-readout projector as Euler source and blocks reduced-action laundering",
            "remaining_gap": "MISSING_CLOSED_FIELD_LIST;MISSING_NO_EXTENSION_THEOREM;MISSING_SECTION_GAUGE_PROOF",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GPR2634_2_natural_local_action",
            "proposed_generating_clause": "S_parent is a natural local scalar functional of Q_MTS, public coframe/metric, ordinary matter and universal constants only",
            "current_evidence": "2618 writes the action-normal-form signature; 2623 retains scalar/tower countermodels",
            "status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "if_it_closed": "turns source-map and action ownership from bookkeeping into theorem structure",
            "remaining_gap": "MISSING_ACTION_INVENTORY_COMPLETION;MISSING_NO_SCALAR_PREFATOR;MISSING_NO_INTEGRATED_OUT_TOWER",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GPR2634_3_EH_selection",
            "proposed_generating_clause": "the local public branch is metric/coframe-only, diffeomorphism-invariant, second-order and residual-silent at leading order",
            "current_evidence": "2622 says Lovelock/R2FR relative theorems are useful but parent locks remain unsigned",
            "status": "RELATIVE_THEOREM_READY_PARENT_HYPOTHESES_UNSIGNED",
            "if_it_closed": "EH plus Lambda is selected instead of imported",
            "remaining_gap": "MISSING_METRIC_ONLY_PROOF;MISSING_SECOND_ORDER_NO_TOWER;MISSING_RESIDUAL_SILENCE",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GPR2634_4_source_and_matter_factorization",
            "proposed_generating_clause": "ordinary matter factors through terminal public coframe and universal constants; no active source-only species prefactors",
            "current_evidence": "422/2632 give the no-cheat/source-prefactor contract, but not a parent derivation",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "if_it_closed": "source side becomes Hilbert/Universal and compatible with Bianchi/Ward identities",
            "remaining_gap": "MISSING_MATTER_FUNCTOR_DERIVATION;MISSING_CONSTANT_SECTOR_UNIVERSALITY;MISSING_NO_SOURCE_PREFACATOR_PARENT_CLAUSE",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GPR2634_5_coefficient_owner",
            "proposed_generating_clause": "parent normalization owns a1, kappa_MTS, source worldtube normalization and measured-G transfer before tests",
            "current_evidence": "2619/2633 keep Newton bridge conditional and kappa/source residuals live",
            "status": "BLOCKED_COEFFICIENT_OWNER",
            "if_it_closed": "Newtonian coupling no longer needs fitted GM as premise",
            "remaining_gap": "MISSING_A1_OWNER;MISSING_SOURCE_WORLDTUBE_GAUSS;MISSING_G_REF_TRANSFER",
            "valid_for_claim": "False",
        },
    ]


def proof_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "PCH2634_0_attempted_leap",
            "statement": "Assume GPR2634_0-5 are all parent-derived, not axioms.",
            "verdict": "ASSUMPTION_TOO_STRONG_FOR_CURRENT_CORPUS",
            "evidence": "423/2609/2623 explicitly fail universal-property/no-natural-marker theorem",
            "effect": "cannot claim the parent generating principle as derived",
            "valid_for_claim": "False",
        },
        {
            "step_id": "PCH2634_1_conditional_success",
            "statement": "Under those clauses, 2633 local-GR gate closes in theorem shape: parent action -> EH/kappa -> Hilbert source -> no-shadow readout -> PPN vector.",
            "verdict": "EXACT_CONDITIONAL_ROUTE",
            "evidence": "2618/2619/2622/2633 supply the bridge structure",
            "effect": "we know precisely what proof would be enough",
            "valid_for_claim": "False",
        },
        {
            "step_id": "PCH2634_2_failure_location",
            "statement": "The proof fails before variation: the parent object is not proven primitive-minimal/closed.",
            "verdict": "FAILS_AT_UNIVERSAL_PROPERTY_AND_DOMAIN_CLOSURE",
            "evidence": "2625 certificate does not close; 2623 retains generators",
            "effect": "EH/no-shadow/source silence cannot be promoted from closure to derivation",
            "valid_for_claim": "False",
        },
        {
            "step_id": "PCH2634_3_not_a_dead_end",
            "statement": "Failure to derive the parent principle does not kill the programme; it forces status discipline.",
            "verdict": "DERIVATION_TARGET_RETAINED_EFFECTIVE_BRANCH_REQUIRED",
            "evidence": "operator/residual packs exist and can become testable once source-backed",
            "effect": "continue proof hunt, but prepare explicit residual branch instead of pretending local GR is won",
            "valid_for_claim": "False",
        },
    ]


def universal_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "UG2634_0_category",
            "missing_theorem": "define the category of admissible MTS parent objects and morphisms",
            "why_needed": "without it, primitive/minimal has no proof meaning",
            "current_status": "MISSING_OBJECT_LANGUAGE",
            "next_possible_attack": "source-hunt actual primitive definitions; otherwise write as explicit axiom candidate",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "UG2634_1_initial_or_free_object",
            "missing_theorem": "Q_MTS is initial/free/minimal for motion-time-space data",
            "why_needed": "this is the only clean way to forbid Q_tilde=(Q,m)/G_rel marker extensions without taste",
            "current_status": "NOT_DERIVED",
            "next_possible_attack": "prove universal property or demote no-extension to closure axiom",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "UG2634_2_no_natural_marker",
            "missing_theorem": "every natural local marker functor Q_MTS -> Marker is constant, gauge, universal auxiliary, or global/topological stress-free data",
            "why_needed": "kills co-moving material markers, domain class scalars, species constants and finite-fibre charge routes",
            "current_status": "NOT_DERIVED",
            "next_possible_attack": "generator-by-generator elimination with residual rows for failures",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "UG2634_3_no_tower",
            "missing_theorem": "integrating out auxiliary/private sectors cannot regenerate R2/f(R)/Ricci2/Weyl2/nonlocal towers in the public branch",
            "why_needed": "Lovelock/EH selection can fail after reduction even if the parent looks second order",
            "current_status": "NOT_DERIVED",
            "next_possible_attack": "sector Hessian/positive-operator/source-independent solution tests or explicit operator coefficients",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "UG2634_4_parent_domain_certificate",
            "missing_theorem": "closed Conf_parent/Args(S_parent) certificate excluding readout/projector/fitted masks before variation",
            "why_needed": "turns readout-after-variation from policy into theorem-zero",
            "current_status": "CERTIFICATE_ATTEMPT_FAILED_CURRENT_EVIDENCE",
            "next_possible_attack": "field-by-field source certificate or retain E_readout_total residual",
            "valid_for_claim": "False",
        },
    ]


def route_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "ROUTE2634_0_universal_property_proof",
            "route": "prove primitive universal property/no-extension theorem",
            "upside": "could close many local-GR clauses at once",
            "risk": "current corpus has repeatedly failed to derive it",
            "score": "BEST_IF_SOURCE_EXISTS_HIGH_RISK",
            "selected_now": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE2634_1_source_hunt_then_decision",
            "route": "one focused source hunt for explicit primitive-universal-property evidence, then decide axiom-vs-effective",
            "upside": "avoids endless circling and prevents accidental invention",
            "risk": "may end by demoting the route",
            "score": "BEST_NEXT",
            "selected_now": "True",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE2634_2_generator_by_generator",
            "route": "eliminate readout, marker, memory, finite-fibre, domain, source and tower generators one by one",
            "upside": "derivation-first and source-checkable",
            "risk": "slower; may leave effective residuals",
            "score": "GOOD_FALLBACK",
            "selected_now": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE2634_3_effective_residual_branch",
            "route": "declare local branch effective GR plus explicit residual vector",
            "upside": "testable soon and honest",
            "risk": "weaker than fundamental derivation",
            "score": "TESTABLE_FALLBACK",
            "selected_now": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE2634_4_public_local_GR_claim",
            "route": "claim MTS derives GR now",
            "upside": "none scientifically",
            "risk": "wrong; unsupported by current gates",
            "score": "FORBIDDEN",
            "selected_now": "False",
            "valid_for_claim": "False",
        },
    ]


def effective_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "EFF2634_0_status",
            "branch_statement": "If the universal-property source hunt fails, local GR becomes effective-leading-operator plus residual vector, not parent-derived GR.",
            "required_before_testing": "source-backed values or theorem-zero rows for e_EH_import,e_kappaG,DeltaE_MTS,DObs_e_R,b_R,d_R,w_R,endpoint,Delta_PPN_abs",
            "claim_policy": "nonclaim until every residual row has units, source path, arena projection and comparator bound",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "EFF2634_1_not_failure",
            "branch_statement": "Effective branch is not a total failure; it is the honest way to test the theory if the derivation route remains unsigned.",
            "required_before_testing": "same baseline controls as GR/alternative theories; no one-theory-only jackknife standards",
            "claim_policy": "comparison language only after baselines and residual vectors are runnable",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "EFF2634_2_derivation_retained",
            "branch_statement": "Derivation route remains open only if a real universal-property/no-extension source appears or a generator is eliminated by theorem.",
            "required_before_testing": "record every promoted zero as theorem-zero with source evidence",
            "claim_policy": "no closure zero may be renamed theorem zero",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2634_0_internal",
            "claim": "2634 may guide private parent-action work",
            "status": "ALLOW_INTERNAL_NONCLAIM",
            "passed": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2634_1_generating_principle",
            "claim": "parent action generating principle is derived",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2634_2_universal_property",
            "claim": "Q_MTS primitive-minimal/no-extension theorem is proven",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2634_3_local_GR",
            "claim": "local GR/Newton follows as derived MTS limit",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2634_4_effective_test_ready",
            "claim": "effective residual branch is ready for scoring",
            "status": "BLOCKED_UNTIL_RESIDUAL_ROWS_SOURCE_BACKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2634_0_result",
            "decision": "GENERATING_PRINCIPLE_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "the proof fails at primitive universal property, no-natural-marker, no-tower and closed parent-domain clauses",
            "consequence": "do not claim local GR as derived",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2634_1_gain",
            "decision": "MISSING_AXIOM_OR_THEOREM_IS_NOW_EXACT",
            "reason": "the needed statement is not vague: Q_MTS must be primitive-minimal/no-extension with trivial local marker algebra",
            "consequence": "future work must either prove this from sources or label it as an axiom/closure",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2634_2_best_next",
            "decision": "ONE_SOURCE_HUNT_THEN_AXIOM_OR_EFFECTIVE_DECISION",
            "reason": "423,2609,2623 already tried the global theorem; repeating without new source evidence would be circling",
            "consequence": "2635 should audit whether the corpus contains an explicit universal-property source; if not, freeze it as axiom-only and move to effective residual testing/generator elimination",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2635-Y5-R2FR-universal-property-source-hunt-or-effective-residual-branch-freeze.md",
            "script": "scripts/Y5_R2FR_universal_property_source_hunt_or_effective_residual_branch_freeze_2635.py",
            "objective": "perform one focused source-backed hunt for an explicit primitive-universal-property/no-extension theorem for Q_MTS; if absent, freeze that route as axiom-only and move to generator-by-generator eliminations or the effective GR residual branch",
            "include": "407,410,422,423,2609,2618,2623,2625,2633,2634 and any original primitive MTS source files under post-checkpoint-work",
            "exclude": "inventing a universal property, repeating the same minimality failure without new evidence, public local-GR claim, fitted GM, gamma-only pass",
            "selected": "True",
            "valid_for_claim": "False",
        },
        {
            "next_target": "2635b-Y5-R2FR-effective-GR-residual-vector-source-pack.md",
            "script": "scripts/Y5_R2FR_effective_GR_residual_vector_source_pack_2635b.py",
            "objective": "fallback: start the effective residual branch by sourcing the residual vector rows needed before local tests",
            "include": "e_EH_import,e_kappaG,DeltaE_MTS,E_readout_total,DObs_e_R,b_R,d_R,w_R,endpoint,Delta_PPN_abs",
            "exclude": "using effective residual fits as fundamental derivation",
            "selected": "False",
            "valid_for_claim": "False",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    targets = [
        ("COPY2634_principle", OUTPUTS["principle_attempt"], LOCAL_BOUNDS / "Parent_action_generating_principle_2634_NONCLAIM.csv"),
        ("COPY2634_universal_gap", OUTPUTS["universal_gap"], LOCAL_BOUNDS / "Universal_property_gap_2634_NONCLAIM.csv"),
        ("COPY2634_effective", OUTPUTS["effective_branch"], LOCAL_BOUNDS / "Effective_GR_branch_demotion_2634_NONCLAIM.csv"),
        ("COPY2634_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2634_UNIVERSAL_PROPERTY_SOURCE_HUNT_NEXT.csv"),
    ]
    return [
        {
            "copy_id": copy_id,
            "source_path": str(source),
            "copy_path": str(target),
            "source_exists": bool_text(source.exists()),
            "copy_exists": bool_text(target.exists()),
            "valid_for_claim": "False",
        }
        for copy_id, source, target in targets
    ]


def copy_branch_artifacts() -> None:
    copies = [
        (OUTPUTS["principle_attempt"], LOCAL_BOUNDS / "Parent_action_generating_principle_2634_NONCLAIM.csv"),
        (OUTPUTS["universal_gap"], LOCAL_BOUNDS / "Universal_property_gap_2634_NONCLAIM.csv"),
        (OUTPUTS["effective_branch"], LOCAL_BOUNDS / "Effective_GR_branch_demotion_2634_NONCLAIM.csv"),
        (OUTPUTS["next_target"], RAB_QUEUE / "JR2634_UNIVERSAL_PROPERTY_SOURCE_HUNT_NEXT.csv"),
    ]
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def formalization_has_2634_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and ("2634" in path.name or "PARENT_ACTION_GENERATOR_2634" in path.name):
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [
        LOCAL_BOUNDS / "Parent_action_generating_principle_2634_NONCLAIM.csv",
        LOCAL_BOUNDS / "Universal_property_gap_2634_NONCLAIM.csv",
        LOCAL_BOUNDS / "Effective_GR_branch_demotion_2634_NONCLAIM.csv",
        RAB_QUEUE / "JR2634_UNIVERSAL_PROPERTY_SOURCE_HUNT_NEXT.csv",
    ]
    checks = [
        (
            "VAL2634_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in generated["source_register"]),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2634_01_principle_attempt",
            any(row["clause_id"] == "GPR2634_0_primitive_universal_property" for row in generated["principle_attempt"]),
            "generating-principle attempt includes primitive universal property clause",
        ),
        (
            "VAL2634_02_not_derived",
            any(row["status"] == "NOT_DERIVED" for row in generated["principle_attempt"])
            and any(row["decision"] == "GENERATING_PRINCIPLE_NOT_DERIVED_CURRENT_CORPUS" for row in generated["decision"]),
            "generating principle is not promoted as derived",
        ),
        (
            "VAL2634_03_conditional_route_retained",
            any(row["verdict"] == "EXACT_CONDITIONAL_ROUTE" for row in generated["proof_chain"]),
            "conditional local-GR route remains retained",
        ),
        (
            "VAL2634_04_universal_gap_explicit",
            len(generated["universal_gap"]) >= 5
            and any(row["gap_id"] == "UG2634_1_initial_or_free_object" for row in generated["universal_gap"]),
            "universal-property/no-extension gaps are explicit",
        ),
        (
            "VAL2634_05_effective_branch_nonclaim",
            all(row["valid_for_claim"] == "False" for row in generated["effective_branch"]),
            "effective residual branch remains nonclaim",
        ),
        (
            "VAL2634_06_route_selection",
            any(row["selected_now"] == "True" and row["route_id"] == "ROUTE2634_1_source_hunt_then_decision" for row in generated["route_scorecard"]),
            "one source-hunt then axiom/effective decision selected",
        ),
        (
            "VAL2634_07_claim_gates_safe",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in generated["claim_gates"]),
            "no claim gate promotes parent action/local GR/effective tests",
        ),
        (
            "VAL2634_08_next_target",
            any(row["selected"] == "True" and row["next_target"].startswith("2635-Y5-R2FR-universal-property") for row in generated["next_target"]),
            "2635 universal-property source hunt selected",
        ),
        (
            "VAL2634_09_branch_copies",
            all(path.exists() and csv_parses(path) for path in copy_paths),
            "nonclaim branch copies and acquisition queue exist and parse",
        ),
        (
            "VAL2634_10_csv_parse",
            all(path.exists() and csv_parses(path) for path in output_csvs),
            "all generated 2634 CSVs parse",
        ),
        (
            "VAL2634_11_formalization_untouched",
            not formalization_has_2634_outputs(),
            "no 2634 outputs are written under formalization-workbench",
        ),
        (
            "VAL2634_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    overall = all(status for _, status, _ in checks)
    rows = [
        {"check_id": check_id, "status": "PASS" if status else "FAIL", "detail": detail, "valid_for_claim": "False"}
        for check_id, status, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2634_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2634 parent-action generating principle attempt or effective residual branch freeze",
            "valid_for_claim": "False",
        }
    )
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2634 - Y5 R2/f(R) Parent Action Generating Principle Or Effective GR Residual Branch",
        "",
        "Status: `Y5_R2FR_2634_parent_action_generating_principle_not_derived_universal_property_gap_explicit_nonclaim`",
        "",
        "Claim ceiling: no parent generating-principle theorem, no local-GR/Newton proof, no PPN/WEP/R10 pass, no EH import-as-proof, no fitted `G/GM`, no gamma-only pass, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2634 takes the leap and asks whether the parent action normal form can be generated rather than merely written. The answer from current evidence is: not yet. The missing theorem is exact: `Q_MTS` must be primitive-minimal by a universal/no-extension property, with no nonconstant natural marker functor and no hidden tower regeneration.",
        "",
        "That is not a reason to bin the theory. It is a reason to stop pretending a closure contract is a derivation. The conditional GR bridge remains alive, but the project now has a hard fork: find source-backed universal-property evidence, or freeze that route as axiom-only and test an effective GR-plus-residual branch.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Generating-Principle Attempt",
        md_table(generated["principle_attempt"]),
        "",
        "## Proof Chain Verdict",
        md_table(generated["proof_chain"]),
        "",
        "## Universal-Property Gap",
        md_table(generated["universal_gap"]),
        "",
        "## Route Scorecard",
        md_table(generated["route_scorecard"]),
        "",
        "## Effective GR Branch Demotion",
        md_table(generated["effective_branch"]),
        "",
        "## Claim Gates",
        md_table(generated["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(generated["decision"]),
        "",
        "## Next Target",
        md_table(generated["next_target"]),
        "",
        "## Branch Copies",
        md_table(generated["branch_copies"]),
        "",
        "## Validation",
        md_table(validation),
        "",
        "## Plain-English Verdict",
        "",
        "This is the no-bullshit status: we can now state the action principle MTS needs, but the corpus does not yet derive it. The missing keystone is the universal-property/no-extension theorem for `Q_MTS`; without that, marker fields and hidden towers remain legal countermodels.",
        "",
        "Best next move: one focused source hunt for that theorem. If it is not there, we freeze the universal-property route as axiom-only and pivot to generator-by-generator eliminations plus an effective residual branch. That is how we avoid circling while still taking the derivation route seriously.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "principle_attempt": principle_attempt_rows(),
        "proof_chain": proof_chain_rows(),
        "universal_gap": universal_gap_rows(),
        "route_scorecard": route_scorecard_rows(),
        "effective_branch": effective_branch_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in generated.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    generated["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], generated["branch_copies"])
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(generated, validation)
    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
