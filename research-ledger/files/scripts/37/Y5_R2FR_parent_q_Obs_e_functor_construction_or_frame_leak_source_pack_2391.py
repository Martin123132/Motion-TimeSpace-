from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PARENT_Q_OBS_E_FUNCTOR_CONSTRUCTION_OR_FRAME_LEAK_SOURCE_PACK_2391"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2391_00_2390_doc",
            "source_key": "2390_q_Obs_e_handoff",
            "source_path": POST_ROOT / "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md",
            "needles": ["2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md", "epsilon_q_owner", "epsilon_DObs_e"],
            "source_role": "2390 selected parent q/Obs_e functor construction",
        },
        {
            "row_id": "SRC2391_01_2390_certificates",
            "source_key": "2390_same_frame_certificates",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv",
            "needles": ["SFC2390_0_parent_q", "MISSING_PARENT_Q_MAP", "SFC2390_1_Obs_e"],
            "source_role": "q and Obs_e ownership gaps",
        },
        {
            "row_id": "SRC2391_02_2390_leaks",
            "source_key": "2390_frame_source_leaks",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2390_FRAME_SOURCE_LEAK_VALUES.csv",
            "needles": ["epsilon_q_owner", "epsilon_DObs_e", "Delta_same_frame_total_over_MH"],
            "source_role": "frame leak rows to refine",
        },
        {
            "row_id": "SRC2391_03_945_doc",
            "source_key": "945_q_candidate_warning",
            "source_path": POST_ROOT / "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            "needles": ["q_candidate(Phi)", "Obs_e(q_candidate) = e_obs", "projection-by-declaration trick"],
            "source_role": "q candidate and tautological projection warning",
        },
        {
            "row_id": "SRC2391_04_1737_doc",
            "source_key": "1737_q_Dq_basis",
            "source_path": POST_ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            "needles": ["visible quotient candidate `Q_vis`", "DObs_e[v]=0", "not jointly signed"],
            "source_role": "Q_vis and Dq vertical basis source rows",
        },
        {
            "row_id": "SRC2391_05_1738_doc",
            "source_key": "1738_coframe_kernel",
            "source_path": POST_ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
            "needles": ["chain-rule coframe-kernel theorem is exact", "single universal coframe is not enough", "`e_obs=exp(b_g X)e0`"],
            "source_role": "coframe kernel theorem and common-frame counterexample",
        },
        {
            "row_id": "SRC2391_06_1739_doc",
            "source_key": "1739_parent_coframe_ownership",
            "source_path": POST_ROOT / "1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md",
            "needles": ["e_obs=E(Q_vis)", "`b_g=0` by the chain rule", "remain unsigned"],
            "source_role": "parent coframe ownership stack",
        },
        {
            "row_id": "SRC2391_07_1879_doc",
            "source_key": "1879_common_frame_leak",
            "source_path": POST_ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
            "needles": ["e_obs = E(Q_vis)", "D_C_R e_obs = 0", "hidden universal Weyl/disformal/source-prefactor slot"],
            "source_role": "common-frame leak residual stack",
        },
        {
            "row_id": "SRC2391_08_1963_doc",
            "source_key": "1963_owned_coframe_action",
            "source_path": POST_ROOT / "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md",
            "needles": ["S_parent = S_MTS_core[Xi,e,q]", "CANDIDATE_ACTION_WRITTEN_NONCANONICAL", "must be promoted into a canonical parent action"],
            "source_role": "candidate owned-coframe parent action branch",
        },
        {
            "row_id": "SRC2391_09_1964_doc",
            "source_key": "1964_legitimacy",
            "source_path": POST_ROOT / "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md",
            "needles": ["e_obs=E[q(Phi_MTS)]", "GR_INSERTION_RISK_EXPLICIT", "SCALAR_GRADIENT_ROUTE_TOO_RESTRICTIVE"],
            "source_role": "owned coframe legitimacy and GR insertion risk",
        },
        {
            "row_id": "SRC2391_10_2006_doc",
            "source_key": "2006_EqPhi_readout_map",
            "source_path": POST_ROOT / "2006-Y5-R2FR-parent-EqPhi-coframe-readout-map-or-owned-coframe-closure-demotion.md",
            "needles": ["partial win, not a full proof", "e_obs=E[q(Phi_MTS)]", "projection-by-declaration warning"],
            "source_role": "constructive coframe-readout map attempt and demotion",
        },
        {
            "row_id": "SRC2391_11_2048_doc",
            "source_key": "2048_motion_load_coframe",
            "source_path": POST_ROOT / "2048-Y5-R2FR-motion-load-coframe-construction-or-CMTS-provenance.md",
            "needles": ["motion-load route can construct a local observed coframe", "T sqrt(S)=1", "all ordinary matter/source/readout sectors use this coframe"],
            "source_role": "concrete static coframe branch and remaining local-GR blockers",
        },
        {
            "row_id": "SRC2391_12_2323_doc",
            "source_key": "2323_common_matter_frame",
            "source_path": POST_ROOT / "2323-Y5-R2FR-common-matter-frame-action-signature-or-readout-tail-row.md",
            "needles": ["ordinary matter frame `e_obs(q(Phi))`", "`alpha_readout=0`", "The active branch is not there yet"],
            "source_role": "common matter frame readout-tail theorem",
        },
    ]
    rows: list[dict[str, object]] = []
    for source in sources:
        path = Path(source["source_path"])
        needles = list(source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": source["row_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": str(path.exists()).lower(),
                "required": "true",
                "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                "needles": "; ".join(needles),
                "source_role": source["source_role"],
                "valid_for_claim": no_claim(),
            }
        )
    return rows


