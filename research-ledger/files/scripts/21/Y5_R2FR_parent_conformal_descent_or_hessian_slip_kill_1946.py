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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1946"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1946-Y5-R2FR-parent-conformal-descent-contract-or-Hessian-slip-kill.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1945_doc": ROOT / "1945-Y5-R2FR-R11-traceless-spatial-zero-proof-or-Cassini-slip-bound.md",
    "1945_validation": OUT / "P8_Y5_BRR545_1945_VALIDATION.csv",
    "1945_contract": OUT / "P8_Y5_PARENT_QLOC_1945_PARENT_CONFORMAL_DESCENT_CONTRACT.csv",
    "1945_zero": OUT / "P8_Y5_PARENT_QLOC_1945_TF_ZERO_THEOREM_ATTEMPT.csv",
    "1912_descent": OUT / "P8_Y5_PARENT_QLOC_1912_NEIGHBOURHOOD_DESCENT_SIGNATURE_ATTEMPT.csv",
    "1912_axioms": OUT / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
    "1913_action_q": OUT / "P8_Y5_PARENT_QLOC_1913_PARENT_ACTION_Q_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
    "1913_typing": OUT / "P8_Y5_PARENT_QLOC_1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
    "1917_qkernel": OUT / "P8_Y5_PARENT_QLOC_1917_SINGLE_PUBLIC_METRIC_QKERNEL_AUDIT.csv",
    "1931_signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
}

