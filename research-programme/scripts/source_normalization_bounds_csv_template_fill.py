from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-normalization-bounds-csv-template-fill"
CHECKPOINT_DOC = "427-source-normalization-bounds-csv-template-fill.md"
STATUS = "source_normalization_bounds_csv_template_fill_written_verified_local_bound_claims_csv_ready_for_evaluate_no_data_claim_no_local_GR_pass"
CLAIM_CEILING = "verified_bounds_source_intake_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "427-local-bound-runner-v4-evaluate-smoke.md"
SOURCE_INTAKE_DIR = ROOT / "source-intake" / "local_bounds"
CLAIMS_CSV = SOURCE_INTAKE_DIR / "local_bound_claims.csv"


SOURCE_DOCS = [
    {
        "path": "426-local-bound-runner-v4-dryrun-wrapper.md",
        "role": "source-intake and evaluate workflow contract",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims_TEMPLATE.csv",
        "role": "runner-v4 generated template and required schema",
    },
    {
        "path": "runs/20260602-091000-local-bound-runner-v4-dryrun-wrapper/results/schema_validation.csv",
        "role": "dry-run schema validation evidence",
    },
    {
        "path": "scripts/local_bound_runner_v4_real_data_interface.py",
        "role": "evaluate-mode schema and source-lock evaluator",
    },
    {
        "path": "runs/20260602-061500-local-bound-runner-v4-real-data-interface/results/local_data_targets.csv",
        "role": "canonical R0-R11 local target map",
    },
]


VERIFIED_SOURCES = [
    {
        "source_id": "MICROSCOPE_PRL_2022",
        "title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
        "url_or_doi": "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102",
        "source_type": "primary_PRL_arxiv",
        "used_for_rows": "R0;R1",
        "extracted_bound": "eta(Ti,Pt)=[-1.5 +/- 2.3(stat) +/- 1.5(syst)]e-15; combined sigma rounded to 2.8e-15",
        "verification_status": "web_verified",
    },
    {
        "source_id": "GALILEO_REDSHIFT_DELVA_PRL_2018",
        "title": "A gravitational redshift test using eccentric Galileo satellites",
        "url_or_doi": "https://arxiv.org/abs/1812.03711; doi:10.1103/PhysRevLett.121.231101",
        "source_type": "primary_PRL_arxiv",
        "used_for_rows": "R2",
        "extracted_bound": "fractional deviation (+0.19 +/- 2.48)e-5 at 1 sigma",
        "verification_status": "web_verified",
    },
    {
        "source_id": "CASSINI_NATURE_2003",
        "title": "A test of general relativity using radio links with the Cassini spacecraft",
        "url_or_doi": "https://www.nature.com/articles/nature01997; doi:10.1038/nature01997",
        "source_type": "primary_Nature",
        "used_for_rows": "R3",
        "extracted_bound": "gamma=1+(2.1 +/- 2.3)e-5",
        "verification_status": "web_verified",
    },
    {
        "source_id": "WILL_LIVING_REVIEWS_2014_PPN_TABLE",
        "title": "The Confrontation between General Relativity and Experiment",
        "url_or_doi": "https://link.springer.com/article/10.12942/lrr-2014-4; mirror table: https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
        "source_type": "review_Living_Reviews",
        "used_for_rows": "R4;R5;R6;R7;R8",
        "extracted_bound": "Table 4: beta-1 8e-5, alpha1 1e-4 or 4e-5, alpha2 2e-9, alpha3 4e-20, xi 4e-9",
        "verification_status": "web_verified",
    },
    {
        "source_id": "BISKUPEK_MULLER_TORRE_UNIVERSE_2021",
        "title": "Benefit of new high-precision LLR data for the determination of relativistic parameters",
        "url_or_doi": "https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034",
        "source_type": "primary_LLR_article",
        "used_for_rows": "R9",
        "extracted_bound": "Gdot/G0=(-5.0 +/- 9.6)e-15 yr^-1",
        "verification_status": "web_verified",
    },
    {
        "source_id": "ADELBERGER_HECKEL_NELSON_2003_ISL",
        "title": "Tests of the gravitational inverse-square law",
        "url_or_doi": "https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503",
        "source_type": "review_inverse_square_law",
        "used_for_rows": "R10",
        "extracted_bound": "Yukawa alpha(lambda) is range-dependent and must stay curve-input symbolic",
        "verification_status": "web_verified_symbolic",
    },
    {
        "source_id": "MTS_OPERATOR_LEDGER_425",
        "title": "EH Operator Retained Ledger and Source-Normalization Test Plan",
        "url_or_doi": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "source_type": "internal_retained_operator_ledger",
        "used_for_rows": "R11",
        "extracted_bound": "non-EH operator coefficients are symbolic retained rows, not empirical pass rows",
        "verification_status": "local_verified_symbolic",
    },
]


