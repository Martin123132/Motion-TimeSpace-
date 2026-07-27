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


DOC = ROOT / "2083-Y5-R2FR-domain-surface-norm-selector-and-CQX-constant-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
Q_R_HAT_POLICY_CEILING = 4.6e-05


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid"}


def formalization_has_2083_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2083-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2083*",
        "*Y5_R2FR_domain_surface_norm_selector_and_CQX_constant_source_pack_2083*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2083_00_2082_doc",
            ROOT / "2082-Y5-R2FR-CQX-outer-trace-flux-extraction-source-pack-or-domain-demotion.md",
            ["NEXT2082_0_2083", "C_QX_trace", "VAL2082_OVERALL"],
            "2082 handoff: source/define common local domain, surface, norm, projector and normalization pack.",
        ),
        (
            "SRC2083_01_2082_validation",
            OUT / "P8_Y5_BRR545_2082_VALIDATION.csv",
            ["VAL2082_OVERALL", "2083 domain/surface/norm source pack selected", "claim_allowed"],
            "2082 validation confirms all C_QX formulae are conditional and nonclaim.",
        ),
        (
            "SRC2083_02_2082_contract",
            OUT / "P8_Y5_PARENT_QLOC_2082_SOURCE_READY_INPUT_CONTRACT.csv",
            ["REQ2082_0_domain", "S_ext;r_ext;area_ext;normal_orientation;reference_subtraction", "MISSING_SOURCE_READY_ROW"],
            "2082 required-input contract is the direct checklist for 2083.",
        ),
        (
            "SRC2083_03_1256_exterior",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_1_spherical_exterior", "r^2 Z_R partial_r R_AB = Q_R", "Q_R = int_{S_r} Pi_R^n dS"],
            "1256 gives the exterior current grammar for trace and flux normalization.",
        ),
        (
            "SRC2083_04_1172_trace",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["HBP1172_2_trace_to_boundary", "C_trace(D,gamma)", "MISSING_TRACE_CONSTANT"],
            "1172 gives trace theorem grammar and says the concrete domain constant is missing.",
        ),
        (
            "SRC2083_05_1206_normal_trace",
            ROOT / "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            ["DRV1206_0_boundary_trace_lowering", "C_NT(D,gamma)", "LOWERED_TO_GEOMETRIC_TRACE_CONTRACT_NONCLAIM"],
            "1206 gives normal-trace grammar but no reciprocal-domain constant.",
        ),
        (
            "SRC2083_06_2062_orientation",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "N_sphere", "MISSING_ORIENTATION_CONVENTION"],
            "2062 names the finite normalization/orientation blockers.",
        ),
        (
            "SRC2083_07_1521_bridge",
            ROOT / "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md",
            ["QBRG1521_3_same_normalization", "QLOC_TO_QR_BRIDGE_NOT_PROVED", "retained-channel silence"],
            "1521 keeps q_loc to q_R bridge and retained-channel silence blocked.",
        ),
        (
            "SRC2083_08_1244_GM",
            OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            ["GM1244_0_qR_definition", "q_R_hat = Q_R c^2/(G M_source)", "weak-field map assumes areal-radial matching"],
            "1244 supplies q_R_hat and areal-radial weak-field convention as a convention-only row.",
        ),
        (
            "SRC2083_09_2080_runner",
            ROOT / "2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md",
            ["MISSING_QRHAT_MAP", "K_qR", "VAL2080_OVERALL"],
            "2080 finite runner still awaits the K_qR/C_QX map.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                exists=path.exists(),
                needle_count=len(needles),
                missing_needles=";".join(missing),
                status="EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                note=note,
            )
        )
    return rows


