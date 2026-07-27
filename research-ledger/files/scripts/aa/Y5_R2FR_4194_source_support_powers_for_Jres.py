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

CHECKPOINT = "4194"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_SUPPORT_POWERS_FOR_JRES_4194"
DECISION = (
    "JRES_SOURCE_SUPPORT_POWERS_N1_N2_CONDITIONALLY_DERIVED_FROM_FIXED_POINT_PARITY_"
    "GDOT_AMPLITUDE_BUDGET_REMAINS_HARD_NONCLAIM"
)
DOC_PATH = POST / "4194-Y5-R2FR-source-support-powers-for-Jres-or-numeric-profile-fill.md"
FORMAL_210_PATH = FORMAL / "210-PPC4161-source-support-powers-for-Jres.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-035"
SPINE_MARKER = "PPC4161_SOURCE_SUPPORT_POWERS_FOR_JRES_4194"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_SUPPORT_POWERS_FOR_JRES_4194"
NEXT_TARGET = "4195-Y5-R2FR-parent-ZL-parity-signature-or-Jres-numeric-profile-smoke.md"

STRONG_UB = 3.7965595357794454e-7
WEAK_UB = 1e-4
CGAMMA_VALUES = [1.0, 1e-3, 1e-6]

SOURCES = {
    "SRC4194_00_4193_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4193_NEXT_TARGET.csv",
        "source-support powers for J_res",
        "4193 selected source-support powers for J_res.",
    ),
    "SRC4194_01_4193_support": (
        SOURCE_DIR / "P8_Y5_R2FR_4193_SUPPORT_POWER_BOUND_FORM.csv",
        "U_B^(1+nS) A_S",
        "4193 support-power bound form.",
    ),
    "SRC4194_02_4193_budget": (
        SOURCE_DIR / "P8_Y5_R2FR_4193_FINITE_PROFILE_BUDGET.csv",
        "BUD4193_SYMBOLIC_DTXI",
        "4193 Green-profile budgets.",
    ),
    "SRC4194_03_123_doc": (
        FORMAL / "123-local-source-power-theorem.md",
        "local_source_power_theorem_form_constructed_not_parent_derived",
        "local source-power theorem status.",
    ),
    "SRC4194_04_123_conditions": (
        FORMAL / "runs" / "20260528-140716-local-source-power-theorem" / "results" / "theorem_conditions.csv",
        "S_cg(0,Y)=0 and S_cg is C1 in D_L",
        "source-power theorem condition table.",
    ),
    "SRC4194_05_123_powers": (
        FORMAL / "runs" / "20260528-140716-local-source-power-theorem" / "results" / "power_laws.csv",
        "S_cg(D_L,Y)=D_L S_1(D_L,Y)+O(D_L^2)",
        "source-power theorem power laws.",
    ),
    "SRC4194_06_125_invariant": (
        FORMAL / "125-local-leakage-vector-invariant.md",
        "D_L <= U_B",
        "leakage-vector candidate with algebraic D_L bound.",
    ),
    "SRC4194_07_125_results": (
        FORMAL / "runs" / "20260528-154725-local-leakage-vector-invariant" / "results" / "invariant_construction.csv",
        "D_L <= U_B",
        "candidate invariant construction result.",
    ),
    "SRC4194_08_126_evenness": (
        FORMAL / "126-scalar-evenness-origin.md",
        "scalar_evenness_origin_parity_candidate_not_parent_derived",
        "scalar evenness/parity origin status.",
    ),
    "SRC4194_09_130_repair": (
        FORMAL / "130-smooth-scalar-channel-repair.md",
        "D_L <= U_B",
        "smooth scalar repair closure precedent.",
    ),
    "SRC4194_10_75_projected": (
        FORMAL / "75-projected-source-laws.md",
        "nS = 1",
        "projected source-law minimal integer orders.",
    ),
    "SRC4194_11_77_sigma": (
        FORMAL / "77-sigma-L-source-silence-theorem.md",
        "It cannot be inferred from `Pi_B` alone.",
        "sigma-L theorem warning.",
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


def power_theorem_import_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "IMP4194_0_fixed_point_distance",
            "D_L = U_B H_L(X_B), with bounded H_L",
            "D_L <= C_D U_B",
            "candidate/closure; H_L bound not parent-derived",
            "lets D_L powers become U_B powers",
        ),
        (
            "IMP4194_1_source_power",
            "S_cg(D_L,Y)=D_L S_1(D_L,Y)+O(D_L^2)",
            "nS = 1",
            "conditional theorem form; source parity/support silence not parent-derived",
            "U_B S_cg = O(U_B^2)",
        ),
        (
            "IMP4194_2_attractor_power",
            "m_L(D_L,Y)=m_*+0.5 m_2(Y)D_L^2+O(D_L^3)",
            "nL = 2",
            "conditional theorem form; scalar evenness/extremality not parent-derived",
            "D_t m_L and Delta_h m_L can be O(U_B^2) if gradients preserve powers",
        ),
        (
            "IMP4194_3_gradient_power",
            "D_t U_B=O(U_B/T_B), grad U_B=O(U_B/L_B), Delta_h U_B=O(U_B/L_B^2)",
            "derivatives preserve nL=2",
            "far-local conditional; transition shell still open",
            "J_res attractor terms remain O(U_B^2)",
        ),
        (
            "IMP4194_4_boundary_power",
            "boundary_in = O(U_B^2 A_bdy) or boundary_in=0/routed",
            "nB >= 2 or exact boundary silence",
            "not parent-derived",
            "prevents boundary from dominating J_res",
        ),
    ]
    return [
        {
            **common(),
            "import_id": import_id,
            "imported_condition": imported_condition,
            "power_result": power_result,
            "current_status": current_status,
            "effect_on_Jres": effect_on_Jres,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for import_id, imported_condition, power_result, current_status, effect_on_Jres in entries
    ]


def jres_power_derivation_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "JPOW4194_0_source_term",
            "U_B S_cg",
            "S_cg=O(D_L), D_L<=C_D U_B",
            "O(U_B^2)",
            "nJ_source = 2",
            "conditional",
        ),
        (
            "JPOW4194_1_attractor_laplacian",
            "D_m Delta_h m_L",
            "m_L-m_*=O(D_L^2), D_L<=C_D U_B, derivative powers preserved",
            "O(D_m U_B^2/L_B^2)",
            "nJ_laplacian = 2",
            "conditional",
        ),
        (
            "JPOW4194_2_attractor_drift",
            "-D_t m_L",
            "m_L-m_*=O(D_L^2), D_L<=C_D U_B, time derivative powers preserved",
            "O(U_B^2/T_B)",
            "nJ_drift = 2",
            "conditional",
        ),
        (
            "JPOW4194_3_boundary",
            "boundary_in",
            "boundary zero/routed or O(U_B^2)",
            "0 or O(U_B^2 A_bdy)",
            "nJ_boundary >= 2 required",
            "open",
        ),
        (
            "JPOW4194_4_total",
            "J_res",
            "all above clauses plus no cross-term cancellation",
            "||J_res|| <= U_B^2 A_J + A_bdy_open",
            "nJ_total = 2 if boundary suppressed",
            "conditional_not_parent_claim",
        ),
    ]
    return [
        {
            **common(),
            "power_id": power_id,
            "term": term,
            "assumptions": assumptions,
            "derived_order": derived_order,
            "jres_power": jres_power,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for power_id, term, assumptions, derived_order, jres_power, status in entries
    ]


def normalized_budget_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for window_id, ub in [("strong_local", STRONG_UB), ("weaker_local", WEAK_UB)]:
        ub2 = ub * ub
        for c_gamma in CGAMMA_VALUES:
            gdot_budget = 2.42e-14 / c_gamma
            grad_budget = 4.0e-9 / c_gamma
            rows.append(
                {
                    **common(),
                    "budget_id": f"NB4194_{window_id}_Gdot_cGamma_{c_gamma:.0e}",
                    "window": window_id,
                    "U_B": f"{ub:.16g}",
                    "U_B_squared": f"{ub2:.16g}",
                    "channel": "D_t Xi_0",
                    "assumed_abs_cGamma": f"{c_gamma:.16g}",
                    "profile_limit": f"{gdot_budget:.16g}",
                    "required_AJ_multiplier": f"{gdot_budget / ub2:.16g}",
                    "multiplier_units": "mu_Xi*T_res",
                    "interpretation": "If ||J_res||=U_B^2 A_J and A_bdy=0, then A_J must be <= required_AJ_multiplier*(mu_Xi*T_res).",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            rows.append(
                {
                    **common(),
                    "budget_id": f"NB4194_{window_id}_gradXi_cGamma_{c_gamma:.0e}",
                    "window": window_id,
                    "U_B": f"{ub:.16g}",
                    "U_B_squared": f"{ub2:.16g}",
                    "channel": "L_loc grad_perp Xi_0",
                    "assumed_abs_cGamma": f"{c_gamma:.16g}",
                    "profile_limit": f"{grad_budget:.16g}",
                    "required_AJ_multiplier": f"{grad_budget / ub2:.16g}",
                    "multiplier_units": "mu_Xi*(L_res/L_loc)",
                    "interpretation": "If ||J_res||=U_B^2 A_J and A_bdy=0, then A_J must be <= required_AJ_multiplier*(mu_Xi*L_res/L_loc).",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
    return rows


def parent_signature_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "PSIG4194_0_D_L_bound",
            "D_L<=C_D U_B",
            "candidate algebraic if Z_L=U_B H_L and H_L bounded",
            "candidate_not_parent_derived",
            "derive H_L from universal coarse-grained variables and prove boundedness",
        ),
        (
            "PSIG4194_1_source_parity",
            "S_cg is odd/linear in signed leakage coordinates or support-silent",
            "125/126 give theorem shape, not parent origin",
            "not_parent_derived",
            "derive signed leakage coordinates and source parity from parent/coarse-graining",
        ),
        (
            "PSIG4194_2_scalar_evenness",
            "m_L depends on leakage only through even scalar s_L",
            "126 gives parity theorem form",
            "not_parent_derived",
            "derive leakage-frame reflection/isotropy or environmental variational extremum",
        ),
        (
            "PSIG4194_3_gradient_preservation",
            "D_t U_B, grad U_B and Delta_h U_B preserve powers in far-local tested systems",
            "131 gives far-local conditional, transition shell open",
            "conditional_transition_open",
            "derive or bound transition-shell q/current separately",
        ),
        (
            "PSIG4194_4_boundary_power",
            "boundary_in=0/routed or O(U_B^2)",
            "192 gives private selector precedent only",
            "boundary_open",
            "derive parent no-flux/domain theorem or fill boundary amplitude",
        ),
        (
            "PSIG4194_5_current_verdict",
            "J_res=O(U_B^2)",
            "valid as a conditional fixed-point/parity route",
            "conditional_not_claim",
            "compare to budgets or parent-sign the parity/source-support theorem",
        ),
    ]
    return [
        {
            **common(),
            "signature_id": signature_id,
            "needed_clause": needed_clause,
            "current_evidence": current_evidence,
            "status": status,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for signature_id, needed_clause, current_evidence, status, next_action in entries
    ]


def scenario_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "SCEN4194_exact_parent_signed",
            "D_L bound, source parity, scalar evenness, gradient preservation and boundary silence all parent-signed",
            "J_res=O(U_B^2) and exact zero in U_B=0 limit",
            "not current state",
        ),
        (
            "SCEN4194_conditional_strong_local",
            "U_B=3.7965595357794454e-7, nJ=2, order-one effective amplitudes, A_bdy=0",
            "gradient budget easy; Gdot budget requires A_J <= 0.168*(mu_Xi*T_res)/|c_Gamma|",
            "promising but amplitude/time-scale dependent",
        ),
        (
            "SCEN4194_weaker_margin",
            "U_B=1e-4, nJ=2, order-one effective amplitudes, A_bdy=0",
            "Gdot budget becomes extremely hard for |c_Gamma|~1; gradient budget still possible",
            "requires stronger amplitudes, smaller c_Gamma, larger mu_Xi*T_res, or exact zero",
        ),
        (
            "SCEN4194_logistic_only",
            "Pi_B close to one but no source parity/evenness",
            "only explicit U_B factor is insufficient; m_L drift can dominate",
            "fail/open",
        ),
        (
            "SCEN4194_boundary_unsuppressed",
            "nS/nL powers hold but boundary_in is O(1)",
            "J_res is dominated by boundary input and local silence fails",
            "requires boundary theorem or bound",
        ),
    ]
    return [
        {
            **common(),
            "scenario_id": scenario_id,
            "assumptions": assumptions,
            "outcome": outcome,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for scenario_id, assumptions, outcome, status in entries
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "nS_conditional": "1",
            "nL_conditional": "2",
            "nJ_conditional": "2",
            "source_power_parent_derived": "False",
            "Jres_exact_zero_closed": "False",
            "normalized_budget_rows_written": "True",
            "public_local_GR_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4194_0_no_parent_overclaim",
            "Do not claim nS=1/nL=2 are parent-derived; they are conditional on fixed-point/parity/evenness clauses.",
        ),
        (
            "FW4194_1_no_UB2_victory",
            "Do not treat J_res=O(U_B^2) as automatically enough for Gdot; amplitude and time-scale multipliers still matter.",
        ),
        (
            "FW4194_2_no_transition_shell_claim",
            "Far-local gradient preservation does not prove transition-shell safety.",
        ),
        (
            "FW4194_3_no_boundary_erasure",
            "Boundary input must be zero/routed or bounded; source powers do not erase incoming boundary modes.",
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
            "power_theorem_import_written": "True",
            "Jres_power_derivation_written": "True",
            "nS_conditional": "1",
            "nL_conditional": "2",
            "nJ_conditional": "2",
            "normalized_budget_rows": str(len(normalized_budget_rows())),
            "parent_signature_complete": "False",
            "exact_zero_lemma_closed": "False",
            "public_local_GR_claim_allowed": "False",
            "formal_210_written": str(FORMAL_210_PATH.exists()),
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
            "why": "4194 conditionally gives J_res=O(U_B^2), but the parent still has to sign the Z_L parity/evenness clauses or the budget must be filled with numeric mu_Xi, T_res, L_res and amplitudes.",
            "route_A": "derive signed leakage coordinates, source parity, scalar evenness and H_L boundedness from parent/coarse-graining",
            "route_B": "run a normalized J_res profile smoke with chosen mu_Xi*T_res and L_res/L_loc assumptions to see whether the Gdot budget is plausible",
            "recommended_first": "parent Z_L parity signature",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc_text() -> str:
    return f"""# 210 - PPC4161 Source-Support Powers For Jres

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, PPN safety, or exact scalar-memory silence. It consolidates the older fixed-point/source-power theorem into the newer `J_res` gate.

## Imported Fixed-Point Power Theorem

The local source-power theorem gives the following conditional structure:

```text
D_L <= C_D U_B,
S_cg = D_L S_1 + O(D_L^2),
m_L = m_* + 1/2 m_2 D_L^2 + O(D_L^3).
```

Therefore:

```text
nS = 1,
nL = 2.
```

These are not parent-derived yet. They require:

```text
source silence/parity,
scalar evenness or fixed-point extremality,
bounded H_L in D_L=U_B H_L,
far-local derivative power preservation,
boundary silence or routing.
```

## Jres Power Result

4193 defined:

```text
J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

Under the conditional fixed-point/parity route:

```text
U_B S_cg = O(U_B^2),
D_m Delta_h m_L = O(D_m U_B^2/L_B^2),
D_t m_L = O(U_B^2/T_B).
```

If the boundary term is also zero/routed or `O(U_B^2)`, then:

```text
J_res = O(U_B^2).
```

That is the cleanest finite-margin route currently available.

## Budget Reality Check

The 4193 budgets say:

```text
|J_res| <= mu_Xi T_res * 2.42e-14 / |c_Gamma|      yr^-1
|J_res| <= mu_Xi (L_res/L_loc) * 4e-9 / |c_Gamma| yr^-1.
```

For the strong local window:

```text
U_B = {STRONG_UB:.16g},
U_B^2 = {STRONG_UB * STRONG_UB:.16g}.
```

So if `J_res = U_B^2 A_J` and `|c_Gamma|=1`, the Gdot channel requires roughly:

```text
A_J <= {(2.42e-14 / (STRONG_UB * STRONG_UB)):.16g} * (mu_Xi T_res).
```

The gradient channel is much looser:

```text
A_J <= {(4e-9 / (STRONG_UB * STRONG_UB)):.16g} * (mu_Xi L_res/L_loc).
```

So the next hard target is not just the power `U_B^2`; it is the amplitude/time-scale normalization.

## Verdict

4194 narrows the local branch:

```text
nS = 1,
nL = 2,
nJ = 2
```

as a conditional fixed-point/parity route. It does not claim parent derivation.

## Next Gate

`{NEXT_TARGET}` should either parent-sign the `Z_L` parity/evenness route, or run a normalized `J_res` profile smoke against the 4194 budget multipliers.
"""


def checkpoint_doc_text() -> str:
    return f"""# 4194 - Source-Support Powers For Jres Or Numeric Profile Fill

Generated by: `post-checkpoint-work/scripts/Y5_R2FR_4194_source_support_powers_for_Jres.py`

## Summary

4194 consolidates the older fixed-point source-power theorem into the newer 4193 residual-source gate:

```text
J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

## Result

Conditional powers:

```text
nS = 1,
nL = 2,
nJ = 2
```

provided:

```text
D_L <= C_D U_B,
S_cg = O(D_L),
m_L - m_* = O(D_L^2),
derivatives preserve U_B powers,
boundary_in = 0/routed or O(U_B^2).
```

This is not parent-derived yet.

## Budget Warning

`J_res=O(U_B^2)` is useful, but not automatically enough. For the strong local window and `|c_Gamma|=1`, the Gdot channel requires:

```text
A_J <= {(2.42e-14 / (STRONG_UB * STRONG_UB)):.16g} * (mu_Xi T_res).
```

## Decision

`{DECISION}`
"""


def ensure_docs() -> None:
    FORMAL_210_PATH.write_text(formal_doc_text(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc_text(), encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The J_res source-support powers consolidate to nS=1, nL=2 and nJ=2 under the fixed-point/parity route, but the route remains conditional and the Gdot amplitude budget is still hard.",
            "current_evidence": "4194 power-theorem import, Jres power derivation, normalized budget multipliers, parent-signature audit, scenario ledger and nonclaim firewall.",
            "status": "private_conditional_Jres_power_law_nonclaim_parent_parity_signature_open",
            "next_test": "Parent-sign Z_L parity/evenness and H_L boundedness, or fill numeric mu_Xi, T_res, L_res and A_J rows against the 4194 budgets.",
            "key_risk": "Using U_B^2 power counting as a local-GR proof would hide amplitude, transition-gradient and boundary failures.",
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "appended"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4194 Source-Support Powers For Jres

Marker: `{PACKET_MARKER}`

4194 consolidates the conditional fixed-point/parity source powers:

```text
nS = 1,
nL = 2,
nJ = 2.
```

This gives:

```text
J_res = O(U_B^2)
```

only if source parity, scalar evenness, gradient preservation and boundary routing are accepted or derived. It is not yet a parent-derived local-GR proof.
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "appended"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Source-Support Powers For Jres

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4194 folds the older source-power theorem into the newer residual-source gate:

```text
J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

Conditional fixed-point/parity powers:

```text
nS = 1,
nL = 2,
nJ = 2.
```

Current verdict: useful finite-margin power law, not parent-derived; Gdot budget still requires amplitude/time-scale control even when `J_res=O(U_B^2)`.
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "appended"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source_register = rows_by_name["P8_Y5_R2FR_4194_SOURCE_REGISTER"]
    imports = rows_by_name["P8_Y5_R2FR_4194_POWER_THEOREM_IMPORT"]
    powers = rows_by_name["P8_Y5_R2FR_4194_JRES_POWER_DERIVATION"]
    budget = rows_by_name["P8_Y5_R2FR_4194_NORMALIZED_BUDGET_REQUIREMENTS"]
    signature = rows_by_name["P8_Y5_R2FR_4194_PARENT_SIGNATURE_AUDIT"]
    status = rows_by_name["P8_Y5_R2FR_4194_STATUS"][0]
    all_generated_rows = [
        row
        for name, rows in rows_by_name.items()
        if name != "P8_Y5_R2FR_4194_SOURCE_REGISTER"
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4194_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source_register), str(source_register)),
        ("VAL4194_1_source_tokens", "all source tokens found", all(row["required_text_found"] == "True" for row in source_register), str(source_register)),
        ("VAL4194_2_import_powers", "imports include nS=1 and nL=2", any(row["power_result"] == "nS = 1" for row in imports) and any(row["power_result"] == "nL = 2" for row in imports), str(imports)),
        ("VAL4194_3_Jres_power", "Jres derivation reaches nJ=2 conditionally", any(row["jres_power"] == "nJ_total = 2 if boundary suppressed" for row in powers), str(powers)),
        ("VAL4194_4_budget_rows", "normalized budget rows cover strong and weak windows", len(budget) == 12 and {row["window"] for row in budget} == {"strong_local", "weaker_local"}, str(budget)),
        ("VAL4194_5_Gdot_hard_budget", "strong local Gdot multiplier is finite and below one for cGamma=1", any(row["budget_id"] == "NB4194_strong_local_Gdot_cGamma_1e+00" and float(row["required_AJ_multiplier"]) < 1.0 for row in budget), str(budget)),
        ("VAL4194_6_parent_open", "parent signature audit remains open", any(row["status"] in {"not_parent_derived", "boundary_open", "conditional_transition_open"} for row in signature) and status["parent_signature_complete"] == "False", str(signature)),
        ("VAL4194_7_nonclaim_status", "exact zero remains open and public claim false", status["exact_zero_lemma_closed"] == "False" and status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4194_8_formal_210", "formal 210 exists with marker", FORMAL_210_PATH.exists() and SPINE_MARKER in read_text(FORMAL_210_PATH), str(FORMAL_210_PATH)),
        ("VAL4194_9_checkpoint_doc", "checkpoint doc exists with decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4194_10_claim_row", "claim register contains L-035", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4194_11_packet_180", "packet marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4194_12_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4194_13_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
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
            "check_id": "VAL4194_14_py_compile",
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
        "P8_Y5_R2FR_4194_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4194_POWER_THEOREM_IMPORT": power_theorem_import_rows(),
        "P8_Y5_R2FR_4194_JRES_POWER_DERIVATION": jres_power_derivation_rows(),
        "P8_Y5_R2FR_4194_NORMALIZED_BUDGET_REQUIREMENTS": normalized_budget_rows(),
        "P8_Y5_R2FR_4194_PARENT_SIGNATURE_AUDIT": parent_signature_rows(),
        "P8_Y5_R2FR_4194_SCENARIOS": scenario_rows(),
        "P8_Y5_R2FR_4194_DECISION": decision_rows(),
        "P8_Y5_R2FR_4194_CLAIM_FIREWALL": claim_firewall_rows(),
        "P8_Y5_R2FR_4194_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4194_NEXT_TARGET": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(SOURCE_DIR / f"{name}.csv", rows)

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4194_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4194 validation failed: {failed}")

    print(DECISION)
    print(f"formal={FORMAL_210_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
