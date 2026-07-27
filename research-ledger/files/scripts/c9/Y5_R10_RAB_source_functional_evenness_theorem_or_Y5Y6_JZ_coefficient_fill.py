from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1354"
TITLE = "1354-Y5-R10-RAB-source-functional-evenness-theorem-or-Y5Y6-JZ-coefficient-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
EVENNESS_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_FUNCTIONAL_EVENNESS_ATTEMPT.csv"
Y5Y6_COEFFICIENT_PATH = OUT_DIR / f"{PACK_ID}_Y5Y6_JZ_COEFFICIENT_FILL.csv"
RUNNER_REJECTION_PATH = OUT_DIR / f"{PACK_ID}_JZ_RUNNER_REJECTION.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1354_VALIDATION.csv"


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
            "source_id": "SRC1354_0_1353_doc",
            "source_path": "1353-Y5-R10-RAB-Z-component-lock-and-no-linear-source-theorem-or-JZ-source-pack.md",
            "required_anchor": "Current verdict",
            "purpose": "1353 identifies source/coupling evenness as the root obstruction.",
        },
        {
            "source_id": "SRC1354_1_1353_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1353_NEXT_TARGET.csv",
            "required_anchor": "NEXT1353_0_1354",
            "purpose": "handoff to source-functional evenness theorem or Y5/Y6 JZ fill.",
        },
        {
            "source_id": "SRC1354_2_1353_JZ",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1353_JZ_BZ_SOURCE_PACK.csv",
            "required_anchor": "JZ1353_2_Y5_source_normalization",
            "purpose": "JZ/BZ retained source pack including Y5/Y6.",
        },
        {
            "source_id": "SRC1354_3_response_contract",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "required_anchor": "RD516_4_zero_odd_source",
            "purpose": "response doublet requires zero odd source, especially Y5/Y6.",
        },
        {
            "source_id": "SRC1354_4_response_variation",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            "required_anchor": "AV517_4_Euler_equation",
            "purpose": "Euler equation has source-current blocker.",
        },
        {
            "source_id": "SRC1354_5_1011_qbound",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
            "required_anchor": "QBF1011_6_Y6_extra_stress",
            "purpose": "existing Y5/Y6 q_loc bound-fill rows.",
        },
        {
            "source_id": "SRC1354_6_1012_y5_doc",
            "source_path": "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            "required_anchor": "Y5C1012_0_radial_Meff_hair",
            "purpose": "Y5 eight-channel source-normalization vector.",
        },
        {
            "source_id": "SRC1354_7_1345_source_charge",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1345_SOURCE_CHARGE_RUNNER_INPUTS.csv",
            "required_anchor": "QIN1345_4_4_memory_class_scalar",
            "purpose": "current source-charge runner rejects symbolic closure rows.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def evenness_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "SFE1354_0_parent_exchange_symmetry",
            "claim_piece": "parent source functional has R_+ <-> R_- symmetry",
            "test": "S_source[R_+,R_-,matter,source,boundary]=S_source[R_-,R_+,matter,source,boundary]",
            "current_evidence": "Gamma_eff exchange symmetry exists only as response-sector template; source functional symmetry is not supplied",
            "status": "NOT_PARENT_SIGNED",
            "failure_consequence": "J_Z may be nonzero even if Gamma_eff is even",
        },
        {
            "clause_id": "SFE1354_1_source_pullback",
            "claim_piece": "sources couple only through R_even or quotient-visible data",
            "test": "delta_Z mu_source = delta_Z masses = delta_Z clock/readout = delta_Z boundary_reference = 0 at Z=0",
            "current_evidence": "1353/1012 retain measured-GM, source-normalization, readout, and species source rows",
            "status": "FAILED_CURRENT_EVIDENCE",
            "failure_consequence": "ordinary source/readout terms can generate J_Z",
        },
        {
            "clause_id": "SFE1354_2_Y5_measured_GM_evenness",
            "claim_piece": "measured-GM/source-normalization is exchange-even",
            "test": "all eight Y5 channels have theorem-zero or sourced numeric coefficients",
            "current_evidence": "1012 says Y5 owner theorem is not proved and all eight coefficient rows are retained/unfilled",
            "status": "NOT_DERIVED_HARD_BLOCK",
            "failure_consequence": "Newton/GR reduction can be spoiled by source-normalization J_Z",
        },
        {
            "clause_id": "SFE1354_3_Y6_extra_stress_evenness",
            "claim_piece": "extra stress is invisible/topological/exchange-even",
            "test": "T_extra has no linear Z contribution to Khat/Ward/PPN/source channels",
            "current_evidence": "1011 keeps Y6 extra-stress as retained debt; no invisibility theorem found",
            "status": "NOT_DERIVED_HARD_BLOCK",
            "failure_consequence": "Khat/Ward silence may fail through linear Delta_K[Y6]",
        },
        {
            "clause_id": "SFE1354_4_boundary_evenness",
            "claim_piece": "boundary/source-current functional is exchange-even or exact",
            "test": "B_Z=0 by parent boundary condition, fixed reference, or topological subtraction before readout",
            "current_evidence": "1353 B_Z row remains missing theorem/value; 1345 boundary rows are not zero-signed",
            "status": "OPEN",
            "failure_consequence": "bulk double-zero can leak through linked boundary/source flux",
        },
        {
            "clause_id": "SFE1354_5_readout_species_evenness",
            "claim_piece": "readout and species/material source maps are exchange-even",
            "test": "post-readout projector and species constants cannot add odd Z dependence",
            "current_evidence": "1345 keeps readout backreaction and source-only species prefactors live",
            "status": "UNSIGNED",
            "failure_consequence": "composition/readout channels can regenerate a first-order source",
        },
        {
            "clause_id": "SFE1354_6_verdict",
            "claim_piece": "source-functional evenness theorem",
            "test": "SFE1354_0 through SFE1354_5 all pass with source paths",
            "current_evidence": "source pullback, Y5, Y6, boundary, readout, and species clauses remain unsigned/open",
            "status": "THEOREM_NOT_PROVED",
            "failure_consequence": "must retain Y5/Y6 J_Z coefficient rows",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def y5y6_coefficients() -> list[dict[str, object]]:
    rows = [
        {
            "coefficient_id": "JZ1354_Y5_0_radial_Meff_hair",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_radial_Meff",
            "meaning": "linear Z coupling to radial effective-mass/source-measure hair",
            "units_required": "dimensionless or radial profile units mapped to beta_minus_1/alpha(lambda)",
            "observable_link": "partial_r ln(mu_obs); beta_minus_1; alpha(lambda); R11",
            "source_requirement": "radial no-hair theorem or numeric profile with source path",
            "current_status": "MISSING_THEOREM_OR_NUMERIC_PROFILE",
        },
        {
            "coefficient_id": "JZ1354_Y5_1_boundary_monopole",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_boundary",
            "meaning": "linear Z coupling to boundary monopole/source-reference shift",
            "units_required": "dimensionless",
            "observable_link": "beta_minus_1; alpha3; xi; Gdot_over_G; R11",
            "source_requirement": "boundary no-hair theorem or numeric coefficient",
            "current_status": "MISSING_BOUNDARY_ZERO_OR_COEFFICIENT",
        },
        {
            "coefficient_id": "JZ1354_Y5_2_domain_projector_mass",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_domain_projector",
            "meaning": "linear Z coupling from domain/projector source mass selection",
            "units_required": "dimensionless projector/source units",
            "observable_link": "alpha1; alpha2; alpha3; xi; R11",
            "source_requirement": "domain projector zero theorem or numeric projector products",
            "current_status": "MISSING_DOMAIN_PROJECTOR_ZERO_OR_VALUE",
        },
        {
            "coefficient_id": "JZ1354_Y5_3_bulk_X_Yukawa",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_bulk_X",
            "meaning": "linear Z coupling to finite-range bulk X/Yukawa source tail",
            "units_required": "dimensionless plus length scale",
            "observable_link": "alpha(lambda); R10; R11",
            "source_requirement": "bulk mass-gap theorem or source-backed alpha(lambda) curve",
            "current_status": "MISSING_BULK_GAP_OR_ALPHA_CURVE",
        },
        {
            "coefficient_id": "JZ1354_Y5_4_nonEH_operator",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_nonEH_source",
            "meaning": "linear Z coupling to non-EH operator/source potential",
            "units_required": "dimensionless or operator-family units",
            "observable_link": "gamma_minus_1; beta_minus_1; alpha(lambda); R11",
            "source_requirement": "EH-only theorem or non-EH coefficient map",
            "current_status": "MISSING_NONEH_OPERATOR_MAP",
        },
        {
            "coefficient_id": "JZ1354_Y5_5_species_source",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_species_A",
            "meaning": "linear Z coupling to species/material source charge",
            "units_required": "dimensionless by species/material pair",
            "observable_link": "eta_WEP_source_charge; clock source residual; R11",
            "source_requirement": "selector-blind source theorem or species charge vector",
            "current_status": "MISSING_SPECIES_CHARGE_VECTOR",
        },
        {
            "coefficient_id": "JZ1354_Y5_6_time_drift",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_time_drift",
            "meaning": "linear Z coupling to source-normalization time drift",
            "units_required": "dimensionless or per-time with convention",
            "observable_link": "Gdot_over_G; R11",
            "source_requirement": "stationarity theorem or time-drift coefficient",
            "current_status": "MISSING_STATIONARITY_OR_TIME_COEFFICIENT",
        },
        {
            "coefficient_id": "JZ1354_Y5_7_calibration_offset",
            "sector": "Y5_source_normalization",
            "symbol": "j_Z_calibration",
            "meaning": "linear Z coupling hidden in absolute source calibration",
            "units_required": "dimensionless",
            "observable_link": "beta_minus_1; Gdot_over_G; R11",
            "source_requirement": "parent fixed universal calibration theorem or retained offset value",
            "current_status": "MISSING_CALIBRATION_THEOREM_OR_OFFSET",
        },
        {
            "coefficient_id": "JZ1354_Y6_0_isotropic_extra_stress",
            "sector": "Y6_extra_stress",
            "symbol": "j_Z_Textra_iso",
            "meaning": "linear Z isotropic extra-stress contribution to Khat/Ward residual",
            "units_required": "stress-density or PPN-normalized units",
            "observable_link": "gamma_minus_1; beta_minus_1; source stress; R11",
            "source_requirement": "topological invisibility theorem or stress-response coefficient",
            "current_status": "MISSING_TEXTRA_ISO_THEOREM_OR_BOUND",
        },
        {
            "coefficient_id": "JZ1354_Y6_1_anisotropic_extra_stress",
            "sector": "Y6_extra_stress",
            "symbol": "j_Z_Textra_STF",
            "meaning": "linear Z tracefree/anisotropic extra-stress contribution",
            "units_required": "STF stress or PPN alpha_i units",
            "observable_link": "alpha1; alpha2; alpha3; xi; orbital preferred-frame residual",
            "source_requirement": "STF silence theorem or PPN/source-stress bound",
            "current_status": "MISSING_TEXTRA_STF_THEOREM_OR_BOUND",
        },
        {
            "coefficient_id": "JZ1354_Y6_2_boundary_stress_flux",
            "sector": "Y6_extra_stress",
            "symbol": "b_Z_Textra_boundary",
            "meaning": "linear Z extra-stress boundary flux",
            "units_required": "boundary stress-flux units",
            "observable_link": "M_eff flux; orbital/source closure; boundary force",
            "source_requirement": "boundary no-flux theorem or finite flux profile",
            "current_status": "MISSING_STRESS_BOUNDARY_FLUX_CERTIFICATE",
        },
        {
            "coefficient_id": "JZ1354_Y6_3_metric_response_tail",
            "sector": "Y6_extra_stress",
            "symbol": "delta_K_Z_Y6",
            "meaning": "linear Z mismatch between extra stress and Khat metric response",
            "units_required": "stress-response tensor units",
            "observable_link": "q_loc; PPN; R10/local residual vector",
            "source_requirement": "Khat metric-response match or Delta_K bound",
            "current_status": "MISSING_METRIC_RESPONSE_TAIL_BOUND",
        },
    ]
    for row in rows:
        row["coefficient_value_or_theorem"] = "MISSING"
        row["accepted_for_scoring"] = False
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def runner_rejections(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for row in rows:
        missing = []
        if str(row["coefficient_value_or_theorem"]).startswith("MISSING"):
            missing.append("MISSING_VALUE_OR_THEOREM")
        if not row.get("valid_for_claim", False):
            missing.append("VALID_FOR_CLAIM_FALSE")
        if not row.get("accepted_for_scoring", False):
            missing.append("NOT_ACCEPTED_FOR_SCORING")
        output.append(
            {
                "runner_id": "RUN_" + str(row["coefficient_id"]),
                "coefficient_id": row["coefficient_id"],
                "sector": row["sector"],
                "runner_verdict": "REJECT",
                "failure_reasons": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return output


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1354_0_source_evenness",
            "claim": "parent source functional is exchange-even in Z",
            "current_status": "BLOCKED",
            "reason": "source pullback, Y5, Y6, boundary, readout, and species clauses are unsigned/open",
        },
        {
            "gate_id": "GATE1354_1_JZ_zero",
            "claim": "J_Z/B_Z vanish in the compact local branch",
            "current_status": "BLOCKED",
            "reason": "Y5/Y6 coefficient rows are missing theorem-zero or numeric values",
        },
        {
            "gate_id": "GATE1354_2_response_doublet_physical",
            "claim": "response-doublet F1=0 is the physical q_loc/local-GR zero",
            "current_status": "BLOCKED",
            "reason": "source-functional evenness theorem failed current evidence",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1354_0_evenness_not_proved",
            "decision": "Source-functional exchange-evenness is not proved.",
            "why": "evenness of the response density does not automatically constrain matter, measured-GM, boundary, readout, or extra-stress couplings",
            "next_action": "treat Y5/Y6 J_Z coefficients as live nonclaim inputs",
        },
        {
            "decision_id": "DEC1354_1_Y5_priority",
            "decision": "Y5 is the highest-priority coupling target.",
            "why": "measured-GM/source-normalization sits directly between MTS and Newton/GR recovery",
            "next_action": "try to derive Y5 source functional pullback/flux closure before numeric scoring",
        },
        {
            "decision_id": "DEC1354_2_Y6_retained",
            "decision": "Y6 extra stress remains a separate Khat/Ward residual.",
            "why": "extra stress can spoil local-GR even if scalar Gamma_eff has a double-zero",
            "next_action": "only close it by topological invisibility, metric-response match, or sourced PPN/stress bound",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1354_0_1355",
            "target_file": "1355-Y5-R10-RAB-Y5-source-functional-pullback-or-JZ-source-normalization-basis.md",
            "target_script": "scripts/Y5_R10_RAB_Y5_source_functional_pullback_or_JZ_source_normalization_basis.py",
            "task": "try to derive Y5 measured-GM/source-normalization as a quotient/source pullback that is even in Z; if not, build the source-normalization J_Z basis row-by-row",
            "success_condition": "Y5 pullback theorem, or explicit nonclaim J_Z basis for source-normalization channels with units/source requirements",
            "do_not": "do not use response-density symmetry as source symmetry; do not absorb J_Z into fitted G; do not edit formalization-workbench or use GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate_outputs(
    sources: list[dict[str, object]],
    evenness: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    rejections: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1354_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in evenness if row["clause_id"] == "SFE1354_6_verdict")
    add(
        "VAL1354_1_evenness_not_proved",
        "source-functional evenness theorem is not promoted",
        verdict["status"] == "THEOREM_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["failure_consequence"]),
    )

    y5_rows = [row for row in coeffs if str(row["sector"]) == "Y5_source_normalization"]
    y6_rows = [row for row in coeffs if str(row["sector"]) == "Y6_extra_stress"]
    add(
        "VAL1354_2_Y5Y6_coefficients_present",
        "Y5 and Y6 JZ coefficient rows are present",
        len(y5_rows) >= 8 and len(y6_rows) >= 4,
        f"Y5={len(y5_rows)};Y6={len(y6_rows)}",
    )

    add(
        "VAL1354_3_coefficients_nonclaim",
        "all coefficient rows remain nonclaim and unscored",
        all(not row["accepted_for_scoring"] and not row["claim_allowed"] and row["coefficient_value_or_theorem"] == "MISSING" for row in coeffs),
        f"rows={len(coeffs)}",
    )

    add(
        "VAL1354_4_runner_rejects_all",
        "runner rejection rows reject every coefficient",
        len(rejections) == len(coeffs) and all(row["runner_verdict"] == "REJECT" and not row["claim_allowed"] for row in rejections),
        f"rejections={len(rejections)}",
    )

    add(
        "VAL1354_5_claim_gates_blocked",
        "all claim gates remain blocked",
        all(row["current_status"] == "BLOCKED" and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['current_status']}" for row in gates),
    )

    all_rows = sources + evenness + coeffs + rejections + gates + decisions + next_target
    add(
        "VAL1354_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1354*", "*1354-Y5-R10-RAB-source-functional*", "*Y5_R10_RAB_source_functional*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1354_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1354_8_next_target_1355",
        "next target routes to Y5 source-functional pullback",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1355-Y5-R10-RAB-Y5-source-functional"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1354_9_overall",
        "overall 1354 validation",
        all(row["status"] == "PASS" for row in validations),
        "1354 blocks source-evenness claim and installs Y5/Y6 JZ coefficient debts",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    evenness: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    rejections: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1354 does not prove source-functional exchange-evenness. The response density can be even in `Z` while the source/readout/GM/stress functional still carries linear `J_Z` terms.",
            "**Main progress:** Y5 and Y6 are now explicit coupling debts rather than fog. Y5 is the Newton/GR pressure point because it controls measured-GM/source-normalization; Y6 is the Khat/Ward pressure point because extra stress can re-enter the local residual even when scalar `Gamma_eff` double-zero algebra works.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Source-functional evenness attempt",
            table(["clause_id", "claim_piece", "test", "status", "failure_consequence"], evenness),
            "## Y5/Y6 JZ coefficient fill",
            table(["coefficient_id", "sector", "symbol", "meaning", "observable_link", "current_status", "accepted_for_scoring"], coeffs),
            "## Runner rejection",
            table(["runner_id", "coefficient_id", "sector", "runner_verdict", "failure_reasons"], rejections),
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
    evenness = evenness_attempt()
    coeffs = y5y6_coefficients()
    rejections = runner_rejections(coeffs)
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, evenness, coeffs, rejections, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(EVENNESS_ATTEMPT_PATH, evenness)
    write_csv(Y5Y6_COEFFICIENT_PATH, coeffs)
    write_csv(RUNNER_REJECTION_PATH, rejections)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, evenness, coeffs, rejections, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
