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

CHECKPOINT = "4217"
CLAIM_ID = "L-058"
BRANCH_ID = "MTS_R2FR_Y5_BOUNDARY_CORNER_CURL_ZERO_4217"
DECISION = (
    "BOUNDARY_CORNER_CURL_ZERO_CONDITIONALLY_DERIVED_FOR_DIFFERENTIABILITY_"
    "OWNED_NOFLUX_COLLAR_RADIATIVE_EDGE_FLUX_BOUND_ROW_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md"
DOC_PATH = POST / "4217-Y5-R2FR-boundary-corner-curl-zero-or-flux-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_BOUNDARY_CORNER_CURL_ZERO_4217"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_CORNER_CURL_ZERO_4217"
NEXT_TARGET = "4218-Y5-R2FR-visible-EM-material-curl-zero-or-residual-bound-row.md"

SOURCES = {
    "SRC4217_00_4216_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4216_NEXT_TARGET.csv",
        "4217-Y5-R2FR-boundary-corner-curl-zero-or-flux-bound-row.md",
        "4216 selected boundary/corner flux as next source-charge obstruction.",
    ),
    "SRC4217_01_4212_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv",
        "I_boundary+I_corner",
        "4212 retained boundary/corner curl component.",
    ),
    "SRC4217_02_4176_noflux": (
        SOURCE_DIR / "P8_Y5_R2FR_4176_NO_FLUX_THEOREM.csv",
        "NFT4176_3_Hamiltonian_boundary",
        "Local boundary no-flux Hamiltonian boundary clause.",
    ),
    "SRC4217_03_4061_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_BOUNDARY_REFERENCE_KERNEL_THEOREM.csv",
        "BND4061_0_differentiability_owner",
        "Boundary differentiability/reference owner theorem.",
    ),
    "SRC4217_04_4038_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "PNT4038_1_exterior_collar",
        "EM/Poynting no-flux collar theorem.",
    ),
    "SRC4217_05_3999_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_3999_FLUX_CLOSURE_THEOREM.csv",
        "FCT3999_3_flux_closure_theorem",
        "Hilbert mass flux closure theorem.",
    ),
    "SRC4217_06_4207_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv",
        "PO4207_5_radiative_route",
        "Radiative flux routes as boundary/Hamiltonian row.",
    ),
    "SRC4217_07_3982_surface": (
        SOURCE_DIR / "P8_Y5_R2FR_3982_CONTROLLED_SURFACE_EXCHANGE_ZERO_THEOREM.csv",
        "CSX3982_0_branch",
        "Controlled surface/exchange silence theorem.",
    ),
    "SRC4217_08_192_formal": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0",
        "Formal no-flux theorem radiative exception.",
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
            "BCC4217_0_boundary_one_form",
            "boundary/corner part of Hamiltonian one-form",
            "alpha_boundary(delta)=int_partialW(delta Q_tau-i_tau theta_total)_boundary + corner/improvement terms",
            "definition_imported",
            "the term is a Hamiltonian differentiability/accounting object, not a hidden bulk force",
        ),
        (
            "BCC4217_1_differentiability_owner",
            "differentiability-owned boundary",
            "GHY/exact/topological/reference terms are fixed by the variational principle and cancel derivative-of-delta-field pieces.",
            "conditional_zero_theorem",
            "boundary terms must be owned before variation, not chosen after readout",
        ),
        (
            "BCC4217_2_fixed_corner_data",
            "fixed corner and edge data",
            "corner boosts, normals, orientations, edge modes and improvement choices are fixed, exact, or explicitly routed.",
            "conditional_corner_theorem",
            "kills corner curl only if the corner is not a live dynamical edge mode",
        ),
        (
            "BCC4217_3_no_flux_collar",
            "compact stationary no-flux collar",
            "no source crossing, no imposed incoming radiation, no open-memory/cosmology pullback, and no wall/shear flux through the local collar.",
            "conditional_no_flux_theorem",
            "ordinary compact local tests do not receive hidden boundary current",
        ),
        (
            "BCC4217_4_poynting_once",
            "Poynting/radiative routing",
            "stationary bound EM stress is counted once in T_total; nonzero radiative Poynting is a boundary/Hamiltonian flux row.",
            "conditional_radiative_route",
            "radiation is not erased or double-counted",
        ),
        (
            "BCC4217_5_flux_identity",
            "annulus flux identity",
            "M_H[S2]-M_H[S1]=N_G int_A d(Pi_M J_H[tau]); if Ward current, projector transport and boundary/reference channels are silent, the flux vanishes.",
            "conditional_flux_closure",
            "surface independence follows from exact flux closure, not an assumed plateau",
        ),
        (
            "BCC4217_6_curl_zero",
            "boundary/corner curl zero",
            "I_boundary+I_corner=0 under BCC4217_1 through BCC4217_5.",
            "conditional_zero_theorem",
            "closes the 4212 boundary/corner numerator only inside the differentiability-owned no-flux selector",
        ),
        (
            "BCC4217_7_flux_bound_fallback",
            "boundary/corner fallback bound",
            "|I_boundary+I_corner|/M_H_ref <= (|R_diff_owner|+|R_corner_edge|+|R_rad_flux|+|R_source_crossing|+|R_memory_pullback|+|R_improvement|)/M_H_ref",
            "bound_row_retained",
            "live edges, radiation, source crossing and memory pullbacks are scored componentwise",
        ),
        (
            "BCC4217_8_nonclaim_guard",
            "public claim guard",
            "Full H_tau/Newton/local-GR closure remains false until visible EM/material residuals, Dq/coupling leakage and M_H_ref close.",
            "nonclaim_guard",
            "boundary/corner closure is not the whole source-charge theorem",
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
        ("BCA4217_0_differentiability_owner", "boundary terms are GHY/exact/topological/reference differentiability terms", "conditional_from_4061_4176", "R_diff_owner"),
        ("BCA4217_1_fixed_corner", "corner/edge mode data fixed, exact or routed", "conditional_selected_branch", "R_corner_edge"),
        ("BCA4217_2_no_flux", "stationary compact collar with no source/radiative crossing", "conditional_from_4176_3982_4038", "R_rad_flux;R_source_crossing"),
        ("BCA4217_3_poynting_once", "Poynting is Hilbert stress counted once; radiation routes to boundary row", "conditional_from_4207", "R_poynting_double_count;R_rad_flux"),
        ("BCA4217_4_memory_separation", "galaxy/cosmology/open-memory sectors have zero local pullback or are support-separated", "conditional_from_4176", "R_memory_pullback"),
        ("BCA4217_5_MHref", "M_H_ref exists before normalized scoring", "M_H_ref_missing_for_global_score", "MISSING_STABLE_MH_REF"),
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
            "BCU4217_0_I_boundary_corner",
            "I_boundary+I_corner",
            "boundary exact, corner, improvement and radiative flux contribution",
            "0_under_BCC4217_selector",
            "CONDITIONAL_ZERO_SELECTOR",
        ),
        (
            "BCU4217_1_boundary_flux_bound",
            "I_boundary_corner_bound",
            "(|R_diff_owner|+|R_corner_edge|+|R_rad_flux|+|R_source_crossing|+|R_memory_pullback|+|R_improvement|)/M_H_ref",
            "MISSING_GLOBAL_BOUNDARY_SIGNATURE_OR_MHREF",
            "BOUND_ROW_RETAINED",
        ),
        (
            "BCU4217_2_delta_Htau_update",
            "delta_H_tau_nonintegrable_over_MH",
            "4212 sum with I_qbasic_vertical, I_projector, I_ref, I_tau+I_surface+C_frame and I_boundary+I_corner removed only inside selectors; otherwise include fallback bounds",
            "PARTIAL_REDUCTION_NONCLAIM",
            "FULL_SCORE_REQUIRES_VISIBLE_EM_DQ_MHREF",
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
        ("BCB4217_0_R_diff_owner", "R_diff_owner", "boundary term not owned by differentiability/reference variational principle", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("BCB4217_1_R_corner_edge", "R_corner_edge", "live corner boost/edge mode/orientation/improvement curl", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("BCB4217_2_R_rad_flux", "R_rad_flux", "radiative EM/gravity/Poynting flux through local collar", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("BCB4217_3_R_source_crossing", "R_source_crossing", "matter/apparatus/source current crossing boundary", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("BCB4217_4_R_memory_pullback", "R_memory_pullback", "galaxy/cosmology/open-memory sector pullback into local collar", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("BCB4217_5_R_improvement", "R_improvement", "unfixed exact/improvement/corner convention with nonzero surface integral", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("BCB4217_6_M_H_ref", "M_H_ref", "positive same-frame Hamiltonian source denominator", "MISSING_STABLE_MH_REF"),
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
            "BR4217_0_activate_selector",
            "Activate boundary/corner zero selector",
            "use I_boundary+I_corner=0 only when boundary terms are differentiability-owned, corners fixed and collar no-flux",
            "removes fifth retained 4212 curl numerator conditionally",
        ),
        (
            "BR4217_1_bound_flux",
            "Fill boundary flux bound row",
            "if any boundary/corner clause fails, score R_diff/R_corner/R_rad/R_source/R_memory/R_improvement over M_H_ref",
            "keeps edge/radiation physics explicit",
        ),
        (
            "BR4217_2_no_radiation_erasure",
            "Forbid radiation erasure",
            "nonzero EM/gravity/radiative Poynting flux routes to boundary/Hamiltonian row, not local bulk zero",
            "protects real radiation sectors",
        ),
        (
            "BR4217_3_visible_EM_next",
            "Attack visible EM/material residual next",
            "derive or bound I_matter_EM after boundary/corner term is conditionally handled",
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
            "decision_id": "DEC4217_0",
            "decision": DECISION,
            "I_boundary_corner_closed_inside_selector": "True",
            "global_boundary_corner_signature": "False",
            "radiation_erasure_allowed": "False",
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
        ("FW4217_0_global_boundary", "global boundary/corner zero", "blocked_until_differentiability_owner_fixed_corner_no_flux_and_MHref_parent_signed"),
        ("FW4217_1_radiation", "radiation erasure", "forbidden_if_EM_gravity_or_memory_flux_is_nonzero"),
        ("FW4217_2_Htau", "full H_tau integrability", "blocked_until_visible_EM_Dq_and_MHref_close"),
        ("FW4217_3_Newton", "Newton/local-GR source bridge", "blocked_until_Htau_integrability_and_M_H_ref_close"),
        ("FW4217_4_public", "public local-GR claim", "blocked_private_conditional_theorem_only"),
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
            "status_id": "STATUS4217",
            "status": "boundary_corner_curl_conditionally_zero_selector_nonclaim",
            "strong_result": "I_boundary+I_corner is zero when boundary terms are differentiability-owned, corner data fixed/exact/routed and the local collar has no flux crossing",
            "remaining_gap": "global boundary adoption, M_H_ref and remaining visible EM/material and Dq/coupling curl terms remain unsigned",
            "project_effect": "fifth retained 4212 curl numerator is conditionally removed; next target is visible EM/material residual",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4217 conditionally closes the boundary/corner curl term; the next retained source-charge obstruction is visible EM/material/current residual.",
            "route_A": "derive I_matter_EM=0 from standard visible matter import, Maxwell-Hodge owner, current owner and no radiative double-count",
            "route_B": "if not zero, fill visible EM/material residual over M_H_ref as the next bound row",
            "route_C": "keep qbasic, projector, reference, tau/frame and boundary selector caveats attached to the reduced curl sum",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 233 - PPC4161 boundary/corner curl zero or flux bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

4212 retained:

```text
I_boundary + I_corner.
```

4217 proves the conditional zero route for differentiability-owned boundaries and fixed/no-flux local collars.

## Boundary One-Form

The boundary part of the Hamiltonian one-form is:

```text
alpha_boundary(delta)
= int_partialW (delta Q_tau - i_tau theta_total)_boundary
  + corner/exact/improvement terms.
```

It vanishes as an independent curl source only when those terms are owned by the variational principle, fixed corner data, or routed flux rows.

## Zero Theorem

Assume:

1. boundary terms are GHY/exact/topological/reference differentiability terms;
2. corner boosts, normals, orientations, edge modes and improvements are fixed, exact, or explicitly routed;
3. the compact local collar has no source crossing, no imposed incoming radiation, and no open-memory/cosmology pullback;
4. stationary bound EM/Poynting stress is counted once in `T_total`;
5. any live radiative EM/gravity/Poynting flux is routed as a boundary/Hamiltonian row.

Then:

```text
I_boundary + I_corner = 0.
```

## No Radiation Erasure

The theorem does not erase radiation. If:

```text
F_rad[tau] != 0,
```

then the term is retained as boundary/Hamiltonian flux, not converted into a hidden bulk force and not silently set to zero.

## Fallback Bound

If any clause fails:

```text
|I_boundary+I_corner|/M_H_ref
<= (|R_diff_owner|
 + |R_corner_edge|
 + |R_rad_flux|
 + |R_source_crossing|
 + |R_memory_pullback|
 + |R_improvement|) / M_H_ref.
```

## Reduced Curl Status

Inside the 4213 through 4217 selectors, the reduced 4212 numerator drops:

```text
I_qbasic_vertical,
I_projector,
I_ref,
I_tau+I_surface+C_frame,
I_boundary+I_corner.
```

The full source-charge theorem still requires:

- `I_matter_EM`;
- `I_Dq`;
- stable positive `M_H_ref`.

## Next Target

`{NEXT_TARGET}` should attack:

```text
I_matter_EM.
```
"""


def checkpoint_doc() -> str:
    return f"""# 4217 Y5 R2FR boundary corner curl zero or flux bound row

**Status:** `{DECISION}`.

**Forward move:** the boundary/corner curl term is conditionally zero:

```text
differentiability-owned boundary + fixed corner data + no-flux collar
=> I_boundary+I_corner=0.
```

Radiation is not erased. Nonzero radiative, source-crossing, memory-pullback or edge-mode flux remains a bound row.

## Files written

- `formalization-workbench\\233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4217_BOUNDARY_CORNER_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4217_BOUNDARY_FLUX_COMPONENTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4217_DECISION.csv`

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
        f'"The boundary/corner Hamiltonian curl term is conditionally closed: when boundary terms are differentiability-owned, corner data are fixed/exact/routed, and the compact local collar has no source/radiative/memory flux crossing, I_boundary+I_corner=0; otherwise live edge, radiation, source-crossing and improvement terms are retained as componentwise flux bounds.",'
        f'"4217 source audit, boundary/corner theorem, activation clauses, flux components, curl score update, route matrix, decision row and firewall.",'
        f'private_boundary_corner_curl_zero_conditional_nonclaim,'
        f'"Attack visible EM/material/current residual I_matter_EM, or fill it as the next source-charge bound row.",'
        f'"No-flux is a local selector, not a radiation eraser; nonzero boundary flux remains physical and scored."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 boundary/corner curl zero - 4217

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4217 conditionally closes the 4212 boundary/corner curl:

```text
differentiability-owned boundary + fixed corner data + no-flux collar
=> I_boundary+I_corner=0.
```

Nonzero radiative/source-crossing/memory/edge flux is not erased; it remains a boundary/Hamiltonian bound row."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet boundary/corner curl zero - 4217

Marker: `{PACKET_MARKER}`

The packet now has conditional zero theorems for `I_qbasic_vertical`, `I_projector`, `I_ref`, `I_tau+I_surface+C_frame`, and `I_boundary+I_corner`. Next retained obstruction: visible EM/material residual."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4217_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4217_BOUNDARY_CORNER_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4217_ACTIVATION_CLAUSES.csv"]
    score = rows_by_file["P8_Y5_R2FR_4217_CURL_SCORE_UPDATE.csv"]
    bound = rows_by_file["P8_Y5_R2FR_4217_BOUNDARY_FLUX_COMPONENTS.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4217_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4217_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "BCC4217_0_boundary_one_form",
        "BCC4217_1_differentiability_owner",
        "BCC4217_2_fixed_corner_data",
        "BCC4217_3_no_flux_collar",
        "BCC4217_4_poynting_once",
        "BCC4217_5_flux_identity",
        "BCC4217_6_curl_zero",
        "BCC4217_7_flux_bound_fallback",
        "BCC4217_8_nonclaim_guard",
    }
    required_bounds = {
        "R_diff_owner",
        "R_corner_edge",
        "R_rad_flux",
        "R_source_crossing",
        "R_memory_pullback",
        "R_improvement",
        "M_H_ref",
    }
    checks = [
        ("VAL4217_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4217_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4217_2_theorem_complete", "boundary/corner theorem contains all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4217_3_curl_zero_clause", "I_boundary+I_corner zero clause exists", any(row["theorem_id"] == "BCC4217_6_curl_zero" and row["status"] == "conditional_zero_theorem" for row in theorem)),
        ("VAL4217_4_radiation_guard", "radiation erasure guard exists", any(row["theorem_id"] == "BCC4217_4_poynting_once" for row in theorem)),
        ("VAL4217_5_activation_clauses", "activation clauses include differentiability, corner, no-flux, poynting, memory and MHref", {"BCA4217_0_differentiability_owner", "BCA4217_1_fixed_corner", "BCA4217_2_no_flux", "BCA4217_3_poynting_once", "BCA4217_4_memory_separation", "BCA4217_5_MHref"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4217_6_score_update_zero", "curl score update records conditional boundary/corner zero", any(row["quantity"] == "I_boundary+I_corner" and row["value_or_bound"] == "0_under_BCC4217_selector" for row in score)),
        ("VAL4217_7_bound_components", "bound component rows cover all boundary/corner failures", required_bounds.issubset({row["component"] for row in bound})),
        ("VAL4217_8_routes", "routes include selector, bound, no radiation erasure and visible EM next", {"BR4217_0_activate_selector", "BR4217_1_bound_flux", "BR4217_2_no_radiation_erasure", "BR4217_3_visible_EM_next"}.issubset({row["route_id"] for row in routes})),
        ("VAL4217_9_decision_nonclaim", "decision keeps global and local-GR claims false", decision["global_boundary_corner_signature"] == "False" and decision["local_GR_claim"] == "False"),
        ("VAL4217_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4217_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4217_12_claim_register", "claim register contains L-058", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4217_13_spine_packet_markers", "spine and packet markers present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)),
        ("VAL4217_14_next_target", "next target is visible EM/material residual", decision["next_target"] == NEXT_TARGET),
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
        "P8_Y5_R2FR_4217_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4217_BOUNDARY_CORNER_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4217_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4217_CURL_SCORE_UPDATE.csv": score_update_rows(),
        "P8_Y5_R2FR_4217_BOUNDARY_FLUX_COMPONENTS.csv": bound_component_rows(),
        "P8_Y5_R2FR_4217_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4217_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4217_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4217_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4217_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4217_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4217_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
