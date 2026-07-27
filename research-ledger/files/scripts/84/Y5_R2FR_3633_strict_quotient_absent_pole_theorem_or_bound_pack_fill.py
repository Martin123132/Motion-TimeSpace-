from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3633"
BRANCH_ID = "MTS_R2FR_Y5_STRICT_QUOTIENT_ABSENT_POLE_OR_BOUND_PACK_FILL_3633"
DOC = ROOT / "3633-Y5-R2FR-strict-quotient-absent-pole-theorem-or-bound-pack-fill.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def out_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3633_SOURCE_REGISTER.csv",
        "strict_theorem": RESIDUALS / "P8_Y5_R2FR_3633_STRICT_QUOTIENT_THEOREM.csv",
        "candidate_q_map": RESIDUALS / "P8_Y5_R2FR_3633_CANDIDATE_Q_MAP.csv",
        "absent_pole_audit": RESIDUALS / "P8_Y5_R2FR_3633_ABSENT_POLE_AUDIT.csv",
        "r0_r11_coverage": RESIDUALS / "P8_Y5_R2FR_3633_R0_R11_COVERAGE_GATE.csv",
        "bound_fill_targets": RESIDUALS / "P8_Y5_R2FR_3633_BOUND_PACK_FILL_TARGETS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3633_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3633_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3633_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_strict_quotient_absent_pole_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3633_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    sources = [
        (
            "handoff_3632",
            RESIDUALS / "P8_Y5_R2FR_3632_NEXT_TARGET.csv",
            "strict quotient/no-independent-pole",
            "3632 handoff: attempt strict quotient theorem before numerical residual scoring.",
        ),
        (
            "owner_routes_3632",
            RESIDUALS / "P8_Y5_R2FR_3632_SAME_PARENT_OWNER_ROUTES.csv",
            "strict quotient action / no independent X or Z pole",
            "ranked route saying absent quotient variable is the least-scrutiny local-GR path.",
        ),
        (
            "bound_pack_3632",
            RESIDUALS / "P8_Y5_R2FR_3632_DQJZ_BOUND_PACK.csv",
            "Dq_Z_norm",
            "nonclaim Dq/J_Z/X-sector rows to use if theorem-zero route fails.",
        ),
        (
            "lx_candidates_669",
            RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
            "absent_quotient_variable",
            "minimal L_X route hierarchy; absent quotient variable is rank 1 but not derived.",
        ),
        (
            "q_audit_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
            "PARTIAL_PRIOR_CONTRACT",
            "audit saying q is useful but still not computable or parent-owned.",
        ),
        (
            "field_chart_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
            "Q_vis",
            "candidate field chart with visible quotient and residual blocks separated.",
        ),
        (
            "dq_tests_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
            "MISSING_UNIFIED_Z_BASIS",
            "Dq tests showing Z/phi verticality is not currently runnable.",
        ),
        (
            "momentum_owner_583",
            RESIDUALS / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv",
            "zero_momentum_map",
            "older momentum-map owner attempt that names strict quotient as best if projection is derived.",
        ),
        (
            "parent_blocks_580",
            RESIDUALS / "P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv",
            "absent_quotient_variable",
            "parent-block candidate list showing no independent X variation is the strongest route.",
        ),
        (
            "sector_owner_668",
            RESIDUALS / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
            "MTS_extra_fields_X",
            "sector audit: X-sector Lagrangian owner remains missing if no-pole route fails.",
        ),
        (
            "r0_r11_template",
            RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
            "R11_EH_operator_ledger",
            "local residual channels that must be covered before local GR is claimed.",
        ),
        (
            "retained_dq_leaks_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
            "Dq_Z_norm",
            "first concrete Dq leak target if q-kernel proof does not close.",
        ),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
        }
        for source_id, path, needle, role in sources
    ]


