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


DOC = ROOT / "2149-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2148": ROOT / "2148-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md",
    "1828": ROOT / "1828-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md",
    "1829": ROOT / "1829-Y5-R2FR-metric-only-connection-theorem-or-P4-hinge-source-pack.md",
    "1830": ROOT / "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md",
    "1831": ROOT / "1831-Y5-R2FR-parent-field-inventory-certificate-or-first-P4-numeric-row.md",
    "1832": ROOT / "1832-Y5-R2FR-torsion-nonmetricity-zero-theorem-or-first-coefficient-source-row.md",
    "1833": ROOT / "1833-Y5-R2FR-distortion-equation-owner-or-hypermomentum-source-row.md",
    "1834": ROOT / "1834-Y5-R2FR-no-hypermomentum-matter-functor-or-DeltaGamma-bound-row.md",
    "1835": ROOT / "1835-Y5-R2FR-DeltaGamma-component-map-to-P4-observables.md",
    "1836": ROOT / "1836-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton.md",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2149_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2149-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2149*",
        "*Y5_R2FR_connection_hinge_bivector_owner_or_c2_map_fill_2149*",
        "*AFRAME_CONNECTION_DELTAGAMMA_FRONTIER_2149*",
        "*JR2149*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2149_00_2148", DOCS["2148"], [["VAL2148_OVERALL"], ["CONNECTION_HINGE_OWNER_NEXT"], ["c2_visible"]], "current handoff from Phi/c2 hinge to connection/hinge geometry owner"),
        ("SRC2149_01_1828", DOCS["1828"], [["VAL1828_OVERALL"], ["CONNECTION_OWNER_FAILS_CURRENT_CORPUS"], ["HINGE_OWNER_FAILS_CURRENT_CORPUS"]], "connection and hinge owners both fail current corpus"),
        ("SRC2149_02_1829", DOCS["1829"], [["VAL1829_OVERALL"], ["METRIC_ONLY_CONNECTION_THEOREM_NOT_SIGNED"], ["P4_HINGE_SOURCE_PACK_STAGED_NONCLAIM"]], "metric-only theorem exact but parent grammar unsigned"),
        ("SRC2149_03_1830", DOCS["1830"], [["VAL1830_OVERALL"], ["NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN"], ["P4_EXECUTABLE_ROW_FILL_REQUIRED"]], "no-independent-connection grammar attempt fails"),
        ("SRC2149_04_1831", DOCS["1831"], [["VAL1831_OVERALL"], ["PARENT_FIELD_INVENTORY_CERTIFICATE_NOT_PROVEN"], ["FIRST_P4_NUMERIC_ROW_NOT_FILLED"]], "field inventory certificate and first P4 row remain incomplete"),
        ("SRC2149_05_1832", DOCS["1832"], [["VAL1832_OVERALL"], ["TQ_ZERO_THEOREM_NOT_PROVEN_CURRENT_CORPUS"], ["distortion tensor"]], "torsion/nonmetricity reduced to distortion C equation"),
        ("SRC2149_06_1833", DOCS["1833"], [["VAL1833_OVERALL"], ["DISTORTION_EQUATION_OWNER_NOT_PROVEN"], ["Delta_Gamma"]], "distortion equation owner missing; hypermomentum row staged"),
        ("SRC2149_07_1834", DOCS["1834"], [["VAL1834_OVERALL"], ["NO_HYPERMOMENTUM_THEOREM_NOT_PROVEN"], ["DELTAGAMMA_BOUND_ROW_STAGED_NONCLAIM"]], "no-hypermomentum theorem fails; DeltaGamma components retained"),
        ("SRC2149_08_1835", DOCS["1835"], [["VAL1835_OVERALL"], ["DELTAGAMMA_OBSERVABLE_MAP_SKELETON_WRITTEN_NONCLAIM"], ["PROJECTION_MATRICES_MISSING"]], "DeltaGamma components mapped to arenas but not score-ready"),
        ("SRC2149_09_1836", DOCS["1836"], [["VAL1836_OVERALL"], ["P_WEP_FROM_MATTER_FUNCTOR_NEXT"], ["WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON_WRITTEN_NONCLAIM"]], "first projection skeleton built; P_WEP matter-functor response is next"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def frontier_chain_rows() -> list[dict[str, object]]:
    chain = [
        ("FC2149_0", "2148", "connection/hinge owner selected", "Phi/c2 route synced to Palatini/Regge geometry owner", "geometry owner target"),
        ("FC2149_1", "1828", "connection and hinge fail", "Gamma_eff/omega_obs and B_h/A_h are not parent-owned", "P4/hinge fallback retained"),
        ("FC2149_2", "1829", "metric-only theorem", "metric/coframe-only parent would make LC compatibility kinematic", "parent grammar unsigned"),
        ("FC2149_3", "1830", "no independent connection grammar", "need proof no independent connection/hypermomentum slot exists", "not proven"),
        ("FC2149_4", "1831", "field inventory certificate", "candidate q/e/omega stack not enough; first P4 row identified", "certificate fails"),
        ("FC2149_5", "1832", "distortion C equation", "T and Q are projections of C=Gamma-Gamma_LC; need M_C C=0", "M_C/source/projective/boundary missing"),
        ("FC2149_6", "1833", "distortion owner", "delta_C S = M_C C - Delta_Gamma + B_C + P_projective", "equation owner missing"),
        ("FC2149_7", "1834", "DeltaGamma source", "no-hypermomentum theorem fails; DeltaGamma split into components", "component bound row staged"),
        ("FC2149_8", "1835", "observable map", "DeltaGamma components mapped to WEP/PPN/clock/lightcone/R10/orbital channels", "projection matrices missing"),
        ("FC2149_9", "1836", "first projection skeleton", "WEP/clock/lightcone projection skeleton declares P_WEP, P_clock, P_lightcone", "P_WEP response operator next"),
    ]
    rows: list[dict[str, object]] = []
    for chain_id, checkpoint, object_name, gain, status in chain:
        source_path = DOCS[checkpoint]
        line_number, _ = find_line(source_path, ["Current verdict", "Current Verdict", "**Current verdict:**"])
        rows.append(
            row(
                chain_id=chain_id,
                checkpoint=checkpoint,
                source_path=str(source_path),
                verdict_line=line_number,
                object=object_name,
                gain=gain,
                current_status=status,
            )
        )
    return rows


def geometry_to_projection_rows() -> list[dict[str, object]]:
    return [
        row(step_id="GTP2149_0_geometry_owner", object="Gamma_eff/omega_obs + B_h/A_h", exact_need="derive connection compatibility and oriented hinge bivector from MTS geometry", status="FAILED_CURRENT_CORPUS", consequence="Palatini/Regge c2-zero route not promotable"),
        row(step_id="GTP2149_1_metric_only", object="metric/coframe-only parent grammar", exact_need="prove omega/Gamma is derivative-only omega[e_obs] and no independent connection is varied", status="NOT_PARENT_SIGNED", consequence="Levi-Civita compatibility remains conditional"),
        row(step_id="GTP2149_2_distortion", object="C = Gamma - Gamma_LC[g]", exact_need="derive M_C C = Delta_Gamma - B_C - P_projective with positive/invertible M_C", status="EQUATION_OWNER_MISSING", consequence="T=Q=0 theorem blocked"),
        row(step_id="GTP2149_3_source_current", object="Delta_Gamma", exact_need="prove matter/source/readout actions have no independent Gamma current or bound each component", status="NO_HYPERMOMENTUM_NOT_PROVEN", consequence="connection coupling becomes explicit source-current vector"),
        row(step_id="GTP2149_4_projection", object="P_WEP, P_clock, P_lightcone", exact_need="map DeltaGamma components into observable residuals with common units", status="SKELETON_ONLY", consequence="no local test is score-ready"),
        row(step_id="GTP2149_5_live_frontier", object="P_WEP from matter functor", exact_need="derive WEP response operator from parent matter functor before component values are inserted", status="NEXT_BEST_TARGET", consequence="first empirical local-coupling projection can become disciplined"),
    ]


def deltagamma_component_rows() -> list[dict[str, object]]:
    return [
        row(component_id="DG2149_0_spin", component="spin_hypermomentum", channel="axial_torsion_spin_coupling", observables="WEP;clock;lightcone;spin;operator_ledger", status="MISSING_SPIN_CURRENT_NORM_AND_P_WEP"),
        row(component_id="DG2149_1_material", component="material_marker_connection_current", channel="species_source_charge", observables="WEP;clock;source_charge", status="MISSING_MATERIAL_TENSOR_AND_MATTER_FUNCTOR"),
        row(component_id="DG2149_2_source_support", component="source_support_connection_current", channel="source_normalization_operator", observables="R10;PPN;orbital_GM;source_charge", status="MISSING_SOURCE_SUPPORT_PROJECTION"),
        row(component_id="DG2149_3_clock_rods", component="clock_rod_nonmetric_connection_current", channel="nonmetricity_weyl_trace", observables="clock;rod;redshift;WEP", status="MISSING_CLOCK_FUNCTIONAL_AND_Q_TRACE_UNITS"),
        row(component_id="DG2149_4_photon_lightcone", component="photon_lightcone_connection_current", channel="nonmetricity_shear_lightcone", observables="lightcone;PPN_gamma;clock", status="MISSING_LIGHTCONE_RESPONSE_OPERATOR"),
        row(component_id="DG2149_5_orbital_readout", component="orbital_readout_connection_current", channel="source_readout_connection_current", observables="orbital_GM;Gdot;R10;PPN", status="MISSING_NO_FITTED_G_GUARD_PROJECTION"),
        row(component_id="DG2149_6_projective", component="projective_trace_current", channel="torsion_trace_projective_mode", observables="WEP;clock;source_charge;projective_certificate", status="MISSING_PROJECTIVE_ALL_SECTOR_CERTIFICATE"),
    ]


def response_operator_rows() -> list[dict[str, object]]:
    return [
        row(operator_id="ROP2149_0_common_units", operator="DeltaGamma_WCL common vector", needed_form="one dual-connection normalization for spin/material/clock/lightcone/projective components", current_status="MISSING_COMMON_UNITS", score_ready=False),
        row(operator_id="ROP2149_1_P_WEP", operator="P_WEP_eta_AB", needed_form="linearized response from matter-functor connection currents to differential acceleration", current_status="PRIMARY_NEXT_TARGET", score_ready=False),
        row(operator_id="ROP2149_2_P_clock", operator="P_clock", needed_form="clock/rod/redshift response to Q_trace, spin and material currents", current_status="HELD_AFTER_P_WEP", score_ready=False),
        row(operator_id="ROP2149_3_P_lightcone", operator="P_lightcone", needed_form="photon eikonal/null-cone response to trace-free nonmetricity and spin/lightcone currents", current_status="HELD_AFTER_P_WEP", score_ready=False),
        row(operator_id="ROP2149_4_P_R10_PPN_orbital", operator="P_R10/P_PPN/P_orbital", needed_form="source-support and orbital-readout projections without fitted-G absorption", current_status="SECONDARY_SKELETON_PENDING", score_ready=False),
        row(operator_id="ROP2149_5_projective", operator="P_projective_all", needed_form="all-sector projective invariance certificate or trace gauge-fixing map", current_status="MISSING_PROJECTIVE_CERTIFICATE", score_ready=False),
        row(operator_id="ROP2149_6_no_score", operator="local score gate", needed_form="component values + common units + projection matrices + bounds", current_status="NO_ARENA_SCORE_READY", score_ready=False),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2149_0_sync", decision="CURRENT_BRANCH_SYNCED_TO_1836_FRONTIER", because="1828-1836 chase connection/hinge ownership into distortion, DeltaGamma, and the first WEP-clock-lightcone projection skeleton", next_action="stop repeating connection-hinge audits"),
        row(decision_id="DEC2149_1_geometry_result", decision="PALATINI_REGGE_GEOMETRY_NOT_PROMOTED", because="connection compatibility, hinge bivector, parent field inventory and distortion equation are not parent-signed", next_action="do not claim c2 zero or local GR"),
        row(decision_id="DEC2149_2_source_result", decision="DELTAGAMMA_VECTOR_RETAINED", because="no-hypermomentum theorem fails and source/readout/spin/projective components remain legal", next_action="map and bound components rather than erase them"),
        row(decision_id="DEC2149_3_primary_next", decision="P_WEP_FROM_MATTER_FUNCTOR_NEXT", because="WEP is the harshest first local projection and uses the same matter-functor descent needed for clocks/source charge", next_action="derive P_WEP or stage WEP component-bound rows"),
        row(decision_id="DEC2149_4_claim_policy", decision="NO_LOCAL_GR_NEWTON_CLAIM", because="projection operators, component values, common units and arena bounds are missing", next_action="private nonclaim derivation/testing pipeline continues"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2149_0_2150",
            next_target="2150-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md",
            script="scripts/Y5_R2FR_PWEP_response_operator_from_matter_functor_or_component_bound_row_2150.py",
            objective="Derive P_WEP from the parent matter functor and common observed source frame; if it fails, stage sourced nonclaim component-bound rows for eta_AB with units, material basis, projection matrix and no-cancellation guard.",
            forbidden_shortcuts="do not insert placeholder DeltaGamma coefficients; do not borrow clock/lightcone projections as WEP; do not absorb residuals into fitted G; do not claim WEP/local GR; no formalization-workbench edits; no GitHub action",
        )
    ]


def write_branch_copies(
    chain: list[dict[str, object]],
    geometry: list[dict[str, object]],
    components: list[dict[str, object]],
    response: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2149_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_CONNECTION_DELTAGAMMA_FRONTIER_2149_NONCLAIM.csv", geometry + response),
        ("COPY2149_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2149_DELTAGAMMA_WEP_FRONTIER_NONCLAIM.csv", components + response),
        ("COPY2149_2_acquisition_queue", QUEUE / "JR2149_PWEP_MATTER_FUNCTOR_QUEUE.csv", next_rows + response),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    geometry: list[dict[str, object]],
    components: list[dict[str, object]],
    response: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    chain_ok = len(chain) == 10 and chain[0]["checkpoint"] == "2148" and chain[-1]["checkpoint"] == "1836"
    geometry_ok = (
        any(item["step_id"] == "GTP2149_2_distortion" and item["status"] == "EQUATION_OWNER_MISSING" for item in geometry)
        and any(item["step_id"] == "GTP2149_3_source_current" and item["object"] == "Delta_Gamma" for item in geometry)
        and any(item["step_id"] == "GTP2149_5_live_frontier" and item["status"] == "NEXT_BEST_TARGET" for item in geometry)
    )
    components_ok = len(components) == 7 and any(item["component_id"] == "DG2149_6_projective" for item in components)
    response_ok = (
        any(item["operator_id"] == "ROP2149_1_P_WEP" and item["current_status"] == "PRIMARY_NEXT_TARGET" for item in response)
        and all(not truthy(item.get("score_ready", False)) for item in response)
    )
    decisions_ok = (
        any(item["decision"] == "P_WEP_FROM_MATTER_FUNCTOR_NEXT" for item in decisions)
        and any(item["decision"] == "NO_LOCAL_GR_NEWTON_CLAIM" for item in decisions)
    )
    next_ok = any(item["route_id"] == "NEXT2149_0_2150" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, chain, geometry, components, response, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2149_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, chain_ok, geometry_ok, components_ok, response_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2149_00_sources", sources_ok, "2148 and 1828-1836 source checkpoints validate"),
        ("VAL2149_01_chain", chain_ok, "frontier chain runs from 2148 through 1836"),
        ("VAL2149_02_geometry", geometry_ok, "geometry owner failure is converted to distortion/DeltaGamma/projection frontier"),
        ("VAL2149_03_components", components_ok, "all seven DeltaGamma components are retained"),
        ("VAL2149_04_response", response_ok, "P_WEP is selected and no response row is score-ready"),
        ("VAL2149_05_decisions", decisions_ok, "decisions select P_WEP next and block local claims"),
        ("VAL2149_06_next", next_ok, "next target is 2150 P_WEP response operator"),
        ("VAL2149_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2149_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2149_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2149_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2149"),
        ("VAL2149_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2149_OVERALL", all_ok, "2149 syncs connection/hinge ownership to DeltaGamma projection frontier and selects P_WEP matter-functor response next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    geometry: list[dict[str, object]],
    components: list[dict[str, object]],
    response: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2149 - Y5/R2FR Connection Hinge Bivector Owner Or c2 Map Fill",
            "## Current Verdict",
            "2149 does **not** prove connection compatibility, hinge ownership, `c2_visible=0`, P4 safety, WEP, PPN, clocks, lightcone propagation, local GR, Newton, or any public claim. It syncs the current 2148 geometry target to the deepest verified private frontier.",
            "The important result is that the Palatini/Regge route did not vanish; it became sharper. Connection/hinge ownership reduces to the distortion equation `delta_C S = M_C C - Delta_Gamma + B_C + P_projective = 0`. Since `M_C`, source silence, boundary silence and projective silence are not parent-signed, the branch becomes a disciplined `Delta_Gamma` residual-vector problem.",
            "The live edge is now `P_WEP`: derive the WEP response operator from the parent matter functor and common observed source frame. If that works, clocks and lightcones may inherit the same geometry discipline. If it fails, the connection/coupling branch stays empirical with explicit component bounds.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Frontier Chain",
            md_table(chain, ["chain_id", "checkpoint", "verdict_line", "object", "gain", "current_status", "valid_for_claim"]),
            "## Geometry To Projection Map",
            md_table(geometry, ["step_id", "object", "exact_need", "status", "consequence", "valid_for_claim"]),
            "## DeltaGamma Components",
            md_table(components, ["component_id", "component", "channel", "observables", "status", "valid_for_claim"]),
            "## Response Operator Status",
            md_table(response, ["operator_id", "operator", "needed_form", "current_status", "score_ready", "valid_for_claim"]),
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
    chain = frontier_chain_rows()
    geometry = geometry_to_projection_rows()
    components = deltagamma_component_rows()
    response = response_operator_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2149_SOURCE_REGISTER.csv",
        "chain": OUT / "P8_Y5_PARENT_QLOC_2149_FRONTIER_CHAIN.csv",
        "geometry": OUT / "P8_Y5_PARENT_QLOC_2149_GEOMETRY_TO_PROJECTION_MAP.csv",
        "components": OUT / "P8_Y5_PARENT_QLOC_2149_DELTAGAMMA_COMPONENTS.csv",
        "response": OUT / "P8_Y5_PARENT_QLOC_2149_RESPONSE_OPERATOR_STATUS.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2149_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2149_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2149_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2149_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["chain"], chain)
    write_csv(paths["geometry"], geometry)
    write_csv(paths["components"], components)
    write_csv(paths["response"], response)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(chain, geometry, components, response, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, chain, geometry, components, response, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, chain, geometry, components, response, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
