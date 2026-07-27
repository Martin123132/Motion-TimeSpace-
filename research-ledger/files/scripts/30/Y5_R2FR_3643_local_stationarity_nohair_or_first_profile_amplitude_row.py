from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3643"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_STATIONARITY_NOHAIR_OR_FIRST_PROFILE_AMPLITUDE_ROW_3643"
DOC = ROOT / "3643-Y5-R2FR-local-stationarity-nohair-or-first-profile-amplitude-row.md"


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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3643_SOURCE_REGISTER.csv",
        "nohair_theorem_attempt": RESIDUALS / "P8_Y5_R2FR_3643_LOCAL_STATIONARITY_NOHAIR_THEOREM_ATTEMPT.csv",
        "premise_audit": RESIDUALS / "P8_Y5_R2FR_3643_NOHAIR_PREMISE_AUDIT.csv",
        "amplitude_rows": RESIDUALS / "P8_Y5_R2FR_3643_XN_AMPLITUDE_RANGE_PROFILE_ROWS.csv",
        "bound_updates": RESIDUALS / "P8_Y5_R2FR_3643_PROFILE_BOUND_UPDATE_ROWS.csv",
        "claim_gate": RESIDUALS / "P8_Y5_R2FR_3643_CLAIM_GATE.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3643_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3643_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3643_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    specs = [
        ("next_3642", RESIDUALS / "P8_Y5_R2FR_3642_NEXT_TARGET.csv", "A_X=dot_A_X=dot_ell_X=dot_X_inf=0", "3642 handoff to local stationarity/no-hair"),
        ("profile_derivation_3642", RESIDUALS / "P8_Y5_R2FR_3642_LOCAL_XN_PROFILE_DERIVATION.csv", "PROFILE_LAW_DERIVED_CONDITIONALLY", "3642 profile law and derivative laws"),
        ("profile_candidates_3642", RESIDUALS / "P8_Y5_R2FR_3642_XN_PROFILE_CANDIDATES.csv", "XNP3642_1_massive_yukawa", "3642 Yukawa/Gauss candidates"),
        ("bound_updates_3642", RESIDUALS / "P8_Y5_R2FR_3642_BETA_BOUND_UPDATE_ROWS.csv", "A_X;ell_X", "3642 bound rows requiring amplitude/range"),
        ("elliptic_rebase_2606", RESIDUALS / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_BOUNDARY_AMPLITUDE_THEOREM.csv", "BAT2606_1_nohair_zero_case", "coercive energy identity and exact conditional no-hair theorem"),
        ("gk_nohair_2470", RESIDUALS / "P8_Y5_GK_NOHAIR_2470_NOHAIR_PROOF_ATTEMPT.csv", "NH2470_6_current_status", "prior GK no-hair proof status"),
        ("gk_positivity_2470", RESIDUALS / "P8_Y5_GK_NOHAIR_2470_POSITIVITY_CLAUSES.csv", "POS2470_1_quadratic_form", "coercivity and positivity clauses"),
        ("boundary_obstructions_549", RESIDUALS / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_OBSTRUCTION_LEDGER.csv", "BCO549_3_derivative_hair", "boundary derivative hair obstruction"),
        ("time_drift_row", RESIDUALS / "P8_time_drift_residual_or_zero.csv", "TD3048_0_time_drift_definition", "existing Gdot/time drift row"),
        ("radial_mu_row", RESIDUALS / "P8_radial_mu_profile_or_zero.csv", "RH3048_0_radial_hair_definition", "existing radial source hair row"),
        ("constant_gm_gate", RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM2_radial_hair", "constant-GM derivative hair gate"),
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


def nohair_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "theorem_id": "NH3643_0_operator_contract",
            "claim": "local X_N exterior perturbation obeys a coercive screened elliptic operator",
            "mathematical_form": "L_X delta X_N := (-D_X Delta_h + M_X^2) delta X_N = J_X^eff on exterior domain Omega_ext, with D_X>0 and M_X^2>=0",
            "derived_result": "this is the minimal form needed to make no-hair or amplitude bounds meaningful",
            "promotion_condition": "parent owns L_X, D_X, M_X^2, domain, units, and normalization of X_N",
            "status": "CONDITIONAL_OPERATOR_FORM",
        },
        {
            **base,
            "theorem_id": "NH3643_1_energy_identity",
            "claim": "multiply by delta X_N and integrate by parts",
            "mathematical_form": "int_Omega D_X |grad delta X_N|^2 + M_X^2 delta X_N^2 = int_Omega J_X^eff delta X_N + int_boundary delta X_N n.D_X grad delta X_N",
            "derived_result": "if source and boundary flux vanish, positive energy forces the profile to vanish",
            "promotion_condition": "source silence, boundary no-flux, coercivity, and regular exterior domain",
            "status": "EXACT_CONDITIONAL_ENERGY_IDENTITY",
        },
        {
            **base,
            "theorem_id": "NH3643_2_zero_hair_branch",
            "claim": "A_X=0 and Q_X=0 follow only in the exact no-source/no-boundary branch",
            "mathematical_form": "J_X^eff=0, boundary_flux=0, harmonic/topological sector=0, M_X^2>=0, D_X>0 => delta X_N=0 => A_X=Q_X=0",
            "derived_result": "local stationarity/no-hair is a theorem if all premises are parent-signed",
            "promotion_condition": "all premises in premise audit marked parent_signed",
            "status": "THEOREM_ZERO_CONDITIONAL_NOT_PARENT_SIGNED",
        },
        {
            **base,
            "theorem_id": "NH3643_3_time_stationarity_branch",
            "claim": "dot_A_X=dot_ell_X=dot_X_inf=0 requires stationarity of operator, source, boundary, and calibration projector",
            "mathematical_form": "partial_t L_X=0, partial_t J_X^eff=0, partial_t boundary_flux=0, partial_t projector=0 => partial_t delta X_N=0",
            "derived_result": "Gdot cannot be silenced by static profile shape alone; the time derivative of the data must vanish",
            "promotion_condition": "Killing/local stationarity plus source/current/projector time-silence theorem",
            "status": "TIME_ZERO_CONDITIONAL_NOT_PARENT_SIGNED",
        },
        {
            **base,
            "theorem_id": "NH3643_4_finite_amplitude_branch",
            "claim": "if any premise is unsigned, the finite profile must be carried explicitly",
            "mathematical_form": "A_X = A_src + A_bdy + A_top + A_proj + A_shell, ell_X=1/sqrt(M_X^2/D_X) when M_X^2>0",
            "derived_result": "the profile is no longer a vague closure gap; it becomes amplitude/range rows with source owners",
            "promotion_condition": "source-backed values or parent-zero theorem for every amplitude component",
            "status": "AMPLITUDE_ROW_REQUIRED",
        },
    ]


def premise_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    specs = [
        ("P3643_0_operator_owner", "L_X, D_X, M_X^2 are parent-owned with units", "needed to know which profile law is legal", "unsigned; 3642 only derived symbolic profile law", "MISSING_PARENT_OPERATOR_OWNERSHIP"),
        ("P3643_1_coercivity", "D_X>0 and M_X^2>=0, plus cross terms bounded by eta<1", "prevents ghost/tachyon homogeneous hair", "2470/2606 state condition but do not parent-sign it", "MISSING_COERCIVITY_SIGNATURE"),
        ("P3643_2_source_silence", "J_X^eff=0 outside compact source and no residual source tail", "kills A_src", "source-current descent remains unsigned in beta_common branch", "MISSING_SOURCE_SILENCE"),
        ("P3643_3_boundary_no_flux", "boundary flux and relative cohomology class vanish", "kills A_bdy/A_top", "boundary exactness/cohomology route remains conditional", "MISSING_BOUNDARY_NOFLUX"),
        ("P3643_4_projector_silence", "projector/readout/calibration carries no local profile source", "kills A_proj and dot projector terms", "projector stress/hiding remains an obstruction", "MISSING_PROJECTOR_SILENCE"),
        ("P3643_5_stationarity", "partial_t L_X=partial_t J_X=partial_t boundary=partial_t projector=0", "kills dot_A_X, dot_ell_X, dot_X_inf", "local stationary source theorem not parent-signed", "MISSING_LOCAL_STATIONARITY"),
        ("P3643_6_topology", "no harmonic/topological exterior mode", "kills Q_X and A_top", "topological hair ledger remains open", "MISSING_TOPOLOGY_CERTIFICATE"),
    ]
    return [
        {
            **base,
            "premise_id": premise_id,
            "premise": premise,
            "why_needed": why_needed,
            "current_evidence": current_evidence,
            "status": status,
            "parent_signed": False,
        }
        for premise_id, premise, why_needed, current_evidence, status in specs
    ]


def amplitude_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    return [
        {
            **base,
            "row_id": "AMP3643_0_master_profile",
            "profile": "delta X_N(r,t)=A_X(t) exp(-r/ell_X(t))/r + Q_X(t)/r + X_inf(t)",
            "amplitude_law": "A_X=A_src+A_bdy+A_top+A_proj+A_shell",
            "range_law": "ell_X=sqrt(D_X/M_X^2) for M_X^2>0; massless branch uses Q_X/r",
            "units_required": "A_X has X_N*length units; ell_X has length; Q_X has X_N*length units",
            "source_requirements": "parent L_X; D_X; M_X^2; source current J_X; boundary flux; topology; projector/calibration source",
            "status": "FIRST_PROFILE_AMPLITUDE_ROW_FILLED_NONCLAIM",
        },
        {
            **base,
            "row_id": "AMP3643_1_source_component",
            "profile": "A_src",
            "amplitude_law": "A_src ~ (1/(4*pi*D_X)) int_source e^{r'/ell_X} J_X^eff d^3x in spherical Green approximation",
            "range_law": "uses same ell_X as local operator",
            "units_required": "same as A_X after Green normalization",
            "source_requirements": "J_X^eff units, compact support, source geometry, Green normalization",
            "status": "MISSING_SOURCE_CURRENT_VALUE",
        },
        {
            **base,
            "row_id": "AMP3643_2_boundary_component",
            "profile": "A_bdy",
            "amplitude_law": "A_bdy set by exterior boundary flux n.D_X grad(delta X_N) and relative cohomology class",
            "range_law": "screened by exp(-d_boundary/ell_X) when ell_X finite",
            "units_required": "boundary flux converted to X_N*length",
            "source_requirements": "boundary class, no-flux theorem or flux value, domain distance d_boundary",
            "status": "MISSING_BOUNDARY_FLUX_VALUE",
        },
        {
            **base,
            "row_id": "AMP3643_3_time_component",
            "profile": "dot_A_X;dot_ell_X;dot_X_inf",
            "amplitude_law": "Xdot_N=dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf + projector/source-motion terms",
            "range_law": "time variation of ell_X contributes even if A_X is small",
            "units_required": "X_N per time; ell_X per time; yr^-1 projection for Gdot",
            "source_requirements": "stationarity theorem or numeric time-profile coefficients",
            "status": "MISSING_TIME_PROFILE_VALUES",
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
            "bound_id": "BU3643_0_gdot",
            "arena": "Gdot_clock",
            "updated_formula": "|beta_common| <= (9.0e-13 yr^-1 + |explicit_t residuals|)/|dot_A_X e^{-r/ell_X}/r + A_X e^{-r/ell_X} dot_ell_X/ell_X^2 + dot_X_inf + projector/source-motion|",
            "zero_route": "all time-profile coefficients vanish by parent stationarity theorem",
            "missing_inputs": "dot_A_X;dot_ell_X;dot_X_inf;projector/source-motion terms",
            "status": "BOUND_UPDATED_WITH_AMPLITUDE_ROW",
        },
        {
            **base,
            "bound_id": "BU3643_1_radial",
            "arena": "orbital_radial",
            "updated_formula": "partial_r X_N=-(1/r+1/ell_X) A_X e^{-r/ell_X}/r - Q_X/r^2; plug into beta_common radial hair bound",
            "zero_route": "A_X=Q_X=0 by no-hair theorem",
            "missing_inputs": "A_X;Q_X;ell_X;radial residual limit;explicit_r residuals",
            "status": "BOUND_UPDATED_WITH_AMPLITUDE_ROW",
        },
        {
            **base,
            "bound_id": "BU3643_2_ppn",
            "arena": "PPN_local_GR",
            "updated_formula": "gamma-1 = C_qgamma[S_beta(A_X,Q_X,ell_X)] beta_common^2 + C_grad partial_r X_N + retained channels",
            "zero_route": "A_X=Q_X=0 and scalar trace/leakage response zero by Ward-safe theorem",
            "missing_inputs": "S_beta amplitude map;C_qgamma norms;retained channels",
            "status": "BOUND_UPDATED_WITH_AMPLITUDE_ROW",
        },
        {
            **base,
            "bound_id": "BU3643_3_r10",
            "arena": "R10_short_range",
            "updated_formula": "ell_X is the candidate lambda_X; A_X controls support/profile factor in alpha_common(lambda)",
            "zero_route": "A_X=0 or ell_X outside sensitivity by theorem/source-backed range",
            "missing_inputs": "A_X;ell_X;K_X;M_X^2;tau_R10(lambda);alpha_bound(lambda)",
            "status": "BOUND_UPDATED_WITH_AMPLITUDE_ROW",
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
            "gate_id": "G3643_0_nohair_promotion",
            "gate": "No local no-hair/stationarity claim unless every premise is parent-signed.",
            "pass_condition": "operator ownership, coercivity, source silence, boundary no-flux, projector silence, stationarity, and topology certificate all pass",
            "status": "ENFORCED",
        },
        {
            **base,
            "gate_id": "G3643_1_amplitude_required",
            "gate": "If any premise is unsigned, carry A_X/ell_X/Q_X and time-profile coefficients explicitly.",
            "pass_condition": "finite profile rows have units, source premises, and links to Gdot/PPN/R10/radial bounds",
            "status": "ENFORCED",
        },
        {
            **base,
            "gate_id": "G3643_2_no_single_radius_calibration",
            "gate": "A single calibrated GM/radius cannot erase radial profile hair.",
            "pass_condition": "profile is theorem-zero for every exterior radius or bounded as a function of r/lambda",
            "status": "ENFORCED",
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "NOHAIR_THEOREM_CONDITIONAL_PROFILE_AMPLITUDE_ROWS_FILLED",
            "summary": "3643 attempts the local stationarity/no-hair proof. The coercive energy identity gives an exact theorem-zero route, but the live corpus does not parent-sign operator ownership, coercivity, source silence, boundary no-flux, projector silence, stationarity, and topology. Therefore the branch now carries explicit A_X, ell_X, Q_X, dot_A_X, dot_ell_X, and dot_X_inf rows into Gdot, radial/orbital, PPN, and R10 bounds.",
            "claim_ceiling": "no local-GR/Newton, no-hair, Gdot, radial, PPN, or R10 pass is allowed from 3643",
            "useful_result": "the profile gap has been reduced to named amplitude/range/time coefficients with source-owner requirements",
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3643_0",
            "target_doc": "3644-Y5-R2FR-profile-source-owner-or-first-amplitude-prior.md",
            "target_script": "scripts/Y5_R2FR_3644_profile_source_owner_or_first_amplitude_prior.py",
            "objective": "try to derive the source owner for A_src/A_bdy/A_proj/A_top and the operator coefficients D_X,M_X^2; if unsigned, fill first nonclaim prior-width rows for A_X and ell_X with units and explicit bound-channel links",
            "success_gate": "either A_X components are parent-zero/owned, or A_X and ell_X gain explicit source-owner/prior rows suitable for a future numeric smoke runner",
            "valid_for_claim": False,
        }
    ]


def write_doc(src, theorem, premises, amplitudes, bounds, gates, status, nxt) -> None:
    text = "\n\n".join(
        [
            "# 3643 Y5 R2FR local stationarity nohair or first profile amplitude row",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Theorem attempt",
            (
                "The clean no-hair route is real but conditional: if `L_X=(-D_X Delta_h+M_X^2)` is parent-owned and coercive, "
                "`J_X^eff=0`, boundary flux is zero, projector/calibration stress is silent, and there is no topological mode, then the energy identity forces `delta X_N=0`. "
                "That gives `A_X=Q_X=0`. Time silence additionally needs stationarity of the operator, source, boundary, and projector data."
            ),
            "## Live result",
            (
                "Those premises are not all parent-signed in the current corpus, so the branch cannot claim local no-hair. "
                "The fallback is now explicit: `A_X=A_src+A_bdy+A_top+A_proj+A_shell`, `ell_X=sqrt(D_X/M_X^2)`, and time coefficients "
                "`dot_A_X`, `dot_ell_X`, `dot_X_inf` feed the Gdot/radial/PPN/R10 bound rows."
            ),
            "## No-hair rows",
            "\n".join(f"- `{row['theorem_id']}`: {row['status']} — {row['mathematical_form']}" for row in theorem),
            "## Premise audit",
            "\n".join(f"- `{row['premise_id']}`: {row['status']} — {row['premise']}" for row in premises),
            "## Amplitude rows",
            "\n".join(f"- `{row['row_id']}`: {row['profile']} | {row['amplitude_law']} | {row['status']}" for row in amplitudes),
            "## Bound updates",
            "\n".join(f"- `{row['bound_id']}`: {row['arena']} — `{row['updated_formula']}`." for row in bounds),
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

    add("VAL3643_0_sources_exist", all(bool(row["exists"]) for row in src), "all source paths exist")
    add("VAL3643_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3643_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")
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
    add("VAL3643_3_csv_parse", parse_ok, "; ".join(details))

    theorem = read_csv(out["nohair_theorem_attempt"])
    premises = read_csv(out["premise_audit"])
    amplitudes = read_csv(out["amplitude_rows"])
    bounds = read_csv(out["bound_updates"])
    gates = read_csv(out["claim_gate"])
    status = read_csv(out["status"])
    nxt = read_csv(out["next_target"])

    add("VAL3643_4_energy_identity_present", any("int_Omega D_X" in row["mathematical_form"] for row in theorem), "coercive energy identity written")
    add("VAL3643_5_zero_conditional_not_promoted", any(row["status"] == "THEOREM_ZERO_CONDITIONAL_NOT_PARENT_SIGNED" for row in theorem), "zero hair remains conditional")
    required_premises = {"P3643_0_operator_owner", "P3643_1_coercivity", "P3643_2_source_silence", "P3643_3_boundary_no_flux", "P3643_4_projector_silence", "P3643_5_stationarity", "P3643_6_topology"}
    add("VAL3643_6_premise_audit_complete", required_premises.issubset({row["premise_id"] for row in premises}), "premise audit covers operator/source/boundary/projector/stationarity/topology")
    add("VAL3643_7_amplitude_master_row", any("A_X=A_src+A_bdy+A_top+A_proj+A_shell" in row["amplitude_law"] for row in amplitudes), "master amplitude decomposition present")
    add("VAL3643_8_time_coefficients_present", any("dot_A_X" in row["profile"] or "dot_A_X" in row["amplitude_law"] for row in amplitudes), "time profile coefficient row present")
    add("VAL3643_9_bounds_cover_arenas", {"Gdot_clock", "orbital_radial", "PPN_local_GR", "R10_short_range"}.issubset({row["arena"] for row in bounds}), "Gdot/radial/PPN/R10 bound updates present")
    add("VAL3643_10_claim_gates", any(row["gate_id"] == "G3643_0_nohair_promotion" for row in gates) and any(row["gate_id"] == "G3643_1_amplitude_required" for row in gates), "no-hair promotion and amplitude-required gates present")
    add("VAL3643_11_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in theorem + premises + amplitudes + bounds + gates + status + nxt), "all generated rows remain nonclaim")
    leak_patterns = [
        "*Y5_R2FR_3643*",
        "3643-Y5-R2FR-*",
        "Y5_R2FR_3643_*",
    ]
    leaks = []
    if FORMALIZATION.exists():
        for pattern in leak_patterns:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3643_12_no_formalization_leak", not leaks, "no 3643 files in formalization-workbench")
    add("VAL3643_13_next_target_written", bool(nxt) and "3644" in nxt[0]["target_doc"], "3644 source-owner/prior target written")
    add("VAL3643_14_doc_written", DOC.exists() and "A_X=A_src+A_bdy+A_top+A_proj+A_shell" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with amplitude law")
    add("VAL3643_15_status_honest", status[0]["status"] == "NOHAIR_THEOREM_CONDITIONAL_PROFILE_AMPLITUDE_ROWS_FILLED", "status keeps no-hair conditional and profile rows live")
    return rows


def main() -> None:
    t = now()
    out = outputs()
    src = source_rows(t)
    theorem = nohair_rows(t)
    premises = premise_rows(t)
    amplitudes = amplitude_rows(t)
    bounds = bound_update_rows(t)
    gates = claim_gate_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)

    write_csv(out["source_register"], src)
    write_csv(out["nohair_theorem_attempt"], theorem)
    write_csv(out["premise_audit"], premises)
    write_csv(out["amplitude_rows"], amplitudes)
    write_csv(out["bound_updates"], bounds)
    write_csv(out["claim_gate"], gates)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, theorem, premises, amplitudes, bounds, gates, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3643 validation failed: {failures}")
    print(f"wrote 3643 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
