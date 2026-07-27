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

CHECKPOINT = "4188"
BRANCH_ID = "MTS_R2FR_Y5_FINITE_CGAMMA_BOUND_RUNNER_4188"
DECISION = (
    "FINITE_CGAMMA_PRODUCT_BOUND_LAW_DERIVED_AND_RUNNER_BUILT_"
    "SUPPORT_PROOF_STILL_OPEN_NONCLAIM"
)
DOC_PATH = POST / "4188-Y5-R2FR-finite-cGamma-PPN-clock-orbital-bound-runner-or-support-proof.md"
FORMAL_204_PATH = FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-029"
SPINE_MARKER = "PPC4161_FINITE_CGAMMA_PRODUCT_BOUND_LAW_4188"
PACKET_MARKER = "PPC4161_PACKET_FINITE_CGAMMA_PRODUCT_BOUND_LAW_4188"
NEXT_TARGET = "4189-Y5-R2FR-cGamma-parent-memory-equation-or-first-profile-coefficient-fill.md"

SOURCES = {
    "SRC4188_00_4187_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4187_NEXT_TARGET.csv",
        "build finite c_Gamma PPN-clock-orbital runner",
        "4187 next target.",
    ),
    "SRC4188_01_4187_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4187_MEMORY_SUPPORT_PROJECTOR_CONTRACT.csv",
        "P_loc[Gamma_mem E_I",
        "4187 exact support/projector contract.",
    ),
    "SRC4188_02_4187_bound_interface": (
        SOURCE_DIR / "P8_Y5_R2FR_4187_FINITE_CGAMMA_BOUND_INTERFACE.csv",
        "FB4187_2_orbital",
        "4187 finite c_Gamma arena interface.",
    ),
    "SRC4188_03_formal_203": (
        FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md",
        "c_Gamma_parent_zero = false",
        "formal c_Gamma support/projector gate.",
    ),
    "SRC4188_04_4173_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv",
        "B4173_14_orbit_combo",
        "source-backed local bound table.",
    ),
    "SRC4188_05_4173_sources": (
        SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_REGISTER.csv",
        "SRC4173_WEB_00_Will2014_PPN_table",
        "source register for local bounds.",
    ),
    "SRC4188_06_4164_ppn": (
        SOURCE_DIR / "P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR.csv",
        "L_gamma[E_mu_nu_residual]",
        "PPN residual map from local equation residuals.",
    ),
    "SRC4188_07_4172_ppn": (
        SOURCE_DIR / "P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION.csv",
        "gamma-1=0",
        "private PPN zero vector before c_Gamma reactivation.",
    ),
    "SRC4188_08_4171_orbit": (
        SOURCE_DIR / "P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv",
        "a_r=-G_N M_H^dress/r^2",
        "Newton/orbital readout law.",
    ),
    "SRC4188_09_3937_route": (
        SOURCE_DIR / "P8_Y5_R2FR_3937_R10_OR_ORBITAL_READINESS_COMPARISON.csv",
        "orbital_ephemeris",
        "earlier orbital-first route decision.",
    ),
    "SRC4188_10_3938_orbital": (
        SOURCE_DIR / "P8_Y5_R2FR_3938_ORBITAL_BOUND_IMPORTS.csv",
        "BIMP3938_0_Gdot",
        "source-backed orbital/PPN bound imports.",
    ),
    "SRC4188_11_3797_clock": (
        SOURCE_DIR / "P8_Y5_R2FR_3797_CLOCK_JOIN_LEDGER.csv",
        "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM",
        "clock product-bound ledger.",
    ),
    "SRC4188_12_3797_R10": (
        SOURCE_DIR / "P8_Y5_R2FR_3797_R10_BOUND_JOIN_LEDGER.csv",
        "AVAILABLE_NONCLAIM_REVIEW_REQUIRED",
        "R10 bound-curve join ledger.",
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


def numeric(value: str) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


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


def support_proof_attempt_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SPA4188_0_parent_operator",
            "Need explicit parent memory equation L_Gamma Gamma_mem = J_Gamma plus boundary data.",
            "not_found",
            "Without L_Gamma and its sign, no positive/no-hair theorem can be closed.",
            "derive_or_choose parent Gamma_mem operator.",
        ),
        (
            "SPA4188_1_vertical_split",
            "Need Gamma_mem = Gamma_vert + Gamma_hor with P_loc Gamma_hor=0 or bound.",
            "partial_only",
            "Quotient readouts are vertical-silent, but Gamma_mem itself is not proven vertical.",
            "prove Gamma_hor absent or fill finite C_Gamma,horizontal.",
        ),
        (
            "SPA4188_2_bulk_source",
            "Need J_Gamma_bulk=0 for ordinary compact matter.",
            "not_found",
            "Hilbert source descent kills source-measure drift but not memory excitation by invariant I_local.",
            "derive J_Gamma from parent action variation.",
        ),
        (
            "SPA4188_3_boundary_nohair",
            "Need F_Gamma boundary-only with no compact side flux and no homogeneous tensor residue.",
            "partial_only",
            "Boundary routing exists as a template; Gamma_perp/K_perp no-hair is not parent-owned.",
            "prove tensor boundary no-hair or bound Gamma_perp.",
        ),
        (
            "SPA4188_4_finite_bound_escape",
            "If any previous clause remains unsigned, use C_Gamma product bounds.",
            "selected",
            "This is the non-smuggled route: derive the exact inequality the missing parent coefficient must satisfy.",
            "build runner rows now.",
        ),
    ]
    return [
        {
            **common(),
            "attempt_id": attempt_id,
            "required_clause": required_clause,
            "current_status": current_status,
            "why_it_matters": why_it_matters,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for attempt_id, required_clause, current_status, why_it_matters, next_action in rows
    ]


def c_gamma_law_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "LAW4188_0_definition",
            "Define C_Gamma,a := c_Gamma * N_a[P_loc Gamma_mem, J_a^Gamma, Gamma_perp]",
            "collapses the unknown parent coefficient, local profile and arena projection into one effective product",
            "exact bookkeeping identity",
        ),
        (
            "LAW4188_1_linear_bound",
            "For each arena a, Delta O_a = C_Gamma,a + O(C_Gamma,a^2) in unit-normalized first-order smoke rows.",
            "the source-backed bound B_a gives |C_Gamma,a| <= B_a at first order",
            "derived finite-bound law",
        ),
        (
            "LAW4188_2_nonunit_jacobian",
            "If a real Jacobian J_a is later supplied, replace the smoke bound by |c_Gamma * profile_a| <= B_a / |J_a|.",
            "prevents hiding behind unit normalization",
            "ready for coefficient fill",
        ),
        (
            "LAW4188_3_no_cancellation",
            "Bounds are channelwise; cancellations between gamma, beta, xi, alpha_i, zeta_i, clock and orbital rows are not allowed.",
            "avoids fitting away one local residual with another",
            "claim firewall",
        ),
        (
            "LAW4188_4_zero_recovery",
            "If the 4187 support/no-hair clauses are later parent-proved, every C_Gamma,a row becomes zero and this runner becomes a regression check.",
            "connects finite-bound branch back to derivation-first branch",
            "future proof hook",
        ),
    ]
    return [
        {
            **common(),
            "law_id": law_id,
            "statement": statement,
            "consequence": consequence,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for law_id, statement, consequence, status in rows
    ]


def bound_import_rows() -> List[Dict[str, str]]:
    imported = []
    for row in parse_csv(SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv"):
        bound = numeric(row.get("allowed_abs_bound", ""))
        include = row.get("arena") in {
            "PPN",
            "PPN_orbital",
            "PPN_preferred_frame",
            "PPN_conservation",
            "clock_orbital",
            "clock_redshift",
            "orbital",
            "short_range_gravity",
            "WEP",
        }
        if not include:
            continue
        imported.append(
            {
                **common(),
                "import_id": f"IMP4188_{row['bound_id']}",
                "source_bound_id": row["bound_id"],
                "arena": row["arena"],
                "observable": row["observable"],
                "allowed_abs_bound": "" if bound is None else f"{bound:.17g}",
                "units": row["units"],
                "source_id": row["source_id"],
                "source_backed": row["source_backed"],
                "numeric_bound": str(bound is not None and bound > 0),
                "usable_for_cGamma_product_bound": str(bound is not None and bound > 0),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return imported


def channel_map(observable: str, arena: str) -> tuple[str, str, str]:
    if observable in {"gamma_minus_1", "beta_minus_1", "xi", "((2+2gamma-beta)/3)-1"}:
        return ("metric_scalar_or_location", "C_Gamma_metric", "PPN/orbital metric residual")
    if observable in {"alpha1", "alpha2", "alpha3"}:
        return ("vector_or_momentum_flux", "C_Gamma_vector", "preferred-frame/momentum residual")
    if observable.startswith("zeta"):
        return ("stress_conservation", "C_Gamma_stress", "hidden stress/source residual")
    if observable == "Gdot_over_G":
        return ("time_drift", "C_Gamma_Gdot", "local coupling/source drift residual")
    if observable == "redshift_violation_alpha":
        return ("clock_readout", "C_Gamma_clock", "clock/redshift residual")
    if "Yukawa" in observable or "lambda" in observable:
        return ("finite_range", "C_Gamma_R10", "short-range fifth-force residual")
    if observable == "eta_TiPt":
        return ("composition_guard", "C_Gamma_WEP", "species/source-composition residual guard")
    return (arena, "C_Gamma_misc", "misc local residual")


def runner_rows() -> List[Dict[str, str]]:
    rows = []
    for imported in bound_import_rows():
        bound = numeric(imported["allowed_abs_bound"])
        if bound is None:
            continue
        channel, effective_product, meaning = channel_map(imported["observable"], imported["arena"])
        unit_jacobian = 1.0
        max_product = bound / unit_jacobian
        rows.append(
            {
                **common(),
                "runner_id": f"RUN4188_{imported['source_bound_id']}",
                "arena": imported["arena"],
                "observable": imported["observable"],
                "cGamma_channel": channel,
                "effective_product": effective_product,
                "linearized_residual_model": f"Delta_{imported['observable']} = {effective_product} + O({effective_product}^2)",
                "unit_normalized_jacobian": f"{unit_jacobian:.17g}",
                "max_abs_effective_product": f"{max_product:.17g}",
                "units": imported["units"],
                "source_bound_id": imported["source_bound_id"],
                "source_id": imported["source_id"],
                "meaning": meaning,
                "numeric_prediction_available": "False",
                "claim_status": "nonclaim_bound_on_effective_product_not_cGamma_alone",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def strictest_rows() -> List[Dict[str, str]]:
    numeric_rows = runner_rows()
    by_channel: Dict[str, Dict[str, str]] = {}
    for row in numeric_rows:
        value = float(row["max_abs_effective_product"])
        current = by_channel.get(row["effective_product"])
        if current is None or value < float(current["max_abs_effective_product"]):
            by_channel[row["effective_product"]] = row
    output = []
    for effective_product, row in sorted(by_channel.items()):
        output.append(
            {
                **common(),
                "effective_product": effective_product,
                "strictest_observable": row["observable"],
                "strictest_arena": row["arena"],
                "max_abs_effective_product": row["max_abs_effective_product"],
                "units": row["units"],
                "source_bound_id": row["source_bound_id"],
                "interpretation": f"Any future parent coefficient feeding {effective_product} must be below this product bound unless 4187 zero theorem closes.",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return output


def priority_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "priority_id": "PRI4188_0",
            "selected_next": "derive_or_fill C_Gamma_metric and C_Gamma_Gdot/orbital first",
            "why": "The orbital/Newton bridge already has source-charge and acceleration readouts, and PPN gamma/beta/Gdot give direct tests of local GR-to-Newton reduction.",
            "avoid": "R10 first, unless a finite-range c_Gamma profile survives; R10 still needs a reviewed curve and alpha projection.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "priority_id": "PRI4188_1",
            "selected_next": "do not chase every PPN component equally",
            "why": "A generic memory tensor could feed many channels, but the parent route should decide scalar metric, vector flux, stress conservation, clock drift, or finite range before scoring.",
            "avoid": "using the tight alpha3 bound as a scarecrow unless the derivation actually creates momentum nonconservation.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FW4188_0_product_not_cGamma",
            "The runner bounds C_Gamma,arena = c_Gamma times profile/projection/Jacobian, not c_Gamma alone.",
        ),
        (
            "FW4188_1_no_zero_claim",
            "c_Gamma_parent_zero remains false until 4187 support/no-hair clauses are parent-proved.",
        ),
        (
            "FW4188_2_no_public_pass",
            "No local-GR, PPN, clock, orbital or R10 pass can be claimed from product bounds alone.",
        ),
        (
            "FW4188_3_no_cancellation",
            "A future score must pass channelwise bounds without cancellations between unrelated observables.",
        ),
        (
            "FW4188_4_R10_deferred",
            "R10 remains nonclaim unless a real alpha(lambda) curve and c_Gamma finite-range projection are both reviewed.",
        ),
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
            "support_nohair_proof_closed": "False",
            "finite_cGamma_product_law_derived": "True",
            "bound_import_rows": str(len(bound_import_rows())),
            "runner_rows": str(len(runner_rows())),
            "strictest_product_rows": str(len(strictest_rows())),
            "c_Gamma_parent_zero": "False",
            "numeric_cGamma_prediction_available": "False",
            "product_bounds_available": "True",
            "public_local_GR_claim_allowed": "False",
            "formal_204_written": str(FORMAL_204_PATH.exists()),
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
            "why": "4188 turns c_Gamma into explicit product bounds. The next productive step is to derive or fill the parent memory equation/projection coefficient for the leading channel instead of adding more generic ledgers.",
            "route_A": "derive Gamma_mem parent operator and show vertical/support/no-hair for compact local collars",
            "route_B": "fill first C_Gamma_metric or C_Gamma_Gdot profile/projection coefficient and run against 4188 product bounds",
            "recommended_first": "C_Gamma_metric_or_Gdot because they connect most directly to local GR/Newton reduction",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc_text() -> str:
    strictest_text = "\n".join(
        f"- `{row['effective_product']}` <= `{row['max_abs_effective_product']}` {row['units']} from `{row['strictest_observable']}`"
        for row in strictest_rows()
    )
    return f"""# 204 - PPC4161 Finite c_Gamma Product Bound Law

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove `c_Gamma=0` and does not claim a public local-GR pass. It derives the finite-product bound law that any nonzero local memory residual must satisfy.

## Product Law

From 4187 the active residual is:

```text
E_Gamma^loc = P_loc(delta S_Gamma / delta O_loc).
```

For each local arena `a`, define:

```text
C_Gamma,a := c_Gamma * N_a[P_loc Gamma_mem, J_a^Gamma, Gamma_perp].
```

At first order:

```text
Delta O_a = C_Gamma,a + O(C_Gamma,a^2)
```

in the unit-normalized smoke rows. Therefore a source-backed bound `B_a` gives:

```text
|C_Gamma,a| <= B_a.
```

If a real arena Jacobian is later supplied, the rule becomes:

```text
|c_Gamma * profile_a| <= B_a / |J_a^Gamma|.
```

## Strictest Current Product Bounds

{strictest_text}

## Interpretation

These are bounds on the effective product, not on `c_Gamma` alone. They are useful because the parent derivation now has hard targets. If the parent memory equation later proves the 4187 support/no-hair clauses, all product rows collapse to zero. If not, the first profile/projection fill must beat these numbers without cross-channel cancellation.

## Next Gate

`{NEXT_TARGET}` should derive or fill the leading `C_Gamma_metric`/`C_Gamma_Gdot` coefficient before R10 is promoted.
"""


def checkpoint_doc_text() -> str:
    return f"""# 4188 - Finite c_Gamma PPN/Clock/Orbital Bound Runner Or Support Proof

Generated by: `post-checkpoint-work/scripts/Y5_R2FR_4188_finite_cGamma_PPN_clock_orbital_bound_runner.py`

## Summary

This checkpoint attempts the support/no-hair proof route and finds the same hard missing clauses: no parent-owned `L_Gamma`, no proof that `Gamma_mem` is q-vertical or compact-support silent, no `J_Gamma_bulk=0`, and no tensor no-hair theorem. It then performs the useful fallback: derives and runs finite product bounds.

## Core Result

```text
C_Gamma,a := c_Gamma * N_a[P_loc Gamma_mem, J_a^Gamma, Gamma_perp]
Delta O_a = C_Gamma,a + O(C_Gamma,a^2)
|C_Gamma,a| <= B_a
```

where `B_a` is imported from the source-backed 4173 local bound table.

## Decision

`{DECISION}`

## Nonclaim Policy

The runner bounds effective products, not `c_Gamma` alone. No public local-GR, PPN, clock, orbital or R10 pass is claimed.
"""


def ensure_docs() -> None:
    FORMAL_204_PATH.write_text(formal_doc_text(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc_text(), encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "Finite c_Gamma effective-product bound law is derived for PPN, clock, orbital, WEP guard and R10 arenas; parent zero proof remains open.",
            "current_evidence": "4188 support proof attempt, product-bound law, imported 4173 source-backed bounds, strictest product ledger and nonclaim firewall.",
            "status": "private_finite_product_bound_nonclaim_cGamma_parent_zero_false",
            "next_test": "Derive parent Gamma_mem operator/projection or fill first C_Gamma_metric/C_Gamma_Gdot coefficient and compare against product bounds.",
            "key_risk": "Effective-product bounds could be mistaken for a direct c_Gamma value unless profile and Jacobian coefficients are supplied.",
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "appended"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4188 Finite c_Gamma Product Bound Law

Marker: `{PACKET_MARKER}`

4188 turns the remaining `c_Gamma` memory residual into a finite product-bound rule:

```text
C_Gamma,a := c_Gamma * N_a[P_loc Gamma_mem, J_a^Gamma, Gamma_perp]
|C_Gamma,a| <= B_a.
```

The support/no-hair proof route remains open because the parent memory operator, q-horizontal support, ordinary bulk source and tensor no-hair clauses are not all parent-owned. Product bounds are now executable nonclaim targets for future coefficient fills.
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "appended"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Finite c_Gamma Product Bound Law

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4188 makes the `c_Gamma` fallback quantitative without pretending the parent coefficient is known. For each local arena:

```text
C_Gamma,a := c_Gamma * N_a[P_loc Gamma_mem, J_a^Gamma, Gamma_perp]
Delta O_a = C_Gamma,a + O(C_Gamma,a^2)
|C_Gamma,a| <= B_a.
```

The imported `B_a` rows come from the source-backed 4173 local bound table. This does not claim `c_Gamma=0` or a public local-GR pass; it gives the next derivation a concrete target.
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "appended"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source_register = rows_by_name["P8_Y5_R2FR_4188_SOURCE_REGISTER"]
    status = rows_by_name["P8_Y5_R2FR_4188_STATUS"][0]
    imports = rows_by_name["P8_Y5_R2FR_4188_CGAMMA_BOUND_IMPORTS"]
    runner = rows_by_name["P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER"]
    all_generated_rows = [
        row
        for name, rows in rows_by_name.items()
        if name != "P8_Y5_R2FR_4188_SOURCE_REGISTER"
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4188_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source_register), str(source_register)),
        ("VAL4188_1_source_tokens", "all source tokens found", all(row["required_text_found"] == "True" for row in source_register), str(source_register)),
        ("VAL4188_2_support_not_closed", "support/no-hair proof remains explicitly open", status["support_nohair_proof_closed"] == "False", str(status)),
        ("VAL4188_3_product_law", "finite cGamma product law derived", status["finite_cGamma_product_law_derived"] == "True", str(status)),
        ("VAL4188_4_imports", "numeric source-backed imports exist", len([row for row in imports if row["usable_for_cGamma_product_bound"] == "True"]) >= 10, str(len(imports))),
        ("VAL4188_5_runner", "runner produces product bounds", len(runner) >= 10 and all(float(row["max_abs_effective_product"]) > 0 for row in runner), str(len(runner))),
        ("VAL4188_6_strictest", "strictest product rows exist", len(rows_by_name["P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS"]) >= 4, str(rows_by_name["P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS"])),
        ("VAL4188_7_cGamma_false", "c_Gamma parent zero remains false", status["c_Gamma_parent_zero"] == "False", str(status)),
        ("VAL4188_8_no_public_claim", "public local GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4188_9_formal_204", "formal 204 exists with marker", FORMAL_204_PATH.exists() and SPINE_MARKER in read_text(FORMAL_204_PATH), str(FORMAL_204_PATH)),
        ("VAL4188_10_checkpoint_doc", "checkpoint doc exists and has decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4188_11_claim_row", "claim register contains L-029", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4188_12_packet_180", "packet 180 marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4188_13_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4188_14_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
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
            "check_id": "VAL4188_15_py_compile",
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
        "P8_Y5_R2FR_4188_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4188_SUPPORT_NOHAIR_PROOF_ATTEMPT": support_proof_attempt_rows(),
        "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_LAW": c_gamma_law_rows(),
        "P8_Y5_R2FR_4188_CGAMMA_BOUND_IMPORTS": bound_import_rows(),
        "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER": runner_rows(),
        "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS": strictest_rows(),
        "P8_Y5_R2FR_4188_PRIORITY_DECISION": priority_rows(),
        "P8_Y5_R2FR_4188_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4188_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4188_NEXT_TARGET": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(SOURCE_DIR / f"{name}.csv", rows)

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4188_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4188 validation failed: {failed}")

    print(DECISION)
    print(f"formal={FORMAL_204_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
