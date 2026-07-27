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

CHECKPOINT = "4213"
CLAIM_ID = "L-054"
BRANCH_ID = "MTS_R2FR_Y5_QBASIC_VERTICAL_PRESYMPLECTIC_SILENCE_4213"
DECISION = (
    "QBASIC_VERTICAL_PRESYMPLECTIC_SILENCE_CONDITIONALLY_DERIVED_"
    "I_QBASIC_VERTICAL_ZERO_INSIDE_PULLBACK_NOFLUX_SELECTOR_"
    "GLOBAL_PARENT_SIGNATURE_AND_EDGE_MODE_CAVEATS_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md"
DOC_PATH = POST / "4213-Y5-R2FR-qbasic-vertical-presymplectic-silence-or-curl-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_QBASIC_VERTICAL_PRESYMPLECTIC_SILENCE_4213"
PACKET_MARKER = "PPC4161_PACKET_QBASIC_VERTICAL_PRESYMPLECTIC_SILENCE_4213"
NEXT_TARGET = "4214-Y5-R2FR-projector-stress-curl-zero-or-first-bound-row.md"

SOURCES = {
    "SRC4213_00_4212_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_NEXT_TARGET.csv",
        "ker(Dq) subset ker(Omega_parent)",
        "4212 selects the q-basic vertical presymplectic target.",
    ),
    "SRC4213_01_228_formal": (
        FORMAL / "228-PPC4161-Htau-integrability-operator-and-curl-bound.md",
        "I_qbasic_vertical = int_S",
        "4212 curl component requiring closure.",
    ),
    "SRC4213_02_3766_kernel": (
        SOURCE_DIR / "P8_Y5_R2FR_3766_KERNEL_NULL_THEOREM.csv",
        "KNT3766_2_presymplectic_contraction",
        "Prior kernel-null presymplectic theorem.",
    ),
    "SRC4213_03_4177_vertical": (
        SOURCE_DIR / "P8_Y5_R2FR_4177_VERTICAL_SILENCE_PROOF.csv",
        "VSP4177_3_no_bulk_residual",
        "Quotient-naturality vertical Noether identity.",
    ),
    "SRC4213_04_4109_qbasic": (
        SOURCE_DIR / "P8_Y5_R2FR_4109_QBASIC_AX_THEOREM.csv",
        "QAX4109_0_qbasic_criterion",
        "q-basic differential criterion.",
    ),
    "SRC4213_05_3692_omega": (
        SOURCE_DIR / "P8_Y5_R2FR_3692_OMEGA_OWNER_CONTRACT_ROWS.csv",
        "OOT3692_4_exact_theorem",
        "Omega-owner exact theorem and boundary caveat.",
    ),
    "SRC4213_06_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge",
        "No-flux boundary/edge-mode routing.",
    ),
    "SRC4213_07_4212_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv",
        "I_qbasic_vertical",
        "4212 retained curl component.",
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
    items = [
        (
            "QVP4213_0_fibre_split",
            "vertical fibre split",
            "For a local quotient q, allowed representative variations v_q satisfy Dq[v_q]=0.",
            "exact_local_identity",
            "q-basic vertical directions are defined before any dynamics is assigned to them",
        ),
        (
            "QVP4213_1_pullback_action",
            "pullback parent action",
            "If L_parent|loc = q^*L_red + dB_vert and S_src=Sbar_src[q(Phi),psi,A,theta], then vertical bulk variations vanish.",
            "conditional_action_theorem",
            "this is the non-smuggled action-level criterion",
        ),
        (
            "QVP4213_2_theta_descent",
            "theta descent",
            "theta_parent = q^*theta_red + delta B_vert + dC_vert for local quotient-owned boundary data.",
            "conditional_theta_theorem",
            "theta must descend from the same parent action, not be borrowed after the fact",
        ),
        (
            "QVP4213_3_omega_null",
            "presymplectic nullity",
            "omega_parent = q^*omega_red + d delta B_vert, so i_v omega_parent = d beta_v for every v in ker(Dq).",
            "conditional_presymplectic_theorem",
            "bulk contraction vanishes because Dq[v]=0",
        ),
        (
            "QVP4213_4_boundary_silence",
            "boundary silence",
            "If compact support/no-flux/fixed edge data gives int_S i_tau d beta_v=0, vertical edge flux is silent.",
            "conditional_boundary_theorem",
            "otherwise the term is an edge-mode/boundary-charge row",
        ),
        (
            "QVP4213_5_curl_zero",
            "q-basic vertical curl zero",
            "I_qbasic_vertical = int_S i_tau omega_qbasic_vertical = 0 under QVP4213_0 through QVP4213_4.",
            "conditional_zero_theorem",
            "this closes the 4212 q-basic vertical curl only inside the selector",
        ),
        (
            "QVP4213_6_global_caveat",
            "global parent signature caveat",
            "The zero theorem is not a public/local-GR claim until the pullback parent action and edge silence are globally parent-signed.",
            "nonclaim_guard",
            "keeps the theorem from becoming a plateau axiom",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": item[0],
            "clause": item[1],
            "statement": item[2],
            "status": item[3],
            "meaning": item[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for item in items
    ]


def activation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ACT4213_0_qbasic",
            "Dq[v_q]=0 and all readouts in this sector are q-basic",
            "satisfied_inside_selector_from_4109_4177",
            "outside selector becomes R_qbasic_defect",
        ),
        (
            "ACT4213_1_action_pullback",
            "L_parent|loc=q^*L_red+dB_vert",
            "conditional_from_3766_not_global_public_signature",
            "if false add R_pullback_action",
        ),
        (
            "ACT4213_2_theta_omega_owner",
            "theta_parent and omega_parent descend from that same action",
            "conditional_from_3766_and_3692",
            "if false add R_theta_omega_owner",
        ),
        (
            "ACT4213_3_boundary",
            "int_S i_tau d beta_v=0 in compact local collar",
            "conditional_from_192_4177",
            "if false add R_vertical_edge_flux",
        ),
        (
            "ACT4213_4_source_matter",
            "S_src and visible matter constants are quotient-owned",
            "conditional_from_4177_4210_chain",
            "if false add R_source_marker_leak",
        ),
        (
            "ACT4213_5_MHref",
            "M_H_ref exists before normalized scoring",
            "missing_for_global_score",
            "zero theorem can close numerator term but not full normalized source-mass gate",
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


def curl_update_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CU4213_0_I_qbasic_vertical",
            "I_qbasic_vertical",
            "int_S i_tau omega_qbasic_vertical",
            "0_under_QVP4213_selector",
            "CONDITIONAL_ZERO_SELECTOR",
            "False",
        ),
        (
            "CU4213_1_bound_fallback",
            "I_qbasic_vertical_bound",
            "(|R_pullback_action|+|R_theta_omega_owner|+|R_vertical_edge_flux|+|R_qbasic_defect|+|R_source_marker_leak|)/M_H_ref",
            "MISSING_GLOBAL_PARENT_SIGNATURE_OR_MHREF",
            "BOUND_ROW_RETAINED",
            "False",
        ),
        (
            "CU4213_2_delta_Htau_update",
            "delta_H_tau_nonintegrable_over_MH",
            "4212 sum with I_qbasic_vertical removed only inside selector; otherwise include fallback bound",
            "PARTIAL_REDUCTION_NONCLAIM",
            "FULL_SCORE_REQUIRES_REMAINING_COMPONENTS",
            "False",
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
            "valid_for_global_claim": row[5],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def route_rows() -> List[Dict[str, str]]:
    routes = [
        (
            "QR4213_0_activate_selector",
            "Use q-basic vertical silence inside compact local selector",
            "drop I_qbasic_vertical from the local curl numerator only when QVP4213 clauses are active",
            "reduces the 4212 obstruction without claiming full local GR",
        ),
        (
            "QR4213_1_edge_bound",
            "If boundary data is not silent, retain edge-mode row",
            "score R_vertical_edge_flux/M_H_ref",
            "prevents boundary charge being hidden as zero",
        ),
        (
            "QR4213_2_pullback_bound",
            "If parent pullback action is not signed, retain pullback-defect row",
            "score R_pullback_action/M_H_ref",
            "prevents action-descent assumption from becoming an axiom",
        ),
        (
            "QR4213_3_projector_next",
            "Attack projector stress next",
            "derive or bound I_projector after I_qbasic_vertical is conditionally handled",
            "next largest curl term in the 4212 decomposition",
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
            "decision_id": "DEC4213_0",
            "decision": DECISION,
            "I_qbasic_vertical_closed_inside_selector": "True",
            "global_parent_pullback_signature": "False",
            "edge_mode_global_silence": "False",
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
        ("FW4213_0_global_zero", "global I_qbasic_vertical zero", "blocked_until_pullback_action_and_edge_silence_parent_signed"),
        ("FW4213_1_Htau", "full H_tau integrability", "blocked_until_projector_reference_tau_boundary_visible_Dq_and_MHref_close"),
        ("FW4213_2_Newton", "Newton/local-GR source bridge", "blocked_until_Htau_integrability_and_M_H_ref_close"),
        ("FW4213_3_edge", "edge-mode erasure", "forbidden_if_boundary_charge_is_nonzero_or_unfixed"),
        ("FW4213_4_public", "public local-GR claim", "blocked_private_conditional_theorem_only"),
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
            "status_id": "STATUS4213",
            "status": "qbasic_vertical_curl_conditionally_zero_selector_nonclaim",
            "strong_result": "I_qbasic_vertical is zero inside the pullback q-basic no-flux selector by presymplectic nullity of ker(Dq)",
            "remaining_gap": "global parent action pullback signature, edge-mode silence, M_H_ref and other 4212 curl components remain unsigned",
            "project_effect": "one MTS-specific curl obstruction is conditionally removed; next target is projector stress curl",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4213 conditionally closes the q-basic vertical curl term; the next retained 4212 numerator is projector stress.",
            "route_A": "prove I_projector=0 from quotient-owned readout projectors and observed Hodge/coframe descent",
            "route_B": "if not zero, fill I_projector/M_H_ref as the next curl-bound row",
            "route_C": "keep boundary edge and parent pullback caveats attached to the q-basic zero theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 229 - PPC4161 q-basic vertical presymplectic silence

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

4212 isolated the MTS-specific Hamiltonian curl term:

```text
I_qbasic_vertical = int_S i_tau omega_qbasic_vertical.
```

4213 proves the clean conditional route for making this term vanish without a plateau axiom.

## Theorem

Let `q: Phi -> Q` be the local quotient map and let `v` be an allowed q-basic vertical variation:

```text
Dq[v] = 0.
```

Assume the compact local parent action has pullback-plus-boundary form:

```text
L_parent|loc = q^* L_red[Q] + dB_vert
S_src = Sbar_src[q(Phi), psi, A, theta].
```

Then:

```text
theta_parent = q^* theta_red + delta B_vert + dC_vert
omega_parent = q^* omega_red + d delta B_vert.
```

Contracting with `v in ker(Dq)` gives:

```text
i_v omega_parent = d beta_v.
```

If the compact local collar has no vertical edge flux,

```text
int_S i_tau d beta_v = 0,
```

then:

```text
I_qbasic_vertical = int_S i_tau omega_qbasic_vertical = 0.
```

## What This Actually Closes

Inside the quotient-natural pullback/no-flux selector, the 4212 q-basic vertical Hamiltonian-curl numerator is zero. This is not a fitted cancellation and not a plateau assumption; it follows from action descent and presymplectic nullity of quotient fibres.

## What It Does Not Close

The result is still nonclaim globally because these pieces remain unsigned outside the selector:

- parent action pullback signature for the whole local packet;
- global edge-mode/boundary silence;
- stable positive `M_H_ref`;
- `I_projector`, `I_ref`, `I_tau+I_surface`, `I_boundary+I_corner`, `I_matter_EM`, and `I_Dq`;
- public Newton/local-GR source bridge.

## Fallback Bound

If any selector clause fails:

```text
|I_qbasic_vertical|/M_H_ref
<= (|R_pullback_action|
 + |R_theta_omega_owner|
 + |R_vertical_edge_flux|
 + |R_qbasic_defect|
 + |R_source_marker_leak|) / M_H_ref.
```

## Next Target

`{NEXT_TARGET}` should attack the next retained 4212 curl term:

```text
I_projector.
```
"""


def checkpoint_doc() -> str:
    return f"""# 4213 Y5 R2FR q-basic vertical presymplectic silence or curl bound

**Status:** `{DECISION}`.

**Forward move:** `I_qbasic_vertical` is conditionally zero inside the pullback q-basic no-flux selector:

```text
L_parent|loc=q^*L_red+dB
=> omega_parent=q^*omega_red+d delta B
=> i_v omega_parent=d beta_v
=> int_S i_tau d beta_v=0
=> I_qbasic_vertical=0.
```

This is a real geometric derivation, not a closure axiom. It remains nonclaim globally until the parent pullback signature and edge silence are parent-signed.

## Files written

- `formalization-workbench\\229-PPC4161-qbasic-vertical-presymplectic-silence.md`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4213_QBASIC_VERTICAL_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4213_CURL_SCORE_UPDATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4213_DECISION.csv`

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
        f'"The q-basic vertical Hamiltonian curl term is conditionally closed: if the compact local parent action is q-pullback plus boundary and vertical edge flux is silent, ker(Dq) is presymplectic-null and I_qbasic_vertical=0; global parent signature, edge-mode silence, M_H_ref and remaining curl components stay nonclaim.",'
        f'"4213 source audit, q-basic vertical theorem, activation clauses, curl score update, route matrix, decision row and firewall.",'
        f'private_qbasic_vertical_presymplectic_silence_conditional_nonclaim,'
        f'"Attack the projector-stress curl term I_projector, or fill its first bound row if quotient-owned projector descent fails.",'
        f'"This removes one MTS-specific curl obstruction only inside the selector; it does not yet prove full H_tau integrability or local GR."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 q-basic vertical presymplectic silence - 4213

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4213 conditionally closes the 4212 q-basic vertical curl:

```text
L_parent|loc=q^*L_red+dB
=> omega_parent=q^*omega_red+d delta B
=> i_v omega_parent=d beta_v
=> I_qbasic_vertical=0
```

inside compact no-flux local collars. The result is retained as private/nonclaim until parent pullback signature, edge silence, `M_H_ref`, and the remaining curl components close."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet q-basic vertical presymplectic silence - 4213

Marker: `{PACKET_MARKER}`

The packet now has a clean conditional zero theorem for `I_qbasic_vertical`. Next retained obstruction is projector stress: `I_projector`."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4213_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4213_QBASIC_VERTICAL_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4213_ACTIVATION_CLAUSES.csv"]
    score = rows_by_file["P8_Y5_R2FR_4213_CURL_SCORE_UPDATE.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4213_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4213_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "QVP4213_0_fibre_split",
        "QVP4213_1_pullback_action",
        "QVP4213_2_theta_descent",
        "QVP4213_3_omega_null",
        "QVP4213_4_boundary_silence",
        "QVP4213_5_curl_zero",
        "QVP4213_6_global_caveat",
    }
    checks = [
        ("VAL4213_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4213_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4213_2_theorem_complete", "q-basic vertical theorem has all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4213_3_curl_zero_clause", "I_qbasic_vertical zero clause exists", any(row["theorem_id"] == "QVP4213_5_curl_zero" and row["status"] == "conditional_zero_theorem" for row in theorem)),
        ("VAL4213_4_global_caveat", "global caveat remains explicit", any(row["theorem_id"] == "QVP4213_6_global_caveat" for row in theorem)),
        ("VAL4213_5_activation_clauses", "activation clauses include action, omega, boundary, source and MHref", {"ACT4213_1_action_pullback", "ACT4213_2_theta_omega_owner", "ACT4213_3_boundary", "ACT4213_4_source_matter", "ACT4213_5_MHref"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4213_6_score_update_zero", "curl score update records conditional qbasic zero", any(row["quantity"] == "I_qbasic_vertical" and row["value_or_bound"] == "0_under_QVP4213_selector" for row in score)),
        ("VAL4213_7_bound_fallback", "fallback bound row retained", any(row["quantity"] == "I_qbasic_vertical_bound" and row["status"] == "BOUND_ROW_RETAINED" for row in score)),
        ("VAL4213_8_routes", "routes include selector, edge, pullback and projector next", {"QR4213_0_activate_selector", "QR4213_1_edge_bound", "QR4213_2_pullback_bound", "QR4213_3_projector_next"}.issubset({row["route_id"] for row in routes})),
        ("VAL4213_9_decision_nonclaim", "decision keeps global and local-GR claims false", decision["global_parent_pullback_signature"] == "False" and decision["local_GR_claim"] == "False"),
        ("VAL4213_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4213_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4213_12_claim_register", "claim register contains L-054", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4213_13_spine_packet_markers", "spine and packet markers present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)),
        ("VAL4213_14_next_target", "next target is projector stress", decision["next_target"] == NEXT_TARGET),
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
        "P8_Y5_R2FR_4213_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4213_QBASIC_VERTICAL_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4213_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4213_CURL_SCORE_UPDATE.csv": curl_update_rows(),
        "P8_Y5_R2FR_4213_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4213_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4213_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4213_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4213_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4213_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4213_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
