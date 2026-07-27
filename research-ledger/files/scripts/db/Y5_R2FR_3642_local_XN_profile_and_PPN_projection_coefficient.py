from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3642"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_XN_PROFILE_AND_PPN_PROJECTION_COEFFICIENT_3642"
DOC = ROOT / "3642-Y5-R2FR-local-XN-profile-and-PPN-projection-coefficient.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3642_SOURCE_REGISTER.csv",
        "profile_derivation": RESIDUALS / "P8_Y5_R2FR_3642_LOCAL_XN_PROFILE_DERIVATION.csv",
        "profile_candidates": RESIDUALS / "P8_Y5_R2FR_3642_XN_PROFILE_CANDIDATES.csv",
        "ppn_projection": RESIDUALS / "P8_Y5_R2FR_3642_BETA_COMMON_TO_PPN_CGAMMA_MAP.csv",
        "bound_update": RESIDUALS / "P8_Y5_R2FR_3642_BETA_BOUND_UPDATE_ROWS.csv",
        "claim_gate": RESIDUALS / "P8_Y5_R2FR_3642_CLAIM_GATE.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3642_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3642_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3642_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    specs = [
        ("next_3641", RESIDUALS / "P8_Y5_R2FR_3641_NEXT_TARGET.csv", "local X_N time/radial profile", "3641 handoff to local profile and PPN coefficient"),
        ("fill_3641", RESIDUALS / "P8_Y5_R2FR_3641_BETA_COMMON_FIRST_NUMERIC_FILL.csv", "C_gamma is the MTS-to-PPN projection coefficient", "observational seeds requiring Xdot_N/C_gamma"),
        ("bounds_3640", RESIDUALS / "P8_Y5_R2FR_3640_BETA_COMMON_BOUND_INVERSION_ROWS.csv", "partial_r X_N", "bound inversion formulas inherited from 3640"),
        ("ward_residuals_3640", RESIDUALS / "P8_Y5_R2FR_3640_BETA_COMMON_WARD_RESIDUAL_DECOMPOSITION.csv", "beta_common = beta_q + beta_boundary", "five-term beta_common Ward residual split"),
        ("cgm_gate", RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM2_radial_hair", "time/radial derivative hair gate"),
        ("time_drift", RESIDUALS / "P8_time_drift_residual_or_zero.csv", "MISSING_NUMERIC_OR_DERIVED_ZERO_DRIFT", "existing time drift residual ledger"),
        ("radial_mu", RESIDUALS / "P8_radial_mu_profile_or_zero.csv", "MISSING_RADIAL_PROFILE_OR_DERIVED_ZERO", "existing radial source hair ledger"),
        ("local_profile_schema", RESIDUALS / "P8_Y5_PARENT_QLOC_2029_LOCAL_PROFILE_SCHEMA.csv", "PROF2029_4_range", "local profile schema with range/amplitude fields"),
        ("first_qloc_profile", RESIDUALS / "P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv", "QPROF1712_2_PPN_projection", "older q_loc profile to PPN projection template"),
        ("ppn_projection_1182", RESIDUALS / "P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv", "PPNP1182_2_gamma_leakage", "symbolic scalar PPN projection map"),
        ("cqgamma_1370", RESIDUALS / "P8_Y5_R10_1370_WARD_SAFE_CQGAMMA_DERIVATION.csv", "CQG1370_3_gamma_projection_coefficient", "Ward-safe q_loc to gamma coefficient"),
        ("cqgamma_inputs_1371", RESIDUALS / "P8_Y5_R10_1371_CQGAMMA_NORM_BOUND_INPUT_TABLE.csv", "CQN1371_5_qloc_norm", "missing numeric C_qgamma norm inputs"),
        ("ppn_parent_1520", RESIDUALS / "P8_Y5_PARENT_LCG_1520_CQGAMMA_DERIVATION_ATTEMPT.csv", "C_qgamma = R_gamma", "operator-form C_qgamma attempt"),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
            "valid_for_claim": False,
        }
        for source_id, path, needle, role in specs
    ]


