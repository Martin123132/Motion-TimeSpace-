from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3008"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence-or-explicit-residual-split-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3008_SOURCE_REGISTER.csv",
    "action_audit": RESIDUALS / "P8_Y5_R2FR_3008_QLOC_ACTION_EXISTENCE_AUDIT.csv",
    "metric_theorem": RESIDUALS / "P8_Y5_R2FR_3008_METRIC_RESPONSE_WARD_THEOREM.csv",
    "candidate_scorecard": RESIDUALS / "P8_Y5_R2FR_3008_CANDIDATE_ROUTE_SCORECARD.csv",
    "residual_split": RESIDUALS / "P8_Y5_R2FR_3008_EXPLICIT_QLOC_RESIDUAL_SPLIT.csv",
    "coupling_guard": RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3008_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3008_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3008_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3008_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3008_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "metric_theorem_copy": PARENT_ACTION / "Gamma_Khat_q_loc_metric_response_Ward_theorem_3008_CONDITIONAL_NOT_SIGNED.csv",
    "action_audit_copy": PARENT_ACTION / "Gamma_Khat_q_loc_action_existence_audit_3008_NOT_SIGNED.csv",
    "residual_split_copy": LOCAL_BOUNDS / "q_loc_explicit_residual_split_3008_NONCLAIM.csv",
    "coupling_guard_copy": LOCAL_BOUNDS / "coupling_guard_rows_3008_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3008_GK_METRIC_RESPONSE_MATCH_AND_COUPLING_DESCENT_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3008_00_3007_next",
        RESIDUALS / "P8_Y5_R2FR_3007_NEXT_TARGET.csv",
        ["NEXT3007_0_3008", "Gamma-Khat-q_loc-action-existence"],
        "3007 selects Gamma/Khat/q_loc action existence or residual split as 3008.",
    ),
    (
        "SRC3008_01_3007_doc",
        ROOT / "3007-Y5-R2FR-minimal-parent-action-sector-grammar-or-sector-variation-ledger-under-AX1090.md",
        ["The coupling issue is now front and centre", "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence"],
        "3007 identifies coupling and the Gamma/Khat/q_loc block as the next hard strike.",
    ),
    (
        "SRC3008_02_3007_grammar",
        RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
        ["G3007_4_Gamma_Khat_q_loc", "G3007_10_verdict"],
        "3007 grammar defines the GK/q_loc sector and forbids hiding it inside EH.",
    ),
    (
        "SRC3008_03_GK513_contract",
        RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        ["GK513_0_action_existence", "GK513_5_boundary_no_flux"],
        "GK513 gives the exact action-existence, Helmholtz, Euler, double-zero, projector and boundary requirements.",
    ),
    (
        "SRC3008_04_GO516_candidates",
        RESIDUALS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner"],
        "GO516 lists the candidate owner actions and fallback residual branch.",
    ),
    (
        "SRC3008_05_GK514_candidates",
        RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
        ["GK514_A_metric_response_scalar_density", "GK514_D_residual_branch"],
        "GK514 makes metric response the cleanest candidate and residual branch the fallback.",
    ),
    (
        "SRC3008_06_GK514_decision",
        RESIDUALS / "P8_GK_STRESS_ACTION_DECISION.csv",
        ["D514_0", "D514_3"],
        "GK514 decision says the metric-response action is the best candidate but current MTS is not matched.",
    ),
    (
        "SRC3008_07_GK514_gates",
        RESIDUALS / "P8_GK_STRESS_ACTION_GATE_TESTS.csv",
        ["G514_0_candidate_constructed", "G514_4_residual_fallback"],
        "GK514 gates already fail current q_loc zero and keep residual fallback.",
    ),
    (
        "SRC3008_08_GK514_route",
        RESIDUALS / "P8_GK_STRESS_ACTION_ROUTE_UPDATE.csv",
        ["RU514_0", "RU514_2"],
        "GK514 route update points to real symbol matching and residual explicitness.",
    ),
    (
        "SRC3008_09_2207_metric_variation",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2207_GAMMA_EFF_METRIC_VARIATION_ATTEMPT.csv",
        ["GMV2207_0_response_doublet_setup", "GMV2207_3_verdict"],
        "2207 shows the response-doublet metric variation can formally provide double-zero, but not current K_hat matching.",
    ),
    (
        "SRC3008_10_2140_gamma_variation",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2140_GAMMAG_VARIATION_IDENTITIES.csv",
        ["GVAR2140_0_action_piece", "GVAR2140_7_verdict"],
        "2140 proves Gamma value-zero is not enough; metric functional variation/residuals remain.",
    ),
    (
        "SRC3008_11_response_contract",
        RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        ["RD516_0_doublet_variables", "RD516_6_boundary_no_flux"],
        "Response doublet contract gives the best double-zero route and its hard source/boundary blockers.",
    ),
    (
        "SRC3008_12_response_variation",
        RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        ["AV517_0_define_doublet", "AV517_5_positive_theorem"],
        "Response variation shows formal double-zero and positive theorem remain conditional.",
    ),
    (
        "SRC3008_13_symbol_map",
        RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        ["Gamma_eff", "K_hat^{mu nu}", "q_loc^nu"],
        "Symbol map says Gamma/Khat/q_loc are residual/action-owner targets, not fundamental fields.",
    ),
    (
        "SRC3008_14_first_variation_gates",
        RESIDUALS / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        ["FV512_2_Gamma_Khat_q", "FV512_5_mass_projector"],
        "First-variation gates mark q_loc and source normalization as local-GR blockers.",
    ),
    (
        "SRC3008_15_matter_descent",
        RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv",
        ["PRE2611_0_q_map", "PRE2611_8_verdict"],
        "Matter descent audit keeps q-only matter/source descent unsigned.",
    ),
    (
        "SRC3008_16_source_prefactors",
        RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        ["SP2612_0_absent_slot", "SP2612_6_readout_worldtube"],
        "Source-prefactor classification lists hidden coupling countermodels that must be forbidden or bounded.",
    ),
    (
        "SRC3008_17_coupling_vector",
        RESIDUALS / "P8_Y5_COUPLING_VECTOR_2660_COUPLING_RESIDUAL_VECTOR_SCHEMA.csv",
        ["CV2660_0_c_g", "CV2660_7_total_policy"],
        "Coupling vector schema supplies local arena residual channels for hidden coupling coefficients.",
    ),
    (
        "SRC3008_18_1009_sector",
        RESIDUALS / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
        ["PCS1009_4_Gamma_Khat_extra", "PCS1009_9_total_parent_contract"],
        "1009 sector contract places Gamma/Khat/q_loc as a hard extra sector.",
    ),
]

