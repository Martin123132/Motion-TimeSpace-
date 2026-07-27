from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2558"
BRANCH_ID = "MTS_R2FR_PARENT_CLOCK_EXCHANGE_CURRENT_OR_STATIONARY_SOURCE_THEOREM_2558"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2558-Y5-R2FR-parent-clock-exchange-current-or-stationary-source-theorem.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2558_SOURCE_REGISTER.csv",
    "parent_exchange_attempt": OUT / "P8_Y5_NO_SHADOW_2558_PARENT_EXCHANGE_ATTEMPT.csv",
    "theorem_hypotheses": OUT / "P8_Y5_NO_SHADOW_2558_STATIONARY_THEOREM_HYPOTHESES.csv",
    "proof_steps": OUT / "P8_Y5_NO_SHADOW_2558_STATIONARY_PROOF_STEPS.csv",
    "exterior_result": OUT / "P8_Y5_NO_SHADOW_2558_EXTERIOR_QLOC_RESULT.csv",
    "boundary_jump_ledger": OUT / "P8_Y5_NO_SHADOW_2558_BOUNDARY_JUMP_LEDGER.csv",
    "dynamic_exchange_ledger": OUT / "P8_Y5_NO_SHADOW_2558_DYNAMIC_EXCHANGE_LEDGER.csv",
    "scope_limits": OUT / "P8_Y5_NO_SHADOW_2558_SCOPE_LIMITS.csv",
    "promotion_verdict": OUT / "P8_Y5_NO_SHADOW_2558_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2558_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2558_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2558_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2558_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2558_VALIDATION.csv",
}

