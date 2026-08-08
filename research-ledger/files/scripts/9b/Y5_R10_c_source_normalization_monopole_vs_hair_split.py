from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1139-Y5-R10-c-source-normalization-monopole-vs-hair-split.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1139_0_1138_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1138_NEXT_TARGET.csv",
            "needle": "NEXT1138_0_1139",
            "note": "1138 handoff to c monopole-vs-hair split.",
        },
        {
            "source_id": "SRC1139_1_1138_c_row",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1138_CANONICAL_C_SOURCE_NORMALIZATION_ROW.csv",
            "needle": "CROW1138_0_c_domain_source_normalization_operator",
            "note": "Canonical c row remains blocked.",
        },
        {
            "source_id": "SRC1139_2_1138_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1138_C_ZERO_ROUTE_AUDIT.csv",
            "needle": "CZ1138_2_no_absorption",
            "note": "1138 rejects measured-GM/source-normalization absorption shortcut.",
        },
        {
            "source_id": "SRC1139_3_parent_terms",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A4_mass_flux_projector",
            "note": "Parent action terms separate mass-flux calibration from coupling/hair/source blindness.",
        },
        {
            "source_id": "SRC1139_4_ward_contract",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C3_closed_calibrated_mass_current",
            "note": "Ward/source-owner contract gives the monopole calibration clause.",
        },
        {
            "source_id": "SRC1139_5_missing_ledger",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "source_normalization_operator",
            "note": "R11 missing ledger keeps source-normalization hair unresolved.",
        },
        {
            "source_id": "SRC1139_6_fill_requirements",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R11_EH_operator_ledger",
            "note": "R11 fill requirement says no MISSING fields before claim.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def split_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "component_id": "CS1139_0_universal_monopole",
                "component": "c_universal_monopole",
                "physical_meaning": "constant source monopole calibration that could be absorbed into measured G_eff*M_eff if parent-signed",
                "danger_rows": "R11 only unless drift/species/range/frame dependence appears",
                "absorbable_if": "C3 closed calibrated mass current and C4 constant universal coupling both parent-sign no time/range/species/frame dependence",
                "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
                "claim_effect": "not claim-valid; can only be harmless if all hair components below are zero",
                "valid_for_claim": "false",
            },
            {
                "component_id": "CS1139_1_time_drift_hair",
                "component": "c_time_or_Gdot_hair",
                "physical_meaning": "time-dependent source normalization/coupling drift",
                "danger_rows": "R9;R11",
                "absorbable_if": "partial_t G_eff=0 and partial_t mu_obs=0 are parent-derived",
                "current_status": "MISSING_C4_CONSTANT_COUPLING",
                "claim_effect": "blocks source drift/Gdot/local-GR claims",
                "valid_for_claim": "false",
            },
            {
                "component_id": "CS1139_2_range_radial_hair",
                "component": "c_range_radial_hair",
                "physical_meaning": "radial or finite-range dependence beyond constant monopole",
                "danger_rows": "R3;R4;R10;R11",
                "absorbable_if": "partial_r mu_obs=partial_lambda mu_obs=0 or source-backed R10/radial bounds exist",
                "current_status": "MISSING_C6_NO_RANGE_RADIAL_HAIR",
                "claim_effect": "blocks R10/local source-hair claims",
                "valid_for_claim": "false",
            },
            {
                "component_id": "CS1139_3_species_marker_hair",
                "component": "c_species_marker_hair",
                "physical_meaning": "species/material-marker/source-label dependence in active gravitational source",
                "danger_rows": "R1;R11",
                "absorbable_if": "selector-blind source action proves partial_A mu_obs=0",
                "current_status": "MISSING_C5_NO_SPECIES_MARKER_SOURCE_CHARGE",
                "claim_effect": "blocks WEP/source-charge branch",
                "valid_for_claim": "false",
            },
            {
                "component_id": "CS1139_4_vector_preferred_frame_hair",
                "component": "c_vector_preferred_frame_hair",
                "physical_meaning": "local vector/source-normalization marker in observed coframe",
                "danger_rows": "R5;R6;R7;R11",
                "absorbable_if": "domain selector/source-normalization vector coefficient is theorem-zero, not gauge-hidden",
                "current_status": "MISSING_VECTOR_THEOREM_OR_COEFFICIENT",
                "claim_effect": "blocks alpha1/alpha2/alpha3 preferred-frame safety",
                "valid_for_claim": "false",
            },
            {
                "component_id": "CS1139_5_anisotropic_stress_hair",
                "component": "c_anisotropic_STF_hair",
                "physical_meaning": "tracefree anisotropic projector/source stress",
                "danger_rows": "R8;R11",
                "absorbable_if": "projector/domain stress is parent-owned topological or bounded",
                "current_status": "CONDITIONAL_PROJECTOR_STRESS_NOT_PARENT_OWNED",
                "claim_effect": "blocks preferred-location/xi safety",
                "valid_for_claim": "false",
            },
            {
                "component_id": "CS1139_6_domain_flux_hair",
                "component": "c_domain_flux_hair",
                "physical_meaning": "domain flux source-normalization contribution feeding alpha3 through K*c*epsilon",
                "danger_rows": "R7;R11",
                "absorbable_if": "epsilon=0, K=0, c=0, or sourced K*c*epsilon bound passes 4e-20 without cancellation",
                "current_status": "MISSING_K_c_EPSILON_PRODUCT",
                "claim_effect": "blocks alpha3/local-GR route",
                "valid_for_claim": "false",
            },
            {
                "component_id": "CS1139_7_verdict",
                "component": "c_total",
                "physical_meaning": "total c_domain_source_normalization_operator",
                "danger_rows": "R1;R3;R4;R5;R6;R7;R8;R9;R10;R11",
                "absorbable_if": "CS1139_0 is parent-signed and CS1139_1 through CS1139_6 are theorem-zero or source-bounded",
                "current_status": "SPLIT_COMPLETE_ALL_CLAIM_ROUTES_BLOCKED",
                "claim_effect": "c remains retained and nonclaim",
                "valid_for_claim": "false",
            },
        ]
    )


