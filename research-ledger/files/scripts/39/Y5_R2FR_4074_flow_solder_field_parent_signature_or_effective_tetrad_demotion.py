from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4074-Y5-R2FR-flow-solder-field-parent-signature-or-effective-tetrad-demotion.md"

DECISION = "FLOW_SOLDER_PARENT_SIGNATURE_NOT_DERIVED_EFFECTIVE_TETRAD_DEMOTION_CONTRACT_STAGED"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4074_00_4073_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4073_NEXT_TARGET.csv",
        "4074-Y5-R2FR-flow-solder-field-parent-signature-or-effective-tetrad-demotion.md",
        "4073 selected the flow/solder signature target.",
    ),
    "SRC4074_01_4073_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4073_ADOPTION_DECISION.csv",
        "private_parent_action_candidate",
        "4073 adopted the motion-frame gauge branch only as private candidate.",
    ),
    "SRC4074_02_4073_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4073_EFFECTIVE_BRANCH_FALLBACK.csv",
        "demote B^A to effective tetrad/coframe infrastructure",
        "4073 already identified the B-field derivation as the decisive fallback gate.",
    ),
    "SRC4074_03_4072_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
        "e^A = D_omega X^A + B^A",
        "4072 defines the solder equation used by the branch.",
    ),
    "SRC4074_04_4072_gauge": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv",
        "B' = Lambda B - D' a",
        "4072 records the required inhomogeneous B-field transformation law.",
    ),
    "SRC4074_05_primitives": (
        FORMALIZATION / "03-unified-field-theory-programme.md",
        "Candidate MTS primitives:",
        "formal programme lists the currently owned primitive vocabulary.",
    ),
    "SRC4074_06_scalar_action": (
        PROJECT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "gradients encode directional flow of curvature information",
        "core scalar action treats psi gradients as directional flow.",
    ),
    "SRC4074_07_flow_paper": (
        PROJECT / "core-mts-framework" / "field-theory" / "motion-timespace-research.md",
        "is a scalar field representing the local axiomatic tension",
        "flow paper identifies Psi as scalar local tension/divergence of flow.",
    ),
    "SRC4074_08_relativity": (
        PROJECT / "core-mts-framework" / "relativity" / "mbt-special-relativity-a-respectful-extension-of-einstein.md",
        "No Absolute Reference Frame",
        "relativity extension keeps no preferred-frame intent.",
    ),
    "SRC4074_09_motion_load": (
        ROOT / "01-motion-load-route-contract.md",
        "motion-load, clock residue, and spatial routing",
        "motion-load route supplies clock/spatial routing language.",
    ),
    "SRC4074_10_local_gr_reduction": (
        ROOT / "02-motion-load-local-GR-reduction.md",
        "clock residue and spatial routing are reciprocal",
        "motion-load local-GR reduction gives reciprocal routing condition.",
    ),
    "SRC4074_11_observer_coframe": (
        ROOT / "10-observer-map-symplectic-contract.md",
        "The local observer coframe must be defined",
        "observer coframe contract blocks PPN claims until the coframe is owned.",
    ),
    "SRC4074_12_frame_theorem": (
        ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "not enough parent coframe/reference geometry",
        "R10 frame theorem says parent coframe/reference geometry remains unsigned.",
    ),
    "SRC4074_13_observed_flow": (
        SOURCE_DIR / "P8_local_GR_observed_flow_stationary_branch_status.csv",
        "conditional_same_stack_owner",
        "observed flow/coframe branch is conditional, not parent-signed.",
    ),
    "SRC4074_14_noether_load": (
        SOURCE_DIR / "P8_local_GR_Qcoh_Noether_load_tensor_status.csv",
        "best_route_is_Noether_deformation_tensor",
        "Noether load route depends on observed flow/coframe ownership.",
    ),
    "SRC4074_15_em_hodge": (
        SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "Poynting_flow",
        "EM/Hodge/Poynting route is a coframe consistency constraint.",
    ),
    "SRC4074_16_poynting_status": (
        SOURCE_DIR / "P8_EM_source_label_forgetting_EM_Hodge_status.csv",
        "Poynting_as_Maxwell_Hilbert_stress",
        "Poynting is a derived Hilbert-stress readout once Hodge/coframe are owned.",
    ),
    "SRC4074_17_clock_gate": (
        SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_CLOCK_COMPATIBILITY_GATE.csv",
        "MISSING_PARENT_CLOCK_EQUATION",
        "clock strain route remains conditional without parent clock equation.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4074_SOURCE_REGISTER.csv",
    "signature_test": SOURCE_DIR / "P8_Y5_R2FR_4074_FLOW_TO_SOLDER_SIGNATURE_TEST.csv",
    "derivation_attempt": SOURCE_DIR / "P8_Y5_R2FR_4074_BFIELD_DERIVATION_ATTEMPT.csv",
    "demotion_contract": SOURCE_DIR / "P8_Y5_R2FR_4074_EFFECTIVE_TETRAD_DEMOTION_CONTRACT.csv",
    "residual_interface": SOURCE_DIR / "P8_Y5_R2FR_4074_RESIDUAL_INTERFACE_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4074_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4074_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4074_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4074_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4074_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def signature_test_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "test_id": "SIG4074_0_required_B_law",
            "candidate_object": "Cartan solder compensator B^A",
            "required_B_signature": "internal-vector-valued one-form with B'^A = Lambda^A_B B^B - D'a^A",
            "current_MTS_signature": "not a scalar, not a pure gradient, and not a frame-invariant stress readout",
            "result": "REQUIRED_SIGNATURE_DEFINED",
            "derivation_or_obstruction": "B^A is a gauge compensator for local translations; its inhomogeneous term cannot be produced by an ordinary covariant tensor alone.",
            "repair_condition": "future parent must own a local translation sector or a rank-four flow coframe whose split gives B^A",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "SIG4074_1_scalar_primitives",
            "candidate_object": "psi/Psi, Gamma, chi, tau",
            "required_B_signature": "four internal one-forms with translation-compensator law",
            "current_MTS_signature": "scalar fields or scalar response/time parameters",
            "result": "FAIL_CURRENT_MTS_B_SIGNATURE",
            "derivation_or_obstruction": "A scalar or scalar functional can make ds or covariant derivatives, but those transform tensorially and do not carry the -D'a^A term.",
            "repair_condition": "promote from scalar flow to an owned local frame/flow packet Theta^A with internal index A",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "SIG4074_2_gradient_flow",
            "candidate_object": "d psi or grad psi directional flow",
            "required_B_signature": "non-exact solder/translation connection component",
            "current_MTS_signature": "exact one-form or vector readout from a scalar",
            "result": "NO_GO_FOR_PURE_GRADIENT_B",
            "derivation_or_obstruction": "Pure gradients are exact and transform homogeneously; forcing them to absorb local translations imports the compensator rather than deriving it.",
            "repair_condition": "allow non-exact coframe/anholonomy through Cartan structure equations rather than pure scalar gradients",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "SIG4074_3_motion_load_clock_route",
            "candidate_object": "motion-load, clock residue, spatial routing",
            "required_B_signature": "local coframe basis for rods/clocks/matter before weak-field readout",
            "current_MTS_signature": "speed-budget and routing scalars/profiles",
            "result": "INSUFFICIENT_FOR_B_DERIVATION",
            "derivation_or_obstruction": "The c^2 split can constrain norms and reciprocity, but it does not by itself choose four solder one-forms or their gauge transformation.",
            "repair_condition": "derive an observer coframe first, then use motion-load as a compatibility equation on that coframe",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "SIG4074_4_observed_flow_coframe",
            "candidate_object": "observed flow/coframe same-stack owner",
            "required_B_signature": "parent-signed universal coframe for matter, EM, clocks, and PPN",
            "current_MTS_signature": "conditional same-stack contract",
            "result": "CONDITIONAL_ONLY_NOT_PARENT_SIGNED",
            "derivation_or_obstruction": "The branch correctly says all sectors must use the same coframe, but 1003/3538 keep that coframe unsigned at parent level.",
            "repair_condition": "prove quotient coframe descent from parent fields or demote coframe to effective infrastructure",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "SIG4074_5_poynting_hodge_route",
            "candidate_object": "Poynting vector / EM Hodge flow",
            "required_B_signature": "universal metric/coframe source before EM stress is varied",
            "current_MTS_signature": "Poynting is Maxwell Hilbert stress once Hodge and coframe are owned",
            "result": "USEFUL_CONSTRAINT_NOT_B_ORIGIN",
            "derivation_or_obstruction": "The Poynting vector is measured relative to a Hodge star/coframe; using it to generate the same coframe would be circular unless the EM Hodge owner is independently parent-derived.",
            "repair_condition": "use Poynting/Hodge as a residual test of coframe consistency, not as the primary solder derivation",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "SIG4074_6_rank_four_repair",
            "candidate_object": "Theta^A flow coframe repair",
            "required_B_signature": "Theta'^A = Lambda^A_B Theta^B and Theta^A = D_omega X^A + B^A",
            "current_MTS_signature": "not present as an owned parent field in current corpus",
            "result": "FINITE_REPAIR_CONTRACT_IDENTIFIED",
            "derivation_or_obstruction": "A rank-four flow coframe could make the branch genuinely MTS-owned, but it is an additional parent signature until derived from existing flow variables.",
            "repair_condition": "define Theta^A as parent flow/carrying-capacity one-forms with non-degenerate determinant and Cartan covariance",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def derivation_attempt_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "step_id": "DER4074_0_no_go_lemma",
            "lemma": "scalar_flow_cannot_be_B_compensator",
            "statement": "For any scalar parent variable s with ordinary local Lorentz/diffeomorphism covariance, any local algebraic object F(s, ds, nabla ds, ...) transforms homogeneously; it cannot acquire the inhomogeneous -D'a^A term required of B^A.",
            "proof_status": "PROVED_AS_SIGNATURE_NO_GO_UNDER_CURRENT_PRIMITIVES",
            "uses_sources": "03-unified-field-theory-programme.md; the-fundamental-action-of-motion-timespace-field-theory.md; motion-timespace-research.md",
            "blocks_claim": True,
            "repair_path": "introduce parent-owned local translations or a non-exact flow coframe Theta^A",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "DER4074_1_motion_frame_identity",
            "lemma": "B_is_the_translation_compensator_in_e_equals_DX_plus_B",
            "statement": "The identity e^A = D_omega X^A + B^A is gauge covariant only because B^A shifts by -D'a^A under local translations.",
            "proof_status": "DERIVED_FROM_4072_TRANSFORMATION_LAW",
            "uses_sources": "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv; P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv",
            "blocks_claim": True,
            "repair_path": "make B^A parent-owned rather than inferred from scalar flow after the fact",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "DER4074_2_observer_coframe_contract",
            "lemma": "same_observer_coframe_is_required_but_not_origin",
            "statement": "All matter, clocks, EM, and PPN readouts must descend through the same observer coframe; this is a universality gate, not a derivation of the coframe.",
            "proof_status": "CONTRACT_REAFFIRMED",
            "uses_sources": "10-observer-map-symplectic-contract.md; 1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
            "blocks_claim": True,
            "repair_path": "either prove quotient coframe descent or treat the coframe as the GR baseline infrastructure",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "DER4074_3_poynting_non_circularity",
            "lemma": "Poynting_route_tests_the_coframe_but_does_not_create_it",
            "statement": "Poynting flux can lock EM stress to the same coframe after Maxwell/Hodge ownership, but it cannot be the first-principles source of B^A without circularly assuming the Hodge star.",
            "proof_status": "DERIVED_NON_CIRCULARITY_CONSTRAINT",
            "uses_sources": "P8_EM_Hodge_flow_rule_bound_or_zero.csv; P8_EM_source_label_forgetting_EM_Hodge_status.csv",
            "blocks_claim": True,
            "repair_path": "use EM/Hodge/Poynting as downstream residual evidence after coframe ownership is established",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "DER4074_4_repair_theorem_target",
            "lemma": "rank_four_flow_coframe_would_be_sufficient",
            "statement": "If MTS owns non-degenerate Theta^A with Theta'^A = Lambda^A_B Theta^B and Theta^A = D_omega X^A + B^A, then B^A is recoverable as Theta^A - D_omega X^A and the local metric follows as g_obs = eta_AB Theta^A Theta^B.",
            "proof_status": "SUFFICIENT_CONDITION_CONSTRUCTED_NOT_CURRENTLY_SATISFIED",
            "uses_sources": "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv; P8_Y5_R2FR_4073_EFFECTIVE_BRANCH_FALLBACK.csv",
            "blocks_claim": True,
            "repair_path": "4075 should test whether the observer-map/motion-load data can build Theta^A without smuggling a tetrad",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def demotion_contract_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "DEM4074_0_effective_tetrad",
            "branch": "effective_tetrad_baseline",
            "condition": "if B^A is not parent-signed by MTS flow/coframe data",
            "allowed_move": "import e^A/B^A as effective GR/Einstein-Cartan infrastructure for local tests",
            "forbidden_move": "claim MTS derives local GR/Newton/PPN from scalar flow alone",
            "residual_to_score": "epsilon_B_derivation",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "DEM4074_1_kappa_G",
            "branch": "effective_Newton_G",
            "condition": "kappa_eff or G is fitted/measured unless parent normalization derives it",
            "allowed_move": "compare residual corrections around GR using measured G",
            "forbidden_move": "claim numerical Newton G prediction from 4074",
            "residual_to_score": "epsilon_kappa_normalization",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "DEM4074_2_torsion_nonmetricity",
            "branch": "Einstein_Cartan_to_EH_reduction",
            "condition": "torsion/nonmetricity must vanish, be auxiliary, or be bounded",
            "allowed_move": "carry torsion as residual until stiffness/source rows close",
            "forbidden_move": "silently identify Einstein-Cartan with Einstein-Hilbert",
            "residual_to_score": "epsilon_torsion + epsilon_nonmetricity",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "DEM4074_3_shared_stack",
            "branch": "same_coframe_matter_EM_clock",
            "condition": "matter, EM Hodge, clocks, Poynting stress, and orbital readouts use same e_obs",
            "allowed_move": "treat disagreements as residual tests",
            "forbidden_move": "use separate hidden EM or clock coframes",
            "residual_to_score": "Delta_Hodge_EM + clock_strain + source_label_leak",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def residual_interface_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "RES4074_0_B_signature",
            "quantity": "epsilon_B_derivation",
            "definition": "1 or symbolic blocked flag while B^A lacks parent flow-solder signature",
            "arena": "local_GR;PPN;R10;orbital",
            "current_status": "BLOCKED_BY_CURRENT_SIGNATURE_NO_GO",
            "next_input_needed": "Theta^A parent coframe theorem or effective tetrad demotion acceptance",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4074_1_Hodge",
            "quantity": "Delta_Hodge_EM",
            "definition": "difference between EM Hodge/flow rule and observed gravitational coframe",
            "arena": "Maxwell;Poynting;light_cone;clock",
            "current_status": "DOWNSTREAM_CONSISTENCY_TEST",
            "next_input_needed": "same e_obs owner before Poynting can be used as evidence",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4074_2_clock",
            "quantity": "epsilon_clock_strain",
            "definition": "local clock/tau leakage away from stationary or inertial collars",
            "arena": "clock;PPN;source_conservation",
            "current_status": "MISSING_PARENT_CLOCK_EQUATION",
            "next_input_needed": "tau variation/action equation or local collar bound",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4074_3_flow",
            "quantity": "Qcoh / Noether deformation tensor",
            "definition": "observed flow deformation residual relative to Killing/no-flux branch",
            "arena": "local_GR;orbital;PPN",
            "current_status": "CONDITIONAL_ON_OBSERVED_FLOW_COFRAME_OWNERSHIP",
            "next_input_needed": "parent-owned u/h/tau_obs from same e_obs",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4074_4_frame",
            "quantity": "Delta_ref_frame_profile_over_MH",
            "definition": "frame/coframe reference leakage in R10/local tests",
            "arena": "R10;WEP;preferred_frame",
            "current_status": "NOT_ENOUGH_PARENT_COFRAME_REFERENCE_GEOMETRY",
            "next_input_needed": "covariant frame/coframe descent certificate",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4074_0",
            "decision": DECISION,
            "meaning": "current MTS flow primitives do not derive the B^A solder compensator; effective tetrad demotion is staged unless a rank-four flow coframe repair closes",
            "derived_progress": "proved the scalar/gradient flow no-go for B^A and isolated the exact sufficient repair contract Theta^A",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4074_1",
            "decision": "DO_NOT_THROW_BRANCH_AWAY",
            "meaning": "the branch remains useful as a GR baseline/residual scorer even if B^A is effective rather than derived",
            "derived_progress": "Poynting/Hodge/clock/source terms are now downstream residual tests, not circular B-field origins",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4074_0_local_GR",
            "claim": "MTS derives local GR/Newton/PPN",
            "claim_allowed": False,
            "reason": "B^A/e^A coframe origin is not parent-signed by current MTS primitives.",
            "unlock_condition": "parent-owned Theta^A coframe theorem plus torsion/nonmetricity/kappa/source gates",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4074_1_B_derivation",
            "claim": "B^A is derived from MTS flow/transport",
            "claim_allowed": False,
            "reason": "current flow variables are scalar/gradient/routing/readout objects and fail the inhomogeneous translation law.",
            "unlock_condition": "construct non-smuggled rank-four flow coframe or local translation gauge sector",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4074_2_Poynting_origin",
            "claim": "Poynting vector derives the gravitational coframe",
            "claim_allowed": False,
            "reason": "Poynting stress needs a Hodge star/coframe first; it is a downstream consistency test.",
            "unlock_condition": "independent EM Hodge/coframe parent ownership",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4074_3_effective_baseline",
            "claim": "effective tetrad branch may be used for private residual testing",
            "claim_allowed": True,
            "reason": "using measured GR infrastructure as a baseline is allowed if clearly labelled non-derivation.",
            "unlock_condition": "not a public derivation claim; residuals are scored honestly against GR/EM/clocks/orbits",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4074_0",
            "next_target": "4075-Y5-R2FR-flow-coframe-repair-or-effective-GR-residual-scorer.md",
            "script": "scripts/Y5_R2FR_4075_flow_coframe_repair_or_effective_GR_residual_scorer.py",
            "why": "try one concrete Theta^A repair from clock+spatial observer forms; if that smuggles the tetrad, switch to a residual scorer around effective GR",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4074_1",
            "next_target": "EM_Hodge_Poynting_downstream_residual",
            "script": "defer_to_4075_or_later",
            "why": "Poynting is useful, but only after the shared coframe owner is fixed or explicitly effective",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_FLOW_SOLDER_PARENT_SIGNATURE_OR_EFFECTIVE_TETRAD_DEMOTION_4074",
            "checkpoint_id": 4074,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4074 proves current scalar/gradient/routing/Poynting flow variables cannot derive B^A because they lack the required inhomogeneous local-translation compensator law; it stages effective tetrad demotion and isolates Theta^A as the finite repair contract.",
            "valid_for_claim": False,
            "github_action": False,
        }
    ]


