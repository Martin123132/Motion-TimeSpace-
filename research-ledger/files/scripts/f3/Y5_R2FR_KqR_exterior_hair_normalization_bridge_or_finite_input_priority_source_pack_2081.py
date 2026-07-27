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


DOC = ROOT / "2081-Y5-R2FR-KqR-exterior-hair-normalization-bridge-or-finite-input-priority-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
Q_R_HAT_POLICY_CEILING = 4.6e-05


def formalization_has_2081_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2081-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2081*",
        "*Y5_R2FR_KqR_exterior_hair_normalization_bridge_or_finite_input_priority_source_pack_2081*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2081_00_2080_doc",
            ROOT / "2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md",
            ["NEXT2080_0_2081", "MISSING_QRHAT_MAP", "VAL2080_OVERALL"],
            "2080 handoff: derive/source K_qR or emit priority finite-input source pack.",
        ),
        (
            "SRC2081_01_2080_validation",
            OUT / "P8_Y5_BRR545_2080_VALIDATION.csv",
            ["VAL2080_OVERALL", "2081 K_qR bridge target selected", "claim_allowed"],
            "2080 validation confirms fail-closed finite runner and K_qR next target.",
        ),
        (
            "SRC2081_02_1253_charge",
            ROOT / "1253-Y5-R10-reciprocal-Hcore-boundary-charge-derivation-attempt.md",
            ["BCA1253_0_QR_current_constant", "W partial_r R_AB = Q_R", "constant charge is not automatically zero"],
            "reciprocal exterior charge exists as a conservation constant, not yet a prediction.",
        ),
        (
            "SRC2081_03_1256_exterior",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_1_spherical_exterior", "r^2 Z_R partial_r R_AB = Q_R", "WAITING_FOR_PARENT_QRHAT"],
            "spherical exterior current shape and finite q_Rhat guardrail.",
        ),
        (
            "SRC2081_04_1244_GM",
            OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            ["GM1244_0_qR_definition", "q_R_hat = Q_R c^2/(G M_source)", "CONVENTION_DECLARED_NONCLAIM"],
            "dimensionless q_R_hat convention and GM/source convention.",
        ),
        (
            "SRC2081_05_1244_policy",
            OUT / "P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            ["RPF1244_0_policy", "4.6e-05", "MISSING_QR_VALUE_UNCHANGED"],
            "policy feed: external q_R ceiling but missing MTS q_R value.",
        ),
        (
            "SRC2081_06_1255_ceiling",
            ROOT / "1255-Y5-R10-qRhat-source-hunt-or-parent-Hcore-reentry.md",
            ["abs(q_R_hat) <= 4.6e-5", "READY_NONCLAIM_NUMERIC_PASS", "not an MTS prediction"],
            "Cassini q_Rhat ceiling as nonclaim comparator only.",
        ),
        (
            "SRC2081_07_1521_bridge",
            ROOT / "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md",
            ["QBRG1521_3_same_normalization", "QLOC_TO_QR_BRIDGE_NOT_PROVED", "Do not import the q_R guardrail into q_loc"],
            "q_loc to q_R bridge is not proved.",
        ),
        (
            "SRC2081_08_1172_trace",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["HBP1172_2_trace_to_boundary", "C_trace(D,gamma)", "MISSING_TRACE_CONSTANT"],
            "trace theorem grammar available but missing domain constant.",
        ),
        (
            "SRC2081_09_2062_orientation",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "MISSING_ORIENTATION_CONVENTION", "CONDITIONAL_PROOF_ONLY"],
            "orientation/boundary/corner grammar still unsigned.",
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


