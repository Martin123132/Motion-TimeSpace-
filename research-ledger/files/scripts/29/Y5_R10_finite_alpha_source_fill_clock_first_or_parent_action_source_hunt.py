from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "766-Y5-R10-finite-alpha-source-fill-clock-first-or-parent-action-source-hunt.md"
NEXT_TARGET = "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md"
STATUS = "Y5_R10_766_finite_alpha_clock_first_source_fill_imported_parent_action_source_hunt_no_zero_claim"
CLAIM_CEILING = "finite_alpha_clock_source_fill_and_parent_source_hunt_only_no_kappa_alpha_zero_no_clock_WEP_R10_EM_PPN_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

PARENT_TQ_SOURCE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_766_PARENT_TQ_SOURCE_INPUT_CANDIDATE.csv"
NO_LAMBDA_F2_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_766_NO_LAMBDA_F2_SYMMETRY_INPUT_CANDIDATE.csv"
LOCAL_CHIX_DYNAMICS_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_766_LOCAL_CHIX_DYNAMICS_INPUT_CANDIDATE.csv"
FINITE_ALPHA_ARENA_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_766_FINITE_ALPHA_ARENA_PROJECTION_INPUT_CANDIDATE.csv"
WEP_NO_ALPHA_VERTEX_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_766_WEP_NO_ALPHA_VERTEX_INPUT_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_766_SOURCE_REGISTER.csv"
PARENT_HUNT_PATH = RESIDUALS / "P8_Y5_R10_766_PARENT_ACTION_SOURCE_HUNT.csv"
CLOCK_SOURCE_LOCK_PATH = RESIDUALS / "P8_Y5_R10_766_CLOCK_ALPHA_SOURCE_LOCK.csv"
PRODUCT_BOUND_IMPORT_PATH = RESIDUALS / "P8_Y5_R10_766_PRODUCT_BOUND_IMPORT.csv"
CROSS_ARENA_HANDOFF_PATH = RESIDUALS / "P8_Y5_R10_766_CROSS_ARENA_HANDOFF.csv"
SOURCE_FILL_PATH = RESIDUALS / "P8_Y5_R10_766_SOURCE_FILL_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_766_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_766_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_766_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_766_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "765_doc": {
        "path": POST_CHECKPOINT / "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md",
        "needles": [
            "Current result: **the parent vertical-generator norm route is the exact right theorem shape, but it is not parent-signed**",
            "766-Y5-R10-finite-alpha-source-fill-clock-first-or-parent-action-source-hunt.md",
        ],
        "role": "immediate finite-alpha handoff",
    },
    "765_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_765_VALIDATION.csv",
        "needles": ["V765_15_validation_rows_ready", "V765_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "646_doc": {
        "path": POST_CHECKPOINT / "646-Y5-R10-clock-alpha-sensitivity-source-fill-or-finite-prior-runner.md",
        "needles": ["Source-backed optical-clock alpha pairs are now staged", "Galileo `alpha` redshift row is not `alpha_EM`"],
        "role": "clock alpha source-fill source",
    },
    "646_clock_sources": {
        "path": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "needles": ["CAS646_0_AlHg", "CAS646_1_YbE3E2"],
        "role": "source-backed clock-pair sensitivities",
    },
    "647_doc": {
        "path": POST_CHECKPOINT / "647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md",
        "needles": ["Strongest staged product bound is the Yb+ E3/E2 row", "2.1e-18"],
        "role": "clock product-bound map",
    },
    "647_product_bound": {
        "path": RESIDUALS / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
        "needles": ["CPB647_1_YbE3E2", "2.1e-18"],
        "role": "source-backed clock product bounds",
    },
    "647_H0_diagnostic": {
        "path": RESIDUALS / "P8_Y5_R10_647_H0_NORMALIZED_DIAGNOSTIC.csv",
        "needles": ["H0D647_1_YbE3E2", "2.93296e-08"],
        "role": "H0-normalized diagnostic bound",
    },
    "648_doc": {
        "path": POST_CHECKPOINT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md",
        "needles": ["Yb+ clocks force", "2.93e-8"],
        "role": "clock product-bound pressure runner",
    },
    "649_doc": {
        "path": POST_CHECKPOINT / "649-Y5-R10-local-chiX-silence-theorem-or-ultra-screened-alpha-branch.md",
        "needles": ["ultra-screened nonclaim branch", "2.933e-08"],
        "role": "local silence or ultra-screen branch",
    },
    "650_doc": {
        "path": POST_CHECKPOINT / "650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md",
        "needles": ["same local screening variable", "clock-only escape hatch"],
        "role": "cross-arena same-screen contract",
    },
    "652_beta_target": {
        "path": RESIDUALS / "P8_Y5_R10_652_SOURCE_NORMALIZATION_TARGET.csv",
        "needles": ["BST652_2_robust_target", "2.887280314062e-05"],
        "role": "WEP source-normalization stress target",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def parent_hunt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "PAH766_0_TQ_parent_action_source",
            "target": "parent compact charge generator T_Q as a varied parent-action object",
            "source_status": "not_found_in_current_corpus",
            "zero_route_impact": "without T_Q, the parent vertical-generator norm theorem remains dormant",
            "fallback": "finite alpha branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "PAH766_1_no_lambda_F2_symmetry",
            "target": "parent symmetry forbids independent lambda_A F_Q^2",
            "source_status": "not_found_in_current_corpus",
            "zero_route_impact": "lambda_A F_Q^2 remains the decisive alpha-owner counterexample",
            "fallback": "finite kappa_alpha source-fill",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "PAH766_2_same_owner_current",
            "target": "J_Q, charge unit, and A_Q matter coupling share one Noether/Ward owner",
            "source_status": "not_found_in_current_corpus",
            "zero_route_impact": "charge-current normalization can still reopen b_theta/b_kappa",
            "fallback": "source normalization and WEP/R10/EM projection rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "PAH766_3_readout_coframe_descent",
            "target": "Hodge star, hbar/c readout, and clock coframe are quotient-fixed for alpha_EM",
            "source_status": "not_found_as_parent_signed_clause",
            "zero_route_impact": "clock/spectroscopy readout can still see finite alpha pressure",
            "fallback": "clock product bound and local chi_X dynamics/screening branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "PAH766_4_verdict",
            "target": "reactivate kappa_alpha=0 theorem route",
            "source_status": "blocked_no_parent_action_source",
            "zero_route_impact": "do not use alpha zero as evidence",
            "fallback": "clock-first finite alpha corridor remains active but nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def clock_source_lock_rows(generated_utc: str) -> list[dict[str, Any]]:
    clock_rows = read_csv_rows(RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv")
    rows: list[dict[str, Any]] = []
    for row in clock_rows:
        rows.append(
            {
                "clock_lock_id": row.get("clock_pair_id", ""),
                "clock_pair": row.get("clock_pair", ""),
                "delta_K_alpha_used": row.get("delta_K_alpha_used", ""),
                "source_status": row.get("delta_K_alpha_source_status", ""),
                "source_value": row.get("alpha_drift_source_value", ""),
                "MTS_projection": row.get("MTS_projection", ""),
                "missing_MTS_side": row.get("MTS_missing", ""),
                "numeric_score_ready": row.get("numeric_score_ready", "false"),
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    rows.append(
        {
            "clock_lock_id": "R2R766_Galileo_repair",
            "clock_pair": "Galileo eccentric-satellite redshift alpha row",
            "delta_K_alpha_used": "not_applicable",
            "source_status": "repaired_not_alpha_EM",
            "source_value": "LPI/redshift violation parameter, not fine-structure alpha_EM",
            "MTS_projection": "do_not_use_as_delta_alpha_EM",
            "missing_MTS_side": "none; row excluded from alpha_EM source-fill",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    )
    return rows


def product_bound_rows(generated_utc: str) -> list[dict[str, Any]]:
    product_rows = read_csv_rows(RESIDUALS / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv")
    h0_rows = {row.get("clock_pair_id", ""): row for row in read_csv_rows(RESIDUALS / "P8_Y5_R10_647_H0_NORMALIZED_DIAGNOSTIC.csv")}
    rows: list[dict[str, Any]] = []
    for row in product_rows:
        h0_row = h0_rows.get(row.get("clock_pair_id", ""), {})
        rows.append(
            {
                "bound_import_id": row.get("bound_id", ""),
                "clock_pair_id": row.get("clock_pair_id", ""),
                "clock_pair": row.get("clock_pair", ""),
                "product_bound_1sigma_yr_inv": row.get("conservative_abs_product_bound_1sigma_yr_inv", ""),
                "H0_normalized_product_bound": h0_row.get("bound_on_abs_kappa_times_dchi_dN_1sigma", ""),
                "what_is_bounded": "kappa_alpha * tau_clock_time, or diagnostic kappa_alpha * dchi_X/dN if tau=H0*dchi/dN",
                "standalone_kappa_bound_ready": row.get("standalone_kappa_bound_ready", "false"),
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def cross_arena_handoff_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "CAH766_0_clocks",
            "arena": "atomic clocks",
            "imported_result": "Yb+ E3/E2 gives |kappa_alpha*tau_clock_time| <= 2.1e-18 yr^-1 and H0 diagnostic 2.93296e-08",
            "current_status": "source_backed_product_bound_nonclaim",
            "next_requirement": "derive tau_clock/local chi_X dynamics or retain ultra-screened branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "handoff_id": "CAH766_1_local_silence",
            "arena": "local lab domains",
            "imported_result": "tau_clock=0 would pass clocks but local chi_X silence clauses are unsigned",
            "current_status": "conditional_not_parent_signed",
            "next_requirement": "parent domain classifier, strict local coframe, no-alpha-vertex clause",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "handoff_id": "CAH766_2_shared_screen",
            "arena": "clocks/WEP/R10/EM",
            "imported_result": "same S_lab_alpha must be used across local alpha-sensitive arenas",
            "current_status": "cross_arena_contract_nonclaim",
            "next_requirement": "no arena-specific screen without parent domain reason",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "handoff_id": "CAH766_3_WEP_pressure",
            "arena": "WEP/MICROSCOPE",
            "imported_result": "if common-geometry zero fails, robust beta_source_alpha target is <= 2.887e-05",
            "current_status": "numeric_target_not_derived",
            "next_requirement": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "handoff_id": "CAH766_4_R10_EM_PPN",
            "arena": "R10/EM/PPN",
            "imported_result": "finite alpha branch has no R10/EM projection score and does not repair PPN/local-GR",
            "current_status": "blocked_projection_or_separate_GR_debt",
            "next_requirement": "R10/EM projection source rows and separate local-GR derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "SFS766_0_parent_TQ_source",
            "artifact": str(PARENT_TQ_SOURCE_CANDIDATE_PATH),
            "required_columns": "generator_id;parent_action_location;compactness;fixed_norm;connection_projection;source_path;valid_for_claim",
            "claim_gate": "reactivate alpha-zero route only if T_Q is a real parent-action object",
            "current_status": f"schema_only_candidate_missing={bool_string(not PARENT_TQ_SOURCE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS766_1_no_lambda_F2_symmetry",
            "artifact": str(NO_LAMBDA_F2_CANDIDATE_PATH),
            "required_columns": "symmetry_id;forbidden_operator;proof_owner;boundary_terms;source_path;valid_for_claim",
            "claim_gate": "lambda_A F_Q^2 is parent-forbidden, not set to zero by taste",
            "current_status": f"schema_only_candidate_missing={bool_string(not NO_LAMBDA_F2_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS766_2_local_chiX_dynamics",
            "artifact": str(LOCAL_CHIX_DYNAMICS_CANDIDATE_PATH),
            "required_columns": "domain;chiX_definition;tau_clock_time;tau_over_H0;parent_domain_classifier;source_path;valid_for_claim",
            "claim_gate": "clock product bounds become theory predictions only after tau dynamics are supplied",
            "current_status": f"schema_only_candidate_missing={bool_string(not LOCAL_CHIX_DYNAMICS_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS766_3_finite_alpha_arena_projection",
            "artifact": str(FINITE_ALPHA_ARENA_CANDIDATE_PATH),
            "required_columns": "arena;shared_screen_variable;tau_factor;sensitivity_vector;bound_source_path;valid_for_claim",
            "claim_gate": "clocks, WEP, R10, and EM use the same alpha screen unless a parent exception is derived",
            "current_status": f"schema_only_candidate_missing={bool_string(not FINITE_ALPHA_ARENA_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS766_4_WEP_no_alpha_vertex",
            "artifact": str(WEP_NO_ALPHA_VERTEX_CANDIDATE_PATH),
            "required_columns": "matter_clause;species_blind_geometry;no_alpha_vertex;selector_Ward_status;source_path;valid_for_claim",
            "claim_gate": "WEP alpha/composition channel is zero by parent matter functor, not by arena-specific screening",
            "current_status": f"schema_only_candidate_missing={bool_string(not WEP_NO_ALPHA_VERTEX_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D766_0_parent_source_hunt",
            "decision": "no parent-action source found that reactivates kappa_alpha=0",
            "why": "T_Q, no-lambda-F2 symmetry, same-owner current, and readout/coframe descent remain unsigned",
            "claim_status": "zero_route_dormant",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D766_1_clock_first_fill",
            "decision": "import the source-backed clock-first finite alpha corridor",
            "why": "646/647 already provide Al/Hg and Yb E3/E2 delta_K and product bounds; no new web acquisition is needed for this checkpoint",
            "claim_status": "source_fill_imported_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D766_2_next",
            "decision": "move to parent matter functor/no-alpha-vertex or WEP closure",
            "why": "clock product bounds force ultra-screening, and WEP then demands either a common-geometry zero theorem or beta_source_alpha <= 2.887e-05",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU766_0_allowed",
            "allowed_after_766": "use clock data as product bounds on kappa_alpha*tau_clock_time",
            "forbidden_after_766": "quote them as standalone kappa_alpha bounds",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU766_1_allowed",
            "allowed_after_766": "retain ultra-screened alpha as a nonclaim cross-arena branch",
            "forbidden_after_766": "invent clock-only or WEP-only screening factors",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU766_2_allowed",
            "allowed_after_766": "try the parent matter-functor/no-alpha-vertex derivation next",
            "forbidden_after_766": "claim WEP or local-GR safety from alpha screening alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "parent alpha-zero source hunt stays blocked; finite clock-alpha source-fill is imported as nonclaim product-bound corridor",
            "hard_blocker": "standalone kappa_alpha requires local chi_X/tau dynamics; WEP requires no-alpha-vertex/common-geometry theorem or beta_source suppression",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    parent_hunt: list[dict[str, Any]],
    clock_lock: list[dict[str, Any]],
    product_bounds: list[dict[str, Any]],
    cross_arena: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V766_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V766_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_765 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_765_VALIDATION.csv")
    validation.append({"check_id": "V766_2_prior_765_clean", "result": "pass" if prior_765 and all(row.get("result") == "pass" for row in prior_765) else "fail", "detail": "765 validation has no failures"})
    validation.append({"check_id": "V766_3_parent_source_hunt_blocks_zero", "result": "pass" if any(row["hunt_id"] == "PAH766_4_verdict" and row["source_status"] == "blocked_no_parent_action_source" for row in parent_hunt) else "fail", "detail": "alpha-zero route remains dormant"})
    real_clock_rows = [row for row in clock_lock if row["clock_lock_id"].startswith("CAS646_")]
    validation.append({"check_id": "V766_4_clock_sources_imported", "result": "pass" if len(real_clock_rows) == 2 and all(abs(to_float(row["delta_K_alpha_used"])) > 0 for row in real_clock_rows) else "fail", "detail": "two source-backed clock alpha rows imported"})
    validation.append({"check_id": "V766_5_product_bounds_positive", "result": "pass" if len(product_bounds) == 2 and all(to_float(row["product_bound_1sigma_yr_inv"]) > 0 for row in product_bounds) else "fail", "detail": "clock product bounds positive"})
    validation.append({"check_id": "V766_6_no_standalone_kappa_claim", "result": "pass" if all(row["standalone_kappa_bound_ready"] == "false" for row in product_bounds) else "fail", "detail": "product bounds are not standalone kappa bounds"})
    validation.append({"check_id": "V766_7_cross_arena_handoff_retained", "result": "pass" if len(cross_arena) == 5 and any(row["handoff_id"] == "CAH766_3_WEP_pressure" for row in cross_arena) else "fail", "detail": "clock/WEP/R10/EM handoff present"})
    beta_rows = read_csv_rows(RESIDUALS / "P8_Y5_R10_652_SOURCE_NORMALIZATION_TARGET.csv")
    robust = [row for row in beta_rows if row.get("target_id") == "BST652_2_robust_target"]
    validation.append({"check_id": "V766_8_WEP_beta_target_importable", "result": "pass" if robust and to_float(robust[0].get("required_abs_beta_source_max", "")) > 0 else "fail", "detail": "robust WEP beta target available"})
    validation.append({"check_id": "V766_9_source_fill_schema_written", "result": "pass" if len(source_fill) == 5 and all(row["valid_for_claim"] == "false" for row in source_fill) else "fail", "detail": "source-fill rows schema-only"})
    candidate_paths = [PARENT_TQ_SOURCE_CANDIDATE_PATH, NO_LAMBDA_F2_CANDIDATE_PATH, LOCAL_CHIX_DYNAMICS_CANDIDATE_PATH, FINITE_ALPHA_ARENA_CANDIDATE_PATH, WEP_NO_ALPHA_VERTEX_CANDIDATE_PATH]
    validation.append({"check_id": "V766_10_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in candidate_paths) else "fail", "detail": "no claim-input artifacts fabricated"})
    all_generated = parent_hunt + clock_lock + product_bounds + cross_arena + source_fill + decisions + routes + summary
    validation.append({"check_id": "V766_11_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V766_12_no_local_or_arena_claim", "result": "pass" if "no_kappa_alpha_zero_no_clock_WEP_R10_EM_PPN_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha/local arena claims remain blocked"})
    validation.append({"check_id": "V766_13_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        PARENT_HUNT_PATH,
        CLOCK_SOURCE_LOCK_PATH,
        PRODUCT_BOUND_IMPORT_PATH,
        CROSS_ARENA_HANDOFF_PATH,
        SOURCE_FILL_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V766_14_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V766_15_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V766_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    parent_hunt: list[dict[str, Any]],
    clock_lock: list[dict[str, Any]],
    product_bounds: list[dict[str, Any]],
    cross_arena: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 766 - Y5 R10 Finite Alpha Source Fill Clock-First Or Parent-Action Source Hunt

Start point: 765 made the `kappa_alpha=0` theorem beautifully sharp but still unsigned because `lambda_A F_Q^2`, generator/current rescaling, and readout/coframe leakage remain legal.

Current result: **no parent-action source was found that reactivates alpha-zero, so the finite-alpha branch imports the existing clock-first source-fill as a nonclaim product-bound corridor**. Clocks do not yet bound standalone `kappa_alpha`; they bound `kappa_alpha * tau_clock_time`. The strongest imported row is Yb+ E3/E2: `|kappa_alpha * tau_clock_time| <= 2.1e-18 yr^-1`, or diagnostic `|kappa_alpha dchi_X/dN| <= 2.93296e-08` if `tau_clock_time=H0 dchi_X/dN`.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Parent-Action Source Hunt

{markdown_table(parent_hunt, ["hunt_id", "target", "source_status", "zero_route_impact", "fallback", "valid_for_claim"])}

## Clock Alpha Source Lock

{markdown_table(clock_lock, ["clock_lock_id", "clock_pair", "delta_K_alpha_used", "source_status", "source_value", "MTS_projection", "missing_MTS_side", "numeric_score_ready", "valid_for_claim"])}

## Product Bound Import

{markdown_table(product_bounds, ["bound_import_id", "clock_pair_id", "clock_pair", "product_bound_1sigma_yr_inv", "H0_normalized_product_bound", "what_is_bounded", "standalone_kappa_bound_ready", "valid_for_claim"])}

## Cross-Arena Handoff

{markdown_table(cross_arena, ["handoff_id", "arena", "imported_result", "current_status", "next_requirement", "valid_for_claim"])}

## Source-Fill Schema

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "why", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_766", "forbidden_after_766", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is where the alpha branch stops being vibes and starts being boxed in. The parent-theorem route remains the clean win condition, but no current source signs it. The clock route is real and source-backed, but brutal: without local `chi_X` silence or ultra-screening, it crushes finite alpha quickly. And WEP is now the next referee: either the parent matter functor/no-alpha-vertex theorem kills composition dependence, or the branch needs a real source-normalization suppression target, not another knob.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    parent_hunt = parent_hunt_rows(generated_utc)
    clock_lock = clock_source_lock_rows(generated_utc)
    product_bounds = product_bound_rows(generated_utc)
    cross_arena = cross_arena_handoff_rows(generated_utc)
    source_fill = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, parent_hunt, clock_lock, product_bounds, cross_arena, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_HUNT_PATH, parent_hunt, ["hunt_id", "target", "source_status", "zero_route_impact", "fallback", "valid_for_claim", "generated_utc"])
    write_csv(CLOCK_SOURCE_LOCK_PATH, clock_lock, ["clock_lock_id", "clock_pair", "delta_K_alpha_used", "source_status", "source_value", "MTS_projection", "missing_MTS_side", "numeric_score_ready", "valid_for_claim", "generated_utc"])
    write_csv(PRODUCT_BOUND_IMPORT_PATH, product_bounds, ["bound_import_id", "clock_pair_id", "clock_pair", "product_bound_1sigma_yr_inv", "H0_normalized_product_bound", "what_is_bounded", "standalone_kappa_bound_ready", "valid_for_claim", "generated_utc"])
    write_csv(CROSS_ARENA_HANDOFF_PATH, cross_arena, ["handoff_id", "arena", "imported_result", "current_status", "next_requirement", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "why", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_766", "forbidden_after_766", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, parent_hunt, clock_lock, product_bounds, cross_arena, source_fill, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
