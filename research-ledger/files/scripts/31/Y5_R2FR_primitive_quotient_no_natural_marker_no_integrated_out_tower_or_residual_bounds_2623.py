from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2623-Y5-R2FR-primitive-quotient-no-natural-marker-no-integrated-out-tower-or-residual-bounds.md"

PREFIX = "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "primitive_theorem": RESIDUALS / f"{PREFIX}_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
    "marker_audit": RESIDUALS / f"{PREFIX}_NO_NATURAL_MARKER_AUDIT.csv",
    "tower_audit": RESIDUALS / f"{PREFIX}_NO_INTEGRATED_OUT_TOWER_AUDIT.csv",
    "generator_matrix": RESIDUALS / f"{PREFIX}_GENERATOR_ELIMINATION_MATRIX.csv",
    "residual_fallback": RESIDUALS / f"{PREFIX}_RESIDUAL_BOUND_FALLBACK.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2623_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2623_00_2622_handoff_doc",
        "description": "2622 selects primitive quotient/no-marker/no-tower as the next lock",
        "path": ROOT / "2622-Y5-R2FR-Lovelock-hypothesis-audit-metric-only-second-order-or-residual-bounds.md",
        "needles": ["NEXT2622_0_primary", "PRIMITIVE_QUOTIENT_NO_MARKER_NO_TOWER_IS_NEXT", "GAP2622_2_no_integrated_out_tower"],
    },
    {
        "source_id": "SRC2623_01_2622_validation",
        "description": "2622 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_2622_VALIDATION.csv",
        "needles": ["VAL2622_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2623_02_2622_parent_gaps",
        "description": "2622 parent signature gap matrix",
        "path": RESIDUALS / "P8_Y5_LOVELOCK_GATE_2622_PARENT_SIGNATURE_GAP_MATRIX.csv",
        "needles": ["GAP2622_0_minimal_quotient", "GAP2622_2_no_integrated_out_tower"],
    },
    {
        "source_id": "SRC2623_03_965_primitive",
        "description": "historical primitive quotient/no-natural-marker theorem attempt",
        "path": ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
        "needles": ["PQ965_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS", "ALG965_9_verdict"],
    },
    {
        "source_id": "SRC2623_04_966_generators",
        "description": "historical local invariant generator elimination ranking",
        "path": ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md",
        "needles": ["GE966_7_verdict", "NOT_ELIMINATED_CURRENT_CORPUS", "DEC966_0_generator_audit"],
    },
    {
        "source_id": "SRC2623_05_423_minimality",
        "description": "minimality/no-extension theorem attempt",
        "path": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "needles": ["parent_universal_property_derived", "fail", "co_moving_marker_field"],
    },
    {
        "source_id": "SRC2623_06_710_scalar_descent",
        "description": "scalar/class descent and frame-transfer guard",
        "path": ROOT / "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md",
        "needles": ["DPC710_2_no_R_prefactor", "fail_current_corpus", "CE710_0_variable_prefactor"],
    },
    {
        "source_id": "SRC2623_07_967_readout",
        "description": "readout-after-variation schema and memory positive-operator lemma",
        "path": ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
        "needles": ["RAV967_5_verdict", "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED", "MPO967_6_verdict"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        rows.append(
            {
                "source_id": source["source_id"],
                "description": source["description"],
                "source_path": str(source["path"]),
                "exists": exists,
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": False,
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2623_0_current_handoff",
            "input_checkpoint": "2622",
            "what_it_gave": "the Lovelock/R2FR relative theorem now depends on primitive quotient, no-marker, and no-tower locks",
            "current_use": "attempt those parent locks directly",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2623_1_primitive_attempts",
            "input_checkpoint": "423/965",
            "what_it_gave": "fixed spurions can be conditionally excluded, but covariant material markers remain legal",
            "current_use": "retain the useful anti-cheat result while not overclaiming no-marker",
            "claim_status": "partial_relative_guard",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2623_2_generator_order",
            "input_checkpoint": "966",
            "what_it_gave": "ranked local invariant generators and selected readout projector as first tactical lock",
            "current_use": "make readout-after-variation the next 26xx target if the global theorem fails",
            "claim_status": "generator_order_imported",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2623_3_scalar_guard",
            "input_checkpoint": "710/963/964",
            "what_it_gave": "scalar prefactor and integrated-out tower countermodels remain live",
            "current_use": "stop R2/fR zero from being promoted until no-marker/no-tower is signed",
            "claim_status": "scalar_tower_retained",
            "valid_for_claim": False,
        },
    ]


def primitive_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PQT2623_0_target",
            "theorem_piece": "primitive quotient/no-natural-marker/no-integrated-out-tower theorem",
            "formal_target": "I_loc(Q_MTS)=I_geom[jets(e_obs)] + universal constants; no marker m, scalar sigma, or eliminated sector Z can enter S_eff[g] as F(sigma)R, R2, Ricci2, Weyl2, or nonlocal kernels",
            "current_status": "TARGET_DEFINED_NOT_PROVED",
            "partial_gain": "exactly states what would parent-sign the Lovelock/R2FR relative theorem",
            "remaining_gap": "universal property/minimal quotient object is not derived",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PQT2623_1_fixed_spurion",
            "theorem_piece": "fixed active spurions",
            "formal_target": "fixed non-transforming labels are not quotient-covariant parent fields",
            "current_status": "CONDITIONAL_PASS_IF_STRICT_QUOTIENT_PARENT_PROVEN",
            "partial_gain": "kills the crudest active-label cheat",
            "remaining_gap": "does not kill co-moving/covariant material markers or invariant scalars",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PQT2623_2_no_natural_marker_functor",
            "theorem_piece": "no nonconstant natural marker functor",
            "formal_target": "there exists no natural functor M:Q_MTS -> Marker that supplies matter-visible local scalar/vector labels beyond geometry and constants",
            "current_status": "NOT_DERIVED",
            "partial_gain": "names the exact category-level lock",
            "remaining_gap": "finite-cell spectra, domain classes, memory scalars, species constants, and orientation markers remain admissible",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PQT2623_3_no_extension_universal_property",
            "theorem_piece": "parent object is primitive/minimal",
            "formal_target": "Q_MTS is the full primitive parent object; covariant extensions Q_tilde=(Q,m)/G_rel are not parent-admissible unless gauge, universal auxiliary, or stress-free topological",
            "current_status": "NOT_DERIVED",
            "partial_gain": "turns minimality from taste into a theorem target",
            "remaining_gap": "co-moving material marker and species/domain marker countermodels remain legal",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PQT2623_4_no_integrated_out_tower",
            "theorem_piece": "hidden sector elimination cannot regenerate curvature towers",
            "formal_target": "for all eliminated Z_A, S_parent[g,Z_A[g]] has no generated R2/fR/Ricci2/Weyl2/nonlocal operator in the observed frame",
            "current_status": "NOT_DERIVED",
            "partial_gain": "identifies the exact hole that lets auxiliary scalars look harmless before reduction",
            "remaining_gap": "no proof of source-independent auxiliary solution, no kernel/locality theorem, no tower exclusion",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PQT2623_5_current_verdict",
            "theorem_piece": "primitive parent lock",
            "formal_target": "parent-sign metric-only second-order EH selection and R2/fR zero",
            "current_status": "THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "partial_gain": "the obstruction is finite and ordered, not vague",
            "remaining_gap": "readout projector, species constants, domain class, memory scalar, finite fibre, orientation marker, and hidden tower remain nonclaim",
            "valid_for_claim": False,
        },
    ]


def marker_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "marker_id": "MRK2623_0_readout_projector",
            "candidate_generator": "post-readout projector or representative section",
            "current_status": "CONDITIONAL_SCHEMA_THEOREM_READY_NOT_PARENT_SIGNED",
            "damage_if_live": "projector-dependent source/operator residuals can return through a varied reduced action",
            "kill_route": "prove readout is only R_read:Sol(S_parent)->Obs after variation and never an action argument",
            "fallback": "retain projector residual rows",
            "valid_for_claim": False,
        },
        {
            "marker_id": "MRK2623_1_species_constants",
            "candidate_generator": "species/source constants",
            "current_status": "NOT_UNIVERSALIZED",
            "damage_if_live": "WEP/source-charge/clock nonuniversality",
            "kill_route": "single matter functional and no source-only species prefactor theorem",
            "fallback": "retain epsilon_A/beta_source_normalized bounds",
            "valid_for_claim": False,
        },
        {
            "marker_id": "MRK2623_2_domain_class",
            "candidate_generator": "relative boundary/domain class",
            "current_status": "NOT_ELIMINATED",
            "damage_if_live": "branch selection can become posthoc local/cosmology selector",
            "kill_route": "parent-selected local domain with trivial relative class and boundary no-hair",
            "fallback": "retain domain/source class residual",
            "valid_for_claim": False,
        },
        {
            "marker_id": "MRK2623_3_memory_scalar",
            "candidate_generator": "memory/class scalar",
            "current_status": "POSITIVE_OPERATOR_ROUTE_UNSIGNED",
            "damage_if_live": "clock drift, gamma shift, fifth force, or non-EH prefactor",
            "kill_route": "positive local operator with zero source and boundary/zero-mode control",
            "fallback": "retain memory scalar amplitude-bound row",
            "valid_for_claim": False,
        },
        {
            "marker_id": "MRK2623_4_finite_fibre",
            "candidate_generator": "finite-cell fibre spectrum",
            "current_status": "NOT_DECOUPLED",
            "damage_if_live": "matter-visible scalar charge, mass gap, fifth-force scale",
            "kill_route": "unique source-independent gapped fibre ground state and matter-blind functor",
            "fallback": "retain finite-fibre residual",
            "valid_for_claim": False,
        },
        {
            "marker_id": "MRK2623_5_orientation_arrow",
            "candidate_generator": "orientation/time-arrow marker",
            "current_status": "CLASSIFIED_CONDITIONAL_NOT_EXCLUDED",
            "damage_if_live": "preferred-frame/parity/time-asymmetry residuals",
            "kill_route": "show contained in observed coframe/spin structure or global discrete datum",
            "fallback": "retain connection/preferred-frame residual",
            "valid_for_claim": False,
        },
        {
            "marker_id": "MRK2623_6_overall",
            "candidate_generator": "local invariant algebra",
            "current_status": "I_LOC_TRIVIALITY_NOT_DERIVED",
            "damage_if_live": "no-marker theorem cannot activate Lovelock/R2FR route",
            "kill_route": "eliminate generators one by one, starting with readout projector",
            "fallback": "explicit residual/bound vector",
            "valid_for_claim": False,
        },
    ]


