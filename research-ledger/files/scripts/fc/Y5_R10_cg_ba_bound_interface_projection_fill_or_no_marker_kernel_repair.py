from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def row_by(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    return {}


def rows_where(path: Path, key: str, values: set[str]) -> list[dict[str, str]]:
    return [row for row in read_csv(path) if row.get(key) in values]


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "946_doc",
            "path": "946-Y5-R10-q-kernel-presymplectic-null-and-no-marker-certificate-or-cg-ba-bound-row.md",
            "role": "handoff: q-kernel certificate failed and c_g/b_A interface retained",
            "needle": "Local bound anchors exist",
        },
        {
            "source_id": "946_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_946_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V946_12_validation_rows_ready",
        },
        {
            "source_id": "946_interface",
            "path": "source-intake/mts_residuals/P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv",
            "role": "inherited nonclaim c_g/b_A bound interface",
            "needle": "CGB946_0_cg_R10",
        },
        {
            "source_id": "778_ppn_candidate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_778_PPN_COUPLING_RESPONSE_INPUT_CANDIDATE.csv",
            "role": "PPN response candidate showing missing MTS response matrix",
            "needle": "MISSING_CHANNEL_MAP",
        },
        {
            "source_id": "778_readout_candidate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_778_EM_CLOCK_ORBIT_READOUT_INPUT_CANDIDATE.csv",
            "role": "clock/photon/orbit readout candidate showing missing readout functionals",
            "needle": "MISSING_READOUT_FUNCTIONAL",
        },
        {
            "source_id": "778_descent_candidate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_778_COUPLING_DESCENT_INPUT_CANDIDATE.csv",
            "role": "coupling descent input candidate showing parent owner missing",
            "needle": "MISSING_PARENT_SIGNED_OWNER",
        },
        {
            "source_id": "786_bound_source_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_786_BG_BOUND_SOURCE_PACK.csv",
            "role": "bound source pack with missing R10/PPN/clock/orbital projections",
            "needle": "BGS786_0_ppn",
        },
        {
            "source_id": "753_external_ppn",
            "path": "source-intake/mts_residuals/P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv",
            "role": "external PPN literature anchors",
            "needle": "EXT753_0_Will_2014_LRR",
        },
        {
            "source_id": "646_clock_alpha_sensitivity",
            "path": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "role": "clock alpha sensitivity source rows",
            "needle": "CAS646_0_AlHg",
        },
        {
            "source_id": "766_clock_alpha_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_766_CLOCK_ALPHA_SOURCE_LOCK.csv",
            "role": "clock alpha source lock and Galileo exclusion",
            "needle": "R2R766_Galileo_repair",
        },
        {
            "source_id": "647_tau_clock_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
            "role": "clock product-map definition",
            "needle": "TAU647_0_time_drift",
        },
        {
            "source_id": "647_clock_product_bound",
            "path": "source-intake/mts_residuals/P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
            "role": "source-backed clock product bounds",
            "needle": "CPB647_0_AlHg",
        },
        {
            "source_id": "651_microscope_material_model",
            "path": "source-intake/mts_residuals/P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv",
            "role": "MICROSCOPE material composition model",
            "needle": "MM651_PtRh10_Pt",
        },
        {
            "source_id": "651_wep_alpha_stress",
            "path": "source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv",
            "role": "WEP alpha/source stress diagnostics",
            "needle": "WAS651_0_alpha_Coulomb",
        },
        {
            "source_id": "633_matter_frame_cases",
            "path": "source-intake/mts_residuals/P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv",
            "role": "matter-frame candidate classification after 631",
            "needle": "MFC633_7_631_variation",
        },
        {
            "source_id": "631_source_test_charge",
            "path": "source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv",
            "role": "source/test charge branch law",
            "needle": "Q631_0_universal_weyl_charge",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "no species/source charge contract",
            "needle": "S2_constant_sector_universality",
        },
        {
            "source_id": "763_no_marker_spurion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "no-marker/no-spurion theorem attempt",
            "needle": "NMS763_6_verdict",
        },
        {
            "source_id": "local_bounds",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "local empirical bound anchors",
            "needle": "MICROSCOPE_final_TiPt",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def projection_fill_attempt() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "PFA947_0_R10_projection",
            "arena": "R10 fifth force / inverse-square",
            "desired_projection": "alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g",
            "input_loaded": "946 interface and local alpha(lambda) anchor loaded",
            "filled_value_or_formula": "no numeric tau_R10, K_X(lambda), Qbar_XH, or c_g filled",
            "parent_input_needed": "parent c_g plus R10 source/test Yukawa projection",
            "current_status": "MISSING_TAU_R10_AND_PARENT_CG",
            "score_ready": "false",
            "valid_for_claim": "false",
            "source_paths": "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv; local_bound_claims.csv",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PFA947_1_PPN_projection",
            "arena": "PPN gamma/beta",
            "desired_projection": "gamma_minus_1 and beta_minus_1 as response operators on c_g/frame leak",
            "input_loaded": "Will/Cassini/beta anchors and 778/786 missing-response rows loaded",
            "filled_value_or_formula": "external PPN bound values loaded only",
            "parent_input_needed": "MTS response matrix M_gamma, M_beta with gauge/frame certificate",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
            "score_ready": "false",
            "valid_for_claim": "false",
            "source_paths": "P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv; P8_Y5_R10_778_PPN_COUPLING_RESPONSE_INPUT_CANDIDATE.csv; P8_Y5_R10_786_BG_BOUND_SOURCE_PACK.csv",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PFA947_2_WEP_material_projection",
            "arena": "MICROSCOPE/WEP composition",
            "desired_projection": "eta_AB ~ P_WEP(profile)(b_A-b_B) with material source charges",
            "input_loaded": "MICROSCOPE PtRh10/TA6V material model and alpha/source stress diagnostics loaded",
            "filled_value_or_formula": "candidate beta-source caps available only as diagnostic stress rows",
            "parent_input_needed": "source-normalized MTS b_A or theorem-zero species/source charge",
            "current_status": "PARTIAL_SOURCE_ROWS_LOADED_MISSING_MTS_SOURCE_CHARGE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "source_paths": "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv; P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PFA947_3_clock_product_projection",
            "arena": "atomic clocks / alpha_EM drift",
            "desired_projection": "d ln(alpha_EM)/dt = kappa_alpha * tau_clock_time",
            "input_loaded": "Al/Hg and Yb clock sensitivities plus product bounds loaded",
            "filled_value_or_formula": "|kappa_alpha * tau_clock_time| product bounds are source-backed",
            "parent_input_needed": "standalone kappa_alpha and tau_clock split, or constant-sector theorem-zero",
            "current_status": "PRODUCT_BOUND_READY_NONCLAIM_STANDALONE_COEFFICIENT_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "source_paths": "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv; P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PFA947_4_cg_parent_value",
            "arena": "parent common-frame/Weyl coefficient",
            "desired_projection": "c_g derived from parent action, quotient selection, or no-marker theorem",
            "input_loaded": "matter-frame candidates and source-test charge law loaded",
            "filled_value_or_formula": "no numeric c_g and no c_g=0 theorem signed",
            "parent_input_needed": "parent-selected quotient-only matter frame or sourced finite c_g",
            "current_status": "MISSING_PARENT_CG",
            "score_ready": "false",
            "valid_for_claim": "false",
            "source_paths": "P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv; P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PFA947_5_bA_parent_value",
            "arena": "species/source/constant coefficient",
            "desired_projection": "b_A=0 by constant-sector universality or finite sourced residual",
            "input_loaded": "no-species/source-charge contract loaded",
            "filled_value_or_formula": "no numeric b_A and no b_A=0 theorem signed",
            "parent_input_needed": "constant-sector universality, source-normalization species-blind theorem, or finite b_A source path",
            "current_status": "MISSING_PARENT_BA",
            "score_ready": "false",
            "valid_for_claim": "false",
            "source_paths": "P8_no_species_source_charge_CONTRACT.csv",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PFA947_6_no_marker_repair",
            "arena": "no-marker/kernel repair",
            "desired_projection": "all matter-visible marker/source/current coefficients theorem-zero",
            "input_loaded": "763 no-marker theorem attempt and no-species contract loaded",
            "filled_value_or_formula": "conditional theorem shape only",
            "parent_input_needed": "all no-marker, constant, source-weight, non-Hilbert-current, and boundary-silence clauses parent-signed",
            "current_status": "NO_MARKER_REPAIR_UNSIGNED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "source_paths": "P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv; P8_no_species_source_charge_CONTRACT.csv",
            "generated_utc": stamp(),
        },
    ]


