from __future__ import annotations

import csv
import hashlib
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main\post-checkpoint-work"
)
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4029-Y5-R2FR-phi-owner-sign-convention-or-tracefree-residual-bound-input.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4029_SOURCE_REGISTER.csv",
    "sign_convention": SOURCE_DIR / "P8_Y5_R2FR_4029_GAMMA_OWNER_SIGN_CONVENTION.csv",
    "phi_owner": SOURCE_DIR / "P8_Y5_R2FR_4029_PHI_OWNER_EULER_DERIVATION.csv",
    "energy_identity": SOURCE_DIR / "P8_Y5_R2FR_4029_PHI_LOCAL_VACUUM_ENERGY_IDENTITY.csv",
    "tracefree_residual": SOURCE_DIR / "P8_Y5_R2FR_4029_TRACEFREE_RESIDUAL_REDUCTION.csv",
    "bound_inputs": SOURCE_DIR / "P8_Y5_R2FR_4029_TRACEFREE_BOUND_INPUTS.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4029_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4029_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4029_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4029_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4029_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4029_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4029_VALIDATION.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def short_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "SRC4029_0_4028_doc",
            "path": "4028-Y5-R2FR-tracefree-improvement-parent-sign-or-DGK-first-bound-row.md",
            "needle": "S_phi=int sqrt|g|",
            "role": "4028 introduced the local phi owner template",
        },
        {
            "source_id": "SRC4029_1_4028_derivation",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4028_TRACEFREE_IMPROVEMENT_DERIVATION.csv",
            "needle": "DER4028_2_response_convention",
            "role": "provides the previous sigma_resp*c_I sign placeholder",
        },
        {
            "source_id": "SRC4029_2_4028_owner",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4028_PHI_OWNER_LOCAL_ACTION_TEMPLATE.csv",
            "needle": "OWN4028_0_local_phi",
            "role": "provides the dynamical phi owner candidate",
        },
        {
            "source_id": "SRC4029_3_4028_sign_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4028_TRACEFREE_SIGN_AND_PROJECTION_GATE.csv",
            "needle": "sigma_resp*c_I=1",
            "role": "identifies the sign clause that 4029 fixes internally",
        },
        {
            "source_id": "SRC4029_4_4028_bound",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4028_DGK_FIRST_BOUND_ROW.csv",
            "needle": "BND4028_0_tracefree_master",
            "role": "previous symbolic D_TF residual bound row",
        },
        {
            "source_id": "SRC4029_5_first_variation_contract",
            "path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            "needle": "-2/sqrt(-g)",
            "role": "fixes the stress convention for S_GK=-I_Gamma",
        },
        {
            "source_id": "SRC4029_6_gamma_owner_candidate",
            "path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "needle": "K_hat^{mu nu} := 2/sqrt(-g)",
            "role": "fixes the Gamma-owner Khat convention directly",
        },
        {
            "source_id": "SRC4029_7_metric_response_contract",
            "path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "fixed sign convention",
            "role": "requires exact metric response with declared sign",
        },
    ]


