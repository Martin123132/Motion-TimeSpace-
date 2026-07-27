from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PARENT_MATTER_ACTION_CURRENT_DENSITY_OR_JH_OWNER_LEAK_VALUES_2389"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md"
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
            "row_id": "SRC2389_00_2388_doc",
            "source_key": "2388_current_density_handoff",
            "source_path": POST_ROOT / "2388-Y5-R2FR-parent-Hilbert-current-worldtube-support-or-selector-leak-values.md",
            "needles": ["2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md", "derive T_a and J_H[tau]"],
            "source_role": "2388 selects parent matter-action current density as next lock",
        },
        {
            "row_id": "SRC2389_01_2388_certificates",
            "source_key": "2388_worldtube_support_certificate",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv",
            "needles": ["WSC2388_0_parent_Lm", "MISSING_PARENT_MATTER_LAGRANGIAN", "WSC2388_1_same_frame"],
            "source_role": "explicit parent Lm and same-frame lock gaps",
        },
        {
            "row_id": "SRC2389_02_2388_leaks",
            "source_key": "2388_selector_leaks",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2388_SELECTOR_LEAK_VALUES.csv",
            "needles": ["epsilon_JH_owner", "Delta_frame_source_over_MH", "MISSING_PARENT_TAU_SELECTOR"],
            "source_role": "owner/frame/tau leak rows to sharpen",
        },
        {
            "row_id": "SRC2389_03_1009_contract_doc",
            "source_key": "1009_parent_action_contract",
            "source_path": POST_ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needles": ["minimum parent-action blocks", "no total parent action is promoted", "local-GR claim is allowed"],
            "source_role": "parent action block contract without promotion",
        },
        {
            "row_id": "SRC2389_04_1756_hidden_source",
            "source_key": "1756_hidden_source_ledger",
            "source_path": POST_ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
            "needles": ["delta_X S_parent = L_X X + J_hidden + gated coupling terms + boundary", "proof not closed"],
            "source_role": "hidden source terms must be excluded or bounded",
        },
        {
            "row_id": "SRC2389_05_1760_matter_descent",
            "source_key": "1760_matter_worldtube_descent",
            "source_path": POST_ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["matter only sees `e_obs(q(Phi))`", "delta_v S_matter=0", "direct/legal possibility"],
            "source_role": "quotient-only matter descent theorem and obstruction",
        },
        {
            "row_id": "SRC2389_06_1016_parent_selector",
            "source_key": "1016_parent_worldtube_contract",
            "source_path": POST_ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "needles": ["S_matter = S_matter[e_obs,psi_m]", "same_frame_measure_not_parent_signed", "contract_only_no_full_current_Lagrangian"],
            "source_role": "same observed coframe and current-Lagrangian gap",
        },
        {
            "row_id": "SRC2389_07_parent_contract_csv",
            "source_key": "parent_action_contract_csv",
            "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "needles": ["PAC537_0_covariant_parent_action", "PAC537_1_single_observed_source_frame", "PAC537_7_extra_sector_mass_charge_silence"],
            "source_role": "parent action clauses for matter/current ownership",
        },
        {
            "row_id": "SRC2389_08_2183_selector",
            "source_key": "2183_worldtube_hilbert_selector",
            "source_path": POST_ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
            "needles": ["delta S_matter/delta e_obs", "source worldtube is selected before readout"],
            "source_role": "Hilbert source selector depends on matter variation",
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


def current_density_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCD2389_0_action_grammar",
            "step": "observed-frame matter action grammar",
            "statement": "Use S_m[Phi,psi_m] := integral_M L_m(e_obs(q(Phi)), psi_m, D_omega_obs(q(Phi)) psi_m; c_i), with no independent X, rho_A, W_source, C_top, fitted radius, or readout-mask slot.",
            "derivation_status": "CONDITIONAL_GR_COMPATIBLE_GRAMMAR",
            "current_gain": "identifies the only low-scrutiny way for MTS matter to share the GR source current",
            "remaining_gap": "q(Phi), e_obs(q), omega_obs(q), constants c_i, and no-extra-slot rule are not parent-signed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCD2389_1_coframe_variation",
            "step": "Hilbert density from observed coframe",
            "statement": "Varying e_obs gives delta L_m = E_m delta psi_m + T_a wedge delta e_obs^a + dTheta_m, so T_a := delta L_m/delta e_obs^a is the parent matter current density once e_obs(q) is owned.",
            "derivation_status": "CONDITIONAL_VARIATIONAL_IDENTITY",
            "current_gain": "J_H no longer needs an ad hoc source density if the parent owns e_obs(q)",
            "remaining_gap": "no signed MTS matter Lagrangian or observed coframe pullback yet",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCD2389_2_tau_current",
            "step": "Hilbert source current",
            "statement": "For parent-fixed tau, define J_H[tau] := -tau^a T_a and W_source := closure(supp J_H[tau]); this is pre-readout if tau and e_obs are selected by parent boundary/asymptotic data.",
            "derivation_status": "CONDITIONAL_CURRENT_DENSITY",
            "current_gain": "the current used for worldtube support is now tied to the same observed matter sector",
            "remaining_gap": "tau selector and same-frame source/readout lock remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCD2389_3_vertical_descent_zero",
            "step": "vertical hidden-source exclusion",
            "statement": "For v in ker(Dq), if matter fields are lifted/fixed over q and no direct source slots exist, then delta_v S_m = integral (delta S_m/delta e_obs) D(e_obs o q)[v] + matter-lift terms = 0.",
            "derivation_status": "CONDITIONAL_CHAIN_RULE_ZERO",
            "current_gain": "kills J_hidden and direct matter/worldtube X-source terms by derivation rather than by small fitted numbers",
            "remaining_gap": "matter lift, no-marker grammar, and no direct V_m[X,rho_A,W_source] exclusion remain contract-only",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCD2389_4_no_extra_mass_channel",
            "step": "extra-sector mass-charge silence",
            "statement": "If all motion/time/memory/domain fields enter matter only through e_obs(q), then their local mass charge contribution is mediated by T_a; there is no separate local source current for them.",
            "derivation_status": "CONDITIONAL_NO_EXTRA_CHANNEL",
            "current_gain": "protects the local Newton/GR source normalization from a second hidden mass source",
            "remaining_gap": "extra-sector silence is not proven by a full parent action",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCD2389_5_verdict",
            "step": "current verdict",
            "statement": "The matter-current density route is mathematically clean: quotient-only observed-frame matter gives the right J_H. Current MTS has not yet parent-signed the quotient map, observed coframe, tau, constants, matter lift, or no-extra-slot clauses.",
            "derivation_status": "ROUTE_SHARPENED_NOT_CLAIMED",
            "current_gain": "the coupling bottleneck is now a finite list of parent-action clauses",
            "remaining_gap": "ownership certificates and leak values remain nonclaim",
            "valid_for_claim": no_claim(),
        },
    ]


