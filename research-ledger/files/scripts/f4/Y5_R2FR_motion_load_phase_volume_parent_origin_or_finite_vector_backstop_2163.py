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


DOC = ROOT / "2163-Y5-R2FR-motion-load-phase-volume-parent-origin-or-finite-vector-backstop.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2162": ROOT / "2162-Y5-R2FR-minimal-parent-X-sector-action-clause-or-PPN-vector-fill.md",
    "2162_validation": OUT / "P8_Y5_BRR545_2162_VALIDATION.csv",
    "2162_next": OUT / "P8_Y5_PARENT_QLOC_2162_NEXT_TARGET.csv",
    "1859": ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
    "1859_validation": OUT / "P8_Y5_BRR545_1859_VALIDATION.csv",
    "1860": ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
    "1860_validation": OUT / "P8_Y5_BRR545_1860_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2163_SOURCE_REGISTER.csv",
    "motion_origin": OUT / "P8_Y5_PARENT_QLOC_2163_MOTION_LOAD_ORIGIN_AUDIT.csv",
    "euler_route": OUT / "P8_Y5_PARENT_QLOC_2163_EULER_DIFFERENCE_ROUTE.csv",
    "qloc_bridge": OUT / "P8_Y5_PARENT_QLOC_2163_QLOC_BRIDGE_STATUS.csv",
    "finite_vector": OUT / "P8_Y5_PARENT_QLOC_2163_FINITE_VECTOR_BACKSTOP.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2163_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2163_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2163_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2163_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2163_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2163_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_MOTION_LOAD_QLOC_2163_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2163_QLOC_VECTOR_NONCLAIM.csv",
    "queue": QUEUE / "JR2163_QLOC_COUPLING_OR_VECTOR_BACKSTOP_QUEUE.csv",
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


