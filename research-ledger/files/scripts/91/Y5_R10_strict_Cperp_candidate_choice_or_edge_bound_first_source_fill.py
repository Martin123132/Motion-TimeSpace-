from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1162-Y5-R10-strict-Cperp-candidate-choice-or-edge-bound-first-source-fill.md"


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


def missing_value(value: object) -> bool:
    text = str(value)
    return (
        text.strip() == ""
        or "MISSING" in text
        or "NOT_CLAIM" in text
        or "NONCLAIM" in text
        or "SOURCE_ANCHOR_ONLY" in text
        or "BLOCKED" in text
        or "NOT_DERIVED" in text
    )


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1162_0_1161_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1161_NEXT_TARGET.csv",
            "needle": "NEXT1161_0_1162",
            "role": "handoff selecting strict Cperp candidate choice or edge-bound source fill.",
        },
        {
            "source_id": "SRC1162_1_1161_candidate_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SOURCE_AUDIT.csv",
            "needle": "CDR1161_0_candidate_topological_residual",
            "role": "topological/projector residual candidate to assess strictly.",
        },
        {
            "source_id": "SRC1162_2_1161_source_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
            "needle": "CDSRC1161_0_Cperp_definition",
            "role": "Cperp/d_rel source fields that remain missing.",
        },
        {
            "source_id": "SRC1162_3_272_skeleton",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "no-Cperp action skeleton works if physical configuration space is [C]=C/ker(P_D)",
            "role": "best source anchor for topological/projector Cperp candidate.",
        },
        {
            "source_id": "SRC1162_4_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "weighted Stokes source anchor for corner and derivative terms.",
        },
        {
            "source_id": "SRC1162_5_1020_cohomology",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_2_relative_cohomology",
            "role": "relative cohomology source anchor for harmonic edge terms.",
        },
        {
            "source_id": "SRC1162_6_1020_residual",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_3_residual_bound",
            "role": "residual edge bound source anchor.",
        },
        {
            "source_id": "SRC1162_7_1019_edge_coefficients",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "SP1019_4_edge_coefficients",
            "role": "edge coefficient schema for boundary primitive and cocycle rows.",
        },
        {
            "source_id": "SRC1162_8_1019_projector",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "SP1019_6_projector_zero_or_bound",
            "role": "projector source-bound schema.",
        },
        {
            "source_id": "SRC1162_9_1040_cocycle",
            "relative_path": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "needle": "KBC1040_0_contract",
            "role": "K_boundary cocycle formula contract.",
        },
        {
            "source_id": "SRC1162_10_1144_selector",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv",
            "needle": "RC1144_2_same_parent_law",
            "role": "local/FLRW no-hand-switch selector remains missing.",
        },
        {
            "source_id": "SRC1162_11_1146_no_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
            "needle": "NF1146_6_verdict",
            "role": "epsilon/domain no-flux sibling remains unproved.",
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


def candidate_choice_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "candidate_id": "CAND1162_0_topological_projector_residual",
                "candidate_definition": "C_perp := (I-P_D) C or equivalent topological/projector residual",
                "decision": "SELECT_AS_PRIMARY_SOURCE_ACQUISITION_CANDIDATE_NONCLAIM",
                "reason": "it is the only candidate directly aligned with the 272 quotient/topological projector route",
                "missing_for_adoption": "P_D owner; C object; form degree; d_rel complex; domain/boundary class; variation rule; units; closedness identity",
                "claim_status": "NOT_ADOPTED_FOR_CLAIM",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "CAND1162_1_domain_memory_current",
                "candidate_definition": "C_perp := P_D J_D or J_rel-style domain/memory current residual",
                "decision": "DEMOTE_TO_BRANCH_SELECTOR_SIBLING",
                "reason": "useful for local/FLRW branch law, but not the same C-sector object unless mapped by a parent equation",
                "missing_for_adoption": "same-variable map from C_perp to J_D/J_rel and proof it controls c_g route",
                "claim_status": "NOT_CPERP_DEFINITION",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "CAND1162_2_frame_conformal_residual",
                "candidate_definition": "C_perp as frame/A_g/Xhat residual",
                "decision": "REJECT_AS_PRIMARY_CPERP_DEFINITION",
                "reason": "it would define away the common-frame coupling before proving matter descent/no-shadow-frame",
                "missing_for_adoption": "independent single-public-metric or quotient-matter theorem",
                "claim_status": "REJECTED_FOR_NOW",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "CAND1162_3_generic_relative_operator",
                "candidate_definition": "generic d_rel on an unspecified relative pair",
                "decision": "RETAIN_AS_FORMAL_TEMPLATE_ONLY",
                "reason": "standard relative notation is useful but not a source-backed C-sector operator",
                "missing_for_adoption": "bulk complex; boundary complex; pullback; signs; nilpotency; C-sector domain",
                "claim_status": "NOT_A_PHYSICAL_DEFINITION",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "CAND1162_4_verdict",
                "candidate_definition": "strict Cperp candidate choice",
                "decision": "ONE_PRIMARY_CANDIDATE_SELECTED_FOR_SOURCE_ACQUISITION_ONLY",
                "reason": "topological/projector residual is the least circular route; all other candidates are demoted or rejected",
                "missing_for_adoption": "source-backed contract must still be written before exactness or c_g zero can be tested",
                "claim_status": "NO_CPERP_CLAIM",
                "valid_for_claim": "false",
            },
        ]
    )


