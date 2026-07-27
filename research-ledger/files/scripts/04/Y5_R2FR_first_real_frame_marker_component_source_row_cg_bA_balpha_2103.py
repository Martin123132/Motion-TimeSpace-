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


DOC = ROOT / "2103-Y5-R2FR-first-real-frame-marker-component-source-row-cg-bA-balpha.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2102_DOC = ROOT / "2102-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"
CSV_2102_BOUND = OUT / "P8_Y5_PARENT_QLOC_2102_BOUND_INPUT_ROWS.csv"
CSV_2102_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_2102_SURVIVING_COUPLING_COMPONENTS.csv"
CSV_2102_ARENAS = OUT / "P8_Y5_PARENT_QLOC_2102_ARENA_RESIDUAL_MAP.csv"
CSV_2102_DEC = OUT / "P8_Y5_PARENT_QLOC_2102_DECISION_LEDGER.csv"
CSV_2102_NEXT = OUT / "P8_Y5_PARENT_QLOC_2102_NEXT_TARGET.csv"
CSV_2102_VAL = OUT / "P8_Y5_BRR545_2102_VALIDATION.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2103_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2103-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2103*",
        "*Y5_R2FR_first_real_frame_marker_component_source_row_cg_bA_balpha_2103*",
        "*AFRAME_FIRST_FRAME_MARKER_SOURCE_2103*",
        "*JR2103_CG_PPN*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def local_source_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2103_00_2102_doc",
            SRC_2102_DOC,
            ["NEXT2102_0_2103", "FIRST_REAL_FRAME_MARKER_COMPONENT_SOURCE_ROW_NEXT", "VAL2102_OVERALL"],
            "2102 selects first real frame/marker component source rows rather than another no-marker loop.",
        ),
        (
            "SRC2103_01_2102_bound_rows",
            CSV_2102_BOUND,
            ["FMB2102_0_cg", "FMB2102_2_bA", "FMB2102_3_balpha", "MISSING_NUMERIC_BOUND"],
            "2102 bound input rows define c_g, b_A and b_alpha as live nonclaim components.",
        ),
        (
            "SRC2103_02_2102_components",
            CSV_2102_COMPONENTS,
            ["SCC2102_0_cg", "SCC2102_2_bA", "SCC2102_3_balpha", "LIVE_UNSIGNED"],
            "2102 surviving components identify the three first source targets.",
        ),
        (
            "SRC2103_03_2102_arenas",
            CSV_2102_ARENAS,
            ["ARM2102_1_PPN", "ARM2102_4_WEP", "ARM2102_5_EM", "BLOCKED_VALUES_MISSING"],
            "2102 arena rows map c_g/b_A/b_alpha to PPN, WEP and EM/clock tests.",
        ),
        (
            "SRC2103_04_2102_decision",
            CSV_2102_DEC,
            ["DEC2102_2_best_route", "FIRST_REAL_FRAME_MARKER_COMPONENT_SOURCE_ROW_NEXT"],
            "2102 decision says the non-looping route is a first component source row.",
        ),
        (
            "SRC2103_05_2102_next",
            CSV_2102_NEXT,
            ["NEXT2102_0_2103", "2103-Y5-R2FR-first-real-frame-marker-component-source-row-cg-bA-balpha.md"],
            "2102 next target points exactly at this source table.",
        ),
        (
            "SRC2103_06_2102_validation",
            CSV_2102_VAL,
            ["VAL2102_OVERALL", "PASS", "first source-backed component row"],
            "2102 validation is clean and nonclaim.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2103_local_handoff",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2103=use,
                valid_for_claim=False,
            )
        )
    return rows