source_rows = []
for source_id, path, required, role in SOURCE_SPECS:
    source_rows.append(
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(required),
                "anchors_found": anchors(path, required),
                "missing_anchors": missing_anchors(path, required),
                "role": role,
            }
        )
    )


action_audit_rows = [
    base(
        {
            "audit_id": "GKA3008_0_action_existence",
            "required_clause": "There exists a local diffeomorphism-invariant S_GK whose stress/current owns Gamma_eff and K_hat.",
            "derivation_attempt": "take T_GK^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu}; require T_GK=-2/sqrt(-g) delta S_GK/delta g_mu_nu up to convention",
            "current_verdict": "CONDITIONAL_ROUTE_ONLY",
            "why_not_promoted": "current corpus does not identify existing Gamma_eff/K_hat with a single scalar-density metric response",
            "source_anchors": "GK513_0_action_existence;GK514_A_metric_response_scalar_density;GMV2207_3_verdict",
        }
    ),
    base(
        {
            "audit_id": "GKA3008_1_Helmholtz_integrability",
            "required_clause": "The claimed T_GK satisfies symmetric second-variation/Helmholtz conditions.",
            "derivation_attempt": "metric-response scalar action would satisfy Helmholtz automatically if Gamma_eff is the actual action density",
            "current_verdict": "NOT_CHECKED_FOR_CURRENT_SYMBOLS",
            "why_not_promoted": "K_hat is not proven equal to the functional metric response of Gamma_eff",
            "source_anchors": "GK513_1_integrability;G514_2_current_MTS_match",
        }
    ),
    base(
        {
            "audit_id": "GKA3008_2_Ward_Euler_closure",
            "required_clause": "Diffeomorphism Ward identity turns q_loc into Euler/source/boundary residuals.",
            "derivation_attempt": "if T_GK is action-derived, nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + boundary/improvement terms",
            "current_verdict": "EXACT_CONDITIONAL_THEOREM",
            "why_not_promoted": "the E_A field list and boundary/improvement terms are not supplied by current MTS",
            "source_anchors": "GK513_2_Euler_closure;GVAR2140_6_bianchi_constraint",
        }
    ),
    base(
        {
            "audit_id": "GKA3008_3_double_zero",
            "required_clause": "T_GK(Phi0)=0 and first variation of T_GK vanishes at the local fixed point.",
            "derivation_attempt": "response-doublet normal form Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) gives F_1=0 at Z=0 if no odd/source/boundary linear term exists",
            "current_verdict": "FORMAL_DOUBLE_ZERO_NOT_MTS_PROMOTION",
            "why_not_promoted": "zero odd source, component coverage, positive operator and physical q_loc/PPN map are not derived",
            "source_anchors": "GK513_3_double_zero;RD516_4_zero_odd_source;AV517_3_double_zero",
        }
    ),
    base(
        {
            "audit_id": "GKA3008_4_projector_ownership",
            "required_clause": "P_loc is parent-owned and cannot hide/tune force components.",
            "derivation_attempt": "q_loc=P_loc nabla_mu T_GK^{mu nu}; projector terms must commute with local limit or be residualized",
            "current_verdict": "OPEN_RESIDUAL",
            "why_not_promoted": "P_loc/Pi_M projector variation and commutator stress remain unsigned",
            "source_anchors": "GK513_4_projector_ownership;FV512_5_mass_projector",
        }
    ),
    base(
        {
            "audit_id": "GKA3008_5_boundary_no_flux",
            "required_clause": "S_GK boundary/symplectic terms carry no extra mass/force flux through local linking surfaces.",
            "derivation_attempt": "topological/exact route can silence bulk but requires fixed boundary class and theta_GK/Q_GK no-flux",
            "current_verdict": "OPEN_RESIDUAL",
            "why_not_promoted": "boundary flux and charge-unit convention remain open",
            "source_anchors": "GK513_5_boundary_no_flux;GMV2207_2_topological_boundary_setup;RD516_6_boundary_no_flux",
        }
    ),
    base(
        {
            "audit_id": "GKA3008_6_coupling_guard",
            "required_clause": "Matter/source coupling has no hidden direct source prefactor that reintroduces q_loc as a physical force.",
            "derivation_attempt": "q-only matter descent would remove direct X/source/worldtube slots by object language",
            "current_verdict": "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED",
            "why_not_promoted": "source-only weights, hidden frames, alpha/mass vertices and readout-worldtube masks remain live countermodels",
            "source_anchors": "PRE2611_8_verdict;SP2612_2_relative_species;CV2660_7_total_policy",
        }
    ),
    base(
        {
            "audit_id": "GKA3008_7_verdict",
            "required_clause": "Current MTS promotes q_loc -> 0 from a parent action.",
            "derivation_attempt": "metric-response Ward theorem is mathematically good as a future parent-action route",
            "current_verdict": "QLOC_ZERO_NOT_CLAIMED_RESIDUAL_SPLIT_REQUIRED",
            "why_not_promoted": "conditional theorem lacks current symbol match, source descent, projector ownership and boundary no-flux",
            "source_anchors": "all rows above",
        }
    ),
]