NEEDLES = {
    "1945_doc": ["ZT1945_2_conformal_spatial_condition", "PC1945_5_conditional_theorem", "VAL1945_OVERALL"],
    "1945_validation": ["VAL1945_OVERALL", "PASS"],
    "1945_contract": ["PC1945_0_no_surviving_spatial_dyad", "PC1945_5_conditional_theorem"],
    "1945_zero": ["ZT1945_1_spherical_symmetry_test", "ZT1945_3_scalar_hessian_test"],
    "1912_descent": ["NQD1912_1_chain_rule", "NQD1912_4_verdict"],
    "1912_axioms": ["AX1912_1_q_functor", "AX1912_8_boundary_domain_silence"],
    "1913_action_q": ["PAQ1913_2_q_functor", "PAQ1913_5_verdict"],
    "1913_typing": ["QTM1913_1_q_functor", "QTM1913_7_readout_boundary"],
    "1917_qkernel": ["SPQ1917_4_qkernel_null", "FAILED_CURRENT_CORPUS"],
    "1931_signature": ["SIG1931_1_EH_or_R11_operator", "SIG1931_9_Ward_Bianchi_conservation"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1946_SOURCE_REGISTER.csv",
    "descent_theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_1946_PARENT_DESCENT_THEOREM_ATTEMPT.csv",
    "hessian_slip_kill": OUT / "P8_Y5_PARENT_QLOC_1946_HESSIAN_SLIP_KILL_LEMMA.csv",
    "conformal_clause_status": OUT / "P8_Y5_PARENT_QLOC_1946_CONFORMAL_DESCENT_CLAUSE_STATUS.csv",
    "boundary_kernel_risk": OUT / "P8_Y5_PARENT_QLOC_1946_BOUNDARY_KERNEL_RISK_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1946_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1946_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1946_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1946_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1946_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_descent": SOURCE_WEIGHT_DOCS / "PARENT_CONFORMAL_DESCENT_ATTEMPT_1946_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1946_CLAIM_GATE_NONCLAIM.csv",
    "next_queue": QUEUE / "JR1946_BOUNDARY_KERNEL_OR_CASSINI_SLIP_NUMERIC_INPUT_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1946_CLAIM_GATE.csv",
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
                "purpose": "1946 parent conformal descent or Hessian slip kill",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_SOURCE_OR_NEEDLE",
                "issue": "" if ok else "source path missing or required needles absent",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def descent_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DTH1946_0_target",
            "claim_tested": "Parent local conformal descent proves P_TF[R11_ij]=0.",
            "derivation_or_test": "Need PC1945_0 through PC1945_3: no surviving spatial dyad, conformal residual, Hessian silence, and boundary/kernel silence.",
            "status": "TARGET_SHARP",
            "consequence": "would close the leading Cassini gamma slip source for the R11 branch",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DTH1946_1_O3_algebraic_lemma",
            "claim_tested": "An algebraic O(3)-equivariant spatial residual has no traceless spatial part.",
            "derivation_or_test": "In a local orthonormal rest frame, if no vector/dyad/tensor other than delta_ij is available and R11_ij is algebraic, O(3)-equivariance forces R11_ij=S delta_ij.",
            "status": "CONDITIONAL_O3_CONFORMAL_LEMMA_DERIVED",
            "consequence": "P_TF[R11_ij]=0 follows, but only after the parent proves no independent spatial structure survives",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DTH1946_2_q_chain_rule_limit",
            "claim_tested": "The existing q-chain rule is enough to prove conformal descent.",
            "derivation_or_test": "1912 proves Dq[V]=0 implies Lie_V g_obs=0 if q and Obs_e are owned, but it does not prove the residual action has no hidden dyad/Hessian/boundary term.",
            "status": "INSUFFICIENT_FOR_TF_ZERO",
            "consequence": "geometry vertical blindness is necessary but not sufficient for local Cassini safety",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DTH1946_3_parent_action_schema_limit",
            "claim_tested": "The 1913 parent action/q schema signs the no-dyad condition.",
            "derivation_or_test": "1913 writes a coherent S_parent/q/Obs_e schema with S_res, but records it as a contract stack rather than a parent-certified operator domain.",
            "status": "SCHEMA_ONLY_NOT_PARENT_SIGNED",
            "consequence": "S_res can still carry anisotropic residual structure unless the operator domain forbids it",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DTH1946_4_qkernel_null_limit",
            "claim_tested": "q-kernel nullness proves all vertical/hideen spatial structure is physically silent.",
            "derivation_or_test": "1917 explicitly marks q-kernel null/matter invisibility as failed in the current corpus.",
            "status": "QKERNEL_NULL_NOT_SIGNED",
            "consequence": "Dq[v]=0 cannot yet be promoted to action-null or boundary-null silence",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DTH1946_5_verdict",
            "claim_tested": "1946 proves parent conformal descent.",
            "derivation_or_test": "The O(3) conformal lemma is derived conditionally, but the parent has not signed no-dyad, q-kernel nullness, Hessian silence, or boundary/kernel silence.",
            "status": "PARENT_CONFORMAL_DESCENT_NOT_CLOSED",
            "consequence": "local-GR/Cassini remains nonclaim; the next target is boundary/Hessian silence or numeric slip bound inputs",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def hessian_slip_kill_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "HSK1946_0_TF_formula",
            "object": "scalar memory Hessian R11_ij=partial_i partial_j f(r)",
            "statement": "P_TF[R11_ij]=(f''-f'/r)(n_i n_j-delta_ij/3)",
            "status": "HESSIAN_TF_FORMULA_RECORDED",
            "claim_impact": "generic scalar Hessian memory creates Cassini gamma slip",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "HSK1946_1_zero_ODE",
            "object": "zero traceless Hessian condition",
            "statement": "P_TF=0 iff f''=f'/r for the radial scalar Hessian channel",
            "status": "HESSIAN_ZERO_ODE_DERIVED",
            "claim_impact": "the scalar-memory danger is reduced to a one-dimensional local ODE",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "HSK1946_2_solution_family",
            "object": "solutions to f''=f'/r",
            "statement": "f(r)=a r^2+b, hence partial_i partial_j f=2a delta_ij and the Hessian is conformal/common-mode",
            "status": "ZERO_SLIP_SOLUTION_FAMILY_DERIVED",
            "claim_impact": "even nonzero a is gamma-safe at leading slip order, but it may feed Newtonian/common-mode/cosmology gates",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "HSK1946_3_bounded_decay_kill",
            "object": "bounded/decaying local vacuum scalar",
            "statement": "If the local residual scalar and gradient are bounded/decaying and no local r^2 cosmological term is admitted, then a=0 and f is locally constant/silent.",
            "status": "BOUNDED_DECAY_KILLS_HESSIAN_SLIP_CONDITIONALLY",
            "claim_impact": "this is a real route to kill Hessian slip, but the boundary condition is not parent-signed",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "HSK1946_4_bound_route",
            "object": "nonzero Hessian anisotropy",
            "statement": "If f''-f'/r is nonzero, Cassini requires |nabla^{-2}(f''-f'/r)| to be bounded through kappa_R/C_TF/U_solar.",
            "status": "BOUND_ROUTE_READY_INPUTS_MISSING",
            "claim_impact": "numeric comparison needs coefficients and boundary-conditioned inverse Laplacian",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def conformal_clause_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CDS1946_0_no_dyad",
            "parent_clause": "no surviving spatial vector/dyad/tensor in local vacuum quotient",
            "current_evidence": "1912/1913 define the needed q/Obs_e route conditionally; 1917 says q-kernel nullness failed in current corpus",
            "status": "NOT_PARENT_SIGNED",
            "if_filled": "O(3) algebraic lemma can force R11_ij=S delta_ij",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CDS1946_1_algebraic_residual",
            "parent_clause": "local residual is algebraic in g_obs/delta_ij rather than built from Hessians or boundary kernels",
            "current_evidence": "R11 operator remains a retained residual family; higher-derivative and nonlocal families are live",
            "status": "NOT_PARENT_SIGNED",
            "if_filled": "removes generic derivative slip channel",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CDS1946_2_hessian_silence",
            "parent_clause": "scalar Hessian channel is locally constant/silent or f=a r^2+b common-mode only",
            "current_evidence": "1946 derives the ODE and bounded/decay kill condition; boundary condition not parent-owned",
            "status": "CONDITIONAL_MATH_READY_PARENT_BOUNDARY_UNSIGNED",
            "if_filled": "kills the most direct scalar-memory source of gamma slip",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CDS1946_3_boundary_kernel_silence",
            "parent_clause": "boundary/nonlocal kernels are O(3)-isotropic common-mode or below the Cassini slip bound",
            "current_evidence": "1912 and 1913 retain boundary/readout/domain silence as open",
            "status": "OPEN_BOUNDARY_DOMAIN_SILENCE",
            "if_filled": "prevents hidden anisotropy from returning through support/readout",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CDS1946_4_theorem_status",
            "parent_clause": "PC1945_0 through PC1945_3 are all signed",
            "current_evidence": "conditional lemmas exist; required parent signatures are missing",
            "status": "THEOREM_NOT_CLOSED",
            "if_filled": "P_TF[R11_ij]=0 and delta_gamma_R11=0 at leading weak-field order",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def boundary_kernel_risk_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "risk_id": "BKR1946_0_qvertical_flux",
            "risk_channel": "q-vertical flux or boundary primitive",
            "why_it_matters": "Dq[v]=0 does not imply action-null if i_v Theta_parent has local boundary flux",
            "needed_control": "bulk null plus zero local boundary flux, or retained finite slip bound",
            "status": "RISK_OPEN",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "risk_id": "BKR1946_1_nonlocal_kernel_anisotropy",
            "risk_channel": "nonlocal memory kernel K_ij(x,x')",
            "why_it_matters": "kernel anisotropy can generate P_TF even when local algebraic terms are conformal",
            "needed_control": "prove local kernel O(3)-isotropic/common-mode or bound its TF projection",
            "status": "RISK_OPEN",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "risk_id": "BKR1946_2_source_worldtube_dyad",
            "risk_channel": "source/support/worldtube structure",
            "why_it_matters": "finite source or range averaging can introduce n_i n_j-type dyads",
            "needed_control": "derive isotropic averaging in the solar-system branch or include source-profile bound",
            "status": "RISK_OPEN",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "risk_id": "BKR1946_3_common_r2_mode",
            "risk_channel": "f=a r^2+b common-mode Hessian",
            "why_it_matters": "gamma-safe but can shift Newtonian/common-mode/cosmology gates",
            "needed_control": "route to Xi_N/effective-G/cosmological constant ledger rather than Cassini gamma",
            "status": "SEPARATE_COMMON_MODE_GATE",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1946_0_O3_conformal_lemma",
            "claim": "Algebraic O(3)-equivariant local residuals are conformal and have P_TF=0.",
            "status": "PASS_NONCLAIM",
            "reason": "conditional tensor lemma derived",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1946_1_hessian_kill_lemma",
            "claim": "The scalar Hessian slip channel is killed by f''=f'/r and bounded/decaying boundary conditions.",
            "status": "PASS_NONCLAIM",
            "reason": "ODE and solution family derived conditionally",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1946_2_parent_conformal_descent",
            "claim": "MTS parent action proves conformal descent for local R11.",
            "status": "FAIL_BLOCKED",
            "reason": "q-kernel nullness, no-dyad, and operator-domain exclusions are not signed",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1946_3_boundary_kernel_silence",
            "claim": "boundary/nonlocal kernels cannot generate local gamma slip",
            "status": "FAIL_BLOCKED",
            "reason": "boundary/domain/readout silence remains open",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1946_4_Cassini_gamma_pass",
            "claim": "MTS passes Cassini gamma through parent-zero R11 slip",
            "status": "FAIL_BLOCKED",
            "reason": "conditional zero route is not parent-signed and bound inputs remain missing",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1946_5_local_GR_PPN",
            "claim": "MTS derives local GR/PPN",
            "status": "FAIL_BLOCKED",
            "reason": "gamma slip is narrowed but not closed; other PPN/common-mode residuals remain",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1946_6_public_claim",
            "claim": "1946 is a public-ready local-GR proof",
            "status": "FAIL_BLOCKED",
            "reason": "private conditional theorem checkpoint only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1946_0_progress",
            "decision": "CONDITIONAL_CONFORMAL_AND_HESSIAN_KILL_LEMMAS_DERIVED",
            "reason": "we now know exactly how local R11 slip dies if the parent leaves only algebraic O(3) common-mode or bounded/decaying scalar Hessians",
            "next_action": "attempt boundary/kernel silence or source the Cassini slip bound inputs",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1946_1_block",
            "decision": "PARENT_CONFORMAL_DESCENT_NOT_CLAIMED",
            "reason": "1912/1913/1917 show q ownership and q-kernel action-nullness are still unsigned",
            "next_action": "do not use q-chain-rule alone as a local-GR proof",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1946_2_route",
            "decision": "NEXT_ATTACK_BOUNDARY_KERNEL_OR_NUMERIC_SLIP_BOUND",
            "reason": "the remaining danger is anisotropy from boundary/nonlocal kernel/source worldtube, or missing kappa_R/C_TF/U inputs",
            "next_action": "build 1947 boundary-kernel isotropy gate; if it fails, prepare numeric Cassini slip bound runner",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT1946_0_primary",
            "priority": "selected",
            "target_doc": "1947-Y5-R2FR-boundary-kernel-isotropy-or-Cassini-slip-bound-inputs.md",
            "target_script": "scripts/Y5_R2FR_boundary_kernel_isotropy_or_Cassini_slip_bound_inputs_1947.py",
            "objective": "prove local boundary/nonlocal kernels are O(3)-isotropic/common-mode and Hessian-safe, or build the coefficient/input ledger for a Cassini slip bound runner",
            "acceptance_output": "boundary-kernel silence theorem with parent clauses, or explicit kappa_R/C_TF/U/inverse-Laplacian/source-profile inputs with claim=false",
            "nonclaim_rule": "no Cassini/local-GR claim unless TF slip is parent-zero or bounded with real coefficients and boundary conditions",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1946_0_project_position",
            "status": "CONDITIONAL_LOCAL_SLIP_KILL_LEMMAS_READY_PARENT_SIGNATURE_OPEN",
            "strongest_result": "O(3) algebraic residuals are conformal, and radial Hessian slip vanishes iff f''=f'/r with bounded/decaying local scalars becoming silent",
            "what_improved": "the local-GR/Cassini route now has exact mathematical kill conditions rather than an informal plateau axiom",
            "still_missing": "parent no-dyad/q-kernel nullness/boundary-kernel silence or numeric slip-bound coefficients",
            "claim_status": "Cassini/local-GR public claims remain blocked",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_descent"], rows_by_name["descent_theorem_attempt"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["next_queue"], rows_by_name["next_target"])
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


def formalization_1946_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for _ in FORMALIZATION.rglob("*1946*"))


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
    rows.append(validation_row("VAL1946_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found" if sources_ok else "source path or needle missing"))

    theorem_statuses = {row["status"] for row in rows_by_name["descent_theorem_attempt"]}
    theorem_ok = "CONDITIONAL_O3_CONFORMAL_LEMMA_DERIVED" in theorem_statuses and "PARENT_CONFORMAL_DESCENT_NOT_CLOSED" in theorem_statuses
    rows.append(validation_row("VAL1946_01_descent_attempt", "PASS" if theorem_ok else "FAIL", "conditional conformal lemma derived and parent proof blocked"))

    hessian_text = "\n".join(row["status"] + " " + row["statement"] for row in rows_by_name["hessian_slip_kill"])
    hessian_ok = "HESSIAN_ZERO_ODE_DERIVED" in hessian_text and "BOUNDED_DECAY_KILLS_HESSIAN_SLIP_CONDITIONALLY" in hessian_text
    rows.append(validation_row("VAL1946_02_hessian_kill", "PASS" if hessian_ok else "FAIL", "Hessian slip ODE and bounded/decay kill condition recorded"))

    clause_ok = any(row["status"] == "THEOREM_NOT_CLOSED" for row in rows_by_name["conformal_clause_status"]) and all(row["claim_allowed"] == flag(False) for row in rows_by_name["conformal_clause_status"])
    rows.append(validation_row("VAL1946_03_clause_status", "PASS" if clause_ok else "FAIL", "conformal descent clauses remain nonclaim"))

    boundary_ok = all(row["status"] in {"RISK_OPEN", "SEPARATE_COMMON_MODE_GATE"} for row in rows_by_name["boundary_kernel_risk"])
    rows.append(validation_row("VAL1946_04_boundary_risk", "PASS" if boundary_ok else "FAIL", "boundary/kernel risks recorded"))

    claim_rows = rows_by_name["claim_gate"]
    claim_ok = len([row for row in claim_rows if row["status"] == "PASS_NONCLAIM"]) == 2 and len([row for row in claim_rows if row["status"] == "FAIL_BLOCKED"]) == 5
    rows.append(validation_row("VAL1946_05_claim_gates", "PASS" if claim_ok else "FAIL", "only conditional nonclaim gates pass; claims blocked"))

    decision_ok = any(row["decision"] == "NEXT_ATTACK_BOUNDARY_KERNEL_OR_NUMERIC_SLIP_BOUND" for row in rows_by_name["decision"])
    rows.append(validation_row("VAL1946_06_decision", "PASS" if decision_ok else "FAIL", "boundary/kernel or numeric slip route selected"))

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1947-Y5-R2FR-boundary-kernel-isotropy")
    rows.append(validation_row("VAL1946_07_next_target", "PASS" if next_ok else "FAIL", "1947 boundary-kernel target selected"))

    flags_ok = all(row.get("valid_for_claim") == flag(False) and row.get("claim_allowed") == flag(False) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1946_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = all(csv_has_rows(path) for path in output_paths)
    rows.append(validation_row("VAL1946_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    branch_ok = all(csv_has_rows(path) for path in BRANCH_COPIES.values())
    rows.append(validation_row("VAL1946_10_branch_copies", "PASS" if branch_ok else "FAIL", "; ".join(str(path) for path in BRANCH_COPIES.values())))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    rows.append(validation_row("VAL1946_11_pycache_absent", "PASS" if pycache_absent else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_1946_artifact_count()
    rows.append(validation_row("VAL1946_12_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1946_artifact_count={formalization_count}"))

    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(validation_row("VAL1946_OVERALL", "PASS" if overall_ok else "FAIL", "1946 parent conformal descent contract or Hessian slip kill"))
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
        "# 1946 Y5 R2FR: Parent Conformal Descent Contract or Hessian Slip Kill",
        "",
        "## Verdict",
        "",
        "1946 gets us closer to the local-GR/Cassini gate, but it does not close it. The useful gain is mathematical: if the local parent residual is algebraic and O(3)-equivariant with no surviving spatial dyad, then `R11_ij=S delta_ij`, so `P_TF[R11_ij]=0`. That is the clean conformal descent route.",
        "",
        "The Hessian danger is also sharpened. For a scalar memory Hessian `R11_ij=partial_i partial_j f(r)`, the slip source is proportional to `f''-f'/r`. Zero slip requires `f''=f'/r`, hence `f=a r^2+b`; with bounded/decaying local-vacuum boundary conditions and no admitted local `r^2` common mode, this collapses to a constant/silent scalar.",
        "",
        "The parent proof is still blocked because q-chain-rule silence is only pointwise geometry silence, not action-null or boundary-null silence. The current corpus does not yet sign no-dyad, q-kernel nullness, algebraic-only residuals, or boundary/kernel isotropy. So this is a stronger derivation map, not a Cassini pass.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Parent Descent Theorem Attempt",
        "",
        markdown_table(rows_by_name["descent_theorem_attempt"]),
        "",
        "## Hessian Slip Kill Lemma",
        "",
        markdown_table(rows_by_name["hessian_slip_kill"]),
        "",
        "## Conformal Descent Clause Status",
        "",
        markdown_table(rows_by_name["conformal_clause_status"]),
        "",
        "## Boundary/Kernel Risk Ledger",
        "",
        markdown_table(rows_by_name["boundary_kernel_risk"]),
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
        "descent_theorem_attempt": descent_theorem_attempt_rows(),
        "hessian_slip_kill": hessian_slip_kill_rows(),
        "conformal_clause_status": conformal_clause_status_rows(),
        "boundary_kernel_risk": boundary_kernel_risk_rows(),
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
