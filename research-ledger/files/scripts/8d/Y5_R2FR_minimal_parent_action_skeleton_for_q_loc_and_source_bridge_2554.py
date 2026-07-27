from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2554"
BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_ACTION_SKELETON_FOR_QLOC_AND_SOURCE_BRIDGE_2554"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SCRIPTS = ROOT / "scripts"

DOC = ROOT / "2554-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-and-source-bridge.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2554_SOURCE_REGISTER.csv",
    "field_inventory": OUT / "P8_Y5_NO_SHADOW_2554_FIELD_INVENTORY.csv",
    "candidate_actions": OUT / "P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv",
    "variation_ownership": OUT / "P8_Y5_NO_SHADOW_2554_VARIATION_OWNERSHIP.csv",
    "qloc_derivation": OUT / "P8_Y5_NO_SHADOW_2554_QLOC_DERIVATION_ATTEMPT.csv",
    "source_bridge": OUT / "P8_Y5_NO_SHADOW_2554_SOURCE_BRIDGE_CONTRACT.csv",
    "local_vacuum_law": OUT / "P8_Y5_NO_SHADOW_2554_LOCAL_VACUUM_AMPLITUDE_LAW.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2554_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2554_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2554_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2554_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2554_VALIDATION.csv",
}

COPY_TARGETS = {
    "candidate_action_nonclaim": QUEUE / "JR2554_PARENT_ACTION_SKELETON_CANDIDATES_NONCLAIM.csv",
    "qloc_law_nonclaim": LOCAL_BOUNDS / "Qloc_local_vacuum_law_2554_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2554_00_2553_doc",
        "source_path": ROOT / "2553-Y5-R2FR-local-GR-route-triage-after-Hamiltonian-denominator-block.md",
        "needles": ["LGR2553_R0_new_parent_action_skeleton", "NEXT2553_0_selected", "VAL2553_OVERALL"],
        "role": "active handoff selecting constructive parent-action skeleton",
    },
    {
        "source_id": "SRC2554_01_2553_route_triage",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2553_LOCAL_GR_ROUTE_TRIAGE.csv",
        "needles": ["LGR2553_R0_new_parent_action_skeleton", "SELECTED_PRIMARY_NEXT_ROUTE"],
        "role": "machine-readable route selection",
    },
    {
        "source_id": "SRC2554_02_2553_prereqs",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2553_PREREQUISITE_MATRIX.csv",
        "needles": ["PRE2553_1_variational_origin_q_loc", "PRE2553_2_source_bridge", "PRE2553_4_local_vacuum_double_zero"],
        "role": "missing prerequisites to attack",
    },
    {
        "source_id": "SRC2554_03_2552_reopen_material",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2552_REOPEN_MATERIAL_SPEC.csv",
        "needles": ["MAT2552_0_action_source", "MAT2552_3_GK_pack", "MAT2552_4_source_pack"],
        "role": "parent-action reopen material requirements",
    },
    {
        "source_id": "SRC2554_04_1010_gk_residual",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "DEC1010_0_derivation_route_precise", "V1010_SUMMARY"],
        "role": "Gamma/Khat/q_loc hard block and exact route-to-proof",
    },
    {
        "source_id": "SRC2554_05_symbol_map",
        "source_path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "needles": ["q_loc^nu", "not_derived_zero; plateau_axiom_forbidden", "Pi_M"],
        "role": "symbol/action placement map",
    },
    {
        "source_id": "SRC2554_06_variation_gates",
        "source_path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "needles": ["FV512_2_Gamma_Khat_q", "fail_for_current_claim"],
        "role": "first-variation fail gate to improve",
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
    rows: list[dict[str, Any]] = []
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


def field_inventory_rows() -> list[dict[str, Any]]:
    rows = [
        ("FLD2554_0_metric", "g_mu_nu", "spacetime metric", "fundamental_or_background_parent", "needed for covariance, covariant derivatives, stress variation", "EH anchor exists but not full parent", "included_in_skeleton"),
        ("FLD2554_1_clock", "tau_mu / coframe", "local clock/coframe sector", "candidate_parent_field", "needed for local frame, P_loc and same-frame source readout", "not fully parent-owned", "included_as_conditional"),
        ("FLD2554_2_vertical_generator", "A_nu", "vertical/local generator", "new_auxiliary_candidate", "variation with respect to A_nu can own q_loc equation", "not currently sourced in corpus", "new_material_required"),
        ("FLD2554_3_connection_scalar", "Gamma_eff", "effective scalar connection/compression", "candidate_parent_field", "appears through grad^nu Gamma_eff in q_loc", "hard block in q_loc map", "included_as_conditional"),
        ("FLD2554_4_displacement_tensor", "K_hat^{mu nu}", "response/displacement tensor", "derived_or_auxiliary", "defined as partial L_K / partial(nabla_mu A_nu)", "not currently variationally derived", "included_as_derived_definition"),
        ("FLD2554_5_source_current", "J_M^nu", "matter/source worldtube current", "must_be_parent_derived", "right side of q_loc equation and Newton source bridge", "Pi_M/worldtube source bridge missing", "included_but_unsigned"),
        ("FLD2554_6_projector", "P_loc^nu_rho", "local projector/selector", "candidate_parent_or_frame_structure", "physical residual is P_loc applied to Euler current", "selector stress and boundary closure missing", "included_as_conditional"),
        ("FLD2554_7_reference", "beta_ref/H_ref", "reference/counterterm data", "late_boundary_data_only", "must not set source normalization", "2552 forbids denominator reuse", "not_used_in_skeleton"),
    ]
    return [
        {
            **base_row(),
            "field_id": field_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "role_in_skeleton": role,
            "current_evidence": evidence,
            "2554_treatment": treatment,
        }
        for field_id, symbol, meaning, status, role, evidence, treatment in rows
    ]


def candidate_action_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "candidate_id": "ACT2554_A_vertical_generator_current_law",
            "candidate_name": "vertical generator current-law action",
            "action_skeleton": "S_GK=int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma(Gamma_eff,g,tau)]",
            "key_definition": "K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)",
            "variation_target": "delta_A S gives nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}-J_M^nu=0",
            "why_it_is_not_a_plateau_axiom": "q_loc is an Euler equation for A_nu rather than imposed after the fact",
            "risk": "A_nu, L_K, L_Gamma, J_M and P_loc are new parent material; coupling may be tautological unless symmetry/source descent is supplied",
            "verdict": "BEST_CONSTRUCTIVE_CANDIDATE_BUT_NONCLAIM",
            "promote_now": "false",
        },
        {
            "candidate_id": "ACT2554_B_multiplier_constraint",
            "candidate_name": "direct multiplier constraint",
            "action_skeleton": "S_constraint=int sqrt(-g) lambda_nu P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}-J_M^nu)",
            "key_definition": "lambda_nu enforces q_loc=P_loc J_M",
            "variation_target": "delta_lambda S gives q_loc=P_loc J_M directly",
            "why_it_is_not_a_plateau_axiom": "not established; it is too close to imposing the answer",
            "risk": "high closure-risk unless lambda arises from gauge/symmetry reduction",
            "verdict": "DEMOTE_UNLESS_SYMMETRY_DERIVED",
            "promote_now": "false",
        },
        {
            "candidate_id": "ACT2554_C_quadratic_penalty",
            "candidate_name": "quadratic residual penalty",
            "action_skeleton": "S_penalty=int sqrt(-g)[-1/2 Z_q q_loc_nu q_loc^nu + source terms]",
            "key_definition": "q_loc treated as costly residual rather than exact constraint",
            "variation_target": "variation produces differential equations for q_loc but not automatic q_loc=0",
            "why_it_is_not_a_plateau_axiom": "residual is dynamical and bounded, not asserted zero",
            "risk": "gives finite bounds rather than exact GR reduction; may introduce local fifth-force tails",
            "verdict": "BOUND_FALLBACK_NOT_GR_PROOF",
            "promote_now": "false",
        },
        {
            "candidate_id": "ACT2554_D_reference_cancellation",
            "candidate_name": "reference/counterterm cancellation",
            "action_skeleton": "choose H_ref/B_ref so local q_loc readout cancels",
            "key_definition": "reference data absorbs local residual",
            "variation_target": "none before readout",
            "why_it_is_not_a_plateau_axiom": "it is not acceptable",
            "risk": "smuggles local GR through boundary bookkeeping",
            "verdict": "REJECTED",
            "promote_now": "false",
        },
    ]
    return [{**base_row(), **row} for row in rows]


