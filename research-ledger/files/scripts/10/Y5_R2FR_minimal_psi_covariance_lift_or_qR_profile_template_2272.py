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

BRANCH_ID = "MTS_R2FR_MINIMAL_PSI_COVARIANCE_LIFT_OR_QR_PROFILE_2272"
DOC = ROOT / "2272-Y5-R2FR-minimal-psi-covariance-lift-or-qR-profile-template.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2272_00_2271_doc",
        "source_key": "2271_doc",
        "source_path": ROOT / "2271-Y5-R2FR-parent-psi-action-Phiq-pullback-contract-or-qR-numeric-backstop.md",
        "needles": ["PBF2271_1_q_tangent", "PBC2271_8_verdict", "NEXT2271_0_primary"],
        "role": "handoff: q tangent locked, parent pullback still unsigned",
    },
    {
        "source_id": "SRC2272_01_2271_validation",
        "source_key": "2271_validation",
        "source_path": OUT / "P8_Y5_BRR545_2271_VALIDATION.csv",
        "needles": ["VAL2271_OVERALL", "PASS"],
        "role": "confirms 2271 passed before 2272 starts",
    },
    {
        "source_id": "SRC2272_02_2271_formulas",
        "source_key": "2271_formulas",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv",
        "needles": ["PBF2271_1_q_tangent", "PBF2271_3_q_zero_channel_relation"],
        "role": "machine-readable Phi/q tangent formulas",
    },
    {
        "source_id": "SRC2272_03_2271_contract",
        "source_key": "2271_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2271_PULLBACK_CONTRACT.csv",
        "needles": ["PBC2271_2_lift", "PBC2271_8_verdict", "PULLBACK_CONTRACT_UNSIGNED"],
        "role": "missing parent pullback clauses",
    },
    {
        "source_id": "SRC2272_04_2271_hessian",
        "source_key": "2271_hessian",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2271_HESSIAN_SOURCE_LEDGER.csv",
        "needles": ["HSL2271_0_MR2", "HSL2271_1_jR", "HSL2271_2_qR_ratio"],
        "role": "finite stiffness/source ledger",
    },
    {
        "source_id": "SRC2272_05_2270_map",
        "source_key": "2270_map",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2270_PSI_COVARIANCE_TO_PHIQ_MAP.csv",
        "needles": ["PCM2270_1_component_projection", "PCM2270_2_q_zero_condition"],
        "role": "psi covariance to Phi/q channel map",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2272_SOURCE_REGISTER.csv",
    "algebraic_lift": OUT / "P8_Y5_PARENT_QLOC_2272_ALGEBRAIC_COVARIANCE_LIFT.csv",
    "q_lift": OUT / "P8_Y5_PARENT_QLOC_2272_Q_TANGENT_LIFT_ATTEMPT.csv",
    "integrability": OUT / "P8_Y5_PARENT_QLOC_2272_FIELD_INTEGRABILITY_LEDGER.csv",
    "profile_template": OUT / "P8_Y5_PARENT_QLOC_2272_QR_PROFILE_TEMPLATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2272_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2272_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2272_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2272_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2272_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2272_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_lift": QUEUE / "JR2272_MINIMAL_COVARIANCE_LIFT_THEOREM_NONCLAIM.csv",
    "queue_profile": QUEUE / "JR2272_QR_PROFILE_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_minimal_psi_covariance_lift_refusal_2272.csv",
    "beta_docs": BETA_DOCS / "RAB_MINIMAL_PSI_COVARIANCE_LIFT_2272_NONCLAIM.csv",
}


