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

CHECKPOINT = "4191"
BRANCH_ID = "MTS_R2FR_Y5_MEMORY_FIXED_POINT_MINIMIZER_CONTRACT_4191"
DECISION = (
    "MEMORY_FIXED_POINT_NORMAL_FORM_AND_SMOOTH_MINIMIZER_THEOREM_WRITTEN_"
    "PARENT_SIGNATURE_UNSIGNED_PROFILE_BOUNDS_REMAIN_ACTIVE_NONCLAIM"
)
DOC_PATH = POST / "4191-Y5-R2FR-memory-fixed-point-equation-and-smooth-minimizer-contract.md"
FORMAL_207_PATH = FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-032"
SPINE_MARKER = "PPC4161_MEMORY_FIXED_POINT_SMOOTH_MINIMIZER_4191"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_FIXED_POINT_SMOOTH_MINIMIZER_4191"
NEXT_TARGET = "4192-Y5-R2FR-parent-Xi-Hessian-signs-and-boundary-domain-or-profile-fill.md"

SOURCES = {
    "SRC4191_00_4190_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4190_NEXT_TARGET.csv",
        "fixed-point equation and smooth-minimizer contract",
        "4190 handoff selecting the fixed-point/minimizer target.",
    ),
    "SRC4191_01_4190_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4190_STATIONARITY_CONTRACT.csv",
        "E_Xi[Xi_0; local invariants]=0",
        "4190 stationarity contract.",
    ),
    "SRC4191_02_4190_lemma": (
        SOURCE_DIR / "P8_Y5_R2FR_4190_LEMMA_ATTEMPT.csv",
        "smooth unique fixed point",
        "4190 conditional zero lemma attempt.",
    ),
    "SRC4191_03_4190_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4190_DTXI_GRADXI_PROFILE_BOUNDS.csv",
        "2.42e-14 / |c_Gamma|",
        "4190 finite fallback profile bounds.",
    ),
    "SRC4191_04_fixed_point_79": (
        FORMAL / "79-local-fixed-point-mechanism.md",
        "local_fixed_point_mechanism_conditional_closure_not_parent_derived",
        "older local fixed-point mechanism audit.",
    ),
    "SRC4191_05_parent_DL_122": (
        FORMAL / "122-parent-DL-fixed-point-silence.md",
        "parent_DL_fixed_point_silence_partial_F1_only",
        "parent D_L fixed-point silence gate.",
    ),
    "SRC4191_06_extremality_124": (
        FORMAL / "124-fixed-point-extremality-origin.md",
        "fixed_point_extremality_origin_best_route_ZL_not_parent_derived",
        "fixed-point extremality origin gate.",
    ),
    "SRC4191_07_scalar_129": (
        FORMAL / "129-scalar-channel-stationarity.md",
        "scalar_channel_stationarity_not_parent_derived_zLcg_pruned_repair_required",
        "scalar-channel stationarity blocker.",
    ),
    "SRC4191_08_smooth_130": (
        FORMAL / "130-smooth-scalar-channel-repair.md",
        "smooth_scalar_channel_repair_clean_closure_not_parent_derived_gradients_open",
        "smooth scalar repair precedent.",
    ),
    "SRC4191_09_formal_206": (
        FORMAL / "206-PPC4161-local-memory-stationarity-gradient-zero-gate.md",
        "E_Xi[Xi_0; local invariants] = 0",
        "formal 4190 target document.",
    ),
    "SRC4191_10_equation_register": (
        FORMAL / "05-equation-register.md",
        "grad m -> 0",
        "equation register local equilibrium target.",
    ),
    "SRC4191_11_spine": (
        FORMAL / "07-unification-spine.md",
        "PPC4161_LOCAL_MEMORY_STATIONARITY_GRADIENT_ZERO_GATE_4190",
        "current spine marker for the 4190 handoff.",
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


def fixed_point_normal_form_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "NF4191_0_memory_projection",
            "Xi_0 := N_0[P_loc Gamma_mem]",
            "scalar memory projection feeding Gdot and preferred-location channels",
            "dimensionless or parent-normalized scalar",
            "defined by 4190, parent operator normalization still needs final action ownership",
            "sets the variable whose local fixed point must be derived",
        ),
        (
            "NF4191_1_action",
            "S_Xi[Xi_0; I_loc] = integral_U sqrt(-g_obs)[-1/2 Z_Xi h^ab nabla_a Xi_0 nabla_b Xi_0 - V_Xi(Xi_0; I_loc)] + S_boundary",
            "minimal local memory action normal form",
            "action density",
            "candidate parent normal form, not yet signed by parent corpus",
            "gives an Euler-Lagrange equation instead of a plateau axiom",
        ),
        (
            "NF4191_2_euler_lagrange",
            "E_Xi := -nabla_a(Z_Xi h^ab nabla_b Xi_0) + partial_Xi V_Xi(Xi_0; I_loc) = 0",
            "fixed-point equation to replace assumed local stationarity",
            "field equation",
            "conditional theorem target",
            "if solved by a unique smooth minimizer, local derivative zeros follow from source derivative zeros",
        ),
        (
            "NF4191_3_quadratic_minimum",
            "V_Xi = 1/2 M_Xi^2 [Xi_0 - Xi_star(I_loc)]^2 + O([Xi_0 - Xi_star]^3)",
            "smooth local minimum expansion",
            "potential density",
            "M_Xi^2 positivity and higher-order smoothness unsigned",
            "forbids the old cusp-linear |z| source leak if parent smoothness is proved",
        ),
        (
            "NF4191_4_fixed_point_map",
            "Xi_0 = Xi_star(I_loc) when boundary data and local invariants are stationary/homogeneous",
            "local fixed-point readout",
            "map from local invariants to scalar memory projection",
            "smooth map unsigned",
            "turns stationarity of inputs into D_t Xi_0=0 and grad_perp Xi_0=0",
        ),
        (
            "NF4191_5_boundary_domain",
            "self-adjoint local domain with no memory-flux boundary source and boundary Xi_0=Xi_star(I_loc) or natural no-flux minimizer data",
            "domain condition",
            "boundary condition",
            "unsigned",
            "prevents hiding a residual local force in the boundary term",
        ),
    ]
    return [
        {
            **common(),
            "normal_form_id": normal_form_id,
            "expression": expression,
            "role": role,
            "units_or_type": units_or_type,
            "parent_status": parent_status,
            "implication": implication,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for normal_form_id, expression, role, units_or_type, parent_status, implication in entries
    ]


def smooth_minimizer_theorem_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "THM4191_0_hypothesis_action",
            "Assume S_Xi has the NF4191_1 normal form on a compact local test collar U.",
            "hypothesis",
            "needed",
            "not parent-signed",
        ),
        (
            "THM4191_1_coercive_operator",
            "If Z_Xi>0 and the boundary/domain is self-adjoint, the gradient part is coercive up to the allowed zero mode.",
            "mathematical condition",
            "standard variational implication",
            "Z_Xi and domain unsigned",
        ),
        (
            "THM4191_2_strict_local_minimum",
            "If M_Xi^2>0 and V_Xi is C^2 near Xi_star, the local branch has a unique smooth minimizer Xi_0=Xi_star(I_loc).",
            "mathematical condition",
            "implicit-function/minimizer theorem route",
            "M_Xi^2 and smooth Xi_star unsigned",
        ),
        (
            "THM4191_3_time_derivative",
            "D_t Xi_0 = (partial_A Xi_star) D_t I_loc^A; therefore stationary local invariants imply D_t Xi_0=0.",
            "derived conditional consequence",
            "proves the Gdot channel zero only if source stationarity is parent-owned",
            "stationary invariants unsigned",
        ),
        (
            "THM4191_4_transverse_gradient",
            "grad_perp Xi_0 = (partial_A Xi_star) grad_perp I_loc^A; therefore homogeneous/projected local invariants imply grad_perp Xi_0=0.",
            "derived conditional consequence",
            "proves the preferred-location channel zero only if projector/source-gradient silence is parent-owned",
            "homogeneous projection unsigned",
        ),
        (
            "THM4191_5_cusp_rejection",
            "A linear |z| term is not C^1 at z=0 and cannot appear in this smooth minimizer theorem.",
            "derived regularity filter",
            "rejects the old cusp route unless replaced by smooth quadratic invariants",
            "smoothness still needs parent origin",
        ),
        (
            "THM4191_6_conditional_result",
            "All hypotheses together imply D_t Xi_0=0 and grad_perp Xi_0=0 without a plateau axiom.",
            "conditional theorem",
            "the desired local zero law is mathematically available",
            "parent signature incomplete, so no local-GR claim",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "statement": statement,
            "role": role,
            "math_status": math_status,
            "parent_status": parent_status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, statement, role, math_status, parent_status in entries
    ]


