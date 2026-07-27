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


DOC = ROOT / "2028-Y5-R2FR-vZ-local-vacuum-double-zero-or-finite-jZB-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2028_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2028*vZ*")) or any(FORMALIZATION.rglob("*2028*double*zero*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2028_00_2027_handoff",
            ROOT / "2027-Y5-R2FR-vZ-cross-coupling-operator-or-first-numeric-leak-bound.md",
            ["NEXT2027_0_2028", "NGZ2027_1_vacuum_double_zero", "VAL2027_OVERALL"],
            "2027 handoff selects local vacuum double-zero or finite J_B^Z/C_ZB rows.",
        ),
        (
            "SRC2028_01_2027_nogo_csv",
            OUT / "P8_Y5_PARENT_QLOC_2027_BULK_Z_NOGO_ESCAPE_AUDIT.csv",
            ["NGZ2027_0_canonical_bulk_Z", "NGZ2027_1_vacuum_double_zero"],
            "machine-readable no-go/escape audit.",
        ),
        (
            "SRC2028_02_1473_double_zero",
            ROOT / "1473-Y5-R10-RAB-parent-coupling-double-zero-theorem-or-executable-residual-vector.md",
            ["DZ1473_0_taylor_lemma", "DZ1473_2_positive_gap_supports_not_replaces", "VAL1473_19_overall"],
            "earlier Taylor double-zero theorem and positive-gap distinction.",
        ),
        (
            "SRC2028_03_1666_unobservable",
            ROOT / "1666-Y5-R2FR-coupling-vertical-generator-parent-object-language-or-residual-bound-handoff.md",
            ["THM1666_0_statement", "RBH1666_5_coupling_slope", "CG1666_3_matter_source_coupling_zero"],
            "conditional local unobservability and coupling-slope handoff.",
        ),
        (
            "SRC2028_04_1792_evenness",
            ROOT / "1792-Y5-R2FR-source-functional-evenness-and-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            ["EVT1792_1_exchange_evenness_condition", "ACQ1792_0_bulk_JZ", "CG1792_0_no_linear_source"],
            "source-functional evenness and J_Z/B_Z acquisition ledger.",
        ),
        (
            "SRC2028_05_1861_evenness_refresh",
            ROOT / "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            ["SFE1861_1_exchange_evenness_condition", "JBC1861_0_bulk_JZ", "QI1861_0_formal_double_zero"],
            "refreshed evenness/current obstruction and finite profile fallback.",
        ),
        (
            "SRC2028_06_1747_gap",
            ROOT / "1747-Y5-R2FR-canonical-gap-coupling-source-silence-or-wall-bound-row.md",
            ["CPG1747_1_gap", "GAS1747_0_mu_m2", "VAL1747_OVERALL"],
            "canonical gap/amplitude rows remain missing but define the required mass-gap input.",
        ),
        (
            "SRC2028_07_1885_source_beta",
            ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
            ["B2G1885_5_eigenvalue_route", "CG1885_2_source_coupling_zero", "VAL1885_OVERALL"],
            "beta/source coupling and Hessian/eigenvalue route remain nonclaim.",
        ),
        (
            "SRC2028_08_1937_hilbert",
            ROOT / "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
            ["HST1937_0_variational_source_owner", "CG1937_2_parent_derivation", "VAL1937_OVERALL"],
            "Hilbert source action candidate and parent-derivation blocker.",
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


def theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "VDZ2028_0_canonical_shift",
            "canonical local Z normal form",
            "Let Z=Z0+zeta and S_Z=int sqrt(-g)[-1/2 K0 g^{mu nu} partial_mu zeta partial_nu zeta - V(Z0+zeta)] plus higher terms.",
            "PROTOTYPE_THEOREM_SETUP",
            "This is the minimal model needed to test whether Z can be locally silent without pretending it has no stress.",
            "K0,V,Z0 not parent-sourced",
        ),
        (
            "VDZ2028_1_stationary_branch",
            "stationary branch",
            "V'(Z0)=0 and partial_mu Z0=0 make the Z Euler equation stationary on the local background.",
            "EXACT_CONDITIONAL_CLAUSE",
            "Stationarity removes the linear potential force.",
            "stationarity point not derived",
        ),
        (
            "VDZ2028_2_zero_vacuum_source",
            "zero background stress",
            "V(Z0)=0, partial_mu Z0=0, and zero boundary energy imply T_Z[B,Z0]=0, hence J_B^Z|0=0 for the canonical bulk sector.",
            "EXACT_CONDITIONAL_CLAUSE",
            "This is the missing extra condition beyond mere stationarity.",
            "vacuum subtraction/reference owner missing",
        ),
        (
            "VDZ2028_3_cross_slope_zero",
            "first derivative of visible source",
            "delta T_Z/delta zeta|0 has only terms proportional to V'(Z0) or background gradients; with V'(Z0)=0 and partial Z0=0, C_ZB=0 for the canonical bulk sector.",
            "EXACT_CONDITIONAL_CLAUSE",
            "This proves the first-order double-zero for the visible Z stress.",
            "direct readout/source/boundary terms remain outside the canonical bulk proof",
        ),
        (
            "VDZ2028_4_no_direct_source_slot",
            "matter/readout/source silence",
            "partial_Z S_matter|0=0, partial_Z source_norm|0=0, partial_Z readout|0=0, and partial_Z theta|0=0 are required so the bulk double-zero is not bypassed.",
            "REQUIRED_SIDE_CLAUSE",
            "This protects WEP/Newton/clocks from a hidden source-only slot.",
            "not parent-derived in current corpus",
        ),
        (
            "VDZ2028_5_gap_and_quadratic_bound",
            "positive mass gap and residual order",
            "If m_Z^2:=V''(Z0)/K0>0 and K0>0, then remaining canonical bulk stress begins at O((partial zeta)^2 + m_Z^2 zeta^2), with range ell_Z=1/m_Z in units c=hbar=1.",
            "EXACT_CONDITIONAL_BOUND_FORM",
            "A real positive gap converts failed exact silence into a bounded second-order residual.",
            "m_Z^2, K0, amplitude and profile are missing",
        ),
        (
            "VDZ2028_6_boundary_zero",
            "boundary/no-flux clause",
            "Q_Z=0/proper/exact and no linked boundary flux are required; otherwise boundary B_Z can source the local branch even when bulk double-zero holds.",
            "REQUIRED_SIDE_CLAUSE",
            "This prevents edge terms from carrying the fifth-force/source residual.",
            "boundary theorem or value missing",
        ),
        (
            "VDZ2028_7_verdict",
            "local vacuum double-zero verdict",
            "The theorem works for a canonical prototype: V(Z0)=V'(Z0)=0, partial Z0=0, K0>0, m_Z^2>0, no direct source/readout slot and Q_Z=0 imply J_B^Z=C_ZB=0 at first order. Current MTS has not sourced those clauses, so this remains nonclaim.",
            "THEOREM_PROVED_CONDITIONAL_NOT_ACTIVATED",
            "This is the best exact local-GR route found so far for a non-topological Z sector.",
            "parent S_Z/local branch/source/boundary inputs missing",
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


def obligation_rows() -> list[dict[str, object]]:
    data = [
        ("OBL2028_0_SZ_source", "S_Z source", "explicit parent sector S_Z with field variables and variation convention", "MISSING_PARENT_SOURCE"),
        ("OBL2028_1_K0", "K0", "positive local kinetic coefficient K0>0", "MISSING_VALUE_OR_THEOREM"),
        ("OBL2028_2_Z0", "Z0", "local branch point and proof partial_mu Z0=0", "MISSING_LOCAL_BRANCH"),
        ("OBL2028_3_V0", "V(Z0)", "zero vacuum/source level after non-circular reference fixing", "MISSING_VACUUM_REFERENCE"),
        ("OBL2028_4_Vprime0", "V'(Z0)", "stationary branch condition", "MISSING_STATIONARITY_PROOF"),
        ("OBL2028_5_mZ2", "m_Z^2", "positive Hessian/gap V''(Z0)/K0", "MISSING_MASS_GAP"),
        ("OBL2028_6_source_slot", "direct source slot", "partial_Z S_matter/source/readout/theta all zero", "MISSING_NO_SOURCE_SLOT_PROOF"),
        ("OBL2028_7_boundary", "Q_Z/B_Z", "zero/proper/exact boundary charge and no linked flux", "MISSING_BOUNDARY_ZERO"),
        ("OBL2028_8_profile", "A_Z and ell_Z", "local amplitude/profile bound for second-order residual", "MISSING_PROFILE_AMPLITUDE"),
        ("OBL2028_9_arena_projection", "arena projection", "map residual stress/source rows to PPN/R10/WEP/clocks/orbital thresholds", "MISSING_ARENA_PROJECTION"),
    ]
    rows = []
    for row_id, symbol, requirement, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "requirement": requirement,
                "status": status,
                "source_path": "MISSING_PARENT_OR_DATA_SOURCE",
                "claim_status": "NONCLAIM_OBLIGATION",
            }
        )
        rows.append(row)
    return rows


