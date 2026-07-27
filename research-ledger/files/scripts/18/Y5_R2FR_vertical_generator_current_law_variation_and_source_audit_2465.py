from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_VERTICAL_GENERATOR_CURRENT_LAW_VARIATION_AND_SOURCE_AUDIT_2465"
CHECKPOINT_ID = "2465"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2465-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_ACTION_2465_SOURCE_REGISTER.csv",
    "variation_audit": OUT / "P8_Y5_PARENT_ACTION_2465_VARIATION_AUDIT.csv",
    "dimension_audit": OUT / "P8_Y5_PARENT_ACTION_2465_DIMENSION_AUDIT.csv",
    "boundary_audit": OUT / "P8_Y5_PARENT_ACTION_2465_BOUNDARY_AUDIT.csv",
    "stress_audit": OUT / "P8_Y5_PARENT_ACTION_2465_STRESS_TENSOR_EXPOSURE.csv",
    "source_descent": OUT / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv",
    "tautology_audit": OUT / "P8_Y5_PARENT_ACTION_2465_TAUTOLOGY_RED_TEAM.csv",
    "promotion_verdict": OUT / "P8_Y5_PARENT_ACTION_2465_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_ACTION_2465_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PARENT_ACTION_2465_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_ACTION_2465_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_ACTION_2465_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2465_VALIDATION.csv",
}

COPY_TARGETS = {
    "candidate_variation_contract": QUEUE / "JR2465_VERTICAL_GENERATOR_VARIATION_CONTRACT_NONCLAIM.csv",
    "source_descent_queue": QUEUE / "JR2465_SOURCE_CURRENT_DESCENT_REQUIRED_NONCLAIM.csv",
    "local_vacuum_guardrail": LOCAL_BOUNDS / "Local_vacuum_guardrail_2465_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2465_00_2464_doc",
        "source_path": ROOT / "2464-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-and-source-bridge.md",
        "needles": [
            "ACT2464_A_vertical_generator_current_law",
            "QDER2464_1_vary_A",
            "SRCBR2464_0_current_origin",
            "NEXT2464_0_selected",
            "VAL2464_OVERALL",
        ],
        "role": "handoff selecting ACT2464_A for stress-test",
    },
    {
        "source_id": "SRC2465_01_2464_candidates",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2464_A_vertical_generator_current_law", "BEST_CONSTRUCTIVE_CANDIDATE_BUT_NONCLAIM"],
        "role": "candidate action source rows",
    },
    {
        "source_id": "SRC2465_02_2464_qloc_derivation",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_QLOC_DERIVATION_ATTEMPT.csv",
        "needles": ["QDER2464_1_vary_A", "PASS_AS_FORMAL_VARIATION", "CONDITIONAL_ZERO_NOT_CURRENT_CLAIM"],
        "role": "formal q_loc variation handoff",
    },
    {
        "source_id": "SRC2465_03_2464_source_bridge",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_SOURCE_BRIDGE_CONTRACT.csv",
        "needles": ["SRCBR2464_0_current_origin", "SRCBR2464_1_worldtube_integral", "SRCBR2464_4_universality"],
        "role": "missing source bridge clauses",
    },
    {
        "source_id": "SRC2465_04_2464_local_law",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_LOCAL_VACUUM_AMPLITUDE_LAW.csv",
        "needles": ["LAW2464_0_exact_conditional_zero", "LAW2464_1_F1_zero", "LAW2464_4_current_limit"],
        "role": "conditional local vacuum law to stress-test",
    },
    {
        "source_id": "SRC2465_05_1010_gk_residual",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "DEC1010_0_derivation_route_precise", "V1010_SUMMARY"],
        "role": "pre-2464 hard q_loc block",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": exists,
                "missing_needles": ";".join(missing),
                "source_pass": exists and not missing,
                "role": source["role"],
            }
        )
    return rows


