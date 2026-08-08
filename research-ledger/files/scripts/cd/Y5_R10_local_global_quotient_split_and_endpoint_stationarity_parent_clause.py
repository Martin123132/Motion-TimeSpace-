from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_864_SOURCE_REGISTER.csv"
PARENT_CLAUSE_PATH = RESIDUALS / "P8_Y5_R10_864_PARENT_CLAUSE_CANDIDATE.csv"
SPLIT_LEMMA_PATH = RESIDUALS / "P8_Y5_R10_864_LOCAL_GLOBAL_SPLIT_LEMMA.csv"
ENDPOINT_STATIONARITY_PATH = RESIDUALS / "P8_Y5_R10_864_ENDPOINT_STATIONARITY_AUDIT.csv"
QSTAR_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_864_QSTAR_NORMALIZATION_AUDIT.csv"
LOCAL_NOHAIR_PATH = RESIDUALS / "P8_Y5_R10_864_LOCAL_NOHAIR_CONTRACT.csv"
GR_NEWTON_PATH = RESIDUALS / "P8_Y5_R10_864_GR_NEWTON_IMPACT_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_864_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_864_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_864_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_864_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_864_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_864_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_863_VALIDATION.csv"

STATUS = "Y5_R10_864_local_global_quotient_split_clause_written_sufficient_not_parent_derived_nonclaim"
CLAIM_CEILING = "parent_clause_candidate_only_no_endpoint_stationarity_no_Qstar_no_local_GR_claim"
NEXT_TARGET = "865-Y5-R10-minimal-boundary-charge-action-for-endpoint-stationarity-and-Qstar.md"

