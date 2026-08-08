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


DOC = ROOT / "2162-Y5-R2FR-minimal-parent-X-sector-action-clause-or-PPN-vector-fill.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2161": ROOT / "2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md",
    "2161_validation": OUT / "P8_Y5_BRR545_2161_VALIDATION.csv",
    "2161_next": OUT / "P8_Y5_PARENT_QLOC_2161_NEXT_TARGET.csv",
    "1856": ROOT / "1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md",
    "1856_validation": OUT / "P8_Y5_BRR545_1856_VALIDATION.csv",
    "1857": ROOT / "1857-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md",
    "1857_validation": OUT / "P8_Y5_BRR545_1857_VALIDATION.csv",
    "1858": ROOT / "1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md",
    "1858_validation": OUT / "P8_Y5_BRR545_1858_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2162_SOURCE_REGISTER.csv",
    "action_clause": OUT / "P8_Y5_PARENT_QLOC_2162_PARENT_X_ACTION_CLAUSE_ATTEMPT.csv",
    "fork": OUT / "P8_Y5_PARENT_QLOC_2162_SCALAR_OR_CONSTRAINT_FORK.csv",
    "ppn_vector": OUT / "P8_Y5_PARENT_QLOC_2162_PPN_VECTOR_FILL.csv",
    "component_queue": OUT / "P8_Y5_PARENT_QLOC_2162_COMPONENT_BOUND_QUEUE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2162_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2162_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2162_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2162_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2162_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2162_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_X_ACTION_OR_VECTOR_2162_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2162_LOCAL_VECTOR_NONCLAIM.csv",
    "queue": QUEUE / "JR2162_CONSTRAINT_OR_VECTOR_FILL_QUEUE.csv",
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


def formalization_has_2162_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2162-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2162*",
        "*P8_Y5_BRR545_2162*",
        "*Y5_R2FR_minimal_parent_X_sector_action_clause_or_PPN_vector_fill_2162*",
        "*AFRAME_PARENT_X_ACTION_OR_VECTOR_2162*",
        "*JR2162*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2162_00_2161_handoff",
            DOCS["2161"],
            [["NEXT2161_0_2162"], ["PAC2161_1_quadratic_action"], ["VAL2161_OVERALL"]],
            "2161 selects the minimal parent X-sector action clause or PPN vector-fill target.",
        ),
        (
            "SRC2162_01_2161_validation",
            DOCS["2161_validation"],
            [["VAL2161_OVERALL"], ["PASS"]],
            "2161 validation passed as nonclaim.",
        ),
        (
            "SRC2162_02_2161_next_csv",
            DOCS["2161_next"],
            [["NEXT2161_0_2162"], ["X-sector"], ["PPN vector"]],
            "machine-readable 2162 handoff.",
        ),
        (
            "SRC2162_03_1856_scalar_rejection",
            DOCS["1856"],
            [["REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH"], ["FORK1856_1_constraint_auxiliary"], ["VAL1856_OVERALL"]],
            "prior primitive audit rejects physical propagating scalar as fundamental current branch.",
        ),
        (
            "SRC2162_04_1856_validation",
            DOCS["1856_validation"],
            [["VAL1856_OVERALL"], ["PASS"]],
            "1856 validation passed as nonclaim.",
        ),
        (
            "SRC2162_05_1857_constraint_theorem",
            DOCS["1857"],
            [["CLG1857_5_local_GR_consequence"], ["EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"], ["VAL1857_OVERALL"]],
            "constraint/auxiliary route supplies a clean conditional local-GR theorem shape.",
        ),
        (
            "SRC2162_06_1857_validation",
            DOCS["1857_validation"],
            [["VAL1857_OVERALL"], ["PASS"]],
            "1857 validation passed as nonclaim.",
        ),
        (
            "SRC2162_07_1858_parent_origin",
            DOCS["1858"],
            [["MOTION_LOAD_PHASE_VOLUME_PARENT_ORIGIN_SELECTED"], ["NEXT1858_0_primary"], ["VAL1858_OVERALL"]],
            "parent constraint package selects motion-load/phase-volume parent origin as the bottleneck.",
        ),
        (
            "SRC2162_08_1858_validation",
            DOCS["1858_validation"],
            [["VAL1858_OVERALL"], ["PASS"]],
            "1858 validation passed as nonclaim.",
        ),
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


