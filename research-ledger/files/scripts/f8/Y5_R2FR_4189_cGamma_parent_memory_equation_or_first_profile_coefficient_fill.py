from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4189"
BRANCH_ID = "MTS_R2FR_Y5_CGAMMA_PROFILE_PROJECTION_CLASSIFIER_4189"
DECISION = (
    "CGAMMA_METRIC_GDOT_PROJECTION_SPLIT_DERIVED_FIRST_SYMBOLIC_COEFFICIENTS_FILLED_"
    "PARENT_MEMORY_EQUATION_STILL_OPEN_NONCLAIM"
)
DOC_PATH = POST / "4189-Y5-R2FR-cGamma-parent-memory-equation-or-first-profile-coefficient-fill.md"
FORMAL_205_PATH = FORMAL / "205-PPC4161-cGamma-profile-projection-coefficient-gate.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-030"
SPINE_MARKER = "PPC4161_CGAMMA_PROFILE_PROJECTION_COEFFICIENT_GATE_4189"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_PROFILE_PROJECTION_COEFFICIENT_GATE_4189"
NEXT_TARGET = "4190-Y5-R2FR-local-memory-stationarity-gradient-zero-lemma-or-dtXi-bound.md"

SOURCES = {
    "SRC4189_00_4188_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4188_NEXT_TARGET.csv",
        "fill first C_Gamma_metric or C_Gamma_Gdot profile/projection coefficient",
        "4188 handoff.",
    ),
    "SRC4189_01_4188_strictest": (
        SOURCE_DIR / "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS.csv",
        "C_Gamma_Gdot",
        "4188 strictest product bounds.",
    ),
    "SRC4189_02_4188_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER.csv",
        "Delta_Gdot_over_G = C_Gamma_Gdot",
        "4188 product-bound runner.",
    ),
    "SRC4189_03_formal_204": (
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "|c_Gamma * profile_a| <= B_a / |J_a^Gamma|",
        "formal finite-product law.",
    ),
    "SRC4189_04_formal_203": (
        FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md",
        "S_Gamma[U] = integral_U sqrt(-g_obs) c_Gamma Gamma_mem I_local",
        "formal c_Gamma residual action.",
    ),
    "SRC4189_05_core_repair": (
        FORMAL / "10-core-consistency-repair.md",
        "u^μ∇_μχ + χ/τ_Γ = source(Γ_mem, matter)",
        "core memory/exchange clue; not a full Gamma_mem parent equation.",
    ),
    "SRC4189_06_equation_register": (
        FORMAL / "05-equation-register.md",
        "K_MTS = P_MTS[psi,Gamma_mem,matter,g,L_cg]",
        "equation register says memory stress is still closure target.",
    ),
    "SRC4189_07_units": (
        FORMAL / "09-canonical-notation-and-units.md",
        "units remain open until its action/source law is chosen",
        "units warning.",
    ),
    "SRC4189_08_kappa_lock": (
        FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md",
        "Gdot/G = D_t ln(kappa_* Z_H)",
        "Gdot coupling law before c_Gamma residual reactivation.",
    ),
    "SRC4189_09_source_descent": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "R_A^G = D_A ln G_eff",
        "source-measure drift closure relation.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def strict_bound(product: str) -> Dict[str, str]:
    for row in parse_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS.csv"):
        if row["effective_product"] == product:
            return row
    raise KeyError(product)


def runner_bound(observable: str) -> Dict[str, str]:
    for row in parse_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER.csv"):
        if row["observable"] == observable:
            return row
    raise KeyError(observable)


