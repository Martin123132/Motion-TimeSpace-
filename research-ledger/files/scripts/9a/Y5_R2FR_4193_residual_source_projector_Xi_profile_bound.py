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

CHECKPOINT = "4193"
BRANCH_ID = "MTS_R2FR_Y5_RESIDUAL_SOURCE_PROJECTOR_XI_PROFILE_4193"
DECISION = (
    "JRES_PROJECTOR_ZERO_CONTRACT_AND_GREEN_PROFILE_BUDGET_DERIVED_"
    "SOURCE_SUPPORT_AND_BOUNDARY_PARENT_SIGNATURE_STILL_OPEN_NONCLAIM"
)
DOC_PATH = POST / "4193-Y5-R2FR-residual-source-projector-and-Xi-profile-amplitude-bound.md"
FORMAL_209_PATH = FORMAL / "209-PPC4161-residual-source-projector-and-Xi-profile-amplitude-bound.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-034"
SPINE_MARKER = "PPC4161_RESIDUAL_SOURCE_PROJECTOR_XI_PROFILE_4193"
PACKET_MARKER = "PPC4161_PACKET_RESIDUAL_SOURCE_PROJECTOR_XI_PROFILE_4193"
NEXT_TARGET = "4194-Y5-R2FR-source-support-powers-for-Jres-or-numeric-profile-fill.md"

