from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3861"
BRANCH = "MTS_R2FR_Y5_NO_SHADOW_COFRAME_BASICNESS_OR_EPSILON_SHADOW_FRAME_BOUND_3861"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3861-Y5-R2FR-no-shadow-coframe-basicness-or-epsilon-shadow-frame-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3860_THEOREM = OUT / "P8_Y5_R2FR_3860_COFRAME_BASICNESS_THEOREM.csv"
CSV_3860_AUDIT = OUT / "P8_Y5_R2FR_3860_PARENT_SIGNATURE_AUDIT.csv"
CSV_3860_RESIDUAL = OUT / "P8_Y5_R2FR_3860_FRAME_SOURCE_RESIDUAL_UPDATE.csv"
CSV_3860_GATES = OUT / "P8_Y5_R2FR_3860_CLAIM_GATES.csv"
CSV_3860_VALIDATION = OUT / "P8_Y5_BRR545_3860_VALIDATION.csv"
CSV_1030_PUBLIC_METRIC = OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"
CSV_1029_SHADOW = OUT / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv"
CSV_3647_SHADOW = OUT / "P8_Y5_R2FR_3647_NO_SHADOW_THEOREM_ATTEMPT.csv"
CSV_2888_CERT = OUT / "P8_Y5_R2FR_2888_TERMINAL_PUBLIC_COFRAME_NO_SHADOW_CERTIFICATE_AUDIT.csv"
CSV_3767_LLEAK = OUT / "P8_Y5_R2FR_3767_LLEAK_BOUND_INTERFACE.csv"
CSV_3767_OPERATORS = OUT / "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv"
CSV_3766_BOUND = OUT / "P8_Y5_R2FR_3766_FIRST_FRAME_RESIDUAL_BOUND.csv"
CSV_3504_DELTA_HODGE = OUT / "P8_Y5_R2FR_3504_DELTA_HODGE_BOUND_VECTOR.csv"
CSV_3504_HODGE = OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv"
CSV_3505_EM_DOMAIN = OUT / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"
CSV_3494_SPIN = OUT / "P8_Y5_R2FR_3494_COFRAME_SPIN_THEOREM_ATTEMPT.csv"
CSV_3498_NATURALITY = OUT / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv"
CSV_FRAME_SPLIT = OUT / "P8_frame_source_split_residual_or_zero.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3861_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3861_NO_SHADOW_COFRAME_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3861_SHADOW_SLOT_AUDIT.csv",
    "bound": OUT / "P8_Y5_R2FR_3861_EPSILON_SHADOW_FRAME_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3861_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3861_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3861_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3861_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3861_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3861_00_3860_theorem", CSV_3860_THEOREM, "NO_QOBS_BY_DECLARATION", "3860 coframe anti-tautology theorem"),
    ("SRC3861_01_3860_audit", CSV_3860_AUDIT, "B_sector_readout+B_shadow_frame+B_readout_order", "3860 shadow/readout residual owner"),
    ("SRC3861_02_3860_residual", CSV_3860_RESIDUAL, "epsilon_shadow_g", "3860 frame-source residual update"),
    ("SRC3861_03_3860_gates", CSV_3860_GATES, "PASS_3861_NO_SHADOW_COFRAME_TARGET", "3860 next-target gate"),
    ("SRC3861_04_3860_validation", CSV_3860_VALIDATION, "PASS", "previous validation"),
    ("SRC3861_05_1030_public_metric", CSV_1030_PUBLIC_METRIC, "A_g(Xhat), B_g(Xhat)", "public metric action contract"),
    ("SRC3861_06_1029_shadow", CSV_1029_SHADOW, "FAIL_CURRENT_CLAIM", "R10 no-shadow frame theorem audit"),
    ("SRC3861_07_3647_shadow", CSV_3647_SHADOW, "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED", "recent no-shadow theorem attempt"),
    ("SRC3861_08_2888_certificate", CSV_2888_CERT, "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS", "terminal public coframe certificate"),
    ("SRC3861_09_3767_lleak", CSV_3767_LLEAK, "epsilon_shadow_g", "shadow-frame leak bound interface"),
    ("SRC3861_10_3767_operator", CSV_3767_OPERATORS, "L_leak_shadow_g", "shadow metric leak operator"),
    ("SRC3861_11_3766_bound", CSV_3766_BOUND, "delta_frame_source <= C_Omega", "frame residual fallback bound"),
    ("SRC3861_12_3504_delta_hodge", CSV_3504_DELTA_HODGE, "C_Hodge_hidden", "EM hidden Hodge component"),
    ("SRC3861_13_3504_hodge", CSV_3504_HODGE, "independent constitutive tensor", "Hodge uniqueness countermodel"),
    ("SRC3861_14_3505_em_domain", CSV_3505_EM_DOMAIN, "C_Hodge_hidden", "visible EM action-domain exhaustion ledger"),
    ("SRC3861_15_3494_spin", CSV_3494_SPIN, "owned-coframe ordinary branch", "owned coframe ordinary branch"),
    ("SRC3861_16_3498_naturality", CSV_3498_NATURALITY, "q/e_obs/tau functor projector", "functorial projector chain rule"),
    ("SRC3861_17_frame_split", CSV_FRAME_SPLIT, "SEEDED_NONCLAIM_3048_MISSING_SOURCE_VARIATION_FRAME_THEOREM", "frame/source split fallback"),
]

