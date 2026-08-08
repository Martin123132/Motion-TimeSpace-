from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2109-Y5-R2FR-extra-sector-natural-bundle-lift-or-finite-DqZ-tail-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2108_DOC = ROOT / "2108-Y5-R2FR-field-by-field-vX-parent-action-signature-or-finite-tail-retention.md"
CSV_2108_NATURAL = OUT / "P8_Y5_PARENT_QLOC_2108_NATURAL_LIFT_TEST.csv"
CSV_2108_TAILS = OUT / "P8_Y5_PARENT_QLOC_2108_FINITE_TAIL_RETENTION.csv"
CSV_2108_NEXT = OUT / "P8_Y5_PARENT_QLOC_2108_NEXT_TARGET.csv"
CSV_2108_VAL = OUT / "P8_Y5_BRR545_2108_VALIDATION.csv"

SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
CSV_GK_CONTRACT = OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"
CSV_PIM_CONTRACT = OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
CSV_MASS_FLUX = OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv"
CSV_QCOH = OUT / "P8_QCOH_PARENT_ACTION_CONTRACT.csv"

SRC_1590_DOC = ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md"
CSV_1590_OWNER = OUT / "P8_Y5_PARENT_QLOC_1590_OWNER_BUNDLE_SYNTHESIS.csv"
CSV_1590_FIXED = OUT / "P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv"

SRC_1783_DOC = ROOT / "1783-Y5-R2FR-constraint-first-residual-exclusion-or-DqZ-component-proof.md"
CSV_1783_DQZ = OUT / "P8_Y5_PARENT_QLOC_1783_DQZ_EOBS_COMPONENT_ROWS.csv"
CSV_1783_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1783_EXCLUSION_THEOREM_ATTEMPT.csv"
CSV_1783_ROUTES = OUT / "P8_Y5_PARENT_QLOC_1783_RESIDUAL_EXCLUSION_ROUTE_MATRIX.csv"

SRC_1784_DOC = ROOT / "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md"
CSV_1784_ACTION = OUT / "P8_Y5_PARENT_QLOC_1784_FIELD_ACTION_PACKET.csv"