metric_theorem_rows = [
    base(
        {
            "theorem_id": "MRW3008_0_define_metric_response_stress",
            "statement": "Define T_GK^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu}. If this is the Hilbert stress of one diffeomorphism-invariant S_GK, then Gamma_eff and K_hat are not independent bookkeeping objects.",
            "mathematical_form": "T_GK^{mu nu} = -2/sqrt(-g) delta S_GK/delta g_mu_nu = Gamma_eff g^{mu nu}-K_hat^{mu nu}",
            "status": "CONDITIONAL_EXACT_DEFINITION",
            "promotion_blocker": "current K_hat not matched to this metric response",
        }
    ),
    base(
        {
            "theorem_id": "MRW3008_1_diffeomorphism_Ward_identity",
            "statement": "Diffeomorphism invariance gives the Ward identity for the same fields that build Gamma_eff and K_hat.",
            "mathematical_form": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + nabla_mu B_GK^{mu nu}",
            "status": "CONDITIONAL_EXACT_IDENTITY",
            "promotion_blocker": "E_A list and B_GK boundary/improvement terms are not current-owned",
        }
    ),
    base(
        {
            "theorem_id": "MRW3008_2_q_loc_as_projected_Ward_residual",
            "statement": "With the metric-response identity, the physical q_loc expression is the projected Ward residual.",
            "mathematical_form": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})=P_loc(sum_A E_A nabla^nu Phi^A+nabla_mu B_GK^{mu nu})",
            "status": "CONDITIONAL_DERIVATION_ROUTE",
            "promotion_blocker": "P_loc parent ownership and boundary silence are missing",
        }
    ),
    base(
        {
            "theorem_id": "MRW3008_3_on_shell_local_zero",
            "statement": "q_loc vanishes on compact local vacuum only if Euler equations hold, source terms vanish, boundary flux is silent and P_loc is fixed.",
            "mathematical_form": "E_A=0, B_GK=0, delta P_loc=0 => q_loc^nu=0",
            "status": "GOOD_CONDITIONAL_THEOREM_NOT_CURRENT_MTS",
            "promotion_blocker": "conditions are not jointly signed",
        }
    ),
    base(
        {
            "theorem_id": "MRW3008_4_double_zero_amplitude_law",
            "statement": "If T_GK has a stationary local kernel, then F_1=0 and the leading local leakage is quadratic.",
            "mathematical_form": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 => ||q_loc|| <= O(||delta Phi|| ||nabla delta Phi||)+boundary/source/projector residuals",
            "status": "CONDITIONAL_AMPLITUDE_LAW",
            "promotion_blocker": "no source/odd term and physical component map are not derived",
        }
    ),
    base(
        {
            "theorem_id": "MRW3008_5_failed_shortcut",
            "statement": "A Lagrange multiplier action A_nu q_loc^nu is not accepted as a proof by itself.",
            "mathematical_form": "S_lambda=int sqrt(-g) A_nu P_loc(nabla^nu Gamma_eff-div K_hat) imposes q_loc=0 but adds multiplier stress/current unless A_nu is itself fixed/silent by parent rules",
            "status": "REJECTED_CLOSURE_AXIOM",
            "promotion_blocker": "it smuggles the desired equation instead of deriving the physical sector",
        }
    ),
    base(
        {
            "theorem_id": "MRW3008_6_current_status",
            "statement": "3008 constructs the correct theorem contract but does not prove current MTS satisfies it.",
            "mathematical_form": "metric-response Ward route kept; current q_loc remains explicit residual",
            "status": "THEOREM_CONTRACT_ONLY",
            "promotion_blocker": "symbol match, coupling descent and boundary/projector clauses remain missing",
        }
    ),
]