SOURCES = {
    "SRC4193_00_4192_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4192_NEXT_TARGET.csv",
        "residual source projector and Xi profile amplitude bound",
        "4192 selected the residual source/profile target.",
    ),
    "SRC4193_01_4192_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4192_RESIDUAL_SOURCE_RESOLVENT_BOUNDS.csv",
        "J_res = [1 - Pi_B] S_cg + D_m Delta_h m_L - D_t m_L + boundary_in",
        "4192 residual source definition.",
    ),
    "SRC4193_02_4190_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4190_DTXI_GRADXI_PROFILE_BOUNDS.csv",
        "2.42e-14 / |c_Gamma|",
        "4190 finite D_t Xi and gradient profile limits.",
    ),
    "SRC4193_03_formal_208": (
        FORMAL / "208-PPC4161-parent-Xi-Hessian-signs-and-boundary-domain.md",
        "delta Xi = L_Xi^-1 J_res",
        "formal 4192 Green/resolvent handoff.",
    ),
    "SRC4193_04_memory_41": (
        FORMAL / "41-memory-action-or-relaxation-law-v0.md",
        "Pi_B -> 1",
        "selected open-system local branch.",
    ),
    "SRC4193_05_support_71": (
        FORMAL / "71-source-support-boundary-law.md",
        "U_B S_cg",
        "source-support law for coarse-grained memory source.",
    ),
    "SRC4193_06_support_75": (
        FORMAL / "75-projected-source-laws.md",
        "S_cg(U_B,Y) = U_B^nS S_*(U_B,Y)",
        "projected source-power theorem form.",
    ),
    "SRC4193_07_support_75_mL": (
        FORMAL / "75-projected-source-laws.md",
        "m_L(U_B,Y) = m_* + U_B^nL m_tilde(U_B,Y)",
        "projected attractor-power theorem form.",
    ),
    "SRC4193_08_sigma_77": (
        FORMAL / "77-sigma-L-source-silence-theorem.md",
        "S_cg|local = 0",
        "exact local source-silence fixed point target.",
    ),
    "SRC4193_09_boundary_192": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "route as boundary charge, not hidden bulk current",
        "boundary/Hamiltonian routing precedent.",
    ),
    "SRC4193_10_support_results_72": (
        FORMAL / "72-source-support-boundary-first-results.md",
        "source_support_boundary_law_conditional_open",
        "prior support-boundary result status.",
    ),
    "SRC4193_11_profile_205": (
        FORMAL / "205-PPC4161-cGamma-profile-projection-coefficient-gate.md",
        "C_Gamma_Gdot = c_Gamma D_t Xi_0",
        "profile coefficient link to observables.",
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


def residual_decomposition_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "JRES4193_0_unscreened_source",
            "[1 - Pi_B] S_cg = U_B S_cg",
            "large-scale/coarse-grained memory source leaking into local branch",
            "zero if Pi_B=1 exactly or P_loc S_cg=0; bounded if S_cg=U_B^nS S_*",
            "not parent-closed",
        ),
        (
            "JRES4193_1_attractor_curvature",
            "D_m Delta_h m_L",
            "spatial variation of the local attractor",
            "zero if m_L is locally constant after P_loc; bounded if m_L=m_*+U_B^nL m_tilde with controlled derivatives",
            "not parent-closed",
        ),
        (
            "JRES4193_2_attractor_drift",
            "-D_t m_L",
            "time drift of the local attractor/readout branch",
            "zero if m_L and local invariants are stationary; bounded by U_B^nL/T_B if classifier derivatives are controlled",
            "not parent-closed",
        ),
        (
            "JRES4193_3_boundary_input",
            "boundary_in",
            "incoming homogeneous memory or boundary mismatch",
            "zero if Dirichlet/no-flux/Hamiltonian boundary routing is parent-selected; otherwise bounded by screened boundary amplitude",
            "not parent-closed",
        ),
        (
            "JRES4193_4_full_residual",
            "J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in",
            "complete residual source driving delta Xi = L_Xi^-1 J_res",
            "exact silence requires P_loc J_res=0; finite branch requires Green-profile bounds",
            "active gate",
        ),
    ]
    return [
        {
            **common(),
            "term_id": term_id,
            "term": term,
            "meaning": meaning,
            "zero_or_bound_condition": zero_or_bound_condition,
            "parent_status": parent_status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for term_id, term, meaning, zero_or_bound_condition, parent_status in entries
    ]


def projector_zero_contract_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "PZ4193_0_exact_projector",
            "P_loc J_res = 0",
            "single exact zero condition for the scalar residual source",
            "follows only if PZ4193_1 through PZ4193_4 hold",
            "open",
        ),
        (
            "PZ4193_1_source_silence",
            "P_loc[U_B S_cg]=0",
            "coarse-grained source does not project into compact local tests",
            "requires exact Pi_B=1 surface, compact support projector, or S_cg|local=0 theorem",
            "open",
        ),
        (
            "PZ4193_2_attractor_homogeneity",
            "P_loc[D_m Delta_h m_L]=0",
            "local attractor has no spatial residual in the tested collar",
            "requires constant m_* branch or source-supported m_L gradients",
            "open",
        ),
        (
            "PZ4193_3_attractor_stationarity",
            "P_loc[D_t m_L]=0",
            "local attractor has no drift along the readout time flow",
            "requires stationary local invariants and no classifier/source feedback",
            "open",
        ),
        (
            "PZ4193_4_boundary_silence",
            "P_loc[boundary_in]=0",
            "boundary term is zero, outside support, or Hamiltonian-routed",
            "requires parent-selected boundary/domain clause",
            "open",
        ),
        (
            "PZ4193_5_no_cancellation",
            "each term must vanish or be bounded separately; cross-term cancellation is not allowed as evidence",
            "prevents tuning J_res by subtracting unrelated source channels",
            "claim hygiene rule",
            "active",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "condition": condition,
            "role": role,
            "required_evidence": required_evidence,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, condition, role, required_evidence, status in entries
    ]


