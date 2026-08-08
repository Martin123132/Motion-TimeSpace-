from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "628-Y5-R10-real-local-bound-input-sources-for-cg-or-Zcg-proof.md"
SCRIPT_REL = "scripts/Y5_R10_real_local_bound_input_sources_for_cg_or_Zcg_proof.py"
STATUS = "Y5_R10_real_local_bound_sources_acquired_as_nonclaim_candidates_cg_and_Zcg_still_unsourced"
CLAIM_CEILING = "source_acquisition_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md", "immediate handoff: Z_cg false and c_g acquisition ledger"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_627_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_627_CG_ACQUISITION_LEDGER.csv", "required c_g/local inputs"),
        ("source-intake/mts_residuals/P8_Y5_R10_627_ARENA_BLOCKER_MATRIX.csv", "arena blockers"),
        ("source-intake/mts_residuals/P8_Y5_R10_627_SOURCE_REQUIREMENTS.csv", "source requirements"),
        ("626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md", "descent criterion and c_g bound schema"),
        ("625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md", "representative Weyl/disformal source branch"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_external_source_candidates() -> list[dict[str, object]]:
    return [
        {
            "source_id": "EXT628_0_R10_EOTWASH_2020_PRL",
            "arena": "R10",
            "needed_input": "alpha_bound_lambda",
            "title": "New Test of the Gravitational 1/r^2 Law at Separations down to 52 micrometers",
            "authors_year": "Lee, Adelberger, Cook, Fleischer, Heckel 2020",
            "url": "https://doi.org/10.1103/PhysRevLett.124.101101",
            "doi": "10.1103/PhysRevLett.124.101101",
            "extracted_value": "alpha=1 anchor: lambda < 38.6 micrometer at 95% confidence; separations 52 micrometer to 3.0 mm",
            "extraction_method": "abstract_anchor_only_not_full_curve",
            "source_confidence": "high_for_anchor_low_for_curve",
            "source_status": "source_candidate_anchor_only",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT628_1_R10_EOTWASH_2020_ARXIV",
            "arena": "R10",
            "needed_input": "alpha_bound_lambda",
            "title": "arXiv full text for Eot-Wash 2020 inverse-square-law test",
            "authors_year": "Lee et al. 2020",
            "url": "https://arxiv.org/abs/2002.11761",
            "doi": "10.1103/PhysRevLett.124.101101",
            "extracted_value": "candidate full-curve figure source; not digitized in this checkpoint",
            "extraction_method": "source_located_not_digitized",
            "source_confidence": "high_for_paper_low_for_machine_curve",
            "source_status": "full_curve_digitization_candidate",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT628_2_PPN_CASSINI_2003",
            "arena": "PPN",
            "needed_input": "tau_PPN_or_PPN_baseline",
            "title": "A test of general relativity using radio links with the Cassini spacecraft",
            "authors_year": "Bertotti, Iess, Tortora 2003",
            "url": "https://doi.org/10.1038/nature01997",
            "doi": "10.1038/nature01997",
            "extracted_value": "gamma - 1 = (2.1 +/- 2.3)e-5",
            "extraction_method": "published_summary_value",
            "source_confidence": "high_for_PPN_baseline_not_tau_projection",
            "source_status": "baseline_candidate_not_cg_projection",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT628_3_ORBITAL_LLR_2018",
            "arena": "orbital_PPN",
            "needed_input": "tau_orbital_or_orbital_baseline",
            "title": "Relativistic tests with lunar laser ranging",
            "authors_year": "Hofmann and Muller 2018",
            "url": "https://doi.org/10.1088/1361-6382/aa8f7a",
            "doi": "10.1088/1361-6382/aa8f7a",
            "extracted_value": "Gdot/G=(7.1 +/- 7.6)e-14 yr^-1; beta-1=(-4.5 +/- 5.6)e-5; gamma-1=(-1.2 +/- 1.2)e-4",
            "extraction_method": "abstract_values",
            "source_confidence": "high_for_orbital_baseline_not_tau_projection",
            "source_status": "baseline_candidate_not_cg_projection",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT628_4_CLOCK_ROSENBAND_2008",
            "arena": "clock",
            "needed_input": "tau_clock_or_clock_baseline",
            "title": "Frequency ratio of Al+ and Hg+ single-ion optical clocks; metrology at the 17th decimal place",
            "authors_year": "Rosenband et al. 2008",
            "url": "https://www.nist.gov/publications/frequency-ratio-al-and-hg-single-ion-optical-clocks-metrology-17th-decimal-place",
            "doi": "10.1126/science.1154622",
            "extracted_value": "alpha_dot/alpha=(1.4 +/- 1.7)e-17 yr^-1 preliminary constraint",
            "extraction_method": "NIST_publication_page",
            "source_confidence": "high_for_clock_constant_drift_not_tau_clock",
            "source_status": "baseline_candidate_not_cg_projection",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT628_5_WEP_MICROSCOPE_2022",
            "arena": "WEP_side_constraint",
            "needed_input": "composition_baseline_optional",
            "title": "MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle",
            "authors_year": "Touboul et al. 2022",
            "url": "https://doi.org/10.1103/PhysRevLett.129.121102",
            "doi": "10.1103/PhysRevLett.129.121102",
            "extracted_value": "eta(Ti,Pt)=(-1.5 +/- 2.3 stat +/- 1.5 syst)e-15",
            "extraction_method": "PubMed/arXiv summary value",
            "source_confidence": "high_for_WEP_baseline_not_cg_projection",
            "source_status": "side_constraint_candidate",
            "valid_for_claim": "false",
        },
    ]


def build_zcg_source_audit() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "ZSRC628_0_parent_q",
            "needed_proof": "parent quotient map q:Phi_parent -> Q_MTS",
            "source_found": "false",
            "source_candidate": "local contracts only from 626/627",
            "why_not_enough": "contract rows do not construct q from parent action",
            "Z_cg_status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ZSRC628_1_verticality",
            "needed_proof": "v_X in ker(Dq) on local matter branch",
            "source_found": "false",
            "source_candidate": "conditional rows from 623-627",
            "why_not_enough": "conditional verticality is not a parent theorem",
            "Z_cg_status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ZSRC628_2_matter_descent",
            "needed_proof": "S_matter=Sbar[q(Phi),Psi,theta]",
            "source_found": "false",
            "source_candidate": "conditional descent criterion in 626",
            "why_not_enough": "criterion is not an action derivation",
            "Z_cg_status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ZSRC628_3_no_representative_frame",
            "needed_proof": "no representative Weyl/disformal coefficients",
            "source_found": "false",
            "source_candidate": "625 exclusion lemma",
            "why_not_enough": "exclusion depends on unsigned quotient-invariant matter action",
            "Z_cg_status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ZSRC628_4_total",
            "needed_proof": "Z_cg=true",
            "source_found": "false",
            "source_candidate": "none",
            "why_not_enough": "zero proof remains local contract only",
            "Z_cg_status": "false",
            "valid_for_claim": "false",
        },
    ]


