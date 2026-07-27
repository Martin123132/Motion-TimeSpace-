from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3410-Y5-R2FR-q_loc-beta-alpha-vector-residue-split-under-AX1090.md"

SOURCES = {
    "doc_3409": ROOT / "3409-Y5-R2FR-nonEH-residue-bound-pack-relative-to-GR-pole-under-AX1090.md",
    "channels_3409": OUT / "P8_Y5_R2FR_3409_NON_EH_RESIDUE_CHANNELS.csv",
    "locks_3409": OUT / "P8_Y5_R2FR_3409_EMPIRICAL_LOCKS.csv",
    "gates_3409": OUT / "P8_Y5_R2FR_3409_PROMOTION_GATES.csv",
    "next_3409": OUT / "P8_Y5_R2FR_3409_NEXT_TARGET.csv",
    "qloc_guard_3403": OUT / "P8_Y5_R2FR_3403_QLOC_BETA_ALPHA_GUARD.csv",
    "beta_envelope_531": OUT / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv",
    "r11_beta_vector_530": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "doc_746": ROOT / "746-Y5-R10-q_loc-to-PPN-or-alpha3-projection-map-contract.md",
    "doc_747": ROOT / "747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md",
    "doc_748": ROOT / "748-Y5-R10-q_loc-vector-parity-zero-theorem-or-Wqalpha3-source-row.md",
    "doc_749": ROOT / "749-Y5-R10-q_loc-vector-component-decomposition-or-alpha3-response-operator-fill.md",
    "doc_869": ROOT / "869-Y5-R10-q_loc-residual-vector-decomposition-or-zero-theorem.md",
    "doc_3064": ROOT / "3064-Y5-R2FR-GammaKhat-q_loc-double-zero-proof-or-GK-component-bound-runner-under-AX1090.md",
    "alpha_gate_746": OUT / "P8_Y5_R10_746_ALPHA3_MOMENTUM_FLUX_GATE.csv",
    "pressure_747": OUT / "P8_Y5_R10_747_WQALPHA3_COEFFICIENT_PRESSURE.csv",
    "parity_748": OUT / "P8_Y5_R10_748_VECTOR_PARITY_ZERO_THEOREM_AUDIT.csv",
    "decomp_749": OUT / "P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv",
    "gk_gate_3064": OUT / "P8_Y5_R2FR_3064_GAMMAKHAT_QLOC_PROOF_GATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3410_SOURCE_REGISTER.csv",
    "q_loc_decomposition_theorem": OUT / "P8_Y5_R2FR_3410_QLOC_DECOMPOSITION_THEOREM.csv",
    "ppn_lane_split": OUT / "P8_Y5_R2FR_3410_PPN_LANE_SPLIT.csv",
    "alpha_vector_product_bound": OUT / "P8_Y5_R2FR_3410_ALPHA_VECTOR_PRODUCT_BOUND.csv",
    "vector_zero_proof_audit": OUT / "P8_Y5_R2FR_3410_VECTOR_ZERO_PROOF_AUDIT.csv",
    "scalar_safe_branch_contract": OUT / "P8_Y5_R2FR_3410_SCALAR_SAFE_BRANCH_CONTRACT.csv",
    "derived_bound_formulas": OUT / "P8_Y5_R2FR_3410_DERIVED_BOUND_FORMULAS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3410_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3410_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3410_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3410_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3410_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_optional(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


qloc_guard = load_optional(SOURCES["qloc_guard_3403"])
beta_row = find_row(qloc_guard, "guard_id", "QG3403_0_beta_projection")
alpha_warning_row = find_row(qloc_guard, "guard_id", "QG3403_1_alpha3_warning")
acceptance_row = find_row(qloc_guard, "guard_id", "QG3403_2_acceptance")


def float_or_none(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


Q_PROXY = float_or_none(beta_row.get("value")) or 7.432631961576971e-06
BETA_BOUND = float_or_none(beta_row.get("beta_bound")) or 7.8e-05
ALPHA_WARNING = float_or_none(alpha_warning_row.get("value")) or 185815799039424.3
ALPHA3_BOUND_INFERRED = Q_PROXY / ALPHA_WARNING
PRODUCT_LIMIT = ALPHA3_BOUND_INFERRED / Q_PROXY


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3409": "non-EH residue bound pack and next-target handoff",
        "channels_3409": "q_loc residue denominator and no-cancellation context",
        "locks_3409": "beta and alpha3 warning locks",
        "gates_3409": "local-GR blocked gate after 3409",
        "next_3409": "3410 target declaration",
        "qloc_guard_3403": "numeric beta-only q_proxy and alpha3 warning",
        "beta_envelope_531": "q_loc beta envelope and alpha3 guard carry-through",
        "r11_beta_vector_530": "componentwise q_loc/vector/source/readout risks",
        "doc_746": "componentwise q_loc projection map contract",
        "doc_747": "alpha3 coefficient pressure derivation",
        "doc_748": "conditional vector-parity zero theorem",
        "doc_749": "q_loc component decomposition and response operator contract",
        "doc_869": "q_loc identity decomposition and retained residuals",
        "doc_3064": "GammaKhat/Khat response identity bottleneck",
        "alpha_gate_746": "alpha3 momentum-flux gate table",
        "pressure_747": "W_q_alpha3 f_qV pressure table",
        "parity_748": "vector parity zero theorem audit",
        "decomp_749": "q_loc component decomposition contract",
        "gk_gate_3064": "GammaKhat q_loc proof gates",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def q_loc_decomposition_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "QDT3410_0_define_frame",
            "statement": "Choose a local asymptotic rest frame with unit timelike u^mu, spatial projector h^mu_nu=delta^mu_nu+u^mu u_nu, and fixed observed readout g_obs.",
            "mathematical_form": "q_loc^nu = -(u_mu q_loc^mu) u^nu + h^nu_mu q_loc^mu",
            "result": "splits the retained residual into time/scalar and spatial/vector pieces before any PPN claim",
            "status": "KINEMATIC_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "step_id": "QDT3410_1_Hodge_split",
            "statement": "On each compact local spatial slice, decompose the spatial piece into scalar-longitudinal and transverse/vector parts.",
            "mathematical_form": "h^nu_mu q_loc^mu = D^nu chi_q + q_T^nu, with D_nu q_T^nu=0 and u_nu q_T^nu=0, modulo harmonic boundary modes",
            "result": "D^nu chi_q feeds scalar PPN/fifth-force lanes; q_T^nu and harmonic boundary modes feed preferred-frame/vector lanes",
            "status": "CONDITIONAL_ON_BOUNDARY_CLASS",
            "valid_for_claim": False,
        },
        {
            "step_id": "QDT3410_2_even_odd_split",
            "statement": "Separate exchange-even scalar source pieces from exchange-odd vector/momentum pieces.",
            "mathematical_form": "q_loc = q_even_scalar + q_odd_vector + q_boundary_harmonic + q_source_readout",
            "result": "alpha_i/xi silence requires q_odd_vector=q_boundary_harmonic=0 or a parent-owned zero response",
            "status": "DERIVED_ROUTING_NOT_ZERO",
            "valid_for_claim": False,
        },
        {
            "step_id": "QDT3410_3_no_single_scalar_pass",
            "statement": "The beta-only q_proxy cannot be reused as an all-channel pass.",
            "mathematical_form": "Delta_PPN[q_loc]={delta_gamma_q,delta_beta_q,alpha1_q,alpha2_q,alpha3_q,xi_q,alpha_q(lambda)}",
            "result": "each component needs its own projection coefficient and empirical lock",
            "status": "HARD_POLICY_FROM_746_3409",
            "valid_for_claim": False,
        },
    ]


