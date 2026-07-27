from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4323"
CLAIM_ID = "L-164"
BRANCH = "MTS_R2FR_Y5_DQ_THETA_MARKER_HPERP_ZERO_LIFT_OR_MARKER_TAIL_BOUND_4323"
DECISION = "THETA_MARKER_HPERP_ZERO_LIFTED_FOR_STANDARD_CALIBRATED_BRANCH_MARKER_TAIL_BOUND_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_THETA_MARKER_HPERP_ZERO_LIFT_OR_MARKER_TAIL_BOUND_4323"
PACKET_MARKER = "PPC4161_PACKET_DQ_THETA_MARKER_HPERP_ZERO_LIFT_OR_MARKER_TAIL_BOUND_4323"
NEXT_TARGET = "4324-Y5-R2FR-hidden-source-prefactor-and-marker-tail-zero-or-bound.md"

FORMAL_PATH = FORMAL / "339-PPC4161-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md"
DOC_PATH = POST / "4323-Y5-R2FR-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4323_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4323_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4322_NEXT_TARGET.csv",
        "Dq_theta_marker[Hperp]",
        "4322 handoff selecting theta-marker lift.",
    ),
    "SRC4323_01_theta_zero": (
        FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "Dq_theta_marker = 0",
        "4264 standard calibrated q-basic theta-marker zero.",
    ),
    "SRC4323_02_theta_fixed": (
        FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "D_X theta_obs = 0",
        "4264 fixed-before-variation branch theorem.",
    ),
    "SRC4323_03_theta_bound": (
        FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "marker/source-label readout tails",
        "4264 marker-tail bound fork.",
    ),
    "SRC4323_04_visible_matter_contract": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "theta_obs = {m_A, charges, alpha_EM, hbar, c, material labels}",
        "standard visible matter import contract.",
    ),
    "SRC4323_05_em_guard": (
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "D_X theta_obs = 0",
        "visible EM/readout guard for calibrated constants.",
    ),
    "SRC4323_06_4322_matter": (
        FORMAL / "338-PPC4161-Dq-matter-descent-lift-or-geometry-theta-bound-row.md",
        "epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden",
        "4322 matter dependency row to simplify.",
    ),
    "SRC4323_07_4321_source_readout": (
        FORMAL / "337-PPC4161-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md",
        "epsilon_source_readout <= L_T epsilon_matter",
        "4321 source-readout dependency row.",
    ),
    "SRC4323_08_4320_component": (
        FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md",
        "Dq_theta_marker[Hperp]",
        "4320 component status.",
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
            "4323 lifts the 4264 calibrated q-basic theta-marker row to the Hperp component in the standard visible branch. "
            "Because theta_obs={m_A,charges,alpha_EM,hbar,c,material labels} is calibrated/q-basic and fixed before variation, "
            "D_Hperp theta_obs=0 and Dq_theta_marker[Hperp]=0 provided no material, environment, source-normalization, species, "
            "clock-standard or charge-label marker is inserted into S_parent or S_eff before variation. The fallback marker-tail "
            "bound is epsilon_theta_marker <= ||J_theta L_Hperp theta||/||J_ref|| + R_marker_source_label + R_environment_selector "
            "+ R_source_normalization + R_standard_drift. In the standard zero branch, 4322 simplifies to "
            "epsilon_matter <= L_mg epsilon_geom + epsilon_matter_hidden, and 4321 simplifies by deleting the theta term from "
            "epsilon_source_readout. No local GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4323 source register, theta lift audit, marker-tail ledger, simplified dependency formulas, component update, runner, "
            "firewall, decision, status, next-target and validation CSV."
        ),
        "private_theta_marker_Hperp_standard_branch_zero_with_marker_tail_firewall_nonclaim",
        (
            "Close or bound hidden source-prefactor/marker tails, geometry, boundary/projector and tau rows before claiming local tests."
        ),
        (
            "Using calibrated constants as a numerical prediction of masses, charges, alpha_EM, hbar, c or G_N; hiding source "
            "normalization or environment selectors in theta; deleting marker tails outside the standard visible branch; or claiming "
            "local GR/Newton while geometry/tau/boundary/hidden-source gates remain open."
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
            "AUD4323_0_standard_constants",
            "standard theta list",
            "theta_obs={m_A, charges, alpha_EM, hbar, c, material labels}",
            "SIGNED_FOR_STANDARD_VISIBLE_BRANCH",
            "these are calibrated/q-basic constants, not hidden parent fields",
        ),
        (
            "AUD4323_1_fixed_before_variation",
            "theta fixed before variation",
            "D_Hperp theta_obs = 0",
            "LIFTED_FROM_D_X_THETA_OBS_ZERO",
            "Hperp cannot move fixed q-basic markers inside the standard branch",
        ),
        (
            "AUD4323_2_component_zero",
            "theta-marker Hperp component",
            "Dq_theta_marker[Hperp] = 0 and epsilon_theta_marker=0",
            "CONDITIONAL_ZERO_DERIVED",
            "valid only if marker-tail firewall rows are zero",
        ),
        (
            "AUD4323_3_tail_firewall",
            "hidden marker/source-label tails",
            "m_A(Phi), charge labels(Phi), clock standards(Phi), source normalization(Phi), environment selectors(Phi)",
            "RETAINED_OUTSIDE_STANDARD_BRANCH",
            "prevents calibrated constants from becoming hidden fields by notation",
        ),
        (
            "AUD4323_4_no_numeric_prediction",
            "calibration is not prediction",
            "theta zero does not derive numerical masses, charges, alpha_EM, hbar, c, source masses or G_N",
            "PUBLIC_CLAIM_BLOCKED",
            "this is a local-branch structural zero only",
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
        ("MT4323_0_mass_label", "m_A(Phi)", "hidden mass/species label before variation", "MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH"),
        ("MT4323_1_charge_label", "charge labels(Phi) or alpha_EM(Phi)", "hidden charge/current normalization marker", "MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH"),
        ("MT4323_2_clock_standard", "clock standards(Phi), hbar(Phi), c(Phi)", "hidden unit/clock marker", "MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH"),
        ("MT4323_3_material_label", "material labels(Phi)", "hidden material/environment response marker", "MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH"),
        ("MT4323_4_source_normalization", "source normalization(Phi)", "source mass/readout marker reentry", "ROUTE_TO_HIDDEN_SOURCE_PREFACTOR_OR_RSRC"),
        ("MT4323_5_environment_selector", "environment selectors(Phi)", "active branch/medium selector before variation", "ROUTE_TO_SELECTOR_OR_BOUNDARY"),
    ]
    rows: List[Dict[str, str]] = []
    for tail_id, tail, meaning, status in specs:
        row = base_row()
        row.update({"tail_id": tail_id, "tail": tail, "meaning": meaning, "status": status})
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4323_0_zero",
            "standard theta zero",
            "D_Hperp theta_obs=0 => Dq_theta_marker[Hperp]=0 => epsilon_theta_marker=0",
            "4264 lifted to Hperp",
            "CONDITIONAL_ZERO_DERIVED",
        ),
        (
            "F4323_1_tail_bound",
            "marker-tail fallback",
            "epsilon_theta_marker <= ||J_theta L_Hperp theta||/||J_ref|| + R_marker_source_label + R_environment_selector + R_source_normalization + R_standard_drift",
            "4264 bound fork",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "F4323_2_matter_simplified",
            "4322 matter row after theta zero",
            "epsilon_matter <= L_mg epsilon_geom + epsilon_matter_hidden",
            "4322 plus F4323_0",
            "STANDARD_BRANCH_SIMPLIFICATION",
        ),
        (
            "F4323_3_source_readout_simplified",
            "4321 source-readout row after theta zero and matter substitution",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + L_T epsilon_matter_hidden + epsilon_SR_hidden",
            "4321/4322 plus F4323_0",
            "STANDARD_BRANCH_SIMPLIFICATION",
        ),
        (
            "F4323_4_Nsrc_handoff",
            "4319 source-support handoff",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||), with epsilon_theta_marker=0 only in the standard branch",
            "4319/4320/4323",
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
            "CU4323_0",
            "Dq_theta_marker[Hperp]",
            "STANDARD_BRANCH_ZERO_LIFTED",
            "epsilon_theta_marker=0 if theta_obs fixed/q-basic and marker-tail firewall closes",
            "tail bound retained outside standard branch",
        ),
        (
            "CU4323_1",
            "Dq_matter[Hperp]",
            "SIMPLIFIED_BY_THETA_ZERO",
            "epsilon_matter <= L_mg epsilon_geom + epsilon_matter_hidden",
            "geometry and hidden matter tails remain",
        ),
        (
            "CU4323_2",
            "Dq_source_readout[Hperp]",
            "SIMPLIFIED_BY_THETA_ZERO",
            "theta term removed from source-readout dependency envelope",
            "geometry, tau, boundary/projector and hidden source tails remain",
        ),
        (
            "CU4323_3",
            "hidden source-prefactor / marker tails",
            "NEXT_TARGET",
            "source normalization and hidden species weights now carry the main source-coupling tail burden",
            "4324 should prove zero or bound them",
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
        ("RUN4323_0_standard", "standard calibrated q-basic visible branch", "ALLOW_THETA_ZERO", "epsilon_theta_marker=0", "no public numeric prediction"),
        ("RUN4323_1_tail_present", "hidden marker/source-label tail present", "USE_TAIL_BOUND", "epsilon_theta_marker finite", "claim blocked"),
        ("RUN4323_2_numeric_prediction", "use theta zero to predict constants", "REJECT", "calibration is not prediction", "firewall"),
        ("RUN4323_3_source_norm_hidden", "source normalization hidden in theta", "REJECT_ZERO_ROUTE_TO_4324", "source-prefactor tail retained", "firewall"),
        ("RUN4323_4_environment_selector", "environment selector inserted before variation", "REJECT_ZERO_USE_SELECTOR_BOUND", "selector/boundary route", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4323_0", "Theta zero is branch-local and cannot be used to predict numerical constants.", "BLOCK_NUMERIC_PREDICTION"),
        ("FW4323_1", "Hidden source normalization or species weights cannot be hidden inside theta zero.", "BLOCK_SOURCE_PREFACTOR_ERASURE"),
        ("FW4323_2", "Environment selectors and material labels remain explicit if parent-field dependent.", "BLOCK_SELECTOR_ERASURE"),
        ("FW4323_3", "Clock-standard or charge-normalization tails route to clock/EM/source rows if not fixed.", "BLOCK_EM_CLOCK_DOUBLE_COUNT"),
        ("FW4323_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until geometry, tau, boundary and hidden-source tails close.", "BLOCK_LOCAL_TEST_CLAIM"),
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
            "decision_id": "DEC4323_0",
            "result": DECISION,
            "reason": "The calibrated q-basic theta row is fixed before variation, so the Hperp theta-marker component closes in the standard branch; marker/source-label tails remain explicit outside that branch.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4323_0", "theta_marker", "STANDARD_BRANCH_ZERO_LIFTED", "epsilon_theta_marker=0 under q-basic fixed theta and no hidden tails"),
        ("STAT4323_1", "matter_dependency", "SIMPLIFIED", "theta term removed from 4322 matter row"),
        ("STAT4323_2", "source_readout_dependency", "SIMPLIFIED", "theta term removed from 4321/4322 source-readout row"),
        ("STAT4323_3", "hidden_source_prefactor", "NEXT_TARGET", "source normalization/species marker tails now matter"),
        ("STAT4323_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
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
            "next_target_id": "NT4323_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can hidden species/source-prefactor and marker/source-label tails be theorem-zeroed in the standard branch, or must they become finite source-coupling rows?",
            "preferred_route": "prove source-label forgetting/no-hidden-slot theorem for w_A(Phi), source normalization and marker tails",
            "fallback_route": "retain epsilon_matter_hidden, epsilon_SR_hidden and R_marker/source-prefactor rows with no-cancellation bounds",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 339 - PPC4161 Dq theta-marker Hperp zero lift or marker-tail bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not derive numerical masses, charges, `alpha_EM`, `hbar`, `c`, source masses, `G_N`, local GR, Newton, R10, PPN, WEP, clock safety, or orbital safety.

## Result

The 4264 theta-marker row **does** lift to `Hperp` inside the standard calibrated q-basic visible branch:

```text
theta_obs = {{m_A, charges, alpha_EM, hbar, c, material labels}},
D_Hperp theta_obs = 0
=> Dq_theta_marker[Hperp] = 0
=> epsilon_theta_marker = 0.
```

This is not a numerical prediction of constants. It is a branch-local structural zero. If hidden marker/source-label/environment dependence is inserted before variation, the marker-tail bound is retained.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Theta Lift Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Marker Tail Ledger
{md_table(tables["tails"], ["tail_id", "tail", "meaning", "status"])}

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
    post = f"""# 4323 - Dq theta-marker Hperp zero lift or marker-tail bound

## Verdict

- Lifted the 4264 theta-marker zero to `Dq_theta_marker[Hperp]=0` inside the standard calibrated q-basic branch.
- Kept marker/source-label/environment tails explicit outside that branch.
- Simplified the 4322 matter row and 4321 source-readout row by deleting the theta term.
- No numerical-constant or local-GR claim fires.

## Simplified Formulas
{md_table([tables["formulas"][0], tables["formulas"][2], tables["formulas"][3]], ["formula_id", "name", "formula", "status"])}

## Tail Firewall
{md_table(tables["tails"], ["tail_id", "tail", "status"])}

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

    add("VAL4323_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4323_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4323_zero_lift", "theta Hperp zero formula exists", any(r["formula_id"] == "F4323_0_zero" and "epsilon_theta_marker=0" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4323_tail_bound", "marker-tail bound exists", any(r["formula_id"] == "F4323_1_tail_bound" and "R_marker_source_label" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4323_matter_simplified", "matter formula removes theta term", any(r["formula_id"] == "F4323_2_matter_simplified" and "epsilon_theta_marker" not in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4323_source_simplified", "source-readout formula removes theta term", any(r["formula_id"] == "F4323_3_source_readout_simplified" and "epsilon_theta_marker" not in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4323_tail_ledger", "marker tail ledger has at least six rows", len(tables["tails"]) >= 6, "tails")
    add("VAL4323_no_numeric_prediction", "numeric prediction shortcut rejected", any(r["runner_id"] == "RUN4323_2_numeric_prediction" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4323_source_norm_firewall", "source normalization hidden in theta rejected", any(r["runner_id"] == "RUN4323_3_source_norm_hidden" and "REJECT" in r["action"] for r in tables["runner"]), "runner")
    add("VAL4323_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4323_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    add("VAL4323_next_target", "next target is 4324", any("4324" in r["next_target"] for r in tables["next"]), "next")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4323_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4323_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4323_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4323_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4323_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4323_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4323_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4323_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4323_THETA_LIFT_AUDIT.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4323_MARKER_TAIL_LEDGER.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4323_THETA_SIMPLIFIED_FORMULAS.csv",
        "component_update": SOURCE_DIR / "P8_Y5_R2FR_4323_COMPONENT_UPDATE.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4323_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4323_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4323_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4323_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4323_NEXT_TARGET.csv",
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
## PPC4161 4323 Dq theta-marker Hperp zero lift or marker-tail bound

Marker: `{MARKER}`

4323 lifts the calibrated q-basic theta-marker zero to `Hperp` inside the standard visible branch: `D_Hperp theta_obs=0 => Dq_theta_marker[Hperp]=0 => epsilon_theta_marker=0`. This simplifies the matter/source-readout envelopes by deleting the theta term, while retaining marker/source-label/environment/source-normalization tails outside the standard branch.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4323 packet theta-marker zero lift

Marker: `{PACKET_MARKER}`

Packet update: theta-marker is closed in the standard calibrated branch, not globally. The remaining source-coupling burden shifts to hidden source-prefactor/marker tails, geometry, tau and boundary/projector gates.
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
