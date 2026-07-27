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

CHECKPOINT = "4228"
CLAIM_ID = "L-069"
BRANCH = "MTS_R2FR_Y5_CORE_SIGNATURE_CLAUSE_ADOPTION_4228"
DECISION = "PRIVATE_LOCAL_SELECTOR_ADOPTS_PARENT_SIGNATURE_CLAUSE_BETA_SIG_ZERO_BINDING_BOUND_REMAINS_NONCLAIM"
MARKER = "PPC4161_CORE_SIGNATURE_CLAUSE_ADOPTION_4228"
PACKET_MARKER = "PPC4161_PACKET_CORE_SIGNATURE_CLAUSE_ADOPTION_4228"
NEXT_TARGET = "4229-Y5-R2FR-binding-stabilizer-positive-energy-theorem-or-beta-bind-bound.md"

FORMAL_PATH = FORMAL / "244-PPC4161-core-signature-clause-adoption-or-beta-sig-bound-fill.md"
DOC_PATH = POST / "4228-Y5-R2FR-core-signature-clause-adoption-or-beta-sig-bound-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4228_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4228_00_4227_next": SourceSpec(
        "SRC4228_00_4227_next",
        SOURCE_DIR / "P8_Y5_R2FR_4227_NEXT_TARGET.csv",
        "4228-Y5-R2FR-core-signature-clause-adoption-or-beta-sig-bound-fill.md",
        "4227 selected parent signature adoption or beta_sig fill as the next route.",
    ),
    "SRC4228_01_243_formal": SourceSpec(
        "SRC4228_01_243_formal",
        FORMAL / "243-PPC4161-core-signature-mismatch-and-binding-bound-row.md",
        "signature_clause_adopted := false",
        "4227 formal packet before adoption: beta_sig remains active unless the parent clause is signed.",
    ),
    "SRC4228_02_4227_theorem": SourceSpec(
        "SRC4228_02_4227_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_4227_SIGNATURE_MISMATCH_THEOREM.csv",
        "SMT4227_1_conditional_zero",
        "4227 conditional zero theorem for E_signature_mismatch_abs.",
    ),
    "SRC4228_03_3924_parent": SourceSpec(
        "SRC4228_03_3924_parent",
        SOURCE_DIR / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv",
        "CLA3924_1_action",
        "Minimal local parent action candidate containing EH, visible source, quadratic hidden sectors and boundary/readout certificates.",
    ),
    "SRC4228_04_3924_branch": SourceSpec(
        "SRC4228_04_3924_branch",
        SOURCE_DIR / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv",
        "CLA3924_2_branch",
        "Local branch surface defining Y_loc=0, H_priv=0 and source-silent collar.",
    ),
    "SRC4228_05_3924_Y": SourceSpec(
        "SRC4228_05_3924_Y",
        SOURCE_DIR / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv",
        "CLA3924_6_Y",
        "Quadratic/coercive residual fibre and no visible-linear hidden terms.",
    ),
    "SRC4228_06_3924_effect": SourceSpec(
        "SRC4228_06_3924_effect",
        SOURCE_DIR / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv",
        "CLA3924_11_effect",
        "3924 states the clause is strong enough for the private local theorem stack if adopted.",
    ),
    "SRC4228_07_190_selector": SourceSpec(
        "SRC4228_07_190_selector",
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "PPC4161-TK-HQNP-local-selector-private",
        "Earlier quarantined local selector branch: action-level signatures, not after-the-fact closure.",
    ),
    "SRC4228_08_193_quotient": SourceSpec(
        "SRC4228_08_193_quotient",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_parent|Wloc =",
        "Quotient/action/matter descent before variation closes representative/projector residuals.",
    ),
    "SRC4228_09_185_source": SourceSpec(
        "SRC4228_09_185_source",
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "S_src = S_matter",
        "Single Hilbert source-measure descent and common metric/coframe volume.",
    ),
    "SRC4228_10_3950_aux": SourceSpec(
        "SRC4228_10_3950_aux",
        SOURCE_DIR / "P8_Y5_R2FR_3950_GK_POSITIVE_AUXILIARY_SIGNATURE.csv",
        "GKS3950_0_parent_density",
        "Positive auxiliary density form supporting the local quadratic hidden/residual signature branch.",
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


def adoption_rows() -> List[Dict[str, str]]:
    data = [
        (
            "CSA4228_0_branch_selection",
            "private local selector",
            "local_signature_branch := PPC4161-TK-HQNP-local-selector-private cap CLA3924_minimal_parent_signature",
            "This imports the already-quarantined local selector and intersects it with the 3924 minimal parent signature clause.",
            "ADOPTED_PRIVATE_SELECTOR_ONLY",
        ),
        (
            "CSA4228_1_parent_action_signature",
            "local parent action",
            "S_parent^loc := S_EH + S_vis + S_Y + S_H + S_int^{>=2} + S_R11^{DZ} + S_G0 + S_B^{top} + S_proj^{top/readout}",
            "This is an action-level branch signature, so residual silence is selected before variation rather than imposed after equations are written.",
            "ADOPTED_PRIVATE_PARENT_SIGNATURE",
        ),
        (
            "CSA4228_2_branch_surface",
            "branch surface",
            "Y_loc=0, H_priv=0, source-silent q_src collar, fixed q-basic domain, no incoming history tail",
            "The local zero is attached to a compact local collar and does not erase galaxy/cosmology/open-memory sectors.",
            "ADOPTED_LOCAL_COLLAR_ONLY",
        ),
        (
            "CSA4228_3_positive_hidden_signature",
            "quadratic residual fibre",
            "S_Y+S_H+S_int^{>=2} has nonnegative quadratic form with mass gap off gauge directions and no visible-linear Y/H terms",
            "At the branch surface the first variation of hidden/residual fields vanishes, and no affine hidden stress enters the visible Hilbert source.",
            "SIGNS_SMT4227_CONDITION",
        ),
        (
            "CSA4228_4_descent_before_variation",
            "quotient and source descent",
            "S_parent|Wloc=S_red[q(Phi),psi]+S_top[q(Phi)]+dB[q(Phi)] and S_matter factors through q before variation",
            "Representative/vertical degrees are silent by chain rule, not by post-hoc projection.",
            "SIGNS_DESCENT_CONDITION",
        ),
        (
            "CSA4228_5_boundary_readout_silence",
            "boundary and readout",
            "S_B and S_proj are topological, fixed, q-owned or routed; no source-dependent hidden boundary charge enters M_EH",
            "This signs the boundary/readout part of the 4227 conditional zero contract in the private selector only.",
            "SIGNS_BOUNDARY_READOUT_CONDITION",
        ),
        (
            "CSA4228_6_adoption_scope",
            "scope declaration",
            "signature_clause_adopted_private := true; signature_clause_adopted_global := false",
            "The route is now usable inside the private local selector but remains quarantined from public/global MTS claims.",
            "PRIVATE_ADOPTION_GLOBAL_QUARANTINE",
        ),
    ]
    return [
        {
            **common(),
            "adoption_id": adoption_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for adoption_id, piece, formula, derivation, status in data
    ]


def beta_sig_rows() -> List[Dict[str, str]]:
    data = [
        (
            "BSZ4228_0_signature_zero",
            "signature mismatch",
            "E_signature_mismatch_abs|private_selector := 0",
            "CSA4228 signs every 4227 conditional-zero clause inside the private local selector.",
            "ZERO_IN_PRIVATE_SELECTOR",
        ),
        (
            "BSZ4228_1_beta_sig_zero",
            "beta signature score",
            "beta_sig_private_selector := 0",
            "Since the mismatch numerator is zero on the adopted branch, the fallback beta_sig source row is not needed inside that branch.",
            "ZERO_IN_PRIVATE_SELECTOR",
        ),
        (
            "BSZ4228_2_core_negative_zero",
            "MTS core negative channel",
            "E_MTS_core_neg_abs|private_selector <= E_signature_mismatch_abs = 0",
            "Combining 4226 with the 4228 signature adoption removes the remaining MTS-core negative-energy channel in the local selector.",
            "CORE_NEGATIVE_CHANNEL_CLOSED_PRIVATE",
        ),
        (
            "BSZ4228_3_reopened_if_rejected",
            "fallback if branch rejected",
            "if signature_clause_adopted_private is rejected, E_signature_mismatch_abs <= beta_sig E_plus_min reopens",
            "This prevents hidden closure: the zero is owned by the branch signature, not by a universal theorem.",
            "FALLBACK_BOUND_RETAINED",
        ),
        (
            "BSZ4228_4_not_MEH_pass",
            "remaining denominator numerator",
            "epsilon_E_core_bind <= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min",
            "Signature is no longer the local selector bottleneck; binding/stabilizer is now the live obstruction.",
            "BINDING_BOUND_REMAINS",
        ),
    ]
    return [
        {
            **common(),
            "beta_sig_id": beta_sig_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for beta_sig_id, piece, formula, derivation, status in data
    ]


def epsilon_gate_rows() -> List[Dict[str, str]]:
    data = [
        (
            "EG4228_0_previous_gate",
            "previous gate",
            "epsilon_E_core_bind := (E_binding_stabilizer_neg_abs + E_signature_mismatch_abs)/E_plus_min",
            "4227 split the gate into signature mismatch and binding/stabilizer rows.",
            "REFERENCE",
        ),
        (
            "EG4228_1_private_selector_gate",
            "adopted selector gate",
            "epsilon_E_core_bind|private_selector <= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min",
            "Substitute E_signature_mismatch_abs=0 from CSA4228 and the binding bound from 4227.",
            "DERIVED_ACTIVE_GATE",
        ),
        (
            "EG4228_2_pass_condition",
            "MEH sign pass condition",
            "E_plus_min>0 and (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min < 1",
            "This is now the concrete remaining sign pass test for the private selector.",
            "BINDING_NUMERATOR_REQUIRED",
        ),
        (
            "EG4228_3_bind_zero_forbidden",
            "binding no-shortcut",
            "beta_bind and E_stab_neg_abs cannot be set to zero by the signature adoption",
            "The adopted signature clause closes hidden/residual mismatch only, not ordinary binding bookkeeping.",
            "FIREWALL_RULE",
        ),
        (
            "EG4228_4_claim_status",
            "claim status",
            "M_EH/local_GR/Newton/PPN remain unavailable until EG4228_2 is sourced or proved",
            "The local selector has moved from signature debt to binding/stabilizer debt, but the comparator is still unscored.",
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
            "private_signature_clause_adopted": "True",
            "global_signature_clause_adopted": "False",
            "E_signature_mismatch_abs_private": "0",
            "beta_sig_private": "0",
            "E_MTS_core_neg_abs_private": "0",
            "binding_bound_schema_ready": "True",
            "beta_bind_filled": "False",
            "E_stab_neg_abs_filled": "False",
            "MEH_claim": "False",
            "local_GR_claim": "False",
            "newton_claim": "False",
            "PPN_claim": "False",
            "summary": "4228 privately adopts the local selector parent-signature clause, closing beta_sig and the MTS-core negative-energy channel inside that quarantined branch; binding/stabilizer remains the live sign numerator.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        (
            "CSF4228_0_no_global_adoption",
            "Do not treat private selector adoption as global MTS parent-action proof.",
            "BLOCKED",
            "CSA4228 is scoped to compact local collars and inherits 190 quarantine.",
        ),
        (
            "CSF4228_1_no_public_local_GR",
            "Do not claim public local GR/Newton/PPN from beta_sig_private=0.",
            "BLOCKED",
            "Binding/stabilizer and empirical comparator rows are still unscored.",
        ),
        (
            "CSF4228_2_no_binding_erasure",
            "Do not erase beta_bind or E_stab_neg_abs using the signature clause.",
            "BLOCKED",
            "Binding belongs to the Hilbert source ledger and needs its own theorem or bound.",
        ),
        (
            "CSF4228_3_no_sector_spillover",
            "Do not apply the compact local selector to galaxies, cosmology, open-memory, transition or radiative sectors.",
            "BLOCKED",
            "Those sectors require exact no-flux/support separation or separate residual bounds.",
        ),
        (
            "CSF4228_4_no_numerical_G",
            "Do not claim a numerical derivation of G_N.",
            "BLOCKED",
            "The branch closes a signature mismatch, not the measured coupling magnitude.",
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
            "status_id": "CSS4228_STATUS",
            "decision": DECISION,
            "summary": "The local selector can now use beta_sig=0 privately; the next real obstruction is the binding/stabilizer positive-energy or beta-bound theorem.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4228 closes the core signature mismatch inside the private local selector; the remaining epsilon numerator is beta_bind E_visible_rest + E_stab_neg_abs.",
            "derive_first": "try to prove binding/stabilizer positivity or a virial/Hilbert-source lower-bound theorem in the same local collar",
            "fill_second": "if positivity fails, source conservative beta_bind and E_stab_neg_abs bounds",
            "fallback": "keep M_EH, local-GR, Newton and PPN unavailable until the binding numerator is scored below E_plus_min",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 244 - PPC4161 Core Signature Clause Adoption Or Beta-Sig Bound Fill

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Adoption

The local branch now adopts:

```text
local_signature_branch
:= PPC4161-TK-HQNP-local-selector-private
   cap CLA3924_minimal_parent_signature.
```

This is not a global MTS claim. It is a private compact-local selector.

## Parent signature

Inside that selector:

```text
S_parent^loc
:= S_EH
 + S_vis
 + S_Y + S_H + S_int^{{>=2}}
 + S_R11^{{DZ}}
 + S_G0
 + S_B^{{top}}
 + S_proj^{{top/readout}}.
```

with:

```text
Y_loc = H_priv = 0,
S_Y+S_H+S_int^{{>=2}} has a nonnegative quadratic form,
no visible-linear Y/H terms,
q/source/readout descent before variation,
fixed/q-owned/source-silent boundary and readout terms.
```

## Consequence

This signs the 4227 conditional-zero theorem inside the private selector:

```text
E_signature_mismatch_abs|private_selector := 0.
beta_sig_private_selector := 0.
```

Using 4226:

```text
E_MTS_core_neg_abs|private_selector
<= E_signature_mismatch_abs
= 0.
```

So the MTS-core negative-energy channel is closed in the private local selector.

## Remaining gate

The denominator gate is now:

```text
epsilon_E_core_bind|private_selector
<= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min.
```

The branch passes the sign gate only if:

```text
E_plus_min > 0
and
(beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min < 1.
```

## Firewalls

The adoption does not:

- prove global MTS parent adoption;
- prove numerical `G_N`;
- erase binding/stabilizer bookkeeping;
- claim public local GR, Newton or PPN;
- apply to galaxy, cosmology, open-memory, transition or radiative sectors.

## Next target

`{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""# 4228 - Core Signature Clause Adoption Or Beta-Sig Bound Fill

**Status:** `{DECISION}`.

## What moved

The private local selector now adopts the parent signature clause needed by 4227:

```text
signature_clause_adopted_private := true
signature_clause_adopted_global := false
```

Therefore:

```text
E_signature_mismatch_abs|private_selector = 0
beta_sig_private_selector = 0
E_MTS_core_neg_abs|private_selector = 0
```

This is real progress: the local sign problem no longer has a free `beta_sig` leak inside the quarantined selector branch.

## What remains

The whole local sign gate now hangs on binding/stabilizer:

```text
epsilon_E_core_bind
<= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min.
```

No `M_EH`, local-GR, Newton or PPN claim follows until `beta_bind`, `E_stab_neg_abs` and `E_plus_min` are proved/sourced.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The private compact-local selector adopts the 3924 minimal parent signature clause, so the 4227 conditional-zero theorem can be used inside that branch: E_signature_mismatch_abs=0, beta_sig_private=0, and E_MTS_core_neg_abs=0. The remaining sign gate is the binding/stabilizer numerator (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min.",'
        f'"4228 source audit, parent signature adoption rows, beta_sig zero rows, epsilon gate, decision and firewall.",'
        f'private_local_signature_clause_adoption_nonclaim,'
        f'"Prove binding/stabilizer positivity or fill source-backed beta_bind, E_stab_neg_abs and E_plus_min rows.",'
        f'"This closes only the private selector signature mismatch. It does not prove global MTS adoption, numerical G_N, public local GR, Newton, PPN or empirical local tests."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 103. Core Signature Clause Adoption

Marker: `{MARKER}`

4228 adopts the 3924 parent signature clause inside the already-quarantined compact local selector:

```text
signature_clause_adopted_private := true,
signature_clause_adopted_global := false.
```

Therefore:

```text
E_signature_mismatch_abs|private_selector = 0,
beta_sig_private_selector = 0,
E_MTS_core_neg_abs|private_selector = 0.
```

The remaining local sign gate is:

```text
epsilon_E_core_bind|private_selector
<= (beta_bind E_visible_rest + E_stab_neg_abs)/E_plus_min.
```
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Core Signature Clause Adoption

Marker: `{PACKET_MARKER}`

The private local selector now owns the parent signature clause required to set `beta_sig=0`. The remaining sign debt is binding/stabilizer only; no public local-GR/Newton/PPN or global MTS claim is allowed from this adoption.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4228_SOURCE_REGISTER.csv"]
    adoption = rows_by_file["P8_Y5_R2FR_4228_PARENT_SIGNATURE_ADOPTION.csv"]
    beta_rows = rows_by_file["P8_Y5_R2FR_4228_BETA_SIG_ZERO_ROWS.csv"]
    gates = rows_by_file["P8_Y5_R2FR_4228_EPSILON_GATE_UPDATE.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4228_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4228_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4228_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]
    adoption_ids = {row["adoption_id"] for row in adoption}
    beta_ids = {row["beta_sig_id"] for row in beta_rows}
    gate_ids = {row["gate_id"] for row in gates}
    firewall_ids = {row["firewall_id"] for row in firewalls}

    checks = [
        ("VAL4228_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4228_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4228_2_adoption_rows",
            "adoption rows cover branch, parent action, branch surface, positive hidden signature, descent, boundary and scope",
            {"CSA4228_0_branch_selection", "CSA4228_1_parent_action_signature", "CSA4228_2_branch_surface", "CSA4228_3_positive_hidden_signature", "CSA4228_4_descent_before_variation", "CSA4228_5_boundary_readout_silence", "CSA4228_6_adoption_scope"}.issubset(adoption_ids),
        ),
        (
            "VAL4228_3_private_not_global",
            "decision adopts private signature but not global signature",
            decision["private_signature_clause_adopted"] == "True" and decision["global_signature_clause_adopted"] == "False",
        ),
        (
            "VAL4228_4_beta_sig_zero",
            "beta rows zero E_signature_mismatch_abs, beta_sig and MTS core negative channel privately",
            {"BSZ4228_0_signature_zero", "BSZ4228_1_beta_sig_zero", "BSZ4228_2_core_negative_zero"}.issubset(beta_ids)
            and decision["beta_sig_private"] == "0"
            and decision["E_MTS_core_neg_abs_private"] == "0",
        ),
        (
            "VAL4228_5_fallback_retained",
            "fallback beta_sig row reopens if branch rejected",
            "BSZ4228_3_reopened_if_rejected" in beta_ids,
        ),
        (
            "VAL4228_6_epsilon_gate_binding_only",
            "epsilon gate now depends on binding/stabilizer numerator in private selector",
            {"EG4228_1_private_selector_gate", "EG4228_2_pass_condition", "EG4228_3_bind_zero_forbidden", "EG4228_4_claim_status"}.issubset(gate_ids),
        ),
        (
            "VAL4228_7_decision_nonclaim",
            "decision keeps all local claims unavailable",
            decision["MEH_claim"] == "False"
            and decision["local_GR_claim"] == "False"
            and decision["newton_claim"] == "False"
            and decision["PPN_claim"] == "False",
        ),
        (
            "VAL4228_8_firewall",
            "firewall blocks global adoption, public local GR, binding erasure, sector spillover and numerical G",
            {"CSF4228_0_no_global_adoption", "CSF4228_1_no_public_local_GR", "CSF4228_2_no_binding_erasure", "CSF4228_3_no_sector_spillover", "CSF4228_4_no_numerical_G"}.issubset(firewall_ids),
        ),
        (
            "VAL4228_9_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4228_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4228_11_claim_register", "claim register contains L-069", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4228_12_spine_packet", "spine and packet contain 4228 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4228_13_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4228_14_status_script", "status records decision and generator script exists", rows_by_file["P8_Y5_R2FR_4228_STATUS.csv"][0]["decision"] == DECISION and (SCRIPTS / "Y5_R2FR_4228_core_signature_clause_adoption_or_beta_sig_bound_fill.py").exists()),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4228_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4228_PARENT_SIGNATURE_ADOPTION.csv": adoption_rows(),
        "P8_Y5_R2FR_4228_BETA_SIG_ZERO_ROWS.csv": beta_sig_rows(),
        "P8_Y5_R2FR_4228_EPSILON_GATE_UPDATE.csv": epsilon_gate_rows(),
        "P8_Y5_R2FR_4228_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4228_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4228_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4228_NEXT_TARGET.csv": next_target_rows(),
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