def local_cell_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CELL2083_0_domain_family",
            "D_ext[r_source,r_ext]",
            "local exterior extraction shell outside the compact source worldtube and inside the weak-field comparison region",
            "CANDIDATE_SELECTOR_NOT_PARENT_SIGNED",
            "source body; source radius/worldtube; r_ext placement; local weak-field chart; boundary class",
        ),
        (
            "CELL2083_1_outer_surface",
            "S_ext={r=r_ext}",
            "round areal sphere with area_ext=4*pi*r_ext^2 and outward normal n=+partial_r",
            "GEOMETRICALLY_EXACT_IF_AREAL_RADIAL_CHART_SIGNED",
            "areal-radius certificate; normal orientation; nonround fallback if chart is not spherical",
        ),
        (
            "CELL2083_2_reference_subtraction",
            "R_AB_ref",
            "subtract asymptotic or background offset before extracting the 1/r coefficient",
            "REQUIRED_NOT_SOURCED",
            "R_AB_infinity or local reference prescription; proof subtraction does not erase flux",
        ),
        (
            "CELL2083_3_XE_norm",
            "X_E",
            "finite reciprocal energy norm used by the 2080 pressure inequality and the C_QX extraction theorem",
            "REQUIRED_NOT_SOURCED",
            "norm_id; measure; derivative order; same-domain link to trace/flux constants",
        ),
        (
            "CELL2083_4_RAB_projector",
            "P_RAB",
            "component projector from finite reciprocal variables to the exterior scalar R_AB whose monopole is Q_R",
            "REQUIRED_NOT_SOURCED",
            "field basis; gauge/representative silence; proof P_RAB X_E is the controlled component",
        ),
        (
            "CELL2083_5_ZR_PiR",
            "Z_R and Pi_R^n",
            "choose unit-Q_R, kinetic-Z_R trace, flux-density, or total-flux normalization before applying C_QX",
            "REQUIRED_NOT_SOURCED",
            "Z_R units/sign; Pi_R density-vs-total flag; N_sphere convention; orientation",
        ),
        (
            "CELL2083_6_GM_binding",
            "GM_source",
            "bind raw Q_R to q_R_hat=Q_R c^2/(G M_source) for the named local-test source",
            "CONVENTION_EXISTS_VALUE_STILL_NEEDED",
            "source_body; measured GM; coordinate convention; direct q_R_hat row if bypassing raw Q_R",
        ),
    ]
    return [
        row(
            cell_id=cell_id,
            selector_object=selector_object,
            definition=definition,
            status=status,
            missing_inputs=missing_inputs,
            source_ready=False,
            score_ready=False,
            claim_allowed=False,
        )
        for cell_id, selector_object, definition, status, missing_inputs in specs
    ]


def cqx_constant_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CQX2083_0_unit_trace_round",
            "unit-Q_R trace on round areal S_ext",
            "R_AB=-Q_R/r_ext; area_ext=4*pi*r_ext^2; ||R_AB||_S <= C_trace_out X_E",
            "C_QX=C_trace_out/sqrt(4*pi)",
            "C_trace_out;S_ext certificate;P_RAB;reference subtraction",
        ),
        (
            "CQX2083_1_kinetic_trace_round",
            "kinetic-Z_R trace on round areal S_ext",
            "R_AB=-Q_R/(Z_R*r_ext); area_ext=4*pi*r_ext^2; ||R_AB||_S <= C_trace_out X_E",
            "C_QX=abs(Z_R)*C_trace_out/sqrt(4*pi)",
            "Z_R;C_trace_out;S_ext certificate;P_RAB;reference subtraction",
        ),
        (
            "CQX2083_2_normal_derivative_round",
            "normal derivative on round areal S_ext",
            "partial_n R_AB=Q_R/(Z_R*r_ext^2); ||partial_n R_AB||_S <= C_normal_out X_E",
            "C_QX=abs(Z_R)*r_ext*C_normal_out/sqrt(4*pi)",
            "Z_R;r_ext;C_normal_out;normal_orientation;boundary_class",
        ),
        (
            "CQX2083_3_flux_density_round",
            "Pi_R^n density on round areal S_ext",
            "Q_R=int_S Pi_R^n dS; ||Pi_R^n||_S <= C_flux_out X_E; area_ext=4*pi*r_ext^2",
            "C_QX=sqrt(4*pi)*r_ext*C_flux_out",
            "Pi_R_density_normalization;r_ext;C_flux_out;orientation;absolute tails",
        ),
        (
            "CQX2083_4_total_flux",
            "total-charge normalized flux",
            "the controlled boundary variable is already total Q_R, not an L2 density",
            "C_QX=C_flux_total",
            "total_flux_norm_definition;C_flux_total;orientation;source path",
        ),
    ]
    return [
        row(
            constant_id=constant_id,
            route=route,
            assumptions=assumptions,
            C_QX_formula=C_QX_formula,
            missing_inputs=missing_inputs,
            status="FORMULA_READY_INPUTS_MISSING",
            score_ready=False,
            claim_allowed=False,
        )
        for constant_id, route, assumptions, C_QX_formula, missing_inputs in specs
    ]