def profile_derivation_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "derivation_id": "XN3642_0_local_generator_definition",
            "object": "X_N",
            "equation": "beta_common = X_N[ln mu_obs_common]; local drift and radial hair require Xdot_N := u^a nabla_a X_N and Xr_N := n^a nabla_a X_N",
            "derived_result": "the observational Gdot and radial/PPN rows depend on derivatives of the normalized local generator, not just on beta_common",
            "zero_condition": "X_N is stationary and radially constant in the exterior local source frame, or beta_common is parent-zero",
            "status": "DERIVED_DEFINITION",
        },
        {
            **base,
            "derivation_id": "XN3642_1_stationary_exterior_zero",
            "object": "Xdot_N",
            "equation": "if L_u X_N=0 in the calibrated local source frame and all explicit_t Ward residuals vanish, then d ln mu_obs/dt=0",
            "derived_result": "Gdot seed becomes a theorem-zero branch only under a signed stationarity/source-normalization theorem",
            "zero_condition": "parent signs local stationarity, no source flux, no cosmological bleed-through, and no time-dependent calibration projector",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
        },
        {
            **base,
            "derivation_id": "XN3642_2_exterior_profile_operator",
            "object": "X_N(r,t)",
            "equation": "(Box_loc - m_X^2) delta X_N = J_X^eff with J_X^eff=0 outside the compact source gives delta X_N(r)=A_X exp(-r/ell_X)/r + X_inf for a static spherical exterior",
            "derived_result": "finite local hair must be Yukawa/Gauss-shaped unless the parent operator/profile differs",
            "zero_condition": "A_X=0 by Gauss/no-hair/Ward theorem, or ell_X and A_X are sourced and bounded",
            "status": "PROFILE_LAW_DERIVED_CONDITIONALLY",
        },
        {
            **base,
            "derivation_id": "XN3642_3_radial_derivative_law",
            "object": "partial_r X_N",
            "equation": "for delta X_N=A_X exp(-r/ell_X)/r, partial_r X_N = -(1/r + 1/ell_X) delta X_N",
            "derived_result": "radial source hair can now be bounded by amplitude/range rather than a free unknown function",
            "zero_condition": "A_X=0, ell_X -> 0 below arena sensitivity, or beta_common*partial_r X_N below orbital/R10/PPN bounds",
            "status": "RADIAL_LAW_FILLED_SYMBOLIC",
        },
        {
            **base,
            "derivation_id": "XN3642_4_time_drift_law",
            "object": "Xdot_N",
            "equation": "Xdot_N = dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf plus source-motion/projector terms",
            "derived_result": "Gdot needs either a stationarity theorem or time-profile amplitudes dot_A_X, dot_ell_X, dot_X_inf",
            "zero_condition": "dot_A_X=dot_ell_X=dot_X_inf=0 and projector/source-motion terms vanish",
            "status": "TIME_LAW_FILLED_SYMBOLIC",
        },
        {
            **base,
            "derivation_id": "XN3642_5_ppn_coefficient_definition",
            "object": "C_gamma",
            "equation": "gamma-1 = C_gamma beta_common^2 + C_grad nabla X_N + retained channels; C_gamma := C_qgamma[N_beta->q_loc]",
            "derived_result": "C_gamma is the existing Ward-safe C_qgamma operator applied to the beta_common-induced conserved metric source, not a new free scalar",
            "zero_condition": "C_qgamma response vanishes by tracefree/no-leak theorem, or beta-induced q_loc source is zero",
            "status": "CGAMMA_MAP_DERIVED_SYMBOLIC",
        },
    ]


def profile_candidate_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "profile_id": "XNP3642_0_stationary_constant",
            "branch": "theorem_zero_candidate",
            "profile": "X_N=X_inf constant in local exterior",
            "Xdot_N": "0",
            "partial_r_X_N": "0",
            "required_parent_premises": "stationary local source; quotient-owned source normalization; no boundary/source/projector/calibration residual",
            "claim_status": "CONDITIONAL_NOT_SIGNED",
        },
        {
            **base,
            "profile_id": "XNP3642_1_massive_yukawa",
            "branch": "finite_profile_bound",
            "profile": "X_N=X_inf + A_X exp(-r/ell_X)/r",
            "Xdot_N": "dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf",
            "partial_r_X_N": "-(1/r+1/ell_X) A_X exp(-r/ell_X)/r",
            "required_parent_premises": "linearized local operator; compact source exterior; ell_X=1/m_X; amplitude A_X sourced",
            "claim_status": "BOUNDABLE_SYMBOLIC",
        },
        {
            **base,
            "profile_id": "XNP3642_2_massless_gauss",
            "branch": "finite_profile_bound",
            "profile": "X_N=X_inf + Q_X/r",
            "Xdot_N": "dot_Q_X/r + dot_X_inf",
            "partial_r_X_N": "-Q_X/r^2",
            "required_parent_premises": "massless exterior mode; Gauss charge Q_X; no screening",
            "claim_status": "BOUNDABLE_SYMBOLIC_HIGH_PRESSURE",
        },
        {
            **base,
            "profile_id": "XNP3642_3_cosmological_bleed",
            "branch": "drift_guard",
            "profile": "X_N=X_inf(t)+local screened correction",
            "Xdot_N": "dot_X_inf + screened local terms",
            "partial_r_X_N": "screened local terms only",
            "required_parent_premises": "cosmology/local matching map and screening/domain lock",
            "claim_status": "CANNOT_IMPORT_COSMOLOGY_AS_LOCAL_SILENCE",
        },
    ]


