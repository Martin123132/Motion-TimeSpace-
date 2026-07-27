from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3573-Y5-R2FR-PiM-flux-closure-Ward-Euler-or-Meff-drift-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PIM_FLUX_CLOSURE_3573"
CHECKPOINT_ID = "3573"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3572": RESIDUALS / "P8_Y5_R2FR_3572_NEXT_TARGET.csv",
        "projector_proof_3572": RESIDUALS / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
        "projector_bounds_3572": RESIDUALS / "P8_Y5_R2FR_3572_KPROJECTOR_OPERATOR_NORM_ROWS.csv",
        "selector_update_3572": RESIDUALS / "P8_Y5_R2FR_3572_BLC_SELECTOR_UPDATE.csv",
        "status_3572": RESIDUALS / "P8_Y5_R2FR_3572_STATUS.csv",
        "pim_flux": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "mass_flux": RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "charge_residuals": RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "charge_attempt": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "pg_gate": RESIDUALS / "P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv",
        "constant_gm_zero": RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "constant_gm_derivative": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "pg_map": RESIDUALS / "P8_PG_calibration_residual_MAP.csv",
        "ham_pim_validation": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_READOUT_VALIDATION.csv",
        "pim_htau_commutator": RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3572": "declares 3573 target",
        "projector_proof_3572": "imports closed delta_Gamma Pi_M result",
        "projector_bounds_3572": "imports d(Pi_M J_H) as next flux target",
        "selector_update_3572": "imports selector update after projector Gamma closure",
        "status_3572": "imports remaining source-calibration blockers",
        "pim_flux": "imports Ward/topological flux closure contract",
        "mass_flux": "imports Euler/calibration mass-flux contract",
        "charge_residuals": "imports charge-current residual decomposition",
        "charge_attempt": "imports direct charge-current equality attempt",
        "pg_gate": "imports Poisson/Gauss derive-or-fill rows",
        "constant_gm_zero": "imports constant GM theorem attempt",
        "constant_gm_derivative": "imports derivative hair identity",
        "pg_map": "imports calibration residual map",
        "ham_pim_validation": "imports no-overclaim validation for Hamiltonian/PiM route",
        "pim_htau_commutator": "imports PiM/Htau residual components",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def closure_fork_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "FLUX3573_0_target",
            "mass flux closure target",
            "J_M := Pi_M J_H must be a parent-owned mass-channel current and satisfy dJ_M=d(Pi_M J_H)=0 in the compact local exterior.",
            "Without this, M_eff can drift with time/radius and Newtonian measured-GM calibration is not derived.",
            "TARGET_DEFINED",
            "pim_flux",
        ),
        (
            "FLUX3573_1_ward_route",
            "Ward/Killing route",
            "If the local exterior supplies an observed stationary/asymptotic time generator xi and J_M^mu=T_H^{mu nu}xi_nu, then nabla_mu T_H^{mu nu}=0 plus L_xi g_obs=0 gives dJ_M=0.",
            "Ward conservation alone is not enough; the mass generator xi and same-frame source current must be parent-owned.",
            "EXACT_IF_STATIONARY_HAMILTONIAN_OWNER_SIGNED",
            "pim_flux",
        ),
        (
            "FLUX3573_2_topological_route",
            "topological mass-current route",
            "If a parent topological/closed-form mass current J_M^top exists and equals Pi_M J_H on shell, then d(Pi_M J_H)=dJ_M^top=0.",
            "This is the clean non-ad-hoc route, but the corpus only marks it promising, not derived.",
            "PROMISING_NOT_IN_CORPUS",
            "pim_flux",
        ),
        (
            "FLUX3573_3_euler_route",
            "Euler constraint route",
            "If a parent-owned lambda_M or equivalent source-normalization equation has an independent gauge/topological/Ward origin, its Euler equation may impose d(Pi_M J_H)=0.",
            "A multiplier added solely to force GM success is not allowed.",
            "EXACT_IF_NO_AD_HOC_MULTIPLIER_PROVED",
            "mass_flux",
        ),
        (
            "FLUX3573_4_flux_difference_law",
            "annulus flux law",
            "M_eff(S_2)-M_eff(S_1)=int_{S2xI} d(Pi_M J_H).",
            "This converts failed closure into radial source hair or time drift instead of a hidden calibration offset.",
            "DERIVED_STOKES_BOUND_BACKBONE",
            "mass_flux",
        ),
        (
            "FLUX3573_5_measured_GM_warning",
            "closed current is not yet Newton",
            "Even if d(Pi_M J_H)=0, Newton needs M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H and mu_obs=G_ref M_eff with constant G_ref and no mu_extra.",
            "Flux closure is first-order source conservation; measured-GM and local-GR promotion require extra gates.",
            "SCOPE_GUARD",
            "charge_attempt",
        ),
        (
            "FLUX3573_6_verdict",
            "3573 verdict",
            "The exact closure routes are now written, but none are parent-derived in the current corpus; dln_Meff_dt and partial_r_ln_mu_obs stay retained as executable source-normalization residuals.",
            "This is not defeat: it is the first clean Newton-source drift fork after the projector Gamma commutator was closed.",
            "CLOSURE_NOT_CLAIMED_BOUND_ROWS_ACTIVE",
            "status_3572",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "fork_id": fork_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for fork_id, claim_piece, statement, derivation, status, source_key in specs
    ]


