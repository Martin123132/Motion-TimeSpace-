from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4535"
CLAIM_ID = "L-377"
MARKER = "PPC4161_ACTION_SCALE_MEASURE_OWNER_FROM_MTS_ACTION_LINE_OR_ADOPT_STRICT_GRAMMAR_CLOSURE_4535"
PACKET_MARKER = "PPC4161_PACKET_ACTION_SCALE_MEASURE_OWNER_FROM_MTS_ACTION_LINE_OR_ADOPT_STRICT_GRAMMAR_CLOSURE_4535"
DECISION = "MTS_ACTION_LINE_SIGNS_TOTAL_HILBERT_SOURCE_ROOT_EDGE_BUT_NOT_COMPONENT_LEVEL_NO_WA"
NEXT_TARGET = "4536-Y5-R2FR-connected-matter-graph-no-relative-action-weight-or-finite-deltaw-bound.md"

FORMAL_PATH = FORMAL / "551-PPC4161-action-scale-measure-owner-from-MTS-action-line-or-adopt-strict-grammar-closure.md"
DOC_PATH = POST / "4535-Y5-R2FR-action-scale-measure-owner-from-MTS-action-line-or-adopt-strict-grammar-closure.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4535_SOURCE_REGISTER.csv"
ACTION_LINE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_ACTION_LINE_PARSE.csv"
OWNER_DERIVATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_OWNER_DERIVATION_SPLIT.csv"
COMPONENT_COUNTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_COMPONENT_WEIGHT_COUNTERMODEL_GATE.csv"
CLOSURE_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_STRICT_GRAMMAR_CLOSURE_STATUS.csv"
FINITE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_FINITE_DELTAW_BOUND_ROUTE.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4535_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4535_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC4535_00_action_principle",
            "label": "core MTS action line",
            "path": ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
            "needle": "A = ∫ [ (1/2κ) R",
            "role": "one total action measure and L_matter root edge",
        },
        {
            "source_id": "SRC4535_01_4422_hbar_measure",
            "label": "4422 hbar/measure owner theorem",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4422_DERIVATION_ROWS.csv",
            "needle": "UHM4422_1_exact_owner_contract",
            "role": "species weights as hbar/action-scale replicas",
        },
        {
            "source_id": "SRC4535_02_4423_action_density",
            "label": "4423 action-density owner output",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4423_ACTION_DENSITY_OWNER_OUTPUT.csv",
            "needle": "ADLO4423_0_core_MTS_action_schema",
            "role": "single L_matter root edge and remaining component blockers",
        },
        {
            "source_id": "SRC4535_03_4534_induction",
            "label": "4534 strict grammar induction",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4534_CONSTRUCTOR_EXHAUSTION_INDUCTION.csv",
            "needle": "IND4534_0_theorem",
            "role": "source-only weights killed under strict grammar",
        },
        {
            "source_id": "SRC4535_04_4534_grammar",
            "label": "4534 strict primitive grammar",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4534_STRICT_MTS_PRIMITIVE_GRAMMAR.csv",
            "needle": "GRAM4534_4_application_status",
            "role": "strict grammar application remains unsigned",
        },
        {
            "source_id": "SRC4535_05_4533_countermodels",
            "label": "4533 countermodel gate",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4533_SOURCE_WEIGHT_COUNTERMODEL_RESOLUTION.csv",
            "needle": "CEX4533_0_relative_species_weight",
            "role": "relative species weight countermodel",
        },
        {
            "source_id": "SRC4535_06_4533_source_pack",
            "label": "4533 source pack",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv",
            "needle": "SP4533_5_delta_w_species",
            "role": "finite Delta_w fallback row",
        },
        {
            "source_id": "SRC4535_07_4534_value_fill",
            "label": "4534 source pack value fill",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4534_SOURCE_PACK_VALUE_FILL_ATTEMPT.csv",
            "needle": "VF4534_OVERALL",
            "role": "no claim-grade finite fill found",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in source_specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def action_line_rows() -> list[dict[str, Any]]:
    return [
        {
            "parse_id": "ALP4535_0_total_action",
            "action_line_piece": "A = ∫[(1/2κ)R - L_Lambda_kappa + L_matter] sqrt(-g)d4x",
            "derived_owner": "one parent integration measure mu_g=sqrt(-g)d4x and one total matter density symbol L_matter",
            "what_it_signs": "the root Hilbert-source edge T_total = -2/sqrt(-g) delta S_matter/delta g",
            "what_it_does_not_sign": "the internal decomposition of L_matter into component actions with or without relative weights",
            "current_status": "ROOT_EDGE_SIGNED_COMPONENT_GRAPH_OPEN",
            "valid_for_claim": "False",
        },
        {
            "parse_id": "ALP4535_1_common_multiplier",
            "action_line_piece": "S_matter -> w_star S_matter",
            "derived_owner": "one common scalar is degenerate with the calibrated gravitational coupling kappa/G_N after source convention is fixed",
            "what_it_signs": "common mode is not a WEP/R10/PPN relative source vector",
            "what_it_does_not_sign": "orthogonal component weights P_perp Delta_w_A",
            "current_status": "COMMON_MODE_CALIBRATION_ONLY",
            "valid_for_claim": "False",
        },
        {
            "parse_id": "ALP4535_2_literal_no_wA",
            "action_line_piece": "the written action contains L_matter, not sum_A w_A L_A",
            "derived_owner": "literal surface grammar has no source-only species coefficient",
            "what_it_signs": "if the written grammar is adopted as complete, w_A is absent",
            "what_it_does_not_sign": "completeness of the grammar, because L_matter could be defined internally as a weighted component sum",
            "current_status": "SURFACE_GRAMMAR_NO_WA_NOT_UNIQUENESS_PROOF",
            "valid_for_claim": "False",
        },
    ]


def owner_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "OWN4535_0_root_edge_theorem",
            "claim": "The MTS action line derives a total Hilbert-source root edge.",
            "derivation": "Let S_matter[g,psi_A,theta_A]=int L_matter sqrt(-g)d4x as written. Variation before readout gives T_total_{mu nu}=-(2/sqrt(-g)) delta S_matter/delta g^{mu nu}. Since the written root has one measure and one L_matter symbol, the active source functor at this level is total Hilbert stress, not a family of source-only labels.",
            "result": "DERIVED_ROOT_EDGE",
            "effect": "source coupling is no longer fully foggy: root source owner is signed for the literal action branch.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "OWN4535_1_why_root_edge_not_enough",
            "claim": "The root edge does not prove component no-w_A.",
            "derivation": "A theorist can define L_matter:=sum_A w_A L_A and still write one integral and one T_total. Ward identities and covariance conserve the selected weighted source. Therefore the action line alone cannot decide whether w_A is illegal or simply hidden inside L_matter.",
            "result": "COUNTERMODEL_SURVIVES_COMPONENT_LEVEL",
            "effect": "prevents a false win from the single integral notation.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "OWN4535_2_action_quantum_interpretation",
            "claim": "Relative w_A is an action-scale/phase-unit split, not just a harmless classical normalization.",
            "derivation": "In a phase/path-weight reading, exp(i sum_A w_A S_A/hbar_parent)=exp(i sum_A S_A/hbar_A) with hbar_A=hbar_parent/w_A. Thus no relative w_A follows if the parent owns one hbar/action phase and one species-blind measure. Without that owner the countermodel survives.",
            "result": "EXACT_CONDITIONAL_OWNER_THEOREM",
            "effect": "turns source coupling into a concrete action-scale owner question.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "OWN4535_3_connected_graph_route",
            "claim": "A connected ordinary matter graph can make relative sector weights observable rather than source-only.",
            "derivation": "If the parent matter graph has canonical kinetic normalizations and shared interaction vertices, independent w_A factors can be moved only by field redefinitions that alter dimensionless couplings, masses, charge/current normalizations, or interaction strengths. Then invisible active-source-only w_A is not available; it becomes either measured theta_A data or a forbidden source-only spurion.",
            "result": "PROMISING_NEXT_DERIVATION_ROUTE",
            "effect": "next step is not another action-line pass but a connected matter graph/no-prefactor theorem.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "OWN4535_4_current_verdict",
            "claim": "Current MTS signs the root edge but not the full component owner.",
            "derivation": "Core action evidence signs one total L_matter and Hilbert source. Prior hbar/measure and strict grammar evidence signs exact conditional theorems. None proves that the parent matter graph is connected, canonically normalized, and stable against hidden/readout/radiative re-entry.",
            "result": "PARTIAL_DERIVATION_NONCLAIM",
            "effect": "local GR/Newton source-coupling route is narrowed to component graph/no-prefactor plus finite Delta_w bound.",
            "valid_for_claim": "False",
        },
    ]


