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

CHECKPOINT = "4187"
BRANCH_ID = "MTS_R2FR_Y5_CGAMMA_MEMORY_SUPPORT_PROJECTOR_ZERO_4187"
DECISION = (
    "CGAMMA_ZERO_ROUTES_AUDITED_SUPPORT_PROJECTOR_CONTRACT_WRITTEN_"
    "PARENT_ZERO_NOT_CLOSED_FINITE_BOUND_INTERFACE_READY_NONCLAIM"
)
DOC_PATH = POST / "4187-Y5-R2FR-local-memory-support-projector-zero-law-for-cGamma-or-PPN-clock-bound.md"
FORMAL_203_PATH = FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-028"
SPINE_MARKER = "PPC4161_LOCAL_MEMORY_SUPPORT_PROJECTOR_CGAMMA_4187"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_MEMORY_SUPPORT_PROJECTOR_CGAMMA_4187"
NEXT_TARGET = "4188-Y5-R2FR-finite-cGamma-PPN-clock-orbital-bound-runner-or-support-proof.md"

SOURCES = {
    "SRC4187_00_4186_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4186_NEXT_TARGET.csv",
        "derive local memory support/projector zero",
        "4186 handoff: c_Gamma must be attacked directly.",
    ),
    "SRC4187_01_formal_202": (
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "c_Gamma_parent_zero = false",
        "4186 formal result: c_D and delta_kappa close privately, c_Gamma remains open.",
    ),
    "SRC4187_02_blocker_ledger": (
        SOURCE_DIR / "P8_Y5_R2FR_4186_CGAMMA_MEMORY_BLOCKER_LEDGER.csv",
        "local support law missing",
        "Primary c_Gamma blocker ledger.",
    ),
    "SRC4187_03_bound_interface": (
        SOURCE_DIR / "P8_Y5_R2FR_4186_BOUND_RUNNER_INTERFACE.csv",
        "active_next_bound_or_zero_target",
        "4186 finite-bound interface handoff.",
    ),
    "SRC4187_04_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "Vertical Silence Proof",
        "Vertical quotient silence route.",
    ),
    "SRC4187_05_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "route as boundary charge, not hidden bulk current",
        "Boundary/Hamiltonian routing route.",
    ),
    "SRC4187_06_redteam_support": (
        FORMAL / "06-consistency-red-team.md",
        "source_support_boundary_law_conditional_open",
        "Red-team support warning.",
    ),
    "SRC4187_07_redteam_tensor": (
        FORMAL / "06-consistency-red-team.md",
        "Scalar memory support does not erase divergence-free homogeneous tensor modes",
        "Tensor/homogeneous residual warning.",
    ),
    "SRC4187_08_palatini_selector": (
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "local memory couplings -> coefficient `c_Gamma`",
        "c_Gamma residual origin.",
    ),
    "SRC4187_09_residual_map": (
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "c_Gamma    local memory hair",
        "4185 residual coefficient map.",
    ),
    "SRC4187_10_thresholds": (
        FORMAL / "102-transition-closure-observable-threshold-spec.md",
        "S_PPN_residual_norm = max absolute component of the local PPN residual vector",
        "PPN residual vector threshold target.",
    ),
    "SRC4187_11_local_pack": (
        FORMAL / "189-PPC4161-local-empirical-validation-pack.md",
        "Private nonclaim",
        "Local empirical comparator pack remains nonclaim.",
    ),
    "SRC4187_12_recovery_bookmark": (
        POST / "RECOVERY_BOOKMARK_2026-07-03_after_drive_swap.md",
        "Treat the `D:` local project as the canonical head",
        "Drive-swap recovery bookmark.",
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


def zero_route_audit_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ZR4187_0_vertical_quotient",
            "vertical quotient route",
            "If Gamma_mem is purely vertical or representative-only, Dq[delta Gamma_mem]=0, and all ordinary local readouts factor through q, then P_loc(delta S_Gamma)=0.",
            "conditional theorem available",
            "not closed",
            "The corpus proves vertical silence for known ordinary readouts, but does not yet prove Gamma_mem has no q-horizontal component.",
            "prove Gamma_mem in ker(Dq) or split Gamma_mem=Gamma_vertical+Gamma_horizontal with a bound on the horizontal part",
        ),
        (
            "ZR4187_1_compact_support",
            "compact local support route",
            "If supp(Gamma_mem) is disjoint from the compact local collar W_loc, or P_loc Gamma_mem=0 throughout W_loc, then the bulk c_Gamma projector vanishes.",
            "exact if support law is parent-owned",
            "not closed",
            "The support/locality theorem is still missing, and constant memory pieces can renormalize local invariant coefficients unless fixed by a selector.",
            "derive support separation from the parent memory equation or demote it to finite screening",
        ),
        (
            "ZR4187_2_boundary_routing",
            "boundary/Hamiltonian routing route",
            "If the memory flux is a divergence or symplectic boundary charge with zero compact side flux, its local bulk Euler derivative is silent.",
            "conditional theorem available",
            "not closed",
            "The local no-flux theorem routes known transition/radiative pieces, but c_Gamma-specific memory flux has not been parent-identified as a boundary charge.",
            "derive J_Gamma_bulk=0 and F_Gamma_boundary as the only nonzero memory term",
        ),
        (
            "ZR4187_3_positive_no_hair",
            "positive/no-hair route",
            "If Gamma_mem obeys a positive local operator L_Gamma Gamma_mem=J_Gamma with J_Gamma=0 and zero boundary data on W_loc, then Gamma_mem=0 in W_loc.",
            "valid mathematical route",
            "not closed",
            "The parent operator, sign, source term, and boundary data are not all present in the corpus.",
            "construct L_Gamma, prove positivity/coercivity, prove J_Gamma=0 for ordinary compact matter, and lock boundary data",
        ),
        (
            "ZR4187_4_screening",
            "finite screening route",
            "If P_loc(delta S_Gamma) is nonzero but below each arena threshold, c_Gamma is bounded rather than zero.",
            "fallback not proof",
            "ready as nonclaim",
            "Screening can save phenomenology but is not a derived local-GR theorem unless the suppression law is parent-owned.",
            "build PPN, clock, orbital and R10 projection rows with units and source-backed thresholds",
        ),
        (
            "ZR4187_5_homogeneous_tensor",
            "homogeneous tensor residue route",
            "Even scalar support silence is insufficient if a divergence-free Gamma_perp/K_perp tensor mode survives local projection.",
            "hard obstruction",
            "open",
            "This is the cleanest reason the route cannot be closed by scalar support alone.",
            "prove tensor boundary no-hair or include Gamma_perp in the finite residual vector",
        ),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "zero_condition": zero_condition,
            "mathematical_status": mathematical_status,
            "current_status": current_status,
            "why_not_claimed": why_not_claimed,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for (
            route_id,
            route,
            zero_condition,
            mathematical_status,
            current_status,
            why_not_claimed,
            next_action,
        ) in rows
    ]


