from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_BOUNDARY_STATIONARITY_EQUATION_FOR_SIGMA_REF_OR_SOURCE_PACK_FILL_2384"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2384-Y5-R2FR-boundary-stationarity-equation-for-Sigma-ref-or-source-pack-fill.md"
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
            "row_id": "SRC2384_00_2383_doc",
            "source_key": "2383_doc",
            "source_path": POST_ROOT / "2383-Y5-R2FR-parent-selector-equation-for-Sigma-ref-or-Delta-ref-source-pack.md",
            "needles": ["boundary stationarity equation selected next", "E_Sigma"],
            "source_role": "2383 handoff to boundary stationarity equation",
        },
        {
            "row_id": "SRC2384_01_2383_theorem",
            "source_key": "2383_implicit_theorem",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2383_IMPLICIT_SELECTOR_THEOREM.csv",
            "needles": ["IST2383_2_non_degeneracy", "IST2383_5_verdict"],
            "source_role": "implicit selector theorem and missing-current-verdict rows",
        },
        {
            "row_id": "SRC2384_02_2383_candidates",
            "source_key": "2383_candidates",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2383_SELECTOR_EQUATION_CANDIDATES.csv",
            "needles": ["SEC2383_0_boundary_stationarity", "SEC2383_4_verdict"],
            "source_role": "candidate selector equations",
        },
        {
            "row_id": "SRC2384_03_667_doc",
            "source_key": "667_doc",
            "source_path": POST_ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
            "needles": ["B_total  = B_GHY + B_ref + B_class + B_ct", "B_ref is named but not selected by a current parent principle"],
            "source_role": "parent boundary action ansatz and reference-lock failure",
        },
        {
            "row_id": "SRC2384_04_667_ansatz",
            "source_key": "667_ansatz",
            "source_path": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
            "needles": ["PBA667_2_boundary_action", "PBA667_4_reference_rule"],
            "source_role": "machine-readable boundary action ansatz",
        },
        {
            "row_id": "SRC2384_05_668_doc",
            "source_key": "668_doc",
            "source_path": POST_ROOT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
            "needles": ["B_ref", "fail_current_claim"],
            "source_role": "sector/boundary-condition lock failure",
        },
        {
            "row_id": "SRC2384_06_668_boundary_lock",
            "source_key": "668_boundary_lock",
            "source_path": RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
            "needles": ["BCL668_1_reference_fixed_branch", "BCL668_6_worldtube_linking_surfaces"],
            "source_role": "reference and surface lock rows",
        },
        {
            "row_id": "SRC2384_07_999_contract",
            "source_key": "999_parent_contract",
            "source_path": RESIDUALS / "P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv",
            "needles": ["FBC999_1_variation_or_constraint", "FBC999_6_MHref_sidecar"],
            "source_role": "parent selector contract requirements",
        },
        {
            "row_id": "SRC2384_08_1001_audit",
            "source_key": "1001_radius_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1001_RADIUS_SURFACE_THEOREM_AUDIT.csv",
            "needles": ["RSA1001_4_reference_charge", "RSA1001_5_theorem_verdict"],
            "source_role": "surface/no-retune audit requirements",
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


def stationarity_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSE2384_0_ansatz_equation",
            "step": "stationarity equation from boundary ansatz",
            "equation": "E_Sigma := delta_{Sigma_ref} int_boundary(B_ref[Sigma_ref]+B_class[chi_B,C_top]+B_ct[Sigma_ref]) = 0",
            "what_is_derived": "This is the exact Euler/stationarity equation a parent boundary action would have to provide.",
            "current_gap": "B_ref[Sigma_ref], B_ct[Sigma_ref] and boundary class functional are named but not explicitly supplied by current MTS.",
            "status": "FORM_DERIVED_FUNCTIONAL_MISSING",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSE2384_1_source_free_derivative",
            "step": "source-free stationarity derivative",
            "equation": "D_source E_Sigma = H_SigmaSigma D_source Sigma_ref + partial_source E_Sigma",
            "what_is_derived": "If the boundary functional contains no source/material/GM/readout inputs, partial_source E_Sigma=0.",
            "current_gap": "no-forbidden-input proof for the actual boundary functional is missing",
            "status": "CONDITIONAL_DERIVATION",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSE2384_2_non_degenerate_solution",
            "step": "nondegenerate reference branch",
            "equation": "H_SigmaSigma^{-1} exists on the quotient by gauge/topological zero modes",
            "what_is_derived": "Then D_source Sigma_ref=0 follows, giving source-blind H_ref/B_ref by 2382.",
            "current_gap": "selector Hessian/operator is not computed because boundary functional is not explicit",
            "status": "CONDITIONAL_NOT_COMPUTABLE_YET",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSE2384_3_sufficient_selector_action",
            "step": "sufficient future parent action clause",
            "equation": "S_sel = 1/2 <F_bc(Sigma_ref;B_class,C_top,tau,e_infty), A F_bc> with A positive and source-free",
            "what_is_derived": "If F_bc=0 fixes the reference data uniquely and A,F_bc are source-free, the selector is source-blind.",
            "current_gap": "S_sel is a sufficient future completion contract, not a current MTS derivation",
            "status": "SUFFICIENT_CONTRACT_NOT_PARENT_OWNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSE2384_4_verdict",
            "step": "current stationarity result",
            "equation": "delta_{Sigma_ref}S_parent_boundary=0",
            "what_is_derived": "The correct stationarity equation and sufficient action contract are now explicit.",
            "current_gap": "current MTS has not supplied the explicit boundary selector functional, Hessian, source-free certificate or M_H_ref",
            "status": "THEOREM_NOT_PROMOTED_RETAIN_SOURCE_PACK",
            "valid_for_claim": no_claim(),
        },
    ]