def formalization_has_2163_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2163-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2163*",
        "*P8_Y5_BRR545_2163*",
        "*Y5_R2FR_motion_load_phase_volume_parent_origin_or_finite_vector_backstop_2163*",
        "*AFRAME_MOTION_LOAD_QLOC_2163*",
        "*JR2163*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2163_00_2162_handoff",
            DOCS["2162"],
            [["NEXT2162_0_2163"], ["SCF2162_1_constraint_auxiliary"], ["VAL2162_OVERALL"]],
            "2162 selects motion-load/phase-volume parent origin or finite-vector backstop.",
        ),
        (
            "SRC2163_01_2162_validation",
            DOCS["2162_validation"],
            [["VAL2162_OVERALL"], ["PASS"]],
            "2162 validation passed as nonclaim.",
        ),
        (
            "SRC2163_02_2162_next_csv",
            DOCS["2162_next"],
            [["NEXT2162_0_2163"], ["motion-load"], ["finite residual"]],
            "machine-readable 2163 handoff.",
        ),
        (
            "SRC2163_03_1859_phase_volume",
            DOCS["1859"],
            [["MPD1859_5_direct_phase_volume_verdict"], ["FRS1859_2_parent_Euler_difference"], ["VAL1859_OVERALL"]],
            "prior parent-origin audit rejects direct phase-volume and selects Euler-difference route.",
        ),
        (
            "SRC2163_04_1859_validation",
            DOCS["1859_validation"],
            [["VAL1859_OVERALL"], ["PASS"]],
            "1859 validation passed as nonclaim.",
        ),
        (
            "SRC2163_05_1860_qloc_bridge",
            DOCS["1860"],
            [["QZA1860_7_verdict"], ["NEXT1860_0_primary"], ["VAL1860_OVERALL"]],
            "Gamma/Khat/q_loc bridge records formal mechanism but live coupling lock remains open.",
        ),
        (
            "SRC2163_06_1860_validation",
            DOCS["1860_validation"],
            [["VAL1860_OVERALL"], ["PASS"]],
            "1860 validation passed as nonclaim.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def motion_origin_rows() -> list[dict[str, object]]:
    data = [
        (
            "MLO2163_0_identity",
            "radial observer-cell identity",
            "J_q := T sqrt(S); C_R := ln(T^2 S)=2 ln(J_q)",
            "EXACT_IDENTITY",
            "bookkeeping is clean and matches the local reciprocity variable",
        ),
        (
            "MLO2163_1_if_fixed",
            "if parent law gives J_q=1",
            "T sqrt(S)=1 -> T^2 S=1; with T^2=1-L and S=(1-L)^(-p), p=1",
            "EXACT_CONDITIONAL_LOCAL_GR_RECIPROCITY",
            "this is the target, not the proof",
        ),
        (
            "MLO2163_2_direct_phase_volume",
            "motion-load/phase-volume story",
            "load reduces clock capacity while radial routing compensates",
            "MOTIVATION_NOT_PARENT_DERIVATION",
            "does not supply an Euler equation, multiplier, boundary class or no-charge theorem",
        ),
        (
            "MLO2163_3_liouville_no_go",
            "ordinary Liouville or symplectic phase volume",
            "canonical phase-volume preservation is true too broadly and does not select p=1",
            "REJECT_AS_SELECTOR",
            "cannot be used as the parent law",
        ),
        (
            "MLO2163_4_cell_current",
            "conserved radial cell current",
            "partial_r(W_R partial_r C_R)=0 -> W_R partial_r C_R=Q_R",
            "DERIVES_CONSTANT_NOT_ZERO",
            "needs Q_R=0 source/boundary theorem before local reciprocity follows",
        ),
        (
            "MLO2163_5_direct_verdict",
            "direct motion-load parent origin",
            "motion-load/phase-volume alone does not derive C_R=0 in the current corpus",
            "REJECT_DIRECT_PARENT_DERIVATION_CURRENT_CORPUS",
            "move to MTS-owned Euler difference and q_loc/coupling lock",
        ),
    ]
    return [
        row(origin_id=origin_id, object=object_name, formula_or_claim=formula_or_claim, status=status, consequence=consequence)
        for origin_id, object_name, formula_or_claim, status, consequence in data
    ]


def euler_difference_rows() -> list[dict[str, object]]:
    data = [
        (
            "EDR2163_0_parent_euler_pair",
            "E_time and E_radial",
            "derive both from MTS parent variations without importing Einstein equations",
            "MISSING_PARENT_EULER_PAIR",
            "local GR cannot be reduced until the parent equations exist",
        ),
        (
            "EDR2163_1_difference_law",
            "D_R[MTS]=E_time-E_radial",
            "D_R[MTS] = partial_r C_R - S_R[source,residual,boundary,readout] = 0",
            "CONDITIONAL_ROUTE_FORM",
            "if S_R=0 and boundary normalization closes, C_R=0 follows",
        ),
        (
            "EDR2163_2_source_residual_side",
            "S_R terms",
            "S_R contains q_loc, DeltaGamma/source-current, support, boundary and readout residuals",
            "MISSING_SOURCE_RESIDUAL_ZERO",
            "extra-sector silence is the actual local-GR bottleneck",
        ),
        (
            "EDR2163_3_boundary_no_charge",
            "Q_R/no-charge theorem",
            "Q_R=0 plus C_R(infinity)=0 gives C_R=0 for current/equation-difference branch",
            "NO_CHARGE_THEOREM_UNSIGNED",
            "boundary/projector/local-source proof is still required",
        ),
        (
            "EDR2163_4_conditional_gr",
            "local reciprocity/GR limit",
            "E_time-E_radial derived, S_R=0, Q_R=0 -> C_R=0 -> p=1 local reciprocity",
            "EXACT_CONDITIONAL_TARGET",
            "this would be a serious GR-reduction path if the premises close",
        ),
        (
            "EDR2163_5_verdict",
            "Euler-difference route",
            "best surviving noncircular route, but not a current derivation",
            "LIVE_ROUTE_NOT_CLOSED",
            "attack q_loc/coupling lock next and retain finite vector backstop",
        ),
    ]
    return [
        row(route_id=route_id, object=object_name, formula_or_requirement=formula_or_requirement, status=status, consequence=consequence)
        for route_id, object_name, formula_or_requirement, status, consequence in data
    ]


def qloc_bridge_rows() -> list[dict[str, object]]:
    data = [
        (
            "QBS2163_0_definition",
            "q_loc^nu",
            "q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "DEFINITION_RECORDED",
            "local force/source residual to zero or bound",
        ),
        (
            "QBS2163_1_formal_mechanism",
            "positive auxiliary / response doublet",
            "formal action, metric response, Helmholtz readiness and double-zero inside a constructed class",
            "PASS_FORMAL_ONLY",
            "gives a mechanism shape, not live MTS activation",
        ),
        (
            "QBS2163_2_live_action_pair",
            "Gamma_eff/K_hat variational pair",
            "K_hat must equal metric response of a parent-owned Gamma_eff density with boundary/improvement terms",
            "LIVE_ADOPTION_NOT_CLOSED",
            "q_loc is not yet a Ward/Euler residual of a real sector",
        ),
        (
            "QBS2163_3_coupling_lock",
            "matter/source/readout/boundary evenness or descent",
            "linear J_Z/B_Z/species/readout terms vanish or are quotient-descended",
            "COUPLING_LOCK_OPEN",
            "formal F1=0 can leak back into physical observables",
        ),
        (
            "QBS2163_4_projector_boundary",
            "P_loc and boundary no-flux",
            "local projector, derivative silence and source-worldtube/local-sphere flux are parent-owned",
            "BOUNDARY_PROJECTOR_OPEN",
            "local-vacuum plateau cannot be asserted",
        ),
        (
            "QBS2163_5_residual_status",
            "epsilon_GK_q_loc",
            "norm of projected Gamma/Khat mismatch after source, boundary and readout terms",
            "RETAIN_NONCLAIM",
            "carry into Euler source side and empirical vector backstop",
        ),
        (
            "QBS2163_6_verdict",
            "q_loc zero as local theorem",
            "formal mechanism exists but live action/coupling/boundary/observable locks are unsigned",
            "QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "next target is source-functional evenness/coupling lock or finite coefficient acquisition",
        ),
    ]
    return [
        row(bridge_id=bridge_id, object=object_name, formula_or_requirement=formula_or_requirement, status=status, consequence=consequence)
        for bridge_id, object_name, formula_or_requirement, status, consequence in data
    ]


def finite_vector_rows() -> list[dict[str, object]]:
    data = [
        ("FVB2163_0_epsilon_q_loc", "epsilon_GK_q_loc", "q_loc norm after local projection", "local_GR;PPN;clock;orbital;R10/source-normalization", "SOURCE_COEFFICIENT_REQUIRED", False),
        ("FVB2163_1_DeltaGamma", "DeltaGamma_source_connection", "connection/hypermomentum/source-current leakage", "WEP;clock;lightcone;PPN_gamma;local_GR", "SOURCE_COEFFICIENT_REQUIRED", False),
        ("FVB2163_2_QR_boundary", "Q_R_boundary", "radial cell no-charge/boundary constant", "local reciprocity;orbital;lab finite-source", "BOUNDARY_THEOREM_OR_BOUND_REQUIRED", False),
        ("FVB2163_3_SR_source", "S_R_source_side", "Euler-difference source/residual/readout side", "local_GR;PPN;orbital;clock", "SOURCE_MAP_REQUIRED", False),
        ("FVB2163_4_total_backstop", "finite residual vector", "|residual_total| <= sum absolute component bounds", "R10;PPN;clock;orbital;WEP", "SCHEMA_OPEN_VALUES_MISSING", False),
    ]
    return [
        row(backstop_id=backstop_id, quantity=quantity, definition=definition, arenas=arenas, status=status, valid_for_claim=valid_for_claim)
        for backstop_id, quantity, definition, arenas, status, valid_for_claim in data
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2163_0_identity", "J_q/C_R identity and p=1 conditional are exact", True, "bookkeeping and conditional local reciprocity algebra close"),
        ("CG2163_1_direct_phase_volume", "motion-load/phase-volume directly derives C_R=0", False, "specific cell preservation is not parent-derived"),
        ("CG2163_2_euler_route_selected", "Euler-difference route is selected", True, "best surviving noncircular route"),
        ("CG2163_3_parent_euler_closed", "E_time/E_radial and D_R[MTS] are parent-derived", False, "parent Euler pair/source map missing"),
        ("CG2163_4_q_loc_zero", "q_loc is theorem-zero on local branch", False, "live action/coupling/boundary/observable locks open"),
        ("CG2163_5_finite_vector_ready", "finite vector backstop is numerically source-ready", False, "component rows are placeholders/acquisition targets"),
        ("CG2163_6_local_GR_claim", "local GR/Newton reduction is derived", False, "needs parent Euler, source silence, no-charge, q_loc lock and readout descent"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2163_0_phase_volume_closure", "claim J_q=1 from intuition alone", "MOTIVATION_NOT_DERIVATION", "BLOCKED", "direct phase-volume route rejected", False),
        ("REF2163_1_liouville_selector", "use Liouville/symplectic volume to select p=1", "TOO_BROAD", "BLOCKED", "does not distinguish local reciprocity branch", False),
        ("REF2163_2_no_charge_assumption", "set Q_R=0 by local vacuum wording", "NO_CHARGE_THEOREM_UNSIGNED", "BLOCKED", "boundary/source theorem missing", False),
        ("REF2163_3_q_loc_zero", "promote formal q_loc normal form to physical zero", "COUPLING_LOCK_OPEN", "BLOCKED", "live Gamma/Khat/source/readout/boundary locks unsigned", False),
        ("REF2163_4_local_gr", "claim derived local GR/Newton now", "PARENT_EULER_AND_RESIDUAL_SILENCE_MISSING", "BLOCKED", "conditional route only", False),
    ]
    return [
        row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible)
        for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data
    ]


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2163_0_phase_volume",
            "Direct phase-volume is demoted to motivation/closure for the current corpus.",
            "it finds the right condition but lacks parent Euler/multiplier/no-charge machinery.",
            "do not claim local reciprocity from J_q=1 unless parent-derived later",
        ),
        (
            "DEC2163_1_euler_difference",
            "The live derivation route is parent Euler difference plus source/residual silence.",
            "D_R[MTS]=partial_r C_R-S_R=0 can yield C_R=0 only when S_R and Q_R are zero/bounded.",
            "attack q_loc/coupling lock because it contaminates S_R",
        ),
        (
            "DEC2163_2_backstop",
            "Finite residual vector backstop is now explicitly open.",
            "if q_loc or boundary/source terms do not zero, they must be bounded in R10/PPN/clock/orbital arenas.",
            "source epsilon_GK_q_loc, DeltaGamma, Q_R and S_R component rows",
        ),
        (
            "DEC2163_3_next",
            "Next checkpoint should target source-functional evenness J_Z/B_Z coupling lock.",
            "that is the fastest way to decide whether the formal q_loc double-zero becomes physical or remains a finite residual.",
            "2164-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-finite-vector-coefficients.md",
        ),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2163_0_2164",
            "2164-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-finite-vector-coefficients.md",
            "scripts/Y5_R2FR_source_functional_evenness_JZ_BZ_coupling_lock_or_finite_vector_coefficients_2164.py",
            "try to prove matter, source-normalization, species, readout and boundary functionals are exchange-even or quotient-descended in the local residual Z; if not, create nonclaim finite coefficient rows for epsilon_GK_q_loc, DeltaGamma, Q_R and S_R",
            "selected",
            "parent-signed no-linear-source theorem activates q_loc double-zero, or finite residual coefficient rows become the empirical backstop",
        ),
        (
            "NEXT2163_1_parallel",
            "2164b-Y5-R2FR-live-Khat-metric-variation-comparison.md",
            "scripts/Y5_R2FR_live_Khat_metric_variation_comparison_2164b.py",
            "compute K_metric from candidate Gamma_eff scalar density and compare against live K_hat including boundary/improvement terms",
            "held",
            "term-by-term metric-response match or explicit mismatch ledger",
        ),
    ]
    return [
        row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition)
        for route_id, next_target, script, objective, selection_status, success_condition in data
    ]