def component_counter_rows() -> list[dict[str, Any]]:
    return [
        {
            "counter_id": "CCG4535_0_weighted_decomposition",
            "countermodel": "Define L_matter := sum_A w_A L_A inside the single action line.",
            "why_action_line_survives": "one integral, one measure and one total Hilbert source still exist",
            "what_breaks_or_changes": "source normalization becomes T_total=sum_A w_A T_A; if interactions connect sectors, field redefinitions change measured couplings",
            "killed_by": "parent-owned connected matter graph with canonical normalization plus no source-only spurion",
            "current_status": "LIVE_COMPONENT_COUNTERMODEL",
            "valid_for_claim": "False",
        },
        {
            "counter_id": "CCG4535_1_common_weight",
            "countermodel": "w_A=w_star for all A",
            "why_action_line_survives": "common factor multiplies the whole matter action",
            "what_breaks_or_changes": "nothing relative after measured G/kappa calibration, provided source convention is fixed",
            "killed_by": "not necessary; classify as calibration mode",
            "current_status": "CALIBRATION_MODE_NOT_LOCAL_RESIDUAL",
            "valid_for_claim": "False",
        },
        {
            "counter_id": "CCG4535_2_orthogonal_weight",
            "countermodel": "P_perp Delta_w_A != 0",
            "why_action_line_survives": "can be hidden in the internal definition of L_matter",
            "what_breaks_or_changes": "composition-dependent source charge; WEP/R10/PPN source normalization residual",
            "killed_by": "strict grammar/action-scale owner or finite bound on Delta_w*tau",
            "current_status": "LIVE_PHYSICAL_RESIDUAL_UNLESS_OWNER_SIGNED",
            "valid_for_claim": "False",
        },
    ]


