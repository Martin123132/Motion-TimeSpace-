from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_NOHAIR_ALPHA3_2248"
DOC = ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2248_0_2247_doc",
        "source_key": "2247_handoff",
        "source_path": ROOT / "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md",
        "needles": ["RC2247_2_positive_sourcefree_physical_R", "DEC2247_2_next_target"],
        "role": "selects the R_AB source-free positive no-hair route",
    },
    {
        "source_id": "SRC2248_1_2247_validation",
        "source_key": "2247_validation",
        "source_path": OUT / "P8_Y5_BRR545_2247_VALIDATION.csv",
        "needles": ["VAL2247_OVERALL", "PASS"],
        "role": "confirms 2247 passed before 2248 starts",
    },
    {
        "source_id": "SRC2248_2_2247_candidate",
        "source_key": "2247_candidate_classifier",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_PARENT_R_CANDIDATE_CLASSIFIER.csv",
        "needles": ["RC2247_2_positive_sourcefree_physical_R", "VIABLE_NOHAIR_ROUTE_INPUTS_MISSING"],
        "role": "ranks positive source-free R_AB as viable but unsigned",
    },
    {
        "source_id": "SRC2248_3_2247_template",
        "source_key": "2247_theta_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_PR_TEMPLATE_CONTRACT.csv",
        "needles": ["TPR2247_4_positive_RAB_example", "FAIL_CURRENT_CLAIM_THETAR_PR_NOT_PARENT_OWNED"],
        "role": "gives the candidate positive R_AB action and Theta_R template",
    },
    {
        "source_id": "SRC2248_4_2247_owner_gate",
        "source_key": "2247_owner_gate",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_OWNER_GATE.csv",
        "needles": ["TOG2247_5_verdict", "FAIL_CURRENT_CLAIM_THETAR_PR_OWNER_MISSING"],
        "role": "keeps Theta_R/P_R unowned at claim level",
    },
    {
        "source_id": "SRC2248_5_2247_noflux",
        "source_key": "2247_noflux",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_NOFLUX_THEOREM_ZERO_ROUTE.csv",
        "needles": ["positive source-free operator", "Phi_boundary_local"],
        "role": "stages the no-flux/no-hair theorem route",
    },
    {
        "source_id": "SRC2248_6_2247_prior",
        "source_key": "2247_alpha3_prior",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
        "needles": ["BCP2247_0_K_boundary_alpha3", "BCP2247_1_Phi_boundary_local"],
        "role": "alpha3 boundary coefficient prior scaffold",
    },
    {
        "source_id": "SRC2248_7_2246_alpha3",
        "source_key": "2246_alpha3",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2246_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
        "needles": ["alpha3", "valid_for_claim"],
        "role": "previous alpha3 projection coefficient template",
    },
    {
        "source_id": "SRC2248_8_04_contract",
        "source_key": "04_vacuum_contract",
        "source_path": ROOT / "04-vacuum-reciprocity-action-contract.md",
        "needles": ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "J_R = 0 in local vacuum"],
        "role": "early one-dimensional vacuum reciprocity action contract",
    },
    {
        "source_id": "SRC2248_9_05_attempt",
        "source_key": "05_reciprocity_attempt",
        "source_path": ROOT / "05-reciprocity-theorem-attempt.md",
        "needles": ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB]", "asymptotic-flatness no-hair"],
        "role": "early R_AB no-hair theorem attempt and caveats",
    },
    {
        "source_id": "SRC2248_10_06_neutrality",
        "source_key": "06_source_neutrality",
        "source_path": ROOT / "06-reciprocal-charge-source-neutrality.md",
        "needles": ["J_R = 0 -> W R_AB' = Q_R.", "R_AB is not a scalar hair mode at all."],
        "role": "early source-neutrality route and non-hair alternative",
    },
    {
        "source_id": "SRC2248_11_1800_doc",
        "source_key": "1800_x_nohair",
        "source_path": ROOT / "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md",
        "needles": ["XPA1800_5_verdict", "X_POSITIVE_OPERATOR_NOT_ACTIVATED"],
        "role": "analogous X-sector positive-operator/no-hair gate",
    },
    {
        "source_id": "SRC2248_12_1800_validation",
        "source_key": "1800_validation",
        "source_path": OUT / "P8_Y5_BRR545_1800_VALIDATION.csv",
        "needles": ["VAL1800_OVERALL", "PASS"],
        "role": "confirms old X-sector analogue passed",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2248_SOURCE_REGISTER.csv",
    "conditional_identity": OUT / "P8_Y5_PARENT_QLOC_2248_RAB_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "activation_audit": OUT / "P8_Y5_PARENT_QLOC_2248_RAB_NOHAIR_ACTIVATION_AUDIT.csv",
    "jr_decomposition": OUT / "P8_Y5_PARENT_QLOC_2248_JR_SOURCE_ZERO_DECOMPOSITION.csv",
    "boundary_gate": OUT / "P8_Y5_PARENT_QLOC_2248_BOUNDARY_FLUX_ZERO_GATE.csv",
    "alpha3_prior": OUT / "P8_Y5_PARENT_QLOC_2248_ALPHA3_PRIOR_FIRST_FILL.csv",
    "acceptance_gate": OUT / "P8_Y5_PARENT_QLOC_2248_ACCEPTANCE_GATE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2248_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2248_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2248_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2248_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2248_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_nohair": QUEUE / "JR2248_RAB_NOHAIR_IDENTITY_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2248_ALPHA3_PRIOR_FIRST_FILL_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_nohair_alpha3_prior_nonclaim_2248.csv",
    "beta_docs": BETA_DOCS / "RAB_NOHAIR_ALPHA3_PRIOR_2248_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    check_rows = overall or rows
    return all(row.get(result_key, "").lower() == "pass" for row in check_rows)


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def conditional_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "identity_id": "NH2248_0_candidate_sector",
            "object": "source-free positive R_AB sector",
            "statement": "Take L_R = -1/2 Z_R <nabla R,nabla R> -1/2 M_R^2 <R,R> + <J_R,R> on a gauge-reduced local exterior domain.",
            "proof_step": "This is a candidate specialization of TPR2247_4, not a selected parent action.",
            "premises_needed": "PARENT_SELECTED_L_R;DENSITY_CONVENTION;FIELD_SPACE_METRIC;PROJECTOR;DOMAIN",
            "current_status": "CANDIDATE_ACTION_NOT_PARENT_SELECTED",
            "source_paths": src("2247_theta_template", "2247_owner_gate"),
            "conditional_theorem": False,
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "NH2248_1_field_equation",
            "object": "Euler-Lagrange equation",
            "statement": "E_R=0 gives (-Z_R Box_R + M_R^2) R_AB = J_R_AB, up to projector/mixing/corner terms.",
            "proof_step": "Vary the first-derivative quadratic sector and integrate by parts; all omitted terms must be either included or zero-proved.",
            "premises_needed": "FINITE_DERIVATIVE_ORDER;NO_MIXING_OR_MIXING_ACCOUNTED;PROJECTOR_SELF_ADJOINT",
            "current_status": "FORMAL_STEP_READY_PARENT_TERMS_OPEN",
            "source_paths": src("2247_theta_template", "04_vacuum_contract", "05_reciprocity_attempt"),
            "conditional_theorem": False,
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "NH2248_2_energy_identity",
            "object": "integrated no-hair identity",
            "statement": "int_D (Z_R |nabla R|^2 + M_R^2 |R|^2) dV + Phi_boundary_local = int_D <R,J_R> dV.",
            "proof_step": "Multiply the field equation by R_AB, integrate over D, and move the boundary flux into Phi_boundary_local.",
            "premises_needed": "Z_R_POSITIVE;M_R2_NONNEGATIVE_OR_POSITIVE;SELF_ADJOINT_DOMAIN;BOUNDARY_TERM_DEFINED",
            "current_status": "CONDITIONAL_IDENTITY_DERIVED",
            "source_paths": src("2247_noflux", "05_reciprocity_attempt"),
            "conditional_theorem": True,
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "NH2248_3_zero_theorem",
            "object": "R_AB=0 local exterior theorem",
            "statement": "If Z_R>0, M_R^2>0, J_R=0, Phi_boundary_local=0, zero modes are removed, and the local domain is source-free, then R_AB=0 on D.",
            "proof_step": "The left side is a sum of non-negative terms; with the right side and boundary flux zero, coercivity forces R_AB=0.",
            "premises_needed": "PARENT_SIGNED_ZR;PARENT_SIGNED_MR2;PARENT_SIGNED_JR_ZERO;PARENT_SIGNED_PHI_BOUNDARY_ZERO;ZERO_MODE_RULE;SOURCE_FREE_DOMAIN",
            "current_status": "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED",
            "source_paths": src("2247_noflux", "06_source_neutrality"),
            "conditional_theorem": True,
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "NH2248_4_local_residual_consequence",
            "object": "alpha3/R10/PPN residual switch",
            "statement": "On the proven no-hair branch, Phi_boundary_local=0 and R_AB exchange coefficients vanish; otherwise they become finite residual rows.",
            "proof_step": "R_AB=0 kills the candidate local boundary/exchange amplitudes only after the projection map and boundary coefficient definitions are parent-owned.",
            "premises_needed": "PROJECTION_MAP;K_BOUNDARY_DEFINITION;EDGE_TAIL_POLICY;NO_CANCELLATION_GUARD",
            "current_status": "CONSEQUENCE_READY_BUT_NOT_CLAIMED",
            "source_paths": src("2247_alpha3_prior", "2246_alpha3"),
            "conditional_theorem": True,
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "NH2248_5_verdict",
            "object": "2248 no-hair status",
            "statement": "The exact local no-hair identity is now written, but the activation premises are not parent-signed.",
            "proof_step": "Keep it as a conditional theorem gate; do not promote local GR, alpha3, R10, PPN, WEP, clock, or orbital claims.",
            "premises_needed": "ALL_ACTIVATION_GATES_PASS",
            "current_status": "NOHAIR_IDENTITY_CONDITIONAL_NOT_ACTIVATED",
            "source_paths": src("2247_validation", "1800_x_nohair"),
            "conditional_theorem": True,
            **false_flags(),
        },
    ]


