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


DOC = ROOT / "2166-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOCS = {
    "2165": ROOT / "2165-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md",
    "2165_validation": OUT / "P8_Y5_BRR545_2165_VALIDATION.csv",
    "2165_next": OUT / "P8_Y5_PARENT_QLOC_2165_NEXT_TARGET.csv",
    "1864": ROOT / "1864-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md",
    "1864_validation": OUT / "P8_Y5_BRR545_1864_VALIDATION.csv",
    "1865": ROOT / "1865-Y5-R2FR-parent-Euler-difference-normal-form-or-SR-residual-decomposition.md",
    "1865_validation": OUT / "P8_Y5_BRR545_1865_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2166_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_2166_LOCAL_GR_REDUCTION_THEOREM.csv",
    "sr_map": OUT / "P8_Y5_PARENT_QLOC_2166_RLOCAL_TO_SR_MAP.csv",
    "prioritizer": OUT / "P8_Y5_PARENT_QLOC_2166_PROOF_ATTACK_PRIORITIZER.csv",
    "first_attack": OUT / "P8_Y5_PARENT_QLOC_2166_FIRST_ATTACK_STATUS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2166_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2166_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2166_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2166_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2166_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2166_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_LOCAL_GR_CONTRACT_2166_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2166_SR_VECTOR_NONCLAIM.csv",
    "queue": QUEUE / "JR2166_RECIPROCITY_SELECTOR_OR_HCORE_QUEUE.csv",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2166_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2166-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2166*",
        "*P8_Y5_BRR545_2166*",
        "*Y5_R2FR_local_GR_reduction_contract_and_residual_vector_prioritizer_2166*",
        "*AFRAME_LOCAL_GR_CONTRACT_2166*",
        "*JR2166*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2166_00_2165_handoff", DOCS["2165"], [["NEXT2165_0_2166"], ["IJX2165_4_total_vector"], ["VAL2165_OVERALL"]], "2165 routes R_local^MTS into the local-GR contract."),
        ("SRC2166_01_2165_validation", DOCS["2165_validation"], [["VAL2165_OVERALL"], ["PASS"]], "2165 validation passed as nonclaim."),
        ("SRC2166_02_2165_next_csv", DOCS["2165_next"], [["NEXT2165_0_2166"], ["local-GR"], ["residual"]], "machine-readable 2166 handoff."),
        ("SRC2166_03_1864_contract", DOCS["1864"], [["LGT1864_6_verdict"], ["RSM1864_7_readout_projection"], ["NEXT1864_0_primary"]], "prior local-GR theorem contract and residual prioritizer."),
        ("SRC2166_04_1864_validation", DOCS["1864_validation"], [["VAL1864_OVERALL"], ["PASS"]], "1864 validation passed as nonclaim."),
        ("SRC2166_05_1865_dr_attempt", DOCS["1865"], [["DRA1865_6_verdict"], ["SRD1865_8_total"], ["NEXT1865_0_primary"]], "prior D_R derivation attempt finds generic Euler-difference obstruction and selects reciprocity selector/H_core."),
        ("SRC2166_06_1865_validation", DOCS["1865_validation"], [["VAL1865_OVERALL"], ["PASS"]], "1865 validation passed as nonclaim."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def theorem_rows() -> list[dict[str, object]]:
    data = [
        ("LGT2166_0_variables", "local reciprocal variables", "J_q:=T sqrt(S); C_R:=ln(T^2 S)=2 ln(J_q)", "EXACT_DEFINITION", "C_R=0 is equivalent to reciprocal local branch T^2 S=1"),
        ("LGT2166_1_parent_Euler_pair", "parent E_time/E_radial", "derive E_time=delta S_parent/delta ln(T), E_radial=delta S_parent/delta ln(sqrt(S)) from MTS parent action", "MISSING_EULER_PAIR", "legal variables for a reduction proof are not yet parent-owned"),
        ("LGT2166_2_DR_normal_form", "D_R[MTS] normal form", "D_R=E_time-E_radial=partial_r C_R-S_R[R_local^MTS,source,boundary,readout]=0, or partial_r(W partial_r C_R)-J_R=0", "CONTRACT_READY_NOT_DERIVED", "generic Euler difference does not force this form"),
        ("LGT2166_3_SR_silence", "S_R=0 or finite-bounded", "all R_local^MTS components must vanish by theorem or be retained as finite absolute bounds", "RESIDUAL_VECTOR_RETAINED", "no coupling/source/readout term may be hidden in fitted GM"),
        ("LGT2166_4_boundary_no_charge", "Q_R=0 and normalization", "boundary/source neutrality plus C_R(infinity)=0 integrates the source-free equation to C_R=0", "BOUNDARY_NO_CHARGE_UNSIGNED", "conserved current alone leaves Q_R hair"),
        ("LGT2166_5_reciprocal_consequence", "local GR-style branch", "if LGT2166_1 through LGT2166_4 close, C_R=0; with T^2=1-L and S=(1-L)^(-p), p=1", "EXACT_CONDITIONAL_NOT_ACTIVATED", "would be the serious local GR/Newton reduction route"),
        ("LGT2166_6_verdict", "local GR/Newton derivation", "current MTS has theorem contract but not parent Euler pair, D_R normal form, S_R silence or Q_R no-charge", "LOCAL_GR_REDUCTION_CONTRACT_READY_NOT_DERIVED", "select reciprocity-selector/H_core source equation as next missing gear"),
    ]
    return [row(theorem_id=theorem_id, object=object_name, statement=statement, status=status, consequence=consequence) for theorem_id, object_name, statement, status, consequence in data]


def sr_map_rows() -> list[dict[str, object]]:
    data = [
        ("RSM2166_0_Delta_Hsrc", "S_R_source_measure", "Delta_Hsrc", "c_H Delta_Hsrc/M_H_ref", "CENTRAL_Y5_RESIDUAL_RETAINED", "orbital;Gauss;PPN;Newton"),
        ("RSM2166_1_I_X", "S_R_current_curl", "I_X", "c_I I_X/M_H_ref", "NOT_THEOREM_ZERO", "orbital;PPN;source_normalization;local_GR"),
        ("RSM2166_2_J_X_qbarXT", "S_R_matter_source", "J_X/qbar_XT", "c_J J_X + c_q qbar_XT", "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING", "R10;WEP;clock;PPN;orbital"),
        ("RSM2166_3_constants", "S_R_constant_composition", "b_alpha,b_mu,b_mA,b_nuc,b_clock_i", "c_alpha b_alpha + c_mu b_mu + c_A b_mA + c_nuc b_nuc + Sigma_i c_clock_i b_clock_i", "ALPHA_MASS_CLOCK_CHANNELS_RETAINED", "fine_structure;WEP;clock;R10"),
        ("RSM2166_4_boundary_history", "S_R_boundary_history", "J_boundary,J_history,qbar_nonH", "c_B B_R + c_hist H_R + c_nonH qbar_nonH", "TAILS_NOT_ZERO_NOT_BOUNDED", "orbital;source_normalization;R10;local_GR"),
        ("RSM2166_5_q_loc", "S_R_extra_sector", "epsilon_GK_q_loc", "c_GK epsilon_GK_q_loc", "RETAIN_NONCLAIM", "local_GR;PPN;clock;orbital;WEP;R10"),
        ("RSM2166_6_reciprocal_hair", "S_R_QR_hair", "Q_R,J_R", "Q_R or int J_R dr after operator integration", "NO_CHARGE_THEOREM_NOT_DERIVED", "PPN_gamma;orbital;lightcone;local_GR"),
        ("RSM2166_7_readout", "S_R_readout_projection", "C_readout,Delta_Pi", "c_readout C_readout + c_proj Delta_Pi", "PURE_POSTPROCESSING_SAFE_NOT_GENERAL", "Pantheon;BAO;SPARC;R10;WEP;clock;PPN"),
        ("RSM2166_8_total", "S_R_total_abs", "S_R[R_local^MTS]", "|S_R| <= sum absolute values of RSM2166_0 through RSM2166_7", "SYMBOLIC_READY_VALUES_MISSING", "local_GR;PPN;orbital;R10;WEP;clock"),
    ]
    return [row(slot_id=slot_id, sr_slot=sr_slot, residual_symbol=residual_symbol, symbolic_entry=symbolic_entry, current_status=current_status, arena_links=arena_links) for slot_id, sr_slot, residual_symbol, symbolic_entry, current_status, arena_links in data]


def prioritizer_rows() -> list[dict[str, object]]:
    data = [
        ("PR2166_0_reciprocity_selector", "derive selector orientation/kernel or H_core source equation", 5, 4, 5, 5, "generic Euler difference no-go means this is the missing gear", "SELECT_FIRST"),
        ("PR2166_1_q_loc_live_pair", "Gamma_eff/K_hat live metric-response pair or S_R source row", 5, 3, 4, 4, "q_loc contaminates S_R, but selector must first define its slot", "SECOND_AFTER_SELECTOR"),
        ("PR2166_2_no_extra_matter_vertices", "forbid extra F2/mass/binding/source-weight vertices", 4, 3, 5, 5, "coupling gut-punch, held parallel until S_R coefficients are oriented", "HELD_PARALLEL_HIGH_VALUE"),
        ("PR2166_3_boundary_no_charge", "prove Q_R=0 and boundary/reference normalization", 4, 3, 3, 3, "necessary after S_R silence, but needs operator form", "THIRD_OR_PARALLEL_AFTER_OPERATOR"),
        ("PR2166_4_source_coefficients", "source finite S_R coefficients and units", 3, 4, 4, 4, "empirical backstop after selector/source map exists", "BACKSTOP_AFTER_OPERATOR"),
    ]
    return [row(priority_id=priority_id, target=target, impact=impact, tractability=tractability, dependency=dependency, scrutiny_risk=scrutiny_risk, rationale=rationale, selection=selection) for priority_id, target, impact, tractability, dependency, scrutiny_risk, rationale, selection in data]


def first_attack_rows() -> list[dict[str, object]]:
    data = [
        ("FAS2166_0_generic_action", "generic parent action slice", "for S=int dr L(x,y,x',y'), E_x-E_y=(partial_x-partial_y)L-d/dr[(partial_xprime-partial_yprime)L]", "DERIVED_GENERIC_IDENTITY", "too weak to imply partial_r C_R-S_R"),
        ("FAS2166_1_orientation", "Euler orientation/sign", "which parent variation combination selects C_R must be parent-signed", "ORIENTATION_CERTIFICATE_REQUIRED", "cannot infer from GR equation difference"),
        ("FAS2166_2_selector", "reciprocity selector/operator", "need parent kernel yielding partial_r C_R or partial_r(W partial_r C_R)", "MISSING_RECIPROCITY_SELECTOR_OR_PARENT_KERNEL", "no no-hair/local reciprocity theorem can run"),
        ("FAS2166_3_SR_decomposition", "S_R residual source map", "all known local residuals have symbolic S_R slots", "SYMBOLIC_DECOMPOSITION_READY_NONCLAIM", "coefficients/units/source maps missing"),
        ("FAS2166_4_verdict", "first proof attack", "D_R normal form was attempted through generic variation and did not derive", "DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS", "target H_core/selector/source equation next"),
    ]
    return [row(attack_id=attack_id, target=target, statement=statement, status=status, consequence=consequence) for attack_id, target, statement, status, consequence in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2166_0_contract_ready", "local-GR reduction theorem contract is exact conditional", True, "C_R=0 consequence is clean if premises close"),
        ("CG2166_1_DR_derived", "D_R[MTS]=partial_r C_R-S_R is derived", False, "selector/orientation/H_core missing"),
        ("CG2166_2_SR_zero", "S_R=0 on local branch", False, "all residual slots remain nonclaim"),
        ("CG2166_3_QR_zero", "Q_R boundary/no-charge theorem closes", False, "boundary/source neutrality unsigned"),
        ("CG2166_4_local_GR", "MTS derives local GR/Newton branch", False, "D_R/S_R/Q_R premises not closed"),
        ("CG2166_5_empirical_ready", "S_R residual vector can be scored", False, "coefficients/units/arena projections missing"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2166_0_gr_import", "use GR radial identity as MTS proof", "FORBIDDEN_GR_IMPORT", "BLOCKED", "EH fixed point not derived first", False),
        ("REF2166_1_generic_euler", "claim generic Euler difference gives C_R operator", "GENERIC_DIFFERENCE_TOO_WEAK", "BLOCKED", "selector/orientation missing", False),
        ("REF2166_2_hide_residuals", "drop R_local^MTS outside S_R", "RESIDUAL_MAP_REQUIRED", "BLOCKED", "every residual has an S_R slot", False),
        ("REF2166_3_nocharge_by_words", "set Q_R=0 by local-vacuum wording", "NO_CHARGE_THEOREM_UNSIGNED", "BLOCKED", "conservation leaves Q_R constant", False),
        ("REF2166_4_local_gr", "claim local GR/Newton now", "D_R_SR_QR_OPEN", "BLOCKED", "contract ready but not derived", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2166_0_contract", "The local-GR reduction theorem is now a precise contract, not a claim.", "C_R=0 follows only after parent D_R, S_R silence and Q_R no-charge close.", "use as proof checklist"),
        ("DEC2166_1_obstruction", "Generic Euler variation is insufficient.", "E_time-E_radial does not automatically select partial_r C_R.", "derive reciprocity selector/H_core kernel next"),
        ("DEC2166_2_residual_map", "R_local^MTS must enter S_R explicitly.", "Delta_Hsrc, I_X/J_X, constants, boundary/history, q_loc, reciprocal hair and readout all have slots.", "no residual hiding"),
        ("DEC2166_3_next", "Next checkpoint is reciprocity-selector operator or H_core source equation.", "this is the missing gear that could make D_R a real MTS equation rather than a closure benchmark.", "2167-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        ("NEXT2166_0_2167", "2167-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md", "scripts/Y5_R2FR_reciprocity_selector_operator_or_Hcore_source_equation_2167.py", "try to derive the parent reciprocity-selector orientation/kernel that makes the time/radial Euler combination select C_R; if unavailable, demote D_R to a closure-only benchmark and emit source-ready Z_R/J_R/S_R coefficient requirements", "selected", "parent-owned L_MTS_core/H_core yields the C_R operator without GR import, or all missing selector/source/operator inputs become explicit nonclaim rows"),
        ("NEXT2166_1_parallel_QR", "2167b-Y5-R2FR-reciprocal-no-charge-boundary-theorem-or-QR-source-row.md", "scripts/Y5_R2FR_reciprocal_no_charge_boundary_theorem_or_QR_source_row_2167b.py", "attempt Q_R=0 from boundary/source neutrality; if not, create finite Q_R/J_R source rows for PPN/orbital/lightcone comparison", "held", "Q_R no-charge theorem or finite sourced reciprocal-hair residual rows"),
        ("NEXT2166_2_parallel_q_loc", "2167c-Y5-R2FR-epsilon-GK-q-loc-to-SR-coefficient-map.md", "scripts/Y5_R2FR_epsilon_GK_qloc_to_SR_coefficient_map_2167c.py", "map epsilon_GK_q_loc into S_R with a declared coefficient/unit convention or prove the q_loc source slot vanishes", "held", "q_loc term is parent-zero or source-ready as an S_R component"),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(theorem: list[dict[str, object]], sr_map: list[dict[str, object]], prioritizer: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2166_0_source_weight_docs", BRANCH_COPIES["source_weight"], theorem + prioritizer),
        ("COPY2166_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], sr_map),
        ("COPY2166_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + prioritizer),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    sr_map: list[dict[str, object]],
    prioritizer: list[dict[str, object]],
    first_attack: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    theorem_ok = any(item["theorem_id"] == "LGT2166_6_verdict" and item["status"] == "LOCAL_GR_REDUCTION_CONTRACT_READY_NOT_DERIVED" for item in theorem)
    sr_ok = any(item["slot_id"] == "RSM2166_8_total" and item["current_status"] == "SYMBOLIC_READY_VALUES_MISSING" for item in sr_map)
    priority_ok = any(item["priority_id"] == "PR2166_0_reciprocity_selector" and item["selection"] == "SELECT_FIRST" for item in prioritizer)
    attack_ok = any(item["attack_id"] == "FAS2166_4_verdict" and item["status"] == "DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS" for item in first_attack)
    gate_ok = any(item["gate_id"] == "CG2166_0_contract_ready" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "CG2166_4_local_GR" and not truthy(item["gate_pass"]) for item in gates) and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2166_3_next" and "2167" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2166_0_2167" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False)) for group in (sources, theorem, sr_map, prioritizer, first_attack, gates, refusals, decisions, next_rows, copies) for item in group)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2166_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, theorem_ok, sr_ok, priority_ok, attack_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2166_00_sources", sources_ok, "2165 plus 1864/1865 source paths and needles validate"),
        ("VAL2166_01_theorem", theorem_ok, "local-GR theorem contract is ready but not derived"),
        ("VAL2166_02_sr_map", sr_ok, "R_local^MTS components all enter S_R slots"),
        ("VAL2166_03_prioritizer", priority_ok, "reciprocity selector/H_core target selected first"),
        ("VAL2166_04_first_attack", attack_ok, "generic Euler-difference obstruction is carried forward"),
        ("VAL2166_05_claim_gates", gate_ok, "contract can pass while D_R/local-GR claims remain blocked"),
        ("VAL2166_06_refusals", refusal_ok, "refusal runner blocks GR import, generic Euler shortcut, residual hiding, no-charge and local-GR claims"),
        ("VAL2166_07_decision", decisions_ok, "decision ledger selects 2167 reciprocity selector/H_core"),
        ("VAL2166_08_next", next_ok, "2167 next target selected"),
        ("VAL2166_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2166_10_csv_parse", csv_ok, "all generated 2166 CSVs parse cleanly"),
        ("VAL2166_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2166_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2166"),
        ("VAL2166_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2166_OVERALL", all_ok, "2166 builds the local-GR contract, maps R_local into S_R, and selects the reciprocity selector/H_core gate."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    sr_map: list[dict[str, object]],
    prioritizer: list[dict[str, object]],
    first_attack: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2165, _ = find_line(DOCS["2165"], ["NEXT2165_0_2166"])
    line_1864, _ = find_line(DOCS["1864"], ["LGT1864_6_verdict"])
    line_1865, _ = find_line(DOCS["1865"], ["DRA1865_6_verdict"])
    content = "\n\n".join(
        [
            "# 2166 - Y5/R2FR Local-GR Reduction Contract And Residual Vector Prioritizer",
            "## Current Verdict",
            "2166 does **not** derive local GR/Newton, does **not** derive `D_R[MTS]=partial_r C_R-S_R`, and does **not** prove `S_R=0` or `Q_R=0`.",
            "It does make the local-GR reduction contract sharp: `C_R=ln(T^2 S)=0` is the exact reciprocal target, and every live residual in `R_local^MTS` is forced into an `S_R` slot. Nothing can hide in fitted source normalization, readout, q_loc, boundary hair, or coupling language.",
            "The carried-forward obstruction is important: a generic parent Euler difference is too weak. The missing gear is a parent-owned reciprocity-selector orientation/kernel or explicit `L_MTS_core/H_core` whose Euler equation selects `C_R` without importing GR.",
            f"This follows the 2165 handoff at line {line_2165}, imports the 1864 local-GR contract at line {line_1864}, and carries the 1865 `D_R` obstruction at line {line_1865}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Local-GR Reduction Theorem",
            md_table(theorem, ["theorem_id", "object", "statement", "status", "consequence", "valid_for_claim"]),
            "## R_local To S_R Map",
            md_table(sr_map, ["slot_id", "sr_slot", "residual_symbol", "symbolic_entry", "current_status", "arena_links", "valid_for_claim"]),
            "## Proof Attack Prioritizer",
            md_table(prioritizer, ["priority_id", "target", "impact", "tractability", "dependency", "scrutiny_risk", "rationale", "selection", "valid_for_claim"]),
            "## First Attack Status",
            md_table(first_attack, ["attack_id", "target", "statement", "status", "consequence", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Refusal Runner",
            md_table(refusals, ["refusal_id", "attempted_claim", "input_status", "runner_result", "blocked_by", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This is the right kind of grim-but-good progress. We are not pretending the local GR branch is derived; we are specifying exactly what would derive it. The next proof is not 'more coupling hunting' in the fog. It is the reciprocity selector: find the parent operator or `H_core` that makes the time/radial equation difference select `C_R`. If that fails, the branch becomes a closure benchmark with explicit source-ready residual coefficients.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    theorem = theorem_rows()
    sr_map = sr_map_rows()
    prioritizer = prioritizer_rows()
    first_attack = first_attack_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["sr_map"], sr_map)
    write_csv(OUTPUTS["prioritizer"], prioritizer)
    write_csv(OUTPUTS["first_attack"], first_attack)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(theorem, sr_map, prioritizer, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, theorem, sr_map, prioritizer, first_attack, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, theorem, sr_map, prioritizer, first_attack, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2166 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
