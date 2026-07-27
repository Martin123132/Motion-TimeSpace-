from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3639"
BRANCH_ID = "MTS_R2FR_Y5_COMMON_BETA_ZERO_OR_SOURCE_NORMALIZATION_RUNNER_3639"
DOC = ROOT / "3639-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md"


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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3639_SOURCE_REGISTER.csv",
        "proof_audit": RESIDUALS / "P8_Y5_R2FR_3639_COMMON_BETA_ZERO_PROOF_AUDIT.csv",
        "identity": RESIDUALS / "P8_Y5_R2FR_3639_COMMON_BETA_IDENTITY.csv",
        "observable_rows": RESIDUALS / "P8_Y5_R2FR_3639_COMMON_BETA_OBSERVABLE_ROWS.csv",
        "source_normalization_rows": RESIDUALS / "P8_Y5_R2FR_3639_SOURCE_NORMALIZATION_RUNNER_ROWS.csv",
        "decision": RESIDUALS / "P8_Y5_R2FR_3639_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3639_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3639_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3639_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3638", RESIDUALS / "P8_Y5_R2FR_3638_NEXT_TARGET.csv", "beta_common=0", "3638 selected common beta zero/source-normalization as the next target."),
        ("component_pack_3638", RESIDUALS / "P8_Y5_R2FR_3638_BETAX_COMPONENT_PACK.csv", "COMMON_MODE_ACTIVE_NOT_WEP_ERASED", "3638 beta component pack exposes common beta."),
        ("eta_update_3638", RESIDUALS / "P8_Y5_R2FR_3638_ETA_SOURCE_AB_COMPONENT_UPDATE.csv", "beta_common still bypasses", "3638 explains why differential eta does not erase common beta."),
        ("constant_gm_gate", RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM0_master_identity", "master measured-GM derivative identity."),
        ("constant_gm_species", RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM3_species_source_charge", "species/source charge row separated from common-mode rows."),
        ("global_superselection", RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv", "GS7_scalar_branch_fallback", "global coupling can fall back to executable scalar residual branch."),
        ("no_species_contract", RESIDUALS / "P8_no_species_source_charge_CONTRACT.csv", "S4_source_normalization_species_blind", "source normalization species-blind contract."),
        ("source_bound_1027", ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md", "Claim ceiling", "prior source-zero or bounded-coupling checkpoint."),
        ("frame_marker_1028", ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md", "tau_R10", "prior frame/marker input pack with arena timescales."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        rows.append(
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
        )
    return rows


def proof_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    rows = [
        {
            **base,
            "proof_id": "CB3639_0_definition",
            "claim": "beta_common := X_N[ln mu_obs] for the species-blind part of mu_obs.",
            "derived_relation": "beta_X^A = beta_common + delta_beta_A and Delta beta_X_AB = delta_beta_A - delta_beta_B.",
            "closure_condition": "none; this is a definition inherited from 3638.",
            "status": "DERIVED_IDENTITY",
            "why_not_closed": "definition alone does not set beta_common to zero.",
        },
        {
            **base,
            "proof_id": "CB3639_1_quotient_zero_route",
            "claim": "If mu_obs = mu_bar(q(Phi)) and X_N in ker(Dq), then beta_common = X_N[ln mu_bar(q(Phi))] = 0.",
            "derived_relation": "X_N[ln mu_obs] = D ln(mu_bar)[Dq(X_N)] = 0.",
            "closure_condition": "parent signs mu_obs as quotient-owned q-data and X_N as vertical to that q-map.",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "why_not_closed": "3638/CGM rows retain measured-GM/source-normalization derivatives as live residuals.",
        },
        {
            **base,
            "proof_id": "CB3639_2_unit_gauge_route",
            "claim": "A common source scaling is unobservable only if it is pure calibration gauge.",
            "derived_relation": "delta ln G_eff + delta ln M_eff + delta ln(1+epsilon_mu) = 0 as a parent Ward/gauge identity.",
            "closure_condition": "parent action supplies a scale/gauge Noether identity, not a fitted cancellation.",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "why_not_closed": "GS6 warns that absolute G normalization is calibration-only, but derivatives need a theorem.",
        },
        {
            **base,
            "proof_id": "CB3639_3_scalar_tensor_guard",
            "claim": "Universal coupling can pass WEP but still fail PPN/R10/Gdot.",
            "derived_relation": "species-blind beta_common cancels from Delta beta_AB, but beta_common^2 contributes to finite-range/PPN/common-source channels.",
            "closure_condition": "beta_common = 0, infinite mass/range suppression, or numeric bound rows.",
            "status": "COMMON_MODE_NOT_WEP_ERASED",
            "why_not_closed": "differential WEP is the wrong lock for a universal source coupling.",
        },
        {
            **base,
            "proof_id": "CB3639_4_verdict",
            "claim": "The common-beta zero proof cannot be claimed from the current parent corpus.",
            "derived_relation": "beta_common remains a source-normalization residual with exact observable maps.",
            "closure_condition": "3640 must either sign the quotient/unit-gauge Ward identity or fill numeric arena bounds.",
            "status": "ZERO_PROOF_UNSIGNED_OBSERVABLE_RUNNER_FILLED",
            "why_not_closed": "the route is sharpened into a theorem contract, but the required parent signature is still absent.",
        },
    ]
    return rows


def identity_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "identity_id": "ID3639_0_master_common_beta",
            "symbol": "beta_common",
            "identity": "beta_common = X_N[ln mu_obs_common] = X_N[ln G_eff] + X_N[ln M_eff] + X_N[ln(1+epsilon_mu)]",
            "units": "dimensionless per normalized X_N",
            "observable_link": "source_normalization;R10;PPN;Gdot;radial_source_hair;clock_common_mode",
            "status": "EXACT_DECOMPOSITION_NO_ZERO_CLAIM",
        },
        {
            **base,
            "identity_id": "ID3639_1_time_projection",
            "symbol": "dot_mu_over_mu",
            "identity": "d ln mu_obs_common/dt = beta_common * dX_N/dt + explicit_t[ln G_eff M_eff(1+epsilon_mu)]",
            "units": "time^-1",
            "observable_link": "Gdot;clock_common_mode;ephemeris",
            "status": "REQUIRES_XDOT_OR_PARENT_ZERO",
        },
        {
            **base,
            "identity_id": "ID3639_2_radial_projection",
            "symbol": "partial_r_ln_mu",
            "identity": "partial_r ln mu_obs_common = beta_common * partial_r X_N + explicit_r[ln G_eff M_eff(1+epsilon_mu)]",
            "units": "length^-1",
            "observable_link": "orbital;inverse_square;R10_range",
            "status": "REQUIRES_PROFILE_OR_PARENT_ZERO",
        },
        {
            **base,
            "identity_id": "ID3639_3_wEP_null_space",
            "symbol": "eta_source_AB",
            "identity": "eta_source_AB sees Delta beta_AB, not beta_common; beta_common lies in the WEP null direction.",
            "units": "dimensionless",
            "observable_link": "WEP_guard",
            "status": "WEP_CANNOT_CLOSE_COMMON_MODE",
        },
    ]


def observable_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "arena": "R10_short_range",
            "observable": "alpha_common(lambda)",
            "prediction_skeleton": "alpha_common(lambda) = K_X * beta_common_source * beta_common_test * tau_R10(lambda) / M_X^2",
            "pass_condition": "for every lambda: |alpha_common(lambda)| <= alpha_bound(lambda), or beta_common=0 by theorem",
            "needed_inputs": "K_X;M_X^2;tau_R10(lambda);beta_common_source;beta_common_test;real alpha_bound(lambda)",
            "status": "NONCLAIM_SYMBOLIC_MAP_FILLED",
        },
        {
            **base,
            "arena": "PPN_local_GR",
            "observable": "PPN_residual_vector_common",
            "prediction_skeleton": "Delta_PPN_common ~ (gamma-1, beta_PPN-1, alpha_i, zeta_i) sourced at leading order by beta_common^2 and derivatives of beta_common",
            "pass_condition": "PPN vector below bounds or parent theorem beta_common=0 in local vacuum/source-normalized branch",
            "needed_inputs": "local propagator normalization; beta_common local value; derivative beta'_common; mapping to standard PPN gauge",
            "status": "NONCLAIM_PPN_MAP_FILLED",
        },
        {
            **base,
            "arena": "Gdot_clock",
            "observable": "dln_mu_obs_dt",
            "prediction_skeleton": "dln_mu_obs_dt = beta_common * Xdot_N + explicit_t residuals",
            "pass_condition": "absolute drift below clock/ephemeris bounds or parent time-superselection theorem",
            "needed_inputs": "Xdot_N local; clock sensitivity map; ephemeris convention; source mass standard",
            "status": "NONCLAIM_DRIFT_MAP_FILLED",
        },
        {
            **base,
            "arena": "orbital_radial",
            "observable": "radial_source_hair",
            "prediction_skeleton": "a_r = -mu_obs(r)/r^2 with partial_r ln mu_obs = beta_common partial_r X_N + explicit_r residuals",
            "pass_condition": "no radial profile outside compact support or profile below orbital residual bounds",
            "needed_inputs": "X_N(r);source boundary condition;orbital residual covariance;calibrated mu at reference radius",
            "status": "NONCLAIM_RADIAL_MAP_FILLED",
        },
        {
            **base,
            "arena": "source_normalization",
            "observable": "calibration_null_or_physical_beta",
            "prediction_skeleton": "beta_common is gauge only if delta ln mu_obs_common is a parent-owned calibration transformation with zero derivatives in observables",
            "pass_condition": "signed Ward/superselection identity or explicit residual branch",
            "needed_inputs": "parent scale symmetry;measure/coframe descent;boundary silence;calibration convention",
            "status": "THEOREM_CONTRACT_NOT_SIGNED",
        },
    ]


