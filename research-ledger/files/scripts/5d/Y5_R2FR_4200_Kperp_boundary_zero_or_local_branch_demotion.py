from __future__ import annotations

import csv
import json
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4200"
CLAIM_ID = "L-041"
BRANCH_ID = "MTS_R2FR_Y5_KPERP_BOUNDARY_ZERO_OR_DEMOTION_4200"
DECISION = (
    "KPERP_ENERGY_ZERO_THEOREM_CONDITIONAL_BOUND_FALLBACK_ACTIVE_LOCAL_BRANCH_"
    "DEMOTED_UNTIL_PARENT_OPERATOR_BOUNDARY_KERNEL_SIGNED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md"
DOC_PATH = POST / "4200-Y5-R2FR-Kperp-boundary-zero-or-local-branch-demotion.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_KPERP_BOUNDARY_ZERO_OR_DEMOTION_4200"
PACKET_MARKER = "PPC4161_PACKET_KPERP_BOUNDARY_ZERO_OR_DEMOTION_4200"
NEXT_TARGET = "4201-Y5-R2FR-Kperp-finite-coefficient-vector-or-parent-tensor-operator-source.md"

SOURCES = {
    "SRC4200_00_4199_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4199_DECISION.csv",
        "Kperp_parent_signed",
        "4199 decision row identifies Kperp as unsigned.",
    ),
    "SRC4200_01_4199_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4199_BOUNDARY_KPERP_LEDGER.csv",
        "BK4199_1_Kperp_zero",
        "4199 boundary/Kperp ledger.",
    ),
    "SRC4200_02_73_kperp_energy": (
        FORMAL / "73-support-powers-kperp-lemma.md",
        "0 = <K_perp, L_T K_perp>",
        "Older Kperp zero-boundary energy lemma.",
    ),
    "SRC4200_03_74_kperp_result": (
        FORMAL / "74-support-powers-kperp-first-results.md",
        "separate positive elliptic/static zero-boundary lemma",
        "Prior support-powers/Kperp result.",
    ),
    "SRC4200_04_61_tensor_ansatz": (
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "partial_mu K_perp,loc^{mu nu} = 0",
        "Local tensor ansatz leaves divergence-free Kperp freedom.",
    ),
    "SRC4200_05_62_ppn_result": (
        FORMAL / "62-local-ppn-tensor-ansatz-first-results.md",
        "local_ppn_tensor_ansatz_open_amplitude_required",
        "PPN ansatz result requires Kperp choice or bound.",
    ),
    "SRC4200_06_192_no_flux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.",
        "Private local no-flux/boundary routing theorem.",
    ),
    "SRC4200_07_3974_boundary_certificate": (
        SOURCE_DIR / "P8_Y5_R2FR_3974_PARENT_BOUNDARY_ACTION_CONTRACT.csv",
        "BAC3974_5_certificate",
        "Boundary action Z_B certificate contract.",
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


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def zero_clause_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "KZ4200_0_parent_tensor_equation",
            "parent tensor equation",
            "P_perp(delta S_parent/delta g) gives L_T K_perp = S_T with S_T=0 in the compact local branch",
            "required",
            "unsigned",
            "No parent-owned second-variation/tensor operator row currently derives L_T and S_T=0.",
        ),
        (
            "KZ4200_1_positive_static_operator",
            "positive elliptic/static operator",
            "<K,L_T K> >= c_grad ||D K||^2 + c_mass ||K||^2 with c_grad>0 and c_mass>=0",
            "required",
            "unsigned",
            "73/74 state this as the valid route, but do not parent-sign ellipticity/staticity or positivity.",
        ),
        (
            "KZ4200_2_boundary_zero_or_routed",
            "zero boundary / routed radiative charge",
            "K_perp|partial W=0 or decay/no-incoming data, with any F_rad routed as Hamiltonian boundary charge",
            "required",
            "conditional_unsigned",
            "192 gives a private selector theorem and 3974 gives a Z_B contract, but parent boundary signature is missing.",
        ),
        (
            "KZ4200_3_trivial_kernel",
            "no homogeneous TT zero mode",
            "ker(L_T) intersect divergence-free local tensor sector = {0}",
            "required",
            "unsigned",
            "Neumann-like constants, topology, gauge representatives, or incoming homogeneous waves are not excluded by parent data.",
        ),
        (
            "KZ4200_4_no_source_projection",
            "no transverse source projection",
            "S_T=P_perp(source/current/sector leakage)=0 through the local PPN order being claimed",
            "required",
            "unsigned",
            "Scalar support powers do not automatically kill transverse tensor source projection.",
        ),
        (
            "KZ4200_5_total_zero_certificate",
            "Kperp zero theorem",
            "all clauses KZ4200_0..4 signed => K_perp=0 by energy identity",
            "derived_conditional",
            "not_parent_signed",
            "The conditional proof is exact, but the premises are not all parent-owned; no local-GR claim follows.",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_form": mathematical_form,
            "requirement_level": requirement_level,
            "current_status": current_status,
            "reason": reason,
            "parent_signed": "False" if clause_id != "KZ4200_5_total_zero_certificate" else "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, mathematical_form, requirement_level, current_status, reason in rows
    ]


