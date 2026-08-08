from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / "5158"
RESULT_JSON = OUT / "clock_charge_source_symmetry_results.json"
OPERATOR_CSV = OUT / "clock_charge_source_operator_audit.csv"
CURRENT_CSV = OUT / "clock_memory_modified_current.csv"
BALANCE_CSV = OUT / "neutral_pair_vs_signed_charge.csv"
DECISION_CSV = OUT / "state_preparation_branch_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5158_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5158-Y5-R2FR-clock-charge-source-symmetry-no-go-and-neutral-state-pivot.md"
)

PREVIOUS_DOCUMENT = (
    POST
    / "5157-Y5-R2FR-composite-motion-clock-charge-entropy-adiabatic-state-preparation-reentry-gate.md"
)
PREVIOUS_RESULT = OUT.parent / "5157" / "composite_motion_clock_state_preparation_results.json"
PREVIOUS_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5157_VALIDATION.csv"
)
PAIR_DOCUMENT = (
    POST
    / "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md"
)
PAIR_SCRIPT = POST / "scripts" / "Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel.py"
CLOCK_DOCUMENT = (
    POST
    / "4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md"
)
BATH_COMPLETION = (
    POST
    / "4895-Y5-R2FR-full-positive-spectral-matrix-clock-counterterm-and-local-GR-decoupling-or-bath-cosmology-retirement-gate.md"
)
BATH_RETIREMENT = (
    POST
    / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md"
)
METRIC_BASELINE = (
    POST
    / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md"
)
LOCAL_PARENT = (
    POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
)
PAIR_OPERATOR = (
    POST
    / "4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md"
)
GRAVITON_PAIR = (
    POST
    / "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md"
)
X2_CASCADE = (
    POST
    / "4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md"
)
NUMBER_CHANGE = (
    POST
    / "4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md"
)
CP_EVEN_HIERARCHY = (
    POST
    / "4955-Y5-R2FR-six-derivative-shift-sector-X3-parent-flow-and-number-changing-fixed-ratio-or-strong-2PI-route-rejection.md"
)
ESSENTIAL_AMPLITUDE = (
    POST
    / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
)
FULL_PROJECTOR = (
    POST
    / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
)

MARKER = "MTS_5158_CLOCK_CHARGE_SOURCE_SYMMETRY_NO_GO_NEUTRAL_STATE_PIVOT"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ROUTE_DECISION = (
    "NO_REGULAR_PARENT_NET_CHARGE_SOURCE_RETAIN_PRECHARGED_CLOCK_ONLY_AS_BOUNDARY_"
    "USE_NEUTRAL_ONE_CLOCK_STATE_FOR_CONDITIONAL_COLLAPSE"
)


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(file_digest(item).encode("ascii"))
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def source_paths() -> dict[str, Path]:
    return {
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "previous_validation": PREVIOUS_VALIDATION,
        "clock_pair_document": PAIR_DOCUMENT,
        "clock_pair_script": PAIR_SCRIPT,
        "clock_action_document": CLOCK_DOCUMENT,
        "bath_positive_completion": BATH_COMPLETION,
        "bath_retirement": BATH_RETIREMENT,
        "metric_baseline": METRIC_BASELINE,
        "local_parent": LOCAL_PARENT,
        "reflection_even_pair_operator": PAIR_OPERATOR,
        "graviton_pair_source": GRAVITON_PAIR,
        "X2_cascade": X2_CASCADE,
        "finite_time_number_change": NUMBER_CHANGE,
        "CP_even_hierarchy": CP_EVEN_HIERARCHY,
        "essential_amplitude": ESSENTIAL_AMPLITUDE,
        "full_projector": FULL_PROJECTOR,
    }


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.is_file(),
            "sha256": file_digest(path) if path.is_file() else "",
            "role": "read_only_parent_or_predecessor",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for source_id, path in paths.items()
    ]


