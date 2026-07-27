from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3652"
BRANCH_ID = "MTS_R2FR_Y5_WEAK_FIELD_SOURCE_HAMILTONIAN_GM_CALIBRATION_OR_SOURCE_VECTOR_BOUND_3652"
DOC = ROOT / "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_register(ts: str) -> list[dict[str, object]]:
    bounds = LOCAL_BOUNDS / "local_bound_claims.csv"
    specs = [
        ("next_3651", RESIDUALS / "P8_Y5_R2FR_3651_NEXT_TARGET.csv", "weak-field-source-Hamiltonian", "3651 selected weak-field source Hamiltonian next"),
        ("doc_3651", ROOT / "3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md", "WEAK_FIELD_SOURCE_HAMILTONIAN_NEXT", "3651 source Hamiltonian decision"),
        ("sens_3651", RESIDUALS / "P8_Y5_R2FR_3651_MATERIAL_SENSITIVITY_ROWS.csv", "q_matter_source_abs", "3651 matter/source envelope"),
        ("proj_3651", RESIDUALS / "P8_Y5_R2FR_3651_PROJECTION_ROWS.csv", "PPN_source_calibration", "3651 PPN/orbital projections"),
        ("theorem_3651", RESIDUALS / "P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv", "delta(GM)_obs/(GM)", "3651 fitted-GM guard"),
        ("bounds_R1_WEP", bounds, "R1_WEP_source_charge", "WEP source-charge anchor"),
        ("bounds_R3_gamma", bounds, "R3_gamma", "PPN gamma anchor"),
        ("bounds_R4_beta", bounds, "R4_beta", "PPN beta anchor"),
        ("bounds_R9_Gdot", bounds, "R9_Gdot", "Gdot/LLR orbital-source anchor"),
        ("bounds_R10", bounds, "R10_fifth_force", "R10 inverse-square/fifth-force anchor"),
        ("matrix_1048", RESIDUALS / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv", "BM1048_4_PPN_source", "1048 PPN source-calibration matrix row"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def theorem_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "theorem_id": "WFH3652_0_parent_source_Hamiltonian",
            "claim": "Newtonian source mass is owned when the weak-field Hamiltonian descends from the same parent matter action.",
            "mathematical_form": "H_S = M_S^eff(q,theta_rep)c^2 + p^2/(2M_S^eff) + M_S^eff Phi_obs + O(v^4/c^4), with M_S^eff not an independent X_N marker.",
            "derivation_step": "Expanding the same quotient-owned matter action in v/c gives inertial mass, active gravitational source, and clock/source readout from one object.",
            "result": "If the parent action signs this, fitted GM is not a separate source-coupling knob.",
            "status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent-signed weak-field source Hamiltonian and source-measure descent",
        },
        {
            **base(ts),
            "theorem_id": "WFH3652_1_GM_calibration_law",
            "claim": "Fitted GM is a calibration product, not a proof of local GR by itself.",
            "mathematical_form": "mu_obs=(GM)_fit = G_obs M_S^eff[1+q_metric+q_readout+q_boundary+q_source]; delta ln mu_obs = delta ln G_obs + delta ln M_S^eff + q_metric + q_readout + q_boundary + q_source.",
            "derivation_step": "Kepler/orbital dynamics measure the product mu=GM. Without the source Hamiltonian owner, a quiet orbit can absorb source calibration into fitted GM.",
            "result": "Newtonian recovery must prove or bound the source-calibration vector, not only match orbits.",
            "status": "GM_DEGENERACY_LAW_DERIVED",
            "missing_for_claim": "separate source mass, G_obs, metric/readout, and boundary residual ownership",
        },
        {
            **base(ts),
            "theorem_id": "WFH3652_2_Poisson_source_law",
            "claim": "The Newtonian Poisson source closes only if active and inertial source mass are the same quotient-owned density.",
            "mathematical_form": "nabla^2 Phi_N = 4*pi*G_obs*rho_active + S_metric + S_boundary; rho_active=rho_inertial[1+q_source_mass+q_matter_source_abs].",
            "derivation_step": "The 00 weak-field equation sees active stress-energy. Matter/source residuals re-enter as a source-density mismatch if not parent-owned.",
            "result": "The Newtonian limit requires rho_active=rho_inertial and residual source terms theorem-zero or bounded.",
            "status": "POISSON_SOURCE_CONDITION_DERIVED",
            "missing_for_claim": "active/inertial source identity and boundary silence",
        },
        {
            **base(ts),
            "theorem_id": "WFH3652_3_fifth_force_projection",
            "claim": "The same source charge produces the Yukawa/R10 branch.",
            "mathematical_form": "Z_X(nabla^2-lambda_X^-2)deltaX = -K_X rho_S Q_S^X; V_X(r)=-G_obs m_S m_T alpha_ST exp(-r/lambda_X)/r; alpha_ST=K_X Q_S^X Q_T^X/(4*pi*Z_X*G_obs).",
            "derivation_step": "A nonzero Q_S^X sources the local residual field. R10 tests and WEP/source-charge tests are projections of this same Hamiltonian source.",
            "result": "R10 cannot be scored until K_X, Z_X, lambda_X, Q_S^X, and Q_T^X are sourced or theorem-zero.",
            "status": "YUKAWA_SOURCE_PROJECTION_DERIVED",
            "missing_for_claim": "K_X, Z_X, lambda_X, and numeric/source-backed charges",
        },
        {
            **base(ts),
            "theorem_id": "WFH3652_4_PPN_vector_law",
            "claim": "PPN residuals inherit metric, source, readout, and boundary components.",
            "mathematical_form": "Delta_PPN = (gamma-1,beta-1,alpha1,alpha2,alpha3,xi,Gdot/G)_MTS = P_metric[h2,h4] + P_source[delta ln mu_obs,Q_S^X] + P_readout + P_boundary + P_nonEH.",
            "derivation_step": "Weak-field metric coefficients alone are insufficient if source calibration, clock/readout, non-Hilbert operators, or boundary currents are unowned.",
            "result": "A GR/PPN limit needs a vector zero theorem or bounded residual vector across all components.",
            "status": "PPN_RESIDUAL_VECTOR_DERIVED",
            "missing_for_claim": "metric weak-field coefficients and source/readout/boundary zero theorems",
        },
        {
            **base(ts),
            "theorem_id": "WFH3652_5_orbital_guard",
            "claim": "Orbital agreement is degenerate with fitted GM unless source calibration is separated.",
            "mathematical_form": "a^3 n^2 = mu_fit; residual_orbit = P_orb[delta ln mu_obs, Delta_PPN, preferred-frame, boundary/domain terms].",
            "derivation_step": "Classical orbits primarily determine mu_fit. That makes orbital success a necessary test but not a source-Hamiltonian proof unless cross-linked to WEP/R10/PPN and independent source calibration.",
            "result": "The orbital branch must use the same q_source vector as WEP/R10/PPN.",
            "status": "ORBITAL_GM_DEGENERACY_GUARD_DERIVED",
            "missing_for_claim": "orbital residual vector and independent source-calibration map",
        },
        {
            **base(ts),
            "theorem_id": "WFH3652_6_GR_Newton_zero_conditions",
            "claim": "Exact local GR/Newton recovery has a contract.",
            "mathematical_form": "q_metric=q_source=q_readout=q_boundary=q_nonEH=Q_A^X=f_EM=b_alpha=c_g=b_dis=0 and EH weak-field coefficients match GR through O(v^4/c^4).",
            "derivation_step": "Newton/PPN is recovered only when the metric field equations, source Hamiltonian, readout, and retained nonmetric channels are jointly silenced.",
            "result": "This is the local-GR gate: not impossible, but it must be signed as one branch rather than imported from GR notation.",
            "status": "LOCAL_GR_CONTRACT_DERIVED",
            "missing_for_claim": "single parent branch signing every zero condition",
        },
        {
            **base(ts),
            "theorem_id": "WFH3652_7_verdict",
            "claim": "Current MTS proves the weak-field source Hamiltonian and local GR/Newton limit.",
            "mathematical_form": "WFH3652_0 through WFH3652_6 parent-signed => Newtonian Poisson and PPN-GR vector; otherwise retain q_GM_source_abs and Delta_PPN_MTS.",
            "derivation_step": "The source-Hamiltonian route is explicit, but current corpus has not signed source mass, GM calibration, boundary/readout, and PPN metric coefficients together.",
            "result": "Current MTS has a derived weak-field source-calibration law but not a local GR/Newton pass.",
            "status": "FAIL_CURRENT_CLAIM_WEAK_FIELD_SOURCE_HAMILTONIAN_UNSIGNED",
            "missing_for_claim": "parent-signed weak-field Hamiltonian/PPN branch or numeric bounded vector",
        },
    ]


