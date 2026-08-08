from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
MICRO_RESIDUALS = POST / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"

CHECKPOINT = "4372"
CLAIM_ID = "L-213"
BRANCH = "MTS_R2FR_Y5_TRANSITION_EPERP_ENVELOPE_DECOMPOSITION_OR_MEASURE_OWNER_ACTION_LINE_PROOF_4372"
MARKER = "PPC4161_TRANSITION_EPERP_ENVELOPE_DECOMPOSITION_OR_MEASURE_OWNER_ACTION_LINE_PROOF_4372"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_EPERP_ENVELOPE_DECOMPOSITION_OR_MEASURE_OWNER_ACTION_LINE_PROOF_4372"
DECISION = "EPERP_COMPONENT_ENVELOPE_DECOMPOSITION_DERIVED_MEASURE_OWNER_ACTION_LINE_CONDITIONAL_NONCLAIM"
NEXT_TARGET = "4373-Y5-R2FR-transition-first-Eperp-component-zero-or-bound-measure-source-mass.md"

FORMAL_PATH = FORMAL / "388-PPC4161-transition-Eperp-envelope-decomposition-or-measure-owner-action-line-proof.md"
DOC_PATH = POST / "4372-Y5-R2FR-transition-Eperp-envelope-decomposition-or-measure-owner-action-line-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4372_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4372_00_4371_formal": (
        FORMAL / "387-PPC4161-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md",
        "epsilon_Gsrc_perp = epsilon_measure_perp + epsilon_mass_perp + epsilon_transition_perp + epsilon_XiT_perp",
        "4371 decomposes the missing E_perp target at the measure-owner firewall.",
    ),
    "SRC4372_01_4371_acquisition": (
        SOURCE_DIR / "P8_Y5_R2FR_4371_ACQUISITION_ROWS.csv",
        "ACQ4371_0_Eperp_bound",
        "4371 leaves E_perp as the missing bound to decompose.",
    ),
    "SRC4372_02_4371_measure": (
        SOURCE_DIR / "P8_Y5_R2FR_4371_MEASURE_OWNER_LEMMA.csv",
        "MO4371_0_measure_zero_lemma",
        "measure-owner zero lemma is conditional and unsigned.",
    ),
    "SRC4372_03_4371_support": (
        SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv",
        "SUP4371_2_Sun_Earth_average",
        "support geometry is filled but E_perp remains unsourced.",
    ),
    "SRC4372_04_4178_reactivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_2_wrong_mass_charge",
        "wrong mass/source charge reopens measured-GM/source-normalization rows.",
    ),
    "SRC4372_05_4362_csrc": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_VECTOR_BASIS.csv",
        "CSRC4362_3_epsilon_Gsrc_open",
        "epsilon_Gsrc_open is the non-product source/coupling drift envelope.",
    ),
    "SRC4372_06_4332_xi": (
        SOURCE_DIR / "P8_Y5_R2FR_4332_XI_OPEN_TAIL_ROWS.csv",
        "TAIL4332_6_Xi_open",
        "Xi_open is the canonical hidden source-label tail.",
    ),
    "SRC4372_07_4334_topen": (
        SOURCE_DIR / "P8_Y5_R2FR_4334_OPEN_TAIL_VECTOR_BASIS.csv",
        "T4334_7_matter_shadow",
        "T_open keeps projection/EM/coeff/tau/domain/matter-shadow tails.",
    ),
    "SRC4372_08_transition_hair": (
        FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "HB4356_7_total_with_4355",
        "transition hair feeds epsilon_Gsrc if open.",
    ),
    "SRC4372_09_measure_edge": (
        MICRO_RESIDUALS / "R2FR_parent_owned_edge_audit_nonclaim_1606.csv",
        "EDGE1606_5_measure",
        "measure/Jacobian owner edge remains unsigned.",
    ),
    "SRC4372_10_formal_194": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "No orbital `GM`",
        "source mass/coupling must not be defined by orbital GM.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4372_0_Eperp_no_cancellation",
            "statement": "The noncommon source-normalization envelope is bounded by the sum of separately owned component envelopes.",
            "formula": "E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T",
            "proof": "epsilon_Gsrc_perp is decomposed into named residual fields and the sup norm obeys the triangle inequality. No cancellation between sectors is permitted unless a parent identity is proved before scoring.",
            "status": "DERIVED_ENVELOPE_BOUND",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4372_1_score_transfer",
            "statement": "The 4370/4371 Newton support gate now applies to the component sum.",
            "formula": "|deltaa_perp|/|a_N| <= K_N(s) (E_measure + E_mass + E_transition + E_Xi + E_T)",
            "proof": "substitute the no-cancellation E_perp bound into the K_N(s) coefficient gate.",
            "status": "DERIVED_SCORE_CHAIN",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4372_2_measure_action_line_conditional_zero",
            "statement": "If ordinary matter is on one parent action line with one q-basic species-blind measure, no field-normalization/hbar source slot, and variation before readout, then E_measure=0.",
            "formula": "S_m=int dmu_* L_m(q(Phi),Psi); D_A ln dmu_*=0 => E_measure=0",
            "proof": "the Hilbert source variation sees the same measure for every source/species/readout label, so the noncommon source-measure defect has no transverse component.",
            "status": "CONDITIONAL_PROOF_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4372_3_measure_zero_not_full_zero",
            "statement": "Even if E_measure=0, local GR still needs E_mass, E_transition, E_Xi, and E_T zeroed or bounded.",
            "formula": "E_perp|_{E_measure=0} <= E_mass + E_transition + E_Xi + E_T",
            "proof": "component ownership is separate; a measure theorem does not prove same-source mass, transition-kernel membership, hidden source-label silence, or projection-tail silence.",
            "status": "FIREWALL_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def component_rows() -> List[Dict[str, str]]:
    return [
        {
            "component_id": "EP4372_0_measure",
            "symbol": "E_measure",
            "definition": "source-measure/Jacobian/hbar/field-normalization contribution to epsilon_Gsrc_perp",
            "zero_condition": "one q-basic species-blind measure before variation and no hidden normalization slot",
            "current_status": "CONDITIONAL_LEMMA_UNSIGNED",
            "source_anchor": "MO4371_0; EDGE1606_5_measure; RE4178_1_ZH_leak",
            "next_action": "prove species-blind measure/Jacobian action-line clause or carry finite derivative envelope",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4372_1_mass",
            "symbol": "E_mass",
            "definition": "same-source-mass/worldtube/Hamiltonian charge mismatch contribution",
            "zero_condition": "M_Hdress equals the Hilbert/worldtube source charge before orbital readout with no GM laundering",
            "current_status": "PRIVATE_SELECTOR_NOT_GLOBAL",
            "source_anchor": "RE4178_2_wrong_mass_charge; formal 186/187/194",
            "next_action": "prove same-worldtube support and source-mass owner, or bound wrong-mass-charge residual",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4372_2_transition",
            "symbol": "E_transition",
            "definition": "noncommon transition source hair feeding epsilon_Gsrc",
            "zero_condition": "transition residue is static l=0 universal range-free same-metric same-worldtube Hilbert monopole",
            "current_status": "TRANSITION_KERNEL_UNSIGNED",
            "source_anchor": "HB4356_7_total_with_4355",
            "next_action": "zero/source Y_tau, Y_l>=1, Y_species_frame_source, Y_lambda, Y_nonEH, Y_boundary",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4372_3_Xi",
            "symbol": "E_Xi",
            "definition": "hidden source-label/source-prefactor tail contribution",
            "zero_condition": "all 4332 Xi component zero clauses hold in the Hilbert-owner source-label-forgetting branch",
            "current_status": "OPEN_TAIL_RETAINED",
            "source_anchor": "TAIL4332_6_Xi_open; ZERO4332_8_Xi",
            "next_action": "prove source-label forgetting/no-hidden-slot clauses or bound Xi components",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4372_4_Topen",
            "symbol": "E_T",
            "definition": "projection/readout/EM/coeff/tau/domain/matter-shadow tail contribution",
            "zero_condition": "T_open projection basis is theorem-zero or source-backed below local-test bounds",
            "current_status": "PROJECTION_MATRIX_INPUTS_OPEN",
            "source_anchor": "T4334_0_Xi through T4334_7_matter_shadow",
            "next_action": "fill or zero arena projection matrix components fixed before scoring",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
    ]


def measure_action_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "MA4372_0_single_action_line",
            "clause": "ordinary matter terms descend from one parent action-density line",
            "needed_for": "forbid independent sector/source weights before variation",
            "current_evidence": "P4361_0 target sharpened but unsigned",
            "current_status": "UNSIGNED",
            "activates_E_measure_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "MA4372_1_species_blind_measure",
            "clause": "one q-basic measure/Jacobian/hbar and no field-normalization source slot",
            "needed_for": "D_A ln dmu_*=0 and no hidden source-measure leak",
            "current_evidence": "P4361_2 required extension unsigned; EDGE1606_5 parent_owned=False",
            "current_status": "UNSIGNED",
            "activates_E_measure_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "MA4372_2_typed_no_source_prefactor",
            "clause": "source labels cannot define a scalar prefactor object in the parent grammar",
            "needed_for": "exclude N_src(Phi), theta_src(Phi), hbar_A, field rescaling countermodels",
            "current_evidence": "P4361_3 conditional grammar unsigned; MO4371_1 countermodel retained",
            "current_status": "UNSIGNED_WITH_COUNTERMODEL",
            "activates_E_measure_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "MA4372_3_variation_before_readout",
            "clause": "readout/projector/worldtube maps cannot introduce source labels after variation",
            "needed_for": "prevents post-variation source-measure reentry",
            "current_evidence": "P4361_4 branch-local conditional, not global",
            "current_status": "BRANCH_LOCAL_ONLY",
            "activates_E_measure_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "MA4372_4_same_branch_lock",
            "clause": "all measure-owner clauses hold on the same local branch as source-mass and transition-hair clauses",
            "needed_for": "promote E_measure=0 into a useful E_perp reduction without mixing selectors",
            "current_evidence": "4371/4372 keep same-source mass, transition, Xi and T components separate",
            "current_status": "NOT_ASSEMBLED",
            "activates_E_measure_zero": "False",
            "valid_for_claim": "False",
        },
    ]