candidate_scorecard_rows = [
    base(
        {
            "candidate_id": "CAND3008_0_metric_response_scalar",
            "route": "S_GK=-int sqrt(-g) Gamma_eff with K_hat as metric response",
            "best_use": "cleanest derivation of q_loc as Ward residual",
            "passes": "diffeomorphism identity and Helmholtz if the identity is actually true",
            "fails_or_open": "current Gamma_eff/K_hat definitions not matched",
            "selected_status": "PRIMARY_CONDITIONAL_ROUTE_NOT_PROMOTED",
            "next_input_needed": "explicit K_hat = metric response of Gamma_eff row",
        }
    ),
    base(
        {
            "candidate_id": "CAND3008_1_response_doublet",
            "route": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "best_use": "derives F_1=0/double-zero if exchange symmetry and zero odd source hold",
            "passes": "formal local amplitude law",
            "fails_or_open": "component map, source-normalization rows and physical PPN/q_loc matching not derived",
            "selected_status": "BEST_DOUBLE_ZERO_SUBROUTE_NOT_PROMOTED",
            "next_input_needed": "zero odd source and Z=q_loc/PPN component map",
        }
    ),
    base(
        {
            "candidate_id": "CAND3008_2_positive_auxiliary",
            "route": "positive auxiliary energy density with mass gap",
            "best_use": "can force local Z=0 from an energy identity",
            "passes": "plausible minimization mechanism",
            "fails_or_open": "source-free collar, boundary no-flux, and K_hat identity unsigned",
            "selected_status": "SECONDARY_CONDITIONAL_ROUTE",
            "next_input_needed": "operator positivity plus J_A=B_A=0",
        }
    ),
    base(
        {
            "candidate_id": "CAND3008_3_topological_exact",
            "route": "Gamma/Khat as exact or topological boundary/improvement density",
            "best_use": "silences bulk without propagating new fields",
            "passes": "bulk residual can be zero under fixed class",
            "fails_or_open": "boundary flux and charge-unit convention remain live",
            "selected_status": "BOUNDARY_RISK_ROUTE",
            "next_input_needed": "theta_GK/Q_GK no-flux and fixed reference class",
        }
    ),
    base(
        {
            "candidate_id": "CAND3008_4_lagrange_multiplier",
            "route": "A_nu q_loc^nu constraint action",
            "best_use": "formal equation imposition",
            "passes": "sets q_loc=0 algebraically if accepted",
            "fails_or_open": "not accepted because it adds multiplier stress and smuggles the closure axiom",
            "selected_status": "REJECTED_SHORTCUT",
            "next_input_needed": "do not use unless A_nu is parent-silent and sourced",
        }
    ),
    base(
        {
            "candidate_id": "CAND3008_5_residual_split",
            "route": "no S_GK accepted; carry q_loc as explicit residual vector",
            "best_use": "keeps theory honest and testable while derivation remains incomplete",
            "passes": "prevents EH-only hiding and no-cancellation cheating",
            "fails_or_open": "requires real local bound/projection inputs before scoring",
            "selected_status": "SELECTED_CURRENT_FALLBACK",
            "next_input_needed": "numeric/source-backed local residual bounds and coupling projections",
        }
    ),
]


