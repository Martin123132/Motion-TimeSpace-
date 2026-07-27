from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4296"
CLAIM_ID = "L-137"
BRANCH = "MTS_R2FR_Y5_PLEAK_TRANSITION_COMPONENT_ZERO_ATTEMPTS_OR_BOUND_ROW_SELECTION_4296"
DECISION = "FIRST_TWO_PLEAK_COMPONENTS_NOT_ZERO_DERIVED_BOUND_ROWS_SELECTED_NONCLAIM"
MARKER = "PPC4161_PLEAK_TRANSITION_COMPONENT_ZERO_ATTEMPTS_4296"
PACKET_MARKER = "PPC4161_PACKET_PLEAK_TRANSITION_COMPONENT_ZERO_ATTEMPTS_4296"
NEXT_TARGET = "4297-Y5-R2FR-qtr-vertical-or-topological-rest-proof-attempt-for-PnonHilbert.md"

FORMAL_PATH = FORMAL / "312-PPC4161-Pleak-transition-component-zero-attempts-or-bound-row-selection.md"
DOC_PATH = POST / "4296-Y5-R2FR-Pleak-transition-component-zero-attempts-or-bound-row-selection.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4296_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4296_00_4295_formal": (
        FORMAL / "311-PPC4161-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md",
        "P_nonHilbert_action_domain q_tr = 0",
        "4295 names the first zero attempt target.",
    ),
    "SRC4296_01_4295_pleak": (
        SOURCE_DIR / "P8_Y5_R2FR_4295_PLEAK_DECOMPOSITION.csv",
        "P_off_worldtube_readout_order q_tr",
        "4295 machine decomposition of live P_leak components.",
    ),
    "SRC4296_02_4295_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4295_CLAUSE_PROMOTION_AUDIT.csv",
        "PARTIAL_SUPPORT_FOR_ORDINARY_SOURCES_ONLY",
        "4295 clause audit separates ordinary-source support from raw transition promotion.",
    ),
    "SRC4296_03_4293_required": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "REQ4293_WEP",
        "4293 suppression rows are the fallback when zero is not derived.",
    ),
    "SRC4296_04_137_source_lift": (
        FORMAL / "137-transition-source-lift-action-block.md",
        "transition_source_lift_action_block_not_derived_minimal_contract_required",
        "Source-lift action block route was previously contract-only.",
    ),
    "SRC4296_05_138_metric_null": (
        FORMAL / "138-metric-null-action-block-contract.md",
        "metric_null_action_block_contract_defined_not_derived_route_contract_only",
        "Metric-null action block route exists as contract, not theorem.",
    ),
    "SRC4296_06_193_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "R_proj = Pi_loc D Obar_loc[Dq[v]] = 0.",
        "Quotient vertical silence is the best derivation route for P_nonHilbert.",
    ),
    "SRC4296_07_196_min_parent": (
        FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md",
        "q-owned exact/topological/silent rest.",
        "Minimal parent-action candidate contains q-owned silent rest, but not raw transition adoption.",
    ),
    "SRC4296_08_281_Dq_matter": (
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "Dq_matter = 0",
        "Matter-domain zero is conditionally adopted, not enough for raw q_tr.",
    ),
    "SRC4296_09_282_Dq_source": (
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "Dq_source_readout = 0",
        "Source-readout zero is conditionally adopted, not enough for raw q_tr.",
    ),
    "SRC4296_10_186_worldtube": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "ell_M(Pi_M^H J_H_total) := M_H^dress",
        "Private Hamiltonian worldtube readout is available inside the selector.",
    ),
    "SRC4296_11_307_PiM": (
        FORMAL / "307-PPC4161-PiM-Htau-private-selector-glue-reactivation-or-residual-transfer.md",
        "Pi_M/H_tau = solved inside private Hamiltonian selector",
        "PiM/Htau denominator is not the first blocker inside the selector.",
    ),
    "SRC4296_12_308_membership": (
        FORMAL / "308-PPC4161-transition-membership-and-nonEH-monopole-zero-or-shared-residual-vector.md",
        "But this membership is **not parent-signed**",
        "Transition same-worldtube membership is conditional and not parent-signed.",
    ),
    "SRC4296_13_1016_selector": (
        POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "Current MTS has not yet signed those clauses.",
        "Worldtube/source selector remains unsigned for current MTS.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4296 attacks the first two P_leak components from 4295. P_nonHilbert_action_domain q_tr can be zero "
                "only if the raw transition is Hilbert-action owned before variation, q-vertical by quotient naturality, "
                "q-owned exact/topological rest, or a derived metric-null block. The corpus supports those routes only "
                "conditionally, not for raw q_tr. P_off_worldtube_readout_order q_tr can be zero only if transition support "
                "is inside W_H before M_H^dress readout; the Hamiltonian selector exists, but transition membership remains "
                "not parent-signed. Therefore both first components remain nonclaim and are assigned fallback bound rows."
            ),
            (
                "4296 source register, component-zero attempts, bound-selection rows, control cases, decision, firewall, "
                "status and validation CSV."
            ),
            "private_first_two_pleak_components_not_zero_derived_bound_rows_selected_nonclaim",
            (
                "Try the q_tr vertical/topological-rest proof first for P_nonHilbert_action_domain; if it fails, carry the "
                "component through the 4293 local bound vector."
            ),
            (
                "Using ordinary-source Hilbert descent as raw transition proof, treating Hamiltonian selector existence as "
                "transition support membership, or claiming local-GR/WEP/R10 pass."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def req_lookup() -> Dict[str, Dict[str, str]]:
    return {row.get("requirement_id", ""): row for row in csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv")}


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


def component_zero_attempt_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "ZA4296_P0_HILBERT_ACTION",
            "P_nonHilbert_action_domain q_tr",
            "Hilbert-action ownership before variation",
            "q_tr = delta S_tr^H[g_obs,chi;tau]/delta g_obs with same metric/source measure",
            "NOT_PARENT_SIGNED_FOR_RAW_TRANSITION",
            "185 signs ordinary source descent; 137/138/308 do not sign raw transition S_tr^H.",
            "P_nonHilbert q_tr remains live",
        ),
        (
            "ZA4296_P0_Q_VERTICAL",
            "P_nonHilbert_action_domain q_tr",
            "quotient vertical silence",
            "Dq[q_tr]=0 and local action/readouts factor through q before variation",
            "BEST_NEXT_ATTEMPT_NOT_YET_SIGNED",
            "193 proves the theorem if q_tr is vertical; current corpus has not shown raw q_tr is in ker(Dq).",
            "next target tries this route directly",
        ),
        (
            "ZA4296_P0_TOPOLOGICAL_REST",
            "P_nonHilbert_action_domain q_tr",
            "q-owned exact/topological rest",
            "q_tr=dB or topological density with zero local bulk Hilbert response",
            "CONDITIONAL_REST_ROUTE_NOT_RAW_TRANSITION_SIGNED",
            "196 allows q-owned silent rest in the candidate; 137/138 say transition metric-nullity is still contract-only.",
            "fallback to component bound if not derived",
        ),
        (
            "ZA4296_P0_METRIC_NULL_BLOCK",
            "P_nonHilbert_action_domain q_tr",
            "metric-null transition action block",
            "Sigma_metric[q_tr] := -2/sqrt(-g) delta S_tr/delta g_loc = 0",
            "CONTRACT_ONLY_NOT_DERIVED",
            "137/138 wrote the contract and explicitly did not derive it.",
            "fallback to 4293 local bound vector",
        ),
        (
            "ZA4296_P1_HAMILTONIAN_SELECTOR",
            "P_off_worldtube_readout_order q_tr",
            "Hamiltonian/worldtube denominator",
            "Pi_M := Pi_M^H and ell_M(Pi_M^H J_H_total)=M_H^dress[W_H;tau]",
            "SOLVED_ONLY_INSIDE_SELECTOR",
            "186/307 solve the denominator if J_tr is already in J_H_total; they do not prove raw transition membership.",
            "membership remains live",
        ),
        (
            "ZA4296_P1_SUPPORT_MEMBERSHIP",
            "P_off_worldtube_readout_order q_tr",
            "same-worldtube before readout",
            "supp J_tr^H subset W_H=closure(supp J_H_total) before M_H^dress readout",
            "NOT_PARENT_SIGNED_FOR_RAW_TRANSITION",
            "308 and 1016 explicitly keep current transition/source selector membership unsigned.",
            "fallback to source-measure/readout-order residual rows",
        ),
        (
            "ZA4296_P1_PRE_READOUT_ORDER",
            "P_off_worldtube_readout_order q_tr",
            "variation/readout order",
            "transition enters the source action before charge/readout, not as a late GM repair",
            "NOT_PARENT_SIGNED_FOR_RAW_TRANSITION",
            "1016 blocks source-measure equality until parent action, tau, compactness, M_H_ref and PiM_H are signed.",
            "fallback to R_eq/I_commutator/epsilon_selector rows",
        ),
    ]
    return [
        {
            **common(),
            "attempt_id": attempt_id,
            "component": component,
            "route": route,
            "zero_condition": condition,
            "status": status,
            "evidence": evidence,
            "result": result,
            "zero_derived": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for attempt_id, component, route, condition, status, evidence, result in raw
    ]


def bound_selection_rows() -> List[Dict[str, str]]:
    reqs = req_lookup()
    rows: List[Dict[str, str]] = []
    for req_id, component, role in [
        ("REQ4293_WEP", "P_nonHilbert_action_domain q_tr", "composition/source-charge leakage fallback"),
        ("REQ4293_GAMMA", "P_nonHilbert_action_domain q_tr", "metric spatial-curvature readout fallback"),
        ("REQ4293_BETA", "P_nonHilbert_action_domain q_tr", "second-order metric readout fallback"),
        ("REQ4293_CLOCK", "P_nonHilbert_action_domain q_tr", "clock-frame readout fallback"),
        ("REQ4293_ORBIT", "P_nonHilbert_action_domain q_tr", "orbital/source-normalization readout fallback"),
        ("REQ4293_GDOT_TIMESCALE", "P_nonHilbert_action_domain q_tr", "time-drift fallback if component is not static"),
        ("REQ4293_R10_ANCHOR", "P_nonHilbert_action_domain q_tr", "finite-range hair fallback; anchor only"),
    ]:
        req = reqs.get(req_id, {})
        rows.append(
            {
                **common(),
                "bound_selection_id": f"BS4296_{len(rows):02d}_{req_id}",
                "component": component,
                "selected_bound_or_input": req_id,
                "selected_value": req.get("required_value", "MISSING_4293_REQUIREMENT"),
                "units": req.get("units", "MISSING_UNITS"),
                "role": role,
                "selection_status": "ACTIVE_IF_ZERO_ROUTE_FAILS",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    for input_id, component, selected, status, role in [
        (
            "BS4296_07_epsilon_PiH",
            "P_off_worldtube_readout_order q_tr",
            "epsilon_PiH <= |R_kernel|+|I_commutator|+|C_curl|+|C_ref|+|C_frame|+|C_units|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|",
            "FORMULA_ONLY_FROM_4291",
            "fallback if Hamiltonian selector not adopted before readout",
        ),
        (
            "BS4296_08_Delta_worldtube_domain",
            "P_off_worldtube_readout_order q_tr",
            "FIS1016_2_worldtube_domain_shift",
            "BLOCKED_MISSING_INPUT",
            "source worldtube domain shift row from 1016",
        ),
        (
            "BS4296_09_R_eq_integral",
            "P_off_worldtube_readout_order q_tr",
            "FIS1016_4_R_eq_integral",
            "BLOCKED_MISSING_INPUT",
            "finite shell/source-measure equality residual row from 1016",
        ),
        (
            "BS4296_10_I_commutator",
            "P_off_worldtube_readout_order q_tr",
            "FIS1016_5_I_commutator",
            "BLOCKED_MISSING_INPUT",
            "Hamiltonian PiM commutator/order residual row from 1016",
        ),
        (
            "BS4296_11_epsilon_selector_Meff",
            "P_off_worldtube_readout_order q_tr",
            "FIS1016_7_epsilon_selector_Meff",
            "BLOCKED_MISSING_INPUT",
            "selector no-cancellation envelope row from 1016",
        ),
    ]:
        rows.append(
            {
                **common(),
                "bound_selection_id": input_id,
                "component": component,
                "selected_bound_or_input": selected,
                "selected_value": "MISSING_NUMERIC_SOURCE_BACKED_ROW",
                "units": "dimensionless_or_source_normalized",
                "role": role,
                "selection_status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def control_case_rows() -> List[Dict[str, str]]:
    controls = [
        ("CTRL4296_0_full_P0_zero", True, False, False, False, True, "P0_ZERO_BY_HILBERT_ACTION"),
        ("CTRL4296_1_vertical_P0_zero", False, True, False, False, True, "P0_ZERO_BY_QUOTIENT_VERTICALITY"),
        ("CTRL4296_2_topological_P0_zero", False, False, True, False, True, "P0_ZERO_BY_TOPOLOGICAL_REST"),
        ("CTRL4296_3_metric_null_P0_zero", False, False, False, True, True, "P0_ZERO_BY_METRIC_NULL_BLOCK"),
        ("CTRL4296_4_no_P0_zero", False, False, False, False, False, "P0_BOUND_ROWS_ACTIVE"),
        ("CTRL4296_5_worldtube_P1_zero", True, True, True, True, True, "P1_ZERO_BY_PRE_READOUT_MEMBERSHIP"),
        ("CTRL4296_6_no_worldtube_P1", True, False, True, True, False, "P1_BOUND_ROWS_ACTIVE"),
        ("CTRL4296_7_late_readout_P1", True, True, False, True, False, "P1_BOUND_ROWS_ACTIVE"),
        ("CTRL4296_8_no_PiM_selector_P1", True, True, True, False, False, "P1_BOUND_ROWS_ACTIVE"),
    ]
    rows: List[Dict[str, str]] = []
    for control_id, hilbert, vertical_or_worldtube, topological_or_prereadout, metric_null_or_pim, expected_zero, expected_outcome in controls:
        if control_id.startswith("CTRL4296_0") or control_id.startswith("CTRL4296_1") or control_id.startswith("CTRL4296_2") or control_id.startswith("CTRL4296_3") or control_id.startswith("CTRL4296_4"):
            actual_zero = hilbert or vertical_or_worldtube or topological_or_prereadout or metric_null_or_pim
            actual_outcome = (
                "P0_ZERO_BY_HILBERT_ACTION"
                if hilbert
                else "P0_ZERO_BY_QUOTIENT_VERTICALITY"
                if vertical_or_worldtube
                else "P0_ZERO_BY_TOPOLOGICAL_REST"
                if topological_or_prereadout
                else "P0_ZERO_BY_METRIC_NULL_BLOCK"
                if metric_null_or_pim
                else "P0_BOUND_ROWS_ACTIVE"
            )
            component = "P_nonHilbert_action_domain q_tr"
        else:
            actual_zero = hilbert and vertical_or_worldtube and topological_or_prereadout and metric_null_or_pim
            actual_outcome = "P1_ZERO_BY_PRE_READOUT_MEMBERSHIP" if actual_zero else "P1_BOUND_ROWS_ACTIVE"
            component = "P_off_worldtube_readout_order q_tr"
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "component": component,
                "flag_A": str(hilbert),
                "flag_B": str(vertical_or_worldtube),
                "flag_C": str(topological_or_prereadout),
                "flag_D": str(metric_null_or_pim),
                "actual_zero": str(actual_zero),
                "expected_zero": str(expected_zero),
                "actual_outcome": actual_outcome,
                "expected_outcome": expected_outcome,
                "expected_matches_actual": str(actual_zero == expected_zero and actual_outcome == expected_outcome),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4296_0",
            "decision": DECISION,
            "what_moved": "The first two P_leak components now have explicit zero routes and fallback bound rows; neither is silently left as a vague missing coupling.",
            "best_next": "Try q_tr vertical/topological-rest proof for P_nonHilbert_action_domain before doing more numeric bound plumbing.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4296_0_no_ordinary_source_promotion", "Dq_matter/Dq_source zeros do not prove raw transition q_tr is vertical or Hilbert-owned."),
        ("FW4296_1_no_metric_null_contract_claim", "Metric-null action-block contract is not a derived source lift."),
        ("FW4296_2_no_worldtube_shortcut", "Hamiltonian selector existence does not prove transition support enters W_H before readout."),
        ("FW4296_3_bound_rows_are_fallbacks", "Selected bound rows are obligations, not evidence of pass."),
        ("FW4296_4_nonclaim", "No local-GR/WEP/R10/PPN/clock/orbital claim is allowed from 4296."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4296_0",
            "P_nonHilbert_action_domain_zero_derived": "False",
            "P_off_worldtube_readout_order_zero_derived": "False",
            "P_nonHilbert_best_route": "q_tr vertical/topological rest proof",
            "P_off_worldtube_best_route": "supp J_tr^H subset W_H before readout proof after P_nonHilbert route",
            "bound_selection_rows": str(len(bound_selection_rows())),
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4296_0",
            "next_target": NEXT_TARGET,
            "objective": "Try to prove raw q_tr is q-vertical or q-owned exact/topological rest, so P_nonHilbert_action_domain q_tr vanishes by quotient naturality or zero bulk response.",
            "fallback": "If q_tr is not vertical/topological/Hilbert-owned, route P_nonHilbert through the 4293 suppression vector.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    reqs = req_lookup()
    return f"""
# 312 P_leak transition component zero attempts or bound-row selection

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4296 attacks the first two leak-projector pieces from 4295:

```text
P_nonHilbert_action_domain q_tr,
P_off_worldtube_readout_order q_tr.
```

Neither is zero-derived for the raw transition shell in the current corpus.

## P_nonHilbert route

The component would vanish if any one of these were parent-signed:

```text
q_tr = delta S_tr^H[g_obs,chi;tau]/delta g_obs,
Dq[q_tr] = 0,
q_tr = q-owned exact/topological rest with zero local bulk response,
Sigma_metric[q_tr] = 0.
```

Current state:

```text
ordinary Hilbert source descent exists,
quotient vertical silence theorem exists,
q-owned silent-rest candidate exists,
metric-null contract exists,
but none is signed for raw q_tr.
```

So the next best derivation is:

```text
prove Dq[q_tr]=0 or q_tr=dB/topological-rest.
```

If that fails, the 4293 fallback bounds remain live, including:

```text
Y_WEP   <= {reqs.get('REQ4293_WEP', {}).get('required_value', 'MISSING')}
Y_gamma <= {reqs.get('REQ4293_GAMMA', {}).get('required_value', 'MISSING')}
Y_beta  <= {reqs.get('REQ4293_BETA', {}).get('required_value', 'MISSING')}
Y_clock <= {reqs.get('REQ4293_CLOCK', {}).get('required_value', 'MISSING')}
Y_orbit <= {reqs.get('REQ4293_ORBIT', {}).get('required_value', 'MISSING')}
```

## P_off_worldtube route

The component would vanish if:

```text
supp J_tr^H subset W_H = closure(supp J_H_total)
```

before `M_H^dress[W_H;tau]` is read out.

Current state:

```text
Pi_M/H_tau/worldtube glue is solved inside the private selector,
but raw transition membership in W_H is not parent-signed.
```

So the fallback is not a local-GR pass. It is a source-measure/readout-order residual row:

```text
epsilon_PiH,
Delta_worldtube_domain,
R_eq_integral,
I_commutator,
epsilon_selector_Meff.
```

## Status

This is a nonclaim checkpoint. It narrows the next proof target rather than pretending a proof exists.

Next target: `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4296 Y5 R2FR P_leak transition component zero attempts

## Purpose

Try the derivation path for the first two `P_leak q_tr` components, then select bound rows if the derivation does not close.

## Outcome

`P_nonHilbert_action_domain q_tr` is not zero-derived yet. The best next proof route is `Dq[q_tr]=0` or q-owned exact/topological rest.

`P_off_worldtube_readout_order q_tr` is not zero-derived yet. The Hamiltonian selector exists, but transition support membership before readout is unsigned.

## Next

Attempt the q-vertical/topological-rest proof for raw `q_tr`.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    attempts = csv_rows(paths["component_zero_attempts"])
    bounds = csv_rows(paths["bound_selection"])
    controls = csv_rows(paths["control_cases"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4296_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4296_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4296_2_attempts_cover_first_two_components",
            {row["component"] for row in attempts} == {"P_nonHilbert_action_domain q_tr", "P_off_worldtube_readout_order q_tr"}
            and sum(row["component"] == "P_nonHilbert_action_domain q_tr" for row in attempts) >= 4
            and sum(row["component"] == "P_off_worldtube_readout_order q_tr" for row in attempts) >= 3,
            "zero attempts cover P0 and P1 routes",
        ),
        (
            "VAL4296_3_no_zero_promoted",
            bool(attempts) and all(row["zero_derived"] == "False" for row in attempts),
            "no first-two P_leak zero is promoted",
        ),
        (
            "VAL4296_4_bound_selection",
            any(row["selected_bound_or_input"] == "REQ4293_WEP" for row in bounds)
            and any(row["selected_bound_or_input"] == "FIS1016_4_R_eq_integral" for row in bounds)
            and len(bounds) >= 12,
            "fallback bound/input rows are selected",
        ),
        (
            "VAL4296_5_control_cases",
            bool(controls) and all(row["expected_matches_actual"] == "True" for row in controls),
            "control cases distinguish zero routes from bound fallback",
        ),
        ("VAL4296_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4296_7_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4296_8_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-137 private nonclaim row",
        ),
        (
            "VAL4296_9_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4296_10_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4296_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4296_SOURCE_REGISTER.csv",
        "component_zero_attempts": SOURCE_DIR / "P8_Y5_R2FR_4296_COMPONENT_ZERO_ATTEMPTS.csv",
        "bound_selection": SOURCE_DIR / "P8_Y5_R2FR_4296_BOUND_SELECTION_ROWS.csv",
        "control_cases": SOURCE_DIR / "P8_Y5_R2FR_4296_COMPONENT_CONTROL_CASES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4296_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4296_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4296_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4296_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["component_zero_attempts"], component_zero_attempt_rows())
    write_csv(paths["bound_selection"], bound_selection_rows())
    write_csv(paths["control_cases"], control_case_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4296 first P_leak component zero attempts",
        (
            "4296 attacks `P_nonHilbert_action_domain q_tr` and `P_off_worldtube_readout_order q_tr`. "
            "Neither zero is parent-derived for raw transition shell. The next best route is a direct "
            "`Dq[q_tr]=0` or q-owned exact/topological-rest proof; otherwise 4293 and 1016 fallback rows stay active."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4296 packet first P_leak component gate",
        (
            "Packet update: the first two transition leak components are not vague blockers anymore. Each has a zero route "
            "and a bound fallback; the next proof target is raw `q_tr` verticality/topological rest."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