CLAIM_ROWS = [
    {
        "dataset_id": "MICROSCOPE_final_TiPt",
        "test_arena": "MICROSCOPE/Eotvos/composition",
        "row_id": "R0_identity_coframe_direct",
        "observable": "eta_WEP_direct_geometry",
        "measured_value": "-1.5e-15",
        "one_sigma": f"{math.sqrt(2.3**2 + 1.5**2):.12g}e-15",
        "upper_bound": "2.8e-15",
        "units": "dimensionless",
        "confidence_label": "1sigma_combined_rounded_from_stat_syst",
        "baseline_model": "WEP_null_eta_0",
        "reference_path_or_url": "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102",
        "reference_note": "MICROSCOPE Ti/Pt WEP result; maps only direct geometry/source test row, not a theorem-zero promotion",
    },
    {
        "dataset_id": "MICROSCOPE_final_TiPt_source_charge_proxy",
        "test_arena": "MICROSCOPE/Eotvos/composition",
        "row_id": "R1_WEP_source_charge",
        "observable": "eta_WEP_source_charge",
        "measured_value": "-1.5e-15",
        "one_sigma": f"{math.sqrt(2.3**2 + 1.5**2):.12g}e-15",
        "upper_bound": "2.8e-15",
        "units": "dimensionless",
        "confidence_label": "1sigma_combined_rounded_direct_WEP_proxy",
        "baseline_model": "WEP_null_eta_0",
        "reference_path_or_url": "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102",
        "reference_note": "Uses same WEP source as direct proxy; full source-normalization R1 channel remains retained",
    },
    {
        "dataset_id": "Galileo_redshift_Delva_2018",
        "test_arena": "redshift/clocks",
        "row_id": "R2_clock_redshift",
        "observable": "alpha_clock_redshift",
        "measured_value": "1.9e-06",
        "one_sigma": "2.48e-05",
        "upper_bound": "2.48e-05",
        "units": "dimensionless",
        "confidence_label": "1sigma_fractional_redshift_deviation",
        "baseline_model": "GR_redshift_alpha_0",
        "reference_path_or_url": "https://arxiv.org/abs/1812.03711; doi:10.1103/PhysRevLett.121.231101",
        "reference_note": "Galileo eccentric satellites redshift/LPI test; clock row only",
    },
    {
        "dataset_id": "Cassini_Shapiro_gamma_2003",
        "test_arena": "Cassini/VLBI/solar-system light propagation",
        "row_id": "R3_gamma",
        "observable": "gamma_minus_1",
        "measured_value": "2.1e-05",
        "one_sigma": "2.3e-05",
        "upper_bound": "2.3e-05",
        "units": "dimensionless",
        "confidence_label": "1sigma_Cassini_gamma",
        "baseline_model": "PPN_GR_gamma_1",
        "reference_path_or_url": "https://www.nature.com/articles/nature01997; doi:10.1038/nature01997",
        "reference_note": "Cassini Shapiro/radio-link gamma result",
    },
    {
        "dataset_id": "Will_2014_PPN_beta_table",
        "test_arena": "planetary ephemerides/LLR",
        "row_id": "R4_beta",
        "observable": "beta_minus_1",
        "measured_value": "-4.1e-05",
        "one_sigma": "7.8e-05",
        "upper_bound": "7.8e-05",
        "units": "dimensionless",
        "confidence_label": "1sigma_Messenger_planetary_fit_with_Cassini_gamma_prior",
        "baseline_model": "PPN_GR_beta_1",
        "reference_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
        "reference_note": "Will 2014 review reports beta-1=(-4.1 +/- 7.8)e-5 and Table 4 limit about 8e-5",
    },
    {
        "dataset_id": "Will_2014_PPN_alpha1_table",
        "test_arena": "pulsar/solar-system preferred-frame",
        "row_id": "R5_alpha1",
        "observable": "alpha1",
        "measured_value": "",
        "one_sigma": "",
        "upper_bound": "1e-04",
        "units": "dimensionless",
        "confidence_label": "conservative_Table4_LLR_bound",
        "baseline_model": "PPN_GR_alpha1_0",
        "reference_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
        "reference_note": "Will Table 4 gives 1e-4 LLR and 4e-5 PSR J1738+0333; conservative solar-system-compatible row uses 1e-4",
    },
    {
        "dataset_id": "Will_2014_PPN_alpha2_table",
        "test_arena": "solar-spin/pulsar preferred-frame",
        "row_id": "R6_alpha2",
        "observable": "alpha2",
        "measured_value": "",
        "one_sigma": "",
        "upper_bound": "2e-09",
        "units": "dimensionless",
        "confidence_label": "Table4_millisecond_pulsar_bound",
        "baseline_model": "PPN_GR_alpha2_0",
        "reference_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
        "reference_note": "Will Table 4 alpha2 preferred-frame bound; strong-field caveat retained",
    },
    {
        "dataset_id": "Will_2014_PPN_alpha3_table",
        "test_arena": "pulsar/solar-system momentum flux",
        "row_id": "R7_alpha3",
        "observable": "alpha3",
        "measured_value": "",
        "one_sigma": "",
        "upper_bound": "4e-20",
        "units": "dimensionless",
        "confidence_label": "Table4_pulsar_Pdot_statistics_bound",
        "baseline_model": "PPN_GR_alpha3_0",
        "reference_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
        "reference_note": "Will Table 4 alpha3 pulsar acceleration bound; ultratight exchange/flux lock",
    },
    {
        "dataset_id": "Will_2014_PPN_xi_table",
        "test_arena": "local anisotropy/preferred-location",
        "row_id": "R8_xi",
        "observable": "xi",
        "measured_value": "",
        "one_sigma": "",
        "upper_bound": "4e-09",
        "units": "dimensionless",
        "confidence_label": "Table4_millisecond_pulsar_bound",
        "baseline_model": "PPN_GR_xi_0",
        "reference_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
        "reference_note": "Will Table 4 preferred-location xi bound; strong-field caveat retained",
    },
    {
        "dataset_id": "LLR_Biskupek_Muller_Torre_2021",
        "test_arena": "LLR/ephemerides/pulsars",
        "row_id": "R9_Gdot",
        "observable": "Gdot_over_G",
        "measured_value": "-5.0e-15",
        "one_sigma": "9.6e-15",
        "upper_bound": "9.6e-15",
        "units": "yr^-1",
        "confidence_label": "1sigma_LLR_current_result",
        "baseline_model": "constant_G_GR",
        "reference_path_or_url": "https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034",
        "reference_note": "LLR result Gdot/G0=(-5.0 +/- 9.6)e-15 yr^-1",
    },
    {
        "dataset_id": "Adelberger_Heckel_Nelson_2003_ISL_curve",
        "test_arena": "fifth-force/inverse-square",
        "row_id": "R10_fifth_force",
        "observable": "delta_G_or_fifth_force_yukawa",
        "measured_value": "",
        "one_sigma": "",
        "upper_bound": "alpha(lambda)",
        "units": "range-dependent",
        "confidence_label": "symbolic_curve_required",
        "baseline_model": "Newton_inverse_square_plus_Yukawa_alpha_lambda",
        "reference_path_or_url": "https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503",
        "reference_note": "Inverse-square law constraints are a curve in alpha(lambda); this row is intentionally symbolic and unscored",
    },
    {
        "dataset_id": "MTS_EH_operator_retained_ledger_425",
        "test_arena": "local operator closure",
        "row_id": "R11_EH_operator_ledger",
        "observable": "non_EH_operator_coefficients",
        "measured_value": "",
        "one_sigma": "",
        "upper_bound": "symbolic",
        "units": "operator family",
        "confidence_label": "symbolic_operator_ledger_required",
        "baseline_model": "EH_plus_Lambda_target_vs_retained_nonEH_operators",
        "reference_path_or_url": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "reference_note": "Operator-family row is internal retained ledger, not an empirical pass",
    },
]


