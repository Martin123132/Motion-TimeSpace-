from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2555"
BRANCH_ID = "MTS_R2FR_VERTICAL_GENERATOR_CURRENT_LAW_VARIATION_AND_SOURCE_AUDIT_2555"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SCRIPTS = ROOT / "scripts"

DOC = ROOT / "2555-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2555_SOURCE_REGISTER.csv",
    "variation_audit": OUT / "P8_Y5_NO_SHADOW_2555_VARIATION_AUDIT.csv",
    "dimension_audit": OUT / "P8_Y5_NO_SHADOW_2555_DIMENSION_AUDIT.csv",
    "boundary_audit": OUT / "P8_Y5_NO_SHADOW_2555_BOUNDARY_AUDIT.csv",
    "stress_audit": OUT / "P8_Y5_NO_SHADOW_2555_STRESS_TENSOR_EXPOSURE.csv",
    "source_descent": OUT / "P8_Y5_NO_SHADOW_2555_SOURCE_CURRENT_DESCENT.csv",
    "tautology_audit": OUT / "P8_Y5_NO_SHADOW_2555_TAUTOLOGY_RED_TEAM.csv",
    "promotion_verdict": OUT / "P8_Y5_NO_SHADOW_2555_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2555_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2555_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2555_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2555_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2555_VALIDATION.csv",
}

COPY_TARGETS = {
    "candidate_variation_contract": QUEUE / "JR2555_VERTICAL_GENERATOR_VARIATION_CONTRACT_NONCLAIM.csv",
    "source_descent_queue": QUEUE / "JR2555_SOURCE_CURRENT_DESCENT_REQUIRED_NONCLAIM.csv",
    "local_vacuum_guardrail": LOCAL_BOUNDS / "Local_vacuum_guardrail_2555_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2555_00_2554_doc",
        "source_path": ROOT / "2554-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-and-source-bridge.md",
        "needles": ["ACT2554_A_vertical_generator_current_law", "QDER2554_1_vary_A", "SRCBR2554_0_current_origin", "NEXT2554_0_selected", "VAL2554_OVERALL"],
        "role": "active handoff selecting ACT2554_A for stress-test",
    },
    {
        "source_id": "SRC2555_01_2554_candidates",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2554_A_vertical_generator_current_law", "BEST_CONSTRUCTIVE_CANDIDATE_BUT_NONCLAIM"],
        "role": "candidate action source rows",
    },
    {
        "source_id": "SRC2555_02_2554_qloc_derivation",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_QLOC_DERIVATION_ATTEMPT.csv",
        "needles": ["QDER2554_1_vary_A", "PASS_AS_FORMAL_VARIATION", "CONDITIONAL_ZERO_NOT_CURRENT_CLAIM"],
        "role": "formal q_loc variation handoff",
    },
    {
        "source_id": "SRC2555_03_2554_source_bridge",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_SOURCE_BRIDGE_CONTRACT.csv",
        "needles": ["SRCBR2554_0_current_origin", "SRCBR2554_1_worldtube_integral", "SRCBR2554_4_universality"],
        "role": "missing source bridge clauses",
    },
    {
        "source_id": "SRC2555_04_2554_local_law",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_LOCAL_VACUUM_AMPLITUDE_LAW.csv",
        "needles": ["LAW2554_0_exact_conditional_zero", "LAW2554_1_F1_zero", "LAW2554_4_current_limit"],
        "role": "conditional local vacuum law to stress-test",
    },
    {
        "source_id": "SRC2555_05_1010_gk_residual",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "DEC1010_0_derivation_route_precise", "V1010_SUMMARY"],
        "role": "pre-2554 hard q_loc block",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "true" if value else "false"


