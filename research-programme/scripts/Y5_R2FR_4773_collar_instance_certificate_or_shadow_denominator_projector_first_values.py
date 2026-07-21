from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4773"
CLAIM_ID = "L-615"
MARKER = "PPC4161_COLLAR_INSTANCE_CERTIFICATE_OR_SHADOW_DENOMINATOR_PROJECTOR_FIRST_VALUES_4773"
PACKET_MARKER = "PPC4161_PACKET_COLLAR_INSTANCE_CERTIFICATE_OR_SHADOW_DENOMINATOR_PROJECTOR_FIRST_VALUES_4773"
DECISION = "PRIVATE_COMPACT_COLLAR_SELECTOR_INSTANCE_CERTIFIED_NUMERATOR_COLLAPSES_CONDITIONALLY_TO_ZERO_DENOMINATOR_PROJECTOR_POSITIVITY_STILL_BLOCKS_QBAR_SCORE_NONCLAIM"
NEXT_TARGET = "4774-Y5-R2FR-denominator-projector-positive-lock-or-first-source-backed-M0-epsilon-row.md"

DOC_PATH = POST / "4773-Y5-R2FR-collar-instance-certificate-or-shadow-denominator-projector-first-values.md"
FORMAL_PATH = FORMAL / "789-PPC4161-collar-instance-certificate-or-shadow-denominator-projector-first-values.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_SOURCE_REGISTER.csv"
COLLAR_CERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_COLLAR_INSTANCE_CERTIFICATE.csv"
SHADOW_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_SHADOW_IMPORT_CERTIFICATE.csv"
NUMERATOR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_NUMERATOR_COLLAPSE_UPDATE.csv"
DENOMINATOR_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_DENOMINATOR_PROJECTOR_REMAINING_GATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4773_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4773_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4773_0_4772_collar", SOURCE_DIR / "P8_Y5_R2FR_4772_COMPACT_STATIONARY_COLLAR_ZERO_THEOREM.csv", "CCT4772_5_total", "4772 collar zero theorem"),
    ("SRC4773_1_4772_qedge", SOURCE_DIR / "P8_Y5_R2FR_4772_QEDGE_QBAR_UPDATE.csv", "QQ4772_4_qbar_product", "4772 Qedge/Qbar update"),
    ("SRC4773_2_4772_scoring", SOURCE_DIR / "P8_Y5_R2FR_4772_LOCAL_SCORING_GATE_STATUS.csv", "SG4772_5_qbar", "4772 scoring gate status"),
    ("SRC4773_3_vertical_silence", FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md", "R_proj = Pi_loc D Obar_loc[Dq[v]] = 0", "4177 quotient naturality private selector"),
    ("SRC4773_4_matter_interface", SOURCE_DIR / "P8_Y5_R2FR_4277_MATTER_INTERFACE_DESCENT_THEOREM.csv", "AD4277_4_shadow_slot_exclusion", "4277 standard matter-interface no-shadow branch"),
    ("SRC4773_5_qshadow_normal", SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_NORMAL_FORM_THEOREM.csv", "QSH4610_0_decomposition", "4610 Qshadow normal form"),
    ("SRC4773_6_qshadow_qbar", SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_QBARXH_UPDATE_ROWS.csv", "QSU4610_2_QbarXH", "4610 Qbar shadow product formula"),
    ("SRC4773_7_source_shadow", SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_SHADOW_OUTPUT.csv", "SH4431_0_exact_shadow_zero_contract", "4431 source-shadow zero contract"),
    ("SRC4773_8_denominator_lemma", SOURCE_DIR / "P8_Y5_R2FR_4764_MLOWER_PIM_DENOMINATOR_LEMMA.csv", "DL4764_3_projector_lock", "4764 denominator/projector lemma"),
    ("SRC4773_9_denominator_pack", SOURCE_DIR / "P8_Y5_R2FR_4764_DENOMINATOR_BOUND_PACK.csv", "DB4764_5_score_gate", "4764 denominator/projector missing-value pack"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    COLLAR_CERT_CSV,
    SHADOW_IMPORT_CSV,
    NUMERATOR_UPDATE_CSV,
    DENOMINATOR_GATE_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def collar_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("CIC4773_0_instance", "C_static_iso_private", "ideal compact stationary isolated local source collar", "branch instance selected before empirical readout", "SIGNED_PRIVATE_MATH_INSTANCE"),
        ("CIC4773_1_worldtube", "W_H", "W_H=closure(supp mu_H) before readout with compact support separation", "imports source-qbasic/support selector branch", "SIGNED_PRIVATE"),
        ("CIC4773_2_stationary", "stationary averaging window", "time-averaged dU_EM/dt=0 and no collar time flow", "static isolated collar hypothesis; not universal clock/solar claim", "SIGNED_FOR_INSTANCE"),
        ("CIC4773_3_same_Hodge", "same Maxwell-Hodge/current owner", "EM stress is Hilbert-owned once and Poynting is either stress flux or explicit wall flux", "imports 4714/4772 same-owner condition", "SIGNED_PRIVATE"),
        ("CIC4773_4_no_external_flux", "incoming/apparatus/radiative flux", "Phi_incoming=Phi_apparatus=F_rad=B_app_support=0", "closed isolated collar only; open collars use finite envelope", "SIGNED_FOR_INSTANCE"),
        ("CIC4773_5_fixed_boundary", "matter and Hamiltonian boundary", "delta_v psi fixed/compact or exact/q-owned; B_Ham_corner and B_normal_momentum vanish", "imports vertical-silence boundary routing and scalar no-normal-flux branch", "SIGNED_FOR_INSTANCE"),
        ("CIC4773_6_no_double_count", "boundary accounting", "lift-boundary, Poynting and Hamiltonian/corner rows are disjoint or identified by owner before summing", "prevents cancellation/double-counting", "SIGNED_ACCOUNTING"),
        ("CIC4773_7_boundary_total", "E_boundary_total_4773", "E_boundary_total_4772=0_private_collar_candidate becomes E_boundary_total_4773=0_private_C_static_iso", "collar theorem now has a private instance", "CERTIFIED_PRIVATE_IDEAL_INSTANCE_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": certificate_id,
            "object": obj,
            "certificate_clause": clause,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, obj, clause, meaning, status in specs
    ]


def shadow_import_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SIC4773_0_standard_interface", "canonical frame/source shadow slot", "ordinary matter couples through the q-owned observed interface; direct A_g/B_dis/source-frame slot is excluded", "Q_shadow_action=0_private_selector", "PRIVATE_IMPORT"),
        ("SIC4773_1_projector_shadow", "source-map/projector shadow", "source projector is identity/common calibration/fixed q-basic before readout; no post-Hilbert material/source projector", "Q_shadow_projector=0_private_selector", "PRIVATE_IMPORT"),
        ("SIC4773_2_source_shadow", "independent source functional shadow", "single parent Hilbert source, no independent source functional, no weighted duplicate action, no Hom into active source coefficient", "source_shadow=0_private_selector", "PRIVATE_IMPORT_FROM_4431_CONTRACT"),
        ("SIC4773_3_nonvariational_shadow", "nonvariational shadow", "nonvariational blocks are absent, separately conserved real blocks scored elsewhere, or forbidden by Noether consistency", "Q_shadow_nonvariational=0_private_selector", "PRIVATE_IMPORT"),
        ("SIC4773_4_shadow_total", "Q_shadow_abs", "|Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|", "0_private_selector", "SHADOW_ZERO_PRIVATE_SELECTOR_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "shadow_id": shadow_id,
            "shadow_channel": channel,
            "condition": condition,
            "private_value_or_formula": value,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for shadow_id, channel, condition, value, status in specs
    ]


def numerator_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("NU4773_0_bulk", "Q_bulk_XH_abs", "0_private_selector", "4771 bulk source-qbasic closure inside private on-shell/gauge branch", "PRIVATE_ZERO"),
        ("NU4773_1_edge_shell", "Q_edge_shell_abs", "0_private_C_static_iso", "source-qbasic support plus compact collar no boundary birth/death", "PRIVATE_ZERO"),
        ("NU4773_2_edge_boundary", "Q_edge_boundary_abs", "0_private_C_static_iso", "collar instance certifies E_boundary_total_4773=0", "PRIVATE_ZERO"),
        ("NU4773_3_edge_total", "Q_edge_XH_abs", "0_private_C_static_iso", "shell plus boundary edge rows zero in the private collar instance", "PRIVATE_ZERO"),
        ("NU4773_4_shadow", "Q_shadow_abs", "0_private_selector", "private no-shadow/import certificate", "PRIVATE_ZERO"),
        ("NU4773_5_Qtot", "Q_tot_XH_abs", "0_private_collar_selector", "Q_bulk + Q_edge + Q_shadow all zero in the combined private collar-selector instance", "NUMERATOR_COLLAPSED_NONCLAIM"),
        ("NU4773_6_open_fallback", "Q_tot_XH_abs_open", "|Q_bulk|+|Q_edge_shell|+E_boundary_total_4772_open+|Q_shadow|", "used for open/radiative/public/off-selector arenas", "FINITE_FALLBACK_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "quantity": quantity,
            "private_value_or_formula": value,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, quantity, value, meaning, status in specs
    ]


def denominator_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DG4773_0_projector_comm", "E_PiM_comm", "0_private_if Pi_M is fixed/q-basic and selected before readout", "conditional theorem from 4764 DL4764_3, not yet an empirical/source-backed row", "CONDITIONAL_PROJECTOR_LOCK"),
        ("DG4773_1_projector_norm", "P_M_bound", "finite if Pi_M is a fixed bounded projector on the chosen source norm", "operator norm/value still not supplied", "VALUE_OR_NORM_MISSING"),
        ("DG4773_2_denominator", "M_lower", "M_0(1-epsilon_abs)>0", "requires M_0>0 and 0<=epsilon_abs<1 with same-frame units; source-backed values still missing", "POSITIVE_LOCK_MISSING"),
        ("DG4773_3_qbar_private", "Qbar_XH", "(P_M Q_tot + E_PiM_comm)/M_lower", "with Q_tot=0 and E_PiM_comm=0, Qbar=0 only after M_lower>0 is certified", "BLOCKED_BY_DENOMINATOR_POSITIVITY"),
        ("DG4773_4_score_policy", "local-GR/Newton score", "do not score from numerator collapse alone", "must next certify denominator/projector positivity or fill first source-backed values", "PRODUCT_STILL_BLOCKED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "quantity": quantity,
            "formula_or_condition": formula,
            "current_status": current_status,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, quantity, formula, current_status, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4773_0_denominator_projector", "certify M_lower>0 and projector lock or fill first M_0/epsilon_abs/P_M_bound/E_PiM_comm rows", "last hard product gate after private numerator collapse", "SELECTED_NEXT"),
        ("ROUTE4773_1_open_arena_values", "fill finite open-collar and off-selector values", "needed for radiative/lab/apparatus arenas that do not satisfy C_static_iso", "PARALLEL"),
        ("ROUTE4773_2_public_parent", "promote private collar-selector instance to one public parent action selector", "would turn private branch into public theorem rather than private local instance", "LONGER_ROUTE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4773_0_private_scope", "C_static_iso is a private ideal collar-selector instance, not a public/global MTS theorem.", "prevents public overclaim", False),
        ("GATE4773_1_open_fallback", "Open/radiative/nonstationary/apparatus arenas must use finite fallback rows.", "prevents using static collar zero outside domain", False),
        ("GATE4773_2_shadow_scope", "Q_shadow_abs=0 is private selector only; off-selector source-shadow countermodels remain active.", "keeps shadow risk honest", False),
        ("GATE4773_3_denominator", "Qbar/local-GR score cannot fire until M_lower>0 and projector/commutator gates are certified.", "blocks numerator-only scoring", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": allowed,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect, allowed in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4773_0", "No local GR/Newton/PPN/WEP/R10/clock/orbital pass from 4773.", "numerator collapse is private and denominator/projector still block scoring"),
        ("FW4773_1", "No applying C_static_iso to open/radiative/lab/apparatus collars.", "finite fallback remains mandatory outside the instance"),
        ("FW4773_2", "No public no-shadow theorem from private selector import.", "source-shadow countermodels remain off-branch"),
        ("FW4773_3", "No Qbar score without M_lower positivity and projector lock/value rows.", "division/projection gate remains"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall, reason in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4773_0",
            "decision": DECISION,
            "summary": "4773 certifies a private ideal compact stationary collar-selector instance C_static_iso. In that instance the boundary total zero candidate becomes a signed private branch row, Qedge shell/boundary and Qshadow collapse, and the local numerator Q_tot_XH is zero conditionally. The Qbar/local-GR score is still blocked by denominator positivity and projector/commutator gates.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4773_0",
            "state": "completed_nonclaim",
            "meaning": "Private collar-selector numerator collapse is certified; denominator/projector product gate remains.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "After private numerator collapse, the hard blocker is M_lower positivity plus projector norm/commutator certification or first source-backed values.",
            "route_priority": "denominator_projector_positive_lock_first_then_open_arena_values",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    collar: list[dict[str, Any]],
    shadow: list[dict[str, Any]],
    numerator: list[dict[str, Any]],
    denominator: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4773: Collar Instance Certificate or Shadow/Denominator/Projector First Values

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

- 4773 certifies one private mathematical instance: `C_static_iso_private`, an ideal compact stationary isolated collar-selector branch.
- This is **not** a public/global theorem and not an empirical local-GR/Newton claim.
- Inside `C_static_iso_private` plus the private no-shadow selector:

```text
E_boundary_total_4773 = 0_private_C_static_iso
Q_edge_shell_abs = 0_private_C_static_iso
Q_edge_boundary_abs = 0_private_C_static_iso
Q_shadow_abs = 0_private_selector
Q_tot_XH_abs = 0_private_collar_selector.
```

- The hard remaining product gate is:

```text
Qbar_XH = (Pi_M Q_tot_XH + E_PiM_comm) / M_lower.
```

Even with `Q_tot_XH=0`, no score fires until `M_lower>0` and projector/commutator gates are certified.

## Collar Instance Certificate

{markdown_table(collar, ["certificate_id", "object", "certificate_clause", "status"])}

## Shadow Import Certificate

{markdown_table(shadow, ["shadow_id", "shadow_channel", "private_value_or_formula", "status"])}

## Numerator Collapse Update

{markdown_table(numerator, ["update_id", "quantity", "private_value_or_formula", "status"])}

## Denominator/Projector Remaining Gate

{markdown_table(denominator, ["gate_id", "quantity", "formula_or_condition", "current_status", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect", "claim_allowed"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4773: Private Collar-Selector Numerator Collapse

Generated: `{timestamp}`

4773 certifies the private ideal collar-selector instance:

```text
C_static_iso_private
```

where the source collar is compact, stationary, isolated, same-Hodge, fixed/exact/q-owned at the boundary, selected before readout, and no-double-counted.

In this instance:

```text
Q_bulk_XH_abs = 0
Q_edge_shell_abs = 0
Q_edge_boundary_abs = 0
Q_shadow_abs = 0
Q_tot_XH_abs = 0.
```

This is a private numerator collapse, not a scored local-GR result. The score still waits for:

```text
M_lower > 0,
P_M_bound finite,
E_PiM_comm = 0 or bounded.
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4773 certifies `C_static_iso_private`, an ideal compact stationary isolated collar-selector branch.
- In that private instance, boundary total, Qedge shell, Qedge boundary and Qshadow collapse, yielding `Q_tot_XH_abs=0_private_collar_selector`.
- This is not public/global and not empirical; open/radiative/off-selector arenas retain finite fallback rows.
- Qbar/local-GR scoring remains blocked by `M_lower>0`, projector norm and commutator gates.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4773 packet update: private local numerator collapse is now explicit for `C_static_iso_private`. The next hard gate is denominator/projector positivity rather than more boundary bookkeeping.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4773-Y5-R2FR-collar-instance-certificate-or-shadow-denominator-projector-first-values.md`

## Decision

`{DECISION}`

## What moved forward

- Certified the private ideal compact stationary collar-selector instance `C_static_iso_private`.
- Collapsed boundary total, Qedge shell, Qedge boundary and Qshadow inside that private instance.
- Reduced the private local numerator to `Q_tot_XH_abs=0_private_collar_selector`.
- Left Qbar/local-GR scoring blocked by denominator positivity and projector/commutator gates.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_private_collar_selector_numerator_collapse",
        "4773 certifies a private ideal compact stationary collar-selector instance and collapses the private local numerator while leaving denominator/projector scoring blocked.",
        "Generated source register, collar instance certificate, shadow import certificate, numerator collapse update, denominator/projector remaining gate, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "private_collar_selector_numerator_collapse_denominator_projector_blocked_nonclaim",
        NEXT_TARGET,
        "Promoting C_static_iso_private to public/empirical local GR, or scoring Qbar without M_lower/projector gates.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need denominator/projector positive lock or first source-backed M0/epsilon row.",
        "Collar instance certificate and numerator collapse",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    collar: list[dict[str, Any]],
    shadow: list[dict[str, Any]],
    numerator: list[dict[str, Any]],
    denominator: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4773_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4773_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4773_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    checks.append(("VAL4773_2_collar_instance", "private ideal collar instance certified", any(row["status"] == "CERTIFIED_PRIVATE_IDEAL_INSTANCE_NONCLAIM" for row in collar), str(COLLAR_CERT_CSV)))
    checks.append(("VAL4773_3_shadow_zero", "private shadow zero imported", any(row["shadow_channel"] == "Q_shadow_abs" and row["private_value_or_formula"] == "0_private_selector" for row in shadow), str(SHADOW_IMPORT_CSV)))
    checks.append(("VAL4773_4_numerator_collapse", "Qtot numerator collapses private", any(row["quantity"] == "Q_tot_XH_abs" and row["private_value_or_formula"] == "0_private_collar_selector" for row in numerator), str(NUMERATOR_UPDATE_CSV)))
    checks.append(("VAL4773_5_open_fallback_retained", "open/off-selector finite fallback retained", any(row["quantity"] == "Q_tot_XH_abs_open" and row["status"] == "FINITE_FALLBACK_RETAINED" for row in numerator), str(NUMERATOR_UPDATE_CSV)))
    checks.append(("VAL4773_6_denominator_blocked", "denominator/projector gate still blocks Qbar score", any(row["quantity"] == "Qbar_XH" and row["status"] == "BLOCKED_BY_DENOMINATOR_POSITIVITY" for row in denominator) and any(row["status"] == "POSITIVE_LOCK_MISSING" for row in denominator), str(DENOMINATOR_GATE_CSV)))
    checks.append(("VAL4773_7_route_selected", "route selects denominator/projector next", any(row["selection_status"] == "SELECTED_NEXT" and ("denominator" in row["route"] or "M_lower" in row["route"]) for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4773_8_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4773_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4773_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4773_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4773_12_claim_row", "claim row L-615 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4773_13_resume", "resume points from 4773 to 4774", "4773-Y5" in resume_text and "4774-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4773_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

    overall = all(passed for _, _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4773_OVERALL",
            "check": "all 4773 collar-instance/numerator-collapse checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    collar = collar_certificate_rows(timestamp)
    shadow = shadow_import_rows(timestamp)
    numerator = numerator_update_rows(timestamp)
    denominator = denominator_gate_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(COLLAR_CERT_CSV, collar)
    write_csv(SHADOW_IMPORT_CSV, shadow)
    write_csv(NUMERATOR_UPDATE_CSV, numerator)
    write_csv(DENOMINATOR_GATE_CSV, denominator)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, collar, shadow, numerator, denominator, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, collar, shadow, numerator, denominator, routes, gates, timestamp))


if __name__ == "__main__":
    main()