def no_marker_repair_audit() -> list[dict[str, str]]:
    specs = [
        (
            "NRA947_0_one_observed_coframe",
            "one observed coframe selected before ordinary matter/readout",
            "S0_one_observed_coframe_parent_selected",
            "conditional_not_parent_derived",
            "parent-selected observed-frame theorem missing",
        ),
        (
            "NRA947_1_matter_factorization",
            "matter action factors only through observed quotient/coframe and universal constants",
            "S1_matter_factorization",
            "sufficient_axiom_not_parent_derived",
            "quotient matter functor theorem missing",
        ),
        (
            "NRA947_2_constant_superselection",
            "ordinary constants and charge normalizations are selector-trivial superselection labels",
            "S2_constant_sector_universality; NMS763_2_constant_superselection",
            "not_parent_signed",
            "alpha_EM, q_A, mass-ratio, and charge-normalization vertical derivatives remain legal",
        ),
        (
            "NRA947_3_source_weight_universality",
            "all ordinary matter sources one universal Hilbert/coframe current",
            "S4_source_normalization_species_blind; NMS763_3_universal_source_weight",
            "not_parent_signed",
            "species-weighted source currents remain legal",
        ),
        (
            "NRA947_4_no_material_marker_extension",
            "material markers and post-readout masks are absent or gauge/zero-projection",
            "S3_no_material_marker_extension; NMS763_1_no_material_marker",
            "partial_fixed_spurion_only",
            "co-moving material marker remains legal",
        ),
        (
            "NRA947_5_nonHilbert_boundary_silence",
            "spin/torsion/edge/topological currents vanish, are exact, or are retained explicitly",
            "S5_no_bulk_boundary_composition_charge; S6_no_connection_source_charge; NMS763_4_nonHilbert_current",
            "not_parent_signed",
            "boundary/local projection silence is not owned for every matter arena",
        ),
        (
            "NRA947_6_total_repair",
            "qbar_XT_vec=(b_g,b_theta,b_m,b_kappa,b_NH,b_EFT)=0",
            "all no-marker/no-species clauses close together",
            "repair_failed_current_corpus",
            "the required clauses are individually unsigned or policy-only",
        ),
    ]
    rows = []
    for audit_id, clause, required_theorem, current_status, blocker in specs:
        passes_repair = current_status == "parent_signed"
        rows.append(
            {
                "audit_id": audit_id,
                "clause": clause,
                "required_theorem": required_theorem,
                "source_evidence": "P8_no_species_source_charge_CONTRACT.csv; P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
                "current_status": current_status,
                "blocker": blocker,
                "closes_zero_if_signed": "true",
                "passes_repair": flag(passes_repair),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def bound_interface_update() -> list[dict[str, str]]:
    local_r10 = row_by(LOCAL_BOUNDS, "row_id", "R10_fifth_force")
    local_wep = row_by(LOCAL_BOUNDS, "row_id", "R1_WEP_source_charge")
    local_clock = row_by(LOCAL_BOUNDS, "row_id", "R2_clock_redshift")
    local_gamma = row_by(LOCAL_BOUNDS, "row_id", "R3_gamma")
    local_beta = row_by(LOCAL_BOUNDS, "row_id", "R4_beta")
    wep_rows = rows_where(
        OUT / "P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv",
        "stress_id",
        {"WAS651_0_alpha_Coulomb", "WAS651_1_surface_binding"},
    )
    clock_product_rows = rows_where(
        OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
        "bound_id",
        {"CPB647_0_AlHg", "CPB647_1_YbE3E2"},
    )
    alpha_coulomb = next((row for row in wep_rows if row.get("stress_id") == "WAS651_0_alpha_Coulomb"), {})
    surface_binding = next((row for row in wep_rows if row.get("stress_id") == "WAS651_1_surface_binding"), {})
    alhg = next((row for row in clock_product_rows if row.get("bound_id") == "CPB647_0_AlHg"), {})
    yb = next((row for row in clock_product_rows if row.get("bound_id") == "CPB647_1_YbE3E2"), {})
    return [
        {
            "interface_id": "BI947_0_cg_R10",
            "inherited_from": "CGB946_0_cg_R10",
            "symbol": "c_g",
            "arena": "R10 fifth-force",
            "empirical_bound": local_r10.get("upper_bound", "alpha(lambda)"),
            "bound_units": local_r10.get("units", "range-dependent"),
            "bound_source": local_r10.get("reference_path_or_url", "MISSING_BOUND_SOURCE"),
            "projection_or_product": "alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g",
            "loaded_source_rows": "946 interface; R10 symbolic alpha(lambda) anchor",
            "missing_mts_side": "K_X(lambda), Qbar_XH, tau_R10, c_g",
            "current_status": "MISSING_R10_PROJECTION",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "interface_id": "BI947_1_cg_PPN",
            "inherited_from": "CGB946_1_cg_PPN_gamma; CGB946_2_cg_PPN_beta",
            "symbol": "c_g",
            "arena": "PPN gamma/beta",
            "empirical_bound": f"gamma<={local_gamma.get('upper_bound', '2.3e-05')}; beta<={local_beta.get('upper_bound', '7.8e-05')}",
            "bound_units": "dimensionless",
            "bound_source": f"{local_gamma.get('reference_path_or_url', '')}; {local_beta.get('reference_path_or_url', '')}",
            "projection_or_product": "gamma_minus_1,beta_minus_1 ~ M_PPN(profile) tau_PPN c_g",
            "loaded_source_rows": "753 external PPN anchors; 778/786 missing response rows",
            "missing_mts_side": "M_gamma, M_beta, tau_PPN, gauge/frame certificate",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "interface_id": "BI947_2_bA_WEP_alpha",
            "inherited_from": "CGB946_3_bA_WEP",
            "symbol": "b_A-b_B",
            "arena": "MICROSCOPE/WEP composition",
            "empirical_bound": local_wep.get("upper_bound", "2.8e-15"),
            "bound_units": local_wep.get("units", "dimensionless"),
            "bound_source": local_wep.get("reference_path_or_url", "MISSING_BOUND_SOURCE"),
            "projection_or_product": "eta_AB ~ source_normalized_beta_AB; diagnostics require |beta_source|max <= min(candidate caps)",
            "loaded_source_rows": f"alpha_Coulomb_cap={alpha_coulomb.get('required_abs_beta_source_max', 'MISSING')}; surface_binding_cap={surface_binding.get('required_abs_beta_source_max', 'MISSING')}",
            "missing_mts_side": "source normalization and MTS b_A channel coefficient",
            "current_status": "PARTIAL_DIAGNOSTIC_CAPS_ONLY",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "interface_id": "BI947_3_clock_product_AlHg",
            "inherited_from": "CPB647_0_AlHg",
            "symbol": "kappa_alpha * tau_clock_time",
            "arena": "Al/Hg clock ratio",
            "empirical_bound": alhg.get("conservative_abs_product_bound_1sigma_yr_inv", "3.9e-17"),
            "bound_units": "yr^-1",
            "bound_source": alhg.get("source_measurements", "NIST/Frontiers source row"),
            "projection_or_product": alhg.get("product_bound_statement", "|kappa_alpha * tau_clock_time| <= 3.9e-17 yr^-1"),
            "loaded_source_rows": "CAS646_0_AlHg; TAU647_0_time_drift; CPB647_0_AlHg",
            "missing_mts_side": "standalone kappa_alpha/tau_clock split or constant-superselection theorem",
            "current_status": "PRODUCT_BOUND_SOURCE_BACKED_NONCLAIM",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "interface_id": "BI947_4_clock_product_Yb",
            "inherited_from": "CPB647_1_YbE3E2",
            "symbol": "kappa_alpha * tau_clock_time",
            "arena": "Yb E3/E2 clock ratio",
            "empirical_bound": yb.get("conservative_abs_product_bound_1sigma_yr_inv", "2.1e-18"),
            "bound_units": "yr^-1",
            "bound_source": yb.get("source_measurements", "PTB/Frontiers source row"),
            "projection_or_product": yb.get("product_bound_statement", "|kappa_alpha * tau_clock_time| <= 2.1e-18 yr^-1"),
            "loaded_source_rows": "CAS646_1_YbE3E2; TAU647_0_time_drift; CPB647_1_YbE3E2",
            "missing_mts_side": "standalone kappa_alpha/tau_clock split or constant-superselection theorem",
            "current_status": "PRODUCT_BOUND_SOURCE_BACKED_NONCLAIM",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "interface_id": "BI947_5_score_gate",
            "inherited_from": "947 aggregate",
            "symbol": "c_g;b_A;kappa_alpha*tau_clock",
            "arena": "all local bound interfaces",
            "empirical_bound": f"R10={local_r10.get('upper_bound', 'alpha(lambda)')}; WEP={local_wep.get('upper_bound', '2.8e-15')}; clock={local_clock.get('upper_bound', '2.48e-05')}",
            "bound_units": "mixed",
            "bound_source": "local_bound_claims.csv plus source-backed clock/WEP sidecar rows",
            "projection_or_product": "score only if parent coefficient and arena projection are both real",
            "loaded_source_rows": "WEP material model and clock product bounds loaded; R10/PPN anchors loaded",
            "missing_mts_side": "at least one MISSING_PARENT_INPUT or MISSING_ARENA_PROJECTION remains in every claim route",
            "current_status": "NO_ROW_SCORE_READY",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC947_0_projection_fill",
            "topic": "projection fill attempt",
            "result": "partial_source_fill_only",
            "reason": "WEP materials/stress diagnostics and clock product bounds are real source rows, but R10/PPN projections and parent coefficients remain missing",
            "next_action": "turn product-bound channels into explicit nonclaim runner or continue no-marker theorem repair",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC947_1_no_marker_repair",
            "topic": "no-marker/kernel repair",
            "result": "repair_unsigned",
            "reason": "constant-sector, source-weight, material-marker, non-Hilbert-current, and boundary/local silence clauses are not parent-signed",
            "next_action": "attempt constant-superselection/no-marker theorem before treating b_A=0 as derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC947_2_bound_interface",
            "topic": "c_g/b_A local bound interface",
            "result": "interface_improved_but_nonclaim",
            "reason": "source side is cleaner; theory side is still missing the coefficient/projection handshakes",
            "next_action": "948-Y5-R10-clock-WEP-product-bound-runner-or-constant-superselection-no-marker-theorem.md",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE947_0_R10_score",
            "claim": "R10 fifth-force score can be run as MTS evidence",
            "required_condition": "numeric c_g, K_X(lambda), Qbar_XH, tau_R10 and real alpha(lambda) bound curve",
            "current_evidence": "symbolic bound anchor only; parent/R10 projection missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE947_1_PPN_score",
            "claim": "PPN gamma/beta local-GR pass",
            "required_condition": "MTS response matrix with gauge/frame certificate and bounded residual vector",
            "current_evidence": "external PPN anchors loaded; MTS response matrix missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE947_2_WEP_score",
            "claim": "MICROSCOPE/WEP composition pass",
            "required_condition": "source-normalized b_A projection or theorem-zero species/source charge",
            "current_evidence": "material model and diagnostic caps loaded; MTS source charge missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE947_3_clock_score",
            "claim": "standalone clock/local constants pass",
            "required_condition": "standalone kappa_alpha and tau_clock split, or constant-sector theorem-zero",
            "current_evidence": "product bounds source-backed but split not owned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE947_4_zero_theorem",
            "claim": "c_g=b_A=0 by parent no-marker/kernel theorem",
            "required_condition": "all no-marker, constant, source-weight, boundary, and non-Hilbert clauses parent-signed",
            "current_evidence": "conditional theorem shapes only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "948-Y5-R10-clock-WEP-product-bound-runner-or-constant-superselection-no-marker-theorem.md",
            "objective": "build the first explicit nonclaim product-bound runner for clock/WEP channels, or derive the constant-superselection/no-marker theorem that sets the coefficients to zero",
            "include": "clock product rows, WEP material/stress diagnostics, constant-sector theorem attempt, species/source charge contract, source-normalization audit",
            "exclude": "R10/local-GR pass claim, PPN pass claim, standalone coefficient claims without parent input, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    interface_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if passes else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_946_VALIDATION.csv"))
    wep_loaded = any("WEP_material" in row["attempt_id"] and row["current_status"].startswith("PARTIAL") for row in projection_rows)
    clock_loaded = any(row["interface_id"] == "BI947_3_clock_product_AlHg" for row in interface_rows) and any(
        row["interface_id"] == "BI947_4_clock_product_Yb" for row in interface_rows
    )
    r10_blocked = any(row["interface_id"] == "BI947_0_cg_R10" and row["score_ready"] == "false" for row in interface_rows)
    ppn_blocked = any(row["interface_id"] == "BI947_1_cg_PPN" and row["score_ready"] == "false" for row in interface_rows)
    repair_unsigned = any(row["audit_id"] == "NRA947_6_total_repair" and row["passes_repair"] == "false" for row in repair_rows)
    all_score_false = all(row.get("score_ready") == "false" for row in interface_rows + projection_rows)
    claim_gates_false = all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    decision_nonclaim = all(row.get("claim_allowed") == "false" for row in decision_rows)
    target_selected = target_rows and target_rows[0]["next_target"].startswith("948-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, projection_rows, repair_rows, interface_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V947_0_sources_exist_and_needles", sources_ok, "all 947 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V947_1_prior_946_clean", prior_clean, "P8_Y5_BRR545_946_VALIDATION.csv clean")
    add("V947_2_WEP_partial_rows_loaded", wep_loaded, "MICROSCOPE material/stress diagnostics loaded as partial nonclaim rows")
    add("V947_3_clock_product_rows_loaded", clock_loaded, "AlHg and Yb product-bound rows loaded")
    add("V947_4_R10_projection_blocked", r10_blocked, "R10 remains blocked by missing parent coefficient/projection")
    add("V947_5_PPN_projection_blocked", ppn_blocked, "PPN remains blocked by missing MTS response matrix")
    add("V947_6_no_marker_repair_unsigned", repair_unsigned, "no-marker repair total row fails")
    add("V947_7_no_score_ready_rows", all_score_false, "all projection/interface rows have score_ready=false")
    add("V947_8_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V947_9_decisions_nonclaim", decision_nonclaim, "decision ledger remains nonclaim")
    add("V947_10_next_target_selected", target_selected, "948 clock/WEP product runner or constant-superselection theorem selected")
    add("V947_11_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V947_12_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V947_13_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    interface_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 947 Y5 R10: c_g/b_A Bound Interface Projection Fill Or No-Marker Kernel Repair

Status: `Y5_R10_947_projection_fill_partial_no_marker_repair_unsigned_nonclaim`

Claim ceiling: `source_side_improved_only_no_R10_no_PPN_no_WEP_no_clock_no_local_GR_claim`

## Result

This checkpoint tried the cleanest next move after 946: either fill real arena projections for the retained `c_g/b_A` bound interface, or repair the no-marker/kernel route so the offending coefficients become theorem-zero.

The result is useful but still nonclaim. The WEP side now has material/stress diagnostic inputs, and the clock side has source-backed product bounds. R10 and PPN still lack the MTS arena projections, and the parent coefficients `c_g`, `b_A`, and standalone `kappa_alpha/tau_clock` are not derived. The no-marker repair also remains unsigned.

So the honest state is:

```text
source side cleaner,
theory-side coefficient/projection handshake still missing,
no local-GR/R10/WEP/clock/PPN claim promoted.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Projection Fill Attempt

{md_table(projection_rows, ["attempt_id", "arena", "desired_projection", "filled_value_or_formula", "current_status", "score_ready"])}

## No-Marker Repair Audit

{md_table(repair_rows, ["audit_id", "clause", "current_status", "blocker", "passes_repair"])}

## Bound Interface Update

{md_table(interface_rows, ["interface_id", "symbol", "arena", "empirical_bound", "projection_or_product", "missing_mts_side", "current_status", "score_ready"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    projection_rows = projection_fill_attempt()
    repair_rows = no_marker_repair_audit()
    interface_rows = bound_interface_update()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        projection_rows,
        repair_rows,
        interface_rows,
        decision_rows,
        claim_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_947_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv",
        projection_rows,
        [
            "attempt_id",
            "arena",
            "desired_projection",
            "input_loaded",
            "filled_value_or_formula",
            "parent_input_needed",
            "current_status",
            "score_ready",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_947_NO_MARKER_REPAIR_AUDIT.csv",
        repair_rows,
        [
            "audit_id",
            "clause",
            "required_theorem",
            "source_evidence",
            "current_status",
            "blocker",
            "closes_zero_if_signed",
            "passes_repair",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv",
        interface_rows,
        [
            "interface_id",
            "inherited_from",
            "symbol",
            "arena",
            "empirical_bound",
            "bound_units",
            "bound_source",
            "projection_or_product",
            "loaded_source_rows",
            "missing_mts_side",
            "current_status",
            "score_ready",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_947_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_947_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_947_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_947_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        projection_rows,
        repair_rows,
        interface_rows,
        decision_rows,
        claim_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
