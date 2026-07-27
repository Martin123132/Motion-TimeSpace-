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
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1712"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1712-Y5-R2FR-response-displacement-conjugacy-action-or-first-q_loc-profile-row.md"

SOURCE_FILES = {
    "1711_doc": ROOT / "1711-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-input-pack-smoke-runner.md",
    "1711_validation": OUT / "P8_Y5_BRR545_1711_VALIDATION.csv",
    "1711_next": OUT / "P8_Y5_PARENT_QLOC_1711_NEXT_TARGET.csv",
    "1711_doublet": OUT / "P8_Y5_PARENT_QLOC_1711_RESPONSE_DOUBLET_STATUS.csv",
    "1711_fallback": OUT / "P8_Y5_PARENT_QLOC_1711_QLOC_FALLBACK_LINK.csv",
    "1352_doc": ROOT / "1352-Y5-R10-RAB-response-displacement-conjugacy-action-or-q_loc-profile-source-fill.md",
    "1352_action": OUT / "P8_Y5_R10_1352_RESPONSE_DISPLACEMENT_ACTION_TEMPLATE.csv",
    "1352_identity": OUT / "P8_Y5_R10_1352_METRIC_RESPONSE_IDENTITY_AUDIT.csv",
    "1352_blocker": OUT / "P8_Y5_R10_1352_CONJUGACY_BLOCKER_AUDIT.csv",
    "1352_qprofile": OUT / "P8_Y5_R10_1352_QLOC_PROFILE_SOURCE_ROW.csv",
    "1353_doc": ROOT / "1353-Y5-R10-RAB-Z-component-lock-and-no-linear-source-theorem-or-JZ-source-pack.md",
    "1353_zlock": OUT / "P8_Y5_R10_1353_Z_COMPONENT_LOCK_ATTEMPT.csv",
    "1353_no_linear": OUT / "P8_Y5_R10_1353_NO_LINEAR_SOURCE_THEOREM_ATTEMPT.csv",
    "1353_jz_pack": OUT / "P8_Y5_R10_1353_JZ_BZ_SOURCE_PACK.csv",
    "515_audit": OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "516_candidates": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
    "516_contract": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
    "517_variation": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
}

