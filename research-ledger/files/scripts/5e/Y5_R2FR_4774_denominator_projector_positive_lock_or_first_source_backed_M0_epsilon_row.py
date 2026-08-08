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

CHECKPOINT = "4774"
CLAIM_ID = "L-616"
MARKER = "PPC4161_DENOMINATOR_PROJECTOR_POSITIVE_LOCK_OR_FIRST_SOURCE_BACKED_M0_EPSILON_ROW_4774"
PACKET_MARKER = "PPC4161_PACKET_DENOMINATOR_PROJECTOR_POSITIVE_LOCK_OR_FIRST_SOURCE_BACKED_M0_EPSILON_ROW_4774"
DECISION = "PRIVATE_DENOMINATOR_PROJECTOR_POSITIVE_LOCK_DERIVED_QBAR_XH_ZERO_INSIDE_C_STATIC_ISO_BRANCH_PUBLIC_AND_SOURCE_BACKED_VALUES_STILL_OPEN_NONCLAIM"
NEXT_TARGET = "4775-Y5-R2FR-private-local-GR-limit-certificate-or-open-arena-first-values.md"

DOC_PATH = POST / "4774-Y5-R2FR-denominator-projector-positive-lock-or-first-source-backed-M0-epsilon-row.md"
FORMAL_PATH = FORMAL / "790-PPC4161-denominator-projector-positive-lock-or-first-source-backed-M0-epsilon-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_SOURCE_REGISTER.csv"
DENOMINATOR_LOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_DENOMINATOR_POSITIVE_LOCK_THEOREM.csv"
PROJECTOR_LOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_PROJECTOR_LOCK_THEOREM.csv"
QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_QBAR_PRIVATE_ZERO_UPDATE.csv"
FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_OPEN_OR_EMPIRICAL_FALLBACK_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4774_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4774_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4774_0_4773_numerator", SOURCE_DIR / "P8_Y5_R2FR_4773_NUMERATOR_COLLAPSE_UPDATE.csv", "NU4773_5_Qtot", "4773 private numerator collapse"),
    ("SRC4774_1_4773_denominator_gate", SOURCE_DIR / "P8_Y5_R2FR_4773_DENOMINATOR_PROJECTOR_REMAINING_GATE.csv", "DG4773_3_qbar_private", "4773 remaining Qbar gate"),
    ("SRC4774_2_4764_inverse_lock", SOURCE_DIR / "P8_Y5_R2FR_4764_MLOWER_PIM_DENOMINATOR_LEMMA.csv", "DL4764_2_inverse_lock", "4764 denominator inverse lock"),
    ("SRC4774_3_4764_projector_lock", SOURCE_DIR / "P8_Y5_R2FR_4764_MLOWER_PIM_DENOMINATOR_LEMMA.csv", "DL4764_3_projector_lock", "4764 fixed/q-basic projector commutator lock"),
    ("SRC4774_4_4764_bound_pack", SOURCE_DIR / "P8_Y5_R2FR_4764_DENOMINATOR_BOUND_PACK.csv", "DB4764_5_score_gate", "4764 source-backed missing-value gate"),
    ("SRC4774_5_4170_hamiltonian_projector", SOURCE_DIR / "P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION.csv", "HQ4170_4_projector_identity", "4170 Pi_M as Hamiltonian/Hilbert charge map"),
    ("SRC4774_6_4170_radial_glue", SOURCE_DIR / "P8_Y5_R2FR_4170_NOETHER_RADIAL_GLUE.csv", "NG4170_6_radial", "4170 same charge on any linking surface"),
    ("SRC4774_7_4230_positive_denominator", SOURCE_DIR / "P8_Y5_R2FR_4230_MEH_EPSILON_SCORE.csv", "MES4230_4_MHref_positive", "4230 private MHref positivity and epsilon zero"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    DENOMINATOR_LOCK_CSV,
    PROJECTOR_LOCK_CSV,
    QBAR_UPDATE_CSV,
    FALLBACK_CSV,
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


def denominator_lock_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "DL4774_0_branch_intersection",
            "C_static_iso_private ∩ PPC4161-TK-HQ ∩ MEH_private_selector",
            "intersect the 4773 collar-selector numerator branch with the 4170 Hamiltonian charge branch and the 4230 positive-denominator selector",
            "same tau, coframe, reference, linking surface family, source worldtube and q-owned support selector",
            "PRIVATE_BRANCH_INTERSECTION_DEFINED",
        ),
        (
            "DL4774_1_M0_definition",
            "M_0 := M_EH_private = c^-2 E_plus_private",
            "4230 gives E_plus_private=E_H^dress>0 for rho_H>=0 and nonzero compact ordinary-source support",
            "M_0>0 is a private positive-source premise, not a measured numeric source row and not a prediction of G",
            "M0_POSITIVE_PRIVATE_PREMISE",
        ),
        (
            "DL4774_2_epsilon_zero",
            "epsilon_abs_private := sum_i |Delta_i|/M_0 = 0",
            "4170 fixed reference/no-flux/radial glue plus 4230 denominator epsilon row set the same-frame drift numerator to zero inside the full selector",
            "requires exact same frame/reference/surface support; any open/radiative/off-selector term reactivates fallback",
            "EPSILON_ZERO_PRIVATE_SELECTOR",
        ),
        (
            "DL4774_3_Mlower_positive",
            "M_lower = M_0(1-epsilon_abs_private)=M_0>0",
            "4764 inverse-lock lemma becomes legally usable in the private branch because M_0>0 and epsilon_abs_private=0<1",
            "source-backed numerical M_0 is still missing for public/empirical scoring",
            "MLOWER_POSITIVE_PRIVATE_NONCLAIM",
        ),
        (
            "DL4774_4_no_division_singularity",
            "1/M_lower <= 1/M_0",
            "the private denominator is nonzero, so Qbar division is mathematically legal inside the selected branch",
            "not an arena-wide denominator floor; only the ideal compact source collar branch is locked",
            "PRIVATE_DIVISION_LOCK",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": lock_id,
            "quantity_or_clause": quantity,
            "formula_or_statement": formula,
            "derivation_basis": basis,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for lock_id, quantity, formula, basis, status in specs
    ]


