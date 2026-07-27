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

from local_residual_integration_gate import evaluate_local_residual_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4439"
CLAIM_ID = "L-280"
MARKER = "PPC4161_INTEGRATE_FIXED_BRANCH_EM_ZERO_INTO_LOCAL_RESIDUAL_VECTOR_4439"
PACKET_MARKER = "PPC4161_PACKET_FIXED_BRANCH_EM_ZERO_LOCAL_RESIDUAL_VECTOR_4439"
DECISION = "FIXED_BRANCH_EM_TAIL_DELETED_FROM_LOCAL_RESIDUAL_VECTOR_SOURCE_CHARGE_GEOMETRY_PROJECTION_TAILS_REMAIN"
NEXT_TARGET = "4440-Y5-R2FR-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md"

FORMAL_PATH = FORMAL / "455-PPC4161-integrate-fixed-branch-EM-zero-into-local-residual-vector-or-source-charge-tail.md"
DOC_PATH = POST / "4439-Y5-R2FR-integrate-fixed-branch-EM-zero-into-local-residual-vector-or-source-charge-tail.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4439_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4439_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4439_DERIVATION_ROWS.csv"
LOCAL_RESIDUAL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4439_LOCAL_RESIDUAL_INTEGRATION_INPUT.csv"
LOCAL_RESIDUAL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4439_LOCAL_RESIDUAL_INTEGRATION_OUTPUT.csv"
VECTOR_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4439_LOCAL_RESIDUAL_VECTOR_AFTER_EM.csv"
BLOCKER_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4439_REMAINING_BLOCKER_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4439_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4439_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4439_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4439_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "local_residual_integration_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4439_integrate_fixed_branch_EM_zero_into_local_residual_vector_or_source_charge_tail.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4438 = SOURCE_DIR / "P8_Y5_R2FR_4438_NEXT_TARGET.csv"
ZERO4438 = SOURCE_DIR / "P8_Y5_R2FR_4438_TOTAL_EM_ZERO_ROWS.csv"
SURV4438 = SOURCE_DIR / "P8_Y5_R2FR_4438_OPEN_EM_SURVIVOR_ROWS.csv"
KLEG4438 = SOURCE_DIR / "P8_Y5_R2FR_4438_K_ACTION_SOURCE_LEG_OUTPUT.csv"
FORMAL_454 = FORMAL / "454-PPC4161-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md"
FORMAL_369 = FORMAL / "369-PPC4161-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md"
FORMAL_370 = FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md"
FORMAL_344 = FORMAL / "344-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md"
FORMAL_345 = FORMAL / "345-PPC4161-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md"
FORMAL_346 = FORMAL / "346-PPC4161-coefficient-drift-zero-or-source-backed-tail-bound.md"
FORMAL_190 = FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


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


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4439_00_4438_next", "path": NEXT_4438, "needle": "4439-Y5-R2FR-integrate-fixed-branch-EM-zero", "role": "4438 handoff."},
        {"source_id": "SRC4439_01_454_formal", "path": FORMAL_454, "needle": "ZERO4438_0_total_EM_product", "role": "fixed branch total EM zero."},
        {"source_id": "SRC4439_02_zero4438", "path": ZERO4438, "needle": "ZERO4438_0_total_EM_product", "role": "machine-readable fixed EM zero row."},
        {"source_id": "SRC4439_03_survivor4438", "path": SURV4438, "needle": "SURV4438_3_nonEM_local_residuals", "role": "non-EM local residual survivor row."},
        {"source_id": "SRC4439_04_kleg4438", "path": KLEG4438, "needle": "KLEG4438_0_total_fixed_branch_EM_product_zero", "role": "K action-scale EM product zero row."},
        {"source_id": "SRC4439_05_369_clean_vector", "path": FORMAL_369, "needle": "RV4353_0_clean_private", "role": "clean local vector after private owner-tail deletion."},
        {"source_id": "SRC4439_06_370_source_charge", "path": FORMAL_370, "needle": "epsilon_Gsrc <=", "role": "source-charge/coupling residual envelope."},
        {"source_id": "SRC4439_07_344_geometry", "path": FORMAL_344, "needle": "F4328_4_geometry_core_update", "role": "geometry core tails before EM-Hodge reduction."},
        {"source_id": "SRC4439_08_345_hodge", "path": FORMAL_345, "needle": "F4329_4_geometry_core_update", "role": "same-Hodge EM reduction and open EM tails."},
        {"source_id": "SRC4439_09_346_coeff", "path": FORMAL_346, "needle": "F4330_6_geometry_core_update", "role": "coefficient reduction and remaining geometry core."},
        {"source_id": "SRC4439_10_190_selector", "path": FORMAL_190, "needle": "CONDITIONAL_PARENT_ACTION_SELECTOR_THEOREM_DERIVED_GLOBAL_ADOPTION_NOT_PROVED_LOCAL_BRANCH_QUARANTINED", "role": "parent selector quarantine."},
        {"source_id": "SRC4439_11_295_noneh", "path": FORMAL_295, "needle": "RESIDUAL_EFT_VECTOR_REDUCED_TO_PRIVATE_ZERO_SUBSET", "role": "non-EH/EFT residual pack."},
        {"source_id": "SRC4439_12_gate", "path": GATE_PATH, "needle": "def evaluate_local_residual_row", "role": "4439 local residual integration gate."},
        {"source_id": "SRC4439_13_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4439\"", "role": "4439 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(source_path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(source_path),
                "path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "line_number": line_of(source_path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "LRI4439_0_subtraction_law",
            "claim": "The fixed-branch EM residual product can be subtracted from the already-clean private local residual vector.",
            "derivation": "4353 gives Delta_local_after_owner = Delta_nonowner_remaining after the private owner channel is deleted. Split Delta_nonowner_remaining into Delta_EM_fixed + Delta_EM_open + epsilon_Gsrc + epsilon_geom_projection + epsilon_nonEH + epsilon_parent_selector + epsilon_empirical. 4438 gives Delta_EM_fixed=0 only on the fixed q-basic same-Hodge static closed-collar branch.",
            "consequence": "Delta_local_fixed_after_EM = epsilon_Gsrc + epsilon_geom_projection + epsilon_nonEH + epsilon_parent_selector + epsilon_empirical on that branch.",
            "status": "FIXED_BRANCH_EM_SUBTRACTED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LRI4439_1_open_EM_firewall",
            "claim": "Open radiation, readout regeneration and global/dynamic EM are not deleted by the fixed-branch subtraction.",
            "derivation": "4438 routes open EM to boundary/source-energy rows and retains readout/EFT/global-dynamic EM as explicit counterbranches. Therefore the open branch vector is Delta_local_open_EM = Delta_local_fixed_after_EM + Delta_EM_open_dynamic.",
            "consequence": "No Poynting/vector-wave route is erased; it remains a sourced finite tail outside the static closed-collar branch.",
            "status": "OPEN_EM_RETAINED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LRI4439_2_no_local_GR_claim",
            "claim": "The local GR/Newton/PPN claim remains blocked after the fixed EM tail is removed.",
            "derivation": "370 keeps epsilon_Gsrc active until source charge, H_tau/MHref, kappa/source-measure and same-branch integrability clauses close. 344-346 keep readout-frame, terminal/projection, Xi_src_hidden and open coefficient/EM branches. 190 keeps the parent selector private; 295 keeps non-EH/EFT finite rows.",
            "consequence": "4439 is real narrowing, not a final local-GR proof.",
            "status": "NONEM_BLOCKERS_REMAIN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LRI4439_3_next_source_charge",
            "claim": "The next highest-leverage target is the source-charge/coupling tail epsilon_Gsrc.",
            "derivation": "With the clean owner channel and fixed-branch EM product removed, the source mass/coupling bridge is now the leading structural gate for Newton/GR reduction, provided geometry/readout/projection tails stay explicitly carried.",
            "consequence": NEXT_TARGET,
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
        },
    ]


