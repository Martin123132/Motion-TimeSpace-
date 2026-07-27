from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_ID,
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2027-Y5-R2FR-vZ-cross-coupling-operator-or-first-numeric-leak-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2027_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2027*vZ*")) or any(FORMALIZATION.rglob("*2027*coupling*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2027_00_2026_handoff",
            ROOT / "2026-Y5-R2FR-parent-q-Dq-matrix-field-action-or-first-vZ-DObs-row.md",
            ["NEXT2026_0_2027", "CZB2026_0_mixed_hessian", "VAL2026_OVERALL"],
            "2026 handoff selects C_ZB/J_B^Z or first finite v_Z leak bound.",
        ),
        (
            "SRC2027_01_2026_coupling_csv",
            OUT / "P8_Y5_PARENT_QLOC_2026_VZ_ACTION_COUPLING_OBSTRUCTION.csv",
            ["CZB2026_0_mixed_hessian", "CZB2026_5_verdict"],
            "machine-readable C_ZB target from 2026.",
        ),
        (
            "SRC2027_02_1009_parent_contract",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_9_total_parent_contract", "CG1009_0_total_parent_action", "DEC1009_0_contract_not_parent_action"],
            "parent current-chain action contract remains useful but unpromoted.",
        ),
        (
            "SRC2027_03_1023_action_descent",
            ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            ["QVC1023_2_action_descent", "CDA1023_4_verdict", "DEC1023_2_future_reopen"],
            "q/vX/action descent certificate failure and future reopen condition.",
        ),
        (
            "SRC2027_04_1540_selector",
            ROOT / "1540-Y5-parent-coupling-selector-source-silence-attempt.md",
            ["CSEL1540_0_candidate_theorem", "VAR1540_0_matter_variation", "VAR1540_1_stress_not_zero"],
            "selector theorem and stress-shortcut refusal.",
        ),
        (
            "SRC2027_05_1666_object_language",
            ROOT / "1666-Y5-R2FR-coupling-vertical-generator-parent-object-language-or-residual-bound-handoff.md",
            ["THM1666_0_statement", "BLK1666_5_coupling_double_zero", "RBH1666_5_coupling_slope"],
            "conditional local unobservability theorem and residual coupling-slope handoff.",
        ),
        (
            "SRC2027_06_1473_double_zero",
            ROOT / "1473-Y5-R10-RAB-parent-coupling-double-zero-theorem-or-executable-residual-vector.md",
            ["DZ1473_0_taylor_lemma", "DZ1473_4_verdict", "ERV1473_1_source_weight"],
            "double-zero theorem and executable residual-vector fallback.",
        ),
        (
            "SRC2027_07_1885_source_coupling",
            ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
            ["CG1885_2_source_coupling_zero", "PSTAT1885_1_bottleneck", "VAL1885_OVERALL"],
            "source coupling remains the main local bottleneck.",
        ),
        (
            "SRC2027_08_1937_hilbert",
            ROOT / "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
            ["HST1937_0_variational_source_owner", "HST1937_3_verdict", "VAL1937_OVERALL"],
            "minimal Hilbert source coupling signature candidate.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def coupling_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "CZD2027_0_parent_split",
            "parent action split",
            "S_parent[B,Z,U,psi]=S_EH[B]+S_matter[B,psi,theta]+S_Z[B,Z,U]+S_boundary[B,Z,U].",
            "DEFINITIONAL_NORMAL_FORM",
            "This exposes every way the quotient-invisible Z sector can still source visible geometry.",
            "parent Lagrangian not yet signed as the MTS action",
        ),
        (
            "CZD2027_1_visible_euler",
            "visible Euler equation",
            "E_B := delta S_parent/delta B = E_EH[B]+E_matter[B,psi]+J_B^Z+J_B^boundary.",
            "DERIVED_VARIATION_IDENTITY",
            "Local GR requires the extra visible source terms to vanish or be bounded.",
            "J_B^Z and boundary source are not computed from a parent action",
        ),
        (
            "CZD2027_2_mixed_operator",
            "cross-coupling operator",
            "C_ZB := delta J_B^Z/delta Z |branch = delta^2 S_Z/(delta B delta Z)|branch.",
            "DERIVED_OPERATOR_DEFINITION",
            "This is the exact coefficient that decides whether a Z displacement leaks into GR equations at first order.",
            "no source-backed S_Z sector or mixed Hessian convention",
        ),
        (
            "CZD2027_3_Dq_zero_insufficient",
            "Dq-zero limitation",
            "Dq[v_Z]=0 can make observed readout invariant, but it does not imply J_B^Z=0; metric-dependent Z energy still gravitates.",
            "NO_SHORTCUT_THEOREM",
            "This prevents us from mistaking kinematic quotient invisibility for dynamical local-GR recovery.",
            "requires either action descent/topological sector or finite source bound",
        ),
        (
            "CZD2027_4_exact_silence_system",
            "exact vZ silence conditions",
            "Dq[v_Z]=0, J_B^Z=0, C_ZB=0, partial_Z readout=0, Q_Z=0, and tau projectability together imply first-order local v_Z silence.",
            "EXACT_CONDITIONAL_THEOREM",
            "This is the least-cheatable local-GR bridge from the Z side.",
            "six premises are unsigned together",
        ),
        (
            "CZD2027_5_verdict",
            "2027 coupling verdict",
            "The coupling problem is now reduced to a parent action theorem or finite residual vector: prove topological/constraint/double-zero Z silence, or bound J_B^Z and C_ZB.",
            "THEOREM_TARGET_NOT_CLAIMED",
            "We are no longer circling: the next testable object is a mixed visible-fiber source operator.",
            "C_ZB/J_B^Z source rows missing",
        ),
    ]
    rows = []
    for row_id, obj, statement, status, implication, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": obj,
                "statement": statement,
                "status": status,
                "implication": implication,
                "blocker": blocker,
            }
        )
        rows.append(row)
    return rows