NEEDLES = {
    "1711_doc": ["NEXT1711_0_primary", "response/displacement conjugacy action"],
    "1711_validation": ["VAL1711_OVERALL", "PASS"],
    "1711_next": ["1712-Y5-R2FR-response-displacement-conjugacy-action-or-first-q_loc-profile-row.md", "selected"],
    "1711_doublet": ["RD1711_5_verdict", "PROMISING_TEMPLATE_NOT_CURRENT_DERIVATION"],
    "1711_fallback": ["QFL1711_0_R10", "template_only_not_scoreable"],
    "1352_doc": ["physical coupling map is still the missing beast", "PROMISING_TEMPLATE_NOT_LIVE_PROOF"],
    "1352_action": ["RDA1352_5_verdict", "PROMISING_TEMPLATE_NOT_LIVE_PROOF"],
    "1352_identity": ["MRI1352_3_Ward_residual", "WARD_ROUTE_OPEN_NOT_CLOSED"],
    "1352_blocker": ["BLK1352_0_component_lock", "CONJUGACY_ACTION_NOT_LIVE"],
    "1352_qprofile": ["QPROF1352_0_minimal_residual_source", "first_profile_source_row_template_not_scoreable"],
    "1353_doc": ["coupling obstruction precisely", "J_Z/B_Z"],
    "1353_zlock": ["ZLOCK1353_4_verdict", "COMPONENT_LOCK_NOT_PROVED"],
    "1353_no_linear": ["NLS1353_5_verdict", "THEOREM_NOT_PROVED"],
    "1353_jz_pack": ["JZ1353_2_Y5_source_normalization", "RETAINED_NONCLAIM_HARD_BLOCK"],
    "515_audit": ["MA515_1_Khat_metric_response", "fail_for_current_claim"],
    "516_candidates": ["GO516_A_response_doublet_quadratic_density", "best_candidate_not_current_MTS_derived"],
    "516_contract": ["RD516_4_zero_odd_source", "not_derived_hard_block"],
    "517_variation": ["AV517_3_double_zero", "conditional_pass_not_MTS_promotion"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1712_SOURCE_REGISTER.csv"
CONJUGACY_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1712_RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv"
METRIC_IDENTITY = OUT / "P8_Y5_PARENT_QLOC_1712_METRIC_RESPONSE_IDENTITY_AUDIT.csv"
BLOCKER_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1712_CONJUGACY_BLOCKER_AUDIT.csv"
FIRST_QLOC_PROFILE = OUT / "P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1712_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1712_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1712_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1712_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    CONJUGACY_ATTEMPT,
    METRIC_IDENTITY,
    BLOCKER_AUDIT,
    FIRST_QLOC_PROFILE,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    CONJUGACY_ATTEMPT,
    METRIC_IDENTITY,
    BLOCKER_AUDIT,
    FIRST_QLOC_PROFILE,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    CONJUGACY_ATTEMPT: [
        QUARANTINE / "RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_response_displacement_conjugacy_attempt_1712.csv",
        QUEUE / "JR1712_RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv",
    ],
    METRIC_IDENTITY: [
        QUARANTINE / "METRIC_RESPONSE_IDENTITY_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_metric_response_identity_audit_1712.csv",
        QUEUE / "JR1712_METRIC_RESPONSE_IDENTITY_AUDIT.csv",
    ],
    BLOCKER_AUDIT: [
        QUARANTINE / "CONJUGACY_BLOCKER_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_conjugacy_blocker_audit_1712.csv",
        QUEUE / "JR1712_CONJUGACY_BLOCKER_AUDIT.csv",
    ],
    FIRST_QLOC_PROFILE: [
        QUARANTINE / "FIRST_QLOC_PROFILE_ROW.csv",
        BRANCH_RESIDUALS / "R2FR_first_q_loc_profile_row_1712.csv",
        QUEUE / "JR1712_FIRST_QLOC_PROFILE_ROW.csv",
    ],
    RUNNER_REFUSAL: [
        QUARANTINE / "RUNNER_REFUSAL.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_1712.csv",
        QUEUE / "JR1712_RUNNER_REFUSAL.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1712.csv",
        QUEUE / "JR1712_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1712.csv",
        QUEUE / "JR1712_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _field in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1712_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1712": "response/displacement conjugacy attempt and first q_loc profile row",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def conjugacy_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CJA1712_0_parent_doublet",
            "R_+^A,R_-^A with Z^A=(R_+^A-R_-^A)/2",
            "conditional template imported from 516/517/1352",
            "CONDITIONAL_DOUBLETS_ONLY",
            "physical Y0-Y6 component coverage is not parent-locked",
            "would give candidate residual coordinates",
        ),
        (
            "CJA1712_1_even_density",
            "Gamma_eff=Gamma0+1/2 Z^A M_AB Z^B+O(Z^4)",
            "formal double-zero exists at Z=0 if no odd source term is legal",
            "FORMAL_F1_ZERO_ONLY",
            "M_AB owner, units, positivity and no-linear-source theorem are not signed",
            "could remove the local plateau axiom if source side closes",
        ),
        (
            "CJA1712_2_metric_response",
            "K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu}",
            "metric response identity exists under the template",
            "K_HAT_MATCH_NOT_FOUND",
            "live K_hat has not been shown equal to this metric response term-by-term",
            "would make q_loc a Ward residual rather than closure",
        ),
        (
            "CJA1712_3_Ward_residual",
            "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})",
            "becomes projected Euler/Ward residual only if SGK/Khat/Ploc/source/boundary close",
            "WARD_ROUTE_CONDITIONAL",
            "source, boundary, projector and readout terms still re-enter",
            "would connect local-GR reduction to diffeomorphism identity",
        ),
        (
            "CJA1712_4_component_lock",
            "Z^A equals physical q_loc/PPN/source-normalization residual vector",
            "1353 proves this is not currently derived",
            "COMPONENT_LOCK_NOT_PROVED",
            "Y5 source-normalization and Y6 extra-stress may live outside the doublet",
            "must close before formal F1=0 becomes physical",
        ),
        (
            "CJA1712_5_no_linear_source",
            "J_Z=B_Z=0 for matter, source-normalization, boundary and readout",
            "1353 records no-linear-source theorem failure",
            "SOURCE_ZERO_NOT_PROVED",
            "source pullback, Y5, Y6 and boundary exactness remain unsigned",
            "must close before local residual can be zero by theorem",
        ),
        (
            "CJA1712_6_verdict",
            "response/displacement conjugacy action",
            "best derivation route retained but not a live parent proof",
            "CONJUGACY_ACTION_NOT_PARENT_SIGNED",
            "component lock, no-linear-source, metric response, positivity, P_loc and boundary all remain open",
            "route stays alive; claim gates stay shut",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "object": obj,
            "derived_or_imported_evidence": evidence,
            "current_status": status,
            "blocking_gap": gap,
            "payoff_if_closed": payoff,
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, obj, evidence, status, gap, payoff in rows
    ]


def metric_identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MRI1712_0_Z_variation",
            "delta Gamma_eff/delta Z^A=M_AB Z^B+O(Z^3)",
            "conditional_pass",
            "formal F1 vanishes at Z=0",
            "Z=0 is not yet a proved physical local residual state",
        ),
        (
            "MRI1712_1_metric_variation",
            "delta_g S_GK produces K_metric^{mu nu} and T_GK^{mu nu}",
            "formal_identity_only",
            "Gamma_eff and K can become one variational object",
            "live K_hat tensor pieces, sign convention and boundary terms are not matched",
        ),
        (
            "MRI1712_2_projected_Ward",
            "nabla_mu T_GK^{mu nu}=E_A nabla^nu Z^A+E_even nabla^nu R_even^A+boundary/source terms",
            "conditional_identity_only",
            "on shell, source-free and no-flux gives q_loc silence",
            "J_Z/B_Z/Y5/Y6/readout terms remain active",
        ),
        (
            "MRI1712_3_cR2_link",
            "c_R2_eff may be sourced by the same response operator if the Hessian/metric-response owner is real",
            "not_derived",
            "could give an R2/fR coefficient instead of a placeholder",
            "no parent coefficient or source-normalized scalar channel exists",
        ),
        (
            "MRI1712_4_verdict",
            "Gamma_eff/K_hat conjugacy",
            "not_symbol_matched",
            "route is mathematically coherent but not physically locked",
            "no local-GR, c_R2, R10 or PPN promotion",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "identity_id": identity_id,
            "identity": identity,
            "current_status": status,
            "physical_payoff": payoff,
            "current_gap": gap,
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for identity_id, identity, status, payoff, gap in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BLK1712_0_component_lock",
            "Z^A covers all physical leakage components Y0-Y6 and maps to q_loc/PPN/source-normalization",
            "ZLOCK1353_4_verdict COMPONENT_LOCK_NOT_PROVED",
            "OPEN_HARD_BLOCK",
            "construct source-backed Z^A -> {R10, PPN, clock, orbital, R11/source-normalization} map",
        ),
        (
            "BLK1712_1_no_linear_source",
            "J_Z=B_Z=0 for matter/source/boundary/readout channels",
            "NLS1353_5_verdict THEOREM_NOT_PROVED",
            "OPEN_HARD_BLOCK",
            "prove source-functional evenness or fill J_Z/B_Z coefficient rows",
        ),
        (
            "BLK1712_2_Y5_Y6",
            "Y5 source-normalization and Y6 extra-stress are even/topological/bounded",
            "JZ1353_2 and JZ1353_3 retained nonclaim hard blocks",
            "OPEN_HARD_BLOCK",
            "attack Y5/Y6 source coupling directly; no hidden closure",
        ),
        (
            "BLK1712_3_metric_symbol_match",
            "live K_hat equals K_metric[Gamma_eff] term-by-term",
            "MA515_1 fail_for_current_claim",
            "OPEN",
            "compute metric response from a chosen Gamma_eff and compare tensor components",
        ),
        (
            "BLK1712_4_operator_domain",
            "M_AB/L_AB positive, self-adjoint, gauge-reduced and unit-normalized",
            "RD516_3 formal_candidate_only",
            "OPEN",
            "declare inner product, gauge quotient, boundary domain and dimensions",
        ),
        (
            "BLK1712_5_projector_boundary",
            "P_loc owner and boundary no-flux before readout",
            "1711 owner bundle keeps P_loc/boundary open",
            "OPEN",
            "derive projection order and linking-sphere flux silence",
        ),
        (
            "BLK1712_6_verdict",
            "all response/displacement conjugacy blockers close together",
            "multiple open blockers",
            "CONJUGACY_NOT_LIVE_PROOF",
            "move to source-functional coupling lock or explicit finite q_loc profile acquisition",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "required_close": required,
            "evidence": evidence,
            "status": status,
            "next_attack": next_attack,
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, required, evidence, status, next_attack in rows
    ]


def first_qloc_profile_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QPROF1712_0_parent_residual_vector",
            "all local arenas",
            "q_loc^nu finite residual vector",
            "q_loc^nu=P_loc[sum_A E_A nabla^nu Phi^A+J_Z^nu+B_Z^nu+nabla_mu Delta_K^{mu nu}+C_readout^nu]",
            "E_A;Phi^A;J_Z;B_Z;Delta_K;C_readout;P_loc;domain/coframe;normalization",
            "stress-divergence or force-density units, with explicit conversion to arena observables",
            "parent action/source-profile file for every nonzero term",
            "MISSING_COMPONENT_LOCK;MISSING_JZ_BZ;MISSING_DELTA_K;MISSING_PLOC_OWNER;MISSING_UNITS",
        ),
        (
            "QPROF1712_1_R10_projection",
            "R10 short-range gravity",
            "q_loc/B_mem -> alpha(lambda)",
            "alpha_pred(lambda)=K_X(lambda) Qbar_XH(lambda) qbar_XT(lambda) with parent-sourced coefficients only",
            "K_X;Qbar_XH;qbar_XT;lambda_X;geometry;source normalization;real bound curve",
            "dimensionless alpha and SI length lambda",
            "MTS coefficient source plus source-backed R10 alpha(lambda) bound curve",
            "MISSING_PARENT_COEFFICIENTS;MISSING_NUMERIC_PROFILE",
        ),
        (
            "QPROF1712_2_PPN_projection",
            "PPN weak-field",
            "q_loc^nu -> gamma,beta,alpha_i,xi,Gdot residual vector",
            "Delta g_munu[q_loc] solved in weak-field gauge then projected into PPN parameters",
            "weak-field metric solution; gauge lock; source stress; q_loc coefficients",
            "dimensionless PPN parameters and time-variation units for Gdot/G",
            "parent q_loc profile plus PPN projection theorem/bound source",
            "MISSING_WEAK_FIELD_MAP;MISSING_GAUGE_LOCK",
        ),
        (
            "QPROF1712_3_clock_orbital_source",
            "clock/orbital/source-normalization",
            "q_loc readout tail and source charge response",
            "clock shift, acceleration/precession and measured-GM drift from the same q_loc profile",
            "clock response; orbital acceleration map; source charge equality; material/species map",
            "fractional frequency, acceleration/precession, and GM drift units",
            "source-backed clock/orbital/readout response files",
            "MISSING_CLOCK_RESPONSE;MISSING_ORBITAL_PROJECTION;MISSING_SOURCE_NORMALIZATION_OPERATOR",
        ),
        (
            "QPROF1712_4_theorem_zero_certificate",
            "all local arenas",
            "q_loc^nu=0 theorem certificate",
            "allowed only if SGK/Khat metric match, P_loc owner, E_A=0, J_Z=0, B_Z=0, Delta_K=0 and C_readout=0",
            "all theorem premises with source paths",
            "certificate replaces numeric profile only after all premises pass",
            "single parent-signed theorem bundle",
            "MISSING_PARENT_SIGNED_THEOREM_BUNDLE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "profile_id": profile_id,
            "arena": arena,
            "profile_object": profile_object,
            "expression": expression,
            "required_inputs": required_inputs,
            "units_required": units,
            "source_path_required": source_path,
            "current_missing": current_missing,
            "row_status": "template_only_not_scoreable",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for profile_id, arena, profile_object, expression, required_inputs, units, source_path, current_missing in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1712_0_conjugacy_proof", "promote response/displacement action to parent proof", "REJECT_NOT_PARENT_SIGNED", "component lock, no-linear-source, metric response, P_loc and boundary all open"),
        ("RUN1712_1_q_loc_zero", "set q_loc^nu=0 from formal F1=0", "REJECT_SHADOW_ZERO", "formal Z double-zero is not physical q_loc zero without component/source lock"),
        ("RUN1712_2_cR2_prediction", "score c_R2/fRR or scalaron branch", "REJECT_NO_PARENT_COEFFICIENT", "response Hessian is not source-normalized into c_R2"),
        ("RUN1712_3_R10_alpha", "score alpha(lambda) from q_loc row", "NOT_RUN_TEMPLATE_ONLY", "R10 projection lacks parent coefficients and numeric q_loc profile"),
        ("RUN1712_4_PPN", "score PPN residual vector", "NOT_RUN_TEMPLATE_ONLY", "weak-field metric map and gauge lock missing"),
        ("RUN1712_5_local_GR_Newton", "claim derived local GR/Newton", "BLOCKED_NO_CLAIM", "operator/source/GM/PPN/R11 gates not closed together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT1712_0_primary",
            "1713-Y5-R2FR-source-functional-evenness-and-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            "scripts/Y5_R2FR_source_functional_evenness_and_JZ_BZ_coupling_lock_or_profile_acquisition.py",
            "try to prove source/matter/boundary/readout functionals are exchange-even in Z, especially Y5/Y6; if not, acquire explicit nonclaim J_Z/B_Z/q_loc profile coefficients",
            "selected",
        ),
        (
            "NEXT1712_1_parallel_cR2",
            "1713b-Y5-R2FR-cR2-coefficient-input-pack-from-response-Hessian.md",
            "scripts/Y5_R2FR_cR2_coefficient_input_pack_from_response_Hessian.py",
            "held route for c_R2 only after response Hessian/source normalization exists",
            "held_until_coupling_lock",
        ),
        (
            "NEXT1712_2_parallel_connection",
            "1713c-Y5-R2FR-Levi-Civita-torsion-nonmetricity-comparison-gate.md",
            "scripts/Y5_R2FR_Levi_Civita_torsion_nonmetricity_comparison_gate.py",
            "parallel connection gate remains useful but should not outrun q_loc coupling lock",
            "held_parallel",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "success_condition": "source-functional evenness theorem or explicit source-backed finite q_loc/J_Z/B_Z acquisition rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1712_0_conjugacy", "response/displacement action is parent-owned", "BLOCKED_NO_CLAIM", "template is coherent but component/source/metric/projector/boundary clauses are open"),
        ("CG1712_1_F1_physical_zero", "F1=0 is a physical local residual theorem", "BLOCKED_NO_CLAIM", "formal Z double-zero lacks physical component lock"),
        ("CG1712_2_q_loc_zero", "q_loc^nu vanishes locally", "BLOCKED_NO_CLAIM", "J_Z/B_Z/Y5/Y6 and boundary/readout terms are not theorem-zero"),
        ("CG1712_3_cR2_zero_or_value", "c_R2/fRR is zero or has a parent coefficient", "BLOCKED_NO_CLAIM", "response Hessian has not been normalized into a scalar coefficient"),
        ("CG1712_4_R10_PPN_score", "R10/PPN/clock/orbital scores can be run", "BLOCKED_NO_CLAIM", "profile rows are template-only and not numeric/source-backed"),
        ("CG1712_5_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "local operator, source, GM, PPN and R11 gates remain jointly open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def parse_all(paths: list[Path]) -> bool:
    for path in paths:
        read_csv(path)
    return True


def claim_flags_false(paths: list[Path]) -> bool:
    checked_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "score_emitted",
        "parent_signed",
        "source_backed",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in checked_keys and truthy(value):
                    return False
    return True


def formalization_1712_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [
        path
        for path in FORMALIZATION.rglob("*1712*")
        if path.is_file() and ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    source_rows: list[dict[str, Any]],
    attempt_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    blocker_rows_: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    remove_pycache()
    checks = [
        ("VAL1712_0_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL1712_1_needles_present", all(row["needles_present"] for row in source_rows), "required source needles are present"),
        (
            "VAL1712_2_conjugacy_not_promoted",
            any(row["attempt_id"] == "CJA1712_6_verdict" and row["current_status"] == "CONJUGACY_ACTION_NOT_PARENT_SIGNED" for row in attempt_rows),
            "response/displacement route retained as nonclaim proof attempt",
        ),
        (
            "VAL1712_3_metric_response_not_matched",
            any(row["identity_id"] == "MRI1712_4_verdict" and row["current_status"] == "not_symbol_matched" for row in identity_rows),
            "Gamma_eff/K_hat identity remains formal, not symbol-matched",
        ),
        (
            "VAL1712_4_blockers_cover_coupling",
            all(
                any(row["blocker_id"] == blocker_id and "OPEN" in row["status"] for row in blocker_rows_)
                for blocker_id in ["BLK1712_0_component_lock", "BLK1712_1_no_linear_source", "BLK1712_2_Y5_Y6"]
            ),
            "component lock, no-linear-source, and Y5/Y6 remain explicit hard blockers",
        ),
        (
            "VAL1712_5_first_qloc_profile_nonclaim",
            any(row["profile_id"] == "QPROF1712_0_parent_residual_vector" for row in profile_rows)
            and all(row["row_status"] == "template_only_not_scoreable" for row in profile_rows),
            "first q_loc profile/acquisition rows are staged but not scoreable",
        ),
        (
            "VAL1712_6_runner_refuses_shortcuts",
            all("REJECT" in row["status"] or "NOT_RUN" in row["status"] or "BLOCKED" in row["status"] for row in runner_rows_),
            "runner refuses q_loc-zero/cR2/R10/PPN/local-GR shortcuts",
        ),
        (
            "VAL1712_7_next_selected",
            any(row["route_id"] == "NEXT1712_0_primary" and row["selection_status"] == "selected" for row in next_rows_),
            "next target selects source-functional evenness / JZ-BZ coupling lock",
        ),
        (
            "VAL1712_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows_),
            "all claim gates remain blocked",
        ),
        ("VAL1712_9_csv_parse", parse_all(GENERATED_CSVS), "all generated 1712 CSVs parse"),
        (
            "VAL1712_10_no_claim_flags",
            claim_flags_false(CLAIM_CHECKED_CSVS),
            "all generated scoring and claim flags remain false",
        ),
        (
            "VAL1712_11_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets),
            "branch/quarantine/queue copies exist",
        ),
        (
            "VAL1712_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1712_13_formalization_untouched",
            not formalization_1712_hits(),
            "no 1712 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1712_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1712 response/displacement conjugacy attempt and first q_loc profile validation",
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    attempt_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    blocker_rows_: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    content = "\n\n".join(
        [
            "# 1712 - Response/Displacement Conjugacy Action Or First q_loc Profile Row",
            "## Verdict\n"
            "- The response/displacement action is still the best clean derivation route, but 1712 cannot promote it to a parent proof.\n"
            "- The algebraic double-zero is real only as a conditional template: `F_1=0` follows for an even `Gamma_eff`, but not yet for physical `q_loc`.\n"
            "- The blocker is the coupling map: `Z^A` must be the physical local residual vector and `J_Z/B_Z`, especially Y5/Y6, must vanish or be bounded.\n"
            "- Because that proof is unsigned, 1712 stages the first strict finite-residual `q_loc` profile row instead of smuggling in a plateau.\n"
            "- No q_loc-zero, c_R2, R10, PPN, clock, orbital, Newton, EH or local-GR claim is made.",
            "## Source Register\n" + table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
            "## Response/Displacement Conjugacy Attempt\n"
            + table(attempt_rows, ["attempt_id", "object", "derived_or_imported_evidence", "current_status", "blocking_gap", "payoff_if_closed"]),
            "## Metric/Ward Identity Audit\n"
            + table(identity_rows, ["identity_id", "identity", "current_status", "physical_payoff", "current_gap"]),
            "## Conjugacy Blocker Audit\n"
            + table(blocker_rows_, ["blocker_id", "required_close", "evidence", "status", "next_attack"]),
            "## First q_loc Profile Rows\n"
            + table(profile_rows, ["profile_id", "arena", "profile_object", "expression", "current_missing", "row_status"]),
            "## Runner Refusal\n" + table(runner_rows_, ["runner_id", "case", "status", "reason"]),
            "## Next Target\n" + table(next_rows_, ["route_id", "next_target", "script", "objective", "selection_status"]),
            "## Claim Gates\n" + table(claim_rows_, ["claim_id", "claim", "status", "reason"]),
            "## Validation\n" + table(validation_rows_, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "1712 says the route is not dead, but the missing object has a name now: the coupling functional. If the source/matter/readout side is exchange-even in the response doublet, the double-zero could become a real local-GR mechanism. If it is not, the honest branch is finite `q_loc` with explicit `J_Z/B_Z` coefficients and empirical bounds.",
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    attempt_rows = conjugacy_attempt_rows()
    identity_rows = metric_identity_rows()
    blocker_rows_ = blocker_rows()
    profile_rows = first_qloc_profile_rows()
    runner_rows_ = runner_rows()
    next_rows_ = next_rows()
    claim_rows_ = claim_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(CONJUGACY_ATTEMPT, attempt_rows)
    write_csv(METRIC_IDENTITY, identity_rows)
    write_csv(BLOCKER_AUDIT, blocker_rows_)
    write_csv(FIRST_QLOC_PROFILE, profile_rows)
    write_csv(RUNNER_REFUSAL, runner_rows_)
    write_csv(NEXT_TARGET, next_rows_)
    write_csv(CLAIM_GATE, claim_rows_)
    copy_outputs()

    validation_rows_ = validation_rows(
        source_rows,
        attempt_rows,
        identity_rows,
        blocker_rows_,
        profile_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
    )
    write_csv(VALIDATION, validation_rows_)
    write_doc(
        source_rows,
        attempt_rows,
        identity_rows,
        blocker_rows_,
        profile_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
        validation_rows_,
    )

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"1712 validation {validation_rows_[-1]['result']}")


if __name__ == "__main__":
    main()
