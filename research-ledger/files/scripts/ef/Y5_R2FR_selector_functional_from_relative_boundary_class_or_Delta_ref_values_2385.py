from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_SELECTOR_FUNCTIONAL_FROM_RELATIVE_BOUNDARY_CLASS_OR_DELTA_REF_VALUES_2385"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2385-Y5-R2FR-selector-functional-from-relative-boundary-class-or-Delta-ref-values.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2385_00_2384_doc",
            "source_key": "2384_doc",
            "source_path": POST_ROOT / "2384-Y5-R2FR-boundary-stationarity-equation-for-Sigma-ref-or-source-pack-fill.md",
            "needles": ["S_sel = 1/2 <F_bc, A F_bc>", "selector functional construction selected next"],
            "source_role": "2384 handoff to selector functional construction",
        },
        {
            "row_id": "SRC2385_01_2384_stationarity",
            "source_key": "2384_stationarity",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2384_BOUNDARY_STATIONARITY_ATTEMPT.csv",
            "needles": ["BSE2384_3_sufficient_selector_action", "THEOREM_NOT_PROMOTED_RETAIN_SOURCE_PACK"],
            "source_role": "stationarity equation and sufficient selector-action contract",
        },
        {
            "row_id": "SRC2385_02_60_doc",
            "source_key": "60_relative_contract",
            "source_path": POST_ROOT / "60-relative-cohomology-boundary-contract.md",
            "needles": ["relative memory class", "relative_boundary_contract_written_not_derived"],
            "source_role": "relative cohomology boundary contract precedent",
        },
        {
            "row_id": "SRC2385_03_71_doc",
            "source_key": "71_relative_current",
            "source_path": POST_ROOT / "71-relative-boundary-current-construction-attempt.md",
            "needles": ["a formal relative current can be written, but it is not parent-derived yet", "relative_pair_written"],
            "source_role": "relative current construction precedent and nonclaim status",
        },
        {
            "row_id": "SRC2385_04_996_doc",
            "source_key": "996_relative_owner",
            "source_path": POST_ROOT / "996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md",
            "needles": ["future parent action must select `C_top`, `B_ref`", "contract is not signed by the current corpus"],
            "source_role": "relative boundary class owner failure and contract",
        },
        {
            "row_id": "SRC2385_05_1020_doc",
            "source_key": "1020_domain_certificate",
            "source_path": POST_ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needles": ["weighted-Stokes theorem", "closed/corner-free domain"],
            "source_role": "boundary/cohomology/corner conditions",
        },
        {
            "row_id": "SRC2385_06_1020_domain_csv",
            "source_key": "1020_domain_csv",
            "source_path": RESIDUALS / "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv",
            "needles": ["BDC1020_1_boundary_class", "BDC1020_2_relative_cohomology"],
            "source_role": "machine-readable boundary class/cohomology certificates",
        },
        {
            "row_id": "SRC2385_07_667_ansatz",
            "source_key": "667_ansatz",
            "source_path": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
            "needles": ["PBA667_2_boundary_action", "PBA667_4_reference_rule"],
            "source_role": "parent boundary action scaffold",
        },
        {
            "row_id": "SRC2385_08_2384_next",
            "source_key": "2384_next",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2384_NEXT_TARGET.csv",
            "needles": ["NEXT2384_0_selected", "relative boundary class data"],
            "source_role": "machine-readable 2385 target",
        },
    ]
    rows: list[dict[str, object]] = []
    for source in sources:
        path = Path(source["source_path"])
        needles = list(source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": source["row_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": str(path.exists()).lower(),
                "required": "true",
                "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                "needles": "; ".join(needles),
                "source_role": source["source_role"],
                "valid_for_claim": no_claim(),
            }
        )
    return rows