def variation_ownership_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAR2554_0_delta_A", "A_nu", "nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu} - J_M^nu = 0", "owned by ACT2554_A if K_hat=partial L_K/partial(nabla A)", "FORMALLY_CLOSES_QLOC_EULER_EQUATION", "still needs source descent and dimensions"),
        ("VAR2554_1_delta_Gamma", "Gamma_eff", "-nabla_nu A^nu + partial L_Gamma/partial Gamma_eff = 0 plus boundary", "owned by ACT2554_A", "CLOSES_COMPANION_EQUATION_CONDITIONAL", "must not force unphysical gauge or nonlocal clock behaviour"),
        ("VAR2554_2_delta_matter", "Psi", "matter Euler equations plus source current J_M^nu", "not owned until L_m and source map are specified", "MISSING_SOURCE_BRIDGE", "Newton limit blocked until J_M is physical source current"),
        ("VAR2554_3_delta_metric", "g_mu_nu", "Einstein/EH stress plus GK stress plus matter stress", "not owned by minimal GK skeleton alone", "MISSING_FULL_PARENT_STRESS", "local GR pass requires stress either zero, bounded, or absorbed consistently"),
        ("VAR2554_4_delta_projector", "P_loc", "selector stress/boundary terms", "not owned", "MISSING_SELECTOR_VARIATION", "physical projection may leak residual if not parent-defined"),
        ("VAR2554_5_boundary", "boundary data", "n_mu K_hat^{mu nu} delta A_nu and Gamma/A surface terms", "not fixed by skeleton", "MISSING_BOUNDARY_SILENCE", "local vacuum law needs boundary flux condition"),
    ]
    return [
        {
            **base_row(),
            "variation_id": variation_id,
            "varied_object": varied_object,
            "formal_euler_output": output,
            "ownership_status": ownership,
            "closure_status": status,
            "remaining_issue": issue,
        }
        for variation_id, varied_object, output, ownership, status, issue in rows
    ]


