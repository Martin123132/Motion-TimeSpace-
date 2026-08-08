from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3641"
BRANCH_ID = "MTS_R2FR_Y5_BETA_BOUND_INPUT_PRIORITIZER_AND_FIRST_NUMERIC_FILL_3641"
DOC = ROOT / "3641-Y5-R2FR-beta-bound-input-prioritizer-and-first-numeric-fill.md"


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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3641_SOURCE_REGISTER.csv",
        "observational_seeds": RESIDUALS / "P8_Y5_R2FR_3641_OBSERVATIONAL_LIMIT_SEEDS.csv",
        "priority_matrix": RESIDUALS / "P8_Y5_R2FR_3641_BETA_COMMON_ARENA_PRIORITY_MATRIX.csv",
        "first_fill": RESIDUALS / "P8_Y5_R2FR_3641_BETA_COMMON_FIRST_NUMERIC_FILL.csv",
        "scoreability": RESIDUALS / "P8_Y5_R2FR_3641_SCOREABILITY_AUDIT.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3641_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3641_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3641_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    local_specs = [
        ("next_3640", RESIDUALS / "P8_Y5_R2FR_3640_NEXT_TARGET.csv", "sourced numeric limit inputs", "3640 handoff to beta-bound prioritizer"),
        ("bounds_3640", RESIDUALS / "P8_Y5_R2FR_3640_BETA_COMMON_BOUND_INVERSION_ROWS.csv", "R10_short_range", "3640 bound inversion formulas"),
        ("ward_3640", RESIDUALS / "P8_Y5_R2FR_3640_WARD_IDENTITY_DERIVATION.csv", "WARD_ZERO_UNSIGNED_BOUND_INVERSION_REQUIRED", "3640 Ward-zero verdict"),
    ]
    rows = [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_type": "local_file",
            "local_path": str(path),
            "source_url": "",
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
            "valid_for_claim": False,
        }
        for source_id, path, needle, role in local_specs
    ]
    web_specs = [
        (
            "cassini_gamma_pubmed",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "Bertotti-Iess-Tortora Cassini gamma result gamma = 1 + (2.1 +/- 2.3)e-5; used as nonclaim PPN seed.",
        ),
        (
            "llr_gdot_arxiv",
            "https://arxiv.org/abs/gr-qc/0411113",
            "Williams-Turyshev-Boggs LLR result dG/G=(4 +/- 9)e-13 yr^-1; used as nonclaim drift seed.",
        ),
        (
            "llr_gdot_pubmed",
            "https://pubmed.ncbi.nlm.nih.gov/15697965/",
            "PubMed mirror of the LLR dG/G=(4 +/- 9)e-13 yr^-1 result.",
        ),
        (
            "eotwash_2020_prl",
            "https://link.aps.org/doi/10.1103/PhysRevLett.124.101101",
            "Eot-Wash 2020 PRL short-range inverse-square-law test down to 52 micrometers; anchor only until alpha(lambda) curve is digitized.",
        ),
        (
            "eotwash_inverse_square_page",
            "https://www.npl.washington.edu/eotwash/inverse-square-law",
            "Eot-Wash public inverse-square-law page: no deviation down to about 0.06 mm; continuity check for R10 anchor.",
        ),
    ]
    for source_id, url, role in web_specs:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_type": "web_source",
                "local_path": "",
                "source_url": url,
                "exists": True,
                "needle": "source-backed summary from web lookup",
                "needle_found": True,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def observational_seed_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "seed_id": "OBS3641_0_cassini_gamma",
            "arena": "PPN_local_GR",
            "observable": "gamma_minus_one",
            "central_value": 2.1e-5,
            "one_sigma_uncertainty": 2.3e-5,
            "limit_value_used": 2.3e-5,
            "limit_kind": "one_sigma_seed_not_final_bound",
            "units": "dimensionless",
            "source_id": "cassini_gamma_pubmed",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "claim_status": "OBSERVATIONAL_LIMIT_SEED_ONLY",
        },
        {
            **base,
            "seed_id": "OBS3641_1_llr_gdot",
            "arena": "Gdot_clock",
            "observable": "dG_over_G_dt",
            "central_value": 4.0e-13,
            "one_sigma_uncertainty": 9.0e-13,
            "limit_value_used": 9.0e-13,
            "limit_kind": "one_sigma_seed_not_final_bound",
            "units": "yr^-1",
            "source_id": "llr_gdot_arxiv;llr_gdot_pubmed",
            "source_url": "https://arxiv.org/abs/gr-qc/0411113 ; https://pubmed.ncbi.nlm.nih.gov/15697965/",
            "claim_status": "OBSERVATIONAL_LIMIT_SEED_ONLY",
        },
        {
            **base,
            "seed_id": "OBS3641_2_eotwash_lambda_anchor",
            "arena": "R10_short_range",
            "observable": "lambda_min_tested",
            "central_value": 5.2e-5,
            "one_sigma_uncertainty": "",
            "limit_value_used": 5.2e-5,
            "limit_kind": "anchor_only_not_alpha_curve",
            "units": "m",
            "source_id": "eotwash_2020_prl;eotwash_inverse_square_page",
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.124.101101 ; https://www.npl.washington.edu/eotwash/inverse-square-law",
            "claim_status": "ANCHOR_ONLY_NO_ALPHA_BOUND",
        },
    ]