def memory_equation_sweep_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MES4189_0_full_Gamma_parent_equation",
            "L_Gamma Gamma_mem = J_Gamma with sign, source, domain and boundary data",
            "not_found",
            "No current source supplies a complete parent-owned Gamma_mem operator/source/boundary system.",
            "needed for theorem-zero/no-hair",
        ),
        (
            "MES4189_1_exchange_clue",
            "u^mu nabla_mu chi + chi/tau_Gamma = source(Gamma_mem,matter)",
            "clue_only",
            "This is an exchange/susceptibility equation for chi, not a closed Gamma_mem dynamics.",
            "can inspire stationarity lemma but cannot sign c_Gamma zero",
        ),
        (
            "MES4189_2_closure_register",
            "K_MTS = P_MTS[psi,Gamma_mem,matter,g,L_cg]",
            "closure_target",
            "The equation register explicitly says this is not yet action-derived.",
            "must be replaced by parent action or bounded residual",
        ),
        (
            "MES4189_3_units",
            "Gamma_mem units/action/source law open",
            "open",
            "Direct numeric c_Gamma is impossible until the parent normalization is fixed.",
            "work with product coefficients only",
        ),
        (
            "MES4189_4_Gdot_route",
            "Gdot/G = D_t ln(kappa_* Z_H) plus any c_Gamma-induced local product drift",
            "formula_ready",
            "kappa/source drift is privately zero, so c_Gamma_Gdot can be isolated as D_t of the memory product.",
            "first coefficient law filled symbolically",
        ),
    ]
    return [
        {
            **common(),
            "sweep_id": sweep_id,
            "target": target,
            "status": status,
            "finding": finding,
            "consequence": consequence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for sweep_id, target, status, finding, consequence in rows
    ]


def projection_grammar_rows() -> List[Dict[str, str]]:
    gdot = strict_bound("C_Gamma_Gdot")
    metric = strict_bound("C_Gamma_metric")
    vector = strict_bound("C_Gamma_vector")
    stress = strict_bound("C_Gamma_stress")
    rows = [
        (
            "PG4189_0_scalar_time",
            "scalar time-drift coefficient",
            "Xi_0(t,x) := N_0[P_loc Gamma_mem]; C_Gamma_Gdot = c_Gamma D_t Xi_0",
            gdot["max_abs_effective_product"],
            gdot["units"],
            "D_t Xi_0 = 0 or product below bound",
            "filled_symbolic",
        ),
        (
            "PG4189_1_scalar_gradient",
            "preferred-location/spatial-gradient coefficient",
            "C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|",
            metric["max_abs_effective_product"],
            "dimensionless",
            "grad_perp Xi_0 = 0 or product below xi bound",
            "split_from_coarse_C_Gamma_metric",
        ),
        (
            "PG4189_2_isotropic_metric_amplitude",
            "isotropic metric amplitude coefficient",
            "C_Gamma_gamma = c_Gamma Xi_gamma and C_Gamma_beta = c_Gamma Xi_beta",
            runner_bound("gamma_minus_1")["max_abs_effective_product"],
            "dimensionless",
            "EH-proportional constant part is calibration-only; non-EH isotropic part must satisfy gamma/beta/orbit bounds",
            "filled_symbolic",
        ),
        (
            "PG4189_3_vector_memory",
            "vector/preferred-frame coefficient",
            "C_Gamma_vector = c_Gamma |Xi_i|",
            vector["max_abs_effective_product"],
            vector["units"],
            "Xi_i = 0 by local isotropy/quotient silence or product below alpha bounds",
            "classified_severe_if_active",
        ),
        (
            "PG4189_4_stress_memory",
            "hidden stress/conservation coefficient",
            "C_Gamma_stress = c_Gamma |nabla_mu Delta T_Gamma^{mu nu}|_norm",
            stress["max_abs_effective_product"],
            stress["units"],
            "Hilbert conservation kills it only if memory stress is included in T_total or has zero divergence",
            "classified",
        ),
    ]
    return [
        {
            **common(),
            "projector_id": projector_id,
            "component": component,
            "coefficient_law": law,
            "current_bound": bound,
            "bound_units": units,
            "zero_or_pass_condition": condition,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for projector_id, component, law, bound, units, condition, status in rows
    ]


def first_coefficient_fill_rows() -> List[Dict[str, str]]:
    gdot = strict_bound("C_Gamma_Gdot")
    xi = strict_bound("C_Gamma_metric")
    gamma = runner_bound("gamma_minus_1")
    beta = runner_bound("beta_minus_1")
    orbit = runner_bound("((2+2gamma-beta)/3)-1")
    rows = [
        (
            "FCF4189_0_CGamma_Gdot",
            "C_Gamma_Gdot",
            "c_Gamma D_t Xi_0",
            gdot["max_abs_effective_product"],
            gdot["units"],
            "If Gamma_mem is locally stationary in the compact collar, D_t Xi_0=0 and this channel vanishes.",
            "conditional_zero_or_bound",
        ),
        (
            "FCF4189_1_CGamma_xi",
            "C_Gamma_metric_gradient",
            "c_Gamma L_loc |grad_perp Xi_0|",
            xi["max_abs_effective_product"],
            "dimensionless",
            "If local memory is homogeneous/isotropic after quotient projection, grad_perp Xi_0=0 and preferred-location xi is not the active metric bound.",
            "coarse_metric_split",
        ),
        (
            "FCF4189_2_CGamma_gamma",
            "C_Gamma_metric_iso_gamma",
            "c_Gamma Xi_gamma",
            gamma["max_abs_effective_product"],
            gamma["units"],
            "Applies only to non-EH-proportional spatial-curvature response; constant EH-proportional rescaling belongs to calibration.",
            "symbolic_bound",
        ),
        (
            "FCF4189_3_CGamma_beta",
            "C_Gamma_metric_iso_beta",
            "c_Gamma Xi_beta",
            beta["max_abs_effective_product"],
            beta["units"],
            "Applies to nonlinear-potential response not already fixed by the EH self-interaction.",
            "symbolic_bound",
        ),
        (
            "FCF4189_4_CGamma_orbit_combo",
            "C_Gamma_metric_orbit_combo",
            "c_Gamma (2 Xi_gamma - Xi_beta)/3",
            orbit["max_abs_effective_product"],
            orbit["units"],
            "Orbital combo bound is the clean local-GR/Newton readout after gamma/beta split.",
            "symbolic_bound",
        ),
    ]
    return [
        {
            **common(),
            "fill_id": fill_id,
            "coefficient": coefficient,
            "filled_formula": formula,
            "max_abs_product": max_abs,
            "units": units,
            "interpretation": interpretation,
            "status": status,
            "numeric_parent_value_available": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for fill_id, coefficient, formula, max_abs, units, interpretation, status in rows
    ]


def scenario_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SC4189_0_support_nohair",
            "P_loc Gamma_mem = 0 and Gamma_perp=0",
            "all C_Gamma channels zero",
            "would pass all product bounds",
            "not closed because parent memory equation/no-hair is unsigned",
        ),
        (
            "SC4189_1_stationary_homogeneous_scalar",
            "D_t Xi_0=0, grad_perp Xi_0=0, Xi_i=0, stress divergence=0",
            "C_Gamma_Gdot=0; C_Gamma_xi=0; vector/stress zero; isotropic metric amplitude remains",
            "safe only if isotropic part is EH-proportional calibration or below gamma/beta/orbital bounds",
            "best current derivation target",
        ),
        (
            "SC4189_2_time_drifting_scalar",
            "D_t Xi_0 nonzero",
            "requires |c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1",
            "very tight but cleanly testable",
            "needs local stationarity lemma or numeric drift profile",
        ),
        (
            "SC4189_3_spatial_gradient_scalar",
            "grad_perp Xi_0 nonzero",
            "requires |c_Gamma L_loc grad_perp Xi_0| <= 4e-9",
            "tests preferred-location/local-background leakage",
            "needs local homogeneity/gradient-zero lemma or bound",
        ),
        (
            "SC4189_4_vector_or_momentum_memory",
            "Xi_i or self-acceleration channel nonzero",
            "alpha3-style bounds can be as tight as 4e-20",
            "not the default bound unless derivation creates vector/momentum leakage",
            "do not scarecrow; classify before scoring",
        ),
        (
            "SC4189_5_hidden_stress_memory",
            "memory stress is not included in conserved T_total or has nonzero divergence",
            "zeta/stress product bounds activate",
            "Hilbert stress owner may kill this if memory stress is consistently included",
            "needs conservation-owned memory stress derivation",
        ),
    ]
    return [
        {
            **common(),
            "scenario_id": scenario_id,
            "scenario": scenario,
            "channel_result": result,
            "bound_consequence": consequence,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for scenario_id, scenario, result, consequence, next_action in rows
    ]


def unit_smoke_rows() -> List[Dict[str, str]]:
    rows = []
    for row in first_coefficient_fill_rows():
        bound = float(row["max_abs_product"])
        unit_projection = 1.0
        pass_unit = unit_projection <= bound
        rows.append(
            {
                **common(),
                "smoke_id": f"US4189_{row['fill_id']}",
                "coefficient": row["coefficient"],
                "unit_projection_value": f"{unit_projection:.17g}",
                "max_abs_product": row["max_abs_product"],
                "units": row["units"],
                "unit_projection_passes": str(pass_unit),
                "required_suppression_factor": f"{bound:.17g}",
                "meaning": "Unit-normalized nonzero c_Gamma projection is unsafe unless theorem-zero or suppression beats this factor.",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4189_0_coarse_metric_split", "Do not apply xi/preferred-location bound to purely isotropic stationary metric memory without proving a preferred-location projection."),
        ("FW4189_1_product_not_cGamma", "All bounds remain product bounds; no direct c_Gamma value is claimed."),
        ("FW4189_2_stationary_not_assumed", "D_t Xi_0=0 and grad Xi_0=0 are theorem targets, not assumptions."),
        ("FW4189_3_no_alpha3_scarecrow", "The alpha3 bound is relevant only if the derivation creates vector/momentum nonconservation."),
        ("FW4189_4_no_public_pass", "No local-GR, PPN, clock, orbital or R10 pass is claimed from this classifier."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "enforced": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "parent_memory_equation_found": "False",
            "coarse_CGamma_metric_split": "True",
            "CGamma_Gdot_formula_filled": "True",
            "CGamma_gradient_xi_formula_filled": "True",
            "stationary_homogeneous_scalar_target_selected": "True",
            "numeric_parent_value_available": "False",
            "public_local_GR_claim_allowed": "False",
            "formal_205_written": str(FORMAL_205_PATH.exists()),
            "claim_register_action": claim_action,
            "packet_180_action": packet_action,
            "spine_action": spine_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4189 splits c_Gamma into physical projection channels and fills the first symbolic coefficient laws. The next real derivation is local stationarity/homogeneity: D_t Xi_0=0 and grad_perp Xi_0=0, or bounded values for them.",
            "route_A": "derive stationary homogeneous local memory lemma from relaxation/equilibrium equation",
            "route_B": "fill dtXi_0 and gradXi_0 profile coefficients and compare with Gdot/xi bounds",
            "recommended_first": "prove or bound D_t Xi_0 before R10/vector lanes",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc_text() -> str:
    return f"""# 205 - PPC4161 c_Gamma Profile Projection Coefficient Gate

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove `c_Gamma=0`, does not supply a numeric parent value, and does not claim local GR. It refines the 4188 coarse product bounds into physical projection channels.

## Parent Equation Sweep

The current corpus does not contain a complete parent-owned equation:

```text
L_Gamma Gamma_mem = J_Gamma
```

with signed operator, source, domain and boundary data. The closest available relation is an exchange/susceptibility clue for `chi`, not a closed `Gamma_mem` dynamics. Therefore the theorem-zero route remains open.

## First Coefficient Split

Let:

```text
Xi_0(t,x) := N_0[P_loc Gamma_mem].
```

Then the first two useful local products are:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0,
|C_Gamma_Gdot| <= 2.42e-14 yr^-1.

C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|,
|C_Gamma_xi| <= 4e-9.
```

This splits the old coarse `C_Gamma_metric` row into time drift, preferred-location gradient and isotropic metric response. That matters: the `xi` bound should not be used as a scarecrow against a purely stationary homogeneous scalar memory term.

## Best Current Target

The best next derivation is the stationary homogeneous scalar local-memory lemma:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0,
Xi_i = 0,
nabla_mu Delta T_Gamma^{{mu nu}} = 0.
```

If this closes, the tight `Gdot`, `xi`, vector and stress channels vanish and only the isotropic EH-proportional/calibration question remains. If it fails, `4188/4189` give explicit product bounds.

## Next Gate

`{NEXT_TARGET}` should derive the local stationarity/gradient-zero lemma or fill `D_t Xi_0` and `grad_perp Xi_0` profile coefficients.
"""


def checkpoint_doc_text() -> str:
    return f"""# 4189 - c_Gamma Parent Memory Equation Or First Profile Coefficient Fill

Generated by: `post-checkpoint-work/scripts/Y5_R2FR_4189_cGamma_parent_memory_equation_or_first_profile_coefficient_fill.py`

## Summary

4189 searches for a complete parent `Gamma_mem` equation and does not find one. Instead of stopping there, it fills the first useful symbolic profile/projection laws:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0
C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|
```

and splits the coarse `C_Gamma_metric` row into time-drift, spatial-gradient/preferred-location and isotropic-metric pieces.

## Decision

`{DECISION}`

## Result

The next derivation target is no longer vague. Prove local stationarity/homogeneity of `Xi_0`, or fill bounded `D_t Xi_0` / `grad_perp Xi_0` profile rows.
"""


def ensure_docs() -> None:
    FORMAL_205_PATH.write_text(formal_doc_text(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc_text(), encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The c_Gamma local-memory residual has been split into physical projection channels, with first symbolic formulas for Gdot and preferred-location metric leakage.",
            "current_evidence": "4189 parent-equation sweep, projection grammar, first coefficient fill, scenario classifier and unit-projection smoke rows.",
            "status": "private_projection_classifier_nonclaim_parent_memory_equation_open",
            "next_test": "Derive D_t Xi_0=0 and grad_perp Xi_0=0 from the local memory stationarity/relaxation law, or fill bounded profile coefficients.",
            "key_risk": "Using the strict xi or alpha3 bounds on the wrong projection channel would overstate failure; assuming stationarity would smuggle closure.",
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "appended"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4189 c_Gamma Profile Projection Coefficient Gate

Marker: `{PACKET_MARKER}`

4189 splits the coarse `C_Gamma_metric` bound into physical projection channels:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0,
C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|.
```

The parent `Gamma_mem` equation is still not found, but the next derivation is now sharp: prove local stationarity/homogeneity of `Xi_0`, or fill `D_t Xi_0` and `grad_perp Xi_0` profile coefficients.
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "appended"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 c_Gamma Profile Projection Coefficient Gate

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4189 refines the `c_Gamma` product-bound branch. The coarse metric product is split into:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0,
C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|,
C_Gamma_gamma/beta = c_Gamma Xi_gamma/beta.
```

The parent `Gamma_mem` equation is still open, but the next target is no longer generic: prove or bound local stationarity and homogeneity of the scalar memory projection `Xi_0`.
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "appended"


def validation_rows(rows_by_name: Dict[str, List[Dict[str, str]]], claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    source_register = rows_by_name["P8_Y5_R2FR_4189_SOURCE_REGISTER"]
    status = rows_by_name["P8_Y5_R2FR_4189_STATUS"][0]
    fills = rows_by_name["P8_Y5_R2FR_4189_FIRST_COEFFICIENT_FILL"]
    grammar = rows_by_name["P8_Y5_R2FR_4189_PROJECTION_GRAMMAR"]
    all_generated_rows = [
        row
        for name, rows in rows_by_name.items()
        if name != "P8_Y5_R2FR_4189_SOURCE_REGISTER"
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4189_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source_register), str(source_register)),
        ("VAL4189_1_source_tokens", "all source tokens found", all(row["required_text_found"] == "True" for row in source_register), str(source_register)),
        ("VAL4189_2_parent_equation_open", "parent memory equation remains open", status["parent_memory_equation_found"] == "False", str(status)),
        ("VAL4189_3_metric_split", "coarse C_Gamma_metric split exists", status["coarse_CGamma_metric_split"] == "True" and len(grammar) >= 5, str(grammar)),
        ("VAL4189_4_gdot_formula", "C_Gamma_Gdot formula filled", any(row["coefficient"] == "C_Gamma_Gdot" and "D_t Xi_0" in row["filled_formula"] for row in fills), str(fills)),
        ("VAL4189_5_xi_formula", "C_Gamma_xi/gradient formula filled", any(row["coefficient"] == "C_Gamma_metric_gradient" and "grad_perp Xi_0" in row["filled_formula"] for row in fills), str(fills)),
        ("VAL4189_6_unit_smoke", "unit smoke rows show nonzero projections require suppression", len(rows_by_name["P8_Y5_R2FR_4189_UNIT_PROJECTION_SMOKE"]) >= 5, "unit smoke rows present"),
        ("VAL4189_7_no_public_claim", "public local GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4189_8_formal_205", "formal 205 exists with marker", FORMAL_205_PATH.exists() and SPINE_MARKER in read_text(FORMAL_205_PATH), str(FORMAL_205_PATH)),
        ("VAL4189_9_checkpoint_doc", "checkpoint doc exists and has decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4189_10_claim_row", "claim register contains L-030", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4189_11_packet_180", "packet marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4189_12_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4189_13_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
    ]
    validation = [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(passed),
            "detail": detail,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed, detail in checks
    ]
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4189_14_py_compile",
            "check": "script compiles and __pycache__ removed",
            "passed": str(not pycache.exists()),
            "detail": str(SCRIPT_PATH),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    ensure_docs()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4189_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4189_MEMORY_EQUATION_SWEEP": memory_equation_sweep_rows(),
        "P8_Y5_R2FR_4189_PROJECTION_GRAMMAR": projection_grammar_rows(),
        "P8_Y5_R2FR_4189_FIRST_COEFFICIENT_FILL": first_coefficient_fill_rows(),
        "P8_Y5_R2FR_4189_SCENARIO_CLASSIFIER": scenario_rows(),
        "P8_Y5_R2FR_4189_UNIT_PROJECTION_SMOKE": unit_smoke_rows(),
        "P8_Y5_R2FR_4189_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4189_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4189_NEXT_TARGET": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(SOURCE_DIR / f"{name}.csv", rows)

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4189_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4189 validation failed: {failed}")

    print(DECISION)
    print(f"formal={FORMAL_205_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
