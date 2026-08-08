from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2561"
BRANCH_ID = "MTS_R2FR_EXPLICIT_GK_QUADRATIC_OPERATOR_SIGN_AUDIT_2561"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2561-Y5-R2FR-explicit-GK-quadratic-operator-sign-audit.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2561_SOURCE_REGISTER.csv",
    "operator_ansatz": OUT / "P8_Y5_NO_SHADOW_2561_OPERATOR_ANSATZ.csv",
    "dimension_sign_table": OUT / "P8_Y5_NO_SHADOW_2561_DIMENSION_SIGN_TABLE.csv",
    "coercivity_audit": OUT / "P8_Y5_NO_SHADOW_2561_COERCIVITY_AUDIT.csv",
    "ghost_tachyon_checks": OUT / "P8_Y5_NO_SHADOW_2561_GHOST_TACHYON_CHECKS.csv",
    "nohair_eligibility": OUT / "P8_Y5_NO_SHADOW_2561_NOHAIR_ELIGIBILITY.csv",
    "stress_bound_route": OUT / "P8_Y5_NO_SHADOW_2561_STRESS_BOUND_ROUTE.csv",
    "promotion_verdict": OUT / "P8_Y5_NO_SHADOW_2561_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2561_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2561_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2561_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2561_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2561_VALIDATION.csv",
}

