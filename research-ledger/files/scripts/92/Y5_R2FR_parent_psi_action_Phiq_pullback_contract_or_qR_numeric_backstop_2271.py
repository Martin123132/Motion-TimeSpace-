from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_PSI_ACTION_PHIQ_PULLBACK_CONTRACT_2271"
DOC = ROOT / "2271-Y5-R2FR-parent-psi-action-Phiq-pullback-contract-or-qR-numeric-backstop.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2271_00_2270_doc",
        "source_key": "2270_doc",
        "source_path": ROOT / "2270-Y5-R2FR-psi-to-Phiq-quotient-map-or-qR-stiffness-source.md",
        "needles": ["PCM2270_1_component_projection", "SSA2270_2_qR_ratio", "NEXT2270_0_primary"],
        "role": "handoff: q is covariance mismatch; pullback contract selected",
    },
    {
        "source_id": "SRC2271_01_2270_validation",
        "source_key": "2270_validation",
        "source_path": OUT / "P8_Y5_BRR545_2270_VALIDATION.csv",
        "needles": ["VAL2270_OVERALL", "PASS"],
        "role": "confirms 2270 passed before 2271 starts",
    },
    {
        "source_id": "SRC2271_02_2270_map",
        "source_key": "2270_map",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2270_PSI_COVARIANCE_TO_PHIQ_MAP.csv",
        "needles": ["PCM2270_1_component_projection", "DERIVED_LINEAR_CHANNEL_TEST"],
        "role": "machine-readable psi covariance to Phi/q map",
    },
    {
        "source_id": "SRC2271_03_2270_stiffness",
        "source_key": "2270_stiffness",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2270_STIFFNESS_SOURCE_ATTEMPT.csv",
        "needles": ["SSA2270_0_MR2_pullback", "SSA2270_1_jR_source", "SSA2270_2_qR_ratio"],
        "role": "machine-readable missing stiffness/source pullback inputs",
    },
    {
        "source_id": "SRC2271_04_2268_split",
        "source_key": "2268_split",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2268_PHI_Q_VARIABLE_SPLIT.csv",
        "needles": ["PQS2268_0_definitions", "PQS2268_2_reduced_branch"],
        "role": "Phi/q exact variable split",
    },
    {
        "source_id": "SRC2271_05_micro_action",
        "source_key": "micro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "L_MTS", "g_{μν} = η_{μν}"],
        "role": "primitive psi action and covariance metric source",
    },
    {
        "source_id": "SRC2271_06_macro_action",
        "source_key": "macro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["g_{μν}(x)", "⟨ ∂_μ ψ(x) ∂_ν ψ(x) ⟩_{smooth}", "correct Lorentzian signature"],
        "role": "macro psi-gradient smoothing statement",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2271_SOURCE_REGISTER.csv",
    "pullback_formulas": OUT / "P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv",
    "pullback_contract": OUT / "P8_Y5_PARENT_QLOC_2271_PULLBACK_CONTRACT.csv",
    "hessian_ledger": OUT / "P8_Y5_PARENT_QLOC_2271_HESSIAN_SOURCE_LEDGER.csv",
    "numeric_backstop": OUT / "P8_Y5_PARENT_QLOC_2271_QR_NUMERIC_BACKSTOP_INTAKE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2271_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2271_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2271_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2271_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2271_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2271_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_contract": QUEUE / "JR2271_PHIQ_PULLBACK_CONTRACT_NONCLAIM.csv",
    "queue_backstop": QUEUE / "JR2271_QR_NUMERIC_BACKSTOP_INTAKE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_psi_action_Phiq_pullback_refusal_2271.csv",
    "beta_docs": BETA_DOCS / "RAB_PSI_ACTION_PHIQ_PULLBACK_2271_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def pullback_formula_rows() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "PBF2271_0_inverse_map",
            "object": "Phi/q to covariance-channel map",
            "formula": "A=exp(2Phi+q/2), B=exp(-2Phi+q/2), C_tt=1-A, C_rr=B-1",
            "use": "turns a proposed Phi/q history into the covariance components the psi map must realize",
            "status": "EXACT_FORMULA",
            "valid_for_claim": False,
        },
        {
            "formula_id": "PBF2271_1_q_tangent",
            "object": "q-direction at fixed Phi",
            "formula": "partial_q C_tt=-A/2, partial_q C_rr=B/2; at q=0 this is (-exp(2Phi)/2, exp(-2Phi)/2)",
            "use": "defines the covariance tangent whose Hessian would be M_R^2",
            "status": "EXACT_TANGENT",
            "valid_for_claim": False,
        },
        {
            "formula_id": "PBF2271_2_phi_tangent",
            "object": "Phi-direction at fixed q",
            "formula": "partial_Phi C_tt=-2A, partial_Phi C_rr=-2B",
            "use": "separates Newton-potential motion from reciprocal-strain motion in covariance space",
            "status": "EXACT_TANGENT",
            "valid_for_claim": False,
        },
        {
            "formula_id": "PBF2271_3_q_zero_channel_relation",
            "object": "reduced branch relation",
            "formula": "q=0 iff (1-C_tt)(1+C_rr)=1; equivalently C_rr=C_tt/(1-C_tt)",
            "use": "the exact relation a parent psi covariance theorem must prove",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "formula_id": "PBF2271_4_weak_channel",
            "object": "linear weak-field channel",
            "formula": "q=(C_rr-C_tt)+O(C^2)",
            "use": "first diagnostic for any psi covariance model or numerical backstop",
            "status": "DERIVED_LINEAR_TEST",
            "valid_for_claim": False,
        },
    ]