def energy_identity_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "EI4200_0_equation",
            "start from tensor equation",
            "L_T K_perp = 0",
            "requires parent-owned local tensor operator and zero transverse source",
            "conditional",
        ),
        (
            "EI4200_1_pairing",
            "multiply by Kperp and integrate over W_loc",
            "0=<K_perp,L_T K_perp>_W",
            "requires fixed inner product, measure/coframe descent, and controlled boundary terms",
            "conditional",
        ),
        (
            "EI4200_2_coercivity",
            "integrate by parts",
            "<K,L_T K> >= c_grad||D K||^2+c_mass||K||^2 - B_T",
            "requires positive static/elliptic operator and nonnegative/routed boundary form",
            "conditional",
        ),
        (
            "EI4200_3_zero_result",
            "zero boundary and no kernel",
            "B_T=0 and ker(L_T)=0 imply ||K_perp||_E=0",
            "proves K_perp=0 only under all zero clauses",
            "derived_conditional",
        ),
        (
            "EI4200_4_failure_formula",
            "if clauses fail",
            "||K_perp||_E <= C_T (||S_T|| + ||B_T|| + ||I_T|| + ||Z_T||)",
            "fallback bound keeps every obstruction explicit rather than hidden in A_J",
            "fallback_active",
        ),
    ]
    return [
        {
            **common(),
            "identity_id": identity_id,
            "step": step,
            "formula": formula,
            "required_premise": required_premise,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for identity_id, step, formula, required_premise, status in rows
    ]


def fallback_bound_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "KB4200_0_transverse_source",
            "S_T",
            "P_perp(source/current/sector leakage)",
            "||S_T||",
            "missing_parent_zero_or_numeric_value",
            "feeds delta_gamma, xi, alpha_i depending on tensor/vector split",
        ),
        (
            "KB4200_1_boundary_data",
            "B_T",
            "nonzero Dirichlet/Robin/surface/Hamiltonian boundary obstruction",
            "||B_T||",
            "missing_ZB_or_boundary_norm",
            "feeds boundary hair and can dominate A_boundary/U_B^2",
        ),
        (
            "KB4200_2_incoming_modes",
            "I_T",
            "incoming hyperbolic/radiative homogeneous tensor memory",
            "||I_T||",
            "missing_no_incoming_certificate",
            "not killed by static elliptic proof; must be absent or routed",
        ),
        (
            "KB4200_3_zero_mode_projection",
            "Z_T",
            "projection on ker(L_T) or TT/topological/gauge zero-mode sector",
            "||P_ker K_perp||",
            "missing_kernel_certificate",
            "Neumann/topology/gauge freedom can survive no-flux",
        ),
        (
            "KB4200_4_operator_inverse",
            "C_T",
            "coercivity inverse/resolvent norm",
            "1/c_T",
            "missing_positive_operator_value",
            "needed to convert obstruction norms into PPN residual bounds",
        ),
        (
            "KB4200_5_ppn_projection",
            "W_i^K",
            "observable projection weights",
            "|R_i^K| <= W_i^K ||K_perp||_E",
            "missing_metric_projection_coefficients",
            "needed for delta_gamma, alpha1, alpha2, xi, beta, clocks and Gdot rows",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "bound_slot": bound_slot,
            "current_status": current_status,
            "observable_impact": observable_impact,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, symbol, definition, bound_slot, current_status, observable_impact in rows
    ]


