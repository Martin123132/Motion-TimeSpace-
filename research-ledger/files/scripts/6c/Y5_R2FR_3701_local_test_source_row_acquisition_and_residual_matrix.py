from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3701"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_TEST_SOURCE_ROW_ACQUISITION_AND_RESIDUAL_MATRIX_3701"
DOC = ROOT / "3701-Y5-R2FR-local-test-source-row-acquisition-and-residual-matrix.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def local_source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3700", RESIDUALS / "P8_Y5_R2FR_3700_NEXT_TARGET.csv", "source-ready numeric/symbolic rows"),
        ("arena_3700", RESIDUALS / "P8_Y5_R2FR_3700_ARENA_RUNNER_ROWS.csv", "R10"),
        ("tensor_3700", RESIDUALS / "P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv", "rho_i"),
        ("claim_3700", RESIDUALS / "P8_Y5_R2FR_3700_CLAIM_GATES.csv", "R10 alpha_bound(lambda)"),
    ]
    rows = []
    for source_id, path, needle in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base(timestamp),
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "local residual matrix handoff input",
            }
        )
    return rows


def web_source_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "WEB3701_R10_Lee2020",
            "short-range Newton/R10",
            "Lee et al. 2020 short-range test of Newtonian gravity",
            "https://pubmed.ncbi.nlm.nih.gov/32216404/",
            "10.1103/PhysRevLett.124.101101",
            "2020",
            "PubMed + University of Washington public summary",
            "Newtonian fit down to 52 micrometers; gravitational-strength Yukawa interactions limited to ranges below 38.6 micrometers at 95% confidence.",
            "anchor_only_non_curve",
        ),
        (
            "WEB3701_R10_UWash2020",
            "short-range Newton/R10",
            "University of Washington Eot-Wash public summary",
            "https://phys.washington.edu/news/2020/04/06/experiment-finds-gravity-still-works-down-50-micrometers",
            "",
            "2020",
            "public summary of same experiment",
            "95% confidence alpha=1 Yukawa range anchor: lambda < 38.6 micrometers.",
            "anchor_only_non_curve",
        ),
        (
            "WEB3701_PPN_Cassini2003",
            "PPN gamma",
            "Bertotti, Iess, Tortora Cassini radio-link test",
            "https://www.nature.com/articles/nature01997",
            "10.1038/nature01997",
            "2003",
            "reported gamma measurement",
            "gamma = 1 + (2.1 +/- 2.3) x 10^-5.",
            "numeric_normalizer_partial",
        ),
        (
            "WEB3701_WEP_MICROSCOPE2022",
            "WEP/species",
            "MICROSCOPE mission final results",
            "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
            "10.1103/PhysRevLett.129.121102",
            "2022",
            "PRL abstract and arXiv summary",
            "Weak equivalence principle tested at precision 10^-15 in Eotvos ratio eta.",
            "numeric_normalizer_partial",
        ),
        (
            "WEB3701_EM_NIST_ALPHA2022",
            "EM/fine structure",
            "NIST CODATA fine-structure constant",
            "https://physics.nist.gov/cgi-bin/cuu/Value?alph=",
            "",
            "2022 adjustment",
            "NIST constants page",
            "alpha = 7.2973525643 x 10^-3 with standard uncertainty 0.0000000011 x 10^-3.",
            "numeric_constant_anchor",
        ),
        (
            "WEB3701_CLOCK_Zheng2023",
            "clock/redshift",
            "Lab-based gravitational-redshift test with miniature clock network",
            "https://www.nature.com/articles/s41467-023-40629-8",
            "10.1038/s41467-023-40629-8",
            "2023",
            "Nature Communications abstract",
            "Measured fractional frequency gradient -12.4 +/- 0.7(stat) +/- 2.5(sys) x 10^-19 per cm over 1 cm.",
            "numeric_normalizer_partial",
        ),
        (
            "WEB3701_CLOCK_Bothwell2022",
            "clock/redshift",
            "Resolving gravitational redshift across a millimetre-scale atomic sample",
            "https://www.nist.gov/publications/resolving-gravitational-redshift-across-millimetre-scale-atomic-sample",
            "10.1038/s41586-021-04349-7",
            "2022",
            "NIST publication page",
            "NIST/JILA Nature result resolving gravitational redshift across millimetre-scale atomic sample.",
            "clock_context_anchor",
        ),
        (
            "WEB3701_GR_WillReview",
            "PPN/orbital review",
            "Will, The Confrontation between General Relativity and Experiment",
            "https://link.springer.com/article/10.12942/lrr-2006-3",
            "10.12942/lrr-2006-3",
            "2006",
            "Living Reviews article",
            "Review source for PPN and Solar-System tests; includes Cassini gamma result.",
            "review_context_anchor",
        ),
    ]
    return [
        {
            **base(timestamp),
            "web_source_id": source_id,
            "arena": arena,
            "title": title,
            "url": url,
            "doi": doi,
            "year": year,
            "extraction_method": extraction_method,
            "key_value": key_value,
            "source_status": source_status,
            "claim_allowed": False,
        }
        for source_id, arena, title, url, doi, year, extraction_method, key_value, source_status in specs
    ]


