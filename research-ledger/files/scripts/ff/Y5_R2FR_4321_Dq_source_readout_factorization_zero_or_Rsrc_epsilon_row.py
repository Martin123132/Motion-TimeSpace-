from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4321"
CLAIM_ID = "L-162"
BRANCH = "MTS_R2FR_Y5_DQ_SOURCE_READOUT_FACTORIZATION_ZERO_OR_RSRC_EPSILON_ROW_4321"
DECISION = "SOURCE_READOUT_INDEPENDENT_LEG_REMOVED_DEPENDENCY_BOUND_DERIVED_RSRC_RESIDUAL_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_SOURCE_READOUT_FACTORIZATION_ZERO_OR_RSRC_EPSILON_ROW_4321"
PACKET_MARKER = "PPC4161_PACKET_DQ_SOURCE_READOUT_FACTORIZATION_ZERO_OR_RSRC_EPSILON_ROW_4321"
NEXT_TARGET = "4322-Y5-R2FR-Dq-matter-descent-lift-or-geometry-theta-bound-row.md"

FORMAL_PATH = FORMAL / "337-PPC4161-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md"
DOC_PATH = POST / "4321-Y5-R2FR-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4321_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4321_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4320_NEXT_TARGET.csv",
        "Dq_source_readout[Hperp]",
        "4320 handoff selecting source/readout.",
    ),
    "SRC4321_01_quotient_natural": (
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "For any local observable/readout that factors before variation",
        "4219 quotient-natural readout zero theorem template.",
    ),
    "SRC4321_02_matter_domain": (
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "S_matter = Sbar[psi, g_obs(q), theta_obs]",
        "4265 standard matter-domain descent and source-prefactor tax.",
    ),
    "SRC4321_03_hilbert_source_readout": (
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "Q_src = Qbar_src[T_obs, g_obs, Sigma_obs, xi_obs]",
        "4266 standard Hilbert/ADM source-readout theorem.",
    ),
    "SRC4321_04_coefficient_tax": (
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "The surviving term:",
        "4266 coefficient drift is not source-readout zero.",
    ),
    "SRC4321_05_interface_guard": (
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "These rows block the obvious field-rename escapes",
        "4277 guard against hiding source-readout in other component rows.",
    ),
    "SRC4321_06_calibrated_coupling": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "no hidden source/readout dependence",
        "4178 structural GR/Newton source-coupling criterion.",
    ),
    "SRC4321_07_4319_pairing": (
        FORMAL / "335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md",
        "S_cg_nonHilbert = S_A Hperp^A + R_src_readout",
        "4319 explicit Rsrc split.",
    ),
    "SRC4321_08_4320_schema": (
        FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md",
        "source_factor_q_certificate",
        "4320 source-readout schema.",
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
            "4321 lifts the earlier 4266 Hilbert/ADM source-readout theorem into the newer Hperp source-support route without "
            "overclaiming. In the standard branch, the observed source charge is Q_src=Qbar_src[T_obs,g_obs,Sigma_obs,xi_obs] "
            "with ordinary matter already descended through Sbar_m[psi,g_obs(q),theta_obs]. Therefore there is no independent "
            "Hperp source-readout leg: any Dq_source_readout[Hperp] variation is inherited from matter, geometry, tau/reference, "
            "boundary/projector, theta/selector, or hidden source-weight residuals. The retained bound is epsilon_source_readout "
            "<= L_T epsilon_matter + L_g epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + "
            "L_theta epsilon_theta_marker + epsilon_SR_hidden, with R_src_readout bounded by hidden source weights, post-readout "
            "tails, projector commutators and worldtube-selector reentry. Coefficient drift such as delta kappa_cal Q_src is kept "
            "in Dq_coeff, not double-counted as R_src_readout. No local GR/Newton/R10/PPN/clock/orbital claim fires."
        ),
        (
            "4321 source register, factorization audit, zero-condition matrix, dependency-bound formulas, Rsrc residual ledger, "
            "component update, runner, firewall, decision, status, next-target and validation CSV."
        ),
        "private_source_readout_independent_leg_removed_dependency_bound_nonclaim",
        (
            "Close or bound epsilon_matter, epsilon_geom, epsilon_boundary_projector, epsilon_tau, epsilon_theta_marker, hidden "
            "source weights, post-readout tails, projector commutators and worldtube selector reentry before scoring local tests."
        ),
        (
            "Treating the 4266 standard Hilbert/ADM source-readout zero as Dq_source_readout[Hperp]=0 for arbitrary Hperp; hiding "
            "coefficient drift in source-readout; deleting collar/projector dependence; or claiming local GR/Newton while the "
            "dependent component epsilons remain open."
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
            "AUD4321_0_Qsrc_form",
            "Hilbert/ADM source charge is post-solution readout",
            "Q_src = Qbar_src[T_obs,g_obs,Sigma_obs,xi_obs]",
            "SIGNED_FOR_STANDARD_BRANCH_BY_4266",
            "This removes a free source-readout slot only in the declared standard branch.",
        ),
        (
            "AUD4321_1_matter_descent",
            "ordinary matter action descends through observed geometry and theta",
            "S_matter = Sbar_m[psi,g_obs(q),theta_obs]",
            "SIGNED_FOR_STANDARD_BRANCH_BY_4265_4277",
            "T_obs has no independent hidden source leg if the matter-domain branch is used.",
        ),
        (
            "AUD4321_2_Hperp_lift",
            "Hperp source-readout variation is inherited, not free",
            "delta_Hperp Q_src = DQbar_src[delta T_obs,delta g_obs,delta Sigma_obs,delta xi_obs]",
            "DERIVED_DEPENDENCY_BOUND",
            "This is the core lift: not zero unless inherited component variations vanish.",
        ),
        (
            "AUD4321_3_exact_zero",
            "exact source-readout zero condition",
            "epsilon_matter=epsilon_geom=epsilon_boundary_projector=epsilon_tau=epsilon_theta_marker=epsilon_SR_hidden=0",
            "CONDITIONAL_ZERO_ROUTE",
            "Then epsilon_source_readout=0; R_src_readout also needs hidden/readout tails zero.",
        ),
        (
            "AUD4321_4_coefficient_tax",
            "coefficient drift is not counted here",
            "delta(kappa_cal Q_src)=(delta kappa_cal)Q_src+kappa_cal delta Q_src",
            "Dq_coeff_RETAINED_NO_DOUBLE_COUNT",
            "4321 kills/bounds only the source-readout factor, not measured coupling drift.",
        ),
        (
            "AUD4321_5_Rsrc",
            "explicit Rsrc residual remains a separate no-cancellation envelope",
            "R_src_readout = R_hidden_weights + R_post_readout + R_projector_comm + R_worldtube_selector",
            "BOUND_ROW_REQUIRED",
            "This prevents deleting source labels or collars by notation.",
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
        ("ZC4321_0_matter", "epsilon_matter=0", "T_obs inherits no Hperp matter-domain variation", "Dq_matter route"),
        ("ZC4321_1_geometry", "epsilon_geom=0", "g_obs and Hodge/readout geometry inherit no Hperp variation", "Dq_geom route"),
        ("ZC4321_2_boundary", "epsilon_boundary_projector=0", "Sigma_obs/collar/projector readout is q-owned", "Dq_boundary_projector route"),
        ("ZC4321_3_tau", "epsilon_tau=0", "xi_obs/reference/time normal is q-owned", "Dq_tau route"),
        ("ZC4321_4_theta", "epsilon_theta_marker=0", "theta/species/selector marker does not reenter source readout", "Dq_theta_marker route"),
        ("ZC4321_5_hidden", "epsilon_SR_hidden=0", "no hidden source weights, post-readout tails, or source-label drift", "Rsrc route"),
        ("ZC4321_6_coeff", "epsilon_coeff handled outside source-readout", "delta kappa_cal Q_src remains in Dq_coeff", "no double count"),
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
            "F4321_0_chain_rule",
            "source-readout chain rule",
            "delta_Hperp Q_src = DQbar_src[delta_Hperp T_obs, delta_Hperp g_obs, delta_Hperp Sigma_obs, delta_Hperp xi_obs]",
            "4266 lifted to Hperp",
            "DERIVED",
        ),
        (
            "F4321_1_epsilon_source_readout",
            "dependency bound",
            "epsilon_source_readout <= L_T epsilon_matter + L_g epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + L_theta epsilon_theta_marker + epsilon_SR_hidden",
            "no-cancellation Lipschitz envelope",
            "BOUND_DERIVED_VALUES_MISSING",
        ),
        (
            "F4321_2_Rsrc",
            "explicit readout residual",
            "||R_src_readout|| <= R_hidden_weights + R_post_readout + R_projector_comm + R_worldtube_selector",
            "4319 residual split plus 4265/4266 exclusions",
            "BOUND_DERIVED_VALUES_MISSING",
        ),
        (
            "F4321_3_zero",
            "exact source-readout closure",
            "if all dependency epsilons and Rsrc residual rows are zero, then Dq_source_readout[Hperp]=0 and R_src_readout=0",
            "4321 zero-condition matrix",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "F4321_4_Nsrc_substitution",
            "4319 substitution",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp sqrt(sum_{i!=SR} w_i epsilon_i^2 + w_SR epsilon_source_readout^2)+||R_src_readout||)",
            "4319/4320 with 4321 dependency row",
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
        ("Rsrc_hidden_weights", "hidden source/species weights w_A(Phi)", "source-label drift before variation", "MISSING_ZERO_OR_BOUND", "not Dq_coeff unless it multiplies kappa_cal"),
        ("Rsrc_post_readout", "post-readout transfer tail", "readout applied after solving in a non-q-natural way", "MISSING_ZERO_OR_BOUND", "post-solution q-natural readout zeros it"),
        ("Rsrc_projector_comm", "source-readout projector commutator", "||[P_readout,Dq]Hperp||", "MISSING_ZERO_OR_BOUND", "can move to boundary/projector if q-owned"),
        ("Rsrc_worldtube_selector", "worldtube/collar selector reentry", "source surface changes before variation", "MISSING_ZERO_OR_BOUND", "owned by boundary/domain if not zero"),
        ("Rsrc_coeff_excluded", "delta kappa_cal Q_src", "coefficient drift", "RETAINED_IN_DQ_COEFF", "explicit no-double-count row"),
    ]
    rows: List[Dict[str, str]] = []
    for residual_id, residual, meaning, status, owner_note in specs:
        row = base_row()
        row.update({"residual_id": residual_id, "residual": residual, "meaning": meaning, "status": status, "owner_note": owner_note})
        rows.append(row)
    return rows