def scorechain_rows() -> List[Dict[str, str]]:
    support_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv")
    rows: List[Dict[str, str]] = []
    for row in support_rows:
        rows.append(
            {
                "score_id": f"SC4372_{row['support_id']}",
                "support_id": row["support_id"],
                "source_body": row["source_body"],
                "test_body_or_readout": row["test_body_or_readout"],
                "K_N": row["selected_K_N"],
                "score_formula": "fractional_residual <= K_N*(E_measure+E_mass+E_transition+E_Xi+E_T)",
                "pass_formula": f"E_measure+E_mass+E_transition+E_Xi+E_T <= delta_N/{row['selected_K_N']}",
                "current_status": "GEOMETRY_READY_COMPONENT_ENVELOPES_MISSING",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def acquisition_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "ACQ4372_0_E_measure",
            "needed_quantity": "E_measure theorem-zero or finite bound",
            "preferred_route": "prove MA4372 measure action-line clauses",
            "fallback_route": "source a finite D_A delta_ZH / source-measure envelope",
            "current_status": "UNSIGNED_UNBOUNDED",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ACQ4372_1_E_mass",
            "needed_quantity": "same-source mass/worldtube mismatch bound",
            "preferred_route": "parent-sign M_Hdress as same Hilbert source charge before readout",
            "fallback_route": "bound wrong-mass-charge residual from source/worldtube map",
            "current_status": "PRIVATE_SELECTOR_NOT_GLOBAL",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ACQ4372_2_E_transition",
            "needed_quantity": "transition hair envelope",
            "preferred_route": "prove static l=0 common Hilbert monopole membership",
            "fallback_route": "source/bound Y_tau, Y_l>=1, Y_species_frame_source, Y_lambda, Y_nonEH, Y_boundary",
            "current_status": "UNSIGNED_UNBOUNDED",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ACQ4372_3_E_Xi",
            "needed_quantity": "Xi_open component bound",
            "preferred_route": "prove all 4332 source-label-forgetting clauses",
            "fallback_route": "bound retained Xi components with no cancellation",
            "current_status": "OPEN_TAIL",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ACQ4372_4_E_T",
            "needed_quantity": "T_open arena tail bound",
            "preferred_route": "prove standard source-readout closure or source-backed projection matrices",
            "fallback_route": "bound each T4334 component in the target arena",
            "current_status": "PROJECTION_INPUTS_OPEN",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4372_0_decomposition",
            "claim_tested": "E_perp decomposed into no-cancellation component envelope",
            "required_inputs": "component definitions and triangle-inequality theorem",
            "status": "PASS_DERIVED",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4372_1_measure_action_line",
            "claim_tested": "E_measure=0",
            "required_inputs": "all MA4372 clauses parent-signed on one branch",
            "status": "BLOCKED_UNSIGNED",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4372_2_component_score",
            "claim_tested": "Newton/source-normalization score using component sum",
            "required_inputs": "numeric/theorem-zero rows for all component envelopes plus delta_N",
            "status": "BLOCKED_COMPONENT_INPUTS_MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4372_3_public_local_GR",
            "claim_tested": "public local-GR/Newton/PPN pass",
            "required_inputs": "component score plus PPN/EM/Bianchi/boundary closure",
            "status": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4372_0",
            "decision": DECISION,
            "summary": (
                "4372 decomposes E_perp into a no-cancellation component envelope: E_measure, E_mass, E_transition, E_Xi and E_T. "
                "The Newton/source gate from 4370/4371 now scores the sum, not a foggy single parameter. The measure-owner action-line proof is sharpened: "
                "one q-basic species-blind measure with no hbar/Jacobian/field-normalization/source-prefactor slot would set E_measure=0, but 4361/1606 keep the needed clauses unsigned. "
                "Even if E_measure closed, E_mass, E_transition, E_Xi and E_T would still need zero/bound rows. No local-GR/Newton/PPN claim fires."
            ),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4372_0",
            "object": "E_perp",
            "status": "DECOMPOSED",
            "note": "E_perp is now a sum of five named envelopes under a no-cancellation rule.",
        },
        {
            "status_id": "STAT4372_1",
            "object": "E_measure",
            "status": "CONDITIONAL_ZERO_PROOF_UNSIGNED",
            "note": "action-line measure owner proof is written but not parent-signed.",
        },
        {
            "status_id": "STAT4372_2",
            "object": "score chain",
            "status": "GEOMETRY_READY_COMPONENTS_MISSING",
            "note": "4371 support rows now score the component sum once component bounds exist.",
        },
        {
            "status_id": "STAT4372_3",
            "object": "next work",
            "status": "FIRST_COMPONENT_ZERO_OR_BOUND",
            "note": "attack E_measure or E_mass first because they sit closest to calibrated source coupling.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4372_0",
            "target": NEXT_TARGET,
            "question": "Can the first E_perp component be zeroed or bounded, starting with E_measure or E_mass?",
            "preferred_route": "try to parent-sign E_measure via the action-line measure owner clauses",
            "alternate_route": "derive/source an E_mass same-worldtube source-mass mismatch bound",
            "avoid": "treating the component decomposition as a numeric bound",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    components: List[Dict[str, str]],
    measure_action: List[Dict[str, str]],
    scorechain: List[Dict[str, str]],
    acquisition: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: E_perp envelope decomposition or measure-owner action-line proof

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4372 turns `E_perp` from one missing symbol into a no-cancellation component envelope:

```text
E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T.
```

The Newton/source-normalization score chain is therefore:

```text
|deltaa_perp|/|a_N| <= K_N(s)
  (E_measure + E_mass + E_transition + E_Xi + E_T).
```

This is constructive: each component now has its own zero route or finite-bound route. It also blocks a common bad move: a proof for one component cannot be sold as a proof of local GR.

The measure-owner action-line proof is now exact but conditional:

```text
S_m = int dmu_* L_m(q(Phi), Psi),
D_A ln dmu_* = 0
  => E_measure=0.
```

Current corpus status: the measure/Jacobian/hbar/no-source-prefactor clauses are not parent-signed, so the proof does not activate yet.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Theorem Rows

{md_table(theorems, ["theorem_id", "statement", "formula", "proof", "status"])}

## E_perp Component Envelopes

{md_table(components, ["component_id", "symbol", "definition", "zero_condition", "current_status", "source_anchor", "next_action"])}

## Measure-Owner Action-Line Audit

{md_table(measure_action, ["clause_id", "clause", "needed_for", "current_evidence", "current_status", "activates_E_measure_zero"])}

## Geometry Score Chain

{md_table(scorechain, ["score_id", "support_id", "source_body", "test_body_or_readout", "K_N", "score_formula", "pass_formula", "current_status"])}

## Acquisition Rows

{md_table(acquisition, ["input_id", "needed_quantity", "preferred_route", "fallback_route", "current_status"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "valid_for_claim"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4372: E_perp envelope decomposition or measure-owner action-line proof

Marker: `{MARKER}`

## What changed

- Decomposed `E_perp` into `E_measure + E_mass + E_transition + E_Xi + E_T`.
- Mapped the 4371 geometry gate onto the component sum.
- Wrote the exact conditional action-line proof for `E_measure=0`.
- Kept the proof unsigned because measure/Jacobian/hbar/source-prefactor clauses are not parent-certified.

## Decision row

{md_table(decisions, ["decision_id", "decision", "summary", "next_target"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4372 Transition E_perp component envelope

Marker: `{MARKER}`

4372 decomposes the Newton/source-normalization obstruction:

```text
E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T.
```

This makes the 4370/4371 geometry gate operational at component level:

```text
|deltaa_perp|/|a_N| <= K_N(s)(E_measure+E_mass+E_transition+E_Xi+E_T).
```

The measure-owner action-line proof is exact but conditional: a single q-basic species-blind matter measure with no Jacobian/hbar/field-normalization/source-prefactor slot would give `E_measure=0`. Current evidence does not parent-sign those clauses. Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4372 packet update: E_perp decomposed

Marker: `{PACKET_MARKER}`

Packet update: `E_perp` is no longer one missing box. It is the no-cancellation sum of `E_measure`, `E_mass`, `E_transition`, `E_Xi`, and `E_T`. The next packet work should zero or bound the first component, preferably `E_measure` via the measure action-line proof or `E_mass` via same-worldtube source-mass ownership.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4372 decomposes the missing epsilon_Gsrc_perp envelope into a no-cancellation component bound: "
                "E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T. "
                "The 4370/4371 Newton/source geometry gate now scores this component sum. "
                "The measure-owner action-line proof is sharpened: if ordinary matter has one q-basic species-blind parent measure with no Jacobian/hbar/field-normalization/source-prefactor slot before variation, then E_measure=0. "
                "Those clauses remain unsigned, and even E_measure=0 would not close E_mass, E_transition, E_Xi or E_T. No local-GR/Newton/PPN/WEP/clock/orbital/R10 claim fires."
            ),
            "4372 source register, theorem rows, E_perp component envelopes, measure-owner action-line audit, geometry score chain, acquisition rows, claim gates, decision, status, next target and validation CSV.",
            "Eperp_component_decomposition_measure_owner_conditional_unsigned_nonclaim",
            "Zero or bound the first E_perp component, preferably E_measure via action-line measure ownership or E_mass via same-worldtube source-mass ownership.",
            "Treating a component theorem as full local GR; cancelling component envelopes; claiming E_measure=0 without excluding Jacobian/hbar/source-normalization slots; using support geometry as a numeric residual bound.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4372_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4372_THEOREM_ROWS.csv")
    components = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4372_EPERP_COMPONENT_ENVELOPES.csv")
    measure_action = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4372_MEASURE_OWNER_ACTION_LINE_AUDIT.csv")
    scorechain = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4372_GEOMETRY_SCORE_CHAIN.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4372_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4372_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4372_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4372_2_decomposition_theorem",
        any(row["theorem_id"] == "TH4372_0_Eperp_no_cancellation" and "E_measure" in row["formula"] for row in theorems),
        "no-cancellation decomposition theorem exists",
    )
    add(
        "VAL4372_3_five_components",
        {row["symbol"] for row in components} == {"E_measure", "E_mass", "E_transition", "E_Xi", "E_T"},
        "exact five component envelopes present",
    )
    add(
        "VAL4372_4_measure_unsigned",
        all(row["activates_E_measure_zero"] == "False" for row in measure_action),
        "measure action-line clauses do not falsely activate zero",
    )
    add(
        "VAL4372_5_scorechain_uses_components",
        all("E_measure+E_mass+E_transition+E_Xi+E_T" in row["score_formula"] for row in scorechain),
        "all support geometry rows score the component sum",
    )
    add("VAL4372_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4372_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4372_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4372_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4372_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4372_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4372_12_no_valid_claim_rows",
        all("True" not in [row.get("valid_for_claim", ""), row.get("claim_allowed", "")] for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4372_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_rows()
    theorems = theorem_rows()
    components = component_rows()
    measure_action = measure_action_rows()
    scorechain = scorechain_rows()
    acquisition = acquisition_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4372_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4372_THEOREM_ROWS.csv": theorems,
        "P8_Y5_R2FR_4372_EPERP_COMPONENT_ENVELOPES.csv": components,
        "P8_Y5_R2FR_4372_MEASURE_OWNER_ACTION_LINE_AUDIT.csv": measure_action,
        "P8_Y5_R2FR_4372_GEOMETRY_SCORE_CHAIN.csv": scorechain,
        "P8_Y5_R2FR_4372_ACQUISITION_ROWS.csv": acquisition,
        "P8_Y5_R2FR_4372_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4372_DECISION.csv": decisions,
        "P8_Y5_R2FR_4372_STATUS.csv": statuses,
        "P8_Y5_R2FR_4372_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorems, components, measure_action, scorechain, acquisition, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()

    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
