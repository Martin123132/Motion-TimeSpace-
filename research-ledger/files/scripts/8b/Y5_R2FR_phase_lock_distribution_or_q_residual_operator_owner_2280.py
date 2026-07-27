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

BRANCH_ID = "MTS_R2FR_PHASE_LOCK_OR_Q_OPERATOR_OWNER_2280"
DOC = ROOT / "2280-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2280_00_2279_doc",
        "source_key": "2279_doc",
        "source_path": ROOT / "2279-Y5-R2FR-nonlinear-phase-exchange-coefficients-or-q-residual-operator.md",
        "needles": ["NEXT2279_0_primary", "NO_DIRECTED_EXCHANGE_FROM_RANDOM_PHASE_AVERAGE", "Q_OPERATOR_BACKSTOP_STAGED"],
        "role": "handoff selecting phase-lock distribution or q residual operator owner",
    },
    {
        "source_id": "SRC2280_01_2279_validation",
        "source_key": "2279_validation",
        "source_path": OUT / "P8_Y5_BRR545_2279_VALIDATION.csv",
        "needles": ["VAL2279_OVERALL", "PASS"],
        "role": "confirms 2279 passed before 2280 starts",
    },
    {
        "source_id": "SRC2280_02_2278_condition",
        "source_key": "2278_exchange_condition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2278_EXACT_EXCHANGE_CONDITION.csv",
        "needles": ["EXC2278_2_tangent_lock", "EXACT_WEIGHT_EXCHANGE_TARGET"],
        "role": "exact q-zero preservation condition",
    },
    {
        "source_id": "SRC2280_03_2279_projection",
        "source_key": "2279_nonlinear_projection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2279_NONLINEAR_PHASE_PROJECTION_AUDIT.csv",
        "needles": ["NPP2279_2_independent_phase_zero", "NPP2279_3_phase_locked_route"],
        "role": "phase projection audit that rejects random averaging and leaves locked distribution open",
    },
    {
        "source_id": "SRC2280_04_2279_q_operator",
        "source_key": "2279_q_operator_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2279_Q_RESIDUAL_OPERATOR_TEMPLATE.csv",
        "needles": ["QOP2279_0_transport_relaxation", "QOP2279_1_elliptic_stiffness"],
        "role": "operator templates needing a parent owner",
    },
    {
        "source_id": "SRC2280_05_fundamental_action",
        "source_key": "fundamental_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "λ |ψ|^{n−1}", "n = 4/3"],
        "role": "current scalar psi action; no explicit q-stiffness or phase-lock term found",
    },
    {
        "source_id": "SRC2280_06_axio_phase",
        "source_key": "axio_phase_dynamics",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "field-theory" / "axio-stable-three-body-bound-states-in-a-dissipative-field-theory.md",
        "needles": ["phase topology", "nonlinear phase dynamics", "curvature saturation"],
        "role": "evidence that locked phase structures appear in corpus, but not a local-GR derivation",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2280_SOURCE_REGISTER.csv",
    "invariance_law": OUT / "P8_Y5_PARENT_QLOC_2280_Q_INVARIANT_MANIFOLD_LAW.csv",
    "phase_lock_owner": OUT / "P8_Y5_PARENT_QLOC_2280_PHASE_LOCK_OWNER_AUDIT.csv",
    "q_operator_owner": OUT / "P8_Y5_PARENT_QLOC_2280_Q_OPERATOR_OWNER_AUDIT.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_2280_MINIMAL_PARENT_CONTRACT.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2280_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2280_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2280_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2280_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2280_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2280_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_phase_lock": QUEUE / "JR2280_PHASE_LOCK_OWNER_AUDIT_NONCLAIM.csv",
    "queue_contract": QUEUE / "JR2280_Q_STIFFNESS_PARENT_CONTRACT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_phase_lock_or_q_operator_refusal_2280.csv",
    "beta_docs": BETA_DOCS / "RAB_Q_INVARIANT_MANIFOLD_2280_NONCLAIM.csv",
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": path,
                "exists": path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def invariance_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "QIM2280_0_definition",
            "object": "local residual coordinate",
            "formula": "q := C_R - F(C_T), with F(C_T)=C_T/(1-C_T)",
            "derived_condition": "Dq = DC_R - DC_T/(1-C_T)^2",
            "status": "DERIVED_FROM_2278_EXACT_EXCHANGE_CONDITION",
            "valid_for_claim": False,
        },
        {
            "law_id": "QIM2280_1_invariant_manifold",
            "object": "q=0 local-GR manifold",
            "formula": "q=0 is preserved iff Dq|_{q=0}=0",
            "derived_condition": "E_R - F'(C_T) E_T + B_q = 0 on q=0",
            "status": "NECESSARY_AND_SUFFICIENT_TANGENCY_CONDITION",
            "valid_for_claim": False,
        },
        {
            "law_id": "QIM2280_2_stable_manifold",
            "object": "finite residual branch",
            "formula": "Dq = -kappa_q q + S_q + higher_order(q^2)",
            "derived_condition": "if kappa_q>=K>0 then q decays up to sourced residuals",
            "status": "CONDITIONAL_STABILITY_LAW",
            "valid_for_claim": False,
        },
        {
            "law_id": "QIM2280_3_score_rule",
            "object": "local-GR claim gate",
            "formula": "local_GR_score_allowed only if tangency or coercive residual operator is parent-signed",
            "derived_condition": "phase exchange alone is insufficient unless it proves QIM2280_1",
            "status": "CLAIM_DISCIPLINE_RULE",
            "valid_for_claim": False,
        },
    ]