def tower_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "tower_id": "TOW2623_0_auxiliary_scalar",
            "hidden_route": "auxiliary scalar integrated out",
            "example": "S=S_EH+int sqrt(-g)(-M^2 phi^2/2+beta phi R) -> beta^2 R^2/(2M^2)",
            "current_status": "LIVE_COUNTERMODEL",
            "needed_kill": "source-independent universal auxiliary solution with no R coupling, or infinite mass/zero coupling theorem",
            "fallback": "retain scalar-tower coefficient rows",
            "valid_for_claim": False,
        },
        {
            "tower_id": "TOW2623_1_marker_prefactor",
            "hidden_route": "quotient-invariant scalar multiplies R",
            "example": "int sqrt(-g) F(sigma_marker) R",
            "current_status": "LIVE_COUNTERMODEL",
            "needed_kill": "no-natural-marker plus no scalar/class EH prefactor descent clause",
            "fallback": "retain delta_AEH_scalar and gradient rows",
            "valid_for_claim": False,
        },
        {
            "tower_id": "TOW2623_2_memory_kernel",
            "hidden_route": "memory/nonlocal kernel",
            "example": "R Box^{-1} R or compact history kernel analogue",
            "current_status": "LIVE_COUNTERMODEL",
            "needed_kill": "locality reduction or positive-operator zero/source theorem",
            "fallback": "retain nonlocal kernel bounds",
            "valid_for_claim": False,
        },
        {
            "tower_id": "TOW2623_3_reduced_action",
            "hidden_route": "readout-reduced action varied as if parent",
            "example": "S_red[g,P_read] creates projector Euler terms",
            "current_status": "POLICY_BLOCKED_NOT_PARENT_THEOREM_BLOCKED",
            "needed_kill": "readout-after-variation parent domain theorem",
            "fallback": "retain projector residual rows",
            "valid_for_claim": False,
        },
        {
            "tower_id": "TOW2623_4_overall",
            "hidden_route": "all integrated-out curvature towers",
            "example": "S_eff[g] contains R2/fR/Ricci2/Weyl2/nonlocal terms after eliminating nonmetric sectors",
            "current_status": "NO_TOWER_THEOREM_NOT_PROVEN",
            "needed_kill": "parent universal no-tower theorem or sector-by-sector elimination",
            "fallback": "operator coefficient source-bound pack",
            "valid_for_claim": False,
        },
    ]


