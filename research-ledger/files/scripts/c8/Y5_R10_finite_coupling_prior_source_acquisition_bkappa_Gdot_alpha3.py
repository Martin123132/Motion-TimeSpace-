from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "981-Y5-R10-finite-coupling-prior-source-acquisition-bkappa-Gdot-alpha3.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def local_source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "980_doc",
            "path": "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md",
            "role": "handoff: no-marker theorem failed globally and finite coupling priors are needed",
            "needle": "DEC980_3_best_next",
        },
        {
            "source_id": "980_fallback",
            "path": "source-intake/mts_residuals/P8_Y5_R10_980_FINITE_PRIOR_FALLBACK.csv",
            "role": "local finite-prior fallback rows",
            "needle": "FP980_0_b_kappa_species_split",
        },
        {
            "source_id": "979_prior_priority",
            "path": "source-intake/mts_residuals/P8_Y5_R10_979_QBAR_PRIOR_SOURCE_PRIORITY.csv",
            "role": "earlier coupling-prior source priority",
            "needle": "QPRI979_2_K_boundary_alpha3",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "local alpha3/Gdot anchor rows needing source hardening",
            "needle": "alpha3_flux",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def web_source_rows() -> list[dict[str, str]]:
    return [
        {
            "web_source_id": "WEB981_0_MICROSCOPE_WEP",
            "title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
            "authors_or_collaboration": "Touboul et al. / MICROSCOPE",
            "year": "2022",
            "url": "https://arxiv.org/abs/2209.15487",
            "doi_or_journal": "Phys. Rev. Lett. 129, 121102; DOI https://doi.org/10.1103/PhysRevLett.129.121102",
            "source_type": "primary_result_preprint_and_PRL",
            "extracted_quantity": "eta(Ti,Pt)",
            "value": "-1.5e-15",
            "uncertainty_stat": "2.3e-15",
            "uncertainty_syst": "1.5e-15",
            "units": "dimensionless",
            "confidence_or_note": "1 sigma statistical and systematic errors reported separately; use only as WEP/source-splitting anchor",
            "extraction_method": "arXiv abstract/source metadata checked online 2026-06-14",
            "valid_for_claim": "false",
        },
        {
            "web_source_id": "WEB981_1_LLR_GDOT",
            "title": "Benefit of New High-Precision LLR Data for the Determination of Relativistic Parameters",
            "authors_or_collaboration": "Biskupek, Mueller, Torre",
            "year": "2021",
            "url": "https://arxiv.org/abs/2012.12032",
            "doi_or_journal": "Universe 7(2), 34; DOI https://doi.org/10.3390/universe7020034",
            "source_type": "primary_LLR_analysis",
            "extracted_quantity": "Gdot/G0",
            "value": "-5.0e-15",
            "uncertainty_stat": "9.6e-15",
            "uncertainty_syst": "",
            "units": "yr^-1",
            "confidence_or_note": "reported uncertainty; local 417 anchor appears to use 9.6e-15 yr^-1 as an uncertainty-scale bound",
            "extraction_method": "arXiv abstract/source metadata checked online 2026-06-14",
            "valid_for_claim": "false",
        },
        {
            "web_source_id": "WEB981_2_ALPHA3_STRONG_PULSAR",
            "title": "Discovery of Three Wide-orbit Binary Pulsars: Implications for Binary Evolution and Equivalence Principles",
            "authors_or_collaboration": "Stairs et al.",
            "year": "2005",
            "url": "https://arxiv.org/abs/astro-ph/0506188",
            "doi_or_journal": "Astrophysical Journal source via arXiv",
            "source_type": "primary_pulsar_bound",
            "extracted_quantity": "strong-field alpha3_hat upper limit",
            "value": "4.0e-20",
            "uncertainty_stat": "",
            "uncertainty_syst": "",
            "units": "dimensionless",
            "confidence_or_note": "95 percent upper limit on alpha3_hat; not automatically identical to weak-field local PPN alpha3",
            "extraction_method": "arXiv abstract/source metadata checked online 2026-06-14",
            "valid_for_claim": "false",
        },
        {
            "web_source_id": "WEB981_3_ALPHA3_WEAK_SOLAR",
            "title": "Orbital motions and the conservation-law/preferred-frame alpha3 parameter",
            "authors_or_collaboration": "Iorio",
            "year": "2014",
            "url": "https://arxiv.org/abs/1309.7149",
            "doi_or_journal": "Galaxies 2(4), 482-495; DOI https://doi.org/10.3390/galaxies2040482",
            "source_type": "weak_field_solar_system_analysis",
            "extracted_quantity": "weak-field alpha3 upper estimate",
            "value": "6.0e-10",
            "uncertainty_stat": "",
            "uncertainty_syst": "",
            "units": "dimensionless",
            "confidence_or_note": "preliminary weak-field bound using supplementary perihelion precessions; less tight than pulsar alpha3_hat but closer to local PPN context",
            "extraction_method": "arXiv/MDPI source metadata checked online 2026-06-14",
            "valid_for_claim": "false",
        },
    ]


def candidate_prior_rows(web_sources: list[dict[str, str]]) -> list[dict[str, str]]:
    microscope_sigma = math.sqrt((2.3e-15) ** 2 + (1.5e-15) ** 2)
    microscope_approx_2sigma = abs(-1.5e-15) + 2.0 * microscope_sigma
    gdot_approx_2sigma = abs(-5.0e-15) + 2.0 * 9.6e-15
    return [
        {
            "prior_id": "CP981_0_b_kappa_species_split_WEP",
            "component": "b_kappa",
            "observable_channel": "WEP/source-composition",
            "source_id": "WEB981_0_MICROSCOPE_WEP",
            "candidate_value": f"{microscope_approx_2sigma:.3e}",
            "candidate_units": "dimensionless",
            "candidate_convention": "rough |central|+2*sqrt(stat^2+syst^2) screening envelope from eta(Ti,Pt); not a derived MTS coefficient",
            "MTS_projection_status": "MISSING_SOURCE_CHARGE_PROJECTION",
            "claim_status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP981_1_kappa_running_Gdot",
            "component": "b_kappa",
            "observable_channel": "Gdot/orbital/local-time drift",
            "source_id": "WEB981_1_LLR_GDOT",
            "candidate_value": f"{gdot_approx_2sigma:.3e}",
            "candidate_units": "yr^-1",
            "candidate_convention": "rough |central|+2*sigma screening envelope from LLR Gdot/G0; not an MTS drift profile",
            "MTS_projection_status": "MISSING_ENVIRONMENT_PROFILE_AND_XHAT_TIME_MAP",
            "claim_status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP981_2_alpha3_strong_pulsar",
            "component": "boundary_alpha3_flux",
            "observable_channel": "strong-field pulsar preferred-frame/conservation-law",
            "source_id": "WEB981_2_ALPHA3_STRONG_PULSAR",
            "candidate_value": "4.000e-20",
            "candidate_units": "dimensionless",
            "candidate_convention": "95 percent upper limit on alpha3_hat; keep separate from local weak-field alpha3",
            "MTS_projection_status": "MISSING_STRONG_TO_LOCAL_PPN_PROJECTION",
            "claim_status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP981_3_alpha3_weak_solar",
            "component": "boundary_alpha3_flux",
            "observable_channel": "weak-field solar-system preferred-frame",
            "source_id": "WEB981_3_ALPHA3_WEAK_SOLAR",
            "candidate_value": "6.000e-10",
            "candidate_units": "dimensionless",
            "candidate_convention": "preliminary weak-field bound; useful as context but much weaker than pulsar alpha3_hat",
            "MTS_projection_status": "MISSING_BOUNDARY_ALPHA3_PROJECTION_MATRIX",
            "claim_status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def local_anchor_reconciliation_rows() -> list[dict[str, str]]:
    return [
        {
            "anchor_id": "LAR981_0_417_Gdot",
            "local_anchor": "417 Gdot_drift = 9.600e-15 yr^-1",
            "web_source_match": "WEB981_1_LLR_GDOT reports uncertainty 9.6e-15 yr^-1 around central -5.0e-15 yr^-1",
            "reconciliation": "local row appears to store the 1 sigma uncertainty scale, not a conservative absolute bound",
            "action": "replace claim language with convention-labelled screening envelope before scoring",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "LAR981_1_417_alpha3",
            "local_anchor": "417 alpha3_flux = 4.000e-20 dimensionless",
            "web_source_match": "WEB981_2_ALPHA3_STRONG_PULSAR gives alpha3_hat 95 percent upper limit 4.0e-20",
            "reconciliation": "source is strong-field pulsar alpha3_hat; not automatically a weak-field local boundary alpha3 coefficient",
            "action": "keep separate from weak-field solar alpha3 and require projection before use",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "LAR981_2_WEP_source_split",
            "local_anchor": "979/980 b_kappa species_source_weight_splitting needs external bound",
            "web_source_match": "WEB981_0_MICROSCOPE_WEP gives Ti/Pt Eotvos result at 10^-15 scale",
            "reconciliation": "good first WEP anchor, but maps to b_kappa only through composition/source-charge sensitivity matrix",
            "action": "source composition sensitivities or derive universal Hilbert source before scoring",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE981_0_source_provenance",
            "claim": "external source rows have usable provenance",
            "gate_pass": "true",
            "claim_allowed": "false",
            "why_not": "provenance exists, but MTS coefficient projection is missing",
        },
        {
            "gate_id": "CGATE981_1_numeric_MTS_priors",
            "claim": "candidate values are valid MTS priors",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "candidate values are observational anchors, not projected MTS coefficient bounds",
        },
        {
            "gate_id": "CGATE981_2_b_kappa_bound",
            "claim": "b_kappa species/source splitting is bounded",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "composition/source-charge projection matrix is missing",
        },
        {
            "gate_id": "CGATE981_3_alpha3_bound",
            "claim": "K_boundary_alpha3 is bounded for MTS local branch",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "strong-field alpha3_hat and weak-field alpha3 need separate projection conventions",
        },
        {
            "gate_id": "CGATE981_4_local_GR",
            "claim": "R10/WEP/PPN/local-GR branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source acquisition only; no runner scoring or parent derivation",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC981_0_source_acquisition",
            "topic": "finite coupling priors",
            "result": "source_backed_observational_anchors_acquired",
            "reason": "MICROSCOPE, LLR Gdot, pulsar alpha3_hat, and solar alpha3 sources are recorded",
            "next_action": "derive projection maps from observational anchors to MTS residual coefficients",
        },
        {
            "decision_id": "DEC981_1_alpha3_policy",
            "topic": "alpha3",
            "result": "split_strong_and_weak_alpha3",
            "reason": "4e-20 is strong-field alpha3_hat; weak-field solar-system alpha3 is much weaker but context-closer",
            "next_action": "do not use pulsar alpha3_hat as local PPN prior without a projection argument",
        },
        {
            "decision_id": "DEC981_2_Gdot_policy",
            "topic": "Gdot",
            "result": "local_anchor_relabel_needed",
            "reason": "417's 9.6e-15 yr^-1 matches the LLR uncertainty scale, not a full conservative absolute envelope",
            "next_action": "store both central value and chosen envelope convention before any scoring",
        },
        {
            "decision_id": "DEC981_3_best_next",
            "topic": "next checkpoint",
            "result": "projection_matrix_or_screening_runner",
            "reason": "we now have source anchors; the blocker is mapping them into b_kappa, K_boundary_alpha3, and local residual vector components",
            "next_action": "write 982 coupling-bound projection matrix skeleton and nonclaim screening runner",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "982-Y5-R10-coupling-bound-projection-matrix-skeleton-and-screening-runner.md",
            "objective": "map WEP/Gdot/alpha3 observational anchors into explicit MTS residual coefficient slots without claiming a pass",
            "include": "composition/source-charge projection placeholders, Gdot-to-Xhat environment map, strong-vs-weak alpha3 split, screening-only runner",
            "exclude": "local-GR pass, theorem-zero promotion, invented projection coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    local_sources: list[dict[str, str]],
    web_sources: list[dict[str, str]],
    priors: list[dict[str, str]],
    anchors: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    local_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in local_sources)
    web_urls_ok = all(row["url"].startswith("https://") and row["doi_or_journal"] for row in web_sources)
    web_values_ok = all(float(row["value"]) or row["value"] == "0" for row in web_sources)
    units_ok = all(row["units"] in {"dimensionless", "yr^-1"} for row in web_sources)
    web_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in web_sources)
    prior_nonclaim_ok = all(row["valid_for_claim"] == "false" and row["claim_status"] == "blocked_nonclaim" for row in priors)
    projection_missing_ok = all(row["MTS_projection_status"].startswith("MISSING_") for row in priors)
    anchor_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in anchors)
    claims_ok = all(row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC981_3_best_next" and row["result"] == "projection_matrix_or_screening_runner" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {
            "check_id": "V981_0_local_sources",
            "result": "pass" if local_ok else "fail",
            "detail": "local handoff/source anchors exist and needles are found",
        },
        {
            "check_id": "V981_1_web_source_urls",
            "result": "pass" if web_urls_ok else "fail",
            "detail": "web source URLs and DOI/journal strings are recorded",
        },
        {
            "check_id": "V981_2_web_values_numeric",
            "result": "pass" if web_values_ok else "fail",
            "detail": "web source extracted values parse as numeric",
        },
        {
            "check_id": "V981_3_units_recognized",
            "result": "pass" if units_ok else "fail",
            "detail": "all web source units are recognized",
        },
        {
            "check_id": "V981_4_web_sources_nonclaim",
            "result": "pass" if web_nonclaim_ok else "fail",
            "detail": "all web source rows remain valid_for_claim=false",
        },
        {
            "check_id": "V981_5_candidate_priors_nonclaim",
            "result": "pass" if prior_nonclaim_ok else "fail",
            "detail": "candidate priors are blocked nonclaim rows",
        },
        {
            "check_id": "V981_6_projection_missing",
            "result": "pass" if projection_missing_ok else "fail",
            "detail": "every candidate prior still requires an MTS projection map",
        },
        {
            "check_id": "V981_7_anchor_reconciliation_nonclaim",
            "result": "pass" if anchor_nonclaim_ok else "fail",
            "detail": "local anchor reconciliations remain nonclaim",
        },
        {
            "check_id": "V981_8_claim_gates_safe",
            "result": "pass" if claims_ok else "fail",
            "detail": "claim gates do not allow local-GR or coefficient-bound claims",
        },
        {
            "check_id": "V981_9_decision_next_target",
            "result": "pass" if decisions_ok else "fail",
            "detail": "982 projection matrix/screening runner selected",
        },
        {
            "check_id": "V981_10_next_target_written",
            "result": "pass" if next_ok else "fail",
            "detail": "next target row is present and nonclaim",
        },
        {
            "check_id": "V981_11_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
        },
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V981_READY",
            "result": "pass" if ready else "fail",
            "detail": "981 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    local_sources: list[dict[str, str]],
    web_sources: list[dict[str, str]],
    priors: list[dict[str, str]],
    anchors: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 981 Y5 R10: Finite Coupling Prior Source Acquisition b_kappa Gdot alpha3",
        "",
        "Status: `Y5_R10_981_source_backed_observational_anchors_acquired_nonclaim_projection_maps_missing`",
        "",
        "Claim ceiling: source acquisition only. No `b_kappa` bound, no `K_boundary_alpha3` bound, no `qbar` pass, no WEP/PPN/local-GR pass, and no public claim.",
        "",
        "## Readout",
        "",
        "After 980, continuous constants cannot honestly be theorem-zeroed by the no-marker functor route. 981 therefore hardens the first finite local coupling anchors from external sources, while keeping every row nonclaim until the projection from observation to MTS coefficient is derived.",
        "",
        "The key caution is alpha3: the tight `4.0e-20` number is a strong-field pulsar `alpha3_hat` bound, not automatically the weak-field local PPN boundary coefficient. The weak-field solar-system alpha3 bound is much weaker but context-closer. Both are retained separately.",
        "",
        "## Local Source Register",
        "",
        md_table(local_sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Web Source Ledger",
        "",
        md_table(web_sources, ["web_source_id", "title", "year", "url", "doi_or_journal", "extracted_quantity", "value", "units", "confidence_or_note", "valid_for_claim"]),
        "",
        "## Candidate Coupling Priors",
        "",
        md_table(priors, ["prior_id", "component", "observable_channel", "source_id", "candidate_value", "candidate_units", "candidate_convention", "MTS_projection_status", "valid_for_claim"]),
        "",
        "## Local Anchor Reconciliation",
        "",
        md_table(anchors, ["anchor_id", "local_anchor", "web_source_match", "reconciliation", "action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    local_sources = local_source_register()
    web_sources = web_source_rows()
    priors = candidate_prior_rows(web_sources)
    anchors = local_anchor_reconciliation_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(local_sources, web_sources, priors, anchors, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_981_LOCAL_SOURCE_REGISTER.csv", local_sources)
    write_csv(OUT / "P8_Y5_R10_981_WEB_SOURCE_LEDGER.csv", web_sources)
    write_csv(OUT / "P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv", priors)
    write_csv(OUT / "P8_Y5_R10_981_LOCAL_ANCHOR_RECONCILIATION.csv", anchors)
    write_csv(OUT / "P8_Y5_R10_981_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_981_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_981_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_981_VALIDATION.csv", validation)
    write_doc(local_sources, web_sources, priors, anchors, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