def calibration_rows(ts: str) -> list[dict[str, object]]:
    row = {**base(ts), "score_ready": False}
    specs = [
        ("GMC3652_0_mu_fit", "mu_fit", "(GM)_fit measured by orbital/ephemeris dynamics", "m^3 s^-2 or normalized", "orbital/ephemeris source path; source body", "ORBITAL_SOURCE_DATA_REQUIRED", "orbital;PPN", "tau_orbital;tau_PPN"),
        ("GMC3652_1_delta_mu", "delta_ln_mu_obs", "delta ln mu_obs = delta ln G_obs + delta ln M_S^eff + q_metric + q_readout + q_boundary + q_source", "dimensionless", "3652 GM calibration law", "COMPONENT_VALUES_REQUIRED", "orbital;PPN;Gdot", "tau_orbital;tau_PPN"),
        ("GMC3652_2_Qsource", "Q_source_X", "source-body logarithmic charge from 3651 matrix", "dimensionless", "3651 Q_source_X row; source composition/Hamiltonian", "SOURCE_BODY_CHARGE_REQUIRED", "WEP;R10;PPN;orbital", "tau_WEP;tau_R10;tau_PPN;tau_orbital"),
        ("GMC3652_3_Qtest", "Q_test_X", "test-body logarithmic charge from 3651 matrix", "dimensionless", "3651 composition/test rows", "TEST_BODY_CHARGE_REQUIRED", "WEP;R10", "tau_WEP;tau_R10"),
        ("GMC3652_4_alpha_ST", "alpha_ST", "K_X Q_source_X Q_test_X/(4*pi Z_X G_obs)", "dimensionless Yukawa strength", "K_X;Z_X;G_obs;Q_source_X;Q_test_X", "R10_COMPONENTS_REQUIRED", "R10", "tau_R10"),
        ("GMC3652_5_rho_source", "rho_active_minus_inertial", "rho_active/rho_inertial - 1 = q_source_mass + q_matter_source_abs + boundary/readout terms", "dimensionless density residual", "source Hamiltonian active/inertial identity", "ACTIVE_INERTIAL_IDENTITY_REQUIRED", "Newton;PPN;orbital", "tau_PPN;tau_orbital"),
        ("GMC3652_6_PPN_vector", "Delta_PPN_MTS", "(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,Gdot/G)_MTS source-calibration vector", "mixed dimensionless and yr^-1 for Gdot", "local_bounds R3-R9 plus MTS weak-field map", "PPN_COMPONENT_MAP_REQUIRED", "PPN", "tau_PPN"),
        ("GMC3652_7_orbital_vector", "Delta_orbital_MTS", "orbital residual vector after separating fitted GM from source calibration", "observable-dependent", "orbital residual data/model map", "ORBITAL_VECTOR_REQUIRED", "orbital", "tau_orbital"),
        ("GMC3652_8_total_guard", "q_GM_source_abs", "sum of absolute GM/source components |delta ln G|+|delta ln M_S|+|q_metric|+|q_readout|+|q_boundary|+|q_source|", "dimensionless envelope", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "Newton;PPN;orbital;WEP;R10", "all_tau"),
    ]
    return [
        {
            **row,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "required_inputs": required,
            "current_status": status,
            "observable_links": links,
            "tau_domain_link": tau,
        }
        for row_id, symbol, definition, units, required, status, links, tau in specs
    ]