def functor_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOF2391_0_quotient_foliation",
            "step": "regular parent quotient",
            "statement": "Let V be the parent vertical distribution of locally unobserved/residual directions. If V is involutive, regular, and integrates to a free/proper equivalence relation, then Q_vis := Phi_parent/V exists locally and q: Phi_parent -> Q_vis is a submersion.",
            "derivation_status": "CONDITIONAL_QUOTIENT_EXISTENCE_THEOREM",
            "current_gain": "turns q from a label into a geometric quotient criterion",
            "remaining_gap": "V, integrability, regular rank, and free/proper quotient are not parent-signed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOF2391_1_basic_coframe",
            "step": "basic observed coframe",
            "statement": "If a parent coframe candidate e_parent[Phi] is constant on q-fibres, equivalently Lie_v e_parent=0 for every v in V, then there is a unique Obs_e on Q_vis with e_parent = Obs_e o q.",
            "derivation_status": "CONDITIONAL_DESCENT_THEOREM",
            "current_gain": "gives the exact contract for e_obs(Phi)=Obs_e(q(Phi))",
            "remaining_gap": "Lie_v e_parent=0 is not proven for the current MTS parent fields",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOF2391_2_kernel_zero",
            "step": "DObs_e kernel zero",
            "statement": "Once e_parent = Obs_e o q, every v in ker(Dq) satisfies DObs_e[Dq(v)] = 0 and Lie_v e_obs=0; the local frame response vanishes by chain rule.",
            "derivation_status": "CONDITIONAL_KERNEL_ZERO",
            "current_gain": "connects q/Obs_e ownership directly to the 2390 same-frame theorem",
            "remaining_gap": "kernel membership and source-weighted norms remain unmeasured/unproved",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOF2391_3_tautology_guard",
            "step": "projection-by-declaration guard",
            "statement": "Defining q_candidate(Phi) to include e_obs and then setting Obs_e(q_candidate)=e_obs is projection-by-declaration, not claim-grade, unless ker(Dq_candidate) is proven presymplectic-null, matter-invisible, and no-marker/no-shadow.",
            "derivation_status": "ANTI_TAUTOLOGY_GUARD",
            "current_gain": "prevents importing the desired coframe as a quotient proof",
            "remaining_gap": "presymplectic-null and matter-invisible kernel certificates are missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOF2391_4_owned_branch_status",
            "step": "owned-coframe branch status",
            "statement": "The 1963/2048 owned-coframe branches supply plausible candidate coframe objects, including a concrete static motion-load coframe, but they do not yet prove the full parent quotient map, transverse legs, determinant, no-shadow, readout, tau, and source support stack.",
            "derivation_status": "CANDIDATE_BRANCH_NOT_CANONICAL",
            "current_gain": "keeps the coframe route alive without pretending it is already canonical local GR",
            "remaining_gap": "canonical parent action and sector exceptions remain open",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOF2391_5_shadow_countermodel",
            "step": "shadow-frame countermodel",
            "statement": "A universal frame e_obs=exp(b_g X) E(Q_vis) is one public frame but not quotient-basic unless b_g=0 or X is included as a physical visible coordinate; therefore shadow-frame terms must be zeroed or bounded.",
            "derivation_status": "OBSTRUCTION_RETAINED",
            "current_gain": "clarifies why one-frame language is weaker than quotient descent",
            "remaining_gap": "b_g, b_dis, b_A, q_nonH, source-prefactor, and readout-tail rows remain live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOF2391_6_verdict",
            "step": "current verdict",
            "statement": "2391 can state the exact parent contract for q/Obs_e descent, but current MTS does not yet satisfy it. The next leap is to prove V is a parent-null/matter-invisible quotient distribution or demote q/Obs_e to a closure branch with finite frame-leak rows.",
            "derivation_status": "ROUTE_EXACT_NOT_CLAIMED",
            "current_gain": "the same-frame problem is now a quotient/fibre theorem problem",
            "remaining_gap": "all q/Obs_e ownership rows remain nonclaim",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_0_parent_vertical_distribution",
            "certificate": "parent vertical distribution V",
            "required_test": "define the local unobserved/residual vertical vectors as parent variations, not post-readout labels",
            "status": "MISSING_PARENT_VERTICAL_DISTRIBUTION",
            "residual_if_missing": "epsilon_q_owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_1_regular_integrable_quotient",
            "certificate": "regular integrable quotient",
            "required_test": "V has constant rank, is involutive, and integrates to a local quotient Q_vis with q a submersion",
            "status": "MISSING_REGULAR_INTEGRABLE_QUOTIENT_PROOF",
            "residual_if_missing": "epsilon_q_rank_or_integrability",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_2_presymplectic_null",
            "certificate": "presymplectic-null kernel",
            "required_test": "i_v Theta_parent = dB_v with zero compact local flux, so vertical directions carry no physical Hamiltonian charge",
            "status": "MISSING_PRESYMPLECTIC_NULL_KERNEL",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_3_basic_coframe",
            "certificate": "basic coframe over q",
            "required_test": "Lie_v e_parent=0 for every v in V, or a source-weighted DObs_e bound is supplied",
            "status": "MISSING_BASIC_COFRAME_PROOF",
            "residual_if_missing": "epsilon_DObs_e",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_4_no_projection_declaration",
            "certificate": "no projection-by-declaration",
            "required_test": "q may not include e_obs as a tautological component unless its kernel is already proven null/matter-invisible",
            "status": "MISSING_ANTI_TAUTOLOGY_CERTIFICATE",
            "residual_if_missing": "epsilon_projection_declaration",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_5_no_shadow_frame",
            "certificate": "no shadow frame/source slot",
            "required_test": "no Weyl/disformal/species/source-prefactor/readout-tail variable survives outside q/Obs_e",
            "status": "MISSING_NO_SHADOW_FRAME_THEOREM",
            "residual_if_missing": "epsilon_shadow_frame",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_6_matter_readout_descent",
            "certificate": "matter/readout/tau descent through q/Obs_e",
            "required_test": "matter, clocks, rods, photons, orbit, source worldtube, PPN projectors, and tau are functors of the same q/Obs_e data",
            "status": "MISSING_ALL_SECTOR_DESCENT",
            "residual_if_missing": "alpha_readout_or_Delta_W_support",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOC2391_7_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "derive H_tau-H_ref in the same q/Obs_e/tau branch with no orbital-GM import",
            "status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "all normalized rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


