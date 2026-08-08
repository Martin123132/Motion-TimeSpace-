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


DOC = ROOT / "2117-Y5-R2FR-canonical-owned-coframe-action-promotion-or-sector-exceptions-ledger.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2116_NEXT = OUT / "P8_Y5_PARENT_QLOC_2116_NEXT_TARGET.csv"
CSV_2116_SIGNATURE = OUT / "P8_Y5_PARENT_QLOC_2116_PARENT_SPIN_SIGNATURE_AUDIT.csv"
CSV_2116_AXIAL = OUT / "P8_Y5_PARENT_QLOC_2116_AXIAL_COMPONENT_SOURCE_VALUES.csv"
CSV_2116_VAL = OUT / "P8_Y5_BRR545_2116_VALIDATION.csv"

CSV_2114_SECTOR = OUT / "P8_Y5_PARENT_QLOC_2114_SECTOR_GAMMA_SLOT_AUDIT.csv"
CSV_2114_ARENA = OUT / "P8_Y5_PARENT_QLOC_2114_ARENA_IMPACT.csv"
CSV_2114_CMTS = OUT / "P8_Y5_PARENT_QLOC_2114_CMTS_SOURCE_PACK.csv"

CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"
CSV_1963_NOGAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"
CSV_1309_MATTER = OUT / "P8_Y5_R10_1309_MATTER_CONSTANT_PREMISE_GATE.csv"
CSV_943_COFRAME = OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
CSV_944_DESCENT = OUT / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv"
CSV_988_EM = OUT / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv"
CSV_989_EM = OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv"
CSV_1068_SOURCE = OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv"
CSV_1068_ORBIT = OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv"
CSV_1071_KERNEL = OUT / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv"
CSV_1209_DOMAIN = OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
CSV_2099_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv"
CSV_2099_BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_2099_SCORE_BLOCKERS.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2117_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2117-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2117*",
        "*Y5_R2FR_canonical_owned_coframe_action_promotion_or_sector_exceptions_ledger_2117*",
        "*AFRAME_CANONICAL_OWNED_COFRAME_2117*",
        "*JR2117_SOURCE_READOUT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2117_00_2116_next", CSV_2116_NEXT, ["NEXT2116_0_2117", "sector exceptions"], "2116 selects canonical owned-coframe promotion or sector exceptions."),
        ("SRC2117_01_2116_signature", CSV_2116_SIGNATURE, ["PSS2116_6_verdict", "SIGNED_INSIDE_1963_CANDIDATE_NOT_GLOBAL_CORPUS"], "2116 closes spin only inside the 1963 candidate branch."),
        ("SRC2117_02_2116_axial", CSV_2116_AXIAL, ["ACV2116_0_xi_A_candidate_branch", "DERIVED_ZERO_ONLY_INSIDE_CANDIDATE_BRANCH"], "2116 derives xi_A zero only inside the candidate branch."),
        ("SRC2117_03_2116_validation", CSV_2116_VAL, ["VAL2116_OVERALL", "PASS"], "2116 validation passed."),
        ("SRC2117_04_1963_action", CSV_1963_ACTION, ["ACT1963_0_target", "ACT1963_5_no_independent_Gamma_clause", "FORWARD_LEAP_NOT_FINAL_CLAIM"], "1963 candidate parent action and status."),
        ("SRC2117_05_1963_nogamma", CSV_1963_NOGAMMA, ["NGT1963_0_theorem", "NGT1963_1_spinor_guard", "NGT1963_3_not_EH"], "1963 no-Gamma theorem and scope limit."),
        ("SRC2117_06_2114_sector", CSV_2114_SECTOR, ["SGS2114_0_gravity_geometry", "SGS2114_9_verdict", "FAIL_CURRENT_CLAIM"], "2114 all-sector Gamma-slot audit."),
        ("SRC2117_07_2114_arena", CSV_2114_ARENA, ["ARENA2114_1_WEP", "ARENA2114_5_ORBIT", "MISSING_PROJECTION_MATRIX"], "2114 arena impact ledger."),
        ("SRC2117_08_2114_cmts", CSV_2114_CMTS, ["CMTS2114_8_total", "NOT_RUN_COMPONENTS_MISSING"], "2114 C_MTS total residual pack."),
        ("SRC2117_09_1309_matter", CSV_1309_MATTER, ["MCG1309_0_observed_coframe", "CONDITIONAL_NOT_PARENT_DERIVED"], "1309 matter coframe/spin connection condition."),
        ("SRC2117_10_943_coframe", CSV_943_COFRAME, ["CFC943_4_connection_lock", "contract_exact_but_unsigned"], "943 coframe coupling contract remains unsigned."),
        ("SRC2117_11_944_descent", CSV_944_DESCENT, ["QDG944_4_geometry_stack_descent", "not_proved_current_corpus"], "944 descent proof gate remains conditional."),
        ("SRC2117_12_988_em", CSV_988_EM, ["EMLOCK988_5_theorem_verdict", "conditional_exact_but_not_promoted"], "988 EM lock theorem not promoted."),
        ("SRC2117_13_989_em", CSV_989_EM, ["ELA989_5_total", "not_promoted"], "989 EM lock signature audit not promoted."),
        ("SRC2117_14_1068_source", CSV_1068_SOURCE, ["SWT1068_5_verdict", "SOURCE_WORLDTUBE_NOT_ACQUIRED"], "1068 source worldtube not acquired."),
        ("SRC2117_15_1068_orbit", CSV_1068_ORBIT, ["ORB1068_5_verdict", "ORBIT_READOUT_NOT_ACQUIRED"], "1068 orbit/readout not acquired."),
        ("SRC2117_16_1071_kernel", CSV_1071_KERNEL, ["KER1071_6_verdict", "KERNEL_SKELETON_YES_NUMERIC_TAU_NO"], "1071 official kernel skeleton without numeric tau."),
        ("SRC2117_17_1209_domain", CSV_1209_DOMAIN, ["DMP1209_4_total_epsilon_status", "LOWERED_NOT_NUMERIC"], "1209 domain/projector stress still not numeric/parent-signed."),
        ("SRC2117_18_2099_components", CSV_2099_COMPONENTS, ["DGM2099_0_spin", "DGM2099_6_projective", "MAP_REGISTERED_PROJECTION_MISSING"], "2099 component projection maps still missing."),
        ("SRC2117_19_2099_blockers", CSV_2099_BLOCKERS, ["SBL2099_0_component_values", "SBL2099_4_no_cancellation"], "2099 score blockers and no-cancellation guard."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    return rows


def canonical_promotion_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="COP2117_0_candidate_action_text",
            requirement="owned-coframe parent action text exists",
            current_status="PASS_CANDIDATE",
            evidence="ACT1963_0_target and ACT1963_5_no_independent_Gamma_clause",
            implication="candidate branch is concrete enough to audit sector by sector",
            missing_for_activation="canonical parent selection and full sector exception closure",
            activation_ready=False,
        ),
        row(
            gate_id="COP2117_1_spin_exception",
            requirement="spin has no independent contorsion/axial current",
            current_status="PASS_INSIDE_CANDIDATE_ONLY",
            evidence="PSS2116_6_verdict and ACV2116_0_xi_A_candidate_branch",
            implication="spin is no longer the leading blocker if the owned-coframe branch is adopted",
            missing_for_activation="promote candidate branch globally",
            activation_ready=False,
        ),
        row(
            gate_id="COP2117_2_all_sector_coverage",
            requirement="all ordinary sectors are Gamma-free/coframe-owned",
            current_status="FAIL_CURRENT_CORPUS",
            evidence="SGS2114_9_verdict",
            implication="LC/local-GR activation cannot happen yet",
            missing_for_activation="close EM/source/clock/light/orbit/boundary/projective exceptions",
            activation_ready=False,
        ),
        row(
            gate_id="COP2117_3_observable_projection",
            requirement="residual maps to R10/WEP/PPN/clock/light/orbit are zero or bounded",
            current_status="FAIL_SCORE_READY",
            evidence="ARENA2114_* and SBL2099_*",
            implication="even if action text is adopted, empirical local gates need projection matrices or zeros",
            missing_for_activation="projection matrices, response operators, numeric kernels or theorem-zero certificates",
            activation_ready=False,
        ),
        row(
            gate_id="COP2117_4_verdict",
            requirement="promote 1963 to canonical local parent branch",
            current_status="PROMOTION_BLOCKED_BY_SECTOR_EXCEPTIONS",
            evidence="2116 spin pass plus 2114/988/989/1068/1209/2099 blockers",
            implication="do not demote 1963; use it as the working branch and close exceptions one by one",
            missing_for_activation="sector exception ledger resolution",
            activation_ready=False,
        ),
    ]


