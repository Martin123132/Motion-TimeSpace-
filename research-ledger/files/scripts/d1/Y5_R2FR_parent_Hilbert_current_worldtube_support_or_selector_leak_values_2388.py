from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PARENT_HILBERT_CURRENT_WORLDTUBE_SUPPORT_OR_SELECTOR_LEAK_VALUES_2388"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2388-Y5-R2FR-parent-Hilbert-current-worldtube-support-or-selector-leak-values.md"
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
            "row_id": "SRC2388_00_2387_doc",
            "source_key": "2387_domain_handoff",
            "source_path": POST_ROOT / "2387-Y5-R2FR-boundary-domain-selector-continuity-no-crossing-or-class-leak-values.md",
            "needles": ["W_source := closure(supp J_H[tau])", "2388-Y5-R2FR-parent-Hilbert-current-worldtube-support-or-selector-leak-values.md"],
            "source_role": "2387 selects parent Hilbert current/worldtube support as next gate",
        },
        {
            "row_id": "SRC2388_01_2387_certificates",
            "source_key": "2387_domain_certificates",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2387_DOMAIN_CERTIFICATE_MATRIX.csv",
            "needles": ["DCC2387_0_JH", "MISSING_COMPACT_SUPPORT_CERTIFICATE", "MISSING_POSITIVE_MHREF"],
            "source_role": "certificate gaps that 2388 must either close or carry as leak rows",
        },
        {
            "row_id": "SRC2388_02_1016_doc",
            "source_key": "1016_parent_worldtube_contract",
            "source_path": POST_ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "needles": ["W_source = closure(supp J_H[tau])", "contract_only_no_full_current_Lagrangian", "same-frame source current"],
            "source_role": "prior legal selector contract and missing parent Lagrangian warning",
        },
        {
            "row_id": "SRC2388_03_1718_doc",
            "source_key": "1718_support_owner",
            "source_path": POST_ROOT / "1718-Y5-R2FR-worldtube-support-owner-or-Icommutator-domain-numerator-bound.md",
            "needles": ["W_source = closure(supp J_H[tau])", "selector theorem is mathematically clean but remains conditional", "compact support"],
            "source_role": "worldtube support owner audit",
        },
        {
            "row_id": "SRC2388_04_1760_doc",
            "source_key": "1760_matter_worldtube_descent",
            "source_path": POST_ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["parent-owned Hilbert worldtubes", "delta_v S_matter=0", "direct/legal possibility"],
            "source_role": "matter/worldtube quotient descent obstruction",
        },
        {
            "row_id": "SRC2388_05_2183_doc",
            "source_key": "2183_worldtube_hilbert_selector",
            "source_path": POST_ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
            "needles": ["delta S_matter/delta e_obs", "source worldtube is selected before readout", "source-free annulus"],
            "source_role": "worldtube-Hilbert selector theorem attempt",
        },
        {
            "row_id": "SRC2388_06_1714_equality_doc",
            "source_key": "1714_worldtube_hilbert_equality",
            "source_path": POST_ROOT / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
            "needles": ["Pi_M J_H = J_M_top + dB_zero", "same object as the observed Hilbert/worldtube source mass"],
            "source_role": "source normalization requires the same Hilbert object, not merely a closed charge",
        },
        {
            "row_id": "SRC2388_07_parent_contract_csv",
            "source_key": "parent_action_contract_csv",
            "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "needles": ["PAC537_0_covariant_parent_action", "PAC537_2_parent_fixed_worldtube", "PAC537_5_Hilbert_topological_charge_equality"],
            "source_role": "parent action contract clauses for current/worldtube ownership",
        },
        {
            "row_id": "SRC2388_08_source_measure_csv",
            "source_key": "worldtube_source_measure_csv",
            "source_path": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            "needles": ["T510_1_worldtube_source_measure", "T510_3_Newton_PPN_readout"],
            "source_role": "GR/Newton transfer requires dressed Hamiltonian source charge",
        },
        {
            "row_id": "SRC2388_09_2182_doc",
            "source_key": "2182_topological_hilbert_equality",
            "source_path": POST_ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
            "needles": ["Pi_M J_H = J_M_top + dB_zero + R_eq", "same Hilbert source object"],
            "source_role": "topological route must become same Hilbert source object",
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


def hilbert_current_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCS2388_0_parent_matter_variation",
            "step": "parent Hilbert current definition",
            "statement": "For a parent matter action S_m[e_obs,psi_m]=int L_m, define the coframe Hilbert current T_a by delta L_m = E_m delta psi_m + T_a wedge delta e_obs^a + dTheta_m.",
            "derivation_status": "CONDITIONAL_STANDARD_VARIATIONAL_IDENTITY",
            "required_parent_clause": "explicit diffeomorphism-covariant L_m with one observed coframe e_obs and fixed matter variables",
            "current_gap": "no signed MTS parent matter Lagrangian supplies T_a",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCS2388_1_tau_contraction",
            "step": "time-generator contraction",
            "statement": "For a parent-fixed time generator tau=tau^a e_a, set J_H[tau] := -tau^a T_a, equivalently J_H^mu[tau]=T^mu_nu tau^nu in metric notation up to the chosen sign convention.",
            "derivation_status": "CONDITIONAL_CURRENT_FORMULA",
            "required_parent_clause": "tau fixed before source/readout and measured in the same observed frame as matter, clocks, rods, and orbital readout",
            "current_gap": "tau/e_obs same-frame lock not parent-signed for this branch",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCS2388_2_worldtube_support",
            "step": "worldtube support selector",
            "statement": "Define W_source[tau] := closure(supp J_H[tau]) before any residual fit; if J_H is parent-owned, W_source is selected by the source current rather than by a fitted radius or boundary.",
            "derivation_status": "CONDITIONAL_SELECTOR_DEFINITION",
            "required_parent_clause": "J_H is a real parent current and support is regular enough to admit linked exterior surfaces",
            "current_gap": "support compactness/regularity and source-tail treatment remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCS2388_3_diffeomorphism_naturality",
            "step": "covariant support transformation",
            "statement": "If L_m is natural under diffeomorphisms, then phi_*J_H[tau;Phi]=J_H[phi_*tau;phi_*Phi], so supp(J_H) and W_source transform covariantly.",
            "derivation_status": "CONDITIONAL_NATURALITY_THEOREM",
            "required_parent_clause": "no external material marker, noncovariant cutoff, or readout-chosen support mask",
            "current_gap": "no-marker/no-cutoff grammar is still a contract row, not a parent theorem",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCS2388_4_no_crossing_implication",
            "step": "domain no-crossing handoff",
            "statement": "If W_source is compact and remains a positive distance from the annulus boundary during the allowed source variation, then the linked surface class cannot jump and D_source C_top=0 follows conditionally.",
            "derivation_status": "CONDITIONAL_HANDOFF_TO_2387",
            "required_parent_clause": "compact support, fixed linked surfaces, no retuning after readout, no topology-changing source event",
            "current_gap": "the no-crossing certificate is not sourced by a parent support theorem",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCS2388_5_realistic_tail_warning",
            "step": "compactness caveat",
            "statement": "For fields with exterior stress, radiation, scalar tails, or long-range electromagnetic energy, closure(supp J_H) need not be compact; the compact-source theorem then becomes a tail-bound problem, not a zero proof.",
            "derivation_status": "OBSTRUCTION_RETAINED",
            "required_parent_clause": "either prove exterior Hilbert tail vanishes in the selected matter sector or provide a finite tail/source-pack bound",
            "current_gap": "no sector-by-sector tail theorem exists",
            "valid_for_claim": no_claim(),
        },
    ]