def selector_functional_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSF2385_0_constraint_map",
            "component": "relative boundary constraint map",
            "functional_form": "F_bc(Sigma_ref;B_class,C_top,tau,e_infty)=(C_rel(Sigma_ref)-C_top, d_S B_ref-h_rel-r_rel, corner_lock, tau_lock, frame_lock, S0_lock)",
            "why_this_route": "turns reference selection into explicit constraints on relative class/domain data",
            "current_status": "CONSTRAINT_MAP_WRITTEN_NOT_PARENT_OWNED",
            "missing_for_claim": "parent-owned definitions of C_rel, h_rel, r_rel, corner_lock, tau_lock, frame_lock and S0_lock",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSF2385_1_multiplier_action",
            "component": "lower-scrutiny selector action",
            "functional_form": "S_sel=int_boundary <lambda_bc,F_bc>_top",
            "why_this_route": "Lagrange multiplier constraints avoid importing a metric/Hodge norm into the selector unless a source-free pairing is proved",
            "current_status": "SUFFICIENT_CONTRACT_NOT_CURRENT_PARENT_ACTION",
            "missing_for_claim": "topological/source-free pairing, multiplier boundary conditions and parent action inclusion",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSF2385_2_stationarity",
            "component": "stationarity equations",
            "functional_form": "delta_lambda S_sel=F_bc=0; delta_Sigma S_sel=(D_Sigma F_bc)^dagger lambda_bc=0",
            "why_this_route": "regular constraints set the selector data before readout",
            "current_status": "FORMAL_VARIATION_DERIVED_CONDITIONAL",
            "missing_for_claim": "regularity/full-rank proof for D_Sigma F_bc and zero-mode quotient",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSF2385_3_source_blindness",
            "component": "source-blind selector proof",
            "functional_form": "D_source F_bc=0 and rank(D_Sigma F_bc)=full => D_source Sigma_ref=0",
            "why_this_route": "connects relative boundary class construction to 2383 implicit selector theorem",
            "current_status": "CONDITIONAL_THEOREM_SHAPE",
            "missing_for_claim": "source-free proof for each F_bc component and full-rank certificate",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSF2385_4_norm_square_variant",
            "component": "norm-square selector action",
            "functional_form": "S_sel=1/2 <F_bc,A F_bc>",
            "why_this_route": "positive form can prove uniqueness if A is source-free positive",
            "current_status": "RISKIER_VARIANT_RETAINED_ONLY_IF_PAIRING_SOURCE_FREE",
            "missing_for_claim": "A/pairing must not depend on source/readout metric data",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSF2385_5_verdict",
            "component": "current selector functional verdict",
            "functional_form": "relative-class Lagrange selector",
            "why_this_route": "best available low-cheat path to make Sigma_ref parent-selected",
            "current_status": "CONTRACT_ADVANCED_NOT_PROMOTED",
            "missing_for_claim": "explicit parent-owned F_bc components, source-free pairing and rank proof",
            "valid_for_claim": no_claim(),
        },
    ]


def component_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCG2385_0_Crel",
            "constraint_component": "C_rel(Sigma_ref)-C_top",
            "needed_zero": "relative/topological class fixed before source/readout",
            "current_status": "C_TOP_CONTRACT_NOT_PARENT_SELECTED",
            "failure_residual": "epsilon_top_abs;Delta_ref_class_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCG2385_1_exact_boundary",
            "constraint_component": "d_S B_ref-h_rel-r_rel",
            "needed_zero": "exact/proper boundary representative with harmonic/residual parts absent or bounded",
            "current_status": "B_REF_PRIMITIVE_NOT_PARENT_OWNED",
            "failure_residual": "B_zero_remainder;Delta_ref_functional_gap",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCG2385_2_corner",
            "constraint_component": "corner_lock",
            "needed_zero": "corner-free domain or included fixed corner charge",
            "current_status": "CORNER_CERTIFICATE_MISSING",
            "failure_residual": "epsilon_corner_abs",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCG2385_3_tau_frame",
            "constraint_component": "tau_lock and frame_lock",
            "needed_zero": "same tau/coframe for Q_tau, H_ref and M_H_ref",
            "current_status": "SAME_FRAME_LOCK_MISSING",
            "failure_residual": "epsilon_delta_tau_abs;M_H_ref non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCG2385_4_surface",
            "constraint_component": "S0_lock",
            "needed_zero": "source-independent linked surfaces and no retuning",
            "current_status": "SURFACE_NO_RETUNE_MISSING",
            "failure_residual": "Delta_ref_surface_component_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCG2385_5_pairing",
            "constraint_component": "topological/source-free pairing <lambda,F>",
            "needed_zero": "no metric/source/readout stress from the selector action",
            "current_status": "PAIRING_SOURCE_FREE_CERTIFICATE_MISSING",
            "failure_residual": "selector_pairing_stress_leak",
            "valid_for_claim": no_claim(),
        },
    ]