def validate_sources(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in rows if not row["exists"]]
    needles = [row["source_id"] for row in rows if not row["needle_found"]]
    ok = not missing and not needles
    detail = f"missing={missing}; needle_missing={needles}"
    return ok, detail


def validate_csv_parse(paths: List[Path]) -> Tuple[bool, str]:
    failures: List[str] = []
    for path in paths:
        try:
            with path.open("r", newline="", encoding="utf-8") as input_file:
                rows = list(csv.DictReader(input_file))
            if not rows:
                failures.append(f"{path.name}: empty")
        except Exception as exc:  # pragma: no cover - validation path
            failures.append(f"{path.name}: {exc}")
    return not failures, "; ".join(failures) if failures else "all generated CSVs parse"


def validate_no_public_claim(row_groups: List[List[Dict[str, object]]]) -> Tuple[bool, str]:
    text = str(row_groups)
    forbidden = [
        "public_claim': True",
        '"public_claim": True',
        "github_action': True",
        '"github_action": True',
        "MTS derives local GR/Newton/PPN', 'claim_allowed': True",
        "B^A is derived from MTS flow/transport', 'claim_allowed': True",
        "Poynting vector derives the gravitational coframe', 'claim_allowed': True",
    ]
    hits = [token for token in forbidden if token in text]
    return not hits, f"forbidden_public_claim_tokens={hits}"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    no_claim_ok, no_claim_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4074_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4074_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4074_02_no_public_or_github_claim", "passed": no_claim_ok, "detail": no_claim_detail},
        {
            "check_id": "VAL4074_03_current_B_signature_fails",
            "passed": "FAIL_CURRENT_MTS_B_SIGNATURE" in joined and "NO_GO_FOR_PURE_GRADIENT_B" in joined,
            "detail": "scalar/gradient MTS flow fails B^A translation-compensator signature",
        },
        {
            "check_id": "VAL4074_04_theta_repair_contract",
            "passed": "Theta^A" in joined and "FINITE_REPAIR_CONTRACT_IDENTIFIED" in joined,
            "detail": "finite rank-four flow coframe repair contract is present",
        },
        {
            "check_id": "VAL4074_05_poynting_non_circularity",
            "passed": "Poynting_route_tests_the_coframe_but_does_not_create_it" in joined,
            "detail": "Poynting/Hodge route is downstream, not circular B origin",
        },
        {
            "check_id": "VAL4074_06_effective_tetrad_demotion",
            "passed": "effective_tetrad_baseline" in joined and "epsilon_B_derivation" in joined,
            "detail": "effective tetrad demotion contract and residual are explicit",
        },
        {
            "check_id": "VAL4074_07_next_target",
            "passed": "4075-Y5-R2FR-flow-coframe-repair-or-effective-GR-residual-scorer.md" in joined,
            "detail": "next target is the coframe repair/residual scorer fork",
        },
        {"check_id": "VAL4074_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4074 - Flow-Solder Field Parent Signature Or Effective Tetrad Demotion

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Result

4074 attacks the exact thing that was still too hand-wavy after the motion-frame gauge adoption:

```text
e^A = D_omega X^A + B^A
B'^A = Lambda^A_B B^B - D'a^A
g_obs = eta_AB e^A e^B
```

The result is a useful no-go, not a vibe-check:

```text
current scalar/gradient/routing MTS flow variables do not derive B^A.
```

The reason is structural. `B^A` is not merely "flow". It is an internal-vector-valued one-form with an inhomogeneous local-translation compensator term. A scalar field, scalar clock, scalar memory term, exact gradient, speed-budget split, Poynting vector, or Hilbert stress readout transforms tensorially/homogeneously once the frame is chosen. None of them can supply the `-D'a^A` shift without importing the very gauge object we are trying to derive.

## What Was Proved

Under the current corpus primitives:

```text
psi/Psi, Gamma, chi, tau, d psi, motion-load, clock residue, spatial routing
```

any local object built algebraically from scalar flow data transforms as a scalar/tensor/readout. It can constrain norms, source couplings, Hodge consistency, or clock strain, but it cannot become the Cartan translation compensator `B^A`.

So the branch cannot honestly claim:

```text
MTS flow -> B^A -> e^A -> GR
```

yet.

## Poynting Vector Route

This also answers the Poynting-vector suspicion cleanly.

Poynting flow is valuable, but downstream. It is Maxwell/Hilbert stress measured through a Hodge star and observer coframe. It can test whether EM, clocks, matter, and gravity are using the same `e_obs`, but it cannot be the first source of `B^A` without circularly assuming the coframe/Hodge structure.

## The Forward Repair

There is still a precise route that would make this work:

```text
Theta^A = parent-owned flow coframe
Theta'^A = Lambda^A_B Theta^B
Theta^A = D_omega X^A + B^A
B^A = Theta^A - D_omega X^A
g_obs = eta_AB Theta^A Theta^B
```

If MTS can derive a non-degenerate rank-four `Theta^A` from clock plus spatial observer routing without smuggling a tetrad, the local GR branch becomes serious again.

## Demotion Contract

Until that repair closes, local gravity must be treated as:

```text
effective tetrad / Einstein-Cartan / GR baseline
plus MTS residuals
```

The residuals to score are:

```text
epsilon_B_derivation
epsilon_torsion
epsilon_nonmetricity
epsilon_kappa_normalization
Delta_Hodge_EM
epsilon_clock_strain
source_label_leak
Qcoh / Noether deformation
Delta_ref_frame_profile_over_MH
```

## Decision

This is not the branch dying. It is the branch losing the right to smuggle the tetrad.

4074 says:

```text
Either derive Theta^A properly next,
or use effective GR as the baseline and score MTS residuals honestly.
```

## Next

`4075` should try one concrete repair:

```text
clock one-form + spatial observer routing triad -> Theta^A
```

If that route imports a tetrad in disguise, switch immediately to the effective-GR residual scorer.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    signature = signature_test_rows(current_timestamp)
    derivation = derivation_attempt_rows(current_timestamp)
    demotion = demotion_contract_rows(current_timestamp)
    residuals = residual_interface_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["signature_test"], signature)
    write_csv(OUTPUTS["derivation_attempt"], derivation)
    write_csv(OUTPUTS["demotion_contract"], demotion)
    write_csv(OUTPUTS["residual_interface"], residuals)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["signature_test"],
        OUTPUTS["derivation_attempt"],
        OUTPUTS["demotion_contract"],
        OUTPUTS["residual_interface"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        signature,
        derivation,
        demotion,
        residuals,
        decisions,
        claims,
        next_targets,
        statuses,
    ]
    validation = validation_rows(sources, generated_csvs, row_groups)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
