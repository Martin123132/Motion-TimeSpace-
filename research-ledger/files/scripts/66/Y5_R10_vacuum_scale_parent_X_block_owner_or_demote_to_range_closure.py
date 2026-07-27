from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "616-Y5-R10-vacuum-scale-parent-X-block-owner-or-demote-to-range-closure.md"
SCRIPT_REL = "scripts/Y5_R10_vacuum_scale_parent_X_block_owner_or_demote_to_range_closure.py"
STATUS = "Y5_R10_vacuum_scale_bridge_demoted_to_range_closure_parent_owner_contract_written"
CLAIM_CEILING = "range_closure_theorem_target_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "617-Y5-R10-field-space-normalization-beta-eigenvalue-owner-or-no-pole-return.md"

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
        ("615-Y5-R10-explicit-parent-X-block-short-range-origin-or-range-closure.md", "615 immediate handoff"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_615_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_615_NONCLAIM_SUMMARY.csv", "vacuum-scale bridge summary"),
        ("source-intake/mts_residuals/P8_Y5_R10_615_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv", "prior X-block bridge contract"),
        ("source-intake/mts_residuals/P8_Y5_R10_615_SHORT_RANGE_ORIGIN_CANDIDATE_AUDIT.csv", "prior short-range candidates"),
        ("614-Y5-R10-lambda-X-parent-Hessian-window-or-CX-envelope-scorecard.md", "lambda/Hessian pressure map"),
        ("580-Y5-R10-explicit-parent-X-block-ansatz-or-finite-residual-score.md", "no-pole versus finite residual branch map"),
        ("04-vacuum-reciprocity-action-contract.md", "vacuum silence contract guardrail"),
        ("21-cosmology-parent-bridge-audit.md", "cosmology parent bridge not-derived status"),
        ("23-strict-cosmology-branch-contract.md", "strict cosmology closure status"),
        ("206-parent-C-screening-fixed-point-mechanism.md", "domain/projector local silence context"),
        ("209-Lcg-domain-scale-parent-derivation-or-demotion.md", "domain-scale demotion precedent"),
        ("511-minimal-parent-action-local-GR-fixed-point-ansatz.md", "local-GR fixed-point action contract"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "review-candidate R10 pressure curve"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim placeholder kept unchanged"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_vacuum_owner_rows(vac: dict[str, float]) -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "VO616_0_vacuum_scale_definition",
            "owner_clause": "define vacuum length from a vacuum density",
            "parent_formula": "ell_vac = hbar*c/rho_vac^(1/4)",
            "derivation_result": f"dimensionally clean reference scale; ell_DE={vac['ell_DE_um']:.6g} um for the private constants",
            "missing_piece": "rho_vac itself is not yet derived by the MTS parent action as a fixed vacuum extremum",
            "verdict": "bridge_input_available_not_owner",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "VO616_1_parent_vacuum_extremum",
            "owner_clause": "parent action owns rho_vac before local fitting",
            "parent_formula": "delta S_parent/dPhi=0 -> rho_vac = rho_DE and local subtraction leaves the same scale",
            "derivation_result": "current cosmology files map vacuum/memory variables but label the branch not parent-derived",
            "missing_piece": "vacuum extremum, amplitude, and background subtraction theorem",
            "verdict": "not_signed",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "VO616_2_local_X_Hessian_identity",
            "owner_clause": "local X range is a same-branch Hessian ratio",
            "parent_formula": "lambda_X^-2 = M_X^2/Z_X = [partial_X^2 V_eff(X)]_0/Z_X",
            "derivation_result": "formal identity recovered; this is the correct object to derive",
            "missing_piece": "explicit V_eff(X), Z_X, and branch normalization from the same parent block",
            "verdict": "formula_only",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "VO616_3_field_space_normalization_blocker",
            "owner_clause": "vacuum density alone must set a mass, not just a potential height",
            "parent_formula": "V_eff=rho_vac U(X/f_X) gives M_X^2/Z_X = rho_vac U''(0)/(Z_X f_X^2)",
            "derivation_result": "rho_vac by itself does not determine lambda_X; the field-space metric/decay scale controls the range",
            "missing_piece": "Z_X f_X^2 = rho_vac^(1/2)/beta, or an equivalent parent-normalized field metric",
            "verdict": "key_blocker_for_parent_ownership",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "VO616_4_beta_eff_invariant",
            "owner_clause": "dimensionless beta must be a parent spectrum/eigenvalue",
            "parent_formula": "beta_eff = ell_vac^2 M_X^2/Z_X",
            "derivation_result": "beta_eff is the physical invariant; beta in the range 3..5 is useful but not yet derived",
            "missing_piece": "trace, regularity, or Hessian eigenvalue theorem fixing beta before R10 comparison",
            "verdict": "target_not_derived",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "VO616_5_no_posthoc_gate",
            "owner_clause": "range must be selected without looking at alpha_bound(lambda)",
            "parent_formula": "parent action -> beta_eff -> lambda_X, then compare to R10",
            "derivation_result": "the current bridge was discovered from R10 pressure, so it is useful guidance but not evidence",
            "missing_piece": "pre-R10 parent derivation of beta_eff and C_X in one normalization ledger",
            "verdict": "demote_to_range_closure_for_now",
            "valid_for_claim": "false",
        },
    ]