def pullback_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PBC2271_0_smoothing_kernel",
            "required_object": "coarse-graining/smoothing operator",
            "acceptance_test": "define <partial_mu psi partial_nu psi>_smooth, domain, boundary, covariance, and local static radial projection",
            "current_status": "MISSING_EXPLICIT_KERNEL",
            "why_it_matters": "without the kernel there is no computable C_tt or C_rr from psi",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_1_metric_projection",
            "required_object": "sign/frame/areal convention",
            "acceptance_test": "declare how g_tt,g_rr are projected into A=T^2 and B=S in the local branch",
            "current_status": "PARTIAL_CONVENTION_ONLY",
            "why_it_matters": "q and Phi are not invariantly defined until the local observer/radial frame is fixed",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_2_lift",
            "required_object": "right-inverse/lift from (Phi,q) tangent to psi variations",
            "acceptance_test": "construct delta_q psi and delta_Phi psi such that their covariance variations match PBF2271_1 and PBF2271_2",
            "current_status": "MISSING_PSI_LIFT",
            "why_it_matters": "Hessians of A_MTS[psi] along q cannot be computed without a lift",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_3_effective_action",
            "required_object": "parent effective action Gamma[Phi,q]",
            "acceptance_test": "define whether Gamma is a constrained pullback, extremized action, averaged action, or effective action after integrating microscopic psi modes",
            "current_status": "MISSING_EFFECTIVE_ACTION_DEFINITION",
            "why_it_matters": "M_R^2 and j_R depend on which parent action is actually varied",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_4_q_absence_or_verticality",
            "required_object": "q absent/vertical theorem",
            "acceptance_test": "prove q is absent from the image of the psi map, or q variations are quotient-vertical with matter/readout descent",
            "current_status": "MISSING_ABSENCE_VERTICALITY_PROOF",
            "why_it_matters": "this is the only route to derived q=0 without finite residual scoring",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_5_stiffness_hessian",
            "required_object": "M_R^2",
            "acceptance_test": "compute second_q Gamma at q=0 in declared units and prove sign/positivity if using finite stiffness",
            "current_status": "MISSING_MR2",
            "why_it_matters": "without M_R^2 the finite q_R branch has no theory coefficient",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_6_source_leg",
            "required_object": "j_R",
            "acceptance_test": "compute first q-source leg from matter/readout with J_R=j_R L+O(L^2)",
            "current_status": "MISSING_JR",
            "why_it_matters": "without j_R the q_R ratio cannot be formed",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_7_no_gradient_guard",
            "required_object": "q operator inventory",
            "acceptance_test": "show the pullback does not generate nabla q kinetic/boundary momentum, or explicitly retain W_q and Q_R hair",
            "current_status": "MISSING_OPERATOR_INVENTORY",
            "why_it_matters": "finite algebraic q_R is safe only if it does not secretly become a Q_R/r hair field",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PBC2271_8_verdict",
            "required_object": "claim-grade Phi/q pullback package",
            "acceptance_test": "PBC2271_0 through PBC2271_7 pass jointly",
            "current_status": "PULLBACK_CONTRACT_UNSIGNED",
            "why_it_matters": "current corpus cannot yet derive local GR or score finite q_R from psi",
            "valid_for_claim": False,
        },
    ]