def source_normalization_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "runner_id": "SNR3639_0_calibrated_mu",
            "target": "mu_obs_common",
            "equation": "mu_obs_common := G_eff M_eff(1+epsilon_mu)",
            "zero_route": "X_N[mu_obs_common]=0 because mu_obs_common descends through q or is pure calibration gauge",
            "failure_route": "retain beta_common and project to R10/PPN/Gdot/radial rows",
            "required_parent_signature": "q owns measured source normalization; no hidden boundary/projector source term",
            "status": "ACTIVE_FORK",
        },
        {
            **base,
            "runner_id": "SNR3639_1_no_cancellation",
            "target": "beta_common_zero",
            "equation": "X_N ln G_eff + X_N ln M_eff + X_N ln(1+epsilon_mu) = 0",
            "zero_route": "accepted only if a Ward identity forces the sum to vanish termwise or as a symmetry identity",
            "failure_route": "ordinary cancellation between terms is tuning and not claim-valid",
            "required_parent_signature": "scale/source-normalization Noether identity with units and boundary terms",
            "status": "NO_TUNED_CANCELLATION_ALLOWED",
        },
        {
            **base,
            "runner_id": "SNR3639_2_common_wEP_guard",
            "target": "WEP_null_direction",
            "equation": "Delta beta_AB = 0 while beta_common != 0 is allowed",
            "zero_route": "not available from differential WEP alone",
            "failure_route": "common mode must be tested by R10/PPN/Gdot/radial channels",
            "required_parent_signature": "independent common source-current silence theorem",
            "status": "WEP_NOT_SUFFICIENT",
        },
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "decision_id": "DEC3639_0_zero_not_claimed",
            "decision": "Do not claim beta_common=0 from the current corpus.",
            "reason": "the quotient and unit-gauge routes are exact but unsigned.",
            "status": "ZERO_PROOF_UNSIGNED",
        },
        {
            **base,
            "decision_id": "DEC3639_1_runner_filled",
            "decision": "Keep beta_common as a source-normalization residual with explicit arena equations.",
            "reason": "this converts a hidden coupling into testable R10/PPN/Gdot/radial rows.",
            "status": "OBSERVABLE_RUNNER_FILLED",
        },
        {
            **base,
            "decision_id": "DEC3639_2_next",
            "decision": "Next target is the parent source-normalization Ward identity.",
            "reason": "this is the cleanest route to local GR/Newton without using WEP as a proxy.",
            "status": "WARD_IDENTITY_NEXT",
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "COMMON_BETA_ZERO_UNSIGNED_SOURCE_NORMALIZATION_RUNNER_FILLED",
            "summary": "3639 tried the common-beta zero proof. The exact quotient route and pure-calibration route are now written, but neither is parent-signed, so beta_common remains live. The useful advance is that beta_common is no longer a vague missing coupling: it is mapped into R10, PPN, Gdot/clock, radial/orbital, and source-normalization equations.",
            "claim_ceiling": "no local-GR/Newton, PPN, R10, Gdot, clock, or source-normalization pass is allowed from 3639",
            "next_pressure_point": "derive the parent Ward/source-normalization identity forcing X_N ln mu_obs_common = 0, or fill numeric beta_common bounds",
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3639_0",
            "target_doc": "3640-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_3640_parent_source_normalization_ward_identity_or_beta_common_bound_fill.py",
            "objective": "attempt to derive the Ward/source-normalization identity X_N ln mu_obs_common = 0 from the parent action, including measure, coframe, connection, boundary, and calibration terms; if unsigned, fill numeric/symbolic beta_common bound rows for R10, PPN, Gdot, radial/orbital, and clock arenas",
            "success_gate": "either beta_common=0 is parent-signed, or every arena has an explicit nonclaim beta_common row with units, source paths, required coefficients, and bound inputs",
            "valid_for_claim": False,
        }
    ]


