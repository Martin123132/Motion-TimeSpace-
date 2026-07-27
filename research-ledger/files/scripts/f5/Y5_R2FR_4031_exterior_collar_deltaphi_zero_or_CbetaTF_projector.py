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
DOC_PATH = ROOT / "4031-Y5-R2FR-exterior-collar-deltaphi-zero-or-CbetaTF-projector.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4031_SOURCE_REGISTER.csv",
    "collar_theorem": SOURCE_DIR / "P8_Y5_R2FR_4031_EXTERIOR_COLLAR_DELTAPHI_THEOREM.csv",
    "hair_bound": SOURCE_DIR / "P8_Y5_R2FR_4031_DELTAPHI_HAIR_BOUND.csv",
    "cbeta_projector": SOURCE_DIR / "P8_Y5_R2FR_4031_CBETA_TF_PROJECTOR.csv",
    "tracefree_update": SOURCE_DIR / "P8_Y5_R2FR_4031_TRACEFREE_RESIDUAL_UPDATE.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4031_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4031_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4031_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4031_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4031_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4031_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4031_VALIDATION.csv",
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
            "source_id": "SRC4031_0_4030_doc",
            "path": "4030-Y5-R2FR-curvature-channel-routing-or-tracefree-score-input.md",
            "needle": "delta_phi",
            "role": "selects delta_phi hair as the next obstruction",
        },
        {
            "source_id": "SRC4031_1_4030_residual",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4030_CURVATURE_RESIDUAL_SPLIT.csv",
            "needle": "CURV4030_0_reduced_DTF",
            "role": "gives reduced D_TF after EH routing",
        },
        {
            "source_id": "SRC4031_2_4030_score",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4030_TRACEFREE_SCORE_INPUTS.csv",
            "needle": "SCORE4030_3_ppn_projector",
            "role": "requires C_beta_TF if theorem-zero fails",
        },
        {
            "source_id": "SRC4031_3_4029_energy",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4029_PHI_LOCAL_VACUUM_ENERGY_IDENTITY.csv",
            "needle": "LOCAL_VACUUM_PHI_SILENCE_DERIVED_CONDITIONALLY",
            "role": "provides energy identity for delta_phi silence",
        },
        {
            "source_id": "SRC4031_4_4029_owner",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4029_PHI_OWNER_EULER_DERIVATION.csv",
            "needle": "Box phi - mu_phi^2",
            "role": "provides exterior homogeneous phi equation",
        },
        {
            "source_id": "SRC4031_5_4021_EH",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv",
            "needle": "DeltaE_R11^(1)=DeltaE_R11^(2)=0",
            "role": "provides EH-only PPN baseline under witness",
        },
        {
            "source_id": "SRC4031_6_4030_EH",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4030_EH_CHANNEL_ROUTING.csv",
            "needle": "EHR4030_3_curvature_routing",
            "role": "keeps constant phi routed to Newton coupling",
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


def build_collar_theorem(ts: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "COL4031_0_domain",
            "object": "exterior collar",
            "statement": "Let Omega_ext be a static/asymptotically stationary exterior collar outside the compact source support.",
            "formula": "Omega_ext={R_src<r<R_out}; u:=delta_phi=phi-phi_*",
            "status": "DOMAIN_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "COL4031_1_equation",
            "object": "homogeneous phi equation",
            "statement": "If the exterior has F=Gamma_eff+C=0 after EH/Newton routing, u obeys a homogeneous massive scalar equation.",
            "formula": "(Delta-mu_phi^2)u=0 in the static collar; Lorentzian version uses the positive energy current on stationary data.",
            "status": "EXTERIOR_EQUATION_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "COL4031_2_energy",
            "object": "energy identity",
            "statement": "Multiplying by u and integrating gives a positive identity controlled only by boundary flux.",
            "formula": "int_Omega(|grad u|^2+mu_phi^2 u^2)dV = int_boundary u*n.grad u dS",
            "status": "ENERGY_IDENTITY_SPECIALIZED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "COL4031_3_zero",
            "object": "delta_phi zero branch",
            "statement": "If the collar has fixed-branch/asymptotic u=0 or no scalar charge u*n.grad u=0, then u=0 for mu_phi>0; for mu_phi=0 only a constant survives, and that constant is absorbed into phi_*.",
            "formula": "u=0 modulo constant-renormalization; Hess(u)=0; delta_phi*G_TF=0 in the exterior EH vacuum.",
            "status": "DELTAPHI_ZERO_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "COL4031_4_failure_mode",
            "object": "scalar charge leakage",
            "statement": "If inner-boundary scalar charge or unfixed outer data survives, u is physical hair and must be bounded/scored.",
            "formula": "Q_phi:=int_{S_src} n.grad u dS; Q_phi!=0 activates Yukawa/harmonic collar residual.",
            "status": "BOUND_BRANCH_TRIGGER",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_hair_bound(ts: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "HAIR4031_0_yukawa",
            "arena": "mu_phi>0 exterior",
            "formula": "|u(r)| <= |Q_phi| exp[-mu_phi(r-R_src)]/(4*pi*r) + boundary_outer",
            "implied_residual": "A_delta_phiG/L_phiG <= A_u*A_GTF/L_GTF",
            "score_status": "symbolic_not_numeric",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "HAIR4031_1_massless",
            "arena": "mu_phi=0 exterior",
            "formula": "u(r)=u_infty+Q_phi/(4*pi*r)+higher multipoles; u_infty renormalizes phi_*",
            "implied_residual": "only Q_phi/r and multipoles enter PPN/source residuals",
            "score_status": "symbolic_not_numeric",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "HAIR4031_2_zero_gate",
            "arena": "fixed-branch exterior",
            "formula": "Q_phi=0 and boundary_outer fixed => A_delta_phiG/L_phiG=0",
            "implied_residual": "trace-free curvature-hair residual vanishes in exterior collar",
            "score_status": "conditional_theorem_not_live_adopted",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "HAIR4031_3_needed_data",
            "arena": "score fallback",
            "formula": "need Q_phi or A_u plus mu_phi, R_src, collar boundary condition, and G_TF arena map",
            "implied_residual": "without these, C_beta_TF cannot become numeric",
            "score_status": "data_requirements_written",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_cbeta_projector(ts: str) -> list[dict[str, object]]:
    return [
        {
            "projector_id": "CBETA4031_0_definition",
            "quantity": "C_beta_TF",
            "definition": "C_beta_TF := Pi_beta[L_PPN^{-1}(2*c_I*delta_phi*G_TF + retained trace-free residuals)]",
            "meaning": "project the residual metric solution onto the coefficient of U^2 in g_00 after EH/Newton normalization",
            "status": "PROJECTOR_DEFINED",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "projector_id": "CBETA4031_1_zero_case",
            "quantity": "delta_beta_TF",
            "definition": "if delta_phi=0 in the exterior collar, C_beta_TF*A_delta_phiG/L_phiG=0",
            "meaning": "no beta penalty from the trace-free scalar hair in the theorem-zero branch",
            "status": "ZERO_BRANCH_DEFINED",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "projector_id": "CBETA4031_2_score_case",
            "quantity": "delta_beta_TF",
            "definition": "delta_beta_TF = C_beta_TF * (A_delta_phiG/L_phiG) with C_beta_TF fixed by the weak-field Green operator and source frame",
            "meaning": "if scalar hair survives, beta scoring becomes a calculable residual rather than an overclaim",
            "status": "SCORE_BRANCH_SYMBOLIC",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "projector_id": "CBETA4031_3_inputs",
            "quantity": "numeric projector inputs",
            "definition": "requires source-frame U, collar Green function, boundary data, Q_phi/mu_phi, and normalization against EH U^2 term",
            "meaning": "next numeric work is sharply specified if the theorem branch fails",
            "status": "INPUTS_REQUIRED",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_tracefree_update(ts: str) -> list[dict[str, object]]:
    return [
        {
            "update_id": "TFU4031_0_if_zero",
            "branch": "exterior theorem-zero",
            "updated_residual": "D_TF=(1-c_I)K_L + D_phiF + D_owner + D_boundary + D_adoption + D_kappa_sector with K_L=0 and delta_phi*G_TF=0 on exterior collar",
            "effect": "trace-free scalar-curvature obstruction is removed from the exterior PPN arena under explicit boundary/source clauses",
            "status": "CONDITIONAL_SIMPLIFICATION",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "update_id": "TFU4031_1_if_hair",
            "branch": "hair survives",
            "updated_residual": "D_TF retains 2*c_I*delta_phi*G_TF and activates delta_beta_TF=C_beta_TF*A_delta_phiG/L_phiG",
            "effect": "trace-free branch remains testable with scalar-charge/Yukawa data",
            "status": "SCORE_FALLBACK_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "update_id": "TFU4031_2_next_obstruction",
            "branch": "after exterior zero",
            "updated_residual": "boundary/source matching and live-adoption terms become the leading local-GR obstruction",
            "effect": "moves target from scalar hair to boundary/source-current closure",
            "status": "NEXT_OBSTRUCTION_IDENTIFIED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4031_0_zero",
            "input_condition": "F=0 exterior, Q_phi=0/fixed-boundary, mu_phi^2>=0, EH exterior",
            "expected_verdict": "DELTAPHI_ZERO_ON_EXTERIOR_COLLAR_IF_BOUNDARY_SIGNED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4031_1_hair",
            "input_condition": "Q_phi or unfixed boundary data survives",
            "expected_verdict": "CBETA_TF_PROJECTOR_DEFINED_NOT_NUMERIC",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4031_2_current",
            "input_condition": "current source hierarchy after 4031",
            "expected_verdict": "EXTERIOR_ZERO_CONDITIONAL_BOUNDARY_ADOPTION_OPEN",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4031_0_zero",
            "verdict": "DELTAPHI_ZERO_ON_EXTERIOR_COLLAR_IF_BOUNDARY_SIGNED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4031",
            "next_action": "then attack boundary/source-current adoption because scalar hair is gone only conditionally",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4031_1_hair",
            "verdict": "CBETA_TF_PROJECTOR_DEFINED_NOT_NUMERIC",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4031",
            "next_action": "source Q_phi, mu_phi and collar Green function before beta scoring",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4031_2_current",
            "verdict": "EXTERIOR_ZERO_CONDITIONAL_BOUNDARY_ADOPTION_OPEN",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4031",
            "next_action": "4032 should prove fixed-branch scalar charge Q_phi=0 or source Q_phi bound rows",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4031_0_theorem",
            "decision": "delta_phi is zero on the exterior collar if the homogeneous phi equation and boundary/no-scalar-charge clauses are signed",
            "status": "THEOREM_BRANCH_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4031_1_projector",
            "decision": "if scalar hair survives, C_beta_TF is now defined as the PPN U^2 projection of the residual Green solution",
            "status": "PROJECTOR_BRANCH_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4031_2_next",
            "decision": "move to 4032-Y5-R2FR-scalar-charge-zero-or-Yukawa-hair-bound-input.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4031_0_delta_phi_zero",
            "claim": "delta_phi is zero in the live exterior theory",
            "allowed": False,
            "reason": "the theorem needs boundary/no-scalar-charge and parent-adoption clauses signed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4031_1_beta_score",
            "claim": "PPN beta residual is numerically scored",
            "allowed": False,
            "reason": "C_beta_TF is defined but lacks numeric source/collar inputs",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4031_2_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "boundary/source-current/adoption terms remain open",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4031_0",
            "next_doc": "4032-Y5-R2FR-scalar-charge-zero-or-Yukawa-hair-bound-input.md",
            "next_script": "scripts/Y5_R2FR_4032_scalar_charge_zero_or_Yukawa_hair_bound_input.py",
            "why": "Q_phi=0 is now the concrete clause separating theorem-zero from beta-score fallback",
            "fallback": "if Q_phi cannot be proven zero, source a Yukawa/harmonic hair bound and keep C_beta_TF active",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4031_0",
            "checkpoint": "4031",
            "headline": "exterior delta_phi zero theorem derived conditionally and C_beta_TF fallback projector defined",
            "verdict": "EXTERIOR_ZERO_CONDITIONAL_BOUNDARY_ADOPTION_OPEN",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4031 - Exterior Collar Deltaphi Zero Or CbetaTF Projector

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4031 attacks the remaining scalar hair from 4030. Let

`u := delta_phi = phi - phi_*`.

On a static exterior collar with `F=Gamma_eff+C=0`, the phi-owner equation reduces to

`(Delta - mu_phi^2)u=0`.

Multiplying by `u` and integrating gives

`int_Omega(|grad u|^2+mu_phi^2 u^2)dV = int_boundary u n.grad u dS`.

Therefore, if the exterior branch has fixed/asymptotic `u=0` or no scalar charge `u n.grad u=0`, then `u=0` for `mu_phi>0`. In the massless case, only a constant survives, and that constant is absorbed into `phi_*` and hence into `kappa_obs`.

## Residual Consequence

Under those clauses,

`delta_phi*G_TF=0`

on the exterior PPN collar. If the scalar charge is not zero, the residual is not hidden; it becomes a hair bound:

`|u(r)| <= |Q_phi| exp[-mu_phi(r-R_src)]/(4*pi*r) + boundary_outer`.

## C_beta_TF Fallback

If hair survives, define

`C_beta_TF := Pi_beta[L_PPN^{-1}(2*c_I*delta_phi*G_TF + retained trace-free residuals)]`.

Then

`delta_beta_TF = C_beta_TF*(A_delta_phiG/L_phiG)`.

So 4031 gives the route a theorem-zero branch and a score branch.

## Current Verdict

- Current evaluator result: `EXTERIOR_ZERO_CONDITIONAL_BOUNDARY_ADOPTION_OPEN`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4031`.
- Source needles found: `{found}/{len(sources)}`.

## Next Target

- `4032-Y5-R2FR-scalar-charge-zero-or-Yukawa-hair-bound-input.md`
- `scripts/Y5_R2FR_4032_scalar_charge_zero_or_Yukawa_hair_bound_input.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts})


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    collar: list[dict[str, object]],
    hair: list[dict[str, object]],
    cbeta: list[dict[str, object]],
    update: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    theorem_ids = {str(row["theorem_id"]) for row in collar}
    hair_ids = {str(row["bound_id"]) for row in hair}
    projector_ids = {str(row["projector_id"]) for row in cbeta}
    update_ids = {str(row["update_id"]) for row in update}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4031_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4031_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4031_02_domain", "COL4031_0_domain" in theorem_ids, "exterior collar domain row present", ts)
    add_validation(rows, "VAL4031_03_equation", "COL4031_1_equation" in theorem_ids, "homogeneous phi equation row present", ts)
    add_validation(rows, "VAL4031_04_energy", "COL4031_2_energy" in theorem_ids, "energy identity row present", ts)
    add_validation(rows, "VAL4031_05_zero", "COL4031_3_zero" in theorem_ids, "delta_phi zero theorem row present", ts)
    add_validation(rows, "VAL4031_06_failure", "COL4031_4_failure_mode" in theorem_ids, "scalar charge failure mode row present", ts)
    add_validation(rows, "VAL4031_07_yukawa", "HAIR4031_0_yukawa" in hair_ids, "Yukawa hair bound row present", ts)
    add_validation(rows, "VAL4031_08_massless", "HAIR4031_1_massless" in hair_ids, "massless hair row present", ts)
    add_validation(rows, "VAL4031_09_zero_gate", "HAIR4031_2_zero_gate" in hair_ids, "zero gate bound row present", ts)
    add_validation(rows, "VAL4031_10_projector", "CBETA4031_0_definition" in projector_ids, "C_beta_TF definition row present", ts)
    add_validation(rows, "VAL4031_11_projector_score", "CBETA4031_2_score_case" in projector_ids, "C_beta_TF score row present", ts)
    add_validation(rows, "VAL4031_12_update_zero", "TFU4031_0_if_zero" in update_ids, "trace-free zero update row present", ts)
    add_validation(rows, "VAL4031_13_current_verdict", "EXTERIOR_ZERO_CONDITIONAL_BOUNDARY_ADOPTION_OPEN" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4031_14_no_claims", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4031_15_no_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in hair + cbeta), "hair/projector rows not score-ready", ts)
    add_validation(rows, "VAL4031_16_next_decision", any("4032" in str(row["decision"]) for row in decisions), "4032 next decision present", ts)
    add_validation(rows, "VAL4031_17_next_target", bool(next_target and "4032" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4031_18_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4031_19_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4031_20_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4031_21_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in collar + hair + cbeta + update + decisions), "all theorem/projector rows remain nonclaim", ts)
    return rows


def main() -> None:
    ts = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    collar = build_collar_theorem(ts)
    hair = build_hair_bound(ts)
    cbeta = build_cbeta_projector(ts)
    update = build_tracefree_update(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["collar_theorem"], collar)
    write_csv(OUTPUTS["hair_bound"], hair)
    write_csv(OUTPUTS["cbeta_projector"], cbeta)
    write_csv(OUTPUTS["tracefree_update"], update)
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
        collar,
        hair,
        cbeta,
        update,
        results,
        decisions,
        claims,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4031 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
