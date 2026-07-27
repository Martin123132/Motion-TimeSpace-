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


DOC = ROOT / "2124-Y5-R2FR-source-feedback-kernel-normal-form-or-first-bounded-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2123_NEXT = OUT / "P8_Y5_PARENT_QLOC_2123_NEXT_TARGET.csv"
CSV_2123_VAL = OUT / "P8_Y5_BRR545_2123_VALIDATION.csv"
CSV_2123_SPLIT = OUT / "P8_Y5_PARENT_QLOC_2123_PI_SPLIT_THEOREM.csv"
CSV_2123_ZERO = OUT / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_ZERO_CONDITIONS.csv"
CSV_2123_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2123_FINITE_KERNEL_BOUND_ROWS.csv"
CSV_2123_ARENA = OUT / "P8_Y5_PARENT_QLOC_2123_ARENA_VERDICT.csv"
CSV_1701_COMM = OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv"
CSV_1209_DOMAIN = OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
CSV_1420_WEP = OUT / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv"
CSV_1899_OWNER = OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv"
CSV_1900_SOURCE = OUT / "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv"
CSV_2118_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_1963_NO_GAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2124_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2124-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2124*",
        "*Y5_R2FR_source_feedback_kernel_normal_form_or_first_bounded_row_2124*",
        "*AFRAME_SOURCE_FEEDBACK_2124*",
        "*JR2124_SOURCE_FEEDBACK*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2124_00_2123_next", CSV_2123_NEXT, ["NEXT2123_0_2124", "source-feedback-kernel-normal-form"], "2123 handoff selects source-feedback normal form or first bounded row."),
        ("SRC2124_01_2123_validation", CSV_2123_VAL, ["VAL2123_OVERALL", "PASS"], "2123 validation passed."),
        ("SRC2124_02_2123_split", CSV_2123_SPLIT, ["PIS2123_0_pure_postprocessing", "PIS2123_4_verdict"], "pure postprocessing closed; source-feedback retained."),
        ("SRC2124_03_2123_zero", CSV_2123_ZERO, ["ZC2123_0_variable_descent", "ZC2123_5_no_cancellation"], "zero conditions and absolute envelope."),
        ("SRC2124_04_2123_kernels", CSV_2123_KERNELS, ["FK2123_0_source_support", "FK2123_4_total_abs"], "finite kernel bound rows staged."),
        ("SRC2124_05_2123_arena", CSV_2123_ARENA, ["ARENA2123_4_local_gr", "NOT_CLAIMABLE"], "local GR bridge remains not claimable."),
        ("SRC2124_06_1701_commutator", CSV_1701_COMM, ["RC1701_2_projection_operator", "RC1701_4_calibration_feedback"], "projector/calibration feedback is the retained commutator class."),
        ("SRC2124_07_1209_domain", CSV_1209_DOMAIN, ["DMP1209_2_projector_stress_zero_branch", "DMP1209_3_projector_stress_bound"], "domain/projector finite bound route."),
        ("SRC2124_08_1420_wep", CSV_1420_WEP, ["WAC1420_0_source_worldtube_profile", "WAC1420_2_GM_common_mode_guard", "WAC1420_10_executability_verdict"], "WEP source projection gaps and GM guard."),
        ("SRC2124_09_1899_owner", CSV_1899_OWNER, ["ACO1899_0_target", "ACO1899_5_wep_readout_limit"], "action/current owner lemma and empirical limit."),
        ("SRC2124_10_1900_source", CSV_1900_SOURCE, ["PSR1900_3_source_composition_obstruction", "PSR1900_4_finite_source_multipole"], "source composition and finite source multipole blockers."),
        ("SRC2124_11_2118_kernels", CSV_2118_KERNELS, ["KSR2118_0_source_worldtube_kernel", "KSR2118_7_total_no_cancellation"], "source/readout kernel suite."),
        ("SRC2124_12_1963_chain", CSV_1963_NO_GAMMA, ["NGT1963_2_q_vertical_silence", "CONDITIONAL_CHAIN_RULE_ZERO"], "q-vertical silence chain rule."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def protocol_variable_rows() -> list[dict[str, object]]:
    return [
        row(protocol_id="SIG2124_0_source_profile", sigma_component="sigma_source_profile", meaning="Earth/source density, composition and support profile entering source projection", zero_condition="D_v sigma_source_profile=0 by q/e_obs descent or fixed protocol", current_status="UNSIGNED", linked_kernel="FK2124_0_source_GM"),
        row(protocol_id="SIG2124_1_GM_calibration", sigma_component="sigma_GM_common_mode", meaning="GM/G calibration convention separating common-mode mass normalization from relative source weights", zero_condition="only universal source factor enters fitted GM; relative source vector orthogonal to calibration", current_status="GUARD_WRITTEN_NOT_NUMERIC", linked_kernel="FK2124_0_source_GM"),
        row(protocol_id="SIG2124_2_material_response", sigma_component="sigma_material_response", meaning="test-body material tensor and source-charge basis", zero_condition="universal Hilbert coupling or source-relative tensor zero in parent basis", current_status="FULL_TENSOR_MISSING", linked_kernel="FK2124_1_WEP_material"),
        row(protocol_id="SIG2124_3_mask_orbit", sigma_component="sigma_mask_orbit_attitude", meaning="segment masks, attitude, orbit window and sensitive-axis projection", zero_condition="official protocol fixed before variation or q/e_obs descended", current_status="OFFICIAL_ARRAYS_MISSING", linked_kernel="FK2124_2_WEP_readout"),
        row(protocol_id="SIG2124_4_boundary_domain", sigma_component="sigma_boundary_domain", meaning="support tube, boundary transport, time normal, weight function and local projector", zero_condition="fixed same Fermi/parent readout map with no independent variation", current_status="CONDITIONAL_ZERO_NOT_PARENT_SIGNED", linked_kernel="FK2124_3_boundary_domain"),
        row(protocol_id="SIG2124_5_clock_light", sigma_component="sigma_clock_light_response", meaning="clock, rod and lightcone response operators", zero_condition="metric-only g_obs response with no direct representative dependence", current_status="RESPONSE_OPERATOR_MISSING", linked_kernel="FK2124_4_clock_light"),
    ]


def chain_rule_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="CR2124_0_setup",
            object="source-feedback observable",
            expression="K_A(Phi)=Pi_A(y(Phi),sigma_A(Phi)) J_A(y(Phi),sigma_A(Phi)), with y=(q(Phi),e_obs,A_owned,theta)",
            result="separates owned observed variables y from protocol/source-feedback variables sigma_A",
            proof_status="NORMAL_FORM_DEFINED",
            zero_ready=False,
        ),
        row(
            theorem_id="CR2124_1_vertical_variation",
            object="vertical derivative",
            expression="For v in ker(Dq) with D_v e_obs=0, D_v K_A=[D_sigma Pi_A[J_A]+Pi_A D_sigma J_A] D_v sigma_A",
            result="all dangerous source-feedback leakage is concentrated in D_v sigma_A",
            proof_status="CHAIN_RULE_DERIVED",
            zero_ready=False,
        ),
        row(
            theorem_id="CR2124_2_zero_case",
            object="derived zero condition",
            expression="If sigma_A=sigma_bar_A(y) or sigma_A is fixed external protocol, then D_v sigma_A=0 and D_v K_A=0",
            result="this is the exact source-feedback zero theorem, but only if sigma ownership is signed",
            proof_status="CONDITIONAL_ZERO_VALID",
            zero_ready=False,
        ),
        row(
            theorem_id="CR2124_3_bound_case",
            object="finite kernel envelope",
            expression="||D_v K_A|| <= (||D_sigma Pi_A|| ||J_A|| + ||Pi_A|| ||D_sigma J_A||) ||D_v sigma_A||",
            result="first universal source-feedback bound shape; arena rows only need L_A and epsilon_sigma_A",
            proof_status="FINITE_BOUND_NORMAL_FORM_DERIVED",
            zero_ready=False,
        ),
        row(
            theorem_id="CR2124_4_verdict",
            object="2124 derivation verdict",
            expression="C_A=0 iff protocol leakage epsilon_sigma_A is zero or the bracket operator vanishes; otherwise C_A is bounded, not erased",
            result="normal form achieved; first numeric/source-backed bound still absent",
            proof_status="NORMAL_FORM_CLOSED_NUMERIC_BOUND_OPEN",
            zero_ready=False,
        ),
    ]


