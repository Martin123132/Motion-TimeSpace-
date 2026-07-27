from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2206"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2206_SOURCE_REGISTER.csv",
    "ward_identity": OUT / "P8_Y5_PARENT_QLOC_2206_WARD_IDENTITY_DERIVATION.csv",
    "signature_audit": OUT / "P8_Y5_PARENT_QLOC_2206_PARENT_SIGNATURE_AUDIT.csv",
    "residual_demotion": OUT / "P8_Y5_PARENT_QLOC_2206_OFFICIAL_RESIDUAL_DEMOTION.csv",
    "arena_projection": OUT / "P8_Y5_PARENT_QLOC_2206_ARENA_PROJECTION_QUEUE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2206_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2206_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2206_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2206_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2206_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2206_GK_QLOC_OFFICIAL_RESIDUAL_DEMOTION_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2206_PARENT_SIGNATURE_AUDIT_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_WARD_IDENTITY_2206_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2206_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2206-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2206*",
        "*P8_Y5_BRR545_2206*",
        "*Y5_R2FR_GammaKhat_q_loc_parent_action_signature_or_official_residual_demotion_2206*",
        "*JR2206*",
        "*PARENT_QLOC_WARD_IDENTITY_2206*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2205_handoff",
            ROOT / "2205-Y5-R2FR-current-frontier-EH-descent-PiM-source-readout-synthesis.md",
            ["NEXT2205_0_2206", "SEL2205_1_success", "VAL2205_OVERALL"],
            "2205 selects Gamma/Khat/q_loc parent-signature derivation or official residual demotion.",
        ),
        (
            "2190_gk_qloc_gate",
            ROOT / "2190-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
            ["DG2190_9_verdict", "CR2190_F_residual_lock", "VAL2190_OVERALL"],
            "2190 writes the exact q_loc zero theorem chain and keeps residual lock active.",
        ),
        (
            "2191_qloc_runner",
            ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md",
            ["TZ2191_8_all_or_nothing", "RUN2191_6_theorem_zero", "VAL2191_OVERALL"],
            "2191 makes q_loc executable as vector/profile and theorem-zero certificate slots.",
        ),
        (
            "1010_action_helmholtz",
            ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "V1010_SUMMARY"],
            "1010 provides the first action/metric-response/Helmholtz schema for q_loc.",
        ),
        (
            "GK_first_variation_contract",
            OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            ["GK513_0_action_existence", "GK513_5_boundary_no_flux"],
            "first variation contract lists the action, Helmholtz, Euler, double-zero, P_loc, and boundary clauses.",
        ),
        (
            "GK_action_candidates",
            OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
            ["GK514_A_metric_response_scalar_density", "GK514_D_residual_branch"],
            "candidate action rows identify metric-response scalar density, auxiliary, topological, and residual branches.",
        ),
        (
            "GK_metric_response_audit",
            OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            ["MA515_1_Khat_metric_response", "MA515_6_units_and_readout"],
            "metric-response audit says Gamma/Khat are not yet matched as one variational stress with units.",
        ),
        (
            "Gamma_owner_candidates",
            OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner"],
            "Gamma owner candidates preserve the response-doublet route and fallback residual runner.",
        ),
        (
            "2189_inventory",
            ROOT / "2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md",
            ["EI2189_0_GK", "PR2189_0_GK", "VAL2189_OVERALL"],
            "2189 ranks Gamma/Khat/q_loc as the first hard extra-sector obstruction.",
        ),
        (
            "2198_component_pressure",
            ROOT / "2198-Y5-R2FR-beta-source-zero-or-bounded-component-pack.md",
            ["BCV2198_6_total", "TBG2198_3_vector_tail", "VAL2198_OVERALL"],
            "2198 supplies the no-cancellation component-vector discipline and proxy-pressure warning.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def ward_identity_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            derivation_id="WID2206_0_define_stress",
            statement="Define T_GK^{mu nu}:=K_hat^{mu nu}-Gamma_eff g^{mu nu} in the same metric, volume, and boundary convention.",
            algebraic_result="nabla_mu T_GK^{mu nu}=nabla_mu K_hat^{mu nu}-nabla^nu Gamma_eff",
            implication="q_loc^nu=-P_loc nabla_mu T_GK^{mu nu}",
            proof_status="DERIVED_ALGEBRAIC_IDENTITY",
            missing_for_claim="actual MTS K_hat/Gamma_eff must be source-matched to this T_GK",
        ),
        base_row(
            derivation_id="WID2206_1_if_parent_action",
            statement="If T_GK is the Hilbert stress of a local diffeomorphism-invariant parent action S_GK[g,Phi], Noether/Ward gives nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A plus boundary/support terms.",
            algebraic_result="q_loc^nu=-P_loc(sum_A E_A nabla^nu Phi^A + B_GK^nu + S_GK_source^nu)",
            implication="compact local vacuum can set q_loc=0 only after Euler, source, projector and boundary clauses are signed",
            proof_status="CONDITIONAL_FIELD_THEORY_THEOREM",
            missing_for_claim="parent action owner, Euler closure, source silence, P_loc owner, and no-flux boundary certificate",
        ),
        base_row(
            derivation_id="WID2206_2_double_zero_upgrade",
            statement="If T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 at the compact local fixed point, the first-order local leakage F1_GK vanishes.",
            algebraic_result="F1_GK=0 under parent-signed C0 and dC double-zero clauses",
            implication="q_loc hair begins only at bounded second order or disappears on shell",
            proof_status="CONDITIONAL_DOUBLE_ZERO_LAW",
            missing_for_claim="Gamma/Khat fixed-point expansion and parent-signed first-variation zero",
        ),
        base_row(
            derivation_id="WID2206_3_projection_boundary_guard",
            statement="The projected theorem is valid only if P_loc is parent-owned before readout and boundary/symplectic flux is zero or explicitly retained.",
            algebraic_result="P_loc q=0 does not follow from unprojected bookkeeping if nabla P_loc, support motion, or boundary flux survive",
            implication="P_loc and boundary are not optional decorations; they are theorem clauses",
            proof_status="GUARDRAIL_DERIVED_FROM_INTERFACE",
            missing_for_claim="P_loc commutator zero, fixed domain/support, and theta_GK/Q_GK no-flux proof",
        ),
        base_row(
            derivation_id="WID2206_4_current_verdict",
            statement="The Ward route is the right route, but current sources do not parent-sign it for actual MTS Gamma/Khat.",
            algebraic_result="theorem_zero_q_loc=false; official_residual_demotion=true",
            implication="q_loc remains the local-test residual vector for PPN/R10/R11/clock/orbital arenas",
            proof_status="DERIVATION_ATTEMPT_FAILED_CURRENT_CORPUS",
            missing_for_claim="source-signed S_GK, metric response, Helmholtz, Euler, double-zero, P_loc and boundary clauses",
        ),
    ]