def component_update_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CU4321_0",
            "Dq_source_readout[Hperp]",
            "INDEPENDENT_LEG_REMOVED_DEPENDENCY_BOUND_RETAINED",
            "epsilon_source_readout <= L_T epsilon_matter + L_g epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + L_theta epsilon_theta_marker + epsilon_SR_hidden",
            "zero if dependency rows and Rsrc rows close",
        ),
        (
            "CU4321_1",
            "R_src_readout",
            "EXPLICIT_RESIDUAL_BOUND_RETAINED",
            "||R_src_readout|| <= R_hidden_weights + R_post_readout + R_projector_comm + R_worldtube_selector",
            "zero only if hidden/readout/collar tails close",
        ),
        (
            "CU4321_2",
            "Dq_coeff",
            "COEFFICIENT_TAX_RETAINED",
            "delta kappa_cal Q_src remains Dq_coeff, not source-readout",
            "prevents double counting",
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
        ("RUN4321_0_current", "current corpus", "USE_DEPENDENCY_BOUND", "source-readout independent leg removed; inherited epsilons remain", "no local claim"),
        ("RUN4321_1_exact_zero", "all dependency rows and Rsrc tails zero", "ALLOW_SOURCE_READOUT_ZERO", "epsilon_source_readout=0 and R_src_readout=0", "then remove source-readout from EDq/Nsrc"),
        ("RUN4321_2_finite_bound", "dependency epsilons sourced but nonzero", "ALLOW_NONCLAIM_BOUND", "feed dependency bound into 4319 Nsrc", "local tests still blocked"),
        ("RUN4321_3_coeff_shortcut", "coefficient drift counted as Rsrc to hide Dq_coeff", "REJECT", "delta kappa_cal Q_src belongs to Dq_coeff", "firewall"),
        ("RUN4321_4_generic_4266", "4266 zero applied to arbitrary Hperp without dependency rows", "REJECT", "4266 is standard-branch source-readout zero, not a blanket Hperp zero", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4321_0", "4266 cannot be used as a blanket Dq_source_readout[Hperp]=0 theorem.", "BLOCK_BLANKET_ZERO"),
        ("FW4321_1", "Coefficient drift stays in Dq_coeff and must not be hidden in R_src_readout.", "BLOCK_DOUBLE_COUNT_OR_ERASURE"),
        ("FW4321_2", "Worldtube/collar/projector dependence stays explicit unless q-owned.", "BLOCK_COLLAR_ERASURE"),
        ("FW4321_3", "Finite Lipschitz constants are nonclaim until sourced or theorem-owned.", "BLOCK_NUMERIC_CLAIM"),
        ("FW4321_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked until dependent component gates close.", "BLOCK_LOCAL_TEST_CLAIM"),
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
            "decision_id": "DEC4321_0",
            "result": DECISION,
            "reason": "The standard Hilbert/ADM source-readout theorem removes an independent source-readout slot, but Hperp closure now depends on matter, geometry, boundary/projector, tau, theta and explicit Rsrc tails.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4321_0", "source_readout_independent_leg", "REMOVED_CONDITIONALLY", "standard Hilbert/ADM branch has no free Q_src slot"),
        ("STAT4321_1", "epsilon_source_readout", "DEPENDENCY_BOUND_DERIVED", "requires dependent epsilon rows and Lipschitz constants"),
        ("STAT4321_2", "R_src_readout", "RESIDUAL_RETAINED", "hidden weights/readout/projector/collar tails remain explicit"),
        ("STAT4321_3", "Dq_coeff", "RETAINED", "coupling drift is not solved here"),
        ("STAT4321_4", "local_claim", "BLOCKED", "no local GR/Newton/test claim fires"),
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
            "next_target_id": "NT4321_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can Dq_matter[Hperp] be lifted from the 4265 matter-domain descent into a geometry/theta dependency bound, reducing another independent Dq component?",
            "preferred_route": "derive delta_Hperp S_matter through g_obs(q) and theta_obs(q), with no direct hidden matter slot",
            "fallback_route": "write epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden as a nonclaim row",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 337 - PPC4161 Dq source-readout factorization zero or Rsrc epsilon row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, Newtonian mechanics, R10, PPN, clock safety, orbital safety, or a numerical value of `G_N`.

## Result

The older 4266 Hilbert/ADM source-readout theorem is usable, but only in the disciplined way. It removes an independent source-readout leg in the standard branch:

```text
Q_src = Qbar_src[T_obs, g_obs, Sigma_obs, xi_obs].
```

For `Hperp`, that does **not** mean a free zero. It means:

```text
delta_Hperp Q_src = DQbar_src[delta_Hperp T_obs, delta_Hperp g_obs, delta_Hperp Sigma_obs, delta_Hperp xi_obs].
```

So `Dq_source_readout[Hperp]` is now a dependency-bound component, not a mysterious free coupling. It vanishes only if the matter, geometry, boundary/projector, tau/reference, theta/selector and hidden source-readout tails vanish.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Factorization Audit
{md_table(tables["audit"], ["audit_id", "clause", "statement", "status", "implication"])}

## Zero Conditions
{md_table(tables["zero"], ["condition_id", "condition", "implication", "owner_component"])}

## Bound Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "basis", "status"])}

## Rsrc Residual Ledger
{md_table(tables["residuals"], ["residual_id", "residual", "meaning", "status", "owner_note"])}

## Component Update
{md_table(tables["component_update"], ["update_id", "component", "status", "new_row", "zero_condition"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4321 - Dq source-readout factorization zero or Rsrc epsilon row

## Verdict

- Removed the independent standard-branch source-readout leg using the 4266 Hilbert/ADM theorem.
- Did **not** claim blanket `Dq_source_readout[Hperp]=0`.
- Derived the honest dependency bound for `epsilon_source_readout`.
- Kept `R_src_readout` tails and `Dq_coeff` coupling drift explicit.

## Main Bound
{md_table([tables["formulas"][1], tables["formulas"][2], tables["formulas"][4]], ["formula_id", "name", "formula", "status"])}

## Residual Ledger
{md_table(tables["residuals"], ["residual_id", "residual", "status", "owner_note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
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

    add("VAL4321_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4321_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4321_audit_lift", "Hperp chain-rule lift exists", any(r["audit_id"] == "AUD4321_2_Hperp_lift" and r["status"] == "DERIVED_DEPENDENCY_BOUND" for r in tables["audit"]), "audit")
    add("VAL4321_no_blanket_zero", "blanket zero is rejected", any(r["runner_id"] == "RUN4321_4_generic_4266" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4321_dependency_formula", "dependency formula includes matter and geometry", any("epsilon_matter" in r["formula"] and "epsilon_geom" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4321_Rsrc_formula", "Rsrc formula includes hidden and projector terms", any("R_hidden_weights" in r["formula"] and "R_projector_comm" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4321_coeff_not_double_counted", "coefficient tax retained outside Rsrc", any(r["residual_id"] == "Rsrc_coeff_excluded" and r["status"] == "RETAINED_IN_DQ_COEFF" for r in tables["residuals"]), "residuals")
    add("VAL4321_zero_conditions", "zero condition matrix has at least six rows", len(tables["zero"]) >= 6, "zero")
    add("VAL4321_component_update", "component update marks independent leg removed", any("INDEPENDENT_LEG_REMOVED" in r["status"] for r in tables["component_update"]), "component_update")
    add("VAL4321_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4321_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    add("VAL4321_next_target", "next target is 4322", any("4322" in r["next_target"] for r in tables["next"]), "next")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4321_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4321_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4321_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4321_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4321_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4321_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4321_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4321_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4321_SOURCE_READOUT_FACTORIZATION_AUDIT.csv",
        "zero": SOURCE_DIR / "P8_Y5_R2FR_4321_SOURCE_READOUT_ZERO_CONDITIONS.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4321_SOURCE_READOUT_DEPENDENCY_FORMULAS.csv",
        "residuals": SOURCE_DIR / "P8_Y5_R2FR_4321_RSRC_RESIDUAL_LEDGER.csv",
        "component_update": SOURCE_DIR / "P8_Y5_R2FR_4321_COMPONENT_UPDATE.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4321_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4321_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4321_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4321_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4321_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "zero": zero_condition_rows(),
        "formulas": formula_rows(),
        "residuals": residual_rows(),
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
## PPC4161 4321 Dq source-readout factorization zero or Rsrc epsilon row

Marker: `{MARKER}`

4321 removes the independent standard-branch source-readout leg by importing the 4266 Hilbert/ADM theorem, but it refuses the blanket zero shortcut. For `Hperp`, `Dq_source_readout[Hperp]` is dependency-bound by matter, geometry, boundary/projector, tau/reference, theta/selector and hidden source-readout tails; `R_src_readout` remains explicit, and coefficient drift stays in `Dq_coeff`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4321 packet source-readout dependency row

Marker: `{PACKET_MARKER}`

Packet update: source-readout is no longer a free mystery coupling in the standard Hilbert/ADM branch. The remaining cost is an inherited dependency envelope plus explicit `R_src_readout` tails. Next target: lift `Dq_matter[Hperp]` through the matter-domain theorem or bound it by geometry/theta terms.
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
