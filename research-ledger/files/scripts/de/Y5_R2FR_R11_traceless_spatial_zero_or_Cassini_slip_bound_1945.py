from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1945"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1945-Y5-R2FR-R11-traceless-spatial-zero-proof-or-Cassini-slip-bound.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1944_doc": ROOT / "1944-Y5-R2FR-R11-weak-field-potential-equations-or-coefficient-placeholder-ledger.md",
    "1944_validation": OUT / "P8_Y5_BRR545_1944_VALIDATION.csv",
    "1944_derivation": OUT / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv",
    "1944_coefficients": OUT / "P8_Y5_PARENT_QLOC_1944_R11_PROJECTION_COEFFICIENT_LEDGER.csv",
    "1944_slip": OUT / "P8_Y5_PARENT_QLOC_1944_CASSINI_SLIP_CONTROL_LEDGER.csv",
    "1944_next": OUT / "P8_Y5_PARENT_QLOC_1944_NEXT_TARGET.csv",
    "1940_r11": OUT / "P8_Y5_PARENT_QLOC_1940_R11_RESIDUAL_OPERATOR_LEDGER.csv",
    "1943_runner": OUT / "P8_Y5_PARENT_QLOC_1943_CASSINI_GAMMA_BOUND_RUNNER.csv",
}

