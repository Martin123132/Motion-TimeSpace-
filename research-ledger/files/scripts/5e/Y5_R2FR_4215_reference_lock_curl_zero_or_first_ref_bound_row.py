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

CHECKPOINT = "4215"
CLAIM_ID = "L-056"
BRANCH_ID = "MTS_R2FR_Y5_REFERENCE_LOCK_CURL_ZERO_4215"
DECISION = (
    "REFERENCE_LOCK_CURL_ZERO_CONDITIONALLY_DERIVED_FOR_PARENT_SELECTED_"
    "SOURCE_BLIND_HREF_DELTA_REF_BOUND_ROW_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "231-PPC4161-reference-lock-curl-zero-or-bound.md"
DOC_PATH = POST / "4215-Y5-R2FR-reference-lock-curl-zero-or-first-ref-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_REFERENCE_LOCK_CURL_ZERO_4215"
PACKET_MARKER = "PPC4161_PACKET_REFERENCE_LOCK_CURL_ZERO_4215"
NEXT_TARGET = "4216-Y5-R2FR-tau-surface-frame-lock-or-curl-bound-row.md"

SOURCES = {
    "SRC4215_00_4214_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4214_NEXT_TARGET.csv",
        "4215-Y5-R2FR-reference-lock-curl-zero-or-first-ref-bound-row.md",
        "4214 selected reference curl as next source-charge obstruction.",
    ),
    "SRC4215_01_4212_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv",
        "I_ref",
        "4212 retained reference curl component.",
    ),
    "SRC4215_02_4002_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv",
        "HIR4002_3_fixed_reference_selector",
        "Exact Htau/Href reference selector theorem.",
    ),
    "SRC4215_03_4002_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4002_CURL_REFERENCE_BOUND_VECTOR.csv",
        "HRB4002_4_I_ref_Delta_ref",
        "Reference curl/fallback bound row.",
    ),
    "SRC4215_04_4158_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM.csv",
        "BRL4158_7_verdict",
        "Boundary/reference lock theorem and unsigned packet caveat.",
    ),
    "SRC4215_05_4061_kernel": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_BOUNDARY_REFERENCE_KERNEL_THEOREM.csv",
        "BND4061_1_reference_lock",
        "Selected reference lock branch.",
    ),
    "SRC4215_06_4211_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4211_HTAU_MHSOURCE_OWNER_CONTRACT.csv",
        "HMO4211_4_reference_lock",
        "4211 source-charge owner reference clause.",
    ),
    "SRC4215_07_230_formal": (
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "I_ref = curl(-delta H_ref)",
        "4214 formal next target.",
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
            "RLC4215_0_alpha_reference_piece",
            "reference piece in Hamiltonian one-form",
            "alpha_tau,S(delta)=int_S(delta Q_tau-i_tau theta_total(delta))-delta H_ref",
            "definition_imported",
            "I_ref is precisely the field-space curl of the reference subtraction term",
        ),
        (
            "RLC4215_1_fixed_parent_reference",
            "parent-selected reference object",
            "H_ref=H_ref[Sigma_ref,B_ref,tau_ref,e_ref] is chosen before source/radius/frame/readout variation.",
            "conditional_reference_lock",
            "reference data may be boundary/topology/asymptotic data, not a fitted GM counterterm",
        ),
        (
            "RLC4215_2_derivative_silence",
            "source-blind derivative silence",
            "D_source H_ref=D_radius H_ref=D_frame H_ref=D_readout H_ref=0 on the selected branch.",
            "conditional_zero_theorem",
            "prevents H_ref from absorbing measured source drift",
        ),
        (
            "RLC4215_3_exact_one_form",
            "exact reference one-form",
            "If H_ref is a fixed functional on the allowed branch, then d_field(delta H_ref)=0.",
            "mathematical_exactness_theorem",
            "field-space exterior derivative squares to zero for a genuine fixed functional",
        ),
        (
            "RLC4215_4_reference_curl_zero",
            "reference curl zero",
            "I_ref := curl(-delta H_ref)=0 under RLC4215_1 through RLC4215_3.",
            "conditional_zero_theorem",
            "closes the 4212 reference numerator inside the fixed-reference selector",
        ),
        (
            "RLC4215_5_no_refit_guard",
            "no post-fit counterterm",
            "H_ref cannot be chosen from orbital GM, fitted acceleration, PPN residuals, R10 residuals, or observed source mismatch.",
            "anti_circularity_guard",
            "otherwise the reference subtraction erases the effect it is supposed to test",
        ),
        (
            "RLC4215_6_boundary_monopole_guard",
            "boundary/free monopole guard",
            "source-free homogeneous or boundary monopoles are zero only if outer reference plus inner charge/no-flux clauses are adopted.",
            "conditional_boundary_guard",
            "unfixed boundary monopoles remain Delta_ref/I_boundary rows",
        ),
        (
            "RLC4215_7_bound_fallback",
            "reference fallback bound",
            "|I_ref+Delta_ref|/M_H_ref <= (|R_ref_selector|+|R_ref_source|+|R_ref_radius|+|R_ref_frame|+|R_ref_fit|+|R_ref_boundary|)/M_H_ref",
            "bound_row_retained",
            "reference lock failures are scored componentwise with no cancellation credit",
        ),
        (
            "RLC4215_8_nonclaim_guard",
            "public claim guard",
            "Full H_tau/Newton/local-GR closure remains false until M_H_ref, tau/surface, boundary/corner, visible EM and Dq terms also close.",
            "nonclaim_guard",
            "reference curl zero is not the full source-charge theorem",
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
            "RLA4215_0_reference_selector",
            "Sigma_ref/B_ref selected by parent branch before variation",
            "conditional_from_4002_4061_4158",
            "R_ref_selector",
        ),
        (
            "RLA4215_1_source_blind",
            "D_source H_ref=D_readout H_ref=0",
            "conditional_selected_branch",
            "R_ref_source;R_ref_readout",
        ),
        (
            "RLA4215_2_radius_frame_blind",
            "D_radius H_ref=D_frame H_ref=0",
            "conditional_selected_branch",
            "R_ref_radius;R_ref_frame",
        ),
        (
            "RLA4215_3_no_fit_counterterm",
            "reference not selected from orbital GM/PPN/R10 residuals",
            "active_guard",
            "R_ref_fit",
        ),
        (
            "RLA4215_4_boundary_monopole",
            "homogeneous/reference boundary modes fixed or charge-routed",
            "conditional_from_4158",
            "R_ref_boundary;I_boundary",
        ),
        (
            "RLA4215_5_MHref",
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
            "RSU4215_0_I_ref",
            "I_ref",
            "curl(-delta H_ref)",
            "0_under_RLC4215_selector",
            "CONDITIONAL_ZERO_SELECTOR",
        ),
        (
            "RSU4215_1_Delta_ref_bound",
            "I_ref_plus_Delta_ref_bound",
            "(|R_ref_selector|+|R_ref_source|+|R_ref_radius|+|R_ref_frame|+|R_ref_fit|+|R_ref_boundary|)/M_H_ref",
            "MISSING_GLOBAL_REFERENCE_SIGNATURE_OR_MHREF",
            "BOUND_ROW_RETAINED",
        ),
        (
            "RSU4215_2_delta_Htau_update",
            "delta_H_tau_nonintegrable_over_MH",
            "4212 sum with I_qbasic_vertical, I_projector and I_ref removed only inside their selectors; otherwise include fallback bounds",
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
        ("RCB4215_0_R_ref_selector", "R_ref_selector", "reference branch not parent-selected before variation", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("RCB4215_1_R_ref_source", "R_ref_source", "source/readout dependence of H_ref", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("RCB4215_2_R_ref_radius", "R_ref_radius", "radial/surface-family drift of H_ref", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("RCB4215_3_R_ref_frame", "R_ref_frame", "frame/tau/coframe dependence of H_ref", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("RCB4215_4_R_ref_fit", "R_ref_fit", "post-fit counterterm chosen from observed residuals", "FORBIDDEN_IF_NONZERO"),
        ("RCB4215_5_R_ref_boundary", "R_ref_boundary", "unfixed homogeneous/boundary/reference monopole", "MISSING_OR_ZERO_UNDER_SELECTOR"),
        ("RCB4215_6_M_H_ref", "M_H_ref", "positive same-frame Hamiltonian source denominator", "MISSING_STABLE_MH_REF"),
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
            "RR4215_0_activate_selector",
            "Activate fixed-reference zero selector",
            "use I_ref=0 only when H_ref is parent-selected, source-blind, radius/frame/readout silent and not fit from observations",
            "removes third retained 4212 curl numerator conditionally",
        ),
        (
            "RR4215_1_bound_reference",
            "Fill reference bound row",
            "if any reference clause fails, score R_ref_selector/source/radius/frame/fit/boundary over M_H_ref",
            "keeps reference debt empirical rather than hidden",
        ),
        (
            "RR4215_2_no_counterterm",
            "Forbid post-fit counterterm",
            "never use H_ref to cancel orbital GM, PPN, R10, clock or source residuals",
            "protects anti-circularity",
        ),
        (
            "RR4215_3_tau_surface_next",
            "Attack tau/surface lock next",
            "derive fixed tau/surface/frame lock or score I_tau+I_surface",
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
            "decision_id": "DEC4215_0",
            "decision": DECISION,
            "I_ref_closed_inside_selector": "True",
            "global_reference_parent_signature": "False",
            "post_fit_counterterm_allowed": "False",
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
        ("FW4215_0_global_reference", "global I_ref zero", "blocked_until_reference_selector_source_blind_radius_frame_boundary_and_MHref_parent_signed"),
        ("FW4215_1_counterterm", "post-fit reference counterterm", "forbidden_if_chosen_from_observed_residuals"),
        ("FW4215_2_Htau", "full H_tau integrability", "blocked_until_tau_surface_boundary_visible_Dq_and_MHref_close"),
        ("FW4215_3_Newton", "Newton/local-GR source bridge", "blocked_until_Htau_integrability_and_M_H_ref_close"),
        ("FW4215_4_public", "public local-GR claim", "blocked_private_conditional_theorem_only"),
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
            "status_id": "STATUS4215",
            "status": "reference_curl_conditionally_zero_selector_nonclaim",
            "strong_result": "I_ref is zero when H_ref is a parent-selected fixed source-blind reference functional because d_field(delta H_ref)=0",
            "remaining_gap": "global reference adoption, boundary monopole charge matching, M_H_ref and remaining tau/surface, boundary/corner, visible EM and Dq curl terms remain unsigned",
            "project_effect": "third retained 4212 curl numerator is conditionally removed; next target is tau/surface/frame lock",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4215 conditionally closes the reference curl term; the next retained source-charge obstruction is tau/surface/frame lock.",
            "route_A": "derive tau_source=tau_charge=tau_clock=tau_readout and fixed surface family before variation",
            "route_B": "if not zero, fill I_tau+I_surface+C_frame over M_H_ref as the next bound row",
            "route_C": "keep qbasic, projector and reference selector caveats attached to the reduced curl sum",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 231 - PPC4161 reference-lock curl zero or bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

4212 retained:

```text
I_ref = curl(-delta H_ref).
```

4215 proves the clean zero route and retains the bound route if the reference is unfixed, branch-dependent, or post-fit.

## Reference One-Form

The Hamiltonian one-form is:

```text
alpha_tau,S(delta)
= int_S(delta Q_tau - i_tau theta_total(delta))
  - delta H_ref.
```

If `H_ref` is a fixed parent-selected functional on the allowed local branch, then:

```text
d_field(delta H_ref) = 0
I_ref := curl(-delta H_ref) = 0.
```

This is a mathematical exactness statement, not a numerical fit.

## Activation Clauses

The zero theorem is active only if:

1. `Sigma_ref`/`B_ref` is selected by the parent branch before variation;
2. `D_source H_ref = D_readout H_ref = 0`;
3. `D_radius H_ref = D_frame H_ref = 0`;
4. no orbital `GM`, PPN, R10, clock, or source residual is used to choose `H_ref`;
5. homogeneous/free boundary monopoles are fixed, zero, or charge-routed;
6. `M_H_ref` exists before any normalized score is claimed.

## Fallback Bound

If any clause fails:

```text
|I_ref + Delta_ref|/M_H_ref
<= (|R_ref_selector|
 + |R_ref_source|
 + |R_ref_radius|
 + |R_ref_frame|
 + |R_ref_fit|
 + |R_ref_boundary|) / M_H_ref.
```

`R_ref_fit` is not a tunable parameter. If nonzero, the reference route is contaminated and must be reported.

## Reduced Curl Status

Inside the 4213, 4214, and 4215 selectors, the reduced 4212 numerator drops:

```text
I_qbasic_vertical, I_projector, I_ref.
```

The full source-charge theorem still requires:

- `I_tau+I_surface`;
- `I_boundary+I_corner`;
- `I_matter_EM`;
- `I_Dq`;
- stable positive `M_H_ref`.

## Next Target

`{NEXT_TARGET}` should attack:

```text
I_tau + I_surface + C_frame.
```
"""


def checkpoint_doc() -> str:
    return f"""# 4215 Y5 R2FR reference-lock curl zero or first ref bound row

**Status:** `{DECISION}`.

**Forward move:** `I_ref` is conditionally zero for a parent-selected fixed source-blind reference:

```text
H_ref fixed before source/radius/frame/readout variation
=> d_field(delta H_ref)=0
=> I_ref=curl(-delta H_ref)=0.
```

If `H_ref` is fitted from observed residuals or drifts with source/readout/radius/frame, it is not a reference; it is a residual counterterm and must be scored.

## Files written

- `formalization-workbench\\231-PPC4161-reference-lock-curl-zero-or-bound.md`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4215_REFERENCE_LOCK_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4215_REFERENCE_BOUND_COMPONENTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4215_DECISION.csv`

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
        f'"The reference-lock Hamiltonian curl term is conditionally closed: when H_ref is a parent-selected fixed source-blind reference functional chosen before source, radius, frame and readout variation, d_field(delta H_ref)=0 and I_ref=0; unfixed, drifting or post-fit references are retained as I_ref+Delta_ref bound rows.",'
        f'"4215 source audit, reference-lock theorem, activation clauses, bound components, curl score update, route matrix, decision row and firewall.",'
        f'private_reference_lock_curl_zero_conditional_nonclaim,'
        f'"Attack tau/surface/frame lock I_tau+I_surface+C_frame, or fill it as the next source-charge bound row.",'
        f'"A fixed reference is legal; a reference chosen to cancel observed residuals is circular."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 reference-lock curl zero - 4215

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4215 conditionally closes the 4212 reference curl:

```text
H_ref fixed before variation
=> d_field(delta H_ref)=0
=> I_ref=0.
```

If the reference drifts with source, radius, frame, readout, boundary monopole, or fitted residuals, it remains an `I_ref+Delta_ref` bound row."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet reference-lock curl zero - 4215

Marker: `{PACKET_MARKER}`

The packet now has conditional zero theorems for `I_qbasic_vertical`, `I_projector`, and `I_ref`. Next retained obstruction: tau/surface/frame lock."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4215_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4215_REFERENCE_LOCK_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4215_ACTIVATION_CLAUSES.csv"]
    score = rows_by_file["P8_Y5_R2FR_4215_CURL_SCORE_UPDATE.csv"]
    bound = rows_by_file["P8_Y5_R2FR_4215_REFERENCE_BOUND_COMPONENTS.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4215_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4215_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "RLC4215_0_alpha_reference_piece",
        "RLC4215_1_fixed_parent_reference",
        "RLC4215_2_derivative_silence",
        "RLC4215_3_exact_one_form",
        "RLC4215_4_reference_curl_zero",
        "RLC4215_5_no_refit_guard",
        "RLC4215_6_boundary_monopole_guard",
        "RLC4215_7_bound_fallback",
        "RLC4215_8_nonclaim_guard",
    }
    required_bounds = {
        "R_ref_selector",
        "R_ref_source",
        "R_ref_radius",
        "R_ref_frame",
        "R_ref_fit",
        "R_ref_boundary",
        "M_H_ref",
    }
    checks = [
        ("VAL4215_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4215_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4215_2_theorem_complete", "reference theorem contains all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4215_3_curl_zero_clause", "I_ref zero clause exists", any(row["theorem_id"] == "RLC4215_4_reference_curl_zero" and row["status"] == "conditional_zero_theorem" for row in theorem)),
        ("VAL4215_4_no_refit_guard", "post-fit counterterm is forbidden", any(row["theorem_id"] == "RLC4215_5_no_refit_guard" for row in theorem)),
        ("VAL4215_5_activation_clauses", "activation clauses include selector, source, radius/frame, no fit, boundary and MHref", {"RLA4215_0_reference_selector", "RLA4215_1_source_blind", "RLA4215_2_radius_frame_blind", "RLA4215_3_no_fit_counterterm", "RLA4215_4_boundary_monopole", "RLA4215_5_MHref"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4215_6_score_update_zero", "curl score update records conditional reference zero", any(row["quantity"] == "I_ref" and row["value_or_bound"] == "0_under_RLC4215_selector" for row in score)),
        ("VAL4215_7_bound_components", "bound component rows cover all reference failures", required_bounds.issubset({row["component"] for row in bound})),
        ("VAL4215_8_routes", "routes include selector, bound, no counterterm and tau next", {"RR4215_0_activate_selector", "RR4215_1_bound_reference", "RR4215_2_no_counterterm", "RR4215_3_tau_surface_next"}.issubset({row["route_id"] for row in routes})),
        ("VAL4215_9_decision_nonclaim", "decision keeps global and local-GR claims false", decision["global_reference_parent_signature"] == "False" and decision["local_GR_claim"] == "False"),
        ("VAL4215_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4215_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4215_12_claim_register", "claim register contains L-056", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4215_13_spine_packet_markers", "spine and packet markers present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)),
        ("VAL4215_14_next_target", "next target is tau/surface lock", decision["next_target"] == NEXT_TARGET),
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
        "P8_Y5_R2FR_4215_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4215_REFERENCE_LOCK_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4215_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4215_CURL_SCORE_UPDATE.csv": score_update_rows(),
        "P8_Y5_R2FR_4215_REFERENCE_BOUND_COMPONENTS.csv": bound_component_rows(),
        "P8_Y5_R2FR_4215_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4215_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4215_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4215_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4215_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4215_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4215_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
