from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1355"
TITLE = "1355-Y5-R10-RAB-Y5-source-functional-pullback-or-JZ-source-normalization-basis"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PULLBACK_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_Y5_PULLBACK_THEOREM_ATTEMPT.csv"
JZ_BASIS_PATH = OUT_DIR / f"{PACK_ID}_Y5_JZ_BASIS.csv"
OBSTRUCTION_LINK_PATH = OUT_DIR / f"{PACK_ID}_Y5_OBSTRUCTION_LINKS.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1355_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1355_0_1354_doc",
            "source_path": "1354-Y5-R10-RAB-source-functional-evenness-theorem-or-Y5Y6-JZ-coefficient-fill.md",
            "required_anchor": "Current verdict",
            "purpose": "1354 blocks source-functional evenness and selects Y5.",
        },
        {
            "source_id": "SRC1355_1_1354_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1354_NEXT_TARGET.csv",
            "required_anchor": "NEXT1354_0_1355",
            "purpose": "handoff to Y5 source-functional pullback.",
        },
        {
            "source_id": "SRC1355_2_1354_y5_coeffs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1354_Y5Y6_JZ_COEFFICIENT_FILL.csv",
            "required_anchor": "JZ1354_Y5_0_radial_Meff_hair",
            "purpose": "Y5 source-normalization JZ coefficient rows.",
        },
        {
            "source_id": "SRC1355_3_1012_y5_doc",
            "source_path": "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            "required_anchor": "Y5O1012_8_verdict",
            "purpose": "prior Y5 owner theorem attempt and eight-channel vector.",
        },
        {
            "source_id": "SRC1355_4_1013_flux_doc",
            "source_path": "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            "required_anchor": "PFC1013_8_verdict",
            "purpose": "measured-GM flux closure theorem attempt.",
        },
        {
            "source_id": "SRC1355_5_1013_vector",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
            "required_anchor": "OBS1013_0_projected_extra_current",
            "purpose": "exact measured-GM obstruction vector.",
        },
        {
            "source_id": "SRC1355_6_1014_coeffs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv",
            "required_anchor": "PCC1014_1_I_commutator",
            "purpose": "Pi_M commutator/projector coefficient debts.",
        },
        {
            "source_id": "SRC1355_7_1029_cg_doc",
            "source_path": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
            "required_anchor": "CE1029_1_einstein_jordan_relabel",
            "purpose": "frame relabel warning: couplings can move into source-normalization.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def pullback_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "YPB1355_0_same_frame",
            "claim_piece": "same observed coframe for matter, clocks, source current, and orbit",
            "required_form": "S_matter[psi,e_obs] defines J_H[e_obs] and the same e_obs defines rods, clocks, orbital readout, and source measure",
            "current_evidence": "Y5O1012_0 conditional_not_parent_derived; frame/c_g warnings remain active",
            "status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "if_missing": "source pullback can hide a frame coupling as measured-GM drift",
        },
        {
            "clause_id": "YPB1355_1_quotient_pullback",
            "claim_piece": "measured source functional factors through quotient-visible data and is even in Z",
            "required_form": "mu_obs = mu_bar[q(Phi),theta_source] with D_Z q=0 or Z exchange-even before readout",
            "current_evidence": "1354 source pullback failed current evidence; no parent source functional supplied",
            "status": "NOT_SUPPLIED",
            "if_missing": "J_Z[Y5] remains a live coupling",
        },
        {
            "clause_id": "YPB1355_2_PiM_parent_origin",
            "claim_piece": "Pi_M is parent-owned before readout",
            "required_form": "Pi_M maps J_H to an absolute/topological mass-flux class without post-fit masking",
            "current_evidence": "Y5O1012_2 not_parent_derived; PFC1013_1 candidate_origin_not_completed",
            "status": "NOT_PARENT_DERIVED",
            "if_missing": "projector can introduce source-normalization hair",
        },
        {
            "clause_id": "YPB1355_3_flux_closure",
            "claim_piece": "compact-exterior projected Hilbert flux closes",
            "required_form": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H=0 or exact obstruction vector is scored",
            "current_evidence": "PFC1013_8 fail_current_claim; OBS1013 rows retained_unfilled",
            "status": "EXACT_OBSTRUCTION_NOT_ZERO",
            "if_missing": "radial/time/source residuals survive",
        },
        {
            "clause_id": "YPB1355_4_worldtube_glue",
            "claim_piece": "worldtube source measure equals exterior parent charge before orbital fitting",
            "required_form": "M_source[W]=int_S Q_M[tau]=M_eff with fixed calibration",
            "current_evidence": "Y5O1012_4 not_derived_core_missing_piece; PFC1013_6 not_yet_derived_core_missing_piece",
            "status": "NOT_DERIVED_CORE_MISSING_PIECE",
            "if_missing": "closed wrong charge can mimic Newton recovery",
        },
        {
            "clause_id": "YPB1355_5_no_extra_mu_channels",
            "claim_piece": "no extra source-normalization channels remain",
            "required_form": "mu_extra boundary/bulk/domain/projector/memory/nonEH/species/time/calibration terms are theorem-zero or bounded",
            "current_evidence": "Y5O1012_5 retained_debt; 1354 installs eight JZ rows",
            "status": "RETAINED_DEBT",
            "if_missing": "Y5 source functional is not even/quotient-only",
        },
        {
            "clause_id": "YPB1355_6_no_absorption",
            "claim_piece": "J_Z is not absorbed into fitted G or source calibration",
            "required_form": "range/time/species/radial/frame derivatives are zero or carried as explicit residual rows",
            "current_evidence": "Y5O1012_6 rule_written_not_satisfied; 1029 warns frame relabel moves coupling into source-normalization",
            "status": "RULE_WRITTEN_NOT_SATISFIED",
            "if_missing": "a coupling can disappear by notation and reappear as measured-GM",
        },
        {
            "clause_id": "YPB1355_7_Newton_Poisson_orbit",
            "claim_piece": "same charge sources Poisson/Gauss and orbital acceleration",
            "required_form": "nabla^2 Phi=4pi G_ref rho_H and a_r=-G_ref M_ref/r^2 from the same parent charge",
            "current_evidence": "Y5O1012_7 conditional_not_parent_derived; PFC1013_7 not_parent_derived",
            "status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "if_missing": "Newton recovery cannot be claimed even if a charge is conserved",
        },
        {
            "clause_id": "YPB1355_8_verdict",
            "claim_piece": "Y5 source-functional pullback theorem",
            "required_form": "YPB1355_0 through YPB1355_7 all pass with source paths",
            "current_evidence": "same-frame, quotient pullback, Pi_M origin, flux closure, worldtube glue, extra channels, calibration, and Newton readout are not closed",
            "status": "PULLBACK_THEOREM_NOT_PROVED",
            "if_missing": "retain Y5 J_Z basis as nonclaim",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def jz_basis() -> list[dict[str, object]]:
    rows = [
        {
            "basis_id": "Y5JZ1355_0_radial_Meff_hair",
            "basis_symbol": "j_Z_radial_Meff",
            "basis_formula": "M_eff^-1 int_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]_radial",
            "dominant_obstruction": "OBS1013_6_flux_leak;PCC1014_5_epsilon_radial_Meff",
            "observable_link": "partial_r ln(mu_obs); beta_minus_1; alpha(lambda); R11",
            "units_required": "dimensionless radial envelope or profile units",
            "current_status": "MISSING_RADIAL_PROFILE_OR_THEOREM",
        },
        {
            "basis_id": "Y5JZ1355_1_boundary_monopole",
            "basis_symbol": "j_Z_boundary",
            "basis_formula": "M_eff^-1 int_boundary B_zero_flux or boundary/source-reference shift",
            "dominant_obstruction": "OBS1013_4_boundary_zero_flux;PCC1014_2_B_zero_flux",
            "observable_link": "beta_minus_1; alpha3; xi; Gdot_over_G; R11",
            "units_required": "dimensionless GM-flux or boundary coefficient",
            "current_status": "MISSING_BOUNDARY_ZERO_OR_VALUE",
        },
        {
            "basis_id": "Y5JZ1355_2_domain_projector_mass",
            "basis_symbol": "j_Z_domain_projector",
            "basis_formula": "M_eff^-1 int_A [d,Pi_M]J_H + delta_g Pi_M stress source projected onto domain selector",
            "dominant_obstruction": "OBS1013_1_PiM_commutator;OBS1013_5_projector_stress;PCC1014_1_I_commutator",
            "observable_link": "alpha1; alpha2; alpha3; xi; R11",
            "units_required": "dimensionless projector/source units",
            "current_status": "MISSING_PROJECTOR_COMMUTATOR_OR_STRESS_MAP",
        },
        {
            "basis_id": "Y5JZ1355_3_bulk_X_Yukawa",
            "basis_symbol": "j_Z_bulk_X",
            "basis_formula": "finite-range X/source tail contribution to mu_extra(lambda)",
            "dominant_obstruction": "OBS1013_0_projected_extra_current plus R10 alpha(lambda) source map",
            "observable_link": "alpha(lambda); R10; R11",
            "units_required": "dimensionless plus length scale",
            "current_status": "MISSING_BULK_GAP_OR_ALPHA_CURVE",
        },
        {
            "basis_id": "Y5JZ1355_4_nonEH_operator",
            "basis_symbol": "j_Z_nonEH_source",
            "basis_formula": "non-EH/source operator vector projected into measured-GM and PPN response",
            "dominant_obstruction": "OBS1013_0_projected_extra_current;OBS1013_7_calibration_PPN_tail",
            "observable_link": "gamma_minus_1; beta_minus_1; alpha(lambda); R11",
            "units_required": "operator-family or dimensionless units",
            "current_status": "MISSING_NONEH_OPERATOR_COEFFICIENT_MAP",
        },
        {
            "basis_id": "Y5JZ1355_5_species_source",
            "basis_symbol": "j_Z_species_A",
            "basis_formula": "species/material source charge vector after source-worldtube/readout projection",
            "dominant_obstruction": "OBS1013_0_projected_extra_current; 1029 frame/source relabel warning",
            "observable_link": "eta_WEP_source_charge; clock source residual; R11",
            "units_required": "dimensionless by species/material pair",
            "current_status": "MISSING_SPECIES_CHARGE_VECTOR",
        },
        {
            "basis_id": "Y5JZ1355_6_time_drift",
            "basis_symbol": "j_Z_time_drift",
            "basis_formula": "d ln M_eff/dt or d ln mu_obs/dt from finite-annulus flux leakage",
            "dominant_obstruction": "OBS1013_6_flux_leak; constant-GM residual rows",
            "observable_link": "Gdot_over_G; R11",
            "units_required": "yr^-1 or dimensionless per-time convention",
            "current_status": "MISSING_TIME_DRIFT_PROFILE_OR_STATIONARITY",
        },
        {
            "basis_id": "Y5JZ1355_7_calibration_offset",
            "basis_symbol": "j_Z_calibration",
            "basis_formula": "Delta_cal + Delta_PPN from closed-charge-to-orbit calibration mismatch",
            "dominant_obstruction": "OBS1013_7_calibration_PPN_tail; Y5O1012_6 no-absorption rule",
            "observable_link": "beta_minus_1; Gdot_over_G; R11",
            "units_required": "dimensionless calibration/residual vector",
            "current_status": "MISSING_CALIBRATION_THEOREM_OR_OFFSET",
        },
    ]
    for row in rows:
        row["value_or_theorem"] = "MISSING"
        row["accepted_for_scoring"] = False
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def obstruction_links() -> list[dict[str, object]]:
    return [
        {
            "link_id": "LINK1355_0_exact_obstruction",
            "source_object": "d(Pi_M J_H)",
            "exact_form": "Pi_M dJ_H + [d,Pi_M]J_H; with extra channels: -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "basis_rows": "Y5JZ1355_0;Y5JZ1355_2;Y5JZ1355_6",
            "status": "RETAINED_UNFILLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "link_id": "LINK1355_1_worldtube_glue",
            "source_object": "M_source[W]=int_S Q_M[tau]=M_eff",
            "exact_form": "worldtube/exterior equality before orbital fitting",
            "basis_rows": "all Y5JZ1355 rows",
            "status": "NOT_DERIVED_CORE_MISSING_PIECE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "link_id": "LINK1355_2_no_absorption",
            "source_object": "G/calibration/readout separation",
            "exact_form": "constant calibration may be absorbed; Z-dependent radial/time/species/frame terms may not",
            "basis_rows": "Y5JZ1355_5;Y5JZ1355_6;Y5JZ1355_7",
            "status": "RULE_WRITTEN_NOT_SATISFIED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1355_0_Y5_pullback",
            "claim": "Y5 measured-GM/source-normalization is a quotient pullback even in Z",
            "current_status": "BLOCKED",
            "reason": "same-frame, Pi_M origin, flux closure, worldtube glue, and no-extra-channel clauses fail",
        },
        {
            "gate_id": "GATE1355_1_Y5_JZ_zero",
            "claim": "all Y5 J_Z source-normalization coefficients vanish",
            "current_status": "BLOCKED",
            "reason": "eight J_Z basis rows are missing values or theorem-zero certificates",
        },
        {
            "gate_id": "GATE1355_2_Newton_GR_recovery",
            "claim": "Newton/GR source normalization is derived",
            "current_status": "BLOCKED",
            "reason": "measured-GM pullback and obstruction score are not claim-ready",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1355_0_pullback_not_closed",
            "decision": "Y5 source-functional pullback is not closed.",
            "why": "quotient pullback alone is missing; the exact Pi_M/J_H obstruction and worldtube glue are still open",
            "next_action": "attack Pi_M/J_H/worldtube equality or score the obstruction basis",
        },
        {
            "decision_id": "DEC1355_1_basis_installed",
            "decision": "The Y5 J_Z basis is installed row-by-row.",
            "why": "this prevents measured-GM/source-normalization from being hidden inside a fitted G",
            "next_action": "derive or source each basis coefficient before any Newton/local-GR claim",
        },
        {
            "decision_id": "DEC1355_2_best_next_target",
            "decision": "Best next target is the worldtube/Hilbert equality route.",
            "why": "without M_source[W]=int_S Q_M=M_eff, a conserved charge can still be the wrong Newtonian source",
            "next_action": "try worldtube-Hilbert source equality or retain R_eq/I_commutator rows",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1355_0_1356",
            "target_file": "1356-Y5-R10-RAB-worldtube-Hilbert-source-equality-or-R_eq-Icommutator-fill.md",
            "target_script": "scripts/Y5_R10_RAB_worldtube_Hilbert_source_equality_or_Req_Icommutator_fill.py",
            "task": "try to prove worldtube source measure equals the exterior Hilbert/topological mass charge before orbital fitting; if not, retain R_eq, I_commutator, and calibration rows as nonclaim",
            "success_condition": "worldtube-Hilbert equality theorem, or explicit nonclaim R_eq/I_commutator/calibration source rows with units",
            "do_not": "do not absorb residuals into fitted G; do not use closed wrong charge as Newton recovery; do not edit formalization-workbench or use GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate_outputs(
    sources: list[dict[str, object]],
    pullback: list[dict[str, object]],
    basis: list[dict[str, object]],
    links: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1355_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in pullback if row["clause_id"] == "YPB1355_8_verdict")
    add(
        "VAL1355_1_pullback_not_proved",
        "Y5 pullback theorem is not promoted",
        verdict["status"] == "PULLBACK_THEOREM_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["if_missing"]),
    )

    add(
        "VAL1355_2_basis_has_eight_rows",
        "Y5 JZ basis has eight source-normalization rows",
        len(basis) == 8,
        f"rows={len(basis)}",
    )

    add(
        "VAL1355_3_basis_nonclaim",
        "basis rows remain missing/unscored/nonclaim",
        all(row["value_or_theorem"] == "MISSING" and not row["accepted_for_scoring"] and not row["claim_allowed"] for row in basis),
        "all basis rows reject scoring",
    )

    add(
        "VAL1355_4_obstruction_links_present",
        "obstruction links connect basis to PiM/worldtube/no-absorption debts",
        len(links) == 3 and all(not row["claim_allowed"] for row in links),
        f"links={len(links)}",
    )

    add(
        "VAL1355_5_claim_gates_blocked",
        "all claim gates remain blocked",
        all(row["current_status"] == "BLOCKED" and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['current_status']}" for row in gates),
    )

    all_rows = sources + pullback + basis + links + gates + decisions + next_target
    add(
        "VAL1355_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1355*", "*1355-Y5-R10-RAB-Y5-source*", "*Y5_R10_RAB_Y5_source*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1355_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1355_8_next_target_1356",
        "next target routes to worldtube-Hilbert equality",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1356-Y5-R10-RAB-worldtube-Hilbert"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1355_9_overall",
        "overall 1355 validation",
        all(row["status"] == "PASS" for row in validations),
        "1355 blocks Y5 pullback claim and installs source-normalization JZ basis",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    pullback: list[dict[str, object]],
    basis: list[dict[str, object]],
    links: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1355 does not derive Y5 measured-GM/source-normalization as a quotient pullback. The source functional still has open `J_Z` channels unless same-frame Hilbert current, parent `Pi_M`, flux closure, worldtube glue, and no-absorption calibration all close.",
            "**Main progress:** the Y5 obstruction is now in a usable basis. The eight source-normalization channels are tied to exact obstruction objects (`-Pi_M dJ_extra`, `[d,Pi_M]J_H`, `A_parent`, `R_eq`, `B_zero_flux`, calibration tails) rather than vague fitted-G language.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Y5 pullback theorem attempt",
            table(["clause_id", "claim_piece", "required_form", "status", "if_missing"], pullback),
            "## Y5 JZ basis",
            table(["basis_id", "basis_symbol", "basis_formula", "dominant_obstruction", "observable_link", "current_status", "accepted_for_scoring"], basis),
            "## Obstruction links",
            table(["link_id", "source_object", "exact_form", "basis_rows", "status"], links),
            "## Claim gates",
            table(["gate_id", "claim", "current_status", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    pullback = pullback_attempt()
    basis = jz_basis()
    links = obstruction_links()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, pullback, basis, links, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PULLBACK_ATTEMPT_PATH, pullback)
    write_csv(JZ_BASIS_PATH, basis)
    write_csv(OBSTRUCTION_LINK_PATH, links)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, pullback, basis, links, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