COPY_TARGETS = {
    "operator_sign_contract": LOCAL_BOUNDS / "GK_quadratic_operator_sign_contract_2561_NONCLAIM.csv",
    "nohair_eligibility_contract": LOCAL_BOUNDS / "GK_nohair_eligibility_2561_NONCLAIM.csv",
    "parent_sign_boundary_queue": QUEUE / "JR2561_PARENT_SIGN_BOUNDARY_TOPOLOGY_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2561_00_2560_doc",
        "source_path": ROOT / "2560-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
        "needles": ["NEXT2560_0_selected", "POS2560_1_quadratic_form", "COEF2560_0_c_A", "VAL2560_OVERALL"],
        "role": "active handoff selecting explicit GK quadratic operator sign audit",
    },
    {
        "source_id": "SRC2561_01_2560_positivity",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2560_POSITIVITY_CLAUSES.csv",
        "needles": ["POS2560_1_quadratic_form", "POS2560_2_cross_term_bound", "POS2560_7_parent_sign"],
        "role": "positivity and cross-term clauses to instantiate",
    },
    {
        "source_id": "SRC2561_02_2560_coefficients",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2560_PARENT_COEFFICIENT_LEDGER.csv",
        "needles": ["COEF2560_0_c_A", "COEF2560_4_eta_cross", "MISSING_PARENT_VALUE"],
        "role": "missing parent coefficients/signs ledger",
    },
    {
        "source_id": "SRC2561_03_2560_nohair",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2560_NOHAIR_PROOF_ATTEMPT.csv",
        "needles": ["NH2560_2_energy_identity", "NH2560_6_current_status", "NOT_PROMOTED"],
        "role": "no-hair proof method and nonpromotion status",
    },
    {
        "source_id": "SRC2561_04_2560_bound",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2560_STRESS_BOUND_FALLBACK.csv",
        "needles": ["BND2560_1_energy_bound", "BND2560_5_current_status", "MISSING_PARENT_COEFFICIENTS"],
        "role": "stress-bound fallback if no-hair cannot be parent-signed",
    },
    {
        "source_id": "SRC2561_05_2555_variation",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_VARIATION_AUDIT.csv",
        "needles": ["VAR2555_2_delta_A_bulk", "VAR2555_4_delta_Gamma_bulk", "VAR2555_6_not_theorem"],
        "role": "A/Gamma Euler equations compatible with operator ansatz",
    },
    {
        "source_id": "SRC2561_06_2554_candidate",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2554_A_vertical_generator_current_law", "A_nu nabla^nu Gamma_eff", "BEST_CONSTRUCTIVE_CANDIDATE_BUT_NONCLAIM"],
        "role": "candidate GK source action containing the A-Gamma cross structure",
    },
    {
        "source_id": "SRC2561_07_2471_precedent",
        "source_path": ROOT / "2471-Y5-R2FR-explicit-GK-quadratic-operator-sign-audit.md",
        "needles": ["OP2471_0_stationary_energy", "COER2471_1_cross_bound", "VAL2471_OVERALL"],
        "role": "earlier explicit operator sign audit precedent, re-run against 2560 chain",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for spec in SOURCE_SPECS:
        path = Path(spec["source_path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        exists = path.exists()
        rows.append(
            {
                **base_row(),
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "missing_needles": ";".join(missing),
                "source_pass": bool_text(exists and not missing),
                "role": spec["role"],
            }
        )
    return rows


def operator_ansatz_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OP2561_0_stationary_energy",
            "E_GK=int_Omega sqrt(h)[0.5 Z_A D_i A_j D^i A^j + 0.5 m_A2 A_i A^i + 0.5 Z_G D_i gamma D^i gamma + 0.5 m_G2 gamma^2 + c_AG A^i D_i gamma]",
            "gamma:=Gamma_eff-Gamma_0; stationary exterior energy functional, not full Lorentzian quantum action",
            "minimal explicit operator for no-hair/sign audit",
            "CANDIDATE_ONLY",
        ),
        (
            "OP2561_1_displacement",
            "K_hat^{ij}=Z_A D^i A^j plus possible symmetric/projected refinements",
            "matches K_hat as derivative of L_K with respect to D_i A_j",
            "keeps q_loc Euler route compatible",
            "CANDIDATE_ONLY",
        ),
        (
            "OP2561_2_gamma_gap",
            "L_Gamma≈0.5 m_G2 gamma^2 plus optional positive gradient term",
            "local expansion around Gamma_0",
            "gapped Gamma branch can suppress scalar memory hair locally",
            "CANDIDATE_ONLY",
        ),
        (
            "OP2561_3_cross_origin",
            "c_AG A^i D_i gamma is the stationary energy version of A_nu nabla^nu Gamma_eff",
            "cross term is required by the q_loc current-law action",
            "must be bounded or completed by parent terms to avoid hair/instability",
            "RISK_TERM",
        ),
        (
            "OP2561_4_vacuum_normalization",
            "L_Gamma has gamma=0 as stationary point and zero local vacuum energy after fixed parent subtraction",
            "avoids local cosmological stress",
            "required for T_GK silence",
            "REQUIRED_NOT_SOURCED",
        ),
        (
            "OP2561_5_scope",
            "operator is a minimal audit ansatz, not a source-backed MTS action",
            "coefficients are not yet parent-signed",
            "cannot promote local GR",
            "NONCLAIM",
        ),
    ]
    return [
        {**base_row(), "operator_id": item, "operator_or_clause": operator, "basis": basis, "effect": effect, "status": status}
        for item, operator, basis, effect, status in rows
    ]


def dimension_sign_rows() -> list[dict[str, Any]]:
    rows = [
        ("SIGN2561_0_Z_A", "Z_A", "coefficient of D A squared", "positive", "Z_A>0", "MISSING_PARENT_SIGN"),
        ("SIGN2561_1_m_A2", "m_A2", "A mode gap/mass squared", "nonnegative or gauge-removed", "m_A2>0 for easiest no-hair; m_A2=0 needs gauge/topology proof", "MISSING_PARENT_SIGN"),
        ("SIGN2561_2_Z_G", "Z_G", "coefficient of D gamma squared", "positive", "Z_G>0", "MISSING_PARENT_SIGN"),
        ("SIGN2561_3_m_G2", "m_G2", "Gamma potential curvature at Gamma_0", "nonnegative", "m_G2>0 for gapped scalar; m_G2=0 needs boundary vacuum fixing", "MISSING_PARENT_SIGN"),
        ("SIGN2561_4_c_AG", "c_AG", "A-Gamma derivative mixing", "bounded", "c_AG^2 < m_A2 Z_G in normalized convention", "MISSING_PARENT_BOUND"),
        ("SIGN2561_5_Lambda_GK", "Lambda_GK", "vacuum energy/subtraction", "zero or fixed", "L_Gamma(Gamma_0)=0 or parent-fixed Lambda", "MISSING_PARENT_NORMALISATION"),
        ("SIGN2561_6_boundary", "C_boundary", "boundary/no-flux control", "nonnegative leakage coefficient", "zero for exact no-hair or bounded for fallback", "MISSING_BOUNDARY_CONTRACT"),
    ]
    return [
        {**base_row(), "sign_id": item, "symbol": symbol, "meaning": meaning, "required_sign": required_sign, "condition": condition, "status": status}
        for item, symbol, meaning, required_sign, condition, status in rows
    ]


def coercivity_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("COER2561_0_positive_blocks", "Z_A>0, Z_G>0, m_A2>0, m_G2>=0", "base positive quadratic energy", "REQUIRED_NOT_DERIVED"),
        ("COER2561_1_cross_bound", "c_AG^2 < m_A2 Z_G in a normalized stationary energy convention", "Schur/Young bound for A dot D gamma cross term", "PLAUSIBLE_IF_PARENT_SIGNED"),
        ("COER2561_2_eta_form", "abs(cross) <= eta E_positive with eta<1", "coordinate-free statement of the same condition", "PLAUSIBLE_IF_PARENT_SIGNED"),
        ("COER2561_3_completed_square", "0.5 m_A2 |A|^2 + c_AG A.D gamma + 0.5 Z_G |D gamma|^2 = positive square + 0.5(Z_G-c_AG^2/m_A2)|D gamma|^2", "explicit completion of square when m_A2>0", "PASS_AS_FORMAL_INEQUALITY"),
        ("COER2561_4_massless_gamma_warning", "if m_G2=0 then constant gamma zero-mode must be removed by boundary/vacuum normalization", "otherwise vacuum hair can survive", "BOUNDARY_REQUIRED"),
        ("COER2561_5_massless_A_warning", "if m_A2=0 then transverse/harmonic A hair can survive unless gauge/topology removes it", "Maxwell-like no-hair requires gauge and boundary theorem", "TOPOLOGY_REQUIRED"),
        ("COER2561_6_current_status", "current corpus has no parent-signed values or inequalities for Z_A,Z_G,m_A2,m_G2,c_AG", "no-hair eligibility remains unproved", "NOT_PROMOTED"),
    ]
    return [
        {**base_row(), "coercivity_id": item, "condition_or_step": condition, "basis": basis, "status": status}
        for item, condition, basis, status in rows
    ]


