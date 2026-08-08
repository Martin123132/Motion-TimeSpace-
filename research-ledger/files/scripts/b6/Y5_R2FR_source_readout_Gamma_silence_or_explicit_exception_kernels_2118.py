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


DOC = ROOT / "2118-Y5-R2FR-source-readout-Gamma-silence-or-explicit-exception-kernels.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2117_NEXT = OUT / "P8_Y5_PARENT_QLOC_2117_NEXT_TARGET.csv"
CSV_2117_EXC = OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv"
CSV_2117_MATRIX = OUT / "P8_Y5_PARENT_QLOC_2117_ZERO_ACTIVATION_MATRIX.csv"
CSV_2117_PROMOTION = OUT / "P8_Y5_PARENT_QLOC_2117_CANONICAL_PROMOTION_GATE.csv"
CSV_2117_VAL = OUT / "P8_Y5_BRR545_2117_VALIDATION.csv"

CSV_1068_SOURCE = OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv"
CSV_1068_ORBIT = OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv"
CSV_1071_KERNEL = OUT / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv"
CSV_1209_DOMAIN = OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
CSV_2099_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv"
CSV_2099_BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_2099_SCORE_BLOCKERS.csv"
CSV_2114_ARENA = OUT / "P8_Y5_PARENT_QLOC_2114_ARENA_IMPACT.csv"
CSV_2114_CMTS = OUT / "P8_Y5_PARENT_QLOC_2114_CMTS_SOURCE_PACK.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2118_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2118-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2118*",
        "*Y5_R2FR_source_readout_Gamma_silence_or_explicit_exception_kernels_2118*",
        "*AFRAME_SOURCE_READOUT_2118*",
        "*JR2118_SOURCE_READOUT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2118_00_2117_next", CSV_2117_NEXT, ["NEXT2117_0_2118", "source-readout-Gamma-silence"], "2117 selects source/readout Gamma silence or explicit kernels."),
        ("SRC2118_01_2117_exceptions", CSV_2117_EXC, ["SEC2117_4_source_worldtube", "SEC2117_9_verdict", "PROMOTION_BLOCKED"], "2117 sector exception ledger."),
        ("SRC2118_02_2117_matrix", CSV_2117_MATRIX, ["Z2117_8_LC_activation", "sector exceptions survive"], "2117 keeps LC activation false."),
        ("SRC2118_03_2117_promotion", CSV_2117_PROMOTION, ["COP2117_4_verdict", "PROMOTION_BLOCKED_BY_SECTOR_EXCEPTIONS"], "2117 canonical promotion verdict."),
        ("SRC2118_04_2117_validation", CSV_2117_VAL, ["VAL2117_OVERALL", "PASS"], "2117 validation passed."),
        ("SRC2118_05_1068_source", CSV_1068_SOURCE, ["SWT1068_5_verdict", "SOURCE_WORLDTUBE_NOT_ACQUIRED"], "source worldtube requirements."),
        ("SRC2118_06_1068_orbit", CSV_1068_ORBIT, ["ORB1068_5_verdict", "ORBIT_READOUT_NOT_ACQUIRED"], "MICROSCOPE orbit/readout requirements."),
        ("SRC2118_07_1071_kernel", CSV_1071_KERNEL, ["KER1071_6_verdict", "KERNEL_SKELETON_YES_NUMERIC_TAU_NO"], "official MICROSCOPE kernel skeleton."),
        ("SRC2118_08_1209_domain", CSV_1209_DOMAIN, ["DMP1209_0_domain_motion_zero_branch", "DMP1209_4_total_epsilon_status"], "domain/projector stress audit."),
        ("SRC2118_09_2099_components", CSV_2099_COMPONENTS, ["DGM2099_2_source_support", "DGM2099_6_projective", "MAP_REGISTERED_PROJECTION_MISSING"], "DeltaGamma component map."),
        ("SRC2118_10_2099_blockers", CSV_2099_BLOCKERS, ["SBL2099_0_component_values", "SBL2099_4_no_cancellation"], "score blockers and no-cancellation guard."),
        ("SRC2118_11_2114_arena", CSV_2114_ARENA, ["ARENA2114_0_R10", "ARENA2114_5_ORBIT", "MISSING_PROJECTION_MATRIX"], "arena impact matrix."),
        ("SRC2118_12_2114_cmts", CSV_2114_CMTS, ["CMTS2114_8_total", "NOT_RUN_COMPONENTS_MISSING"], "DeltaGamma total source pack."),
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


