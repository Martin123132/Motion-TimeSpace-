from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1944"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1944-Y5-R2FR-R11-weak-field-potential-equations-or-coefficient-placeholder-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1939_doc": ROOT / "1939-Y5-R2FR-parent-gravity-operator-EH-or-R11-residual-Newtonian-law.md",
    "1939_r11": OUT / "P8_Y5_PARENT_QLOC_1939_R11_RESIDUAL_NEWTONIAN_LAW.csv",
    "1940_doc": ROOT / "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md",
    "1940_r11": OUT / "P8_Y5_PARENT_QLOC_1940_R11_RESIDUAL_OPERATOR_LEDGER.csv",
    "1941_ppn": OUT / "P8_Y5_PARENT_QLOC_1941_PPN_R11_RESIDUAL_VECTOR.csv",
    "1942_equations": OUT / "P8_Y5_PARENT_QLOC_1942_PPN_R11_EQUATION_MAP.csv",
    "1943_doc": ROOT / "1943-Y5-R2FR-delta-gamma-R11-weak-field-solve-or-Cassini-bound-runner.md",
    "1943_validation": OUT / "P8_Y5_BRR545_1943_VALIDATION.csv",
    "1943_runner": OUT / "P8_Y5_PARENT_QLOC_1943_CASSINI_GAMMA_BOUND_RUNNER.csv",
}