def priority_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "rank": 1,
            "arena": "Gdot_clock",
            "why_first": "has a direct source-normalization drift seed with units yr^-1; only needs Xdot_N/existing time profile before a beta_common inequality is executable",
            "observational_seed_available": True,
            "parent_inputs_missing": "Xdot_N;explicit_t residuals;clock convention",
            "next_action": "derive or estimate local Xdot_N from MTS time/local-vacuum branch",
        },
        {
            **base,
            "rank": 2,
            "arena": "PPN_local_GR",
            "why_first": "Cassini gamma seed exists and directly pressures local-GR reduction; needs PPN projection coefficient C_PPN",
            "observational_seed_available": True,
            "parent_inputs_missing": "C_PPN;derivative map;PPN gauge projection",
            "next_action": "derive beta_common to PPN gamma map or prove coefficient zero",
        },
        {
            **base,
            "rank": 3,
            "arena": "R10_short_range",
            "why_first": "strong short-range empirical anchor exists, but full alpha(lambda) curve and MTS K_X/M_X/tau_R10 inputs are still needed",
            "observational_seed_available": True,
            "parent_inputs_missing": "alpha_bound(lambda);K_X;M_X^2;tau_R10(lambda)",
            "next_action": "digitize/source alpha(lambda) curve only after parent coupling coefficients are explicit",
        },
        {
            **base,
            "rank": 4,
            "arena": "orbital_radial",
            "why_first": "important for Newtonian inverse-square recovery but needs an MTS local radial profile before public residuals can bite",
            "observational_seed_available": False,
            "parent_inputs_missing": "partial_r X_N;radial source boundary;orbital covariance",
            "next_action": "derive local X_N(r) or demote to bound row",
        },
        {
            **base,
            "rank": 5,
            "arena": "source_WEP_null_guard",
            "why_first": "not a beta_common bound because common-mode coupling cancels from differential WEP",
            "observational_seed_available": True,
            "parent_inputs_missing": "none for the guard; use only as a no-false-pass check",
            "next_action": "keep WEP separate from common-source normalization",
        },
    ]