def ppn_lane_split() -> list[dict[str, Any]]:
    return [
        {
            "lane_id": "PLS3410_0_gamma",
            "observable_lane": "gamma-1 / spatial curvature slip",
            "source_piece": "scalar-longitudinal q_chi and projector/source slip",
            "projection_law": "delta_gamma_q = W_q_gamma * f_gamma * q_proxy",
            "known_number": "MISSING_W_q_gamma_AND_f_gamma",
            "pass_condition": "numeric sourced product below gamma lock, or theorem-zero of spatial slip",
            "current_status": "UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "lane_id": "PLS3410_1_beta",
            "observable_lane": "beta-1 / U^2 nonlinear source hair",
            "source_piece": "scalar-even U^2 component of q_loc",
            "projection_law": "delta_beta_q = W_q_beta * f_beta * q_proxy",
            "known_number": f"q_proxy={Q_PROXY}; beta_bound={BETA_BOUND}; stored_fraction={Q_PROXY / BETA_BOUND}",
            "pass_condition": "W_q_beta*f_beta stays order unity or smaller in same normalization, with source/readout theorem",
            "current_status": "PROMISING_BUT_PROVISIONAL",
            "valid_for_claim": False,
        },
        {
            "lane_id": "PLS3410_2_alpha1_alpha2",
            "observable_lane": "preferred-frame alpha1/alpha2",
            "source_piece": "transverse vector q_T, domain vector, or hidden frame spurion",
            "projection_law": "alpha{1,2}_q = W_q_alpha{1,2} * f_qV * q_proxy",
            "known_number": "MISSING_ALPHA1_ALPHA2_LOCKS_AND_RESPONSE_PRODUCTS",
            "pass_condition": "f_qV=0 by theorem, or sourced products pass alpha1/alpha2 locks independently",
            "current_status": "HIGH_RISK_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "lane_id": "PLS3410_3_alpha3",
            "observable_lane": "preferred-frame alpha3 / momentum nonconservation",
            "source_piece": "momentum-flux projection of q_T or boundary/domain flux",
            "projection_law": "alpha3_q = W_q_alpha3 * f_qV * q_proxy",
            "known_number": f"q_proxy={Q_PROXY}; inferred_alpha3_bound={ALPHA3_BOUND_INFERRED:.16g}; |W_q_alpha3 f_qV|<={PRODUCT_LIMIT:.16g}",
            "pass_condition": "theorem-zero of momentum flux or source-backed product below the limit",
            "current_status": "TIGHTEST_ACTIVE_QLOC_RISK",
            "valid_for_claim": False,
        },
        {
            "lane_id": "PLS3410_4_xi",
            "observable_lane": "preferred-location xi",
            "source_piece": "anisotropic domain/projector/boundary harmonic component",
            "projection_law": "xi_q = W_q_xi * f_xi * q_proxy",
            "known_number": "MISSING_W_q_xi_AND_DOMAIN_ANISOTROPY_FRACTION",
            "pass_condition": "no anisotropic boundary/domain spurion, or sourced xi product below lock",
            "current_status": "HIGH_RISK_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "lane_id": "PLS3410_5_R10",
            "observable_lane": "finite-range alpha(lambda)",
            "source_piece": "finite-range scalar kernel from q_chi/source normalization",
            "projection_law": "alpha_q(lambda)=W_q_R10(lambda)*f_range(lambda)*q_proxy",
            "known_number": "MISSING_RANGE_KERNEL_AND_NUMERATOR",
            "pass_condition": "no local finite-range kernel or full sourced comparison to alpha_bound(lambda)",
            "current_status": "DEFER_UNTIL_RANGE_KERNEL_EXISTS",
            "valid_for_claim": False,
        },
    ]