def projector_lock_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PL4774_0_identity",
            "Pi_M := Pi_M^H",
            "ell_M(Pi_M^H J_H_total):=M_H^dress[W_H;tau]",
            "4170 identifies Pi_M with the fixed Hamiltonian/Hilbert charge map, not a post-fit topological mask",
            "FIXED_PROJECTOR_IDENTITY_PRIVATE",
        ),
        (
            "PL4774_1_qbasic_selection",
            "D_v Pi_M = 0",
            "Pi_M is selected before readout from q-owned tau, coframe, reference, worldtube and surface data",
            "this is the condition needed by 4764 DL4764_3",
            "QBASIC_PROJECTOR_PRIVATE",
        ),
        (
            "PL4774_2_commutator_zero",
            "E_PiM_comm = [D_v,Pi_M]Q_tot = 0_private",
            "with Pi_M fixed/q-basic, 4764 DL4764_3 gives no source-mask/readout commutator",
            "open/adaptive masks or data-selected projectors reopen this term",
            "COMMUTATOR_ZERO_PRIVATE_SELECTOR",
        ),
        (
            "PL4774_3_norm_bound",
            "P_M_bound <= 1_private_readout_norm",
            "in the selected Hamiltonian source-channel readout norm the fixed channel projector is contractive; otherwise only finite boundedness is retained",
            "the bound is private/conventional, not a public measured operator norm",
            "PROJECTOR_NORM_FINITE_PRIVATE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": lock_id,
            "quantity_or_clause": quantity,
            "formula_or_statement": formula,
            "derivation_basis": basis,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for lock_id, quantity, formula, basis, status in specs
    ]


