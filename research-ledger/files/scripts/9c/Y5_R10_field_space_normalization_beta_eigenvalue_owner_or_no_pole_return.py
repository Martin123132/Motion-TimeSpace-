from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "617-Y5-R10-field-space-normalization-beta-eigenvalue-owner-or-no-pole-return.md"
SCRIPT_REL = "scripts/Y5_R10_field_space_normalization_beta_eigenvalue_owner_or_no_pole_return.py"
STATUS = "Y5_R10_field_space_normalization_law_derived_conditionally_beta_not_owned_no_pole_return_selected"
CLAIM_CEILING = "conditional_field_space_contract_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "618-Y5-R10-no-pole-source-zero-certificate-after-finite-branch-demotion.md"

HBAR_C_EVM = 1.973269804e-7
EV_J = 1.602176634e-19
C_M_S = 299_792_458.0
G_SI = 6.67430e-11
MPC_M = 3.0856775814913673e22
H0_KM_S_MPC = 67.4
OMEGA_DE = 0.685


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def f(value: float) -> str:
    return f"{value:.12e}"


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def vacuum_scale() -> dict[str, float]:
    h0_s = H0_KM_S_MPC * 1000.0 / MPC_M
    rho_crit_j_m3 = 3.0 * h0_s * h0_s * C_M_S * C_M_S / (8.0 * math.pi * G_SI)
    rho_de_j_m3 = OMEGA_DE * rho_crit_j_m3
    rho_de_ev4 = (rho_de_j_m3 / EV_J) * (HBAR_C_EVM**3)
    e_de_ev = rho_de_ev4 ** 0.25
    ell_de_m = HBAR_C_EVM / e_de_ev
    return {
        "H0_s_minus1": h0_s,
        "rho_crit_J_m3": rho_crit_j_m3,
        "rho_DE_J_m3": rho_de_j_m3,
        "rho_DE_eV4": rho_de_ev4,
        "sqrt_rho_DE_eV2": math.sqrt(rho_de_ev4),
        "E_DE_eV": e_de_ev,
        "ell_DE_m": ell_de_m,
        "ell_DE_um": ell_de_m * 1.0e6,
        "M2_over_Z_beta1_m_minus2": 1.0 / (ell_de_m * ell_de_m),
    }


