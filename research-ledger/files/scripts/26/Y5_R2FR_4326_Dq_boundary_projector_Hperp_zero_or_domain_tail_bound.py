from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4326"
CLAIM_ID = "L-167"
BRANCH = "MTS_R2FR_Y5_DQ_BOUNDARY_PROJECTOR_HPERP_ZERO_OR_DOMAIN_TAIL_BOUND_4326"
DECISION = "BOUNDARY_PROJECTOR_HPERP_ZERO_LIFTED_FOR_QBASIC_NOFLUX_DOMAIN_BRANCH_DOMAIN_TAIL_BOUND_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_BOUNDARY_PROJECTOR_HPERP_ZERO_OR_DOMAIN_TAIL_BOUND_4326"
PACKET_MARKER = "PPC4161_PACKET_DQ_BOUNDARY_PROJECTOR_HPERP_ZERO_OR_DOMAIN_TAIL_BOUND_4326"
NEXT_TARGET = "4327-Y5-R2FR-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md"

FORMAL_PATH = FORMAL / "342-PPC4161-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md"
DOC_PATH = POST / "4326-Y5-R2FR-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4326_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4326_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4325_NEXT_TARGET.csv",
        "Dq_boundary_projector[Hperp]",
        "4325 handoff selecting boundary/projector row.",
    ),
    "SRC4326_01_projector": (
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "D_v P_loc = 0",
        "4214 q-basic/fixed projector zero route.",
    ),
    "SRC4326_02_projector_bound": (
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "R_denominator",
        "4214 projector/domain fallback envelope.",
    ),
    "SRC4326_03_boundary_zero": (
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_boundary + I_corner = 0",
        "4217 boundary/corner zero route.",
    ),
    "SRC4326_04_boundary_bound": (
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "R_memory_pullback",
        "4217 boundary/corner fallback envelope.",
    ),
    "SRC4326_05_no_flux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge",
        "4176 no-flux selector and radiation routing firewall.",
    ),
    "SRC4326_06_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "R_proj = Pi_loc D Obar_loc[Dq[v]] = 0",
        "4177 q-natural projector residual closure.",
    ),
    "SRC4326_07_component": (
        FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md",
        "Dq_boundary_projector[Hperp]",
        "4320 boundary/projector component status.",
    ),
    "SRC4326_08_tau_source_readout": (
        FORMAL / "341-PPC4161-Dq-tau-reference-Hperp-zero-or-clock-tail-bound.md",
        "L_Sigma epsilon_boundary_projector",
        "4325 source-readout row to simplify after boundary/projector zero.",
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
            "4326 lifts the 4214 projector and 4217 boundary/corner zero routes to the Hperp boundary-projector component. "
            "In the q-basic no-flux domain branch, P_loc=P_bar(q) or fixed before variation, e_obs=e_bar(q), the Hodge/readout "
            "is observed-geometry owned, the source worldtube/domain/surface normal is fixed or q-owned, no active selector wall, "
            "second denominator, source crossing, open-memory pullback, boundary projector flux or un-routed radiation remains, "
            "and differentiability/corner terms are fixed/exact/routed. Then Dq_boundary_projector[Hperp]=0 and "
            "epsilon_boundary_projector=0. If any clause fails, retain a domain-tail envelope from projector metric/domain/Hodge/wall/"
            "denominator/source-readout terms plus boundary differentiability/corner/radiative/source-crossing/memory/improvement terms. "
            "This deletes the L_Sigma epsilon_boundary_projector term from source-readout only in the q-basic no-flux branch. No local "
            "GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4326 source register, boundary/projector audit, domain-tail ledger, simplified formulas, component update, runner, "
            "firewall, decision, status, next-target and validation CSV."
        ),
        "private_boundary_projector_Hperp_standard_branch_zero_with_domain_tail_firewall_nonclaim",
        (
            "Close or bound geometry/no-shadow, Xi_src_hidden, coefficient and remaining local-test projection rows."
        ),
        (
            "Erasing radiation or source crossing as a bulk zero; using a post-fit projector/domain; hiding a second denominator or "
            "active wall; applying boundary zero outside no-flux support separation; or claiming local GR/Newton while geometry/Xi gates remain open."
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
            "AUD4326_0_projector",
            "q-basic/fixed projector",
            "P_loc=P_bar(q) or fixed before variation, so D_Hperp P_loc=0",
            "CONDITIONAL_ZERO_INPUT",
            "projector is not a post-fit sector switch",
        ),
        (
            "AUD4326_1_domain",
            "q-owned/fixed source worldtube and domain",
            "source worldtube, domain, surface normal and readout boundary are fixed or q-owned before variation",
            "CONDITIONAL_ZERO_INPUT",
            "domain changes are tails if not owned",
        ),
        (
            "AUD4326_2_no_wall",
            "no wall/denominator/hidden projector",
            "no active selector wall, boundary projector flux, second denominator or hidden constitutive projector remains",
            "CONDITIONAL_ZERO_INPUT",
            "blocks branch-switching by notation",
        ),
        (
            "AUD4326_3_boundary_no_flux",
            "differentiability-owned no-flux collar",
            "boundary/corner terms are fixed/exact/routed; no source crossing, imposed incoming radiation or open-memory pullback enters",
            "CONDITIONAL_ZERO_INPUT",
            "radiation is routed, not erased",
        ),
        (
            "AUD4326_4_Hperp_zero",
            "boundary-projector Hperp component zero",
            "all clauses above => Dq_boundary_projector[Hperp]=0 and epsilon_boundary_projector=0",
            "CONDITIONAL_ZERO_DERIVED",
            "zero is branch-local",
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
        ("DT4326_0_metric", "R_P_metric", "projector metric/readout not q-owned", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_1_domain", "R_domain", "domain/worldtube/surface normal moves before variation", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_2_hodge", "R_Hodge_readout", "Hodge/readout boundary not observed-geometry owned", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_3_wall", "R_wall", "active selector wall or branch switch", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_4_denominator", "R_denominator", "second denominator or normalization switch", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_5_source_readout", "R_source_readout", "source/readout boundary projector leakage", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_6_diff", "R_diff_owner", "boundary differentiability term not owned/fixed", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_7_corner", "R_corner_edge", "corner/edge mode/boost/orientation residual", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_8_rad", "R_rad_flux", "radiative EM/gravity/Poynting flux crossing boundary", "ROUTE_AS_BOUNDARY_FLUX"),
        ("DT4326_9_crossing", "R_source_crossing", "source crosses compact collar boundary", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_10_memory", "R_memory_pullback", "open-memory/cosmology sector pullback into local collar", "MISSING_ZERO_OR_BOUND"),
        ("DT4326_11_improvement", "R_improvement", "unowned exact/improvement/corner term", "MISSING_ZERO_OR_BOUND"),
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
            "F4326_0_zero",
            "boundary/projector Hperp zero",
            "q-basic projector + q-owned/fixed domain + no wall/denominator + differentiability-owned no-flux boundary => Dq_boundary_projector[Hperp]=0 => epsilon_boundary_projector=0",
            "4214/4217/4176 lifted to Hperp",
            "CONDITIONAL_ZERO_DERIVED",
        ),
        (
            "F4326_1_domain_tail",
            "domain/projector fallback",
            "epsilon_boundary_projector <= R_P_metric + R_domain + R_Hodge_readout + R_wall + R_denominator + R_source_readout + R_diff_owner + R_corner_edge + R_rad_flux + R_source_crossing + R_memory_pullback + R_improvement",
            "4214/4217 fallback envelopes",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "F4326_2_source_readout_simplified",
            "4325 source-readout row after boundary/projector zero",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + Xi_src_hidden",
            "4325 plus F4326_0",
            "STANDARD_BRANCH_SIMPLIFICATION",
        ),
        (
            "F4326_3_EDq_update",
            "EDq component update",
            "E_Dq,Hperp^2 := sum_{i!=tau,boundary_projector} w_i epsilon_i^2 in the locked no-flux branch; otherwise include w_boundary epsilon_boundary_projector^2",
            "4320 plus 4325/4326",
            "NONCLAIM_HANDOFF",
        ),
        (
            "F4326_4_Nsrc_handoff",
            "source-support handoff",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||), with boundary contribution removed only in the q-basic no-flux branch",
            "4319/4326",
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
            "CU4326_0",
            "Dq_boundary_projector[Hperp]",
            "STANDARD_BRANCH_ZERO_LIFTED",
            "epsilon_boundary_projector=0 if q-basic projector/domain/no-flux boundary clauses close",
            "domain-tail bound retained outside no-flux branch",
        ),
        (
            "CU4326_1",
            "Dq_source_readout[Hperp]",
            "SIMPLIFIED_BY_BOUNDARY_ZERO",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + Xi_src_hidden",
            "only geometry and hidden source tail remain in this dependency envelope",
        ),
        (
            "CU4326_2",
            "E_Dq,Hperp",
            "BOUNDARY_COMPONENT_CONDITIONAL",
            "remove w_boundary epsilon_boundary_projector^2 only in no-flux q-basic branch",
            "do not erase radiative/source-crossing branches",
        ),
        (
            "CU4326_3",
            "Dq_geom[Hperp]",
            "NEXT_TARGET",
            "geometry/no-shadow is now the only direct source-readout dependency besides Xi_src_hidden",
            "4327 should revisit geometry with the narrowed chain",
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
        ("RUN4326_0_qbasic_noflux", "q-basic projector/domain and no-flux boundary", "ALLOW_BOUNDARY_PROJECTOR_ZERO", "epsilon_boundary_projector=0", "branch-local zero"),
        ("RUN4326_1_tail_present", "wall/domain/radiative/source-crossing tail present", "USE_DOMAIN_TAIL_BOUND", "epsilon_boundary_projector finite", "claim blocked"),
        ("RUN4326_2_radiation", "radiative flux crosses boundary", "REJECT_BULK_ZERO_ROUTE_FLUX", "R_rad_flux retained as boundary/Hamiltonian flux", "firewall"),
        ("RUN4326_3_postfit_projector", "projector chosen after residuals", "REJECT_ZERO", "R_P_metric/R_wall/R_denominator retained", "firewall"),
        ("RUN4326_4_branch_mix", "smooth/no-flux zero mixed with exterior/source-crossing branch", "REJECT", "domain tail retained", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4326_0", "Boundary/projector zero requires q-basic/fixed projector and domain before variation.", "BLOCK_POST_FIT_PROJECTOR"),
        ("FW4326_1", "Radiative EM/gravity/Poynting flux is routed as boundary/Hamiltonian flux, not erased.", "BLOCK_RADIATION_ERASURE"),
        ("FW4326_2", "Do not mix no-flux compact collar zero with exterior/worldtube/source-crossing branches.", "BLOCK_BRANCH_MIX"),
        ("FW4326_3", "Active walls, second denominators and hidden constitutive projectors remain explicit tails.", "BLOCK_SELECTOR_ERASURE"),
        ("FW4326_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until geometry, Xi and coefficient/local-test gates close.", "BLOCK_LOCAL_TEST_CLAIM"),
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
            "decision_id": "DEC4326_0",
            "result": DECISION,
            "reason": "4214/4217/4176 give a clean q-basic no-flux projector/domain zero route, but domain, wall, radiation and source-crossing tails are retained outside that branch.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4326_0", "boundary_projector", "STANDARD_BRANCH_ZERO_LIFTED", "epsilon_boundary_projector=0 under q-basic no-flux domain clauses"),
        ("STAT4326_1", "domain_tail", "BOUND_RETAINED", "radiation/source-crossing/domain/wall tails explicit"),
        ("STAT4326_2", "source_readout_dependency", "SIMPLIFIED", "boundary term removed in no-flux branch"),
        ("STAT4326_3", "geometry", "NEXT_TARGET", "only direct source-readout dependency besides Xi_src_hidden"),
        ("STAT4326_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
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
            "next_target_id": "NT4326_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the geometry/no-shadow row be closed or narrowed now that source-readout depends only on geometry and Xi_src_hidden?",
            "preferred_route": "parent-sign observed coframe/metric/Hodge/no-shadow descent for Hperp",
            "fallback_route": "retain epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+epsilon_wall+epsilon_Hodge_geom and route to finite local tests",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 342 - PPC4161 Dq boundary-projector Hperp zero or domain-tail bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, R10, PPN, clock safety, orbital safety, WEP, or a numerical value of `G_N`.

## Result

The boundary/projector row closes inside the q-basic no-flux domain branch:

```text
P_loc=P_bar(q) or fixed,
domain/worldtube/surface normal q-owned or fixed,
no active wall or second denominator,
boundary/corner terms fixed/exact/routed,
no source crossing or un-routed radiation
=> Dq_boundary_projector[Hperp]=0
=> epsilon_boundary_projector=0.
```

If any domain/projector/boundary clause fails, the domain-tail bound remains live.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Boundary Projector Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Domain Tail Ledger
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
    post = f"""# 4326 - Dq boundary-projector Hperp zero or domain-tail bound

## Verdict

- Lifted `Dq_boundary_projector[Hperp]=0` inside the q-basic no-flux domain branch.
- Retained domain/projector/radiative/source-crossing tails outside that branch.
- Simplified source-readout to geometry plus `Xi_src_hidden`.
- Next target is geometry/no-shadow.

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

    add("VAL4326_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4326_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4326_zero_lift", "boundary Hperp zero formula exists", any(r["formula_id"] == "F4326_0_zero" and "epsilon_boundary_projector=0" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4326_tail_bound", "domain-tail bound exists", any(r["formula_id"] == "F4326_1_domain_tail" and "R_rad_flux" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4326_source_simplified", "source-readout formula removes boundary term", any(r["formula_id"] == "F4326_2_source_readout_simplified" and "epsilon_boundary_projector" not in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4326_tail_ledger", "domain tail ledger has at least twelve rows", len(tables["tails"]) >= 12, "tails")
    add("VAL4326_reject_radiation_erasure", "radiation erasure rejected", any(r["runner_id"] == "RUN4326_2_radiation" and "REJECT" in r["action"] for r in tables["runner"]), "runner")
    add("VAL4326_geometry_next", "geometry next target exists", any("geometry" in r["next_target"] for r in tables["next"]), "next")
    add("VAL4326_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4326_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4326_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4326_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4326_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4326_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4326_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4326_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4326_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4326_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4326_BOUNDARY_PROJECTOR_AUDIT.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4326_DOMAIN_TAIL_LEDGER.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4326_BOUNDARY_SIMPLIFIED_FORMULAS.csv",
        "component_update": SOURCE_DIR / "P8_Y5_R2FR_4326_COMPONENT_UPDATE.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4326_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4326_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4326_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4326_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4326_NEXT_TARGET.csv",
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
## PPC4161 4326 Dq boundary-projector Hperp zero or domain-tail bound

Marker: `{MARKER}`

4326 lifts the q-basic projector/no-flux boundary branch to `Hperp`: fixed or q-owned projector, worldtube/domain/surface normal, no active wall/second denominator, and differentiability-owned no-flux boundary give `Dq_boundary_projector[Hperp]=0` and `epsilon_boundary_projector=0`. Domain, radiation, source-crossing and wall tails remain explicit outside that branch.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4326 packet boundary-projector zero lift

Marker: `{PACKET_MARKER}`

Packet update: boundary/projector closes in the q-basic no-flux domain branch. After this, the narrowed source-readout envelope is geometry plus `Xi_src_hidden`; geometry/no-shadow is the next direct gate.
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