def ppn_projection_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "map_id": "CG3642_0_metric_slip_definition",
            "quantity": "gamma_minus_1",
            "map": "gamma-1 = (Psi-Phi)/Phi_GR in weak-field scalar/isotropic PPN projection",
            "C_gamma_definition": "C_gamma is the coefficient of beta_common^2 after measured-GM calibration and removal/bounding of derivative channels",
            "source_link": "PPNP1182_0_metric_ansatz;PPNP1182_2_gamma_leakage",
            "status": "PPN_CONVENTION_LINKED",
        },
        {
            **base,
            "map_id": "CG3642_1_ward_safe_operator",
            "quantity": "C_gamma",
            "map": "C_gamma := C_qgamma[S_beta] = -(c^2/(2U_ref)) P_scalar P_metric G_EH Div^-1[S_beta]",
            "C_gamma_definition": "S_beta is the conserved compensator/source produced by beta_common after source-normalization Ward splitting",
            "source_link": "CQG1370_3_gamma_projection_coefficient;CQG1370_4_norm_bound",
            "status": "SYMBOLIC_OPERATOR_COEFFICIENT_DERIVED",
        },
        {
            **base,
            "map_id": "CG3642_2_norm_bound",
            "quantity": "|C_gamma|",
            "map": "|C_gamma| <= (c^2/(2U_min)) N_G N_D N_beta",
            "C_gamma_definition": "N_beta maps beta_common^2 into the norm of the conserved q/source compensator; N_G and N_D are the metric Green and divergence inverse norms",
            "source_link": "CQN1371_2_potential_floor;CQN1371_3_green_norm;CQN1371_4_div_inverse_norm;CQN1371_5_qloc_norm",
            "status": "NORM_BOUND_DERIVED_INPUTS_MISSING",
        },
        {
            **base,
            "map_id": "CG3642_3_qR_bridge_guard",
            "quantity": "conditional C_gamma=-1/2",
            "map": "C_gamma=-1/2 may be used only if beta_common-induced q_loc equals q_R_hat with same GM convention, gauge, source averaging, and no retained channels",
            "C_gamma_definition": "otherwise use the operator coefficient, not the q_R shortcut",
            "source_link": "CQG1520_2_qR_bridge_conditional;QMAP1240_3_gamma_projection",
            "status": "SHORTCUT_BLOCKED_UNLESS_BRIDGE_SIGNED",
        },
    ]


def bound_update_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "bound_id": "B3642_0_gdot_stationary_or_profile",
            "arena": "Gdot_clock",
            "updated_bound": "|beta_common| <= (9.0e-13 yr^-1 + |explicit_t residuals|)/|dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf|",
            "claimable_zero_route": "Xdot_N=0 only if local stationarity and projector/source/calibration time silence are parent-signed",
            "still_missing": "A_X;ell_X;dot_A_X;dot_ell_X;dot_X_inf;explicit_t residuals",
            "status": "FORMULA_SHARPENED_NOT_NUMERIC",
        },
        {
            **base,
            "bound_id": "B3642_1_ppn_cgamma_operator",
            "arena": "PPN_local_GR",
            "updated_bound": "|beta_common| <= sqrt(2.3e-5/|C_gamma|), C_gamma=C_qgamma[S_beta]",
            "claimable_zero_route": "C_gamma=0 only if scalar trace/leakage response vanishes by Ward-safe operator theorem",
            "still_missing": "S_beta;U_ref/U_min;G_EH;Div^-1;N_beta;retained channels",
            "status": "CGAMMA_BOUND_SHARPENED_NOT_NUMERIC",
        },
        {
            **base,
            "bound_id": "B3642_2_radial_yukawa",
            "arena": "orbital_radial",
            "updated_bound": "|beta_common| <= (|partial_r ln mu|_limit + |explicit_r residuals|)/(|A_X| exp(-r/ell_X)(1/r+1/ell_X)/r)",
            "claimable_zero_route": "A_X=0 by Gauss/no-hair/source Ward theorem",
            "still_missing": "A_X;ell_X;radial residual limit;explicit_r residuals;source radius/calibration",
            "status": "RADIAL_BOUND_SHARPENED_NOT_NUMERIC",
        },
        {
            **base,
            "bound_id": "B3642_3_r10_profile_link",
            "arena": "R10_short_range",
            "updated_bound": "lambda_X=ell_X and alpha_common(lambda)=K_X beta_common^2 tau_R10(lambda)/M_X^2 with profile support A_X exp(-r/ell_X)/r",
            "claimable_zero_route": "ell_X/support outside R10 sensitivity or A_X=0 by theorem",
            "still_missing": "alpha_bound(lambda);K_X;M_X^2;tau_R10(lambda);A_X;ell_X",
            "status": "R10_PROFILE_LINK_SHARPENED_NOT_NUMERIC",
        },
    ]


