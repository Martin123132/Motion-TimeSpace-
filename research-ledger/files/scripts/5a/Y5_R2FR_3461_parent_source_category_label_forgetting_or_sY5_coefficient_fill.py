from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3461-Y5-R2FR-parent-source-category-label-forgetting-or-sY5-coefficient-fill-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3461": Path(__file__).resolve(),
    "doc_3460": ROOT / "3460-Y5-R2FR-source-current-owner-for-doublet-or-Y5-source-normalization-bound-under-AX1090.md",
    "theorem_3460": OUT / "P8_Y5_R2FR_3460_Y5_OWNER_THEOREM_ATTEMPT.csv",
    "decomp_3460": OUT / "P8_Y5_R2FR_3460_SOURCE_CURRENT_DECOMPOSITION.csv",
    "bounds_3460": OUT / "P8_Y5_R2FR_3460_Y5_BOUND_PLUG_ROWS.csv",
    "doc_1064": ROOT / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md",
    "label_1064": OUT / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "slot_1064": OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv",
    "requirements_1064": OUT / "P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
    "predictions_1064": OUT / "P8_Y5_R10_1064_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv",
    "bounds_1064": OUT / "P8_Y5_R10_1064_RELATIVE_WEIGHT_BOUND_IMPORT.csv",
    "contract_1055": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "counter_1055": OUT / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv",
    "source_functor_953": OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
    "minimal_955": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "parent_990": OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
    "r11_minimum": OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", "<br>").replace("|", "/"))
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3461": "generator for this checkpoint",
        "doc_3460": "source-current owner predecessor",
        "theorem_3460": "Y5 owner theorem attempt input",
        "decomp_3460": "s_Y5 source-current decomposition input",
        "bounds_3460": "Y5 bound plug rows input",
        "doc_1064": "older label-forgetting proof/runner checkpoint",
        "label_1064": "label-forgetting proof attempt rows",
        "slot_1064": "no-source-only-slot audit",
        "requirements_1064": "numeric source requirements",
        "predictions_1064": "relative-weight prediction templates",
        "bounds_1064": "relative-weight empirical bound anchors",
        "contract_1055": "minimal parent action contract candidate",
        "counter_1055": "counterexample ledger",
        "source_functor_953": "source functor theorem attempt",
        "minimal_955": "minimal matter action lemma",
        "parent_990": "parent action contract",
        "r11_minimum": "R11 source-normalization minimum coefficient rows",
        "local_bounds": "local bound anchors",
    }
    return [
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def category_proof_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CPF3461_0_target",
            "claim": "Parent source category forgets matter labels before gravitational source selection.",
            "test": "source functor factors as C_matter -> T_total -> grav_source, not C_matter -> labelled family {(T_A,A)} -> grav_source",
            "result": "TARGET_PRECISE",
            "why": "This is exactly what would force s_Y5=0 for relative source-weight channels.",
            "source_path": str(SOURCES["source_functor_953"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPF3461_1_symmetric_monoidal_naturality",
            "claim": "Naturality/permutation symmetry removes arbitrary labels.",
            "test": "identical copies of the same matter object cannot receive different source weights if the functor is permutation-natural",
            "result": "PARTIAL_ONLY",
            "why": "It removes copy-label weights but still allows different natural weights for non-isomorphic species/representations.",
            "source_path": str(SOURCES["label_1064"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPF3461_2_nonisomorphic_species_counterexample",
            "claim": "Category naturality alone forbids all w_A.",
            "test": "take non-isomorphic matter sectors A,B with source map F((T_A,A),(T_B,B))=kappa_A T_A+kappa_B T_B",
            "result": "FAIL_COUNTEREXAMPLE",
            "why": "The map can remain covariant, additive, and natural on each sector while retaining representation/species-dependent constants.",
            "source_path": str(SOURCES["counter_1055"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPF3461_3_minimal_grammar_route",
            "claim": "A no-source-only-slot parent grammar would remove w_A.",
            "test": "Allowed[S_matter] contains masses/charges/representation constants but no coefficient whose only role is gravitational source weighting",
            "result": "SUFFICIENT_CONTRACT_NOT_DERIVED",
            "why": "This would prove label forgetting, but it is a grammar/minimality clause unless derived from deeper MTS primitives.",
            "source_path": str(SOURCES["minimal_955"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPF3461_4_field_rescaling_loophole",
            "claim": "Relative w_A can always be removed by field rescaling.",
            "test": "rescale Psi_A to absorb w_A",
            "result": "NOT_GENERAL",
            "why": "Interactions, charges, quantum normalization, composite binding, and readout constants can move the coefficient rather than erase it.",
            "source_path": str(SOURCES["minimal_955"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPF3461_5_verdict",
            "claim": "s_Y5=0 from parent category label forgetting",
            "test": "CPF3461_0 through CPF3461_4 close as parent-derived statements",
            "result": "NOT_PROVED_CURRENT_CORPUS",
            "why": "The exact sufficient theorem is known, but no-source-only-slot/minimal grammar is not derived from deeper MTS.",
            "source_path": str(SOURCES["theorem_3460"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def sY5_coefficient_fill() -> list[dict[str, Any]]:
    return [
        {
            "coeff_id": "SY5C3461_0_common_mode",
            "coefficient": "s_Y5_common",
            "definition": "doublet derivative of one common universal source normalization",
            "formula": "s_Y5_common = partial_Z ln C0 at Z=0",
            "theorem_zero_route": "C0 is fixed, universal, range/time/species/frame independent",
            "numeric_route": "not useful as a relative test unless derivative/nonconstant piece survives",
            "current_status": "CONDITIONAL_CALIBRATION_ONLY",
            "feeds": "Y5B3460_0_source_work_norm",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coeff_id": "SY5C3461_1_relative_species_weight",
            "coefficient": "s_Y5_species or Delta_w_AB",
            "definition": "species/source-label derivative or contrast in measured source normalization",
            "formula": "Delta_w_AB = w_A-w_B; contribution <= C_w ||Delta_w||",
            "theorem_zero_route": "parent no-source-only-slot grammar plus label-forgotten source functor",
            "numeric_route": "WEP product |Delta_w_AB tau_WEP| <= 2.8e-15 after tau/material map is supplied",
            "current_status": "PRIMARY_NUMERIC_OR_THEOREM_TARGET",
            "feeds": "Y5B3460_0_source_work_norm; WEP; R10; PPN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coeff_id": "SY5C3461_2_nonHilbert_source",
            "coefficient": "Q_nonH",
            "definition": "unowned source current not equal to Hilbert variation of the same matter action",
            "formula": "J_norm contribution += Q_nonH",
            "theorem_zero_route": "single parent Noether current owner and no retained q_res source channel",
            "numeric_route": "source-backed non-Hilbert current norm with units",
            "current_status": "OPEN_OWNER_CHANNEL",
            "feeds": "Y5B3460_0_source_work_norm",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coeff_id": "SY5C3461_3_boundary_domain_support",
            "coefficient": "Q_boundary_source + Q_domain_source",
            "definition": "boundary/domain/support/projector contribution to source normalization",
            "formula": "J_norm contribution += Q_boundary_source + Q_domain_source",
            "theorem_zero_route": "no-flux boundary, fixed reference class, parent-owned linear projector",
            "numeric_route": "boundary/domain coefficient vector in R11 source-normalization units",
            "current_status": "OPEN_BOUNDARY_DOMAIN_CHANNEL",
            "feeds": "Y5B3460_0_source_work_norm; B_flux gate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "coeff_id": "SY5C3461_4_range_time_radial_hair",
            "coefficient": "Q_range + Q_time + Q_radial",
            "definition": "finite-range, time-drift, or radial measured-G/source-normalization hair",
            "formula": "J_norm contribution += Q_range + Q_time + Q_radial",
            "theorem_zero_route": "no radial/range/time source hair and constant universal coupling",
            "numeric_route": "R10 alpha(lambda), Gdot, and radial profile inputs",
            "current_status": "OPEN_R11_CHANNEL",
            "feeds": "Y5B3460_0_source_work_norm; R10; Gdot; Newton inverse-square",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def first_fill_requirements() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "FFR3461_0_WEP_first_row",
            "target_component": "SY5C3461_1_relative_species_weight",
            "required_inputs": "species_pair;Delta_w_AB;tau_WEP;material/source map;eta_prediction;source_file",
            "acceptance": "derived zero from parent grammar OR numeric |Delta_w_AB tau_WEP| below 2.8e-15",
            "current_status": "MISSING_DELTA_W_AB_TAU_WEP_PRODUCT",
            "why_first": "WEP/source-charge is the tightest direct species-source label test and already has an empirical anchor.",
            "source_path": str(SOURCES["requirements_1064"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "requirement_id": "FFR3461_1_PPN_gamma_beta",
            "target_component": "SY5C3461_1_relative_species_weight",
            "required_inputs": "C_gamma_source_weight;C_beta_source_weight;Delta_w_source;weak-field response map",
            "acceptance": "theorem-zero or products below gamma/beta anchors",
            "current_status": "MISSING_RESPONSE_OPERATOR",
            "why_first": "Newton source normalization must survive PPN readout before local-GR promotion.",
            "source_path": str(SOURCES["requirements_1064"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "requirement_id": "FFR3461_2_R10_range",
            "target_component": "SY5C3461_4_range_time_radial_hair",
            "required_inputs": "lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;promoted alpha_bound(lambda)",
            "acceptance": "no finite-range theorem or sourced curve comparison",
            "current_status": "MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT",
            "why_first": "A source-normalization tail with range dependence cannot be absorbed into measured G.",
            "source_path": str(SOURCES["requirements_1064"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def theorem_status() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "TS3461_0_proof_result",
            "question": "Did parent-category label forgetting get proved?",
            "answer": "No. The exact sufficient theorem is known, but no-source-only-slot/minimal grammar is still an unsigned parent-action condition.",
            "verdict": "PROOF_NOT_CLOSED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "TS3461_1_progress_result",
            "question": "Did the work move forward?",
            "answer": "Yes. It shows why naturality is only partial, identifies the non-isomorphic species counterexample, and splits s_Y5 into coefficient rows that feed the 3460/3459 bounds.",
            "verdict": "BOUND_PATH_SHARPENED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "TS3461_2_best_next",
            "question": "What is the next practical step?",
            "answer": "Either derive the no-source-only-slot grammar from the parent observable algebra, or fill the first WEP relative-source product row as a nonclaim smoke input.",
            "verdict": "NEXT_GRAMMAR_OR_FIRST_NUMERIC_ROW",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3462-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-WEP-sY5-row-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3462_no_source_only_slot_parent_grammar_or_first_WEP_sY5_row.py",
            "objective": "Try to derive the no-source-only-slot parent grammar from the MTS observable algebra; if not, fill the first WEP s_Y5/Delta_w product row as nonclaim smoke data feeding 3461 -> 3460 -> 3459.",
            "success_gate": "Either w_A is structurally forbidden by a parent grammar theorem, or FFR3461_0 receives a sourced theorem-zero/numeric product row with units and refusal gates.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3461_0_result",
            "decision": "Do not promote label forgetting. Treat no-source-only-slot as the exact parent grammar theorem still to derive, and retain s_Y5 coefficient rows.",
            "because": "Naturality/permutation arguments only remove arbitrary copy labels, not representation/species-dependent source weights across non-isomorphic matter sectors.",
            "next_action": "Attempt no-source-only-slot from parent observable algebra, or fill the first WEP s_Y5 product row.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_modified_count_since(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        except OSError:
            continue
        if mtime >= start_utc:
            count += 1
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    proof_rows = rows_by_name["category_proof_audit"]
    coeff_rows = rows_by_name["sY5_coefficient_fill"]
    req_rows = rows_by_name["first_fill_requirements"]
    status_rows = rows_by_name["theorem_status"]
    next_rows = rows_by_name["next_target"]

    generated_paths = [
        OUT / "P8_Y5_R2FR_3461_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3461_CATEGORY_PROOF_AUDIT.csv",
        OUT / "P8_Y5_R2FR_3461_SY5_COEFFICIENT_FILL.csv",
        OUT / "P8_Y5_R2FR_3461_FIRST_FILL_REQUIREMENTS.csv",
        OUT / "P8_Y5_R2FR_3461_THEOREM_STATUS.csv",
        OUT / "P8_Y5_R2FR_3461_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3461_NEXT_TARGET.csv",
    ]
    csv_parse_ok = True
    csv_details: list[str] = []
    for path in generated_paths:
        try:
            parsed = read_csv(path)
            csv_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_details.append(f"{path.name}:{exc}")

    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3461_0_sources_exist",
            "description": "all source paths exist",
            "passed": all(bool(row["exists"]) for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        }
    )
    checks.append(
        {
            "check_id": "VAL3461_1_counterexample_retained",
            "description": "non-isomorphic species counterexample is retained",
            "passed": any(row["audit_id"] == "CPF3461_2_nonisomorphic_species_counterexample" and row["result"] == "FAIL_COUNTEREXAMPLE" for row in proof_rows),
            "detail": ";".join(f"{row['audit_id']}={row['result']}" for row in proof_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3461_2_sY5_components",
            "description": "sY5 coefficient split covers common, species, nonHilbert, boundary/domain and range/time/radial",
            "passed": {
                "SY5C3461_0_common_mode",
                "SY5C3461_1_relative_species_weight",
                "SY5C3461_2_nonHilbert_source",
                "SY5C3461_3_boundary_domain_support",
                "SY5C3461_4_range_time_radial_hair",
            }.issubset({row["coeff_id"] for row in coeff_rows}),
            "detail": ";".join(row["coeff_id"] for row in coeff_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3461_3_first_fill_requirements",
            "description": "first fill requirements include WEP, PPN and R10",
            "passed": {"FFR3461_0_WEP_first_row", "FFR3461_1_PPN_gamma_beta", "FFR3461_2_R10_range"}.issubset(
                {row["requirement_id"] for row in req_rows}
            ),
            "detail": ";".join(row["requirement_id"] for row in req_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3461_4_no_claims",
            "description": "all rows remain nonclaim and proof status is not closed",
            "passed": all(
                str(row.get("claim_allowed", "False")) == "False"
                for rows in rows_by_name.values()
                for row in rows
                if isinstance(row, dict)
            )
            and any(row["verdict"] == "PROOF_NOT_CLOSED" for row in status_rows),
            "detail": ";".join(row["verdict"] for row in status_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3461_5_csv_parse",
            "description": "generated CSV files parse cleanly",
            "passed": csv_parse_ok,
            "detail": ";".join(csv_details),
        }
    )
    checks.append(
        {
            "check_id": "VAL3461_6_next_target_3462",
            "description": "next target is no-source-only-slot grammar or first WEP sY5 row",
            "passed": len(next_rows) == 1 and "3462-Y5-R2FR-no-source-only-slot" in str(next_rows[0]["next_doc"]),
            "detail": str(next_rows[0]["next_doc"]) if next_rows else "missing next row",
        }
    )
    modified_count = formalization_modified_count_since(start_utc)
    checks.append(
        {
            "check_id": "VAL3461_7_formalization_untouched",
            "description": "formalization-workbench unchanged during this script",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        }
    )
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3461_8_overall",
            "description": "3461 label-forgetting/sY5 checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3461 - Parent Source Category Label-Forgetting Or sY5 Coefficient Fill Under AX1090",
        "",
        "## Purpose",
        "",
        "This checkpoint tests the actual parent-category proof behind `s_Y5=0`. It separates what category/naturality can really prove from what still has to be a parent grammar theorem. The important result: permutation/naturality removes arbitrary copy labels, but it does not by itself remove different source weights for non-isomorphic matter species.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"]),
        "",
        "## Category Proof Audit",
        "",
        md_table(rows_by_name["category_proof_audit"]),
        "",
        "## sY5 Coefficient Fill",
        "",
        md_table(rows_by_name["sY5_coefficient_fill"]),
        "",
        "## First Fill Requirements",
        "",
        md_table(rows_by_name["first_fill_requirements"]),
        "",
        "## Theorem Status",
        "",
        md_table(rows_by_name["theorem_status"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision_ledger"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"]),
        "",
        "## Bottom Line",
        "",
        "- Proof result: label-forgetting is still not derived; the no-source-only-slot parent grammar is the exact missing theorem.",
        "- Useful refinement: `s_Y5` is now split into common, relative-species, non-Hilbert, boundary/domain, and range/time/radial components.",
        "- Next move: either prove the grammar theorem from the observable algebra, or fill the first WEP relative-source product row as nonclaim data.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "category_proof_audit": category_proof_audit(),
        "sY5_coefficient_fill": sY5_coefficient_fill(),
        "first_fill_requirements": first_fill_requirements(),
        "theorem_status": theorem_status(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    output_map = {
        "source_register": OUT / "P8_Y5_R2FR_3461_SOURCE_REGISTER.csv",
        "category_proof_audit": OUT / "P8_Y5_R2FR_3461_CATEGORY_PROOF_AUDIT.csv",
        "sY5_coefficient_fill": OUT / "P8_Y5_R2FR_3461_SY5_COEFFICIENT_FILL.csv",
        "first_fill_requirements": OUT / "P8_Y5_R2FR_3461_FIRST_FILL_REQUIREMENTS.csv",
        "theorem_status": OUT / "P8_Y5_R2FR_3461_THEOREM_STATUS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3461_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3461_NEXT_TARGET.csv",
    }
    for name, path in output_map.items():
        write_csv(path, rows_by_name[name])
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUT / "P8_Y5_BRR545_3461_VALIDATION.csv", rows_by_name["validation"])
    write_doc(rows_by_name)
    print(f"wrote {DOC}")
    print("wrote 8 csv outputs")


if __name__ == "__main__":
    main()