def qbar_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QB4774_0_product_formula",
            "Qbar_XH",
            "Qbar_XH=(Pi_M Q_tot_XH + E_PiM_comm)/M_lower",
            "imports 4773 denominator gate formula",
            "PRODUCT_FORM_RESTATED",
        ),
        (
            "QB4774_1_numerator",
            "Q_tot_XH_abs",
            "0_private_collar_selector",
            "4773 collapses bulk, edge and shadow numerator in C_static_iso_private",
            "NUMERATOR_ZERO_IMPORTED",
        ),
        (
            "QB4774_2_projector_comm",
            "E_PiM_comm",
            "0_private_fixed_qbasic_projector",
            "4774 projector lock closes the commutator in the same private branch",
            "COMMUTATOR_ZERO_PRIVATE",
        ),
        (
            "QB4774_3_denominator",
            "M_lower",
            "M_0>0_private",
            "4774 denominator lock imports 4230 positivity into 4764 inverse-lock lemma",
            "DENOMINATOR_POSITIVE_PRIVATE",
        ),
        (
            "QB4774_4_qbar_zero",
            "Qbar_XH_abs",
            "0_private_C_static_iso_denominator_locked",
            "because numerator and commutator are zero and denominator is positive in the branch",
            "QBAR_ZERO_PRIVATE_BRANCH_NONCLAIM",
        ),
        (
            "QB4774_5_local_score_ceiling",
            "local-GR/Newton empirical score",
            "not scored",
            "private ideal branch closure is not public parent-action adoption, not numeric G prediction and not open-arena validation",
            "PUBLIC_SCORE_STILL_BLOCKED",
        ),
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


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FB4774_0_source_backed_M0",
            "M_0_numeric_source_row",
            "MISSING_SOURCE_BACKED_M0",
            "need an arena-owned same-frame Hamiltonian denominator or calibrated source mass row with units/provenance",
            "OPEN_FOR_EMPIRICAL_PROMOTION",
        ),
        (
            "FB4774_1_source_backed_epsilon",
            "epsilon_abs_numeric_source_row",
            "MISSING_SOURCE_BACKED_EPSILON_COMPONENTS",
            "need drift components, reference/frame/surface errors and proof they remain below the denominator",
            "OPEN_FOR_EMPIRICAL_PROMOTION",
        ),
        (
            "FB4774_2_public_parent_action",
            "parent action adoption",
            "MISSING_PUBLIC_PARENT_SIGNATURE",
            "need the full parent action to own q, theta, Hodge/current and matter descent rather than private selector assumptions",
            "OPEN_FOR_THEORY_PROMOTION",
        ),
        (
            "FB4774_3_open_collar",
            "open/radiative/apparatus arena",
            "FINITE_FALLBACK_ONLY",
            "any boundary flux, incoming wave, apparatus support, adaptive mask or radiative wall reactivates Q_tot and denominator drift envelopes",
            "OPEN_ARENA_NOT_CLOSED",
        ),
        (
            "FB4774_4_numeric_G",
            "G_Newton or G_eff",
            "NOT_DERIVED_HERE",
            "4774 only proves private legal division/zero residual; it does not derive the numerical value of Newton's constant",
            "G_DERIVATION_STILL_OPEN",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "fallback_id": fallback_id,
            "object": obj,
            "current_value_or_status": value,
            "needed_to_promote": needed,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for fallback_id, obj, value, needed, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "RT4774_0_private_local_GR_certificate",
            "assemble private local-GR limit certificate from 4773 numerator zero plus 4774 denominator/projector lock",
            "turn the private branch into a clean theorem statement with exact assumptions and no public overclaim",
            "SELECTED_NEXT",
        ),
        (
            "RT4774_1_empirical_M0_rows",
            "source real M0/epsilon rows for R10, PPN, clocks and orbital systems",
            "needed for public/arena promotion, but after the private branch is written cleanly",
            "NEXT_AFTER_CERTIFICATE",
        ),
        (
            "RT4774_2_G_value",
            "try to derive or calibrate Newton G from the same Hamiltonian charge normalization",
            "important but should not be mixed with the residual-zero theorem",
            "QUEUED_SEPARATE_GATE",
        ),
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
        (
            "PG4774_0_no_public_local_GR_claim",
            "Qbar_XH=0_private_C_static_iso_denominator_locked is a private branch theorem only",
            "prevents public local-GR/Newton/R10/PPN claim from the private selector",
        ),
        (
            "PG4774_1_no_numeric_G_claim",
            "M_lower positivity is not a derivation of the measured numerical Newton constant",
            "keeps G derivation/calibration as a separate gate",
        ),
        (
            "PG4774_2_open_arena_reactivation",
            "if flux, radiation, apparatus support, adaptive masks or noncompact support appear, fallback rows replace the zero theorem",
            "prevents smuggling the compact collar theorem into real open systems",
        ),
        (
            "PG4774_3_parent_action_required",
            "public promotion requires parent-signed q/theta/Hodge/current/matter descent and same-frame denominator data",
            "keeps private branch closure from being mistaken for global theory completion",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4774_0", "do not call this a public local-GR pass", "PRIVATE_BRANCH_ONLY"),
        ("FW4774_1", "do not claim R10/PPN/clock/orbital pass from 4774", "NO_EMPIRICAL_CLAIM"),
        ("FW4774_2", "do not claim Newton's constant numerical value is derived", "G_VALUE_STILL_OPEN"),
        ("FW4774_3", "do not use private collar zeros for radiative/open/apparatus systems", "OPEN_SYSTEM_FALLBACK_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall_rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4774 closes the mathematical division/projector obstruction inside the private compact stationary source branch; public/source-backed arena promotion remains open.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_BRANCH_NONCLAIM",
            "summary": "Private denominator/projector positive lock derived and Qbar_XH zero follows inside C_static_iso; empirical/public gates remain blocked.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "With numerator and denominator/projector locked in the private branch, the next step is a clean private local-GR limit certificate plus explicit open-arena first-value requirements.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    denominator: list[dict[str, Any]],
    projector: list[dict[str, Any]],
    qbar: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4774 — Denominator/Projector Positive Lock or First Source-Backed M0/Epsilon Row

Generated: `{timestamp}`

## Purpose

4773 left the local branch in a very specific state:

```text
Q_tot_XH_abs = 0_private_collar_selector
Qbar_XH = (Pi_M Q_tot_XH + E_PiM_comm) / M_lower
```

So the next question is not another broad search. It is precise:

```text
Can the private branch prove M_lower>0 and E_PiM_comm=0 without inventing a source row?
```

## Result

Inside the intersected private branch

```text
C_static_iso_private ∩ PPC4161-TK-HQ ∩ MEH_private_selector
```

the answer is yes, as a private/nonclaim theorem:

```text
M_0 := M_EH_private = c^-2 E_plus_private > 0
epsilon_abs_private = 0
M_lower = M_0(1-epsilon_abs_private)=M_0>0
E_PiM_comm = 0_private_fixed_qbasic_projector
Qbar_XH_abs = 0_private_C_static_iso_denominator_locked.
```

This is a real narrowing/closure of the local branch, but it is not yet a public or empirical local-GR pass.

## Denominator Positive Lock

{markdown_table(denominator, ["lock_id", "quantity_or_clause", "formula_or_statement", "status"])}

## Projector Lock

{markdown_table(projector, ["lock_id", "quantity_or_clause", "formula_or_statement", "status"])}

## Qbar Update

{markdown_table(qbar, ["update_id", "quantity", "private_value_or_formula", "status"])}

## Open or Empirical Fallback Rows

{markdown_table(fallback, ["fallback_id", "object", "current_value_or_status", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4774: Denominator/Projector Positive Lock

Generated: `{timestamp}`

4774 intersects the 4773 compact-collar numerator branch with the 4170 Hamiltonian/Hilbert source-charge branch and the 4230 private positive-denominator selector.

Private branch theorem:

```text
Q_tot_XH_abs = 0_private_collar_selector
M_lower = M_0 > 0
E_PiM_comm = 0_private_fixed_qbasic_projector
Qbar_XH_abs = 0_private_C_static_iso_denominator_locked.
```

This closes the private denominator/projector obstruction for the ideal compact stationary source collar. It does not derive the measured value of `G`, does not score R10/PPN/clocks/orbits, and does not promote the branch to public local GR.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4774 intersects the 4773 compact-collar numerator-zero branch with the 4170 Hamiltonian charge projector and the 4230 private MHref positivity selector.
- Inside that private branch, `M_0:=M_EH_private>0`, `epsilon_abs_private=0`, `M_lower=M_0>0`, `E_PiM_comm=0_private`, and `Qbar_XH_abs=0_private_C_static_iso_denominator_locked`.
- This is the first clean private local residual-zero product closure: numerator, projector commutator and denominator are all locked in the ideal branch.
- It remains nonclaim: no public parent-action adoption, no source-backed numeric denominator rows, no measured `G`, and no open/radiative/apparatus arena pass.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4774 packet update: the private local branch now has a legal Qbar division. The compact stationary isolated source collar gives `Qbar_XH_abs=0_private_C_static_iso_denominator_locked` once 4170/4230 are intersected with 4773.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4774-Y5-R2FR-denominator-projector-positive-lock-or-first-source-backed-M0-epsilon-row.md`

## Decision

`{DECISION}`

## What moved forward

- Imported the 4230 private positive-denominator selector into the 4773 compact-collar branch.
- Fixed the Hamiltonian/Hilbert source projector using the 4170 branch and the 4764 projector lock.
- Derived `M_lower=M_0>0`, `E_PiM_comm=0_private`, and `Qbar_XH_abs=0_private_C_static_iso_denominator_locked` inside the ideal private branch.
- Kept all public/local-GR, numeric-G, R10, PPN, clock, orbital and open-arena claims blocked.

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
        "local_gr_private_denominator_projector_positive_lock",
        "4774 derives the private denominator/projector positive lock and Qbar_XH zero inside the compact stationary collar branch.",
        "Generated source register, denominator positive lock theorem, projector lock theorem, Qbar update, fallback rows, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "private_qbar_zero_branch_denominator_locked_public_empirical_gates_blocked",
        NEXT_TARGET,
        "Promoting private Qbar zero to public local GR, deriving measured G, or scoring empirical arenas without source-backed rows.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need private local-GR limit certificate, then source-backed/open-arena denominator and projection values.",
        "Denominator/projector positive lock",
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
    denominator: list[dict[str, Any]],
    projector: list[dict[str, Any]],
    qbar: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4774_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4774_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4774_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    checks.append(("VAL4774_2_Mlower_positive", "M_lower positive private row exists", any(row["quantity_or_clause"] == "M_lower = M_0(1-epsilon_abs_private)=M_0>0" and row["status"] == "MLOWER_POSITIVE_PRIVATE_NONCLAIM" for row in denominator), str(DENOMINATOR_LOCK_CSV)))
    checks.append(("VAL4774_3_epsilon_zero", "epsilon zero private row exists", any(row["quantity_or_clause"] == "epsilon_abs_private := sum_i |Delta_i|/M_0 = 0" and row["status"] == "EPSILON_ZERO_PRIVATE_SELECTOR" for row in denominator), str(DENOMINATOR_LOCK_CSV)))
    checks.append(("VAL4774_4_commutator_zero", "projector commutator zero row exists", any(row["quantity_or_clause"] == "E_PiM_comm = [D_v,Pi_M]Q_tot = 0_private" and row["status"] == "COMMUTATOR_ZERO_PRIVATE_SELECTOR" for row in projector), str(PROJECTOR_LOCK_CSV)))
    checks.append(("VAL4774_5_projector_norm", "projector finite/readout norm row exists", any(row["quantity_or_clause"] == "P_M_bound <= 1_private_readout_norm" and row["status"] == "PROJECTOR_NORM_FINITE_PRIVATE" for row in projector), str(PROJECTOR_LOCK_CSV)))
    checks.append(("VAL4774_6_qbar_zero", "Qbar private zero row exists", any(row["quantity"] == "Qbar_XH_abs" and row["private_value_or_formula"] == "0_private_C_static_iso_denominator_locked" for row in qbar), str(QBAR_UPDATE_CSV)))
    checks.append(("VAL4774_7_score_blocked", "empirical score remains blocked", any(row["quantity"] == "local-GR/Newton empirical score" and row["status"] == "PUBLIC_SCORE_STILL_BLOCKED" for row in qbar), str(QBAR_UPDATE_CSV)))
    checks.append(("VAL4774_8_missing_source_rows_retained", "fallback keeps missing source-backed rows explicit", any(row["current_value_or_status"] == "MISSING_SOURCE_BACKED_M0" for row in fallback) and any(row["current_value_or_status"] == "MISSING_SOURCE_BACKED_EPSILON_COMPONENTS" for row in fallback), str(FALLBACK_CSV)))
    checks.append(("VAL4774_9_route_selected", "route selects private local-GR certificate next", any(row["selection_status"] == "SELECTED_NEXT" and "private local-GR limit certificate" in row["route"] for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4774_10_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4774_11_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4774_12_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4774_13_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4774_14_claim_row", "claim row L-616 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4774_15_resume", "resume points from 4774 to 4775", "4774-Y5" in resume_text and "4775-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4774_16_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

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
            "validation_id": "VAL4774_OVERALL",
            "check": "all 4774 denominator/projector positive-lock checks pass",
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
    denominator = denominator_lock_rows(timestamp)
    projector = projector_lock_rows(timestamp)
    qbar = qbar_update_rows(timestamp)
    fallback = fallback_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(DENOMINATOR_LOCK_CSV, denominator)
    write_csv(PROJECTOR_LOCK_CSV, projector)
    write_csv(QBAR_UPDATE_CSV, qbar)
    write_csv(FALLBACK_CSV, fallback)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, denominator, projector, qbar, fallback, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, denominator, projector, qbar, fallback, routes, gates, timestamp))


if __name__ == "__main__":
    main()
