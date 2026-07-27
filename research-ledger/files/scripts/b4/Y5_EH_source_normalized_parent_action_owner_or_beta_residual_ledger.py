from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1585"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1585-Y5-EH-source-normalized-parent-action-owner-or-beta-residual-ledger.md"

SOURCE_FILES = {
    "1584_doc": ROOT / "1584-Y5-PPN-beta-conservation-common-matter-gate.md",
    "1584_validation": OUT / "P8_Y5_BRR545_1584_VALIDATION.csv",
    "1584_beta": OUT / "P8_Y5_PARENT_QLOC_1584_BETA_GATE.csv",
    "1584_conservation": OUT / "P8_Y5_PARENT_QLOC_1584_CONSERVATION_GATE.csv",
    "1584_matter": OUT / "P8_Y5_PARENT_QLOC_1584_COMMON_MATTER_GATE.csv",
    "1584_newton": OUT / "P8_Y5_PARENT_QLOC_1584_NEWTON_SOURCE_GATE.csv",
    "528_doc": ROOT / "528-Y5-EH-family-mass-parameter-route-or-beta-residual-fill.md",
    "527_doc": ROOT / "527-Y5-fill-A-B-from-source-equation-or-demote-beta-to-residual.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "439_doc": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
    "source_calibrated_eh_stack": OUT / "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
    "source_calibrated_eh_decision": OUT / "P8_Y5_SOURCE_CALIBRATED_EH_DECISION.csv",
    "source_calibrated_eh_validation": OUT / "P8_Y5_SOURCE_CALIBRATED_EH_VALIDATION.csv",
    "eh_1512_premises": OUT / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
    "local_eh_operator_audit": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "beta_envelope": OUT / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv",
    "delta_beta_law": OUT / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv",
    "r11_beta_vector": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1584_doc": ["NEXT_1585_EH_SOURCE_NORMALIZED_PARENT_ACTION_OWNER_OR_BETA_RESIDUAL_LEDGER", "gamma/q_R_hat branch is not local GR"],
    "1584_validation": ["VAL1584_OVERALL", "PASS"],
    "1584_beta": ["BETA1584_4_verdict", "FAIL_CURRENT_CLAIM_BETA_NOT_DERIVED"],
    "1584_conservation": ["CONS1584_1_projected_identity", "OBSTRUCTION_DERIVED_NOT_ZERO"],
    "1584_matter": ["MAT1584_4_verdict", "FAIL_CURRENT_CLAIM_COMMON_MATTER_NOT_DERIVED"],
    "1584_newton": ["NEW1584_4_verdict", "FAIL_CURRENT_CLAIM_NEWTON_SOURCE_NOT_DERIVED"],
    "528_doc": ["EH exterior + one measured mass parameter mu", "=> beta = 1"],
    "527_doc": ["B_source=A_source^2", "beta is a retained residual"],
    "523_doc": ["measured orbital `GM`", "scorecard_unfilled_no_claim"],
    "439_doc": ["P6_second_order_metric_equations", "central_blocker_not_derived"],
    "source_calibrated_eh_stack": ["SCEH529_5_isotropic_PPN_expansion", "SCEH529_7_beta_local_GR_gate"],
    "source_calibrated_eh_decision": ["D529_2_current_MTS_not_promoted", "local_GR_claim_false"],
    "source_calibrated_eh_validation": ["V529_6_no_overclaim", "local_GR_claim_allowed=false"],
    "eh_1512_premises": ["PRE1512_2_second_order", "CENTRAL_BLOCKER_NOT_DERIVED", "PRE1512_7_acceptance", "BLOCKED"],
    "local_eh_operator_audit": ["R2_fR_scalar_mode", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT"],
    "beta_envelope": ["ENV531_2_R11_operator_sum", "MISSING_R11_COEFFICIENT_VECTOR_OR_EH_NOHAIR"],
    "delta_beta_law": ["DB525_3_beta_residual", "delta_beta_source = B_source/A_source^2 - 1"],
    "r11_beta_vector": ["B530_0_source_AB", "B530_11_readout_frame"],
    "local_bounds": ["Will_2014_PPN_beta_table", "beta_minus_1", "7.8e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1585_SOURCE_REGISTER.csv"
OWNER_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1585_EH_SOURCE_OWNER_CONTRACT.csv"
CONDITIONAL_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1585_CONDITIONAL_GR_THEOREM_CHAIN.csv"
CURRENT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1585_CURRENT_CORPUS_OWNER_AUDIT.csv"
BETA_RESIDUAL_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv"
LOCAL_GR_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1585_LOCAL_GR_REDUCTION_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1585_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1585_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1585_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1585_VALIDATION.csv"

COPY_TARGETS = {
    OWNER_CONTRACT: [
        QUARANTINE / "EH_SOURCE_OWNER_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "EH_source_owner_contract_nonclaim_1585.csv",
    ],
    CONDITIONAL_THEOREM: [
        QUARANTINE / "CONDITIONAL_GR_THEOREM_CHAIN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "conditional_GR_theorem_chain_nonclaim_1585.csv",
    ],
    CURRENT_AUDIT: [
        QUARANTINE / "CURRENT_CORPUS_OWNER_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "current_corpus_owner_audit_nonclaim_1585.csv",
    ],
    BETA_RESIDUAL_LEDGER: [
        QUARANTINE / "BETA_RESIDUAL_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "beta_residual_ledger_nonclaim_1585.csv",
    ],
    LOCAL_GR_RUNNER: [
        QUARANTINE / "LOCAL_GR_REDUCTION_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "local_GR_reduction_runner_nonclaim_1585.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "EH_source_owner_or_beta_residual_decision_nonclaim_1585.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1585_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "EH source-normalized parent action owner attempt and beta residual fallback",
                **flags(),
            }
        )
    return rows


def owner_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OWN1585_0_parent_action",
            "single parent action owner",
            "S_parent supplies the observed metric/coframe, EH-like local operator, matter action, source normalization, boundary policy and all retained residual sectors in one variation",
            "prevents mixing an MTS source law with imported GR dynamics",
            "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "no single varied parent action currently owns all pieces",
        ),
        (
            "OWN1585_1_EH_operator",
            "EH-only local exterior operator",
            "E_ext^{mu nu}=a G^{mu nu}+b g^{mu nu} plus theorem-zero/topological or explicitly bounded retained H_i^{mu nu}",
            "gives the GR nonlinear operator that generates beta=1 for the one-parameter exterior",
            "MISSING_EH_ONLY_PARENT_SIGNATURE",
            "second-order metric-only, Levi-Civita and no-extra-field premises remain open",
        ),
        (
            "OWN1585_2_universal_matter",
            "universal Hilbert matter/source coupling",
            "S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A] and J_H is the source current used by the field equation",
            "ties clocks, rods, photons, source variation and PPN readout to the same geometry",
            "MISSING_COMMON_MATTER_SIGNATURE",
            "coframe ownership, tau lock, no-marker and matter descent remain unsigned",
        ),
        (
            "OWN1585_3_measured_GM",
            "source-normalized measured mass parameter",
            "mu_EH=mu_obs=G0 M_H[Pi_M J_H] with zero extra flux, zero derivative hair and fixed normalization",
            "makes the nonlinear EH mass parameter the measured orbital Newtonian potential",
            "MISSING_SOURCE_DENOMINATOR",
            "Gauss/orbital/source-current scorecard remains unfilled",
        ),
        (
            "OWN1585_4_no_quadratic_leakage",
            "no independent U^2 residual leakage",
            "delta_beta_R11=delta_beta_q_loc=delta_beta_boundary=delta_beta_readout=0 or each is source-backed below lock",
            "prevents beta=1 being spoiled after the EH/source route is selected",
            "MISSING_SECOND_ORDER_RESIDUAL_CONTROL",
            "R11 vector, q_loc U2 normalization, boundary/domain and readout rows remain open",
        ),
        (
            "OWN1585_5_verdict",
            "source-normalized EH parent owner",
            "OWN1585_0 through OWN1585_4 are parent-signed or explicitly bounded without cancellation",
            "would allow beta/conservation/common matter/Newton gates to be re-run as a serious local-GR candidate",
            "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED",
            "the current corpus has the contract, not the parent-signed owner",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "owner_id": owner_id,
            "contract_piece": contract_piece,
            "required_statement": required_statement,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for owner_id, contract_piece, required_statement, effect_if_signed, status, blocking_gap in rows
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "THM1585_0_assume_owner",
            "Assume the same parent action supplies EH-only exterior equations, universal matter coupling, source-normalized mu and no quadratic residual leakage.",
            "OWN1585_0..OWN1585_4 all signed",
            "local branch may be solved as one observed EH mass-family problem",
            "CONDITIONAL_PREMISE",
        ),
        (
            "THM1585_1_bianchi",
            "Diffeomorphism invariance of the signed EH plus same-frame matter action gives the source-compatible Bianchi/Ward identity.",
            "nabla_mu G^{mu nu}=0 and E_matter=0 imply nabla_mu T_H^{mu nu}=0 in the observed frame",
            "projected conservation obstruction terms must vanish or be retained as explicit residuals",
            "CONDITIONAL_THEOREM_NOT_CURRENT_MTS_DERIVED",
        ),
        (
            "THM1585_2_newton",
            "The weak-field 00 equation with the same Hilbert source gives the Poisson coefficient for measured U.",
            "nabla^2 U=4 pi G0 rho_H and mu_EH=mu_obs",
            "Newtonian source denominator closes only if measured-GM calibration lands",
            "CONDITIONAL_THEOREM_NOT_CURRENT_MTS_DERIVED",
        ),
        (
            "THM1585_3_beta",
            "The one-parameter EH exterior makes the quadratic coefficient the square of the first-order mass amplitude.",
            "g00=-1+2U/c^2-2U^2/c^4+O(c^-6), so beta_eff=1",
            "beta=1 follows only after no extra U^2 source/operator/readout leakage is proven",
            "CONDITIONAL_THEOREM_NOT_CURRENT_MTS_DERIVED",
        ),
        (
            "THM1585_4_common_matter",
            "Because all matter sectors use the same observed coframe, the PPN readout and source law are common rather than species/frame dependent.",
            "e_source=e_matter=e_clock=e_orbit=e_obs through O(U^2)",
            "WEP/clock/orbital gates can share one local geometry only if tau/coframe locks close",
            "CONDITIONAL_THEOREM_NOT_CURRENT_MTS_DERIVED",
        ),
        (
            "THM1585_5_limit",
            "The theorem is a clean target, not current evidence.",
            "conditional_owner => beta=1 and compatible local GR spine; current_MTS_owner=false",
            "do not claim GR until the owner audit flips or the residual ledger scores below locks",
            "REFERENCE_CONTRACT_ONLY_NO_CLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_step_id": theorem_step_id,
            "statement": statement,
            "math_form": math_form,
            "consequence": consequence,
            "status": status,
            **flags(),
        }
        for theorem_step_id, statement, math_form, consequence, status in rows
    ]


def current_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AUD1585_0_EH_operator",
            "EH-only metric operator",
            "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
            "PRE1512_2_second_order is CENTRAL_BLOCKER_NOT_DERIVED and PRE1512_7_acceptance is BLOCKED",
            "FAIL_OPEN",
            "cannot use Lovelock/EH route as current MTS proof",
        ),
        (
            "AUD1585_1_R11_vector",
            "non-EH operator families",
            "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
            "R2/fR, Ricci/Weyl squared, scalar, vector, torsion, bulk, memory, source-normalization and projector families have missing zero/numeric coefficients",
            "FAIL_OPEN",
            "non-EH U2 and local-test leakage cannot be silently dropped",
        ),
        (
            "AUD1585_2_source_calibration",
            "measured GM source denominator",
            "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
            "scorecard_unfilled_no_claim and measured-GM parent derivation remains false",
            "FAIL_OPEN",
            "mu_EH cannot yet be identified with observed orbital GM",
        ),
        (
            "AUD1585_3_beta_source",
            "A/B source normalization",
            "527-Y5-fill-A-B-from-source-equation-or-demote-beta-to-residual.md",
            "B_source=A_source^2 is the safe route, but beta remains a retained residual",
            "FAIL_OPEN",
            "no second-order source equation currently supplies A_source and B_source",
        ),
        (
            "AUD1585_4_common_matter",
            "same coframe/tau matter coupling",
            "P8_Y5_PARENT_QLOC_1584_COMMON_MATTER_GATE.csv",
            "MAT1584_4_verdict is FAIL_CURRENT_CLAIM_COMMON_MATTER_NOT_DERIVED",
            "FAIL_OPEN",
            "universal matter coupling cannot be assumed",
        ),
        (
            "AUD1585_5_conservation",
            "projected source-compatible conservation",
            "P8_Y5_PARENT_QLOC_1584_CONSERVATION_GATE.csv",
            "CONS1584_1_projected_identity keeps extra-current, commutator and anomaly obstruction terms",
            "FAIL_OPEN",
            "total Ward conservation is not enough",
        ),
        (
            "AUD1585_6_verdict",
            "current parent-owner status",
            "this 1585 audit",
            "no required owner clause is parent-signed across EH operator, source normalization, common matter and second-order leakage",
            "FAIL_CURRENT_CLAIM_OWNER_NOT_DERIVED",
            "route stays private/nonclaim and falls back to finite residual ledger",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "gate": gate,
            "source_path": source_path,
            "evidence": evidence,
            "status": status,
            "consequence": consequence,
            **flags(),
        }
        for audit_id, gate, source_path, evidence, status, consequence in rows
    ]