def log_interp_alpha(curve_rows: list[dict[str, str]], lambda_m: float) -> tuple[float, str]:
    rows = sorted(curve_rows, key=lambda row: float(row["lambda_value"]))
    if lambda_m <= float(rows[0]["lambda_value"]):
        return float(rows[0]["alpha_bound"]), "clamped_low:" + rows[0]["bound_id"]
    if lambda_m >= float(rows[-1]["lambda_value"]):
        return float(rows[-1]["alpha_bound"]), "clamped_high:" + rows[-1]["bound_id"]
    log_lam = math.log10(lambda_m)
    for left, right in zip(rows, rows[1:]):
        l0 = float(left["lambda_value"])
        l1 = float(right["lambda_value"])
        if l0 <= lambda_m <= l1:
            x0 = math.log10(l0)
            x1 = math.log10(l1)
            y0 = math.log10(float(left["alpha_bound"]))
            y1 = math.log10(float(right["alpha_bound"]))
            t = 0.0 if x1 == x0 else (log_lam - x0) / (x1 - x0)
            alpha = 10 ** (y0 + t * (y1 - y0))
            return alpha, f"log_interp:{left['bound_id']}->{right['bound_id']}"
    raise RuntimeError("interpolation failed")


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("616-Y5-R10-vacuum-scale-parent-X-block-owner-or-demote-to-range-closure.md", "616 immediate handoff"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_616_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_616_NONCLAIM_SUMMARY.csv", "prior nonclaim summary"),
        ("source-intake/mts_residuals/P8_Y5_R10_616_VACUUM_OWNER_ATTEMPT.csv", "vacuum owner blocker rows"),
        ("source-intake/mts_residuals/P8_Y5_R10_616_BETA_OWNER_ATTEMPT.csv", "beta candidate pressure rows"),
        ("source-intake/mts_residuals/P8_Y5_R10_616_PARENT_X_BLOCK_OWNER_CONTRACT.csv", "field-space owner contract"),
        ("580-Y5-R10-explicit-parent-X-block-ansatz-or-finite-residual-score.md", "no-pole route target and finite residual fallback"),
        ("511-minimal-parent-action-local-GR-fixed-point-ansatz.md", "local-GR fixed-point/double-zero contract"),
        ("210-GK-alphaK-parent-invariant-or-fixed-closure.md", "field-space metric precedent"),
        ("223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X multiplier/no-dof route"),
        ("224-defect-potential-Vdef-or-X-route-demotion.md", "partial Vdef owner and X route demotion precedent"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "review-candidate R10 pressure curve"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim placeholder kept unchanged"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_field_space_rows(vac: dict[str, float]) -> list[dict[str, object]]:
    return [
        {
            "row_id": "FS617_0_exact_second_variation",
            "target": "derive the invariant finite-X range law from a vacuum-normalized local block",
            "mathematical_form": "S_X=int sqrt(h)[1/2 Z_X |grad X|^2 + rho_vac U(X/f_X)]",
            "derived_result": "M_X^2/Z_X = rho_vac U''(0)/(Z_X f_X^2)",
            "owner_status": "identity_derived",
            "missing_piece": "explicit parent choice of U, Z_X, and f_X",
            "valid_for_claim": "false",
        },
        {
            "row_id": "FS617_1_beta_invariant",
            "target": "isolate the dimensionless invariant that actually selects lambda_X",
            "mathematical_form": "beta_eff = ell_vac^2 M_X^2/Z_X = U''(0) rho_vac^(1/2)/(Z_X f_X^2)",
            "derived_result": "beta_eff is invariant under harmless X-coordinate relabelling if Z_X f_X^2 is transformed consistently",
            "owner_status": "invariant_identified",
            "missing_piece": "parent field-space metric fixing Z_X f_X^2",
            "valid_for_claim": "false",
        },
        {
            "row_id": "FS617_2_canonical_vacuum_metric",
            "target": "make rho_vac produce a mass scale without a hidden knob",
            "mathematical_form": "Z_X f_X^2 = rho_vac^(1/2)",
            "derived_result": f"then beta_eff=U''(0); sqrt(rho_DE)={f(vac['sqrt_rho_DE_eV2'])} eV^2",
            "owner_status": "clean_contract_not_signed",
            "missing_piece": "no current parent Ward identity fixes the X field-space metric to rho_vac^(1/2)",
            "valid_for_claim": "false",
        },
        {
            "row_id": "FS617_3_rescaling_guard",
            "target": "block fake beta derivations from field rescaling",
            "mathematical_form": "X -> a X changes f_X and Z_X but not Z_X f_X^2 if the parent metric is real",
            "derived_result": "only the product Z_X f_X^2 and the Hessian eigenvalue are physical",
            "owner_status": "guardrail_pass",
            "missing_piece": "normalization ledger tying lambda_X and C_X to the same parent branch",
            "valid_for_claim": "false",
        },
        {
            "row_id": "FS617_4_existing_corpus_check",
            "target": "find a current source that already owns the X field-space metric",
            "mathematical_form": "M_AB or DeWitt/defect metric restricted to X direction",
            "derived_result": "nearby files own pieces of trace/flow/G_K conditionally, but not the full X metric or cross-term policy",
            "owner_status": "not_found",
            "missing_piece": "parent M_AB restricted to X plus stress/Bianchi variation",
            "valid_for_claim": "false",
        },
        {
            "row_id": "FS617_5_finite_branch_ceiling",
            "target": "decide whether finite short-range branch can be promoted",
            "mathematical_form": "parent_signed(Z_X f_X^2) and parent_signed(U''(0)) required before R10 comparison",
            "derived_result": "the finite branch remains closure-only until both are signed",
            "owner_status": "promotion_blocked",
            "missing_piece": "field-space metric theorem and beta spectrum theorem",
            "valid_for_claim": "false",
        },
    ]


def build_beta_spectrum_rows(curve_rows: list[dict[str, str]], epsilon_shell: float, vac: dict[str, float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    candidates = [
        ("BS617_0_beta1", 1.0, "single_canonical_X_mode", "U''(0)=1", "natural but transition-band, not short-forgiving", "conditional_not_signed"),
        ("BS617_1_beta3", 3.0, "spatial_trace_eigenvalue", "three equal spatial curvature channels", "best low-scrutiny finite theorem target; lambda just above 50 um", "best_conditional_target_not_signed"),
        ("BS617_2_beta4", 4.0, "four_block_trace_eigenvalue", "3+1 equal block if time participates", "short and simple, but requires a time-channel owner", "conditional_not_signed"),
        ("BS617_3_beta5", 5.0, "trace_plus_constraint_effective_mode", "trace block plus one/two auxiliary stiffness contributions", "numerically excellent but less clean than beta=3", "candidate_not_signed"),
        ("BS617_4_beta6", 6.0, "rank_two_or_l2_regular_mode", "regular tensor/eigenvalue count candidate", "short and safe, but risks looking model-chosen", "candidate_not_signed"),
        ("BS617_5_direct_38p6_backsolve", 5.206677122050, "direct_range_backsolve", "beta chosen to hit lambda=38.6 um", "forbidden as derivation unless independently reproduced", "closure_only"),
    ]
    for row_id, beta, route, eigen_contract, interpretation, status in candidates:
        lambda_m = vac["ell_DE_m"] / math.sqrt(beta)
        alpha_bound, interpolation = log_interp_alpha(curve_rows, lambda_m)
        rows.append(
            {
                "beta_id": row_id,
                "beta_eff": f(beta),
                "candidate_owner_route": route,
                "eigenvalue_contract": eigen_contract,
                "lambda_X_m": f(lambda_m),
                "lambda_X_um": f(lambda_m * 1.0e6),
                "M_X2_over_Z_X_m_minus2": f(1.0 / (lambda_m * lambda_m)),
                "alpha_bound_review_candidate": f(alpha_bound),
                "max_abs_CX_review_pressure": f(alpha_bound / epsilon_shell),
                "interpolation": interpolation,
                "interpretation": interpretation,
                "current_status": status,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_no_pole_return_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "NP617_0_finite_branch_status",
            "route": "finite_vacuum_scale_X",
            "current_result": "conditional algebra derived but parent field-space metric and beta eigenvalue not signed",
            "allowed_use": "nonclaim range-closure theorem target and pressure map",
            "forbidden_use": "local-GR reduction, R10 pass, or predicted lambda claim",
            "next_action": "retain_as_closure_sidecar",
            "valid_for_claim": "false",
        },
        {
            "route_id": "NP617_1_no_pole_return",
            "route": "quotient_vertical_no_pole",
            "current_result": "still the cleanest GR-reduction route because it removes the physical X Green function",
            "allowed_use": "attempt parent certificate delta_X pi=0, no X pole, no boundary charge",
            "forbidden_use": "declare X absent after gauge/readout rather than before variation",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "NP617_2_source_zero_return",
            "route": "positive_sourcefree_X_nohair",
            "current_result": "secondary route if X is physical but channelwise J_X and boundary flux vanish",
            "allowed_use": "prove source/test/boundary/projector zeros in one normalization ledger",
            "forbidden_use": "use WEP or covariance alone as source-zero proof",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "NP617_3_residual_bound_fallback",
            "route": "finite_alpha_residual",
            "current_result": "survival may be possible for C_X around 100 and short lambda, but that is not a derivation",
            "allowed_use": "private local-bound smoke row after coefficients are source-backed",
            "forbidden_use": "treat empirical survival as field-theory completion",
            "next_action": "only_after_no_pole_or_source_zero_attempt",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D617_0_main_verdict",
            "status": STATUS,
            "decision": "derive the exact finite-branch field-space law conditionally, but do not promote it",
            "meaning": "the missing object is no longer vague: parent must fix Z_X f_X^2 and U''(0)",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D617_1_beta3_target",
            "status": "beta3_spatial_trace_best_low_scrutiny_target_not_signed",
            "decision": "keep beta=3 as the cleanest finite theorem target",
            "meaning": "if X is a canonically vacuum-normalized spatial-trace mode, lambda_X=50.85 um follows",
            "next_target": "future_beta_eigenvalue_theorem_only_if_new_parent_metric_available",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D617_2_range_closure",
            "status": "finite_short_range_branch_closure_sidecar",
            "decision": "finite short-range route remains a sidecar, not the main local-GR proof",
            "meaning": "without field-space/eigenvalue ownership, the branch is still closure even if numerically forgiving",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D617_3_no_pole_return",
            "status": "no_pole_source_zero_return_selected",
            "decision": "return the next derivation attempt to no-pole/source-zero certificate",
            "meaning": "to reduce to GR like GR reduces to Newton, remove or silence the physical X pole instead of tuning its range",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D617_4_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "this checkpoint only sharpens the theorem contract",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_update_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU617_0_allowed",
            "allowed_after_617": "state the exact finite-branch law beta_eff=U'' rho_vac^(1/2)/(Z_X f_X^2)",
            "forbidden_after_617": "state that rho_DE by itself predicts lambda_X",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU617_1_allowed",
            "allowed_after_617": "use beta=3 as a low-scrutiny theorem target",
            "forbidden_after_617": "use beta=3,4,5,or 5.2067 as a claimed prediction",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU617_2_allowed",
            "allowed_after_617": "return to quotient/no-pole and source-zero routes for local-GR reduction",
            "forbidden_after_617": "let finite R10 survival replace a GR-reduction theorem",
            "next_action": NEXT_TARGET,
        },
    ]


def build_summary_rows(vac: dict[str, float], beta_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    beta3 = next(row for row in beta_rows if row["beta_id"] == "BS617_1_beta3")
    beta5 = next(row for row in beta_rows if row["beta_id"] == "BS617_3_beta5")
    direct = next(row for row in beta_rows if row["beta_id"] == "BS617_5_direct_38p6_backsolve")
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "field_space_law": "beta_eff=Upp0*rho_vac^(1/2)/(Z_X*f_X^2)",
            "canonical_metric_contract": "Z_X*f_X^2=rho_vac^(1/2)",
            "canonical_metric_signed": "false",
            "beta_eigenvalue_signed": "false",
            "ell_DE_um": f(vac["ell_DE_um"]),
            "sqrt_rho_DE_eV2": f(vac["sqrt_rho_DE_eV2"]),
            "beta3_lambda_um": beta3["lambda_X_um"],
            "beta3_max_abs_CX": beta3["max_abs_CX_review_pressure"],
            "beta5_lambda_um": beta5["lambda_X_um"],
            "beta5_max_abs_CX": beta5["max_abs_CX_review_pressure"],
            "direct_38p6um_status": direct["current_status"],
            "selected_next_route": "no_pole_or_source_zero_certificate",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    field_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    no_pole_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row for row in source_register if not parse_bool(row["exists"])]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    no_claim_rows = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for table in [field_rows, beta_rows, no_pole_rows, decision_rows, summary_rows]
        for row in table
    )
    exact_law_present = any(row["owner_status"] == "identity_derived" for row in field_rows)
    canonical_not_signed = summary_rows[0]["canonical_metric_signed"] == "false"
    beta3_target = any(row["beta_id"] == "BS617_1_beta3" and row["current_status"] == "best_conditional_target_not_signed" for row in beta_rows)
    direct_demoted = any(row["beta_id"] == "BS617_5_direct_38p6_backsolve" and row["current_status"] == "closure_only" for row in beta_rows)
    no_pole_selected = summary_rows[0]["selected_next_route"] == "no_pole_or_source_zero_certificate"
    return [
        {"check_id": "V617_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": f"missing={len(missing_sources)}"},
        {"check_id": "V617_1_prior_616_clean", "result": "pass" if not prior_failures else "fail", "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}"},
        {"check_id": "V617_2_field_space_law_derived_conditionally", "result": "pass" if exact_law_present else "fail", "detail": str(summary_rows[0]["field_space_law"])},
        {"check_id": "V617_3_canonical_metric_not_signed", "result": "pass" if canonical_not_signed else "fail", "detail": "Z_X*f_X^2=rho_vac^(1/2) remains contract"},
        {"check_id": "V617_4_beta3_target_retained_not_claimed", "result": "pass" if beta3_target else "fail", "detail": "beta3 spatial-trace target"},
        {"check_id": "V617_5_direct_backsolve_demoted", "result": "pass" if direct_demoted else "fail", "detail": "beta=5.2067 closure_only"},
        {"check_id": "V617_6_no_pole_return_selected", "result": "pass" if no_pole_selected else "fail", "detail": str(summary_rows[0]["selected_next_route"])},
        {"check_id": "V617_7_no_claim_rows", "result": "pass" if no_claim_rows else "fail", "detail": f"all_valid_for_claim_false={no_claim_rows}"},
        {"check_id": "V617_8_next_target_set", "result": "pass" if decision_rows[0]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V617_9_no_R10_or_local_GR_claim", "result": "pass", "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false"},
    ]


def write_doc(
    generated: str,
    source_register: list[dict[str, object]],
    field_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    no_pole_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 617 Y5 R10 field-space normalization beta eigenvalue owner or no-pole return

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The exact finite-branch law was derived conditionally:
  `beta_eff = U''(0) rho_vac^(1/2)/(Z_X f_X^2)`.
- This is useful because the missing object is now precise: the parent action must own `Z_X f_X^2` and the Hessian eigenvalue `U''(0)`.
- The clean contract would be `Z_X f_X^2 = rho_vac^(1/2)`, which makes `beta_eff=U''(0)`. Current corpus does not derive that field-space metric.
- `beta=3` is the best low-scrutiny finite theorem target: a canonical spatial-trace eigenvalue would give `lambda_X={summary_rows[0]['beta3_lambda_um']} um`.
- Because the field-space metric and beta eigenvalue are not signed, the finite short-range branch remains closure-only. The next main route returns to no-pole/source-zero.

## Derivation
Starting from

```text
S_X = int sqrt(h)[1/2 Z_X |grad X|^2 + rho_vac U(X/f_X)]
```

the local second variation gives

```text
M_X^2/Z_X = rho_vac U''(0)/(Z_X f_X^2).
```

With `ell_vac^-2 = rho_vac^(1/2)` in natural units,

```text
beta_eff = ell_vac^2 M_X^2/Z_X
         = U''(0) rho_vac^(1/2)/(Z_X f_X^2).
```

So a finite prediction needs two independent parent facts: a field-space metric and a dimensionless eigenvalue. Without both, the range is still chosen by closure, even if the number is attractive.

## Source Register
{md_table(source_register)}

## Field-Space Normalization Attempt
{md_table(field_rows)}

## Beta Eigenvalue Candidate Ledger
{md_table(beta_rows)}

## No-Pole Return Gate
{md_table(no_pole_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(summary_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This round did not give the knockout, but it did something important: it removed the fog. The finite branch can only become a prediction if a parent Ward/metric theorem fixes `Z_X f_X^2` and a real Hessian spectrum gives beta, preferably `3`. Until then, the more serious GR-reduction path is no-pole/source-zero: make the extra local force absent by principle, not merely short-ranged by a nice-looking scale.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated = utc_now()
    source_register = build_source_register()
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_616_VALIDATION.csv")
    summary_613 = read_csv(OUT / "P8_Y5_R10_613_NONCLAIM_SUMMARY.csv")[0]
    epsilon_shell = float(summary_613["epsilon_shell"])
    curve_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv")
    vac = vacuum_scale()

    field_rows = build_field_space_rows(vac)
    beta_rows = build_beta_spectrum_rows(curve_rows, epsilon_shell, vac)
    no_pole_rows = build_no_pole_return_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_update_rows()
    summary_rows = build_summary_rows(vac, beta_rows)
    validation_rows = build_validation_rows(
        source_register,
        prior_validation,
        field_rows,
        beta_rows,
        no_pole_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(OUT / "P8_Y5_R10_617_SOURCE_REGISTER.csv", source_register)
    write_csv(OUT / "P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv", field_rows)
    write_csv(OUT / "P8_Y5_R10_617_BETA_EIGENVALUE_CANDIDATE_LEDGER.csv", beta_rows)
    write_csv(OUT / "P8_Y5_R10_617_NO_POLE_RETURN_GATE.csv", no_pole_rows)
    write_csv(OUT / "P8_Y5_BRR545_617_DECISION.csv", decision_rows)
    write_csv(OUT / "P8_Y5_BRR545_617_ROUTE_UPDATE.csv", route_rows)
    write_csv(OUT / "P8_Y5_R10_617_NONCLAIM_SUMMARY.csv", summary_rows)
    write_csv(OUT / "P8_Y5_BRR545_617_VALIDATION.csv", validation_rows)

    write_doc(
        generated,
        source_register,
        field_rows,
        beta_rows,
        no_pole_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC),
        "validation": rel(OUT / "P8_Y5_BRR545_617_VALIDATION.csv"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