def write_branch_copies(
    motion_origin: list[dict[str, object]],
    euler_route: list[dict[str, object]],
    qloc_bridge: list[dict[str, object]],
    finite_vector: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2163_0_source_weight_docs", BRANCH_COPIES["source_weight"], motion_origin + euler_route),
        ("COPY2163_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], qloc_bridge + finite_vector),
        ("COPY2163_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + finite_vector),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    motion_origin: list[dict[str, object]],
    euler_route: list[dict[str, object]],
    qloc_bridge: list[dict[str, object]],
    finite_vector: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    origin_ok = any(item["origin_id"] == "MLO2163_5_direct_verdict" and item["status"] == "REJECT_DIRECT_PARENT_DERIVATION_CURRENT_CORPUS" for item in motion_origin)
    euler_ok = any(item["route_id"] == "EDR2163_5_verdict" and item["status"] == "LIVE_ROUTE_NOT_CLOSED" for item in euler_route)
    qloc_ok = any(item["bridge_id"] == "QBS2163_6_verdict" and item["status"] == "QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS" for item in qloc_bridge)
    vector_ok = any(item["backstop_id"] == "FVB2163_4_total_backstop" and item["status"] == "SCHEMA_OPEN_VALUES_MISSING" for item in finite_vector)
    gate_ok = (
        any(item["gate_id"] == "CG2163_2_euler_route_selected" and truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "CG2163_6_local_GR_claim" and not truthy(item["gate_pass"]) for item in gates)
        and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    )
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2163_3_next" and "2164" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2163_0_2164" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, motion_origin, euler_route, qloc_bridge, finite_vector, gates, refusals, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2163_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, origin_ok, euler_ok, qloc_ok, vector_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2163_00_sources", sources_ok, "2162 plus 1859/1860 source paths and needles validate"),
        ("VAL2163_01_origin", origin_ok, "direct motion-load/phase-volume origin is rejected as current derivation"),
        ("VAL2163_02_euler_route", euler_ok, "Euler-difference route remains live but not closed"),
        ("VAL2163_03_qloc_bridge", qloc_ok, "q_loc formal mechanism remains nonclaim until coupling lock closes"),
        ("VAL2163_04_vector_backstop", vector_ok, "finite residual vector backstop is open but values missing"),
        ("VAL2163_05_claim_gates", gate_ok, "identity/route selection can pass while local-GR claim remains blocked"),
        ("VAL2163_06_refusals", refusal_ok, "refusal runner blocks phase-volume closure, no-charge assumption, q_loc zero and local-GR claims"),
        ("VAL2163_07_decision", decisions_ok, "decision ledger selects 2164 coupling-lock target"),
        ("VAL2163_08_next", next_ok, "2164 next target selected"),
        ("VAL2163_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2163_10_csv_parse", csv_ok, "all generated 2163 CSVs parse cleanly"),
        ("VAL2163_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2163_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2163"),
        ("VAL2163_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2163_OVERALL", all_ok, "2163 rejects direct phase-volume as derivation, selects Euler/q_loc coupling lock, and opens the finite-vector backstop."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    motion_origin: list[dict[str, object]],
    euler_route: list[dict[str, object]],
    qloc_bridge: list[dict[str, object]],
    finite_vector: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2162, _ = find_line(DOCS["2162"], ["NEXT2162_0_2163"])
    line_1859, _ = find_line(DOCS["1859"], ["MPD1859_5_direct_phase_volume_verdict"])
    line_1860, _ = find_line(DOCS["1860"], ["QZA1860_7_verdict"])
    content = "\n\n".join(
        [
            "# 2163 - Y5/R2FR Motion-Load Phase-Volume Parent Origin Or Finite Vector Backstop",
            "## Current Verdict",
            "2163 does **not** derive local GR/Newton, does **not** prove `J_q=1`, and does **not** prove `q_loc=0` as a physical theorem.",
            "`J_q=T sqrt(S)` and `C_R=ln(T^2S)=2ln(J_q)` are exact, and `J_q=1` exactly gives the local reciprocity/p=1 target. But direct motion-load/phase-volume remains motivation or closure in the current corpus, not the parent law.",
            "The surviving derivation route is parent Euler difference plus extra-sector silence: derive `D_R[MTS]=E_time-E_radial=partial_r C_R-S_R=0`, then prove `S_R=0`, `Q_R=0`, and readout descent. The immediate bottleneck is the `Gamma_eff/K_hat/q_loc` coupling lock.",
            f"This follows the 2162 handoff at line {line_2162}, imports the 1859 direct-origin rejection at line {line_1859}, and carries forward the 1860 q_loc bridge verdict at line {line_1860}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Motion-Load Origin Audit",
            md_table(motion_origin, ["origin_id", "object", "formula_or_claim", "status", "consequence", "valid_for_claim"]),
            "## Euler Difference Route",
            md_table(euler_route, ["route_id", "object", "formula_or_requirement", "status", "consequence", "valid_for_claim"]),
            "## q_loc Bridge Status",
            md_table(qloc_bridge, ["bridge_id", "object", "formula_or_requirement", "status", "consequence", "valid_for_claim"]),
            "## Finite Vector Backstop",
            md_table(finite_vector, ["backstop_id", "quantity", "definition", "arenas", "status", "valid_for_claim"]),
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
            "This is the cleanest statement of where we are: motion-load/phase-volume gives the target condition, not yet the derivation. The route that could actually make GR emerge is now field-equation shaped: parent Euler difference plus q_loc/source/boundary/readout silence. That is good news structurally, because it stops the theory from being a fifth-force scalar dodge. The next fight is whether the formal q_loc double-zero can be made physical by a coupling-lock theorem; if not, every leftover term must go into the finite residual vector and be tested.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    motion_origin = motion_origin_rows()
    euler_route = euler_difference_rows()
    qloc_bridge = qloc_bridge_rows()
    finite_vector = finite_vector_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["motion_origin"], motion_origin)
    write_csv(OUTPUTS["euler_route"], euler_route)
    write_csv(OUTPUTS["qloc_bridge"], qloc_bridge)
    write_csv(OUTPUTS["finite_vector"], finite_vector)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(motion_origin, euler_route, qloc_bridge, finite_vector, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, motion_origin, euler_route, qloc_bridge, finite_vector, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, motion_origin, euler_route, qloc_bridge, finite_vector, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2163 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