SRC_1013_DOC = ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
SRC_1014_DOC = ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2109_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2109-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2109*",
        "*Y5_R2FR_extra_sector_natural_bundle_lift_or_finite_DqZ_tail_row_2109*",
        "*AFRAME_EXTRA_SECTOR_NATURALITY_2109*",
        "*JR2109_GK_OWNER*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2109_00_2108_doc",
            SRC_2108_DOC,
            ["NEXT2108_0_2109", "EXTRA_SECTOR_NATURALITY_FIRST", "VAL2108_OVERALL"],
            "2108 selects extra-sector naturality as the next proof fork.",
        ),
        (
            "SRC2109_01_2108_natural",
            CSV_2108_NATURAL,
            ["NLT2108_2_extra_sector", "MISSING_NATURAL_BUNDLE_SIGNATURE", "NLT2108_6_verdict"],
            "2108 natural-lift table isolates the extra-sector blocker.",
        ),
        (
            "SRC2109_02_2108_tails",
            CSV_2108_TAILS,
            ["FTR2108_0_DqZ_geom", "FTR2108_2_memory_projector", "MISSING_ARENA_PROJECTION"],
            "2108 finite-tail table keeps DqZ, memory/projector and arena projections live.",
        ),
        (
            "SRC2109_03_2108_next",
            CSV_2108_NEXT,
            ["NEXT2108_0_2109", "extra-sector-natural-bundle-lift", "finite DqZ"],
            "2108 next-target row points exactly at this checkpoint.",
        ),
        (
            "SRC2109_04_2108_validation",
            CSV_2108_VAL,
            ["VAL2108_OVERALL", "PASS", "extra-sector natural-bundle lift next"],
            "2108 validation passed cleanly.",
        ),
        (
            "SRC2109_05_1009_doc",
            SRC_1009_DOC,
            ["PCS1009_4_Gamma_Khat_extra", "PCS1009_5_domain_projector_selector", "CG1009_3_GK_q_loc_zero"],
            "1009 already narrowed the parent-action problem to Gamma/Khat/q_loc and projector sectors.",
        ),
        (
            "SRC2109_06_GK_contract",
            CSV_GK_CONTRACT,
            ["GK513_0_action_existence", "GK513_3_double_zero", "GK513_5_boundary_no_flux"],
            "Gamma/Khat/q_loc first-variation contract names action, Helmholtz, Euler, double-zero, projector and boundary obligations.",
        ),
        (
            "SRC2109_07_PiM_contract",
            CSV_PIM_CONTRACT,
            ["PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler", "PM8_retained_residual_fallback"],
            "Pi_M contract blocks projector naturality without variation and flux closure.",
        ),
        (
            "SRC2109_08_mass_flux",
            CSV_MASS_FLUX,
            ["MF2_Euler_flux_closure", "MF6_zero_boundary_and_nonHilbert_flux", "MF8_retained_residual_fallback"],
            "Mass-flux contract keeps measured-GM/Newton source normalization open.",
        ),
        (
            "SRC2109_09_Qcoh",
            CSV_QCOH,
            ["C2_domain_selector", "C3_stress_accounting", "C5_no_cancellation"],
            "Qcoh/domain contract says the selector and stress accounting are not parent-derived.",
        ),
        (
            "SRC2109_10_1590_doc",
            SRC_1590_DOC,
            ["OBS1590_0_conditional_theorem", "OBS1590_5_owner_verdict", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS"],
            "1590 identifies the strongest Gamma/Khat/Ploc owner bundle branch but rejects it as current claim.",
        ),
        (
            "SRC2109_11_1590_owner",
            CSV_1590_OWNER,
            ["OBS1590_0_conditional_theorem", "OBS1590_5_owner_verdict", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS"],
            "1590 owner synthesis gives the sharp conditional GK owner theorem and missing clauses.",
        ),
        (
            "SRC2109_12_1590_fixed",
            CSV_1590_FIXED,
            ["FLG1590_0_parent_action_branch", "FLG1590_5_verdict", "ZERO_THEOREM_NOT_DERIVED"],
            "1590 fixed-L0 double-zero branch is best local closure candidate but not live claim.",
        ),
        (
            "SRC2109_13_1783_doc",
            SRC_1783_DOC,
            ["fallback is explicit nonclaim `Dq_Z` component rows", "Claim ceiling"],
            "1783 routes failed residual exclusion into finite DqZ component rows.",
        ),
        (
            "SRC2109_14_1783_DQZ",
            CSV_1783_DQZ,
            ["DZE1783_0_geometry", "DZE1783_5_total_abs", "RETAINED_NONCLAIM_ENVELOPE"],
            "1783 DqZ rows are the finite-tail fallback when naturality/no-pole fails.",
        ),
        (
            "SRC2109_15_1783_theorem",
            CSV_1783_THEOREM,
            ["CFT1783_0_constraint_first_theorem", "CFT1783_4_current_verdict", "FAIL_CURRENT_PARENT_PROOF"],
            "1783 exclusion theorem remains exact conditional but unsigned.",
        ),
        (
            "SRC2109_16_1783_routes",
            CSV_1783_ROUTES,
            ["REM1783_0_quotient_no_pole", "REM1783_4_finite_DqZ", "SCHEMA_READY_NO_VALUES"],
            "1783 route matrix ranks quotient/no-pole first and finite DqZ as fallback.",
        ),
        (
            "SRC2109_17_1784_doc",
            SRC_1784_DOC,
            ["field-by-field `v_X`", "fallback is explicit finite `Dq_Z[e_obs,g_obs]`"],
            "1784 Omega/DCX packet keeps field action incomplete and DqZ fallback live.",
        ),
        (
            "SRC2109_18_1784_action",
            CSV_1784_ACTION,
            ["FAP1784_2_Gamma_Khat_qloc", "FAP1784_3_domain_memory_projector", "UNMAPPED"],
            "1784 field-action packet names GK and domain/memory/projector gaps.",
        ),
        (
            "SRC2109_19_1013_doc",
            SRC_1013_DOC,
            ["PFC1013_8_verdict", "OBS1013_1_PiM_commutator", "CG1013_0_flux_closure"],
            "1013 gives the exact Pi_M flux obstruction vector.",
        ),
        (
            "SRC2109_20_1014_doc",
            SRC_1014_DOC,
            ["PCT1014_7_verdict", "PCC1014_1_I_commutator", "fail_current_claim"],
            "1014 blocks Pi_M commutator/projector variation zero.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2109_extra_sector_naturality",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2109=use,
                valid_for_claim=False,
            )
        )
    return rows


def extra_sector_naturality_rows() -> list[dict[str, object]]:
    specs = [
        (
            "ESN2109_0_target",
            "extra-sector naturality",
            "Gamma/Khat/q_loc, domain, memory and projector variables must be natural parent-bundle objects or quotient/proper-gauge representatives under the same v_X lift as metric/coframe.",
            "TARGET_SHARP",
            "would let the local-GR proof use one parent symmetry instead of separate closures",
            "field action and covariant Lagrangian for each extra block",
        ),
        (
            "ESN2109_1_GK_action",
            "Gamma/Khat/q_loc",
            "There exists covariant scalar-density S_GK[g,Phi] whose metric response is K_hat/Gamma_eff and whose Euler/Ward identity makes q_loc an on-shell residual.",
            "CONDITIONAL_THEOREM_SHARP_NOT_PARENT_SIGNED",
            "this is the cleanest core route if parent-signed",
            "S_GK source, Helmholtz, Euler closure, Khat metric-response match and P_loc owner",
        ),
        (
            "ESN2109_2_fixed_L0_double_zero",
            "fixed-L0 double-zero branch",
            "S_GK^0=-int sqrt(-g)L0^-2 Fhat(m;m*) with Fhat(m*)=Fhat_prime(m*)=0 can close algebraic local stress pieces under strict clauses.",
            "BEST_LOCAL_CLOSURE_BRANCH_NOT_LIVE_CLAIM",
            "gives a serious candidate for q_loc suppression without tuning c_g by hand",
            "parent adoption, universal m*, sign convention, K_conn/K_domain/K_boundary and memory stress",
        ),
        (
            "ESN2109_3_domain_selector",
            "chi_D/Qcoh/domain",
            "Domain selector and coherent projector are selected by parent Euler/topological law before readout, not by fitting a local mask.",
            "NOT_DERIVED",
            "would prevent local/FLRW branch choice from being post hoc",
            "delta S/delta chi_D, Qcoh parent variable, domain stress and branch rule",
        ),
        (
            "ESN2109_4_projector_PiM",
            "Pi_M/source projector",
            "Pi_M is a parent symplectic/cohomological/source-current map whose variation, commutator and stress are owned.",
            "NOT_PARENT_DERIVED",
            "would protect Newtonian measured-GM/source normalization",
            "projector variation, [d,Pi_M]J_H, flux closure and calibration",
        ),
        (
            "ESN2109_5_memory_response",
            "memory/response sector",
            "Memory/response doublet is a parent field system with local zero theorem or scored finite residual under the same lift.",
            "PARTIAL_CANDIDATE_NOT_MAPPED",
            "would align cosmology memory with local suppression instead of treating them as disconnected",
            "complete component map, source silence, positivity and PPN lock",
        ),
        (
            "ESN2109_6_boundary_support",
            "boundary/support tails",
            "Extra-sector boundary, support and source-normalization terms are exact/proper/topological or explicitly retained.",
            "OPEN",
            "prevents local source hair from hiding in boundary/projector channels",
            "boundary no-flux, support-map ownership and measured-Hamiltonian projection",
        ),
        (
            "ESN2109_7_verdict",
            "extra-sector natural-bundle lift",
            "ESN2109_1 through ESN2109_6 close on the same parent branch.",
            "FAIL_CURRENT_CLAIM",
            "the route is promising but not claim-grade; finite DqZ/GK/projector tails remain live",
            "S_GK owner first, then domain/projector/boundary closure",
        ),
    ]
    return [
        row(
            naturality_id=naturality_id,
            object=object_,
            required_statement=required_statement,
            current_status=current_status,
            if_true=if_true,
            missing_for_claim=missing_for_claim,
            valid_for_claim=False,
        )
        for naturality_id, object_, required_statement, current_status, if_true, missing_for_claim in specs
    ]


def gk_action_test_rows() -> list[dict[str, object]]:
    specs = [
        ("GK2109_0_action_existence", "S_GK[g,Phi] exists as local diffeomorphism-invariant scalar action", "GK513_0", "NOT_SUPPLIED", "Gamma_eff/K_hat remain bookkeeping if absent"),
        ("GK2109_1_helmholtz", "T_GK satisfies variational Helmholtz/integrability conditions", "GK513_1", "NOT_CHECKED", "no action exists for claimed stress if it fails"),
        ("GK2109_2_euler_ward", "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A and vanishes on compact local vacuum shell", "GK513_2", "NOT_DERIVED", "stress divergence remains source-exchange residual"),
        ("GK2109_3_double_zero", "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0", "GK513_3/FLG1590_1", "STRICT_CONTRACT_WRITTEN_NOT_PARENT_SIGNED", "F_1/local PPN hair remains if missing"),
        ("GK2109_4_Khat_metric_response", "K_hat equals metric response of the same S_GK branch", "OBS1590_0", "CONDITIONAL_THEOREM_SHARP_NOT_PARENT_SIGNED", "q_loc cannot be called on-shell Ward residual"),
        ("GK2109_5_Ploc_owner", "P_loc is parent-owned and commutes with fixed-point/readout limit", "GK513_4", "OPEN", "projection can hide force components"),
        ("GK2109_6_boundary_no_flux", "theta_GK/Q_GK/boundary flux is zero/topological/proper on compact branch", "GK513_5", "OPEN", "bulk q_loc silence leaks through boundary"),
        ("GK2109_7_owner_verdict", "same parent branch owns S_GK, Khat, Ploc, double-zero and boundary silence", "OBS1590_5", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS", "no local-GR promotion from GK branch"),
    ]
    return [
        row(
            test_id=test_id,
            requirement=requirement,
            source_clause=source_clause,
            current_status=current_status,
            failure_if_missing=failure_if_missing,
            valid_for_claim=False,
        )
        for test_id, requirement, source_clause, current_status, failure_if_missing in specs
    ]


def domain_projector_rows() -> list[dict[str, object]]:
    specs = [
        ("DPL2109_0_Qcoh_parent", "Qcoh is an action variable or derived Noether/load tensor", "C0_parent_variable", "MISSING_EXPLICIT_PARENT_VARIABLE", "Qcoh branch stays closure-only"),
        ("DPL2109_1_domain_selector", "chi_D/domain selected by parent Euler/topological law", "C2_domain_selector", "NOT_DERIVED", "domain mask can be post-hoc"),
        ("DPL2109_2_domain_stress", "metric variation of P_coh and chi_D vanishes or is retained", "C3_stress_accounting", "RETAINED_DEBT", "projector/domain stress feeds PPN/source rows"),
        ("DPL2109_3_PiM_origin", "Pi_M comes from parent cohomology/symplectic/source identity before readout", "PM0/MF0", "CANDIDATE_ORIGIN_NOT_COMPLETED", "measured-GM map remains closure-only"),
        ("DPL2109_4_PiM_variation", "delta Pi_M terms are included or theorem-zero", "PM5", "NOT_PARENT_DERIVED", "hidden projector stress/source force remains"),
        ("DPL2109_5_flux_closure", "d(Pi_M J_H)=0 follows from Ward/Euler/topological equation", "PM6/MF2", "NOT_PARENT_DERIVED", "M_eff radial drift/source flux rows remain"),
        ("DPL2109_6_commutator", "[d,Pi_M]J_H=0 or bounded", "1013/1014", "FAIL_CURRENT_CLAIM", "commutator contaminates source normalization"),
        ("DPL2109_7_no_cancellation", "boundary/domain/projector channels are not cancelled by hand", "C5", "GUARD_ACTIVE", "finite rows stay absolute-summed"),
        ("DPL2109_8_verdict", "domain/memory/projector natural lift closes", "2108/2109", "FAIL_CURRENT_CLAIM", "finite projector/source-support tails stay live"),
    ]
    return [
        row(
            lift_id=lift_id,
            requirement=requirement,
            source_clause=source_clause,
            current_status=current_status,
            failure_if_missing=failure_if_missing,
            valid_for_claim=False,
        )
        for lift_id, requirement, source_clause, current_status, failure_if_missing in specs
    ]


def dqz_tail_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DQZ2109_0_geometry",
            "Dq_Z[e_obs,g_obs]",
            "epsilon_Z_geom := ||D_Z e_obs|| + ||D_Z g_obs||",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "DZE1783_0_geometry",
            "finite observed-geometry leak if extra-sector naturality fails",
        ),
        (
            "DQZ2109_1_GK_q_loc",
            "Gamma/Khat/q_loc naturality residual",
            "epsilon_GK := ||delta_v Gamma_eff|| + ||delta_v K_hat|| + ||q_loc||",
            "MISSING_SGK_OWNER_OR_NUMERIC_BOUND",
            "GK513/1590",
            "finite source/current tail if S_GK owner bundle fails",
        ),
        (
            "DQZ2109_2_domain_projector",
            "chi_D/Qcoh/Pi_M/support residual",
            "epsilon_proj := ||delta_v chi_D||+||delta_v Qcoh||+||[d,Pi_M]J_H||+||delta Pi_M||",
            "MISSING_PROJECTOR_THEOREM_OR_NUMERIC_BOUND",
            "Qcoh/PiM/1013/1014",
            "finite projector/source-support tail",
        ),
        (
            "DQZ2109_3_source_readout",
            "Dq_Z[source/readout/theta_A]",
            "epsilon_readout := ||Dsource||+||Dclock||+||Dorbit||+||Dtheta_A||",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "DZE1783_1/DZE1783_2",
            "finite matter/readout/constant marker leak",
        ),
        (
            "DQZ2109_4_boundary_tau",
            "Dq_Z[boundary/projector/tau]",
            "epsilon_boundary := ||Dboundary||+||Dprojector||+||Dq(L_tau Phi)-L_tau_red q(Phi)||",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "DZE1783_3",
            "finite boundary/tau/projector tail",
        ),
        (
            "DQZ2109_5_component_lock",
            "Z_to_Yloc_projection",
            "epsilon_map := ||Y_loc-Z|| over q_loc/PPN/source/coupling components",
            "MISSING_COMPONENT_MAP",
            "DZE1783_4",
            "cannot translate DqZ into observable local residual without this",
        ),
        (
            "DQZ2109_6_total_abs",
            "epsilon_extra_abs",
            "abs(DQZ2109_0)+abs(DQZ2109_1)+abs(DQZ2109_2)+abs(DQZ2109_3)+abs(DQZ2109_4)+abs(DQZ2109_5)",
            "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "DZE1783_5_total_abs",
            "nonclaim no-cancellation envelope for local tests",
        ),
    ]
    return [
        row(
            tail_id=tail_id,
            retained_tail=retained_tail,
            finite_formula=finite_formula,
            current_status=current_status,
            source_anchor=source_anchor,
            meaning=meaning,
            score_ready=False,
            valid_prediction_row=False,
            valid_for_claim=False,
        )
        for tail_id, retained_tail, finite_formula, current_status, source_anchor, meaning in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2109_0_target_written", "extra-sector naturality gate is written", True, "GK, domain, memory/projector, Pi_M and DqZ tails are separated"),
        ("GATE2109_1_GK_action_owned", "S_GK/Khat/q_loc owner bundle is parent-signed", False, "1590 says owner bundle is conditional but not claim-grade"),
        ("GATE2109_2_fixed_L0_live", "fixed-L0 double-zero branch is live parent action", False, "parent adoption, universal m*, cdb/memory/boundary residuals missing"),
        ("GATE2109_3_domain_projector_owned", "domain/memory/projector lift is parent-owned", False, "chi_D/Qcoh/Pi_M variation and flux closure remain unsigned"),
        ("GATE2109_4_DqZ_zero", "DqZ component residuals are theorem-zero", False, "1783 keeps DqZ component rows nonclaim and value-missing"),
        ("GATE2109_5_finite_tail_policy", "finite DqZ/GK/projector tails retained", True, "fallback rows are explicit, nonclaim and no-cancellation"),
        ("GATE2109_6_local_GR_Newton", "derived local GR/Newton follows", False, "extra-sector natural-bundle lift is not parent-signed"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=gate_pass,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, gate, gate_pass, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2109_0_result",
            "EXTRA_SECTOR_NATURALITY_NOT_CLOSED",
            "The GK owner bundle is promising but not parent-signed; domain/projector/memory sectors remain explicit residual channels.",
            "no local-GR or no-pole promotion from 2109",
        ),
        (
            "DEC2109_1_best_positive_route",
            "GK_OWNER_BUNDLE_FIRST",
            "S_GK/Khat/q_loc is the core local-residual sector and has the strongest conditional theorem plus fixed-L0 double-zero candidate.",
            "try to parent-sign S_GK^0/Khat metric response and isolate cdb/memory/boundary residuals",
        ),
        (
            "DEC2109_2_fallback",
            "FINITE_DQZ_GK_PROJECTOR_TAILS_RETAINED",
            "If GK ownership fails, the theory must carry DqZ/GK/projector tails into local-test bound rows with units and source paths.",
            "absolute-sum residual envelope; no cancellation and no claim-valid rows",
        ),
        (
            "DEC2109_3_projector_timing",
            "PROJECTOR_AFTER_GK_OWNER",
            "Pi_M/domain calculations need the extra-sector current/action first; otherwise projector algebra closes the wrong object.",
            "do not compute boundary/degree proof before field-action owner is selected",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
            valid_for_claim=False,
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2109_0_2110",
            next_target="2110-Y5-R2FR-Gamma-Khat-q_loc-parent-action-owner-or-DqZ-GK-tail-bound.md",
            script="scripts/Y5_R2FR_Gamma_Khat_q_loc_parent_action_owner_or_DqZ_GK_tail_bound_2110.py",
            objective="Try to parent-sign the S_GK/Khat/q_loc owner bundle: action existence, Helmholtz integrability, Khat metric-response match, fixed-L0 double-zero branch, P_loc ownership, and boundary/no-flux closure; if it fails, retain a finite GK/q_loc tail row with source paths, units, common norm and no-cancellation.",
            forbidden_shortcuts="claiming Gamma/Khat naturality from covariance language only; fixed-L0 closure without parent adoption; ignoring K_conn/K_domain/K_boundary/memory stress; projector closure before GK current exists; local-GR/Newton claim; formalization-workbench edits; GitHub action",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    naturality: list[dict[str, object]],
    gk_tests: list[dict[str, object]],
    projector: list[dict[str, object]],
    tails: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2109_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_EXTRA_SECTOR_NATURALITY_2109_NONCLAIM.csv",
            naturality + gk_tests + projector + decisions,
        ),
        (
            "COPY2109_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2109_EXTRA_SECTOR_STATUS_NONCLAIM.csv",
            gk_tests + projector + tails,
        ),
        (
            "COPY2109_2_acquisition_queue",
            QUEUE / "JR2109_GK_OWNER_OR_DQZ_TAIL_QUEUE.csv",
            tails + next_target,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, copy_rows in copies:
        write_csv(path, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(path),
                path_exists=path.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    naturality: list[dict[str, object]],
    gk_tests: list[dict[str, object]],
    projector: list[dict[str, object]],
    tails: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    naturality_ok = any(row_.get("naturality_id") == "ESN2109_7_verdict" and row_.get("current_status") == "FAIL_CURRENT_CLAIM" for row_ in naturality)
    gk_ok = any(row_.get("test_id") == "GK2109_7_owner_verdict" and row_.get("current_status") == "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS" for row_ in gk_tests)
    projector_ok = any(row_.get("lift_id") == "DPL2109_8_verdict" and row_.get("current_status") == "FAIL_CURRENT_CLAIM" for row_ in projector)
    tails_ok = (
        len(tails) >= 7
        and any(row_.get("tail_id") == "DQZ2109_6_total_abs" and row_.get("current_status") == "MISSING_COMPONENT_VALUES_AND_COMMON_NORM" for row_ in tails)
        and all(not truthy(row_.get("valid_for_claim")) for row_ in tails)
    )
    gates_ok = (
        all(not truthy(row_.get("claim_allowed")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2109_6_local_GR_Newton" and not truthy(row_.get("gate_pass")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2109_5_finite_tail_policy" and truthy(row_.get("gate_pass")) for row_ in gates)
    )
    decision_ok = any(row_.get("decision") == "GK_OWNER_BUNDLE_FIRST" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2109_0_2110" and "Gamma-Khat-q_loc" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready"))
        for collection in (sources, naturality, gk_tests, projector, tails, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2109_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2109_00_sources", sources_ok, "all cited source paths exist and contain expected extra-sector/DqZ needles"),
        ("VAL2109_01_naturality", naturality_ok, "extra-sector naturality gate is complete and fails current claim"),
        ("VAL2109_02_GK_owner", gk_ok, "GK owner bundle is recognized as strongest candidate but not claim-grade"),
        ("VAL2109_03_projector", projector_ok, "domain/memory/projector lift remains nonclaim"),
        ("VAL2109_04_DqZ_tails", tails_ok, "finite DqZ/GK/projector tails are retained explicitly and unscoreable"),
        ("VAL2109_05_claim_gates", gates_ok, "local-GR/Newton gate remains blocked while finite-tail policy passes"),
        ("VAL2109_06_decision", decision_ok, "decision selects GK owner bundle first"),
        ("VAL2109_07_next", next_ok, "next target is 2110 Gamma/Khat/q_loc owner or finite GK tail bound"),
        ("VAL2109_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2109_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2109_10_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2109_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2109"),
        ("VAL2109_12_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2109_OVERALL",
            overall,
            "2109 tests extra-sector naturality, rejects current local-GR promotion, retains finite DqZ tails, and selects GK owner bundle next",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if ok else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, ok, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    naturality: list[dict[str, object]],
    gk_tests: list[dict[str, object]],
    projector: list[dict[str, object]],
    tails: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2109 - Y5/R2FR Extra-Sector Natural-Bundle Lift Or Finite DqZ Tail Row",
        "",
        "## Current Verdict",
        "",
        "2109 tries the right leap: make the non-GR MTS sectors natural parent-bundle objects under the same proper `v_X` lift as the metric/coframe. The result is useful but not a promotion. `Gamma/Khat/q_loc` has the strongest candidate route through a parent `S_GK` owner bundle and the fixed-`L0` double-zero branch, but that branch is still not parent-signed.",
        "",
        "The domain, memory, `Qcoh`, `Pi_M`, source-support and projector sectors remain explicit residual channels. Projector algebra is not flux closure, and a closed topological current is not automatically the observed Hilbert/measured-GM current. Therefore the finite `DqZ/GK/projector` tail envelope stays live and nonclaim.",
        "",
        "The next positive route is not another generic no-pole pass. It is the concrete `S_GK/Khat/q_loc` owner bundle: action existence, Helmholtz integrability, Khat metric-response match, fixed-`L0` double zero, `P_loc` ownership, and boundary/no-flux closure.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2109", "valid_for_claim"]),
        "## Extra-Sector Naturality Gate",
        md_table(naturality, ["naturality_id", "object", "current_status", "required_statement", "if_true", "missing_for_claim", "valid_for_claim"]),
        "## GK Action Naturality Test",
        md_table(gk_tests, ["test_id", "requirement", "source_clause", "current_status", "failure_if_missing", "valid_for_claim"]),
        "## Domain/Projector Lift Test",
        md_table(projector, ["lift_id", "requirement", "source_clause", "current_status", "failure_if_missing", "valid_for_claim"]),
        "## Finite DqZ Tail Rows",
        md_table(tails, ["tail_id", "retained_tail", "current_status", "finite_formula", "source_anchor", "meaning", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "gate", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target",
        md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    naturality = extra_sector_naturality_rows()
    gk_tests = gk_action_test_rows()
    projector = domain_projector_rows()
    tails = dqz_tail_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2109_SOURCE_REGISTER.csv",
        "naturality": OUT / "P8_Y5_PARENT_QLOC_2109_EXTRA_SECTOR_NATURALITY_GATE.csv",
        "gk_tests": OUT / "P8_Y5_PARENT_QLOC_2109_GK_ACTION_NATURALITY_TEST.csv",
        "projector": OUT / "P8_Y5_PARENT_QLOC_2109_DOMAIN_PROJECTOR_LIFT_TEST.csv",
        "tails": OUT / "P8_Y5_PARENT_QLOC_2109_DQZ_FINITE_TAIL_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2109_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2109_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2109_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2109_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2109_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["naturality"], naturality)
    write_csv(paths["gk_tests"], gk_tests)
    write_csv(paths["projector"], projector)
    write_csv(paths["tails"], tails)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(naturality, gk_tests, projector, tails, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, naturality, gk_tests, projector, tails, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, naturality, gk_tests, projector, tails, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