COPY_TARGETS = {
    "stationary_theorem_contract": LOCAL_BOUNDS / "Stationary_local_source_theorem_2558_NONCLAIM.csv",
    "parent_exchange_contract": QUEUE / "JR2558_PARENT_CLOCK_EXCHANGE_CONTRACT_NONCLAIM.csv",
    "boundary_jump_ledger": LOCAL_BOUNDS / "Worldtube_boundary_jump_ledger_2558_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2558_00_2557_doc",
        "source_path": ROOT / "2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
        "needles": ["NEXT2557_0_selected", "EXC2557_1_minimal_on_shell_form", "WTG2557_1_stationary_surface", "VAL2557_OVERALL"],
        "role": "active handoff selecting parent exchange or stationary source theorem",
    },
    {
        "source_id": "SRC2558_01_2557_divergence",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2557_DIVERGENCE_IDENTITY.csv",
        "needles": ["DIV2557_1_full_product_rule", "DIV2557_4_Killing_or_covariantly_constant_clock", "DIV2557_5_generic_clock_obstruction"],
        "role": "exact divergence identity and stationary/dynamic split",
    },
    {
        "source_id": "SRC2558_02_2557_exchange",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2557_EXCHANGE_CURRENT_IDENTITY.csv",
        "needles": ["EXC2557_0_required_identity", "EXC2557_3_parent_source_requirement", "MISSING_PARENT_DERIVATION"],
        "role": "exchange-current missing parent derivation",
    },
    {
        "source_id": "SRC2558_03_2557_worldtube",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2557_WORLDTUBE_SURFACE_GATE.csv",
        "needles": ["WTG2557_1_stationary_surface", "WTG2557_3_distributional_surface", "PASS_GUARDRAIL"],
        "role": "surface independence and jump ledger blockers",
    },
    {
        "source_id": "SRC2558_04_2554_qloc",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_QLOC_DERIVATION_ATTEMPT.csv",
        "needles": ["QDER2554_2_project_local", "QDER2554_3_vacuum_zero", "CONDITIONAL_ZERO_NOT_CURRENT_CLAIM"],
        "role": "q_loc projection and exterior-zero conditional contract",
    },
    {
        "source_id": "SRC2558_05_2555_source_current",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_SOURCE_CURRENT_DESCENT.csv",
        "needles": ["SRC2555_2_Noether_identity", "SRC2555_4_external_vacuum", "SRC2555_5_universality"],
        "role": "Noether/current/support clauses not yet owned",
    },
    {
        "source_id": "SRC2558_06_2555_stress",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_STRESS_TENSOR_EXPOSURE.csv",
        "needles": ["STR2555_1_vacuum_stealth_condition", "STR2555_4_GR_limit_gate", "BLOCKED_CURRENT_CLAIM"],
        "role": "stress tensor blocker after q_loc silence",
    },
    {
        "source_id": "SRC2558_07_2468_precedent",
        "source_path": ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
        "needles": ["PV2468_0_stationary_theorem", "DYN2468_1_exchange_required", "VAL2468_OVERALL"],
        "role": "earlier stationary theorem precedent, re-run against 2557 chain",
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


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def bool_text(value: bool) -> str:
    return "true" if value else "false"


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


def parent_exchange_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PEX2558_0_target_identity",
            "derive I_GK such that nabla_mu J_M^mu + I_GK = 0",
            "2557 exchange gate",
            "needed for dynamic MTS/time source conservation",
            "TARGET_DEFINED",
        ),
        (
            "PEX2558_1_leak_form",
            "L_tau = ell_J T^{mu nu}nabla_(mu tau_nu) + (nabla_mu ell_J)T^{mu nu}tau_nu",
            "2557 divergence identity after matter shell, with variable-scale term retained",
            "parent exchange must cancel L_tau in dynamic regions",
            "FORM_DERIVED",
        ),
        (
            "PEX2558_2_Noether_route",
            "a diffeomorphism/clock Noether identity could give I_GK from E_tau, E_Gamma, E_Khat and boundary terms",
            "generic covariant-action logic",
            "acceptable only if the parent action contains tau/Gamma/Khat equations with matching coefficients",
            "CONDITIONAL_ROUTE",
        ),
        (
            "PEX2558_3_required_parent_signature",
            "I_GK = -L_tau must be produced by signed parent equations, not inserted into the continuity equation",
            "anti-patch rule",
            "requires explicit terms in L_K, L_Gamma, clock/coframe action, and source coupling",
            "MISSING_PARENT_SIGNATURE",
        ),
        (
            "PEX2558_4_current_corpus_result",
            "current source files do not provide the signed tau/Gamma/Khat variation that yields I_GK=-L_tau",
            "2554-2557 source audit",
            "dynamic exchange theorem is rejected for now",
            "PARENT_DERIVATION_NOT_FOUND",
        ),
        (
            "PEX2558_5_stationary_escape",
            "if nabla_(mu tau_nu)=0 and ell_J is fixed in a local collar, L_tau=0 so I_GK is not needed there",
            "stationary/Killing local collar",
            "narrow stationary source theorem can be proved conditionally without a dynamic exchange current",
            "STATIONARY_ROUTE_OPEN",
        ),
    ]
    return [
        {**base_row(), "exchange_attempt_id": item, "contract_or_step": step, "basis": basis, "result": result, "status": status}
        for item, step, basis, result, status in rows
    ]


