from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "961-Y5-R10-priority-operator-parent-zero-clauses-or-bound-source-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    literal = str(FORMALIZATION).replace("'", "''")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + literal
        + "' -Recurse -File | Where-Object { $_.LastWriteTime -gt $since } | Measure-Object).Count; "
        + "Write-Output $count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    try:
        return int(completed.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return -2


def source_register() -> list[dict[str, str]]:
    local_specs = [
        {
            "source_id": "960_doc",
            "source_type": "local",
            "path_or_url": "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
            "role": "handoff: R2/fR filter and torsion Levi-Civita gate",
            "needle": "R2/fR: filter works",
        },
        {
            "source_id": "960_validation",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_BRR545_960_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V960_11_validation_rows_ready",
        },
        {
            "source_id": "960_bound_pack",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_R10_960_PRIORITY_BOUND_PACK.csv",
            "role": "R2/fR and torsion bound-pack scaffold",
            "needle": "BPACK960_0",
        },
        {
            "source_id": "960_P4_review",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_R10_960_P4_CONNECTION_SUBROW_REVIEW.csv",
            "role": "P4 connection subrow placeholder review",
            "needle": "P4REV960_5",
        },
        {
            "source_id": "959_fill_template",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_R10_959_R11_PRIORITY_FILL_TEMPLATE.csv",
            "role": "priority R11 fill template",
            "needle": "R11FILL959_0",
        },
        {
            "source_id": "443_connection",
            "source_type": "local",
            "path_or_url": "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
            "role": "Levi-Civita compatibility theorem/vector fork",
            "needle": "Levi-Civita compatibility remains conditional",
        },
        {
            "source_id": "785_connection_stack",
            "source_type": "local",
            "path_or_url": "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
            "role": "coframe/connection stack blocker",
            "needle": "torsion/nonmetricity gate blocks claim",
        },
        {
            "source_id": "R11_P4_template",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/R11_P4_connection_rows_TEMPLATE.csv",
            "role": "six P4 connection rows needing real fills",
            "needle": "torsion_nonmetricity_combined",
        },
        {
            "source_id": "R11_executable",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "role": "non-EH executable vector with R2/fR and torsion rows",
            "needle": "R2_fR_scalar_mode",
        },
        {
            "source_id": "700_EH_algebra",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_R10_700_EH_POISSON_ALGEBRA_CERTIFICATE.csv",
            "role": "conditional EH-to-Poisson algebra certificate",
            "needle": "ALG700_4_poisson_coefficient",
        },
    ]
    web_specs = [
        {
            "source_id": "ext_Lee2020_R10",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/2002.11761",
            "role": "modern Eot-Wash short-range R10 alpha(lambda) source candidate",
            "needle": "New Test of the Gravitational 1/r^2 Law at Separations down to 52",
        },
        {
            "source_id": "ext_Kapner2007_R10",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/hep-ph/0611184",
            "role": "older Eot-Wash R10 anchor and continuity source",
            "needle": "lambda = 56 micrometers",
        },
        {
            "source_id": "ext_Adelberger2003_review",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/hep-ph/0307284",
            "role": "inverse-square-law review/source hierarchy continuity",
            "needle": "Tests of the Gravitational Inverse-Square Law",
        },
        {
            "source_id": "ext_Will2014_PPN",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/1403.7377",
            "role": "PPN and solar-system bound source candidate",
            "needle": "The Confrontation between General Relativity and Experiment",
        },
        {
            "source_id": "ext_Cassini2003_gamma",
            "source_type": "web",
            "path_or_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "role": "Cassini gamma source candidate for scalar-mode PPN projection",
            "needle": "gamma = 1 + (2.1 +/- 2.3) x 10(-5)",
        },
        {
            "source_id": "ext_Terrano2015_spin",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/1508.02463",
            "role": "spin-dependent/torsion-style bound source candidate",
            "needle": "Short-range spin-dependent interactions of electrons",
        },
        {
            "source_id": "ext_Safronova2017_clocks",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/1710.01833",
            "role": "clock/atomic new-physics source candidate",
            "needle": "Search for New Physics with Atoms and Molecules",
        },
        {
            "source_id": "ext_Uzan2011_constants",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/1009.5514",
            "role": "clock/constant-variation and WEP linkage review source candidate",
            "needle": "Varying Constants, Gravitation and Cosmology",
        },
    ]
    rows = []
    for spec in local_specs:
        path = source_path(spec["path_or_url"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists_or_recorded": flag(exists),
                "needle_or_url_recorded": flag(needle_found),
                "extraction_status": "local_needle_checked",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for spec in web_specs:
        recorded = spec["path_or_url"].startswith("https://") and len(spec["path_or_url"]) > len("https://")
        rows.append(
            {
                **spec,
                "absolute_path": "",
                "exists_or_recorded": flag(recorded),
                "needle_or_url_recorded": flag(recorded),
                "extraction_status": "web_source_string_recorded_manual_browse_required_for_numeric_use",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_zero_clauses() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PZ961_R2FR_0_operator_exclusion",
            "operator_family": "R2_fR_scalar_mode",
            "zero_condition": "The parent local weak-field quotient action contains only EH+Lambda plus boundary/topological terms at second metric-derivative order.",
            "formal_contract": "S_loc[g_obs]=int sqrt(-g_obs)[a + b R(g_obs) - 2 Lambda] + S_boundary/topological; no R^2, R_{mu nu}R^{mu nu}, C^2, R Box R, or generic f(R) Taylor coefficient beyond linear R survives.",
            "would_imply": "c_R2=c_fR=0 in the executable R11 scalar-mode row.",
            "status": "conditional_unsigned",
            "unsigned_input": "parent operator-selection theorem/no-extra-field clause not yet signed",
            "next_action": "attempt parent proof that quotient locality + second-order metric-only dynamics excludes the scalar curvature tower",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PZ961_R2FR_1_trace_scalar_absence",
            "operator_family": "R2_fR_scalar_mode",
            "zero_condition": "The linearized trace equation carries no finite-mass scalar pole.",
            "formal_contract": "f''(R0)=0, or the R^2 coefficient is field-redefinition redundant/topological, so (Box-m_s^2)delta R is absent or m_s -> infinity.",
            "would_imply": "no Yukawa alpha(lambda) branch from the R2/fR sector.",
            "status": "blocked_missing_parent_certificate",
            "unsigned_input": "no sourced coefficient normalization and no topological/redundancy certificate",
            "next_action": "if proof fails, source alpha(lambda)/gamma/beta map and keep finite scalar as R11 residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PZ961_LC_0_no_independent_connection",
            "operator_family": "torsion_nonmetricity",
            "zero_condition": "The parent configuration has no independent connection variable in the observed quotient.",
            "formal_contract": "Gamma^alpha_{mu nu} is not varied independently; it is defined as Gamma_LC[g_obs] or omega[e_obs] everywhere matter, light, spin, clocks, and sources are evaluated.",
            "would_imply": "T^alpha_{mu nu}=0 and Q_{lambda mu nu}=0 kinematically.",
            "status": "conditional_unsigned",
            "unsigned_input": "observed metric/coframe connection-only parent clause not derived for every sector",
            "next_action": "prove all sector actions descend through observed coframe/metric connection only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PZ961_LC_1_Palatini_no_hypermomentum",
            "operator_family": "torsion_nonmetricity",
            "zero_condition": "If an independent Gamma exists, its field equation is pure Palatini-EH with zero hypermomentum and projective silence.",
            "formal_contract": "delta_Gamma S_EH=0 and Delta_matter^lambda_{mu nu}=0 imply Gamma=Gamma_LC[g_obs] up to an unobservable projective gauge.",
            "would_imply": "connection residual rows collapse to derived zero after EH and matter-coupling gates close.",
            "status": "conditional_unsigned",
            "unsigned_input": "EH-only LHS and universal no-Gamma matter/source/readout coupling remain open",
            "next_action": "derive no-hypermomentum from source-functor/matter-descent clause or retain P4 residuals",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PZ961_LC_2_no_representative_connection_leak",
            "operator_family": "torsion_nonmetricity",
            "zero_condition": "No representative Weyl, disformal, torsion, spin, source-charge, clock, lightcone, or boundary coupling survives quotient projection.",
            "formal_contract": "Every local observable depends on q(Phi) through g_obs/e_obs only; vertical connection deformations lie in ker(DObs) and in the presymplectic null directions.",
            "would_imply": "all six P4 connection subrows get theorem-zero rather than numeric bound fills.",
            "status": "blocked_missing_projection_proof",
            "unsigned_input": "boundary/local projection silence and spin/source connection independence not proved",
            "next_action": "map each P4 subrow either to zero certificate or to bound acquisition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PZ961_VERDICT",
            "operator_family": "priority_operator_stack",
            "zero_condition": "R2/fR and torsion/nonmetricity are both parent-zeroed.",
            "formal_contract": "PZ961_R2FR_0 or PZ961_R2FR_1 closes, and PZ961_LC_0 or PZ961_LC_1+PZ961_LC_2 closes.",
            "would_imply": "R11 priority operator gate could move back to EH/Newton local-GR reduction.",
            "status": "not_closed_current_corpus",
            "unsigned_input": "both priority families still require parent signatures or real bound rows",
            "next_action": "split next target: attack R2/fR zero proof first because it is sharper and less sprawling than full connection geometry",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def zero_clause_dryrun(clauses: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for clause in clauses:
        status = clause["status"]
        closed = status in {"derived_zero", "parent_signed"}
        rows.append(
            {
                "dryrun_id": clause["clause_id"].replace("PZ961", "DRY961"),
                "operator_family": clause["operator_family"],
                "test": clause["zero_condition"],
                "result": "pass" if closed else "blocked",
                "blocking_input": clause["unsigned_input"],
                "claim_allowed": flag(closed),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def bound_source_acquisition_ledger() -> list[dict[str, str]]:
    return [
        {
            "acquisition_id": "BS961_R2FR_0_full_curve_Lee2020",
            "operator_family": "R2_fR_scalar_mode",
            "quantity": "alpha_bound(lambda)",
            "arena": "R10_short_range_Yukawa",
            "source_target": "Lee et al. 2020 Eot-Wash PRL/arXiv full exclusion curve",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "extraction_method": "digitize figure/table before any claim",
            "required_parent_inputs": "c_R2_or_c_fR; coefficient units; scalar mass m_s; scalar coupling alpha_scalar; alpha(lambda) normalization",
            "candidate_value": "MISSING_DIGITIZED_CURVE",
            "candidate_units": "lambda: micrometer_or_meter; alpha: dimensionless",
            "provenance_status": "source_identified_not_digitized",
            "valid_for_claim": "false",
            "reason_blocked": "full curve not extracted and MTS scalar coefficient/mass map absent",
            "next_action": "digitize/source machine-readable curve only after parent scalar map exists",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BS961_R2FR_1_anchor_Lee2020",
            "operator_family": "R2_fR_scalar_mode",
            "quantity": "gravitational_strength_range_anchor",
            "arena": "R10_short_range_Yukawa",
            "source_target": "Lee et al. 2020 anchor: gravitational-strength Yukawa range below 38.6 micrometer",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "extraction_method": "anchor_only_non_curve",
            "required_parent_inputs": "same as BS961_R2FR_0",
            "candidate_value": "lambda_anchor=38.6",
            "candidate_units": "micrometer",
            "provenance_status": "source_backed_anchor_not_claim_curve",
            "valid_for_claim": "false",
            "reason_blocked": "anchor alone cannot substitute for alpha(lambda) curve and parent map is absent",
            "next_action": "use only as sanity-check row, not scoreable evidence",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BS961_R2FR_2_anchor_Kapner2007",
            "operator_family": "R2_fR_scalar_mode",
            "quantity": "older_alpha_lambda_anchor",
            "arena": "R10_short_range_Yukawa",
            "source_target": "Kapner et al. 2006/2007 Eot-Wash continuity anchor",
            "source_url": "https://arxiv.org/abs/hep-ph/0611184",
            "extraction_method": "anchor_only_non_curve",
            "required_parent_inputs": "same as BS961_R2FR_0",
            "candidate_value": "abs(alpha)<=1 at lambda=56",
            "candidate_units": "alpha dimensionless; lambda micrometer",
            "provenance_status": "source_backed_anchor_not_claim_curve",
            "valid_for_claim": "false",
            "reason_blocked": "older anchor useful for regression tests only, not a modern full curve",
            "next_action": "retain for continuity and code-smoke comparisons",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BS961_R2FR_3_review_Adelberger2003",
            "operator_family": "R2_fR_scalar_mode",
            "quantity": "source_hierarchy_review",
            "arena": "R10_short_range_Yukawa",
            "source_target": "Adelberger-Heckel-Nelson 2003 inverse-square-law review",
            "source_url": "https://arxiv.org/abs/hep-ph/0307284",
            "extraction_method": "review_continuity_not_numeric_bound",
            "required_parent_inputs": "none for bibliography; all numeric model inputs still missing",
            "candidate_value": "REVIEW_ONLY",
            "candidate_units": "not_numeric",
            "provenance_status": "source_hierarchy_recorded",
            "valid_for_claim": "false",
            "reason_blocked": "review source is not itself an executable modern bound curve",
            "next_action": "use to justify source hierarchy, not to claim MTS passes",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BS961_R2FR_4_PPN_gamma_Cassini",
            "operator_family": "R2_fR_scalar_mode",
            "quantity": "gamma_minus_1",
            "arena": "PPN_solar_system",
            "source_target": "Cassini gamma measurement",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "extraction_method": "numeric_bound_after_formula_map",
            "required_parent_inputs": "scalar coupling to gamma; screening/range regime; solar-system normalization",
            "candidate_value": "gamma-1=(2.1 +/- 2.3)e-5",
            "candidate_units": "dimensionless",
            "provenance_status": "source_identified_anchor_not_mapped",
            "valid_for_claim": "false",
            "reason_blocked": "no R2/fR scalar-mode PPN projection from parent coefficients",
            "next_action": "only use after deriving gamma(alpha_scalar,m_s,screening)",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BS961_R2FR_5_PPN_review_Will",
            "operator_family": "R2_fR_scalar_mode",
            "quantity": "PPN_formalism_and_bound_context",
            "arena": "PPN_solar_system_orbital",
            "source_target": "Will 2014 GR-experiment review",
            "source_url": "https://arxiv.org/abs/1403.7377",
            "extraction_method": "review_context_then_specific_bound_rows",
            "required_parent_inputs": "gamma/beta/orbital-residual maps",
            "candidate_value": "REVIEW_ONLY",
            "candidate_units": "not_numeric",
            "provenance_status": "source_hierarchy_recorded",
            "valid_for_claim": "false",
            "reason_blocked": "review does not replace an executable MTS-to-PPN map",
            "next_action": "use for PPN row definitions and source targets",
            "generated_utc": stamp(),
        },
    ]


def p4_connection_bound_acquisition() -> list[dict[str, str]]:
    base = [
        (
            "P4B961_0",
            "torsion_nonmetricity_combined",
            "c_T_or_c_Q",
            "eta_WEP;clock_residual;lightcone_residual;operator_ledger",
            "https://arxiv.org/abs/1403.7377",
            "split into torsion trace, axial torsion, Weyl nonmetricity, shear nonmetricity before scoring",
        ),
        (
            "P4B961_1",
            "axial_torsion_spin_coupling",
            "c_A_or_S_mu",
            "spin_torsion_residual;clock_residual;operator_ledger",
            "https://arxiv.org/abs/1508.02463",
            "map spin-dependent force conventions to torsion axial-vector normalization",
        ),
        (
            "P4B961_2",
            "torsion_trace_projective_mode",
            "c_Ttrace_or_T_mu",
            "eta_WEP;source_charge_residual;operator_ledger",
            "https://arxiv.org/abs/1403.7377",
            "prove projective invariance or source WEP/source-charge bound map",
        ),
        (
            "P4B961_3",
            "nonmetricity_weyl_trace",
            "c_Qtrace_or_Q_mu",
            "clock_residual;rod_residual;eta_WEP;operator_ledger",
            "https://arxiv.org/abs/1009.5514",
            "map Weyl nonmetricity to clock/rod/fundamental-constant drift channel",
        ),
        (
            "P4B961_4",
            "nonmetricity_shear_lightcone",
            "c_Qshear_or_Q_tilde",
            "lightcone_residual;clock_residual;eta_WEP;operator_ledger",
            "https://arxiv.org/abs/1710.01833",
            "map shear nonmetricity to lightcone/clock observable without assuming metric light rays",
        ),
        (
            "P4B961_5",
            "independent_connection_hypermomentum",
            "c_Delta_or_Delta_lambda_munu",
            "eta_WEP;source_charge_residual;clock_residual;operator_ledger",
            "https://arxiv.org/abs/1403.7377",
            "derive no-Gamma matter theorem or source hypermomentum-sensitive test matter bounds",
        ),
    ]
    rows = []
    for row_id, family, coefficient, observables, source_url, next_action in base:
        rows.append(
            {
                "bound_id": row_id,
                "operator_family": family,
                "coefficient_symbol": coefficient,
                "needed_inputs": "coefficient_value; coefficient_units; normalization; weak_field_map; predicted_residual_or_bound_source; formula_reference; source_file; assumptions",
                "arena": "P4_connection_R11_local_arena",
                "induced_observable": observables,
                "candidate_source_url": source_url,
                "candidate_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT",
                "candidate_units": "MISSING_COEFFICIENT_OR_CONNECTION_UNITS",
                "weak_field_map": "MISSING_P4_CONNECTION_TO_OBSERVABLE_MAP",
                "ready_for_scoring": "false",
                "valid_for_claim": "false",
                "verdict": "SOURCE_ACQUISITION_ROW_ONLY",
                "next_action": next_action,
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC961_0_R2_fR_route",
            "topic": "R2/fR scalar-mode priority",
            "result": "derive_first_then_bound",
            "reason": "the zero clause is sharp: local second-order metric-only EH dynamics would kill c_R2/c_fR cleanly if parent-signed",
            "next_action": "make 962 attempt a proof of c_R2=c_fR=0 before spending tokens on full curve digitization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC961_1_connection_route",
            "topic": "torsion/nonmetricity priority",
            "result": "retain_as_parallel_bound_stack",
            "reason": "connection zero proof requires more sector-by-sector descent clauses and is more sprawling than R2/fR",
            "next_action": "keep P4 rows ready but do not claim local-GR compatibility from them",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC961_2_project_status",
            "topic": "local-GR reduction",
            "result": "closer_but_still_not_claimable",
            "reason": "source-side Newton/GR RHS is much cleaner than before, but LHS operator selection still has two priority leaks",
            "next_action": "close or explicitly bound R2/fR first; then return to connection/no-hypermomentum",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE961_0_EH_operator_selection",
            "claim": "local LHS reduces to EH plus Lambda",
            "required_condition": "all non-EH local operators are parent-zero, topological/redundant, or executable bounded residuals",
            "current_evidence": "R2/fR and torsion/nonmetricity priority rows remain unsigned/non-executable",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE961_1_R2_fR_zero",
            "claim": "R2/fR scalar mode is absent",
            "required_condition": "c_R2=c_fR=0 or scalar pole absent by parent theorem",
            "current_evidence": "zero clause written but not parent-signed",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE961_2_P4_connection_zero",
            "claim": "observed connection is Levi-Civita for all local sectors",
            "required_condition": "no independent Gamma, or Palatini EH plus zero hypermomentum/projective silence",
            "current_evidence": "conditional clauses only; six P4 rows still bound-acquisition rows",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE961_3_R10_PPN_local_claim",
            "claim": "MTS passes R10/PPN/local-GR bound gates",
            "required_condition": "numeric parent coefficients, maps, sourced bounds, and residuals below limits",
            "current_evidence": "source URLs/anchors recorded, but no parent coefficients or executable maps",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "962-Y5-R10-R2-fR-zero-clause-proof-or-scalar-mode-bound-source-acquisition.md",
            "objective": "try to prove c_R2=c_fR=0 from the parent local second-order metric-only/no-extra-field clause; if not, acquire scalar-mode alpha(lambda)/PPN source inputs without claiming a pass",
            "include": "parent operator-selection proof; trace scalar-pole test; field-redefinition/topological escape audit; Lee2020/Kapner2007/Will/Cassini source rows",
            "exclude": "torsion full proof, EH claim, local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    clauses: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    p4_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    local_sources_ok = all(
        source["exists_or_recorded"] == "true" and source["needle_or_url_recorded"] == "true"
        for source in sources
        if source["source_type"] == "local"
    )
    web_sources_ok = all(
        source["exists_or_recorded"] == "true" and source["needle_or_url_recorded"] == "true"
        for source in sources
        if source["source_type"] == "web"
    )
    clauses_nonclaim = all(row["valid_for_claim"] == "false" and row["status"] != "parent_signed" for row in clauses)
    dryrun_blocks_claim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in dryrun_rows)
    bound_rows_nonclaim = all(row["valid_for_claim"] == "false" for row in bound_rows)
    p4_rows_nonclaim = all(row["valid_for_claim"] == "false" and row["ready_for_scoring"] == "false" for row in p4_rows)
    claim_gates_closed = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    no_formalization_edits = formalization_changed_after_start() == 0
    outputs_inside_root = all(
        str(path.resolve()).startswith(str(ROOT.resolve()))
        for path in [
            DOC,
            OUT / "P8_Y5_R10_961_SOURCE_REGISTER.csv",
            OUT / "P8_Y5_R10_961_PARENT_ZERO_CLAUSES.csv",
            OUT / "P8_Y5_R10_961_ZERO_CLAUSE_DRYRUN.csv",
            OUT / "P8_Y5_R10_961_BOUND_SOURCE_ACQUISITION_LEDGER.csv",
            OUT / "P8_Y5_R10_961_P4_CONNECTION_BOUND_ACQUISITION.csv",
            OUT / "P8_Y5_R10_961_DECISION_LEDGER.csv",
            OUT / "P8_Y5_R10_961_CLAIM_GATE.csv",
            OUT / "P8_Y5_R10_961_NEXT_TARGET.csv",
            OUT / "P8_Y5_BRR545_961_VALIDATION.csv",
        ]
    )
    checks = [
        ("V961_0_local_sources_checked", local_sources_ok, "all cited local handoff paths exist and needles were found"),
        ("V961_1_web_sources_recorded", web_sources_ok, "all cited web source strings are recorded for later manual/numeric extraction"),
        ("V961_2_parent_zero_clauses_nonclaim", clauses_nonclaim, "zero clauses remain unsigned/nonclaim"),
        ("V961_3_zero_dryrun_blocks_claim", dryrun_blocks_claim, "zero-clause dry run blocks every claim"),
        ("V961_4_R2FR_bound_rows_nonclaim", bound_rows_nonclaim, "scalar-mode source rows are source/acquisition rows only"),
        ("V961_5_P4_rows_nonclaim", p4_rows_nonclaim, "all P4 connection rows remain invalid for claim"),
        ("V961_6_claim_gates_false", claim_gates_closed, "EH/R2FR/P4/R10/PPN claims all blocked"),
        ("V961_7_decisions_ready", len(decision_rows) == 3, "decision ledger has three rows"),
        ("V961_8_next_target_ready", len(target_rows) == 1, "next target row written"),
        ("V961_9_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
        ("V961_10_outputs_inside_post_checkpoint", outputs_inside_root, "all output paths resolve inside post-checkpoint-work"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "V961_11_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "961 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    clauses: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    p4_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 961 Y5 R10: Priority Operator Parent Zero Clauses Or Bound Source Acquisition

Status: `Y5_R10_961_priority_operator_zero_clauses_written_sources_staged_nonclaim`

Claim ceiling: no EH, measured-GM, R10, PPN, orbital, clock, WEP, or local-GR pass is claimed here. This checkpoint is a ruthless gate: either parent-zero the priority leaks, or force them into explicit sourced residual rows.

## Ruthless Readout

The clean route is still derivation-first. `R2/fR` is the sharper target: if the parent action really gives local second-order metric-only dynamics, then `c_R2=c_fR=0` follows as an operator-selection clause rather than a fitted convenience. That proof is not yet signed, so the scalar-mode branch remains blocked.

The connection route is also mathematically respectable but heavier. It closes only if the parent has no independent observed connection, or if Palatini-EH plus zero hypermomentum and projective silence force `Gamma=Gamma_LC[g_obs]`. Current files make that route conditional, not derived.

So the project is not grim, but it is at a hard, honest hinge: RHS/source coupling has become much cleaner; LHS/local operator selection still needs either theorem-zero or real bound rows. No smuggling. No victory lap. But the target is now narrow enough to attack.

## Source Register

{md_table(sources, ["source_id", "source_type", "path_or_url", "role", "exists_or_recorded", "needle_or_url_recorded", "extraction_status"])}

## Parent Zero Clauses

{md_table(clauses, ["clause_id", "operator_family", "zero_condition", "status", "unsigned_input", "next_action"])}

## Zero-Clause Dry Run

{md_table(dryrun_rows, ["dryrun_id", "operator_family", "result", "blocking_input", "claim_allowed"])}

## Scalar-Mode Bound Source Acquisition

{md_table(bound_rows, ["acquisition_id", "operator_family", "quantity", "arena", "source_target", "candidate_value", "provenance_status", "valid_for_claim"])}

## P4 Connection Bound Acquisition

{md_table(p4_rows, ["bound_id", "operator_family", "coefficient_symbol", "induced_observable", "candidate_source_url", "ready_for_scoring", "verdict"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    clauses = parent_zero_clauses()
    dryrun_rows = zero_clause_dryrun(clauses)
    bound_rows = bound_source_acquisition_ledger()
    p4_rows = p4_connection_bound_acquisition()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        clauses,
        dryrun_rows,
        bound_rows,
        p4_rows,
        decision_rows,
        claim_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_961_SOURCE_REGISTER.csv",
        sources,
        [
            "source_id",
            "source_type",
            "path_or_url",
            "role",
            "needle",
            "absolute_path",
            "exists_or_recorded",
            "needle_or_url_recorded",
            "extraction_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_961_PARENT_ZERO_CLAUSES.csv",
        clauses,
        [
            "clause_id",
            "operator_family",
            "zero_condition",
            "formal_contract",
            "would_imply",
            "status",
            "unsigned_input",
            "next_action",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_961_ZERO_CLAUSE_DRYRUN.csv",
        dryrun_rows,
        ["dryrun_id", "operator_family", "test", "result", "blocking_input", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_961_BOUND_SOURCE_ACQUISITION_LEDGER.csv",
        bound_rows,
        [
            "acquisition_id",
            "operator_family",
            "quantity",
            "arena",
            "source_target",
            "source_url",
            "extraction_method",
            "required_parent_inputs",
            "candidate_value",
            "candidate_units",
            "provenance_status",
            "valid_for_claim",
            "reason_blocked",
            "next_action",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_961_P4_CONNECTION_BOUND_ACQUISITION.csv",
        p4_rows,
        [
            "bound_id",
            "operator_family",
            "coefficient_symbol",
            "needed_inputs",
            "arena",
            "induced_observable",
            "candidate_source_url",
            "candidate_value",
            "candidate_units",
            "weak_field_map",
            "ready_for_scoring",
            "valid_for_claim",
            "verdict",
            "next_action",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_961_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_961_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_961_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_961_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, clauses, dryrun_rows, bound_rows, p4_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