def no_go_rows() -> list[dict[str, object]]:
    data = [
        (
            "NGZ2027_0_canonical_bulk_Z",
            "canonical local Z bulk action",
            "If S_Z contains sqrt(-g_obs)[-1/2 K(Z)(nabla Z)^2 - V(Z)], then delta S_Z/delta g_obs gives a Z stress tensor.",
            "GENERICALLY_VISIBLE",
            "A normal energy-carrying Z field is not locally GR-silent merely because q ignores Z.",
            "need vacuum double-zero/topological/constraint route or finite stress bound",
        ),
        (
            "NGZ2027_1_vacuum_double_zero",
            "local vacuum double-zero",
            "If nabla Z_0=0, V(Z_0)=0, V'(Z_0)=0, direct matter/readout Z-couplings vanish, and boundary charge is zero, then J_B^Z=0 and C_ZB=0 at first order for the canonical scalar prototype.",
            "EXACT_CONDITIONAL_ESCAPE",
            "This is a real derivation route: first-order local leakage dies, second-order leakage remains bounded by mass/amplitude.",
            "Z_0, potential, mass gap, direct couplings, and boundary conditions are not sourced",
        ),
        (
            "NGZ2027_2_topological_exact_sector",
            "topological/exact sector",
            "If S_Z is metric-independent up to an exact boundary term with Q_Z=0/proper, then J_B^Z=0 and C_ZB=0.",
            "EXACT_CONDITIONAL_ESCAPE",
            "This would be the cleanest local-GR route, but only if it follows from the parent action rather than declaration.",
            "no parent topological/exact certificate",
        ),
        (
            "NGZ2027_3_constraint_sector",
            "first-class constraint sector",
            "If Z is removed by a first-class constraint with closed bracket, zero edge charge, and no matter descent leak, no physical local Z stress remains.",
            "EXACT_CONDITIONAL_ESCAPE",
            "This matches the quotient route but needs the full constraint certificate.",
            "Omega/DC_X/bracket/degree count remain unsigned",
        ),
        (
            "NGZ2027_4_nonzero_vacuum_energy",
            "nonzero Z vacuum energy",
            "If V(Z_0) != 0 or boundary energy is nonzero, J_B^Z contributes a cosmological-constant/source term even when V'(Z_0)=0.",
            "FAILS_EXACT_LOCAL_GR_SILENCE",
            "Stationarity is not enough; zero energy/source level is separately required.",
            "vacuum subtraction/reference owner missing",
        ),
        (
            "NGZ2027_5_direct_source_slot",
            "direct matter/source slot",
            "If S_matter or source normalization has a direct Z/source-weight argument, then partial_Z S_matter or source-weight leakage survives.",
            "FAILS_EXACT_LOCAL_GR_SILENCE",
            "This is the WEP/Newton/source-coupling loophole already identified in 1885/1937.",
            "no-source-only-slot theorem not parent-derived",
        ),
    ]
    rows = []
    for row_id, case, statement, status, implication, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "case": case,
                "statement": statement,
                "status": status,
                "implication": implication,
                "blocker": blocker,
            }
        )
        rows.append(row)
    return rows


