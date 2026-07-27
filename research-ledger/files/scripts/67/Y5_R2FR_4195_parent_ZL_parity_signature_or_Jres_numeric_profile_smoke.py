from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4195"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ZL_PARITY_SIGNATURE_4195"
DECISION = (
    "ZL_PARITY_EVENNESS_LEMMA_PROVED_UNDER_LEAKAGE_INVOLUTION_"
    "PARENT_OWNERSHIP_OPEN_JRES_POWER_REMAINS_CONDITIONAL"
)
DOC_PATH = POST / "4195-Y5-R2FR-parent-ZL-parity-signature-or-Jres-numeric-profile-smoke.md"
FORMAL_PATH = FORMAL / "211-PPC4161-parent-ZL-parity-signature.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-036"
SPINE_MARKER = "PPC4161_PARENT_ZL_PARITY_SIGNATURE_4195"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ZL_PARITY_SIGNATURE_4195"
NEXT_TARGET = "4196-Y5-R2FR-scalar-leakage-reference-nulling-or-Jres-profile-smoke.md"

SOURCES = {
    "SRC4195_00_4194_formal": (
        FORMAL / "210-PPC4161-source-support-powers-for-Jres.md",
        "nJ = 2",
        "4194 conditional J_res source-support power target.",
    ),
    "SRC4195_01_4194_parent_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4194_PARENT_SIGNATURE_AUDIT.csv",
        "PSIG4194_2_scalar_evenness",
        "4194 parent-signature audit rows.",
    ),
    "SRC4195_02_123_source_power": (
        FORMAL / "123-local-source-power-theorem.md",
        "local_source_power_theorem_form_constructed_not_parent_derived",
        "Earlier source-power theorem form.",
    ),
    "SRC4195_03_125_ZL": (
        FORMAL / "125-local-leakage-vector-invariant.md",
        "Z_L^A",
        "Candidate signed leakage vector and finite-margin bound.",
    ),
    "SRC4195_04_126_evenness": (
        FORMAL / "126-scalar-evenness-origin.md",
        "scalar_evenness_origin_parity_candidate_not_parent_derived",
        "Scalar evenness/parity origin gate.",
    ),
    "SRC4195_05_128_symmetry": (
        FORMAL / "128-leakage-frame-symmetry.md",
        "true scalar leakage channels can still enter linearly",
        "Leakage-frame symmetry warning: scalar channels are not killed by ordinary rotations alone.",
    ),
    "SRC4195_06_131_gradient": (
        FORMAL / "131-repaired-local-gradient-power.md",
        "repaired_local_gradient_power_far_local_conditional_transition_shell_open",
        "Far-local gradient-power conditional gate.",
    ),
    "SRC4195_07_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "LOCAL_BOUNDARY_NO_FLUX_THEOREM_CLOSES_TRANSITION_CURRENT_PRIVATE_SELECTOR",
        "Boundary/no-flux selector precedent.",
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