def local_residual_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "LRI4439_0_clean_fixed_branch_after_EM",
            "branch": "private clean fixed q-basic same-Hodge static closed-collar branch",
            "owner_tail_deleted": True,
            "fixed_branch_EM_zero": True,
            "open_EM_retained": True,
            "source_charge_closed": False,
            "coupling_no_drift_closed": False,
            "geometry_projection_closed": False,
            "nonEH_closed": False,
            "parent_selector_adopted": False,
            "empirical_projection_ready": False,
            "source_path": str(FORMAL_369),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "Fixed EM tail subtracts cleanly, but non-EM blockers remain.",
        },
        {
            "row_id": "LRI4439_1_open_dynamic_EM_branch",
            "branch": "open radiation, readout-regenerated or global/dynamic EM branch",
            "owner_tail_deleted": True,
            "fixed_branch_EM_zero": False,
            "open_EM_retained": True,
            "source_charge_closed": False,
            "coupling_no_drift_closed": False,
            "geometry_projection_closed": False,
            "nonEH_closed": False,
            "parent_selector_adopted": False,
            "empirical_projection_ready": False,
            "source_path": str(FORMAL_454),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Open EM is carried as Delta_EM_open_dynamic, not deleted.",
        },
        {
            "row_id": "LRI4439_2_source_charge_conditional_branch",
            "branch": "conditional H_tau/MHref and calibrated G source-charge branch",
            "owner_tail_deleted": True,
            "fixed_branch_EM_zero": True,
            "open_EM_retained": True,
            "source_charge_closed": False,
            "coupling_no_drift_closed": False,
            "geometry_projection_closed": False,
            "nonEH_closed": False,
            "parent_selector_adopted": False,
            "empirical_projection_ready": False,
            "source_path": str(FORMAL_370),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Conditional Newton bridge exists but epsilon_Gsrc is still active.",
        },
        {
            "row_id": "LRI4439_3_public_selector_branch",
            "branch": "public/global parent selector branch",
            "owner_tail_deleted": False,
            "fixed_branch_EM_zero": False,
            "open_EM_retained": True,
            "source_charge_closed": False,
            "coupling_no_drift_closed": False,
            "geometry_projection_closed": False,
            "nonEH_closed": False,
            "parent_selector_adopted": False,
            "empirical_projection_ready": False,
            "source_path": str(FORMAL_190),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Public/global adoption remains quarantined.",
        },
    ]