NEEDLES = {
    "1939_doc": ["GAC1939_2_field_equation", "R111939_0_field_equation", "R111939_2_Newtonian_projection"],
    "1939_r11": ["R111939_0_field_equation", "R111939_2_Newtonian_projection"],
    "1940_doc": ["R111940_5_ppn_residual", "LOV1940_3_second_order", "VAL1940_OVERALL"],
    "1940_r11": ["R111940_1_higher_derivative_curvature", "R111940_5_ppn_residual"],
    "1941_ppn": ["PPN1941_1_gamma_residual", "PPN1941_0_newtonian_residual"],
    "1942_equations": ["EQ1942_1_gamma", "delta_gamma"],
    "1943_doc": ["DG1943_2_delta_gamma_exact", "MISS1943_1_Phi_R11", "NEXT1943_0_primary", "VAL1943_OVERALL"],
    "1943_validation": ["VAL1943_OVERALL", "PASS"],
    "1943_runner": ["RUN1943_0_cassini_schema", "MISSING_NUMERIC_R11_POTENTIALS"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1944_SOURCE_REGISTER.csv",
    "weak_field_derivation": OUT / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv",
    "coefficient_ledger": OUT / "P8_Y5_PARENT_QLOC_1944_R11_PROJECTION_COEFFICIENT_LEDGER.csv",
    "cassini_slip_control": OUT / "P8_Y5_PARENT_QLOC_1944_CASSINI_SLIP_CONTROL_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1944_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1944_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1944_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1944_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1944_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_potential_derivation": SOURCE_WEIGHT_DOCS / "R11_WEAK_FIELD_POTENTIAL_DERIVATION_1944_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1944_CLAIM_GATE_NONCLAIM.csv",
    "cassini_slip_queue": QUEUE / "JR1944_R11_TF_SLIP_ZERO_OR_BOUND_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1944_CLAIM_GATE.csv",
}


def flag(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needles(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = read_text(path)
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in SOURCES.items():
        needles = NEEDLES[source_id]
        ok = has_needles(path, needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": str(path),
                "purpose": "1944 R11 weak-field potential equation reduction",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_SOURCE_OR_NEEDLE",
                "issue": "" if ok else "source path missing or required needles absent",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def weak_field_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_0_field_subtraction",
            "step": "Subtract the GR/EH weak-field branch from the retained residual field equation.",
            "symbolic_statement": "delta G_mn + kappa_R R11_mn^(1) = 0",
            "result": "RESIDUAL_FIELD_EQUATION_DERIVED_SYMBOLIC",
            "assumptions_or_missing_inputs": "same ordinary matter source; weak static local frame; Lambda locally negligible; R11 linearization exists",
            "cassini_relevance": "turns the problem from vague R11 into equations for residual metric potentials",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_1_metric_potential_split",
            "step": "Use the 1943 potential split.",
            "symbolic_statement": "Phi=U+Phi_R11; Psi=U+Psi_R11; gamma_R11=(U+Psi_R11)/(U+Phi_R11)",
            "result": "POTENTIAL_SPLIT_READY",
            "assumptions_or_missing_inputs": "observed-frame weak-field gauge and denominator regularity still need source locking",
            "cassini_relevance": "Cassini gamma is controlled by the difference between spatial and time potentials",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_2_scalar_00_projection",
            "step": "Project the residual equation onto the scalar time-time sector.",
            "symbolic_statement": "C00_Phi nabla^2 Phi_R11 + C00_Psi nabla^2 Psi_R11 = -kappa_R P00[R11]",
            "result": "SCALAR_COMMON_MODE_EQUATION_WITH_COEFFICIENT_SLOTS",
            "assumptions_or_missing_inputs": "C00_Phi,C00_Psi,P00[R11],kappa_R are not parent-sourced",
            "cassini_relevance": "controls common Newtonian/effective-G residuals more directly than gamma slip",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_3_traceless_spatial_projection",
            "step": "Project the residual equation onto the traceless spatial sector.",
            "symbolic_statement": "C_TF nabla^2(Psi_R11-Phi_R11) = -kappa_R P_TF[R11_ij]",
            "result": "ANISOTROPIC_SLIP_EQUATION_WITH_COEFFICIENT_SLOTS",
            "assumptions_or_missing_inputs": "C_TF and P_TF[R11_ij] must be derived from the parent R11 operator",
            "cassini_relevance": "this is the clean object Cassini gamma constrains",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_4_potential_solution_form",
            "step": "Invert the local Poisson/slip operator symbolically.",
            "symbolic_statement": "Psi_R11-Phi_R11 = -(kappa_R/C_TF) nabla^{-2} P_TF[R11_ij]",
            "result": "FORMAL_SLIP_SOLUTION_DERIVED",
            "assumptions_or_missing_inputs": "boundary condition and inverse-Laplacian domain not fixed",
            "cassini_relevance": "turns gamma into a source/projection bound rather than a free parameter",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_5_delta_gamma_source_law",
            "step": "Insert the slip solution into the 1943 linear delta-gamma expression.",
            "symbolic_statement": "delta_gamma_R11 ~= -(kappa_R/(C_TF U)) nabla^{-2} P_TF[R11_ij]",
            "result": "DELTA_GAMMA_SOURCE_LAW_SYMBOLIC",
            "assumptions_or_missing_inputs": "small-residual proof and U normalization missing",
            "cassini_relevance": "Cassini can be tested once P_TF[R11_ij], C_TF, kappa_R and U are supplied",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_6_common_mode_separation",
            "step": "Separate gamma slip from common potential renormalization.",
            "symbolic_statement": "If Phi_R11=Psi_R11 then delta_gamma_R11=0, while Xi_N/common-mode tests remain active.",
            "result": "CASSINI_COMMON_MODE_NOT_ENOUGH",
            "assumptions_or_missing_inputs": "common mode still needs inverse-square/ephemeris control",
            "cassini_relevance": "a nonzero R11 branch can evade gamma only if it is locally slip-free",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "WFE1944_7_local_zero_route",
            "step": "State the sharp theorem target for local GR recovery.",
            "symbolic_statement": "P_TF[R11_ij]=0 in the local vacuum/isotropic branch => Psi_R11-Phi_R11=0 => delta_gamma_R11=0",
            "result": "BEST_ZERO_PROOF_TARGET_IDENTIFIED",
            "assumptions_or_missing_inputs": "must be parent-derived from local geometry/descent, not inserted as a plateau axiom",
            "cassini_relevance": "this is the least ad-hoc route to a Cassini-safe local branch",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def coefficient_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_0_kappa_R",
            "symbol": "kappa_R",
            "definition": "coupling of the retained R11 residual tensor to the observed metric equation",
            "needed_for": "normalizes Phi_R11, Psi_R11 and delta_gamma_R11",
            "status": "MISSING_PARENT_COUPLING_NORMALIZATION",
            "source_path": str(SOURCES["1939_doc"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_1_P00",
            "symbol": "P00[R11]",
            "definition": "time-time scalar projection of the linearized R11 residual",
            "needed_for": "common Newtonian/effective-G residual equation",
            "status": "MISSING_R11_00_OPERATOR",
            "source_path": str(SOURCES["1939_r11"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_2_PTF",
            "symbol": "P_TF[R11_ij]",
            "definition": "traceless spatial projection of the linearized R11 residual",
            "needed_for": "anisotropic slip and Cassini gamma residual",
            "status": "MISSING_R11_TF_OPERATOR",
            "source_path": str(SOURCES["1940_r11"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_3_C00",
            "symbol": "C00_Phi,C00_Psi",
            "definition": "weak-field gauge coefficients multiplying scalar Laplacians in the 00 residual equation",
            "needed_for": "translate R11_00 into Phi_R11/Psi_R11 common mode",
            "status": "MISSING_WEAK_FIELD_CONVENTION_LOCK",
            "source_path": str(SOURCES["1943_doc"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_4_CTF",
            "symbol": "C_TF",
            "definition": "weak-field coefficient multiplying nabla^2(Psi_R11-Phi_R11) in the traceless spatial equation",
            "needed_for": "convert P_TF[R11_ij] into delta_gamma_R11",
            "status": "MISSING_TF_NORMALIZATION",
            "source_path": str(SOURCES["1943_doc"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_5_inverse_laplacian",
            "symbol": "nabla^{-2}",
            "definition": "boundary-conditioned inverse Laplacian for local solar-system weak-field residuals",
            "needed_for": "turn projected R11 source into an actual slip amplitude",
            "status": "MISSING_LOCAL_BOUNDARY_CONDITION",
            "source_path": str(SOURCES["1943_doc"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_6_small_residual",
            "symbol": "epsilon_R11=max(|Phi_R11|,|Psi_R11|)/|U|",
            "definition": "smallness parameter required for the linear delta-gamma approximation",
            "needed_for": "controlled comparison to Cassini gamma",
            "status": "MISSING_SMALL_RESIDUAL_PROOF",
            "source_path": str(SOURCES["1943_runner"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "COEF1944_7_U_frame",
            "symbol": "U_solar_frame",
            "definition": "observed solar-system Newtonian potential normalization used in the Cassini comparison",
            "needed_for": "dimensionless delta_gamma_R11 source law",
            "status": "MISSING_OBSERVED_FRAME_NORMALIZATION",
            "source_path": str(SOURCES["1942_equations"]),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def cassini_slip_control_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "control_id": "SLIP1944_0_cassini_controls_slip",
            "object": "Psi_R11-Phi_R11",
            "statement": "Cassini gamma constrains the anisotropic spatial/time potential difference, not every R11 residual equally.",
            "status": "DERIVED_SYMBOLIC_NONCLAIM",
            "implication": "focus on P_TF[R11_ij] before trying to numerically fit broad R11 families",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "control_id": "SLIP1944_1_common_mode_separate",
            "object": "Phi_R11=Psi_R11 common mode",
            "statement": "A common residual potential can renormalize Newtonian gravity without directly producing gamma slip.",
            "status": "USEFUL_SEPARATION_NONCLAIM",
            "implication": "common mode belongs to Xi_N/ephemeris/inverse-square gates, not the first Cassini gamma gate",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "control_id": "SLIP1944_2_zero_theorem_target",
            "object": "P_TF[R11_ij]",
            "statement": "If the parent local vacuum branch forces P_TF[R11_ij]=0, then delta_gamma_R11 is theorem-zero at this order.",
            "status": "BEST_ZERO_PROOF_TARGET",
            "implication": "prove local isotropy/vacuum/descent kills the traceless spatial projection",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "control_id": "SLIP1944_3_bound_route",
            "object": "nabla^{-2} P_TF[R11_ij]",
            "statement": "If the traceless projection is nonzero, the Cassini route needs a sourced bound on its inverse-Laplacian amplitude.",
            "status": "BOUND_ROUTE_READY_INPUTS_MISSING",
            "implication": "derive or source kappa_R, C_TF, local boundary conditions and the projected source amplitude",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "control_id": "SLIP1944_4_no_pass_yet",
            "object": "Cassini/local-GR claim",
            "statement": "The reduction is sharper, but no numeric or theorem-zero R11 slip result exists yet.",
            "status": "CLAIM_BLOCKED",
            "implication": "do not call this a Cassini pass; call it the narrowed target",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1944_0_symbolic_field_split",
            "claim": "R11 weak-field residuals can be written as scalar/common and traceless-spatial/slip equations.",
            "status": "PASS_NONCLAIM",
            "reason": "symbolic projection ledger created with missing coefficient slots explicit",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1944_1_slip_controls_gamma",
            "claim": "Cassini gamma primarily constrains Psi_R11-Phi_R11 / anisotropic slip.",
            "status": "PASS_NONCLAIM",
            "reason": "follows from 1943 delta_gamma expression and weak-field potential split",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1944_2_numeric_coefficients",
            "claim": "All R11 weak-field coefficients are parent-sourced numeric inputs.",
            "status": "FAIL_BLOCKED",
            "reason": "kappa_R, C_TF, P_TF, boundary and smallness inputs remain missing",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1944_3_R11_TF_zero",
            "claim": "P_TF[R11_ij]=0 in the local solar-system branch.",
            "status": "FAIL_BLOCKED",
            "reason": "zero theorem identified but not derived from parent local geometry",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1944_4_Cassini_gamma_pass",
            "claim": "MTS passes the Cassini gamma bound.",
            "status": "FAIL_BLOCKED",
            "reason": "no theorem-zero or numeric bounded delta_gamma_R11 prediction exists",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1944_5_local_GR_PPN",
            "claim": "MTS derives local GR/PPN.",
            "status": "FAIL_BLOCKED",
            "reason": "gamma is only one residual; beta, preferred-frame, Newtonian and conservation residuals remain open",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1944_6_public_claim",
            "claim": "1944 is a public-ready local-GR proof.",
            "status": "FAIL_BLOCKED",
            "reason": "private derivation checkpoint and coefficient ledger only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1944_0_status",
            "decision": "R11_WEAK_FIELD_REDUCED_TO_COMMON_MODE_AND_ANISOTROPIC_SLIP",
            "reason": "delta_gamma depends on Psi_R11-Phi_R11, which is sourced by the traceless spatial projection of R11",
            "next_action": "stop treating all R11 residuals as equally fatal; attack P_TF[R11_ij] first",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1944_1_best_route",
            "decision": "PROVE_LOCAL_TF_R11_ZERO_OR_BOUND_ITS_SLIP",
            "reason": "a local isotropic/vacuum theorem could set gamma residual to zero without requiring every common-mode correction to vanish",
            "next_action": "derive P_TF[R11_ij]=0 from parent local geometry/descent, or create a Cassini slip bound input ledger",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1944_2_not_circling",
            "decision": "TARGET_NARROWED_FROM_R11_GENERALITY_TO_ONE_PROJECTION",
            "reason": "the project now knows exactly which R11 component Cassini gamma punishes first",
            "next_action": "1945 should be a proof attempt on the traceless spatial residual, not another broad audit",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT1944_0_primary",
            "priority": "selected",
            "target_doc": "1945-Y5-R2FR-R11-traceless-spatial-zero-proof-or-Cassini-slip-bound.md",
            "target_script": "scripts/Y5_R2FR_R11_traceless_spatial_zero_or_Cassini_slip_bound_1945.py",
            "objective": "derive P_TF[R11_ij]=0 for the local vacuum/isotropic branch, or build a sourced Cassini slip bound ledger with claim=false",
            "acceptance_output": "parent-signed zero theorem for the traceless spatial projection, or explicit missing inputs kappa_R/C_TF/P_TF/boundary with Cassini still blocked",
            "nonclaim_rule": "do not claim Cassini/local GR pass unless P_TF is theorem-zero or its inverse-Laplacian amplitude is sourced below the Cassini bound",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1944_0_project_position",
            "status": "CASSINI_GAMMA_REDUCED_TO_R11_TRACELESS_SPATIAL_SLIP_TARGET",
            "strongest_result": "delta_gamma_R11 ~= -(kappa_R/(C_TF U)) nabla^{-2} P_TF[R11_ij], with all coefficient/source slots explicit",
            "what_improved": "the local-GR blocker is no longer vague; the first sharp object is the traceless spatial R11 projection",
            "still_missing": "parent-derived P_TF zero theorem or sourced coefficient/bound inputs",
            "claim_status": "Cassini/local-GR public claims remain blocked",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_potential_derivation"], rows_by_name["weak_field_derivation"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["cassini_slip_queue"], rows_by_name["next_target"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_has_rows(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle))) > 0


def formalization_1944_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for _ in FORMALIZATION.rglob("*1944*"))


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, str]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": flag(False),
        "claim_allowed": flag(False),
    }


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    rows.append(validation_row("VAL1944_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found" if sources_ok else "source path or needle missing"))

    derivation_text = "\n".join(row["result"] + " " + row["symbolic_statement"] for row in rows_by_name["weak_field_derivation"])
    derivation_ok = "ANISOTROPIC_SLIP_EQUATION_WITH_COEFFICIENT_SLOTS" in derivation_text and "DELTA_GAMMA_SOURCE_LAW_SYMBOLIC" in derivation_text
    rows.append(validation_row("VAL1944_01_derivation", "PASS" if derivation_ok else "FAIL", "weak-field potential and delta-gamma source laws recorded"))

    coeff_ok = all(row["status"].startswith("MISSING_") and row["valid_for_claim"] == flag(False) for row in rows_by_name["coefficient_ledger"])
    rows.append(validation_row("VAL1944_02_coefficients_blocked", "PASS" if coeff_ok else "FAIL", "all coefficient rows remain missing/nonclaim"))

    slip_text = "\n".join(row["status"] + " " + row["statement"] for row in rows_by_name["cassini_slip_control"])
    slip_ok = "BEST_ZERO_PROOF_TARGET" in slip_text and "CLAIM_BLOCKED" in slip_text
    rows.append(validation_row("VAL1944_03_slip_control", "PASS" if slip_ok else "FAIL", "Cassini slip target and nonclaim blocker recorded"))

    claim_rows = rows_by_name["claim_gate"]
    nonclaim_passes = [row for row in claim_rows if row["status"] == "PASS_NONCLAIM"]
    blocked_claims = [row for row in claim_rows if row["status"] == "FAIL_BLOCKED"]
    claim_ok = len(nonclaim_passes) == 2 and len(blocked_claims) == 5 and all(row["claim_allowed"] == flag(False) for row in claim_rows)
    rows.append(validation_row("VAL1944_04_claim_gates", "PASS" if claim_ok else "FAIL", "only symbolic nonclaim gates pass; all local-GR claims blocked"))

    decision_ok = any("PROVE_LOCAL_TF_R11_ZERO_OR_BOUND_ITS_SLIP" == row["decision"] for row in rows_by_name["decision"])
    rows.append(validation_row("VAL1944_05_decision", "PASS" if decision_ok else "FAIL", "traceless spatial zero/bound target selected"))

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1945-Y5-R2FR-R11-traceless-spatial-zero-proof")
    rows.append(validation_row("VAL1944_06_next_target", "PASS" if next_ok else "FAIL", "1945 traceless-spatial R11 target selected"))

    flags_ok = all(row.get("valid_for_claim") == flag(False) and row.get("claim_allowed") == flag(False) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1944_07_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = all(csv_has_rows(path) for path in output_paths)
    rows.append(validation_row("VAL1944_08_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    branch_ok = all(csv_has_rows(path) for path in BRANCH_COPIES.values())
    rows.append(validation_row("VAL1944_09_branch_copies", "PASS" if branch_ok else "FAIL", "; ".join(str(path) for path in BRANCH_COPIES.values())))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    rows.append(validation_row("VAL1944_10_pycache_absent", "PASS" if pycache_absent else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_1944_artifact_count()
    rows.append(validation_row("VAL1944_11_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1944_artifact_count={formalization_count}"))

    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(validation_row("VAL1944_OVERALL", "PASS" if overall_ok else "FAIL", "1944 R11 weak-field potential equations or coefficient placeholder ledger"))
    return rows


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1944 Y5 R2FR: R11 Weak-Field Potential Equations or Coefficient Placeholder Ledger",
        "",
        "## Verdict",
        "",
        "1944 is a real narrowing step. The local Cassini problem is no longer just \"R11 exists, scary\". After subtracting the GR branch, the weak-field residual splits into a scalar/common-mode channel and a traceless-spatial anisotropic-slip channel.",
        "",
        "The useful result is: `delta_gamma_R11 ~= -(kappa_R/(C_TF U)) nabla^{-2} P_TF[R11_ij]`. So Cassini gamma mostly attacks the traceless spatial projection `P_TF[R11_ij]`, not every possible common residual. A common residual with `Phi_R11=Psi_R11` still needs Newtonian/ephemeris control, but it does not by itself create gamma slip.",
        "",
        "This is still nonclaim: `kappa_R`, `C_TF`, `P_TF[R11_ij]`, boundary conditions, and the small-residual proof are not parent-sourced. The next best derivation is a zero theorem or bound for `P_TF[R11_ij]`.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Weak-Field Derivation",
        "",
        markdown_table(rows_by_name["weak_field_derivation"]),
        "",
        "## Projection Coefficient Ledger",
        "",
        markdown_table(rows_by_name["coefficient_ledger"]),
        "",
        "## Cassini Slip Control Ledger",
        "",
        markdown_table(rows_by_name["cassini_slip_control"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "weak_field_derivation": weak_field_derivation_rows(),
        "coefficient_ledger": coefficient_ledger_rows(),
        "cassini_slip_control": cassini_slip_control_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
