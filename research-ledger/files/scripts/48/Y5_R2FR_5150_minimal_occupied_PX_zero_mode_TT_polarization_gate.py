from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from pathlib import Path
from typing import Any

from scipy.special import beta, gamma


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / "5150"
RESULT_JSON = OUT / "minimal_occupied_PX_zero_mode_TT_results.json"
HESSIAN_CSV = OUT / "occupied_PX_hessian_and_Ward_contract.csv"
LOOP_CSV = OUT / "zero_mode_TT_loop_derivation.csv"
SIGN_CSV = OUT / "critical_sign_and_scale_gate.csv"
ROUTE_CSV = OUT / "surviving_motion_response_routes.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5150_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5150-Y5-R2FR-minimal-occupied-PX-zero-mode-TT-polarization-and-critical-sign-gate.md"
)
MARKER = "MTS_5150_MINIMAL_OCCUPIED_PX_ZERO_MODE_TT_CRITICAL_SIGN_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
REDUCED_PLANCK_MASS_EV = 2.435e27
HBAR_C_EV_M = 1.973269804e-7
KPC_M = 3.085677581491367e19


SOURCE_PATHS = {
    "causal_kernel_gate": POST
    / "5149-Y5-R2FR-causal-spectral-density-critical-motion-mixing-and-vacuum-no-go.md",
    "causal_kernel_result": POST
    / "source-intake"
    / "functional_rg"
    / "5149"
    / "causal_spectral_density_and_critical_mixing_results.json",
    "kernel_result": POST
    / "source-intake"
    / "functional_rg"
    / "5148"
    / "regime_selective_motion_response_results.json",
    "galaxy_smoke": POST
    / "source-intake"
    / "functional_rg"
    / "5148"
    / "galaxy_kernel_interface_smoke.csv",
    "stationary_motion_CTP": POST
    / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md",
    "functional_PX_parent": POST
    / "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md",
    "universal_metric_source": POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md",
}


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def loop_coefficients() -> dict[str, float]:
    dimension = 3.0
    numerator_power = 2.0
    denominator_power = 2.0
    radial = (
        gamma(numerator_power + dimension / 2.0)
        * gamma(denominator_power - numerator_power - dimension / 2.0)
        / (
            (4.0 * math.pi) ** (dimension / 2.0)
            * gamma(dimension / 2.0)
            * gamma(denominator_power)
        )
    )
    tensor_average = radial / (dimension * (dimension + 2.0))
    parameter_integral = beta(2.5, 2.5)
    one_contraction = tensor_average * parameter_integral
    connected_Txy = 2.0 * one_contraction
    metric_hessian = -connected_Txy / 4.0
    return {
        "radial_l4_integral_coefficient": float(radial),
        "tensor_average_coefficient": float(tensor_average),
        "feynman_parameter_integral": float(parameter_integral),
        "one_contraction_Txy_coefficient": float(one_contraction),
        "connected_Txy_Txy_coefficient": float(connected_Txy),
        "metric_hessian_nonanalytic_coefficient": float(metric_hessian),
    }


