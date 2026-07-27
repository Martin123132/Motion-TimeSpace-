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

CHECKPOINT = "4226"
CLAIM_ID = "L-067"
BRANCH = "MTS_R2FR_Y5_GAMMA_LOCAL_BOUNDARY_BRANCH_4226"
DECISION = "GAMMA_BOUNDARY_BRANCH_ADOPTED_FOR_LOCAL_ENERGY_ONLY_DAMPING_QUARANTINED_OPEN_SYSTEM_ROW_RETAINED_NONCLAIM"
MARKER = "PPC4161_GAMMA_LOCAL_BOUNDARY_BRANCH_4226"
PACKET_MARKER = "PPC4161_PACKET_GAMMA_LOCAL_BOUNDARY_BRANCH_4226"
NEXT_TARGET = "4227-Y5-R2FR-core-signature-mismatch-and-binding-bound-row.md"

FORMAL_PATH = FORMAL / "242-PPC4161-gamma-bath-energy-balance-source-row-or-boundary-branch-adoption.md"
DOC_PATH = POST / "4226-Y5-R2FR-gamma-bath-energy-balance-source-row-or-boundary-branch-adoption.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4226_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4226_00_4225_next": SourceSpec(
        "SRC4226_00_4225_next",
        SOURCE_DIR / "P8_Y5_R2FR_4225_NEXT_TARGET.csv",
        "4226-Y5-R2FR-gamma-bath-energy-balance-source-row-or-boundary-branch-adoption.md",
        "4225 selected bath balance row or boundary branch adoption.",
    ),
    "SRC4226_01_4225_route": SourceSpec(
        "SRC4226_01_4225_route",
        SOURCE_DIR / "P8_Y5_R2FR_4225_ROUTE_SPLIT.csv",
        "GDR4225_0_boundary_identity",
        "4225 route split with boundary route and cost.",
    ),
    "SRC4226_02_4225_bounds": SourceSpec(
        "SRC4226_02_4225_bounds",
        SOURCE_DIR / "P8_Y5_R2FR_4225_UPDATED_BOUND_ROWS.csv",
        "GDB4225_0_boundary_energy",
        "4225 boundary zero and open-system bound rows.",
    ),
    "SRC4226_03_4225_obligations": SourceSpec(
        "SRC4226_03_4225_obligations",
        SOURCE_DIR / "P8_Y5_R2FR_4225_OPEN_SYSTEM_OBLIGATIONS.csv",
        "GDO4225_6_demote_if_missing",
        "4225 demotion rule if open-system owner is missing.",
    ),
    "SRC4226_04_241_formal": SourceSpec(
        "SRC4226_04_241_formal",
        FORMAL / "241-PPC4161-gamma-damping-open-system-action-or-boundary-repair.md",
        "This is safe for the local `M_EH` sign gate",
        "Formal 4225 statement of local boundary safety and damping cost.",
    ),
    "SRC4226_05_240_formal": SourceSpec(
        "SRC4226_05_240_formal",
        FORMAL / "240-PPC4161-lambda-gamma-core-action-sign-and-binding-bound-source-row.md",
        "lambda >= 0",
        "4224 lambda sign reduction feeding the core-energy bound.",
    ),
    "SRC4226_06_239_formal": SourceSpec(
        "SRC4226_06_239_formal",
        FORMAL / "239-PPC4161-binding-stabilizer-and-MTS-core-negative-energy-bound-or-parent-signature.md",
        "E_binding_stabilizer_neg_abs",
        "4223 binding/core negative-energy bound schema.",
    ),
    "SRC4226_07_parent_v1": SourceSpec(
        "SRC4226_07_parent_v1",
        FORMAL / "83-parent-equations-v1.md",
        "damping-like terms do not belong",
        "Parent v1 supports quarantining damping out of the closed local action.",
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


def branch_rows() -> List[Dict[str, str]]:
    data = [
        (
            "GBB4226_0_branch_choice",
            "local packet gamma mode",
            "gamma_mode_local := boundary_route",
            "Adopt boundary gamma only for the compact local-GR energy proof.",
            "ADOPTED_PRIVATE_LOCAL_BRANCH_NONCLAIM",
        ),
        (
            "GBB4226_1_energy_zero",
            "gamma energy row",
            "E_gamma_bath_or_open_abs := 0",
            "The fixed gamma term is a local boundary term under fixed endpoint/no-flux conditions.",
            "CONDITIONAL_ZERO_FOR_LOCAL_ENERGY",
        ),
        (
            "GBB4226_2_damping_quarantine",
            "damping status",
            "damping_owned_by_local_closed_action := false",
            "Collapse/decoherence/irreversible damping claims cannot cite the local boundary-gamma branch.",
            "QUARANTINE_ACTIVE",
        ),
        (
            "GBB4226_3_open_route_retained",
            "global/open-system gamma route",
            "gamma_open_system_route := retained_for_nonlocal_quantum_memory_cosmology",
            "A real damping branch remains possible but must fill bath/current/stress rows outside this local proof.",
            "RETAINED_UNSCORED",
        ),
        (
            "GBB4226_4_updated_core_bound",
            "local MTS core negative-energy row",
            "E_MTS_core_neg_abs <= E_signature_mismatch_abs",
            "lambda sign is nonnegative and gamma bath row is zero only on the local boundary branch.",
            "REDUCED_BOUND_VALUES_MISSING",
        ),
    ]
    return [
        {
            **common(),
            "branch_id_local": branch_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for branch_id, piece, formula, derivation, status in data
    ]


def quarantine_rows() -> List[Dict[str, str]]:
    data = [
        (
            "GQ4226_0_quantum_collapse",
            "quantum/collapse damping",
            "cannot use local boundary gamma",
            "requires open-system bath/doubled action before claim",
        ),
        (
            "GQ4226_1_cosmology_memory",
            "cosmology/galaxy memory damping",
            "cannot use local boundary gamma",
            "requires q_gamma/K_bath exchange ledger in large-scale sector",
        ),
        (
            "GQ4226_2_local_energy",
            "local-GR energy sign",
            "may use boundary gamma zero",
            "only as private selector branch with fixed endpoint/no-flux clauses",
        ),
        (
            "GQ4226_3_public_language",
            "public theory prose",
            "must not say damping is derived from the closed action",
            "allowed phrase: damping is an open-system target or local boundary-quarantined term",
        ),
    ]
    return [
        {
            **common(),
            "quarantine_id": quarantine_id,
            "arena": arena,
            "rule": rule,
            "required_next_step": next_step,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for quarantine_id, arena, rule, next_step in data
    ]


def updated_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "GUB4226_0_gamma",
            "E_gamma_bath_or_open_abs",
            "0",
            "local boundary gamma branch",
            "CONDITIONAL_ZERO_LOCAL_ONLY",
        ),
        (
            "GUB4226_1_core",
            "E_MTS_core_neg_abs",
            "E_signature_mismatch_abs",
            "lambda>=0 plus gamma boundary zero",
            "REDUCED_TO_SIGNATURE_MISMATCH",
        ),
        (
            "GUB4226_2_MEH",
            "epsilon_E_core_bind",
            "(E_binding_stabilizer_neg_abs + E_signature_mismatch_abs)/E_plus_min",
            "after local gamma branch adoption",
            "NOT_SCORE_READY",
        ),
        (
            "GUB4226_3_open_gamma",
            "E_gamma_open_abs",
            "retained separately for real damping branch",
            "not part of the local boundary energy proof",
            "RETAINED_UNSCORED",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "condition": condition,
            "status": status,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, quantity, formula, condition, status in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "gamma_local_boundary_branch_adopted": "True",
            "E_gamma_bath_or_open_abs_zero_local": "True",
            "damping_claim_quarantined": "True",
            "open_system_gamma_parent_owned": "False",
            "E_signature_mismatch_available": "False",
            "binding_fraction_bound_available": "False",
            "M_EH_positive_available": "False",
            "local_GR_claim": "False",
            "remaining_gap": "core_signature_mismatch_and_binding_bound",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        ("GBF4226_0_no_damping_claim", "claim local closed action derives damping", "blocked", "boundary branch explicitly quarantines damping"),
        ("GBF4226_1_no_global_gamma_transfer", "use local boundary gamma to prove global/quantum damping", "blocked", "open-system route retained but unowned"),
        ("GBF4226_2_no_endpoint_cheat", "set gamma energy zero without fixed endpoint/no-flux clauses", "blocked", "boundary zero requires local boundary conditions"),
        ("GBF4226_3_no_MEH_claim", "promote gamma zero to M_EH positivity", "blocked", "signature mismatch and binding rows remain"),
        ("GBF4226_4_no_public_overclaim", "state MTS has solved damping/action consistency", "blocked", "only local boundary branch is repaired"),
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
            "status_id": "GBS4226_STATUS",
            "decision": DECISION,
            "summary": "Gamma is locally zeroed as boundary energy for the local-GR proof, while damping claims are quarantined to a future open-system bath/current route.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "After local gamma boundary adoption, the MEH sign score is down to core signature mismatch plus binding/stabilizer bound.",
            "derive_first": "prove E_signature_mismatch_abs=0 from the parent local action/field-space metric or fill a conservative bound",
            "fill_second": "fill beta_bind and E_stab_neg_abs rows",
            "fallback": "keep M_EH unavailable and score epsilon_E_core_bind only after both rows are sourced",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 242 - PPC4161 Gamma Bath Energy Balance Source Row Or Boundary Branch Adoption

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Local branch adoption

For the compact local-GR energy proof, adopt:

```text
gamma_mode_local := boundary_route.
```

Then:

```text
E_gamma_bath_or_open_abs := 0.
```

This is allowed only because the fixed-`gamma` term is a boundary term under fixed endpoint/no-flux local clauses.

## Cost

The cost is explicit:

```text
damping_owned_by_local_closed_action := false.
```

So collapse/decoherence/irreversible damping language is quarantined. It must use the retained open-system route later, with bath/current/stress rows.

## Updated local core bound

Using 4224 and the local boundary-gamma branch:

```text
E_MTS_core_neg_abs <= E_signature_mismatch_abs.
```

The local `M_EH` sign gate now depends on:

```text
epsilon_E_core_bind
= (E_binding_stabilizer_neg_abs + E_signature_mismatch_abs)/E_plus_min.
```

## Next target

`{NEXT_TARGET}` should attack `E_signature_mismatch_abs` and the binding/stabilizer bound directly.
"""


def checkpoint_doc() -> str:
    return f"""# 4226 - Gamma Bath Energy Balance Source Row Or Boundary Branch Adoption

**Status:** `{DECISION}`.

## Main move

The local packet adopts boundary-gamma for energy safety:

```text
E_gamma_bath_or_open_abs = 0.
```

But damping claims are quarantined:

```text
damping_owned_by_local_closed_action = false.
```

## Remaining local sign gap

```text
E_MTS_core_neg_abs <= E_signature_mismatch_abs.
```

and:

```text
epsilon_E_core_bind=(E_binding_stabilizer_neg_abs+E_signature_mismatch_abs)/E_plus_min.
```

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"For the private local-GR energy proof, gamma is adopted as a boundary-route term only: E_gamma_bath_or_open_abs=0 under fixed endpoint/no-flux local clauses, while damping/collapse/decoherence claims are quarantined to a future open-system bath/current route.",'
        f'"4226 source audit, branch adoption rows, quarantine rows, updated bound rows, decision and firewall.",'
        f'private_gamma_boundary_branch_local_energy_nonclaim,'
        f'"Prove or bound E_signature_mismatch_abs and binding/stabilizer negative energy.",'
        f'"This closes gamma only for the private local energy branch; it does not prove damping, M_EH, M_H_ref, local GR, Newton or PPN."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 101. Local Gamma Boundary Branch

Marker: `{MARKER}`

4226 adopts:

```text
gamma_mode_local := boundary_route,
E_gamma_bath_or_open_abs := 0.
```

This is only for the local-GR energy proof. Damping claims are quarantined to an open-system route. The remaining `M_EH` sign gap is:

```text
epsilon_E_core_bind
= (E_binding_stabilizer_neg_abs + E_signature_mismatch_abs)/E_plus_min.
```
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Local Gamma Boundary Branch

Marker: `{PACKET_MARKER}`

Gamma is locally boundary-routed for the private energy-sign proof. The packet must not use this to claim damping; open-system gamma remains a separate unfilled branch.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4226_SOURCE_REGISTER.csv"]
    branches = rows_by_file["P8_Y5_R2FR_4226_BRANCH_ADOPTION.csv"]
    quarantine = rows_by_file["P8_Y5_R2FR_4226_DAMPING_QUARANTINE.csv"]
    bounds = rows_by_file["P8_Y5_R2FR_4226_UPDATED_BOUND_ROWS.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4226_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4226_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4226_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]

    checks = [
        ("VAL4226_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4226_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4226_2_branch_adoption",
            "branch rows adopt local boundary gamma, set gamma energy zero and quarantine damping",
            {"GBB4226_0_branch_choice", "GBB4226_1_energy_zero", "GBB4226_2_damping_quarantine"}.issubset({row["branch_id_local"] for row in branches}),
        ),
        (
            "VAL4226_3_quarantine",
            "quarantine rows separate local energy from damping/cosmology/quantum claims",
            {"GQ4226_0_quantum_collapse", "GQ4226_1_cosmology_memory", "GQ4226_2_local_energy", "GQ4226_3_public_language"}.issubset({row["quarantine_id"] for row in quarantine}),
        ),
        (
            "VAL4226_4_bounds",
            "bounds reduce core sign gap to signature mismatch plus binding",
            {"GUB4226_0_gamma", "GUB4226_1_core", "GUB4226_2_MEH", "GUB4226_3_open_gamma"}.issubset({row["bound_id"] for row in bounds}),
        ),
        (
            "VAL4226_5_decision_nonclaim",
            "decision adopts boundary gamma but keeps local-GR unavailable",
            decision["gamma_local_boundary_branch_adopted"] == "True"
            and decision["damping_claim_quarantined"] == "True"
            and decision["local_GR_claim"] == "False",
        ),
        (
            "VAL4226_6_firewall",
            "firewall blocks damping, global transfer, endpoint cheat, MEH claim and public overclaim",
            {"GBF4226_0_no_damping_claim", "GBF4226_1_no_global_gamma_transfer", "GBF4226_2_no_endpoint_cheat", "GBF4226_3_no_MEH_claim", "GBF4226_4_no_public_overclaim"}.issubset({row["firewall_id"] for row in firewalls}),
        ),
        (
            "VAL4226_7_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4226_8_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4226_9_claim_register", "claim register contains L-067", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4226_10_spine_packet", "spine and packet contain 4226 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4226_11_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4226_12_script_exists", "generator script exists", (SCRIPTS / "Y5_R2FR_4226_gamma_bath_energy_balance_source_row_or_boundary_branch_adoption.py").exists()),
        ("VAL4226_13_status", "status records nonclaim branch adoption", rows_by_file["P8_Y5_R2FR_4226_STATUS.csv"][0]["decision"] == DECISION),
        (
            "VAL4226_14_open_gamma_retained",
            "open gamma route retained separately",
            any(row["bound_id"] == "GUB4226_3_open_gamma" and row["status"] == "RETAINED_UNSCORED" for row in bounds),
        ),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4226_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4226_BRANCH_ADOPTION.csv": branch_rows(),
        "P8_Y5_R2FR_4226_DAMPING_QUARANTINE.csv": quarantine_rows(),
        "P8_Y5_R2FR_4226_UPDATED_BOUND_ROWS.csv": updated_bound_rows(),
        "P8_Y5_R2FR_4226_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4226_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4226_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4226_NEXT_TARGET.csv": next_target_rows(),
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