def base_row(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
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


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def inside_root(path: Path) -> bool:
    resolved = path.resolve()
    root = ROOT.resolve()
    return resolved == root or root in resolved.parents


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def variation_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAR2555_0_action_assumed", "S_GK=int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma(Gamma_eff,g,tau)]", "candidate assumption from 2554", "contract object only", "PASS_AS_CANDIDATE_INPUT"),
        ("VAR2555_1_define_Khat", "K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)", "regular differentiable L_K", "K_hat is a displacement/momentum conjugate to vertical gradient", "PASS_AS_FORMAL_DEFINITION"),
        ("VAR2555_2_delta_A_bulk", "delta_A S_GK=int sqrt(-g)[-nabla_mu K_hat^{mu nu}+nabla^nu Gamma_eff-J_M^nu] delta A_nu + boundary", "A_nu variations unconstrained or span the physical vertical subspace", "Euler equation gives nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}=J_M^nu", "PASS_AS_FORMAL_VARIATION"),
        ("VAR2555_3_projected_equation", "q_loc^nu=P_loc^nu_rho(nabla^rho Gamma_eff-nabla_mu K_hat^{mu rho})=P_loc^nu_rho J_M^rho", "P_loc is parent-owned/fixed and does not hide fitted test-arena coefficients", "physical residual equals projected source current", "CONDITIONAL_ON_PROJECTOR_DESCENT"),
        ("VAR2555_4_delta_Gamma_bulk", "delta_Gamma S_GK=int sqrt(-g)[-nabla_nu A^nu + dL_Gamma/dGamma_eff] delta Gamma_eff + boundary", "Gamma_eff is varied independently and L_Gamma is local", "companion equation fixes divergence/gap branch for A", "CONDITIONAL_COMPANION_EQUATION"),
        ("VAR2555_5_integrability", "nabla_nu J_M^nu = nabla_nu nabla^nu Gamma_eff - nabla_nu nabla_mu K_hat^{mu nu}", "take divergence of A equation", "current conservation is not automatic unless Noether/source descent supplies identity or exchange law", "BLOCKED_UNTIL_SOURCE_DESCENT"),
        ("VAR2555_6_not_theorem", "ACT2554_A is not promoted to current MTS", "A_nu, L_K, L_Gamma, J_M, P_loc and boundary conditions remain new/unsigned", "useful parent-action contract, not a local-GR proof", "NONCLAIM"),
    ]
    return [{**base_row(), "variation_id": a, "statement": b, "assumption": c, "result": d, "status": e} for a, b, c, d, e in rows]


def dimension_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("DIM2555_0_natural_units", "Use c=hbar=1 and four-dimensional action density dimension [L]=M^4.", "bookkeeping convention", "PASS", "sets scale language only"),
        ("DIM2555_1_dimension_relation", "[A]+[Gamma_eff]=M^3 in exponent notation a+g=3", "A_nu nabla^nu Gamma_eff has dimension M^4", "PASS_AS_RELATION", "one-parameter family until Gamma_eff meaning is fixed"),
        ("DIM2555_2_current_relation", "[J_M]=M^(4-a) where [A]=M^a", "A_nu J_M^nu has dimension M^4", "PASS_AS_RELATION", "ordinary vector current M^3 selects a=1"),
        ("DIM2555_3_viable_branch", "If J_M is a matter/source current with dimension M^3, then [A]=M and [Gamma_eff]=M^2.", "source-current branch", "VIABLE_DIMENSION_BRANCH", "Gamma_eff must be curvature/compression-like, not a literal Christoffel symbol of dimension M"),
        ("DIM2555_4_Khat_dimension", "For [A]=M and L_K~Z_K(nabla A)^2/2 with dimensionless Z_K, [K_hat]=M^2 and [nabla K_hat]=M^3.", "quadratic vertical-gradient branch", "PASS_ON_VIABLE_BRANCH", "matches [nabla Gamma_eff] and [J_M]"),
        ("DIM2555_5_literal_connection_warning", "If Gamma_eff is forced to be literal connection-like with dimension M, then [A]=M^2 and [J_M]=M^2.", "alternative branch", "WARNING_DIMENSION_MISMATCH_WITH_ORDINARY_MATTER_CURRENT", "would require nonstandard current or extra scale coefficient"),
        ("DIM2555_6_parent_scale_needed", "Any branch with noncanonical dimensions needs explicit parent scale coefficients, not hidden fitted normalisation.", "scale audit", "MISSING_PARENT_SCALE", "must be sourced before numeric local tests"),
    ]
    return [{**base_row(), "dimension_id": a, "statement": b, "basis": c, "status": d, "issue_or_consequence": e} for a, b, c, d, e in rows]