def delta_ref_value_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRV2385_0_class_leak",
            "quantity": "Delta_ref_class_leak_over_MH",
            "formula": "abs(partial_source C_rel * K_class)/M_H_ref or theorem-zero via parent selected C_top",
            "current_value": "MISSING_CREL_SOURCE_DERIVATIVE;MISSING_K_CLASS;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRV2385_1_pairing_stress",
            "quantity": "selector_pairing_stress_leak_over_MH",
            "formula": "abs(delta_metric <lambda,F_bc>_pairing)/M_H_ref",
            "current_value": "MISSING_PAIRING_METRIC_VARIATION;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRV2385_2_rank_leak",
            "quantity": "selector_rank_branch_leak_over_MH",
            "formula": "norm(P_kernel D_source Sigma_ref)/M_H_ref",
            "current_value": "MISSING_RANK_CERTIFICATE;MISSING_KERNEL_PROJECTOR;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRV2385_3_total",
            "quantity": "Delta_ref_relative_selector_total_over_MH",
            "formula": "absolute sum of class, primitive, corner, tau/frame, surface, pairing and rank leaks over M_H_ref",
            "current_value": "COMPONENTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2385_0_best_functional",
            "decision": "prefer Lagrange-multiplier relative-class selector over norm-square selector",
            "reason": "it avoids smuggling a source/readout metric into the selector pairing unless the pairing is parent-proved source-free",
            "consequence": "S_sel=<lambda,F_bc> becomes the clean future parent-action contract",
            "status": "LOWER_SCRUTINY_SELECTOR_CONTRACT_SELECTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2385_1_no_promotion",
            "decision": "do not promote selector functional theorem",
            "reason": "F_bc components, pairing, rank/nondegeneracy and M_H_ref are not parent-owned",
            "consequence": "Delta_ref values remain missing/nonclaim",
            "status": "CONTRACT_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2385_2_next",
            "decision": "attack C_rel/C_top parent selection or fill values",
            "reason": "the first concrete component is relative class selection; if that fails, no selector functional closes",
            "consequence": "2386 should try to derive C_top superselection from parent topology/Ward data or source-pack class leak",
            "status": "SELECT_2386_CTOP_SUPERSELECTION",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2385_0_selector_functional_shape",
            "gate": "relative-class selector functional shape written",
            "gate_status": "PASS_CONTRACT_ONLY",
            "claim_effect": "future parent action target",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2385_1_Fbc_parent_owned",
            "gate": "F_bc components parent-owned and source-free",
            "gate_status": "FAIL",
            "claim_effect": "Sigma_ref not proved source-blind",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2385_2_pairing_source_free",
            "gate": "selector pairing/source measure source-free",
            "gate_status": "FAIL_UNSIGNED",
            "claim_effect": "selector stress/source leak remains possible",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2385_3_rank",
            "gate": "regular/full-rank constraint map after quotient",
            "gate_status": "FAIL",
            "claim_effect": "branch leak remains possible",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2385_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "Delta_ref values remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2385_5_local_GR_Newton",
            "gate": "local GR/Newton recovery",
            "gate_status": "FAIL_NONCLAIM",
            "claim_effect": "reference/source-measure/denominator gates remain open",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2385_0_contract_as_claim",
            "claim": "treat S_sel=<lambda,F_bc> contract as current MTS proof",
            "allowed": "false",
            "reason": "F_bc and pairing are not parent-owned in the active corpus",
            "blocking_rows": "RSF2385_1_multiplier_action;CG2385_1_Fbc_parent_owned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2385_1_metric_norm_shortcut",
            "claim": "use norm-square selector without proving source-free pairing",
            "allowed": "false",
            "reason": "metric/Hodge pairing can reintroduce source/readout stress",
            "blocking_rows": "RSF2385_4_norm_square_variant;RCG2385_5_pairing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2385_2_score_values",
            "claim": "score Delta_ref values now",
            "allowed": "false",
            "reason": "component values and M_H_ref are missing",
            "blocking_rows": "DRV2385_0_class_leak;DRV2385_3_total;CG2385_4_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2385_0_selected",
            "next_file": "2386-Y5-R2FR-Ctop-superselection-from-parent-topology-or-class-leak-row.md",
            "success_condition": "derive parent-owned C_top/relative class superselection with D_source C_top=0 before readout",
            "fallback_condition": "fill Delta_ref_class_leak_over_MH with finite source derivative, units, source path and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2385_1_parallel",
            "next_file": "2386b-Y5-R2FR-source-free-pairing-for-selector-or-pairing-stress-row.md",
            "success_condition": "prove <lambda,F_bc> pairing is topological/source-free and has no metric/readout stress",
            "fallback_condition": "retain selector_pairing_stress_leak row",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2385_2_parallel",
            "next_file": "2386c-Y5-R2FR-selector-rank-zero-mode-quotient-or-branch-leak-row.md",
            "success_condition": "prove D_Sigma F_bc is full rank after quotienting gauge/topological zero modes",
            "fallback_condition": "retain selector_rank_branch_leak row",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2385_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2385_RELATIVE_SELECTOR_FUNCTIONAL.csv": selector_functional_rows,
    "P8_Y5_PARENT_QLOC_2385_COMPONENT_GATES.csv": component_gate_rows,
    "P8_Y5_PARENT_QLOC_2385_DELTA_REF_VALUE_ROWS.csv": delta_ref_value_rows,
    "P8_Y5_PARENT_QLOC_2385_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2385_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2385_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2385_NEXT_TARGET.csv": next_target_rows,
}


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                return False
    return True


