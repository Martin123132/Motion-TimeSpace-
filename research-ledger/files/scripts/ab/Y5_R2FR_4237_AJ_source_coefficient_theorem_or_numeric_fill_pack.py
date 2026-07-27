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

CHECKPOINT = "4237"
CLAIM_ID = "L-078"
BRANCH = "MTS_R2FR_Y5_AJ_SOURCE_COEFFICIENT_THEOREM_4237"
DECISION = "AJ_SOURCE_COEFFICIENT_THEOREM_DERIVED_TO_VERTICAL_CURRENT_AND_M2_SHAPE_FUNCTION_NUMERIC_FILL_OPEN_NONCLAIM"
MARKER = "PPC4161_AJ_SOURCE_COEFFICIENT_THEOREM_4237"
PACKET_MARKER = "PPC4161_PACKET_AJ_SOURCE_COEFFICIENT_THEOREM_4237"
NEXT_TARGET = "4238-Y5-R2FR-vertical-current-M2-zero-theorem-or-profile-sampler.md"

FORMAL_PATH = FORMAL / "253-PPC4161-AJ-source-coefficient-theorem-or-numeric-fill-pack.md"
DOC_PATH = POST / "4237-Y5-R2FR-AJ-source-coefficient-theorem-or-numeric-fill-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4237_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4237_00_4236_next": SourceSpec(
        "SRC4237_00_4236_next",
        SOURCE_DIR / "P8_Y5_R2FR_4236_NEXT_TARGET.csv",
        "4237-Y5-R2FR-AJ-source-coefficient-theorem-or-numeric-fill-pack.md",
        "4236 selected the AJ source coefficient theorem/fill target.",
    ),
    "SRC4237_01_4236_formal": SourceSpec(
        "SRC4237_01_4236_formal",
        FORMAL / "252-PPC4161-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md",
        "A_J,eff_private = A_src + A_lap + A_drift.",
        "4236 reduced the private cGamma obstruction to three source coefficients.",
    ),
    "SRC4237_02_4236_ledger": SourceSpec(
        "SRC4237_02_4236_ledger",
        SOURCE_DIR / "P8_Y5_R2FR_4236_AJ_COEFFICIENT_LEDGER.csv",
        "A_J_eff_private = A_src + A_lap + A_drift",
        "Machine-readable 4236 AJ coefficient ledger.",
    ),
    "SRC4237_03_parity_m": SourceSpec(
        "SRC4237_03_parity_m",
        FORMAL / "211-PPC4161-parent-ZL-parity-signature.md",
        "m_L(z,Y) = m_0(Y) + 1/2 H_AB(Y) z_L^A z_L^B + O(|z_L|^3).",
        "Parent leakage-evenness expansion for scalar memory.",
    ),
    "SRC4237_04_parity_source": SourceSpec(
        "SRC4237_04_parity_source",
        FORMAL / "211-PPC4161-parent-ZL-parity-signature.md",
        "||S_cg|| <= C_S D_L.",
        "Parent source-current Lipschitz/odd support bound.",
    ),
    "SRC4237_05_leakage_profile": SourceSpec(
        "SRC4237_05_leakage_profile",
        FORMAL / "211-PPC4161-parent-ZL-parity-signature.md",
        "z_L^A = U_B H_L^A(Y),    ||H_L|| <= C_H,",
        "Leakage profile scaling that turns powers into coefficients.",
    ),
    "SRC4237_06_support_powers": SourceSpec(
        "SRC4237_06_support_powers",
        FORMAL / "210-PPC4161-source-support-powers-for-Jres.md",
        "D_m Delta_h m_L = O(D_m U_B^2/L_B^2),",
        "Laplacian contribution in the J_res support-power route.",
    ),
    "SRC4237_07_amplitude_owner": SourceSpec(
        "SRC4237_07_amplitude_owner",
        FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md",
        "A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2.",
        "Parent AJ amplitude owner decomposition.",
    ),
    "SRC4237_08_operator_bound": SourceSpec(
        "SRC4237_08_operator_bound",
        FORMAL / "215-PPC4161-source-operator-amplitude-AJ-bound.md",
        "A_J,eff <= C_D C_S",
        "Prior source-operator coefficient contract.",
    ),
    "SRC4237_09_operator_missing": SourceSpec(
        "SRC4237_09_operator_missing",
        FORMAL / "215-PPC4161-source-operator-amplitude-AJ-bound.md",
        "C_D, C_S, C_M, C_lap, C_t,",
        "Open primitive constants that must become parent-owned or numeric rows.",
    ),
    "SRC4237_10_kperp_closed": SourceSpec(
        "SRC4237_10_kperp_closed",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "R_i^K = |W_i^K| N_T/D_T = 0",
        "4234 private tensor/Kperp closure used to keep AJ scalar-only.",
    ),
    "SRC4237_11_cgamma_budget": SourceSpec(
        "SRC4237_11_cgamma_budget",
        FORMAL / "251-PPC4161-cGamma-support-nohair-or-full-budget-profile-bound-runner.md",
        "|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1",
        "4235 full-budget cGamma local row.",
    ),
    "SRC4237_12_claim_register": SourceSpec(
        "SRC4237_12_claim_register",
        FORMAL / "02-claims-register.csv",
        "L-077",
        "Prior claim-register anchor for 4236.",
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


def all_generated_groups() -> Iterable[List[Dict[str, str]]]:
    return (
        source_rows(),
        theorem_rows(),
        coefficient_map_rows(),
        zero_candidate_rows(),
        numeric_fill_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    )


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


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "TH4237_0_vertical_profile",
            "z_L^A = U_B H_L^A(Y)",
            "Use the parent leakage profile as the carrier of all local residual coefficients.",
            "imported conditional from 4195",
        ),
        (
            "TH4237_1_source_expansion",
            "S_cg(z,Y) = S_A(Y) z_L^A + O(|z_L|^2)",
            "Odd/covariant source current gives a linear vertical-current coefficient.",
            "derived Taylor form under R_L contract",
        ),
        (
            "TH4237_2_memory_shape",
            "m_L(z,Y) = m_0(Y) + U_B^2 M_2(Y) + O(U_B^3)",
            "Even scalar memory collapses the lap/drift pieces onto one leakage-shape scalar.",
            "derived from m_AB H_L^A H_L^B",
        ),
        (
            "TH4237_3_M2_definition",
            "M_2(Y) := 1/2 H_AB(Y) H_L^A(Y) H_L^B(Y)",
            "Defines the only shape function needed by A_lap and A_drift at leading order.",
            "new coefficient theorem",
        ),
        (
            "TH4237_4_Jres_expansion",
            "J_res = U_B^2 [S_A H_L^A + D_m Delta_h M_2 - D_t M_2] + O(U_B^3) + boundary_in",
            "Leading private compact AJ coefficient is no longer arbitrary.",
            "new coefficient theorem",
        ),
        (
            "TH4237_5_private_compact",
            "A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|",
            "4234/4235 remove boundary/Kperp in the private compact selector.",
            "active private bound, not numeric",
        ),
        (
            "TH4237_6_budget_gate",
            "|S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2| <= 0.1678939074330212*(mu_Xi T_res)/|c_Gamma|",
            "Strong local Gdot gate translated into vertical-current/M2 language.",
            "scoreable only after source rows exist",
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


def coefficient_map_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CM4237_0_A_src_exact",
            "A_src",
            "sup_local |S_A H_L^A|",
            "sup_local C_S C_H or C_D C_S",
            "source-current contraction, not a free amplitude",
            "open_source_current_projection",
        ),
        (
            "CM4237_1_A_lap_exact",
            "A_lap",
            "sup_local |D_m Delta_h M_2|",
            "D_m C_M C_lap/L_B^2",
            "Laplacian of the leakage-shape scalar",
            "open_shape_laplacian",
        ),
        (
            "CM4237_2_A_drift_exact",
            "A_drift",
            "sup_local |D_t M_2|",
            "C_M C_t/T_B",
            "Time drift of the same leakage-shape scalar",
            "open_shape_drift",
        ),
        (
            "CM4237_3_AJ_exact",
            "A_J_eff_private",
            "sup_local |S_A H_L^A + D_m Delta_h M_2 - D_t M_2|",
            "A_src + A_lap + A_drift",
            "combined private compact coefficient without cancellation credit",
            "derived_symbolic_bound",
        ),
        (
            "CM4237_4_no_cancellation",
            "absolute_budget",
            "|x+y-z| <= |x|+|y|+|z|",
            "no cancellation used",
            "prevents fake pass by tuned source/lap/drift cancellation",
            "active_guard",
        ),
    ]
    return [
        {
            **common(),
            "coefficient_map_id": coefficient_map_id,
            "coefficient": coefficient,
            "exact_row": exact_row,
            "safe_bound": safe_bound,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for coefficient_map_id, coefficient, exact_row, safe_bound, meaning, status in rows
    ]


def zero_candidate_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ZC4237_0_source_blind",
            "S_A H_L^A = 0",
            "A_src = 0 at leading U_B^2",
            "Requires parent source-current to be vertical-orthogonal or support-silent, not merely odd.",
            "unsigned",
        ),
        (
            "ZC4237_1_harmonic_shape",
            "Delta_h M_2 = 0",
            "A_lap = 0 at leading U_B^2",
            "Requires M_2 harmonic/constant on the tested compact local collar.",
            "unsigned",
        ),
        (
            "ZC4237_2_stationary_shape",
            "D_t M_2 = 0",
            "A_drift = 0 at leading U_B^2",
            "Requires stationary dressed source or parent flow preserving the leakage-shape scalar.",
            "unsigned",
        ),
        (
            "ZC4237_3_full_zero",
            "S_A H_L^A = Delta_h M_2 = D_t M_2 = 0",
            "A_J_eff_private = 0 at leading U_B^2",
            "Would close the private cGamma source amplitude route, but all three clauses need parent signatures.",
            "target_not_claimed",
        ),
        (
            "ZC4237_4_numeric_fallback",
            "|S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2| <= budget",
            "local branch can still pass without exact zeros",
            "Requires sourced numeric rows for vertical-current/M2 profiles, tau ratio and cGamma.",
            "fallback_open",
        ),
    ]
    return [
        {
            **common(),
            "zero_candidate_id": zero_candidate_id,
            "condition": condition,
            "effect": effect,
            "required_parent_signature": required_parent_signature,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for zero_candidate_id, condition, effect, required_parent_signature, status in rows
    ]


def numeric_fill_rows() -> List[Dict[str, str]]:
    rows = [
        ("NF4237_0_HL", "H_L^A(Y)", "dimensionless", "needed for A_src and M_2", "MISSING_PARENT_PROFILE", "False"),
        ("NF4237_1_SAH", "S_A H_L^A", "dimensionless source-current contraction", "fills A_src", "MISSING_PARENT_CURRENT", "False"),
        ("NF4237_2_M2", "M_2(Y)", "dimensionless leakage-shape scalar", "owner for A_lap/A_drift", "MISSING_PARENT_SHAPE", "False"),
        ("NF4237_3_DeltaM2", "Delta_h M_2", "1/length^2 before normalization", "fills A_lap", "MISSING_LOCAL_PROFILE", "False"),
        ("NF4237_4_DtM2", "D_t M_2", "1/time before normalization", "fills A_drift", "MISSING_LOCAL_PROFILE", "False"),
        ("NF4237_5_Dm", "D_m", "diffusion/memory mobility normalization", "fills A_lap normalization", "MISSING_PARENT_NORMALIZATION", "False"),
        ("NF4237_6_tau_ratio", "T_res/tau_L", "dimensionless", "turns mu_Xi T_res into Pi_B*T_res/tau_L", "MISSING_TIMESCALE_SOURCE", "False"),
        ("NF4237_7_cGamma", "c_Gamma", "dimensionless readout coupling", "sets local budget denominator", "MISSING_COUPLING_SOURCE", "False"),
        ("NF4237_8_profiles", "profile_a/J_a", "arena-dependent", "alpha3, Gdot, gradient score rows", "MISSING_ARENA_PROJECTION", "False"),
    ]
    return [
        {
            **common(),
            "fill_id": fill_id,
            "quantity": quantity,
            "units": units,
            "role": role,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "claim_allowed": "False",
        }
        for fill_id, quantity, units, role, status, valid_for_claim in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "forward_move": "A_src/A_lap/A_drift are reduced to S_A H_L^A and the single scalar M_2=1/2 H_AB H_L^A H_L^B, instead of being arbitrary amplitudes.",
            "scoreable_now": "False",
            "why_not_scoreable": "S_A H_L^A, M_2 profiles, D_m, T_res/tau_L, c_Gamma and arena projections are still unsigned/unfilled.",
            "best_next_move": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4237_0_no_claim", "No local-GR, PPN, R10, clock, orbital or WEP claim may cite 4237 alone.", "active"),
        ("FW4237_1_no_cancellation", "Do not score |source+lap-drift| using cancellation unless the parent signs the relative phase.", "active"),
        ("FW4237_2_no_numeric_fill", "Placeholder numeric rows stay invalid for claim until sourced parent values exist.", "active"),
        ("FW4237_3_private_scope", "Boundary/Kperp closures remain private compact selector results, not global public theorems.", "active"),
        ("FW4237_4_next_gate", "4238 must either prove vertical-current/M2 zeros or build a real profile sampler.", "active"),
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
            "status": "private_derivation_forward_move_nonclaim",
            "summary": "4237 collapses the three AJ source coefficients onto one vertical current contraction plus one leakage-shape scalar M_2 and its local derivatives.",
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
            "reason": "The remaining derivation pressure is now exact: prove S_A H_L^A=0, Delta_h M_2=0 and D_t M_2=0 under the parent selector, or source a real profile sampler for those three quantities.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 253 - PPC4161 AJ Source Coefficient Theorem Or Numeric Fill Pack

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4237 is a forward derivation, not a claim. It takes the 4236 private obstruction:

```text
A_J,eff_private = A_src + A_lap + A_drift
```

and collapses the three coefficients onto one vertical-current contraction plus one leakage-shape scalar.

Use the parent leakage profile:

```text
z_L^A = U_B H_L^A(Y).
```

The odd/covariant source-current expansion is:

```text
S_cg(z,Y) = S_A(Y) z_L^A + O(|z_L|^2).
```

The even scalar-memory expansion is:

```text
m_L(z,Y) = m_0(Y) + U_B^2 M_2(Y) + O(U_B^3),
M_2(Y) := 1/2 H_AB(Y) H_L^A(Y) H_L^B(Y).
```

Therefore:

```text
J_res = U_B^2 [S_A H_L^A + D_m Delta_h M_2 - D_t M_2] + O(U_B^3) + boundary_in.
```

In the private compact selector where 4234/4235 remove boundary and Kperp from the scalar budget:

```text
A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|.
```

## Strong Local Budget

The strong local Gdot row becomes:

```text
|S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|
<= 0.1678939074330212 * (mu_Xi T_res)/|c_Gamma|.
```

Using `mu_Xi ~= Pi_B/tau_L`:

```text
<= 0.167893843691 * Pi_B*(T_res/tau_L)/|c_Gamma|.
```

## Why This Matters

The live problem is no longer three vague amplitudes. It is now:

```text
source-current contraction: S_A H_L^A,
shape Laplacian:           Delta_h M_2,
shape drift:               D_t M_2.
```

The best exact-zero route is:

```text
S_A H_L^A = 0,
Delta_h M_2 = 0,
D_t M_2 = 0.
```

If those cannot be proved, the fallback is a real profile sampler/numeric source pack for the same three quantities.

## Claim Status

No public local-GR or PPN claim is allowed from 4237. The theorem gives the exact next thing to prove or source.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4237 - AJ Source Coefficient Theorem Or Numeric Fill Pack

**Status:** `{DECISION}`.

## Forward Move

4237 turns:

```text
A_src + A_lap + A_drift
```

into:

```text
S_A H_L^A + D_m Delta_h M_2 - D_t M_2,
M_2 = 1/2 H_AB H_L^A H_L^B.
```

That is the derivation leap: the obstruction is now a vertical-current/M2 profile problem, not three disconnected closure constants.

## Still Not A Pass

The required source rows are not filled:

```text
S_A H_L^A,
Delta_h M_2,
D_t M_2,
D_m,
T_res/tau_L,
c_Gamma,
profile_a/J_a.
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
            "claim": "The 4236 AJ coefficients reduce to a vertical-current/M2 theorem: A_src, A_lap and A_drift are controlled by S_A H_L^A, Delta_h M_2 and D_t M_2, with M_2=1/2 H_AB H_L^A H_L^B. This is a private nonclaim until the vertical-current/M2 rows are parent-signed or numerically sourced.",
            "current_evidence": "4237 source register, theorem rows, coefficient map, zero-candidate ledger, numeric fill rows, decision and firewall.",
            "status": "private_AJ_coefficient_theorem_nonclaim",
            "next_test": "Prove S_A H_L^A=0, Delta_h M_2=0 and D_t M_2=0 under the parent selector, or build a real profile sampler/source pack for those rows.",
            "key_risk": "Treating the vertical-current/M2 theorem as a numeric local-GR pass would overclaim; the source rows are still missing.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 AJ Source Coefficient Theorem

Marker: `{MARKER}`

4237 reduces the 4236 private source-coefficient obstruction:

```text
A_J,eff_private = A_src + A_lap + A_drift
```

to:

```text
A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|,
M_2 = 1/2 H_AB H_L^A H_L^B.
```

This is a real derivation step: the remaining local-GR pressure is now exact vertical-current/M2 zero proof or profile sourcing, not arbitrary amplitude bookkeeping.
"""
    packet_block = f"""
## Packet Update - AJ Source Coefficient Theorem

Marker: `{PACKET_MARKER}`

4237 turns the cGamma source problem into three concrete profile rows:

```text
S_A H_L^A,
Delta_h M_2,
D_t M_2.
```

The private branch passes only if those rows vanish under the parent selector or fit inside the 4236 strong local budget after real sourcing.
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
    theorem = theorem_rows()
    coeffs = coefficient_map_rows()
    zeroes = zero_candidate_rows()
    fill = numeric_fill_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4237_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4237_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4237_2_M2_theorem", "theorem rows define M_2", any(row["theorem_id"] == "TH4237_3_M2_definition" and "H_AB" in row["formula"] for row in theorem), "theorem rows")
    add("VAL4237_3_Jres_expansion", "Jres expansion includes vertical current and M2 derivatives", any("S_A H_L^A + D_m Delta_h M_2 - D_t M_2" in row["formula"] for row in theorem), "theorem rows")
    add("VAL4237_4_coefficient_map", "coefficient map has A_src/A_lap/A_drift exact rows", {"A_src", "A_lap", "A_drift"}.issubset({row["coefficient"] for row in coeffs}), "coefficient map")
    add("VAL4237_5_no_cancellation_guard", "coefficient map includes no-cancellation guard", any(row["coefficient_map_id"] == "CM4237_4_no_cancellation" for row in coeffs), "coefficient map")
    add("VAL4237_6_zero_candidates", "zero candidates include source, harmonic and stationary clauses", {"ZC4237_0_source_blind", "ZC4237_1_harmonic_shape", "ZC4237_2_stationary_shape"}.issubset({row["zero_candidate_id"] for row in zeroes}), "zero candidates")
    add("VAL4237_7_fill_rows_invalid", "all numeric fill rows remain invalid for claim", all(row["valid_for_claim"] == "False" for row in fill), "numeric fill rows")
    add("VAL4237_8_decision_not_scoreable", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4237_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4237_10_claim_register", "claims register contains L-078", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4237_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4237_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4237_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4237_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4237_SOURCE_REGISTER.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4237_THEOREM_ROWS.csv",
        "coefficient": SOURCE_DIR / "P8_Y5_R2FR_4237_COEFFICIENT_MAP.csv",
        "zero": SOURCE_DIR / "P8_Y5_R2FR_4237_ZERO_CANDIDATES.csv",
        "fill": SOURCE_DIR / "P8_Y5_R2FR_4237_NUMERIC_FILL_ROWS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4237_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4237_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4237_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4237_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["theorem"], theorem_rows())
    write_csv(paths["coefficient"], coefficient_map_rows())
    write_csv(paths["zero"], zero_candidate_rows())
    write_csv(paths["fill"], numeric_fill_rows())
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
