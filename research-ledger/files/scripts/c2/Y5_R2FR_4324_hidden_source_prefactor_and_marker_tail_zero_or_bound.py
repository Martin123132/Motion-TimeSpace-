from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4324"
CLAIM_ID = "L-165"
BRANCH = "MTS_R2FR_Y5_HIDDEN_SOURCE_PREFACTOR_AND_MARKER_TAIL_ZERO_OR_BOUND_4324"
DECISION = "NO_HIDDEN_SLOT_NOT_PARENT_SIGNED_SOURCE_PREFACTOR_MASTER_TAIL_BOUND_DERIVED_NONCLAIM"
MARKER = "PPC4161_HIDDEN_SOURCE_PREFACTOR_AND_MARKER_TAIL_ZERO_OR_BOUND_4324"
PACKET_MARKER = "PPC4161_PACKET_HIDDEN_SOURCE_PREFACTOR_AND_MARKER_TAIL_ZERO_OR_BOUND_4324"
NEXT_TARGET = "4325-Y5-R2FR-Dq-tau-reference-Hperp-zero-or-clock-tail-bound.md"

FORMAL_PATH = FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md"
DOC_PATH = POST / "4324-Y5-R2FR-hidden-source-prefactor-and-marker-tail-zero-or-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4324_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4324_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4323_NEXT_TARGET.csv",
        "hidden species/source-prefactor",
        "4323 handoff selecting hidden source-prefactor tails.",
    ),
    "SRC4324_01_no_hidden_slots": (
        FORMAL / "320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md",
        "No independent f(m,X)F^2, source-label drift, hidden Hodge drift, or species marker coupling",
        "4304 no-hidden-slot clause not parent-signed.",
    ),
    "SRC4324_02_standard_Asrc": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "A_src=0 on the standard Dq/Hperp-closed branch",
        "4305 source amplitude closure in standard Dq/Hperp branch.",
    ),
    "SRC4324_03_EM_weight": (
        FORMAL / "329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md",
        "species/readout weight residual if prevariation source weights exist",
        "4313 EM/source-label weight residual retained unless source-label forgetting closes.",
    ),
    "SRC4324_04_source_readout_tails": (
        FORMAL / "337-PPC4161-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md",
        "hidden source/species weights w_A(Phi)",
        "4321 Rsrc hidden source/species tail.",
    ),
    "SRC4324_05_matter_hidden": (
        FORMAL / "338-PPC4161-Dq-matter-descent-lift-or-geometry-theta-bound-row.md",
        "epsilon_matter_hidden",
        "4322 hidden matter/source-prefactor tail.",
    ),
    "SRC4324_06_marker_tail": (
        FORMAL / "339-PPC4161-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md",
        "R_marker_source_label",
        "4323 marker/source-label tail.",
    ),
    "SRC4324_07_inner_source": (
        FORMAL / "333-PPC4161-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md",
        "matter/source action carries no independent m-boundary charge",
        "4317 no-direct-m-charge clause remains parent-signature dependent.",
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
            "4324 attacks the hidden source-prefactor/marker-tail coupling gate exposed by 4321-4323. The exact zero route is a "
            "no-hidden-slot/source-label-forgetting theorem: no w_A(Phi), source normalization(Phi), marker source-label drift, "
            "hidden matter operator, hidden EM current/Hodge weight, environment selector, or independent m-boundary source charge "
            "may enter before variation. Current sources do not globally parent-sign that clause, so the checkpoint derives a master "
            "tail budget Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + "
            "R_source_normalization + delta_w_EM + R_no_direct_m_charge. If the no-hidden-slot theorem is parent-signed, Xi_src_hidden=0; "
            "otherwise it is retained as a no-cancellation source-coupling row feeding N_src_nonHilbert, N_rest_nonEM, N_EM and N_inner. "
            "No local GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4324 source register, no-hidden-slot audit, master tail budget, zero route, dependency substitutions, runner, firewall, "
            "decision, status, next-target and validation CSV."
        ),
        "private_hidden_source_prefactor_master_tail_bound_nonclaim",
        (
            "Parent-sign no-hidden-slot/source-label-forgetting or source finite bounds for w_A, source normalization, marker drift, "
            "hidden matter operators, EM weights, environment selectors and no-direct-m-charge rows."
        ),
        (
            "Declaring calibrated source labels to be zero without a parent no-hidden-slot clause; cancelling hidden tails across EM, "
            "matter and source-readout; hiding source normalization in theta; or claiming local GR/Newton while Xi_src_hidden remains open."
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
            "AUD4324_0_no_hidden_slot",
            "no-hidden-slot/source-label-forgetting theorem",
            "no independent source labels, species weights, normalization markers, hidden EM/Hodge weights or environment selectors before variation",
            "NOT_GLOBAL_PARENT_SIGNED",
            "exact zero route exists but cannot be claimed globally",
        ),
        (
            "AUD4324_1_standard_branch",
            "standard Dq/Hperp closed branch",
            "A_src=0 and N_src,strong_standard=0 if all Dq/Hperp rows close",
            "CONDITIONAL_STANDARD_BRANCH_IMPORT",
            "useful only inside the signed standard branch",
        ),
        (
            "AUD4324_2_master_tail",
            "hidden source-coupling tail",
            "Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge",
            "MASTER_BOUND_DERIVED",
            "the foggy coupling problem is now a named residual budget",
        ),
        (
            "AUD4324_3_zero",
            "exact hidden-tail zero",
            "no-hidden-slot signed => Xi_src_hidden=0",
            "CONDITIONAL_ZERO_ROUTE",
            "would remove hidden source-prefactor tails from matter/source-readout/EM/inner rows",
        ),
        (
            "AUD4324_4_bound",
            "failure branch",
            "any hidden source-prefactor survives => Xi_src_hidden finite row required",
            "BOUND_ROUTE_REQUIRED",
            "no cancellation between source, EM, matter, theta or inner-charge tails",
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
        ("HT4324_0_wA", "R_hidden_weights", "hidden source/species weights w_A(Phi)", "source-readout/matter", "MISSING_ZERO_OR_BOUND"),
        ("HT4324_1_norm", "R_source_normalization", "source normalization or source-mass label drift", "theta/source-readout/inner", "MISSING_ZERO_OR_BOUND"),
        ("HT4324_2_marker", "R_marker_source_label", "marker/source-label readout tail", "theta/source-readout", "MISSING_ZERO_OR_BOUND"),
        ("HT4324_3_matter", "epsilon_matter_hidden", "direct hidden matter operator or source-prefactor tail", "matter", "MISSING_ZERO_OR_BOUND"),
        ("HT4324_4_sr", "epsilon_SR_hidden", "post-readout hidden source tail", "source-readout", "MISSING_ZERO_OR_BOUND"),
        ("HT4324_5_em", "delta_w_EM", "EM species/readout weight residual", "EM/Ward", "MISSING_ZERO_OR_BOUND"),
        ("HT4324_6_inner", "R_no_direct_m_charge", "independent m-boundary/source charge tail", "inner/source-domain", "MISSING_ZERO_OR_BOUND"),
        ("HT4324_7_env", "R_environment_selector", "environment/medium selector before variation", "selector/boundary", "MISSING_ZERO_OR_BOUND"),
    ]
    rows: List[Dict[str, str]] = []
    for tail_id, symbol, meaning, owner, status in specs:
        row = base_row()
        row.update({"tail_id": tail_id, "symbol": symbol, "meaning": meaning, "owner": owner, "status": status})
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4324_0_master_tail",
            "hidden source-prefactor master budget",
            "Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge + R_environment_selector",
            "4321-4323 plus 4304/4313/4317",
            "DERIVED_MASTER_BUDGET",
        ),
        (
            "F4324_1_tail_bound",
            "source-label derivative fallback",
            "Xi_src_hidden <= C_w||D_Hperp ln w_A|| + C_norm||D_Hperp ln N_src|| + C_mark||D_Hperp theta_src|| + C_op||D_Hperp O_hidden|| + C_EM||delta_w_EM|| + C_inner||Q_m^H|| + C_env||D_Hperp sigma_env||",
            "no-cancellation source-coupling envelope",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "F4324_2_zero",
            "no-hidden-slot zero",
            "if source-label forgetting/no-hidden-slot theorem is parent-signed, then Xi_src_hidden=0",
            "4304 exact clause as conditional route",
            "CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
        ),
        (
            "F4324_3_matter_substitution",
            "4323 matter row with hidden tail isolated",
            "epsilon_matter <= L_mg epsilon_geom + epsilon_matter_hidden <= L_mg epsilon_geom + Xi_src_hidden",
            "4323 plus F4324_0",
            "REDUCED_DEPENDENCY_HANDOFF",
        ),
        (
            "F4324_4_source_readout_substitution",
            "4323 source-readout row with hidden tails isolated",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + Xi_src_hidden",
            "4323 plus F4324_0",
            "REDUCED_DEPENDENCY_HANDOFF",
        ),
        (
            "F4324_5_Nsrc_handoff",
            "source-support handoff",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||), with hidden source-prefactor cost carried by Xi_src_hidden",
            "4319/4324",
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
            "CU4324_0",
            "hidden source-prefactor tails",
            "MASTER_TAIL_BUDGET_DERIVED",
            "Xi_src_hidden collects hidden source weights, source normalization, marker tails, hidden matter, source-readout, EM weights, inner charge and environment selector tails",
            "not zero unless no-hidden-slot/source-label-forgetting is parent-signed",
        ),
        (
            "CU4324_1",
            "Dq_matter[Hperp]",
            "HIDDEN_TAIL_ISOLATED",
            "epsilon_matter <= L_mg epsilon_geom + Xi_src_hidden",
            "geometry and hidden source tail remain",
        ),
        (
            "CU4324_2",
            "Dq_source_readout[Hperp]",
            "HIDDEN_TAIL_ISOLATED",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + Xi_src_hidden",
            "geometry, tau, boundary/projector and hidden tail remain",
        ),
        (
            "CU4324_3",
            "Dq_tau[Hperp]",
            "NEXT_TARGET",
            "tau/reference is the next uncluttered dependency after theta and hidden tail isolation",
            "4325 should lift or bound the clock/reference row",
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
        ("RUN4324_0_current", "current corpus", "USE_MASTER_TAIL_BOUND", "Xi_src_hidden retained", "no parent no-hidden-slot signature"),
        ("RUN4324_1_exact_zero", "no-hidden-slot/source-label-forgetting parent-signed", "ALLOW_XI_ZERO", "Xi_src_hidden=0", "then matter/source-readout hidden tails vanish"),
        ("RUN4324_2_finite_bound", "tail derivative/source rows sourced", "ALLOW_NONCLAIM_BOUND", "finite Xi_src_hidden feeds Nsrc/Nrest/NEM/Ninner", "claim still blocked"),
        ("RUN4324_3_cancel_tails", "cancel hidden source tails across components", "REJECT", "no-cancellation budget", "firewall"),
        ("RUN4324_4_theta_hide", "hide source normalization in theta zero", "REJECT", "route to Xi_src_hidden", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4324_0", "Do not claim no-hidden-slot/source-label-forgetting unless parent action signs it.", "BLOCK_UNSIGNED_ZERO"),
        ("FW4324_1", "Do not cancel hidden source tails across matter, EM, source-readout, theta or inner-charge rows.", "BLOCK_CANCELLATION"),
        ("FW4324_2", "Do not hide source normalization in calibrated theta constants.", "BLOCK_THETA_ERASURE"),
        ("FW4324_3", "Do not use U_B^2 A_src standard zero outside the Dq/Hperp-closed standard branch.", "BLOCK_BRANCH_LEAKAGE"),
        ("FW4324_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until Xi_src_hidden and geometry/tau/boundary/lambda gates close.", "BLOCK_LOCAL_TEST_CLAIM"),
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
            "decision_id": "DEC4324_0",
            "result": DECISION,
            "reason": "The corpus has a clean no-hidden-slot zero route but 4304 explicitly does not parent-sign it globally, so hidden source-prefactor/marker tails become the master coupling budget Xi_src_hidden.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4324_0", "no_hidden_slot_zero", "CONDITIONAL_NOT_PARENT_SIGNED", "exact route exists but not globally claimable"),
        ("STAT4324_1", "Xi_src_hidden", "MASTER_BOUND_DERIVED", "coupling fog is now a named source-tail budget"),
        ("STAT4324_2", "matter_source_readout", "HIDDEN_TAIL_ISOLATED", "hidden tails no longer spread through multiple names"),
        ("STAT4324_3", "tau_reference", "NEXT_TARGET", "next dependency after theta/hidden-tail isolation"),
        ("STAT4324_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
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
            "next_target_id": "NT4324_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the tau/reference clock row be lifted to Dq_tau[Hperp]=0 in the standard local branch, or must a finite clock/reference tail enter source-readout and local tests?",
            "preferred_route": "prove local tau/reference normal is q-owned/fixed before variation and has no hidden clock-standard leg",
            "fallback_route": "retain epsilon_tau <= clock/reference Jacobian tail plus boundary/normal residual",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 340 - PPC4161 hidden source-prefactor and marker-tail zero or bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove the parent no-hidden-slot theorem, local GR, Newtonian mechanics, R10, PPN, clock safety, orbital safety, WEP, or a numerical value of `G_N`.

## Result

4324 pins down the coupling wall. The exact zero route is:

```text
no hidden source/species weights,
no source-normalization marker drift,
no hidden matter operator,
no hidden EM/current/Hodge weight,
no environment selector,
no independent m-boundary source charge
=> Xi_src_hidden = 0.
```

But 4304 does not globally parent-sign that no-hidden-slot clause. So the honest result is a master tail budget:

```text
Xi_src_hidden
:= epsilon_matter_hidden
 + epsilon_SR_hidden
 + R_marker_source_label
 + R_hidden_weights
 + R_source_normalization
 + delta_w_EM
 + R_no_direct_m_charge
 + R_environment_selector.
```

That is progress: the coupling problem is now one named budget, not scattered fog.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## No-Hidden-Slot Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Tail Ledger
{md_table(tables["tails"], ["tail_id", "symbol", "meaning", "owner", "status"])}

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
    post = f"""# 4324 - hidden source-prefactor and marker-tail zero or bound

## Verdict

- Did not fake the no-hidden-slot theorem; 4304 says it is not globally parent-signed.
- Derived the master hidden source-coupling budget `Xi_src_hidden`.
- Isolated hidden source tails inside the matter and source-readout formulas.
- Set next target to the tau/reference clock row.

## Master Budget
{md_table([tables["formulas"][0], tables["formulas"][1], tables["formulas"][2]], ["formula_id", "name", "formula", "status"])}

## Reduced Dependencies
{md_table([tables["formulas"][3], tables["formulas"][4]], ["formula_id", "name", "formula", "status"])}

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

    add("VAL4324_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4324_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4324_no_hidden_not_signed", "no-hidden-slot is not parent signed", any(r["audit_id"] == "AUD4324_0_no_hidden_slot" and r["status"] == "NOT_GLOBAL_PARENT_SIGNED" for r in tables["audit"]), "audit")
    add("VAL4324_master_tail", "master tail formula exists", any(r["formula_id"] == "F4324_0_master_tail" and "Xi_src_hidden" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4324_tail_bound", "tail derivative fallback exists", any(r["formula_id"] == "F4324_1_tail_bound" and "D_Hperp ln w_A" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4324_zero_conditional", "zero route remains conditional", any(r["formula_id"] == "F4324_2_zero" and "NOT_PARENT_SIGNED" in r["status"] for r in tables["formulas"]), "formulas")
    add("VAL4324_tail_ledger", "tail ledger has at least eight rows", len(tables["tails"]) >= 8, "tails")
    add("VAL4324_substitution", "matter/source-readout substitutions include Xi", any(r["formula_id"] == "F4324_4_source_readout_substitution" and "Xi_src_hidden" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4324_reject_cancellation", "tail cancellation rejected", any(r["runner_id"] == "RUN4324_3_cancel_tails" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4324_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4324_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    add("VAL4324_next_target", "next target is 4325", any("4325" in r["next_target"] for r in tables["next"]), "next")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4324_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4324_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4324_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4324_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4324_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4324_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4324_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4324_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4324_NO_HIDDEN_SLOT_AUDIT.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4324_HIDDEN_SOURCE_TAIL_LEDGER.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4324_MASTER_TAIL_FORMULAS.csv",
        "component_update": SOURCE_DIR / "P8_Y5_R2FR_4324_COMPONENT_UPDATE.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4324_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4324_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4324_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4324_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4324_NEXT_TARGET.csv",
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
## PPC4161 4324 hidden source-prefactor and marker-tail zero or bound

Marker: `{MARKER}`

4324 refuses to smuggle the no-hidden-slot theorem: 4304 does not globally parent-sign it. The hidden source-prefactor/marker problem is consolidated into `Xi_src_hidden`, a master tail budget collecting hidden matter, source-readout, marker/source-label, source-normalization, EM weight, inner-charge and environment-selector tails.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4324 packet hidden source-prefactor master tail

Marker: `{PACKET_MARKER}`

Packet update: the coupling sore point is now `Xi_src_hidden`. If no-hidden-slot/source-label-forgetting is parent-signed, `Xi_src_hidden=0`; otherwise it becomes the finite source-coupling tail feeding matter, source-readout, EM and inner-source rows.
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