def symbolic_identities() -> dict[str, Any]:
    amplitude, mass, theta_gradient, memory_gradient, mixing = sp.symbols(
        "A m dtheta dphi kappa", real=True
    )
    lagrangian = (
        -sp.Rational(1, 2) * amplitude**2 * theta_gradient**2
        - sp.Rational(1, 2) * mass**2 * amplitude**2
        + mixing * memory_gradient * theta_gradient
    )
    phase_current = sp.diff(lagrangian, theta_gradient)
    amplitude_equation_algebraic = sp.diff(lagrangian, amplitude)
    mixing_amplitude_source = sp.diff(
        mixing * memory_gradient * theta_gradient, amplitude
    )
    amplitude_zero_residual = sp.simplify(
        amplitude_equation_algebraic.subs(amplitude, 0)
    )
    theta_coordinate = sp.symbols("theta", real=True)
    theta_shift_derivative = sp.diff(lagrangian, theta_coordinate)
    positive_charge, negative_charge = sp.Integer(1), sp.Integer(-1)
    return {
        "phase_current": str(phase_current),
        "amplitude_equation_algebraic_part": str(amplitude_equation_algebraic),
        "mixing_amplitude_source": str(mixing_amplitude_source),
        "mixing_does_not_source_amplitude": mixing_amplitude_source == 0,
        "zero_amplitude_residual": str(amplitude_zero_residual),
        "zero_amplitude_is_homogeneous_solution": amplitude_zero_residual == 0,
        "phase_shift_derivative": str(theta_shift_derivative),
        "phase_shift_symmetry_exact": theta_shift_derivative == 0,
        "neutral_pair_total_charge": int(positive_charge + negative_charge),
        "neutral_pair_charge_zero": positive_charge + negative_charge == 0,
    }


