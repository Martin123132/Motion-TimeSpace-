from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4041-Y5-R2FR-cnorm-common-mode-into-kappa-obs-or-Gdot-bound.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4041_SOURCE_REGISTER.csv",
    "cnorm_split": SOURCE_DIR / "P8_Y5_R2FR_4041_CNORM_SPLIT.csv",
    "kappa_routing": SOURCE_DIR / "P8_Y5_R2FR_4041_KAPPA_OBS_ROUTING.csv",
    "drift_bounds": SOURCE_DIR / "P8_Y5_R2FR_4041_DRIFT_BOUND_TEMPLATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4041_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4041_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4041_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4041_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4041_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4041_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4041_VALIDATION.csv",
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
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4041_0", ROOT / "4040-Y5-R2FR-local-memory-tail-selector-wall-silence-or-cZ-envelope.md", "Remaining live local residuals: `Delta_cZ_envelope`, `c_norm`, `c_nonEH`", "immediate predecessor residual vector"),
        ("SRC4041_1", SOURCE_DIR / "P8_Y5_R2FR_4040_REMAINING_LOCAL_RESIDUAL_VECTOR.csv", "universal source/action normalization drift", "c_norm route from 4040"),
        ("SRC4041_2", SOURCE_DIR / "P8_Y5_R2FR_4030_EH_CHANNEL_ROUTING.csv", "kappa_obs=1/(1/kappa_*+2*c_I*phi_*)", "EH/Newton coupling renormalization"),
        ("SRC4041_3", SOURCE_DIR / "P8_Y5_R2FR_4030_NEWTON_COUPLING_RENORMALIZATION.csv", "D_X ln G_obs=0", "constancy condition and Bianchi guard"),
        ("SRC4041_4", SOURCE_DIR / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv", "d kappa_eff=0", "topological/global constant kappa route"),
        ("SRC4041_5", SOURCE_DIR / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv", "Gdot_over_G", "fallback drift residuals"),
        ("SRC4041_6", SOURCE_DIR / "P8_Y5_source_normalization_renormalized_G_status.csv", "constant universal source calibration is absorbable into G_N", "prior renormalized-G result"),
        ("SRC4041_7", SOURCE_DIR / "P8_Y5_source_normalization_derivative_hair_status.csv", "DERIVATIVE_HAIR_BOUND_RUNNER_NONCLAIM_READY", "derivative hair remains finite-channel"),
        ("SRC4041_8", SOURCE_DIR / "P8_Y5_R2FR_3636_JX_NORMALIZATION_GATE.csv", "D_a ln mu_obs = D_a ln G_eff + D_a ln M_eff + D_a ln(1+epsilon_mu)", "source-normalization derivative decomposition"),
        ("SRC4041_9", SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "M_eff(S2)-M_eff(S1)", "M_eff flux closure condition"),
        ("SRC4041_10", SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv", "dln_Meff_dt", "M_eff residual map"),
        ("SRC4041_11", SOURCE_DIR / "P8_Y5_Gauss_orbital_calibration_status.csv", "constant-G_eff / radial-time-hair gate", "Newton/Gauss/orbital calibration warning"),
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


def cnorm_split_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "split_id": "CN4041_0_common_constant",
            "piece": "common constant source/action normalization",
            "formula": "G_obs=c^4*kappa_obs/(8*pi), kappa_obs=1/(1/kappa_*+2*c_I*phi_*)",
            "selected_branch_result": "calibrates the local Newton coupling; not a fifth-force/source-hair residual",
            "status": "ROUTED_TO_OBSERVED_G_CALIBRATION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "split_id": "CN4041_1_G_derivative",
            "piece": "time/radial/range/frame/source derivative of G_obs",
            "formula": "D_a ln G_obs = -D_a ln(1/kappa_*+2*c_I*phi_*)",
            "selected_branch_result": "zero only if kappa_* and phi_* are fixed/global and delta_phi/Delta_cZ do not induce local hair",
            "status": "ZERO_CONDITIONAL_ELSE_GDOT_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "split_id": "CN4041_2_Meff_derivative",
            "piece": "projected source mass/charge drift",
            "formula": "D_a ln M_eff from d(Pi_M J_H) and source-measure flux",
            "selected_branch_result": "retained unless Pi_M/H_tau/H_ref/worldtube source current closes",
            "status": "MEFF_FLUX_RESIDUAL_RETAINED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "split_id": "CN4041_3_epsilon_mu",
            "piece": "extra/source-frame/projector/species normalization",
            "formula": "D_a ln(1+epsilon_mu)",
            "selected_branch_result": "retained as source-normalization envelope unless same-frame/source-universality and extra-sector silence close",
            "status": "SOURCE_NORMALIZATION_HAIR_RETAINED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "split_id": "CN4041_4_total",
            "piece": "total c_norm residual",
            "formula": "Delta_source_norm = D_a ln mu_obs = D_a ln G_obs + D_a ln M_eff + D_a ln(1+epsilon_mu)",
            "selected_branch_result": "constant common mode is routed away; derivative/source/range/frame/species hair is carried as an absolute envelope",
            "status": "CNORM_REDUCED_TO_DERIVATIVE_HAIR_ENVELOPE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def kappa_routing_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "route_id": "KR4041_0_EH_calibration",
            "route": "constant common mode into observed EH/Newton coupling",
            "formula": "I_EH+I_imp=int sqrt|g|[(1/(2*kappa_*))+c_I*phi_*]R + residual(delta_phi)",
            "condition": "phi_* and kappa_* are fixed/global local-branch constants",
            "result": "G_obs is calibrated once, exactly like GR calibrates Newton's constant",
            "status": "CALIBRATION_ROUTE_ACCEPTED_INTERNAL",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "route_id": "KR4041_1_topological_kappa",
            "route": "derive local constancy of kappa by topological zero-form/three-form sector",
            "formula": "S_kappa_top=int kappa_eff dA_3; delta_A S => d kappa_eff=0",
            "condition": "topological kappa sector is part of the selected local branch packet",
            "result": "D_local kappa_eff=0 on connected local domains",
            "status": "LOCAL_BRANCH_KAPPA_CONSTANCY_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "route_id": "KR4041_2_Bianchi_guard",
            "route": "spacetime-varying coupling is physical",
            "formula": "nabla_mu[(1/kappa_eff)G^{mu nu}]=0 forces exchange terms if nabla kappa_eff != 0",
            "condition": "any nonconstant G_eff branch",
            "result": "nonconstant c_norm cannot be hidden in calibration; it must be bounded",
            "status": "BIANCHI_DRIFT_GUARD_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "route_id": "KR4041_3_Meff_gate",
            "route": "observed GM still needs source-measure flux closure",
            "formula": "M_eff(S2)-M_eff(S1)=int_A d(Pi_M J_H)",
            "condition": "Pi_M/H_tau/source current is parent-owned and closed outside source support",
            "result": "constant G alone is not enough for Newton; M_eff drift remains a separate envelope",
            "status": "MEFF_GATE_RETAINED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def drift_bound_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "DB4041_0_Gdot",
            "symbol": "D_t ln G_obs",
            "used_if": "kappa/phi fixed-sector constancy or delta_phi silence fails",
            "bound_target": "|Gdot/G| <= 9.6e-15 yr^-1 or updated arena lock",
            "formula": "D_t ln G_obs = -D_t ln(1/kappa_*+2*c_I*phi_*)",
            "missing_inputs": "D_t kappa_*,D_t phi_*,delta_phi time hair,source path",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "DB4041_1_radial",
            "symbol": "partial_r ln mu_obs",
            "used_if": "radial source strength varies outside compact support",
            "bound_target": "radial hair below PPN/R10/orbital locks",
            "formula": "partial_r ln mu_obs=partial_r ln G_obs+partial_r ln M_eff+partial_r ln(1+epsilon_mu)",
            "missing_inputs": "radial profiles for G_obs,M_eff,epsilon_mu and arena projection",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "DB4041_2_range",
            "symbol": "alpha_norm(lambda)",
            "used_if": "source normalization has finite-range dependence",
            "bound_target": "R10 alpha(lambda) below inverse-square bound curve",
            "formula": "alpha_norm(lambda)=projection[D_lambda ln mu_obs]",
            "missing_inputs": "lambda grid,alpha_bound(lambda),projection normalization,source curve",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "DB4041_3_species",
            "symbol": "eta_source_AB",
            "used_if": "source normalization depends on species/material/source labels",
            "bound_target": "eta_source_AB <= 2.8e-15 or derived source universality",
            "formula": "eta_source_AB ~ D_A ln mu_obs - D_B ln mu_obs",
            "missing_inputs": "material/source derivatives,composition map,bound source",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "DB4041_4_total",
            "symbol": "Delta_cnorm_envelope",
            "used_if": "any derivative/source/range/frame/domain component remains",
            "bound_target": "absolute no-cancellation envelope below all mapped local locks",
            "formula": "|Delta_cnorm| <= |D ln G_obs|+|D ln M_eff|+|D ln(1+epsilon_mu)|",
            "missing_inputs": "all component derivative bounds and arena projections",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4041_0_cZ",
            "symbol": "Delta_cZ_envelope",
            "residual": "absolute c_Z tail/wall envelope from 4040",
            "current_route": "carried until kernel/selector inputs are filled or zero-proven",
            "priority": "carried",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4041_1_cnorm",
            "symbol": "Delta_cnorm_envelope",
            "residual": "nonconstant source-normalization derivative hair",
            "current_route": "fill Gdot/radial/range/species/frame/source-measure derivative rows or derive all zero",
            "priority": "carried_but_sharp",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4041_2_nonEH",
            "symbol": "c_nonEH",
            "residual": "non-EH or higher-curvature metric operator leakage",
            "current_route": "show decoupling at local scale or compare to PPN/Cassini-style bounds",
            "priority": "next",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4041_0_selected_constant_common_mode",
            "verdict": "COMMON_MODE_ROUTED_TO_KAPPA_OBS_DERIVATIVE_HAIR_RETAINED",
            "result": "constant common c_norm is calibration into G_obs; nonconstant drift/range/source hair is an absolute envelope",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4041",
            "next_action": "carry Delta_cnorm_envelope and attack c_nonEH/operator residual",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4041_1_if_constancy_fails",
            "verdict": "GDOT_SOURCE_NORMALIZATION_BOUND_BRANCH_REQUIRED",
            "result": "nonconstant G_eff or M_eff becomes Gdot/radial/R10/WEP/source-frame residual",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4041",
            "next_action": "fill drift/range/species rows before any local test score",
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4041_0_calibration",
            "decision": "Route the constant universal source-normalization/common-mode into observed kappa_obs/G_obs.",
            "status": "COMMON_MODE_CALIBRATION_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4041_1_derivative_hair",
            "decision": "Do not route derivative/time/radial/range/species/frame/source drift into calibration.",
            "status": "DERIVATIVE_HAIR_RETAINED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4041_2_newton_guard",
            "decision": "Constant G_obs does not by itself prove Newtonian mechanics; M_eff/Gauss/orbital calibration and nonEH source operator remain open.",
            "status": "NEWTON_PROMOTION_GUARD_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4041_3_next",
            "decision": "Move to 4042-Y5-R2FR-nonEH-operator-decoupling-or-PPN-bound-vector.md.",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4041_0_common_mode",
            "claim": "constant common-mode normalization routes into G_obs",
            "allowed": True,
            "scope": "internal selected local branch calibration stance",
            "reason": "EH/Newton coefficient relation and topological kappa constancy route",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4041_1_full_cnorm_zero",
            "claim": "full c_norm zero",
            "allowed": False,
            "scope": "all source-normalization effects",
            "reason": "derivative/source/range/frame/Meff hair remains",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4041_2_newton",
            "claim": "Newtonian mechanics/local GR pass",
            "allowed": False,
            "scope": "full local weak-field phenomenology",
            "reason": "M_eff flux, Gauss/orbital calibration, Delta_cZ, Delta_cnorm, and c_nonEH remain open",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4041_0",
            "next_doc": "4042-Y5-R2FR-nonEH-operator-decoupling-or-PPN-bound-vector.md",
            "next_script": "scripts/Y5_R2FR_4042_nonEH_operator_decoupling_or_PPN_bound_vector.py",
            "why": "c_norm is now split into calibrated common mode plus derivative envelope; the last structural local-GR leak in the 4034 vector is c_nonEH/operator/PPN leakage.",
            "fallback": "if nonEH decoupling fails, build PPN/Cassini/R10 operator residual bound vector with no cancellation credit",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STATUS4041_0",
            "checkpoint": "4041",
            "canonical_status": "CNORM_COMMON_MODE_ROUTED_DERIVATIVE_ENVELOPE_ACTIVE",
            "strongest_result": "constant universal normalization is not a force residual; it routes into calibrated G_obs, while derivative/source/range/frame hair remains explicit.",
            "still_missing": "Gdot/radial/range/species/frame/Meff derivative inputs or zero theorems; c_nonEH/PPN operator closure",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    total = len(sources)
    return f"""# 4041 - c_norm Common Mode Into kappa_obs Or Gdot Bound

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{found}/{total}`.

## What Actually Moved

4041 splits `c_norm` into the part that is just calibration and the part that is real physics.

The constant/common mode routes into the observed Newton coupling:

`G_obs=c^4*kappa_obs/(8*pi)`, with `kappa_obs=1/(1/kappa_*+2*c_I*phi_*)`.

That is not a fifth-force/source-hair residual. It is the same kind of calibrated coupling role that Newton's constant plays in GR.

## What Does Not Get Hidden

Any nonconstant piece is physical:

`Delta_source_norm = D_a ln mu_obs = D_a ln G_obs + D_a ln M_eff + D_a ln(1+epsilon_mu)`.

So time drift, radial hair, range dependence, species/source dependence, frame/domain dependence, and `M_eff` flux drift remain explicit.

## Bound Interface

If the fixed/global sector route fails:

- `D_t ln G_obs` maps to `Gdot/G`;
- `partial_r ln mu_obs` maps to radial source hair / PPN / orbital residuals;
- `alpha_norm(lambda)` maps to R10 inverse-square tests;
- `eta_source_AB` maps to source/WEP composition locks;
- `Delta_cnorm_envelope` is the no-cancellation sum of the remaining derivative pieces.

## Current Verdict

- Current evaluator result: `COMMON_MODE_ROUTED_TO_KAPPA_OBS_DERIVATIVE_HAIR_RETAINED`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4041`.
- Remaining live local residuals: `Delta_cZ_envelope`, `Delta_cnorm_envelope`, `c_nonEH`.

## Next Target

- `4042-Y5-R2FR-nonEH-operator-decoupling-or-PPN-bound-vector.md`
- `scripts/Y5_R2FR_4042_nonEH_operator_decoupling_or_PPN_bound_vector.py`
"""


def validation_rows(
    ts: str,
    sources: List[Dict[str, object]],
    split: List[Dict[str, object]],
    routing: List[Dict[str, object]],
    bounds: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
        return {"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts}

    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH), str(SCRIPT_PATH)]
    return [
        row("VAL4041_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4041_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4041_02_common_split", any(item["split_id"] == "CN4041_0_common_constant" for item in split), "common constant split present"),
        row("VAL4041_03_derivative_split", any(item["split_id"] == "CN4041_1_G_derivative" for item in split), "G derivative split present"),
        row("VAL4041_04_Meff_split", any(item["split_id"] == "CN4041_2_Meff_derivative" for item in split), "M_eff split present"),
        row("VAL4041_05_total_split", any(item["split_id"] == "CN4041_4_total" for item in split), "total c_norm split present"),
        row("VAL4041_06_EH_route", any(item["route_id"] == "KR4041_0_EH_calibration" for item in routing), "EH calibration route present"),
        row("VAL4041_07_kappa_route", any(item["route_id"] == "KR4041_1_topological_kappa" for item in routing), "topological kappa route present"),
        row("VAL4041_08_Bianchi_guard", any(item["route_id"] == "KR4041_2_Bianchi_guard" for item in routing), "Bianchi guard present"),
        row("VAL4041_09_Meff_gate", any(item["route_id"] == "KR4041_3_Meff_gate" for item in routing), "M_eff gate present"),
        row("VAL4041_10_Gdot_bound", any(item["bound_id"] == "DB4041_0_Gdot" for item in bounds), "Gdot bound present"),
        row("VAL4041_11_radial_bound", any(item["bound_id"] == "DB4041_1_radial" for item in bounds), "radial bound present"),
        row("VAL4041_12_range_bound", any(item["bound_id"] == "DB4041_2_range" for item in bounds), "range bound present"),
        row("VAL4041_13_species_bound", any(item["bound_id"] == "DB4041_3_species" for item in bounds), "species/source bound present"),
        row("VAL4041_14_total_envelope", any(item["bound_id"] == "DB4041_4_total" for item in bounds), "total c_norm envelope present"),
        row("VAL4041_15_bound_nonclaim", all(item["valid_for_public_claim"] is False for item in bounds), "bounds remain nonclaim"),
        row("VAL4041_16_remaining_cZ", any(item["symbol"] == "Delta_cZ_envelope" for item in remaining), "c_Z envelope carried"),
        row("VAL4041_17_remaining_cnorm", any(item["symbol"] == "Delta_cnorm_envelope" for item in remaining), "c_norm envelope carried"),
        row("VAL4041_18_remaining_nonEH", any(item["symbol"] == "c_nonEH" for item in remaining), "c_nonEH next"),
        row("VAL4041_19_current_verdict", any(item["case_id"] == "CASE4041_0_selected_constant_common_mode" for item in evaluator), "current evaluator present"),
        row("VAL4041_20_no_full_cnorm_claim", any(item["claim_id"] == "CLAIM4041_1_full_cnorm_zero" and item["allowed"] is False for item in claims), "full c_norm zero not claimed"),
        row("VAL4041_21_common_claim_scoped", any(item["claim_id"] == "CLAIM4041_0_common_mode" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "common-mode claim scoped internal"),
        row("VAL4041_22_no_public_local_claim", all(item["public_claim_allowed"] is False for item in claims), "no public claims allowed"),
        row("VAL4041_23_next_decision", any(item["decision_id"] == "DEC4041_3_next" for item in decisions), "4042 next decision present"),
        row("VAL4041_24_next_target", bool(next_target and "4042" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4041_25_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4041_26_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4041_27_script_compiles", compile_ok, "script compiles"),
        row("VAL4041_28_private_guard", all(item["valid_for_public_claim"] is False for table in [split, routing, bounds, remaining, decisions] for item in table), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    split = cnorm_split_rows(ts)
    routing = kappa_routing_rows(ts)
    bounds = drift_bound_rows(ts)
    remaining = remaining_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["cnorm_split"], split)
    write_csv(OUTPUTS["kappa_routing"], routing)
    write_csv(OUTPUTS["drift_bounds"], bounds)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["evaluator"], evaluator)
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

    checks = validation_rows(ts, sources, split, routing, bounds, remaining, evaluator, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4041 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