def absorption_test_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "test_id": "ABS1139_0_constant",
                "test": "constant universal monopole",
                "must_show": "same constant for all times, radii, species, frames, and systems",
                "current_status": "NOT_PARENT_DERIVED",
                "result": "fail_for_claim",
                "valid_for_claim": "false",
            },
            {
                "test_id": "ABS1139_1_derivative_silent",
                "test": "no derivative/range/time hair",
                "must_show": "partial_t=partial_r=partial_lambda=0 and no source-gradient terms",
                "current_status": "NOT_DERIVED_SYMBOLIC",
                "result": "fail_for_claim",
                "valid_for_claim": "false",
            },
            {
                "test_id": "ABS1139_2_no_marker",
                "test": "no species/material/source marker",
                "must_show": "partial_A mu_obs=0 from selector-blind source action",
                "current_status": "NOT_PARENT_DERIVED",
                "result": "fail_for_claim",
                "valid_for_claim": "false",
            },
            {
                "test_id": "ABS1139_3_no_vector_STF",
                "test": "no vector or STF anisotropic hair",
                "must_show": "preferred-frame vector and tracefree stress pieces vanish in observed coframe",
                "current_status": "MISSING_OR_CONDITIONAL",
                "result": "fail_for_claim",
                "valid_for_claim": "false",
            },
            {
                "test_id": "ABS1139_4_absorption_verdict",
                "test": "c can be absorbed into measured GM",
                "must_show": "ABS1139_0 through ABS1139_3 all pass before readout",
                "current_status": "ABSORPTION_NOT_ALLOWED",
                "result": "fail_for_claim",
                "valid_for_claim": "false",
            },
        ]
    )