def action_clause_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "PXA2162_0_candidate_clause",
            "minimal propagating X-sector",
            "S_X^(2)=-1/2 int sqrt(-g) M_Pl^2[Z_X(g,q)(grad Xhat)^2+M_X^2(g,q)Xhat^2]+int sqrt(-g)Xhat J_X+boundary",
            "CLOSURE_CLAUSE_ONLY",
            "coherent EFT scaffold, but not derived from motion/time/space primitives",
        ),
        (
            "PXA2162_1_field_owner",
            "primitive Xhat owner",
            "one dimensionless parent normal coordinate owns c_g, Z_X, M_X^2, J_X and projections",
            "FAIL_CURRENT_CLAIM_NO_PRIMITIVE_OWNER",
            "1856 rejects physical scalar as fundamental current branch",
        ),
        (
            "PXA2162_2_hessian_coefficients",
            "Z_X and M_X^2",
            "delta^2 S_parent fixes positive Z_X and signed M_X^2 or protected zero",
            "FAIL_CURRENT_CLAIM_COEFFICIENTS_MISSING",
            "2161 still has relation-only N_X/lambda",
        ),
        (
            "PXA2162_3_cross_hessian_schur",
            "cross-Hessian or Schur complement",
            "mixed variables are diagonalized or retained in an effective multi-component block",
            "FAIL_CURRENT_CLAIM_CROSS_BLOCK_UNSIGNED",
            "single-field c_g isolation remains unsafe",
        ),
        (
            "PXA2162_4_source_boundary",
            "J_X/support/boundary/domain/readout",
            "ordinary matter source and boundary terms are zero by theorem or carried as explicit residuals",
            "FAIL_CURRENT_CLAIM_SOURCE_BOUNDARY_UNSIGNED",
            "local vacuum and plateau claims remain blocked",
        ),
        (
            "PXA2162_5_ppn_interface",
            "tau_PPN, S_PPN(lambda_X,env), vector tails",
            "same parent action maps the local residual to Cassini/PPN/R10/clock/orbital observables",
            "FAIL_CURRENT_CLAIM_ARENA_PROJECTIONS_MISSING",
            "empirical scoring must use nonclaim component rows",
        ),
        (
            "PXA2162_6_verdict",
            "derived parent X-sector action",
            "the minimal propagating scalar action is not parent-derived in the current corpus",
            "FAIL_AS_DERIVED_PARENT_ACTION_CLOSURE_ONLY",
            "use only as private EFT/backstop; selected route is constraint/auxiliary before readout",
        ),
    ]
    return [
        row(clause_id=clause_id, object=object_name, formula_or_requirement=formula_or_requirement, status=status, consequence=consequence)
        for clause_id, object_name, formula_or_requirement, status, consequence in data
    ]