def zero_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="SRZ2118_0_source_worldtube_zero",
            target="source_support_connection_current",
            conditional_zero_statement="If S_source, support tube, source weights and finite-source profile are functionals only of q/e_obs and calibrated common-mode GM, then no independent Gamma-source current survives.",
            current_status="CONDITIONAL_ZERO_NOT_SIGNED",
            evidence="SWT1068_5_verdict says source worldtube not acquired; SEC2117_4_source_worldtube remains not closed.",
            missing_for_zero="source stress/profile, composition convention, finite-source support, frame units or theorem reducing them to owned coframe",
            fallback_kernel="KSR2118_0_source_worldtube_kernel",
            zero_ready=False,
        ),
        row(
            theorem_id="SRZ2118_1_clock_rod_zero",
            target="clock_rod_nonmetric_connection_current",
            conditional_zero_statement="If clocks and rods read only proper time/length from g_obs=e_obs^T eta e_obs with fixed matter constants, Weyl/nonmetric readout currents vanish.",
            current_status="CONDITIONAL_ZERO_NOT_SIGNED",
            evidence="DGM2099_3_clock_rods and ARENA2114_3_CLOCK require response operators.",
            missing_for_zero="clock functional, rod calibration functional, Q_trace normalization, redshift bound source or parent readout theorem",
            fallback_kernel="KSR2118_2_clock_redshift_kernel",
            zero_ready=False,
        ),
        row(
            theorem_id="SRZ2118_2_lightcone_zero",
            target="photon_lightcone_connection_current",
            conditional_zero_statement="If photon/lightcone propagation is the null cone of g_obs plus owned EM gauge data only, trace-free nonmetric/shear-lightcone currents vanish.",
            current_status="CONDITIONAL_ZERO_NOT_SIGNED",
            evidence="DGM2099_4_photon_lightcone and ARENA2114_4_LIGHT require lightcone response operator.",
            missing_for_zero="lightcone response operator, photon/readout branch, gauge convention and PPN gamma map",
            fallback_kernel="KSR2118_3_lightcone_kernel",
            zero_ready=False,
        ),
        row(
            theorem_id="SRZ2118_3_orbital_GM_zero",
            target="orbital_readout_connection_current",
            conditional_zero_statement="If orbit/GM readout is a downstream functor of source measure, Poisson/Gauss calibration and g_obs geodesic motion, no direct readout Gamma current survives.",
            current_status="CONDITIONAL_ZERO_NOT_SIGNED",
            evidence="ORB1068_5_verdict says orbit/readout not acquired; KER1071_6 has skeleton but numeric tau no.",
            missing_for_zero="official orbit/attitude/source arrays, GM transfer convention, fitted-G absorption guard and time/range law",
            fallback_kernel="KSR2118_1_orbit_WEP_kernel; KSR2118_4_orbital_GM_kernel",
            zero_ready=False,
        ),
        row(
            theorem_id="SRZ2118_4_boundary_domain_zero",
            target="Delta_boundary; K_boundary; K_comm; epsilon_geom",
            conditional_zero_statement="If support tube, boundary, time normal, projector and weights are fixed by the same Fermi/parent readout map, domain-motion and projector-stress currents vanish.",
            current_status="CONDITIONAL_ZERO_NOT_SIGNED",
            evidence="DMP1209_0 and DMP1209_2 give zero branches but DMP1209_4 remains lowered not numeric.",
            missing_for_zero="domain id, central worldline, support map, boundary transport, readout channel, support weight and projector stress norm",
            fallback_kernel="KSR2118_5_boundary_domain_kernel",
            zero_ready=False,
        ),
        row(
            theorem_id="SRZ2118_5_projective_zero",
            target="projective_trace_current",
            conditional_zero_statement="If every sector is projectively invariant or the trace mode is fixed before matter/readout coupling, projective trace is gauge and unobservable.",
            current_status="CONDITIONAL_ZERO_NOT_SIGNED",
            evidence="DGM2099_6_projective and SEC2117_8_projective_trace say all-sector certificate is missing.",
            missing_for_zero="projective gauge rule, all-sector invariance proof, source/readout trace coupling bound",
            fallback_kernel="KSR2118_6_projective_trace_kernel",
            zero_ready=False,
        ),
        row(
            theorem_id="SRZ2118_6_verdict",
            target="source/readout Gamma silence",
            conditional_zero_statement="All source/readout zero clauses must be signed before canonical owned-coframe LC activation.",
            current_status="ZERO_THEOREM_NOT_CLOSED",
            evidence="2117 exception ledger plus 1068/1071/1209/2099 blockers.",
            missing_for_zero="source, clock/light, orbit, boundary/domain and projective clauses",
            fallback_kernel="Delta_Gamma_abs no-cancellation kernel suite",
            zero_ready=False,
        ),
    ]