def leak_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_0_q_owner",
            "quantity": "epsilon_q_owner",
            "formula": "abs(integral_S (J_H[q_candidate]-J_H[q_parent]))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_Q_MAP;MISSING_JH_DENSITY;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_1_q_rank_integrability",
            "quantity": "epsilon_q_rank_or_integrability",
            "formula": "||[v_i,v_j] mod V|| + ||rank(Dq)-rank_expected||",
            "units": "field-space quotient defect",
            "current_value": "MISSING_VERTICAL_BASIS;MISSING_BRACKET_TABLE;MISSING_RANK_AUDIT",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_2_kernel_charge",
            "quantity": "epsilon_kernel_charge",
            "formula": "abs(integral_S (delta Q_v - i_v theta_parent))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_THETA_PARENT;MISSING_Q_V;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_3_DObs_e",
            "quantity": "epsilon_DObs_e",
            "formula": "||Lie_v e_parent||_source_weighted / ||e_parent||",
            "units": "dimensionless frame response",
            "current_value": "MISSING_BASIC_COFRAME_PROOF;MISSING_SOURCE_WEIGHT;MISSING_VERTICAL_BASIS",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_4_projection_declaration",
            "quantity": "epsilon_projection_declaration",
            "formula": "1 if q includes e_obs without null-kernel proof else 0",
            "units": "boolean guard",
            "current_value": "MISSING_ANTI_TAUTOLOGY_CERTIFICATE",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_5_shadow_frame",
            "quantity": "epsilon_shadow_frame",
            "formula": "abs(b_g)+abs(b_dis)+abs(b_A)+abs(q_nonH)+abs(source_prefactor_leak)",
            "units": "dimensionless leading frame/source envelope",
            "current_value": "MISSING_BG;MISSING_BDIS;MISSING_BA;MISSING_Q_NONH;MISSING_SOURCE_PREFACTOR_BOUND",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_6_all_sector_descent",
            "quantity": "epsilon_all_sector_descent",
            "formula": "abs(alpha_readout)+abs(Delta_W_support)+abs(Delta_tau_n)+abs(clock_rod_lightcone_frame_tail)",
            "units": "dimensionless readout/source envelope",
            "current_value": "MISSING_PROJECTOR_DESCENT;MISSING_SUPPORT_DESCENT;MISSING_TAU_NORMALIZATION;MISSING_CLOCK_ROD_LIGHTCONE_DESCENT",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QEL2391_7_total",
            "quantity": "Delta_q_Obs_e_total_over_MH",
            "formula": "epsilon_q_owner + epsilon_q_rank_or_integrability + epsilon_kernel_charge + epsilon_DObs_e + epsilon_projection_declaration + epsilon_shadow_frame + epsilon_all_sector_descent",
            "units": "dimensionless",
            "current_value": "COMPONENTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2391_0_accept_descent_theorem",
            "decision": "accept quotient/basic-coframe descent as the exact route",
            "reason": "regular quotient plus basic coframe gives Obs_e and DObs_e[Dq(v)]=0 by standard descent",
            "consequence": "the local frame-zero problem becomes parent ownership of V/q/e_parent",
            "status": "CONDITIONAL_DESCENT_THEOREM_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2391_1_reject_tautological_q",
            "decision": "reject q=(e_obs,...) as sufficient by itself",
            "reason": "including e_obs in q can hide the desired conclusion unless the kernel is independently null and matter-invisible",
            "consequence": "projection-by-declaration becomes an explicit guard row",
            "status": "ANTI_TAUTOLOGY_GUARD_REQUIRED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2391_2_owned_branch_conditional",
            "decision": "keep 1963/2048 owned-coframe branches alive but closure-only",
            "reason": "they supply concrete coframe candidates, but not canonical q/Obs_e ownership or all-sector descent",
            "consequence": "coframe branch is promising but not promoted to local GR",
            "status": "OWNED_COFRAME_BRANCH_RETAINED_CONDITIONAL",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2391_3_next",
            "decision": "attack vertical distribution nullness next",
            "reason": "without a parent-null/matter-invisible kernel, no q/Obs_e quotient construction is claim-grade",
            "consequence": "2392 should prove V=ker(Dq) is presymplectic-null and matter-invisible, or fill kernel-charge/source rows",
            "status": "SELECT_2392_VERTICAL_KERNEL_NULLNESS",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2391_0_descent_shape",
            "gate": "quotient/basic-coframe descent theorem shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "use as route; not evidence of current-MTS closure",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2391_1_parent_vertical_distribution",
            "gate": "parent vertical distribution and regular quotient",
            "gate_status": "FAIL",
            "claim_effect": "q ownership not claim-grade",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2391_2_basic_coframe",
            "gate": "Lie_v e_parent=0 for all vertical v",
            "gate_status": "FAIL",
            "claim_effect": "Obs_e descent not promoted",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2391_3_kernel_nullness",
            "gate": "presymplectic-null/matter-invisible kernel",
            "gate_status": "FAIL",
            "claim_effect": "projection-by-declaration guard remains active",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2391_4_no_shadow_all_sector",
            "gate": "no shadow frame and all-sector descent",
            "gate_status": "FAIL",
            "claim_effect": "frame/readout residuals remain live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2391_5_GR_Newton",
            "gate": "local GR/Newton from q/Obs_e",
            "gate_status": "BLOCKED",
            "claim_effect": "no GR/Newton reduction claim from 2391",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2391_0_claim_q_Obs_e",
            "claim": "parent q/Obs_e functor is constructed for current MTS",
            "allowed": "false",
            "reason": "V, quotient regularity, basic coframe, null kernel, no-shadow, all-sector descent, and M_H_ref are unsigned",
            "blocking_rows": "QOC2391_0_parent_vertical_distribution;QOC2391_1_regular_integrable_quotient;QOC2391_3_basic_coframe;QOC2391_7_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2391_1_tautological_projection",
            "claim": "q_candidate containing e_obs proves Obs_e descent",
            "allowed": "false",
            "reason": "that is projection-by-declaration unless ker(Dq_candidate) is independently null and matter-invisible",
            "blocking_rows": "QOC2391_2_presymplectic_null;QOC2391_4_no_projection_declaration",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": "MTS_R2FR_PARENT_Q_OBS_E_FUNCTOR_CONSTRUCTION_OR_FRAME_LEAK_SOURCE_PACK_2391",
            "row_id": "REF2391_2_claim_shadow_zero",
            "claim": "shadow-frame/readout residuals vanish",
            "allowed": "false",
            "reason": "Weyl/disformal/source-prefactor/readout tails are retained unless zeroed by parent theorem or bounded",
            "blocking_rows": "QOC2391_5_no_shadow_frame;QOC2391_6_matter_readout_descent;QEL2391_5_shadow_frame;QEL2391_6_all_sector_descent",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2391_3_claim_GR_Newton",
            "claim": "local GR/Newton follows from q/Obs_e shape",
            "allowed": "false",
            "reason": "q/Obs_e descent is necessary but not sufficient; EH exterior, source charge, M_H_ref, Poisson/Gauss, PPN, and boundary locks remain required",
            "blocking_rows": "CG2391_5_GR_Newton;QOC2391_7_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2391_0_selected",
            "next_file": "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
            "success_condition": "prove V=ker(Dq) is parent presymplectic-null, matter-invisible, and zero compact-flux so q/Obs_e is not projection-by-declaration",
            "fallback_condition": "fill epsilon_kernel_charge, epsilon_q_rank_or_integrability, and epsilon_projection_declaration rows with source paths and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2391_1_parallel",
            "next_file": "2392b-Y5-R2FR-basic-coframe-Lie-v-zero-or-DObs-e-operator-bound.md",
            "success_condition": "prove Lie_v e_parent=0 for every retained local vertical vector",
            "fallback_condition": "source epsilon_DObs_e operator/source-weight rows",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2391_2_parallel",
            "next_file": "2392c-Y5-R2FR-no-shadow-frame-and-all-sector-descent-or-residual-pack.md",
            "success_condition": "derive no Weyl/disformal/source-prefactor/readout-tail slots outside q/Obs_e",
            "fallback_condition": "source finite b_g, b_dis, b_A, q_nonH, alpha_readout and Delta_W_support bounds",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2391_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_FUNCTOR_THEOREM.csv": functor_theorem_rows,
    "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_LEAK_VALUES.csv": leak_rows,
    "P8_Y5_PARENT_QLOC_2391_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2391_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2391_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2391_NEXT_TARGET.csv": next_target_rows,
}


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                return False
    return True


