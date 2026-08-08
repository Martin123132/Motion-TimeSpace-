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

CHECKPOINT = "4196"
BRANCH_ID = "MTS_R2FR_Y5_SCALAR_LEAKAGE_REFERENCE_NULLING_4196"
DECISION = (
    "SCALAR_REFERENCE_NULLING_THEOREM_SHARPENS_ROUTE_STATIONARITY_ALONE_REJECTED_"
    "ZTHETA_ZDOTB_NEED_PARENT_REVERSAL_OR_ENVELOPE_ZLCG_PRUNED_JRES_PROFILE_NEXT"
)
DOC_PATH = POST / "4196-Y5-R2FR-scalar-leakage-reference-nulling-or-Jres-profile-smoke.md"
FORMAL_PATH = FORMAL / "212-PPC4161-scalar-leakage-reference-nulling.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-037"
SPINE_MARKER = "PPC4161_SCALAR_LEAKAGE_REFERENCE_NULLING_4196"
PACKET_MARKER = "PPC4161_PACKET_SCALAR_LEAKAGE_REFERENCE_NULLING_4196"
NEXT_TARGET = "4197-Y5-R2FR-normalized-Jres-profile-smoke-with-4194-budgets.md"

SOURCES = {
    "SRC4196_00_4195_formal": (
        FORMAL / "211-PPC4161-parent-ZL-parity-signature.md",
        "Scalar leakage channels identified in `128-leakage-frame-symmetry.md`",
        "4195 handoff naming scalar leakage reference nulling.",
    ),
    "SRC4196_01_127_coordinates": (
        FORMAL / "127-signed-leakage-coordinate-map.md",
        "z_L^A = {z_theta, z_dotB, z_Bgrad_i, z_grad_i, z_shear_ij, z_rot_ij, z_Lcg}",
        "Signed leakage coordinate bundle.",
    ),
    "SRC4196_02_128_scalar_block": (
        FORMAL / "128-leakage-frame-symmetry.md",
        "true scalar leakage channels can still enter linearly",
        "Earlier proof that O(3) leakage-frame symmetry does not kill scalar channels.",
    ),
    "SRC4196_03_129_stationarity": (
        FORMAL / "129-scalar-channel-stationarity.md",
        "Stationary local backgrounds set scalar channel values near zero, but they do",
        "Earlier rejection of stationarity alone.",
    ),
    "SRC4196_04_130_repair": (
        FORMAL / "130-smooth-scalar-channel-repair.md",
        "Q_theta = z_theta^2 / (1 + z_theta^2)",
        "Clean smooth-quadratic repair, marked as closure not parent-derived.",
    ),
    "SRC4196_05_131_gradient": (
        FORMAL / "131-repaired-local-gradient-power.md",
        "transition shells require one of",
        "Gradient obstruction after scalar repair.",
    ),
    "SRC4196_06_206_stationarity_gate": (
        FORMAL / "206-PPC4161-local-memory-stationarity-gradient-zero-gate.md",
        "no cusp-linear `|z|` terms",
        "Recent stationarity/gradient-zero gate warning.",
    ),
    "SRC4196_07_207_fixed_point": (
        FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md",
        "no |z|, sign(z), free z_Lcg, or tuned L_cg term enters V_Xi",
        "Fixed-point smooth minimizer contract warning.",
    ),
    "SRC4196_08_4195_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4195_NEXT_TARGET.csv",
        "prove scalar leakage reference nulling",
        "4195 machine-readable next target.",
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


def append_unique_line(path: Path, marker: str, line: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if text and not text.endswith("\n"):
            handle.write("\n")
        handle.write(line)


def append_unique_csv_row(path: Path, key_column: str, key_value: str, row: Dict[str, str]) -> None:
    rows = parse_csv(path)
    if any(existing.get(key_column) == key_value for existing in rows):
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writerow(row)


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


def nulling_theorem_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "THM4196_0_stationarity_alone_rejected",
            "f(0,Y)=f_0(Y) or z_scalar=0 on a stationary local background",
            "does_not_imply partial f / partial z_scalar = 0",
            "counterexample f=f_0+a z is smooth, stationary-valued at z=0, and still has a first-order leakage term",
            "rejected_as_derivation",
        ),
        (
            "THM4196_1_reversal_symmetry",
            "parent local branch has an exact reversal/involution R_s: z_s -> -z_s with Y fixed and f(R_s z_s,Y)=f(z_s,Y)",
            "partial f / partial z_s at z_s=0 equals 0",
            "Taylor series contains only even powers in z_s for scalar output f",
            "valid_exact_theorem_if_parent_signed",
        ),
        (
            "THM4196_2_envelope_extremum",
            "z_s is not an observable input but an auxiliary scalar minimized by V_eff(z_s,Y), with partial V_eff/partial z_s=0 and positive Hessian at z_s=z_*(Y)",
            "linear terms vanish for parent-owned minimized action/readout by envelope theorem",
            "works only for quantities descending from the same minimized functional; arbitrary source maps can still be linear",
            "valid_limited_theorem_if_parent_signed",
        ),
        (
            "THM4196_3_smooth_even_source_map",
            "dangerous scalar source maps use Q_s=z_s^2/(1+z_s^2), never |z_s|, sign(z_s), or linear z_s",
            "Q_s=O(z_s^2), so scalar amplitude contribution is quadratic",
            "mathematically clean but a closure unless parent derives Q_s as the source invariant",
            "valid_clean_closure_not_parent_derived",
        ),
        (
            "THM4196_4_Lcg_pruning",
            "z_Lcg is excluded from primitive scalar source variables unless ell_* and ell_norm are parent-derived or an RG/gauge equation makes physical outputs L_cg independent",
            "removes hidden first-order L_cg reference dial",
            "safe hygiene, not a derivation of L_cg",
            "prune_until_parent_reference_or_RG_owned",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "premise": premise,
            "result": result,
            "proof_or_counterexample": proof_or_counterexample,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, premise, result, proof_or_counterexample, status in entries
    ]


def channel_audit_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "CHAN4196_0_z_theta",
            "z_theta",
            "signed scalar expansion/local volume-flow leakage",
            "linear term a_theta z_theta is allowed by spatial symmetry",
            "parent reversal of local equilibrium expansion, envelope extremum, or parent-owned Q_theta",
            "not_parent_signed",
            "keep smooth quadratic Q_theta closure only as private nonclaim or fit finite A_J in 4197",
        ),
        (
            "CHAN4196_1_z_dotB",
            "z_dotB",
            "signed scalar time-derivative/open-memory leakage",
            "linear term a_dotB z_dotB is allowed unless time reversal/equilibrium or auxiliary-flux extremum is signed",
            "parent time-reversal/equilibrium theorem, Onsager-even source invariant, envelope extremum, or parent-owned Q_dotB",
            "not_parent_signed",
            "keep smooth quadratic Q_dotB closure only as private nonclaim or fit finite A_J in 4197",
        ),
        (
            "CHAN4196_2_z_Lcg",
            "z_Lcg",
            "signed scalar coarse-graining scale reference leakage",
            "acts like hidden reference dial if ell_* and ell_norm are chosen by hand",
            "parent-derived ell_* and ell_norm, or RG/gauge independence equation partial f/partial L_cg=0",
            "pruned_not_derived",
            "exclude from primitive scalar source map until parent reference/RG ownership exists",
        ),
        (
            "CHAN4196_3_vector_tensor_bundle",
            "z_Bgrad_i,z_grad_i,z_shear_ij,z_rot_ij",
            "vector/tensor/pseudovector leakage",
            "ordinary leakage-frame symmetry can remove scalar linear contractions when no preferred local vector/tensor exists",
            "same R_L/O(3) parent-equivariance as 4195",
            "conditional_better_than_scalar_channels",
            "not the main 4196 blocker",
        ),
    ]
    return [
        {
            **common(),
            "channel_id": channel_id,
            "channel": channel,
            "channel_type": channel_type,
            "linear_leakage_status": linear_leakage_status,
            "nulling_route_required": nulling_route_required,
            "current_verdict": current_verdict,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for channel_id, channel, channel_type, linear_leakage_status, nulling_route_required, current_verdict, next_action in entries
    ]


def contract_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "CON4196_0_no_stationarity_shortcut",
            "Reject any proof that only shows z_theta=z_dotB=0 on the local background.",
            "must also show zero first derivatives of every scalar output/source map",
            "closed_as_rule",
        ),
        (
            "CON4196_1_parent_reversal",
            "For z_theta/z_dotB, parent must supply a local equilibrium/reversal involution or time-symmetric auxiliary sector.",
            "partial_ztheta f = partial_zdotB f = 0",
            "open",
        ),
        (
            "CON4196_2_envelope_origin",
            "If z_theta/z_dotB are auxiliary minimizer/flux variables, f must descend from the minimized parent functional.",
            "envelope theorem kills linear readout only for functional-owned observables",
            "open",
        ),
        (
            "CON4196_3_no_cusp_linear",
            "Forbid |z|, sign(z), free z_Lcg, or tuned L_cg terms in V_Xi and J_res source maps.",
            "prevents hidden O(U_B) scalar leakage returning under a smooth label",
            "partially_closed_as_firewall",
        ),
        (
            "CON4196_4_Lcg_prune",
            "z_Lcg remains pruned unless parent derives ell_* and ell_norm or RG/gauge independence.",
            "no primitive L_cg scalar leakage source",
            "closed_as_private_hygiene_not_derivation",
        ),
        (
            "CON4196_5_numeric_reality_check",
            "Because parent reversal/envelope signatures are still unsigned, run normalized J_res profile smoke next.",
            "tests whether the clean closure has plausible amplitude against 4194 budgets",
            "next_target",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "contract_clause": contract_clause,
            "required_effect": required_effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, contract_clause, required_effect, status in entries
    ]