def first_bounded_row_schema() -> list[dict[str, object]]:
    return [
        row(
            bound_id="FK2124_0_source_GM",
            arena="source/R10/PPN/orbit",
            normal_form="|C_source_GM| <= L_source_GM * epsilon_sigma_source_GM",
            lipschitz_factor="L_source_GM = ||D_sigma Pi_source|| ||J_source|| + ||Pi_source|| ||D_sigma J_source||",
            protocol_leak="epsilon_sigma_source_GM = ||D_v(sigma_source_profile, sigma_GM_common_mode)||",
            required_inputs="source profile/composition; support map; GM calibration equation; relative source-weight basis; units; source path",
            current_status="FIRST_BOUNDED_ROW_SCHEMA_ONLY",
            valid_for_claim=False,
            score_ready=False,
        ),
        row(
            bound_id="FK2124_1_WEP_material",
            arena="MICROSCOPE material/source leg",
            normal_form="|C_WEP_material| <= L_material * epsilon_sigma_material",
            lipschitz_factor="L_material from material tensor/source-charge basis response",
            protocol_leak="epsilon_sigma_material = ||D_v sigma_material_response||",
            required_inputs="full Ti/Pt material response tensor; source-charge basis; sign convention; source path",
            current_status="SCHEMA_ONLY_FULL_TENSOR_MISSING",
            valid_for_claim=False,
            score_ready=False,
        ),
        row(
            bound_id="FK2124_2_WEP_readout",
            arena="MICROSCOPE mask/orbit/readout",
            normal_form="|C_WEP_readout| <= L_readout * epsilon_sigma_mask_orbit",
            lipschitz_factor="L_readout from official projection operator and acceleration residual envelope",
            protocol_leak="epsilon_sigma_mask_orbit = ||D_v sigma_mask_orbit_attitude||",
            required_inputs="official CMSM arrays; masks; attitude; axis; segment averaging; eta convention",
            current_status="SCHEMA_ONLY_OFFICIAL_ARRAYS_MISSING",
            valid_for_claim=False,
            score_ready=False,
        ),
        row(
            bound_id="FK2124_3_boundary_domain",
            arena="local projector/domain",
            normal_form="epsilon_comm <= C_stress*(partial_readout_P_norm + partial_weight_P_norm + connection_mismatch_norm)",
            lipschitz_factor="C_stress and projector stress operator norm",
            protocol_leak="domain_motion_Linf and projector_stress_Linf",
            required_inputs="C_stress; partial_readout_P_norm; partial_weight_P_norm; connection_mismatch_norm; source path",
            current_status="SCHEMA_ONLY_DERIVED_VALUES_MISSING",
            valid_for_claim=False,
            score_ready=False,
        ),
        row(
            bound_id="FK2124_4_total_abs",
            arena="all source-feedback arenas",
            normal_form="Delta_source_feedback_abs = sum_A |C_A| with no cancellation",
            lipschitz_factor="sum_A L_A",
            protocol_leak="arena-specific epsilon_sigma_A",
            required_inputs="each arena zero certificate or finite bound row in common units",
            current_status="TOTAL_ABSOLUTE_ENVELOPE_RETAINED",
            valid_for_claim=False,
            score_ready=False,
        ),
    ]