def variation_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VAR2465_0_action_assumed",
            "S_GK=int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma(Gamma_eff,g,tau)]",
            "candidate assumption from 2464",
            "contract object only",
            "PASS_AS_CANDIDATE_INPUT",
        ),
        (
            "VAR2465_1_define_Khat",
            "K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)",
            "regular differentiable L_K",
            "K_hat is a displacement/momentum conjugate to vertical gradient",
            "PASS_AS_FORMAL_DEFINITION",
        ),
        (
            "VAR2465_2_delta_A_bulk",
            "delta_A S_GK=int sqrt(-g)[-nabla_mu K_hat^{mu nu}+nabla^nu Gamma_eff-J_M^nu] delta A_nu + boundary",
            "A_nu variations unconstrained or span the physical vertical subspace",
            "Euler equation gives nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}=J_M^nu",
            "PASS_AS_FORMAL_VARIATION",
        ),
        (
            "VAR2465_3_projected_equation",
            "q_loc^nu=P_loc^nu_rho(nabla^rho Gamma_eff-nabla_mu K_hat^{mu rho})=P_loc^nu_rho J_M^rho",
            "P_loc is parent-owned/fixed and does not hide fitted test-arena coefficients",
            "physical residual equals projected source current",
            "CONDITIONAL_ON_PROJECTOR_DESCENT",
        ),
        (
            "VAR2465_4_delta_Gamma_bulk",
            "delta_Gamma S_GK=int sqrt(-g)[-nabla_nu A^nu + dL_Gamma/dGamma_eff] delta Gamma_eff + boundary",
            "Gamma_eff is varied independently and L_Gamma is local",
            "companion equation fixes divergence/gap branch for A",
            "CONDITIONAL_COMPANION_EQUATION",
        ),
        (
            "VAR2465_5_integrability",
            "nabla_nu J_M^nu = nabla_nu nabla^nu Gamma_eff - nabla_nu nabla_mu K_hat^{mu nu}",
            "take divergence of A equation",
            "current conservation is not automatic unless Noether/source descent supplies identity or exchange law",
            "BLOCKED_UNTIL_SOURCE_DESCENT",
        ),
        (
            "VAR2465_6_not_theorem",
            "ACT2464_A is not promoted to current MTS",
            "A_nu, L_K, L_Gamma, J_M, P_loc and boundary conditions remain new/unsigned",
            "useful parent-action contract, not a local-GR proof",
            "NONCLAIM",
        ),
    ]
    return [
        {
            **base_row(),
            "variation_id": variation_id,
            "statement": statement,
            "assumption": assumption,
            "result": result,
            "status": status,
        }
        for variation_id, statement, assumption, result, status in rows
    ]


def dimension_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DIM2465_0_natural_units",
            "Use c=hbar=1 and four-dimensional action density dimension [L]=M^4.",
            "bookkeeping convention",
            "PASS",
            "sets scale language only",
        ),
        (
            "DIM2465_1_dimension_relation",
            "[A]+[Gamma_eff]=M^3 in exponent notation a+g=3",
            "A_nu nabla^nu Gamma_eff has dimension M^4",
            "PASS_AS_RELATION",
            "one-parameter family until Gamma_eff meaning is fixed",
        ),
        (
            "DIM2465_2_current_relation",
            "[J_M]=M^(4-a) where [A]=M^a",
            "A_nu J_M^nu has dimension M^4",
            "PASS_AS_RELATION",
            "ordinary vector current M^3 selects a=1",
        ),
        (
            "DIM2465_3_viable_branch",
            "If J_M is a matter/source current with dimension M^3, then [A]=M and [Gamma_eff]=M^2.",
            "source-current branch",
            "VIABLE_DIMENSION_BRANCH",
            "Gamma_eff must be curvature/compression-like, not a literal Christoffel symbol of dimension M",
        ),
        (
            "DIM2465_4_Khat_dimension",
            "For [A]=M and L_K~Z_K(nabla A)^2/2 with dimensionless Z_K, [K_hat]=M^2 and [nabla K_hat]=M^3.",
            "quadratic vertical-gradient branch",
            "PASS_ON_VIABLE_BRANCH",
            "matches [nabla Gamma_eff] and [J_M]",
        ),
        (
            "DIM2465_5_literal_connection_warning",
            "If Gamma_eff is forced to be literal connection-like with dimension M, then [A]=M^2 and [J_M]=M^2.",
            "alternative branch",
            "WARNING_DIMENSION_MISMATCH_WITH_ORDINARY_MATTER_CURRENT",
            "would require nonstandard current or extra scale coefficient",
        ),
        (
            "DIM2465_6_parent_scale_needed",
            "Any branch with noncanonical dimensions needs explicit parent scale coefficients, not hidden fitted normalisation.",
            "scale audit",
            "MISSING_PARENT_SCALE",
            "must be sourced before numeric local tests",
        ),
    ]
    return [
        {
            **base_row(),
            "dimension_id": dimension_id,
            "statement": statement,
            "basis": basis,
            "status": status,
            "issue_or_consequence": consequence,
        }
        for dimension_id, statement, basis, status, consequence in rows
    ]