residual_split_rows = [
    base(
        {
            "residual_id": "QRES3008_0_metric_response_mismatch",
            "symbol": "epsilon_GK_metric_response_abs",
            "mathematical_form": "||P_loc nabla_mu[(Gamma_eff g^{mu nu}-K_hat^{mu nu})-T_metric^{mu nu}[Gamma_eff]]||",
            "units": "force_per_mass_or_acceleration_equivalent_after_projection",
            "arena_links": "PPN;R10;orbital;clock",
            "required_inputs": "explicit Gamma_eff functional; computed K_metric; current K_hat definition; P_loc",
            "current_status": "MISSING_SYMBOL_MATCH",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2207_GAMMA_EFF_METRIC_VARIATION_ATTEMPT.csv"),
        }
    ),
    base(
        {
            "residual_id": "QRES3008_1_Euler_residual",
            "symbol": "epsilon_GK_Euler_abs",
            "mathematical_form": "||P_loc sum_A E_A nabla^nu Phi^A||",
            "units": "projected_force_density",
            "arena_links": "PPN;local_GR;source_normalization",
            "required_inputs": "field list Phi^A; Euler equations E_A; local vacuum/source support clause",
            "current_status": "MISSING_EULER_FIELD_LIST",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"),
        }
    ),
    base(
        {
            "residual_id": "QRES3008_2_double_zero_F1",
            "symbol": "epsilon_GK_F1_abs",
            "mathematical_form": "||P_loc nabla_mu[(partial_A T_GK^{mu nu})_0 delta Phi^A]||",
            "units": "projected_force_density_linear_order",
            "arena_links": "PPN;R10;clock;orbital",
            "required_inputs": "local fixed point Phi0; first derivative tensor; no odd/source linear term",
            "current_status": "MISSING_ZERO_ODD_SOURCE_AND_COMPONENT_MAP",
            "source_path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
        }
    ),
    base(
        {
            "residual_id": "QRES3008_3_projector_commutator",
            "symbol": "epsilon_GK_projector_abs",
            "mathematical_form": "||[P_loc,nabla_mu]T_GK^{mu nu} + (delta P_loc) nabla_mu T_GK^{mu nu}||",
            "units": "projected_force_density",
            "arena_links": "PPN_alpha_i;R11;orbital",
            "required_inputs": "parent P_loc definition; delta P_loc; commutator/source-bound row",
            "current_status": "MISSING_PROJECTOR_OWNERSHIP",
            "source_path": str(RESIDUALS / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv"),
        }
    ),
    base(
        {
            "residual_id": "QRES3008_4_boundary_flux",
            "symbol": "epsilon_GK_boundary_flux_abs",
            "mathematical_form": "|int_partialU Delta(theta_GK,Q_GK,tau)| / M_ref_like",
            "units": "dimensionless_after_denominator_or_force_flux_before_denominator",
            "arena_links": "R10;PPN;orbital;source_mass",
            "required_inputs": "theta_GK; Q_GK; fixed boundary/reference class; denominator convention",
            "current_status": "MISSING_BOUNDARY_NO_FLUX",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"),
        }
    ),
    base(
        {
            "residual_id": "QRES3008_5_hidden_matter_coupling",
            "symbol": "epsilon_GK_matter_source_coupling_abs",
            "mathematical_form": "abs(delta_w_A, b_dis, dln_alpha_EM/dX, dln_m_A/dX, q_nonH_domain_tail, source_worldtube_mask)",
            "units": "arena_specific_coupling_vector",
            "arena_links": "WEP;clocks;EM;PPN;R10;orbital",
            "required_inputs": "q-only matter descent theorem or coupling coefficient bounds",
            "current_status": "MISSING_COUPLING_DESCENT",
            "source_path": str(RESIDUALS / "P8_Y5_COUPLING_VECTOR_2660_COUPLING_RESIDUAL_VECTOR_SCHEMA.csv"),
        }
    ),
    base(
        {
            "residual_id": "QRES3008_6_tau_surface",
            "symbol": "epsilon_GK_tau_surface_abs",
            "mathematical_form": "mismatch(tau_source,tau_charge,tau_clock,tau_readout,S_local)",
            "units": "arena_projection_factor",
            "arena_links": "all_local_arenas",
            "required_inputs": "tau/surface lock and arena projection pack",
            "current_status": "MISSING_TAU_SURFACE_LOCK",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv"),
        }
    ),
    base(
        {
            "residual_id": "QRES3008_7_total_no_cancellation",
            "symbol": "epsilon_q_loc_total_abs_envelope",
            "mathematical_form": "sum_i abs(epsilon_i) over QRES3008_0..6",
            "units": "arena_specific_abs_envelope",
            "arena_links": "all_local_arenas",
            "required_inputs": "all residual components theorem-zero or source-backed numeric",
            "current_status": "NOT_SCOREABLE_COMPONENTS_MISSING",
            "source_path": "this checkpoint",
        }
    ),
]


coupling_guard_rows = [
    base(
        {
            "guard_id": "CG3008_0_q_only_geometry",
            "guard_clause": "observed metric/coframe descends through q(Phi)",
            "forbidden_leak": "T^{mu nu} Lie_v g_obs direct local source",
            "current_status": "NOT_PARENT_SIGNED",
            "if_fails": "q_loc zero does not imply matter/source silence",
            "source_anchors": "PRE2611_1_observed_geometry",
        }
    ),
    base(
        {
            "guard_id": "CG3008_1_no_direct_X_vertex",
            "guard_clause": "ordinary matter action has no direct X/Gamma/memory/source vertex",
            "forbidden_leak": "alpha_EM(X), m_A(X), q_A X_mu J_A^mu, source-only weights",
            "current_status": "POLICY_NOT_PARENT_THEOREM",
            "if_fails": "clock, WEP and fifth-force residuals return",
            "source_anchors": "PRE2611_4_no_shadow_prefactor;SP2612_5_alpha_mass_vertex",
        }
    ),
    base(
        {
            "guard_id": "CG3008_2_no_relative_source_weight",
            "guard_clause": "no relative species/source prefactor w_A=w_*(1+epsilon_A)",
            "forbidden_leak": "composition-dependent active source",
            "current_status": "LIVE_COUNTERMODEL",
            "if_fails": "WEP/source-normalization residual must be bounded",
            "source_anchors": "SP2612_2_relative_species;CV2660_4_P_WEP_source_weight",
        }
    ),
    base(
        {
            "guard_id": "CG3008_3_no_hidden_frame",
            "guard_clause": "no hidden conformal/disformal matter frame outside declared parent grammar",
            "forbidden_leak": "g_A=A_A(X)^2 g_obs plus disformal terms",
            "current_status": "LIVE_UNLESS_DECLARED_EXTENSION",
            "if_fails": "PPN/clock/orbital residual vector stays live",
            "source_anchors": "SP2612_4_hidden_frame;CV2660_1_b_dis",
        }
    ),
    base(
        {
            "guard_id": "CG3008_4_worldtube_before_readout",
            "guard_clause": "worldtube/source support is parent-owned before readout",
            "forbidden_leak": "post-readout source mask w(W_source,Pi_M,readout,domain)",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_fails": "active source can change without visible matter equation change",
            "source_anchors": "PRE2611_5_worldtube_support;SP2612_6_readout_worldtube",
        }
    ),
    base(
        {
            "guard_id": "CG3008_5_Hilbert_source_owner",
            "guard_clause": "ordinary active source is one Hilbert/coframe current with one global kappa",
            "forbidden_leak": "non-Hilbert/domain-tail source current",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "if_fails": "Newton source mass cannot be read from the Hamiltonian charge",
            "source_anchors": "PRE2611_7_hilbert_source_owner;CV2660_5_q_nonH",
        }
    ),
    base(
        {
            "guard_id": "CG3008_6_guard_verdict",
            "guard_clause": "all coupling guard clauses must pass in the same parent branch",
            "forbidden_leak": "apparent q_loc/local GR proof with hidden matter/source coupling",
            "current_status": "COUPLING_GUARD_NOT_CLOSED",
            "if_fails": "local GR/Newton remains nonclaim even if GK metric-response route is later matched",
            "source_anchors": "PRE2611_8_verdict;CV2660_7_total_policy",
        }
    ),
]


gate_rows = [
    base(
        {
            "gate_id": "GATE3008_0_sources",
            "gate": "all 3008 source anchors exist",
            "gate_status": "PASS" if all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows) else "FAIL",
            "condition_passed": all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows),
            "promotion_allowed_now": False,
            "reason": "sources support the audit/theorem contract only",
        }
    ),
    base(
        {
            "gate_id": "GATE3008_1_metric_response_theorem",
            "gate": "metric-response Ward theorem constructed",
            "gate_status": "PASS_AS_CONDITIONAL_THEOREM",
            "condition_passed": True,
            "promotion_allowed_now": False,
            "reason": "conditional theorem is good, but current MTS symbol match is missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3008_2_current_symbol_match",
            "gate": "current Gamma_eff/K_hat satisfy metric-response identity",
            "gate_status": "FAIL_CLOSED",
            "condition_passed": False,
            "promotion_allowed_now": False,
            "reason": "K_hat is not computed as the functional metric response of Gamma_eff in current corpus",
        }
    ),
    base(
        {
            "gate_id": "GATE3008_3_double_zero",
            "gate": "F_1=0/local double-zero derived for physical components",
            "gate_status": "CONDITIONAL_ONLY",
            "condition_passed": False,
            "promotion_allowed_now": False,
            "reason": "response-doublet route gives formal double-zero but not component/source closure",
        }
    ),
    base(
        {
            "gate_id": "GATE3008_4_coupling_guard",
            "gate": "hidden matter/source couplings excluded",
            "gate_status": "FAIL_CLOSED",
            "condition_passed": False,
            "promotion_allowed_now": False,
            "reason": "source prefactors and hidden frames remain live countermodels",
        }
    ),
    base(
        {
            "gate_id": "GATE3008_5_residual_split",
            "gate": "q_loc residual split staged",
            "gate_status": "PASS_NONCLAIM",
            "condition_passed": True,
            "promotion_allowed_now": False,
            "reason": "residual rows keep the branch testable without declaring q_loc zero",
        }
    ),
    base(
        {
            "gate_id": "GATE3008_6_local_claims",
            "gate": "local GR/Newton/PPN/WEP/R10 claim allowed",
            "gate_status": "FAIL_CLOSED",
            "condition_passed": False,
            "promotion_allowed_now": False,
            "reason": "q_loc action owner, source coupling and denominator/source bridge remain unproved",
        }
    ),
]


