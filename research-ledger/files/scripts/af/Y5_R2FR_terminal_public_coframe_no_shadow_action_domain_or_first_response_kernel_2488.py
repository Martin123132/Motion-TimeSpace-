from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_TERMINAL_PUBLIC_COFRAME_NO_SHADOW_2488"
CHECKPOINT_ID = "2488"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2488-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2488_SOURCE_REGISTER.csv",
    "action_domain": OUT / "P8_Y5_NO_SHADOW_2488_ACTION_DOMAIN_ATTEMPT.csv",
    "zero_theorem": OUT / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv",
    "countermodels": OUT / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv",
    "response_kernel": OUT / "P8_Y5_NO_SHADOW_2488_RESPONSE_KERNEL_ACQUISITION.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2488_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2488_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2488_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2488_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2488_VALIDATION.csv",
}

COPY_TARGETS = {
    "action_domain": LOCAL_BOUNDS / "No_shadow_action_domain_attempt_2488_NONCLAIM.csv",
    "zero_theorem": LOCAL_BOUNDS / "No_shadow_zero_theorem_2488_NONCLAIM.csv",
    "response_kernel": LOCAL_BOUNDS / "Common_frame_response_kernel_acquisition_2488_NONCLAIM.csv",
    "countermodels": LOCAL_BOUNDS / "No_shadow_countermodel_ledger_2488_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2488_FIRST_COMMON_FRAME_RESPONSE_KERNEL_OR_ACTION_CLAUSE.csv",
}

