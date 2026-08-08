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


DOC = ROOT / "2026-Y5-R2FR-parent-q-Dq-matrix-field-action-or-first-vZ-DObs-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2026_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2026*vZ*")) or any(FORMALIZATION.rglob("*2026*DObs*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2026_00_2025_handoff",
            ROOT / "2025-Y5-R2FR-Dq-vX-observed-metric-zero-or-finite-DObs-leak-row.md",
            ["NEXT2025_0_2026", "DVO2025_6_verdict", "VAL2025_OVERALL"],
            "2025 handoff selects parent q/Dq/v_Z or first DObs/Dg leak row.",
        ),
        (
            "SRC2026_01_2025_next_csv",
            OUT / "P8_Y5_PARENT_QLOC_2025_NEXT_TARGET.csv",
            ["NEXT2025_0_2026"],
            "machine-readable 2026 target row.",
        ),
        (
            "SRC2026_02_2025_zero_csv",
            OUT / "P8_Y5_PARENT_QLOC_2025_DQ_VX_OBS_METRIC_ZERO_ATTEMPT.csv",
            ["DVO2025_0_chain_rule", "DVO2025_6_verdict"],
            "conditional Dq-to-observed-metric zero theorem.",
        ),
        (
            "SRC2026_03_1737_vertical_doc",
            ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            ["VB1737_0_vZ", "FDQ1737_vZ_e", "DEC1737_1_coframe_zero"],
            "v_Z source rows and retained finite-leak fallbacks.",
        ),
        (
            "SRC2026_04_1737_vertical_csv",
            OUT / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv",
            ["VB1737_0_vZ", "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK"],
            "machine-readable v_Z vertical-basis status.",
        ),
        (
            "SRC2026_05_1737_qmap_csv",
            OUT / "P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv",
            ["QMAP1737_1_e_obs", "QMAP1737_5_Z_phi_RAB"],
            "q-map contract showing observed geometry and Z/phi/RAB auxiliary status.",
        ),
        (
            "SRC2026_06_1784_doc",
            ROOT / "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md",
            ["ODP1784_4_field_action", "DZG1784_0_eobs_metric", "DEC1784_2_fallback"],
            "field-action incompleteness and Dq_Z geometry fallback.",
        ),
        (
            "SRC2026_07_1784_packet_csv",
            OUT / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_VERTICAL_PACKET_GATE.csv",
            ["ODP1784_4_field_action", "ODP1784_7_matter_readout", "ODP1784_8_verdict"],
            "machine-readable parent vertical-action packet status.",
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


def normal_form_rows() -> list[dict[str, object]]:
    data = [
        (
            "VZN2026_0_bundle_split",
            "local parent bundle split",
            "Assume a local chart Phi=(B_obs,Z,U) with B_obs=(e_obs,g_obs,source/readout,theta,tau,boundary projector) and Z a fiber coordinate.",
            "NORMAL_FORM_CONDITIONAL",
            "This is the clean non-circular version of saying Z is representative-only.",
            "not parent-derived from a Lagrangian or quotient construction",
            "derive the split from the parent q map, not by naming it",
        ),
        (
            "VZN2026_1_quotient_projection",
            "quotient map",
            "q(Phi)=B_obs and therefore Dq[(0,delta Z,0)]=0.",
            "EXACT_IF_BUNDLE_SPLIT_SIGNED",
            "This proves Dq[v_Z]=0 without handwaving once the bundle split is signed.",
            "q(Phi)=B_obs is still an ansatz row",
            "write q components field-by-field",
        ),
        (
            "VZN2026_2_vertical_generator",
            "first v_Z direction",
            "v_Z=partial_Z is vertical only if it has no components along B_obs and no hidden readout/marker/boundary action.",
            "EXACT_IF_COMPONENT_LOCK_SIGNED",
            "This prevents a geometry-only Lie derivative from pretending to be the full generator.",
            "v_Z on matter/readout/constants/boundary/tau is unsigned",
            "fill the v_Z field-action row across all parent variables",
        ),
        (
            "VZN2026_3_observed_geometry_zero",
            "observed coframe/metric",
            "If VZN2026_1 and VZN2026_2 hold, then DObs_e[v_Z]=DE_q(Dq[v_Z])=0 and Dg_obs[v_Z]=2 sym_eta(e_obs,DObs_e[v_Z])=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "This is the first real local-geometry zero path.",
            "premises are unsigned",
            "do not claim local GR until action/readout/boundary coupling is also silent",
        ),
        (
            "VZN2026_4_action_coupling_condition",
            "visible-sector Euler coupling",
            "Even if Dq[v_Z]=0, local GR also requires J_B^Z:=delta S_Z/delta B_obs=0 or bounded-small on the local branch.",
            "MISSING_COUPLING_OPERATOR",
            "This exposes the real coupling problem rather than hiding it downstream.",
            "no parent mixed Hessian/cross-source operator is available",
            "derive C_ZB or emit finite coupling/leak rows",
        ),
        (
            "VZN2026_5_verdict",
            "2026 v_Z verdict",
            "The v_Z zero route can be proved as a normal-form lemma, but it is not physically active until q(Phi)=B_obs, v_Z field action, and visible-sector coupling silence are all parent-signed.",
            "ZERO_ROUTE_SHARP_NOT_CLAIMED",
            "We have moved from vague local silence to a precise coupling operator target.",
            "bundle split, q map, v_Z field action, C_ZB, matter/readout descent, and boundary charge are unsigned",
            "2027 should derive or bound C_ZB and the first v_Z leak coefficients",
        ),
    ]
    rows = []
    for row_id, obj, statement, status, claim_effect, blocker, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": obj,
                "statement": statement,
                "status": status,
                "claim_effect": claim_effect,
                "blocker": blocker,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def dq_first_row_rows() -> list[dict[str, object]]:
    data = [
        ("VZDQ2026_0_Qvis", "Dq_Qvis[v_Z]", "partial_Z B_obs", "0 if q(B,Z,U)=B_obs", "UNSIGNED_CONDITIONAL_ZERO", "MISSING_Q_MAP_SOURCE"),
        ("VZDQ2026_1_eobs", "DObs_e[v_Z]", "partial_Z e_obs", "0 if e_obs=E(B_obs)", "UNSIGNED_CONDITIONAL_ZERO", "MISSING_E_FUNCTOR_SOURCE"),
        ("VZDQ2026_2_gobs", "Dg_obs[v_Z]", "2 sym_eta(e_obs,DObs_e[v_Z])", "0 if DObs_e[v_Z]=0", "UNSIGNED_CONDITIONAL_ZERO", "MISSING_E_FUNCTOR_SOURCE"),
        ("VZDQ2026_3_source_readout", "Dsource_readout[v_Z]", "partial_Z source/readout", "0 if readouts factor through B_obs", "MISSING_PARENT_INPUT", "MISSING_READOUT_DESCENT"),
        ("VZDQ2026_4_theta_marker", "Dtheta[v_Z]", "partial_Z theta_A", "0 if constants/material labels are quotient-owned", "MISSING_PARENT_INPUT", "MISSING_THETA_OWNER"),
        ("VZDQ2026_5_tau", "Dtau[v_Z]", "partial_Z tau or Dq(L_tau Phi)-L_tau_red q(Phi)", "0 if tau is q-projectable", "MISSING_PARENT_INPUT", "MISSING_TAU_LOCK"),
        ("VZDQ2026_6_boundary", "Dboundary_projector[v_Z]", "partial_Z boundary/projector data", "0 if boundary/projector is basic or exact-zero", "MISSING_PARENT_INPUT", "MISSING_BOUNDARY_ZERO"),
    ]
    rows = []
    for row_id, component, derivative, zero_condition, status, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "component": component,
                "derivative": derivative,
                "zero_condition": zero_condition,
                "status": status,
                "blocker": blocker,
                "claim_status": "NONCLAIM_FIRST_ROW",
            }
        )
        rows.append(row)
    return rows