def explicit_kernel_rows() -> list[dict[str, object]]:
    return [
        row(
            kernel_id="KSR2118_0_source_worldtube_kernel",
            residual_component="source_support_connection_current",
            kernel_shape="Delta_source(lambda) = integral d^3x K_source(x,lambda; e_obs, support) * rho_source_residual(x)",
            observable_links="R10 alpha(lambda); PPN gamma/beta; orbital_GM; WEP source leg",
            required_inputs="T_source^Earth(x); composition/source-charge convention; finite-source support; frame units; common-mode GM guard",
            current_status="KERNEL_SHAPE_ONLY_INPUTS_MISSING",
            source_anchor="SWT1068_0..5; DGM2099_2_source_support",
            score_ready=False,
        ),
        row(
            kernel_id="KSR2118_1_orbit_WEP_kernel",
            residual_component="tau_WEP orbit/source projection",
            kernel_shape="tau_WEP = < P_inst(t) [Delta_a_source(t)-Delta_a_test(t)] >_segments using official gx,gz,Sxx,Sxz basis",
            observable_links="MICROSCOPE eta_AB; WEP; source/readout local coupling",
            required_inputs="orbit ephemeris; attitude axis; eta convention; environmental model; segment averaging kernel",
            current_status="OFFICIAL_FORM_SKELETON_NUMERIC_INPUTS_MISSING",
            source_anchor="ORB1068_0..5; KER1071_0..6",
            score_ready=False,
        ),
        row(
            kernel_id="KSR2118_2_clock_redshift_kernel",
            residual_component="clock_rod_nonmetric_connection_current",
            kernel_shape="delta_nu/nu = P_clock[Q_trace, rod calibration, material markers, projective trace]",
            observable_links="clock/redshift; WEP clock leg; local-GR redshift",
            required_inputs="clock functional; rod calibration functional; Q_trace normalization; redshift bound source; material-marker exclusion",
            current_status="RESPONSE_OPERATOR_MISSING",
            source_anchor="DGM2099_3_clock_rods; ARENA2114_3_CLOCK",
            score_ready=False,
        ),
        row(
            kernel_id="KSR2118_3_lightcone_kernel",
            residual_component="photon_lightcone_connection_current",
            kernel_shape="gamma_minus_1 or Shapiro residual = P_lightcone[Q_shear, photon branch, source geometry]",
            observable_links="PPN gamma; Shapiro/lightcone; clock cross-check",
            required_inputs="trace-free Q normalization; photon/readout branch; gauge choice; lightcone response operator",
            current_status="RESPONSE_OPERATOR_MISSING",
            source_anchor="DGM2099_4_photon_lightcone; ARENA2114_4_LIGHT",
            score_ready=False,
        ),
        row(
            kernel_id="KSR2118_4_orbital_GM_kernel",
            residual_component="orbital_readout_connection_current",
            kernel_shape="delta(GM)_obs or fifth-force residual = P_orbit[source_support, readout_action, inverse-square split, time/range law]",
            observable_links="orbital_GM; Gdot/G; R10; PPN beta/gamma",
            required_inputs="source-readout action; GM calibration convention; range law; no fitted-G absorption proof",
            current_status="GM_TRANSFER_KERNEL_MISSING",
            source_anchor="DGM2099_5_orbital_readout; ARENA2114_5_ORBIT",
            score_ready=False,
        ),
        row(
            kernel_id="KSR2118_5_boundary_domain_kernel",
            residual_component="epsilon_geom / boundary-domain current",
            kernel_shape="epsilon_geom = C_P*(fermi_curvature_projector_drift + coframe_lock + domain_motion + projector_stress)",
            observable_links="R10 local geometry; source support; conservation; PPN",
            required_inputs="C_P; G_res_norm; support map; boundary transport; weight function; projector stress norm",
            current_status="BOUND_SHAPE_DERIVED_VALUES_MISSING",
            source_anchor="DMP1209_0..4",
            score_ready=False,
        ),
        row(
            kernel_id="KSR2118_6_projective_trace_kernel",
            residual_component="projective_trace_current",
            kernel_shape="projective residual = P_projective[source, clock, WEP] unless all-sector projective-invariance certificate is supplied",
            observable_links="WEP; clock; source charge; projective certificate",
            required_inputs="projective gauge rule; all-sector invariance proof; trace-coupling normalization or bound source",
            current_status="CERTIFICATE_OR_BOUND_MISSING",
            source_anchor="DGM2099_6_projective; SBL2099_3_response_operators",
            score_ready=False,
        ),
        row(
            kernel_id="KSR2118_7_total_no_cancellation",
            residual_component="Delta_Gamma_abs",
            kernel_shape="Delta_Gamma_abs = sum_i abs(P_i component_i) with each component zero-theorem or separately bounded",
            observable_links="all local connection arenas",
            required_inputs="component values/zeros; common units; projection matrices; response operators; no-cancellation ledger",
            current_status="TOTAL_KERNEL_BLOCKED_COMPONENTS_MISSING",
            source_anchor="SBL2099_0..4; CMTS2114_8_total",
            score_ready=False,
        ),
    ]