decision_rows = [
    base(
        {
            "decision_id": "DEC3008_0_keep_metric_response_route",
            "decision": "Keep the metric-response Ward route as the best derivation target.",
            "rationale": "It is not a plateau axiom: if T_GK=Gamma g-Khat comes from one diffeomorphism-invariant action, q_loc is the projected Ward residual.",
            "next_effect": "future work can try to match real Gamma_eff/K_hat definitions instead of guessing a force law.",
        }
    ),
    base(
        {
            "decision_id": "DEC3008_1_no_q_loc_promotion",
            "decision": "Do not claim q_loc -> 0 for current MTS.",
            "rationale": "The current corpus lacks the actual metric-response identity, source-free Euler field list, projector ownership and boundary silence.",
            "next_effect": "q_loc remains an explicit residual split, not a hidden local-GR proof.",
        }
    ),
    base(
        {
            "decision_id": "DEC3008_2_reject_multiplier_shortcut",
            "decision": "Reject a pure Lagrange-multiplier q_loc=0 action as proof.",
            "rationale": "It imposes the desired equation and introduces multiplier stress/current unless the multiplier sector is itself parent-silent.",
            "next_effect": "the route stays derivational rather than closure-by-notation.",
        }
    ),
    base(
        {
            "decision_id": "DEC3008_3_coupling_guard_is_mandatory",
            "decision": "Treat hidden matter/source coupling as a coequal blocker.",
            "rationale": "Even a successful GK action route would not give Newton/GR if matter/source prefactors, hidden frames or worldtube masks remain legal.",
            "next_effect": "next target combines real Gamma/Khat matching with matter-source coupling descent guard.",
        }
    ),
]


