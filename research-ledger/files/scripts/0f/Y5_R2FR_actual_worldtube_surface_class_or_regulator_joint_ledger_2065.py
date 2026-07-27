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


DOC = ROOT / "2065-Y5-R2FR-actual-worldtube-surface-class-or-regulator-joint-ledger.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2065_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2065-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2065*",
            "*Y5_R2FR_actual_worldtube_surface_class_or_regulator_joint_ledger_2065*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2065_00_2064_doc",
            ROOT / "2064-Y5-R2FR-corner-free-worldtube-certificate-or-PiR-corner-bound.md",
            ["NEXT2064_0_2065", "Excision surfaces", "joint ledger"],
            "2064 handoff into actual worldtube surface class or regulator-joint ledger.",
        ),
        (
            "SRC2065_01_2064_next",
            OUT / "P8_Y5_PARENT_QLOC_2064_NEXT_TARGET.csv",
            ["NEXT2064_0_2065", "surface_id", "regulator"],
            "machine-readable 2065 target.",
        ),
        (
            "SRC2065_02_2064_certificate",
            OUT / "P8_Y5_PARENT_QLOC_2064_CORNER_FREE_CERTIFICATE_ATTEMPT.csv",
            ["CFC2064_1_actual_surface_class", "MISSING_ACTUAL_BOUNDARY_SURFACE_CLASS", "CFC2064_2_regulator_joints"],
            "actual surface class and regulator-joint blockers.",
        ),
        (
            "SRC2065_03_2064_corner_bound",
            OUT / "P8_Y5_PARENT_QLOC_2064_FINITE_PIR_CORNER_BOUND_SCHEMA.csv",
            ["PCB2064_1_joint_ledger", "PCB2064_2_beta_corner", "MISSING_BETA_CORNER_VALUES"],
            "finite Pi_R corner bound schema requiring joint and beta_corner rows.",
        ),
        (
            "SRC2065_04_2063_component_intake",
            OUT / "P8_Y5_PARENT_QLOC_2063_FINITE_PIR_COMPONENT_INTAKE.csv",
            ["PCI2063_3_corner_bound", "MISSING_CORNER_COEFFICIENT_BETA_CORNER", "PCI2063_4_total_join"],
            "componentized Pi_R total fallback from 2063.",
        ),
        (
            "SRC2065_05_1166_corner_doc",
            ROOT / "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
            ["LC1166_0_boundary_of_boundary", "LC1166_1_regulator_joints", "CONDITIONAL_MATH_ZERO_NOT_ARENA_CERTIFIED"],
            "earlier local-corner certificate precedent.",
        ),
        (
            "SRC2065_06_1165_corner_csv",
            OUT / "P8_Y5_R10_1165_CCORNER_DSF_EPSILON_CERTIFICATE_ROWS.csv",
            ["CCZ1165_0_surface_without_corners", "MISSING_LOCAL_SURFACE_CERTIFICATE", "CCZ1165_6_finite_bound"],
            "surface-without-corners certificate and finite fallback rows.",
        ),
        (
            "SRC2065_07_1020_boundary_doc",
            ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            ["BDC1020_0_surface_manifold", "partial S_edge = empty", "Stokes zero can hide corner charge"],
            "boundary/cohomology warning against hiding corner charge.",
        ),
        (
            "SRC2065_08_1001_surface_doc",
            ROOT / "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
            ["MISSING_CLOSED_BREF_AND_CORNER_CERTIFICATE", "zero-by-boundary-silence and zero-by-fixed-radius are rejected", "corner certificates are absent"],
            "surface theorem guardrail against fixed-radius shortcuts.",
        ),
        (
            "SRC2065_09_1016_worldtube_selector",
            ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            ["PSC1016_3_support_selector", "PSC1016_4_linking_surface_class", "PST1016_5_verdict"],
            "conditional compact Hilbert source worldtube selector.",
        ),
        (
            "SRC2065_10_worldtube_glue",
            OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            ["W504_0_worldtube_setup", "W504_3_exterior_closure_equation", "W504_4_worldtube_source_measure_glue"],
            "worldtube/exterior-annulus glue clauses.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def candidate_surface_class_rows() -> list[dict[str, object]]:
    data = [
        (
            "ASC2065_0_ideal_stationary_annulus",
            "S_stat_annulus_candidate",
            "D_stat = Sigma_t intersect exterior(W_source) between R_in and R_out",
            "S = S_out union (-S_in)",
            "If Sigma_t is stationary, W_source is compact/smooth, S_in and S_out are smooth closed two-surfaces, and there are no regulator seams, then partial S = empty.",
            "CONDITIONAL_GEOMETRY_ZERO_AVAILABLE",
            "best low-scrutiny route: use a stationary spatial annulus, not a finite-time worldtube with caps",
            False,
        ),
        (
            "ASC2065_1_outer_readout_sphere",
            "S_out",
            "large readout sphere on the same stationary slice",
            "closed smooth two-sphere",
            "Corner-free as a manifold component if the readout surface is parent-owned and fixed before observable fitting.",
            "MISSING_READOUT_SURFACE_OWNER",
            "outer sphere geometry is easy; ownership and same-frame readout are not signed",
            False,
        ),
        (
            "ASC2065_2_inner_source_boundary",
            "S_in",
            "boundary of compact source support W_source = closure(supp J_H[tau])",
            "closed smooth source-linking surface",
            "Corner-free if the parent action fixes a smooth compact Hilbert source support with same-frame source measure.",
            "MISSING_PARENT_SOURCE_WORLDTUBE_OWNER",
            "inherits the worldtube/source-measure selector debt",
            False,
        ),
        (
            "ASC2065_3_time_caps",
            "C_time_caps",
            "finite-time worldtube caps",
            "absent in a purely stationary spatial-annulus theorem",
            "No caps appear only if the PPN/local branch is explicitly reduced to a stationary spatial slice before boundary variation.",
            "MISSING_STATIONARY_REDUCTION_OWNER",
            "otherwise source-worldtube endpoints remain possible corner sources",
            False,
        ),
        (
            "ASC2065_4_regulator_patch_seams",
            "C_regulator",
            "cutoff/excision/regulator/matched-patch seams",
            "must be absent or separately enumerated",
            "Any active seam becomes a corner family C_i requiring zero theorem or beta_corner bound.",
            "MISSING_REGULATOR_JOINT_LEDGER",
            "this is the dominant non-geometric blocker",
            False,
        ),
        (
            "ASC2065_5_verdict",
            "actual local/PPN surface class",
            "candidate annulus not yet identified with actual action/readout/source surface",
            "no arena certificate",
            "The ideal stationary annulus is mathematically clean but not parent-signed as the actual local branch surface.",
            "CONDITIONAL_SURFACE_CLASS_NOT_ARENA_CERTIFIED",
            "do not claim Pi_R^corner=0 from this checkpoint",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, surface_id, domain_D, S_components, certificate, status, note, accepted in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "surface_id": surface_id,
                "domain_D": domain_D,
                "S_components": S_components,
                "certificate_statement": certificate,
                "status": status,
                "note": note,
                "accepted_as_actual_surface": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def actual_surface_requirement_rows() -> list[dict[str, object]]:
    data = [
        (
            "ASR2065_0_surface_id",
            "surface_id",
            "single named surface class used by action variation, source support, readout, and bound rows",
            "MISSING_ACTUAL_SURFACE_ID",
            "2064 target demands this explicitly",
        ),
        (
            "ASR2065_1_domain_D",
            "domain D",
            "D must be declared as spatial stationary annulus, exterior worldtube slab, or another exact object",
            "MISSING_DOMAIN_DEFINITION",
            "without D, partial(partialD)=0 cannot attach to the branch",
        ),
        (
            "ASR2065_2_source_selector",
            "source worldtube W_source",
            "W_source must be fixed by parent Hilbert source support before readout",
            "MISSING_PARENT_SOURCE_WORLDTUBE_OWNER",
            "matches PSC1016/W504 debt",
        ),
        (
            "ASR2065_3_surface_equivalence",
            "same surface across action/readout/source",
            "the boundary in the variational principle must be the same boundary used by q_R and local/PPN readout",
            "MISSING_ACTION_READOUT_SOURCE_EQUIVALENCE",
            "prevents a clean theorem from landing on the wrong surface",
        ),
        (
            "ASR2065_4_stationary_slice",
            "stationary slice reduction",
            "finite time caps are absent only after a parent-owned stationary spatial reduction",
            "MISSING_STATIONARY_SLICE_THEOREM",
            "otherwise caps/endpoints require beta_corner rows",
        ),
        (
            "ASR2065_5_smoothness",
            "smooth closed components",
            "S_in and S_out must be smooth compact closed two-surfaces with no active boundary",
            "MISSING_SMOOTHNESS_REGULARITY_CERTIFICATE",
            "source boundary regularity cannot be assumed",
        ),
        (
            "ASR2065_6_regulator_ledger",
            "cutoff/excision/regulator ledger",
            "every cutoff, excision, patch, reference, numerical, or matching seam must be absent or listed",
            "MISSING_REGULATOR_JOINT_LEDGER",
            "prevents hidden corner charge",
        ),
        (
            "ASR2065_7_RAB_boundary_policy",
            "R_AB boundary variation policy",
            "free natural variation with no R_AB boundary/corner functional, not fixed R_AB boundary data",
            "MISSING_PARENT_BOUNDARY_POLICY_SIGNATURE",
            "fixed boundary data was already rejected as a no-hair proof",
        ),
        (
            "ASR2065_8_equation_path",
            "equation/source path",
            "the parent document must point to equations implementing the above clauses",
            "MISSING_PARENT_EQUATION_PATH",
            "no public or local claim without source path",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, requirement, required_content, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "requirement": requirement,
                "required_content": required_content,
                "status": status,
                "note": note,
                "parent_signed": False,
                "valid_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def regulator_joint_ledger_rows() -> list[dict[str, object]]:
    data = [
        (
            "RJL2065_0_outer_readout_surface",
            "S_out",
            "outer readout sphere",
            "corner-free component if smooth closed",
            "parent-owned readout surface fixed before fitting",
            "UNKNOWN_OWNER_NOT_ACTIVE_CORNER_YET",
            "MISSING_READOUT_SURFACE_OWNER",
            False,
        ),
        (
            "RJL2065_1_inner_source_surface",
            "S_in",
            "inner source-linking surface",
            "corner-free component if smooth compact source boundary",
            "W_source = closure(supp J_H[tau]) is parent-owned and smooth",
            "UNKNOWN_SOURCE_SURFACE",
            "MISSING_PARENT_SOURCE_WORLDTUBE_OWNER",
            True,
        ),
        (
            "RJL2065_2_time_caps",
            "C_time_caps",
            "finite-time cap/endcap joints",
            "absent only in stationary spatial-annulus reduction",
            "parent-signed stationary reduction removes temporal caps",
            "UNKNOWN_ACTIVE",
            "MISSING_STATIONARY_SLICE_THEOREM",
            True,
        ),
        (
            "RJL2065_3_source_worldtube_endpoints",
            "C_source_caps",
            "source-worldtube endpoints/caps",
            "absent only if the local branch never uses finite source-worldtube slabs",
            "spatial support theorem or explicit endpoint zero theorem",
            "UNKNOWN_ACTIVE",
            "MISSING_SOURCE_ENDPOINT_LEDGER",
            True,
        ),
        (
            "RJL2065_4_cutoff_regulator_seams",
            "C_cutoff",
            "radial cutoff and smoothing-regulator seams",
            "zero only if regulator is absent or R_AB-silent",
            "regulator list plus silence theorem",
            "UNKNOWN_ACTIVE",
            "MISSING_CUTOFF_REGULATOR_LEDGER",
            True,
        ),
        (
            "RJL2065_5_excision_surfaces",
            "C_excision",
            "excised source interior or singular-core joins",
            "zero only if excision boundary is not used or has R_AB-silent corner grammar",
            "excision policy plus beta/silence row",
            "UNKNOWN_ACTIVE",
            "MISSING_EXCISION_POLICY",
            True,
        ),
        (
            "RJL2065_6_matched_patch_joints",
            "C_patch",
            "matched asymptotic or coordinate patch joins",
            "zero only if patch transition is smooth and R_AB-silent",
            "patch atlas and transition theorem",
            "UNKNOWN_ACTIVE",
            "MISSING_PATCH_JOINT_LEDGER",
            True,
        ),
        (
            "RJL2065_7_reference_readout_join",
            "C_ref",
            "reference-subtraction/readout-surface join",
            "zero only if reference boundary is the same closed surface or source-independent",
            "reference/readout boundary equivalence",
            "UNKNOWN_ACTIVE",
            "MISSING_REFERENCE_SURFACE_CERTIFICATE",
            True,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, surface_id, joint_family, where_it_enters, zero_condition, status, blocker, beta_required in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "surface_id": surface_id,
                "joint_family": joint_family,
                "where_it_enters": where_it_enters,
                "zero_condition": zero_condition,
                "status": status,
                "blocker": blocker,
                "active_or_unknown": "unknown",
                "requires_beta_corner_if_active": beta_required,
                "valid_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def beta_corner_placeholder_rows() -> list[dict[str, object]]:
    data = [
        (
            "BCP2065_0_beta_source_surface",
            "beta_corner_source_surface",
            "S_in/source boundary",
            "Pi_R^corner_abs += abs(beta_corner_source_surface) * W_source_surface",
            "MISSING_PARENT_SOURCE_SURFACE_BETA_OR_ZERO_THEOREM",
        ),
        (
            "BCP2065_1_beta_time_caps",
            "beta_corner_time_caps",
            "finite time caps/endpoints",
            "Pi_R^corner_abs += abs(beta_corner_time_caps) * W_time_caps",
            "MISSING_STATIONARY_SLICE_THEOREM_OR_CAP_BETA",
        ),
        (
            "BCP2065_2_beta_cutoff",
            "beta_corner_cutoff",
            "cutoff/regulator seams",
            "Pi_R^corner_abs += abs(beta_corner_cutoff) * W_cutoff",
            "MISSING_REGULATOR_BETA_OR_SILENCE_THEOREM",
        ),
        (
            "BCP2065_3_beta_excision",
            "beta_corner_excision",
            "excision/singular-core joins",
            "Pi_R^corner_abs += abs(beta_corner_excision) * W_excision",
            "MISSING_EXCISION_BETA_OR_SILENCE_THEOREM",
        ),
        (
            "BCP2065_4_beta_patch",
            "beta_corner_patch",
            "matched-patch joins",
            "Pi_R^corner_abs += abs(beta_corner_patch) * W_patch",
            "MISSING_PATCH_BETA_OR_SILENCE_THEOREM",
        ),
        (
            "BCP2065_5_beta_reference",
            "beta_corner_reference",
            "reference/readout join",
            "Pi_R^corner_abs += abs(beta_corner_reference) * W_reference",
            "MISSING_REFERENCE_BETA_OR_SURFACE_EQUIVALENCE",
        ),
        (
            "BCP2065_6_no_cancellation_join",
            "Pi_R_corner_abs_total",
            "all active/unknown corner families",
            "sum_i abs(beta_corner_i) * W_i; join into Pi_R^tot_abs without sign cancellation",
            "MISSING_ALL_BETA_CORNER_VALUES_AND_WEIGHTS",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, joint_family, formula, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "joint_family": joint_family,
                "formula": formula,
                "units": "boundary-current units or explicitly declared",
                "required_input": "numeric bound/value or theorem-zero, source path, equation anchor, weight W_i",
                "blocker": blocker,
                "source_ready_schema": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows(
    surfaces: list[dict[str, object]],
    requirements: list[dict[str, object]],
    joints: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    verdict = next(row for row in surfaces if row["row_id"] == "ASC2065_5_verdict")
    missing_requirements = [row["row_id"] for row in requirements if not row["parent_signed"]]
    unknown_joints = [row["row_id"] for row in joints if row["status"].startswith("UNKNOWN")]
    rows_data = [
        (
            "RUN2065_0_ideal_annulus",
            "stationary spatial-annulus theorem",
            "CONDITIONAL_GEOMETRY_ZERO_AVAILABLE",
            "works if the actual arena is a stationary annulus with closed S_in/S_out and no seams",
            False,
        ),
        (
            "RUN2065_1_actual_surface_owner",
            "actual PPN/local branch surface",
            "REFUSED_ACTUAL_SURFACE_OWNER_MISSING",
            f"{verdict['status']}; missing_requirements={len(missing_requirements)}",
            False,
        ),
        (
            "RUN2065_2_joint_ledger",
            "regulator/cutoff/source endpoint ledger",
            "LEDGER_SCHEMA_WRITTEN_NOT_SOURCE_FILLED",
            f"unknown_joint_families={len(unknown_joints)}; beta_rows={len(beta_rows)}",
            False,
        ),
        (
            "RUN2065_VERDICT",
            "actual worldtube surface class or regulator-joint ledger",
            "ACTUAL_SURFACE_NOT_CERTIFIED_BETA_CORNER_LEDGER_REQUIRED",
            "no Pi_R^corner zero claim; next step must prove stationary surface owner or fill first beta_corner row",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, run_verdict, reason, accepted in rows_data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": run_verdict,
                "reason": reason,
                "accepted_for_scoring": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2065_0_ideal_annulus",
            "ideal stationary annulus proves Pi_R^corner=0",
            "FAIL_BLOCKED",
            "conditional geometry not yet identified with actual local/PPN arena",
        ),
        (
            "GATE2065_1_actual_surface_owner",
            "parent-owned actual surface_id/domain D",
            "FAIL_BLOCKED",
            "surface_id, D, action/readout/source equivalence, and equation path missing",
        ),
        (
            "GATE2065_2_source_worldtube",
            "same-frame compact source worldtube",
            "FAIL_BLOCKED",
            "W_source selector and source measure remain conditional",
        ),
        (
            "GATE2065_3_stationary_slice",
            "no time caps/endpoints",
            "FAIL_BLOCKED",
            "stationary spatial-slice reduction is not parent-signed",
        ),
        (
            "GATE2065_4_regulator_ledger",
            "all regulator/cutoff/excision/patch joints absent or listed",
            "FAIL_BLOCKED",
            "joint ledger is a schema, not a filled source certificate",
        ),
        (
            "GATE2065_5_beta_corner",
            "finite beta_corner source rows",
            "FAIL_BLOCKED",
            "all beta_corner values/zeros and weights remain placeholders",
        ),
        (
            "GATE2065_6_PiRtot_qR",
            "Pi_R^tot and q_R local/PPN score",
            "FAIL_BLOCKED",
            "no-cancellation Pi_R^tot join and q_R normalization remain incomplete",
        ),
        (
            "GATE2065_7_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "no formalization-workbench edit is made",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2065_0_best_route",
            "STATIONARY_SPATIAL_ANNULUS_IS_THE_BEST_ZERO_ROUTE",
            "It avoids time caps by construction and reduces the problem to parent-owned S_in/S_out plus regulator silence.",
        ),
        (
            "DEC2065_1_current_status",
            "ACTUAL_SURFACE_OWNER_NOT_SIGNED",
            "The corpus has a clean candidate, not a theorem that the actual local branch uses that candidate.",
        ),
        (
            "DEC2065_2_what_improved",
            "CORNER_PROBLEM_IS_NOW_FINITE_AND_AUDITABLE",
            "Instead of a vague corner objection, we now have exact surface clauses and beta_corner source-row slots.",
        ),
        (
            "DEC2065_3_no_shortcut",
            "DO_NOT_PROMOTE_IDEAL_ANNULUS_TO_CLAIM",
            "That would smuggle in the plateau/closure move under a geometry label.",
        ),
        (
            "DEC2065_4_next",
            "PROVE_STATIONARY_PPN_SURFACE_OWNER_OR_FILL_FIRST_BETA_ROW",
            "The next highest-value move is either parent-sign the actual stationary annulus or source one finite beta_corner family.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2065_0_2066",
            "target_doc": "2066-Y5-R2FR-stationary-PPN-surface-owner-or-first-beta-corner-row.md",
            "objective": "prove the parent-owned stationary PPN/local annulus surface class with smooth closed S_in/S_out and no caps/seams, or fill the first source-backed beta_corner finite row",
            "must_include": "surface_id; D_stat; W_source owner; same-frame tau/source measure; S_in/S_out smoothness; stationary slice theorem; regulator ledger verdict; first beta_corner row if proof fails; no-cancellation Pi_Rtot join",
            "excluded": "assuming stationary smoothness; fixed R_AB boundary data; closure-only proof; Cassini/local-GR scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    surfaces: list[dict[str, object]],
    joints: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2065_0_source_weight_surface_candidate",
            SOURCE_WEIGHT_DOCS / "AFRAME_ACTUAL_WORLDTUBE_SURFACE_CLASS_2065_CONDITIONAL_NONCLAIM.csv",
            surfaces,
        ),
        (
            "COPY2065_1_source_weight_joint_ledger",
            SOURCE_WEIGHT_DOCS / "AFRAME_REGULATOR_JOINT_LEDGER_2065_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            joints,
        ),
        (
            "COPY2065_2_source_weight_beta_corner",
            SOURCE_WEIGHT_DOCS / "AFRAME_BETA_CORNER_2065_PLACEHOLDER_SOURCE_ROWS_NONCLAIM.csv",
            beta_rows,
        ),
        (
            "COPY2065_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2065_SURFACE_JOINT_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2065_4_queue_next",
            QUEUE / "JR2065_STATIONARY_PPN_SURFACE_OWNER_OR_BETA_CORNER_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY", "claim_allowed": False})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    surfaces: list[dict[str, object]],
    requirements: list[dict[str, object]],
    joints: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    surface_verdict = next(row for row in surfaces if row["row_id"] == "ASC2065_5_verdict")
    surface_ok = (
        any(row["row_id"] == "ASC2065_0_ideal_stationary_annulus" for row in surfaces)
        and surface_verdict["status"] == "CONDITIONAL_SURFACE_CLASS_NOT_ARENA_CERTIFIED"
        and all(not bool(row["accepted_as_actual_surface"]) for row in surfaces)
    )
    requirement_ok = len(requirements) >= 9 and all(not bool(row["parent_signed"]) for row in requirements)
    required_joint_families = {
        "inner source-linking surface",
        "finite-time cap/endcap joints",
        "source-worldtube endpoints/caps",
        "radial cutoff and smoothing-regulator seams",
        "excised source interior or singular-core joins",
        "matched asymptotic or coordinate patch joins",
        "reference-subtraction/readout-surface join",
    }
    joint_ok = required_joint_families.issubset({str(row["joint_family"]) for row in joints}) and all(not bool(row["valid_for_scoring"]) for row in joints)
    beta_ok = len(beta_rows) >= 7 and all(bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in beta_rows)
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2065_VERDICT")
    dry_ok = dry_verdict["verdict"] == "ACTUAL_SURFACE_NOT_CERTIFIED_BETA_CORNER_LEDGER_REQUIRED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2065_0_2066"
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, surfaces, requirements, joints, beta_rows, dry_rows_, gates, next_rows_]
        for row in group
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2065_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2065_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2065_02_surface_candidate", surface_ok, "ideal stationary annulus route exists but is not arena-certified"))
    checks.append(("VAL2065_03_actual_requirements", requirement_ok, "actual surface owner requirements remain explicit and unsigned"))
    checks.append(("VAL2065_04_joint_ledger", joint_ok, "regulator/source/cap/patch/reference joint families are enumerated"))
    checks.append(("VAL2065_05_beta_rows", beta_ok, "beta_corner placeholder rows are source-ready but unscored"))
    checks.append(("VAL2065_06_dry_verdict", dry_ok, "dry run refuses Pi_R^corner zero claim and requires surface owner or beta rows"))
    checks.append(("VAL2065_07_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2065_08_next_selected", next_ok, "2066 stationary PPN surface owner or first beta row target selected"))
    checks.append(("VAL2065_09_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2065_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2065_11_no_formalization_artifacts", not formalization_has_2065_artifacts(), "no 2065 artifacts were written under formalization-workbench"))
    checks.append(("VAL2065_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2065_OVERALL", overall, "2065 constructs the surface/joint gate and keeps local-GR/R10 claims blocked"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    surfaces: list[dict[str, object]],
    requirements: list[dict[str, object]],
    joints: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2065 Y5 R2FR Actual Worldtube Surface Class Or Regulator Joint Ledger",
        "",
        "## Current Verdict",
        "",
        "2065 finds the cleanest zero route: use a parent-owned stationary spatial annulus `D_stat` whose boundary is only two smooth closed components, `S_out` and `S_in`. In that ideal case, there are no finite-time caps and `partial S=empty`, so the pure corner contribution can be zero.",
        "",
        "That is a useful route, not yet a theorem for current MTS. The corpus still does not parent-sign that the actual local/PPN action, source support, readout surface, and finite-bound rows all use this same stationary annulus. The source worldtube owner, same-frame source measure, stationary slice reduction, regulator/cutoff/excision ledger, and reference/readout equivalence remain unsigned.",
        "",
        "So the result is progress but not a local-GR pass: the vague corner objection has been converted into a finite checklist. Either 2066 proves the stationary annulus is the actual parent-owned surface, or it must start filling `beta_corner_i` rows for active/unknown joints and join them into `Pi_R^tot_abs` without cancellation.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, corner-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Candidate Surface Class",
        md_table(surfaces, ["row_id", "surface_id", "domain_D", "S_components", "certificate_statement", "status", "note", "accepted_as_actual_surface", "claim_allowed"]),
        "## Actual Surface Requirements",
        md_table(requirements, ["row_id", "requirement", "required_content", "status", "note", "parent_signed", "valid_for_scoring", "claim_allowed"]),
        "## Regulator Joint Ledger Schema",
        md_table(joints, ["row_id", "surface_id", "joint_family", "where_it_enters", "zero_condition", "status", "blocker", "active_or_unknown", "requires_beta_corner_if_active", "valid_for_scoring", "claim_allowed"]),
        "## Beta Corner Placeholder Rows",
        md_table(beta_rows, ["row_id", "quantity", "joint_family", "formula", "units", "required_input", "blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Dry Run",
        md_table(dry_rows_, ["run_id", "target", "verdict", "reason", "accepted_for_scoring", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    surfaces = candidate_surface_class_rows()
    requirements = actual_surface_requirement_rows()
    joints = regulator_joint_ledger_rows()
    beta_rows = beta_corner_placeholder_rows()
    dry_rows_ = dry_run_rows(surfaces, requirements, joints, beta_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2065_SOURCE_REGISTER.csv",
        "surfaces": OUT / "P8_Y5_PARENT_QLOC_2065_CANDIDATE_SURFACE_CLASS.csv",
        "requirements": OUT / "P8_Y5_PARENT_QLOC_2065_ACTUAL_SURFACE_REQUIREMENTS.csv",
        "joints": OUT / "P8_Y5_PARENT_QLOC_2065_REGULATOR_JOINT_LEDGER_SCHEMA.csv",
        "beta": OUT / "P8_Y5_PARENT_QLOC_2065_BETA_CORNER_PLACEHOLDER_ROWS.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2065_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2065_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2065_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2065_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2065_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2065_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["surfaces"], surfaces)
    write_csv(paths["requirements"], requirements)
    write_csv(paths["joints"], joints)
    write_csv(paths["beta"], beta_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(surfaces, joints, beta_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, surfaces, requirements, joints, beta_rows, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, surfaces, requirements, joints, beta_rows, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, surfaces, requirements, joints, beta_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