def activation_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RNH2248_0_parent_route",
            "needed_input": "parent-selected positive R_AB route",
            "activation_condition": "RC2247_2 is promoted from viable candidate to lawful parent sector, or absent/constraint route replaces it",
            "current_evidence": "2247 ranks RC2247_2 but refuses parent action selection",
            "current_status": "PARENT_ROUTE_NOT_SELECTED",
            "missing_input": "MISSING_PARENT_ROUTE_SELECTION",
            "source_paths": src("2247_handoff", "2247_candidate_classifier"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RNH2248_1_operator_sign_gap",
            "needed_input": "Z_R>0 and M_R^2>0",
            "activation_condition": "coercive positive operator on the source-free local domain, with zero modes removed or bounded",
            "current_evidence": "TPR2247_4 has symbolic Z_R/M_R^2 only",
            "current_status": "OPERATOR_SIGN_GAP_MISSING",
            "missing_input": "MISSING_ZR;MISSING_MR2;MISSING_HESSIAN_SIGNATURE;MISSING_ZERO_MODE_RULE",
            "source_paths": src("2247_theta_template", "1800_x_nohair"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RNH2248_2_JR_zero",
            "needed_input": "J_R=0 in local exterior",
            "activation_condition": "matter, readout, boundary, history, projector, and counterterm source legs vanish separately or enter a strict absolute envelope",
            "current_evidence": "early reciprocity docs demand J_R=0 but do not parent-sign the full source decomposition",
            "current_status": "SOURCE_ZERO_NOT_PROVED",
            "missing_input": "MISSING_JR_COMPONENT_ZERO_OR_BOUNDS",
            "source_paths": src("04_vacuum_contract", "05_reciprocity_attempt", "06_source_neutrality"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RNH2248_3_boundary_flux_zero",
            "needed_input": "Phi_boundary_local=0",
            "activation_condition": "proper boundary class, zero incoming flux, no source-worldtube edge charge, and no topological/corner hair",
            "current_evidence": "2247 prior names Phi_boundary_local but leaves it nonclaim",
            "current_status": "BOUNDARY_FLUX_ZERO_NOT_PROVED",
            "missing_input": "MISSING_BOUNDARY_CLASS;MISSING_EDGE_CHARGE_RULE;MISSING_CORNER_TOPOLOGY_RULE",
            "source_paths": src("2247_alpha3_prior", "2247_noflux"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RNH2248_4_projection_cleanup",
            "needed_input": "projection from R_AB=0 to local observable silence",
            "activation_condition": "q_loc, alpha3, R10, PPN, clocks, and orbital residual maps either vanish under R_AB=0 or carry explicit finite tails",
            "current_evidence": "2247 keeps boundary/R10 coefficients as templates only",
            "current_status": "OBSERVABLE_PROJECTION_NOT_SIGNED",
            "missing_input": "MISSING_QLOC_PROJECTION;MISSING_K_BOUNDARY_ALPHA3;MISSING_EDGE_TAIL_ENVELOPE",
            "source_paths": src("2247_alpha3_prior", "2246_alpha3"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RNH2248_5_verdict",
            "needed_input": "activated R_AB no-hair theorem",
            "activation_condition": "RNH2248_0 through RNH2248_4 pass together in the same parent branch",
            "current_evidence": "the proof skeleton is valid, but all physical activation clauses remain unsigned",
            "current_status": "RAB_NOHAIR_NOT_ACTIVATED",
            "missing_input": "MISSING_PARENT_ROUTE_OPERATOR_SOURCE_BOUNDARY_PROJECTION_PACK",
            "source_paths": src("2247_handoff", "2247_validation"),
            **false_flags(),
        },
    ]


def jr_decomposition_rows() -> list[dict[str, Any]]:
    components = [
        ("JR2248_0_matter", "J_R_matter", "direct local matter coupling to R_AB", "MISSING_MATTER_DESCENT_OR_ZERO_COUPLING"),
        ("JR2248_1_readout", "J_R_readout", "clock/rod/readout dependence that can source R_AB even in exterior vacuum", "MISSING_READOUT_SOURCE_RULE"),
        ("JR2248_2_boundary", "J_R_boundary", "source-worldtube, edge, and boundary collar source term", "MISSING_BOUNDARY_SOURCE_RULE"),
        ("JR2248_3_history", "J_R_history", "memory/history tail that acts as an effective source", "MISSING_HISTORY_TAIL_ZERO_OR_BOUND"),
        ("JR2248_4_projector", "J_R_projector", "projector/constraint leakage into the R_AB sector", "MISSING_PROJECTOR_COMMUTATOR_ZERO_OR_BOUND"),
        ("JR2248_5_counterterm", "J_R_counterterm", "reference/counterterm dependence that can mimic a source", "MISSING_COUNTERTERM_REFERENCE_RULE"),
    ]
    rows = []
    for component_id, component, meaning, missing in components:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "component_id": component_id,
                "component": component,
                "meaning": meaning,
                "zero_condition": f"{component}=0 parent-signed, or absolute bound supplied with source path",
                "current_status": "NOT_ZERO_PROVED",
                "missing_input": missing,
                "no_cancellation_policy": "each component must vanish or be bounded separately; no hidden cancellation in total J_R",
                "source_paths": src("04_vacuum_contract", "06_source_neutrality"),
                **false_flags(),
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "component_id": "JR2248_6_total_verdict",
            "component": "J_R_total",
            "meaning": "total source term in the R_AB no-hair identity",
            "zero_condition": "all component rows pass, or an absolute component envelope is below the local bound target",
            "current_status": "JR_TOTAL_ZERO_NOT_PROVED",
            "missing_input": "MISSING_ALL_COMPONENT_ZERO_OR_ABSOLUTE_BOUNDS",
            "no_cancellation_policy": "total zero cannot be declared from cancellation between unknown components",
            "source_paths": src("2247_noflux", "1800_x_nohair"),
            **false_flags(),
        }
    )
    return rows


def boundary_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("BFG2248_0_dirichlet", "R_AB|partialD=0", "would force Phi_boundary_local=0 for the candidate quadratic identity", "not parent-signed for source worldtube and asymptotic matching"),
        ("BFG2248_1_neumann", "n_mu nabla^mu R_AB|partialD=0", "would kill the canonical flux term", "not parent-signed for all local arenas"),
        ("BFG2248_2_falloff", "R_AB and flux fall off at infinity", "works only for isolated asymptotically controlled exterior domains", "does not cover finite lab, clock, or near-source boundaries"),
        ("BFG2248_3_compact_collar", "generator and jets vanish on the boundary collar", "inherits the 2245 proper compact representative result", "does not cover physical source-worldtube charges"),
        ("BFG2248_4_topological_corner", "no corner/topological zero mode", "removes residual boundary hair", "corner/reference/cohomology class not audited"),
        ("BFG2248_5_verdict", "Phi_boundary_local=0", "all boundary routes close in the same local domain", "boundary flux zero not parent-proved"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "boundary_route": route,
            "why_it_would_work": works,
            "why_not_closed": why_not,
            "current_status": "BOUNDARY_ZERO_ROUTE_OPEN" if gate_id != "BFG2248_5_verdict" else "PHI_BOUNDARY_ZERO_NOT_PROVED",
            "source_paths": src("2247_alpha3_prior", "2247_noflux", "06_source_neutrality"),
            **false_flags(),
        }
        for gate_id, route, works, why_not in rows
    ]