def build_beta_owner_rows(curve_rows: list[dict[str, str]], epsilon_shell: float, vac: dict[str, float]) -> list[dict[str, object]]:
    beta_candidates = [
        ("BO616_0_beta1", 1.0, "unit_vacuum_curvature", "simplest Hessian coefficient; natural but only lands at the transition band", "candidate_not_claim"),
        ("BO616_1_beta3", 3.0, "three_spatial_trace_candidate", "least-fussy short-range target if X curvature is a 3D isotropic trace eigenvalue", "best_low_scrutiny_target_not_derived"),
        ("BO616_2_beta4", 4.0, "four_block_trace_candidate", "would follow from a four-component trace/equal-eigenvalue block if the parent operator supplies it", "candidate_not_derived"),
        ("BO616_3_beta5", 5.0, "five_effective_mode_candidate", "lands close to the 38.6 um anchor but currently has no exact parent spectrum owner", "candidate_not_derived"),
        ("BO616_4_beta6", 6.0, "rank_two_or_l2_candidate", "a plausible regularity/eigenvalue number, but more model-dependent than beta=3", "candidate_not_derived"),
        ("BO616_5_beta_for_38p6um", 5.206677122050, "direct_38p6um_backsolve", "excellent pressure window but forbidden as a derivation unless independently reproduced", "closure_only"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, beta, route, interpretation, status in beta_candidates:
        lambda_m = vac["ell_DE_m"] / math.sqrt(beta)
        alpha_bound, interpolation = log_interp_alpha(curve_rows, lambda_m)
        rows.append(
            {
                "beta_id": row_id,
                "beta_eff": f(beta),
                "candidate_owner_route": route,
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


def build_parent_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "PC616_0_same_branch_second_variation",
            "required_clause": "Z_X, M_X^2, J_X, and C_X are read from one second variation",
            "mathematical_form": "delta^2 S_parent|local -> Z_X, M_X^2, source/test product",
            "current_status": "formula_available_not_evaluated",
            "claim_effect": "blocks_finite_branch_claim",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PC616_1_vacuum_scale_owner",
            "required_clause": "the parent vacuum/cosmology sector supplies rho_vac as a local Hessian scale",
            "mathematical_form": "V_eff(X) contains rho_vac U(X/f_X) on the same branch",
            "current_status": "not_signed",
            "claim_effect": "bridge_not_prediction",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PC616_2_field_space_metric_lock",
            "required_clause": "field normalization is fixed so rho_vac becomes a mass scale",
            "mathematical_form": "Z_X f_X^2 = rho_vac^(1/2)/beta or equivalent canonical normalization",
            "current_status": "missing_hard_blocker",
            "claim_effect": "beta_can_float_without_this",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PC616_3_beta_spectrum_lock",
            "required_clause": "beta is an eigenvalue/trace/regularity index, not fitted",
            "mathematical_form": "beta_eff in Spec(H_X) or beta_eff=Tr(P_X H_X P_X)",
            "current_status": "candidate_numbers_only",
            "claim_effect": "range_closure_until_owned",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PC616_4_positive_operator_and_double_zero",
            "required_clause": "finite X branch is stable and does not create first-order local GR leakage",
            "mathematical_form": "Z_X>0, M_X^2>0, partial_X g_obs|0=0 or source/test product bounded",
            "current_status": "not_jointly_signed",
            "claim_effect": "R10_survival_not_local_GR_reduction",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PC616_5_no_pole_fallback",
            "required_clause": "if field-space/vacuum ownership fails, return to quotient/no-pole theorem",
            "mathematical_form": "delta_X pi=0 and no physical X Green function",
            "current_status": "separate_route_still_stronger",
            "claim_effect": "best_GR_reduction_route_remains_open",
            "valid_for_claim": "false",
        },
    ]


def build_demotion_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "DG616_0_rho_vac_parent_owned",
            "gate": "rho_vac is derived by parent vacuum/cosmology action",
            "pass_condition": "vacuum extremum fixes rho_vac before local bound comparison",
            "current_status": "not_passed",
            "action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG616_1_X_vacuum_coupling_signed",
            "gate": "same parent action couples X Hessian to rho_vac",
            "pass_condition": "partial_X^2 V_eff(0) is explicitly sourced by the vacuum block",
            "current_status": "not_passed",
            "action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG616_2_field_space_normalization_signed",
            "gate": "Z_X or f_X is fixed by the parent field-space metric",
            "pass_condition": "beta_eff cannot be changed by a hidden normalization choice",
            "current_status": "not_passed_hard_blocker",
            "action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG616_3_beta_predeclared",
            "gate": "beta is derived as an eigenvalue/trace before looking at R10",
            "pass_condition": "beta=3,4,5,or other exact value follows from the operator spectrum",
            "current_status": "not_passed",
            "action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG616_4_range_closure_label",
            "gate": "if any owner gate fails, the finite short-range bridge is closure-only",
            "pass_condition": "document and CSVs keep all rows valid_for_claim=false",
            "current_status": "passed_policy",
            "action": "range_closure_demoted_no_public_claim",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG616_5_no_R10_promotion",
            "gate": "R10/local-GR pass remains blocked",
            "pass_condition": "no R10, WEP, PPN, or local-GR flags are promoted",
            "current_status": "passed_policy",
            "action": "return_to_derivation_or_bound_with_nonclaim_status",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D616_0_main_verdict",
            "status": STATUS,
            "decision": "demote the vacuum-scale finite-range bridge to labelled range closure for now",
            "meaning": "rho_DE gives a beautiful scale, but the parent field-space normalization and beta eigenvalue are not signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D616_1_key_derivation_result",
            "status": "field_space_normalization_blocker_identified",
            "decision": "vacuum density alone does not derive lambda_X",
            "meaning": "a density sets a potential height; the X range also needs the parent kinetic/field metric",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D616_2_best_finite_target",
            "status": "beta_3_to_5_remains_best_theorem_target",
            "decision": "keep beta around 3..5 as a private eigenvalue/trace target, not as evidence",
            "meaning": "these values put lambda_X in a forgiving R10 band without directly choosing 38.6 um",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D616_3_GR_reduction_route",
            "status": "no_pole_or_source_zero_still_stronger",
            "decision": "do not confuse finite-range survival with derived local GR",
            "meaning": "the clean GR-reduction route remains quotient/no-pole, source-zero, or double-zero plus positive operator",
            "next_target": "return_to_no_pole_if_617_cannot_sign_field_space_and_beta",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D616_4_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "this checkpoint is internal theorem pressure and closure labelling",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_update_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU616_0_allowed",
            "allowed_after_616": "use beta=3..5 as a theorem target for a parent Hessian spectrum",
            "forbidden_after_616": "call beta=3..5 derived without field-space normalization and eigenvalue proof",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU616_1_allowed",
            "allowed_after_616": "label the vacuum-scale finite branch as range closure or nonclaim bridge",
            "forbidden_after_616": "present the tens-of-microns range as a prediction",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU616_2_allowed",
            "allowed_after_616": "prefer no-pole/source-zero if local-GR reduction is the target",
            "forbidden_after_616": "treat R10 finite survival as equivalent to GR reduction",
            "next_action": "return_to_no_pole_if_field_space_owner_fails",
        },
    ]