def beta_residual_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BRL1585_0_delta_beta_source",
            "delta_beta_source",
            "B_source/A_source^2 - 1",
            "A_source, B_source or parent proof B_source=A_source^2",
            "MISSING_A_B_SOURCE_EQUATION_OR_EH_MASS_FAMILY_OWNER",
            "dimensionless",
            "beta_minus_1 <= 7.8e-05 or theorem-zero",
        ),
        (
            "BRL1585_1_delta_beta_R11",
            "sum_abs_delta_beta_R11_i",
            "absolute sum over R11 beta component vector",
            "EH-only theorem-zero or executable R11 coefficient vector",
            "MISSING_R11_COEFFICIENT_VECTOR_OR_EH_NOHAIR",
            "dimensionless",
            "beta/gamma/preferred-frame locks by family",
        ),
        (
            "BRL1585_2_delta_beta_q_loc",
            "delta_beta_q_loc",
            "physical U2 projection of P_loc(nabla Gamma_eff-div Khat)",
            "Ward-zero through O(U2) or beta-normalized q_loc profile",
            "PROVISIONAL_BUDGET_NOT_VALID_FOR_CLAIM",
            "dimensionless",
            "beta lock plus alpha_i/xi leak checks",
        ),
        (
            "BRL1585_3_delta_beta_boundary_domain",
            "delta_beta_boundary_domain",
            "boundary/domain/projector quadratic stress beta projection",
            "no-flux/no-hair theorem or coefficient map with units",
            "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP",
            "dimensionless",
            "beta, alpha3, xi and Gdot locks",
        ),
        (
            "BRL1585_4_delta_beta_readout",
            "delta_beta_readout",
            "second-order mismatch between source metric and observed isotropic PPN readout",
            "same observed coframe/readout theorem through O(U2)",
            "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2",
            "dimensionless",
            "WEP/clock/gamma/beta locks",
        ),
        (
            "BRL1585_5_conservation_projected_obstruction",
            "Delta_conservation",
            "-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "projected extra-current zero, commutator zero, anomaly zero or sourced finite bounds",
            "MISSING_PROJECTED_CONSERVATION_ZERO_OR_BOUNDS",
            "dimensionless_or_GM_flux_units",
            "beta/Gdot/radial source hair/local-GR gates",
        ),
        (
            "BRL1585_6_measured_GM_denominator",
            "epsilon_SN",
            "(mu_obs-G_eff M_H)/(G_eff M_H)",
            "full Gauss/orbital/source-current scorecard",
            "MISSING_SOURCE_NORMALIZATION_SCORECARD",
            "dimensionless",
            "Newton, beta and local-GR precondition",
        ),
        (
            "BRL1585_7_total_no_cancellation",
            "Delta_beta_total_abs",
            "sum_i abs(beta residual components) with no cancellation credit",
            "all prior rows theorem-zero or numeric/source-backed and unit-normalized",
            "NOT_RUN_COMPONENTS_MISSING",
            "dimensionless",
            "Delta_beta_total_abs <= 7.8e-05",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "formula_or_map": formula_or_map,
            "required_input": required_input,
            "current_status": current_status,
            "units": units,
            "bound_or_target": bound_or_target,
            "no_cancellation": True,
            **flags(),
        }
        for residual_id, symbol, formula_or_map, required_input, current_status, units, bound_or_target in rows
    ]