def finite_bound_rows() -> list[dict[str, object]]:
    data = [
        ("VZF2028_0_jBZ_zero", "J_B^Z|0", "0 if V(Z0)=0, grad Z0=0 and boundary zero", "source ratio", "MISSING_ZERO_OR_VALUE"),
        ("VZF2028_1_cZB_zero", "C_ZB|0", "0 if V'(Z0)=0, grad Z0=0 and no direct source/readout slot", "first-order source slope", "MISSING_ZERO_OR_VALUE"),
        ("VZF2028_2_second_order_bulk", "epsilon_Z2_bulk", "C2[(grad zeta)^2 + m_Z^2 zeta^2]", "arena-normalized source", "MISSING_C2_PROFILE"),
        ("VZF2028_3_tail_profile", "zeta_tail", "A_Z exp(-d/ell_Z) with ell_Z=1/m_Z", "field amplitude", "MISSING_AZ_MZ_DISTANCE"),
        ("VZF2028_4_boundary_flux", "B_Z", "linked boundary/collar flux after integrations by parts", "boundary source", "MISSING_BOUNDARY_VALUE"),
        ("VZF2028_5_direct_slot", "S_Z_direct", "linear direct matter/source/readout coefficient", "source/readout units", "MISSING_NO_SOURCE_SLOT_VALUE"),
        ("VZF2028_6_total_local_residual", "epsilon_Z_total", "sum of bulk second-order, boundary, direct slot and tau/readout residuals", "arena-normalized total", "MISSING_ARENA_PROJECTION"),
    ]
    rows = []
    for row_id, symbol, formula, units, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "source_path": "MISSING_PARENT_OR_DATA_SOURCE",
                "status": status,
                "claim_status": "RETAINED_NONCLAIM_FINITE_BOUND",
            }
        )
        rows.append(row)
    return rows