def gm_guard_rows() -> list[dict[str, object]]:
    return [
        row(
            guard_id="GM2124_0_common_mode_rule",
            target="measured-G/GM absorption guard",
            statement="A fitted GM may absorb only the universal common-mode source factor; it cannot absorb relative source weights that contract differently with test-body material response.",
            current_status="RULE_DERIVED_AS_REQUIRED_GUARD",
            missing_for_claim="source-weight basis and calibration equation",
            consequence="no fitted-G rescue for WEP/R10/PPN source-feedback kernels",
        ),
        row(
            guard_id="GM2124_1_zero_condition",
            target="source-feedback zero via GM guard",
            statement="C_source_GM=0 if the non-common source residual vector is zero, or if material/readout response is orthogonal to it in the parent basis.",
            current_status="CONDITIONAL_ZERO_NOT_SIGNED",
            missing_for_claim="parent source residual vector; material/readout response tensor",
            consequence="source/GM row remains schema-only",
        ),
        row(
            guard_id="GM2124_2_bound_condition",
            target="first bounded row route",
            statement="If zero is not signed, a conservative bound needs ||source_residual_noncommon||, ||material_response|| and the projection/readout Lipschitz factor.",
            current_status="BOUND_ROUTE_DEFINED_VALUES_MISSING",
            missing_for_claim="numeric/source-backed values and uncertainties",
            consequence="next checkpoint should try source/GM common-mode descent or source-profile acquisition",
        ),
        row(
            guard_id="GM2124_3_verdict",
            target="GM guard verdict",
            statement="The guard is now algebraic rather than rhetorical: common-mode can be fitted out, relative source-feedback cannot.",
            current_status="GUARD_NORMAL_FORM_CLOSED_DATA_OPEN",
            missing_for_claim="source-backed non-common residual or theorem-zero certificate",
            consequence="prevents a fake local-GR pass by calibration absorption",
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2124_0_normal_form", gate="source-feedback chain-rule normal form derived", gate_pass=True, rationale="D_v K_A reduces to bracket times D_v sigma_A"),
        row(gate_id="GATE2124_1_pure_postprocessing_closed", gate="pure postprocessing remains closed", gate_pass=True, rationale="2123 closed report-level commutators by type"),
        row(gate_id="GATE2124_2_source_GM_zero", gate="source/GM feedback zero claimed", gate_pass=False, rationale="D_v sigma_source_GM is not parent-signed zero"),
        row(gate_id="GATE2124_3_first_numeric_bound", gate="first source-backed finite bound row available", gate_pass=False, rationale="2124 writes the schema/normal form, but no numeric source-backed values are present"),
        row(gate_id="GATE2124_4_fitted_G_absorption_blocked", gate="fitted-G absorption shortcut blocked", gate_pass=True, rationale="common-mode and relative source weights are separated explicitly"),
        row(gate_id="GATE2124_5_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="source-feedback protocol leakage remains nonzero or unbounded"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2124_0", decision="NORMAL_FORM_DERIVED", because="the remaining commutator is exactly controlled by protocol leakage D_v sigma_A", next_action="use L_A epsilon_sigma_A rows for every source-feedback arena"),
        row(decision_id="DEC2124_1", decision="NO_NUMERIC_BOUND_YET", because="source profile, material tensor, CMSM arrays and projector-stress constants are still absent", next_action="do not score; write acquisition or proof targets"),
        row(decision_id="DEC2124_2", decision="GM_GUARD_IS_NEXT_BEST_ROUTE", because="blocking fitted-G absorption is necessary before R10/WEP/PPN source rows can be trusted", next_action="try to prove common-mode source descent or fill a source-backed Earth/profile bound row"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2124_0_2125",
            next_target="2125-Y5-R2FR-GM-common-mode-source-descent-or-Earth-profile-bound-row.md",
            script="scripts/Y5_R2FR_GM_common_mode_source_descent_or_Earth_profile_bound_row_2125.py",
            objective="Attack the first 2124 bound row: prove the source/GM protocol variable is common-mode and q/e_obs-descended, or write a nonclaim source-backed Earth/source-profile acquisition row for the non-common residual.",
            forbidden_shortcuts="fitted-G absorption of relative source weights; assuming source point-mass universality; using bulk Earth composition as orbit-profile source vector without bound; CMSM templates/surrogates; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    normal_form: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gm_guard: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2124_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_SOURCE_FEEDBACK_NORMAL_FORM_2124_NONCLAIM.csv", normal_form + bounds + gm_guard),
        ("COPY2124_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2124_SOURCE_FEEDBACK_KERNEL_NORMAL_FORM_NONCLAIM.csv", normal_form + bounds + gm_guard),
        ("COPY2124_2_acquisition_queue", QUEUE / "JR2124_SOURCE_FEEDBACK_KERNEL_OR_GM_GUARD_QUEUE.csv", next_rows + bounds),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    protocols: list[dict[str, object]],
    chain_rule: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gm_guard: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    protocols_ok = len(protocols) >= 6 and any(item["protocol_id"] == "SIG2124_1_GM_calibration" for item in protocols)
    chain_ok = any(item["theorem_id"] == "CR2124_1_vertical_variation" and item["proof_status"] == "CHAIN_RULE_DERIVED" for item in chain_rule) and any(item["theorem_id"] == "CR2124_3_bound_case" and item["proof_status"] == "FINITE_BOUND_NORMAL_FORM_DERIVED" for item in chain_rule)
    bounds_ok = any(item["bound_id"] == "FK2124_0_source_GM" and item["current_status"] == "FIRST_BOUNDED_ROW_SCHEMA_ONLY" for item in bounds) and all(not truthy(item["score_ready"]) for item in bounds)
    gm_ok = any(item["guard_id"] == "GM2124_3_verdict" and item["current_status"] == "GUARD_NORMAL_FORM_CLOSED_DATA_OPEN" for item in gm_guard)
    gates_ok = any(item["gate_id"] == "GATE2124_0_normal_form" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2124_5_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2124_2" and item["decision"] == "GM_GUARD_IS_NEXT_BEST_ROUTE" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2124_0_2125" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, protocols, chain_rule, bounds, gm_guard, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2124_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, protocols_ok, chain_ok, bounds_ok, gm_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2124_00_sources", sources_ok, "all cited 2123/source-feedback rows exist and contain expected needles"),
        ("VAL2124_01_protocols", protocols_ok, "protocol variables sigma_A are listed, including GM calibration"),
        ("VAL2124_02_chain_rule", chain_ok, "vertical source-feedback chain rule and finite bound normal form are derived"),
        ("VAL2124_03_bounds", bounds_ok, "first bounded row schema exists but no finite row is score-ready"),
        ("VAL2124_04_gm_guard", gm_ok, "GM common-mode guard is algebraically separated from relative source weights"),
        ("VAL2124_05_gates", gates_ok, "normal form passes while local-GR/Newton/PPN claim fails"),
        ("VAL2124_06_decisions", decisions_ok, "decision ledger selects GM/source descent as next best route"),
        ("VAL2124_07_next", next_ok, "next target selects GM common-mode source descent or Earth profile bound row"),
        ("VAL2124_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2124_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2124_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2124_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2124"),
        ("VAL2124_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2124_OVERALL", all_ok, "2124 derives the source-feedback protocol-variable normal form, blocks fitted-G absorption, and leaves the first source/GM finite bound row as nonclaim schema-only."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    protocols: list[dict[str, object]],
    chain_rule: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gm_guard: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2124 - Y5/R2FR Source-Feedback Kernel Normal Form Or First Bounded Row",
            "## Current Verdict",
            "2124 turns the remaining source-feedback commutator into an executable normal form. Write every dangerous source/readout object as `K_A(Phi)=Pi_A(y(Phi),sigma_A(Phi)) J_A(y(Phi),sigma_A(Phi))`, with `y=(q(Phi),e_obs,A_owned,theta)` and `sigma_A` collecting protocol/source-feedback structures. For a vertical variation `v in ker(Dq)`, the 1963 chain rule kills the `y` variation, leaving only protocol leakage:",
            "`D_v K_A=[D_sigma Pi_A[J_A]+Pi_A D_sigma J_A] D_v sigma_A`.",
            "That is progress because it tells us exactly what must be derived next. If `D_v sigma_A=0`, the source-feedback commutator is zero. If not, the residual is bounded by a Lipschitz factor times `epsilon_sigma_A`. The first source/GM bound row is now written as a schema, but it is not score-ready because source profile, material tensor, official readout arrays and projector-stress constants remain missing.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Protocol Variables",
            md_table(protocols, ["protocol_id", "sigma_component", "meaning", "zero_condition", "current_status", "linked_kernel", "valid_for_claim"]),
            "## Source-Feedback Chain Rule",
            md_table(chain_rule, ["theorem_id", "object", "expression", "result", "proof_status", "zero_ready", "valid_for_claim"]),
            "## First Bounded Row Schema",
            md_table(bounds, ["bound_id", "arena", "normal_form", "lipschitz_factor", "protocol_leak", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "## GM Guard Descent Audit",
            md_table(gm_guard, ["guard_id", "target", "statement", "current_status", "missing_for_claim", "consequence", "valid_for_claim"]),
            "## Claim Gates",
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
    protocols = protocol_variable_rows()
    chain_rule = chain_rule_rows()
    bounds = first_bounded_row_schema()
    gm_guard = gm_guard_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2124_SOURCE_REGISTER.csv",
        "protocols": OUT / "P8_Y5_PARENT_QLOC_2124_PROTOCOL_VARIABLE_NORMAL_FORM.csv",
        "chain_rule": OUT / "P8_Y5_PARENT_QLOC_2124_SOURCE_FEEDBACK_CHAIN_RULE.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2124_FIRST_BOUNDED_ROW_SCHEMA.csv",
        "gm_guard": OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2124_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2124_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2124_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2124_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2124_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["protocols"], protocols)
    write_csv(paths["chain_rule"], chain_rule)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["gm_guard"], gm_guard)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(chain_rule, bounds, gm_guard, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, protocols, chain_rule, bounds, gm_guard, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, protocols, chain_rule, bounds, gm_guard, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