def support_projector_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SP4187_0_action_term",
            "local memory action term",
            "S_Gamma[U] = integral_U sqrt(-g_obs) c_Gamma Gamma_mem I_local[g_obs,R,T,source] + boundary",
            "defines the residual whose local projection must vanish or be bounded",
            "written",
        ),
        (
            "SP4187_1_projector",
            "local observable projector",
            "E_Gamma^loc := P_loc(delta S_Gamma / delta O_loc), where O_loc includes metric, clock, source and EM readouts.",
            "the local-GR condition is E_Gamma^loc=0, not merely small-looking prose",
            "written",
        ),
        (
            "SP4187_2_exact_zero",
            "exact zero law",
            "c_Gamma is locally silent iff P_loc[Gamma_mem E_I + derivative terms in Gamma_mem + J_Gamma I_local + H_Gamma_perp]=0.",
            "this is the derived contract a parent action must satisfy",
            "conditional theorem",
        ),
        (
            "SP4187_3_vertical_clause",
            "vertical clause",
            "P_loc Dq[delta Gamma_mem]=0 and Dq readouts ignore the representative direction.",
            "kills representative-only memory",
            "unsigned for Gamma_mem",
        ),
        (
            "SP4187_4_support_clause",
            "support clause",
            "P_loc Gamma_mem=0 or Gamma_mem is fixed/constant in a way already absorbed by calibrated parent coefficients.",
            "kills compact local bulk amplitude",
            "unsigned",
        ),
        (
            "SP4187_5_bulk_source_clause",
            "bulk source clause",
            "J_Gamma_bulk=0 for ordinary compact matter after Hilbert source descent and same-coframe locking.",
            "prevents matter from exciting local memory hair",
            "unsigned",
        ),
        (
            "SP4187_6_boundary_clause",
            "boundary clause",
            "F_Gamma appears only as a Hamiltonian boundary charge with no compact side flux into local tests.",
            "routes radiative memory away from local bulk force laws",
            "unsigned for Gamma_mem",
        ),
        (
            "SP4187_7_tensor_clause",
            "homogeneous tensor clause",
            "Gamma_perp/K_perp divergence-free homogeneous modes vanish or are bounded in the same projector norm.",
            "prevents scalar support from hiding tensor local hair",
            "unsigned",
        ),
        (
            "SP4187_8_claim_gate",
            "claim gate",
            "All clauses SP4187_3 through SP4187_7 must be parent-owned before c_Gamma_parent_zero=true.",
            "keeps local-GR claim blocked while any clause is missing",
            "active",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "clause": clause,
            "statement": statement,
            "consequence": consequence,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, clause, statement, consequence, status in rows
    ]


