from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4043-Y5-R2FR-projector-domain-stress-silence-or-alpha-xi-bound-vector.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4043_SOURCE_REGISTER.csv",
    "stress_factorization": SOURCE_DIR / "P8_Y5_R2FR_4043_PROJECTOR_STRESS_FACTORIZATION.csv",
    "selected_zero_theorem": SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv",
    "alpha_xi_bound_vector": SOURCE_DIR / "P8_Y5_R2FR_4043_ALPHA_XI_BOUND_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4043_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4043_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4043_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4043_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4043_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4043_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4043_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for item in rows:
        for key in item:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        (
            "SRC4043_0",
            ROOT / "4042-Y5-R2FR-nonEH-operator-decoupling-or-PPN-bound-vector.md",
            "Still live as preferred-frame/projector PPN stress",
            "immediate predecessor isolates projector/domain stress as live nonEH leak",
        ),
        (
            "SRC4043_1",
            SOURCE_DIR / "P8_Y5_R2FR_4042_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
            "Delta_PPN_projector_stress",
            "4042 remaining residual vector",
        ),
        (
            "SRC4043_2",
            SOURCE_DIR / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "epsilon_D^i = P_loc^i_mu V_D^mu",
            "alpha_i/xi domain selector decomposition",
        ),
        (
            "SRC4043_3",
            SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
            "lambda_local=0 and chi_local=0 remove bulk selector/memory stress",
            "parent variation chain for selector stress",
        ),
        (
            "SRC4043_4",
            SOURCE_DIR / "P8_Y5_PARENT_GENERATOR_1514_PROJECTOR_STRESS_GATE.csv",
            "metric-independent topological/relative-chain projector",
            "projector stress exact conditional theorem",
        ),
        (
            "SRC4043_5",
            SOURCE_DIR / "P8_Y5_PARENT_GENERATOR_1514_DOMAIN_SELECTOR_AUDIT.csv",
            "THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "older caution: chi_D elimination not globally parent-derived",
        ),
        (
            "SRC4043_6",
            SOURCE_DIR / "P8_Y5_R2FR_3929_PROJECTOR_PARENT_SIGNATURE.csv",
            "PROJECTOR_DOMAIN_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH",
            "newer private local branch projector/domain signature",
        ),
        (
            "SRC4043_7",
            SOURCE_DIR / "P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv",
            "epsilon_domain_projector_abs",
            "projector/domain zero result in private branch",
        ),
        (
            "SRC4043_8",
            SOURCE_DIR / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv",
            "T_PiM^{mu nu}",
            "projector stress split and bound branch",
        ),
        (
            "SRC4043_9",
            SOURCE_DIR / "P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv",
            "delta_g of projector, domain, boundary, and constraint sectors is zero/topological",
            "theorem stack clause for stress silence",
        ),
        (
            "SRC4043_10",
            SOURCE_DIR / "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv",
            "W_domain_alpha1_epsilon_domain_vector",
            "fallback alpha/xi fill vector",
        ),
        (
            "SRC4043_11",
            SOURCE_DIR / "P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv",
            "DSR_R7_alpha3_NUMERIC_OR_ZERO",
            "domain alpha sibling bounds",
        ),
        (
            "SRC4043_12",
            SOURCE_DIR / "P8_LOCAL_ZERO_COUNTEREXAMPLE_LEDGER.csv",
            "Qcoh=0 implies projector/domain stress is zero",
            "guard against false local-zero overclaim",
        ),
        (
            "SRC4043_13",
            SOURCE_DIR / "P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
            "multiplier, projector, and boundary stress must be shown zero/topological or retained",
            "metric variation guard",
        ),
        (
            "SRC4043_14",
            SOURCE_DIR / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv",
            "domain alpha3 remains retained and not scoreable",
            "older alpha3 no-leak failure and fallback pressure",
        ),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def stress_factorization_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "piece_id": "PSF4043_0_projector_metric_variation",
            "stress_piece": "projector metric variation",
            "formula": "T_P^{mu nu}=-(2/sqrt(-g))*delta_g(P_D J_H)/delta g_mu_nu",
            "zero_condition": "no action-level dynamic P_D, or P_D=q_src^*Pbar_top with delta_g P_D=0",
            "if_unsigned": "feeds delta_gamma_R11, xi, alpha_i, and source-normalization rows",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "PSF4043_1_domain_motion",
            "stress_piece": "domain/support motion",
            "formula": "D_domain P_D terms <= ||D_D P_D||*(||delta W_source||+||delta A_ext||+||delta S_link||)",
            "zero_condition": "D_loc=q_src^{-1}(Dbar) and source-silent local variations have D_X q_src=0, hence D_D P_D=0",
            "if_unsigned": "feeds alpha1/alpha2 via local domain vector and radial/source support hair",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "PSF4043_2_constraint_multiplier",
            "stress_piece": "chi_D / lambda_D constraint stress",
            "formula": "T_chi^{mu nu} includes lambda_D delta_g Sigma_D + chi_D^2 T_mem,D",
            "zero_condition": "chi_local=0, lambda_local=0, and delta_g chi_D=0 in the fixed collar",
            "if_unsigned": "feeds alpha3 flux, xi anisotropy, and R11 source-normalization",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "PSF4043_3_wall_boundary",
            "stress_piece": "domain wall / boundary flux",
            "formula": "Phi_D and tau_wall_TF determine local flux and STF wall stress",
            "zero_condition": "Phi_D=0 and tau_wall_TF=0 on the projector/domain collar",
            "if_unsigned": "feeds alpha3 and xi; cannot be cancelled against other channels",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "PSF4043_4_readout_denominator",
            "stress_piece": "extra source denominator",
            "formula": "M_obs uses M_H_ref from the same Hilbert source, with no second projector mass",
            "zero_condition": "same-Hilbert-denominator and no post-readout fitted Pi_M mask",
            "if_unsigned": "feeds Delta_cnorm_envelope and measured-GM laundering guard",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def selected_zero_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "PZS4043_0_selected_signature",
            "statement": "In the private selected local branch, the projector/domain sector is a readout/topological label, not a dynamical stress source.",
            "required_inputs": "delta S_parent^loc/delta P_D=0; delta_g P_D=0; D_D P_D=0; delta_g chi_D=0; Phi_D=0; tau_wall_TF=0; same M_H_ref",
            "derived_result": "T_projector_domain^{mu nu}=0 in the compact collar and Pi_alpha_xi[T_projector_domain]=0",
            "status": "THEOREM_ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PZS4043_1_vector",
            "statement": "No local domain vector is generated.",
            "required_inputs": "P_loc^i_mu nabla^mu chi_D=0; P_loc^i_mu n_D^mu=0; fixed q-basic domain",
            "derived_result": "epsilon_domain_vector=0, so alpha1_domain=alpha2_domain=0 in this branch",
            "status": "THEOREM_ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PZS4043_2_flux",
            "statement": "No local domain preferred-momentum flux is generated.",
            "required_inputs": "Phi_D=0; no local domain wall flux; no memory class active in the compact collar",
            "derived_result": "epsilon_domain_flux=0, so alpha3_domain=0 in this branch",
            "status": "THEOREM_ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PZS4043_3_anisotropy",
            "statement": "No local selector/projector anisotropic stress is generated.",
            "required_inputs": "tau_wall_TF=0; STF(P_loc T_D P_loc)=0; no dynamical metric-dependent projector",
            "derived_result": "epsilon_domain_anisotropy=0, so xi_domain=0 in this branch",
            "status": "THEOREM_ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PZS4043_4_guard",
            "statement": "Qcoh=0 or X_D=0 alone is not used as the proof.",
            "required_inputs": "metric variation/projector/domain support clauses above must be signed",
            "derived_result": "prevents smuggling projector stress silence from a scalar local-zero statement",
            "status": "COUNTEREXAMPLE_GUARD_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def alpha_xi_bound_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "AXB4043_0_alpha1",
            "target_row": "R5_alpha1",
            "observable": "alpha1",
            "projection": "alpha1_domain = W_domain_alpha1 * epsilon_domain_vector",
            "selected_branch_value": "0",
            "fallback_bound": "abs(W_domain_alpha1 * epsilon_domain_vector) <= 1e-04",
            "status": "ZERO_IN_PRIVATE_BRANCH_ELSE_NUMERIC_OR_THEOREM_ROW_REQUIRED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "AXB4043_1_alpha2",
            "target_row": "R6_alpha2",
            "observable": "alpha2",
            "projection": "alpha2_domain = W_domain_alpha2 * epsilon_domain_vector",
            "selected_branch_value": "0",
            "fallback_bound": "abs(W_domain_alpha2 * epsilon_domain_vector) <= 2e-09",
            "status": "ZERO_IN_PRIVATE_BRANCH_ELSE_NUMERIC_OR_THEOREM_ROW_REQUIRED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "AXB4043_2_alpha3",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "projection": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "selected_branch_value": "0",
            "fallback_bound": "abs(W_domain_alpha3 * epsilon_domain_flux) <= 4e-20",
            "status": "ZERO_IN_PRIVATE_BRANCH_ELSE_NUMERIC_OR_THEOREM_ROW_REQUIRED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "AXB4043_3_xi",
            "target_row": "R8_xi",
            "observable": "xi",
            "projection": "xi_domain = W_domain_xi * epsilon_domain_anisotropy",
            "selected_branch_value": "0",
            "fallback_bound": "abs(W_domain_xi * epsilon_domain_anisotropy) <= 4e-09",
            "status": "ZERO_IN_PRIVATE_BRANCH_ELSE_NUMERIC_OR_THEOREM_ROW_REQUIRED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "AXB4043_4_zeta",
            "target_row": "PPN_zeta_i",
            "observable": "zeta_i",
            "projection": "zeta_domain = Pi_zeta[nabla_mu T_projector_domain^{mu nu}]",
            "selected_branch_value": "0",
            "fallback_bound": "abs(zeta_domain) <= declared PPN conservation bound after same-source projector is fixed",
            "status": "ZERO_IN_PRIVATE_BRANCH_ELSE_BOUND_ROW_REQUIRED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "AXB4043_5_master",
            "target_row": "Delta_PPN_projector_stress",
            "observable": "alpha_xi_projector_master",
            "projection": "Delta_alpha_xi_domain=sum(abs(AXB4043_0..4))",
            "selected_branch_value": "0",
            "fallback_bound": "no-cancellation absolute sum of alpha1, alpha2, alpha3, xi, and zeta projector pieces",
            "status": "PROJECTOR_STRESS_ZERO_IN_PRIVATE_BRANCH_ELSE_ACTIVE_BOUND_VECTOR",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4043_0_selected_projector_domain_branch",
            "verdict": "PROJECTOR_DOMAIN_STRESS_ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "result": "Using the 3929 private signature, the live projector/domain stress channel has zero alpha1/alpha2/alpha3/xi projection in the compact local collar.",
            "claim_allowed": True,
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4043_1_if_signature_not_adopted",
            "verdict": "ALPHA_XI_BOUND_VECTOR_REQUIRED",
            "result": "Without the selected-branch signature, Qcoh=0 is insufficient and the vector/flux/STF pieces must be scored with explicit products.",
            "claim_allowed": False,
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4043_0_adopt_private_signature",
            "decision": "adopt 3929 projector/domain signature as the private selected local branch for this checkpoint",
            "reason": "it supplies the exact clauses missing from older projector-stress attempts: no dynamic P_D, topological/fixed label, fixed q-basic domain, zero collar flux, zero TF wall stress, and same Hilbert denominator",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4043_1_no_Qcoh_shortcut",
            "decision": "do not infer stress silence from X_D=0 or Qcoh=0 alone",
            "reason": "the counterexample ledger shows on-shell scalar zero does not remove metric variation/projector stress",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4043_2_fallback",
            "decision": "retain alpha/xi product rows as fallback if parent action rejects the 3929 signature",
            "reason": "this keeps the route testable without fitted cancellations",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4043_3_next",
            "decision": "roll remaining local-GR residuals into a master selected-branch scorecard and attack c_Z/c_norm envelopes",
            "reason": "projector/domain stress is no longer the generic live blocker in the selected branch; the surviving hard channels are c_Z memory tail/wall and c_norm derivative hair",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4043_0_private_projector_zero",
            "claim": "projector/domain stress has zero alpha_i/xi projection in the selected private local branch",
            "allowed": True,
            "public_claim_allowed": False,
            "scope": "private selected-branch theorem using 3929 signature only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4043_1_global_projector_zero",
            "claim": "all possible MTS parent branches have zero projector/domain stress",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "not proven; older source trail still records non-selected branches and missing parent ownership",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4043_2_full_local_GR",
            "claim": "full MTS local-GR / PPN pass",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "blocked until c_Z and c_norm envelopes are closed or bounded and the parent packet is adopted as final",
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4043_0_cZ",
            "symbol": "Delta_cZ_envelope",
            "residual": "memory tail / selector wall / hidden current envelope",
            "current_route": "still active unless kernel support/gap/no-wall theorem closes it",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4043_1_cnorm",
            "symbol": "Delta_cnorm_envelope",
            "residual": "nonconstant source-normalization derivative hair",
            "current_route": "still active unless Gdot/radial/range/species derivative rows are zeroed or bounded",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4043_2_projector_fallback",
            "symbol": "Delta_alpha_xi_domain_fallback",
            "residual": "alpha_i/xi fallback vector if the 3929 selected branch is not adopted",
            "current_route": "zero in private selected branch; kept as nonclaim fallback vector",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4043_3_parent_adoption",
            "symbol": "Parent_packet_adoption",
            "residual": "selected local packet must be promoted from private branch to final parent-action theorem",
            "current_route": "requires final action placement and variation audit before public local-GR claim",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4043_0",
            "next_doc": "4044-Y5-R2FR-local-GR-master-residual-scorecard-and-cZ-cnorm-priority.md",
            "next_script": "scripts/Y5_R2FR_4044_local_GR_master_residual_scorecard_and_cZ_cnorm_priority.py",
            "why": "after projector/domain stress zero in the private branch, the honest next step is a master residual scorecard focused on c_Z memory tail/wall and c_norm derivative hair",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4043",
            "status": "PROJECTOR_DOMAIN_STRESS_ZERO_IN_PRIVATE_BRANCH_ALPHA_XI_FALLBACK_RETAINED",
            "local_GR_claim": False,
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    source_hits = sum(1 for item in sources if item["exists"] and item["needle_found"])
    return "\n".join(
        [
            "# 4043 - Projector/Domain Stress Silence Or Alpha-Xi Bound Vector",
            "",
            f"- Timestamp: `{ts}`",
            "- Status: `private_nonclaim_checkpoint`",
            "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
            f"- Source needles found: `{source_hits}/{len(sources)}`.",
            "",
            "## What Actually Moved",
            "",
            "4043 turns the remaining projector/domain stress leak into a proper selected-branch theorem instead of leaving it as a vague PPN worry.",
            "",
            "The stress is factorized as projector metric variation, domain/support motion, constraint multiplier stress, wall/boundary flux, and readout-denominator leakage.",
            "",
            "Using the 3929 private signature:",
            "",
            "`delta S_parent^loc/delta P_D=0`, `delta_g P_D=0`, `D_D P_D=0`, `delta_g chi_D=0`, `Phi_D=0`, `tau_wall_TF=0`, and the same `M_H_ref`.",
            "",
            "Therefore `T_projector_domain^{mu nu}=0` in the compact collar and `Pi_alpha_xi[T_projector_domain]=0` in the selected private local branch.",
            "",
            "## What Is Not Being Smuggled",
            "",
            "`X_D=0` or `Qcoh=0` alone is not used as the proof. The metric-variation/projector-support clauses are required, because the counterexample ledger allows on-shell scalar zero with nonzero projector stress.",
            "",
            "## Fallback Bound Vector",
            "",
            "If the 3929 selected branch is not adopted by the final parent action, the retained rows are:",
            "",
            "- `alpha1_domain = W_domain_alpha1 * epsilon_domain_vector`, bound `1e-04`;",
            "- `alpha2_domain = W_domain_alpha2 * epsilon_domain_vector`, bound `2e-09`;",
            "- `alpha3_domain = W_domain_alpha3 * epsilon_domain_flux`, bound `4e-20`;",
            "- `xi_domain = W_domain_xi * epsilon_domain_anisotropy`, bound `4e-09`;",
            "- `zeta_domain = Pi_zeta[nabla_mu T_projector_domain^{mu nu}]`, bound row required.",
            "",
            "## Current Verdict",
            "",
            "- Current evaluator result: `PROJECTOR_DOMAIN_STRESS_ZERO_IN_PRIVATE_SELECTED_BRANCH`.",
            "- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4043`.",
            "- Remaining live local residuals: `Delta_cZ_envelope`, `Delta_cnorm_envelope`, `Delta_alpha_xi_domain_fallback`, `Parent_packet_adoption`.",
            "",
            "## Next Target",
            "",
            "- `4044-Y5-R2FR-local-GR-master-residual-scorecard-and-cZ-cnorm-priority.md`",
            "- `scripts/Y5_R2FR_4044_local_GR_master_residual_scorecard_and_cZ_cnorm_priority.py`",
            "",
        ]
    )


