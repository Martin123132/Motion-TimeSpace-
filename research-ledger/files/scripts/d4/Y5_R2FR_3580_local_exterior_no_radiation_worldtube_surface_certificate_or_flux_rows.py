from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3580-Y5-R2FR-local-exterior-no-radiation-worldtube-surface-certificate-or-flux-rows.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_LOCAL_EXTERIOR_POYNTING_CERTIFICATE_3580"
CHECKPOINT_ID = "3580"


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
        "handoff_3579": RESIDUALS / "P8_Y5_R2FR_3579_NEXT_TARGET.csv",
        "theorem_3579": RESIDUALS / "P8_Y5_R2FR_3579_PUBLIC_EM_POYNTING_THEOREM.csv",
        "conditions_3579": RESIDUALS / "P8_Y5_R2FR_3579_NO_FLUX_CONDITIONS.csv",
        "flux_rows_3579": RESIDUALS / "P8_Y5_R2FR_3579_POYNTING_FLUX_BOUND_ROWS.csv",
        "status_3579": RESIDUALS / "P8_Y5_R2FR_3579_STATUS.csv",
        "maxwell_poynting_3463": RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
        "poynting_vector_3502": RESIDUALS / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "poynting_functional_3234": ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
        "stationary_status_3538": RESIDUALS / "P8_local_GR_observed_flow_stationary_branch_status.csv",
        "stationary_certificate_686": RESIDUALS / "P8_Y5_R10_686_LOCAL_STATIONARY_CERTIFICATE.csv",
        "tau_owner_2067": RESIDUALS / "P8_Y5_PARENT_QLOC_2067_STATIONARY_TAU_OWNER_ATTEMPT.csv",
        "surface_owner_2066": RESIDUALS / "P8_Y5_PARENT_QLOC_2066_STATIONARY_SURFACE_OWNER_ATTEMPT.csv",
        "surface_requirements_2065": RESIDUALS / "P8_Y5_PARENT_QLOC_2065_ACTUAL_SURFACE_REQUIREMENTS.csv",
        "worldtube_support_2388": RESIDUALS / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv",
        "source_support_3560": ROOT / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md",
        "boundary_flux_2248": RESIDUALS / "P8_Y5_PARENT_QLOC_2248_BOUNDARY_FLUX_ZERO_GATE.csv",
        "boundary_flux_fill_549": RESIDUALS / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv",
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
            "role": "3580 local exterior Poynting no-radiation/worldtube/surface certificate input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "LET3580_0_stationary_annulus",
            "local exterior annulus object",
            "A_tau(R_in,R_out)=Sigma_tau cap exterior(W_source) cap {R_in<=r<=R_out}; partial A=S_out union (-S_in)",
            "This is the clean object for the no-radiation certificate: a spatial stationary annulus with no time caps and no source support in the collar.",
            "CANDIDATE_OBJECT_DEFINED_NOT_PARENT_SIGNED",
            "surface_owner_2066",
        ),
        (
            "LET3580_1_covariant_poynting_current",
            "Killing-energy current for public EM",
            "j_EM^mu[tau]=-T_EM^{mu nu}tau_nu; div j_EM = -T_EM^{mu nu}nabla_(mu tau_nu)+tau_nu F^{nu lambda}J_lambda",
            "For a Killing tau and source-free collar, the EM energy current is closed. This is the covariant version of Poynting transport.",
            "EXACT_CONDITIONAL_IDENTITY",
            "maxwell_poynting_3463",
        ),
        (
            "LET3580_2_flux_transport",
            "stationary source-free collar flux transport",
            "Phi_out-Phi_in = int_A [partial_tau u_EM + J dot E + T_EM^{mu nu}nabla_(mu tau_nu)] dV + C_corner",
            "If the collar is stationary, source-free, same-tau, and corner-free, the net Poynting flux is radially transported: Phi_out=Phi_in.",
            "TRANSPORT_THEOREM_DERIVED_CONDITIONAL",
            "poynting_functional_3234",
        ),
        (
            "LET3580_3_zero_anchor",
            "no-radiation is a boundary anchor, not an automatic consequence",
            "Phi_out=Phi_in and Phi_anchor=0 => Phi_EM_rad=0 on all linked surfaces",
            "3580 refuses the shortcut: stationarity/source-free collar proves equality of fluxes, not zero, until one owned anchor is zero.",
            "ZERO_REDUCED_TO_ANCHOR_PLUS_TRANSPORT",
            "poynting_vector_3502",
        ),
        (
            "LET3580_4_htau_component",
            "3579 public EM H_tau component",
            "I_matter_EM_flux=0 if transport defect, anchor flux, crossing flux, and EM gauge/corner terms all vanish",
            "This is the usable activation contract for 3579; otherwise the same terms become absolute nonclaim bound rows.",
            "HTAU_ACTIVATION_CONTRACT_WRITTEN",
            "theorem_3579",
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


def transport_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "TRL3580_0_divergence_identity",
            "div j_EM[tau]",
            "-T_EM^{mu nu}nabla_(mu tau_nu)+tau_nu F^{nu lambda}J_lambda",
            "exact identity from Maxwell stress conservation and Killing-energy current definition",
            "EXACT_CONDITIONAL",
            "maxwell_poynting_3463",
        ),
        (
            "TRL3580_1_stationary_killing_zero",
            "T_EM symgrad(tau)",
            "T_EM^{mu nu}nabla_(mu tau_nu)=0",
            "zero if the same observed tau is Killing on the local exterior collar",
            "ZERO_IF_STATIONARY_TAU_OWNER_SIGNED",
            "tau_owner_2067",
        ),
        (
            "TRL3580_2_source_free_collar_zero",
            "tau.F.J collar work",
            "tau_nu F^{nu lambda}J_lambda=0 in A_tau",
            "zero if compact source support is inside S_in and no charged current crosses the collar",
            "ZERO_IF_WORLDTUBE_SUPPORT_NO_CROSSING_SIGNED",
            "worldtube_support_2388",
        ),
        (
            "TRL3580_3_surface_transport",
            "Phi_out-Phi_in",
            "int_{S_out} S dot n dA - int_{S_in} S dot n dA = 0",
            "follows from TRL3580_0..2 and a corner-free stationary spatial annulus",
            "TRANSPORT_ZERO_IF_SURFACE_OWNER_SIGNED",
            "surface_owner_2066",
        ),
        (
            "TRL3580_4_anchor_zero",
            "Phi_anchor",
            "Phi_anchor in {Phi_in, Phi_out, Phi_infty, prescribed no-incoming/no-outgoing boundary}",
            "one owned zero anchor is still required before transport becomes no-radiation",
            "ANCHOR_REQUIRED_NOT_AUTOMATIC",
            "poynting_vector_3502",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "transport_id": transport_id,
            "quantity": quantity,
            "formula": formula,
            "result": result,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for transport_id, quantity, formula, result, status, source_key in specs
    ]


