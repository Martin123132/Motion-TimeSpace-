from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4025"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4025-Y5-R2FR-response-field-owner-construction-or-DGK-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
COMPACT_SHELL_PROXY = 7.432631961576971e-06

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4025_SOURCE_REGISTER.csv",
    "owner": SRC / "P8_Y5_R2FR_4025_RESPONSE_FIELD_OWNER_CONTRACT.csv",
    "theorem": SRC / "P8_Y5_R2FR_4025_METRIC_RESPONSE_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4025_OWNER_ADOPTION_AUDIT.csv",
    "bound": SRC / "P8_Y5_R2FR_4025_DGK_BOUND_FILL_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4025_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4025_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4025_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4025_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4025_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4025_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4025_VALIDATION.csv",
}

NEXT_DOC = "4026-Y5-R2FR-explicit-Gamma-density-or-DGK-profile-input-acquisition.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4026_explicit_Gamma_density_or_DGK_profile_input_acquisition.py"


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
        ("SRC4025_00_handoff", SRC / "P8_Y5_R2FR_4024_NEXT_TARGET.csv", "NEXT4024_0", "4024 handoff"),
        ("SRC4025_01_symbol", SRC / "P8_Y5_R2FR_4024_GK_SYMBOL_MATCH_MATRIX.csv", "SM4024_6_current_verdict", "4024 symbol verdict"),
        ("SRC4025_02_template", SRC / "P8_Y5_R2FR_4024_RESPONSE_FIELD_TEMPLATE_ROUTE.csv", "RFT4024_0_parent_field", "4024 response template"),
        ("SRC4025_03_bound", SRC / "P8_Y5_R2FR_4024_QLOC_PROFILE_BOUND_RUNNER_ROWS.csv", "QRUN4024_1_DGK_profile", "4024 DGK runner row"),
        ("SRC4025_04_noether", SRC / "P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv", "N1_parent_response_identity", "Noether response identity template"),
        ("SRC4025_05_candidates", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_A_metric_response_scalar_density", "GK action candidates"),
        ("SRC4025_06_decision", SRC / "P8_GK_STRESS_ACTION_DECISION.csv", "D514_0", "GK action decision"),
        ("SRC4025_07_gates", SRC / "P8_GK_STRESS_ACTION_GATE_TESTS.csv", "G514_2_current_MTS_match", "GK action gate tests"),
        ("SRC4025_08_contract", SRC / "P8_GK_METRIC_RESPONSE_CONTRACT.csv", "MR514_1_Khat_metric_response", "metric response contract"),
        ("SRC4025_09_audit", SRC / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", "MA515_1_Khat_metric_response", "metric response audit"),
        ("SRC4025_10_passfail", SRC / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv", "PF515_2_Khat_response_found", "pass/fail result"),
        ("SRC4025_11_stealth", SRC / "P8_Y5_GK_STRESS_2469_STEALTH_BRANCH_CONDITIONS.csv", "STL2469_6_conditional_result", "stress silence contract"),
        ("SRC4025_12_ppn", SRC / "P8_Y5_GK_STRESS_2469_PPN_RESIDUAL_LEDGER.csv", "PPN2469_2_hair_bound", "PPN stress residual ledger"),
        ("SRC4025_13_bound_dry", SRC / "P8_Y5_GK_BOUND_RUNNER_2474_DRY_RUN_INPUTS.csv", "DRY2474_1_PPN_toy_nonclaim", "older bound runner dry input"),
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


def owner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "OWN4025_0_response_field",
            "clause": "parent response carrier",
            "mathematical_form": "Introduce response carrier R_A and local fields Y^A on the observed branch; R_A is parent-owned, covariant, and varied before readout.",
            "closes": "Gamma/Khat are not post-readout knobs",
            "current_status": "candidate_contract_not_corpus_adopted",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "OWN4025_1_scalar_density",
            "clause": "Gamma scalar action density",
            "mathematical_form": "I_Gamma[g,Y,R]=int sqrt|g| Gamma_eff(g,Y,nablaY,R,D,topological data)",
            "closes": "SM4024_0_Gamma_owner if actual corpus supplies this density with units",
            "current_status": "constructed_contract_missing_actual_density",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "OWN4025_2_metric_response",
            "clause": "Khat as reduced metric response",
            "mathematical_form": "K_Gamma^{mu nu}:=-2 E_g^{mu nu}[Gamma_eff] where delta I_Gamma=int sqrt|g|[1/2 Gamma_eff g^{mu nu}+E_g^{mu nu}]delta g_{mu nu}+d theta_Gamma",
            "closes": "SM4024_1_Khat_response if Khat^{mu nu}=K_Gamma^{mu nu}+improvement_boundary_silent",
            "current_status": "constructed_contract_missing_actual_Khat_match",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "OWN4025_3_stress_identity",
            "clause": "Hilbert stress identity",
            "mathematical_form": "S_GK=-I_Gamma gives T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_Gamma^{mu nu}; D_GK=Gamma_eff g-Khat-T_can tracks mismatch",
            "closes": "q_loc Ward route if Khat=K_Gamma and T_can=T_GK through 2PN",
            "current_status": "exact_under_contract",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "OWN4025_4_fixed_point",
            "clause": "double-zero local fixed point",
            "mathematical_form": "Gamma_eff(Y0)=Gamma0, nabla Gamma0=0, K_Gamma(Y0)=Gamma0 g plus subtracted background, partial_A(T_GK)|Y0=0",
            "closes": "F_1=0 if actual Gamma/Khat expansion obeys the clause",
            "current_status": "candidate_clause_not_symbol_checked",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "OWN4025_5_noether",
            "clause": "Ward identity",
            "mathematical_form": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Y^A + E_R nabla^nu R + boundary/improvement terms",
            "closes": "q_loc=0 only if Euler, projector, and boundary terms are parent-zero or bounded",
            "current_status": "ownership_not_zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM4025_0_metric_response",
            "statement": "If I_Gamma is a covariant scalar-density action and Khat equals the reduced metric response K_Gamma, then S_GK=-I_Gamma has Hilbert stress Gamma_eff g-Khat.",
            "proof": "Vary I_Gamma: delta I_Gamma=int sqrt|g|[1/2 Gamma_eff g^{mu nu}+E_g^{mu nu}]delta g_{mu nu}+dtheta. With K_Gamma=-2E_g, the Hilbert stress of -I_Gamma is Gamma_eff g^{mu nu}-K_Gamma^{mu nu}.",
            "result": "D_GK=0 under exact owner/match convention",
            "status": "exact_conditional_theorem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "THM4025_1_Ward_zero",
            "statement": "If the response carrier equations hold, P_loc is parent-owned, and boundary flux vanishes, q_loc is zero on shell.",
            "proof": "Diffeomorphism invariance gives divergence of Hilbert stress as Euler terms plus boundary/improvement terms. On shell and with owned projection/no-flux, P_loc annihilates the remaining divergence.",
            "result": "q_loc=0 is derivable without a plateau axiom only under the owner clauses",
            "status": "exact_conditional_theorem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "THM4025_2_noether_guard",
            "statement": "Noether ownership alone does not prove local-GR recovery.",
            "proof": "The Noether audit gives conservation/exchange ownership but not J_Y=0, B_Y=0, no-hair, or stress silence. Homogeneous stress can survive even when q_loc current is zero.",
            "result": "must retain D_GK/Euler/boundary bound rows unless all owner clauses pass",
            "status": "anti_overclaim_guard",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "AUD4025_0_Gamma_density",
            "requirement": "actual MTS corpus supplies Gamma_eff(g,Y,nablaY,R,D,...) as scalar density with units",
            "current_evidence": "not found in prior symbol/match audits",
            "verdict": "not_adopted",
            "next_action": "4026 must propose explicit Gamma_eff density or demote Gamma contribution to A_DGK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4025_1_Khat_response",
            "requirement": "actual Khat equals K_Gamma plus boundary-silent improvement",
            "current_evidence": "Khat appears as symbol/identity target, not live metric response",
            "verdict": "not_adopted",
            "next_action": "compute K_Gamma from proposed density and compare component by component",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4025_2_double_zero",
            "requirement": "actual Gamma/Khat expansion has no linear local fixed-point stress",
            "current_evidence": "candidate clause exists, symbol expansion not checked",
            "verdict": "unverified",
            "next_action": "Taylor-expand actual density or fill F_1 profile coefficient",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4025_3_boundary_projector",
            "requirement": "P_loc and boundary term are parent-owned/no-flux",
            "current_evidence": "boundary/projector gates remain open",
            "verdict": "open",
            "next_action": "derive no-flux or carry compact-shell proxy with unit map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4025_4_current_verdict",
            "requirement": "all owner clauses live",
            "current_evidence": "AUD4025_0 and AUD4025_1 fail adoption",
            "verdict": "owner_contract_written_not_live",
            "next_action": "response-field construction attempt or DGK bound fill",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DGKB4025_0_master",
            "quantity": "Q_loc_envelope",
            "formula": "Q_loc <= C_Ploc*(A_DGK/L_DGK + A_Euler/L_Euler + A_boundary/L_boundary)",
            "source_status": "schema_ready_not_numeric",
            "needed_inputs": "C_Ploc; A_DGK; L_DGK; A_Euler; L_Euler; A_boundary; L_boundary",
            "observable_map": "delta_beta_q_loc; alpha_q(lambda); source-exchange",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGKB4025_1_A_DGK",
            "quantity": "A_DGK/L_DGK",
            "formula": "||nabla_mu[Gamma_eff g^{mu nu}-Khat^{mu nu}-T_can^{mu nu}]||",
            "source_status": "requires explicit Gamma density or component mismatch profile",
            "needed_inputs": "component norm, length scale, units relative to EH source",
            "observable_map": "PPN beta/gamma q_loc tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGKB4025_2_A_Euler",
            "quantity": "A_Euler/L_Euler",
            "formula": "sum_A |E_A||nablaY^A| plus response-carrier source forcing",
            "source_status": "requires local source-silence/no-hair or forcing profile",
            "needed_inputs": "Euler residual, field-gradient scale, no-hair constants",
            "observable_map": "fifth-force/source-exchange",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGKB4025_3_boundary",
            "quantity": "A_boundary/L_boundary",
            "formula": "boundary_flux_GK or compact-shell leakage proxy",
            "source_status": f"proxy_available_{COMPACT_SHELL_PROXY}_not_unit_mapped",
            "needed_inputs": "boundary normalization, PPN map, source-measure frame",
            "observable_map": "alpha3; GM drift; beta/gamma boundary tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGKB4025_4_C_beta",
            "quantity": "C_beta_qloc",
            "formula": "delta_beta_q_loc=C_beta_qloc*Q_loc",
            "source_status": "missing PPN projector normalization",
            "needed_inputs": "weak-field solution/projector from q_loc source to beta",
            "observable_map": "PPN beta",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "DGKB4025_5_C_R10",
            "quantity": "C_R10_qloc(lambda)",
            "formula": "alpha_q(lambda)=C_R10_qloc(lambda)*Q_loc",
            "source_status": "missing finite-range profile map",
            "needed_inputs": "lambda profile, Yukawa/non-Yukawa mapping, source normalization",
            "observable_map": "R10 alpha(lambda)",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4025_0_owner_adopted",
            "assumption": "Gamma density and Khat metric response are live corpus definitions",
            "expected": "D_GK=0 and q_loc zero route reopens after Euler/projector/boundary checks",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4025_1_current_state",
            "assumption": "owner contract is constructed but not adopted by current corpus",
            "expected": "D_GK bound fill remains active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4025_2_density_proposed_next",
            "assumption": "4026 proposes explicit Gamma density",
            "expected": "compute K_Gamma and test Khat equality",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4025_3_density_fails",
            "assumption": "no scalar density owner can be made compatible",
            "expected": "fill A_DGK/L_DGK and PPN/R10 maps as residual bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case_id == "CASE4025_0_owner_adopted":
            verdict = "OWNER_WOULD_ZERO_DGK_CONDITIONALLY"
            next_action = "then close Euler/projector/boundary gates"
        elif case_id == "CASE4025_1_current_state":
            verdict = "OWNER_CONTRACT_WRITTEN_NOT_LIVE"
            next_action = "4026 explicit Gamma density or DGK profile inputs"
        elif case_id == "CASE4025_2_density_proposed_next":
            verdict = "NEXT_DERIVATION_ROUTE_DEFINED"
            next_action = "compute K_Gamma from explicit density"
        else:
            verdict = "DGK_BOUND_FILL_REQUIRED"
            next_action = "fill A_DGK/L_DGK, C_beta_qloc, C_R10_qloc",
        rows.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4025",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4025_0_owner_contract",
            "decision": "wrote explicit metric-response owner contract",
            "rationale": "this is the exact condition under which Gamma_eff/Khat become one variational object",
            "effect": "the derivation route is now concrete rather than symbolic",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4025_1_not_live",
            "decision": "do not mark the owner as adopted",
            "rationale": "actual Gamma density and Khat metric-response definitions are still missing",
            "effect": "D_GK remains active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4025_2_bound_fill",
            "decision": "promoted D_GK bound rows into first fill schema",
            "rationale": "if the owner construction fails, q_loc must become empirically boundable",
            "effect": "next work has exact source inputs rather than vague residual language",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4025_3_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "4026 should either propose the explicit density or fill the bound inputs",
            "effect": "keeps derive-first and testability routes both alive",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4025_0_owner_adopted",
            "claim": "Gamma/Khat response owner is adopted by current corpus",
            "allowed": False,
            "reason": "owner contract is written but actual density/metric-response definitions are missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4025_1_DGK_zero",
            "claim": "D_GK=0",
            "allowed": False,
            "reason": "requires live Khat=K_Gamma and component match through local 2PN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4025_2_q_loc_zero",
            "claim": "q_loc=0",
            "allowed": False,
            "reason": "requires D_GK=0 plus Euler/projector/boundary gates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4025_3_bound_pass",
            "claim": "D_GK/q_loc bound passes PPN/R10",
            "allowed": False,
            "reason": "bound rows are schema-ready but not numeric/source-backed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4025_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "either propose an explicit Gamma_eff scalar density and compute K_Gamma for comparison with Khat, or fill source-ready D_GK profile inputs A_DGK/L_DGK plus C_beta_qloc and C_R10_qloc",
            "success_condition": "one of SM4024_0/1 becomes live through explicit density/response, or DGKB4025_1/4/5 become source-ready nonclaim bound rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "response-field owner contract derived; not adopted; D_GK bound fill schema hardened",
            "current_best_route": "explicit Gamma density then Khat metric-response comparison",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current = next(row for row in results if row["case_id"] == "CASE4025_1_current_state")
    DOC_PATH.write_text(
        f"""# 4025 - Response-Field Owner Construction Or D_GK Bound Fill

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

This checkpoint constructs the exact owner contract needed to make `Gamma_eff/Khat` a real variational object.

Let:

`I_Gamma[g,Y,R]=int sqrt|g| Gamma_eff(g,Y,nablaY,R,D,topological data)`.

Define the reduced metric response by:

`delta I_Gamma=int sqrt|g|[1/2 Gamma_eff g^{{mu nu}}+E_g^{{mu nu}}]delta g_{{mu nu}}+d theta_Gamma`,

`K_Gamma^{{mu nu}} := -2 E_g^{{mu nu}}`.

Then for `S_GK=-I_Gamma`, the Hilbert stress is:

`T_GK^{{mu nu}}=Gamma_eff g^{{mu nu}}-K_Gamma^{{mu nu}}`.

So if the actual corpus adopts:

`Khat^{{mu nu}}=K_Gamma^{{mu nu}} + boundary-silent improvement`,

then `D_GK=0` and the q_loc zero route reopens.

## Current Verdict

- Current evaluator result: `{current["verdict"]}`.
- Claim result: `{current["claim_result"]}`.
- Source needles found: `{source_hits}/{source_total}`.

The owner contract is exact, but it is **not live-adopted** by the current corpus because the explicit `Gamma_eff` density and `Khat=K_Gamma` component match are still missing.

## Bound Fill

If the owner route fails, the active bound schema is:

`Q_loc <= C_Ploc*(A_DGK/L_DGK + A_Euler/L_Euler + A_boundary/L_boundary)`.

The first missing source-ready rows are:

- `A_DGK/L_DGK`: component mismatch profile;
- `C_beta_qloc`: weak-field PPN beta projector;
- `C_R10_qloc(lambda)`: short-range/fifth-force profile map.

## Next Target

- `{NEXT_DOC}`
- `{NEXT_SCRIPT}`
""",
        encoding="utf-8",
    )


def append_spine(timestamp: str) -> None:
    marker = "## 4025 - Response-Field Owner Contract"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: derived exact owner contract: `I_Gamma=int sqrt|g| Gamma_eff`, `K_Gamma^{{mu nu}}=-2E_g^{{mu nu}}`, and `S_GK=-I_Gamma` gives `T_GK^{{mu nu}}=Gamma_eff g^{{mu nu}}-K_Gamma^{{mu nu}}`.
- If actual `Khat=K_Gamma` plus boundary-silent improvement, then `D_GK=0` and the q_loc Ward route reopens.
- Guard: current corpus has not supplied the explicit `Gamma_eff` density or component match, so no `D_GK=0` or q_loc-zero claim.
- Bound fallback hardened: `Q_loc <= C_Ploc*(A_DGK/L_DGK + A_Euler/L_Euler + A_boundary/L_boundary)`.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4025 - Response-Field Owner Contract" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4025_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4025_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, owner_id in enumerate(["OWN4025_0_response_field", "OWN4025_1_scalar_density", "OWN4025_2_metric_response", "OWN4025_3_stress_identity", "OWN4025_4_fixed_point", "OWN4025_5_noether"], start=2):
        add(f"VAL4025_{idx:02d}_owner", any(row["owner_id"] == owner_id for row in owner), f"{owner_id} present")
    for idx, theorem_id in enumerate(["THM4025_0_metric_response", "THM4025_1_Ward_zero", "THM4025_2_noether_guard"], start=8):
        add(f"VAL4025_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    for idx, audit_id in enumerate(["AUD4025_0_Gamma_density", "AUD4025_1_Khat_response", "AUD4025_2_double_zero", "AUD4025_3_boundary_projector", "AUD4025_4_current_verdict"], start=11):
        add(f"VAL4025_{idx:02d}_audit", any(row["audit_id"] == audit_id for row in audit), f"{audit_id} present")
    for idx, bound_id in enumerate(["DGKB4025_0_master", "DGKB4025_1_A_DGK", "DGKB4025_2_A_Euler", "DGKB4025_3_boundary", "DGKB4025_4_C_beta", "DGKB4025_5_C_R10"], start=16):
        add(f"VAL4025_{idx:02d}_bound", any(row["bound_id"] == bound_id for row in bound), f"{bound_id} present")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4025_22_current_case", result_lookup["CASE4025_1_current_state"]["verdict"] == "OWNER_CONTRACT_WRITTEN_NOT_LIVE", "current case says owner not live")
    add("VAL4025_23_density_next", result_lookup["CASE4025_2_density_proposed_next"]["verdict"] == "NEXT_DERIVATION_ROUTE_DEFINED", "density route defined")
    add("VAL4025_24_bound_case", result_lookup["CASE4025_3_density_fails"]["verdict"] == "DGK_BOUND_FILL_REQUIRED", "bound fallback case defined")
    add("VAL4025_25_audit_not_adopted", any(row["audit_id"] == "AUD4025_4_current_verdict" and row["verdict"] == "owner_contract_written_not_live" for row in audit), "owner not adopted recorded")
    add("VAL4025_26_decision_owner", any(row["decision_id"] == "DEC4025_0_owner_contract" for row in decisions), "owner decision recorded")
    add("VAL4025_27_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates false")
    add("VAL4025_28_bound_not_ready", all(str(row.get("score_ready", "")).lower() == "false" for row in bound), "bound rows not score-ready")
    add("VAL4025_29_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    output_tables = [
        sources,
        owner,
        theorem,
        audit,
        bound,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4025_30_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4025_31_doc_exists", DOC_PATH.exists() and "owner contract is exact" in read_text(DOC_PATH), "document written with owner verdict")
    add("VAL4025_32_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4025_33_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4025_34_compile", compile_ok, "script compiles")
    add("VAL4025_35_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4025_36_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4025_37_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4025_38_overclaim_block", any(row["claim_id"] == "CLAIM4025_2_q_loc_zero" and str(row["allowed"]).lower() == "false" for row in claims), "q_loc overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    owner = owner_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bound = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["owner"], owner)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
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

    validation = build_validation_rows(timestamp, sources, owner, theorem, audit, bound, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4025 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