def sector_exception_rows() -> list[dict[str, object]]:
    return [
        row(
            exception_id="SEC2117_0_gravity_geometry",
            sector="gravity/observed geometry",
            candidate_status="OWNED_COFRAME_CANDIDATE_EXISTS",
            current_exception="q/e_obs functor and local geometry operator not canonically selected",
            residual_if_open="C_MTS master residual; higher-curvature/local-operator residual",
            source_anchor="ACT1963_3_geometry_term; SGS2114_0_gravity_geometry",
            closure_action="promote owned coframe branch or prove multifield rank map into e_obs",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_1_ordinary_matter",
            sector="ordinary matter",
            candidate_status="MATTER_FUNCTOR_WRITTEN_CANDIDATE",
            current_exception="universal matter functor remains conditional, direct Xi/q_loc/species-marker dependence not fully excluded",
            residual_if_open="Delta_matter; material_marker_connection_current",
            source_anchor="ACT1963_4_matter_functor; MCG1309_0_observed_coframe; SGS2114_1_ordinary_matter",
            closure_action="sector-by-sector matter/readout audit for direct representative or species-marker couplings",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_2_spin",
            sector="spinor/spin transport",
            candidate_status="CLOSED_INSIDE_CANDIDATE_BRANCH",
            current_exception="not globally canonical yet",
            residual_if_open="Delta_spin_axial only if independent torsionful spin connection is reintroduced",
            source_anchor="PSS2116_6_verdict; ACV2116_0_xi_A_candidate_branch; SGS2114_2_spin",
            closure_action="carry as branch-zero while canonicalization proceeds; keep affine fallback if branch rejected",
            zero_ready=True,
        ),
        row(
            exception_id="SEC2117_3_EM_gauge",
            sector="EM/internal gauge",
            candidate_status="OWNED_GAUGE_PLACEHOLDER_PRESENT",
            current_exception="T_Q owner, unique F2, current owner, readout descent and no-alpha vertex unsigned",
            residual_if_open="material_marker_connection_current; alpha_EM residual; charge/source normalization residual",
            source_anchor="EMLOCK988_5_theorem_verdict; ELA989_5_total; SGS2114_3_EM_gauge",
            closure_action="prove compact charge-generator owner and no separate alpha vertex, or keep EM residual rows",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_4_source_worldtube",
            sector="source/worldtube",
            candidate_status="NOT_CLOSED",
            current_exception="source stress profile, composition, finite-source support and frame units missing",
            residual_if_open="Delta_source; source_support_connection_current",
            source_anchor="SWT1068_5_verdict; SGS2114_4_source_worldtube; DGM2099_2_source_support",
            closure_action="source worldtube theorem-zero or source-backed kernel/profile acquisition",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_5_clocks_rods_light",
            sector="clocks/rods/lightcones",
            candidate_status="NOT_CLOSED",
            current_exception="clock/rod/light readout functions and nonmetricity response operators not parent-signed",
            residual_if_open="Delta_clock_light; Q_trace; Q_shear",
            source_anchor="SGS2114_5_clocks_rods_light; DGM2099_3_clock_rods; DGM2099_4_photon_lightcone",
            closure_action="derive metric-only readout from owned coframe or fill clock/light response operators",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_6_orbital_readout",
            sector="orbital/Newton/GM readout",
            candidate_status="NOT_CLOSED",
            current_exception="orbit/source-GM transfer and fitted-G absorption guard remain missing",
            residual_if_open="Delta_orbit; orbital_readout_connection_current",
            source_anchor="ORB1068_5_verdict; KER1071_6_verdict; SGS2114_6_orbital_readout; DGM2099_5_orbital_readout",
            closure_action="official orbit/readout kernel plus GM transfer convention, or theorem-zero downstream functor",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_7_boundary_nonHilbert",
            sector="boundary/non-Hilbert/domain",
            candidate_status="NOT_CLOSED",
            current_exception="boundary/support/domain motion/projector stress clauses not parent-signed or numeric",
            residual_if_open="Delta_boundary; K_comm; K_boundary; epsilon_geom",
            source_anchor="DMP1209_4_total_epsilon_status; SGS2114_7_boundary_nonHilbert",
            closure_action="proper support/domain/readout collar theorem or finite residual bounds",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_8_projective_trace",
            sector="projective trace",
            candidate_status="NOT_CLOSED",
            current_exception="all-sector projective invariance proof missing",
            residual_if_open="projective_trace_current",
            source_anchor="SGS2114_8_projective_trace; DGM2099_6_projective",
            closure_action="prove projective mode is gauge/unobservable in every sector or bound trace coupling",
            zero_ready=False,
        ),
        row(
            exception_id="SEC2117_9_verdict",
            sector="all sectors",
            candidate_status="PROMOTION_BLOCKED",
            current_exception="only spin closes inside candidate; multiple local sectors retain exceptions",
            residual_if_open="Delta_Gamma_abs with no cancellation",
            source_anchor="SGS2114_9_verdict; CMTS2114_8_total; SBL2099_4_no_cancellation",
            closure_action="close source/readout/boundary/projective exceptions next",
            zero_ready=False,
        ),
    ]


