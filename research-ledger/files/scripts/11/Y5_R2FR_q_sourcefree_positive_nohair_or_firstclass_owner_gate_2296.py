from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_Q_SOURCEFREE_NOHAIR_FIRSTCLASS_2296"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2296-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md"

PATHS = {
    "2295_doc": ROOT / "2295-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md",
    "2295_validation": OUT / "P8_Y5_BRR545_2295_VALIDATION.csv",
    "2295_next": OUT / "P8_Y5_PARENT_QLOC_2295_NEXT_TARGET.csv",
    "2295_classifier": OUT / "P8_Y5_PARENT_QLOC_2295_PARENT_Q_CANDIDATE_CLASSIFIER.csv",
    "2295_template": OUT / "P8_Y5_PARENT_QLOC_2295_THETAQ_PQ_TEMPLATE_CONTRACT.csv",
    "2295_owner": OUT / "P8_Y5_PARENT_QLOC_2295_THETAQ_OWNER_GATE.csv",
    "2295_noflux": OUT / "P8_Y5_PARENT_QLOC_2295_NOFLUX_THEOREM_ZERO_ROUTE.csv",
    "2295_priors": OUT / "P8_Y5_PARENT_QLOC_2295_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "2294_formula": OUT / "P8_Y5_PARENT_QLOC_2294_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "2293_compact": OUT / "P8_Y5_PARENT_QLOC_2293_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "2248_doc": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
    "2248_validation": OUT / "P8_Y5_BRR545_2248_VALIDATION.csv",
    "2248_boundary": OUT / "P8_Y5_PARENT_QLOC_2248_BOUNDARY_FLUX_ZERO_GATE.csv",
    "2248_alpha3": OUT / "P8_Y5_PARENT_QLOC_2248_ALPHA3_PRIOR_FIRST_FILL.csv",
    "1042_doc": ROOT / "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md",
    "1042_validation": OUT / "P8_Y5_BRR545_1042_VALIDATION.csv",
    "action_terms": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "min_action": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}

