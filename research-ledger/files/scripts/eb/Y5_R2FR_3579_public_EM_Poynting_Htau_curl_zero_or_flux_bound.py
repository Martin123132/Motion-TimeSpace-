from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3579-Y5-R2FR-public-EM-Poynting-Htau-curl-zero-or-flux-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PUBLIC_EM_POYNTING_HTAU_CURL_3579"
CHECKPOINT_ID = "3579"


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
        "handoff_3578": RESIDUALS / "P8_Y5_R2FR_3578_NEXT_TARGET.csv",
        "curl_components_3578": RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_COMPONENT_VECTOR.csv",
        "curl_identities_3578": RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_IDENTITIES.csv",
        "theta_qtau_3578": RESIDUALS / "P8_Y5_R2FR_3578_THETA_QTAU_COMPONENT_UPDATE.csv",
        "status_3578": RESIDUALS / "P8_Y5_R2FR_3578_STATUS.csv",
        "maxwell_poynting_3463": RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
        "em_owner_3465": RESIDUALS / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
        "em_alpha_charge_3464": RESIDUALS / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
        "em_poynting_vector_3502": RESIDUALS / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "em_hodge_bound_3503": RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "em_current_ward_3508": RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
        "em_no_source_only_3509": RESIDUALS / "P8_EM_no_source_only_matter_functor_residual.csv",
        "em_visible_status_3525": RESIDUALS / "P8_EM_visible_EM_first_owner_branch_status.csv",
        "em_unique_status_3528": RESIDUALS / "P8_EM_unique_F2_or_calibrated_alpha_status.csv",
        "em_same_owner_3547": RESIDUALS / "P8_Y5_parent_EM_same_owner_zero_or_Ke_alpha_source_leg_status.csv",
        "source_current_532": RESIDUALS / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "hilbert_worldtube_536": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
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
            "role": "3579 public EM/Poynting H_tau curl derivation or flux-bound input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "PEM3579_0_public_Maxwell_stress",
            "standard observed-frame Maxwell stress",
            "S_EM=-1/(4 mu0) int sqrt(-g_obs) F_{mn}F^{mn}+int A_mu J^mu",
            "Varying the observed metric/coframe gives T_EM^{mu nu}; in a local inertial frame T_EM^{0i}=S_Poynting^i/c^2.",
            "EXACT_CONDITIONAL_ON_OBSERVED_HODGE",
            "maxwell_poynting_3463",
        ),
        (
            "PEM3579_1_matter_EM_exchange",
            "internal Lorentz exchange cancels in total public stress",
            "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "Matter-only and EM-only currents need not be conserved separately, but the total matter+EM Hilbert current is conserved when both come from the same public action/current.",
            "EXACT_CONDITIONAL_TOTAL_STRESS_ZERO",
            "maxwell_poynting_3463",
        ),
        (
            "PEM3579_2_poynting_flux_identity",
            "Poynting theorem as the public boundary-flux diagnostic",
            "d_t U_EM(V)+int_boundary(V) S_Poynting dot n dA=-int_V J dot E dV",
            "For stationary bound public EM fields with no current crossing the linking surface and no radiation/background leakage, the net EM boundary flux is zero.",
            "DERIVED_CONDITIONAL_NO_FLUX_IDENTITY",
            "em_poynting_vector_3502",
        ),
        (
            "PEM3579_3_covariant_phase_space_zero",
            "public matter+EM contribution to d_F alpha_tau",
            "I_matter_EM_flux=abs(int_BF[-int_S i_tau omega_{matter+EM}+C_tau^{matter+EM}])",
            "If tau is the same observed stationary generator, L_tau fields=0 up to fixed EM gauge, the linking surface is fixed, and total matter+EM source current is the varied Hilbert current, then omega(delta Phi,L_tau Phi)=0 and the public EM/matter curl component vanishes.",
            "CONDITIONAL_THEOREM_ZERO_WRITTEN",
            "curl_components_3578",
        ),
        (
            "PEM3579_4_not_alpha_owner",
            "flux zero is not unique-F2 or alpha derivation",
            "I_matter_EM_flux=0 does not imply Delta_Hodge_EM=0, w_EM=0, C_XF2=0, or b_alpha=0.",
            "The local exterior no-flux lemma only removes a public boundary/current-exchange curl term; EM normalization, hidden F2, charge/current owner, and readout/radiative closure remain separate coupling gates.",
            "SCOPE_GUARD_EXPLICIT",
            "em_owner_3465",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, mathematical_form, derivation, status, source_key in specs
    ]