def alpha_vector_product_bound() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "AVP3410_0_product_law",
            "quantity": "alpha3_q",
            "formula": "alpha3_q = W_q_alpha3 * f_qV * q_proxy",
            "q_proxy": Q_PROXY,
            "bound": ALPHA3_BOUND_INFERRED,
            "derived_limit": PRODUCT_LIMIT,
            "interpretation": "only the product W_q_alpha3*f_qV matters; order-one vector leakage is excluded",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AVP3410_1_if_response_order_one",
            "quantity": "f_qV_limit_if_W_order_one",
            "formula": "f_qV <= alpha3_bound/q_proxy",
            "q_proxy": Q_PROXY,
            "bound": ALPHA3_BOUND_INFERRED,
            "derived_limit": PRODUCT_LIMIT,
            "interpretation": "the vector/momentum fraction must be effectively zero unless the response weight is itself tiny",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AVP3410_2_if_vector_fraction_order_one",
            "quantity": "W_q_alpha3_limit_if_f_order_one",
            "formula": "W_q_alpha3 <= alpha3_bound/q_proxy",
            "q_proxy": Q_PROXY,
            "bound": ALPHA3_BOUND_INFERRED,
            "derived_limit": PRODUCT_LIMIT,
            "interpretation": "a mostly vector q_loc would need an unnatural response suppression, so theorem-zero is preferred",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AVP3410_3_verdict",
            "quantity": "alpha_vector_status",
            "formula": "pass iff f_qV=0 by parent theorem or abs(W_q_alpha3*f_qV)<=limit with sourced rows",
            "q_proxy": Q_PROXY,
            "bound": ALPHA3_BOUND_INFERRED,
            "derived_limit": PRODUCT_LIMIT,
            "interpretation": "not passed; this is a pressure bound and next-proof target",
            "valid_for_claim": False,
        },
    ]