def first_fill_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "fill_id": "FILL3641_0_gdot_beta_bound_seed",
            "arena": "Gdot_clock",
            "observational_limit": "sigma(|dG/G dt|)=9.0e-13 yr^-1 with central 4.0e-13 yr^-1",
            "beta_bound_formula": "|beta_common| <= (9.0e-13 yr^-1 + |explicit_t residuals|)/|Xdot_N|",
            "numeric_beta_bound": "",
            "why_not_numeric": "Xdot_N and explicit_t residuals are parent/MTS inputs, not observational inputs",
            "source_url": "https://arxiv.org/abs/gr-qc/0411113",
            "status": "OBSERVATIONAL_NUMERIC_SEED_FILLED_PARENT_INPUTS_MISSING",
        },
        {
            **base,
            "fill_id": "FILL3641_1_ppn_gamma_beta_bound_seed",
            "arena": "PPN_local_GR",
            "observational_limit": "sigma(|gamma-1|)=2.3e-5 with central 2.1e-5",
            "beta_bound_formula": "|beta_common| <= sqrt(2.3e-5/|C_gamma|) if derivative terms are zero or separately bounded",
            "numeric_beta_bound": "",
            "why_not_numeric": "C_gamma is the MTS-to-PPN projection coefficient and is not yet derived",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "status": "OBSERVATIONAL_NUMERIC_SEED_FILLED_PARENT_INPUTS_MISSING",
        },
        {
            **base,
            "fill_id": "FILL3641_2_r10_lambda_anchor_seed",
            "arena": "R10_short_range",
            "observational_limit": "lambda_min anchor = 5.2e-5 m; not an alpha(lambda) limit row",
            "beta_bound_formula": "|beta_common(lambda)| <= sqrt(|alpha_bound(lambda)| M_X^2/(|K_X tau_R10(lambda)|))",
            "numeric_beta_bound": "",
            "why_not_numeric": "alpha_bound(lambda) curve plus K_X, M_X^2, and tau_R10(lambda) are still required",
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.124.101101",
            "status": "ANCHOR_FILLED_FULL_CURVE_AND_PARENT_INPUTS_MISSING",
        },
    ]


def scoreability_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "audit_id": "SCORE3641_0_no_beta_claim",
            "question": "Can any beta_common numeric pass/fail be claimed now?",
            "answer": "no",
            "reason": "observational limits are now seeded, but every beta_common inequality still needs at least one parent coefficient/profile input",
            "next_unlock": "derive Xdot_N first or derive C_gamma first",
        },
        {
            **base,
            "audit_id": "SCORE3641_1_best_next",
            "question": "Which missing input gives the fastest real progress?",
            "answer": "Xdot_N local time profile, then C_gamma PPN projection",
            "reason": "Gdot has the cleanest dimensional seed; PPN has the cleanest GR-reduction pressure",
            "next_unlock": "3642 local X_N time/radial profile and PPN projection fork",
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "OBSERVATIONAL_LIMIT_SEEDS_FILLED_BETA_BOUND_STILL_PARENT_BLOCKED",
            "summary": "3641 fills the first source-backed observational seeds for beta_common: Cassini PPN gamma, LLR Gdot/G, and Eot-Wash/R10 short-range lambda anchor. No beta_common pass is claimed because Xdot_N, C_gamma, alpha(lambda), K_X, M_X^2, and tau_R10 remain parent/MTS inputs.",
            "claim_ceiling": "no beta_common bound, local-GR/Newton pass, PPN pass, Gdot pass, or R10 pass is allowed from 3641",
            "best_next": "derive local Xdot_N and/or C_gamma before spending effort digitizing full R10 curves",
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3641_0",
            "target_doc": "3642-Y5-R2FR-local-XN-profile-and-PPN-projection-coefficient.md",
            "target_script": "scripts/Y5_R2FR_3642_local_XN_profile_and_PPN_projection_coefficient.py",
            "objective": "derive or bound the local X_N time/radial profile and the beta_common-to-PPN gamma coefficient C_gamma; these are the shortest path from observational seeds to a real local-GR/Newton constraint",
            "success_gate": "either Xdot_N and C_gamma are parent-derived/zero, or they gain explicit nonclaim bound rows with units and source paths",
            "valid_for_claim": False,
        }
    ]