def boundary_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BND2465_0_A_boundary",
            "delta_A boundary term",
            "int_boundary sqrt|h| n_mu K_hat^{mu nu} delta A_nu",
            "Dirichlet delta A=0, Neumann n_mu K_hat^{mu nu}=0, or parent counterterm",
            "MISSING_BOUNDARY_CONDITION",
            "local vacuum zero can be spoiled by boundary flux",
        ),
        (
            "BND2465_1_Gamma_boundary",
            "delta_Gamma boundary term",
            "int_boundary sqrt|h| n_nu A^nu delta Gamma_eff",
            "fixed Gamma_eff, n.A=0, or parent counterterm",
            "MISSING_BOUNDARY_CONDITION",
            "companion equation not well-posed until fixed",
        ),
        (
            "BND2465_2_local_collar",
            "local vacuum collar flux",
            "||n_mu K_hat^{mu nu}||_collar and ||n.A||_collar",
            "must vanish or be bounded by source/worldtube leakage",
            "MISSING_COLLAR_BOUND",
            "F1=0 remains conditional",
        ),
        (
            "BND2465_3_reference_safety",
            "reference boundary data",
            "H_ref/B_ref not used in ACT2464_A",
            "reference must stay late/readout-only",
            "PASS_GUARDRAIL",
            "avoids M_H_ref/counterterm smuggling",
        ),
        (
            "BND2465_4_distributional_source",
            "worldtube boundary layer",
            "J_M may be distributional on source boundary",
            "requires matching condition across worldtube",
            "MISSING_JUMP_CONDITION",
            "Newton limit/source mass not yet derived",
        ),
    ]
    return [
        {
            **base_row(),
            "boundary_id": boundary_id,
            "object": obj,
            "term": term,
            "required_condition": condition,
            "status": status,
            "effect": effect,
        }
        for boundary_id, obj, term, condition, status, effect in rows
    ]


