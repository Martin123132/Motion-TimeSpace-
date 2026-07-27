from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1597"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md"

SOURCE_FILES = {
    "1596_doc": ROOT / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
    "1596_validation": OUT / "P8_Y5_BRR545_1596_VALIDATION.csv",
    "1596_contraction_law": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv",
    "1596_tau_factor_audit": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv",
    "1596_action_last_gate": OUT / "P8_Y5_PARENT_QLOC_1596_ACTION_MEASURE_OWNER_LAST_GATE.csv",
    "1596_delta_w_status": OUT / "P8_Y5_PARENT_QLOC_1596_DELTA_W_BOUND_STATUS.csv",
    "1596_tau_acquisition": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv",
    "1596_next_target": OUT / "P8_Y5_PARENT_QLOC_1596_NEXT_TARGET.csv",
    "1595_candidate": OUT / "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv",
    "1083_source_caveat": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1482_tau_readiness": OUT / "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv",
}

NEEDLES = {
    "1596_doc": ["NEXT_1597_TAU_LOWER_BOUND_OR_COUPLING_ZERO_PROOF", "tau_min"],
    "1596_validation": ["VAL1596_OVERALL", "PASS"],
    "1596_contraction_law": ["TCL1596_2_delta_w_amplitude_law", "tau_min > 0"],
    "1596_tau_factor_audit": ["TFA1596_4_readout_matrix", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1596_action_last_gate": ["AMG1596_3_last_gate_verdict", "ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED"],
    "1596_delta_w_status": ["DWB1596_3_delta_w_bound", "SYMBOLIC_ONLY_NO_NUMERIC_DELTA_W"],
    "1596_tau_acquisition": ["TSA1596_3_tau_min", "strictly positive"],
    "1596_next_target": ["1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof", "tau_min>0"],
    "1595_candidate": ["SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor", "2.8e-15"],
    "1083_source_caveat": ["SCG1083_0_profile_weighting", "MISSING_SOURCE_PROFILE_WEIGHTING"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1482_tau_readiness": ["TAU1482_7_numeric_tau", "NOT_EVALUATED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1597_SOURCE_REGISTER.csv"
TAU_LOWER_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1597_TAU_LOWER_BOUND_THEOREM_AUDIT.csv"
NULL_COUNTERMODEL = OUT / "P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv"
COUPLING_ZERO_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1597_COUPLING_ZERO_PROOF_AUDIT.csv"
WEP_PRODUCT_STATUS = OUT / "P8_Y5_PARENT_QLOC_1597_WEP_PRODUCT_BRANCH_STATUS.csv"
NONDEGEN_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1597_REQUIRED_NONDEGENERACY_INPUTS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1597_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1597_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1597_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1597_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1597_VALIDATION.csv"

COPY_TARGETS = {
    TAU_LOWER_THEOREM: [
        QUARANTINE / "TAU_LOWER_BOUND_THEOREM_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_tau_lower_bound_theorem_audit_nonclaim_1597.csv",
    ],
    NULL_COUNTERMODEL: [
        QUARANTINE / "NULL_SPACE_COUNTERMODEL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_null_space_countermodel_nonclaim_1597.csv",
    ],
    COUPLING_ZERO_AUDIT: [
        QUARANTINE / "COUPLING_ZERO_PROOF_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_coupling_zero_proof_audit_nonclaim_1597.csv",
    ],
    WEP_PRODUCT_STATUS: [
        QUARANTINE / "WEP_PRODUCT_BRANCH_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_wep_product_branch_status_nonclaim_1597.csv",
    ],
    NONDEGEN_INPUTS: [
        QUARANTINE / "REQUIRED_NONDEGENERACY_INPUTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_required_nondegeneracy_inputs_nonclaim_1597.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1597.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1597_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1597_tau_lower_bound_or_coupling_zero_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def tau_lower_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "TLB1597_0_projection_definition",
            "statement": "tau_WEP = N_eta^{-1} <K_CMSM, S_Earth x M_TiPt> in the branch-locked linear readout convention",
            "needed_condition": "N_eta finite and nonzero; K_CMSM, S_Earth, M_TiPt in same convention",
            "current_status": "FORMAL_PAIRING_ONLY",
            "result": "DEFINITION_SHARPENED_NOT_EVALUATED",
            "source": "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv:TCL1596_0_linearized_observable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "TLB1597_1_sufficient_lower_bound",
            "statement": "if ||K_CMSM||>=k_min, ||S_Earth||>=s_min, ||M_TiPt||>=m_min, |cos(theta)|>=c_min>0 and N_eta<=N_max then |tau_WEP|>=k_min*s_min*m_min*c_min/N_max",
            "needed_condition": "positive norm lower bounds plus a positive alignment/non-null bound",
            "current_status": "CONDITIONAL_THEOREM_DERIVED",
            "result": "TAU_MIN_REQUIRES_ALIGNMENT_NOT_JUST_NONZERO_FACTORS",
            "source": "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv:TSA1596_3_tau_min",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "TLB1597_2_norms_insufficient",
            "statement": "nonzero source, material and readout factors do not imply nonzero tau_WEP because the readout pairing can be orthogonal to the source-material vector",
            "needed_condition": "exclude kernel/orthogonality by source data or parent theorem",
            "current_status": "NO_SHORTCUT_LEMMA_DERIVED",
            "result": "GENERIC_TAU_MIN_NOT_PROVEN",
            "source": "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv:TFA1596_0_to_TFA1596_6",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "TLB1597_3_current_corpus_verdict",
            "statement": "current corpus lacks K_CMSM, source worldtube, material response tensor, product normalization and alignment proof",
            "needed_condition": "official data import or parent nondegeneracy theorem",
            "current_status": "TAU_LOWER_BOUND_NOT_DERIVED",
            "result": "NO_NUMERIC_TAU_MIN",
            "source": "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def null_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "NSC1597_0_linear_space_model",
            "construction": "Let K be a nonzero linear readout functional and let V=S_Earth x M_TiPt be nonzero but chosen in ker(K).",
            "math_result": "<K,V>=0 while K!=0 and V!=0",
            "meaning": "tau_WEP can vanish even with nonzero source/material/readout objects",
            "blocked_claim": "generic tau_min>0",
            "escape_condition": "prove V not in ker(K), or import data showing the branch-locked V has nonzero readout projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "NSC1597_1_cancellation_model",
            "construction": "Allow shell/orbit/readout contributions with opposite signs and no signed material model.",
            "math_result": "positive and negative pieces can cancel in the orbit average",
            "meaning": "bulk-source positivity does not imply tau_WEP positivity after readout projection",
            "blocked_claim": "tau_WEP lower bound from bulk composition alone",
            "escape_condition": "sourced signed kernel plus no-cancellation or absolute-response theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "NSC1597_2_measured_G_absorption_guard",
            "construction": "If a common-mode source response is absorbed into measured G, only relative residuals remain visible.",
            "math_result": "absorption cannot establish tau_min for the differential channel",
            "meaning": "measured-G renormalization is not a proof of local-GR reduction",
            "blocked_claim": "local-GR pass from hiding source response",
            "escape_condition": "derive zero residual, or bound the differential residual directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def coupling_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CZP1597_0_delta_w_zero_route",
            "target": "Delta_w_TiPt=0",
            "required_statement": "Ti and Pt matter actions descend through the same parent action measure with no representative source weights",
            "current_status": "ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED",
            "result": "ZERO_PROOF_NOT_AVAILABLE",
            "source": "P8_Y5_PARENT_QLOC_1596_ACTION_MEASURE_OWNER_LAST_GATE.csv:AMG1596_3_last_gate_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CZP1597_1_current_owner_limit",
            "target": "remove pre-variation w_A",
            "required_statement": "current/source ownership must act before variation, not just after equations of motion",
            "current_status": "CURRENT_OWNER_INSUFFICIENT",
            "result": "POST_VARIATION_ROUTE_DOES_NOT_KILL_COUPLING",
            "source": "P8_Y5_PARENT_QLOC_1596_ACTION_MEASURE_OWNER_LAST_GATE.csv:AMG1596_1_current_owner_theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CZP1597_2_coupling_zero_verdict",
            "target": "coupling/source-weight zero theorem",
            "required_statement": "parent symmetry or quotient descent forbids all finite relative matter weights",
            "current_status": "COUPLING_ZERO_PROOF_NOT_DERIVED",
            "result": "FINITE_PRODUCT_BRANCH_REMAINS_OPEN",
            "source": "CZP1597_0_delta_w_zero_route;CZP1597_1_current_owner_limit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def wep_product_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "WPS1597_0_product_bound",
            "quantity": "abs(Delta_w_TiPt*tau_WEP)",
            "status": "SOURCE_BACKED_BOUND_ANCHOR_RETAINED",
            "value_or_formula": "<= 2.8e-15",
            "what_it_allows": "private bound-only bookkeeping",
            "what_it_does_not_allow": "no Delta_w number, no WEP pass, no local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "WPS1597_1_delta_w",
            "quantity": "abs(Delta_w_TiPt)",
            "status": "BLOCKED_BY_NO_TAU_MIN",
            "value_or_formula": "if tau_min>0 then <=2.8e-15/tau_min",
            "what_it_allows": "conditional amplitude law only",
            "what_it_does_not_allow": "no numeric Delta_w bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "WPS1597_2_zero_route",
            "quantity": "Delta_w_TiPt=0",
            "status": "BLOCKED_BY_NO_PARENT_COUPLING_ZERO_PROOF",
            "value_or_formula": "not derived",
            "what_it_allows": "target for parent action work",
            "what_it_does_not_allow": "no zero theorem claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def nondegeneracy_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "NDI1597_0_K_norm",
            "needed_input": "k_min lower bound for official K_CMSM readout functional",
            "why_needed": "readout must be nonzero in the branch-locked channel",
            "source_route": "official MICROSCOPE readout/design matrix",
            "status": "MISSING",
            "priority": "highest",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "NDI1597_1_source_norm",
            "needed_input": "s_min lower bound for Earth source-weight vector",
            "why_needed": "source object must be nonzero in the same convention",
            "source_route": "source worldtube/profile import or parent source theorem",
            "status": "MISSING",
            "priority": "highest",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "NDI1597_2_material_norm",
            "needed_input": "m_min lower bound for Ti/Pt material response difference",
            "why_needed": "test-pair vector must be nonzero in the finite source-weight channel",
            "source_route": "material response tensor or parent matter-action map",
            "status": "MISSING",
            "priority": "high",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "NDI1597_3_alignment",
            "needed_input": "c_min lower bound for |cos(theta)| between readout functional and source-material vector",
            "why_needed": "this is what excludes the null-space countermodel",
            "source_route": "official data computation or parent nondegeneracy theorem",
            "status": "MISSING_CRITICAL",
            "priority": "highest",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "NDI1597_4_normalization",
            "needed_input": "N_max upper bound and sign/absolute convention for eta normalization",
            "why_needed": "turns pairing lower bound into dimensionless tau_min",
            "source_route": "MICROSCOPE product convention/readout normalization",
            "status": "MISSING",
            "priority": "high",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1597_0_tau_min",
            "acceptance_rule": "tau_min requires positive alignment/non-null proof or sourced data",
            "input_state": "no K/source/material/alignment/normalization inputs",
            "runner_result": "REJECT_TAU_MIN_CLAIM",
            "effect": "Delta_w remains unbounded numerically",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1597_1_null_countermodel",
            "acceptance_rule": "if countermodel exists, generic tau lower-bound theorem fails",
            "input_state": "nonzero vector may sit in readout kernel",
            "runner_result": "ACCEPT_BLOCKING_COUNTERMODEL",
            "effect": "official data or parent nondegeneracy proof required",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1597_2_coupling_zero",
            "acceptance_rule": "coupling zero requires parent action-measure/matter descent proof",
            "input_state": "last gate not closed",
            "runner_result": "REJECT_COUPLING_ZERO_CLAIM",
            "effect": "finite source-weight branch retained",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1597_0_tau_min", "tau_WEP lower bound exists", "blocked by null-space countermodel and missing data"),
        ("CG1597_1_delta_w", "numeric Delta_w_TiPt bound exists", "blocked by no tau_min"),
        ("CG1597_2_zero", "Delta_w_TiPt=0 theorem", "blocked by no parent coupling/action-measure proof"),
        ("CG1597_3_wep", "MTS passes WEP/MICROSCOPE", "blocked; product anchor only"),
        ("CG1597_4_local_gr", "derived local GR branch", "blocked; coupling/source residual remains open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": "BLOCKED",
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1597_0_tau_min",
            "decision": "TAU_MIN_NOT_DERIVED",
            "reason": "nonzero factors do not exclude readout-kernel orthogonality",
            "next_action": "import official readout/source data or derive parent nondegeneracy",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1597_1_coupling_zero",
            "decision": "COUPLING_ZERO_NOT_DERIVED",
            "reason": "action-measure owner still fails at pre-variation w_A",
            "next_action": "continue zero theorem only if parent action package can be supplied",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1597_2_best_route",
            "decision": "NEXT_1598_OFFICIAL_READOUT_OR_PARENT_NONDEGENERACY",
            "reason": "the theorem route now needs exactly the same nondegeneracy object the data route would compute",
            "next_action": "build official MICROSCOPE readout/source import gate, or prove K not orthogonal to branch source vector",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1598-Y5-R2FR-official-MICROSCOPE-readout-or-parent-nondegeneracy.md",
            "script": "scripts/Y5_R2FR_official_MICROSCOPE_readout_or_parent_nondegeneracy.py",
            "objective": "either import/source the official readout/source objects needed to compute tau_WEP, or prove a parent nondegeneracy theorem excluding the readout-kernel null case",
            "success_condition": "a sourced nonzero projection/alignment row, or a parent theorem that forces c_min>0; otherwise keep WEP product-bound only",
            "do_not": "do not use tau_WEP=1, surrogate-only readout matrices, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for src, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    truthy = {"true", "1", "yes", "y"}
    fields = {"score_ready", "valid_prediction_row", "claim_allowed"}
    for path in paths:
        for row in read_csv(path):
            for field in fields:
                if row.get(field, "").strip().lower() in truthy:
                    return False
    return True


def no_formalization_1597() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1597*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    theorem = read_csv(TAU_LOWER_THEOREM)
    nulls = read_csv(NULL_COUNTERMODEL)
    coupling = read_csv(COUPLING_ZERO_AUDIT)
    status = read_csv(WEP_PRODUCT_STATUS)
    inputs = read_csv(NONDEGEN_INPUTS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1597_0_sources_exist", all(row["exists"] == "True" or row["exists"] is True for row in sources), "all cited 1597 source paths exist"),
        ("VAL1597_1_needles_found", all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources), "all required 1597 source needles found"),
        ("VAL1597_2_conditional_tau_bound", any(row["theorem_id"] == "TLB1597_1_sufficient_lower_bound" and "c_min>0" in row["statement"] for row in theorem), "conditional tau lower-bound theorem recorded"),
        ("VAL1597_3_norms_insufficient", any(row["theorem_id"] == "TLB1597_2_norms_insufficient" for row in theorem), "nonzero norms insufficient lemma recorded"),
        ("VAL1597_4_null_countermodel", any(row["countermodel_id"] == "NSC1597_0_linear_space_model" and "ker(K)" in row["construction"] for row in nulls), "readout-kernel countermodel recorded"),
        ("VAL1597_5_coupling_zero_blocked", any(row["proof_id"] == "CZP1597_2_coupling_zero_verdict" and row["result"] == "FINITE_PRODUCT_BRANCH_REMAINS_OPEN" for row in coupling), "coupling zero proof remains blocked"),
        ("VAL1597_6_product_branch_only", any(row["status_id"] == "WPS1597_0_product_bound" for row in status), "WEP product anchor retained only"),
        ("VAL1597_7_alignment_input_required", any(row["input_id"] == "NDI1597_3_alignment" and row["status"] == "MISSING_CRITICAL" for row in inputs), "alignment/non-null input required"),
        ("VAL1597_8_runner_blocks_tau_min", any(row["runner_id"] == "RUN1597_0_tau_min" and row["runner_result"] == "REJECT_TAU_MIN_CLAIM" for row in runner), "runner rejects tau_min claim"),
        ("VAL1597_9_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1597 claim gates remain closed"),
        ("VAL1597_10_decision_next", any(row["decision"] == "NEXT_1598_OFFICIAL_READOUT_OR_PARENT_NONDEGENERACY" for row in decisions), "decision selects 1598 official readout/parent nondegeneracy"),
        ("VAL1597_11_csv_parse", csv_parses(generated_csvs), "all generated 1597 CSVs parse"),
        ("VAL1597_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1597 rows are score-ready, prediction rows, or claim-allowed"),
        ("VAL1597_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1597_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1597_15_formalization_untouched", no_formalization_1597(), "no 1597 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1597_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1597 tau lower-bound or coupling-zero proof validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    nulls: list[dict[str, Any]],
    coupling: list[dict[str, Any]],
    status: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1597 - R2/fR tau Lower Bound Or Coupling Zero Proof",
                "## Verdict\n"
                "- 1597 derives the precise `tau_min` condition: a usable lower bound needs nonzero readout, source and material norms **plus** a positive alignment/non-null bound.\n"
                "- Nonzero factors alone do not prove `tau_WEP != 0`; the source-material vector can sit in the readout kernel, giving `tau_WEP=0` while every component is nonzero.\n"
                "- The coupling-zero route also remains open: the parent action-measure package still has not killed pre-variation `w_A`.\n"
                "- Therefore the MICROSCOPE row remains a source-backed product bound only: `abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15`.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## tau Lower-Bound Theorem Audit",
                md_table(theorem, ["theorem_id", "statement", "current_status", "result"]),
                "## Null-Space Countermodel",
                md_table(nulls, ["countermodel_id", "construction", "math_result", "meaning", "escape_condition"]),
                "## Coupling Zero Proof Audit",
                md_table(coupling, ["proof_id", "target", "current_status", "result"]),
                "## WEP Product Branch Status",
                md_table(status, ["status_id", "quantity", "status", "value_or_formula", "what_it_does_not_allow"]),
                "## Required Nondegeneracy Inputs",
                md_table(inputs, ["input_id", "needed_input", "why_needed", "source_route", "status", "priority"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = tau_lower_theorem_rows()
    nulls = null_countermodel_rows()
    coupling = coupling_zero_rows()
    status = wep_product_status_rows()
    inputs = nondegeneracy_input_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        TAU_LOWER_THEOREM,
        NULL_COUNTERMODEL,
        COUPLING_ZERO_AUDIT,
        WEP_PRODUCT_STATUS,
        NONDEGEN_INPUTS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(TAU_LOWER_THEOREM, theorem)
    write_csv(NULL_COUNTERMODEL, nulls)
    write_csv(COUPLING_ZERO_AUDIT, coupling)
    write_csv(WEP_PRODUCT_STATUS, status)
    write_csv(NONDEGEN_INPUTS, inputs)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, nulls, coupling, status, inputs, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
