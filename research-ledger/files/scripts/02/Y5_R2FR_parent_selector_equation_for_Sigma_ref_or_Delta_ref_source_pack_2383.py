from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PARENT_SELECTOR_EQUATION_FOR_SIGMA_REF_OR_DELTA_REF_SOURCE_PACK_2383"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2383-Y5-R2FR-parent-selector-equation-for-Sigma-ref-or-Delta-ref-source-pack.md"
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
            "row_id": "SRC2383_00_2382_doc",
            "source_key": "2382_doc",
            "source_path": POST_ROOT / "2382-Y5-R2FR-fixed-boundary-class-and-Href-selector-or-Delta-ref-row.md",
            "needles": ["parent equation that fixes `Sigma_ref`", "D_source Sigma_ref = 0"],
            "source_role": "2382 selected parent selector equation as next target",
        },
        {
            "row_id": "SRC2383_01_2382_theorem",
            "source_key": "2382_theorem",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv",
            "needles": ["FRT2382_2_source_blind_chain_rule", "THEOREM_NOT_PROMOTED_RETAIN_DELTA_REF_ROW"],
            "source_role": "source-blind chain-rule theorem and nonpromotion gate",
        },
        {
            "row_id": "SRC2383_02_2382_grammar",
            "source_key": "2382_grammar",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2382_SELECTOR_INPUT_GRAMMAR.csv",
            "needles": ["SIG2382_4_observed_GM", "SIG2382_6_residual_sign"],
            "source_role": "allowed/forbidden selector input grammar",
        },
        {
            "row_id": "SRC2383_03_999_doc",
            "source_key": "999_doc",
            "source_path": POST_ROOT / "999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md",
            "needles": ["what parent rule forces the reference branch before source/readout exists?", "MISSING_SELECTOR_EQUATION"],
            "source_role": "older fixed-branch selector equation gap",
        },
        {
            "row_id": "SRC2383_04_999_parent_contract",
            "source_key": "999_parent_contract",
            "source_path": RESIDUALS / "P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv",
            "needles": ["FBC999_1_variation_or_constraint", "FBC999_6_MHref_sidecar"],
            "source_role": "parent action selector contract rows",
        },
        {
            "row_id": "SRC2383_05_999_selector_attempt",
            "source_key": "999_selector_attempt",
            "source_path": RESIDUALS / "P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv",
            "needles": ["FBS999_1_parent_variational_owner", "FBS999_7_verdict"],
            "source_role": "fixed-branch selector attempt failure rows",
        },
        {
            "row_id": "SRC2383_06_1000_schema",
            "source_key": "1000_schema",
            "source_path": RESIDUALS / "P8_Y5_R10_1000_STRICT_INPUT_SCHEMA.csv",
            "needles": ["SIS1000_0_partial_source_Delta_ref", "SIS1000_2_Bref_rule", "SIS1000_3_MHref"],
            "source_role": "fallback Delta_ref source-pack schema",
        },
        {
            "row_id": "SRC2383_07_1001_radius_audit",
            "source_key": "1001_radius_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1001_RADIUS_SURFACE_THEOREM_AUDIT.csv",
            "needles": ["RSA1001_1_surface_class", "RSA1001_5_theorem_verdict"],
            "source_role": "surface-domain selector no-retune blocker",
        },
        {
            "row_id": "SRC2383_08_545_doc",
            "source_key": "545_doc",
            "source_path": POST_ROOT / "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
            "needles": ["reference choice remains a contract", "not a parent result"],
            "source_role": "minimal reference action contract not parent-owned",
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


def implicit_selector_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "IST2383_0_setup",
            "step": "selector equation setup",
            "statement": "Let E_Sigma(Sigma_ref; B_class, C_top, tau, e_infty)=0 be the parent boundary/reference selector equation.",
            "condition": "E_Sigma contains no source/material/GM/readout/residual inputs",
            "result": "Sigma_ref is selected by parent structural data, not by fit",
            "missing_in_current_corpus": "explicit E_Sigma equation and source path",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IST2383_1_source_free_equation",
            "step": "source-free equation derivative",
            "statement": "D_source E_Sigma = (partial E_Sigma/partial Sigma_ref) D_source Sigma_ref + partial_source E_Sigma.",
            "condition": "partial_source E_Sigma=0 because no forbidden source inputs appear",
            "result": "Hessian/operator times D_source Sigma_ref is zero",
            "missing_in_current_corpus": "no-marker/no-GM/no-readout certificate for E_Sigma",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IST2383_2_non_degeneracy",
            "step": "implicit function nondegeneracy",
            "statement": "If partial E_Sigma/partial Sigma_ref is invertible on the allowed boundary class after gauge/topological zero modes are quotiented, then D_source Sigma_ref=0.",
            "condition": "selector Hessian/operator has no source-dependent flat branch or uncontrolled zero mode",
            "result": "source-blindness follows from the implicit function theorem",
            "missing_in_current_corpus": "nondegeneracy/unique-branch certificate",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IST2383_3_reference_zero",
            "step": "Delta_ref source component",
            "statement": "D_source Sigma_ref=0 implies D_source B_ref=0 and D_source H_ref=0 by the 2382 chain-rule criterion.",
            "condition": "same selector controls B_ref, H_ref, surface S0 and counterterm B_ct",
            "result": "partial_source Delta_ref=0 conditionally",
            "missing_in_current_corpus": "parent-owned Sigma_ref and counterterm/surface provenance",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IST2383_4_failure_modes",
            "step": "failure modes",
            "statement": "If E_Sigma contains source labels, GM calibration, post-readout residual data, moving surfaces, or degenerate branch choices, the theorem fails.",
            "condition": "none",
            "result": "Delta_ref components must be source-packed rather than zeroed",
            "missing_in_current_corpus": "finite component numerators and M_H_ref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IST2383_5_verdict",
            "step": "current verdict",
            "statement": "The implicit-function route is mathematically sharp but not parent-signed in current MTS.",
            "condition": "E_Sigma source-free plus nondegenerate branch certificate are not present",
            "result": "selector equation theorem is not promoted; Delta_ref source pack remains required",
            "missing_in_current_corpus": "E_Sigma, no-forbidden-input proof, nondegeneracy certificate, M_H_ref",
            "valid_for_claim": no_claim(),
        },
    ]