SOURCES = [
    {
        "source_id": "SRC2488_00_2487_handoff",
        "source_path": ROOT / "2487-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md",
        "needles": ["NEXT2487_0_selected", "NS2487_3_current_verdict", "VAL2487_OVERALL"],
        "role": "current handoff: no-shadow action-domain or first response-kernel target",
    },
    {
        "source_id": "SRC2488_01_1880_terminal_public",
        "source_path": ROOT / "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
        "needles": ["TPC1880_0_terminal_object", "ZTH1880_0_exact_conditional", "BIN1880_1_response_kernels"],
        "role": "terminal public coframe exact conditional theorem and response-kernel debt",
    },
    {
        "source_id": "SRC2488_02_1879_ownership",
        "source_path": ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
        "needles": ["PCO1879_1_coframe_owner", "NSF1879_5_verdict", "CFL1879_4_total_abs"],
        "role": "parent coframe ownership clauses and b_R/d_R/w_R finite rows",
    },
    {
        "source_id": "SRC2488_03_1738_kernel",
        "source_path": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
        "needles": ["DOK1738_0_chain_rule_kernel", "DOK1738_1_same_coframe_not_enough", "CM1738_0_common_Weyl"],
        "role": "chain-rule coframe kernel and same-coframe countermodel",
    },
    {
        "source_id": "SRC2488_04_1878_qshape_failure",
        "source_path": ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
        "needles": ["CKT1878_0_chain_rule", "CKT1878_3_common_frame_countermodel", "VAL1878_OVERALL"],
        "role": "q_shape shortcut failure and observed-coframe trapdoor",
    },
    {
        "source_id": "SRC2488_05_2486_quotient",
        "source_path": ROOT / "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
        "needles": ["THM2486_0_chain_rule_descent", "RS2486_2_RAB", "VAL2486_OVERALL"],
        "role": "quotient descent theorem and rejection of cheap R_AB verticality",
    },
    {
        "source_id": "SRC2488_06_2485_parent_normal_form",
        "source_path": ROOT / "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md",
        "needles": ["NF2485_0_parent_action_skeleton", "DG2485_4_vertical_derivatives", "VAL2485_OVERALL"],
        "role": "parent normal-form skeleton and derivative grammar debt",
    },
    {
        "source_id": "SRC2488_07_2487_validation",
        "source_path": OUT / "P8_Y5_BRR545_2487_VALIDATION.csv",
        "needles": ["VAL2487_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def action_domain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "clause_id": "AD2488_0_terminal_public_coframe",
            "clause": "ordinary observables factor through a terminal public coframe",
            "formal_statement": "Obs_A(Phi,Psi)=Obsbar_A(E(Q_vis(Phi)),Psi,theta_pub) for clocks, rods, photons, source current and orbit readout",
            "status": "CANDIDATE_NOT_PARENT_DERIVED",
            "proof_attempt": "If the parent category has one terminal object E(Q_vis) for ordinary readout, then hidden/residual representatives cannot enter local metric observations.",
            "blocker": "current normal-form files do not prove terminality or the visible quotient object Q_vis",
            "implication_if_signed": "moves common coframe terms toward theorem-zero instead of empirical finite rows",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2488_1_no_C_frame_slot",
            "clause": "no Weyl/disformal shadow-frame argument",
            "formal_statement": "Allowed[S_matter,Obs] excludes A_R(C_R)^2 g_pub, B_R(C_R) u_mu u_nu, and E(Q_vis,C_R)",
            "status": "CLOSURE_ONLY_NOT_DERIVED",
            "proof_attempt": "Diffeomorphism covariance and one public frame do not forbid a universal hidden conformal/disformal factor.",
            "blocker": "no parent action-domain grammar bans C_R/J_q representative dependence inside the ordinary metric slot",
            "implication_if_signed": "b_R=d_R=0",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2488_2_no_source_prefactor",
            "clause": "no source-only matter prefactor",
            "formal_statement": "Allowed[S_matter] excludes sum_A w_A(C_R) L_A(Psi_A,e_pub) and source-weight currents not descending through Q_vis",
            "status": "NOT_DERIVED",
            "proof_attempt": "WEP and Ward conservation are insufficient: a universal or sector-balanced source prefactor can be locally covariant.",
            "blocker": "ordinary matter descent and source-current owner are not parent-signed at the action-domain level",
            "implication_if_signed": "w_R=0 and the Hilbert-source normalization leak is silenced",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2488_3_connection_tau_boundary_inherit",
            "clause": "connection, tau, source support and boundary endpoints inherit the same public coframe",
            "formal_statement": "omega=omega[e_pub], tau=tau(Q_vis), source support=sigma(Q_vis), and P_loc dE/dQ_endpoint=0",
            "status": "INHERITANCE_STACK_UNSIGNED",
            "proof_attempt": "Metric/coframe descent would not be enough if the connection, clock map, source support or endpoint data selects a hidden representative later.",
            "blocker": "connection descent, tau pushforward and boundary endpoint silence remain open branches",
            "implication_if_signed": "epsilon_endpoint_R=0 and coframe zero cannot reopen through endpoints",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2488_4_verdict",
            "clause": "parent action-domain exclusion closes no-shadow",
            "formal_statement": "AD2488_0 through AD2488_3 are all parent-signed in one branch",
            "status": "ACTION_DOMAIN_NO_SHADOW_NOT_DERIVED_CURRENT_CORPUS",
            "proof_attempt": "Attempted proof fails because the parent normal form is still a skeleton, not a signed object-language theorem.",
            "blocker": "terminality, no-extra-frame grammar, source-prefactor ban and inheritance stack are unsigned",
            "implication_if_signed": "b_R=d_R=w_R=epsilon_endpoint_R=0",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def zero_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "ZTH2488_0_exact_conditional",
            "theorem_statement": "If ordinary matter/readout has e_pub=E(Q_vis), no C_R/J_q Weyl, disformal, source-prefactor or endpoint slot is in the action/readout domain, and connection/tau/source/boundary maps inherit e_pub, then b_R=d_R=w_R=epsilon_endpoint_R=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_failure": "By action-domain exclusion, the functional derivatives of ordinary readout with respect to C_R/J_q representative directions vanish; the inherited maps have no independent argument to reintroduce them.",
            "required_clauses": "AD2488_0_terminal_public_coframe;AD2488_1_no_C_frame_slot;AD2488_2_no_source_prefactor;AD2488_3_connection_tau_boundary_inherit",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZTH2488_1_shortcuts_rejected",
            "theorem_statement": "Covariance, WEP, Ward conservation, same-frame language and q_shape forgetting are not enough to prove no-shadow.",
            "status": "SHORTCUTS_REJECTED",
            "proof_or_failure": "Common Weyl/disformal/source-prefactor countermodels remain covariant and can be universal while still moving local metric, clock, PPN or source normalization.",
            "required_clauses": "parent action-domain exclusion, not slogan-level symmetry",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZTH2488_2_current_verdict",
            "theorem_statement": "Current MTS derives terminal public coframe no-shadow locally.",
            "status": "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "proof_or_failure": "The exact conditional theorem exists, but its premises are still closure contracts rather than parent-derived action grammar.",
            "required_clauses": "all AD2488 clauses plus coefficient owner signatures",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZTH2488_3_fallback",
            "theorem_statement": "Unsigned no-shadow rows must become response-kernel inputs, not claims.",
            "status": "RESPONSE_KERNEL_REQUIRED_NONCLAIM",
            "proof_or_failure": "Finite b_R/d_R/w_R/endpoint coefficients need arena-specific kernels, accepted bounds, units, source paths and no-cancellation envelopes.",
            "required_clauses": "PPN, clock/WEP or orbital response kernel with same baseline and source convention",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "countermodel_id": "CM2488_0_common_weyl",
            "ansatz": "e_obs = exp(b_R C_R) e_pub",
            "why_it_survives": "one universal coframe can still depend on a hidden/residual representative and shift local metric/clock/PPN readout",
            "kills_shortcut": "same-frame;WEP;covariance",
            "required_fix": "derive b_R=0 by action-domain exclusion or source a PPN/clock/orbital response bound",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2488_1_common_disformal",
            "ansatz": "g_obs = A(C_R)^2 g_pub + D(C_R) u_mu u_nu",
            "why_it_survives": "a universal preferred-frame/disformal dependence can be covariant once the current field is part of the domain",
            "kills_shortcut": "covariance;single-public-metric",
            "required_fix": "derive no current/disformal slot or source preferred-frame PPN kernel",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2488_2_source_prefactor",
            "ansatz": "S_matter includes sum_A w_A(C_R)L_A",
            "why_it_survives": "source normalization can move while the metric coframe looks universal",
            "kills_shortcut": "WEP;Ward;metric-only readout",
            "required_fix": "derive source-current descent/no source-only slot or source WEP/clock/R10 source-leg bounds",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2488_3_endpoint_boundary",
            "ansatz": "e_obs=E(Q_vis,Q_endpoint) with P_loc partial_Q_endpoint E nonzero",
            "why_it_survives": "boundary or endpoint data can leak locally after the main coframe map is declared public",
            "kills_shortcut": "bulk coframe descent",
            "required_fix": "derive boundary endpoint silence or source orbital/light-time endpoint kernel",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2488_4_qshape_forgetting",
            "ansatz": "Dq_shape[v_R]=0 while DObs_e[v_R] is nonzero",
            "why_it_survives": "forgetting a label in q_shape does not prove clocks, rods, photons and sources forget it",
            "kills_shortcut": "q_shape;cheap verticality",
            "required_fix": "derive observed readout functor basicity or retain finite DObs/common-frame rows",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def response_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "KER2488_0_PPN_metric_bR",
            "arena": "PPN_metric_gamma_beta",
            "selected_priority": "SELECTED_FIRST_KERNEL_NONCLAIM",
            "candidate_relation": "|delta gamma|+|delta beta| <= K_PPN_b |b_R| + K_PPN_d |d_R| + K_PPN_endpoint |epsilon_endpoint_R|",
            "required_inputs": "b_R;d_R;epsilon_endpoint_R;PPN response operator;GR baseline;accepted PPN bounds;source convention",
            "missing_inputs": "MISSING_RESPONSE_KERNEL;MISSING_NUMERIC_COEFFICIENTS;MISSING_ACCEPTED_BOUND_SET;MISSING_BASELINE",
            "reason_for_priority": "PPN metric response is the most direct local-GR test of a common frame leak",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2488_1_clock_WEP_wR",
            "arena": "clock_WEP_source_normalization",
            "selected_priority": "SECONDARY_KERNEL_NONCLAIM",
            "candidate_relation": "|delta clock|+|eta_WEP| <= K_clock_b |b_R| + K_WEP_w |w_R| + material_terms",
            "required_inputs": "b_R;w_R;material sensitivities;tau_clock;tau_WEP;accepted clock/WEP bounds",
            "missing_inputs": "MISSING_MATERIAL_MAP;MISSING_TAU_PROJECTION;MISSING_RESPONSE_KERNEL",
            "reason_for_priority": "WEP-clean common-mode source shifts may hide from composition tests but show in clock/source normalization",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2488_2_orbital_light_time",
            "arena": "orbital_light_time",
            "selected_priority": "TERTIARY_KERNEL_NONCLAIM",
            "candidate_relation": "|delta a|+|delta light_time| <= K_orb_b |b_R| + K_orb_d |d_R| + K_orb_end |epsilon_endpoint_R|",
            "required_inputs": "b_R;d_R;epsilon_endpoint_R;orbital response kernel;ephemeris baseline;accepted residual convention",
            "missing_inputs": "MISSING_ORBIT_KERNEL;MISSING_ENDPOINT_PROJECTION;MISSING_BASELINE",
            "reason_for_priority": "orbital/light-time tests catch endpoint and preferred-frame leakage not seen in simple metric rows",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2488_3_R10_guarded",
            "arena": "R10_short_range_guarded",
            "selected_priority": "HELD_LATER_WRONG_ROUTE_GUARD",
            "candidate_relation": "alpha_R10(lambda) may receive a source-leg term only after finite range Z_R/M_R^2/lambda_R and source/test charges exist",
            "required_inputs": "Z_R;M_R^2;lambda_R;source/test charges;R10 bound curve;tau_R10;w_R source leg",
            "missing_inputs": "MISSING_FINITE_RANGE_OPERATOR;MISSING_SOURCE_TEST_CHARGES;MISSING_BOUND_CURVE",
            "reason_for_priority": "common-frame source coupling cannot replace the finite-range R10 branch",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2488_4_absolute_envelope",
            "arena": "all_local_arenas",
            "selected_priority": "NO_CANCELLATION_ENVELOPE_REQUIRED",
            "candidate_relation": "epsilon_common_frame_abs=|b_R|+|d_R|+|w_R|+|epsilon_endpoint_R| plus sourced DObs/tau/readout leaks",
            "required_inputs": "all leak coefficients with units, source paths, normalization frame and no-cancellation rule",
            "missing_inputs": "MISSING_NUMERIC_OR_THEOREM_ZERO_FOR_ALL_COMPONENTS",
            "reason_for_priority": "prevents accidental cancellation from being sold as local GR",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2488_0_internal",
            "claim": "2488 may be used as a private no-shadow audit and response-kernel routing file",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "all public/local claims are explicitly blocked and finite rows are not scored",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2488_1_no_shadow_zero",
            "claim": "b_R=d_R=w_R=epsilon_endpoint_R=0",
            "gate_status": "BLOCKED",
            "reason": "terminal public coframe, no-extra-frame grammar, no source-prefactor and inheritance stack are not parent-derived",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2488_2_response_kernel_score",
            "claim": "finite common-frame rows pass PPN/clock/WEP/orbital bounds",
            "gate_status": "BLOCKED",
            "reason": "response kernels, numeric coefficients, accepted bounds, units and baselines are missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2488_3_local_GR_Newton",
            "claim": "MTS reduces to local GR/Newton through no-shadow coframe",
            "gate_status": "BLOCKED",
            "reason": "no-shadow is not derived and is not sufficient without EH/kappa, source normalization, beta and conservation closure",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2488_4_no_shortcuts",
            "claim": "same-frame, WEP, Ward, q_shape or fitted-GM shortcut is used as proof",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "all shortcut routes are explicitly rejected or held as countermodels",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2488_0_result",
            "decision": "ACTION_DOMAIN_NO_SHADOW_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "The zero theorem is exact if terminality/no-extra-frame/source/inheritance clauses are signed, but those clauses remain closure-level.",
            "effect": "retain b_R,d_R,w_R,endpoint and total-envelope rows as nonclaim residuals",
        },
        {
            "decision_id": "DEC2488_1_best_next",
            "decision": "FIRST_PPN_RESPONSE_KERNEL_SELECTED",
            "reason": "PPN gamma/beta/preferred-frame leakage is the cleanest local-GR-facing kernel for common Weyl/disformal frame terms.",
            "effect": "next checkpoint should derive/source K_PPN_b,K_PPN_d,K_PPN_endpoint or find the parent no-shadow clause",
        },
        {
            "decision_id": "DEC2488_2_route_guard",
            "decision": "R10_HELD_LATER_AS_GUARDED_SOURCE_LEG",
            "reason": "R10 needs a finite-range operator and real alpha(lambda) bound chain; common-frame source prefactors cannot stand in for that.",
            "effect": "do not route no-shadow failure into R10 claims",
        },
        {
            "decision_id": "DEC2488_3_status",
            "decision": "LOCAL_GR_BRANCH_STILL_ALIVE_BUT_NOT_CLAIMABLE",
            "reason": "The logic is sharpening: either derive action-domain silence or project finite leaks into local tests.",
            "effect": "continue derivation-first, with PPN kernel fallback as the next disciplined pressure test",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2488_0_selected",
            "selection_status": "selected",
            "target_file": "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
            "target_script": "scripts/Y5_R2FR_first_common_frame_PPN_response_kernel_or_parent_no_shadow_clause_2489.py",
            "task": "derive or source the first response kernel mapping b_R/d_R/endpoint leak to PPN gamma,beta,preferred-frame residuals; alternatively find the parent action-domain no-shadow clause",
            "acceptance_target": "one source-ready PPN response-kernel row or a signed parent no-shadow clause; all local-GR claims remain blocked unless theorem-zero or source-backed numeric bounds exist",
            "guardrails": "no same-frame shortcut; no WEP/Ward shortcut; no q_shape shortcut; no fitted GM; no R10 shortcut; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "action_domain": OUTPUTS["action_domain"],
        "zero_theorem": OUTPUTS["zero_theorem"],
        "response_kernel": OUTPUTS["response_kernel"],
        "countermodels": OUTPUTS["countermodels"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2488_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2488_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2488_01_action_domain_verdict_blocked",
        any(row["clause_id"] == "AD2488_4_verdict" and row["status"] == "ACTION_DOMAIN_NO_SHADOW_NOT_DERIVED_CURRENT_CORPUS" for row in data["action_domain"]),
        "action-domain no-shadow proof attempt is explicit and blocked",
    )
    add(
        "VAL2488_02_zero_theorem_conditional",
        any(row["theorem_id"] == "ZTH2488_0_exact_conditional" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in data["zero_theorem"]),
        "exact conditional no-shadow theorem is retained",
    )
    add(
        "VAL2488_03_current_no_shadow_not_claimed",
        any(row["theorem_id"] == "ZTH2488_2_current_verdict" and row["status"] == "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in data["zero_theorem"]),
        "current no-shadow zero is not promoted",
    )
    add(
        "VAL2488_04_countermodels_retained",
        len(data["countermodels"]) >= 5 and all(row["valid_for_claim"] is False for row in data["countermodels"]),
        "Weyl, disformal, source-prefactor, endpoint and q_shape countermodels remain live",
    )
    add(
        "VAL2488_05_first_kernel_selected",
        any(row["kernel_id"] == "KER2488_0_PPN_metric_bR" and row["selected_priority"] == "SELECTED_FIRST_KERNEL_NONCLAIM" for row in data["response_kernel"]),
        "PPN metric response kernel is selected as first fallback",
    )
    add(
        "VAL2488_06_kernel_rows_nonclaim",
        all(row["valid_for_claim"] is False for row in data["response_kernel"]),
        "all response-kernel rows are nonclaim and missing-input guarded",
    )
    add(
        "VAL2488_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows no-shadow, local-GR, PPN, R10 or Newton claim",
    )
    add(
        "VAL2488_08_shortcuts_rejected",
        any(row["gate_id"] == "GATE2488_4_no_shortcuts" and row["gate_status"] == "PASS_GUARDRAIL" for row in data["claim_gates"]),
        "same-frame, WEP, Ward, q_shape, fitted-GM and R10 shortcuts are rejected",
    )
    add(
        "VAL2488_09_next_target_written",
        any(row["route_id"] == "NEXT2488_0_selected" for row in data["next"]),
        "2489 PPN response-kernel or parent no-shadow target selected",
    )
    add("VAL2488_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2488*", "*P8_Y5_NO_SHADOW_2488*", "*JR2488*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2488_11_no_formalization_artifacts", not formalization_artifacts, "no 2488 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2488_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2488_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2488_OVERALL",
        overall,
        "2488 blocks action-domain no-shadow promotion, preserves exact conditional theorem, and selects first PPN response-kernel fallback",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2488 Y5 R2FR Terminal Public Coframe No-Shadow Action Domain Or First Response Kernel",
        "",
        "**Status:** no public/local claim. The no-shadow theorem is exact only as a conditional theorem; the current corpus does not yet derive the parent action-domain clause that excludes hidden Weyl, disformal, source-prefactor and endpoint slots.",
        "",
        "**Main result:** the derivation route did not close today. The theory still has a clean route: if ordinary matter/readout is forced to factor through a terminal public coframe `e_pub=E(Q_vis)` and the parent action domain forbids extra `C_R/J_q` frame/source/end-point arguments, then `b_R=d_R=w_R=epsilon_endpoint_R=0`. But those premises are not signed by the parent normal form yet. Therefore the disciplined fallback is the first common-frame PPN response kernel, not an R10 or WEP shortcut.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Action-Domain Attempt",
        markdown_table(data["action_domain"], ["clause_id", "clause", "formal_statement", "status", "proof_attempt", "blocker", "implication_if_signed", "valid_for_claim"]),
        "",
        "## Zero Theorem",
        markdown_table(data["zero_theorem"], ["theorem_id", "theorem_statement", "status", "proof_or_failure", "required_clauses", "valid_for_claim"]),
        "",
        "## Countermodel Ledger",
        markdown_table(data["countermodels"], ["countermodel_id", "ansatz", "why_it_survives", "kills_shortcut", "required_fix", "valid_for_claim"]),
        "",
        "## Response-Kernel Acquisition",
        markdown_table(data["response_kernel"], ["kernel_id", "arena", "selected_priority", "candidate_relation", "required_inputs", "missing_inputs", "reason_for_priority", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "action_domain": action_domain_rows(),
        "zero_theorem": zero_theorem_rows(),
        "countermodels": countermodel_rows(),
        "response_kernel": response_kernel_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["action_domain"], data["action_domain"])
    write_csv(OUTPUTS["zero_theorem"], data["zero_theorem"])
    write_csv(OUTPUTS["countermodels"], data["countermodels"])
    write_csv(OUTPUTS["response_kernel"], data["response_kernel"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