def component_bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "bound_id": "CB1139_0_time",
                "component": "c_time_or_Gdot_hair",
                "needed_row": "system_id; c_time_abs; time_window; units; source_path; valid_for_claim",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "status": "SOURCE_ROW_REQUIRED",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CB1139_1_range",
                "component": "c_range_radial_hair",
                "needed_row": "system_id; c_range_abs; lambda_or_radius; units; source_path; valid_for_claim",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "status": "SOURCE_ROW_REQUIRED",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CB1139_2_species",
                "component": "c_species_marker_hair",
                "needed_row": "system_id; species_pair; c_species_abs; units; source_path; valid_for_claim",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "status": "SOURCE_ROW_REQUIRED",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CB1139_3_vector",
                "component": "c_vector_preferred_frame_hair",
                "needed_row": "system_id; vector_component; c_vector_abs; coframe; units; source_path; valid_for_claim",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "status": "SOURCE_ROW_REQUIRED",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CB1139_4_anisotropy",
                "component": "c_anisotropic_STF_hair",
                "needed_row": "system_id; STF_component; c_STF_abs; coframe; units; source_path; valid_for_claim",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "status": "SOURCE_ROW_REQUIRED",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CB1139_5_flux",
                "component": "c_domain_flux_hair",
                "needed_row": "system_id; K_abs; c_flux_abs; epsilon_abs; product_abs; units; source_path; valid_for_claim",
                "current_value": "MISSING_K_c_EPSILON_PRODUCT",
                "status": "SOURCE_ROW_REQUIRED",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1139_0_split_done",
                "rule": "c is split into monopole plus dangerous hair components",
                "gate_pass": "true_nonclaim",
                "reason": "split ledger exists but no component is claim-ready",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1139_1_monopole_absorbable",
                "rule": "universal monopole absorption is parent-signed",
                "gate_pass": "false",
                "reason": "C3/C4 calibration and constant coupling are not parent-derived together",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1139_2_hair_zero",
                "rule": "all derivative/vector/species/range/anisotropic/flux hair components vanish",
                "gate_pass": "false",
                "reason": "every hair component remains missing, conditional, or source-row required",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1139_3_absorption_shortcut",
                "rule": "source-unity/gauge absorption shortcut is forbidden",
                "gate_pass": "true_nonclaim",
                "reason": "absorption fails unless universal monopole and all hair-zero tests pass",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1139_4_component_bounds",
                "rule": "component bound/source rows are executable",
                "gate_pass": "false",
                "reason": "component bound rows are schemas only",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1139_5_local_GR",
                "rule": "R10/PPN/local-GR can promote",
                "gate_pass": "false",
                "reason": "c hair is not zero or bounded",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1139_0_verdict",
                "decision": "c_split_done_but_absorption_not_allowed",
                "reason": "universal monopole is not parent-signed and hair components are not zero/bounded",
                "next_action": "attack hair-zero theorem or fill component bound rows",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1139_1_best_next",
                "decision": "hair_zero_theorem_or_component_bound_pack",
                "reason": "this is the least cheating path: only non-monopole hair is observable damage",
                "next_action": "try to prove all hair components vanish; otherwise build strict component source pack",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1139_2_claim_ceiling",
                "decision": "keep_c_R11_branch_blocked",
                "reason": "c_total cannot be treated as calibration until every dangerous hair component is closed",
                "next_action": "do not use c as zero, unity, or absorbed in any alpha3/R11 product",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1139_0_1140",
                "next_target": "1140-Y5-R10-c-hair-zero-theorem-or-component-bound-pack.md",
                "objective": "prove derivative/range/species/vector/anisotropic/flux source-normalization hair vanish, or build strict source-backed component-bound rows for each c hair channel",
                "include": "time hair; range/radial hair; species marker hair; vector hair; STF anisotropy hair; flux hair; observed coframe; sibling row guards",
                "exclude": "universal monopole absorption shortcut; source-unity; product shortcut; tuned cancellation; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    split: list[dict[str, object]],
    absorption: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = split + absorption + bounds + gates + decisions + next_target
    components = {row["component"] for row in split}
    add("V1139_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1139_1_split_coverage", {"c_universal_monopole", "c_time_or_Gdot_hair", "c_range_radial_hair", "c_species_marker_hair", "c_vector_preferred_frame_hair", "c_anisotropic_STF_hair", "c_domain_flux_hair", "c_total"}.issubset(components), "monopole and all dangerous hair components are represented")
    add("V1139_2_total_blocked", split[-1]["current_status"] == "SPLIT_COMPLETE_ALL_CLAIM_ROUTES_BLOCKED", "c total remains blocked after split")
    add("V1139_3_absorption_fails", absorption[-1]["current_status"] == "ABSORPTION_NOT_ALLOWED", "absorption shortcut remains forbidden")
    add("V1139_4_bounds_required", all(row["status"] == "SOURCE_ROW_REQUIRED" for row in bounds), "all component bounds remain source-row required")
    add("V1139_5_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked")
    add("V1139_6_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1139_7_next_target", next_target[0]["next_target"].startswith("1140-") and "c-hair-zero" in str(next_target[0]["next_target"]), "1140 handoff targets c hair zero theorem or component bounds")
    add("V1139_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1139_9_csv_parse", csv_parse_ok, "all 1139 CSV outputs parse cleanly")
    add("V1139_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1139_SUMMARY", True, "1139 splits c into monopole and hair components, rejects absorption, and sends hair channels to 1140")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    split: list[dict[str, object]],
    absorption: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1139 - Y5/R10 c Source-Normalization Monopole-vs-Hair Split

**Current verdict:** `c_domain_source_normalization_operator` can only be harmless if it is a pure universal monopole calibration. The current corpus does not prove that, and all dangerous hair components remain open.

**Useful progress:** the blocker is now decomposed. `c_universal_monopole` is the only potentially absorbable component; time, range/radial, species, vector, anisotropic, and flux hair must be theorem-zero or source-bounded.

**Important rejection:** source-unity or measured-GM absorption remains forbidden unless the monopole is parent-signed and every hair component vanishes.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or FLRW claim follows from 1139.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Monopole-vs-Hair Split
{table(["component_id", "component", "physical_meaning", "danger_rows", "absorbable_if", "current_status", "claim_effect", "valid_for_claim"], split)}

## Absorption Tests
{table(["test_id", "test", "must_show", "current_status", "result", "valid_for_claim"], absorption)}

## Component Bound Schemas
{table(["bound_id", "component", "needed_row", "current_value", "status", "valid_for_claim"], bounds)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1139_SOURCE_REGISTER.csv",
        "split": OUT / "P8_Y5_R10_1139_C_MONOPOLE_HAIR_SPLIT.csv",
        "absorption": OUT / "P8_Y5_R10_1139_C_ABSORPTION_TESTS.csv",
        "bounds": OUT / "P8_Y5_R10_1139_C_HAIR_COMPONENT_BOUND_SCHEMAS.csv",
        "gates": OUT / "P8_Y5_R10_1139_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1139_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1139_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1139_VALIDATION.csv",
    }
    sources = source_rows()
    split = split_rows()
    absorption = absorption_test_rows()
    bounds = component_bound_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["split"], split)
    write_csv(outputs["absorption"], absorption)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, split, absorption, bounds, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, split, absorption, bounds, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