def lemma_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "LEM4195_0_signed_coordinate",
            "Choose a signed local leakage coordinate z_L^A with z_L=0 on the compact local GR leaf.",
            "If the coarse-graining map admits z_L^A = U_B H_L^A(Y) with bounded H_L, then D_L=sqrt(G_AB z_L^A z_L^B)<=C_D U_B.",
            "conditional_existing_candidate",
            "125 supplies a non-cheating candidate, but H_L boundedness is not parent-signed.",
        ),
        (
            "LEM4195_1_leakage_involution",
            "Postulate or derive an involution R_L: z_L^A -> -z_L^A that fixes quotient/local observables Y.",
            "R_L makes leakage sign a representative label rather than a new scalar observable.",
            "exact_if_parent_symmetry_exists",
            "Current corpus does not yet prove parent action, measure and coarse-graining are R_L equivariant.",
        ),
        (
            "LEM4195_2_scalar_evenness",
            "If scalar local data descend through R_L-even invariants, m_L(R_L z,Y)=m_L(z,Y).",
            "C2 Taylor expansion gives partial_A m_L(0,Y)=0 and m_L=m_0(Y)+1/2 H_AB(Y)z^A z^B+O(|z|^3).",
            "lemma_proved_under_involution",
            "128 warns true scalar leakage channels can enter linearly unless this descent is parent-owned.",
        ),
        (
            "LEM4195_3_source_parity",
            "If the projected residual source is R_L-odd/covariant, S_cg(R_L z,Y)=-S_cg(z,Y), or support-silent.",
            "Then S_cg(0,Y)=0 and smoothness gives ||S_cg||<=C_S D_L, so U_B S_cg=O(U_B^2).",
            "lemma_proved_under_source_covariance",
            "Current corpus has theorem shape, not the parent source operator transformation law.",
        ),
        (
            "LEM4195_4_gradient_preservation",
            "If z_L=U_B H_L(Y), H_L and log-gradients are bounded far from transition shells.",
            "D_t m_L=O(U_B^2/T_B) and Delta_h m_L=O(U_B^2/L_B^2).",
            "far_local_conditional",
            "131 leaves transition shells open; 4195 does not close them.",
        ),
        (
            "LEM4195_5_boundary_routing",
            "If the local collar has no-flux/support separation or Hamiltonian boundary routing.",
            "boundary_in=0/routed or at worst an explicit boundary-charge row, not a hidden bulk source.",
            "private_selector_conditional",
            "192 closes this only inside the private selector branch.",
        ),
    ]
    return [
        {
            **common(),
            "lemma_id": lemma_id,
            "input_clause": input_clause,
            "result": result,
            "status": status,
            "limitation": limitation,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for lemma_id, input_clause, result, status, limitation in entries
    ]


def parent_signature_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "SIG4195_0_parent_action",
            "S_parent[Phi]=S_parent[R_L Phi]",
            "missing",
            "needed to stop parity from being an imposed closure",
            "derive R_L as a gauge/redundancy of the motion-frame/coarse-graining variables",
        ),
        (
            "SIG4195_1_measure_connection",
            "measure, coframe, connection and projector commute with R_L",
            "missing",
            "otherwise odd/even power counting can be broken by the projection machinery",
            "audit PPC4161 packet for R_L equivariance of each map",
        ),
        (
            "SIG4195_2_scalar_descent",
            "m_L and Xi_star descend through even invariants such as s_L=G_AB z^A z^B",
            "partly_theorem_shaped",
            "the scalar linear channel is the main leak identified by 128",
            "prove scalar reference nulling or environmental extremum from parent variation",
        ),
        (
            "SIG4195_3_source_covariance",
            "P_loc S_cg is R_L-odd/covariant or support-silent",
            "not_signed",
            "needed for S_cg=O(D_L) instead of O(1)",
            "derive projected source transformation from the same Hilbert/current operator used in local GR branch",
        ),
        (
            "SIG4195_4_HL_bound",
            "H_L bounded and denominator floors are nonzero on the compact tested local domain",
            "candidate",
            "needed for D_L<=C_D U_B",
            "turn compact-domain and denominator-floor clauses into parent/source conditions",
        ),
        (
            "SIG4195_5_transition_boundary",
            "transition shells and boundaries are either excluded, routed, or separately bounded",
            "conditional_private_selector",
            "needed to prevent gradients/boundaries from dominating the U_B^2 bulk result",
            "run numeric J_res profile smoke or prove transition-current routing from parent no-flux theorem",
        ),
    ]
    return [
        {
            **common(),
            "signature_id": signature_id,
            "required_parent_signature": required_parent_signature,
            "current_status": current_status,
            "why_it_matters": why_it_matters,
            "next_action": next_action,
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for signature_id, required_parent_signature, current_status, why_it_matters, next_action in entries
    ]


def jres_consequence_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "CONS4195_0_scalar",
            "R_L-even scalar descent",
            "m_L-m_0=O(D_L^2)",
            "keeps D_t m_L and Delta_h m_L quadratic if gradients preserve powers",
            "conditional_exact_lemma",
        ),
        (
            "CONS4195_1_source",
            "R_L-odd/covariant projected source",
            "S_cg=O(D_L)",
            "makes U_B S_cg=O(U_B^2)",
            "conditional_exact_lemma",
        ),
        (
            "CONS4195_2_bulk_Jres",
            "scalar evenness + source covariance + bounded H_L",
            "J_res_bulk=O(U_B^2)",
            "matches the 4194 nJ=2 route",
            "conditional_not_parent_signed",
        ),
        (
            "CONS4195_3_local_GR",
            "all above plus boundary and transition routing plus amplitude budgets",
            "local PPN residual can be zero/bounded",
            "not enough for public local GR claim without parent signatures and numeric source-backed bounds",
            "blocked_as_claim",
        ),
    ]
    return [
        {
            **common(),
            "consequence_id": consequence_id,
            "condition": condition,
            "mathematical_result": mathematical_result,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for consequence_id, condition, mathematical_result, effect, status in entries
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "lemma_proved_under_contract": "True",
            "parent_owns_RL_involution": "False",
            "parent_owns_scalar_descent": "False",
            "parent_owns_source_covariance": "False",
            "Jres_bulk_power_if_contract_signed": "O(U_B^2)",
            "exact_local_GR_claim_closed": "False",
            "recommended_next": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4195_0_no_parent_ownership_claim",
            "Do not say MTS derives scalar evenness unless R_L is a parent symmetry/gauge redundancy.",
        ),
        (
            "FW4195_1_no_local_GR_claim",
            "Do not say local GR/PPN is solved: transition, boundary and amplitude budgets remain active.",
        ),
        (
            "FW4195_2_no_numeric_pass",
            "No numeric local bound pass is made in 4195; this is a derivation contract.",
        ),
        (
            "FW4195_3_no_hidden_scalar_linear_channel",
            "If scalar leakage channels are allowed to be signed observables, the quadratic route fails.",
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
            "route_A_derivation_first": "prove scalar leakage reference nulling: scalar z_theta/z_dotB/z_Lcg channels are quotient/gauge representatives, not physical signed scalars",
            "route_B_smoke_first": "run normalized J_res profile smoke using the 4194 budget multipliers for mu_Xi*T_res, L_res/L_loc, A_J and boundary amplitude",
            "recommended_first": "route_A if still deriving; route_B if we want immediate plausibility numbers",
            "why": "4195 proves the parity/evenness lemma under an R_L contract, but 128 shows the remaining danger is scalar signed leakage, not vector/tensor leakage.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4195 converts the parity/evenness route into an exact lemma under a leakage involution R_L, but current sources do not parent-sign R_L, scalar descent, or source covariance.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_docs() -> None:
    formal = f"""# 211 - PPC4161 Parent ZL Parity Signature

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint proves a clean local parity/evenness lemma under an explicit leakage-involution contract, but it does **not** prove that the current MTS parent action owns that contract.

## Exact Lemma Under Contract

Let `z_L^A` be signed leakage coordinates around the compact local GR leaf `z_L=0`, with quotient/local observables `Y` fixed. Suppose there is an involution:

```text
R_L: z_L^A -> -z_L^A,    R_L Y = Y.
```

If the parent action, measure, coframe/connection, projector and coarse-graining maps are `R_L`-equivariant, then sign of `z_L` is a representative label rather than an extra physical scalar.

If scalar local memory descends through `R_L`-even invariants:

```text
m_L(R_L z,Y) = m_L(z,Y),
```

then the Taylor expansion at the local leaf has no linear term:

```text
m_L(z,Y) = m_0(Y) + 1/2 H_AB(Y) z_L^A z_L^B + O(|z_L|^3).
```

So:

```text
m_L - m_0 = O(D_L^2).
```

If the projected residual source is odd/covariant or support-silent:

```text
S_cg(R_L z,Y) = -S_cg(z,Y),
```

then:

```text
S_cg(0,Y)=0,
||S_cg|| <= C_S D_L.
```

With the bounded leakage map:

```text
z_L^A = U_B H_L^A(Y),    ||H_L|| <= C_H,
```

we get:

```text
D_L <= C_D U_B,
S_cg = O(U_B),
m_L - m_0 = O(U_B^2).
```

Therefore the 4194 bulk residual route is mathematically valid under the contract:

```text
U_B S_cg = O(U_B^2),
D_m Delta_h m_L = O(D_m U_B^2/L_B^2),
D_t m_L = O(U_B^2/T_B),
J_res,bulk = O(U_B^2).
```

## What Did Not Close

This does not yet parent-sign the local GR branch because three signatures remain open:

1. `R_L` must be a symmetry/gauge redundancy of the parent and coarse-graining maps, not a chosen post-hoc reflection.
2. Scalar leakage channels identified in `128-leakage-frame-symmetry.md` must be reference-null or quotient variables; ordinary spatial reflection does not remove signed scalar leakage by itself.
3. `P_loc S_cg` must transform as an odd/covariant leakage source or be support-silent under the same parent current operator.

So 4195 is a real mathematical narrowing, not a final victory lap.

## Verdict

The parity/evenness mechanism is internally strong:

```text
R_L contract signed => nS=1, nL=2, nJ_bulk=2.
```

The current MTS corpus has not yet signed the `R_L` contract at parent level:

```text
parent_owns_R_L = false,
parent_owns_scalar_descent = false,
parent_owns_source_covariance = false.
```

## Next Gate

`{NEXT_TARGET}` should either prove scalar leakage reference nulling from the parent quotient map, or run the normalized `J_res` profile smoke against the 4194 amplitude budgets.
"""
    checkpoint = f"""# 4195 - Y5 R2FR Parent ZL Parity Signature Or Jres Numeric Profile Smoke

Decision: `{DECISION}`

## Summary

4195 tries the derivation-first path for the 4194 `J_res=O(U_B^2)` route.

It proves the useful lemma:

```text
leakage involution R_L + scalar even descent + source odd/covariance + bounded H_L
=> S_cg=O(U_B), m_L-m_0=O(U_B^2), J_res,bulk=O(U_B^2).
```

That is the right mathematical shape for the local branch.

## Hard Result

The lemma itself is not the weak point. The weak point is ownership.

Current source files show:

- `125` defines a candidate `Z_L` invariant and `D_L<=U_B` style bound.
- `126` gives scalar evenness as a theorem-shaped parity candidate, not parent-derived.
- `128` explicitly warns that true scalar leakage channels can still enter linearly.
- `131` keeps gradient suppression far-local and leaves transition shells open.
- `192` gives boundary/no-flux routing only in the private selector branch.

## Consequence

The route is not dead. It is sharper:

```text
derive R_L as parent quotient/gauge symmetry
or
run numeric J_res profile smoke to see if the amplitude budget is plausible.
```

## Nonclaim Firewall

No local GR, PPN, R10, clock, orbital, or public empirical claim is made here.
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
            "claim": "The Z_L parity/evenness route is an exact local lemma under a parent leakage-involution contract, giving S_cg=O(U_B), m_L-m_0=O(U_B^2), and J_res,bulk=O(U_B^2), but parent ownership of the involution remains open.",
            "current_evidence": "4195 source audit, parity lemma rows, parent-signature ledger, J_res consequence table, decision row and nonclaim firewall.",
            "status": "private_conditional_parity_lemma_parent_ownership_open",
            "next_test": "Prove scalar leakage reference nulling and source covariance from the parent quotient map, or run normalized J_res profile smoke against the 4194 budgets.",
            "key_risk": "Treating a useful reflection lemma as a parent-derived symmetry would smuggle in the local screening mechanism instead of deriving it.",
        },
    )
    append_unique_line(
        SPINE_PATH,
        SPINE_MARKER,
        f"""

### PPC4161 Parent ZL Parity Signature - 4195

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4195 proves the clean lemma:

```text
R_L: z_L -> -z_L, scalar even descent, source odd/covariance, bounded H_L
=> nS=1, nL=2, nJ_bulk=2.
```

The parent action has not yet signed `R_L`, scalar descent, or source covariance. The remaining sharp blocker is the scalar signed leakage channel flagged by `128`; vector/tensor leakage reflection is not enough.
""",
    )
    append_unique_line(
        PACKET_180_PATH,
        PACKET_MARKER,
        f"""

## PPC4161 Packet Parent ZL Parity Signature - 4195

Marker: `{PACKET_MARKER}`

Inside the private packet, the 4194 `J_res=O(U_B^2)` route is now tied to an explicit leakage involution contract:

```text
R_L: z_L^A -> -z_L^A,
m_L(R_L z,Y)=m_L(z,Y),
S_cg(R_L z,Y)=-S_cg(z,Y).
```

If parent-owned, this gives `S_cg=O(U_B)`, `m_L-m_0=O(U_B^2)`, and `J_res,bulk=O(U_B^2)`. Current packet status remains nonclaim because parent ownership of `R_L`, scalar descent, source covariance, transition routing, and amplitude budgets is still open.
""",
    )


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4195_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4195_PARITY_LEMMA.csv": lemma_rows(),
        "P8_Y5_R2FR_4195_PARENT_SIGNATURE_AUDIT.csv": parent_signature_rows(),
        "P8_Y5_R2FR_4195_JRES_CONSEQUENCE.csv": jres_consequence_rows(),
        "P8_Y5_R2FR_4195_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4195_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4195_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4195_STATUS.csv": status_rows(),
    }


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4195_SOURCE_REGISTER.csv"]
    lemma = rows_by_file["P8_Y5_R2FR_4195_PARITY_LEMMA.csv"]
    parent = rows_by_file["P8_Y5_R2FR_4195_PARENT_SIGNATURE_AUDIT.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4195_DECISION.csv"][0]
    firewall = rows_by_file["P8_Y5_R2FR_4195_CLAIM_FIREWALL.csv"]

    checks = [
        (
            "VAL4195_0_sources_exist",
            "all source paths exist",
            all(row["exists"] == "True" for row in source),
        ),
        (
            "VAL4195_1_source_tokens",
            "all source required text markers found",
            all(row["required_text_found"] == "True" for row in source),
        ),
        (
            "VAL4195_2_lemma_contract_present",
            "leakage involution, scalar evenness, source parity and boundary rows exist",
            {"LEM4195_1_leakage_involution", "LEM4195_2_scalar_evenness", "LEM4195_3_source_parity", "LEM4195_5_boundary_routing"}.issubset(
                {row["lemma_id"] for row in lemma}
            ),
        ),
        (
            "VAL4195_3_exact_lemma_not_parent_claim",
            "lemma proved under contract but parent ownership false",
            decision["lemma_proved_under_contract"] == "True"
            and decision["parent_owns_RL_involution"] == "False"
            and decision["parent_owns_scalar_descent"] == "False",
        ),
        (
            "VAL4195_4_parent_rows_unsigned",
            "parent signatures remain unsigned",
            all(row["parent_signed"] == "False" for row in parent),
        ),
        (
            "VAL4195_5_Jres_bulk_power_recorded",
            "Jres consequence records O(U_B^2)",
            any(row["mathematical_result"] == "J_res_bulk=O(U_B^2)" for row in rows_by_file["P8_Y5_R2FR_4195_JRES_CONSEQUENCE.csv"]),
        ),
        (
            "VAL4195_6_no_claim_flags",
            "no 4195 row has claim_allowed or valid_for_claim true",
            all(
                row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False"
                for table in rows_by_file.values()
                for row in table
            ),
        ),
        (
            "VAL4195_7_firewall_rows",
            "firewall contains no parent ownership, no local GR, no numeric pass, no hidden scalar rule",
            len(firewall) == 4,
        ),
        (
            "VAL4195_8_docs_written",
            "formal and checkpoint docs contain markers",
            SPINE_MARKER in read_text(FORMAL_PATH) and DECISION in read_text(DOC_PATH),
        ),
        (
            "VAL4195_9_claim_register",
            "claim register has L-036",
            CLAIM_ID in read_text(CLAIMS_PATH),
        ),
        (
            "VAL4195_10_spine_marker",
            "spine marker appended",
            SPINE_MARKER in read_text(SPINE_PATH),
        ),
        (
            "VAL4195_11_packet_marker",
            "packet marker appended",
            PACKET_MARKER in read_text(PACKET_180_PATH),
        ),
        (
            "VAL4195_12_next_target",
            "next target selected",
            NEXT_TARGET in rows_by_file["P8_Y5_R2FR_4195_NEXT_TARGET.csv"][0]["next_target"],
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
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4195_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4195 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4195_VALIDATION.csv'}")
    print("rows=13 validation checks")


if __name__ == "__main__":
    main()
