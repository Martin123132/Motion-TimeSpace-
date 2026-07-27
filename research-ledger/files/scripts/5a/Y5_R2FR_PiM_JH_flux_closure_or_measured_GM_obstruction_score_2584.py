from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_PIM_JH_FLUX_CLOSURE_2584"
CHECKPOINT_ID = "2584"

DOC = ROOT / "2584-Y5-R2FR-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PIM_JH_FLUX_2584_SOURCE_REGISTER.csv",
    "closure_audit": OUT / "P8_Y5_PIM_JH_FLUX_2584_CLOSURE_DERIVATION_AUDIT.csv",
    "obstruction_vector": OUT / "P8_Y5_PIM_JH_FLUX_2584_EXACT_OBSTRUCTION_VECTOR.csv",
    "surface_test": OUT / "P8_Y5_PIM_JH_FLUX_2584_COMPACT_EXTERIOR_SURFACE_TEST.csv",
    "runner_refusal": OUT / "P8_Y5_PIM_JH_FLUX_2584_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_PIM_JH_FLUX_2584_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PIM_JH_FLUX_2584_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PIM_JH_FLUX_2584_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PIM_JH_FLUX_2584_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2584_VALIDATION.csv",
}

COPY_TARGETS = {
    "closure_audit": QUEUE / "JR2584_PIM_JH_FLUX_CLOSURE_AUDIT_NONCLAIM.csv",
    "obstruction_vector": LOCAL_BOUNDS / "PiM_JH_flux_obstruction_vector_2584_NONCLAIM.csv",
    "surface_test": LOCAL_BOUNDS / "PiM_JH_compact_exterior_surface_test_2584_NONCLAIM.csv",
    "next_target": QUEUE / "JR2584_PIM_CHAINMAP_COMMUTATOR_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2584_00_2583_handoff",
            "source_path": ROOT / "2583-Y5-R2FR-Y5-source-normalization-owner-or-q_loc-R11-bound-implementation.md",
            "needles": ["NEXT2583_0_selected", "Y5O2583_3_flux_closure", "VAL2583_OVERALL"],
            "role": "active handoff selecting PiM JH flux closure as the next root target",
        },
        {
            "source_id": "SRC2584_01_1013_prior_flux",
            "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            "needles": ["PFC1013_8_verdict", "OBS1013_0_projected_extra_current", "OBS1013_1_PiM_commutator"],
            "role": "prior exact obstruction vector and compact-exterior closure failure",
        },
        {
            "source_id": "SRC2584_02_flux_contract",
            "source_path": OUT / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "needles": ["FC2_closed_mass_current_equation", "FC8_retained_residual_fallback"],
            "role": "Ward/topological mass-flux closure contract",
        },
        {
            "source_id": "SRC2584_03_2578_hamiltonian",
            "source_path": ROOT / "2578-Y5-R2FR-PiM-Hamiltonian-coupling-identity-or-source-backed-residual-fill.md",
            "needles": ["CPS2578_2_PiM_Hamiltonian_identity", "RES2578_0_PiM_H", "VAL2578_OVERALL"],
            "role": "Hamiltonian PiM identity and coupling-baseline transfer ledger",
        },
        {
            "source_id": "SRC2584_04_2577_selector",
            "source_path": ROOT / "2577-Y5-R2FR-worldtube-Hilbert-source-selector-coupling-and-zero-boundary-flux-or-R-eq-fill.md",
            "needles": ["R_eq=0", "I_commutator=0", "VAL2577_OVERALL"],
            "role": "worldtube-Hilbert selector and zero boundary flux route",
        },
        {
            "source_id": "SRC2584_05_2579_descent",
            "source_path": ROOT / "2579-Y5-R2FR-EH-fixed-point-descent-coupling-PiM-lock-or-double-zero-residuals.md",
            "needles": ["EH_DESCENT_COUPLING_PIM_PACKAGE_NOT_DERIVED_CURRENT_CORPUS", "PiM lock", "VAL2579_OVERALL"],
            "role": "EH descent, PiM lock and extra-sector double-zero blocker",
        },
        {
            "source_id": "SRC2584_06_nonhilbert_residual",
            "source_path": LOCAL_BOUNDS / "NonHilbert_residual_row_2538_NONCLAIM.csv",
            "needles": ["valid_for_claim", "false"],
            "role": "non-Hilbert residual rows remain nonclaim",
        },
        {
            "source_id": "SRC2584_07_hilbert_source_norm",
            "source_path": LOCAL_BOUNDS / "Hilbert_worldtube_source_normalization_2568_THEOREM_NONCLAIM.csv",
            "needles": ["THM2568_6_zero_certificate_verdict", "valid_for_claim"],
            "role": "Hilbert worldtube source-normalization theorem clauses",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                }
            )
        )
    return rows


