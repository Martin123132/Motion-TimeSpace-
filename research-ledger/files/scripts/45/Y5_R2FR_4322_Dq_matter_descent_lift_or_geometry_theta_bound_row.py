from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4322"
CLAIM_ID = "L-163"
BRANCH = "MTS_R2FR_Y5_DQ_MATTER_DESCENT_LIFT_OR_GEOMETRY_THETA_BOUND_ROW_4322"
DECISION = "MATTER_COMPONENT_INDEPENDENT_LEG_REMOVED_GEOMETRY_THETA_DEPENDENCY_BOUND_DERIVED_NONCLAIM"
MARKER = "PPC4161_DQ_MATTER_DESCENT_LIFT_OR_GEOMETRY_THETA_BOUND_ROW_4322"
PACKET_MARKER = "PPC4161_PACKET_DQ_MATTER_DESCENT_LIFT_OR_GEOMETRY_THETA_BOUND_ROW_4322"
NEXT_TARGET = "4323-Y5-R2FR-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md"

FORMAL_PATH = FORMAL / "338-PPC4161-Dq-matter-descent-lift-or-geometry-theta-bound-row.md"
DOC_PATH = POST / "4322-Y5-R2FR-Dq-matter-descent-lift-or-geometry-theta-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4322_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4322_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4321_NEXT_TARGET.csv",
        "Dq_matter[Hperp]",
        "4321 handoff selecting matter descent lift.",
    ),
    "SRC4322_01_theta": (
        FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "Dq_theta_marker = 0",
        "4264 standard calibrated q-basic theta marker row.",
    ),
    "SRC4322_02_matter_domain": (
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "S_matter = Sbar[psi, g_obs(q), theta_obs]",
        "4265 matter action-domain theorem.",
    ),
    "SRC4322_03_source_prefactor_tax": (
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "Source-prefactor tax",
        "4265 lists hidden matter/source prefactors not closed by matter descent.",
    ),
    "SRC4322_04_interface": (
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "delta_v S_matter = 0",
        "4277 matter-interface descent and shadow-frame guard.",
    ),
    "SRC4322_05_geometry": (
        FORMAL / "262-PPC4161-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md",
        "epsilon_geom",
        "4246 geometry dependency row.",
    ),
    "SRC4322_06_4320_component": (
        FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md",
        "Dq_matter[Hperp]",
        "4320 matter component status.",
    ),
    "SRC4322_07_4321_source_readout": (
        FORMAL / "337-PPC4161-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md",
        "epsilon_source_readout <= L_T epsilon_matter",
        "4321 source-readout dependency row to be reduced by matter lift.",
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
            "4322 lifts the 4265 matter-domain theorem into the Hperp component route. For the standard local branch, "
            "S_matter=Sbar_m[psi,g_obs(q),theta_obs] has no independent hidden-parent matter argument, so variation along "
            "Hperp obeys the chain rule delta_Hperp S_matter=(delta Sbar/delta g_obs)delta_Hperp g_obs+(delta Sbar/delta theta_obs)"
            "delta_Hperp theta_obs plus any explicitly retained hidden matter/source-prefactor tail. Therefore Dq_matter[Hperp] is "
            "not an independent component: epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden. "
            "Substituting this into the 4321 source-readout row removes epsilon_matter as a free mystery cost and pushes it onto "
            "geometry, theta and hidden-matter tails. No local GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4322 source register, matter descent audit, zero-condition matrix, dependency formulas, hidden matter tail ledger, "
            "source-readout substitution, runner, firewall, decision, status, next-target and validation CSV."
        ),
        "private_matter_component_independent_leg_removed_geometry_theta_bound_nonclaim",
        (
            "Close or bound epsilon_geom, epsilon_theta_marker and epsilon_matter_hidden before claiming Dq_matter[Hperp]=0 or "
            "feeding source-readout/local tests."
        ),
        (
            "Treating matter descent as a blanket geometry-independent source zero; hiding species/source prefactors inside ordinary "
            "matter; cancelling geometry and theta tails; or claiming local GR/Newton while dependent geometry/theta gates remain open."
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
            "AUD4322_0_matter_action",
            "standard branch matter action",
            "S_matter=Sbar_m[psi,g_obs(q),theta_obs]",
            "SIGNED_FOR_STANDARD_BRANCH_BY_4265",
            "matter has no independent parent-field slot in this branch",
        ),
        (
            "AUD4322_1_Hperp_chain_rule",
            "Hperp variation of matter action",
            "delta_Hperp S_matter = S_g delta_Hperp g_obs + S_theta delta_Hperp theta_obs + R_matter_hidden",
            "DERIVED_DEPENDENCY_BOUND",
            "matter component inherits geometry/theta variation",
        ),
        (
            "AUD4322_2_zero_route",
            "exact matter component zero",
            "epsilon_geom=0, epsilon_theta_marker=0, epsilon_matter_hidden=0",
            "CONDITIONAL_ZERO_ROUTE",
            "then Dq_matter[Hperp]=0 in the standard branch",
        ),
        (
            "AUD4322_3_hidden_tax",
            "hidden matter/source-prefactor tails",
            "w_A(Phi), direct hidden operators, disformal ordinary-frame slots, source-normalization reentry",
            "RETAINED_AS_EPSILON_MATTER_HIDDEN",
            "keeps field-rename escapes out of the zero theorem",
        ),
        (
            "AUD4322_4_source_readout_substitution",
            "4321 dependency reduction",
            "epsilon_source_readout no longer needs free epsilon_matter",
            "SUBSTITUTION_READY",
            "source-readout now depends on geometry/theta/hidden tails instead of independent matter row",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for audit_id, clause, statement, status, implication in specs:
        row = base_row()
        row.update({"audit_id": audit_id, "clause": clause, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def zero_condition_rows() -> List[Dict[str, str]]:
    specs = [
        ("ZC4322_0_geometry", "epsilon_geom=0", "observed metric/coframe/Hodge geometry has no Hperp variation", "Dq_geom"),
        ("ZC4322_1_theta", "epsilon_theta_marker=0", "masses, charges, standards, material labels and selectors are q-basic/fixed", "Dq_theta_marker"),
        ("ZC4322_2_hidden", "epsilon_matter_hidden=0", "no direct hidden matter operator or species/source-prefactor dependence", "hidden matter tail"),
        ("ZC4322_3_domain", "matter action domain unchanged", "no source collar/worldtube/domain change is counted as matter", "boundary/domain owner"),
        ("ZC4322_4_em", "ordinary EM stress handled in EM/Poynting row", "do not hide EM constitutive tails inside matter zero", "Dq_EM owner"),
    ]
    rows: List[Dict[str, str]] = []
    for condition_id, condition, implication, owner in specs:
        row = base_row()
        row.update({"condition_id": condition_id, "condition": condition, "implication": implication, "owner_component": owner})
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4322_0_chain_rule",
            "matter action chain rule",
            "delta_Hperp S_matter = S_g delta_Hperp g_obs + S_theta delta_Hperp theta_obs + R_matter_hidden",
            "4265/4277 lifted to Hperp",
            "DERIVED",
        ),
        (
            "F4322_1_epsilon_matter",
            "matter dependency bound",
            "epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden",
            "no-cancellation Lipschitz envelope",
            "BOUND_DERIVED_VALUES_MISSING",
        ),
        (
            "F4322_2_exact_zero",
            "exact matter component zero",
            "if epsilon_geom=epsilon_theta_marker=epsilon_matter_hidden=0, then Dq_matter[Hperp]=0",
            "4322 zero-condition matrix",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "F4322_3_source_readout_substitution",
            "source-readout with matter substituted",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + (L_T L_mtheta + L_theta)epsilon_theta_marker + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + L_T epsilon_matter_hidden + epsilon_SR_hidden",
            "4321 plus F4322_1",
            "REDUCED_DEPENDENCY_HANDOFF",
        ),
        (
            "F4322_4_Nsrc_handoff",
            "4319 source-support handoff",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||), with epsilon_matter replaced by F4322_1 where used",
            "4319/4321/4322",
            "NONCLAIM_HANDOFF",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, basis, status in specs:
        row = base_row()
        row.update({"formula_id": formula_id, "name": name, "formula": formula, "basis": basis, "status": status})
        rows.append(row)
    return rows


def hidden_tail_rows() -> List[Dict[str, str]]:
    specs = [
        ("HM4322_0_species_weight", "w_A(Phi) S_A", "species/source weight before variation", "MISSING_ZERO_OR_BOUND"),
        ("HM4322_1_direct_hidden_operator", "O_hidden(Phi,psi)", "direct hidden matter coupling", "MISSING_ZERO_OR_BOUND"),
        ("HM4322_2_shadow_frame", "A_g(phi_X)e_pub or disformal slot", "ordinary frame shadow coupling", "MISSING_ZERO_OR_BOUND_OR_ALREADY_ZERO_BY_4277"),
        ("HM4322_3_source_normalization", "source normalization marker", "source mass/normalization injected through matter labels", "ROUTE_TO_THETA_OR_SOURCE_READOUT"),
        ("HM4322_4_domain_reentry", "matter domain/collar reentry", "domain changes posing as matter action variation", "ROUTE_TO_BOUNDARY_DOMAIN"),
    ]
    rows: List[Dict[str, str]] = []
    for tail_id, tail, meaning, status in specs:
        row = base_row()
        row.update({"tail_id": tail_id, "tail": tail, "meaning": meaning, "status": status})
        rows.append(row)
    return rows


def component_update_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CU4322_0",
            "Dq_matter[Hperp]",
            "INDEPENDENT_LEG_REMOVED_GEOMETRY_THETA_BOUND_RETAINED",
            "epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden",
            "zero if geometry, theta and hidden matter tails close",
        ),
        (
            "CU4322_1",
            "Dq_source_readout[Hperp]",
            "SOURCE_READOUT_DEPENDENCY_REDUCED",
            "substitute epsilon_matter bound into 4321 source-readout formula",
            "source-readout now leans harder on geometry/theta/tau/boundary",
        ),
        (
            "CU4322_2",
            "Dq_theta_marker[Hperp]",
            "NEXT_TARGET",
            "theta is the easiest remaining dependency because 4264 already adopted the standard q-basic row",
            "4323 should lift or bound it",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for update_id, component, status, new_row, zero_condition in specs:
        row = base_row()
        row.update({"update_id": update_id, "component": component, "status": status, "new_row": new_row, "zero_condition": zero_condition})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUN4322_0_current", "current corpus", "USE_DEPENDENCY_BOUND", "matter independent leg removed; geometry/theta/hidden tails remain", "no local claim"),
        ("RUN4322_1_exact_zero", "geometry, theta and hidden matter tails zero", "ALLOW_MATTER_ZERO", "epsilon_matter=0", "then source-readout dependency reduces"),
        ("RUN4322_2_finite_bound", "geometry/theta finite", "ALLOW_NONCLAIM_BOUND", "epsilon_matter finite and feedable", "claim still blocked"),
        ("RUN4322_3_hidden_slot", "direct hidden matter operator inserted", "REJECT_ZERO_USE_BOUND", "epsilon_matter_hidden retained", "firewall"),
        ("RUN4322_4_domain_shortcut", "collar/domain change hidden as matter variation", "REJECT", "route to boundary/domain", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4322_0", "Matter-domain descent cannot be used as a geometry-independent blanket source zero.", "BLOCK_BLANKET_ZERO"),
        ("FW4322_1", "Hidden matter/source-prefactor tails stay explicit in epsilon_matter_hidden.", "BLOCK_HIDDEN_SLOT_ERASURE"),
        ("FW4322_2", "Domain, collar and worldtube changes stay in boundary/domain rows.", "BLOCK_DOMAIN_ERASURE"),
        ("FW4322_3", "EM/Poynting constitutive tails stay in EM rows, not matter zero.", "BLOCK_EM_DOUBLE_COUNT"),
        ("FW4322_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until geometry/theta and other dependencies close.", "BLOCK_LOCAL_TEST_CLAIM"),
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
            "decision_id": "DEC4322_0",
            "result": DECISION,
            "reason": "The 4265/4277 matter-domain theorem removes an independent matter component, but Hperp closure depends on observed geometry, theta markers and explicit hidden matter tails.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4322_0", "matter_independent_leg", "REMOVED_CONDITIONALLY", "standard branch matter action descends through g_obs and theta"),
        ("STAT4322_1", "epsilon_matter", "DEPENDENCY_BOUND_DERIVED", "requires geometry/theta/hidden rows"),
        ("STAT4322_2", "source_readout", "DEPENDENCY_REDUCED", "4321 source-readout formula now substitutes matter bound"),
        ("STAT4322_3", "theta_marker", "NEXT_TARGET", "4264 provides a likely exact standard-branch lift"),
        ("STAT4322_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
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
            "next_target_id": "NT4322_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the 4264 calibrated q-basic theta-marker row be lifted to Dq_theta_marker[Hperp]=0 in the standard branch, or must marker tails be retained?",
            "preferred_route": "prove theta_obs is fixed before variation and has no hidden marker/source-label insertion for Hperp",
            "fallback_route": "retain epsilon_theta_marker <= marker Jacobian tail plus source-label/environment selector residuals",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 338 - PPC4161 Dq matter descent lift or geometry theta bound row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, Newtonian mechanics, R10, PPN, WEP, clock safety, orbital safety, or a numerical source-coupling value.

## Result

The standard matter action-domain theorem can be lifted into the `Hperp` route, but only as a dependency statement:

```text
S_matter = Sbar_m[psi, g_obs(q), theta_obs]
```

therefore

```text
delta_Hperp S_matter = S_g delta_Hperp g_obs + S_theta delta_Hperp theta_obs + R_matter_hidden.
```

So `Dq_matter[Hperp]` is not an independent mystery component. It is bounded by geometry, theta-marker and hidden-matter tails:

```text
epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden.
```

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Matter Descent Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Zero Conditions
{md_table(tables["zero"], ["condition_id", "condition", "implication", "owner_component"])}

## Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "basis", "status"])}

## Hidden Matter Tail Ledger
{md_table(tables["hidden"], ["tail_id", "tail", "meaning", "status"])}

## Component Update
{md_table(tables["component_update"], ["update_id", "component", "status", "new_row", "zero_condition"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4322 - Dq matter descent lift or geometry theta bound row

## Verdict

- Removed `Dq_matter[Hperp]` as an independent mystery component in the standard branch.
- Derived `epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden`.
- Substituted the matter bound into the 4321 source-readout dependency row.
- Kept hidden matter/source-prefactor, EM and domain tails explicit.

## Main Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Component Update
{md_table(tables["component_update"], ["update_id", "component", "status", "new_row"])}

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

    add("VAL4322_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4322_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4322_chain_rule", "matter chain-rule row exists", any(r["audit_id"] == "AUD4322_1_Hperp_chain_rule" and r["status"] == "DERIVED_DEPENDENCY_BOUND" for r in tables["audit"]), "audit")
    add("VAL4322_dependency_formula", "epsilon_matter formula includes geometry and theta", any("epsilon_geom" in r["formula"] and "epsilon_theta_marker" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4322_source_substitution", "source-readout substitution formula exists", any(r["formula_id"] == "F4322_3_source_readout_substitution" and "epsilon_source_readout" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4322_hidden_tails", "hidden matter tails listed", len(tables["hidden"]) >= 5, "hidden")
    add("VAL4322_no_domain_shortcut", "domain shortcut rejected", any(r["runner_id"] == "RUN4322_4_domain_shortcut" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4322_component_update", "matter independent leg removed", any("INDEPENDENT_LEG_REMOVED" in r["status"] for r in tables["component_update"]), "component_update")
    add("VAL4322_next_theta", "theta is next target", any("theta-marker" in r["next_target"] for r in tables["next"]), "next")
    add("VAL4322_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4322_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4322_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4322_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4322_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4322_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4322_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4322_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4322_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4322_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4322_MATTER_DESCENT_AUDIT.csv",
        "zero": SOURCE_DIR / "P8_Y5_R2FR_4322_MATTER_ZERO_CONDITIONS.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4322_MATTER_DEPENDENCY_FORMULAS.csv",
        "hidden": SOURCE_DIR / "P8_Y5_R2FR_4322_HIDDEN_MATTER_TAIL_LEDGER.csv",
        "component_update": SOURCE_DIR / "P8_Y5_R2FR_4322_COMPONENT_UPDATE.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4322_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4322_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4322_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4322_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4322_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "zero": zero_condition_rows(),
        "formulas": formula_rows(),
        "hidden": hidden_tail_rows(),
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
## PPC4161 4322 Dq matter descent lift or geometry theta bound row

Marker: `{MARKER}`

4322 removes `Dq_matter[Hperp]` as an independent standard-branch mystery component. The matter action descends through `g_obs(q)` and `theta_obs`, so the retained row is `epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden`; hidden matter/source-prefactor tails remain explicit.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4322 packet matter descent dependency row

Marker: `{PACKET_MARKER}`

Packet update: the matter component is now a geometry/theta/hidden-tail dependency, not a free source coupling. This also reduces the 4321 source-readout row by substituting the matter bound. Next target: lift the 4264 theta-marker zero to `Hperp` or retain marker tails.
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