def build_acquisition_status_rows() -> list[dict[str, object]]:
    return [
        {
            "input_id": "SRCACQ628_0_Z_cg",
            "parameter": "Z_cg",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "local parent proof still missing",
            "candidate_value": "false",
            "units": "boolean",
            "claim_blocker": "parent proof unsigned",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_1_c_g",
            "parameter": "c_g",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "none; theory coefficient requires parent model or fit protocol",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "claim_blocker": "no parent coefficient or empirical mapping",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_2_tau_R10",
            "parameter": "tau_R10",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "Eot-Wash material/source geometry, but projection model absent",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "claim_blocker": "tau_R10 projection not derived",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_3_tau_PPN",
            "parameter": "tau_PPN",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "Cassini and LLR PPN baselines",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "claim_blocker": "tau_PPN projection not derived",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_4_tau_clock",
            "parameter": "tau_clock",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "Rosenband/NIST clock constraint",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "claim_blocker": "clock common-frame projection not derived",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_5_tau_orbital",
            "parameter": "tau_orbital",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "LLR orbital/PPN baseline",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "claim_blocker": "orbital common-frame projection not derived",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_6_K_X",
            "parameter": "K_X",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "none in external experimental sources; parent kernel needed",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "schema_required",
            "claim_blocker": "parent kernel missing",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_7_Qbar_XH",
            "parameter": "Qbar_XH",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "none in external experimental sources; parent projection needed",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "schema_required",
            "claim_blocker": "parent projection missing",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_8_lambda_X",
            "parameter": "lambda_X",
            "source_status_after_628": "not_sourced",
            "best_source_candidate": "Eot-Wash constrains Yukawa lambda externally but does not define parent lambda_X",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "length",
            "claim_blocker": "parent range missing",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SRCACQ628_9_alpha_bound_lambda",
            "parameter": "alpha_bound_lambda",
            "source_status_after_628": "anchor_candidate_only",
            "best_source_candidate": "Eot-Wash 2020 PRL/arXiv",
            "candidate_value": "alpha=1 excluded above lambda=38.6 micrometer; full curve not digitized",
            "units": "dimensionless_bound_vs_length",
            "claim_blocker": "anchor-only non-curve and other local inputs missing",
            "valid_for_claim": "false",
        },
    ]