def build_source_register(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        full = ROOT / spec["path"]
        text = read_text(full)
        rows.append(
            {
                **spec,
                "absolute_path": str(full),
                "exists": full.exists(),
                "needle_found": spec["needle"] in text,
                "sha256_16": short_hash(full),
                "timestamp_utc": ts,
            }
        )
    return rows


def build_sign_convention(ts: str) -> list[dict[str, object]]:
    return [
        {
            "sign_id": "SIGN4029_0_owner_functional",
            "object": "Gamma owner functional",
            "definition": "I_Gamma[g,fields]=int sqrt|g| Gamma_eff",
            "convention": "Khat_metric^{mu nu}=+2/sqrt|g| delta I_Gamma/delta g_{mu nu} with volume term treated separately",
            "result": "this matches the existing Gamma-owner candidate row and removes the free sigma_resp sign",
            "status": "SIGN_CONVENTION_FIXED_INTERNALLY",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "sign_id": "SIGN4029_1_action_relation",
            "object": "relation to S_GK",
            "definition": "S_GK=-I_Gamma",
            "convention": "T_GK^{mu nu}=-2/sqrt|g| delta S_GK/delta g_{mu nu}=+2/sqrt|g| delta I_Gamma/delta g_{mu nu}",
            "result": "the first-variation stress convention and Gamma-owner Khat convention are compatible",
            "status": "NO_SIGN_CONFLICT",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "sign_id": "SIGN4029_2_lower_metric_variation",
            "object": "phi R response",
            "definition": "I_imp[c_I]=c_I int sqrt|g| phi R",
            "convention": "delta g^{ab}=-g^{a mu}g^{b nu}delta g_{mu nu}",
            "result": "K_imp^{mu nu}=2*c_I[nabla^mu nabla^nu phi-g^{mu nu}Box phi-phi G^{mu nu}]",
            "status": "LOWER_METRIC_RESPONSE_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "sign_id": "SIGN4029_3_tracefree_match",
            "object": "K_L match",
            "definition": "Pi_TF[K_imp]^{mu nu}=2*c_I[(nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi)-phi G_TF^{mu nu}]",
            "convention": "c_I=1 gives the old K_L derivative piece with the positive sign",
            "result": "the old sigma_resp*c_I=1 condition becomes the concrete Gamma-owner coefficient condition c_I=1",
            "status": "SIGN_CLAUSE_CLOSED_CONDITIONALLY",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_phi_owner(ts: str) -> list[dict[str, object]]:
    return [
        {
            "owner_id": "PHI4029_0_dynamical_owner",
            "field": "phi",
            "action": "I_phi=int sqrt|g|[-zeta_phi/2 grad(phi)^2 - zeta_phi*mu_phi^2/2*(phi-phi_*)^2 - (2*zeta_phi/3)phi F]",
            "F_definition": "F:=Gamma_eff+C, assuming F is independent of phi or already split into F_rest",
            "euler_result": "Box phi - mu_phi^2(phi-phi_*) = (2/3)F",
            "new_residual_if_guard_fails": "D_phiF=(2/3)phi*(delta F/delta phi)",
            "status": "LOCAL_OWNER_EULER_RELATION_DERIVED_WITH_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "owner_id": "PHI4029_1_constraint_owner",
            "field": "lambda_phi",
            "action": "I_con=int sqrt|g| lambda_phi[Box phi-(2/3)F]",
            "F_definition": "F:=Gamma_eff+C",
            "euler_result": "variation in lambda_phi imposes Box phi=(2/3)F exactly",
            "new_residual_if_guard_fails": "D_lambda_stress plus boundary integrations by parts",
            "status": "EXACT_CONSTRAINT_ROUTE_AVAILABLE_BUT_STRESS_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "owner_id": "PHI4029_2_preferred_route",
            "field": "phi",
            "action": "use PHI4029_0 first, keep PHI4029_1 only as fallback",
            "F_definition": "dynamical local field is less singular than hard constraint",
            "euler_result": "local field-theory owner exists at template level",
            "new_residual_if_guard_fails": "owner stress must be included in T_can or bounded",
            "status": "PREFERRED_OWNER_ROUTE_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_energy_identity(ts: str) -> list[dict[str, object]]:
    return [
        {
            "identity_id": "EID4029_0_local_vacuum",
            "assumptions": "F=0 on local vacuum patch; mu_phi^2>=0; no-flux or fixed-boundary collar; u:=phi-phi_*",
            "identity": "int(|grad u|^2 + mu_phi^2 u^2)dV = boundary term",
            "consequence": "if boundary term vanishes, u=0 for mu_phi>0 or u=constant for mu_phi=0",
            "effect_on_KL": "nabla_mu nabla_nu phi=0, so K_L=0 on the compact local fixed branch",
            "status": "LOCAL_VACUUM_PHI_SILENCE_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "identity_id": "EID4029_1_forced_bound",
            "assumptions": "F nonzero but small; elliptic/hyperbolic local Green estimate exists on collar length L_phi",
            "identity": "||Hess phi|| <= C_phiF||F|| + C_phiB||boundary data||",
            "consequence": "A_KL/L_KL can be bounded by F amplitude and boundary leakage",
            "effect_on_KL": "trace-free Khat residual becomes scoreable once F and boundary maps are sourced",
            "status": "BOUND_TEMPLATE_DERIVED_NOT_NUMERIC",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "identity_id": "EID4029_2_owner_stress_guard",
            "assumptions": "phi owner stress enters the same parent variational ledger",
            "identity": "D_owner=0 only if phi sits on the local fixed branch or T_phi is included in T_can/Khat consistently",
            "consequence": "no hidden extra fifth-force term is allowed",
            "effect_on_KL": "owner route helps only when its stress is not dropped",
            "status": "OWNER_STRESS_GUARD_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_tracefree_residual(ts: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "DTF4029_0_reduced_law",
            "component": "D_TF",
            "formula": "D_TF^{mu nu}=(1-c_I)K_L^{mu nu}+2*c_I*phi*G_TF^{mu nu}+D_phiF^{mu nu}+D_owner^{mu nu}+D_boundary^{mu nu}+D_adoption^{mu nu}",
            "improvement_from_4028": "sigma_resp removed; sign condition reduced to c_I=1 in the Gamma-owner convention",
            "zero_conditions": "c_I=1; G_TF channel silent/routed; D_phiF=D_owner=D_boundary=D_adoption=0",
            "status": "RESIDUAL_REDUCED_NOT_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "DTF4029_1_local_vacuum_limit",
            "component": "K_L",
            "formula": "if F=0 and no-flux boundary then K_L=0 by the phi energy identity",
            "improvement_from_4028": "phi owner silence is now derivable on the compact local fixed branch",
            "zero_conditions": "requires local vacuum source F=0 and boundary collar theorem",
            "status": "PHI_OWNER_SILENCE_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "DTF4029_2_surviving_obstruction",
            "component": "curvature/adoption",
            "formula": "2*phi*G_TF + D_adoption is now the leading obstruction after sign normalization",
            "improvement_from_4028": "target list shortened",
            "zero_conditions": "prove EH/matter channel routing or source a bound for A_phiG/L_phiG",
            "status": "NEXT_OBSTRUCTION_IDENTIFIED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_bound_inputs(ts: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BND4029_0_tracefree_reduced",
            "component": "A_TF/L_TF",
            "formula": "A_TF/L_TF <= |1-c_I|A_KL/L_KL + 2|c_I|A_phiG/L_phiG + A_phiF/L_phiF + A_owner/L_owner + A_boundary/L_boundary + A_adoption/L_adoption",
            "source_status": "symbolic_reduced",
            "first_numeric_need": "c_I adoption or |1-c_I| bound; then A_phiG/L_phiG",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "BND4029_1_phi_owner_forced",
            "component": "A_KL/L_KL",
            "formula": "A_KL/L_KL <= C_phiF*A_F/L_F + C_phiB*A_boundary/L_boundary",
            "source_status": "elliptic_bound_template",
            "first_numeric_need": "C_phiF, A_F, L_F and boundary collar units",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "BND4029_2_local_vacuum_zero",
            "component": "K_L",
            "formula": "K_L=0 under F=0, mu_phi^2>=0, and no-flux/fixed boundary",
            "source_status": "conditional_theorem_certificate",
            "first_numeric_need": "none if local vacuum support theorem is sourced",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "BND4029_3_projector_still_missing",
            "component": "observable score",
            "formula": "delta_beta_TF=C_beta_TF*A_TF/L_TF; alpha_TF(lambda)=C_R10_TF(lambda)*A_TF/L_TF",
            "source_status": "projector_missing",
            "first_numeric_need": "derive C_beta_TF before any PPN score",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4029_0_sign_only",
            "input_condition": "Gamma-owner convention accepted but no live action adoption",
            "expected_verdict": "SIGN_CONVENTION_FIXED_TRACEFREE_STILL_NONCLAIM",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4029_1_local_vacuum",
            "input_condition": "F=0, no-flux boundary, mu_phi^2>=0",
            "expected_verdict": "PHI_OWNER_LOCAL_VACUUM_KL_ZERO_CONDITIONALLY",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4029_2_current",
            "input_condition": "current source hierarchy after 4029",
            "expected_verdict": "TRACEFREE_RESIDUAL_REDUCED_CURVATURE_ADOPTION_OPEN",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4029_0_sign_only",
            "verdict": "SIGN_CONVENTION_FIXED_TRACEFREE_STILL_NONCLAIM",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4029",
            "next_action": "source/adopt c_I=1 or retain |1-c_I| bound",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4029_1_local_vacuum",
            "verdict": "PHI_OWNER_LOCAL_VACUUM_KL_ZERO_CONDITIONALLY",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4029",
            "next_action": "prove local vacuum support/collar theorem or keep boundary term",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4029_2_current",
            "verdict": "TRACEFREE_RESIDUAL_REDUCED_CURVATURE_ADOPTION_OPEN",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4029",
            "next_action": "4030 should attack phi*G_TF EH/matter-channel routing first",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4029_0_sign",
            "decision": "replace sigma_resp*c_I with concrete Gamma-owner convention and coefficient c_I=1",
            "status": "SIGN_FOG_REMOVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4029_1_phi_owner",
            "decision": "dynamical local phi owner can derive Box phi=(2/3)(Gamma_eff+C) with an explicit F-dependence guard",
            "status": "OWNER_ROUTE_ADVANCED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4029_2_residual",
            "decision": "D_TF is reduced; leading surviving obstruction is phi*G_TF plus adoption/boundary terms",
            "status": "NEXT_OBSTRUCTION_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4029_3_next",
            "decision": "move to 4030-Y5-R2FR-curvature-channel-routing-or-tracefree-score-input.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4029_0_tracefree_live",
            "claim": "trace-free Khat component is live-adopted",
            "allowed": False,
            "reason": "sign convention is fixed internally, but live parent action/adoption row is not yet installed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4029_1_phi_owner_closed",
            "claim": "phi owner contributes no residual everywhere",
            "allowed": False,
            "reason": "silence is derived only under local-vacuum/no-flux/fixed-branch assumptions",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4029_2_DTF_zero",
            "claim": "D_TF=0",
            "allowed": False,
            "reason": "phi*G_TF, boundary and adoption terms remain open",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4029_3_local_GR",
            "claim": "local-GR/PPN branch passes",
            "allowed": False,
            "reason": "no PPN projector or full Khat closure yet",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4029_0",
            "next_doc": "4030-Y5-R2FR-curvature-channel-routing-or-tracefree-score-input.md",
            "next_script": "scripts/Y5_R2FR_4030_curvature_channel_routing_or_tracefree_score_input.py",
            "why": "after sign and phi-owner reduction, phi*G_TF is the leading trace-free obstruction",
            "fallback": "if curvature channel cannot be routed, source A_phiG/L_phiG and C_beta_TF",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4029_0",
            "checkpoint": "4029",
            "headline": "Gamma-owner sign convention fixed and local phi owner Euler/energy route derived conditionally",
            "verdict": "TRACEFREE_RESIDUAL_REDUCED_CURVATURE_ADOPTION_OPEN",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4029 - Phi Owner Sign Convention Or Tracefree Residual Bound Input

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4029 removes one piece of fog. Using the Gamma-owner functional

`I_Gamma=int sqrt|g| Gamma_eff`

and the existing convention

`Khat_metric^{{mu nu}}=+2/sqrt|g| delta I_Gamma/delta g_{{mu nu}}`,

the improvement term

`I_imp[c_I]=c_I int sqrt|g| phi R`

has lower-metric response

`K_imp^{{mu nu}}=2*c_I[nabla^mu nabla^nu phi-g^{{mu nu}}Box phi-phi G^{{mu nu}}]`.

Therefore

`Pi_TF[K_imp]^{{mu nu}}=2*c_I[(nabla^mu nabla^nu phi-(1/4)g^{{mu nu}}Box phi)-phi G_TF^{{mu nu}}]`.

So the old sign placeholder is now concrete: the derivative trace-free piece matches `K_L` when `c_I=1`.

## Phi Owner

The local owner template

`I_phi=int sqrt|g|[-zeta_phi/2 grad(phi)^2-zeta_phi*mu_phi^2/2*(phi-phi_*)^2-(2*zeta_phi/3)phi F]`

with `F:=Gamma_eff+C` gives

`Box phi-mu_phi^2(phi-phi_*)=(2/3)F`,

provided `F` is independent of `phi` or has been split into `F_rest`. If not, the extra term is retained as `D_phiF`.

## Local Vacuum Identity

For `F=0`, `mu_phi^2>=0`, and no-flux/fixed boundary data,

`int(|grad u|^2+mu_phi^2 u^2)dV=boundary`, where `u=phi-phi_*`.

If the boundary term vanishes, `phi` is constant and `K_L=0` on the compact local fixed branch.

## Reduced Residual

The trace-free residual is now

`D_TF^{{mu nu}}=(1-c_I)K_L^{{mu nu}}+2*c_I*phi*G_TF^{{mu nu}}+D_phiF^{{mu nu}}+D_owner^{{mu nu}}+D_boundary^{{mu nu}}+D_adoption^{{mu nu}}`.

That is better than 4028: the sign ambiguity is gone, and the leading surviving obstruction is now `phi*G_TF` plus adoption/boundary bookkeeping.

## Current Verdict

- Current evaluator result: `TRACEFREE_RESIDUAL_REDUCED_CURVATURE_ADOPTION_OPEN`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4029`.
- Source needles found: `{found}/{len(sources)}`.

## Next Target

- `4030-Y5-R2FR-curvature-channel-routing-or-tracefree-score-input.md`
- `scripts/Y5_R2FR_4030_curvature_channel_routing_or_tracefree_score_input.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts})


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    sign: list[dict[str, object]],
    phi_owner: list[dict[str, object]],
    energy: list[dict[str, object]],
    residual: list[dict[str, object]],
    bounds: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sign_ids = {str(row["sign_id"]) for row in sign}
    owner_ids = {str(row["owner_id"]) for row in phi_owner}
    energy_ids = {str(row["identity_id"]) for row in energy}
    residual_ids = {str(row["residual_id"]) for row in residual}
    bound_ids = {str(row["bound_id"]) for row in bounds}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4029_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4029_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4029_02_sign_owner", "SIGN4029_0_owner_functional" in sign_ids, "Gamma-owner sign convention row present", ts)
    add_validation(rows, "VAL4029_03_sign_match", "SIGN4029_3_tracefree_match" in sign_ids, "c_I=1 match row present", ts)
    add_validation(rows, "VAL4029_04_phi_owner", "PHI4029_0_dynamical_owner" in owner_ids, "dynamical phi owner row present", ts)
    add_validation(rows, "VAL4029_05_phi_guard", any("D_phiF" in str(row) for row in phi_owner), "phi-dependence guard retained", ts)
    add_validation(rows, "VAL4029_06_energy_identity", "EID4029_0_local_vacuum" in energy_ids, "local vacuum energy identity row present", ts)
    add_validation(rows, "VAL4029_07_owner_stress_guard", "EID4029_2_owner_stress_guard" in energy_ids, "owner stress guard row present", ts)
    add_validation(rows, "VAL4029_08_reduced_residual", "DTF4029_0_reduced_law" in residual_ids, "reduced D_TF residual row present", ts)
    add_validation(rows, "VAL4029_09_surviving_obstruction", "DTF4029_2_surviving_obstruction" in residual_ids, "surviving obstruction row present", ts)
    add_validation(rows, "VAL4029_10_bound_reduced", "BND4029_0_tracefree_reduced" in bound_ids, "reduced trace-free bound row present", ts)
    add_validation(rows, "VAL4029_11_projector_missing", "BND4029_3_projector_still_missing" in bound_ids, "projector missing row present", ts)
    add_validation(rows, "VAL4029_12_no_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in bounds), "no bound row is score-ready", ts)
    add_validation(rows, "VAL4029_13_current_verdict", "TRACEFREE_RESIDUAL_REDUCED_CURVATURE_ADOPTION_OPEN" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4029_14_no_claims", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4029_15_next_decision", any("4030" in str(row["decision"]) for row in decisions), "4030 next decision present", ts)
    add_validation(rows, "VAL4029_16_next_target", bool(next_target and "4030" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4029_17_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4029_18_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4029_19_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4029_20_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in sign + phi_owner + energy + residual + bounds + decisions), "all theorem rows remain nonclaim", ts)
    return rows


def main() -> None:
    ts = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    sign = build_sign_convention(ts)
    phi_owner = build_phi_owner(ts)
    energy = build_energy_identity(ts)
    residual = build_tracefree_residual(ts)
    bounds = build_bound_inputs(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["sign_convention"], sign)
    write_csv(OUTPUTS["phi_owner"], phi_owner)
    write_csv(OUTPUTS["energy_identity"], energy)
    write_csv(OUTPUTS["tracefree_residual"], residual)
    write_csv(OUTPUTS["bound_inputs"], bounds)
    write_csv(OUTPUTS["evaluator_cases"], cases)
    write_csv(OUTPUTS["evaluator_results"], results)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
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

    validation = build_validation_rows(
        ts,
        sources,
        sign,
        phi_owner,
        energy,
        residual,
        bounds,
        results,
        decisions,
        claims,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4029 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
