from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
CORE = ROOT / "core-mts-framework"

CHECKPOINT = "4223"
CLAIM_ID = "L-064"
BRANCH = "MTS_R2FR_Y5_BINDING_CORE_NEGATIVE_ENERGY_GATE_4223"
DECISION = "BINDING_AND_MTS_CORE_SIGN_REDUCED_TO_CANONICAL_ACTION_BOUND_GAMMA_BOUNDARY_OR_BATH_AND_BINDING_FRACTION_ROWS_NONCLAIM"
MARKER = "PPC4161_BINDING_CORE_NEGATIVE_ENERGY_GATE_4223"
PACKET_MARKER = "PPC4161_PACKET_BINDING_CORE_NEGATIVE_ENERGY_GATE_4223"
NEXT_TARGET = "4224-Y5-R2FR-lambda-gamma-core-action-sign-and-binding-bound-source-row.md"

FORMAL_PATH = FORMAL / "239-PPC4161-binding-stabilizer-and-MTS-core-negative-energy-bound-or-parent-signature.md"
DOC_PATH = POST / "4223-Y5-R2FR-binding-stabilizer-and-MTS-core-negative-energy-bound-or-parent-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4223_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4223_00_4222_next": SourceSpec(
        "SRC4223_00_4222_next",
        SOURCE_DIR / "P8_Y5_R2FR_4222_NEXT_TARGET.csv",
        "4223-Y5-R2FR-binding-stabilizer-and-MTS-core-negative-energy-bound-or-parent-signature.md",
        "4222 selected binding/stabilizer and MTS-core signs as the next obstruction.",
    ),
    "SRC4223_01_4222_bounds": SourceSpec(
        "SRC4223_01_4222_bounds",
        SOURCE_DIR / "P8_Y5_R2FR_4222_NEGATIVE_BOUND_ROWS.csv",
        "NEB4222_0_binding_stabilizer",
        "4222 negative-energy rows staged for this fill.",
    ),
    "SRC4223_02_fundamental_action": SourceSpec(
        "SRC4223_02_fundamental_action",
        CORE / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "A_MTS[ψ]",
        "Microscopic psi action with kinetic, gradient, gamma and lambda terms.",
    ),
    "SRC4223_03_effective_field": SourceSpec(
        "SRC4223_03_effective_field",
        CORE / "field-theory" / "the-effective-field-theory-of-motion-timespace.md",
        "A_MTS[ψ]",
        "Effective field theory restatement of the microscopic psi action and energy functional.",
    ),
    "SRC4223_04_gravity_bounded": SourceSpec(
        "SRC4223_04_gravity_bounded",
        CORE / "gravity" / "motion-timespace-mts-gravity.md",
        "Hamiltonian remains bounded from below",
        "Gravity note claiming bounded Hamiltonian/no Ostrogradsky route.",
    ),
    "SRC4223_05_parent_signature": SourceSpec(
        "SRC4223_05_parent_signature",
        SOURCE_DIR / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv",
        "S_Y is quadratic/coercive",
        "Minimal parent signature clause for coercive hidden/residual fibres.",
    ),
    "SRC4223_06_hamiltonian_matrix": SourceSpec(
        "SRC4223_06_hamiltonian_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_3949_MTS_HAMILTONIAN_SIGNATURE_MATRIX.csv",
        "SIG3949_7_matter_binding",
        "Older MTS Hamiltonian signature matrix naming matter/binding and MTS-core gaps.",
    ),
    "SRC4223_07_GK_auxiliary": SourceSpec(
        "SRC4223_07_GK_auxiliary",
        SOURCE_DIR / "P8_Y5_R2FR_3950_GK_POSITIVE_AUXILIARY_SIGNATURE.csv",
        "positive auxiliary parent density",
        "Positive auxiliary density route for residual core sectors.",
    ),
    "SRC4223_08_source_decomposition": SourceSpec(
        "SRC4223_08_source_decomposition",
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H = T_matter + T_EM + T_binding",
        "Hilbert source decomposition including binding.",
    ),
    "SRC4223_09_4222_formal": SourceSpec(
        "SRC4223_09_4222_formal",
        FORMAL / "238-PPC4161-positive-energy-sector-signature-matrix-or-negative-energy-bound-fill.md",
        "binding/stabilizer and MTS core",
        "Current partial positive-energy signature matrix.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in SOURCE_SPECS.values():
        text = read_text(source.path)
        rows.append(
            {
                **common(),
                "source_id": source.source_id,
                "path": str(source.path),
                "exists": str(source.path.exists()),
                "required_text": source.required_text,
                "required_text_found": str(source.required_text in text),
                "role": source.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def core_action_rows() -> List[Dict[str, str]]:
    data = [
        (
            "CAS4223_0_source_lagrangian",
            "psi core Lagrangian",
            "L_psi = (1/2c^2) psi_dot^2 - (1/2)|grad psi|^2 - gamma psi psi_dot - (lambda/n)|psi|^n",
            "read from core action files",
            "SOURCE_BACKED_FORMULA_SHAPE",
        ),
        (
            "CAS4223_1_gamma_boundary",
            "gamma term as boundary",
            "-gamma psi psi_dot = -(gamma/2) d_t(psi^2) when gamma is fixed",
            "If gamma is a fixed coefficient in a conservative action, it is a time-boundary term and does not make the bulk Hamiltonian negative.",
            "DERIVED_CONDITIONAL_BOUNDARY_TERM",
        ),
        (
            "CAS4223_2_gamma_bath",
            "gamma term as physical damping",
            "if gamma represents irreversible damping, move it to E_gamma_bath_or_open_abs",
            "A real dissipative term is not a closed Hamiltonian bulk energy; it needs a bath/boundary balance row.",
            "OPEN_SYSTEM_BOUND_REQUIRED_IF_DAMPING",
        ),
        (
            "CAS4223_3_canonical_H",
            "canonical psi Hamiltonian density",
            "H_psi = (1/2c^2) psi_dot^2 + (1/2)|grad psi|^2 + (lambda/n)|psi|^n + H_gamma_boundary",
            "The gamma contribution cancels from the bulk Legendre transform when treated as a fixed boundary term.",
            "DERIVED_CONDITIONAL_HAMILTONIAN",
        ),
        (
            "CAS4223_4_lambda_sign",
            "lambda potential sign gate",
            "lambda>=0 and n>0 => H_psi_bulk>=0",
            "Core MTS energy is nonnegative only after the potential sign and units are parent-signed.",
            "MISSING_LAMBDA_SIGN_SOURCE",
        ),
        (
            "CAS4223_5_negative_bound",
            "fallback core negative-energy bound",
            "E_MTS_core_neg_abs <= (max(0,-lambda)/n) int |psi|^n + E_gamma_bath_or_open_abs + E_signature_mismatch_abs",
            "If lambda/gamma/signature cannot be signed, the core damage is a finite conservative bound row.",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
        ),
    ]
    return [
        {
            **common(),
            "core_id": core_id,
            "piece": piece,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for core_id, piece, formula, derivation, status in data
    ]


def binding_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "BBS4223_0_total_source_split",
            "binding/stabilizer split",
            "E_total_source = E_visible_rest + E_EM_closed + E_binding + E_stabilizer + ...",
            "Binding is part of the one Hilbert source; it is not separately weighted or dropped.",
            "SOURCE_DECOMPOSITION_LOCKED",
        ),
        (
            "BBS4223_1_negative_binding_fraction",
            "negative binding fraction",
            "E_binding_stabilizer_neg_abs <= beta_bind E_visible_rest + E_stab_neg_abs",
            "A stable bound source is acceptable if its negative binding/stabilizer contribution is bounded below by the positive rest/field pool.",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
        ),
        (
            "BBS4223_2_stability_shortcut",
            "bounded-below matter theorem",
            "S_matter+S_binding+S_stabilizer bounded below with nonzero support => E_visible_rest - E_binding_stabilizer_neg_abs > 0",
            "This would sign the sector if parent-owned for the local branch.",
            "MISSING_PARENT_STABILITY_THEOREM",
        ),
        (
            "BBS4223_3_no_component_cheat",
            "component accounting guard",
            "negative binding cannot be treated as WEP/source violation if it is already inside the same total Hilbert source",
            "The danger is sign size, not a second coupling, once source descent is signed.",
            "ACCOUNTING_GUARD_DERIVED",
        ),
    ]
    return [
        {
            **common(),
            "binding_id": binding_id,
            "piece": piece,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for binding_id, piece, formula, derivation, status in data
    ]


def residual_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "RBI4223_0_lambda_sign",
            "lambda_sign",
            "lambda>=0 with declared units and n>0",
            "core action source or parent potential signature",
            "MISSING_SOURCE_VALUE",
            "dimensionless_or_declared",
        ),
        (
            "RBI4223_1_gamma_mode",
            "gamma_mode",
            "fixed_boundary_term OR open-system damping with bath balance",
            "parent action/boundary condition or bath energy ledger",
            "MISSING_MODE_CERTIFICATE",
            "declared",
        ),
        (
            "RBI4223_2_core_negative",
            "E_MTS_core_neg_abs",
            "(max(0,-lambda)/n) int |psi|^n + E_gamma_bath_or_open_abs + E_signature_mismatch_abs",
            "lambda/gamma/core signature rows",
            "MISSING_COMPONENT_VALUES",
            "energy",
        ),
        (
            "RBI4223_3_beta_bind",
            "beta_bind",
            "E_binding_stabilizer_neg_abs/E_visible_rest upper bound",
            "stable matter/source model or conservative numeric bound",
            "MISSING_BOUND_VALUE",
            "dimensionless",
        ),
        (
            "RBI4223_4_binding_negative",
            "E_binding_stabilizer_neg_abs",
            "beta_bind E_visible_rest + E_stab_neg_abs",
            "binding/stabilizer stability row",
            "MISSING_COMPONENT_VALUES",
            "energy",
        ),
        (
            "RBI4223_5_epsilon_E_core_bind",
            "epsilon_E_core_bind",
            "(E_binding_stabilizer_neg_abs+E_MTS_core_neg_abs)/E_plus_min",
            "computed after E_plus_min and component bounds exist",
            "NOT_SCORE_READY",
            "dimensionless",
        ),
    ]
    return [
        {
            **common(),
            "input_id": input_id,
            "quantity": quantity,
            "formula_or_condition": formula,
            "required_evidence": evidence,
            "current_status": status,
            "units": units,
            "source_path": "MISSING_SOURCE_ROW",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, quantity, formula, evidence, status, units in data
    ]


def composed_gate_rows() -> List[Dict[str, str]]:
    rows = [
        {
            **common(),
            "gate_id": "BCG4223_0_core_zero_route",
            "quantity": "Z_MTS_core_nonnegative",
            "condition": "lambda>=0, n>0, gamma fixed-boundary or bath-balanced, positive kinetic metric, no hidden wrong-sign parent sector",
            "effect": "E_MTS_core_neg_abs=0",
            "status": "CONDITIONAL_ROUTE_BUILT_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "BCG4223_1_binding_small_route",
            "quantity": "Z_binding_small",
            "condition": "beta_bind + E_stab_neg_abs/E_visible_rest is source-backed and small enough",
            "effect": "binding/stabilizer cannot overturn E_plus_min",
            "status": "BOUND_ROUTE_BUILT_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "BCG4223_2_MEH_feed",
            "quantity": "epsilon_E_partial_update",
            "condition": "epsilon_E_partial includes core/binding bounds plus open/reference/virial/frame rows",
            "effect": "M_EH >= c^-2 E_plus_min(1-epsilon_E_partial)",
            "status": "COMPOSED_GATE_READY_NOT_SCORE_READY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "core_canonical_Hamiltonian_derived": "True",
            "gamma_boundary_or_bath_split_derived": "True",
            "lambda_sign_available": "False",
            "MTS_core_negative_bound_values_available": "False",
            "binding_fraction_bound_available": "False",
            "M_EH_positive_available": "False",
            "local_GR_claim": "False",
            "remaining_gap": "lambda_gamma_action_sign_and_binding_bound_source_rows",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        ("BCF4223_0_no_gamma_bulk_panic", "treat gamma psi psi_dot as automatic negative bulk energy", "blocked", "fixed gamma is a boundary term; real damping needs bath/open-flux row"),
        ("BCF4223_1_no_lambda_assumption", "assume lambda>=0 without source/signature row", "blocked", "core positivity depends on the potential sign"),
        ("BCF4223_2_no_binding_drop", "delete binding/stabilizer energy because ordinary matter is positive", "blocked", "negative binding must be included or bounded"),
        ("BCF4223_3_no_rest_mass_only", "use visible rest energy alone as E_plus proof", "blocked", "binding/core/open/reference/virial/frame terms still enter epsilon_E"),
        ("BCF4223_4_no_local_GR_claim", "promote the partial sign gate to local GR", "blocked", "M_EH and M_H_ref remain unavailable until the rows score"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move, status, reason in data
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "BCS4223_STATUS",
            "decision": DECISION,
            "summary": "MTS core energy is reduced to a canonical Hamiltonian sign gate plus lambda/gamma rows; binding/stabilizer is reduced to a bounded negative-fraction row. No MEH/local-GR claim.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4223 derives the core Hamiltonian/boundary split and binding-bound schema; the next executable row is lambda/gamma sign plus beta_bind or conservative component values.",
            "derive_first": "prove lambda>=0 and gamma is boundary/bath-balanced from the parent action",
            "fill_second": "source beta_bind, E_stab_neg_abs, E_gamma_bath_or_open_abs and E_signature_mismatch_abs rows",
            "fallback": "keep M_EH unavailable and score conservative epsilon_E_core_bind once values exist",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 239 - PPC4161 Binding/Stabilizer And MTS-Core Negative Energy Bound Or Parent Signature

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Purpose

4222 isolated the first sign-damaging sectors in the `M_EH` proof:

```text
E_binding_stabilizer_neg_abs,
E_MTS_core_neg_abs.
```

4223 tries to reduce both instead of simply relisting them.

## MTS core action sign

The source action has the schematic form:

```text
L_psi = (1/2c^2) psi_dot^2 - (1/2)|grad psi|^2 - gamma psi psi_dot - (lambda/n)|psi|^n.
```

For fixed `gamma`:

```text
- gamma psi psi_dot = -(gamma/2) d_t(psi^2).
```

So `gamma` is not automatically a negative bulk-energy term. It is either:

- a boundary term in the conservative action; or
- a real damping/open-system channel requiring a bath/flux energy row.

The canonical bulk Hamiltonian route is:

```text
H_psi = (1/2c^2) psi_dot^2 + (1/2)|grad psi|^2 + (lambda/n)|psi|^n + H_gamma_boundary.
```

Therefore:

```text
lambda >= 0, n > 0, gamma boundary/bath-balanced
=> E_MTS_core_neg_abs = 0.
```

If that is not signed, the honest fallback is:

```text
E_MTS_core_neg_abs
<= (max(0,-lambda)/n) int |psi|^n
 + E_gamma_bath_or_open_abs
 + E_signature_mismatch_abs.
```

## Binding/stabilizer bound

Binding is part of the single Hilbert source, not a second coupling. But negative binding energy can still damage the positivity bound. The needed row is:

```text
E_binding_stabilizer_neg_abs
<= beta_bind E_visible_rest + E_stab_neg_abs.
```

This becomes safe only when `beta_bind` and `E_stab_neg_abs` are source-backed and small enough relative to `E_plus_min`.

## Updated MEH gate

The next score is:

```text
epsilon_E_core_bind
= (E_binding_stabilizer_neg_abs + E_MTS_core_neg_abs)/E_plus_min.
```

No `M_EH` positivity claim follows until this and the open/reference/virial/frame rows are scored.

## Next target

`{NEXT_TARGET}` should fill the actual `lambda/gamma/beta_bind` source rows or prove the parent signature that makes them zero/safe.
"""


def checkpoint_doc() -> str:
    return f"""# 4223 - Binding/Stabilizer And MTS-Core Negative Energy Bound Or Parent Signature

**Status:** `{DECISION}`.

## Main move

This checkpoint does not just say "binding and core signs are missing." It derives the exact sign gate:

```text
H_psi = (1/2c^2) psi_dot^2 + (1/2)|grad psi|^2 + (lambda/n)|psi|^n + H_gamma_boundary.
```

`gamma psi psi_dot` is boundary-like for fixed `gamma`; if it is intended as physical damping, it is an open-system/bath row.

## Bound rows staged

- `E_MTS_core_neg_abs <= (max(0,-lambda)/n) int |psi|^n + E_gamma_bath_or_open_abs + E_signature_mismatch_abs`
- `E_binding_stabilizer_neg_abs <= beta_bind E_visible_rest + E_stab_neg_abs`

## Decision

No local-GR/Newton claim is made. The route is sharper, but the source rows for `lambda`, `gamma`, `beta_bind`, and stabilizer/core mismatch values are still missing.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The binding/stabilizer and MTS-core negative-energy obstruction is reduced to explicit sign and bound rows: the fixed-gamma psi term is a boundary term or an open-system bath row, the canonical psi Hamiltonian is nonnegative if lambda>=0 and n>0, and binding/stabilizer damage is bounded by beta_bind E_visible_rest + E_stab_neg_abs.",'
        f'"4223 source audit, core action sign derivation, binding bound rows, residual bound inputs, composed gates, decision and firewall.",'
        f'private_binding_core_negative_energy_gate_nonclaim,'
        f'"Fill or derive lambda/gamma action sign and beta_bind/stabilizer source rows.",'
        f'"This is a sharper sign-gate reduction, not an M_EH positivity proof; no local-GR/Newton claim follows until rows score."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 98. Binding And MTS-Core Negative Energy Gate

Marker: `{MARKER}`

4223 reduces the remaining sign-damaging energy pieces to:

```text
E_MTS_core_neg_abs
<= (max(0,-lambda)/n) int |psi|^n
 + E_gamma_bath_or_open_abs
 + E_signature_mismatch_abs,
```

and:

```text
E_binding_stabilizer_neg_abs
<= beta_bind E_visible_rest + E_stab_neg_abs.
```

The useful physics point is that fixed `gamma psi psi_dot` is boundary-like, while true damping must be bath-balanced. The next row must source `lambda`, `gamma` mode, and `beta_bind`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Binding/Core Energy Sign Gate

Marker: `{PACKET_MARKER}`

The packet now has a concrete sign route for the MTS core and a conservative binding/stabilizer bound schema. It remains private/nonclaim until `lambda>=0`, gamma boundary/bath balance, and binding/stabilizer fractions are source-backed.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4223_SOURCE_REGISTER.csv"]
    core = rows_by_file["P8_Y5_R2FR_4223_CORE_ACTION_SIGN.csv"]
    binding = rows_by_file["P8_Y5_R2FR_4223_BINDING_BOUND.csv"]
    residuals = rows_by_file["P8_Y5_R2FR_4223_RESIDUAL_BOUND_INPUTS.csv"]
    gates = rows_by_file["P8_Y5_R2FR_4223_COMPOSED_GATES.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4223_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4223_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4223_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]

    checks = [
        ("VAL4223_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4223_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4223_2_core_derivation",
            "core rows include gamma boundary, canonical Hamiltonian, lambda gate and negative fallback",
            {"CAS4223_1_gamma_boundary", "CAS4223_3_canonical_H", "CAS4223_4_lambda_sign", "CAS4223_5_negative_bound"}.issubset({row["core_id"] for row in core}),
        ),
        (
            "VAL4223_3_binding_bound",
            "binding rows include fraction bound and stability shortcut",
            {"BBS4223_1_negative_binding_fraction", "BBS4223_2_stability_shortcut", "BBS4223_3_no_component_cheat"}.issubset({row["binding_id"] for row in binding}),
        ),
        (
            "VAL4223_4_residual_inputs",
            "residual schema covers lambda, gamma, core, beta_bind, binding and epsilon score",
            {"lambda_sign", "gamma_mode", "E_MTS_core_neg_abs", "beta_bind", "E_binding_stabilizer_neg_abs", "epsilon_E_core_bind"}.issubset({row["quantity"] for row in residuals}),
        ),
        (
            "VAL4223_5_composed_gates",
            "composed gates include core zero route, binding small route and MEH feed",
            {"BCG4223_0_core_zero_route", "BCG4223_1_binding_small_route", "BCG4223_2_MEH_feed"}.issubset({row["gate_id"] for row in gates}),
        ),
        (
            "VAL4223_6_decision_nonclaim",
            "decision keeps values and local-GR unavailable",
            decision["lambda_sign_available"] == "False" and decision["binding_fraction_bound_available"] == "False" and decision["local_GR_claim"] == "False",
        ),
        (
            "VAL4223_7_firewall",
            "firewall blocks gamma panic, lambda assumption, binding drop, rest mass only and local GR claim",
            {"BCF4223_0_no_gamma_bulk_panic", "BCF4223_1_no_lambda_assumption", "BCF4223_2_no_binding_drop", "BCF4223_3_no_rest_mass_only", "BCF4223_4_no_local_GR_claim"}.issubset({row["firewall_id"] for row in firewalls}),
        ),
        (
            "VAL4223_8_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4223_9_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4223_10_claim_register", "claim register contains L-064", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4223_11_spine_packet", "spine and packet contain 4223 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4223_12_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4223_13_script_exists", "generator script exists", (SCRIPTS / "Y5_R2FR_4223_binding_stabilizer_and_MTS_core_negative_energy_bound_or_parent_signature.py").exists()),
        ("VAL4223_14_status", "status records nonclaim reduction", rows_by_file["P8_Y5_R2FR_4223_STATUS.csv"][0]["decision"] == DECISION),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4223_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4223_CORE_ACTION_SIGN.csv": core_action_rows(),
        "P8_Y5_R2FR_4223_BINDING_BOUND.csv": binding_bound_rows(),
        "P8_Y5_R2FR_4223_RESIDUAL_BOUND_INPUTS.csv": residual_bound_rows(),
        "P8_Y5_R2FR_4223_COMPOSED_GATES.csv": composed_gate_rows(),
        "P8_Y5_R2FR_4223_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4223_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4223_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4223_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)

    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8")
    update_registers()
    validation_rows = validate(rows_by_file)
    write_csv(VALIDATION_PATH, validation_rows)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={VALIDATION_PATH}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
