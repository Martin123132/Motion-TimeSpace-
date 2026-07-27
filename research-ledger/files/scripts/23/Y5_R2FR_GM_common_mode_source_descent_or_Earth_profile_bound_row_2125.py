from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2125-Y5-R2FR-GM-common-mode-source-descent-or-Earth-profile-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2124_NEXT = OUT / "P8_Y5_PARENT_QLOC_2124_NEXT_TARGET.csv"
CSV_2124_VAL = OUT / "P8_Y5_BRR545_2124_VALIDATION.csv"
CSV_2124_BOUNDS = OUT / "P8_Y5_PARENT_QLOC_2124_FIRST_BOUNDED_ROW_SCHEMA.csv"
CSV_2124_GM = OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv"
CSV_1332_THEOREM = OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv"
CSV_1337_REDUCTION = OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv"
CSV_1337_UPDATE = OUT / "P8_Y5_R10_1337_COMMON_MODE_THEOREM_UPDATE.csv"
CSV_1337_COUNTER = OUT / "P8_Y5_R10_1337_ADMISSIBLE_COUNTERMODEL_LEDGER.csv"
CSV_1425_GUARD = OUT / "P8_Y5_R10_1425_MEASURED_G_COMMON_MODE_GUARD.csv"
CSV_1425_PROOF = OUT / "P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv"
CSV_1425_PACK = OUT / "P8_Y5_R10_1425_FINITE_COEFFICIENT_PACK_CONTRACT.csv"
CSV_1083_EARTH = OUT / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv"
CSV_1083_CAVEAT = OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv"
CSV_1216_EARTH = OUT / "P8_Y5_R10_1216_EARTH_SOURCE_FACTOR_IMPORT.csv"
CSV_1901_FILL = OUT / "P8_Y5_PARENT_QLOC_1901_SOURCE_VECTOR_FILL_NONCLAIM.csv"
CSV_1901_DRYRUN = OUT / "P8_Y5_PARENT_QLOC_1901_GUARD_SOURCE_VECTOR_DRYRUN_RESULTS.csv"
CSV_1424_CONTRACT = OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv"
CSV_1419_VECTOR = OUT / "P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv"