def phase_lock_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PLO2280_0_uniform_phases",
            "candidate_owner": "independent random phase distribution",
            "test": "P(Phi)=constant gives <N(psi) sin(phi_I)>=0",
            "result": "REJECTED_AS_OWNER",
            "reason": "2279 parity result: no directed exchange, so no tangency mechanism",
            "missing_inputs": "none; this route is closed under the stated symmetry",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PLO2280_1_even_locked_distribution",
            "candidate_owner": "phase-locked but time-reversal/even distribution",
            "test": "P_locked(Phi)=P_locked(-Phi)",
            "result": "REJECTED_AS_DIRECTED_OWNER",
            "reason": "odd sine/action projection still cancels unless the distribution contains a lagged/odd component",
            "missing_inputs": "odd phase component or dissipative lag",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PLO2280_2_odd_lag_distribution",
            "candidate_owner": "lagged locked-phase distribution",
            "test": "P_locked = P_even + epsilon_A sin(phi_A) + cross terms",
            "result": "POSSIBLE_BUT_UNSOURCED",
            "reason": "can generate nonzero E_A, but must also satisfy E_R-F'(C_T)E_T+B_q=0 for all relevant local states",
            "missing_inputs": "parent equation for epsilon_A; projectors P_T/P_R; smoothing kernel; q-feedback or boundary law",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PLO2280_3_boundary_memory_kernel",
            "candidate_owner": "boundary-correlated memory kernel",
            "test": "E_A = integral K_A(t-s,boundary) N(psi(s)) ds",
            "result": "POSSIBLE_BUT_UNSOURCED",
            "reason": "a delayed kernel can break the even-phase cancellation, but no kernel owner or positivity law is present",
            "missing_inputs": "kernel definition; causality; sign/positivity; source path; local limit",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PLO2280_4_q_feedback_lock",
            "candidate_owner": "q-dependent lock distribution",
            "test": "P_locked[q] chosen so Dq=-kappa_q q",
            "result": "RECLASSIFIED_AS_Q_OPERATOR",
            "reason": "once the distribution depends on q to enforce tangency, the real owner is a q residual/stiffness operator, not free phase locking",
            "missing_inputs": "parent q-sector or Onsager/dissipation law",
            "valid_for_claim": False,
        },
    ]