def local_test_source_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "SRC3701_R10_lambda_alpha1_anchor",
            "short-range Newton/R10",
            "lambda_alpha1_excluded_above",
            38.6,
            "micrometer",
            "95pct_anchor_for_alpha_equals_1",
            "WEB3701_R10_UWash2020",
            "anchor_only_non_curve",
            "full alpha_bound(lambda) curve still missing; cannot score arbitrary MTS lambda_H",
        ),
        (
            "SRC3701_R10_min_separation",
            "short-range Newton/R10",
            "minimum_detector_attractor_separation",
            52.0,
            "micrometer",
            "experiment_scale_anchor",
            "WEB3701_R10_Lee2020",
            "geometry_anchor",
            "does not by itself give alpha_bound(lambda)",
        ),
        (
            "SRC3701_PPN_gamma_sigma",
            "PPN/local metric",
            "sigma_gamma_minus_one",
            2.3e-5,
            "dimensionless",
            "Cassini_1sigma_normalizer",
            "WEB3701_PPN_Cassini2003",
            "numeric_normalizer_partial",
            "only gamma normalizer; beta, alpha1, alpha2, xi and MTS projection constants still missing",
        ),
        (
            "SRC3701_WEP_eta_precision",
            "WEP/species",
            "eta_precision",
            1.0e-15,
            "dimensionless",
            "Eotvos_ratio_precision",
            "WEB3701_WEP_MICROSCOPE2022",
            "numeric_normalizer_partial",
            "species residual tensors and composition scores missing",
        ),
        (
            "SRC3701_EM_alpha_value",
            "Maxwell/EM/Poynting stress",
            "fine_structure_alpha",
            7.2973525643e-3,
            "dimensionless",
            "CODATA_value",
            "WEB3701_EM_NIST_ALPHA2022",
            "numeric_constant_anchor",
            "constant value is not a residual tolerance; alpha_fs source-silence residual missing",
        ),
        (
            "SRC3701_EM_alpha_std_uncertainty",
            "Maxwell/EM/Poynting stress",
            "fine_structure_alpha_standard_uncertainty",
            1.1e-12,
            "dimensionless",
            "CODATA_standard_uncertainty",
            "WEB3701_EM_NIST_ALPHA2022",
            "numeric_normalizer_partial",
            "EM stress/Poynting residual tensor missing",
        ),
        (
            "SRC3701_CLOCK_gradient_sys_stat_combined",
            "precision clocks/time",
            "redshift_gradient_uncertainty",
            2.6e-19,
            "fractional_frequency_per_cm",
            "approx_sqrt_stat2_plus_sys2",
            "WEB3701_CLOCK_Zheng2023",
            "numeric_normalizer_partial",
            "clock projection convention and MTS clock residual tensor missing",
        ),
    ]
    return [
        {
            **base(timestamp),
            "source_row_id": row_id,
            "arena": arena,
            "quantity": quantity,
            "numeric_value": value,
            "units": units,
            "value_kind": value_kind,
            "web_source_id": web_source_id,
            "row_status": row_status,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "missing_to_score": missing_to_score,
        }
        for row_id, arena, quantity, value, units, value_kind, web_source_id, row_status, missing_to_score in specs
    ]