def consequence_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "CONS4196_0_if_parent_reversal_signed",
            "z_theta/z_dotB reversal or envelope signed; z_Lcg pruned/RG-owned; no cusp-linear source",
            "scalar source map is O(z_theta^2+z_dotB^2)+no z_Lcg primitive",
            "supports the 4194/4195 nJ=2 bulk route",
            "conditional_not_current_claim",
        ),
        (
            "CONS4196_1_current_corpus",
            "stationarity plus smooth quadratic repair but no parent reversal/envelope signature",
            "clean closure exists, but scalar double-zero is not parent-derived",
            "must not be used as local GR proof",
            "nonclaim",
        ),
        (
            "CONS4196_2_next_empirical_math",
            "take the closure as a private branch and assign A_J, mu_Xi*T_res, L_res/L_loc and boundary amplitudes",
            "normalized J_res profile smoke can decide if the closure is numerically plausible",
            "moves from symbolic loop to amplitude test",
            "recommended_next",
        ),
    ]
    return [
        {
            **common(),
            "consequence_id": consequence_id,
            "condition": condition,
            "result": result,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for consequence_id, condition, result, meaning, status in entries
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "stationarity_alone_rejected": "True",
            "reversal_symmetry_theorem_valid": "True",
            "envelope_theorem_route_valid_limited": "True",
            "ztheta_parent_signed": "False",
            "zdotB_parent_signed": "False",
            "zLcg_pruned": "True",
            "scalar_double_zero_parent_derived": "False",
            "Jres_profile_smoke_recommended_next": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4196_0_no_stationarity_shortcut",
            "Do not treat z_theta=z_dotB=0 on a stationary background as proof of zero linear coefficients.",
        ),
        (
            "FW4196_1_no_parent_reversal_claim",
            "Do not claim z_theta/z_dotB are nulled unless parent reversal/envelope ownership is explicitly signed.",
        ),
        (
            "FW4196_2_no_Lcg_reference_dial",
            "Do not let z_Lcg enter primitive scalar source maps without parent ell_* or RG/gauge independence.",
        ),
        (
            "FW4196_3_no_local_GR_claim",
            "Do not claim local GR/PPN safety from the scalar repair; amplitude and transition/boundary budgets remain active.",
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


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "Derivation-first route now has exact contracts but parent signatures remain unsigned; to avoid symbolic circling, test the clean closure branch against the hard 4194 Gdot/gradient budgets.",
            "inputs_needed": "A_J grid, mu_Xi*T_res grid, L_res/L_loc grid, c_Gamma choices, boundary amplitude cases, strong and weak U_B windows",
            "acceptance_gate": "No pass claim unless rows are numeric, sourced/declared as assumption rows, and all claim flags stay false until parent signatures and source-backed bounds exist.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4196 proves what would null scalar leakage, rejects stationarity alone, prunes z_Lcg, and moves next to a normalized J_res profile smoke because parent reversal/envelope ownership is still unsigned.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_docs() -> None:
    formal = f"""# 212 - PPC4161 Scalar Leakage Reference Nulling

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint attempts the derivation route for scalar leakage reference nulling. It proves the exact contracts that would work, rejects stationarity alone, and records that current parent ownership remains unsigned.

## Failed Shortcut

Stationary local values are not enough.

```text
z_s = 0 at the local background
```

does not imply:

```text
partial f / partial z_s = 0.
```

Counterexample:

```text
f(z_s,Y) = f_0(Y) + a(Y) z_s.
```

This is smooth and has the correct background value at `z_s=0`, but it still contains a first-order scalar leakage source.

## Valid Nulling Routes

### 1. Reversal/Involution Route

If the parent local branch supplies an exact scalar reversal:

```text
R_s: z_s -> -z_s,     R_s Y = Y,
f(R_s z_s,Y)=f(z_s,Y),
```

then Taylor expansion gives:

```text
partial f / partial z_s |_(z_s=0) = 0.
```

This would null `z_theta` and `z_dotB` linears if parent signed the corresponding local equilibrium/time-reversal or auxiliary-flux reversal symmetry.

### 2. Envelope/Extremum Route

If a scalar leakage coordinate is an auxiliary variable minimized by a parent functional:

```text
partial V_eff / partial z_s = 0,
partial^2 V_eff / partial z_s^2 > 0,
```

and the local readout/source descends from that same minimized functional, then the envelope theorem kills the first-order readout. This is valid but limited: arbitrary source maps can still contain linear `z_s` unless they are owned by the same parent functional.

### 3. Smooth-Even Source Route

The clean closure repair remains:

```text
Q_theta = z_theta^2/(1+z_theta^2),
Q_dotB  = z_dotB^2/(1+z_dotB^2).
```

These are smooth and quadratic:

```text
Q_theta = O(z_theta^2),
Q_dotB  = O(z_dotB^2).
```

But until the parent derives these as the actual source invariants, this is closure hygiene rather than parent derivation.

## Channel Verdict

```text
z_theta  -> not parent-signed; needs reversal/envelope/Q_theta ownership
z_dotB   -> not parent-signed; needs time-reversal/equilibrium/envelope/Q_dotB ownership
z_Lcg    -> pruned unless ell_* and ell_norm are parent-derived or RG/gauge independence is proved
```

## Consequence for J_res

If the contracts are signed:

```text
scalar source = O(z_theta^2 + z_dotB^2),
z_Lcg primitive source = absent,
J_res,bulk = O(U_B^2).
```

Current corpus status:

```text
scalar_double_zero_parent_derived = false.
```

So the next useful move is no longer another symbolic restatement. It is a normalized `J_res` profile smoke against the 4194 budgets, unless a parent reversal/envelope theorem is supplied.

## Next Gate

`{NEXT_TARGET}` should test whether the clean private closure branch can plausibly satisfy the hard `Gdot/G` and gradient budgets using explicit assumption grids for `A_J`, `mu_Xi T_res`, `L_res/L_loc`, `c_Gamma`, and boundary amplitude.
"""
    checkpoint = f"""# 4196 - Y5 R2FR Scalar Leakage Reference Nulling Or Jres Profile Smoke

Decision: `{DECISION}`

## Summary

4196 tries to derive scalar leakage reference nulling.

It proves:

```text
stationary background alone is insufficient;
parent reversal/involution is sufficient;
parent envelope/extremum is sufficient only for readouts owned by the minimized functional;
smooth Q_theta/Q_dotB repair is clean but not parent-derived;
z_Lcg must stay pruned unless its reference or RG role is parent-derived.
```

## What Moved

The old scalar-channel problem is now less foggy:

- `z_theta` and `z_dotB` are not killed by ordinary spatial symmetry.
- They can be killed by a parent local reversal/equilibrium theorem or by envelope ownership.
- `z_Lcg` is not a physical primitive source until its reference is derived.
- The clean closure branch is mathematically sane enough to profile numerically, but not claim.

## Next

Run `{NEXT_TARGET}` to stop circling the symbolic obstruction and see whether the private clean-closure branch has plausible amplitude against the 4194 `Gdot/G` and gradient budgets.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def write_register_updates() -> None:
    append_unique_csv_row(
        CLAIMS_PATH,
        "claim_id",
        CLAIM_ID,
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "Scalar leakage reference nulling is derived only under parent reversal/involution or limited envelope-extremum ownership; stationarity alone is rejected, z_Lcg is pruned, and z_theta/z_dotB remain unsigned parent obligations.",
            "current_evidence": "4196 source audit, nulling theorem table, scalar-channel audit, contract ledger, consequence table, decision row and nonclaim firewall.",
            "status": "private_partial_nulling_theorem_nonclaim_parent_reversal_open",
            "next_test": "Run normalized J_res profile smoke against the 4194 budgets, or parent-sign reversal/envelope ownership for z_theta and z_dotB.",
            "key_risk": "Using smooth quadratic scalar repair as if it were parent-derived would hide a closure assumption in the local GR branch.",
        },
    )
    append_unique_line(
        SPINE_PATH,
        SPINE_MARKER,
        f"""

### PPC4161 Scalar Leakage Reference Nulling - 4196

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4196 rejects the stationarity shortcut:

```text
z_s=0 does not imply partial_zs f=0.
```

It proves two valid nulling contracts:

```text
parent reversal/involution -> zero linear scalar coefficient;
parent-owned envelope extremum -> zero first-order minimized-functional readout.
```

Current MTS status remains nonclaim: `z_theta` and `z_dotB` still need parent reversal/envelope ownership, while `z_Lcg` stays pruned unless a parent reference or RG/gauge independence equation is derived. Next target is a normalized `J_res` profile smoke against the 4194 budgets.
""",
    )
    append_unique_line(
        PACKET_180_PATH,
        PACKET_MARKER,
        f"""

## PPC4161 Packet Scalar Leakage Reference Nulling - 4196

Marker: `{PACKET_MARKER}`

Inside the private packet, scalar leakage is now governed by the 4196 rule:

```text
stationarity alone != zero scalar linear coefficient;
R_s or envelope ownership required for z_theta/z_dotB;
z_Lcg pruned unless parent reference/RG ownership is supplied.
```

The private clean-closure branch may use smooth `Q_theta` and `Q_dotB` invariants for profiling, but that is not a local-GR proof until parent ownership and the 4194 amplitude budgets close.
""",
    )


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4196_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4196_NULLING_THEOREM.csv": nulling_theorem_rows(),
        "P8_Y5_R2FR_4196_SCALAR_CHANNEL_AUDIT.csv": channel_audit_rows(),
        "P8_Y5_R2FR_4196_CONTRACT_LEDGER.csv": contract_rows(),
        "P8_Y5_R2FR_4196_JRES_CONSEQUENCE.csv": consequence_rows(),
        "P8_Y5_R2FR_4196_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4196_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4196_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4196_STATUS.csv": status_rows(),
    }


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4196_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4196_NULLING_THEOREM.csv"]
    channels = rows_by_file["P8_Y5_R2FR_4196_SCALAR_CHANNEL_AUDIT.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4196_DECISION.csv"][0]
    firewall = rows_by_file["P8_Y5_R2FR_4196_CLAIM_FIREWALL.csv"]

    checks = [
        (
            "VAL4196_0_sources_exist",
            "all source paths exist",
            all(row["exists"] == "True" for row in source),
        ),
        (
            "VAL4196_1_source_tokens",
            "all source required text markers found",
            all(row["required_text_found"] == "True" for row in source),
        ),
        (
            "VAL4196_2_stationarity_rejected",
            "stationarity-alone shortcut is explicitly rejected",
            any(row["theorem_id"] == "THM4196_0_stationarity_alone_rejected" and row["status"] == "rejected_as_derivation" for row in theorem),
        ),
        (
            "VAL4196_3_valid_nulling_routes",
            "reversal and envelope routes recorded",
            {"THM4196_1_reversal_symmetry", "THM4196_2_envelope_extremum"}.issubset({row["theorem_id"] for row in theorem}),
        ),
        (
            "VAL4196_4_scalar_channels_audited",
            "z_theta, z_dotB and z_Lcg audited",
            {"z_theta", "z_dotB", "z_Lcg"}.issubset({row["channel"] for row in channels}),
        ),
        (
            "VAL4196_5_zLcg_pruned",
            "z_Lcg is pruned, not derived",
            any(row["channel"] == "z_Lcg" and row["current_verdict"] == "pruned_not_derived" for row in channels),
        ),
        (
            "VAL4196_6_parent_not_derived",
            "scalar double-zero remains not parent-derived",
            decision["scalar_double_zero_parent_derived"] == "False"
            and decision["ztheta_parent_signed"] == "False"
            and decision["zdotB_parent_signed"] == "False",
        ),
        (
            "VAL4196_7_next_smoke",
            "Jres profile smoke recommended next",
            decision["Jres_profile_smoke_recommended_next"] == "True"
            and NEXT_TARGET in rows_by_file["P8_Y5_R2FR_4196_NEXT_TARGET.csv"][0]["next_target"],
        ),
        (
            "VAL4196_8_no_claim_flags",
            "no 4196 row has claim_allowed or valid_for_claim true",
            all(
                row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False"
                for table in rows_by_file.values()
                for row in table
            ),
        ),
        (
            "VAL4196_9_firewall_rows",
            "firewall contains four anti-smuggling rules",
            len(firewall) == 4,
        ),
        (
            "VAL4196_10_docs_written",
            "formal and checkpoint docs contain decision marker",
            DECISION in read_text(FORMAL_PATH) and DECISION in read_text(DOC_PATH),
        ),
        (
            "VAL4196_11_claim_register",
            "claim register has L-037",
            CLAIM_ID in read_text(CLAIMS_PATH),
        ),
        (
            "VAL4196_12_spine_marker",
            "spine marker appended",
            SPINE_MARKER in read_text(SPINE_PATH),
        ),
        (
            "VAL4196_13_packet_marker",
            "packet marker appended",
            PACKET_MARKER in read_text(PACKET_180_PATH),
        ),
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
    write_docs()
    write_register_updates()
    rows_by_file = all_rows()
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4196_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4196 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4196_VALIDATION.csv'}")
    print("rows=14 validation checks")


if __name__ == "__main__":
    main()
