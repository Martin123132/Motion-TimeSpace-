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

from parent_refinement_signature_gate import (  # noqa: E402
    as_float,
    claim_gate_rows,
    finite_c2_bound_rows,
    read_csv,
    refinement_dichotomy_rows,
    refinement_signature_contract_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4460"
CLAIM_ID = "L-302"
MARKER = "PPC4161_PARENT_REFINEMENT_GAUGE_SIGNATURE_OR_VISIBLE_C2_FINITE_ROW_4460"
PACKET_MARKER = "PPC4161_PACKET_PARENT_REFINEMENT_GAUGE_SIGNATURE_OR_VISIBLE_C2_FINITE_ROW_4460"
DECISION = "REFINEMENT_ZERO_REQUIRES_PARENT_QUOTIENT_PROJECTIVE_SIGNATURE_FINITE_C2_BRANCH_RETAINED_NONCLAIM"
NEXT_TARGET = "4461-Y5-R2FR-connection-hinge-refinement-owner-or-c2-scalaron-map.md"

FORMAL_PATH = FORMAL / "476-PPC4161-parent-refinement-gauge-signature-or-visible-c2-finite-row.md"
DOC_PATH = POST / "4460-Y5-R2FR-parent-refinement-gauge-signature-or-visible-c2-finite-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4460_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4460_SOURCE_REGISTER.csv"
SIGNATURE_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_PARENT_REFINEMENT_SIGNATURE_CONTRACT.csv"
DICHOTOMY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_REFINEMENT_DICHOTOMY.csv"
FINITE_C2_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_VISIBLE_C2_FINITE_ROW_TEMPLATE.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_refinement_signature_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4460_parent_refinement_gauge_signature_or_visible_c2_finite_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4459 = SOURCE_DIR / "P8_Y5_R2FR_4459_NEXT_TARGET.csv"
FORMAL_475 = FORMAL / "475-PPC4161-primitive-deficit-refinement-linearity-or-first-coefficient-owner-row.md"
SIGNATURE_4459 = SOURCE_DIR / "P8_Y5_R2FR_4459_SELECTOR_SIGNATURE_AUDIT.csv"
PHI_SCAN_4459 = SOURCE_DIR / "P8_Y5_R2FR_4459_PHI_REFINEMENT_SCAN.csv"
REGION_4458 = SOURCE_DIR / "P8_Y5_R2FR_4458_MTS_BASIS_COEFFICIENT_REGION.csv"
BOUNDS_4457 = SOURCE_DIR / "P8_Y5_R2FR_4457_COEFFICIENT_REGION_BOUNDS.csv"
DOC_340 = POST / "340-full-cell-equivalence-gauge-redundancy-gate.md"
DOC_341 = POST / "341-indistinguishable-cell-quotient-parent-action-gate.md"
DOC_1824 = POST / "1824-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md"
DOC_1826 = POST / "1826-Y5-R2FR-log-holonomy-action-owner-or-trace-norm-c2-prior.md"
DOC_1827 = POST / "1827-Y5-R2FR-Palatini-Regge-field-match-or-c2-scalaron-map.md"
DOC_2148 = POST / "2148-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md"
DOC_2149 = POST / "2149-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md"
CELL_CURRENT_11 = POST / "11-cell-current-origin-attempt.md"


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
        {"source_id": "SRC4460_00_next4459", "ref": NEXT_4459, "needle": "4460-Y5-R2FR-parent-refinement-gauge-signature-or-visible-c2-finite-row.md", "role": "4459 selected parent refinement signature or finite c2 row."},
        {"source_id": "SRC4460_01_formal475", "ref": FORMAL_475, "needle": "S_n(delta)=n Phi(delta/n)", "role": "4459 refinement theorem."},
        {"source_id": "SRC4460_02_sig4459", "ref": SIGNATURE_4459, "needle": "SIG4459_1_refinement_equivalence", "role": "parent refinement-equivalence blocker."},
        {"source_id": "SRC4460_03_scan4459", "ref": PHI_SCAN_4459, "needle": "PHI4459_2", "role": "higher-order terms fail refinement invariance."},
        {"source_id": "SRC4460_04_region4458", "ref": REGION_4458, "needle": "REG4458_1_no_Riemann_basis", "role": "finite basis coefficient fallback map."},
        {"source_id": "SRC4460_05_bounds4457", "ref": BOUNDS_4457, "needle": "QB4457_0_scalar_D0", "role": "D0 coefficient bound for finite row pressure."},
        {"source_id": "SRC4460_06_cell340", "ref": DOC_340, "needle": "label symmetry alone is not enough", "role": "symmetry versus gauge distinction."},
        {"source_id": "SRC4460_07_cell341", "ref": DOC_341, "needle": "the parent configuration space is the quotient R^27 / S27", "role": "quotient state-space route."},
        {"source_id": "SRC4460_08_phi1824", "ref": DOC_1824, "needle": "Signed-deficit oddness would kill", "role": "conditional oddness zero route."},
        {"source_id": "SRC4460_09_log1826", "ref": DOC_1826, "needle": "Palatini/Regge-shaped action", "role": "log-holonomy/action-owner fork."},
        {"source_id": "SRC4460_10_field1827", "ref": DOC_1827, "needle": "MISSING_CONNECTION_COMPATIBILITY", "role": "connection/hinge field-match blocker."},
        {"source_id": "SRC4460_11_frontier2148", "ref": DOC_2148, "needle": "connection + hinge ownership", "role": "current Phi/c2 frontier."},
        {"source_id": "SRC4460_12_frontier2149", "ref": DOC_2149, "needle": "distortion equation", "role": "geometry owner failure becomes residual-vector branch."},
        {"source_id": "SRC4460_13_cell_current11", "ref": CELL_CURRENT_11, "needle": "gives a Ward identity, not R_AB=0", "role": "current conservation alone insufficient."},
        {"source_id": "SRC4460_14_gate", "ref": GATE_PATH, "needle": "def refinement_signature_contract_rows", "role": "4460 refinement signature gate."},
        {"source_id": "SRC4460_15_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4460"', "role": "4460 generator script."},
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


def d0_bound() -> float | None:
    try:
        bounds = read_csv(BOUNDS_4457)
    except FileNotFoundError:
        return None
    scalar = next((row for row in bounds if row.get("bound_id") == "QB4457_0_scalar_D0"), None)
    if scalar is None:
        return None
    return as_float(scalar.get("coefficient_upper_bound_m2"))


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "signature_result": "quotient/projective refinement signature written but not parent-derived",
            "zero_selector_signed": False,
            "finite_c2_score_ready": False,
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
            "refinement_status": "exact_signature_contract_written_parent_origin_open",
            "coefficient_status": "finite_c2_basis_branch_retained_but_unsourced",
            "geometry_status": "connection_hinge_owner_frontier_retained",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4460_0",
            "target": NEXT_TARGET,
            "objective": "Derive the connection/hinge owner needed to make refinement flux physical and Palatini/Regge-like, or turn finite c2 into a scalaron/local-bound map.",
            "derive_first": "prove Gamma_eff/omega_obs, Log(U_h), and B_h/A_h are parent-owned under refinement rather than imported EH/Regge notation",
            "fallback": "fill c2_visible, ell_cell, shape_factor, c_R2_eff, scalaron coupling/range, PPN/R10/clock/orbital projection rows",
            "risk": "treating quotient/refinement symmetry or Palatini notation as parent ownership",
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
        "claim": "The refinement-zero route now has an exact parent-signature contract: MTS must own quotient/projective refinement equivalence and a cylindrical first-moment action, otherwise finite c2/curvature-square rows survive.",
        "current_evidence": "4460 source register, parent refinement signature contract, refinement dichotomy, finite c2 row template, claim gates, decision, status, next target and validation CSV.",
        "status": "private_signature_contract_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "cell symmetry or Palatini/Regge notation may be mistaken for a parent-derived refinement quotient.",
        "sector": "local_gr_newton_r10",
        "evidence": "4460 source register, parent refinement signature contract, refinement dichotomy, finite c2 row template, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "cell symmetry or Palatini/Regge notation may be mistaken for a parent-derived refinement quotient.",
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
    contracts = refinement_signature_contract_rows()
    dichotomy = refinement_dichotomy_rows()
    finite = finite_c2_bound_rows(d0_bound())
    gates = claim_gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_rows()
    body = f"""# 476 - PPC4161 Parent Refinement Gauge Signature Or Visible c2 Finite Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4460 takes the 4459 theorem and asks what must be true in the parent MTS action for it to count. The answer is not "cells are symmetric." The parent must own a quotient/projective refinement structure: refined and unrefined descriptions of the same physical curvature flux must be the same physical state, and the action must be cylindrical under the refinement map.

That signature is now explicit, but not parent-derived. Therefore the visible `c2` / curvature-square branch remains finite and nonclaim until either the quotient-refinement signature closes or the coefficient branch is sourced and bounded.

## Parent Refinement Signature Contract

{table(contracts)}

## Refinement Dichotomy

{table(dichotomy)}

## Visible c2 Finite Row Template

{table(finite)}

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
    packet = f"""# 4460 - Parent refinement gauge signature or visible c2 finite row

Private checkpoint. No GitHub action. No public local-GR/R10/PPN/Newton claim.

- The exact parent signature is now written: refinement must be quotient/projective gauge, not mere cell-label symmetry.
- If the signature closes, 4459 can zero the same-channel visible `c2` response.
- If it does not close, primitive grains, trace/norm holonomy costs, or independent density-squared channels make finite `c2/c_R2/c_Ric/c_W` rows mandatory.
- Current corpus does not parent-sign the quotient/projective action, connection/hinge owner, or no-second-channel clauses.

Next target: `{NEXT_TARGET}`

Marker: `{PACKET_MARKER}`
"""
    write_text(DOC_PATH, packet)
    append_marker_section(
        SPINE_PATH,
        MARKER,
        f"""## {MARKER}

The refinement-zero route now has a parent-signature contract rather than a vibe: MTS must define physical local geometry on a quotient/projective refinement state space and a cylindrical first-moment action. Cell symmetry alone is insufficient. Since the signature is not parent-signed, finite `c2/c_R2/c_Ric/c_W` rows remain the honest fallback.
""",
    )
    append_marker_section(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## {PACKET_MARKER}

4460 converts the 4459 refinement theorem into a parent-action gate. Exact zero needs quotient/projective refinement equivalence, cylindrical action, oriented flux additivity, no physical cell marker/grain, connection/hinge ownership, and no second channel. Otherwise the branch becomes finite `c2`/curvature-square residual scoring.
""",
    )


def validation_rows() -> List[Dict[str, object]]:
    source = read_csv(SOURCE_REGISTER)
    contracts = read_csv(SIGNATURE_CONTRACT_CSV)
    dichotomy = read_csv(DICHOTOMY_CSV)
    finite = read_csv(FINITE_C2_CSV)
    gates = read_csv(CLAIM_GATES_CSV)
    checks = [
        ("VAL4460_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in source), "every cited local source path exists"),
        ("VAL4460_1_local_needles_found", all(row["needle_found"] == "True" for row in source), "every cited local source needle is present"),
        ("VAL4460_2_signature_rows", len(contracts) >= 6 and any(row["contract_id"] == "RGC4460_1_cylindrical_action" for row in contracts), "refinement signature contract rows written"),
        ("VAL4460_3_blocks_zero_claim", all(row["blocks_zero_claim"] == "True" for row in contracts), "all signature clauses block zero claim until signed"),
        ("VAL4460_4_dichotomy", len(dichotomy) >= 4 and any(row["case_id"] == "DICH4460_2_physical_grain_cutoff" for row in dichotomy), "refinement dichotomy includes finite-grain fallback"),
        ("VAL4460_5_finite_rows_nonclaim", all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in finite), "finite c2 rows remain nonclaim"),
        ("VAL4460_6_claim_gates_safe", all(row["claim_allowed"] == "False" for row in gates), "no claim gate allows local-GR/R10 promotion"),
        ("VAL4460_7_parent_gate_false", any(row["gate_id"] == "CG4460_2_parent_signed" and row["gate_pass"] == "False" for row in gates), "parent signature gate remains explicitly false"),
        ("VAL4460_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-302"),
        ("VAL4460_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4460_10_post_doc", DOC_PATH.exists() and PACKET_MARKER in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4460_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4460_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4460_13_next_target", NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4460_14_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(SIGNATURE_CONTRACT_CSV, refinement_signature_contract_rows())
    write_csv(DICHOTOMY_CSV, refinement_dichotomy_rows())
    write_csv(FINITE_C2_CSV, finite_c2_bound_rows(d0_bound()))
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