next_rows = [
    base(
        {
            "next_id": "NEXT3008_0_3009",
            "priority": "selected_primary",
            "target_doc": "3009-Y5-R2FR-Gamma-Khat-metric-response-symbol-match-and-coupling-descent-guard-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_Gamma_Khat_metric_response_symbol_match_and_coupling_descent_guard_under_AX1090_3009.py",
            "mission": "Try to match the actual current Gamma_eff and K_hat definitions to the metric-response identity while simultaneously auditing whether matter/source coupling descends q-only with no hidden source prefactor.",
            "success_condition": "either the real symbols satisfy K_hat=metric response of Gamma_eff and coupling guard clauses close, or both failures become explicit source-ready residual rows for local tests.",
            "fallback_if_fail": "move to numeric/source-backed local residual bound inputs for epsilon_q_loc_total_abs_envelope and the coupling residual vector.",
            "guardrails": "no q_loc zero claim from formal theorem alone; no Lagrange-multiplier closure trick; no hidden matter/source prefactor; no EH-only current import; no orbital-GM denominator; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
        }
    )
]


write_csv(OUTPUTS["sources"], source_rows)
write_csv(OUTPUTS["action_audit"], action_audit_rows)
write_csv(OUTPUTS["metric_theorem"], metric_theorem_rows)
write_csv(OUTPUTS["candidate_scorecard"], candidate_scorecard_rows)
write_csv(OUTPUTS["residual_split"], residual_split_rows)
write_csv(OUTPUTS["coupling_guard"], coupling_guard_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

shutil.copyfile(OUTPUTS["metric_theorem"], BRANCH_OUTPUTS["metric_theorem_copy"])
shutil.copyfile(OUTPUTS["action_audit"], BRANCH_OUTPUTS["action_audit_copy"])
shutil.copyfile(OUTPUTS["residual_split"], BRANCH_OUTPUTS["residual_split_copy"])
shutil.copyfile(OUTPUTS["coupling_guard"], BRANCH_OUTPUTS["coupling_guard_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = []
for copy_id, path in BRANCH_OUTPUTS.items():
    copy_rows = rows(path)
    claim_flags_present = any(
        boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) or boolish(row.get("score_ready")) or boolish(row.get("valid_prediction_row"))
        for row in copy_rows
    )
    branch_rows.append(
        base(
            {
                "copy_id": copy_id,
                "path": str(path),
                "path_exists": path.exists(),
                "row_count": len(copy_rows),
                "csv_parse_ok": csv_ok(path),
                "claim_flags_present": claim_flags_present,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv" or not path.exists():
            continue
        for row in rows(path):
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if boolish(row.get(key)):
                    return False
    return True


validation_rows = [
    base(
        {
            "validation_id": "VAL3008_00_sources_exist",
            "passed": all(boolish(row["path_exists"]) for row in source_rows),
            "detail": "every cited source path exists",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_01_source_anchors",
            "passed": all(boolish(row["anchors_found"]) for row in source_rows),
            "detail": "every source contains required anchors",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_02_metric_theorem_written",
            "passed": len(metric_theorem_rows) >= 7 and any(row["theorem_id"] == "MRW3008_2_q_loc_as_projected_Ward_residual" for row in metric_theorem_rows),
            "detail": "metric-response Ward theorem and q_loc projection are written",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_03_no_q_loc_promotion",
            "passed": any(row["audit_id"] == "GKA3008_7_verdict" and "NOT_CLAIMED" in row["current_verdict"] for row in action_audit_rows),
            "detail": "q_loc zero is not promoted",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_04_shortcut_rejected",
            "passed": any(row["theorem_id"] == "MRW3008_5_failed_shortcut" and "REJECTED" in row["status"] for row in metric_theorem_rows),
            "detail": "Lagrange-multiplier closure shortcut is rejected",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_05_residual_split_written",
            "passed": len(residual_split_rows) >= 8 and any(row["residual_id"] == "QRES3008_7_total_no_cancellation" for row in residual_split_rows),
            "detail": "explicit q_loc residual split and no-cancellation envelope are staged",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_06_coupling_guard_written",
            "passed": len(coupling_guard_rows) >= 7 and any(row["guard_id"] == "CG3008_6_guard_verdict" for row in coupling_guard_rows),
            "detail": "hidden matter/source coupling guard rows are staged",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_07_local_claims_blocked",
            "passed": any(row["gate_id"] == "GATE3008_6_local_claims" and not boolish(row["promotion_allowed_now"]) for row in gate_rows),
            "detail": "no local GR/Newton/PPN/WEP/R10 claim is allowed",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_08_next_target_selected",
            "passed": next_rows[0]["target_doc"].startswith("3009-Y5-R2FR-Gamma-Khat-metric-response-symbol-match"),
            "detail": "3009 selects real symbol match and coupling descent guard",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_09_branch_copies",
            "passed": all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) and not boolish(row["claim_flags_present"]) for row in branch_rows),
            "detail": "branch copies exist, parse, and carry no claim flags",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_10_csv_parse",
            "passed": all(csv_ok(path) for path in list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())),
            "detail": "all 3008 CSV outputs parse cleanly",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_11_paths_under_post_checkpoint",
            "passed": all(under(path, ROOT) for path in generated_paths),
            "detail": "all generated outputs are under post-checkpoint-work",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_12_formalization_untouched",
            "passed": not any(FORMALIZATION.rglob("*3008*")) if FORMALIZATION.exists() else True,
            "detail": "no targeted 3008 files exist under formalization-workbench",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3008_13_no_claim_flags",
            "passed": no_claim_flags(list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())),
            "detail": "all generated rows remain valid_for_claim=false and claim_allowed=false",
            "required": True,
        }
    ),
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    base(
        {
            "validation_id": "VAL3008_OVERALL",
            "passed": overall_pass,
            "detail": "3008 constructs the conditional metric-response Ward route for q_loc, rejects shortcut closure, and stages explicit residual/coupling guard rows without promoting local GR/Newton",
            "required": True,
        }
    )
)
write_csv(OUTPUTS["validation"], validation_rows)


doc = f"""# 3008 - Y5/R2FR Gamma-Khat q_loc Action Existence Or Explicit Residual Split Under AX1090

Status: `Y5_R2FR_3008_metric_response_Ward_route_constructed_current_q_loc_not_promoted_residual_split_staged_3009_next`

Generated: `{RUN_UTC}`

## Current Verdict

3008 gets a real derivation target on the table. If `T_GK^{{mu nu}} := Gamma_eff g^{{mu nu}} - K_hat^{{mu nu}}` is the Hilbert stress of one diffeomorphism-invariant `S_GK`, then

`q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})`

is not a magic force field. It is the projected Ward/Euler residual:

`q_loc^nu = P_loc(sum_A E_A nabla^nu Phi^A + boundary/improvement terms)`.

That is the proper derivation route. In compact local vacuum it vanishes only if the Euler equations hold, boundary flux is silent, the projector is parent-owned, and hidden matter/source couplings are absent.

So the good news: the theory now has a clean mathematical route for `q_loc -> 0` that is not a plateau axiom. The bad news, still honest: current MTS does not yet prove the actual `Gamma_eff` and `K_hat` definitions satisfy this metric-response identity, and it does not yet close the hidden coupling guard. So 3008 refuses the claim and stages explicit residual rows.

## Source Register

{md_table(source_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## q_loc Action-Existence Audit

{md_table(action_audit_rows, ["audit_id", "required_clause", "derivation_attempt", "current_verdict", "why_not_promoted"])}

## Metric-Response Ward Theorem

{md_table(metric_theorem_rows, ["theorem_id", "statement", "mathematical_form", "status", "promotion_blocker"])}

## Candidate Route Scorecard

{md_table(candidate_scorecard_rows, ["candidate_id", "route", "best_use", "passes", "fails_or_open", "selected_status"])}

## Explicit q_loc Residual Split

{md_table(residual_split_rows, ["residual_id", "symbol", "mathematical_form", "units", "arena_links", "current_status"])}

## Coupling Guard Rows

{md_table(coupling_guard_rows, ["guard_id", "guard_clause", "forbidden_leak", "current_status", "if_fails"])}

## Promotion Gates

{md_table(gate_rows, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "rationale", "next_effect"])}

## Next Target

{md_table(next_rows, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "path", "path_exists", "row_count", "csv_parse_ok", "claim_flags_present"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "detail", "required"])}

## Plain-English Takeaway

This is progress, and it is the good kind. We did not prove local GR, but we found the exact gate that would make the ugly local force object respectable. If `Gamma_eff g - K_hat` is a real metric-response stress tensor, `q_loc` becomes a Noether/Ward residual. Then local silence follows from equations of motion plus boundary/projector/coupling guards, not wishful thinking. That is the route worth trying.

The current gap is also sharper now: match the real symbols, then kill hidden coupling. If either fails, the theory can still be tested by explicit residual bounds, but it cannot claim the GR/Newton reduction yet.

## Forbidden Claims From 3008

- `q_loc^nu` is zero in current MTS.
- `Gamma_eff` and `K_hat` are already matched to a signed metric-response action.
- The response-doublet double-zero is physically component-complete.
- A Lagrange multiplier imposing `q_loc=0` is an acceptable derivation.
- Hidden matter/source couplings are excluded.
- `theta_GK`, `Q_tau^GK`, `H_tau`, `M_H_ref` or local GR/Newton/PPN/WEP/R10 are promoted.
"""

DOC.write_text(doc, encoding="utf-8")

if not overall_pass:
    failed = [row["validation_id"] for row in validation_rows if not boolish(row["passed"])]
    raise SystemExit(f"3008 validation failed: {failed}")

print(f"wrote {DOC}")
for key, path in OUTPUTS.items():
    print(f"{key}: {path}")
for key, path in BRANCH_OUTPUTS.items():
    print(f"{key}: {path}")
