from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4328"
CLAIM_ID = "L-169"
BRANCH = "MTS_R2FR_Y5_PARENT_NO_EXTRA_FRAME_SIGNATURE_OR_CG_BDIS_BOUND_RUNNER_4328"
DECISION = "ORDINARY_MATTER_GX_BDIS_ZERO_LIFTED_CONDITIONALLY_FULL_FRAME_RUNNER_RETAINS_EM_COEFF_XI_TAILS_NONCLAIM"
MARKER = "PPC4161_PARENT_NO_EXTRA_FRAME_SIGNATURE_OR_CG_BDIS_BOUND_RUNNER_4328"
PACKET_MARKER = "PPC4161_PACKET_PARENT_NO_EXTRA_FRAME_SIGNATURE_OR_CG_BDIS_BOUND_RUNNER_4328"
NEXT_TARGET = "4329-Y5-R2FR-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md"

FORMAL_PATH = FORMAL / "344-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md"
DOC_PATH = POST / "4328-Y5-R2FR-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4328_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4328_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4327_NEXT_TARGET.csv",
        "parent no-extra-frame/no-shadow action-domain signature",
        "4327 handoff selecting no-extra-frame or c_g/b_dis runner.",
    ),
    "SRC4328_01_4272": (
        FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md",
        "Current evidence does not sign it",
        "4272 public no-extra-frame still unsigned; finite runner required.",
    ),
    "SRC4328_02_projection": (
        FORMAL / "289-PPC4161-cg-bdis-projection-input-fill-or-parent-no-extra-frame-action-signature.md",
        "|N_X c_g| <= 0.00578792",
        "4273 PPN projection contract and b_dis separation.",
    ),
    "SRC4328_03_product": (
        FORMAL / "290-PPC4161-parent-NX-cg-product-or-no-extra-frame-action-domain-proof.md",
        "alpha_eff = |N_X c_g| = |c_g|/sqrt(Z_X)",
        "4274 product reduction.",
    ),
    "SRC4328_04_gX": (
        FORMAL / "291-PPC4161-parent-cg-zero-theorem-or-ZX-cg-source-row.md",
        "g_X := d ln A_g/d phi_X = c_g/sqrt(Z_X)",
        "4275 invariant coupling.",
    ),
    "SRC4328_05_terminal_reject": (
        FORMAL / "292-PPC4161-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md",
        "terminal public metric/coframe object e_pub exists",
        "4276 rejects terminal-metric shortcut.",
    ),
    "SRC4328_06_matter_zero": (
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "g_X = d ln A_g/dphi_X = 0",
        "4277 standard-branch ordinary matter g_X/b_dis zero.",
    ),
    "SRC4328_07_geometry_bottleneck": (
        FORMAL / "343-PPC4161-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md",
        "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom_core + Xi_src_hidden",
        "4327 narrowed source-readout bottleneck.",
    ),
    "SRC4328_08_EM_Hodge": (
        FORMAL / "331-PPC4161-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md",
        "hidden/motion/time field defines a disformal or medium-like EM Hodge star",
        "4315 EM/Hodge hidden-frame tail remains a separate gate.",
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
            "4328 lifts the 4277 matter-interface action-domain proof into the narrowed 4327 geometry bottleneck. In the standard "
            "ordinary-matter branch, S_matter[Psi;Phi]=Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))] gives delta_v S_matter=0 for "
            "vertical Hperp variations, so the ordinary conformal/disformal shadow-frame couplings vanish: g_X=d ln A_g/dphi_X=0 "
            "and b_dis=0. This does not close the full geometry gate: public parent no-extra-frame/no-shadow remains unsigned, "
            "terminal public metric alone is rejected, EM/Hodge constitutive frame slots, coefficient drift and Xi_src_hidden remain. "
            "The finite nonstandard runner is canonical, not raw-c_g: alpha_eff=|g_X|=|c_g|/sqrt(Z_X), with the diagnostic local PPN "
            "contract |g_X|<=0.00578792 before tails, while b_dis requires a separate preferred-frame/clock/orbital projection or a zero theorem. "
            "No local GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4328 source register, no-extra-frame audit, ordinary matter zero row, canonical gX/bdis runner schema, residual-tail ledger, "
            "source-readout update, runner, firewall, decision, status, next-target and validation CSV."
        ),
        "private_ordinary_matter_gX_bdis_zero_full_geometry_runner_retained_nonclaim",
        (
            "Close or bound EM/Hodge constitutive frame tail, coefficient drift, Xi_src_hidden, source-backed gX/bdis values and projection constants."
        ),
        (
            "Comparing raw c_g to Cassini/R10/clock bounds; using terminal metric as no-frame proof; treating ordinary matter g_X=0 as full geometry zero; "
            "hiding EM/Hodge/disformal tails; or claiming local GR/Newton while Xi/EM/coefficient/local-test gates remain open."
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
            "AUD4328_0_public_signature",
            "public parent no-extra-frame",
            "S_ord=sum_A S_A[Psi_A,e_obs(q),omega[e_obs],theta_A] with no A_g,B_dis,h_perp,source-only,post-readout or hidden Hodge frame slot",
            "NOT_GLOBAL_PARENT_SIGNED",
            "full geometry zero cannot be claimed",
        ),
        (
            "AUD4328_1_terminal_shortcut",
            "terminal metric shortcut",
            "terminal public metric/coframe alone does not exclude pre-readout matter frame slots",
            "REJECTED",
            "must use action-domain exclusion, not category slogan",
        ),
        (
            "AUD4328_2_ordinary_matter",
            "ordinary matter action-domain",
            "S_matter=Sbar_m[Psi,g_obs(q),theta_obs(q)] implies g_X=0 and b_dis=0 for ordinary matter in the standard branch",
            "CONDITIONAL_ZERO_LIFTED",
            "ordinary matter shadow-frame coupling removed on this branch",
        ),
        (
            "AUD4328_3_canonical_runner",
            "canonical finite coupling",
            "g_X=c_g/sqrt(Z_X), alpha_eff=|g_X|, diagnostic |g_X|<=0.00578792 before tails",
            "RUNNER_SCHEMA_READY",
            "raw c_g is not scoreable",
        ),
        (
            "AUD4328_4_full_geometry",
            "remaining full geometry tails",
            "EM/Hodge constitutive frame, coefficient drift, Xi_src_hidden, readout-frame/terminal tails and local projections remain",
            "TAILS_RETAINED",
            "local GR still blocked",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for audit_id, clause, statement, status, implication in specs:
        row = base_row()
        row.update({"audit_id": audit_id, "clause": clause, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def zero_rows() -> List[Dict[str, str]]:
    specs = [
        ("ZERO4328_0_gX_matter", "ordinary matter g_X", "g_X=d ln A_g/dphi_X=0", "standard matter-interface action-domain branch", "CONDITIONAL_ZERO"),
        ("ZERO4328_1_bdis_matter", "ordinary matter b_dis", "b_dis=0", "standard matter-interface action-domain branch", "CONDITIONAL_ZERO"),
        ("ZERO4328_2_hperp_matter", "ordinary matter h_s^perp", "D_Hperp h_s^perp=0 if no independent shadow-frame slot exists", "same action-domain exclusion", "CONDITIONAL_ZERO"),
        ("ZERO4328_3_EM_Hodge", "EM/Hodge frame slot", "not closed by ordinary matter descent", "same-Hodge/constitutive owner gate", "RETAINED"),
        ("ZERO4328_4_coeff", "coefficient/coupling drift", "not closed by ordinary matter descent", "Dq_coeff/calibrated coupling gate", "RETAINED"),
        ("ZERO4328_5_Xi", "hidden source-prefactor tails", "not closed by ordinary matter descent", "Xi_src_hidden gate", "RETAINED"),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, item, zero_statement, owner, status in specs:
        row = base_row()
        row.update({"row_id": row_id, "item": item, "zero_statement": zero_statement, "owner": owner, "status": status})
        rows.append(row)
    return rows


def runner_schema_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUNSC4328_0_gX", "g_X", "canonical conformal coupling", "dimensionless/canonical field inverse", "parent zero or source-backed value", "False"),
        ("RUNSC4328_1_alpha_eff", "alpha_eff", "PPN scalar response", "dimensionless", "alpha_eff=|g_X| under unit response before tails", "False"),
        ("RUNSC4328_2_ppn_bound", "alpha_eff_bound", "diagnostic Cassini/PPN contract", "dimensionless", "0.00578792", "False"),
        ("RUNSC4328_3_bdis", "b_dis", "disformal/preferred-frame coupling", "projection-dependent", "zero theorem or projection matrix", "False"),
        ("RUNSC4328_4_ZX", "Z_X", "canonical normalization guard", "positive kinetic coefficient", "only for raw c_g conversion, not final score", "False"),
        ("RUNSC4328_5_tails", "tail_guard_sum", "non-gX residuals", "arena residual norm", "absolute no-cancellation sum", "False"),
        ("RUNSC4328_6_projection", "arena_projection", "PPN/R10/clock/orbital projection constants", "arena-specific", "source-backed matrices", "False"),
    ]
    rows: List[Dict[str, str]] = []
    for schema_id, symbol, meaning, units, required_value, valid_for_claim in specs:
        row = base_row()
        row.update(
            {
                "schema_id": schema_id,
                "symbol": symbol,
                "meaning": meaning,
                "units_or_type": units,
                "required_value": required_value,
                "value_valid_for_claim": valid_for_claim,
            }
        )
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4328_0_ordinary_zero",
            "ordinary matter no-extra-frame zero",
            "S_matter=Sbar_m[Psi,g_obs(q),theta_obs(q)] and Dq[Hperp]=0 => g_X=0 and b_dis=0 for ordinary matter in the standard branch",
            "4277 lifted into 4327 bottleneck",
            "CONDITIONAL_ZERO_DERIVED",
        ),
        (
            "F4328_1_canonical_gX",
            "canonical frame coupling",
            "g_X := d ln A_g/dphi_X = c_g/sqrt(Z_X), alpha_eff=|g_X|",
            "4274/4275 invariantization",
            "CANONICAL_RUNNER_SCHEMA",
        ),
        (
            "F4328_2_ppn_contract",
            "diagnostic PPN contract",
            "|g_X| <= 0.00578792 before non-gX tails, range/profile factors and projection guards",
            "4273/4275",
            "DIAGNOSTIC_NOT_CLAIM",
        ),
        (
            "F4328_3_bdis_route",
            "b_dis route",
            "b_dis=0 by action-domain no-disformal slot, otherwise require preferred-frame/clock/orbital projection matrix and absolute tail sum",
            "4273/4277",
            "ZERO_OR_BOUND_ROUTE",
        ),
        (
            "F4328_4_geometry_core_update",
            "geometry core update",
            "epsilon_geom_core <= C_EMframe epsilon_EM_Hodge_frame + C_coeff epsilon_coeff + C_readout epsilon_readout_frame + C_terminal epsilon_terminal + tail_guard_sum after ordinary matter g_X=b_dis=0",
            "4327 plus F4328_0",
            "REDUCED_BUT_OPEN",
        ),
        (
            "F4328_5_source_readout_update",
            "source-readout update",
            "epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom_core_reduced + Xi_src_hidden",
            "4327 plus F4328_4",
            "NONCLAIM_HANDOFF",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, basis, status in specs:
        row = base_row()
        row.update({"formula_id": formula_id, "name": name, "formula": formula, "basis": basis, "status": status})
        rows.append(row)
    return rows


def residual_rows() -> List[Dict[str, str]]:
    specs = [
        ("RES4328_0_EM_Hodge", "epsilon_EM_Hodge_frame", "hidden/disformal EM Hodge or constitutive frame slot", "Dq_EM/Hodge owner", "MISSING_ZERO_OR_BOUND"),
        ("RES4328_1_coeff", "epsilon_coeff", "coefficient/coupling drift or calibrated constant leakage", "Dq_coeff", "MISSING_ZERO_OR_BOUND"),
        ("RES4328_2_readout", "epsilon_readout_frame", "post-readout frame slot", "readout/frame guard", "MISSING_ZERO_OR_BOUND"),
        ("RES4328_3_terminal", "epsilon_terminal", "terminal metric/readout mismatch", "terminal/public metric guard", "MISSING_ZERO_OR_BOUND"),
        ("RES4328_4_Xi", "Xi_src_hidden", "hidden source-prefactor master tail", "4324", "MISSING_ZERO_OR_BOUND"),
        ("RES4328_5_projection", "tail_guard_sum", "non-gX projection/tail residuals", "finite local runner", "MISSING_ZERO_OR_BOUND"),
    ]
    rows: List[Dict[str, str]] = []
    for residual_id, symbol, meaning, owner, status in specs:
        row = base_row()
        row.update({"residual_id": residual_id, "symbol": symbol, "meaning": meaning, "owner": owner, "status": status})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUN4328_0_standard_matter", "standard ordinary matter action-domain branch", "ALLOW_GX_BDIS_MATTER_ZERO", "g_X=b_dis=0 for ordinary matter", "full geometry still open"),
        ("RUN4328_1_public_parent", "public parent signs no-extra-frame for matter+EM+readouts", "ALLOW_GEOMETRY_CORE_ZERO", "epsilon_geom_core=0 if Xi/coeff/tails also zero", "not current corpus"),
        ("RUN4328_2_finite_gX", "source-backed canonical g_X and tail guards", "ALLOW_NONCLAIM_BOUND", "finite local projection runner", "claim only after all projection rows valid"),
        ("RUN4328_3_raw_cg", "compare raw c_g to local bounds", "REJECT", "use g_X=c_g/sqrt(Z_X)", "firewall"),
        ("RUN4328_4_terminal_shortcut", "terminal public metric implies no shadow frame", "REJECT", "action-domain exclusion required", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4328_0", "Do not compare raw c_g to PPN/R10/clock/orbital bounds; use canonical g_X and projection/tail guards.", "BLOCK_RAW_CG_SCORE"),
        ("FW4328_1", "Terminal public metric/coframe does not by itself prove no-extra-frame action-domain exclusion.", "BLOCK_TERMINAL_SHORTCUT"),
        ("FW4328_2", "Ordinary matter g_X=b_dis=0 does not erase EM/Hodge constitutive, coefficient, readout-frame or Xi tails.", "BLOCK_FULL_GEOMETRY_OVERCLAIM"),
        ("FW4328_3", "b_dis needs its own zero theorem or preferred-frame/clock/orbital projection matrix.", "BLOCK_BDIS_UNSCORED"),
        ("FW4328_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until EM/Hodge, coefficient, Xi and projection gates close.", "BLOCK_LOCAL_TEST_CLAIM"),
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
            "decision_id": "DEC4328_0",
            "result": DECISION,
            "reason": "4277 closes ordinary matter g_X/b_dis in the standard action-domain branch, but full public geometry/no-shadow still needs EM/Hodge, coefficient, Xi and projection gates or a source-backed canonical runner.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4328_0", "ordinary_matter_frame", "CONDITIONAL_ZERO_LIFTED", "g_X=b_dis=0 in standard ordinary matter branch"),
        ("STAT4328_1", "full_geometry_core", "OPEN", "EM/Hodge, coefficient, readout and Xi tails remain"),
        ("STAT4328_2", "finite_runner", "SCHEMA_READY_NONCLAIM", "canonical g_X/b_dis runner defined"),
        ("STAT4328_3", "EM_Hodge", "NEXT_TARGET", "hidden Hodge/constitutive frame tail blocks full geometry"),
        ("STAT4328_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
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
            "next_target_id": "NT4328_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can Dq_EM[Hperp] and the hidden Hodge/constitutive frame tail be zeroed in the same-Hodge Maxwell branch, or must EM constitutive tails feed the geometry/source-readout runner?",
            "preferred_route": "prove same-Hodge Maxwell/EM action-domain ownership with no hidden/disformal EM metric or constitutive frame slot",
            "fallback_route": "retain epsilon_EM_Hodge_frame and Delta_Hodge_EM as finite local EM/clock/PPN projection tails",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 344 - PPC4161 parent no-extra-frame signature or c_g/b_dis bound runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove full `Dq_geom[Hperp]=0`, local GR, Newtonian mechanics, R10, PPN, WEP, clock safety, orbital safety, Maxwell closure, or a numerical value of `G_N`.

## Result

The ordinary-matter frame part **does** close in the standard action-domain branch:

```text
S_matter[Psi;Phi]=Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))]
=> g_X=d ln A_g/dphi_X=0,
=> b_dis=0.
```

But full geometry/no-shadow does **not** close globally. The public no-extra-frame signature is still unsigned, terminal metric alone is rejected, and EM/Hodge, coefficient, readout-frame and `Xi_src_hidden` tails remain.

The finite runner is canonical:

```text
g_X := c_g/sqrt(Z_X),
alpha_eff=|g_X|,
|g_X| <= 0.00578792
```

before non-`g_X` tails and only with source-backed projection rows.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## No-Extra-Frame Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Zero Rows
{md_table(tables["zero"], ["row_id", "item", "zero_statement", "owner", "status"])}

## Runner Schema
{md_table(tables["schema"], ["schema_id", "symbol", "meaning", "units_or_type", "required_value", "value_valid_for_claim"])}

## Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "basis", "status"])}

## Residual Tails
{md_table(tables["residuals"], ["residual_id", "symbol", "meaning", "owner", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4328 - parent no-extra-frame signature or c_g/b_dis bound runner

## Verdict

- Lifted ordinary matter `g_X=b_dis=0` in the standard action-domain branch.
- Rejected raw `c_g` scoring and terminal-metric shortcut.
- Kept full geometry open through EM/Hodge, coefficient, readout-frame and `Xi_src_hidden` tails.
- Next target is Dq_EM/Hodge constitutive ownership.

## Core Formulas
{md_table([tables["formulas"][0], tables["formulas"][1], tables["formulas"][4]], ["formula_id", "name", "formula", "status"])}

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

    add("VAL4328_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4328_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4328_matter_zero", "ordinary matter gX zero row exists", any(r["row_id"] == "ZERO4328_0_gX_matter" and r["status"] == "CONDITIONAL_ZERO" for r in tables["zero"]), "zero")
    add("VAL4328_bdis_zero", "ordinary matter bdis zero row exists", any(r["row_id"] == "ZERO4328_1_bdis_matter" and r["status"] == "CONDITIONAL_ZERO" for r in tables["zero"]), "zero")
    add("VAL4328_raw_cg_blocked", "raw c_g scoring rejected", any(r["runner_id"] == "RUN4328_3_raw_cg" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4328_terminal_blocked", "terminal shortcut rejected", any(r["runner_id"] == "RUN4328_4_terminal_shortcut" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4328_schema_gX", "runner schema includes g_X and b_dis", {"g_X", "b_dis"}.issubset({r["symbol"] for r in tables["schema"]}), "schema")
    add("VAL4328_formula_canonical", "canonical gX formula exists", any(r["formula_id"] == "F4328_1_canonical_gX" and "c_g/sqrt(Z_X)" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4328_full_tails_retained", "EM and coefficient tails retained", {"epsilon_EM_Hodge_frame", "epsilon_coeff"}.issubset({r["symbol"] for r in tables["residuals"]}), "residuals")
    add("VAL4328_next_EM", "next target is EM/Hodge", any("EM-Hodge" in r["next_target"] for r in tables["next"]), "next")
    add("VAL4328_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4328_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4328_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4328_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4328_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4328_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4328_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4328_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4328_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4328_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4328_NO_EXTRA_FRAME_AUDIT.csv",
        "zero": SOURCE_DIR / "P8_Y5_R2FR_4328_ORDINARY_MATTER_FRAME_ZERO_ROWS.csv",
        "schema": SOURCE_DIR / "P8_Y5_R2FR_4328_CG_BDIS_RUNNER_SCHEMA.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4328_FRAME_RUNNER_FORMULAS.csv",
        "residuals": SOURCE_DIR / "P8_Y5_R2FR_4328_FRAME_RESIDUAL_TAILS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4328_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4328_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4328_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4328_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4328_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "zero": zero_rows(),
        "schema": runner_schema_rows(),
        "formulas": formula_rows(),
        "residuals": residual_rows(),
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
## PPC4161 4328 parent no-extra-frame signature or c_g/b_dis bound runner

Marker: `{MARKER}`

4328 lifts the 4277 matter-interface action-domain proof into the narrowed geometry chain: ordinary matter has `g_X=b_dis=0` in the standard branch. Full geometry/no-shadow remains open because public parent no-extra-frame is unsigned and EM/Hodge, coefficient, readout-frame and `Xi_src_hidden` tails remain. The finite runner must score canonical `g_X=c_g/sqrt(Z_X)`, never raw `c_g`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4328 packet no-extra-frame runner

Marker: `{PACKET_MARKER}`

Packet update: ordinary matter frame coupling is zero in the standard action-domain branch, but the full geometry bottleneck now shifts to EM/Hodge constitutive frame tails, coefficient drift, `Xi_src_hidden`, and source-backed canonical `g_X/b_dis` runner rows.
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