def selector_equation_candidate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEC2383_0_boundary_stationarity",
            "candidate_equation": "delta_{Sigma_ref} S_parent_boundary = 0",
            "allowed_inputs": "boundary class, tau, coframe, corner/topology data",
            "forbidden_inputs": "source labels, observed GM, fitted mass, residual value",
            "current_status": "CANDIDATE_NOT_IN_CORPUS",
            "would_close": "FRT2382 source-blindness if source-free and nondegenerate",
            "fallback": "Delta_ref_counterterm_component_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEC2383_1_Ward_charge_lock",
            "candidate_equation": "Ward/diffeomorphism charge normalization fixes reference branch",
            "allowed_inputs": "generator tau, asymptotic symmetry class, boundary orientation",
            "forbidden_inputs": "measured source charge before Hilbert/topological equality",
            "current_status": "CANDIDATE_NOT_IN_CORPUS",
            "would_close": "pre-readout H_ref selector",
            "fallback": "R_eq/I_commutator remain parallel",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEC2383_2_topological_selector",
            "candidate_equation": "C_top(Sigma_ref)=C_top^0 with fixed relative cohomology class",
            "allowed_inputs": "topological class and boundary homology",
            "forbidden_inputs": "material/source composition or orbital normalization",
            "current_status": "CANDIDATE_PARTIAL_ONLY",
            "would_close": "topological part of selector if also unique and same-frame",
            "fallback": "epsilon_top_abs and Delta_ref_surface_component_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEC2383_3_stationary_vacuum_reference",
            "candidate_equation": "reference branch is the unique source-free stationary solution in the same boundary class",
            "allowed_inputs": "zero-source stationary branch and asymptotic coframe",
            "forbidden_inputs": "using reference-only zero as evidence for current source branch",
            "current_status": "CANDIDATE_RISKY_UNOWNED",
            "would_close": "reference selector if uniqueness and no source retuning are proved",
            "fallback": "reference-only zero refused; Delta_ref source pack",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEC2383_4_verdict",
            "candidate_equation": "current MTS parent selector equation",
            "allowed_inputs": "source-free parent structural data",
            "forbidden_inputs": "all source/readout/calibration labels",
            "current_status": "NOT_DERIVED",
            "would_close": "none yet",
            "fallback": "source-pack Delta_ref components",
            "valid_for_claim": no_claim(),
        },
    ]