def residual_vector_rows(ts: str) -> list[dict[str, object]]:
    row = {**base(ts), "score_ready": False}
    specs = [
        ("PVR3652_0_gamma", "gamma_minus_1", "PPN spatial curvature residual receives metric plus source/readout calibration", "dimensionless", "local_bounds.csv:R3_gamma", "METRIC_AND_SOURCE_MAP_REQUIRED"),
        ("PVR3652_1_beta", "beta_minus_1", "PPN nonlinearity residual receives metric self-coupling plus source Hamiltonian corrections", "dimensionless", "local_bounds.csv:R4_beta", "METRIC_AND_SOURCE_MAP_REQUIRED"),
        ("PVR3652_2_alpha1", "alpha1", "preferred-frame residual must include source momentum/current and boundary/domain leakage", "dimensionless", "local_bounds.csv:R5_alpha1", "PREFERRED_FRAME_SOURCE_MAP_REQUIRED"),
        ("PVR3652_3_alpha2", "alpha2", "spin/preferred-frame residual must include source frame and boundary/domain leakage", "dimensionless", "local_bounds.csv:R6_alpha2", "PREFERRED_FRAME_SOURCE_MAP_REQUIRED"),
        ("PVR3652_4_alpha3", "alpha3", "momentum nonconservation residual tests source current/flux silence", "dimensionless", "local_bounds.csv:R7_alpha3", "SOURCE_FLUX_SILENCE_REQUIRED"),
        ("PVR3652_5_xi", "xi", "preferred-location residual tests source/background coupling and boundary/domain terms", "dimensionless", "local_bounds.csv:R8_xi", "PREFERRED_LOCATION_SOURCE_MAP_REQUIRED"),
        ("PVR3652_6_Gdot", "Gdot_over_G", "time-varying source calibration or G_obs drift appears in LLR/orbital residual", "yr^-1", "local_bounds.csv:R9_Gdot", "TIME_DRIFT_SOURCE_MAP_REQUIRED"),
        ("PVR3652_7_R10", "alpha_lambda_R10", "short-range Yukawa branch from Q_source_X Q_test_X", "range-dependent", "local_bounds.csv:R10_fifth_force", "R10_CURVE_AND_MTS_COMPONENTS_REQUIRED"),
        ("PVR3652_8_total", "PPN_orbital_source_abs", "absolute residual envelope across PPN, Gdot, orbital, and R10 source calibration terms", "mixed normalized vector", "3652 no-cancellation policy", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        {
            **row,
            "vector_id": vector_id,
            "observable": observable,
            "definition": definition,
            "units": units,
            "source_path_or_bound": source,
            "current_status": status,
        }
        for vector_id, observable, definition, units, source, status in specs
    ]


def projection_rows(ts: str) -> list[dict[str, object]]:
    row = {**base(ts), "score_ready": False}
    specs = [
        ("WFP3652_0_Newton", "Newtonian_Poisson", "nabla^2 Phi_N=4*pi G_obs rho_inertial only if active/inertial source identity and boundary silence hold", "rho_active_minus_inertial;q_GM_source_abs;EH weak-field coefficients", "SOURCE_IDENTITY_UNSIGNED"),
        ("WFP3652_1_PPN", "local_GR_PPN", "Delta_PPN_MTS must be zero or bounded against R3-R9", "Delta_PPN_MTS;q_GM_source_abs;PPN bounds", "PPN_VECTOR_NOT_SCORE_READY"),
        ("WFP3652_2_orbital", "orbital_dynamics", "orbital residuals must be evaluated after fitted-GM degeneracy is separated", "mu_fit;Delta_orbital_MTS;source body map", "ORBITAL_VECTOR_NOT_SCORE_READY"),
        ("WFP3652_3_WEP", "WEP_crosscheck", "same Q_source_X and Q_test_X enter eta_AB source-charge row", "Q_source_X;DeltaQ_AB_X;tau_WEP;R1 bound", "COMPOSITION_VALUES_MISSING"),
        ("WFP3652_4_R10", "R10_crosscheck", "same source Hamiltonian charge enters alpha_ST(lambda)", "alpha_ST;lambda_X;R10 curve", "R10_COMPONENTS_MISSING"),
        ("WFP3652_5_clock", "clock_readout_crosscheck", "clock/readout residual must not be used to hide source GM drift", "b_clock;b_alpha;delta_ln_mu_obs;Gdot", "READOUT_SOURCE_BRIDGE_MISSING"),
        ("WFP3652_6_total", "all_local_arenas", "single no-cancellation envelope across metric, source, readout, boundary, non-EH, WEP, R10, PPN, and orbital rows", "all component rows;source paths;units", "NO_CANCELLATION_POLICY_ACTIVE"),
    ]
    return [
        {
            **row,
            "projection_id": projection_id,
            "arena": arena,
            "projection_law": law,
            "required_inputs": required,
            "current_status": status,
        }
        for projection_id, arena, law, required, status in specs
    ]


def decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "decision_id": "DEC3652_0_derivation",
            "decision": "Weak-field source calibration is derived: fitted GM equals G_obs times effective source mass plus metric/readout/boundary/source residuals.",
            "status": "GM_CALIBRATION_LAW_DERIVED",
        },
        {
            **base(ts),
            "decision_id": "DEC3652_1_verdict",
            "decision": "Current MTS does not parent-sign weak-field source Hamiltonian, active/inertial source identity, PPN metric vector, readout, and boundary silence together.",
            "status": "PARENT_WEAK_FIELD_SOURCE_HAMILTONIAN_UNSIGNED",
        },
        {
            **base(ts),
            "decision_id": "DEC3652_2_rows",
            "decision": "q_GM_source_abs, Delta_PPN_MTS, Delta_orbital_MTS, alpha_ST, and source-density residual rows are staged as nonclaim bounds.",
            "status": "SOURCE_CALIBRATION_VECTOR_CREATED_NOT_SCORE_READY",
        },
        {
            **base(ts),
            "decision_id": "DEC3652_3_next",
            "decision": "Next target is the Newton-Poisson/PPN zero-vector gate: derive the metric weak-field coefficients and close or retain every local-GR residual component.",
            "status": "NEWTON_PPN_ZERO_VECTOR_GATE_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "WEAK_FIELD_GM_CALIBRATION_LAW_DERIVED_SOURCE_VECTOR_NONCLAIM",
            "summary": "3652 derives the fitted-GM/source-Hamiltonian calibration law, the Poisson source condition, and the PPN/orbital residual vector, while keeping all rows nonclaim.",
            "claim_ceiling": "no weak-field source Hamiltonian, Newtonian, PPN, orbital, R10, WEP, local-GR, or calibrated-source pass is claimed",
            "useful_result": "The local-GR throat is now explicit: prove a parent weak-field source Hamiltonian plus PPN metric zero vector, or score q_GM_source_abs/Delta_PPN_MTS as retained residuals.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3652_0",
            "target_doc": "3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md",
            "target_script": "scripts/Y5_R2FR_3653_Newton_Poisson_PPN_zero_vector_gate_or_local_GR_residual_fit.py",
            "objective": "derive the exact Newton-Poisson and PPN-GR zero-vector conditions from the parent weak-field action, or retain a bounded local-GR residual vector with source/readout/boundary/non-EH components",
            "success_gate": "either Newton/PPN local GR limit is parent-signed, or every residual component has units, source paths, arena links, and no-cancellation guards",
        }
    ]