def external_source_rows() -> list[dict[str, object]]:
    specs = [
        (
            "EXT2103_0_cassini_ppn_gamma",
            "Cassini radio-link test of GR",
            "Bertotti, Iess, Tortora, Nature 425, 374-376 (2003)",
            "https://doi.org/10.1038/nature01997",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "PPN gamma / Shapiro delay",
            "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
            "c_g;b_dis;q_nonH",
            "primary DOI/PubMed source; value transcribed as a source anchor only",
            "MTS_PPN_PROJECTION_MISSING",
        ),
        (
            "EXT2103_1_microscope_wep",
            "MICROSCOPE final WEP result",
            "Touboul et al., Phys. Rev. Lett. 129, 121102 (2022)",
            "https://doi.org/10.1103/PhysRevLett.129.121102",
            "https://arxiv.org/abs/2209.15487",
            "Eotvos ratio eta(Ti,Pt)",
            "eta(Ti,Pt) = [-1.5 +/- 2.3(stat) +/- 1.5(syst)] x 10^-15",
            "b_A;b_marker;delta_kappa_A;q_domain",
            "primary arXiv/PRL source; composition mapping still MTS-missing",
            "MTS_COMPOSITION_PROJECTION_MISSING",
        ),
        (
            "EXT2103_2_eotwash_short_range",
            "Eot-Wash inverse-square law anchor",
            "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um, Phys. Rev. Lett. 124, 101101 (2020)",
            "https://doi.org/10.1103/PhysRevLett.124.101101",
            "https://www.npl.washington.edu/eotwash/node/1",
            "short-range Yukawa alpha(lambda)",
            "separations down to 52 um; full alpha(lambda) curve still needs digitization/table",
            "c_g;b_A;delta_kappa_A;q_boundary",
            "official Eot-Wash publication listing plus DOI; not a digitized bound curve",
            "MTS_R10_ALPHA_CURVE_AND_PROJECTION_MISSING",
        ),
        (
            "EXT2103_3_rosenband_alpha_clock",
            "Al+/Hg+ optical-clock alpha variation",
            "Rosenband et al., Science 319, 1808-1812 (2008)",
            "https://doi.org/10.1126/science.1154622",
            "https://pubmed.ncbi.nlm.nih.gov/18323415/",
            "present-era fine-structure variation",
            "dot(alpha)/alpha = (-1.6 +/- 2.3) x 10^-17 yr^-1",
            "b_alpha;b_A;b_marker;c_g",
            "primary DOI/PubMed source; local spatial/frame projection still missing",
            "MTS_CLOCK_ALPHA_PROJECTION_MISSING",
        ),
    ]
    return [
        row(
            external_id=external_id,
            source_title=title,
            citation=citation,
            doi_url=doi_url,
            source_url=source_url,
            observable=observable,
            source_bound_or_measurement=measurement,
            candidate_mts_components=components,
            extraction_note=note,
            mts_mapping_status=status,
            source_backed=True,
            projection_ready=False,
            score_ready=False,
            valid_for_claim=False,
        )
        for external_id, title, citation, doi_url, source_url, observable, measurement, components, note, status in specs
    ]


