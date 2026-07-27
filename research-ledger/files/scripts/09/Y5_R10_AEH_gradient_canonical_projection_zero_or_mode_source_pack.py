from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "719-Y5-R10-AEH-gradient-canonical-projection-zero-or-mode-source-pack.md"
NEXT_TARGET = "720-Y5-R10-canonical-mode-kinetic-null-or-retained-ZM-source-pack.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "718_doc": {
        "path": POST_CHECKPOINT / "718-Y5-R10-AEH-prefactor-gradient-zero-theorem-or-retained-source-pack.md",
        "note": "AEH gradient gate and projection target",
    },
    "718_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_718_VALIDATION.csv",
        "note": "prior checkpoint validation",
    },
    "718_variation": {
        "path": RESIDUALS / "P8_Y5_R10_718_AEH_VARIATION_DERIVATION.csv",
        "note": "A_a projection condition and D=4 charge formula",
    },
    "718_source_pack": {
        "path": RESIDUALS / "P8_Y5_R10_718_RETAINED_AEH_SOURCE_PACK.csv",
        "note": "retained AEH source pack with A_a missing",
    },
    "718_queue": {
        "path": RESIDUALS / "P8_Y5_R10_718_BOUND_OR_DERIVE_QUEUE.csv",
        "note": "projection selected as next target",
    },
    "715_pack": {
        "path": RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
        "note": "minimum scalar coefficient pack with Z/M/E rows",
    },
    "716_doc": {
        "path": POST_CHECKPOINT / "716-Y5-R10-matter-coupling-source-charge-derivation-or-free-coefficient-lock.md",
        "note": "source charge definition",
    },
    "717_conformal": {
        "path": RESIDUALS / "P8_Y5_R10_717_CONFORMAL_DERIVATION.csv",
        "note": "D=4 Einstein-frame charge formula",
    },
    "708_contract": {
        "path": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
        "note": "source row contract for Z/M/canonical modes",
    },
    "708_expansion": {
        "path": RESIDUALS / "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
        "note": "symbolic local expansion and canonical-mode map",
    },
    "708_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_708_VALIDATION.csv",
        "note": "708 validation",
    },
    "714_queue": {
        "path": RESIDUALS / "P8_Y5_R10_714_RETAINED_BRANCH_SOURCE_QUEUE.csv",
        "note": "retained branch source queue",
    },
    "714_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_714_VALIDATION.csv",
        "note": "714 validation",
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def csv_contains(path: Path, *needles: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def all_valid_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]

    projection_theorem_audit = [
        {
            "audit_id": "PZT719_0_field_space",
            "clause": "field-space coordinates",
            "required_statement": "u^I and the background point u0 are fixed so a_I is a covector on a known field space",
            "current_status": "missing_field_list_and_background",
            "projection_effect": "cannot define physical projector without the field-space basis",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "PZT719_1_kinetic_rank",
            "clause": "kinetic metric and null directions",
            "required_statement": "Z_IJ(u0) is sourced and classified into positive, null/gauge, constrained, and ghost-forbidden directions",
            "current_status": "missing_Z_IJ_and_rank_classification",
            "projection_effect": "no-mode or null-mode theorem cannot be claimed",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "PZT719_2_mass_range",
            "clause": "mass/range matrix",
            "required_statement": "M2_IJ is sourced in the same field-space convention as Z_IJ",
            "current_status": "missing_M2_IJ",
            "projection_effect": "cannot distinguish exact silence from short-range suppression",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "PZT719_3_canonical_basis",
            "clause": "canonical diagonalization",
            "required_statement": "E_a^I diagonalizes the physical Z/M generalized eigenproblem and is normalized",
            "current_status": "missing_E_a_I",
            "projection_effect": "A_a=E_a^I a_I cannot be evaluated",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "PZT719_4_projection_zero",
            "clause": "observable AEH projection zero",
            "required_statement": "A_a=E_a^I a_I=0 for every physical local mode a, equivalently P_phys(a)=0",
            "current_status": "not_derived_current_corpus",
            "projection_effect": "would silence AEH gradient without requiring a_I=0",
            "valid_for_claim": "false",
            "source_paths": source_path_string("718_variation", "718_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "PZT719_5_no_mode",
            "clause": "no local scalar mode",
            "required_statement": "rank(P_phys)=0, or all scalar/class directions are gauge/topological/constrained with no propagating local source",
            "current_status": "not_parent_signed",
            "projection_effect": "would close local scalar branch toward GR",
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "PZT719_6_short_range_not_zero",
            "clause": "massive short-range suppression",
            "required_statement": "large m_a or tiny lambda_a is a bound/scoring route, not an exact local-GR theorem",
            "current_status": "guard_active",
            "projection_effect": "prevents replacing projection zero with range suppression",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "PZT719_7_verdict",
            "clause": "claim-ready projection silence",
            "required_statement": "field list, Z/M, E modes, rank/null classification, and A_a=0/no-mode theorem are all sourced",
            "current_status": "fail_current_corpus",
            "projection_effect": "projection silence not claimable yet",
            "valid_for_claim": "false",
            "source_paths": source_path_string("718_doc", "715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    canonical_mode_derivation = [
        {
            "step_id": "CMD719_0_quadratic_action",
            "object": "local scalar quadratic branch",
            "equation": "S_2 = int sqrt(-g)[-1/2 Z_IJ nabla delta u^I nabla delta u^J - 1/2 M2_IJ delta u^I delta u^J + J_I delta u^I]",
            "result": "Z_IJ and M2_IJ decide whether scalar/class directions are physical modes or constraints",
            "status": "derived_shape",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CMD719_1_generalized_modes",
            "object": "canonical physical modes",
            "equation": "M2_IJ E_a^J = m_a^2 Z_IJ E_a^J, with E_a^I Z_IJ E_b^J = delta_ab on the physical subspace",
            "result": "only non-null normalized modes enter local fifth-force/PPN scoring",
            "status": "conditional_formula",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CMD719_2_physical_projector",
            "object": "physical mode projector",
            "equation": "P_phys is the projector onto non-gauge, non-null, non-topological scalar directions selected by Z/M and constraints",
            "result": "exact AEH silence requires P_phys^T a = 0, not merely small a_I",
            "status": "conditional_zero_condition",
            "valid_for_claim": "false",
            "source_paths": source_path_string("718_variation", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CMD719_3_AEH_projection",
            "object": "AEH projected source",
            "equation": "A_a := E_a^I a_I",
            "result": "A_a is the observable AEH-gradient coupling to canonical mode a",
            "status": "definition",
            "valid_for_claim": "false",
            "source_paths": source_path_string("718_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CMD719_4_effective_charge",
            "object": "D=4 retained scalar charge",
            "equation": "Q_Aa = N_frame(E_a^I b_A,I - A_a/2)",
            "result": "projection zero A_a=0 removes AEH frame charge but still leaves matter charge E_a^I b_A,I",
            "status": "derived_from_716_717_718",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal", "718_variation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CMD719_5_range",
            "object": "mode range",
            "equation": "lambda_a = hbar/(m_a c) or lambda_a=1/m_a in natural units with stated convention",
            "result": "range affects R10 scoring; it is not an exact projection-zero theorem",
            "status": "conditional_formula",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    mode_source_pack = [
        {
            "pack_id": "MSP719_0_field_list",
            "symbol": "u^I",
            "definition": "ordered retained scalar/class field coordinates",
            "current_value_or_status": "MISSING_FIELD_LIST",
            "units": "field_units",
            "priority": "P0",
            "unlocks": "defines a_I, Z_IJ, M2_IJ, E_a^I indices",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "MSP719_1_kinetic",
            "symbol": "Z_IJ",
            "definition": "field-space kinetic metric at u0 with rank/null/gauge classification",
            "current_value_or_status": "MISSING_KINETIC_METRIC_AND_RANK",
            "units": "dimensionless_or_field_units",
            "priority": "P0",
            "unlocks": "no-mode theorem or physical projector",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "MSP719_2_mass",
            "symbol": "M2_IJ",
            "definition": "mass/range matrix in same convention as Z_IJ",
            "current_value_or_status": "MISSING_MASS_MATRIX",
            "units": "mass_squared",
            "priority": "P1",
            "unlocks": "lambda_a and range-dependent R10 scoring",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "MSP719_3_modes",
            "symbol": "E_a^I",
            "definition": "canonical physical mode basis normalized with Z_IJ",
            "current_value_or_status": "MISSING_CANONICAL_DIAGONALIZATION",
            "units": "mixed",
            "priority": "P0",
            "unlocks": "A_a, Q_Aa, alpha(lambda), PPN maps",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "MSP719_4_AEH_projection",
            "symbol": "A_a",
            "definition": "E_a^I a_I",
            "current_value_or_status": "MISSING_AEH_CANONICAL_PROJECTION",
            "units": "canonical_inverse_field_units",
            "priority": "P0",
            "unlocks": "decides whether AEH gradient is physically visible",
            "valid_for_claim": "false",
            "source_paths": source_path_string("718_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "MSP719_5_matter_projection",
            "symbol": "B_Aa",
            "definition": "E_a^I b_A,I",
            "current_value_or_status": "MISSING_MATTER_CHARGE_PROJECTION",
            "units": "canonical_inverse_field_units",
            "priority": "P1",
            "unlocks": "WEP and source/test charge scoring",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "MSP719_6_effective_charge",
            "symbol": "Q_Aa",
            "definition": "N_frame(B_Aa - A_a/2)",
            "current_value_or_status": "MISSING_EFFECTIVE_CANONICAL_CHARGE",
            "units": "dimensionless",
            "priority": "P1",
            "unlocks": "R10 alpha, PPN, WEP, clocks",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal", "718_variation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "MSP719_7_range",
            "symbol": "lambda_a",
            "definition": "hbar/(m_a c) after canonical mass diagonalization",
            "current_value_or_status": "MISSING_RANGE",
            "units": "length",
            "priority": "P2",
            "unlocks": "R10 alpha(lambda) x-axis",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    projection_branch_matrix = [
        {
            "branch_id": "PBM719_0_no_mode",
            "branch": "no physical scalar mode",
            "condition": "rank(P_phys)=0 or all scalar/class directions are gauge/topological/constrained",
            "local_effect": "A_a and Q_Aa absent",
            "status": "not_parent_signed",
            "claim_effect": "would strongly support local-GR branch if signed with conservation owner",
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "PBM719_1_AEH_projection_zero",
            "branch": "AEH projection zero",
            "condition": "A_a=E_a^I a_I=0 for all physical modes",
            "local_effect": "AEH frame charge removed, matter charge still needs b_A,I branch",
            "status": "not_derived",
            "claim_effect": "partial local rescue, not complete GR reduction",
            "valid_for_claim": "false",
            "source_paths": source_path_string("718_variation", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "PBM719_2_charge_cancellation",
            "branch": "source charge cancellation",
            "condition": "B_Aa=A_a/2 for every relevant source/test A and mode a",
            "local_effect": "Q_Aa=0 by cancellation",
            "status": "not_derived",
            "claim_effect": "very strong and fragile; would need a symmetry, not fitting",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "718_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "PBM719_3_retained_mode",
            "branch": "retained physical scalar mode",
            "condition": "A_a or B_Aa nonzero for at least one finite-range physical mode",
            "local_effect": "score R10/PPN/WEP/Gdot/R11 with sourced coefficients",
            "status": "selected_fallback_if_projection_fails",
            "claim_effect": "no local-GR claim; empirical scoring required",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    local_observable_update = [
        {
            "arena_id": "LOU719_0_Newton",
            "arena": "Newtonian limit",
            "projection_dependency": "A0 plus sum_a Q_Aa Q_Ba exp(-r/lambda_a); exact GR-like Newtonian limit needs no mode or Q_Aa=0/short-range bound",
            "current_status": "blocked_until_modes_charges_ranges_sourced",
            "claim_effect": "no Newton pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "718_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOU719_1_R10",
            "arena": "fifth force",
            "projection_dependency": "alpha_AB,a(lambda_a)=Q_Aa Q_Ba with Q_Aa=N_frame(B_Aa-A_a/2)",
            "current_status": "blocked_until_real_Q_lambda_bound_curve",
            "claim_effect": "no R10 score",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion", "718_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOU719_2_PPN",
            "arena": "PPN gamma/beta",
            "projection_dependency": "universal nonzero Q_Aa contributes scalar-tensor PPN; beta needs derivative of projected charge",
            "current_status": "blocked_until_projection_and_derivative_rows_sourced",
            "claim_effect": "no PPN pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOU719_3_WEP",
            "arena": "WEP",
            "projection_dependency": "composition dependence lives in B_Aa after common A_a shift",
            "current_status": "blocked_until_material_charge_projection_sourced",
            "claim_effect": "no WEP pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOU719_4_R11",
            "arena": "retained scalar operator class",
            "projection_dependency": "if P_phys rank nonzero, scalar branch remains an R11 operator until scored",
            "current_status": "blocked_until_ZM_mode_source_pack",
            "claim_effect": "no R11 closure",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_contract", "714_queue"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    decision = [
        {
            "decision_id": "D719_0_projection_zero",
            "target": "A_a=E_a^I a_I=0",
            "result": "not_available_current_corpus",
            "reason": "physical mode basis and projector are missing",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D719_1_no_mode",
            "target": "rank(P_phys)=0/no local scalar",
            "result": "not_available_current_corpus",
            "reason": "Z_IJ rank/null/gauge classification is missing",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D719_2_retained_source",
            "target": "retained canonical mode source pack",
            "result": "selected_current_route",
            "reason": "source Z_IJ, M2_IJ, E_a^I, A_a, B_Aa, Q_Aa, and lambda_a or prove a no-mode theorem",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BDQ719_0_Z_rank",
            "target": "Z_IJ rank/null/gauge classification",
            "preferred_route": "derive all scalar/class directions are non-propagating/gauge/topological",
            "fallback_route": "source Z_IJ and construct physical projector",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ719_1_M2_modes",
            "target": "M2_IJ and E_a^I",
            "preferred_route": "derive no finite-range physical modes",
            "fallback_route": "source mass matrix and diagonalize canonical modes",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ719_2_projection_score",
            "target": "A_a and B_Aa projections",
            "preferred_route": "derive A_a=0 and B_Aa=0/cancellation",
            "fallback_route": "score Q_Aa and lambda_a against local tests",
            "priority": "P1",
            "next_artifact": "retained_scalar_local_residual_score_pack_after_ZM",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "718_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    claim_gate_evaluation = [
        {
            "gate_id": "CG719_0_prior_718",
            "gate": "prior AEH gradient checkpoint",
            "observed_state": "718 validation clean and nonclaim",
            "result": "pass_structure",
            "claim_effect": "can build projection gate without promoting claims",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG719_1_projection_zero",
            "gate": "A_a=0 projection theorem",
            "observed_state": "E_a^I missing",
            "result": "fail_blocked",
            "claim_effect": "AEH gradient silence not claimable",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG719_2_no_mode",
            "gate": "no physical scalar mode theorem",
            "observed_state": "Z_IJ rank/null/gauge classification missing",
            "result": "fail_blocked",
            "claim_effect": "local scalar closure not claimable",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG719_3_short_range_guard",
            "gate": "short range vs exact zero",
            "observed_state": "M2/lambda missing and range suppression is not theorem zero",
            "result": "pass_guard",
            "claim_effect": "prevents range suppression from becoming fake GR proof",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG719_4_local_claims",
            "gate": "local-GR/Newton/PPN/R10/WEP/R11",
            "observed_state": "mode/source coefficients missing",
            "result": "fail_blocked",
            "claim_effect": "no local claim",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG719_5_next_target",
            "gate": "next derivation target",
            "observed_state": NEXT_TARGET,
            "result": "pass_structure",
            "claim_effect": "go after Z/M/no-mode next",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_AEH_gradient_projection_zero_failed_mode_source_pack_written_nonclaim",
            "claim_ceiling": "canonical_projection_contract_only_no_Aa_zero_no_no_mode_no_local_GR_Newton_PPN_R10_WEP_R11_claim",
            "main_result": "projection silence is the right theorem target but cannot be claimed without Z/M/E mode data",
            "projection_formula": "A_a=E_a^I a_I",
            "retained_charge_formula": "Q_Aa=N_frame(B_Aa-A_a/2), B_Aa=E_a^I b_A,I",
            "remaining_blocker": "Z_IJ rank/null classification, M2_IJ, canonical modes E_a^I, A_a, B_Aa, lambda_a",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
    ]

    csv_outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_719_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "role", "valid_for_claim", "generated_utc"],
        ),
        "projection_theorem_audit": (
            RESIDUALS / "P8_Y5_R10_719_CANONICAL_PROJECTION_THEOREM_AUDIT.csv",
            projection_theorem_audit,
            ["audit_id", "clause", "required_statement", "current_status", "projection_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "canonical_mode_derivation": (
            RESIDUALS / "P8_Y5_R10_719_CANONICAL_MODE_DERIVATION.csv",
            canonical_mode_derivation,
            ["step_id", "object", "equation", "result", "status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "mode_source_pack": (
            RESIDUALS / "P8_Y5_R10_719_MODE_SOURCE_PACK.csv",
            mode_source_pack,
            ["pack_id", "symbol", "definition", "current_value_or_status", "units", "priority", "unlocks", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "projection_branch_matrix": (
            RESIDUALS / "P8_Y5_R10_719_PROJECTION_BRANCH_MATRIX.csv",
            projection_branch_matrix,
            ["branch_id", "branch", "condition", "local_effect", "status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "local_observable_update": (
            RESIDUALS / "P8_Y5_R10_719_LOCAL_OBSERVABLE_UPDATE.csv",
            local_observable_update,
            ["arena_id", "arena", "projection_dependency", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "decision": (
            RESIDUALS / "P8_Y5_R10_719_ZERO_OR_MODE_SOURCE_DECISION.csv",
            decision,
            ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_719_BOUND_OR_DERIVE_QUEUE.csv",
            bound_or_derive_queue,
            ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "claim_gate_evaluation": (
            RESIDUALS / "P8_Y5_R10_719_CLAIM_GATE_EVALUATION.csv",
            claim_gate_evaluation,
            ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_719_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "main_result",
                "projection_formula",
                "retained_charge_formula",
                "remaining_blocker",
                "next_target",
                "valid_for_claim",
                "generated_utc",
            ],
        ),
    }

    for path, rows, fields in csv_outputs.values():
        write_csv(path, rows, fields)

    generated_csv_paths = [path for path, _, _ in csv_outputs.values()]
    validation: list[dict[str, str]] = []

    def add_check(check_id: str, ok: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if ok else "fail",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    all_sources_exist = all(info["path"].exists() for info in SOURCES.values())
    add_check("V719_0_source_paths_exist", all_sources_exist, "all cited source paths exist" if all_sources_exist else "missing source path")

    add_check(
        "V719_1_prior_718_clean",
        prior_validation_clean(SOURCES["718_validation"]["path"]),
        "718_validation_failures=0",
    )

    older_clean = all(prior_validation_clean(SOURCES[key]["path"]) for key in ["708_validation", "714_validation"])
    add_check("V719_2_supporting_validations_clean", older_clean, "708 and 714 validations clean" if older_clean else "supporting validation not clean")

    pack_715 = SOURCES["715_pack"]["path"]
    add_check(
        "V719_3_Z_M_E_missing_confirmed",
        csv_contains(pack_715, "MISSING_KINETIC_METRIC", "MISSING_MASS_MATRIX", "MISSING_CANONICAL_DIAGONALIZATION"),
        "715 pack confirms Z/M/E missing",
    )

    add_check(
        "V719_4_projection_selected_by_718",
        csv_contains(SOURCES["718_queue"]["path"], "A_a=E_a^I a_I", "719-Y5-R10-AEH-gradient-canonical-projection-zero-or-mode-source-pack.md"),
        "718 queue selected projection target",
    )

    projection_audit_path = csv_outputs["projection_theorem_audit"][0]
    add_check(
        "V719_5_projection_zero_not_promoted",
        csv_contains(projection_audit_path, "PZT719_7_verdict", "fail_current_corpus"),
        "projection silence not promoted",
    )

    mode_derivation_path = csv_outputs["canonical_mode_derivation"][0]
    add_check(
        "V719_6_physical_projector_formula_written",
        csv_contains(mode_derivation_path, "P_phys", "P_phys^T a = 0"),
        "physical projector zero condition written",
    )

    add_check(
        "V719_7_Aa_charge_formula_written",
        csv_contains(mode_derivation_path, "A_a := E_a^I a_I", "Q_Aa = N_frame(E_a^I b_A,I - A_a/2)"),
        "A_a and retained charge formula written",
    )

    source_pack_path = csv_outputs["mode_source_pack"][0]
    add_check(
        "V719_8_mode_source_pack_missing_markers",
        csv_contains(source_pack_path, "MISSING_KINETIC_METRIC_AND_RANK", "MISSING_CANONICAL_DIAGONALIZATION", "MISSING_AEH_CANONICAL_PROJECTION"),
        "mode source pack keeps missing markers",
    )

    add_check(
        "V719_9_no_mode_not_parent_signed",
        csv_contains(csv_outputs["projection_branch_matrix"][0], "PBM719_0_no_mode", "not_parent_signed"),
        "no-mode branch not parent-signed",
    )

    add_check(
        "V719_10_local_arenas_blocked",
        all("blocked" in row["current_status"] for row in local_observable_update),
        "all local observable rows blocked until sourced",
    )

    add_check(
        "V719_11_next_target_selected",
        csv_contains(csv_outputs["decision"][0], NEXT_TARGET) and csv_contains(csv_outputs["bound_or_derive_queue"][0], NEXT_TARGET),
        NEXT_TARGET,
    )

    add_check(
        "V719_12_no_claim_rows_promoted",
        all_valid_false(generated_csv_paths),
        "all generated rows valid_for_claim=false",
    )

    outputs_scoped = all(str(path).startswith(str(POST_CHECKPOINT)) for path in generated_csv_paths + [OUTPUT_DOC])
    add_check("V719_13_outputs_scoped", outputs_scoped, "all outputs under post-checkpoint-work")

    formalization_count = formalization_changed_after_cutoff()
    add_check(
        "V719_14_formalization_workbench_untouched",
        formalization_count == 0,
        f"formalization_changed_after_cutoff={formalization_count}",
    )

    add_check(
        "V719_15_short_range_guard",
        csv_contains(projection_audit_path, "PZT719_6_short_range_not_zero", "guard_active"),
        "range suppression is not promoted to exact zero",
    )

    add_check(
        "V719_16_status_nonclaim",
        csv_contains(csv_outputs["nonclaim_summary"][0], "no_Aa_zero_no_no_mode_no_local_GR"),
        "projection contract only; no local claim",
    )

    add_check(
        "V719_17_source_register_written",
        len(source_register) >= 12 and all(row["exists"] == "true" for row in source_register),
        f"source_rows={len(source_register)}",
    )

    validation_path = RESIDUALS / "P8_Y5_BRR545_719_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "result", "detail", "generated_utc"])

    sections = [
        "# 719 - Y5 R10 AEH Gradient Canonical Projection Zero Or Mode Source Pack",
        "",
        "## Summary",
        "",
        "This checkpoint tests the sharper rescue from 718: `a_I` itself does not have to vanish if its observable canonical projection vanishes.",
        "",
        "The exact target is:",
        "",
        "`A_a := E_a^I a_I = 0` for every physical local scalar mode `a`, equivalently `P_phys^T a = 0`.",
        "",
        "The current corpus cannot claim that yet because the physical mode data are missing: `Z_IJ`, `M2_IJ`, `E_a^I`, rank/null classification, and the no-mode theorem are not sourced.",
        "",
        "The retained D=4 scalar charge is now sharpened to",
        "",
        "`Q_Aa = N_frame (B_Aa - A_a/2)`, with `B_Aa=E_a^I b_A,I`.",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Generated UTC | `{GENERATED_UTC}` |",
        "| Claim status | nonclaim/private checkpoint |",
        f"| Next target | `{NEXT_TARGET}` |",
        "",
        "## Projection Theorem Audit",
        "",
        markdown_table(projection_theorem_audit, ["audit_id", "clause", "current_status", "projection_effect", "valid_for_claim"]),
        "",
        "## Canonical Mode Derivation",
        "",
        markdown_table(canonical_mode_derivation, ["step_id", "object", "equation", "result", "status", "valid_for_claim"]),
        "",
        "## Mode Source Pack",
        "",
        markdown_table(mode_source_pack, ["pack_id", "symbol", "definition", "current_value_or_status", "priority", "unlocks", "valid_for_claim"]),
        "",
        "## Projection Branch Matrix",
        "",
        markdown_table(projection_branch_matrix, ["branch_id", "branch", "condition", "local_effect", "status", "claim_effect", "valid_for_claim"]),
        "",
        "## Local Observable Update",
        "",
        markdown_table(local_observable_update, ["arena_id", "arena", "projection_dependency", "current_status", "claim_effect", "valid_for_claim"]),
        "",
        "## Zero Or Mode Source Decision",
        "",
        markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Bound Or Derive Queue",
        "",
        markdown_table(bound_or_derive_queue, ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim"]),
        "",
        "## Claim Gate Evaluation",
        "",
        markdown_table(claim_gate_evaluation, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"]),
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "projection_formula", "retained_charge_formula", "remaining_blocker", "next_target", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        markdown_table(source_register, ["source_id", "path", "exists", "role"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Verdict",
        "",
        "The projection route is good physics, but it is not closed. We now know the exact thing to prove: either no physical scalar mode exists, or the physical projector kills the AEH gradient, `P_phys^T a=0`. Without `Z_IJ`, `M2_IJ`, and `E_a^I`, that cannot be claimed. Next move is therefore the kinetic/null-mode gate: prove the scalar directions are non-propagating, or source the retained mode pack and score the branch honestly.",
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")

    passes = sum(1 for row in validation if row["result"] == "pass")
    total = len(validation)
    print(f"Y5_R10_AEH_gradient_projection_zero_failed_mode_source_pack_written_nonclaim: validation_passes={passes}/{total}")


if __name__ == "__main__":
    main()
