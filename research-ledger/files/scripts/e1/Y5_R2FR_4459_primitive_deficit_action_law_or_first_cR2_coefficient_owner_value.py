from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from primitive_deficit_refinement_gate import (  # noqa: E402
    claim_gate_rows,
    coefficient_owner_template_rows,
    phi_refinement_scan_rows,
    read_csv,
    selector_signature_rows,
    theorem_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4459"
CLAIM_ID = "L-301"
MARKER = "PPC4161_PRIMITIVE_DEFICIT_REFINEMENT_LINEARITY_OR_FIRST_COEFFICIENT_OWNER_4459"
PACKET_MARKER = "PPC4161_PACKET_PRIMITIVE_DEFICIT_REFINEMENT_LINEARITY_OR_FIRST_COEFFICIENT_OWNER_4459"
DECISION = "REFINEMENT_INVARIANCE_FORCES_LINEAR_DEFICIT_RESPONSE_CONDITIONALLY_PARENT_SIGNATURE_AND_COEFFICIENT_VALUES_STILL_MISSING_NONCLAIM"
NEXT_TARGET = "4460-Y5-R2FR-parent-refinement-gauge-signature-or-visible-c2-finite-row.md"

FORMAL_PATH = FORMAL / "475-PPC4161-primitive-deficit-refinement-linearity-or-first-coefficient-owner-row.md"
DOC_PATH = POST / "4459-Y5-R2FR-primitive-deficit-action-law-or-first-cR2-coefficient-owner-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4459_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4459_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_REFINEMENT_LINEARITY_THEOREM.csv"
PHI_SCAN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_PHI_REFINEMENT_SCAN.csv"
SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_SELECTOR_SIGNATURE_AUDIT.csv"
OWNER_TEMPLATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_FIRST_COEFFICIENT_OWNER_TEMPLATE.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "primitive_deficit_refinement_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4459_primitive_deficit_action_law_or_first_cR2_coefficient_owner_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4458 = SOURCE_DIR / "P8_Y5_R2FR_4458_NEXT_TARGET.csv"
FORMAL_474 = FORMAL / "474-PPC4161-MTS-quadratic-coefficient-normalization-map-or-cR2-zero-selector.md"
STATUS_4458 = SOURCE_DIR / "P8_Y5_R2FR_4458_STATUS.csv"
THEOREM_1823 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1823_PRIMITIVE_DEFICIT_ACTION_LAW_ATTEMPT.csv"
SCALING_1823 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1823_DEFICIT_CONTINUUM_SCALING_AUDIT.csv"
OWNER_1823 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1823_VISIBLE_C2_OWNER_ROW.csv"
DOC_1823 = POST / "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md"
HOLONOMY_1822 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1822_LINEAR_HOLONOMY_PARENT_AXIOM_ATTEMPT.csv"
OWNER_1822 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1822_R2FR_COEFFICIENT_OWNER_ROW.csv"
ZERO_3300 = SOURCE_DIR / "P8_Y5_R2FR_3300_CURVATURE_SQUARED_CONDITIONAL_ZERO_PROOF.csv"
DOC_964 = POST / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"
MOTION_LOAD = POST / "01-motion-load-route-contract.md"
PHASE_VOLUME = POST / "08-phase-volume-reciprocity-origin.md"
HAMILTONIAN_CELL = POST / "09-hamiltonian-radial-cell-derivation.md"
OBSERVER_CONTRACT = POST / "10-observer-map-symplectic-contract.md"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4459_00_next4458", "ref": NEXT_4458, "needle": NEXT_TARGET.replace("4460", "4459").replace("parent-refinement-gauge-signature-or-visible-c2-finite-row", "primitive-deficit-action-law-or-first-cR2-coefficient-owner-value"), "role": "4458 selected primitive deficit/coefficient owner target."},
        {"source_id": "SRC4459_01_formal474", "ref": FORMAL_474, "needle": "primitive deficit-action linearity", "role": "formal 4458 next hinge."},
        {"source_id": "SRC4459_02_status4458", "ref": STATUS_4458, "needle": "basis_map_derived_parent_values_missing", "role": "4458 nonclaim status."},
        {"source_id": "SRC4459_03_deficit1823", "ref": THEOREM_1823, "needle": "DAL1823_2_generic_deficit_cost", "role": "generic deficit cost exposes visible c2."},
        {"source_id": "SRC4459_04_scaling1823", "ref": SCALING_1823, "needle": "DCS1823_1_quadratic", "role": "continuum scaling for quadratic deficit response."},
        {"source_id": "SRC4459_05_owner1823", "ref": OWNER_1823, "needle": "VC21823_1_visible_c2", "role": "visible c2 owner row."},
        {"source_id": "SRC4459_06_doc1823", "ref": DOC_1823, "needle": "Phi''(0)=0", "role": "1823 narrative target."},
        {"source_id": "SRC4459_07_holonomy1822", "ref": HOLONOMY_1822, "needle": "LHA1822_2_same_cell_additivity", "role": "same-cell additivity conditional lemma."},
        {"source_id": "SRC4459_08_owner1822", "ref": OWNER_1822, "needle": "CO1822_1_visible_c2", "role": "R2/fR coefficient owner row."},
        {"source_id": "SRC4459_09_zero3300", "ref": ZERO_3300, "needle": "CZ3300_2_c_R2_zero", "role": "conditional curvature-square zero theorem."},
        {"source_id": "SRC4459_10_doc964", "ref": DOC_964, "needle": "EH + epsilon int sqrt(-g) R^2", "role": "countermodel against easy zero."},
        {"source_id": "SRC4459_11_motion_load", "ref": MOTION_LOAD, "needle": "The contract is to derive `p=1`, not fit it.", "role": "parallel motion-load derivation discipline."},
        {"source_id": "SRC4459_12_phase_volume", "ref": PHASE_VOLUME, "needle": "phase_volume_reciprocity_motivated_not_parent_derived", "role": "parallel cell-preservation route status."},
        {"source_id": "SRC4459_13_hamiltonian", "ref": HAMILTONIAN_CELL, "needle": "generic symplectic or Liouville phase-volume preservation does not derive p=1", "role": "generic preservation rejected."},
        {"source_id": "SRC4459_14_observer", "ref": OBSERVER_CONTRACT, "needle": "It must preserve or constrain the radial observer configuration cell separately", "role": "separate cell law contract."},
        {"source_id": "SRC4459_15_gate", "ref": GATE_PATH, "needle": "def phi_refinement_scan_rows", "role": "4459 refinement gate."},
        {"source_id": "SRC4459_16_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4459"', "role": "4459 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["ref"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(path),
                "local_path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "refinement_theorem": "S_n(delta)=n Phi(delta/n) invariant for all n forces Phi(delta)=k1 delta",
            "parent_refinement_signature_signed": False,
            "first_coefficient_owner_ready": False,
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "math_status": "refinement_linearity_theorem_derived_conditionally",
            "parent_status": "oriented_refinement_equivalence_not_parent_signed",
            "coefficient_status": "visible_c2_and_basis_coefficients_missing",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4459_0",
            "target": NEXT_TARGET,
            "objective": "Either parent-sign the refinement-gauge first-moment action law, or fill the first finite visible c2 / c_R2,c_Ric,c_W coefficient owner row.",
            "derive_first": "prove subdivision/refinement of one physical curvature flux is a gauge/readout-silent equivalence in the MTS parent action",
            "fallback": "source Phi''(0), cell scale, shape factor, and 4458 basis coefficients as nonclaim finite rows",
            "risk": "using refinement linearity as if the parent had signed the refinement premise",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "A refinement-invariance theorem now shows that a primitive first-moment deficit response must be linear, so Phi''(0)=0 conditionally; the MTS parent has not yet signed the refinement premise or finite coefficient values.",
        "current_evidence": "4459 source register, refinement theorem, Phi refinement scan, selector signature audit, coefficient-owner template, claim gates, decision, status, next target and validation CSV.",
        "status": "private_conditional_theorem_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "refinement invariance is a theorem premise, not yet a parent-owned MTS axiom/derivation.",
        "sector": "local_gr_newton_r10",
        "evidence": "4459 source register, refinement theorem, Phi refinement scan, selector signature audit, coefficient-owner template, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "refinement invariance is a theorem premise, not yet a parent-owned MTS axiom/derivation.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(claim_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    current = text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + section.strip() + "\n")


def write_docs() -> None:
    sources = source_rows()
    theorems = theorem_rows()
    scan = phi_refinement_scan_rows()
    signatures = selector_signature_rows()
    owners = coefficient_owner_template_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_rows()
    body = f"""# 475 - PPC4161 Primitive Deficit Refinement Linearity Or First Coefficient Owner Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4459 takes the derivation route first. It proves an exact conditional refinement theorem: if one physical curvature/holonomy deficit can be subdivided into `n` primitive subcells without changing the parent action, then `S_n(delta)=n Phi(delta/n)` must equal `Phi(delta)` for all `n`. Smoothness then forces `Phi(delta)=k1 delta`; in particular `Phi''(0)=0`.

This is stronger than "we prefer a linear deficit cost" and weaker than a public local-GR proof. The parent MTS action still has to sign the oriented-flux/refinement-equivalence premise and the no-second-channel guards.

## Refinement Linearity Theorem

{table(theorems)}

## Phi Refinement Scan

{table(scan)}

## Selector Signature Audit

{table(signatures)}

## First Coefficient Owner Template

{table(owners)}

## Claim Gates

{table(gates)}

## Decision

{table(decisions)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Source Register

{table(sources)}
"""
    write_text(FORMAL_PATH, body)
    packet = f"""# 4459 - Primitive deficit action law or first cR2 coefficient owner value

Private checkpoint. No GitHub action. No public local-GR/R10/PPN claim.

- Proved the exact refinement theorem: `S_n(delta)=n Phi(delta/n)` is invariant for all `n` only when the same-channel primitive response is linear.
- Therefore `Phi''(0)=0` follows if, and only if, the parent signs subdivision/refinement equivalence for one physical oriented curvature flux.
- A finite `delta^2`, `R^2`, Ricci/Weyl, hidden scalar, marker, or memory-tower response remains legal as a separate second channel until excluded or sourced.
- Next: parent-sign the refinement gauge law or fill the first finite coefficient-owner row.

Next target: `{NEXT_TARGET}`

Marker: `{PACKET_MARKER}`
"""
    write_text(DOC_PATH, packet)
    append_marker_section(
        SPINE_PATH,
        MARKER,
        f"""## {MARKER}

The curvature-square survivor now has a real zero-selector theorem candidate. If MTS parent cells are refinement-equivalent first-moment curvature-flux measures, then `S_n(delta)=n Phi(delta/n)=Phi(delta)` forces `Phi(delta)` to be linear and kills `Phi''(0)`. This is not yet a claim: the parent refinement signature, no-second-channel guard, and coefficient-owner fallback remain open.
""",
    )
    append_marker_section(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## {PACKET_MARKER}

4459 proves the conditional refinement-linearity theorem behind the primitive deficit route. It turns the question into one exact parent signature: is primitive curvature cost an oriented refinement-invariant first-moment measure, or is there a separate finite `c2/c_R2/c_Ric/c_W` response channel to source and bound?
""",
    )


def validation_rows() -> List[Dict[str, object]]:
    source = read_csv(SOURCE_REGISTER)
    theorem = read_csv(THEOREM_CSV)
    scan = read_csv(PHI_SCAN_CSV)
    signatures = read_csv(SIGNATURE_CSV)
    owners = read_csv(OWNER_TEMPLATE_CSV)
    gates = read_csv(CLAIM_GATES_CSV)
    checks = [
        ("VAL4459_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in source), "every cited local source path exists"),
        ("VAL4459_1_local_needles_found", all(row["needle_found"] == "True" for row in source), "every cited local source needle is present"),
        ("VAL4459_2_refinement_theorem_written", any(row["theorem_id"] == "RFL4459_0_target" and "Phi''(0)=0" in row["result"] for row in theorem), "refinement theorem row written"),
        ("VAL4459_3_c2_refinement_pressure", any(row["theorem_id"] == "RFL4459_1_c2_rejection" and "1/n" in row["derivation"] for row in theorem), "delta squared refinement pressure written"),
        ("VAL4459_4_phi_scan_orders", len(scan) == 4 and any(row["term_id"] == "PHI4459_2" and row["refinement_invariant"] == "False" for row in scan), "Phi scan separates linear from higher orders"),
        ("VAL4459_5_signature_blocks", all(row["blocks_zero_claim"] == "True" for row in signatures), "all parent signature rows block zero claim until signed"),
        ("VAL4459_6_owner_template_nonclaim", all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in owners), "finite coefficient owner rows remain nonclaim"),
        ("VAL4459_7_claim_gates_safe", all(row["claim_allowed"] == "False" for row in gates), "no claim gate allows local-GR/R10 promotion"),
        ("VAL4459_8_required_blockers_false", any(row["gate_id"] == "CG4459_2_parent_signature" and row["gate_pass"] == "False" for row in gates), "parent signature gate remains explicitly false"),
        ("VAL4459_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-301"),
        ("VAL4459_10_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4459_11_post_doc", DOC_PATH.exists() and PACKET_MARKER in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4459_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4459_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4459_14_next_target", NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4459_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(THEOREM_CSV, theorem_rows())
    write_csv(PHI_SCAN_CSV, phi_refinement_scan_rows())
    write_csv(SIGNATURE_CSV, selector_signature_rows())
    write_csv(OWNER_TEMPLATE_CSV, coefficient_owner_template_rows())
    write_csv(CLAIM_GATES_CSV, claim_gate_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_docs()
    update_claims_register()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