def owner_certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_0_q_map",
            "certificate": "parent quotient map q",
            "required_test": "q(Phi) is explicitly defined and Dq(v)=0 characterizes vertical directions used in the local branch",
            "status": "MISSING_PARENT_Q_MAP_SIGNATURE",
            "residual_if_missing": "epsilon_q_owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_1_eobs_pullback",
            "certificate": "observed coframe pullback e_obs(q)",
            "required_test": "matter, clocks, rods, source charge, and orbital readout all use one e_obs derived from q(Phi)",
            "status": "MISSING_EOBS_PULLBACK_AND_SAME_FRAME_LOCK",
            "residual_if_missing": "Delta_frame_source_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_2_Lm_density",
            "certificate": "explicit matter Lagrangian density",
            "required_test": "L_m(e_obs,psi_m,Dpsi_m;c_i) is written and varied to produce T_a before readout",
            "status": "MISSING_EXPLICIT_LM_DENSITY",
            "residual_if_missing": "epsilon_JH_owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_3_tau_owner",
            "certificate": "parent-fixed tau",
            "required_test": "tau is selected by parent boundary/asymptotic data in the same observed frame and not by residual fitting",
            "status": "MISSING_PARENT_TAU_SELECTOR",
            "residual_if_missing": "epsilon_tau_selector",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_4_matter_lift",
            "certificate": "matter lift/fixed representation data",
            "required_test": "vertical variations v in ker(Dq) do not independently move psi_m, constants, material labels, or representation data",
            "status": "MISSING_MATTER_LIFT_NO_MARKER_PROOF",
            "residual_if_missing": "epsilon_marker_matter_lift",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_5_no_direct_slots",
            "certificate": "no direct source/worldtube slots",
            "required_test": "forbid V_m[X,rho_A,W_source,C_top] and any source prefactor outside q/e_obs",
            "status": "MISSING_NO_DIRECT_SLOT_GRAMMAR",
            "residual_if_missing": "epsilon_hidden_source_slot",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_6_support_tail",
            "certificate": "current support/tail rule",
            "required_test": "J_H support is compact/regular or exterior Hilbert tail norm is bounded in the selected local source class",
            "status": "MISSING_SUPPORT_OR_TAIL_THEOREM",
            "residual_if_missing": "epsilon_support_tail",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OCC2389_7_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "derive the denominator from the same J_H/tau/e_obs branch",
            "status": "MISSING_POSITIVE_MHREF",
            "residual_if_missing": "all normalized current rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