def vector_zero_proof_audit() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "VZ3410_0_no_spurion",
            "needed_clause": "q_loc carries no independent local vector, aether, wall normal, or preferred-frame marker after quotient/readout.",
            "mathematical_form": "q_loc^nu is built only from scalar invariants, g_obs, u_matter^mu, and compact boundary data that vanish in the local rest frame",
            "would_imply": "no alpha_i/xi source beyond ordinary PPN matter velocities",
            "current_status": "UNSIGNED",
            "blocker": "parent representative/readout map does not yet forbid vector/domain spurions",
            "valid_for_claim": False,
        },
        {
            "clause_id": "VZ3410_1_Hodge_transverse_zero",
            "needed_clause": "transverse vector and harmonic boundary components vanish.",
            "mathematical_form": "q_T^i=0 and q_harmonic^i=0 on the compact local collar",
            "would_imply": "f_qV=0 for alpha1/alpha2/alpha3/xi lanes",
            "current_status": "CONDITIONAL_ONLY",
            "blocker": "boundary class and P_loc commutator remain unsigned",
            "valid_for_claim": False,
        },
        {
            "clause_id": "VZ3410_2_momentum_map_zero",
            "needed_clause": "q_loc vector flux is a first-class vertical momentum-map constraint.",
            "mathematical_form": "P_mom q_loc = delta G[epsilon]/delta epsilon with G[epsilon]=int epsilon C_X + Q_boundary, C_X=0, Q_boundary=0",
            "would_imply": "preferred-frame momentum flux is gauge/constraint, not physical",
            "current_status": "NOT_DERIVED",
            "blocker": "parent symplectic potential, vertical generator, algebra closure and boundary silence are not signed",
            "valid_for_claim": False,
        },
        {
            "clause_id": "VZ3410_3_GK_Ward_identity",
            "needed_clause": "Gamma_eff and K_hat are metric-response partners from one parent scalar-density action.",
            "mathematical_form": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu}; nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + B_GK",
            "would_imply": "on shell with B_GK=0, q_loc is Euler/boundary exact and both scalar and vector lanes can close",
            "current_status": "BEST_NEXT_PROOF_ROUTE_NOT_SIGNED",
            "blocker": "3064 says K_hat metric-response identity is not matched to current MTS symbols",
            "valid_for_claim": False,
        },
        {
            "clause_id": "VZ3410_4_verdict",
            "needed_clause": "f_qV=0 can be claimed now.",
            "mathematical_form": "VZ3410_0 through VZ3410_3 closed",
            "would_imply": "q_loc alpha-vector lanes vanish and beta/gamma scalar lanes remain to be scored",
            "current_status": "NOT_PROVED",
            "blocker": "at least one essential parent clause is unsigned in each route",
            "valid_for_claim": False,
        },
    ]