def ghost_tachyon_rows() -> list[dict[str, Any]]:
    rows = [
        ("GHOST2561_0_vector_gradient", "Z_A<0", "ghost/gradient instability in A sector", "FORBIDDEN_SIGN"),
        ("GHOST2561_1_gamma_gradient", "Z_G<0", "ghost/gradient instability in Gamma sector", "FORBIDDEN_SIGN"),
        ("GHOST2561_2_vector_mass", "m_A2<0", "tachyonic vector hair in stationary exterior", "FORBIDDEN_SIGN"),
        ("GHOST2561_3_gamma_mass", "m_G2<0", "tachyonic Gamma/memory hair", "FORBIDDEN_SIGN"),
        ("GHOST2561_4_cross_instability", "c_AG^2 >= m_A2 Z_G", "cross-term can defeat positive blocks", "FORBIDDEN_OR_BOUND_ROUTE"),
        ("GHOST2561_5_vacuum_energy", "unfixed L_Gamma(Gamma_0)", "local Lambda/stress offset survives", "FORBIDDEN_FOR_GR_CLAIM"),
        ("GHOST2561_6_status", "no forbidden sign is known to occur, but no healthy sign is parent-proven either", "source audit", "UNKNOWN_NOT_CLAIM"),
    ]
    return [
        {**base_row(), "check_id": item, "bad_condition": bad_condition, "effect": effect, "status": status}
        for item, bad_condition, effect, status in rows
    ]


def nohair_eligibility_rows() -> list[dict[str, Any]]:
    rows = [
        ("NHG2561_0_operator", "minimal stationary quadratic operator exists", "OP2561_0", "PASS_AS_ANSATZ"),
        ("NHG2561_1_coercive", "coercivity condition can be stated", "COER2561_0-3", "PASS_AS_INEQUALITY"),
        ("NHG2561_2_parent_sign", "coefficients are parent-derived with healthy signs", "SIGN2561 rows", "MISSING_PARENT_SIGN"),
        ("NHG2561_3_boundary_topology", "boundary and topology eliminate harmonic hair", "COER2561_4-5", "MISSING_BOUNDARY_TOPOLOGY"),
        ("NHG2561_4_tau_projector", "tau/P_loc stress is silent or fixed", "2560 POS2560_6", "MISSING_TAU_PROJECTOR_STRESS_CLAUSE"),
        ("NHG2561_5_vacuum_normalization", "Gamma vacuum energy is zero or fixed", "OP2561_4", "MISSING_PARENT_NORMALISATION"),
        ("NHG2561_6_eligibility", "no-hair is plausible if NHG2561_2-5 close", "operator and coercivity contracts", "PLAUSIBLE_NOT_PROVED"),
        ("NHG2561_7_current_claim", "current MTS does not yet pass local GR/PPN", "missing parent signs and boundary/topology", "BLOCKED_CURRENT_CLAIM"),
    ]
    return [
        {**base_row(), "eligibility_id": item, "criterion": criterion, "basis": basis, "status": status}
        for item, criterion, basis, status in rows
    ]


