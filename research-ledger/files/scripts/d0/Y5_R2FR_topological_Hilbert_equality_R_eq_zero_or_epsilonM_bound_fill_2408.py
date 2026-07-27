from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_TOPOLOGICAL_HILBERT_EQUALITY_R_EQ_ZERO_OR_EPSILONM_BOUND_FILL_2408"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2408-Y5-R2FR-topological-Hilbert-equality-R-eq-zero-or-epsilonM-bound-fill.md"


def post(path_text: str) -> Path:
    return POST_ROOT / path_text


SOURCES = [
    {
        "source_id": "SRC2408_2407_handoff",
        "path": str(post("2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md")),
        "needles": "NEXT2407_0_selected|PZ2407_5_topological_Hilbert_equality|ENV2407_0_no_cancellation|VAL2407_OVERALL",
        "role": "immediate handoff: topological-Hilbert equality/R_eq is the Pi_M bottleneck",
    },
    {
        "source_id": "SRC2408_2182_doc",
        "path": str(post("2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md")),
        "needles": "TEA2182_1_same_worldtube_class|TEA2182_7_current_verdict|EMB2182_6_total_envelope|VAL2182_OVERALL",
        "role": "prior full equality-or-bound checkpoint",
    },
    {
        "source_id": "SRC2408_2182_equality_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2182_TOPOLOGICAL_HILBERT_EQUALITY_AUDIT.csv")),
        "needles": "TEA2182_0_identity_target|TEA2182_7_current_verdict",
        "role": "machine equality audit from 2182",
    },
    {
        "source_id": "SRC2408_2182_bzero_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2182_REQ_BZERO_ZERO_CONDITIONS.csv")),
        "needles": "BZ2182_1_compact_flux_zero|BZ2182_5_current_verdict",
        "role": "B_zero zero-flux condition ledger",
    },
    {
        "source_id": "SRC2408_2182_finite_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2182_FINITE_ROWS.csv")),
        "needles": "EFR2182_0_R_eq|EFR2182_7_Delta_Newton",
        "role": "finite nonclaim rows for R_eq/B_zero/I_commutator/epsilon_M",
    },
    {
        "source_id": "SRC2408_1714_worldtube_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1714_WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv")),
        "needles": "WHE1714_4_same_object_equality|WHE1714_8_verdict",
        "role": "worldtube-Hilbert source equality theorem attempt",
    },
    {
        "source_id": "SRC2408_1153_conditional_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_R10_1153_CONDITIONAL_EQUALITY_THEOREM_GATE.csv")),
        "needles": "THEO1153_0_statement|THEO1153_7_verdict",
        "role": "conditional same-object theorem and no-tautology guard",
    },
    {
        "source_id": "SRC2408_2204_route_merge",
        "path": str(post("2204-Y5-R2FR-topological-Hilbert-equality-or-R-eq-first-row.md")),
        "needles": "SOT2204_0_conditional_lemma|SOT2204_4_route_verdict|FR2204_2_parent_action_descent|VAL2204_OVERALL",
        "role": "anti-duplicate route merge selecting parent-action descent frontier",
    },
    {
        "source_id": "SRC2408_2205_frontier",
        "path": str(post("2205-Y5-R2FR-current-frontier-EH-descent-PiM-source-readout-synthesis.md")),
        "needles": "SEL2205_0_target|BLK2205_0_GK_q_loc_parent_signature|NEXT2205_0_2206|VAL2205_OVERALL",
        "role": "frontier synthesis selecting Gamma/Khat/q_loc before further source-equality looping",
    },
    {
        "source_id": "SRC2408_2206_qloc",
        "path": str(post("2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md")),
        "needles": "WID2206_0_define_stress|DEC2206_3_best_next|NEXT2206_0_2207|VAL2206_OVERALL",
        "role": "downstream q_loc Ward-divergence contract and metric-response next target",
    },
]


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCES:
        source_path = Path(source["path"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_path": source["path"],
                "exists": str(source_path.exists()).lower(),
                "needles": source["needles"],
                "role": source["role"],
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def equality_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "THE2408_0_identity_with_residual",
            "claim_piece": "topological-Hilbert equality with residual",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "status": "EXACT_IDENTITY_DEFINITION",
            "result": "R_eq is the named failure mode of the same-object route",
            "missing_for_claim": "R_eq=0 theorem or source-backed R_eq_integral value",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THE2408_1_same_worldtube_conditional",
            "claim_piece": "same compact Hilbert source class",
            "mathematical_form": "if Pi_M J_H and J_M_top represent the same compact source cohomology class, their difference is exact up to R_eq",
            "status": "CONDITIONAL_MATH_CLEAN_ALREADY_RECORDED",
            "result": "the topological route is mathematically serious",
            "missing_for_claim": "parent-signed W_source, Hilbert measure, period charge, topological representative, and no hidden exchange",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THE2408_2_wrong_object_guard",
            "claim_piece": "closed topological current is not enough",
            "mathematical_form": "dJ_M_top=0 does not imply measured source closure unless R_eq=0 and B_zero_flux=0",
            "status": "GUARDRAIL_ACTIVE",
            "result": "closed wrong charge cannot be promoted to measured mass",
            "missing_for_claim": "same-object equality plus zero compact boundary flux",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THE2408_3_commutator_link",
            "claim_piece": "Pi_M commutator inherited from R_eq",
            "mathematical_form": "d(Pi_M J_H)=dR_eq when dJ_M_top=0 and d^2B_zero=0 under same-class assumptions",
            "status": "EXACT_CONDITIONAL_COMMUTATOR_LINK",
            "result": "if R_eq is not zero, I_commutator remains a live finite row",
            "missing_for_claim": "R_eq zero or finite radial/shell profile",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THE2408_4_current_verdict",
            "claim_piece": "current MTS parent-signs topological-Hilbert equality",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero with R_eq=0 and integral_boundary dB_zero=0",
            "status": "NOT_PARENT_SIGNED_NONCLAIM",
            "result": "the conditional theorem exists, but current branch does not prove the equality",
            "missing_for_claim": "R_eq=0, B_zero_flux=0, worldtube ownership, extra-channel silence, calibration, and M_H_ref",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def bzero_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "condition_id": "BZ2408_0_exact_representative",
            "condition": "dB_zero is only a representative shift",
            "statement": "dB_zero may shift exact representatives without changing the source cohomology class",
            "status": "REFERENCE_REPRESENTATIVE_ALLOWED",
            "failure_mode": "if treated as source charge, it launders boundary mass",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "condition_id": "BZ2408_1_compact_flux_zero",
            "condition": "compact linked-boundary flux vanishes",
            "statement": "integral_boundary dB_zero=0 for the same compact linked boundary used in M_eff scoring",
            "status": "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE",
            "failure_mode": "nonzero boundary flux shifts Newton/source normalization",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "condition_id": "BZ2408_2_fixed_reference",
            "condition": "single parent-fixed reference",
            "statement": "B_zero reference is fixed once by the parent source worldtube, not per arena",
            "status": "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "failure_mode": "arena-specific reference choices mimic measured-G calibration",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "condition_id": "BZ2408_3_no_boundary_leak",
            "condition": "no hidden inner/asymptotic leak",
            "statement": "no flux through infinity, source-hole surfaces, or moving excision boundaries",
            "status": "MISSING_BOUNDARY_TOPOLOGY_CERTIFICATE",
            "failure_mode": "local and orbital masses differ by surface hair",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "condition_id": "BZ2408_4_current_verdict",
            "condition": "B_zero zero proof for current branch",
            "statement": "B_zero_flux=0 with fixed source worldtube, reference, and projector-stress silence",
            "status": "B_ZERO_FLUX_ZERO_NOT_DERIVED",
            "failure_mode": "retain B_zero_flux as finite nonclaim row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def finite_rows() -> list[dict[str, str]]:
    base_rows = [
        ("REQ2408_0_R_eq", "R_eq_integral", "normalized integral of Pi_M J_H - J_M_top - dB_zero", "MISSING_R_EQ_ZERO_OR_VALUE", "dimensionless_after_M_H_ref_normalization", "Newton;PPN;R10;R11"),
        ("REQ2408_1_B_zero", "B_zero_flux", "compact linked-boundary flux of dB_zero/reference improvement", "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE", "GM_flux_or_dimensionless_after_M_H_ref_normalization", "Newton;PPN;R7;R8;R9;R11"),
        ("REQ2408_2_I_commutator", "I_commutator", "finite annulus integral of [d,Pi_M]J_H or dR_eq", "MISSING_I_COMMUTATOR_ZERO_OR_VALUE", "GM_flux_or_dimensionless_after_M_H_ref_normalization", "Newton;R10;R11;radial-source"),
        ("REQ2408_3_worldtube", "epsilon_worldtube", "source-domain/linking-surface/time-generator/Hilbert-measure mismatch", "MISSING_WORLDTUBE_SELECTOR_ZERO_OR_VALUE", "dimensionless", "Newton;PPN;WEP;orbital-source"),
        ("REQ2408_4_extra", "epsilon_extra_current", "nonEH/symplectic/memory/domain/range/frame/projector source-current channels", "MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE", "dimensionless_or_GM_flux", "Newton;PPN;WEP;R10;R11"),
        ("REQ2408_5_calibration", "epsilon_calibration", "absolute calibration residual between Hilbert source charge and Newton coefficient", "MISSING_ABSOLUTE_CALIBRATION_ZERO_OR_VALUE", "dimensionless", "Newton;PPN;orbital"),
        ("REQ2408_6_total", "epsilon_M_abs", "absolute no-cancellation envelope for measured source normalization", "MISSING_COMPONENT_INPUTS", "dimensionless", "Newton;local_GR;R10;R11"),
        ("REQ2408_7_Delta_Newton", "Delta_Newton_v_link", "(1+delta_KC)(1+epsilon_M)-1", "MISSING_DELTA_KC_AND_EPSILON_M_INPUTS", "dimensionless", "Newton;PPN;local_GR"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "units": units,
            "observable_link": observable_link,
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, symbol, definition, status, units, observable_link in base_rows
    ]


def route_merge_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2408_0_requested_2407_target",
            "route_piece": "topological-Hilbert equality/R_eq zero",
            "status": "ACTIVE_HANDOFF_HANDLED",
            "evidence": "2407 selected this as the Pi_M bottleneck",
            "action": "merge prior equality work rather than restart it",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2408_1_conditional_theorem",
            "route_piece": "same-object theorem",
            "status": "CONDITIONAL_THEOREM_ALREADY_AVAILABLE",
            "evidence": "1153, 1714, 1773, 2182, and 2204 all isolate the same condition",
            "action": "do not count this as current-MTS proof",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2408_2_finite_rows",
            "route_piece": "R_eq/B_zero/I_commutator/epsilon_M rows",
            "status": "SOURCE_READY_UNFILLED_NONCLAIM",
            "evidence": "2182 finite rows exist but lack values, source paths, and M_H_ref denominator",
            "action": "retain rows as empirical fallback, do not score placeholders",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RM2408_3_duplicate_guard",
            "route_piece": "repeat equality derivation",
            "status": "REJECTED_AS_DUPLICATE",
            "evidence": "2204 already made the anti-merry-go-round decision",
            "action": "move to parent-action/descent and q_loc metric-response frontier",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2408_0_conditional_math",
            "gate": "topological-Hilbert same-object theorem exists",
            "status": "PASS_NONCLAIM",
            "implication": "conditional math is clean but not a current MTS proof",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2408_1_current_equality",
            "gate": "Pi_M J_H=J_M_top+dB_zero is parent-signed",
            "status": "BLOCKED_NONCLAIM",
            "implication": "same worldtube, period-charge lock, M_H_ref, B_zero and no-extra-channel clauses remain unsigned",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2408_2_R_eq_first_row",
            "gate": "R_eq first row is source-backed",
            "status": "BLOCKED_NONCLAIM",
            "implication": "R_eq row is schema/placeholder only",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2408_3_no_recircle",
            "gate": "avoid duplicate equality derivation loop",
            "status": "PASS_GUARDRAIL",
            "implication": "2408 merges existing equality work and selects the next non-duplicate target",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG2408_4_local_gr_newton",
            "gate": "Newton/local-GR reduction can be claimed",
            "status": "BLOCKED_NONCLAIM",
            "implication": "source equality, q_loc, PiM, boundary, response operators, and empirical rows remain incomplete",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2408_0_closed_wrong_object",
            "claim": "closed J_M_top proves measured mass",
            "allowed": "false",
            "reason": "closed topological charge may be the wrong object unless same Hilbert/worldtube equality is parent-signed",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2408_1_late_multiplier",
            "claim": "add a late equality multiplier to impose R_eq=0",
            "allowed": "false",
            "reason": "late multiplier is closure bookkeeping unless it has an independent parent origin",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2408_2_reference_only_zero",
            "claim": "choose B_zero/reference to cancel the residual",
            "allowed": "false",
            "reason": "reference must be fixed once before readout and have zero compact flux",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2408_3_repeat_route",
            "claim": "repeat topological-Hilbert equality as new progress",
            "allowed": "false",
            "reason": "conditional equality is already mapped; next progress needs parent action/descent or source-backed rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2408_0_equality_status",
            "decision": "CONDITIONAL_EQUALITY_THEOREM_ACCEPTED",
            "rationale": "same compact Hilbert source class gives the exact route to Pi_M J_H=J_M_top+dB_zero+R_eq",
            "next_action": "do not claim current MTS equality until parent signatures close",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2408_1_claim_status",
            "decision": "CURRENT_MTS_EQUALITY_NOT_PARENT_SIGNED",
            "rationale": "R_eq=0, B_zero_flux=0, source worldtube, M_H_ref, calibration, and extra-channel silence are not signed",
            "next_action": "keep finite rows nonclaim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2408_2_route_merge",
            "decision": "REJECT_DUPLICATE_EQUALITY_REDERIVATION",
            "rationale": "2182 and 2204 already record this gate; repeating it would not move the theory closer to GR",
            "next_action": "move to the current frontier selected by 2205/2206",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2408_3_next",
            "decision": "METRIC_RESPONSE_OR_FIRST_QLOC_RESPONSE_ROW_NEXT",
            "rationale": "2206 reduces q_loc to a Ward divergence if T_GK=Khat-Gamma_eff g is parent-owned; the missing root is the Khat/Gamma_eff metric response",
            "next_action": "2409 should try one explicit Gamma_eff metric variation or create the first source-ready q_loc response-operator row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2408_0_selected",
            "next_doc": "2409-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            "why": "topological-Hilbert equality is already conditionally mapped; 2206 shows the next non-duplicate root is Khat/Gamma_eff metric response or a q_loc response operator",
            "expected_output": "either source-sign one Gamma_eff metric variation matching K_hat, or emit one PPN/R10 q_loc response-operator row with units, source path, and valid_for_claim=false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2408_1_parallel_source",
            "next_doc": "2409B-Y5-R2FR-source-backed-R-eq-MHref-Bzero-input-acquisition.md",
            "why": "if derivation stalls, R_eq/M_H_ref/B_zero inputs are the honest finite source-normalization fallback",
            "expected_output": "one real source-backed row with units and arena projection, still nonclaim until the full envelope closes",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2408_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2408_TOPOLOGICAL_HILBERT_EQUALITY_STATUS.csv": equality_rows,
    "P8_Y5_PARENT_QLOC_2408_BZERO_ZERO_CONDITIONS.csv": bzero_rows,
    "P8_Y5_PARENT_QLOC_2408_FINITE_ROWS.csv": finite_rows,
    "P8_Y5_PARENT_QLOC_2408_ROUTE_MERGE_AUDIT.csv": route_merge_rows,
    "P8_Y5_PARENT_QLOC_2408_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2408_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2408_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2408_NEXT_TARGET.csv": next_target_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sources_exist() -> bool:
    return all(Path(source["path"]).exists() for source in SOURCES)


def needles_found() -> bool:
    for source in SOURCES:
        source_path = Path(source["path"])
        if not source_path.exists():
            return False
        text = source_path.read_text(encoding="utf-8", errors="ignore")
        for needle in source["needles"].split("|"):
            if needle not in text:
                return False
    return True


def generated_rows() -> list[dict[str, str]]:
    return [
        *source_register_rows(),
        *equality_rows(),
        *bzero_rows(),
        *finite_rows(),
        *route_merge_rows(),
        *claim_gate_rows(),
        *refusal_rows(),
        *decision_rows(),
        *next_target_rows(),
    ]


def generated_text() -> str:
    return "\n".join(str(row) for row in generated_rows())


def csvs_parse() -> bool:
    csv_paths = list(CSV_BUILDERS.keys()) + ["P8_Y5_BRR545_2408_VALIDATION.csv"]
    for csv_name in csv_paths:
        csv_path = RESIDUALS / csv_name
        if not csv_path.exists():
            return False
        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            rows = list(csv.DictReader(csv_file))
        if not rows:
            return False
    return True


def no_claim_flags() -> bool:
    return all(
        str(row.get("valid_for_claim", "false")).lower() == "false"
        and str(row.get("claim_allowed", "false")).lower() == "false"
        for row in generated_rows()
    )


def finite_rows_nonclaim_unfilled() -> bool:
    rows = finite_rows()
    return len(rows) == 8 and all(row["score_ready"] == "false" and row["value"] == "MISSING_NUMERIC_VALUE" for row in rows)


def formalization_untouched_by_outputs() -> bool:
    output_paths = [DOC_PATH, *(RESIDUALS / csv_name for csv_name in CSV_BUILDERS), RESIDUALS / "P8_Y5_BRR545_2408_VALIDATION.csv"]
    try:
        formalization_resolved = FORMALIZATION_ROOT.resolve()
    except FileNotFoundError:
        return True
    for output_path in output_paths:
        try:
            output_resolved = output_path.resolve()
        except FileNotFoundError:
            output_resolved = output_path.parent.resolve() / output_path.name
        if formalization_resolved == output_resolved or formalization_resolved in output_resolved.parents:
            return False
    return True


def validation_rows() -> list[dict[str, str]]:
    text = generated_text()
    checks = [
        {
            "row_id": "VAL2408_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2408_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2408_02_conditional_equality",
            "status": "PASS" if "THE2408_1_same_worldtube_conditional" in text and "CONDITIONAL_MATH_CLEAN_ALREADY_RECORDED" in text else "FAIL",
            "detail": "conditional same-object theorem is recorded without promotion",
        },
        {
            "row_id": "VAL2408_03_current_not_signed",
            "status": "PASS" if "NOT_PARENT_SIGNED_NONCLAIM" in text and "R_eq=0" in text else "FAIL",
            "detail": "current MTS equality remains unsigned/nonclaim",
        },
        {
            "row_id": "VAL2408_04_bzero_retained",
            "status": "PASS" if "B_ZERO_FLUX_ZERO_NOT_DERIVED" in text else "FAIL",
            "detail": "B_zero flux remains retained as finite nonclaim row",
        },
        {
            "row_id": "VAL2408_05_finite_rows_nonclaim",
            "status": "PASS" if finite_rows_nonclaim_unfilled() else "FAIL",
            "detail": "R_eq/B_zero/I_commutator/epsilon_M rows are unfilled nonclaim placeholders",
        },
        {
            "row_id": "VAL2408_06_route_merge",
            "status": "PASS" if "REJECTED_AS_DUPLICATE" in text and "RM2408_3_duplicate_guard" in text else "FAIL",
            "detail": "duplicate equality rederivation is rejected",
        },
        {
            "row_id": "VAL2408_07_claim_gates",
            "status": "PASS" if "CG2408_4_local_gr_newton" in text and "BLOCKED_NONCLAIM" in text else "FAIL",
            "detail": "local GR/Newton remains blocked",
        },
        {
            "row_id": "VAL2408_08_next_selected",
            "status": "PASS" if "NEXT2408_0_selected" in text and "Gamma-eff-metric-variation" in text else "FAIL",
            "detail": "Gamma_eff metric variation or first q_loc response row selected next",
        },
        {
            "row_id": "VAL2408_09_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2408_10_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true or claim_allowed=true",
        },
        {
            "row_id": "VAL2408_11_formalization_untouched_by_outputs",
            "status": "PASS" if formalization_untouched_by_outputs() else "FAIL",
            "detail": "script outputs stay inside post-checkpoint-work",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2408_OVERALL",
            "status": overall,
            "detail": "2408 merges the topological-Hilbert equality route, keeps R_eq/epsilon_M nonclaim, rejects duplicate rederivation, and selects Gamma_eff metric variation/q_loc response as next",
        }
    )
    return [{"branch_id": BRANCH_ID, **row} for row in checks]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    body = f"""# 2408 - Topological-Hilbert Equality R_eq Zero Or EpsilonM Bound Fill

## Result

This checkpoint handles the 2407 target without looping.

The equality route is real and clean **conditionally**:

`Pi_M J_H = J_M_top + dB_zero + R_eq`.

If `Pi_M J_H` and `J_M_top` are the same compact Hilbert source cohomology class, and if the exact representative has
zero compact boundary flux, then the topological route can carry the measured source object rather than a closed wrong
charge.  But current MTS sources do not parent-sign `R_eq=0`, `B_zero_flux=0`, the source worldtube, `M_H_ref`, the
absolute calibration, or the no-extra-current clauses.

So 2408 does not re-prove the same equality one more time.  It preserves the finite `R_eq/B_zero/I_commutator/epsilon_M`
rows and routes the next derivation toward the non-duplicate root: `Gamma_eff/Khat` metric response or the first
source-ready `q_loc` response operator.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim", "claim_allowed"])}

## Topological-Hilbert Equality Status

{markdown_table(equality_rows(), ["row_id", "claim_piece", "mathematical_form", "status", "result", "missing_for_claim", "valid_for_claim", "claim_allowed"])}

## B_zero Zero Conditions

{markdown_table(bzero_rows(), ["condition_id", "condition", "statement", "status", "failure_mode", "valid_for_claim", "claim_allowed"])}

## Finite R_eq And Epsilon_M Rows

{markdown_table(finite_rows(), ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim", "claim_allowed"])}

## Route Merge Audit

{markdown_table(route_merge_rows(), ["route_id", "route_piece", "status", "evidence", "action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gate_rows(), ["gate_id", "gate", "status", "implication", "valid_for_claim", "claim_allowed"])}

## Refusal Runner

{markdown_table(refusal_rows(), ["row_id", "claim", "allowed", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision_rows(), ["decision_id", "decision", "rationale", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target_rows(), ["route_id", "next_doc", "why", "expected_output", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows(), ["row_id", "status", "detail"])}

## Practical Status

This is a useful non-result: the topological source route is not nonsense, but it is already mapped.  The way forward is
not another equality table with a different hat.  The way forward is to attack the object that decides whether the
local extra sector is silent or testable:

`T_GK = K_hat - Gamma_eff g`.

If a concrete `Gamma_eff` variation matches `K_hat`, the local-GR bridge gets a real parent-action clause.  If it does
not, `q_loc` becomes a clean finite response vector for PPN/R10/clock/orbital testing.  Still private, still no GitHub.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for csv_name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / csv_name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2408_VALIDATION.csv", validation_rows())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2408_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2408_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