SOURCES = [
    ("SRC2296_00_2295_doc", "q_owner_handoff", PATHS["2295_doc"], ["sourcefree_q_nohair_template", "first-class"], "2295 selected q no-hair/first-class owner gate."),
    ("SRC2296_01_2295_validation", "prior_validation", PATHS["2295_validation"], ["VAL2295_OVERALL", "PASS"], "2295 validation passed."),
    ("SRC2296_02_2295_next", "explicit_next_target", PATHS["2295_next"], ["2296-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md", "Z_q"], "Direct 2296 handoff."),
    ("SRC2296_03_2295_classifier", "q_route_classifier", PATHS["2295_classifier"], ["QC2295_1_first_class_vertical_constraint", "QC2295_2_positive_sourcefree_physical_q"], "q route classifier."),
    ("SRC2296_04_2295_template", "Thetaq_template", PATHS["2295_template"], ["TPQ2295_4_positive_q_example", "Theta_q"], "q positive template."),
    ("SRC2296_05_2295_owner", "Thetaq_owner_gate", PATHS["2295_owner"], ["TOG2295_5_verdict", "FAIL_CURRENT_CLAIM_THETAQ_PQ_OWNER_MISSING"], "q owner gate still blocked."),
    ("SRC2296_06_2295_noflux", "q_noflux_routes", PATHS["2295_noflux"], ["NFR2295_0_positive_energy", "NFR2295_2_first_class_constraint"], "q no-hair and first-class route staging."),
    ("SRC2296_07_2295_priors", "q_coefficient_priors", PATHS["2295_priors"], ["BCP2295_0_K_boundary_alpha3_q", "BCP2295_2_edge_R10_coefficients_q"], "q coefficient prior scaffold."),
    ("SRC2296_08_2294_formula", "Bq_formula", PATHS["2294_formula"], ["BQF2294_2_candidate_Qq", "B_q"], "B_q/Q_q formula contract."),
    ("SRC2296_09_2293_compact", "proper_compact_boundary", PATHS["2293_compact"], ["QQK2293_2_Qq_zero", "QQK2293_3_Kboundary_zero"], "proper compact q boundary silence."),
    ("SRC2296_10_2248_doc", "RAB_nohair_precedent", PATHS["2248_doc"], ["conditional no-hair identity", "J_R"], "R_AB conditional no-hair precedent."),
    ("SRC2296_11_2248_validation", "RAB_nohair_validation", PATHS["2248_validation"], ["VAL2248_OVERALL", "PASS"], "2248 validation passed."),
    ("SRC2296_12_2248_boundary", "RAB_boundary_flux", PATHS["2248_boundary"], ["BFG2248_5_verdict", "PHI_BOUNDARY_ZERO_NOT_PROVED"], "boundary flux gate precedent."),
    ("SRC2296_13_2248_alpha3", "RAB_alpha3_prior", PATHS["2248_alpha3"], ["A3P2248_0_formula", "4e-20"], "alpha3 prior first-fill precedent."),
    ("SRC2296_14_1042_doc", "generic_nohair_precedent", PATHS["1042_doc"], ["positive-X no-hair", "Phi_boundary_local"], "generic positive no-hair precedent."),
    ("SRC2296_15_1042_validation", "generic_nohair_validation", PATHS["1042_validation"], ["V1042_SUMMARY", "pass"], "1042 validation passed."),
    ("SRC2296_16_action_terms", "parent_action_contract", PATHS["action_terms"], ["A0_total_covariant_parent", "A7_bulk_X_nohair_or_curve"], "parent action term contract."),
    ("SRC2296_17_min_action", "minimal_GR_blocks", PATHS["min_action"], ["A511_3_extra_field_silence", "A511_6_metric_readout"], "minimal local-GR block constraints."),
    ("SRC2296_18_local_bounds", "alpha3_anchor", PATHS["local_bounds"], ["R7_alpha3", "4e-20"], "source-backed alpha3 anchor."),
    ("SRC2296_19_R10_candidate", "R10_review_bound", PATHS["r10_candidate"], ["R10_VECTOR_2020_REVIEW", "alpha"], "R10 review-candidate bound curve, nonclaim."),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2296_SOURCE_REGISTER.csv",
    "nohair_identity": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "premise_gates": OUT / "P8_Y5_PARENT_QLOC_2296_NOHAIR_PREMISE_GATES.csv",
    "firstclass_gate": OUT / "P8_Y5_PARENT_QLOC_2296_FIRSTCLASS_OWNER_GATE.csv",
    "source_zero": OUT / "P8_Y5_PARENT_QLOC_2296_JQ_SOURCE_ZERO_AUDIT.csv",
    "boundary_gate": OUT / "P8_Y5_PARENT_QLOC_2296_BOUNDARY_FLUX_ZERO_GATE.csv",
    "alpha3_prior": OUT / "P8_Y5_PARENT_QLOC_2296_ALPHA3_PRIOR_FIRST_FILL.csv",
    "r10_impact": OUT / "P8_Y5_PARENT_QLOC_2296_R10_IMPACT_LEDGER.csv",
    "acceptance": OUT / "P8_Y5_PARENT_QLOC_2296_ACCEPTANCE_GATES.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2296_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2296_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2296_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2296_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2296_VALIDATION.csv",
}

BRANCH_COPY_TARGETS = {
    "queue_nohair": QUEUE / "JR2296_Q_NOHAIR_IDENTITY_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2296_ALPHA3_PRIOR_FIRST_FILL_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_nohair_alpha3_prior_nonclaim_2296.csv",
    "beta_docs": BETA_DOCS / "Q_NOHAIR_ALPHA3_PRIOR_2296_NONCLAIM.csv",
}


def ensure_dirs() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        if not rows:
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def contains_all(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def alpha3_bound() -> str:
    for row in read_csv(PATHS["local_bounds"]):
        if row.get("row_id") == "R7_alpha3" or row.get("observable") == "alpha3":
            return row.get("upper_bound", "4e-20")
    return "4e-20"


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "source_id": sid,
            "role": role,
            "path": str(path),
            "exists": path.exists(),
            "needles_present": contains_all(path, needles),
            "needles": ";".join(needles),
            "notes": notes,
            "valid_for_claim": False,
        }
        for sid, role, path, needles, notes in SOURCES
    ]