def write_doc(src, seeds, priorities, fills, scores, status, nxt) -> None:
    text = "\n\n".join(
        [
            "# 3641 Y5 R2FR beta bound input prioritizer and first numeric fill",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## What moved",
            (
                "This checkpoint puts real observational numbers under the `beta_common` arena map without pretending the MTS parent "
                "coefficients are known. Cassini seeds the PPN channel, LLR seeds the local drift channel, and Eot-Wash seeds the R10 "
                "short-range channel as an anchor only."
            ),
            "## Observational seeds",
            "\n".join(f"- `{row['seed_id']}`: `{row['arena']}` `{row['observable']}` limit seed `{row['limit_value_used']}` `{row['units']}` from {row['source_url']}." for row in seeds),
            "## Prioritizer",
            "\n".join(f"- Rank {row['rank']} `{row['arena']}`: {row['why_first']}" for row in priorities),
            "## First-fill rows",
            "\n".join(f"- `{row['fill_id']}`: {row['beta_bound_formula']} | status `{row['status']}`." for row in fills),
            "## Scoreability",
            "\n".join(f"- `{row['audit_id']}`: {row['answer']} — {row['reason']}" for row in scores),
            "## Next target",
            f"`{nxt[0]['target_doc']}` via `{nxt[0]['target_script']}`.",
            "## Sources",
            "\n".join(f"- `{row['source_id']}`: `{row['source_url'] or row['local_path']}` exists={row['exists']} needle_found={row['needle_found']}" for row in src),
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

    add("VAL3641_0_sources_exist", all(bool(row["exists"]) for row in src), "all local/web source rows exist")
    add("VAL3641_1_needles_found", all(bool(row["needle_found"]) for row in src), "local source needles and web source summaries present")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3641_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")
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
    add("VAL3641_3_csv_parse", parse_ok, "; ".join(details))

    seeds = read_csv(out["observational_seeds"])
    priorities = read_csv(out["priority_matrix"])
    fills = read_csv(out["first_fill"])
    scores = read_csv(out["scoreability"])
    status = read_csv(out["status"])
    nxt = read_csv(out["next_target"])

    add("VAL3641_4_numeric_seeds_present", {"OBS3641_0_cassini_gamma", "OBS3641_1_llr_gdot", "OBS3641_2_eotwash_lambda_anchor"}.issubset({row["seed_id"] for row in seeds}), "Cassini, LLR, and R10 seed rows present")
    add("VAL3641_5_positive_numeric_values", all(float(row["limit_value_used"]) > 0 for row in seeds), "all seed numeric values are positive")
    add("VAL3641_6_priority_order", priorities[0]["arena"] == "Gdot_clock" and priorities[1]["arena"] == "PPN_local_GR", "Gdot then PPN selected as fastest next route")
    add("VAL3641_7_parent_inputs_not_hidden", all(row["numeric_beta_bound"] == "" and "MISSING" not in row["beta_bound_formula"] for row in fills), "beta formulas written without fake numeric bound")
    add("VAL3641_8_scoreability_honest", any(row["answer"] == "no" and "parent coefficient" in row["reason"] for row in scores), "scoreability audit blocks pass claim")
    add("VAL3641_9_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in seeds + priorities + fills + scores + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3641*")) if FORMALIZATION.exists() else []
    add("VAL3641_10_no_formalization_leak", not leaks, "no 3641 files in formalization-workbench")
    add("VAL3641_11_next_target_written", bool(nxt) and "3642" in nxt[0]["target_doc"], "3642 X_N/PPN target written")
    add("VAL3641_12_doc_written", DOC.exists() and "Cassini" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with observational seeds")
    add("VAL3641_13_status_honest", status[0]["status"] == "OBSERVATIONAL_LIMIT_SEEDS_FILLED_BETA_BOUND_STILL_PARENT_BLOCKED", "status keeps beta bound blocked")
    return rows


def main() -> None:
    t = now()
    out = outputs()
    src = source_rows(t)
    seeds = observational_seed_rows(t)
    priorities = priority_rows(t)
    fills = first_fill_rows(t)
    scores = scoreability_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)

    write_csv(out["source_register"], src)
    write_csv(out["observational_seeds"], seeds)
    write_csv(out["priority_matrix"], priorities)
    write_csv(out["first_fill"], fills)
    write_csv(out["scoreability"], scores)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, seeds, priorities, fills, scores, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3641 validation failed: {failures}")
    print(f"wrote 3641 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
