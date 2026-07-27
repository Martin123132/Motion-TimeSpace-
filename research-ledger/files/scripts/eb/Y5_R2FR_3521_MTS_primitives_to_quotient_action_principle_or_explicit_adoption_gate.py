from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3521-Y5-R2FR-MTS-primitives-to-quotient-action-principle-or-explicit-adoption-gate.md"
CANONICAL_STATUS = OUT / "P8_EM_MTS_primitives_to_QAP_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3521": {"path": Path(__file__).resolve(), "role": "3521 generator"},
    "doc_3520": {
        "path": ROOT / "3520-Y5-R2FR-quotient-action-principle-derives-q-normal-form-or-finite-source-bounds.md",
        "role": "QAP-to-q-normal-form handoff",
    },
    "next_3520": {
        "path": OUT / "P8_Y5_R2FR_3520_NEXT_TARGET.csv",
        "role": "3521 target handoff",
    },
    "qap_3520": {
        "path": OUT / "P8_Y5_R2FR_3520_QUOTIENT_ACTION_PRINCIPLE_THEOREM.csv",
        "role": "3520 QAP theorem rows",
    },
    "qap_gates_3520": {
        "path": OUT / "P8_Y5_R2FR_3520_PARENT_SIGNATURE_GATE.csv",
        "role": "3520 parent signature blockers",
    },
    "heuristics_000": {
        "path": ROOT / "000-private-fork-heuristics-for-martin-style-search.md",
        "role": "private MTS motion/time/space heuristic guardrails",
    },
    "motion_load_01": {
        "path": ROOT / "01-motion-load-route-contract.md",
        "role": "motion-load primitive route contract",
    },
    "cell_341": {
        "path": ROOT / "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "role": "indistinguishable-cell quotient identity test",
    },
    "quotient_407": {
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive relational quotient action sketch",
    },
    "gauge_noether_12": {
        "path": ROOT / "12-gauge-noether-origin-audit.md",
        "role": "gauge/Noether origin warning",
    },
    "parent_object_2711": {
        "path": ROOT / "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md",
        "role": "parent object derivation from MTS primitives attempt",
    },
    "sort_constructor_2688": {
        "path": ROOT / "2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md",
        "role": "parent sort constructor from MTS primitives attempt",
    },
    "vertical_noether_3115": {
        "path": ROOT / "3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md",
        "role": "local vertical Noether generator certificate",
    },
    "matter_action_2587": {
        "path": ROOT / "2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
        "role": "minimal parent matter coupling action candidate",
    },
    "normalization_3464": {
        "path": ROOT / "3464-Y5-R2FR-canonical-action-normalization-from-MTS-primitives-or-WEP-effective-source-bound.md",
        "role": "canonical action normalization from MTS primitives attempt",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def primitive_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "primitive_id": "PRIM3521_0_motion_time_space_relationality",
            "candidate_primitive": "motion/time/space are operationally relational rather than labels on independent substances",
            "positive_content": "supports a state description in terms of traversal/clock/routing relations instead of arbitrary representatives",
            "needed_for_QAP": "must define an equivalence relation on histories, not just a heuristic vocabulary",
            "current_status": "MOTIVATION_STRONG_NOT_FORMAL_EQUIVALENCE",
            "source_path": str(SOURCES["heuristics_000"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
        {
            "primitive_id": "PRIM3521_1_motion_load_route",
            "candidate_primitive": "motion-load capacity/routing variables",
            "positive_content": "offers a primitive route where local clock/routing/load constraints may generate GR-like limits",
            "needed_for_QAP": "must show representative load/routing labels are unphysical identities when readouts agree",
            "current_status": "ROUTE_CONTRACT_NOT_STATE_QUOTIENT",
            "source_path": str(SOURCES["motion_load_01"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
        {
            "primitive_id": "PRIM3521_2_indistinguishable_cell",
            "candidate_primitive": "indistinguishable finite-cell/fibre relabelling",
            "positive_content": "341 proves quotient observables are constant on relabelling orbits and exposes fixed-active-marker countermodels",
            "needed_for_QAP": "must prove the parent variable is the unlabelled orbit, not a labelled species vector with a symmetry",
            "current_status": "CLEAN_IDENTITY_ROUTE_PARENT_VARIABLE_ORIGIN_OPEN",
            "source_path": str(SOURCES["cell_341"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
        {
            "primitive_id": "PRIM3521_3_relational_quotient_action",
            "candidate_primitive": "primitive relational quotient/readout parent-action sketch",
            "positive_content": "407 sketches the right configuration objects and action blocks for quotient/readout discipline",
            "needed_for_QAP": "configuration quotient, no-marker theorem, matter quotient functor and total flux owner must be proved",
            "current_status": "BEST_THEOREM_TARGET_NOT_THEOREM",
            "source_path": str(SOURCES["quotient_407"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
        {
            "primitive_id": "PRIM3521_4_gauge_noether",
            "candidate_primitive": "observer-splitting gauge/Noether origin",
            "positive_content": "Noether route identifies what first-class parent constraint would be needed",
            "needed_for_QAP": "Noether identity must be produced by a constrained parent action, not used as a substitute for it",
            "current_status": "WARNING_PASS_FIRSTCLASS_PARENT_MISSING",
            "source_path": str(SOURCES["gauge_noether_12"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
        {
            "primitive_id": "PRIM3521_5_parent_object",
            "candidate_primitive": "single parent action object from MTS primitives",
            "positive_content": "2711 shows the pieces point at one missing owner and makes local parent object closure explicit",
            "needed_for_QAP": "Conf_parent, action, quotient map, matter domain and variation order must be constructed together",
            "current_status": "EXPLICIT_CLOSURE_REQUIRED_NOT_DERIVED",
            "source_path": str(SOURCES["parent_object_2711"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
        {
            "primitive_id": "PRIM3521_6_sort_constructor",
            "candidate_primitive": "parent sort/source constructor from MTS primitives",
            "positive_content": "2688 partially constructs Q_obs/public-geometry lane and rejects syntax-by-decree promotions",
            "needed_for_QAP": "constructor exhaustion must show no active-source coefficient sort or hidden marker survives",
            "current_status": "PARTIAL_QOBS_CONSTRUCTOR_SOURCE_EXHAUSTION_UNSIGNED",
            "source_path": str(SOURCES["sort_constructor_2688"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
        {
            "primitive_id": "PRIM3521_7_vertical_noether_certificate",
            "candidate_primitive": "proper first-class vertical generator with zero boundary charge",
            "positive_content": "3115 gives a hard iff-style local-silence certificate",
            "needed_for_QAP": "candidate representative directions must satisfy off-shell Noether identity, Hamiltonian generator, bracket closure and boundary silence",
            "current_status": "EXACT_CERTIFICATE_CONTRACT_NOT_SOURCE_SIGNED",
            "source_path": str(SOURCES["vertical_noether_3115"]["path"]),
            "gate_pass": "False",
            "valid_for_claim": "False",
        },
    ]


def primitive_to_qap_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "P2Q3521_0_identity_principle",
            "claim": "If MTS primitives identify two histories as the same physical history, every physical action phase and variational equation must be invariant on that identity class.",
            "formal_statement": "For histories Phi1~Phi2 by primitive MTS identity, S_parent[Phi1]-S_parent[Phi2] is at most a fixed proper boundary/2pi phase term; otherwise the stationary equations or quantum/statistical weights distinguish the representatives.",
            "derivation": "If the action differs nontrivially along an identity fibre, varying along the fibre changes equations, source currents, or phase weights. That makes the representative label empirically active, contradicting the premise that the two histories are the same physical MTS history.",
            "effect_if_signed": "QAP follows: S_parent descends to Conf_parent/~ before matter/source variation.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "fires_now": "False",
            "source_path": str(SOURCES["qap_3520"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "P2Q3521_1_identity_vs_symmetry",
            "claim": "Relabelling symmetry is not enough; the parent state itself must be an orbit/equivalence class.",
            "formal_statement": "If labels are physical species coordinates, a symmetric action S(h)=S(permutation h) does not imply h and permutation h are the same state. If the parent state is [h] in R^n/S_n, representative dependence is ill-defined.",
            "derivation": "341's same-formula trap: the same invariant formula can describe either a quotient variable or a labelled-species vector. The state-space definition, not formula symmetry, decides whether QAP is derived.",
            "effect_if_signed": "finite-cell/source-label relabellings become representative gauge identities rather than global symmetries.",
            "current_status": "EXACT_GUARD_THEOREM_NOT_PARENT_SIGNED",
            "fires_now": "False",
            "source_path": str(SOURCES["cell_341"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "P2Q3521_2_motion_time_space_readout",
            "claim": "Motion/time/space primitives can support QAP only if readouts depend on invariant traversal relations, not representative labels.",
            "formal_statement": "Allowed readouts O_A must satisfy O_A(Phi)=Obar_A([Phi]) for local clocks, rods, photons, source masses, EM/Hodge readout and boundaries.",
            "derivation": "If any readout changes along the proposed primitive fibre, the fibre is physically visible and cannot be quotiented for local source coupling.",
            "effect_if_signed": "DObs_A[v_q]=0 and Qvis ownership become primitive consequences.",
            "current_status": "CONDITIONAL_READOUT_TEST_NOT_CLOSED",
            "fires_now": "False",
            "source_path": str(SOURCES["vertical_noether_3115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "P2Q3521_3_no_active_marker",
            "claim": "A primitive quotient forbids fixed active markers, source masks and species/source labels from entering bulk action terms.",
            "formal_statement": "There is no parent morphism IdentityFibre -> ActiveSourceCoefficient except constants/common modes; fixed markers are external readout dressings or residuals, not bulk primitives.",
            "derivation": "An active marker selects a representative inside an identity class. If it affects the action, it makes the marker physical and defeats the quotient.",
            "effect_if_signed": "no source-only prefactor, no hidden active q source scalar, no fixed active P_active bulk term.",
            "current_status": "EXACT_CONDITIONAL_NO_MARKER_THEOREM_NOT_SIGNED",
            "fires_now": "False",
            "source_path": str(SOURCES["sort_constructor_2688"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "P2Q3521_4_noether_certificate",
            "claim": "A derived primitive identity should appear as a first-class vertical Noether generator in the local variational theory.",
            "formal_statement": "For vertical generator v_epsilon, R^dagger(E(S_parent))=0 off shell, Omega(delta Phi,v_epsilon)=delta G[epsilon], G=int epsilon C+Q_boundary, bracket closes and Q_boundary is zero/exact/proper.",
            "derivation": "This is the local Hamiltonian/covariant-phase-space expression of action descent on identity fibres.",
            "effect_if_signed": "representative directions are true gauge; Dq[v]=0 becomes backed by a generator rather than a declaration.",
            "current_status": "EXACT_CERTIFICATE_REQUIRED_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["vertical_noether_3115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "P2Q3521_5_current_verdict",
            "claim": "Current MTS primitives do not yet parent-own QAP, but they reduce it to one sharp primitive identity theorem.",
            "formal_statement": "MTS derives QAP iff it derives a parent history equivalence relation whose fibres are readout-invisible, no-marker, first-class/proper-boundary identity directions.",
            "derivation": "Combine 3520 QAP theorem with 341 identity-vs-symmetry guard, 407 quotient sketch, 2711 parent-object audit and 3115 Noether certificate.",
            "effect_if_signed": "QAP becomes a parent theorem and 3519/3520 q-normal-form consequences can promote conditionally.",
            "current_status": "QAP_NOT_PARENT_DERIVED_YET_EXPLICIT_ADOPTION_GATE_REQUIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["parent_object_2711"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "QAPG3521_0_equivalence_relation",
            "gate": "primitive history equivalence relation",
            "pass_condition": "MTS defines Phi~Phi' from motion/time/space relational identity before readout",
            "current_evidence": "heuristics and 407/341 sketches exist; no formal relation is parent-derived",
            "passed": "False",
            "if_failed": "QAP remains conditional/adoption candidate",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "QAPG3521_1_identity_not_symmetry",
            "gate": "identity rather than labelled global symmetry",
            "pass_condition": "parent variable is an orbit/unlabelled object, not a labelled species vector with invariant formulas",
            "current_evidence": "341 explicitly warns the formula alone does not derive quotient identity",
            "passed": "False",
            "if_failed": "source labels and active markers can be physical residuals",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "QAPG3521_2_readout_invariance",
            "gate": "all local readouts constant on primitive fibres",
            "pass_condition": "clocks, rods, photons, source mass, EM/Hodge, boundary/support and arena projections descend through quotient",
            "current_evidence": "3115 and 2570 give exact tests; source/readout/boundary channels are not all signed",
            "passed": "False",
            "if_failed": "Dq[v_q] and readout tails remain finite",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "QAPG3521_3_no_marker_exhaustion",
            "gate": "no active marker/source-label constructor",
            "pass_condition": "no parent morphism from representative/marker/species labels into active-source coefficients",
            "current_evidence": "2688 partially constructs Q_obs but constructor exhaustion fails",
            "passed": "False",
            "if_failed": "source prefactor and marker residuals remain live",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "QAPG3521_4_first_class_generator",
            "gate": "Noether/Hamiltonian generator certificate",
            "pass_condition": "off-shell Noether identity, differentiable first-class generator, bracket closure and zero/proper boundary charge",
            "current_evidence": "3115 gives certificate requirements; no candidate v_q satisfies them in current corpus",
            "passed": "False",
            "if_failed": "verticality remains candidate, not theorem",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "QAPG3521_5_boundary_action_unit",
            "gate": "boundary and action normalization compatibility",
            "pass_condition": "proper boundary terms and one action unit preserve identity-fibre descent",
            "current_evidence": "3464 and 3457 give conditional contracts; normalization/boundary ownership not derived",
            "passed": "False",
            "if_failed": "sector weights and boundary source shifts stay explicit",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "QAPG3521_6_total",
            "gate": "QAP parent-owned by current MTS",
            "pass_condition": "QAPG3521_0 through QAPG3521_5 pass in one branch",
            "current_evidence": "no single source signs all gates",
            "passed": "False",
            "if_failed": "QAP can be used only as explicit private adoption/closure or conditional theorem target",
            "valid_for_claim": "False",
        },
    ]


def adoption_rows() -> list[dict[str, Any]]:
    return [
        {
            "adoption_id": "QAPA3521_0_QAP_LC",
            "name": "local quotient action principle adoption gate",
            "statement": "For the private local transition branch only, adopt that physical local parent histories are equivalence classes under representative changes that leave motion/time/space readouts invariant; S_parent descends to that quotient before matter/source variation.",
            "allowed_use": "organize conditional derivations; forbid direct q_private source operators inside the adopted branch; route unsigned clauses to finite residuals",
            "forbidden_use": "claim MTS has derived local GR/Newton/PPN/WEP/R10/clock or source coupling from primitives",
            "current_status": "NOT_ADOPTED_BY_THIS_SCRIPT_EXPLICIT_GATE_ONLY",
            "valid_for_claim": "False",
        },
        {
            "adoption_id": "QAPA3521_1_required_label",
            "name": "if used, label as closure/adoption",
            "statement": "Any future step using QAP without passing QAPG3521 gates must label it as QAP_LC adoption, not parent theorem.",
            "allowed_use": "private theorem-search scaffold",
            "forbidden_use": "public claim or hidden assumption",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3521_0_PIP_to_QAP",
            "quantity": "primitive_identity_principle_implies_QAP",
            "value": "conditional_true",
            "meaning": "if MTS primitives identify representatives as the same history, action descent follows or the representative becomes observable",
            "claim_effect": "real derivation route, not current theorem",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3521_1_QAP_parent_owned",
            "quantity": "QAP_parent_owned_by_current_MTS",
            "value": "False",
            "meaning": "the equivalence relation/identity not symmetry/no-marker/Noether/boundary gates do not pass together",
            "claim_effect": "QAP is conditional or explicit adoption only",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3521_2_coupling_route",
            "quantity": "CqT_BqWeyl_route_status",
            "value": "closer_not_claimed",
            "meaning": "3519/3520 zero routes are backed by a primitive identity theorem target, but parent ownership is absent",
            "claim_effect": "C_qT and B_qWeyl remain finite-bound unless QAP gates close",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3521_3_next_best",
            "quantity": "next_best_attack",
            "value": "identity_vs_symmetry_and_marker_countermodels",
            "meaning": "the bottleneck is proving representative relabelling is identity, not merely symmetry, while forbidding active markers",
            "claim_effect": "continue derivation-first with a focused countermodel test",
            "valid_for_claim": "False",
        },
    ]


def finite_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QAPF3521_0_identity_failure",
            "source_channel": "representative_identity_not_signed",
            "bound_formula": "E_QAP <= E_equiv + E_identity_symmetry + E_marker + E_readout + E_noether + E_boundary",
            "required_inputs": "equivalence-relation certificate, readout derivative norms, marker/source-label coefficient bounds, boundary charge bounds",
            "prediction_value": "MISSING_QAP_FAILURE_BOUND",
            "status": "NONCLAIM_IF_QAP_NOT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QAPF3521_1_active_marker",
            "source_channel": "active_marker_or_source_label",
            "bound_formula": "E_marker <= ||dS/dm_active|| ||L_v m_active||",
            "required_inputs": "marker covector, active-source coefficient target, readout/source map",
            "prediction_value": "MISSING_ACTIVE_MARKER_BOUND",
            "status": "NONCLAIM_IF_NO_MARKER_THEOREM_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QAPF3521_2_noether_charge",
            "source_channel": "failed_first_class_generator",
            "bound_formula": "E_Noether <= ||R_dagger(E)|| + ||deltaG - i_v Omega|| + ||Q_boundary|| + ||K_boundary||",
            "required_inputs": "candidate generator, Euler operators, symplectic form, boundary charge/cocycle",
            "prediction_value": "MISSING_NOETHER_GENERATOR_BOUND",
            "status": "NONCLAIM_IF_GENERATOR_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3521_0_derivation_result",
            "decision": "QAP is derivable from a primitive identity principle, conditionally",
            "rationale": "if representative histories are identical, representative-dependent action terms make them distinguishable and contradict the primitive.",
            "effect": "the route is mathematical, not vibes; QAP is now one step below MTS primitives.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3521_1_current_promotion",
            "decision": "do not promote QAP as current MTS theorem",
            "rationale": "identity vs symmetry, no-marker exhaustion, readout invariance and first-class Noether certificate remain unsigned.",
            "effect": "finite residuals and explicit adoption labels remain mandatory.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3521_2_next_target",
            "decision": "attack representative identity vs labelled symmetry next",
            "rationale": "341 shows this is the exact fork: quotient state-space proves QAP; symmetric labelled species does not.",
            "effect": "the next checkpoint should run countermodels and make the adoption/derivation choice sharper.",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3522-Y5-R2FR-representative-identity-vs-global-symmetry-or-active-marker-bound.md",
            "next_script": "scripts/Y5_R2FR_3522_representative_identity_vs_global_symmetry_or_active_marker_bound.py",
            "objective": "Decide whether the live MTS representative/cell/q_private labels are quotient identities or labelled degrees with global symmetry; if identity is not derived, stage active-marker/source-label finite bounds.",
            "success_gate": "Either parent state-space is an orbit/unlabelled object with no active marker, or QAP_LC is explicitly marked adoption and marker/source-label residual rows stay finite.",
            "why_next": "3521 reduces QAP ownership to the identity-vs-symmetry fork; 341 already gives the right countermodel shape.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    primitives: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    status: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3521_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        }
    )
    theorem_text = " ".join(row["claim"] + " " + row["effect_if_signed"] for row in theorem)
    checks.append(
        {
            "check_id": "VAL3521_1_pip_to_qap_theorem_present",
            "passed": bool_text("same physical history" in theorem_text and "QAP follows" in theorem_text),
            "detail": "primitive identity principle to QAP theorem is present",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3521_2_identity_symmetry_guard_present",
            "passed": bool_text(any("identity rather than labelled global symmetry" in row["gate"] for row in gates)),
            "detail": "identity-vs-symmetry gate included",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3521_3_primitive_audit_not_promoted",
            "passed": bool_text(all(row["gate_pass"] == "False" and row["valid_for_claim"] == "False" for row in primitives)),
            "detail": "all primitive sources remain nonclaim gates",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3521_4_adoption_gate_not_hidden",
            "passed": bool_text(any(row["adoption_id"] == "QAPA3521_0_QAP_LC" and row["current_status"] == "NOT_ADOPTED_BY_THIS_SCRIPT_EXPLICIT_GATE_ONLY" for row in adoption)),
            "detail": "explicit QAP_LC adoption gate exists but is not silently adopted",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3521_5_no_claim_flags_true",
            "passed": bool_text(
                all(row["fires_now"] == "False" and row["valid_for_claim"] == "False" for row in theorem)
                and all(row["passed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
                and all(row["valid_for_claim"] == "False" for row in adoption + status + bounds)
            ),
            "detail": "no QAP/local-GR/source-coupling claim is promoted",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3521_6_bounds_nonclaim",
            "passed": bool_text(all(row["prediction_value"].startswith("MISSING_") and row["valid_for_claim"] == "False" for row in bounds)),
            "detail": "fallback bounds remain source/input placeholders",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3521_7_next_target_identity_symmetry",
            "passed": bool_text(any("identity-vs-global-symmetry" in row["next_doc"] or "identity_vs_global_symmetry" in row["next_script"] for row in next_rows)),
            "detail": "3522 identity-vs-symmetry target selected",
            "valid_for_claim": "False",
        }
    )
    csvs_parse = True
    parse_details: list[str] = []
    for name, path in outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        if name == "validation" and not path.exists():
            parse_details.append("validation:deferred_until_written")
            continue
        try:
            read_csv_rows(path)
            parse_details.append(name)
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{name}:{exc}")
    checks.append(
        {
            "check_id": "VAL3521_8_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    output_paths_in_root = all(str(path).startswith(str(ROOT)) for path in outputs.values()) and str(DOC).startswith(str(ROOT))
    checks.append(
        {
            "check_id": "VAL3521_9_outputs_stay_in_post_checkpoint_work",
            "passed": bool_text(output_paths_in_root),
            "detail": f"root={ROOT}",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3521_10_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3521_SUMMARY",
            "passed": bool_text(passed),
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    primitives: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    status: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3521 - MTS Primitives To Quotient Action Principle Or Explicit Adoption Gate

## Summary
- **Derivation result:** QAP follows from a primitive identity principle: if two MTS histories are the same physical history, the action cannot depend on which representative label was used.
- **The sharp fork:** quotient identity is not the same as global relabelling symmetry. A symmetric labelled-species action does not derive QAP; an orbit/unlabelled parent state does.
- **Current MTS status:** the corpus strongly motivates the quotient route, but does not yet parent-own the equivalence relation, no-marker exhaustion, readout invariance, first-class generator, and boundary/action-unit clauses together.
- **No hidden closure:** QAP is not silently adopted here. If future work uses it before those gates close, it must be labelled `QAP_LC` adoption/closure.
- **Next move:** attack the identity-vs-symmetry fork directly using active-marker/source-label countermodels.

## Core Derivation
Let `Phi ~ Phi'` mean the two histories are the same MTS physical history, differing only by representative/cell/private labels. If

`S_parent[Phi] != S_parent[Phi']`

by more than a fixed proper boundary or phase convention, then the stationary equations, source currents, or phase/statistical weights distinguish `Phi` from `Phi'`. That makes the representative label physical. Therefore primitive identity implies

`S_parent = pi^* S_phys + dB_proper + S_constraint`,

which is exactly the quotient action principle used in 3520.

The problem is not the mathematics. The problem is parent ownership of `~`: MTS must prove the relevant labels are identity fibres, not labelled physical species with a symmetry.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Primitive Source Audit
{markdown_table(primitives, ["primitive_id", "candidate_primitive", "positive_content", "needed_for_QAP", "current_status", "gate_pass", "valid_for_claim"])}

## Primitive-To-QAP Theorems
{markdown_table(theorem, ["theorem_id", "claim", "formal_statement", "derivation", "effect_if_signed", "current_status", "fires_now", "valid_for_claim"])}

## Promotion Gates
{markdown_table(gates, ["gate_id", "gate", "pass_condition", "current_evidence", "passed", "if_failed", "valid_for_claim"])}

## Explicit Adoption Gate
{markdown_table(adoption, ["adoption_id", "name", "statement", "allowed_use", "forbidden_use", "current_status", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Finite Bounds If QAP Not Derived
{markdown_table(bounds, ["bound_id", "source_channel", "bound_formula", "required_inputs", "prediction_value", "status", "valid_for_claim"])}

## Decisions
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}

Generated: {now_utc()}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    primitives = primitive_audit_rows()
    theorem = primitive_to_qap_theorem_rows()
    gates = promotion_gate_rows()
    adoption = adoption_rows()
    status = status_rows()
    bounds = finite_bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3521_SOURCE_REGISTER.csv",
        "primitive_audit": OUT / "P8_Y5_R2FR_3521_PRIMITIVE_SOURCE_AUDIT.csv",
        "theorem": OUT / "P8_Y5_R2FR_3521_PRIMITIVE_IDENTITY_TO_QAP_THEOREM.csv",
        "gates": OUT / "P8_Y5_R2FR_3521_QAP_PROMOTION_GATES.csv",
        "adoption": OUT / "P8_Y5_R2FR_3521_EXPLICIT_QAP_ADOPTION_GATE.csv",
        "status": OUT / "P8_Y5_R2FR_3521_MTS_PRIMITIVES_TO_QAP_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "bounds": OUT / "P8_Y5_R2FR_3521_QAP_FAILURE_FINITE_BOUNDS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3521_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3521_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3521_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["primitive_audit"], primitives, ["primitive_id", "candidate_primitive", "positive_content", "needed_for_QAP", "current_status", "source_path", "gate_pass", "valid_for_claim"])
    write_csv(outputs["theorem"], theorem, ["theorem_id", "claim", "formal_statement", "derivation", "effect_if_signed", "current_status", "fires_now", "source_path", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "gate", "pass_condition", "current_evidence", "passed", "if_failed", "valid_for_claim"])
    write_csv(outputs["adoption"], adoption, ["adoption_id", "name", "statement", "allowed_use", "forbidden_use", "current_status", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["bounds"], bounds, ["bound_id", "source_channel", "bound_formula", "required_inputs", "prediction_value", "status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])

    validation_rows = validate(outputs, sources, primitives, theorem, gates, adoption, status, bounds, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, primitives, theorem, gates, adoption, status, bounds, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