def build_numeric_anchor_rows() -> list[dict[str, object]]:
    return [
        {
            "anchor_id": "ANCH628_0_R10_alpha1",
            "source_id": "EXT628_0_R10_EOTWASH_2020_PRL",
            "quantity": "alpha_equal_1_lambda_limit",
            "value": "38.6",
            "uncertainty": "not_extracted",
            "units": "micrometer",
            "meaning": "gravitational-strength Yukawa interaction range limit at 95 percent confidence",
            "use_status": "anchor_only_non_curve",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "ANCH628_1_R10_min_separation",
            "source_id": "EXT628_0_R10_EOTWASH_2020_PRL",
            "quantity": "minimum_detector_attractor_separation",
            "value": "52",
            "uncertainty": "not_extracted",
            "units": "micrometer",
            "meaning": "experimental separation lower end",
            "use_status": "context_only",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "ANCH628_2_PPN_Cassini_gamma",
            "source_id": "EXT628_2_PPN_CASSINI_2003",
            "quantity": "gamma_minus_one",
            "value": "2.1e-5",
            "uncertainty": "2.3e-5",
            "units": "dimensionless",
            "meaning": "Cassini PPN gamma baseline",
            "use_status": "baseline_not_tau_projection",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "ANCH628_3_LLR_gamma",
            "source_id": "EXT628_3_ORBITAL_LLR_2018",
            "quantity": "gamma_minus_one",
            "value": "-1.2e-4",
            "uncertainty": "1.2e-4",
            "units": "dimensionless",
            "meaning": "LLR PPN gamma baseline",
            "use_status": "baseline_not_tau_projection",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "ANCH628_4_CLOCK_alpha_dot",
            "source_id": "EXT628_4_CLOCK_ROSENBAND_2008",
            "quantity": "alpha_dot_over_alpha",
            "value": "1.4e-17",
            "uncertainty": "1.7e-17",
            "units": "yr^-1",
            "meaning": "clock constraint on temporal fine-structure variation",
            "use_status": "baseline_not_tau_clock",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "ANCH628_5_MICROSCOPE_eta",
            "source_id": "EXT628_5_WEP_MICROSCOPE_2022",
            "quantity": "eta_Ti_Pt",
            "value": "-1.5e-15",
            "uncertainty": "2.3e-15_stat_1.5e-15_syst",
            "units": "dimensionless",
            "meaning": "WEP side constraint candidate",
            "use_status": "side_constraint_not_cg_projection",
            "valid_for_claim": "false",
        },
    ]