def clause_audit_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "LCA3580_0_same_hodge_current",
            "NFC3579_0;NFC3579_1",
            "same observed Hodge and same public matter/EM current owner",
            "PASS_CONDITIONAL_FROM_3463",
            "enough for public stress accounting but not full EM coupling ownership",
            "maxwell_poynting_3463",
        ),
        (
            "LCA3580_1_stationary_tau",
            "NFC3579_2",
            "same observed stationary generator on the collar",
            "NARROWED_TO_TAU_KILLING_OWNER",
            "must prove tau_obs is parent-selected and Killing on the exterior collar, not fitted after readout",
            "tau_owner_2067",
        ),
        (
            "LCA3580_2_no_radiation",
            "NFC3579_3",
            "no net radiative/background Poynting leakage",
            "NARROWED_TO_TRANSPORT_PLUS_ZERO_ANCHOR",
            "source-free stationary collar gives Phi_out=Phi_in; zero additionally requires one owned zero anchor",
            "poynting_vector_3502",
        ),
        (
            "LCA3580_3_no_current_crossing",
            "NFC3579_4",
            "charged matter worldtube is inside the linking surface and no current crosses boundary",
            "NARROWED_TO_WORLDTUBE_SUPPORT_NO_CROSSING",
            "3560 gives a support-descent route, but compact support/no crossing remains unsigned unless parent-owned",
            "source_support_3560",
        ),
        (
            "LCA3580_4_fixed_gauge_surface",
            "NFC3579_5",
            "fixed EM gauge representative and surface class",
            "NARROWED_TO_CONSTANT_GAUGE_PLUS_CORNER_FREE_SURFACE",
            "gauge/corner contribution vanishes only if gauge parameter is constant on closed compatible surfaces or the corner term is exact/proper",
            "poynting_functional_3234",
        ),
        (
            "LCA3580_5_surface_owner",
            "implicit surface clause",
            "S_in, S_out, Sigma_tau and regulator seams are the actual action/source/readout surfaces",
            "REQUIRED_NOT_PARENT_SIGNED",
            "2065/2066 show the annulus is mathematically clean but not yet arena-certified as the actual parent surface",
            "surface_requirements_2065",
        ),
        (
            "LCA3580_6_verdict",
            "local exterior certificate",
            "transport theorem exists; full no-radiation certificate is not parent-signed",
            "CERTIFICATE_NARROWED_NOT_PROMOTED",
            "do not claim I_matter_EM_flux=0 unless tau/surface/worldtube/anchor/gauge clauses all close",
            "status_3579",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "upstream_clause": upstream_clause,
            "clause": clause,
            "status": status,
            "reason": reason,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, upstream_clause, clause, status, reason, source_key in specs
    ]