def bridge_formula_rows() -> list[dict[str, object]]:
    return [
        row(
            formula_id="KQR2081_0_exterior_hair",
            object="exterior reciprocal charge",
            statement="in the q_R convention, R_AB=-Q_R/r plus reference offset gives q_R_hat=Q_R*c^2/(G*M_source)",
            derived_or_conditional="CONVENTION_AVAILABLE_NONCLAIM",
            required_inputs="source body; measured GM_source; sign/orientation; exterior scalar channel selection",
            claim_allowed=False,
        ),
        row(
            formula_id="KQR2081_1_trace_extraction",
            object="Dirichlet/trace extraction candidate",
            statement="if ||R_AB||_{L2(S_ext)} <= C_trace_out*X_E and R_AB=-Q_R/r_ext on S_ext, then |Q_R| <= (r_ext/sqrt(area_ext))*C_trace_out*X_E",
            derived_or_conditional="CONDITIONAL_BOUND_DERIVED",
            required_inputs="S_ext; area_ext; r_ext; C_trace_out; same R_AB component; reference subtraction",
            claim_allowed=False,
        ),
        row(
            formula_id="KQR2081_2_flux_extraction",
            object="Neumann/flux extraction candidate",
            statement="if |Q_R| <= C_flux_out*X_E from the normal flux trace of Pi_R^n, then q_R_hat <= (c^2/(G*M_source))*C_flux_out*X_E",
            derived_or_conditional="CONDITIONAL_BOUND_DERIVED",
            required_inputs="Pi_R^n normalization; Z_R convention; flux trace constant; orientation; boundary class",
            claim_allowed=False,
        ),
        row(
            formula_id="KQR2081_3_KqR_definition",
            object="K_qR",
            statement="K_qR := (c^2/(G*M_source))*C_QX, where C_QX maps X_E to |Q_R| by trace or flux extraction",
            derived_or_conditional="EXACT_BRIDGE_FORMULA_VALUES_MISSING",
            required_inputs="C_QX; GM_source; source body; exterior channel; sign and no-cancellation guards",
            claim_allowed=False,
        ),
        row(
            formula_id="KQR2081_4_pressure_join",
            object="2080 pressure inequality",
            statement="(c^2/(G*M_source))*C_QX*0.5*(a+sqrt(a^2+4*F_outer_abs)) <= 4.6e-05",
            derived_or_conditional="PRESSURE_JOIN_DERIVED_INPUTS_MISSING",
            required_inputs="C_QX plus 2080 finite inputs: C_Poincare,C_trace,rho_R_norm,b_C_norm,F_outer_abs",
            claim_allowed=False,
        ),
    ]


def bridge_clause_audit_rows() -> list[dict[str, object]]:
    specs = [
        (
            "BCA2081_0_exterior_channel",
            "same exterior scalar R_AB channel",
            "finite X_E controls the reciprocal field component whose exterior monopole is Q_R",
            "R_AB channel appears in 1253/1256",
            "X_E-to-R_AB component/projector is not specified",
            "MISSING_COMPONENT_PROJECTOR",
        ),
        (
            "BCA2081_1_outer_surface",
            "outer extraction surface S_ext",
            "declared sphere/worldtube surface with radius, area, normal, reference subtraction",
            "q_R convention requires an exterior 1/r coefficient",
            "S_ext/r_ext/area_ext/orientation are missing",
            "MISSING_OUTER_SURFACE_GEOMETRY",
        ),
        (
            "BCA2081_2_CQX_trace",
            "C_QX by trace",
            "C_QX=(r_ext/sqrt(area_ext))*C_trace_out in the Dirichlet extraction route",
            "trace-theorem grammar exists from 1172",
            "C_trace_out and same-domain norm link are missing",
            "MISSING_TRACE_EXTRACTION_CONSTANT",
        ),
        (
            "BCA2081_3_CQX_flux",
            "C_QX by flux",
            "C_QX=C_flux_out when energy norm controls the normal reciprocal flux/current",
            "1256 gives r^2 Z_R partial_r R_AB = Q_R conditionally",
            "Z_R/Pi_R^n normalization and flux trace bound are missing",
            "MISSING_FLUX_EXTRACTION_CONSTANT",
        ),
        (
            "BCA2081_4_GM",
            "GM_source convention",
            "q_R_hat=Q_R*c^2/(G*M_source) with measured source GM from the same weak-field comparator",
            "1244 declares convention",
            "actual source row remains convention-only until source body/value/provenance is selected",
            "GM_CONVENTION_DECLARED_VALUE_STILL_NEEDED_FOR_RAW_QR",
        ),
        (
            "BCA2081_5_q_loc_bridge",
            "q_loc to q_R bridge",
            "finite q_loc residual reduces to the same exterior q_R scalar hair with same normalization",
            "1521 names exact bridge clauses",
            "QLOC_TO_QR_BRIDGE_NOT_PROVED",
            "MISSING_QLOC_TO_QR_BRIDGE",
        ),
        (
            "BCA2081_6_retained_channels",
            "no-cancellation retained-channel guard",
            "DeltaK, boundary, source, vector/gauge, matter-normalization channels are zero-derived or separately bounded",
            "1521 and 2080 keep no-cancellation guard active",
            "retained channels are not all silenced or bounded in the same arena",
            "MISSING_RETAINED_CHANNEL_SILENCE",
        ),
        (
            "BCA2081_7_policy_ceiling",
            "q_R_hat ceiling",
            "external comparator abs(q_R_hat)<=4.6e-05",
            "1255 supplies source-backed nonclaim ceiling",
            "ceiling cannot create K_qR or q_R_hat_predicted",
            "SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY",
        ),
    ]
    rows = []
    for audit_id, clause, requirement, positive_support, obstruction, status in specs:
        rows.append(
            row(
                audit_id=audit_id,
                clause=clause,
                requirement=requirement,
                positive_support=positive_support,
                obstruction=obstruction,
                status=status,
                source_ready=status == "SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY",
                bridge_pass=False,
                claim_allowed=False,
            )
        )
    return rows