def activation_matrix_rows() -> list[dict[str, object]]:
    return [
        row(matrix_id="Z2117_0_spin", zero_object="Delta_spin_axial", branch_zero=True, global_zero=False, reason="2116 signs spin only inside 1963 candidate", blocker="candidate not canonical globally"),
        row(matrix_id="Z2117_1_matter", zero_object="Delta_matter", branch_zero=False, global_zero=False, reason="matter functor candidate exists", blocker="direct Xi/q_loc/species-marker audit incomplete"),
        row(matrix_id="Z2117_2_EM", zero_object="alpha_EM/material current residual", branch_zero=False, global_zero=False, reason="owned gauge placeholder exists", blocker="T_Q/current/no-alpha clauses unsigned"),
        row(matrix_id="Z2117_3_source", zero_object="source_support_connection_current", branch_zero=False, global_zero=False, reason="source leg can be downstream in owned-coframe branch", blocker="source worldtube not acquired"),
        row(matrix_id="Z2117_4_clock_light", zero_object="clock/light nonmetricity currents", branch_zero=False, global_zero=False, reason="metric readout desired", blocker="response operators and readout descent missing"),
        row(matrix_id="Z2117_5_orbit", zero_object="orbital_readout_connection_current", branch_zero=False, global_zero=False, reason="orbits should be downstream functors", blocker="kernel/GM transfer/fitted-G guard missing"),
        row(matrix_id="Z2117_6_boundary", zero_object="boundary/domain/projector residuals", branch_zero=False, global_zero=False, reason="proper collar theorem may close pieces", blocker="domain/projector stress not parent-signed/numeric"),
        row(matrix_id="Z2117_7_projective", zero_object="projective_trace_current", branch_zero=False, global_zero=False, reason="could be gauge", blocker="all-sector invariance proof missing"),
        row(matrix_id="Z2117_8_LC_activation", zero_object="K_conn and Delta_Gamma_abs", branch_zero=False, global_zero=False, reason="owned-coframe branch is promising", blocker="sector exceptions survive; no cancellation allowed"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2117_0_candidate_branch_retained", gate="1963 owned-coframe branch remains best local-GR route", gate_pass=True, rationale="spin/coupling closure shows the branch has real theorem power"),
        row(gate_id="GATE2117_1_spin_blocker_lowered", gate="spin is no longer leading blocker inside candidate branch", gate_pass=True, rationale="2116 derives xi_A=0 only by variable absence in the candidate"),
        row(gate_id="GATE2117_2_canonical_promotion", gate="owned-coframe branch is canonical/global", gate_pass=False, rationale="sector exceptions and descent gates remain open"),
        row(gate_id="GATE2117_3_all_sector_zero", gate="all Gamma slots zero or residualized", gate_pass=False, rationale="EM/source/clock/light/orbit/boundary/projective exceptions survive"),
        row(gate_id="GATE2117_4_empirical_projection_ready", gate="R10/WEP/PPN/clock/light/orbit projections score-ready", gate_pass=False, rationale="projection matrices, response operators and numeric kernels are missing"),
        row(gate_id="GATE2117_5_local_GR_Newton", gate="derived local GR/Newton may be claimed", gate_pass=False, rationale="LC activation plus EH/source/readout/PPN gates are still not closed"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2117_0", decision="OWNED_COFRAME_BRANCH_RETAINED", because="2116 made the spin/coupling problem derivably clean inside the 1963 branch.", next_action="Do not abandon this route; canonicalize it by closing sector exceptions."),
        row(decision_id="DEC2117_1", decision="PROMOTION_NOT_ALLOWED_YET", because="2114 plus EM/source/readout/domain ledgers show multiple live exceptions.", next_action="Keep the work private/nonclaim and retain Delta_Gamma_abs outside proven zeros."),
        row(decision_id="DEC2117_2", decision="SOURCE_READOUT_EXCEPTIONS_NEXT", because="after spin, source/worldtube, clock/light/orbit readout, boundary and projective clauses dominate local-GR risk.", next_action="attack source/readout Gamma silence or write explicit kernels/bounds."),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2117_0_2118",
            next_target="2118-Y5-R2FR-source-readout-Gamma-silence-or-explicit-exception-kernels.md",
            script="scripts/Y5_R2FR_source_readout_Gamma_silence_or_explicit_exception_kernels_2118.py",
            objective="Try to close the largest remaining owned-coframe exceptions: source worldtube, clock/rod/lightcone readout, orbital/GM transfer, boundary/domain and projective trace. Prove theorem-zero where possible; otherwise write explicit residual kernels and source queues.",
            forbidden_shortcuts="claiming 1963 is canonical; ignoring EM/source/readout exceptions; fitted-G absorption; cancellation between residuals; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    promotion_rows: list[dict[str, object]],
    exceptions: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2117_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_CANONICAL_OWNED_COFRAME_2117_NONCLAIM.csv", promotion_rows + exceptions + matrix_rows),
        ("COPY2117_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTIONS_NONCLAIM.csv", exceptions + matrix_rows),
        ("COPY2117_2_acquisition_queue", QUEUE / "JR2117_SOURCE_READOUT_EXCEPTION_CLOSURE_QUEUE.csv", next_rows + exceptions),
    ]
    result: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        result.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return result


def validation_rows(
    sources: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    exceptions: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    promotion_blocked_ok = any(item["gate_id"] == "COP2117_4_verdict" and item["current_status"] == "PROMOTION_BLOCKED_BY_SECTOR_EXCEPTIONS" for item in promotion_rows)
    spin_lowered_ok = any(item["exception_id"] == "SEC2117_2_spin" and truthy(item["zero_ready"]) for item in exceptions)
    exceptions_block_ok = any(item["exception_id"] == "SEC2117_9_verdict" and item["candidate_status"] == "PROMOTION_BLOCKED" for item in exceptions)
    lc_false_ok = any(item["matrix_id"] == "Z2117_8_LC_activation" and not truthy(item["branch_zero"]) and not truthy(item["global_zero"]) for item in matrix_rows)
    gates_ok = (
        any(item["gate_id"] == "GATE2117_1_spin_blocker_lowered" and truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "GATE2117_2_canonical_promotion" and not truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "GATE2117_5_local_GR_Newton" and not truthy(item["gate_pass"]) for item in gates)
    )
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, promotion_rows, exceptions, matrix_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2117_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    next_ok = any(item["route_id"] == "NEXT2117_0_2118" for item in next_rows)
    all_ok = all([sources_ok, promotion_blocked_ok, spin_lowered_ok, exceptions_block_ok, lc_false_ok, gates_ok, no_claim_flags, branch_ok, csv_ok, formalization_clean, pycache_clean, next_ok])
    checks = [
        ("VAL2117_00_sources", sources_ok, "all cited canonicalization/sector sources exist and contain expected needles"),
        ("VAL2117_01_promotion_blocked", promotion_blocked_ok, "canonical promotion is explicitly blocked by sector exceptions"),
        ("VAL2117_02_spin_lowered", spin_lowered_ok, "spin is marked zero-ready only inside the candidate branch"),
        ("VAL2117_03_exception_verdict", exceptions_block_ok, "sector exception ledger blocks global LC activation"),
        ("VAL2117_04_lc_matrix", lc_false_ok, "LC activation matrix remains false globally"),
        ("VAL2117_05_claim_gates", gates_ok, "spin progress passes but canonical/local-GR gates fail"),
        ("VAL2117_06_no_claim_flags", no_claim_flags, "no generated row allows a claim or score"),
        ("VAL2117_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2117_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2117_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2117"),
        ("VAL2117_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2117_11_next", next_ok, "next target selects source/readout Gamma silence or explicit exception kernels"),
        ("VAL2117_OVERALL", all_ok, "2117 keeps the owned-coframe route, lowers the spin blocker, blocks canonical promotion on remaining sector exceptions, and selects source/readout closure next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    exceptions: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2117 - Y5/R2FR Canonical Owned-Coframe Action Promotion Or Sector Exceptions Ledger",
            "## Current Verdict",
            "2117 confirms the project is not merely circling. The 1963 owned-coframe branch remains the best route because 2116 turned the spin/coupling problem into a branch-zero theorem: inside that candidate branch, spin does not need a KRT rescue.",
            "But the branch cannot yet be promoted to global/canonical local GR. The remaining blockers are sector exceptions: EM-lock, source worldtube, clock/rod/lightcone readout, orbital/GM transfer, boundary/domain/projector stress, and projective trace. These must be theorem-zeroed or written as explicit residual kernels.",
            "So the status is stronger and sharper: spin is lowered; canonical promotion is blocked by named non-spin sectors; next work should attack source/readout Gamma silence rather than keep poking the same spin wound.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Canonical Promotion Gate",
            md_table(promotion_rows, ["gate_id", "requirement", "current_status", "evidence", "implication", "missing_for_activation", "activation_ready", "valid_for_claim"]),
            "## Sector Exception Ledger",
            md_table(exceptions, ["exception_id", "sector", "candidate_status", "current_exception", "residual_if_open", "closure_action", "zero_ready", "valid_for_claim"]),
            "## Zero Activation Matrix",
            md_table(matrix_rows, ["matrix_id", "zero_object", "branch_zero", "global_zero", "reason", "blocker", "valid_for_claim"]),
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
    promotion_rows = canonical_promotion_rows()
    exceptions = sector_exception_rows()
    matrix_rows = activation_matrix_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2117_SOURCE_REGISTER.csv",
        "promotion": OUT / "P8_Y5_PARENT_QLOC_2117_CANONICAL_PROMOTION_GATE.csv",
        "exceptions": OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv",
        "matrix": OUT / "P8_Y5_PARENT_QLOC_2117_ZERO_ACTIVATION_MATRIX.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2117_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2117_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2117_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2117_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2117_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["promotion"], promotion_rows)
    write_csv(paths["exceptions"], exceptions)
    write_csv(paths["matrix"], matrix_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(promotion_rows, exceptions, matrix_rows, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, promotion_rows, exceptions, matrix_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, promotion_rows, exceptions, matrix_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