def flux_bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "LFB3580_0_transport_defect",
            "Delta_Phi_transport",
            "abs(Phi_out-Phi_in)",
            "power or energy/time",
            "bounded by int_A(|partial_tau u_EM|+|J dot E|+|T_EM symgrad(tau)|)dV + |C_corner|",
            "ZERO_IF_STATIONARY_SOURCE_FREE_CORNER_FREE_ELSE_BOUND",
            "poynting_functional_3234",
        ),
        (
            "LFB3580_1_flux_anchor",
            "Phi_anchor",
            "min anchor among |Phi_in|, |Phi_out|, |Phi_infty|, or specified no-incoming/no-outgoing condition",
            "power or energy/time",
            "must be theorem-zero or sourced as a finite boundary/asymptotic flux value",
            "ANCHOR_VALUE_OR_ZERO_REQUIRED",
            "poynting_vector_3502",
        ),
        (
            "LFB3580_2_current_crossing",
            "J_cross_EM",
            "int_boundary(A_tau) |J^mu n_mu| dSigma",
            "charge/time or current flux units",
            "zero if source support is compactly inside S_in and no charged current crosses linked surfaces",
            "WORLDTUBE_NO_CROSSING_OR_BOUND_REQUIRED",
            "worldtube_support_2388",
        ),
        (
            "LFB3580_3_surface_gauge_corner",
            "C_EM_surface_gauge",
            "absolute EM gauge/corner term in C_tau^EM on S_in union S_out",
            "Hamiltonian curl numerator units",
            "zero for constant gauge on closed compatible surfaces or exact/proper corner form; otherwise bound explicitly",
            "GAUGE_SURFACE_CERTIFICATE_OR_BOUND_REQUIRED",
            "poynting_functional_3234",
        ),
        (
            "LFB3580_4_regulator_corner",
            "B_corner_flux",
            "sum over active cutoff/excision/regulator/matched-patch seam fluxes",
            "Hamiltonian curl numerator units",
            "zero only if all seams are absent or separately exact/proper",
            "REGULATOR_LEDGER_OR_BOUND_REQUIRED",
            "surface_requirements_2065",
        ),
        (
            "LFB3580_5_total_public_EM_flux",
            "Phi_EM_public_abs",
            "Phi_anchor_abs + Delta_Phi_transport_abs + J_cross_work_abs + C_EM_surface_gauge_abs + B_corner_flux_abs",
            "Hamiltonian curl numerator units or normalized by M_H_ref c^2 over a stated window",
            "no cancellation credit; every positive component must be zero or bounded",
            "BOUND_FORMULA_READY_INPUT_VALUES_MISSING",
            "flux_rows_3579",
        ),
        (
            "LFB3580_6_Htau_feed",
            "I_matter_EM_flux",
            "I_matter_EM_flux <= A_F sup_BF Phi_EM_public_abs",
            "Hamiltonian curl numerator units",
            "feeds 3579/3578 H_tau curl vector until all rows zero",
            "HTAU_FEED_READY_NONCLAIM",
            "conditions_3579",
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
            "HTU3580_0_3579_refinement",
            "PFB3579_1_Phi_EM_rad",
            "replace generic Phi_EM_rad with Phi_anchor + Delta_Phi_transport + crossing/gauge/corner rows",
            "public EM flux is now a transport/anchor problem, not a vague radiation placeholder",
            "flux_rows_3579",
        ),
        (
            "HTU3580_1_activation_rule",
            "I_matter_EM_flux",
            "I_matter_EM_flux=0 if LET3580 transport clauses plus zero anchor plus no-crossing plus gauge/surface clauses all close",
            "strict activation rule for 3579 public EM zero",
            "theorem_3579",
        ),
        (
            "HTU3580_2_nonclaim_bound",
            "Delta_H_curl_bound",
            "retain A_F sup_BF Phi_EM_public_abs if any clause is unsigned",
            "full H_tau curl remains nonclaim and no local-GR promotion follows",
            "status_3579",
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
        ("GATE3580_0_sources", "source audit", "PASS", "all required 3580 source paths and anchors exist"),
        ("GATE3580_1_transport_law", "stationary source-free Poynting transport", "PASS_CONDITIONAL", "Phi_out=Phi_in follows under Killing tau, source-free collar, and corner-free annulus"),
        ("GATE3580_2_no_radiation_zero", "Phi_EM_rad=0", "FAIL_CURRENT_CLAIM", "transport does not imply zero without a parent-owned zero anchor"),
        ("GATE3580_3_tau_surface_owner", "same tau and actual surface owner", "FAIL_CURRENT_CLAIM", "2065/2066/2067 still mark parent tau/surface ownership unsigned"),
        ("GATE3580_4_worldtube_no_crossing", "current crossing zero", "FAIL_CURRENT_CLAIM", "2388/3560 give a route, but compact support/no crossing is not parent-signed"),
        ("GATE3580_5_gauge_corner", "EM gauge/surface corner zero", "FAIL_CURRENT_CLAIM", "constant gauge/exact corner route is conditional only"),
        ("GATE3580_6_htau_public_EM", "I_matter_EM_flux zero", "FAIL_CURRENT_CLAIM", "zero allowed only after all above gates close; otherwise use LFB3580 rows"),
        ("GATE3580_7_local_GR", "local GR/Newton/PPN pass", "FAIL_CURRENT_CLAIM", "public EM branch narrowed, but other H_tau/local-GR residuals remain live"),
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
            "source_path": str(source_paths["status_3579"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3580_0_transport_not_magic_zero",
            "accept the transport theorem and reject automatic no-radiation",
            "Poynting conservation in a stationary source-free collar proves radial equality of fluxes, not zero.",
            "the zero proof now has a precise missing anchor instead of a vague radiation assumption",
            "ADOPTED",
            "poynting_functional_3234",
        ),
        (
            "DEC3580_1_worldtube_surface_precision",
            "bind no-crossing and no-corner claims to actual parent surfaces",
            "Current support/surface files show the clean annulus exists mathematically but is not yet parent-signed as the actual local branch surface.",
            "prevents scoring a no-flux theorem on the wrong boundary",
            "ADOPTED_GUARD",
            "surface_requirements_2065",
        ),
        (
            "DEC3580_2_next_target",
            "attack stationary annulus same-tau/surface ownership plus flux anchor",
            "This is the shared bottleneck for 3579 public EM zero and several H_tau/local-GR denominator terms.",
            "3581 should try to parent-sign the common stationary annulus/tau/surface/anchor package or fill the first finite anchor/corner rows.",
            "NEXT_TARGET_SELECTED",
            "tau_owner_2067",
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
            "status": "POYNTING_TRANSPORT_THEOREM_DERIVED_ZERO_REDUCED_TO_ANCHOR_AND_SURFACE_CERTIFICATE",
            "strongest_result": "In a stationary source-free public EM collar, the Poynting/Killing-energy flux is transported between linked surfaces: Phi_out=Phi_in up to explicit transport, crossing, gauge and corner defects. Therefore no-radiation is reduced to one owned zero anchor plus the same tau/surface/worldtube/gauge certificate.",
            "still_missing": "parent-owned stationary tau, actual action/source/readout surface class, compact support/no-crossing certificate, zero flux anchor, EM gauge/corner certificate, and numeric/source-backed values if any clause fails",
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
            "next_id": "NEXT3580_0",
            "target_doc": "3581-Y5-R2FR-stationary-annulus-same-tau-surface-owner-or-flux-anchor-row.md",
            "target_script": "scripts/Y5_R2FR_3581_stationary_annulus_same_tau_surface_owner_or_flux_anchor_row.py",
            "objective": "parent-sign the common stationary annulus/tau/surface/zero-anchor package used by the 3580 Poynting transport theorem, or emit the first finite Phi_anchor, tau-surface, and EM gauge/corner rows with units",
            "success_gate": "same tau, S_in/S_out, source support, and one zero flux anchor are signed on the same branch, or LFB3580_1 through LFB3580_4 become sourced nonclaim bound rows",
            "reason": "3580 proves transport; the remaining step is owning the actual stationary annulus and zero anchor rather than repeating generic Poynting objections",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "local_exterior_Poynting_certificate",
            "status": "TRANSPORT_THEOREM_READY_ZERO_ANCHOR_MISSING",
            "derived_law": "Phi_out-Phi_in = transport_defect + crossing + gauge/corner terms",
            "zero_activation": "stationary_tau + source_free_collar + no_crossing + corner_free_surface + one_zero_anchor",
            "fallback_bound": "Phi_anchor_abs + Delta_Phi_transport_abs + J_cross_work_abs + C_EM_surface_gauge_abs + B_corner_flux_abs",
            "next_action": "own stationary annulus/tau/surface/anchor or fill finite rows",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorems: list[dict[str, object]],
    transport: list[dict[str, object]],
    clauses: list[dict[str, object]],
    bounds: list[dict[str, object]],
    updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3580_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3580 source paths exist"))
    needles = {
        "handoff_3579": "NEXT3579_0",
        "theorem_3579": "PEM3579_2_poynting_flux_identity",
        "conditions_3579": "NFC3579_3_no_radiative_boundary_flux",
        "flux_rows_3579": "PFB3579_1_Phi_EM_rad",
        "status_3579": "PUBLIC_EM_POYNTING_HTAU_COMPONENT",
        "maxwell_poynting_3463": "EM3463_2_poynting",
        "poynting_vector_3502": "EMF3502_1_radiative_poynting_flux",
        "poynting_functional_3234": "PF3234_0_functional",
        "stationary_status_3538": "STAT3538_1_stationary",
        "stationary_certificate_686": "LSC686_1_stationary_solution",
        "tau_owner_2067": "STO2067_1_Killing_identity",
        "surface_owner_2066": "SSO2066_1_domain_Dstat",
        "surface_requirements_2065": "ASR2065_2_source_selector",
        "worldtube_support_2388": "WSC2388_5_no_crossing",
        "source_support_3560": "SWT3560_4_failure_decomposition",
        "boundary_flux_2248": "BFG2248_5_verdict",
        "boundary_flux_fill_549": "FB549_0_boundary_flux_bound",
    }
    validations.append(("VAL3580_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3580 anchors found"))
    validations.append(("VAL3580_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3580 output files written"))
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
    validations.append(("VAL3580_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3580_4_transport_theorem_present", any(row["theorem_id"] == "LET3580_2_flux_transport" for row in theorems), "flux transport theorem row present"))
    validations.append(("VAL3580_5_anchor_not_overclaimed", any(row["theorem_id"] == "LET3580_3_zero_anchor" and "ANCHOR" in str(row["status"]) for row in theorems), "zero anchor requirement retained"))
    validations.append(("VAL3580_6_transport_components_present", {"TRL3580_1_stationary_killing_zero", "TRL3580_2_source_free_collar_zero", "TRL3580_4_anchor_zero"}.issubset({str(row["transport_id"]) for row in transport}), "stationary/source-free/anchor transport rows present"))
    validations.append(("VAL3580_7_clause_audit_present", {"LCA3580_1_stationary_tau", "LCA3580_2_no_radiation", "LCA3580_3_no_current_crossing", "LCA3580_4_fixed_gauge_surface"}.issubset({str(row["clause_id"]) for row in clauses}), "3579 clause audit narrowed"))
    validations.append(("VAL3580_8_bound_rows_present", {"Phi_anchor", "Delta_Phi_transport", "J_cross_EM", "C_EM_surface_gauge", "Phi_EM_public_abs"}.issubset({str(row["symbol"]) for row in bounds}), "finite fallback rows present"))
    validations.append(("VAL3580_9_htau_update_present", any(row["update_id"] == "HTU3580_1_activation_rule" for row in updates), "H_tau activation update present"))
    validations.append(("VAL3580_10_no_zero_claim", any(row["gate_id"] == "GATE3580_2_no_radiation_zero" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "no-radiation zero not overclaimed"))
    validations.append(("VAL3580_11_next_target_selected", any(row["decision_id"] == "DEC3580_2_next_target" for row in decisions), "3581 target selected"))
    validations.append(("VAL3580_12_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in theorems + transport + clauses + bounds + updates + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorems + transport + clauses + bounds + updates + gates + decisions)
    validations.append(("VAL3580_13_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3580*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3580_14_formalization_workbench_untouched", not formalization_touched, "no 3580 checkpoint output appears in formalization-workbench"))
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
    transport: list[dict[str, object]],
    clauses: list[dict[str, object]],
    bounds: list[dict[str, object]],
    updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3580 - Local exterior no-radiation worldtube/surface certificate or flux rows",
        "",
        "## Verdict",
        "3580 proves the useful part and refuses the fake part.  In a stationary, source-free public EM collar the Poynting/Killing-energy flux is transported between linked surfaces: `Phi_out=Phi_in` up to explicit transport, crossing, gauge and corner defects.",
        "",
        "That is not yet `Phi_EM_rad=0`.  No-radiation is reduced to a precise activation package: same stationary `tau`, actual `S_in/S_out` surface ownership, compact worldtube/no-crossing, corner-free fixed EM gauge surface, and one owned zero flux anchor.  If any clause fails, the fallback is the absolute nonclaim row `Phi_EM_public_abs`.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Local exterior theorem"])
    for row in theorems:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Transport rows"])
    for row in transport:
        lines.append(f"- `{row['transport_id']}` `{row['quantity']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}` `{row['upstream_clause']}`: {row['status']} ({row['reason']})")
    lines.extend(["", "## Flux bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Htau update"])
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
    transport = transport_rows(source_paths)
    clauses = clause_audit_rows(source_paths)
    bounds = flux_bound_rows(source_paths)
    updates = htau_update_rows(source_paths)
    gates = gate_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3580_SOURCE_REGISTER.csv",
        "local_exterior_theorem": RESIDUALS / "P8_Y5_R2FR_3580_LOCAL_EXTERIOR_CERTIFICATE_THEOREM.csv",
        "transport_law": RESIDUALS / "P8_Y5_R2FR_3580_STATIONARY_COLLAR_TRANSPORT_LAW.csv",
        "clause_audit": RESIDUALS / "P8_Y5_R2FR_3580_CERTIFICATE_CLAUSE_AUDIT.csv",
        "flux_bound_rows": RESIDUALS / "P8_Y5_R2FR_3580_FLUX_BOUND_ROWS.csv",
        "htau_update": RESIDUALS / "P8_Y5_R2FR_3580_HTAU_UPDATE.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3580_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3580_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3580_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3580_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_local_exterior_no_radiation_certificate_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3580_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["local_exterior_theorem"], theorems)
    write_csv(outputs["transport_law"], transport)
    write_csv(outputs["clause_audit"], clauses)
    write_csv(outputs["flux_bound_rows"], bounds)
    write_csv(outputs["htau_update"], updates)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, theorems, transport, clauses, bounds, updates, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, theorems, transport, clauses, bounds, updates, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3580 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