def source_pack_rows() -> list[dict[str, object]]:
    specs = [
        ("PACK2083_0_domain_id", "domain_id", "highest", "shared local extraction domain for X_E, C_QX, and local-test projection", "MISSING"),
        ("PACK2083_1_surface_geometry", "S_ext;r_ext;area_ext;normal_orientation", "highest", "round areal sphere certificate or explicit nonround area/normal replacement", "MISSING"),
        ("PACK2083_2_reference", "R_AB_reference_subtraction", "highest", "background/asymptotic offset prescription for the 1/r coefficient", "MISSING"),
        ("PACK2083_3_projector", "P_RAB", "highest", "component projector from reciprocal field variables to exterior R_AB", "MISSING"),
        ("PACK2083_4_XE_norm", "X_E norm metadata", "highest", "norm, measure, derivative order, and same-domain relation to C_trace/C_flux", "MISSING"),
        ("PACK2083_5_trace_constant", "C_trace_out", "high", "trace bound ||R_AB||_L2(S_ext)<=C_trace_out X_E", "MISSING"),
        ("PACK2083_6_normal_constant", "C_normal_out", "high", "normal derivative bound ||partial_n R_AB||_L2(S_ext)<=C_normal_out X_E", "MISSING"),
        ("PACK2083_7_flux_constant", "C_flux_out or C_flux_total", "high", "Pi_R flux density or total-charge bound with explicit normalization", "MISSING"),
        ("PACK2083_8_ZR_PiR", "Z_R;Pi_R^n;N_sphere", "high", "kinetic/flux normalization and density-vs-total flag", "MISSING"),
        ("PACK2083_9_GM", "source_body;GM_source", "medium", "raw Q_R to q_R_hat conversion for a named local comparator", "CONVENTION_ONLY"),
        ("PACK2083_10_retained_channels", "retained-channel ledger", "medium", "zero-bound or independently bound all non-R_AB channels before claim", "MISSING"),
    ]
    return [
        row(
            pack_id=pack_id,
            required_input=required_input,
            priority=priority,
            purpose=purpose,
            current_status=current_status,
            source_ready=False,
            score_ready=False,
            claim_allowed=False,
        )
        for pack_id, required_input, priority, purpose, current_status in specs
    ]


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2083_0_unit_trace_round",
            route="unit-Q_R round trace",
            formula="K_qR=(c^2/(G*M_source))*C_trace_out/sqrt(4*pi)",
            input_status="REFUSED_MISSING_TRACE_DOMAIN_PROJECTOR_GM",
            missing_inputs="C_trace_out;domain_id;S_ext_certificate;P_RAB;GM_source;retained_channel_ledger",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2083_1_kinetic_trace_round",
            route="kinetic-Z_R round trace",
            formula="K_qR=(c^2/(G*M_source))*abs(Z_R)*C_trace_out/sqrt(4*pi)",
            input_status="REFUSED_MISSING_ZR_TRACE_DOMAIN_PROJECTOR_GM",
            missing_inputs="Z_R;C_trace_out;domain_id;S_ext_certificate;P_RAB;GM_source;retained_channel_ledger",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2083_2_normal_round",
            route="normal derivative round trace",
            formula="K_qR=(c^2/(G*M_source))*abs(Z_R)*r_ext*C_normal_out/sqrt(4*pi)",
            input_status="REFUSED_MISSING_NORMAL_CONSTANT_AND_NORMALIZATION",
            missing_inputs="Z_R;r_ext;C_normal_out;normal_orientation;domain_id;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2083_3_flux_density_round",
            route="Pi_R density flux",
            formula="K_qR=(c^2/(G*M_source))*sqrt(4*pi)*r_ext*C_flux_out",
            input_status="REFUSED_MISSING_PIR_DENSITY_CONSTANT",
            missing_inputs="Pi_R_density_normalization;r_ext;C_flux_out;orientation;domain_id;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2083_4_total_flux",
            route="total-charge flux",
            formula="K_qR=(c^2/(G*M_source))*C_flux_total",
            input_status="REFUSED_MISSING_TOTAL_FLUX_SOURCE",
            missing_inputs="C_flux_total;total_flux_norm_definition;orientation;domain_id;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2083_0_candidate_cell", "candidate local extraction cell exists", "PASS_SCHEMA_ONLY", "round areal surface/domain pack is written as a nonclaim selector"),
        ("GATE2083_1_surface_parent_signed", "surface/domain are parent-signed", "FAIL_BLOCKED", "areal sphere, normal, reference subtraction and domain_id are not parent-owned rows"),
        ("GATE2083_2_projector", "P_RAB maps X_E to exterior R_AB", "FAIL_BLOCKED", "component projector remains missing"),
        ("GATE2083_3_constants", "C_trace/C_normal/C_flux constants supplied", "FAIL_BLOCKED", "no numerical or theorem-bound constants exist in the same domain"),
        ("GATE2083_4_ZR_PiR", "Z_R/Pi_R normalization supplied", "FAIL_BLOCKED", "density-vs-total and kinetic normalization remain unsigned"),
        ("GATE2083_5_KqR_score", "K_qR can be scored", "FAIL_REFUSED", "all dry-run branches refuse missing source inputs"),
        ("GATE2083_6_local_GR_claim", "local GR/Newton/PPN claim", "FAIL_BLOCKED", "q_loc bridge and retained-channel silence still missing"),
    ]
    return [
        row(
            gate_id=gate_id,
            condition=condition,
            status=status,
            reason=reason,
            claim_allowed=False,
        )
        for gate_id, condition, status, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2083_0_round_cell_is_best_next_candidate",
            decision="Use the round areal exterior cell as the default candidate selector.",
            because="1244 already uses an areal-radial weak-field convention and 2082 shows the round sphere cancels the trace-radius factor.",
            next_action="parent-sign the surface/domain/reference/projector rows before any score",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2083_1_trace_route_is_least_scrutiny",
            decision="The trace route is the least exposed finite route if C_trace_out and P_RAB can be sourced.",
            because="it avoids Pi_R density-vs-total ambiguity and reduces to C_trace_out/sqrt(4*pi) in unit-Q_R normalization.",
            next_action="attack P_RAB plus C_trace_out before flux-density scoring",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2083_2_flux_route_stays_fallback",
            decision="Flux route remains useful but has more normalization traps.",
            because="it needs Pi_R density/total convention, Z_R or N_sphere, orientation, and absolute tail accounting.",
            next_action="keep flux rows as fallback if trace projector fails",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2083_3_next_target",
            decision="Next target is the R_AB component projector and trace constant owner.",
            because="without P_RAB and C_trace_out, the clean geometric cell still cannot bind X_E to Q_R.",
            next_action="build 2084 P_RAB projector and C_trace_out owner-or-demotion checkpoint",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2083_0_2084",
            target_doc="2084-Y5-R2FR-RAB-component-projector-and-Ctrace-owner-or-flux-fallback.md",
            objective="derive/source the P_RAB component projector and C_trace_out owner for the round exterior extraction cell; if the trace route fails, keep flux route as fallback with explicit Pi_R density/total normalization",
            must_include="P_RAB definition; gauge/representative silence; X_E to R_AB bound; C_trace_out theorem or source row; reference subtraction; Z_R convention if kinetic; no local-test claim",
            exclusions="using Cassini ceiling as prediction; scoring K_qR without P_RAB and C_trace_out; closure q_R=0; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    cells: list[dict[str, object]],
    constants: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2083_0_source_weight_domain",
            SOURCE_WEIGHT_DOCS / "AFRAME_DOMAIN_SURFACE_CQX_SELECTOR_2083_NONCLAIM.csv",
            cells + constants + dry,
        ),
        (
            "COPY2083_1_wep_domain",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2083_DOMAIN_CQX_SELECTOR_NONCLAIM.csv",
            constants + dry,
        ),
        (
            "COPY2083_2_queue_2084",
            QUEUE / "JR2083_RAB_PROJECTOR_CTRACE_OWNER_QUEUE.csv",
            pack + next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data_rows in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=copy_id,
                path=str(path),
                rows_written=len(data_rows),
                status="WRITTEN_NONCLAIM_COPY",
                claim_allowed=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    cells: list[dict[str, object]],
    constants: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    cell_schema_ok = any(r["cell_id"] == "CELL2083_1_outer_surface" for r in cells)
    reference_ok = any(r["cell_id"] == "CELL2083_2_reference_subtraction" for r in cells)
    projector_missing_ok = any(r["cell_id"] == "CELL2083_4_RAB_projector" and r["status"] == "REQUIRED_NOT_SOURCED" for r in cells)
    unit_trace_ok = any(r["constant_id"] == "CQX2083_0_unit_trace_round" and "sqrt(4*pi)" in str(r["C_QX_formula"]) for r in constants)
    kinetic_trace_ok = any(r["constant_id"] == "CQX2083_1_kinetic_trace_round" and "abs(Z_R)" in str(r["C_QX_formula"]) for r in constants)
    flux_ok = any(r["constant_id"] == "CQX2083_3_flux_density_round" and "sqrt(4*pi)*r_ext" in str(r["C_QX_formula"]) for r in constants)
    source_pack_ok = all(r["score_ready"] is False or str(r["score_ready"]).lower() == "false" for r in pack)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in dry)
    gates_blocked = all(not truthy(r.get("claim_allowed")) for r in gates)
    least_scrutiny_selected = any(r["decision_id"] == "DEC2083_1_trace_route_is_least_scrutiny" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2083_0_2084"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [cells, constants, pack, dry, gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2083_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2083_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2083_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2083_02_cell_schema", cell_schema_ok, "round areal extraction cell schema exists"),
        ("VAL2083_03_reference", reference_ok, "reference subtraction row exists"),
        ("VAL2083_04_projector_missing", projector_missing_ok, "P_RAB projector is explicitly missing/not smuggled"),
        ("VAL2083_05_unit_trace_constant", unit_trace_ok, "unit-Q_R round trace C_QX constant is reduced"),
        ("VAL2083_06_kinetic_trace_constant", kinetic_trace_ok, "kinetic Z_R round trace C_QX constant is reduced"),
        ("VAL2083_07_flux_constant", flux_ok, "round flux-density C_QX constant is reduced"),
        ("VAL2083_08_source_pack_nonclaim", source_pack_ok, "source pack rows remain unscored/nonclaim"),
        ("VAL2083_09_dry_refusal", dry_refused, "all dry-run branches refuse missing inputs"),
        ("VAL2083_10_claim_gates_blocked", gates_blocked, "claim gates remain blocked"),
        ("VAL2083_11_least_scrutiny_route", least_scrutiny_selected, "trace route selected as least-scrutiny next attack"),
        ("VAL2083_12_next_selected", next_ok, "2084 P_RAB/C_trace target selected"),
        ("VAL2083_13_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2083_14_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2083_15_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2083_16_no_formalization_artifacts", no_formalization_artifacts, "no 2083 artifacts were written under formalization-workbench"),
        ("VAL2083_17_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2083_OVERALL", overall, "2083 installs the candidate local extraction cell, reduces C_QX constants, refuses scoring, and selects P_RAB/C_trace owner"))
    return [
        row(
            check_id=check_id,
            status="PASS" if status else "FAIL",
            detail=detail,
            claim_allowed=False,
        )
        for check_id, status, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    cells: list[dict[str, object]],
    constants: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2083 Y5 R2FR Domain Surface Norm Selector And C_QX Constant Source Pack",
        "",
        "## Current Verdict",
        "",
        "2083 takes the `C_QX` bridge from conditional algebra to a concrete nonclaim local extraction-cell contract. The cleanest candidate is a round areal exterior surface `S_ext={r=r_ext}` inside the weak-field local-test chart, with `area_ext=4*pi*r_ext^2`, outward normal `+partial_r`, and an explicit `R_AB` reference subtraction.",
        "",
        "This is not yet parent-signed. The cell is a selector schema, not a claim. It tells us exactly what source rows must exist before `K_qR=(c^2/(G*M_source))*C_QX` can be scored.",
        "",
        "The least-scrutiny route is now the trace route: under unit-`Q_R` normalization, the round-sphere identity reduces to `C_QX=C_trace_out/sqrt(4*pi)`. Under the kinetic convention, it becomes `C_QX=|Z_R|*C_trace_out/sqrt(4*pi)`. This avoids the flux route's density-vs-total normalization trap.",
        "",
        "The flux route remains available but demoted to fallback: for a round sphere and L2 flux density, `C_QX=sqrt(4*pi)*r_ext*C_flux_out`; if the controlled flux is already total-charge normalized, `C_QX=C_flux_total`.",
        "",
        "The next hard physics gate is not another broad local-GR discussion. It is specific: derive/source the `P_RAB` component projector and the `C_trace_out` owner in the same domain/norm. Until those exist, no local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## Local Extraction Cell",
        md_table(cells, ["cell_id", "selector_object", "definition", "status", "missing_inputs", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## C_QX Constant Reductions",
        md_table(constants, ["constant_id", "route", "assumptions", "C_QX_formula", "missing_inputs", "status", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Source Pack",
        md_table(pack, ["pack_id", "required_input", "priority", "purpose", "current_status", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry, ["run_id", "route", "formula", "input_status", "missing_inputs", "K_qR_value", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "condition", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "exclusions", "claim_allowed", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows_written", "status", "claim_allowed", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    cells = local_cell_rows()
    constants = cqx_constant_rows()
    pack = source_pack_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2083_SOURCE_REGISTER.csv",
        "cells": OUT / "P8_Y5_PARENT_QLOC_2083_LOCAL_EXTRACTION_CELL.csv",
        "constants": OUT / "P8_Y5_PARENT_QLOC_2083_CQX_CONSTANT_REDUCTIONS.csv",
        "pack": OUT / "P8_Y5_PARENT_QLOC_2083_SOURCE_PACK.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2083_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2083_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2083_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2083_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2083_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2083_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["cells"], cells)
    write_csv(paths["constants"], constants)
    write_csv(paths["pack"], pack)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(cells, constants, pack, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, cells, constants, pack, dry, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, cells, constants, pack, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