def support_certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_0_parent_Lm",
            "certificate": "explicit parent matter Lagrangian",
            "required_test": "write L_m[e_obs,psi_m,Dpsi_m] and derive T_a = delta L_m/delta e_obs^a before readout",
            "status": "MISSING_PARENT_MATTER_LAGRANGIAN",
            "residual_if_missing": "epsilon_JH_owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_1_same_frame",
            "certificate": "single observed source frame",
            "required_test": "matter, clocks, rods, tau, and orbital readout use the same e_obs/theta frame",
            "status": "MISSING_SAME_FRAME_TAU_EOBS_LOCK",
            "residual_if_missing": "Delta_frame_source_over_MH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_2_parent_tau",
            "certificate": "parent-owned time generator tau",
            "required_test": "tau is selected by parent boundary/asymptotic data, not by local residual fitting",
            "status": "MISSING_PARENT_TAU_SELECTOR",
            "residual_if_missing": "epsilon_tau_selector",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_3_support_compact",
            "certificate": "compact regular Hilbert support",
            "required_test": "closure(supp J_H[tau]) is compact/regular or an exterior tail norm is bounded",
            "status": "MISSING_COMPACT_SUPPORT_OR_TAIL_BOUND",
            "residual_if_missing": "epsilon_support_tail",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_4_no_marker",
            "certificate": "no material marker or readout mask",
            "required_test": "W_source is computed from J_H only; no fitted radius, galaxy mask, or residual-tuned boundary enters",
            "status": "MISSING_NO_MARKER_NO_READOUT_MASK_PROOF",
            "residual_if_missing": "epsilon_marker_selector",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_5_no_crossing",
            "certificate": "source-free annulus/no-crossing",
            "required_test": "A cap W_source remains empty under the allowed source variation with linked surfaces fixed",
            "status": "MISSING_NO_CROSSING_CERTIFICATE",
            "residual_if_missing": "epsilon_crossing_flux",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_6_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "derive finite positive Hamiltonian/Hilbert charge denominator in the same tau/e_obs frame",
            "status": "MISSING_POSITIVE_MHREF",
            "residual_if_missing": "all normalized rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WSC2388_7_same_object",
            "certificate": "same Hilbert/topological source object",
            "required_test": "Pi_M J_H = J_M_top + dB_zero + R_eq with R_eq and boundary flux either zero or bounded",
            "status": "MISSING_TOPOLOGICAL_HILBERT_EQUALITY",
            "residual_if_missing": "epsilon_M_source_mismatch",
            "valid_for_claim": no_claim(),
        },
    ]


