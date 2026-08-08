from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "615-Y5-R10-explicit-parent-X-block-short-range-origin-or-range-closure.md"
SCRIPT_REL = "scripts/Y5_R10_explicit_parent_X_block_short_range_origin_or_range_closure.py"
STATUS = "Y5_R10_short_range_vacuum_scale_bridge_found_but_parent_X_block_not_signed"
CLAIM_CEILING = "vacuum_scale_bridge_and_range_closure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "616-Y5-R10-vacuum-scale-parent-X-block-owner-or-demote-to-range-closure.md"

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


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("614-Y5-R10-lambda-X-parent-Hessian-window-or-CX-envelope-scorecard.md", "614 immediate handoff"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_614_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_614_NONCLAIM_SUMMARY.csv", "lambda scorecard summary"),
        ("source-intake/mts_residuals/P8_Y5_R10_614_LAMBDA_WINDOW_SCORECARD.csv", "range/C_X window pressure"),
        ("source-intake/mts_residuals/P8_Y5_R10_614_PARENT_HESSIAN_CONTRACT.csv", "parent Hessian contract"),
        ("580-Y5-R10-explicit-parent-X-block-ansatz-or-finite-residual-score.md", "prior parent X-block branch candidates"),
        ("source-intake/mts_residuals/P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv", "prior X-block candidate ledger"),
        ("607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md", "epsilon-shell factorization"),
        ("610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md", "finite p1 branch lock"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "review-candidate R10 pressure curve"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim placeholder kept unchanged"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


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


def build_vacuum_bridge_rows(vac: dict[str, float], target_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = [
        {
            "calc_id": "VB615_0_constants",
            "quantity": "input cosmology constants",
            "value": f"H0={H0_KM_S_MPC} km/s/Mpc; Omega_DE={OMEGA_DE}",
            "units": "mixed",
            "meaning": "fixed reference values for private dimensional bridge only",
            "claim_status": "nonclaim_reference",
            "valid_for_claim": "false",
        },
        {
            "calc_id": "VB615_1_rho_DE",
            "quantity": "rho_DE",
            "value": f(vac["rho_DE_J_m3"]),
            "units": "J/m^3",
            "meaning": "dark-energy/vacuum density scale used as candidate parent curvature density",
            "claim_status": "bridge_candidate",
            "valid_for_claim": "false",
        },
        {
            "calc_id": "VB615_2_E_DE",
            "quantity": "rho_DE^(1/4)",
            "value": f(vac["E_DE_eV"]),
            "units": "eV",
            "meaning": "natural mass scale associated with rho_DE in natural units",
            "claim_status": "bridge_candidate",
            "valid_for_claim": "false",
        },
        {
            "calc_id": "VB615_3_ell_DE",
            "quantity": "hbar*c/rho_DE^(1/4)",
            "value": f(vac["ell_DE_um"]),
            "units": "um",
            "meaning": "vacuum-scale length; close to the R10 transition band but not parent-owned",
            "claim_status": "bridge_candidate",
            "valid_for_claim": "false",
        },
    ]
    for target in target_rows:
        lam_m = float(target["lambda_X_m"])
        lam_um = float(target["lambda_X_um"])
        beta_needed = (vac["ell_DE_m"] / lam_m) ** 2
        rows.append(
            {
                "calc_id": "VB615_beta_" + target["target_id"],
                "quantity": "beta_needed_for_target_lambda",
                "value": f(beta_needed),
                "units": "dimensionless",
                "meaning": f"if M_X^2/Z_X=beta/ell_DE^2 then beta={beta_needed:.4g} gives lambda={lam_um:g} um",
                "claim_status": "bridge_target_not_parent_signed",
                "valid_for_claim": "false",
            }
        )
    return rows


def build_scale_candidate_rows(curve_rows: list[dict[str, str]], epsilon_shell: float, vac: dict[str, float]) -> list[dict[str, object]]:
    candidates = [
        ("SC615_0_no_pole", "quotient_vertical_no_pole", None, "K_X=0; no physical Green pole", "best local-GR theorem route, but not a finite short-range derivation", "conditional_theorem_target"),
        ("SC615_1_vacuum_beta1", "vacuum_density_fourth_root_beta1", 1.0, "m_X=sqrt(beta)*rho_DE^(1/4)", "natural meV-scale bridge; lands near transition band", "promising_bridge_not_parent_signed"),
        ("SC615_2_vacuum_beta3", "vacuum_density_fourth_root_beta3", 3.0, "m_X=sqrt(beta)*rho_DE^(1/4)", "order-few Hessian eigenvalue pushes vacuum length into short forgiving band", "best_finite_bridge_candidate"),
        ("SC615_3_vacuum_beta5", "vacuum_density_fourth_root_beta5", 5.0, "m_X=sqrt(beta)*rho_DE^(1/4)", "order-few Hessian eigenvalue lands close to 38.6 um anchor neighbourhood", "best_finite_bridge_candidate"),
        ("SC615_4_direct_mass_closure", "choose_lambda_38p6um_directly", None, "M_X^2/Z_X=6.711590e8 m^-2 inserted", "works as closure but is not a derivation without an owner for the scale", "closure_only"),
        ("SC615_5_regular_core", "regularity_core_length", None, "lambda_X=L_reg if parent regularity supplies L_reg", "potential route, but no numeric parent L_reg is present in the current corpus", "unfilled_theorem_target"),
        ("SC615_6_hubble_scale", "Hubble_or_FLRW_curvature", None, "lambda_X~c/H0", "far too long for an active finite fifth force; only safe with no-pole/source-zero", "rejected_for_finite_R10_branch"),
    ]
    rows: list[dict[str, object]] = []
    for candidate_id, route, beta, formula, interpretation, status in candidates:
        if beta is None and route != "choose_lambda_38p6um_directly":
            lam_m = ""
            lam_um = ""
            m2_over_z = ""
            alpha_bound = ""
            max_cx = ""
            interp = "not_applicable"
        else:
            if route == "choose_lambda_38p6um_directly":
                lam_m_float = 3.86e-5
            else:
                lam_m_float = vac["ell_DE_m"] / math.sqrt(float(beta))
            alpha, interp = log_interp_alpha(curve_rows, lam_m_float)
            lam_m = f(lam_m_float)
            lam_um = f(lam_m_float * 1.0e6)
            m2_over_z = f(1.0 / (lam_m_float * lam_m_float))
            alpha_bound = f(alpha)
            max_cx = f(alpha / epsilon_shell)
        rows.append(
            {
                "candidate_id": candidate_id,
                "route": route,
                "parent_formula_or_contract": formula,
                "lambda_m": lam_m,
                "lambda_um": lam_um,
                "M_X2_over_Z_X_m_minus2": m2_over_z,
                "alpha_bound_review_candidate": alpha_bound,
                "max_abs_CX_review_pressure": max_cx,
                "interpolation": interp,
                "interpretation": interpretation,
                "current_status": status,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_parent_block_rows(vac: dict[str, float]) -> list[dict[str, object]]:
    return [
        {
            "block_id": "XB615_0_minimal_bridge_block",
            "action_block": "S_X^(2)=1/2 int sqrt(h)[Z_X |grad X|^2 + beta*Z_X*ell_vac^-2 X^2] - int sqrt(h) X J_X",
            "derived_consequence": "lambda_X=ell_vac/sqrt(beta)",
            "would_buy": "order-few beta gives 38-50 um and keeps finite p1 branch away from the R10 trough",
            "owner_gap": "parent action must derive ell_vac from the same vacuum/cosmology sector and beta from a Hessian eigenvalue",
            "status": "candidate_parent_block_not_signed",
            "valid_for_claim": "false",
        },
        {
            "block_id": "XB615_1_beta_3_to_5_short_band",
            "action_block": "M_X^2/Z_X=beta/ell_vac^2 with beta in [3,5]",
            "derived_consequence": f"lambda_X={vac['ell_DE_um']/math.sqrt(5):.6g}..{vac['ell_DE_um']/math.sqrt(3):.6g} um",
            "would_buy": "short forgiving R10 window without choosing lambda directly",
            "owner_gap": "beta must be a trace/eigenvalue/regularity coefficient, not a fitted parameter",
            "status": "best_finite_derivation_target",
            "valid_for_claim": "false",
        },
        {
            "block_id": "XB615_2_beta_1_transition",
            "action_block": "M_X^2/Z_X=ell_vac^-2",
            "derived_consequence": f"lambda_X={vac['ell_DE_um']:.6g} um",
            "would_buy": "natural meV-scale range but not as forgiving as 38-50 um",
            "owner_gap": "still requires parent bridge from cosmological vacuum density to local Hessian",
            "status": "promising_but_moderate_pressure",
            "valid_for_claim": "false",
        },
        {
            "block_id": "XB615_3_direct_lambda_closure",
            "action_block": "M_X^2/Z_X=(38.6 um)^-2",
            "derived_consequence": "lambda_X=38.6 um by definition",
            "would_buy": "excellent private pressure but scientifically weak unless scale is independently derived",
            "owner_gap": "post-hoc range selection risk",
            "status": "closure_only_if_used",
            "valid_for_claim": "false",
        },
        {
            "block_id": "XB615_4_no_pole_escape",
            "action_block": "constraint/quotient removes the inverse X operator",
            "derived_consequence": "K_X=0 and lambda_X is irrelevant",
            "would_buy": "strongest GR-reduction route",
            "owner_gap": "first-class constraint/no-boundary-charge proof still missing",
            "status": "separate_theorem_route",
            "valid_for_claim": "false",
        },
    ]


def build_acceptance_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "AG615_0_not_posthoc",
            "acceptance_gate": "short range must be derived before R10 comparison",
            "pass_condition": "parent action yields ell_vac and beta independently of alpha_bound(lambda)",
            "current_status": "not_passed",
            "repair": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG615_1_same_branch",
            "acceptance_gate": "Z_X, M_X^2, C_X, and epsilon_shell are from the same local branch",
            "pass_condition": "one parent normalization ledger transforms all pieces together",
            "current_status": "not_passed",
            "repair": "canonicalize X normalization and source/test product",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG615_2_positive_operator",
            "acceptance_gate": "finite branch is elliptic and stable",
            "pass_condition": "Z_X>0 and M_X^2>0 with no ghost/tachyon",
            "current_status": "not_evaluated",
            "repair": "explicit second variation of proposed X block",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG615_3_beta_owner",
            "acceptance_gate": "dimensionless beta is parent-owned",
            "pass_condition": "beta is a fixed Hessian eigenvalue, trace coefficient, or regularity index",
            "current_status": "not_passed",
            "repair": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG615_4_no_claim",
            "acceptance_gate": "no R10/local-GR promotion from bridge rows",
            "pass_condition": "all generated rows valid_for_claim=false",
            "current_status": "passed_policy",
            "repair": "claim requires parent-signed block plus claim-grade bound curve",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D615_0_derivation_attempt",
            "status": STATUS,
            "decision": "record vacuum-scale Hessian bridge as best finite short-range candidate, not as a derivation",
            "meaning": "the meV vacuum scale naturally sits near the required R10 band, but parent ownership is missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D615_1_direct_range_closure",
            "status": "direct_lambda_choice_rejected_as_derivation",
            "decision": "do not set lambda_X=38.6um by hand",
            "meaning": "that would be a closure/fitted range, not Grossmann-grade derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D615_2_best_next",
            "status": "vacuum_scale_owner_next",
            "decision": "attempt to parent-own ell_vac and beta in the explicit X block",
            "meaning": "if beta~3-5 is derived, the finite branch has a serious non-posthoc route",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D615_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "bridge rows are private theory construction pressure only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_update_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU615_0_allowed",
            "allowed_after_615": "use vacuum-scale bridge as a theorem target for the parent X block",
            "forbidden_after_615": "claim the short range is derived from rho_DE without the parent coupling/eigenvalue proof",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU615_1_allowed",
            "allowed_after_615": "label direct 38.6um range as closure if used",
            "forbidden_after_615": "hide direct lambda selection as a prediction",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU615_2_allowed",
            "allowed_after_615": "keep no-pole theorem as stronger alternate route",
            "forbidden_after_615": "call finite short-range survival local-GR reduction",
            "next_action": "return_to_no_pole_if_vacuum_bridge_fails",
        },
    ]


def build_summary_rows(vac: dict[str, float], candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    beta3 = next(row for row in candidates if row["candidate_id"] == "SC615_2_vacuum_beta3")
    beta5 = next(row for row in candidates if row["candidate_id"] == "SC615_3_vacuum_beta5")
    direct = next(row for row in candidates if row["candidate_id"] == "SC615_4_direct_mass_closure")
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "ell_DE_um": f(vac["ell_DE_um"]),
            "E_DE_eV": f(vac["E_DE_eV"]),
            "beta3_lambda_um": beta3["lambda_um"],
            "beta5_lambda_um": beta5["lambda_um"],
            "beta3_max_abs_CX": beta3["max_abs_CX_review_pressure"],
            "beta5_max_abs_CX": beta5["max_abs_CX_review_pressure"],
            "direct_38p6um_status": direct["current_status"],
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
    bridge_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    block_rows: list[dict[str, object]],
    acceptance_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row for row in source_register if not parse_bool(row["exists"])]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    no_claim_rows = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for table in [bridge_rows, candidate_rows, block_rows, acceptance_rows, decision_rows, summary_rows]
        for row in table
    )
    ell_de = float(summary_rows[0]["ell_DE_um"])
    beta3_lam = float(summary_rows[0]["beta3_lambda_um"])
    beta5_lam = float(summary_rows[0]["beta5_lambda_um"])
    best_candidates = [row for row in candidate_rows if row["current_status"] == "best_finite_bridge_candidate"]
    direct_closure = next(row for row in candidate_rows if row["candidate_id"] == "SC615_4_direct_mass_closure")
    owner_gap = any(row["current_status"] == "not_passed" for row in acceptance_rows)
    return [
        {"check_id": "V615_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": f"missing={len(missing_sources)}"},
        {"check_id": "V615_1_prior_614_clean", "result": "pass" if not prior_failures else "fail", "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}"},
        {"check_id": "V615_2_vacuum_scale_calculated", "result": "pass" if 50.0 < ell_de < 120.0 else "fail", "detail": f"ell_DE_um={ell_de:.6g}"},
        {"check_id": "V615_3_beta3_to_5_short_band", "result": "pass" if 30.0 <= beta5_lam <= beta3_lam <= 60.0 else "fail", "detail": f"beta5_um={beta5_lam:.6g};beta3_um={beta3_lam:.6g}"},
        {"check_id": "V615_4_best_bridge_not_claimed", "result": "pass" if len(best_candidates) == 2 and no_claim_rows else "fail", "detail": f"best_candidates={len(best_candidates)}"},
        {"check_id": "V615_5_direct_lambda_demoted", "result": "pass" if direct_closure["current_status"] == "closure_only" else "fail", "detail": str(direct_closure["current_status"])},
        {"check_id": "V615_6_parent_owner_gap_retained", "result": "pass" if owner_gap else "fail", "detail": "beta_and_vacuum_bridge_not_parent_signed"},
        {"check_id": "V615_7_no_claim_rows", "result": "pass" if no_claim_rows else "fail", "detail": f"all_valid_for_claim_false={no_claim_rows}"},
        {"check_id": "V615_8_next_target_set", "result": "pass" if decision_rows[0]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V615_9_no_R10_or_local_GR_claim", "result": "pass", "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false"},
    ]


def write_doc(
    generated: str,
    source_register: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    block_rows: list[dict[str, object]],
    acceptance_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 615 Y5 R10 explicit parent X-block short-range origin or range closure

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- Tried the finite short-range derivation instead of just scoring windows.
- Best finite candidate found: a vacuum-scale Hessian bridge, `m_X=sqrt(beta) rho_DE^(1/4)`, giving `lambda_X=ell_DE/sqrt(beta)`.
- With the reference vacuum scale, `ell_DE={summary_rows[0]['ell_DE_um']} um`; beta around `3..5` gives `lambda_X` in the short forgiving band.
- This is promising, not claimed. The parent action still has to derive why local `X` uses the vacuum density scale and why beta is order-few.
- Directly setting `lambda_X=38.6 um` is demoted to closure-only unless that scale is independently derived.

## Source Register
{md_table(source_register)}

## Vacuum Scale Bridge Calculation
{md_table(bridge_rows)}

## Short-Range Origin Candidate Audit
{md_table(candidate_rows)}

## Explicit Parent X-Block Contract
{md_table(block_rows)}

## Acceptance Gates
{md_table(acceptance_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(summary_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is the first finite-range route that feels like it might have a real parent-scale story rather than just "pick the nice lambda." The vacuum density fourth-root naturally lives in the same neighbourhood as short-range gravity bounds, and an order-few Hessian eigenvalue moves it into the 38-50 um band. But it is not yet derived. The next punch is very specific: prove the parent `X` block gets its curvature from the vacuum/cosmology sector with beta fixed by trace, regularity, or a Hessian eigenvalue. If we cannot do that, this route becomes a labelled range closure, not a fundamental prediction.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated = utc_now()
    source_register = build_source_register()
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_614_VALIDATION.csv")
    target_rows = read_csv(OUT / "P8_Y5_R10_578_MASS_GAP_TARGETS.csv")
    summary_613 = read_csv(OUT / "P8_Y5_R10_613_NONCLAIM_SUMMARY.csv")[0]
    epsilon_shell = float(summary_613["epsilon_shell"])
    curve_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv")
    vac = vacuum_scale()

    bridge_rows = build_vacuum_bridge_rows(vac, target_rows)
    candidate_rows = build_scale_candidate_rows(curve_rows, epsilon_shell, vac)
    block_rows = build_parent_block_rows(vac)
    acceptance_rows = build_acceptance_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_update_rows()
    summary_rows = build_summary_rows(vac, candidate_rows)
    validation_rows = build_validation_rows(
        source_register,
        prior_validation,
        bridge_rows,
        candidate_rows,
        block_rows,
        acceptance_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(OUT / "P8_Y5_R10_615_SOURCE_REGISTER.csv", source_register)
    write_csv(OUT / "P8_Y5_R10_615_VACUUM_SCALE_BRIDGE_CALC.csv", bridge_rows)
    write_csv(OUT / "P8_Y5_R10_615_SHORT_RANGE_ORIGIN_CANDIDATE_AUDIT.csv", candidate_rows)
    write_csv(OUT / "P8_Y5_R10_615_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv", block_rows)
    write_csv(OUT / "P8_Y5_R10_615_ACCEPTANCE_GATES.csv", acceptance_rows)
    write_csv(OUT / "P8_Y5_BRR545_615_DECISION.csv", decision_rows)
    write_csv(OUT / "P8_Y5_BRR545_615_ROUTE_UPDATE.csv", route_rows)
    write_csv(OUT / "P8_Y5_R10_615_NONCLAIM_SUMMARY.csv", summary_rows)
    write_csv(OUT / "P8_Y5_BRR545_615_VALIDATION.csv", validation_rows)

    write_doc(
        generated,
        source_register,
        bridge_rows,
        candidate_rows,
        block_rows,
        acceptance_rows,
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
        "validation": rel(OUT / "P8_Y5_BRR545_615_VALIDATION.csv"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
