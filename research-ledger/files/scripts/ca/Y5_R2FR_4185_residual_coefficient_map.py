from __future__ import annotations

import csv
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

CHECKPOINT = "4185"
BRANCH_ID = "MTS_R2FR_Y5_EXTRA_INVARIANT_RESIDUAL_COEFFICIENT_MAP_4185"
DECISION = (
    "RESIDUAL_COEFFICIENT_ARENA_MAP_WRITTEN_PARENT_ZERO_OR_SCALE_LAWS_MISSING_"
    "SOURCE_BOUND_INTERFACES_READY_NONCLAIM"
)
DOC_PATH = POST / "4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
FORMAL_201_PATH = FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-026"
SPINE_MARKER = "PPC4161_EXTRA_INVARIANT_RESIDUAL_COEFFICIENT_MAP_4185"
PACKET_MARKER = "PPC4161_PACKET_EXTRA_INVARIANT_RESIDUAL_COEFFICIENT_MAP_4185"
NEXT_TARGET = "4186-Y5-R2FR-same-coframe-source-memory-zero-law-for-cD-deltaKappa-cGamma-or-bound-runner.md"

SOURCES = {
    "SRC4185_00_4184_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4184_NEXT_TARGET.csv",
        "derive parent scale laws or zeros",
        "4184 handoff asking for parent zeros/scale laws or source-backed bounds.",
    ),
    "SRC4185_01_formal_200": (
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "Each coefficient must be parent-zero",
        "formal 200 residual coefficient firewall.",
    ),
    "SRC4185_02_4184_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv",
        "local memory coupling c_Gamma",
        "4184 residual coefficient ledger.",
    ),
    "SRC4185_03_ppn_vector": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "private PPN residual vector structure.",
    ),
    "SRC4185_04_local_bounds": (
        FORMAL / "189-PPC4161-local-empirical-validation-pack.md",
        "Source-Backed Bound Classes",
        "existing source-backed comparator pack and caveats.",
    ),
    "SRC4185_05_threshold_spec": (
        FORMAL / "102-transition-closure-observable-threshold-spec.md",
        "S_PPN_residual_norm",
        "older observable threshold/residual norm spec.",
    ),
    "SRC4185_06_R10_join": (
        SOURCE_DIR / "P8_Y5_R2FR_3797_R10_BOUND_JOIN_LEDGER.csv",
        "AVAILABLE_NONCLAIM_REVIEW_REQUIRED",
        "R10 bound-curve availability and nonclaim review state.",
    ),
    "SRC4185_07_orbital_readiness": (
        SOURCE_DIR / "P8_Y5_R2FR_3937_R10_OR_ORBITAL_READINESS_COMPARISON.csv",
        "orbital_ephemeris",
        "orbital-first readiness comparison.",
    ),
    "SRC4185_08_source_coupling": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "calibrated source coupling relation and numeric-G firewall.",
    ),
    "SRC4185_09_claim_L025": (
        CLAIMS_PATH,
        "conditional_Palatini_IR_selector_nonclaim",
        "latest claim row before residual coefficient map.",
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


def coefficient_map_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RC4185_0_cD",
            "c_D",
            "second metric / disformal matter-EM owner",
            "same observed coframe violation: matter or Maxwell-Hodge sees metric not equal to g_obs",
            "WEP eta, clock redshift, EM propagation, Poynting/Hilbert stress mismatch",
            "derive same-coframe parent functor so c_D=0",
            "source-backed WEP/clock/EM bound if finite",
            "priority_1_root_metric_owner",
        ),
        (
            "RC4185_1_deltaKappa",
            "delta_kappa",
            "source-coupling drift",
            "kappa_eff or Hilbert source charge varies by time/species/frame/environment",
            "Gdot/G, orbital GM consistency, clock/local-G variation, WEP source dependence",
            "derive topological/source-measure lock so delta_kappa=0",
            "measured-G envelope, LLR Gdot/G, orbital ephemeris residual",
            "priority_2_newton_coupling_owner",
        ),
        (
            "RC4185_2_cGamma",
            "c_Gamma",
            "local memory coupling",
            "Gamma_mem multiplies local curvature/torsion/source invariant and creates local hair",
            "PPN residual vector, clocks, R10 finite-range, local-G variation",
            "derive local screening/silence or compact-support decoupling so c_Gamma=0 locally",
            "PPN/clock/R10 bound if finite",
            "priority_3_MTS_specific_local_risk",
        ),
        (
            "RC4185_3_cT",
            "c_T",
            "torsion-square coefficient",
            "irreducible torsion modes survive outside algebraic torsionless EC branch",
            "PPN preferred-frame/spin coupling, R10/contact force, clock/spin tests",
            "derive torsion algebraic zero/heavy mass from parent normal form",
            "PPN/R10/spin-clock bound if finite",
            "priority_4_geometry_extra_mode",
        ),
        (
            "RC4185_4_cR2",
            "c_R2 or M_R",
            "curvature-square / higher-derivative coefficient",
            "R2/Ricci2/Riemann2 creates finite-range scalar/tensor correction or short-range Yukawa tail",
            "R10 alpha(lambda), orbital precession, cosmology consistency",
            "derive high parent mass scale M_R or zero coefficient",
            "R10 curve or orbital bound if finite",
            "priority_5_finite_range_EFT_tail",
        ),
        (
            "RC4185_5_cBdy",
            "c_bdy",
            "unrouted boundary or edge charge",
            "boundary/topological/radiative contribution enters bulk Hamiltonian/source readout",
            "orbital mass leakage, radiation reaction, clock/source drift",
            "derive fixed/exact/Hamiltonian-routed boundary so c_bdy=0 in bulk",
            "flux/orbital/radiative bound if finite",
            "priority_6_boundary_route_guard",
        ),
    ]
    return [
        {
            **common(),
            "map_id": map_id,
            "coefficient": coefficient,
            "residual_family": family,
            "physical_failure_mode": failure,
            "primary_arenas": arenas,
            "parent_zero_or_scale_law_route": parent_route,
            "fallback_bound_route": bound_route,
            "priority": priority,
            "coefficient_value_status": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for map_id, coefficient, family, failure, arenas, parent_route, bound_route, priority in rows
    ]


def bound_interface_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BI4185_0_PPN",
            "PPN_vector",
            "delta_gamma, delta_beta, alpha_i, xi, zeta_i, Gdot/G",
            "c_D, c_Gamma, c_T, delta_kappa",
            "existing private vector source; finite coefficients need projection Jacobian J_PPN",
            "not_scoreable_until_projection_coefficients_exist",
        ),
        (
            "BI4185_1_R10",
            "R10_Yukawa",
            "alpha(lambda) or product-bound row",
            "c_R2, c_T, c_Gamma",
            "candidate bound curve and score gate exist but remain nonclaim/review-required",
            "not_scoreable_until_alpha_projection_and_curve_promotion_exist",
        ),
        (
            "BI4185_2_WEP",
            "WEP_eta",
            "composition/source-label differential acceleration",
            "c_D, delta_kappa, c_Gamma",
            "source-backed class exists from comparator pack",
            "not_scoreable_until material/source projection coefficients exist",
        ),
        (
            "BI4185_3_clock",
            "clock_redshift_and_frequency",
            "redshift alpha, clock-source drift, local memory/time response",
            "c_D, c_Gamma, delta_kappa, c_T",
            "source-backed class exists from comparator pack",
            "not_scoreable_until clock observable projection exists",
        ),
        (
            "BI4185_4_orbital",
            "orbital_ephemeris",
            "perihelion/precession, GM consistency, inverse-square, Gdot/G",
            "delta_kappa, c_R2, c_bdy, c_Gamma",
            "orbital-first comparison already selected as cleaner than detached R10",
            "not_scoreable_until ephemeris/source rows or analytic envelope exist",
        ),
        (
            "BI4185_5_EM",
            "EM_propagation_Poynting",
            "Hodge owner, speed/polarization, stress-energy flux",
            "c_D, c_bdy, c_Gamma",
            "Maxwell-Hodge owner theorem exists only inside private selector",
            "not_scoreable_until global same-coframe/EM projection is parent-signed",
        ),
    ]
    return [
        {
            **common(),
            "interface_id": interface_id,
            "arena": arena,
            "observable": observable,
            "coefficients": coefficients,
            "available_source_or_scaffold": source,
            "score_status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for interface_id, arena, observable, coefficients, source, status in rows
    ]


def parent_scale_law_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PSL4185_0_same_coframe",
            "c_D",
            "q-owned single observed coframe functor: all matter and EM actions descend through g_obs",
            "c_D=0 if globally parent-signed",
            "not yet global; private selector only",
        ),
        (
            "PSL4185_1_source_lock",
            "delta_kappa",
            "topological kappa lock plus Hilbert source-measure descent with no species/readout multiplier",
            "delta_kappa=0 if parent-owned",
            "numeric G still calibrated; global adoption open",
        ),
        (
            "PSL4185_2_memory_silence",
            "c_Gamma",
            "compact local branch projects Gamma_mem only into screened/routed invariants or no local support",
            "c_Gamma=0 locally or c_Gamma suppressed by parent screening scale",
            "central MTS-specific open debt",
        ),
        (
            "PSL4185_3_torsion_mass",
            "c_T",
            "Palatini/EC algebraic torsion with spinless local matter, or torsion mass above local test range",
            "c_T=0/heavy",
            "needs parent normal-form clause or spin/torsion bound",
        ),
        (
            "PSL4185_4_higher_derivative_scale",
            "c_R2/M_R",
            "parent low-energy expansion scale suppresses curvature-square terms",
            "M_R large enough that lambda_R below tested range or alpha below bounds",
            "needs parent scale or R10/orbital bound",
        ),
        (
            "PSL4185_5_boundary_route",
            "c_bdy",
            "boundary terms exact, fixed, topological, or Hamiltonian-routed outside bulk local equations",
            "c_bdy=0 as bulk source",
            "private local no-flux exists; global adoption open",
        ),
    ]
    return [
        {
            **common(),
            "scale_law_id": law_id,
            "coefficient": coefficient,
            "parent_law_candidate": law,
            "zero_or_scale_consequence": consequence,
            "current_status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for law_id, coefficient, law, consequence, status in rows
    ]


def scorecard_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SC4185_0",
            "c_D",
            "highest",
            "fails WEP/clock/EM source ownership if nonzero",
            "derive same-coframe parent functor first",
            "do_not_start_with_R10",
        ),
        (
            "SC4185_1",
            "delta_kappa",
            "highest",
            "directly affects Newton coupling, orbital GM, and local G drift",
            "derive source-lock or orbital/LLR envelope",
            "core_GR_to_Newton_bridge",
        ),
        (
            "SC4185_2",
            "c_Gamma",
            "highest",
            "MTS-specific local memory hair can reopen PPN/R10/clocks",
            "derive local memory silence/screening",
            "core_MTS_risk",
        ),
        (
            "SC4185_3",
            "c_T",
            "medium",
            "torsion residual is dangerous but standard EC algebraic silence may close it if parent-signed",
            "derive torsion zero/heavy law or PPN/R10/spin bound",
            "geometry_extra_mode",
        ),
        (
            "SC4185_4",
            "c_R2/M_R",
            "medium",
            "finite-range corrections are scoreable with R10/orbital once projection exists",
            "use R10/orbital fallback after source/metric/memory root clauses",
            "EFT_tail",
        ),
        (
            "SC4185_5",
            "c_bdy",
            "medium",
            "private boundary routing exists but global adoption remains open",
            "keep boundary coefficient ledger and orbital/radiative flux fallback",
            "boundary_guard",
        ),
    ]
    return [
        {
            **common(),
            "scorecard_id": scorecard_id,
            "coefficient": coefficient,
            "priority_level": priority,
            "why_it_matters": why,
            "recommended_next_action": action,
            "route_label": route,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for scorecard_id, coefficient, priority, why, action, route in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "residual_coefficients_mapped": "True",
            "parent_zero_or_scale_laws_written": "True",
            "source_bound_interfaces_written": "True",
            "all_coefficients_numeric_or_parent_zero": "False",
            "source_backed_bound_pass_claim_allowed": "False",
            "recommended_first_route": "same_coframe_source_memory_zero_law_for_cD_deltaKappa_cGamma",
            "R10_status": "deferred_nonclaim_until_projection_and_curve_promotion",
            "orbital_status": "clean_bound_route_after_source_coupling_projection",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "meaning": (
                "4185 converts the Palatini residual leftovers into a coefficient-to-arena map. "
                "No coefficient is promoted; the next derivation should attack c_D, delta_kappa, and c_Gamma first."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FW4185_0_coefficients",
            "The residual coefficients are bounded or zero.",
            "They are mapped; each still needs a parent-zero/scale law or source-backed numeric bound.",
        ),
        (
            "FW4185_1_R10",
            "R10 proves the residual branch passes.",
            "R10 rows are nonclaim until projection coefficients and reviewed bound curve are promoted.",
        ),
        (
            "FW4185_2_orbital",
            "Orbital readiness is an empirical pass.",
            "Orbital is selected as a cleaner route, but source/ephemeris rows or analytic envelopes are still required.",
        ),
        (
            "FW4185_3_public_GR",
            "MTS now has public local GR.",
            "This is still a private conditional branch; public local-GR claim stays false.",
        ),
        (
            "FW4185_4_numeric_G",
            "MTS predicts numeric G.",
            "delta_kappa/source coupling map preserves the numeric-G firewall.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_language": forbidden,
            "safe_language": safe,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, safe in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "source_sweep_complete": "True",
            "residual_coefficients_mapped": "True",
            "parent_zero_or_scale_laws_written": "True",
            "source_bound_interfaces_written": "True",
            "all_coefficients_numeric_or_parent_zero": "False",
            "recommended_first_route": "cD_deltaKappa_cGamma",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_201_written": "True",
            "claim_register_action": claim_action,
            "packet_180_action": packet_action,
            "spine_action": spine_action,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": (
                "4185 shows the first root risks are same-coframe/source-memory ownership, not detached R10 scoring. "
                "A zero law for c_D, delta_kappa, and c_Gamma would protect WEP, clocks, EM/Poynting, Newton coupling, and local memory leakage at once."
            ),
            "route_A": "derive parent functor/source-memory zero law: c_D=0, delta_kappa=0, and c_Gamma locally screened or zero",
            "route_B": "if any of c_D, delta_kappa, or c_Gamma remains finite, build WEP/clock/orbital/PPN bound runner rows before R10",
            "defer_R10_until": "finite-range coefficients c_R2/c_T/c_Gamma have projection numerators and reviewed alpha(lambda) curve",
            "public_claim_policy": "no public local-GR claim until all coefficient rows are parent-zero, heavy/screened, or source-backed bounded",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    names = [
        "P8_Y5_R2FR_4185_SOURCE_REGISTER",
        "P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP",
        "P8_Y5_R2FR_4185_BOUND_INTERFACE_MATRIX",
        "P8_Y5_R2FR_4185_PARENT_ZERO_SCALE_LAW_CANDIDATES",
        "P8_Y5_R2FR_4185_PRIORITY_SCORECARD",
        "P8_Y5_R2FR_4185_BRANCH_DECISION",
        "P8_Y5_R2FR_4185_CLAIM_FIREWALL",
        "P8_Y5_R2FR_4185_STATUS",
        "P8_Y5_R2FR_4185_NEXT_TARGET",
    ]
    return {name: SOURCE_DIR / f"{name}.csv" for name in names}


def write_formal_201() -> None:
    text = f"""# 201 - PPC4161 Extra-Invariant Residual Coefficient Map

Marker: `{SPINE_MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This file maps the residual coefficients left by the conditional Palatini selector. It does not claim that any coefficient is zero, bounded, or empirically passed.

## Coefficient Map

The residuals are now explicit:

```text
c_D         second metric / disformal same-coframe leak
delta_kappa source-coupling drift
c_Gamma    local memory hair
c_T         torsion-square residual
c_R2 or M_R curvature-square finite-range tail
c_bdy       unrouted boundary/edge charge
```

Each coefficient has two possible exits:

```text
parent route: coefficient = 0, symmetry-forbidden, heavy, screened, or boundary-routed;
bound route: coefficient finite but projected into PPN, WEP, clocks, orbital, R10, or EM arenas.
```

## Priority

The first route should not be a detached R10 fit. The root-risk order is:

1. `c_D` because same-coframe failure breaks WEP, clocks, EM propagation, and Poynting/Hilbert stress ownership.
2. `delta_kappa` because source-coupling drift breaks the Newton coupling and orbital/clock local-G consistency.
3. `c_Gamma` because MTS-specific local memory hair can reopen PPN/R10/clocks.
4. `c_T`, `c_R2/M_R`, and `c_bdy` as geometry/EFT/boundary residuals.

## Existing Bound Scaffolds

The project already has a private local comparator scaffold for:

- PPN vector;
- R10 Yukawa anchor/curve candidates;
- WEP eta;
- clock redshift;
- local `Gdot/G`;
- orbital/inverse-square consistency.

But these are scaffolds, not a pass for the new residual coefficients. A finite coefficient still needs a projection Jacobian/numerator and a source-backed bound row.

## Verdict

```text
residual_coefficients_mapped = true
parent_zero_or_scale_laws_written = true
source_bound_interfaces_written = true
all_coefficients_numeric_or_parent_zero = false
public_local_GR_claim_allowed = false
```

## Next Target

`{NEXT_TARGET}`
"""
    FORMAL_201_PATH.write_text(text, encoding="utf-8")


def write_doc() -> None:
    text = f"""# 4185 - Y5 R2FR Extra-Invariant Residual Coefficient Map To PPN/R10/Clocks Or Parent Scale Law

Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Result

4185 converts the leftover Palatini-selector debts into a coefficient map:

```text
c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, c_bdy.
```

Each now has:

- a physical failure mode;
- a parent-zero or parent-scale route;
- a fallback empirical arena;
- a nonclaim status.

## Tactical Read

The best next attack is not R10 first. It is the root ownership triple:

```text
c_D -> same coframe,
delta_kappa -> source coupling,
c_Gamma -> local memory silence/screening.
```

If those close, the remaining torsion/curvature/boundary coefficients become much easier EFT leftovers. If they do not close, WEP/clocks/orbital/PPN should be used before R10.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gravity",
            "claim": (
                "The extra A_MF-invariant local residuals are now mapped to explicit coefficients and test arenas, "
                "but none is promoted as zero or bounded without parent-zero/scale-law or source-backed projection evidence"
            ),
            "current_evidence": (
                "formalization-workbench/201-PPC4161-extra-invariant-residual-coefficient-map.md records c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, "
                "and c_bdy; maps each to PPN/R10/WEP/clock/orbital/EM arenas; prioritizes c_D, delta_kappa and c_Gamma; and keeps public_claim=false"
            ),
            "status": "residual_coefficient_map_nonclaim_parent_zero_or_numeric_bounds_missing_public_claim_false",
            "next_test": "Derive same-coframe/source-memory zero law for c_D, delta_kappa and c_Gamma, or build WEP/clock/orbital/PPN bound rows",
            "key_risk": (
                "The map is not a pass: finite coefficients still need projection numerators/Jacobians and source-backed bounds; "
                "R10 remains deferred until finite-range projection inputs and curve review close"
            ),
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "added"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4185 Residual Coefficient Arena Map

Marker: `{PACKET_MARKER}`

`post-checkpoint-work/4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md` maps every extra-invariant coefficient left by 4184:

```text
c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, c_bdy.
```

The selected next route is the root ownership triple:

```text
c_D -> same-coframe parent functor
delta_kappa -> source-coupling/kappa lock
c_Gamma -> local memory silence or screening
```

No coefficient is claimed zero or bounded yet.
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "added"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Extra-Invariant Residual Coefficient Map

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4185 maps the Palatini-selector residual coefficients to parent-zero/scale-law routes and fallback empirical arenas. The first priority is the root ownership triple `c_D`, `delta_kappa`, and `c_Gamma`; R10 is deferred until finite-range projection coefficients and reviewed curve rows are claim-ready.

Next target:

`{NEXT_TARGET}`
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "added"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    paths = output_paths()
    source_ok = all(
        row["exists"] == "True" and row["required_text_found"] == "True"
        for row in rows_by_name["P8_Y5_R2FR_4185_SOURCE_REGISTER"]
    )
    decision = rows_by_name["P8_Y5_R2FR_4185_BRANCH_DECISION"][0]
    status = rows_by_name["P8_Y5_R2FR_4185_STATUS"][0]
    all_generated_rows = [
        row
        for rows in rows_by_name.values()
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4185_0_sources", "all cited sources exist and contain required text", source_ok, ""),
        ("VAL4185_1_coefficients", "all six residual coefficients are mapped", len(rows_by_name["P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP"]) == 6, ""),
        ("VAL4185_2_cD_priority", "c_D is highest priority", any(row["coefficient"] == "c_D" and row["priority_level"] == "highest" for row in rows_by_name["P8_Y5_R2FR_4185_PRIORITY_SCORECARD"]), ""),
        ("VAL4185_3_cGamma", "c_Gamma has memory parent law candidate", any(row["coefficient"] == "c_Gamma" for row in rows_by_name["P8_Y5_R2FR_4185_PARENT_ZERO_SCALE_LAW_CANDIDATES"]), ""),
        ("VAL4185_4_R10_nonclaim", "R10 is deferred nonclaim", decision["R10_status"] == "deferred_nonclaim_until_projection_and_curve_promotion", str(decision)),
        ("VAL4185_5_not_all_bounded", "coefficients are not all zero/bounded", decision["all_coefficients_numeric_or_parent_zero"] == "False", str(decision)),
        ("VAL4185_6_public_claim", "public local-GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4185_7_numeric_G", "numeric G remains unpredicted", status["numeric_G_predicted"] == "False", str(status)),
        ("VAL4185_8_formal_201", "formal 201 exists and has marker", FORMAL_201_PATH.exists() and SPINE_MARKER in read_text(FORMAL_201_PATH), str(FORMAL_201_PATH)),
        ("VAL4185_9_doc", "4185 doc exists and has decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4185_10_claim_row", "claim register contains L-026", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4185_11_packet_180", "packet 180 addendum marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4185_12_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4185_13_next", "next target recorded", rows_by_name["P8_Y5_R2FR_4185_NEXT_TARGET"][0]["next_target"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4185_14_output_paths", "all declared output CSVs exist", all(path.exists() for path in paths.values()), str(paths)),
        ("VAL4185_15_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
    ]
    validation = [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "details": details,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, description, passed, details in checks
    ]
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4185_16_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_201()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4185_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP": coefficient_map_rows(),
        "P8_Y5_R2FR_4185_BOUND_INTERFACE_MATRIX": bound_interface_rows(),
        "P8_Y5_R2FR_4185_PARENT_ZERO_SCALE_LAW_CANDIDATES": parent_scale_law_rows(),
        "P8_Y5_R2FR_4185_PRIORITY_SCORECARD": scorecard_rows(),
        "P8_Y5_R2FR_4185_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4185_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4185_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4185_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4185_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4185 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_201_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