NEEDLES = {
    "1944_doc": ["WFE1944_3_traceless_spatial_projection", "WFE1944_7_local_zero_route", "VAL1944_OVERALL"],
    "1944_validation": ["VAL1944_OVERALL", "PASS"],
    "1944_derivation": ["WFE1944_5_delta_gamma_source_law", "P_TF[R11_ij]"],
    "1944_coefficients": ["COEF1944_2_PTF", "MISSING_R11_TF_OPERATOR"],
    "1944_slip": ["SLIP1944_2_zero_theorem_target", "BEST_ZERO_PROOF_TARGET"],
    "1944_next": ["NEXT1944_0_primary", "traceless-spatial"],
    "1940_r11": ["R111940_5_ppn_residual", "DEFINE_OR_BOUND"],
    "1943_runner": ["RUN1943_0_cassini_schema", "2.3e-05"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1945_SOURCE_REGISTER.csv",
    "zero_theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_1945_TF_ZERO_THEOREM_ATTEMPT.csv",
    "spherical_tensor_audit": OUT / "P8_Y5_PARENT_QLOC_1945_SPHERICAL_TENSOR_AUDIT.csv",
    "cassini_slip_bound_form": OUT / "P8_Y5_PARENT_QLOC_1945_CASSINI_SLIP_BOUND_FORM.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_1945_PARENT_CONFORMAL_DESCENT_CONTRACT.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1945_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1945_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1945_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1945_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1945_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_zero_attempt": SOURCE_WEIGHT_DOCS / "R11_TF_ZERO_THEOREM_ATTEMPT_1945_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1945_CLAIM_GATE_NONCLAIM.csv",
    "cassini_slip_queue": QUEUE / "JR1945_PARENT_CONFORMAL_DESCENT_OR_CASSINI_SLIP_BOUND_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1945_CLAIM_GATE.csv",
}


def flag(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needles(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = read_text(path)
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in SOURCES.items():
        needles = NEEDLES[source_id]
        ok = has_needles(path, needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": str(path),
                "purpose": "1945 R11 traceless-spatial zero proof or Cassini slip bound",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_SOURCE_OR_NEEDLE",
                "issue": "" if ok else "source path missing or required needles absent",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def zero_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZT1945_0_target",
            "claim_tested": "P_TF[R11_ij]=0 implies delta_gamma_R11=0 at the 1944 weak-field order.",
            "derivation_or_countercheck": "From 1944: delta_gamma_R11 ~= -(kappa_R/(C_TF U)) nabla^{-2} P_TF[R11_ij].",
            "status": "TARGET_FROM_1944_CONFIRMED",
            "what_it_means": "Cassini gamma is safe if the local parent branch kills the traceless spatial R11 projection.",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZT1945_1_spherical_symmetry_test",
            "claim_tested": "Spherical symmetry alone forces P_TF[R11_ij]=0.",
            "derivation_or_countercheck": "A general spherical spatial tensor has R_ij=A(r)n_i n_j+B(r)(delta_ij-n_i n_j), so P_TF[R_ij]=(A-B)(n_i n_j-delta_ij/3).",
            "status": "REJECTED_SYMMETRY_ALONE_NOT_ENOUGH",
            "what_it_means": "radial anisotropy survives spherical symmetry; we need A=B or a stronger parent descent rule",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZT1945_2_conformal_spatial_condition",
            "claim_tested": "A conformal/isotropic spatial residual forces P_TF[R11_ij]=0.",
            "derivation_or_countercheck": "If R11_ij=S(r)delta_ij in the local orthonormal spatial frame, then P_TF[R11_ij]=0 identically.",
            "status": "SUFFICIENT_ZERO_CONDITION_DERIVED",
            "what_it_means": "the parent action can pass this gamma gate if local residuals descend only through the metric trace/conformal slot",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZT1945_3_scalar_hessian_test",
            "claim_tested": "A scalar memory/Hessian residual automatically has zero traceless spatial projection.",
            "derivation_or_countercheck": "For R11_ij=partial_i partial_j f(r), P_TF[R11_ij]=(f''-f'/r)(n_i n_j-delta_ij/3); zero requires f''=f'/r, so f=a r^2+b.",
            "status": "REJECTED_GENERIC_HESSIAN_CREATES_SLIP",
            "what_it_means": "a gradient/Hessian memory route fails Cassini unless the scalar is locally constant/silent or specially quadratic with acceptable boundaries",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZT1945_4_parent_descent_route",
            "claim_tested": "Parent local-vacuum descent can enforce conformal residuals.",
            "derivation_or_countercheck": "If no independent local spatial vector/tensor survives the quotient and the residual is algebraic in g_ij, then R11_ij=S g_ij and the TF projection vanishes.",
            "status": "CONDITIONAL_ROUTE_IDENTIFIED_NOT_PARENT_SIGNED",
            "what_it_means": "this is the route to prove; it cannot be assumed without a parent action/descent clause",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZT1945_5_verdict",
            "claim_tested": "The local R11 traceless-spatial zero theorem is proved.",
            "derivation_or_countercheck": "Sufficient conditions were derived, but the parent has not signed the conformal-descent/no-Hessian/no-boundary-anisotropy clauses.",
            "status": "ZERO_PROOF_OPEN_CONTRACT_EXPLICIT",
            "what_it_means": "not a failure of the whole theory; it is a precise missing parent contract",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def spherical_tensor_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "STA1945_0_general_spherical_tensor",
            "object": "R_ij=A n_i n_j+B(delta_ij-n_i n_j)",
            "tf_projection": "(A-B)(n_i n_j-delta_ij/3)",
            "verdict": "SPHERICAL_SYMMETRY_PERMITS_TF_SLIP",
            "needed_fix": "derive A=B or remove the radial anisotropy source",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "STA1945_1_conformal_tensor",
            "object": "R_ij=S delta_ij",
            "tf_projection": "0",
            "verdict": "SUFFICIENT_FOR_ZERO",
            "needed_fix": "parent residual must descend through metric trace/conformal slot only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "STA1945_2_scalar_hessian",
            "object": "R_ij=partial_i partial_j f(r)",
            "tf_projection": "(f''-f'/r)(n_i n_j-delta_ij/3)",
            "verdict": "DANGEROUS_UNLESS_LOCALLY_SILENT",
            "needed_fix": "prove f is locally constant/silent in solar vacuum, or bound f''-f'/r",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "STA1945_3_vector_flow",
            "object": "R_ij includes v_i v_j or preferred-flow dyads",
            "tf_projection": "generically nonzero",
            "verdict": "PREFERRED_FRAME_DANGER",
            "needed_fix": "derive local vertical/flow silence or map into alpha1/alpha2 as well as gamma",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "STA1945_4_boundary_memory",
            "object": "nonlocal/boundary memory kernel",
            "tf_projection": "depends on kernel anisotropy and boundary data",
            "verdict": "BOUNDARY_SILENCE_NEEDED",
            "needed_fix": "prove local solar-system kernel reduces to conformal/common mode or is below Cassini bound",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def cassini_slip_bound_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "CSB1945_0_gamma_policy",
            "quantity": "delta_gamma_R11",
            "bound_form": "|delta_gamma_R11| <= gamma_bound_policy",
            "status": "POLICY_NUMERIC_SOURCE_RECORDED_ELSEWHERE_NOT_CLAIM_READY",
            "missing_input": "confidence convention: 1sigma/2sigma/conservative absolute bound",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "CSB1945_1_projected_source_bound",
            "quantity": "nabla^{-2} P_TF[R11_ij]",
            "bound_form": "|nabla^{-2} P_TF[R11_ij]| <= |C_TF U/kappa_R| gamma_bound_policy",
            "status": "SYMBOLIC_BOUND_FORM_READY_INPUTS_MISSING",
            "missing_input": "C_TF,kappa_R,U_solar_frame,boundary-conditioned inverse Laplacian",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "CSB1945_2_zero_shortcut",
            "quantity": "P_TF[R11_ij]",
            "bound_form": "P_TF[R11_ij]=0 => bound satisfied exactly at this weak-field order",
            "status": "ZERO_SHORTCUT_CONDITIONAL_NOT_SIGNED",
            "missing_input": "parent conformal-descent theorem",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PC1945_0_no_surviving_spatial_dyad",
            "required_clause": "The local vacuum quotient leaves no independent spatial vector/dyad capable of forming n_i n_j, v_i v_j, or Hessian anisotropy.",
            "why_required": "without this, spherical symmetry can still produce traceless radial slip",
            "status": "MISSING_PARENT_SIGNATURE",
            "if_signed": "removes the generic TF source channel",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PC1945_1_conformal_residual",
            "required_clause": "The spatial R11 residual descends algebraically as R11_ij=S g_ij or vanishes in the local branch.",
            "why_required": "this is the direct sufficient condition for P_TF[R11_ij]=0",
            "status": "MISSING_PARENT_SIGNATURE",
            "if_signed": "proves the Cassini gamma slip source is zero",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PC1945_2_hessian_silence",
            "required_clause": "Any scalar memory/Hessian contribution is locally constant/silent, or its f''-f'/r component is bounded.",
            "why_required": "generic Hessian residuals produce gamma slip",
            "status": "MISSING_PARENT_SIGNATURE",
            "if_signed": "closes the most dangerous scalar-memory leakage route",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PC1945_3_boundary_kernel_silence",
            "required_clause": "Boundary/nonlocal kernels project only into common mode locally, or are below the Cassini slip bound.",
            "why_required": "memory kernels can reintroduce anisotropic spatial stress",
            "status": "MISSING_PARENT_SIGNATURE",
            "if_signed": "prevents hidden nonlocal slip from bypassing the local proof",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PC1945_4_coefficient_lock",
            "required_clause": "kappa_R, C_TF, U_solar_frame and the inverse-Laplacian boundary condition are fixed if a bound route is used.",
            "why_required": "without numeric/derived coefficients the Cassini comparison cannot be made",
            "status": "MISSING_PARENT_OR_SOURCE_INPUTS",
            "if_signed": "turns the symbolic inequality into an actual bound runner",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PC1945_5_conditional_theorem",
            "required_clause": "If PC1945_0 through PC1945_3 are signed, then P_TF[R11_ij]=0 and delta_gamma_R11=0 at the 1944 weak-field order.",
            "why_required": "records the exact future theorem statement",
            "status": "CONDITIONAL_THEOREM_READY_NOT_CLAIMED",
            "if_signed": "local Cassini gamma gate closes for the R11 branch at leading weak-field order",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1945_0_tensor_decomposition",
            "claim": "A spherical local residual can be decomposed into conformal/common and traceless radial anisotropic parts.",
            "status": "PASS_NONCLAIM",
            "reason": "decomposition and TF projection recorded",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1945_1_zero_condition",
            "claim": "R11_ij=S delta_ij is sufficient to set P_TF[R11_ij]=0.",
            "status": "PASS_NONCLAIM",
            "reason": "sufficient condition derived symbolically",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1945_2_spherical_zero",
            "claim": "Spherical symmetry alone proves P_TF[R11_ij]=0.",
            "status": "FAIL_REJECTED",
            "reason": "radial anisotropy A-B survives spherical symmetry",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1945_3_parent_zero_theorem",
            "claim": "MTS parent proves the local traceless-spatial R11 projection is zero.",
            "status": "FAIL_BLOCKED",
            "reason": "conformal-descent/no-Hessian/no-boundary-anisotropy clauses are unsigned",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1945_4_Cassini_slip_bound",
            "claim": "MTS R11 slip is below the Cassini gamma bound.",
            "status": "FAIL_BLOCKED",
            "reason": "symbolic bound exists but numeric/source inputs are missing",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1945_5_local_GR_PPN",
            "claim": "MTS derives local GR/PPN.",
            "status": "FAIL_BLOCKED",
            "reason": "gamma slip target is narrowed but not closed; other PPN residuals remain",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1945_6_public_claim",
            "claim": "1945 is a public-ready local-GR proof.",
            "status": "FAIL_BLOCKED",
            "reason": "private theorem-attempt checkpoint only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1945_0_zero_status",
            "decision": "SPHERICAL_SYMMETRY_ALONE_REJECTED_AS_ZERO_PROOF",
            "reason": "a radial anisotropic TF tensor survives as (A-B)(n_i n_j-delta_ij/3)",
            "next_action": "do not use spherical symmetry as a shortcut; require conformal descent or a bound",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1945_1_best_route",
            "decision": "PARENT_CONFORMAL_DESCENT_IS_THE_CLEAN_ZERO_ROUTE",
            "reason": "R11_ij=S g_ij kills the traceless spatial projection exactly",
            "next_action": "try to derive the conformal-descent/no-dyad/no-Hessian clauses from the parent action or MTS quotient map",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1945_2_fallback",
            "decision": "IF_CONFORMAL_DESCENT_FAILS_BUILD_CASSINI_SLIP_BOUND_RUNNER",
            "reason": "the bound form is already known but coefficients and local boundary data are missing",
            "next_action": "source or derive kappa_R,C_TF,U_solar_frame and inverse-Laplacian amplitude",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT1945_0_primary",
            "priority": "selected",
            "target_doc": "1946-Y5-R2FR-parent-conformal-descent-contract-or-Hessian-slip-kill.md",
            "target_script": "scripts/Y5_R2FR_parent_conformal_descent_or_hessian_slip_kill_1946.py",
            "objective": "attempt to derive the parent conformal-descent/no-dyad/no-Hessian clauses that make P_TF[R11_ij]=0, or demote to a Cassini slip bound runner",
            "acceptance_output": "signed parent clauses proving R11_ij=S g_ij locally, or explicit Hessian/boundary slip terms with claim=false",
            "nonclaim_rule": "no Cassini/local-GR claim unless the TF projection is parent-zero or bounded with real coefficients and boundary conditions",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1945_0_project_position",
            "status": "TF_ZERO_PROOF_NOT_CLOSED_BUT_PARENT_CONTRACT_EXACT",
            "strongest_result": "spherical symmetry alone fails; conformal spatial descent R11_ij=S g_ij is sufficient for P_TF=0 and Cassini gamma safety at leading order",
            "what_improved": "the proof obligation is now a concrete parent contract rather than a vague local-GR hope",
            "still_missing": "parent derivation of conformal descent/no dyad/no Hessian/boundary silence, or numeric Cassini slip inputs",
            "claim_status": "Cassini/local-GR public claims remain blocked",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_zero_attempt"], rows_by_name["zero_theorem_attempt"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["cassini_slip_queue"], rows_by_name["next_target"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_has_rows(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle))) > 0


def formalization_1945_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for _ in FORMALIZATION.rglob("*1945*"))


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, str]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": flag(False),
        "claim_allowed": flag(False),
    }


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    rows.append(validation_row("VAL1945_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found" if sources_ok else "source path or needle missing"))

    proof_statuses = {row["status"] for row in rows_by_name["zero_theorem_attempt"]}
    proof_ok = "REJECTED_SYMMETRY_ALONE_NOT_ENOUGH" in proof_statuses and "SUFFICIENT_ZERO_CONDITION_DERIVED" in proof_statuses and "ZERO_PROOF_OPEN_CONTRACT_EXPLICIT" in proof_statuses
    rows.append(validation_row("VAL1945_01_zero_attempt", "PASS" if proof_ok else "FAIL", "zero proof attempted with rejection and sufficient condition recorded"))

    spherical_text = "\n".join(row["tf_projection"] + row["verdict"] for row in rows_by_name["spherical_tensor_audit"])
    spherical_ok = "A-B" in spherical_text and "SUFFICIENT_FOR_ZERO" in spherical_text and "DANGEROUS_UNLESS_LOCALLY_SILENT" in spherical_text
    rows.append(validation_row("VAL1945_02_spherical_audit", "PASS" if spherical_ok else "FAIL", "spherical tensor and Hessian audit recorded"))

    bound_text = "\n".join(row["bound_form"] + row["status"] for row in rows_by_name["cassini_slip_bound_form"])
    bound_ok = "gamma_bound_policy" in bound_text and "SYMBOLIC_BOUND_FORM_READY_INPUTS_MISSING" in bound_text
    rows.append(validation_row("VAL1945_03_bound_form", "PASS" if bound_ok else "FAIL", "Cassini slip bound form recorded nonclaim"))

    contract_ok = any(row["status"] == "CONDITIONAL_THEOREM_READY_NOT_CLAIMED" for row in rows_by_name["parent_contract"]) and all(row["claim_allowed"] == flag(False) for row in rows_by_name["parent_contract"])
    rows.append(validation_row("VAL1945_04_parent_contract", "PASS" if contract_ok else "FAIL", "parent conformal-descent contract recorded"))

    claim_rows = rows_by_name["claim_gate"]
    claim_ok = (
        len([row for row in claim_rows if row["status"] == "PASS_NONCLAIM"]) == 2
        and any(row["status"] == "FAIL_REJECTED" for row in claim_rows)
        and len([row for row in claim_rows if row["status"] == "FAIL_BLOCKED"]) == 4
        and all(row["claim_allowed"] == flag(False) for row in claim_rows)
    )
    rows.append(validation_row("VAL1945_05_claim_gates", "PASS" if claim_ok else "FAIL", "only symbolic nonclaim gates pass; spherical shortcut rejected; claims blocked"))

    decision_ok = any(row["decision"] == "PARENT_CONFORMAL_DESCENT_IS_THE_CLEAN_ZERO_ROUTE" for row in rows_by_name["decision"])
    rows.append(validation_row("VAL1945_06_decision", "PASS" if decision_ok else "FAIL", "parent conformal descent selected as clean route"))

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1946-Y5-R2FR-parent-conformal-descent-contract")
    rows.append(validation_row("VAL1945_07_next_target", "PASS" if next_ok else "FAIL", "1946 parent conformal-descent target selected"))

    flags_ok = all(row.get("valid_for_claim") == flag(False) and row.get("claim_allowed") == flag(False) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1945_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = all(csv_has_rows(path) for path in output_paths)
    rows.append(validation_row("VAL1945_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    branch_ok = all(csv_has_rows(path) for path in BRANCH_COPIES.values())
    rows.append(validation_row("VAL1945_10_branch_copies", "PASS" if branch_ok else "FAIL", "; ".join(str(path) for path in BRANCH_COPIES.values())))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    rows.append(validation_row("VAL1945_11_pycache_absent", "PASS" if pycache_absent else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_1945_artifact_count()
    rows.append(validation_row("VAL1945_12_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1945_artifact_count={formalization_count}"))

    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(validation_row("VAL1945_OVERALL", "PASS" if overall_ok else "FAIL", "1945 R11 traceless-spatial zero proof or Cassini slip bound"))
    return rows


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1945 Y5 R2FR: R11 Traceless-Spatial Zero Proof or Cassini Slip Bound",
        "",
        "## Verdict",
        "",
        "1945 takes the proof shot. Result: the clean zero theorem is not closed yet, but the exact parent contract is now visible.",
        "",
        "Important rejection: spherical symmetry alone does not kill the Cassini slip source. A general spherical spatial residual has `R_ij=A(r)n_i n_j+B(r)(delta_ij-n_i n_j)`, whose traceless piece is `(A-B)(n_i n_j-delta_ij/3)`. So if we try to sneak in \"local spherical vacuum\" as the whole proof, Cassini can still punch us.",
        "",
        "Useful sufficient condition: if the parent local branch forces `R11_ij=S(r)delta_ij` or zero in the local orthonormal spatial frame, then `P_TF[R11_ij]=0`, hence `delta_gamma_R11=0` at the 1944 weak-field order. Generic scalar Hessian memory is dangerous because `partial_i partial_j f(r)` gives a nonzero traceless part unless `f''=f'/r`.",
        "",
        "So the next derivation target is sharper: derive parent conformal descent/no surviving spatial dyad/no Hessian or boundary anisotropy. If that cannot be derived, switch to a Cassini slip bound runner.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Zero Theorem Attempt",
        "",
        markdown_table(rows_by_name["zero_theorem_attempt"]),
        "",
        "## Spherical Tensor Audit",
        "",
        markdown_table(rows_by_name["spherical_tensor_audit"]),
        "",
        "## Cassini Slip Bound Form",
        "",
        markdown_table(rows_by_name["cassini_slip_bound_form"]),
        "",
        "## Parent Conformal-Descent Contract",
        "",
        markdown_table(rows_by_name["parent_contract"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "zero_theorem_attempt": zero_theorem_attempt_rows(),
        "spherical_tensor_audit": spherical_tensor_audit_rows(),
        "cassini_slip_bound_form": cassini_slip_bound_form_rows(),
        "parent_contract": parent_contract_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