def q_operator_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "QOO2280_0_current_scalar_action",
            "candidate_owner": "current A_MTS[psi] scalar action",
            "operator_generated": "psi wave/nonlinear equation only",
            "ownership_result": "NO_EXPLICIT_Q_OWNER_FOUND",
            "reason": "the action contains kinetic, damping-like gamma psi dot(psi), and lambda |psi|^n terms, but no q=C_R-F(C_T) stiffness, multiplier, or residual transport term",
            "required_for_claim": "derive q operator from variation or amend parent action",
            "valid_for_claim": False,
        },
        {
            "owner_id": "QOO2280_1_constraint_multiplier",
            "candidate_owner": "Lagrange multiplier eta_q q",
            "operator_generated": "q=0 exactly",
            "ownership_result": "VIABLE_PARENT_EXTENSION_NOT_SOURCED",
            "reason": "would make the local-GR branch exact, but risks smuggling the plateau as an axiom unless eta_q follows from quotient/regularity principle",
            "required_for_claim": "source eta_q from parent symmetry or variational regularity",
            "valid_for_claim": False,
        },
        {
            "owner_id": "QOO2280_2_q_stiffness_sector",
            "candidate_owner": "S_q=-1/2 integral sqrt(-g_eff)[Z_q nabla q nabla q + M_q^2 q^2]",
            "operator_generated": "L_q q = -nabla_i(Z_q nabla^i q)+M_q^2 q",
            "ownership_result": "BEST_CONDITIONAL_ROUTE",
            "reason": "gives a real coercive residual operator and finite q bounds if Z_q>0, M_q^2>0, boundary conditions and observable map are sourced",
            "required_for_claim": "derive Z_q and M_q^2 from parent regularity/coarse-graining, not fit by hand",
            "valid_for_claim": False,
        },
        {
            "owner_id": "QOO2280_3_onsager_relaxation",
            "candidate_owner": "dissipative gradient flow Dq=-M_q delta F_q/delta q",
            "operator_generated": "Dq + kappa_q q = S_q",
            "ownership_result": "VIABLE_IF_DISSIPATION_PRINCIPLE_EXISTS",
            "reason": "fits the existing memory/dissipation motif but requires a signed entropy/Onsager principle",
            "required_for_claim": "derive mobility M_q>=0 and free-energy F_q from parent motion-time coarse graining",
            "valid_for_claim": False,
        },
        {
            "owner_id": "QOO2280_4_boundary_silence",
            "candidate_owner": "boundary/local projection silence",
            "operator_generated": "B_q=0",
            "ownership_result": "UNSIGNED",
            "reason": "even a q-stiffness route needs boundary terms to vanish or be bounded",
            "required_for_claim": "no-flux theorem or explicit boundary residual bound",
            "valid_for_claim": False,
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "MPC2280_0_no_free_phase_claim",
            "requirement": "Do not claim phase locking closes local GR unless the phase distribution is derived.",
            "mathematical_form": "P_locked must be sourced and must make E_R-F'(C_T)E_T+B_q=0 on q=0",
            "current_status": "UNSIGNED",
            "next_evidence_needed": "parent phase-lock equation, projector map, and coefficient calculation",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MPC2280_1_q_sector",
            "requirement": "If phase locking is not derived, add/derive a q-stiffness or q-relaxation owner.",
            "mathematical_form": "S_q=-1/2 integral [Z_q |nabla q|^2 + M_q^2 q^2] or Dq=-M_q delta F_q/delta q",
            "current_status": "BEST_CONDITIONAL_PARENT_COMPLETION",
            "next_evidence_needed": "derive Z_q>0/M_q^2>0 or mobility/free energy from regularity/coarse-graining",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MPC2280_2_gr_limit",
            "requirement": "Show the q-sector decouples or becomes silent in the GR/Newton limit.",
            "mathematical_form": "q->0 and R_local=P_obs q below PPN/R10/clock/orbital bounds",
            "current_status": "MISSING_OBSERVABLE_PROJECTION",
            "next_evidence_needed": "PPN/R10/clock/orbital projection matrices and bounds",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MPC2280_3_no_smuggling",
            "requirement": "A q-stiffness term must be motivated by parent geometry, not inserted only to pass local tests.",
            "mathematical_form": "Z_q,M_q^2 derived from quotient regularity, covariance positivity, or entropy production",
            "current_status": "PHYSICS_JUSTIFICATION_REQUIRED",
            "next_evidence_needed": "2281 derivation attempt",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2280_0_invariant_manifold_law",
            "claim": "q=0 preservation requires E_R-F'(C_T)E_T+B_q=0",
            "gate_pass": True,
            "reason": "direct derivative of q=C_R-C_T/(1-C_T)",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2280_1_phase_lock_derives_local_gr",
            "claim": "phase locking derives the local GR branch",
            "gate_pass": False,
            "reason": "non-even locked distribution/projectors are not sourced and tangency is not proven",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2280_2_current_action_owns_q_operator",
            "claim": "current scalar action already owns kappa_q/L_q/G_q",
            "gate_pass": False,
            "reason": "no explicit q-stiffness, multiplier, or q-gradient-flow term is present in the cited action",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2280_3_q_stiffness_route",
            "claim": "q-stiffness sector is the cleanest parent-completion candidate",
            "gate_pass": True,
            "reason": "it directly owns L_q and makes local residual bounds mathematically checkable, but remains a conditional extension",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2280_4_local_gr",
            "claim": "derived local GR/Newton limit",
            "gate_pass": False,
            "reason": "q-sector coefficients, boundary terms, and observable projections remain unsourced",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2280_0_phase_lock_claim",
            "attempted_claim": "Locked nonlinear phases close the exact q-zero exchange law.",
            "runner_result": "BLOCKED",
            "blocked_by": "phase-lock distribution/projectors and tangency coefficients are not parent-derived",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2280_1_existing_action_claim",
            "attempted_claim": "The existing scalar action already gives the q residual operator.",
            "runner_result": "BLOCKED",
            "blocked_by": "no q-stiffness, q-multiplier, Onsager mobility, or boundary silence theorem found in cited action",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2280_2_local_gr_claim",
            "attempted_claim": "MTS has derived local GR/Newton mechanics.",
            "runner_result": "BLOCKED",
            "blocked_by": "q invariant manifold has a precise law, but no parent-signed owner yet",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2280_0_real_gain",
            "decision": "LOCAL_GAP_RECAST_AS_INVARIANT_MANIFOLD_OWNER",
            "reason": "the problem is no longer vague coupling; it is who owns Dq=0 or Dq=-kappa_q q.",
            "next_action": "derive q-stiffness/relaxation from parent regularity or prove phase-lock tangency.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2280_1_phase_lock_status",
            "decision": "PHASE_LOCK_ONLY_ROUTE_DEMOTED",
            "reason": "nonzero exchange is not enough; it must satisfy exact q tangency across the local branch.",
            "next_action": "keep phase locking as a possible source term, not as the current owner of local GR.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2280_2_best_route",
            "decision": "Q_STIFFNESS_OR_ONSAGER_OWNER_IS_BEST_ROUTE",
            "reason": "it is the least hand-wavy way to make q=0 invariant/stable and to compute residual bounds.",
            "next_action": "attempt to derive S_q from covariance regularity/coarse-grained action.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2280_3_next",
            "decision": "Q_STIFFNESS_PARENT_SECTOR_NEXT",
            "reason": "this is the shortest path to a derivable local GR branch or a clean no-go.",
            "next_action": "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2280_0_primary",
            "next_target": "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md",
            "script": "scripts/Y5_R2FR_q_stiffness_parent_sector_or_no_go_2281.py",
            "objective": "derive a parent q-stiffness or Onsager relaxation sector from covariance regularity/coarse-graining, or prove that adding it would be closure-only",
            "selection_status": "selected",
            "success_condition": "Z_q/M_q^2 or kappa_q is parent-signed with positivity, boundary silence, and observable projection gates; otherwise local branch remains nonclaim",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_phase_lock": OUTPUTS["phase_lock_owner"],
        "queue_contract": OUTPUTS["parent_contract"],
        "branch_wep": OUTPUTS["refusal"],
        "beta_docs": OUTPUTS["invariance_law"],
    }
    return [
        {
            "copy_id": copy_id,
            "source_path": source_by_copy[copy_id],
            "target_path": target,
            "target_exists": target.exists(),
            "target_parses": csv_parses(target) if target.exists() else False,
            "reason": "branch copy for q invariant-manifold and q-stiffness follow-up work",
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def false_flag_check() -> bool:
    guarded_fields = {"score_ready", "score_eligible", "accepted_ready", "valid_for_claim", "claim_allowed"}
    for path in generated_csvs():
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for field in guarded_fields.intersection(row):
                    if row[field].strip().lower() == "true":
                        return False
                if "gate_pass" in row and row.get("valid_for_claim", "").strip().lower() == "true":
                    return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_ok = all(row["exists"] for row in source_rows)
    needles_ok = all(row["needles_present"] for row in source_rows)

    prior_text = read_text(OUT / "P8_Y5_BRR545_2279_VALIDATION.csv")
    prior_ok = "VAL2279_OVERALL" in prior_text and "PASS" in prior_text

    laws = invariance_law_rows()
    phase = phase_lock_owner_rows()
    owners = q_operator_owner_rows()
    contract = parent_contract_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()

    invariant_law = any(row["law_id"] == "QIM2280_1_invariant_manifold" for row in laws)
    stable_law = any(row["law_id"] == "QIM2280_2_stable_manifold" for row in laws)
    phase_demoted = any(row["audit_id"] == "PLO2280_4_q_feedback_lock" and row["result"] == "RECLASSIFIED_AS_Q_OPERATOR" for row in phase)
    current_action_blocked = any(row["owner_id"] == "QOO2280_0_current_scalar_action" and row["ownership_result"] == "NO_EXPLICIT_Q_OWNER_FOUND" for row in owners)
    best_route = any(row["owner_id"] == "QOO2280_2_q_stiffness_sector" and row["ownership_result"] == "BEST_CONDITIONAL_ROUTE" for row in owners)
    contract_nonclaim = all(row["valid_for_claim"] is False for row in contract)
    local_blocked = any(row["claim_id"] == "CG2280_4_local_gr" and row["gate_pass"] is False for row in claims)
    q_route_not_claimed = any(row["claim_id"] == "CG2280_3_q_stiffness_route" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusals)
    next_selected = any(row["route_id"] == "NEXT2280_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2280*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2280_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2280_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2280_2_prior_validation", prior_ok, "2279 validation passes"),
        ("VAL2280_3_invariant_law", invariant_law, "q=0 invariant-manifold law written"),
        ("VAL2280_4_stable_law", stable_law, "finite residual stable-manifold law written"),
        ("VAL2280_5_phase_demoted", phase_demoted, "q-feedback phase lock is reclassified as q operator ownership"),
        ("VAL2280_6_current_action_blocked", current_action_blocked, "current scalar action does not explicitly own q operator"),
        ("VAL2280_7_best_route", best_route, "q-stiffness sector selected as best conditional route"),
        ("VAL2280_8_contract_nonclaim", contract_nonclaim, "minimal parent contract remains nonclaim"),
        ("VAL2280_9_local_blocked", local_blocked, "local GR/Newton claim remains blocked"),
        ("VAL2280_10_q_route_not_claimed", q_route_not_claimed, "q-stiffness route is useful but not claimed"),
        ("VAL2280_11_refusal_blocks", refusal_blocks, "refusal runner blocks phase/action/local claims"),
        ("VAL2280_12_next_selected", next_selected, "2281 target selected"),
        ("VAL2280_13_csv_parse", csvs_parse, "all generated 2280 CSVs parse"),
        ("VAL2280_14_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2280_15_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2280_16_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2280_17_formalization_no_2280", formalization_clean, "formalization-workbench has no 2280 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2280_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2280 recasts the local-GR gap as invariant-manifold ownership, demotes free phase-locking, selects q-stiffness/Onsager ownership as the best conditional route, and blocks local claims",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    laws = invariance_law_rows()
    phase = phase_lock_owner_rows()
    owners = q_operator_owner_rows()
    contract = parent_contract_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2280 - Y5/R2FR Phase-Lock Distribution Or q Residual Operator Owner",
        "",
        "## Verdict",
        "",
        "This checkpoint makes a useful leap: the local-GR problem is an invariant-manifold ownership problem. With `q := C_R - C_T/(1-C_T)`, preserving the local branch requires `Dq=0` on `q=0`, i.e. `E_R - F'(C_T)E_T + B_q = 0`. Nonzero phase exchange is not enough; it must be tangent to that manifold.",
        "",
        "Free phase-locking is therefore demoted. Random/even phase distributions cannot direct the exchange, and odd/lagged locked distributions remain unsourced. If a phase distribution is chosen to depend on `q`, then the real owner is no longer phase-locking by itself; it is a `q` residual/stiffness operator.",
        "",
        "The best route is now explicit and hard-edged: derive a parent `q`-stiffness or Onsager relaxation sector, such as `S_q=-1/2 ∫[Z_q |∇q|^2 + M_q^2 q^2]`, from covariance regularity/coarse-graining. If that cannot be derived, the local transition remains closure-only.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## q Invariant-Manifold Law",
        table(["law_id", "object", "formula", "derived_condition", "status", "valid_for_claim"], laws),
        "",
        "## Phase-Lock Owner Audit",
        table(["audit_id", "candidate_owner", "test", "result", "reason", "missing_inputs", "valid_for_claim"], phase),
        "",
        "## q Operator Owner Audit",
        table(["owner_id", "candidate_owner", "operator_generated", "ownership_result", "reason", "required_for_claim", "valid_for_claim"], owners),
        "",
        "## Minimal Parent Contract",
        table(["contract_id", "requirement", "mathematical_form", "current_status", "next_evidence_needed", "valid_for_claim"], contract),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusals),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is not circling. It moves the missing coupling from a foggy idea to a named parent-action requirement. To derive local GR/Newton, MTS now needs either a source-backed phase-lock distribution satisfying the exact tangency equation, or a parent q-stiffness/relaxation sector with positive coefficients and silent/bounded boundary terms.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["invariance_law"], invariance_law_rows())
    write_csv(OUTPUTS["phase_lock_owner"], phase_lock_owner_rows())
    write_csv(OUTPUTS["q_operator_owner"], q_operator_owner_rows())
    write_csv(OUTPUTS["parent_contract"], parent_contract_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["phase_lock_owner"], COPY_TARGETS["queue_phase_lock"])
    shutil.copyfile(OUTPUTS["parent_contract"], COPY_TARGETS["queue_contract"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["invariance_law"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