def residual_bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DRIFT3573_0_dlnMeff_dt",
            "dln_Meff_dt",
            "dln_Meff_dt := (1/M_eff) dM_eff/dt, with M_eff=int_S Pi_M J_H",
            "yr^-1 or s^-1 after declared time unit",
            "zero iff d(Pi_M J_H)=0 over time slabs and no boundary/reference flux",
            "MISSING_THEOREM_OR_NUMERIC_VALUE",
            "pg_gate",
            "Gdot/local GM drift",
        ),
        (
            "DRIFT3573_1_partial_r_ln_mu_obs",
            "partial_r_ln_mu_obs",
            "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_mu)",
            "m^-1, AU^-1, or dimensionless per declared radial interval",
            "zero iff no radial G_eff, no radial M_eff flux, and no radial mu_extra/range hair",
            "MISSING_THEOREM_OR_PROFILE",
            "constant_gm_derivative",
            "inverse-square Newton/radial source hair",
        ),
        (
            "DRIFT3573_2_Delta_flux",
            "Delta_flux",
            "Delta_flux := abs(int_annulus d(Pi_M J_H)) / abs(M_eff)",
            "dimensionless",
            "controls radial/time mass-flux failure directly",
            "FORMULA_READY_INPUT_INTEGRAL_MISSING",
            "charge_residuals",
            "Meff conservation; radial source hair",
        ),
        (
            "DRIFT3573_3_Delta_cal",
            "Delta_cal",
            "Delta_cal := M_eff[Pi_M J_H] - M_Gauss_orbital",
            "mass or dimensionless after division by M_eff",
            "closed flux can still be miscalibrated to measured Newtonian GM",
            "CALIBRATION_GATE_OPEN",
            "pg_map",
            "Poisson/Gauss/orbital source calibration",
        ),
        (
            "DRIFT3573_4_mu_extra",
            "mu_extra_boundary_bulk_domain",
            "epsilon_mu := mu_extra/(G_eff M_eff); mu_obs=G_eff M_eff(1+epsilon_mu)",
            "dimensionless",
            "non-Hilbert/boundary/domain/memory/source hair must be zero or bounded",
            "CENTRAL_MU_EXTRA_VECTOR_UNFILLED",
            "constant_gm_zero",
            "Newton source normalization; local GR",
        ),
        (
            "DRIFT3573_5_dlnGeff_dt",
            "dln_Geff_dt",
            "dln mu_obs/dt = dln_Geff_dt + dln_Meff_dt + dln(1+epsilon_mu)/dt",
            "yr^-1 or s^-1",
            "constant universal coupling is a separate required theorem",
            "SEPARATE_COUPLING_SUPERSELECTION_OPEN",
            "constant_gm_derivative",
            "Gdot/source coupling drift",
        ),
        (
            "DRIFT3573_6_alpha_lambda",
            "alpha(lambda)",
            "finite-range residual curve if no radial/range no-hair theorem exists",
            "dimensionless alpha at length lambda",
            "range dependence cannot be absorbed into one fitted GM",
            "R10_CURVE_OR_NO_RANGE_THEOREM_MISSING",
            "pg_gate",
            "R10/fifth-force/Newton inverse-square",
        ),
        (
            "DRIFT3573_7_total_source_drift",
            "D_X_ln_mu_obs",
            "D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)",
            "channel-specific derivative units",
            "no cancellation credit unless a parent identity supplies it",
            "EXECUTABLE_IDENTITY_NONCLAIM",
            "constant_gm_derivative",
            "global source-normalization scorecard",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "zero_or_bound_condition": condition,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "observable_link": observable,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for residual_id, symbol, formula, units, condition, status, source_key, observable in specs
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3573_0_sources", "source audit", "PASS", "all required 3573 source paths exist"),
        ("GATE3573_1_closure_identity", "flux difference law", "PASS_FORMULA", "Stokes/annulus law converts closure failure into residual rows"),
        ("GATE3573_2_ward_route", "Ward/Killing closure", "FAIL_CURRENT_CLAIM", "stationary/Hamiltonian mass generator and same-frame current not parent-derived"),
        ("GATE3573_3_topological_route", "topological mass current", "FAIL_CURRENT_CLAIM", "promising route exists but no parent current equal to Pi_M J_H is in corpus"),
        ("GATE3573_4_euler_route", "Euler lambda_M closure", "FAIL_CURRENT_CLAIM", "no non-ad-hoc multiplier/source-normalization Euler origin"),
        ("GATE3573_5_drift_rows", "Meff/radial residual rows", "PASS_NONCLAIM", "dln_Meff_dt and partial_r_ln_mu_obs rows generated with units and source links"),
        ("GATE3573_6_Newton_claim", "source-normalized Newton", "FAIL_CURRENT_CLAIM", "closed calibrated mass flux and measured-GM equality remain open"),
        ("GATE3573_7_local_GR_claim", "local GR", "FAIL_CURRENT_CLAIM", "second-order PPN/source stability deferred until first-order source rows close"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["status_3572"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3573_0_no_Ward_shortcut",
            "do not count Ward conservation alone as d(Pi_M J_H)=0",
            "Ward needs a parent-owned mass generator/current and no exchange/boundary projection leakage.",
            "prevents smuggling Newton source conservation from general covariance alone",
            "ADOPTED",
            "pim_flux",
        ),
        (
            "DEC3573_1_drift_rows_live",
            "retain dln_Meff_dt and partial_r_ln_mu_obs as first-class rows",
            "If mass flux is not closed, the failure is observable as Gdot/radial source hair/inverse-square leakage.",
            "keeps testing path alive instead of burying source calibration in fitted GM",
            "ADOPTED_NONCLAIM",
            "pg_gate",
        ),
        (
            "DEC3573_2_next_target",
            "try topological mass-current origin next",
            "FC5 is the cleanest non-ad-hoc route: define a closed absolute mass current and prove it equals Pi_M J_H on shell.",
            "3574 should construct or reject J_M^top=Pi_M J_H; if rejected, fill dln_Meff_dt/radial source rows numerically or from bounds",
            "NEXT_TARGET_SELECTED",
            "pim_flux",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "PIM_FLUX_CLOSURE_FORK_DERIVED_MEFF_DRIFT_ROWS_ACTIVE",
            "strongest_result": "M_eff(S2)-M_eff(S1)=int_annulus d(Pi_M J_H) and dln_Meff_dt/partial_r_ln_mu_obs residual rows are explicit; Ward/topological/Euler closure routes are named but not parent-derived.",
            "still_missing": "observed time/Hamiltonian mass generator, topological mass current equal to Pi_M J_H, non-ad-hoc Euler closure, no exchange/boundary flux, constant G_eff and measured-GM calibration",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3573_0",
            "target_doc": "3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md",
            "target_script": "scripts/Y5_R2FR_3574_topological_mass_current_origin_or_Meff_drift_source_row.py",
            "objective": "try to construct a parent-owned closed topological mass current J_M^top and prove J_M^top=Pi_M J_H on shell; if not, source the dln_Meff_dt/partial_r residual rows",
            "success_gate": "closed non-ad-hoc mass current equal to projected Hilbert source, or source-backed drift/radial residual inputs",
            "reason": "3573 shows Ward/Euler closure is not claimable without a parent-owned mass current",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "PiM_mass_flux_closure_or_Meff_drift",
            "status": "CLOSURE_NOT_CLAIMED_DRIFT_ROWS_ACTIVE",
            "closure_formula": "M_eff(S2)-M_eff(S1)=int_annulus d(Pi_M J_H)",
            "drift_formula": "D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)",
            "next_action": "construct topological mass current or source drift/radial residuals",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    closure: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3573_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3573 source paths exist"))
    needles = {
        "handoff_3572": "NEXT3572_0",
        "projector_proof_3572": "PN3572_6_result",
        "projector_bounds_3572": "KPROJ3572_3_flux",
        "selector_update_3572": "UPD3572_2_flux_closure",
        "status_3572": "d(Pi_M J_H)=0",
        "pim_flux": "FC2_closed_mass_current_equation",
        "mass_flux": "MF2_Euler_flux_closure",
        "charge_residuals": "Delta_flux",
        "charge_attempt": "CC7_closed_flux_and_Gauss_calibration",
        "pg_gate": "P8_Meff_conservation",
        "constant_gm_zero": "Z2_calibrated_PiM_flux_conservation",
        "constant_gm_derivative": "CGM1_time_drift",
        "pg_map": "PG4_Gauss_surface_integral",
        "ham_pim_validation": "V540_7_no_overclaim",
        "pim_htau_commutator": "PHCR3514_0_total",
    }
    validations.append(("VAL3573_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected mass-flux source needles found"))
    validations.append(("VAL3573_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3573 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3573_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3573_4_flux_law_present", any(row["fork_id"] == "FLUX3573_4_flux_difference_law" and "int_{S2xI}" in str(row["statement"]) for row in closure), "annulus flux law present"))
    validations.append(("VAL3573_5_ward_euler_routes_present", {"FLUX3573_1_ward_route", "FLUX3573_2_topological_route", "FLUX3573_3_euler_route"}.issubset({str(row["fork_id"]) for row in closure}), "Ward/topological/Euler closure routes present"))
    validations.append(("VAL3573_6_drift_rows_present", {"dln_Meff_dt", "partial_r_ln_mu_obs", "Delta_flux"}.issubset({str(row["symbol"]) for row in residuals}), "Meff drift/radial/flux residual rows present"))
    validations.append(("VAL3573_7_Newton_claim_blocked", any(row["gate_id"] == "GATE3573_6_Newton_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "Newton claim remains blocked"))
    validations.append(("VAL3573_8_next_topological_target_selected", any(row["decision_id"] == "DEC3573_2_next_target" for row in decisions), "topological mass-current target selected"))
    validations.append(("VAL3573_9_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in closure + residuals + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in closure + residuals + gates + decisions)
    validations.append(("VAL3573_10_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3573*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3573_11_formalization_workbench_untouched", not formalization_touched, "no 3573 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    closure: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3573 - PiM flux closure: Ward/Euler or Meff drift bound",
        "",
        "## Verdict",
        "3573 writes the Newton-source fork cleanly.  The required closure is `d(Pi_M J_H)=0`, equivalently `M_eff(S2)-M_eff(S1)=int_annulus d(Pi_M J_H)`.  Ward conservation, a topological current, or an Euler constraint could close it, but none is parent-derived yet.",
        "",
        "So Newton/source calibration is not claimed.  The fallback rows are now explicit: `dln_Meff_dt`, `partial_r_ln_mu_obs`, `Delta_flux`, `Delta_cal`, `mu_extra`, `dln_Geff_dt`, and `alpha(lambda)`.  This prevents fitted-G sleight of hand: if flux closure fails, it becomes Gdot/radial/fifth-force/source-hair data.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Closure fork"])
    for row in closure:
        lines.append(f"- `{row['fork_id']}`: {row['statement']} ({row['status']})")
    lines.extend(["", "## Drift and radial rows"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Activation gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    closure = closure_fork_rows(source_paths)
    residuals = residual_bound_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3573_SOURCE_REGISTER.csv",
        "closure_fork": RESIDUALS / "P8_Y5_R2FR_3573_PIM_FLUX_CLOSURE_FORK.csv",
        "drift_bound_rows": RESIDUALS / "P8_Y5_R2FR_3573_MEFF_DRIFT_RADIAL_BOUND_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3573_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3573_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3573_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3573_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_PiM_flux_closure_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3573_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["closure_fork"], closure)
    write_csv(outputs["drift_bound_rows"], residuals)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, closure, residuals, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, closure, residuals, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3573 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