def claim_gate_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "gate_id": "G3642_0_no_constant_profile_axiom",
            "gate": "Do not assert Xdot_N=partial_r X_N=0 as a local plateau axiom.",
            "pass_condition": "stationarity/no-hair/Ward theorem signs it, or finite profile rows are bounded",
            "status": "ENFORCED",
        },
        {
            **base,
            "gate_id": "G3642_1_no_qR_shortcut",
            "gate": "Do not import C_gamma=-1/2 from q_R unless q_loc/q_R normalization bridge is signed.",
            "pass_condition": "same source averaging, GM convention, gauge, and retained-channel silence",
            "status": "ENFORCED",
        },
        {
            **base,
            "gate_id": "G3642_2_local_gr_newton_route",
            "gate": "Local GR/Newton recovery requires constant measured source normalization and zero/scored PPN slip.",
            "pass_condition": "Xdot_N, partial_r X_N, and C_gamma branch are parent-zero or numerically below bounds",
            "status": "ACTIVE",
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "LOCAL_XN_PROFILE_LAWS_AND_CGAMMA_OPERATOR_MAP_FILLED_NONCLAIM",
            "summary": "3642 derives the local X_N profile laws needed for Gdot/radial/R10 bounds and maps beta_common to the existing Ward-safe C_qgamma PPN operator. It does not claim Xdot_N=0, radial hair zero, or C_gamma numeric; it sharpens each into theorem-zero premises or explicit amplitude/range/operator inputs.",
            "claim_ceiling": "no local-GR/Newton, PPN, Gdot, R10, radial, or beta_common pass is allowed from 3642",
            "useful_result": "the next hard unknowns are now concrete: A_X, ell_X, dot_A_X, dot_ell_X, dot_X_inf, S_beta, U_ref, G_EH, Div^-1, and N_beta",
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3642_0",
            "target_doc": "3643-Y5-R2FR-local-stationarity-nohair-or-first-profile-amplitude-row.md",
            "target_script": "scripts/Y5_R2FR_3643_local_stationarity_nohair_or_first_profile_amplitude_row.py",
            "objective": "try to derive the local stationarity/no-hair theorem A_X=dot_A_X=dot_ell_X=dot_X_inf=0; if unsigned, fill the first nonclaim amplitude/range row for the Yukawa/Gauss X_N profile",
            "success_gate": "either local X_N profile is theorem-zero, or A_X/ell_X time/radial profile rows exist with units, source premises, and links to Gdot/PPN/R10 bounds",
            "valid_for_claim": False,
        }
    ]