def source_pack_rows() -> list[dict[str, object]]:
    specs = [
        ("PACK2081_0_CQX_trace", "C_QX_trace", "highest", "derive/source outer trace extraction constant from X_E to |Q_R|", "S_ext;r_ext;area_ext;C_trace_out;component_projector;reference_subtraction"),
        ("PACK2081_1_CQX_flux", "C_QX_flux", "highest", "derive/source normal flux extraction constant from X_E to |Q_R|", "Pi_R^n;Z_R;normal_orientation;flux_trace_constant;boundary_class"),
        ("PACK2081_2_GM", "GM_source", "high", "bind q_R_hat normalization to source body and measured GM convention", "source_body;GM_source;coordinate_convention;provenance"),
        ("PACK2081_3_domain", "domain/norm metadata", "high", "make 2080 and K_qR use the same local domain/norm/surface family", "domain_id;norm_id;boundary_id;outer_surface_id"),
        ("PACK2081_4_finite_inputs", "2080 finite inputs", "medium", "source C_Poincare,C_trace,rho_R_norm,b_C_norm,F_outer_abs after K_qR map shape is fixed", "C_Poincare;C_trace;rho_R_norm;b_C_norm;F_outer_abs"),
        ("PACK2081_5_retained_channels", "no-cancellation ledger", "medium", "zero-bound or separately bound channels not represented by q_R_hat", "DeltaK;boundary;source;vector_gauge;matter_normalization"),
        ("PACK2081_6_ceiling", "q_R_hat_policy_ceiling", "available", "retain external comparator as nonclaim pressure target", "4.6e-05;source path;policy row"),
    ]
    rows = []
    for row_id, quantity, priority, objective, required_fields in specs:
        rows.append(
            row(
                row_id=row_id,
                quantity=quantity,
                priority=priority,
                objective=objective,
                required_fields=required_fields,
                current_status="SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY" if row_id == "PACK2081_6_ceiling" else "MISSING",
                source_ready=row_id == "PACK2081_6_ceiling",
                score_ready=False,
                claim_allowed=False,
            )
        )
    return rows


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2081_0_KqR_bridge",
            target="compute K_qR=(c^2/(GM_source))*C_QX",
            input_status="REFUSED_MISSING_BRIDGE_INPUTS",
            missing_inputs="C_QX;GM_source;outer_surface;component_projector;q_loc_to_qR_bridge;retained_channel_silence",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2081_1_trace_route",
            target="Dirichlet trace extraction route",
            input_status="REFUSED_MISSING_TRACE_EXTRACTION",
            missing_inputs="S_ext;r_ext;area_ext;C_trace_out;R_AB component projector",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2081_2_flux_route",
            target="Neumann flux extraction route",
            input_status="REFUSED_MISSING_FLUX_EXTRACTION",
            missing_inputs="Pi_R^n;Z_R;normalization;flux trace bound;orientation",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
    ]