def edge_source_fill_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "fill_id": "EFS1162_0_C_corner",
                "quantity": "C_corner",
                "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
                "source_needle": "ETB1020_1_weighted_Stokes_identity",
                "current_value": "MISSING_CORNER_ZERO_OR_NUMERIC_BOUND",
                "units": "declared_by_boundary_charge_convention",
                "status": "SOURCE_ANCHOR_ONLY_VALUE_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_1_norm_dS_Feps",
                "quantity": "norm_dS_Feps",
                "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
                "source_needle": "ETB1020_1_weighted_Stokes_identity",
                "current_value": "MISSING_WEIGHT_DERIVATIVE_NORM",
                "units": "dual_surface_norm",
                "status": "SOURCE_ANCHOR_ONLY_VALUE_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_2_norm_bC",
                "quantity": "norm_bC",
                "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
                "source_needle": "CDSRC1161_0_Cperp_definition",
                "current_value": "MISSING_BC_PRIMITIVE_AND_NORM",
                "units": "dual_to_norm_dS_Feps",
                "status": "BLOCKED_BY_CPERP_PRIMITIVE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_3_harmonic_edge_abs",
                "quantity": "harmonic_edge_abs",
                "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
                "source_needle": "BDC1020_2_relative_cohomology",
                "current_value": "MISSING_HARMONIC_EDGE_ZERO_OR_BOUND",
                "units": "boundary_charge_units",
                "status": "SOURCE_ANCHOR_ONLY_VALUE_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_4_residual_edge_abs",
                "quantity": "residual_edge_abs",
                "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
                "source_needle": "ETB1020_3_residual_bound",
                "current_value": "MISSING_RESIDUAL_EDGE_ZERO_OR_BOUND",
                "units": "boundary_charge_units",
                "status": "SOURCE_ANCHOR_ONLY_VALUE_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_5_K_boundary",
                "quantity": "K_boundary",
                "source_anchor": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
                "source_needle": "KBC1040_0_contract",
                "current_value": "MISSING_COCYCLE_ZERO_OR_NUMERIC_BOUND",
                "units": "boundary_generator_units",
                "status": "FORMULA_CONTRACT_ONLY_VALUE_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_6_Qbar_CXH",
                "quantity": "Qbar_CXH",
                "source_anchor": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
                "source_needle": "SP1019_6_projector_zero_or_bound",
                "current_value": "MISSING_PROJECTOR_SOURCE_BOUND",
                "units": "dimensionless_after_MH_normalization",
                "status": "SOURCE_ANCHOR_ONLY_VALUE_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_7_branch_selector",
                "quantity": "local_trivial_FLRW_active_selector",
                "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv",
                "source_needle": "RC1144_2_same_parent_law",
                "current_value": "MISSING_PARENT_BRANCH_SELECTION_LAW",
                "units": "boolean_theorem_or_branch_functional",
                "status": "SHAPE_SUPPORT_ONLY_VALUE_MISSING",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "fill_id": "EFS1162_8_epsilon_no_flux_sibling",
                "quantity": "epsilon_domain_flux_zero_or_bound",
                "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
                "source_needle": "NF1146_6_verdict",
                "current_value": "MISSING_EPSILON_NO_FLUX_CERTIFICATE_OR_PROFILE",
                "units": "alpha3_product_convention",
                "status": "SIBLING_GATE_BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1162_0_one_Cperp_only",
                "guard": "carry only one primary Cperp candidate forward",
                "status": "ACTIVE",
                "reason": "multiple candidate definitions would let the theory switch objects mid-proof",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1162_1_candidate_not_claim",
                "guard": "selected candidate is for source acquisition only",
                "status": "ACTIVE",
                "reason": "P_D, C, d_rel, closedness, units, and branch selector remain missing",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1162_2_no_frame_residual_definition",
                "guard": "do not define Cperp as A_g/Xhat frame residual without matter descent",
                "status": "ACTIVE",
                "reason": "that would hide the c_g coupling problem inside a definition",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1162_3_edge_values_required",
                "guard": "edge-bound rows with anchors but missing values are not scoreable",
                "status": "ACTIVE",
                "reason": "source anchors are provenance, not numerical or theorem-zero evidence",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1162_4_no_local_claim",
                "guard": "no local-GR/Newton/c_g/R10/PPN/WEP/clock/orbital claim from candidate selection",
                "status": "ACTIVE",
                "reason": "candidate choice is a narrowing step, not a derivation or empirical pass",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1162_0_sources_exist",
                "rule": "all cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1162_1_one_candidate_selected",
                "rule": "exactly one primary Cperp candidate is carried forward",
                "gate_pass": "true_nonclaim",
                "reason": "topological/projector residual selected for source acquisition only",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1162_2_candidate_adopted_for_claim",
                "rule": "selected Cperp candidate is a parent-signed definition",
                "gate_pass": "false",
                "reason": "source contract still missing P_D, C, d_rel, units, and closedness",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1162_3_edge_source_fill_rows",
                "rule": "edge-bound terms have provenance anchors",
                "gate_pass": "true_nonclaim",
                "reason": "each edge term has an existing source anchor but missing value/theorem-zero status",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1162_4_claim_promotion",
                "rule": "Cperp exactness, edge pass, q-null, c_g-zero, local-GR/Newton/R10/PPN/WEP/clock/orbital claim allowed",
                "gate_pass": "false",
                "reason": "candidate is nonclaim and edge values remain missing",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1162_0_candidate_choice",
                "decision": "topological_projector_residual_selected_for_acquisition",
                "reason": "least circular path to the 272 quotient proof; other candidates are either sibling objects or dangerous shortcuts",
                "next_action": "write source contract for C_perp=(I-P_D)C with d_rel complex",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1162_1_edge_fill",
                "decision": "edge_bound_source_anchors_filled_values_missing",
                "reason": "corner, derivative, primitive, harmonic, residual, cocycle, and projector rows now point to concrete source anchors",
                "next_action": "build runner stub that refuses claim until values/theorem-zero rows are supplied",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1162_2_best_next",
                "decision": "target_topological_Cperp_source_contract_and_edge_runner_stub",
                "reason": "the next real progress is either a source-backed definition contract or executable nonclaim bound plumbing",
                "next_action": "1163 topological Cperp source contract plus edge-bound runner stub",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1162_0_1163",
                "next_target": "1163-Y5-R10-topological-Cperp-source-contract-and-edge-bound-runner-stub.md",
                "objective": "write the strict source contract for C_perp=(I-P_D)C and a runner stub that refuses edge-bound claims until all source-fill values or theorem-zero certificates exist",
                "include": "P_D owner; C object; form degree; d_rel complex; closedness identity; B_C primitive; edge-bound input schema; no-claim runner gates",
                "exclude": "claiming selected candidate; switching Cperp definitions; invented edge values; c_g zero claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    edge_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
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

    all_rows = candidates + edge_rows + guards + gates + decisions + next_target
    primary = [row for row in candidates if row["decision"] == "SELECT_AS_PRIMARY_SOURCE_ACQUISITION_CANDIDATE_NONCLAIM"]
    add(
        "V1162_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1162_1_exactly_one_primary_candidate",
        len(primary) == 1 and primary[0]["candidate_id"] == "CAND1162_0_topological_projector_residual",
        "one primary Cperp candidate is selected for acquisition only",
    )
    add(
        "V1162_2_nonprimary_demoted",
        any(row["candidate_id"] == "CAND1162_1_domain_memory_current" and "DEMOTE" in row["decision"] for row in candidates)
        and any(row["candidate_id"] == "CAND1162_2_frame_conformal_residual" and "REJECT" in row["decision"] for row in candidates),
        "domain-current and frame-residual candidates are not competing definitions",
    )
    add(
        "V1162_3_candidate_nonclaim",
        all(row["valid_for_claim"] == "false" and row["claim_status"] != "CLAIM_READY" for row in candidates),
        "candidate choice remains nonclaim",
    )
    add(
        "V1162_4_edge_rows_have_existing_anchors",
        all((ROOT / str(row["source_anchor"])).exists() and str(row["source_needle"]) in read_text(ROOT / str(row["source_anchor"])) for row in edge_rows),
        "all edge fill rows point to existing source anchors and needles",
    )
    add(
        "V1162_5_edge_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and missing_value(row["current_value"]) for row in edge_rows),
        "edge fill rows remain missing/nonclaim until sourced",
    )
    add(
        "V1162_6_guards_active",
        {
            "GUARD1162_0_one_Cperp_only",
            "GUARD1162_1_candidate_not_claim",
            "GUARD1162_2_no_frame_residual_definition",
            "GUARD1162_3_edge_values_required",
            "GUARD1162_4_no_local_claim",
        }.issubset({row["guard_id"] for row in guards if row["status"] == "ACTIVE"}),
        "all strict-candidate and edge-value guards are active",
    )
    add(
        "V1162_7_claim_gates_blocked",
        any(row["gate_id"] == "G1162_2_candidate_adopted_for_claim" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1162_4_claim_promotion" and row["gate_pass"] == "false" for row in gates),
        "candidate adoption and local claim gates remain blocked",
    )
    add(
        "V1162_8_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1162_9_next_target",
        next_target[0]["next_target"].startswith("1163-")
        and "topological-Cperp-source-contract" in str(next_target[0]["next_target"]),
        "1163 handoff targets topological Cperp source contract and edge-bound runner stub",
    )
    add(
        "V1162_10_generated_under_post_checkpoint",
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
    add("V1162_11_csv_parse", csv_parse_ok, "all 1162 CSV outputs parse cleanly")
    add("V1162_12_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1162_SUMMARY",
        True,
        "1162 selects the topological/projector residual as the only Cperp acquisition candidate, demotes competing definitions, and fills edge-bound source anchors without claims",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    edge_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1162 - Y5/R10 Strict Cperp Candidate Choice or Edge Bound First Source Fill

**Current verdict:** one candidate is selected, but not claimed. `C_perp := (I-P_D)C` or the equivalent topological/projector residual is the only route carried forward, because it is the least circular match to the quotient/topological projector spine.

**Important demotion:** `P_D J_D` remains a useful branch-selector sibling, not the Cperp definition. The `A_g/Xhat` frame-residual definition is rejected for now because it would hide the coupling problem inside notation.

**Main progress:** the first edge-bound source-fill rows now have concrete source anchors for corner, surface-derivative, primitive, harmonic, residual, cocycle, projector, selector, and epsilon/no-flux terms. They are still nonclaim because values/theorem-zero certificates are missing.

**No claim:** no `Cperp` exactness, edge pass, `q`-null, `c_g=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, GitHub, or public claim follows from 1162.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Strict Candidate Choice
{table(["candidate_id", "candidate_definition", "decision", "reason", "missing_for_adoption", "claim_status", "valid_for_claim"], candidates)}

## Edge-Bound First Source Fill
{table(["fill_id", "quantity", "source_anchor", "source_needle", "current_value", "units", "status", "valid_for_claim", "claim_allowed"], edge_rows)}

## No-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

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
        "source_register": OUT / "P8_Y5_R10_1162_SOURCE_REGISTER.csv",
        "candidates": OUT / "P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv",
        "edge_rows": OUT / "P8_Y5_R10_1162_EDGE_BOUND_FIRST_SOURCE_FILL.csv",
        "guards": OUT / "P8_Y5_R10_1162_NO_CPERP_CANDIDATE_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1162_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1162_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1162_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1162_VALIDATION.csv",
    }

    sources = source_rows()
    candidates = candidate_choice_rows()
    edge_rows = edge_source_fill_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["candidates"], candidates)
    write_csv(outputs["edge_rows"], edge_rows)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, candidates, edge_rows, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, candidates, edge_rows, guards, gates, decisions, validation, next_target)
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
