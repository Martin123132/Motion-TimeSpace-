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


DOC = ROOT / "2165-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOCS = {
    "2164": ROOT / "2164-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-finite-vector-coefficients.md",
    "2164_validation": OUT / "P8_Y5_BRR545_2164_VALIDATION.csv",
    "2164_next": OUT / "P8_Y5_PARENT_QLOC_2164_NEXT_TARGET.csv",
    "1863": ROOT / "1863-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md",
    "1863_validation": OUT / "P8_Y5_BRR545_1863_VALIDATION.csv",
    "1864": ROOT / "1864-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md",
    "1864_validation": OUT / "P8_Y5_BRR545_1864_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2165_SOURCE_REGISTER.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_2165_PARENT_CURRENT_CONTRACT.csv",
    "sublemmas": OUT / "P8_Y5_PARENT_QLOC_2165_CURRENT_CHAIN_SUBLEMMA_STATUS.csv",
    "ix_jx": OUT / "P8_Y5_PARENT_QLOC_2165_IX_JX_DEMOTION_LEDGER.csv",
    "requirements": OUT / "P8_Y5_PARENT_QLOC_2165_FINITE_RESIDUAL_REQUIREMENTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2165_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2165_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2165_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2165_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2165_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2165_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_CURRENT_CHAIN_2165_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2165_IX_JX_VECTOR_NONCLAIM.csv",
    "queue": QUEUE / "JR2165_LOCAL_GR_CONTRACT_OR_RESIDUAL_PRIORITIZER_QUEUE.csv",
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