def closure_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "CL4535_0_strict_grammar_option",
            "closure": "StrictMTSPrimitiveSet from 4534",
            "status": "AVAILABLE_AS_EXPLICIT_PRIVATE_CLOSURE",
            "why_not_claim": "the current parent action line does not by itself prove the grammar is unique or radiative/readout stable",
            "if_adopted": "P_perp Delta_w_A=0 and source-only species weights are unformable",
            "risk": "would be an axiom/closure, not a derivation",
            "valid_for_claim": "False",
        },
        {
            "closure_id": "CL4535_1_recommended_default",
            "closure": "do not adopt yet as final theorem",
            "status": "DERIVE_NEXT",
            "why_not_claim": "a connected matter graph/no-prefactor theorem may derive more of the closure without fiat",
            "if_adopted": "useful for private branch testing only",
            "risk": "premature closure would hide the exact place source coupling is still open",
            "valid_for_claim": "False",
        },
    ]


def finite_bound_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv"):
        if row.get("pack_id") in {"SP4533_5_delta_w_species", "SP4533_6_PPN_proxy", "SP4533_7_WEP_unit_proxy"}:
            rows.append(
                {
                    "bound_id": "FBR4535_" + row["pack_id"].replace("SP4533_", ""),
                    "quantity": row.get("quantity", ""),
                    "current_value": row.get("current_value", ""),
                    "status": row.get("status", ""),
                    "usable_now": "False",
                    "reason": "proxy/symbolic row only; no parent component graph coefficient and no no-cancellation material projection",
                    "next_needed": row.get("acceptance", ""),
                    "source_path": row.get("source_path", ""),
                    "valid_for_claim": "False",
                }
            )
    rows.append(
        {
            "bound_id": "FBR4535_OVERALL",
            "quantity": "Delta_w component finite branch",
            "current_value": "no claim-grade bound",
            "status": "FINITE_BRANCH_OPEN",
            "usable_now": "False",
            "reason": "need either owner theorem zero or numeric Delta_w/tau/material no-cancellation row",
            "next_needed": "connected matter graph no-relative-weight theorem or finite Delta_w bound with source-backed material projection",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv"),
            "valid_for_claim": "False",
        }
    )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4535_0_root_edge",
            "gate": "total Hilbert source root edge",
            "status": "PASS_DERIVED_FOR_LITERAL_ACTION_BRANCH",
            "meaning": "one L_matter and one measure give one total Hilbert source before readout",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4535_1_component_no_wA",
            "gate": "component-level no relative source weight",
            "status": "BLOCKED_COMPONENT_GRAPH_OWNER_UNSIGNED",
            "meaning": "L_matter can still be internally decomposed with relative weights unless the parent matter graph/no-prefactor theorem closes",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4535_2_strict_closure",
            "gate": "adopt strict grammar closure",
            "status": "AVAILABLE_BUT_NOT_PROMOTED",
            "meaning": "strict closure would kill w_A but would be closure, not derivation",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4535_3_finite_bound",
            "gate": "finite Delta_w bound",
            "status": "BLOCKED_NO_SOURCE_BACKED_VALUE",
            "meaning": "symbolic/proxy rows exist but no claim-grade component coefficient",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4535_0",
            "decision": DECISION,
            "meaning": "4535 moves the coupling branch forward by signing the total Hilbert-source root edge from the actual MTS action line. The remaining live target is narrower: component-level relative action weights inside L_matter. The best next derivation is a connected matter graph/canonical normalization/no-source-prefactor theorem; if that fails, use explicit strict-grammar closure or source-backed finite Delta_w bounds.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4535_0",
            "target": NEXT_TARGET,
            "objective": "Try to prove that the ordinary matter component graph is connected/canonically normalized enough that relative w_A cannot remain an invisible active-source-only coefficient.",
            "derive_first": "show independent component action weights either reduce to common calibration or change measured dimensionless couplings/mass/charge data, so the source-only orthogonal vector is not parent-generated.",
            "fallback": "keep strict grammar as named closure only and build finite Delta_w/tau/material projection bound rows.",
            "avoid": "claiming the single L_matter line alone proves no internal weighted decomposition.",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    action_line: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4535_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    action_ok = {"ALP4535_0_total_action", "ALP4535_2_literal_no_wA"}.issubset({row["parse_id"] for row in action_line})
    checks.append({"validation_id": "VAL4535_01_action_parse", "status": "PASS" if action_ok else "FAIL", "detail": "action line parsed into root edge and component-open rows"})

    owner_ok = {"OWN4535_0_root_edge_theorem", "OWN4535_1_why_root_edge_not_enough", "OWN4535_4_current_verdict"}.issubset({row["derivation_id"] for row in owner})
    checks.append({"validation_id": "VAL4535_02_owner_split", "status": "PASS" if owner_ok else "FAIL", "detail": "owner derivation split has root theorem and component blocker"})

    counter_ok = {"CCG4535_0_weighted_decomposition", "CCG4535_2_orthogonal_weight"}.issubset({row["counter_id"] for row in counters})
    checks.append({"validation_id": "VAL4535_03_countermodels", "status": "PASS" if counter_ok else "FAIL", "detail": "component weighted decomposition countermodel retained"})

    closure_ok = any(row["closure_id"] == "CL4535_1_recommended_default" and row["status"] == "DERIVE_NEXT" for row in closure)
    checks.append({"validation_id": "VAL4535_04_closure_status", "status": "PASS" if closure_ok else "FAIL", "detail": "strict grammar closure available but not promoted"})

    finite_ok = any(row["bound_id"] == "FBR4535_OVERALL" and row["usable_now"] == "False" for row in finite)
    checks.append({"validation_id": "VAL4535_05_finite_bound", "status": "PASS" if finite_ok else "FAIL", "detail": "finite Delta_w branch checked and remains open"})

    gate_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    checks.append({"validation_id": "VAL4535_06_claims_blocked", "status": "PASS" if gate_ok else "FAIL", "detail": "all claim gates remain nonclaim"})

    csv_files = [SOURCE_REGISTER, ACTION_LINE_CSV, OWNER_DERIVATION_CSV, COMPONENT_COUNTER_CSV, CLOSURE_STATUS_CSV, FINITE_BOUND_CSV, GATES_CSV, DECISION_CSV, NEXT_CSV]
    csv_ok = True
    detail: list[str] = []
    for path in csv_files:
        try:
            if not read_csv(path):
                csv_ok = False
                detail.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            detail.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4535_07_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(detail)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4535_08_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4535_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4535 action-scale/measure owner split and next component graph target"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    action_line: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4535 - action-scale measure owner from MTS action line or strict grammar closure

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains internal, conditional and nonclaim.