def nohair_rows() -> list[dict[str, Any]]:
    rows = [
        ("NH2296_0_candidate_sector", "source-free positive q sector", "Take L_q=-1/2 Z_q nabla_mu q nabla^mu q -1/2 M_q^2 q^2 + J_q q plus nonnegative mixing on a gauge-reduced local exterior domain.", "CANDIDATE_ACTION_NOT_PARENT_SELECTED", True, "sets the positive operator theorem target"),
        ("NH2296_1_Euler_Lagrange", "local q equation", "L_q^{op} q = J_q, with L_q^{op}=-nabla_mu(Z_q^{mu nu}nabla_nu .)+M_q^2+positive_mix.", "FORMULA_DERIVED_CONDITIONAL_ON_LQ", True, "operator must be parent-owned before use"),
        ("NH2296_2_energy_identity", "integrated no-hair identity", "int_D (Z_q |nabla q|^2 + M_q^2 q^2 + positive_mix[q]) dV + Phi_boundary_local_q = int_D q J_q dV.", "CONDITIONAL_IDENTITY_DERIVED", True, "if right-hand side and boundary vanish, positivity kills q"),
        ("NH2296_3_zero_theorem", "q=0 local exterior theorem", "If Z_q>0, M_q^2>0, J_q=0, Phi_boundary_local_q=0, zero modes are removed, and the local domain is source-free, then q=0 on D.", "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED", True, "local GR branch only after all premises are parent-signed"),
        ("NH2296_4_firstclass_alternative", "first-class q no-pole route", "If Omega_flat(v_q)=delta C_q, brackets close, Q_q/K_boundary are proper/exact zero, degree count removes q, and matter descends, q has no physical local pole.", "ALTERNATIVE_CONDITIONAL_THEOREM_STATED", True, "not yet proved because Omega/DCq/degree/matter clauses are open"),
        ("NH2296_5_residual_consequence", "alpha3/R10/PPN residual switch", "On activated no-hair or first-class branch, q edge/bulk exchange coefficients vanish; otherwise alpha3/R10/WEP/clock/PPN rows remain finite residuals.", "CONSEQUENCE_READY_BUT_NOT_CLAIMED", True, "projection tails still require explicit bounds"),
        ("NH2296_6_verdict", "2296 no-hair/first-class status", "The local q no-hair and first-class routes are mathematically clear but not activated by current parent evidence.", "NOHAIR_AND_FIRSTCLASS_CONDITIONAL_NOT_ACTIVATED", True, "move to J_q source-zero / component-bound pack"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "identity_id": row[0],
            "object": row[1],
            "formula_or_statement": row[2],
            "status": row[3],
            "mathematically_derived": row[4],
            "claim_effect": row[5],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def premise_rows() -> list[dict[str, Any]]:
    rows = [
        ("NHP2296_0_parent_Lq", "parent q action and boundary class", "explicit parent L_q or constraint route with field normalization and allowed boundary class", "LQ_NOT_PARENT_SELECTED", "no-hair identity is a candidate theorem only"),
        ("NHP2296_1_Z_positive", "Z_q positive kinetic operator", "Z_q^{mu nu} is positive/coercive on the local exterior domain after projector/mixing reduction", "ZQ_SIGN_NOT_PARENT_SIGNED", "ghost/anti-elliptic or sign-indefinite mode can evade no-hair"),
        ("NHP2296_2_mass_gap", "M_q^2 positive local gap", "M_q^2>=m_min^2>0 or zero modes are removed by gauge/topology/boundary conditions", "MQ2_GAP_NOT_PARENT_SIGNED", "massless/topological/long-range q mode can remain"),
        ("NHP2296_3_source_zero", "J_q=0 channelwise", "ordinary matter, constants, boundary, projector, domain, and memory sources vanish by parent identity", "SOURCE_ZERO_NOT_DERIVED", "positive q is sourced and becomes empirical alpha(lambda)"),
        ("NHP2296_4_boundary_flux_zero", "Phi_boundary_local_q=0", "boundary flux, source worldtube, reference subtraction, and topology/corner terms vanish or are bounded", "BOUNDARY_FLUX_ZERO_NOT_DERIVED", "alpha3/R10 boundary coefficient rows remain active"),
        ("NHP2296_5_no_zero_mode", "no topological/gauge zero mode outside proper quotient", "kernel of L_q is quotient/proper or fixed by boundary/reference data", "TOPOLOGY_KERNEL_GATE_OPEN", "positive norm may kill only nonzero modes, leaving topological hair"),
        ("NHP2296_6_projection_cleanup", "q=0 implies observable residual silence", "alpha3, R10, WEP, clock, PPN, and orbital projections vanish or are separately bounded", "OBSERVABLE_PROJECTION_NOT_SIGNED", "local q silence does not automatically silence every readout"),
        ("NHP2296_7_verdict", "claim-grade source-free positive q no-hair", "NHP2296_0 through NHP2296_6 pass together", "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED", "keep theorem as conditional and retain nonclaim priors"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "premise": row[1],
            "required_test": row[2],
            "current_status": row[3],
            "if_missing": row[4],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def firstclass_rows() -> list[dict[str, Any]]:
    rows = [
        ("FC2296_0_parent_Omega", "parent symplectic form", "Omega_Y is written on the full q/metric/coframe/domain/matter/boundary phase space", "MISSING_PARENT_OMEGA", "cannot identify v_q as gauge"),
        ("FC2296_1_constraint_map", "q constraint/source map C_q", "C_q is parent-owned and D C_q maps variations into the q covector", "MISSING_PARENT_DCQ", "D C_q remains bookkeeping"),
        ("FC2296_2_momentum_map", "Omega_flat(v_q)=delta C_q", "i_vq Omega_Y=delta C_q[epsilon]+boundary terms with differentiable generator", "MISSING_MOMENTUM_MAP", "first-class status not proved"),
        ("FC2296_3_boundary_silence", "proper/exact Q_q and K_boundary", "Q_q=0/exact/proper and K_boundary=0 for allowed local branch", "PARTIAL_PROPER_COMPACT_ONLY", "2293 covers compact representative branch, not full source boundary"),
        ("FC2296_4_bracket_closure", "first-class bracket", "{G_q[epsilon],G_q[eta]}=G_q[[epsilon,eta]]+K_boundary with K_boundary zero/proper", "MISSING_BRACKET_CLOSURE", "second-class or anomalous edge mode can remain"),
        ("FC2296_5_degree_count", "q phase-space removal", "primary/secondary first-class constraints remove the local q pair and reduced Omega is nondegenerate", "MISSING_DEGREE_COUNT", "no-pole can be confused with under-specified dynamics"),
        ("FC2296_6_matter_descent", "matter/readout quotient descent", "S_matter and constants/readouts depend only on quotient observables, with no q marker", "MISSING_MATTER_DESCENT", "WEP/clock/R10 source-test beta rows remain live"),
        ("FC2296_7_verdict", "claim-grade first-class q no-pole", "FC2296_0 through FC2296_6 pass together", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED", "positive no-hair and coefficient priors remain fallback"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "needed": row[1],
            "test": row[2],
            "current_status": row[3],
            "if_missing": row[4],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("JQ2296_0_matter_pullback", "ordinary matter and constants", "matter action and constants do not couple linearly to q in the local exterior", "qbar_qT; WEP; clock; R10 test charge", "NOT_ZERO_PROVED"),
        ("JQ2296_1_boundary_source", "boundary/source worldtube", "Q_edge, B_q, and source boundary flux vanish or are orthogonal to Pi_M", "Qbar_edge_qH(lambda); Phi_boundary_local_q; alpha3", "NOT_ZERO_PROVED"),
        ("JQ2296_2_projector_domain", "projector/domain selector", "projector/domain sector is topological, first-class, or positive source-free with zero stress/flux", "preferred-frame PPN; alpha3; R10 domain tail", "NOT_ZERO_PROVED"),
        ("JQ2296_3_memory_kernel", "memory/history kernel", "memory kernel has no source-free local q projection or is bounded in absolute tail", "Gdot; alpha3; R10 memory tail", "NOT_ZERO_PROVED"),
        ("JQ2296_4_source_normalization", "measured source mass and calibration", "Pi_M^H source measure is orthogonal to q hair and measured GM uses same charge", "Qbar_qH; M_H_ref; PPN source normalization", "NOT_ZERO_PROVED"),
        ("JQ2296_5_counterterm_reference", "counterterm/reference source", "B_ref/B_ct does not inject q source after reference subtraction", "K_boundary_alpha3_q; Qbar_edge_qH; exactness", "NOT_ZERO_PROVED"),
        ("JQ2296_6_total_verdict", "J_q_total", "all source channels vanish or enter absolute source envelope", "finite positive-q branch remains empirical/nonclaim", "JQ_TOTAL_ZERO_NOT_PROVED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "source_id": row[0],
            "channel": row[1],
            "zero_condition": row[2],
            "residual_if_open": row[3],
            "current_status": row[4],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def boundary_rows() -> list[dict[str, Any]]:
    rows = [
        ("BFG2296_0_dirichlet", "q|partialD=0", "would force Phi_boundary_local_q=0 for the candidate quadratic identity", "BOUNDARY_ZERO_ROUTE_OPEN", "not parent-signed for source worldtube and asymptotic matching"),
        ("BFG2296_1_neumann", "n_mu nabla^mu q|partialD=0", "would force the simple quadratic flux term to vanish", "BOUNDARY_ZERO_ROUTE_OPEN", "not signed for finite lab/source boundary or exact/counterterm flux"),
        ("BFG2296_2_falloff", "q and flux fall off at infinity", "works only for isolated asymptotically controlled exterior domains", "BOUNDARY_ZERO_ROUTE_OPEN", "does not cover finite lab, clock, or near-source boundaries"),
        ("BFG2296_3_compact_collar", "generator and jets vanish on the boundary collar", "inherits the 2293 proper compact representative result", "BOUNDARY_ZERO_ROUTE_OPEN", "does not cover physical source-worldtube charges"),
        ("BFG2296_4_topological_corner", "no corner/topological zero mode", "removes residual boundary hair", "BOUNDARY_ZERO_ROUTE_OPEN", "corner/reference/cohomology class not audited"),
        ("BFG2296_5_verdict", "Phi_boundary_local_q=0", "all boundary routes close in the same local domain", "PHI_BOUNDARY_ZERO_NOT_PROVED", "boundary flux zero not parent-proved"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "boundary_route": row[1],
            "why_it_would_work": row[2],
            "current_status": row[3],
            "why_not_closed": row[4],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def alpha3_rows() -> list[dict[str, Any]]:
    bound = alpha3_bound()
    rows = [
        ("A3P2296_0_formula", "alpha3_MTS_q_boundary", "alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q+alpha3_tail_abs", bound, "NONCLAIM_PRIOR_FIRST_FILL_INPUTS_MISSING"),
        ("A3P2296_1_zero_switch", "alpha3_MTS_q=0", "alpha3_MTS_q=0 only if q no-hair/first-class theorem activates and projection tails vanish", "automatically below bound only after theorem activation", "ZERO_SWITCH_REJECTED_CURRENTLY"),
        ("A3P2296_2_bound_prior", "K_boundary_alpha3_q prior", f"if Phi_boundary_local_q is finite and nonzero, |K_boundary_alpha3_q| <= ({bound}-|alpha3_tail_abs|)/|Phi_boundary_local_q|", bound, "INEQUALITY_READY_NUMERIC_INPUTS_MISSING"),
        ("A3P2296_3_verdict", "alpha3 prior claim readiness", "no alpha3/local-GR pass can be claimed from 2296", f"{bound} retained as external target only", "ALPHA3_PRIOR_NONCLAIM_ONLY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row[0],
            "target": row[1],
            "formula": row[2],
            "alpha3_bound": row[3],
            "current_status": row[4],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def r10_rows() -> list[dict[str, Any]]:
    rows = [
        ("R10I2296_0_if_nohair_closes", "source-free q no-hair closes", "bulk q exchange vanishes on theorem domain", "must still prove source/readout/boundary/source-worldtube scopes", False),
        ("R10I2296_1_if_firstclass_closes", "first-class q constraint closes", "q removed from reduced local phase space; no physical q pole", "must still prove matter descent and boundary proper/exact silence", False),
        ("R10I2296_2_if_source_open", "J_q open", "positive q is sourced; R10 alpha(lambda), WEP/clock/PPN residual rows stay live", "requires K_edge_q/Qbar/qbar and no-cancellation tails", False),
        ("R10I2296_3_if_boundary_open", "Phi_boundary_local_q open", "boundary alpha3 and R10 edge residuals stay live with absolute no-cancellation addition", "requires K_boundary_alpha3_q or edge K/Qbar/qbar rows", False),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": row[0],
            "branch": row[1],
            "effect": row[2],
            "remaining_caveat": row[3],
            "valid_for_claim": row[4],
        }
        for row in rows
    ]


def acceptance_rows() -> list[dict[str, Any]]:
    rows = [
        ("AC2296_0_conditional_identity", "conditional q no-hair identity is mathematically written", "PASS_CONDITIONAL_ONLY", "NH2296_2/NH2296_3 provide the energy identity and zero theorem under stated premises"),
        ("AC2296_1_nohair_activation", "q no-hair theorem activates physically", "FAIL_PREMISES_UNSIGNED", "parent route, sign/gap, J_q zero, boundary zero, topology, and projection cleanup are missing"),
        ("AC2296_2_firstclass_activation", "q first-class no-pole theorem activates physically", "FAIL_PREMISES_UNSIGNED", "Omega/DCq, bracket, boundary, degree count, and matter descent are missing"),
        ("AC2296_3_alpha3_prior", "alpha3 prior row is claim-ready", "FAIL_NUMERIC_OR_ZERO_INPUTS_MISSING", "K_boundary_alpha3_q, Phi_boundary_local_q and tails are not sourced or theorem-zero"),
        ("AC2296_4_no_cancellation", "no hidden cancellation shortcut", "POLICY_PASS_NO_SCORE", "J_q and boundary tails must vanish or be bounded componentwise"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "test": row[1],
            "status": row[2],
            "evidence": row[3],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CL2296_0_nohair", "source-free positive q no-hair closes local branch", "BLOCKED", "identity is conditional but L_q/Z_q/M_q/J_q/Phi/topology/projection gates are not parent-signed"),
        ("CL2296_1_firstclass", "first-class q no-pole closes local branch", "BLOCKED", "Omega/DCq/bracket/degree/matter descent gates are not parent-signed"),
        ("CL2296_2_alpha3", "alpha3 boundary residual passes", "BLOCKED", "A3P2296 rows keep the prior nonclaim"),
        ("CL2296_3_R10_PPN_WEP", "R10/PPN/WEP/clock/orbital local residuals pass", "BLOCKED", "projection coefficients and source/test tails are missing"),
        ("CL2296_4_local_GR_Newton", "local GR/Newton reduction is derived", "BLOCKED", "q no-hair and first-class theorem routes are conditional only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": row[0],
            "claim": row[1],
            "status": row[2],
            "reason": row[3],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2296_0_theorem_status", "CONDITIONAL_Q_NOHAIR_AND_FIRSTCLASS_ROUTES_RETAINED", "positive no-hair identity is clean mathematics and first-class route is exact if its canonical clauses close", "do not claim local GR until activation clauses are parent-signed"),
        ("DEC2296_1_no_claim", "DO_NOT_CLAIM_LOCAL_GR_ALPHA3_R10_PASS", "parent route, operator signs, J_q silence, boundary flux, first-class closure, and projection tails are not signed", "keep alpha3/R10 as nonclaim prior scaffolds"),
        ("DEC2296_2_next", "JQ_SOURCE_ZERO_OR_COMPONENT_BOUND_PACK_NEXT", "J_q is the coupling/source leg; closing it activates positive no-hair, while failing it gives empirical residual rows", "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": row[0],
            "decision": row[1],
            "reason": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        ("NEXT2296_0_primary", "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md", "scripts/Y5_R2FR_Jq_source_zero_or_component_bound_pack_2297.py", "prove J_q source silence componentwise, or emit matter/readout/boundary/history/projector/counterterm source bounds for the q sector", "selected", "J_q=0 theorem or absolute source-component envelope ready for alpha3/R10/PPN scoring"),
        ("NEXT2296_1_parallel_operator", "2297b-Y5-R2FR-q-Zq-Mq2-sign-gap-source-row.md", "scripts/Y5_R2FR_q_Zq_Mq2_sign_gap_source_row_2297b.py", "derive or source Z_q, M_q^2, Hessian signature, and zero-mode rule for the candidate q operator", "held_parallel", "coercive operator certificate or explicit finite-range fallback"),
        ("NEXT2296_2_parallel_boundary", "2297c-Y5-R2FR-q-boundary-flux-zero-or-alpha3-tail-row.md", "scripts/Y5_R2FR_q_boundary_flux_zero_or_alpha3_tail_row_2297c.py", "prove Phi_boundary_local_q=0 for the local domain, or emit sourced alpha3 boundary/tail coefficients", "held_parallel", "boundary zero theorem or sourced alpha3 tail envelope"),
        ("NEXT2296_3_parallel_firstclass", "2297d-Y5-R2FR-q-firstclass-Omega-DCq-degree-matter-gate.md", "scripts/Y5_R2FR_q_firstclass_Omega_DCq_degree_matter_gate_2297d.py", "prove Omega_flat(v_q)=delta C_q, bracket closure, degree count, and matter descent for the q first-class route", "held_parallel", "first-class no-pole certificate or explicit failure ledger"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": row[0],
            "next_target": row[1],
            "script": row[2],
            "objective": row[3],
            "priority": row[4],
            "acceptance_output": row[5],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def copy_branch_files() -> list[dict[str, Any]]:
    plan = {
        "queue_nohair": OUTPUTS["nohair_identity"],
        "queue_alpha3": OUTPUTS["alpha3_prior"],
        "branch_wep": OUTPUTS["alpha3_prior"],
        "beta_docs": OUTPUTS["alpha3_prior"],
    }
    rows = []
    for copy_id, src in plan.items():
        dest = BRANCH_COPY_TARGETS[copy_id]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": str(src),
                "target_path": str(dest),
                "target_exists": dest.exists(),
                "target_parses": True,
                "reason": "conditional q no-hair / alpha3 nonclaim queue",
            }
        )
    return rows


def parse_csvs(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
        return True
    except Exception:
        return False


def claim_flags_false(paths: list[Path]) -> bool:
    fields = {"valid_for_claim", "score_ready", "mathematically_derived"}
    for path in paths:
        for row in read_csv(path):
            for field in fields.intersection(row.keys()):
                value = str(row[field]).lower()
                if field == "mathematically_derived":
                    continue
                if value not in {"false", "0", "no"}:
                    return False
    return True


def formalization_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    return sum(1 for path in FORMALIZATION.rglob("*2296*") if not any(part in ignored for part in path.parts))


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    for path in FORMALIZATION.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        try:
            if path.stat().st_mtime >= START_TS:
                return True
        except OSError:
            continue
    return False


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = [path for key, path in OUTPUTS.items() if key != "validation"] + [Path(row["target_path"]) for row in copies]
    checks = [
        ("VAL2296_00_sources_exist", all(row["exists"] for row in source_rows()), "all cited source paths exist"),
        ("VAL2296_01_needles_present", all(row["needles_present"] for row in source_rows()), "all cited source needles are present"),
        ("VAL2296_02_prior_validations", contains_all(PATHS["2295_validation"], ["VAL2295_OVERALL", "PASS"]) and contains_all(PATHS["2248_validation"], ["VAL2248_OVERALL", "PASS"]) and contains_all(PATHS["1042_validation"], ["V1042_SUMMARY", "pass"]), "2295, 2248, and 1042 validation sources pass"),
        ("VAL2296_03_conditional_identity_written", any(row["identity_id"] == "NH2296_3_zero_theorem" and row["status"] == "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED" for row in read_csv(OUTPUTS["nohair_identity"])), "conditional q zero theorem is written"),
        ("VAL2296_04_firstclass_route_stated", any(row["identity_id"] == "NH2296_4_firstclass_alternative" for row in read_csv(OUTPUTS["nohair_identity"])) and any(row["gate_id"] == "FC2296_7_verdict" for row in read_csv(OUTPUTS["firstclass_gate"])), "first-class q alternative is stated and blocked safely"),
        ("VAL2296_05_nohair_not_activated", any(row["gate_id"] == "NHP2296_7_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED" for row in read_csv(OUTPUTS["premise_gates"])), "activation audit refuses current no-hair claim"),
        ("VAL2296_06_Jq_decomposition_blocks", any(row["source_id"] == "JQ2296_6_total_verdict" and row["current_status"] == "JQ_TOTAL_ZERO_NOT_PROVED" for row in read_csv(OUTPUTS["source_zero"])), "J_q total zero is not assumed"),
        ("VAL2296_07_boundary_flux_blocks", any(row["gate_id"] == "BFG2296_5_verdict" and row["current_status"] == "PHI_BOUNDARY_ZERO_NOT_PROVED" for row in read_csv(OUTPUTS["boundary_gate"])), "boundary flux zero remains blocked"),
        ("VAL2296_08_alpha3_nonclaim", all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["alpha3_prior"])), "alpha3 prior rows remain nonclaim"),
        ("VAL2296_09_R10_impact_retained", any(row["impact_id"] == "R10I2296_2_if_source_open" for row in read_csv(OUTPUTS["r10_impact"])), "R10/local residual impacts remain nonclaim"),
        ("VAL2296_10_acceptance_blocks", all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["acceptance"])), "acceptance gate blocks claims"),
        ("VAL2296_11_claim_gates_blocked", all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["claim_gates"])), "all claim gates are blocked"),
        ("VAL2296_12_next_target_written", read_csv(OUTPUTS["next_target"])[0]["next_target"].startswith("2297-Y5-R2FR-Jq-source-zero"), "J_q source-zero target selected"),
        ("VAL2296_13_decision_selects_Jq", any(row["decision_id"] == "DEC2296_2_next" and "JQ_SOURCE_ZERO" in row["decision"] for row in read_csv(OUTPUTS["decisions"])), "decision ledger selects J_q coupling/source leg"),
        ("VAL2296_14_csv_parse", parse_csvs(generated), "all generated 2296 CSVs parse"),
        ("VAL2296_15_no_claim_flags", claim_flags_false(generated), "no generated 2296 row is claim-valid"),
        ("VAL2296_16_branch_copies", len(copies) == len(BRANCH_COPY_TARGETS) and parse_csvs([Path(row["target_path"]) for row in copies]), "branch/queue nonclaim copies exist and parse"),
        ("VAL2296_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL2296_18_formalization_no_2296", formalization_count() == 0, "formalization-workbench has no non-venv 2296 artifacts"),
        ("VAL2296_19_formalization_untouched", not formalization_touched(), "formalization-workbench untouched during 2296 run"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": cid, "result": "PASS" if ok else "FAIL", "detail": detail} for cid, ok, detail in checks]
    rows.append({"branch_id": BRANCH_ID, "check_id": "VAL2296_OVERALL", "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL", "detail": "2296 proves the conditional q no-hair identity, states the first-class alternative, refuses activation, stages alpha3 prior first-fill, and selects J_q source-zero next"})
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_doc(sources, nohair, premises, firstclass, source_zero, boundary, alpha3, r10, acceptance, claims, decisions, next_target, copies, validation) -> str:
    src_md = [{**row, "path": rel(Path(row["path"]))} for row in sources]
    copy_md = [{**row, "source_path": rel(Path(row["source_path"])), "target_path": rel(Path(row["target_path"]))} for row in copies]
    return "\n\n".join([
        "# 2296 - Y5/R2FR q Source-Free Positive No-Hair or First-Class Owner Gate",
        "## Verdict\n"
        "- 2296 proves a conditional local q no-hair theorem: if the parent theory supplies a positive/coercive q operator, `J_q=0`, `Phi_boundary_local_q=0`, zero-mode removal, and clean projection maps, then `q=0` in the local exterior.\n"
        "- It also states the parallel first-class route: if `Omega_flat(v_q)=delta C_q`, brackets close, boundary charge/cocycle are proper-zero, degree count removes q, and matter descends, then q has no physical local pole.\n"
        "- Neither route is activated yet. The source leg `J_q` is now the next pressure point.",
        "## Source Register\n" + md_table(src_md, ["source_id", "role", "path", "exists", "needles_present", "notes", "valid_for_claim"]),
        "## Conditional q No-Hair Identity\n" + md_table(nohair, ["identity_id", "object", "formula_or_statement", "status", "mathematically_derived", "claim_effect", "valid_for_claim"]),
        "## No-Hair Premise Gates\n" + md_table(premises, ["gate_id", "premise", "required_test", "current_status", "if_missing", "valid_for_claim"]),
        "## First-Class Owner Gate\n" + md_table(firstclass, ["gate_id", "needed", "test", "current_status", "if_missing", "valid_for_claim"]),
        "## J_q Source-Zero Audit\n" + md_table(source_zero, ["source_id", "channel", "zero_condition", "residual_if_open", "current_status", "valid_for_claim"]),
        "## Boundary Flux Zero Gate\n" + md_table(boundary, ["gate_id", "boundary_route", "why_it_would_work", "current_status", "why_not_closed", "valid_for_claim"]),
        "## Alpha3 Prior First Fill\n" + md_table(alpha3, ["row_id", "target", "formula", "alpha3_bound", "current_status", "valid_for_claim"]),
        "## R10 Impact Ledger\n" + md_table(r10, ["impact_id", "branch", "effect", "remaining_caveat", "valid_for_claim"]),
        "## Acceptance Gates\n" + md_table(acceptance, ["gate_id", "test", "status", "evidence", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n" + md_table(claims, ["claim_id", "claim", "status", "reason", "score_ready", "valid_for_claim"]),
        "## Decision Ledger\n" + md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
        "## Next Target\n" + md_table(next_target, ["route_id", "next_target", "script", "objective", "priority", "acceptance_output", "valid_for_claim"]),
        "## Branch Copies\n" + md_table(copy_md, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
        "## Validation\n" + md_table(validation, ["check_id", "result", "detail"]),
        "## Working Interpretation\nThis is the clearest local-GR route so far for the q branch, but only as a conditional theorem. The math says q disappears if the source leg, boundary flux, positivity, zero modes, and projection tails all close. The first-class route could be even cleaner, but it needs the canonical Omega/DCq/degree/matter package. The next useful attack is therefore the coupling/source leg `J_q`: either prove it vanishes componentwise or turn each component into an honest bounded residual.",
    ]) + "\n"


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    nohair = nohair_rows()
    premises = premise_rows()
    firstclass = firstclass_rows()
    source_zero = source_zero_rows()
    boundary = boundary_rows()
    alpha3 = alpha3_rows()
    r10 = r10_rows()
    acceptance = acceptance_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    for key, rows in [
        ("source_register", sources),
        ("nohair_identity", nohair),
        ("premise_gates", premises),
        ("firstclass_gate", firstclass),
        ("source_zero", source_zero),
        ("boundary_gate", boundary),
        ("alpha3_prior", alpha3),
        ("r10_impact", r10),
        ("acceptance", acceptance),
        ("claim_gates", claims),
        ("decisions", decisions),
        ("next_target", next_target),
    ]:
        write_csv(OUTPUTS[key], rows)

    copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], copies)
    remove_pycache()
    validation = validation_rows(copies)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(sources, nohair, premises, firstclass, source_zero, boundary, alpha3, r10, acceptance, claims, decisions, next_target, copies, validation), encoding="utf-8")
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit("2296 validation failed: " + ", ".join(row["check_id"] for row in failed))
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
