from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_OBSERVED_COFRAME_PULLBACK_SAME_FRAME_LOCK_OR_FRAME_SOURCE_LEAK_VALUES_2390"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md"
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
            "row_id": "SRC2390_00_2389_doc",
            "source_key": "2389_same_frame_handoff",
            "source_path": POST_ROOT / "2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md",
            "needles": ["2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md", "e_obs(q(Phi))", "Delta_frame_source_over_MH"],
            "source_role": "2389 selects observed coframe pullback and same-frame tau lock",
        },
        {
            "row_id": "SRC2390_01_2389_certificates",
            "source_key": "2389_current_owner_certificates",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv",
            "needles": ["OCC2389_1_eobs_pullback", "MISSING_EOBS_PULLBACK_AND_SAME_FRAME_LOCK", "OCC2389_3_tau_owner"],
            "source_role": "q/e_obs/tau ownership gaps",
        },
        {
            "row_id": "SRC2390_02_2389_leaks",
            "source_key": "2389_jh_owner_leaks",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2389_JH_OWNER_LEAK_VALUES.csv",
            "needles": ["Delta_frame_source_over_MH", "epsilon_q_owner", "epsilon_tau_selector"],
            "source_role": "frame/source leak quantities to refine",
        },
        {
            "row_id": "SRC2390_03_684_doc",
            "source_key": "684_tau_coframe_lock",
            "source_path": POST_ROOT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
            "needles": ["e_source = e_clock = e_photon = e_ruler = e_orbit = e_obs", "tau_source = tau_charge = tau_clock = tau_orbit = tau_obs[e_obs]", "has not parent-signed it"],
            "source_role": "same observed coframe/tau contract and nonclaim status",
        },
        {
            "row_id": "SRC2390_04_same_coframe_clause",
            "source_key": "same_coframe_parent_clause",
            "source_path": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
            "needles": ["UOC519_2_readout_uses_same_e", "UOC519_3_source_current_definition", "UOC519_5_no_conformal_disformal_shadow_frame"],
            "source_role": "machine same-coframe clauses",
        },
        {
            "row_id": "SRC2390_05_tau_contract",
            "source_key": "685_tau_generator_contract",
            "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "needles": ["TGC685_0_define_tau_obs", "TGC685_5_orbit_readout_route", "TGC685_6_verdict"],
            "source_role": "one tau for source, clock, orbit, charge, and boundary",
        },
        {
            "row_id": "SRC2390_06_943_doc",
            "source_key": "943_single_observed_coframe",
            "source_path": POST_ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "needles": ["e_obs(Phi) = Obs_e(q(Phi))", "Lie_v e_obs = D Obs_e[Dq(v)] = 0", "does **not** parent-sign that descent"],
            "source_role": "single observed coframe matter-coupling contract",
        },
        {
            "row_id": "SRC2390_07_944_doc",
            "source_key": "944_quotient_coframe_descent",
            "source_path": POST_ROOT / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            "needles": ["e_obs(Phi)=Obs_e(q(Phi))", "Lie_v e_obs = DObs_e[Dq(v)] = 0", "does **not** prove the current MTS parent"],
            "source_role": "chain-rule quotient coframe descent proof and missing parent construction",
        },
        {
            "row_id": "SRC2390_08_1738_doc",
            "source_key": "1738_coframe_kernel",
            "source_path": POST_ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
            "needles": ["chain-rule coframe-kernel theorem is exact", "single universal coframe is not enough", "b_g=0"],
            "source_role": "coframe kernel theorem plus shadow-frame warning",
        },
        {
            "row_id": "SRC2390_09_1739_doc",
            "source_key": "1739_parent_coframe_ownership",
            "source_path": POST_ROOT / "1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md",
            "needles": ["e_obs=E(Q_vis)", "`b_g=0` by the chain rule", "MISSING_PARENT_COFRAME_OWNERSHIP"],
            "source_role": "parent coframe ownership stack and common-frame derivative row",
        },
        {
            "row_id": "SRC2390_10_1879_doc",
            "source_key": "1879_common_frame_leak",
            "source_path": POST_ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
            "needles": ["e_obs = E(Q_vis)", "D_C_R e_obs = 0", "hidden universal Weyl/disformal/source-prefactor slot"],
            "source_role": "finite common-frame leak residual stack",
        },
        {
            "row_id": "SRC2390_11_2323_doc",
            "source_key": "2323_common_matter_frame",
            "source_path": POST_ROOT / "2323-Y5-R2FR-common-matter-frame-action-signature-or-readout-tail-row.md",
            "needles": ["ordinary matter frame `e_obs(q(Phi))`", "source/readout projector", "`alpha_readout=0`"],
            "source_role": "readout-tail theorem for PPN common matter frame",
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


def same_frame_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFL2390_0_pullback_definition",
            "step": "observed coframe pullback",
            "statement": "Define the local observed coframe by e_obs(Phi) := Obs_e(q(Phi)), where q is parent-owned and Obs_e is fixed before any source, PPN, orbital, clock, or R10 readout.",
            "derivation_status": "CONDITIONAL_PULLBACK_DEFINITION",
            "current_gain": "turns the public metric/coframe into a parent functor rather than a representative-frame convention",
            "remaining_gap": "parent q and Obs_e functor are not constructed for current MTS",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFL2390_1_vertical_kernel",
            "step": "coframe kernel zero",
            "statement": "For vertical v in ker(Dq), Lie_v e_obs = DObs_e[Dq(v)] = 0. Therefore a true quotient coframe cannot carry local representative-frame force.",
            "derivation_status": "CONDITIONAL_CHAIN_RULE_THEOREM",
            "current_gain": "this is a real derivation route for frame silence, not an assumption",
            "remaining_gap": "kernel membership and parent q/Obs_e ownership remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFL2390_2_same_readout_functor",
            "step": "single readout functor",
            "statement": "Require e_source = e_clock = e_photon = e_ruler = e_orbit = e_obs, so matter stress, clock rates, rods, lightcones, and slow-orbit readout use the same coframe.",
            "derivation_status": "CONDITIONAL_SAME_FRAME_CONTRACT",
            "current_gain": "blocks a patchwork where source mass and observations use different metrics",
            "remaining_gap": "readout projector/support descent and clock/rod/photon/orbit functors are not parent-signed together",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFL2390_3_tau_lock",
            "step": "same-frame tau lock",
            "statement": "Require tau_source = tau_charge = tau_clock = tau_orbit = tau_boundary = tau_obs[e_obs], with tau selected before readout by stationary/asymptotic/clock-normalization data.",
            "derivation_status": "CONDITIONAL_TAU_IDENTITY",
            "current_gain": "prevents borrowing a convenient Hamiltonian tau for mass and a different clock/orbit tau for tests",
            "remaining_gap": "stationary generator, Hamiltonian integrability, and clock normalization are not parent-signed as one object",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFL2390_4_no_shadow_frame",
            "step": "no shadow frame theorem",
            "statement": "A single public coframe is insufficient if e_obs has hidden Weyl, disformal, species, source-prefactor, non-Hilbert-current, or support-retune dependence on residual fields.",
            "derivation_status": "OBSTRUCTION_RETAINED",
            "current_gain": "separates true coframe ownership from a universal but physical fifth-force frame",
            "remaining_gap": "b_g, b_dis, b_A, q_nonH, Delta_tau_n, Delta_W_support, and alpha_readout are not zeroed or bounded",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFL2390_5_MHref_link",
            "step": "same-frame denominator link",
            "statement": "M_H_ref must be derived from H_tau[S_link]-H_ref in the same e_obs/tau branch; importing orbital GM as the denominator would be circular.",
            "derivation_status": "ANTI_CIRCULARITY_GUARD",
            "current_gain": "keeps the GR/Newton source normalization from proving itself with its own readout",
            "remaining_gap": "positive same-frame M_H_ref remains missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFL2390_6_verdict",
            "step": "current verdict",
            "statement": "The same-frame theorem is sharp: parent q and Obs_e plus a single tau/readout functor would make the local frame branch much cleaner. Current MTS has not signed the full stack.",
            "derivation_status": "ROUTE_SHARPENED_NOT_CLAIMED",
            "current_gain": "the next bottleneck is parent construction of q/Obs_e, not a vague frame preference problem",
            "remaining_gap": "all frame/source leak rows remain nonclaim",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_0_parent_q",
            "certificate": "parent q map",
            "required_test": "q: Phi_parent -> Q_vis is explicitly constructed before local readout, with Dq(v)=0 for the local vertical directions",
            "status": "MISSING_PARENT_Q_MAP",
            "residual_if_missing": "epsilon_q_owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_1_Obs_e",
            "certificate": "observed coframe functor Obs_e",
            "required_test": "e_obs(Phi)=Obs_e(q(Phi)) is a parent-owned map, not a chosen representative frame",
            "status": "MISSING_PARENT_OBS_E_FUNCTOR",
            "residual_if_missing": "epsilon_DObs_e",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_2_same_readout",
            "certificate": "source/clock/rod/photon/orbit same-frame readout",
            "required_test": "all matter, clock, rod, photon/lightcone, orbit, source-current, and boundary-charge functionals use the same e_obs",
            "status": "MISSING_ALL_SECTOR_SAME_FRAME_SIGNATURE",
            "residual_if_missing": "Delta_frame_source_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_3_tau_lock",
            "certificate": "parent tau identity",
            "required_test": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs[e_obs] before readout",
            "status": "MISSING_PARENT_TAU_IDENTITY",
            "residual_if_missing": "epsilon_tau_selector",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_4_no_shadow_frame",
            "certificate": "no Weyl/disformal/species/source shadow frame",
            "required_test": "no A(X), B(X), species-frame, source-prefactor, non-Hilbert-current, or support-retune dependence remains outside q/e_obs",
            "status": "MISSING_NO_SHADOW_FRAME_THEOREM",
            "residual_if_missing": "epsilon_shadow_frame",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_5_projector_support",
            "certificate": "projector/support descent",
            "required_test": "source worldtube, PPN projector, orbital GM map, and boundary surfaces descend through the same q/e_obs data before scoring",
            "status": "MISSING_PROJECTOR_SUPPORT_DESCENT",
            "residual_if_missing": "alpha_readout_or_Delta_W_support",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_6_no_retune",
            "certificate": "no readout retuning",
            "required_test": "coframe/tau/projector/support choices are fixed before residual fitting and are not retuned per dataset",
            "status": "MISSING_NO_READOUT_RETUNE_PROOF",
            "residual_if_missing": "epsilon_readout_retune",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2390_7_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "derive H_tau[S_link]-H_ref with the same e_obs/tau/source branch, positive and noncircular",
            "status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "all normalized frame rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


def leak_value_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_0_q_owner",
            "quantity": "epsilon_q_owner",
            "formula": "abs(integral_S (J_H[q_candidate]-J_H[q_parent]))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_Q_MAP;MISSING_JH_DENSITY;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_1_DObs_e",
            "quantity": "epsilon_DObs_e",
            "formula": "||DObs_e[Dq(v)]||_source_weighted / ||e_obs||",
            "units": "dimensionless frame response",
            "current_value": "MISSING_PARENT_OBS_E_FUNCTOR;MISSING_DQ_VERTICAL_BASIS;MISSING_SOURCE_WEIGHT",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_2_frame_source",
            "quantity": "Delta_frame_source_over_MH",
            "formula": "abs(integral_S (T_a[e_source]-T_a[e_obs]) tau^a)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_SOURCE_FRAME_MAP;MISSING_SAME_FRAME_LOCK;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_3_tau_selector",
            "quantity": "epsilon_tau_selector",
            "formula": "abs(integral_S T_a (tau_role^a - tau_obs^a))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_TAU_IDENTITY;MISSING_TA_DENSITY;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_4_shadow_frame",
            "quantity": "epsilon_shadow_frame",
            "formula": "abs(b_g)+abs(b_dis)+abs(b_A)+abs(q_nonH)",
            "units": "dimensionless leading frame-coupling envelope",
            "current_value": "MISSING_BG;MISSING_BDIS;MISSING_BA;MISSING_Q_NONH;MISSING_SOURCE_PATHS",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_5_readout_tail",
            "quantity": "alpha_readout_or_Delta_W_support",
            "formula": "abs(projector_readout_tail)+abs(Delta_W_support)+abs(Delta_tau_n)",
            "units": "dimensionless PPN/source-readout tail envelope",
            "current_value": "MISSING_PROJECTOR_DESCENT;MISSING_SUPPORT_DESCENT;MISSING_TAU_NORMALIZATION",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_6_retune",
            "quantity": "epsilon_readout_retune",
            "formula": "abs(partial_readout e_obs * Delta_readout_choice) + abs(partial_readout tau * Delta_readout_choice)",
            "units": "dimensionless",
            "current_value": "MISSING_NO_RETUNE_PROOF;MISSING_READOUT_CHOICE_BOUND;MISSING_SOURCE_PATHS",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLV2390_7_total",
            "quantity": "Delta_same_frame_total_over_MH",
            "formula": "epsilon_q_owner + epsilon_DObs_e + Delta_frame_source_over_MH + epsilon_tau_selector + epsilon_shadow_frame + alpha_readout_or_Delta_W_support + epsilon_readout_retune",
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
            "row_id": "DEC2390_0_accept_kernel_route",
            "decision": "accept quotient coframe pullback as the clean same-frame route",
            "reason": "e_obs=Obs_e(q(Phi)) and Dq(v)=0 give Lie_v e_obs=0 by chain rule",
            "consequence": "frame silence becomes derivable if q/Obs_e are parent-owned",
            "status": "CONDITIONAL_COFRAME_KERNEL_ROUTE_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2390_1_no_single_frame_shortcut",
            "decision": "reject one-frame wording as sufficient",
            "reason": "a universal but hidden Weyl/disformal/source-prefactor frame can be one public frame and still physically active",
            "consequence": "shadow-frame rows remain live until theorem-zeroed or bounded",
            "status": "NO_SHADOW_FRAME_REQUIRED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2390_2_no_promotion",
            "decision": "do not promote same-frame lock for current MTS",
            "reason": "parent q, Obs_e, all-sector readout, tau identity, no-shadow-frame, projector/support descent, no-retune and M_H_ref are unsigned",
            "consequence": "J_H/W_source/local-GR/Newton/PPN/clock/orbital/R10 claims remain blocked",
            "status": "SAME_FRAME_LOCK_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2390_3_next",
            "decision": "construct parent q/Obs_e functor next",
            "reason": "without q and Obs_e, the rest of the same-frame chain has no parent object to descend through",
            "consequence": "2391 should derive q/Obs_e or fill epsilon_q_owner and epsilon_DObs_e source rows",
            "status": "SELECT_2391_PARENT_Q_OBS_E_FUNCTOR",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2390_0_chain_rule_shape",
            "gate": "coframe pullback chain-rule zero shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "use as derivation route, not claim evidence",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2390_1_parent_q_Obs_e",
            "gate": "parent q/Obs_e ownership",
            "gate_status": "FAIL",
            "claim_effect": "same-frame theorem not promoted",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2390_2_tau_identity",
            "gate": "same tau for source/charge/clock/orbit/boundary",
            "gate_status": "FAIL",
            "claim_effect": "tau leak remains open",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2390_3_no_shadow_frame",
            "gate": "no hidden Weyl/disformal/species/source frame",
            "gate_status": "FAIL",
            "claim_effect": "common-frame residual remains live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2390_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "normalized frame rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2390_5_GR_Newton",
            "gate": "local GR/Newton same-frame source normalization",
            "gate_status": "BLOCKED",
            "claim_effect": "no GR/Newton reduction claim from 2390",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2390_0_claim_same_frame",
            "claim": "same observed coframe/tau lock is parent-derived for current MTS",
            "allowed": "false",
            "reason": "q, Obs_e, all-sector readout functors, tau identity, no-shadow-frame, and M_H_ref are unsigned",
            "blocking_rows": "SFC2390_0_parent_q;SFC2390_1_Obs_e;SFC2390_2_same_readout;SFC2390_3_tau_lock;SFC2390_7_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2390_1_single_frame_enough",
            "claim": "one public coframe alone removes frame forces",
            "allowed": "false",
            "reason": "one coframe can still contain hidden Weyl/disformal/species/source prefactor dependence",
            "blocking_rows": "SFC2390_4_no_shadow_frame;FLV2390_4_shadow_frame",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2390_2_claim_readout_tail_zero",
            "claim": "clock/orbit/PPN/readout tails vanish",
            "allowed": "false",
            "reason": "projector/support descent and no-retune are not parent-signed",
            "blocking_rows": "SFC2390_5_projector_support;SFC2390_6_no_retune;FLV2390_5_readout_tail",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2390_3_claim_GR_Newton",
            "claim": "local GR/Newton reduction follows from same-frame shape",
            "allowed": "false",
            "reason": "the same-frame route is necessary but not sufficient; EH exterior fixed point, Hamiltonian charge, M_H_ref, Poisson/Gauss, and PPN closure remain required",
            "blocking_rows": "CG2390_5_GR_Newton;SFC2390_7_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2390_0_selected",
            "next_file": "2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md",
            "success_condition": "construct parent q and Obs_e so e_obs(Phi)=Obs_e(q(Phi)) is owned before readout and Dq(v)=0 implies Lie_v e_obs=0",
            "fallback_condition": "fill epsilon_q_owner and epsilon_DObs_e rows with source paths, units, operator norms, and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2390_1_parallel",
            "next_file": "2391b-Y5-R2FR-no-shadow-frame-zero-or-bg-bdis-bA-bound-values.md",
            "success_condition": "derive b_g=b_dis=b_A=q_nonH=0 from the parent action or no-slot grammar",
            "fallback_condition": "source finite common-frame residual bounds for PPN/WEP/clock/R10 projection",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2390_2_parallel",
            "next_file": "2391c-Y5-R2FR-parent-tau-identity-stationary-clock-Hamiltonian-or-tau-leak-row.md",
            "success_condition": "derive tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary from one parent observed generator",
            "fallback_condition": "fill epsilon_tau_selector and Delta_tau_n nonclaim rows",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2390_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_THEOREM.csv": same_frame_theorem_rows,
    "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2390_FRAME_SOURCE_LEAK_VALUES.csv": leak_value_rows,
    "P8_Y5_PARENT_QLOC_2390_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2390_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2390_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2390_NEXT_TARGET.csv": next_target_rows,
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
    add("VAL2390_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2390_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = same_frame_theorem_rows()
    add(
        "VAL2390_02_pullback_definition_present",
        any("e_obs(Phi) := Obs_e(q(Phi))" in row["statement"] for row in theorem),
        "observed coframe pullback definition is present",
    )
    add(
        "VAL2390_03_vertical_kernel_present",
        any("Lie_v e_obs = DObs_e[Dq(v)] = 0" in row["statement"] for row in theorem),
        "vertical coframe-kernel zero theorem shape is present",
    )
    certs = certificate_rows()
    add(
        "VAL2390_04_required_gaps_explicit",
        all("MISSING" in row["status"] for row in certs),
        "q/Obs_e/readout/tau/no-shadow/projector/no-retune/MHref gaps explicit",
    )
    values = leak_value_rows()
    add(
        "VAL2390_05_value_rows_nonready",
        all(
            row["score_ready"] == "false"
            and (("MISSING" in row["current_value"]) or row["current_value"] == "COMPONENTS_MISSING")
            for row in values
        ),
        "frame/source leak rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2390_06_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2390_0_chain_rule_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2390_07_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths),
        "generated CSVs parse and have rows",
    )
    add("VAL2390_08_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2390_09_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2390_10_next_selected",
        any(row["row_id"] == "NEXT2390_0_selected" for row in next_target_rows()),
        "parent q/Obs_e functor construction selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2390_OVERALL",
        overall,
        "2390 derives conditional observed-coframe pullback/same-frame route, refuses promotion without q/Obs_e/tau/no-shadow/MHref, and selects parent q/Obs_e functor next",
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
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_FRAME_SOURCE_LEAK_VALUES.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2390_VALIDATION.csv")

    body = f"""# 2390 - observed coframe pullback same-frame lock or frame-source leak values

## Result

2390 attacks the same-frame lock needed before the MTS local branch can seriously claim a GR/Newton reduction.

The clean route is:

`e_obs(Phi) := Obs_e(q(Phi))`.

Then for every vertical variation `v in ker(Dq)`:

`Lie_v e_obs = DObs_e[Dq(v)] = 0`.

That is a real derivation route. If matter, clocks, rods, photons/lightcones, orbital readout, Hilbert source charge,
Hamiltonian charge, and boundary reference all use this same `e_obs` plus one parent `tau_obs[e_obs]`, then frame
leakage can be killed by parent ownership rather than tuning.

But a single public coframe is not enough by itself. A hidden Weyl/disformal/species/source-prefactor slot can be
universal and still physically active. Therefore 2390 keeps `b_g`, `b_dis`, `b_A`, `q_nonH`, `Delta_tau_n`,
`Delta_W_support`, `alpha_readout`, and same-frame denominator gaps live unless the parent action theorem-zeros them.

Current MTS does not yet sign parent `q`, `Obs_e`, all-sector readout functors, same `tau`, no-shadow-frame,
projector/support descent, no-retune, or positive same-frame `M_H_ref`. No same-frame pass, `J_H` pass, `W_source`
pass, local-GR pass, Newton pass, PPN, clock, orbital, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Same Frame Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "derivation_status", "current_gain", "remaining_gap", "valid_for_claim"])}

## Same Frame Certificate

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## Frame Source Leak Values

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

This is a good narrowing. The coframe route is not hand-wavy: if `q` and `Obs_e` are parent-owned, the frame-zero
statement is a chain-rule theorem. The next honest lock is therefore `2391`: build the parent `q/Obs_e` functor or
turn `epsilon_q_owner` and `epsilon_DObs_e` into sourced finite rows.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2390_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2390_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
