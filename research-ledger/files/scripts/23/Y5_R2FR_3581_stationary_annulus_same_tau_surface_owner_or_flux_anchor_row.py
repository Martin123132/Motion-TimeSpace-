from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3581-Y5-R2FR-stationary-annulus-same-tau-surface-owner-or-flux-anchor-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_STATIONARY_ANNULUS_PACKAGE_3581"
CHECKPOINT_ID = "3581"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3580": RESIDUALS / "P8_Y5_R2FR_3580_NEXT_TARGET.csv",
        "transport_3580": RESIDUALS / "P8_Y5_R2FR_3580_STATIONARY_COLLAR_TRANSPORT_LAW.csv",
        "clauses_3580": RESIDUALS / "P8_Y5_R2FR_3580_CERTIFICATE_CLAUSE_AUDIT.csv",
        "flux_rows_3580": RESIDUALS / "P8_Y5_R2FR_3580_FLUX_BOUND_ROWS.csv",
        "status_3580": RESIDUALS / "P8_Y5_R2FR_3580_STATUS.csv",
        "adoption_3576": RESIDUALS / "P8_Y5_R2FR_3576_CANDIDATE_PARENT_BRANCH_ADOPTION_PACKET.csv",
        "reference_3577": RESIDUALS / "P8_Y5_R2FR_3577_HREF_REFERENCE_LOCK.csv",
        "htau_ref_3577": RESIDUALS / "P8_Y5_R2FR_3577_HTAU_QBASIC_REFERENCE_THEOREM.csv",
        "status_3577": RESIDUALS / "P8_Y5_R2FR_3577_STATUS.csv",
        "source_support_3560_doc": ROOT / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md",
        "source_support_3560_status": RESIDUALS / "P8_Y5_source_support_qbasic_worldtube_status.csv",
        "stationary_3538": RESIDUALS / "P8_local_GR_observed_flow_stationary_branch_status.csv",
        "tau_owner_2067": RESIDUALS / "P8_Y5_PARENT_QLOC_2067_STATIONARY_TAU_OWNER_ATTEMPT.csv",
        "surface_owner_2066": RESIDUALS / "P8_Y5_PARENT_QLOC_2066_STATIONARY_SURFACE_OWNER_ATTEMPT.csv",
        "surface_requirements_2065": RESIDUALS / "P8_Y5_PARENT_QLOC_2065_ACTUAL_SURFACE_REQUIREMENTS.csv",
        "worldtube_support_2388": RESIDUALS / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv",
        "annulus_audit_1730": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_ANNULUS_SUPPORT_AUDIT.csv",
        "aext_support_1731": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_AEXT_SUPPORT_THEOREM_ATTEMPT.csv",
        "poynting_3234": ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
        "poynting_vector_3502": RESIDUALS / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "gauge_2171": RESIDUALS / "P8_Y5_PARENT_QLOC_2171_NOETHER_GAUGE_CONDITION_LEDGER.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3581 stationary annulus same-tau/surface/anchor activation package input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def package_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "SAP3581_0_package_object",
            "single stationary annulus package",
            "P_ann := (tau_obs, Sigma_tau, W_source, S_in, S_out, H_ref, EM_gauge_class, Phi_anchor)",
            "The no-radiation theorem is not a property of one row. It is a same-branch package: tau, source support, surfaces, reference, gauge and anchor must be fixed together before readout.",
            "PACKAGE_DEFINED",
            "transport_3580",
        ),
        (
            "SAP3581_1_activation_implication",
            "Poynting zero switch",
            "Z_Poynting=true iff Z_tau & Z_surface & Z_worldtube & Z_anchor & Z_gauge & Z_no_seams",
            "If all clauses close on the same branch, 3580 transport plus Phi_anchor=0 gives Phi_EM_rad=0, hence the 3579 public EM H_tau component can be zeroed.",
            "EXACT_BOOLEAN_SWITCH_WRITTEN",
            "flux_rows_3580",
        ),
        (
            "SAP3581_2_internal_credit",
            "earned internal credits",
            "PC3400 fixes branch variables before readout; H_ref source derivative is zero; Pi_M^H and R_eq/B_zero wrong-object channel are internally narrowed",
            "These credits reduce the package but do not prove stationarity, actual surface ownership, zero anchor, or gauge/corner silence.",
            "INTERNAL_CREDITS_APPLIED_NONCLAIM",
            "adoption_3576",
        ),
        (
            "SAP3581_3_fallback",
            "finite row fallback",
            "If any Z_i=false, use R_ann_abs := Phi_anchor_abs + Delta_tau_surface_abs + Delta_surface_owner_abs + J_cross_EM_abs + C_EM_surface_gauge_abs + B_corner_flux_abs",
            "This is the no-cancellation replacement for a failed same-annulus zero proof.",
            "BOUND_VECTOR_CONSTRUCTED",
            "flux_rows_3580",
        ),
        (
            "SAP3581_4_scope_guard",
            "scope guard",
            "Z_Poynting does not imply H_tau curl zero, EM coupling owner, positive M_H_ref, Newtonian limit, PPN pass, or local GR",
            "The package only controls the public EM/Poynting piece of the H_tau curl vector.",
            "NO_OVERCLAIM_GUARD",
            "status_3580",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "package_id": package_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for package_id, claim_piece, mathematical_form, derivation, status, source_key in specs
    ]