DECISION = [
    {
        "decision": "Create a verified local_bound_claims.csv from primary/review sources for rows R0-R11, while explicitly preserving the symbolic fifth-force and non-EH-operator rows. This source-intake file is suitable for evaluate-mode smoke testing, but it is not evidence that MTS passes the local bounds because no MTS residual vector has been supplied yet.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "external_sources_loaded": "yes_for_bounds_csv",
        "MTS_residuals_loaded": "no",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "427-local-bound-runner-v4-evaluate-smoke.md",
        "task": "run evaluate mode on the verified local_bound_claims.csv and inspect statuses/ratios/no-claim gates",
        "priority": "P0",
    },
    {
        "next_file": "428-MTS-local-residual-vector-input-contract.md",
        "task": "define the actual MTS residual vector that must be evaluated against these bounds",
        "priority": "P0",
    },
    {
        "next_file": "428-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "task": "attempt to derive source_residuals=0 and mu_extra=0 from Ward/Bianchi exchange ownership",
        "priority": "P1",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for item in SOURCE_DOCS:
        path = ROOT / item["path"]
        rows.append(
            {
                "source_file": item["path"],
                "exists": path.exists(),
                "role": item["role"],
            }
        )
    return rows


def row_quality_rows(template_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    template_by_row = {row["row_id"]: row for row in template_rows if row.get("row_id")}
    rows = []
    for row in CLAIM_ROWS:
        template = template_by_row.get(row["row_id"], {})
        is_symbolic = row["upper_bound"] in {"alpha(lambda)", "symbolic"}
        numeric_lock_match = row["upper_bound"] == template.get("upper_bound", "") or is_symbolic
        rows.append(
            {
                "row_id": row["row_id"],
                "dataset_id": row["dataset_id"],
                "upper_bound": row["upper_bound"],
                "template_lock": template.get("upper_bound", ""),
                "reference_present": bool(row["reference_path_or_url"]) and "replace_with_verified_source" not in row["reference_path_or_url"],
                "numeric_or_symbolic_policy": "symbolic_deferred" if is_symbolic else "numeric_evaluate_ready",
                "template_lock_match_or_symbolic": numeric_lock_match,
                "claim_policy": "no_MTS_pass_without_residual_vector",
                "quality_status": "pass" if row["reference_path_or_url"] and (numeric_lock_match or not template) else "review",
            }
        )
    return rows


def symbolic_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": row["row_id"],
            "observable": row["observable"],
            "upper_bound": row["upper_bound"],
            "reason_deferred": "requires range-dependent curve or operator-family coefficient ledger",
            "claim_policy": "no_symbolic_pass",
        }
        for row in CLAIM_ROWS
        if row["upper_bound"] in {"alpha(lambda)", "symbolic"}
    ]


def gate_rows(
    source_rows: list[dict[str, Any]],
    template_rows: list[dict[str, str]],
    quality_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    missing_references = [row for row in quality_rows if not row["reference_present"]]
    missing_quality = [row for row in quality_rows if row["quality_status"] != "pass"]
    unique_row_ids = {row["row_id"] for row in CLAIM_ROWS}
    template_ids = {row["row_id"] for row in template_rows if row.get("row_id")}
    missing_template_rows = sorted(unique_row_ids - template_ids)
    symbolic_count = len(symbolic_rows())
    return [
        {
            "gate": "local_source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"{len(missing_sources)} missing local source paths",
        },
        {
            "gate": "claims_csv_written",
            "status": "pass" if CLAIMS_CSV.exists() else "fail",
            "evidence": str(CLAIMS_CSV),
        },
        {
            "gate": "claims_row_count",
            "status": "pass" if len(CLAIM_ROWS) == 12 else "fail",
            "evidence": f"{len(CLAIM_ROWS)} rows",
        },
        {
            "gate": "claims_rows_map_to_template",
            "status": "pass" if not missing_template_rows else "fail",
            "evidence": ";".join(missing_template_rows) if missing_template_rows else "all claim row IDs in template",
        },
        {
            "gate": "references_verified_not_placeholders",
            "status": "pass" if not missing_references else "fail",
            "evidence": f"{len(missing_references)} missing/placeholder references",
        },
        {
            "gate": "row_quality_passed",
            "status": "pass" if not missing_quality else "review",
            "evidence": f"{len(missing_quality)} rows need review",
        },
        {
            "gate": "symbolic_rows_deferred",
            "status": "pass" if symbolic_count == 2 else "fail",
            "evidence": f"{symbolic_count} symbolic rows: R10 and R11 expected",
        },
        {
            "gate": "MTS_residual_vector_loaded",
            "status": "not_run",
            "evidence": "bounds source-intake only; no MTS residual vector supplied",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "source intake is not WEP/EH/Newton/PPN/fifth-force proof",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def md_cell(value: Any) -> str:
    return str(value).replace("|", ";")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_cell(row[column]) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    source_rows: list[dict[str, Any]],
    quality_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, str]],
) -> None:
    source_table_rows = [
        {
            "source_id": row["source_id"],
            "source_type": row["source_type"],
            "used_for_rows": row["used_for_rows"],
            "verification_status": row["verification_status"],
        }
        for row in VERIFIED_SOURCES
    ]
    claim_table_rows = [
        {
            "row_id": row["row_id"],
            "dataset_id": row["dataset_id"],
            "observable": row["observable"],
            "upper_bound": row["upper_bound"],
            "reference_note": row["reference_note"],
        }
        for row in CLAIM_ROWS
    ]
    quality_table_rows = [
        {
            "row_id": row["row_id"],
            "numeric_or_symbolic_policy": row["numeric_or_symbolic_policy"],
            "template_lock_match_or_symbolic": row["template_lock_match_or_symbolic"],
            "quality_status": row["quality_status"],
        }
        for row in quality_rows
    ]
    symbolic_table_rows = symbolic_rows()
    local_source_table_rows = [
        {
            "source_file": row["source_file"],
            "exists": row["exists"],
            "role": row["role"],
        }
        for row in source_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 427 - Source-Normalization Bounds CSV Template Fill

Private source-intake checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 426 proved the runner-v4 dry-run machinery works. This checkpoint fills the actual `source-intake/local_bounds/local_bound_claims.csv` file with verified local-bound sources so evaluate mode can run.

The important discipline: these are bounds on possible residual channels, not predictions of MTS. They become tests of MTS only after we supply an MTS residual vector for `eta`, `gamma`, `beta`, `alpha_i`, `xi`, `Gdot/G`, fifth-force curves, and non-EH coefficients.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalization_bounds_csv_template_fill.py` |
| Run directory | `runs/{run_dir.name}` |
| Claims CSV | `source-intake/local_bounds/local_bound_claims.csv` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Local Source Register

{markdown_table(local_source_table_rows, ["source_file", "exists", "role"])}

## 4. Verified External/Internal Sources

{markdown_table(source_table_rows, ["source_id", "source_type", "used_for_rows", "verification_status"])}

## 5. Claims CSV Rows

{markdown_table(claim_table_rows, ["row_id", "dataset_id", "observable", "upper_bound", "reference_note"])}

## 6. Row Quality

{markdown_table(quality_table_rows, ["row_id", "numeric_or_symbolic_policy", "template_lock_match_or_symbolic", "quality_status"])}

## 7. Symbolic Rows Deferred

{markdown_table(symbolic_table_rows, ["row_id", "observable", "upper_bound", "reason_deferred", "claim_policy"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: we now have a real source-intake file. The next move is the evaluate smoke. If that passes, the bottleneck becomes physics again: derive or estimate the actual MTS residual vector. That is where local GR either starts earning its keep or gets shoved back into closure-only.

## 10. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    template_rows = read_csv(SOURCE_INTAKE_DIR / "local_bound_claims_TEMPLATE.csv")
    source_rows = source_register_rows()
    quality = row_quality_rows(template_rows)
    SOURCE_INTAKE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(CLAIMS_CSV, CLAIM_ROWS)
    gate_result_rows = gate_rows(source_rows, template_rows, quality)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "verified_source_register.csv", VERIFIED_SOURCES)
    write_csv(results_dir / "local_bound_claims_rows.csv", CLAIM_ROWS)
    write_csv(results_dir / "row_source_quality.csv", quality)
    write_csv(results_dir / "symbolic_rows_deferred.csv", symbolic_rows())
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    failed_gates = [row["gate"] for row in gate_result_rows if row["status"] == "fail" and row["gate"] != "local_GR_promoted"]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "claims_csv": str(CLAIMS_CSV),
        "claims_rows": len(CLAIM_ROWS),
        "verified_sources": len(VERIFIED_SOURCES),
        "symbolic_rows_deferred": len(symbolic_rows()),
        "MTS_residual_vector_loaded": False,
        "external_sources_loaded": True,
        "local_GR_claim_allowed": False,
        "failed_operational_gates": failed_gates,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, source_rows, quality, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill source-intake local_bound_claims.csv from verified local-bound references."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