def boundary_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND2555_0_A_boundary", "delta_A boundary term", "int_boundary sqrt|h| n_mu K_hat^{mu nu} delta A_nu", "Dirichlet delta A=0, Neumann n_mu K_hat^{mu nu}=0, or parent counterterm", "MISSING_BOUNDARY_CONDITION", "local vacuum zero can be spoiled by boundary flux"),
        ("BND2555_1_Gamma_boundary", "delta_Gamma boundary term", "int_boundary sqrt|h| n_nu A^nu delta Gamma_eff", "fixed Gamma_eff, n.A=0, or parent counterterm", "MISSING_BOUNDARY_CONDITION", "companion equation not well-posed until fixed"),
        ("BND2555_2_local_collar", "local vacuum collar flux", "||n_mu K_hat^{mu nu}||_collar and ||n.A||_collar", "must vanish or be bounded by source/worldtube leakage", "MISSING_COLLAR_BOUND", "F1=0 remains conditional"),
        ("BND2555_3_reference_safety", "reference boundary data", "H_ref/B_ref not used in ACT2554_A", "reference must stay late/readout-only", "PASS_GUARDRAIL", "avoids M_H_ref/counterterm smuggling"),
        ("BND2555_4_distributional_source", "worldtube boundary layer", "J_M may be distributional on source boundary", "requires matching condition across worldtube", "MISSING_JUMP_CONDITION", "Newton limit/source mass not yet derived"),
    ]
    return [{**base_row(), "boundary_id": a, "object": b, "term": c, "required_condition": d, "status": e, "effect": f} for a, b, c, d, e, f in rows]


def stress_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("STR2555_0_metric_variation_exists", "T_GK^{mu nu}=-(2/sqrt(-g)) delta S_GK/delta g_mu_nu", "L_K, covariant derivatives, index contractions, sqrt(-g), A.nabla Gamma and L_Gamma all expose metric dependence", "MISSING_EXPLICIT_STRESS", "local GR cannot pass until T_GK is zero, higher order, screened, or included consistently"),
        ("STR2555_1_vacuum_stealth_condition", "In local vacuum, q_loc=0 does not by itself imply T_GK=0.", "A/Gamma/Khat may store stress even when Euler residual vanishes", "MISSING_STEALTH_BRANCH", "need vacuum branch A=0/Gamma=const or stress cancellation from parent symmetry"),
        ("STR2555_2_Gamma_gap", "A positive gap m_tr from L_Gamma/L_K could suppress local residual modes.", "transition law ell_tr/L_cg=1/(m_tr L_cg)", "PARAMETRIC_ONLY", "gap coefficient must be parent-derived"),
        ("STR2555_3_WEP_risk", "If J_M coupling is species-dependent, WEP/PPN failure is likely.", "A_nu J_M^nu couples directly to matter source current", "MISSING_UNIVERSALITY_PROOF", "source current must be universal or geometrically induced"),
        ("STR2555_4_GR_limit_gate", "GR limit requires T_GK^{mu nu}->0 or controlled renormalization in local vacuum.", "metric equations decide actual local GR reduction", "BLOCKED_CURRENT_CLAIM", "q_loc Euler equation alone is not enough"),
    ]
    return [{**base_row(), "stress_id": a, "statement": b, "basis": c, "status": d, "effect": e} for a, b, c, d, e in rows]


