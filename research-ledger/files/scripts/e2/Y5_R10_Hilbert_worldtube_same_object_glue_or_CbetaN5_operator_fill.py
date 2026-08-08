from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "941-Y5-R10-Hilbert-worldtube-same-object-glue-or-CbetaN5-operator-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "940_doc",
            "path": "940-Y5-R10-chain-map-Hilbert-equality-or-CbetaN5-operator-source.md",
            "role": "handoff selecting Hilbert worldtube same-object route",
            "needle": "941-Y5-R10-Hilbert-worldtube-same-object-glue-or-CbetaN5-operator-fill.md",
        },
        {
            "source_id": "940_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_940_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V940_14_validation_rows_ready",
        },
        {
            "source_id": "662_doc",
            "path": "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
            "role": "same-object theorem and R_glue residual identity",
            "needle": "Q_H[W] = H_tau[S] - H_ref",
        },
        {
            "source_id": "510_doc",
            "path": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
            "role": "GR/EH worldtube source-measure reference theorem",
            "needle": "worldtube_source_measure_glue_theorem_contract_built_EH_known_MTS_not_derived",
        },
        {
            "source_id": "HWT536_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
            "role": "machine theorem-step rows for Hilbert worldtube glue",
            "needle": "HWT536_0_parent_worldtube_fixed",
        },
        {
            "source_id": "HWG535_certificate",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            "role": "missing worldtube/certificate rows",
            "needle": "HWG535_0_worldtube_fixed_before_readout",
        },
        {
            "source_id": "PAC537_contract",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "role": "parent action clauses required for HWT536",
            "needle": "PAC537_2_parent_fixed_worldtube",
        },
        {
            "source_id": "WT510_theorem",
            "path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            "role": "EH conditional source-measure theorem",
            "needle": "T510_2_MTS_transfer_condition",
        },
        {
            "source_id": "WT510_clauses",
            "path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
            "role": "worldtube source-measure clause status",
            "needle": "WG510_1_minimal_observed_matter_coupling",
        },
        {
            "source_id": "WT510_proof",
            "path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
            "role": "Noether/Stokes proof sketch",
            "needle": "P510_5",
        },
        {
            "source_id": "Hilbert_monopole",
            "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
            "role": "measured-GM and second-order source calibration",
            "needle": "HM7_second_order_source_stability",
        },
        {
            "source_id": "940_cbeta",
            "path": "source-intake/mts_residuals/P8_Y5_R10_940_CBETA_OPERATOR_SOURCE.csv",
            "role": "Cbeta operator schema from 940",
            "needle": "CBS940_2_C_beta_N5",
        },
        {
            "source_id": "local_beta_bound",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "R4 beta observation row",
            "needle": "R4_beta",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def same_object_proof_stack() -> list[dict[str, str]]:
    specs = [
        (
            "SOG941_0_parent_action",
            "explicit diffeomorphism-covariant parent action owns the Hilbert current and Noether charge",
            "delta L = E_A delta Phi^A + dTheta; J_tau = Theta(Phi,L_tau Phi)-tau dot L",
            "without parent variation, worldtube charge is only named",
            "contract_only_no_full_Lagrangian",
        ),
        (
            "SOG941_1_single_observed_source_frame",
            "matter couples to one observed metric/coframe used by source, clocks, rods, and orbital readout",
            "S_matter = S_matter[e_obs,psi_m]; J_H[tau]=delta S_matter/delta e_obs contracted with tau",
            "prevents source mass and orbital mass from living in different frames",
            "not_parent_signed",
        ),
        (
            "SOG941_2_parent_fixed_worldtube",
            "compact source support and linking surfaces are selected before fitted readout",
            "W_source=supp(J_H[tau]); S_1,S_2 link W_source; delta W_source=0 on allowed branch",
            "prevents retuning the mass channel per radius/system",
            "not_parent_signed_key_blocker",
        ),
        (
            "SOG941_3_dressed_charge",
            "source charge is dressed Hamiltonian/Noether charge, not bare rest mass",
            "Q_H[W] := H_tau[S_outer]-H_ref",
            "includes binding/reference/field energy owned by the parent charge",
            "guardrail_adopted_not_derived",
        ),
        (
            "SOG941_4_same_worldtube_PD",
            "topological representative is Poincare-dual to the same Hilbert worldtube",
            "J_M^top := Q_H[W] PD(W_source), not Q_independent omega_independent",
            "prevents closed topology from conserving the wrong object",
            "not_parent_signed_key_blocker",
        ),
        (
            "SOG941_5_action_owned_PiM_chain_map",
            "Pi_M is fixed by parent algebra and commutes on the same current complex",
            "[d,Pi_M]J_H=0; int_S Pi_M J_H = 4*pi*G_ref(H_tau-H_ref)",
            "connects surface charge to projected Hilbert source without commutator hair",
            "not_parent_signed",
        ),
        (
            "SOG941_6_zero_reference_boundary_flux",
            "reference, exact improvement, and boundary terms have zero linked flux",
            "int_boundary dB_zero=0; H_ref fixed once; Delta_symp=0 or retained",
            "prevents hidden monopole/boundary offset",
            "missing_certificate_or_bound",
        ),
        (
            "SOG941_7_extra_sector_mass_silence",
            "non-EH/domain/memory/range/connection/source sectors carry no independent compact mass charge",
            "Delta_extra=Delta_frame=Delta_nonEH=0 or source-backed below local locks",
            "keeps MTS from getting GR-looking source closure by hidden charge channels",
            "field_specific_queue_open",
        ),
        (
            "SOG941_8_readout_PPN_stability",
            "same charge controls 1/r coefficient and survives second-order PPN expansion",
            "g_00=-1+2G_ref M_source/r+O(r^-2); delta_beta_source=0",
            "turns same-object charge into local GR, not just Newton-looking leading order",
            "not_reached",
        ),
        (
            "SOG941_9_total_verdict",
            "if SOG941_0 through SOG941_8 hold, Hilbert and topological charges are the same parent object",
            "R_glue=Pi_M J_H-J_M^top-dB_zero=0; d(Pi_M J_H)=0",
            "would close the PiM source-normalization branch honestly",
            "conditional_theorem_not_current_claim",
        ),
    ]
    return [
        {
            "step_id": step_id,
            "needed_statement": needed_statement,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "current_status": current_status,
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for step_id, needed_statement, mathematical_form, why_needed, current_status in specs
    ]


def obstruction_audit() -> list[dict[str, str]]:
    specs = [
        (
            "OBS941_0_worldtube_selector",
            "W_source=supp(J_H) fixed before readout",
            "source support/domain selector can still be chosen after seeing residuals",
            "R_worldtube;Delta_worldtube_domain",
            "primary_next_target",
        ),
        (
            "OBS941_1_same_frame_measure",
            "one observed source frame",
            "matter/source, clock, rod, and orbital readouts may live in split frames",
            "R_measure;Delta_frame",
            "primary_next_target",
        ),
        (
            "OBS941_2_topological_same_object",
            "J_M^top=Q_H[W]PD(W_source)",
            "topological label can be conserved independently of Hilbert source mass",
            "R_top;R_eq",
            "blocked_by_worldtube_selector",
        ),
        (
            "OBS941_3_PiM_chain_map",
            "[d,Pi_M]J_H=0 on same current complex",
            "commutator/projector stress survives if Pi_M is not parent-owned",
            "R_PiM;I_commutator;T_PiM",
            "blocked_by_PiM_parent_ownership",
        ),
        (
            "OBS941_4_boundary_flux",
            "int_boundary dB_zero=0 and fixed reference",
            "exact terms can carry compact boundary charge",
            "R_boundary;B_zero_flux;Delta_symp",
            "blocked_by_boundary_certificate",
        ),
        (
            "OBS941_5_readout_stability",
            "charge controls weak-field metric and beta order",
            "closed charge may still not be measured GM or beta-safe",
            "Delta_cal;Delta_PPN;C_beta_N5",
            "not_reached",
        ),
    ]
    return [
        {
            "obstruction_id": obstruction_id,
            "target": target,
            "failure_mode": failure_mode,
            "residual_if_missing": residual_if_missing,
            "priority": priority,
            "resolved": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for obstruction_id, target, failure_mode, residual_if_missing, priority in specs
    ]


def residual_template() -> list[dict[str, str]]:
    specs = [
        (
            "RWT941_0_R_glue_integral",
            "R_glue_integral",
            "int_A dR_glue with R_glue=Pi_M J_H-J_M^top-dB_zero",
            "system_id;r1;r2;R_glue_integral;M_ref;units;normalization;source_file;assumptions;valid_for_claim",
            "MISSING_NUMERIC_OR_THEOREM_ZERO_INPUT",
        ),
        (
            "RWT941_1_worldtube_domain_shift",
            "Delta_worldtube_domain",
            "fractional change in Q_H[W] under allowed worldtube/linking-surface choices",
            "system_id;domain_rule;Delta_worldtube_domain;M_ref;units;source_file;assumptions;valid_for_claim",
            "MISSING_DOMAIN_SELECTOR_BOUND",
        ),
        (
            "RWT941_2_measure_frame_shift",
            "Delta_frame_source",
            "same-frame source measure mismatch between source, metric, clocks, and orbits",
            "system_id;frame_pair;Delta_frame_source;local_lock;source_file;assumptions;valid_for_claim",
            "MISSING_FRAME_BOUND_OR_THEOREM",
        ),
        (
            "RWT941_3_boundary_reference_flux",
            "B_zero_flux;Delta_symp",
            "reference, exact improvement, and symplectic boundary charge shift",
            "system_id;boundary_rule;B_zero_flux;Delta_symp;M_ref;source_file;assumptions;valid_for_claim",
            "MISSING_BOUNDARY_REFERENCE_INPUT",
        ),
        (
            "RWT941_4_PiM_commutator_stress",
            "I_commutator;T_PiM_munu",
            "commutator integral and projector stress inherited from unsigned PiM chain map",
            "system_id;operator_family;I_commutator;projector_stress_beta_equiv;affected_PPN_rows;source_file;assumptions;valid_for_claim",
            "MISSING_PIM_BOUND_INPUT",
        ),
        (
            "RWT941_5_epsilon_glue",
            "epsilon_glue_Meff",
            "epsilon_glue = component-sum absolute normalized R_glue residual",
            "system_id;epsilon_glue;component_sum_abs;M_ref;normalization;source_file;assumptions;valid_for_claim",
            "MISSING_COMPONENT_INPUTS",
        ),
    ]
    return [
        {
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "required_columns": required_columns,
            "current_status": current_status,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for input_id, quantity, definition, required_columns, current_status in specs
    ]


def cbeta_operator_fill() -> list[dict[str, str]]:
    beta_bound = ""
    beta_source = ""
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == "R4_beta":
            beta_bound = row.get("upper_bound", "")
            beta_source = row.get("reference_path_or_url", "")
            break
    specs = [
        (
            "CBF941_0_R4_beta_bound",
            "beta_bound",
            beta_bound,
            beta_source,
            "source_bound_loaded",
        ),
        (
            "CBF941_1_operator_kernel",
            "L_EH^(4)",
            "second-order weak-field operator taking S_N5 to delta g_00^(4)",
            "MISSING_SECOND_ORDER_WEAK_FIELD_OPERATOR_SOURCE",
            "operator_missing",
        ),
        (
            "CBF941_2_source_vector",
            "S_N5",
            "{R_glue,I_commutator,T_PiM,B_zero_flux,Delta_extra,Delta_cal}",
            "MISSING_NUMERIC_OR_THEOREM_ZERO_SOURCE_VECTOR",
            "source_vector_missing",
        ),
        (
            "CBF941_3_C_beta_N5",
            "C_beta_N5",
            "-delta g_00_N5^(4)/(2 U^2 X_N5)",
            "MISSING_OPERATOR_SOLUTION_AND_PROFILE",
            "formal_definition_only",
        ),
        (
            "CBF941_4_score_gate",
            "score_gate",
            "|C_beta_N5 X_N5| <= 7.8e-05 only after every source component is real or theorem-zero",
            "derived_gate_no_numeric_prediction",
            "score_blocked",
        ),
    ]
    return [
        {
            "operator_id": operator_id,
            "symbol": symbol,
            "definition_or_formula": definition_or_formula,
            "source_or_missing_input": source_or_missing_input,
            "status": status,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for operator_id, symbol, definition_or_formula, source_or_missing_input, status in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC941_0_same_object",
            "decision": "same_object_glue_not_proved",
            "reason": "parent worldtube selector, same observed source frame, topological same-object certificate, zero boundary flux, and readout stability remain unsigned",
            "consequence": "R_glue remains active and d(Pi_M J_H)=0 cannot be claimed",
            "next_action": "attack parent worldtube selector and source-frame lock first",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC941_1_best_route",
            "decision": "worldtube_selector_source_frame_selected_next",
            "reason": "without W_source=supp(J_H) and one observed source frame, the topological PD object can be a conserved wrong charge",
            "consequence": "same-object proof narrows to source support and frame ownership",
            "next_action": "942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC941_2_Cbeta",
            "decision": "Cbeta_operator_fill_still_blocked",
            "reason": "operator kernel and source vector require either theorem-zero R_glue components or numeric profiles",
            "consequence": "no beta score or local-GR claim",
            "next_action": "defer Cbeta fill until source-glue route stalls or residual data exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE941_0_same_worldtube",
            "claim": "J_M^top is the PD representative of the same Hilbert source worldtube",
            "blocker": "worldtube selector and topological same-object certificate missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE941_1_same_source_frame",
            "claim": "source, clock, rod, and orbital readout use one observed frame",
            "blocker": "single observed matter/coframe source clause not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE941_2_R_glue_zero",
            "claim": "R_glue=0 and d(Pi_M J_H)=0",
            "blocker": "same-object, PiM chain-map, zero boundary flux, and hidden-sector silence are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE941_3_Cbeta_score",
            "claim": "C_beta_N5 operator row is numeric and scoreable",
            "blocker": "weak-field operator kernel and source vector are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE941_4_local_GR",
            "claim": "Newton/local-GR/PPN branch is derived",
            "blocker": "source-glue and readout/PPN stability remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md",
            "objective": "derive W_source=supp(J_H) and one observed source frame before readout, or fill the C_beta_N5 weak-field operator kernel row",
            "include": "parent source support selector, fixed linking surfaces, S_matter[e_obs,psi], J_H[tau], frame locks for clocks/rods/orbits, residual Delta_worldtube_domain/Delta_frame, fallback L_EH^(4) kernel",
            "exclude": "assuming same-worldtube object, independent topological label, late equality multiplier, beta pass claim, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_940_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    total_conditional = any(row["step_id"] == "SOG941_9_total_verdict" and row["current_status"] == "conditional_theorem_not_current_claim" for row in proof_rows)
    proof_no_claim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in proof_rows)
    primary_worldtube = any(row["obstruction_id"] == "OBS941_0_worldtube_selector" and row["priority"] == "primary_next_target" for row in obstruction_rows)
    primary_frame = any(row["obstruction_id"] == "OBS941_1_same_frame_measure" and row["priority"] == "primary_next_target" for row in obstruction_rows)
    residuals_blocked = residual_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in residual_rows)
    cbeta_blocked = any(row["operator_id"] == "CBF941_3_C_beta_N5" and row["status"] == "formal_definition_only" for row in cbeta_rows) and any(row["operator_id"] == "CBF941_4_score_gate" and row["status"] == "score_blocked" for row in cbeta_rows)
    beta_bound_loaded = any(row["operator_id"] == "CBF941_0_R4_beta_bound" and row["definition_or_formula"] == "7.8e-05" for row in cbeta_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("942-Y5-R10-parent-worldtube-selector-source-frame") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + proof_rows + obstruction_rows + residual_rows + cbeta_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V941_0_sources_exist_and_needles", sources_ok, "all 941 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V941_1_prior_940_clean", prior_clean, "P8_Y5_BRR545_940_VALIDATION.csv clean")
    add("V941_2_same_object_theorem_conditional", total_conditional, "same-object theorem remains conditional only")
    add("V941_3_proof_no_claim", proof_no_claim, "no same-object proof row promoted")
    add("V941_4_worldtube_primary", primary_worldtube, "worldtube selector selected as primary next target")
    add("V941_5_frame_primary", primary_frame, "same observed source frame selected as primary next target")
    add("V941_6_residuals_blocked", residuals_blocked, "R_glue residual template remains non-scoreable")
    add("V941_7_Cbeta_blocked", cbeta_blocked, "C_beta_N5 operator fill remains formal and blocked")
    add("V941_8_beta_bound_loaded", beta_bound_loaded, "R4 beta bound 7.8e-05 loaded")
    add("V941_9_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V941_10_claim_gates_false", claims_false, "all claim gates remain false")
    add("V941_11_next_target_selected", next_selected, "942 parent worldtube selector/source-frame target selected")
    add("V941_12_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V941_13_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V941_14_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 941 - Y5/R10 Hilbert Worldtube Same-Object Glue Or CbetaN5 Operator Fill

Generated: `{stamp()}`

Status: `Y5_R10_941_Hilbert_worldtube_same_object_glue_not_proved_worldtube_selector_source_frame_selected_nonclaim`

Claim ceiling: `same_object_worldtube_gate_only_no_R_glue_zero_no_closed_PiM_flux_no_beta_score_no_local_GR_pass`

## Result

The honest same-object theorem would be:

```text
W_source = supp(J_H[tau]),
Q_H[W] = H_tau[S_outer] - H_ref,
J_M^top = Q_H[W] PD(W_source),
Pi_M J_H = J_M^top + dB_zero,
int_boundary dB_zero = 0.
```

That would make the topological charge and Hilbert source charge the same parent object, not two separately named objects glued together after the fact.

941 does **not** prove this. The parent still has not signed:

```text
S_matter = S_matter[e_obs, psi],
J_H[tau] from the same observed source frame,
W_source fixed by source support before readout,
topological PD representative of that same W_source,
zero B_zero/reference flux,
extra-sector mass silence,
second-order PPN/readout stability.
```

So `R_glue=0`, `d(Pi_M J_H)=0`, measured-GM normalization, beta safety, and local-GR reduction remain blocked.

The next lever is now very concrete: prove `W_source=supp(J_H)` and the one observed source frame before readout. If that fails, fill `Delta_worldtube_domain` and `Delta_frame_source` as residuals, or source the weak-field `C_beta_N5` kernel.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Same-Object Proof Stack

{md_table(proof_rows, ["step_id", "needed_statement", "mathematical_form", "current_status", "claim_allowed"])}

## Obstruction Audit

{md_table(obstruction_rows, ["obstruction_id", "target", "failure_mode", "residual_if_missing", "priority", "resolved"])}

## Residual Template

{md_table(residual_rows, ["input_id", "quantity", "definition", "current_status", "score_ready"])}

## Cbeta Operator Fill

{md_table(cbeta_rows, ["operator_id", "symbol", "definition_or_formula", "source_or_missing_input", "status", "score_ready"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def ensure_csv_roundtrip(paths: list[Path]) -> None:
    for path in paths:
        rows = read_csv(path)
        if rows and any(None in row for row in rows):
            raise SystemExit(f"malformed CSV row in {path}")


def main() -> None:
    sources = source_register()
    proof_rows = same_object_proof_stack()
    obstruction_rows = obstruction_audit()
    residual_rows = residual_template()
    cbeta_rows = cbeta_operator_fill()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, proof_rows, obstruction_rows, residual_rows, cbeta_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_941_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_941_SAME_OBJECT_PROOF_STACK.csv",
            proof_rows,
            ["step_id", "needed_statement", "mathematical_form", "why_needed", "current_status", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_941_OBSTRUCTION_AUDIT.csv",
            obstruction_rows,
            ["obstruction_id", "target", "failure_mode", "residual_if_missing", "priority", "resolved", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_941_RESIDUAL_TEMPLATE.csv",
            residual_rows,
            ["input_id", "quantity", "definition", "required_columns", "current_status", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_941_CBETA_OPERATOR_FILL.csv",
            cbeta_rows,
            ["operator_id", "symbol", "definition_or_formula", "source_or_missing_input", "status", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_941_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_941_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_941_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_941_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, proof_rows, obstruction_rows, residual_rows, cbeta_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_941_Hilbert_worldtube_same_object_glue_not_proved_worldtube_selector_source_frame_selected_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md")


if __name__ == "__main__":
    main()
