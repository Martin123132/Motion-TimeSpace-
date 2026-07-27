from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4325"
CLAIM_ID = "L-166"
BRANCH = "MTS_R2FR_Y5_DQ_TAU_REFERENCE_HPERP_ZERO_OR_CLOCK_TAIL_BOUND_4325"
DECISION = "TAU_REFERENCE_HPERP_ZERO_LIFTED_FOR_SINGLE_PARENT_TIME_FRAME_BRANCH_CLOCK_TAIL_BOUND_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_TAU_REFERENCE_HPERP_ZERO_OR_CLOCK_TAIL_BOUND_4325"
PACKET_MARKER = "PPC4161_PACKET_DQ_TAU_REFERENCE_HPERP_ZERO_OR_CLOCK_TAIL_BOUND_4325"
NEXT_TARGET = "4326-Y5-R2FR-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md"

FORMAL_PATH = FORMAL / "341-PPC4161-Dq-tau-reference-Hperp-zero-or-clock-tail-bound.md"
DOC_PATH = POST / "4325-Y5-R2FR-Dq-tau-reference-Hperp-zero-or-clock-tail-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4325_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4325_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4324_NEXT_TARGET.csv",
        "Dq_tau[Hperp]",
        "4324 handoff selecting tau/reference row.",
    ),
    "SRC4325_01_tau_lock": (
        FORMAL / "232-PPC4161-tau-surface-frame-lock-or-bound.md",
        "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout",
        "4216 single parent-owned time/surface/frame lock.",
    ),
    "SRC4325_02_tau_fallback": (
        FORMAL / "232-PPC4161-tau-surface-frame-lock-or-bound.md",
        "R_clock_readout",
        "4216 fallback clock/frame/surface residual envelope.",
    ),
    "SRC4325_03_ref_lock": (
        FORMAL / "231-PPC4161-reference-lock-curl-zero-or-bound.md",
        "no orbital `GM`, PPN, R10, clock, or source residual is used to choose `H_ref`",
        "4215 reference lock no-post-fit clause.",
    ),
    "SRC4325_04_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "Ordinary matter, EM stress, clocks, rods and source readouts must also factor through q",
        "4177 quotient naturality includes clocks/rods/source readouts.",
    ),
    "SRC4325_05_charge_owner": (
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "tau_source=tau_charge=tau_clock=tau_readout",
        "4211 source-charge owner requires same tau and observed coframe.",
    ),
    "SRC4325_06_component": (
        FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md",
        "Dq_tau[Hperp]",
        "4320 tau component status.",
    ),
    "SRC4325_07_source_readout": (
        FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md",
        "L_xi epsilon_tau",
        "4324 source-readout row to simplify after tau zero.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4325 lifts the 4216 tau/surface/frame lock to the Hperp Dq_tau component. If the local packet selects one "
            "parent-owned time generator before variation, tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout, "
            "uses one fixed or tau-dragged surface family, one observed coframe e_obs=e_bar(q), common-mode units/orientation, "
            "and no clock/PPN/orbital/source residual is used to choose the reference, then Dq_tau[Hperp]=0 and epsilon_tau=0 "
            "inside the standard branch. If any clause fails, the retained clock/reference tail is "
            "epsilon_tau <= R_tau_split + R_surface_motion + R_frame_coframe + R_clock_readout + R_orbital_readout + R_units "
            "+ R_ref_fit. This deletes the L_xi epsilon_tau term from the 4324 source-readout envelope only in the locked branch. "
            "No local GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4325 source register, tau lock audit, clock-tail ledger, simplified formulas, component update, runner, firewall, "
            "decision, status, next-target and validation CSV."
        ),
        "private_tau_reference_Hperp_standard_branch_zero_with_clock_tail_firewall_nonclaim",
        (
            "Close or bound boundary/projector, geometry/no-shadow, Xi_src_hidden, coefficient and remaining local-test projection rows."
        ),
        (
            "Choosing clock/PPN/orbital frame after seeing residuals; using fitted GM or clock normalization to define tau; applying "
            "tau zero outside the one-parent-frame branch; or claiming local GR/Newton while geometry, boundary/projector and hidden-source gates remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def audit_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "AUD4325_0_single_tau",
            "one parent-owned time generator",
            "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout",
            "SIGNED_CONDITIONALLY_BY_4216",
            "one tau prevents clock/source/orbit/readout split curl",
        ),
        (
            "AUD4325_1_surface_coframe",
            "one surface family and observed coframe",
            "S_link fixed or tau-dragged; e_obs=e_bar(q) used by EH, Hilbert stress, EM, rods, clocks, orbital readout and PPN",
            "SIGNED_CONDITIONALLY_BY_4216",
            "frame switches become residuals if not fixed before variation",
        ),
        (
            "AUD4325_2_reference_no_fit",
            "reference selected before comparison",
            "no orbital GM, PPN, R10, clock, or source residual is used to choose H_ref",
            "SIGNED_CONDITIONALLY_BY_4215",
            "post-fit clock/reference choices are scored, not erased",
        ),
        (
            "AUD4325_3_Hperp_zero",
            "tau Hperp component zero",
            "locked tau/reference/coframe branch => Dq_tau[Hperp]=0 and epsilon_tau=0",
            "CONDITIONAL_ZERO_DERIVED",
            "zero is branch-local, not global",
        ),
        (
            "AUD4325_4_fallback",
            "clock/reference failure branch",
            "tau split, surface motion, frame/coframe, clock/orbital readout, units and reference fit residuals remain explicit",
            "BOUND_ROUTE_RETAINED",
            "no cancellation with geometry, boundary/projector or source tails",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for audit_id, clause, statement, status, implication in specs:
        row = base_row()
        row.update({"audit_id": audit_id, "clause": clause, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def tail_rows() -> List[Dict[str, str]]:
    specs = [
        ("CT4325_0_tau_split", "R_tau_split", "different source/charge/clock/orbit/PPN/readout tau choices", "MISSING_ZERO_OR_BOUND"),
        ("CT4325_1_surface", "R_surface_motion", "surface family not fixed or tau-dragged before variation", "MISSING_ZERO_OR_BOUND"),
        ("CT4325_2_frame", "R_frame_coframe", "observed coframe/frame switch not q-owned", "MISSING_ZERO_OR_BOUND"),
        ("CT4325_3_clock", "R_clock_readout", "clock normalization/readout selected after residuals", "MISSING_ZERO_OR_BOUND"),
        ("CT4325_4_orbit", "R_orbital_readout", "orbital frame or fitted GM used to choose readout", "MISSING_ZERO_OR_BOUND"),
        ("CT4325_5_units", "R_units", "non-common-mode units/orientation/source normalization", "MISSING_ZERO_OR_BOUND"),
        ("CT4325_6_ref_fit", "R_ref_fit", "reference H_ref chosen by PPN/R10/clock/source residual", "MISSING_ZERO_OR_BOUND"),
        ("CT4325_7_boundary_normal", "R_boundary_normal", "normal/corner/boundary leg mixed into tau row", "ROUTE_TO_BOUNDARY_PROJECTOR"),
    ]
    rows: List[Dict[str, str]] = []
    for tail_id, symbol, meaning, status in specs:
        row = base_row()
        row.update({"tail_id": tail_id, "symbol": symbol, "meaning": meaning, "status": status})
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4325_0_zero",
            "tau/reference Hperp zero",
            "single parent tau+surface+coframe+reference lock => Dq_tau[Hperp]=0 => epsilon_tau=0",
            "4216/4215 lifted to Hperp",
            "CONDITIONAL_ZERO_DERIVED",
        ),
        (
            "F4325_1_clock_tail",
            "clock/reference fallback",
            "epsilon_tau <= R_tau_split + R_surface_motion + R_frame_coframe + R_clock_readout + R_orbital_readout + R_units + R_ref_fit + R_boundary_normal",
            "4216/4215 fallback envelopes",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "F4325_2_source_readout_simplified",
            "4324 source-readout row after tau zero",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + Xi_src_hidden",
            "4324 plus F4325_0",
            "STANDARD_BRANCH_SIMPLIFICATION",
        ),
        (
            "F4325_3_EDq_update",
            "EDq component update",
            "E_Dq,Hperp^2 := sum_{i!=tau} w_i epsilon_i^2 in the locked tau branch; otherwise add w_tau epsilon_tau^2",
            "4320 plus F4325_0/F4325_1",
            "NONCLAIM_HANDOFF",
        ),
        (
            "F4325_4_Nsrc_handoff",
            "source-support handoff",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||), with tau contribution removed only in locked branch",
            "4319/4325",
            "NONCLAIM_HANDOFF",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, basis, status in specs:
        row = base_row()
        row.update({"formula_id": formula_id, "name": name, "formula": formula, "basis": basis, "status": status})
        rows.append(row)
    return rows


def component_update_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CU4325_0",
            "Dq_tau[Hperp]",
            "STANDARD_BRANCH_ZERO_LIFTED",
            "epsilon_tau=0 if one parent tau/surface/coframe/reference lock is fixed before variation",
            "clock-tail bound retained outside locked branch",
        ),
        (
            "CU4325_1",
            "Dq_source_readout[Hperp]",
            "SIMPLIFIED_BY_TAU_ZERO",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + Xi_src_hidden",
            "geometry, boundary/projector and hidden source tail remain",
        ),
        (
            "CU4325_2",
            "E_Dq,Hperp",
            "TAU_COMPONENT_CONDITIONAL",
            "remove w_tau epsilon_tau^2 only in locked branch",
            "do not erase clock tests outside branch",
        ),
        (
            "CU4325_3",
            "Dq_boundary_projector[Hperp]",
            "NEXT_TARGET",
            "boundary/projector is now the direct source-readout dependency alongside geometry and Xi_src_hidden",
            "4326 should lift or bound it",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for update_id, component, status, new_row, note in specs:
        row = base_row()
        row.update({"update_id": update_id, "component": component, "status": status, "new_row": new_row, "note": note})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUN4325_0_locked", "single parent tau/surface/frame/reference lock", "ALLOW_TAU_ZERO", "epsilon_tau=0", "branch-local zero"),
        ("RUN4325_1_tail_present", "post-fit clock/frame/reference or tau split present", "USE_CLOCK_TAIL_BOUND", "epsilon_tau finite", "claim blocked"),
        ("RUN4325_2_clock_fit", "clock normalization chosen after residuals", "REJECT_ZERO", "R_clock_readout retained", "firewall"),
        ("RUN4325_3_orbital_fit", "fitted GM/orbital frame chooses H_ref or tau", "REJECT_ZERO", "R_orbital_readout/R_ref_fit retained", "firewall"),
        ("RUN4325_4_boundary_mix", "boundary normal/corner leg hidden in tau", "REJECT_ROUTE_TO_BOUNDARY", "R_boundary_normal retained", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4325_0", "Tau/reference zero requires one parent-owned lock chosen before variation and empirical comparison.", "BLOCK_POST_FIT_ZERO"),
        ("FW4325_1", "Do not use clock normalization, fitted GM, PPN gauge or source residuals to choose tau/H_ref.", "BLOCK_FITTED_FRAME"),
        ("FW4325_2", "Boundary normals, corners and moving surfaces route to boundary/projector if not parent-owned.", "BLOCK_BOUNDARY_ERASURE"),
        ("FW4325_3", "Do not claim clock safety from epsilon_tau=0 while geometry/Xi/boundary/local-test projections remain open.", "BLOCK_CLOCK_OVERCLAIM"),
        ("FW4325_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until geometry, boundary/projector, Xi and coefficient gates close.", "BLOCK_LOCAL_TEST_CLAIM"),
    ]
    rows: List[Dict[str, str]] = []
    for rule_id, rule, action in specs:
        row = base_row()
        row.update({"rule_id": rule_id, "rule": rule, "action": action})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "decision_id": "DEC4325_0",
            "result": DECISION,
            "reason": "4216 gives a clean single-parent tau/surface/frame lock; lifted to Hperp it closes Dq_tau only inside that locked branch, with post-fit clock/reference tails retained.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4325_0", "tau_reference", "STANDARD_BRANCH_ZERO_LIFTED", "epsilon_tau=0 under one parent tau/surface/coframe/reference lock"),
        ("STAT4325_1", "clock_tail", "BOUND_RETAINED", "post-fit clock/orbital/reference/frame tails explicit"),
        ("STAT4325_2", "source_readout_dependency", "SIMPLIFIED", "tau term removed in locked branch"),
        ("STAT4325_3", "boundary_projector", "NEXT_TARGET", "remaining direct source-readout dependency"),
        ("STAT4325_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, obj, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "object": obj, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4325_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can boundary/projector/domain readout be lifted to Dq_boundary_projector[Hperp]=0 in the standard local branch, or must finite domain/projector tails remain?",
            "preferred_route": "prove source worldtube, projector, domain, surface normal and readout boundary are q-owned/fixed before variation",
            "fallback_route": "retain epsilon_boundary_projector <= projector commutator + domain wall + boundary normal/corner residuals",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 341 - PPC4161 Dq tau-reference Hperp zero or clock-tail bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, R10, PPN, clock safety, orbital safety, WEP, or a numerical value of `G_N`.

## Result

The tau/reference row closes inside the single-parent-time locked branch:

```text
tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout,
S_link fixed or tau-dragged,
e_obs=e_bar(q),
H_ref selected before residuals
=> Dq_tau[Hperp]=0
=> epsilon_tau=0.
```

If any clock/frame/reference clause is chosen after variation or after seeing residuals, the clock-tail bound is retained.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Tau Lock Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Clock Tail Ledger
{md_table(tables["tails"], ["tail_id", "symbol", "meaning", "status"])}

## Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "basis", "status"])}

## Component Update
{md_table(tables["component_update"], ["update_id", "component", "status", "new_row", "note"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4325 - Dq tau-reference Hperp zero or clock-tail bound

## Verdict

- Lifted `Dq_tau[Hperp]=0` inside the one-parent tau/surface/frame/reference branch.
- Retained clock/reference tails for post-fit or split-frame branches.
- Simplified the source-readout row by removing `L_xi epsilon_tau` only in the locked branch.
- Next target is boundary/projector/domain leakage.

## Main Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Tail Firewall
{md_table(tables["tails"], ["tail_id", "symbol", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validate_csv(path: Path):
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, f"csv parse failed: {exc}"
    if not rows:
        return False, "csv has no data rows"
    return True, f"csv parsed rows={len(rows)}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4325_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4325_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4325_zero_lift", "tau Hperp zero formula exists", any(r["formula_id"] == "F4325_0_zero" and "epsilon_tau=0" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4325_tail_bound", "clock-tail bound exists", any(r["formula_id"] == "F4325_1_clock_tail" and "R_clock_readout" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4325_source_simplified", "source-readout formula removes epsilon_tau", any(r["formula_id"] == "F4325_2_source_readout_simplified" and "epsilon_tau" not in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4325_tail_ledger", "clock tail ledger has at least eight rows", len(tables["tails"]) >= 8, "tails")
    add("VAL4325_reject_clock_fit", "clock fit shortcut rejected", any(r["runner_id"] == "RUN4325_2_clock_fit" and r["action"] == "REJECT_ZERO" for r in tables["runner"]), "runner")
    add("VAL4325_boundary_next", "boundary/projector next target exists", any("boundary-projector" in r["next_target"] for r in tables["next"]), "next")
    add("VAL4325_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4325_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4325_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4325_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4325_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4325_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4325_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4325_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4325_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4325_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4325_TAU_LOCK_AUDIT.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4325_CLOCK_TAIL_LEDGER.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4325_TAU_SIMPLIFIED_FORMULAS.csv",
        "component_update": SOURCE_DIR / "P8_Y5_R2FR_4325_COMPONENT_UPDATE.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4325_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4325_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4325_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4325_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4325_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "tails": tail_rows(),
        "formulas": formula_rows(),
        "component_update": component_update_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4325 Dq tau-reference Hperp zero or clock-tail bound

Marker: `{MARKER}`

4325 lifts the 4216 tau/surface/frame lock to `Hperp`: one parent-owned `tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout`, fixed/tau-dragged surface family, q-owned coframe and preselected `H_ref` give `Dq_tau[Hperp]=0` and `epsilon_tau=0` in the locked branch. Post-fit clock/frame/reference tails remain explicit outside it.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4325 packet tau-reference zero lift

Marker: `{PACKET_MARKER}`

Packet update: tau/reference is closed in the single-parent-time branch, but clock/readout/frame tails remain explicit if the branch is post-fit or split. The source-readout dependency now leans on geometry, boundary/projector and `Xi_src_hidden`.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