def generator_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "generator_id": "GEN2623_0_readout_projector",
            "generator": "post-readout projector",
            "current_status": "FIRST_TACTICAL_LOCK",
            "why_first": "it is a clean schema theorem: non-arguments of S_parent cannot vary",
            "next_test": "parent domain excludes readout variables and reduced-action backreaction",
            "valid_for_claim": False,
        },
        {
            "rank": 2,
            "generator_id": "GEN2623_1_species_constants",
            "generator": "species/source constants",
            "current_status": "RETAINED",
            "why_first": "large WEP/source impact but requires matter-functional schema",
            "next_test": "single Hilbert matter functional with no source-only slots",
            "valid_for_claim": False,
        },
        {
            "rank": 3,
            "generator_id": "GEN2623_2_memory_scalar",
            "generator": "memory/class scalar",
            "current_status": "RETAINED_WITH_POSITIVE_OPERATOR_ROUTE",
            "why_first": "can be attacked by a real energy identity if parent inputs exist",
            "next_test": "L_X positivity, J_X=0, boundary/zero-mode data",
            "valid_for_claim": False,
        },
        {
            "rank": 4,
            "generator_id": "GEN2623_3_finite_fibre",
            "generator": "finite-cell fibre spectrum",
            "current_status": "RETAINED",
            "why_first": "harder quotient-invariant scalar route",
            "next_test": "unique source-independent gapped ground state and matter blindness",
            "valid_for_claim": False,
        },
        {
            "rank": 5,
            "generator_id": "GEN2623_4_domain_class",
            "generator": "domain/relative class selector",
            "current_status": "RETAINED",
            "why_first": "needs local/cosmology selector theorem",
            "next_test": "selected local D, trivial relative class, boundary exchange no-hair",
            "valid_for_claim": False,
        },
        {
            "rank": 6,
            "generator_id": "GEN2623_5_orientation_arrow",
            "generator": "orientation/time-arrow marker",
            "current_status": "RETAINED",
            "why_first": "belongs with connection/torsion branch",
            "next_test": "geometry-contained arrow or preferred-frame residual",
            "valid_for_claim": False,
        },
    ]