def stringify(value: Any) -> str:
    if isinstance(value, Path):
        return str(value)
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path) if path.exists() else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": path,
                "exists": path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def algebraic_lift_rows() -> list[dict[str, Any]]:
    return [
        {
            "lift_id": "ACL2272_0_setup",
            "object": "smoothed covariance channel",
            "statement": "Let C=U S U^T, where columns/rows of U represent local psi-gradient carriers after smoothing and S is the channel signature/weight matrix.",
            "assumptions": "C is invertible on the active local block; deltaC is symmetric; the lift is only first order and covariance-level.",
            "derivation": "The linearized covariance is L_U(deltaU)=deltaU S U^T + U S deltaU^T.",
            "status": "FORMAL_SETUP",
            "valid_for_claim": False,
        },
        {
            "lift_id": "ACL2272_1_right_inverse",
            "object": "algebraic right inverse",
            "statement": "For invertible C, choose deltaU = (1/2) deltaC C^{-1} U.",
            "assumptions": "C^{-1} exists on the projected block; no field exactness, boundary, smoothing, or action stationarity is claimed.",
            "derivation": "deltaU S U^T=(1/2)deltaC C^{-1} C=(1/2)deltaC and U S deltaU^T=(1/2)C C^{-T} deltaC^T=(1/2)deltaC, so L_U(deltaU)=deltaC.",
            "status": "ALGEBRAIC_COVARIANCE_LIFT_EXISTS_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "lift_id": "ACL2272_2_rank_boundary",
            "object": "rank-deficient or cone-boundary channel",
            "statement": "If C is rank deficient on the active block, the tangent is restricted and the right inverse above cannot be used without a pseudoinverse plus tangent-cone checks.",
            "assumptions": "No corpus source proves the local covariance block is interior/invertible.",
            "derivation": "At rank boundary, arbitrary symmetric deltaC can leave the covariance cone or require carriers not represented by the parent psi sector.",
            "status": "RANK_CONDITION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "lift_id": "ACL2272_3_not_parent_action",
            "object": "parent action pullback",
            "statement": "A covariance-level lift is not yet a pullback of A_MTS[psi] to Gamma[Phi,q].",
            "assumptions": "Need exact smoothing kernel, psi carrier inventory, field exactness, boundary conditions, and effective action definition.",
            "derivation": "The construction proves only that a local covariance tangent can be algebraically represented when C is invertible.",
            "status": "FIELD_LEVEL_LIFT_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def q_tangent_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "QTL2272_0_target",
            "target": "q tangent at q=0",
            "formula": "deltaC_tt=-(1/2)exp(2Phi) deltaq; deltaC_rr=(1/2)exp(-2Phi) deltaq; off-diagonal projected components set to zero.",
            "lift_candidate": "deltaU_q=(1/2) deltaC_q C^{-1} U if the active covariance block is invertible.",
            "missing_parent_input": "local C block, signature/weights S, smoothing operator, psi carrier basis U",
            "status": "TARGET_TANGENT_LOCKED_LIFT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QTL2272_1_diagonal_carrier_limit",
            "target": "diagonal independent carrier intuition",
            "formula": "For diagonal nonzero C_tt,C_rr one may write delta u_t/u_t=deltaC_tt/(2C_tt) and delta u_r/u_r=deltaC_rr/(2C_rr).",
            "lift_candidate": "delta u_t/u_t=-exp(2Phi)deltaq/(4C_tt); delta u_r/u_r=exp(-2Phi)deltaq/(4C_rr).",
            "missing_parent_input": "proof that t and r gradient carriers can be varied independently while remaining gradients of psi",
            "status": "USEFUL_LOCAL_FORMULA_NOT_A_FIELD_PROOF",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QTL2272_2_q_zero_readout",
            "target": "exact q=0 reduced branch",
            "formula": "(1-C_tt)(1+C_rr)=1, equivalently C_rr=C_tt/(1-C_tt).",
            "lift_candidate": "A lawful parent mechanism must either preserve this constraint dynamically or give q_R=j_R/M_R^2 small enough for local tests.",
            "missing_parent_input": "dynamical invariance of q=0 surface or finite stiffness/source ratio",
            "status": "Q_ZERO_SURFACE_IDENTIFIED_NOT_PROTECTED",
            "valid_for_claim": False,
        },
    ]