def write_doc(src, deriv, profiles, ppn, bounds, gates, status, nxt) -> None:
    text = "\n\n".join(
        [
            "# 3642 Y5 R2FR local XN profile and PPN projection coefficient",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Derivation result",
            (
                "`X_N` now has two non-smuggled local branches. The clean branch is theorem-zero: `Xdot_N=0` and "
                "`partial_r X_N=0` only if local stationarity, source-normalization descent, boundary silence, and projector/calibration silence are signed. "
                "The finite branch is a local exterior profile: `delta X_N=A_X exp(-r/ell_X)/r`, giving "
                "`partial_r X_N=-(1/r+1/ell_X) delta X_N`."
            ),
            (
                "The PPN coefficient is also tied down: `C_gamma` is not a free knob. It is the existing Ward-safe "
                "`C_qgamma` operator applied to the beta-induced conserved source, `C_gamma=C_qgamma[S_beta]`."
            ),
            "## Profile derivation rows",
            "\n".join(f"- `{row['derivation_id']}`: {row['status']} — {row['equation']}" for row in deriv),
            "## Profile candidates",
            "\n".join(f"- `{row['profile_id']}`: `{row['profile']}` | `Xdot_N={row['Xdot_N']}` | `partial_r_X_N={row['partial_r_X_N']}`." for row in profiles),
            "## PPN coefficient map",
            "\n".join(f"- `{row['map_id']}`: {row['status']} — `{row['map']}`." for row in ppn),
            "## Bound updates",
            "\n".join(f"- `{row['bound_id']}`: {row['arena']} — `{row['updated_bound']}`." for row in bounds),
            "## Claim gates",
            "\n".join(f"- `{row['gate_id']}`: {row['status']} — {row['gate']}" for row in gates),
            "## Next target",
            f"`{nxt[0]['target_doc']}` via `{nxt[0]['target_script']}`.",
            "## Sources",
            "\n".join(f"- `{row['source_id']}`: `{row['local_path']}` exists={row['exists']} needle_found={row['needle_found']}" for row in src),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(out: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3642_0_sources_exist", all(bool(row["exists"]) for row in src), "all source paths exist")
    add("VAL3642_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3642_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")
    parse_ok = True
    details = []
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3642_3_csv_parse", parse_ok, "; ".join(details))

    deriv = read_csv(out["profile_derivation"])
    profiles = read_csv(out["profile_candidates"])
    ppn = read_csv(out["ppn_projection"])
    bounds = read_csv(out["bound_update"])
    gates = read_csv(out["claim_gate"])
    status = read_csv(out["status"])
    nxt = read_csv(out["next_target"])

    add("VAL3642_4_yukawa_law_present", any("exp(-r/ell_X)/r" in row["equation"] for row in deriv), "Yukawa/Gauss exterior law derived")
    add("VAL3642_5_time_law_present", any("dot_A_X" in row["equation"] for row in deriv), "time drift law derives Xdot_N inputs")
    add("VAL3642_6_profiles_cover_branches", {"theorem_zero_candidate", "finite_profile_bound", "drift_guard"}.issubset({row["branch"] for row in profiles}), "profile branch set covers zero, finite, and drift guard")
    add("VAL3642_7_cgamma_operator_map", any("C_qgamma[S_beta]" in row["map"] for row in ppn), "C_gamma tied to Ward-safe C_qgamma operator")
    add("VAL3642_8_qr_shortcut_guard", any(row["status"] == "SHORTCUT_BLOCKED_UNLESS_BRIDGE_SIGNED" for row in ppn), "q_R shortcut guard present")
    add("VAL3642_9_bounds_updated", {"Gdot_clock", "PPN_local_GR", "orbital_radial", "R10_short_range"}.issubset({row["arena"] for row in bounds}), "Gdot/PPN/radial/R10 bound updates present")
    add("VAL3642_10_no_axiom_gate", any(row["gate_id"] == "G3642_0_no_constant_profile_axiom" and row["status"] == "ENFORCED" for row in gates), "constant profile axiom forbidden")
    add("VAL3642_11_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in deriv + profiles + ppn + bounds + gates + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3642*")) if FORMALIZATION.exists() else []
    add("VAL3642_12_no_formalization_leak", not leaks, "no 3642 files in formalization-workbench")
    add("VAL3642_13_next_target_written", bool(nxt) and "3643" in nxt[0]["target_doc"], "3643 local no-hair/amplitude target written")
    add("VAL3642_14_doc_written", DOC.exists() and "C_gamma=C_qgamma[S_beta]" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with C_gamma operator map")
    add("VAL3642_15_status_honest", status[0]["status"] == "LOCAL_XN_PROFILE_LAWS_AND_CGAMMA_OPERATOR_MAP_FILLED_NONCLAIM", "status keeps profile/C_gamma nonclaim")
    return rows


def main() -> None:
    t = now()
    out = outputs()
    src = source_rows(t)
    deriv = profile_derivation_rows(t)
    profiles = profile_candidate_rows(t)
    ppn = ppn_projection_rows(t)
    bounds = bound_update_rows(t)
    gates = claim_gate_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)

    write_csv(out["source_register"], src)
    write_csv(out["profile_derivation"], deriv)
    write_csv(out["profile_candidates"], profiles)
    write_csv(out["ppn_projection"], ppn)
    write_csv(out["bound_update"], bounds)
    write_csv(out["claim_gate"], gates)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, deriv, profiles, ppn, bounds, gates, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3642 validation failed: {failures}")
    print(f"wrote 3642 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