def activation_clause_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "ACT3581_0_branch_fixed_before_readout",
            "Z_branch",
            "g_obs/e_obs, q(Phi), tau, H_tau, H_ref, Pi_M^H, kappa_MTS and source support are fixed before scoring",
            "PASS_INTERNAL_CANDIDATE",
            "3576 PC3400 adoption gives this inside the private branch; no public claim.",
            "adoption_3576",
        ),
        (
            "ACT3581_1_same_public_current",
            "Z_public_current",
            "public matter+EM Hilbert stress/current uses the same observed Hodge/coframe",
            "PASS_CONDITIONAL_PUBLIC_EM",
            "3463/3579 give standard public EM/matter stress accounting; full EM owner still separate.",
            "clauses_3580",
        ),
        (
            "ACT3581_2_Href_fixed",
            "Z_Href",
            "H_ref is source/readout blind on the fixed branch and uses the same linked boundary class",
            "PASS_INTERNAL_CANDIDATE_IF_SURFACE_CLASS_FIXED",
            "3577 signs H_ref derivative silence, but surface class ownership still feeds Z_surface.",
            "reference_3577",
        ),
        (
            "ACT3581_3_tau_Killing",
            "Z_tau",
            "tau_obs is parent-selected and Killing on the local exterior collar",
            "MISSING_STATIONARY_TAU_OWNER",
            "2067 still blocks parent tau/Killing ownership and same-tau normalization.",
            "tau_owner_2067",
        ),
        (
            "ACT3581_4_same_tau_roles",
            "Z_same_tau",
            "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs",
            "MISSING_SAME_TAU_NORMALIZATION",
            "Needed so a cap/flux zero in one generator is not scored in another.",
            "tau_owner_2067",
        ),
        (
            "ACT3581_5_actual_surfaces",
            "Z_surface",
            "S_in/S_out/Sigma_tau are the same action, source, boundary-reference and readout surfaces",
            "MISSING_ACTUAL_SURFACE_OWNER",
            "2065/2066 define the annulus but do not parent-sign it as the actual arena surface.",
            "surface_owner_2066",
        ),
        (
            "ACT3581_6_worldtube_no_crossing",
            "Z_worldtube",
            "W_source is compact/regular/q-basic and no charge/current crosses the collar",
            "MISSING_WORLDTUBE_SUPPORT_NO_CROSSING",
            "3560 gives a real support-descent route, but rho_H q-basicness and regular support remain unsigned.",
            "source_support_3560_doc",
        ),
        (
            "ACT3581_7_zero_flux_anchor",
            "Z_anchor",
            "one owned anchor satisfies Phi_anchor=0 on the same branch",
            "MISSING_ZERO_FLUX_ANCHOR",
            "3580 proves transport, not zero; a no-incoming/no-outgoing/asymptotic/interior anchor must be owned or bounded.",
            "poynting_vector_3502",
        ),
        (
            "ACT3581_8_EM_gauge_corner",
            "Z_gauge",
            "EM gauge representative is fixed on closed compatible surfaces and corner terms are exact/proper or absent",
            "MISSING_EM_GAUGE_CORNER_CERTIFICATE",
            "3234 gives the exact routes; current branch has no signed gauge/corner certificate.",
            "poynting_3234",
        ),
        (
            "ACT3581_9_no_regulator_seams",
            "Z_no_seams",
            "no cutoff/excision/regulator/matched-patch seams carry active flux",
            "MISSING_REGULATOR_LEDGER",
            "2065 explicitly keeps seam/corner ledger missing.",
            "surface_requirements_2065",
        ),
        (
            "ACT3581_10_activation",
            "Z_Poynting",
            "Z_tau & Z_same_tau & Z_surface & Z_worldtube & Z_anchor & Z_gauge & Z_no_seams",
            "FAIL_CURRENT_CLAIM_SWITCH_READY",
            "The package is exact, but the live branch cannot set I_matter_EM_flux=0 until missing clauses close.",
            "status_3580",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "symbol": symbol,
            "required_statement": required_statement,
            "status": status,
            "reason": reason,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, symbol, required_statement, status, reason, source_key in specs
    ]


