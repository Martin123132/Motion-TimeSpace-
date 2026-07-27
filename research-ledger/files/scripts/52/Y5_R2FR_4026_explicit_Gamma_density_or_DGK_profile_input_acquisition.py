from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4026"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4026-Y5-R2FR-explicit-Gamma-density-or-DGK-profile-input-acquisition.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4026_SOURCE_REGISTER.csv",
    "density": SRC / "P8_Y5_R2FR_4026_EXPLICIT_GAMMA_DENSITY_CANDIDATE.csv",
    "response": SRC / "P8_Y5_R2FR_4026_KGAMMA_RESPONSE_COMPONENTS.csv",
    "match": SRC / "P8_Y5_R2FR_4026_KHAT_COMPONENT_MATCH_AUDIT.csv",
    "bound": SRC / "P8_Y5_R2FR_4026_DGK_PROFILE_INPUT_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4026_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4026_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4026_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4026_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4026_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4026_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4026_VALIDATION.csv",
}

NEXT_DOC = "4027-Y5-R2FR-Khat-component-completion-or-DGK-bound-normalization.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4027_Khat_component_completion_or_DGK_bound_normalization.py"
COMPACT_SHELL_PROXY = 7.432631961576971e-06


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
        ("SRC4026_00_handoff", SRC / "P8_Y5_R2FR_4025_NEXT_TARGET.csv", "NEXT4025_0", "4025 handoff"),
        ("SRC4026_01_owner", SRC / "P8_Y5_R2FR_4025_RESPONSE_FIELD_OWNER_CONTRACT.csv", "OWN4025_1_scalar_density", "4025 owner contract"),
        ("SRC4026_02_theorem", SRC / "P8_Y5_R2FR_4025_METRIC_RESPONSE_THEOREM.csv", "THM4025_0_metric_response", "metric response theorem"),
        ("SRC4026_03_bound", SRC / "P8_Y5_R2FR_4025_DGK_BOUND_FILL_ROWS.csv", "DGKB4025_1_A_DGK", "D_GK bound row"),
        ("SRC4026_04_operator", SRC / "P8_Y5_GK_OPERATOR_2471_OPERATOR_ANSATZ.csv", "OP2471_0_stationary_energy", "explicit quadratic GK ansatz"),
        ("SRC4026_05_dimensions", SRC / "P8_Y5_GK_OPERATOR_2471_DIMENSION_SIGN_TABLE.csv", "DS2471_4_ZG", "dimension/sign table"),
        ("SRC4026_06_nohair", SRC / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv", "NHG2471_5_eligibility", "nohair eligibility"),
        ("SRC4026_07_verdict", SRC / "P8_Y5_GK_OPERATOR_2471_PROMOTION_VERDICT.csv", "PV2471_4_overall", "2471 verdict"),
        ("SRC4026_08_stealth", SRC / "P8_Y5_GK_STRESS_2469_STEALTH_BRANCH_CONDITIONS.csv", "STL2469_4_positive_gap", "stealth/nohair conditions"),
        ("SRC4026_09_ppn", SRC / "P8_Y5_GK_STRESS_2469_PPN_RESIDUAL_LEDGER.csv", "PPN2469_2_hair_bound", "PPN residual ledger"),
        ("SRC4026_10_match", SRC / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", "MA515_1_Khat_metric_response", "metric response match audit"),
        ("SRC4026_11_bound_runner", SRC / "P8_Y5_R2FR_4024_QLOC_PROFILE_BOUND_RUNNER_ROWS.csv", "QRUN4024_4_delta_beta_map", "q_loc beta map"),
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


def density_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "density_id": "DEN4026_0_fields",
            "piece": "response fields",
            "mathematical_form": "Y^A=(A_mu,gamma), gamma:=Gamma_eff-Gamma_0, with local fixed point A_mu=0, gamma=0",
            "meaning": "minimal response-carrier content from the older GK ansatz",
            "status": "candidate_nonclaim",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "DEN4026_1_density",
            "piece": "explicit Gamma density ansatz",
            "mathematical_form": "Gamma_quad=Gamma_0 + 1/2 Z_A nabla_mu A_nu nabla^mu A^nu + 1/2 m_A^2 A_mu A^mu + 1/2 Z_G nabla_mu gamma nabla^mu gamma + 1/2 m_G^2 gamma^2 + c_AG A^mu nabla_mu gamma",
            "meaning": "covariant lift of the 2471 stationary quadratic operator; total derivatives/improvements kept separate",
            "status": "candidate_density_not_corpus_adopted",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "DEN4026_2_subtraction",
            "piece": "vacuum subtraction",
            "mathematical_form": "Gamma_0 is fixed background/cosmological subtraction; local force uses nabla Gamma_0=0 and delta Gamma_0 excluded from compact local source readout",
            "meaning": "prevents constant vacuum energy from masquerading as local mass/source stress",
            "status": "required_clause",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "DEN4026_3_coercivity",
            "piece": "sign/gap conditions",
            "mathematical_form": "Z_A>0, Z_G>0, m_A^2>=0, m_G^2>=0, and cross term bounded by |c_AG|^2 < Z_A*m_G^2 or equivalent positive-block condition",
            "meaning": "would support local no-hair/positive energy route",
            "status": "plausible_sign_contract_not_parent_derived",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "DEN4026_4_verdict",
            "piece": "density verdict",
            "mathematical_form": "Gamma_quad is explicit enough to compute K_Gamma, but not enough to claim MTS owns Gamma_eff",
            "meaning": "use for component audit and D_GK fill, not public local-GR proof",
            "status": "candidate_useful_not_live",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def response_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "response_id": "KGR4026_0_trace_potential",
            "component": "trace/potential response",
            "from_density": "Gamma_quad g^{mu nu} contains Gamma_0, mass terms and potential trace pieces",
            "needed_in_Khat_or_DGK": "constant subtraction plus mass/potential trace response",
            "current_match": "not_found_as_live_Khat_component",
            "DGK_piece": "D_trace_potential",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "response_id": "KGR4026_1_A_gradient",
            "component": "A_mu gradient response",
            "from_density": "metric response of 1/2 Z_A nablaA.nablaA gives symmetric kinetic stress plus connection/boundary improvements",
            "needed_in_Khat_or_DGK": "full symmetric A-gradient response, not only schematic Z_A D^i A^j",
            "current_match": "shape_match_only_from_2471",
            "DGK_piece": "D_A_grad",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "response_id": "KGR4026_2_gamma_gradient",
            "component": "gamma gradient response",
            "from_density": "metric response of 1/2 Z_G nabla gamma.nabla gamma",
            "needed_in_Khat_or_DGK": "scalar gradient stress and trace",
            "current_match": "missing_live_Khat_component",
            "DGK_piece": "D_gamma_grad",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "response_id": "KGR4026_3_cross",
            "component": "A dot grad gamma cross response",
            "from_density": "metric response of c_AG A^mu nabla_mu gamma plus boundary/improvement terms",
            "needed_in_Khat_or_DGK": "cross stress, sign convention, and parent normalization",
            "current_match": "risk_term_not_parent_completed",
            "DGK_piece": "D_cross_AG",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "response_id": "KGR4026_4_mass",
            "component": "mass/gap response",
            "from_density": "metric response of 1/2 m_A^2 A^2 + 1/2 m_G^2 gamma^2",
            "needed_in_Khat_or_DGK": "mass trace and A_mu A_nu stress pieces",
            "current_match": "missing_live_Khat_component",
            "DGK_piece": "D_mass_gap",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "response_id": "KGR4026_5_boundary",
            "component": "boundary/improvement response",
            "from_density": "metric variation of derivative terms produces theta_Gamma and possible improvement terms",
            "needed_in_Khat_or_DGK": "boundary-silent theorem or explicit boundary flux row",
            "current_match": "open_boundary_projector_gate",
            "DGK_piece": "D_boundary_improvement",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def match_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "match_id": "KM4026_0_density_available",
            "test": "explicit Gamma density exists",
            "result": "pass_as_candidate",
            "evidence": "DEN4026_1_density",
            "claim_effect": "does not prove corpus adoption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "KM4026_1_Khat_full_response",
            "test": "actual Khat contains every KGR4026 response component through local 2PN",
            "result": "fail_current_claim",
            "evidence": "only A-gradient shape match found; trace/gamma/cross/mass/boundary components missing or unsigned",
            "claim_effect": "D_GK remains nonzero/unbounded",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "KM4026_2_double_zero",
            "test": "Gamma_quad local fixed point gives no linear stress",
            "result": "pass_under_candidate_if_coefficients_parent_signed",
            "evidence": "quadratic density and vacuum subtraction",
            "claim_effect": "not live until parent signs coefficients and boundary conditions",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "KM4026_3_nohair",
            "test": "positive/gapped exterior forces A=0,gamma=0",
            "result": "plausible_not_proved",
            "evidence": "2471 sign contract and 2469 stealth/nohair conditions",
            "claim_effect": "requires parent signs, boundary/topology, and source silence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "KM4026_4_bound_fallback",
            "test": "missing Khat components are routed to D_GK bound rows",
            "result": "pass_nonclaim",
            "evidence": "DGK4026 profile rows",
            "claim_effect": "testable fallback exists but not numeric",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DGK4026_0_D_trace_potential",
            "component": "D_trace_potential",
            "formula": "missing/unsigned Gamma0, mass, and potential trace response contribution to D_GK",
            "source_or_input_needed": "vacuum subtraction and mass/potential response ownership",
            "current_value": "SYMBOLIC_COMPONENT_NOT_NUMERIC",
            "maps_to": "A_DGK/L_DGK; beta/gamma source tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGK4026_1_D_A_grad",
            "component": "D_A_grad",
            "formula": "full A-gradient metric response minus actual Khat A-gradient component",
            "source_or_input_needed": "symmetric/projected Khat component, coefficient Z_A, length scale L_A",
            "current_value": "SHAPE_MATCH_ONLY_NOT_NUMERIC",
            "maps_to": "A_DGK/L_DGK; preferred-frame/q_loc tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGK4026_2_D_gamma_grad",
            "component": "D_gamma_grad",
            "formula": "Z_G scalar-gradient response not matched by live Khat",
            "source_or_input_needed": "Z_G, gamma profile amplitude, length scale L_gamma",
            "current_value": "MISSING_COMPONENT",
            "maps_to": "A_DGK/L_DGK; R10 scalar-profile map",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGK4026_3_D_cross_AG",
            "component": "D_cross_AG",
            "formula": "metric response of c_AG A^mu nabla_mu gamma minus any adopted cross Khat component",
            "source_or_input_needed": "c_AG normalization/sign and cross profile",
            "current_value": "RISK_TERM_UNSIGNED",
            "maps_to": "local hair/source-exchange; R10/PPN cross tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGK4026_4_D_mass_gap",
            "component": "D_mass_gap",
            "formula": "m_A^2 A_mu A_nu and m_G^2 gamma^2 trace response mismatch",
            "source_or_input_needed": "m_A^2,m_G^2,parent scale and profile amplitudes",
            "current_value": "MISSING_PARENT_SIGN_AND_SCALE",
            "maps_to": "nohair/leakage envelope",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGK4026_5_D_boundary_improvement",
            "component": "D_boundary_improvement",
            "formula": "theta_Gamma/improvement flux contribution, with compact-shell proxy available",
            "source_or_input_needed": "boundary no-flux theorem or unit map for compact-shell proxy",
            "current_value": f"PROXY_{COMPACT_SHELL_PROXY}_UNMAPPED",
            "maps_to": "alpha3; GM drift; beta/gamma boundary tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGK4026_6_C_beta_C_R10",
            "component": "observable projectors",
            "formula": "delta_beta_q_loc=C_beta_qloc*Q_loc; alpha_q(lambda)=C_R10_qloc(lambda)*Q_loc",
            "source_or_input_needed": "weak-field beta projector and finite-range profile map",
            "current_value": "MISSING_PROJECTOR_MAPS",
            "maps_to": "PPN/R10 acceptance",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4026_0_full_component_match",
            "assumption": "actual Khat supplies every KGR4026 component with parent-signed coefficients",
            "expected": "D_GK=0 candidate route can be promoted to next Euler/projector tests",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4026_1_current_state",
            "assumption": "Gamma_quad exists only as candidate and Khat has partial shape match",
            "expected": "D_GK component bound rows remain active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4026_2_parent_signs_density",
            "assumption": "parent signs Z/m/c coefficients and boundary topology",
            "expected": "nohair route becomes plausible and component match can be retried",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4026_3_match_fails",
            "assumption": "Khat remains only partial response",
            "expected": "fill D_trace, D_gamma, D_cross, D_mass, D_boundary plus C_beta/C_R10",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case_id == "CASE4026_0_full_component_match":
            verdict = "DGK_ZERO_IF_ALL_COMPONENTS_MATCH"
            next_action = "then close Euler/projector/boundary gates"
        elif case_id == "CASE4026_1_current_state":
            verdict = "EXPLICIT_DENSITY_CANDIDATE_BUT_KHAT_INCOMPLETE"
            next_action = "4027 component completion or DGK bound normalization"
        elif case_id == "CASE4026_2_parent_signs_density":
            verdict = "PARENT_SIGN_ROUTE_DEFINED"
            next_action = "source coefficient signs/scales and boundary topology",
        else:
            verdict = "DGK_COMPONENT_BOUND_REQUIRED"
            next_action = "fill component amplitudes and PPN/R10 maps"
        rows.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4026",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4026_0_density_candidate",
            "decision": "promoted the 2471 quadratic GK operator into an explicit Gamma density candidate",
            "rationale": "it is the best available concrete density for testing the 4025 owner equation",
            "effect": "K_Gamma can now be split into response components",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4026_1_match_fails",
            "decision": "current Khat evidence does not contain the full metric response",
            "rationale": "only partial A-gradient shape match is present; trace/gamma/cross/mass/boundary pieces are missing or unsigned",
            "effect": "D_GK remains active and componentized",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4026_2_bound_inputs",
            "decision": "split A_DGK into component rows",
            "rationale": "componentized D_GK can be bounded or completed one piece at a time",
            "effect": "4027 has a concrete fill/completion target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4026_3_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "next step must either complete Khat components or normalize the DGK bound rows",
            "effect": "derive-first and bound-first paths remain explicit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4026_0_density_adopted",
            "claim": "Gamma_quad is the live MTS Gamma_eff density",
            "allowed": False,
            "reason": "density is a candidate ansatz, not parent-signed corpus action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4026_1_Khat_match",
            "claim": "Khat equals K_Gamma through local 2PN",
            "allowed": False,
            "reason": "full response components are not live-matched",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4026_2_DGK_zero",
            "claim": "D_GK=0",
            "allowed": False,
            "reason": "D_trace/D_gamma/D_cross/D_mass/D_boundary components remain open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4026_3_bound_pass",
            "claim": "D_GK bound passes PPN/R10",
            "allowed": False,
            "reason": "component amplitudes and C_beta/C_R10 maps are not numeric/source-backed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4026_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "either complete live Khat components for Gamma_quad response, or normalize D_GK component-bound rows with amplitudes, units, and PPN/R10 projector maps",
            "success_condition": "one Khat component is parent-completed or at least one D_GK component row becomes source-ready with declared units and observable map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "explicit Gamma density candidate written; Khat full response fails current match; D_GK component rows emitted",
            "current_best_route": "complete Khat response components or normalize D_GK bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current = next(row for row in results if row["case_id"] == "CASE4026_1_current_state")
    DOC_PATH.write_text(
        f"""# 4026 - Explicit Gamma Density Or D_GK Profile Input Acquisition

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The best explicit candidate density is now written:

`Gamma_quad = Gamma_0 + 1/2 Z_A nabla_mu A_nu nabla^mu A^nu + 1/2 m_A^2 A_mu A^mu + 1/2 Z_G nabla_mu gamma nabla^mu gamma + 1/2 m_G^2 gamma^2 + c_AG A^mu nabla_mu gamma`,

with `gamma := Gamma_eff - Gamma_0`.

This is a covariant lift of the older stationary quadratic GK operator. It is useful because it lets us compute what `K_Gamma` must contain.

## Match Verdict

Current `Khat` evidence does **not** contain the full metric response of `Gamma_quad`.

The open/missing response pieces are:

- trace/potential response;
- full symmetric `A_mu` gradient response;
- `gamma` gradient response;
- `A dot grad gamma` cross response;
- mass/gap response;
- boundary/improvement response.

So `D_GK` is not zeroed.

## Bound Inputs

The mismatch is now componentized:

`D_GK = D_trace + D_A_grad + D_gamma_grad + D_cross_AG + D_mass_gap + D_boundary`.

These feed:

- `A_DGK/L_DGK`;
- `C_beta_qloc`;
- `C_R10_qloc(lambda)`.

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
    marker = "## 4026 - Explicit Gamma Density Candidate And DGK Components"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: explicit candidate `Gamma_quad` density written from the 2471 GK operator ansatz.
- Match verdict: current `Khat` only has partial shape evidence; full metric response components are missing or unsigned.
- `D_GK` is now split into `D_trace`, `D_A_grad`, `D_gamma_grad`, `D_cross_AG`, `D_mass_gap`, and `D_boundary`.
- No claim: `Gamma_quad` is candidate/nonclaim and `D_GK=0` is not proven.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4026 - Explicit Gamma Density Candidate And DGK Components" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    density: list[dict[str, Any]],
    response: list[dict[str, Any]],
    match: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4026_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4026_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, density_id in enumerate(["DEN4026_0_fields", "DEN4026_1_density", "DEN4026_2_subtraction", "DEN4026_3_coercivity", "DEN4026_4_verdict"], start=2):
        add(f"VAL4026_{idx:02d}_density", any(row["density_id"] == density_id for row in density), f"{density_id} present")
    add("VAL4026_07_density_not_signed", all(str(row.get("parent_signed", "")).lower() == "false" for row in density), "density rows not parent-signed")
    for idx, response_id in enumerate(["KGR4026_0_trace_potential", "KGR4026_1_A_gradient", "KGR4026_2_gamma_gradient", "KGR4026_3_cross", "KGR4026_4_mass", "KGR4026_5_boundary"], start=8):
        add(f"VAL4026_{idx:02d}_response", any(row["response_id"] == response_id for row in response), f"{response_id} present")
    add("VAL4026_14_khat_fail", any(row["match_id"] == "KM4026_1_Khat_full_response" and row["result"] == "fail_current_claim" for row in match), "Khat full response failure recorded")
    add("VAL4026_15_bound_fallback", any(row["match_id"] == "KM4026_4_bound_fallback" and row["result"] == "pass_nonclaim" for row in match), "bound fallback recorded")
    for idx, bound_id in enumerate(["DGK4026_0_D_trace_potential", "DGK4026_1_D_A_grad", "DGK4026_2_D_gamma_grad", "DGK4026_3_D_cross_AG", "DGK4026_4_D_mass_gap", "DGK4026_5_D_boundary_improvement", "DGK4026_6_C_beta_C_R10"], start=16):
        add(f"VAL4026_{idx:02d}_bound", any(row["bound_id"] == bound_id for row in bound), f"{bound_id} present")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4026_23_current_case", result_lookup["CASE4026_1_current_state"]["verdict"] == "EXPLICIT_DENSITY_CANDIDATE_BUT_KHAT_INCOMPLETE", "current case says Khat incomplete")
    add("VAL4026_24_match_fail_case", result_lookup["CASE4026_3_match_fails"]["verdict"] == "DGK_COMPONENT_BOUND_REQUIRED", "match failure routes to DGK components")
    add("VAL4026_25_decision_density", any(row["decision_id"] == "DEC4026_0_density_candidate" for row in decisions), "density decision recorded")
    add("VAL4026_26_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates false")
    add("VAL4026_27_bound_not_ready", all(str(row.get("score_ready", "")).lower() == "false" for row in bound), "bound rows not score-ready")
    add("VAL4026_28_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    output_tables = [
        sources,
        density,
        response,
        match,
        bound,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4026_29_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4026_30_doc_exists", DOC_PATH.exists() and "Gamma_quad" in read_text(DOC_PATH), "document written with Gamma density")
    add("VAL4026_31_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4026_32_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4026_33_compile", compile_ok, "script compiles")
    add("VAL4026_34_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4026_35_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4026_36_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4026_37_overclaim_block", any(row["claim_id"] == "CLAIM4026_2_DGK_zero" and str(row["allowed"]).lower() == "false" for row in claims), "D_GK overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    density = density_rows(timestamp)
    response = response_rows(timestamp)
    match = match_rows(timestamp)
    bound = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["density"], density)
    write_csv(OUTPUTS["response"], response)
    write_csv(OUTPUTS["match"], match)
    write_csv(OUTPUTS["bound"], bound)
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

    validation = build_validation_rows(timestamp, sources, density, response, match, bound, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4026 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