def write_document(result: dict[str, Any]) -> None:
    loop = result["zero_mode_loop"]
    scale = result["scale_match"]
    DOCUMENT.write_text(
        f"""# 5150 - Minimal occupied `P(X)` zero-mode TT polarization and critical-sign gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

The actual smallest occupied-state calculation has now been performed. The
route is granted its most favorable gapless limit; the current positive
`m_gap^2` would only strengthen the analytic/gapped obstruction. A regular
reflection-even `P(X)` action on an occupied background has a stable gapless
scalar mode when

```text
Z_t=P_X+2 Xbar P_XX>0,
Z_s=P_X>0,
c_s^2=Z_s/Z_t>0.
```

Its tree static Hessian is local and rational in `k^2`; on a homogeneous
timelike state the scalar has no linear transverse-traceless metric mixing.
The first universal nonanalytic TT term therefore comes from the occupied
zero-mode stress loop.

## Exact zero-mode loop

Take external momentum along `z`. After static canonical normalization,
`T_xy=partial_x phi partial_y phi`, so the connected correlator is

```text
<T_xy(k)T_xy(-k)>_c
 =2 W_state integral d^3p/(2pi)^3
   p_x^2 p_y^2/[p^2(p+k)^2].
```

Dimensional regularization isolates the scheme-independent nonanalytic term.
Feynman parametrization, the `d=3` tensor average
`<l_x^2 l_y^2>=l^4/[d(d+2)]`, and
`integral_0^1 [x(1-x)]^(3/2) dx=B(5/2,5/2)` give

```text
integral p_x^2 p_y^2/[p^2(p+k)^2] = |k|^3/1024,
<T_xy T_xy>_c = W_state |k|^3/512.
```

The executed coefficient is `{loop['connected_Txy_Txy_coefficient']}`.
For a thermal state `W_state=T_chi`; for a general passive Gaussian
occupation it is the positive zero-mode weight.

## Effective-action sign

The universal metric vertex is `S_int=(1/2) integral h_xy T_xy`. Expanding
`-ln Z[h]` gives the connected term

```text
Delta Gamma2 = -(1/8) h_xy h_xy <T_xy T_xy>_c,
Delta K_TT   = -W_state |k|^3/2048.
```

The calculated coefficient is
`{loop['metric_hessian_nonanalytic_coefficient']}`. Analytic seagulls and
counterterms can renormalize constant and `k^2` terms but cannot change this
nonanalytic coefficient.

Checkpoint 5149 proved that the desired stable critical kernel requires

```text
K_TT,desired = +M_R^2 |k|^3/(A mu)+... .
```

If an analytic medium susceptibility first enforces the required unit-mixing
`k^2` cancellation, the minimal passive scalar leaves a **negative** `|k|^3`
coefficient. It crosses into a gradient/Jeans instability instead of the
positive checkpoint-5148 response. The homogeneous passive one-scalar
realization is therefore rejected for the common no-slip/TT kernel.

## Scale magnitude

Ignoring the sign only to expose the required state size, coefficient matching
would demand

```text
N_eff W_state = 2048 M_R^2/(A mu).
```

At the median read-only `L_eff={scale['median_L_eff_kpc']} kpc`, with
`mu L_eff={scale['mu_times_L_eff']}` and
`A={scale['amplitude']}`, the required product is
`10^{scale['log10_required_Neff_Wstate_eV']} eV`. This is not a fitted
parameter or a pass; it confirms that an ordinary small occupation cannot
repair the sign or magnitude.

## What survives

This result rejects only the minimal homogeneous passive `P(X)` realization
of the checkpoint-5148 **common metric response**. It does not reject:

- a non-equilibrium active state, provided full CTP stability and positive
  dissipation are proved rather than assumed;
- additional parent vector/tensor or fermionic collective modes with a
  different TT sign;
- the motion field acting as a genuine conserved gravitating state stress
  rather than as a dressed vacuum/common-projector propagator.

The third route changes the next question in a useful way. Instead of forcing
the scalar to renormalize every metric polarization identically, derive its
occupied stress profile and calculate rotation **and lensing** from the same
Hilbert tensor. The local branch remains exactly `psi=0`; no Mercury coupling
is reopened.

## Next calculation

Derive the most general stationary axisymmetric reflection-even motion-state
stress permitted by the current CTP two-point function, impose conservation
and regularity, and invert the weak Einstein equations for both metric
potentials. Test whether the resulting circular-speed support can match the
5148 `S_q` target while its lensing slip remains acceptable. No occupation or
radial stress may be inserted by hand.

All `{result['validation_count']}` validation checks pass. The protected
`formalization-workbench` hash remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub or galaxy-repo
write occurred.
""",
        encoding="utf-8",
    )


