from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3640"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_SOURCE_NORMALIZATION_WARD_OR_BETA_COMMON_BOUND_FILL_3640"
DOC = ROOT / "3640-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md"


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


def paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3640_SOURCE_REGISTER.csv",
        "ward_derivation": RESIDUALS / "P8_Y5_R2FR_3640_WARD_IDENTITY_DERIVATION.csv",
        "residual_decomposition": RESIDUALS / "P8_Y5_R2FR_3640_BETA_COMMON_WARD_RESIDUAL_DECOMPOSITION.csv",
        "bound_inversion": RESIDUALS / "P8_Y5_R2FR_3640_BETA_COMMON_BOUND_INVERSION_ROWS.csv",
        "claim_gate": RESIDUALS / "P8_Y5_R2FR_3640_CLAIM_GATE.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3640_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3640_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3640_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    specs = [
        ("next_3639", RESIDUALS / "P8_Y5_R2FR_3639_NEXT_TARGET.csv", "Ward/source-normalization identity", "handoff selecting parent Ward/source-normalization target"),
        ("proof_3639", RESIDUALS / "P8_Y5_R2FR_3639_COMMON_BETA_ZERO_PROOF_AUDIT.csv", "CONDITIONAL_ZERO_NOT_PARENT_SIGNED", "prior conditional zero route"),
        ("identity_3639", RESIDUALS / "P8_Y5_R2FR_3639_COMMON_BETA_IDENTITY.csv", "beta_common = X_N[ln mu_obs_common]", "common beta exact identity"),
        ("observables_3639", RESIDUALS / "P8_Y5_R2FR_3639_COMMON_BETA_OBSERVABLE_ROWS.csv", "R10_short_range", "arena maps to inherit"),
        ("source_runner_3639", RESIDUALS / "P8_Y5_R2FR_3639_SOURCE_NORMALIZATION_RUNNER_ROWS.csv", "NO_TUNED_CANCELLATION_ALLOWED", "no tuned cancellation policy"),
        ("constant_gm_gate", RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM0_master_identity", "measured-GM derivative master identity"),
        ("global_superselection", RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv", "GS7_scalar_branch_fallback", "global coupling scalar fallback"),
        ("species_contract", RESIDUALS / "P8_no_species_source_charge_CONTRACT.csv", "S4_source_normalization_species_blind", "source-normalization species-blind contract"),
        ("frame_marker_1028", ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md", "tau_R10", "prior arena timescale/input pack"),
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


def ward_derivation_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "step_id": "W3640_0_parent_variation",
            "object": "S_parent[Phi,psi]",
            "equation": "delta_X S_parent = integral(E_Phi delta_X Phi + E_psi delta_X psi) + integral_boundary Theta(Phi,delta_X Phi) + delta_X S_source + delta_X S_counterterm",
            "zero_condition": "X_N is a parent gauge/vertical generator and the action, measure, coframe, connection, matter source term, and counterterms descend through q",
            "derived_result": "on shell, delta_X S_parent reduces to the boundary/source-normalization Ward charge",
            "status": "DERIVED_VARIATION_FORM",
        },
        {
            **base,
            "step_id": "W3640_1_noether_charge",
            "object": "source normalization charge Q_mu",
            "equation": "delta_X Q_mu = delta_X Q_boundary + delta_X Q_source + delta_X Q_projection + delta_X Q_calibration",
            "zero_condition": "boundary silence, source-current descent, projector descent, and calibration gauge invariance",
            "derived_result": "if all four terms vanish, X_N ln mu_obs_common = 0",
            "status": "CONDITIONAL_WARD_ZERO",
        },
        {
            **base,
            "step_id": "W3640_2_beta_common_identity",
            "object": "beta_common",
            "equation": "beta_common = X_N ln mu_obs_common = beta_q + beta_boundary + beta_source + beta_projection + beta_calibration",
            "zero_condition": "beta_q=beta_boundary=beta_source=beta_projection=beta_calibration=0 by parent identity",
            "derived_result": "the old single missing coupling is decomposed into five independently auditable Ward residuals",
            "status": "EXACT_RESIDUAL_SPLIT",
        },
        {
            **base,
            "step_id": "W3640_3_newton_gr_reduction_gate",
            "object": "local Newton/GR source",
            "equation": "mu_obs(r,t,A) = constant_mu + O(beta_common residuals); local GR/Newton source limit requires d_t mu_obs = d_r mu_obs = Delta_A mu_obs = alpha_common(lambda) = PPN_common = 0 or below bounds",
            "zero_condition": "same parent Ward identity must kill every local derivative/projection, not just WEP differences",
            "derived_result": "this is the clean local-GR/Newton gate: calibrated source coupling must be a quotient/gauge charge or a bounded physical residual",
            "status": "LOCAL_GR_NEWTON_GATE_SHARPENED",
        },
        {
            **base,
            "step_id": "W3640_4_verdict",
            "object": "parent corpus",
            "equation": "current evidence signs the algebraic Ward form, not the parent zero of all residual pieces",
            "zero_condition": "needs signed parent source-normalization Ward theorem or filled arena bounds",
            "derived_result": "beta_common=0 remains unclaimed; bound-inversion rows are filled for the live branch",
            "status": "WARD_ZERO_UNSIGNED_BOUND_INVERSION_REQUIRED",
        },
    ]


def residual_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    rows = [
        ("beta_q", "X_N ln mu_bar(q(Phi))", "quotient ownership of measured source normalization", "zero if mu_obs_common=mu_bar(q(Phi)) and Dq(X_N)=0"),
        ("beta_boundary", "X_N ln Q_boundary", "asymptotic/boundary charge silence", "zero if boundary charge is invariant under X_N"),
        ("beta_source", "X_N ln Q_source", "matter/source current descent", "zero if active source current has no X_N representative dependence"),
        ("beta_projection", "X_N ln Q_projection", "projector/readout descent", "zero if local-to-observable projector commutes with quotient map"),
        ("beta_calibration", "X_N ln Q_calibration", "unit/calibration gauge", "zero if common scale shift is pure convention with no observable derivatives"),
    ]
    return [
        {
            **base,
            "residual_id": f"BR3640_{i}_{symbol}",
            "symbol": symbol,
            "definition": definition,
            "parent_signature_needed": signature,
            "zero_rule": zero_rule,
            "master_sum": "beta_common = beta_q + beta_boundary + beta_source + beta_projection + beta_calibration",
            "status": "ZERO_REQUIRED_OR_BOUND",
        }
        for i, (symbol, definition, signature, zero_rule) in enumerate(rows)
    ]


def bound_rows(t: str) -> list[dict[str, object]]:
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
            "prediction": "alpha_common(lambda)=K_X beta_S beta_T tau_R10(lambda)/M_X^2",
            "inverted_beta_bound": "|beta_common| <= sqrt(|alpha_bound(lambda)| M_X^2/(|K_X tau_R10(lambda)|)) for beta_S=beta_T=beta_common",
            "needed_numeric_inputs": "alpha_bound(lambda);K_X;M_X^2;tau_R10(lambda);source/test normalization convention",
            "status": "BOUND_FORMULA_FILLED_INPUTS_MISSING",
        },
        {
            **base,
            "arena": "PPN_local_GR",
            "observable": "Delta_PPN_common",
            "prediction": "Delta_PPN_common = C_PPN beta_common^2 + C'_PPN grad(beta_common) + higher_order",
            "inverted_beta_bound": "|beta_common| <= sqrt(|Delta_PPN_limit|/|C_PPN|) when derivative terms vanish or are separately bounded",
            "needed_numeric_inputs": "C_PPN;Delta_PPN_limit;local derivative map;PPN gauge projection",
            "status": "BOUND_FORMULA_FILLED_INPUTS_MISSING",
        },
        {
            **base,
            "arena": "Gdot_clock",
            "observable": "d ln mu_obs/dt",
            "prediction": "d ln mu_obs/dt = beta_common Xdot_N + explicit_t residuals",
            "inverted_beta_bound": "|beta_common| <= (|dln_mu_dt|_limit + |explicit_t residuals|)/|Xdot_N|",
            "needed_numeric_inputs": "Xdot_N;clock/ephemeris dln_mu_dt limit;explicit_t residual estimate",
            "status": "BOUND_FORMULA_FILLED_INPUTS_MISSING",
        },
        {
            **base,
            "arena": "orbital_radial",
            "observable": "partial_r ln mu_obs",
            "prediction": "partial_r ln mu_obs = beta_common partial_r X_N + explicit_r residuals",
            "inverted_beta_bound": "|beta_common| <= (|partial_r ln mu|_limit + |explicit_r residuals|)/|partial_r X_N|",
            "needed_numeric_inputs": "partial_r X_N;orbital/range residual bound;source boundary condition;calibration radius",
            "status": "BOUND_FORMULA_FILLED_INPUTS_MISSING",
        },
        {
            **base,
            "arena": "source_WEP_null_guard",
            "observable": "eta_source_AB",
            "prediction": "eta_source_AB depends on Delta beta_AB and is blind to beta_common",
            "inverted_beta_bound": "no beta_common bound follows from differential eta alone",
            "needed_numeric_inputs": "none for guard; use R10/PPN/Gdot/radial instead",
            "status": "NO_BOUND_FROM_WEP_COMMON_MODE",
        },
        {
            **base,
            "arena": "clock_common_mode",
            "observable": "clock common drift",
            "prediction": "Delta nu/nu common = S_mu beta_common Xdot_N + S_alpha b_alpha Xdot_N + ...",
            "inverted_beta_bound": "|beta_common| <= (|clock_common_limit| + non_mu_terms)/|S_mu Xdot_N|",
            "needed_numeric_inputs": "clock sensitivity S_mu;Xdot_N;non_mu terms;clock dataset convention",
            "status": "BOUND_FORMULA_FILLED_INPUTS_MISSING",
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
            "gate_id": "G3640_0_no_axiom",
            "gate": "beta_common=0 may not be asserted as a plateau/closure axiom",
            "pass_condition": "signed parent Ward identity or numeric bound pass in every local arena",
            "status": "ENFORCED",
        },
        {
            **base,
            "gate_id": "G3640_1_termwise_or_identity",
            "gate": "beta_q + beta_boundary + beta_source + beta_projection + beta_calibration cannot be cancelled by tuning",
            "pass_condition": "each term is zero by descent/silence, or the full sum is zero by an explicit Noether/Ward identity",
            "status": "ENFORCED",
        },
        {
            **base,
            "gate_id": "G3640_2_local_gr_newton",
            "gate": "local GR/Newton source recovery requires source-normalization silence, not only WEP silence",
            "pass_condition": "R10/PPN/Gdot/radial/clock all pass or beta_common is parent-zero",
            "status": "ACTIVE",
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "WARD_FORM_DERIVED_PARENT_ZERO_UNSIGNED_BETA_COMMON_BOUNDS_FILLED",
            "summary": "3640 derives the parent Ward/source-normalization form for beta_common and splits the residual into beta_q, beta_boundary, beta_source, beta_projection, and beta_calibration. The parent-zero theorem is still unsigned, but the live branch now has explicit inverted bound formulas for R10, PPN, Gdot/clock, radial/orbital, source-WEP null guard, and clock common-mode channels.",
            "claim_ceiling": "no local-GR/Newton, PPN, R10, Gdot, clock, or source-normalization pass is allowed from 3640",
            "useful_result": "the coupling problem is now a five-term Ward residual plus arena-bound inequalities, not an undefined missing coefficient",
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3640_0",
            "target_doc": "3641-Y5-R2FR-beta-bound-input-prioritizer-and-first-numeric-fill.md",
            "target_script": "scripts/Y5_R2FR_3641_beta_bound_input_prioritizer_and_first_numeric_fill.py",
            "objective": "prioritize which beta_common arena can be numerically constrained first, then fill the easiest real bound inputs without claiming a pass: likely Gdot/clock or R10 depending on available local coefficients and public bounds",
            "success_gate": "at least one beta_common bound row gains sourced numeric limit inputs while parent coefficients remain explicit and nonclaim, or a stronger parent Ward signature is found",
            "valid_for_claim": False,
        }
    ]