def scalar_or_constraint_fork_rows() -> list[dict[str, object]]:
    data = [
        (
            "SCF2162_0_physical_scalar",
            "propagating Xhat scalar",
            "EFT/closure backstop only",
            "REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH",
            "adds fifth-force scalar hair unless the missing coefficients and source projections are derived",
            "do not use for local-GR claim",
        ),
        (
            "SCF2162_1_constraint_auxiliary",
            "constraint/auxiliary/quotient-first X removal",
            "selected derivation route",
            "SELECTED_PRIMARY_ROUTE",
            "eliminates the local residual before physical phase space and matter readout if parent package closes",
            "attack parent origin/generator/boundary/matter descent",
        ),
        (
            "SCF2162_2_vector_backstop",
            "finite residual PPN/R10/clock/orbital component vector",
            "empirical nonclaim backstop",
            "SCHEMA_FILLED_SOURCE_ROWS_REQUIRED",
            "keeps the project testable if derivation stalls",
            "source real component bounds and projections",
        ),
        (
            "SCF2162_3_current",
            "active local branch",
            "constraint route plus vector backstop",
            "ROUTE_SHARPENED_NOT_PROVEN",
            "local GR is not derived yet, but the best route is no longer the physical scalar c_g route",
            "2163 should derive motion-load/phase-volume parent origin or fall back to vector coefficients",
        ),
    ]
    return [
        row(fork_id=fork_id, branch=branch, role=role, status=status, reason=reason, next_action=next_action)
        for fork_id, branch, role, status, reason, next_action in data
    ]


def ppn_vector_fill_rows() -> list[dict[str, object]]:
    data = [
        (
            "PVF2162_0_cg",
            "common conformal component",
            "alpha_cg=tau_g S_PPN(lambda_X,env)c_g/sqrt(Z_X)",
            "needs c_g,Z_X,M_X^2,lambda_X,tau_g,S_PPN from one parent branch",
            "PPN gamma/Shapiro; R10 if finite range",
            "ACQUISITION_REQUIRED_NONCLAIM",
        ),
        (
            "PVF2162_1_disformal",
            "disformal/preferred-frame component",
            "alpha_dis=tau_dis b_dis",
            "needs matter metric expansion and preferred-frame projection",
            "PPN alpha1/alpha2; clocks; photon propagation",
            "ACQUISITION_REQUIRED_NONCLAIM",
        ),
        (
            "PVF2162_2_nonH",
            "non-Hilbert/source-current component",
            "alpha_nonH=tau_nonH q_nonH",
            "needs source-current law, conservation accounting and ordinary-matter projection",
            "PPN gamma; orbital source normalization; WEP",
            "ACQUISITION_REQUIRED_NONCLAIM",
        ),
        (
            "PVF2162_3_support_domain",
            "support/domain representative component",
            "alpha_support=tau_support Delta_W_support+tau_domain q_domain",
            "needs representative-domain theorem and support-dependence bound",
            "finite-source PPN; R10 geometry; orbital systems",
            "ACQUISITION_REQUIRED_NONCLAIM",
        ),
        (
            "PVF2162_4_boundary",
            "boundary/local flux component",
            "alpha_boundary=tau_boundary q_boundary",
            "needs zero/exact/fixed/retained boundary charge",
            "local-vacuum plateau; orbital boundary terms; lab finite source",
            "ACQUISITION_REQUIRED_NONCLAIM",
        ),
        (
            "PVF2162_5_readout",
            "measured-G/readout calibration component",
            "alpha_readout=tau_readout C_readout",
            "needs map from varied fields to measured GM, clocks, photons and PPN gamma",
            "Cassini gamma; ephemerides; clocks",
            "ACQUISITION_REQUIRED_NONCLAIM",
        ),
        (
            "PVF2162_6_total",
            "absolute no-cancellation residual vector",
            "|alpha_PPN_total|<=|alpha_cg|+|alpha_dis|+|alpha_nonH|+|alpha_support|+|alpha_boundary|+|alpha_readout|",
            "needs every component zero by theorem or source-bounded numerically",
            "PPN/local-GR acceptance gate",
            "SCHEMA_FILLED_VALUES_MISSING",
        ),
    ]
    return [
        row(vector_id=vector_id, component=component, formula=formula, required_source=required_source, observable_link=observable_link, status=status)
        for vector_id, component, formula, required_source, observable_link, status in data
    ]