def strict_theorem_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "theorem_id": "THM3633_0_parent_quotient_setup",
            "claim": "Let C be the parent configuration space, q:C->Q the ordinary-matter quotient, and V=ker(Dq) the fibre directions.",
            "identity": "v in V implies Dq[v]=0 by definition",
            "proof_step": "The only allowed physical variables before variation are q(Phi); X/Z may label a representative only if they are fibre coordinates, not independent coordinates of Q.",
            "live_status": "CONDITIONAL_DEFINITION_NOT_PARENT_SIGNED",
            "blocks_if_missing": "without explicit q and V, X/Z absence is a slogan rather than a theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM3633_1_action_pullback",
            "claim": "If S_parent[Phi]=S_red[q(Phi)] + S_top[q(Phi)] and S_top has no local fibre variation, then every fibre variation is an off-shell null variation of the bulk action.",
            "identity": "delta_v S_parent = delta S_red[Dq[v]] + delta S_top[Dq[v]] = 0",
            "proof_step": "This is the clean version of 'X is absent': the variation with respect to X is not set to zero after the fact; it never exists as a physical Euler-Lagrange equation.",
            "live_status": "CONDITIONAL_PROOF",
            "blocks_if_missing": "current corpus still keeps residual blocks as formal candidates, so pullback form is not established",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM3633_2_matter_source_descent",
            "claim": "If S_matter and source normalization depend on Phi only through q(Phi), then the X/Z fibre has no matter current.",
            "identity": "J_X = (1/sqrt(-g)) delta(S_matter+S_source)/delta X | fibre = 0",
            "proof_step": "This closes the source-coupling hole from 3629 only if matter/source descent is parent-owned, not closure-labelled.",
            "live_status": "CONDITIONAL_PROOF_NOT_LIVE",
            "blocks_if_missing": "matter pullback, source/readout mass, clock map, and material marker dependence are not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM3633_3_presymplectic_null",
            "claim": "If the presymplectic potential is also a quotient pullback up to an exact/proper boundary term, fibre directions are null gauge directions.",
            "identity": "i_v Omega = 0 modulo delta Q_v, with Q_v=0/exact/proper on the local collar",
            "proof_step": "This is the covariant phase-space version of the absent-pole theorem: no physical charge means no physical generator in the X/Z direction.",
            "live_status": "CONDITIONAL_PROOF_NOT_LIVE",
            "blocks_if_missing": "theta/Omega owner and boundary charge silence remain missing from 3632",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM3633_4_no_green_function_pole",
            "claim": "If X/Z is not a physical tangent direction, no L_X Hessian, inverse propagator, Green function residue, range lambda_X, or Yukawa alpha row exists.",
            "identity": "no_X_Green_function: {Z_X,M_X^2,K_X,qbar_XT,Qbar_XH,lambda_X} are absent-not-zero",
            "proof_step": "This is stronger and cleaner than fitting K_X=0. The pole is removed before local matter is coupled.",
            "live_status": "CONDITIONAL_PROOF_NOT_LIVE",
            "blocks_if_missing": "if any source, boundary, or readout depends on X/Z, the X-sector must be scored instead",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM3633_5_R10_R11_consequence",
            "claim": "The strict quotient route would silence the X-sector part of R10/R11 but does not by itself prove the whole local-GR branch.",
            "identity": "alpha_X(lambda_X) is undefined/absent; residual R3-R11 still require EH metric/operator and boundary coverage",
            "proof_step": "This keeps the theorem honest: no-pole closes one pressure channel, not all PPN, clock, WEP, or EH-selection channels.",
            "live_status": "THEOREM_SCOPE_LIMIT",
            "blocks_if_missing": "R0-R11 coverage map is still required before any local-GR statement",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def candidate_q_map_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "map_id": "QMAP3633_0_visible_geometry",
            "candidate_component": "G_obs=(e_obs,g_obs,nabla_obs)",
            "allowed_dependency": "depends only on q(Phi), not on representative fibre coordinates X/Z",
            "forbidden_dependency": "direct X/Z dependence in coframe, connection, or metric readout",
            "Dq_test": "Dq_Gobs[partial_X]=0 and Dq_Gobs[partial_Z]=0",
            "current_evidence": "1667 has partial alignment only; coframe/action ownership open",
            "status": "CANDIDATE_NOT_PARENT_SIGNED",
            "first_fill_action": "write explicit formulas for e_obs and g_obs as functions of the parent chart",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "QMAP3633_1_source_readout",
            "candidate_component": "M_obs=(mu_obs,source mass,orbit readout,Hamiltonian normalization)",
            "allowed_dependency": "source/readout data descends through q before local test coupling",
            "forbidden_dependency": "hidden X/Z dependence in GM calibration, source mass, or R10/R11 readout",
            "Dq_test": "Dq_Mobs[partial_X]=0 and Dq_Mobs[partial_Z]=0",
            "current_evidence": "retained Dsource_readout leak row says this is not proven",
            "status": "Dq_LEAK_RETAINED",
            "first_fill_action": "evaluate Dsource_readout_Dq_leak after q formulas exist",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "QMAP3633_2_clock_and_markers",
            "candidate_component": "Theta_obs=(clock map, constants, material markers)",
            "allowed_dependency": "clock/constants/material labels are q-owned or fixed external standards",
            "forbidden_dependency": "X/Z dependent clock scale, material marker, or fine-structure-like label",
            "Dq_test": "Dq_theta_marker[partial_X/Z]=0",
            "current_evidence": "1667 retained Dtheta_marker leak row",
            "status": "Dq_LEAK_RETAINED",
            "first_fill_action": "separate clock map from source normalization and EM/marker channels",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "QMAP3633_3_boundary_class",
            "candidate_component": "B_obs=(boundary class, projector Pi_M, reference term)",
            "allowed_dependency": "boundary and projector are q-owned or exact/proper under fibre variation",
            "forbidden_dependency": "X/Z surface charge, memory flux, preferred-frame edge hair",
            "Dq_test": "Q_boundary[partial_X/Z]=0/exact/proper",
            "current_evidence": "3632 boundary charge owner missing; 667 boundary flux open",
            "status": "BOUNDARY_SILENCE_NOT_DERIVED",
            "first_fill_action": "compute or bound boundary_projector_Dq_leak and boundary_flux_X",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "QMAP3633_4_excluded_residual_fibre",
            "candidate_component": "Fibre=(X,Z,phi,R_phys representative labels)",
            "allowed_dependency": "may appear only as redundant chart labels or constrained gauge fibre before variation",
            "forbidden_dependency": "physical L_X, source current J_X, finite Green-function pole, or residual readout in q",
            "Dq_test": "Dq[partial_fibre]=0 for all q components and no boundary charge survives",
            "current_evidence": "field chart still lists residual blocks; Dq_Z not runnable",
            "status": "ABSENCE_NOT_PROVEN",
            "first_fill_action": "start with Dq_Z_norm because it is the first exact obstruction to verticality",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def absent_pole_audit_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "audit_id": "APG3633_0_q_explicit",
            "clause": "q:C->Q explicit enough to compute Dq",
            "current_evidence": "1667 calls q a partial prior contract; Dq tests are defined but not runnable",
            "result": "FAIL_CURRENTLY",
            "why_it_matters": "strict quotient proof cannot start without q and its kernel",
            "repair_route": "construct q formulas or keep Dq_Z_norm as score row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "APG3633_1_XZ_absent_before_variation",
            "clause": "X/Z absent from physical tangent space before matter coupling",
            "current_evidence": "580/669 identify this as best route, but not derived; 1667 still retains residual blocks",
            "result": "FAIL_CURRENTLY",
            "why_it_matters": "if X/Z remains physical, a local pole/source row is unavoidable",
            "repair_route": "prove residual fibre is redundant or move to Z_X, M_X^2, J_X rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "APG3633_2_matter_source_descent",
            "clause": "S_matter, source normalization, clocks, and markers descend through q",
            "current_evidence": "3629/3630 show J_Z=0 only if total source coupling has no linear fibre term",
            "result": "FAIL_CURRENTLY",
            "why_it_matters": "matter can source a field even if the geometry map looks vertical",
            "repair_route": "evaluate Dsource_readout, Dtheta_marker, J_X, and WEP/source charge rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "APG3633_3_boundary_charge_silence",
            "clause": "boundary/projector variation is zero, exact, or proper",
            "current_evidence": "3632 says boundary charge owner is missing",
            "result": "FAIL_CURRENTLY",
            "why_it_matters": "edge charge can reintroduce preferred-frame, source, and memory flux channels",
            "repair_route": "score boundary_projector_Dq_leak and boundary_flux_X if no theorem closes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "APG3633_4_R0_R11_coverage",
            "clause": "all local residual channels R0-R11 are covered by theorem-zero or executable bound",
            "current_evidence": "template has 12 rows; strict quotient only directly targets the X/Yukawa pole route",
            "result": "FAIL_CURRENTLY",
            "why_it_matters": "killing an extra-sector pole is not yet a GR reduction",
            "repair_route": "use R0-R11 coverage gate to keep EH/PPN/source/clock rows separate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "APG3633_5_verdict",
            "clause": "strict quotient absent-pole theorem promoted to live claim",
            "current_evidence": "the conditional theorem is sound, but the parent-owned q/pullback/boundary hypotheses are not live",
            "result": "NO_CLAIM_DQZ_TARGET_SELECTED",
            "why_it_matters": "this prevents both overclaiming and endless circling",
            "repair_route": "next work must construct q enough to compute Dq_Z_norm or demote X/Z to scored residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def coverage_rows(t: str) -> list[dict[str, object]]:
    template = RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv"
    source_rows_local = read_csv(template)
    notes = {
        "R0_identity_coframe_direct": ("conditional", "needs explicit e_obs(q) and same-frame coframe descent"),
        "R1_WEP_source_charge": ("not_covered", "source charge can survive even if direct geometry descends"),
        "R2_clock_redshift": ("not_covered", "clock map/marker descent must be separate"),
        "R3_gamma": ("not_covered", "requires EH metric operator and source normalization"),
        "R4_beta": ("not_covered", "requires second-order EH/source projection"),
        "R5_alpha1": ("not_covered", "preferred-frame vector channels can be boundary/source driven"),
        "R6_alpha2": ("not_covered", "preferred-frame tensor/vector projection still open"),
        "R7_alpha3": ("not_covered", "boundary momentum/edge hair remains open"),
        "R8_xi": ("not_covered", "preferred-location/source coupling not removed by X absence alone"),
        "R9_Gdot": ("not_covered", "time drift of source normalization is a separate readout"),
        "R10_fifth_force": ("conditional_best_hit", "strict quotient would remove X Yukawa pole if absence theorem closes"),
        "R11_EH_operator_ledger": ("partial_only", "X pole absence helps, but EH-only operator selection is still needed"),
    }
    rows: list[dict[str, object]] = []
    for row in source_rows_local:
        row_id = row["row_id"]
        coverage_status, missing = notes[row_id]
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "row_id": row_id,
                "observable": row["observable"],
                "strict_quotient_effect": coverage_status,
                "still_missing": missing,
                "source_template": str(template),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def bound_fill_target_rows(t: str) -> list[dict[str, object]]:
    source_dq = RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv"
    source_rv = RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv"
    source_pack = RESIDUALS / "P8_Y5_R2FR_3632_DQJZ_BOUND_PACK.csv"
    rows = [
        {
            "target_id": "BFT3633_0_Dq_Z_norm",
            "rank": 1,
            "quantity": "Dq_Z_norm",
            "target_type": "Dq_leak",
            "why_first": "it is the exact mathematical obstruction to calling Z a quotient fibre",
            "candidate_formula": "||Dq[partial_Z]|| over (e_obs, source/readout, theta_marker, boundary_projector)",
            "required_inputs": "explicit q components; Z basis; norm convention; arena projection; no-cancellation guard",
            "source_paths": f"{source_dq};{source_pack}",
            "source_ready": False,
            "score_status": "not_scoreable_q_map_missing",
            "next_action": "construct q enough to evaluate Dq[partial_Z], or prove every component is identically zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "target_id": "BFT3633_1_J_X",
            "rank": 2,
            "quantity": "J_X",
            "target_type": "source_current",
            "why_first": "if Dq_Z does not vanish, source-zero is the next clean no-hair route",
            "candidate_formula": "(1/sqrt(-g)) delta(S_matter+S_source+S_hidden)/delta X",
            "required_inputs": "matter pullback; hidden source terms; clock/source normalization; units",
            "source_paths": source_rv,
            "source_ready": False,
            "score_status": "not_scoreable_source_zero_not_derived",
            "next_action": "derive J_X=0 from q-descent or promote it to a sourced residual coefficient",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "target_id": "BFT3633_2_X_operator",
            "rank": 3,
            "quantity": "Z_X;M_X^2;K_X;lambda_X",
            "target_type": "physical_X_operator",
            "why_first": "needed only if X survives as physical rather than absent quotient fibre",
            "candidate_formula": "lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT",
            "required_inputs": "parent Hessian; units; Green-function normalization; source/test charges",
            "source_paths": source_rv,
            "source_ready": False,
            "score_status": "not_scoreable_parent_operator_missing",
            "next_action": "do not start alpha claims until Z_X, M_X^2, K_X, Qbar_XH, qbar_XT are numeric or theorem-zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "target_id": "BFT3633_3_boundary_flux_X",
            "rank": 4,
            "quantity": "boundary_flux_X;Dboundary_projector_Dq_leak",
            "target_type": "boundary_charge",
            "why_first": "boundary charge can defeat both quotient and source-free arguments",
            "candidate_formula": "Q_boundary[partial_X/Z] plus projector leakage in local collar",
            "required_inputs": "boundary class; reference term; Pi_M; compact-collar condition; units",
            "source_paths": f"{source_dq};{source_rv}",
            "source_ready": False,
            "score_status": "not_scoreable_boundary_owner_missing",
            "next_action": "prove Q_boundary=0/exact/proper or retain alpha3/source-normalization edge rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC3633_0_theorem_result",
            "decision": "The strict quotient theorem is mathematically clean: if S_parent is a pullback through q and X/Z live only in ker(Dq) with no boundary charge, no X/Z pole or source exists.",
            "status": "CONDITIONAL_THEOREM_CONSTRUCTED",
            "next_action": "keep this as the preferred route because it removes the coupling rather than tuning it",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3633_1_live_evidence",
            "decision": "The live corpus does not yet satisfy the theorem hypotheses: q is not computable, X/Z absence is not signed, matter/source descent is open, and boundary charge is open.",
            "status": "STRICT_QUOTIENT_NOT_CLAIMED",
            "next_action": "do not claim local-GR/R10/PPN silence from 3633",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3633_2_first_fill",
            "decision": "The first real target is Dq_Z_norm, not another broad audit: construct q and compute Dq[partial_Z] across geometry, source/readout, markers, and boundary.",
            "status": "DQZ_FIRST_TARGET_SELECTED",
            "next_action": "3634 should build the explicit q-map/Dq_Z evaluator or demote Z/X to scored source rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "STRICT_QUOTIENT_THEOREM_CONSTRUCTED_NOT_SIGNED_DQZ_TARGET_SELECTED",
            "summary": "3633 proves the exact conditional absent-pole theorem and then applies it to the live evidence. The theorem is sound but not claim-live because q, matter/source descent, and boundary silence are not parent-owned. The forward move is now sharply reduced to Dq_Z_norm: either compute/prove it zero from an explicit q-map, or treat X/Z as scored residuals.",
            "claim_ceiling": "no local-GR, R10, R11, PPN, WEP, clock, Newton, or X-pole claim is allowed from 3633",
            "useful_result": "the coupling problem is now localized: either X/Z is absent before variation, or J_X and Dq leaks must be real scored quantities",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3633_0",
            "target_doc": "3634-Y5-R2FR-explicit-q-map-and-DqZ-evaluation-or-X-source-row.md",
            "target_script": "scripts/Y5_R2FR_3634_explicit_q_map_and_DqZ_evaluation_or_X_source_row.py",
            "objective": "construct the explicit ordinary-matter quotient q enough to evaluate Dq[partial_Z]; if any q component depends on Z/X, demote the absent-pole route and open J_X/Z_X/M_X^2 source rows",
            "success_gate": "either Dq_Z_norm is theorem-zero componentwise across geometry/source/marker/boundary, or a nonclaim executable row records the first nonzero leak with units/source path/comparator target",
            "reason": "3633 moved the problem from broad owner-chain circling to a single calculable verticality test.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "strict_quotient_absent_pole_theorem",
            "canonical_status": "CONDITIONAL_THEOREM_SOUND_NOT_PARENT_SIGNED",
            "usable_result": "If X/Z are absent from Q before variation and all matter/source/boundary terms descend through q, then J_X=0, i_v Omega is proper/null, and no X Green-function pole exists. Live evidence now reduces to the explicit Dq_Z test.",
            "hard_block": "explicit q-map and componentwise Dq[partial_Z]=0 or sourced residual row",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    output = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(output)


def write_doc(
    src: list[dict[str, object]],
    theorem: list[dict[str, object]],
    q_map: list[dict[str, object]],
    audit: list[dict[str, object]],
    coverage: list[dict[str, object]],
    targets: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3633 Y5 R2FR strict quotient absent-pole theorem or bound-pack fill",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Main result",
            (
                "The useful leap is now exact. If the parent action is genuinely a quotient pullback,\n\n"
                "```text\n"
                "S_parent[Phi] = S_red[q(Phi)] + S_matter[g_obs(q(Phi)), Psi]\n"
                "              + S_source[q(Phi), Psi] + S_boundary[q(Phi)] + S_top[q(Phi)]\n"
                "```\n\n"
                "and `X/Z` are only fibre labels with `Dq[partial_X]=Dq[partial_Z]=0`, then `delta_X S_parent=delta_Z S_parent=0` before fitting, `J_X=J_Z=0`, and there is no `L_X` Green-function pole to mediate an R10/R11 fifth-force row. That is the route we want. The live corpus does not yet sign the hypotheses, so 3633 selects the next non-vague test: compute or prove `Dq_Z_norm=0` componentwise."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Strict quotient theorem",
            table(theorem, ["theorem_id", "claim", "identity", "proof_step", "live_status", "blocks_if_missing"]),
            "## Candidate q map",
            table(q_map, ["map_id", "candidate_component", "allowed_dependency", "forbidden_dependency", "Dq_test", "status", "first_fill_action"]),
            "## Absent-pole live audit",
            table(audit, ["audit_id", "clause", "current_evidence", "result", "repair_route"]),
            "## R0-R11 coverage gate",
            table(coverage, ["row_id", "observable", "strict_quotient_effect", "still_missing"]),
            "## First bound-pack fill targets",
            table(targets, ["target_id", "rank", "quantity", "target_type", "why_first", "candidate_formula", "required_inputs", "score_status", "next_action"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(outputs: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3633_0_sources_exist", all(bool(row["exists"]) for row in src), "all cited source paths exist")
    add("VAL3633_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")

    pre = {name: path for name, path in outputs.items() if name != "validation"}
    add("VAL3633_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")

    details = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3633_3_csv_parse", parse_ok, "; ".join(details))

    theorem = read_csv(outputs["strict_theorem"])
    q_map = read_csv(outputs["candidate_q_map"])
    audit = read_csv(outputs["absent_pole_audit"])
    coverage = read_csv(outputs["r0_r11_coverage"])
    targets = read_csv(outputs["bound_fill_targets"])
    decisions = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    nxt = read_csv(outputs["next_target"])

    add("VAL3633_4_theorem_has_variation_zero", any("delta_v S_parent" in row["identity"] for row in theorem), "pullback variation-zero theorem row present")
    add("VAL3633_5_theorem_has_no_pole_clause", any("no_X_Green_function" in row["identity"] for row in theorem), "absent Green-function pole clause present")
    add("VAL3633_6_q_map_excludes_fibre", any(row["map_id"] == "QMAP3633_4_excluded_residual_fibre" and "Dq[partial_fibre]=0" in row["Dq_test"] for row in q_map), "q-map candidate includes excluded fibre test")
    add("VAL3633_7_live_audit_blocks_claim", any(row["audit_id"] == "APG3633_5_verdict" and row["result"] == "NO_CLAIM_DQZ_TARGET_SELECTED" for row in audit), "live audit prevents claim and selects DqZ target")
    add("VAL3633_8_r0_r11_complete", len(coverage) == 12 and {row["row_id"] for row in coverage} >= {"R0_identity_coframe_direct", "R10_fifth_force", "R11_EH_operator_ledger"}, "all R0-R11 template rows covered")
    add("VAL3633_9_dqz_first_target", bool(targets) and targets[0]["quantity"] == "Dq_Z_norm" and targets[0]["score_status"] == "not_scoreable_q_map_missing", "Dq_Z_norm selected as first non-vague target")
    add("VAL3633_10_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in theorem + q_map + audit + coverage + targets + decisions + status + nxt), "all generated rows remain nonclaim")
    add("VAL3633_11_decision_not_circling", any(row["status"] == "DQZ_FIRST_TARGET_SELECTED" for row in decisions), "decision table narrows next target to DqZ")
    leaks = list(FORMALIZATION.rglob("*3633*")) if FORMALIZATION.exists() else []
    add("VAL3633_12_no_formalization_leak", not leaks, "no 3633 files in formalization-workbench")
    add("VAL3633_13_next_target_written", bool(nxt) and "3634" in nxt[0]["target_doc"], "3634 explicit q/DqZ target written")
    add("VAL3633_14_doc_written", DOC.exists() and "Dq_Z_norm" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with Dq_Z_norm target")
    add("VAL3633_15_canonical_status_written", outputs["canonical_status"].exists() and "CONDITIONAL_THEOREM_SOUND_NOT_PARENT_SIGNED" in outputs["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical strict quotient status written")
    return rows


def main() -> None:
    t = now()
    outputs = out_paths()
    src = source_rows(t)
    theorem = strict_theorem_rows(t)
    q_map = candidate_q_map_rows(t)
    audit = absent_pole_audit_rows(t)
    coverage = coverage_rows(t)
    targets = bound_fill_target_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(outputs["source_register"], src)
    write_csv(outputs["strict_theorem"], theorem)
    write_csv(outputs["candidate_q_map"], q_map)
    write_csv(outputs["absent_pole_audit"], audit)
    write_csv(outputs["r0_r11_coverage"], coverage)
    write_csv(outputs["bound_fill_targets"], targets)
    write_csv(outputs["decision_gates"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], nxt)
    write_csv(outputs["canonical_status"], canonical)
    write_doc(src, theorem, q_map, audit, coverage, targets, decisions, status, nxt)

    validation = validate(outputs, src)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3633 validation failed: {failures}")
    print(f"wrote 3633 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