def failure_rows() -> list[dict[str, object]]:
    data = [
        ("FAIL2028_0_stationary_not_zero", "V'(Z0)=0 but V(Z0)!=0", "leaves vacuum stress/source; local GR not exact"),
        ("FAIL2028_1_massless_flat", "m_Z^2=0", "no finite range; second-order residual may become long-range"),
        ("FAIL2028_2_negative_kinetic", "K0<=0", "ghost/instability; cannot use positive gap bound"),
        ("FAIL2028_3_direct_matter_linear", "partial_Z S_matter|0 != 0", "WEP/source/readout leak survives the bulk double-zero"),
        ("FAIL2028_4_boundary_flux", "Q_Z or B_Z nonzero", "edge source bypasses the local vacuum proof"),
        ("FAIL2028_5_profile_amplitude_unknown", "A_Z unknown", "quadratic residual cannot be bounded or compared"),
    ]
    rows = []
    for row_id, condition, consequence in data:
        row = base_row()
        row.update({"row_id": row_id, "condition": condition, "consequence": consequence, "status": "ACTIVE_FAILURE_MODE"})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2028_0_theorem_written", "canonical local vacuum double-zero theorem is written", "VDZ2028_0..7", "PASS_CONDITIONAL_NONCLAIM", False),
        ("GATE2028_1_parent_SZ", "parent S_Z/K/V/Z0 branch is sourced", "OBL2028_0..5", "FAIL_MISSING_PARENT_SOURCE", False),
        ("GATE2028_2_no_source_slot", "direct matter/readout/source Z slot is zero", "OBL2028_6", "FAIL_MISSING_NO_SOURCE_SLOT_PROOF", False),
        ("GATE2028_3_boundary_zero", "Q_Z/B_Z boundary channel is zero/proper/exact", "OBL2028_7", "FAIL_MISSING_BOUNDARY_ZERO", False),
        ("GATE2028_4_second_order_bound", "residual second-order profile is bounded", "VZF2028_2..6", "FAIL_MISSING_PROFILE_AND_PROJECTION", False),
        ("GATE2028_5_local_GR_claim", "local GR/Newton/PPN/R10 pass can be claimed", "GATE2028_1..4", "FAIL_BLOCKED", False),
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
                "reason": "double-zero theorem is conditional and missing parent/source/profile inputs",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2028_0_result", "The local vacuum double-zero theorem closes mathematically for a canonical prototype.", "this is the strongest non-topological local-GR route so far, but it is not parent-signed"),
        ("DEC2028_1_key_upgrade", "Stationarity is upgraded to stationarity plus zero vacuum source plus zero first derivative of visible stress.", "prevents false passes from V'(Z0)=0 alone"),
        ("DEC2028_2_live_blocker", "The missing input is now concrete: S_Z normal form, Z0, K0, V0, Vprime0, m_Z2, no-source slot, Q_Z, and A_Z.", "next work should source those rows rather than invent new gates"),
        ("DEC2028_3_fallback", "If S_Z cannot be sourced, emit finite J_B^Z/C_ZB/profile rows and compare to local arenas as bounded residuals.", "keeps MTS testable without claiming derived local GR"),
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
            "next_id": "NEXT2028_0_2029",
            "target_doc": "2029-Y5-R2FR-source-SZ-normal-form-and-local-profile-pack.md",
            "objective": "extract or construct the parent S_Z normal form and local branch data K0,V(Z0),V'(Z0),m_Z^2,A_Z,Q_Z,no-source-slot; otherwise stage finite J_B^Z/C_ZB/profile rows",
            "required_inputs": "source path for S_Z; local reference convention; Z0; kinetic sign; potential derivatives; boundary charge; matter/readout descent; profile amplitude; arena projection",
            "exclusions": "local-GR claim; stationarity-only proof; hiding V(Z0) in fitted constants; boundary/readout silence by assertion; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(
    theorem_rows_: list[dict[str, object]],
    obligation_rows_: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2028_0_source_weight", SOURCE_WEIGHT_DOCS / "AFRAME_VZ_LOCAL_VACUUM_DOUBLE_ZERO_2028_NONCLAIM.csv", theorem_rows_),
        ("COPY2028_1_wep_lock", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2028_VZ_DOUBLE_ZERO_STATUS_NONCLAIM.csv", obligation_rows_),
        ("COPY2028_2_acquisition_queue", QUEUE / "JR2028_VZ_SZ_PROFILE_BOUND_QUEUE.csv", bound_rows),
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
    theorem_rows_: list[dict[str, object]],
    obligation_rows_: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    failure_rows_: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2028_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2028_01_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2028_02_theorem_verdict", any(row["row_id"] == "VDZ2028_7_verdict" and row["status"] == "THEOREM_PROVED_CONDITIONAL_NOT_ACTIVATED" for row in theorem_rows_), "conditional double-zero theorem verdict is present"))
    checks.append(("VAL2028_03_stationarity_not_enough", any(row["row_id"] == "FAIL2028_0_stationary_not_zero" for row in failure_rows_), "stationarity-only failure is explicit"))
    checks.append(("VAL2028_04_gap_clause", any(row["row_id"] == "VDZ2028_5_gap_and_quadratic_bound" and "m_Z^2" in str(row["statement"]) for row in theorem_rows_), "positive gap/quadratic residual clause is explicit"))
    checks.append(("VAL2028_05_obligations_nonclaim", all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in obligation_rows_), "proof obligations remain nonclaim and missing"))
    checks.append(("VAL2028_06_bounds_nonclaim", all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in bound_rows), "finite bound rows remain nonclaim and missing"))
    checks.append(("VAL2028_07_claims_blocked", all(row["claim_allowed"] is False for row in gate_rows), "all local claims remain blocked"))
    checks.append(("VAL2028_08_next_selected", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2028_0_2029", "next target is selected"))
    checks.append(("VAL2028_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2028_10_no_formalization_2028_artifacts", not formalization_has_2028_artifacts(), "no 2028 vZ/double-zero artifacts were written under formalization-workbench"))
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2028_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2028 v_Z local vacuum double-zero checkpoint is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows_: list[dict[str, object]],
    obligation_rows_: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    failure_rows_: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2028 Y5 R2FR vZ Local Vacuum Double-Zero Or Finite J_BZ Bound",
        "",
        "## Current Verdict",
        "The local vacuum double-zero route now has an actual proof skeleton. For a canonical local `Z` sector, `V(Z0)=0`, `V'(Z0)=0`, `partial_mu Z0=0`, `K0>0`, `m_Z^2>0`, no direct matter/readout/source slot, and zero/proper boundary charge imply `J_B^Z=0` and `C_ZB=0` at first order. That is genuinely promising, but current MTS has not sourced `S_Z`, `Z0`, the potential derivatives, the mass gap, the boundary condition, or the no-source-slot theorem, so no local-GR/Newton/PPN/R10 claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## Local Vacuum Double-Zero Theorem",
        md_table(theorem_rows_, ["row_id", "object", "statement", "status", "implication", "blocker", "valid_for_claim"]),
        "## Proof Obligations",
        md_table(obligation_rows_, ["row_id", "symbol", "requirement", "status", "source_path", "claim_status", "valid_for_claim"]),
        "## Finite J_BZ/C_ZB Bound Rows",
        md_table(bound_rows, ["row_id", "symbol", "formula", "units", "source_path", "status", "claim_status", "valid_for_claim"]),
        "## Failure Modes",
        md_table(failure_rows_, ["row_id", "condition", "consequence", "status", "valid_for_claim"]),
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
    theorem_rows_ = theorem_rows()
    obligation_rows_ = obligation_rows()
    bound_rows = finite_bound_rows()
    failure_rows_ = failure_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2028_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2028_VZ_LOCAL_VACUUM_DOUBLE_ZERO_THEOREM.csv",
        "obligation": OUT / "P8_Y5_PARENT_QLOC_2028_PROOF_OBLIGATIONS.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2028_FINITE_JBZ_CZB_BOUND_ROWS.csv",
        "failure": OUT / "P8_Y5_PARENT_QLOC_2028_FAILURE_MODES.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2028_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2028_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2028_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2028_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2028_VALIDATION.csv",
    }
    write_csv(paths["source"], source_rows)
    write_csv(paths["theorem"], theorem_rows_)
    write_csv(paths["obligation"], obligation_rows_)
    write_csv(paths["bounds"], bound_rows)
    write_csv(paths["failure"], failure_rows_)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(theorem_rows_, obligation_rows_, bound_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        theorem_rows_,
        obligation_rows_,
        bound_rows,
        failure_rows_,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        theorem_rows_,
        obligation_rows_,
        bound_rows,
        failure_rows_,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        theorem_rows_,
        obligation_rows_,
        bound_rows,
        failure_rows_,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