def coupling_rows() -> list[dict[str, object]]:
    data = [
        (
            "CZB2026_0_mixed_hessian",
            "C_ZB",
            "C_ZB := delta/delta B_obs (delta S_parent/delta Z) = delta^2 S_parent/(delta B_obs delta Z)",
            "visible-sector source induced by the Z fiber",
            "MISSING_PARENT_LAGRANGIAN",
        ),
        (
            "CZB2026_1_visible_source",
            "J_B^Z",
            "J_B^Z := delta S_Z/delta B_obs evaluated on the local branch",
            "direct obstruction to GR equations for B_obs",
            "MISSING_COUPLING_OPERATOR",
        ),
        (
            "CZB2026_2_matter_readout",
            "partial_Z S_matter",
            "matter/readout/constants must descend as S_matter=Sbar(B_obs,psi,theta) with partial_Z readout=0",
            "prevents WEP/clock/source marker leak",
            "MISSING_MATTER_QUOTIENT",
        ),
        (
            "CZB2026_3_boundary_charge",
            "Q_Z and K_boundary",
            "local boundary charge/cocycle for v_Z must be zero, exact, or projected away with a source-backed projector",
            "prevents edge charge from mimicking local fifth-force source",
            "MISSING_BOUNDARY_CHARGE_ZERO",
        ),
        (
            "CZB2026_4_silence_condition",
            "Z-local-silence system",
            "Dq[v_Z]=0, J_B^Z=0, partial_Z readouts=0, Q_Z=0, and tau projectability together imply the v_Z branch is locally silent.",
            "minimal parent contract for exact local silence",
            "MULTIPLE_UNSIGNED_CLAUSES",
        ),
        (
            "CZB2026_5_verdict",
            "coupling verdict",
            "The coupling is now the front door: without C_ZB/J_B^Z, Dq-zero alone is not enough to claim local GR.",
            "demotes v_Z to theorem-target plus finite-leak queue",
            "COUPLING_NOT_DERIVED",
        ),
    ]
    rows = []
    for row_id, symbol, definition, role, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "role": role,
                "status": status,
                "claim_status": "NONCLAIM_COUPLING_TARGET",
            }
        )
        rows.append(row)
    return rows