def selector_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSC2384_0_functional",
            "contract_item": "explicit boundary selector functional",
            "minimum_form": "B_ref[Sigma_ref]+B_ct[Sigma_ref]+B_class[chi_B,C_top] or S_sel[F_bc]",
            "acceptance_test": "functional written in parent variables with source path and equation reference",
            "current_status": "MISSING_FUNCTIONAL",
            "residual_if_missing": "Delta_ref_counterterm_component_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSC2384_1_source_free_inputs",
            "contract_item": "source-free selector input grammar",
            "minimum_form": "inputs only boundary class, topology/cohomology, corner convention, tau/coframe and stationary branch data",
            "acceptance_test": "no source/material/GM/readout/residual labels in functional provenance",
            "current_status": "MISSING_NO_FORBIDDEN_INPUT_CERTIFICATE",
            "residual_if_missing": "selector_forbidden_input_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSC2384_2_hessian",
            "contract_item": "selector Hessian/nondegeneracy",
            "minimum_form": "H_SigmaSigma positive or invertible after quotienting gauge/topological zero modes",
            "acceptance_test": "zero-mode basis declared and no source-dependent flat direction remains",
            "current_status": "MISSING_SELECTOR_HESSIAN",
            "residual_if_missing": "selector_branch_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSC2384_3_surface_lock",
            "contract_item": "surface/domain no-retune",
            "minimum_form": "D_source S0=0; linked surfaces use one parent boundary class; no source crosses annulus",
            "acceptance_test": "surface class id, corner certificate, no-crossed-source and no-retune proof",
            "current_status": "MISSING_SURFACE_LOCK",
            "residual_if_missing": "Delta_ref_surface_component_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSC2384_4_MHref",
            "contract_item": "same-frame M_H_ref",
            "minimum_form": "finite positive M_H_ref with tau_id/frame_id shared by H_ref and Q_tau",
            "acceptance_test": "no orbital-GM import; source path/equation ref/units present",
            "current_status": "MISSING_POSITIVE_MHREF",
            "residual_if_missing": "all normalized Delta_ref rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


