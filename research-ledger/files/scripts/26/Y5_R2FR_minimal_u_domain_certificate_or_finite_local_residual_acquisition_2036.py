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


DOC = ROOT / "2036-Y5-R2FR-minimal-u-domain-certificate-or-finite-local-residual-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2036_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2036*u*domain*")) or any(FORMALIZATION.rglob("*2036*finite*residual*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2036_00_2035_handoff",
            ROOT / "2035-Y5-R2FR-quotient-factorisation-exhaustion-or-row-null-hessian-source.md",
            ["NEXT2035_0_2036", "EXH2035_8_verdict", "VAL2035_OVERALL"],
            "2035 selects narrow u-domain certificate or finite residual acquisition.",
        ),
        (
            "SRC2036_01_2035_next",
            OUT / "P8_Y5_PARENT_QLOC_2035_NEXT_TARGET.csv",
            ["NEXT2035_0_2036"],
            "machine-readable 2036 target.",
        ),
        (
            "SRC2036_02_407_sketch",
            ROOT / "407-primitive-relational-quotient-action-sketch.md",
            ["configuration_space_sketch_written", "matter_quotient_functor_derived", "It does not yet derive those facts."],
            "primitive relational quotient action sketch; best candidate but not theorem.",
        ),
        (
            "SRC2036_03_423_no_extension",
            ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
            ["primitive_universal_property", "parent_universal_property_derived", "local_GR_promoted"],
            "no-extension theorem attempt rejects current derivation.",
        ),
        (
            "SRC2036_04_967_readout",
            ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
            ["RAV967_5_verdict", "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED"],
            "readout-after-variation schema is clean but not parent-signed.",
        ),
        (
            "SRC2036_05_968_domain_csv",
            OUT / "P8_Y5_R10_968_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
            ["PDS968_0_conf_parent_field_list", "PDS968_2_readout_exclusion", "PDS968_6_verdict"],
            "parent-domain signature audit is not parent-signed.",
        ),
        (
            "SRC2036_06_1107_exhaustion_csv",
            OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            ["EXH1107_0_target", "EXH1107_6_verdict", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
            "broad object-language exhaustion remains closure-only.",
        ),
        (
            "SRC2036_07_1023_action_descent",
            ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            ["QVC1023_2_action_descent", "DEC1023_0_certificate_result"],
            "q/v_X/action descent certificate does not close.",
        ),
        (
            "SRC2036_08_1265_auxiliary",
            ROOT / "1265-Y5-R10-RAB-auxiliary-constraint-protection-or-finite-ZR-bound-runner.md",
            ["AP1265_1_no_derivatives", "AET1265_0_auxiliary_elimination", "VAL1265_11_overall"],
            "auxiliary elimination theorem is exact conditional but unsigned.",
        ),
        (
            "SRC2036_09_1789_countermodel",
            ROOT / "1789-Y5-R2FR-no-integrated-out-curvature-tower-or-finite-scalar-bound-pack.md",
            ["CM1789_2_readout_reduced_eft"],
            "readout-reduced EFT countermodel remains live.",
        ),
        (
            "SRC2036_10_1868_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_2_no_independent_RAB", "CPG1868_4_constraint_admission"],
            "candidate no-independent-RAB and Lambda_R admission grammar.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def u_domain_certificate_rows() -> list[dict[str, object]]:
    data = [
        (
            "UDOM2036_0_u_variable",
            "u := R_AB = 2 ln(J_q)",
            "derived reciprocal/readout coordinate to be excluded from parent action arguments except Lambda_R u",
            "DEFINITION_READY",
            "needs parent domain certificate to become theorem-active",
        ),
        (
            "UDOM2036_1_typed_conf_parent",
            "Conf_parent lists primitive relational/coframe/transport/matter/boundary variables and excludes u, Du, readout projectors, and post-readout masks",
            "would remove u from L_phys by domain typing",
            "FAIL_SKETCH_NOT_CLOSED",
            "407 is a configuration-space sketch; 968 says closed Conf_parent is missing",
        ),
        (
            "UDOM2036_2_parent_generate_u",
            "ParentGenerate_u has image {Lambda_R u auxiliary constraint} only; no independent u or Du target exists",
            "would prove the exact branch without scalar hair",
            "FAIL_NO_UNIVERSAL_PROPERTY",
            "423 and 1107 say no universal-property/no-extension theorem is derived",
        ),
        (
            "UDOM2036_3_lambda_origin",
            "Lambda_R u is a parent-owned auxiliary block with preservation, matter descent, and boundary silence",
            "would make u=0 a parent equation rather than closure",
            "FAIL_CONDITIONAL_TEMPLATE",
            "1265/1868 keep Lambda_R admission conditional",
        ),
        (
            "UDOM2036_4_no_Du_constructor",
            "no vertical metric, vertical connection, Sobolev norm, or local invariant can form G_vert(Du,Du)",
            "would force row-null Hessian at tree level",
            "FAIL_UNSIGNED_GRAMMAR",
            "AP1265_1 and CPG1868_3 are unsigned grammar protections",
        ),
        (
            "UDOM2036_5_matter_descent",
            "ordinary matter descends through e_pub/theta and never sees u or hidden species/readout markers",
            "would set J_R=0",
            "FAIL_UNSIGNED_MATTER_FUNCTOR",
            "407/967/968 keep matter and readout clauses conditional",
        ),
        (
            "UDOM2036_6_boundary_readout_stability",
            "boundary/readout/reduced-EFT paths cannot regenerate u after variation",
            "would set Q_R=B_R=0 and prevent post-readout EFT loophole",
            "FAIL_COUNTERMODEL_LIVE",
            "1789 countermodel and 967 reduced-action tax remain live",
        ),
        (
            "UDOM2036_7_certificate_verdict",
            "minimal u-domain certificate is not derived from current corpus",
            "derivation-first on this exact local branch must stop unless a new parent-domain proof is supplied",
            "MINIMAL_U_DOMAIN_CERTIFICATE_NOT_DERIVED",
            "switch to finite local residual acquisition while preserving certificate as theorem target",
        ),
    ]
    rows = []
    for row_id, clause, consequence, status, evidence in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "consequence": consequence,
                "status": status,
                "evidence": evidence,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_acquisition_rows() -> list[dict[str, object]]:
    data = [
        (
            "FACQ2036_0_branch_policy",
            "finite local residual acquisition activates",
            "because UDOM2036_7 rejects the current certificate",
            "ACTIVE_NONCLAIM",
            "not a local-GR failure; it is a demand for values/bounds",
        ),
        (
            "FACQ2036_1_ZRR",
            "Z_RR^{mu nu}",
            "J_u^A Z_AB^{mu nu} J_u^B",
            "MISSING_PARENT_HESSIAN_OR_ZERO_THEOREM",
            "kinetic self-response of reciprocal readout",
        ),
        (
            "FACQ2036_2_ZRY",
            "Z_RY^{mu nu}",
            "J_u^A Z_AB^{mu nu} J_Y^B",
            "MISSING_PARENT_CROSS_HESSIAN_OR_ZERO_THEOREM",
            "cross-response; scalar Z_RR alone is insufficient",
        ),
        (
            "FACQ2036_3_MR2",
            "M_R^2",
            "partial^2 V_eff/partial u^2",
            "MISSING_PARENT_MASS_HESSIAN_OR_ZERO_THEOREM",
            "finite range/screening input",
        ),
        (
            "FACQ2036_4_JR",
            "J_R",
            "[partial L/partial u - nabla_mu partial L/partial(D_mu u)]_0",
            "MISSING_MATTER_CORE_SOURCE_OR_DESCENT_THEOREM",
            "direct local source/fifth-force channel",
        ),
        (
            "FACQ2036_5_QR_BR",
            "Q_R/B_R",
            "Pi_R^n and partial B/partial u",
            "MISSING_BOUNDARY_SOURCE_OR_SILENCE_THEOREM",
            "exterior hair/boundary charge channel",
        ),
        (
            "FACQ2036_6_arena_maps",
            "tau_R10,tau_PPN,tau_clock,tau_orbital",
            "projection maps from residual vector to experiments",
            "MISSING_ARENA_PROJECTIONS",
            "turns finite rows into tests rather than prose",
        ),
        (
            "FACQ2036_7_claim_gate",
            "finite local branch claim",
            "all coefficients/projections sourced, units checked, no-cancellation guard passed",
            "FAIL_BLOCKED",
            "no current local-GR/Newton/R10/PPN/clock/orbital claim",
        ),
    ]
    rows = []
    for row_id, symbol, formula, status, role in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "status": status,
                "role": role,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def accepted_schema_rows() -> list[dict[str, object]]:
    columns = [
        ("symbol", "one of Z_RR,Z_RY,M_R2,J_R,Q_R,B_R,tau_R10,tau_PPN,tau_clock,tau_orbital"),
        ("value", "finite numeric value or theorem_zero=true with parent-signed authority"),
        ("units", "same-frame units; dimensionless normalization if normalized"),
        ("normalization", "definition of u, J_u, Hessian convention, and sign"),
        ("source_path", "existing local path or external source URL/DOI if later acquired"),
        ("equation_ref", "equation/row proving value or bound"),
        ("arena_projection", "R10/PPN/clock/orbital/WEP map if used for a claim"),
        ("no_cancellation_components", "absolute component list before cancellation"),
        ("valid_for_claim", "false until every required field is real and reviewed"),
    ]
    rows = []
    for field, requirement in columns:
        row = base_row()
        row.update(
            {
                "field": field,
                "requirement": requirement,
                "status": "REQUIRED",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def route_decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2036_0_certificate_result",
            "The minimal u-domain certificate does not close.",
            "The corpus has a good sketch and schema theorem, but not the parent universal-property/domain proof needed to remove u and Du as action arguments.",
        ),
        (
            "DEC2036_1_derivation_policy",
            "Stop spending derivation-first credit on this exact local branch until a new parent-domain proof appears.",
            "Continuing to rewrite the same no-u claim would be circular; the responsible next move is finite residual acquisition.",
        ),
        (
            "DEC2036_2_theory_status",
            "The local-GR route is not dead.",
            "It has become a clean conditional theorem plus a concrete finite residual test program.",
        ),
        (
            "DEC2036_3_next_work",
            "Build a finite local residual runner and acquire/source actual coefficient or bound rows.",
            "Start with Z_RR/Z_RY/J_R/Q_R/B_R and then map to R10/PPN/clock/orbital.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2036_0_u_domain_certificate", "minimal u-domain certificate", "FAIL_NOT_DERIVED", "UDOM2036_7"),
        ("GATE2036_1_lambda_origin", "Lambda_R u parent-owned", "FAIL_CONDITIONAL", "Lambda_R block still template/conditional"),
        ("GATE2036_2_no_Du_constructor", "no u/Du action constructor", "FAIL_UNSIGNED", "no-extension/object-language proof missing"),
        ("GATE2036_3_matter_boundary", "J_R=Q_R=B_R=0", "FAIL_UNSIGNED", "matter/boundary/readout stability not signed"),
        ("GATE2036_4_finite_acquisition", "finite residual acquisition active", "PASS_NONCLAIM", "source requirements written"),
        ("GATE2036_5_local_GR_claim", "local GR/Newton/R10/PPN/clock/orbital pass", "FAIL_BLOCKED", "no certificate and no finite bounds"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "status": status,
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2036_0_2037",
            "target_doc": "2037-Y5-R2FR-finite-local-residual-runner-and-bound-map.md",
            "objective": "implement the finite local residual acquisition runner for Z_RR/Z_RY/M_R2/J_R/Q_R/B_R, refuse placeholders, and map accepted nonclaim rows to R10, PPN, clock, orbital, and WEP residual vectors",
            "must_include": "accepted schema; row-null Hessian vector; source/boundary rows; no-cancellation guard; units/normalization; arena projection placeholders; runner refusal reasons; no local claim",
            "excluded": "another broad object-language proof; scalar-projection-only scoring; cancellation pass; placeholder values; local-GR claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    domain_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2036_0_source_weight_domain",
            SOURCE_WEIGHT_DOCS / "AFRAME_MINIMAL_U_DOMAIN_CERTIFICATE_2036_REJECTED_NONCLAIM.csv",
            domain_rows,
        ),
        (
            "COPY2036_1_wep_finite_acquisition",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2036_FINITE_LOCAL_RESIDUAL_ACQUISITION_NONCLAIM.csv",
            acquisition_rows,
        ),
        (
            "COPY2036_2_rab_schema",
            QUEUE / "JR2036_ACCEPTED_FINITE_LOCAL_RESIDUAL_SCHEMA_NONCLAIM.csv",
            schema_rows,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    domain_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2036_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2036_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    verdict = next(row for row in domain_rows if row["row_id"] == "UDOM2036_7_certificate_verdict")
    checks.append(("VAL2036_02_certificate_rejected", verdict["status"] == "MINIMAL_U_DOMAIN_CERTIFICATE_NOT_DERIVED", "minimal u-domain certificate is rejected for current corpus"))
    branch = next(row for row in acquisition_rows if row["row_id"] == "FACQ2036_0_branch_policy")
    checks.append(("VAL2036_03_finite_branch_active", branch["status"] == "ACTIVE_NONCLAIM", "finite residual acquisition is activated as nonclaim"))
    checks.append(("VAL2036_04_schema_required", len(schema_rows) >= 9 and all(row["status"] == "REQUIRED" for row in schema_rows), "accepted finite residual schema is written"))
    checks.append(("VAL2036_05_claims_blocked", all(str(row.get("claim_allowed", "")).lower() == "false" for row in gate_rows), "all claim gates remain false"))
    checks.append(("VAL2036_06_next_selected", next_rows[0]["target_id"] == "NEXT2036_0_2037", "next target is selected"))
    checks.append(("VAL2036_07_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2036_08_no_formalization_2036_artifacts", not formalization_has_2036_artifacts(), "no 2036 domain/finite-residual artifacts were written under formalization-workbench"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2036_OVERALL", overall_ok, "2036 minimal u-domain certificate checkpoint is internally valid and nonclaim"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    domain_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 2036 Y5 R2FR Minimal U Domain Certificate Or Finite Local Residual Acquisition",
        "",
        "## Current Verdict",
        "",
        "The narrow `u=R_AB` parent-domain certificate does not close from the current corpus. This is the responsible stopping point for derivation-first on this exact local branch: the exact theorem is still a good target, but current evidence does not prove that `u` and `D_mu u` are absent action arguments while `Lambda_R u` is parent-owned. The branch is therefore switched to finite local residual acquisition, with no local-GR/Newton/R10/PPN/clock/orbital claim.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Minimal U Domain Certificate",
        md_table(domain_rows, ["row_id", "clause", "consequence", "status", "evidence", "claim_allowed"]),
        "## Finite Local Residual Acquisition",
        md_table(acquisition_rows, ["row_id", "symbol", "formula", "status", "role", "claim_allowed"]),
        "## Accepted Row Schema",
        md_table(schema_rows, ["field", "requirement", "status", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Claim Gate",
        md_table(gate_rows, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    domain_rows = u_domain_certificate_rows()
    acquisition_rows = finite_acquisition_rows()
    schema_rows = accepted_schema_rows()
    decision_rows_ = route_decision_rows()
    gate_rows = claim_gate_rows()
    next_rows = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2036_SOURCE_REGISTER.csv",
        "domain": OUT / "P8_Y5_PARENT_QLOC_2036_MINIMAL_U_DOMAIN_CERTIFICATE.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2036_FINITE_LOCAL_RESIDUAL_ACQUISITION.csv",
        "schema": OUT / "P8_Y5_PARENT_QLOC_2036_ACCEPTED_ROW_SCHEMA.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2036_DECISION_LEDGER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2036_CLAIM_GATE.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2036_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2036_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2036_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["domain"], domain_rows)
    write_csv(paths["acquisition"], acquisition_rows)
    write_csv(paths["schema"], schema_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["gates"], gate_rows)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(domain_rows, acquisition_rows, schema_rows)
    write_csv(paths["branch"], branch_rows)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        domain_rows,
        acquisition_rows,
        schema_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        domain_rows,
        acquisition_rows,
        schema_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        domain_rows,
        acquisition_rows,
        schema_rows,
        decision_rows_,
        gate_rows,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