def parent_signature_audit_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "SIG4191_0_parent_equation",
            "parent-owned E_Xi[Xi_0; I_loc]=0",
            "4190 states the target; no full parent memory action yet",
            "unsigned",
            "derive from parent action/coarse-graining or keep finite-profile branch",
        ),
        (
            "SIG4191_1_positive_Z_Xi",
            "Z_Xi>0",
            "no source-owned kinetic sign row currently exists for Xi_0",
            "missing_parent_input",
            "derive Hessian/kinetic sign from parent memory sector",
        ),
        (
            "SIG4191_2_positive_M_Xi2",
            "M_Xi^2>0 at Xi_star",
            "older R-lock gives partial F1 style stationarity but not this Xi Hessian",
            "missing_parent_input",
            "derive local Hessian or bounded profile values",
        ),
        (
            "SIG4191_3_smooth_Xi_star",
            "Xi_star(I_loc) is C^1/C^2 in local invariants",
            "130 gives a clean smooth closure repair, not parent derivation",
            "closure_only",
            "source smoothness from action or demote to explicit closure",
        ),
        (
            "SIG4191_4_no_cusp_terms",
            "no |z|, sign(z), free z_Lcg, or sector-tuned L_cg term enters V_Xi",
            "129 prunes z_Lcg and flags cusp terms; not parent-derived",
            "pruned_not_derived",
            "prove smooth-even invariant source map",
        ),
        (
            "SIG4191_5_boundary_domain",
            "self-adjoint local domain and no memory-flux boundary source",
            "203-206 define support/projector needs; no complete boundary theorem",
            "missing_boundary_theorem",
            "derive local no-flux/Hamiltonian boundary routing",
        ),
        (
            "SIG4191_6_stationary_local_invariants",
            "D_t I_loc^A=0 along the compact local readout",
            "206 says this is needed; local systems may be stationary approximately but not parent-proved",
            "arena_projection_open",
            "derive local invariant stationarity or fill D_t Xi_0 profile",
        ),
        (
            "SIG4191_7_homogeneous_projection",
            "P_loc kills grad_perp I_loc^A or bounds it",
            "4190 computes the fallback bound but not a projector-zero proof",
            "arena_projection_open",
            "derive projector/source-gradient silence or fill grad_perp Xi_0 profile",
        ),
        (
            "SIG4191_8_current_verdict",
            "parent signature sufficient for exact zero",
            "at least seven clauses above remain unsigned or closure-only",
            "false",
            "do not claim local GR; attack Hessian/domain signs next",
        ),
    ]
    return [
        {
            **common(),
            "signature_id": signature_id,
            "required_parent_clause": required_parent_clause,
            "current_evidence": current_evidence,
            "status": status,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for signature_id, required_parent_clause, current_evidence, status, next_action in entries
    ]


def stationarity_implication_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "IMP4191_0_exact_zero_branch",
            "If SIG4191_0 through SIG4191_7 are all parent-signed, then D_t Xi_0=0 and grad_perp Xi_0=0.",
            "exact local scalar-memory silence",
            "not currently active",
        ),
        (
            "IMP4191_1_Gdot_channel",
            "C_Gamma_Gdot = c_Gamma D_t Xi_0, so exact D_t Xi_0=0 kills this residual.",
            "local Gdot safety",
            "conditional only",
        ),
        (
            "IMP4191_2_preferred_location_channel",
            "C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|, so exact grad_perp Xi_0=0 kills this residual.",
            "preferred-location metric safety",
            "conditional only",
        ),
        (
            "IMP4191_3_current_branch",
            "Because the parent signature is unsigned, the 4190 finite profile bounds remain the operative local branch.",
            "nonclaim fallback",
            "active",
        ),
    ]
    return [
        {
            **common(),
            "implication_id": implication_id,
            "statement": statement,
            "effect": effect,
            "current_status": current_status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for implication_id, statement, effect, current_status in entries
    ]


def fallback_profile_bound_link_rows() -> List[Dict[str, str]]:
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4190_DTXI_GRADXI_PROFILE_BOUNDS.csv"
    source_rows_4190 = parse_csv(source_path)
    selected_rows = [
        source_row
        for source_row in source_rows_4190
        if source_row.get("bound_id") in {
            "DTXI4190_cGamma_1e+00",
            "GRADXI4190_cGamma_1e+00",
            "SYMBOLIC4190_DTXI",
            "SYMBOLIC4190_GRADXI",
        }
    ]
    rows: List[Dict[str, str]] = []
    for source_row in selected_rows:
        rows.append(
            {
                **common(),
                "link_id": f"LINK4191_{source_row['bound_id']}",
                "source_bound_id": source_row["bound_id"],
                "source_path": str(source_path),
                "channel": source_row["channel"],
                "assumed_abs_cGamma": source_row["assumed_abs_cGamma"],
                "required_abs_profile_bound": source_row["required_abs_profile_bound"],
                "units": source_row["units"],
                "current_role": "fallback bound remains active because 4191 parent minimizer signature is unsigned",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "normal_form_written": "True",
            "conditional_minimizer_theorem_written": "True",
            "exact_zero_lemma_closed": "False",
            "parent_signature_complete": "False",
            "finite_profile_bounds_remain_active": "True",
            "public_local_GR_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4191_0_no_plateau_axiom",
            "Do not replace the fixed-point theorem with an asserted local-vacuum plateau.",
        ),
        (
            "FW4191_1_no_public_local_GR",
            "Do not claim local GR/Newton/PPN recovery from 4191; the theorem is conditional and parent signature is incomplete.",
        ),
        (
            "FW4191_2_no_hidden_Lcg_tuning",
            "Do not reintroduce z_Lcg or a sector-tuned L_cg reference inside Xi_star.",
        ),
        (
            "FW4191_3_no_bound_to_zero_swap",
            "Do not treat the finite 4190 profile bounds as proof of exact D_t Xi_0=0 or grad_perp Xi_0=0.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in entries
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    audit_rows = parent_signature_audit_rows()
    unsigned_count = len(
        [
            audit_row
            for audit_row in audit_rows
            if audit_row["status"] not in {"signed", "derived", "filled"}
        ]
    )
    return [
        {
            **common(),
            "decision": DECISION,
            "normal_form_written": "True",
            "smooth_minimizer_conditional_theorem_available": "True",
            "parent_signed": "False",
            "unsigned_parent_clause_count": str(unsigned_count),
            "exact_zero_lemma_closed": "False",
            "finite_profile_bounds_remain_active": "True",
            "public_local_GR_claim_allowed": "False",
            "formal_207_written": str(FORMAL_207_PATH.exists()),
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
            "why": "4191 gives the exact smooth-minimizer theorem, but the parent action still has to sign Z_Xi, M_Xi^2, Xi_star smoothness and the local boundary/domain.",
            "route_A": "derive Z_Xi>0, M_Xi^2>0, smooth Xi_star(I_loc), and self-adjoint/no-flux local domain from the parent action",
            "route_B": "fill bounded D_t Xi_0 and grad_perp Xi_0 profiles against the 4190 finite bounds",
            "recommended_first": "parent Xi Hessian signs and boundary/domain",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc_text() -> str:
    return f"""# 207 - PPC4161 Memory Fixed-Point Equation And Smooth-Minimizer Contract

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, PPN safety, clock safety, orbital safety, R10 safety, or exact scalar-memory silence. It constructs the exact theorem form that would prove the desired local zeros if the parent action signs the missing clauses.

## Target Variable

```text
Xi_0 := N_0[P_loc Gamma_mem].
```

4190 showed that the dangerous local residuals reduce to:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0
C_Gamma_xi   = c_Gamma L_loc |grad_perp Xi_0|.
```

So the derivation target is:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0.
```

## Parent Normal Form

The least-smuggled parent route is not a plateau axiom. It is a local memory action:

```text
S_Xi[Xi_0; I_loc]
  = integral_U sqrt(-g_obs)[
      -1/2 Z_Xi h^ab nabla_a Xi_0 nabla_b Xi_0
      - V_Xi(Xi_0; I_loc)
    ] + S_boundary.
```

The fixed-point equation is:

```text
E_Xi := -nabla_a(Z_Xi h^ab nabla_b Xi_0)
        + partial_Xi V_Xi(Xi_0; I_loc)
        = 0.
```

The smooth-minimizer branch requires:

```text
V_Xi = 1/2 M_Xi^2 [Xi_0 - Xi_star(I_loc)]^2
       + O([Xi_0 - Xi_star]^3),

Z_Xi > 0,
M_Xi^2 > 0.
```

## Conditional Theorem

If:

```text
1. the parent action supplies the normal form above;
2. Z_Xi > 0 and the local boundary/domain is self-adjoint/no-flux;
3. M_Xi^2 > 0 and Xi_star(I_loc) is smooth;
4. no |z|, sign(z), free z_Lcg, or tuned L_cg term enters V_Xi;
5. local invariants are stationary and homogeneous after P_loc;
```

then the local solution is the smooth fixed point:

```text
Xi_0 = Xi_star(I_loc).
```

By the chain rule:

```text
D_t Xi_0       = (partial_A Xi_star) D_t I_loc^A,
grad_perp Xi_0 = (partial_A Xi_star) grad_perp I_loc^A.
```

Thus stationary and projected-homogeneous local invariants imply:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0.
```

That is a real derivation route. It is not yet a completed derivation because the parent signature is unsigned.

## Current Parent Signature

Current status:

```text
parent_signed = false
exact_zero_lemma_closed = false
finite_profile_bounds_remain_active = true
```

Unsigned clauses:

```text
Z_Xi > 0,
M_Xi^2 > 0,
smooth Xi_star(I_loc),
self-adjoint/no-flux local boundary domain,
stationary local invariants,
homogeneous/projected transverse source gradients.
```

## Fallback Bound Branch

Until those clauses are derived, the operative local branch remains the 4190 profile-bound fork:

```text
|D_t Xi_0| <= 2.42e-14 / |c_Gamma| yr^-1
|L_loc grad_perp Xi_0| <= 4e-9 / |c_Gamma|.
```

## Next Gate

`{NEXT_TARGET}` should attack parent Hessian/kinetic signs and the boundary/domain, or else fill finite profile values.
"""


def checkpoint_doc_text() -> str:
    return f"""# 4191 - Memory Fixed-Point Equation And Smooth-Minimizer Contract

Generated by: `post-checkpoint-work/scripts/Y5_R2FR_4191_memory_fixed_point_equation_and_smooth_minimizer_contract.py`

## Summary

4191 tries the derivation route rather than circling the obstruction. It writes the exact local memory action normal form and proves the conditional smooth-minimizer theorem that would give:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0.
```

## Result

The theorem route is mathematically clean:

```text
S_Xi -> E_Xi=0 -> Xi_0=Xi_star(I_loc) -> D_t Xi_0=0 and grad_perp Xi_0=0
```

if the parent action signs `Z_Xi>0`, `M_Xi^2>0`, smooth `Xi_star`, local no-flux/self-adjoint boundary data, and stationary/projected homogeneous local invariants.

Current corpus does not yet sign those clauses, so the exact local zero is **not** claimed.

## Active Fallback

The 4190 finite branch remains active:

```text
|D_t Xi_0| <= 2.42e-14 / |c_Gamma| yr^-1
|L_loc grad_perp Xi_0| <= 4e-9 / |c_Gamma|
```

## Decision

`{DECISION}`
"""


def ensure_docs() -> None:
    FORMAL_207_PATH.write_text(formal_doc_text(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc_text(), encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The local scalar-memory zero route has an explicit parent fixed-point/minimizer normal form and a conditional theorem, but the parent signature is not complete.",
            "current_evidence": "4191 normal-form ledger, smooth-minimizer theorem, parent-signature audit, fallback profile-bound link and nonclaim firewall.",
            "status": "private_conditional_minimizer_theorem_nonclaim_parent_signature_unsigned_profile_bounds_active",
            "next_test": "Derive Z_Xi>0, M_Xi^2>0, smooth Xi_star and local no-flux/self-adjoint boundary domain, or fill D_t Xi_0 and grad_perp Xi_0 profiles.",
            "key_risk": "Treating a clean conditional minimizer theorem as parent derivation would smuggle the remaining Hessian, boundary and source-projection clauses.",
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "appended"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4191 Memory Fixed-Point Smooth-Minimizer Contract

Marker: `{PACKET_MARKER}`

4191 constructs the exact theorem route for the local scalar memory projection:

```text
S_Xi[Xi_0; I_loc] -> E_Xi=0 -> Xi_0=Xi_star(I_loc).
```

If the parent signs `Z_Xi>0`, `M_Xi^2>0`, smooth `Xi_star`, no-flux/self-adjoint boundary data, and stationary/projected homogeneous local invariants, then:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0.
```

The parent signature is still unsigned, so the 4190 finite profile bounds remain active.
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "appended"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Memory Fixed-Point Smooth-Minimizer Contract

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4191 converts the 4190 local scalar-memory zero target into a concrete parent-action theorem:

```text
S_Xi[Xi_0; I_loc]
  = integral_U sqrt(-g_obs)[-1/2 Z_Xi h^ab nabla_a Xi_0 nabla_b Xi_0
    - V_Xi(Xi_0; I_loc)] + S_boundary,

E_Xi = 0,
V_Xi = 1/2 M_Xi^2 [Xi_0 - Xi_star(I_loc)]^2 + higher order.
```

If the parent signs positive `Z_Xi`, positive `M_Xi^2`, smooth `Xi_star`, and no-flux/self-adjoint local domain with stationary/projected homogeneous local invariants, then:

```text
D_t Xi_0 = 0 and grad_perp Xi_0 = 0.
```

Current verdict: theorem route constructed, parent signature unsigned, exact local-GR branch not claimed, 4190 finite profile bounds remain active.
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "appended"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source_register = rows_by_name["P8_Y5_R2FR_4191_SOURCE_REGISTER"]
    normal_form = rows_by_name["P8_Y5_R2FR_4191_FIXED_POINT_NORMAL_FORM"]
    theorem = rows_by_name["P8_Y5_R2FR_4191_SMOOTH_MINIMIZER_THEOREM"]
    audit = rows_by_name["P8_Y5_R2FR_4191_PARENT_SIGNATURE_AUDIT"]
    fallback = rows_by_name["P8_Y5_R2FR_4191_FALLBACK_PROFILE_BOUND_LINK"]
    status = rows_by_name["P8_Y5_R2FR_4191_STATUS"][0]
    all_generated_rows = [
        row
        for name, rows in rows_by_name.items()
        if name != "P8_Y5_R2FR_4191_SOURCE_REGISTER"
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4191_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source_register), str(source_register)),
        ("VAL4191_1_source_tokens", "all source tokens found", all(row["required_text_found"] == "True" for row in source_register), str(source_register)),
        ("VAL4191_2_normal_form_action", "normal form includes action and E_Xi", any("S_Xi" in row["expression"] for row in normal_form) and any("E_Xi" in row["expression"] for row in normal_form), str(normal_form)),
        ("VAL4191_3_minimizer_theorem", "conditional minimizer theorem includes both zeros", any("D_t Xi_0=0" in row["statement"] for row in theorem) and any("grad_perp Xi_0=0" in row["statement"] for row in theorem), str(theorem)),
        ("VAL4191_4_parent_unsigned", "parent signature remains unsigned", status["parent_signed"] == "False" and any(row["status"] in {"missing_parent_input", "closure_only", "missing_boundary_theorem", "arena_projection_open"} for row in audit), str(audit)),
        ("VAL4191_5_profile_fallback", "4190 fallback profile bounds linked", len(fallback) >= 4 and any("2.42e-14" in row["required_abs_profile_bound"] for row in fallback) and any("4e-9" in row["required_abs_profile_bound"] for row in fallback), str(fallback)),
        ("VAL4191_6_no_public_claim", "public local GR claim remains false", status["public_local_GR_claim_allowed"] == "False" and status["exact_zero_lemma_closed"] == "False", str(status)),
        ("VAL4191_7_formal_207", "formal 207 exists with marker", FORMAL_207_PATH.exists() and SPINE_MARKER in read_text(FORMAL_207_PATH), str(FORMAL_207_PATH)),
        ("VAL4191_8_checkpoint_doc", "checkpoint doc exists with decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4191_9_claim_row", "claim register contains L-032", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4191_10_packet_180", "packet marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4191_11_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4191_12_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
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
            "check_id": "VAL4191_13_py_compile",
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
        "P8_Y5_R2FR_4191_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4191_FIXED_POINT_NORMAL_FORM": fixed_point_normal_form_rows(),
        "P8_Y5_R2FR_4191_SMOOTH_MINIMIZER_THEOREM": smooth_minimizer_theorem_rows(),
        "P8_Y5_R2FR_4191_PARENT_SIGNATURE_AUDIT": parent_signature_audit_rows(),
        "P8_Y5_R2FR_4191_STATIONARITY_IMPLICATIONS": stationarity_implication_rows(),
        "P8_Y5_R2FR_4191_FALLBACK_PROFILE_BOUND_LINK": fallback_profile_bound_link_rows(),
        "P8_Y5_R2FR_4191_DECISION": decision_rows(),
        "P8_Y5_R2FR_4191_CLAIM_FIREWALL": claim_firewall_rows(),
        "P8_Y5_R2FR_4191_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4191_NEXT_TARGET": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(SOURCE_DIR / f"{name}.csv", rows)

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4191_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4191 validation failed: {failed}")

    print(DECISION)
    print(f"formal={FORMAL_207_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