def stress_bound_route_rows() -> list[dict[str, Any]]:
    rows = [
        ("BOUND2561_0_exact_branch", "if healthy signs plus boundary/topology close, epsilon_GK=0", "no-hair route", "CONDITIONAL_ONLY"),
        ("BOUND2561_1_near_coercive_branch", "if c_AG^2 approaches m_A2 Z_G, residual bound degrades as 1/(1-eta)", "cross-term bound", "BOUND_FORM_ONLY"),
        ("BOUND2561_2_massless_branch", "if m_A2=0 or m_G2=0, harmonic/constant modes require separate boundary/topology bounds", "massless warnings", "BOUND_FORM_ONLY"),
        ("BOUND2561_3_negative_branch", "if any required sign is wrong, no-hair route fails and local branch must use stress-bound-only or be rejected", "ghost/tachyon audit", "DEMOTE_IF_FOUND"),
        ("BOUND2561_4_numeric_block", "no numerical epsilon_GK can be computed until parent signs/coefs are supplied", "coefficient ledger", "MISSING_PARENT_COEFFICIENTS"),
    ]
    return [
        {**base_row(), "route_id": item, "route_or_bound": route, "basis": basis, "status": status}
        for item, route, basis, status in rows
    ]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2561_0_operator", "Is an explicit GK quadratic operator written?", "YES_AS_ANSATZ", "minimal stationary operator recorded", "progress"),
        ("PV2561_1_signs", "Are sign/coercivity conditions known?", "YES_AS_CONDITIONS", "Z/mass signs plus cross bound stated", "contract only"),
        ("PV2561_2_parent_origin", "Are the signs parent-derived?", "NO", "current corpus lacks source for coefficients", "blocks promotion"),
        ("PV2561_3_nohair", "Is no-hair plausible?", "PLAUSIBLE_NOT_PROVED", "coercive branch exists if parent signs and boundary/topology close", "next target"),
        ("PV2561_4_bound_route", "Is stress-bound fallback ready?", "YES_FORMAL", "operator audit identifies failure modes and residual branches", "nonclaim fallback"),
        ("PV2561_5_overall", "Overall 2561 verdict", "OPERATOR_SIGN_CONTRACT_WRITTEN_PARENT_SIGN_AND_BOUNDARY_PENDING", "no local GR claim; next gate is parent sign plus boundary topology", "continue"),
    ]
    return [
        {**base_row(), "verdict_id": item, "question": question, "result": result, "evidence": evidence, "effect": effect}
        for item, question, result, evidence, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2561_0_operator_ansatz", "Explicit GK quadratic operator exists.", "PASS_AS_ANSATZ", "operator written for stationary exterior audit", "true", "false"),
        ("GATE2561_1_coercivity_conditions", "No-hair coercivity conditions are stated.", "PASS_AS_CONTRACT", "positive blocks and cross bound stated", "true", "false"),
        ("GATE2561_2_parent_signs", "Parent action proves healthy signs.", "BLOCKED", "coefficients remain unsigned", "false", "false"),
        ("GATE2561_3_nohair_proved", "No-hair theorem is proved.", "BLOCKED", "boundary/topology/tau clauses remain unsigned", "false", "false"),
        ("GATE2561_4_local_GR_PPN", "Local GR/PPN branch passes.", "BLOCKED", "no-hair and numeric stress bounds not closed", "false", "false"),
        ("GATE2561_5_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [
        {**base_row(), "gate_id": item, "claim": claim, "gate_status": status, "reason": reason, "gate_pass": gate_pass, "claim_promoted": promoted}
        for item, claim, status, reason, gate_pass, promoted in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2561_0_keep_operator", "Keep the minimal quadratic GK operator as an audit ansatz.", "it makes the hidden sign problem explicit", "use it for parent-sign search"),
        ("DEC2561_1_no_promotion", "Do not promote no-hair or local GR.", "healthy signs and boundary/topology are not parent-derived", "claim gates stay blocked"),
        ("DEC2561_2_next_parent_sign", "Next search for parent sign origin and boundary/topology closure.", "operator audit says those are now the precise missing clauses", "2562 selected"),
        ("DEC2561_3_bound_fallback", "Keep stress-bound-only fallback if parent signs fail.", "wrong sign or unbounded cross-term would kill no-hair", "future empirical/local residual route preserved"),
    ]
    return [
        {**base_row(), "decision_id": item, "decision": decision, "reason": reason, "effect": effect}
        for item, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2561_0_selected",
            "selection_status": "selected",
            "target_file": "2562-Y5-R2FR-parent-sign-origin-and-boundary-topology-nohair-gate.md",
            "target_script": "scripts/Y5_R2FR_parent_sign_origin_and_boundary_topology_nohair_gate_2562.py",
            "task": "try to parent-sign the GK quadratic coefficients and close boundary/topology no-hair; if not possible, demote the local metric branch to stress-bound only",
            "acceptance_target": "parent sign source audit, boundary condition ledger, topology/harmonic hair audit, no-hair eligibility verdict, stress-bound demotion rule, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    copy_sources = {
        "operator_sign_contract": OUTPUTS["coercivity_audit"],
        "nohair_eligibility_contract": OUTPUTS["nohair_eligibility"],
        "parent_sign_boundary_queue": OUTPUTS["dimension_sign_table"],
    }
    rows = []
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        shutil.copyfile(source, target)
        rows.append(
            {
                **base_row(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": bool_text(source.exists()),
                "target_exists": bool_text(target.exists()),
            }
        )
    return rows


def csv_row_count(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    with path.open(newline="", encoding="utf-8") as handle:
        return max(sum(1 for _ in csv.DictReader(handle)), 0)


def formalization_status_detail() -> tuple[bool, str]:
    touched_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC, Path(__file__).resolve()]
    outside_formalization = [path for path in touched_paths if not is_relative_to(path, FORMALIZATION)]
    return len(outside_formalization) == len(touched_paths), f"declared_2561_paths_outside_formalization={len(outside_formalization)}/{len(touched_paths)}"


def validation_rows(
    sources: list[dict[str, Any]],
    operator: list[dict[str, Any]],
    signs: list[dict[str, Any]],
    coercivity: list[dict[str, Any]],
    ghost: list[dict[str, Any]],
    eligibility: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail})

    add("VAL2561_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present")
    add("VAL2561_01_operator_written", any(row["operator_id"] == "OP2561_0_stationary_energy" and row["status"] == "CANDIDATE_ONLY" for row in operator), "explicit operator ansatz written")
    add("VAL2561_02_sign_table", any(row["sign_id"] == "SIGN2561_4_c_AG" and row["status"] == "MISSING_PARENT_BOUND" for row in signs), "dimension/sign table records cross bound")
    add("VAL2561_03_coercivity_bound", any(row["coercivity_id"] == "COER2561_1_cross_bound" and row["status"] == "PLAUSIBLE_IF_PARENT_SIGNED" for row in coercivity), "coercivity cross-term bound stated")
    add("VAL2561_04_completed_square", any(row["coercivity_id"] == "COER2561_3_completed_square" and row["status"] == "PASS_AS_FORMAL_INEQUALITY" for row in coercivity), "completed-square inequality recorded")
    add("VAL2561_05_ghost_tachyon", len(ghost) >= 7 and any(row["check_id"] == "GHOST2561_4_cross_instability" for row in ghost), "ghost/tachyon checks recorded")
    add("VAL2561_06_nohair_not_promoted", any(row["eligibility_id"] == "NHG2561_7_current_claim" and row["status"] == "BLOCKED_CURRENT_CLAIM" for row in eligibility), "no-hair/local-GR claim remains blocked")
    add("VAL2561_07_bound_fallback", any(row["route_id"] == "BOUND2561_3_negative_branch" and row["status"] == "DEMOTE_IF_FOUND" for row in bounds), "stress-bound demotion route recorded")
    add("VAL2561_08_overall_verdict", any(row["verdict_id"] == "PV2561_5_overall" and row["result"] == "OPERATOR_SIGN_CONTRACT_WRITTEN_PARENT_SIGN_AND_BOUNDARY_PENDING" for row in verdicts), "overall verdict preserves nonclaim status")
    add("VAL2561_09_claim_gates_safe", all(row["claim_promoted"] == "false" for row in gates), "no claim gate promotes local-GR/Newton claims")
    add("VAL2561_10_next_target_written", any(row["route_id"] == "NEXT2561_0_selected" and row["selection_status"] == "selected" for row in next_rows), "2562 parent-sign/boundary target selected")
    add("VAL2561_11_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_copies), "nonclaim branch copies exist")

    output_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]
    add("VAL2561_12_all_outputs_inside_post_checkpoint", all(is_relative_to(path, ROOT) for path in output_paths), "all 2561 outputs stay inside post-checkpoint-work")
    formalization_ok, formalization_detail = formalization_status_detail()
    add("VAL2561_13_formalization_workbench_not_targeted", formalization_ok, "declared 2561 outputs do not target formalization-workbench", formalization_detail)

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        add(f"VAL2561_OUTPUT_{key}", path.exists() and csv_row_count(path) > 0, f"{key} output exists and has rows", str(path))

    for copy_id, path in COPY_TARGETS.items():
        add(f"VAL2561_COPY_{copy_id}", path.exists() and csv_row_count(path) > 0, f"{copy_id} copy exists and has rows", str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2561_OVERALL", overall, "2561 writes explicit GK quadratic operator signs, keeps no-hair nonclaim, and selects parent-sign/boundary gate")
    return rows


def escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(escape_md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    operator: list[dict[str, Any]],
    signs: list[dict[str, Any]],
    coercivity: list[dict[str, Any]],
    ghost: list[dict[str, Any]],
    eligibility: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2561 Y5 R2FR Explicit GK Quadratic Operator Sign Audit",
                "**Status:** explicit operator audit written, not promoted. A minimal stationary exterior GK energy ansatz now makes the hidden sign problem concrete: healthy no-hair needs positive `Z_A`, `Z_G`, nonnegative/gapped `m_A2`, `m_G2`, bounded `c_AG`, parent-normalized vacuum energy, and boundary/topology silence.",
                "**Main result:** no fatal sign is currently proven, but no healthy sign is parent-proven either. The no-hair route is plausible if the parent action signs the operator and closes boundary/topology/tau clauses. Until then, local GR/PPN remains blocked and the fallback is stress-bound-only.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
                "## Operator Ansatz",
                markdown_table(operator, ["operator_id", "operator_or_clause", "basis", "effect", "status"]),
                "## Dimension And Sign Table",
                markdown_table(signs, ["sign_id", "symbol", "meaning", "required_sign", "condition", "status"]),
                "## Coercivity Audit",
                markdown_table(coercivity, ["coercivity_id", "condition_or_step", "basis", "status"]),
                "## Ghost/Tachyon Checks",
                markdown_table(ghost, ["check_id", "bad_condition", "effect", "status"]),
                "## No-hair Eligibility",
                markdown_table(eligibility, ["eligibility_id", "criterion", "basis", "status"]),
                "## Stress Bound Route",
                markdown_table(bounds, ["route_id", "route_or_bound", "basis", "status"]),
                "## Promotion Verdict",
                markdown_table(verdicts, ["verdict_id", "question", "result", "evidence", "effect"]),
                "## Claim Gates",
                markdown_table(gates, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_promoted"]),
                "## Decision Ledger",
                markdown_table(decisions, ["decision_id", "decision", "reason", "effect"]),
                "## Next Target",
                markdown_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
                "## Branch Copies",
                markdown_table(branch_copies, ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
                "## Validation",
                markdown_table(validations, ["check_id", "status", "notes", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    operator = operator_ansatz_rows()
    signs = dimension_sign_rows()
    coercivity = coercivity_audit_rows()
    ghost = ghost_tachyon_rows()
    eligibility = nohair_eligibility_rows()
    bounds = stress_bound_route_rows()
    verdicts = promotion_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["operator_ansatz"], operator)
    write_csv(OUTPUTS["dimension_sign_table"], signs)
    write_csv(OUTPUTS["coercivity_audit"], coercivity)
    write_csv(OUTPUTS["ghost_tachyon_checks"], ghost)
    write_csv(OUTPUTS["nohair_eligibility"], eligibility)
    write_csv(OUTPUTS["stress_bound_route"], bounds)
    write_csv(OUTPUTS["promotion_verdict"], verdicts)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_copies = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validations = validation_rows(sources, operator, signs, coercivity, ghost, eligibility, bounds, verdicts, gates, decisions, next_rows, branch_copies)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, operator, signs, coercivity, ghost, eligibility, bounds, verdicts, gates, decisions, next_rows, branch_copies, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
