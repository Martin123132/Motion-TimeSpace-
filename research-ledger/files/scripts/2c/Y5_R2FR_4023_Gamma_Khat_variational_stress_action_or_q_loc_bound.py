from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4023"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4023-Y5-R2FR-Gamma-Khat-variational-stress-action-or-q-loc-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4023_SOURCE_REGISTER.csv",
    "identity": SRC / "P8_Y5_R2FR_4023_QLOC_STRESS_IDENTITY.csv",
    "action": SRC / "P8_Y5_R2FR_4023_CANONICAL_SGK_ACTION_ATTEMPT.csv",
    "match": SRC / "P8_Y5_R2FR_4023_GK_MATCH_AND_HELMHOLTZ_GATES.csv",
    "theorem": SRC / "P8_Y5_R2FR_4023_QLOC_ZERO_THEOREM_OR_BOUND_FORK.csv",
    "bound": SRC / "P8_Y5_R2FR_4023_QLOC_BOUND_INTERFACE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4023_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4023_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4023_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4023_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4023_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4023_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4023_VALIDATION.csv",
}

NEXT_DOC = "4024-Y5-R2FR-GK-symbol-match-or-q-loc-profile-bound-runner.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4024_GK_symbol_match_or_q_loc_profile_bound_runner.py"


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
        ("SRC4023_00_handoff", SRC / "P8_Y5_R2FR_4022_NEXT_TARGET.csv", "NEXT4022_0", "4022 handoff"),
        ("SRC4023_01_survivor", SRC / "P8_Y5_R2FR_4022_SURVIVOR_PPN_ROUTE.csv", "SURV4022_10_Gamma_Khat_q_loc", "q_loc survivor route"),
        ("SRC4023_02_priority", SRC / "P8_Y5_R2FR_4022_FIRST_RESIDUAL_PRIORITY.csv", "PRI4022_0_first_target", "q_loc priority"),
        ("SRC4023_03_513_rewrite", SRC / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv", "SR513_0_define_extra_stress", "stress-divergence rewrite"),
        ("SRC4023_04_513_contract", SRC / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "GK513_0_action_existence", "GK action contract"),
        ("SRC4023_05_513_integrability", SRC / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv", "IG513_2_metric_variationality", "integrability gates"),
        ("SRC4023_06_513_demotion", SRC / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv", "QR513_0_nonvariational_stress", "residual demotion routes"),
        ("SRC4023_07_513_tests", SRC / "P8_GAMMA_KHAT_QLOC_GATE_TESTS.csv", "G513_0_algebraic_rewrite", "q_loc gate tests"),
        ("SRC4023_08_bound_spec", SRC / "P8_QLOC_BOUND_RUNNER_SPEC.csv", "QB516_0_compact_shell_budget", "q_loc bound spec"),
        ("SRC4023_09_trigger", SRC / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv", "BT517_0_owner_match_fails", "q_loc bound trigger"),
        ("SRC4023_10_nohair", SRC / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv", "NH1534_3_exact_nohair", "conditional no-hair theorem"),
        ("SRC4023_11_leakage", SRC / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv", "LEAK1534_6_verdict", "quadratic leakage bound"),
        ("SRC4023_12_exact_status", SRC / "P8_Y5_PARENT_QLOC_1535_EXACT_NOHAIR_STATUS.csv", "EH1535_4_verdict", "exact no-hair status"),
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


def identity_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "ID4023_0_define_TGK",
            "statement": "Define the effective Gamma-Khat stress tensor.",
            "mathematical_form": "T_GK^{mu nu}:=Gamma_eff g_obs^{mu nu}-Khat^{mu nu}",
            "result": "q_loc becomes a stress-divergence problem",
            "status": "exact_definition",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "identity_id": "ID4023_1_divergence",
            "statement": "For the observed Levi-Civita derivative, the divergence of T_GK is exactly the unprojected q_loc source.",
            "mathematical_form": "nabla_mu T_GK^{mu nu}=nabla^nu Gamma_eff-nabla_mu Khat^{mu nu}",
            "result": "q_loc^nu=P_loc nabla_mu T_GK^{mu nu}",
            "status": "exact_algebraic_identity",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "identity_id": "ID4023_2_Ward_route",
            "statement": "If T_GK is Hilbert stress of a diffeomorphism-invariant sector, its divergence is controlled by the Euler equations.",
            "mathematical_form": "T_GK^{mu nu}=(-2/sqrt|g|)delta S_GK/delta g_{mu nu}; nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Y^A + gauge identities",
            "result": "on shell, q_loc=0 if the projector and boundary terms are parent-owned",
            "status": "exact_conditional_Noether_route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "identity_id": "ID4023_3_mismatch",
            "statement": "If the canonical Hilbert stress does not equal Gamma_eff g-Khat, the mismatch is the physical residual.",
            "mathematical_form": "D_GK^{mu nu}:=Gamma_eff g^{mu nu}-Khat^{mu nu}-T_can^{mu nu}",
            "result": "q_loc=P_loc(sum_A E_A nablaY^A + nabla_mu D_GK^{mu nu}) plus boundary/improvement terms",
            "status": "exact_residual_split",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def action_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "action_id": "SGK4023_0_fields",
            "component": "local deviation fields",
            "mathematical_form": "Y^A=(local Gamma/Khat carrier fields) with fixed point Y^A=0 and V=ker(Dq)",
            "purpose": "make Gamma/Khat a parent-owned field sector rather than bookkeeping",
            "derivation_status": "candidate_sufficient_construction",
            "corpus_matched": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "SGK4023_1_action",
            "component": "canonical local Hilbert action",
            "mathematical_form": "S_can[Y,g]=int sqrt|g|[-1/2 H_AB(Y) g^{mu nu} nabla_mu Y^A nabla_nu Y^B - V(Y)] + dB_GK",
            "purpose": "guarantee metric variationality and Ward identity by construction",
            "derivation_status": "constructed_candidate_action",
            "corpus_matched": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "SGK4023_2_stress",
            "component": "canonical Hilbert stress",
            "mathematical_form": "T_can^{mu nu}=H_AB nabla^mu Y^A nabla^nu Y^B-g^{mu nu}[1/2 H_AB nabla_rho Y^A nabla^rho Y^B+V(Y)] + improvements",
            "purpose": "candidate target for T_GK=Gamma_eff g-Khat",
            "derivation_status": "exact_from_S_can",
            "corpus_matched": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "SGK4023_3_double_zero",
            "component": "fixed-point double zero",
            "mathematical_form": "V(0)=0; partial_A V(0)=0; nablaY=0 at local fixed point => T_can(0)=0 and partial_A T_can(0)=0",
            "purpose": "derive F_1=0 for the canonical sector rather than assuming a plateau",
            "derivation_status": "exact_under_candidate_fixed_point",
            "corpus_matched": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "SGK4023_4_match_condition",
            "component": "Gamma/Khat symbol match",
            "mathematical_form": "D_GK^{mu nu}:=Gamma_eff g^{mu nu}-Khat^{mu nu}-T_can^{mu nu}=0 through local 2PN order",
            "purpose": "separate real derivation from a merely compatible auxiliary model",
            "derivation_status": "required_not_yet_verified",
            "corpus_matched": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def match_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MATCH4023_0_tensor_type",
            "gate": "Gamma_eff scalar and Khat symmetric covariant rank-2 tensor in observed branch",
            "pass_under_candidate": True,
            "current_corpus_status": "not_fully_checked_against_symbols",
            "if_failed": "q_loc cannot be a Hilbert-stress Ward residual",
            "next_action": "symbol-match Gamma_eff and Khat definitions to observed metric tensor types",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MATCH4023_1_Helmholtz",
            "gate": "Helmholtz/inverse-variational symmetry for sqrt|g| T_GK",
            "pass_under_candidate": True,
            "current_corpus_status": "unverified_for_actual_Gamma_Khat",
            "if_failed": "nonvariational mismatch D_GK must be bounded",
            "next_action": "compute or symbolically certify Helmholtz defect H_GK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MATCH4023_2_Euler_closure",
            "gate": "local carrier fields obey E_A=0 in compact local vacuum",
            "pass_under_candidate": True,
            "current_corpus_status": "source/boundary forcing not yet parent-zeroed",
            "if_failed": "source-exchange term sum_A E_A nablaY^A survives",
            "next_action": "use no-hair/energy identity or retain forcing bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MATCH4023_3_double_zero",
            "gate": "T_GK and first variation vanish at local fixed point",
            "pass_under_candidate": True,
            "current_corpus_status": "true for S_can; unverified for actual Gamma/Khat",
            "if_failed": "F_1 survives and PPN local branch fails or must be scored",
            "next_action": "match fixed-point expansion of Gamma_eff and Khat to T_can",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MATCH4023_4_projector_boundary",
            "gate": "P_loc is parent-owned and boundary/symplectic flux is zero or fixed topological subtraction",
            "pass_under_candidate": False,
            "current_corpus_status": "open per 513 and 1535",
            "if_failed": "bulk Ward zero does not prove local observable zero",
            "next_action": "derive projector ownership and boundary no-flux or carry compact-shell leakage bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MATCH4023_5_2PN_match",
            "gate": "D_GK^{mu nu}=0 through local 2PN order in the observed readout",
            "pass_under_candidate": False,
            "current_corpus_status": "not_matched",
            "if_failed": "nabla_mu D_GK^{mu nu} enters delta_beta_q_loc/R10/source-exchange rows",
            "next_action": "4024 symbol-match or run q_loc profile bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "FORK4023_0_zero_theorem",
            "branch": "zero_route",
            "condition": "MATCH4023_0..5 all pass and carrier fields are on shell",
            "mathematical_result": "q_loc^nu=P_loc nabla_mu T_GK^{mu nu}=0 through local 2PN",
            "status": "exact_conditional_not_current_claim",
            "next_action": "verify D_GK=0 and projector/boundary gates against actual corpus",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fork_id": "FORK4023_1_mismatch_bound",
            "branch": "bound_route",
            "condition": "D_GK!=0, Helmholtz defect nonzero, Euler closure fails, or boundary/projector gate fails",
            "mathematical_result": "|q_loc| <= ||P_loc||[sum_A |E_A||nablaY^A| + |nabla_mu D_GK^{mu nu}|] + boundary_flux",
            "status": "finite_bound_interface",
            "next_action": "fill amplitude/profile rows and map to delta_beta_q_loc/R10 alpha(lambda)",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fork_id": "FORK4023_2_nohair_subroute",
            "branch": "nohair_or_leakage",
            "condition": "positive local operator, source silence, boundary silence and zero-mode ownership",
            "mathematical_result": "Y=0 exact; if source/boundary forcing survives, energy norm E(Y)<=N_lock and leakage starts from sourced bound",
            "status": "conditional_nohair_else_leakage",
            "next_action": "source D_m, M_scr, N_lock, C_emb, boundary flux and weak-field map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BND4023_0_DGK_norm",
            "quantity": "||nabla_mu D_GK^{mu nu}||",
            "formula": "D_GK^{mu nu}=Gamma_eff g^{mu nu}-Khat^{mu nu}-T_can^{mu nu}",
            "current_value": "MISSING_SYMBOL_MATCH_OR_NUMERIC_PROFILE",
            "observable_map": "delta_beta_q_loc; R10 alpha(lambda); source-exchange",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BND4023_1_Euler_forcing",
            "quantity": "sum_A |E_A||nablaY^A|",
            "formula": "Ward source term if carrier fields are not on shell",
            "current_value": "MISSING_LOCAL_EULER_SOURCE_SILENCE",
            "observable_map": "local fifth force; source-normalization residual",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BND4023_2_boundary_flux",
            "quantity": "boundary_flux_GK",
            "formula": "integral_boundary Delta(theta_GK,Q_GK,tau) or compact-shell leakage budget",
            "current_value": "AVAILABLE_PROXY_7.432631961576971e-06_NOT_YET_MAPPED_TO_PPN",
            "observable_map": "alpha3; measured-GM drift; beta/gamma tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BND4023_3_quadratic_leakage",
            "quantity": "quadratic fixed-point leakage",
            "formula": "|F_vac|<=1/2 V2_max U_Y^2 + 1/6 V3_max U_Y^3; |F_vac'|<=V2_max U_Y + 1/2 V3_max U_Y^2",
            "current_value": "MISSING_V2_V3_UY_AND_DOMAIN_CONSTANTS",
            "observable_map": "K_chain; q_loc amplitude; R10/local PPN",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BND4023_4_delta_beta_interface",
            "quantity": "delta_beta_q_loc",
            "formula": "Pi_beta[P_loc(nabla_mu D_GK^{mu nu}+Euler+boundary)]",
            "current_value": "MISSING_PPN_PROJECTOR_NORMALIZATION",
            "observable_map": "PPN beta residual",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4023_0_full_match",
            "assumption": "T_GK equals T_can through 2PN, carrier fields are on shell, projector/boundary gates pass",
            "expected": "q_loc theorem-zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4023_1_current_state",
            "assumption": "canonical action exists but actual Gamma/Khat symbol match and boundary/projector gates are not verified",
            "expected": "progress but no local-GR claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4023_2_mismatch_survives",
            "assumption": "D_GK or Helmholtz defect is nonzero",
            "expected": "q_loc bound branch required",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4023_3_source_boundary_survives",
            "assumption": "Euler source or boundary flux survives despite canonical action",
            "expected": "no-hair/leakage bound inputs required",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case_id == "CASE4023_0_full_match":
            verdict = "QLOC_ZERO_IF_FULL_MATCH"
            next_action = "promote only after symbol match/projector/boundary evidence exists"
        elif case_id == "CASE4023_1_current_state":
            verdict = "CANONICAL_ACTION_BUILT_MATCH_PENDING"
            next_action = "4024 must symbol-match Gamma/Khat or run profile bound"
        elif case_id == "CASE4023_2_mismatch_survives":
            verdict = "D_GK_BOUND_REQUIRED"
            next_action = "fill D_GK norm and PPN/R10 maps"
        else:
            verdict = "NOHAIR_OR_LEAKAGE_INPUTS_REQUIRED"
            next_action = "source D_m/M_scr/N_lock/boundary constants"
        rows.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4023",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4023_0_constructed_Scan",
            "decision": "constructed canonical Hilbert-stress action S_can for a possible GK carrier sector",
            "rationale": "this proves the zero route is mathematically real if Gamma/Khat match the canonical stress",
            "effect": "q_loc is no longer a mystery term; it is either Noether-zero or mismatch-bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4023_1_keep_mismatch",
            "decision": "introduced D_GK mismatch tensor instead of claiming symbol equality",
            "rationale": "matching actual Gamma_eff/Khat to S_can is still unverified",
            "effect": "no smuggled closure; residual branch is explicit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4023_2_current_verdict",
            "decision": "current result is action route built, corpus match pending",
            "rationale": "projector/boundary/source/no-hair gates remain open",
            "effect": "local-GR claim remains false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4023_3_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "the next useful step is symbol matching or an executable q_loc profile bound",
            "effect": "4024 can close D_GK=0 or make q_loc testable",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4023_0_q_loc_zero",
            "claim": "q_loc is theorem-zero in current MTS",
            "allowed": False,
            "reason": "S_can exists, but actual Gamma/Khat symbol match, projector ownership and boundary silence are not verified",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4023_1_local_GR",
            "claim": "MTS locally reduces to GR/PPN",
            "allowed": False,
            "reason": "q_loc/R11/source-normalization gates still require match or bound evidence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4023_2_bound_pass",
            "claim": "q_loc residual is below PPN/R10 bounds",
            "allowed": False,
            "reason": "bound interface rows are not numeric or PPN-normalized",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4023_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "match actual Gamma_eff/Khat symbols to the canonical Hilbert stress T_can through local 2PN; if D_GK cannot be zeroed, fill the first q_loc amplitude/profile bound rows and PPN/R10 maps",
            "success_condition": "D_GK is either theorem-zero with projector/boundary ownership or converted into numeric/source-ready q_loc bound inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "canonical S_GK action route constructed; D_GK mismatch retained as bound target",
            "current_best_route": "symbol-match Gamma/Khat to T_can or run q_loc profile bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current = next(row for row in results if row["case_id"] == "CASE4023_1_current_state")
    DOC_PATH.write_text(
        f"""# 4023 - Gamma-Khat Variational Stress Action Or q_loc Bound

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

This checkpoint makes the main identity exact:

`T_GK^{{mu nu}} := Gamma_eff g_obs^{{mu nu}} - Khat^{{mu nu}}`

so

`nabla_mu T_GK^{{mu nu}} = nabla^nu Gamma_eff - nabla_mu Khat^{{mu nu}}`

and therefore

`q_loc^nu = P_loc nabla_mu T_GK^{{mu nu}}`.

## Constructive Attempt

I built a canonical candidate action:

`S_can[Y,g] = int sqrt|g|[-1/2 H_AB(Y) g^{{mu nu}} nabla_mu Y^A nabla_nu Y^B - V(Y)] + dB_GK`.

Its Hilbert stress is:

`T_can^{{mu nu}} = H_AB nabla^mu Y^A nabla^nu Y^B - g^{{mu nu}}[1/2 H_AB nabla_rho Y^A nabla^rho Y^B + V(Y)] + improvements`.

At the local fixed point `Y=0`, with `V(0)=0`, `partial_A V(0)=0`, and `nablaY=0`, this gives the double-zero:

`T_can(0)=0` and `partial_A T_can(0)=0`.

So the route is mathematically real: if actual `Gamma_eff/Khat` matches this Hilbert stress through local 2PN, Ward/Noether gives `q_loc=0` on shell without a plateau axiom.

## Guardrail

The match is not assumed. Define:

`D_GK^{{mu nu}} := Gamma_eff g^{{mu nu}} - Khat^{{mu nu}} - T_can^{{mu nu}}`.

Then:

`q_loc = P_loc[sum_A E_A nablaY^A + nabla_mu D_GK^{{mu nu}}] + boundary/projector terms`.

That is the clean fork:

- if `D_GK=0`, Euler closure holds, and projector/boundary gates pass, `q_loc=0`;
- otherwise `D_GK`, Euler forcing, and boundary flux become the q_loc bound inputs.

## Current Verdict

- Current evaluator result: `{current["verdict"]}`.
- Claim result: `{current["claim_result"]}`.
- Source needles found: `{source_hits}/{source_total}`.

No local-GR or q_loc-zero claim is made from 4023.

## Next Target

- `{NEXT_DOC}`
- `{NEXT_SCRIPT}`
""",
        encoding="utf-8",
    )


def append_spine(timestamp: str) -> None:
    marker = "## 4023 - Gamma/Khat Variational Stress Route"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Exact identity: `T_GK^{{mu nu}}:=Gamma_eff g^{{mu nu}}-Khat^{{mu nu}}`, so `q_loc^nu=P_loc nabla_mu T_GK^{{mu nu}}`.
- Constructed candidate: `S_can[Y,g]=int sqrt|g|[-1/2 H_AB nablaY^A nablaY^B - V(Y)] + dB_GK`.
- Hilbert stress route: if actual `Gamma_eff/Khat` matches `T_can` through local 2PN and Euler/projector/boundary gates pass, Ward identity gives `q_loc=0`.
- Guardrail: mismatch `D_GK=Gamma_eff g-Khat-T_can` is retained; if nonzero, it becomes the q_loc residual bound target.
- No claim: symbol match and boundary/projector ownership are pending.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4023 - Gamma/Khat Variational Stress Route" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    identity: list[dict[str, Any]],
    action: list[dict[str, Any]],
    match: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4023_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4023_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, identity_id in enumerate(["ID4023_0_define_TGK", "ID4023_1_divergence", "ID4023_2_Ward_route", "ID4023_3_mismatch"], start=2):
        add(f"VAL4023_{idx:02d}_identity", any(row["identity_id"] == identity_id for row in identity), f"{identity_id} present")
    for idx, action_id in enumerate(["SGK4023_0_fields", "SGK4023_1_action", "SGK4023_2_stress", "SGK4023_3_double_zero", "SGK4023_4_match_condition"], start=6):
        add(f"VAL4023_{idx:02d}_action", any(row["action_id"] == action_id for row in action), f"{action_id} present")
    for idx, gate_id in enumerate(["MATCH4023_0_tensor_type", "MATCH4023_1_Helmholtz", "MATCH4023_2_Euler_closure", "MATCH4023_3_double_zero", "MATCH4023_4_projector_boundary", "MATCH4023_5_2PN_match"], start=11):
        add(f"VAL4023_{idx:02d}_match", any(row["gate_id"] == gate_id for row in match), f"{gate_id} present")
    for idx, fork_id in enumerate(["FORK4023_0_zero_theorem", "FORK4023_1_mismatch_bound", "FORK4023_2_nohair_subroute"], start=17):
        add(f"VAL4023_{idx:02d}_fork", any(row["fork_id"] == fork_id for row in theorem), f"{fork_id} present")
    for idx, bound_id in enumerate(["BND4023_0_DGK_norm", "BND4023_1_Euler_forcing", "BND4023_2_boundary_flux", "BND4023_3_quadratic_leakage", "BND4023_4_delta_beta_interface"], start=20):
        add(f"VAL4023_{idx:02d}_bound", any(row["bound_id"] == bound_id for row in bound), f"{bound_id} present")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4023_25_current_case", result_lookup["CASE4023_1_current_state"]["verdict"] == "CANONICAL_ACTION_BUILT_MATCH_PENDING", "current case says match pending")
    add("VAL4023_26_mismatch_case", result_lookup["CASE4023_2_mismatch_survives"]["verdict"] == "D_GK_BOUND_REQUIRED", "mismatch case routes to bound")
    add("VAL4023_27_source_boundary_case", result_lookup["CASE4023_3_source_boundary_survives"]["verdict"] == "NOHAIR_OR_LEAKAGE_INPUTS_REQUIRED", "source/boundary case routes to nohair/leakage")
    add("VAL4023_28_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates false")
    add("VAL4023_29_decision_mismatch", any(row["decision_id"] == "DEC4023_1_keep_mismatch" for row in decisions), "mismatch decision recorded")
    add("VAL4023_30_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    output_tables = [
        sources,
        identity,
        action,
        match,
        theorem,
        bound,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4023_31_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4023_32_action_not_corpus_matched", all(str(row.get("corpus_matched", "")).lower() == "false" for row in action), "candidate action not marked corpus-matched")
    add("VAL4023_33_bound_not_ready", all(str(row.get("score_ready", "")).lower() == "false" for row in bound), "bound rows not score-ready")
    add("VAL4023_34_doc_exists", DOC_PATH.exists() and "D_GK" in read_text(DOC_PATH), "document written with mismatch guardrail")
    add("VAL4023_35_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4023_36_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4023_37_compile", compile_ok, "script compiles")
    add("VAL4023_38_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4023_39_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4023_40_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4023_41_qloc_claim_blocked", any(row["claim_id"] == "CLAIM4023_0_q_loc_zero" and str(row["allowed"]).lower() == "false" for row in claims), "q_loc overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    identity = identity_rows(timestamp)
    action = action_rows(timestamp)
    match = match_rows(timestamp)
    theorem = theorem_rows(timestamp)
    bound = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["identity"], identity)
    write_csv(OUTPUTS["action"], action)
    write_csv(OUTPUTS["match"], match)
    write_csv(OUTPUTS["theorem"], theorem)
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

    validation = build_validation_rows(timestamp, sources, identity, action, match, theorem, bound, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4023 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
