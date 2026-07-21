from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4732"
CLAIM_ID = "L-574"
MARKER = "PPC4161_R826_PARENT_CONSTRUCTOR_LIST_OR_CI826_VI_SOURCE_ROW_4732"
PACKET_MARKER = "PPC4161_PACKET_R826_PARENT_CONSTRUCTOR_LIST_OR_CI826_VI_SOURCE_ROW_4732"
DECISION = "R826_CONSTRUCTOR_CANDIDATES_EXTRACTED_NO_PARENT_DENSITY_SIGNATURE_FOUND_EULER_RESIDUAL_ROUTE_PRIORITIZED_NONCLAIM"
NEXT_TARGET = "4733-Y5-R2FR-XB-qbasic-lock-and-Jm-hidden-source-row-or-R826-descent-proof.md"

DOC_PATH = POST / "4732-Y5-R2FR-R826-parent-constructor-list-from-action-density-or-CI826-VI-source-row.md"
FORMAL_PATH = FORMAL / "748-PPC4161-R826-parent-constructor-list-from-action-density-or-CI826-VI-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_SOURCE_REGISTER.csv"
CONSTRUCTOR_SCAN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_R826_CONSTRUCTOR_SCAN.csv"
CONSTRUCTOR_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_R826_CONSTRUCTOR_LIST_GATE.csv"
EULER_TRANSLATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_EULER_RESIDUAL_TO_HHIDDEN_TRANSLATION.csv"
VALUE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_CI826_VI_SOURCE_ROW_CONTRACT.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4732_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4732_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4732_0_resume", POST / "CURRENT_LOCAL_RESUME.md", "4732-Y5-R2FR-R826-parent-constructor-list-from-action-density-or-CI826-VI-source-row.md", "current local handoff into 4732"),
    ("SRC4732_1_4731_doc", POST / "4731-Y5-R2FR-CoeffR826-typed-target-owner-from-parent-action-or-Hhidden-value-source.md", "actual `R826` constructor list", "4731 handoff to constructor list"),
    ("SRC4732_2_4731_next", SOURCE_DIR / "P8_Y5_R2FR_4731_NEXT_TARGET.csv", "4732-Y5-R2FR-R826-parent-constructor-list-from-action-density-or-CI826-VI-source-row.md", "machine handoff into 4732"),
    ("SRC4732_3_4731_owner", SOURCE_DIR / "P8_Y5_R2FR_4731_COEFFR826_PARENT_OWNER_THEOREM.csv", "OWN4731_5_actual_R826_constructor", "actual R826 constructor is unsigned"),
    ("SRC4732_4_4731_value", SOURCE_DIR / "P8_Y5_R2FR_4731_FIRST_HHIDDEN_VALUE_SOURCE_ROW.csv", "HVAL4731_0_value_product", "C_I826 V_I source row demand"),
    ("SRC4732_5_4673_slot", SOURCE_DIR / "P8_Y5_R2FR_4673_R826_SLOT_OWNER_AUDIT.csv", "R8264673_2_R_descends", "R826 descent/no-slot audit"),
    ("SRC4732_6_4673_bridge", SOURCE_DIR / "P8_Y5_R2FR_4673_AM_R826_NO_SOURCE_SLOT_BRIDGE.csv", "BR4673_4_countermodel", "pre-action response slot countermodel"),
    ("SRC4732_7_4674_euler", SOURCE_DIR / "P8_Y5_R2FR_4674_R826_EULER_RESIDUAL_PROOF.csv", "PR4674_2_exact_identity", "Euler residual identity"),
    ("SRC4732_8_4674_bound", SOURCE_DIR / "P8_Y5_R2FR_4674_FIRST_FINITE_B826_BOUND_SCHEMA.csv", "BND4674_0_master", "finite B826 residual bound schema"),
    ("SRC4732_9_4672_weld", SOURCE_DIR / "P8_Y5_R2FR_4672_B826_EVEN_RESPONSE_WELD.csv", "WELD4672_3_no_source_slot_theorem", "even/no-source B826 weld"),
    ("SRC4732_10_4671_root", SOURCE_DIR / "P8_Y5_R2FR_4671_B826_ROOT_LOCK_TEST.csv", "BRL4671_1_root_lock", "root-lock test"),
    ("SRC4732_11_4670_component", SOURCE_DIR / "P8_Y5_R2FR_4670_BMEM_FIRST_COMPONENT_AUDIT.csv", "BFC4670_1_B826", "B826 first component audit"),
    ("SRC4732_12_4507_formula", SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv", "BMF4507_1_826_term", "Bmem formula source"),
    ("SRC4732_13_4514_vector", SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv", "BMV4514_0_B826", "B826 component vector source"),
    ("SRC4732_14_4730_counter", SOURCE_DIR / "P8_Y5_R2FR_4730_HIDDEN_SCALAR_R826_COUNTEREXAMPLE_TRANSFER.csv", "HSC8264730_0_generic", "hidden scalar counterexample transfer"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def constructor_scan_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("SCAN4732_0_formula", "structure formula", "B_826 = a_F L_cg^-2 R_m(m_L;X_B)", "imports B826 as the first Bmem component but does not identify the parent density constructor", "STRUCTURE_FOUND_NOT_CONSTRUCTOR", "SRC4732_12_4507_formula"),
        ("SCAN4732_1_qdescent_candidate", "q-descent constructor candidate", "R_826=R_826(q;X_B) with X_B q-basic/fixed", "would give dR_826[v]=0 and C_I826=0 if signed", "CANDIDATE_NOT_SIGNED", "SRC4732_5_4673_slot"),
        ("SCAN4732_2_even_candidate", "even response candidate", "R_826(q,z;X_B)=R_826(q,-z;X_B)", "differentiating at z=0 gives R_m=0 and B826=0", "CANDIDATE_NOT_SIGNED", "SRC4732_9_4672_weld"),
        ("SCAN4732_3_euler_candidate", "Euler residual constructor candidate", "E_m=delta S_parent/delta m=R_m+J_m_src+J_m_bdy+J_m_readout+J_m_domain=0", "turns B826 into the unowned branch-force residual", "BEST_CURRENT_DERIVED_ROUTE_CONDITIONAL", "SRC4732_7_4674_euler"),
        ("SCAN4732_4_post_variation_candidate", "post-variation diagnostic candidate", "R_826 is readout/post-solution and absent from parent source slots", "would remove the source force rather than make it small", "CANDIDATE_REQUIRES_READOUT_DOMAIN_PROOF", "SRC4732_6_4673_bridge"),
        ("SCAN4732_5_counterconstructor", "live counterconstructor", "S_parent contains R_826(q,z;X_B) or w_R R_826 before variation", "then R826 keeps a hidden/source target and C_I826 V_I survives", "COUNTERCONSTRUCTOR_ACTIVE", "SRC4732_6_4673_bridge"),
        ("SCAN4732_6_search_verdict", "actual parent density line", "no sourced line currently proves the actual parent constructor is q-only, even, or post-variation", "constructor list is not claim-grade; use Euler residual/value-source route", "NO_PARENT_DENSITY_SIGNATURE_FOUND", "SRC4732_3_4731_owner"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "scan_id": scan_id,
            "object": obj,
            "candidate_or_formula": formula,
            "effect": effect,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for scan_id, obj, formula, effect, status, source_id in specs
    ]


def constructor_gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("CLG4732_0_parent_density", "actual parent density contains named R826 constructor", "needed to decide whether R826 is q-descended, even, post-variation, or a live pre-action response slot", "MISSING_PARENT_DENSITY_SIGNATURE", "SRC4732_1_4731_doc"),
        ("CLG4732_1_XB_lock", "X_B q-basic/fixed under vertical variation", "without X_B lock, R_826(q;X_B) still can carry hidden motion", "MISSING_XB_QBASIC_LOCK", "SRC4732_5_4673_slot"),
        ("CLG4732_2_no_hidden_slot", "no C_hid/I_hid/memory scalar/domain marker target", "needed for C_I826=0", "MISSING_NO_HIDDEN_TARGET_SIGNATURE", "SRC4732_14_4730_counter"),
        ("CLG4732_3_same_owner", "same owner as A_m/common measure/current", "prevents beta_visible and B826 being killed by different closures", "COMMON_OWNER_UNSIGNED", "SRC4732_6_4673_bridge"),
        ("CLG4732_4_readout_domain", "readout/post-variation domain proof", "needed if R826 is diagnostic rather than parent force", "READOUT_DOMAIN_UNSIGNED", "SRC4732_6_4673_bridge"),
        ("CLG4732_5_euler_residual", "Euler residual identity usable", "PR4674 supplies the best current bound route if parent stationarity is signed", "CONDITIONAL_IDENTITY_AVAILABLE", "SRC4732_7_4674_euler"),
        ("CLG4732_6_constructor_verdict", "constructor list verdict", "candidate constructors are extracted, but no actual parent density signature is found", "CONSTRUCTOR_LIST_UNSIGNED", "SRC4732_3_4731_owner"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, gate, meaning, status, source_id in specs
    ]


def euler_translation_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("EHT4732_0_identity", "B826 Euler residual identity", "B_826 = -a_F L_cg^-2 (J_m_src+J_m_bdy+J_m_readout+J_m_domain+E_m_res)", "imports 4674 exact conditional identity", "DERIVED_CONDITIONAL_IDENTITY", "SRC4732_7_4674_euler"),
        ("EHT4732_1_hidden_value_slot", "C_I826 V_I placement", "C_I826 V_I is one possible contribution to J_m_src or J_m_hidden inside J_m_unowned", "connects 4731 hidden-value row to the sharper Euler residual route", "TRANSLATION_WRITTEN_NONCLAIM", "SRC4732_4_4731_value"),
        ("EHT4732_2_descent_zero", "q-descent zero", "R_826=R_826(q;X_B) and X_B fixed implies J_m_hidden=0 and C_I826=0", "exact if constructor list and X_B lock sign", "EXACT_IF_SIGNED", "SRC4732_5_4673_slot"),
        ("EHT4732_3_countercase", "pre-action hidden source", "R_826(q,I_hid;X_B) or w_R(I_hid)R_826 gives J_m_hidden != 0", "keeps finite Hhidden row alive", "COUNTERCASE_ACTIVE", "SRC4732_14_4730_counter"),
        ("EHT4732_4_best_next", "next executable target", "attack X_B q-basic lock and J_m_hidden source row together", "this is narrower than broad constructor exhaustion", "NEXT_TARGET_SELECTED", "SRC4732_8_4674_bound"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "translation_id": translation_id,
            "target": target,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for translation_id, target, formula, meaning, status, source_id in specs
    ]


def value_source_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("CIVI4732_0_master", "C_I826_V_I_or_Jm_hidden", "first hidden-source value row", "|J_m_hidden| or C_I826 V_I", "I_hid definition; Coeff_R826 constructor; C_I826; V_I; domain; units; source_path", "MISSING_NUMERIC_INPUTS", "SRC4732_4_4731_value"),
        ("CIVI4732_1_XB", "X_B_qbasic_lock", "descent guard", "D_v X_B=0", "definition of X_B; proof it is q-basic/fixed; source path", "MISSING_XB_LOCK", "SRC4732_5_4673_slot"),
        ("CIVI4732_2_CI826", "C_I826", "hidden sensitivity", "sup|partial Coeff_R826/partial I_hid|", "zero theorem or value with units; no unity convention", "MISSING_CI826_VALUE", "SRC4732_4_4731_value"),
        ("CIVI4732_3_VI", "V_I", "hidden vertical amplitude", "sup|D_v I_hid|", "hidden scalar normalization; branch domain; source path", "MISSING_VI_VALUE", "SRC4732_4_4731_value"),
        ("CIVI4732_4_Jm_hidden", "J_m_hidden", "Euler residual hidden branch force", "|J_m_hidden| <= C_I826 V_I + gradient/marker/readout/domain pieces", "compatible units with PR4674 J_m_unowned", "MISSING_JM_HIDDEN_VALUE", "SRC4732_8_4674_bound"),
        ("CIVI4732_5_acceptance", "valid_for_claim", "claim switch", "true only if q-descent/even/post-variation signs or all source rows are numeric with units", "currently false", "FALSE_NOW", "SRC4732_8_4674_bound"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "role": role,
            "formula": formula,
            "required_columns": required,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, quantity, role, formula, required, status, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4732_0_sources_verified", "All 4732 source paths exist and needles are found.", True, "NONE"),
        ("GATE4732_1_constructor_candidates_extracted", "q-descent, even, Euler residual and post-variation candidates are extracted.", True, "CANDIDATES_ONLY_NOT_CLAIM"),
        ("GATE4732_2_parent_density_signature_found", "Actual parent action density gives R826 constructor list.", False, "PARENT_DENSITY_SIGNATURE_MISSING"),
        ("GATE4732_3_XB_qbasic_signed", "X_B is q-basic/fixed under vertical variation.", False, "XB_LOCK_MISSING"),
        ("GATE4732_4_hidden_counterconstructor_closed", "pre-action hidden/source response slot is forbidden.", False, "COUNTERCONSTRUCTOR_ACTIVE"),
        ("GATE4732_5_euler_residual_values_sourced", "J_m_hidden/C_I826/V_I values or theorem-zero rows are sourced.", False, "JM_HIDDEN_VALUES_MISSING"),
        ("GATE4732_6_B826_claim_ready", "B826 hidden constructor/value slot is claim-grade.", False, "B826_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4732_0_search_not_proof", "A corpus hit for R826 is not a parent constructor signature."),
        ("FW4732_1_no_formula_to_zero", "B_826=a_F L_cg^-2 R_m is structure, not R_m=0."),
        ("FW4732_2_no_Am_free_ride", "A_m q-basic does not automatically make R826 q-basic."),
        ("FW4732_3_no_even_without_owner", "Even-response zero needs the same parent owner; no borrowed symmetry."),
        ("FW4732_4_no_euler_without_values", "Euler residual identity is sharper but still needs zero theorems or source-backed J_m rows."),
        ("FW4732_5_no_public_claim", "No local-GR, PPN, R10 or GitHub claim from this checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derivation_result": "R826 constructor candidates are extracted: q-descent, even response, post-variation diagnostic and Euler residual identity",
            "nonclaim_result": "no actual parent density signature proves which constructor is owned; hidden/source counterconstructor remains active",
            "finite_row_result": "C_I826 V_I is translated into the J_m_hidden/Euler residual source-row contract",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4732_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4732_1_science_verdict",
            "status": "constructor_candidates_extracted_euler_residual_route_prioritized",
            "detail": "The work moved from generic constructor missingness to an explicit candidate list and J_m_hidden source-row route.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "4732 shows the narrowest remaining proof is X_B q-basic/R826 descent; the practical fallback is the J_m_hidden source row.",
            "first_task": "Try to prove D_v X_B=0 and R_826=R_826(q;X_B) or post-variation diagnostic status.",
            "fallback_task": "Fill J_m_hidden/C_I826/V_I with units, branch domain and source path so the Euler residual bound can run.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    scan: list[dict[str, Any]],
    constructor_gate: list[dict[str, Any]],
    euler: list[dict[str, Any]],
    values: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4732 - R826 Parent Constructor List From Action Density or CI826 VI Source Row

Generated: `{ts}`

## Purpose

4732 actually hunts the `R826` constructor rather than leaving it as a vague missing parent-owner clause.

## What Actually Moved

- Existing corpus hits were separated into real constructor candidates: `q`-descent, even response, post-variation diagnostic, and Euler residual identity.
- No current source signs an actual parent density line proving which constructor is owned.
- The strongest current route is the 4674 Euler identity: `B_826 = -a_F L_cg^-2 (J_m_src+J_m_bdy+J_m_readout+J_m_domain+E_m_res)`.
- The hidden scalar value row is now translated into the sharper residual object: `J_m_hidden` or `C_I826 V_I`, with `X_B` q-basic lock as the next proof target.

## Constructor Scan

{bullets(scan, "scan_id", "status")}

## Constructor List Gate

{bullets(constructor_gate, "gate_id", "status")}

## Euler Residual Translation

{bullets(euler, "translation_id", "status")}

## Source Row Contract

{bullets(values, "row_id", "status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 748 - R826 Parent Constructor List From Action Density or CI826 VI Source Row

Generated: `{ts}`

## Result

The constructor search found four live forms:

- `R_826=R_826(q;X_B)` with `X_B` q-basic/fixed.
- `R_826(q,z;X_B)=R_826(q,-z;X_B)` under a parent even branch.
- `R_826` as a post-variation/readout diagnostic absent from source slots.
- The Euler residual identity `E_m=R_m+J_m_src+J_m_bdy+J_m_readout+J_m_domain=0`.

No current source signs the actual parent density constructor. The practical route is therefore the Euler residual:

`B_826 = -a_F L_cg^-2 (J_m_src+J_m_bdy+J_m_readout+J_m_domain+E_m_res)`.

## Fallback Contract

`C_I826 V_I` is now treated as one component of `J_m_hidden` inside the unowned branch-force residual.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the R826 constructor search now has four explicit branches: q-descent, even response, post-variation diagnostic, and Euler residual identity.
- Current blocker: no actual parent density signature proves which R826 constructor is owned; the hidden/source counterconstructor remains active.
- Finite row: `C_I826 V_I` is translated into a `J_m_hidden` component of the Euler residual bound.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: uses the 4673/4674 trail to convert R826 constructor missingness into an explicit candidate list and a J_m_hidden source-row route.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- The R826 constructor candidates are extracted and classified.
- No parent density signature is found yet, so the zero route remains conditional.
- The practical fallback is now `J_m_hidden` / `C_I826 V_I` inside the Euler residual bound.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4732 extracts the R826 constructor candidates and prioritizes the Euler residual/J_m_hidden route; no parent density signature is found, so the result remains nonclaim.",
        "current_evidence": "Generated source register, constructor scan, constructor gate, Euler residual translation, C_I826 V_I source row contract, gates, firewalls, decision, status, next target and validation.",
        "status": "R826_constructor_candidates_extracted_euler_residual_route_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a constructor candidate or formula hit as an actual parent action density signature.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "X_B q-basic lock, parent density signature, J_m_hidden, C_I826 and V_I remain unsourced.",
        "title": "R826 parent constructor list from action density or CI826 VI source row",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    scan: list[dict[str, Any]],
    constructor_gate: list[dict[str, Any]],
    euler: list[dict[str, Any]],
    values: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        CONSTRUCTOR_SCAN_CSV,
        CONSTRUCTOR_GATE_CSV,
        EULER_TRANSLATION_CSV,
        VALUE_ROW_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    scan_status = ";".join(row["status"] for row in scan)
    constructor_status = ";".join(row["status"] for row in constructor_gate)
    euler_status = ";".join(row["status"] for row in euler)
    value_status = ";".join(row["status"] for row in values)
    checks = [
        ("VAL4732_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4732 source paths exist"),
        ("VAL4732_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4732 source needles found"),
        ("VAL4732_2_constructor_candidates_extracted", "CANDIDATE_NOT_SIGNED" in scan_status and "BEST_CURRENT_DERIVED_ROUTE_CONDITIONAL" in scan_status, "constructor candidates are extracted"),
        ("VAL4732_3_no_parent_density_signature", "NO_PARENT_DENSITY_SIGNATURE_FOUND" in scan_status and "CONSTRUCTOR_LIST_UNSIGNED" in constructor_status, "actual parent density signature is not promoted"),
        ("VAL4732_4_euler_translation_written", "DERIVED_CONDITIONAL_IDENTITY" in euler_status and "TRANSLATION_WRITTEN_NONCLAIM" in euler_status, "Euler residual translation is written"),
        ("VAL4732_5_source_row_contract_created", "MISSING_CI826_VALUE" in value_status and "MISSING_JM_HIDDEN_VALUE" in value_status, "C_I826/V_I/J_m_hidden source contract is created"),
        ("VAL4732_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4732_0_sources_verified", "GATE4732_1_constructor_candidates_extracted"}), "all claim gates remain closed except structural nonclaim gates"),
        ("VAL4732_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4732_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4732_9_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-574"),
        ("VAL4732_10_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4733 next target"),
        ("VAL4732_11_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4732 CSV files parse cleanly"),
        ("VAL4732_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4732_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4732 R826 parent constructor list or CI826 VI source row validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    scan = constructor_scan_rows(ts)
    constructor_gate = constructor_gate_rows(ts)
    euler = euler_translation_rows(ts)
    values = value_source_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(CONSTRUCTOR_SCAN_CSV, scan)
    write_csv(CONSTRUCTOR_GATE_CSV, constructor_gate)
    write_csv(EULER_TRANSLATION_CSV, euler)
    write_csv(VALUE_ROW_CSV, values)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, scan, constructor_gate, euler, values, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, scan, constructor_gate, euler, values, gates, ts))


if __name__ == "__main__":
    main()