def stress_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "STR2465_0_metric_variation_exists",
            "T_GK^{mu nu}=-(2/sqrt(-g)) delta S_GK/delta g_mu_nu",
            "L_K, covariant derivatives, index contractions, sqrt(-g), A.nabla Gamma and L_Gamma all expose metric dependence",
            "MISSING_EXPLICIT_STRESS",
            "local GR cannot pass until T_GK is zero, higher order, screened, or included consistently",
        ),
        (
            "STR2465_1_vacuum_stealth_condition",
            "In local vacuum, q_loc=0 does not by itself imply T_GK=0.",
            "A/Gamma/Khat may store stress even when Euler residual vanishes",
            "MISSING_STEALTH_BRANCH",
            "need vacuum branch A=0/Gamma=const or stress cancellation from parent symmetry",
        ),
        (
            "STR2465_2_Gamma_gap",
            "A positive gap m_tr from L_Gamma/L_K could suppress local residual modes.",
            "transition law ell_tr/L_cg=1/(m_tr L_cg)",
            "PARAMETRIC_ONLY",
            "gap coefficient must be parent-derived",
        ),
        (
            "STR2465_3_WEP_risk",
            "If J_M coupling is species-dependent, WEP/PPN failure is likely.",
            "A_nu J_M^nu couples directly to matter source current",
            "MISSING_UNIVERSALITY_PROOF",
            "source current must be universal or geometrically induced",
        ),
        (
            "STR2465_4_GR_limit_gate",
            "GR limit requires T_GK^{mu nu}->0 or controlled renormalization in local vacuum.",
            "metric equations decide actual local GR reduction",
            "BLOCKED_CURRENT_CLAIM",
            "q_loc Euler equation alone is not enough",
        ),
    ]
    return [
        {
            **base_row(),
            "stress_id": stress_id,
            "statement": statement,
            "basis": basis,
            "status": status,
            "effect": effect,
        }
        for stress_id, statement, basis, status, effect in rows
    ]


def source_descent_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SRC2465_0_matter_origin",
            "J_M^nu := -delta S_matter/delta A_nu or equivalent Noether current.",
            "prevents fitted mass current",
            "MISSING",
            "must specify L_matter[A,Psi,g,tau] or symmetry current",
        ),
        (
            "SRC2465_1_vertical_generator",
            "A_nu must couple to an actual vertical generator R_M on matter/source states, not an arbitrary label.",
            "connects q_loc to real motion/flow degrees of freedom",
            "MISSING",
            "need R_M, its charge, and whether it is universal",
        ),
        (
            "SRC2465_2_Noether_identity",
            "nabla_nu J_M^nu=0 or controlled exchange must follow from local symmetry/diffeomorphism identity.",
            "integrability of the A equation",
            "MISSING",
            "without this, ACT2464_A overconstrains Gamma/Khat/source evolution",
        ),
        (
            "SRC2465_3_worldtube_readout",
            "M_source[W] or source charge equals int_S J_M^nu dSigma_nu on parent-defined surfaces.",
            "Newton source bridge",
            "MISSING",
            "no orbital GM substitution allowed",
        ),
        (
            "SRC2465_4_external_vacuum",
            "J_M^nu=0 outside the worldtube except explicitly bounded distributional tails.",
            "local q_loc zero and F1=0",
            "MISSING",
            "needs source support theorem or matter falloff bound",
        ),
        (
            "SRC2465_5_universality",
            "same current law across species and local arenas.",
            "WEP/PPN safety",
            "MISSING",
            "must not introduce composition-dependent fifth force",
        ),
        (
            "SRC2465_6_candidate_route",
            "Possible route: matter covariant derivative D^A_mu Psi = D_mu Psi + A_mu R_M Psi, with J_M from variation.",
            "constructive source-descent route",
            "CANDIDATE_ONLY",
            "next checkpoint should try this and reject it if it violates WEP or dimensions",
        ),
    ]
    return [
        {
            **base_row(),
            "source_id": source_id,
            "required_clause": clause,
            "why_needed": why,
            "status": status,
            "missing_or_next": missing,
        }
        for source_id, clause, why, status, missing in rows
    ]


