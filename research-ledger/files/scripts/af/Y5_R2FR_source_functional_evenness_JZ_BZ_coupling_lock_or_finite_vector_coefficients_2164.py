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


DOC = ROOT / "2164-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-finite-vector-coefficients.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOCS = {
    "2163": ROOT / "2163-Y5-R2FR-motion-load-phase-volume-parent-origin-or-finite-vector-backstop.md",
    "2163_validation": OUT / "P8_Y5_BRR545_2163_VALIDATION.csv",
    "2163_next": OUT / "P8_Y5_PARENT_QLOC_2163_NEXT_TARGET.csv",
    "1861": ROOT / "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md",
    "1861_validation": OUT / "P8_Y5_BRR545_1861_VALIDATION.csv",
    "1862": ROOT / "1862-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
    "1862_validation": OUT / "P8_Y5_BRR545_1862_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2164_SOURCE_REGISTER.csv",
    "evenness": OUT / "P8_Y5_PARENT_QLOC_2164_EVENNESS_THEOREM_AUDIT.csv",
    "coupling": OUT / "P8_Y5_PARENT_QLOC_2164_JZ_BZ_COUPLING_LOCK_AUDIT.csv",
    "finite": OUT / "P8_Y5_PARENT_QLOC_2164_FINITE_VECTOR_COEFFICIENTS.csv",
    "y5_bridge": OUT / "P8_Y5_PARENT_QLOC_2164_Y5_PIM_DELTASRC_BRIDGE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2164_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2164_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2164_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2164_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2164_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2164_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_JZ_BZ_COUPLING_LOCK_2164_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2164_FINITE_VECTOR_NONCLAIM.csv",
    "queue": QUEUE / "JR2164_CURRENT_CHAIN_OR_FINITE_IX_JX_QUEUE.csv",
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