def signature_audit_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "PSA2206_0_action_owner",
            "S_GK_parent_action",
            "S_GK[g,Phi] is a local diffeomorphism-invariant scalar action whose Hilbert stress is T_GK=Khat-Gamma*g",
            "MISSING_PARENT_SIGNED_S_GK",
            "1010/GK514 only provide candidate actions; MA515 says Gamma scalar density owner is missing",
            "q_action_owner_defect",
        ),
        (
            "PSA2206_1_metric_response",
            "Khat_metric_response",
            "K_hat equals the metric response of sqrt(-g)Gamma_eff, including derivative and boundary terms under a fixed convention",
            "MISSING_PARENT_SIGNED_METRIC_RESPONSE",
            "MA515_1 fails current claim; Khat is not computed from a proposed Gamma_eff",
            "q_metric_response_defect",
        ),
        (
            "PSA2206_2_Helmholtz",
            "Helmholtz_integrability",
            "the second metric variation of sqrt(-g)T_GK is symmetric up to allowed boundary terms",
            "MISSING_HELMHOLTZ_CERTIFICATE",
            "1010 says integrability is not checked for current symbols",
            "q_Helmholtz_defect",
        ),
        (
            "PSA2206_3_Euler_Ward",
            "Euler_Ward_closure",
            "the fields in S_GK satisfy E_A=0 in compact local vacuum and all source-current terms are absent",
            "MISSING_EULER_SOURCE_ZERO",
            "Ward route is conditional; source/support current silence is not parent-signed",
            "q_Euler_source_defect",
        ),
        (
            "PSA2206_4_double_zero",
            "T_GK_double_zero",
            "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 for the local fixed point",
            "MISSING_GK_DOUBLE_ZERO_EXPANSION",
            "GO516 response-doublet could work, but is not derived for physical q_loc components",
            "epsilon_C0_GammaKhat;epsilon_dC_GammaKhat",
        ),
        (
            "PSA2206_5_Ploc",
            "P_loc_parent_owner",
            "P_loc is selected by the parent branch before readout and its commutator/variation is zero or retained",
            "MISSING_PLOC_OWNER_AND_COMMUTATOR",
            "2190/2191 retain P_loc commutator as live residual",
            "q_Ploc_commutator",
        ),
        (
            "PSA2206_6_boundary",
            "boundary_symplectic_no_flux",
            "theta_GK/Q_GK boundary, support, and compact-collar flux vanish or are retained as explicit rows",
            "MISSING_GK_BOUNDARY_NO_FLUX",
            "boundary no-flux remains open in 1010 and 2190",
            "q_GK_boundary_flux",
        ),
        (
            "PSA2206_7_units_readout",
            "units_and_observable_response",
            "Gamma/Khat/q_loc have declared units and response maps into PPN/R10/R11/clock/orbital observables",
            "MISSING_UNITS_AND_RESPONSE_OPERATORS",
            "MA515_6 and 2191 leave units/readout maps source-missing",
            "q_units_response_defect",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for clause_id, clause, required, status, evidence, residual in clauses:
        rows.append(
            base_row(
                clause_id=clause_id,
                clause=clause,
                required_statement=required,
                current_status=status,
                parent_signed=False,
                passes_now=False,
                evidence=evidence,
                residual_if_missing=residual,
                theorem_zero_component=False,
            )
        )
    rows.append(
        base_row(
            clause_id="PSA2206_8_all_or_nothing",
            clause="q_loc_theorem_zero",
            required_statement="q_loc=0 can be promoted only if every PSA2206_0..PSA2206_7 clause passes in one parent branch",
            current_status="THEOREM_ZERO_FALSE_OFFICIAL_RESIDUAL_DEMOTION",
            parent_signed=False,
            passes_now=False,
            evidence="at least one required parent signature is missing; in fact all core clauses remain unsigned",
            residual_if_missing="q_loc_residual_vector_abs",
            theorem_zero_component=False,
        )
    )
    return rows


def residual_demotion_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "QDEM2206_0_action",
            "q_action_owner_defect",
            "missing parent action owner for Gamma/Khat stress",
            "MISSING_PARENT_SIGNED_S_GK",
            "stress_divergence_or_force_density",
            "local_GR;PPN",
            "acquire explicit S_GK or keep defect as live residual",
        ),
        (
            "QDEM2206_1_metric",
            "q_metric_response_defect",
            "K_hat minus metric response of sqrt(-g)Gamma_eff",
            "MISSING_KHAT_METRIC_RESPONSE",
            "stress_divergence_or_force_density",
            "PPN;R10;local_GR",
            "compute K_metric from candidate Gamma_eff and compare tensor structure",
        ),
        (
            "QDEM2206_2_helmholtz",
            "q_Helmholtz_defect",
            "antisymmetric second-variation obstruction for proposed T_GK",
            "MISSING_HELMHOLTZ_INTEGRABILITY",
            "stress_response_operator_norm",
            "PPN;local_GR",
            "run explicit Helmholtz symmetry test after S_GK candidate is fixed",
        ),
        (
            "QDEM2206_3_euler",
            "q_Euler_source_defect",
            "sum_A E_A nabla^nu Phi^A plus source/support terms in compact local vacuum",
            "MISSING_EULER_SOURCE_ZERO",
            "force_density",
            "PPN;clocks;orbital",
            "derive source-current zero or stage finite source-current bound",
        ),
        (
            "QDEM2206_4_C0",
            "epsilon_C0_GammaKhat",
            "zeroth-order T_GK/GammaKhat amplitude at Phi0",
            "MISSING_TGK_ZERO",
            "dimensionless_or_stress_norm",
            "PPN;R10;local_GR",
            "expand Gamma/Khat around Phi0 and test background subtraction",
        ),
        (
            "QDEM2206_5_dC",
            "epsilon_dC_GammaKhat",
            "first variation partial_A T_GK(Phi0)",
            "MISSING_TGK_DERIVATIVE_ZERO",
            "dimensionless_operator_norm",
            "PPN;R10;local_GR",
            "derive response-doublet or fixed-point symmetry that kills linear hair",
        ),
        (
            "QDEM2206_6_Ploc",
            "q_Ploc_commutator",
            "derivative/readout commutator (nabla_mu P_loc)K_hat and kernel leakage",
            "MISSING_PLOC_OWNER_AND_COMMUTATOR",
            "force_density_or_dimensionless_after_projection",
            "PPN_alpha_i;WEP;local_GR",
            "derive parent projector/domain lock or source finite commutator bound",
        ),
        (
            "QDEM2206_7_boundary",
            "q_GK_boundary_flux",
            "compact local boundary/symplectic flux from theta_GK/Q_GK",
            "MISSING_GK_BOUNDARY_NO_FLUX",
            "force_flux_or_GM_flux",
            "Newton;R10;R11;PPN",
            "derive no-flux on compact collars or stage boundary-flux row",
        ),
        (
            "QDEM2206_8_metric_footprint",
            "q_Khat_metric_footprint",
            "metric/PPN response from Khat carrier amplitude even if divergence cancellation works",
            "MISSING_METRIC_RESPONSE_MATRIX",
            "PPN_vector_or_metric_coefficients",
            "PPN;clocks;orbital",
            "build metric response matrix before scoring beta/gamma/alpha_i",
        ),
        (
            "QDEM2206_9_total",
            "q_loc_residual_vector_abs",
            "absolute no-cancellation envelope across all q_loc defects",
            "MISSING_COMPONENT_INPUTS",
            "arena_normalized_vector",
            "local_GR;PPN;R10;R11;clocks;orbital",
            "sum source-backed component bounds only after response operators exist",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, definition, status, units, observable_link, next_action in specs:
        rows.append(
            base_row(
                row_id=row_id,
                symbol=symbol,
                definition=definition,
                value=status,
                status=status,
                units=units,
                observable_link=observable_link,
                source_path="MISSING_SOURCE_PATH",
                score_ready=False,
                official_residual=True,
                no_cancellation_rule="absolute_sum_only_no_hidden_cancellation",
                next_action=next_action,
            )
        )
    return rows


def arena_projection_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "APQ2206_0_PPN",
            "PPN",
            "Delta_PPN_q = R_PPN[q_loc_residual_vector]",
            "beta,gamma,alpha_i,zeta_i,xi response map plus source normalization",
            "MISSING_PPN_RESPONSE_OPERATOR;MISSING_QLOC_COMPONENT_PROFILE;MISSING_METRIC_RESPONSE_MATRIX",
        ),
        (
            "APQ2206_1_R10",
            "R10_short_range",
            "alpha_R10_q(lambda)=R_R10[q_loc(lambda)]",
            "range kernel, alpha(lambda) conversion, real bound curve, q_loc units",
            "MISSING_R10_PROJECTION_OPERATOR;MISSING_RANGE_KERNEL;MISSING_BOUND_CURVE_LINK",
        ),
        (
            "APQ2206_2_R11",
            "R11_source_normalization",
            "c_GK_operator_vector(lambda)=R_R11[q_loc]",
            "source measure map, PiM link, H/M normalization",
            "MISSING_R11_OPERATOR_MAP;MISSING_SOURCE_MEASURE_NORMALIZATION;MISSING_PIM_LINK",
        ),
        (
            "APQ2206_3_clocks",
            "clock_time",
            "Delta_clock_q=R_clock[q_loc]",
            "clock frame, redshift/frequency response coefficients, matter-frame owner",
            "MISSING_CLOCK_RESPONSE_COEFFICIENTS;MISSING_CLOCK_FRAME;MISSING_MATTER_FRAME_OWNER",
        ),
        (
            "APQ2206_4_orbital",
            "orbital_systems",
            "Delta_orbital_q=R_orbital[q_loc]",
            "force-to-acceleration map, source charge equality, radial profile",
            "MISSING_ORBITAL_FORCE_MAP;MISSING_SOURCE_CHARGE_EQUALITY;MISSING_RADIAL_PROFILE",
        ),
        (
            "APQ2206_5_local_GR",
            "local_GR_Newton_limit",
            "q_loc theorem-zero or residual bound below every local threshold",
            "all parent signatures or all finite residual components with conservative thresholds",
            "THEOREM_ZERO_FALSE;MISSING_COMPONENT_BOUNDS;LOCAL_GR_CLAIM_BLOCKED",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for queue_id, arena, projected_quantity, required_operator, status in specs:
        rows.append(
            base_row(
                queue_id=queue_id,
                arena=arena,
                projected_quantity=projected_quantity,
                required_operator=required_operator,
                status=status,
                score_ready=False,
                theorem_zero_override=False,
                notes="official residual demotion row; no arena score until operator/profile/source rows are real",
            )
        )
    return rows


def claim_gate_rows(signature_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_signed = all(truthy(row.get("passes_now")) for row in signature_rows if str(row.get("clause_id", "")).startswith("PSA2206_") and row.get("clause_id") != "PSA2206_8_all_or_nothing")
    return [
        base_row(
            gate_id="CG2206_0_ward_identity",
            gate="q_loc is the projected negative Ward divergence of T_GK=Khat-Gamma*g",
            status="PASS_CONDITIONAL_IDENTITY",
            implication="the coupling problem is sharply reduced to parent action ownership, not mystical force language",
        ),
        base_row(
            gate_id="CG2206_1_parent_signature",
            gate="all parent signature clauses pass",
            status="PASS" if all_signed else "BLOCKED_NONCLAIM",
            implication="q_loc theorem-zero is blocked because action/metric/Helmholtz/Euler/double-zero/P_loc/boundary clauses are not signed together",
        ),
        base_row(
            gate_id="CG2206_2_theorem_zero",
            gate="q_loc=0 can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="theorem_zero_q_loc=false; no local-GR/Newton/PPN/R10 claim follows",
        ),
        base_row(
            gate_id="CG2206_3_residual_demotion",
            gate="q_loc becomes official finite residual vector",
            status="PASS_NONCLAIM",
            implication="future testing must use explicit components, source paths, units, and response operators",
        ),
        base_row(
            gate_id="CG2206_4_no_shortcuts",
            gate="plateau/scalar-proxy/measured-G/readout-cancellation shortcuts",
            status="BLOCKED_GUARDRAIL",
            implication="none of those routes may zero q_loc or pass local GR",
        ),
        base_row(
            gate_id="CG2206_5_GitHub",
            gate="public/github update",
            status="BLOCKED_NONCLAIM",
            implication="private goal work only; no GitHub action",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2206_0_gain",
            decision="WARD_DIVERGENCE_REDUCTION_DERIVED",
            rationale="With T_GK=Khat-Gamma_eff*g, q_loc is exactly -P_loc div T_GK. That is the clean parent-action route to local silence.",
            next_action="use this identity as the official proof contract for all future GK/q_loc attempts",
        ),
        base_row(
            decision_id="DEC2206_1_limit",
            decision="CURRENT_MTS_DOES_NOT_PARENT_SIGN_TGK",
            rationale="Current source files provide candidate actions and audits, but not a matched S_GK, metric response, Helmholtz, Euler, double-zero, P_loc and boundary chain.",
            next_action="do not claim q_loc theorem-zero; keep parent signature false",
        ),
        base_row(
            decision_id="DEC2206_2_demotion",
            decision="QLOC_OFFICIALLY_DEMOTED_TO_FINITE_RESIDUAL_VECTOR",
            rationale="Because the theorem-zero chain remains unsigned, q_loc must be carried as explicit component rows for PPN/R10/R11/clock/orbital tests.",
            next_action="fill one response operator/component source row next, rather than re-proving the generic theorem",
        ),
        base_row(
            decision_id="DEC2206_3_best_next",
            decision="METRIC_RESPONSE_OR_PPN_OPERATOR_NEXT",
            rationale="The biggest root-cause missing item is Khat=d(sqrt(-g)Gamma_eff)/dg. If that cannot be sourced, the empirical path needs the first PPN/R10 response operator.",
            next_action="2207 should try one explicit Gamma_eff candidate metric variation; if it fails, write the first source-ready PPN/R10 operator row",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2206_0_2207",
            selection_status="selected",
            target_file="2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            target_script="scripts/Y5_R2FR_Gamma_eff_metric_variation_or_first_q_loc_response_operator_row_2207.py",
            objective="try one concrete Gamma_eff candidate and compute its metric response against K_hat; if no candidate is source-signed, fill the first nonclaim q_loc response-operator row for PPN or R10",
            success_condition="either a Khat metric-response clause is parent-signed for one branch, or one arena projection row has source path, units, operator schema, and valid_for_claim=false",
            do_not_do="do not claim q_loc=0, do not use plateau axiom, do not score placeholders, do not hide residuals in measured G, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2206_1_parallel_source",
            selection_status="held_parallel",
            target_file="2207b-Y5-R2FR-PiM-source-measure-lock-after-q-loc-demotion.md",
            target_script="scripts/Y5_R2FR_PiM_source_measure_lock_after_q_loc_demotion_2207b.py",
            objective="return to PiM/source-measure only after the first q_loc metric-response/operator row is attempted",
            success_condition="PiM/source-measure residuals are not absorbed into q_loc or measured G",
            do_not_do="do not switch targets to avoid the coupling problem; keep PiM parallel, not a substitute",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["residual_demotion"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["signature_audit"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["ward_identity"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        row_count = 0
        if source.exists():
            shutil.copy2(source, target)
            copied = target.exists()
            parse_ok, row_count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=row_count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(
            base_row(
                validation_id=validation_id,
                status="PASS" if status else "FAIL",
                detail=detail,
            )
        )

    sources_exist = all(truthy(row.get("path_exists")) for row in source_rows)
    needles_found = all(truthy(row.get("needles_found")) for row in source_rows)
    add("VAL2206_00_sources_exist", sources_exist, f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2206_01_needles_found", needles_found, f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    ward_identity_ok = any(row.get("derivation_id") == "WID2206_0_define_stress" and "q_loc" in str(row.get("implication")) for row in ward_rows)
    demotion_verdict_ok = any(row.get("derivation_id") == "WID2206_4_current_verdict" and "official_residual_demotion=true" in str(row.get("algebraic_result")) for row in ward_rows)
    add("VAL2206_02_ward_identity", ward_identity_ok and demotion_verdict_ok, "q_loc=-P_loc div T_GK identity is written and current verdict demotes residual")

    core_signature_rows = [row for row in signature_rows if row.get("clause_id") != "PSA2206_8_all_or_nothing"]
    all_signature_false = all(not truthy(row.get("passes_now")) and not truthy(row.get("parent_signed")) for row in core_signature_rows)
    all_or_nothing_false = any(row.get("clause_id") == "PSA2206_8_all_or_nothing" and not truthy(row.get("passes_now")) for row in signature_rows)
    add("VAL2206_03_signature_audit", all_signature_false and all_or_nothing_false, f"signature clauses false={sum(not truthy(row.get('passes_now')) for row in core_signature_rows)}/{len(core_signature_rows)}")

    residual_ok = len(residual_rows) >= 10 and any(row.get("symbol") == "q_loc_residual_vector_abs" for row in residual_rows)
    residual_nonclaim = all(truthy(row.get("official_residual")) and not truthy(row.get("score_ready")) for row in residual_rows)
    add("VAL2206_04_residual_demotion", residual_ok and residual_nonclaim, f"residual rows={len(residual_rows)}; official nonclaim={residual_nonclaim}")

    required_arenas = {"PPN", "R10_short_range", "R11_source_normalization", "clock_time", "orbital_systems", "local_GR_Newton_limit"}
    arena_set = {str(row.get("arena")) for row in arena_rows}
    arena_ok = required_arenas.issubset(arena_set) and all(not truthy(row.get("score_ready")) for row in arena_rows)
    add("VAL2206_05_arena_projection_queue", arena_ok, f"arenas covered={len(required_arenas.intersection(arena_set))}/{len(required_arenas)}")

    claim_gate_ok = any(row.get("gate_id") == "CG2206_2_theorem_zero" and str(row.get("status")) == "BLOCKED_NONCLAIM" for row in claim_rows)
    shortcut_gate_ok = any(row.get("gate_id") == "CG2206_4_no_shortcuts" and str(row.get("status")) == "BLOCKED_GUARDRAIL" for row in claim_rows)
    add("VAL2206_06_claim_gate", claim_gate_ok and shortcut_gate_ok, "theorem-zero and shortcut gates remain blocked")

    decision_ok = any(row.get("decision") == "WARD_DIVERGENCE_REDUCTION_DERIVED" for row in decision_rows_) and any(row.get("decision") == "QLOC_OFFICIALLY_DEMOTED_TO_FINITE_RESIDUAL_VECTOR" for row in decision_rows_)
    add("VAL2206_07_decision", decision_ok, "decision ledger records Ward reduction and official demotion")

    next_ok = any(
        row.get("route_id") == "NEXT2206_0_2207"
        and ("metric variation" in str(row.get("objective")) or "metric response" in str(row.get("objective")))
        for row in next_rows
    )
    add("VAL2206_08_next_target", next_ok, "2207 metric-response or first response-operator row selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2206_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in branch_rows)
    add("VAL2206_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in branch_rows))

    generated_groups = [source_rows, ward_rows, signature_rows, residual_rows, arena_rows, claim_rows, decision_rows_, next_rows, branch_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2206_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    formalization_clean = not formalization_has_2206_artifacts()
    add("VAL2206_12_formalization_clean", formalization_clean, "formalization-workbench has no 2206 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2206_13_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2206_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2206 derives the Ward-divergence contract for q_loc, refuses current theorem-zero promotion, and officially demotes q_loc to finite residual testing",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2206 - Y5/R2FR GammaKhat q_loc Parent Action Signature Or Official Residual Demotion",
        "",
        "## Current Verdict",
        "",
        "2206 makes the coupling problem sharper rather than softer. The useful algebraic leap is:",
        "",
        "`T_GK^{mu nu}:=K_hat^{mu nu}-Gamma_eff g^{mu nu}` implies `q_loc^nu=-P_loc nabla_mu T_GK^{mu nu}`.",
        "",
        "So the clean route to local silence is not a plateau axiom. It is a parent-action Ward/Euler theorem: if `T_GK` is the Hilbert stress of a diffeomorphism-invariant `S_GK`, and the compact local branch signs Euler closure, double-zero, `P_loc` ownership and boundary no-flux, then `q_loc` can vanish on shell.",
        "",
        "Current MTS evidence does **not** sign that full chain. Therefore `q_loc` is now officially demoted to a finite residual vector for PPN/R10/R11/clock/orbital testing. This is not a defeat; it is the exact honesty gate before real tests.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Ward Identity Derivation",
        "",
        md_table(ward_rows, ["derivation_id", "statement", "algebraic_result", "implication", "proof_status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Parent Signature Audit",
        "",
        md_table(signature_rows, ["clause_id", "clause", "required_statement", "current_status", "parent_signed", "passes_now", "evidence", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Official Residual Demotion",
        "",
        md_table(residual_rows, ["row_id", "symbol", "definition", "status", "units", "observable_link", "source_path", "score_ready", "official_residual", "next_action", "valid_for_claim"]),
        "",
        "## Arena Projection Queue",
        "",
        md_table(arena_rows, ["queue_id", "arena", "projected_quantity", "required_operator", "status", "score_ready", "theorem_zero_override", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(branch_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is a forward move. The coupling is not an undefined monster anymore: it is the Ward divergence of one specific tensor **if** `K_hat-Gamma_eff g` is owned by a parent action.",
        "",
        "The grim bit: current sources do not prove that ownership. The good bit: the next target is now surgical. Either compute one concrete `Gamma_eff` metric variation and match `K_hat`, or stop pretending and fill the first real q_loc response-operator row for PPN/R10 testing.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    ward_rows = ward_identity_rows()
    signature_rows = signature_audit_rows()
    residual_rows = residual_demotion_rows()
    arena_rows = arena_projection_rows()
    claim_rows = claim_gate_rows(signature_rows)
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["ward_identity"], ward_rows),
        (OUTPUTS["signature_audit"], signature_rows),
        (OUTPUTS["residual_demotion"], residual_rows),
        (OUTPUTS["arena_projection"], arena_rows),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        ward_rows,
        signature_rows,
        residual_rows,
        arena_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        ward_rows,
        signature_rows,
        residual_rows,
        arena_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