def selector_leak_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLV2388_0_JH_owner",
            "quantity": "epsilon_JH_owner",
            "formula": "abs(Delta C_top_from_nonparent_JH * K_class)/M_H_ref",
            "units": "dimensionless after M_H_ref normalization",
            "current_value": "MISSING_PARENT_MATTER_LAGRANGIAN;MISSING_K_CLASS;MISSING_M_H_REF",
            "source_path": "",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLV2388_1_tau_frame",
            "quantity": "Delta_frame_source_over_MH",
            "formula": "abs(integral_S (J_H[tau_local]-J_H[tau_parent]))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_TAU_SELECTOR;MISSING_SAME_FRAME_CURRENT;MISSING_M_H_REF",
            "source_path": "",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLV2388_2_support_tail",
            "quantity": "epsilon_support_tail",
            "formula": "integral_{M\\W_delta} |J_H[tau]| / M_H_ref",
            "units": "dimensionless source-charge fraction",
            "current_value": "MISSING_JH_DENSITY;MISSING_W_DELTA;MISSING_TAIL_NORM;MISSING_M_H_REF",
            "source_path": "",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLV2388_3_marker_selector",
            "quantity": "epsilon_marker_selector",
            "formula": "abs(Delta C_top_from_readout_mask * K_marker)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_NO_MARKER_PROOF;MISSING_K_MARKER;MISSING_M_H_REF",
            "source_path": "",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLV2388_4_crossing_flux",
            "quantity": "epsilon_crossing_flux",
            "formula": "integral_path integral_{partial A} |i_n J_H[tau]| dlambda / M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_NO_CROSSING_PATH;MISSING_BOUNDARY_FLUX;MISSING_M_H_REF",
            "source_path": "",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLV2388_5_same_object",
            "quantity": "epsilon_M_source_mismatch",
            "formula": "abs(integral_S (Pi_M J_H - J_M_top - dB_zero))/M_H_ref",
            "units": "dimensionless source-charge mismatch",
            "current_value": "MISSING_PIM_JH;MISSING_JM_TOP;MISSING_B_ZERO;MISSING_R_EQ;MISSING_M_H_REF",
            "source_path": "",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLV2388_6_total",
            "quantity": "Delta_ref_worldtube_selector_total_over_MH",
            "formula": "epsilon_JH_owner + Delta_frame_source_over_MH + epsilon_support_tail + epsilon_marker_selector + epsilon_crossing_flux + epsilon_M_source_mismatch",
            "units": "dimensionless",
            "current_value": "COMPONENTS_MISSING",
            "source_path": "",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2388_0_accept_shape",
            "decision": "accept conditional Hilbert-current/worldtube selector shape",
            "reason": "the variational definition J_H[tau] := -tau^a delta L_m/delta e_obs^a is the right GR-compatible source object when parent-owned",
            "consequence": "worldtube selection is no longer arbitrary in form; it is a parent-current problem",
            "status": "CONDITIONAL_SELECTOR_SHAPE_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2388_1_no_promotion",
            "decision": "do not claim parent-owned W_source for current MTS",
            "reason": "explicit L_m, tau/e_obs lock, compact/tail theorem, no-marker proof, no-crossing certificate, M_H_ref, and Pi_M/J_M_top equality are missing",
            "consequence": "local-GR/Newton/R10/PPN/orbital/clock claims remain blocked",
            "status": "WORLD_TUBE_SELECTOR_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2388_2_tail_route",
            "decision": "retain tail-bound fallback",
            "reason": "realistic fields can have exterior stress/tails, so compact support cannot be assumed globally",
            "consequence": "if zero support fails, score support-tail and crossing-flux rows rather than hiding them",
            "status": "TAIL_BOUND_FALLBACK_REQUIRED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2388_3_next",
            "decision": "attack parent matter action current density next",
            "reason": "without an explicit L_m and same-frame tau/e_obs lock, J_H remains a legal placeholder",
            "consequence": "2389 should derive the parent matter-current density or fill epsilon_JH_owner and Delta_frame_source rows",
            "status": "SELECT_2389_PARENT_MATTER_CURRENT_DENSITY",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2388_0_selector_shape",
            "gate": "Hilbert-current selector formula shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "use as derivation route, not as evidence",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2388_1_parent_Lm",
            "gate": "explicit parent matter Lagrangian",
            "gate_status": "FAIL",
            "claim_effect": "J_H owner not claim-grade",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2388_2_tau_frame",
            "gate": "same-frame tau/e_obs source current",
            "gate_status": "FAIL",
            "claim_effect": "source-frame leakage remains open",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2388_3_compact_tail",
            "gate": "compact support or explicit tail bound",
            "gate_status": "FAIL",
            "claim_effect": "no-crossing theorem cannot be promoted",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2388_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "normalized residual rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2388_5_GR_Newton",
            "gate": "GR/Newton local source normalization",
            "gate_status": "BLOCKED",
            "claim_effect": "no local-GR/Newton claim",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2388_0_claim_Wsource",
            "claim": "W_source is now parent-derived for current MTS",
            "allowed": "false",
            "reason": "the selector formula is conditional; parent L_m and same-frame tau/e_obs lock are missing",
            "blocking_rows": "WSC2388_0_parent_Lm;WSC2388_1_same_frame;WSC2388_2_parent_tau",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2388_1_assume_compact",
            "claim": "compact support/no-crossing is automatic",
            "allowed": "false",
            "reason": "long-range field stress or tails can make support noncompact; a zero theorem or tail bound is required",
            "blocking_rows": "WSC2388_3_support_compact;SLV2388_2_support_tail;SLV2388_4_crossing_flux",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2388_2_score_residuals",
            "claim": "selector leak rows can be scored now",
            "allowed": "false",
            "reason": "M_H_ref and all parent coefficients/source paths are missing",
            "blocking_rows": "SLV2388_0_JH_owner;SLV2388_6_total;WSC2388_6_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2388_3_claim_GR",
            "claim": "local GR/Newton follows from the Hilbert-current shape",
            "allowed": "false",
            "reason": "GR/Newton also requires EH exterior fixed point, Hamiltonian charge equality, M_H_ref, PPN closure, and same object Pi_M/J_H/J_M_top",
            "blocking_rows": "WSC2388_7_same_object;CG2388_5_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2388_0_selected",
            "next_file": "2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md",
            "success_condition": "write an explicit parent matter action sector and derive T_a and J_H[tau] in the same observed coframe before readout",
            "fallback_condition": "fill epsilon_JH_owner, Delta_frame_source_over_MH, and epsilon_tau_selector rows with sourced finite bounds and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2388_1_parallel",
            "next_file": "2389b-Y5-R2FR-compact-support-tail-bound-or-crossing-flux-row.md",
            "success_condition": "prove sector-specific compact support/no exterior Hilbert tail for the local source class",
            "fallback_condition": "source a support-tail norm and no-crossing boundary-flux row",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2388_2_parallel",
            "next_file": "2389c-Y5-R2FR-Hilbert-topological-same-object-or-epsilonM-row.md",
            "success_condition": "derive Pi_M J_H = J_M_top + dB_zero with R_eq=0 and zero linked boundary flux",
            "fallback_condition": "carry epsilon_M_source_mismatch as finite nonclaim residual",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2388_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2388_HILBERT_CURRENT_SELECTOR_THEOREM.csv": hilbert_current_theorem_rows,
    "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv": support_certificate_rows,
    "P8_Y5_PARENT_QLOC_2388_SELECTOR_LEAK_VALUES.csv": selector_leak_rows,
    "P8_Y5_PARENT_QLOC_2388_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2388_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2388_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2388_NEXT_TARGET.csv": next_target_rows,
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
    add("VAL2388_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2388_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = hilbert_current_theorem_rows()
    add(
        "VAL2388_02_current_formula_present",
        any("J_H[tau] := -tau^a T_a" in row["statement"] for row in theorem),
        "Hilbert current contraction formula is present",
    )
    add(
        "VAL2388_03_worldtube_support_present",
        any("closure(supp J_H[tau])" in row["statement"] for row in theorem),
        "worldtube support selector definition is present",
    )
    certs = support_certificate_rows()
    add(
        "VAL2388_04_required_gaps_explicit",
        all("MISSING" in row["status"] for row in certs),
        "parent Lm/tau/support/no-marker/no-crossing/MHref/equality gaps explicit",
    )
    values = selector_leak_rows()
    add(
        "VAL2388_05_value_rows_nonready",
        all(row["score_ready"] == "false" and "MISSING" in row["current_value"] or row["current_value"] == "COMPONENTS_MISSING" for row in values),
        "selector leak rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2388_06_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2388_0_selector_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2388_07_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths),
        "generated CSVs parse and have rows",
    )
    add("VAL2388_08_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2388_09_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2388_10_next_selected",
        any(row["row_id"] == "NEXT2388_0_selected" for row in next_target_rows()),
        "parent matter action/current density selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2388_OVERALL",
        overall,
        "2388 derives conditional parent Hilbert-current/worldtube selector shape, refuses promotion without parent Lm/tau/support/MHref/equality, and selects current-density ownership next",
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
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_HILBERT_CURRENT_SELECTOR_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_SELECTOR_LEAK_VALUES.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2388_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2388_VALIDATION.csv")

    body = f"""# 2388 - parent Hilbert current worldtube support or selector leak values

## Result

2388 takes the 2387 handoff literally: do not treat `W_source` as a fitted domain label.  Make it the support of a
parent-owned Hilbert current, or keep the selector as a leak.

The conditional derivation is:

1. Start with a parent matter action `S_m[e_obs,psi_m]=int L_m`.
2. Vary with respect to the observed coframe:
   `delta L_m = E_m delta psi_m + T_a wedge delta e_obs^a + dTheta_m`.
3. Contract the Hilbert coframe current with a parent-fixed time generator:
   `J_H[tau] := -tau^a T_a`.
4. Define the source worldtube before readout:
   `W_source[tau] := closure(supp J_H[tau])`.

If `L_m`, `e_obs`, `tau`, the matter variables, and the support rule are all parent-owned, then `W_source` is a
covariant pre-readout selector.  If the support is compact and remains away from the annulus boundary during source
variation, the 2387 no-crossing argument can carry `D_source C_top=0` conditionally.

This is useful, but it is not yet a current-MTS local-GR proof.  The current corpus still lacks an explicit parent
matter Lagrangian, same-frame `tau/e_obs` lock, compact-support or tail theorem, no-marker proof, no-crossing
certificate, positive `M_H_ref`, and Hilbert/topological same-object equality.

So 2388 improves the derivation route, but refuses promotion.  No `W_source` pass, local-GR pass, Newton pass, PPN,
clock, orbital, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Hilbert Current Selector Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "derivation_status", "required_parent_clause", "current_gap", "valid_for_claim"])}

## Worldtube Support Certificate

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## Selector Leak Values

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

This is a real narrowing of the GR/Newton bridge.  We are no longer asking vaguely whether the local boundary
knows the source.  The question is now whether the parent action can produce one observed-frame Hilbert current
`J_H[tau]`, and whether its support is compact or tail-bounded enough to choose linked exterior domains without
readout retuning.  That is the next honest lock.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2388_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2388_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