def write_doc(sources, theorem, calibration, residuals, projections, decision_rows, status, next_target) -> None:
    lines = [
        "# 3652 - Weak-field source Hamiltonian, GM calibration, or source-vector bound",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The weak-field gate is now explicit. Orbital/Newtonian data measure `mu_fit=(GM)_fit`; this equals `G_obs M_S^eff` only after the source Hamiltonian, active/inertial source identity, metric readout, and boundary/domain terms are owned. The derived calibration law is `delta ln mu_obs = delta ln G_obs + delta ln M_S^eff + q_metric + q_readout + q_boundary + q_source`.",
        "",
        "This means matching orbits is not by itself a local-GR proof: fitted `GM` can absorb source calibration. Current MTS does not yet sign the weak-field source Hamiltonian and PPN zero vector, so `q_GM_source_abs` and `Delta_PPN_MTS` remain nonclaim residual rows.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: `{row['status']}` — {row['result']}")
    lines.extend(["", "## GM/source calibration rows"])
    for row in calibration:
        lines.append(f"- `{row['row_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## PPN/orbital residual vector"])
    for row in residuals:
        lines.append(f"- `{row['vector_id']}`: `{row['observable']}` — {row['current_status']}")
    lines.extend(["", "## Projection rows"])
    for row in projections:
        lines.append(f"- `{row['projection_id']}`: `{row['arena']}` — {row['current_status']}")
    lines.extend(["", "## Decisions"])
    for row in decision_rows:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` — {row['decision']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(ts, output_paths, sources, theorem, calibration, residuals, projections, decision_rows, status, next_target):
    rows = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3652_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3652_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3652_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3652 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3652_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3652_4_GM_law", any("delta ln mu_obs" in row["mathematical_form"] for row in theorem), "GM calibration law present")
    add("VAL3652_5_Poisson_law", any("nabla^2 Phi_N" in row["mathematical_form"] for row in theorem), "Poisson source condition present")
    add("VAL3652_6_Yukawa_law", any("alpha_ST=K_X" in row["mathematical_form"] for row in theorem), "R10/Yukawa source projection present")
    add("VAL3652_7_PPN_vector", any("Delta_PPN" in row["mathematical_form"] for row in theorem), "PPN residual vector law present")
    add("VAL3652_8_local_GR_contract", any(row["status"] == "LOCAL_GR_CONTRACT_DERIVED" for row in theorem), "local GR zero-contract present")
    add("VAL3652_9_verdict_unsigned", any(row["status"] == "FAIL_CURRENT_CLAIM_WEAK_FIELD_SOURCE_HAMILTONIAN_UNSIGNED" for row in theorem), "weak-field source Hamiltonian not claimed")
    required_symbols = {"mu_fit", "delta_ln_mu_obs", "Q_source_X", "Q_test_X", "alpha_ST", "rho_active_minus_inertial", "Delta_PPN_MTS", "Delta_orbital_MTS", "q_GM_source_abs"}
    add("VAL3652_10_calibration_rows_complete", required_symbols.issubset({row["symbol"] for row in calibration}), "GM/source calibration rows complete")
    required_observables = {"gamma_minus_1", "beta_minus_1", "alpha1", "alpha2", "alpha3", "xi", "Gdot_over_G", "alpha_lambda_R10", "PPN_orbital_source_abs"}
    add("VAL3652_11_residual_vector_complete", required_observables.issubset({row["observable"] for row in residuals}), "PPN/R10/orbital residual vector complete")
    required_proj = {"Newtonian_Poisson", "local_GR_PPN", "orbital_dynamics", "WEP_crosscheck", "R10_crosscheck", "clock_readout_crosscheck"}
    add("VAL3652_12_projection_rows_complete", required_proj.issubset({row["arena"] for row in projections}), "Newton/PPN/orbital/WEP/R10/clock projections complete")
    add("VAL3652_13_tau_links", all(row["tau_domain_link"] for row in calibration), "every calibration row has tau/domain link")
    add("VAL3652_14_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in calibration + residuals + projections), "no generated scoring rows are score-ready")
    generated = sources + theorem + calibration + residuals + projections + decision_rows + status + next_target
    add("VAL3652_15_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3652_16_no_cancellation", any(row["symbol"] == "q_GM_source_abs" and "sum of absolute" in row["definition"] for row in calibration), "GM/source no-cancellation envelope present")
    add("VAL3652_17_status_honest", status[0]["status"] == "WEAK_FIELD_GM_CALIBRATION_LAW_DERIVED_SOURCE_VECTOR_NONCLAIM", "status keeps weak-field branch nonclaim")
    doc_text = text(DOC)
    add("VAL3652_18_doc_written", "mu_fit=(GM)_fit" in doc_text and "Current MTS does not yet sign" in doc_text and "Delta_PPN_MTS" in doc_text, "doc records GM law and caveat")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3652*", "3652-Y5-R2FR-*", "Y5_R2FR_3652_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3652_19_no_formalization_leak", not leaks, "no 3652 checkpoint files in formalization-workbench")
    add("VAL3652_20_next_target", next_target[0]["target_doc"].startswith("3653-") and "PPN-zero-vector" in next_target[0]["target_doc"], "3653 Newton/PPN zero-vector gate selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = theorem_rows(ts)
    calibration = calibration_rows(ts)
    residuals = residual_vector_rows(ts)
    projections = projection_rows(ts)
    decision_rows = decisions(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3652_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3652_WEAK_FIELD_HAMILTONIAN_THEOREM_ATTEMPT.csv",
        "calibration": RESIDUALS / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv",
        "projections": RESIDUALS / "P8_Y5_R2FR_3652_PROJECTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3652_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3652_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3652_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3652_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["calibration"], calibration)
    write_csv(outputs["residuals"], residuals)
    write_csv(outputs["projections"], projections)
    write_csv(outputs["decisions"], decision_rows)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, calibration, residuals, projections, decision_rows, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, calibration, residuals, projections, decision_rows, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3652 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3652 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