SOURCE_SPECS = [
    {
        "source_id": "863_doc",
        "path": POST_CHECKPOINT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needles": [
            "local/global quotient split",
            "CZT863_2_local_global_split",
            "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        ],
        "role": "immediate local/global quotient split handoff",
    },
    {
        "source_id": "863_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V863_8_route_selected,pass",
            "V863_10_all_rows_nonclaim,pass",
            "V863_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "407_primitive_quotient",
        "path": POST_CHECKPOINT / "407-primitive-relational-quotient-action-sketch.md",
        "needles": [
            "Primitive Relational Quotient Action Sketch",
            "S_matter_quotient_functor",
            "local_GR_promoted",
        ],
        "role": "primitive quotient parent action sketch",
    },
    {
        "source_id": "410_quotient_matter_functor",
        "path": POST_CHECKPOINT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": [
            "Conditional Functor Theorem",
            "Counterexample Functors",
            "quotient_matter_functor_parent_derived",
        ],
        "role": "matter functor factorization and counterexample ledger",
    },
    {
        "source_id": "626_descent_signature",
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "needles": [
            "Descent Criterion",
            "QIM626_0_descent_equivalence",
            "boundary projection certificate",
        ],
        "role": "quotient-invariant matter action descent criterion",
    },
    {
        "source_id": "760_descent_pack",
        "path": POST_CHECKPOINT / "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md",
        "needles": [
            "quotient matter descent is not parent-signed",
            "QMD760_0_descent_equivalence",
            "coupling residual source-pack schema",
        ],
        "role": "latest quotient matter descent nonclaim source pack",
    },
    {
        "source_id": "761_vertical_matter_action",
        "path": POST_CHECKPOINT / "761-Y5-R10-parent-matter-domain-vertical-action-or-coupling-source-fill.md",
        "needles": [
            "parent matter-domain vertical-action contract",
            "MVA761_0_domain_category",
            "MVA761_5_evaluability_verdict",
        ],
        "role": "vertical action on ordinary matter domain",
    },
    {
        "source_id": "762_geometry_stack",
        "path": POST_CHECKPOINT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        "needles": [
            "geometry-stack descent is not parent-signed",
            "GSD762_2_coframe_metric_descent",
            "GSD762_5_stack_verdict",
        ],
        "role": "matter measure/coframe/connection/operator descent",
    },
    {
        "source_id": "623_coframe_functor",
        "path": POST_CHECKPOINT / "623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md",
        "needles": [
            "factorization through the quotient",
            "OCF623_0_factorization_lemma",
            "b_g=0",
        ],
        "role": "coframe factorization chain-rule lemma",
    },
    {
        "source_id": "110_endpoint_equation",
        "path": POST_CHECKPOINT / "110-endpoint-charge-equation-attempt.md",
        "needles": [
            "spatial-cell endpoint quadratic",
            "endpoint_equation_parent_derived",
            "Qstar_charge_unit_derived",
        ],
        "role": "endpoint charge quadratic target and missing Qstar unit",
    },
    {
        "source_id": "111_variational_owner",
        "path": POST_CHECKPOINT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needles": [
            "formal_term_written_but_not_parent_derived",
            "coefficients_parent_forced",
            "endpoint_arrow_derived",
        ],
        "role": "formal endpoint owner candidate and coefficient/arrow blockers",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def parent_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "PC864_0_parent_domains",
            "parent_clause": "Define one parent configuration Phi with two quotient functors: q_FLRW:Phi->Q_FLRW and q_loc[U]:Phi->Q_loc(U).",
            "mathematical_condition": "Q_trace in Q_FLRW, while local matter on compact U factors through Q_loc(U)",
            "if_signed": "cosmological trace memory and local rods/clocks can be different quotient readouts of the same parent state",
            "current_status": "sufficient_clause_written_not_parent_derived",
            "blocker": "current corpus sketches quotient objects but does not sign q_FLRW and q_loc as action-level functors",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC864_1_trace_vertical_split",
            "parent_clause": "Introduce the trace endpoint direction v_T such that q_FLRW sees it and q_loc does not.",
            "mathematical_condition": "Dq_FLRW[v_T] = delta Q_trace != 0 and Dq_loc[U][v_T] = 0 for local non-cosmological U",
            "if_signed": "Q_trace can drive FLRW memory while being invisible to local matter variations",
            "current_status": "central_new_clause_not_parent_derived",
            "blocker": "no parent proof currently classifies Q_trace as local-vertical but FLRW-observable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC864_2_local_matter_descent",
            "parent_clause": "Ordinary matter descends through the local quotient only.",
            "mathematical_condition": "S_matter[U]=Sbar_matter[Obs_loc(q_loc[U](Phi)),Psi,theta(q_loc[U])]",
            "if_signed": "partial_{v_T} ehat_loc=0 and direct Pi_I^matter can vanish by chain rule",
            "current_status": "known_sufficient_but_not_signed",
            "blocker": "matter-domain vertical action, geometry-stack descent, and no-marker clauses remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC864_3_boundary_FLRW_action",
            "parent_clause": "The trace endpoint is owned by a boundary/FLRW action, not by local matter.",
            "mathematical_condition": "S_trace=S_trace[Q_trace,Q_*,q_FLRW] with delta S_trace/dQ_early=delta S_trace/dQ_today=0",
            "if_signed": "endpoint values become action-owned rather than fitted from cosmology",
            "current_status": "formal_owner_possible_not_parent_forced",
            "blocker": "110/111 found target equations and formal potential, but coefficients, arrow, and Q_* are not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC864_4_boundary_nohair",
            "parent_clause": "Boundary/exact trace currents have zero local projection and no shear/vector/clock/WEP hair.",
            "mathematical_condition": "P_loc J_trace=0; P_loc dB_trace=0; no B_TF, B_0i, clock, or species marker component",
            "if_signed": "q_loc^nu does not receive a hidden trace endpoint source",
            "current_status": "necessary_nohair_clause_not_signed",
            "blocker": "boundary projection silence is repeatedly listed as open in 626/760/863",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC864_5_total_verdict",
            "parent_clause": "Promote local/global quotient split.",
            "mathematical_condition": "PC864_0..PC864_4 jointly parent-signed",
            "if_signed": "DeltaR and local silence can share one parent mechanism without a local-GR cheat",
            "current_status": "not_promoted",
            "blocker": "all key clauses are sufficient contracts, not derived parent action facts",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def split_lemma_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "LGS864_0_conditional_split_lemma",
            "statement": "If Q_trace is in Q_FLRW but v_T is in ker(Dq_loc[U]), then local matter geometry is v_T-blind while FLRW memory can still vary.",
            "proof_sketch": "partial_{v_T} Obs_loc(q_loc)=DObs_loc(Dq_loc[v_T])=0, but Dq_FLRW[v_T]=delta Q_trace can source the global Ward current",
            "proof_status": "conditional_valid",
            "claim_gap": "parent action has not signed the two quotient functors or the v_T classification",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "LGS864_1_local_coframe_corollary",
            "statement": "Under the split and matter descent, partial_{v_T} ehat_loc=0 and Pi_T^matter=0.",
            "proof_sketch": "Pi_T^matter=(delta S_matter/d ehat_loc) partial_{v_T} ehat_loc plus theta terms; both vanish if no-marker descent holds",
            "proof_status": "conditional_chain_rule_corollary",
            "claim_gap": "no-marker constants and geometry-stack descent are not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "LGS864_2_FLRW_endpoint_corollary",
            "statement": "Under the split and boundary action, Q_trace can be varied by endpoint Ward equations.",
            "proof_sketch": "delta_{Q_trace} S_trace=0 gives endpoint equations while local compact variations do not couple to Q_trace",
            "proof_status": "formal_corollary_only",
            "claim_gap": "no specific parent-derived S_trace or Q_* charge metric exists yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "LGS864_3_not_a_decoupled_patch",
            "statement": "The split is acceptable only if q_FLRW and q_loc are compatible quotient readouts of one parent state.",
            "proof_sketch": "a disconnected FLRW sector plus GR local sector would be a patchwork model, not a unified parent mechanism",
            "proof_status": "guardrail",
            "claim_gap": "compatibility/inclusion map between Q_loc and Q_FLRW remains to be written",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def endpoint_stationarity_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "endpoint_id": "ES864_0_endpoint_variables",
            "required_object": "Q_early,Q_today,Q_trace",
            "candidate_condition": "Q_trace=(Q_early-Q_today)/Q_*",
            "current_status": "named_not_parent_derived",
            "risk_if_missing": "DeltaR remains a named contrast rather than an action variable",
            "next_action": "construct minimal boundary charge action with explicit endpoint variables",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "endpoint_id": "ES864_1_stationarity_equations",
            "required_object": "endpoint Euler equations",
            "candidate_condition": "delta S_trace/dQ_early=0 and delta S_trace/dQ_today=0",
            "current_status": "not_parent_derived",
            "risk_if_missing": "endpoint values can be fitted or chosen post hoc",
            "next_action": "derive or reject stationarity from boundary charge action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "endpoint_id": "ES864_2_exact_roots",
            "required_object": "endpoint quadratic or equivalent charge law",
            "candidate_condition": "27 R^2 - 12 R + 1 = 0, roots 1/9 and 1/3, DeltaR=2/9",
            "current_status": "target_found_not_derived",
            "risk_if_missing": "the exact 2/9 remains theorem target rather than prediction",
            "next_action": "explain coefficients 27,12,1 from parent charge pairing or reject exact-root route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "endpoint_id": "ES864_3_endpoint_arrow",
            "required_object": "early high endpoint to today low endpoint",
            "candidate_condition": "R_early=1/3, R_today=1/9, DeltaR>0",
            "current_status": "not_parent_derived",
            "risk_if_missing": "sign/order can be reversed or chosen after the fit",
            "next_action": "derive cosmological arrow or keep only conditional sign bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qstar_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "qstar_id": "QS864_0_charge_unit",
            "object": "Q_*",
            "candidate_definition": "parent-normalized trace Ward charge unit",
            "current_status": "missing",
            "blocks": "DeltaR dimensionless prediction and endpoint equation normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS864_1_charge_pairing",
            "object": "boundary charge metric",
            "candidate_definition": "<J_trace,J_trace>_Q or equivalent integral pairing",
            "current_status": "not_parent_derived",
            "blocks": "coefficient derivation for endpoint potential/quadratic",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS864_2_trace_leg_normalization",
            "object": "three equal FLRW trace legs",
            "candidate_definition": "Q_* makes each exact parent trace leg q_trace=2/27",
            "current_status": "conditional_on_exact_readout_and_current",
            "blocks": "DeltaR=3q_trace promotion if unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "qstar_id": "QS864_3_no_calibration_leak",
            "object": "not data-fitted Q_*",
            "candidate_definition": "Q_* fixed before SN/BAO scoring",
            "current_status": "future_promotion_gate",
            "blocks": "post-fit circularity removal",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nohair_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "nohair_id": "NH864_0_local_projection",
            "required_silence": "P_loc J_trace=0",
            "mathematical_form": "compact local experiments see q_loc only, not Q_trace",
            "current_status": "conditional_on_split",
            "if_fails": "trace endpoint contributes to q_loc^nu",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "nohair_id": "NH864_1_boundary_exact_terms",
            "required_silence": "P_loc dB_trace=0",
            "mathematical_form": "boundary/exact trace variation has no local force/source/clock projection",
            "current_status": "not_parent_signed",
            "if_fails": "bulk silence is spoiled by edge currents",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "nohair_id": "NH864_2_shear_vector_modes",
            "required_silence": "B_TF=B_0i=0 in local exterior",
            "mathematical_form": "trace endpoint is monopole/FLRW trace only",
            "current_status": "not_parent_signed",
            "if_fails": "PPN gamma, preferred-frame, or anisotropic stress rows activate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "nohair_id": "NH864_3_clock_WEP_markers",
            "required_silence": "no clock/species/material marker dependence on Q_trace",
            "mathematical_form": "partial_{Q_trace} theta_A=0 for local ordinary matter constants",
            "current_status": "not_parent_signed",
            "if_fails": "WEP/clock/fifth-force coupling residual source pack activates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gr_newton_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "impact_id": "GN864_0_if_split_signed",
            "branch": "local GR/Newton route",
            "conditional_result": "trace endpoint does not source local matter/coframe/projector equations",
            "remaining_debt": "EH operator selection, source normalization, N5/projector stress, boundary no-hair",
            "current_status": "useful_but_not_sufficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "GN864_1_if_endpoint_action_signed",
            "branch": "cosmology amplitude route",
            "conditional_result": "DeltaR can be selected by boundary stationarity rather than fitted",
            "remaining_debt": "derive Q_*, endpoint roots, and arrow before data scoring",
            "current_status": "not_signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "GN864_2_if_split_fails",
            "branch": "retained residual route",
            "conditional_result": "trace/coframe leakage must be scored in PPN, WEP, clock, orbital, and R10 arenas",
            "remaining_debt": "source-normalized residual coefficients and baselines",
            "current_status": "fallback_required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "GN864_3_verdict",
            "branch": "GR/Newton promotion",
            "conditional_result": "not promoted from 864",
            "remaining_debt": "parent action signatures for split, descent, no-marker, endpoint, Q_*, no-hair",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC864_0_selected",
            "route": "minimal_boundary_charge_action_for_endpoint_stationarity_and_Qstar",
            "status": "selected",
            "reason": "864 gives the split clause; the sharpest remaining numerical-theorem blocker is endpoint stationarity and Q_* normalization",
            "include": "boundary charge action, endpoint Euler equations, Q_* unit, coefficient origin for 27/12/1, endpoint arrow",
            "exclude": "new cosmology scoring, fitted DeltaR, public claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC864_1_deferred",
            "route": "local_residual_source_pack",
            "status": "deferred",
            "reason": "only needed if the split or no-hair clauses remain unsigned after the boundary charge attempt",
            "include": "PPN/WEP/clock/orbital/R10 residual coefficients",
            "exclude": "using residual rows to claim derived GR limit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG864_0_no_split_claim",
            "claim": "local/global quotient split is derived",
            "status": "forbidden",
            "reason": "864 writes a sufficient parent clause but does not derive q_FLRW/q_loc from an action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG864_1_no_endpoint_claim",
            "claim": "endpoint stationarity derives DeltaR=2/9",
            "status": "forbidden",
            "reason": "endpoint equations, roots, Q_*, and arrow remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG864_2_no_local_silence_claim",
            "claim": "P_loc J_trace=0 and Pi_I^matter=0 are proven",
            "status": "forbidden",
            "reason": "local silence follows only conditionally from the split plus matter descent/no-marker/no-hair clauses",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG864_3_no_local_GR_claim",
            "claim": "MTS reduces to GR/Newton locally",
            "status": "forbidden",
            "reason": "local GR still needs source normalization, EH/operator selection, N5 stress closure, and no-hair",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG864_4_allowed_private_result",
            "claim": "minimal parent-action clause is now explicit",
            "status": "allowed_private_nonclaim",
            "reason": "the split clause is a concrete sufficient theorem target and no longer vague prose",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D864_0",
            "finding": "local_global_split_clause_written",
            "reason": "q_FLRW/q_loc plus v_T visible-global/invisible-local is the exact sufficient clause for cosmology memory without local matter leakage",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D864_1",
            "finding": "clause_is_not_current_derivation",
            "reason": "the existing corpus has quotient sketches and conditional descent lemmas, but not an action-level proof of the two quotient functors or v_T classification",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D864_2",
            "finding": "endpoint_stationarity_and_Qstar_are_next",
            "reason": "even if the split is adopted, DeltaR=2/9 still needs boundary endpoint equations, charge unit, coefficient origin, and arrow",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive or reject a minimal boundary charge action that produces endpoint stationarity, Q_* normalization, the 27R^2-12R+1 equation, and the endpoint arrow",
            "include": "S_trace, Q_early, Q_today, Q_*, charge pairing, coefficient origin, endpoint arrow, nonclaim guards",
            "exclude": "SN/BAO refits, fitted endpoint values, formalization-workbench edits, public claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "wrote the minimal sufficient local/global quotient split parent clause and separated its endpoint, Q_*, no-hair, and matter-descent debts",
            "best_partial_result": "if Q_trace is FLRW-visible but locally vertical, local matter/coframe silence follows conditionally while FLRW memory remains possible",
            "hard_blockers": "parent-signed q_FLRW/q_loc functors, v_T classification, endpoint stationarity, Q_* unit, no-marker descent, boundary no-hair",
            "what_is_not_claimed": "local/global split derivation, DeltaR=2/9 prediction, P_loc J_trace=0, Pi_I^matter=0, q_loc=0, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    qstar_rows_: list[dict[str, object]],
    nohair_rows_: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    parent_clause_ok = any(row["clause_id"] == "PC864_1_trace_vertical_split" and row["current_status"] == "central_new_clause_not_parent_derived" for row in parent_rows)
    split_lemma_ok = any(row["lemma_id"] == "LGS864_0_conditional_split_lemma" and row["proof_status"] == "conditional_valid" for row in split_rows)
    endpoint_block_ok = any(row["endpoint_id"] == "ES864_1_stationarity_equations" and row["current_status"] == "not_parent_derived" for row in endpoint_rows)
    qstar_block_ok = any(row["qstar_id"] == "QS864_0_charge_unit" and row["current_status"] == "missing" for row in qstar_rows_)
    nohair_block_ok = any(row["nohair_id"] == "NH864_1_boundary_exact_terms" and row["current_status"] == "not_parent_signed" for row in nohair_rows_)
    gr_not_promoted = any(row["impact_id"] == "GN864_3_verdict" and row["current_status"] == "not_derived" for row in gr_rows)
    route_selected = any(row["route_id"] == "RC864_0_selected" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, parent_rows, split_rows, endpoint_rows, qstar_rows_, nohair_rows_, gr_rows, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V864_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V864_1_prior_863_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V864_2_parent_clause_written", "result": "pass" if parent_clause_ok else "fail", "detail": "trace visible-global/invisible-local split clause recorded"},
        {"check_id": "V864_3_split_lemma_conditional", "result": "pass" if split_lemma_ok else "fail", "detail": "local/global split lemma is conditional, not promoted"},
        {"check_id": "V864_4_endpoint_blocks_claim", "result": "pass" if endpoint_block_ok else "fail", "detail": "endpoint stationarity remains not parent-derived"},
        {"check_id": "V864_5_Qstar_blocks_claim", "result": "pass" if qstar_block_ok else "fail", "detail": "Q_* charge unit remains missing"},
        {"check_id": "V864_6_nohair_blocks_claim", "result": "pass" if nohair_block_ok else "fail", "detail": "boundary projection silence remains unsigned"},
        {"check_id": "V864_7_local_GR_not_promoted", "result": "pass" if gr_not_promoted else "fail", "detail": "local GR/Newton verdict remains not derived"},
        {"check_id": "V864_8_route_selected", "result": "pass" if route_selected else "fail", "detail": "minimal boundary charge action selected next"},
        {"check_id": "V864_9_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V864_10_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V864_11_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V864_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V864_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    qstar_rows_: list[dict[str, object]],
    nohair_rows_: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 864 - Y5 R10 Local-Global Quotient Split And Endpoint Stationarity Parent Clause",
        "",
        "Current result: **the minimal parent-action clause is now explicit, but it is still a sufficient contract rather than a derived theorem**. The clause is: one parent state `Phi` must have two compatible quotient readouts. `q_FLRW` sees the trace endpoint `Q_trace`; `q_loc[U]` used by local rods, clocks, matter, and PPN does not. In symbols, `Dq_FLRW[v_T] != 0` while `Dq_loc[U][v_T]=0`. If the parent action signs that and ordinary matter descends through `q_loc`, then cosmological trace memory can coexist with local GR silence. The corpus does not yet derive the split, endpoint stationarity, `Q_*`, or boundary no-hair.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Parent Clause Candidate",
        "",
        csv_table(parent_rows, ["clause_id", "parent_clause", "mathematical_condition", "if_signed", "current_status", "blocker", "valid_for_claim"]),
        "",
        "## Local-Global Split Lemma",
        "",
        csv_table(split_rows, ["lemma_id", "statement", "proof_sketch", "proof_status", "claim_gap", "valid_for_claim"]),
        "",
        "## Endpoint Stationarity Audit",
        "",
        csv_table(endpoint_rows, ["endpoint_id", "required_object", "candidate_condition", "current_status", "risk_if_missing", "next_action", "valid_for_claim"]),
        "",
        "## Qstar Normalization Audit",
        "",
        csv_table(qstar_rows_, ["qstar_id", "object", "candidate_definition", "current_status", "blocks", "valid_for_claim"]),
        "",
        "## Local Nohair Contract",
        "",
        csv_table(nohair_rows_, ["nohair_id", "required_silence", "mathematical_form", "current_status", "if_fails", "valid_for_claim"]),
        "",
        "## GR/Newton Impact Ledger",
        "",
        csv_table(gr_rows, ["impact_id", "branch", "conditional_result", "remaining_debt", "current_status", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    parent_rows = parent_clause_rows(generated_utc)
    split_rows = split_lemma_rows(generated_utc)
    endpoint_rows = endpoint_stationarity_rows(generated_utc)
    qstar_rows_ = qstar_rows(generated_utc)
    nohair_rows_ = nohair_rows(generated_utc)
    gr_rows = gr_newton_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        parent_rows,
        split_rows,
        endpoint_rows,
        qstar_rows_,
        nohair_rows_,
        gr_rows,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_CLAUSE_PATH, parent_rows, ["clause_id", "parent_clause", "mathematical_condition", "if_signed", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(SPLIT_LEMMA_PATH, split_rows, ["lemma_id", "statement", "proof_sketch", "proof_status", "claim_gap", "valid_for_claim", "generated_utc"])
    write_csv(ENDPOINT_STATIONARITY_PATH, endpoint_rows, ["endpoint_id", "required_object", "candidate_condition", "current_status", "risk_if_missing", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(QSTAR_AUDIT_PATH, qstar_rows_, ["qstar_id", "object", "candidate_definition", "current_status", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_NOHAIR_PATH, nohair_rows_, ["nohair_id", "required_silence", "mathematical_form", "current_status", "if_fails", "valid_for_claim", "generated_utc"])
    write_csv(GR_NEWTON_PATH, gr_rows, ["impact_id", "branch", "conditional_result", "remaining_debt", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, parent_rows, split_rows, endpoint_rows, qstar_rows_, nohair_rows_, gr_rows, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print("partial_clause=q_FLRW sees Q_trace while q_loc is vertical to it; sufficient for local silence if matter descent/nohair also sign")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
