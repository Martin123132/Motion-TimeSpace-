from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3646"
BRANCH_ID = "MTS_R2FR_Y5_MATTER_COUPLING_DESCENT_OR_FIRST_BETA_SOURCE_ROW_3646"
DOC = ROOT / "3646-Y5-R2FR-matter-coupling-descent-or-first-beta-source-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3646_SOURCE_REGISTER.csv",
        "descent_theorem": RESIDUALS / "P8_Y5_R2FR_3646_MATTER_DESCENT_THEOREM_ATTEMPT.csv",
        "clause_audit": RESIDUALS / "P8_Y5_R2FR_3646_MATTER_DESCENT_CLAUSE_AUDIT.csv",
        "beta_rows": RESIDUALS / "P8_Y5_R2FR_3646_FIRST_BETA_SOURCE_ROWS.csv",
        "material_schema": RESIDUALS / "P8_Y5_R2FR_3646_MATERIAL_CHANNEL_SCHEMA.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3646_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3646_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3646_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3646_VALIDATION.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3645", RESIDUALS / "P8_Y5_R2FR_3645_NEXT_TARGET.csv", "matter-coupling-descent", "3645 handoff to matter descent/beta source rows"),
        ("jx_3645", RESIDUALS / "P8_Y5_R2FR_3645_JX_VARIATION_DERIVATION.csv", "JXD3645_3_quotient_zero_gate", "3645 quotient-zero source current gate"),
        ("obs_637", RESIDUALS / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv", "OF637_1_chain_rule", "637 observed functor chain-rule theorem"),
        ("qmap_637", RESIDUALS / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv", "QM637_2_vertical_kernel", "637 quotient kernel condition"),
        ("qvx_1023", ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md", "QVC1023_3_matter_descent", "1023 q/vX/matter descent failure audit"),
        ("qbar_1027", ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md", "QZ1027_0_chain_rule", "1027 qbarXT source-zero chain rule"),
        ("matter_pullback_1044", ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md", "MPD1044_8_current_verdict", "1044 matter pullback verdict"),
        ("matter_functor_1045", ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md", "DEC1045_0_theorem_shape", "1045 parent matter functor theorem shape"),
        ("no_shadow_1046", ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md", "Current verdict", "1046 no-shadow/no-marker theorem status"),
        ("beta_1036", RESIDUALS / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv", "BETA1036_4_quotient_zero", "1036 beta source/test split"),
        ("bounded_beta_1037", RESIDUALS / "P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv", "BB1037_7_beta_product_guard", "1037 bounded beta component template"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def descent_theorem_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False}
    return [
        {
            **base,
            "theorem_id": "MDT3646_0_statement",
            "claim": "Matter coupling zero theorem.",
            "hypotheses": "S_matter=Sbar_m[Obs(q(Phi)),Psi,theta_A]; v_X in ker(Dq); DObs(Dq[v_X])=0; Lie_vX theta_A=0; no hidden conformal/disformal matter frame; no material marker or post-readout source weight sees X_N.",
            "derivation": "delta_vX S_matter=(delta Sbar/dObs) DObs(Dq[v_X]) + sum_A (partial Sbar/partial theta_A) Lie_vX theta_A + shadow/marker terms.",
            "result": "If every hypothesis holds in the same parent branch, delta_vX S_matter=0, J_X^matter=0, beta_i=0, and qbar_XT=0.",
            "status": "EXACT_CHAIN_RULE_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent q-kernel, observed geometry/coframe functor, matter functor, no-shadow frame, no-marker constants/materials, and hidden-source silence",
        },
        {
            **base,
            "theorem_id": "MDT3646_1_metric_frame_part",
            "claim": "Metric/coframe matter variation cancels if observed geometry is a quotient functor.",
            "hypotheses": "g_obs/e_obs/omega_obs = Obs(q(Phi)) and v_X in ker(Dq).",
            "derivation": "partial_X g_obs = DObs_g(Dq[v_X])=0 and partial_X e_obs=DObs_e(Dq[v_X])=0.",
            "result": "The Hilbert stress channel gives no J_X^matter contribution from geometry under quotient descent.",
            "status": "MATH_PASS_NEEDS_PARENT_OBS_SIGNATURE",
            "missing_for_claim": "Obs_g/Obs_e parent selection and no representative frame leakage",
        },
        {
            **base,
            "theorem_id": "MDT3646_2_constants_marker_part",
            "claim": "Constants/material markers are the dangerous non-geometric source channel.",
            "hypotheses": "theta_A are fixed representation data or quotient functions with Lie_vX theta_A=0.",
            "derivation": "sum_A (partial Sbar/partial theta_A) Lie_vX theta_A vanishes iff every theta_A is X-blind in the parent branch.",
            "result": "If alpha_EM(X), masses, clock ratios, material labels, or binding fractions carry X_N dependence, beta_i is nonzero even with quotient geometry.",
            "status": "COUNTERMODEL_CLASS_IDENTIFIED",
            "missing_for_claim": "no-marker theorem or coefficient rows b_A, b_alpha, b_mass, b_clock with source paths",
        },
        {
            **base,
            "theorem_id": "MDT3646_3_shadow_frame_part",
            "claim": "Universal shadow-frame coupling can evade WEP-looking tests but still source R10/PPN.",
            "hypotheses": "ordinary matter uses g_m=A_g(X_N)^2 g_obs + B_dis(X_N) dX_N dX_N or equivalent frame.",
            "derivation": "beta_i receives d ln A_g/dX_N plus disformal/readout pieces common to source and test legs.",
            "result": "Universal coupling is not automatically safe; it tends to enter finite exchange as beta_s beta_t or c_g^2.",
            "status": "LIVE_COUNTERMODEL_OR_BOUND_ROW",
            "missing_for_claim": "no-shadow-frame theorem or c_g/b_dis numeric/source rows",
        },
        {
            **base,
            "theorem_id": "MDT3646_4_fallback_beta_definition",
            "claim": "If the theorem is unsigned, beta is the honest object to test.",
            "hypotheses": "m_i^eff=m_i^eff(Xhat, material, readout, constants, hidden support).",
            "derivation": "beta_i := partial_Xhat ln m_i^eff = beta_geom + beta_shadow + beta_marker + beta_binding + beta_nonH + beta_projector.",
            "result": "|beta_i| is bounded by an absolute component envelope; no cancellation between unknown components is credited.",
            "status": "BETA_FALLBACK_DERIVED",
            "missing_for_claim": "component theorem-zero rows or numeric bounds with source paths",
        },
    ]


def clause_audit_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}
    specs = [
        ("MDC3646_0_q_kernel", "v_X in ker(Dq)", "QM637_2 gives conditional math-pass", "MISSING_PARENT_Q_KERNEL_FOR_ACTUAL_XN", "needed for geometric descent"),
        ("MDC3646_1_obs_geometry", "Obs_g/Obs_e factor through q", "OF637 chain rule gives exact shape", "MISSING_OBS_GEOMETRY_PARENT_SIGNATURE", "kills metric/coframe Hilbert-stress source"),
        ("MDC3646_2_matter_functor", "S_matter=Sbar_m[Obs(q(Phi)),Psi,theta]", "1045 has theorem shape", "MISSING_PARENT_MATTER_FUNCTOR", "turns ordinary matter into quotient pullback"),
        ("MDC3646_3_no_shadow_frame", "no A_g(X), B_dis(X), or hidden matter frame", "1046 identifies countermodels", "MISSING_NO_SHADOW_FRAME_THEOREM_OR_COEFFICIENTS", "blocks universal c_g/b_dis leakage"),
        ("MDC3646_4_no_marker_constants", "Lie_vX theta_A=0 for masses, alpha_EM, clocks, materials", "1027/1046 mark it unsigned", "MISSING_NO_MARKER_THEOREM_OR_COEFFICIENTS", "blocks material/composition beta"),
        ("MDC3646_5_hidden_source_silence", "no hidden/source/domain support in ordinary body action", "3645 isolates hidden/domain current", "MISSING_HIDDEN_SOURCE_SILENCE", "blocks non-Hilbert beta/source current"),
        ("MDC3646_6_projector_readout", "calibration/readout fixed before X variation", "1009/3645 isolate projector debt", "MISSING_PROJECTOR_READOUT_SIGNATURE", "blocks post-readout beta"),
        ("MDC3646_7_same_branch", "all clauses close in one parent branch", "1023 rejects stitched certificate", "MISSING_SINGLE_PARENT_BRANCH_CERTIFICATE", "prevents ladder magic from mixed checkpoints"),
    ]
    return [
        {
            **base,
            "clause_id": cid,
            "clause": clause,
            "current_evidence": evidence,
            "current_status": status,
            "why_it_matters": why,
        }
        for cid, clause, evidence, status, why in specs
    ]


def beta_rows(ts: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    specs = [
        ("BETA3646_0_theorem_zero", "source_and_test", "beta_i_zero", "beta_i=0 if matter descent/no-shadow/no-marker theorem is parent-signed", "parent theorem certificate path", "MISSING_PARENT_THEOREM_CERTIFICATE", "all local arenas"),
        ("BETA3646_1_geom_shadow", "source_or_test", "beta_geom_shadow", "|beta_geom_shadow| <= |c_g| + |b_dis|*|tau_dis| + frame profile terms", "no-shadow theorem or c_g/b_dis bounds", "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND", "R10;PPN;WEP;clock"),
        ("BETA3646_2_constants_marker", "source_or_test", "beta_marker", "|beta_marker| <= sum_A |S_A b_A| + |S_alpha b_alpha| + |S_clock b_clock|", "no-marker theorem or constants/material coefficients", "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS", "WEP;clock;composition;R10"),
        ("BETA3646_3_binding_material", "source_or_test", "beta_binding", "|beta_binding| <= sum_k |f_k b_k| for nuclear/EM/binding material fractions", "composition sensitivities and binding coefficient rows", "MISSING_MATERIAL_SENSITIVITY_ROWS", "WEP;clock;R10 material dependence"),
        ("BETA3646_4_nonH_source", "source_or_test", "beta_nonH", "|beta_nonH| <= |q_nonH|+|q_domain|+|q_boundary|+|support_shift|", "hidden/source/domain/boundary silence theorem or numeric bounds", "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND", "orbital;R10;local_GR"),
        ("BETA3646_5_projector_readout", "source_or_test", "beta_projector", "|beta_projector| <= |delta_X Pi_M|+|delta_X P_loc|+|delta_X calibration|", "projector/readout variation fixed before calibration", "MISSING_PROJECTOR_READOUT_BOUND", "PPN;GM calibration;clock"),
        ("BETA3646_6_abs_total", "source_and_test", "beta_s_abs;beta_t_abs", "beta_abs=sum_components |beta_component|", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all local arenas"),
        ("BETA3646_7_product_guard", "source_times_test", "abs_beta_product", "|beta_s beta_t| <= beta_s_abs beta_t_abs; universal Weyl contributes through c_g^2 unless packed into source leg", "beta_s_abs;beta_t_abs;normalization convention", "CLAIM_BLOCKED", "R10;PPN;WEP;clock;orbital"),
    ]
    return [
        {
            **base,
            "beta_id": bid,
            "leg": leg,
            "symbol": symbol,
            "formula_or_bound": formula,
            "required_inputs": required,
            "current_status": status,
            "observable_links": links,
        }
        for bid, leg, symbol, formula, required, status, links in specs
    ]


def material_schema_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "score_ready": False}
    specs = [
        ("MAT3646_0_body_id", "body_id", True, "identifier", "source/test body or material row id", "REQUIRED"),
        ("MAT3646_1_role", "role", True, "source/test/both", "which beta leg the row fills", "REQUIRED"),
        ("MAT3646_2_material", "material_or_body_class", True, "text", "material/body composition class; no generic beta without material/readout declaration", "REQUIRED_MISSING_VALUES"),
        ("MAT3646_3_sensitivities", "S_A;S_alpha;S_clock;f_binding", True, "dimensionless", "composition/constant sensitivity vector", "REQUIRED_MISSING_VALUES"),
        ("MAT3646_4_coefficients", "c_g;b_dis;b_A;b_alpha;b_clock;q_nonH", True, "dimensionless_or_declared", "MTS-side coupling coefficients or theorem-zero certificates", "REQUIRED_MISSING_VALUES"),
        ("MAT3646_5_beta_components", "beta_geom_shadow;beta_marker;beta_binding;beta_nonH;beta_projector", True, "dimensionless", "component beta values/bounds", "REQUIRED_MISSING_VALUES"),
        ("MAT3646_6_source_paths", "source_paths", True, "paths/URLs", "source for every sensitivity, coefficient, and theorem-zero certificate", "REQUIRED_FOR_ANY_CLAIM"),
        ("MAT3646_7_guard", "absolute_no_cancellation", True, "bool", "components add by absolute envelope, not cancellation", "REQUIRED_TRUE"),
    ]
    return [
        {
            **base,
            "schema_id": sid,
            "field": field,
            "required": required,
            "units": units,
            "description": description,
            "current_status": status,
        }
        for sid, field, required, units, description, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False}
    return [
        {
            **base,
            "decision_id": "DEC3646_0_theorem_attempt",
            "decision": "The matter-coupling zero theorem is mathematically clean by chain rule.",
            "status": "THEOREM_SHAPE_EXACT",
        },
        {
            **base,
            "decision_id": "DEC3646_1_current_verdict",
            "decision": "It is not a current MTS claim because observed geometry, matter functor, no-shadow frame, no-marker constants, hidden source silence, and projector readout are not signed in one parent branch.",
            "status": "PARENT_SIGNATURE_UNSIGNED",
        },
        {
            **base,
            "decision_id": "DEC3646_2_fallback",
            "decision": "First beta/source rows are created as nonclaim rows; they make coupling testable instead of hand-waved.",
            "status": "BETA_ROWS_CREATED_NOT_SCORE_READY",
        },
        {
            **base,
            "decision_id": "DEC3646_3_best_next",
            "decision": "Attack no-shadow observed frame first, because a universal A_g(X) or disformal matter frame can mimic WEP safety while still sourcing finite exchange.",
            "status": "OBS_FRAME_NO_SHADOW_OR_COEFFICIENTS_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "MATTER_DESCENT_THEOREM_CONDITIONAL_BETA_ROWS_CREATED",
            "summary": "3646 proves the matter-coupling zero route as an exact conditional chain-rule theorem, rejects current claim status because parent signatures are missing, and creates first R2FR beta/source rows with absolute no-cancellation guards.",
            "claim_ceiling": "no J_X^matter=0, beta_i=0, qbar_XT=0, local-GR/Newton, R10, PPN, clock, orbital, or WEP pass is claimed",
            "useful_result": "the next fight is narrowed to no-shadow observed frame/no-marker constants or sourced beta coefficients",
            "valid_for_claim": False,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3646_0",
            "target_doc": "3647-Y5-R2FR-observed-frame-no-shadow-theorem-or-cg-bdis-coefficient-row.md",
            "target_script": "scripts/Y5_R2FR_3647_observed_frame_no_shadow_theorem_or_cg_bdis_coefficient_row.py",
            "objective": "prove ordinary matter uses only the quotient observed frame with no A_g(X_N), B_dis(X_N), or post-readout frame leakage; if unsigned, create c_g and b_dis source rows with observable links",
            "success_gate": "either no-shadow observed frame is parent-signed, or c_g/b_dis rows have units, source paths, arena projections, and no-cancellation guards",
            "valid_for_claim": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_doc(
    src: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    beta: list[dict[str, object]],
    schema: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    lines = [
        "# 3646 Y5 R2FR matter coupling descent or first beta source row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "**Claim ceiling:** no coupling-zero, beta-zero, local-GR/Newton, R10, PPN, clock, orbital, or WEP pass is claimed.",
        "",
        "## Theorem attempt",
        "",
        "The clean route is exact but conditional:",
        "",
        "`S_matter=Sbar_m[Obs(q(Phi)),Psi,theta_A]`, `v_X in ker(Dq)`, `DObs(Dq[v_X])=0`, and `Lie_vX theta_A=0` imply `J_X^matter=0` and `beta_i=0`, provided there is no hidden conformal/disformal matter frame or material marker depending on `X_N`.",
        "",
        "This is useful because it says exactly what must be derived; it is not a closure axiom.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} — {row['result']}")
    lines.extend(["", "## Clause audit"])
    for row in audit:
        lines.append(f"- `{row['clause_id']}`: `{row['clause']}` — {row['current_status']}")
    lines.extend(["", "## First beta/source rows"])
    for row in beta:
        lines.append(f"- `{row['beta_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Material schema"])
    for row in schema:
        lines.append(f"- `{row['field']}`: {row['current_status']} — {row['description']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} — {row['decision']}")
    lines.extend(["", "## Next target", "", f"`{nxt[0]['target_doc']}` via `{nxt[0]['target_script']}`.", "", "## Sources"])
    for row in src:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['source_exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(out: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    ts = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3646_0_sources_exist", all(bool(row["source_exists"]) for row in src), "all source paths exist")
    add("VAL3646_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3646_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all outputs and doc written")

    parsed: dict[str, list[dict[str, str]]] = {}
    parse_ok = True
    counts = []
    for name, path in pre.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            parsed[name] = read_csv(path)
            counts.append(f"{name}:{len(parsed[name])}")
        except Exception as exc:  # pragma: no cover - validation path
            parse_ok = False
            counts.append(f"{name}:ERR:{exc}")
    add("VAL3646_3_csv_parse", parse_ok, "; ".join(counts))

    theorem = parsed["descent_theorem"]
    audit = parsed["clause_audit"]
    beta = parsed["beta_rows"]
    schema = parsed["material_schema"]
    decisions = parsed["decisions"]
    status = parsed["status"]
    nxt = parsed["next_target"]
    generated_groups = [theorem, audit, beta, schema, decisions, status, nxt]

    add("VAL3646_4_theorem_statement", any("J_X^matter=0" in row["result"] and "beta_i=0" in row["result"] for row in theorem), "conditional matter zero theorem present")
    required_clauses = {"v_X in ker(Dq)", "Obs_g/Obs_e factor through q", "S_matter=Sbar_m[Obs(q(Phi)),Psi,theta]", "no A_g(X), B_dis(X), or hidden matter frame", "Lie_vX theta_A=0 for masses, alpha_EM, clocks, materials"}
    add("VAL3646_5_clause_audit_complete", required_clauses.issubset({row["clause"] for row in audit}), "q, observed frame, matter functor, no-shadow, and no-marker clauses audited")
    required_betas = {"beta_i_zero", "beta_geom_shadow", "beta_marker", "beta_binding", "beta_nonH", "beta_projector", "beta_s_abs;beta_t_abs", "abs_beta_product"}
    add("VAL3646_6_beta_rows_complete", required_betas.issubset({row["symbol"] for row in beta}), "first beta source/test rows complete")
    required_schema = {"material_or_body_class", "S_A;S_alpha;S_clock;f_binding", "c_g;b_dis;b_A;b_alpha;b_clock;q_nonH", "source_paths", "absolute_no_cancellation"}
    add("VAL3646_7_material_schema_complete", required_schema.issubset({row["field"] for row in schema}), "material schema has sensitivity, coefficient, source, and no-cancellation fields")
    add("VAL3646_8_no_score_ready", all(row.get("score_ready", "False").lower() == "false" for table in [beta, schema] for row in table), "beta/material rows refuse scoring")
    add("VAL3646_9_nonclaim_all_outputs", all(row.get("valid_for_claim", "False").lower() == "false" for table in generated_groups for row in table), "all generated rows remain nonclaim")
    add("VAL3646_10_decision_next", any(row["status"] == "OBS_FRAME_NO_SHADOW_OR_COEFFICIENTS_NEXT" for row in decisions), "observed frame/no-shadow target selected next")
    add("VAL3646_11_next_target_written", bool(nxt) and "3647" in nxt[0]["target_doc"], "3647 target written")
    add("VAL3646_12_status_honest", status[0]["status"] == "MATTER_DESCENT_THEOREM_CONDITIONAL_BETA_ROWS_CREATED", "status keeps theorem conditional and beta rows nonclaim")
    doc_text = DOC.read_text(encoding="utf-8", errors="replace") if DOC.exists() else ""
    add("VAL3646_13_doc_written", "J_X^matter=0" in doc_text and "beta_i=0" in doc_text and "not a closure axiom" in doc_text, "doc records theorem shape and caveat")
    leak_patterns = ["*Y5_R2FR_3646*", "3646-Y5-R2FR-*", "Y5_R2FR_3646_*"]
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in leak_patterns:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3646_14_no_formalization_leak", not leaks, "no 3646 checkpoint files in formalization-workbench")
    add("VAL3646_15_single_branch_guard", any(row["current_status"] == "MISSING_SINGLE_PARENT_BRANCH_CERTIFICATE" for row in audit), "single-parent-branch guard retained")
    add("VAL3646_16_product_guard", any(row["symbol"] == "abs_beta_product" and "beta_s_abs beta_t_abs" in row["formula_or_bound"] for row in beta), "source-test beta product guard present")
    return rows


def main() -> None:
    ts = now()
    out = outputs()
    src = source_register(ts)
    theorem = descent_theorem_rows(ts)
    audit = clause_audit_rows(ts)
    beta = beta_rows(ts)
    schema = material_schema_rows(ts)
    decisions = decision_rows(ts)
    status = status_rows(ts)
    nxt = next_target_rows(ts)

    write_csv(out["source_register"], src)
    write_csv(out["descent_theorem"], theorem)
    write_csv(out["clause_audit"], audit)
    write_csv(out["beta_rows"], beta)
    write_csv(out["material_schema"], schema)
    write_csv(out["decisions"], decisions)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, theorem, audit, beta, schema, decisions, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3646 validation failed: {failures}")
    print(f"wrote 3646 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