def finite_row_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "FAR3581_0_Phi_anchor_abs",
            "Phi_anchor_abs",
            "min(|Phi_in|, |Phi_out|, |Phi_infty|, |Phi_prescribed_boundary|)",
            "power or energy/time",
            "MISSING_ZERO_ANCHOR_OR_NUMERIC_FLUX",
            "owned no-incoming/no-outgoing/asymptotic/interior anchor, or a sourced finite EM flux value",
            "poynting_vector_3502",
        ),
        (
            "FAR3581_1_Delta_tau_surface_abs",
            "Delta_tau_surface_abs",
            "|int_A T_EM^{mu nu}nabla_(mu tau_nu)dV| plus same-tau mismatch cap",
            "energy/time or Hamiltonian curl numerator units",
            "MISSING_TAU_KILLING_AND_SAME_TAU_OWNER",
            "stationary tau theorem or finite epsilon_tau/symgrad_tau row with a same-frame denominator",
            "tau_owner_2067",
        ),
        (
            "FAR3581_2_Delta_surface_owner_abs",
            "Delta_surface_owner_abs",
            "absolute mismatch between variational boundary, source support boundary, readout surface, and reference surface",
            "Hamiltonian curl numerator units",
            "MISSING_ACTUAL_SURFACE_EQUIVALENCE",
            "single surface id plus action/source/readout/reference equivalence, or finite mismatch/corner row",
            "surface_requirements_2065",
        ),
        (
            "FAR3581_3_J_cross_EM_abs",
            "J_cross_EM_abs",
            "int_boundary(A_tau)|J^mu n_mu|dSigma with EM work conversion stated",
            "charge/time plus conversion, or energy/time after J.E weighting",
            "MISSING_WORLDTUBE_NO_CROSSING",
            "compact source/no-crossing certificate or finite crossing flux value",
            "worldtube_support_2388",
        ),
        (
            "FAR3581_4_C_EM_surface_gauge_abs",
            "C_EM_surface_gauge_abs",
            "absolute EM gauge/corner term in C_tau^EM on S_in union S_out",
            "Hamiltonian curl numerator units",
            "MISSING_GAUGE_CORNER_CERTIFICATE",
            "constant gauge on closed compatible surfaces, exact/proper corner theorem, or finite corner value",
            "poynting_3234",
        ),
        (
            "FAR3581_5_B_corner_flux_abs",
            "B_corner_flux_abs",
            "sum active cutoff/excision/regulator/matched-patch seam fluxes",
            "Hamiltonian curl numerator units",
            "MISSING_REGULATOR_SEAM_LEDGER",
            "seam absence theorem or sourced finite seam flux values",
            "surface_owner_2066",
        ),
        (
            "FAR3581_6_R_ann_abs",
            "R_ann_abs",
            "Phi_anchor_abs + Delta_tau_surface_abs + Delta_surface_owner_abs + J_cross_EM_abs + C_EM_surface_gauge_abs + B_corner_flux_abs",
            "Hamiltonian curl numerator units or normalized over M_H_ref c^2 with stated window",
            "NO_CANCELLATION_BOUND_VECTOR_READY_VALUES_MISSING",
            "all preceding rows zero or finite sourced values; no cancellation credit",
            "flux_rows_3580",
        ),
        (
            "FAR3581_7_I_matter_EM_flux",
            "I_matter_EM_flux",
            "I_matter_EM_flux <= A_F sup_BF R_ann_abs",
            "Hamiltonian curl numerator units",
            "HTAU_FEED_READY_NONCLAIM",
            "public EM contribution to 3578/3579 H_tau curl vector",
            "transport_3580",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "required_input": required_input,
            "source_path": str(source_paths[source_key]),
            "numeric_value": "MISSING_NUMERIC_OR_PARENT_ZERO",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, units, status, required_input, source_key in specs
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3581_0_sources", "source audit", "PASS", "all required source paths and anchors exist"),
        ("GATE3581_1_package_switch", "single annulus activation switch", "PASS_NONCLAIM", "same-branch boolean package is written"),
        ("GATE3581_2_internal_credits", "branch/Href/PiM internal credits", "PASS_INTERNAL_CANDIDATE", "3576/3577 credits applied without public promotion"),
        ("GATE3581_3_tau_surface", "tau and surface owner", "FAIL_CURRENT_CLAIM", "stationary tau, same tau, and actual surface ownership remain unsigned"),
        ("GATE3581_4_anchor", "zero flux anchor", "FAIL_CURRENT_CLAIM", "Phi_anchor=0 is not sourced or parent-signed"),
        ("GATE3581_5_worldtube_gauge", "worldtube no-crossing and EM gauge/corner", "FAIL_CURRENT_CLAIM", "support/no-crossing and gauge/corner certificates remain unsigned"),
        ("GATE3581_6_public_EM_zero", "I_matter_EM_flux=0", "FAIL_CURRENT_CLAIM", "activation switch false until missing clauses close"),
        ("GATE3581_7_local_GR", "local GR/Newton/PPN", "FAIL_CURRENT_CLAIM", "only public EM H_tau component was sharpened"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["status_3580"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3581_0_single_switch",
            "collapse tau/surface/worldtube/anchor/gauge into one activation package",
            "The Poynting branch was at risk of being re-audited clause-by-clause forever; the exact boolean switch now says when the zero fires.",
            "future work must close or fill named rows, not restate the whole problem",
            "ADOPTED",
            "flux_rows_3580",
        ),
        (
            "DEC3581_1_internal_credit_but_no_claim",
            "use 3576/3577 internal credits only inside the private branch",
            "The fixed-before-readout and H_ref/PiM credits are real narrowing, but they do not prove stationarity or zero anchor.",
            "keeps progress without smuggling closure",
            "ADOPTED_GUARD",
            "adoption_3576",
        ),
        (
            "DEC3581_2_next_target",
            "attack Phi_anchor first",
            "After 3581, the cleanest remaining Poynting-specific blocker is the zero flux anchor; tau/surface/worldtube also matter, but the anchor is the unique new thing 3580 exposed.",
            "3582 should derive a no-incoming/no-outgoing/asymptotic/interior zero anchor or fill the first finite Phi_anchor row.",
            "NEXT_TARGET_SELECTED",
            "poynting_vector_3502",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "STATIONARY_ANNULUS_PACKAGE_SWITCH_READY_ZERO_ANCHOR_AND_OWNER_ROWS_REQUIRED",
            "strongest_result": "The 3580 no-radiation route is now a single activation package P_ann. Internal branch/H_ref/PiM credits are applied, and I_matter_EM_flux=0 is reduced to one same-branch switch requiring stationary tau, same tau, actual S_in/S_out surfaces, compact no-crossing worldtube, zero Phi_anchor, fixed EM gauge/corners, and no regulator seams.",
            "still_missing": "stationary tau owner, same-tau normalization, actual surface equivalence, compact regular support/no-crossing, zero flux anchor, EM gauge/corner certificate, regulator seam ledger, and finite values if any theorem-zero fails",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3581_0",
            "target_doc": "3582-Y5-R2FR-Phi-anchor-zero-boundary-condition-or-first-finite-flux-row.md",
            "target_script": "scripts/Y5_R2FR_3582_Phi_anchor_zero_boundary_condition_or_first_finite_flux_row.py",
            "objective": "derive an owned zero flux anchor for the stationary public EM/Poynting annulus, or fill the first finite Phi_anchor row with units, boundary condition, and source path",
            "success_gate": "Phi_anchor=0 is parent-signed for one named anchor on the same P_ann branch, or FAR3581_0 receives a source-backed finite value and remains nonclaim",
            "reason": "3581 makes the activation switch exact; Phi_anchor is now the cleanest Poynting-specific missing proof input",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "stationary_annulus_public_EM_switch",
            "status": "BOOLEAN_ACTIVATION_READY_NOT_CLOSED",
            "activation_rule": "Z_Poynting=Z_tau & Z_same_tau & Z_surface & Z_worldtube & Z_anchor & Z_gauge & Z_no_seams",
            "fallback_bound": "R_ann_abs=Phi_anchor_abs+Delta_tau_surface_abs+Delta_surface_owner_abs+J_cross_EM_abs+C_EM_surface_gauge_abs+B_corner_flux_abs",
            "next_action": "derive or source Phi_anchor",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    package: list[dict[str, object]],
    clauses: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3581_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3581 source paths exist"))
    needles = {
        "handoff_3580": "NEXT3580_0",
        "transport_3580": "TRL3580_4_anchor_zero",
        "clauses_3580": "LCA3580_2_no_radiation",
        "flux_rows_3580": "LFB3580_1_flux_anchor",
        "status_3580": "POYNTING_TRANSPORT_THEOREM",
        "adoption_3576": "ADOPT3576_0_branch",
        "reference_3577": "REF3577_0_fixed_reference_rule",
        "htau_ref_3577": "HTQ3577_4_live_blocker",
        "status_3577": "HREF_REFERENCE_DERIVATIVE_SILENCE",
        "source_support_3560_doc": "SWT3560_4_failure_decomposition",
        "source_support_3560_status": "SOURCE_SUPPORT_QBASIC_LEMMA",
        "stationary_3538": "STAT3538_1_stationary",
        "tau_owner_2067": "STO2067_1_Killing_identity",
        "surface_owner_2066": "SSO2066_1_domain_Dstat",
        "surface_requirements_2065": "ASR2065_3_surface_equivalence",
        "worldtube_support_2388": "WSC2388_5_no_crossing",
        "annulus_audit_1730": "ASA1730_2_source_free_annulus",
        "aext_support_1731": "AST1731_0_geometry_antecedent",
        "poynting_3234": "PF3234_0_functional",
        "poynting_vector_3502": "EMF3502_1_radiative_poynting_flux",
        "gauge_2171": "VG2171_4_boundary_silence",
    }
    validations.append(("VAL3581_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3581 anchors found"))
    validations.append(("VAL3581_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3581 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3581_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3581_4_switch_present", any(row["package_id"] == "SAP3581_1_activation_implication" for row in package), "boolean activation switch present"))
    validations.append(("VAL3581_5_internal_credit_present", any(row["package_id"] == "SAP3581_2_internal_credit" for row in package), "internal credit row present"))
    required_clause_symbols = {"Z_tau", "Z_same_tau", "Z_surface", "Z_worldtube", "Z_anchor", "Z_gauge", "Z_no_seams", "Z_Poynting"}
    validations.append(("VAL3581_6_activation_clauses_present", required_clause_symbols.issubset({str(row["symbol"]) for row in clauses}), "all activation clauses present"))
    required_finite_symbols = {"Phi_anchor_abs", "Delta_tau_surface_abs", "Delta_surface_owner_abs", "J_cross_EM_abs", "C_EM_surface_gauge_abs", "B_corner_flux_abs", "R_ann_abs"}
    validations.append(("VAL3581_7_finite_rows_present", required_finite_symbols.issubset({str(row["symbol"]) for row in finite_rows}), "finite fallback rows present"))
    validations.append(("VAL3581_8_anchor_not_claimed", any(row["symbol"] == "Z_anchor" and "MISSING" in str(row["status"]) for row in clauses), "zero flux anchor not overclaimed"))
    validations.append(("VAL3581_9_public_EM_zero_not_claimed", any(row["gate_id"] == "GATE3581_6_public_EM_zero" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "I_matter_EM_flux zero remains unclaimed"))
    validations.append(("VAL3581_10_next_target_selected", any(row["decision_id"] == "DEC3581_2_next_target" for row in decisions), "Phi_anchor next target selected"))
    validations.append(("VAL3581_11_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in package + clauses + finite_rows + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in package + clauses + finite_rows + gates + decisions)
    validations.append(("VAL3581_12_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3581*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3581_13_formalization_workbench_untouched", not formalization_touched, "no 3581 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    package: list[dict[str, object]],
    clauses: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3581 - Stationary annulus same-tau surface owner or flux anchor row",
        "",
        "## Verdict",
        "3581 turns the 3580 Poynting transport result into one exact activation package.  The package is `P_ann=(tau_obs, Sigma_tau, W_source, S_in, S_out, H_ref, EM_gauge_class, Phi_anchor)`, and the zero switch is `Z_Poynting=Z_tau & Z_same_tau & Z_surface & Z_worldtube & Z_anchor & Z_gauge & Z_no_seams`.",
        "",
        "Current result: the switch is written but not closed.  The useful internal credits are kept: fixed-before-readout private branch, `H_ref` source-blindness, and `Pi_M^H/R_eq/B_zero` narrowing.  The live blockers are now explicit finite rows, led by `Phi_anchor_abs`.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Package theorem"])
    for row in package:
        lines.append(f"- `{row['package_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Activation clauses"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}` `{row['symbol']}`: {row['status']} ({row['reason']})")
    lines.extend(["", "## Finite rows"])
    for row in finite_rows:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    package = package_theorem_rows(source_paths)
    clauses = activation_clause_rows(source_paths)
    finite_rows = finite_row_rows(source_paths)
    gates = gate_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3581_SOURCE_REGISTER.csv",
        "package_theorem": RESIDUALS / "P8_Y5_R2FR_3581_STATIONARY_ANNULUS_PACKAGE_THEOREM.csv",
        "activation_clauses": RESIDUALS / "P8_Y5_R2FR_3581_ACTIVATION_CLAUSES.csv",
        "finite_rows": RESIDUALS / "P8_Y5_R2FR_3581_FINITE_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3581_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3581_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3581_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3581_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_stationary_annulus_public_EM_switch_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3581_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["package_theorem"], package)
    write_csv(outputs["activation_clauses"], clauses)
    write_csv(outputs["finite_rows"], finite_rows)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, package, clauses, finite_rows, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, package, clauses, finite_rows, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3581 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