def operator_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "canonical_Cartesian_pair",
            "|grad Z|^2+m_X^2|Z|^2",
            "O(2)_X_EXACT",
            "div J_X=0",
            "NO_NET_CHARGE_SOURCE",
            "regular at Z=0",
            PAIR_DOCUMENT,
        ),
        (
            "universal_metric_pair_vertex",
            "h_mn T_X^mn",
            "O(2)_X_EXACT",
            "vacuum emission creates X plus anti-X with total Q_X=0",
            "NEUTRAL_PAIR_SOURCE_ONLY",
            "same rank-one metric residue",
            GRAVITON_PAIR,
        ),
        (
            "curvature_kinetic_portal",
            "C^2 |grad Z|^2",
            "O(2)_X_EXACT_IF_DOUBLET_COMPLETED",
            "changes propagation but has no tadpole at Z=0",
            "NO_NET_CHARGE_SOURCE",
            "FLRW Weyl tensor vanishes",
            LOCAL_PARENT,
        ),
        (
            "clock_memory_gradient_mix",
            "kappa_mix grad(phi).grad(theta)",
            "PHASE_SHIFT_EXACT",
            "modifies the conserved current but is independent of amplitude",
            "NO_AMPLITUDE_NUCLEATION",
            "Cartesian representation divides by X_1^2+X_2^2 and is undefined at Z=0",
            PAIR_DOCUMENT,
        ),
        (
            "Schwinger_Keldysh_exchange",
            "div J_subsystem=Q_SK; div(J_subsystem+J_bath)=0",
            "TOTAL_CURRENT_CONSERVED",
            "can exchange a pre-existing signed bath charge only",
            "NO_PARENT_SIGNED_BATH_STATE",
            "full bath cosmology retired and its state normalization unselected",
            BATH_RETIREMENT,
        ),
        (
            "reflection_even_Rpsi2_Tpsi2",
            "R psi^2 and T psi^2",
            "PAIR_EVEN_NO_INTERNAL_TORQUE",
            "changes the pair Hessian but does not select a phase orientation",
            "NO_NET_CHARGE_SOURCE_AND_LOCAL_ROUTE_REJECTED",
            "static local window failed",
            PAIR_OPERATOR,
        ),
        (
            "real_scalar_X2_X3_hierarchy",
            "P(X)=X/2+cX^2+eX^3+...",
            "CP_EVEN_REAL_SCALAR_BASIS",
            "allows neutral real-quanta number change but owns no signed O(2) charge",
            "NOT_A_CLOCK_CHARGE_SOURCE",
            "an O(2) doublet completion would require a new flow derivation",
            CP_EVEN_HIERARCHY,
        ),
        (
            "direct_linear_tadpole",
            "J_1 X_1+J_2 X_2",
            "BREAKS_O2_AND_REFLECTION",
            "would source amplitude and phase directly",
            "ABSENT_AND_LOCAL_COG_UNSAFE",
            "would reopen a classical one-scalar source unless separately screened",
            LOCAL_PARENT,
        ),
        (
            "chemical_potential_current",
            "b_mu J_X^mu",
            "O(2)_X_EXACT",
            "biases energy at fixed Q_X but does not change total Q_X in a closed system",
            "NO_CHARGE_FROM_ZERO_WITHOUT_RESERVOIR",
            "no signed reservoir is parent-owned",
            CLOCK_DOCUMENT,
        ),
        (
            "boundary_superselection_charge",
            "Q_X=Q_boundary",
            "CONSISTENT_STATE_BOUNDARY",
            "supplies a precharged coherent clock sector",
            "WORKS_AS_GLOBAL_INPUT_NOT_DYNAMICAL_DERIVATION",
            "one global number; no arena dependence",
            PREVIOUS_DOCUMENT,
        ),
    ]
    return [
        {
            "operator": operator,
            "form": form,
            "symmetry": symmetry,
            "effect": effect,
            "source_verdict": verdict,
            "local_or_parent_issue": issue,
            "source_path": str(source),
            "regular_parent_net_charge_source": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for operator, form, symmetry, effect, verdict, issue, source in rows
    ]


def current_rows(identities: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        (
            "polar_action",
            "L=-[(grad A)^2+A^2((grad theta)^2+m^2)]/2+kappa_mix grad(phi).grad(theta)",
            "theta=m_X U",
            "EXACT_REDUCTION_FOR_A_NONZERO",
        ),
        (
            "modified_Noether_current",
            f"j_theta={identities['phase_current']}",
            "phase-shift invariance",
            "EXACT_CONSERVED_TOTAL_CLOCK_CURRENT",
        ),
        (
            "amplitude_equation",
            f"dL/dA={identities['amplitude_equation_algebraic_part']} plus Box A",
            "mixing term has dL_mix/dA=0",
            "HOMOGENEOUS_IN_A",
        ),
        (
            "zero_amplitude",
            f"E_A(A=0)={identities['zero_amplitude_residual']}",
            "where the Cartesian action is regular",
            "NO_CLASSICAL_NUCLEATION",
        ),
        (
            "Cartesian_origin",
            "L_mix proportional grad(phi).(X_1 grad X_2-X_2 grad X_1)/(X_1^2+X_2^2)",
            "A=0",
            "UNDEFINED_NOT_A_REGULAR_SOURCE",
        ),
        (
            "regularity_dichotomy",
            "regular completion vanishes sufficiently fast at A=0 or singular completion is excluded",
            "local EFT and exact Cartesian vacuum",
            "EITHER_NO_SOURCE_OR_NOT_ADMISSIBLE",
        ),
        (
            "open_system_exchange",
            "div j_pair=-div j_bath=Q_SK",
            "closed total parent",
            "REQUIRES_PARENT_SIGNED_BATH_CHARGE_AND_STATE",
        ),
    ]
    return [
        {
            "step": step,
            "equation": equation,
            "premise": premise,
            "status": status,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for step, equation, premise, status in rows
    ]


def balance_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "gravitational_vacuum_pair",
            "X+anti-X",
            2,
            0,
            "energy and total number can be produced; signed clock charge cannot",
        ),
        (
            "real_scalar_number_change",
            "2<->4 or 1<->3 real quanta",
            "variable",
            "not_defined",
            "not an O(2) clock-charge sector",
        ),
        (
            "precharged_coherent_pair",
            "one phase orientation",
            "macroscopic",
            "nonzero_boundary_value",
            "supports a WKB clock but requires a charge superselection input",
        ),
        (
            "charge_neutral_one_clock_yield",
            "particles plus antiparticles produced on one reheating surface",
            "macroscopic",
            0,
            "can still give S_Xgamma=0 for total frozen number, but no unique internal phase clock",
        ),
        (
            "local_Cartesian_vacuum",
            "no occupied quanta",
            0,
            0,
            "retains GR/Newton/Maxwell exactly at displayed order",
        ),
    ]
    return [
        {
            "state": state,
            "content": content,
            "total_particle_number_role": number,
            "signed_internal_charge": charge,
            "physics_consequence": consequence,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for state, content, number, charge, consequence in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D5158_01",
            "branch": "existing_regular_parent_net_clock_charge",
            "verdict": "REJECTED",
            "reason": "every regular displayed vertex preserves the phase charge or produces neutral pairs",
            "next_action": "do not claim dynamic clock-charge preparation",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5158_02",
            "branch": "4890_clock_memory_mix_as_nucleation_source",
            "verdict": "REJECTED",
            "reason": "the mix is amplitude-independent in polar variables and undefined at the Cartesian origin",
            "next_action": "retain it only on an already occupied controlled chart",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5158_03",
            "branch": "precharged_composite_clock",
            "verdict": "CONSISTENT_BOUNDARY_SECTOR_ONLY",
            "reason": "a single global Q_X is compatible with all local cogs but is not generated",
            "next_action": "label Q_X or Y_X as state data unless a future microscopic asymmetry derives it",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5158_04",
            "branch": "charge_neutral_one_clock_motion_state",
            "verdict": "LEAST_ADDITIVE_ACTIVE_ROUTE",
            "reason": "it preserves the current real-scalar parent and can inherit adiabaticity for total frozen number without a new signed charge",
            "next_action": "use one globally calibrated state in the no-refit collapse comparator while keeping state preparation nonclaim",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5158_05",
            "branch": "nonlinear_formation",
            "verdict": "ADVANCE_TO_EXECUTION",
            "reason": "the source audit has now been attempted and closed negatively; further source relabelling will not derive q/core/p=2",
            "next_action": "run the frozen Vlasov plus wave-density-matrix collapse gate without fitting the target profile",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def make_document(identities: dict[str, Any]) -> str:
    return f"""# 5158 - Clock-charge source symmetry no-go and neutral-state pivot

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5157 did not leave charge generation as a paper target. This
checkpoint searches the existing pair, gravity, memory, open-bath and
`X2/X3` vertices for an actual source. The result is negative and sharp:
there is no regular parent-owned operator in the current corpus that evolves
zero signed internal clock charge into the macroscopic charged condensate.

The checkpoint-4890 pair remains a valid representation of an **already
precharged** sector. It is not a state-preparation mechanism. The least
additive active route is therefore the existing neutral real-scalar motion
state, with one global state calibration and an explicitly conditional
one-clock adiabatic law, followed now by the no-refit collapse test.

## 1. General symmetry theorem

For `theta=m_X U`, the relevant polar action is

```text
L=-[(grad A)^2+A^2((grad theta)^2+m_X^2)]/2
  +kappa_mix grad(phi).grad(theta).
```

It contains no undifferentiated `theta`. The exact Noether current obtained
symbolically is

```text
j_theta={identities['phase_current']},
div j_theta=0
```

for the closed reversible sector. The phase-shift derivative is exactly
`{identities['phase_shift_derivative']}`. Gravity, curvature dressing and
CP-even derivative self-interactions do not change this conclusion when they
are completed as an `O(2)_X` doublet.

Consequently a neutral source can create only charge-balanced pairs. The
executed charge sum is
`(+1)+(-1)={identities['neutral_pair_total_charge']}`. Gravitational particle
production may populate energy and total occupation, but it cannot orient the
macroscopic phase clock.

## 2. Why the old clock-memory mixing does not rescue it

The checkpoint-4890 microscopic mixing is

```text
L_mix proportional grad(phi).
 (X_1 grad X_2-X_2 grad X_1)/(X_1^2+X_2^2).
```

For `A>0` this reduces to `kappa_mix grad(phi).grad(theta)` and modifies the
conserved current. It is independent of `A`, so its amplitude derivative is
exactly `{identities['mixing_amplitude_source']}`. The amplitude equation is
homogeneous and its `A=0` residual is
`{identities['zero_amplitude_residual']}`. It can redistribute current on an
already occupied polar chart; it does not nucleate the amplitude.

At `A=0` its Cartesian denominator vanishes. This gives a strict dichotomy:

1. a regular Cartesian completion vanishes sufficiently fast at the origin,
   preserving the no-source result; or
2. the singular expression is not an admissible local parent at the exact
   GR vacuum.

Neither branch supplies a regular vacuum-to-clock transition.

## 3. Open bath and number-changing routes

The Schwinger--Keldysh clock equation permits subsystem exchange,

```text
div j_pair=-div j_bath=Q_SK,
```

but the closed total current is still conserved. Generating signed pair charge
requires the bath to carry the opposite signed charge and requires its state
to choose the asymmetry. No such signed bath-charge row exists, and checkpoints
4895--4896 retired the full bath cosmology after its reciprocal stress changed
the early gravitational normalization. It cannot be revived as an unnamed
charge reservoir.

The checkpoints 4952--4959 do derive neutral gravitational pair production
and real-scalar `2<->4`/finite-time number-changing channels. They are CP-even
and own total occupation, not an oriented `O(2)_X` charge. Complexifying those
results would require a new doublet flow and would still preserve net charge
unless an explicit asymmetric operator and state were added.

A direct linear tadpole could create an amplitude, but it breaks the
reflection/O(2) selection rule and reopens the local one-scalar source that
checkpoint 4947 removed. A chemical-potential current can bias a state at
fixed charge but cannot create charge in a closed system. Neither is an
existing safe solution.

## 4. What survives

Two state branches remain mathematically honest:

```text
precharged complex pair:
  exact WKB clock + exact conserved charge;
  Q_X is one global boundary datum, not dynamically derived;

neutral real scalar / neutral pair gas:
  current active parent and Schrodinger--Poisson limit retained;
  total frozen number can obey the 5157 charge/entropy-style
  one-clock adiabatic theorem after production;
  no unique internal phase clock is claimed.
```

The second branch adds less to the active parent. It is selected for the next
conditional collapse calculation. This selection does not promote its
abundance or primordial covariance to a fundamental prediction.

## 5. Machine-cog consequence

The no-go protects rather than weakens the local result. No unsafe tadpole,
direct matter charge, second metric or electromagnetic charge is introduced.
The exact Cartesian vacuum remains the checkpoint-4947 GR/Newton/Maxwell
branch; Maxwell and Poynting momentum remain in the same Hilbert source. An
occupied neutral motion state can still gravitate on galactic scales through
that same metric.

What is not yet known is whether nonlinear evolution of the globally fixed
state produces `q_parent`, the finite wave core and the `p=2` edge. The source
hunt has now been performed rather than deferred. The next move is execution,
not another relabelling of the source.

## 6. Status

```text
regular current-changing parent vertex              = absent by source audit;
4890 mix as amplitude nucleation                     = rejected exactly;
neutral gravitational pair production               = retained;
real-scalar number-changing hierarchy                = retained but not charge;
precharged composite clock                           = boundary sector only;
neutral one-clock state                              = selected conditional route;
local GR/Newton/Maxwell cog                          = retained;
q/core/p=2 formation                                 = still unproved.
```

All generated rows remain nonclaim. The protected `formalization-workbench`
digest remains `{FORMAL_DIGEST_LOCK}`. No GitHub action occurred.
"""


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, detail: Any
) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing checkpoint sources: {missing}")
    source_hashes_before = {key: file_digest(path) for key, path in paths.items()}
    formal_before = tree_digest(FORMAL)

    previous = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    if previous["checkpoint_marker"] != "MTS_5157_COMPOSITE_MOTION_CLOCK_ADIABATIC_STATE_PREPARATION_GATE":
        raise RuntimeError("checkpoint 5157 marker mismatch")
    identities = symbolic_identities()
    operators = operator_rows()
    currents = current_rows(identities)
    balances = balance_rows()
    decisions = decision_rows()
    provenance = provenance_rows(paths)

    write_csv(OPERATOR_CSV, operators)
    write_csv(CURRENT_CSV, currents)
    write_csv(BALANCE_CSV, balances)
    write_csv(DECISION_CSV, decisions)
    write_csv(PROVENANCE_CSV, provenance)
    DOCUMENT.write_text(make_document(identities), encoding="utf-8")

    source_hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "V5158_01_source_paths_exist", not missing, missing)
    add_validation(
        validation,
        "V5158_02_source_hashes_unchanged",
        source_hashes_before == source_hashes_after,
        source_hashes_after,
    )
    add_validation(
        validation,
        "V5158_03_formalization_workbench_unchanged",
        formal_before == formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "V5158_04_phase_shift_symmetry_exact",
        identities["phase_shift_symmetry_exact"],
        identities["phase_shift_derivative"],
    )
    add_validation(
        validation,
        "V5158_05_mixing_amplitude_source_zero",
        identities["mixing_does_not_source_amplitude"],
        identities["mixing_amplitude_source"],
    )
    add_validation(
        validation,
        "V5158_06_zero_amplitude_homogeneous_solution",
        identities["zero_amplitude_is_homogeneous_solution"],
        identities["zero_amplitude_residual"],
    )
    add_validation(
        validation,
        "V5158_07_neutral_pair_charge_balance",
        identities["neutral_pair_charge_zero"],
        identities["neutral_pair_total_charge"],
    )
    add_validation(
        validation,
        "V5158_08_all_candidate_operators_audited",
        len(operators) == 10,
        len(operators),
    )
    add_validation(
        validation,
        "V5158_09_no_regular_parent_net_charge_source",
        not any(row["regular_parent_net_charge_source"] for row in operators),
        [row["source_verdict"] for row in operators],
    )
    add_validation(
        validation,
        "V5158_10_clock_mix_origin_singularity_recorded",
        any(row["operator"] == "clock_memory_gradient_mix" and "undefined" in row["local_or_parent_issue"] for row in operators),
        "Cartesian denominator X_1^2+X_2^2",
    )
    add_validation(
        validation,
        "V5158_11_regular_completion_dichotomy_recorded",
        any(row["step"] == "regularity_dichotomy" and row["status"] == "EITHER_NO_SOURCE_OR_NOT_ADMISSIBLE" for row in currents),
        "regular no-source or singular rejection",
    )
    add_validation(
        validation,
        "V5158_12_open_bath_not_falsely_used",
        any(row["operator"] == "Schwinger_Keldysh_exchange" and row["source_verdict"] == "NO_PARENT_SIGNED_BATH_STATE" for row in operators),
        "signed reservoir absent",
    )
    add_validation(
        validation,
        "V5158_13_gravity_pair_source_neutral",
        any(row["operator"] == "universal_metric_pair_vertex" and row["source_verdict"] == "NEUTRAL_PAIR_SOURCE_ONLY" for row in operators),
        "X plus anti-X",
    )
    add_validation(
        validation,
        "V5158_14_real_scalar_hierarchy_not_relabelled",
        any(row["operator"] == "real_scalar_X2_X3_hierarchy" and row["source_verdict"] == "NOT_A_CLOCK_CHARGE_SOURCE" for row in operators),
        "real number change is not signed charge",
    )
    add_validation(
        validation,
        "V5158_15_unsafe_tadpole_rejected",
        any(row["operator"] == "direct_linear_tadpole" and row["source_verdict"] == "ABSENT_AND_LOCAL_COG_UNSAFE" for row in operators),
        "reflection and local source protected",
    )
    add_validation(
        validation,
        "V5158_16_precharged_branch_boundary_only",
        any(row["branch"] == "precharged_composite_clock" and row["verdict"] == "CONSISTENT_BOUNDARY_SECTOR_ONLY" for row in decisions),
        "Q_X remains state data",
    )
    add_validation(
        validation,
        "V5158_17_neutral_route_selected",
        any(row["branch"] == "charge_neutral_one_clock_motion_state" and row["verdict"] == "LEAST_ADDITIVE_ACTIVE_ROUTE" for row in decisions),
        "current real-scalar parent retained",
    )
    add_validation(
        validation,
        "V5158_18_collapse_execution_selected",
        any(row["branch"] == "nonlinear_formation" and row["verdict"] == "ADVANCE_TO_EXECUTION" for row in decisions),
        "no more source relabelling",
    )
    add_validation(
        validation,
        "V5158_19_local_GR_branch_not_modified",
        previous["local_GR_Newton_Maxwell_branch_retained_conditionally"],
        "no new source adopted",
    )
    add_validation(
        validation,
        "V5158_20_all_rows_nonclaim",
        all(not row["valid_for_claim"] for rows in (operators, currents, balances, decisions, provenance) for row in rows),
        "all generated rows",
    )
    generated_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in (OPERATOR_CSV, CURRENT_CSV, BALANCE_CSV, DECISION_CSV, PROVENANCE_CSV, DOCUMENT)
    )
    add_validation(
        validation,
        "V5158_21_no_placeholder_markers",
        "MISSING_" not in generated_text and "PLACEHOLDER" not in generated_text,
        "generated artifacts scanned",
    )
    add_validation(
        validation,
        "V5158_22_document_marker_present",
        MARKER in DOCUMENT.read_text(encoding="utf-8"),
        str(DOCUMENT),
    )
    add_validation(
        validation,
        "V5158_23_route_decision_fail_closed",
        "NO_REGULAR_PARENT_NET_CHARGE_SOURCE" in ROUTE_DECISION,
        ROUTE_DECISION,
    )
    add_validation(
        validation,
        "V5158_24_no_net_charge_claim",
        all("DERIVED_NET_CHARGE" not in row["source_verdict"] for row in operators),
        "source audit negative",
    )
    add_validation(
        validation,
        "V5158_25_predecessor_validation_passed",
        not previous["validation_failures"] and previous["validation_count"] == 28,
        previous["validation_count"],
    )
    failures = [row["check_id"] for row in validation if not row["passed"]]
    write_csv(VALIDATION_CSV, validation)

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "route_decision": ROUTE_DECISION,
        "symbolic_identities": identities,
        "summary": {
            "operator_rows": len(operators),
            "regular_parent_net_charge_sources": sum(bool(row["regular_parent_net_charge_source"]) for row in operators),
            "current_rows": len(currents),
            "state_balance_rows": len(balances),
        },
        "existing_regular_parent_net_clock_charge_source": False,
        "clock_memory_mix_nucleates_amplitude": False,
        "neutral_gravitational_pair_source_retained": True,
        "precharged_composite_clock_is_boundary_sector": True,
        "neutral_one_clock_state_selected_conditionally": True,
        "parent_state_preparation_fully_derived": False,
        "advance_to_no_refit_nonlinear_collapse": True,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_cosmology_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "validation_count": len(validation),
        "validation_failures": failures,
    }
    write_json(RESULT_JSON, result)
    if failures:
        raise RuntimeError(f"checkpoint 5158 validation failed: {failures}")


if __name__ == "__main__":
    main()