def acquisition_priority_rows() -> list[dict[str, object]]:
    return [
        row(priority_id="ACQ2118_0_source_readout_theorem", priority_rank=1, target="parent source/readout functor", action="try to prove source, clock/light, orbit, boundary and projective readouts are functionals only of q/e_obs plus owned gauges", success_effect="turn multiple kernels to theorem-zero", valid_for_claim=False),
        row(priority_id="ACQ2118_1_MICROSCOPE_numeric_kernel", priority_rank=2, target="WEP/source-orbit kernel", action="acquire or reconstruct orbit, attitude, gx/gz/Sxx/Sxz arrays and eta convention", success_effect="make tau_WEP projection numerically runnable", valid_for_claim=False),
        row(priority_id="ACQ2118_2_clock_light_response", priority_rank=3, target="clock/light PPN response", action="write metric-only readout theorem or source response operators for Q_trace/Q_shear", success_effect="block or score clock/light residuals", valid_for_claim=False),
        row(priority_id="ACQ2118_3_projective_certificate", priority_rank=4, target="projective trace", action="prove all-sector invariance under Gamma -> Gamma + delta A or retain trace bound", success_effect="remove common guard current", valid_for_claim=False),
        row(priority_id="ACQ2118_4_boundary_domain_values", priority_rank=5, target="domain/projector stress", action="source support maps, weights, boundary transport and C_P/G_res values", success_effect="make epsilon_geom bounded instead of vague", valid_for_claim=False),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2118_0_theorem_attempt", gate="source/readout zero theorem attempted", gate_pass=True, rationale="all major remaining clauses have conditional zero statements and missing inputs"),
        row(gate_id="GATE2118_1_full_zero", gate="source/readout Gamma silence closed", gate_pass=False, rationale="none of source, clock/light, orbit, boundary or projective clauses is parent-signed"),
        row(gate_id="GATE2118_2_kernel_pack", gate="explicit residual kernels staged", gate_pass=True, rationale="kernel shapes and required inputs are now listed for every open source/readout component"),
        row(gate_id="GATE2118_3_score_ready", gate="local residuals score-ready", gate_pass=False, rationale="numeric inputs, response operators, common units and projection matrices are missing"),
        row(gate_id="GATE2118_4_no_cancellation", gate="no-cancellation guard retained", gate_pass=True, rationale="Delta_Gamma_abs remains a sum of absolute components unless exact identities are proven"),
        row(gate_id="GATE2118_5_local_GR_Newton", gate="derived local GR/Newton claim allowed", gate_pass=False, rationale="canonical owned-coframe promotion still blocked by source/readout kernels and EH/source gates"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2118_0", decision="SOURCE_READOUT_ZERO_NOT_CLOSED", because="conditional zero theorems exist but none of the source/readout clauses is parent-signed.", next_action="do not claim canonical LC/local-GR from 1963 yet"),
        row(decision_id="DEC2118_1", decision="KERNEL_SUITE_STAGED", because="each open exception now has an explicit projection/kernel shape and input list.", next_action="use these kernels as the acquisition and future runner contract"),
        row(decision_id="DEC2118_2", decision="BEST_NEXT_MICROSCOPE_OR_PROJECTIVE", because="MICROSCOPE has an official skeleton but lacks numeric arrays; projective trace is a common theoretical guard.", next_action="either acquire numeric WEP kernel inputs or prove all-sector projective invariance"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2118_0_2119",
            next_target="2119-Y5-R2FR-projective-invariance-certificate-or-MICROSCOPE-numeric-kernel-acquisition.md",
            script="scripts/Y5_R2FR_projective_invariance_certificate_or_MICROSCOPE_numeric_kernel_acquisition_2119.py",
            objective="Choose the sharper next fork: prove the all-sector projective trace is gauge/unobservable in the owned-coframe branch, or acquire/reconstruct the MICROSCOPE numeric orbit/source kernel so source/readout residuals become runnable.",
            forbidden_shortcuts="claiming source/readout silence; treating kernel skeleton as numeric data; fitted-G absorption; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(zero_rows: list[dict[str, object]], kernel_rows: list[dict[str, object]], acquisition_rows: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2118_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_SOURCE_READOUT_2118_NONCLAIM.csv", zero_rows + kernel_rows),
        ("COPY2118_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_KERNELS_NONCLAIM.csv", kernel_rows + acquisition_rows),
        ("COPY2118_2_acquisition_queue", QUEUE / "JR2118_SOURCE_READOUT_KERNEL_INPUT_QUEUE.csv", next_rows + acquisition_rows + kernel_rows),
    ]
    result: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        result.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return result


def validation_rows(
    sources: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    kernel_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    zero_not_closed_ok = any(item["theorem_id"] == "SRZ2118_6_verdict" and item["current_status"] == "ZERO_THEOREM_NOT_CLOSED" for item in zero_rows)
    kernels_ok = len(kernel_rows) >= 8 and all(not truthy(item["score_ready"]) for item in kernel_rows)
    required_kernel_terms = " ".join(str(value) for item in kernel_rows for value in item.values())
    kernel_terms_ok = all(term in required_kernel_terms for term in ("source_support_connection_current", "tau_WEP", "clock_rod_nonmetric_connection_current", "photon_lightcone_connection_current", "projective_trace_current", "Delta_Gamma_abs"))
    acquisition_ok = len(acquisition_rows) >= 5
    gates_ok = any(item["gate_id"] == "GATE2118_1_full_zero" and not truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2118_2_kernel_pack" and truthy(item["gate_pass"]) for item in gates)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, zero_rows, kernel_rows, acquisition_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2118_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    next_ok = any(item["route_id"] == "NEXT2118_0_2119" for item in next_rows)
    all_ok = all([sources_ok, zero_not_closed_ok, kernels_ok, kernel_terms_ok, acquisition_ok, gates_ok, no_claim_flags, branch_ok, csv_ok, formalization_clean, pycache_clean, next_ok])
    checks = [
        ("VAL2118_00_sources", sources_ok, "all cited source/readout files exist and contain expected needles"),
        ("VAL2118_01_zero_not_closed", zero_not_closed_ok, "source/readout zero theorem remains explicitly unclosed"),
        ("VAL2118_02_kernel_pack", kernels_ok, "kernel rows are staged and non-score-ready"),
        ("VAL2118_03_kernel_terms", kernel_terms_ok, "kernel pack covers source, WEP/orbit, clock, light, projective and DeltaGamma total"),
        ("VAL2118_04_acquisition", acquisition_ok, "acquisition priorities are staged"),
        ("VAL2118_05_claim_gates", gates_ok, "kernel pack exists but full zero and score gates fail"),
        ("VAL2118_06_no_claim_flags", no_claim_flags, "no generated row allows a claim or score"),
        ("VAL2118_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2118_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2118_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2118"),
        ("VAL2118_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2118_11_next", next_ok, "next target selects projective certificate or MICROSCOPE numeric kernel"),
        ("VAL2118_OVERALL", all_ok, "2118 stages source/readout zero clauses and explicit exception kernels, keeps claims blocked, and selects the next fork."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    kernel_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2118 - Y5/R2FR Source-Readout Gamma Silence Or Explicit Exception Kernels",
            "## Current Verdict",
            "2118 does not close source/readout Gamma silence, but it turns the remaining wall into a proper contract. Each open source/readout exception now has a conditional zero theorem and an explicit fallback kernel.",
            "The owned-coframe route still looks like the right route: if source, clocks, light, orbit, boundary/domain and projective trace are all downstream functionals of `q/e_obs`, their independent Gamma currents vanish by variable absence. But the current corpus has not signed those readout/source clauses.",
            "So the honest status is: spin is lowered, source/readout is the wall, and the next useful step is either a projective-invariance certificate or MICROSCOPE numeric kernel acquisition. No local-GR/Newton/PPN claim follows yet.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Source-Readout Zero Theorem Attempt",
            md_table(zero_rows, ["theorem_id", "target", "current_status", "conditional_zero_statement", "missing_for_zero", "fallback_kernel", "zero_ready", "valid_for_claim"]),
            "## Explicit Exception Kernels",
            md_table(kernel_rows, ["kernel_id", "residual_component", "kernel_shape", "observable_links", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "## Acquisition Priorities",
            md_table(acquisition_rows, ["priority_id", "priority_rank", "target", "action", "success_effect", "valid_for_claim"]),
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
    zero_rows = zero_theorem_rows()
    kernel_rows = explicit_kernel_rows()
    acquisition_rows = acquisition_priority_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_REGISTER.csv",
        "zero": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv",
        "kernels": OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2118_ACQUISITION_PRIORITIES.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2118_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2118_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2118_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2118_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2118_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["zero"], zero_rows)
    write_csv(paths["kernels"], kernel_rows)
    write_csv(paths["acquisition"], acquisition_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(zero_rows, kernel_rows, acquisition_rows, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, zero_rows, kernel_rows, acquisition_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, zero_rows, kernel_rows, acquisition_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
