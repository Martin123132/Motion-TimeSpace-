from __future__ import annotations

import csv
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

CHECKPOINT = "4214"
CLAIM_ID = "L-055"
BRANCH_ID = "MTS_R2FR_Y5_PROJECTOR_STRESS_CURL_ZERO_4214"
DECISION = (
    "PROJECTOR_STRESS_CURL_ZERO_CONDITIONALLY_DERIVED_INSIDE_QBASIC_"
    "OBSERVED_COFRAME_HODGE_NO_WALL_SELECTOR_BOUND_ROW_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md"
DOC_PATH = POST / "4214-Y5-R2FR-projector-stress-curl-zero-or-first-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_PROJECTOR_STRESS_CURL_ZERO_4214"
PACKET_MARKER = "PPC4161_PACKET_PROJECTOR_STRESS_CURL_ZERO_4214"
NEXT_TARGET = "4215-Y5-R2FR-reference-lock-curl-zero-or-first-ref-bound-row.md"

SOURCES = {
    "SRC4214_00_4213_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4213_NEXT_TARGET.csv",
        "4214-Y5-R2FR-projector-stress-curl-zero-or-first-bound-row.md",
        "4213 selected projector stress as next curl obstruction.",
    ),
    "SRC4214_01_4212_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv",
        "I_projector",
        "4212 retained projector curl component.",
    ),
    "SRC4214_02_4089_projector": (
        SOURCE_DIR / "P8_Y5_R2FR_4089_PROJECTOR_ZERO_THEOREM.csv",
        "PD4089_1_qbasic_zero",
        "Projector/domain stress zero theorem.",
    ),
    "SRC4214_03_4177_projector": (
        SOURCE_DIR / "P8_Y5_R2FR_4177_PROJECTOR_RESIDUAL_CLOSE_OR_BOUND.csv",
        "PR4177_0_gamma_beta",
        "Private quotient-naturality projector closures.",
    ),
    "SRC4214_04_4208_hodge": (
        SOURCE_DIR / "P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv",
        "HZ4208_0_observed_coframe",
        "Observed coframe/Hodge descent contract.",
    ),
    "SRC4214_05_4205_coframe": (
        SOURCE_DIR / "P8_Y5_R2FR_4205_EH_COFRAME_SIGNATURE_GATE.csv",
        "SIG4205_0_same_coframe",
        "Same observed coframe gate.",
    ),
    "SRC4214_06_4121_source_readout": (
        SOURCE_DIR / "P8_Y5_R2FR_4121_SOURCE_READOUT_DESCENT_THEOREM.csv",
        "SDT4121_0_source_quotient_setup",
        "Source/readout descent theorem.",
    ),
    "SRC4214_07_4014_hodge_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
        "OHN4014_0_observed_Hodge_lock",
        "Observed Hodge owner theorem.",
    ),
    "SRC4214_08_229_formal": (
        FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md",
        "I_projector.",
        "4213 formal next target.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


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
    rows = []
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


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PCT4214_0_factorization",
            "projector stress factorization",
            "T_proj = T_P + T_domain + T_chi + T_wall + T_denominator",
            "imported_factor_split",
            "4089 splits every projector stress escape route before any zero is claimed",
        ),
        (
            "PCT4214_1_qbasic_projector",
            "q-basic/fixed projector",
            "If P_loc=P_bar(q) or fixed topological/readout label, then D_v P_loc=0 and delta_field P_loc has no independent curl.",
            "conditional_zero_theorem",
            "kills metric-projector and domain-motion stress for quotient-fibre variations",
        ),
        (
            "PCT4214_2_observed_coframe_hodge",
            "observed coframe/Hodge descent",
            "If e_obs=e_bar(q) and *_obs is fixed by g_obs plus orientation, then D_v e_obs=D_v *_obs=0.",
            "conditional_zero_theorem",
            "prevents the projector from re-entering through hidden Hodge/coframe dependence",
        ),
        (
            "PCT4214_3_source_readout_descent",
            "source/readout descent",
            "If M_obs, clock, orbital, EM and PPN readouts factor through q, projector readout has no vertical source current.",
            "conditional_zero_theorem",
            "protects against measured-GM or apparatus labels smuggling in projector stress",
        ),
        (
            "PCT4214_4_no_wall_denominator",
            "no wall/constraint/second denominator",
            "If selector multipliers, wall flux, STF wall stress and second projector denominator vanish or are boundary-routed, T_chi=T_wall=T_denominator=0.",
            "conditional_zero_theorem",
            "keeps active boundaries and denominators from being called projectors",
        ),
        (
            "PCT4214_5_curl_zero",
            "projector curl zero",
            "I_projector = int_S i_tau omega_projector = 0 under PCT4214_1 through PCT4214_4.",
            "conditional_zero_theorem",
            "closes the 4212 projector numerator only inside the q-basic observed-coframe no-wall selector",
        ),
        (
            "PCT4214_6_bound_fallback",
            "fallback bound if any selector clause fails",
            "|I_projector|/M_H_ref <= (|R_P_metric|+|R_domain|+|R_Hodge_readout|+|R_wall|+|R_denominator|+|R_source_readout|)/M_H_ref",
            "bound_row_retained",
            "no cancellation credit between projector escape routes",
        ),
        (
            "PCT4214_7_nonclaim_guard",
            "public claim guard",
            "Full local-GR/PPN source closure remains false until parent coframe, Hodge domain, projector owner and M_H_ref are signed.",
            "nonclaim_guard",
            "conditional projector silence is not the whole H_tau theorem",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": row[0],
            "clause": row[1],
            "statement": row[2],
            "status": row[3],
            "meaning": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def activation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PAC4214_0_projector_owner",
            "P_loc is q-basic/fixed before variation",
            "conditional_from_4089_4177",
            "R_P_metric;R_domain",
        ),
        (
            "PAC4214_1_coframe_hodge",
            "same observed coframe and Hodge descend through q",
            "conditional_from_4205_4208_4014",
            "R_Hodge_readout;R_coframe_projector",
        ),
        (
            "PAC4214_2_source_readout",
            "source/readout quantities factor through q",
            "conditional_from_4121",
            "R_source_readout;R_measured_GM_projector",
        ),
        (
            "PAC4214_3_wall_boundary",
            "no wall/constraint/boundary projector flux",
            "conditional_private_selector",
            "R_wall;R_boundary_projector",
        ),
        (
            "PAC4214_4_denominator",
            "no second projector denominator and M_H_ref exists",
            "M_H_ref_missing_for_global_score",
            "R_denominator;MISSING_STABLE_MH_REF",
        ),
        (
            "PAC4214_5_no_cancellation",
            "componentwise zero or bound only",
            "active_guard",
            "NO_CANCELLATION_CREDIT",
        ),
    ]
    return [
        {
            **common(),
            "activation_id": row[0],
            "condition": row[1],
            "current_status": row[2],
            "if_failed": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def score_update_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PSU4214_0_I_projector",
            "I_projector",
            "int_S i_tau omega_projector",
            "0_under_PCT4214_selector",
            "CONDITIONAL_ZERO_SELECTOR",
        ),
        (
            "PSU4214_1_projector_bound",
            "I_projector_bound",
            "(|R_P_metric|+|R_domain|+|R_Hodge_readout|+|R_wall|+|R_denominator|+|R_source_readout|)/M_H_ref",
            "MISSING_GLOBAL_PARENT_SIGNATURE_OR_MHREF",
            "BOUND_ROW_RETAINED",
        ),
        (
            "PSU4214_2_delta_Htau_update",
            "delta_H_tau_nonintegrable_over_MH",
            "4212 sum with I_qbasic_vertical and I_projector removed only inside their selectors; otherwise include fallback bounds",
            "PARTIAL_REDUCTION_NONCLAIM",
            "FULL_SCORE_REQUIRES_REMAINING_COMPONENTS",
        ),
    ]
    return [
        {
            **common(),
            "row_id": row[0],
            "quantity": row[1],
            "formula": row[2],
            "value_or_bound": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def bound_component_rows() -> List[Dict[str, str]]:
    rows = [
        ("PCB4214_0_R_P_metric", "R_P_metric", "metric variation of projector kernel", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("PCB4214_1_R_domain", "R_domain", "domain/support motion of projector", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("PCB4214_2_R_Hodge_readout", "R_Hodge_readout", "hidden Hodge/coframe readout tail", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("PCB4214_3_R_wall", "R_wall", "wall/constraint/boundary projector flux", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("PCB4214_4_R_denominator", "R_denominator", "second denominator or projector normalization drift", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("PCB4214_5_R_source_readout", "R_source_readout", "source/readout or measured-GM projector leakage", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("PCB4214_6_M_H_ref", "M_H_ref", "positive same-frame Hamiltonian denominator", "MISSING_STABLE_MH_REF"),
    ]
    return [
        {
            **common(),
            "component_id": row[0],
            "component": row[1],
            "definition": row[2],
            "value_or_status": row[3],
            "numeric_value": "MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def route_rows() -> List[Dict[str, str]]:
    routes = [
        (
            "PR4214_0_activate_selector",
            "Activate projector zero selector",
            "use I_projector=0 only when q-basic projector, observed coframe/Hodge descent and no-wall denominator clauses all hold",
            "removes second retained 4212 curl numerator conditionally",
        ),
        (
            "PR4214_1_bound_projector",
            "Fill projector bound row",
            "if any selector clause fails, score R_P/R_domain/R_Hodge/R_wall/R_denominator/R_source individually",
            "keeps empirical route open without fake zero",
        ),
        (
            "PR4214_2_no_ppn_claim",
            "Block PPN/local-GR claim",
            "do not claim PPN/local-GR until I_ref, tau/surface, boundary/corner, visible EM, Dq and M_H_ref close",
            "prevents overclaim from one projector theorem",
        ),
        (
            "PR4214_3_reference_next",
            "Attack reference curl next",
            "derive H_ref derivative silence or score Delta_ref/I_ref",
            "next source-charge obstruction after qbasic and projector terms",
        ),
    ]
    return [
        {
            **common(),
            "route_id": row[0],
            "route": row[1],
            "action": row[2],
            "effect": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in routes
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4214_0",
            "decision": DECISION,
            "I_projector_closed_inside_selector": "True",
            "global_projector_owner_signature": "False",
            "global_observed_coframe_signature": "False",
            "M_H_ref_available": "False",
            "full_Htau_integrability_claim": "False",
            "local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4214_0_global_projector", "global I_projector zero", "blocked_until_projector_owner_coframe_hodge_wall_denominator_parent_signed"),
        ("FW4214_1_PPN", "PPN projector pass", "blocked_until_projector_zero_selector_or_component_bounds_are_source_backed"),
        ("FW4214_2_Htau", "full H_tau integrability", "blocked_until_I_ref_tau_boundary_visible_Dq_and_MHref_close"),
        ("FW4214_3_Newton", "Newton/local-GR source bridge", "blocked_until_Htau_integrability_and_M_H_ref_close"),
        ("FW4214_4_public", "public local-GR claim", "blocked_private_conditional_theorem_only"),
    ]
    return [
        {
            **common(),
            "firewall_id": row[0],
            "claim_family": row[1],
            "blocker": row[2],
            "status": "blocked_nonclaim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4214",
            "status": "projector_stress_curl_conditionally_zero_selector_nonclaim",
            "strong_result": "I_projector is zero inside the q-basic observed-coframe/Hodge no-wall selector",
            "remaining_gap": "global projector owner, same coframe parent signature, Hodge domain exclusion, wall/denominator silence, M_H_ref and remaining H_tau curl components remain unsigned",
            "project_effect": "second retained 4212 curl numerator is conditionally removed; next target is reference curl",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4214 conditionally closes the projector curl term; the next retained source-charge obstruction is the reference curl/reference-lock row.",
            "route_A": "derive H_ref derivative silence from a parent-selected reference branch before source/radius/frame/readout variation",
            "route_B": "if not zero, fill I_ref or Delta_ref_over_MH as the next bound row",
            "route_C": "keep projector and qbasic selector caveats attached to the reduced curl sum",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 230 - PPC4161 projector stress curl zero or bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

4212 retained the projector curl term:

```text
I_projector = int_S i_tau omega_projector.
```

4214 proves the conditional zero route and keeps the bound route if any projector clause fails.

## Factorization

The projector/domain stress is split before any zero claim:

```text
T_proj = T_P + T_domain + T_chi + T_wall + T_denominator.
```

## Conditional Zero Theorem

Assume:

1. `P_loc` is q-basic or fixed before variation: `P_loc=P_bar(q)` or a fixed topological/readout label.
2. the same observed coframe descends: `e_obs=e_bar(q)`;
3. the Hodge star is only `*_obs[g_obs,orientation]`;
4. source/readout quantities factor through `q`;
5. no active selector wall, boundary projector flux, second denominator, or hidden constitutive projector remains.

Then:

```text
D_v P_loc = 0
D_v e_obs = 0
D_v *_obs = 0
T_P = T_domain = T_chi = T_wall = T_denominator = 0
omega_projector = 0
I_projector = int_S i_tau omega_projector = 0.
```

This closes the projector numerator only inside the q-basic observed-coframe/Hodge no-wall selector.

## Fallback Bound

If any clause fails:

```text
|I_projector|/M_H_ref
<= (|R_P_metric|
 + |R_domain|
 + |R_Hodge_readout|
 + |R_wall|
 + |R_denominator|
 + |R_source_readout|) / M_H_ref.
```

No cancellation between these terms earns theorem-zero credit.

## Remaining Curl Sum

Inside the 4213 and 4214 selectors, the reduced 4212 curl numerator drops `I_qbasic_vertical` and `I_projector`. The full `H_tau` theorem still needs:

- `I_ref`;
- `I_tau+I_surface`;
- `I_boundary+I_corner`;
- `I_matter_EM`;
- `I_Dq`;
- stable positive `M_H_ref`.

## Next Target

`{NEXT_TARGET}` should attack:

```text
I_ref = curl(-delta H_ref)
```

or the equivalent `Delta_ref_over_MH` bound row.
"""


def checkpoint_doc() -> str:
    return f"""# 4214 Y5 R2FR projector stress curl zero or first bound row

**Status:** `{DECISION}`.

**Forward move:** `I_projector` is conditionally zero inside the q-basic observed-coframe/Hodge no-wall selector:

```text
P_loc=P_bar(q), e_obs=e_bar(q), *_obs=*[g_obs]
=> T_proj=0
=> omega_projector=0
=> I_projector=0.
```

This is not a global PPN/local-GR claim. It remains nonclaim until the projector owner, same coframe/Hodge action-domain, wall/denominator silence and `M_H_ref` are parent-signed or bounded.

## Files written

- `formalization-workbench\\230-PPC4161-projector-stress-curl-zero-or-bound.md`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4214_PROJECTOR_CURL_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4214_PROJECTOR_BOUND_COMPONENTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4214_DECISION.csv`

## Next target

`{NEXT_TARGET}`.
"""


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The projector-stress Hamiltonian curl term is conditionally closed: if the local projector is q-basic/fixed, the observed coframe and Hodge star descend through q, source/readout quantities are q-owned, and wall/denominator projector fluxes are silent, then omega_projector=0 and I_projector=0; otherwise a componentwise projector bound row is retained.",'
        f'"4214 source audit, projector curl theorem, activation clauses, bound components, curl score update, route matrix, decision row and firewall.",'
        f'private_projector_stress_curl_zero_conditional_nonclaim,'
        f'"Attack reference-lock curl I_ref or fill Delta_ref_over_MH/I_ref as the next source-charge bound row.",'
        f'"Projector silence reduces the H_tau curl only inside the selector; it does not prove full H_tau integrability, PPN, or local GR."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 projector stress curl zero - 4214

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4214 conditionally closes the 4212 projector curl:

```text
P_loc=P_bar(q), e_obs=e_bar(q), *_obs=*[g_obs], no wall/second denominator
=> omega_projector=0
=> I_projector=0.
```

The fallback bound remains `(|R_P_metric|+|R_domain|+|R_Hodge_readout|+|R_wall|+|R_denominator|+|R_source_readout|)/M_H_ref` if any selector clause fails."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet projector stress curl zero - 4214

Marker: `{PACKET_MARKER}`

The packet now has conditional zero theorems for `I_qbasic_vertical` and `I_projector`. Next retained source-charge obstruction: reference curl `I_ref` / `Delta_ref_over_MH`."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4214_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4214_PROJECTOR_CURL_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4214_ACTIVATION_CLAUSES.csv"]
    score = rows_by_file["P8_Y5_R2FR_4214_CURL_SCORE_UPDATE.csv"]
    bound = rows_by_file["P8_Y5_R2FR_4214_PROJECTOR_BOUND_COMPONENTS.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4214_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4214_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "PCT4214_0_factorization",
        "PCT4214_1_qbasic_projector",
        "PCT4214_2_observed_coframe_hodge",
        "PCT4214_3_source_readout_descent",
        "PCT4214_4_no_wall_denominator",
        "PCT4214_5_curl_zero",
        "PCT4214_6_bound_fallback",
        "PCT4214_7_nonclaim_guard",
    }
    required_bounds = {
        "R_P_metric",
        "R_domain",
        "R_Hodge_readout",
        "R_wall",
        "R_denominator",
        "R_source_readout",
        "M_H_ref",
    }
    checks = [
        ("VAL4214_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4214_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4214_2_theorem_complete", "projector theorem contains all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4214_3_curl_zero_clause", "I_projector zero clause exists", any(row["theorem_id"] == "PCT4214_5_curl_zero" and row["status"] == "conditional_zero_theorem" for row in theorem)),
        ("VAL4214_4_bound_fallback", "fallback bound exists", any(row["theorem_id"] == "PCT4214_6_bound_fallback" for row in theorem)),
        ("VAL4214_5_activation_clauses", "activation clauses include projector, coframe, source, wall, denominator and no-cancellation", {"PAC4214_0_projector_owner", "PAC4214_1_coframe_hodge", "PAC4214_2_source_readout", "PAC4214_3_wall_boundary", "PAC4214_4_denominator", "PAC4214_5_no_cancellation"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4214_6_score_update_zero", "curl score update records conditional projector zero", any(row["quantity"] == "I_projector" and row["value_or_bound"] == "0_under_PCT4214_selector" for row in score)),
        ("VAL4214_7_bound_components", "bound component rows cover all projector failures", required_bounds.issubset({row["component"] for row in bound})),
        ("VAL4214_8_routes", "routes include selector, bound, no claim and reference next", {"PR4214_0_activate_selector", "PR4214_1_bound_projector", "PR4214_2_no_ppn_claim", "PR4214_3_reference_next"}.issubset({row["route_id"] for row in routes})),
        ("VAL4214_9_decision_nonclaim", "decision keeps global and local-GR claims false", decision["global_projector_owner_signature"] == "False" and decision["local_GR_claim"] == "False"),
        ("VAL4214_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4214_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4214_12_claim_register", "claim register contains L-055", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4214_13_spine_packet_markers", "spine and packet markers present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)),
        ("VAL4214_14_next_target", "next target is reference lock", decision["next_target"] == NEXT_TARGET),
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
    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8", newline="\n")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8", newline="\n")
    rows_by_file = {
        "P8_Y5_R2FR_4214_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4214_PROJECTOR_CURL_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4214_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4214_CURL_SCORE_UPDATE.csv": score_update_rows(),
        "P8_Y5_R2FR_4214_PROJECTOR_BOUND_COMPONENTS.csv": bound_component_rows(),
        "P8_Y5_R2FR_4214_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4214_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4214_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4214_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4214_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4214_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4214_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
