from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4327"
CLAIM_ID = "L-168"
BRANCH = "MTS_R2FR_Y5_DQ_GEOMETRY_NO_SHADOW_OR_EPSILON_GEOM_PROFILE_REDUCTION_4327"
DECISION = "GEOMETRY_ZERO_REJECTED_SOURCE_READOUT_NARROWED_TO_CORE_FRAME_SHADOW_PLUS_XI_NONCLAIM"
MARKER = "PPC4161_DQ_GEOMETRY_NO_SHADOW_OR_EPSILON_GEOM_PROFILE_REDUCTION_4327"
PACKET_MARKER = "PPC4161_PACKET_DQ_GEOMETRY_NO_SHADOW_OR_EPSILON_GEOM_PROFILE_REDUCTION_4327"
NEXT_TARGET = "4328-Y5-R2FR-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md"

FORMAL_PATH = FORMAL / "343-PPC4161-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md"
DOC_PATH = POST / "4327-Y5-R2FR-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4327_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4327_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4326_NEXT_TARGET.csv",
        "geometry/no-shadow",
        "4326 handoff selecting geometry/no-shadow row.",
    ),
    "SRC4327_01_geom_decomp": (
        FORMAL / "262-PPC4161-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md",
        "epsilon_geom",
        "4246 geometry decomposition and no-shadow target.",
    ),
    "SRC4327_02_no_shadow_missing": (
        FORMAL / "263-PPC4161-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md",
        "A_MF_PARENT_SIGNATURE_NOT_FOUND",
        "4247 blocks full no-shadow adoption.",
    ),
    "SRC4327_03_reduced_geom": (
        FORMAL / "286-PPC4161-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md",
        "epsilon_geom_reduced",
        "4270 compressed geometry obstruction.",
    ),
    "SRC4327_04_core_shadow": (
        FORMAL / "287-PPC4161-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md",
        "epsilon_core_geom",
        "4271 core coframe/shadow-frame fork.",
    ),
    "SRC4327_05_boundary_closed": (
        FORMAL / "342-PPC4161-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md",
        "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + Xi_src_hidden",
        "4326 narrowed source-readout to geometry plus Xi.",
    ),
    "SRC4327_06_Xi": (
        FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md",
        "Xi_src_hidden",
        "4324 master hidden source-prefactor tail.",
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
            "4327 revisits the geometry/no-shadow gate after 4321-4326 narrowed the source-readout chain. The checkpoint rejects "
            "a full Dq_geom[Hperp]=0 claim because A_MF/no-shadow and the public parent no-extra-frame/action-domain clause remain "
            "unsigned. It nevertheless compresses the remaining direct source-readout obstruction: in the locked q-basic no-flux branch, "
            "epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core + Xi_src_hidden, where epsilon_geom_core is controlled by "
            "core observed-readout/coframe-shadow terms or, equivalently, by c_s=D_Hperp ln A_s, b_dis_s=D_Hperp B_s, h_s^perp, "
            "readout-frame and terminal-frame tails. If the parent action signs no independent A_s, B_s, h_s^perp, source-only, "
            "post-readout or hidden Hodge/constitutive frame slots, then epsilon_geom_core=0; otherwise the c_g/b_dis finite-bound runner "
            "is required. No local GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4327 source register, geometry/no-shadow audit, core frame-shadow ledger, reduced formulas, runner, firewall, decision, "
            "status, next-target and validation CSV."
        ),
        "private_geometry_core_frame_shadow_plus_Xi_bottleneck_nonclaim",
        (
            "Parent-sign no-extra-frame/no-shadow action-domain clause or source finite c_g/b_dis/shadow/readout-frame bounds before local tests."
        ),
        (
            "Using A_MF/no-shadow without parent signature; treating Cassini/PPN diagnostics as raw c_g proof; hiding frame-shadow in geometry notation; "
            "or claiming local GR/Newton while epsilon_geom_core or Xi_src_hidden remains open."
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
            "AUD4327_0_full_zero_attempt",
            "full geometry zero",
            "A_MF/no-shadow for Hperp would give Dq_geom[Hperp]=0",
            "REJECTED_NOT_PARENT_SIGNED",
            "A_MF_PARENT_SIGNATURE_NOT_FOUND remains live",
        ),
        (
            "AUD4327_1_reduced_geometry",
            "reduced geometry obstruction",
            "tau, boundary/projector and readout tails are no longer double-counted; geometry compresses to core observed-readout/coframe-shadow plus constitutive reopen tails",
            "REDUCED_BUT_NONZERO",
            "source-readout now depends on geometry core and Xi",
        ),
        (
            "AUD4327_2_core_frame_fork",
            "core frame-shadow theorem",
            "no independent A_s(Phi), B_s(Phi), h_s^perp, source-only frame slot, post-readout frame slot, or hidden Hodge/constitutive frame slot",
            "CONDITIONAL_ZERO_ROUTE",
            "would set c_s=b_dis_s=D_Hperp h_s^perp=0 and epsilon_geom_core=0",
        ),
        (
            "AUD4327_3_finite_bound",
            "c_g/b_dis fallback",
            "if extra frame slots survive, epsilon_geom_core becomes a finite frame-coupling bound",
            "BOUND_ROUTE_REQUIRED",
            "this is now the clean geometry runner target",
        ),
        (
            "AUD4327_4_source_readout",
            "narrowed source-readout",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom_core + Xi_src_hidden",
            "DERIVED_BOTTLENECK",
            "direct source-readout burden is core geometry plus hidden source tail",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for audit_id, clause, statement, status, implication in specs:
        row = base_row()
        row.update({"audit_id": audit_id, "clause": clause, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def frame_rows() -> List[Dict[str, str]]:
    specs = [
        ("GF4327_0_cg", "c_s := D_Hperp ln A_s", "conformal same-frame/shadow coupling", "MISSING_ZERO_OR_BOUND"),
        ("GF4327_1_bdis", "b_dis_s := D_Hperp B_s", "disformal/time-direction frame coupling", "MISSING_ZERO_OR_BOUND"),
        ("GF4327_2_hperp", "D_Hperp h_s^perp", "orthogonal shadow metric component", "MISSING_ZERO_OR_BOUND"),
        ("GF4327_3_readout", "epsilon_readout_frame", "post-readout frame slot", "MISSING_ZERO_OR_BOUND"),
        ("GF4327_4_terminal", "epsilon_terminal", "terminal public metric/readout mismatch", "MISSING_ZERO_OR_BOUND"),
        ("GF4327_5_constitutive", "epsilon_constitutive_reopen", "hidden Hodge/constitutive frame slot", "MISSING_ZERO_OR_BOUND"),
    ]
    rows: List[Dict[str, str]] = []
    for frame_id, symbol, meaning, status in specs:
        row = base_row()
        row.update({"frame_id": frame_id, "symbol": symbol, "meaning": meaning, "status": status})
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4327_0_reduced_geom",
            "locked-branch reduced geometry",
            "epsilon_geom <= epsilon_core_observed_readout + (1+C_Hodge_geom_core)epsilon_core_coframe_shadow + epsilon_constitutive_reopen",
            "4270 plus 4325/4326 removing tau/boundary double-counting",
            "REDUCED_BOUND_READY_VALUES_MISSING",
        ),
        (
            "F4327_1_core_frame_bound",
            "core frame-shadow finite bound",
            "epsilon_geom_core <= C_cg sum_s |c_s| + C_dis sum_s |b_dis_s| + C_shadow sum_s ||h_s^perp|| + C_readout epsilon_readout_frame + C_terminal epsilon_terminal + epsilon_constitutive_reopen",
            "4271 finite bound fork",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "F4327_2_core_zero",
            "no-extra-frame zero",
            "parent no-extra-frame/no-shadow action-domain signature => c_s=b_dis_s=D_Hperp h_s^perp=epsilon_readout_frame=epsilon_terminal=epsilon_constitutive_reopen=0 => epsilon_geom_core=0",
            "4271 exact zero fork",
            "CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
        ),
        (
            "F4327_3_source_readout_bottleneck",
            "narrowed source-readout bottleneck",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom_core + Xi_src_hidden",
            "4326 plus F4327_0/F4327_1",
            "DERIVED_BOTTLENECK",
        ),
        (
            "F4327_4_EDq_bottleneck",
            "EDq geometry/Xi handoff",
            "E_Dq,Hperp^2 retains w_geom epsilon_geom_core^2 plus non-source-readout component rows; source-readout no longer carries tau/boundary/theta/matter as free terms",
            "4320-4327",
            "NONCLAIM_HANDOFF",
        ),
        (
            "F4327_5_claim_gate",
            "local claim gate",
            "source-readout closes only if epsilon_geom_core=0 and Xi_src_hidden=0; local GR still also needs coefficient/EM/inner/lambda/projection gates",
            "4327 firewall",
            "CLAIM_BLOCKED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, basis, status in specs:
        row = base_row()
        row.update({"formula_id": formula_id, "name": name, "formula": formula, "basis": basis, "status": status})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUN4327_0_current", "current corpus", "USE_CORE_FRAME_BOUND", "epsilon_geom_core and Xi_src_hidden remain", "no full geometry zero"),
        ("RUN4327_1_no_extra_frame", "parent no-extra-frame/no-shadow signature signed", "ALLOW_GEOMETRY_CORE_ZERO", "epsilon_geom_core=0", "still needs Xi and other gates"),
        ("RUN4327_2_finite_bound", "c_g/b_dis/shadow values sourced", "ALLOW_NONCLAIM_BOUND", "finite epsilon_geom_core feeds source-readout/local tests", "claim still blocked"),
        ("RUN4327_3_AMF_shortcut", "use A_MF without parent signature", "REJECT", "A_MF_PARENT_SIGNATURE_NOT_FOUND", "firewall"),
        ("RUN4327_4_cassini_shortcut", "treat diagnostic PPN alpha_eff as raw c_g proof", "REJECT", "needs range/profile/tails/projection constants", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4327_0", "Do not claim Dq_geom[Hperp]=0 until parent no-extra-frame/no-shadow action-domain signature exists.", "BLOCK_UNSIGNED_GEOMETRY_ZERO"),
        ("FW4327_1", "Do not use A_MF as a shortcut while A_MF_PARENT_SIGNATURE_NOT_FOUND remains true.", "BLOCK_AMF_SHORTCUT"),
        ("FW4327_2", "Do not treat Cassini/PPN diagnostic bounds as raw c_g/b_dis proof without profile/tail/projection constants.", "BLOCK_DIAGNOSTIC_OVERCLAIM"),
        ("FW4327_3", "Do not hide hidden Hodge/constitutive frame slots inside same-coframe wording.", "BLOCK_CONSTITUTIVE_ERASURE"),
        ("FW4327_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until epsilon_geom_core, Xi_src_hidden and remaining coefficient/EM/inner/lambda gates close.", "BLOCK_LOCAL_TEST_CLAIM"),
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
            "decision_id": "DEC4327_0",
            "result": DECISION,
            "reason": "The full geometry/no-shadow zero remains unsigned, but after 4321-4326 the source-readout chain is narrowed to core frame-shadow geometry plus Xi_src_hidden.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4327_0", "geometry_zero", "REJECTED_NOT_PARENT_SIGNED", "A_MF/no-shadow and no-extra-frame action-domain not signed"),
        ("STAT4327_1", "epsilon_geom_core", "CORE_FRAME_BOUND_DERIVED", "c_g/b_dis/shadow/readout-frame terms are the finite route"),
        ("STAT4327_2", "source_readout", "BOTTLENECK_NARROWED", "direct source-readout burden is epsilon_geom_core plus Xi_src_hidden"),
        ("STAT4327_3", "next_runner", "NEXT_TARGET", "parent no-extra-frame signature or c_g/b_dis bound runner"),
        ("STAT4327_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
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
            "next_target_id": "NT4327_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the parent action sign no independent conformal/disformal/shadow frame slots, or must c_g/b_dis finite local bounds be sourced?",
            "preferred_route": "prove parent no-extra-frame/no-shadow action-domain signature for ordinary matter, EM/Hodge and readouts",
            "fallback_route": "build finite c_g, b_dis, h_perp, readout-frame and constitutive-tail bound runner with local PPN/R10/clock/orbital projections",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 343 - PPC4161 Dq geometry no-shadow or epsilon geom profile reduction

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove `Dq_geom[Hperp]=0`, local GR, Newtonian mechanics, R10, PPN, clock safety, orbital safety, WEP, or a numerical value of `G_N`.

## Result

The full geometry zero is **not** adopted:

```text
A_MF_PARENT_SIGNATURE_NOT_FOUND.
```

But the source-readout chain is now sharply narrowed. After the source-readout, matter, theta, tau and boundary/projector reductions:

```text
epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom_core + Xi_src_hidden.
```

The geometry obstruction is no longer a fog of every local residual. It is the core no-extra-frame/coframe-shadow problem:

```text
epsilon_geom_core <= C_cg sum_s |c_s|
 + C_dis sum_s |b_dis_s|
 + C_shadow sum_s ||h_s^perp||
 + C_readout epsilon_readout_frame
 + C_terminal epsilon_terminal
 + epsilon_constitutive_reopen.
```

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Geometry Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Core Frame Ledger
{md_table(tables["frames"], ["frame_id", "symbol", "meaning", "status"])}

## Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "basis", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4327 - Dq geometry no-shadow or epsilon geom profile reduction

## Verdict

- Rejected full geometry zero because `A_MF/no-shadow` remains unsigned.
- Narrowed source-readout to `epsilon_geom_core + Xi_src_hidden`.
- Reduced geometry to the core conformal/disformal/shadow-frame problem.
- Next target is parent no-extra-frame signature or finite `c_g/b_dis` bound runner.

## Bottleneck Formulas
{md_table([tables["formulas"][1], tables["formulas"][2], tables["formulas"][3]], ["formula_id", "name", "formula", "status"])}

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

    add("VAL4327_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4327_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4327_zero_rejected", "geometry zero rejected as not signed", any(r["audit_id"] == "AUD4327_0_full_zero_attempt" and r["status"] == "REJECTED_NOT_PARENT_SIGNED" for r in tables["audit"]), "audit")
    add("VAL4327_core_bound", "core frame bound formula exists", any(r["formula_id"] == "F4327_1_core_frame_bound" and "C_cg" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4327_source_bottleneck", "source-readout bottleneck formula exists", any(r["formula_id"] == "F4327_3_source_readout_bottleneck" and "Xi_src_hidden" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4327_frame_ledger", "frame ledger has core slots", {"c_s := D_Hperp ln A_s", "b_dis_s := D_Hperp B_s"}.issubset({r["symbol"] for r in tables["frames"]}), "frames")
    add("VAL4327_reject_AMF", "A_MF shortcut rejected", any(r["runner_id"] == "RUN4327_3_AMF_shortcut" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4327_next_runner", "next target is 4328", any("4328" in r["next_target"] for r in tables["next"]), "next")
    add("VAL4327_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4327_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4327_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4327_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4327_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4327_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4327_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4327_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4327_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4327_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4327_GEOMETRY_AUDIT.csv",
        "frames": SOURCE_DIR / "P8_Y5_R2FR_4327_CORE_FRAME_LEDGER.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4327_GEOMETRY_BOTTLENECK_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4327_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4327_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4327_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4327_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4327_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "frames": frame_rows(),
        "formulas": formula_rows(),
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
## PPC4161 4327 Dq geometry no-shadow or epsilon geom profile reduction

Marker: `{MARKER}`

4327 rejects full `Dq_geom[Hperp]=0` because `A_MF/no-shadow` remains unsigned, but it narrows the source-readout chain to `epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom_core + Xi_src_hidden`. The geometry core is the no-extra-frame/coframe-shadow problem: `c_s`, `b_dis_s`, `h_s^perp`, readout-frame, terminal-frame and hidden constitutive tails.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4327 packet geometry bottleneck

Marker: `{PACKET_MARKER}`

Packet update: after source-readout, matter, theta, tau and boundary/projector reductions, the direct source-readout bottleneck is geometry core plus `Xi_src_hidden`. Next: parent no-extra-frame signature or finite `c_g/b_dis` runner.
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