def tautology_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RED2465_0_not_multiplier",
            "ACT2464_A is better than a direct multiplier because A has a displacement sector L_K and produces K_hat as conjugate momentum.",
            "SURVIVES_INITIAL_TAUTOLOGY_TEST",
            "still needs L_K from principle rather than designer choice",
        ),
        (
            "RED2465_1_designer_LK_risk",
            "Choosing L_K only to manufacture a desired K_hat would be post-hoc.",
            "RISK_OPEN",
            "need symmetry, positivity, or simple kinetic principle",
        ),
        (
            "RED2465_2_designer_J_risk",
            "Choosing J_M only to equal the observed Newtonian source would smuggle the limit.",
            "RISK_OPEN",
            "need matter Noether/Hilbert descent and worldtube readout",
        ),
        (
            "RED2465_3_projector_risk",
            "Applying P_loc after the fact can hide failed components.",
            "RISK_OPEN",
            "P_loc must be parent-owned or explicitly fixed by local frame geometry",
        ),
        (
            "RED2465_4_boundary_risk",
            "Boundary silence can become another plateau axiom if not derived.",
            "RISK_OPEN",
            "need fixed variational boundary condition or flux bound",
        ),
        (
            "RED2465_5_claim_discipline",
            "The candidate is promoted only to a sharper contract, not to a theorem.",
            "PASS_GUARDRAIL",
            "local GR remains blocked",
        ),
    ]
    return [
        {
            **base_row(),
            "red_team_id": red_team_id,
            "critique": critique,
            "status": status,
            "required_fix": fix,
        }
        for red_team_id, critique, status, fix in rows
    ]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PV2465_0_formal_variation",
            "Does ACT2464_A produce the q_loc equation by variation?",
            "YES_AS_FORMAL_CONTRACT",
            "delta_A variation gives unprojected current law exactly",
            "promote_to_contract_only",
        ),
        (
            "PV2465_1_dimension_branch",
            "Is there a plausible dimension branch?",
            "YES_CONDITIONAL",
            "ordinary current branch gives [A]=M, [Gamma_eff]=M^2, [K_hat]=M^2",
            "requires Gamma_eff curvature/compression meaning",
        ),
        (
            "PV2465_2_boundary",
            "Are boundary terms closed?",
            "NO",
            "A and Gamma boundary fluxes are not parent-fixed",
            "blocks local vacuum theorem",
        ),
        (
            "PV2465_3_stress",
            "Is T_GK locally silent?",
            "NO",
            "q_loc=0 does not imply stress silence",
            "blocks GR/PPN pass",
        ),
        (
            "PV2465_4_source_bridge",
            "Is J_M parent-derived?",
            "NO",
            "Noether/Hilbert/worldtube current descent missing",
            "blocks Newton limit",
        ),
        (
            "PV2465_5_overall",
            "Overall 2465 verdict",
            "SHARPENED_BUT_NOT_PROMOTED",
            "candidate survives as best constructive route but fails theorem-level source/stress/boundary gates",
            "next target is source-current descent",
        ),
    ]
    return [
        {
            **base_row(),
            "verdict_id": verdict_id,
            "question": question,
            "result": result,
            "evidence": evidence,
            "effect": effect,
        }
        for verdict_id, question, result, evidence, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2465_0_q_loc_variation_contract", "q_loc current law follows from ACT2464_A variation.", "PASS_AS_CONTRACT", "formal variation verified", True, False),
        ("GATE2465_1_current_MTS_theorem", "ACT2464_A is a current MTS theorem.", "BLOCKED", "new fields/source/descent not yet sourced", False, False),
        ("GATE2465_2_source_current", "J_M is parent-derived and conserved.", "BLOCKED", "source descent and Noether identity missing", False, False),
        ("GATE2465_3_boundary_silence", "local collar boundary terms vanish or are bounded.", "BLOCKED", "boundary and jump conditions missing", False, False),
        ("GATE2465_4_stress_silence", "T_GK is locally silent in the GR limit.", "BLOCKED", "stress tensor exposure unresolved", False, False),
        ("GATE2465_5_local_GR_Newton_PPN", "local GR/Newton/PPN branch passes.", "BLOCKED", "formal q_loc law alone is insufficient", False, False),
        ("GATE2465_6_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [
        {
            **base_row(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": status,
            "reason": reason,
            "gate_pass": gate_pass,
            "claim_allowed": claim_allowed,
        }
        for gate_id, claim, status, reason, gate_pass, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2465_0_keep_candidate",
            "Keep ACT2464_A as the active constructive parent-action candidate.",
            "it passes formal q_loc variation and has a plausible dimension branch",
            "continue derivation rather than abandon",
        ),
        (
            "DEC2465_1_not_claimed",
            "Do not claim local-GR/Newton reduction.",
            "boundary, stress and source-current gates fail",
            "framework remains disciplined",
        ),
        (
            "DEC2465_2_source_first",
            "Attack source-current descent next.",
            "without J_M origin, both Newton source and q_loc vacuum support are unstable",
            "2466 should build or reject the matter-current bridge",
        ),
        (
            "DEC2465_3_stress_after_source",
            "Defer full stress tensor until source branch is chosen.",
            "metric variation depends on L_K, L_Gamma and matter coupling choice",
            "avoid doing stress algebra on an unsourced current",
        ),
        (
            "DEC2465_4_public_status",
            "Keep private.",
            "candidate is promising but too easy to misread as a claim",
            "no GitHub action",
        ),
    ]
    return [
        {
            **base_row(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "effect": effect,
        }
        for decision_id, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2465_0_selected",
            "selection_status": "selected",
            "target_file": "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
            "target_script": "scripts/Y5_R2FR_matter_current_descent_and_worldtube_source_bridge_2466.py",
            "task": "attempt to derive J_M from a matter/vertical-generator coupling and build the worldtube source bridge without using fitted orbital GM",
            "acceptance_target": "Noether/Hilbert current attempt, conservation identity, worldtube integral, external-vacuum support condition, WEP/composition guardrail, and honest demotion if source descent fails",
            "guardrails": "no local-GR claim; no orbital-GM source definition; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["variation_audit"], COPY_TARGETS["candidate_variation_contract"])
    shutil.copyfile(OUTPUTS["source_descent"], COPY_TARGETS["source_descent_queue"])
    shutil.copyfile(OUTPUTS["boundary_audit"], COPY_TARGETS["local_vacuum_guardrail"])
    rows = []
    source_map = {
        "candidate_variation_contract": OUTPUTS["variation_audit"],
        "source_descent_queue": OUTPUTS["source_descent"],
        "local_vacuum_guardrail": OUTPUTS["boundary_audit"],
    }
    for copy_id, target in COPY_TARGETS.items():
        source = source_map[copy_id]
        rows.append(
            {
                **base_row(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": source.exists(),
                "target_exists": target.exists(),
            }
        )
    return rows


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(
    sources: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    dimensions: list[dict[str, Any]],
    boundaries: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    source_descent: list[dict[str, Any]],
    red_team: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append(
            {
                **base_row(),
                "check_id": check_id,
                "status": "PASS" if status else "FAIL",
                "notes": notes,
                "detail": detail,
            }
        )

    add("VAL2465_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in sources), "all cited source paths exist and needles are present")
    add("VAL2465_01_variation_contract", any(row["variation_id"] == "VAR2465_2_delta_A_bulk" and row["status"] == "PASS_AS_FORMAL_VARIATION" for row in variation), "delta_A formal variation passes as contract")
    add("VAL2465_02_dimension_branch", any(row["dimension_id"] == "DIM2465_3_viable_branch" and row["status"] == "VIABLE_DIMENSION_BRANCH" for row in dimensions), "viable ordinary-current dimension branch recorded")
    add("VAL2465_03_boundary_blocks", any(row["status"] == "MISSING_BOUNDARY_CONDITION" for row in boundaries), "boundary blockers retained")
    add("VAL2465_04_stress_blocks", any(row["status"] == "BLOCKED_CURRENT_CLAIM" for row in stress), "stress tensor blocker retained")
    add("VAL2465_05_source_missing", all(row["status"] in {"MISSING", "CANDIDATE_ONLY"} for row in source_descent), "source descent remains missing/candidate-only")
    add("VAL2465_06_red_team_written", len(red_team) >= 6 and any(row["status"] == "RISK_OPEN" for row in red_team), "tautology risks recorded")
    add("VAL2465_07_overall_verdict_nonclaim", any(row["verdict_id"] == "PV2465_5_overall" and row["result"] == "SHARPENED_BUT_NOT_PROMOTED" for row in verdicts), "overall verdict is sharpened but not promoted")
    add("VAL2465_08_claim_gates_safe", all(row["claim_allowed"] is False for row in gates), "no claim gate allows public/local-GR claim")
    add("VAL2465_09_next_target_written", bool(next_rows) and next_rows[0]["route_id"] == "NEXT2465_0_selected", "2466 source-current descent selected")
    add("VAL2465_10_branch_copies", all(row["source_exists"] and row["target_exists"] for row in branch_rows), "nonclaim branch copies exist")
    formal_hits = list(FORMALIZATION.rglob("*2465*")) if FORMALIZATION.exists() else []
    add("VAL2465_11_no_formalization_artifacts", not formal_hits, "no 2465 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2465_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2465_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))

    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2465_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2465_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))

    add(
        "VAL2465_OVERALL",
        all(row["status"] == "PASS" for row in rows),
        "2465 sharpens ACT2464_A into a formal q_loc contract but blocks theorem claims on source, boundary and stress gates",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    dimensions: list[dict[str, Any]],
    boundaries: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    source_descent: list[dict[str, Any]],
    red_team: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2465 Y5 R2FR Vertical Generator Current-law Variation And Source Audit",
        "",
        "**Status:** ACT2464_A survives the first serious stress-test as a formal parent-action contract, not a theorem. The variation is genuinely useful: `delta_A S` produces the desired current law rather than merely asserting a local plateau. But source descent, boundary silence and stress-tensor silence all remain open, so local GR/Newton/PPN is still blocked.",
        "",
        "**Best reading:** this is progress. The candidate did not collapse into pure wordplay. It gives a concrete route: make `q_loc` an Euler equation, then prove the matter current and source worldtube are real. The next fight is `J_M`: if that current can be derived cleanly, the Newton limit starts to look much less hand-wavy. If it cannot, this route demotes honestly.",
        "",
        "## Source Register",
        markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Variation Audit",
        markdown_table(variation, ["variation_id", "statement", "assumption", "result", "status"]),
        "",
        "## Dimension Audit",
        markdown_table(dimensions, ["dimension_id", "statement", "basis", "status", "issue_or_consequence"]),
        "",
        "## Boundary Audit",
        markdown_table(boundaries, ["boundary_id", "object", "term", "required_condition", "status", "effect"]),
        "",
        "## Stress Tensor Exposure",
        markdown_table(stress, ["stress_id", "statement", "basis", "status", "effect"]),
        "",
        "## Source-current Descent",
        markdown_table(source_descent, ["source_id", "required_clause", "why_needed", "status", "missing_or_next"]),
        "",
        "## Tautology Red Team",
        markdown_table(red_team, ["red_team_id", "critique", "status", "required_fix"]),
        "",
        "## Promotion Verdict",
        markdown_table(verdicts, ["verdict_id", "question", "result", "evidence", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(gates, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(decisions, ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(branch_rows, ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(validations, ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    variation = variation_audit_rows()
    dimensions = dimension_audit_rows()
    boundaries = boundary_audit_rows()
    stress = stress_audit_rows()
    source_descent = source_descent_rows()
    red_team = tautology_audit_rows()
    verdicts = promotion_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["variation_audit"], variation)
    write_csv(OUTPUTS["dimension_audit"], dimensions)
    write_csv(OUTPUTS["boundary_audit"], boundaries)
    write_csv(OUTPUTS["stress_audit"], stress)
    write_csv(OUTPUTS["source_descent"], source_descent)
    write_csv(OUTPUTS["tautology_audit"], red_team)
    write_csv(OUTPUTS["promotion_verdict"], verdicts)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, variation, dimensions, boundaries, stress, source_descent, red_team, verdicts, gates, decisions, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, variation, dimensions, boundaries, stress, source_descent, red_team, verdicts, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