def finite_bound_interface_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FB4187_0_PPN",
            "PPN",
            "c_Gamma, Gamma_mem profile, J_PPN^Gamma, Gamma_perp/K_perp contribution, PPN residual vector components",
            "dimensionless max-norm against S_PPN_residual_norm threshold",
            "not claim-ready",
        ),
        (
            "FB4187_1_clock",
            "clock/redshift",
            "c_Gamma, local time-frequency projection J_clock^Gamma, environmental source profile, units",
            "fractional frequency/redshift residual",
            "not claim-ready",
        ),
        (
            "FB4187_2_orbital",
            "orbital/LLR/Gdot",
            "c_Gamma, radial acceleration projection J_orbital^Gamma, perihelion/Gdot envelope, source path",
            "acceleration or fractional Gdot/perihelion residual",
            "best first empirical fallback",
        ),
        (
            "FB4187_3_R10",
            "R10 short-range",
            "c_Gamma, Yukawa/range projection lambda_Gamma, alpha_Gamma(lambda), reviewed bound curve row",
            "abs(alpha_predicted)<=alpha_bound",
            "deferred until curve and projection are both real",
        ),
        (
            "FB4187_4_EM_Poynting",
            "EM/Poynting side-channel",
            "memory-driven Hodge or stress leakage into EM propagation/Poynting flux",
            "must be zero by same-Hodge owner or finite bounded",
            "watchlist only",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "arena": arena,
            "required_inputs": required_inputs,
            "comparison_quantity": comparison_quantity,
            "status": status,
            "numeric_prediction_available": "False",
            "source_backed_threshold_available": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, arena, required_inputs, comparison_quantity, status in rows
    ]


