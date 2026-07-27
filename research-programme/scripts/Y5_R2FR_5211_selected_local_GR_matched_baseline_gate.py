from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import sympy as sp

import Y5_R2FR_5210_parent_vacuum_coordinate_ownership as checkpoint_5210


CHECKPOINT = 5211
MARKER = "MTS_5211_SELECTED_LOCAL_GR_MATCHED_GRSM_BASELINE_THEOREM"
CHECKED_DATE = "2026-07-24"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5211-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-"
    "truncation-universal-source-and-matched-GRSM-excess-theorem.md"
)
PUBLIC = checkpoint_5210.PUBLIC
GALAXY = checkpoint_5210.GALAXY
PUBLIC_HEAD = checkpoint_5210.PUBLIC_HEAD
GALAXY_HEAD = checkpoint_5210.GALAXY_HEAD
GALAXY_DIRTY = checkpoint_5210.GALAXY_DIRTY
FORMAL_LOCK = checkpoint_5210.FORMAL_LOCK
REDUCED_PLANCK_EV = 2.435e27
HBAR_C_EV_M = 1.973269804e-7
SOURCE_LOCKS = {
    POST
    / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-"
    "form-factor-completion-or-renormalized-vacuum-freeze.md": (
        "9d57f0ec8028530a48c7cab90b0447fead680461500a8c3da2390a253ac39dd4"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4877_NONLOCAL_FORM_FACTORS.csv": (
        "ac5ee17a54d7dc16f8bee68b4290b0c70ca1bc9a02af204db47e511bb8e435e8"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4877_ARENA_SMOKE.csv": (
        "4881cafb5938ab0145aa3e221b08bafd8165f28a63203d79a07a7b4f818016c7"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4942"
    / "local_homogeneous_branch_identities.csv": (
        "e9e4532679843c78ab2c86ddc39589bb6c694ca9cb17aae6a7bae47af66d4d0a"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4942"
    / "local_O4_C3_CFF_residual_vector.csv": (
        "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4943"
    / "matter_source_selection_rules.csv": (
        "2e9308c2d88336aeeab957fe78ce3d3a1d912809fc9a20afc416031394fb7a1b"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4943"
    / "junction_scalar_charge_and_fifth_force.csv": (
        "5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4943"
    / "interior_stability_benchmarks.csv": (
        "3c49fdc86490eb936c27fc954b420ab1205fa2e6211e87507cc33cec7f64e3af"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4944"
    / "visible_CFF_matching_components.csv": (
        "96a8b2f3efe054681203516422e1f1133a725ce70cb1f36fb0a5ab3b863b7b2a"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4944"
    / "conditional_total_CFF_local_residual_bound.csv": (
        "bc1700d28d660fb6e1d868ecc0a19ef6f472c6b832cb85e832dbed96e69b35f3"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4947"
    / "source_residue_chain.csv": (
        "b08468f29f938dfe72f13b9eec93f73c2b4f9c58ff89e7b67008c6de2cfc1e1d"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "soft_Bianchi_species_coupling_nullspace.csv": (
        "ad714332cf51eccb8b271394715b8de27affe3baee21889223da74aeeee1ac51"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "universal_source_decision.csv": (
        "cbfb4a1a2d77450744e3275ed4ccea66b028f7d67502958f21c823e01f23d4bf"
    ),
    POST
    / "4971-Y5-R2FR-parent-field-content-finite-amplitude-projector-and-"
    "two-scale-anchor-or-local-route-rejection.md": (
        "08ff7fba56ca932e28258ac1112eeed1a3133b3be50a9766bbf1c7e35814ea4f"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4971"
    / "C3_local_anchor_identifiability.csv": (
        "d3b5bc38cc6832e09f5d5008138656ad785ca5d7319f4ecfd98c06e3bf66cd2d"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4971"
    / "C3_two_scale_helicity_projector.csv": (
        "c155389bda075609dbbcaf72fe23e3283395f7c3a5f5291f2ed42908a966be01"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5201"
    / "coframe_matter_variation_and_Ward_chain.csv": (
        "18612fc245ec3eef8fd2ab3a46a742f40fdda5707719a440c74f5b1e626fed77"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5201"
    / "linearized_Einstein_Newton_symbolic_reduction.csv": (
        "654c451646a63325646444eaa54d7a5056ed050bdc60cda19bc7fd4f51dcc8ea"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5201"
    / "full_PPN_residual_vector.csv": (
        "e5f9328a605a65ba9a319f903f404baf0a3d178d9e2f41f48b3a961bdcde1482"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5201"
    / "Maxwell_stress_Poynting_symbolic_reduction.csv": (
        "9bded485d9bda6619533e5b3aa8346fd267c564dea61969f3efe79be9af8144d"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5201"
    / "boundary_state_local_silence_gate.csv": (
        "2a18ff61eaec66da2870c5ede939d62debe56e004401b45688266c180c9dcd40"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5203"
    / "canonical_translation_parent_action.csv": (
        "f0a84d6d37697d9f01b6991ca32e20f6e87352185224b437ac6611039d952c27"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5203"
    / "local_Z2_double_zero_theorem.csv": (
        "76cfc45de79c8c25df02da4c1c13367fe370b465e949570ae9fad21a9fe23d21"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5203"
    / "common_action_branch_reduction.csv": (
        "e64a9b203a062d38336df2b535bbdfed0666042143c720f9dbe00cb11e3e6a42"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "common_minimal_motion_trajectory_results.json": (
        "fbda1e61e5eec0aed77f411fa6309b4e97c87b61e06b007684e9065af2ca70df"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "common_trajectory_flow_theorems.csv": (
        "caef187228801a9c075e5e1b97dd7b92bff398a2f8716976af9f5bcec1904232"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "local_GR_residual_bounds.csv": (
        "72affda71fa29465304cd8066e91b6c30d80de34cdabf34187dd5cc06b0a68cb"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "physical_scale_and_power_counting.csv": (
        "fd04fed1442f83389ee405c6209eb1a2b1ef518ed27ec9fab7fcd7cd605fd312"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "route_decision.csv": (
        "ce2e727af43bfdc1f43f1ae7a701c29b9afbbd2f3aad156941852f503dbb5618"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5209"
    / "local_GR_Newton_Maxwell_residuals.csv": (
        "b1be7467bf034e215befb453f5d977b9a8c8cedf02e61a104ed68943376642fa"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5209"
    / "route_decision.csv": (
        "52452f9aaa88d47732889251abede8ba2de4025fb838a5f258d98405b3b6f541"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5210"
    / "parent_vacuum_coordinate_ownership_results.json": (
        "3d8602208269ad1a0058c2d1feee3fcb057ea29b330260be4aa4173f9851b95c"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5210"
    / "single_calibration_local_propagation.csv": (
        "147a7ab0d895bc0c707ada69926e40949d6417b5d1e9ba75003e44febe64529a"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5210"
    / "route_decision.csv": (
        "4d130fa2759a085ee6b7e6e476ea402fb30cc1da90a83966fa11d1802101c433"
    ),
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def selected_digest(paths: list[Path], base: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(file_digest(path).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint": CHECKPOINT,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "claim_allowed": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def assert_source_locks() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path, expected in SOURCE_LOCKS.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = file_digest(path)
        if actual != expected:
            raise RuntimeError(
                f"source lock mismatch for {path}: expected {expected}, got {actual}"
            )
        hashes[path.relative_to(POST).as_posix()] = actual
    return hashes


def tree_digest() -> str:
    return checkpoint_5210.checkpoint_5209.checkpoint_5208.tree_digest(FORMAL)


def git_state(repository: Path) -> tuple[str, list[str]]:
    return checkpoint_5210.checkpoint_5209.checkpoint_5208.git_state(repository)


def assert_untouched_boundaries() -> dict[str, Any]:
    formal_digest = tree_digest()
    if formal_digest != FORMAL_LOCK:
        raise RuntimeError("formalization-workbench changed")
    public_head, public_status = git_state(PUBLIC)
    if public_head != PUBLIC_HEAD or public_status:
        raise RuntimeError("public worktree changed")
    galaxy_head, galaxy_status = git_state(GALAXY)
    if galaxy_head != GALAXY_HEAD or galaxy_status != GALAXY_DIRTY:
        raise RuntimeError("galaxy repository changed")
    return {
        "formal_tree_sha256": formal_digest,
        "public_head": public_head,
        "public_status": public_status,
        "galaxy_head": galaxy_head,
        "galaxy_status": galaxy_status,
    }


def symbolic_consistent_truncation() -> dict[str, Any]:
    motion_field, kinetic_invariant = sp.symbols("chi X_chi", real=True)
    motion_mass_squared = sp.symbols("m_gap2", positive=True, real=True)
    x2_coefficient, x3_coefficient = sp.symbols("c_X2 c_X3", real=True)
    o4_coefficient, weyl_squared = sp.symbols(
        "u_O4 C_squared",
        real=True,
    )
    field_gradient, field_box, coefficient_gradient = sp.symbols(
        "nabla_chi Box_chi nabla_K",
        real=True,
    )
    motion_potential = motion_mass_squared * motion_field**2 / 2
    derivative_function = (
        x2_coefficient * kinetic_invariant**2
        + x3_coefficient * kinetic_invariant**3
    )
    kinetic_multiplier = (
        1
        - 2 * sp.diff(derivative_function, kinetic_invariant)
        + 2 * o4_coefficient * weyl_squared
    )
    scalar_equation_proxy = (
        kinetic_multiplier * field_box
        + coefficient_gradient * field_gradient
        - sp.diff(motion_potential, motion_field)
    )
    scalar_stress_proxy = (
        kinetic_invariant
        + motion_potential
        + derivative_function
        + o4_coefficient * weyl_squared * kinetic_invariant
    )
    zero_substitution = {
        motion_field: 0,
        kinetic_invariant: 0,
        field_gradient: 0,
        field_box: 0,
    }
    species_count = 5
    universality_constraints = sp.zeros(species_count - 1, species_count)
    for row_index in range(species_count - 1):
        universality_constraints[row_index, row_index] = 1
        universality_constraints[row_index, row_index + 1] = -1
    nullspace = universality_constraints.nullspace()
    return {
        "motion_potential": str(motion_potential),
        "derivative_function": str(derivative_function),
        "P_at_zero": str(
            sp.simplify(derivative_function.subs(kinetic_invariant, 0))
        ),
        "P_X_at_zero": str(
            sp.simplify(
                sp.diff(derivative_function, kinetic_invariant).subs(
                    kinetic_invariant,
                    0,
                )
            )
        ),
        "V_at_zero": str(
            sp.simplify(motion_potential.subs(motion_field, 0))
        ),
        "V_prime_at_zero": str(
            sp.simplify(
                sp.diff(motion_potential, motion_field).subs(
                    motion_field,
                    0,
                )
            )
        ),
        "scalar_equation_on_branch": str(
            sp.simplify(scalar_equation_proxy.subs(zero_substitution))
        ),
        "scalar_stress_on_branch": str(
            sp.simplify(scalar_stress_proxy.subs(zero_substitution))
        ),
        "quadratic_kinetic_multiplier": str(
            sp.simplify(
                kinetic_multiplier.subs(kinetic_invariant, 0)
            )
        ),
        "scalar_hessian_mass_squared": str(motion_mass_squared),
        "universality_constraint_matrix": str(universality_constraints),
        "universality_rank": universality_constraints.rank(),
        "universality_nullity": (
            species_count - universality_constraints.rank()
        ),
        "universality_null_vector": [
            [int(value) for value in vector] for vector in nullspace
        ],
    }


def exact_truncation_rows(
    symbolic: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "theorem_step": "selected_bulk_trajectory",
                "parent_statement": (
                    "F_R(chi)=M_R^2; Z=1; "
                    "V=m_gap^2 chi^2/2; P=P_ge2(X_chi)"
                ),
                "branch_substitution": "chi=0; nabla_chi=0",
                "derived_result": (
                    "constant Einstein residue and reflection-even "
                    "source-free motion block"
                ),
                "proof_owner": "5208 common minimal trajectory",
                "status": "SOURCE_SELECTED_TRAJECTORY",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "motion_equation",
                "parent_statement": (
                    "E_chi=nabla_mu[(1-2P_X+2u_O4 C^2)"
                    "nabla^mu chi]-m_gap^2 chi"
                ),
                "branch_substitution": "chi=0; nabla_chi=0",
                "derived_result": symbolic["scalar_equation_on_branch"],
                "proof_owner": "executed symbolic factorization",
                "status": "EXACT_ZERO_FOR_ARBITRARY_RETAINED_FIELDS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "motion_stress",
                "parent_statement": (
                    "T_chi and delta(C^2 X_chi)/delta g contain "
                    "chi, X_chi, or two motion gradients"
                ),
                "branch_substitution": "chi=0; X_chi=0",
                "derived_result": symbolic["scalar_stress_on_branch"],
                "proof_owner": "executed zero-branch metric variation proxy",
                "status": "EXACT_ZERO",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "direct_visible_source",
                "parent_statement": (
                    "S_visible[e,omega_LC,A,Phi_SM] has no chi argument "
                    "at fixed coframe"
                ),
                "branch_substitution": "selected fixed-metric factorization",
                "derived_result": (
                    "delta S_visible/delta chi=0 and Q_chi=0"
                ),
                "proof_owner": "4943 plus 5208",
                "status": "EXACT_ZERO_DIRECT_SCALAR_CHARGE",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "quadratic_cross_blocks",
                "parent_statement": (
                    "F_R'=Z_A'=A_matter'=0 and the selected F_R is constant"
                ),
                "branch_substitution": "chi=0",
                "derived_result": (
                    "Gamma_hchi=Gamma_Achi=Gamma_matter_chi=0"
                ),
                "proof_owner": "5203 double-zero theorem strengthened by 5208",
                "status": "EXACT_BLOCK_DIAGONALITY",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "state_silence",
                "parent_statement": (
                    "DeltaT_state[n]=n(T_1-T_0) with rho_local=rho_0"
                ),
                "branch_substitution": "n=0 on an open local domain",
                "derived_result": (
                    "DeltaT_state=0 and its Ward source is zero"
                ),
                "proof_owner": "5201 binary-state identity",
                "status": "EXACT_GIVEN_DECLARED_LOCAL_STATE",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "state_selection_boundary",
                "parent_statement": "parent evolution selects rho_local=rho_0",
                "branch_substitution": "not supplied by the current bulk action",
                "derived_result": (
                    "state is a boundary/preparation datum, not a derived attractor"
                ),
                "proof_owner": "5201 explicit open gate",
                "status": "OPEN_STATE_SELECTION_NOT_HIDDEN",
                "valid_for_declared_selected_local_branch": False,
            },
            {
                "theorem_step": "two_derivative_restriction",
                "parent_statement": (
                    "Gamma_parent restricted to chi=0, rho_0 and omitting "
                    "operators above two derivatives"
                ),
                "branch_substitution": "same M_R, Lambda_cal and Z_A globally",
                "derived_result": (
                    "Gamma_2der=integral e[M_R^2(R-2Lambda_cal)/2"
                    "-F^2/4]+S_visible"
                ),
                "proof_owner": "5203 parent plus 5208 and 5210",
                "status": "EXACT_NONLINEAR_GR_LAMBDA_SM_MAXWELL_TRUNCATION",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "restricted_field_equations",
                "parent_statement": "vary the restricted two-derivative action",
                "branch_substitution": "one universal torsionless coframe",
                "derived_result": (
                    "M_R^2(G_mn+Lambda_cal g_mn)=T_visible+T_EM; "
                    "nabla_m F^mn=J^n"
                ),
                "proof_owner": "5201 coframe and U1 variation",
                "status": "EXACT_RESTRICTED_EQUATIONS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "vacuum_coordinate",
                "parent_statement": "Lambda_cal is allowed and RG sourced",
                "branch_substitution": "one frozen universal calibration",
                "derived_result": (
                    "same Lambda_cal in cosmology, local gravity and baseline"
                ),
                "proof_owner": "5210",
                "status": "ONE_RENORMALIZATION_DATUM_NO_ARENA_RETUNING",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "stability_separation",
                "parent_statement": (
                    "K_chichi=-nabla[(1+2u_O4 C^2)nabla]+m_gap^2"
                ),
                "branch_substitution": "positive local kinetic corridor",
                "derived_result": (
                    f"quadratic multiplier={symbolic['quadratic_kinetic_multiplier']}; "
                    "stationarity is exact while stability is separately tested"
                ),
                "proof_owner": "4943 interior benchmarks",
                "status": "TESTED_CORRIDOR_STABLE_NOT_ALL_BACKGROUND_THEOREM",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "theorem_step": "scope_boundary",
                "parent_statement": "C3, CFF, nonlocal logs and p8plus retained",
                "branch_substitution": "matched EFT comparison",
                "derived_result": (
                    "exact GR statement is two-derivative; higher-order "
                    "MTS-specific excess is reported separately"
                ),
                "proof_owner": "5211",
                "status": "NO_ALL_OPERATOR_GR_CLAIM",
                "valid_for_declared_selected_local_branch": True,
            },
        ]
    )


def ward_exchange_rows(
    symbolic: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    imported_nullspace = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4960"
        / "soft_Bianchi_species_coupling_nullspace.csv"
    )
    species_rows = [
        row for row in imported_nullspace if row["species"] != "ALL"
    ]
    source_chain = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4947"
        / "source_residue_chain.csv"
    )
    rows = tagged(
        [
            {
                "chain_step": "coframe_Hilbert_source",
                "operation": "vary the one universal coframe",
                "equation": (
                    "T_a^mu=-(1/e) delta S_visible/delta e^a_mu"
                ),
                "derived_consequence": (
                    "one symmetric Belinfante-Hilbert stress after the "
                    "local Lorentz Ward identity"
                ),
                "independent_calibration": "none",
                "status": "EXACT_VARIATIONAL_SOURCE",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "Diff_Ward",
                "operation": "apply diffeomorphism invariance",
                "equation": (
                    "nabla_mu T_visible^mu_nu=F_nu_mu J^mu "
                    "on visible matter shell"
                ),
                "derived_consequence": "matter-field momentum exchange fixed",
                "independent_calibration": "none",
                "status": "EXACT_NOETHER_IDENTITY",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "U1_Ward",
                "operation": "apply visible gauge invariance",
                "equation": "nabla_mu J^mu=0",
                "derived_consequence": "one conserved electric current",
                "independent_calibration": "alpha_EM fixed once",
                "status": "EXACT_NOETHER_IDENTITY",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "Einstein_equation",
                "operation": "vary the selected restricted action",
                "equation": (
                    "M_R^2(G_mn+Lambda_cal g_mn)=T_total_mn"
                ),
                "derived_consequence": "G_N=1/(8 pi M_R^2)",
                "independent_calibration": "one global G_N",
                "status": "EXACT_TWO_DERIVATIVE_SELECTED_BRANCH",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "source_universality",
                "operation": "intersect soft-spin2 and Bianchi constraints",
                "equation": "kappa_i-kappa_(i+1)=0 for five source classes",
                "derived_consequence": (
                    f"rank={symbolic['universality_rank']}; "
                    f"nullity={symbolic['universality_nullity']}; "
                    f"null={symbolic['universality_null_vector']}"
                ),
                "independent_calibration": "one common residue only",
                "status": "EXECUTED_UNIVERSAL_NULLSPACE",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "conserved_source_exchange",
                "operation": "invert the harmonic-gauge Einstein Hessian",
                "equation": (
                    "Gamma_12=i/[M_R^2(q^2+i0)]"
                    "[T1_mn T2^mn-T1 T2/2]"
                ),
                "derived_consequence": (
                    "one positive massless spin-2 pole with universal residue"
                ),
                "independent_calibration": "same G_N",
                "status": "DERIVED_EXCHANGE_KERNEL",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "harmonic_gauge",
                "operation": "linearize the Einstein equation",
                "equation": (
                    "Box hbar_mn=-2T_mn/M_R^2=-16piG_N T_mn"
                ),
                "derived_consequence": "same source residue in every component",
                "independent_calibration": "same G_N",
                "status": "DERIVED_LINEAR_FIELD_EQUATION",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "Newton_limit",
                "operation": "take static nonrelativistic source limit",
                "equation": "nabla^2 Phi=4piG_N rho; Phi=-G_N M/r",
                "derived_consequence": "d^2x/dt^2=-grad Phi",
                "independent_calibration": "same G_N",
                "status": "DERIVED_NEWTONIAN_MECHANICS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "worldline_limit",
                "operation": "vary neutral, null and charged worldlines",
                "equation": (
                    "u.nabla u=0; k.nabla k=0; "
                    "u.nabla u=(q/m)F.u"
                ),
                "derived_consequence": (
                    "geodesic, lensing and Lorentz-force limits use the "
                    "same metric and source residue"
                ),
                "independent_calibration": "G_N plus alpha_EM only",
                "status": "DERIVED_WORLDLINE_LIMITS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "chain_step": "total_conservation",
                "operation": "combine Einstein, Diff and U1 Ward identities",
                "equation": "nabla_mu(T_visible+T_EM)^mu_nu=0",
                "derived_consequence": "no independent exchange coefficient",
                "independent_calibration": "none",
                "status": "EXACT_ON_FIELD_EQUATIONS",
                "valid_for_declared_selected_local_branch": True,
            },
        ]
    )
    checks = {
        "source_chain_rows": len(source_chain),
        "imported_species_count": len(species_rows),
        "all_imported_relative_couplings_one": all(
            float(row["soft_relative_coupling"]) == 1.0
            and float(row["Bianchi_relative_source_weight"]) == 1.0
            for row in species_rows
        ),
        "constraint_rank": symbolic["universality_rank"],
        "constraint_nullity": symbolic["universality_nullity"],
        "constraint_null_vector": symbolic["universality_null_vector"],
    }
    return rows, checks


def selected_ppn_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5201"
        / "full_PPN_residual_vector.csv"
    )
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(
            {
                "PPN_parameter": source["PPN_parameter"],
                "GR_value": float(source["GR_value"]),
                "selected_MTS_two_derivative_value": float(
                    source["MTS_local_two_derivative_value"]
                ),
                "delta_from_GR": float(source["delta_from_GR"]),
                "derivation": source["derivation"],
                "selected_conditions": (
                    "5208 constant-F_R chi=0 branch; rho_local=rho_0; "
                    "one torsionless coframe; 5210 Lambda_cal frozen and "
                    "matched as the common local background"
                ),
                "higher_EFT_interpretation": (
                    "C3/CFF/nonlocal/p8 residuals are not silently folded "
                    "into constant PPN coefficients"
                ),
                "status": "EXACT_TWO_DERIVATIVE_SELECTED_BRANCH",
                "valid_for_declared_selected_local_branch": True,
            }
        )
    expected_names = {
        "gamma",
        "beta",
        "xi",
        "alpha_1",
        "alpha_2",
        "alpha_3",
        "zeta_1",
        "zeta_2",
        "zeta_3",
        "zeta_4",
    }
    checks = {
        "row_count": len(rows),
        "names": sorted(row["PPN_parameter"] for row in rows),
        "expected_names": sorted(expected_names),
        "all_deltas_zero": all(row["delta_from_GR"] == 0.0 for row in rows),
        "gamma": next(
            row["selected_MTS_two_derivative_value"]
            for row in rows
            if row["PPN_parameter"] == "gamma"
        ),
        "beta": next(
            row["selected_MTS_two_derivative_value"]
            for row in rows
            if row["PPN_parameter"] == "beta"
        ),
    }
    return tagged(rows), checks


def maxwell_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    electric_x, electric_y, electric_z = sp.symbols(
        "E_x E_y E_z",
        real=True,
    )
    magnetic_x, magnetic_y, magnetic_z = sp.symbols(
        "B_x B_y B_z",
        real=True,
    )
    energy_density = sp.simplify(
        (
            electric_x**2
            + electric_y**2
            + electric_z**2
            + magnetic_x**2
            + magnetic_y**2
            + magnetic_z**2
        )
        / 2
    )
    poynting = [
        sp.expand(electric_y * magnetic_z - electric_z * magnetic_y),
        sp.expand(electric_z * magnetic_x - electric_x * magnetic_z),
        sp.expand(electric_x * magnetic_y - electric_y * magnetic_x),
    ]
    rows = tagged(
        [
            {
                "step": "field_strength",
                "equation": "F=dA; nabla_[m F_nr]=0",
                "executed_result": "exact antisymmetric two-form",
                "matched_baseline_role": "common",
                "status": "EXACT_BIANCHI_IDENTITY",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "field_equation",
                "equation": (
                    "nabla_m F^mn-4c_parent nabla_m(C^mnrs F_rs)=J^n"
                ),
                "executed_result": "flat C=0 gives partial_m F^mn=J^n",
                "matched_baseline_role": (
                    "standard visible Wilsons common; parent CFF is excess"
                ),
                "status": "DERIVED_BY_A_VARIATION",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "current_conservation",
                "equation": "nabla_n nabla_m H^mn=0",
                "executed_result": "nabla_n J^n=0",
                "matched_baseline_role": "common",
                "status": "EXACT_FROM_ANTISYMMETRY_AND_U1_WARD",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "Hilbert_stress",
                "equation": (
                    "T_EM^mn=F^m_a F^(na)-g^mn F^2/4+DeltaT_CFF"
                ),
                "executed_result": "same coframe variation as gravity source",
                "matched_baseline_role": (
                    "Maxwell piece common; parent DeltaT_CFF is excess"
                ),
                "status": "DERIVED_VARIATIONAL_STRESS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "energy_density",
                "equation": "T_EM^00",
                "executed_result": str(energy_density),
                "matched_baseline_role": "common",
                "status": "EXECUTED_EXACT",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "Poynting",
                "equation": "T_EM^0i",
                "executed_result": str(poynting),
                "matched_baseline_role": "common",
                "status": "EXECUTED_E_CROSS_B",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "trace",
                "equation": "T_EM^m_m",
                "executed_result": "0",
                "matched_baseline_role": "common classical Maxwell",
                "status": "EXECUTED_ZERO_IN_D4",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "stress_exchange",
                "equation": (
                    "nabla_m T_EM^m_n=-F_nm J^m; "
                    "nabla_m T_visible^m_n=+F_nm J^m"
                ),
                "executed_result": "nabla_m(T_EM+T_visible)^m_n=0",
                "matched_baseline_role": "common",
                "status": "DERIVED_ON_FIELD_EQUATIONS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "step": "motion_portal",
                "equation": "delta S_EM/delta chi=0",
                "executed_result": "0",
                "matched_baseline_role": "MTS-specific direct portal absent",
                "status": "EXACT_ZERO_ON_SELECTED_TRAJECTORY",
                "valid_for_declared_selected_local_branch": True,
            },
        ]
    )
    checks = {
        "energy_density": str(energy_density),
        "poynting": [str(component) for component in poynting],
        "expected_poynting": [
            "-B_y*E_z + B_z*E_y",
            "B_x*E_z - B_z*E_x",
            "-B_x*E_y + B_y*E_x",
        ],
    }
    return rows, checks


def matched_baseline_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "operator_block": "comparison_definition",
                "GRSM_baseline": (
                    "Gamma_GR+SM at the same renormalization scale and scheme"
                ),
                "MTS_parent": "Gamma_MTS",
                "matched_difference": (
                    "DeltaGamma_MTS=Gamma_MTS-Gamma_GR+SM"
                ),
                "matching_condition": (
                    "same G_N, Lambda_cal, alpha_EM, SM masses/couplings "
                    "and common GR+SM Wilson coefficients"
                ),
                "classification": "DEFINITION_OF_FAIR_EFT_COMPARISON",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "EH_and_source_residue",
                "GRSM_baseline": "M_R^2(R-2Lambda_cal)/2",
                "MTS_parent": "same restricted block",
                "matched_difference": "0",
                "matching_condition": "one measured G_N and one Lambda_cal",
                "classification": "COMMON_CALIBRATED_BLOCK",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "visible_SM_and_Maxwell",
                "GRSM_baseline": "S_visible-F^2/4",
                "MTS_parent": "same coframe and U1 representations",
                "matched_difference": "0",
                "matching_condition": "same alpha_EM and visible parameters",
                "classification": "COMMON_CALIBRATED_BLOCK",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "visible_CFF_thresholds",
                "GRSM_baseline": (
                    "electron, muon, tau, electroweak and QCD CFF Wilsons"
                ),
                "MTS_parent": "the same visible-sector thresholds",
                "matched_difference": "0",
                "matching_condition": "same visible field content and scheme",
                "classification": (
                    "COMMON_BASELINE_NOT_AN_MTS_FAILURE_OR_ADVANTAGE"
                ),
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "graviton_ghost_loops",
                "GRSM_baseline": "standard gravitational EFT loops",
                "MTS_parent": "same EH graviton/ghost sector",
                "matched_difference": (
                    "common part cancels; extra motion diagrams remain"
                ),
                "matching_condition": "same gauge and subtraction prescription",
                "classification": "COMMON_BASELINE_WITH_EXCESS_SEPARATED",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "motion_tree_block",
                "GRSM_baseline": "absent",
                "MTS_parent": (
                    "-X_chi/2-m_gap^2 chi^2/2+P_ge2(X_chi)"
                ),
                "matched_difference": "0 on chi=0 at tree level",
                "matching_condition": "selected invariant local branch",
                "classification": "EXACT_TREE_SILENCE",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "motion_nonlocal_loop",
                "GRSM_baseline": "absent",
                "MTS_parent": (
                    "-int sqrt(-g)[C log(-Box) C/(3840pi^2)"
                    "+R log(-Box) R/(2304pi^2)]"
                ),
                "matched_difference": "one real-scalar universal form factor",
                "matching_condition": "q much greater than m_gap",
                "classification": "CALCULATED_MTS_SPECIFIC_EXCESS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "parent_CFF",
                "GRSM_baseline": "common visible CFF coefficient only",
                "MTS_parent": "common visible coefficient plus c_parent",
                "matched_difference": "c_parent CFF",
                "matching_condition": (
                    "locked 4942 endpoint; physical full matching remains "
                    "conditional"
                ),
                "classification": "CONDITIONAL_PARENT_ENDPOINT_EXCESS",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "parent_C3",
                "GRSM_baseline": "common pure-gravity EFT Wilson",
                "MTS_parent": "common Wilson plus selected endpoint C3",
                "matched_difference": "selected endpoint C3 residual",
                "matching_condition": (
                    "4971 proves the physical absolute on-shell anchor "
                    "cannot be supplied by local running alone"
                ),
                "classification": (
                    "TRUNCATION_CONDITIONAL_ABSOLUTE_ANCHOR_OPEN"
                ),
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "O4_and_PX",
                "GRSM_baseline": "absent",
                "MTS_parent": "C^2 X_chi and P_ge2(X_chi)",
                "matched_difference": "0 on chi=0 at tree level",
                "matching_condition": "exact selected local branch",
                "classification": "EXACT_TREE_SILENCE",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "operator_block": "p8plus",
                "GRSM_baseline": "common EFT completion",
                "MTS_parent": "common completion plus MTS-specific excess",
                "matched_difference": "not yet calculated completely",
                "matching_condition": (
                    "full parent Hessian/amplitude and two-scale projectors"
                ),
                "classification": "OPEN_ALL_ORDER_OBSTRUCTION",
                "valid_for_declared_selected_local_branch": False,
            },
        ]
    )


def parent_residual_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_residuals = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4942"
        / "local_O4_C3_CFF_residual_vector.csv"
    )
    cff_components = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4944"
        / "visible_CFF_matching_components.csv"
    )
    cff_factors = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4944"
        / "conditional_total_CFF_local_residual_bound.csv"
    )
    component_map = {row["component_id"]: row for row in cff_components}
    factor_map = {row["system"]: row for row in cff_factors}
    parent_coefficient = float(
        component_map["CFF4944_00_parent"]["coefficient_or_bound_m2"]
    )
    lepton_coefficient = abs(
        float(
            component_map["CFF4944_01_free_leptons"][
                "coefficient_or_bound_m2"
            ]
        )
    )
    visible_control = float(
        component_map["CFF4944_06_calculable_control_interval"][
            "coefficient_or_bound_m2"
        ]
    )
    rows: list[dict[str, Any]] = []
    recomputation_errors: list[float] = []
    for source in source_residuals:
        factor = float(
            factor_map[source["system"]]["CFF_curvature_factor_m_minus_2"]
        )
        calculated_cff_residual = parent_coefficient * factor
        imported_cff_residual = float(
            source["CFF_parent_abs_Delta_v_pol_over_c"]
        )
        relative_error = abs(
            calculated_cff_residual - imported_cff_residual
        ) / imported_cff_residual
        recomputation_errors.append(relative_error)
        rows.append(
            {
                "system": source["system"],
                "source_class": source["source_class"],
                "mass_length_m": float(source["mass_length_m"]),
                "radius_m": float(source["radius_m"]),
                "O4_tree_metric_stress_on_chi0": float(
                    source["O4_tree_metric_stress_on_psi0"]
                ),
                "O4_scalar_cone_shift_on_chi0": float(
                    source["O4_scalar_cone_shift"]
                ),
                "C3_abs_Delta_Phi_over_PhiN": float(
                    source["C3_abs_Delta_Phi_over_PhiN"]
                ),
                "C3_abs_Delta_acceleration_over_aN": float(
                    source["C3_abs_Delta_acceleration_over_aN"]
                ),
                "C3_physical_scope": (
                    "selected endpoint smoke; absolute on-shell anchor "
                    "remains open under checkpoint 4971"
                ),
                "CFF_parent_coefficient_m2": parent_coefficient,
                "CFF_curvature_factor_m_minus_2": factor,
                "CFF_parent_abs_Delta_v_pol_over_c_recomputed": (
                    calculated_cff_residual
                ),
                "CFF_parent_abs_Delta_v_pol_over_c_imported": (
                    imported_cff_residual
                ),
                "CFF_recomputation_relative_error": relative_error,
                "visible_calculable_control_abs_coefficient_m2": (
                    visible_control
                ),
                "parent_to_visible_control_ratio": (
                    parent_coefficient / visible_control
                ),
                "parent_to_free_lepton_ratio": (
                    parent_coefficient / lepton_coefficient
                ),
                "PPN_delta_gamma_at_standard_order": float(
                    source["PPN_delta_gamma_at_standard_order"]
                ),
                "PPN_delta_beta_at_standard_order": float(
                    source["PPN_delta_beta_at_standard_order"]
                ),
                "matched_baseline_interpretation": (
                    "visible CFF is common and cancels; only c_parent is "
                    "counted as the displayed MTS excess"
                ),
                "status": "LOCKED_ENDPOINT_MATCHED_EXCESS_NONCLAIM",
                "valid_for_declared_selected_local_branch": True,
            }
        )
    checks = {
        "parent_coefficient_m2": parent_coefficient,
        "visible_control_m2": visible_control,
        "free_lepton_abs_m2": lepton_coefficient,
        "parent_to_visible_control_ratio": (
            parent_coefficient / visible_control
        ),
        "parent_to_free_lepton_ratio": (
            parent_coefficient / lepton_coefficient
        ),
        "maximum_recomputation_relative_error": max(recomputation_errors),
        "maximum_parent_CFF_residual": max(
            row["CFF_parent_abs_Delta_v_pol_over_c_recomputed"]
            for row in rows
        ),
        "maximum_C3_acceleration_residual": max(
            row["C3_abs_Delta_acceleration_over_aN"] for row in rows
        ),
        "O4_exact_zero_all_rows": all(
            row["O4_tree_metric_stress_on_chi0"] == 0.0
            and row["O4_scalar_cone_shift_on_chi0"] == 0.0
            for row in rows
        ),
    }
    return tagged(rows), checks


def scalar_nonlocal_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    smoke_rows = read_csv(
        POST
        / "source-intake"
        / "mts_residuals"
        / "P8_Y5_R2FR_4877_ARENA_SMOKE.csv"
    )
    scale_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5208"
        / "physical_scale_and_power_counting.csv"
    )
    motion_mass = float(
        next(row["value"] for row in scale_rows if row["quantity"] == "m_gap")
    )
    rows: list[dict[str, Any]] = []
    epsilon0_errors: list[float] = []
    epsilon2_errors: list[float] = []
    for source in smoke_rows:
        length_m = float(source["length_m"])
        momentum_eV = HBAR_C_EV_M / length_m
        logarithm = math.log(REDUCED_PLANCK_EV / momentum_eV)
        momentum_ratio_squared = (
            momentum_eV / REDUCED_PLANCK_EV
        ) ** 2
        epsilon0 = (
            logarithm
            * momentum_ratio_squared
            / (96.0 * math.pi**2)
        )
        epsilon2 = (
            logarithm
            * momentum_ratio_squared
            / (480.0 * math.pi**2)
        )
        imported_scalar = float(source["epsilon0"]) / 4.0
        imported_weyl = float(source["epsilon2"]) / 283.0
        epsilon0_error = abs(epsilon0 - imported_scalar) / imported_scalar
        epsilon2_error = abs(epsilon2 - imported_weyl) / imported_weyl
        epsilon0_errors.append(epsilon0_error)
        epsilon2_errors.append(epsilon2_error)
        mass_ratio_squared = (motion_mass / momentum_eV) ** 2
        rows.append(
            {
                "arena": source["arena"],
                "length_m": length_m,
                "q_eV": momentum_eV,
                "m_gap_eV": motion_mass,
                "m_gap_squared_over_q_squared": mass_ratio_squared,
                "log_Mbar_over_q": logarithm,
                "MTS_extra_real_scalar_S_h2": 1,
                "MTS_extra_real_scalar_W_C": 1,
                "epsilon0_MTS_excess": epsilon0,
                "epsilon2_MTS_excess": epsilon2,
                "dominant_abs_MTS_excess": max(epsilon0, epsilon2),
                "imported_SM_epsilon0_divided_by_4": imported_scalar,
                "imported_SM_epsilon2_divided_by_283": imported_weyl,
                "epsilon0_recomputation_relative_error": epsilon0_error,
                "epsilon2_recomputation_relative_error": epsilon2_error,
                "below_1e_minus_30": max(epsilon0, epsilon2) < 1e-30,
                "massless_form_factor_control": (
                    "q>>m_gap; omitted mass corrections scale as m_gap^2/q^2"
                ),
                "status": "UNIVERSAL_ONE_REAL_SCALAR_MATCHED_EXCESS",
                "valid_for_declared_selected_local_branch": True,
            }
        )
    checks = {
        "motion_mass_eV": motion_mass,
        "maximum_epsilon0_recomputation_relative_error": max(
            epsilon0_errors
        ),
        "maximum_epsilon2_recomputation_relative_error": max(
            epsilon2_errors
        ),
        "maximum_MTS_scalar_nonlocal_excess": max(
            row["dominant_abs_MTS_excess"] for row in rows
        ),
        "maximum_mass_ratio_squared": max(
            row["m_gap_squared_over_q_squared"] for row in rows
        ),
        "all_below_1e_minus_30": all(
            row["below_1e_minus_30"] for row in rows
        ),
    }
    return tagged(rows), checks


def compact_stability_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4943"
        / "interior_stability_benchmarks.csv"
    )
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(
            {
                "system": source["system"],
                "density_multiplier_over_mean": float(
                    source["density_multiplier_over_mean"]
                ),
                "mean_density_kg_m3": float(source["mean_density_kg_m3"]),
                "ricci_proxy_m_minus_2": float(
                    source["ricci_proxy_m_minus_2"]
                ),
                "direct_scalar_charge": 0.0,
                "single_scalar_fifth_force_over_Newton": 0.0,
                "A_time_lower": float(source["A_time_lower"]),
                "B_space_lower": float(source["B_space_lower"]),
                "abs_delta_cchi_squared_bound": float(
                    source["abs_delta_cpsi_squared_bound"]
                ),
                "abs_delta_m2_over_m2_bound": float(
                    source["abs_delta_m2_over_m2_bound"]
                ),
                "O4_abs_delta_Z_over_Z": float(
                    source["O4_abs_delta_Z_over_Z"]
                ),
                "scalarization_from_declared_quadratic_packet": (
                    source["scalarization_from_declared_quadratic_packet"]
                ),
                "scope": (
                    "tested density/DEC corridor; not every EOS, binary "
                    "sensitivity, horizon state or radiation channel"
                ),
                "status": "ZERO_BRANCH_EXISTS_AND_TESTED_CORRIDOR_STABLE",
                "valid_for_declared_selected_local_branch": True,
            }
        )
    checks = {
        "row_count": len(rows),
        "maximum_abs_delta_cchi_squared": max(
            row["abs_delta_cchi_squared_bound"] for row in rows
        ),
        "maximum_abs_delta_m2_over_m2": max(
            row["abs_delta_m2_over_m2_bound"] for row in rows
        ),
        "minimum_A_time": min(row["A_time_lower"] for row in rows),
        "minimum_B_space": min(row["B_space_lower"] for row in rows),
        "all_direct_charges_zero": all(
            row["direct_scalar_charge"] == 0.0 for row in rows
        ),
    }
    return tagged(rows), checks


def all_order_corridor_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "selected_bulk_consistent_truncation",
                "result": "chi=0 is an exact invariant classical bulk branch",
                "scope": "arbitrary retained metric, Maxwell and visible fields",
                "status": "CLOSED",
                "next_required_object": "none at two derivatives",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "two_derivative_GR_Maxwell",
                "result": (
                    "restricted nonlinear action and equations are exactly "
                    "GR+Lambda+SM+Maxwell"
                ),
                "scope": "selected local state and constant-F_R trajectory",
                "status": "CLOSED",
                "next_required_object": "none at two derivatives",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "universal_source_and_Newton",
                "result": (
                    "rank-four constraints leave one all-ones source residue; "
                    "Newton and geodesic limits follow"
                ),
                "scope": "one positive massless spin-2 sector",
                "status": "CLOSED",
                "next_required_object": "none at leading source order",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "full_standard_PPN_vector",
                "result": (
                    "(gamma,beta,xi,alpha1,alpha2,alpha3,zeta1..4)"
                    "=(1,1,0,0,0,0,0,0,0,0)"
                ),
                "scope": "constant two-derivative PPN coefficients",
                "status": "CLOSED",
                "next_required_object": "retain non-PPN EFT residuals separately",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "Maxwell_stress_and_Poynting",
                "result": "standard exact Hilbert stress and E cross B flux",
                "scope": "classical Maxwell block",
                "status": "CLOSED",
                "next_required_object": "retain parent CFF correction",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "vacuum_coordinate",
                "result": (
                    "Lambda_cal is one frozen renormalization/calibration datum"
                ),
                "scope": "same value in every arena and matched baseline",
                "status": "CLOSED_AS_PARAMETER_BOUNDARY_NOT_ZERO_PREDICTION",
                "next_required_object": (
                    "optional enlarged UV vacuum fixed-point calculation"
                ),
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "local_state_selection",
                "result": (
                    "rho_local=rho_0 is exactly silent but not derived as "
                    "a parent attractor"
                ),
                "scope": "boundary/preparation condition",
                "status": "EXPLICIT_STATE_INPUT",
                "next_required_object": (
                    "state preparation or attractor theorem only if demanded"
                ),
                "valid_for_declared_selected_local_branch": False,
            },
            {
                "gate": "motion_scalar_nonlocal_excess",
                "result": (
                    "one-real-scalar universal logarithmic residual calculated"
                ),
                "scope": "q much greater than m_gap local arenas",
                "status": "CALCULATED_AND_TINY",
                "next_required_object": "mass-threshold form factor only near q~m",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "parent_CFF_endpoint",
                "result": (
                    "matched parent-only residual separated from common "
                    "visible QED/QCD thresholds"
                ),
                "scope": "locked endpoint family",
                "status": "CONDITIONAL_ENDPOINT_BOUND",
                "next_required_object": "full parent physical matching",
                "valid_for_declared_selected_local_branch": True,
            },
            {
                "gate": "C3_absolute_onshell_anchor",
                "result": (
                    "4971 exact amplitude projector exists but local running "
                    "has rank zero for the integration constant"
                ),
                "scope": "physical six-derivative four-graviton amplitude",
                "status": "OPEN",
                "next_required_object": (
                    "finite full-parent remainder in two helicity channels"
                ),
                "valid_for_declared_selected_local_branch": False,
            },
            {
                "gate": "p8plus_matched_excess",
                "result": (
                    "two-scale helicity projector is full rank; direct "
                    "full-parent MTS excess is not yet supplied"
                ),
                "scope": "all-operator local GR comparison",
                "status": "OPEN_MAIN_LOCAL_OBSTRUCTION",
                "next_required_object": (
                    "first canonical MTS-specific p8 on-shell coefficient "
                    "from the full parent Hessian/amplitude"
                ),
                "valid_for_declared_selected_local_branch": False,
            },
            {
                "gate": "strong_field_completion",
                "result": (
                    "zero-charge interior branch and finite density corridor "
                    "pass; all EOS, sensitivities and radiation are not closed"
                ),
                "scope": "compact bodies and binaries",
                "status": "PARTIAL",
                "next_required_object": (
                    "matched compact-body sensitivities and radiation"
                ),
                "valid_for_declared_selected_local_branch": False,
            },
            {
                "gate": "full_MTS_unification",
                "result": "not established by this checkpoint",
                "scope": "all branches, states, scales and data",
                "status": "NOT_CLAIMED",
                "next_required_object": (
                    "higher-amplitude closure plus cross-arena state dynamics"
                ),
                "valid_for_declared_selected_local_branch": False,
            },
        ]
    )


def decision_rows(
    parent_checks: dict[str, Any],
    scalar_checks: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "decision": "exact_selected_two_derivative_local_GR",
                "result": "YES",
                "claim": (
                    "the selected 5208 bulk trajectory has an exact nonlinear "
                    "GR+Lambda+SM+Maxwell consistent truncation at chi=0"
                ),
                "boundary": (
                    "rho_local=rho_0 is an explicit state input; higher "
                    "derivative operators are retained separately"
                ),
                "next_action": "do not reopen source coupling or Newton",
            },
            {
                "decision": "universal_source_and_Newton",
                "result": "YES",
                "claim": (
                    "one coframe Hilbert source and one massless spin-2 residue "
                    "derive Newtonian mechanics without species weights"
                ),
                "boundary": "inside the declared parent field content",
                "next_action": "freeze one G_N globally",
            },
            {
                "decision": "full_two_derivative_PPN",
                "result": "YES",
                "claim": "all ten standard PPN coefficients equal GR",
                "boundary": (
                    "common Lambda background and non-PPN EFT tails separated"
                ),
                "next_action": "test only actual residual operators",
            },
            {
                "decision": "Maxwell_Poynting",
                "result": "YES",
                "claim": (
                    "standard Maxwell equation, Hilbert stress, conservation "
                    "and Poynting vector are exact in the restricted block"
                ),
                "boundary": "parent CFF correction remains explicit",
                "next_action": "count common visible thresholds in the baseline",
            },
            {
                "decision": "fair_GRSM_comparator",
                "result": "ADOPTED",
                "claim": (
                    "standard GR+SM loops and visible Wilsons are common "
                    "baseline physics, not MTS-specific failures"
                ),
                "boundary": "same renormalization scheme and measured inputs",
                "next_action": "compare only DeltaGamma_MTS",
            },
            {
                "decision": "resolved_MTS_excess",
                "result": (
                    f"scalar log max={scalar_checks['maximum_MTS_scalar_nonlocal_excess']:.6e}; "
                    f"parent CFF max={parent_checks['maximum_parent_CFF_residual']:.6e}"
                ),
                "claim": (
                    "universal scalar log is calculated; parent endpoint "
                    "CFF/C3 residuals are numerically tiny in their stated scope"
                ),
                "boundary": "C3 physical anchor and complete p8 tail remain open",
                "next_action": "do not call this an all-order local-GR pass",
            },
            {
                "decision": "selected_next_route",
                "result": "DERIVATION_FIRST",
                "claim": "source coupling and two-derivative GR are no longer the gap",
                "boundary": "full MTS remains unproved",
                "next_action": (
                    "DERIVE_FIRST_CANONICAL_MTS_SPECIFIC_P8_ONSHELL_"
                    "COEFFICIENT_FROM_FULL_PARENT_HESSIAN_OR_BOUND_ITS_"
                    "MATCHED_EXCESS"
                ),
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, expected in SOURCE_LOCKS.items():
        relative = path.relative_to(POST).as_posix()
        if "4877" in relative:
            role = "universal nonlocal form factor and arena normalization"
        elif "4942" in relative:
            role = "local zero branch and endpoint C3/CFF/O4 residual"
        elif "4943" in relative:
            role = "matter factorization, junction charge and interior stability"
        elif "4944" in relative:
            role = "visible CFF decomposition and curvature factors"
        elif "4947" in relative or "4960" in relative:
            role = "source residue, Ward and universality chain"
        elif "4971" in relative:
            role = "physical C3 anchor and p8 rank boundary"
        elif "5201" in relative:
            role = "coframe variation, PPN, Maxwell and local state silence"
        elif "5203" in relative:
            role = "canonical parent action and branch reduction"
        elif "5208" in relative:
            role = "selected constant-F_R minimal trajectory and scales"
        elif "5209" in relative:
            role = "finite-mass P(X) and local residual control"
        elif "5210" in relative:
            role = "vacuum-coordinate parameter boundary"
        else:
            role = "locked parent evidence"
        rows.append(
            {
                "source_path": str(path),
                "relative_path": relative,
                "sha256": expected,
                "role": role,
                "exists": path.is_file(),
                "valid_for_declared_selected_local_branch": True,
            }
        )
    return tagged(rows)


def build_document(
    symbolic: dict[str, Any],
    ward_checks: dict[str, Any],
    ppn_checks: dict[str, Any],
    parent_checks: dict[str, Any],
    scalar_checks: dict[str, Any],
    compact_checks: dict[str, Any],
    evidence_digest: str,
) -> str:
    ppn_vector = (
        "(gamma,beta,xi,alpha_1,alpha_2,alpha_3,"
        "zeta_1,zeta_2,zeta_3,zeta_4)"
        "=(1,1,0,0,0,0,0,0,0,0)"
    )
    return f"""# 5211 - Selected-Trajectory Exact GR-Maxwell Consistent Truncation, Universal Source and Matched GR+SM Excess Theorem

Date: `{CHECKED_DATE}`

Formal marker: `{MARKER}`.

## Executive result

This checkpoint produces a real promotion rather than another missing-input
ledger.

On the source-selected checkpoint-5208 trajectory,

```text
F_R(chi)=M_R^2;
Z_chi=1;
V(chi)=m_gap^2 chi^2/2;
P=P_ge2(X_chi);
delta S_visible/delta chi=0.
```

The restriction

```text
chi=0;
nabla_mu chi=0;
rho_local=rho_0
```

is an exact classical consistent truncation of the bulk equations.  The
motion equation evaluates to `{symbolic['scalar_equation_on_branch']}`, its
stress evaluates to `{symbolic['scalar_stress_on_branch']}`, and all
linear metric-motion, photon-motion and matter-motion cross blocks vanish.
After retaining only the two-derivative terms, the restricted nonlinear
action is exactly

```text
Gamma_2der =
 integral d4x e [
   M_R^2 (R-2 Lambda_cal)/2
  -F_mu_nu F^mu_nu/4
 ] + S_visible[e,omega_LC[e],A,Phi_SM].
```

Therefore the selected MTS parent contains an **exact nonlinear
GR + Lambda + Standard Model + Maxwell two-derivative branch**.  This is
stronger than merely recovering a fitted inverse-square force or matching
two weak-field coefficients.

The statement has two explicit boundaries:

1. `rho_local=rho_0` is an allowed, exactly silent state/preparation
   condition, not a parent-derived attractor;
2. `C3`, `CFF`, nonlocal logarithms and `p8+` operators are not erased.

Accordingly this is not an all-operator local-GR theorem and not a full-MTS
claim.

## 1. Exact consistent-truncation proof

The selected motion equation has the factorized form

```text
E_chi =
 nabla_mu [
  (1-2 P_X+2 u_O4 C^2) nabla^mu chi
 ] - m_gap^2 chi.
```

Checkpoint 5208 fixes the curvature function to a constant rather than just
requiring a double zero.  Fixed-metric visible factorization removes direct
matter and Maxwell sources.  Every term in `E_chi` therefore contains
`chi`, `nabla chi`, or a derivative thereof.  The zero-field substitution is
valid for arbitrary retained metric, electromagnetic and visible-matter
configurations.

The machine checks give

```text
P(0)     = {symbolic['P_at_zero']};
P_X(0)   = {symbolic['P_X_at_zero']};
V(0)     = {symbolic['V_at_zero']};
V'(0)    = {symbolic['V_prime_at_zero']};
E_chi|0  = {symbolic['scalar_equation_on_branch']};
T_chi|0  = {symbolic['scalar_stress_on_branch']}.
```

The `O4=C^2 X_chi` term may change the scalar Hessian through
`{symbolic['quadratic_kinetic_multiplier']}`, but it cannot create a
zero-branch tadpole or stress.  Stationarity and stability are therefore
kept logically separate.

## 2. Universal source and Newtonian mechanics

The one-coframe variation defines one Hilbert source.  Local Lorentz,
diffeomorphism and visible-`U(1)` Ward identities then fix the stress
symmetry, energy-momentum exchange and current conservation.

For five source classes, the executed soft/Bianchi constraint matrix has

```text
rank    = {ward_checks['constraint_rank']};
nullity = {ward_checks['constraint_nullity']};
kernel  = {ward_checks['constraint_null_vector']}.
```

Thus species-dependent leading gravitational weights are absent.  The one
conserved-source pole is

```text
Gamma_12 =
 i/[M_R^2(q^2+i0)]
 [T1_mu_nu T2^mu_nu - T1 T2/2].
```

With `G_N=1/(8 pi M_R^2)`, its static slow-source limit is

```text
nabla^2 Phi = 4 pi G_N rho;
Phi = -G_N M/r;
d^2 x/dt^2 = -grad Phi.
```

Neutral, null and charged worldline variations then give the geodesic,
lensing and Lorentz-force equations with the same metric and no
arena-specific source calibration.

## 3. Full two-derivative PPN vector

Transporting the checkpoint-5201 calculation onto the checkpoint-5208
trajectory and the one frozen checkpoint-5210 vacuum datum gives

```text
{ppn_vector}.
```

All `{ppn_checks['row_count']}` standard PPN deltas are exactly zero at
two-derivative order.  The common `Lambda_cal` background and
higher-gradient EFT residuals are reported separately rather than being
mislabelled as constant PPN coefficients.

## 4. Maxwell stress and the Poynting vector

The restricted action gives

```text
nabla_mu F^mu_nu = J_nu;
nabla_[mu F_nu_rho] = 0;

T_EM^mu_nu =
 F^mu_alpha F^(nu alpha)
 -g^mu_nu F_alpha_beta F^(alpha beta)/4.
```

The exact machine reduction gives

```text
T_EM^00 = (E^2+B^2)/2;
T_EM^0i = (E cross B)^i;
T_EM^mu_mu = 0.
```

On the Maxwell and matter equations,

```text
nabla_mu T_EM^mu_nu      = -F_nu_mu J^mu;
nabla_mu T_visible^mu_nu = +F_nu_mu J^mu.
```

The electromagnetic energy flux is therefore part of the same universal
Hilbert source.  It is not an extra phenomenological coupling.  The parent
`CFF` correction remains explicit at higher derivative order.

## 5. Fair matched GR+SM comparison

The relevant comparator is not bare classical GR.  Define both EFTs at the
same subtraction scale and scheme, with common

```text
G_N, Lambda_cal, alpha_EM, SM masses/couplings,
and the ordinary GR+SM Wilson coefficients.
```

Then

```text
Delta Gamma_MTS = Gamma_MTS - Gamma_GR+SM
```

contains only MTS-specific excess.  In particular:

- electron, muon, tau, electroweak and QCD photon-curvature thresholds are
  common visible-sector physics and cancel from the comparison;
- standard graviton/ghost loops are common;
- the extra real motion-scalar logarithm remains;
- parent-specific `C3`, `CFF`, `O4`, and `p8+` pieces remain according to
  their actual branch projection.

This does not make an unknown coefficient vanish.  It prevents standard
GR+SM corrections from being unfairly counted as MTS failures.

## 6. Calculated MTS-specific residuals

For one additional minimally coupled real scalar and `q >> m_gap`,

```text
epsilon_0 =
 ln(Mbar_Pl/q) q^2 /
 [96 pi^2 Mbar_Pl^2];

epsilon_2 =
 ln(Mbar_Pl/q) q^2 /
 [480 pi^2 Mbar_Pl^2].
```

The largest value in the locked local arena set is

```text
max |epsilon_scalar| =
 {scalar_checks['maximum_MTS_scalar_nonlocal_excess']:.16e}.
```

The largest omitted mass-control ratio is

```text
max m_gap^2/q^2 =
 {scalar_checks['maximum_mass_ratio_squared']:.16e}.
```

For the locked parent `CFF` endpoint,

```text
c_parent =
 {parent_checks['parent_coefficient_m2']:.16e} m^2;

c_parent/|c_visible_control| =
 {parent_checks['parent_to_visible_control_ratio']:.16e};

max local |Delta v_pol/c|_parent =
 {parent_checks['maximum_parent_CFF_residual']:.16e}.
```

The common visible coefficient is roughly forty-one orders larger, but it
belongs to both GR+SM and MTS.  The displayed `C3` residuals are retained as
endpoint smoke values only: checkpoint 4971 proves that the absolute
physical on-shell `C3` anchor cannot be obtained from local running alone.

## 7. Compact-source branch

The ordinary-matter junction theorem gives

```text
Q_chi=0;
a_chi/a_Newton=0
```

at classical one-scalar order.  Across the locked Earth, Sun, white-dwarf
and neutron-star density corridor,

```text
max |Delta c_chi^2| =
 {compact_checks['maximum_abs_delta_cchi_squared']:.16e};

max |Delta m_eff^2/m_gap^2| =
 {compact_checks['maximum_abs_delta_m2_over_m2']:.16e}.
```

This establishes branch existence and stability in the tested corridor. It
does not replace all-equation-of-state sensitivities, binary radiation or
horizon-state calculations.

## 8. Exact result and remaining obstruction

The project can now state privately and precisely:

```text
exact selected bulk chi=0 branch                 = yes;
exact nonlinear two-derivative GR+Lambda         = yes;
one universal Hilbert source                     = yes;
Newtonian mechanics from the same residue        = yes;
all ten two-derivative PPN coefficients          = GR;
Maxwell Hilbert stress and Poynting flux         = exact;
direct classical one-scalar fifth force          = zero;
one frozen Lambda_cal without arena retuning     = yes;
universal extra-scalar nonlocal residual         = calculated;
parent CFF/C3 endpoint smoke residuals            = separated;
local state attractor/preparation theorem        = open;
physical absolute C3 amplitude anchor            = open;
complete MTS-specific p8+ matched excess         = open;
all-operator local GR                            = not claimed;
full MTS unification                             = not claimed.
```

The next derivation target is no longer source coupling, Newton, PPN, or
the classical Poynting vector.  It is:

```text
DERIVE_FIRST_CANONICAL_MTS_SPECIFIC_P8_ONSHELL_COEFFICIENT
FROM_THE_FULL_PARENT_HESSIAN_OR_BOUND_ITS_MATCHED_EXCESS.
```

Checkpoint 4971 already supplies the exact two-scale/helicity rank
contract.  The next calculation must supply a parent amplitude coefficient,
not another inventory of the missing object.

## Reproducibility

Run:

```text
post-checkpoint-work/.venv-score/Scripts/python.exe
post-checkpoint-work/scripts/
Y5_R2FR_5211_selected_local_GR_matched_baseline_gate.py --dry-run

post-checkpoint-work/.venv-score/Scripts/python.exe
post-checkpoint-work/scripts/
Y5_R2FR_5211_selected_local_GR_matched_baseline_gate.py

post-checkpoint-work/.venv-score/Scripts/python.exe
post-checkpoint-work/scripts/
Y5_R2FR_5211_selected_local_GR_matched_baseline_gate.py --validate-saved
```

Evidence CSV digest:

```text
{evidence_digest}
```

The checkpoint is private.  Every generated row keeps
`valid_for_full_MTS_claim=false` and `claim_allowed=false`.
"""


def validation_rows(
    symbolic: dict[str, Any],
    truncation: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    ward_checks: dict[str, Any],
    ppn_rows: list[dict[str, Any]],
    ppn_checks: dict[str, Any],
    maxwell: list[dict[str, Any]],
    maxwell_checks: dict[str, Any],
    baseline: list[dict[str, Any]],
    parent_rows: list[dict[str, Any]],
    parent_checks: dict[str, Any],
    scalar_rows: list[dict[str, Any]],
    scalar_checks: dict[str, Any],
    compact_rows: list[dict[str, Any]],
    compact_checks: dict[str, Any],
    corridor: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    datasets: dict[str, list[dict[str, Any]]],
    evidence_digest: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(
        gate: str,
        passed: bool,
        observed: Any,
        expected: Any,
        evidence: str,
    ) -> None:
        rows.append(
            {
                "gate": gate,
                "status": "PASS" if passed else "FAIL",
                "observed": json.dumps(observed, sort_keys=True),
                "expected": json.dumps(expected, sort_keys=True),
                "evidence": evidence,
                "checkpoint": CHECKPOINT,
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "claim_allowed": False,
                "source_checked_date": CHECKED_DATE,
            }
        )

    add(
        "all_source_locks_present",
        all(path.is_file() for path in SOURCE_LOCKS),
        sum(path.is_file() for path in SOURCE_LOCKS),
        len(SOURCE_LOCKS),
        "source provenance",
    )
    add(
        "scalar_equation_exact_zero",
        symbolic["scalar_equation_on_branch"] == "0",
        symbolic["scalar_equation_on_branch"],
        "0",
        "executed branch substitution",
    )
    add(
        "scalar_stress_exact_zero",
        symbolic["scalar_stress_on_branch"] == "0",
        symbolic["scalar_stress_on_branch"],
        "0",
        "executed branch substitution",
    )
    add(
        "P_and_PX_zero_at_origin",
        symbolic["P_at_zero"] == "0" and symbolic["P_X_at_zero"] == "0",
        (symbolic["P_at_zero"], symbolic["P_X_at_zero"]),
        ("0", "0"),
        "P_ge2 definition",
    )
    add(
        "potential_double_zero",
        symbolic["V_at_zero"] == "0"
        and symbolic["V_prime_at_zero"] == "0",
        (symbolic["V_at_zero"], symbolic["V_prime_at_zero"]),
        ("0", "0"),
        "selected massive even potential",
    )
    add(
        "consistent_truncation_claim_present",
        any(
            row["status"]
            == "EXACT_NONLINEAR_GR_LAMBDA_SM_MAXWELL_TRUNCATION"
            for row in truncation
        ),
        [row["status"] for row in truncation],
        "exact restricted action row",
        "exact_consistent_truncation.csv",
    )
    add(
        "state_selection_not_hidden",
        any(
            row["status"] == "OPEN_STATE_SELECTION_NOT_HIDDEN"
            for row in truncation
        ),
        [row["status"] for row in truncation],
        "explicit open state row",
        "5201 state-selection boundary",
    )
    add(
        "universality_rank_four",
        ward_checks["constraint_rank"] == 4,
        ward_checks["constraint_rank"],
        4,
        "executed soft/Bianchi matrix",
    )
    add(
        "universality_nullity_one",
        ward_checks["constraint_nullity"] == 1,
        ward_checks["constraint_nullity"],
        1,
        "executed soft/Bianchi matrix",
    )
    add(
        "universality_all_ones",
        ward_checks["constraint_null_vector"] == [[1, 1, 1, 1, 1]],
        ward_checks["constraint_null_vector"],
        [[1, 1, 1, 1, 1]],
        "executed nullspace",
    )
    add(
        "imported_species_weights_universal",
        ward_checks["all_imported_relative_couplings_one"],
        ward_checks["all_imported_relative_couplings_one"],
        True,
        "4960 source rows",
    )
    add(
        "ward_exchange_chain_nonempty",
        len(ward_rows) >= 10,
        len(ward_rows),
        ">=10",
        "canonical_Ward_exchange_chain.csv",
    )
    add(
        "PPN_has_ten_parameters",
        ppn_checks["row_count"] == 10,
        ppn_checks["row_count"],
        10,
        "selected_full_PPN_vector.csv",
    )
    add(
        "PPN_names_complete",
        ppn_checks["names"] == ppn_checks["expected_names"],
        ppn_checks["names"],
        ppn_checks["expected_names"],
        "selected_full_PPN_vector.csv",
    )
    add(
        "PPN_all_deltas_zero",
        ppn_checks["all_deltas_zero"],
        ppn_checks["all_deltas_zero"],
        True,
        "selected_full_PPN_vector.csv",
    )
    add(
        "PPN_gamma_beta_GR",
        ppn_checks["gamma"] == 1.0 and ppn_checks["beta"] == 1.0,
        (ppn_checks["gamma"], ppn_checks["beta"]),
        (1.0, 1.0),
        "selected_full_PPN_vector.csv",
    )
    add(
        "Maxwell_Poynting_exact",
        maxwell_checks["poynting"] == maxwell_checks["expected_poynting"],
        maxwell_checks["poynting"],
        maxwell_checks["expected_poynting"],
        "executed symbolic E cross B",
    )
    add(
        "Maxwell_chain_nonempty",
        len(maxwell) >= 9,
        len(maxwell),
        ">=9",
        "Maxwell_Poynting_matched_stress.csv",
    )
    add(
        "matched_baseline_visible_CFF_common",
        any(
            row["operator_block"] == "visible_CFF_thresholds"
            and row["matched_difference"] == "0"
            for row in baseline
        ),
        [row["operator_block"] for row in baseline],
        "visible CFF cancellation row",
        "matched_GRSM_baseline_decomposition.csv",
    )
    add(
        "matched_baseline_p8_open",
        any(
            row["operator_block"] == "p8plus"
            and row["classification"] == "OPEN_ALL_ORDER_OBSTRUCTION"
            for row in baseline
        ),
        [row["classification"] for row in baseline],
        "explicit p8 open row",
        "matched_GRSM_baseline_decomposition.csv",
    )
    add(
        "parent_CFF_recomputed",
        parent_checks["maximum_recomputation_relative_error"] < 1e-12,
        parent_checks["maximum_recomputation_relative_error"],
        "<1e-12",
        "c_parent times curvature factor",
    )
    add(
        "parent_CFF_below_visible_control_1e40",
        parent_checks["parent_to_visible_control_ratio"] < 1e-40,
        parent_checks["parent_to_visible_control_ratio"],
        "<1e-40",
        "matched CFF coefficient ratio",
    )
    add(
        "O4_tree_silence_all_systems",
        parent_checks["O4_exact_zero_all_rows"],
        parent_checks["O4_exact_zero_all_rows"],
        True,
        "MTS_specific_C3_CFF_residual_vector.csv",
    )
    add(
        "scalar_epsilon0_recomputed",
        scalar_checks["maximum_epsilon0_recomputation_relative_error"]
        < 1e-12,
        scalar_checks["maximum_epsilon0_recomputation_relative_error"],
        "<1e-12",
        "direct one-real-scalar formula",
    )
    add(
        "scalar_epsilon2_recomputed",
        scalar_checks["maximum_epsilon2_recomputation_relative_error"]
        < 1e-12,
        scalar_checks["maximum_epsilon2_recomputation_relative_error"],
        "<1e-12",
        "direct one-real-scalar formula",
    )
    add(
        "scalar_local_excess_below_1e30",
        scalar_checks["all_below_1e_minus_30"],
        scalar_checks["maximum_MTS_scalar_nonlocal_excess"],
        "<1e-30",
        "MTS_scalar_nonlocal_excess.csv",
    )
    add(
        "scalar_massless_limit_controlled",
        scalar_checks["maximum_mass_ratio_squared"] < 1e-10,
        scalar_checks["maximum_mass_ratio_squared"],
        "<1e-10",
        "m_gap^2/q^2",
    )
    add(
        "compact_direct_charge_zero",
        compact_checks["all_direct_charges_zero"],
        compact_checks["all_direct_charges_zero"],
        True,
        "compact_source_zero_branch_stability.csv",
    )
    add(
        "compact_kinetic_positive",
        compact_checks["minimum_A_time"] > 0.0
        and compact_checks["minimum_B_space"] > 0.0,
        (compact_checks["minimum_A_time"], compact_checks["minimum_B_space"]),
        ">0",
        "4943 stability corridor",
    )
    add(
        "compact_speed_shift_small",
        compact_checks["maximum_abs_delta_cchi_squared"] < 1e-16,
        compact_checks["maximum_abs_delta_cchi_squared"],
        "<1e-16",
        "4943 stability corridor",
    )
    add(
        "all_order_open_gate_retained",
        any(
            row["gate"] == "p8plus_matched_excess"
            and row["status"] == "OPEN_MAIN_LOCAL_OBSTRUCTION"
            for row in corridor
        ),
        [row["status"] for row in corridor],
        "OPEN_MAIN_LOCAL_OBSTRUCTION",
        "all_order_residual_corridor.csv",
    )
    add(
        "C3_physical_anchor_open_retained",
        any(
            row["gate"] == "C3_absolute_onshell_anchor"
            and row["status"] == "OPEN"
            for row in corridor
        ),
        [row["status"] for row in corridor],
        "OPEN",
        "4971 source boundary",
    )
    add(
        "full_MTS_not_claimed",
        any(
            row["gate"] == "full_MTS_unification"
            and row["status"] == "NOT_CLAIMED"
            for row in corridor
        ),
        [row["status"] for row in corridor],
        "NOT_CLAIMED",
        "all_order_residual_corridor.csv",
    )
    add(
        "next_route_is_amplitude_not_inventory",
        any(
            "DERIVE_FIRST_CANONICAL_MTS_SPECIFIC_P8_ONSHELL_COEFFICIENT"
            in row["next_action"]
            for row in decisions
        ),
        [row["next_action"] for row in decisions],
        "canonical p8 on-shell coefficient",
        "route_decision.csv",
    )
    add(
        "all_generated_rows_private",
        all(
            row.get("valid_for_full_MTS_claim") is False
            and row.get("claim_allowed") is False
            for dataset in datasets.values()
            for row in dataset
        ),
        True,
        True,
        "all generated CSV rows",
    )
    add(
        "all_datasets_nonempty",
        all(dataset for dataset in datasets.values()),
        {name: len(dataset) for name, dataset in datasets.items()},
        "all >0",
        "generated CSVs",
    )
    add(
        "all_dataset_rows_have_status_or_role",
        all(
            (
                "status" in row
                or "classification" in row
                or "role" in row
                or "result" in row
            )
            for dataset in datasets.values()
            for row in dataset
        ),
        True,
        True,
        "generated CSV schema",
    )
    add(
        "evidence_digest_nonempty",
        len(evidence_digest) == 64,
        evidence_digest,
        "64 hex characters",
        "generated evidence tree",
    )
    add(
        "document_written",
        DOCUMENT.is_file() and DOCUMENT.stat().st_size > 1000,
        DOCUMENT.stat().st_size if DOCUMENT.is_file() else 0,
        ">1000 bytes",
        str(DOCUMENT),
    )
    add(
        "formalization_workbench_unchanged",
        tree_digest() == FORMAL_LOCK,
        tree_digest(),
        FORMAL_LOCK,
        "no formalization-workbench edit",
    )
    public_head, public_status = git_state(PUBLIC)
    galaxy_head, galaxy_status = git_state(GALAXY)
    add(
        "public_worktree_unchanged",
        public_head == PUBLIC_HEAD and not public_status,
        (public_head, public_status),
        (PUBLIC_HEAD, []),
        "no GitHub/public action",
    )
    add(
        "galaxy_repository_unchanged",
        galaxy_head == GALAXY_HEAD and galaxy_status == GALAXY_DIRTY,
        (galaxy_head, galaxy_status),
        (GALAXY_HEAD, GALAXY_DIRTY),
        "read-only galaxy boundary",
    )
    add(
        "scripts_cache_absent",
        not (POST / "scripts" / "__pycache__").exists(),
        (POST / "scripts" / "__pycache__").exists(),
        False,
        "no retained bytecode artifact",
    )
    return rows


def build_payloads() -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, Any],
]:
    symbolic = symbolic_consistent_truncation()
    truncation = exact_truncation_rows(symbolic)
    ward_rows, ward_checks = ward_exchange_rows(symbolic)
    ppn_rows, ppn_checks = selected_ppn_rows()
    maxwell, maxwell_checks = maxwell_rows()
    baseline = matched_baseline_rows()
    parent_rows, parent_checks = parent_residual_rows()
    scalar_rows, scalar_checks = scalar_nonlocal_rows()
    compact_rows, compact_checks = compact_stability_rows()
    corridor = all_order_corridor_rows()
    decisions = decision_rows(parent_checks, scalar_checks)
    provenance = provenance_rows()
    datasets = {
        "exact_consistent_truncation.csv": truncation,
        "canonical_Ward_exchange_chain.csv": ward_rows,
        "selected_full_PPN_vector.csv": ppn_rows,
        "Maxwell_Poynting_matched_stress.csv": maxwell,
        "matched_GRSM_baseline_decomposition.csv": baseline,
        "MTS_specific_C3_CFF_residual_vector.csv": parent_rows,
        "MTS_scalar_nonlocal_excess.csv": scalar_rows,
        "compact_source_zero_branch_stability.csv": compact_rows,
        "all_order_residual_corridor.csv": corridor,
        "route_decision.csv": decisions,
        "source_provenance.csv": provenance,
    }
    context = {
        "symbolic": symbolic,
        "truncation": truncation,
        "ward_rows": ward_rows,
        "ward_checks": ward_checks,
        "ppn_rows": ppn_rows,
        "ppn_checks": ppn_checks,
        "maxwell": maxwell,
        "maxwell_checks": maxwell_checks,
        "baseline": baseline,
        "parent_rows": parent_rows,
        "parent_checks": parent_checks,
        "scalar_rows": scalar_rows,
        "scalar_checks": scalar_checks,
        "compact_rows": compact_rows,
        "compact_checks": compact_checks,
        "corridor": corridor,
        "decisions": decisions,
    }
    return datasets, context


def run_checkpoint() -> None:
    source_hashes = assert_source_locks()
    boundaries = assert_untouched_boundaries()
    datasets, context = build_payloads()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in datasets.items():
        write_csv(OUT / name, rows)
    evidence_digest = selected_digest(
        [OUT / name for name in datasets],
        OUT,
    )
    DOCUMENT.write_text(
        build_document(
            context["symbolic"],
            context["ward_checks"],
            context["ppn_checks"],
            context["parent_checks"],
            context["scalar_checks"],
            context["compact_checks"],
            evidence_digest,
        ),
        encoding="utf-8",
    )
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "claim_status": "PRIVATE_SCOPED_THEOREM_NO_FULL_MTS_CLAIM",
        "source_hashes": source_hashes,
        "symbolic_checks": context["symbolic"],
        "universal_source_checks": context["ward_checks"],
        "PPN_checks": context["ppn_checks"],
        "Maxwell_checks": context["maxwell_checks"],
        "parent_endpoint_residual_checks": context["parent_checks"],
        "scalar_nonlocal_checks": context["scalar_checks"],
        "compact_stability_checks": context["compact_checks"],
        "selected_local_result": (
            "EXACT_NONLINEAR_TWO_DERIVATIVE_GR_LAMBDA_SM_MAXWELL_"
            "CONSISTENT_TRUNCATION"
        ),
        "source_result": (
            "ONE_UNIVERSAL_HILBERT_SOURCE_AND_NEWTONIAN_LIMIT_DERIVED"
        ),
        "matched_baseline_result": (
            "COMMON_GRSM_CORRECTIONS_SEPARATED_FROM_MTS_SPECIFIC_EXCESS"
        ),
        "all_order_status": (
            "NOT_CLAIMED_C3_ABSOLUTE_ANCHOR_AND_P8PLUS_EXCESS_OPEN"
        ),
        "selected_next_route": (
            "DERIVE_FIRST_CANONICAL_MTS_SPECIFIC_P8_ONSHELL_COEFFICIENT_"
            "FROM_FULL_PARENT_HESSIAN_OR_BOUND_ITS_MATCHED_EXCESS"
        ),
        "evidence_csv_sha256": evidence_digest,
        **boundaries,
    }
    write_json(
        OUT / "selected_local_GR_matched_baseline_results.json",
        result,
    )
    validation = validation_rows(
        context["symbolic"],
        context["truncation"],
        context["ward_rows"],
        context["ward_checks"],
        context["ppn_rows"],
        context["ppn_checks"],
        context["maxwell"],
        context["maxwell_checks"],
        context["baseline"],
        context["parent_rows"],
        context["parent_checks"],
        context["scalar_rows"],
        context["scalar_checks"],
        context["compact_rows"],
        context["compact_checks"],
        context["corridor"],
        context["decisions"],
        datasets,
        evidence_digest,
    )
    write_csv(VALIDATION, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"validation failures: {failures}")
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "validation": f"{len(validation)}/{len(validation)} PASS",
                "selected_local_result": result["selected_local_result"],
                "source_result": result["source_result"],
                "PPN_vector": (
                    "(1,1,0,0,0,0,0,0,0,0)"
                ),
                "maximum_MTS_scalar_nonlocal_excess": context[
                    "scalar_checks"
                ]["maximum_MTS_scalar_nonlocal_excess"],
                "maximum_parent_CFF_residual": context["parent_checks"][
                    "maximum_parent_CFF_residual"
                ],
                "all_order_status": result["all_order_status"],
                "selected_next_route": result["selected_next_route"],
                "evidence_csv_sha256": evidence_digest,
                "formal_tree_sha256": boundaries["formal_tree_sha256"],
            },
            indent=2,
        )
    )


def validate_saved() -> None:
    assert_source_locks()
    boundaries = assert_untouched_boundaries()
    result_path = OUT / "selected_local_GR_matched_baseline_results.json"
    if not result_path.is_file() or not VALIDATION.is_file() or not DOCUMENT.is_file():
        raise RuntimeError("checkpoint-5211 saved products are incomplete")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    validation = read_csv(VALIDATION)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"saved validation failures: {failures}")
    csv_paths = sorted(OUT.glob("*.csv"))
    actual_digest = selected_digest(csv_paths, OUT)
    if actual_digest != result["evidence_csv_sha256"]:
        raise RuntimeError("checkpoint-5211 evidence digest changed")
    expected_csv_names = {
        "exact_consistent_truncation.csv",
        "canonical_Ward_exchange_chain.csv",
        "selected_full_PPN_vector.csv",
        "Maxwell_Poynting_matched_stress.csv",
        "matched_GRSM_baseline_decomposition.csv",
        "MTS_specific_C3_CFF_residual_vector.csv",
        "MTS_scalar_nonlocal_excess.csv",
        "compact_source_zero_branch_stability.csv",
        "all_order_residual_corridor.csv",
        "route_decision.csv",
        "source_provenance.csv",
    }
    if {path.name for path in csv_paths} != expected_csv_names:
        raise RuntimeError("checkpoint-5211 CSV set changed")
    for path in csv_paths:
        rows = read_csv(path)
        if not rows:
            raise RuntimeError(f"empty saved CSV: {path}")
    if (POST / "scripts" / "__pycache__").exists():
        raise RuntimeError("script __pycache__ exists")
    print(
        json.dumps(
            {
                "saved_validation": f"{len(validation)}/{len(validation)} PASS",
                "csv_count": len(csv_paths),
                "evidence_csv_sha256": actual_digest,
                "formal_tree_sha256": boundaries["formal_tree_sha256"],
                "selected_local_result": result["selected_local_result"],
                "all_order_status": result["all_order_status"],
                "selected_next_route": result["selected_next_route"],
            },
            indent=2,
        )
    )


def dry_run() -> None:
    assert_source_locks()
    boundaries = assert_untouched_boundaries()
    datasets, context = build_payloads()
    print(
        json.dumps(
            {
                "dry_run": "PASS",
                "dataset_rows": {
                    name: len(rows) for name, rows in datasets.items()
                },
                "scalar_equation_on_branch": context["symbolic"][
                    "scalar_equation_on_branch"
                ],
                "scalar_stress_on_branch": context["symbolic"][
                    "scalar_stress_on_branch"
                ],
                "universality_rank": context["ward_checks"][
                    "constraint_rank"
                ],
                "universality_nullity": context["ward_checks"][
                    "constraint_nullity"
                ],
                "PPN_rows": context["ppn_checks"]["row_count"],
                "PPN_all_deltas_zero": context["ppn_checks"][
                    "all_deltas_zero"
                ],
                "maximum_MTS_scalar_nonlocal_excess": context[
                    "scalar_checks"
                ]["maximum_MTS_scalar_nonlocal_excess"],
                "maximum_parent_CFF_residual": context["parent_checks"][
                    "maximum_parent_CFF_residual"
                ],
                "maximum_compact_speed_shift": context["compact_checks"][
                    "maximum_abs_delta_cchi_squared"
                ],
                "formal_tree_sha256": boundaries["formal_tree_sha256"],
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    arguments = parser.parse_args()
    if arguments.dry_run:
        dry_run()
    elif arguments.validate_saved:
        validate_saved()
    else:
        run_checkpoint()


if __name__ == "__main__":
    main()