def build_arena_source_status_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "ARENA628_0_R10",
            "source_status": "partial_anchor_found",
            "usable_now": "false",
            "blockers": "full alpha_bound(lambda) curve not digitized; c_g,tau_R10,K_X,Qbar_XH,lambda_X missing",
            "next_action": "digitize/source R10 bound curve or keep alpha=1 anchor nonclaim",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA628_1_PPN",
            "source_status": "baseline_sources_found",
            "usable_now": "false",
            "blockers": "tau_PPN, c_g, lambda_X/profile/M_PPN projection missing",
            "next_action": "derive PPN projection before scoring against Cassini/LLR",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA628_2_CLOCK",
            "source_status": "clock_baseline_source_found",
            "usable_now": "false",
            "blockers": "tau_clock, c_g, environment profile and clock sensitivity mapping missing",
            "next_action": "derive common-frame clock projection or keep clock source as baseline only",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA628_3_ORBITAL",
            "source_status": "LLR_baseline_source_found",
            "usable_now": "false",
            "blockers": "tau_orbital, c_g, lambda_X, source profile and orbital projection missing",
            "next_action": "derive orbital projection or use LLR only as future baseline",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA628_4_ZCG",
            "source_status": "not_found",
            "usable_now": "false",
            "blockers": "parent quotient-invariant matter action proof absent",
            "next_action": "return to derivation if a parent action candidate is supplied",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D628_0_main_verdict",
            "status": STATUS,
            "decision": "real local bound source candidates acquired, but no c_g or Z_cg source found",
            "meaning": "external sources provide arena baselines/anchors, not the parent coefficient or projection needed for claims",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D628_1_R10",
            "status": "R10_anchor_found_full_curve_needed",
            "decision": "use Eot-Wash 2020 as the R10 primary source candidate",
            "meaning": "alpha=1/lambda=38.6 micrometer is anchor-only; full alpha(lambda) curve still needs digitization/table extraction",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D628_2_local_baselines",
            "status": "PPN_clock_orbital_baselines_found",
            "decision": "record Cassini, LLR, Rosenband, and MICROSCOPE as baseline candidates",
            "meaning": "these are useful future comparators but not direct c_g projections",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D628_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no local claim",
            "meaning": "all candidate source rows remain nonclaim and arena rows remain blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU628_0_allowed",
            "allowed_after_628": "cite external sources as candidate anchors/baselines",
            "forbidden_after_628": "treat any source candidate as c_g or Z_cg proof",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU628_1_allowed",
            "allowed_after_628": "digitize/source the Eot-Wash alpha(lambda) curve before R10 scoring",
            "forbidden_after_628": "use alpha=1 anchor as a full bound curve",
            "next_action": "R10 curve digitization or source-backed table search",
        },
        {
            "route_id": "RU628_2_allowed",
            "allowed_after_628": "derive arena projection matrices before using PPN/clock/orbital baselines",
            "forbidden_after_628": "compare c_g to Cassini/LLR/clocks without tau_A and profile model",
            "next_action": "build c_g projection smoke runner after R10 curve handling",
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "external_sources_found": "true",
            "Z_cg_sourced": "false",
            "c_g_sourced": "false",
            "alpha_bound_lambda_full_curve_sourced": "false",
            "alpha_bound_lambda_anchor_found": "true",
            "PPN_baseline_found": "true",
            "clock_baseline_found": "true",
            "orbital_baseline_found": "true",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "clock_pass": "false",
            "orbital_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    local_sources: list[dict[str, object]],
    external_sources: list[dict[str, object]],
    zcg_audit: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    anchors: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_local = [row["source_file"] for row in local_sources if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_627_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]
    external_complete = all(row["url"] and row["source_status"] for row in external_sources)
    r10_anchor = any(row["anchor_id"] == "ANCH628_0_R10_alpha1" and row["use_status"] == "anchor_only_non_curve" for row in anchors)
    no_zcg = all(row["valid_for_claim"] == "false" for row in zcg_audit) and any(row["audit_id"] == "ZSRC628_4_total" and row["Z_cg_status"] == "false" for row in zcg_audit)
    acquisition_safe = all(not parse_bool(row["valid_for_claim"]) for row in acquisition_rows) and any(has_missing_marker(row) for row in acquisition_rows)
    anchors_nonclaim = all(not parse_bool(row["valid_for_claim"]) for row in anchors)
    arenas_blocked = all(row["usable_now"] == "false" and row["valid_for_claim"] == "false" for row in arena_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in external_sources + zcg_audit + acquisition_rows + anchors + arena_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V628_0_local_source_paths_exist",
            "result": "pass" if not missing_local else "fail",
            "detail": "missing=" + str(len(missing_local)) + ("; " + json.dumps(missing_local) if missing_local else ""),
        },
        {
            "check_id": "V628_1_prior_627_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V628_2_external_sources_recorded",
            "result": "pass" if external_complete and len(external_sources) >= 5 else "fail",
            "detail": f"external_rows={len(external_sources)};external_complete={external_complete}",
        },
        {
            "check_id": "V628_3_no_Zcg_or_cg_source_claim",
            "result": "pass" if no_zcg and acquisition_safe else "fail",
            "detail": f"no_zcg={no_zcg};acquisition_safe={acquisition_safe}",
        },
        {
            "check_id": "V628_4_R10_anchor_noncurve",
            "result": "pass" if r10_anchor and anchors_nonclaim else "fail",
            "detail": f"r10_anchor={r10_anchor};anchors_nonclaim={anchors_nonclaim}",
        },
        {
            "check_id": "V628_5_arenas_remain_blocked",
            "result": "pass" if arenas_blocked else "fail",
            "detail": f"arena_rows={len(arena_rows)};arenas_blocked={arenas_blocked}",
        },
        {
            "check_id": "V628_6_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V628_7_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["clock_pass"] == "false"
            and nonclaim["orbital_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["Z_cg_sourced"] == "false"
            and nonclaim["c_g_sourced"] == "false"
            else "fail",
            "detail": "Z_cg=false;c_g=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def write_doc(
    local_sources: list[dict[str, object]],
    external_sources: list[dict[str, object]],
    zcg_audit: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    anchors: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 628 Y5 R10 real local bound input sources for cg or Zcg proof

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- 628 acquired real external source candidates for local bound inputs, but it did **not** find a source for `Z_cg=true` or a numeric/theorem-zero `c_g`.
- Eot-Wash 2020 is the right R10 primary source candidate. It gives a strong anchor, but not a machine-ready full `alpha_bound(lambda)` curve in this checkpoint.
- Cassini, LLR, atomic-clock, and MICROSCOPE sources are useful baseline candidates. They do not by themselves define `tau_PPN`, `tau_clock`, `tau_orbital`, or the MTS projection matrix.
- Therefore every row remains nonclaim and every local arena remains blocked.

## What Was Actually Acquired
```text
R10 source candidate: Eot-Wash 2020 PRL/arXiv
R10 anchor: alpha=1 excluded above lambda=38.6 micrometer, noncurve
PPN baseline candidate: Cassini gamma
Orbital/PPN baseline candidate: LLR 2018
Clock baseline candidate: Rosenband/NIST Al+/Hg+ clock ratio
WEP side candidate: MICROSCOPE final result
```

What was **not** acquired:

```text
Z_cg=true parent proof
c_g numeric/theorem-zero source
tau_R10/tau_PPN/tau_clock/tau_orbital projection model
K_X/Qbar_XH/lambda_X parent inputs
full alpha_bound(lambda) curve
```

## Local Source Register
{md_table(local_sources)}

## External Source Candidates
{md_table(external_sources)}

## Z_cg Source Audit
{md_table(zcg_audit)}

## Acquisition Status
{md_table(acquisition_rows)}

## Nonclaim Numeric Anchors
{md_table(anchors)}

## Arena Source Status
{md_table(arena_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is progress, but it is not evidence yet. We now have real source handles for the local tests, especially R10. The next clean technical move is to digitize or otherwise source the Eot-Wash `alpha_bound(lambda)` curve and build a nonclaim projection smoke runner. Until `c_g`, `tau_A`, `K_X`, `Qbar_XH`, and `lambda_X` are sourced or zero-derived, no local arena can pass.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    local_sources = build_source_register()
    external_sources = build_external_source_candidates()
    zcg_audit = build_zcg_source_audit()
    acquisition_rows = build_acquisition_status_rows()
    anchors = build_numeric_anchor_rows()
    arena_rows = build_arena_source_status_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        local_sources,
        external_sources,
        zcg_audit,
        acquisition_rows,
        anchors,
        arena_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_628_SOURCE_REGISTER.csv", local_sources),
        ("P8_Y5_R10_628_EXTERNAL_SOURCE_CANDIDATES.csv", external_sources),
        ("P8_Y5_R10_628_ZCG_SOURCE_AUDIT.csv", zcg_audit),
        ("P8_Y5_R10_628_ACQUISITION_STATUS.csv", acquisition_rows),
        ("P8_Y5_R10_628_NONCLAIM_NUMERIC_ANCHORS.csv", anchors),
        ("P8_Y5_R10_628_ARENA_SOURCE_STATUS.csv", arena_rows),
        ("P8_Y5_BRR545_628_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_628_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_628_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_628_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        local_sources,
        external_sources,
        zcg_audit,
        acquisition_rows,
        anchors,
        arena_rows,
        decision_rows,
        route_rows,
        nonclaim_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