def finite_profile_budget_rows() -> List[Dict[str, str]]:
    c_gamma_values = [1.0, 1e-3, 1e-6, 1e-9, 1e-12]
    rows: List[Dict[str, str]] = []
    for c_gamma in c_gamma_values:
        dt_bound = 2.42e-14 / c_gamma
        grad_bound = 4.0e-9 / c_gamma
        rows.append(
            {
                **common(),
                "budget_id": f"BUD4193_DTXI_cGamma_{c_gamma:.0e}",
                "channel": "D_t Xi_0",
                "assumed_abs_cGamma": f"{c_gamma:.16g}",
                "profile_limit": f"{dt_bound:.16g}",
                "profile_units": "yr^-1",
                "residual_source_budget": f"mu_Xi[yr^-1] * T_res[yr] * {dt_bound:.16g}",
                "budget_units": "yr^-1",
                "assumption": "quasi-static residual response |D_t Xi_res| <= |Xi_res|/T_res and |Xi_res| <= |J_res|/mu_Xi",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(
            {
                **common(),
                "budget_id": f"BUD4193_GRADXI_cGamma_{c_gamma:.0e}",
                "channel": "L_loc grad_perp Xi_0",
                "assumed_abs_cGamma": f"{c_gamma:.16g}",
                "profile_limit": f"{grad_bound:.16g}",
                "profile_units": "dimensionless",
                "residual_source_budget": f"mu_Xi[yr^-1] * (L_res/L_loc) * {grad_bound:.16g}",
                "budget_units": "yr^-1",
                "assumption": "elliptic residual response L_loc|grad Xi_res| <= (L_loc/L_res)|J_res|/mu_Xi",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.extend(
        [
            {
                **common(),
                "budget_id": "BUD4193_SYMBOLIC_DTXI",
                "channel": "D_t Xi_0",
                "assumed_abs_cGamma": "|c_Gamma|",
                "profile_limit": "2.42e-14 / |c_Gamma|",
                "profile_units": "yr^-1",
                "residual_source_budget": "mu_Xi[yr^-1] * T_res[yr] * 2.42e-14 / |c_Gamma|",
                "budget_units": "yr^-1",
                "assumption": "symbolic Gdot residual-source budget",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            },
            {
                **common(),
                "budget_id": "BUD4193_SYMBOLIC_GRADXI",
                "channel": "L_loc grad_perp Xi_0",
                "assumed_abs_cGamma": "|c_Gamma|",
                "profile_limit": "4e-9 / |c_Gamma|",
                "profile_units": "dimensionless",
                "residual_source_budget": "mu_Xi[yr^-1] * (L_res/L_loc) * 4e-9 / |c_Gamma|",
                "budget_units": "yr^-1",
                "assumption": "symbolic preferred-location residual-source budget",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            },
        ]
    )
    return rows


def support_power_bound_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "SUP4193_0_power_form",
            "S_cg = U_B^nS S_*, m_L = m_* + U_B^nL m_tilde",
            "imports projected-source theorem form without claiming parent derivation",
            "J_res = U_B^(1+nS) S_* + D_m Delta_h(U_B^nL m_tilde) - D_t(U_B^nL m_tilde) + boundary_in",
            "conditional",
        ),
        (
            "SUP4193_1_classifier_derivatives",
            "if D_t U_B=O(U_B/T_B) and grad U_B=O(U_B/L_B), then derivatives preserve the U_B^nL power",
            "prevents classifier gradients from losing a local-safety power",
            "D_t m_L=O(U_B^nL/T_B), Delta_h m_L=O(U_B^nL/L_B^2)",
            "conditional",
        ),
        (
            "SUP4193_2_residual_norm",
            "||J_res|| <= U_B^(1+nS) A_S + D_m U_B^nL A_L/L_B^2 + U_B^nL A_t/T_B + A_bdy",
            "finite-margin residual-source bound",
            "compare this to the budgets in P8_Y5_R2FR_4193_FINITE_PROFILE_BUDGET.csv",
            "derived_bound_form",
        ),
        (
            "SUP4193_3_exact_limit",
            "U_B=0, S_cg|local=0, m_L=m_*, D_t m_*=0, Delta_h m_*=0, A_bdy=0",
            "exact projector-zero limit",
            "J_res=0 and delta Xi=0",
            "not parent-signed",
        ),
        (
            "SUP4193_4_current_verdict",
            "power-counting bound is available, but nS/nL/A terms are not parent-owned here",
            "keeps this as a gate rather than a claim",
            "next step must derive support powers or fill numeric profile rows",
            "open",
        ),
    ]
    return [
        {
            **common(),
            "support_id": support_id,
            "condition": condition,
            "role": role,
            "bound_or_result": bound_or_result,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for support_id, condition, role, bound_or_result, status in entries
    ]


def scenario_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "SCEN4193_exact_projector_zero",
            "P_loc J_res=0 term-by-term; Xi_star stationary/homogeneous; boundary routed",
            "exact zero conditional",
            "D_t Xi_0=0 and grad_perp Xi_0=0",
            "not parent-signed",
        ),
        (
            "SCEN4193_strong_support_finite",
            "S_cg=U_B^nS S_*, m_L=m_*+U_B^nL m_tilde, derivatives preserve powers, boundary suppressed",
            "finite-margin branch",
            "J_res can pass if its bound is below both 4193 budgets",
            "requires sourced nS/nL/amplitudes",
        ),
        (
            "SCEN4193_logistic_only_fail",
            "Pi_B close to one but S_cg and m_L derivatives are not support-suppressed",
            "failure mode",
            "U_B alone is not enough; local source can still exceed Gdot/xi budgets",
            "active warning",
        ),
        (
            "SCEN4193_boundary_incoming_open",
            "source powers hold but boundary_in is unsuppressed or incoming",
            "open/fail mode",
            "positive Hessian does not erase a driven boundary mode",
            "requires boundary theorem or bound",
        ),
    ]
    return [
        {
            **common(),
            "scenario_id": scenario_id,
            "assumptions": assumptions,
            "classification": classification,
            "outcome": outcome,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for scenario_id, assumptions, classification, outcome, status in entries
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "Jres_exact_zero_closed": "False",
            "projector_zero_contract_written": "True",
            "finite_green_budget_written": "True",
            "support_power_bound_form_written": "True",
            "numeric_parent_profile_values_available": "False",
            "public_local_GR_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4193_0_no_cancellation_claim",
            "Do not claim J_res=0 by cancellation between unrelated source, attractor and boundary terms.",
        ),
        (
            "FW4193_1_no_logistic_only_claim",
            "Pi_B close to one is not enough unless S_cg, m_L derivatives and boundary input are support-suppressed or bounded.",
        ),
        (
            "FW4193_2_no_profile_bound_as_exact_zero",
            "A finite Green-function profile bound is not the same as exact local scalar-memory silence.",
        ),
        (
            "FW4193_3_no_public_local_GR",
            "No public local-GR/PPN claim until J_res, Xi_star drift/gradient and c_Gamma product bounds are all closed with source-owned rows.",
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
    return [
        {
            **common(),
            "decision": DECISION,
            "Jres_decomposition_written": "True",
            "projector_zero_contract_written": "True",
            "finite_profile_budget_rows": str(len(finite_profile_budget_rows())),
            "support_power_bound_form_written": "True",
            "exact_zero_lemma_closed": "False",
            "finite_profile_gate_ready": "True",
            "public_local_GR_claim_allowed": "False",
            "formal_209_written": str(FORMAL_209_PATH.exists()),
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
            "why": "4193 gives the exact J_res zero contract and finite Green-profile budget, but the support powers nS/nL and residual amplitudes are still not parent-owned.",
            "route_A": "derive S_cg=U_B^nS S_* and m_L=m_*+U_B^nL m_tilde from the local fixed-point/source-support theorem",
            "route_B": "fill numeric or bounded J_res, T_res, L_res, mu_Xi values and compare to 4193 budgets",
            "recommended_first": "source-support powers for J_res",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc_text() -> str:
    return f"""# 209 - PPC4161 Residual Source Projector And Xi Profile Amplitude Bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, PPN safety, or exact scalar-memory silence. It derives the exact residual-source projector contract and the finite Green-function profile budget that must be passed if exact silence is not proved.

## Residual Source

From 4192:

```text
delta Xi = L_Xi^-1 J_res,
L_Xi = -D_Xi Delta_h + mu_Xi,

J_res =
  [1 - Pi_B] S_cg
  + D_m Delta_h m_L
  - D_t m_L
  + boundary_in.
```

The exact local zero route is:

```text
P_loc J_res = 0
```

term by term, not by tuned cancellation.

## Term-by-Term Zero Contract

```text
P_loc([1 - Pi_B] S_cg) = 0
P_loc(D_m Delta_h m_L) = 0
P_loc(D_t m_L) = 0
P_loc(boundary_in) = 0 or Hamiltonian-routed.
```

If those hold, and `Xi_star` is stationary/homogeneous, then:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0.
```

## Finite Bound Branch

If a residual source survives, the Green-function branch is:

```text
||delta Xi|| <= ||L_Xi^-1|| ||J_res||,
||L_Xi^-1|| <= 1/mu_Xi
```

in the lowest-mode norm when `mu_Xi>0`.

For a residual time scale `T_res`:

```text
|D_t Xi_res| <= |J_res|/(mu_Xi T_res).
```

For a residual spatial scale `L_res`:

```text
L_loc |grad_perp Xi_res|
  <= (L_loc/L_res) |J_res|/mu_Xi.
```

Thus the source budgets are:

```text
|J_res| <= mu_Xi T_res * 2.42e-14 / |c_Gamma|      yr^-1
|J_res| <= mu_Xi (L_res/L_loc) * 4e-9 / |c_Gamma| yr^-1.
```

Both must pass unless the exact zero contract closes.

## Source-Support Power Form

The clean finite-margin theorem form is:

```text
U_B = 1 - Pi_B,
S_cg = U_B^nS S_*,
m_L = m_* + U_B^nL m_tilde.
```

If classifier derivatives preserve powers:

```text
D_t U_B = O(U_B/T_B),
grad U_B = O(U_B/L_B),
```

then:

```text
||J_res|| <=
  U_B^(1+nS) A_S
  + D_m U_B^nL A_L/L_B^2
  + U_B^nL A_t/T_B
  + A_bdy.
```

That is now the concrete quantity to derive or fill.

## Verdict

The exact zero proof is still open. But the route is now sharp:

```text
prove P_loc J_res=0
```

or:

```text
bound J_res below both 4193 Green-profile budgets.
```

## Next Gate

`{NEXT_TARGET}` should derive the source-support powers `nS/nL` for `J_res`, or fill numeric/symbolic `J_res`, `T_res`, `L_res`, and `mu_Xi` rows.
"""


def checkpoint_doc_text() -> str:
    return f"""# 4193 - Residual Source Projector And Xi Profile Amplitude Bound

Generated by: `post-checkpoint-work/scripts/Y5_R2FR_4193_residual_source_projector_Xi_profile_bound.py`

## Summary

4193 attacks the exact residual source left by 4192:

```text
J_res = [1 - Pi_B] S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

It writes the term-by-term projector-zero contract and the finite Green-function budget if any term survives.

## Main Result

Exact zero requires:

```text
P_loc J_res = 0
```

term by term. Otherwise:

```text
|J_res| <= mu_Xi T_res * 2.42e-14 / |c_Gamma|      yr^-1
|J_res| <= mu_Xi (L_res/L_loc) * 4e-9 / |c_Gamma| yr^-1.
```

The finite-margin power-counting form is:

```text
||J_res|| <=
  U_B^(1+nS) A_S
  + D_m U_B^nL A_L/L_B^2
  + U_B^nL A_t/T_B
  + A_bdy.
```

## Decision

`{DECISION}`
"""


def ensure_docs() -> None:
    FORMAL_209_PATH.write_text(formal_doc_text(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc_text(), encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The residual scalar-memory source J_res now has a term-by-term projector-zero contract and finite Green-profile source budgets tied to the 4190 Gdot and preferred-location limits.",
            "current_evidence": "4193 residual decomposition, projector-zero contract, support-power bound form, finite profile budget rows, scenario ledger and nonclaim firewall.",
            "status": "private_Jres_projector_budget_nonclaim_source_support_powers_open",
            "next_test": "Derive source-support powers nS/nL for J_res or fill numeric J_res, mu_Xi, T_res and L_res rows against the 4193 budgets.",
            "key_risk": "Pi_B near one or a positive minimizer can be mistaken for local-GR recovery even when residual source, attractor drift, or boundary input survives.",
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "appended"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4193 Residual Source Projector And Xi Profile Bound

Marker: `{PACKET_MARKER}`

4193 isolates the remaining scalar-memory residual:

```text
J_res = [1 - Pi_B] S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

Exact local silence requires `P_loc J_res=0` term by term. If not, the Green-profile budgets are:

```text
|J_res| <= mu_Xi T_res * 2.42e-14 / |c_Gamma|      yr^-1
|J_res| <= mu_Xi (L_res/L_loc) * 4e-9 / |c_Gamma| yr^-1.
```
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "appended"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Residual Source Projector And Xi Profile Bound

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4193 turns the 4192 residual into a concrete projector/budget gate:

```text
J_res = [1 - Pi_B] S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

Exact local scalar-memory silence needs:

```text
P_loc J_res = 0
```

term by term. If any term survives:

```text
|J_res| <= mu_Xi T_res * 2.42e-14 / |c_Gamma|      yr^-1
|J_res| <= mu_Xi (L_res/L_loc) * 4e-9 / |c_Gamma| yr^-1.
```

Current verdict: zero not closed; finite Green-profile budget ready; next target is deriving source-support powers or filling profile amplitudes.
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "appended"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source_register = rows_by_name["P8_Y5_R2FR_4193_SOURCE_REGISTER"]
    decomposition = rows_by_name["P8_Y5_R2FR_4193_JRES_DECOMPOSITION"]
    projector = rows_by_name["P8_Y5_R2FR_4193_PROJECTOR_ZERO_CONTRACT"]
    budget = rows_by_name["P8_Y5_R2FR_4193_FINITE_PROFILE_BUDGET"]
    support = rows_by_name["P8_Y5_R2FR_4193_SUPPORT_POWER_BOUND_FORM"]
    status = rows_by_name["P8_Y5_R2FR_4193_STATUS"][0]
    all_generated_rows = [
        row
        for name, rows in rows_by_name.items()
        if name != "P8_Y5_R2FR_4193_SOURCE_REGISTER"
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4193_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source_register), str(source_register)),
        ("VAL4193_1_source_tokens", "all source tokens found", all(row["required_text_found"] == "True" for row in source_register), str(source_register)),
        ("VAL4193_2_decomposition", "J_res decomposition includes all four terms", all(any(token in row["term"] for row in decomposition) for token in ["S_cg", "Delta_h m_L", "D_t m_L", "boundary_in"]), str(decomposition)),
        ("VAL4193_3_projector_contract", "projector zero contract is term-by-term", any(row["condition"] == "P_loc J_res = 0" for row in projector) and any("cancellation" in row["condition"] for row in projector), str(projector)),
        ("VAL4193_4_budget_rows", "finite profile budget has symbolic and numeric Gdot/gradient rows", len(budget) >= 12 and any(row["budget_id"] == "BUD4193_SYMBOLIC_DTXI" for row in budget) and any(row["budget_id"] == "BUD4193_SYMBOLIC_GRADXI" for row in budget), str(budget)),
        ("VAL4193_5_budget_limits", "budget limits include 2.42e-14 and 4e-9", any("2.42e-14" in row["profile_limit"] or "2.42e-14" in row["residual_source_budget"] for row in budget) and any("4e-9" in row["profile_limit"] or "4e-9" in row["residual_source_budget"] for row in budget), str(budget)),
        ("VAL4193_6_support_bound", "support power residual bound form is written", any("U_B^(1+nS)" in row["bound_or_result"] for row in support) and any("U_B^nL" in row["bound_or_result"] for row in support), str(support)),
        ("VAL4193_7_nonclaim_status", "exact zero remains open and public claim false", status["exact_zero_lemma_closed"] == "False" and status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4193_8_formal_209", "formal 209 exists with marker", FORMAL_209_PATH.exists() and SPINE_MARKER in read_text(FORMAL_209_PATH), str(FORMAL_209_PATH)),
        ("VAL4193_9_checkpoint_doc", "checkpoint doc exists with decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4193_10_claim_row", "claim register contains L-034", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4193_11_packet_180", "packet marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4193_12_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4193_13_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
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
            "check_id": "VAL4193_14_py_compile",
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
        "P8_Y5_R2FR_4193_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4193_JRES_DECOMPOSITION": residual_decomposition_rows(),
        "P8_Y5_R2FR_4193_PROJECTOR_ZERO_CONTRACT": projector_zero_contract_rows(),
        "P8_Y5_R2FR_4193_FINITE_PROFILE_BUDGET": finite_profile_budget_rows(),
        "P8_Y5_R2FR_4193_SUPPORT_POWER_BOUND_FORM": support_power_bound_rows(),
        "P8_Y5_R2FR_4193_SCENARIOS": scenario_rows(),
        "P8_Y5_R2FR_4193_DECISION": decision_rows(),
        "P8_Y5_R2FR_4193_CLAIM_FIREWALL": claim_firewall_rows(),
        "P8_Y5_R2FR_4193_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4193_NEXT_TARGET": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(SOURCE_DIR / f"{name}.csv", rows)

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4193_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4193 validation failed: {failed}")

    print(DECISION)
    print(f"formal={FORMAL_209_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