def pressure_rows() -> list[dict[str, object]]:
    return [
        row(
            pressure_id="PRESS2081_0_KqR_definition",
            target="K_qR",
            inequality_or_formula="K_qR=(c^2/(G*M_source))*C_QX",
            known_numeric="q_R_hat_policy_ceiling=4.6e-05 only",
            missing_inputs="C_QX;GM_source;source_body;orientation;exterior_channel",
            status="FORMULA_READY_INPUTS_MISSING",
            claim_allowed=False,
        ),
        row(
            pressure_id="PRESS2081_1_joined_2080",
            target="full finite branch pressure",
            inequality_or_formula="(c^2/(G*M_source))*C_QX*0.5*(a+sqrt(a^2+4*F_outer_abs)) <= 4.6e-05",
            known_numeric="q_R_hat_policy_ceiling=4.6e-05 only",
            missing_inputs="C_QX;GM_source;C_Poincare;C_trace;rho_R_norm;b_C_norm;F_outer_abs",
            status="JOINED_PRESSURE_READY_INPUTS_MISSING",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="GATE2081_0_formula",
            condition="K_qR formula is explicit",
            status="PASS_SYMBOLIC_ONLY",
            reason="K_qR=(c^2/(GM_source))*C_QX is now the bridge target",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2081_1_CQX",
            condition="C_QX source maps X_E to |Q_R|",
            status="FAIL_BLOCKED",
            reason="trace/flux extraction constants and component projector are missing",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2081_2_GM",
            condition="GM_source/source body is source-bound for raw Q_R normalization",
            status="FAIL_BLOCKED",
            reason="1244 declares convention but no K_qR source row binds a measured GM/source body",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2081_3_q_loc_bridge",
            condition="q_loc/q_R bridge is proved",
            status="FAIL_BLOCKED",
            reason="1521 keeps bridge missing and forbids importing q_R guardrail into q_loc",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2081_4_runner_score",
            condition="finite branch can compute q_R_hat_predicted",
            status="FAIL_REFUSED",
            reason="K_qR is formula-only and 2080 finite inputs are still missing",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2081_5_local_claim",
            condition="local GR/Newton/PPN claim",
            status="FAIL_BLOCKED",
            reason="no K_qR value and no q_R_hat prediction",
            claim_allowed=False,
        ),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2081_0_bridge_formula",
            decision="K_qR bridge formula is sharpened",
            because="the missing map is exactly C_QX from energy norm X_E to exterior reciprocal charge Q_R, followed by q_R_hat=Q_R c^2/(GM_source)",
            next_action="do not re-derive q_R_hat convention; source C_QX/GM/exterior surface",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2081_1_trace_vs_flux",
            decision="two viable K_qR extraction routes remain",
            because="trace extraction uses boundary value R_AB on S_ext; flux extraction uses Pi_R^n or r^2 Z_R partial_r R_AB",
            next_action="try outer-surface trace/flux source pack before source norms",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2081_2_bridge_blocked",
            decision="current corpus cannot score K_qR",
            because="C_QX, outer surface, component projector, GM source binding, q_loc bridge, and retained-channel silence are missing",
            next_action="build 2082 outer extraction source pack",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2081_0_2082",
            target_doc="2082-Y5-R2FR-CQX-outer-trace-flux-extraction-source-pack-or-domain-demotion.md",
            objective="derive/source C_QX, the extraction constant from finite reciprocal energy norm X_E to exterior charge |Q_R|, by either outer trace extraction or normal flux extraction; if blocked, demote K_qR to formula-only and prioritize domain/norm constants",
            must_include="outer surface S_ext; area/radius/normal; R_AB component projector; trace route C_QX=(r/sqrt(area))*C_trace_out; flux route Pi_R^n/Z_R normalization; GM/source-body binding; no-cancellation retained-channel guard",
            exclusions="using Cassini ceiling as prediction; q_R_hat=0 closure; importing q_loc->q_R without proof; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    formulas: list[dict[str, object]],
    audit: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2081_0_source_weight_KqR",
            SOURCE_WEIGHT_DOCS / "AFRAME_KQR_EXTERIOR_HAIR_BRIDGE_2081_NONCLAIM.csv",
            formulas + audit + dry,
        ),
        (
            "COPY2081_1_wep_KqR",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2081_KQR_BRIDGE_NONCLAIM.csv",
            formulas + dry,
        ),
        (
            "COPY2081_2_queue_CQX",
            QUEUE / "JR2081_CQX_KQR_SOURCE_PACK_QUEUE.csv",
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


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid"}


def validation_rows(
    sources: list[dict[str, object]],
    formulas: list[dict[str, object]],
    audit: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    pressure: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formula_ok = any(r["formula_id"] == "KQR2081_3_KqR_definition" for r in formulas)
    trace_route_ok = any(r["formula_id"] == "KQR2081_1_trace_extraction" for r in formulas)
    flux_route_ok = any(r["formula_id"] == "KQR2081_2_flux_extraction" for r in formulas)
    audit_blocked = all(not truthy(r.get("bridge_pass")) for r in audit)
    ceiling_retained = any(r["status"] == "SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY" for r in audit)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in dry)
    pressure_ok = any(r["pressure_id"] == "PRESS2081_1_joined_2080" for r in pressure)
    gates_blocked = all(not truthy(r.get("claim_allowed")) for r in gates)
    pack_ok = any(r["row_id"] == "PACK2081_0_CQX_trace" for r in pack) and any(r["row_id"] == "PACK2081_1_CQX_flux" for r in pack)
    next_ok = next_rows_[0]["target_id"] == "NEXT2081_0_2082"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [formulas, audit, pack, dry, pressure, gates, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2081_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2081_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2081_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2081_02_KqR_formula", formula_ok, "K_qR bridge formula is explicit"),
        ("VAL2081_03_trace_route", trace_route_ok, "trace extraction route is written"),
        ("VAL2081_04_flux_route", flux_route_ok, "flux extraction route is written"),
        ("VAL2081_05_audit_blocked", audit_blocked, "bridge clauses remain blocked/nonclaim"),
        ("VAL2081_06_ceiling_retained", ceiling_retained, "q_R ceiling retained only as comparator"),
        ("VAL2081_07_dry_refusal", dry_refused, "dry runs refuse missing bridge inputs"),
        ("VAL2081_08_pressure_join", pressure_ok, "joined 2080 pressure formula includes K_qR"),
        ("VAL2081_09_claim_gates_blocked", gates_blocked, "claim gates remain blocked"),
        ("VAL2081_10_pack_ready", pack_ok, "C_QX trace/flux source pack rows exist"),
        ("VAL2081_11_next_selected", next_ok, "2082 C_QX extraction target selected"),
        ("VAL2081_12_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2081_13_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2081_14_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2081_15_no_formalization_artifacts", no_formalization_artifacts, "no 2081 artifacts were written under formalization-workbench"),
        ("VAL2081_16_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2081_OVERALL", overall, "2081 derives K_qR bridge formula, blocks scoring, and selects C_QX extraction source pack"))
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
    formulas: list[dict[str, object]],
    audit: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    pressure: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2081 Y5 R2FR KqR exterior hair normalization bridge or finite input priority source pack",
        "",
        "## Current Verdict",
        "",
        "2081 sharpens `K_qR` into the exact missing bridge:",
        "`K_qR := (c^2/(G*M_source))*C_QX`, where `C_QX` maps the finite reciprocal energy norm `X_E` to the exterior charge magnitude `|Q_R|`.",
        "",
        "Two conditional extraction routes are now explicit. The trace route uses `R_AB=-Q_R/r` on an outer surface and gives `|Q_R| <= (r_ext/sqrt(area_ext))*C_trace_out*X_E`. The flux route uses the normal reciprocal current, schematically `r^2 Z_R partial_r R_AB = Q_R`, and needs a flux trace constant.",
        "",
        "The current corpus does not supply `C_QX`, the outer surface geometry, component projector, flux/trace constant, GM source binding, q_loc-to-q_R bridge, or retained-channel silence. Therefore `K_qR` is formula-only and the finite branch still cannot score.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## Bridge Formulae",
        md_table(formulas, ["formula_id", "object", "statement", "derived_or_conditional", "required_inputs", "claim_allowed", "valid_for_claim"]),
        "## Bridge Clause Audit",
        md_table(audit, ["audit_id", "clause", "requirement", "positive_support", "obstruction", "status", "source_ready", "bridge_pass", "claim_allowed", "valid_for_claim"]),
        "## Priority Source Pack",
        md_table(pack, ["row_id", "quantity", "priority", "objective", "required_fields", "current_status", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry, ["run_id", "target", "input_status", "missing_inputs", "K_qR_value", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
        "## Pressure Join",
        md_table(pressure, ["pressure_id", "target", "inequality_or_formula", "known_numeric", "missing_inputs", "status", "claim_allowed", "valid_for_claim"]),
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
    formulas = bridge_formula_rows()
    audit = bridge_clause_audit_rows()
    pack = source_pack_rows()
    dry = dry_run_rows()
    pressure = pressure_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2081_SOURCE_REGISTER.csv",
        "formulas": OUT / "P8_Y5_PARENT_QLOC_2081_KQR_BRIDGE_FORMULAE.csv",
        "audit": OUT / "P8_Y5_PARENT_QLOC_2081_BRIDGE_CLAUSE_AUDIT.csv",
        "pack": OUT / "P8_Y5_PARENT_QLOC_2081_PRIORITY_SOURCE_PACK.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2081_DRY_RUN.csv",
        "pressure": OUT / "P8_Y5_PARENT_QLOC_2081_PRESSURE_JOIN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2081_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2081_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2081_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2081_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2081_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["formulas"], formulas)
    write_csv(paths["audit"], audit)
    write_csv(paths["pack"], pack)
    write_csv(paths["dry"], dry)
    write_csv(paths["pressure"], pressure)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(formulas, audit, pack, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, formulas, audit, pack, dry, pressure, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, formulas, audit, pack, dry, pressure, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
