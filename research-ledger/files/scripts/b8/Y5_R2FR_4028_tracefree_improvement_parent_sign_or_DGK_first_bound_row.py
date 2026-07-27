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
DOC_PATH = ROOT / "4028-Y5-R2FR-tracefree-improvement-parent-sign-or-DGK-first-bound-row.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4028_SOURCE_REGISTER.csv",
    "derivation": SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_IMPROVEMENT_DERIVATION.csv",
    "sign_gate": SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_SIGN_AND_PROJECTION_GATE.csv",
    "owner_template": SOURCE_DIR / "P8_Y5_R2FR_4028_PHI_OWNER_LOCAL_ACTION_TEMPLATE.csv",
    "bound_row": SOURCE_DIR / "P8_Y5_R2FR_4028_DGK_FIRST_BOUND_ROW.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4028_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4028_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4028_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4028_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4028_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4028_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4028_VALIDATION.csv",
}


def timestamp() -> str:
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
            "source_id": "SRC4028_0_4027_doc",
            "path": "4027-Y5-R2FR-Khat-component-completion-or-DGK-bound-normalization.md",
            "needle": "trace-free improvement route",
            "role": "selects trace-free improvement as the best next derivation target",
        },
        {
            "source_id": "SRC4028_1_4027_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4027_CONDITIONAL_COMPLETION_PATHS.csv",
            "needle": "S_imp=int sqrt|g| c_I phi R",
            "role": "states the exact completion contract that 4028 must test",
        },
        {
            "source_id": "SRC4028_2_1525_identity",
            "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv",
            "needle": "trace-free Hessian identity",
            "role": "records the old algebraic K_L trace-free identity",
        },
        {
            "source_id": "SRC4028_3_1526_variation",
            "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1526_VARIATION_DERIVATION.csv",
            "needle": "delta[sqrt(-g)phi R]",
            "role": "provides the scalar-curvature first-variation identity",
        },
        {
            "source_id": "SRC4028_4_metric_contract",
            "path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "K_hat is exactly",
            "role": "requires Khat to be a real metric response, not an independent knob",
        },
        {
            "source_id": "SRC4028_5_metric_evidence",
            "path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
            "needle": "Gamma_eff must be",
            "role": "keeps the route tied to the existing Gamma/Khat/q_loc evidence stack",
        },
        {
            "source_id": "SRC4028_6_KL_row",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
            "needle": "K_L^{00}",
            "role": "anchors the old first Khat component row that this branch is trying to own",
        },
        {
            "source_id": "SRC4028_7_4026_components",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4026_KGAMMA_RESPONSE_COMPONENTS.csv",
            "needle": "D_A_grad",
            "role": "connects the trace-free improvement test to the D_GK component ledger",
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


def build_derivation(ts: str) -> list[dict[str, object]]:
    return [
        {
            "derivation_id": "DER4028_0_parent_action",
            "step": "improvement action",
            "formula": "S_imp[c_I]=s_imp*c_I*int_M sqrt|g| phi R + B_imp[phi,g,partial M]",
            "result": "specific parent action shape selected for the trace-free component",
            "status": "ACTION_SHAPE_EXPLICIT",
            "remaining": "live corpus adoption of c_I, s_imp, phi and B_imp",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_1_standard_variation",
            "step": "metric variation",
            "formula": "delta(int sqrt|g| phi R)=int sqrt|g|[phi G_mn+(g_mn Box-nabla_m nabla_n)phi]delta g^{mn}+boundary",
            "result": "the Hessian part is generated by the parent action, not inserted by hand",
            "status": "VARIATION_IDENTITY_USED",
            "remaining": "response sign convention must be fixed against live Khat",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_2_response_convention",
            "step": "Khat convention",
            "formula": "K_imp^{mn}=2*sigma_resp*c_I[nabla^m nabla^n phi-g^{mn}Box phi-phi G^{mn}]",
            "result": "all sign ambiguity compressed into sigma_resp*c_I",
            "status": "SIGN_NORMALIZED",
            "remaining": "source row must declare sigma_resp*c_I=1",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_3_tracefree_projection",
            "step": "four-dimensional trace-free projection",
            "formula": "Pi_TF[K_imp]^{mn}=2*sigma_resp*c_I[(nabla^m nabla^n phi-(1/4)g^{mn}Box phi)-phi G_TF^{mn}]",
            "result": "the desired K_L tensor appears exactly as the derivative trace-free part",
            "status": "TRACEFREE_FORMULA_DERIVED",
            "remaining": "curvature channel and adoption clauses decide whether it is live Khat",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_4_match_condition",
            "step": "exact match condition",
            "formula": "if sigma_resp*c_I=1 and Pi_TF(phi G) is silent/absorbed, then Pi_TF[K_imp]=K_L",
            "result": "trace-free Khat component can be closed by a parent action under explicit clauses",
            "status": "CONDITIONAL_ZERO_IF_SIGMA_CI_ONE",
            "remaining": "not yet live-adopted by current MTS source hierarchy",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_5_curvature_guard",
            "step": "curvature channel guard",
            "formula": "R_TF^{mn} term becomes D_phiG unless local vacuum/EH channel routing proves Pi_TF(phi G)=0",
            "result": "prevents smuggling matter curvature into the trace-free zero",
            "status": "GUARD_ADDED",
            "remaining": "prove local-vacuum support or route phi G into EH/matter response",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_6_phi_owner_template",
            "step": "local phi owner",
            "formula": "S_phi=int sqrt|g|[-zeta_phi/2 nabla phi.nabla phi-(mu_phi^2/2)(phi-phi_*)^2-(2*zeta_phi/3)phi(Gamma_eff+C)]",
            "result": "Euler branch can source Box phi=(2/3)(Gamma_eff+C) in a local field-theory way when mu_phi=0 and signs are chosen",
            "status": "OWNER_TEMPLATE_CONSTRUCTED_NOT_ADOPTED",
            "remaining": "coefficient/sign/source adoption and extra stress accounting",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_7_boundary_guard",
            "step": "boundary term",
            "formula": "B_imp must cancel normal derivatives in delta R and must be silent under the local no-flux/readout collar",
            "result": "boundary cannot be ignored; it is either signed silent or enters D_boundary",
            "status": "BOUNDARY_GUARD_EXPLICIT",
            "remaining": "source the exact B_imp convention or bound its contribution",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "derivation_id": "DER4028_8_residual_law",
            "step": "trace-free residual law",
            "formula": "D_TF^{mn}=(1-sigma_resp*c_I)K_L^{mn}+2*sigma_resp*c_I phi G_TF^{mn}+D_phi_owner^{mn}+D_boundary^{mn}+D_adoption^{mn}",
            "result": "if clauses fail, the residual is bounded rather than waved away",
            "status": "FIRST_DGK_BOUND_ROW_DERIVED",
            "remaining": "numeric amplitudes/projectors before PPN or R10 scoring",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_sign_gate(ts: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "SG4028_0_action_exists",
            "clause": "parent action contains S_imp=c_I int sqrt|g| phi R plus boundary",
            "current_result": "constructed_as_candidate_not_corpus_adopted",
            "needed_to_close": "write/adopt S_imp in the live parent action",
            "closes_tracefree_piece": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "SG4028_1_sign",
            "clause": "sigma_resp*c_I=1",
            "current_result": "normalized_but_unsigned",
            "needed_to_close": "declare metric variation convention and coefficient in source hierarchy",
            "closes_tracefree_piece": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "SG4028_2_phi_owner",
            "clause": "phi is a local parent field or constrained auxiliary field",
            "current_result": "local owner template built",
            "needed_to_close": "adopt owner action and account for its stress response",
            "closes_tracefree_piece": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "SG4028_3_curvature_guard",
            "clause": "Pi_TF(phi G)=0 or is routed to EH/matter channel",
            "current_result": "guard explicit",
            "needed_to_close": "prove local vacuum/readout support or include D_phiG bound",
            "closes_tracefree_piece": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "SG4028_4_boundary",
            "clause": "B_imp and local collar are no-flux/silent",
            "current_result": "not signed",
            "needed_to_close": "boundary convention or D_boundary bound",
            "closes_tracefree_piece": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "SG4028_5_live_Khat_adoption",
            "clause": "live Khat^TF is identified with Pi_TF[K_imp]",
            "current_result": "not signed",
            "needed_to_close": "corpus adoption row tying Khat^TF to this response",
            "closes_tracefree_piece": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_owner_template(ts: str) -> list[dict[str, object]]:
    return [
        {
            "owner_id": "OWN4028_0_local_phi",
            "field": "phi",
            "candidate_action": "S_phi=int sqrt|g|[-zeta_phi/2 nabla phi.nabla phi-(mu_phi^2/2)(phi-phi_*)^2-(2*zeta_phi/3)phi(Gamma_eff+C)]",
            "euler_branch": "Box phi - mu_phi^2(phi-phi_*) = (2/3)(Gamma_eff+C) after sign convention",
            "why_it_matters": "turns the old inverse-Box-looking definition into a local parent-field route",
            "risk": "S_phi contributes its own stress and may alter D_GK unless double-zero or included in T_can",
            "status": "CONSTRUCTED_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "owner_id": "OWN4028_1_multiplier_phi",
            "field": "lambda_phi",
            "candidate_action": "S_con=int sqrt|g| lambda_phi[Box phi-(2/3)(Gamma_eff+C)]",
            "euler_branch": "variation in lambda_phi imposes the exact old Box phi relation",
            "why_it_matters": "hard constraint alternative when a kinetic phi field is too expensive",
            "risk": "metric response of lambda_phi and integrations by parts must be silent or retained",
            "status": "ALTERNATIVE_TEMPLATE_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_bound_row(ts: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BND4028_0_tracefree_master",
            "component": "D_TF",
            "formula": "A_TF/L_TF <= |1-sigma_resp*c_I|A_KL/L_KL + 2|sigma_resp*c_I|A_phiG/L_phiG + A_owner/L_owner + A_boundary/L_boundary + A_adoption/L_adoption",
            "units_required": "stress-divergence units relative to EH/source normalization",
            "current_numeric_status": "symbolic_only",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "BND4028_1_zero_limit",
            "component": "D_TF_zero_conditions",
            "formula": "D_TF=0 if sigma_resp*c_I=1, Pi_TF(phi G)=0/channel-routed, D_owner=0, D_boundary=0, and live Khat adoption is signed",
            "units_required": "not numeric; theorem certificate",
            "current_numeric_status": "conditional_theorem_not_signed",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "BND4028_2_first_numeric_need",
            "component": "first numeric fallback",
            "formula": "if theorem signing fails, first number needed is max(A_KL/L_KL, A_phiG/L_phiG) plus C_beta_qloc",
            "units_required": "PPN beta projector or R10 alpha(lambda) projector",
            "current_numeric_status": "projector_missing",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4028_0_all_signed",
            "input_condition": "all sign, owner, curvature, boundary and adoption clauses are true",
            "expected_verdict": "TRACEFREE_COMPONENT_ZERO_DERIVED",
            "claim_result": "internal conditional only until whole Khat/q_loc branch closes",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4028_1_current",
            "input_condition": "current source hierarchy after 4028",
            "expected_verdict": "TRACEFREE_COMPONENT_CONDITIONALLY_DERIVED_NOT_LIVE_ADOPTED",
            "claim_result": "no public q_loc/local-GR claim",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4028_2_bound",
            "input_condition": "one or more signing clauses fail",
            "expected_verdict": "D_TF_BOUND_ROW_ACTIVE_SYMBOLIC_ONLY",
            "claim_result": "cannot score PPN/R10 without numeric amplitudes and projectors",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4028_0_all_signed",
            "verdict": "TRACEFREE_COMPONENT_ZERO_DERIVED_IF_SIGNED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4028",
            "next_action": "then continue to volume/chain/connection/domain/boundary Khat components",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4028_1_current",
            "verdict": "TRACEFREE_COMPONENT_CONDITIONALLY_DERIVED_NOT_LIVE_ADOPTED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4028",
            "next_action": "4029 should adopt/source phi owner and sign convention or keep D_TF bound row active",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4028_2_bound",
            "verdict": "D_TF_BOUND_ROW_ACTIVE_SYMBOLIC_ONLY",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4028",
            "next_action": "derive C_beta_qloc after D_TF has a source amplitude",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4028_0_forward_progress",
            "decision": "the trace-free K_L shape is now tied to a concrete phi R parent-action variation with explicit sign and curvature clauses",
            "status": "DERIVATION_ADVANCED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4028_1_not_promoted",
            "decision": "do not promote Khat^TF as live until sigma_resp*c_I, phi owner, boundary and adoption are source-signed",
            "status": "PRIVATE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4028_2_bound_fallback",
            "decision": "retain D_TF bound row with explicit amplitude law if any theorem clause remains unsigned",
            "status": "BOUND_BRANCH_READY_SYMBOLIC",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4028_3_next",
            "decision": "move to 4029-Y5-R2FR-phi-owner-sign-convention-or-tracefree-residual-bound-input.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4028_0_tracefree_closed",
            "claim": "trace-free Khat component is closed in the live corpus",
            "allowed": False,
            "reason": "derivation is conditional; live adoption and phi owner are not source-signed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4028_1_DTF_zero",
            "claim": "D_TF=0",
            "allowed": False,
            "reason": "zero limit is exact only under unsigned clauses",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4028_2_PPN_R10_score",
            "claim": "trace-free residual passes PPN/R10",
            "allowed": False,
            "reason": "no numeric amplitudes or projector maps",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4028_3_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "only one Khat component was advanced; full q_loc closure remains open",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4028_0",
            "next_doc": "4029-Y5-R2FR-phi-owner-sign-convention-or-tracefree-residual-bound-input.md",
            "next_script": "scripts/Y5_R2FR_4029_phi_owner_sign_convention_or_tracefree_residual_bound_input.py",
            "why": "phi owner and sigma_resp*c_I are the first unsigned clauses blocking the trace-free component from becoming live",
            "fallback": "if adoption fails, source the first A_TF/L_TF and C_beta_qloc inputs",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4028_0",
            "checkpoint": "4028",
            "headline": "trace-free improvement route derived to explicit parent-action conditions",
            "verdict": "TRACEFREE_COMPONENT_CONDITIONALLY_DERIVED_NOT_LIVE_ADOPTED",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4028 - Tracefree Improvement Parent Sign Or D_GK First Bound Row

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

The trace-free Khat route is no longer just "maybe an improvement term". It is now tied to the explicit parent-action variation

`S_imp[c_I]=s_imp*c_I int sqrt|g| phi R + B_imp`.

The metric response gives the derivative trace-free piece

`Pi_TF[K_imp]^{'{'}mu nu{'}'} = 2*sigma_resp*c_I[(nabla^mu nabla^nu phi-(1/4)g^{'{'}mu nu{'}'}Box phi)-phi G_TF^{'{'}mu nu{'}'}]`.

So the old candidate

`K_L^{'{'}mu nu{'}'}=2[nabla^mu nabla^nu phi-(1/4)g^{'{'}mu nu{'}'}Box phi]`

is exactly recovered if `sigma_resp*c_I=1` and the curvature channel `Pi_TF(phi G)` is silent or routed into the EH/matter response.

## New Local Owner Route

To avoid an inverse-Box definition of `phi`, 4028 adds a local owner template:

`S_phi=int sqrt|g|[-zeta_phi/2 nabla phi.nabla phi-(mu_phi^2/2)(phi-phi_*)^2-(2*zeta_phi/3)phi(Gamma_eff+C)]`.

In the `mu_phi=0` branch, with signs fixed, this can produce the old relation `Box phi=(2/3)(Gamma_eff+C)` as an Euler equation. This is useful, but not yet adopted, and its stress contribution must be accounted for.

## Residual Law

Until the clauses are signed, the retained trace-free residual is

`D_TF^{'{'}mu nu{'}'}=(1-sigma_resp*c_I)K_L^{'{'}mu nu{'}'}+2*sigma_resp*c_I phi G_TF^{'{'}mu nu{'}'}+D_phi_owner^{'{'}mu nu{'}'}+D_boundary^{'{'}mu nu{'}'}+D_adoption^{'{'}mu nu{'}'}`.

The first honest bound row is therefore

`A_TF/L_TF <= |1-sigma_resp*c_I|A_KL/L_KL + 2|sigma_resp*c_I|A_phiG/L_phiG + A_owner/L_owner + A_boundary/L_boundary + A_adoption/L_adoption`.

## Current Verdict

- Current evaluator result: `TRACEFREE_COMPONENT_CONDITIONALLY_DERIVED_NOT_LIVE_ADOPTED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4028`.
- Source needles found: `{found}/{len(sources)}`.
- This is real progress: one Khat subcomponent now has a parent-action route and an exact residual law.

## Next Target

- `4029-Y5-R2FR-phi-owner-sign-convention-or-tracefree-residual-bound-input.md`
- `scripts/Y5_R2FR_4029_phi_owner_sign_convention_or_tracefree_residual_bound_input.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": ts,
        }
    )


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    sign_gate: list[dict[str, object]],
    owner_template: list[dict[str, object]],
    bound_row: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    derivation_ids = {str(row["derivation_id"]) for row in derivation}
    sign_ids = {str(row["gate_id"]) for row in sign_gate}
    bound_ids = {str(row["bound_id"]) for row in bound_row}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4028_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4028_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4028_02_variation_row", "DER4028_1_standard_variation" in derivation_ids, "standard phi R variation row present", ts)
    add_validation(rows, "VAL4028_03_tracefree_formula", "DER4028_3_tracefree_projection" in derivation_ids, "trace-free projection row present", ts)
    add_validation(rows, "VAL4028_04_match_condition", "DER4028_4_match_condition" in derivation_ids, "sigma*c_I match condition present", ts)
    add_validation(rows, "VAL4028_05_phi_owner", "DER4028_6_phi_owner_template" in derivation_ids and len(owner_template) >= 1, "local phi owner template present", ts)
    add_validation(rows, "VAL4028_06_boundary_guard", "SG4028_4_boundary" in sign_ids, "boundary guard present", ts)
    add_validation(rows, "VAL4028_07_adoption_gate", "SG4028_5_live_Khat_adoption" in sign_ids, "live Khat adoption gate present", ts)
    add_validation(rows, "VAL4028_08_bound_master", "BND4028_0_tracefree_master" in bound_ids, "first D_TF bound row present", ts)
    add_validation(rows, "VAL4028_09_zero_limit", "BND4028_1_zero_limit" in bound_ids, "zero-limit theorem row present", ts)
    add_validation(rows, "VAL4028_10_no_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in bound_row), "bound rows are not score-ready", ts)
    add_validation(rows, "VAL4028_11_no_claims_allowed", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4028_12_current_verdict", "TRACEFREE_COMPONENT_CONDITIONALLY_DERIVED_NOT_LIVE_ADOPTED" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4028_13_decision_next", any("4029" in str(row["decision"]) for row in decisions), "4029 next decision present", ts)
    add_validation(rows, "VAL4028_14_next_target", bool(next_target and "4029" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4028_15_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4028_16_outputs_in_source_dir", all(str(path).startswith(str(SOURCE_DIR)) for path in OUTPUTS.values()), "CSV outputs stay in source intake", ts)
    add_validation(rows, "VAL4028_17_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4028_18_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4028_19_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in derivation + sign_gate + bound_row), "derivation/sign/bound rows remain nonclaim", ts)
    add_validation(rows, "VAL4028_20_owner_not_adopted", all("ADOPTED" not in str(row.get("status", "")) or "NOT_ADOPTED" in str(row.get("status", "")) for row in owner_template), "owner templates are not falsely adopted", ts)
    return rows


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    derivation = build_derivation(ts)
    sign_gate = build_sign_gate(ts)
    owner_template = build_owner_template(ts)
    bound_row = build_bound_row(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["derivation"], derivation)
    write_csv(OUTPUTS["sign_gate"], sign_gate)
    write_csv(OUTPUTS["owner_template"], owner_template)
    write_csv(OUTPUTS["bound_row"], bound_row)
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
        derivation,
        sign_gate,
        owner_template,
        bound_row,
        results,
        decisions,
        claims,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4028 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