def delta_ref_source_pack_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP2383_0_source_derivative",
            "component": "partial_source_Delta_ref",
            "formula": "finite derivative or theorem_zero=true with PARENT_SIGNED_SELECTOR_TRUE",
            "required_fields": "source_parameter;derivative_value;units;source_path;equation_ref;extraction_method",
            "current_value": "MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO",
            "status": "REQUIRED_IF_SELECTOR_THEOREM_FAILS",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP2383_1_selector_hessian",
            "component": "selector_non_degeneracy_or_branch_leak",
            "formula": "norm(Psi_zero_mode_or_branch_drift)/M_H_ref or theorem_zero via invertible Hessian",
            "required_fields": "Hessian/operator;gauge quotient;zero_mode_basis;branch_id;source_path",
            "current_value": "MISSING_SELECTOR_HESSIAN",
            "status": "REQUIRED_FOR_IMPLICIT_THEOREM",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP2383_2_forbidden_input_audit",
            "component": "selector_forbidden_input_leak",
            "formula": "sum_abs(partial_forbidden Sigma_ref * forbidden_scale)/M_H_ref",
            "required_fields": "GM/material/residual/readout derivatives;scales;units;source paths",
            "current_value": "MISSING_FORBIDDEN_INPUT_DERIVATIVES",
            "status": "REQUIRED_IF_NO_MARKER_PROOF_FAILS",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP2383_3_total",
            "component": "Delta_ref_source_pack_total",
            "formula": "abs(partial_source_Delta_ref*Delta_source_scale)/M_H_ref + selector_branch_leak + forbidden_input_leak",
            "required_fields": "all component values;positive same-frame M_H_ref;absolute no-cancellation guard",
            "current_value": "COMPONENTS_MISSING",
            "status": "NONCLAIM_SOURCE_PACK_STAGED",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2383_0_math_gain",
            "decision": "keep implicit-function selector theorem as the right route",
            "reason": "a source-free nondegenerate parent selector equation would prove D_source Sigma_ref=0 instead of assuming it",
            "consequence": "fixed-reference problem is now an equation/nondegeneracy target, not a vague convention",
            "status": "CONDITIONAL_THEOREM_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2383_1_no_promotion",
            "decision": "do not promote fixed-reference theorem",
            "reason": "current corpus lacks E_Sigma, no-forbidden-input proof, nondegenerate branch certificate and M_H_ref",
            "consequence": "Delta_ref source pack remains live",
            "status": "THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2383_2_next",
            "decision": "attack boundary stationarity equation or source-pack Delta_ref",
            "reason": "SEC2383_0 is the least hand-wavy parent-action route; if it cannot be written, source-pack is the honest fallback",
            "consequence": "2384 should try to write delta_{Sigma_ref}S_boundary=0 explicitly or fill source-pack inputs",
            "status": "SELECT_2384_BOUNDARY_STATIONARITY",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2383_0_implicit_selector_route",
            "gate": "implicit-function source-blindness theorem shape",
            "gate_status": "PASS_CONDITIONAL_SHAPE_ONLY",
            "claim_effect": "valid target for future parent action",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2383_1_Esigma",
            "gate": "explicit parent selector equation E_Sigma=0",
            "gate_status": "FAIL",
            "claim_effect": "D_source Sigma_ref not proved",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2383_2_non_degeneracy",
            "gate": "nondegenerate unique reference branch after quotienting gauge/topological zero modes",
            "gate_status": "FAIL",
            "claim_effect": "branch drift can source Delta_ref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2383_3_no_forbidden_inputs",
            "gate": "selector equation has no source/GM/material/readout/residual inputs",
            "gate_status": "FAIL_UNSIGNED",
            "claim_effect": "source-blindness remains conditional",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2383_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "Delta_ref source pack cannot be scored",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2383_5_local_GR_Newton",
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
            "row_id": "REF2383_0_assume_selector",
            "claim": "assume Sigma_ref is source-blind without E_Sigma",
            "allowed": "false",
            "reason": "2383 derives the route but requires the parent equation and nondegeneracy certificate",
            "blocking_rows": "IST2383_0_setup;IST2383_2_non_degeneracy;CG2383_1_Esigma",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2383_1_degenerate_branch",
            "claim": "use a degenerate reference branch and still declare D_source Sigma_ref=0",
            "allowed": "false",
            "reason": "zero modes/branch drift can carry source dependence unless quotient/nondegeneracy is proved",
            "blocking_rows": "IST2383_2_non_degeneracy;DSP2383_1_selector_hessian",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2383_2_source_pack_score",
            "claim": "score Delta_ref source pack now",
            "allowed": "false",
            "reason": "component numerators, source scales, Hessian, forbidden-input derivatives and M_H_ref are missing",
            "blocking_rows": "DSP2383_0_source_derivative;DSP2383_1_selector_hessian;DSP2383_3_total;CG2383_4_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2383_0_selected",
            "next_file": "2384-Y5-R2FR-boundary-stationarity-equation-for-Sigma-ref-or-source-pack-fill.md",
            "success_condition": "write an explicit source-free delta_{Sigma_ref} S_parent_boundary=0 equation and nondegeneracy/no-forbidden-input certificate",
            "fallback_condition": "fill Delta_ref source-pack component rows with finite numerators, units, source paths and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2383_1_parallel",
            "next_file": "2384b-Y5-R2FR-selector-Hessian-zero-modes-or-branch-leak-row.md",
            "success_condition": "prove the selector Hessian is invertible after quotienting gauge/topological zero modes",
            "fallback_condition": "retain selector_branch_leak nonclaim component",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2383_2_parallel",
            "next_file": "2384c-Y5-R2FR-same-frame-MHref-sidecar-or-denominator-row.md",
            "success_condition": "derive positive same-frame M_H_ref needed to score every normalized row",
            "fallback_condition": "keep normalized local residuals non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2383_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2383_IMPLICIT_SELECTOR_THEOREM.csv": implicit_selector_theorem_rows,
    "P8_Y5_PARENT_QLOC_2383_SELECTOR_EQUATION_CANDIDATES.csv": selector_equation_candidate_rows,
    "P8_Y5_PARENT_QLOC_2383_DELTA_REF_SOURCE_PACK.csv": delta_ref_source_pack_rows,
    "P8_Y5_PARENT_QLOC_2383_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2383_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2383_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2383_NEXT_TARGET.csv": next_target_rows,
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
    add("VAL2383_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2383_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = implicit_selector_theorem_rows()
    add(
        "VAL2383_02_implicit_theorem_present",
        any(row["row_id"] == "IST2383_2_non_degeneracy" for row in theorem)
        and any(row["row_id"] == "IST2383_3_reference_zero" for row in theorem),
        "implicit-function nondegeneracy and reference-zero rows present",
    )
    candidates = selector_equation_candidate_rows()
    add(
        "VAL2383_03_stationarity_candidate_present",
        any(row["row_id"] == "SEC2383_0_boundary_stationarity" for row in candidates),
        "boundary stationarity candidate selected",
    )
    pack = delta_ref_source_pack_rows()
    add(
        "VAL2383_04_source_pack_nonready",
        all(row["score_ready"] == "false" for row in pack),
        "Delta_ref source pack rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2383_05_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2383_0_implicit_selector_route"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2383_06_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add("VAL2383_07_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2383_08_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2383_09_next_selected",
        any(row["row_id"] == "NEXT2383_0_selected" for row in next_target_rows()),
        "boundary stationarity equation selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2383_OVERALL",
        overall,
        "2383 derives the implicit-function selector route, refuses promotion without E_Sigma/nondegeneracy/MHref, and selects boundary stationarity next",
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
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_IMPLICIT_SELECTOR_THEOREM.csv")
    candidates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_SELECTOR_EQUATION_CANDIDATES.csv")
    pack = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_DELTA_REF_SOURCE_PACK.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2383_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2383_VALIDATION.csv")

    body = f"""# 2383 - parent selector equation for Sigma_ref or Delta-ref source pack

## Result

2383 takes the leap from "the selector must be source-blind" to the actual mathematical route that could make it true.

If a parent boundary/reference equation

`E_Sigma(Sigma_ref; B_class, C_top, tau, e_infty) = 0`

contains no source/material/GM/readout/residual inputs, then differentiating with respect to source gives

`(partial E_Sigma / partial Sigma_ref) D_source Sigma_ref + partial_source E_Sigma = 0`.

If `partial_source E_Sigma=0` and the selector Hessian/operator is invertible after quotienting gauge/topological zero
modes, the implicit-function theorem gives `D_source Sigma_ref=0`.  Then 2382's chain rule gives
`D_source B_ref=D_source H_ref=0`.

That is a serious theorem shape.  But current MTS does **not** yet provide `E_Sigma`, the no-forbidden-input proof, the
nondegeneracy certificate, or positive same-frame `M_H_ref`.  So no fixed-reference, `Delta_ref=0`, Newton, local-GR, or
public claim follows.  The fallback `Delta_ref` source pack remains live.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Implicit Selector Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "condition", "result", "missing_in_current_corpus", "valid_for_claim"])}

## Selector Equation Candidates

{markdown_table(candidates, ["row_id", "candidate_equation", "allowed_inputs", "forbidden_inputs", "current_status", "would_close", "fallback", "valid_for_claim"])}

## Delta Ref Source Pack

{markdown_table(pack, ["row_id", "component", "formula", "required_fields", "current_value", "status", "score_ready", "valid_for_claim"])}

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

This is a proper forward step.  We are no longer merely demanding that `H_ref` be fixed; we now have the exact parent
selector equation route and the mathematical proof shape that would make source-blindness follow.  The monster is still
alive because `E_Sigma` is not written, but it has a neck now.

Next best strike: `2384`, try to write `delta_{{Sigma_ref}} S_parent_boundary = 0` explicitly.  If that cannot be done,
stop pretending and fill the `Delta_ref` source pack.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2383_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2383_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