def source_descent_rows() -> list[dict[str, Any]]:
    rows = [
        ("SRC2555_0_matter_origin", "J_M^nu := -delta S_matter/delta A_nu or equivalent Noether current.", "prevents fitted mass current", "MISSING", "must specify L_matter[A,Psi,g,tau] or symmetry current"),
        ("SRC2555_1_vertical_generator", "A_nu must couple to an actual vertical generator R_M on matter/source states, not an arbitrary label.", "connects q_loc to real motion/flow degrees of freedom", "MISSING", "need R_M, its charge, and whether it is universal"),
        ("SRC2555_2_Noether_identity", "nabla_nu J_M^nu=0 or controlled exchange must follow from local symmetry/diffeomorphism identity.", "integrability of the A equation", "MISSING", "without this, ACT2554_A overconstrains Gamma/Khat/source evolution"),
        ("SRC2555_3_worldtube_readout", "M_source[W] or source charge equals int_S J_M^nu dSigma_nu on parent-defined surfaces.", "Newton source bridge", "MISSING", "no orbital GM substitution allowed"),
        ("SRC2555_4_external_vacuum", "J_M^nu=0 outside the worldtube except explicitly bounded distributional tails.", "local q_loc zero and F1=0", "MISSING", "needs source support theorem or matter falloff bound"),
        ("SRC2555_5_universality", "same current law across species and local arenas.", "WEP/PPN safety", "MISSING", "must not introduce composition-dependent fifth force"),
        ("SRC2555_6_candidate_route", "Possible route: matter covariant derivative D^A_mu Psi = D_mu Psi + A_mu R_M Psi, with J_M from variation.", "constructive source-descent route", "CANDIDATE_ONLY", "next checkpoint should try this and reject it if it violates WEP or dimensions"),
    ]
    return [{**base_row(), "source_id": a, "required_clause": b, "why_needed": c, "status": d, "missing_or_next": e} for a, b, c, d, e in rows]