def integrability_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "FIL2272_0_exactness",
            "gate": "covector exactness",
            "requirement": "Each lifted carrier delta u_mu must be a gradient: partial_mu delta u_nu - partial_nu delta u_mu = 0, modulo smoothing.",
            "current_evidence": "No source gives a curl-free psi lift for deltaC_q.",
            "verdict": "UNSIGNED",
            "claim_allowed": False,
        },
        {
            "gate_id": "FIL2272_1_smoothing_inverse",
            "gate": "smoothing/readout inverse",
            "requirement": "The smoothing map from microscopic psi gradients to C_mu_nu must admit a local right inverse on the q tangent.",
            "current_evidence": "2271 explicitly records the missing smoothing kernel and projection convention.",
            "verdict": "UNSIGNED",
            "claim_allowed": False,
        },
        {
            "gate_id": "FIL2272_2_stationarity",
            "gate": "parent action stationarity",
            "requirement": "The lifted delta_q psi must be an allowed variation for the second variation of A_MTS[psi], not only an algebraic covariance perturbation.",
            "current_evidence": "No Hessian of A_MTS along the q-lift has been sourced.",
            "verdict": "UNSIGNED",
            "claim_allowed": False,
        },
        {
            "gate_id": "FIL2272_3_signature",
            "gate": "signature/cone consistency",
            "requirement": "The local covariance representation must tolerate deltaC_tt<0 and deltaC_rr>0 without leaving the allowed carrier cone/signature sector.",
            "current_evidence": "No parent sign/weight inventory proves this.",
            "verdict": "UNSIGNED",
            "claim_allowed": False,
        },
        {
            "gate_id": "FIL2272_4_boundary",
            "gate": "boundary/local projection silence",
            "requirement": "Boundary terms and local projection terms must not reintroduce q-sources into the local GR branch.",
            "current_evidence": "No boundary theorem attached to the q-lift exists.",
            "verdict": "UNSIGNED",
            "claim_allowed": False,
        },
    ]