def validation_rows() -> list[dict[str, object]]:
    csv_paths = [RESIDUALS / name for name in CSV_BUILDERS]
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": no_claim(),
            }
        )

    sources = source_register()
    add("VAL2391_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2391_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = functor_theorem_rows()
    add(
        "VAL2391_02_quotient_theorem_present",
        any("Q_vis := Phi_parent/V" in row["statement"] for row in theorem),
        "quotient existence theorem is present",
    )
    add(
        "VAL2391_03_basic_coframe_present",
        any("e_parent = Obs_e o q" in row["statement"] for row in theorem),
        "basic coframe descent theorem is present",
    )
    add(
        "VAL2391_04_tautology_guard_present",
        any("projection-by-declaration" in row["statement"] for row in theorem),
        "projection-by-declaration guard is present",
    )
    certs = certificate_rows()
    add(
        "VAL2391_05_required_gaps_explicit",
        all("MISSING" in row["status"] for row in certs),
        "vertical/quotient/null/basic/no-shadow/descent/MHref gaps explicit",
    )
    values = leak_rows()
    add(
        "VAL2391_06_value_rows_nonready",
        all(
            row["score_ready"] == "false"
            and (("MISSING" in row["current_value"]) or row["current_value"] == "COMPONENTS_MISSING")
            for row in values
        ),
        "q/Obs_e leak rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2391_07_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2391_0_descent_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2391_08_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths),
        "generated CSVs parse and have rows",
    )
    add("VAL2391_09_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2391_10_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2391_11_next_selected",
        any(row["row_id"] == "NEXT2391_0_selected" for row in next_target_rows()),
        "vertical kernel nullness selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2391_OVERALL",
        overall,
        "2391 states the exact q/Obs_e quotient-basic descent contract, rejects tautological q, refuses promotion without parent-null/matter-invisible kernel, and selects vertical kernel nullness next",
    )
    return rows


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_FUNCTOR_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_LEAK_VALUES.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2391_VALIDATION.csv")

    body = f"""# 2391 - parent q Obs_e functor construction or frame leak source pack

## Result

2391 turns the `q/Obs_e` problem into an exact descent contract.

The clean theorem is:

1. Define a parent vertical distribution `V` of locally unobserved/residual directions.
2. If `V` is regular, involutive, and integrates to a good local quotient, then
   `Q_vis := Phi_parent/V` and `q: Phi_parent -> Q_vis`.
3. If the parent coframe candidate is basic over that quotient,
   `Lie_v e_parent = 0` for every `v in V`, then there is a unique functor `Obs_e` with
   `e_parent = Obs_e o q`.
4. Then `DObs_e[Dq(v)] = 0` and the 2390 same-frame coframe-zero theorem activates conditionally.

That is the good news: the route is mathematically clean.

The bad-news guard is equally important: `q_candidate=(e_obs,...)` with `Obs_e(q_candidate)=e_obs` is not enough.
That can be projection-by-declaration unless `ker(Dq_candidate)` is independently proven presymplectic-null,
matter-invisible, no-marker, and no-shadow-frame.

Current MTS has candidate coframe branches, including the owned-coframe and motion-load constructions, but it has not
signed the parent vertical distribution, regular quotient, basic coframe, null kernel, no-shadow frame, all-sector
descent, or positive same-frame `M_H_ref`.

No parent `q/Obs_e` pass, same-frame pass, `J_H` pass, `W_source` pass, local-GR pass, Newton pass, PPN, clock,
orbital, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## q/Obs_e Functor Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "derivation_status", "current_gain", "remaining_gap", "valid_for_claim"])}

## q/Obs_e Certificate

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## q/Obs_e Leak Values

{markdown_table(values, ["row_id", "quantity", "formula", "units", "current_value", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is progress, not circling.  The exact next lock is not more coframe language; it is whether the vertical kernel
used to form `q` is genuinely parent-null and matter-invisible.  If that closes, `q/Obs_e` stops being a slogan.  If it
does not, the honest output is a kernel-charge/source leak row.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2391_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2391_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