def formalization_has_2164_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2164-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2164*",
        "*P8_Y5_BRR545_2164*",
        "*Y5_R2FR_source_functional_evenness_JZ_BZ_coupling_lock_or_finite_vector_coefficients_2164*",
        "*AFRAME_JZ_BZ_COUPLING_LOCK_2164*",
        "*JR2164*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2164_00_2163_handoff", DOCS["2163"], [["NEXT2163_0_2164"], ["QBS2163_6_verdict"], ["VAL2163_OVERALL"]], "2163 selects J_Z/B_Z coupling lock or finite coefficient rows."),
        ("SRC2164_01_2163_validation", DOCS["2163_validation"], [["VAL2163_OVERALL"], ["PASS"]], "2163 validation passed as nonclaim."),
        ("SRC2164_02_2163_next_csv", DOCS["2163_next"], [["NEXT2163_0_2164"], ["J_Z", "local residual Z"], ["finite coefficient", "finite residual"]], "machine-readable 2164 handoff."),
        ("SRC2164_03_1861_evenness", DOCS["1861"], [["SFE1861_6_verdict"], ["JBC1861_5_acceptance"], ["VAL1861_OVERALL"]], "prior evenness/coupling lock audit: conditional theorem exact, current activation failed."),
        ("SRC2164_04_1861_validation", DOCS["1861_validation"], [["VAL1861_OVERALL"], ["PASS"]], "1861 validation passed as nonclaim."),
        ("SRC2164_05_1862_y5", DOCS["1862"], [["SMC1862_5_verdict"], ["DHS1862_3_I_X"], ["NEXT1862_0_primary"]], "Y5 source-normalization chain narrowed to Pi_M/Delta_Hsrc/I_X/J_X."),
        ("SRC2164_06_1862_validation", DOCS["1862_validation"], [["VAL1862_OVERALL"], ["PASS"]], "1862 validation passed as nonclaim."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def evenness_rows() -> list[dict[str, object]]:
    data = [
        ("SFE2164_0_setup", "local residual doublet", "Z is the local residual/response coordinate whose odd linear couplings source q_loc", "SETUP", "defines what must be even or quotient-descended"),
        ("SFE2164_1_bulk_theorem", "bulk source functional", "S_bulk[Z,psi,eta_even]=S_bulk[-Z,psi,eta_even] => J_Z=dS/dZ|_0=0", "EXACT_CONDITIONAL_THEOREM", "kills bulk linear source only inside the exchange-even class"),
        ("SFE2164_2_boundary_theorem", "boundary/linking functional", "B[Z,eta_even]=B[-Z,eta_even] or exact/no-flux descent => B_Z=0", "EXACT_CONDITIONAL_THEOREM", "kills boundary leakage only if local boundary data are even or descended"),
        ("SFE2164_3_quotient_descent", "matter/readout descent", "S_matter=Sbar[q(Phi),Psi,theta] and Dq(v_Z)=0 => observed matter cannot source Z", "EXACT_CONDITIONAL_ROUTE", "stronger than parity, but q/readout ownership remains unsigned"),
        ("SFE2164_4_readout_species", "readout/species labels", "species, clocks, coframes, markers and calibration maps must be eta-even or quotient variables", "NOT_PARENT_SIGNED", "odd material/readout labels can reintroduce J_Z"),
        ("SFE2164_5_Y5_Y6", "Y5/Y6 hard channels", "source-normalization Y5 and extra-stress Y6 are not killed by parity wording alone", "HARD_BLOCKS_RETAINED", "need Pi_M/current-chain and Y6 stress gates"),
        ("SFE2164_6_verdict", "current MTS source-functional evenness", "SFE2164_1 through SFE2164_5 all parent-close in one branch", "EVENNESS_THEOREM_NOT_ACTIVATED", "formal q_loc double-zero remains conditional only"),
    ]
    return [row(theorem_id=theorem_id, object=object_name, statement=statement, status=status, consequence=consequence) for theorem_id, object_name, statement, status, consequence in data]


def coupling_lock_rows() -> list[dict[str, object]]:
    data = [
        ("JBC2164_0_bulk_JZ", "bulk source current", "J_Z^A", "MISSING_ZERO_THEOREM_OR_VALUE", "prove exchange-even/descended source functional or source finite component rows"),
        ("JBC2164_1_boundary_BZ", "boundary/linking flux current", "B_Z^A", "MISSING_BOUNDARY_ZERO_OR_BOUND", "prove no-flux/exact boundary theorem or source boundary coefficient rows"),
        ("JBC2164_2_readout_species", "readout/species/material dependence", "J_Z[readout/species]", "MISSING_READOUT_SPECIES_MAP", "prove readout descends after quotient or retain finite species/readout rows"),
        ("JBC2164_3_Y5_source_normalization", "observed-GM/source normalization", "Delta_Hsrc, Delta_integrability, I_X/J_X", "HARD_BLOCK_PIM_CURRENT_CHAIN", "single-parent current chain must own Pi_M/tau/source charge or finite I_X/J_X rows"),
        ("JBC2164_4_Y6_extra_stress", "extra stress/Bianchi tail", "J_Z[Y6], Delta_K[Y6]", "HARD_BLOCK_STRESS_PROJECTOR", "prove topological/projector-null/pure-improvement theorem or source finite stress rows"),
        ("JBC2164_5_q_loc_activation", "physical q_loc double-zero", "F1=0 becomes physical only if all coupling legs are zero/bounded", "BLOCKED_BY_COUPLING_LOCK", "formal normal form cannot be promoted yet"),
        ("JBC2164_6_acceptance", "complete coupling lock", "J_total=(J_Z,B_Z,J_Y5,J_Y6,J_readout)", "REJECT_COUPLING_LOCK_NOT_CLOSED", "select parent-current I_X/J_X synthesis as next primary target"),
    ]
    return [row(lock_id=lock_id, channel=channel, symbol=symbol, status=status, next_action=next_action) for lock_id, channel, symbol, status, next_action in data]


def finite_coeff_rows() -> list[dict[str, object]]:
    data = [
        ("FVC2164_0_epsilon_q_loc", "epsilon_GK_q_loc", "norm of projected Gamma/Khat residual", "q_loc_units_or_arena_normalized", "local_GR;PPN;clock;orbital;R10", "MISSING_SOURCE_VALUE", False),
        ("FVC2164_1_DeltaGamma", "DeltaGamma_source_connection", "connection/source-current leakage", "connection_or_acceleration_projection_units", "WEP;clock;lightcone;PPN_gamma;local_GR", "MISSING_SOURCE_VALUE", False),
        ("FVC2164_2_JZ", "J_Z^A", "bulk source-current component vector", "action_density_per_Z_component", "R10;PPN;clock;orbital;WEP", "TEMPLATE_ONLY_NONCLAIM", False),
        ("FVC2164_3_BZ", "B_Z^A", "boundary/linking flux component vector", "boundary_action_or_flux_per_Z_component", "R10;PPN;orbital;source-normalization", "TEMPLATE_ONLY_NONCLAIM", False),
        ("FVC2164_4_Y5", "Delta_Hsrc/I_X/J_X", "source-normalization current-chain residuals", "common_MHref_normalized_absolute_components", "Newton;PPN;R10;clock;orbital", "HARD_BLOCK_NONCLAIM", False),
        ("FVC2164_5_Y6", "J_Z[Y6]/Delta_K[Y6]", "extra-stress/projector residuals", "stress_density_or_arena_projection_units", "local_GR;PPN;clock;orbital;WEP", "HARD_BLOCK_NONCLAIM", False),
        ("FVC2164_6_QR_SR", "Q_R/S_R", "radial no-charge and Euler-source side residuals", "C_R_gradient_or_source_side_units", "local_GR;orbital;lab_finite_source", "MISSING_SOURCE_BOUND", False),
        ("FVC2164_7_total", "finite residual vector", "|epsilon_q_loc|+|DeltaGamma|+|JZ|+|BZ|+|Y5|+|Y6|+|QR/SR|", "declared_common_arena_units", "R10;PPN;clock;orbital;WEP;local_GR", "VALUES_MISSING_NONCLAIM", False),
    ]
    return [row(coeff_id=coeff_id, symbol=symbol, definition=definition, units=units, arena_maps=arena_maps, status=status, valid_for_claim=valid_for_claim) for coeff_id, symbol, definition, units, arena_maps, status, valid_for_claim in data]


def y5_bridge_rows() -> list[dict[str, object]]:
    data = [
        ("Y5B2164_0_selection", "Y5 source-normalization route", "post-1861 coupling lock selects Pi_M/source-charge ownership as primary", "SELECTED_NOT_CLOSED", "Y5 is a coupling lock, not a fitted GM nuisance"),
        ("Y5B2164_1_PiM_tau", "Pi_M/tau_obs owner", "observed source charge must be selected before orbital/source readout", "PIM_OBSERVED_TIME_NOT_PARENT_OWNED", "cannot hide residuals inside measured GM"),
        ("Y5B2164_2_Delta_Hsrc", "Delta_Hsrc", "G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress]", "CENTRAL_Y5_RESIDUAL_RETAINED", "all source-measure failure is now explicit"),
        ("Y5B2164_3_Delta_integrability", "Delta_integrability ladder", "delta_H_tau, Delta_ref, B_zero_flux, Delta_symp, tau_MHref_lock", "ZERO_PROOF_NOT_CLOSED", "subcomponents require theorem-zero or finite rows"),
        ("Y5B2164_4_IX_JX", "I_X/J_X first live lock", "|int_S i_tau omega_X + int_A C_X + boundary_X|/M_H_ref plus J_X source silence", "FIRST_NON_EH_CURL_TARGET", "next work should synthesize current chain or demote I_X/J_X to finite rows"),
        ("Y5B2164_5_verdict", "Y5 coupling-lock status", "source-normalized Newton/local GR cannot reopen until parent current chain or finite coefficients exist", "Y5_SOURCE_OWNER_NOT_PROVED", "select 2165 parent-current synthesis/I_X-J_X demotion"),
    ]
    return [row(y5_id=y5_id, object=object_name, formula_or_role=formula_or_role, status=status, consequence=consequence) for y5_id, object_name, formula_or_role, status, consequence in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2164_0_conditional_evenness", "exchange-even/quotient-descended functionals imply J_Z/B_Z=0", True, "the theorem is exact under its premises"),
        ("CG2164_1_current_evenness", "current MTS proves all observed source/readout/boundary functionals are even or descended", False, "coframe/source/species/readout/boundary/Y5/Y6 clauses unsigned"),
        ("CG2164_2_JZ_BZ_zero", "all J_Z/B_Z physical terms vanish", False, "bulk, boundary, readout/species, Y5 and Y6 channels remain active"),
        ("CG2164_3_q_loc_zero", "formal q_loc double-zero is physically activated", False, "coupling lock open"),
        ("CG2164_4_Y5_source_owner", "Pi_M/Y5 source charge is parent-owned", False, "Delta_Hsrc/I_X/J_X ladder remains open"),
        ("CG2164_5_finite_coefficients_ready", "finite vector coefficients are sourced and arena-mapped", False, "rows are templates/nonclaim acquisition targets"),
        ("CG2164_6_local_GR", "local GR/Newton inheritance is reopened", False, "q_loc, Y5, Y6, readout, boundary and parent Euler gates not jointly closed"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2164_0_formal_evenness", "promote conditional evenness to physical q_loc=0", "PREMISES_UNSIGNED", "BLOCKED", "observed source/readout/boundary functionals not parent-signed", False),
        ("REF2164_1_ignore_Y5", "ignore source-normalization coupling", "Y5_HARD_BLOCK", "BLOCKED", "Delta_Hsrc/I_X/J_X remain central residuals", False),
        ("REF2164_2_ignore_Y6", "ignore extra-stress channel", "Y6_STRESS_BLOCK", "BLOCKED", "conservation does not automatically make stress projector-null", False),
        ("REF2164_3_claim_finite_rows", "score finite vector rows now", "MISSING_VALUES_UNITS_SOURCES", "BLOCKED", "all coefficient rows are nonclaim templates", False),
        ("REF2164_4_local_GR_claim", "claim derived local GR/Newton", "COUPLING_LOCK_OPEN", "BLOCKED", "q_loc/Y5/Y6/readout/boundary not jointly zeroed or bounded", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2164_0_theorem", "Keep exchange-evenness as an exact conditional theorem, not a current claim.", "the source/readout/boundary/Y5/Y6 premises are not parent-signed.", "do not promote q_loc=0 from formal double-zero alone"),
        ("DEC2164_1_coupling_status", "The coupling lock remains the active bottleneck.", "linear source, boundary, readout, Y5 and Y6 leakage can reactivate q_loc.", "retain epsilon_GK_q_loc and finite vector rows"),
        ("DEC2164_2_Y5_priority", "The highest-leverage next target is the Y5 parent-current chain.", "1862 has already narrowed broad GM/source issues to Delta_Hsrc and I_X/J_X.", "construct one parent current chain or demote I_X/J_X to finite rows"),
        ("DEC2164_3_next", "Next checkpoint is single-parent current-chain synthesis or I_X/J_X demotion.", "that is the shortest honest route from coupling lock to source-normalized Newton/local GR.", "2165-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2164_0_2165",
            "2165-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md",
            "scripts/Y5_R2FR_single_parent_current_chain_synthesis_or_Ix_Jx_demotion_2165.py",
            "try to construct one parent current chain owning L_parent, Theta_total, Q_tau^MTS, tau/projectability, boundary/reference, matter descent and X source silence; if not, explicitly demote I_X/J_X to finite nonclaim rows",
            "selected",
            "parent current chain closes and I_X/J_X vanish, or strict finite residual rows are emitted with units/source requirements and no claim",
        ),
        (
            "NEXT2164_1_parallel_Y6",
            "2165b-Y5-R2FR-Y6-topological-projector-null-stress-gate.md",
            "scripts/Y5_R2FR_Y6_topological_projector_null_stress_gate_2165b.py",
            "test whether Y6 extra/projector stress is topological, projector-null, pure improvement, or finite residual with PPN/source-stress projections",
            "held",
            "Y6 stress-zero theorem or source-backed finite PPN/source-stress rows",
        ),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(evenness: list[dict[str, object]], coupling: list[dict[str, object]], finite: list[dict[str, object]], y5_bridge: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2164_0_source_weight_docs", BRANCH_COPIES["source_weight"], evenness + coupling),
        ("COPY2164_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], finite + y5_bridge),
        ("COPY2164_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + finite),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    evenness: list[dict[str, object]],
    coupling: list[dict[str, object]],
    finite: list[dict[str, object]],
    y5_bridge: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    evenness_ok = any(item["theorem_id"] == "SFE2164_6_verdict" and item["status"] == "EVENNESS_THEOREM_NOT_ACTIVATED" for item in evenness)
    coupling_ok = any(item["lock_id"] == "JBC2164_6_acceptance" and item["status"] == "REJECT_COUPLING_LOCK_NOT_CLOSED" for item in coupling)
    finite_ok = any(item["coeff_id"] == "FVC2164_7_total" and item["status"] == "VALUES_MISSING_NONCLAIM" for item in finite) and all(not truthy(item.get("valid_for_claim", False)) for item in finite)
    y5_ok = any(item["y5_id"] == "Y5B2164_5_verdict" and item["status"] == "Y5_SOURCE_OWNER_NOT_PROVED" for item in y5_bridge)
    gate_ok = any(item["gate_id"] == "CG2164_0_conditional_evenness" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "CG2164_6_local_GR" and not truthy(item["gate_pass"]) for item in gates) and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2164_3_next" and "2165" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2164_0_2165" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False)) for group in (sources, evenness, coupling, finite, y5_bridge, gates, refusals, decisions, next_rows, copies) for item in group)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2164_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, evenness_ok, coupling_ok, finite_ok, y5_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2164_00_sources", sources_ok, "2163 plus 1861/1862 source paths and needles validate"),
        ("VAL2164_01_evenness", evenness_ok, "conditional evenness theorem recorded but not activated"),
        ("VAL2164_02_coupling", coupling_ok, "J_Z/B_Z/Y5/Y6 coupling lock remains rejected"),
        ("VAL2164_03_finite", finite_ok, "finite coefficient rows are staged as nonclaim values-missing rows"),
        ("VAL2164_04_y5", y5_ok, "Y5 bridge keeps Delta_Hsrc/I_X/J_X unresolved"),
        ("VAL2164_05_claim_gates", gate_ok, "conditional theorem can pass while q_loc/local-GR claims remain blocked"),
        ("VAL2164_06_refusals", refusal_ok, "refusal runner blocks formal-evenness, Y5/Y6 ignoring, finite-row and local-GR claims"),
        ("VAL2164_07_decision", decisions_ok, "decision ledger selects 2165 current-chain/I_X-J_X target"),
        ("VAL2164_08_next", next_ok, "2165 next target selected"),
        ("VAL2164_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2164_10_csv_parse", csv_ok, "all generated 2164 CSVs parse cleanly"),
        ("VAL2164_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2164_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2164"),
        ("VAL2164_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2164_OVERALL", all_ok, "2164 keeps evenness as conditional, rejects current coupling lock, and selects Y5 current-chain/I_X-J_X demotion."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    evenness: list[dict[str, object]],
    coupling: list[dict[str, object]],
    finite: list[dict[str, object]],
    y5_bridge: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2163, _ = find_line(DOCS["2163"], ["NEXT2163_0_2164"])
    line_1861, _ = find_line(DOCS["1861"], ["SFE1861_6_verdict"])
    line_1862, _ = find_line(DOCS["1862"], ["SMC1862_5_verdict"])
    content = "\n\n".join(
        [
            "# 2164 - Y5/R2FR Source-Functional Evenness, J_Z/B_Z Coupling Lock, Or Finite Vector Coefficients",
            "## Current Verdict",
            "2164 does **not** prove the physical `q_loc` double-zero, does **not** close the coupling lock, and does **not** reopen local GR/Newton inheritance.",
            "It does prove the useful conditional rule: if source, boundary, matter and readout functionals are exchange-even in the local residual `Z`, or quotient-descended before matter readout, their linear `J_Z/B_Z` couplings vanish at `Z=0`. Current MTS has not parent-signed those premises, especially the Y5 source-normalization and Y6 extra-stress channels.",
            "The coupling problem is now concrete: solve the single-parent current chain behind `Pi_M/Delta_Hsrc/I_X/J_X`, or demote those terms into finite residual coefficients with units, sources and arena maps.",
            f"This follows the 2163 handoff at line {line_2163}, imports the 1861 evenness verdict at line {line_1861}, and uses the 1862 Y5/Pi_M bridge at line {line_1862}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Evenness Theorem Audit",
            md_table(evenness, ["theorem_id", "object", "statement", "status", "consequence", "valid_for_claim"]),
            "## J_Z/B_Z Coupling Lock Audit",
            md_table(coupling, ["lock_id", "channel", "symbol", "status", "next_action", "valid_for_claim"]),
            "## Finite Vector Coefficients",
            md_table(finite, ["coeff_id", "symbol", "definition", "units", "arena_maps", "status", "valid_for_claim"]),
            "## Y5 Pi_M / Delta_Hsrc Bridge",
            md_table(y5_bridge, ["y5_id", "object", "formula_or_role", "status", "consequence", "valid_for_claim"]),
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
            "The coupling hunch was right, but in a disciplined way. We have an exact conditional symmetry/descent theorem, not a physical zero yet. The strongest next route is not to repeat the symmetry statement; it is to build one parent current chain that owns the observed source charge and kills or bounds `I_X/J_X`. If that chain fails, the finite residual vector becomes the honest empirical branch.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    evenness = evenness_rows()
    coupling = coupling_lock_rows()
    finite = finite_coeff_rows()
    y5_bridge = y5_bridge_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["evenness"], evenness)
    write_csv(OUTPUTS["coupling"], coupling)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["y5_bridge"], y5_bridge)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(evenness, coupling, finite, y5_bridge, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, evenness, coupling, finite, y5_bridge, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, evenness, coupling, finite, y5_bridge, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2164 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