def scalar_safe_branch_contract() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "SSB3410_0_scalar_only_hypothesis",
            "hypothesis": "q_loc is purely scalar/even in the compact local branch.",
            "required_parent_clauses": "no vector spurion; q_T=0; harmonic boundary zero; same observed readout; source-normalized GM",
            "remaining_tests": "gamma slip, beta U^2 conversion, finite-range R10 if kernel exists, WEP/clock if composition-coupled",
            "allowed_statement": "if these clauses are proven, q_loc preferred-frame channels are zero and q_loc reduces to scalar PPN/fifth-force checks",
            "forbidden_statement": "q_loc passes local GR because beta-only q_proxy is below the beta bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": "SSB3410_1_vector_survives",
            "hypothesis": "any physical q_T or momentum-flux fraction survives.",
            "required_parent_clauses": "source-backed W_q_alpha3 and f_qV, plus alpha1/alpha2/xi maps",
            "remaining_tests": "abs(W_q_alpha3*f_qV)<=5.38167370680806e-15 and independent alpha1/alpha2/xi locks",
            "allowed_statement": "q_loc becomes a bounded residual only if the vector product is tiny with source backing",
            "forbidden_statement": "hide vector leakage in the beta score or cancel it against other sectors",
            "valid_for_claim": False,
        },
    ]


