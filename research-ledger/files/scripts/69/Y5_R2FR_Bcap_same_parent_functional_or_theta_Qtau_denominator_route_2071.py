from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
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


DOC = ROOT / "2071-Y5-R2FR-Bcap-same-parent-functional-or-theta-Qtau-denominator-route.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2071_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2071-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2071*",
        "*Y5_R2FR_Bcap_same_parent_functional_or_theta_Qtau_denominator_route_2071*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2071_00_2070_doc",
            ROOT / "2070-Y5-R2FR-PiR-variation-convention-Kcap-source-row-or-MHref-denominator-lock.md",
            ["NEXT2070_0_2071", "same-parent cap functional", "M_H_ref = H_tau[S_link] - H_ref"],
            "2070 handoff: B_cap same-parent route or theta/Q_tau denominator route.",
        ),
        (
            "SRC2071_01_2070_next",
            OUT / "P8_Y5_PARENT_QLOC_2070_NEXT_TARGET.csv",
            ["NEXT2070_0_2071", "B_cap[R_AB,tau,T_H]", "theta_MTS/Q_tau_MTS dependency"],
            "machine-readable 2071 target.",
        ),
        (
            "SRC2071_02_2070_PiR",
            OUT / "P8_Y5_PARENT_QLOC_2070_PIR_VARIATION_CONVENTION.csv",
            ["PVC2070_3_same_parent_Bcap", "Pi_R_time_caps_abs", "K_cap_to_PiR"],
            "Pi_R cap variation convention and same-parent B_cap blocker.",
        ),
        (
            "SRC2071_03_2070_MHref",
            OUT / "P8_Y5_PARENT_QLOC_2070_MHREF_DENOMINATOR_LOCK.csv",
            ["MHL2070_6_theta_Qtau_dependency", "MISSING_PARENT_THETA_QTAU_EXTRACTION", "M_H_ref"],
            "M_H_ref denominator lock remains upstream of theta/Q_tau.",
        ),
        (
            "SRC2071_04_2070_Kcap_template",
            OUT / "P8_Y5_PARENT_QLOC_2070_KCAP_SOURCE_TEMPLATE.csv",
            ["MISSING_PARENT_BCAP_FUNCTIONAL", "MISSING_K_CAP_TO_PIR_VALUE", "SOURCE_ROW_TEMPLATE_ONLY"],
            "K_cap source row template from 2070.",
        ),
        (
            "SRC2071_05_2062_boundary_grammar",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_1_natural_variation", "BGA2062_3_corner_worldtube", "BGA2062_4_orientation"],
            "boundary functional grammar: natural R_AB variation, corner/worldtube debt, orientation debt.",
        ),
        (
            "SRC2071_06_2063_component_intake",
            OUT / "P8_Y5_PARENT_QLOC_2063_FINITE_PIR_COMPONENT_INTAKE.csv",
            ["PCI2063_3_corner_bound", "PCI2063_4_total_join", "PCI2063_5_qR_Cassini_join"],
            "finite Pi_R component intake and q_R guard.",
        ),
        (
            "SRC2071_07_1006_MHref_audit",
            OUT / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv",
            ["MHA1006_1_integrability", "MHA1006_5_anti_circularity", "MHA1006_6_theorem_verdict"],
            "M_H_ref theorem audit: integrability, anti-circularity, no theorem pass.",
        ),
        (
            "SRC2071_08_1007_integrability",
            ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            ["SRS1007_0_integrability_formula", "SFR1007_0_missing_theta_Qtau", "DEC1007_0_integrability_not_claimed"],
            "H_tau integrability and fixed-reference checkpoint.",
        ),
        (
            "SRC2071_09_1008_theta_Qtau_doc",
            ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            ["CDS1008_3_reference_guard", "CDS1008_4_total_promoter", "CG1008_5_MHref"],
            "parent theta/Q_tau extraction and charge decomposition runner.",
        ),
        (
            "SRC2071_10_1008_piece_ledger",
            OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            ["QTA1008_0_L_parent", "QTA1008_8_Q_total", "not_promoted"],
            "machine-readable charge-piece ledger.",
        ),
        (
            "SRC2071_11_1009_parent_contract",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_9_total_parent_contract", "SVC1009_1_GK_missing_action", "CG1009_0_total_parent_action"],
            "parent current-chain/action contract: sector blocks organized but not promoted.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def bcap_candidate_rows() -> list[dict[str, object]]:
    data = [
        (
            "BFC2071_0_required_decomposition",
            "B_cap[R_AB,tau,T_H]",
            "B_cap = B_RAB_cap[R_AB] + B_tau_cap[tau,T_H] + B_mix_cap[R_AB,tau,T_H] + B_ref/source_caps",
            "must generate pi_R^cap by delta/delta R_AB and N_tau_cap by the same cap-current variation",
            "DECOMPOSITION_WRITTEN_SAME_PARENT_UNSIGNED",
            "The split shows the necessary object: a mixed cap term, not two unrelated ledgers.",
        ),
        (
            "BFC2071_1_RAB_only_fails",
            "B_RAB_cap[R_AB]",
            "delta B_RAB_cap/delta R_AB can define pi_R^cap",
            "cannot by itself own N_tau_cap or tau stress-current leakage",
            "FAILS_SAME_PARENT_TEST",
            "A pure R_AB cap term gives the Pi_R side but not the cap-current side.",
        ),
        (
            "BFC2071_2_tau_only_fails",
            "B_tau_cap[tau,T_H]",
            "tau variation can define a cap current or Hamiltonian leakage contribution",
            "cannot by itself generate pi_R^cap=delta B_cap/delta R_AB",
            "FAILS_SAME_PARENT_TEST",
            "A pure tau cap term gives the current side but not the R_AB momentum side.",
        ),
        (
            "BFC2071_3_Bmix_required",
            "B_mix_cap[R_AB,tau,T_H]",
            "one mixed functional must source both pi_R^cap and N_tau_cap in one equation family",
            "requires parent action/source equation, variation variables, cap surface, units and boundary conditions",
            "MISSING_PARENT_BMIX_CAP_FUNCTIONAL",
            "This is the minimum coupling object needed to make K_cap_to_PiR more than a conversion placeholder.",
        ),
        (
            "BFC2071_4_source_reference_split",
            "B_source_caps + B_ref_caps",
            "source cap and reference cap contributions must be separated before absolute summing",
            "prevents fitted reference or cancellation from hiding cap leakage",
            "MISSING_SOURCE_REFERENCE_CAP_CERTIFICATE",
            "A source/reference split is mandatory before finite PPN/R10 scoring.",
        ),
        (
            "BFC2071_5_measure_orientation",
            "C_cap,dSigma_C,n_C",
            "cap surface, orientation and measure must be fixed before units or signs are meaningful",
            "connects Pi_R_time_caps_abs, N_tau_cap and q_R normalization in the same frame",
            "MISSING_CAP_SURFACE_ORIENTATION_MEASURE",
            "2070 wrote the density convention, but the cap geometry is still unsigned.",
        ),
        (
            "BFC2071_6_verdict",
            "same-parent B_cap route",
            "no sourced B_mix_cap functional exists in the current corpus",
            "K_cap_to_PiR remains source-row-only; no theorem-zero or numeric value is promoted",
            "BCAP_ROUTE_BLOCKED_ON_BMIX_PARENT_FUNCTIONAL",
            "The route is sharpened, not closed.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, candidate_formula, same_parent_requirement, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "candidate_formula": candidate_formula,
                "same_parent_requirement": same_parent_requirement,
                "status": status,
                "note": note,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def same_parent_test_rows() -> list[dict[str, object]]:
    data = [
        (
            "SPT2071_0_RAB_variation",
            "delta B_cap/delta R_AB = pi_R^cap",
            "2070 convention supplies the form but not the parent-owned B_cap equation",
            "CONVENTION_ONLY",
            False,
        ),
        (
            "SPT2071_1_tau_current_variation",
            "N_tau_cap is obtained from tau/stress/current variation of the same B_cap",
            "no parent cap current-chain variation is present",
            "MISSING_PARENT_CURRENT_CHAIN",
            False,
        ),
        (
            "SPT2071_2_identity_of_functional",
            "the B_cap named in the Pi_R variation and current leakage is literally the same functional",
            "B_RAB-only and tau-only rows would be two ledgers, not one parent object",
            "MISSING_FUNCTIONAL_IDENTITY_CERTIFICATE",
            False,
        ),
        (
            "SPT2071_3_units_and_norm",
            "K_cap_to_PiR := ||pi_R^cap||_L1(Ccap)/N_tau_cap has declared units and positive denominator",
            "K units, cap norm and N_tau_cap source are placeholders",
            "MISSING_KCAP_UNITS_AND_DENOMINATOR",
            False,
        ),
        (
            "SPT2071_4_theorem_zero_option",
            "K_cap_to_PiR=0 or Pi_R_time_caps=0 follows only if B_mix_cap is absent by parent theorem",
            "absence of B_mix_cap has not been proved; it is merely not found",
            "THEOREM_ZERO_NOT_AVAILABLE",
            False,
        ),
        (
            "SPT2071_5_no_cancellation_guard",
            "source/reference caps and all Pi_R components are absolute-summed before q_R use",
            "absolute join and q_R normalization remain downstream of missing component sources",
            "MISSING_ABSOLUTE_JOIN_AND_QR_GUARD",
            False,
        ),
        (
            "SPT2071_6_verdict",
            "same-parent cap functional test",
            "B_mix_cap is the required coupling object and is currently unsigned",
            "FAIL_CURRENT_CLAIM_BCAP_SAME_PARENT_UNSIGNED",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, evidence, status, test_pass in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "evidence": evidence,
                "status": status,
                "test_pass": test_pass,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def theta_qtau_route_rows() -> list[dict[str, object]]:
    data = [
        (
            "TQR2071_0_parent_action",
            "S_parent",
            "delta S_parent = E_A delta Phi^A + d theta_MTS",
            "parent action and sector certificates",
            "MISSING_TOTAL_PARENT_ACTION_SWITCH",
            "1009 organizes sectors but does not promote total parent action.",
        ),
        (
            "TQR2071_1_theta_MTS",
            "theta_MTS",
            "theta_MTS = theta_EH + theta_boundary + theta_extra + theta_projector + theta_matter/source",
            "sector-by-sector symplectic potential extraction",
            "MISSING_PARENT_THETA_EXTRACTION",
            "1008 marks theta_total not_extracted.",
        ),
        (
            "TQR2071_2_Qtau_MTS",
            "Q_tau^MTS",
            "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent = dQ_tau^MTS + C_tau",
            "tau action on every retained field and boundary/reference sector",
            "MISSING_PARENT_QTAU_EXTRACTION",
            "1008 keeps Q_total not_promoted.",
        ),
        (
            "TQR2071_3_Htau_integrability",
            "H_tau",
            "delta H_tau = integral_S(delta Q_tau - i_tau theta) is integrable with fixed reference",
            "parent theta/Q_tau, boundary conditions and symplectic flux certificate",
            "MISSING_HTAU_INTEGRABILITY",
            "1007 blocks on missing theta/Q_tau and fixed reference.",
        ),
        (
            "TQR2071_4_fixed_reference",
            "H_ref",
            "reference/counterterm is fixed before source, clock, orbit or local readout",
            "fixed-before-readout certificate",
            "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "prevents post-fit counterterm cancellation.",
        ),
        (
            "TQR2071_5_MHref",
            "M_H_ref",
            "M_H_ref = H_tau[S_link] - H_ref > 0 in the same observed frame",
            "positive same-frame denominator and no boundary/extra-sector contamination",
            "MISSING_POSITIVE_MHREF_CERTIFICATE",
            "1006 refuses denominator theorem pass.",
        ),
        (
            "TQR2071_6_qR_guard",
            "q_R normalization",
            "|Pi_R^tot/(N_sphere Z_R_infty r_s)| + tails enters PPN only after absolute component join",
            "N_sphere, Z_R_infty, r_s, tails and no-cancellation guard",
            "MISSING_QR_NORMALIZATION_CHAIN",
            "2063 blocks cap-only scoring.",
        ),
        (
            "TQR2071_7_verdict",
            "theta/Q_tau denominator route",
            "route is structurally correct but still upstream of the parent current-chain/action contract",
            "needs 1009-style sector action closure before H_tau/M_H_ref can score",
            "THETA_QTAU_ROUTE_BLOCKED_ON_PARENT_CURRENT_CHAIN",
            "The denominator branch is not dead, but it is not yet a scoring branch.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, formula, required_input, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "formula": formula,
                "required_input": required_input,
                "status": status,
                "note": note,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def kcap_schema_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "row_id": "KCS2071_0_Bmix_Kcap_source_row",
            "system_id": "R10_local_reference_branch",
            "B_mix_cap_functional": "MISSING_PARENT_BMIX_CAP_FUNCTIONAL",
            "PiR_cap_abs": "Pi_R_time_caps_abs := integral_Ccap |delta B_mix_cap/delta R_AB| dSigma_C",
            "N_tau_cap_abs": "MISSING_N_TAU_CAP_FROM_SAME_BMIX",
            "K_cap_to_PiR_formula": "K_cap_to_PiR := Pi_R_time_caps_abs / N_tau_cap_abs",
            "K_cap_value": "MISSING_K_CAP_TO_PIR_VALUE_OR_THEOREM_ZERO",
            "K_cap_units": "MISSING_K_CAP_UNITS",
            "source_reference_split": "MISSING_SOURCE_REFERENCE_CAP_SEPARATION",
            "cap_surface": "MISSING_C_CAP_SURFACE_ORIENTATION_MEASURE",
            "qR_normalization_source": "MISSING_QR_NORMALIZATION_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "equation_ref": "MISSING_EQUATION_REF",
            "status": "SOURCE_ROW_SCHEMA_ONLY",
            "claim_allowed": False,
        }
    )
    return [row]


def dry_run_rows(
    bcap_rows: list[dict[str, object]],
    same_parent_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    bcap_verdict = next(row for row in bcap_rows if row["row_id"] == "BFC2071_6_verdict")
    same_parent_verdict = next(row for row in same_parent_rows if row["row_id"] == "SPT2071_6_verdict")
    theta_verdict = next(row for row in theta_rows if row["row_id"] == "TQR2071_7_verdict")
    data = [
        (
            "RUN2071_0_Bcap_decomposition",
            "B_cap decomposition",
            "REFUSED_SAME_PARENT_CLAIM",
            str(bcap_verdict["status"]),
            False,
        ),
        (
            "RUN2071_1_same_parent_test",
            "same-parent cap functional test",
            "FAIL_UNSIGNED_BMIX",
            str(same_parent_verdict["status"]),
            False,
        ),
        (
            "RUN2071_2_theta_Qtau_route",
            "theta/Q_tau denominator route",
            "REFUSED_DENOMINATOR_SCORE",
            str(theta_verdict["status"]),
            False,
        ),
        (
            "RUN2071_VERDICT",
            "Bcap or theta/Qtau route",
            "BMIX_CAP_FUNCTIONAL_MISSING_ROUTE_TO_PARENT_CURRENT_CHAIN",
            "2072 should either construct B_mix_cap as a parent functional or reopen the 1009 current-chain/theta-Q_tau contract.",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict, reason, accepted in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_scoring": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2071_0_Bcap_same_parent",
            "same-parent B_cap owns Pi_R_time_caps and N_tau_cap",
            "FAIL_BLOCKED",
            "B_mix_cap parent functional is missing.",
        ),
        (
            "GATE2071_1_Kcap_value",
            "K_cap_to_PiR value or theorem-zero can score",
            "FAIL_BLOCKED",
            "same functional, units, source path, cap surface and N_tau_cap are missing.",
        ),
        (
            "GATE2071_2_theta_Qtau",
            "parent theta_MTS/Q_tau^MTS route can reopen H_tau",
            "FAIL_BLOCKED",
            "total parent current-chain/action contract remains unpromoted.",
        ),
        (
            "GATE2071_3_MHref",
            "M_H_ref positive same-frame denominator can score",
            "FAIL_BLOCKED",
            "H_tau integrability, fixed reference and positivity remain unsigned.",
        ),
        (
            "GATE2071_4_qR",
            "q_R/local PPN scoring can use cap rows",
            "FAIL_BLOCKED",
            "absolute Pi_R join and q_R normalization chain remain incomplete.",
        ),
        (
            "GATE2071_5_local_GR",
            "local GR/Newton/PPN/R10 claim can be made",
            "FAIL_BLOCKED",
            "neither Bcap/Kcap nor MHref route is score-ready.",
        ),
        (
            "GATE2071_6_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "2071 is contained in post-checkpoint-work.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2071_0_bcap_progress",
            "BCAP_ROUTE_REDUCED_TO_BMIX_CAP_FUNCTIONAL",
            "The coupling blocker is now exact: a mixed cap functional must own both Pi_R and cap-current leakage.",
        ),
        (
            "DEC2071_1_no_fake_unity",
            "KCAP_CANNOT_BE_SET_TO_ONE_OR_ZERO_BY_CONVENTION",
            "K_cap_to_PiR needs a source equation, units and denominator, or a parent theorem-zero.",
        ),
        (
            "DEC2071_2_denominator_route",
            "MHREF_ROUTE_RETURNS_TO_PARENT_THETA_QTAU_CURRENT_CHAIN",
            "M_H_ref is structurally clean but depends on parent theta/Q_tau and fixed-reference closure.",
        ),
        (
            "DEC2071_3_best_next",
            "TARGET_BMIX_CAP_OR_PARENT_CURRENT_CHAIN",
            "The least-scrutiny path is to construct B_mix_cap directly; if not, derive the parent current-chain that owns theta_MTS and Q_tau^MTS.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2071_0_2072",
            "target_doc": "2072-Y5-R2FR-Bmix-cap-functional-or-parent-current-chain-theta-Qtau.md",
            "objective": "construct the mixed cap functional B_mix_cap whose variations yield both Pi_R_time_caps and N_tau_cap, or reopen the parent current-chain action contract that extracts theta_MTS and Q_tau^MTS",
            "must_include": "field list; cap surface C_cap; B_mix_cap action term; delta/delta R_AB variation; tau/current variation; source/reference cap split; K_cap units/value/theorem-zero; fixed reference; q_R normalization guard",
            "excluded": "K=1 by convention; absence-as-zero; fixed R_AB shortcut; fitted H_ref; orbital GM import; cancellation; local-GR/PPN/R10 scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    bcap_rows: list[dict[str, object]],
    same_parent_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    kcap_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2071_0_source_weight_Bcap",
            SOURCE_WEIGHT_DOCS / "AFRAME_BCAP_SAME_PARENT_FUNCTIONAL_2071_NONCLAIM.csv",
            bcap_rows,
        ),
        (
            "COPY2071_1_source_weight_same_parent_test",
            SOURCE_WEIGHT_DOCS / "AFRAME_BCAP_SAME_PARENT_TEST_2071_NONCLAIM.csv",
            same_parent_rows,
        ),
        (
            "COPY2071_2_source_weight_theta_Qtau",
            SOURCE_WEIGHT_DOCS / "AFRAME_THETA_QTAU_DENOMINATOR_ROUTE_2071_NONCLAIM.csv",
            theta_rows,
        ),
        (
            "COPY2071_3_source_weight_Kcap_schema",
            SOURCE_WEIGHT_DOCS / "AFRAME_KCAP_BMIX_SOURCE_SCHEMA_2071_NONCLAIM.csv",
            kcap_rows,
        ),
        (
            "COPY2071_4_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2071_BCAP_THETA_QTAU_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2071_5_queue_next",
            QUEUE / "JR2071_BMIX_CAP_OR_PARENT_CURRENT_CHAIN_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    bcap_rows: list[dict[str, object]],
    same_parent_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    kcap_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    bcap_ok = (
        any(row["row_id"] == "BFC2071_3_Bmix_required" and row["status"] == "MISSING_PARENT_BMIX_CAP_FUNCTIONAL" for row in bcap_rows)
        and any(row["row_id"] == "BFC2071_6_verdict" and row["status"] == "BCAP_ROUTE_BLOCKED_ON_BMIX_PARENT_FUNCTIONAL" for row in bcap_rows)
        and all(not bool(row["ready_for_scoring"]) for row in bcap_rows)
    )
    same_parent_ok = (
        any(row["row_id"] == "SPT2071_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_BCAP_SAME_PARENT_UNSIGNED" for row in same_parent_rows)
        and all(not bool(row["test_pass"]) for row in same_parent_rows)
    )
    theta_ok = (
        any(row["row_id"] == "TQR2071_7_verdict" and row["status"] == "THETA_QTAU_ROUTE_BLOCKED_ON_PARENT_CURRENT_CHAIN" for row in theta_rows)
        and all(not bool(row["ready_for_scoring"]) for row in theta_rows)
    )
    kcap_ok = (
        len(kcap_rows) == 1
        and kcap_rows[0]["status"] == "SOURCE_ROW_SCHEMA_ONLY"
        and "MISSING" in str(kcap_rows[0]["B_mix_cap_functional"])
        and "MISSING" in str(kcap_rows[0]["K_cap_value"])
    )
    dry_ok = any(
        row["run_id"] == "RUN2071_VERDICT"
        and row["verdict"] == "BMIX_CAP_FUNCTIONAL_MISSING_ROUTE_TO_PARENT_CURRENT_CHAIN"
        and not bool(row["accepted_for_scoring"])
        for row in dry_rows_
    )
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2071_0_2072"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, bcap_rows, same_parent_rows, theta_rows, kcap_rows, dry_rows_, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2071_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2071_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2071_02_Bcap_route", bcap_ok, "B_cap route is reduced to missing B_mix_cap parent functional"),
        ("VAL2071_03_same_parent_test", same_parent_ok, "same-parent test fails explicitly rather than promoting Kcap"),
        ("VAL2071_04_theta_Qtau_route", theta_ok, "theta/Q_tau route remains blocked on parent current-chain"),
        ("VAL2071_05_Kcap_schema", kcap_ok, "Kcap source row remains placeholder-marked and nonclaim"),
        ("VAL2071_06_dry_verdict", dry_ok, "dry run routes to 2072 without scoring"),
        ("VAL2071_07_claim_gates_blocked", gates_ok, "all local claim gates remain blocked/nonclaim"),
        ("VAL2071_08_next_selected", next_ok, "2072 Bmix-cap or parent-current-chain target selected"),
        ("VAL2071_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2071_10_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2071_11_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2071_12_no_formalization_artifacts", not formalization_has_2071_artifacts(), "no 2071 artifacts were written under formalization-workbench"),
        ("VAL2071_13_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2071_OVERALL", overall, "2071 sharpens the coupling blocker without promoting a local claim"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    bcap_rows: list[dict[str, object]],
    same_parent_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    kcap_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2071 Y5 R2FR Bcap Same Parent Functional Or Theta Qtau Denominator Route",
        "",
        "## Current Verdict",
        "",
        "2071 does not close the local-GR/PPN branch, but it sharply locates the coupling gap. The only Bcap route that can own both sides of the conversion is a mixed parent cap functional `B_mix_cap[R_AB,tau,T_H]`. A pure `R_AB` cap term can produce `pi_R^cap`; a pure tau/current cap term can produce `N_tau_cap`; neither is enough alone.",
        "",
        "Therefore `K_cap_to_PiR` still cannot be set to `1`, `0`, or any numeric value by convention. It remains a source-row slot until one same parent functional generates `Pi_R_time_caps_abs` and `N_tau_cap` with declared cap surface, units, source/reference split, and q_R normalization guard.",
        "",
        "The denominator route through `M_H_ref = H_tau[S_link] - H_ref` is still the structurally clean fallback, but it returns us to the parent current-chain: extract `theta_MTS` and `Q_tau^MTS`, fix the reference before readout, prove integrability/positivity, and only then reopen local scoring.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, MHref, or q_R claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Bcap Functional Candidate Ledger",
        md_table(bcap_rows, ["row_id", "object_id", "candidate_formula", "same_parent_requirement", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## Same Parent Test",
        md_table(same_parent_rows, ["row_id", "clause", "evidence", "status", "test_pass", "claim_allowed"]),
        "## Theta Qtau Denominator Route",
        md_table(theta_rows, ["row_id", "object_id", "formula", "required_input", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## Kcap Bmix Source Schema",
        md_table(kcap_rows, ["row_id", "system_id", "B_mix_cap_functional", "PiR_cap_abs", "N_tau_cap_abs", "K_cap_to_PiR_formula", "K_cap_value", "K_cap_units", "source_path", "status", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry_rows_, ["run_id", "target", "verdict", "reason", "accepted_for_scoring", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    bcap_rows = bcap_candidate_rows()
    same_parent_rows = same_parent_test_rows()
    theta_rows = theta_qtau_route_rows()
    kcap_rows = kcap_schema_rows()
    dry_rows_ = dry_run_rows(bcap_rows, same_parent_rows, theta_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2071_SOURCE_REGISTER.csv",
        "bcap": OUT / "P8_Y5_PARENT_QLOC_2071_BCAP_FUNCTIONAL_CANDIDATE_LEDGER.csv",
        "same_parent": OUT / "P8_Y5_PARENT_QLOC_2071_SAME_PARENT_TEST.csv",
        "theta": OUT / "P8_Y5_PARENT_QLOC_2071_THETA_QTAU_DENOMINATOR_ROUTE.csv",
        "kcap": OUT / "P8_Y5_PARENT_QLOC_2071_KCAP_BMIX_SOURCE_SCHEMA.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2071_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2071_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2071_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2071_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2071_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2071_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["bcap"], bcap_rows)
    write_csv(paths["same_parent"], same_parent_rows)
    write_csv(paths["theta"], theta_rows)
    write_csv(paths["kcap"], kcap_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(bcap_rows, same_parent_rows, theta_rows, kcap_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(
        sources,
        bcap_rows,
        same_parent_rows,
        theta_rows,
        kcap_rows,
        dry_rows_,
        gates,
        next_rows_,
        copies,
        csv_paths,
    )
    write_csv(paths["validation"], validation)
    write_doc(sources, bcap_rows, same_parent_rows, theta_rows, kcap_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