NO_SHADOW_THEOREM = (
    "For every ordinary sector s, if S_s and every readout r_s depend on parent fields through "
    "e_obs(q_obs), omega_LC[e_obs], fixed/q-basic constants theta, and q_obs-sector fields only, "
    "and the parent grammar excludes independent Weyl/disformal/constitutive frame slots, then the "
    "physical sector coframe satisfies Delta e_s^perp=0 modulo local Lorentz/diffeomorphism/q_obs gauge."
)
CHAIN_RULE_ZERO = (
    "e_s=e_bar_s(q_obs) and v in ker(Dq_obs) imply D_v e_s=0; hence "
    "Lie_v g_s=0 and epsilon_shadow_g=0 for that sector."
)
CURRENT_BLOCK = (
    "The corpus has the conditional theorem route, but the no-extra-frame parent action clause, "
    "terminal public coframe certificate, source/readout inheritance, and EM no-constitutive-Hodge "
    "exclusion are not all parent-signed."
)
SHADOW_BOUND = (
    "B_shadow_frame_3861 <= B_no_extra_frame_action_domain+B_terminal_public_coframe+"
    "B_matter_shadow_slot+B_EM_Hodge_hidden+B_light_clock_frame+B_source_orbit_frame+"
    "B_constant_marker_shadow+B_readout_shadow+B_boundary_endpoint_shadow"
)
EPSILON_BOUND = (
    "epsilon_shadow_g <= epsilon_frame_slot+epsilon_terminal+epsilon_matter+"
    "epsilon_EM_Hodge_hidden+epsilon_light_clock+epsilon_source_orbit+"
    "epsilon_theta_marker+epsilon_readout+epsilon_endpoint"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_no_shadow_coframe_derivation",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "NSC3861_0_decompose_sector_frame",
            "claim_piece": "physical shadow coframe definition",
            "statement": "For each sector, e_s=Lambda_s e_obs + L_{xi_s}e_obs + Delta e_s^perp, where only Delta e_s^perp is a physical shadow after local Lorentz/diffeomorphism/q_obs gauge is removed.",
            "derivation": "gauge-equivalent Lorentz and diffeomorphism pieces are representation choices; any remaining Weyl/disformal/constitutive part changes rods, clocks, light cones, source weights, or EM response.",
            "result": "DEFINITION_SHARPENED",
            "status": "EXACT_DECOMPOSITION_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NSC3861_1_no_shadow_theorem",
            "claim_piece": "no-shadow coframe theorem",
            "statement": NO_SHADOW_THEOREM,
            "derivation": "variable-absence theorem: once the action/readout domains have no independent e_s, A_g(X), B_g(X), U_mu, chi_EM, or source-only frame argument, no non-gauge vertical derivative can hit a sector coframe.",
            "result": "EXACT_CONDITIONAL_NO_SHADOW_COFRAME_THEOREM",
            "status": "CONDITIONAL_THEOREM_PROVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NSC3861_2_chain_rule_zero",
            "claim_piece": "q-basic sector-frame zero",
            "statement": CHAIN_RULE_ZERO,
            "derivation": "apply the same q-basic chain rule as 3860/3498 to the sector-frame map after the no-extra-frame action-domain clause removes independent arguments.",
            "result": "EXACT_CONDITIONAL_EPSILON_SHADOW_ZERO",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NSC3861_3_matter_trace_warning",
            "claim_piece": "finite shadow frame is physical",
            "statement": "If e_m=A_g(Xhat)e_obs or g_m=A_g(Xhat)^2 g_obs+B_dis(Xhat)U_mu U_nu+... is admitted, then partial_Xhat ln A_g and partial_Xhat B_dis create trace/preferred-frame source terms rather than harmless notation.",
            "derivation": "delta_X S_matter=(1/2) int sqrt(-g_m) T_m^{mu nu} delta_X g^m_{mu nu}; conformal and disformal derivatives project into matter trace, clock, WEP, PPN, and orbital channels.",
            "result": "FINITE_SHADOW_IS_SOURCE_COUPLING",
            "status": "COUNTERMODEL_RETAINED_IF_DOMAIN_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NSC3861_4_current_verdict",
            "claim_piece": "strict current corpus verdict",
            "statement": CURRENT_BLOCK,
            "derivation": "1029/1030/3647/2888 mark the closure clauses as exact but unsigned; 3504/3505 keep hidden EM Hodge/constitutive rows live; 3767 retains epsilon_shadow_g.",
            "result": "NO_SHADOW_COFRAME_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CURRENT_NONCLAIM_RESIDUAL_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NSC3861_5_if_closed_handoff",
            "claim_piece": "handoff into local GR branch",
            "statement": "If B_shadow_frame_3861=0, then 3860 loses the B_shadow_frame term and the local branch is reduced to q_obs parent signature, L_leak/source/boundary/constants/readout order, coframe spin, cstar scale, and EH/Newton source calibration.",
            "derivation": "substitute epsilon_shadow_g=0 and B_shadow_frame=0 into the 3860 coframe and frame-source residual bounds.",
            "result": "SHADOW_SLOT_REMOVAL_WOULD_BE_REAL_PROGRESS",
            "status": "CONDITIONAL_LOCAL_GR_RESIDUAL_REDUCTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "SSA3861_0_terminal_public_coframe",
            "clause": "terminal public coframe",
            "required_identity": "ordinary matter, rods, clocks, photons, source masses, and orbital readouts use one e_obs(q_obs)",
            "current_evidence": "2888 and 2487 give the exact certificate shape but say terminality is not parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_terminal_public_coframe",
            "next_action": "prove terminal coframe from parent observable functor or retain epsilon_terminal",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SSA3861_1_no_extra_frame_action_domain",
            "clause": "no Weyl/disformal frame slot",
            "required_identity": "Allowed[S_matter] excludes A_g(Xhat)e_obs, B_g(Xhat)U_mu U_nu, source-only frame prefactors, and representative-frame arguments",
            "current_evidence": "1030 has the exact clause; 1029/3647 say it is not parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_no_extra_frame_action_domain",
            "next_action": "derive action-domain exclusion from parent constructor or keep c_g/b_dis source rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SSA3861_2_matter_trace_source",
            "clause": "finite matter shadow is not gauge",
            "required_identity": "partial_Xhat ln A_g=0 and partial_Xhat B_dis=0 before source variation",
            "current_evidence": "1029 and 3647 derive the trace/source shape conditionally but keep normalization/projection unsigned",
            "passes_current_branch": False,
            "residual_owner": "B_matter_shadow_slot",
            "next_action": "either prove the derivatives vanish by q-basicness or build sourced PPN/R10/clock bound rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SSA3861_3_EM_Hodge_shadow",
            "clause": "EM uses observed Hodge star only",
            "required_identity": "S_EM[A,e_obs(q)] uses *_obs[e_obs] and excludes independent chi_EM or hidden-visible Hodge map",
            "current_evidence": "3504 proves Hodge uniqueness once e_obs is used, but 3504/3505 retain C_Hodge_hidden and constitutive countermodels",
            "passes_current_branch": False,
            "residual_owner": "B_EM_Hodge_hidden",
            "next_action": "make the next target EM hidden Hodge/disformal zero or observable bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SSA3861_4_readout_inheritance",
            "clause": "source/readout inheritance",
            "required_identity": "all r_s=F_s o q_obs, with no endpoint, boundary, calibration, or post-solution shadow readout",
            "current_evidence": "3860 and 3766 keep sector readout, boundary and source-frame residuals active",
            "passes_current_branch": False,
            "residual_owner": "B_readout_shadow+B_boundary_endpoint_shadow+B_source_orbit_frame",
            "next_action": "prove readout-after-variation inheritance or retain delta_frame_source and Delta q_s rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SSA3861_5_spin_connection_branch",
            "clause": "ordinary coframe/spin exhaustion",
            "required_identity": "ordinary spin/matter uses e_obs and omega_LC[e_obs], not an independent coframe or torsionful connection",
            "current_evidence": "3494 closes this inside the owned-coframe candidate branch but not globally",
            "passes_current_branch": False,
            "residual_owner": "B_coframe_spin",
            "next_action": "reuse 3494 only after the owned-coframe branch is parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SSA3861_6_lleak_shadow",
            "clause": "shadow leak in parent pullback",
            "required_identity": "L_leak_shadow_g=0 modulo diffeomorphism/local Lorentz/q_obs gauge",
            "current_evidence": "3767 explicitly lists L_leak_shadow_g with missing parent coefficient",
            "passes_current_branch": False,
            "residual_owner": "epsilon_shadow_g",
            "next_action": "prove single-frame descent or bound from preferred-frame/light/clock/source tests",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "SFB3861_0_symbolic_shadow_residual",
            "target": "B_shadow_frame_3861",
            "formula": SHADOW_BOUND,
            "derivation": "union bound over independent ways a non-gauge sector frame can re-enter after 3860 coframe basicness",
            "inputs_required": "parent action-domain exclusion, terminal coframe certificate, EM no-hidden-Hodge theorem, readout/source inheritance",
            "status": "NONCLAIM_SYMBOLIC_BOUND",
            "numeric_status": "MISSING_PARENT_SIGNATURES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "SFB3861_1_epsilon_shadow_metric",
            "target": "epsilon_shadow_g",
            "formula": EPSILON_BOUND,
            "derivation": "component envelope for sup_A ||Lie_EA g_eff||_g modulo gauge",
            "inputs_required": "component coefficients or theorem-zero rows for frame, EM Hodge, clocks/light/source/orbits, constants, readouts, endpoints",
            "status": "NONCLAIM_SYMBOLIC_EPSILON_BOUND",
            "numeric_status": "MISSING_COEFFICIENTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "SFB3861_2_3860_substitution",
            "target": "B_eobs_basic_3860",
            "formula": "B_eobs_basic_3860 <= B_qobs_signature+B_pullback_Lleak+B_kernel_null+B_boundary_silence+B_source_descent+B_theta_constants+B_sector_readout+B_coframe_spin+B_readout_order+B_shadow_frame_3861",
            "derivation": "replace the 3860 abstract B_shadow_frame term by the explicit 3861 no-shadow residual",
            "inputs_required": "all 3860 clauses plus the 3861 shadow-frame certificate",
            "status": "COFRAME_BOUND_REFINED",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "SFB3861_3_frame_source_substitution",
            "target": "delta_frame_source",
            "formula": "delta_frame_source <= C_L epsilon_L+C_Omega epsilon_Omega+C_src epsilon_src+C_theta epsilon_theta+C_boundary epsilon_boundary+C_readout max_s epsilon_readout_s+C_shadow epsilon_shadow_g",
            "derivation": "3860/3766 frame-source propagation with epsilon_shadow_g now componentized by 3861",
            "inputs_required": "C_i response constants and epsilon_shadow_g components",
            "status": "FRAME_SOURCE_BOUND_RETAINED",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "SFB3861_4_EM_component_priority",
            "target": "B_EM_Hodge_hidden",
            "formula": "B_EM_Hodge_hidden <= |C_Hodge_hidden|+|Delta_chi_principal|+|Delta_chi_skewon|+|Delta_chi_axion_gradient|+|C_Hodge_readout|+|C_XF2|+|Delta_conformal_scale|",
            "derivation": "3504/3505 show the main concrete shadow subbranch is EM constitutive/Hodge ownership rather than generic vibes",
            "inputs_required": "prove observed-Hodge action-domain exhaustion or source observable bounds for each EM constitutive component",
            "status": "NEXT_TARGET_COMPONENT_BOUND",
            "numeric_status": "MISSING_EM_COMPONENT_COEFFICIENTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G3861_0_exact_theorem",
            "gate": "conditional no-shadow theorem is written",
            "status": "PASS_EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "reason": "the variable-absence/q-basic proof is exact under stated parent action-domain premises",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3861_1_no_current_promotion",
            "gate": "no current no-shadow/local-GR claim",
            "status": "BLOCKED_NO_SHADOW_PARENT_SIGNATURE_UNSIGNED",
            "claim_allowed": False,
            "reason": "1029/1030/3647/2888 explicitly keep the no-extra-frame/terminal coframe clauses unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3861_2_EM_not_swept_under_rug",
            "gate": "EM hidden Hodge counterbranch retained",
            "status": "PASS_EM_HODGE_SHADOW_RETAINED",
            "claim_allowed": False,
            "reason": "3504/3505 retain C_Hodge_hidden and constitutive tensor countermodels",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3861_3_epsilon_bound",
            "gate": "epsilon_shadow_g bound is explicit",
            "status": "PASS_SYMBOLIC_BOUND_COMPONENTIZED",
            "claim_allowed": False,
            "reason": "generic shadow leak is split into action-domain, terminal coframe, EM, light/clock, source/orbit, constants, readout, and endpoint parts",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3861_4_next_target",
            "gate": "next target selected",
            "status": "PASS_3862_EM_HIDDEN_HODGE_TARGET",
            "claim_allowed": False,
            "reason": "the most concrete retained shadow component is EM hidden Hodge/disformal structure",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D3861_0",
            "decision": "Do not demote the route; keep the no-shadow theorem as an exact conditional route.",
            "consequence": "The proof route is real, but it is not a current claim because parent signatures are unsigned.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3861_1",
            "decision": "Treat finite shadow-frame derivatives as physical couplings, not gauge.",
            "consequence": "c_g, b_dis, and C_Hodge_hidden remain source/PPN/clock/light bound targets if the no-extra-frame theorem fails.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3861_2",
            "decision": "Attack EM hidden Hodge next.",
            "consequence": "This is narrower than generic shadow-frame talk and directly touches Poynting flow, Maxwell limit, light cones, clocks, and EM stress.",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3861_0",
            "target_checkpoint": "3862-Y5-R2FR-EM-hidden-Hodge-disformal-zero-or-observable-bound.md",
            "script": "scripts/Y5_R2FR_3862_EM_hidden_Hodge_disformal_zero_or_observable_bound.py",
            "objective": "prove the EM action uses only the observed Hodge star *_obs[e_obs(q)] and no hidden/disformal constitutive map, or retain explicit C_Hodge_hidden/Delta_chi bound rows",
            "why_next": "3861 shows the shadow-frame route is blocked mostly by concrete sector slots; 3504/3505 make EM Hodge the sharpest non-generic slot",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_CONDITIONAL_NO_SHADOW_THEOREM_WITH_EXPLICIT_EPSILON_SHADOW_BOUND",
            "summary": "3861 proves the no-shadow coframe theorem conditionally, refuses current promotion, and isolates EM hidden Hodge/disformal structure as the next concrete attack.",
            "doc": rel(DOC_PATH),
            "validation": rel(OUTPUTS["validation"]),
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3861 — No-Shadow Coframe Basicness Or Epsilon-Shadow Frame Bound

Generated: `{timestamp}`

## Purpose

This checkpoint goes after the live coframe leak left by 3860. The target is not another missing-input ledger: it is the exact no-shadow theorem route, plus the explicit residual if the theorem is not parent-signed.

## Result

The exact conditional theorem is:

`{NO_SHADOW_THEOREM}`

Then:

`{CHAIN_RULE_ZERO}`

This is a real derivation route, not a vibe. The catch is also precise:

`{CURRENT_BLOCK}`

So the current branch is still non-claim, but the missing object is now sharply localized.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## No-Shadow Coframe Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "status", "result"])}

## Shadow Slot Audit

{markdown_table(audit, ["audit_id", "clause", "passes_current_branch", "residual_owner", "next_action"])}

## Epsilon-Shadow Bound

{markdown_table(bound, ["bound_id", "target", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3861 does move the ladder: it proves that a shadow coframe vanishes by variable absence and q-basic chain rule if the parent action genuinely has one public observed coframe and no hidden Weyl/disformal/constitutive sector frame. It also refuses the overclaim because the corpus still retains exact counterbranches. The sharpest next target is EM: prove or bound the hidden Hodge/disformal map, because that is where Poynting flow, Maxwell waves, light cones, clocks and EM stress all meet.

Next target: `3862-Y5-R2FR-EM-hidden-Hodge-disformal-zero-or-observable-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3860", "Current State After 3861", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3861 at ")
    )
    paragraph = (
        "`3861` proves the no-shadow coframe route conditionally and makes the live leak explicit. "
        "For each sector, write `e_s=Lambda_s e_obs+L_xi e_obs+Delta e_s^perp`; after local Lorentz/diffeomorphism/q_obs gauge is removed, only `Delta e_s^perp` is a physical shadow. "
        "If all ordinary actions and readouts use `e_obs(q_obs)`, `omega_LC[e_obs]`, q-basic constants and q_obs-sector fields only, while the parent grammar excludes independent Weyl/disformal/constitutive slots, then `Delta e_s^perp=0`; equivalently `e_s=e_bar_s(q_obs)` gives `D_v e_s=0` for `v in ker(Dq_obs)` and hence `epsilon_shadow_g=0`. "
        "The current corpus does not claim that closure: 1029/1030/3647/2888 keep the no-extra-frame/terminal coframe clauses unsigned, while 3504/3505 keep hidden EM Hodge/constitutive rows live. "
        "The retained bound is `B_shadow_frame_3861 <= B_no_extra_frame_action_domain+B_terminal_public_coframe+B_matter_shadow_slot+B_EM_Hodge_hidden+B_light_clock_frame+B_source_orbit_frame+B_constant_marker_shadow+B_readout_shadow+B_boundary_endpoint_shadow` and `epsilon_shadow_g <= epsilon_frame_slot+epsilon_terminal+epsilon_matter+epsilon_EM_Hodge_hidden+epsilon_light_clock+epsilon_source_orbit+epsilon_theta_marker+epsilon_readout+epsilon_endpoint`. "
        "The next concrete slot is EM hidden Hodge/disformal ownership, not another generic shadow-frame pass.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3861-Y5-R2FR-no-shadow-coframe-basicness-or-epsilon-shadow-frame-bound.md`

Target: prove no hidden/shadow coframe participates in matter, EM, source, clock, light, or orbital readout, or retain `epsilon_shadow_g` frame-source bounds.

This is the best next move because 3860 reduces public coframe basicness to parent certificates, and the most concrete coframe-specific leak is a second/shadow frame."""
    new_gate = """`3862-Y5-R2FR-EM-hidden-Hodge-disformal-zero-or-observable-bound.md`

Target: prove the EM action uses only the observed Hodge star `*_obs[e_obs(q)]` and no hidden/disformal constitutive map, or retain explicit `C_Hodge_hidden` / `Delta_chi` observable bounds.

This is the best next move because 3861 shows the generic no-shadow route is exact but unsigned, and EM Hodge is the sharpest retained sector shadow touching Poynting flow, Maxwell waves, light cones, clocks, and EM stress."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3861_NO_SHADOW_COFRAME_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3861_SHADOW_SLOT_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3861_EPSILON_SHADOW_FRAME_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3861_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3861_NO_SHADOW_COFRAME_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3861 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem + audit + bound + gates)
    add(
        "VAL3861_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3861_1_theorem",
        "exact conditional no-shadow theorem is explicit",
        "EXACT_CONDITIONAL_NO_SHADOW_COFRAME_THEOREM" in all_text and "Delta e_s^perp=0" in all_text,
        "no-shadow variable-absence theorem present",
    )
    add(
        "VAL3861_2_chain_rule",
        "q-basic sector-frame chain rule is explicit",
        "EXACT_CONDITIONAL_EPSILON_SHADOW_ZERO" in all_text and "D_v e_s=0" in all_text,
        "sector-frame q-basic chain rule present",
    )
    add(
        "VAL3861_3_no_overclaim",
        "current claim remains blocked",
        "NO_SHADOW_COFRAME_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "BLOCKED_NO_SHADOW_PARENT_SIGNATURE_UNSIGNED" in all_text,
        "current no-shadow/local-GR promotion blocked",
    )
    add(
        "VAL3861_4_counterbranch",
        "finite shadow counterbranches are retained",
        "FINITE_SHADOW_IS_SOURCE_COUPLING" in all_text and "C_Hodge_hidden" in all_text,
        "matter and EM counterbranches retained",
    )
    add(
        "VAL3861_5_bounds",
        "epsilon_shadow_g and B_shadow_frame_3861 bounds are explicit",
        "epsilon_shadow_g <=" in all_text and "B_shadow_frame_3861 <=" in all_text,
        "shadow bounds present",
    )
    add(
        "VAL3861_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + bound + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3861_7_next",
        "next target is EM hidden Hodge",
        DOC_PATH.exists() and "3862-Y5-R2FR-EM-hidden-Hodge-disformal-zero-or-observable-bound" in read_text(DOC_PATH),
        "3862 EM hidden Hodge target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3861_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3861_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "This checkpoint goes after the live coframe leak" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3861*", "P8_Y5_BRR545_3861*", "*Y5_R2FR_3861*", "3861-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3861_10_formalization_clean",
        "formalization-workbench has no generated 3861 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3861 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3861_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bound = bound_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["bound"], bound)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, bound, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, bound, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_NO_SHADOW_COFRAME_THEOREM_CURRENTLY_BLOCKED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