def no_flux_condition_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "NFC3579_0_same_observed_Hodge",
            "same observed coframe/Hodge defines Maxwell stress and local geometry",
            "PASS_CONDITIONAL_STANDARD_FORM",
            "Needed so the Poynting vector is the energy-current of the same public geometry that H_tau sees.",
            "maxwell_poynting_3463",
        ),
        (
            "NFC3579_1_same_current_owner",
            "matter current and Maxwell current are varied from the same public action",
            "PASS_CONDITIONAL_NOT_PARENT_GLOBAL",
            "Needed for Lorentz-force exchange to cancel in total matter+EM Hilbert stress.",
            "maxwell_poynting_3463",
        ),
        (
            "NFC3579_2_stationary_generator",
            "tau is the same observed stationary generator on the collar",
            "REQUIRED_NOT_PARENT_SIGNED",
            "Needed for L_tau Phi=0 and omega(delta Phi,L_tau Phi)=0.",
            "curl_identities_3578",
        ),
        (
            "NFC3579_3_no_radiative_boundary_flux",
            "no net Poynting/radiation/background leakage through the linking boundary",
            "REQUIRED_NOT_PARENT_SIGNED",
            "Needed to set int_boundary S_Poynting dot n dA=0 rather than merely bound it.",
            "em_poynting_vector_3502",
        ),
        (
            "NFC3579_4_no_current_crossing_surface",
            "charged matter worldtube is inside the linking surface and no public current crosses the boundary",
            "REQUIRED_NOT_PARENT_SIGNED",
            "Needed so public EM/matter exchange is internal to the source worldtube.",
            "hilbert_worldtube_536",
        ),
        (
            "NFC3579_5_fixed_EM_gauge_surface",
            "EM gauge representative is fixed on the linking surface or contributes only an exact charge improvement",
            "REQUIRED_NOT_PARENT_SIGNED",
            "Needed to prevent a gauge/corner term from masquerading as Poynting flux.",
            "em_hodge_bound_3503",
        ),
        (
            "NFC3579_6_local_exterior_clause",
            "local exterior is compact, source-free, stationary, and public-sector only for this component",
            "CONDITIONAL_ZERO_IF_ALL_ABOVE",
            "This clause zeros only I_matter_EM_flux, not the full H_tau curl vector.",
            "curl_components_3578",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "condition_id": condition_id,
            "condition": condition,
            "status": status,
            "reason": reason,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for condition_id, condition, status, reason, source_key in specs
    ]