def branch_decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "BD4187_0",
            "decision": DECISION,
            "derive_result": "exact support/projector contract written, but parent-owned zero clauses do not all close",
            "c_Gamma_parent_zero": "False",
            "finite_bound_interface_ready": "True",
            "selected_next_target": NEXT_TARGET,
            "why": "The vertical, support, boundary and no-hair routes are mathematically clean, but current sources do not prove Gamma_mem is vertical, compact-silent, boundary-only, source-free, and tensor-no-hair all at once.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FW4187_0_local_GR",
            "local GR pass cannot be claimed while c_Gamma_parent_zero=false and no finite c_Gamma bounds exist",
        ),
        (
            "FW4187_1_R10",
            "R10 pass cannot be claimed without source-backed alpha(lambda) rows and a real c_Gamma projection",
        ),
        (
            "FW4187_2_PPN_clock_orbital",
            "PPN, clock and orbital passes cannot be claimed without projection Jacobians, units, thresholds and no-cancellation guards",
        ),
        (
            "FW4187_3_public_language",
            "Public-facing language must say c_Gamma remains the active local-memory residual unless 4188 closes proof or bounds",
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


def status_rows(
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "zero_routes_audited": "True",
            "support_projector_contract_written": "True",
            "vertical_route_conditional": "True",
            "boundary_route_conditional": "True",
            "positive_no_hair_route_conditional": "True",
            "c_Gamma_parent_zero": "False",
            "finite_cGamma_bound_interface_ready": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_cGamma_prediction_available": "False",
            "formal_203_written": str(FORMAL_203_PATH.exists()),
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
            "why": "4187 converts c_Gamma into an exact support/projector contract but does not prove every parent zero clause. The next step must either close the Gamma_mem support/no-hair theorem or build a finite nonclaim bound runner.",
            "route_A": "derive Gamma_mem vertical/support/boundary/no-hair clauses directly from the parent memory equation",
            "route_B": "build finite c_Gamma PPN-clock-orbital runner using explicit profiles, units, thresholds and source paths",
            "recommended_first": "orbital_or_PPN_bound_if_zero_proof_stalls",
            "public_claim_policy": "no public local-GR/R10/PPN/clock/orbital claim while c_Gamma has no parent zero or sourced finite bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc_text() -> str:
    return f"""# 203 - PPC4161 Local Memory Support-Projector Zero Law For c_Gamma

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint derives the exact local support/projector contract that would set `c_Gamma` to zero, then audits whether the current corpus actually satisfies it. It does **not** claim public local GR, PPN, clocks, orbital, R10, or a sourced finite `c_Gamma` bound.

## Local Memory Residual

The remaining residual after the same-coframe/source-coupling closure is:

```text
S_Gamma[U] = integral_U sqrt(-g_obs) c_Gamma Gamma_mem I_local[g_obs, R, T, source] + boundary.
```

The local test condition is not `Gamma_mem sounds small`. It is:

```text
E_Gamma^loc := P_loc(delta S_Gamma / delta O_loc) = 0,
```

where `O_loc` includes the metric, clock, source, orbital and EM/Poynting readouts used by compact local tests.

## Exact Contract

The parent route to `c_Gamma_parent_zero=true` requires:

```text
P_loc[
  Gamma_mem E_I
  + derivative terms in Gamma_mem
  + J_Gamma I_local
  + H_Gamma_perp
] = 0.
```

This gives five hard clauses:

1. `Gamma_mem` is vertical/readout-only, or its q-horizontal projection vanishes.
2. `P_loc Gamma_mem = 0` in the compact local collar, or any constant part is already absorbed by calibrated parent coefficients.
3. `J_Gamma_bulk = 0` for ordinary compact matter after Hilbert source descent.
4. memory flux is routed as a Hamiltonian boundary charge, not a hidden bulk source.
5. no divergence-free homogeneous tensor mode `Gamma_perp/K_perp` survives the same projector.

If all five are parent-owned, `c_Gamma=0` in compact local tests. If any one is missing, the theory must use a finite residual bound instead.

## Audit Verdict

The current corpus has strong conditional pieces:

- quotient naturality gives a vertical-silence theorem for ordinary local readouts;
- the no-flux theorem gives a boundary-routing template;
- same-coframe/Hilbert-source descent removes `c_D` and `delta_kappa` style leaks;
- the red-team file already identifies support and tensor boundary silence as the remaining gap.

But the current corpus does not yet prove that `Gamma_mem` itself is vertical, compact-support silent, boundary-only, source-free, and tensor-no-hair. Therefore:

```text
c_Gamma_parent_zero = false
finite_cGamma_bound_interface_ready = true
public_local_GR_claim_allowed = false
```

## Next Gate

The next gate is `{NEXT_TARGET}`:

- route A: derive the missing support/no-hair clauses directly from the parent memory equation;
- route B: build finite `c_Gamma` bounds for PPN, clocks, orbital systems and R10, with units and source paths.
"""


def checkpoint_doc_text() -> str:
    return f"""# 4187 - Local Memory Support-Projector Zero Law For c_Gamma Or PPN/Clock Bound

Generated by: `post-checkpoint-work/scripts/Y5_R2FR_4187_cGamma_memory_support_projector_zero.py`

## Summary

This checkpoint attacks the last root local-GR blocker left by 4186: `c_Gamma`, the local memory-hair residual. It derives the exact local projector condition that must vanish and then audits every plausible zero route.

## Result

The useful theorem is now precise:

```text
P_loc(delta S_Gamma / delta O_loc) = 0
```

requires vertical silence, compact support silence, zero ordinary bulk source, boundary/Hamiltonian routing and no surviving homogeneous tensor mode. The current corpus has conditional tools for several clauses, but it does not parent-sign all of them for `Gamma_mem`.

## Decision

`{DECISION}`

## Outputs

- `formalization-workbench/203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md`
- `source-intake/mts_residuals/P8_Y5_R2FR_4187_CGAMMA_ZERO_ROUTE_AUDIT.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4187_MEMORY_SUPPORT_PROJECTOR_CONTRACT.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4187_FINITE_CGAMMA_BOUND_INTERFACE.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4187_BRANCH_DECISION.csv`

## Nonclaim Firewall

No local-GR, R10, PPN, clock or orbital success claim is allowed from this checkpoint. The output is a contract plus a finite-bound interface, not a pass.
"""


def ensure_formal_doc() -> None:
    FORMAL_203_PATH.write_text(formal_doc_text(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc_text(), encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "Local memory support/projector zero contract for c_Gamma has been derived as a conditional gate; current parent corpus does not close every zero clause.",
            "current_evidence": "4187 zero-route audit, support/projector contract, finite c_Gamma PPN/clock/orbital/R10 interface and nonclaim firewall.",
            "status": "private_conditional_contract_nonclaim_cGamma_parent_zero_false_finite_bound_interface_ready",
            "next_test": "Derive Gamma_mem vertical/support/boundary/no-hair clauses from parent memory equation or run finite c_Gamma bound runner with real source rows.",
            "key_risk": "Scalar support or boundary prose could hide a surviving q-horizontal or divergence-free tensor memory mode.",
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "appended"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4187 Local Memory Support-Projector c_Gamma Gate

Marker: `{PACKET_MARKER}`

`post-checkpoint-work/4187-Y5-R2FR-local-memory-support-projector-zero-law-for-cGamma-or-PPN-clock-bound.md` derives the exact local projector contract for the remaining `c_Gamma` memory-hair residual:

```text
P_loc(delta S_Gamma / delta O_loc) = 0
```

The contract requires vertical silence, compact support silence, zero ordinary bulk source, boundary/Hamiltonian routing and no homogeneous tensor memory residue. Current sources do not prove all clauses for `Gamma_mem`, so:

```text
c_Gamma_parent_zero = false
finite_cGamma_bound_interface_ready = true
public_local_GR_claim_allowed = false
```
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "appended"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Local Memory Support-Projector c_Gamma Gate

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4187 sharpens the final root local-GR blocker. After 4186, `c_D` and `delta_kappa` are privately closed by same-coframe/source-coupling logic, but `c_Gamma` remains. The exact required condition is:

```text
P_loc(delta S_Gamma / delta O_loc) = 0.
```

This closes only if `Gamma_mem` is vertical/readout-only, compact-support silent, ordinary-source silent, boundary-routed and tensor-no-hair in the same local projector. The current corpus has conditional tools but does not parent-sign all clauses, so the next target is a finite `c_Gamma` PPN/clock/orbital/R10 runner or a true parent support/no-hair proof.
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "appended"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source_register = rows_by_name["P8_Y5_R2FR_4187_SOURCE_REGISTER"]
    status = rows_by_name["P8_Y5_R2FR_4187_STATUS"][0]
    all_generated_rows = [
        row
        for name, rows in rows_by_name.items()
        if name != "P8_Y5_R2FR_4187_SOURCE_REGISTER"
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    zero_routes = rows_by_name["P8_Y5_R2FR_4187_CGAMMA_ZERO_ROUTE_AUDIT"]
    finite_bounds = rows_by_name["P8_Y5_R2FR_4187_FINITE_CGAMMA_BOUND_INTERFACE"]
    checks = [
        ("VAL4187_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source_register), str(source_register)),
        ("VAL4187_1_source_tokens", "all source tokens found", all(row["required_text_found"] == "True" for row in source_register), str(source_register)),
        ("VAL4187_2_zero_routes", "zero-route audit has at least six routes", len(zero_routes) >= 6, str(len(zero_routes))),
        ("VAL4187_3_projector_contract", "support/projector contract has claim gate", any(row["contract_id"] == "SP4187_8_claim_gate" for row in rows_by_name["P8_Y5_R2FR_4187_MEMORY_SUPPORT_PROJECTOR_CONTRACT"]), "SP4187_8"),
        ("VAL4187_4_cGamma_false", "c_Gamma parent zero remains false", status["c_Gamma_parent_zero"] == "False", str(status)),
        ("VAL4187_5_bound_interface", "finite c_Gamma bound interface ready", status["finite_cGamma_bound_interface_ready"] == "True" and len(finite_bounds) >= 4, str(status)),
        ("VAL4187_6_no_public_claim", "public local GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4187_7_formal_203", "formal 203 exists with marker", FORMAL_203_PATH.exists() and SPINE_MARKER in read_text(FORMAL_203_PATH), str(FORMAL_203_PATH)),
        ("VAL4187_8_checkpoint_doc", "checkpoint doc exists", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4187_9_claim_row", "claim register contains L-028", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4187_10_packet_180", "packet 180 addendum marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4187_11_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4187_12_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
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
            "check_id": "VAL4187_13_py_compile",
            "check": "script compiles and __pycache__ removed",
            "passed": str(not pycache.exists()),
            "detail": str(SCRIPT_PATH),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    ensure_formal_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4187_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4187_CGAMMA_ZERO_ROUTE_AUDIT": zero_route_audit_rows(),
        "P8_Y5_R2FR_4187_MEMORY_SUPPORT_PROJECTOR_CONTRACT": support_projector_contract_rows(),
        "P8_Y5_R2FR_4187_FINITE_CGAMMA_BOUND_INTERFACE": finite_bound_interface_rows(),
        "P8_Y5_R2FR_4187_BRANCH_DECISION": branch_decision_rows(),
        "P8_Y5_R2FR_4187_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4187_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4187_NEXT_TARGET": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(SOURCE_DIR / f"{name}.csv", rows)

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4187_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4187 validation failed: {failed}")

    print(DECISION)
    print(f"formal={FORMAL_203_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