def local_gr_runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1585_0_conditional_owner",
            "use conditional EH/source owner theorem as current MTS evidence",
            "REFUSE_REFERENCE_PROMOTION",
            "the theorem is exact as a target but the owner clauses are not parent-signed",
        ),
        (
            "RUN1585_1_beta_score",
            "score beta bound using residual ledger",
            "NOT_RUN_COMPONENTS_MISSING",
            "delta_beta_source, R11, boundary/domain, readout and conservation/source-denominator rows are missing",
        ),
        (
            "RUN1585_2_newton_to_gr",
            "promote first-order Newton/source calibration to GR",
            "REFUSE_PLACEHOLDER",
            "source-normalized Newton and second-order PPN beta are separate gates",
        ),
        (
            "RUN1585_3_total_ward",
            "use total Ward identity as local source-compatible Bianchi proof",
            "REFUSE_PLACEHOLDER",
            "projected Hilbert source obstruction remains active",
        ),
        (
            "RUN1585_4_current_local_gr",
            "claim derived local GR branch",
            "BLOCKED_NO_CLAIM",
            "EH operator, measured-GM source, common matter, conservation and beta envelope are not closed",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            **flags(),
        }
        for runner_id, case, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1585_0_parent_owner", "source-normalized EH parent owner", "BLOCKED_NO_CLAIM", "owner clauses are written but not parent-signed"),
        ("GATE1585_1_beta", "beta=1 or beta-bound pass", "BLOCKED_NO_CLAIM", "beta residual ledger is unfilled and conditional theorem is not current evidence"),
        ("GATE1585_2_conservation", "source-compatible Bianchi pass", "BLOCKED_NO_CLAIM", "projected conservation obstruction remains"),
        ("GATE1585_3_newton", "source-normalized Newton pass", "BLOCKED_NO_CLAIM", "measured-GM denominator is unfilled"),
        ("GATE1585_4_local_gr", "derived local GR reduction", "BLOCKED_NO_CLAIM", "all local-GR rungs must close under one parent action or finite residual score"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1585_0_clean_route",
            "CONDITIONAL_EH_SOURCE_OWNER_ROUTE_IS_VALID_TARGET",
            "if the same parent action owns EH operator, universal matter, source-normalized mu and no quadratic leakage, then beta=1/conservation/common matter follow in the local branch",
            "keep this as the route to real GR reduction, not as a present claim",
        ),
        (
            "DEC1585_1_current_status",
            "CURRENT_CORPUS_OWNER_NOT_DERIVED",
            "existing 1512/523/527/528/529/1584 evidence leaves EH-only, measured-GM, common matter, conservation and U2 leakage open",
            "retain nonclaim status",
        ),
        (
            "DEC1585_2_residual_fallback",
            "BETA_RESIDUAL_LEDGER_ACTIVE",
            "if the parent owner cannot be derived soon, beta must be handled by component residual rows and no-cancellation envelope",
            "no beta comparator run until component inputs are real",
        ),
        (
            "DEC1585_3_next",
            "NEXT_1586_PARENT_MINIMALITY_NO_EXTRA_SECTOR_SIGNATURE_OR_R11_BETA_VECTOR_FILL",
            "the highest-leverage derivation is the primitive minimality/no-extra-sector signature that would kill R11/non-EH beta leakage; fallback is filling the executable R11 beta vector",
            "derive first; if unsigned, fill source-backed R11 beta components without claiming local GR",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1586-Y5-parent-minimality-no-extra-sector-signature-or-R11-beta-vector-fill.md",
            "script": "scripts/Y5_parent_minimality_no_extra_sector_signature_or_R11_beta_vector_fill.py",
            "objective": "try to derive a primitive parent minimality/no-extra-sector signature that kills non-EH R11 beta leakage; if it fails, fill the R11 beta component vector with sourced nonclaim rows",
            "do_not": "do not promote the conditional EH theorem, first-order Newton, total Ward conservation, or reference GR rows into MTS local-GR evidence",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1585_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1585" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    owners = read_csv(OWNER_CONTRACT)
    theorem = read_csv(CONDITIONAL_THEOREM)
    audit = read_csv(CURRENT_AUDIT)
    residuals = read_csv(BETA_RESIDUAL_LEDGER)
    runner = read_csv(LOCAL_GR_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_residuals = {
        "delta_beta_source",
        "sum_abs_delta_beta_R11_i",
        "delta_beta_q_loc",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "Delta_conservation",
        "epsilon_SN",
        "Delta_beta_total_abs",
    }
    required_claims = {
        "source-normalized EH parent owner",
        "beta=1 or beta-bound pass",
        "source-compatible Bianchi pass",
        "source-normalized Newton pass",
        "derived local GR reduction",
    }
    checks = [
        ("VAL1585_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1585 source paths exist"),
        ("VAL1585_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1585 source needles found"),
        (
            "VAL1585_2_owner_contract_written_not_claimed",
            any(row["owner_id"] == "OWN1585_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED" for row in owners),
            "source-normalized EH parent owner contract is explicit but not promoted",
        ),
        (
            "VAL1585_3_conditional_theorem_guarded",
            any(row["theorem_step_id"] == "THM1585_3_beta" and row["status"] == "CONDITIONAL_THEOREM_NOT_CURRENT_MTS_DERIVED" for row in theorem)
            and any(row["theorem_step_id"] == "THM1585_5_limit" and row["status"] == "REFERENCE_CONTRACT_ONLY_NO_CLAIM" for row in theorem),
            "conditional beta=1 theorem is written with reference-only guard",
        ),
        (
            "VAL1585_4_current_audit_fails_open",
            any(row["audit_id"] == "AUD1585_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_OWNER_NOT_DERIVED" for row in audit)
            and all(row["claim_allowed"] == "False" for row in audit),
            "current corpus owner audit fails open and does not claim",
        ),
        (
            "VAL1585_5_beta_residual_schema",
            {row["symbol"] for row in residuals} == required_residuals
            and all(row["no_cancellation"] == "True" for row in residuals)
            and any(row["symbol"] == "Delta_beta_total_abs" and row["current_status"] == "NOT_RUN_COMPONENTS_MISSING" for row in residuals),
            "beta residual ledger contains all current components and no-cancellation total",
        ),
        (
            "VAL1585_6_runner_blocks",
            all(row["can_score"] == "False" for row in runner)
            and any(row["runner_id"] == "RUN1585_4_current_local_gr" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner),
            "local-GR runner blocks reference promotion and scoring",
        ),
        (
            "VAL1585_7_claim_gates_closed",
            {row["claim"] for row in gates} == required_claims
            and all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates),
            "all 1585 claim gates remain closed",
        ),
        (
            "VAL1585_8_decision_next",
            any(row["decision"] == "NEXT_1586_PARENT_MINIMALITY_NO_EXTRA_SECTOR_SIGNATURE_OR_R11_BETA_VECTOR_FILL" for row in decisions),
            "decision selects parent minimality/no-extra-sector signature or R11 beta vector fill",
        ),
        ("VAL1585_9_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1585 CSVs parse cleanly"),
        ("VAL1585_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1585_11_no_raw_accepted", not has_1585_rows(RAB_RAW) and not has_1585_rows(RAB_ACCEPTED), "no 1585 rows written to raw/accepted finite directories"),
        ("VAL1585_12_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1585_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1585_14_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1585 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1585_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1585 EH source-normalized parent action owner or beta residual ledger validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1585 - EH Source-Normalized Parent Action Owner Or Beta Residual Ledger",
                "## Verdict\n"
                "- The clean GR route is now exact as a contract: one parent action must own the EH-like local operator, universal matter coupling, source-normalized measured mass, source-compatible conservation and all second-order residual silence.\n"
                "- Under that contract, the local one-parameter EH exterior gives `B=A^2`, `beta=1`, compatible Bianchi/Ward conservation and common matter readout.\n"
                "- Current MTS does not yet earn the contract: EH-only/no-extra-sector, measured-GM, projected conservation, common matter and U2 leakage gates remain open.\n"
                "- Therefore beta is retained as a no-cancellation residual ledger rather than claimed from the conditional theorem.\n"
                "- No beta, Newton, PPN, local-GR, R10, WEP, clock, orbital, conservation or common-matter claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## EH Source Owner Contract",
                md_table(owners, ["owner_id", "contract_piece", "required_statement", "effect_if_signed", "status", "blocking_gap"]),
                "## Conditional GR Theorem Chain",
                md_table(theorem, ["theorem_step_id", "statement", "math_form", "consequence", "status"]),
                "## Current Corpus Owner Audit",
                md_table(audit, ["audit_id", "gate", "source_path", "evidence", "status", "consequence"]),
                "## Beta Residual Ledger",
                md_table(residuals, ["residual_id", "symbol", "formula_or_map", "required_input", "current_status", "units", "bound_or_target", "no_cancellation"]),
                "## Local GR Reduction Runner",
                md_table(runner, ["runner_id", "case", "status", "reason", "can_score"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    owners = owner_contract_rows()
    theorem = conditional_theorem_rows()
    audit = current_audit_rows()
    residuals = beta_residual_ledger_rows()
    runner = local_gr_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        OWNER_CONTRACT,
        CONDITIONAL_THEOREM,
        CURRENT_AUDIT,
        BETA_RESIDUAL_LEDGER,
        LOCAL_GR_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_CONTRACT, owners)
    write_csv(CONDITIONAL_THEOREM, theorem)
    write_csv(CURRENT_AUDIT, audit)
    write_csv(BETA_RESIDUAL_LEDGER, residuals)
    write_csv(LOCAL_GR_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, owners, theorem, audit, residuals, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