def derived_bound_formulas() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "DBF3410_0_component_envelope",
            "formula": "Delta_q_loc_abs <= abs(delta_gamma_q)+abs(delta_beta_q)+abs(alpha1_q)+abs(alpha2_q)+abs(alpha3_q)+abs(xi_q)+abs(alpha_q(lambda))",
            "meaning": "no cancellation between scalar and preferred-frame lanes",
            "inputs_needed": "all W coefficients, component fractions, observed-frame readout, sourced locks",
            "valid_for_claim": False,
        },
        {
            "formula_id": "DBF3410_1_scalar_lanes",
            "formula": "delta_beta_q=W_beta f_beta q_proxy; delta_gamma_q=W_gamma f_gamma q_proxy; alpha_q(lambda)=W_R10(lambda) f_range(lambda) q_proxy",
            "meaning": "scalar/even q_loc is not automatically safe, but it is the route where the existing q_proxy might matter constructively",
            "inputs_needed": "U2 conversion, gamma slip map, range kernel, R10 curve/provenance",
            "valid_for_claim": False,
        },
        {
            "formula_id": "DBF3410_2_preferred_frame",
            "formula": "alphaA_q=W_alphaA f_qV q_proxy for A in {1,2,3}; xi_q=W_xi f_xi q_proxy",
            "meaning": "preferred-frame/local anisotropy lanes are separate and tighter than beta",
            "inputs_needed": "f_qV or zero theorem; W_alphaA; W_xi; bounds for each lane",
            "valid_for_claim": False,
        },
        {
            "formula_id": "DBF3410_3_alpha3_pressure",
            "formula": f"abs(W_q_alpha3*f_qV) <= {PRODUCT_LIMIT:.16g}",
            "meaning": "alpha3 effectively demands vector zero unless a very small product is parent-sourced",
            "inputs_needed": "theorem-zero or source-backed response product",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3410_0_split_written",
            "gate": "q_loc is separated into scalar, vector, preferred-frame, source/readout and range lanes",
            "current_result": "PASS_AS_NONCLAIM_DERIVATION_INTERFACE",
            "promotes_if": "not a claim gate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3410_1_alpha_vector_zero",
            "gate": "q_loc alpha-vector leakage is theorem-zero",
            "current_result": "FAIL_NOT_PROVED",
            "promotes_if": "no-spurion, Hodge transverse zero, momentum-map zero, or GK Ward identity is parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3410_2_alpha_vector_bound",
            "gate": "if vector leakage survives, the product bound is source-backed",
            "current_result": "FAIL_NO_W_OR_f_SOURCE_ROW",
            "promotes_if": f"abs(W_q_alpha3*f_qV)<={PRODUCT_LIMIT:.16g} plus alpha1/alpha2/xi checks",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3410_3_scalar_beta_gamma",
            "gate": "scalar q_loc lanes pass gamma/beta/R10/source-readout checks",
            "current_result": "FAIL_U2_GAMMA_RANGE_READOUT_UNSIGNED",
            "promotes_if": "W_beta, W_gamma, range kernel and same-readout/source normalization are signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3410_4_local_GR",
            "gate": "q_loc no longer blocks local GR",
            "current_result": "BLOCKED",
            "promotes_if": "PG3410_1 or PG3410_2 passes, and PG3410_3 passes or scalar lanes are theorem-zero",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DL3410_0",
            "decision": "Do not use beta-only q_proxy as a local-GR pass.",
            "rationale": "The same stored q_proxy would violate alpha3 by a huge factor if it lands in the momentum-flux lane.",
            "claim_effect": "q_loc remains blocked but now with a precise split",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DL3410_1",
            "decision": "Treat theorem-zero as the natural route and tiny product bounds as fallback.",
            "rationale": f"alpha3 requires abs(W_q_alpha3*f_qV)<={PRODUCT_LIMIT:.16g}; tuning that by hand would be ugly and noncompetitive.",
            "claim_effect": "next work should derive vector silence, not fit a tiny coefficient",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DL3410_2",
            "decision": "Promote the K_hat metric-response identity as the next constructive proof target.",
            "rationale": "If Gamma_eff and K_hat are one parent action response pair, q_loc can become a Ward/Euler/boundary-exact residual instead of an empirical fudge.",
            "claim_effect": "focus shifts from circling q_loc to attacking its parent identity",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3411-Y5-R2FR-Khat-metric-response-identity-for-q_loc-Ward-zero-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3411_Khat_metric_response_identity_for_q_loc_Ward_zero.py",
            "objective": "attempt to prove K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} in the current branch, then use the Ward identity to kill q_loc scalar and vector residuals on compact local vacuum domains",
            "why_next": "this is the leap-forward route: it could remove q_loc as a physical local residual instead of merely bounding its alpha-vector product",
            "valid_for_claim": False,
        },
        {
            "target_id": "3412-Y5-R2FR-q_loc-vector-product-source-row-if-Ward-route-fails-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3412_q_loc_vector_product_source_row_if_Ward_route_fails.py",
            "objective": "if the Ward route fails, source W_q_alpha3 and f_qV or demote q_loc to an explicit bounded closure residual",
            "why_next": "this is the fallback if K_hat cannot be parent-matched",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3410_0",
            "script": str(Path(__file__).resolve()),
            "q_proxy": Q_PROXY,
            "beta_bound": BETA_BOUND,
            "alpha3_bound_inferred": ALPHA3_BOUND_INFERRED,
            "product_limit": PRODUCT_LIMIT,
            "claim_status": "NONCLAIM_DERIVATION_INTERFACE",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    lanes = generated["ppn_lane_split"]
    gates = generated["promotion_gates"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]).lower() == "true" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    alpha3_lane = any(row.get("lane_id") == "PLS3410_3_alpha3" for row in lanes)
    vector_blocked = any(
        row.get("gate_id") == "PG3410_1_alpha_vector_zero" and row.get("current_result") == "FAIL_NOT_PROVED"
        for row in gates
    )
    local_blocked = any(
        row.get("gate_id") == "PG3410_4_local_GR" and row.get("current_result") == "BLOCKED"
        for row in gates
    )
    product_limit_ok = 0 < PRODUCT_LIMIT < 1e-12
    next_is_ward = "Khat-metric-response" in generated["next_target"][0]["target_id"]
    rows = [
        {
            "check_id": "VAL3410_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3410_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3410_2_all_nonclaim",
            "check": "all rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3410 is a derivation/projection interface, not a local-GR claim",
        },
        {
            "check_id": "VAL3410_3_alpha3_lane",
            "check": "alpha3 lane is explicitly separated",
            "passed": alpha3_lane,
            "detail": "PLS3410_3_alpha3 written",
        },
        {
            "check_id": "VAL3410_4_product_limit",
            "check": "alpha3 product limit is derived from q_proxy and alpha warning",
            "passed": product_limit_ok,
            "detail": f"limit={PRODUCT_LIMIT:.16g}",
        },
        {
            "check_id": "VAL3410_5_vector_zero_not_faked",
            "check": "vector zero theorem is not falsely promoted",
            "passed": vector_blocked,
            "detail": "PG3410_1_alpha_vector_zero remains FAIL_NOT_PROVED",
        },
        {
            "check_id": "VAL3410_6_local_GR_blocked",
            "check": "q_loc still blocks local GR until split gates pass",
            "passed": local_blocked,
            "detail": "PG3410_4_local_GR remains BLOCKED",
        },
        {
            "check_id": "VAL3410_7_next_target",
            "check": "next target attacks the Khat metric-response identity",
            "passed": next_is_ward,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3410_8_overall",
            "check": "3410 q_loc split is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3410 - q_loc Beta/Alpha Vector Residue Split",
            "## Summary\n"
            "- This checkpoint does the thing 3409 demanded: it separates q_loc into scalar PPN lanes and preferred-frame/vector lanes.\n"
            "- The beta-only q_proxy remains interesting, but it cannot be used as a local-GR pass.\n"
            f"- The alpha3 product pressure is severe: `|W_q_alpha3 f_qV| <= {PRODUCT_LIMIT:.16g}`.\n"
            "- Therefore the competitive route is not coefficient fiddling; it is proving vector/momentum-flux zero from the parent action.",
            "## q_loc Decomposition Theorem\n" + md_table(generated["q_loc_decomposition_theorem"]),
            "## PPN Lane Split\n" + md_table(generated["ppn_lane_split"]),
            "## Alpha Vector Product Bound\n" + md_table(generated["alpha_vector_product_bound"]),
            "## Vector Zero Proof Audit\n" + md_table(generated["vector_zero_proof_audit"]),
            "## Scalar Safe Branch Contract\n" + md_table(generated["scalar_safe_branch_contract"]),
            "## Derived Bound Formulas\n" + md_table(generated["derived_bound_formulas"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "This is a real fork. If q_loc is parent-proved scalar/even or Ward-exact, the scary preferred-frame lane can be killed and the remaining fight becomes beta/gamma/R10/source normalization. "
            "If q_loc has a physical vector/momentum fraction, the alpha3 product bound is so tight that a competitive theory needs a structural zero, not a tuned tiny coefficient.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "q_loc_decomposition_theorem": q_loc_decomposition_theorem(),
        "ppn_lane_split": ppn_lane_split(),
        "alpha_vector_product_bound": alpha_vector_product_bound(),
        "vector_zero_proof_audit": vector_zero_proof_audit(),
        "scalar_safe_branch_contract": scalar_safe_branch_contract(),
        "derived_bound_formulas": derived_bound_formulas(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3410 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