def source_pack_fill_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPF2384_0_functional_missing",
            "component": "Delta_ref_functional_gap",
            "formula": "abs(delta_{Sigma_ref}S_boundary_unowned)/M_H_ref",
            "required_fields": "explicit functional or finite residual numerator; units; source path; equation ref; M_H_ref",
            "current_value": "MISSING_BOUNDARY_SELECTOR_FUNCTIONAL;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPF2384_1_hessian_gap",
            "component": "selector_branch_leak",
            "formula": "norm(P_zero D_source Sigma_ref)/M_H_ref",
            "required_fields": "Hessian;zero-mode projector;source derivative;units;M_H_ref",
            "current_value": "MISSING_SELECTOR_HESSIAN;MISSING_ZERO_MODE_PROJECTOR;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPF2384_2_forbidden_input_gap",
            "component": "selector_forbidden_input_leak",
            "formula": "sum_abs(partial_forbidden Sigma_ref * forbidden_scale)/M_H_ref",
            "required_fields": "GM/material/readout/residual derivative audit; scales; units; source paths; M_H_ref",
            "current_value": "MISSING_FORBIDDEN_INPUT_DERIVATIVES;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPF2384_3_surface_gap",
            "component": "Delta_ref_surface_no_retune_gap",
            "formula": "abs(partial_surface_Delta_ref * Delta_surface_profile)/M_H_ref",
            "required_fields": "surface class id;partial surface derivative;profile;corner/no-crossed-source certificate;M_H_ref",
            "current_value": "MISSING_SURFACE_CLASS_ID;MISSING_PARTIAL_SURFACE_DERIVATIVE;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPF2384_4_total",
            "component": "Delta_ref_source_pack_total",
            "formula": "abs(functional_gap)+abs(branch_leak)+abs(forbidden_input_leak)+abs(surface_gap) all divided by M_H_ref",
            "required_fields": "all component numerators; positive same-frame M_H_ref; no-cancellation guard",
            "current_value": "COMPONENTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2384_0_equation_form",
            "decision": "accept stationarity equation form",
            "reason": "667 supplies B_total scaffold, so varying Sigma_ref gives the correct E_Sigma shape",
            "consequence": "the missing object is now explicitly the boundary selector functional/Hessian, not vague reference fixing",
            "status": "EQUATION_FORM_DERIVED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2384_1_no_promotion",
            "decision": "do not promote fixed-reference theorem",
            "reason": "B_ref/B_ct/B_class functionals, source-free certificate, Hessian and M_H_ref remain missing",
            "consequence": "Delta_ref source pack remains live and nonclaim",
            "status": "THEOREM_NOT_PARENT_OWNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": "MTS_R2FR_BOUNDARY_STATIONARITY_EQUATION_FOR_SIGMA_REF_OR_SOURCE_PACK_FILL_2384",
            "row_id": "DEC2384_2_next",
            "decision": "attack explicit selector functional or source-pack values",
            "reason": "the next leap is to instantiate F_bc/S_sel or admit finite Delta_ref components",
            "consequence": "2385 should attempt selector functional construction from relative boundary class; fallback fill source pack",
            "status": "SELECT_2385_SELECTOR_FUNCTIONAL",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2384_0_stationarity_form",
            "gate": "stationarity equation form written",
            "gate_status": "PASS_FORM_ONLY",
            "claim_effect": "valid parent-action target, not proof",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2384_1_explicit_functional",
            "gate": "explicit B_ref/B_ct/B_class or S_sel functional exists",
            "gate_status": "FAIL",
            "claim_effect": "E_Sigma cannot be computed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2384_2_source_free_certificate",
            "gate": "no source/GM/material/readout/residual inputs",
            "gate_status": "FAIL_UNSIGNED",
            "claim_effect": "source-blindness not proved",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2384_3_hessian",
            "gate": "nondegenerate selector Hessian after quotient",
            "gate_status": "FAIL",
            "claim_effect": "branch leak remains",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2384_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "Delta_ref source pack non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2384_5_local_GR_Newton",
            "gate": "local GR/Newton recovery",
            "gate_status": "FAIL_NONCLAIM",
            "claim_effect": "boundary/reference, M_H_ref and source-measure gates remain open",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2384_0_form_equals_proof",
            "claim": "stationarity equation form proves fixed reference",
            "allowed": "false",
            "reason": "the explicit functional, source-free certificate, Hessian and M_H_ref are missing",
            "blocking_rows": "CG2384_1_explicit_functional;CG2384_3_hessian;CG2384_4_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2384_1_add_selector_by_hand",
            "claim": "add S_sel by hand and count it as current MTS",
            "allowed": "false",
            "reason": "S_sel is a sufficient future completion contract unless derived from the existing parent programme",
            "blocking_rows": "BSE2384_3_sufficient_selector_action;BSC2384_0_functional",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2384_2_score_source_pack",
            "claim": "score Delta_ref source pack now",
            "allowed": "false",
            "reason": "component numerators and M_H_ref are still missing",
            "blocking_rows": "SPF2384_0_functional_missing;SPF2384_4_total;CG2384_4_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2384_0_selected",
            "next_file": "2385-Y5-R2FR-selector-functional-from-relative-boundary-class-or-Delta-ref-values.md",
            "success_condition": "construct an explicit source-free F_bc/S_sel or B_ref/B_ct/B_class functional from relative boundary class data and prove nondegenerate source-blindness",
            "fallback_condition": "fill finite Delta_ref source-pack component values with units/source/equation paths and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2384_1_parallel",
            "next_file": "2385b-Y5-R2FR-selector-Hessian-zero-mode-quotient-or-branch-leak-row.md",
            "success_condition": "compute/derive Hessian invertibility after gauge/topological quotient",
            "fallback_condition": "retain selector_branch_leak row",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2384_2_parallel",
            "next_file": "2385c-Y5-R2FR-MHref-sidecar-and-source-measure-equality-priority-gate.md",
            "success_condition": "derive positive same-frame M_H_ref and source-measure equality priority order",
            "fallback_condition": "keep normalized rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2384_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2384_BOUNDARY_STATIONARITY_ATTEMPT.csv": stationarity_attempt_rows,
    "P8_Y5_PARENT_QLOC_2384_SELECTOR_CONTRACT.csv": selector_contract_rows,
    "P8_Y5_PARENT_QLOC_2384_DELTA_REF_SOURCE_PACK_FILL.csv": source_pack_fill_rows,
    "P8_Y5_PARENT_QLOC_2384_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2384_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2384_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2384_NEXT_TARGET.csv": next_target_rows,
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
    add("VAL2384_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2384_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    attempts = stationarity_attempt_rows()
    add(
        "VAL2384_02_stationarity_form_present",
        any(row["row_id"] == "BSE2384_0_ansatz_equation" for row in attempts)
        and any(row["row_id"] == "BSE2384_3_sufficient_selector_action" for row in attempts),
        "stationarity form and sufficient selector-action contract present",
    )
    contracts = selector_contract_rows()
    add(
        "VAL2384_03_contract_gaps_explicit",
        all("MISSING" in row["current_status"] for row in contracts),
        "selector functional/Hessian/surface/MHref gaps explicit",
    )
    pack = source_pack_fill_rows()
    add(
        "VAL2384_04_source_pack_nonready",
        all(row["score_ready"] == "false" for row in pack),
        "Delta_ref source pack remains non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2384_05_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2384_0_stationarity_form"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2384_06_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add("VAL2384_07_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2384_08_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2384_09_next_selected",
        any(row["row_id"] == "NEXT2384_0_selected" for row in next_target_rows()),
        "selector functional construction selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2384_OVERALL",
        overall,
        "2384 writes the boundary stationarity equation form and sufficient selector-action contract, refuses promotion without explicit functional/Hessian/MHref, and stages Delta_ref source pack",
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
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_SOURCE_REGISTER.csv")
    attempts = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_BOUNDARY_STATIONARITY_ATTEMPT.csv")
    contracts = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_SELECTOR_CONTRACT.csv")
    pack = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_DELTA_REF_SOURCE_PACK_FILL.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2384_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2384_VALIDATION.csv")

    body = f"""# 2384 - boundary stationarity equation for Sigma_ref or source-pack fill

## Result

2384 writes the explicit stationarity equation form:

`E_Sigma := delta_{{Sigma_ref}} int_boundary(B_ref[Sigma_ref] + B_class[chi_B,C_top] + B_ct[Sigma_ref]) = 0`.

This is a genuine sharpening: the fixed-reference problem is now an explicit parent boundary-functional problem.  If a
source-free functional exists and its selector Hessian is nondegenerate after quotienting gauge/topological zero modes,
then 2383's implicit-function route gives `D_source Sigma_ref=0`, and 2382 gives `D_source B_ref=D_source H_ref=0`.

But current MTS still has only the 667 ansatz scaffold, not the explicit `B_ref/B_ct/B_class` or `S_sel` functional.
So the theorem is not promoted.  The sufficient selector-action clause
`S_sel = 1/2 <F_bc, A F_bc>` is recorded as a future parent-action contract, not current evidence.

No `Delta_ref=0`, `B_zero_flux=0`, `M_H_ref`, Newton, local-GR, PPN, orbital, clock, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Boundary Stationarity Attempt

{markdown_table(attempts, ["row_id", "step", "equation", "what_is_derived", "current_gap", "status", "valid_for_claim"])}

## Selector Contract

{markdown_table(contracts, ["row_id", "contract_item", "minimum_form", "acceptance_test", "current_status", "residual_if_missing", "valid_for_claim"])}

## Delta Ref Source Pack Fill

{markdown_table(pack, ["row_id", "component", "formula", "required_fields", "current_value", "score_ready", "valid_for_claim"])}

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

This is progress, but not victory.  The equation has been written; the functional has not.  The next non-circling move is
to try to build `F_bc` or `B_ref/B_ct/B_class` from relative boundary class data.  If that cannot be done, the honest
route is to stop trying to zero `Delta_ref` and fill the source-pack rows.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2384_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2384_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