def closure_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "FCA2584_0_same_frame_Hilbert_current",
            "required_clause": "J_H is the same-frame Hilbert mass current",
            "mathematical_form": "J_H = delta S_matter / delta e_obs, with e_obs also used by clocks, rods and orbital readout",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "missing_input": "parent matter action descent plus observed coframe/source-frame lock",
            "effect_if_missing": "the closed current can be a formal object rather than the measured source mass",
            "proof_role": "defines the object whose flux is meant to become measured GM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_1_total_Ward_identity",
            "required_clause": "parent total source current has a Ward/Euler identity",
            "mathematical_form": "d(J_H + J_extra) = A_parent",
            "current_status": "STRUCTURE_AVAILABLE_NOT_PARENT_SIGNED_FOR_MTS",
            "missing_input": "explicit parent Euler/Ward current split for the current local branch",
            "effect_if_missing": "dJ_H cannot be replaced by -dJ_extra + A_parent without importing GR machinery",
            "proof_role": "turns the flux problem into a controlled obstruction equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_2_product_identity",
            "required_clause": "projected current obeys exact product decomposition",
            "mathematical_form": "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "current_status": "FORMAL_IDENTITY_ADOPTED_AS_OBSTRUCTION_DEFINITION",
            "missing_input": "zero or bound for every term on the right-hand side",
            "effect_if_missing": "the identity is useful bookkeeping, not a closure proof",
            "proof_role": "defines the measured-GM leakage vector exactly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_3_extra_projection_zero",
            "required_clause": "extra parent sectors are killed by Pi_M in the compact exterior",
            "mathematical_form": "Pi_M dJ_extra = 0 for nonEH, memory, boundary, domain, frame, species and coupling sectors",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_input": "extra-sector double zeros and PiM annihilator theorem",
            "effect_if_missing": "unobserved sectors leak into measured source normalization",
            "proof_role": "removes the first exact obstruction term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_4_chainmap_commutator_zero",
            "required_clause": "Pi_M is a fixed parent chain map before readout",
            "mathematical_form": "[d,Pi_M]J_H = 0 on compact exterior domains",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_input": "fixed topology/source selector, no moving mask, no readout-dependent projector variation",
            "effect_if_missing": "radial source hair and PPN/R11 source-normalization terms remain live",
            "proof_role": "removes the direct product-rule obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_5_parent_anomaly_silence",
            "required_clause": "parent anomaly, corner and symplectic boundary terms vanish or are fixed",
            "mathematical_form": "A_parent = 0 after fixed reference subtraction and compact-boundary no-flux",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_input": "boundary/reference/no-corner theorem in the same local branch",
            "effect_if_missing": "boundary bookkeeping can mimic a source mass shift",
            "proof_role": "removes the final exact obstruction term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_6_worldtube_surface_independence",
            "required_clause": "linked exterior surfaces measure the same charge",
            "mathematical_form": "int_S2 Pi_M J_H - int_S1 Pi_M J_H = int_A d(Pi_M J_H) = 0",
            "current_status": "CONDITIONAL_ON_FCA2584_3_TO_FCA2584_5",
            "missing_input": "compact annulus support and all obstruction zeros",
            "effect_if_missing": "Meff can depend on radius, time or chosen readout surface",
            "proof_role": "turns local flux closure into a conserved measured mass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_7_fixed_calibration",
            "required_clause": "closed surface charge is calibrated to measured Newtonian GM by parent constants",
            "mathematical_form": "M_eff = (4*pi*G_ref)^-1 int_S Pi_M J_H with G_ref, kappa_MTS and ell_J fixed before readout",
            "current_status": "COUPLING_BASELINE_NOT_DERIVED",
            "missing_input": "fixed kappa_MTS/G_ref/ell_J package and no reference absorption",
            "effect_if_missing": "one can close the wrong mass or hide a fitted GM scale",
            "proof_role": "connects flux closure to Newton/GR source normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FCA2584_8_verdict",
            "required_clause": "compact-exterior PiM JH flux closure",
            "mathematical_form": "d(Pi_M J_H)=0 and M_eff is the fixed measured-GM source",
            "current_status": "PIM_JH_FLUX_CLOSURE_NOT_DERIVED_CURRENT_CORPUS",
            "missing_input": "FCA2584_0 through FCA2584_7 must all be parent-signed",
            "effect_if_missing": "Newton/local-GR/source-normalization gates remain blocked",
            "proof_role": "2584 verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def obstruction_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "obstruction_id": "OBS2584_0_projected_extra_current",
            "symbol": "-Pi_M dJ_extra",
            "definition": "projected non-Hilbert, memory, domain, boundary, coupling, frame and species exchange current",
            "zero_or_bound_needed": "Pi_M dJ_extra = 0 or a source-backed component vector below arena bounds",
            "current_status": "MISSING_EXTRA_PROJECTION_ZERO_OR_NUMERIC_VECTOR",
            "units": "GM_flux_or_dimensionless_after_Meff_normalization",
            "affected_rows": "Newton;PPN;R10;R11;WEP;clock;orbital",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS2584_1_PiM_chainmap_commutator",
            "symbol": "[d,Pi_M]J_H",
            "definition": "failure of the mass projector to commute with exterior differentiation on the local compact exterior",
            "zero_or_bound_needed": "[d,Pi_M]J_H = 0 by fixed parent chain map, or I_commutator coefficient rows",
            "current_status": "MISSING_CHAINMAP_ZERO_OR_I_COMMUTATOR_BOUND",
            "units": "GM_flux_or_dimensionless_after_Meff_normalization",
            "affected_rows": "radial_Meff_hair;gamma_minus_1;beta_minus_1;alpha(lambda);R11",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS2584_2_parent_anomaly_boundary",
            "symbol": "A_parent",
            "definition": "parent anomaly, symplectic flux, corner term, reference subtraction, or compact-boundary current",
            "zero_or_bound_needed": "A_parent = 0 in the same local branch with fixed reference subtraction",
            "current_status": "MISSING_PARENT_BOUNDARY_ANOMALY_SILENCE",
            "units": "GM_flux",
            "affected_rows": "Newton;PPN;clock;orbital;local_GR",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS2584_3_topological_equality_residual",
            "symbol": "R_eq",
            "definition": "difference between projected Hilbert current and owned topological mass current plus exact boundary primitive",
            "zero_or_bound_needed": "R_eq = Pi_M J_H - J_M_top - dB_zero = 0 or bounded",
            "current_status": "MISSING_TOPOLOGICAL_HILBERT_EQUALITY",
            "units": "dimensionless_or_GM_flux",
            "affected_rows": "R4;R9;R11;Newton",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS2584_4_zero_boundary_flux",
            "symbol": "B_zero_flux",
            "definition": "compact boundary flux of the exact primitive/reference subtraction used in the source-current equality",
            "zero_or_bound_needed": "int_boundary dB_zero = 0 with no hidden GM absorption",
            "current_status": "MISSING_ZERO_BOUNDARY_FLUX_THEOREM",
            "units": "GM_flux_or_dimensionless",
            "affected_rows": "R10;R11;PPN;orbital",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS2584_5_coupling_baseline",
            "symbol": "delta_kappa + delta_ellJ + epsilon_Gref_match",
            "definition": "coupling, source-current scale, and reference-G mismatch between parent charge and measured GM",
            "zero_or_bound_needed": "d kappa_MTS = 0, d ell_J = 0, and G_ref is induced before readout",
            "current_status": "COUPLING_BASELINE_NOT_PARENT_SIGNED",
            "units": "dimensionless_or_GM_scale_fraction",
            "affected_rows": "Gdot;source_charge;orbital;PPN;local_GR",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS2584_6_surface_flux_leak",
            "symbol": "epsilon_flux(A)",
            "definition": "finite-annulus measured-mass leakage normalized by M_eff",
            "zero_or_bound_needed": "epsilon_flux(A)=M_eff^-1 int_A d(Pi_M J_H)=0 or an arena-specific bound profile",
            "current_status": "DERIVED_AS_BOOKKEEPING_NOT_NUMERICALLY_FILLED",
            "units": "dimensionless_or_yr^-1_or_inverse_length",
            "affected_rows": "dln_Geff_dt;partial_r_ln_mu_obs;alpha(lambda);gamma_minus_1;beta_minus_1",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS2584_TOTAL",
            "symbol": "Omega_GM",
            "definition": "total measured-GM flux obstruction",
            "zero_or_bound_needed": "Omega_GM = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent = 0, plus R_eq/B_zero/coupling calibration tails",
            "current_status": "TOTAL_OBSTRUCTION_RETAINED_NONCLAIM",
            "units": "GM_flux_or_dimensionless_after_Meff_normalization",
            "affected_rows": "Y5;Newton;PPN;R10;R11;clock;orbital;local_GR",
            "source_path": "THIS_CHECKPOINT_SYMBOLIC_DECOMPOSITION_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def surface_test_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "test_id": "ST2584_0_annulus_identity",
            "test": "linked compact exterior surfaces",
            "mathematical_check": "Delta M_eff(S1,S2)=C_G int_A d(Pi_M J_H)",
            "current_result": "EXACT_FORMULA_INSTALLED_NONCLAIM",
            "missing_for_pass": "Omega_GM zero theorem or numeric annulus profile",
            "observable_link": "radial_Meff_hair;orbital_Meff;R10_alpha_lambda",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "test_id": "ST2584_1_time_tube_identity",
            "test": "stationary time tube source conservation",
            "mathematical_check": "dM_eff/dt=C_G int_Cyl d(Pi_M J_H)",
            "current_result": "EXACT_FORMULA_INSTALLED_NONCLAIM",
            "missing_for_pass": "stationary parent Hamiltonian generator plus zero flux",
            "observable_link": "Gdot_over_G;clock_source_residual",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "test_id": "ST2584_2_projector_chainmap_probe",
            "test": "Pi_M fixed-before-readout chain-map test",
            "mathematical_check": "I_commutator(A)=int_A [d,Pi_M]J_H",
            "current_result": "FIRST_TARGET_NOT_FILLED",
            "missing_for_pass": "parent fixed-chainmap proof or coefficient rows with units",
            "observable_link": "R11_source_normalization;PPN_gamma_beta;R10",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "test_id": "ST2584_3_extra_projection_probe",
            "test": "extra-sector annihilator test",
            "mathematical_check": "E_extra(A)=int_A Pi_M dJ_extra",
            "current_result": "NOT_FILLED",
            "missing_for_pass": "extra double-zero and PiM annihilator theorem",
            "observable_link": "WEP;PPN;clock;local_GR",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "test_id": "ST2584_4_calibration_probe",
            "test": "closed charge to measured GM",
            "mathematical_check": "M_eff=(4*pi*G_ref)^-1 int_S Pi_M J_H with fixed kappa_MTS and ell_J",
            "current_result": "COUPLING_BASELINE_BLOCKED",
            "missing_for_pass": "fixed G_ref/kappa/ell_J and no reference absorption",
            "observable_link": "Newton;orbital;PPN;local_GR",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def runner_refusal_rows(obstructions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for obstruction in obstructions:
        if obstruction["obstruction_id"] == "OBS2584_TOTAL":
            continue
        failure_reasons = [
            "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "MISSING_SOURCE_PATH",
            "VALID_FOR_CLAIM_FALSE",
        ]
        rows.append(
            with_stamp(
                {
                    "runner_id": f"OBR2584_{obstruction['obstruction_id']}",
                    "obstruction_id": obstruction["obstruction_id"],
                    "symbol": obstruction["symbol"],
                    "verdict": "REFUSED_CLAIM_RETAINED_UNFILLED",
                    "failure_reasons": failure_reasons,
                    "score_ready": False,
                    "claim_allowed": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2584_0_flux_closure",
            "claim": "d(Pi_M J_H)=0 compact-exterior closure is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "extra projection, chainmap commutator, parent anomaly, worldtube glue and calibration are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2584_1_obstruction_score",
            "claim": "measured-GM obstruction vector is score-ready",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "obstruction terms are exact symbols but no numeric/source-backed coefficients exist",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2584_2_chainmap",
            "claim": "[d,Pi_M]J_H is zero or bounded",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Pi_M fixed-chainmap theorem and I_commutator bound rows are missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2584_3_source_normalization",
            "claim": "Y5 measured-GM/source-normalization owner theorem reopens",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Omega_GM remains retained and coupling baseline remains unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2584_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is claimable",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "compact-exterior measured source mass is not parent-owned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2584_5_guardrail",
            "claim": "flux proof-or-score guardrail is installed",
            "gate_status": "PASS_NONCLAIM",
            "reason": "exact leakage terms are exposed and cannot be hidden inside fitted GM",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2584_0_closure_not_proved",
            "decision": "PIM_JH_FLUX_CLOSURE_NOT_PROVED",
            "reason": "the exact product/Ward obstruction exists, but no term on the right-hand side is parent-signed zero or source-backed bounded",
            "effect": "no Newton, source-normalization, H_tau/M_H_ref or local-GR claim",
        },
        {
            "decision_id": "DEC2584_1_exact_object_gained",
            "decision": "OMEGA_GM_IS_THE_NEXT_MEASURED_SOURCE_OBJECT",
            "reason": "Delta M_eff between linked surfaces is controlled by Omega_GM, not by a vague source-normalization phrase",
            "effect": "future tests can score finite leakage honestly if the proof route fails",
        },
        {
            "decision_id": "DEC2584_2_best_next_target",
            "decision": "PIM_CHAINMAP_COMMUTATOR_SELECTED_NEXT",
            "reason": "[d,Pi_M]J_H is the narrowest direct product-rule obstruction and can be attacked without solving every extra sector at once",
            "effect": "2585 should prove fixed chain-map zero or fill I_commutator coefficient/bound rows",
        },
    ]
    return [with_stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2584_0_selected",
            "selection_status": "selected",
            "target_file": "2585-Y5-R2FR-PiM-chainmap-commutator-zero-or-Icommutator-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_PiM_chainmap_commutator_zero_or_Icommutator_bound_fill_2585.py",
            "task": "prove Pi_M is a parent-owned fixed chain map on compact exterior domains so [d,Pi_M]J_H=0, or fill I_commutator coefficient/bound rows with units, source paths, and arena projections",
            "acceptance_target": "either a parent-signed chainmap theorem removes OBS2584_1, or I_commutator becomes the first source-backed measured-GM obstruction row",
            "guardrails": "no post-readout mass projector; no fitted GM absorption; no topological-current shortcut unless it equals Pi_M J_H; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id if copy_id != "next_target" else "next_target"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2584_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add(
        "VAL2584_00_sources_exist",
        all(row["source_pass"] is True for row in data["sources"]),
        "all cited local source paths exist and required needles are present",
    )
    add(
        "VAL2584_01_closure_blocked",
        any(row["audit_id"] == "FCA2584_8_verdict" and row["valid_for_claim"] is False for row in data["closure_audit"]),
        "PiM JH compact-exterior closure remains blocked",
    )
    add(
        "VAL2584_02_exact_obstruction_vector",
        all(
            symbol in {row["symbol"] for row in data["obstructions"]}
            for symbol in ("-Pi_M dJ_extra", "[d,Pi_M]J_H", "A_parent", "Omega_GM")
        ),
        "exact measured-GM obstruction vector contains product/Ward terms",
    )
    add(
        "VAL2584_03_obstructions_nonclaim",
        all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["obstructions"]),
        "all obstruction rows remain retained nonclaim",
    )
    add(
        "VAL2584_04_surface_tests_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["surface_tests"]),
        "compact-exterior surface tests are formulae, not claims",
    )
    add(
        "VAL2584_05_runner_refuses",
        all(row["claim_allowed"] is False and row["score_ready"] is False for row in data["runner_refusal"]),
        "runner refuses unfilled obstruction rows",
    )
    add(
        "VAL2584_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no flux, source-normalization, Newton or local-GR claim is allowed",
    )
    add(
        "VAL2584_07_next_target_written",
        any(row["route_id"] == "NEXT2584_0_selected" for row in data["next"]),
        "2585 PiM chainmap commutator target selected",
    )
    add(
        "VAL2584_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2584-Y5-R2FR-PiM-JH-flux*",
            "*Y5_R2FR_PiM_JH_flux_closure*",
            "*P8_Y5_PIM_JH_FLUX_2584*",
            "*JR2584*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2584_09_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2584 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2584_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2584_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2584_OVERALL",
        overall,
        "2584 reduces measured-GM flux closure to Omega_GM, keeps all claims blocked, and selects PiM chainmap commutator next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2584 Y5 R2FR PiM JH flux closure or measured-GM obstruction score",
        "",
        "**Status:** private nonclaim derivation checkpoint. Compact-exterior closure of `d(Pi_M J_H)=0` is not derived.",
        "",
        "**Main result:** the honest object is now the exact measured-GM flux obstruction `Omega_GM = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent`, with `R_eq`, `B_zero_flux`, and coupling-baseline tails kept explicit. This is progress because the source-normalization problem is no longer fog: it is a concrete leakage vector. It is not yet a Newton/local-GR proof because no obstruction term is parent-signed zero or source-backed bounded.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Closure Derivation Audit",
        markdown_table(data["closure_audit"], ["audit_id", "required_clause", "mathematical_form", "current_status", "missing_input", "effect_if_missing", "proof_role", "valid_for_claim", "claim_allowed"]),
        "",
        "## Exact Obstruction Vector",
        markdown_table(data["obstructions"], ["obstruction_id", "symbol", "definition", "zero_or_bound_needed", "current_status", "units", "affected_rows", "source_path", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Compact Exterior Surface Test",
        markdown_table(data["surface_tests"], ["test_id", "test", "mathematical_check", "current_result", "missing_for_pass", "observable_link", "score_ready", "valid_for_claim"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "obstruction_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    obstructions = obstruction_vector_rows()
    data = {
        "sources": source_register_rows(),
        "closure_audit": closure_audit_rows(),
        "obstructions": obstructions,
        "surface_tests": surface_test_rows(),
        "runner_refusal": runner_refusal_rows(obstructions),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["closure_audit"], data["closure_audit"])
    write_csv(OUTPUTS["obstruction_vector"], data["obstructions"])
    write_csv(OUTPUTS["surface_test"], data["surface_tests"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2584_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