def vector_rows() -> List[Dict[str, object]]:
    return [
        {
            "vector_id": "RV4439_0_fixed_clean_private_after_EM",
            "domain": "private fixed clean local branch",
            "before": "Delta_local_after_owner = Delta_EM_fixed + Delta_EM_open + epsilon_Gsrc + epsilon_geom_projection + epsilon_nonEH + epsilon_parent_selector + epsilon_empirical",
            "imported_zero": "Delta_EM_fixed=0 from 4438",
            "after": "Delta_local_fixed_after_EM = epsilon_Gsrc + epsilon_geom_projection + epsilon_nonEH + epsilon_parent_selector + epsilon_empirical",
            "claim_status": "NONCLAIM_REMAINING_GATES_EXPLICIT",
            "source_path": str(FORMAL_369),
            "valid_for_claim": False,
        },
        {
            "vector_id": "RV4439_1_open_EM_or_dynamic",
            "domain": "open radiative/readout/global EM branch",
            "before": "Delta_EM_open_dynamic is retained by 4438",
            "imported_zero": "no fixed-branch zero applies outside the static closed-collar domain",
            "after": "Delta_local_open_EM = Delta_local_fixed_after_EM + Delta_EM_open_dynamic",
            "claim_status": "OPEN_EM_BOUND_OR_SOURCE_VALUE_REQUIRED",
            "source_path": str(FORMAL_454),
            "valid_for_claim": False,
        },
        {
            "vector_id": "RV4439_2_public_parent_selector",
            "domain": "public/global parent selector branch",
            "before": "PPC4161 branch remains private/quarantined",
            "imported_zero": "no global branch adoption is imported from 4438",
            "after": "public local GR residual vector remains unclaimed until parent selector and arena projections close",
            "claim_status": "PUBLIC_CLAIM_BLOCKED",
            "source_path": str(FORMAL_190),
            "valid_for_claim": False,
        },
    ]