def qloc_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        ("QDER2554_0_define_displacement", "Define K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu).", "definition from candidate L_K", "turns divergence of K_hat into the Euler divergence term", "PASS_AS_CANDIDATE_DEFINITION"),
        ("QDER2554_1_vary_A", "delta_A S_GK=int sqrt(-g)[-nabla_mu K_hat^{mu nu}+nabla^nu Gamma_eff-J_M^nu]delta A_nu + boundary.", "integration by parts with fixed delta A or boundary term cancelled", "gives the exact unprojected q equation", "PASS_AS_FORMAL_VARIATION"),
        ("QDER2554_2_project_local", "Apply P_loc: q_loc^nu=P_loc^nu_rho(nabla^rho Gamma_eff-nabla_mu K_hat^{mu rho})=P_loc^nu_rho J_M^rho.", "P_loc is fixed or parent-owned and commutes only as specified", "physical q_loc is source current projection", "CONDITIONAL_ON_PROJECTOR"),
        ("QDER2554_3_vacuum_zero", "If J_M^nu=0 and boundary flux is silent in the local vacuum collar, then q_loc^nu=0.", "source-free local exterior and boundary silence", "F1=0 follows because the residual itself is zero to all local perturbative orders allowed by the Euler equation", "CONDITIONAL_ZERO_NOT_CURRENT_CLAIM"),
        ("QDER2554_4_not_promoted", "The derivation is not promoted for current MTS.", "A_nu/L_K/L_Gamma/J_M/P_loc are not sourced from the corpus as a parent action", "2554 is a constructive contract, not evidence of local-GR pass", "NONCLAIM"),
    ]
    return [
        {
            **base_row(),
            "derivation_id": derivation_id,
            "step": step,
            "assumption": assumption,
            "result": result,
            "status": status,
        }
        for derivation_id, step, assumption, result, status in rows
    ]