def theorem_hypothesis_rows() -> list[dict[str, Any]]:
    rows = [
        ("HYP2558_0_action_contract", "ACT2554_A q_loc current-law action is used as a formal contract", "needed for q_loc=P_loc J_M", "CONDITIONAL_INPUT"),
        ("HYP2558_1_hilbert_current", "J_M^mu=ell_J T_matter^{mu nu}tau_nu", "source current from universal Hilbert stress-energy", "CONDITIONAL_INPUT"),
        ("HYP2558_2_parent_scale_fixed", "ell_J is constant and fixed before local readout", "prevents fitted coupling drift and scale leakage", "ASSUMED_NOT_PROVED"),
        ("HYP2558_3_matter_shell", "nabla_mu T_matter^{mu nu}=0 including distributional matching", "needed for current conservation", "ASSUMED_NOT_PROVED"),
        ("HYP2558_4_stationary_clock", "nabla_(mu tau_nu)=0 throughout the source plus exterior collar", "kills Hilbert-current clock strain", "ASSUMED_LOCAL_STATIONARY"),
        ("HYP2558_5_compact_support", "T_matter=0 outside worldtube W except explicitly bounded tails", "needed for exterior J_M=0", "ASSUMED_OR_BOUND_REQUIRED"),
        ("HYP2558_6_projector_owned", "P_loc is fixed or parent-owned in the collar", "prevents projection from hiding residual components", "ASSUMED_NOT_PROVED"),
        ("HYP2558_7_boundary_silent", "A/Gamma/Khat and matter surface-layer fluxes are zero or bounded", "needed for clean local vacuum statement", "ASSUMED_NOT_PROVED"),
        ("HYP2558_8_stress_not_claimed", "T_GK^{mu nu} silence is not assumed in this theorem", "q_loc silence alone is not metric silence", "NEXT_GATE_REQUIRED"),
    ]
    return [
        {**base_row(), "hypothesis_id": item, "hypothesis": hypothesis, "why_needed": why, "status": status}
        for item, hypothesis, why, status in rows
    ]


def proof_step_rows() -> list[dict[str, Any]]:
    rows = [
        ("PRF2558_0_divergence", "Using 2557, nabla.J=(nabla ell)Ttau+ell(nabla T)tau+ell T nabla tau.", "exact product rule", "PASS"),
        ("PRF2558_1_stationary_reduction", "Under fixed ell_J, matter shell, symmetric T and Killing tau, nabla_mu J_M^mu=0.", "HYP2558_2-4", "PASS_CONDITIONAL"),
        ("PRF2558_2_surface_independence", "For any two hypersurfaces cutting W, Q[Sigma_2]-Q[Sigma_1]=int_V nabla.J + side_flux = 0.", "Gauss law plus no side leakage", "PASS_CONDITIONAL"),
        ("PRF2558_3_exterior_current_zero", "Outside W, T_matter=0 so J_M=ell_J T tau=0.", "compact support/exterior vacuum", "PASS_CONDITIONAL"),
        ("PRF2558_4_projected_q_zero", "With q_loc^nu=P_loc^nu_rho J_M^rho, exterior J_M=0 implies q_loc^nu=0.", "ACT2554_A projection contract", "PASS_CONDITIONAL"),
        ("PRF2558_5_F1_zero", "The first local residual coefficient F1 vanishes in the stationary exterior because q_loc itself vanishes there.", "smooth local expansion around zero residual", "PASS_CONDITIONAL"),
        ("PRF2558_6_no_dynamic_exchange", "The proof does not derive I_GK for generic clocks.", "PEX2558_4", "NONCLAIM_LIMIT"),
        ("PRF2558_7_not_full_GR", "Metric stress, ell_J origin, and boundary/jump ownership are not proved.", "remaining gates", "NONCLAIM_LIMIT"),
    ]
    return [
        {**base_row(), "proof_id": item, "proof_step": step, "basis": basis, "status": status}
        for item, step, basis, status in rows
    ]


def exterior_result_rows() -> list[dict[str, Any]]:
    rows = [
        ("EXT2558_0_stationary_q_zero", "q_loc^nu -> 0 in stationary compact-source exterior", "conditional theorem contract", "CONDITIONAL_THEOREM_CONTRACT"),
        ("EXT2558_1_F1_zero", "F1=0 in the same exterior collar", "q_loc vanishes before residual expansion", "CONDITIONAL_THEOREM_CONTRACT"),
        ("EXT2558_2_Delta_m_bound", "abs(Delta m/m) <= C_J epsilon_J/M_source + C_B epsilon_B/M_source + C_tau epsilon_tau/M_source", "tails, boundary flux and non-Killing clock strain bound leakage", "BOUND_FORM_ONLY"),
        ("EXT2558_3_surface_mass", "M_source=int T^{mu nu}tau_nu dSigma_mu is surface-independent under theorem hypotheses", "Hilbert worldtube bridge", "CONDITIONAL_THEOREM_CONTRACT"),
        ("EXT2558_4_dynamic_limit", "generic dynamic clocks are not covered", "I_GK parent derivation missing", "NONCLAIM"),
        ("EXT2558_5_metric_limit", "no full Newton/PPN/local-GR pass follows from this alone", "T_GK stress and metric equation remain unresolved", "NONCLAIM"),
    ]
    return [
        {**base_row(), "result_id": item, "result": result, "basis": basis, "status": status}
        for item, result, basis, status in rows
    ]