def component_source_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CSR2103_0_cg_ppn",
            "c_g",
            "PPN gamma",
            "EXT2103_0_cassini_ppn_gamma",
            "Delta_gamma_MTS = Pi_gamma_cg*c_g + Pi_gamma_dis*b_dis + Pi_gamma_nonH*q_nonH",
            "tau_gamma ~= O(10^-5) from Cassini source anchor",
            "MISSING_Pi_gamma_cg_AND_FRAME_LOCK",
            "highest priority because it is the cleanest local-GR/Newton gate",
        ),
        (
            "CSR2103_1_cg_r10",
            "c_g",
            "short-range Yukawa alpha(lambda)",
            "EXT2103_2_eotwash_short_range",
            "alpha_MTS(lambda)=K_X(lambda)*Qbar_XH(lambda)*qbar_XT(c_g,...)",
            "source anchor exists, but no digitized alpha(lambda) curve in this row",
            "MISSING_K_X_Qbar_XH_AND_DIGITIZED_CURVE",
            "parallel R10 route after PPN projection is defined",
        ),
        (
            "CSR2103_2_bA_wep",
            "b_A",
            "MICROSCOPE eta(Ti,Pt)",
            "EXT2103_1_microscope_wep",
            "eta_TiPt_MTS = Pi_eta_bA*(b_A^Ti-b_A^Pt)+Pi_eta_marker*b_marker+Pi_eta_kappa*delta_kappa_A",
            "tau_eta ~= O(10^-15) from MICROSCOPE source anchor",
            "MISSING_COMPOSITION_CHARGE_MAP_AND_Pi_eta_bA",
            "best composition-dependence pressure test once c_g common-frame degeneracy is sorted",
        ),
        (
            "CSR2103_3_balpha_clock",
            "b_alpha",
            "clock alpha variation",
            "EXT2103_3_rosenband_alpha_clock",
            "clock_residual_MTS = Pi_clock_alpha*b_alpha + Pi_clock_A*b_A + Pi_clock_cg*c_g",
            "tau_alpha_dot ~= O(10^-17 yr^-1) source anchor",
            "MISSING_CLOCK_SENSITIVITY_AND_LOCAL_SPATIAL_PROJECTION",
            "keeps EM/readout channel tied to real clock data without claiming MTS alpha variation",
        ),
        (
            "CSR2103_4_abs_vector_gate",
            "qbar_XT_bound_abs",
            "all local arenas",
            "EXT2103_0;EXT2103_1;EXT2103_2;EXT2103_3",
            "||r_local|| <= |Pi_cg c_g|+|Pi_bA b_A|+|Pi_balpha b_alpha|+other unsigned components",
            "no cancellation allowed; source anchors only bound projected residuals after Pi rows exist",
            "MISSING_PROJECTION_MATRIX_AND_COMPONENT_VALUES",
            "prevents false victory by mixing unrelated bounds or cancelling components",
        ),
    ]
    return [
        row(
            row_id=row_id,
            symbol=symbol,
            source_arena=arena,
            external_source_id=source_id,
            mts_projection_formula=formula,
            source_tolerance_anchor=tolerance,
            current_blocker=blocker,
            priority_reason=priority,
            source_backed=True,
            projection_ready=False,
            score_ready=False,
            valid_for_claim=False,
        )
        for row_id, symbol, arena, source_id, formula, tolerance, blocker, priority in specs
    ]


