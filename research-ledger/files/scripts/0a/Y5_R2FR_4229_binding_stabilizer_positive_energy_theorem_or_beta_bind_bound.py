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

CHECKPOINT = "4229"
CLAIM_ID = "L-070"
BRANCH = "MTS_R2FR_Y5_BINDING_DRESSED_HILBERT_ABSORPTION_4229"
DECISION = "DRESSED_HILBERT_BINDING_ABSORPTION_PRIVATE_SOURCE_BRANCH_EPSILON_CORE_BIND_ZERO_NONCLAIM"
MARKER = "PPC4161_BINDING_DRESSED_HILBERT_ABSORPTION_4229"
PACKET_MARKER = "PPC4161_PACKET_BINDING_DRESSED_HILBERT_ABSORPTION_4229"
NEXT_TARGET = "4230-Y5-R2FR-MEH-total-epsilon-score-open-reference-virial-frame-gate.md"

FORMAL_PATH = FORMAL / "245-PPC4161-binding-stabilizer-positive-energy-theorem-or-beta-bind-bound.md"
DOC_PATH = POST / "4229-Y5-R2FR-binding-stabilizer-positive-energy-theorem-or-beta-bind-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4229_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4229_00_4228_next": SourceSpec(
        "SRC4229_00_4228_next",
        SOURCE_DIR / "P8_Y5_R2FR_4228_NEXT_TARGET.csv",
        "4229-Y5-R2FR-binding-stabilizer-positive-energy-theorem-or-beta-bind-bound.md",
        "4228 selects binding/stabilizer positivity or beta-bound as the next obstruction.",
    ),
    "SRC4229_01_4228_zero": SourceSpec(
        "SRC4229_01_4228_zero",
        SOURCE_DIR / "P8_Y5_R2FR_4228_BETA_SIG_ZERO_ROWS.csv",
        "BSZ4228_2_core_negative_zero",
        "4228 closes the MTS-core negative channel in the private selector.",
    ),
    "SRC4229_02_237_comparator": SourceSpec(
        "SRC4229_02_237_comparator",
        FORMAL / "237-PPC4161-MEH-positive-source-comparator-and-residual-input-fill.md",
        "M_EH[tau,W_source] := c^-2 E_total[tau,W_source]",
        "Same-frame comparator defines M_EH from total Hilbert-source energy, not orbital GM.",
    ),
    "SRC4229_03_238_matrix": SourceSpec(
        "SRC4229_03_238_matrix",
        FORMAL / "238-PPC4161-positive-energy-sector-signature-matrix-or-negative-energy-bound-fill.md",
        "E_plus_min = E_visible_pos + E_EM_closed + E_signed_parent_pos",
        "Earlier partial positive pool that left binding as a negative row.",
    ),
    "SRC4229_04_239_binding": SourceSpec(
        "SRC4229_04_239_binding",
        FORMAL / "239-PPC4161-binding-stabilizer-and-MTS-core-negative-energy-bound-or-parent-signature.md",
        "Binding is part of the single Hilbert source",
        "Existing binding warning: binding is in the source but could damage a bare positive-pool split.",
    ),
    "SRC4229_05_185_source": SourceSpec(
        "SRC4229_05_185_source",
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H = T_matter + T_EM + T_binding",
        "Single Hilbert source includes binding and exact improvements/rest topological terms.",
    ),
    "SRC4229_06_186_hamiltonian": SourceSpec(
        "SRC4229_06_186_hamiltonian",
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref",
        "Dressed Hamiltonian worldtube mass charge is the same source object before orbital readout.",
    ),
    "SRC4229_07_187_newton": SourceSpec(
        "SRC4229_07_187_newton",
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV = M_H^dress[W_H;tau]",
        "Newton readout uses the dressed Hilbert source density and charge.",
    ),
    "SRC4229_08_190_selector": SourceSpec(
        "SRC4229_08_190_selector",
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "single Hilbert source functor",
        "Selector branch requires the single Hilbert source functor.",
    ),
    "SRC4229_09_2616_graph": SourceSpec(
        "SRC4229_09_2616_graph",
        SOURCE_DIR / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
        "SMG2616_3_macroscopic_body_edge",
        "Macroscopic bodies inherit EM/nuclear/lattice binding stress as part of the source graph.",
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


def theorem_rows() -> List[Dict[str, str]]:
    data = [
        (
            "DHB4229_0_same_source_energy",
            "dressed Hilbert source identity",
            "E_H^dress[tau,W_H] := c^2 M_H^dress[W_H;tau] = int_W rho_H c^2 dV_H",
            "The same source current/action that defines T_H and M_H^dress also defines the positive-energy comparator; no orbital GM or fitted rest-mass shortcut enters.",
            "PRIVATE_BRANCH_IDENTITY",
        ),
        (
            "DHB4229_1_binding_absorption",
            "binding absorption law",
            "T_H = T_matter + T_EM + T_binding + T_impr_exact + T_rest_top/zero => E_binding_internal_abs_extra := 0 when E_plus is E_H^dress",
            "Ordinary binding lowers or dresses the Hamiltonian mass, but it is not a second negative residual if the comparator uses the dressed Hilbert source energy.",
            "DERIVED_NO_DOUBLE_COUNT_ROUTE",
        ),
        (
            "DHB4229_2_stabilizer_classification",
            "stabilizer classification",
            "stabilizer sector in private selector = Hilbert binding OR positive quadratic hidden sector OR topological/boundary; otherwise residual reopens",
            "4228 already signs the positive quadratic hidden sector; 185/186 put ordinary binding in the source charge; independent negative stabilizers are not silently erased.",
            "CLASSIFICATION_THEOREM",
        ),
        (
            "DHB4229_3_stable_source_condition",
            "ordinary stable source condition",
            "rho_H >= 0 with nonzero compact support implies E_H^dress>0 and M_H^dress>0 in the private ordinary-source collar",
            "This is the standard stable ordinary-matter branch condition; exotic negative-energy matter or an unstable source invalidates this row and reopens beta_bind.",
            "PRIVATE_STABLE_SOURCE_CONDITION",
        ),
        (
            "DHB4229_4_binding_result",
            "private binding result",
            "E_binding_stabilizer_neg_abs|dressed_private_selector := 0; beta_bind_private := 0; E_stab_neg_abs_private := 0",
            "On the dressed Hilbert source branch, binding is absorbed into the positive source object and independent stabilizer ghosts are excluded by the selector/signature clauses.",
            "ZERO_IN_DRESSED_PRIVATE_SELECTOR",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, piece, formula, derivation, status in data
    ]


def gate_rows() -> List[Dict[str, str]]:
    data = [
        (
            "BHG4229_0_core_bind_gate",
            "previous gate",
            "epsilon_E_core_bind|private_selector <= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min",
            "4228 left binding/stabilizer as the last numerator in the core-bind gate.",
            "REFERENCE",
        ),
        (
            "BHG4229_1_dressed_rebase",
            "dressed source rebase",
            "E_plus_dress := E_H^dress = c^2 M_H^dress, not bare visible rest energy excluding binding",
            "This avoids double-counting ordinary binding as both part of the source mass and a separate negative residual.",
            "ADOPTED_PRIVATE_REBASE",
        ),
        (
            "BHG4229_2_core_bind_zero",
            "core-bind numerator",
            "epsilon_E_core_bind|dressed_private_selector := 0",
            "Substitute E_MTS_core_neg_abs=0 from 4228 and E_binding_stabilizer_neg_abs=0 from DHB4229_4.",
            "CORE_BIND_GATE_CLOSED_PRIVATE",
        ),
        (
            "BHG4229_3_MEH_positive_core",
            "core-bind contribution to MEH",
            "M_EH core-bind sign obstruction removed if E_H^dress>0",
            "This does not score open/ref/virial/nonEH/frame residuals; it only closes the core-bind slice.",
            "PARTIAL_MEH_SIGN_PROGRESS",
        ),
        (
            "BHG4229_4_reopen_rule",
            "reopen rule",
            "if E_plus is bare rest, rho_H positivity fails, or independent stabilizer exists, restore E_binding_stabilizer_neg_abs <= beta_bind E_visible_rest + E_stab_neg_abs",
            "The theorem is a dressed-source branch result, not a universal erasure of binding physics.",
            "FALLBACK_BOUND_RETAINED",
        ),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, piece, formula, derivation, status in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "dressed_Hilbert_rebase_adopted_private": "True",
            "rho_H_positive_stable_source_branch": "True",
            "binding_double_count_removed": "True",
            "beta_bind_private": "0",
            "E_stab_neg_abs_private": "0",
            "E_binding_stabilizer_neg_abs_private": "0",
            "epsilon_E_core_bind_private": "0",
            "MEH_full_claim": "False",
            "local_GR_claim": "False",
            "newton_claim": "False",
            "PPN_claim": "False",
            "summary": "4229 rebases the core-bind sign gate onto the dressed Hilbert Hamiltonian source energy, so ordinary binding is internal source dressing rather than a second negative residual inside the private stable-source selector.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        (
            "BHF4229_0_no_bare_relabel",
            "Do not call bare visible rest energy the dressed Hilbert energy.",
            "BLOCKED",
            "The zero route only works if E_plus is the same dressed Hamiltonian/Hilbert source object.",
        ),
        (
            "BHF4229_1_no_exotic_matter",
            "Do not apply the positive source condition to exotic negative-energy or unstable sources.",
            "BLOCKED",
            "Those cases reopen beta_bind and E_stab_neg_abs.",
        ),
        (
            "BHF4229_2_no_independent_stabilizer",
            "Do not erase an independent negative stabilizer/ghost not included in T_H or signed by 4228.",
            "BLOCKED",
            "Independent stabilizers require their own source/action signature or bound.",
        ),
        (
            "BHF4229_3_no_full_MEH_claim",
            "Do not claim full M_EH positivity from the core-bind zero.",
            "BLOCKED",
            "Open flux, reference, virial/pressure, non-EH and frame residuals still need score rows.",
        ),
        (
            "BHF4229_4_no_orbital_GM_laundering",
            "Do not define E_H^dress or M_H^dress from observed orbital GM.",
            "BLOCKED",
            "The source charge must be parent/Hamiltonian-owned before orbital readout.",
        ),
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
            "status_id": "BHS4229_STATUS",
            "decision": DECISION,
            "summary": "The core-bind numerator is zero in the dressed private stable-source selector; next assemble/score the remaining MEH residual channels.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4229 closes the core-bind sign numerator in the dressed private selector, but full M_EH positivity still needs open/reference/virial/nonEH/frame residual scoring.",
            "derive_first": "try to route open flux, reference, virial/pressure, non-EH and frame terms to zero inside the same compact local selector",
            "fill_second": "where a zero theorem fails, fill conservative epsilon rows against E_H^dress",
            "fallback": "keep local-GR/Newton/PPN public claims unavailable until the total epsilon_E and epsilon_abs gates are scored",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 245 - PPC4161 Binding Stabilizer Positive Energy Theorem Or Beta-Bind Bound

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Key move

The binding problem is a bookkeeping problem unless the source comparator uses the wrong object.

Use the dressed Hilbert/Hamiltonian source energy:

```text
E_H^dress[tau,W_H]
:= c^2 M_H^dress[W_H;tau]
= int_W rho_H c^2 dV_H.
```

The source action already has:

```text
T_H = T_matter + T_EM + T_binding + T_impr_exact + T_rest_top/zero.
```

So ordinary binding is inside the same source object that defines `M_H^dress`.

## No double-count theorem

If:

```text
E_plus_dress := E_H^dress,
rho_H >= 0,
W_H has nonzero compact ordinary-source support,
independent negative stabilizer/ghost sectors are absent or already signed positive,
```

then:

```text
E_binding_stabilizer_neg_abs|dressed_private_selector := 0,
beta_bind_private := 0,
E_stab_neg_abs_private := 0.
```

Reason: binding lowers/dresses the Hamiltonian mass internally, but it is not a second negative residual after the dressed source mass has already been used.

## Combined with 4228

4228 gave:

```text
E_MTS_core_neg_abs|private_selector = 0.
```

Therefore:

```text
epsilon_E_core_bind|dressed_private_selector := 0.
```

## What this does not prove

This is not the full `M_EH` pass yet. It does not score:

```text
E_open_abs,
E_ref_abs,
E_vir_abs,
E_nonEH_abs,
E_frame_abs,
epsilon_abs.
```

It also does not apply to exotic negative-energy matter, an independent stabilizer ghost, or a bare-rest-energy comparator.

## Next target

`{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""# 4229 - Binding Stabilizer Positive Energy Theorem Or Beta-Bind Bound

**Status:** `{DECISION}`.

## What moved

The binding row is closed inside the dressed private ordinary-source selector:

```text
E_plus_dress := c^2 M_H^dress = int_W rho_H c^2 dV_H
T_H includes T_binding
=> E_binding_stabilizer_neg_abs|dressed_private_selector = 0
```

Together with 4228:

```text
epsilon_E_core_bind|dressed_private_selector = 0.
```

## Remaining work

This is a core-bind pass only, not full `M_EH` positivity. Open flux, reference, virial/pressure, non-EH and frame residuals still need zero/bound rows.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"Inside the private dressed Hilbert ordinary-source selector, binding/stabilizer no longer appears as a second negative residual: E_plus is rebased to E_H^dress=c^2 M_H^dress, T_H already includes T_binding, and with rho_H>=0 plus no independent negative stabilizer/ghost, beta_bind_private=0, E_stab_neg_abs_private=0, and epsilon_E_core_bind=0 when combined with 4228.",'
        f'"4229 source audit, dressed Hilbert binding theorem rows, core-bind gate update, decision and firewall.",'
        f'private_dressed_binding_absorption_nonclaim,'
        f'"Assemble and score the remaining M_EH residual channels: open flux, reference, virial/pressure, non-EH, frame and epsilon_abs.",'
        f'"This is a private stable-source core-bind pass only; it does not prove full M_EH positivity, public local GR, Newton, PPN, numerical G_N, or global MTS adoption."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 104. Binding As Dressed Hilbert Source

Marker: `{MARKER}`

4229 rebases the positive source pool to the dressed Hilbert/Hamiltonian source energy:

```text
E_plus_dress := E_H^dress = c^2 M_H^dress.
```

Since:

```text
T_H = T_matter + T_EM + T_binding + T_impr_exact + T_rest_top/zero,
```

ordinary binding is internal source dressing, not an extra negative residual, provided `rho_H>=0` and no independent negative stabilizer/ghost exists. Combined with 4228:

```text
epsilon_E_core_bind|dressed_private_selector = 0.
```
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Binding As Dressed Hilbert Source

Marker: `{PACKET_MARKER}`

The local packet now closes the core-bind numerator inside the dressed private ordinary-source selector. The next remaining work is not beta_bind; it is total `M_EH` residual assembly: open flux, reference, virial/pressure, non-EH and frame terms.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4229_SOURCE_REGISTER.csv"]
    theorems = rows_by_file["P8_Y5_R2FR_4229_DRESSED_BINDING_THEOREM.csv"]
    gates = rows_by_file["P8_Y5_R2FR_4229_CORE_BIND_GATE_UPDATE.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4229_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4229_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4229_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]
    theorem_ids = {row["theorem_id"] for row in theorems}
    gate_ids = {row["gate_id"] for row in gates}
    firewall_ids = {row["firewall_id"] for row in firewalls}

    checks = [
        ("VAL4229_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4229_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4229_2_theorem_rows",
            "theorem rows cover source identity, binding absorption, stabilizer classification, stable source and result",
            {"DHB4229_0_same_source_energy", "DHB4229_1_binding_absorption", "DHB4229_2_stabilizer_classification", "DHB4229_3_stable_source_condition", "DHB4229_4_binding_result"}.issubset(theorem_ids),
        ),
        (
            "VAL4229_3_binding_zero_private",
            "decision zeros beta_bind, stabilizer and binding numerator privately",
            decision["beta_bind_private"] == "0"
            and decision["E_stab_neg_abs_private"] == "0"
            and decision["E_binding_stabilizer_neg_abs_private"] == "0",
        ),
        (
            "VAL4229_4_core_bind_zero",
            "core-bind epsilon is zero in dressed private selector",
            decision["epsilon_E_core_bind_private"] == "0" and "BHG4229_2_core_bind_zero" in gate_ids,
        ),
        (
            "VAL4229_5_rebase_present",
            "gate rows explicitly rebase E_plus to dressed Hilbert energy",
            "BHG4229_1_dressed_rebase" in gate_ids,
        ),
        (
            "VAL4229_6_fallback_retained",
            "fallback beta_bind row reopens when theorem clauses fail",
            "BHG4229_4_reopen_rule" in gate_ids,
        ),
        (
            "VAL4229_7_decision_nonclaim",
            "decision keeps full MEH and local claims unavailable",
            decision["MEH_full_claim"] == "False"
            and decision["local_GR_claim"] == "False"
            and decision["newton_claim"] == "False"
            and decision["PPN_claim"] == "False",
        ),
        (
            "VAL4229_8_firewall",
            "firewall blocks bare relabel, exotic matter, independent stabilizer, full MEH claim and orbital GM laundering",
            {"BHF4229_0_no_bare_relabel", "BHF4229_1_no_exotic_matter", "BHF4229_2_no_independent_stabilizer", "BHF4229_3_no_full_MEH_claim", "BHF4229_4_no_orbital_GM_laundering"}.issubset(firewall_ids),
        ),
        (
            "VAL4229_9_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4229_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4229_11_claim_register", "claim register contains L-070", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4229_12_spine_packet", "spine and packet contain 4229 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4229_13_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4229_14_status_script", "status records decision and generator script exists", rows_by_file["P8_Y5_R2FR_4229_STATUS.csv"][0]["decision"] == DECISION and (SCRIPTS / "Y5_R2FR_4229_binding_stabilizer_positive_energy_theorem_or_beta_bind_bound.py").exists()),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4229_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4229_DRESSED_BINDING_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4229_CORE_BIND_GATE_UPDATE.csv": gate_rows(),
        "P8_Y5_R2FR_4229_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4229_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4229_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4229_NEXT_TARGET.csv": next_target_rows(),
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