def component_bound_queue_rows() -> list[dict[str, object]]:
    data = [
        ("CBQ2162_0_R10", "R10/lab finite-range", "alpha_cg,alpha_support,alpha_boundary", "lambda_X; finite-source geometry; real alpha(lambda) curve", "SOURCE_REQUIRED", False),
        ("CBQ2162_1_PPN", "Cassini/solar-system PPN", "alpha_cg,alpha_dis,alpha_nonH,alpha_readout", "tau_PPN; S_PPN; preferred-frame/readout projections", "SOURCE_REQUIRED", False),
        ("CBQ2162_2_clocks", "clock/time readout", "alpha_dis,alpha_readout,alpha_nonH", "clock-coupling projection and calibration tail", "SOURCE_REQUIRED", False),
        ("CBQ2162_3_orbital", "LLR/ephemerides/orbital systems", "alpha_cg,alpha_support,alpha_boundary,alpha_readout", "range transfer, GM readout, boundary/source support", "SOURCE_REQUIRED", False),
        ("CBQ2162_4_local_GR", "derived local GR/Newton limit", "all vector components", "constraint origin, elimination before readout, matter descent, component zero/bounds", "DERIVATION_REQUIRED", False),
    ]
    return [
        row(queue_id=queue_id, arena=arena, components=components, missing_inputs=missing_inputs, status=status, valid_for_claim=valid_for_claim)
        for queue_id, arena, components, missing_inputs, status, valid_for_claim in data
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2162_0_clause_written", "minimal X-sector action clause exists as a closure scaffold", True, "coherent EFT scaffold is explicit"),
        ("CG2162_1_clause_parent_derived", "minimal X-sector action is derived from MTS primitives", False, "field owner, Hessian, sources and projections fail"),
        ("CG2162_2_physical_scalar_fundamental", "physical propagating Xhat scalar is fundamental current branch", False, "1856 rejection remains active"),
        ("CG2162_3_constraint_route_selected", "constraint/auxiliary route is the selected local-GR attack", True, "1857/1858 conditional route is cleaner"),
        ("CG2162_4_constraint_route_proven", "constraint route derives local GR/Newton", False, "parent origin, boundary, degree count, matter descent and component lock remain open"),
        ("CG2162_5_vector_schema_filled", "PPN/R10 finite residual vector schema is filled", True, "component rows are staged"),
        ("CG2162_6_vector_claim_ready", "component vector is numerically source-bounded", False, "all rows remain acquisition-required nonclaim"),
        ("CG2162_7_public_local_claim", "local GR/PPN/R10 pass can be claimed", False, "neither derivation nor empirical vector closure is complete"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2162_0_insert_scalar_action", "treat PXA2162_0 as derived parent action", "CLOSURE_CLAUSE_ONLY", "BLOCKED", "physical scalar primitive owner failed in 1856", False),
        ("REF2162_1_promote_ZX_MX2", "promote Z_X/M_X^2 to parent coefficients", "COEFFICIENTS_MISSING", "BLOCKED", "2161 did not extract N_X/lambda inputs", False),
        ("REF2162_2_ignore_cross_terms", "score one c_g component alone", "CROSS_VECTOR_UNCONTROLLED", "BLOCKED", "Schur/cross-Hessian and PPN vector tails unsigned", False),
        ("REF2162_3_claim_constraint_GR", "claim constraint route already gives local GR", "PARENT_ORIGIN_OPEN", "BLOCKED", "1857/1858 route is conditional only", False),
        ("REF2162_4_empirical_pass", "claim local tests pass from vector schema", "VALUES_MISSING", "BLOCKED", "component source rows are not numeric bounds", False),
    ]
    return [
        row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible)
        for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data
    ]


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2162_0_parent_action",
            "The minimal propagating X-sector action is kept as closure/backstop, not promoted.",
            "it is mathematically coherent but not derived from MTS primitives and would reintroduce scalar hair.",
            "do not chase raw c_g as the primary local-GR route",
        ),
        (
            "DEC2162_1_primary_route",
            "The primary route is constraint/auxiliary/quotient-first elimination before matter readout.",
            "this is the route that can make local GR a reduction rather than a tuned fifth-force evasion.",
            "derive the parent origin of the nonpropagating reciprocity/constraint law",
        ),
        (
            "DEC2162_2_backstop",
            "The empirical backstop is the full finite residual vector.",
            "if derivation stalls, the project remains testable through R10/PPN/clocks/orbital component bounds.",
            "source real coefficients without allowing claims",
        ),
        (
            "DEC2162_3_next",
            "Next checkpoint should attack motion-load/phase-volume parent origin or open the finite-vector backstop.",
            "1858 already identifies parent origin as upstream of generator, boundary and degree-count cleanup.",
            "2163-Y5-R2FR-motion-load-phase-volume-parent-origin-or-finite-vector-backstop.md",
        ),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2162_0_2163",
            "2163-Y5-R2FR-motion-load-phase-volume-parent-origin-or-finite-vector-backstop.md",
            "scripts/Y5_R2FR_motion_load_phase_volume_parent_origin_or_finite_vector_backstop_2163.py",
            "derive or reject the parent motion-load/phase-volume law that yields the nonpropagating local reciprocity constraint before matter readout; if it fails, open the finite residual vector sourcing backstop",
            "selected",
            "constraint C_X/C_R is parent-owned without importing GR, or the local route is demoted to closure and empirical vector rows become primary",
        ),
        (
            "NEXT2162_1_parallel",
            "2163b-Y5-R2FR-constraint-generator-boundary-degree-count.md",
            "scripts/Y5_R2FR_constraint_generator_boundary_degree_count_2163b.py",
            "after parent origin is signed, prove differentiability, bracket/degree count and boundary silence",
            "held",
            "constraint package closes after origin is real",
        ),
    ]
    return [
        row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition)
        for route_id, next_target, script, objective, selection_status, success_condition in data
    ]