def blocker_rows() -> List[Dict[str, object]]:
    return [
        {"blocker_id": "BLK4439_0_source_charge_Htau_MHref", "symbol": "epsilon_Gsrc", "why_remains": "source charge, H_tau/MHref, kappa/source-measure and integrability clauses are conditional, not closed", "needed_to_close": "prove same-branch source-charge closure or source first finite epsilon_Gsrc tail", "source_path": str(FORMAL_370), "priority": "NEXT_HIGH_LEVERAGE", "valid_for_claim": False},
        {"blocker_id": "BLK4439_1_parent_selector_adoption", "symbol": "S_parent selector", "why_remains": "local selector is still private/quarantined and not a global MTS adoption theorem", "needed_to_close": "parent action selector signed globally or branch explicitly quarantined for every local claim", "source_path": str(FORMAL_190), "priority": "PUBLIC_PROMOTION_GATE", "valid_for_claim": False},
        {"blocker_id": "BLK4439_2_geometry_readout_terminal_Xi", "symbol": "epsilon_geom_projection + Xi_src_hidden", "why_remains": "readout-frame, terminal projection and hidden source return survive prior geometry reductions", "needed_to_close": "prove natural readout/projection zero or write finite source-backed projection tails", "source_path": str(FORMAL_346), "priority": "GEOMETRY_PROJECTION_GATE", "valid_for_claim": False},
        {"blocker_id": "BLK4439_3_nonEH_residual_EFT", "symbol": "epsilon_nonEH", "why_remains": "residual EFT pack is reduced to private zero subset and finite bound targets, not public zero", "needed_to_close": "parent-sign non-EH zeros or source local test coefficients", "source_path": str(FORMAL_295), "priority": "EFT_RESIDUAL_GATE", "valid_for_claim": False},
        {"blocker_id": "BLK4439_4_empirical_projection_constants", "symbol": "Pi_a/local arena maps", "why_remains": "R10/PPN/clock/orbital rows still need real projection constants, units and no-cancellation runners", "needed_to_close": "source projection constants and run local arena comparators", "source_path": str(FORMAL_369), "priority": "EMPIRICAL_GATE", "valid_for_claim": False},
        {"blocker_id": "BLK4439_5_open_EM_branch", "symbol": "Delta_EM_open_dynamic", "why_remains": "open radiation, readout regeneration and global/dynamic EM are outside the fixed static closed-collar zero", "needed_to_close": "prove closed-collar silence in target arena or source E_rad/P_rad/readout/dynamic EM rows", "source_path": str(FORMAL_454), "priority": "OPEN_BRANCH_GATE", "valid_for_claim": False},
    ]


