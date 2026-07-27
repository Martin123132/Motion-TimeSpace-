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

CHECKPOINT = "4227"
CLAIM_ID = "L-068"
BRANCH = "MTS_R2FR_Y5_CORE_SIGNATURE_BINDING_BOUND_4227"
DECISION = "CORE_SIGNATURE_MISMATCH_CONDITIONAL_ZERO_FROM_LOCAL_PARENT_SIGNATURE_BINDING_BOUND_SCHEMA_RETAINED_NONCLAIM"
MARKER = "PPC4161_CORE_SIGNATURE_BINDING_BOUND_4227"
PACKET_MARKER = "PPC4161_PACKET_CORE_SIGNATURE_BINDING_BOUND_4227"
NEXT_TARGET = "4228-Y5-R2FR-core-signature-clause-adoption-or-beta-sig-bound-fill.md"

FORMAL_PATH = FORMAL / "243-PPC4161-core-signature-mismatch-and-binding-bound-row.md"
DOC_PATH = POST / "4227-Y5-R2FR-core-signature-mismatch-and-binding-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4227_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4227_00_4226_next": SourceSpec(
        "SRC4227_00_4226_next",
        SOURCE_DIR / "P8_Y5_R2FR_4226_NEXT_TARGET.csv",
        "4227-Y5-R2FR-core-signature-mismatch-and-binding-bound-row.md",
        "4226 selects the core signature mismatch and binding/stabilizer bound as the next local sign target.",
    ),
    "SRC4227_01_242_formal": SourceSpec(
        "SRC4227_01_242_formal",
        FORMAL / "242-PPC4161-gamma-bath-energy-balance-source-row-or-boundary-branch-adoption.md",
        "epsilon_E_core_bind",
        "Formal 4226 statement of the remaining local energy-sign denominator.",
    ),
    "SRC4227_02_3924_signature": SourceSpec(
        "SRC4227_02_3924_signature",
        SOURCE_DIR / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv",
        "CLA3924_6_Y",
        "Minimal parent signature clause: quadratic/coercive residual fibre and no visible-linear hidden terms if adopted.",
    ),
    "SRC4227_03_3949_matrix": SourceSpec(
        "SRC4227_03_3949_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_3949_MTS_HAMILTONIAN_SIGNATURE_MATRIX.csv",
        "SIG3949_7_matter_binding",
        "Energy-sector matrix identifying matter/binding/stabilizer as a concrete epsilon row requirement.",
    ),
    "SRC4227_04_3950_aux": SourceSpec(
        "SRC4227_04_3950_aux",
        SOURCE_DIR / "P8_Y5_R2FR_3950_GK_POSITIVE_AUXILIARY_SIGNATURE.csv",
        "GKS3950_0_parent_density",
        "Positive auxiliary signature candidate for Gamma/K-hat style residual sectors.",
    ),
    "SRC4227_05_185_hilbert_source": SourceSpec(
        "SRC4227_05_185_hilbert_source",
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H = T_matter + T_EM + T_binding",
        "Hilbert-source decomposition keeping binding in the total source ledger.",
    ),
    "SRC4227_06_2616_exchange_graph": SourceSpec(
        "SRC4227_06_2616_exchange_graph",
        SOURCE_DIR / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv",
        "SMG2616_3_macroscopic_body_edge",
        "Private standard-matter graph saying macroscopic bodies inherit binding/lattice stress.",
    ),
    "SRC4227_07_4223_binding": SourceSpec(
        "SRC4227_07_4223_binding",
        SOURCE_DIR / "P8_Y5_R2FR_4223_BINDING_BOUND.csv",
        "BBS4223_1_negative_binding_fraction",
        "Earlier binding/stabilizer negative-energy fraction schema.",
    ),
    "SRC4227_08_4222_matrix": SourceSpec(
        "SRC4227_08_4222_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_4222_SIGNATURE_MATRIX.csv",
        "PES4222_4_binding_stabilizer",
        "Earlier signature-matrix row isolating binding/stabilizer as unsigned.",
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


def signature_theorem_rows() -> List[Dict[str, str]]:
    data = [
        (
            "SMT4227_0_decomposition",
            "signature mismatch decomposition",
            "E_signature_mismatch_abs <= E_field_metric_neg_abs + E_visible_linear_hidden_abs + E_projection_readout_abs + E_boundary_unsilenced_abs",
            "After lambda and gamma are handled, the remaining local MTS-core negative channel is exactly the part of the parent local action not yet proven to descend as a nonnegative quadratic hidden/residual sector.",
            "DERIVED_DECOMPOSITION_PRIVATE",
        ),
        (
            "SMT4227_1_conditional_zero",
            "conditional zero law",
            "if G_AB >= 0, M_AB >= m_gap^2 > 0 off gauge directions, S_int = O(|Z|^2), Dq/measure/coframe/connection descend, and boundary/readout terms are source-silent, then E_signature_mismatch_abs := 0",
            "Quadratic/coercive hidden fields have vanishing first variation at Z=0 and no visible-linear hidden stress; descended measure/coframe/connection terms prevent representative-dependent stress; fixed/source-silent boundary terms do not enter the local Hilbert source.",
            "CONDITIONAL_ZERO_PROOF_CONTRACT",
        ),
        (
            "SMT4227_2_unsigned_cost",
            "adoption cost",
            "signature_clause_adopted := false until parent local action signs every clause",
            "The corpus has a candidate parent signature clause and positive auxiliary form, but both are currently private candidates with valid_for_claim=false.",
            "NONCLAIM_UNTIL_PARENT_SIGNED",
        ),
        (
            "SMT4227_3_fallback_bound",
            "fallback beta law",
            "E_signature_mismatch_abs <= beta_sig E_plus_min, beta_sig := (E_field_metric_neg_abs + E_visible_linear_hidden_abs + E_projection_readout_abs + E_boundary_unsilenced_abs)/E_plus_min",
            "If the zero law is not adopted, the local branch can still survive by sourcing a conservative beta_sig bound instead of pretending the mismatch vanishes.",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
        ),
        (
            "SMT4227_4_score_rule",
            "score rule",
            "signature_score := 0 if SMT4227_1 is parent-signed else beta_sig source row required",
            "This prevents the proof from cycling: either sign the parent metric/descent clauses or fill an explicit conservative bound.",
            "NEXT_GATE_DEFINED",
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


def binding_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "BBR4227_0_binding_law",
            "binding/stabilizer negative contribution",
            "E_binding_stabilizer_neg_abs <= beta_bind E_visible_rest + E_stab_neg_abs",
            "Binding is part of the total Hilbert source, but the current corpus only gives a ledger relation, not a sourced lower-bound coefficient.",
            "BOUND_SCHEMA_RETAINED",
        ),
        (
            "BBR4227_1_beta_bind",
            "binding fraction coefficient",
            "0 <= beta_bind < 1 required for a useful comparator pass",
            "beta_bind must come from a material/EFT/virial/source-bound row; it cannot be set by hand.",
            "VALUE_MISSING_SOURCE_REQUIRED",
        ),
        (
            "BBR4227_2_stabilizer_floor",
            "absolute stabilizer floor",
            "E_stab_neg_abs >= 0 with source-backed upper contribution E_stab_neg_abs/E_plus_min required",
            "Any stabilizer sector not included in ordinary visible rest energy needs its own nonnegative or bounded-below source certificate.",
            "VALUE_MISSING_SOURCE_REQUIRED",
        ),
        (
            "BBR4227_3_source_link",
            "Hilbert-source binding link",
            "T_H includes T_binding and macroscopic bodies inherit EM/nuclear/lattice binding stress",
            "This proves the right place to count binding, but not the numerical bound needed to pass M_EH.",
            "LEDGER_LINK_ONLY",
        ),
        (
            "BBR4227_4_no_zero_shortcut",
            "no binding magic zero",
            "beta_bind := 0 is forbidden unless a closed-system source theorem proves the binding contribution is nonnegative in the chosen comparator",
            "Unlike the signature mismatch, binding has real negative rest-energy bookkeeping in ordinary systems; it must be bounded, not wished away.",
            "FIREWALL_RULE",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, piece, formula, derivation, status in data
    ]


def epsilon_gate_rows() -> List[Dict[str, str]]:
    data = [
        (
            "ECG4227_0_core_gate",
            "core plus binding gate",
            "epsilon_E_core_bind := (E_binding_stabilizer_neg_abs + E_signature_mismatch_abs)/E_plus_min",
            "This is the remaining 4226 local sign denominator after lambda and boundary-gamma are handled.",
            "ACTIVE_GATE_UNSCORED",
        ),
        (
            "ECG4227_1_substitution",
            "fallback substitution",
            "epsilon_E_core_bind <= beta_sig + (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min",
            "Substitute SMT4227_3 and BBR4227_0 to get a source-fillable inequality.",
            "DERIVED_BOUND_SCHEMA",
        ),
        (
            "ECG4227_2_signature_zero_branch",
            "conditional signature-zero branch",
            "if SMT4227_1 is parent-signed, epsilon_E_core_bind <= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min",
            "This is the cleanest branch: parent signature/descent removes the residual MTS-core sign mismatch, leaving binding/stabilizer only.",
            "CONDITIONAL_REDUCTION_NONCLAIM",
        ),
        (
            "ECG4227_3_pass_rule",
            "MEH sign pass rule",
            "M_EH sign gate may score only if E_plus_min > 0 and epsilon_E_core_bind < 1 with sourced rows",
            "The comparator remains unavailable until every numerator and denominator row is numeric/source-backed.",
            "PASS_RULE_DEFINED_UNFILLED",
        ),
        (
            "ECG4227_4_block_rule",
            "block rule",
            "if signature_clause_adopted=false and beta_sig missing, or beta_bind/E_stab_neg_abs missing, local-GR/Newton/PPN claims remain blocked",
            "No branch is allowed to treat a private signature candidate or placeholder binding coefficient as evidence.",
            "CLAIM_BLOCK_ACTIVE",
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
            "signature_conditional_zero_built": "True",
            "signature_parent_signed": "False",
            "beta_sig_filled": "False",
            "binding_bound_schema_ready": "True",
            "beta_bind_filled": "False",
            "E_stab_neg_abs_filled": "False",
            "MEH_claim": "False",
            "local_GR_claim": "False",
            "newton_claim": "False",
            "summary": "4227 derives the conditional zero contract for E_signature_mismatch_abs and the fallback beta_sig law, while retaining the binding/stabilizer beta-bound as a sourced-input requirement.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        (
            "CBF4227_0_no_parent_signature_claim",
            "Do not set E_signature_mismatch_abs=0 from candidate rows alone.",
            "BLOCKED",
            "The parent local action signature/descent clauses are not signed as claim-grade inputs.",
        ),
        (
            "CBF4227_1_no_beta_fabrication",
            "Do not invent beta_sig, beta_bind or E_stab_neg_abs numeric values.",
            "BLOCKED",
            "A comparator pass needs sourced numbers or a closed theorem, not placeholders.",
        ),
        (
            "CBF4227_2_no_binding_zero",
            "Do not set beta_bind=0 unless a source theorem proves binding nonnegative in the comparator.",
            "BLOCKED",
            "Binding energy bookkeeping is physical and must be bounded carefully.",
        ),
        (
            "CBF4227_3_no_MEH_claim",
            "Do not claim M_EH positivity from this packet.",
            "BLOCKED",
            "The denominator gate is only reduced, not scored.",
        ),
        (
            "CBF4227_4_no_local_GR_Newton_PPN_claim",
            "Do not claim local GR/Newton/PPN from the conditional zero contract.",
            "BLOCKED",
            "Local dynamics still require sourced comparator rows and residual-vector gates.",
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
            "status_id": "CBS4227_STATUS",
            "decision": DECISION,
            "summary": "Signature mismatch has a real conditional-zero theorem contract; binding/stabilizer remains the live source-bound input before any M_EH/local-GR score.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4227 turns E_signature_mismatch_abs into either a parent-signed zero theorem or a beta_sig source row; binding still needs beta_bind/E_stab_neg_abs inputs.",
            "derive_first": "attempt to adopt/sign the local parent signature/descent clause so beta_sig=0 without handwaving",
            "fill_second": "if adoption fails, fill a conservative beta_sig row and then attack beta_bind/E_stab_neg_abs",
            "fallback": "keep M_EH, local-GR, Newton and PPN unavailable until epsilon_E_core_bind is numeric and <1",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 243 - PPC4161 Core Signature Mismatch And Binding Bound Row

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4226 left:

```text
epsilon_E_core_bind
= (E_binding_stabilizer_neg_abs + E_signature_mismatch_abs)/E_plus_min.
```

4227 splits that into two different animals:

```text
E_signature_mismatch_abs
<= E_field_metric_neg_abs
 + E_visible_linear_hidden_abs
 + E_projection_readout_abs
 + E_boundary_unsilenced_abs.
```

and:

```text
E_binding_stabilizer_neg_abs
<= beta_bind E_visible_rest + E_stab_neg_abs.
```

## Conditional zero theorem for the signature mismatch

The signature mismatch is not an empirical fudge term. It has a clean zero route:

```text
if G_AB >= 0,
   M_AB >= m_gap^2 > 0 off gauge directions,
   S_int = O(|Z|^2) with no visible-linear hidden terms,
   Dq, measure, coframe and connection descend,
   boundary/readout terms are source-silent,
then E_signature_mismatch_abs := 0.
```

Reason: the hidden/residual fields are quadratic/coercive at the local branch surface, so their first variation vanishes at `Z=0`; descended geometric data prevents representative-dependent stress; fixed/source-silent boundary terms do not enter the local Hilbert source.

## Cost

The current corpus has candidate rows for this route, not a signed parent theorem. Therefore:

```text
signature_clause_adopted := false
signature_score := beta_sig unless the parent clause is signed
```

where:

```text
E_signature_mismatch_abs <= beta_sig E_plus_min.
```

## Binding/stabilizer branch

Binding is different. It is real source bookkeeping, so the safe law is:

```text
E_binding_stabilizer_neg_abs
<= beta_bind E_visible_rest + E_stab_neg_abs.
```

No binding-zero shortcut is allowed unless a closed source theorem proves that shortcut in the chosen comparator.

## Updated gate

```text
epsilon_E_core_bind
<= beta_sig + (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min.
```

On the parent-signed signature branch:

```text
epsilon_E_core_bind
<= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min.
```

`M_EH`, local GR, Newton and PPN remain unavailable until the rows are signed or sourced and `epsilon_E_core_bind < 1`.

## Next target

`{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""# 4227 - Core Signature Mismatch And Binding Bound Row

**Status:** `{DECISION}`.

## What moved

The core signature mismatch now has a real derivation route:

```text
parent positive/coercive field-space metric
+ no visible-linear hidden terms
+ descended measure/coframe/connection
+ source-silent boundary/readout
=> E_signature_mismatch_abs = 0.
```

But the parent clause is not yet claim-signed, so this remains a private conditional theorem contract.

## Remaining live bound

```text
E_binding_stabilizer_neg_abs <= beta_bind E_visible_rest + E_stab_neg_abs.
```

The useful combined gate is:

```text
epsilon_E_core_bind
<= beta_sig + (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min.
```

## Hard rule

No `M_EH`, local-GR, Newton or PPN claim follows from 4227. The next move is to sign the parent signature clause or fill `beta_sig`, then source `beta_bind` and `E_stab_neg_abs`.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The remaining MTS-core signature mismatch is reduced to a conditional zero theorem: if the parent local field-space metric is positive/coercive, hidden/residual couplings have no visible-linear terms, geometric data descend, and boundary/readout terms are source-silent, then E_signature_mismatch_abs=0; otherwise a beta_sig bound is required. Binding/stabilizer remains bounded by beta_bind E_visible_rest + E_stab_neg_abs.",'
        f'"4227 source audit, signature mismatch theorem rows, binding bound rows, epsilon gate, decision and firewall.",'
        f'private_core_signature_binding_bound_nonclaim,'
        f'"Sign/adopt the parent local signature/descent clause or fill beta_sig; then source beta_bind and E_stab_neg_abs.",'
        f'"This is a conditional theorem contract and bound schema only; it does not prove M_EH positivity, local GR, Newton or PPN."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 102. Core Signature Mismatch And Binding Bound

Marker: `{MARKER}`

4227 reduces the local sign gap to:

```text
E_signature_mismatch_abs <= beta_sig E_plus_min
E_binding_stabilizer_neg_abs <= beta_bind E_visible_rest + E_stab_neg_abs
```

with a conditional zero theorem for the first row:

```text
positive/coercive parent field-space metric
+ no visible-linear hidden terms
+ descended geometric data
+ source-silent boundary/readout
=> E_signature_mismatch_abs = 0.
```

The route is not claim-signed yet. The binding/stabilizer row still needs sourced coefficients.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Core Signature And Binding Bound

Marker: `{PACKET_MARKER}`

The local packet now has a conditional theorem route for `E_signature_mismatch_abs=0`, plus a fallback `beta_sig` row. Binding/stabilizer is not zeroed; it remains a sourced `beta_bind` and `E_stab_neg_abs` bound before any `M_EH` score.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4227_SOURCE_REGISTER.csv"]
    theorems = rows_by_file["P8_Y5_R2FR_4227_SIGNATURE_MISMATCH_THEOREM.csv"]
    bindings = rows_by_file["P8_Y5_R2FR_4227_BINDING_BOUND_ROW.csv"]
    gates = rows_by_file["P8_Y5_R2FR_4227_EPSILON_CORE_BIND_GATE.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4227_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4227_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4227_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]
    theorem_ids = {row["theorem_id"] for row in theorems}
    binding_ids = {row["bound_id"] for row in bindings}
    gate_ids = {row["gate_id"] for row in gates}
    firewall_ids = {row["firewall_id"] for row in firewalls}

    checks = [
        ("VAL4227_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4227_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4227_2_signature_theorem",
            "signature theorem includes decomposition, conditional zero, unsigned cost, fallback bound and score rule",
            {"SMT4227_0_decomposition", "SMT4227_1_conditional_zero", "SMT4227_2_unsigned_cost", "SMT4227_3_fallback_bound", "SMT4227_4_score_rule"}.issubset(theorem_ids),
        ),
        (
            "VAL4227_3_zero_is_conditional",
            "zero row is explicitly conditional and parent-signed false",
            any(row["theorem_id"] == "SMT4227_1_conditional_zero" and "E_signature_mismatch_abs := 0" in row["formula_or_statement"] for row in theorems)
            and decision["signature_parent_signed"] == "False",
        ),
        (
            "VAL4227_4_binding_bound",
            "binding rows include beta law, missing beta, missing stabilizer and no-zero firewall",
            {"BBR4227_0_binding_law", "BBR4227_1_beta_bind", "BBR4227_2_stabilizer_floor", "BBR4227_4_no_zero_shortcut"}.issubset(binding_ids),
        ),
        (
            "VAL4227_5_epsilon_gate",
            "epsilon gate contains fallback substitution and pass/block rules",
            {"ECG4227_0_core_gate", "ECG4227_1_substitution", "ECG4227_3_pass_rule", "ECG4227_4_block_rule"}.issubset(gate_ids),
        ),
        (
            "VAL4227_6_decision_nonclaim",
            "decision builds theorem contract but keeps all claims unavailable",
            decision["signature_conditional_zero_built"] == "True"
            and decision["MEH_claim"] == "False"
            and decision["local_GR_claim"] == "False"
            and decision["newton_claim"] == "False",
        ),
        (
            "VAL4227_7_firewall",
            "firewall blocks unsigned signature, fabricated beta rows, binding zero, MEH and local claims",
            {"CBF4227_0_no_parent_signature_claim", "CBF4227_1_no_beta_fabrication", "CBF4227_2_no_binding_zero", "CBF4227_3_no_MEH_claim", "CBF4227_4_no_local_GR_Newton_PPN_claim"}.issubset(firewall_ids),
        ),
        (
            "VAL4227_8_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4227_9_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4227_10_claim_register", "claim register contains L-068", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4227_11_spine_packet", "spine and packet contain 4227 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4227_12_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4227_13_script_exists", "generator script exists", (SCRIPTS / "Y5_R2FR_4227_core_signature_mismatch_and_binding_bound_row.py").exists()),
        (
            "VAL4227_14_status",
            "status records conditional-zero theorem and live binding bound",
            rows_by_file["P8_Y5_R2FR_4227_STATUS.csv"][0]["decision"] == DECISION,
        ),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4227_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4227_SIGNATURE_MISMATCH_THEOREM.csv": signature_theorem_rows(),
        "P8_Y5_R2FR_4227_BINDING_BOUND_ROW.csv": binding_bound_rows(),
        "P8_Y5_R2FR_4227_EPSILON_CORE_BIND_GATE.csv": epsilon_gate_rows(),
        "P8_Y5_R2FR_4227_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4227_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4227_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4227_NEXT_TARGET.csv": next_target_rows(),
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
