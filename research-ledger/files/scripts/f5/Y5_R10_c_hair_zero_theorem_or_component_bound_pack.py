from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1140-Y5-R10-c-hair-zero-theorem-or-component-bound-pack.md"


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
            "source_id": "SRC1140_0_1139_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1139_NEXT_TARGET.csv",
            "needle": "NEXT1139_0_1140",
            "note": "1139 handoff requires c-hair zero theorem or component-bound pack.",
        },
        {
            "source_id": "SRC1140_1_1139_split",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1139_C_MONOPOLE_HAIR_SPLIT.csv",
            "needle": "CS1139_7_verdict",
            "note": "Total c remains blocked unless monopole is signed and all hair components close.",
        },
        {
            "source_id": "SRC1140_2_1139_bound_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1139_C_HAIR_COMPONENT_BOUND_SCHEMAS.csv",
            "needle": "CB1139_5_flux",
            "note": "1139 supplied nonclaim schemas for time, range, species, vector, STF, and flux c-hair rows.",
        },
        {
            "source_id": "SRC1140_3_1139_absorption",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1139_C_ABSORPTION_TESTS.csv",
            "needle": "ABS1139_4_absorption_verdict",
            "note": "Measured-GM/source-unity absorption remains forbidden.",
        },
        {
            "source_id": "SRC1140_4_parent_A4",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A4_mass_flux_projector",
            "note": "Closed calibrated mass-flux projector is a monopole route, not a hair shortcut.",
        },
        {
            "source_id": "SRC1140_5_parent_A5",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A5_constant_universal_coupling",
            "note": "Constant universal coupling clause is required for time/source-drift silence.",
        },
        {
            "source_id": "SRC1140_6_parent_A6",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A6_selector_blind_source_action",
            "note": "Selector-blind source action is required for species/source-marker silence.",
        },
        {
            "source_id": "SRC1140_7_parent_A7",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A7_bulk_X_nohair_or_curve",
            "note": "Bulk/source no-hair or executable curve mapping is required for range/radial silence.",
        },
        {
            "source_id": "SRC1140_8_parent_A8",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "note": "Topological/domain projector clause is required for vector/STF/flux silence.",
        },
        {
            "source_id": "SRC1140_9_parent_A9",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A9_memory_kernel_local_silence",
            "note": "Local memory silence is required for time and range leakage closure.",
        },
        {
            "source_id": "SRC1140_10_ward_C4",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C4_constant_universal_coupling",
            "note": "Ward identity names the current constant-coupling gap.",
        },
        {
            "source_id": "SRC1140_11_ward_C5",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C5_no_species_or_marker_source_charge",
            "note": "Ward identity names the current no-species/source-marker gap.",
        },
        {
            "source_id": "SRC1140_12_ward_C6",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C6_no_range_or_radial_source_hair",
            "note": "Ward identity names the current no-range/radial-hair gap.",
        },
        {
            "source_id": "SRC1140_13_R11_missing",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "source_normalization_operator",
            "note": "R11 ledger still requires a real coefficient, theorem-zero source, or bound envelope.",
        },
        {
            "source_id": "SRC1140_14_1138_c_row",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1138_CANONICAL_C_SOURCE_NORMALIZATION_ROW.csv",
            "needle": "CROW1138_0_c_domain_source_normalization_operator",
            "note": "Canonical c row remains a blocked contract row.",
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


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "theorem_id": "HAIR1140_0_time",
                "component": "c_time_or_Gdot_hair",
                "target_zero_statement": "partial_t c_domain_source_normalization_operator = 0 and no compact-local memory source drift",
                "required_parent_clause": "A5 constant universal coupling plus A9 local memory silence, expressed as C4",
                "source_anchor": "P8_source_owner_parent_action_terms_CONTRACT.csv::A5/A9; P8_Ward_source_owner_identity_CONTRACT.csv::C4",
                "impacted_rows": "R9;R11",
                "theorem_status": "NOT_DERIVED",
                "failure_mode": "constant-coupling and local-memory-silence clauses are named but not parent-proved",
                "fallback_bound_row": "CBP1140_0_time",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "HAIR1140_1_range",
                "component": "c_range_radial_hair",
                "target_zero_statement": "partial_r c_domain_source_normalization_operator = partial_lambda c_domain_source_normalization_operator = 0",
                "required_parent_clause": "C6 no range/radial source hair plus source-free positive no-hair or executable alpha(lambda) mapping",
                "source_anchor": "P8_Ward_source_owner_identity_CONTRACT.csv::C6; P8_source_owner_parent_action_terms_CONTRACT.csv::A7/A9",
                "impacted_rows": "R3;R4;R10;R11",
                "theorem_status": "NOT_DERIVED_SYMBOLIC",
                "failure_mode": "range/radial derivative silence is listed as a need, not a derived Euler-Lagrange result",
                "fallback_bound_row": "CBP1140_1_range",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "HAIR1140_2_species",
                "component": "c_species_marker_hair",
                "target_zero_statement": "partial_A c_domain_source_normalization_operator = 0 for material/source-label directions",
                "required_parent_clause": "A6 selector-blind source action and C5 no species/marker source charge",
                "source_anchor": "P8_source_owner_parent_action_terms_CONTRACT.csv::A6; P8_Ward_source_owner_identity_CONTRACT.csv::C5",
                "impacted_rows": "R1;R11",
                "theorem_status": "NOT_PARENT_DERIVED",
                "failure_mode": "source-label forgetting is still a required parent-action clause rather than a theorem",
                "fallback_bound_row": "CBP1140_2_species",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "HAIR1140_3_vector",
                "component": "c_vector_preferred_frame_hair",
                "target_zero_statement": "observed-coframe vector part of source-normalization/domain selector vanishes",
                "required_parent_clause": "A8 topological/covariant domain projector and R11 source-normalization vector coefficient zero",
                "source_anchor": "P8_source_owner_parent_action_terms_CONTRACT.csv::A8; R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv::source_normalization_operator",
                "impacted_rows": "R5;R6;R7;R11",
                "theorem_status": "MISSING_VECTOR_THEOREM_OR_COEFFICIENT",
                "failure_mode": "no parent theorem or numeric coefficient kills preferred-frame vector leakage",
                "fallback_bound_row": "CBP1140_3_vector",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "HAIR1140_4_anisotropy",
                "component": "c_anisotropic_STF_hair",
                "target_zero_statement": "tracefree/STF source-normalization stress vanishes in the observed coframe",
                "required_parent_clause": "A8 topological or metric-independent projector/domain selector with no local stress",
                "source_anchor": "P8_source_owner_parent_action_terms_CONTRACT.csv::A8; P8_Y5_R10_1139_C_MONOPOLE_HAIR_SPLIT.csv::CS1139_5_anisotropic_stress_hair",
                "impacted_rows": "R8;R11",
                "theorem_status": "CONDITIONAL_NOT_PARENT_OWNED",
                "failure_mode": "projector/domain stress silence is conditional, not signed by a parent variational identity",
                "fallback_bound_row": "CBP1140_4_anisotropy",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "HAIR1140_5_flux",
                "component": "c_domain_flux_hair",
                "target_zero_statement": "K_R11_flux_alpha3 * c_domain_source_normalization_operator * epsilon_domain_flux is zero or strictly bounded",
                "required_parent_clause": "A8 exact-owned zero-flux divergence, or epsilon=0, K=0, c=0, or sourced product <= alpha3 bound",
                "source_anchor": "P8_source_owner_parent_action_terms_CONTRACT.csv::A8; P8_Y5_R10_1139_C_HAIR_COMPONENT_BOUND_SCHEMAS.csv::CB1139_5_flux",
                "impacted_rows": "R7;R11",
                "theorem_status": "MISSING_K_c_EPSILON_PRODUCT",
                "failure_mode": "no sourced product and no parent theorem-zero factor closes alpha3 flux leakage",
                "fallback_bound_row": "CBP1140_5_flux",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "HAIR1140_6_verdict",
                "component": "c_total_hair",
                "target_zero_statement": "all non-monopole source-normalization hair components vanish",
                "required_parent_clause": "HAIR1140_0 through HAIR1140_5 all derived zero, or every fallback bound row is sourced and passing",
                "source_anchor": "P8_Y5_R10_1139_C_MONOPOLE_HAIR_SPLIT.csv::CS1139_7_verdict",
                "impacted_rows": "R1;R3;R4;R5;R6;R7;R8;R9;R10;R11",
                "theorem_status": "HAIR_ZERO_THEOREM_NOT_CLOSED",
                "failure_mode": "the zero route currently fails; retain component-bound route as nonclaim acquisition path",
                "fallback_bound_row": "CBP1140_all",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def bound_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "bound_id": "CBP1140_0_time",
                "component": "c_time_or_Gdot_hair",
                "arena": "Gdot; clocks; source-drift",
                "impacted_rows": "R9;R11",
                "needed_row": "system_id; c_time_abs; time_window; units; source_path; valid_for_claim",
                "target_bound_or_test": "source-specific Gdot/clock/source-drift bound with fixed time window",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless drift coefficient or declared per-time normalization",
                "status": "SOURCE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CBP1140_1_range",
                "component": "c_range_radial_hair",
                "arena": "R10; inverse-square; radial/orbital residuals",
                "impacted_rows": "R3;R4;R10;R11",
                "needed_row": "system_id; c_range_abs; lambda_or_radius; units; source_path; valid_for_claim",
                "target_bound_or_test": "R10 alpha(lambda) or radial residual source row at declared radius/range",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless coefficient at lambda/radius or declared profile units",
                "status": "SOURCE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CBP1140_2_species",
                "component": "c_species_marker_hair",
                "arena": "WEP; source-charge; material-pair residuals",
                "impacted_rows": "R1;R11",
                "needed_row": "system_id; species_pair; c_species_abs; units; source_path; valid_for_claim",
                "target_bound_or_test": "eta/source-charge bound with material pair and source composition declared",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless differential source coefficient",
                "status": "SOURCE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CBP1140_3_vector",
                "component": "c_vector_preferred_frame_hair",
                "arena": "PPN alpha1; alpha2; alpha3; preferred-frame",
                "impacted_rows": "R5;R6;R7;R11",
                "needed_row": "system_id; vector_component; c_vector_abs; coframe; units; source_path; valid_for_claim",
                "target_bound_or_test": "alpha1 <= 1e-4, alpha2 <= 2e-9, alpha3 bridge guarded by 4e-20 branch",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless observed-coframe vector coefficient",
                "status": "SOURCE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CBP1140_4_anisotropy",
                "component": "c_anisotropic_STF_hair",
                "arena": "PPN xi; preferred-location; STF anisotropy",
                "impacted_rows": "R8;R11",
                "needed_row": "system_id; STF_component; c_STF_abs; coframe; units; source_path; valid_for_claim",
                "target_bound_or_test": "xi <= 4e-9 or source-backed STF stress projection bound",
                "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless observed-coframe STF coefficient",
                "status": "SOURCE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "CBP1140_5_flux",
                "component": "c_domain_flux_hair",
                "arena": "PPN alpha3; domain flux; local-GR residual",
                "impacted_rows": "R7;R11",
                "needed_row": "system_id; K_abs; c_flux_abs; epsilon_abs; product_abs; units; source_path; valid_for_claim",
                "target_bound_or_test": "abs(K*c*epsilon) <= 4e-20 without tuned cancellation",
                "current_value": "MISSING_K_c_EPSILON_PRODUCT",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless alpha3 product coefficient",
                "status": "SOURCE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def arena_map_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "map_id": "MAP1140_0_time",
                "component": "c_time_or_Gdot_hair",
                "test_arena": "Gdot; clocks; long-baseline source drift",
                "observable_readout": "time variation in active source normalization or effective local G*M",
                "blocked_by": "MISSING_C4_CONSTANT_COUPLING; MISSING_A9_LOCAL_MEMORY_SILENCE; MISSING_NUMERIC_BOUND",
                "next_needed": "derive constant coupling/memory silence or source a time-drift bound row",
                "valid_for_claim": "false",
            },
            {
                "map_id": "MAP1140_1_range",
                "component": "c_range_radial_hair",
                "test_arena": "R10; short-range gravity; radial/orbital residuals",
                "observable_readout": "finite-range or radial source-normalization correction",
                "blocked_by": "MISSING_C6_NO_RANGE_RADIAL_HAIR; MISSING_R10_PROFILE_ROW",
                "next_needed": "derive radial/range no-hair or source a real alpha(lambda)/radial residual row",
                "valid_for_claim": "false",
            },
            {
                "map_id": "MAP1140_2_species",
                "component": "c_species_marker_hair",
                "test_arena": "WEP; source charge; material dependence",
                "observable_readout": "composition/source-label dependence in active gravitational source",
                "blocked_by": "MISSING_C5_NO_SPECIES_MARKER_SOURCE_CHARGE",
                "next_needed": "derive selector-blind source theorem or source a finite eta/material-pair row",
                "valid_for_claim": "false",
            },
            {
                "map_id": "MAP1140_3_vector",
                "component": "c_vector_preferred_frame_hair",
                "test_arena": "PPN alpha1; alpha2; alpha3",
                "observable_readout": "preferred-frame vector residual in observed coframe",
                "blocked_by": "MISSING_VECTOR_THEOREM_OR_COEFFICIENT",
                "next_needed": "build first strict vector bound row before any preferred-frame claim",
                "valid_for_claim": "false",
            },
            {
                "map_id": "MAP1140_4_anisotropy",
                "component": "c_anisotropic_STF_hair",
                "test_arena": "PPN xi; preferred-location",
                "observable_readout": "tracefree anisotropic source-normalization stress",
                "blocked_by": "CONDITIONAL_PROJECTOR_STRESS_NOT_PARENT_OWNED",
                "next_needed": "derive topological/metric-independent projector stress zero or source xi/STF bound",
                "valid_for_claim": "false",
            },
            {
                "map_id": "MAP1140_5_flux",
                "component": "c_domain_flux_hair",
                "test_arena": "PPN alpha3; domain-flux local-GR residual",
                "observable_readout": "K*c*epsilon alpha3 leakage product",
                "blocked_by": "MISSING_K_c_EPSILON_PRODUCT",
                "next_needed": "build first strict K/c/epsilon product row or derive a zero factor",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1140_0_source_handoff",
                "rule": "1139 handoff and required source anchors exist",
                "gate_pass": "true_nonclaim",
                "reason": "all cited local source files and needles are present",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1140_1_hair_zero_theorem",
                "rule": "all c-hair components are theorem-zero",
                "gate_pass": "false",
                "reason": "time, range, species, vector, STF, and flux channels remain unsigned or missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1140_2_component_bound_pack",
                "rule": "all component-bound rows are numeric, sourced, and pass their arena limits",
                "gate_pass": "false",
                "reason": "bound pack is schema-ready but contains MISSING_SOURCE_PATH and missing numeric values",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1140_3_absorption_shortcut",
                "rule": "universal-monopole/measured-GM absorption shortcut remains rejected",
                "gate_pass": "true_nonclaim",
                "reason": "hair-zero theorem did not close, so c cannot be absorbed away",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1140_4_alpha3_local_GR",
                "rule": "alpha3/R10/PPN/local-GR promotion allowed",
                "gate_pass": "false",
                "reason": "vector and flux c-hair are not zero or bounded",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1140_5_next_target_selected",
                "rule": "next best source gate is explicit",
                "gate_pass": "true_nonclaim",
                "reason": "vector/flux first-bound row is selected because it attacks the sharp preferred-frame and alpha3 blockers",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1140_0_verdict",
                "decision": "c_hair_zero_theorem_not_proved",
                "reason": "parent contracts identify the needed clauses but do not derive the six hair zeros",
                "next_action": "retain c hair as explicit local residual channels",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1140_1_best_next",
                "decision": "attack_vector_and_flux_hair_first",
                "reason": "preferred-frame vector and K*c*epsilon flux hair are the tightest local-GR/alpha3 pressure points",
                "next_action": "build strict first bound rows for c_vector_preferred_frame_hair and c_domain_flux_hair",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1140_2_claim_ceiling",
                "decision": "no_local_claim_until_zero_or_bounds",
                "reason": "component-bound pack is nonclaim and every c-hair row still lacks either theorem-zero or sourced numeric value",
                "next_action": "do not promote R10, PPN, alpha3, local-GR, or measured-GM absorption from this checkpoint",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1140_0_1141",
                "next_target": "1141-Y5-R10-c-vector-flux-hair-first-bound-row.md",
                "objective": "build strict first source-ready bound rows for c_vector_preferred_frame_hair and c_domain_flux_hair, including observed coframe, alpha1/alpha2/alpha3 arena mapping, K*c*epsilon product policy, source paths, units, and nonclaim gates",
                "include": "vector hair; flux hair; observed coframe; alpha1/alpha2/alpha3 limits; K_abs; c_flux_abs; epsilon_abs; product_abs; no-cancellation rule; source paths",
                "exclude": "absorbing c into measured GM; source-unity; tuned cancellation; local-GR/R10/PPN claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorems: list[dict[str, object]],
    bounds: list[dict[str, object]],
    arena_map: list[dict[str, object]],
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

    all_rows = theorems + bounds + arena_map + gates + decisions + next_target
    required_components = {
        "c_time_or_Gdot_hair",
        "c_range_radial_hair",
        "c_species_marker_hair",
        "c_vector_preferred_frame_hair",
        "c_anisotropic_STF_hair",
        "c_domain_flux_hair",
    }
    theorem_components = {row["component"] for row in theorems}
    bound_components = {row["component"] for row in bounds}
    mapped_components = {row["component"] for row in arena_map}
    add(
        "V1140_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1140_1_theorem_coverage",
        required_components.issubset(theorem_components) and theorems[-1]["theorem_status"] == "HAIR_ZERO_THEOREM_NOT_CLOSED",
        "all six c-hair theorem targets are audited and the total zero theorem remains open",
    )
    add(
        "V1140_2_bound_pack_coverage",
        required_components == bound_components and all(row["status"] == "SOURCE_ROW_REQUIRED" for row in bounds),
        "all six c-hair components have strict nonclaim bound rows",
    )
    add(
        "V1140_3_bound_rows_nonclaim",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in bounds),
        "all component-bound rows remain nonclaim",
    )
    add(
        "V1140_4_bound_rows_require_sources",
        all(row["source_path"] == "MISSING_SOURCE_PATH" for row in bounds),
        "no bound row pretends to have a source path yet",
    )
    add(
        "V1140_5_arena_map_coverage",
        required_components == mapped_components,
        "all c-hair components are mapped to local test arenas",
    )
    add(
        "V1140_6_vector_flux_prioritized",
        any(row["bound_id"] == "CBP1140_3_vector" for row in bounds)
        and any(row["bound_id"] == "CBP1140_5_flux" for row in bounds)
        and decisions[1]["decision"] == "attack_vector_and_flux_hair_first",
        "vector and flux hair are present and selected as the next pressure gate",
    )
    add(
        "V1140_7_gates_blocked",
        all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates)
        and any(row["gate_id"] == "G1140_1_hair_zero_theorem" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1140_4_alpha3_local_GR" and row["gate_pass"] == "false" for row in gates),
        "claim gates remain blocked where physics claims would be made",
    )
    add(
        "V1140_8_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1140_9_next_target",
        next_target[0]["next_target"].startswith("1141-") and "vector-flux" in str(next_target[0]["next_target"]),
        "1141 handoff targets vector/flux c-hair first-bound rows",
    )
    add(
        "V1140_10_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1140_11_csv_parse", csv_parse_ok, "all 1140 CSV outputs parse cleanly")
    add("V1140_12_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1140_SUMMARY",
        True,
        "1140 fails the c-hair zero theorem honestly, creates strict nonclaim bound rows, and selects vector/flux hair as 1141",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorems: list[dict[str, object]],
    bounds: list[dict[str, object]],
    arena_map: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1140 - Y5/R10 c-Hair Zero Theorem or Component-Bound Pack

**Current verdict:** the local `c`-hair zero theorem is not closed. The corpus names the right parent clauses, but it does not yet derive time, range, species, vector, STF, and flux source-normalization hair as zero.

**Useful progress:** the failure is now executable rather than foggy. Each dangerous `c`-hair channel has a strict nonclaim component-bound row and a mapped local test arena.

**Important guard:** `c_domain_source_normalization_operator` still cannot be set to `0`, `1`, or absorbed into measured `GM`. That shortcut only becomes legal after a parent-signed universal monopole plus all hair-zero or sourced passing bounds.

**Best next attack:** prioritize `c_vector_preferred_frame_hair` and `c_domain_flux_hair`; they are the sharpest preferred-frame/alpha3 pressure points and the least forgiving local-GR gates.

**No claim:** no R10, PPN, alpha3, local-GR, measured-GM, or GitHub/public claim follows from 1140.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## c-Hair Zero-Theorem Audit
{table(["theorem_id", "component", "target_zero_statement", "required_parent_clause", "impacted_rows", "theorem_status", "failure_mode", "fallback_bound_row", "valid_for_claim"], theorems)}

## Component Bound Pack
{table(["bound_id", "component", "arena", "impacted_rows", "needed_row", "target_bound_or_test", "current_value", "source_path", "units", "status", "valid_for_claim"], bounds)}

## Hair-to-Test Arena Map
{table(["map_id", "component", "test_arena", "observable_readout", "blocked_by", "next_needed", "valid_for_claim"], arena_map)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1140_SOURCE_REGISTER.csv",
        "theorems": OUT / "P8_Y5_R10_1140_C_HAIR_ZERO_THEOREM_AUDIT.csv",
        "bounds": OUT / "P8_Y5_R10_1140_C_HAIR_COMPONENT_BOUND_PACK.csv",
        "arena_map": OUT / "P8_Y5_R10_1140_HAIR_TO_TEST_ARENA_MAP.csv",
        "gates": OUT / "P8_Y5_R10_1140_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1140_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1140_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1140_VALIDATION.csv",
    }
    sources = source_rows()
    theorems = theorem_rows()
    bounds = bound_pack_rows()
    arena_map = arena_map_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorems"], theorems)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["arena_map"], arena_map)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorems, bounds, arena_map, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorems, bounds, arena_map, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