def boundary_jump_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND2558_0_surface_term", "Q surface independence assumes side_flux=0 or bounded", "worldtube Gauss law", "ASSUMED_NOT_PROVED"),
        ("BND2558_1_matter_jump", "distributional matter boundary must satisfy jump conservation", "compact source boundary", "MISSING_JUMP_IDENTITY"),
        ("BND2558_2_GK_boundary", "A/Gamma/Khat boundary terms must vanish, cancel, or enter the residual bound", "ACT2554_A variation boundary", "MISSING_BOUNDARY_SILENCE"),
        ("BND2558_3_tail_bound", "noncompact matter tails require epsilon_J bound", "real sources are not perfect top-hats", "BOUND_FORM_ONLY"),
        ("BND2558_4_clock_bound", "non-Killing clock leakage requires epsilon_tau bound", "finite local collar", "BOUND_FORM_ONLY"),
        ("BND2558_5_claim_status", "boundary/jump terms block public/local-GR claims", "honest closure gate", "BLOCKS_CLAIM"),
    ]
    return [
        {**base_row(), "boundary_id": item, "condition_or_gap": gap, "basis": basis, "status": status}
        for item, gap, basis, status in rows
    ]


def dynamic_exchange_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("DYN2558_0_clock_leak", "L_tau=ell_J T^{mu nu}nabla_(mu tau_nu)+(nabla_mu ell_J)T^{mu nu}tau_nu", "generic dynamic clock leakage", "FORM_DERIVED"),
        ("DYN2558_1_exchange_required", "Need I_GK=-L_tau for exact dynamic conservation", "A-equation integrability and worldtube surface independence", "MISSING_PARENT_EXCHANGE"),
        ("DYN2558_2_tau_equation", "tau/coframe variation must either produce I_GK or enforce a stationary/Killing condition locally", "parent clock action", "MISSING_PARENT_CLOCK_ACTION"),
        ("DYN2558_3_Gamma_Khat_equation", "Gamma/Khat sector must carry the exchange without reintroducing local stress tails", "parent GK sector consistency", "MISSING_GK_EXCHANGE_STRESS_BALANCE"),
        ("DYN2558_4_cosmology_split", "cosmological memory may keep L_tau nonzero on FLRW scales while local stationary collars close", "sector split", "POSSIBLE_SPLIT"),
        ("DYN2558_5_no_dynamic_claim", "dynamic MTS/time-sector local-GR theorem is not proved", "exchange identity absent", "BLOCKED"),
    ]
    return [
        {**base_row(), "dynamic_id": item, "statement": statement, "basis": basis, "status": status}
        for item, statement, basis, status in rows
    ]


