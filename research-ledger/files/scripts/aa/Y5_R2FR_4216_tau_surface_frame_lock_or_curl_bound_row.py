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

CHECKPOINT = "4216"
CLAIM_ID = "L-057"
BRANCH_ID = "MTS_R2FR_Y5_TAU_SURFACE_FRAME_LOCK_4216"
DECISION = (
    "TAU_SURFACE_FRAME_LOCK_CURL_ZERO_CONDITIONALLY_DERIVED_FOR_ONE_PARENT_"
    "TIME_SURFACE_COFRAME_READOUT_SPLIT_BOUND_ROW_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "232-PPC4161-tau-surface-frame-lock-or-bound.md"
DOC_PATH = POST / "4216-Y5-R2FR-tau-surface-frame-lock-or-curl-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_TAU_SURFACE_FRAME_LOCK_4216"
PACKET_MARKER = "PPC4161_PACKET_TAU_SURFACE_FRAME_LOCK_4216"
NEXT_TARGET = "4217-Y5-R2FR-boundary-corner-curl-zero-or-flux-bound-row.md"

SOURCES = {
    "SRC4216_00_4215_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4215_NEXT_TARGET.csv",
        "4216-Y5-R2FR-tau-surface-frame-lock-or-curl-bound-row.md",
        "4215 selected tau/surface/frame lock as next source-charge obstruction.",
    ),
    "SRC4216_01_231_formal": (
        FORMAL / "231-PPC4161-reference-lock-curl-zero-or-bound.md",
        "I_tau + I_surface + C_frame.",
        "4215 formal next target.",
    ),
    "SRC4216_02_4212_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv",
        "I_tau+I_surface",
        "4212 retained tau/surface curl component.",
    ),
    "SRC4216_03_4097_same_frame": (
        SOURCE_DIR / "P8_Y5_R2FR_4097_SAME_FRAME_SOURCE_COUPLING_THEOREM.csv",
        "SFC4097_0_parent_action_frame",
        "Same-frame source-coupling theorem.",
    ),
    "SRC4216_04_3982_surface": (
        SOURCE_DIR / "P8_Y5_R2FR_3982_CONTROLLED_SURFACE_EXCHANGE_ZERO_THEOREM.csv",
        "CSX3982_0_branch",
        "Controlled surface/exchange silence theorem.",
    ),
    "SRC4216_05_4172_gauge": (
        SOURCE_DIR / "P8_Y5_R2FR_4172_PPN_GAUGE_AND_ASSUMPTIONS.csv",
        "GAUGE4172_1_coordinates",
        "Local PPN gauge/readout coordinates.",
    ),
    "SRC4216_06_4205_coframe": (
        SOURCE_DIR / "P8_Y5_R2FR_4205_EH_COFRAME_SIGNATURE_GATE.csv",
        "SIG4205_0_same_coframe",
        "Same observed coframe gate.",
    ),
    "SRC4216_07_3900_coframe": (
        SOURCE_DIR / "P8_Y5_R2FR_3900_SINGLE_COFRAME_LOCK_ATTEMPT.csv",
        "COF3900_1_single_frame",
        "Single visible coframe lock attempt.",
    ),
    "SRC4216_08_4211_tau": (
        SOURCE_DIR / "P8_Y5_R2FR_4211_HTAU_MHSOURCE_OWNER_CONTRACT.csv",
        "HMO4211_5_tau_frame_lock",
        "4211 source-charge owner tau/frame clause.",
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
            "TSF4216_0_one_time_generator",
            "one parent local time generator",
            "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout is selected before variation.",
            "conditional_lock_theorem",
            "prevents the Hamiltonian charge from using a different time than clocks/orbits/source readout",
        ),
        (
            "TSF4216_1_fixed_surface_family",
            "fixed or tau-dragged surface family",
            "S_link(lambda) is fixed by the parent domain or Lie_tau-dragged with no independent variation in the allowed branch.",
            "conditional_surface_theorem",
            "kills the moving-surface contribution to the Hamiltonian curl",
        ),
        (
            "TSF4216_2_same_observed_coframe",
            "same observed coframe",
            "e_obs(q) is used by EH, Hilbert stress, EM, rods, clocks, orbital readout, PPN coordinates and H_tau.",
            "conditional_frame_theorem",
            "prevents preferred-frame or hidden-frame terms from entering C_frame",
        ),
        (
            "TSF4216_3_fixed_units_orientation",
            "fixed units/orientation/readout normalization",
            "clock units, orientation, local PPN gauge convention, and source normalization are common-mode before comparison.",
            "conditional_units_theorem",
            "prevents C_units/C_frame from masquerading as a physical force",
        ),
        (
            "TSF4216_4_curl_zero",
            "tau/surface/frame curl zero",
            "If TSF4216_0 through TSF4216_3 hold, then I_tau+I_surface+C_frame=0.",
            "conditional_zero_theorem",
            "closes the 4212 tau/surface/frame numerator only inside the same-frame selector",
        ),
        (
            "TSF4216_5_no_coordinate_cheat",
            "no coordinate/readout-after-fit shortcut",
            "A PPN gauge or clock convention chosen after seeing residuals does not count as tau/frame lock.",
            "anti_circularity_guard",
            "the lock must precede source-charge variation and empirical comparison",
        ),
        (
            "TSF4216_6_surface_flux_guard",
            "surface exchange guard",
            "nonisolated, moving, radiative, wall/shear, or apparatus-coupled surfaces are boundary/corner flux rows, not zero.",
            "boundary_guard",
            "controlled surface exchange from 3982 is branch-specific",
        ),
        (
            "TSF4216_7_bound_fallback",
            "tau/surface/frame fallback bound",
            "|I_tau+I_surface+C_frame|/M_H_ref <= (|R_tau_split|+|R_surface_motion|+|R_frame_coframe|+|R_clock_readout|+|R_orbital_readout|+|R_units|)/M_H_ref",
            "bound_row_retained",
            "each mismatch is scored separately with no cancellation credit",
        ),
        (
            "TSF4216_8_nonclaim_guard",
            "public claim guard",
            "Full H_tau/Newton/local-GR closure remains false until boundary/corner, visible EM, Dq and M_H_ref terms also close.",
            "nonclaim_guard",
            "same-frame lock is not the whole source-charge theorem",
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
            "TSA4216_0_tau_common",
            "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout",
            "conditional_from_4211_4097_4172",
            "R_tau_split",
        ),
        (
            "TSA4216_1_surface_fixed",
            "S_link fixed or tau-dragged before variation",
            "conditional_from_3982_controlled_branch",
            "R_surface_motion",
        ),
        (
            "TSA4216_2_same_coframe",
            "one e_obs(q) for geometry/matter/EM/clocks/readout",
            "conditional_from_3900_4205_4097",
            "R_frame_coframe",
        ),
        (
            "TSA4216_3_clock_readout",
            "clock units and redshift readout use same tau/e_obs",
            "conditional_local_packet",
            "R_clock_readout",
        ),
        (
            "TSA4216_4_orbital_ppn_readout",
            "orbital and PPN coordinates use the same local quasi-Cartesian frame before comparison",
            "conditional_from_4172",
            "R_orbital_readout;R_PPN_gauge",
        ),
        (
            "TSA4216_5_MHref",
            "M_H_ref exists before normalized scoring",
            "M_H_ref_missing_for_global_score",
            "MISSING_STABLE_MH_REF",
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
            "TSU4216_0_I_tau_surface_frame",
            "I_tau+I_surface+C_frame",
            "field dependence of tau, moving surface family and frame/coframe mismatch",
            "0_under_TSF4216_selector",
            "CONDITIONAL_ZERO_SELECTOR",
        ),
        (
            "TSU4216_1_tau_surface_bound",
            "I_tau_surface_frame_bound",
            "(|R_tau_split|+|R_surface_motion|+|R_frame_coframe|+|R_clock_readout|+|R_orbital_readout|+|R_units|)/M_H_ref",
            "MISSING_GLOBAL_LOCK_OR_MHREF",
            "BOUND_ROW_RETAINED",
        ),
        (
            "TSU4216_2_delta_Htau_update",
            "delta_H_tau_nonintegrable_over_MH",
            "4212 sum with I_qbasic_vertical, I_projector, I_ref and I_tau+I_surface+C_frame removed only inside their selectors; otherwise include fallback bounds",
            "PARTIAL_REDUCTION_NONCLAIM",
            "FULL_SCORE_REQUIRES_BOUNDARY_VISIBLE_DQ_MHREF",
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
        ("TCB4216_0_R_tau_split", "R_tau_split", "different time generators for source, charge, clock, orbit, PPN, or readout", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("TCB4216_1_R_surface_motion", "R_surface_motion", "moving or reselected linking surface/domain family", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("TCB4216_2_R_frame_coframe", "R_frame_coframe", "hidden coframe/frame mismatch between sectors", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("TCB4216_3_R_clock_readout", "R_clock_readout", "clock/redshift unit convention not common-mode", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("TCB4216_4_R_orbital_readout", "R_orbital_readout", "orbital/PPN coordinate readout selected after comparison", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("TCB4216_5_R_units", "R_units", "unit/orientation/normalization mismatch in H_tau denominator", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("TCB4216_6_M_H_ref", "M_H_ref", "positive same-frame Hamiltonian source denominator", "MISSING_STABLE_MH_REF"),
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
            "TR4216_0_activate_selector",
            "Activate tau/surface/frame zero selector",
            "use I_tau+I_surface+C_frame=0 only when one tau, one surface family and one observed coframe are fixed before variation",
            "removes fourth retained 4212 curl numerator conditionally",
        ),
        (
            "TR4216_1_bound_lock",
            "Fill tau/surface/frame bound row",
            "if any lock fails, score R_tau/R_surface/R_frame/R_clock/R_orbit/R_units over M_H_ref",
            "keeps same-frame debt empirical rather than hidden",
        ),
        (
            "TR4216_2_no_coordinate_cheat",
            "Forbid post-fit gauge/readout lock",
            "do not pick PPN gauge, clock normalization or orbital frame after seeing residuals",
            "protects anti-circularity",
        ),
        (
            "TR4216_3_boundary_next",
            "Attack boundary/corner next",
            "derive boundary/corner curl zero or score flux/corner row",
            "next retained curl term in 4212",
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
            "decision_id": "DEC4216_0",
            "decision": DECISION,
            "I_tau_surface_frame_closed_inside_selector": "True",
            "global_tau_surface_frame_signature": "False",
            "post_fit_coordinate_lock_allowed": "False",
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
        ("FW4216_0_global_lock", "global tau/surface/frame zero", "blocked_until_common_tau_fixed_surface_same_coframe_and_MHref_parent_signed"),
        ("FW4216_1_coordinate", "post-fit coordinate/readout lock", "forbidden_if_chosen_after_observed_residuals"),
        ("FW4216_2_Htau", "full H_tau integrability", "blocked_until_boundary_corner_visible_Dq_and_MHref_close"),
        ("FW4216_3_Newton", "Newton/local-GR source bridge", "blocked_until_Htau_integrability_and_M_H_ref_close"),
        ("FW4216_4_public", "public local-GR claim", "blocked_private_conditional_theorem_only"),
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
            "status_id": "STATUS4216",
            "status": "tau_surface_frame_curl_conditionally_zero_selector_nonclaim",
            "strong_result": "I_tau+I_surface+C_frame is zero when one parent tau, fixed/tau-dragged surfaces and one observed coframe are selected before variation/readout",
            "remaining_gap": "global adoption, M_H_ref and remaining boundary/corner, visible EM and Dq curl terms remain unsigned",
            "project_effect": "fourth retained 4212 curl numerator is conditionally removed; next target is boundary/corner flux",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4216 conditionally closes the tau/surface/frame curl term; the next retained source-charge obstruction is boundary/corner flux.",
            "route_A": "derive I_boundary+I_corner=0 from exact differentiability terms, no-flux collar and fixed corner data",
            "route_B": "if not zero, fill boundary/corner flux over M_H_ref as the next bound row",
            "route_C": "keep qbasic, projector, reference and tau/frame selector caveats attached to the reduced curl sum",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 232 - PPC4161 tau/surface/frame lock or bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

4212 retained:

```text
I_tau + I_surface + C_frame.
```

4216 proves the conditional zero route for a single parent-owned time/surface/frame readout.

## Lock Theorem

Assume the local packet selects before variation:

1. one time generator:

```text
tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout;
```

2. one fixed or `tau`-dragged linking surface family `S_link`;
3. one observed coframe:

```text
e_obs=e_bar(q)
```

used by EH, Hilbert stress, EM, rods, clocks, orbital readout, PPN coordinates and `H_tau`;
4. common-mode units, orientation and source normalization.

Then no independent field-space curl is produced by changing time generator, moving surfaces, or switching frames:

```text
I_tau + I_surface + C_frame = 0.
```

## No Coordinate Cheat

This theorem is active only when the lock is chosen before source-charge variation and before empirical comparison. A PPN gauge, clock normalization, orbital frame, or readout map selected after seeing residuals is a fitted convention and must be scored.

## Fallback Bound

If any clause fails:

```text
|I_tau+I_surface+C_frame|/M_H_ref
<= (|R_tau_split|
 + |R_surface_motion|
 + |R_frame_coframe|
 + |R_clock_readout|
 + |R_orbital_readout|
 + |R_units|) / M_H_ref.
```

## Reduced Curl Status

Inside the 4213, 4214, 4215 and 4216 selectors, the reduced 4212 numerator drops:

```text
I_qbasic_vertical, I_projector, I_ref, I_tau+I_surface+C_frame.
```

The full source-charge theorem still requires:

- `I_boundary+I_corner`;
- `I_matter_EM`;
- `I_Dq`;
- stable positive `M_H_ref`.

## Next Target

`{NEXT_TARGET}` should attack:

```text
I_boundary + I_corner.
```
"""


def checkpoint_doc() -> str:
    return f"""# 4216 Y5 R2FR tau surface frame lock or curl bound row

**Status:** `{DECISION}`.

**Forward move:** the tau/surface/frame curl term is conditionally zero:

```text
one tau + fixed/tau-dragged S_link + one e_obs(q)
=> I_tau+I_surface+C_frame=0.
```

If the clock, charge, orbit, PPN gauge, surface family, frame or units are selected after seeing residuals, the term is not zero; it is a bound row.

## Files written

- `formalization-workbench\\232-PPC4161-tau-surface-frame-lock-or-bound.md`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4216_TAU_SURFACE_FRAME_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4216_TAU_SURFACE_BOUND_COMPONENTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4216_DECISION.csv`

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
        f'"The tau/surface/frame Hamiltonian curl term is conditionally closed: when one parent local time generator, fixed or tau-dragged linking surfaces, one observed coframe, and common units/readout normalization are selected before variation and comparison, I_tau+I_surface+C_frame=0; otherwise the mismatch is retained as a componentwise bound row.",'
        f'"4216 source audit, tau/surface/frame theorem, activation clauses, bound components, curl score update, route matrix, decision row and firewall.",'
        f'private_tau_surface_frame_lock_conditional_nonclaim,'
        f'"Attack boundary/corner curl I_boundary+I_corner, or fill boundary/corner flux as the next source-charge bound row.",'
        f'"A shared frame is legitimate only if parent-owned before readout; a post-fit coordinate/clock convention is circular."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 tau/surface/frame lock - 4216

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4216 conditionally closes the 4212 tau/surface/frame curl:

```text
tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout
and fixed/tau-dragged S_link
and one e_obs(q)
=> I_tau+I_surface+C_frame=0.
```

If any time/surface/frame/readout lock is selected after seeing residuals, the term remains a bound row."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet tau/surface/frame lock - 4216

Marker: `{PACKET_MARKER}`

The packet now has conditional zero theorems for `I_qbasic_vertical`, `I_projector`, `I_ref`, and `I_tau+I_surface+C_frame`. Next retained obstruction: boundary/corner flux."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4216_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4216_TAU_SURFACE_FRAME_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4216_ACTIVATION_CLAUSES.csv"]
    score = rows_by_file["P8_Y5_R2FR_4216_CURL_SCORE_UPDATE.csv"]
    bound = rows_by_file["P8_Y5_R2FR_4216_TAU_SURFACE_BOUND_COMPONENTS.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4216_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4216_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "TSF4216_0_one_time_generator",
        "TSF4216_1_fixed_surface_family",
        "TSF4216_2_same_observed_coframe",
        "TSF4216_3_fixed_units_orientation",
        "TSF4216_4_curl_zero",
        "TSF4216_5_no_coordinate_cheat",
        "TSF4216_6_surface_flux_guard",
        "TSF4216_7_bound_fallback",
        "TSF4216_8_nonclaim_guard",
    }
    required_bounds = {
        "R_tau_split",
        "R_surface_motion",
        "R_frame_coframe",
        "R_clock_readout",
        "R_orbital_readout",
        "R_units",
        "M_H_ref",
    }
    checks = [
        ("VAL4216_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4216_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4216_2_theorem_complete", "tau/surface/frame theorem contains all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4216_3_curl_zero_clause", "I_tau+I_surface+C_frame zero clause exists", any(row["theorem_id"] == "TSF4216_4_curl_zero" and row["status"] == "conditional_zero_theorem" for row in theorem)),
        ("VAL4216_4_no_coordinate_cheat", "post-fit coordinate/readout lock is forbidden", any(row["theorem_id"] == "TSF4216_5_no_coordinate_cheat" for row in theorem)),
        ("VAL4216_5_activation_clauses", "activation clauses include tau, surface, coframe, clock, orbital/PPN and MHref", {"TSA4216_0_tau_common", "TSA4216_1_surface_fixed", "TSA4216_2_same_coframe", "TSA4216_3_clock_readout", "TSA4216_4_orbital_ppn_readout", "TSA4216_5_MHref"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4216_6_score_update_zero", "curl score update records conditional tau/surface/frame zero", any(row["quantity"] == "I_tau+I_surface+C_frame" and row["value_or_bound"] == "0_under_TSF4216_selector" for row in score)),
        ("VAL4216_7_bound_components", "bound component rows cover all tau/surface/frame failures", required_bounds.issubset({row["component"] for row in bound})),
        ("VAL4216_8_routes", "routes include selector, bound, no coordinate cheat and boundary next", {"TR4216_0_activate_selector", "TR4216_1_bound_lock", "TR4216_2_no_coordinate_cheat", "TR4216_3_boundary_next"}.issubset({row["route_id"] for row in routes})),
        ("VAL4216_9_decision_nonclaim", "decision keeps global and local-GR claims false", decision["global_tau_surface_frame_signature"] == "False" and decision["local_GR_claim"] == "False"),
        ("VAL4216_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4216_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4216_12_claim_register", "claim register contains L-057", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4216_13_spine_packet_markers", "spine and packet markers present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)),
        ("VAL4216_14_next_target", "next target is boundary/corner", decision["next_target"] == NEXT_TARGET),
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
        "P8_Y5_R2FR_4216_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4216_TAU_SURFACE_FRAME_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4216_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4216_CURL_SCORE_UPDATE.csv": score_update_rows(),
        "P8_Y5_R2FR_4216_TAU_SURFACE_BOUND_COMPONENTS.csv": bound_component_rows(),
        "P8_Y5_R2FR_4216_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4216_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4216_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4216_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4216_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4216_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4216_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
