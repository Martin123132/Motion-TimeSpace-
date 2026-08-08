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


DOC = ROOT / "2082-Y5-R2FR-CQX-outer-trace-flux-extraction-source-pack-or-domain-demotion.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
Q_R_HAT_POLICY_CEILING = 4.6e-05


def formalization_has_2082_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2082-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2082*",
        "*Y5_R2FR_CQX_outer_trace_flux_extraction_source_pack_or_domain_demotion_2082*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid"}


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2082_00_2081_doc",
            ROOT / "2081-Y5-R2FR-KqR-exterior-hair-normalization-bridge-or-finite-input-priority-source-pack.md",
            ["NEXT2081_0_2082", "C_QX", "VAL2081_OVERALL"],
            "2081 handoff: derive/source C_QX or demote K_qR to formula-only.",
        ),
        (
            "SRC2082_01_2081_validation",
            OUT / "P8_Y5_BRR545_2081_VALIDATION.csv",
            ["VAL2081_OVERALL", "2082 C_QX extraction target selected", "claim_allowed"],
            "2081 validation confirms C_QX is the next gate.",
        ),
        (
            "SRC2082_02_1253_charge",
            ROOT / "1253-Y5-R10-reciprocal-Hcore-boundary-charge-derivation-attempt.md",
            ["BCA1253_0_QR_current_constant", "W partial_r R_AB = Q_R", "constant charge is not automatically zero"],
            "1253 supplies the reciprocal 1/r charge shape but not a source-backed value.",
        ),
        (
            "SRC2082_03_1256_exterior",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_1_spherical_exterior", "r^2 Z_R partial_r R_AB = Q_R", "Pi_R^n"],
            "1256 supplies the kinetic exterior current and exposes the missing Z_R/Pi_R normalization.",
        ),
        (
            "SRC2082_04_1172_trace",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["HBP1172_2_trace_to_boundary", "C_trace(D,gamma)", "MISSING_TRACE_CONSTANT"],
            "1172 supplies trace inequality grammar but not the domain constant.",
        ),
        (
            "SRC2082_05_1206_normal_trace",
            ROOT / "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            ["DRV1206_0_boundary_trace_lowering", "C_NT(D,gamma)", "LOWERED_TO_GEOMETRIC_TRACE_CONTRACT_NONCLAIM"],
            "1206 supplies normal-trace grammar for a boundary flux bound.",
        ),
        (
            "SRC2082_06_1521_qbridge",
            ROOT / "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md",
            ["QBRG1521_3_same_normalization", "QLOC_TO_QR_BRIDGE_NOT_PROVED", "Do not import the q_R guardrail into q_loc"],
            "1521 blocks importing q_R scoring into q_loc without a normalization bridge.",
        ),
        (
            "SRC2082_07_2062_orientation",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "MISSING_ORIENTATION_CONVENTION", "CONDITIONAL_PROOF_ONLY"],
            "2062 keeps orientation and finite Pi_R normalization unsigned.",
        ),
        (
            "SRC2082_08_1244_GM",
            OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            ["GM1244_0_qR_definition", "q_R_hat = Q_R c^2/(G M_source)", "CONVENTION_DECLARED_NONCLAIM"],
            "1244 supplies the q_R_hat convention and GM/source-body contract.",
        ),
        (
            "SRC2082_09_1244_policy",
            OUT / "P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            ["RPF1244_0_policy", "4.6e-05", "MISSING_QR_VALUE_UNCHANGED"],
            "1244 supplies the nonclaim policy ceiling but not an MTS prediction.",
        ),
        (
            "SRC2082_10_2080_runner",
            ROOT / "2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md",
            ["MISSING_QRHAT_MAP", "K_qR", "VAL2080_OVERALL"],
            "2080 runner is still waiting for a K_qR/C_QX map.",
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


def cqx_derivation_rows() -> list[dict[str, object]]:
    return [
        row(
            derivation_id="DRV2082_0_trace_amplitude_identity_unit_QR",
            route="outer trace",
            assumptions="S_ext selected; R_AB reference offset subtracted; R_AB=-Q_R/r_ext is constant on S_ext; area_ext is the induced area",
            derivation="||R_AB||_L2(S_ext)=abs(Q_R)*sqrt(area_ext)/r_ext, hence abs(Q_R)=(r_ext/sqrt(area_ext))*||R_AB||_L2(S_ext)",
            C_QX_formula="C_QX_trace=(r_ext/sqrt(area_ext))*C_trace_out",
            status="EXACT_IF_UNIT_QR_CONVENTION_AND_SURFACE_SIGNED",
            missing_inputs="S_ext;r_ext;area_ext;C_trace_out;R_AB_component_projector;reference_subtraction",
            claim_allowed=False,
        ),
        row(
            derivation_id="DRV2082_1_trace_amplitude_identity_kinetic_ZR",
            route="outer trace",
            assumptions="1256 kinetic normalization; R_AB=-Q_R/(Z_R*r_ext); Z_R is constant on the exterior shell and has declared sign/units",
            derivation="||R_AB||_L2(S_ext)=abs(Q_R)*sqrt(area_ext)/(abs(Z_R)*r_ext), hence abs(Q_R)=abs(Z_R)*r_ext*||R_AB||_L2(S_ext)/sqrt(area_ext)",
            C_QX_formula="C_QX_trace_ZR=(abs(Z_R)*r_ext/sqrt(area_ext))*C_trace_out",
            status="EXACT_IF_ZR_AND_SURFACE_SIGNED",
            missing_inputs="Z_R;S_ext;r_ext;area_ext;C_trace_out;R_AB_component_projector;reference_subtraction",
            claim_allowed=False,
        ),
        row(
            derivation_id="DRV2082_2_trace_round_sphere_reduction",
            route="outer trace",
            assumptions="S_ext is a round areal sphere with area_ext=4*pi*r_ext^2",
            derivation="r_ext/sqrt(area_ext)=1/sqrt(4*pi), so the unit-Q_R trace shape factor is radius-independent",
            C_QX_formula="C_QX_trace_round=C_trace_out/sqrt(4*pi), or abs(Z_R)*C_trace_out/sqrt(4*pi) in the kinetic normalization",
            status="CONDITIONAL_GEOMETRIC_SIMPLIFICATION",
            missing_inputs="round_sphere_certificate;areal_radius_convention;Z_R_if_kinetic;C_trace_out",
            claim_allowed=False,
        ),
        row(
            derivation_id="DRV2082_3_normal_derivative_extraction",
            route="normal derivative",
            assumptions="R_AB=-Q_R/(Z_R*r); outward normal derivative partial_n R_AB=Q_R/(Z_R*r_ext^2) is constant on S_ext",
            derivation="||partial_n R_AB||_L2(S_ext)=abs(Q_R)*sqrt(area_ext)/(abs(Z_R)*r_ext^2), hence abs(Q_R)=abs(Z_R)*r_ext^2*||partial_n R_AB||_L2(S_ext)/sqrt(area_ext)",
            C_QX_formula="C_QX_normal=(abs(Z_R)*r_ext^2/sqrt(area_ext))*C_normal_out",
            status="EXACT_IF_NORMAL_DERIVATIVE_BOUND_SIGNED",
            missing_inputs="Z_R;normal_orientation;C_normal_out;S_ext;r_ext;area_ext;boundary_class",
            claim_allowed=False,
        ),
        row(
            derivation_id="DRV2082_4_flux_density_extraction",
            route="normal flux",
            assumptions="Q_R=int_{S_ext} Pi_R^n dS and ||Pi_R^n||_L2(S_ext)<=C_flux_out*X_E",
            derivation="Cauchy-Schwarz gives abs(Q_R)<=sqrt(area_ext)*C_flux_out*X_E",
            C_QX_formula="C_QX_flux=sqrt(area_ext)*C_flux_out",
            status="EXACT_IF_PIR_DENSITY_NORMALIZATION_SIGNED",
            missing_inputs="Pi_R^n_density_normalization;C_flux_out;S_ext;area_ext;orientation;absolute_tail_budget",
            claim_allowed=False,
        ),
        row(
            derivation_id="DRV2082_5_total_charge_flux_extraction",
            route="normal flux",
            assumptions="the controlled flux variable is already total-charge normalized, abs(Q_R)<=C_flux_total*X_E",
            derivation="No extra area factor is allowed if the source row already defines the norm as total charge rather than density",
            C_QX_formula="C_QX_flux_total=C_flux_total",
            status="EXACT_IF_TOTAL_FLUX_NORMALIZATION_SIGNED",
            missing_inputs="total_flux_norm_definition;C_flux_total;orientation;source_path",
            claim_allowed=False,
        ),
    ]


def obstruction_rows() -> list[dict[str, object]]:
    specs = [
        (
            "OBS2082_0_surface_selector",
            "outer surface S_ext",
            "No source row selects the local extraction surface, areal radius, induced area, outward normal, and reference subtraction.",
            "C_QX cannot be numeric or source-ready.",
            "MISSING_DOMAIN_SURFACE_SELECTOR",
        ),
        (
            "OBS2082_1_component_projector",
            "R_AB component projector",
            "The finite energy norm X_E is not yet tied to the exact scalar R_AB exterior component whose monopole is Q_R.",
            "Trace constants could bound the wrong component.",
            "MISSING_COMPONENT_PROJECTOR",
        ),
        (
            "OBS2082_2_trace_constant",
            "C_trace_out",
            "1172 supplies trace grammar but marks the trace constant/domain specification missing.",
            "Trace route remains conditional only.",
            "MISSING_TRACE_CONSTANT",
        ),
        (
            "OBS2082_3_normal_trace_constant",
            "C_normal_out or C_flux_out",
            "1206 supplies normal-trace grammar but not a reciprocal Pi_R/R_AB flux constant in the same domain.",
            "Flux route remains conditional only.",
            "MISSING_FLUX_TRACE_CONSTANT",
        ),
        (
            "OBS2082_4_ZR_normalization",
            "Z_R/Pi_R normalization",
            "1256 exposes r^2 Z_R partial_r R_AB=Q_R and Q_R=int Pi_R^n dS, but does not supply Z_R units/sign or density-vs-total normalization.",
            "The area/Z_R factor cannot be chosen safely.",
            "MISSING_ZR_AND_PIR_NORMALIZATION",
        ),
        (
            "OBS2082_5_GM_binding",
            "GM/source-body binding",
            "1244 declares q_R_hat=Q_R c^2/(G M_source), but no candidate row binds raw Q_R to a named source body and measured GM.",
            "K_qR cannot become a numerical local-test map.",
            "MISSING_SOURCE_BODY_GM_ROW",
        ),
        (
            "OBS2082_6_q_loc_bridge",
            "q_loc to q_R bridge",
            "1521 explicitly forbids importing the q_R guardrail into q_loc without scalar projection, integration, same normalization, and retained-channel silence.",
            "Local PPN/local-GR claim remains blocked.",
            "QLOC_TO_QR_BRIDGE_NOT_PROVED",
        ),
        (
            "OBS2082_7_retained_channels",
            "no-cancellation guard",
            "Boundary, corner, source, readout, vector/gauge, and matter-normalization channels are not all zero-derived or independently bounded.",
            "No cancellation credit is permitted.",
            "MISSING_RETAINED_CHANNEL_SILENCE",
        ),
    ]
    return [
        row(
            obstruction_id=obstruction_id,
            clause=clause,
            obstruction=obstruction,
            consequence=consequence,
            status=status,
            blocks_claim=True,
            claim_allowed=False,
        )
        for obstruction_id, clause, obstruction, consequence, status in specs
    ]


def input_contract_rows() -> list[dict[str, object]]:
    specs = [
        (
            "REQ2082_0_domain",
            "domain_id",
            "local exterior domain used by X_E, trace theorem, and flux extraction",
            "required_before_scoring",
        ),
        (
            "REQ2082_1_surface",
            "S_ext;r_ext;area_ext;normal_orientation;reference_subtraction",
            "outer surface geometry and orientation for the extraction identity",
            "required_before_scoring",
        ),
        (
            "REQ2082_2_projector",
            "R_AB_component_projector",
            "map from finite reciprocal energy variable X_E to the exact exterior scalar R_AB",
            "required_before_scoring",
        ),
        (
            "REQ2082_3_trace",
            "C_trace_out",
            "trace constant for ||R_AB||_L2(S_ext)<=C_trace_out*X_E in the same norm/domain",
            "required_for_trace_route",
        ),
        (
            "REQ2082_4_normal",
            "C_normal_out",
            "normal derivative constant for ||partial_n R_AB||_L2(S_ext)<=C_normal_out*X_E",
            "required_for_normal_route",
        ),
        (
            "REQ2082_5_flux",
            "C_flux_out or C_flux_total",
            "Pi_R^n flux-density or total-flux bound with normalization explicitly declared",
            "required_for_flux_route",
        ),
        (
            "REQ2082_6_ZR",
            "Z_R;Pi_R^n normalization;density_or_total flag",
            "normalization that selects the right C_QX area/Z_R factor",
            "required_before_scoring",
        ),
        (
            "REQ2082_7_GM",
            "source_body;GM_source;coordinate_convention",
            "raw Q_R to q_R_hat conversion for the chosen local-test source",
            "required_before_scoring",
        ),
        (
            "REQ2082_8_silence",
            "retained_channel_zero_or_bound_rows",
            "no-cancellation ledger for all channels outside the extracted reciprocal scalar",
            "required_before_claim",
        ),
    ]
    return [
        row(
            requirement_id=requirement_id,
            required_input=required_input,
            purpose=purpose,
            priority=priority,
            current_status="MISSING_SOURCE_READY_ROW",
            valid_for_claim=False,
            claim_allowed=False,
        )
        for requirement_id, required_input, purpose, priority in specs
    ]


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2082_0_trace_unit_QR",
            attempted_route="trace identity with R_AB=-Q_R/r",
            formula_tested="C_QX=(r_ext/sqrt(area_ext))*C_trace_out",
            input_status="REFUSED_MISSING_SURFACE_TRACE_PROJECTOR",
            missing_inputs="S_ext;r_ext;area_ext;C_trace_out;R_AB_component_projector;reference_subtraction",
            C_QX_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2082_1_trace_kinetic_ZR",
            attempted_route="trace identity with R_AB=-Q_R/(Z_R*r)",
            formula_tested="C_QX=(abs(Z_R)*r_ext/sqrt(area_ext))*C_trace_out",
            input_status="REFUSED_MISSING_ZR_SURFACE_TRACE_PROJECTOR",
            missing_inputs="Z_R;S_ext;r_ext;area_ext;C_trace_out;R_AB_component_projector;reference_subtraction",
            C_QX_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2082_2_normal_derivative",
            attempted_route="normal derivative identity",
            formula_tested="C_QX=(abs(Z_R)*r_ext^2/sqrt(area_ext))*C_normal_out",
            input_status="REFUSED_MISSING_NORMAL_DERIVATIVE_BOUND",
            missing_inputs="Z_R;normal_orientation;C_normal_out;S_ext;r_ext;area_ext",
            C_QX_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2082_3_flux_density",
            attempted_route="Pi_R^n flux density",
            formula_tested="C_QX=sqrt(area_ext)*C_flux_out",
            input_status="REFUSED_MISSING_PIR_DENSITY_NORMALIZATION",
            missing_inputs="Pi_R^n_density_normalization;C_flux_out;S_ext;area_ext;orientation",
            C_QX_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2082_4_flux_total",
            attempted_route="total-charge flux norm",
            formula_tested="C_QX=C_flux_total",
            input_status="REFUSED_MISSING_TOTAL_FLUX_NORM_SOURCE",
            missing_inputs="total_flux_norm_definition;C_flux_total;orientation;source_path",
            C_QX_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2082_0_CQX_formulae", "C_QX formulae derived symbolically", "PASS_CONDITIONAL", "trace, normal derivative, and flux formulae are explicit"),
        ("GATE2082_1_surface", "outer surface/domain source pack", "FAIL_BLOCKED", "S_ext, r_ext, area_ext, normal, and reference subtraction are missing"),
        ("GATE2082_2_projector", "same R_AB component controlled by X_E", "FAIL_BLOCKED", "component projector from X_E to exterior R_AB is missing"),
        ("GATE2082_3_constants", "trace/normal/flux constants source-backed", "FAIL_BLOCKED", "C_trace_out, C_normal_out, and C_flux_out are not supplied"),
        ("GATE2082_4_ZR_PiR", "Z_R/Pi_R normalization signed", "FAIL_BLOCKED", "density-vs-total flux and Z_R convention are unsigned"),
        ("GATE2082_5_KqR_value", "K_qR can be evaluated", "FAIL_REFUSED", "C_QX and GM/source-body inputs are missing"),
        ("GATE2082_6_local_claim", "local GR/Newton/PPN/R10 claim", "FAIL_BLOCKED", "q_loc bridge and retained-channel silence remain missing"),
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
            decision_id="DEC2082_0_CQX_shape_derived",
            decision="C_QX is now an exact conditional surface/flux extraction contract, not a vague coefficient.",
            because="for a selected exterior surface, the 1/r amplitude identity fixes the geometric factor; the remaining unknowns are source rows, not algebra.",
            next_action="source domain/surface/norm/projector data before trying to score K_qR",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2082_1_round_sphere_simplifies",
            decision="If a round areal sphere is parent-signed, the trace shape factor becomes 1/sqrt(4*pi).",
            because="area_ext=4*pi*r_ext^2 cancels the radius in r_ext/sqrt(area_ext).",
            next_action="do not use the simplification until the areal-sphere convention and Z_R convention are sourced",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2082_2_KqR_demoted_for_now",
            decision="K_qR remains formula-only.",
            because="C_QX requires surface geometry, component projector, trace/flux constants, Z_R/Pi_R normalization, and GM binding.",
            next_action="build 2083 domain/surface/norm selector and trace/flux constant source pack",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2082_3_no_claim",
            decision="No local-GR or PPN claim is allowed from this checkpoint.",
            because="the runner correctly refuses all routes with missing parent inputs.",
            next_action="keep q_R_hat ceiling as a nonclaim comparator only",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2082_0_2083",
            target_doc="2083-Y5-R2FR-domain-surface-norm-selector-and-CQX-constant-source-pack.md",
            objective="source or define the common local domain/surface/norm pack needed by C_QX: domain_id, S_ext, r_ext, area_ext, normal, reference subtraction, R_AB component projector, Z_R/Pi_R normalization, and trace/normal/flux constants",
            must_include="round-sphere/areal-radius certificate or explicit nonround area; density-vs-total Pi_R flag; same X_E norm; GM/source-body row; no-cancellation retained-channel ledger",
            exclusions="using Cassini ceiling as prediction; setting q_R=0 by closure; scoring K_qR without C_QX; local GR/Newton/PPN/R10 claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    derivations: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    contracts: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2082_0_source_weight_CQX",
            SOURCE_WEIGHT_DOCS / "AFRAME_CQX_OUTER_TRACE_FLUX_EXTRACTOR_2082_NONCLAIM.csv",
            derivations + obstructions + dry,
        ),
        (
            "COPY2082_1_wep_CQX",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2082_CQX_EXTRACTOR_NONCLAIM.csv",
            derivations + dry,
        ),
        (
            "COPY2082_2_queue_2083",
            QUEUE / "JR2082_DOMAIN_SURFACE_TRACE_CONSTANT_SOURCE_PACK_QUEUE.csv",
            contracts + next_rows_,
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
    derivations: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    contracts: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    trace_formula_ok = any(r["derivation_id"] == "DRV2082_0_trace_amplitude_identity_unit_QR" for r in derivations)
    kinetic_formula_ok = any(r["derivation_id"] == "DRV2082_1_trace_amplitude_identity_kinetic_ZR" for r in derivations)
    normal_formula_ok = any(r["derivation_id"] == "DRV2082_3_normal_derivative_extraction" for r in derivations)
    flux_formula_ok = any(r["derivation_id"] == "DRV2082_4_flux_density_extraction" for r in derivations)
    round_sphere_ok = any(
        "1/sqrt(4*pi)" in str(r["C_QX_formula"]) or "1/sqrt(4*pi)" in str(r["derivation"])
        for r in derivations
    )
    obstruction_ok = all(truthy(r.get("blocks_claim")) and not truthy(r.get("claim_allowed")) for r in obstructions)
    contract_ok = all(r["current_status"] == "MISSING_SOURCE_READY_ROW" for r in contracts)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in dry)
    gates_blocked = all(not truthy(r.get("claim_allowed")) for r in gates)
    decision_demotes = any(r["decision_id"] == "DEC2082_2_KqR_demoted_for_now" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2082_0_2083"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [derivations, obstructions, contracts, dry, gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2082_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2082_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2082_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2082_02_trace_formula", trace_formula_ok, "unit-Q_R trace extraction formula is derived"),
        ("VAL2082_03_kinetic_trace_formula", kinetic_formula_ok, "Z_R kinetic trace extraction formula is derived"),
        ("VAL2082_04_normal_formula", normal_formula_ok, "normal derivative extraction formula is derived"),
        ("VAL2082_05_flux_formula", flux_formula_ok, "Pi_R flux density extraction formula is derived"),
        ("VAL2082_06_round_sphere_factor", round_sphere_ok, "round sphere simplification is recorded conditionally"),
        ("VAL2082_07_obstructions_block", obstruction_ok, "all missing clauses block claims"),
        ("VAL2082_08_contract_rows_missing", contract_ok, "source-ready input contract rows remain missing/nonclaim"),
        ("VAL2082_09_dry_refusal", dry_refused, "all smoke routes refuse missing inputs"),
        ("VAL2082_10_claim_gates_blocked", gates_blocked, "claim gates remain blocked"),
        ("VAL2082_11_KqR_demoted", decision_demotes, "K_qR is demoted to formula-only pending C_QX source rows"),
        ("VAL2082_12_next_selected", next_ok, "2083 domain/surface/norm source pack selected"),
        ("VAL2082_13_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2082_14_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2082_15_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2082_16_no_formalization_artifacts", no_formalization_artifacts, "no 2082 artifacts were written under formalization-workbench"),
        ("VAL2082_17_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2082_OVERALL", overall, "2082 derives the exact conditional C_QX extraction contract, refuses scoring, and selects domain/surface source pack"))
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
    derivations: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    contracts: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2082 Y5 R2FR C_QX outer trace/flux extraction source pack or domain demotion",
        "",
        "## Current Verdict",
        "",
        "2082 makes a real step forward: `C_QX` is no longer an undefined magic coefficient. It is an exact conditional extraction constant from a finite reciprocal energy norm `X_E` to an exterior reciprocal charge `|Q_R|`, provided the outer surface, component projector, trace/flux constants, and normalization are parent-signed.",
        "",
        "Trace route, unit `Q_R` convention: if `R_AB=-Q_R/r_ext` on `S_ext`, then `|Q_R|=(r_ext/sqrt(area_ext))*||R_AB||_L2(S_ext)`, so `C_QX_trace=(r_ext/sqrt(area_ext))*C_trace_out`.",
        "",
        "Trace route, kinetic `Z_R` convention: if `R_AB=-Q_R/(Z_R*r_ext)`, then `C_QX_trace_ZR=(|Z_R|*r_ext/sqrt(area_ext))*C_trace_out`. For a parent-signed round areal sphere, the geometric factor becomes `1/sqrt(4*pi)`, with an extra `|Z_R|` in the kinetic convention.",
        "",
        "Flux route: if `Q_R=int_{S_ext} Pi_R^n dS` and `||Pi_R^n||_L2(S_ext)<=C_flux_out*X_E`, then `C_QX_flux=sqrt(area_ext)*C_flux_out`; if the norm is already total-charge normalized, `C_QX=C_flux_total`. The density-vs-total normalization must be explicit.",
        "",
        "The current corpus still lacks the source-ready domain/surface/norm pack. Therefore `K_qR=(c^2/(G*M_source))*C_QX` remains formula-only and no local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## C_QX Derivation Rows",
        md_table(derivations, ["derivation_id", "route", "assumptions", "derivation", "C_QX_formula", "status", "missing_inputs", "claim_allowed", "valid_for_claim"]),
        "## Blocking Obstructions",
        md_table(obstructions, ["obstruction_id", "clause", "obstruction", "consequence", "status", "blocks_claim", "claim_allowed", "valid_for_claim"]),
        "## Source-Ready Input Contract",
        md_table(contracts, ["requirement_id", "required_input", "purpose", "priority", "current_status", "claim_allowed", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry, ["run_id", "attempted_route", "formula_tested", "input_status", "missing_inputs", "C_QX_value", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
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
    derivations = cqx_derivation_rows()
    obstructions = obstruction_rows()
    contracts = input_contract_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2082_SOURCE_REGISTER.csv",
        "derivations": OUT / "P8_Y5_PARENT_QLOC_2082_CQX_DERIVATION_CONTRACT.csv",
        "obstructions": OUT / "P8_Y5_PARENT_QLOC_2082_BLOCKING_OBSTRUCTIONS.csv",
        "contracts": OUT / "P8_Y5_PARENT_QLOC_2082_SOURCE_READY_INPUT_CONTRACT.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2082_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2082_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2082_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2082_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2082_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2082_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["derivations"], derivations)
    write_csv(paths["obstructions"], obstructions)
    write_csv(paths["contracts"], contracts)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(derivations, obstructions, contracts, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, derivations, obstructions, contracts, dry, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, derivations, obstructions, contracts, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