def source_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        ("SRCBR2554_0_current_origin", "J_M^nu must be Noether/Hilbert matter current from L_matter, not a fitted mass current.", "prevents orbital-GM smuggling", "MISSING"),
        ("SRCBR2554_1_worldtube_integral", "M_source[W] or charge_source[W] must equal integral of J_M over a parent-defined worldtube/linking surface.", "needed for Newton source", "MISSING"),
        ("SRCBR2554_2_conservation", "nabla_nu J_M^nu=0 or controlled exchange with GK sector must follow from matter equations/diffeomorphism invariance.", "needed for stable local source readout", "MISSING"),
        ("SRCBR2554_3_external_vacuum", "Outside the worldtube, J_M^nu=0 except distributional boundary layer terms explicitly bounded.", "needed for q_loc zero exterior", "MISSING"),
        ("SRCBR2554_4_universality", "same J_M coupling must apply across local tests without species-dependent hand tuning.", "needed for WEP/PPN safety", "MISSING"),
    ]
    return [
        {
            **base_row(),
            "bridge_id": bridge_id,
            "required_clause": clause,
            "why_needed": why,
            "current_status": status,
        }
        for bridge_id, clause, why, status in rows
    ]


def local_vacuum_law_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "law_id": "LAW2554_0_exact_conditional_zero",
            "quantity": "q_loc^nu",
            "law": "q_loc^nu=P_loc^nu_rho J_M^rho",
            "conditions": "ACT2554_A is valid, P_loc is parent-owned/fixed, source-free local collar J_M=0, boundary flux silent",
            "consequence": "q_loc^nu -> 0 exactly in local vacuum",
            "claim_status": "CONDITIONAL_CONTRACT_ONLY",
        },
        {
            "law_id": "LAW2554_1_F1_zero",
            "quantity": "F1",
            "law": "F1=0 because the first local residual coefficient is proportional to the Euler-source residual J_M plus boundary leakage",
            "conditions": "same as LAW2554_0 plus smooth weak-field expansion",
            "consequence": "no linear local fifth-force term in the vacuum collar",
            "claim_status": "CONDITIONAL_CONTRACT_ONLY",
        },
        {
            "law_id": "LAW2554_2_Delta_m_bound",
            "quantity": "Delta m / m",
            "law": "abs(Delta m/m) <= C_P[||P_loc J_M||_collar + ||boundary_flux||]/M_source",
            "conditions": "source bridge supplies M_source and norm convention",
            "consequence": "mass/readout leakage is bounded by source leakage and boundary flux, not arbitrary plateau",
            "claim_status": "BOUND_FORM_ONLY",
        },
        {
            "law_id": "LAW2554_3_transition_length",
            "quantity": "ell_tr/L_cg",
            "law": "ell_tr/L_cg = 1/(m_tr L_cg) if L_Gamma or L_K supplies a parent mass/gap m_tr",
            "conditions": "operator has a real positive gap and cosmological gradient scale L_cg is independently defined",
            "consequence": "transition scale can be derived from parent coefficients rather than fitted as a local patch",
            "claim_status": "PARAMETRIC_ONLY",
        },
        {
            "law_id": "LAW2554_4_current_limit",
            "quantity": "local GR/Newton/PPN",
            "law": "not claimed",
            "conditions": "current corpus lacks ACT2554_A source adoption and source bridge",
            "consequence": "2554 improves route clarity but does not pass local GR",
            "claim_status": "NONCLAIM",
        },
    ]
    return [{**base_row(), **row} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2554_0_formal_variation", "ACT2554_A formally produces the q_loc Euler equation.", "PASS_AS_CANDIDATE", "delta_A derivation closes algebraically once K_hat is a displacement tensor", "true", "false"),
        ("GATE2554_1_parent_source_adoption", "Current MTS adopts ACT2554_A as a sourced parent action.", "BLOCKED", "A_nu, L_K, L_Gamma, J_M and P_loc are new material", "false", "false"),
        ("GATE2554_2_source_bridge", "J_M source bridge is parent-derived.", "BLOCKED", "Pi_M/worldtube/source current remains missing", "false", "false"),
        ("GATE2554_3_local_vacuum_zero", "q_loc^nu -> 0 in local vacuum is derived for current MTS.", "CONDITIONAL_ONLY", "follows from candidate action only if source and boundary clauses are supplied", "false", "false"),
        ("GATE2554_4_local_GR_Newton_PPN", "local GR/Newton/PPN branch passes.", "BLOCKED", "candidate action is not yet full parent action and stress/source/projector terms are not closed", "false", "false"),
        ("GATE2554_5_no_GitHub", "No public/GitHub update from this checkpoint.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [
        {
            **base_row(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": status,
            "reason": reason,
            "gate_pass": passed,
            "claim_allowed": allowed,
        }
        for gate_id, claim, status, reason, passed, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2554_0_best_candidate", "Keep ACT2554_A as the best constructive candidate.", "it derives the q_loc equation as an Euler equation for A_nu rather than imposing a plateau", "next work should vary and dimension-check this candidate harder"),
        ("DEC2554_1_not_promoted", "Do not promote ACT2554_A to current MTS theorem.", "its fields and source current are not sourced parent material yet", "local-GR claim remains blocked"),
        ("DEC2554_2_multiplier_demoted", "Demote direct multiplier constraint.", "it can force q_loc=0 too cheaply and would look like closure by notation", "only revisit if multiplier is symmetry-derived"),
        ("DEC2554_3_source_bridge_is_key", "Treat J_M/Pi_M/worldtube as equally important as q_loc.", "without source bridge, Newton limit can be smuggled through fitted GM", "next checkpoint must own current and source integral"),
        ("DEC2554_4_next_target", "Move to variation/dimension/source audit of ACT2554_A.", "the route is now constructive enough to test rather than merely discuss", "2555 should try to break the candidate"),
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
            "route_id": "NEXT2554_0_selected",
            "selection_status": "selected",
            "target_file": "2555-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md",
            "target_script": "scripts/Y5_R2FR_vertical_generator_current_law_variation_and_source_audit_2555.py",
            "task": "stress-test ACT2554_A by doing the variation, dimensional bookkeeping, boundary terms, stress tensor exposure, and J_M source-current descent clauses",
            "acceptance_target": "either promote the candidate to a sharper parent-action contract or demote it as tautological/inconsistent",
            "guardrails": "no local-GR claim; no M_H_ref reuse; no orbital-GM source definition; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["candidate_actions"], COPY_TARGETS["candidate_action_nonclaim"])
    shutil.copyfile(OUTPUTS["local_vacuum_law"], COPY_TARGETS["qloc_law_nonclaim"])
    rows = []
    for copy_id, target in COPY_TARGETS.items():
        source = OUTPUTS["candidate_actions"] if copy_id == "candidate_action_nonclaim" else OUTPUTS["local_vacuum_law"]
        rows.append(
            {
                **base_row(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


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
        "2554-Y5",
        "_2554_",
        "_2554.",
        "JR2554",
        "P8_Y5_NO_SHADOW_2554",
        "P8_Y5_BRR545_2554",
        "Y5_R2FR_minimal_parent_action_skeleton_for_q_loc_and_source_bridge_2554",
    )
    return [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in artifact_markers)
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    fields: list[dict[str, Any]],
    actions: list[dict[str, Any]],
    variations: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add("VAL2554_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present", ";".join(row["source_id"] for row in sources if row["source_pass"] != "true"))
    add("VAL2554_01_fields_written", len(fields) >= 8, "field inventory covers metric, clock, vertical generator, Gamma, Khat, source, projector and reference")
    add("VAL2554_02_candidate_actions_written", len(actions) >= 4, "candidate action options written")
    add("VAL2554_03_best_candidate_nonclaim", any(row["candidate_id"] == "ACT2554_A_vertical_generator_current_law" and row["verdict"] == "BEST_CONSTRUCTIVE_CANDIDATE_BUT_NONCLAIM" and row["promote_now"] == "false" for row in actions), "best candidate exists but is nonclaim")
    add("VAL2554_04_variation_attempt_written", any(row["variation_id"] == "VAR2554_0_delta_A" for row in variations), "delta_A ownership row written")
    add("VAL2554_05_q_loc_derivation_contract", any(row["derivation_id"] == "QDER2554_1_vary_A" and row["status"] == "PASS_AS_FORMAL_VARIATION" for row in derivation), "formal q_loc variation route written")
    add("VAL2554_06_source_bridge_missing", all(row["current_status"] == "MISSING" for row in bridge), "source bridge remains explicitly missing")
    add("VAL2554_07_laws_nonclaim", all(row["claim_allowed"] == "false" for row in laws), "local vacuum/amplitude laws are nonclaim")
    add("VAL2554_08_claim_gates_safe", all(row["claim_allowed"] == "false" for row in gates), "no local-GR claim allowed")
    add("VAL2554_09_next_target_written", bool(next_rows) and next_rows[0]["route_id"] == "NEXT2554_0_selected", "2555 variation/source audit selected")
    add("VAL2554_10_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_rows), "nonclaim branch copies exist")
    add("VAL2554_11_no_formalization_artifacts", not formalization_hits(), "no 2554 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_hits()))
    add("VAL2554_12_all_outputs_inside_post_checkpoint", all(inside_root(path) for path in list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]), "all 2554 outputs stay inside post-checkpoint-work")
    add("VAL2554_13_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2554_CSV_{path.stem}", ok and count > 0, f"CSV parses with {count} rows" if ok else "CSV parse failed", detail or str(path))

    for copy_id, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2554_COPY_CSV_{copy_id}", ok and count > 0, f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed", detail or str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2554_OVERALL", overall, "2554 constructs a promising q_loc parent-action skeleton but keeps source bridge/local-GR claims blocked")
    return [{**base_row(), **row} for row in rows]


def write_doc(
    sources: list[dict[str, Any]],
    fields: list[dict[str, Any]],
    actions: list[dict[str, Any]],
    variations: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2554 Y5 R2FR Minimal Parent Action Skeleton For q_loc And Source Bridge",
        "",
        "**Result:** constructive route opened, not claimed. The best candidate is a vertical-generator current-law action where `A_nu` is the varied object and `K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)`. This gives the desired `q_loc` equation as an Euler equation rather than a plateau axiom, but it is new parent material and the source bridge is still unsigned.",
        "",
        "**Core sketch:** take",
        "",
        "`S_GK = int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma(Gamma_eff,g,tau)]`",
        "",
        "with `K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)`. Varying `A_nu` gives",
        "",
        "`nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu} - J_M^nu = 0`,",
        "",
        "so `q_loc^nu=P_loc^nu_rho J_M^rho`. In a source-free local collar with boundary silence this gives the desired local vacuum zero. The sting in the tail: `A_nu`, `L_K`, `L_Gamma`, `J_M`, `P_loc`, and boundary/source descent must be sourced from a parent theory before this counts.",
        "",
        "## Source Register",
        markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Field Inventory",
        markdown_table(fields, ["field_id", "symbol", "meaning", "status", "role_in_skeleton", "current_evidence", "2554_treatment"]),
        "",
        "## Candidate Actions",
        markdown_table(actions, ["candidate_id", "candidate_name", "action_skeleton", "key_definition", "variation_target", "risk", "verdict", "promote_now"]),
        "",
        "## Variation Ownership",
        markdown_table(variations, ["variation_id", "varied_object", "formal_euler_output", "ownership_status", "closure_status", "remaining_issue"]),
        "",
        "## q_loc Derivation Attempt",
        markdown_table(derivation, ["derivation_id", "step", "assumption", "result", "status"]),
        "",
        "## Source Bridge Contract",
        markdown_table(bridge, ["bridge_id", "required_clause", "why_needed", "current_status"]),
        "",
        "## Local Vacuum And Amplitude Law",
        markdown_table(laws, ["law_id", "quantity", "law", "conditions", "consequence", "claim_status"]),
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
    fields = field_inventory_rows()
    actions = candidate_action_rows()
    variations = variation_ownership_rows()
    derivation = qloc_derivation_rows()
    bridge = source_bridge_rows()
    laws = local_vacuum_law_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["field_inventory"], fields)
    write_csv(OUTPUTS["candidate_actions"], actions)
    write_csv(OUTPUTS["variation_ownership"], variations)
    write_csv(OUTPUTS["qloc_derivation"], derivation)
    write_csv(OUTPUTS["source_bridge"], bridge)
    write_csv(OUTPUTS["local_vacuum_law"], laws)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, fields, actions, variations, derivation, bridge, laws, gates, decisions, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, fields, actions, variations, derivation, bridge, laws, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