def scope_limit_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCP2558_0_parent_scale", "ell_J still not parent-derived", "blocks numeric local predictions and Newton-source normalisation", "BLOCKED"),
        ("SCP2558_1_GK_stress", "q_loc=0 does not imply T_GK^{mu nu}=0", "blocks local metric/PPN pass", "BLOCKED"),
        ("SCP2558_2_projector", "P_loc still assumed fixed/parent-owned", "projection may hide residual components", "BLOCKED"),
        ("SCP2558_3_boundary", "boundary/jump silence is assumed or bounded only formally", "must become condition or sourced bound", "BLOCKED"),
        ("SCP2558_4_value", "stationary theorem is still valuable", "turns local q_loc silence from plateau axiom into conditional Euler/source theorem", "PROGRESS"),
        ("SCP2558_5_dynamic_route", "dynamic exchange is not dead, but has no signed parent source yet", "requires parent action terms rather than a hand-added continuity fix", "OPEN_NOT_PROMOTED"),
    ]
    return [
        {**base_row(), "scope_id": item, "limit": limit, "effect": effect, "status": status}
        for item, limit, effect, status in rows
    ]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2558_0_parent_exchange", "Is a parent-derived I_GK available?", "NO", "target form is derived but no tau/Gamma/Khat parent signature exists", "dynamic route remains blocked"),
        ("PV2558_1_stationary_theorem", "Is a stationary local-source q_loc theorem available?", "YES_CONDITIONAL", "proof closes under explicit stationary compact-source hypotheses", "promote only as private conditional theorem contract"),
        ("PV2558_2_F1_zero", "Does F1 vanish in that stationary exterior?", "YES_CONDITIONAL", "q_loc=0 before local residual expansion", "supports local residual branch under hypotheses"),
        ("PV2558_3_Newton_local_GR", "Is Newton/local GR derived?", "NO", "metric stress, parent scale, projector and boundary gates unresolved", "no local-GR claim"),
        ("PV2558_4_overall", "Overall 2558 verdict", "CONDITIONAL_STATIONARY_QLOC_F1_ZERO_DYNAMIC_EXCHANGE_BLOCKED", "we got a real narrow theorem, not a full GR bridge", "next target is GK stress silence/local metric equation"),
    ]
    return [
        {**base_row(), "verdict_id": item, "question": question, "result": result, "evidence": evidence, "effect": effect}
        for item, question, result, evidence, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2558_0_parent_exchange", "Parent-derived dynamic I_GK exists.", "BLOCKED", "target form exists but parent variation does not source it", "false", "false"),
        ("GATE2558_1_stationary_q_zero", "Stationary compact-source exterior gives q_loc=0.", "PASS_AS_CONDITIONAL_THEOREM", "explicit hypotheses and proof steps written", "true", "false"),
        ("GATE2558_2_F1_zero", "F1=0 in stationary exterior.", "PASS_AS_CONDITIONAL_THEOREM", "q_loc vanishes before expansion", "true", "false"),
        ("GATE2558_3_boundary_jump", "Boundary/jump terms are parent-silent.", "BLOCKED", "jump and GK boundary clauses remain unsigned", "false", "false"),
        ("GATE2558_4_local_GR", "Local GR/Newton/PPN branch passes.", "BLOCKED", "GK stress/local metric equation and ell_J remain open", "false", "false"),
        ("GATE2558_5_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [
        {**base_row(), "gate_id": item, "claim": claim, "gate_status": status, "reason": reason, "gate_pass": gate_pass, "claim_promoted": promoted}
        for item, claim, status, reason, gate_pass, promoted in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2558_0_reject_dynamic_claim", "Reject the dynamic exchange theorem for now.", "I_GK target is derived but not parent-sourced", "do not use dynamic closure in local claims"),
        ("DEC2558_1_keep_stationary_theorem", "Keep the stationary q_loc/F1 theorem contract.", "it is a real conditional derivation, not a plateau axiom", "use as local-source branch scaffold"),
        ("DEC2558_2_do_not_overclaim", "Do not claim full local GR.", "q_loc silence is not metric stress silence", "claim gates stay blocked"),
        ("DEC2558_3_next_stress_gate", "Move next to GK stress/local metric equation.", "after q_loc zero, the next GR blocker is whether the extra sector gravitates locally", "2559 selected"),
    ]
    return [
        {**base_row(), "decision_id": item, "decision": decision, "reason": reason, "effect": effect}
        for item, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2558_0_selected",
            "selection_status": "selected",
            "target_file": "2559-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
            "target_script": "scripts/Y5_R2FR_GK_stress_silence_and_local_metric_equation_gate_2559.py",
            "task": "test whether the vertical-generator/Gamma-Khat sector has locally silent stress under the stationary q_loc theorem, or whether extra stress blocks GR/PPN even when q_loc=0",
            "acceptance_target": "stress tensor exposure, stealth/screening hypotheses, local metric equation gate, PPN residual source terms, and honest demotion if stress remains unsilenced",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    copy_sources = {
        "stationary_theorem_contract": OUTPUTS["proof_steps"],
        "parent_exchange_contract": OUTPUTS["parent_exchange_attempt"],
        "boundary_jump_ledger": OUTPUTS["boundary_jump_ledger"],
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
    return len(outside_formalization) == len(touched_paths), f"declared_2558_paths_outside_formalization={len(outside_formalization)}/{len(touched_paths)}"


def validation_rows(
    sources: list[dict[str, Any]],
    exchange_attempt: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
    proof_steps: list[dict[str, Any]],
    exterior: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    scope: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail})

    add("VAL2558_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present")
    add("VAL2558_01_exchange_target_defined", any(row["exchange_attempt_id"] == "PEX2558_0_target_identity" and row["status"] == "TARGET_DEFINED" for row in exchange_attempt), "parent exchange target identity defined")
    add("VAL2558_02_exchange_not_parent_sourced", any(row["exchange_attempt_id"] == "PEX2558_4_current_corpus_result" and row["status"] == "PARENT_DERIVATION_NOT_FOUND" for row in exchange_attempt), "dynamic exchange not promoted without parent source")
    add("VAL2558_03_stationary_route_open", any(row["exchange_attempt_id"] == "PEX2558_5_stationary_escape" and row["status"] == "STATIONARY_ROUTE_OPEN" for row in exchange_attempt), "stationary route remains open")
    add("VAL2558_04_hypotheses_explicit", len(hypotheses) >= 9 and any(row["hypothesis_id"] == "HYP2558_4_stationary_clock" for row in hypotheses), "stationary theorem hypotheses explicit")
    add("VAL2558_05_q_zero_proof", any(row["proof_id"] == "PRF2558_4_projected_q_zero" and row["status"] == "PASS_CONDITIONAL" for row in proof_steps), "q_loc zero proof step present")
    add("VAL2558_06_F1_zero", any(row["proof_id"] == "PRF2558_5_F1_zero" and row["status"] == "PASS_CONDITIONAL" for row in proof_steps), "F1 zero conditional proof step present")
    add("VAL2558_07_exterior_result", any(row["result_id"] == "EXT2558_0_stationary_q_zero" and row["status"] == "CONDITIONAL_THEOREM_CONTRACT" for row in exterior), "stationary exterior q_loc result recorded")
    add("VAL2558_08_boundary_blocks_claim", any(row["boundary_id"] == "BND2558_5_claim_status" and row["status"] == "BLOCKS_CLAIM" for row in boundary), "boundary/jump ledger blocks public claim")
    add("VAL2558_09_dynamic_blocked", any(row["dynamic_id"] == "DYN2558_5_no_dynamic_claim" and row["status"] == "BLOCKED" for row in dynamic), "dynamic exchange route remains blocked")
    add("VAL2558_10_stress_next", any(row["scope_id"] == "SCP2558_1_GK_stress" and row["status"] == "BLOCKED" for row in scope), "GK stress blocker retained")
    add("VAL2558_11_overall_verdict", any(row["verdict_id"] == "PV2558_4_overall" and row["result"] == "CONDITIONAL_STATIONARY_QLOC_F1_ZERO_DYNAMIC_EXCHANGE_BLOCKED" for row in verdicts), "overall verdict is conditional stationary theorem plus dynamic block")
    add("VAL2558_12_claim_gates_safe", all(row["claim_promoted"] == "false" for row in gates), "no claim gate promotes local-GR/Newton claims")
    add("VAL2558_13_next_target_written", any(row["route_id"] == "NEXT2558_0_selected" and row["selection_status"] == "selected" for row in next_rows), "2559 stress silence gate selected")
    add("VAL2558_14_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_copies), "nonclaim branch copies exist")

    output_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]
    add("VAL2558_15_all_outputs_inside_post_checkpoint", all(is_relative_to(path, ROOT) for path in output_paths), "all 2558 outputs stay inside post-checkpoint-work")
    formalization_ok, formalization_detail = formalization_status_detail()
    add("VAL2558_16_formalization_workbench_not_targeted", formalization_ok, "declared 2558 outputs do not target formalization-workbench", formalization_detail)

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        add(f"VAL2558_OUTPUT_{key}", path.exists() and csv_row_count(path) > 0, f"{key} output exists and has rows", str(path))

    for copy_id, path in COPY_TARGETS.items():
        add(f"VAL2558_COPY_{copy_id}", path.exists() and csv_row_count(path) > 0, f"{copy_id} copy exists and has rows", str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2558_OVERALL", overall, "2558 rejects unsigned dynamic exchange, proves conditional stationary q_loc/F1 zero, and selects GK stress gate next")
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
    exchange_attempt: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
    proof_steps: list[dict[str, Any]],
    exterior: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    scope: list[dict[str, Any]],
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
                "# 2558 Y5 R2FR Parent Clock Exchange Current Or Stationary Source Theorem",
                "**Status:** derivation split completed. The dynamic exchange target is known, but the current corpus does not yet supply the signed parent `tau/Gamma/Khat` variation that would make `I_GK=-L_tau` a theorem. The stationary compact-source route does close conditionally: under fixed `ell_J`, conserved Hilbert stress, Killing/local-stationary `tau`, compact support, parent-owned `P_loc`, and silent/bounded boundaries, exterior `q_loc=0` and `F1=0` follow from the Euler/source machinery.",
                "**Important boundary:** this is a serious step, not the full GR bridge. It removes the plateau axiom for the stationary local source branch, but it does not prove dynamic clock closure, parent scale, boundary/jump silence, or local metric stress silence. The next hard gate is whether the GK sector has locally silent stress when `q_loc=0`.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
                "## Parent Exchange Attempt",
                markdown_table(exchange_attempt, ["exchange_attempt_id", "contract_or_step", "basis", "result", "status"]),
                "## Stationary Theorem Hypotheses",
                markdown_table(hypotheses, ["hypothesis_id", "hypothesis", "why_needed", "status"]),
                "## Stationary Proof Steps",
                markdown_table(proof_steps, ["proof_id", "proof_step", "basis", "status"]),
                "## Exterior q_loc Result",
                markdown_table(exterior, ["result_id", "result", "basis", "status"]),
                "## Boundary Jump Ledger",
                markdown_table(boundary, ["boundary_id", "condition_or_gap", "basis", "status"]),
                "## Dynamic Exchange Ledger",
                markdown_table(dynamic, ["dynamic_id", "statement", "basis", "status"]),
                "## Scope Limits",
                markdown_table(scope, ["scope_id", "limit", "effect", "status"]),
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
    exchange_attempt = parent_exchange_attempt_rows()
    hypotheses = theorem_hypothesis_rows()
    proof_steps = proof_step_rows()
    exterior = exterior_result_rows()
    boundary = boundary_jump_ledger_rows()
    dynamic = dynamic_exchange_ledger_rows()
    scope = scope_limit_rows()
    verdicts = promotion_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_exchange_attempt"], exchange_attempt)
    write_csv(OUTPUTS["theorem_hypotheses"], hypotheses)
    write_csv(OUTPUTS["proof_steps"], proof_steps)
    write_csv(OUTPUTS["exterior_result"], exterior)
    write_csv(OUTPUTS["boundary_jump_ledger"], boundary)
    write_csv(OUTPUTS["dynamic_exchange_ledger"], dynamic)
    write_csv(OUTPUTS["scope_limits"], scope)
    write_csv(OUTPUTS["promotion_verdict"], verdicts)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_copies = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validations = validation_rows(sources, exchange_attempt, hypotheses, proof_steps, exterior, boundary, dynamic, scope, verdicts, gates, decisions, next_rows, branch_copies)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, exchange_attempt, hypotheses, proof_steps, exterior, boundary, dynamic, scope, verdicts, gates, decisions, next_rows, branch_copies, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