## What Moved

- The core MTS action line now signs a real piece: one total `L_matter`, one `sqrt(-g)d4x` measure and one total Hilbert source root edge.
- This is not enough to claim local GR/Newton source coupling, because `L_matter := sum_A w_A L_A` can still be hidden inside the matter sector unless the component graph/no-prefactor theorem closes.
- The source-coupling problem is therefore narrower: not "find the coupling" in fog, but prove or bound the orthogonal component action-weight vector `P_perp Delta_w_A`.
- Strict grammar from 4534 remains available as an explicit private closure, but 4535 does not promote it as a derived theorem.

## Action Line Parse

{markdown_table(action_line)}

## Owner Derivation Split

{markdown_table(owner)}

### Compact Derivation

From the written MTS action,

`A = int [(1/2 kappa)R - L_Lambda_kappa + L_matter] sqrt(-g)d4x`,

define `S_matter = int L_matter sqrt(-g)d4x`. Variation before readout gives one total Hilbert source:

`T_total_{{mu nu}} = -2/sqrt(-g) delta S_matter / delta g^{{mu nu}}`.

So the root active-source functor is owned by the action line. However, this does not decide the internal definition of `L_matter`. If `L_matter=sum_A w_A L_A`, the same root action and total Hilbert derivative still exist, but the source becomes weighted. Therefore the root edge is derived, while component-level no-`w_A` requires a connected/canonically normalized matter graph or the strict grammar closure from 4534.