def write_doc(src, proof, identity, observables, source_norm, decisions, status, nxt) -> None:
    text = "\n\n".join(
        [
            "# 3639 Y5 R2FR common beta zero or source normalization runner",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Main result",
            (
                "The useful theorem is conditional and exact: if `mu_obs_common = mu_bar(q(Phi))` and `X_N in ker(Dq)`, "
                "then `beta_common = X_N[ln mu_obs_common] = 0`. A second exact route exists if a parent scale/source "
                "Ward identity makes `delta ln G_eff + delta ln M_eff + delta ln(1+epsilon_mu) = 0` as a symmetry, not a tune."
            ),
            (
                "The current parent corpus does not sign either route. Therefore `beta_common` stays live, but it has been "
                "moved out of the fog: it now has explicit R10, PPN, Gdot/clock, radial/orbital, and source-normalization maps."
            ),
            "## Exact identity",
            "\n".join(f"- `{row['symbol']}`: {row['identity']} [{row['status']}]" for row in identity),
            "## Proof audit",
            "\n".join(f"- `{row['proof_id']}`: {row['status']} — {row['claim']}" for row in proof),
            "## Observable maps",
            "\n".join(f"- `{row['arena']}`: `{row['observable']}` via `{row['prediction_skeleton']}`." for row in observables),
            "## Source-normalization runner",
            "\n".join(f"- `{row['runner_id']}`: {row['status']} — {row['equation']}" for row in source_norm),
            "## Decision",
            "\n".join(f"- `{row['decision_id']}`: {row['status']} — {row['decision']}" for row in decisions),
            "## Next target",
            f"`{nxt[0]['target_doc']}` via `{nxt[0]['target_script']}`.",
            "## Sources",
            "\n".join(f"- `{row['source_id']}`: `{row['local_path']}` exists={row['exists']} needle_found={row['needle_found']}" for row in src),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(paths: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
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

    add("VAL3639_0_sources_exist", all(bool(row["exists"]) for row in src), "all source paths exist")
    add("VAL3639_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in paths.items() if name != "validation"}
    add("VAL3639_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")
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
    add("VAL3639_3_csv_parse", parse_ok, "; ".join(details))

    proof = read_csv(paths["proof_audit"])
    identity = read_csv(paths["identity"])
    observables = read_csv(paths["observable_rows"])
    source_norm = read_csv(paths["source_normalization_rows"])
    decisions = read_csv(paths["decision"])
    status = read_csv(paths["status"])
    nxt = read_csv(paths["next_target"])

    add("VAL3639_4_conditional_zero_written", any("Dq(X_N)" in row["derived_relation"] and row["status"] == "CONDITIONAL_ZERO_NOT_PARENT_SIGNED" for row in proof), "quotient zero route written but not promoted")
    add("VAL3639_5_common_beta_identity", any(row["symbol"] == "beta_common" and "X_N[ln G_eff]" in row["identity"] for row in identity), "common beta decomposition present")
    arenas = {row["arena"] for row in observables}
    add("VAL3639_6_observable_arenas", {"R10_short_range", "PPN_local_GR", "Gdot_clock", "orbital_radial", "source_normalization"}.issubset(arenas), "all common-beta arenas mapped")
    add("VAL3639_7_wEP_null_guard", any(row["status"] == "WEP_NOT_SUFFICIENT" for row in source_norm), "WEP null direction guard present")
    add("VAL3639_8_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in proof + identity + observables + source_norm + decisions + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3639*")) if FORMALIZATION.exists() else []
    add("VAL3639_9_no_formalization_leak", not leaks, "no 3639 files in formalization-workbench")
    add("VAL3639_10_next_target_written", bool(nxt) and "3640" in nxt[0]["target_doc"], "3640 Ward/source-normalization target written")
    add("VAL3639_11_doc_written", DOC.exists() and "beta_common" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written")
    add("VAL3639_12_status_honest", status[0]["status"] == "COMMON_BETA_ZERO_UNSIGNED_SOURCE_NORMALIZATION_RUNNER_FILLED", "status keeps zero proof unsigned")
    return rows


def main() -> None:
    t = now()
    paths = outputs()
    src = source_rows(t)
    proof = proof_rows(t)
    identity = identity_rows(t)
    observables = observable_rows(t)
    source_norm = source_normalization_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)

    write_csv(paths["source_register"], src)
    write_csv(paths["proof_audit"], proof)
    write_csv(paths["identity"], identity)
    write_csv(paths["observable_rows"], observables)
    write_csv(paths["source_normalization_rows"], source_norm)
    write_csv(paths["decision"], decisions)
    write_csv(paths["status"], status)
    write_csv(paths["next_target"], nxt)
    write_doc(src, proof, identity, observables, source_norm, decisions, status, nxt)

    validation = validate(paths, src)
    write_csv(paths["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3639 validation failed: {failures}")
    print(f"wrote 3639 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