def write_branch_copies(
    action_clause: list[dict[str, object]],
    fork: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    component_queue: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2162_0_source_weight_docs", BRANCH_COPIES["source_weight"], action_clause + fork),
        ("COPY2162_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], ppn_vector + component_queue),
        ("COPY2162_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + component_queue),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    action_clause: list[dict[str, object]],
    fork: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    component_queue: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    action_ok = any(item["clause_id"] == "PXA2162_6_verdict" and item["status"] == "FAIL_AS_DERIVED_PARENT_ACTION_CLOSURE_ONLY" for item in action_clause)
    fork_ok = any(item["fork_id"] == "SCF2162_1_constraint_auxiliary" and item["status"] == "SELECTED_PRIMARY_ROUTE" for item in fork)
    vector_ok = any(item["vector_id"] == "PVF2162_6_total" and item["status"] == "SCHEMA_FILLED_VALUES_MISSING" for item in ppn_vector)
    queue_ok = len(component_queue) == 5 and all(not truthy(item.get("valid_for_claim", False)) for item in component_queue)
    gate_ok = (
        any(item["gate_id"] == "CG2162_3_constraint_route_selected" and truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "CG2162_7_public_local_claim" and not truthy(item["gate_pass"]) for item in gates)
        and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    )
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2162_3_next" and "2163" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2162_0_2163" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, action_clause, fork, ppn_vector, component_queue, gates, refusals, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2162_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, action_ok, fork_ok, vector_ok, queue_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2162_00_sources", sources_ok, "2161 plus 1856/1857/1858 source paths and needles validate"),
        ("VAL2162_01_action_clause", action_ok, "minimal propagating X action is closure-only, not derived"),
        ("VAL2162_02_fork", fork_ok, "constraint/auxiliary route selected over physical scalar route"),
        ("VAL2162_03_vector_fill", vector_ok, "PPN/local residual vector component schema is filled"),
        ("VAL2162_04_component_queue", queue_ok, "R10/PPN/clock/orbital/local component queues remain nonclaim"),
        ("VAL2162_05_claim_gates", gate_ok, "route selection can pass while public/local claims remain blocked"),
        ("VAL2162_06_refusals", refusal_ok, "refusal runner blocks scalar-action promotion, Z/M promotion, one-component PPN, constraint-GR and empirical-pass claims"),
        ("VAL2162_07_decision", decisions_ok, "decision ledger selects 2163 parent-origin/vector-backstop target"),
        ("VAL2162_08_next", next_ok, "2163 next target selected"),
        ("VAL2162_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2162_10_csv_parse", csv_ok, "all generated 2162 CSVs parse cleanly"),
        ("VAL2162_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2162_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2162"),
        ("VAL2162_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2162_OVERALL", all_ok, "2162 demotes the propagating X action to closure/backstop and selects constraint-origin derivation plus finite-vector sourcing."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    action_clause: list[dict[str, object]],
    fork: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    component_queue: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2161, _ = find_line(DOCS["2161"], ["NEXT2161_0_2162"])
    line_1856, _ = find_line(DOCS["1856"], ["REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH"])
    line_1857, _ = find_line(DOCS["1857"], ["CLG1857_5_local_GR_consequence"])
    line_1858, _ = find_line(DOCS["1858"], ["MOTION_LOAD_PHASE_VOLUME_PARENT_ORIGIN_SELECTED"])
    content = "\n\n".join(
        [
            "# 2162 - Y5/R2FR Minimal Parent X-Sector Action Clause Or PPN Vector Fill",
            "## Current Verdict",
            "2162 does **not** derive a parent-owned propagating `Xhat` scalar action, does **not** extract `Z_X/M_X^2`, and does **not** claim local GR/Newton, PPN, R10, clock, or orbital success.",
            "The minimal propagating X-sector action remains a coherent EFT/closure scaffold only. The active route is now constraint/auxiliary/quotient-first: remove the local residual before physical phase space and ordinary matter readout, with the finite residual vector kept as the empirical backstop.",
            f"This implements the 2161 handoff at line {line_2161}, respects the 1856 physical-scalar rejection at line {line_1856}, uses the 1857 conditional local-GR theorem at line {line_1857}, and inherits the 1858 parent-origin bottleneck at line {line_1858}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Parent X Action Clause Attempt",
            md_table(action_clause, ["clause_id", "object", "formula_or_requirement", "status", "consequence", "valid_for_claim"]),
            "## Scalar Or Constraint Fork",
            md_table(fork, ["fork_id", "branch", "role", "status", "reason", "next_action", "valid_for_claim"]),
            "## PPN/Local Residual Vector Fill",
            md_table(ppn_vector, ["vector_id", "component", "formula", "required_source", "observable_link", "status", "valid_for_claim"]),
            "## Component Bound Queue",
            md_table(component_queue, ["queue_id", "arena", "components", "missing_inputs", "status", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Refusal Runner",
            md_table(refusals, ["refusal_id", "attempted_claim", "input_status", "runner_result", "blocked_by", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This is a real tactical pivot, not a retreat. The propagating scalar coupling route is useful for tests, but it is not the clean GR-reduction route. The cleaner route is to prove that the local residual is a nonpropagating constraint/quotient redundancy before matter sees it. If that parent-origin derivation fails, the project still has a disciplined empirical backstop: source and bound every component of the finite residual vector without pretending it is already local GR.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    action_clause = action_clause_attempt_rows()
    fork = scalar_or_constraint_fork_rows()
    ppn_vector = ppn_vector_fill_rows()
    component_queue = component_bound_queue_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["action_clause"], action_clause)
    write_csv(OUTPUTS["fork"], fork)
    write_csv(OUTPUTS["ppn_vector"], ppn_vector)
    write_csv(OUTPUTS["component_queue"], component_queue)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(action_clause, fork, ppn_vector, component_queue, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, action_clause, fork, ppn_vector, component_queue, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, action_clause, fork, ppn_vector, component_queue, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2162 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