def formalization_has_2165_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2165-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2165*",
        "*P8_Y5_BRR545_2165*",
        "*Y5_R2FR_single_parent_current_chain_synthesis_or_Ix_Jx_demotion_2165*",
        "*AFRAME_PARENT_CURRENT_CHAIN_2165*",
        "*JR2165*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2165_00_2164_handoff", DOCS["2164"], [["NEXT2164_0_2165"], ["Y5B2164_5_verdict"], ["VAL2164_OVERALL"]], "2164 selects single-parent current chain or I_X/J_X demotion."),
        ("SRC2165_01_2164_validation", DOCS["2164_validation"], [["VAL2164_OVERALL"], ["PASS"]], "2164 validation passed as nonclaim."),
        ("SRC2165_02_2164_next_csv", DOCS["2164_next"], [["NEXT2164_0_2165"], ["I_X"], ["J_X"]], "machine-readable 2165 handoff."),
        ("SRC2165_03_1863_current_chain", DOCS["1863"], [["PCC1863_8_synthesis_verdict"], ["IJX1863_7_total_vector"], ["VAL1863_OVERALL"]], "prior current-chain synthesis fails and demotes I_X/J_X."),
        ("SRC2165_04_1863_validation", DOCS["1863_validation"], [["VAL1863_OVERALL"], ["PASS"]], "1863 validation passed as nonclaim."),
        ("SRC2165_05_1864_local_contract", DOCS["1864"], [["LGT1864_6_verdict"], ["RSM1864_2_J_X_qbarXT"], ["NEXT1864_0_primary"]], "local-GR reduction contract consumes R_local^MTS residual vector."),
        ("SRC2165_06_1864_validation", DOCS["1864_validation"], [["VAL1864_OVERALL"], ["PASS"]], "1864 validation passed as nonclaim."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def parent_contract_rows() -> list[dict[str, object]]:
    data = [
        ("PCC2165_0_L_parent", "one local parent action slice", "L_parent owns metric/local residual/source/readout slots before tests", "NOT_PARENT_SIGNED", "no single source for all currents"),
        ("PCC2165_1_Theta_total", "symplectic/current potential", "Theta_total yields Q_tau^MTS and Hamiltonian source charge", "NOT_PARENT_SIGNED", "charge/current owner still split across ledgers"),
        ("PCC2165_2_Qtau", "Q_tau^MTS", "same current produces Pi_M/tau_obs source-normalized mass", "PIM_QTAU_OWNER_NOT_SIGNED", "Delta_Hsrc cannot be zeroed"),
        ("PCC2165_3_projectability", "tau/projector/readout projectability", "Pi_M and tau commute with allowed current complex and readout happens after solution", "PROJECTABILITY_UNSIGNED", "I_projector/readout tails may re-enter"),
        ("PCC2165_4_boundary_reference", "boundary/reference subtraction", "boundary flux, reference terms and surface class are parent-owned", "BOUNDARY_REFERENCE_UNSIGNED", "I_boundary/I_ref remain residuals"),
        ("PCC2165_5_matter_descent", "ordinary matter descent", "S_matter descends through q(Phi) and cannot source X/Z directly", "MATTER_DESCENT_UNSIGNED", "J_X matter channel not zeroed"),
        ("PCC2165_6_X_source_silence", "X source silence", "J_X=0 or every component is finite-sourced with units and arena maps", "SOURCE_ZERO_NOT_PROVED", "dangerous X/local residual remains finite vector debt"),
        ("PCC2165_7_verdict", "single parent current chain", "PCC2165_0 through PCC2165_6 close in one parent branch", "SINGLE_PARENT_CURRENT_CHAIN_NOT_SIGNED", "demote I_X/J_X into finite nonclaim residual vector"),
    ]
    return [row(contract_id=contract_id, clause=clause, requirement=requirement, status=status, consequence=consequence) for contract_id, clause, requirement, status, consequence in data]


def sublemma_rows() -> list[dict[str, object]]:
    data = [
        ("SPC2165_0_same_action", "all currents descend from one action", "CONDITIONAL_SUBLEMMA_ONLY", "requires L_parent and variation order declaration", "BLOCKED"),
        ("SPC2165_1_integrability", "Hamiltonian source charge one-form is exact", "NOT_DERIVED", "curl_delta_H_tau/I_X ladder remains open", "BLOCKED"),
        ("SPC2165_2_chainmap", "Pi_M commutes with physical current differential", "CONDITIONAL_CHAINMAP_ONLY", "[d,Pi_M]J_H not parent-zeroed", "BLOCKED"),
        ("SPC2165_3_boundary", "boundary/reference terms are exact or zero-flux", "NOT_DERIVED", "surface/reference owner missing", "BLOCKED"),
        ("SPC2165_4_readout_order", "readout cannot re-enter source", "PURE_READOUT_SAFE_NOT_GENERAL", "calibration/source-worldtube feedback can feed J_X", "BLOCKED"),
        ("SPC2165_5_verdict", "all current-chain sublemmas close", "FAIL_CURRENT_CLAIM", "conditional pieces do not close together", "BLOCKED"),
    ]
    return [row(sublemma_id=sublemma_id, target=target, status=status, missing=mising, gate=gate) for sublemma_id, target, status, mising, gate in data]


def ix_jx_rows() -> list[dict[str, object]]:
    data = [
        ("IJX2165_0_I_X", "I_X", "first non-EH curl/source component in delta_H_tau/current integrability", "|I_X|/M_H_ref retained inside absolute Delta_integrability envelope", "NOT_THEOREM_ZERO", "MISSING_PARENT_CURRENT_OWNER;MISSING_X_SOURCE_SILENCE;MISSING_PROJECTOR_BOUNDARY_DQ_LOCK", "orbital;PPN;local_GR;source_normalization"),
        ("IJX2165_1_J_X", "J_X", "ordinary/hidden source current for dangerous X/local residual direction", "|J_X| <= |J_matter|+|J_chiD_wall|+|J_boundary|+|J_readout|+|J_history|+|Pi_M_projection_tail|", "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING", "MISSING_CHANNEL_ZERO_OR_COMPONENT_BOUNDS", "R10;WEP;clock;PPN;orbital"),
        ("IJX2165_2_qbarXT", "qbar_XT", "test-body/source charge overlap with X route", "finite source/test charge row required if J_X not zero", "NOT_ZERO_NOT_SOURCED", "MISSING_QBAR_COMPONENTS", "R10;WEP;clock;PPN"),
        ("IJX2165_3_boundary_history", "boundary/history tails", "edge/history/support contributions to J_X and I_X", "absolute no-cancellation tail envelope", "TAILS_NOT_ZERO_NOT_BOUNDED", "MISSING_BOUNDARY_HISTORY_ROWS", "orbital;R10;local_GR"),
        ("IJX2165_4_total_vector", "R_local^MTS", "minimal local residual vector after demotion", "(Delta_Hsrc,I_X,J_X,qbar_XT,b_alpha/b_mA/b_clock,boundary/history,epsilon_GK_q_loc,q_R/S_R)", "FINITE_NONCLAIM_VECTOR_REQUIRED", "MISSING_COMMON_UNITS;MISSING_ARENA_PROJECTIONS;MISSING_NUMERIC_COMPONENT_BOUNDS", "R10;WEP;PPN;clock;orbital;local_GR"),
    ]
    return [row(demotion_id=demotion_id, symbol=symbol, role=role, envelope=envelope, status=status, missing_inputs=missing_inputs, arenas=arenas) for demotion_id, symbol, role, envelope, status, missing_inputs, arenas in data]


def requirements_rows() -> list[dict[str, object]]:
    data = [
        ("FRR2165_0_common_units", "shared projected units", "Delta_Hsrc;I_X;J_X;qbar_XT;epsilon_GK_q_loc;q_R/S_R", "MISSING_COMMON_UNITS", "declare dimensionless normalization or source-charge units for each component"),
        ("FRR2165_1_arena_projection", "arena maps", "R10;WEP;PPN;clock;orbital;local_GR", "MISSING_ARENA_PROJECTIONS", "map each residual into the observables before scoring"),
        ("FRR2165_2_numeric_bounds", "numeric component bounds", "finite rows with source paths and uncertainties", "MISSING_NUMERIC_COMPONENT_BOUNDS", "no claim until real values replace templates"),
        ("FRR2165_3_no_cancellation", "absolute no-cancellation policy", "sum absolute component envelopes unless a theorem identifies one common vanishing current", "POLICY_ACTIVE", "opposite-sign hidden couplings do not count as derivation"),
        ("FRR2165_4_local_GR_slot", "S_R residual slot", "R_local^MTS must enter the parent Euler difference source side", "REQUIRED_FOR_NEXT_CONTRACT", "no residual can be dropped from local reciprocity proof"),
    ]
    return [row(requirement_id=requirement_id, target=target, applies_to=applies_to, status=status, next_action=next_action) for requirement_id, target, applies_to, status, next_action in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2165_0_contract_precise", "single-parent current contract is precise enough to audit", True, "required clauses are explicit"),
        ("CG2165_1_contract_signed", "single-parent current chain is signed in current corpus", False, "multiple parent signatures missing"),
        ("CG2165_2_IX_JX_zero", "I_X and J_X vanish on local branch", False, "source-zero and parent-current owner not proved"),
        ("CG2165_3_finite_vector_ready", "R_local^MTS finite vector is score-ready", False, "units/projections/numeric bounds missing"),
        ("CG2165_4_local_GR", "local GR/Newton reduction is derived", False, "R_local^MTS must enter D_R/S_R contract and be zeroed/bounded"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2165_0_current_chain_claim", "claim single-parent chain closure", "SIGNATURES_MISSING", "BLOCKED", "PCC2165_7 rejects closure", False),
        ("REF2165_1_ix_zero", "claim I_X=0", "PARENT_CURRENT_OWNER_MISSING", "BLOCKED", "integrability/current chain not signed", False),
        ("REF2165_2_jx_zero", "claim J_X=0", "SOURCE_SILENCE_MISSING", "BLOCKED", "matter/readout/boundary/history channels open", False),
        ("REF2165_3_score_vector", "score R_local^MTS now", "VALUES_UNITS_PROJECTIONS_MISSING", "BLOCKED", "finite vector is a ledger, not data yet", False),
        ("REF2165_4_local_gr", "claim local GR/Newton", "D_R_SR_CONTRACT_NOT_DERIVED", "BLOCKED", "local reduction contract needs R_local^MTS source map", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2165_0_contract", "The single-parent current chain is precise but unsigned.", "conditional sublemmas are real but not united by one parent action.", "do not claim I_X/J_X zero"),
        ("DEC2165_1_demotion", "I_X/J_X are demoted into R_local^MTS finite nonclaim vector.", "this preserves testability and prevents source-normalization closure-smuggling.", "carry the vector into the local-GR D_R/S_R contract"),
        ("DEC2165_2_priority", "Next priority is the local-GR reduction contract and residual-vector prioritizer.", "once R_local^MTS is explicit, the next proof attack is D_R normal form and S_R decomposition.", "2166-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        ("NEXT2165_0_2166", "2166-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md", "scripts/Y5_R2FR_local_GR_reduction_contract_and_residual_vector_prioritizer_2166.py", "convert the parent-current contract and R_local^MTS residual vector into a minimal local-GR reduction theorem checklist, then prioritize the first derivation target: parent Euler bridge, matter/constants/source-current exclusion, Gamma/Khat action pair, or boundary/source-measure closure", "selected", "either a signed parent clause closes a residual channel, or the residual channel is converted into a source-ready finite nonclaim row with units and arena projections"),
        ("NEXT2165_1_parallel", "2166b-Y5-R2FR-no-extra-F2-no-mass-source-vertex-signature.md", "scripts/Y5_R2FR_no_extra_F2_no_mass_source_vertex_signature_2166b.py", "try to forbid independent EM kinetic, mass, binding and source-only vertices from the parent action", "held", "no-extra-F2/no-mass/no-source-weight theorem-zero or finite coefficient rows"),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(contract: list[dict[str, object]], ix_jx: list[dict[str, object]], requirements: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2165_0_source_weight_docs", BRANCH_COPIES["source_weight"], contract),
        ("COPY2165_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], ix_jx + requirements),
        ("COPY2165_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + requirements),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    sublemmas: list[dict[str, object]],
    ix_jx: list[dict[str, object]],
    requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    contract_ok = any(item["contract_id"] == "PCC2165_7_verdict" and item["status"] == "SINGLE_PARENT_CURRENT_CHAIN_NOT_SIGNED" for item in contract)
    sublemma_ok = any(item["sublemma_id"] == "SPC2165_5_verdict" and item["status"] == "FAIL_CURRENT_CLAIM" for item in sublemmas)
    ix_ok = any(item["demotion_id"] == "IJX2165_4_total_vector" and item["status"] == "FINITE_NONCLAIM_VECTOR_REQUIRED" for item in ix_jx)
    req_ok = any(item["requirement_id"] == "FRR2165_4_local_GR_slot" and item["status"] == "REQUIRED_FOR_NEXT_CONTRACT" for item in requirements)
    gate_ok = any(item["gate_id"] == "CG2165_0_contract_precise" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "CG2165_4_local_GR" and not truthy(item["gate_pass"]) for item in gates) and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2165_2_priority" and "2166" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2165_0_2166" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False)) for group in (sources, contract, sublemmas, ix_jx, requirements, gates, refusals, decisions, next_rows, copies) for item in group)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2165_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, contract_ok, sublemma_ok, ix_ok, req_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2165_00_sources", sources_ok, "2164 plus 1863/1864 source paths and needles validate"),
        ("VAL2165_01_contract", contract_ok, "single-parent current contract remains unsigned"),
        ("VAL2165_02_sublemmas", sublemma_ok, "conditional sublemmas do not close together"),
        ("VAL2165_03_ix_jx", ix_ok, "I_X/J_X are demoted to finite nonclaim residual vector"),
        ("VAL2165_04_requirements", req_ok, "finite residual requirements include the local-GR S_R slot"),
        ("VAL2165_05_claim_gates", gate_ok, "contract precision passes while local/current claims remain blocked"),
        ("VAL2165_06_refusals", refusal_ok, "refusal runner blocks current-chain, I_X/J_X, vector-score and local-GR claims"),
        ("VAL2165_07_decision", decisions_ok, "decision ledger selects 2166 local-GR contract"),
        ("VAL2165_08_next", next_ok, "2166 next target selected"),
        ("VAL2165_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2165_10_csv_parse", csv_ok, "all generated 2165 CSVs parse cleanly"),
        ("VAL2165_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2165_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2165"),
        ("VAL2165_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2165_OVERALL", all_ok, "2165 rejects single-parent current closure and demotes I_X/J_X into R_local^MTS for the local-GR contract."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    sublemmas: list[dict[str, object]],
    ix_jx: list[dict[str, object]],
    requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2164, _ = find_line(DOCS["2164"], ["NEXT2164_0_2165"])
    line_1863, _ = find_line(DOCS["1863"], ["PCC1863_8_synthesis_verdict"])
    line_1864, _ = find_line(DOCS["1864"], ["LGT1864_6_verdict"])
    content = "\n\n".join(
        [
            "# 2165 - Y5/R2FR Single Parent Current Chain Synthesis Or I_X/J_X Demotion",
            "## Current Verdict",
            "2165 does **not** sign the single-parent current chain, does **not** prove `I_X=0` or `J_X=0`, and does **not** reopen local GR/Newton inheritance.",
            "It does make the useful demotion precise: `I_X/J_X` are no longer vague coupling worries; they are explicit finite nonclaim components of `R_local^MTS`, which must enter the next local-GR `D_R/S_R` reduction contract.",
            f"This follows the 2164 handoff at line {line_2164}, imports the 1863 current-chain verdict at line {line_1863}, and routes the demoted residual vector into the 1864 local-GR contract at line {line_1864}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Parent Current Contract",
            md_table(contract, ["contract_id", "clause", "requirement", "status", "consequence", "valid_for_claim"]),
            "## Current-Chain Sublemma Status",
            md_table(sublemmas, ["sublemma_id", "target", "status", "missing", "gate", "valid_for_claim"]),
            "## I_X/J_X Demotion Ledger",
            md_table(ix_jx, ["demotion_id", "symbol", "role", "envelope", "status", "missing_inputs", "arenas", "valid_for_claim"]),
            "## Finite Residual Requirements",
            md_table(requirements, ["requirement_id", "target", "applies_to", "status", "next_action", "valid_for_claim"]),
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
            "The current-chain route did not close, but this is not wheel-spinning. We now have a precise residual vector that can be inserted into the local-GR reduction theorem. The next best move is to build the `D_R[MTS]=partial_r C_R-S_R` contract and force every residual into an `S_R` slot, so no coupling can hide in source normalization or readout.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    contract = parent_contract_rows()
    sublemmas = sublemma_rows()
    ix_jx = ix_jx_rows()
    requirements = requirements_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_contract"], contract)
    write_csv(OUTPUTS["sublemmas"], sublemmas)
    write_csv(OUTPUTS["ix_jx"], ix_jx)
    write_csv(OUTPUTS["requirements"], requirements)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(contract, ix_jx, requirements, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, contract, sublemmas, ix_jx, requirements, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, contract, sublemmas, ix_jx, requirements, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2165 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