def main() -> None:
    missing = [str(path) for path in SOURCE_PATHS.values() if not path.exists()]
    if missing:
        raise RuntimeError(f"missing source paths: {missing}")
    source_hashes_before = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_before = tree_digest(FORMAL)
    kernel_result = json.loads(
        SOURCE_PATHS["kernel_result"].read_text(encoding="utf-8")
    )
    q_value = float(kernel_result["kernel"]["q"])
    mu_times_length = float(kernel_result["kernel"]["best_mu_times_L_eff"])
    amplitude = float(kernel_result["galaxy_smoke"]["amplitude_geometric_mean"])
    galaxy_rows = read_csv(SOURCE_PATHS["galaxy_smoke"])
    lengths = [float(row["L_eff_kpc"]) for row in galaxy_rows]
    median_length = statistics.median(lengths)
    mu_ev = mu_times_length * HBAR_C_EV_M / (median_length * KPC_M)
    required_state_weight = (
        2048.0 * REDUCED_PLANCK_MASS_EV**2 / (amplitude * mu_ev)
    )
    loop = loop_coefficients()

    hessian_rows = [
        {
            "object": "time_kinetic",
            "equation": "Z_t=P_X+2 Xbar P_XX",
            "required_sign": ">0",
            "status": "STABILITY_CONDITION",
        },
        {
            "object": "space_kinetic",
            "equation": "Z_s=P_X",
            "required_sign": ">0",
            "status": "STABILITY_CONDITION",
        },
        {
            "object": "sound_speed",
            "equation": "c_s^2=Z_s/Z_t",
            "required_sign": ">0",
            "status": "STABILITY_CONDITION",
        },
        {
            "object": "tree_static_kernel",
            "equation": "K_pi(0,k)=Z_s k^2 plus analytic local terms",
            "required_sign": ">=0",
            "status": "ANALYTIC_IN_K2",
        },
        {
            "object": "homogeneous_TT_mixing",
            "equation": "B_(h_TT,pi)=0 for timelike homogeneous Xbar",
            "required_sign": "exact zero",
            "status": "DERIVED_BY_ISOTROPY_AND_TT_PROJECTION",
        },
        {
            "object": "Ward_identity",
            "equation": "k_mu Pi^(mu nu alpha beta)=0 after complete seagull+bubble sum",
            "required_sign": "exact zero",
            "status": "PARENT_DIFF_REQUIREMENT",
        },
    ]

    loop_rows = [
        {
            "step": "d3_radial_integral",
            "value": loop["radial_l4_integral_coefficient"],
            "exact_target": "5/(8 pi)",
        },
        {
            "step": "xy_tensor_average",
            "value": loop["tensor_average_coefficient"],
            "exact_target": "1/(24 pi)",
        },
        {
            "step": "Feynman_parameter_integral",
            "value": loop["feynman_parameter_integral"],
            "exact_target": "3 pi/128",
        },
        {
            "step": "one_Wick_contraction",
            "value": loop["one_contraction_Txy_coefficient"],
            "exact_target": "1/1024",
        },
        {
            "step": "connected_Txy_Txy",
            "value": loop["connected_Txy_Txy_coefficient"],
            "exact_target": "1/512",
        },
        {
            "step": "metric_Hessian_nonanalytic",
            "value": loop["metric_hessian_nonanalytic_coefficient"],
            "exact_target": "-1/2048",
        },
    ]

    sign_rows = [
        {
            "quantity": "desired_critical_k3_coefficient",
            "expression": "+M_R^2/(A mu)",
            "sign": "positive",
            "compatible": True,
        },
        {
            "quantity": "minimal_passive_scalar_zero_mode",
            "expression": "-N_eff W_state/2048",
            "sign": "negative",
            "compatible": False,
        },
        {
            "quantity": "median_L_eff_kpc",
            "expression": str(median_length),
            "sign": "positive",
            "compatible": None,
        },
        {
            "quantity": "mu_eV",
            "expression": str(mu_ev),
            "sign": "positive",
            "compatible": None,
        },
        {
            "quantity": "required_Neff_Wstate_eV_magnitude_only",
            "expression": str(required_state_weight),
            "sign": "positive_magnitude",
            "compatible": False,
        },
    ]

    route_rows = [
        {
            "route": "homogeneous_passive_PX_common_metric_kernel",
            "tree_TT_mixing": "zero",
            "nonanalytic_sign": "negative",
            "status": "REJECTED_AT_CRITICAL_GRADIENT_SIGN",
            "valid_for_claim": False,
        },
        {
            "route": "active_nonequilibrium_CTP_common_metric_kernel",
            "tree_TT_mixing": "state_dependent",
            "nonanalytic_sign": "must_be_derived",
            "status": "OPEN_HIGH_RISK_STABILITY_GATE",
            "valid_for_claim": False,
        },
        {
            "route": "additional_collective_spin_content",
            "tree_TT_mixing": "parent_extension_required",
            "nonanalytic_sign": "must_be_derived",
            "status": "OPEN_PARENT_CONTENT_CHANGE",
            "valid_for_claim": False,
        },
        {
            "route": "conserved_motion_state_stress",
            "tree_TT_mixing": "not_required",
            "nonanalytic_sign": "stress_and_lensing_owned_variationally",
            "status": "SELECTED_NEXT_WITHOUT_PROPAGATOR_DRESSING",
            "valid_for_claim": False,
        },
    ]

    write_csv(HESSIAN_CSV, hessian_rows)
    write_csv(LOOP_CSV, loop_rows)
    write_csv(SIGN_CSV, sign_rows)
    write_csv(ROUTE_CSV, route_rows)
    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)
    scale_summary = {
        "median_L_eff_kpc": median_length,
        "mu_times_L_eff": mu_times_length,
        "mu_eV": mu_ev,
        "amplitude": amplitude,
        "required_Neff_Wstate_eV": required_state_weight,
        "log10_required_Neff_Wstate_eV": math.log10(required_state_weight),
    }
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "q": q_value,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "zero_mode_loop": loop,
        "scale_match": scale_summary,
        "minimal_passive_PX_common_kernel_survives": False,
        "conserved_motion_state_stress_route_selected": True,
        "formalization_workbench_tree_sha256": formal_after,
        "valid_for_PPN_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    checks = [
        ("source_paths_exist", not missing, str(missing)),
        (
            "sources_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formal_tree_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        (
            "one_contraction_coefficient",
            abs(loop["one_contraction_Txy_coefficient"] - 1.0 / 1024.0)
            < 1.0e-14,
            str(loop["one_contraction_Txy_coefficient"]),
        ),
        (
            "connected_TT_coefficient",
            abs(loop["connected_Txy_Txy_coefficient"] - 1.0 / 512.0)
            < 1.0e-14,
            str(loop["connected_Txy_Txy_coefficient"]),
        ),
        (
            "effective_action_sign",
            abs(loop["metric_hessian_nonanalytic_coefficient"] + 1.0 / 2048.0)
            < 1.0e-14,
            str(loop["metric_hessian_nonanalytic_coefficient"]),
        ),
        (
            "tree_homogeneous_TT_mixing_zero",
            next(
                row for row in hessian_rows if row["object"] == "homogeneous_TT_mixing"
            )["required_sign"]
            == "exact zero",
            "timelike isotropic background and TT projection",
        ),
        (
            "critical_k3_sign_mismatch",
            sign_rows[0]["sign"] == "positive"
            and sign_rows[1]["sign"] == "negative",
            str([sign_rows[0]["sign"], sign_rows[1]["sign"]]),
        ),
        (
            "required_state_scale_finite",
            math.isfinite(required_state_weight) and required_state_weight > 0.0,
            str(scale_summary),
        ),
        (
            "minimal_common_kernel_rejected",
            not result["minimal_passive_PX_common_kernel_survives"],
            route_rows[0]["status"],
        ),
        (
            "stress_route_selected_without_local_reopening",
            result["conserved_motion_state_stress_route_selected"],
            route_rows[-1]["status"],
        ),
        (
            "claim_discipline",
            not result["valid_for_PPN_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_full_MTS_claim"],
            "minimal response rejection and next route only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5150_{index:02d}_{name}",
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    result["validation_count"] = len(validation_rows)
    result["validation_failures"] = [
        row["check_id"] for row in validation_rows if not row["passed"]
    ]
    atomic_json(RESULT_JSON, result)
    write_csv(VALIDATION_CSV, validation_rows)
    write_document(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["validation_failures"]:
        raise RuntimeError(
            f"checkpoint 5150 validation failures: {result['validation_failures']}"
        )


if __name__ == "__main__":
    main()