def tautology_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("RED2555_0_not_multiplier", "ACT2554_A is better than a direct multiplier because A has a displacement sector L_K and produces K_hat as conjugate momentum.", "SURVIVES_INITIAL_TAUTOLOGY_TEST", "still needs L_K from principle rather than designer choice"),
        ("RED2555_1_designer_LK_risk", "Choosing L_K only to manufacture a desired K_hat would be post-hoc.", "RISK_OPEN", "need symmetry, positivity, or simple kinetic principle"),
        ("RED2555_2_designer_J_risk", "Choosing J_M only to equal the observed Newtonian source would smuggle the limit.", "RISK_OPEN", "need matter Noether/Hilbert descent and worldtube readout"),
        ("RED2555_3_projector_risk", "Applying P_loc after the fact can hide failed components.", "RISK_OPEN", "P_loc must be parent-owned or explicitly fixed by local frame geometry"),
        ("RED2555_4_boundary_risk", "Boundary silence can become another plateau axiom if not derived.", "RISK_OPEN", "need fixed variational boundary condition or flux bound"),
        ("RED2555_5_claim_discipline", "The candidate is promoted only to a sharper contract, not to a theorem.", "PASS_GUARDRAIL", "local GR remains blocked"),
    ]
    return [{**base_row(), "red_team_id": a, "critique": b, "status": c, "required_fix": d} for a, b, c, d in rows]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2555_0_formal_variation", "Does ACT2554_A produce the q_loc equation by variation?", "YES_AS_FORMAL_CONTRACT", "delta_A variation gives unprojected current law exactly", "promote_to_contract_only"),
        ("PV2555_1_dimension_branch", "Is there a plausible dimension branch?", "YES_CONDITIONAL", "ordinary current branch gives [A]=M, [Gamma_eff]=M^2, [K_hat]=M^2", "requires Gamma_eff curvature/compression meaning"),
        ("PV2555_2_boundary", "Are boundary terms closed?", "NO", "A and Gamma boundary fluxes are not parent-fixed", "blocks local vacuum theorem"),
        ("PV2555_3_stress", "Is T_GK locally silent?", "NO", "q_loc=0 does not imply stress silence", "blocks GR/PPN pass"),
        ("PV2555_4_source_bridge", "Is J_M parent-derived?", "NO", "Noether/Hilbert/worldtube current descent missing", "blocks Newton limit"),
        ("PV2555_5_overall", "Overall 2555 verdict", "SHARPENED_BUT_NOT_PROMOTED", "candidate survives as best constructive route but fails theorem-level source/stress/boundary gates", "next target is source-current descent"),
    ]
    return [{**base_row(), "verdict_id": a, "question": b, "result": c, "evidence": d, "effect": e} for a, b, c, d, e in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2555_0_q_loc_variation_contract", "q_loc current law follows from ACT2554_A variation.", "PASS_AS_CONTRACT", "formal variation verified", "true", "false"),
        ("GATE2555_1_current_MTS_theorem", "ACT2554_A is a current MTS theorem.", "BLOCKED", "new fields/source/descent not yet sourced", "false", "false"),
        ("GATE2555_2_source_current", "J_M is parent-derived and conserved.", "BLOCKED", "source descent and Noether identity missing", "false", "false"),
        ("GATE2555_3_boundary_silence", "local collar boundary terms vanish or are bounded.", "BLOCKED", "boundary and jump conditions missing", "false", "false"),
        ("GATE2555_4_stress_silence", "T_GK is locally silent in the GR limit.", "BLOCKED", "stress tensor exposure unresolved", "false", "false"),
        ("GATE2555_5_local_GR_Newton_PPN", "local GR/Newton/PPN branch passes.", "BLOCKED", "formal q_loc law alone is insufficient", "false", "false"),
        ("GATE2555_6_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [{**base_row(), "gate_id": a, "claim": b, "gate_status": c, "reason": d, "gate_pass": e, "claim_allowed": f} for a, b, c, d, e, f in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2555_0_keep_candidate", "Keep ACT2554_A as the active constructive parent-action candidate.", "it passes formal q_loc variation and has a plausible dimension branch", "continue derivation rather than abandon"),
        ("DEC2555_1_not_claimed", "Do not claim local-GR/Newton reduction.", "boundary, stress and source-current gates fail", "framework remains disciplined"),
        ("DEC2555_2_source_first", "Attack source-current descent next.", "without J_M origin, both Newton source and q_loc vacuum support are unstable", "2556 should build or reject the matter-current bridge"),
        ("DEC2555_3_stress_after_source", "Defer full stress tensor until source branch is chosen.", "metric variation depends on L_K, L_Gamma and matter coupling choice", "avoid doing stress algebra on an unsourced current"),
        ("DEC2555_4_public_status", "Keep private.", "candidate is promising but too easy to misread as a claim", "no GitHub action"),
    ]
    return [{**base_row(), "decision_id": a, "decision": b, "reason": c, "effect": d} for a, b, c, d in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2555_0_selected",
            "selection_status": "selected",
            "target_file": "2556-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
            "target_script": "scripts/Y5_R2FR_matter_current_descent_and_worldtube_source_bridge_2556.py",
            "task": "attempt to derive J_M from a matter/vertical-generator coupling and build the worldtube source bridge without using fitted orbital GM",
            "acceptance_target": "Noether/Hilbert current attempt, conservation identity, worldtube integral, external-vacuum support condition, WEP/composition guardrail, and honest demotion if source descent fails",
            "guardrails": "no local-GR claim; no orbital-GM source definition; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    source_map = {
        "candidate_variation_contract": OUTPUTS["variation_audit"],
        "source_descent_queue": OUTPUTS["source_descent"],
        "local_vacuum_guardrail": OUTPUTS["boundary_audit"],
    }
    for copy_id, target in COPY_TARGETS.items():
        shutil.copyfile(source_map[copy_id], target)
    return [
        {
            **base_row(),
            "copy_id": copy_id,
            "source_path": str(source_map[copy_id]),
            "target_path": str(target),
            "source_exists": truth(source_map[copy_id].exists()),
            "target_exists": truth(target.exists()),
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    artifact_markers = (
        "2555-Y5",
        "_2555_",
        "_2555.",
        "JR2555",
        "P8_Y5_NO_SHADOW_2555",
        "P8_Y5_BRR545_2555",
        "Y5_R2FR_vertical_generator_current_law_variation_and_source_audit_2555",
    )
    return [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in artifact_markers)
    ]


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

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add("VAL2555_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present", ";".join(row["source_id"] for row in sources if row["source_pass"] != "true"))
    add("VAL2555_01_variation_contract", any(row["variation_id"] == "VAR2555_2_delta_A_bulk" and row["status"] == "PASS_AS_FORMAL_VARIATION" for row in variation), "delta_A formal variation passes as contract")
    add("VAL2555_02_dimension_branch", any(row["dimension_id"] == "DIM2555_3_viable_branch" and row["status"] == "VIABLE_DIMENSION_BRANCH" for row in dimensions), "viable ordinary-current dimension branch recorded")
    add("VAL2555_03_boundary_blocks", any(row["status"] == "MISSING_BOUNDARY_CONDITION" for row in boundaries), "boundary blockers retained")
    add("VAL2555_04_stress_blocks", any(row["status"] == "BLOCKED_CURRENT_CLAIM" for row in stress), "stress tensor blocker retained")
    add("VAL2555_05_source_missing", all(row["status"] in {"MISSING", "CANDIDATE_ONLY"} for row in source_descent), "source descent remains missing/candidate-only")
    add("VAL2555_06_red_team_written", len(red_team) >= 6 and any(row["status"] == "RISK_OPEN" for row in red_team), "tautology risks recorded")
    add("VAL2555_07_overall_verdict_nonclaim", any(row["verdict_id"] == "PV2555_5_overall" and row["result"] == "SHARPENED_BUT_NOT_PROMOTED" for row in verdicts), "overall verdict is sharpened but not promoted")
    add("VAL2555_08_claim_gates_safe", all(row["claim_allowed"] == "false" for row in gates), "no claim gate allows public/local-GR claim")
    add("VAL2555_09_next_target_written", bool(next_rows) and next_rows[0]["route_id"] == "NEXT2555_0_selected", "2556 source-current descent selected")
    add("VAL2555_10_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_rows), "nonclaim branch copies exist")
    add("VAL2555_11_no_formalization_artifacts", not formalization_hits(), "no 2555 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_hits()))
    add("VAL2555_12_all_outputs_inside_post_checkpoint", all(inside_root(path) for path in list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]), "all 2555 outputs stay inside post-checkpoint-work")
    add("VAL2555_13_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2555_CSV_{path.stem}", ok and count > 0, f"CSV parses with {count} rows" if ok else "CSV parse failed", detail or str(path))

    for copy_id, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2555_COPY_CSV_{copy_id}", ok and count > 0, f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed", detail or str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2555_OVERALL", overall, "2555 sharpens ACT2554_A into a formal q_loc contract but blocks theorem claims on source, boundary and stress gates")
    return [{**base_row(), **row} for row in rows]


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
        "# 2555 Y5 R2FR Vertical Generator Current-law Variation And Source Audit",
        "",
        "**Result:** ACT2554_A survives the first serious stress-test as a formal parent-action contract, not a theorem. The variation is genuinely useful: `delta_A S` produces the desired current law rather than merely asserting a local plateau. But source descent, boundary silence and stress-tensor silence all remain open, so local GR/Newton/PPN is still blocked.",
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