def finite_bound_rows() -> list[dict[str, object]]:
    data = [
        ("VZB2027_0_jBZ_norm", "j_BZ", "||J_B^Z||/||E_matter|| on the local branch", "dimensionless source ratio", "PPN/Newton/R10", "MISSING_PARENT_ACTION_VALUE"),
        ("VZB2027_1_cZB_slope", "c_ZB", "||C_ZB|| times local Z amplitude divided by visible source norm", "dimensionless first-order leak", "PPN/WEP/R10", "MISSING_MIXED_HESSIAN"),
        ("VZB2027_2_rho_Z_vac", "rho_Z0", "|V(Z_0)| or local Z vacuum stress density", "energy density", "cosmological/local Newton", "MISSING_VACUUM_REFERENCE"),
        ("VZB2027_3_grad_Z_energy", "rho_grad_Z", "K(Z_0)||nabla Z_0||^2/2", "energy density", "orbital/PPN", "MISSING_LOCAL_PROFILE"),
        ("VZB2027_4_direct_readout", "r_Z_readout", "||partial_Z readout|| or direct source-weight derivative", "readout/source units", "WEP/clocks/R10", "MISSING_READOUT_DESCENT"),
        ("VZB2027_5_boundary_charge", "q_Z_boundary", "||Q_Z||+||K_boundary|| projected to local source channel", "source/boundary units", "R10/orbital", "MISSING_BOUNDARY_CHARGE_ZERO"),
        ("VZB2027_6_tau_projector", "tau_Z", "||Dq(L_tau Phi)-L_tau_red q(Phi)|| for v_Z", "time/projector units", "clocks/PPN", "MISSING_TAU_LOCK"),
        ("VZB2027_7_second_order_width", "sigma_Z2", "upper bound on second-order Z stress after double-zero", "dimensionless or arena-specific", "PPN/R10/clocks", "MISSING_MASS_GAP_AND_AMPLITUDE"),
    ]
    rows = []
    for row_id, symbol, definition, units, arena, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "arena_link": arena,
                "source_path": "MISSING_PARENT_OR_DATA_SOURCE",
                "status": status,
                "claim_status": "RETAINED_NONCLAIM_BOUND_ROW",
            }
        )
        rows.append(row)
    return rows


