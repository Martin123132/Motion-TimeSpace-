from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4222"
CLAIM_ID = "L-063"
BRANCH = "MTS_R2FR_Y5_POSITIVE_ENERGY_SIGNATURE_MATRIX_4222"
DECISION = "POSITIVE_ENERGY_SIGNATURE_MATRIX_PARTIALLY_SIGNED_VISIBLE_MAXWELL_TOPOLOGICAL_ZERO_BINDING_AND_MTS_CORE_NEGATIVE_BOUND_ROWS_STAGED_NONCLAIM"
MARKER = "PPC4161_POSITIVE_ENERGY_SIGNATURE_MATRIX_4222"
PACKET_MARKER = "PPC4161_PACKET_POSITIVE_ENERGY_SIGNATURE_MATRIX_4222"
NEXT_TARGET = "4223-Y5-R2FR-binding-stabilizer-and-MTS-core-negative-energy-bound-or-parent-signature.md"

FORMAL_PATH = FORMAL / "238-PPC4161-positive-energy-sector-signature-matrix-or-negative-energy-bound-fill.md"
DOC_PATH = POST / "4222-Y5-R2FR-positive-energy-sector-signature-matrix-or-negative-energy-bound-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4222_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4222_00_4221_next": SourceSpec(
        "SRC4222_00_4221_next",
        SOURCE_DIR / "P8_Y5_R2FR_4221_NEXT_TARGET.csv",
        "4222-Y5-R2FR-positive-energy-sector-signature-matrix-or-negative-energy-bound-fill.md",
        "4221 selected the parent energy-signature matrix or negative-energy bound fill.",
    ),
    "SRC4222_01_4221_formal": SourceSpec(
        "SRC4222_01_4221_formal",
        FORMAL / "237-PPC4161-MEH-positive-source-comparator-and-residual-input-fill.md",
        "M_EH >= c^-2 E_plus",
        "MEH lower-bound law requiring E_plus and epsilon_E inputs.",
    ),
    "SRC4222_02_185_source": SourceSpec(
        "SRC4222_02_185_source",
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H = T_matter + T_EM + T_binding",
        "Hilbert source sector decomposition.",
    ),
    "SRC4222_03_191_maxwell": SourceSpec(
        "SRC4222_03_191_maxwell",
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "rho_EM = T_EM(n,n)",
        "Maxwell-Hodge energy and Poynting ownership.",
    ),
    "SRC4222_04_184_topological": SourceSpec(
        "SRC4222_04_184_topological",
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "T_top^munu",
        "Topological kappa sector stress/source blindness.",
    ),
    "SRC4222_05_234_visible": SourceSpec(
        "SRC4222_05_234_visible",
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "S_vis_standard",
        "Standard visible import and MTS visible deformation guard.",
    ),
    "SRC4222_06_190_selector": SourceSpec(
        "SRC4222_06_190_selector",
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "single Hilbert source functor",
        "Parent local selector and quarantine rule.",
    ),
    "SRC4222_07_3948_energy_gate": SourceSpec(
        "SRC4222_07_3948_energy_gate",
        SOURCE_DIR / "P8_Y5_R2FR_3948_MEH_ENERGY_CONDITION_GATE.csv",
        "BLOCKED_SIGNATURE_MATRIX_MISSING",
        "Earlier energy condition gate naming the missing signature matrix.",
    ),
    "SRC4222_08_4221_sector": SourceSpec(
        "SRC4222_08_4221_sector",
        SOURCE_DIR / "P8_Y5_R2FR_4221_SECTOR_SIGNATURE_MATRIX.csv",
        "MES4221_3_motion_time_space_core",
        "4221 sector matrix to be sharpened.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in SOURCE_SPECS.values():
        text = read_text(source.path)
        rows.append(
            {
                **common(),
                "source_id": source.source_id,
                "path": str(source.path),
                "exists": str(source.path.exists()),
                "required_text": source.required_text,
                "required_text_found": str(source.required_text in text),
                "role": source.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def signature_rows() -> List[Dict[str, str]]:
    data = [
        (
            "PES4222_0_visible_standard",
            "standard visible matter source",
            "E_visible_pos",
            "positive only under standard local visible import and nonzero support",
            "CONDITIONAL_POSITIVE_SECTOR",
            "goes into E_plus if support row exists",
        ),
        (
            "PES4222_1_Maxwell_Hodge_closed",
            "closed Maxwell-Hodge field energy",
            "E_EM_closed = int rho_EM dV",
            "rho_EM = 1/2(E^2+B^2) in observed Hodge/coframe branch",
            "CONDITIONAL_POSITIVE_SECTOR",
            "goes into E_plus for closed/stationary support; open flux goes to E_open_abs",
        ),
        (
            "PES4222_2_topological_kappa",
            "topological kappa sector",
            "E_top = 0",
            "T_top^munu=0 because S_top is metric/source blind inside packet",
            "CONDITIONAL_ZERO_SECTOR",
            "does not damage sign and cannot supply source mass",
        ),
        (
            "PES4222_3_exact_improvement",
            "exact improvement/boundary sector",
            "E_impr = 0 or E_ref_abs/E_open_abs",
            "exact improvements are boundary-only in closed collars",
            "ZERO_OR_BOUND_REQUIRED",
            "closed-domain zero if boundary silence signed; otherwise residual",
        ),
        (
            "PES4222_4_binding_stabilizer",
            "binding and stabilizer sector",
            "E_binding+E_stabilizer",
            "no parent no-ghost/bounded-below signature currently signed",
            "MISSING_PARENT_SIGNATURE_OR_BOUND",
            "first real negative-energy bound target",
        ),
        (
            "PES4222_5_MTS_core_memory",
            "MTS core/memory/extra local sector",
            "E_MTS_core",
            "no complete kinetic/Hessian/constraint-stability signature currently signed",
            "MISSING_PARENT_SIGNATURE_OR_BOUND",
            "first real parent-signature target",
        ),
        (
            "PES4222_6_virial_pressure",
            "Komar/Tolman pressure-stress sector",
            "E_vir_abs",
            "zero only under closed stationary total-source virial theorem",
            "ZERO_OR_BOUND_REQUIRED",
            "cannot be deleted from active mass route",
        ),
        (
            "PES4222_7_frame_reference_open",
            "frame/reference/open-flux sector",
            "E_frame_abs+E_ref_abs+E_open_abs",
            "zero only under same-frame lock, source-blind reference and no open flux",
            "ZERO_OR_BOUND_REQUIRED",
            "feeds epsilon_E if not zero",
        ),
    ]
    return [
        {
            **common(),
            "signature_id": signature_id,
            "sector": sector,
            "energy_piece": energy_piece,
            "signature_statement": signature_statement,
            "status": status,
            "MEH_role": role,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for signature_id, sector, energy_piece, signature_statement, status, role in data
    ]


def signed_piece_rows() -> List[Dict[str, str]]:
    data = [
        (
            "EPS4222_0_Eplus_visible_EM",
            "E_plus_min",
            "E_visible_pos + E_EM_closed + E_signed_parent_pos",
            "partial positive-sector expression",
            "DERIVED_SYMBOLIC_NO_VALUE",
        ),
        (
            "EPS4222_1_Etop_zero",
            "E_top",
            "0",
            "topological kappa contributes no Hilbert source stress",
            "CONDITIONAL_ZERO",
        ),
        (
            "EPS4222_2_Eopen_routing",
            "E_open_abs",
            "abs(open Poynting/radiative/boundary flux)",
            "not bulk source; must be zero or bounded",
            "BOUND_REQUIRED",
        ),
        (
            "EPS4222_3_Eneg_unfilled",
            "E_neg_abs",
            "abs(negative binding/stabilizer/MTS-core pieces)",
            "not signed by current parent action",
            "BOUND_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "piece_id": piece_id,
            "quantity": quantity,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for piece_id, quantity, formula, derivation, status in data
    ]


def negative_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "NEB4222_0_binding_stabilizer",
            "E_binding_stabilizer_neg_abs",
            "abs(min(0,E_binding+E_stabilizer))",
            "parent bounded-below theorem or conservative source-bound row",
            "MISSING_PARENT_SIGNATURE_OR_NUMERIC_BOUND",
        ),
        (
            "NEB4222_1_MTS_core",
            "E_MTS_core_neg_abs",
            "abs(min(0,E_MTS_core))",
            "field-space kinetic/Hessian/constraint-stability signature or conservative bound",
            "MISSING_PARENT_SIGNATURE_OR_NUMERIC_BOUND",
        ),
        (
            "NEB4222_2_nonEH_leakage",
            "E_nonEH_abs",
            "absolute non-EH source leakage",
            "selector theorem zero or finite residual source row",
            "MISSING_ZERO_OR_BOUND",
        ),
        (
            "NEB4222_3_first_score",
            "epsilon_E_partial",
            "(E_binding_stabilizer_neg_abs+E_MTS_core_neg_abs+E_nonEH_abs+E_open_abs+E_ref_abs+E_vir_abs+E_frame_abs)/E_plus_min",
            "computed only after positive support and negative/open bound rows exist",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "quantity": quantity,
            "formula": formula,
            "required_evidence": required_evidence,
            "current_status": current_status,
            "source_path": "MISSING_SOURCE_ROW",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, quantity, formula, required_evidence, current_status in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "visible_standard_signed_conditional": "True",
            "Maxwell_Hodge_positive_conditional": "True",
            "topological_kappa_zero_conditional": "True",
            "binding_stabilizer_signed": "False",
            "MTS_core_signed": "False",
            "negative_bound_values_available": "False",
            "E_plus_available": "False",
            "epsilon_E_computable": "False",
            "M_EH_positive_available": "False",
            "local_GR_claim": "False",
            "remaining_gap": "binding_stabilizer_and_MTS_core_parent_signature_or_negative_energy_bounds",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        ("PEF4222_0_no_visible_only_claim", "visible+EM positivity alone proves M_EH>0", "blocked", "binding/stabilizer/MTS/open/reference/stress sectors can still damage total sign"),
        ("PEF4222_1_no_topological_mass", "topological kappa zero supplies source mass", "blocked", "T_top=0 helps by not spoiling sign; it does not create E_plus"),
        ("PEF4222_2_no_EM_flux_erasure", "open Poynting flux is ignored", "blocked", "open flux is E_open_abs unless boundary-routed zero is signed"),
        ("PEF4222_3_no_binding_assumption", "binding/stabilizer is automatically positive", "blocked", "requires parent no-ghost/bounded-below theorem or conservative bound"),
        ("PEF4222_4_no_MTS_core_assumption", "MTS core energy is automatically positive", "blocked", "requires kinetic/Hessian/constraint-stability signature"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move, status, reason in data
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "PES4222_STATUS",
            "decision": DECISION,
            "summary": "Standard visible matter and closed Maxwell-Hodge energy can feed E_plus conditionally; topological kappa is source-zero; binding/stabilizer and MTS core need parent signatures or conservative negative-energy bounds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4222 partially signs the energy matrix; the first remaining sign-damaging sectors are binding/stabilizer and MTS core.",
            "derive_first": "bounded-below/no-ghost parent signature for S_binding+S_stabilizer and the MTS core local residual sector",
            "fill_second": "conservative E_binding_stabilizer_neg_abs and E_MTS_core_neg_abs rows if a theorem-zero/sign proof fails",
            "fallback": "keep M_EH and M_H_ref unavailable while scoring epsilon_E_partial",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 238 - PPC4161 Positive Energy Sector Signature Matrix Or Negative Energy Bound Fill

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Purpose

4221 derived:

```text
M_EH >= c^-2 E_plus(1-epsilon_E).
```

4222 asks which pieces of `E_plus` and `epsilon_E` can actually be signed from the local packet.

## Partial signatures

The current source hierarchy supports three useful conditional statements:

```text
E_visible_pos >= 0
```

inside the standard visible import branch with nonzero same-frame support;

```text
E_EM_closed = int rho_EM dV >= 0
```

for closed/stationary Maxwell-Hodge energy in the observed Hodge/coframe branch; and

```text
E_top = 0
```

for the parent-adopted topological kappa sector because `T_top^munu=0`.

So the minimum signed positive pool is:

```text
E_plus_min = E_visible_pos + E_EM_closed + E_signed_parent_pos.
```

## What still blocks the sign

The following cannot be signed from current files:

```text
E_binding_stabilizer_neg_abs,
E_MTS_core_neg_abs,
E_nonEH_abs.
```

Open Poynting/radiative flux, reference leakage, virial pressure terms and frame mismatch also remain zero-or-bound gates:

```text
E_open_abs + E_ref_abs + E_vir_abs + E_frame_abs.
```

## Result

This is a real partial derivation, but not a denominator pass:

```text
M_EH >= c^-2 E_plus_min(1-epsilon_E_partial)
```

only becomes useful once `E_plus_min>0` and `epsilon_E_partial<1` are source-backed.

## Next target

`{NEXT_TARGET}` should attack the first sign-damaging sectors directly: binding/stabilizer and MTS core.
"""


def checkpoint_doc() -> str:
    return f"""# 4222 - Positive Energy Sector Signature Matrix Or Negative Energy Bound Fill

**Status:** `{DECISION}`.

## Main move

The energy-signature matrix is no longer blank:

- standard visible matter can enter `E_plus` conditionally;
- closed Maxwell-Hodge energy can enter `E_plus` conditionally;
- topological kappa contributes zero stress/source energy;
- binding/stabilizer and MTS core remain unsigned and require bounds.

## Working inequality

```text
M_EH >= c^-2 E_plus_min(1-epsilon_E_partial).
```

No local-GR or Newton source-normalization claim follows yet, because `E_plus_min` and `epsilon_E_partial` are not scored.

## Generated rows

- `P8_Y5_R2FR_4222_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4222_SIGNATURE_MATRIX.csv`
- `P8_Y5_R2FR_4222_SIGNED_PIECES.csv`
- `P8_Y5_R2FR_4222_NEGATIVE_BOUND_ROWS.csv`
- `P8_Y5_R2FR_4222_DECISION.csv`
- `P8_Y5_R2FR_4222_CLAIM_FIREWALL.csv`
- `P8_Y5_R2FR_4222_STATUS.csv`
- `P8_Y5_R2FR_4222_NEXT_TARGET.csv`

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The M_EH energy-signature matrix is partially signed: standard visible matter and closed Maxwell-Hodge energy can contribute to E_plus conditionally, topological kappa is a zero-source sector, and binding/stabilizer plus MTS-core terms are isolated as negative-energy/bounded-below rows.",'
        f'"4222 source audit, signature matrix, signed pieces, negative bound rows, decision and firewall.",'
        f'private_positive_energy_matrix_partial_nonclaim,'
        f'"Prove or bound the binding/stabilizer and MTS-core energy signs.",'
        f'"This is a partial signature split, not an M_EH positivity proof; E_plus and epsilon_E remain unscored."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 97. Positive Energy Sector Signature Matrix

Marker: `{MARKER}`

4222 partially signs the `M_EH` energy matrix:

```text
E_plus_min = E_visible_pos + E_EM_closed + E_signed_parent_pos.
```

Topological kappa is source-zero, not source-positive. Binding/stabilizer and MTS-core energy remain the first sign-damaging sectors to prove or bound.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Positive Energy Sector Matrix

Marker: `{PACKET_MARKER}`

The packet now separates signed-positive, zero-source and unsigned energy sectors. It remains private/nonclaim until binding/stabilizer and MTS-core negative-energy rows are theorem-zero, bounded small, or parent-signature positive.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4222_SOURCE_REGISTER.csv"]
    signatures = rows_by_file["P8_Y5_R2FR_4222_SIGNATURE_MATRIX.csv"]
    pieces = rows_by_file["P8_Y5_R2FR_4222_SIGNED_PIECES.csv"]
    bounds = rows_by_file["P8_Y5_R2FR_4222_NEGATIVE_BOUND_ROWS.csv"]
    decisions = rows_by_file["P8_Y5_R2FR_4222_DECISION.csv"]
    firewalls = rows_by_file["P8_Y5_R2FR_4222_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4222_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]
    decision = decisions[0]

    checks = [
        ("VAL4222_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4222_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4222_2_signature_coverage",
            "signature matrix covers visible, Maxwell, topological, binding, MTS, virial and frame/reference/open sectors",
            {"PES4222_0_visible_standard", "PES4222_1_Maxwell_Hodge_closed", "PES4222_2_topological_kappa", "PES4222_4_binding_stabilizer", "PES4222_5_MTS_core_memory", "PES4222_6_virial_pressure", "PES4222_7_frame_reference_open"}.issubset({row["signature_id"] for row in signatures}),
        ),
        (
            "VAL4222_3_partial_signatures",
            "visible and Maxwell are conditional positive while topological is conditional zero",
            any(row["signature_id"] == "PES4222_0_visible_standard" and row["status"] == "CONDITIONAL_POSITIVE_SECTOR" for row in signatures)
            and any(row["signature_id"] == "PES4222_1_Maxwell_Hodge_closed" and row["status"] == "CONDITIONAL_POSITIVE_SECTOR" for row in signatures)
            and any(row["signature_id"] == "PES4222_2_topological_kappa" and row["status"] == "CONDITIONAL_ZERO_SECTOR" for row in signatures),
        ),
        (
            "VAL4222_4_unsigned_sectors_retained",
            "binding and MTS core remain missing signature/bound",
            any(row["signature_id"] == "PES4222_4_binding_stabilizer" and row["status"] == "MISSING_PARENT_SIGNATURE_OR_BOUND" for row in signatures)
            and any(row["signature_id"] == "PES4222_5_MTS_core_memory" and row["status"] == "MISSING_PARENT_SIGNATURE_OR_BOUND" for row in signatures),
        ),
        (
            "VAL4222_5_signed_pieces",
            "signed pieces include E_plus_min, E_top zero and E_open routing",
            {"EPS4222_0_Eplus_visible_EM", "EPS4222_1_Etop_zero", "EPS4222_2_Eopen_routing", "EPS4222_3_Eneg_unfilled"}.issubset({row["piece_id"] for row in pieces}),
        ),
        (
            "VAL4222_6_negative_bounds",
            "negative bound rows stage binding, MTS core, nonEH and epsilon partial",
            {"NEB4222_0_binding_stabilizer", "NEB4222_1_MTS_core", "NEB4222_2_nonEH_leakage", "NEB4222_3_first_score"}.issubset({row["bound_id"] for row in bounds}),
        ),
        (
            "VAL4222_7_decision_nonclaim",
            "decision keeps MEH/local-GR unavailable",
            decision["M_EH_positive_available"] == "False" and decision["local_GR_claim"] == "False" and decision["negative_bound_values_available"] == "False",
        ),
        (
            "VAL4222_8_firewall",
            "firewall blocks visible-only, topological-mass, flux-erasure, binding and MTS assumptions",
            {"PEF4222_0_no_visible_only_claim", "PEF4222_1_no_topological_mass", "PEF4222_2_no_EM_flux_erasure", "PEF4222_3_no_binding_assumption", "PEF4222_4_no_MTS_core_assumption"}.issubset({row["firewall_id"] for row in firewalls}),
        ),
        (
            "VAL4222_9_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4222_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4222_11_claim_register", "claim register contains L-063", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4222_12_spine_packet", "spine and packet contain 4222 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4222_13_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4222_14_script_exists", "generator script exists", (SCRIPTS / "Y5_R2FR_4222_positive_energy_sector_signature_matrix_or_negative_energy_bound_fill.py").exists()),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
        }
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4222_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4222_SIGNATURE_MATRIX.csv": signature_rows(),
        "P8_Y5_R2FR_4222_SIGNED_PIECES.csv": signed_piece_rows(),
        "P8_Y5_R2FR_4222_NEGATIVE_BOUND_ROWS.csv": negative_bound_rows(),
        "P8_Y5_R2FR_4222_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4222_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4222_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4222_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)

    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8")
    update_registers()
    validation_rows = validate(rows_by_file)
    write_csv(VALIDATION_PATH, validation_rows)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={VALIDATION_PATH}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