def missing_projection_rows() -> list[dict[str, object]]:
    specs = [
        ("MPR2103_0_Pi_gamma_cg", "Pi_gamma_cg", "coefficient mapping c_g into PPN gamma/Shapiro delay residual", "derive from local weak-field action or parent matter-frame transformation", "blocks c_g->Cassini score"),
        ("MPR2103_1_frame_lock", "frame_lock", "proof that operational rods/clocks use the same frame that enters PPN comparison", "derive readout-frame lock or include frame degeneracy parameter", "blocks measured-G/calibration absorption shortcut"),
        ("MPR2103_2_R10_kernel", "K_X Qbar_XH", "R10 source/test kernel for finite-range component exchange", "derive kernel or source from existing R10 runner inputs", "blocks alpha(lambda) comparator"),
        ("MPR2103_3_composition_charges", "Delta q_A(Ti,Pt)", "composition sensitivity of b_A/b_marker/delta_kappa_A for MICROSCOPE materials", "derive material charge vector or source conservative sensitivity coefficients", "blocks WEP score"),
        ("MPR2103_4_clock_sensitivity", "Pi_clock_alpha", "clock transition sensitivity to b_alpha and readout frame", "source K_alpha for Al+/Hg+ or use clock-comparison sensitivity table", "blocks EM/clock score"),
        ("MPR2103_5_abs_norm", "local residual norm", "common absolute norm joining PPN, WEP, R10 and clock rows without cancellations", "define vector norm and acceptance rules", "blocks any combined local-GR pass"),
    ]
    return [
        row(
            missing_id=missing_id,
            required_quantity=quantity,
            definition=definition,
            how_to_get=how,
            blocks=blocks,
            status="MISSING_REQUIRED_PROJECTION_INPUT",
            valid_for_claim=False,
        )
        for missing_id, quantity, definition, how, blocks in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2103_0_sources", "external source anchors exist", True, "Cassini, MICROSCOPE, Eot-Wash and clock anchors are recorded"),
        ("GATE2103_1_projection", "MTS projection matrix exists", False, "Pi_gamma_cg, R10 kernel, composition charges and clock sensitivities are missing"),
        ("GATE2103_2_component_values", "component values or zero theorems exist", False, "c_g, b_A and b_alpha remain unsigned"),
        ("GATE2103_3_abs_envelope", "absolute no-cancellation residual envelope exists", False, "rule exists but norm/projection rows are missing"),
        ("GATE2103_4_local_GR", "derived local GR/Newton limit can be claimed", False, "requires projection matrix plus component zeros/bounds below all source anchors"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=gate_pass,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, gate, gate_pass, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2103_0_source_result",
            "REAL_SOURCE_ANCHORS_STAGED_NONCLAIM",
            "The project now has real PPN/WEP/R10/clock anchors for c_g, b_A and b_alpha, but they are not MTS scores.",
            "keep them as source-backed projection targets only",
        ),
        (
            "DEC2103_1_best_first_derivation",
            "CG_TO_PPN_PROJECTION_MATRIX_NEXT",
            "c_g to PPN gamma is the cleanest GR/Newton-facing derivation because it attacks the universal-frame coupling before composition complications.",
            "derive Pi_gamma_cg or prove common-frame degeneracy/readout absorption explicitly",
        ),
        (
            "DEC2103_2_no_claim",
            "NO_LOCAL_GR_OR_R10_CLAIM_FROM_SOURCE_ANCHORS",
            "Experimental bounds constrain projected residuals, not raw MTS components, until projection coefficients are derived.",
            "do not compare raw c_g/b_A/b_alpha to external tolerances",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
            valid_for_claim=False,
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2103_0_2104",
            next_target="2104-Y5-R2FR-cg-to-PPN-projection-matrix-or-measured-frame-degeneracy.md",
            script="scripts/Y5_R2FR_cg_to_PPN_projection_matrix_or_measured_frame_degeneracy_2104.py",
            objective="Derive the coefficient mapping common frame coupling c_g into PPN gamma/Shapiro residual, or prove it is exactly a measured-frame degeneracy with no observable PPN residue.",
            forbidden_shortcuts="raw c_g compared directly to gamma; measured-G handwave; cancellation against b_dis/q_nonH; local-GR claim without projection matrix",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    external_sources: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    missing_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2103_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_FIRST_FRAME_MARKER_SOURCE_2103_NONCLAIM.csv",
            external_sources + component_rows + decisions,
        ),
        (
            "COPY2103_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2103_CG_BA_BALPHA_SOURCE_STATUS_NONCLAIM.csv",
            component_rows + missing_rows,
        ),
        (
            "COPY2103_2_acquisition_queue",
            QUEUE / "JR2103_CG_PPN_PROJECTION_OR_FRAME_DEGENERACY_QUEUE.csv",
            missing_rows + next_target,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, copy_rows in copies:
        write_csv(path, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(path),
                path_exists=path.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    local_sources: list[dict[str, object]],
    external_sources: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    missing_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    local_sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in local_sources)
    external_ok = len(external_sources) >= 4 and all(str(source.get("source_url", "")).startswith("https://") and truthy(source.get("source_backed")) for source in external_sources)
    component_ok = len(component_rows) >= 5 and all(truthy(row_.get("source_backed")) and not truthy(row_.get("projection_ready")) for row_ in component_rows)
    missing_ok = len(missing_rows) >= 6 and all(row_.get("status") == "MISSING_REQUIRED_PROJECTION_INPUT" for row_ in missing_rows)
    gates_ok = any(not truthy(row_.get("gate_pass")) for row_ in gates) and all(not truthy(row_.get("claim_allowed")) for row_ in gates)
    decision_ok = any(row_.get("decision") == "CG_TO_PPN_PROJECTION_MATRIX_NEXT" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2103_0_2104" and "2104-Y5-R2FR" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready"))
        for collection in (local_sources, external_sources, component_rows, missing_rows, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2103_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2103_00_local_sources", local_sources_ok, "2102 handoff files exist and contain required needles"),
        ("VAL2103_01_external_sources", external_ok, "real PPN/WEP/R10/clock source anchors recorded with URLs"),
        ("VAL2103_02_component_rows", component_ok, "c_g/b_A/b_alpha rows are source-backed but projection-incomplete"),
        ("VAL2103_03_missing_projection", missing_ok, "projection matrix and sensitivity inputs remain explicit blockers"),
        ("VAL2103_04_claim_gates", gates_ok, "claim gates block local-GR/Newton promotion"),
        ("VAL2103_05_decision", decision_ok, "decision selects c_g to PPN projection as next derivation"),
        ("VAL2103_06_next", next_ok, "next target is 2104 c_g to PPN projection or frame degeneracy"),
        ("VAL2103_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2103_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2103_09_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2103_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2103"),
        ("VAL2103_11_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2103_OVERALL",
            overall,
            "2103 stages real source anchors for c_g/b_A/b_alpha, blocks claims, and selects c_g->PPN projection next",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if ok else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, ok, detail in checks
    ]


def write_doc(
    local_sources: list[dict[str, object]],
    external_sources: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    missing_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2103 - Y5/R2FR First Real Frame-Marker Component Source Row: c_g, b_A, b_alpha",
        "",
        "## Current Verdict",
        "",
        "2103 moves us past the abstract coupling fog. It records real experimental anchors for the first three live frame/marker components: `c_g` via PPN/Cassini and short-range gravity, `b_A` via MICROSCOPE/WEP composition sensitivity, and `b_alpha` via optical-clock fine-structure constraints.",
        "",
        "This is **not** a local-GR, R10, WEP or clock claim. These sources bound observable residuals, not raw MTS variables. The missing object is now the projection matrix from MTS components into each arena.",
        "",
        "The best next derivation is `c_g -> PPN gamma`: either derive the coefficient mapping common-frame coupling into the Cassini/Shapiro residual, or prove it is an exact measured-frame degeneracy with no observable PPN residue.",
        "",
        "## Local Source Register",
        md_table(local_sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2103", "valid_for_claim"]),
        "## External Source Anchors",
        md_table(external_sources, ["external_id", "source_title", "citation", "doi_url", "source_url", "observable", "source_bound_or_measurement", "candidate_mts_components", "mts_mapping_status", "score_ready", "valid_for_claim"]),
        "## Component Source Rows",
        md_table(component_rows, ["row_id", "symbol", "source_arena", "external_source_id", "mts_projection_formula", "source_tolerance_anchor", "current_blocker", "score_ready", "valid_for_claim"]),
        "## Missing Projection Inputs",
        md_table(missing_rows, ["missing_id", "required_quantity", "definition", "how_to_get", "blocks", "status", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "gate", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target",
        md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    local_sources = local_source_rows()
    external_sources = external_source_rows()
    component_rows = component_source_rows()
    missing_rows = missing_projection_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "local_sources": OUT / "P8_Y5_PARENT_QLOC_2103_LOCAL_SOURCE_REGISTER.csv",
        "external_sources": OUT / "P8_Y5_PARENT_QLOC_2103_EXTERNAL_SOURCE_ANCHORS.csv",
        "component_rows": OUT / "P8_Y5_PARENT_QLOC_2103_COMPONENT_SOURCE_ROWS.csv",
        "missing_rows": OUT / "P8_Y5_PARENT_QLOC_2103_MISSING_PROJECTION_INPUTS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2103_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2103_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2103_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2103_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2103_VALIDATION.csv",
    }
    write_csv(paths["local_sources"], local_sources)
    write_csv(paths["external_sources"], external_sources)
    write_csv(paths["component_rows"], component_rows)
    write_csv(paths["missing_rows"], missing_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(external_sources, component_rows, missing_rows, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(local_sources, external_sources, component_rows, missing_rows, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(local_sources, external_sources, component_rows, missing_rows, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