def flux_bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "PFB3579_0_I_matter_EM_flux",
            "I_matter_EM_flux",
            "abs(int_BF[-int_S i_tau omega_{matter+EM}+C_tau^{matter+EM}])",
            "Hamiltonian curl numerator units",
            "0 if NFC3579_0..5 are signed; otherwise bounded by public EM energy/current flux rows below",
            "CONDITIONAL_ZERO_ELSE_BOUND_READY",
            "curl_components_3578",
        ),
        (
            "PFB3579_1_Phi_EM_rad",
            "Phi_EM_rad",
            "int_boundary S_Poynting dot n dA",
            "power or energy/time in observed local frame",
            "Use |int_dt Phi_EM_rad|/(M_H c^2) for a dimensionless window, or |Phi_EM_rad|/(M_H c^2) as time^-1 leakage.",
            "BOUND_ROW_READY_VALUE_MISSING",
            "em_poynting_vector_3502",
        ),
        (
            "PFB3579_2_public_work_exchange",
            "W_public_exchange",
            "int_BF int_V J dot E dV dt",
            "energy in observed local frame",
            "Zero for stationary internal exchange in the total matter+EM stress; otherwise an absolute exchange-row is needed.",
            "CONDITIONAL_ZERO_IN_TOTAL_STRESS_ELSE_BOUND",
            "maxwell_poynting_3463",
        ),
        (
            "PFB3579_3_surface_gauge_corner",
            "C_EM_surface_gauge",
            "surface EM gauge/corner contribution to C_tau^{EM}",
            "Hamiltonian curl numerator units",
            "Zero if the EM gauge representative and charge sector are fixed on the linking surface; otherwise retained as a corner bound.",
            "SURFACE_GAUGE_CERTIFICATE_REQUIRED",
            "em_hodge_bound_3503",
        ),
        (
            "PFB3579_4_Hodge_flow_mismatch",
            "Delta_Hodge_EM",
            "*_EM-*_obs[e_obs(q)] or chi_EM-chi_obs",
            "dimensionless_or_tensor",
            "Not part of ordinary Poynting no-flux, but if nonzero it changes what flux means and must feed Maxwell/clock/PPN gates.",
            "RETAINED_COUPLING_GATE",
            "em_hodge_bound_3503",
        ),
        (
            "PFB3579_5_EM_normalization_multiplier",
            "w_EM",
            "S_EM -> w_EM S_EM; T_EM -> w_EM T_EM",
            "dimensionless",
            "Stationary flux zero does not fix the absolute EM stress normalization; this remains an EM-owner/source-calibration gate.",
            "RETAINED_COUPLING_GATE",
            "em_alpha_charge_3464",
        ),
        (
            "PFB3579_6_hidden_F2_counterterm",
            "C_XF2",
            "Delta S ~ int sqrt(-g) f_X(Phi) F_{mn}F^{mn}",
            "model_dependent",
            "Stationary public no-flux does not ban hidden-visible F2 operators.",
            "RETAINED_COUPLING_GATE",
            "em_owner_3465",
        ),
        (
            "PFB3579_7_readout_radiative_regeneration",
            "C_EM_readout",
            "S_eff/readout regenerates f_X F^2, alpha_X, or EM binding response",
            "model_dependent",
            "Stationary classical no-flux does not prove radiative/readout closure.",
            "RETAINED_COUPLING_GATE",
            "em_current_ward_3508",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "zero_or_bound_rule": rule,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "numeric_value": "MISSING_NUMERIC_OR_PARENT_ZERO",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, rule, status, source_key in specs
    ]