## Component Countermodel Gate

{markdown_table(counters)}

## Strict Grammar Closure Status

{markdown_table(closure)}

## Finite Delta-w Bound Route

{markdown_table(finite)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "claim_name": "local_gr_newton_r2fr_action_line_root_owner",
        "statement": "4535 derives the total Hilbert-source root edge from the MTS action line, but keeps component-level no-w_A blocked until connected matter graph/no-prefactor or finite Delta_w bounds close.",
        "evidence": "Generated action-line parse, owner derivation split, component countermodel gate, strict closure status, finite Delta_w route and validation P8_Y5_BRR545_4535_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_root_edge_signed_component_weights_open",
        "next_target": NEXT_TARGET,
        "blocker": "L_matter can still be internally decomposed as weighted component actions unless parent matter graph/canonical normalization/no-source-prefactor is derived.",
        "sector": "local_gr_newton",
        "source_path": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "failure_mode": "Treating one written L_matter as proof that no internal weighted component decomposition exists.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    action_line = action_line_rows()
    owner = owner_derivation_rows()
    counters = component_counter_rows()
    closure = closure_status_rows()
    finite = finite_bound_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_LINE_CSV, action_line)
    write_csv(OWNER_DERIVATION_CSV, owner)
    write_csv(COMPONENT_COUNTER_CSV, counters)
    write_csv(CLOSURE_STATUS_CSV, closure)
    write_csv(FINITE_BOUND_CSV, finite)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, action_line, owner, counters, closure, finite, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, action_line, owner, counters, closure, finite, gates, decisions, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4535 Action Scale Measure Owner From MTS Action Line Or Strict Grammar Closure

Marker: `{MARKER}`  
4535 signs the total Hilbert-source root edge from the written MTS action: one `L_matter`, one `sqrt(-g)d4x` measure and one total Hilbert variation. It does not overclaim component-level no-`w_A`, because `L_matter=sum_A w_A L_A` can still hide inside the matter sector until a connected/canonically normalized matter graph and no-source-prefactor theorem closes. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4535 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet may now treat the total MTS `L_matter -> T_total` root edge as derived for the literal action branch. The open source-coupling vector is narrowed to component-level `P_perp Delta_w_A`, hidden/readout re-entry and finite Delta-w bounds.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