def profile_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "profile_id": "QRP2272_0_ratio",
            "quantity": "q_R",
            "template": "q_R(r)=j_R(r)/M_R^2(r)",
            "required_inputs": "parent Hessian M_R^2(r); parent source j_R(r); local projection convention; units; source paths",
            "use": "minimal finite-stiffness backstop if exact q=0 protection fails",
            "status": "TEMPLATE_ONLY_PARENT_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "profile_id": "QRP2272_1_residual_vector",
            "quantity": "local residual vector",
            "template": "R_loc=[q_R, partial_r q_R, partial_r^2 q_R, DeltaPhi_induced(q_R), gamma_PPN-1, beta_PPN-1]",
            "required_inputs": "map from q_R to metric potentials; PPN readout; arena scales",
            "use": "future PPN/clock/orbital scoring once q_R is sourced",
            "status": "READOUT_TEMPLATE_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "profile_id": "QRP2272_2_safe_model_family",
            "quantity": "nonclaim profile family",
            "template": "q_R(r)=q0/(1+(r/ell_q)^p) or q0 exp[-(r/ell_q)^p], with p>0 and all parameters sourced before scoring",
            "required_inputs": "q0, ell_q, p from parent coefficients or explicit empirical fit protocol",
            "use": "numerical smoke tests only; cannot replace derivation",
            "status": "SMOKE_TEMPLATE_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2272_0_lift_claim",
            "attempted_claim": "The q tangent has been lifted to a lawful psi variation.",
            "runner_result": "BLOCKED",
            "blocked_by": "FIL2272_0/FIL2272_1/FIL2272_2 unsigned",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2272_1_local_gr_claim",
            "attempted_claim": "The local branch reduces to GR because q=0 is protected.",
            "runner_result": "BLOCKED",
            "blocked_by": "q=0 surface identified but no protection theorem or finite q_R bound",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2272_2_qR_score_claim",
            "attempted_claim": "The finite q_R residual can be scored against PPN/clock/orbital data.",
            "runner_result": "BLOCKED",
            "blocked_by": "M_R^2, j_R, and q_R-to-observable map missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2272_0_covariance_lift",
            "claim": "covariance-level q tangent lift exists",
            "gate_pass": False,
            "reason": "proved only conditionally on invertible local C and unspecified carrier basis",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2272_1_field_lift",
            "claim": "field-level psi lift exists",
            "gate_pass": False,
            "reason": "exactness/curl, smoothing inverse, and parent action variation are unsigned",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2272_2_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "q=0 is not yet protected and finite q_R is not bounded",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2272_3_profile_scoring",
            "claim": "q_R profile can be scored",
            "gate_pass": False,
            "reason": "profile is only a template until parent coefficients or data protocol exist",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2272_0_real_gain",
            "decision": "ALGEBRAIC_COVARIANCE_LIFT_CONDITIONALLY_AVAILABLE",
            "reason": "deltaU=(1/2)deltaC C^{-1}U is a formal right inverse for symmetric covariance tangents when C is invertible.",
            "next_action": "Try to promote this algebraic lift to an exact/curl-free psi-gradient lift.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2272_1_blocker",
            "decision": "FIELD_LEVEL_LIFT_UNSIGNED",
            "reason": "The route still lacks exactness, smoothing inverse, parent Hessian, and boundary silence.",
            "next_action": "Do not claim local GR; attack the exactness/smoothing gate next.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2272_2_backstop",
            "decision": "QR_PROFILE_TEMPLATE_STAGED",
            "reason": "If exact q=0 protection fails, the finite residual must be measured as q_R=j_R/M_R^2 with a PPN residual vector.",
            "next_action": "Keep profile rows nonclaim until M_R^2 and j_R have source paths.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2272_3_next",
            "decision": "EXACTNESS_SMOOTHING_GATE_NEXT",
            "reason": "This is the narrowest remaining parent-action obstruction after the algebraic covariance lift.",
            "next_action": "2273-Y5-R2FR-exact-psi-gradient-lift-curl-smoothing-gate.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2272_0_primary",
            "next_target": "2273-Y5-R2FR-exact-psi-gradient-lift-curl-smoothing-gate.md",
            "script": "scripts/Y5_R2FR_exact_psi_gradient_lift_curl_smoothing_gate_2273.py",
            "objective": "test whether the algebraic q covariance lift can be represented by curl-free psi-gradient variations compatible with smoothing and boundary conditions",
            "selection_status": "selected",
            "success_condition": "exactness/smoothing gates close, or the branch is explicitly demoted to q_R profile scoring only",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows = []
    for copy_id, target in COPY_TARGETS.items():
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": {
                    "queue_lift": OUTPUTS["algebraic_lift"],
                    "queue_profile": OUTPUTS["profile_template"],
                    "branch_wep": OUTPUTS["refusal"],
                    "beta_docs": OUTPUTS["decision"],
                }[copy_id],
                "target_path": target,
                "target_exists": target.exists(),
                "target_parses": csv_parses(target) if target.exists() else False,
                "reason": "branch copy for downstream local-GR/coupling audits",
            }
        )
    return rows


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key not in {"validation"}]