def htau_update_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "HCU3579_0_before",
            "I_matter_EM_flux",
            "3578 status: PUBLIC_FLUX_BOUND_REQUIRED",
            "public EM/matter contribution was live and unsplit",
            "curl_components_3578",
        ),
        (
            "HCU3579_1_after_conditional",
            "I_matter_EM_flux",
            "CONDITIONAL_ZERO_ON_STRICT_PUBLIC_LOCAL_EXTERIOR_ELSE_FLUX_BOUND_READY",
            "if same-Hodge, same-current, stationary, no-radiation, no-current-crossing, fixed-gauge-surface clauses are signed, this component is zero",
            "maxwell_poynting_3463",
        ),
        (
            "HCU3579_2_after_fallback",
            "Delta_H_curl_bound",
            "replace live I_matter_EM_flux by Phi_EM_rad + W_public_exchange + C_EM_surface_gauge if clauses fail",
            "the total H_tau curl vector remains nonzero/not claimed because other components live",
            "curl_components_3578",
        ),
        (
            "HCU3579_3_live_after_3579",
            "live_Htau_components",
            "I_extra;I_boundary_corner;I_tau_surface;I_qdescent_current;plus_public_EM_flux_if_no_flux_clause_unsigned",
            "3579 narrows the public EM term but does not close the local GR branch",
            "status_3578",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": update_id,
            "target": target,
            "status": status,
            "effect": effect,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for update_id, target, status, effect, source_key in specs
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3579_0_sources", "source audit", "PASS", "all required source paths exist and anchors are present"),
        ("GATE3579_1_standard_public_EM", "standard Maxwell/Poynting identities", "PASS_CONDITIONAL", "public EM stress, Poynting current, and matter-EM exchange identities are recorded"),
        ("GATE3579_2_no_flux_theorem", "I_matter_EM_flux zero", "PASS_CONDITIONAL_ONLY", "zero theorem holds only under strict stationary/source-free/no-radiation/fixed-surface clauses"),
        ("GATE3579_3_parent_local_exterior", "parent-owned local exterior clauses", "FAIL_CURRENT_CLAIM", "stationarity, no-radiation, current containment, and fixed gauge/surface are not parent-signed globally"),
        ("GATE3579_4_coupling_owner", "EM owner/coupling gates", "FAIL_CURRENT_CLAIM", "Delta_Hodge_EM, w_EM, C_XF2, charge/current owner and readout/radiative closure remain separate gates"),
        ("GATE3579_5_total_Htau_curl", "full H_tau curl zero", "FAIL_CURRENT_CLAIM", "I_extra, I_boundary_corner, I_tau_surface, and I_qdescent_current remain live"),
        ("GATE3579_6_local_GR", "local GR/Newton/PPN pass", "FAIL_CURRENT_CLAIM", "public EM narrowing is useful but insufficient for local GR reduction"),
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
            "source_path": str(source_paths["status_3578"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3579_0_public_EM_zero",
            "accept strict conditional no-flux theorem for public EM/matter component",
            "This is a real derived component zero, but only if the local exterior clauses are signed.",
            "I_matter_EM_flux is no longer a shapeless missing term; it has a theorem-zero branch and a fallback flux-bound branch.",
            "ADOPTED_NONCLAIM",
            "maxwell_poynting_3463",
        ),
        (
            "DEC3579_1_no_alpha_overreach",
            "separate Poynting no-flux from EM coupling ownership",
            "A stationary EM flux zero does not derive alpha, unique F2, charge normalization, or hidden-visible coefficient exclusion.",
            "prevents a fake Maxwell/local-GR pass while preserving the useful public stress result",
            "ADOPTED_GUARD",
            "em_owner_3465",
        ),
        (
            "DEC3579_2_next_target",
            "attack the strict local exterior certificate next",
            "The least speculative next move is to parent-sign or bound stationarity/no-radiation/current-containment/gauge-surface clauses rather than return immediately to hidden extra-sector actions.",
            "3580 should prove the local exterior no-radiation/worldtube-surface certificate or emit concrete flux rows.",
            "NEXT_TARGET_SELECTED",
            "hilbert_worldtube_536",
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
            "status": "PUBLIC_EM_POYNTING_HTAU_COMPONENT_CONDITIONAL_ZERO_AND_BOUND_READY",
            "strongest_result": "The public matter+EM H_tau curl component has a concrete conditional zero: in a compact stationary local exterior with same observed Hodge, same matter/EM current owner, no radiative Poynting flux, no current crossing the linking surface, and fixed EM gauge/surface data, I_matter_EM_flux=0.",
            "still_missing": "parent-owned local exterior certificate, no-radiation/current-containment/gauge-surface proof, EM Hodge/unique-F2/normalization/current/readout coupling owners, and all other live H_tau curl components",
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
            "next_id": "NEXT3579_0",
            "target_doc": "3580-Y5-R2FR-local-exterior-no-radiation-worldtube-surface-certificate-or-flux-rows.md",
            "target_script": "scripts/Y5_R2FR_3580_local_exterior_no_radiation_worldtube_surface_certificate_or_flux_rows.py",
            "objective": "derive the strict local exterior certificate needed by the 3579 public EM/Poynting no-flux theorem, or emit concrete nonclaim flux rows for radiation, current crossing, and EM surface gauge/corner leakage",
            "success_gate": "NFC3579_2 through NFC3579_5 are parent-signed for the local exterior branch, or PFB3579_1 through PFB3579_3 have sourced bound inputs and units",
            "reason": "3579 reduces public EM to a sharp local-exterior condition; 3580 should try to own that condition before returning to extra-sector curl components",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "I_matter_EM_flux",
            "status": "CONDITIONAL_ZERO_ELSE_FLUX_BOUND_READY",
            "zero_branch": "same_Hodge + same_current_owner + stationary_tau + no_radiative_boundary_flux + no_current_crossing_surface + fixed_EM_gauge_surface",
            "fallback_bound": "Phi_EM_rad + W_public_exchange + C_EM_surface_gauge",
            "scope_guard": "does_not_derive_alpha_unique_F2_wEM_CXF2_or_total_Htau_curl",
            "next_action": "derive local exterior no-radiation/worldtube-surface certificate or fill flux rows",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorems: list[dict[str, object]],
    conditions: list[dict[str, object]],
    bounds: list[dict[str, object]],
    updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3579_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3579 source paths exist"))
    needles = {
        "handoff_3578": "NEXT3578_0",
        "curl_components_3578": "HCURL3578_3_public_matter_EM",
        "curl_identities_3578": "CID3578_1_curl",
        "theta_qtau_3578": "TQU3578_1_matter_EM",
        "status_3578": "HTAU_CURL_COMPONENT_VECTOR_READY",
        "maxwell_poynting_3463": "EM3463_2_poynting",
        "em_owner_3465": "EMO3465_5_verdict",
        "em_alpha_charge_3464": "EAC3464_5_verdict",
        "em_poynting_vector_3502": "EMF3502_1_radiative_poynting_flux",
        "em_hodge_bound_3503": "EMB3503_4_Phi_EM_rad",
        "em_current_ward_3508": "CSR3508_6_nonHilbert_bypass",
        "em_no_source_only_3509": "NSSR3509_6_nonHilbert_source_bypass",
        "em_visible_status_3525": "STAT3525_0_branch",
        "em_unique_status_3528": "STAT3528_0_unique_F2",
        "em_same_owner_3547": "STATUS3547_0",
        "source_current_532": "SC532_1_Hilbert_source_current",
        "hilbert_worldtube_536": "HWT536_0_parent_worldtube_fixed",
    }
    validations.append(("VAL3579_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected EM/Poynting and H_tau anchors found"))
    validations.append(("VAL3579_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3579 output files written"))
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
    validations.append(("VAL3579_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3579_4_poynting_identity_present", any(row["theorem_id"] == "PEM3579_2_poynting_flux_identity" for row in theorems), "Poynting flux identity row present"))
    validations.append(("VAL3579_5_conditional_zero_present", any(row["theorem_id"] == "PEM3579_3_covariant_phase_space_zero" and row["status"] == "CONDITIONAL_THEOREM_ZERO_WRITTEN" for row in theorems), "conditional covariant phase-space zero row present"))
    required_conditions = {"NFC3579_2_stationary_generator", "NFC3579_3_no_radiative_boundary_flux", "NFC3579_4_no_current_crossing_surface", "NFC3579_5_fixed_EM_gauge_surface"}
    validations.append(("VAL3579_6_strict_conditions_retained", required_conditions.issubset({str(row["condition_id"]) for row in conditions}), "strict local exterior conditions retained"))
    validations.append(("VAL3579_7_flux_bound_rows_present", {"Phi_EM_rad", "W_public_exchange", "C_EM_surface_gauge"}.issubset({str(row["symbol"]) for row in bounds}), "fallback flux/corner bound rows present"))
    validations.append(("VAL3579_8_no_alpha_overclaim", any(row["theorem_id"] == "PEM3579_4_not_alpha_owner" for row in theorems), "scope guard prevents alpha/unique-F2 overclaim"))
    validations.append(("VAL3579_9_htau_update_present", any(row["update_id"] == "HCU3579_1_after_conditional" and "CONDITIONAL_ZERO" in str(row["status"]) for row in updates), "H_tau component update present"))
    validations.append(("VAL3579_10_total_curl_not_claimed", any(row["gate_id"] == "GATE3579_5_total_Htau_curl" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "full H_tau curl remains unclaimed"))
    validations.append(("VAL3579_11_next_target_selected", any(row["decision_id"] == "DEC3579_2_next_target" for row in decisions), "local exterior certificate next target selected"))
    validations.append(("VAL3579_12_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in theorems + conditions + bounds + updates + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorems + conditions + bounds + updates + gates + decisions)
    validations.append(("VAL3579_13_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3579*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3579_14_formalization_workbench_untouched", not formalization_touched, "no 3579 checkpoint output appears in formalization-workbench"))
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
    theorems: list[dict[str, object]],
    conditions: list[dict[str, object]],
    bounds: list[dict[str, object]],
    updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3579 - Public EM/Poynting Htau curl zero or flux bound",
        "",
        "## Verdict",
        "3579 gives the public matter+EM `H_tau` curl component a real theorem branch: under a compact stationary local exterior with the same observed Hodge/coframe, the same matter/EM current owner, no net radiative Poynting flux, no charged current crossing the linking surface, and fixed EM gauge/surface data, `I_matter_EM_flux=0`.",
        "",
        "This is useful but not a local-GR or Maxwell-owner victory.  It does **not** derive `alpha_EM`, unique `F^2`, `w_EM=0`, `C_XF2=0`, or the full `H_tau` curl.  If the strict exterior clauses are not parent-signed, the fallback is `Phi_EM_rad + W_public_exchange + C_EM_surface_gauge` as explicit flux/corner rows.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Public EM theorem branch"])
    for row in theorems:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## No-flux conditions"])
    for row in conditions:
        lines.append(f"- `{row['condition_id']}` `{row['condition']}`: {row['status']} ({row['reason']})")
    lines.extend(["", "## Fallback bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Htau component update"])
    for row in updates:
        lines.append(f"- `{row['update_id']}` `{row['target']}`: {row['status']} -> {row['effect']}")
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
    theorems = theorem_rows(source_paths)
    conditions = no_flux_condition_rows(source_paths)
    bounds = flux_bound_rows(source_paths)
    updates = htau_update_rows(source_paths)
    gates = gate_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3579_SOURCE_REGISTER.csv",
        "public_em_theorem": RESIDUALS / "P8_Y5_R2FR_3579_PUBLIC_EM_POYNTING_THEOREM.csv",
        "no_flux_conditions": RESIDUALS / "P8_Y5_R2FR_3579_NO_FLUX_CONDITIONS.csv",
        "flux_bound_rows": RESIDUALS / "P8_Y5_R2FR_3579_POYNTING_FLUX_BOUND_ROWS.csv",
        "htau_component_update": RESIDUALS / "P8_Y5_R2FR_3579_HTAU_COMPONENT_UPDATE.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3579_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3579_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3579_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3579_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_I_matter_EM_flux_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3579_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["public_em_theorem"], theorems)
    write_csv(outputs["no_flux_conditions"], conditions)
    write_csv(outputs["flux_bound_rows"], bounds)
    write_csv(outputs["htau_component_update"], updates)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, theorems, conditions, bounds, updates, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, theorems, conditions, bounds, updates, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3579 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