def boundary_interface_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BI4200_0_no_flux_scope",
            "192 no-flux theorem",
            "closes compact transition current J_tr under selector clauses",
            "does_not_by_itself_zero_Kperp",
            "A divergence-free homogeneous tensor can remain even when transition flux is routed.",
        ),
        (
            "BI4200_1_ZB_scope",
            "3974 Z_B boundary certificate",
            "would kill boundary vector/tensor/normal hair if scalar-zero/no-marker/full-variation/no-normal/derivative clauses are signed",
            "useful_but_unsigned",
            "Z_B attacks boundary hair; Kperp also needs operator positivity and trivial kernel.",
        ),
        (
            "BI4200_2_energy_bridge",
            "4200 bridge",
            "Z_B=1 can set B_T=0; it cannot set S_T=I_T=Z_T=0 without tensor operator clauses",
            "bridge_contract",
            "This prevents overusing boundary no-hair as a transverse tensor no-hair theorem.",
        ),
    ]
    return [
        {
            **common(),
            "interface_id": interface_id,
            "input": input_name,
            "scope": scope,
            "4200_use": use,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for interface_id, input_name, scope, use, guard in rows
    ]


def demotion_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEM4200_0_all_signed",
            "L_T owned, positive, zero/routed boundary, no kernel, no source projection",
            "promote Kperp exact-zero subclaim inside private local branch",
            "not_current_state",
        ),
        (
            "DEM4200_1_boundary_signed_only",
            "Z_B/no-flux closes B_T but S_T/I_T/Z_T remain unsigned",
            "keep finite Kperp residual vector; do not claim exact local GR",
            "possible_future_partial",
        ),
        (
            "DEM4200_2_current_state",
            "any of L_T positivity, source projection, boundary data, incoming mode or kernel clause is unsigned",
            "demote exact clean local-GR route; retain explicit finite closure/bound route",
            "current_state",
        ),
    ]
    return [
        {
            **common(),
            "demotion_id": demotion_id,
            "condition": condition,
            "action": action,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for demotion_id, condition, action, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "energy_identity_derived": "True",
            "Kperp_zero_parent_signed": "False",
            "boundary_ZB_parent_signed": "False",
            "fallback_bound_ready": "True",
            "exact_local_GR_route_status": "demoted_until_tensor_operator_boundary_kernel_signed",
            "finite_residual_route_status": "active_nonclaim",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4200_0_divfree_not_zero", "partial_mu K_perp^{mu nu}=0 is not K_perp=0."),
        ("FW4200_1_no_flux_not_tensor_nohair", "local no-flux closes transition current only under selector clauses; it does not erase TT homogeneous modes."),
        ("FW4200_2_boundary_not_bulk", "Z_B or boundary no-hair can set B_T=0, but not S_T, I_T, Z_T, or operator positivity."),
        ("FW4200_3_static_not_hyperbolic", "elliptic/static energy proof cannot be used on incoming hyperbolic/radiative modes."),
        ("FW4200_4_finite_bound_not_pass", "a fallback norm contract is not a PPN pass until coefficients and observable weights are sourced."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": (
                "4200 derives the conditional Kperp energy zero theorem and exact fallback norm, "
                "but parent tensor operator positivity, boundary zero, source silence, no-incoming and kernel-trivial clauses remain unsigned."
            ),
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4200 converts Kperp into a finite explicit obstruction vector; next step must source/derive those coefficients or parent-sign L_T.",
            "route_A": "derive parent tensor operator L_T, coercivity c_T, zero source projection, and trivial kernel",
            "route_B": "fill finite Kperp coefficient vector S_T,B_T,I_T,Z_T,C_T,W_i^K for PPN comparison",
            "route_C": "if neither closes, keep local branch as phenomenological closure rather than derived local GR",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4200_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4200_KPERP_ZERO_CLAUSES.csv": zero_clause_rows(),
        "P8_Y5_R2FR_4200_ENERGY_IDENTITY.csv": energy_identity_rows(),
        "P8_Y5_R2FR_4200_FALLBACK_BOUND_VECTOR.csv": fallback_bound_rows(),
        "P8_Y5_R2FR_4200_BOUNDARY_INTERFACE.csv": boundary_interface_rows(),
        "P8_Y5_R2FR_4200_DEMOTION_LEDGER.csv": demotion_rows(),
        "P8_Y5_R2FR_4200_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4200_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4200_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4200_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 216 - PPC4161 Kperp Boundary Zero Or Demotion

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint proves the exact conditional route that would kill `K_perp`, but it does not parent-sign the required tensor operator, boundary, source-projection, incoming-mode, or kernel clauses.

## The Actual Zero Theorem

The leftover local tensor freedom is:

```text
partial_mu K_perp,loc^{{mu nu}} = 0.
```

That is not enough. The zero theorem needs a parent-owned local tensor boundary-value problem:

```text
L_T K_perp = 0
```

with `L_T` positive/self-adjoint on the compact local branch, zero or routed boundary data, no incoming homogeneous tensor memory, and no zero modes.

The proof is the energy identity:

```text
0 = <K_perp, L_T K_perp>
  >= c_grad ||D K_perp||^2 + c_mass ||K_perp||^2.
```

If `c_grad>0`, `c_mass>=0`, the boundary form is zero/nonnegative, and the kernel is trivial, then:

```text
K_perp = 0.
```

## Why It Does Not Close Yet

The current corpus has the shape of this theorem, but not the parent signature. In particular:

```text
divergence-free != zero,
local no-flux != transverse tensor no-hair,
boundary Z_B != bulk operator positivity,
elliptic/static proof != hyperbolic incoming-mode proof.
```

## Fallback Bound

If any clause is unsigned, retain the explicit obstruction vector:

```text
||K_perp||_E <= C_T (||S_T|| + ||B_T|| + ||I_T|| + ||Z_T||).
```

where `S_T` is transverse source projection, `B_T` is boundary obstruction, `I_T` is incoming tensor memory, and `Z_T` is zero-mode projection. Observable rows must then use:

```text
|R_i^K| <= W_i^K ||K_perp||_E.
```

## Verdict

4200 moves the work forward by changing the blocker from a vague phrase into a theorem-or-bound contract. Exact local GR is demoted until the parent signs `L_T`, positivity, boundary zero/routing, source silence, no incoming modes, and trivial kernel.

## Next Gate

`{NEXT_TARGET}` should either parent-sign the tensor operator or fill finite sourced coefficient rows for `S_T`, `B_T`, `I_T`, `Z_T`, `C_T`, and `W_i^K`.
"""
    checkpoint = f"""# 4200 - Y5 R2FR Kperp Boundary Zero Or Local Branch Demotion

Decision: `{DECISION}`

## Summary

4200 attempts the `K_perp` proof directly. The conditional theorem is valid:

```text
L_T K_perp=0,
<K,L_T K> >= c_grad||D K||^2+c_mass||K||^2,
zero/routed boundary,
no incoming modes,
ker(L_T)=0
=> K_perp=0.
```

But those clauses are not parent-signed in the current corpus.

## Practical Outcome

This is a real narrowing rather than another missing-list. The exact clean local-GR route is demoted unless 4201 can either:

```text
derive parent ownership of L_T and its boundary/kernel clauses,
```

or fill:

```text
S_T, B_T, I_T, Z_T, C_T, W_i^K
```

as finite sourced rows for PPN comparison.

No public/local-GR claim is allowed from this checkpoint.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,"The K_perp exact-zero theorem is reduced to a positive tensor energy identity, '
        f'but parent tensor-operator, boundary, source-projection, incoming-mode and kernel clauses remain unsigned; '
        f'a finite obstruction-vector fallback is now explicit.","4200 source audit, Kperp zero clauses, energy identity, '
        f'fallback bound vector, boundary interface, demotion ledger, decision row and nonclaim firewall.",'
        f'private_conditional_Kperp_energy_theorem_nonclaim_fallback_bound_active,'
        f'"Derive parent L_T/coercivity/boundary/kernel/source clauses or fill finite S_T/B_T/I_T/Z_T/C_T/W_i^K rows against PPN gates.",'
        f'"Divergence-free K_perp or local no-flux could be mistaken for tensor no-hair unless the operator, boundary and kernel clauses are explicit."'
    )
    claims_text = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," not in claims_text:
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Kperp Boundary Zero Or Demotion - 4200

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4200 proves the conditional tensor no-hair route:

```text
L_T K_perp=0 and <K,L_TK> coercive
plus zero/routed boundary, no incoming modes and trivial kernel
=> K_perp=0.
```

Current status remains nonclaim because those clauses are not parent-signed. The exact local-GR branch is demoted until the parent tensor operator closes or the finite fallback vector `S_T,B_T,I_T,Z_T,C_T,W_i^K` is sourced."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Kperp Boundary Zero Or Demotion - 4200

Marker: `{PACKET_MARKER}`

Inside the private packet, `Kperp` is now governed by an explicit theorem-or-bound split:

```text
zero theorem if parent-owned L_T is positive/static with zero/routed boundary and trivial kernel;
otherwise ||K_perp||_E <= C_T(||S_T||+||B_T||+||I_T||+||Z_T||).
```

The packet remains nonclaim until the parent signs the operator/boundary/kernel clauses or finite PPN projection coefficients are sourced."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4200_SOURCE_REGISTER.csv"]
    clauses = rows_by_file["P8_Y5_R2FR_4200_KPERP_ZERO_CLAUSES.csv"]
    identity = rows_by_file["P8_Y5_R2FR_4200_ENERGY_IDENTITY.csv"]
    fallback = rows_by_file["P8_Y5_R2FR_4200_FALLBACK_BOUND_VECTOR.csv"]
    interface = rows_by_file["P8_Y5_R2FR_4200_BOUNDARY_INTERFACE.csv"]
    demotion = rows_by_file["P8_Y5_R2FR_4200_DEMOTION_LEDGER.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4200_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4200_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4200_1_source_needles", "all source required text markers found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4200_2_zero_clauses", "all five zero theorem clauses plus total certificate are present", len(clauses) == 6),
        ("VAL4200_3_energy_identity", "energy identity contains coercive zero result and fallback formula", any(row["identity_id"] == "EI4200_3_zero_result" for row in identity) and any(row["identity_id"] == "EI4200_4_failure_formula" for row in identity)),
        ("VAL4200_4_fallback_vector", "fallback vector includes S_T, B_T, I_T, Z_T, C_T and W_i^K", {row["symbol"] for row in fallback} == {"S_T", "B_T", "I_T", "Z_T", "C_T", "W_i^K"}),
        ("VAL4200_5_interface_guard", "boundary/no-flux scope guard is explicit", any(row["4200_use"] == "does_not_by_itself_zero_Kperp" for row in interface)),
        ("VAL4200_6_demotion_active", "current demotion row is active", any(row["status"] == "current_state" for row in demotion)),
        ("VAL4200_7_decision_nonclaim", "decision keeps Kperp zero unsigned and local claim false", decision[0]["Kperp_zero_parent_signed"] == "False" and decision[0]["claim_allowed"] == "False"),
        ("VAL4200_8_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4200_9_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4200_10_claim_register", "claim register contains L-041", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4200_11_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4200_12_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    rows_by_file = all_rows()
    write_docs()
    update_registers()
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4200_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4200 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4200_VALIDATION.csv'}")
    print("rows=13 validation checks")


if __name__ == "__main__":
    main()