def leak_value_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "JLV2389_0_q_owner",
            "quantity": "epsilon_q_owner",
            "formula": "abs(integral_S (J_H[q_candidate]-J_H[q_parent]))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_Q_MAP;MISSING_JH_DENSITY;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JLV2389_1_JH_owner",
            "quantity": "epsilon_JH_owner",
            "formula": "abs(integral_S (J_H_from_contract - J_H_from_parent_Lm))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_EXPLICIT_LM_DENSITY;MISSING_VARIATION;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JLV2389_2_frame_source",
            "quantity": "Delta_frame_source_over_MH",
            "formula": "abs(integral_S (T_a[e_obs_readout]-T_a[e_obs_parent]) tau^a)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_EOBS_PULLBACK;MISSING_SAME_FRAME_LOCK;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JLV2389_3_tau_selector",
            "quantity": "epsilon_tau_selector",
            "formula": "abs(integral_S T_a (tau_candidate^a - tau_parent^a))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_TAU_SELECTOR;MISSING_TA_DENSITY;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JLV2389_4_hidden_slot",
            "quantity": "epsilon_hidden_source_slot",
            "formula": "abs(partial_X V_m[X,rho_A,W_source,C_top]|_{X=0})/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_NO_DIRECT_SLOT_PROOF;MISSING_VM_DENSITY;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JLV2389_5_matter_lift",
            "quantity": "epsilon_marker_matter_lift",
            "formula": "abs(delta_v psi_m contribution + delta_v c_i contribution + material-marker contribution)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_MATTER_LIFT;MISSING_NO_MARKER_PROOF;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JLV2389_6_total",
            "quantity": "Delta_JH_owner_total_over_MH",
            "formula": "epsilon_q_owner + epsilon_JH_owner + Delta_frame_source_over_MH + epsilon_tau_selector + epsilon_hidden_source_slot + epsilon_marker_matter_lift",
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
            "row_id": "DEC2389_0_accept_action_grammar",
            "decision": "accept observed-frame quotient-only matter action as the clean route",
            "reason": "it is the route that makes the MTS source current the same kind of Hilbert current used in GR",
            "consequence": "the local source problem becomes ownership of q/e_obs/tau/no-extra-slots, not a free density fit",
            "status": "CONDITIONAL_MATTER_GRAMMAR_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2389_1_vertical_zero_conditional",
            "decision": "accept vertical hidden-source zero only under quotient-only matter descent",
            "reason": "Dq(v)=0 kills delta_v S_m only if matter and all material labels are pulled back through q/e_obs",
            "consequence": "hidden source terms remain live until no-direct-slot and matter-lift certificates exist",
            "status": "CONDITIONAL_CHAIN_RULE_ZERO_ONLY",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2389_2_no_promotion",
            "decision": "do not promote J_H ownership for current MTS",
            "reason": "explicit q, e_obs(q), L_m, tau, matter lift, no-direct-slot rule, support/tail theorem, and M_H_ref remain unsigned",
            "consequence": "local-GR/Newton/source-normalization claims remain blocked",
            "status": "JH_OWNER_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2389_3_next",
            "decision": "attack observed coframe pullback and same-frame lock next",
            "reason": "without e_obs(q) in one frame, even a standard matter Lagrangian cannot prove the same source current for clocks, rods, orbital readout, and mass charge",
            "consequence": "2390 should derive e_obs(q)/tau same-frame ownership or fill frame-source leak values",
            "status": "SELECT_2390_EOBS_Q_PULLBACK_SAME_FRAME_LOCK",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2389_0_action_grammar_shape",
            "gate": "quotient-only observed-frame matter action shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "use as the low-scrutiny route for current ownership",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2389_1_q_eobs",
            "gate": "parent q and e_obs(q) ownership",
            "gate_status": "FAIL",
            "claim_effect": "J_H remains a placeholder density",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2389_2_Lm_variation",
            "gate": "explicit L_m variation",
            "gate_status": "FAIL",
            "claim_effect": "epsilon_JH_owner not score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2389_3_no_hidden_slots",
            "gate": "no direct X/source/worldtube/material slots",
            "gate_status": "FAIL",
            "claim_effect": "hidden source terms remain live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2389_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "normalized rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2389_5_GR_Newton",
            "gate": "GR/Newton local source-current equality",
            "gate_status": "BLOCKED",
            "claim_effect": "no GR/Newton reduction claim from 2389",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2389_0_claim_JH_owned",
            "claim": "J_H[tau] is parent-owned for current MTS",
            "allowed": "false",
            "reason": "the action grammar is conditional; q, e_obs(q), L_m variation, tau, and matter lift are unsigned",
            "blocking_rows": "OCC2389_0_q_map;OCC2389_1_eobs_pullback;OCC2389_2_Lm_density;OCC2389_3_tau_owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2389_1_claim_hidden_zero",
            "claim": "hidden matter/source couplings vanish",
            "allowed": "false",
            "reason": "vertical descent only kills them if there are no direct source/worldtube/material-marker slots",
            "blocking_rows": "OCC2389_4_matter_lift;OCC2389_5_no_direct_slots;JLV2389_4_hidden_slot",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2389_2_claim_same_frame",
            "claim": "the same source current controls clocks, rods, orbital readout, and local mass charge",
            "allowed": "false",
            "reason": "same-frame e_obs/tau lock is not parent-derived",
            "blocking_rows": "OCC2389_1_eobs_pullback;OCC2389_3_tau_owner;JLV2389_2_frame_source",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2389_3_claim_GR_Newton",
            "claim": "local GR/Newton reduction follows",
            "allowed": "false",
            "reason": "source current ownership alone is not enough; EH exterior fixed point, Hamiltonian charge, PPN closure, and M_H_ref are also required",
            "blocking_rows": "CG2389_5_GR_Newton;OCC2389_7_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2389_0_selected",
            "next_file": "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md",
            "success_condition": "derive a single observed coframe e_obs(q(Phi)) and parent-fixed tau used by matter, clocks, rods, orbital readout, and Hilbert source charge",
            "fallback_condition": "fill Delta_frame_source_over_MH, epsilon_q_owner, and epsilon_tau_selector rows with sourced finite nonclaim bounds",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2389_1_parallel",
            "next_file": "2390b-Y5-R2FR-no-direct-source-slot-grammar-or-hidden-source-bound.md",
            "success_condition": "prove no V_m[X,rho_A,W_source,C_top] or material marker can enter matter outside q/e_obs",
            "fallback_condition": "carry epsilon_hidden_source_slot and epsilon_marker_matter_lift as finite nonclaim rows",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2389_2_parallel",
            "next_file": "2390c-Y5-R2FR-explicit-standard-matter-Lm-sidecar-or-current-density-bound.md",
            "success_condition": "write the sector sidecar L_m examples and variation conventions for dust/scalar/EM test matter",
            "fallback_condition": "keep epsilon_JH_owner non-score-ready until a sector L_m is explicit",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2389_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2389_MATTER_ACTION_CURRENT_DENSITY_THEOREM.csv": current_density_theorem_rows,
    "P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv": owner_certificate_rows,
    "P8_Y5_PARENT_QLOC_2389_JH_OWNER_LEAK_VALUES.csv": leak_value_rows,
    "P8_Y5_PARENT_QLOC_2389_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2389_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2389_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2389_NEXT_TARGET.csv": next_target_rows,
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
    add("VAL2389_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2389_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = current_density_theorem_rows()
    add(
        "VAL2389_02_action_grammar_present",
        any("L_m(e_obs(q(Phi))" in row["statement"] for row in theorem),
        "observed-frame quotient-only matter action grammar is present",
    )
    add(
        "VAL2389_03_vertical_zero_present",
        any("v in ker(Dq)" in row["statement"] and "delta_v S_m" in row["statement"] for row in theorem),
        "vertical chain-rule zero condition is present",
    )
    certs = owner_certificate_rows()
    add(
        "VAL2389_04_required_gaps_explicit",
        all("MISSING" in row["status"] for row in certs),
        "q/eobs/Lm/tau/lift/no-slot/support/MHref gaps explicit",
    )
    values = leak_value_rows()
    add(
        "VAL2389_05_value_rows_nonready",
        all(
            row["score_ready"] == "false"
            and (("MISSING" in row["current_value"]) or row["current_value"] == "COMPONENTS_MISSING")
            for row in values
        ),
        "JH owner/frame/hidden-source leak rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2389_06_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2389_0_action_grammar_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2389_07_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths),
        "generated CSVs parse and have rows",
    )
    add("VAL2389_08_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2389_09_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2389_10_next_selected",
        any(row["row_id"] == "NEXT2389_0_selected" for row in next_target_rows()),
        "observed coframe pullback/same-frame lock selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2389_OVERALL",
        overall,
        "2389 derives conditional observed-frame matter-current grammar and vertical hidden-source zero route, refuses JH ownership without q/eobs/Lm/tau/no-slot/MHref, and selects e_obs(q) same-frame lock next",
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
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_MATTER_ACTION_CURRENT_DENSITY_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_JH_OWNER_LEAK_VALUES.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2389_VALIDATION.csv")

    body = f"""# 2389 - parent matter action current density or JH owner leak values

## Result

2389 attacks the coupling/current bottleneck directly.

The clean route is not to invent a new source density.  It is:

`S_m[Phi,psi_m] := integral_M L_m(e_obs(q(Phi)), psi_m, D_omega_obs(q(Phi)) psi_m; c_i)`,

with no independent `X`, `rho_A`, `W_source`, `C_top`, fitted radius, material-marker, or readout-mask slot.

Then the parent Hilbert density is the ordinary observed-frame coframe variation:

`delta L_m = E_m delta psi_m + T_a wedge delta e_obs^a + dTheta_m`,

so `J_H[tau] := -tau^a T_a`.

For every vertical variation `v in ker(Dq)`, the chain rule gives `delta_v S_m=0` if matter fields, constants, and
representation data are fixed over `q` and if no direct hidden source slots exist.  That is the good news: the route
can kill the hidden matter/source current by derivation rather than by tuning.

But current MTS still has not signed the parent `q`, `e_obs(q)`, explicit `L_m`, parent `tau`, matter lift/no-marker
rule, no-direct-slot grammar, support/tail theorem, or same-frame `M_H_ref`.  Therefore this is a conditional
current-density theorem, not a local-GR/Newton claim.

No `J_H` ownership pass, `W_source` pass, local-GR pass, Newton pass, PPN, clock, orbital, R10, or public/GitHub
claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Matter Action Current Density Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "derivation_status", "current_gain", "remaining_gap", "valid_for_claim"])}

## Current Owner Certificate

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## JH Owner Leak Values

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

This is a useful step toward the GR/Newton reduction because it identifies the honest bridge: MTS must make matter
see one observed coframe `e_obs(q(Phi))`, and then the source current is the usual Hilbert current.  The next lock is
therefore not another broad coupling essay.  It is the same-frame pullback: derive `e_obs(q)` and parent `tau`, or
score the frame/source leak.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2389_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2389_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