def validation_rows() -> list[dict[str, object]]:
    csv_paths = [RESIDUALS / name for name in CSV_BUILDERS]
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": no_claim(),
            }
        )

    sources = source_register()
    add("VAL2385_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2385_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    functional = selector_functional_rows()
    add(
        "VAL2385_02_multiplier_functional_present",
        any(row["row_id"] == "RSF2385_1_multiplier_action" for row in functional),
        "Lagrange-multiplier relative selector functional present",
    )
    gates = component_gate_rows()
    add(
        "VAL2385_03_component_gates_present",
        {"RCG2385_0_Crel", "RCG2385_1_exact_boundary", "RCG2385_5_pairing"}.issubset({row["row_id"] for row in gates}),
        "Crel/exact-boundary/pairing component gates present",
    )
    values = delta_ref_value_rows()
    add(
        "VAL2385_04_value_rows_nonready",
        all(row["score_ready"] == "false" for row in values),
        "Delta_ref value rows remain non-score-ready",
    )
    claim_rows = claim_gate_rows()
    add(
        "VAL2385_05_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in claim_rows if row["row_id"] != "CG2385_0_selector_functional_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2385_06_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add("VAL2385_07_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2385_08_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2385_09_next_selected",
        any(row["row_id"] == "NEXT2385_0_selected" for row in next_target_rows()),
        "C_top superselection selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2385_OVERALL",
        overall,
        "2385 constructs the lower-scrutiny relative-class Lagrange selector contract, refuses promotion without parent-owned Fbc/pairing/rank/MHref, and selects Ctop superselection next",
    )
    return rows


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_SOURCE_REGISTER.csv")
    functional = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_RELATIVE_SELECTOR_FUNCTIONAL.csv")
    component_gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_COMPONENT_GATES.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_DELTA_REF_VALUE_ROWS.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2385_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2385_VALIDATION.csv")

    body = f"""# 2385 - selector functional from relative boundary class or Delta-ref values

## Result

2385 builds the lowest-cheat selector-functional route found so far:

`S_sel = int_boundary <lambda_bc, F_bc(Sigma_ref; B_class, C_top, tau, e_infty)>_top`.

This is better than immediately using a norm-square/Hodge selector because it can be formulated as a constraint action;
the metric/source-dependent pairing problem is pushed into an explicit gate instead of hidden inside a norm.

The variation is clean as a future contract:

`delta_lambda S_sel = F_bc = 0`,

`delta_Sigma S_sel = (D_Sigma F_bc)^dagger lambda_bc = 0`.

If `F_bc` is source-free and `D_Sigma F_bc` is full rank after quotienting gauge/topological zero modes, then 2383's
implicit-function route gives source-blind `Sigma_ref`.  But current MTS still lacks parent-owned `F_bc` components,
source-free pairing, rank proof, and `M_H_ref`.  So this is a sharpened contract, not a proof.

No `Delta_ref=0`, `B_zero_flux=0`, Newton, local-GR, PPN, orbital, clock, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Relative Selector Functional

{markdown_table(functional, ["row_id", "component", "functional_form", "why_this_route", "current_status", "missing_for_claim", "valid_for_claim"])}

## Component Gates

{markdown_table(component_gates, ["row_id", "constraint_component", "needed_zero", "current_status", "failure_residual", "valid_for_claim"])}

## Delta Ref Value Rows

{markdown_table(values, ["row_id", "quantity", "formula", "current_value", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is a useful leap, not a close.  We now have a less fragile selector-action architecture: a relative-class
constraint action rather than a fitted reference or metric norm-square.  The first real component to attack is
`C_top` superselection.  If `C_top` cannot be parent-selected before readout, the whole selector branch must become a
source-pack branch.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2385_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2385_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
