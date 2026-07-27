from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4027"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4027-Y5-R2FR-Khat-component-completion-or-DGK-bound-normalization.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
COMPACT_SHELL_PROXY = 7.432631961576971e-06

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4027_SOURCE_REGISTER.csv",
    "component_gate": SRC / "P8_Y5_R2FR_4027_KHAT_COMPONENT_COMPLETION_GATE.csv",
    "completion": SRC / "P8_Y5_R2FR_4027_CONDITIONAL_COMPLETION_PATHS.csv",
    "bound_norm": SRC / "P8_Y5_R2FR_4027_DGK_BOUND_NORMALIZATION_ROWS.csv",
    "priority": SRC / "P8_Y5_R2FR_4027_NEXT_COMPONENT_PRIORITY.csv",
    "cases": SRC / "P8_Y5_R2FR_4027_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4027_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4027_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4027_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4027_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4027_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4027_VALIDATION.csv",
}

NEXT_DOC = "4028-Y5-R2FR-tracefree-improvement-parent-sign-or-DGK-first-bound-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4028_tracefree_improvement_parent_sign_or_DGK_first_bound_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4027_00_handoff", SRC / "P8_Y5_R2FR_4026_NEXT_TARGET.csv", "NEXT4026_0", "4026 handoff"),
        ("SRC4027_01_response", SRC / "P8_Y5_R2FR_4026_KGAMMA_RESPONSE_COMPONENTS.csv", "KGR4026_1_A_gradient", "4026 response components"),
        ("SRC4027_02_match", SRC / "P8_Y5_R2FR_4026_KHAT_COMPONENT_MATCH_AUDIT.csv", "KM4026_1_Khat_full_response", "4026 match audit"),
        ("SRC4027_03_bound", SRC / "P8_Y5_R2FR_4026_DGK_PROFILE_INPUT_ROWS.csv", "DGK4026_6_C_beta_C_R10", "4026 DGK rows"),
        ("SRC4027_04_khat_origin", SRC / "P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv", "KOR1525_2_improvement_action_route", "Khat origin audit"),
        ("SRC4027_05_kernel_req", SRC / "P8_Y5_PARENT_QLOC_1525_KMETRIC_KERNEL_REQUIREMENTS.csv", "KER1525_7_verdict", "Kmetric kernel requirements"),
        ("SRC4027_06_outcome", SRC / "P8_Y5_PARENT_QLOC_1526_DELTAK_OUTCOME_RUNNER.csv", "OUT1526_2_kernel_fallback", "DeltaK outcome runner"),
        ("SRC4027_07_boundary_alpha3", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "boundary", "boundary no-flux attempt"),
        ("SRC4027_08_r11_boundary", SRC / "P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv", "boundary", "R11 boundary stress theorem stack"),
        ("SRC4027_09_beta_components", SRC / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv", "beta", "beta envelope components"),
        ("SRC4027_10_ppn_projector", SRC / "P8_Y5_GAMMAKHAT_QLOC_2581_OFFICIAL_RESIDUAL_INTERFACE.csv", "q_loc", "official q_loc residual interface"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def component_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "KCG4027_0_tracefree_improvement",
            "component": "trace-free improvement/Hessian response",
            "candidate_completion": "K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi]",
            "evidence": "formal candidate and trace-free identity exist",
            "completion_status": "conditional_path_exists_not_parent_signed",
            "DGK_if_open": "D_A_grad / improvement mismatch",
            "next_action": "source phi owner, coefficient, boundary convention and live Khat adoption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "KCG4027_1_volume_trace",
            "component": "volume/trace response",
            "candidate_completion": "Kmetric_volume from delta sqrt|g| Gamma_eff",
            "evidence": "formal subpiece exists but sign/volume convention not fixed",
            "completion_status": "not_complete",
            "DGK_if_open": "D_trace_potential",
            "next_action": "fix sign and background subtraction or bound trace contribution",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "KCG4027_2_chain_m_L",
            "component": "m and L_cg chain response",
            "candidate_completion": "M_m^{mu nu}=delta m/delta g; M_L^{mu nu}=delta L_cg/delta g",
            "evidence": "requirements written; parent kernels missing",
            "completion_status": "not_complete",
            "DGK_if_open": "D_mass_gap / D_chain",
            "next_action": "prove m,L_cg metric-silent/fixed-point zero or supply kernels",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "KCG4027_3_connection",
            "component": "connection/covariant-derivative response",
            "candidate_completion": "K_conn from Christoffel/Hodge/domain/projector metric response",
            "evidence": "old kernel ledger marks missing connection kernel",
            "completion_status": "not_complete",
            "DGK_if_open": "D_A_grad + D_gamma_grad + D_cross_AG",
            "next_action": "derive Levi-Civita/local connection silence or bound K_conn",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "KCG4027_4_domain",
            "component": "domain/projection support response",
            "candidate_completion": "K_domain from integration domain, averaging cells, local collar and projection support",
            "evidence": "old kernel ledger marks missing domain kernel",
            "completion_status": "not_complete",
            "DGK_if_open": "D_boundary_improvement / preferred-frame leakage",
            "next_action": "prove domain descends/topological/no-flux or bound support variation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "KCG4027_5_boundary",
            "component": "boundary/reference/corner response",
            "candidate_completion": "K_boundary from boundary, reference subtraction, corners and no-flux response terms",
            "evidence": "old kernel ledger marks missing boundary kernel; compact-shell proxy exists but unmapped",
            "completion_status": "not_complete",
            "DGK_if_open": "D_boundary_improvement",
            "next_action": "derive no-flux or normalize compact-shell proxy to PPN/R10 units",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "KCG4027_6_projectors",
            "component": "observable projector maps",
            "candidate_completion": "C_beta_qloc and C_R10_qloc(lambda)",
            "evidence": "needed but not numeric/source-backed",
            "completion_status": "not_complete",
            "DGK_if_open": "unscored D_GK envelope",
            "next_action": "derive weak-field beta projector or finite-range map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def completion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "completion_id": "COMP4027_0_tracefree_route",
            "target_component": "KCG4027_0_tracefree_improvement",
            "completion_contract": "S_imp=int sqrt|g| c_I phi R plus fixed boundary term; Khat^{TF}=sigma_resp*c_I*K_L with sigma_resp*c_I=1",
            "needed_to_promote": "phi owner; c_I; sign convention; boundary term; live corpus adoption of Khat^{TF}",
            "status": "best_next_derivation_route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "completion_id": "COMP4027_1_volume_subtraction",
            "target_component": "KCG4027_1_volume_trace",
            "completion_contract": "Gamma_0 and pure trace vacuum pieces are fixed background subtraction, not compact source stress",
            "needed_to_promote": "same readout/source frame and boundary-compatible subtraction",
            "status": "required_guard",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "completion_id": "COMP4027_2_nohair_chain",
            "target_component": "KCG4027_2_chain_m_L",
            "completion_contract": "F'(m_*)=0 and F(m_*)=0 or M_m=M_L=0 on local fixed branch",
            "needed_to_promote": "parent signs fixed-point chain silence",
            "status": "conditional_only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_norm_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "norm_id": "NORM4027_0_master",
            "DGK_component": "D_GK_total",
            "normalized_form": "A_DGK/L_DGK <= sum_i A_i/L_i for i in {trace,A_grad,gamma_grad,cross,mass_gap,boundary}",
            "units_required": "stress-divergence units relative to EH source normalization",
            "current_status": "component_schema_ready_not_numeric",
            "next_input": "at least one A_i,L_i pair or theorem-zero certificate",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "norm_id": "NORM4027_1_trace",
            "DGK_component": "D_trace_potential",
            "normalized_form": "A_trace/L_trace from unowned trace/potential response",
            "units_required": "1/length^3 or declared source-normalized equivalent",
            "current_status": "requires subtraction or amplitude",
            "next_input": "Gamma0/mass trace subtraction certificate or A_trace,L_trace",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "norm_id": "NORM4027_2_A_grad",
            "DGK_component": "D_A_grad",
            "normalized_form": "A_Agrad/L_A from full A-gradient response minus partial Khat shape",
            "units_required": "stress-divergence units; Z_A normalized",
            "current_status": "shape_match_only",
            "next_input": "trace-free improvement signing or A_Agrad,L_A",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "norm_id": "NORM4027_3_gamma_cross_mass",
            "DGK_component": "D_gamma_grad + D_cross_AG + D_mass_gap",
            "normalized_form": "A_gamma/L_gamma + A_cross/L_cross + A_mass/L_mass",
            "units_required": "stress-divergence units; Z_G,c_AG,m_A,m_G normalized",
            "current_status": "missing_parent_sign_and_scale",
            "next_input": "coefficient signs/scales or profile amplitudes",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "norm_id": "NORM4027_4_boundary",
            "DGK_component": "D_boundary_improvement",
            "normalized_form": f"A_boundary_proxy={COMPACT_SHELL_PROXY} requires unit/projector map before use",
            "units_required": "map from compact-shell proxy to PPN/R10/source-measure units",
            "current_status": "proxy_available_not_score_ready",
            "next_input": "C_boundary_to_beta and C_boundary_to_R10 or no-flux theorem",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "norm_id": "NORM4027_5_observable_maps",
            "DGK_component": "projector coefficients",
            "normalized_form": "delta_beta_q_loc=C_beta_qloc*Q_loc; alpha_q(lambda)=C_R10_qloc(lambda)*Q_loc",
            "units_required": "dimensionless PPN beta and alpha(lambda)",
            "current_status": "missing_projector_maps",
            "next_input": "derive C_beta_qloc first because PPN local-GR route is priority",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def priority_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "priority_id": "PRI4027_0_first",
            "rank": 1,
            "target": "trace-free improvement parent signing",
            "reason": "it is the only component with a concrete algebraic shape match and least-scrutiny completion route",
            "next_doc": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "priority_id": "PRI4027_1_second",
            "rank": 2,
            "target": "C_beta_qloc projector normalization",
            "reason": "if Khat completion fails, beta is the most direct local-PPN observable gate",
            "next_doc": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "priority_id": "PRI4027_2_third",
            "rank": 3,
            "target": "boundary/no-flux or compact-shell unit map",
            "reason": "boundary proxy exists but cannot be used until mapped to real observables",
            "next_doc": "deferred unless trace-free route fails",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4027_0_tracefree_signed",
            "assumption": "S_imp signs the trace-free Khat component with live corpus adoption",
            "expected": "D_A_grad/improvement piece can be zeroed conditionally",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4027_1_current_state",
            "assumption": "trace-free route exists but is not parent-signed; other kernels missing",
            "expected": "D_GK remains component-bound branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4027_2_bound_normalized",
            "assumption": "one D_GK component receives amplitude/length/unit map",
            "expected": "first source-ready nonclaim bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case_id == "CASE4027_0_tracefree_signed":
            verdict = "TRACEFREE_COMPONENT_CAN_CLOSE_IF_SIGNED"
            next_action = "then check remaining kernels and observable projectors"
        elif case_id == "CASE4027_1_current_state":
            verdict = "KHAT_INCOMPLETE_DGK_BOUND_BRANCH_ACTIVE"
            next_action = "4028 trace-free parent sign or first normalized bound row"
        else:
            verdict = "FIRST_BOUND_ROW_WOULD_BE_SOURCE_READY"
            next_action = "run PPN/R10 comparison only after official map exists"
        rows.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4027",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4027_0_component_gate",
            "decision": "split Khat completion into trace-free, volume, chain, connection, domain, boundary and projector components",
            "rationale": "full Khat equality cannot be claimed as one blob",
            "effect": "each missing component now has a completion or bound route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4027_1_best_route",
            "decision": "prioritize trace-free improvement parent signing",
            "rationale": "it has the strongest existing algebraic evidence and least-scrutiny completion path",
            "effect": "4028 gets a sharp derivation target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4027_2_bound_normalization",
            "decision": "normalize D_GK components but keep them non-score-ready",
            "rationale": "amplitudes, units and projector maps are still missing",
            "effect": "no fake numeric pass; rows are ready for source inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4027_3_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "next step should either sign the trace-free component or produce the first normalized bound row",
            "effect": "derivation and empirical fallback remain coupled",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4027_0_Khat_complete",
            "claim": "Khat equals full K_Gamma",
            "allowed": False,
            "reason": "volume, chain, connection, domain, boundary and projector components remain unsigned or unnormalized",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4027_1_tracefree_live",
            "claim": "trace-free improvement component is live parent-signed",
            "allowed": False,
            "reason": "formal route exists but parent action, coefficient and boundary convention are not sourced",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4027_2_DGK_bound_pass",
            "claim": "D_GK bound passes PPN/R10",
            "allowed": False,
            "reason": "component rows are normalized schematically but not source-ready/numeric",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4027_3_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "q_loc/D_GK/Khat completion remains open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4027_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "attempt to parent-sign the trace-free improvement route for Khat; if unsigned, produce the first source-ready D_GK bound row, preferably C_beta_qloc or D_A_grad normalization",
            "success_condition": "trace-free component becomes live conditional theorem-zero, or one normalized D_GK row gains units/source path/observable projector status",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "Khat components split; trace-free improvement selected as first completion target; D_GK normalization rows emitted",
            "current_best_route": "trace-free improvement parent sign, else C_beta/D_A_grad first bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current = next(row for row in results if row["case_id"] == "CASE4027_1_current_state")
    DOC_PATH.write_text(
        f"""# 4027 - Khat Component Completion Or D_GK Bound Normalization

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The full `Khat = K_Gamma` question is now split into components:

- trace-free improvement/Hessian response;
- volume/trace response;
- `m` and `L_cg` chain response;
- connection/covariant-derivative response;
- domain/projection support response;
- boundary/reference/corner response;
- observable projector maps.

## Best Route

The best derivation target is the trace-free improvement route:

`K_L^{{mu nu}} = 2[nabla^mu nabla^nu phi - (1/4)g^{{mu nu}} Box phi]`.

This is the only component with a concrete algebraic shape match. It still needs:

- parent action term `int sqrt|g| c_I phi R`;
- phi owner;
- coefficient/sign convention;
- boundary term;
- live corpus adoption of `Khat^TF`.

## Bound Route

Everything not parent-signed remains in:

`A_DGK/L_DGK <= sum_i A_i/L_i`.

The active components are:

`D_trace`, `D_A_grad`, `D_gamma/cross/mass`, `D_boundary`, and projector maps `C_beta_qloc`, `C_R10_qloc(lambda)`.

## Current Verdict

- Current evaluator result: `{current["verdict"]}`.
- Claim result: `{current["claim_result"]}`.
- Source needles found: `{source_hits}/{source_total}`.

## Next Target

- `{NEXT_DOC}`
- `{NEXT_SCRIPT}`
""",
        encoding="utf-8",
    )


def append_spine(timestamp: str) -> None:
    marker = "## 4027 - Khat Component Gate"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: split full `Khat=K_Gamma` into trace-free, volume, chain, connection, domain, boundary and projector components.
- Best derivation target: trace-free improvement route `K_L^{{mu nu}}=2[nabla^mu nabla^nu phi-(1/4)g^{{mu nu}}Box phi]`.
- Bound fallback: `A_DGK/L_DGK <= sum_i A_i/L_i`; active components are trace, A-gradient, gamma/cross/mass, boundary and projector maps.
- No claim: no component is live parent-signed or score-ready.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4027 - Khat Component Gate" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    component_gate: list[dict[str, Any]],
    completion: list[dict[str, Any]],
    bound_norm: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4027_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4027_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, component_id in enumerate(
        ["KCG4027_0_tracefree_improvement", "KCG4027_1_volume_trace", "KCG4027_2_chain_m_L", "KCG4027_3_connection", "KCG4027_4_domain", "KCG4027_5_boundary", "KCG4027_6_projectors"],
        start=2,
    ):
        add(f"VAL4027_{idx:02d}_component", any(row["component_id"] == component_id for row in component_gate), f"{component_id} present")
    add("VAL4027_09_tracefree_conditional", any(row["component_id"] == "KCG4027_0_tracefree_improvement" and row["completion_status"] == "conditional_path_exists_not_parent_signed" for row in component_gate), "trace-free route conditional")
    add("VAL4027_10_other_open", all(row["completion_status"] != "complete" for row in component_gate), "no component marked complete")
    for idx, completion_id in enumerate(["COMP4027_0_tracefree_route", "COMP4027_1_volume_subtraction", "COMP4027_2_nohair_chain"], start=11):
        add(f"VAL4027_{idx:02d}_completion", any(row["completion_id"] == completion_id for row in completion), f"{completion_id} present")
    for idx, norm_id in enumerate(["NORM4027_0_master", "NORM4027_1_trace", "NORM4027_2_A_grad", "NORM4027_3_gamma_cross_mass", "NORM4027_4_boundary", "NORM4027_5_observable_maps"], start=14):
        add(f"VAL4027_{idx:02d}_norm", any(row["norm_id"] == norm_id for row in bound_norm), f"{norm_id} present")
    add("VAL4027_20_priority_tracefree", priority[0]["target"] == "trace-free improvement parent signing", "trace-free selected first")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4027_21_current_case", result_lookup["CASE4027_1_current_state"]["verdict"] == "KHAT_INCOMPLETE_DGK_BOUND_BRANCH_ACTIVE", "current case keeps bound branch active")
    add("VAL4027_22_trace_case", result_lookup["CASE4027_0_tracefree_signed"]["verdict"] == "TRACEFREE_COMPONENT_CAN_CLOSE_IF_SIGNED", "trace case defined")
    add("VAL4027_23_bound_case", result_lookup["CASE4027_2_bound_normalized"]["verdict"] == "FIRST_BOUND_ROW_WOULD_BE_SOURCE_READY", "bound row case defined")
    add("VAL4027_24_decision_best", any(row["decision_id"] == "DEC4027_1_best_route" for row in decisions), "best route decision recorded")
    add("VAL4027_25_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates false")
    add("VAL4027_26_norm_not_ready", all(str(row.get("score_ready", "")).lower() == "false" for row in bound_norm), "normalization rows not score-ready")
    add("VAL4027_27_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    output_tables = [
        sources,
        component_gate,
        completion,
        bound_norm,
        priority,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4027_28_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4027_29_doc_exists", DOC_PATH.exists() and "trace-free improvement route" in read_text(DOC_PATH), "document written with trace-free route")
    add("VAL4027_30_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4027_31_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4027_32_compile", compile_ok, "script compiles")
    add("VAL4027_33_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4027_34_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4027_35_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4027_36_overclaim_block", any(row["claim_id"] == "CLAIM4027_0_Khat_complete" and str(row["allowed"]).lower() == "false" for row in claims), "Khat overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    component_gate = component_gate_rows(timestamp)
    completion = completion_rows(timestamp)
    bound_norm = bound_norm_rows(timestamp)
    priority = priority_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["component_gate"], component_gate)
    write_csv(OUTPUTS["completion"], completion)
    write_csv(OUTPUTS["bound_norm"], bound_norm)
    write_csv(OUTPUTS["priority"], priority)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, component_gate, completion, bound_norm, priority, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4027 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
