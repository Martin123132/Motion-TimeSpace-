from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4238"
CLAIM_ID = "L-079"
BRANCH = "MTS_R2FR_Y5_VERTICAL_CURRENT_M2_ZERO_THEOREM_4238"
DECISION = "VERTICAL_CURRENT_M2_ZERO_THEOREM_EXACT_CONTRACT_WRITTEN_PARENT_SIGNATURE_OPEN_PROFILE_SAMPLER_FALLBACK_STAGED_NONCLAIM"
MARKER = "PPC4161_VERTICAL_CURRENT_M2_ZERO_THEOREM_4238"
PACKET_MARKER = "PPC4161_PACKET_VERTICAL_CURRENT_M2_ZERO_THEOREM_4238"
NEXT_TARGET = "4239-Y5-R2FR-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md"

FORMAL_PATH = FORMAL / "254-PPC4161-vertical-current-M2-zero-theorem-or-profile-sampler.md"
DOC_PATH = POST / "4238-Y5-R2FR-vertical-current-M2-zero-theorem-or-profile-sampler.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4238_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4238_00_4237_next": SourceSpec(
        "SRC4238_00_4237_next",
        SOURCE_DIR / "P8_Y5_R2FR_4237_NEXT_TARGET.csv",
        "4238-Y5-R2FR-vertical-current-M2-zero-theorem-or-profile-sampler.md",
        "4237 selected the vertical-current/M2 zero theorem target.",
    ),
    "SRC4238_01_4237_formal": SourceSpec(
        "SRC4238_01_4237_formal",
        FORMAL / "253-PPC4161-AJ-source-coefficient-theorem-or-numeric-fill-pack.md",
        "A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|.",
        "4237 coefficient theorem to be zeroed or sampled.",
    ),
    "SRC4238_02_4237_zeroes": SourceSpec(
        "SRC4238_02_4237_zeroes",
        SOURCE_DIR / "P8_Y5_R2FR_4237_ZERO_CANDIDATES.csv",
        "S_A H_L^A = Delta_h M_2 = D_t M_2 = 0",
        "Machine-readable exact-zero target from 4237.",
    ),
    "SRC4238_03_fixed_point": SourceSpec(
        "SRC4238_03_fixed_point",
        FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md",
        "stationary and projected-homogeneous local invariants imply:",
        "Existing fixed-point argument for stationary/homogeneous local invariants.",
    ),
    "SRC4238_04_boundary_domain": SourceSpec(
        "SRC4238_04_boundary_domain",
        FORMAL / "208-PPC4161-parent-Xi-Hessian-signs-and-boundary-domain.md",
        "Nonzero radiative/open-memory flux must be routed as Hamiltonian boundary charge",
        "Boundary routing/self-adjoint local domain source.",
    ),
    "SRC4238_05_no_flux": SourceSpec(
        "SRC4238_05_no_flux",
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN.",
        "Private compact no-flux collar theorem.",
    ),
    "SRC4238_06_leakage_vector": SourceSpec(
        "SRC4238_06_leakage_vector",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "Z_L^A =",
        "Local leakage vector/profile candidate used by M2.",
    ),
    "SRC4238_07_leakage_scaling": SourceSpec(
        "SRC4238_07_leakage_scaling",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "D_L <= U_B.",
        "Algebraic leakage smallness if H_L is bounded.",
    ),
    "SRC4238_08_parity": SourceSpec(
        "SRC4238_08_parity",
        FORMAL / "211-PPC4161-parent-ZL-parity-signature.md",
        "S_cg(0,Y)=0,",
        "Source-current parity/silence precursor.",
    ),
    "SRC4238_09_private_tensor": SourceSpec(
        "SRC4238_09_private_tensor",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "R_i^K = |W_i^K| N_T/D_T = 0",
        "Kperp private closure retained as background condition.",
    ),
    "SRC4238_10_claim_register": SourceSpec(
        "SRC4238_10_claim_register",
        FORMAL / "02-claims-register.csv",
        "L-078",
        "Prior claim-register anchor for 4237.",
    ),
}


def common() -> Dict[str, str]:
    return {"timestamp_utc": STAMP, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"empty csv: {path}")
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


def csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def zero_theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ZT4238_0_start",
            "A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|",
            "4237 starting point.",
            "imported",
        ),
        (
            "ZT4238_1_source_zero",
            "If Dq(H_L)=0 and source current descends through q, then S_A H_L^A = 0.",
            "Vertical leakage is representative/gauge motion for the source sector.",
            "exact theorem clause unsigned",
        ),
        (
            "ZT4238_2_harmonic_neumann",
            "If Delta_h M_2 = 0 and n^i grad_i M_2|partialW = 0 on connected compact W, then grad_i M_2 = 0.",
            "Integrate M_2 Delta_h M_2 by parts; no-flux boundary kills the surface term.",
            "mathematical lemma",
        ),
        (
            "ZT4238_3_quotient_constant",
            "If M_2 descends only through projected-homogeneous local invariants, then grad_i M_2 = 0 and Delta_h M_2 = 0.",
            "This is the stronger parent route: no internal M2 source appears.",
            "exact theorem clause unsigned",
        ),
        (
            "ZT4238_4_stationary_flow",
            "If Lie_u H_L^A = 0 and Lie_u H_AB = 0, then D_t M_2 = 0.",
            "Stationary dressed-source flow preserves the leakage-shape scalar.",
            "exact theorem clause unsigned",
        ),
        (
            "ZT4238_5_full_zero",
            "source descent + quotient-constant/harmonic M_2 + stationary flow => A_J,eff_private = 0 at O(U_B^2).",
            "This would close the private cGamma source-amplitude route at leading order.",
            "not parent-signed",
        ),
        (
            "ZT4238_6_remainder",
            "Remaining source starts at O(U_B^3) plus explicitly routed boundary/radiation terms.",
            "If the clauses hold, 4236 strong local budget becomes easy; if not, sample the profile.",
            "conditional",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, formula, meaning, status in rows
    ]


def clause_gate_rows() -> List[Dict[str, str]]:
    rows = [
        ("CG4238_0_verticality", "Dq(H_L)=0", "open", "Need parent quotient map proving H_L is vertical/representative for source readout."),
        ("CG4238_1_source_descent", "S_cg = Sbar[q(Phi),Y] or source-current annihilates ker(Dq)", "open", "This is stronger than odd parity; it kills the linear source contraction."),
        ("CG4238_2_M2_descent", "M_2 = Mbar[q(Phi),I_loc] with projected-homogeneous local invariants", "open", "Would give grad M2=Delta M2=0 in the compact local readout."),
        ("CG4238_3_no_flux_domain", "n grad M_2|partialW = 0 or fixed boundary value", "private_pass", "Covered in the compact no-flux selector, but public/global adoption remains open."),
        ("CG4238_4_stationary_flow", "Lie_u H_L = Lie_u H_AB = 0", "open", "Needed to kill D_t M2 rather than just bound it."),
        ("CG4238_5_boundary_routing", "radiative/open-memory flux routed as Hamiltonian boundary charge", "private_pass", "Do not hide boundary flux inside AJ."),
        ("CG4238_6_tensor_background", "Kperp private static force removed", "private_pass", "Keeps the 4238 branch scalar/cGamma-only."),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "status": status,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, status, next_action in rows
    ]


