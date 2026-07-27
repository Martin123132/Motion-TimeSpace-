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


DOC = ROOT / "2123-Y5-R2FR-readout-projection-commutator-zero-or-finite-kernel-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2122_NEXT = OUT / "P8_Y5_PARENT_QLOC_2122_NEXT_TARGET.csv"
CSV_2122_VAL = OUT / "P8_Y5_BRR545_2122_VALIDATION.csv"
CSV_2122_OWNER = OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv"
CSV_2122_COMM = OUT / "P8_Y5_PARENT_QLOC_2122_COMMUTATOR_OBSTRUCTION_LEDGER.csv"
CSV_2122_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2122_KERNEL_DEMOTION_OR_ZERO_STATUS.csv"
CSV_1701_COMM = OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv"
CSV_1209_DOMAIN = OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
CSV_1420_WEP = OUT / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv"
CSV_1898_COMM = OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv"
CSV_1900_POINT = OUT / "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv"
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


def formalization_has_2123_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2123-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2123*",
        "*Y5_R2FR_readout_projection_commutator_zero_or_finite_kernel_bound_2123*",
        "*AFRAME_COMMUTATOR_2123*",
        "*JR2123_COMMUTATOR*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2123_00_2122_next", CSV_2122_NEXT, ["NEXT2122_0_2123", "delta(Pi J)=Pi delta J"], "2122 selects the commutator zero/finite-kernel target."),
        ("SRC2123_01_2122_validation", CSV_2122_VAL, ["VAL2122_OVERALL", "PASS"], "2122 passed while keeping the commutator active."),
        ("SRC2123_02_2122_owner", CSV_2122_OWNER, ["SRO2122_0_exact_conditional", "SRO2122_6_verdict"], "owner lemma conditional theorem and blocked verdict."),
        ("SRC2123_03_2122_commutator", CSV_2122_COMM, ["COM2122_0_identity", "COM2122_2_countermodel"], "commutator identity and active countermodel."),
        ("SRC2123_04_2122_kernels", CSV_2122_KERNELS, ["KER2122_7_total", "RETAINED"], "kernel suite retained after 2122."),
        ("SRC2123_05_1701_commutator", CSV_1701_COMM, ["RC1701_1_pure_postprocessing", "RC1701_2_projection_operator", "RC1701_4_calibration_feedback"], "older readout no-reentry split."),
        ("SRC2123_06_1209_domain", CSV_1209_DOMAIN, ["DMP1209_0_domain_motion_zero_branch", "DMP1209_2_projector_stress_zero_branch", "DMP1209_4_total_epsilon_status"], "domain/projector stress conditions."),
        ("SRC2123_07_1420_wep", CSV_1420_WEP, ["WAC1420_0_source_worldtube_profile", "WAC1420_2_GM_common_mode_guard", "WAC1420_10_executability_verdict"], "WEP source projection acquisition gaps."),
        ("SRC2123_08_1898_countermodel", CSV_1898_COMM, ["RVC1898_2_projection_commutator_survives", "COUNTERMODEL_ACTIVE"], "projection commutator countermodel."),
        ("SRC2123_09_1900_source", CSV_1900_POINT, ["PSR1900_3_source_composition_obstruction", "PSR1900_4_finite_source_multipole"], "finite source and composition obstruction."),
        ("SRC2123_10_2118_kernels", CSV_2118_KERNELS, ["KSR2118_5_boundary_domain_kernel", "KSR2118_7_total_no_cancellation"], "explicit kernel shapes."),
        ("SRC2123_11_1963_no_gamma", CSV_1963_NO_GAMMA, ["NGT1963_2_q_vertical_silence", "CONDITIONAL_CHAIN_RULE_ZERO"], "chain-rule zero inside owned-coframe branch."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def pi_split_rows() -> list[dict[str, object]]:
    return [
        row(
            split_id="PIS2123_0_pure_postprocessing",
            projection_class="post-variation data/readout map",
            exact_statement="If Pi_A is typed as a map from already-solved parent histories to reported data and has no arrow back into S_parent, E_H, source normalization or coefficient definition, then [delta_parent,Pi_A] is harmless by type.",
            proof_status="ZERO_BY_TYPE_FOR_POSTPROCESSING_ONLY",
            source_anchor="RC1701_1_pure_postprocessing",
            residual_status="closed for reports only; does not close source-feedback rows",
            zero_ready=True,
        ),
        row(
            split_id="PIS2123_1_source_feedback",
            projection_class="source/calibration/projector map used before or during variation",
            exact_statement="If Pi_A fixes source weights, GM normalization, support masks, material channels or effective coefficients before variation, then delta(Pi J) contains (delta Pi)J unless Pi_A descends through q/e_obs or is fixed as external protocol.",
            proof_status="NOT_ZERO_IN_GENERAL",
            source_anchor="RC1701_2_projection_operator; RC1701_4_calibration_feedback; COM2122_2_countermodel",
            residual_status="finite kernel required",
            zero_ready=False,
        ),
        row(
            split_id="PIS2123_2_q_descended_projector",
            projection_class="owned q/e_obs-descended projector",
            exact_statement="If Pi_A=Pi_bar_A(q(Phi),e_obs,A_owned,theta) and J_A=Jbar_A(q(Phi),e_obs,A_owned,theta), then D_v(Pi_A J_A)=0 for every v in ker(Dq).",
            proof_status="CONDITIONAL_ZERO_VALID",
            source_anchor="SRO2122_0_exact_conditional; NGT1963_2_q_vertical_silence",
            residual_status="requires signed descent certificates for support, weights, boundary and readout channels",
            zero_ready=False,
        ),
        row(
            split_id="PIS2123_3_external_protocol",
            projection_class="externally fixed protocol",
            exact_statement="If support, masks, orbit window, boundary transport and calibration protocol are fixed before variation and are not functions of the representative fields, then delta Pi_A=0, but this is a closure assumption unless the parent action declares those structures.",
            proof_status="CLOSURE_NOT_PARENT_DERIVED",
            source_anchor="DMP1209_0_domain_motion_zero_branch; DMP1209_2_projector_stress_zero_branch",
            residual_status="acceptable as explicit closure only, not as derived local-GR theorem",
            zero_ready=False,
        ),
        row(
            split_id="PIS2123_4_verdict",
            projection_class="full source/readout commutator",
            exact_statement="The pure postprocessing part is closed by type, but the physically relevant source-feedback/projector-support part is not parent-signed.",
            proof_status="PARTIAL_ZERO_PLUS_RETAINED_KERNEL",
            source_anchor="1701, 1209, 1420, 1898, 1900, 2122",
            residual_status="local branch still carries finite commutator kernels",
            zero_ready=False,
        ),
    ]


def zero_condition_rows() -> list[dict[str, object]]:
    return [
        row(condition_id="ZC2123_0_variable_descent", condition="Pi_A and J_A descend through q/e_obs", mathematical_test="D_v Pi_A=0 and D_v J_A=0 for all v in ker(Dq)", current_status="UNSIGNED_FOR_SOURCE_FEEDBACK", missing_input="sector descent certificates"),
        row(condition_id="ZC2123_1_no_feedback_typing", condition="readout map is postprocessing only", mathematical_test="Pi_A acts after solving E_parent=0 and is not used in S_parent, coefficient extraction, source normalization or calibration", current_status="CLOSED_FOR_REPORTING_MAPS", missing_input="none for reports; not sufficient for source rows"),
        row(condition_id="ZC2123_2_fixed_protocol", condition="support/mask/boundary protocol is fixed before variation", mathematical_test="delta_v sigma_A=0 for sigma_A={support, mask, orbit window, boundary transport, weight}", current_status="CLOSURE_ONLY", missing_input="parent declaration or source path for protocol"),
        row(condition_id="ZC2123_3_GM_guard", condition="GM calibration is common-mode only", mathematical_test="relative source weights cannot be absorbed into fitted G or GM", current_status="GUARD_WRITTEN_NOT_NUMERIC", missing_input="calibration equation and source-weight basis"),
        row(condition_id="ZC2123_4_finite_source", condition="finite source profile reduces to universal/common-mode point source", mathematical_test="composition/profile multipole correction is zero or bounded before WEP projection", current_status="NOT_PROVEN", missing_input="Earth profile/source composition theorem or sourced kernel"),
        row(condition_id="ZC2123_5_no_cancellation", condition="retained kernels combine by absolute envelope", mathematical_test="Delta_comm_abs=sum_A abs(P_A C_A)", current_status="RETAINED", missing_input="component zeros or finite numeric bounds"),
    ]


def finite_kernel_rows() -> list[dict[str, object]]:
    return [
        row(
            kernel_id="FK2123_0_source_support",
            arena="source/R10/PPN/orbit",
            bound_shape="|C_source| <= ||D_sigma Pi_source|| ||D_v sigma_source|| ||J_source|| + ||Pi_source|| ||D_v J_source||",
            required_inputs="source profile; composition/source-charge convention; support map; GM common-mode guard; units",
            source_anchor="KSR2118_0_source_worldtube_kernel; WAC1420_0_source_worldtube_profile; WAC1420_1_source_composition",
            current_status="FINITE_KERNEL_SHAPE_ONLY",
            score_ready=False,
        ),
        row(
            kernel_id="FK2123_1_wep_mask_orbit",
            arena="MICROSCOPE/WEP",
            bound_shape="|C_WEP| <= ||D_sigma Pi_inst|| (mask_orbit_attitude_norm + finite_source_multipole_norm) ||Delta a||",
            required_inputs="official CMSM readout arrays; attitude/axis kernel; segment masks; eta convention; finite-source error bound",
            source_anchor="KSR2118_1_orbit_WEP_kernel; WAC1420_6_attitude_axis_kernel; PSR1900_4_finite_source_multipole",
            current_status="OFFICIAL_ARRAYS_AND_ERROR_BOUND_MISSING",
            score_ready=False,
        ),
        row(
            kernel_id="FK2123_2_boundary_domain",
            arena="local projector/domain",
            bound_shape="epsilon_comm <= C_stress*(partial_readout_P_norm + partial_weight_P_norm + connection_mismatch_norm)",
            required_inputs="C_stress; partial_readout_P_norm; partial_weight_P_norm; connection_mismatch_norm; source path",
            source_anchor="DMP1209_2_projector_stress_zero_branch; DMP1209_3_projector_stress_bound; KSR2118_5_boundary_domain_kernel",
            current_status="BOUND_DERIVED_VALUES_MISSING",
            score_ready=False,
        ),
        row(
            kernel_id="FK2123_3_clock_light",
            arena="clock/light/PPN gamma",
            bound_shape="|C_clock/light| <= ||D_sigma Pi_clock/light|| ||D_v sigma_clock/light|| ||J_matter||",
            required_inputs="clock functional; rod calibration; photon/lightcone branch; response operator; material-marker exclusion",
            source_anchor="KSR2118_2_clock_redshift_kernel; KSR2118_3_lightcone_kernel",
            current_status="RESPONSE_OPERATOR_MISSING",
            score_ready=False,
        ),
        row(
            kernel_id="FK2123_4_total_abs",
            arena="all local arenas",
            bound_shape="Delta_comm_abs = sum_i abs(C_i) with no cross-arena cancellation",
            required_inputs="each component theorem-zero or finite bound in common units",
            source_anchor="KSR2118_7_total_no_cancellation; ZC2123_5_no_cancellation",
            current_status="TOTAL_KERNEL_RETAINED",
            score_ready=False,
        ),
    ]


def arena_verdict_rows() -> list[dict[str, object]]:
    return [
        row(arena_id="ARENA2123_0_reports", arena="pure reports/data plots", verdict="CLOSED_BY_TYPE", consequence="safe as postprocessing only; no source coupling claim", next_action="mark separately from physics source rows"),
        row(arena_id="ARENA2123_1_wep", arena="WEP/source projection", verdict="OPEN_KERNEL", consequence="cannot score tau_WEP or local WEP without official arrays or theorem-zero", next_action="source FK2123_1 or prove fixed protocol"),
        row(arena_id="ARENA2123_2_r10_ppn_orbit", arena="R10/PPN/orbital source support", verdict="OPEN_KERNEL", consequence="source-normalization/projector tail can leak into local tests", next_action="source FK2123_0 or prove common-mode source descent"),
        row(arena_id="ARENA2123_3_clock_light", arena="clock/light", verdict="OPEN_RESPONSE_OPERATOR", consequence="metric-only readout not yet parent-signed", next_action="derive response operator or retain bound"),
        row(arena_id="ARENA2123_4_local_gr", arena="local GR/Newton bridge", verdict="NOT_CLAIMABLE", consequence="LC/no-Gamma branch is promising but not sufficient", next_action="close source-feedback kernels before promoting local branch"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2123_0_pure_postprocessing_zero", gate="pure postprocessing commutator zero", gate_pass=True, rationale="typed after variation; no arrow back to parent action/source equation"),
        row(gate_id="GATE2123_1_source_feedback_zero", gate="source-feedback/projector commutator zero", gate_pass=False, rationale="requires q/e_obs descent or fixed protocol for support, masks, weights and boundary transport"),
        row(gate_id="GATE2123_2_finite_kernel_written", gate="finite commutator kernel normal form written", gate_pass=True, rationale="source, WEP, boundary/domain, clock/light and total absolute kernel shapes are staged"),
        row(gate_id="GATE2123_3_kernel_score_ready", gate="finite kernels score ready", gate_pass=False, rationale="required source paths/numeric values/official arrays are missing"),
        row(gate_id="GATE2123_4_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="physically relevant source-feedback commutator remains open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2123_0", decision="SPLIT_THE_COMMUTATOR", because="pure reports are safe, source-feedback maps are not automatically safe", next_action="do not let report-level closure masquerade as source-level theorem"),
        row(decision_id="DEC2123_1", decision="PARTIAL_DERIVATION_WIN", because="one class of Pi is now theorem-zero by type", next_action="carry this as a closed subcase in future ledgers"),
        row(decision_id="DEC2123_2", decision="RETAIN_FINITE_KERNELS", because="finite source, GM guard, mask/orbit and boundary projector data remain unsigned", next_action="build source-feedback kernel pack or prove q/e_obs descent for one arena"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2123_0_2124",
            next_target="2124-Y5-R2FR-source-feedback-kernel-normal-form-or-first-bounded-row.md",
            script="scripts/Y5_R2FR_source_feedback_kernel_normal_form_or_first_bounded_row_2124.py",
            objective="Use the 2123 commutator split to close pure postprocessing rows permanently, then attack the source-feedback side by either proving q/e_obs descent for the source/GM guard or writing the first source-backed finite bound row.",
            forbidden_shortcuts="treating reports as source equations; assuming delta Pi=0 for source feedback; using fitted-G absorption; using CMSM templates/surrogates; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    pi_split: list[dict[str, object]],
    kernels: list[dict[str, object]],
    arena: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2123_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_COMMUTATOR_SPLIT_2123_NONCLAIM.csv", pi_split + kernels + arena),
        ("COPY2123_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_KERNEL_STATUS_NONCLAIM.csv", pi_split + kernels + arena),
        ("COPY2123_2_acquisition_queue", QUEUE / "JR2123_COMMUTATOR_KERNEL_OR_SOURCE_FEEDBACK_QUEUE.csv", next_rows + kernels),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    pi_split: list[dict[str, object]],
    zero_conditions: list[dict[str, object]],
    kernels: list[dict[str, object]],
    arena: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    split_ok = any(item["split_id"] == "PIS2123_0_pure_postprocessing" and truthy(item["zero_ready"]) for item in pi_split) and any(item["split_id"] == "PIS2123_4_verdict" and item["proof_status"] == "PARTIAL_ZERO_PLUS_RETAINED_KERNEL" for item in pi_split)
    conditions_ok = any(item["condition_id"] == "ZC2123_0_variable_descent" for item in zero_conditions) and any(item["condition_id"] == "ZC2123_5_no_cancellation" for item in zero_conditions)
    kernels_ok = any(item["kernel_id"] == "FK2123_4_total_abs" and item["current_status"] == "TOTAL_KERNEL_RETAINED" for item in kernels) and all(not truthy(item["score_ready"]) for item in kernels)
    arena_ok = any(item["arena_id"] == "ARENA2123_0_reports" and item["verdict"] == "CLOSED_BY_TYPE" for item in arena) and any(item["arena_id"] == "ARENA2123_4_local_gr" and item["verdict"] == "NOT_CLAIMABLE" for item in arena)
    gates_ok = any(item["gate_id"] == "GATE2123_0_pure_postprocessing_zero" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2123_4_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2123_1" and item["decision"] == "PARTIAL_DERIVATION_WIN" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2123_0_2124" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, pi_split, zero_conditions, kernels, arena, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2123_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, split_ok, conditions_ok, kernels_ok, arena_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2123_00_sources", sources_ok, "all cited commutator/domain/WEP source rows exist and contain expected needles"),
        ("VAL2123_01_split", split_ok, "commutator is split into closed pure-postprocessing and retained source-feedback branches"),
        ("VAL2123_02_zero_conditions", conditions_ok, "zero conditions include q/e_obs descent and no-cancellation envelope"),
        ("VAL2123_03_kernels", kernels_ok, "finite kernel normal forms are retained and not score-ready"),
        ("VAL2123_04_arena", arena_ok, "arena verdict closes reports but blocks local-GR claim"),
        ("VAL2123_05_gates", gates_ok, "pure postprocessing gate passes while local claim gate fails"),
        ("VAL2123_06_decisions", decisions_ok, "decision ledger records a partial derivation win"),
        ("VAL2123_07_next", next_ok, "next target selects source-feedback kernel normal form or first bounded row"),
        ("VAL2123_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2123_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2123_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2123_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2123"),
        ("VAL2123_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2123_OVERALL", all_ok, "2123 proves pure postprocessing commutators harmless by type, but retains finite source-feedback kernels for all physics source/readout arenas."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    pi_split: list[dict[str, object]],
    zero_conditions: list[dict[str, object]],
    kernels: list[dict[str, object]],
    arena: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2123 - Y5/R2FR Readout Projection Commutator Zero Or Finite Kernel Bound",
            "## Current Verdict",
            "2123 gets a real but limited derivation win. The projection commutator is zero for genuinely post-variation reports: maps that only read solved histories and never feed back into the parent action, Hilbert source, coefficient extraction, source normalization or calibration. That part is now closed by type.",
            "The physically dangerous part is not closed. Source-feedback projectors, finite-source support maps, GM calibration guards, material/readout masks, orbit windows and boundary transports can contribute `(delta Pi)J`. Unless those structures descend through `q/e_obs` or are declared as fixed external protocol before variation, they remain finite kernels. Therefore this checkpoint tightens the bridge but still does not allow a local GR/Newton/PPN claim.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Pi Split Theorem",
            md_table(pi_split, ["split_id", "projection_class", "proof_status", "exact_statement", "residual_status", "zero_ready", "valid_for_claim"]),
            "## Zero Conditions",
            md_table(zero_conditions, ["condition_id", "condition", "mathematical_test", "current_status", "missing_input", "valid_for_claim"]),
            "## Finite Kernel Bound Rows",
            md_table(kernels, ["kernel_id", "arena", "bound_shape", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "## Arena Verdict",
            md_table(arena, ["arena_id", "arena", "verdict", "consequence", "next_action", "valid_for_claim"]),
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
    pi_split = pi_split_rows()
    zero_conditions = zero_condition_rows()
    kernels = finite_kernel_rows()
    arena = arena_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2123_SOURCE_REGISTER.csv",
        "pi_split": OUT / "P8_Y5_PARENT_QLOC_2123_PI_SPLIT_THEOREM.csv",
        "zero_conditions": OUT / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_ZERO_CONDITIONS.csv",
        "kernels": OUT / "P8_Y5_PARENT_QLOC_2123_FINITE_KERNEL_BOUND_ROWS.csv",
        "arena": OUT / "P8_Y5_PARENT_QLOC_2123_ARENA_VERDICT.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2123_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2123_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2123_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2123_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2123_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["pi_split"], pi_split)
    write_csv(paths["zero_conditions"], zero_conditions)
    write_csv(paths["kernels"], kernels)
    write_csv(paths["arena"], arena)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(pi_split, kernels, arena, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, pi_split, zero_conditions, kernels, arena, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, pi_split, zero_conditions, kernels, arena, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