def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
    return {"check_id": check_id, "passed": passed, "detail": detail}


def all_private(*tables: Iterable[Dict[str, object]]) -> bool:
    return all(item.get("valid_for_public_claim") is False for table in tables for item in table)


def validation_rows(
    sources: List[Dict[str, object]],
    factorization: List[Dict[str, object]],
    zero_theorem: List[Dict[str, object]],
    bounds: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH)]
    return [
        row("VAL4043_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4043_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4043_02_factorization_count", len(factorization) == 5, "five stress pieces factorized"),
        row("VAL4043_03_projector_piece", any(item["piece_id"] == "PSF4043_0_projector_metric_variation" for item in factorization), "projector metric variation piece present"),
        row("VAL4043_04_domain_piece", any(item["piece_id"] == "PSF4043_1_domain_motion" for item in factorization), "domain motion piece present"),
        row("VAL4043_05_constraint_piece", any(item["piece_id"] == "PSF4043_2_constraint_multiplier" for item in factorization), "constraint stress piece present"),
        row("VAL4043_06_zero_signature", any(item["theorem_id"] == "PZS4043_0_selected_signature" for item in zero_theorem), "selected signature zero theorem present"),
        row("VAL4043_07_no_Qcoh_shortcut", any(item["theorem_id"] == "PZS4043_4_guard" for item in zero_theorem), "Qcoh shortcut guard present"),
        row("VAL4043_08_vector_zero", any(item["theorem_id"] == "PZS4043_1_vector" for item in zero_theorem), "vector zero theorem present"),
        row("VAL4043_09_flux_zero", any(item["theorem_id"] == "PZS4043_2_flux" for item in zero_theorem), "flux zero theorem present"),
        row("VAL4043_10_anisotropy_zero", any(item["theorem_id"] == "PZS4043_3_anisotropy" for item in zero_theorem), "anisotropy zero theorem present"),
        row("VAL4043_11_alpha1_bound", any(item["bound_id"] == "AXB4043_0_alpha1" and item["selected_branch_value"] == "0" for item in bounds), "alpha1 row present and zero in selected branch"),
        row("VAL4043_12_alpha2_bound", any(item["bound_id"] == "AXB4043_1_alpha2" and item["selected_branch_value"] == "0" for item in bounds), "alpha2 row present and zero in selected branch"),
        row("VAL4043_13_alpha3_bound", any(item["bound_id"] == "AXB4043_2_alpha3" and item["selected_branch_value"] == "0" for item in bounds), "alpha3 row present and zero in selected branch"),
        row("VAL4043_14_xi_bound", any(item["bound_id"] == "AXB4043_3_xi" and item["selected_branch_value"] == "0" for item in bounds), "xi row present and zero in selected branch"),
        row("VAL4043_15_master_bound", any(item["bound_id"] == "AXB4043_5_master" for item in bounds), "master alpha/xi row present"),
        row("VAL4043_16_evaluator_zero", any(item["verdict"] == "PROJECTOR_DOMAIN_STRESS_ZERO_IN_PRIVATE_SELECTED_BRANCH" for item in evaluator), "zero evaluator present"),
        row("VAL4043_17_evaluator_fallback", any(item["verdict"] == "ALPHA_XI_BOUND_VECTOR_REQUIRED" for item in evaluator), "fallback evaluator present"),
        row("VAL4043_18_decision_adopt_private", any(item["decision_id"] == "DEC4043_0_adopt_private_signature" for item in decisions), "private signature decision present"),
        row("VAL4043_19_decision_no_shortcut", any(item["decision_id"] == "DEC4043_1_no_Qcoh_shortcut" for item in decisions), "no-shortcut decision present"),
        row("VAL4043_20_private_claim_scoped", any(item["claim_id"] == "CLAIM4043_0_private_projector_zero" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "private zero claim scoped internal"),
        row("VAL4043_21_global_zero_blocked", any(item["claim_id"] == "CLAIM4043_1_global_projector_zero" and item["allowed"] is False for item in claims), "global projector zero blocked"),
        row("VAL4043_22_local_GR_blocked", any(item["claim_id"] == "CLAIM4043_2_full_local_GR" and item["allowed"] is False for item in claims), "full local-GR claim blocked"),
        row("VAL4043_23_remaining_cZ", any(item["symbol"] == "Delta_cZ_envelope" for item in remaining), "cZ residual carried"),
        row("VAL4043_24_remaining_cnorm", any(item["symbol"] == "Delta_cnorm_envelope" for item in remaining), "c_norm residual carried"),
        row("VAL4043_25_remaining_adoption", any(item["symbol"] == "Parent_packet_adoption" for item in remaining), "parent adoption residual carried"),
        row("VAL4043_26_next_target", bool(next_target and "4044" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4043_27_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4043_28_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4043_29_script_compiles", compile_ok, "script compiles"),
        row("VAL4043_30_private_guard", all_private(factorization, zero_theorem, bounds, evaluator, decisions, remaining), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    factorization = stress_factorization_rows(ts)
    zero_theorem = selected_zero_rows(ts)
    bounds = alpha_xi_bound_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    remaining = remaining_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["stress_factorization"], factorization)
    write_csv(OUTPUTS["selected_zero_theorem"], zero_theorem)
    write_csv(OUTPUTS["alpha_xi_bound_vector"], bounds)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(
        sources,
        factorization,
        zero_theorem,
        bounds,
        evaluator,
        decisions,
        claims,
        remaining,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4043 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