def alpha3_prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "A3P2248_0_formula",
            "target": "alpha3_MTS_boundary",
            "formula": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local + alpha3_tail_abs",
            "alpha3_bound": "4e-20",
            "needed_inputs": "K_boundary_alpha3;Phi_boundary_local;alpha3_tail_abs;normalization;source paths;uncertainty policy",
            "current_status": "NONCLAIM_PRIOR_FIRST_FILL_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "source_paths": src("2247_alpha3_prior", "2246_alpha3"),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "A3P2248_1_zero_switch",
            "target": "alpha3_MTS=0",
            "formula": "alpha3_MTS=0 only if R_AB no-hair theorem activates and projection tails vanish",
            "alpha3_bound": "automatically below 4e-20 only after theorem activation",
            "needed_inputs": "RNH2248_5 pass;projection tails zero",
            "current_status": "ZERO_SWITCH_REJECTED_CURRENTLY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "source_paths": src("2247_noflux", "2247_alpha3_prior"),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "A3P2248_2_bound_prior",
            "target": "K_boundary_alpha3 prior",
            "formula": "if Phi_boundary_local is finite and nonzero, |K_boundary_alpha3| <= (4e-20-|alpha3_tail_abs|)/|Phi_boundary_local|",
            "alpha3_bound": "4e-20",
            "needed_inputs": "positive Phi_boundary_local norm or theorem-zero; alpha3_tail_abs; units; source path",
            "current_status": "INEQUALITY_READY_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "source_paths": src("2247_alpha3_prior"),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "A3P2248_3_verdict",
            "target": "alpha3 prior claim readiness",
            "formula": "no alpha3/local-GR pass can be claimed from 2248",
            "alpha3_bound": "4e-20 retained as external target only",
            "needed_inputs": "no-hair activation or sourced coefficient rows",
            "current_status": "ALPHA3_PRIOR_NONCLAIM_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "source_paths": src("2247_alpha3_prior", "1800_x_nohair"),
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("AC2248_0_conditional_identity", "conditional no-hair identity is mathematically written", "PASS_CONDITIONAL_ONLY", "NH2248_2/NH2248_3 provide the energy identity and zero theorem under stated premises", False),
        ("AC2248_1_activation", "R_AB no-hair theorem activates physically", "FAIL_PREMISES_UNSIGNED", "parent route, sign/gap, J_R zero, boundary zero and projection cleanup are missing", False),
        ("AC2248_2_alpha3_prior", "alpha3 prior row is claim-ready", "FAIL_NUMERIC_OR_ZERO_INPUTS_MISSING", "K_boundary_alpha3, Phi_boundary_local and tails are not sourced or theorem-zero", False),
        ("AC2248_3_no_cancellation", "no hidden cancellation shortcut", "POLICY_PASS_NO_SCORE", "J_R and boundary tails must vanish or be bounded componentwise", False),
        ("AC2248_4_verdict", "local R_AB branch is derived or bounded", "RAB_NOHAIR_AND_ALPHA3_NOT_CLAIM_READY", "2248 improves the proof contract but does not close the physical branch", False),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "reason": reason,
            "gate_pass": gate_pass,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason, gate_pass in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CL2248_0_RAB_nohair", "R_AB=0 in local exterior", "BLOCKED", "RNH2248_5 verdict is RAB_NOHAIR_NOT_ACTIVATED"),
        ("CL2248_1_alpha3", "alpha3 boundary residual passes", "BLOCKED", "A3P2248_3 keeps the prior nonclaim"),
        ("CL2248_2_R10_PPN_WEP", "R10/PPN/WEP/clock/orbital local residuals pass", "BLOCKED", "projection coefficients and source/test tails are missing"),
        ("CL2248_3_local_GR_Newton", "local GR/Newton reduction is derived", "BLOCKED", "R_AB no-hair theorem is conditional only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2248_0_theorem_status",
            "decision": "CONDITIONAL_RAB_NOHAIR_IDENTITY_RETAINED",
            "reason": "the energy identity is the right derivable route and no longer needs a plateau axiom",
            "next_action": "activate or refute its premises one at a time",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2248_1_no_claim",
            "decision": "DO_NOT_CLAIM_LOCAL_GR_OR_ALPHA3_PASS",
            "reason": "parent route, operator signs, J_R silence, boundary flux and projection tails are not signed",
            "next_action": "keep alpha3 as nonclaim prior scaffold",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2248_2_next",
            "decision": "JR_SOURCE_ZERO_OR_COMPONENT_BOUND_PACK_NEXT",
            "reason": "J_R is the coupling/source leg; closing it activates the no-hair theorem, while failing it gives the empirical residual row",
            "next_action": "2249-Y5-R2FR-RAB-JR-source-zero-or-component-bound-pack.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2248_0_primary",
            "next_target": "2249-Y5-R2FR-RAB-JR-source-zero-or-component-bound-pack.md",
            "script": "scripts/Y5_R2FR_RAB_JR_source_zero_or_component_bound_pack_2249.py",
            "objective": "prove J_R source silence componentwise, or emit matter/readout/boundary/history/projector/counterterm source bounds for the R_AB sector",
            "selection_status": "selected",
            "success_condition": "J_R=0 theorem, or absolute source-component envelope ready for alpha3/R10/PPN scoring",
            "forbidden_shortcuts": "total-source cancellation; naked linear coupling; local-GR claim; GitHub action; formalization-workbench edit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2248_1_parallel_operator",
            "next_target": "2249b-Y5-R2FR-RAB-ZR-MR2-sign-gap-source-row.md",
            "script": "scripts/Y5_R2FR_RAB_ZR_MR2_sign_gap_source_row_2249b.py",
            "objective": "derive or source Z_R, M_R^2, Hessian signature, and zero-mode rule for the candidate R_AB operator",
            "selection_status": "held_parallel",
            "success_condition": "coercive operator certificate or explicit finite-range fallback",
            "forbidden_shortcuts": "invented positive signs; fitted mass gap; deleting zero modes without boundary/domain proof",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2248_2_parallel_boundary",
            "next_target": "2249c-Y5-R2FR-RAB-boundary-flux-zero-or-alpha3-tail-row.md",
            "script": "scripts/Y5_R2FR_RAB_boundary_flux_zero_or_alpha3_tail_row_2249c.py",
            "objective": "prove Phi_boundary_local=0 for the local domain, or emit sourced alpha3 boundary/tail coefficients",
            "selection_status": "held_parallel",
            "success_condition": "boundary zero theorem or sourced alpha3 tail envelope",
            "forbidden_shortcuts": "collar-only proof applied to source worldtubes; unsourced Phi_boundary amplitude",
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    copies: list[dict[str, Any]] = []
    copy_plan = [
        ("queue_nohair", OUTPUTS["conditional_identity"], COPY_TARGETS["queue_nohair"], "conditional no-hair identity nonclaim queue"),
        ("queue_alpha3", OUTPUTS["alpha3_prior"], COPY_TARGETS["queue_alpha3"], "alpha3 prior first-fill nonclaim queue"),
        ("branch_wep", OUTPUTS["alpha3_prior"], COPY_TARGETS["branch_wep"], "WEP branch locked alpha3 nonclaim copy"),
        ("beta_docs", OUTPUTS["alpha3_prior"], COPY_TARGETS["beta_docs"], "beta-source docs alpha3 nonclaim copy"),
    ]
    for copy_id, source_path, target_path, reason in copy_plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        copies.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2248_{copy_id}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return copies


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_rows(paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    identity = read_csv(OUTPUTS["conditional_identity"])
    activation = read_csv(OUTPUTS["activation_audit"])
    jr = read_csv(OUTPUTS["jr_decomposition"])
    boundary = read_csv(OUTPUTS["boundary_gate"])
    alpha3 = read_csv(OUTPUTS["alpha3_prior"])
    acceptance = read_csv(OUTPUTS["acceptance_gate"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next_target"])
    branch_copies = read_csv(OUTPUTS["branch_copies"])

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}

    csv_parse_ok = True
    for path in paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    formalization_2248 = []
    if FORMALIZATION.exists():
        formalization_2248 = list(FORMALIZATION.rglob("*2248*"))

    rows = [
        check("VAL2248_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2248_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2248_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2247 and 1800 validation sources pass"),
        check("VAL2248_3_conditional_identity_written", any(row["identity_id"] == "NH2248_3_zero_theorem" and row["conditional_theorem"] == "True" for row in identity), "conditional R_AB zero theorem row is present"),
        check("VAL2248_4_nohair_not_activated", any(row["audit_id"] == "RNH2248_5_verdict" and row["current_status"] == "RAB_NOHAIR_NOT_ACTIVATED" for row in activation), "activation audit refuses current no-hair claim"),
        check("VAL2248_5_JR_decomposition_blocks", any(row["component_id"] == "JR2248_6_total_verdict" and row["current_status"] == "JR_TOTAL_ZERO_NOT_PROVED" for row in jr), "J_R total zero is not assumed"),
        check("VAL2248_6_boundary_flux_blocks", any(row["gate_id"] == "BFG2248_5_verdict" and row["current_status"] == "PHI_BOUNDARY_ZERO_NOT_PROVED" for row in boundary), "boundary flux zero remains blocked"),
        check("VAL2248_7_alpha3_nonclaim", all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in alpha3), "alpha3 prior rows remain nonclaim"),
        check("VAL2248_8_acceptance_blocks", any(row["gate_id"] == "AC2248_4_verdict" and row["current_status"] == "RAB_NOHAIR_AND_ALPHA3_NOT_CLAIM_READY" for row in acceptance), "acceptance gate blocks claim readiness"),
        check("VAL2248_9_claim_gates_blocked", all(row["status"] == "BLOCKED" for row in claims), "all claim gates are blocked"),
        check("VAL2248_10_next_target_written", any(row["route_id"] == "NEXT2248_0_primary" and row["selection_status"] == "selected" for row in next_targets), "J_R source-zero target selected"),
        check("VAL2248_11_decision_selects_JR", any(row["decision_id"] == "DEC2248_2_next" and "JR_SOURCE_ZERO" in row["decision"] for row in decisions), "decision ledger selects J_R coupling/source leg"),
        check("VAL2248_12_csv_parse", csv_parse_ok, "all generated 2248 CSVs parse"),
        check("VAL2248_13_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" for path in paths for row in read_csv(path)), "no generated 2248 row is claim-enabled"),
        check("VAL2248_14_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in branch_copies), "branch/queue nonclaim copies exist and parse"),
        check("VAL2248_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2248_16_formalization_no_2248", not formalization_2248, "formalization-workbench has no 2248 outputs"),
    ]
    rows.append(
        check(
            "VAL2248_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2248 proves the conditional R_AB no-hair identity, refuses activation, stages alpha3 prior first-fill, and selects J_R source-zero next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    identity: list[dict[str, Any]],
    activation: list[dict[str, Any]],
    jr: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    alpha3: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2248 - Y5/R2FR R_AB Source-Free Positive No-Hair Identity or Alpha3 Prior First Fill",
            "## Verdict\n\n2248 gets a real mathematical foothold: the local `R_AB` branch now has an exact conditional no-hair identity. If the parent theory supplies a positive/coercive `R_AB` operator, `J_R=0`, `Phi_boundary_local=0`, zero-mode removal, and a clean projection map, then `R_AB=0` follows in the local exterior. That would be the route toward local GR rather than a fitted plateau.\n\nBut the activation clauses are not parent-signed, so this is not a claim. The first alpha3 prior row is staged as nonclaim only, and the next target is the coupling/source leg `J_R`.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Conditional No-Hair Identity\n" + markdown_table(identity, ["identity_id", "object", "statement", "current_status", "conditional_theorem", "valid_for_claim"]),
            "## Activation Audit\n" + markdown_table(activation, ["audit_id", "needed_input", "activation_condition", "current_status", "missing_input", "valid_for_claim"]),
            "## J_R Source-Zero Decomposition\n" + markdown_table(jr, ["component_id", "component", "meaning", "current_status", "missing_input", "valid_for_claim"]),
            "## Boundary Flux Zero Gate\n" + markdown_table(boundary, ["gate_id", "boundary_route", "why_it_would_work", "current_status", "why_not_closed", "valid_for_claim"]),
            "## Alpha3 Prior First Fill\n" + markdown_table(alpha3, ["row_id", "target", "formula", "alpha3_bound", "current_status", "valid_for_claim"]),
            "## Acceptance Gate\n" + markdown_table(acceptance, ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(branch_copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is progress, not a win lap. We now have the cleanest local-GR route in miniature: prove the source leg dies, prove the boundary flux dies, prove the operator is positive, and the extra local `R_AB` channel collapses without fitting. The coupling/source term is the next pressure point because it decides both futures: theorem-zero if it vanishes, empirical residual if it does not.",
        ]
    ) + "\n"


def main() -> None:
    source_rows = source_register_rows()
    identity = conditional_identity_rows()
    activation = activation_audit_rows()
    jr = jr_decomposition_rows()
    boundary = boundary_gate_rows()
    alpha3 = alpha3_prior_rows()
    acceptance = acceptance_gate_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["conditional_identity"], identity)
    write_csv(OUTPUTS["activation_audit"], activation)
    write_csv(OUTPUTS["jr_decomposition"], jr)
    write_csv(OUTPUTS["boundary_gate"], boundary)
    write_csv(OUTPUTS["alpha3_prior"], alpha3)
    write_csv(OUTPUTS["acceptance_gate"], acceptance)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    branch_copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    remove_pycache()
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()

    DOC.write_text(
        build_doc(source_rows, identity, activation, jr, boundary, alpha3, acceptance, claims, decisions, next_targets, branch_copies, validation),
        encoding="utf-8",
    )

    if not validation_pass(OUTPUTS["validation"]):
        raise SystemExit(f"2248 validation failed: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