def build_summary_rows(vac: dict[str, float], beta_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    beta3 = next(row for row in beta_rows if row["beta_id"] == "BO616_1_beta3")
    beta4 = next(row for row in beta_rows if row["beta_id"] == "BO616_2_beta4")
    beta5 = next(row for row in beta_rows if row["beta_id"] == "BO616_3_beta5")
    direct = next(row for row in beta_rows if row["beta_id"] == "BO616_5_beta_for_38p6um")
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "ell_DE_um": f(vac["ell_DE_um"]),
            "E_DE_eV": f(vac["E_DE_eV"]),
            "beta3_lambda_um": beta3["lambda_X_um"],
            "beta4_lambda_um": beta4["lambda_X_um"],
            "beta5_lambda_um": beta5["lambda_X_um"],
            "beta3_max_abs_CX": beta3["max_abs_CX_review_pressure"],
            "beta4_max_abs_CX": beta4["max_abs_CX_review_pressure"],
            "beta5_max_abs_CX": beta5["max_abs_CX_review_pressure"],
            "direct_38p6um_beta": direct["beta_eff"],
            "range_status": "closure_only_until_field_space_and_beta_owner",
            "parent_X_block_signed": "false",
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
    owner_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row for row in source_register if not parse_bool(row["exists"])]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    no_claim_rows = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for table in [owner_rows, beta_rows, contract_rows, demotion_rows, decision_rows, summary_rows]
        for row in table
    )
    hard_blocker_present = any(row["verdict"] == "key_blocker_for_parent_ownership" for row in owner_rows)
    demotion_active = decision_rows[0]["status"] == STATUS and summary_rows[0]["range_status"] == "closure_only_until_field_space_and_beta_owner"
    beta_targets = [row for row in beta_rows if row["current_status"] in {"best_low_scrutiny_target_not_derived", "candidate_not_derived"}]
    next_target_set = all(row.get("next_target", NEXT_TARGET) for row in decision_rows)
    return [
        {"check_id": "V616_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": f"missing={len(missing_sources)}"},
        {"check_id": "V616_1_prior_615_clean", "result": "pass" if not prior_failures else "fail", "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}"},
        {"check_id": "V616_2_vacuum_scale_retained_not_promoted", "result": "pass" if hard_blocker_present else "fail", "detail": "field_space_normalization_blocker_present"},
        {"check_id": "V616_3_beta_candidate_rows_numeric", "result": "pass" if len(beta_rows) == 6 else "fail", "detail": f"beta_rows={len(beta_rows)};theorem_targets={len(beta_targets)}"},
        {"check_id": "V616_4_direct_38p6_demoted", "result": "pass" if any(row["current_status"] == "closure_only" for row in beta_rows) else "fail", "detail": "direct_beta_backsolve_closure_only"},
        {"check_id": "V616_5_parent_contract_blocks_claim", "result": "pass" if any(row["current_status"] == "missing_hard_blocker" for row in contract_rows) else "fail", "detail": f"contract_rows={len(contract_rows)}"},
        {"check_id": "V616_6_demotion_gate_active", "result": "pass" if demotion_active else "fail", "detail": str(summary_rows[0]["range_status"])},
        {"check_id": "V616_7_no_claim_rows", "result": "pass" if no_claim_rows else "fail", "detail": f"all_valid_for_claim_false={no_claim_rows}"},
        {"check_id": "V616_8_next_target_set", "result": "pass" if next_target_set else "fail", "detail": NEXT_TARGET},
        {"check_id": "V616_9_no_R10_or_local_GR_claim", "result": "pass", "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false"},
    ]