def residual_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "RBF2623_0_marker_scalar",
            "residual": "delta_AEH_scalar, grad_ln_AEH_scalar, q_Aa",
            "trigger": "no-marker/no-prefactor theorem fails",
            "needed_sources": "coupling function, scalar mass/range, WEP/clock/PPN/R10 maps",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "fallback_id": "RBF2623_1_curvature_tower",
            "residual": "c_R2,c_fR,c_Ricci2,c_Weyl2,c_nonlocal",
            "trigger": "no-integrated-out-tower theorem fails",
            "needed_sources": "operator basis, units, coefficient ownership, local and cosmology maps",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "fallback_id": "RBF2623_2_projector_readout",
            "residual": "c_projector, reduced-action backreaction",
            "trigger": "readout-after-variation domain theorem fails",
            "needed_sources": "projector definition, commutator/readout norm, source-map projection",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "fallback_id": "RBF2623_3_memory_fibre",
            "residual": "c_memory, c_frame, c_fibre",
            "trigger": "positive-operator/unique-fibre theorem fails",
            "needed_sources": "lambda_gap, J_X norm, boundary data, observable couplings",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2623_0_covariant_material_marker",
            "failure_mode": "co-moving material marker remains covariant and matter-visible",
            "mathematical_form": "Q_tilde=(Q,m)/G_rel with m varied before readout",
            "retained": True,
            "why_survives": "primitive universal no-extension theorem is not derived",
            "what_kills_it": "no-natural-marker/no-extension theorem or retained residual tax",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2623_1_marker_prefactor",
            "failure_mode": "quotient-invariant marker scalar multiplies EH term",
            "mathematical_form": "S=int sqrt(-g) F(sigma) R",
            "retained": True,
            "why_survives": "no scalar/class descent clause is parent-signed",
            "what_kills_it": "no-prefactor theorem or scalar residual bound rows",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2623_2_auxiliary_tower",
            "failure_mode": "hidden auxiliary sector regenerates R2/fR after elimination",
            "mathematical_form": "phi ~ beta R/M^2 then S_eff includes R2",
            "retained": True,
            "why_survives": "no-integrated-out-tower theorem is not derived",
            "what_kills_it": "universal auxiliary/no-tower theorem",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2623_3_reduced_readout_action",
            "failure_mode": "readout projector enters through varied reduced action",
            "mathematical_form": "delta S_red[g,P_read]/delta g adds projector operator",
            "retained": True,
            "why_survives": "readout schema is conditional but not globally parent-signed",
            "what_kills_it": "parent domain excludes readout variables and reduced EFT theorem-zero credit",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2623_4_verdict",
            "failure_mode": "primitive parent lock remains unsigned",
            "mathematical_form": "I_loc(Q_MTS) != proven I_geom + constants",
            "retained": True,
            "why_survives": "2623 ranks generators but does not eliminate them",
            "what_kills_it": "2624 readout-after-variation schema, then memory/fibre/species/domain generator closures",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2623_0_primitive_quotient",
            "claim": "Q_MTS is proven primitive-minimal",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_UNIVERSAL_PROPERTY_NOT_DERIVED",
        },
        {
            "gate_id": "GATE2623_1_no_marker",
            "claim": "no natural marker/scalar functor exists",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_LOCAL_INVARIANT_GENERATORS_RETAINED",
        },
        {
            "gate_id": "GATE2623_2_no_tower",
            "claim": "integrated-out sectors cannot regenerate curvature towers",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_AUXILIARY_MEMORY_PROJECTOR_TOWERS_LIVE",
        },
        {
            "gate_id": "GATE2623_3_R2FR_zero",
            "claim": "R2/fR scalar branch is theorem-zero in MTS",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NO_MARKER_NO_TOWER_UNSIGNED",
        },
        {
            "gate_id": "GATE2623_4_local_GR",
            "claim": "local GR/Newton branch is derived",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PRIMITIVE_PARENT_AND_SOURCE_NORMALIZATION_GATES_OPEN",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2623_0_theorem_result",
            "decision": "PRIMITIVE_QUOTIENT_NO_MARKER_NO_TOWER_NOT_PROVEN",
            "reason": "fixed spurion exclusion is useful, but covariant markers, scalar prefactors, and hidden towers remain legal",
            "next_action": "do not promote Lovelock/R2FR relative theorem to absolute MTS claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2623_1_generator_strategy",
            "decision": "REMOVE_GENERATORS_ONE_BY_ONE",
            "reason": "the global primitive theorem is too strong for current evidence, but the generator list is finite and ordered",
            "next_action": "attack readout projector first because its schema theorem is cleanest",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2623_2_best_next",
            "decision": "READOUT_AFTER_VARIATION_PARENT_SCHEMA_IS_NEXT",
            "reason": "readout as a solution-space map cannot source parent equations; this can remove the first generator if the parent domain is signed",
            "next_action": "build 2624 readout-after-variation parent-domain signature or residual-bound fallback",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2623_0_primary",
            "selection_status": "selected",
            "target_doc": "2624-Y5-R2FR-readout-after-variation-parent-schema-theorem-or-generator-residual-bound.md",
            "target_script": "scripts/Y5_R2FR_readout_after_variation_parent_schema_theorem_or_generator_residual_bound_2624.py",
            "objective": "prove the parent action domain excludes readout variables and forbids reduced-action backreaction from earning theorem-zero credit; otherwise retain projector residual rows",
            "acceptance_gate": "R_read is a map Sol(S_parent)->Obs only after variation, no P_read argument exists in S_parent, and every reduced action is demoted to a retained branch",
            "claim_policy": "no local-GR or projector-zero claim unless the parent domain signature closes",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2623_1_fallback",
            "selection_status": "held_fallback",
            "target_doc": "2624b-Y5-R2FR-memory-positive-operator-input-audit-or-scalar-bound.md",
            "target_script": "scripts/Y5_R2FR_memory_positive_operator_input_audit_or_scalar_bound_2624b.py",
            "objective": "audit the positive-operator memory lemma inputs if readout is already signed or held",
            "acceptance_gate": "L_X positivity, J_X=0, boundary/zero-mode data, and observable projections are source-backed or retained nonclaim",
            "claim_policy": "fallback only; no invented numeric memory bounds",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "primitive": primitive_theorem_rows(),
        "markers": marker_audit_rows(),
        "towers": tower_audit_rows(),
        "generators": generator_matrix_rows(),
        "fallback": residual_fallback_rows(),
        "countermodel": countermodel_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
        "branch_copies": [],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_parse(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return True, sum(1 for _ in csv.DictReader(handle))
    except Exception:
        return False, 0


def copy_outputs() -> list[dict[str, Any]]:
    specs = [
        ("COPY2623_primitive_theorem", "primitive_theorem", OUTPUTS["primitive_theorem"], LOCAL_BOUNDS / "Primitive_quotient_theorem_attempt_2623_NONCLAIM.csv"),
        ("COPY2623_marker_audit", "marker_audit", OUTPUTS["marker_audit"], LOCAL_BOUNDS / "No_natural_marker_audit_2623_NONCLAIM.csv"),
        ("COPY2623_tower_audit", "tower_audit", OUTPUTS["tower_audit"], LOCAL_BOUNDS / "No_integrated_out_tower_audit_2623_NONCLAIM.csv"),
        ("COPY2623_generator_matrix", "generator_matrix", OUTPUTS["generator_matrix"], LOCAL_BOUNDS / "Generator_elimination_matrix_2623_NONCLAIM.csv"),
        ("COPY2623_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2623_READOUT_AFTER_VARIATION_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_key, source, target in specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        parsed, row_count = csv_parse(target)
        rows.append(
            {
                "copy_id": copy_id,
                "source_key": source_key,
                "copy_path": str(target),
                "copy_exists": target.exists(),
                "csv_parse": parsed,
                "row_count": row_count,
                "valid_for_claim": False,
            }
        )
    return rows


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["exists"] and row["needles_present"] for row in rows_map["sources"])


def primitive_not_proven(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "PQT2623_5_current_verdict"
        and row["current_status"] == "THEOREM_NOT_PROVEN_CURRENT_CORPUS"
        and not bool(row["valid_for_claim"])
        for row in rows_map["primitive"]
    )


def marker_blockers_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["marker_id"] == "MRK2623_6_overall" for row in rows_map["markers"]) and all(
        not bool(row["valid_for_claim"]) for row in rows_map["markers"]
    )


def tower_blockers_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["tower_id"] == "TOW2623_4_overall"
        and row["current_status"] == "NO_TOWER_THEOREM_NOT_PROVEN"
        for row in rows_map["towers"]
    )


def readout_ranked_first(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["rank"] == 1
        and row["generator_id"] == "GEN2623_0_readout_projector"
        and row["current_status"] == "FIRST_TACTICAL_LOCK"
        for row in rows_map["generators"]
    )


def residual_fallback_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return len(rows_map["fallback"]) >= 4 and all(row["status"] == "NONCLAIM_BOUND_REQUIRED" for row in rows_map["fallback"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["countermodel_id"] == "CM2623_4_verdict" and bool(row["retained"]) for row in rows_map["countermodel"])


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["claim_allowed"]) and row["status"] == "BLOCKED" for row in rows_map["claim_gates"])


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_like_keys = {"valid_for_claim", "claim_allowed", "score_ready", "claim_ready", "public_claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for field, value in row.items():
                if field in claim_like_keys and bool(value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and bool(row.get("valid_for_claim", False)):
                return False
            if "MISSING_" in joined and str(row.get("current_status", "")).upper() == "READY":
                return False
    return True


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["decision_id"] == "DEC2623_2_best_next"
        and row["decision"] == "READOUT_AFTER_VARIATION_PARENT_SCHEMA_IS_NEXT"
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["route_id"] == "NEXT2623_0_primary" and row["selection_status"] == "selected" for row in rows_map["next"])


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2623*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def csv_parse_all() -> bool:
    return all(csv_parse(path)[0] for key, path in OUTPUTS.items() if key != "validation" and path.exists())


def branch_copies_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return bool(rows_map["branch_copies"]) and all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"])


def check_row(check_id: str, passed: bool, detail: str, blocker: str = "") -> dict[str, Any]:
    return {
        "check_id": check_id,
        "result": "PASS" if passed else "FAIL",
        "detail": detail if passed else blocker,
        "valid_for_claim": False,
    }


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = [
        check_row("VAL2623_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present", "one or more cited source paths or needles missing"),
        check_row("VAL2623_01_primitive_not_proven", primitive_not_proven(rows_map), "primitive quotient theorem remains unproven/nonclaim", "primitive theorem was promoted"),
        check_row("VAL2623_02_marker_blockers_retained", marker_blockers_retained(rows_map), "marker generator blockers retained", "marker blockers missing or promoted"),
        check_row("VAL2623_03_tower_blockers_retained", tower_blockers_retained(rows_map), "no-integrated-out-tower blockers retained", "tower blockers missing or promoted"),
        check_row("VAL2623_04_readout_ranked_first", readout_ranked_first(rows_map), "readout projector selected as first tactical lock", "readout projector not selected first"),
        check_row("VAL2623_05_residual_fallback_nonclaim", residual_fallback_nonclaim(rows_map), "residual fallback rows remain nonclaim", "residual fallback rows missing or promoted"),
        check_row("VAL2623_06_countermodel_retained", countermodel_retained(rows_map), "primitive-lock countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL2623_07_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim", "one or more claim gates opened"),
        check_row("VAL2623_08_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL2623_09_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row("VAL2623_10_formalization_untouched", no_formalization_artifacts(), "no 2623 outputs found under formalization-workbench", "2623 outputs found under formalization-workbench"),
        check_row("VAL2623_11_decision_next", decision_next(rows_map), "decision selects readout-after-variation route", "decision route missing"),
        check_row("VAL2623_12_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL2623_13_branch_copies", branch_copies_pass(rows_map), "branch/local/queue copies exist and parse", "branch copies missing or malformed"),
        check_row("VAL2623_14_csv_parse", csv_parse_all(), "all generated 2623 CSVs parse", "one or more generated 2623 CSVs fail to parse"),
        check_row("VAL2623_15_pycache_absent", pycache_absent(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
    ]
    overall = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2623_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2623 primitive quotient no-natural-marker no-integrated-out-tower or residual bounds",
            "valid_for_claim": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    sections = [
        "# 2623 - Primitive Quotient No Natural Marker No Integrated Out Tower Or Residual Bounds",
        "## Summary\n"
        "- 2623 attacks the exact parent lock selected by 2622: primitive quotient, no natural marker, and no integrated-out curvature tower.\n"
        "- The result is clarifying but not a theorem-zero win: fixed active spurions are conditionally excluded, but covariant markers, scalar prefactors, and hidden towers remain legal without a stronger parent universal-property theorem.\n"
        "- The first tactical lock is now selected: readout-after-variation parent schema. If readout is only `R_read: Sol(S_parent)->Obs`, it cannot vary inside `S_parent`.\n"
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, R2/fR-zero, or `q_loc=0` claim is made.",
        "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "description", "source_path", "exists", "needles_present"]),
        "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "what_it_gave", "current_use", "claim_status"]),
        "## Primitive Quotient Theorem Attempt\n" + markdown_table(rows_map["primitive"], ["attempt_id", "theorem_piece", "formal_target", "current_status", "partial_gain", "remaining_gap"]),
        "## No Natural Marker Audit\n" + markdown_table(rows_map["markers"], ["marker_id", "candidate_generator", "current_status", "damage_if_live", "kill_route", "fallback"]),
        "## No Integrated Out Tower Audit\n" + markdown_table(rows_map["towers"], ["tower_id", "hidden_route", "example", "current_status", "needed_kill", "fallback"]),
        "## Generator Elimination Matrix\n" + markdown_table(rows_map["generators"], ["rank", "generator_id", "generator", "current_status", "why_first", "next_test"]),
        "## Residual Bound Fallback\n" + markdown_table(rows_map["fallback"], ["fallback_id", "residual", "trigger", "needed_sources", "status"]),
        "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "failure_mode", "mathematical_form", "retained", "why_survives", "what_kills_it"]),
        "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "claim_allowed", "status", "blocker"]),
        "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
        "## Next Target\n" + markdown_table(rows_map["next"], ["route_id", "selection_status", "target_doc", "target_script", "objective", "acceptance_gate", "claim_policy"]),
        "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
        "## Validation\n" + markdown_table(validations, ["check_id", "result", "detail", "valid_for_claim"]),
        "## Verdict\n"
        "This is not the magic proof yet, but it is movement in the right direction. The parent-lock obstruction is now finite: marker generators and hidden curvature towers are named, ranked, and routed. The cleanest next theorem is readout-after-variation, because it can remove one generator by domain logic rather than by fitting or taste.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["primitive_theorem"], rows_map["primitive"])
    write_csv(OUTPUTS["marker_audit"], rows_map["markers"])
    write_csv(OUTPUTS["tower_audit"], rows_map["towers"])
    write_csv(OUTPUTS["generator_matrix"], rows_map["generators"])
    write_csv(OUTPUTS["residual_fallback"], rows_map["fallback"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC_PATH.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"2623 validation {validations[-1]['result']}")
    print(f"doc={DOC_PATH}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