def profile_sampler_schema_rows() -> List[Dict[str, str]]:
    rows = [
        ("PS4238_0_domain", "W_loc geometry / collar mesh", "geometry", "needed to evaluate gradients/Laplacian", "MISSING_PROFILE_INPUT"),
        ("PS4238_1_HL", "H_L^A(x,t)", "profile", "needed for source contraction and M2", "MISSING_PROFILE_INPUT"),
        ("PS4238_2_HAB", "H_AB(x,t)", "profile", "needed for M2", "MISSING_PROFILE_INPUT"),
        ("PS4238_3_SA", "S_A(x,t)", "source-current Jacobian", "needed for S_A H_L^A", "MISSING_SOURCE_INPUT"),
        ("PS4238_4_M2", "M_2=1/2 H_AB H_L^A H_L^B", "derived profile", "compute from H_L/H_AB", "DERIVED_AFTER_INPUTS"),
        ("PS4238_5_DeltaM2", "Delta_h M_2", "derived profile", "compute A_lap", "DERIVED_AFTER_INPUTS"),
        ("PS4238_6_DtM2", "D_t M_2", "derived profile", "compute A_drift", "DERIVED_AFTER_INPUTS"),
        ("PS4238_7_budget", "|SAH|+|Dm DeltaM2|+|DtM2|", "score row", "compare to 4236 strong local budget", "BLOCKED_UNTIL_INPUTS"),
    ]
    return [
        {
            **common(),
            "sampler_id": sampler_id,
            "quantity": quantity,
            "kind": kind,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for sampler_id, quantity, kind, role, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "forward_move": "Exact zero route reduced to three parent signatures: source descent/vertical orthogonality, M2 quotient-constant or harmonic no-flux behavior, and stationary leakage-shape flow.",
            "zero_claimed": "False",
            "scoreable_now": "False",
            "why_not_scoreable": "The central source-descent, M2-descent and stationary-flow clauses are unsigned; profile sampler inputs are staged but absent.",
            "best_next_move": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4238_0_no_zero_claim", "Do not claim A_J,eff_private=0 unless source descent, M2 descent/harmonicity, and stationary flow are all parent-signed.", "active"),
        ("FW4238_1_no_harmonic_smuggle", "Do not assume Delta_h M2=0; prove quotient-constant/harmonic source-free behavior or sample it.", "active"),
        ("FW4238_2_no_source_smuggle", "Odd source parity gives S_cg(0)=0, not S_A H_L^A=0; source descent/orthogonality is required.", "active"),
        ("FW4238_3_no_boundary_smuggle", "Any nonzero radiative/open-memory flux stays as boundary charge or explicit bound row.", "active"),
        ("FW4238_4_sampler_nonclaim", "Profile sampler schema rows are nonclaim until real parent/profile inputs are supplied.", "active"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule, status in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": "private_exact_zero_contract_nonclaim",
            "summary": "4238 proves the exact local zero contract under source-descent, quotient-constant/harmonic M2 and stationary-flow clauses, while staging a profile sampler fallback.",
            "zero_claimed": "False",
            "scoreable_now": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "The cheapest remaining route is to attack S_A H_L^A=0 from parent source descent; if that fails, build the M2 profile sampler dry-run.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> Iterable[List[Dict[str, str]]]:
    return (
        source_rows(),
        zero_theorem_rows(),
        clause_gate_rows(),
        profile_sampler_schema_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    )


def formal_doc() -> str:
    return f"""
# 254 - PPC4161 Vertical Current M2 Zero Theorem Or Profile Sampler

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4238 proves the exact contract for killing the 4237 coefficient rows. Starting from:

```text
A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|,
M_2 = 1/2 H_AB H_L^A H_L^B,
```

the private leading source amplitude vanishes if:

```text
S_A H_L^A = 0,
Delta_h M_2 = 0,
D_t M_2 = 0.
```

## Exact Zero Route

The least-smuggled parent route is:

```text
Dq(H_L)=0,
S_cg descends through q or annihilates ker(Dq),
M_2 descends through projected-homogeneous local invariants,
Lie_u H_L^A = Lie_u H_AB = 0,
boundary flux is no-flux/fixed/routed.
```

Then:

```text
S_A H_L^A = 0,
grad_i M_2 = 0,
Delta_h M_2 = 0,
D_t M_2 = 0,
A_J,eff_private = 0 + O(U_B).
```

Equivalently, a harmonic no-flux proof also works for the shape term:

```text
Delta_h M_2 = 0,
n^i grad_i M_2|partialW = 0
```

on a connected compact local collar implies `grad_i M_2=0` by integration by parts.

## Current Status

This is not a local-GR claim. The theorem is exact, but the central parent signatures are not all signed:

```text
source descent / vertical orthogonality: open,
M_2 quotient-constant or harmonic source-free behavior: open,
stationary leakage-shape flow: open.
```

The no-flux and boundary-routing pieces are private-selector passes, not public global theorems.

## Fallback

If the parent source-descent route does not close, use the staged profile sampler:

```text
H_L^A(x,t), H_AB(x,t), S_A(x,t)
  -> M_2
  -> S_A H_L^A, Delta_h M_2, D_t M_2
  -> compare to 4236 strong local budget.
```

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4238 - Vertical Current M2 Zero Theorem Or Profile Sampler

**Status:** `{DECISION}`.

## Forward Move

4238 proves the exact zero contract:

```text
source descent/vertical orthogonality
+ M_2 quotient-constant or harmonic no-flux behavior
+ stationary leakage-shape flow
=> A_J,eff_private = 0 at leading order.
```

This is the cleanest route to derived local cGamma silence so far.

## Not Claimed

The source-descent, M2-descent and stationary-flow clauses are still unsigned. If they do not close, the next honest path is a profile sampler for:

```text
S_A H_L^A,
Delta_h M_2,
D_t M_2.
```

## Next

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    rows = csv_rows(path)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The vertical-current/M2 exact-zero contract is written: source descent/vertical orthogonality, quotient-constant or harmonic no-flux M2, and stationary leakage-shape flow would make A_J,eff_private vanish at leading order. This remains private nonclaim until those parent signatures are supplied.",
            "current_evidence": "4238 source register, zero theorem rows, clause gates, profile sampler schema, decision and firewall.",
            "status": "private_vertical_current_M2_zero_contract_nonclaim",
            "next_test": "Attack S_A H_L^A=0 from parent source descent; otherwise build the M2 profile sampler dry-run.",
            "key_risk": "Assuming harmonic/constant M2 or source orthogonality without parent signature would smuggle the local-GR result.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Vertical Current M2 Zero Theorem

Marker: `{MARKER}`

4238 gives the exact local cGamma source-amplitude zero contract:

```text
Dq(H_L)=0,
S_cg descends through q or annihilates ker(Dq),
M_2 is quotient-constant/harmonic with no-flux boundary,
Lie_u M_2=0
```

imply:

```text
S_A H_L^A = Delta_h M_2 = D_t M_2 = 0,
A_J,eff_private = 0 at leading order.
```

This is still private/nonclaim because source descent, M2 descent and stationary-flow signatures remain open.
"""
    packet_block = f"""
## Packet Update - Vertical Current M2 Zero Theorem

Marker: `{PACKET_MARKER}`

The cGamma source route now has a precise fork:

```text
prove source/M2/stationary zero contract,
or sample S_A H_L^A, Delta_h M_2, D_t M_2 directly.
```
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    theorem = zero_theorem_rows()
    clauses = clause_gate_rows()
    sampler = profile_sampler_schema_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4238_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4238_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4238_2_zero_theorem", "zero theorem includes source/M2/stationary clauses", {"ZT4238_1_source_zero", "ZT4238_3_quotient_constant", "ZT4238_4_stationary_flow"}.issubset({row["theorem_id"] for row in theorem}), "zero theorem rows")
    add("VAL4238_3_harmonic_lemma", "harmonic no-flux lemma present", any(row["theorem_id"] == "ZT4238_2_harmonic_neumann" for row in theorem), "zero theorem rows")
    add("VAL4238_4_clause_status", "central clauses remain open", {"CG4238_0_verticality", "CG4238_1_source_descent", "CG4238_2_M2_descent", "CG4238_4_stationary_flow"}.issubset({row["clause_id"] for row in clauses if row["status"] == "open"}), "clause gates")
    add("VAL4238_5_private_passes", "private no-flux/boundary/tensor passes retained", {"CG4238_3_no_flux_domain", "CG4238_5_boundary_routing", "CG4238_6_tensor_background"}.issubset({row["clause_id"] for row in clauses if row["status"] == "private_pass"}), "clause gates")
    add("VAL4238_6_sampler_schema", "profile sampler schema covers SAH DeltaM2 DtM2", {"PS4238_3_SA", "PS4238_5_DeltaM2", "PS4238_6_DtM2"}.issubset({row["sampler_id"] for row in sampler}), "sampler schema")
    add("VAL4238_7_decision_nonclaim", "decision keeps zero and scoreable false", decision_rows()[0]["zero_claimed"] == "False" and decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4238_8_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4238_9_claim_register", "claims register contains L-079", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4238_10_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4238_11_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4238_12_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4238_13_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4238_14_firewall", "firewall has anti-smuggling rules", len(firewall_rows()) == 5 and all(row["status"] == "active" for row in firewall_rows()), "firewall")
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4238_SOURCE_REGISTER.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4238_ZERO_THEOREM_ROWS.csv",
        "clauses": SOURCE_DIR / "P8_Y5_R2FR_4238_CLAUSE_GATES.csv",
        "sampler": SOURCE_DIR / "P8_Y5_R2FR_4238_PROFILE_SAMPLER_SCHEMA.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4238_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4238_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4238_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4238_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["theorem"], zero_theorem_rows())
    write_csv(paths["clauses"], clause_gate_rows())
    write_csv(paths["sampler"], profile_sampler_schema_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows())
    failed_rows = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed_rows)}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAILED {failed_row['check_id']}: {failed_row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