def leak_queue_rows() -> list[dict[str, object]]:
    data = [
        ("VZL2026_0_epsilon_Z_geom", "epsilon_Z_geom", "||D_Z e_obs|| + ||D_Z g_obs||", "geometry leak", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("VZL2026_1_j_ZB", "j_ZB", "||J_B^Z|| or ||C_ZB|| on the local branch", "visible equation source leak", "MISSING_PARENT_LAGRANGIAN"),
        ("VZL2026_2_r_Z_readout", "r_Z_readout", "||partial_Z readout||", "matter/source/readout leak", "MISSING_READOUT_DESCENT"),
        ("VZL2026_3_theta_Z", "theta_Z", "||partial_Z theta_A||", "constant/material marker leak", "MISSING_THETA_OWNER"),
        ("VZL2026_4_q_Z_boundary", "q_Z_boundary", "||Q_Z|| + ||K_boundary||", "edge/source leakage", "MISSING_BOUNDARY_CHARGE_ZERO"),
        ("VZL2026_5_tau_Z", "tau_Z", "||Dq(L_tau Phi)-L_tau_red q(Phi)|| on v_Z", "clock/time pushforward leak", "MISSING_TAU_LOCK"),
    ]
    rows = []
    for row_id, symbol, definition, role, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "role": role,
                "units": "MISSING_ARENA_UNITS",
                "source_path": "MISSING_PARENT_SOURCE",
                "status": status,
                "claim_status": "RETAINED_NONCLAIM_VZ_LEAK_ROW",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2026_0_bundle_split", "local bundle split B_obs x F_Z is parent-derived", "VZN2026_0", "FAIL_UNSIGNED", False),
        ("GATE2026_1_q_projection", "q(Phi)=B_obs and Dq[v_Z]=0 are signed", "VZN2026_1;VZDQ2026_0", "FAIL_UNSIGNED", False),
        ("GATE2026_2_field_action", "v_Z has no hidden B/readout/boundary/tau components", "VZN2026_2;VZDQ2026_3..6", "FAIL_UNSIGNED", False),
        ("GATE2026_3_coupling_silence", "C_ZB=0 and J_B^Z=0 are derived", "VZN2026_4;CZB2026_0;CZB2026_1", "FAIL_MISSING_COUPLING_OPERATOR", False),
        ("GATE2026_4_boundary_readout_silence", "readout/theta/tau/boundary are Z-blind", "CZB2026_2;CZB2026_3;VZDQ2026_3..6", "FAIL_UNSIGNED", False),
        ("GATE2026_5_vZ_zero_active", "v_Z local geometry zero is active", "GATE2026_0..4", "FAIL_CONDITIONAL_ONLY", False),
        ("GATE2026_6_local_GR_claim", "local GR/PPN/R10 pass can be claimed from v_Z", "GATE2026_5 or sourced VZL rows", "FAIL_BLOCKED", False),
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
                "reason": "normal-form theorem is useful but parent coupling/source rows are not signed",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2026_0_leap", "The next leap is not another downstream test; it is the parent cross-coupling operator C_ZB.", "derive or bound C_ZB before claiming v_Z local silence"),
        ("DEC2026_1_derivation_result", "Dq[v_Z]=0 is provable in a quotient normal form q(B,Z,U)=B, but that normal form must be parent-derived.", "keep it as a theorem target, not a fact"),
        ("DEC2026_2_coupling_warning", "Dq-zero alone does not stop Z from sourcing the observed equations through delta S_Z/delta B_obs.", "local GR needs action descent/coupling silence too"),
        ("DEC2026_3_best_next", "Build the C_ZB/J_B^Z row from the candidate parent Lagrangian, or admit the v_Z branch as a finite bounded residual.", "2027 should be coupling-first"),
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
            "next_id": "NEXT2026_0_2027",
            "target_doc": "2027-Y5-R2FR-vZ-cross-coupling-operator-or-first-numeric-leak-bound.md",
            "objective": "derive C_ZB/J_B^Z from a parent action, or create the first source-ready finite v_Z leak bound row for geometry/readout/boundary/tau",
            "required_inputs": "candidate parent Lagrangian; B_obs/Z split; mixed Hessian convention; matter/readout descent; boundary charge; tau projector; arena norm",
            "exclusions": "local-GR claim; Dq-zero without action descent; projection by declaration; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(
    normal_rows: list[dict[str, object]],
    dq_rows: list[dict[str, object]],
    coupling_rows_: list[dict[str, object]],
    leak_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2026_0_source_weight", SOURCE_WEIGHT_DOCS / "AFRAME_VZ_NORMAL_FORM_2026_NONCLAIM.csv", normal_rows),
        ("COPY2026_1_wep_lock", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2026_VZ_STATUS_NONCLAIM.csv", dq_rows),
        ("COPY2026_2_acquisition_queue", QUEUE / "JR2026_VZ_COUPLING_AND_DOBS_QUEUE.csv", coupling_rows_ + leak_rows),
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
    normal_rows: list[dict[str, object]],
    dq_rows: list[dict[str, object]],
    coupling_rows_: list[dict[str, object]],
    leak_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2026_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2026_01_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2026_02_normal_form_present", any(row["row_id"] == "VZN2026_1_quotient_projection" and "Dq[(0,delta Z,0)]=0" in str(row["statement"]) for row in normal_rows), "quotient normal-form lemma is explicit"))
    checks.append(("VAL2026_03_metric_zero_conditional", any(row["row_id"] == "VZN2026_3_observed_geometry_zero" and "Dg_obs[v_Z]" in str(row["statement"]) for row in normal_rows), "observed geometry zero theorem is conditional and explicit"))
    checks.append(("VAL2026_04_coupling_operator_present", any(row["row_id"] == "CZB2026_0_mixed_hessian" and "delta^2" in str(row["definition"]) for row in coupling_rows_), "C_ZB mixed Hessian target is present"))
    checks.append(("VAL2026_05_dq_first_row_nonclaim", all(row["valid_for_claim"] is False and row["claim_status"] == "NONCLAIM_FIRST_ROW" for row in dq_rows), "first v_Z Dq rows are nonclaim"))
    checks.append(("VAL2026_06_leak_rows_blocked", all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in leak_rows), "finite v_Z leak rows remain blocked/nonclaim"))
    checks.append(("VAL2026_07_claims_blocked", all(row["claim_allowed"] is False for row in gate_rows), "all local claims remain blocked"))
    checks.append(("VAL2026_08_next_selected", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2026_0_2027", "next target is selected"))
    checks.append(("VAL2026_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2026_10_no_formalization_2026_artifacts", not formalization_has_2026_artifacts(), "no 2026 vZ/DObs artifacts were written under formalization-workbench"))
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2026_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2026 v_Z normal-form/coupling gate is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    normal_rows: list[dict[str, object]],
    dq_rows: list[dict[str, object]],
    coupling_rows_: list[dict[str, object]],
    leak_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2026 Y5 R2FR Parent q/Dq Matrix Field Action Or First vZ DObs Row",
        "",
        "## Current Verdict",
        "This checkpoint takes the leap forward: `Dq[v_Z]=0` can be proved cleanly only in a quotient normal form `Phi=(B_obs,Z,U)` with `q(Phi)=B_obs` and `v_Z=partial_Z`. That gives `DObs_e[v_Z]=0` and `Dg_obs[v_Z]=0` by the 2025 chain theorem, but it still does **not** deliver local GR unless the parent action also has no visible-sector Z coupling. The next missing object is therefore the cross-coupling operator `C_ZB` / source `J_B^Z`, not another downstream robustness test.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## vZ Normal-Form Lemma Attempt",
        md_table(normal_rows, ["row_id", "object", "statement", "status", "claim_effect", "blocker", "next_action", "valid_for_claim"]),
        "## First vZ Dq/DObs Row",
        md_table(dq_rows, ["row_id", "component", "derivative", "zero_condition", "status", "blocker", "claim_status", "valid_for_claim"]),
        "## Coupling Obstruction",
        md_table(coupling_rows_, ["row_id", "symbol", "definition", "role", "status", "claim_status", "valid_for_claim"]),
        "## Finite vZ Leak Queue",
        md_table(leak_rows, ["row_id", "symbol", "definition", "role", "units", "source_path", "status", "claim_status", "valid_for_claim"]),
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
    normal_rows = normal_form_rows()
    dq_rows = dq_first_row_rows()
    coupling_rows_ = coupling_rows()
    leak_rows = leak_queue_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2026_SOURCE_REGISTER.csv",
        "normal": OUT / "P8_Y5_PARENT_QLOC_2026_VZ_NORMAL_FORM_LEMMA.csv",
        "dq": OUT / "P8_Y5_PARENT_QLOC_2026_VZ_DQ_MATRIX_FIRST_ROW.csv",
        "coupling": OUT / "P8_Y5_PARENT_QLOC_2026_VZ_ACTION_COUPLING_OBSTRUCTION.csv",
        "leak": OUT / "P8_Y5_PARENT_QLOC_2026_VZ_FINITE_LEAK_QUEUE.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2026_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2026_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2026_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2026_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2026_VALIDATION.csv",
    }
    write_csv(paths["source"], source_rows)
    write_csv(paths["normal"], normal_rows)
    write_csv(paths["dq"], dq_rows)
    write_csv(paths["coupling"], coupling_rows_)
    write_csv(paths["leak"], leak_rows)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(normal_rows, dq_rows, coupling_rows_, leak_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        normal_rows,
        dq_rows,
        coupling_rows_,
        leak_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        normal_rows,
        dq_rows,
        coupling_rows_,
        leak_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        normal_rows,
        dq_rows,
        coupling_rows_,
        leak_rows,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