def arena_projection_rows() -> list[dict[str, object]]:
    data = [
        ("ARENA2027_0_Newton", "Newton/source normalization", "j_BZ, rho_Z0, source-weight slot", "must not be absorbed into fitted G_N without a parent denominator"),
        ("ARENA2027_1_PPN", "PPN gamma/beta/preferred-frame", "c_ZB, rho_grad_Z, second-order width", "requires weak-field projection, not a label-only pass"),
        ("ARENA2027_2_R10", "short-range fifth force", "j_BZ, c_ZB, boundary charge, direct source slot", "requires source/test charge and lambda mapping"),
        ("ARENA2027_3_WEP", "composition dependence", "direct readout/source-weight and nonmetric coefficient ledger", "requires species/material contrast rows"),
        ("ARENA2027_4_clocks", "clock/time readout", "tau_Z and direct theta/readout leakage", "requires tau projector and constants owner"),
        ("ARENA2027_5_orbital", "solar-system/orbital dynamics", "rho_Z0, rho_grad_Z, boundary charge", "requires local profile and boundary/source projection"),
    ]
    rows = []
    for row_id, arena, inputs, guardrail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "arena": arena,
                "required_inputs": inputs,
                "guardrail": guardrail,
                "status": "MISSING_ARENA_PROJECTION",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2027_0_parent_action", "one parent action owns B/Z/matter/boundary/tau sectors", "CZD2027_0;PCS1009_9", "FAIL_UNSIGNED", False),
        ("GATE2027_1_CZB_operator", "C_ZB/J_B^Z computed or theorem-zero", "CZD2027_1..2", "FAIL_MISSING_VALUE_OR_ZERO", False),
        ("GATE2027_2_Dq_not_enough_guard", "Dq[v_Z]=0 alone is used as local-GR proof", "CZD2027_3", "REFUSED", False),
        ("GATE2027_3_exact_escape", "topological/constraint/double-zero Z silence is parent-signed", "NGZ2027_1..3", "FAIL_UNSIGNED", False),
        ("GATE2027_4_finite_bounds", "finite v_Z coupling bounds are score-ready", "VZB2027_*;ARENA2027_*", "FAIL_MISSING_VALUES", False),
        ("GATE2027_5_source_slot", "direct matter/source slot is absent", "NGZ2027_5;1937", "FAIL_NOT_DERIVED", False),
        ("GATE2027_6_local_GR_claim", "local GR/Newton/PPN/R10 pass can be claimed", "GATE2027_0..5", "FAIL_BLOCKED", False),
    ]
    rows = []
    for gate_id, claim, required_rows, status, allowed in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "claim": claim,
                "required_rows": required_rows,
                "status": status,
                "claim_allowed": allowed,
                "reason": "C_ZB/J_B^Z or a finite source-bound vector is not parent-signed",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2027_0_forward_leap", "We found the actual dynamical bottleneck: quotient invisibility is kinematic; local GR needs zero visible Z stress/cross-coupling.", "future work should attack C_ZB/J_B^Z, not repeat Dq-only gates"),
        ("DEC2027_1_no_go", "A conventional bulk Z field generically gravitates through its stress tensor.", "MTS must make Z topological/constraint, local-vacuum-double-zero, or explicitly bounded"),
        ("DEC2027_2_best_derivation_route", "The least-scrutiny exact route is local vacuum double-zero plus no direct source slot: V(Z0)=V'(Z0)=0, nabla Z0=0, Q_Z=0, partial_Z readout=0, m_Z^2>0.", "this is derivable enough to try next and does not pretend the field has no energy"),
        ("DEC2027_3_fallback_route", "If the double-zero cannot be derived, keep the theory alive by sourcing finite J_B^Z/C_ZB/local-profile rows and comparing them to PPN/R10/WEP/clocks.", "bounded residual route remains honest but is not a local-GR derivation"),
    ]
    rows = []
    for decision_id, decision, consequence in data:
        row = base_row()
        row.update({"decision_id": decision_id, "decision": decision, "consequence": consequence})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2027_0_2028",
            "target_doc": "2028-Y5-R2FR-vZ-local-vacuum-double-zero-or-finite-jZB-bound.md",
            "objective": "derive V(Z0)=0, V'(Z0)=0, nabla Z0=0, m_Z^2>0, Q_Z=0, and no direct matter/readout Z slot; if not, source finite J_B^Z/C_ZB bound rows",
            "required_inputs": "candidate S_Z; local branch Z0; potential/reference convention; mass gap; boundary charge; matter/readout descent; local profile amplitude; arena projection",
            "exclusions": "claiming local GR from Dq-zero alone; hiding vacuum energy in fitted constants; using matter equations to kill stress; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(
    theorem_rows: list[dict[str, object]],
    no_go_rows_: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2027_0_source_weight", SOURCE_WEIGHT_DOCS / "AFRAME_VZ_CROSS_COUPLING_2027_NONCLAIM.csv", theorem_rows),
        ("COPY2027_1_wep_lock", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2027_VZ_COUPLING_STATUS_NONCLAIM.csv", no_go_rows_),
        ("COPY2027_2_acquisition_queue", QUEUE / "JR2027_VZ_CZB_JBZ_BOUND_QUEUE.csv", bound_rows),
    ]
    rows = []
    for copy_id, path, payload in copies:
        write_csv(path, payload)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "status": "WRITTEN_NONCLAIM_COPY" if path.exists() and csv_rows_parse(path) else "COPY_WRITE_FAIL",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    no_go_rows_: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2027_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2027_01_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2027_02_CZB_defined", any(row["row_id"] == "CZD2027_2_mixed_operator" and "delta^2 S_Z" in str(row["statement"]) for row in theorem_rows), "C_ZB mixed operator is explicitly defined"))
    checks.append(("VAL2027_03_Dq_no_shortcut", any(row["row_id"] == "CZD2027_3_Dq_zero_insufficient" and row["status"] == "NO_SHORTCUT_THEOREM" for row in theorem_rows), "Dq-zero alone is refused as local-GR proof"))
    checks.append(("VAL2027_04_bulk_Z_no_go", any(row["row_id"] == "NGZ2027_0_canonical_bulk_Z" and row["status"] == "GENERICALLY_VISIBLE" for row in no_go_rows_), "canonical bulk Z stress no-go is recorded"))
    checks.append(("VAL2027_05_double_zero_escape", any(row["row_id"] == "NGZ2027_1_vacuum_double_zero" and "V'(Z_0)=0" in str(row["statement"]) for row in no_go_rows_), "local vacuum double-zero escape route is explicit"))
    checks.append(("VAL2027_06_bounds_nonclaim", all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in bound_rows), "finite bound rows remain nonclaim and missing sourced values"))
    checks.append(("VAL2027_07_arena_projection_blocked", all(row["status"] == "MISSING_ARENA_PROJECTION" for row in arena_rows), "arena projections remain blocked until inputs exist"))
    checks.append(("VAL2027_08_claims_blocked", all(row["claim_allowed"] is False for row in gate_rows), "all local claims remain blocked"))
    checks.append(("VAL2027_09_next_selected", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2027_0_2028", "next target is selected"))
    checks.append(("VAL2027_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2027_11_no_formalization_2027_artifacts", not formalization_has_2027_artifacts(), "no 2027 vZ/coupling artifacts were written under formalization-workbench"))
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2027_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2027 v_Z cross-coupling gate is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    no_go_rows_: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2027 Y5 R2FR vZ Cross-Coupling Operator Or First Numeric Leak Bound",
        "",
        "## Current Verdict",
        "This checkpoint makes the leap that matters. `Dq[v_Z]=0` is only kinematic silence. A normal local `Z` sector still gravitates through its stress tensor unless the parent action makes it topological/constraint-only, local-vacuum-double-zero, or numerically tiny. The new front-door object is `C_ZB := delta^2 S_Z/(delta B_obs delta Z)` together with `J_B^Z := delta S_Z/delta B_obs`. No local-GR/Newton/PPN/R10 claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## Cross-Coupling Theorem Gate",
        md_table(theorem_rows, ["row_id", "object", "statement", "status", "implication", "blocker", "valid_for_claim"]),
        "## Bulk Z No-Go / Escape Audit",
        md_table(no_go_rows_, ["row_id", "case", "statement", "status", "implication", "blocker", "valid_for_claim"]),
        "## Finite vZ Coupling Bound Interface",
        md_table(bound_rows, ["row_id", "symbol", "definition", "units", "arena_link", "source_path", "status", "claim_status", "valid_for_claim"]),
        "## Arena Projection Contract",
        md_table(arena_rows, ["row_id", "arena", "required_inputs", "guardrail", "status", "valid_for_claim"]),
        "## Claim Gate",
        md_table(gate_rows, ["gate_id", "claim", "required_rows", "status", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["decision_id", "decision", "consequence", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows, ["next_id", "target_doc", "objective", "required_inputs", "exclusions", "valid_for_claim"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = coupling_theorem_rows()
    no_go_rows_ = no_go_rows()
    bound_rows = finite_bound_rows()
    arena_rows = arena_projection_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2027_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2027_VZ_CROSS_COUPLING_THEOREM_GATE.csv",
        "nog事": OUT / "P8_Y5_PARENT_QLOC_2027_BULK_Z_NOGO_ESCAPE_AUDIT.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2027_VZ_COUPLING_BOUND_INTERFACE.csv",
        "arena": OUT / "P8_Y5_PARENT_QLOC_2027_ARENA_PROJECTION_CONTRACT.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2027_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2027_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2027_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2027_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2027_VALIDATION.csv",
    }
    write_csv(paths["source"], source_rows)
    write_csv(paths["theorem"], theorem_rows)
    write_csv(paths["nog事"], no_go_rows_)
    write_csv(paths["bounds"], bound_rows)
    write_csv(paths["arena"], arena_rows)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(theorem_rows, no_go_rows_, bound_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        theorem_rows,
        no_go_rows_,
        bound_rows,
        arena_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        theorem_rows,
        no_go_rows_,
        bound_rows,
        arena_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        theorem_rows,
        no_go_rows_,
        bound_rows,
        arena_rows,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
