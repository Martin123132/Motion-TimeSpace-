from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5183"

SIGN_CSV = OUT / "Lorentzian_Euclidean_static_sign_chain.csv"
RESPONSE_CSV = OUT / "two_sign_constrained_response.csv"
SCALING_CSV = OUT / "critical_pair_vs_required_response_scaling.csv"
DISPOSITION_CSV = OUT / "checkpoint_5182_claim_disposition.csv"
ROUTE_CSV = OUT / "sign_consistent_parent_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "Wick_sign_consistent_pair_response_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5183_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5183-Y5-R2FR-Wick-sign-consistent-static-pair-response-and-5182-supersession.md"
)

MARKER = "MTS_5183_WICK_SIGN_CONSISTENT_STATIC_PAIR_RESPONSE_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"
Q_LOCKED = 0.77

ROUTE_DECISION = (
    "CHECKPOINT_5182_MIXED_THE_EUCLIDEAN_PAIR_DETERMINANT_SIGN_WITH_THE_"
    "LORENTZIAN_STATIC_EINSTEIN_CONSTRAINT_SIGN_THE_CONSISTENT_WICK_AND_"
    "SOURCE_MAP_GIVES_THE_PHYSICAL_STATIC_EQUATION_KL_PLUS_C_TIMES_X_EQUALS_"
    "J_SO_THE_5182_ALL_ETA_SCREENING_THEOREM_IS_RETRACTED_THE_PARENT_OWNED_"
    "ETA_ZERO_RESULT_SURVIVES_EXACTLY_BECAUSE_THE_MINIMAL_PAIR_IS_PURE_SLIP_"
    "AND_DUST_INVISIBLE_A_NONZERO_CURVATURE_IMPROVEMENT_CAN_ENHANCE_PHI_"
    "BEFORE_ITS_CONSTRAINT_POLE_BUT_IT_IS_NOT_PARENT_OWNED_AND_THE_LOCAL_"
    "HILBERT_PAIR_CORRECTION_SCALES_AS_K_TIMES_NQ_RELATIVE_TO_EINSTEIN_"
    "WHEREAS_THE_REQUIRED_RESPONSE_SCALES_AS_NQ_OVER_K_THEIR_RATIO_IS_K_"
    "SQUARED_AND_NO_CONSTANT_NORMALIZATION_CAN_REPAIR_THE_FULL_CORRIDOR_"
    "THEREFORE_THE_CURRENT_ZERO_BACKGROUND_PAIR_ROUTE_REMAINS_REJECTED_FOR_"
    "THE_CORRECT_REASONS_AND_THE_NEXT_CALCULATION_IS_THE_PARENT_STATIONARY_"
    "BACKGROUND_LINEAR_METRIC_MOTION_HESSIAN"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES = {
    "checkpoint_4951_document": (
        source_path(
            "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-"
            "index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md"
        ),
        "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131",
    ),
    "checkpoint_4951_result": (
        source_path(
            "source-intake/functional_rg/4951/"
            "coupled_VFZX2_fixed_and_running_gate_results.json"
        ),
        "d48c187595a71c3be6c2720a7545372d06361788a2fb242b902ef8e4bfe6ad8c",
    ),
    "checkpoint_4960_document": (
        source_path(
            "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-"
            "local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
        ),
        "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    ),
    "checkpoint_4960_result": (
        source_path(
            "source-intake/functional_rg/4960/"
            "integrated_H_universal_source_results.json"
        ),
        "6fe2d8335cb1a4902c07c986e597e2f748050aa31f6137c5b52f9ced94542477",
    ),
    "checkpoint_4982_document": (
        source_path(
            "4982-Y5-R2FR-covariant-orderX-Schur-kernel-and-essential-two-point-"
            "subtraction.md"
        ),
        "83bfd153e96f7fb2322e2df1e71dce485caf5b7323230be285081ff280f55645",
    ),
    "checkpoint_4982_result": (
        source_path(
            "source-intake/functional_rg/4982/"
            "covariant_orderX_essential_results.json"
        ),
        "923aceac438808f912b03f032281ccc1bba960987ce70158222efc88f41d6b2f",
    ),
    "checkpoint_5148_document": (
        source_path(
            "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-"
            "theorem.md"
        ),
        "b2d5bddd8ce3cee2299b2cdadd66a0688bbd07c945bc329ac2ade4c20c113352",
    ),
    "checkpoint_5148_result": (
        source_path(
            "source-intake/functional_rg/5148/"
            "regime_selective_motion_response_results.json"
        ),
        "a9f48dd11d6c7f3bdd79436ade9d467c8b870b50c5fb2c5c760abae8dc3f05aa",
    ),
    "checkpoint_5150_document": (
        source_path(
            "5150-Y5-R2FR-minimal-occupied-PX-zero-mode-TT-polarization-and-"
            "critical-sign-gate.md"
        ),
        "1c7152513ee33a185113dc422be35034d7f7f40ea78d47001b4308c971f56458",
    ),
    "checkpoint_5150_result": (
        source_path(
            "source-intake/functional_rg/5150/"
            "minimal_occupied_PX_zero_mode_TT_results.json"
        ),
        "307fd49a9c9c38f47f3c381bcd57ab2001a1c6d286bcb5f2beddaf7eec0160d6",
    ),
    "checkpoint_5181_document": (
        source_path(
            "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-"
            "ownership-gate.md"
        ),
        "54a35ad66744f9e1f5ab6fdd15e66bc6f87a93330a999aae2235ea5cf98b3657",
    ),
    "checkpoint_5181_result": (
        source_path(
            "source-intake/functional_rg/5181/"
            "critical_pair_completion_results.json"
        ),
        "4c1f015ed2d946f4e158cb1b1954b3bb6dfc5a49f2f43c2fc92e847229f8f88d",
    ),
    "checkpoint_5182_document": (
        source_path(
            "5182-Y5-R2FR-static-Hilbert-pair-projector-constrained-Newtonian-"
            "response-and-route-decision.md"
        ),
        "fe9307a74581108b428b12eb4918205b24bc5615c47e370face7eff6892f1fcf",
    ),
    "checkpoint_5182_script": (
        source_path(
            "scripts/Y5_R2FR_5182_static_Hilbert_pair_projector_"
            "Newtonian_response_gate.py"
        ),
        "11d61ba7ac4237ae0d8221260a2a943f08512423160bf45f1f1b0f079fd87c74",
    ),
    "checkpoint_5182_result": (
        source_path(
            "source-intake/functional_rg/5182/"
            "static_Hilbert_pair_projector_results.json"
        ),
        "50fcd555fb9ee889a3d10cd4a5fe45ff61ef8c1447b3d6ff12b38ed9d56d63ee",
    ),
    "checkpoint_5182_validation": (
        source_path(
            "source-intake/mts_residuals/P8_Y5_BRR545_5182_VALIDATION.csv"
        ),
        "4347f9da515e4214346ed84070dce323be25b1ef1c8ed45ec502678728dda78f",
    ),
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        relative = file_path.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(file_digest(file_path).encode("ascii"))
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields = list(rows[0])
    if any(list(row) != fields for row in rows):
        raise ValueError(f"inconsistent fields: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def relative(path: Path) -> str:
    return path.relative_to(POST).as_posix()


def validation_row(
    validation_id: str,
    check: str,
    passed: bool,
    actual: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": validation_id,
        "check": check,
        "passed": bool(passed),
        "actual": actual,
        "expected": expected,
        "checkpoint_marker": MARKER,
    }


def log_slope(x_values: np.ndarray, y_values: np.ndarray) -> float:
    return float(np.polyfit(np.log(x_values), np.log(y_values), 1)[0])


def response_numeric(
    eta_value: float,
    ratio: float,
    sigma: int,
) -> dict[str, float]:
    first = 4.0 * eta_value - 1.0
    second = 1.0 - 8.0 * eta_value
    factor = 48.0 * eta_value**2 - 16.0 * eta_value + 1.0
    denominator = 1.0 + sigma * ratio * factor
    phi_ratio = 1.0 + (
        sigma
        * ratio
        * (first + second) ** 2
        / denominator
    )
    psi_ratio = (
        1.0 - sigma * ratio * first * second
    ) / denominator
    lens_ratio = 0.5 * (
        phi_ratio + psi_ratio
    )
    slip_ratio = (
        sigma
        * ratio
        * second
        * (first + second)
        / denominator
    )
    gamma = (
        psi_ratio / phi_ratio
        if abs(phi_ratio) > 1.0e-15
        else math.copysign(math.inf, psi_ratio)
    )
    return {
        "factor": factor,
        "denominator_over_a": denominator,
        "phi_ratio": phi_ratio,
        "psi_ratio": psi_ratio,
        "lensing_ratio": lens_ratio,
        "slip_over_phi_GR": slip_ratio,
        "gamma_PPN": gamma,
    }


def symbolic_contract() -> dict[str, Any]:
    a, d, u, v, rho, sigma = sp.symbols(
        "a d u v rho sigma",
        real=True,
        nonzero=True,
    )
    eta = sp.symbols("eta", real=True)
    kernel_l = a * sp.Matrix([[0, -1], [-1, 1]])
    vector = sp.Matrix([u, v])
    kernel = kernel_l + sigma * d * vector * vector.T
    potentials = sp.simplify(kernel.inv() * sp.Matrix([rho, 0]))
    phi_gr = -rho / a
    denominator = sp.factor(-kernel.det() / a)
    phi_ratio = sp.factor(potentials[0] / phi_gr)
    psi_ratio = sp.factor(potentials[1] / phi_gr)
    lens_ratio = sp.factor(
        (potentials[0] + potentials[1]) / (2 * phi_gr)
    )
    slip_ratio = sp.factor(
        (potentials[0] - potentials[1]) / phi_gr
    )
    expected_phi = sp.factor(
        1 + sigma * d * (u + v) ** 2 / denominator
    )
    eta_vector = sp.Matrix([4 * eta - 1, 1 - 8 * eta])
    eta_factor = 48 * eta**2 - 16 * eta + 1
    eta_substitution = {u: eta_vector[0], v: eta_vector[1]}
    return {
        "a": a,
        "d": d,
        "u": u,
        "v": v,
        "rho": rho,
        "sigma": sigma,
        "eta": eta,
        "kernel_l": kernel_l,
        "kernel": kernel,
        "denominator": denominator,
        "phi_ratio": phi_ratio,
        "psi_ratio": psi_ratio,
        "lens_ratio": lens_ratio,
        "slip_ratio": slip_ratio,
        "expected_phi": expected_phi,
        "eta_vector": eta_vector,
        "eta_factor": eta_factor,
        "eta_denominator": sp.factor(
            denominator.subs(eta_substitution)
        ),
        "eta_phi_ratio": sp.factor(
            phi_ratio.subs(eta_substitution)
        ),
        "eta_psi_ratio": sp.factor(
            psi_ratio.subs(eta_substitution)
        ),
        "eta_lens_ratio": sp.factor(
            lens_ratio.subs(eta_substitution)
        ),
        "eta_slip_ratio": sp.factor(
            slip_ratio.subs(eta_substitution)
        ),
    }


def make_rows() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    source_4960 = relative(SOURCES["checkpoint_4960_document"][0])
    source_5150 = relative(SOURCES["checkpoint_5150_document"][0])
    source_5182 = relative(SOURCES["checkpoint_5182_document"][0])
    source_5148 = relative(SOURCES["checkpoint_5148_document"][0])
    sign_rows = [
        {
            "step": "Lorentzian_Einstein_static",
            "equation": "S_L,EH^(2)=+1/2 x^T K_L x",
            "sign": "+K_L",
            "status": "derived_ADM_static",
            "source_path": source_4960,
            "valid_for_claim": False,
        },
        {
            "step": "Lorentzian_particle_source",
            "equation": "S_L,src=-J^T x",
            "sign": "-J",
            "status": "derived_from_-m_integral_ds",
            "source_path": source_4960,
            "valid_for_claim": False,
        },
        {
            "step": "Euclidean_Einstein_static",
            "equation": "S_E,EH^(2)=-1/2 x^T K_L x",
            "sign": "-K_L",
            "status": "Wick_rotated_static_action",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "step": "Euclidean_particle_source",
            "equation": "S_E,src=+J^T x",
            "sign": "+J",
            "status": "derived_from_+m_integral_ds_E",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "step": "Euclidean_pair_determinant",
            "equation": "Gamma_E,pair^(2)=-1/2 x^T C x",
            "sign": "-C",
            "status": "derived_from_+1/2_Tr_log_expansion",
            "source_path": source_5150,
            "valid_for_claim": False,
        },
        {
            "step": "Euclidean_stationarity",
            "equation": "(-K_L-C)x+J=0",
            "sign": "consistent",
            "status": "derived",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "step": "physical_static_equation",
            "equation": "(K_L+C)x=J",
            "sign": "sigma=+1",
            "status": "derived",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "step": "checkpoint_5182_equation",
            "equation": "(K_L-C)x=J",
            "sign": "sigma=-1",
            "status": "mixed_Euclidean_Lorentzian_signs",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
    ]

    response_rows = [
        {
            "case": "symbolic_general",
            "sigma": "sigma",
            "eta": "eta",
            "d_over_a": "r",
            "Delta_over_a": "1+sigma*r*(48eta^2-16eta+1)",
            "Phi_over_Phi_GR": "1+sigma*r*16eta^2/(Delta/a)",
            "Psi_over_Psi_GR": "[1-sigma*r*(4eta-1)*(1-8eta)]/(Delta/a)",
            "lensing_over_GR": "(R_Phi+R_Psi)/2",
            "gamma_PPN": "R_Psi/R_Phi",
            "status": "derived",
            "valid_for_claim": False,
        }
    ]
    samples = [
        ("minimal_parent", 0.0),
        ("nontrivial_no_slip", 1.0 / 8.0),
        ("pure_common", 1.0 / 6.0),
        ("negative_improvement", -0.25),
        ("positive_improvement", 1.0),
    ]
    for sigma_value, sign_label in ((-1, "5182_mixed_sign"), (1, "consistent")):
        for case, eta_value in samples:
            factor = 48.0 * eta_value**2 - 16.0 * eta_value + 1.0
            ratio = 0.5
            if 1.0 + sigma_value * ratio * factor <= 0.1:
                ratio = 0.05 / max(abs(factor), 1.0)
            values = response_numeric(eta_value, ratio, sigma_value)
            response_rows.append(
                {
                    "case": f"{sign_label}_{case}",
                    "sigma": sigma_value,
                    "eta": f"{eta_value:.17g}",
                    "d_over_a": f"{ratio:.17g}",
                    "Delta_over_a": f"{values['denominator_over_a']:.17g}",
                    "Phi_over_Phi_GR": f"{values['phi_ratio']:.17g}",
                    "Psi_over_Psi_GR": f"{values['psi_ratio']:.17g}",
                    "lensing_over_GR": f"{values['lensing_ratio']:.17g}",
                    "gamma_PPN": f"{values['gamma_PPN']:.17g}",
                    "status": (
                        "GR_exact"
                        if case == "minimal_parent"
                        else (
                            "enhancement_or_pole_side"
                            if sigma_value == 1
                            else "spurious_screening_branch"
                        )
                    ),
                    "valid_for_claim": False,
                }
            )

    scaling_rows = [
        {
            "quantity": "phase_occupation",
            "formula": "n_q(x)=1/(1+x^q); x=k/mu",
            "low_k_slope": "0",
            "high_k_slope": f"{-Q_LOCKED:.17g}",
            "role": "locked external pair form factor",
            "source_path": relative(SOURCES["checkpoint_5181_document"][0]),
            "valid_for_claim": False,
        },
        {
            "quantity": "required_5148_response",
            "formula": "C_q=n_q(x)/x",
            "low_k_slope": "-1",
            "high_k_slope": f"{-(1.0 + Q_LOCKED):.17g}",
            "role": "flat outer rotation and inner support target",
            "source_path": source_5148,
            "valid_for_claim": False,
        },
        {
            "quantity": "local_Hilbert_pair_ratio",
            "formula": "d/a proportional x*n_q(x)",
            "low_k_slope": "+1",
            "high_k_slope": f"{1.0 - Q_LOCKED:.17g}",
            "role": "two-derivative metric vertices times B0",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "quantity": "shape_ratio",
            "formula": "[x n_q]/[n_q/x]=x^2",
            "low_k_slope": "+2",
            "high_k_slope": "+2",
            "role": "proves no constant coefficient matches both shapes",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
        {
            "quantity": "finite_k_pole",
            "formula": "Delta_+=a+d(48eta^2-16eta+1)=0",
            "low_k_slope": "not_asymptotic_solution",
            "high_k_slope": "not_asymptotic_solution",
            "role": "isolated rank loss cannot replace infrared 1/k corridor",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
    ]

    disposition_rows = [
        {
            "claim_id": "5182_static_Hilbert_vertex",
            "old_status": "derived",
            "new_status": "retained",
            "reason": "metric expansion and rank-one pair covariance are unaffected",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
        {
            "claim_id": "5182_eta_zero_pure_slip",
            "old_status": "derived",
            "new_status": "retained",
            "reason": "w(0)=(-1,1) is sign independent",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
        {
            "claim_id": "5182_eta_zero_dust_invisible",
            "old_status": "derived",
            "new_status": "retained",
            "reason": "u+v=0 makes Phi and Psi exactly GR for sigma plus or minus",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
        {
            "claim_id": "5182_all_eta_screening",
            "old_status": "claimed",
            "new_status": "retracted",
            "reason": "used sigma=-1 from mixed Euclidean and Lorentzian kernels",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
        {
            "claim_id": "5182_eta_one_eighth_screening",
            "old_status": "claimed",
            "new_status": "retracted",
            "reason": "consistent result is 4a/(4a-d)>1 before the pole",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
        {
            "claim_id": "5182_eta_one_sixth_screening",
            "old_status": "claimed",
            "new_status": "retracted",
            "reason": "consistent lensing result is 3a/(3a-d)>1 before the pole",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
        {
            "claim_id": "5182_gap_collapse_not_standalone_rescue",
            "old_status": "derived",
            "new_status": "retained_for_current_parent",
            "reason": "eta=0 remains dust invisible and local pair scaling remains wrong",
            "source_path": source_5182,
            "valid_for_claim": False,
        },
        {
            "claim_id": "5182_zero_background_pair_route",
            "old_status": "rejected",
            "new_status": "rejected_with_corrected_reason",
            "reason": "parent eta=0 invisibility plus k*n_q versus n_q/k shape mismatch",
            "source_path": str(SCRIPT),
            "valid_for_claim": False,
        },
    ]

    route_rows = [
        {
            "decision": "RETRACT_5182_ALL_ETA_SCREENING_THEOREM",
            "status": "required",
            "reason": "the old scalar response combined incompatible signature conventions",
            "next_action": "use checkpoint 5183 as authoritative sign result",
            "valid_for_claim": False,
        },
        {
            "decision": "RETAIN_PARENT_ETA_ZERO_DUST_INVISIBILITY",
            "status": "proved",
            "reason": "minimal Hilbert pair projector is exactly pure slip",
            "next_action": "do not use zero-background pair as galaxy source",
            "valid_for_claim": False,
        },
        {
            "decision": "ALLOW_NONMINIMAL_ENHANCEMENT_ONLY_AS_UNOWNED_EXTENSION",
            "status": "conditional",
            "reason": "consistent sign permits enhancement but parent derives eta=0",
            "next_action": "no claim or fitted eta insertion",
            "valid_for_claim": False,
        },
        {
            "decision": "REJECT_LOCAL_PAIR_SCALING_AS_5148_RESPONSE",
            "status": "proved",
            "reason": "x*n_q and n_q/x differ by x^2 over the full corridor",
            "next_action": "require a different linear/background carrier",
            "valid_for_claim": False,
        },
        {
            "decision": "DERIVE_STATIONARY_BACKGROUND_LINEAR_MIXING",
            "status": "selected_next",
            "reason": "test the remaining parent-owned B block without mixed signs",
            "next_action": "checkpoint_5184",
            "valid_for_claim": False,
        },
        {
            "decision": "RETAIN_DIRECT_CONSERVED_STATE_STRESS",
            "status": "conditional",
            "reason": "checkpoint 5151 is independent of the corrected pair Hessian",
            "next_action": "source-selection remains open",
            "valid_for_claim": False,
        },
        {
            "decision": "NO_LOCAL_GR_GALAXY_OR_FULL_MTS_PROMOTION",
            "status": "nonclaim",
            "reason": "correction restores discipline but does not close the parent bridge",
            "next_action": "keep private",
            "valid_for_claim": False,
        },
    ]

    summary = {
        "checkpoint_5182_sign_consistent": False,
        "checkpoint_5182_all_eta_screening_retracted": True,
        "physical_static_pair_sign_sigma": 1,
        "physical_static_equation": "(K_L+C)x=J",
        "parent_owned_eta": 0.0,
        "parent_eta_zero_dust_response": "exactly_GR",
        "nonminimal_positive_pair_can_enhance_before_pole": True,
        "nonminimal_extension_parent_owned": False,
        "pair_relative_shape": "x*n_q(x)",
        "required_relative_shape": "n_q(x)/x",
        "shape_ratio": "x^2",
        "constant_normalization_can_match_full_corridor": False,
        "current_zero_background_pair_route_rejected": True,
        "direct_conserved_state_stress_survives": True,
        "next_target": "DERIVE_STATIONARY_BACKGROUND_LINEAR_MIXING",
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return (
        sign_rows,
        response_rows,
        scaling_rows,
        disposition_rows,
        route_rows,
        summary,
    )


def write_document(result: dict[str, Any]) -> None:
    metrics = result["metrics"]
    text = f"""# 5183 - Wick-sign-consistent static pair response and 5182 supersession

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Correction

Checkpoint 5182 correctly derived the static Hilbert pair vertex and its
rank-one projector, but it combined the Euclidean matter-determinant sign
with the Lorentzian static Einstein constraint kernel. Its conclusion that
every curvature-improved passive pair must screen the Newtonian potential is
therefore retracted.

This correction does not reopen the current parent pair route. The
parent-owned value remains `eta=0`, where the pair is pure gravitational
slip and exactly invisible to dust. In addition, the local two-derivative
Hilbert pair correction has the wrong momentum scaling for checkpoint 5148.

## 1. Action-level sign map

Let

```text
x=(Phi,Psi),
S_L,EH^(2)=+1/2 x^T K_L x,
S_L,src=-J^T x.
```

For a static Wick rotation,

```text
S_E,EH^(2)=-1/2 x^T K_L x,
S_E,src=+J^T x.
```

The bosonic Euclidean determinant is

```text
Gamma_E,pair=+1/2 Tr log(A_0+V[x]),

Gamma_E,pair^(2)=-1/2 x^T C x,
C>=0.
```

Euclidean stationarity therefore gives

```text
(-K_L-C)x+J=0,

(K_L+C)x=J.
```

Checkpoint 5182 instead inverted `K_L-C`. That was the precise mixed-sign
step.

## 2. Exact two-sign response

Write

```text
K_sigma=K_L+sigma d w w^T,
K_L=a[[0,-1],[-1,1]],
a=2M_R^2 k^2,
d>=0,
w=(u,v).
```

For a dust source,

```text
Delta_sigma=a-sigma d u(u+2v),

Phi/Phi_GR
 =1+sigma d(u+v)^2/Delta_sigma,

Psi/Psi_GR
 =(a-sigma d u v)/Delta_sigma,

(Phi-Psi)/Phi_GR
 =sigma d v(u+v)/Delta_sigma.
```

The old checkpoint used `sigma=-1`. The consistent static free-energy
response has `sigma=+1`. On its GR-connected side `Delta_+>0`,

```text
Phi/Phi_GR>=1.
```

Thus a nonminimal positive pair projector can enhance rather than screen.
This is not a parent prediction because the exact shift-symmetric parent has
no `R chi^2` vertex.

For the operational vector

```text
w(eta)=(4eta-1,1-8eta),
F(eta)=48eta^2-16eta+1,
Delta_+=a+dF(eta),
```

the parent value `eta=0` still obeys

```text
w=(-1,1),
Phi=Psi=Phi_GR.
```

At the nontrivial no-slip value `eta=1/8`,

```text
Phi/Phi_GR=Psi/Psi_GR=4a/(4a-d)>1
```

before the pole. At the pure-common value `eta=1/6`,

```text
Phi/Phi_GR=(9a+d)/(9a-3d),
Psi/Psi_GR=(9a-d)/(9a-3d),
lensing/GR=3a/(3a-d).
```

These replace the corresponding screening formulas in checkpoint 5182.

## 3. Correct route rejection: momentum scaling

Let `x=k/mu` and use the already derived external pair form factor

```text
n_q(x)=1/(1+x^q).
```

Checkpoint 5148 requires

```text
C_q(x)=n_q(x)/x,
```

with slopes `-1` at small `x` and `-(1+q)` at large `x`.

Two local two-derivative Hilbert vertices multiplying the massless
`B_0~1/k` pair bubble give a metric correction `d~k^3 n_q`. Relative to
the Einstein kernel `a~k^2`,

```text
d/a proportional x n_q(x).
```

Its slopes are `+1` and `1-q`. The exact shape ratio is

```text
[x n_q]/[n_q/x]=x^2.
```

For the locked `q={Q_LOCKED}`, the numerical slopes are

```text
pair low/high     = {metrics['pair_low_slope']:.15g},
                    {metrics['pair_high_slope']:.15g},
target low/high   = {metrics['target_low_slope']:.15g},
                    {metrics['target_high_slope']:.15g},
ratio slope       = {metrics['shape_ratio_slope']:.15g}.
```

No constant normalization can turn the pair response into the required
response over the scale corridor. A finite-`k` zero of `Delta_+` is a
constraint pole, not the required asymptotic `1/k` enhancement.

## 4. Claim disposition

Retained from checkpoint 5182:

- the exact static metric expansion and pair covariance;
- `eta=0` pure-slip projection;
- exact dust invisibility of the current parent;
- gap collapse alone does not rescue the current parent route.

Retracted from checkpoint 5182:

- the all-`eta` screening theorem;
- the `eta=1/8` screening formula;
- the `eta=1/6` screening and lensing formulas.

The current zero-background pair route remains rejected, now for two
sign-consistent reasons: the parent owns `eta=0`, and the local pair
correction has `x n_q` rather than `n_q/x` scaling.

## 5. Next calculation

Checkpoint 5184 must now derive or reject the parent stationary nonzero
motion background and its actual linear `h-delta chi` Hessian. It must test
the shift-current equation, regular boundary conditions, background Hilbert
stress, static versus finite-frequency mixing, and the local-GR limit.

Checkpoint 5151's direct conserved state stress remains a distinct
conditional route.

No local-GR, galaxy, cosmology or full-MTS claim is made. The protected
formalization digest remains
`{result['formalization_workbench_tree_sha256']}` and checkpoint 5176
remains `{result['checkpoint_5176_tree_sha256']}`.

## Evidence

- `{relative(SIGN_CSV)}`
- `{relative(RESPONSE_CSV)}`
- `{relative(SCALING_CSV)}`
- `{relative(DISPOSITION_CSV)}`
- `{relative(ROUTE_CSV)}`
- `{relative(PROVENANCE_CSV)}`
- `{relative(RESULT_JSON)}`
- `{relative(VALIDATION_CSV)}`

## Machine decision

`{ROUTE_DECISION}`
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(DOCUMENT)


def calculate(
    symbolic: dict[str, Any],
    rows: tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        dict[str, Any],
    ],
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_5176_before: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    a = symbolic["a"]
    d = symbolic["d"]
    u = symbolic["u"]
    v = symbolic["v"]
    sigma = symbolic["sigma"]
    eta = symbolic["eta"]
    exact_checks = {
        "general_phi_identity": sp.simplify(
            symbolic["phi_ratio"] - symbolic["expected_phi"]
        )
        == 0,
        "eta_factor_identity": sp.simplify(
            symbolic["eta_factor"]
            - (4 * eta - 1) * (12 * eta - 1)
        )
        == 0,
        "minimal_common_overlap_zero": sp.simplify(
            sum(symbolic["eta_vector"]).subs(eta, 0)
        )
        == 0,
        "no_slip_roots": sp.solve(
            sp.Eq(
                sp.together(symbolic["eta_slip_ratio"]).as_numer_denom()[0],
                0,
            ),
            eta,
        )
        == [sp.Integer(0), sp.Rational(1, 8)],
    }

    inverse_residuals = []
    plus_phi_excess_minimum = math.inf
    old_phi_excess_maximum = -math.inf
    sampled_points = 0
    for sigma_value in (-1, 1):
        for eta_value in np.linspace(-2.0, 2.0, 801):
            first = 4.0 * eta_value - 1.0
            second = 1.0 - 8.0 * eta_value
            factor = 48.0 * eta_value**2 - 16.0 * eta_value + 1.0
            for ratio in (0.002, 0.01, 0.05, 0.2, 0.7):
                denominator = 1.0 + sigma_value * ratio * factor
                if denominator <= 1.0e-5:
                    continue
                kernel = np.array(
                    [[0.0, -1.0], [-1.0, 1.0]]
                ) + sigma_value * ratio * np.outer(
                    [first, second],
                    [first, second],
                )
                potentials = np.linalg.solve(
                    kernel,
                    np.array([1.0, 0.0]),
                )
                values = response_numeric(
                    float(eta_value),
                    ratio,
                    sigma_value,
                )
                inverse_residuals.extend(
                    [
                        abs(potentials[0] / -1.0 - values["phi_ratio"]),
                        abs(potentials[1] / -1.0 - values["psi_ratio"]),
                        abs(
                            (potentials[0] + potentials[1]) / -2.0
                            - values["lensing_ratio"]
                        ),
                    ]
                )
                sampled_points += 1
                if sigma_value == 1:
                    plus_phi_excess_minimum = min(
                        plus_phi_excess_minimum,
                        values["phi_ratio"] - 1.0,
                    )
                else:
                    old_phi_excess_maximum = max(
                        old_phi_excess_maximum,
                        values["phi_ratio"] - 1.0,
                    )

    x_low = np.logspace(-10.0, -6.0, 200)
    x_high = np.logspace(6.0, 10.0, 200)

    def occupation(values: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + values**Q_LOCKED)

    pair_low = x_low * occupation(x_low)
    pair_high = x_high * occupation(x_high)
    target_low = occupation(x_low) / x_low
    target_high = occupation(x_high) / x_high
    shape_x = np.logspace(-10.0, 10.0, 500)
    shape_ratio = (
        shape_x * occupation(shape_x)
    ) / (
        occupation(shape_x) / shape_x
    )
    shape_identity_residual = float(
        np.max(np.abs(shape_ratio / shape_x**2 - 1.0))
    )
    metrics = {
        "maximum_numeric_inverse_residual": max(inverse_residuals),
        "sampled_constraint_points": sampled_points,
        "minimum_plus_sign_phi_excess": plus_phi_excess_minimum,
        "maximum_old_sign_phi_excess": old_phi_excess_maximum,
        "pair_low_slope": log_slope(x_low, pair_low),
        "pair_high_slope": log_slope(x_high, pair_high),
        "target_low_slope": log_slope(x_low, target_low),
        "target_high_slope": log_slope(x_high, target_high),
        "shape_ratio_slope": log_slope(shape_x, shape_ratio),
        "shape_identity_residual": shape_identity_residual,
        "old_eta_one_eighth_phi_ratio": response_numeric(
            1.0 / 8.0,
            0.5,
            -1,
        )["phi_ratio"],
        "correct_eta_one_eighth_phi_ratio": response_numeric(
            1.0 / 8.0,
            0.5,
            1,
        )["phi_ratio"],
        "old_eta_one_sixth_lensing_ratio": response_numeric(
            1.0 / 6.0,
            0.5,
            -1,
        )["lensing_ratio"],
        "correct_eta_one_sixth_lensing_ratio": response_numeric(
            1.0 / 6.0,
            0.5,
            1,
        )["lensing_ratio"],
        "exact_symbolic_checks": exact_checks,
    }
    (
        sign_rows,
        response_rows,
        scaling_rows,
        disposition_rows,
        route_rows,
        summary,
    ) = rows
    checks = [
        validation_row(
            "V5183_01_source_count",
            "all declared sources exist",
            len(source_hashes) == len(SOURCES),
            len(source_hashes),
            len(SOURCES),
        ),
        validation_row(
            "V5183_02_source_hashes",
            "all source hashes match locks",
            all(
                source_hashes[name] == expected
                for name, (_, expected) in SOURCES.items()
            ),
            sum(
                source_hashes[name] == expected
                for name, (_, expected) in SOURCES.items()
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5183_03_formal_lock",
            "formalization-workbench remains protected",
            formal_before == FORMAL_DIGEST_LOCK,
            formal_before,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5183_04_5176_lock",
            "checkpoint 5176 remains immutable",
            checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_before,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5183_05_general_phi_identity",
            "general rank-one dust response identity closes",
            exact_checks["general_phi_identity"],
            exact_checks["general_phi_identity"],
            True,
        ),
        validation_row(
            "V5183_06_eta_factor",
            "eta projector factorization closes",
            exact_checks["eta_factor_identity"],
            exact_checks["eta_factor_identity"],
            True,
        ),
        validation_row(
            "V5183_07_eta_zero_overlap",
            "parent eta=0 is pure slip",
            exact_checks["minimal_common_overlap_zero"],
            exact_checks["minimal_common_overlap_zero"],
            True,
        ),
        validation_row(
            "V5183_08_no_slip_roots",
            "no-slip roots remain eta=0 and eta=1/8",
            exact_checks["no_slip_roots"],
            exact_checks["no_slip_roots"],
            True,
        ),
        validation_row(
            "V5183_09_numeric_inverse",
            "direct matrix inversions match symbolic responses",
            metrics["maximum_numeric_inverse_residual"] < 2.0e-10,
            metrics["maximum_numeric_inverse_residual"],
            "<2e-10",
        ),
        validation_row(
            "V5183_10_consistent_enhancement",
            "sigma=+1 never screens Phi on sampled GR-connected points",
            metrics["minimum_plus_sign_phi_excess"] >= -2.0e-12,
            metrics["minimum_plus_sign_phi_excess"],
            ">=-2e-12",
        ),
        validation_row(
            "V5183_11_old_sign_screening",
            "sigma=-1 reproduces the old nonpositive Phi shift",
            metrics["maximum_old_sign_phi_excess"] <= 2.0e-12,
            metrics["maximum_old_sign_phi_excess"],
            "<=2e-12",
        ),
        validation_row(
            "V5183_12_eta_one_eighth_flip",
            "eta=1/8 changes from screening to enhancement",
            metrics["old_eta_one_eighth_phi_ratio"] < 1.0
            < metrics["correct_eta_one_eighth_phi_ratio"],
            [
                metrics["old_eta_one_eighth_phi_ratio"],
                metrics["correct_eta_one_eighth_phi_ratio"],
            ],
            ["<1", ">1"],
        ),
        validation_row(
            "V5183_13_eta_one_sixth_flip",
            "eta=1/6 lensing changes from screening to enhancement",
            metrics["old_eta_one_sixth_lensing_ratio"] < 1.0
            < metrics["correct_eta_one_sixth_lensing_ratio"],
            [
                metrics["old_eta_one_sixth_lensing_ratio"],
                metrics["correct_eta_one_sixth_lensing_ratio"],
            ],
            ["<1", ">1"],
        ),
        validation_row(
            "V5183_14_pair_low_slope",
            "local pair relative correction has low-k slope +1",
            abs(metrics["pair_low_slope"] - 1.0) < 2.0e-5,
            metrics["pair_low_slope"],
            1.0,
        ),
        validation_row(
            "V5183_15_pair_high_slope",
            "local pair relative correction has high-k slope 1-q",
            abs(metrics["pair_high_slope"] - (1.0 - Q_LOCKED))
            < 2.0e-5,
            metrics["pair_high_slope"],
            1.0 - Q_LOCKED,
        ),
        validation_row(
            "V5183_16_target_low_slope",
            "required response has low-k slope -1",
            abs(metrics["target_low_slope"] + 1.0) < 2.0e-5,
            metrics["target_low_slope"],
            -1.0,
        ),
        validation_row(
            "V5183_17_target_high_slope",
            "required response has high-k slope -(1+q)",
            abs(metrics["target_high_slope"] + 1.0 + Q_LOCKED)
            < 2.0e-5,
            metrics["target_high_slope"],
            -(1.0 + Q_LOCKED),
        ),
        validation_row(
            "V5183_18_shape_ratio",
            "pair/target shape ratio is exactly x^2",
            metrics["shape_identity_residual"] < 1.0e-14
            and abs(metrics["shape_ratio_slope"] - 2.0) < 1.0e-12,
            [
                metrics["shape_identity_residual"],
                metrics["shape_ratio_slope"],
            ],
            ["<1e-14", 2.0],
        ),
        validation_row(
            "V5183_19_5182_retracted",
            "all-eta screening theorem is explicitly retracted",
            summary["checkpoint_5182_all_eta_screening_retracted"],
            summary["checkpoint_5182_all_eta_screening_retracted"],
            True,
        ),
        validation_row(
            "V5183_20_parent_eta_zero",
            "current parent still owns eta=0",
            summary["parent_owned_eta"] == 0.0,
            summary["parent_owned_eta"],
            0.0,
        ),
        validation_row(
            "V5183_21_parent_dust_exact",
            "parent eta=0 dust response remains exactly GR",
            summary["parent_eta_zero_dust_response"] == "exactly_GR",
            summary["parent_eta_zero_dust_response"],
            "exactly_GR",
        ),
        validation_row(
            "V5183_22_scaling_rejection",
            "constant normalization cannot repair the response shape",
            not summary["constant_normalization_can_match_full_corridor"],
            summary["constant_normalization_can_match_full_corridor"],
            False,
        ),
        validation_row(
            "V5183_23_route_rejected",
            "current zero-background pair route remains rejected",
            summary["current_zero_background_pair_route_rejected"],
            summary["current_zero_background_pair_route_rejected"],
            True,
        ),
        validation_row(
            "V5183_24_next_target",
            "stationary background mixing is selected next",
            summary["next_target"]
            == "DERIVE_STATIONARY_BACKGROUND_LINEAR_MIXING",
            summary["next_target"],
            "DERIVE_STATIONARY_BACKGROUND_LINEAR_MIXING",
        ),
        validation_row(
            "V5183_25_row_counts",
            "evidence row counts match contract",
            [
                len(sign_rows),
                len(response_rows),
                len(scaling_rows),
                len(disposition_rows),
                len(route_rows),
            ]
            == [8, 11, 5, 8, 7],
            [
                len(sign_rows),
                len(response_rows),
                len(scaling_rows),
                len(disposition_rows),
                len(route_rows),
            ],
            [8, 11, 5, 8, 7],
        ),
        validation_row(
            "V5183_26_selected_next_unique",
            "exactly one next calculation is selected",
            sum(row["status"] == "selected_next" for row in route_rows)
            == 1,
            sum(row["status"] == "selected_next" for row in route_rows),
            1,
        ),
        validation_row(
            "V5183_27_nonclaim",
            "all claim promotion flags remain false",
            not any(
                summary[key]
                for key in (
                    "valid_for_local_GR_claim",
                    "valid_for_galaxy_claim",
                    "valid_for_cosmology_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            [
                summary["valid_for_local_GR_claim"],
                summary["valid_for_galaxy_claim"],
                summary["valid_for_cosmology_claim"],
                summary["valid_for_full_MTS_claim"],
            ],
            [False, False, False, False],
        ),
    ]
    return checks, metrics


def run(dry_run: bool) -> dict[str, Any]:
    missing = [
        name for name, (path, _) in SOURCES.items() if not path.is_file()
    ]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    source_hashes_before = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)
    symbolic = symbolic_contract()
    rows = make_rows()
    checks, metrics = calculate(
        symbolic,
        rows,
        source_hashes_before,
        formal_before,
        checkpoint_5176_before,
    )
    failures = [row["validation_id"] for row in checks if not row["passed"]]
    (
        sign_rows,
        response_rows,
        scaling_rows,
        disposition_rows,
        route_rows,
        summary,
    ) = rows
    dry_result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": dry_run,
        "route_decision": ROUTE_DECISION,
        "metrics": metrics,
        "summary": summary,
        "validation_count": len(checks),
        "validation_failures": failures,
    }
    if failures:
        raise RuntimeError(f"dry validation failures: {failures}")
    if dry_run:
        return dry_result

    write_csv(SIGN_CSV, sign_rows)
    write_csv(RESPONSE_CSV, response_rows)
    write_csv(SCALING_CSV, scaling_rows)
    write_csv(DISPOSITION_CSV, disposition_rows)
    write_csv(ROUTE_CSV, route_rows)
    provenance_rows = [
        {
            "source_id": name,
            "source_path": str(path),
            "sha256": source_hashes_before[name],
            "expected_sha256": expected,
            "status": "hash_locked_read_only",
            "checked_date": CHECKED_DATE,
        }
        for name, (path, expected) in SOURCES.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)

    source_hashes_after = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    output_tables = (
        SIGN_CSV,
        RESPONSE_CSV,
        SCALING_CSV,
        DISPOSITION_CSV,
        ROUTE_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_tables
    )
    output_digest = hashlib.sha256(output_text.encode("utf-8")).hexdigest()
    full_checks = checks + [
        validation_row(
            "V5183_28_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in SOURCES
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5183_29_formal_after",
            "formalization-workbench remains unchanged",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5183_30_5176_after",
            "checkpoint 5176 remains immutable",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5183_31_no_placeholders",
            "generated evidence contains no missing-input placeholder",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5183_32_provenance_rows",
            "every source has one provenance row",
            len(provenance_rows) == len(SOURCES),
            len(provenance_rows),
            len(SOURCES),
        ),
        validation_row(
            "V5183_33_output_parse",
            "all output CSVs parse with nonempty rows",
            all(
                len(list(csv.DictReader(path.open(encoding="utf-8")))) > 0
                for path in output_tables
            ),
            len(output_tables),
            len(output_tables),
        ),
        validation_row(
            "V5183_34_claim_columns",
            "every evidence row remains nonclaim",
            all(
                str(row["valid_for_claim"]).lower() == "false"
                for table in (
                    sign_rows,
                    response_rows,
                    scaling_rows,
                    disposition_rows,
                    route_rows,
                )
                for row in table
            ),
            False,
            False,
        ),
        validation_row(
            "V5183_35_local_branch_unchanged",
            "local GR/Newton/Maxwell branch is unchanged",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
    ]
    full_failures = [
        row["validation_id"] for row in full_checks if not row["passed"]
    ]
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": False,
        "route_decision": ROUTE_DECISION,
        "source_paths": {
            name: str(path) for name, (path, _) in SOURCES.items()
        },
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "checkpoint_5176_tree_sha256": checkpoint_5176_after,
        "output_payload_sha256": output_digest,
        "metrics": metrics,
        "summary": summary,
        "validation_count": len(full_checks),
        "validation_failures": full_failures,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_document(result)
    write_csv(VALIDATION_CSV, full_checks)
    if full_failures:
        raise RuntimeError(f"validation failures: {full_failures}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Derive the Wick-sign-consistent static pair response, retract "
            "the mixed-sign 5182 theorem, and gate the surviving parent route."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate calculations and source locks without writing outputs",
    )
    arguments = parser.parse_args()
    result = run(arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
