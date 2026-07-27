from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3522-Y5-R2FR-representative-identity-vs-global-symmetry-or-active-marker-bound.md"
CANONICAL_STATUS = OUT / "P8_EM_representative_identity_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3522": {
        "path": Path(__file__).resolve(),
        "role": "3522 generator",
    },
    "doc_3521": {
        "path": ROOT / "3521-Y5-R2FR-MTS-primitives-to-quotient-action-principle-or-explicit-adoption-gate.md",
        "role": "QAP primitive-identity handoff",
    },
    "next_3521": {
        "path": OUT / "P8_Y5_R2FR_3521_NEXT_TARGET.csv",
        "role": "3521-selected 3522 target",
    },
    "qap_status_3521": {
        "path": OUT / "P8_EM_MTS_primitives_to_QAP_status.csv",
        "role": "canonical QAP parent-ownership status",
    },
    "identity_source_341": {
        "path": ROOT / "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "role": "same-formula trap, quotient orbit, active-marker countermodel",
    },
    "quotient_sketch_407": {
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive relational quotient/action theorem target",
    },
    "sort_constructor_2688": {
        "path": ROOT / "2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md",
        "role": "source-label constructor exhaustion blocker",
    },
    "parent_object_2711": {
        "path": ROOT / "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md",
        "role": "parent action object ownership blocker",
    },
    "matter_coupling_2587": {
        "path": ROOT / "2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
        "role": "minimal quotient matter-coupling contract and no-source-slot clause",
    },
    "vertical_noether_3115": {
        "path": ROOT / "3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md",
        "role": "local vertical Noether certificate plus Poynting/Hodge readout guard",
    },
    "em_owner_1099": {
        "path": ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        "role": "EM kinetic/gauge-normalization owner and alpha residual guard",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, item in SOURCES.items():
        path = item["path"]
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_text(path.exists()),
                "role": item["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def countermodel_rows() -> list[dict[str, Any]]:
    state = [1.0, 2.0, 5.0]
    swap = [5.0, 2.0, 1.0]
    trace_state = sum(state)
    trace_swap = sum(swap)
    spectrum_state = sorted(state)
    spectrum_swap = sorted(swap)
    class_action_state = sum(value * value for value in state)
    class_action_swap = sum(value * value for value in swap)
    fixed_active_state = state[0]
    fixed_active_swap = swap[0]
    covariant_marker_selected_state = state[0]
    covariant_marker_selected_swap = swap[2]
    rows = [
        {
            "test_id": "CM3522_0_trace_class_function",
            "model": "quotient_orbit",
            "quantity": "sum_i h_i",
            "state_value": f"{trace_state:.6g}",
            "relabelled_value": f"{trace_swap:.6g}",
            "invariant_under_relabel": bool_text(trace_state == trace_swap),
            "distinguishes_representatives": "False",
            "meaning": "trace/sum is a class function and can descend to C/G",
            "claim_effect": "supports conditional quotient theorem only",
            "valid_for_claim": "False",
        },
        {
            "test_id": "CM3522_1_spectrum_class_function",
            "model": "quotient_orbit",
            "quantity": "sorted spectrum",
            "state_value": str(spectrum_state),
            "relabelled_value": str(spectrum_swap),
            "invariant_under_relabel": bool_text(spectrum_state == spectrum_swap),
            "distinguishes_representatives": "False",
            "meaning": "spectrum/multiset is a class function and can be an unlabelled parent variable",
            "claim_effect": "supports conditional quotient theorem only",
            "valid_for_claim": "False",
        },
        {
            "test_id": "CM3522_2_same_formula_trap",
            "model": "symmetric_labelled_species",
            "quantity": "sum_i h_i^2",
            "state_value": f"{class_action_state:.6g}",
            "relabelled_value": f"{class_action_swap:.6g}",
            "invariant_under_relabel": bool_text(class_action_state == class_action_swap),
            "distinguishes_representatives": "True",
            "meaning": "a symmetric formula does not decide whether h and pi.h are one state or two symmetry-related labelled states",
            "claim_effect": "symmetry alone cannot derive QAP",
            "valid_for_claim": "False",
        },
        {
            "test_id": "CM3522_3_fixed_active_marker",
            "model": "fixed_spurion_marker",
            "quantity": "h_active",
            "state_value": f"{fixed_active_state:.6g}",
            "relabelled_value": f"{fixed_active_swap:.6g}",
            "invariant_under_relabel": bool_text(fixed_active_state == fixed_active_swap),
            "distinguishes_representatives": "True",
            "meaning": "a fixed active selector is not a function on C/G and reopens source-label couplings",
            "claim_effect": "active-marker terms must be theorem-zero or bounded",
            "valid_for_claim": "False",
        },
        {
            "test_id": "CM3522_4_covariant_material_marker",
            "model": "extended_quotient_with_marker",
            "quantity": "selected material value",
            "state_value": f"{covariant_marker_selected_state:.6g}",
            "relabelled_value": f"{covariant_marker_selected_swap:.6g}",
            "invariant_under_relabel": bool_text(covariant_marker_selected_state == covariant_marker_selected_swap),
            "distinguishes_representatives": "False",
            "meaning": "a material marker can descend on (state,marker)/G, but it remains physical data rather than a pure identity fibre",
            "claim_effect": "extended quotient allowed; local source residuals still need owner/bounds",
            "valid_for_claim": "False",
        },
    ]
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "QI3522_0_orbit_identity_lemma",
            "claim": "Parent orbit state-space gives representative identity.",
            "formal_statement": "Let G act on candidate prestates C and let q:C->C/G. If physical histories are elements of C/G, and S, matter action, source currents, EM/Hodge readouts and boundary data factor through q up to proper boundary/2pi phase, then vertical relabellings in ker(Dq) are identity directions.",
            "proof_or_counterproof": "Any representative-dependent variation would define a function or current on C rather than C/G, making the representative observable. Therefore it is not a physical bulk term on the quotient.",
            "effect_if_signed": "QAP identity fibre closes for that sector; direct q_private/source-label bulk coefficients are illegal.",
            "current_mts_status": "CONDITIONAL_THEOREM_ONLY_PARENT_ORBIT_NOT_SIGNED",
            "fires_for_live_mts": "False",
            "source_path": str(SOURCES["identity_source_341"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "QI3522_1_symmetry_insufficiency",
            "claim": "Invariant labelled-species formulas do not prove quotient identity.",
            "formal_statement": "S(h)=S(g.h) is compatible with either a function on C/G or a symmetric action on labelled C. The formula alone cannot decide the ontology.",
            "proof_or_counterproof": "The same sum/spectrum formula passes relabelling invariance in both cases. In the labelled case h and g.h are different states related by global symmetry, so direct source labels may still be physical after an active selector is supplied.",
            "effect_if_signed": "Forces the parent-state-space definition to carry the proof, not cosmetic invariance.",
            "current_mts_status": "EXACT_GUARD_ACTIVE",
            "fires_for_live_mts": "True",
            "source_path": str(SOURCES["identity_source_341"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "QI3522_2_fixed_marker_obstruction",
            "claim": "Fixed active markers break pure quotient identity.",
            "formal_statement": "If a fixed marker m selects representatives or source components and L_v m != 0 along the proposed quotient fibre, then any coefficient A(m) creates a physical residual L_v S != 0.",
            "proof_or_counterproof": "The fixed-active countermodel changes h_active under a relabelling even while trace/spectrum remain invariant. It is not a class function on C/G.",
            "effect_if_signed": "No-marker theorem or finite active-marker bound is mandatory before local-GR/source-coupling promotion.",
            "current_mts_status": "OBSTRUCTION_ACTIVE",
            "fires_for_live_mts": "True",
            "source_path": str(SOURCES["sort_constructor_2688"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "QI3522_3_covariant_marker_extension",
            "claim": "Covariant material markers may descend only as extended physical data.",
            "formal_statement": "A pair (state,marker)/G can be a quotient, but the marker is then part of the physical public state, not a representative-erased private label.",
            "proof_or_counterproof": "A marker transformed with the material state preserves selected value under relabelling, but this proves an extended quotient, not marker silence.",
            "effect_if_signed": "Material/source markers are allowed only if their stress/current effect is included in public Hilbert source or bounded as residual.",
            "current_mts_status": "EXTENDED_QUOTIENT_ROUTE_NOT_LOCAL_SILENCE",
            "fires_for_live_mts": "True",
            "source_path": str(SOURCES["matter_coupling_2587"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "QI3522_4_source_coupling_corollary",
            "claim": "Source universality follows from quotient identity plus minimal matter functor, not from symmetry alone.",
            "formal_statement": "If S_matter=Sbar[q(Phi),psi,theta] and no source-only slot/marker exists before variation, then Hilbert stress/current descent is universal on the quotient; otherwise Delta_w, b_alpha, Hodge/Poynting and support residuals remain.",
            "proof_or_counterproof": "Functional variation of a q-factored matter action cannot see ker(Dq); source-label weights require an extra non-q morphism and therefore are exactly the missing no-marker/source-functor owner.",
            "effect_if_signed": "Would connect MTS to GR/Newton source coupling through Hilbert stress rather than fitted GM.",
            "current_mts_status": "BEST_NEXT_CONSTRUCTION_TARGET_NOT_SIGNED",
            "fires_for_live_mts": "False",
            "source_path": str(SOURCES["matter_coupling_2587"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "QI3522_5_EM_Poynting_readout_corollary",
            "claim": "Poynting flow is safe only when Maxwell/Hodge ownership descends through the same quotient.",
            "formal_statement": "If Hodge star, gauge norm, current normalization and EM stress are functions of q(Phi), the Poynting vector is part of Hilbert stress. If any EM constitutive/Hodge/gauge-normalization marker lies outside q, it creates alpha/clock/WEP/R10/source residuals.",
            "proof_or_counterproof": "This is the EM version of the marker theorem: Poynting is not an external magic source, but its readout can expose a nonquotient marker.",
            "effect_if_signed": "Gives a derivation target for Maxwell-to-Hilbert source coupling inside local GR.",
            "current_mts_status": "CONDITIONAL_NOT_SIGNED_EM_OWNER_OPEN",
            "fires_for_live_mts": "False",
            "source_path": str(SOURCES["vertical_noether_3115"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def live_label_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "label_id": "LL3522_0_finite_cell_labels",
            "candidate_label": "finite cell/fibre labels",
            "identity_route": "parent variable is orbit/multiset/spectrum/basis-free fibre object",
            "symmetry_only_counterroute": "labelled 27-component species vector with symmetric formula",
            "active_marker_hazard": "fixed active selector P_active or source mask",
            "current_verdict": "CONDITIONAL_TEMPLATE_NOT_PARENT_ORIGIN_SIGNED",
            "required_to_promote": "derive parent state-space as unlabelled orbit and prove no fixed marker extension",
            "source_path": str(SOURCES["identity_source_341"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "label_id": "LL3522_1_q_private_representative",
            "candidate_label": "q_private/local representative direction",
            "identity_route": "q_private lies entirely in ker(Dq) and has first-class zero-boundary Noether generator",
            "symmetry_only_counterroute": "private shift changes Khat/Gamma/q_loc/source projections",
            "active_marker_hazard": "representative coefficient appears in source or PPN projection",
            "current_verdict": "NOETHER_CERTIFICATE_NOT_SIGNED",
            "required_to_promote": "off-shell Noether identity, Hamiltonian generator, bracket closure and readout silence",
            "source_path": str(SOURCES["vertical_noether_3115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "label_id": "LL3522_2_matter_source_labels",
            "candidate_label": "matter species/source labels",
            "identity_route": "minimal matter action factors through one observed stack q(Phi)",
            "symmetry_only_counterroute": "species weights w_A(X), current rescalings c_A(X), shadow frames",
            "active_marker_hazard": "source-only slot changes Hilbert current before/after readout",
            "current_verdict": "MINIMAL_MATTER_CONTRACT_NOT_UNIQUE_PARENT_DERIVED",
            "required_to_promote": "source-label forgetting functor plus no-source-slot uniqueness proof",
            "source_path": str(SOURCES["matter_coupling_2587"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "label_id": "LL3522_3_constructor_labels",
            "candidate_label": "active-source coefficient constructor labels",
            "identity_route": "Hom_parent(label/hidden/readout, Coeff_active_source)=empty_or_common",
            "symmetry_only_counterroute": "source coefficient grammar can still receive labels by syntax",
            "active_marker_hazard": "Delta_w_species, current rescale, marker-hidden, readout re-entry",
            "current_verdict": "CONSTRUCTOR_EXHAUSTION_UNSIGNED",
            "required_to_promote": "total parent action/source-label forgetting or finite Delta_w values",
            "source_path": str(SOURCES["sort_constructor_2688"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "label_id": "LL3522_4_EM_Hodge_Poynting_labels",
            "candidate_label": "EM Hodge/gauge-normalization/Poynting readout labels",
            "identity_route": "Hodge star, Z_EM, current normalization and Poynting stress are q-owned",
            "symmetry_only_counterroute": "hidden scalar or constitutive coefficient multiplies F^2 while preserving gauge symmetry",
            "active_marker_hazard": "alpha drift, WEP/R10/clock transfer, non-Hilbert Poynting source projection",
            "current_verdict": "EM_OWNER_CONDITIONAL_ONLY",
            "required_to_promote": "parent charge/gauge norm owner and no-extra-F2/no-hidden-constitutive theorem",
            "source_path": str(SOURCES["em_owner_1099"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3522_0_parent_state_orbit",
            "gate": "parent state is orbit/unlabelled object",
            "pass_condition": "Conf_parent is defined as C/G or an equivalent basis-free object before action/readout",
            "current_evidence": "341/407 give theorem templates; 2711 says parent object still not derived",
            "passed": "False",
            "if_failed": "symmetry-only branch remains possible",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3522_1_same_formula_guard",
            "gate": "same formula not used as proof",
            "pass_condition": "invariance of equations is treated as necessary not sufficient",
            "current_evidence": "countermodel CM3522_2 explicitly keeps invariant formula while labels remain physical",
            "passed": "True",
            "if_failed": "QAP would be smuggled from cosmetic symmetry",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3522_2_no_fixed_active_marker",
            "gate": "no fixed active/source marker",
            "pass_condition": "no bulk coefficient or source current can depend on a fixed selector outside q",
            "current_evidence": "2688/2587 keep source-slot and marker residuals open",
            "passed": "False",
            "if_failed": "active-marker residual rows remain mandatory",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3522_3_readout_and_EM_descend",
            "gate": "readouts, Hodge, Poynting, source current descend through q",
            "pass_condition": "DObs[v]=0 for clocks, rods, photons, source mass, EM/Hodge and Poynting/Hilbert source",
            "current_evidence": "3115 says this is conditional; EM owner is not fully signed in 1099",
            "passed": "False",
            "if_failed": "clock/alpha/WEP/R10/PPN/Poynting residual channels remain",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3522_4_first_class_identity_generator",
            "gate": "identity fibre has Noether generator",
            "pass_condition": "off-shell Noether identity, differentiable generator, bracket closure and zero/proper boundary charge",
            "current_evidence": "3115 gives certificate but no live candidate passes it",
            "passed": "False",
            "if_failed": "representative shifts are not proven gauge",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3522_5_total",
            "gate": "representative identity proven for live MTS",
            "pass_condition": "G3522_0 through G3522_4 pass together",
            "current_evidence": "only the same-formula guard passes; parent orbit, no-marker, readout/EM descent and Noether certificate remain unsigned",
            "passed": "False",
            "if_failed": "QAP_LC remains explicit closure/adoption or finite residual route",
            "valid_for_claim": "False",
        },
    ]


def marker_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "AMB3522_0_identity_failure_total",
            "residual_channel": "representative_identity_failure",
            "symbol": "E_identity",
            "bound_or_formula": "E_identity <= E_orbit_origin + E_marker + E_readout + E_Noether + E_boundary",
            "needed_inputs": "orbit parent proof or finite components; readout derivative norms; Noether defect; boundary charge",
            "units": "dimensionless after chosen action norm",
            "source_path": str(SOURCES["qap_status_3521"]["path"]),
            "current_status": "NONCLAIM_COMPONENTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "AMB3522_1_source_label_weight",
            "residual_channel": "source species/source weight",
            "symbol": "Delta_w_label",
            "bound_or_formula": "||P_perp w_source|| or theorem-zero from source-label forgetting functor",
            "needed_inputs": "source composition weights, common-mode projector, parent source functor, arena kernels",
            "units": "dimensionless",
            "source_path": str(SOURCES["sort_constructor_2688"]["path"]),
            "current_status": "VALUE_OR_ZERO_THEOREM_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "AMB3522_2_active_marker_action",
            "residual_channel": "fixed active marker in bulk action",
            "symbol": "epsilon_marker",
            "bound_or_formula": "|delta S_marker| <= ||dS/dm|| ||L_v m||",
            "needed_inputs": "marker covector, vertical action on marker, source/readout projection kernel",
            "units": "action_norm_or_dimensionless",
            "source_path": str(SOURCES["identity_source_341"]["path"]),
            "current_status": "MARKER_DERIVATIVE_OR_ZERO_THEOREM_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "AMB3522_3_source_current_rescale",
            "residual_channel": "Hilbert current/source normalization",
            "symbol": "epsilon_J",
            "bound_or_formula": "||Delta J_H|| <= ||c_A-c_common|| ||J_A|| + boundary/support terms",
            "needed_inputs": "current owner, ell_J parent scale, support/jump ledger, orbital/source map",
            "units": "source_current_norm",
            "source_path": str(SOURCES["matter_coupling_2587"]["path"]),
            "current_status": "CURRENT_OWNER_AND_SUPPORT_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "AMB3522_4_EM_Hodge_Poynting_marker",
            "residual_channel": "EM Hodge/gauge/Poynting readout",
            "symbol": "epsilon_EM",
            "bound_or_formula": "epsilon_EM <= ||L_v log Z_EM|| + ||L_v *g|| + ||L_v chi_constitutive|| + ||D Poynting[v]||",
            "needed_inputs": "parent charge lattice, gauge norm, Hodge owner, constitutive owner, clock/spectral projection",
            "units": "dimensionless_or_stress_norm",
            "source_path": str(SOURCES["vertical_noether_3115"]["path"]),
            "current_status": "EM_OWNER_OR_PRODUCT_BOUNDS_MISSING",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3522_0_conditional_identity_theorem",
            "quantity": "orbit_parent_plus_no_marker_implies_representative_identity",
            "value": "conditional_true",
            "meaning": "if the parent state is an orbit and all action/readout/source terms factor through it, QAP follows for that sector",
            "claim_effect": "real theorem route exists",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3522_1_live_mts_identity",
            "quantity": "representative_identity_parent_owned_by_current_MTS",
            "value": "False",
            "meaning": "the live corpus does not yet prove orbit parent state, no-marker exhaustion, EM/readout descent and Noether generator together",
            "claim_effect": "no local-GR/Newton/Maxwell/source-coupling claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3522_2_not_looping",
            "quantity": "new_information_from_3522",
            "value": "symmetry_alone_falsified",
            "meaning": "the route is narrowed: only orbit-parent identity can close QAP; invariant formula arguments are rejected",
            "claim_effect": "next work should build source-label forgetting functor, not repeat marker ledgers",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3522_3_next_best",
            "quantity": "next_best_attack",
            "value": "source_label_forgetting_functor_and_EM_Hodge_owner",
            "meaning": "the coupling problem is now the functor that erases representative/source labels before Hilbert and Maxwell variation",
            "claim_effect": "continue derivation-first toward GR/Newton/Maxwell source coupling",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3522_0_math_result",
            "decision": "accept conditional orbit-identity lemma",
            "rationale": "representative-dependent bulk terms make representatives observable, so true quotient state-space derives QAP",
            "effect": "we have a theorem target, not just a wish",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3522_1_reject_shortcut",
            "decision": "reject invariant-formula/symmetry shortcut",
            "rationale": "the same formula works for quotient variables and labelled species; parent state-space decides",
            "effect": "prevents smuggling local-GR silence from cosmetic symmetry",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3522_2_current_route",
            "decision": "do not promote live representative identity",
            "rationale": "source labels, active markers, EM/Hodge/Poynting readouts and Noether generator are not parent-signed together",
            "effect": "keep QAP_LC/nonclaim while attacking the source-label forgetting owner",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3523-Y5-R2FR-source-label-forgetting-functor-and-EM-Hodge-owner-or-marker-kernel-bound.md",
            "next_script": "scripts/Y5_R2FR_3523_source_label_forgetting_functor_and_EM_Hodge_owner_or_marker_kernel_bound.py",
            "objective": "Construct the parent functor that forgets representative/source labels before Hilbert and Maxwell variation; if it cannot be parent-signed, produce explicit source-label, Hodge, gauge-normalization and Poynting kernel bounds.",
            "success_gate": "Either S_matter and S_EM factor through q with no source-only/EM-marker slots, or all marker channels remain finite nonclaim rows with source/unit/projection requirements.",
            "why_next": "3522 proves symmetry is not enough and identifies source-label/EM-Hodge ownership as the coupling bottleneck.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    live_audit: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3522_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        }
    )
    counter_by_id = {row["test_id"]: row for row in countermodels}
    checks.append(
        {
            "check_id": "VAL3522_1_countermodels_execute",
            "passed": bool_text(
                counter_by_id["CM3522_0_trace_class_function"]["invariant_under_relabel"] == "True"
                and counter_by_id["CM3522_2_same_formula_trap"]["invariant_under_relabel"] == "True"
                and counter_by_id["CM3522_2_same_formula_trap"]["distinguishes_representatives"] == "True"
                and counter_by_id["CM3522_3_fixed_active_marker"]["invariant_under_relabel"] == "False"
                and counter_by_id["CM3522_4_covariant_material_marker"]["invariant_under_relabel"] == "True"
            ),
            "detail": "quotient functions pass, symmetry shortcut remains ambiguous, fixed marker fails, covariant marker extends quotient",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_2_orbit_identity_theorem_written",
            "passed": bool_text(any(row["theorem_id"] == "QI3522_0_orbit_identity_lemma" for row in theorems)),
            "detail": "conditional orbit identity lemma is written",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_3_symmetry_shortcut_rejected",
            "passed": bool_text(any(row["theorem_id"] == "QI3522_1_symmetry_insufficiency" and row["fires_for_live_mts"] == "True" for row in theorems)),
            "detail": "symmetry-only route is explicitly rejected as a proof of quotient identity",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_4_live_identity_not_promoted",
            "passed": bool_text(
                any(row["gate_id"] == "G3522_5_total" and row["passed"] == "False" for row in gates)
                and any(row["status_id"] == "STAT3522_1_live_mts_identity" and row["value"] == "False" for row in status)
            ),
            "detail": "current MTS representative identity is not promoted",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_5_live_label_audit_covers_core_sectors",
            "passed": bool_text({row["label_id"] for row in live_audit} >= {"LL3522_0_finite_cell_labels", "LL3522_1_q_private_representative", "LL3522_2_matter_source_labels", "LL3522_4_EM_Hodge_Poynting_labels"}),
            "detail": "cell, q_private, matter/source and EM/Hodge/Poynting labels audited",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_6_marker_bounds_nonclaim",
            "passed": bool_text(all(row["valid_for_claim"] == "False" and "MISSING" in row["current_status"] for row in bounds)),
            "detail": "active-marker/source/EM residual bounds remain nonclaim with missing theorem or numeric inputs",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_7_no_claim_flags_true",
            "passed": bool_text(
                all(row.get("valid_for_claim", "False") == "False" for row in sources + countermodels + theorems + live_audit + gates + bounds + status)
                and all(row["claim_allowed"] == "False" for row in decision_rows() + next_rows)
            ),
            "detail": "no local-GR/Newton/Maxwell/source-coupling claim is promoted",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_8_next_target_selected",
            "passed": bool_text(next_rows[0]["next_doc"].startswith("3523-Y5-R2FR-source-label-forgetting-functor")),
            "detail": "3523 source-label forgetting and EM-Hodge owner target selected",
            "valid_for_claim": "False",
        }
    )
    parsed_names: list[str] = []
    parse_ok = True
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed_names.append(name)
        except Exception:
            parse_ok = False
            parsed_names.append(f"{name}:PARSE_FAIL")
    checks.append(
        {
            "check_id": "VAL3522_9_csvs_parse",
            "passed": bool_text(parse_ok),
            "detail": "; ".join(parsed_names),
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_10_outputs_stay_in_post_checkpoint_work",
            "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())),
            "detail": f"root={ROOT}",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3522_11_formalization_workbench_not_targeted",
            "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())),
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3522_SUMMARY",
            "passed": bool_text(passed),
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    live_audit: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3522 - Representative Identity Vs Global Symmetry Or Active Marker Bound

## Summary
- **Actual step forward:** this checkpoint proves the conditional route: if MTS parent histories are orbit/unlabelled quotient states and all bulk action/readout/source terms factor through that quotient, representative relabelling is identity and QAP follows for that sector.
- **Shortcut rejected:** a symmetric labelled formula is not enough. The same formula can be a quotient class function or a labelled-species action with a global symmetry.
- **Coupling hinge:** fixed active/source markers, source-only matter slots, Hodge/gauge-normalization markers and Poynting readout leaks are the exact channels that stop source coupling from being silently universal.
- **Current verdict:** live MTS does not yet parent-own representative identity. The result is sharper than a missing ledger: the next derivation must build the source-label forgetting functor and EM/Hodge owner, or keep their marker kernels finite.
- **No public claim:** no local-GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital or source-coupling pass follows from 3522.

## Core Derivation
Let `G` be the candidate representative-relabel group acting on prestates `C`.

If the physical parent state is `C/G`, then physical quantities are functions on the orbit. A bulk term `B:C->R` is legal only when `B = Bbar o q` up to a proper boundary/phase convention. If `L_v B != 0` for a vertical relabelling `v in ker(Dq)`, then the representative is observable. That contradicts the premise that the representative was identity data.

Therefore:

`parent orbit state + q-factored action/readouts/sources + no marker extension => representative identity => QAP for that sector`.

But:

`S(h)=S(g.h)` alone only proves global invariance. It does not prove that `h` and `g.h` are the same physical history.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Countermodel Runner
{markdown_table(countermodels, ["test_id", "model", "quantity", "state_value", "relabelled_value", "invariant_under_relabel", "distinguishes_representatives", "meaning", "claim_effect", "valid_for_claim"])}

## Identity Theorems And Obstructions
{markdown_table(theorems, ["theorem_id", "claim", "formal_statement", "proof_or_counterproof", "effect_if_signed", "current_mts_status", "fires_for_live_mts", "source_path", "valid_for_claim"])}

## Live Label Audit
{markdown_table(live_audit, ["label_id", "candidate_label", "identity_route", "symmetry_only_counterroute", "active_marker_hazard", "current_verdict", "required_to_promote", "source_path", "valid_for_claim"])}

## Promotion Gates
{markdown_table(gates, ["gate_id", "gate", "pass_condition", "current_evidence", "passed", "if_failed", "valid_for_claim"])}

## Active Marker And Source Bounds
{markdown_table(bounds, ["bound_id", "residual_channel", "symbol", "bound_or_formula", "needed_inputs", "units", "source_path", "current_status", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    countermodels = countermodel_rows()
    theorems = theorem_rows()
    live_audit = live_label_audit_rows()
    gates = promotion_gate_rows()
    bounds = marker_bound_rows()
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3522_SOURCE_REGISTER.csv",
        "countermodels": OUT / "P8_Y5_R2FR_3522_IDENTITY_COUNTERMODELS.csv",
        "theorems": OUT / "P8_Y5_R2FR_3522_IDENTITY_THEOREMS.csv",
        "live_label_audit": OUT / "P8_Y5_R2FR_3522_LIVE_LABEL_AUDIT.csv",
        "promotion_gates": OUT / "P8_Y5_R2FR_3522_PROMOTION_GATES.csv",
        "marker_bounds": OUT / "P8_Y5_R2FR_3522_ACTIVE_MARKER_BOUNDS.csv",
        "status": OUT / "P8_Y5_R2FR_3522_REPRESENTATIVE_IDENTITY_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3522_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3522_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3522_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["countermodels"], countermodels, ["test_id", "model", "quantity", "state_value", "relabelled_value", "invariant_under_relabel", "distinguishes_representatives", "meaning", "claim_effect", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "claim", "formal_statement", "proof_or_counterproof", "effect_if_signed", "current_mts_status", "fires_for_live_mts", "source_path", "valid_for_claim"])
    write_csv(outputs["live_label_audit"], live_audit, ["label_id", "candidate_label", "identity_route", "symmetry_only_counterroute", "active_marker_hazard", "current_verdict", "required_to_promote", "source_path", "valid_for_claim"])
    write_csv(outputs["promotion_gates"], gates, ["gate_id", "gate", "pass_condition", "current_evidence", "passed", "if_failed", "valid_for_claim"])
    write_csv(outputs["marker_bounds"], bounds, ["bound_id", "residual_channel", "symbol", "bound_or_formula", "needed_inputs", "units", "source_path", "current_status", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, countermodels, theorems, live_audit, gates, bounds, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, countermodels, theorems, live_audit, gates, bounds, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