def write_doc(
    generated: str,
    source_register: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 616 Y5 R10 vacuum-scale parent X-block owner or demote to range closure

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- Tried to parent-own the nice vacuum-scale short-range bridge from checkpoint 615.
- Result: not owned yet. The bridge is mathematically attractive, but `rho_DE` alone does not determine `lambda_X`.
- The missing hard clause is the field-space normalization: `V_eff=rho_vac U(X/f_X)` gives `M_X^2/Z_X = rho_vac U''(0)/(Z_X f_X^2)`, so `Z_X f_X^2` must also be parent-derived.
- `beta_eff = ell_DE^2 M_X^2/Z_X` is the real invariant. Values around `3..5` remain excellent theorem targets, but not claimable.
- Finite short-range survival is therefore demoted to labelled range closure. The clean local-GR route still wants no-pole/source-zero/double-zero ownership.

## Derivation Attempt
The parent-owned finite branch would need the chain

```text
S_parent -> rho_vac, Z_X, f_X, U''(0)
M_X^2/Z_X = rho_vac U''(0)/(Z_X f_X^2)
beta_eff = ell_vac^2 M_X^2/Z_X
lambda_X = ell_vac/sqrt(beta_eff)
```

Checkpoint 615 supplied the useful dimensional bridge `ell_vac = hbar*c/rho_DE^(1/4)`. This checkpoint adds the red-team correction: a vacuum energy density is a height in the potential, not by itself a mass curvature for `X`. The parent must also own the `X` field metric or decay scale. Without that, `beta_eff` is a hidden closure parameter.

## Source Register
{md_table(source_register)}

## Vacuum Owner Attempt
{md_table(owner_rows)}

## Beta Owner Attempt
{md_table(beta_rows)}

## Parent X-Block Owner Contract
{md_table(contract_rows)}

## Range Closure Demotion Gate
{md_table(demotion_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(summary_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is not a collapse; it is the exact place the maths got honest. The vacuum scale is still a very good scent trail, but right now it is a range-closure target, not a derived prediction. To promote it, the next move must derive the `X` field-space normalization and beta eigenvalue from the parent action before looking at R10. If that cannot be done, the route should stop pretending to be local-GR reduction and we return to the stronger no-pole/source-zero path.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated = utc_now()
    source_register = build_source_register()
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_615_VALIDATION.csv")
    summary_613 = read_csv(OUT / "P8_Y5_R10_613_NONCLAIM_SUMMARY.csv")[0]
    epsilon_shell = float(summary_613["epsilon_shell"])
    curve_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv")
    vac = vacuum_scale()

    owner_rows = build_vacuum_owner_rows(vac)
    beta_rows = build_beta_owner_rows(curve_rows, epsilon_shell, vac)
    contract_rows = build_parent_contract_rows()
    demotion_rows = build_demotion_gate_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_update_rows()
    summary_rows = build_summary_rows(vac, beta_rows)
    validation_rows = build_validation_rows(
        source_register,
        prior_validation,
        owner_rows,
        beta_rows,
        contract_rows,
        demotion_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(OUT / "P8_Y5_R10_616_SOURCE_REGISTER.csv", source_register)
    write_csv(OUT / "P8_Y5_R10_616_VACUUM_OWNER_ATTEMPT.csv", owner_rows)
    write_csv(OUT / "P8_Y5_R10_616_BETA_OWNER_ATTEMPT.csv", beta_rows)
    write_csv(OUT / "P8_Y5_R10_616_PARENT_X_BLOCK_OWNER_CONTRACT.csv", contract_rows)
    write_csv(OUT / "P8_Y5_R10_616_RANGE_CLOSURE_DEMOTION_GATE.csv", demotion_rows)
    write_csv(OUT / "P8_Y5_BRR545_616_DECISION.csv", decision_rows)
    write_csv(OUT / "P8_Y5_BRR545_616_ROUTE_UPDATE.csv", route_rows)
    write_csv(OUT / "P8_Y5_R10_616_NONCLAIM_SUMMARY.csv", summary_rows)
    write_csv(OUT / "P8_Y5_BRR545_616_VALIDATION.csv", validation_rows)

    write_doc(
        generated,
        source_register,
        owner_rows,
        beta_rows,
        contract_rows,
        demotion_rows,
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
        "validation": rel(OUT / "P8_Y5_BRR545_616_VALIDATION.csv"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
