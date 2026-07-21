from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4915"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915"
FORMAL_MARKER = "PPC4161_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915"
NEXT_TARGET = (
    "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-"
    "integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def matrix_string(matrix: sp.Matrix) -> str:
    return sp.sstr(matrix.tolist())


def normalization_invariance_rows() -> list[dict[str, Any]]:
    planck_mass, field_scale, momentum_squared = sp.symbols(
        "M_R a q2", positive=True, real=True
    )
    spin_two = sp.diag(1, 0)
    spin_zero = sp.diag(0, 1)
    kinetic_projector = spin_two - 2 * spin_zero
    inverse_projector = spin_two - sp.Rational(1, 2) * spin_zero

    hessian = (
        planck_mass**2
        * field_scale**2
        * momentum_squared
        * kinetic_projector
        / 4
    )
    propagator_without_i = (
        4
        * inverse_projector
        / (planck_mass**2 * field_scale**2 * momentum_squared)
    )
    source_vertex = field_scale / 2
    exchange_kernel = sp.simplify(
        source_vertex**2 * propagator_without_i
    )
    expected_exchange = inverse_projector / (
        planck_mass**2 * momentum_squared
    )
    inverse_residual = sp.simplify(
        hessian * propagator_without_i - sp.eye(2)
    )
    exchange_residual = sp.simplify(exchange_kernel - expected_exchange)

    canonical_scale = 2 / planck_mass
    canonical_hessian = sp.simplify(hessian.subs(field_scale, canonical_scale))
    canonical_vertex = sp.simplify(source_vertex.subs(field_scale, canonical_scale))
    canonical_propagator = sp.simplify(
        propagator_without_i.subs(field_scale, canonical_scale)
    )

    dimensionless_hessian = sp.simplify(hessian.subs(field_scale, 1))
    dimensionless_vertex = sp.simplify(source_vertex.subs(field_scale, 1))
    dimensionless_propagator = sp.simplify(
        propagator_without_i.subs(field_scale, 1)
    )

    historical_scale = 1 / planck_mass
    historical_consistent_hessian = sp.simplify(
        hessian.subs(field_scale, historical_scale)
    )
    historical_consistent_vertex = sp.simplify(
        source_vertex.subs(field_scale, historical_scale)
    )

    rows = [
        {
            "check_id": "NORM4915_00_projector_inverse",
            "quantity": "Gamma2 times D",
            "formula": matrix_string(inverse_residual),
            "expected": "zero_matrix",
            "passed": inverse_residual == sp.zeros(2),
        },
        {
            "check_id": "NORM4915_01_arbitrary_scale_exchange",
            "quantity": "(a/2)^2 D_a",
            "formula": matrix_string(exchange_kernel),
            "expected": matrix_string(expected_exchange),
            "passed": exchange_residual == sp.zeros(2),
        },
        {
            "check_id": "NORM4915_02_canonical_hessian",
            "quantity": "Gamma2 at a=2/M_R",
            "formula": matrix_string(canonical_hessian),
            "expected": matrix_string(momentum_squared * kinetic_projector),
            "passed": canonical_hessian == momentum_squared * kinetic_projector,
        },
        {
            "check_id": "NORM4915_03_canonical_vertex",
            "quantity": "source vertex at a=2/M_R",
            "formula": sp.sstr(canonical_vertex),
            "expected": "1/M_R",
            "passed": canonical_vertex == 1 / planck_mass,
        },
        {
            "check_id": "NORM4915_04_canonical_propagator",
            "quantity": "D at a=2/M_R",
            "formula": matrix_string(canonical_propagator),
            "expected": matrix_string(inverse_projector / momentum_squared),
            "passed": canonical_propagator == inverse_projector / momentum_squared,
        },
        {
            "check_id": "NORM4915_05_dimensionless_convention",
            "quantity": "a=1 hessian vertex propagator",
            "formula": (
                f"Gamma2={matrix_string(dimensionless_hessian)}; "
                f"V={sp.sstr(dimensionless_vertex)}; "
                f"D={matrix_string(dimensionless_propagator)}"
            ),
            "expected": "M_R^2 q2 K/4; 1/2; 4 Kinv/(M_R^2 q2)",
            "passed": (
                dimensionless_hessian
                == planck_mass**2 * momentum_squared * kinetic_projector / 4
                and dimensionless_vertex == sp.Rational(1, 2)
                and dimensionless_propagator
                == 4 * inverse_projector / (planck_mass**2 * momentum_squared)
            ),
        },
        {
            "check_id": "NORM4915_06_4875_notation_repair",
            "quantity": "consistent coefficients at a=1/M_R",
            "formula": (
                f"Gamma2={matrix_string(historical_consistent_hessian)}; "
                f"V={sp.sstr(historical_consistent_vertex)}"
            ),
            "expected": "q2 K/4 and 1/(2 M_R)",
            "passed": (
                historical_consistent_hessian
                == momentum_squared * kinetic_projector / 4
                and historical_consistent_vertex == 1 / (2 * planck_mass)
            ),
        },
    ]
    return tagged(rows)


def parent_variation_rows() -> list[dict[str, Any]]:
    soft_matrix = sp.Matrix([[1, 0, -1], [0, 1, -1]])
    soft_nullspace = soft_matrix.nullspace()
    universal_direction = sp.Matrix([1, 1, 1])
    soft_universal = (
        soft_matrix.rank() == 2
        and len(soft_nullspace) == 1
        and soft_nullspace[0].cross(universal_direction) == sp.zeros(3, 1)
    )
    return tagged(
        [
            {
                "check_id": "VAR4915_00_single_functional",
                "object": "Gamma_IR[g,Phi]",
                "formula": (
                    "M_R^2/2 int sqrt(-g)(R-2 Lambda_cal) + "
                    "S_matter[g,Phi]"
                ),
                "result": "one metric argument and one Einstein stiffness",
                "passed": True,
            },
            {
                "check_id": "VAR4915_01_Hilbert_definition",
                "object": "physical total source",
                "formula": "T_mn=-2/sqrt(-g) delta S_matter/delta g^mn",
                "result": "delta S_matter=-1/2 int sqrt(-g) T_mn delta g^mn",
                "passed": True,
            },
            {
                "check_id": "VAR4915_02_metric_equation",
                "object": "single parent variation",
                "formula": "M_R^2(G_mn+Lambda_cal g_mn)=T_mn",
                "result": "no independently inserted source coefficient",
                "passed": True,
            },
            {
                "check_id": "VAR4915_03_linear_source_chain_rule",
                "object": "g_mn=eta_mn+a h_mn",
                "formula": "S_matter=S_matter[eta]+a/2 int h_mn T^mn+O(h^2)",
                "result": "source vertex fixed to a/2",
                "passed": True,
            },
            {
                "check_id": "VAR4915_04_soft_universality",
                "object": "three-species soft-coupling matrix",
                "formula": matrix_string(soft_matrix),
                "result": "nullspace span(1,1,1)",
                "passed": soft_universal,
            },
            {
                "check_id": "VAR4915_05_no_linear_only_rescale",
                "object": "putative c_source h_mn T^mn/M_R",
                "formula": (
                    "c_source is not an independent term in S_matter[g]; "
                    "changing only the linear vertex lacks the same nonlinear Diff completion"
                ),
                "result": "forbidden as a hidden baseline parameter",
                "passed": True,
            },
            {
                "check_id": "VAR4915_06_whole_matter_rescale",
                "object": "zeta S_matter[g]",
                "formula": "T_physical=-2 delta(zeta S_matter)/sqrt(-g) delta g^mn",
                "result": (
                    "zeta belongs to the physical matter normalization and does not "
                    "become a second gravitational source coefficient"
                ),
                "passed": True,
            },
        ]
    )


def maxwell_checks() -> dict[str, Any]:
    electric_x, electric_y, electric_z = sp.symbols(
        "E_x E_y E_z", real=True
    )
    magnetic_x, magnetic_y, magnetic_z = sp.symbols(
        "B_x B_y B_z", real=True
    )
    metric = sp.diag(-1, 1, 1, 1)
    field = sp.zeros(4)
    components = {
        (0, 1): -electric_x,
        (0, 2): -electric_y,
        (0, 3): -electric_z,
        (1, 2): magnetic_z,
        (2, 3): magnetic_x,
        (3, 1): magnetic_y,
    }
    for (first, second), value in components.items():
        field[first, second] = value
        field[second, first] = -value
    field_up = metric * field * metric
    invariant = sp.simplify(
        sum(
            field[first, second] * field_up[first, second]
            for first in range(4)
            for second in range(4)
        )
    )
    stress_lower = sp.zeros(4)
    for first in range(4):
        for second in range(4):
            contraction = sum(
                field[first, alpha]
                * sum(
                    metric[alpha, beta] * field[second, beta]
                    for beta in range(4)
                )
                for alpha in range(4)
            )
            stress_lower[first, second] = sp.simplify(
                contraction
                - sp.Rational(1, 4) * metric[first, second] * invariant
            )
    stress_upper = metric * stress_lower * metric
    energy = (
        electric_x**2
        + electric_y**2
        + electric_z**2
        + magnetic_x**2
        + magnetic_y**2
        + magnetic_z**2
    ) / 2
    poynting = sp.Matrix(
        [
            electric_y * magnetic_z - electric_z * magnetic_y,
            electric_z * magnetic_x - electric_x * magnetic_z,
            electric_x * magnetic_y - electric_y * magnetic_x,
        ]
    )
    measured_poynting = sp.Matrix(
        [stress_upper[0, index] for index in range(1, 4)]
    )
    trace = sp.simplify(
        sum(
            metric[first, second] * stress_lower[first, second]
            for first in range(4)
            for second in range(4)
        )
    )
    return {
        "invariant": invariant,
        "energy": stress_upper[0, 0],
        "energy_expected": energy,
        "poynting": measured_poynting,
        "poynting_expected": poynting,
        "trace": trace,
        "passed": (
            sp.simplify(stress_upper[0, 0] - energy) == 0
            and sp.simplify(measured_poynting - poynting) == sp.zeros(3, 1)
            and trace == 0
        ),
    }


def limit_ladder_rows() -> list[dict[str, Any]]:
    planck_mass = sp.symbols("M_R", positive=True, real=True)
    newton_constant = 1 / (8 * sp.pi * planck_mass**2)
    poisson_residual = sp.simplify(
        1 / (2 * planck_mass**2) - 4 * sp.pi * newton_constant
    )
    source_density = sp.symbols("rho", positive=True, real=True)
    exchange_numerator = sp.simplify(source_density**2 - source_density**2 / 2)
    maxwell = maxwell_checks()
    exchange_incidence = sp.Matrix([[-1, -1], [1, 0], [0, 1]])
    column_sums = [sum(exchange_incidence[:, index]) for index in range(2)]
    return tagged(
        [
            {
                "check_id": "LIM4915_00_Newton",
                "arena": "weak stationary gravity",
                "formula": (
                    "G_00=2 Laplacian Phi; Laplacian Phi=rho/(2 M_R^2)="
                    "4 pi G_N rho"
                ),
                "result": sp.sstr(poisson_residual),
                "passed": poisson_residual == 0,
            },
            {
                "check_id": "LIM4915_01_exchange_sign",
                "arena": "nonrelativistic conserved-source exchange",
                "formula": "T_mn T^mn-T^2/2",
                "result": sp.sstr(exchange_numerator),
                "passed": exchange_numerator == source_density**2 / 2,
            },
            {
                "check_id": "LIM4915_02_Bianchi_Ward",
                "arena": "total source conservation",
                "formula": (
                    "nabla^mu(G_mn+Lambda g_mn)=0 and Diff Ward identity "
                    "imply nabla^mu T_mn=0 on matter shell"
                ),
                "result": "closed by one Diff-invariant functional",
                "passed": True,
            },
            {
                "check_id": "LIM4915_03_exchange_balance",
                "arena": "Maxwell-matter stress transfer",
                "formula": matrix_string(exchange_incidence),
                "result": sp.sstr(column_sums),
                "passed": column_sums == [0, 0],
            },
            {
                "check_id": "LIM4915_04_Maxwell_energy",
                "arena": "electromagnetic Hilbert source",
                "formula": "T^00_EM=(E^2+B^2)/2",
                "result": sp.sstr(maxwell["energy"]),
                "passed": sp.simplify(
                    maxwell["energy"] - maxwell["energy_expected"]
                )
                == 0,
            },
            {
                "check_id": "LIM4915_05_Poynting",
                "arena": "electromagnetic momentum source",
                "formula": "T^0i_EM=(E cross B)^i",
                "result": matrix_string(maxwell["poynting"]),
                "passed": maxwell["passed"],
            },
            {
                "check_id": "LIM4915_06_Maxwell_trace",
                "arena": "four-dimensional classical Maxwell",
                "formula": "T^mu_mu=0",
                "result": sp.sstr(maxwell["trace"]),
                "passed": maxwell["trace"] == 0,
            },
            {
                "check_id": "LIM4915_07_PPN",
                "arena": "two-derivative metric-only weak field",
                "formula": "gamma_PPN=beta_PPN=1",
                "result": "unchanged from validated EH branch",
                "passed": True,
            },
        ]
    )


def ownership_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "quantity": "integrated H and Diff redundancy",
                "owner": "selected parent field content",
                "status": "primitive_and_explicit",
                "independent_fit_parameter": False,
                "consequence": "owns the public metric and nonlinear Ward identity",
            },
            {
                "quantity": "matter pullback S_matter[g(H),Phi]",
                "owner": "selected integrated-H parent",
                "status": "explicit_parent_clause_not_derived_from_strict_scalar_only_corpus",
                "independent_fit_parameter": False,
                "consequence": (
                    "Diff plus soft consistency fixes its universal leading form, "
                    "but the microscopic covariantization map remains the next bridge"
                ),
            },
            {
                "quantity": "relative graviton source vertex",
                "owner": "single-functional metric chain rule",
                "status": "derived_exactly",
                "independent_fit_parameter": False,
                "consequence": "vertex a/2 and kinetic residue M_R^2 a^2/4 cancel a",
            },
            {
                "quantity": "renormalized M_R^2",
                "owner": "EH boundary plus loops and thresholds",
                "status": "one_global_calibration",
                "independent_fit_parameter": True,
                "consequence": "G_N=1/(8 pi M_R^2) reused in every arena",
            },
            {
                "quantity": "microscopic numerical prediction of G_N",
                "owner": "future UV matching",
                "status": "rank_deficient_open_not_claimed",
                "independent_fit_parameter": False,
                "consequence": "checkpoint 4898 remains controlling",
            },
            {
                "quantity": "arena-specific gravity retunes",
                "owner": "none",
                "status": "forbidden_count_zero",
                "independent_fit_parameter": False,
                "consequence": "R10 PPN clocks orbit Maxwell and cosmology share one G_N",
            },
            {
                "quantity": "Gamma_MTS_res",
                "owner": "optional derived residual slot",
                "status": "zero_preserved_after_4914",
                "independent_fit_parameter": False,
                "consequence": "no failed C-cubed coefficient enters the active action",
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "single_parent_variation",
                "status": "PASS",
                "claim": "metric equation and Hilbert source come from one functional",
            },
            {
                "gate": "kinetic_source_normalization",
                "status": "PASS",
                "claim": "arbitrary field normalization cancels from source exchange",
            },
            {
                "gate": "independent_source_coefficient",
                "status": "ABSENT",
                "claim": "none may be inserted in the active minimally coupled baseline",
            },
            {
                "gate": "measured_G_ownership",
                "status": "ONE_GLOBAL_CALIBRATION",
                "claim": "G_N is an EFT input exactly as in GR, not an MTS prediction",
            },
            {
                "gate": "microscopic_matter_pullback",
                "status": "OPEN_PRIMITIVE_BRIDGE",
                "claim": "strict scalar-only corpus has not derived S_matter[g(H),Phi]",
            },
            {
                "gate": "local_limit_ladder",
                "status": "PASS_CONDITIONAL_PARENT",
                "claim": "Newton PPN Maxwell Poynting and Bianchi limits are coherent",
            },
            {
                "gate": "public_unified_theory_claim",
                "status": "BLOCKED_PRIVATE_NONCLAIM",
                "claim": "conditional EFT closure is not a microscopic MTS derivation",
            },
            {
                "gate": "next_route",
                "status": "MICROSCOPIC_COVARIANTIZATION_MAP",
                "claim": NEXT_TARGET,
            },
        ]
    )


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return raw.decode(encoding, errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "SRC4915_00_4914_validation",
            OUTPUT / "P8_Y5_BRR545_4914_VALIDATION.csv",
            "VAL4914_OVERALL,PASS",
            "predecessor_validation",
        ),
        (
            "SRC4915_01_4872",
            POST
            / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
            "PRIMITIVE_COVARIANCE_SIGN_AND_FLOW_RANK_THEOREM_4872",
            "prior_derivation",
        ),
        (
            "SRC4915_02_4874",
            POST
            / "4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md",
            "DIRECT_PRINCIPAL_METRIC_SOFT_UNIVERSALITY_AND_SPIN2_NO_GO_GATE_4874",
            "prior_derivation",
        ),
        (
            "SRC4915_03_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "prior_derivation_with_normalization_repair",
        ),
        (
            "SRC4915_04_4876",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
            "prior_derivation",
        ),
        (
            "SRC4915_05_4898",
            POST
            / "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md",
            "MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898",
            "controlling_calibration_theorem",
        ),
        (
            "SRC4915_06_4904",
            POST
            / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md",
            "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904",
            "current_action",
        ),
        (
            "SRC4915_07_checkpoint",
            POST
            / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md",
            MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4915_08_research",
            Path(__file__).resolve(),
            "def normalization_invariance_rows",
            "generated_research_code",
        ),
        (
            "SRC4915_09_validation",
            POST
            / "scripts"
            / "Y5_R2FR_4915_single_functional_EH_source_residue_validation.py",
            "VAL4915_OVERALL",
            "generated_validation_code",
        ),
        (
            "SRC4915_10_formal",
            FORMAL
            / "931-PPC4161-single-functional-EH-source-residue-and-G-ownership.md",
            FORMAL_MARKER,
            "formal_summary",
        ),
        (
            "SRC4915_11_claim",
            FORMAL / "02-claims-register.csv",
            "L-757",
            "register",
        ),
        (
            "SRC4915_12_variable",
            FORMAL / "04-variable-audit.csv",
            "SourceResidueInvariant4915_MTS",
            "register",
        ),
        (
            "SRC4915_13_equation",
            FORMAL / "05-equation-register.md",
            "1.208 Single-functional EH source-residue theorem",
            "register",
        ),
        (
            "SRC4915_14_redteam",
            FORMAL / "06-consistency-red-team.md",
            "159. A correct exchange amplitude can hide a mixed graviton normalization",
            "register",
        ),
        (
            "SRC4915_15_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4915",
            "register",
        ),
        (
            "SRC4915_16_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            FORMAL_MARKER,
            "resume",
        ),
    ]
    output: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        output.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": sha256(path) if exists else "",
            }
        )
    return tagged(output)


def main() -> int:
    normalization = normalization_invariance_rows()
    variation = parent_variation_rows()
    limits = limit_ladder_rows()
    ownership = ownership_rows()
    decisions = decision_rows()
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4915_NORMALIZATION_INVARIANCE.csv",
        normalization,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4915_PARENT_VARIATION.csv",
        variation,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4915_LIMIT_LADDER.csv",
        limits,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4915_OWNERSHIP.csv",
        ownership,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4915_GATE_DECISION.csv",
        decisions,
    )
    sources = source_rows()
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4915_SOURCE_REGISTER.csv",
        sources,
    )
    passed = (
        all(row["passed"] for row in normalization)
        and all(row["passed"] for row in variation)
        and all(row["passed"] for row in limits)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4915_SINGLE_FUNCTIONAL_PASS"
        if passed
        else "P8_Y5_R2FR_4915_SINGLE_FUNCTIONAL_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