def hessian_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "ledger_id": "HSL2271_0_MR2_definition",
            "target": "M_R^2",
            "definition": "M_R^2 := second derivative of Gamma[Phi,q] with respect to q at q=0, normalized to L_q=-1/2 M_R^2 q^2",
            "needed_inputs": "effective action Gamma; psi lift delta_q psi; units; background Phi; density convention",
            "current_status": "MISSING_EFFECTIVE_ACTION_AND_LIFT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "ledger_id": "HSL2271_1_jR_definition",
            "target": "j_R",
            "definition": "J_R=j_R L+O(L^2), where J_R is the q-directed matter/readout source",
            "needed_inputs": "matter/readout action in Phi/q variables; source normalization; L=2GM/(rc^2) convention",
            "current_status": "MISSING_MATTER_READOUT_PULLBACK",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "ledger_id": "HSL2271_2_qR_ratio",
            "target": "q_R",
            "definition": "q_R=j_R/M_R^2 for the algebraic finite branch",
            "needed_inputs": "HSL2271_0 and HSL2271_1 with compatible units and no-gradient guard",
            "current_status": "MISSING_RATIO_INPUTS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "ledger_id": "HSL2271_3_absence_switch",
            "target": "q=0 theorem",
            "definition": "q theorem-zero can replace q_R only if q is absent/vertical before variation",
            "needed_inputs": "q absence/vertical proof plus matter/readout descent",
            "current_status": "THEOREM_ZERO_FALSE_CURRENT_CORPUS",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def numeric_backstop_rows() -> list[dict[str, Any]]:
    return [
        {
            "backstop_id": "NB2271_0_covariance_data",
            "target": "C_tt;C_rr profile",
            "purpose": "if analytic pullback fails, a toy/numeric psi covariance model must output C_tt and C_rr before q can be estimated",
            "required_fields": "psi_profile; smoothing_kernel; C_tt(r); C_rr(r); frame; units; source_path",
            "current_status": "MISSING_NUMERIC_PROFILE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "backstop_id": "NB2271_1_q_profile",
            "target": "q(r)",
            "purpose": "compute q=ln[(1-C_tt)(1+C_rr)] and weak q_R coefficient",
            "required_fields": "q_profile; L_profile; fit_window; q_R_fit; uncertainty; no_gradient_policy",
            "current_status": "MISSING_Q_PROFILE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "backstop_id": "NB2271_2_comparator_gate",
            "target": "local bounds",
            "purpose": "screen a parent/numeric q_R after it exists",
            "required_fields": "PPN/R10/clock/orbital bounds; projection kernels; no-cancellation guard",
            "current_status": "COMPARATOR_ONLY_NOT_THEORY_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2271_0_pullback_claim",
            "attempted_claim": "A_MTS[psi] has been pulled back to Gamma[Phi,q]",
            "runner_result": "BLOCKED",
            "blocked_by": "PBC2271_8_verdict=PULLBACK_CONTRACT_UNSIGNED",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2271_1_q_zero",
            "attempted_claim": "q is absent/vertical and local GR is derived",
            "runner_result": "BLOCKED",
            "blocked_by": "PBC2271_4_q_absence_or_verticality missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2271_2_finite_qR",
            "attempted_claim": "finite q_R can be scored",
            "runner_result": "BLOCKED",
            "blocked_by": "M_R^2, j_R, and no-gradient guard missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2271_3_numeric_backstop",
            "attempted_claim": "numeric q_R backstop is live",
            "runner_result": "BLOCKED",
            "blocked_by": "C_tt/C_rr/q profiles and fit window missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2271_0_formulas",
            "claim": "covariance pullback formulas are exact",
            "gate_pass": False,
            "reason": "formula readiness is not a physical derivation claim",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2271_1_pullback",
            "claim": "parent pullback exists",
            "gate_pass": False,
            "reason": "smoothing kernel, lift, and effective action missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2271_2_zero",
            "claim": "q theorem-zero/local GR",
            "gate_pass": False,
            "reason": "q absence/vertical proof missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2271_3_finite",
            "claim": "finite q_R coefficient",
            "gate_pass": False,
            "reason": "M_R^2 and j_R missing",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2271_0_formula_gain",
            "decision": "PULLBACK_TANGENTS_LOCKED",
            "reason": "the q and Phi covariance tangents are now explicit, so future Hessian/source work has a target direction",
            "next_action": "use PBF2271_1 and PBF2271_2 for any q Hessian/source calculation",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2271_1_contract",
            "decision": "PARENT_PULLBACK_CONTRACT_UNSIGNED",
            "reason": "kernel, lift, effective action, q absence/verticality, M_R^2, j_R, and no-gradient guard are missing",
            "next_action": "do not claim derived local GR or finite q_R",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2271_2_backstop",
            "decision": "NUMERIC_BACKSTOP_DEFINED_NOT_LIVE",
            "reason": "numeric path needs C_tt/C_rr profiles from a declared psi model before q_R can be estimated",
            "next_action": "build a minimal covariance toy/lift only as nonclaim scaffolding",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2271_3_next",
            "decision": "MINIMAL_COVARIANCE_LIFT_OR_QR_PROFILE_NEXT",
            "reason": "the next productive step is to attempt a minimal lift that realizes delta_q C, or produce a numeric q profile template",
            "next_action": "2272-Y5-R2FR-minimal-psi-covariance-lift-or-qR-profile-template.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2271_0_primary",
            "next_target": "2272-Y5-R2FR-minimal-psi-covariance-lift-or-qR-profile-template.md",
            "script": "scripts/Y5_R2FR_minimal_psi_covariance_lift_or_qR_profile_template_2272.py",
            "objective": "try to construct a minimal psi covariance lift realizing the Phi/q tangents; if no lawful lift is possible, create a strict nonclaim q_R profile template",
            "selection_status": "selected",
            "success_condition": "a lift supplies computable q Hessian/source directions, or the q_R profile template is ready but blocked until source data exist",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2271_contract",
            "source_path": rel(OUTPUTS["pullback_contract"]),
            "target_path": rel(COPY_TARGETS["queue_contract"]),
            "target_exists": COPY_TARGETS["queue_contract"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_contract"]),
            "reason": "Phi/q pullback contract copied as nonclaim queue",
        },
        {
            "copy_id": "BC2271_backstop",
            "source_path": rel(OUTPUTS["numeric_backstop"]),
            "target_path": rel(COPY_TARGETS["queue_backstop"]),
            "target_exists": COPY_TARGETS["queue_backstop"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_backstop"]),
            "reason": "q_R numeric backstop intake copied as nonclaim queue",
        },
        {
            "copy_id": "BC2271_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]),
            "reason": "branch-locked WEP/local refusal gates",
        },
        {
            "copy_id": "BC2271_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]),
            "reason": "portable pullback decision ledger",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    formulas = read_csv(OUTPUTS["pullback_formulas"])
    contract = read_csv(OUTPUTS["pullback_contract"])
    hessian = read_csv(OUTPUTS["hessian_ledger"])
    backstop = read_csv(OUTPUTS["numeric_backstop"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2271_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2271_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2271_2_prior_validation",
            any(row["source_key"] == "2270_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2270 validation passes",
        ),
        (
            "VAL2271_3_formulas",
            {row["formula_id"] for row in formulas}
            >= {"PBF2271_0_inverse_map", "PBF2271_1_q_tangent", "PBF2271_2_phi_tangent", "PBF2271_3_q_zero_channel_relation"},
            "inverse map and covariance tangents are written",
        ),
        (
            "VAL2271_4_contract_unsigned",
            any(row["contract_id"] == "PBC2271_8_verdict" and row["current_status"] == "PULLBACK_CONTRACT_UNSIGNED" for row in contract)
            and all(row["valid_for_claim"].lower() == "false" for row in contract),
            "pullback contract is written and unsigned",
        ),
        (
            "VAL2271_5_hessian_nonclaim",
            all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in hessian),
            "M_R^2/j_R/q_R ledger remains nonclaim",
        ),
        (
            "VAL2271_6_backstop_nonclaim",
            all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in backstop),
            "numeric backstop remains nonclaim",
        ),
        (
            "VAL2271_7_refusal_blocks",
            all(row["score_eligible"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in refusal),
            "refusal runner blocks local claims",
        ),
        (
            "VAL2271_8_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates are all blocked",
        ),
        (
            "VAL2271_9_next_selected",
            any(row["route_id"] == "NEXT2271_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2272 target selected",
        ),
        ("VAL2271_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2271 CSVs parse"),
        (
            "VAL2271_11_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass")
            ),
            "no generated score/claim/gate flags are true",
        ),
        (
            "VAL2271_12_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2271_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2271_14_formalization_no_2271",
            not any(
                path.is_file()
                and (path.name.startswith("2271-") or (path.name.startswith("P8_Y5") and "2271" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2271 output files",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2271_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2271 locks Phi/q covariance tangents, writes the parent pullback contract, keeps q_R nonclaim, and selects 2272",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    formulas = read_csv(OUTPUTS["pullback_formulas"])
    contract = read_csv(OUTPUTS["pullback_contract"])
    hessian = read_csv(OUTPUTS["hessian_ledger"])
    backstop = read_csv(OUTPUTS["numeric_backstop"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2271 - Y5/R2FR Parent psi Action Phi/q Pullback Contract Or q_R Numeric Backstop",
        "",
        "## Verdict",
        "",
        "2271 turns the `psi -> g -> (Phi,q)` problem into a precise pullback contract. The exact inverse channel map is now written: `A=exp(2Phi+q/2)`, `B=exp(-2Phi+q/2)`, `C_tt=1-A`, and `C_rr=B-1`. Therefore the q-direction in covariance space is `partial_q C_tt=-A/2`, `partial_q C_rr=B/2`, while the Phi-direction is `partial_Phi C_tt=-2A`, `partial_Phi C_rr=-2B`.",
        "",
        "That is real progress: any future derivation of finite `M_R^2`, source `j_R`, or theorem-zero `q=0` now has an exact covariance tangent to work with. But the current corpus still lacks the objects needed to pull back `A_MTS[psi]`: smoothing kernel, local projection convention, psi lift for the q tangent, effective action definition, q absence/verticality proof, matter/readout source leg, and no-gradient operator inventory.",
        "",
        "So no local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made. The next move is either construct a minimal lawful psi covariance lift or build a strict nonclaim `q_R` profile template.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Covariance Pullback Formulas",
        table(["formula_id", "object", "formula", "use", "status", "valid_for_claim"], formulas),
        "",
        "## Pullback Contract",
        table(["contract_id", "required_object", "acceptance_test", "current_status", "why_it_matters", "valid_for_claim"], contract),
        "",
        "## Hessian / Source Ledger",
        table(["ledger_id", "target", "definition", "needed_inputs", "current_status", "score_ready", "valid_for_claim"], hessian),
        "",
        "## q_R Numeric Backstop Intake",
        table(["backstop_id", "target", "purpose", "required_fields", "current_status", "score_ready", "valid_for_claim"], backstop),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is a good narrowing step. We are no longer saying vaguely that `psi` creates geometry. We know exactly what `psi` must do in the local branch: either forbid the q tangent, make it quotient-vertical, or give it a computable Hessian/source ratio. The missing beam is now the lift from covariance-channel variations back into lawful `psi` variations.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["pullback_formulas"], pullback_formula_rows())
    write_csv(OUTPUTS["pullback_contract"], pullback_contract_rows())
    write_csv(OUTPUTS["hessian_ledger"], hessian_ledger_rows())
    write_csv(OUTPUTS["numeric_backstop"], numeric_backstop_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["pullback_contract"], COPY_TARGETS["queue_contract"])
    shutil.copyfile(OUTPUTS["numeric_backstop"], COPY_TARGETS["queue_backstop"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