def claim_gate_rows(outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    output_by_id = {row["row_id"]: row for row in outputs}
    no_output_claim = not any(row.get("valid_for_claim") == "True" for row in outputs)
    return [
        {"gate_id": "CG4439_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register is path-backed."},
        {"gate_id": "CG4439_1_fixed_EM_subtracted", "claim": "fixed branch EM residual tail deleted from clean vector", "passed": output_by_id["LRI4439_0_clean_fixed_branch_after_EM"].get("current_status") == "FIXED_BRANCH_EM_DELETED_NONEM_BLOCKERS_REMAIN", "valid_for_claim": False, "detail": "Subtraction succeeds only as nonclaim branch narrowing."},
        {"gate_id": "CG4439_2_open_EM_retained", "claim": "open/dynamic EM branch retained", "passed": output_by_id["LRI4439_1_open_dynamic_EM_branch"].get("current_status") == "OPEN_EM_BRANCH_RETAINED", "valid_for_claim": False, "detail": "Poynting/radiative/readout branch is not erased."},
        {"gate_id": "CG4439_3_vector_rewired", "claim": "local residual vector rewritten after fixed EM zero", "passed": "RV4439_0_fixed_clean_private_after_EM" in text(VECTOR_ROWS), "valid_for_claim": False, "detail": "Residual vector after EM has explicit non-EM terms."},
        {"gate_id": "CG4439_4_source_charge_retained", "claim": "source-charge/coupling blocker retained", "passed": "BLK4439_0_source_charge_Htau_MHref" in text(BLOCKER_ROWS), "valid_for_claim": False, "detail": "epsilon_Gsrc is next high-leverage target."},
        {"gate_id": "CG4439_5_geometry_blockers_retained", "claim": "geometry/projection/non-EH blockers retained", "passed": "BLK4439_2_geometry_readout_terminal_Xi" in text(BLOCKER_ROWS) and "BLK4439_3_nonEH_residual_EFT" in text(BLOCKER_ROWS), "valid_for_claim": False, "detail": "Readout/projection/EFT tails remain carried."},
        {"gate_id": "CG4439_6_no_public_claim", "claim": "4439 emits no local-GR/Newton/PPN public claim", "passed": no_output_claim, "valid_for_claim": False, "detail": "Every output row remains nonclaim."},
        {"gate_id": "CG4439_7_next_target_written", "claim": "next target selected", "passed": NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4439_0",
            "decision": DECISION,
            "summary": "4439 integrates the 4438 fixed-branch total EM zero into the 4353 clean local residual vector. The fixed static same-Hodge EM product is removed from the private vector, but source charge, coupling/no-drift, parent selector, geometry/readout/projection, non-EH/EFT and empirical arena projections remain explicit blockers. Open radiative/readout/global EM is retained outside the fixed branch.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4439_0_fixed_EM", "object": "Delta_EM_fixed", "status": "DELETED_FROM_FIXED_CLEAN_VECTOR", "detail": "Only in fixed q-basic same-Hodge static closed-collar branch.", "valid_for_claim": False},
        {"status_id": "STAT4439_1_open_EM", "object": "Delta_EM_open_dynamic", "status": "RETAINED_OUTSIDE_FIXED_BRANCH", "detail": "Open radiation/readout/global EM still needs source or proof.", "valid_for_claim": False},
        {"status_id": "STAT4439_2_source_charge", "object": "epsilon_Gsrc", "status": "NEXT_HIGH_LEVERAGE_TAIL", "detail": "H_tau/MHref/source-measure/coupling bridge is the next target.", "valid_for_claim": False},
        {"status_id": "STAT4439_3_local_GR", "object": "local GR/Newton/PPN pass", "status": "NOT_CLAIMED", "detail": "EM closure alone is not enough.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4439_0",
            "target": NEXT_TARGET,
            "objective": "Try to close the H_tau/MHref source-charge and calibrated coupling tail epsilon_Gsrc now that the fixed EM residual has been removed from the private clean vector.",
            "derive_first": "prove the same parent-owned source charge, reference subtraction, tau/frame/surface lock, and source-blind kappa_eff all close on one branch",
            "fallback": "write the first explicit finite epsilon_Gsrc tail value/bound rows for R10, PPN, clocks and orbital arenas",
            "avoid": "claiming local GR from the 4439 vector rewrite; treating calibrated G_N as a prediction; using open EM zero outside the static closed-collar branch",
            "valid_for_claim": False,
        }
    ]


def build_doc(
    sources: Sequence[Mapping[str, object]],
    outputs: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 455 PPC4161 integrate fixed-branch EM zero into local residual vector or source-charge tail

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4439 is a useful tightening, not a finish-line claim.

```text
Delta_local_after_owner
  = Delta_EM_fixed
  + Delta_EM_open
  + epsilon_Gsrc
  + epsilon_geom_projection
  + epsilon_nonEH
  + epsilon_parent_selector
  + epsilon_empirical

4438 fixed branch:
Delta_EM_fixed = 0

Therefore:
Delta_local_fixed_after_EM
  = epsilon_Gsrc
  + epsilon_geom_projection
  + epsilon_nonEH
  + epsilon_parent_selector
  + epsilon_empirical
```

- The fixed q-basic same-Hodge static closed-collar EM product is now deleted from the private clean local residual vector.
- Open radiation, readout/EFT regeneration and global/dynamic EM remain explicit source/boundary tails.
- Local GR/Newton/PPN is still not claimed because the source-charge/coupling, parent selector, geometry/projection, non-EH and empirical projection gates remain open.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Local Residual Integration Gate

{table(outputs)}

## Local Residual Vector After EM

{table(vector_rows())}

## Remaining Blocker Rows

{table(blocker_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Status

{table(status_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4439 Y5 R2FR integrate fixed-branch EM zero into local residual vector or source-charge tail

Private checkpoint generated at `{STAMP}`.

Formal mirror: `{FORMAL_PATH}`

Decision: `{DECISION}`

Summary:
- Fixed-branch EM tail is removed from the private clean local residual vector.
- Open EM branches are explicitly retained.
- Source charge/coupling, parent selector, geometry/projection, non-EH/EFT and empirical projections still block local-GR/Newton/PPN promotion.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "em_local_gr",
        "claim": "4439 integrates the fixed-branch total EM zero into the clean private local residual vector: Delta_EM_fixed is deleted on the fixed q-basic same-Hodge static closed-collar branch, while source-charge/coupling, geometry/projection, parent selector, non-EH/EFT and empirical projection tails remain explicit.",
        "current_evidence": "4439 source register, derivation rows, local residual integration gate, vector rows, blocker rows, claim gates, decision, status, next target and validation CSV.",
        "status": "fixed_branch_EM_tail_deleted_from_clean_residual_vector_nonEM_blockers_remain_nonclaim",
        "next_test": "Close H_tau/MHref source-charge and calibrated coupling tail epsilon_Gsrc or write first finite source-backed tail value.",
        "key_risk": "Claiming local GR from EM closure alone; deleting open EM branches; using the static closed-collar zero outside its domain.",
        "sector": "em_local_gr",
        "evidence": "4439 source register, derivation rows, local residual integration gate, vector rows, blocker rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Close H_tau/MHref source-charge and calibrated coupling tail epsilon_Gsrc or write first finite source-backed tail value.",
        "risk": "Claiming local GR from EM closure alone; deleting open EM branches; using the static closed-collar zero outside its domain.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(new_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    body = existing.rstrip() + "\n\n" + section.strip() + "\n"
    write_text(path, body)


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Residual Update - Fixed Branch EM Tail Integration

Marker: `{MARKER}`  
Source checkpoint: `4439-Y5-R2FR-integrate-fixed-branch-EM-zero-into-local-residual-vector-or-source-charge-tail.md`  
Claim register row: `{CLAIM_ID}`

Fixed-branch residual rewrite:

```text
Delta_local_fixed_after_EM
  = epsilon_Gsrc
  + epsilon_geom_projection
  + epsilon_nonEH
  + epsilon_parent_selector
  + epsilon_empirical
```

This deletes only `Delta_EM_fixed` in the fixed q-basic same-Hodge static closed-collar branch. Open EM, source-charge/coupling, projection, non-EH and empirical tails remain nonclaim.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Fixed Branch EM Tail Integration

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4439-Y5-R2FR-integrate-fixed-branch-EM-zero-into-local-residual-vector-or-source-charge-tail.md`

The 4438 fixed EM zero has been wired into the local residual vector. The clean private branch can now carry `Delta_EM_fixed=0`, but the packet still requires `epsilon_Gsrc`, geometry/projection tails, parent selector adoption, non-EH/EFT residual control and empirical arena projections before any local-GR/Newton/PPN promotion.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    outputs = {row["row_id"]: row for row in rows_from(LOCAL_RESIDUAL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in outputs.values())
    checks = [
        ("VAL4439_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4439_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4439_2_fixed_vector_integrated", outputs["LRI4439_0_clean_fixed_branch_after_EM"].get("current_status") == "FIXED_BRANCH_EM_DELETED_NONEM_BLOCKERS_REMAIN", "fixed branch EM zero integrated with non-EM blockers retained"),
        ("VAL4439_3_open_EM_retained", outputs["LRI4439_1_open_dynamic_EM_branch"].get("current_status") == "OPEN_EM_BRANCH_RETAINED", "open/dynamic EM branch retained"),
        ("VAL4439_4_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4439_5_vector_rows", len(rows_from(VECTOR_ROWS)) == 3 and "RV4439_0_fixed_clean_private_after_EM" in text(VECTOR_ROWS), "local residual vector rows written"),
        ("VAL4439_6_blocker_rows", len(rows_from(BLOCKER_ROWS)) == 6 and "BLK4439_0_source_charge_Htau_MHref" in text(BLOCKER_ROWS), "remaining blocker rows written"),
        ("VAL4439_7_claim_gate_no_claim", any(row["gate_id"] == "CG4439_6_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4439_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-280"),
        ("VAL4439_9_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4439_10_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4439_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4439_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4439_13_next_gate", any(row["gate_id"] == "CG4439_7_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4439_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4439_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(LOCAL_RESIDUAL_INPUT, local_residual_input_rows())
    write_csv(LOCAL_RESIDUAL_OUTPUT, evaluate_local_residual_rows(LOCAL_RESIDUAL_INPUT))
    write_csv(VECTOR_ROWS, vector_rows())
    write_csv(BLOCKER_ROWS, blocker_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    outputs = rows_from(LOCAL_RESIDUAL_OUTPUT)
    gates = claim_gate_rows(outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