def false_flag_check() -> bool:
    guarded_fields = {"score_ready", "score_eligible", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass"}
    for path in generated_csvs():
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for field in guarded_fields.intersection(row):
                    if row[field].strip().lower() == "true":
                        return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = source_register_rows()
    source_ok = all(row["exists"] for row in source_rows)
    needles_ok = all(row["needles_present"] for row in source_rows)

    prior_validation = read_text(OUTPUTS["source_register"].parent / "P8_Y5_BRR545_2271_VALIDATION.csv")
    prior_ok = "VAL2271_OVERALL" in prior_validation and "PASS" in prior_validation

    algebra = algebraic_lift_rows()
    algebra_ok = any("deltaU = (1/2) deltaC C^{-1} U" in row["statement"] for row in algebra) and any(
        "L_U(deltaU)=deltaC" in row["derivation"] for row in algebra
    )
    q_lift_ok = any("deltaC_tt=-(1/2)exp(2Phi)" in row["formula"] for row in q_tangent_rows())
    integrability_blocked = all(row["claim_allowed"] is False and row["verdict"] == "UNSIGNED" for row in integrability_rows())
    profile_nonclaim = all(row["valid_for_claim"] is False and row["score_ready"] is False for row in profile_template_rows())
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusal_rows())
    claim_blocks = all(row["gate_pass"] is False and row["valid_for_claim"] is False for row in claim_gate_rows())
    next_selected = any(row["route_id"] == "NEXT2272_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2272*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2272_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2272_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2272_2_prior_validation", prior_ok, "2271 validation passes"),
        ("VAL2272_3_algebraic_lift", algebra_ok, "conditional covariance right-inverse formula written"),
        ("VAL2272_4_q_tangent", q_lift_ok, "q tangent lift target written"),
        ("VAL2272_5_integrability_blocked", integrability_blocked, "field exactness/smoothing gates remain unsigned"),
        ("VAL2272_6_profile_nonclaim", profile_nonclaim, "q_R profile template remains nonclaim"),
        ("VAL2272_7_refusal_blocks", refusal_blocks, "refusal runner blocks local claims"),
        ("VAL2272_8_claim_gates_blocked", claim_blocks, "claim gates are all blocked"),
        ("VAL2272_9_next_selected", next_selected, "2273 target selected"),
        ("VAL2272_10_csv_parse", csvs_parse, "all generated 2272 CSVs parse"),
        ("VAL2272_11_no_claim_flags", no_claim_flags, "no generated score/claim/gate flags are true"),
        ("VAL2272_12_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2272_13_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2272_14_formalization_no_2272", formalization_clean, "formalization-workbench has no 2272 output files"),
    ]

    for check_id, passed, detail in checks:
        rows.append({"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail})

    overall = all(result for _, result, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2272_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2272 proves a conditional algebraic covariance lift, blocks field-level psi lift/local-GR claims, stages q_R profile template, and selects 2273",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    algebra = algebraic_lift_rows()
    q_lift = q_tangent_rows()
    integrability = integrability_rows()
    profiles = profile_template_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2272 - Y5/R2FR Minimal psi Covariance Lift Or q_R Profile Template",
        "",
        "## Verdict",
        "",
        "This checkpoint gets a real mathematical bite: at the covariance level, a first-order q-direction lift exists conditionally. If the local smoothed covariance block is invertible and represented as `C=U S U^T`, then `deltaU=(1/2) deltaC C^{-1} U` is a right inverse of the linearized covariance map.",
        "",
        "But that is not yet the parent-action derivation. The lift is algebraic, not yet a curl-free `psi` gradient lift, not yet passed through the smoothing kernel, not yet a Hessian of `A_MTS[psi]`, and not yet safe against boundary/projection terms. So this is progress, but not a local-GR claim.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Algebraic Covariance Lift",
        table(["lift_id", "object", "statement", "assumptions", "derivation", "status", "valid_for_claim"], algebra),
        "",
        "## q Tangent Lift Attempt",
        table(["attempt_id", "target", "formula", "lift_candidate", "missing_parent_input", "status", "valid_for_claim"], q_lift),
        "",
        "## Field Integrability Ledger",
        table(["gate_id", "gate", "requirement", "current_evidence", "verdict", "claim_allowed"], integrability),
        "",
        "## q_R Profile Template",
        table(["profile_id", "quantity", "template", "required_inputs", "use", "status", "score_ready", "valid_for_claim"], profiles),
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
        "The branch is not circling now; it has sharpened. We have a conditional covariance-level lift theorem, which means the q-channel is not merely hand-waved. The hard remaining question is whether that algebraic lift is actually generated by admissible `psi` fields. If 2273 closes exactness/smoothing, the local-GR route becomes much healthier. If it fails, the honest route is finite `q_R` profile scoring.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["algebraic_lift"], algebraic_lift_rows())
    write_csv(OUTPUTS["q_lift"], q_tangent_rows())
    write_csv(OUTPUTS["integrability"], integrability_rows())
    write_csv(OUTPUTS["profile_template"], profile_template_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["algebraic_lift"], COPY_TARGETS["queue_lift"])
    shutil.copyfile(OUTPUTS["profile_template"], COPY_TARGETS["queue_profile"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
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