def mts_missing_input_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("MISS3701_0_rho_PPN", "PPN/local metric", "rho_PPN", "R_iAB residual tensor for PPN metric observables", "MISSING_PARENT_RESIDUAL_TENSOR"),
        ("MISS3701_1_rho_Newton", "short-range Newton/R10", "rho_Newton", "R_iAB residual tensor for Newtonian potential/force", "MISSING_PARENT_RESIDUAL_TENSOR"),
        ("MISS3701_2_rho_EM", "Maxwell/EM/Poynting stress", "rho_EM", "R_iAB residual tensor for T_EM, alpha_fs, Poynting flux", "MISSING_PARENT_RESIDUAL_TENSOR"),
        ("MISS3701_3_rho_clock", "precision clocks/time", "rho_clock", "clock observable residual tensor and Gamma_kappa convention", "MISSING_PARENT_RESIDUAL_TENSOR"),
        ("MISS3701_4_rho_WEP", "WEP/species", "rho_species_a_minus_b", "composition/species score residual difference", "MISSING_SPECIES_SCORE_MAP"),
        ("MISS3701_5_z2_bound", "all local arenas", "z2_bound", "C_H, J_y+B_y, mu_H, edge, boundary sourced values", "MISSING_PARENT_AMPLITUDE"),
        ("MISS3701_6_Kperp", "PPN/local metric", "Kperp_norm", "tensor residual exact-zero/cubic/bound theorem", "MISSING_TENSOR_GATE"),
        ("MISS3701_7_q_loc", "PPN/local metric", "q_loc_norm", "Green-function projection of local current", "MISSING_LOCAL_CURRENT_SOLVER"),
        ("MISS3701_8_R10_curve", "short-range Newton/R10", "alpha_bound(lambda)", "full digitized or machine-readable alpha-lambda bound curve", "MISSING_FULL_BOUND_CURVE"),
        ("MISS3701_9_orbital_kernel", "orbital dynamics", "K_orbit", "orbital sensitivity kernel and ephemeris tolerance choice", "MISSING_ORBITAL_PROJECTION"),
    ]
    return [
        {
            **base(timestamp),
            "missing_id": missing_id,
            "arena": arena,
            "input_name": input_name,
            "needed_object": needed_object,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for missing_id, arena, input_name, needed_object, status in specs
    ]


def residual_matrix_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "RM3701_0_PPN_gamma",
            "PPN/local metric",
            "S_gamma <= 0.5 rho_PPN z2_bound + K_Kperp||Kperp||/N_PPN + K_q||q_loc||/N_PPN",
            "SRC3701_PPN_gamma_sigma",
            "MISS3701_0_rho_PPN;MISS3701_5_z2_bound;MISS3701_6_Kperp;MISS3701_7_q_loc",
            "EXTERNAL_NORMALIZER_PARTIAL_MTS_SIDE_MISSING",
        ),
        (
            "RM3701_1_R10_anchor",
            "short-range Newton/R10",
            "abs(alpha_eff(lambda_H)) <= alpha_bound_R10(lambda_H); anchor only: alpha=1 excluded for lambda above 38.6 micrometer",
            "SRC3701_R10_lambda_alpha1_anchor",
            "MISS3701_1_rho_Newton;MISS3701_5_z2_bound;MISS3701_8_R10_curve",
            "ANCHOR_ONLY_MTS_SIDE_AND_FULL_CURVE_MISSING",
        ),
        (
            "RM3701_2_clock",
            "precision clocks/time",
            "|delta nu/nu| <= 0.5 rho_clock z2_bound + clock_projection_error",
            "SRC3701_CLOCK_gradient_sys_stat_combined",
            "MISS3701_3_rho_clock;MISS3701_5_z2_bound",
            "EXTERNAL_NORMALIZER_PARTIAL_MTS_SIDE_MISSING",
        ),
        (
            "RM3701_3_EM_alpha",
            "Maxwell/EM/Poynting stress",
            "max(|Delta alpha_fs/alpha_fs|, ||Delta T_EM||/||T_EM||, ||Delta S_EM||/||S_EM||) <= EM tolerance",
            "SRC3701_EM_alpha_std_uncertainty",
            "MISS3701_2_rho_EM;MISS3701_5_z2_bound",
            "CONSTANT_ANCHOR_READY_EM_RESIDUAL_MISSING",
        ),
        (
            "RM3701_4_WEP",
            "WEP/species",
            "eta_species <= 0.5 ||rho_species_a-rho_species_b|| z2_bound + species_projection_error",
            "SRC3701_WEP_eta_precision",
            "MISS3701_4_rho_WEP;MISS3701_5_z2_bound",
            "EXTERNAL_NORMALIZER_PARTIAL_MTS_SIDE_MISSING",
        ),
        (
            "RM3701_5_orbital",
            "orbital dynamics",
            "orbital residual <= K_orbit * 0.5 rho_Newton z0^2 exp(-2r/lambda_H)(1+r/lambda_H)^2 + boundary terms",
            "WEB3701_GR_WillReview",
            "MISS3701_1_rho_Newton;MISS3701_5_z2_bound;MISS3701_9_orbital_kernel",
            "REVIEW_CONTEXT_ONLY_ORBITAL_KERNEL_MISSING",
        ),
    ]
    return [
        {
            **base(timestamp),
            "matrix_id": matrix_id,
            "arena": arena,
            "bound_formula": formula,
            "external_source_or_row": external_source,
            "missing_mts_inputs": missing_inputs,
            "matrix_status": status,
            "arena_score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for matrix_id, arena, formula, external_source, missing_inputs, status in specs
    ]


def score_readiness_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("READY3701_0_R10", "short-range Newton/R10", True, False, False, "R10 has a real alpha=1/lambda anchor, but not a full alpha_bound(lambda) curve and no MTS alpha/lambda rows."),
        ("READY3701_1_PPN", "PPN/local metric", True, False, False, "Cassini gamma normalizer exists, but PPN vector projection, Kperp, q_loc, and rho_PPN are missing."),
        ("READY3701_2_clock", "precision clocks/time", True, False, False, "Clock redshift normalizer exists, but clock residual tensor and convention are missing."),
        ("READY3701_3_EM", "Maxwell/EM/Poynting stress", True, False, False, "NIST alpha anchor exists, but EM/Poynting residual tensor and alpha-source silence row are missing."),
        ("READY3701_4_WEP", "WEP/species", True, False, False, "MICROSCOPE precision exists, but species residual difference map is missing."),
        ("READY3701_5_orbital", "orbital dynamics", False, False, False, "Only review context is attached; orbital kernel/tolerance source row is not ready."),
    ]
    return [
        {
            **base(timestamp),
            "readiness_id": readiness_id,
            "arena": arena,
            "external_anchor_ready": external_ready,
            "mts_side_ready": mts_ready,
            "arena_score_ready": arena_ready,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for readiness_id, arena, external_ready, mts_ready, arena_ready, reason in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3701_0", "External local-test anchors acquired.", "R10, PPN gamma, WEP, alpha, and clock anchors now have source-backed rows.", "SOURCE_ANCHORS_ADVANCE"),
        ("DEC3701_1", "No local arena is score-ready yet.", "The external side is partly real, but every arena still lacks MTS residual tensors/amplitudes or full bound curves.", "CLAIM_BLOCKED"),
        ("DEC3701_2", "Next step should focus on one arena to completion.", "R10 is the cleanest first target because its external anchor/curve directly matches the Yukawa lambda_H branch.", "R10_FIRST_RECOMMENDED"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3701_0_external_sources", "external normalizer/source rows attached for all local arenas", "PARTIAL"),
        ("CG3701_1_mts_residuals", "rho_i residual tensors sourced/bounded", "BLOCKED"),
        ("CG3701_2_amplitude", "z2_bound sourced from parent mass-gap/amplitude rows", "BLOCKED"),
        ("CG3701_3_R10_full_curve", "full R10 alpha_bound(lambda) curve or machine-readable table", "BLOCKED"),
        ("CG3701_4_PPN_tensor", "Kperp and q_loc PPN projection bounded", "BLOCKED"),
        ("CG3701_5_public_claim", "public local-GR/Maxwell/Newton claim allowed", "BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for gate_id, requirement, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3701_0",
            "status": "LOCAL_TEST_EXTERNAL_SOURCE_ANCHORS_ACQUIRED_MTS_RESIDUAL_SIDE_STILL_MISSING",
            "summary": (
                "3701 converts the local-test gates into a source matrix. Public anchors now exist for R10/Newton, Cassini PPN gamma, MICROSCOPE WEP, "
                "NIST fine-structure alpha, and optical-clock redshift. These are deliberately nonclaim rows: they provide external normalizers and anchors, "
                "while MTS-side rho_i, z2_bound, Kperp, q_loc, full R10 curve, EM/Poynting residual tensors, and orbital kernels remain missing."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3701_0",
            "target_doc": "3702-Y5-R2FR-R10-bound-curve-digitizer-and-MTS-alpha-lambda-binder.md",
            "target_script": "scripts/Y5_R2FR_3702_R10_bound_curve_digitizer_and_MTS_alpha_lambda_binder.py",
            "objective": "turn the R10 anchor into a real alpha_bound(lambda) curve/table if possible, and bind symbolic MTS alpha_eff(lambda_H) rows to the 3700 residual formula without allowing claims",
            "success_gate": "R10 becomes score-ready as a nonclaim smoke arena, or the blocker is narrowed to a named missing curve/digitization source",
            "claim_allowed": False,
        }
    ]


def write_doc(
    web_sources: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    missing_rows: list[dict[str, object]],
    residual_matrix: list[dict[str, object]],
    readiness: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3701 Y5 R2FR Local Test Source Row Acquisition And Residual Matrix",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- The external side of the local-test matrix is now partly source-backed.",
        "- R10/Newton has a real Eot-Wash anchor: alpha=1 Yukawa interactions are limited to ranges below `38.6 micrometer` at 95% confidence, but this is anchor-only, not a full curve.",
        "- PPN has a Cassini gamma normalizer: `gamma-1=(2.1 +/- 2.3)e-5`.",
        "- WEP has a MICROSCOPE precision anchor of order `eta ~ 1e-15`.",
        "- EM has the NIST/CODATA fine-structure anchor `alpha=7.2973525643e-3` and standard uncertainty `1.1e-12`.",
        "- Clocks have a lab redshift-gradient uncertainty anchor `~2.6e-19 fractional_frequency_per_cm`.",
        "",
        "## Claim Discipline",
        "",
        "- None of these source rows prove MTS local recovery.",
        "- They only provide external normalizers. The MTS side still needs `rho_i`, `z2_bound`, `Kperp`, `q_loc`, full R10 curve, EM/Poynting residual tensors, and orbital kernels.",
        "",
        "## External Web Sources",
        "",
    ]
    for row in web_sources:
        lines.append(f"- `{row['web_source_id']}`: {row['arena']} | {row['key_value']} | {row['url']}")
    lines.extend(["", "## Local Test Source Rows", ""])
    for row in source_rows:
        lines.append(f"- `{row['source_row_id']}`: {row['arena']} | {row['quantity']}={row['numeric_value']} {row['units']} | `{row['row_status']}`")
    lines.extend(["", "## Residual Matrix Rows", ""])
    for row in residual_matrix:
        lines.append(f"- `{row['matrix_id']}`: {row['arena']} | `{row['matrix_status']}` | missing `{row['missing_mts_inputs']}`")
    lines.extend(["", "## Missing MTS Inputs", ""])
    for row in missing_rows:
        lines.append(f"- `{row['missing_id']}`: {row['arena']} | `{row['input_name']}` | `{row['status']}`")
    lines.extend(["", "## Score Readiness", ""])
    for row in readiness:
        lines.append(f"- `{row['readiness_id']}`: {row['arena']} | external={row['external_anchor_ready']} mts={row['mts_side_ready']} score={row['arena_score_ready']} | {row['reason']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']} | {row['rationale']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    local_sources: list[dict[str, object]],
    web_sources: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    missing_rows: list[dict[str, object]],
    residual_matrix: list[dict[str, object]],
    readiness: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("local_sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in local_sources), ""))
    checks.append(("local_needles_found", "all local source needles found", all(bool(row["needle_found"]) for row in local_sources), ""))
    checks.append(("web_urls_present", "all web source rows have URLs", all(str(row["url"]).startswith("http") for row in web_sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    numeric_positive = all(float(row["numeric_value"]) > 0 for row in source_rows)
    checks.append(("numeric_rows_positive", "all source numeric values are positive", numeric_positive, ""))
    checks.append(("enough_external_anchors", "at least five external anchors attached", len(web_sources) >= 5 and len(source_rows) >= 5, ""))
    r10_rows = [row for row in source_rows if row["arena"] == "short-range Newton/R10"]
    checks.append(("r10_anchor_nonclaim", "R10 rows are anchor-only/nonclaim", any(row["row_status"] == "anchor_only_non_curve" for row in r10_rows) and all(row["valid_for_claim"] is False for row in r10_rows), ""))
    checks.append(("all_source_rows_nonclaim", "all source rows are nonclaim", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in source_rows), ""))
    checks.append(("missing_inputs_isolated", "missing MTS input rows are explicit", len(missing_rows) >= 8 and any(row["input_name"] == "z2_bound" for row in missing_rows), ""))
    checks.append(("matrix_all_not_ready", "residual matrix arenas are not score-ready", all(row["arena_score_ready"] is False for row in residual_matrix), ""))
    checks.append(("readiness_external_partial", "some external anchors ready but no MTS side ready", any(row["external_anchor_ready"] is True for row in readiness) and all(row["mts_side_ready"] is False for row in readiness), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked_or_partial", "claim gates are partial or blocked and nonclaim", all(row["status"] in {"BLOCKED", "PARTIAL"} and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3702", "next target advances to R10 curve/binder", str(next_target[0]["target_doc"]).startswith("3702-") and "R10" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains source matrix core terms", all(term in doc_text for term in ["38.6 micrometer", "Cassini", "MICROSCOPE", "fine-structure", "rho_i", "z2_bound"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3701*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3701 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    local_sources = local_source_register(timestamp)
    web_sources = web_source_rows(timestamp)
    source_rows = local_test_source_rows(timestamp)
    missing_rows = mts_missing_input_rows(timestamp)
    residual_matrix = residual_matrix_rows(timestamp)
    readiness = score_readiness_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "local_sources": RESIDUALS / "P8_Y5_R2FR_3701_LOCAL_SOURCE_REGISTER.csv",
        "web_sources": RESIDUALS / "P8_Y5_R2FR_3701_WEB_SOURCE_ROWS.csv",
        "source_rows": RESIDUALS / "P8_Y5_R2FR_3701_LOCAL_TEST_SOURCE_ROWS.csv",
        "missing": RESIDUALS / "P8_Y5_R2FR_3701_MISSING_MTS_INPUT_ROWS.csv",
        "matrix": RESIDUALS / "P8_Y5_R2FR_3701_RESIDUAL_MATRIX_ROWS.csv",
        "readiness": RESIDUALS / "P8_Y5_R2FR_3701_SCORE_READINESS_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3701_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3701_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3701_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3701_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3701_VALIDATION.csv",
    }

    write_csv(outputs["local_sources"], local_sources)
    write_csv(outputs["web_sources"], web_sources)
    write_csv(outputs["source_rows"], source_rows)
    write_csv(outputs["missing"], missing_rows)
    write_csv(outputs["matrix"], residual_matrix)
    write_csv(outputs["readiness"], readiness)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(web_sources, source_rows, missing_rows, residual_matrix, readiness, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, local_sources, web_sources, source_rows, missing_rows, residual_matrix, readiness, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3701 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3701 checkpoint: local-test external source matrix attached; MTS-side residual rows isolated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