def write_doc(src, ward, residuals, bounds, gates, status, nxt) -> None:
    text = "\n\n".join(
        [
            "# 3640 Y5 R2FR parent source-normalization Ward identity or beta common bound fill",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Actual derivation",
            (
                "Vary the parent action along the normalized common source direction `X_N`. On shell, the bulk Euler terms "
                "drop out, leaving a boundary/source/readout/calibration Ward charge. Therefore the exact local source "
                "coupling is not a single mystery number but"
            ),
            "`beta_common = X_N ln mu_obs_common = beta_q + beta_boundary + beta_source + beta_projection + beta_calibration`.",
            (
                "If `X_N` is a genuine parent gauge/vertical generator, `mu_obs_common` descends through `q`, and the boundary, "
                "source current, projector, and calibration charge are silent, then the Ward identity gives `beta_common=0`. "
                "That would be the clean local-GR/Newton route: calibrated source strength is a quotient/gauge charge."
            ),
            "## Why it is not claimed yet",
            (
                "The corpus signs the algebraic form of the route but not the parent zero of all five residual pieces. "
                "So `beta_common=0` remains unclaimed. No WEP result can close it, because common-mode coupling lies in the WEP null direction."
            ),
            "## Ward derivation rows",
            "\n".join(f"- `{row['step_id']}`: {row['status']} — {row['equation']}" for row in ward),
            "## Residual pieces",
            "\n".join(f"- `{row['symbol']}`: {row['definition']} | zero rule: {row['zero_rule']}" for row in residuals),
            "## Bound inversions",
            "\n".join(f"- `{row['arena']}`: `{row['inverted_beta_bound']}`." for row in bounds),
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

    add("VAL3640_0_sources_exist", all(bool(row["exists"]) for row in src), "all source paths exist")
    add("VAL3640_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3640_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")
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
    add("VAL3640_3_csv_parse", parse_ok, "; ".join(details))

    ward = read_csv(out["ward_derivation"])
    residuals = read_csv(out["residual_decomposition"])
    bounds = read_csv(out["bound_inversion"])
    gates = read_csv(out["claim_gate"])
    status = read_csv(out["status"])
    nxt = read_csv(out["next_target"])

    add("VAL3640_4_ward_form_derived", any("delta_X S_parent" in row["equation"] for row in ward), "parent action variation written")
    add("VAL3640_5_residual_split_present", {"beta_q", "beta_boundary", "beta_source", "beta_projection", "beta_calibration"}.issubset({row["symbol"] for row in residuals}), "five-term beta residual split present")
    add("VAL3640_6_bounds_cover_arenas", {"R10_short_range", "PPN_local_GR", "Gdot_clock", "orbital_radial", "source_WEP_null_guard", "clock_common_mode"}.issubset({row["arena"] for row in bounds}), "bound inversion rows cover required arenas")
    add("VAL3640_7_no_axiom_gate", any(row["gate_id"] == "G3640_0_no_axiom" and row["status"] == "ENFORCED" for row in gates), "no plateau/closure axiom gate enforced")
    add("VAL3640_8_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in ward + residuals + bounds + gates + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3640*")) if FORMALIZATION.exists() else []
    add("VAL3640_9_no_formalization_leak", not leaks, "no 3640 files in formalization-workbench")
    add("VAL3640_10_next_target_written", bool(nxt) and "3641" in nxt[0]["target_doc"], "3641 numeric/prioritizer target written")
    add("VAL3640_11_doc_written", DOC.exists() and "beta_common = X_N ln mu_obs_common" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with Ward identity")
    add("VAL3640_12_status_honest", status[0]["status"] == "WARD_FORM_DERIVED_PARENT_ZERO_UNSIGNED_BETA_COMMON_BOUNDS_FILLED", "status keeps parent zero unsigned")
    return rows


def main() -> None:
    t = now()
    out = paths()
    src = source_rows(t)
    ward = ward_derivation_rows(t)
    residuals = residual_rows(t)
    bounds = bound_rows(t)
    gates = claim_gate_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)

    write_csv(out["source_register"], src)
    write_csv(out["ward_derivation"], ward)
    write_csv(out["residual_decomposition"], residuals)
    write_csv(out["bound_inversion"], bounds)
    write_csv(out["claim_gate"], gates)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, ward, residuals, bounds, gates, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3640 validation failed: {failures}")
    print(f"wrote 3640 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