Q_ALPHA_BULK = 1.691260686750872e-03
Q_SURFACE_BULK = -1.211918219995745e-02
Q_BULK_ABS_L1 = abs(Q_ALPHA_BULK) + abs(Q_SURFACE_BULK)


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2125_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2125-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2125*",
        "*Y5_R2FR_GM_common_mode_source_descent_or_Earth_profile_bound_row_2125*",
        "*AFRAME_GM_SOURCE_2125*",
        "*JR2125_GM_SOURCE*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2125_00_2124_next", CSV_2124_NEXT, ["NEXT2124_0_2125", "GM-common-mode-source-descent"], "2124 handoff selects GM common-mode source descent or Earth profile bound row."),
        ("SRC2125_01_2124_validation", CSV_2124_VAL, ["VAL2124_OVERALL", "PASS"], "2124 validation passed."),
        ("SRC2125_02_2124_bound_schema", CSV_2124_BOUNDS, ["FK2124_0_source_GM", "FIRST_BOUNDED_ROW_SCHEMA_ONLY"], "first source/GM bounded-row schema."),
        ("SRC2125_03_2124_gm_guard", CSV_2124_GM, ["GM2124_3_verdict", "GUARD_NORMAL_FORM_CLOSED_DATA_OPEN"], "GM guard normal form."),
        ("SRC2125_04_1332_common_theorem", CSV_1332_THEOREM, ["CMT1332_0_common_mode_source_coupling", "EXACT_CONDITIONAL_THEOREM"], "older exact conditional common-mode theorem."),
        ("SRC2125_05_1337_reduction", CSV_1337_REDUCTION, ["RED1337_3_no_source_only_species_slot", "SHARPEST_MISSING_PREMISE"], "sharp missing NoSourceOnlySpeciesSlot premise."),
        ("SRC2125_06_1337_update", CSV_1337_UPDATE, ["THM1337_0_common_mode_reduced_theorem", "EXACT_CONDITIONAL_REDUCED_PREMISES"], "reduced common-mode theorem."),
        ("SRC2125_07_1337_counter", CSV_1337_COUNTER, ["CM1337_0_relative_source_weight", "LIVE_UNLESS_NO_SOURCE_SLOT_PARENT_SIGNED"], "relative source-weight countermodel."),
        ("SRC2125_08_1425_guard", CSV_1425_GUARD, ["GCG1425_0_common_scale", "GCG1425_1_relative_residual"], "measured-G guard."),
        ("SRC2125_09_1425_proof", CSV_1425_PROOF, ["CMZ1425_5_verdict", "NOT_PROVED_DEMOTE_FINITE_WEP_TO_SOURCED_INPUT_ONLY"], "common-mode WEP proof attempt."),
        ("SRC2125_10_1425_pack", CSV_1425_PACK, ["PACK1425_2_R_source", "MISSING_SOURCE_VECTOR"], "finite source vector contract."),
        ("SRC2125_11_1083_earth", CSV_1083_EARTH, ["DD_EARTH1083_0_bulk_weighted", "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM"], "numeric bulk Earth DD vector context."),
        ("SRC2125_12_1083_caveat", CSV_1083_CAVEAT, ["SCG1083_0_profile_weighting", "MISSING_SOURCE_PROFILE_WEIGHTING"], "bulk-as-profile caveat."),
        ("SRC2125_13_1216_earth", CSV_1216_EARTH, ["RS1216_0_Earth_DD_bulk_vector", "RS1216_1_source_profile_gate"], "imported nonclaim Earth source factor."),
        ("SRC2125_14_1901_fill", CSV_1901_FILL, ["SVF1901_0_bulk_dd_context", "SVF1901_6_verdict"], "source vector fill ledger."),
        ("SRC2125_15_1901_dryrun", CSV_1901_DRYRUN, ["DRY1901_1_measured_g_hiding", "DRY1901_2_bulk_as_profile"], "guard/source-vector dryrun refusals."),
        ("SRC2125_16_1424_contract", CSV_1424_CONTRACT, ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"], "source vector/product contract."),
        ("SRC2125_17_1419_vector", CSV_1419_VECTOR, ["SRCV1419_5_verdict", "VECTOR_DECLARED_VALUES_MISSING"], "source residual vector missing."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def common_mode_descent_rows() -> list[dict[str, object]]:
    return [
        row(
            descent_id="CMD2125_0_exact_conditional",
            clause="common-mode source descent theorem",
            statement="If ordinary matter is one descended observed matter action with one source measure/scale and no source-only species slot, then all ordinary Hilbert source components enter one calibrated current.",
            source_anchor="CMT1332_0; THM1337_0; CMZ1425_0",
            current_status="EXACT_CONDITIONAL_THEOREM_RESTATED",
            parent_signed=False,
            consequence="relative source-feedback residuals vanish only under the missing parent clause",
        ),
        row(
            descent_id="CMD2125_1_minimal_missing_clause",
            clause="NoSourceOnlySpeciesSlot",
            statement="The parent object language must not admit a morphism from species/material label to active gravitational source coefficient w_A independent of nongravitational constants.",
            source_anchor="RED1337_3_no_source_only_species_slot; THM1337_1_no_source_slot_is_minimal",
            current_status="SHARPEST_MISSING_PREMISE",
            parent_signed=False,
            consequence="this is now the single clean theorem target for source-side local GR",
        ),
        row(
            descent_id="CMD2125_2_countermodel",
            clause="relative source weight survives without the missing clause",
            statement="S_m=sum_A(1+epsilon_A)S_A is covariant/additive and preserves quotient descent if epsilon_A is declared observed constant, but it generates material/source residuals.",
            source_anchor="CM1337_0_relative_source_weight; CMT1332_2_countermodel",
            current_status="LIVE_COUNTERMODEL",
            parent_signed=False,
            consequence="common-mode theorem cannot be promoted by taste or calibration",
        ),
        row(
            descent_id="CMD2125_3_measured_G_guard",
            clause="common mode can be calibrated once",
            statement="A universal scale multiplying total T_matter can be absorbed into measured G_N/GM, but relative residuals cannot be hidden by fitted G.",
            source_anchor="GCG1425_0_common_scale; GCG1425_1_relative_residual; GM2124_3_verdict",
            current_status="GUARD_ACTIVE",
            parent_signed=False,
            consequence="blocks fake local-GR pass through fitted-G absorption",
        ),
        row(
            descent_id="CMD2125_4_verdict",
            clause="GM/source descent verdict",
            statement="The source-side GR route is reduced to proving NoSourceOnlySpeciesSlot plus existing descent/current clauses, or else sourcing a finite non-common source vector.",
            source_anchor="1337 plus 1425 plus 2124",
            current_status="THEOREM_TARGET_SHARPENED_NOT_CLOSED",
            parent_signed=False,
            consequence="move next to parent object-language proof or explicit closure",
        ),
    ]


def earth_profile_bound_rows() -> list[dict[str, object]]:
    return [
        row(
            row_id="EPB2125_0_bulk_DD_context",
            object="bulk Earth DD source vector",
            Q_alpha_Coulomb_Earth=Q_ALPHA_BULK,
            Q_surface_binding_Earth=Q_SURFACE_BULK,
            Q_bulk_abs_L1=Q_BULK_ABS_L1,
            current_status="NUMERIC_BULK_CONTEXT_NONCLAIM_NOT_PROFILE",
            claim_blocker="bulk Earth vector is not shell/profile/worldtube weighted and parent-to-DD/readout maps remain missing",
            source_anchor="DD_EARTH1083_0_bulk_weighted; RS1216_0_Earth_DD_bulk_vector",
            score_ready=False,
        ),
        row(
            row_id="EPB2125_1_profile_weighted_target",
            object="profile/worldtube-weighted Earth source vector",
            Q_alpha_Coulomb_Earth="MISSING_PROFILE_WEIGHTED_VALUE",
            Q_surface_binding_Earth="MISSING_PROFILE_WEIGHTED_VALUE",
            Q_bulk_abs_L1="not_applicable",
            current_status="MISSING_PROFILE_WEIGHTING_FOR_CLAIM",
            claim_blocker="MICROSCOPE/orbit shell weighting and support convention not supplied",
            source_anchor="SCG1083_0_profile_weighting; RS1216_1_source_profile_gate",
            score_ready=False,
        ),
        row(
            row_id="EPB2125_2_parent_basis_map",
            object="MTS parent residual vector to DD/source basis",
            Q_alpha_Coulomb_Earth="MISSING_PARENT_OPERATOR_BASIS_MAP",
            Q_surface_binding_Earth="MISSING_PARENT_OPERATOR_BASIS_MAP",
            Q_bulk_abs_L1="not_applicable",
            current_status="MISSING_PARENT_BASIS_MAP",
            claim_blocker="DD basis remains external comparator unless parent operator map is supplied",
            source_anchor="SCG1083_1_parent_to_DD_map; SRCMAP1424_2_C_parent",
            score_ready=False,
        ),
        row(
            row_id="EPB2125_3_first_bound_formula",
            object="first source/GM non-common residual bound",
            Q_alpha_Coulomb_Earth="symbolic",
            Q_surface_binding_Earth="symbolic",
            Q_bulk_abs_L1="symbolic",
            current_status="BOUND_FORMULA_READY_VALUES_MISSING",
            claim_blocker="needs profile vector, material/readout response, parent coefficients and common units",
            source_anchor="FK2124_0_source_GM; PACK1425_2_R_source; SRCV1419_5_verdict",
            score_ready=False,
        ),
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        row(refusal_id="REF2125_0_guard_as_zero", attempted_shortcut="using measured-G guard as source zero theorem", result="REFUSED", reason="guard separates common and relative components but does not prove the relative component is zero", source_anchor="DRY1901_0_use_guard_as_zero"),
        row(refusal_id="REF2125_1_measured_G_hiding", attempted_shortcut="absorbing relative source weights into fitted G/GM", result="REFUSED", reason="only one universal common-mode factor can be calibrated away", source_anchor="DRY1901_1_measured_g_hiding; GCG1425_1_relative_residual"),
        row(refusal_id="REF2125_2_bulk_as_profile", attempted_shortcut="using bulk Earth DD vector as MICROSCOPE profile/worldtube vector", result="REFUSED", reason="bulk composition is not orbit/profile/shell weighted", source_anchor="DRY1901_2_bulk_as_profile; SCG1083_0_profile_weighting"),
        row(refusal_id="REF2125_3_countermodel_ignored", attempted_shortcut="ignoring relative source-weight countermodel", result="REFUSED", reason="relative source weights remain live unless NoSourceOnlySpeciesSlot is parent-signed", source_anchor="CM1337_0_relative_source_weight"),
    ]


def promotion_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2125_0_common_mode_theorem_exact", gate="common-mode theorem exact conditional", gate_pass=True, rationale="1332/1337 theorem route is valid as a conditional theorem"),
        row(gate_id="GATE2125_1_no_source_slot_parent_signed", gate="NoSourceOnlySpeciesSlot parent signed", gate_pass=False, rationale="still a missing parent object-language clause"),
        row(gate_id="GATE2125_2_bulk_vector_numeric_context", gate="bulk Earth DD vector numeric nonclaim", gate_pass=True, rationale=f"Q_alpha={Q_ALPHA_BULK:.16e}; Q_surface={Q_SURFACE_BULK:.16e}"),
        row(gate_id="GATE2125_3_profile_vector_claim_grade", gate="profile/worldtube source vector claim-grade", gate_pass=False, rationale="bulk vector cannot be promoted to profile-weighted source vector"),
        row(gate_id="GATE2125_4_parent_basis_and_readout", gate="parent basis/material/readout product complete", gate_pass=False, rationale="parent basis map, material tensor, C_parent and readout kernel are missing"),
        row(gate_id="GATE2125_5_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="source-side theorem is conditional and finite source row is not executable"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2125_0", decision="COMMON_MODE_ROUTE_SHARPENED", because="source-side zero is reduced to NoSourceOnlySpeciesSlot plus already-named descent/current clauses", next_action="try parent object-language proof next"),
        row(decision_id="DEC2125_1", decision="EARTH_BULK_VECTOR_REUSED_ONLY_AS_CONTEXT", because="numeric bulk DD vector exists but is not profile/worldtube weighted", next_action="do not use it as WEP/R10/PPN prediction"),
        row(decision_id="DEC2125_2", decision="FINITE_BOUND_ROUTE_STAGED", because="first bound formula can use profile residual once sourced, but required profile/basis/readout inputs are missing", next_action="prepare source-profile acquisition only if object-language proof fails"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2125_0_2126",
            next_target="2126-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-proof-or-profile-acquisition-pack.md",
            script="scripts/Y5_R2FR_NoSourceOnlySpeciesSlot_parent_proof_or_profile_acquisition_pack_2126.py",
            objective="Attempt the cleanest theorem route: prove the parent object language forbids source-only species coefficients. If it fails, make that an explicit closure clause and prepare the source-profile acquisition pack without treating bulk Earth data as a prediction.",
            forbidden_shortcuts="declaring NoSourceOnlySpeciesSlot by preference; fitted-G absorption of relative weights; bulk Earth as profile-weighted source; ignoring relative countermodels; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    descent: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    refusals: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2125_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_GM_SOURCE_DESCENT_2125_NONCLAIM.csv", descent + profile_rows + refusals),
        ("COPY2125_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2125_GM_SOURCE_DESCENT_STATUS_NONCLAIM.csv", descent + profile_rows + refusals),
        ("COPY2125_2_acquisition_queue", QUEUE / "JR2125_NOSOURCE_SLOT_OR_PROFILE_PACK_QUEUE.csv", next_rows + profile_rows),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    descent: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    refusals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    descent_ok = any(item["descent_id"] == "CMD2125_1_minimal_missing_clause" and item["current_status"] == "SHARPEST_MISSING_PREMISE" for item in descent) and any(item["descent_id"] == "CMD2125_2_countermodel" and item["current_status"] == "LIVE_COUNTERMODEL" for item in descent)
    profile_ok = any(item["row_id"] == "EPB2125_0_bulk_DD_context" and item["current_status"] == "NUMERIC_BULK_CONTEXT_NONCLAIM_NOT_PROFILE" for item in profile_rows) and any(item["row_id"] == "EPB2125_1_profile_weighted_target" and item["current_status"] == "MISSING_PROFILE_WEIGHTING_FOR_CLAIM" for item in profile_rows)
    refusals_ok = all(item["result"] == "REFUSED" for item in refusals) and len(refusals) >= 4
    gates_ok = any(item["gate_id"] == "GATE2125_0_common_mode_theorem_exact" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2125_5_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2125_0" and item["decision"] == "COMMON_MODE_ROUTE_SHARPENED" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2125_0_2126" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, descent, profile_rows, refusals, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2125_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, descent_ok, profile_ok, refusals_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2125_00_sources", sources_ok, "all cited common-mode/source-vector rows exist and contain expected needles"),
        ("VAL2125_01_descent", descent_ok, "common-mode route reduced to NoSourceOnlySpeciesSlot while countermodel remains live"),
        ("VAL2125_02_profile_rows", profile_ok, "bulk Earth numeric context is separated from missing profile/worldtube vector"),
        ("VAL2125_03_refusals", refusals_ok, "guard-as-zero, measured-G hiding, bulk-as-profile and countermodel-ignoring shortcuts are refused"),
        ("VAL2125_04_gates", gates_ok, "conditional theorem gate passes while local claim gate fails"),
        ("VAL2125_05_decisions", decisions_ok, "decision ledger sharpens common-mode route"),
        ("VAL2125_06_next", next_ok, "next target is NoSourceOnlySpeciesSlot proof or profile acquisition pack"),
        ("VAL2125_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2125_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2125_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2125_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2125"),
        ("VAL2125_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2125_OVERALL", all_ok, "2125 sharpens the source/GM common-mode route to NoSourceOnlySpeciesSlot and keeps bulk Earth/source-profile rows nonclaim."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    descent: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    refusals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2125 - Y5/R2FR GM Common-Mode Source Descent Or Earth Profile Bound Row",
            "## Current Verdict",
            "2125 sharpens the source side of the local-GR bridge. The common-mode theorem is exact as a conditional theorem: if the parent object language allows only one descended matter source current and forbids source-only species coefficients, relative source weights collapse into one calibrated common mode. That is the clean route.",
            "The missing clause now has a precise name: `NoSourceOnlySpeciesSlot`. Without it, the countermodel `S_m=sum_A(1+epsilon_A)S_A` remains legal enough to generate WEP/source residuals. Fitted `G` or `GM` cannot hide that relative branch; calibration removes only one universal scale.",
            f"The corpus does contain numeric bulk Earth DD context (`Q_alpha={Q_ALPHA_BULK:.16e}`, `Q_surface={Q_SURFACE_BULK:.16e}`), but 2125 keeps it nonclaim because bulk Earth composition is not the MICROSCOPE/orbit profile-weighted source vector. This is disciplined progress: theorem target sharpened, fallback data row staged, no fake pass.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Common-Mode Descent Audit",
            md_table(descent, ["descent_id", "clause", "statement", "current_status", "parent_signed", "consequence", "valid_for_claim"]),
            "## Earth/Profile Bound Row",
            md_table(profile_rows, ["row_id", "object", "Q_alpha_Coulomb_Earth", "Q_surface_binding_Earth", "Q_bulk_abs_L1", "current_status", "claim_blocker", "score_ready", "valid_for_claim"]),
            "## Shortcut Refusals",
            md_table(refusals, ["refusal_id", "attempted_shortcut", "result", "reason", "source_anchor", "valid_for_claim"]),
            "## Promotion Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    descent = common_mode_descent_rows()
    profile_rows = earth_profile_bound_rows()
    refusals = refusal_rows()
    gates = promotion_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2125_SOURCE_REGISTER.csv",
        "descent": OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv",
        "profile": OUT / "P8_Y5_PARENT_QLOC_2125_EARTH_PROFILE_BOUND_ROW.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2125_SOURCE_VECTOR_PROMOTION_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2125_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2125_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2125_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2125_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["descent"], descent)
    write_csv(paths["profile"], profile_rows)
    write_csv(paths["refusals"], refusals)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(descent, profile_rows, refusals, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, descent, profile_rows, refusals, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, descent, profile_rows, refusals, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
