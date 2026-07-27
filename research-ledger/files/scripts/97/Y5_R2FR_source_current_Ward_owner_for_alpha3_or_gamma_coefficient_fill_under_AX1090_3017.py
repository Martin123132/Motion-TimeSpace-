from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3017"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3017-Y5-R2FR-source-current-Ward-owner-for-alpha3-or-gamma-coefficient-fill-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3017_00_3016_doc": ROOT / "3016-Y5-R2FR-gamma-and-alpha3-PPN-kernel-first-derivation-under-AX1090.md",
    "SRC3017_01_3016_validation": RESIDUALS / "P8_Y5_BRR545_3016_VALIDATION.csv",
    "SRC3017_02_3016_alpha3_audit": RESIDUALS / "P8_Y5_R2FR_3016_ALPHA3_ZERO_THEOREM_AUDIT.csv",
    "SRC3017_03_3016_gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3016_GAMMA_KERNEL_DERIVATION.csv",
    "SRC3017_04_1889_Ward_owner": ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md",
    "SRC3017_05_2642_source_current_identity": ROOT / "2642-Y5-R2FR-JH-JNH-boundary-readout-source-current-identity-or-bound-pack.md",
    "SRC3017_06_2918_alpha3_kernel": ROOT / "2918-Y5-R2FR-alpha3-source-current-kernel-or-no-disformal-slot-theorem-under-AX1090.md",
    "SRC3017_07_2919_stationary_alpha3": ROOT / "2919-Y5-R2FR-stationary-alpha3-flux-zero-theorem-or-beta-source-normalization-kernel-under-AX1090.md",
    "SRC3017_08_2939_parent_noether": ROOT / "2939-Y5-R2FR-parent-Noether-theta-Qtau-extraction-or-source-measure-closure-axiom-under-AX1090.md",
    "SRC3017_09_3006_current_owner": ROOT / "3006-Y5-R2FR-parent-theta-Qtau-Htau-extraction-or-Hamiltonian-current-owner-under-AX1090.md",
    "SRC3017_10_1008_theta_Qtau": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
    "SRC3017_11_2749_minimal_action": ROOT / "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md",
    "SRC3017_12_3015_ppn_comparators": RESIDUALS / "P8_Y5_R2FR_3015_PPN_COMPARATOR_LINKS.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3017_SOURCE_REGISTER.csv",
    "ward_owner": RESIDUALS / "P8_Y5_R2FR_3017_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "alpha3_heads": RESIDUALS / "P8_Y5_R2FR_3017_ALPHA3_HEAD_REDUCTION_MATRIX.csv",
    "gamma_fill": RESIDUALS / "P8_Y5_R2FR_3017_GAMMA_COEFFICIENT_FILL_CONTRACT.csv",
    "noether_links": RESIDUALS / "P8_Y5_R2FR_3017_NOETHER_CURRENT_CHAIN_LINKS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3017_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3017_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3017_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3017_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3017_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ward_copy": PARENT_ACTION / "source_current_Ward_owner_alpha3_3017_NOT_SIGNED.csv",
    "alpha3_copy": LOCAL_BOUNDS / "alpha3_head_reduction_matrix_3017_NONCLAIM.csv",
    "gamma_copy": LOCAL_BOUNDS / "gamma_coefficient_fill_contract_3017_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3017_GAMMA_COEFFICIENT_OR_BETA_SQUARE_LAW_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3017_00_3016_doc": "3016 handoff: alpha3 Ward route or gamma coefficient fill",
    "SRC3017_01_3016_validation": "3016 validation/no-claim status",
    "SRC3017_02_3016_alpha3_audit": "alpha3 zero-theorem audit",
    "SRC3017_03_3016_gamma_kernel": "gamma coefficient-ratio kernel",
    "SRC3017_04_1889_Ward_owner": "Ward owner versus species-blind source theorem",
    "SRC3017_05_2642_source_current_identity": "JH/JNH/boundary/readout source-current identity and bound pack",
    "SRC3017_06_2918_alpha3_kernel": "alpha3 source-current head kernel",
    "SRC3017_07_2919_stationary_alpha3": "stationary alpha3 flux attempt and partial q_loc win",
    "SRC3017_08_2939_parent_noether": "parent Noether theta/Qtau extraction status",
    "SRC3017_09_3006_current_owner": "current-chain/Htau owner status",
    "SRC3017_10_1008_theta_Qtau": "theta/Qtau extraction refusal ledger",
    "SRC3017_11_2749_minimal_action": "minimal weak-field parent ansatz and Ward/PPN gate",
    "SRC3017_12_3015_ppn_comparators": "source-backed PPN comparator links",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

ward_owner = [
    base(
        {
            "ward_id": "WARD3017_0_Ward_bridge",
            "clause": "diffeomorphism Ward identity",
            "formal_statement": "delta_xi S_parent=0 implies a conserved current for the source object chosen by the action",
            "current_result": "VALID_CONDITIONAL_BRIDGE",
            "alpha3_effect": "can support alpha3 zero only after the chosen current has no preferred/source-exchange projection",
            "missing_for_claim": "MISSING_CHOSEN_CURRENT_GR_SAFE_PROOF",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_1_label_forgetting",
            "clause": "source functor forgets species/source labels",
            "formal_statement": "q_src({(T_A,A)})=T_total before coupling selection",
            "current_result": "NOT_PARENT_SIGNED",
            "alpha3_effect": "would remove relative source weights feeding Delta_w_eff",
            "missing_for_claim": "MISSING_PARENT_LABEL_FORGETTING_QUOTIENT",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_2_no_source_prefactor",
            "clause": "no source-only prefactors before variation",
            "formal_statement": "S_matter is not sum_A w_A S_A with independent source-only w_A",
            "current_result": "COUNTERMODEL_SURVIVES",
            "alpha3_effect": "pre-action weights can still create Delta_w_eff while Ward conservation holds",
            "missing_for_claim": "MISSING_NO_SOURCE_PREFACTOR_PARENT_CLAUSE",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_3_same_frame_descent",
            "clause": "same observed coframe for matter, clocks, sources and orbits",
            "formal_statement": "S_matter=Sbar[g_obs,psi] and source/readout maps use the same pre-readout coframe",
            "current_result": "CONDITIONAL_UNSIGNED",
            "alpha3_effect": "prevents source-frame/current-frame mismatch from entering alpha3",
            "missing_for_claim": "MISSING_SAME_FRAME_MATTER_DESCENT",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_4_no_nonHilbert_current",
            "clause": "no retained non-Hilbert source-current channel",
            "formal_statement": "J_NH=0 or Pi_alpha3[J_NH]=0 in the compact local branch",
            "current_result": "NOT_DERIVED",
            "alpha3_effect": "would remove the J_NH alpha3 head",
            "missing_for_claim": "MISSING_NO_HILBERT_CURRENT_THEOREM_OR_BOUND",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_5_boundary_domain_no_flux",
            "clause": "boundary/domain/projector alpha3 flux silence",
            "formal_statement": "Pi_alpha3[Q_edge + Q_domain + Q_projector]=0 or finite below 4e-20",
            "current_result": "NOT_DERIVED",
            "alpha3_effect": "would remove boundary/domain preferred-frame momentum heads",
            "missing_for_claim": "MISSING_BOUNDARY_NO_FLUX; MISSING_DOMAIN_PROJECTOR_NOLEAK",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_6_no_preferred_vector_slot",
            "clause": "no disformal/preferred vector current through PPN order",
            "formal_statement": "no parent D(C_R)u_mu u_nu or equivalent preferred-frame source-current slot",
            "current_result": "UNSIGNED_FROM_2918",
            "alpha3_effect": "would remove d_R/vector alpha3 head",
            "missing_for_claim": "MISSING_NO_DISFORMAL_SLOT_THEOREM",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_7_fixed_coupling_scales",
            "clause": "fixed kappa_MTS and ell_J on the local comparison branch",
            "formal_statement": "Dln(kappa_MTS)=0 and Dln(ell_J)=0 before source/readout fitting",
            "current_result": "NOT_PARENT_DERIVED",
            "alpha3_effect": "would remove coupling/source-current scale drift heads",
            "missing_for_claim": "MISSING_CONSTANT_KAPPA_PROOF; MISSING_CONSTANT_ELLJ_PROOF",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_8_parent_current_chain",
            "clause": "theta_MTS/Q_tau/H_tau owner",
            "formal_statement": "one varied parent action supplies theta_MTS, J_tau, Q_tau^MTS, and C_tau with sector certificates",
            "current_result": "BLOCKED_BY_2939_3006_1008",
            "alpha3_effect": "without this, Ward owner remains a contract rather than a proof",
            "missing_for_claim": "MISSING_SINGLE_PARENT_ACTION; MISSING_SECTOR_VARIATIONS; MISSING_CTAU_SILENCE",
        }
    ),
    base(
        {
            "ward_id": "WARD3017_9_verdict",
            "clause": "alpha3 Ward theorem-zero",
            "formal_statement": "WARD3017_0 through WARD3017_8 must all hold to promote alpha3=0",
            "current_result": "THEOREM_ZERO_NOT_SIGNED",
            "alpha3_effect": "alpha3 remains explicit nonclaim residual with named heads",
            "missing_for_claim": "MISSING_ALL_UNSIGNED_ALPHA3_OWNER_CLAUSES",
        }
    ),
]

alpha3_heads = [
    base(
        {
            "head_id": "A3H3017_0_q_loc_Hilbert",
            "symbol": "q_loc_Hilbert_exterior",
            "reduction_result": "CONDITIONAL_PARTIAL_ZERO",
            "source_basis": "2919 stationary compact exterior q_loc head",
            "status": "USEFUL_BUT_NOT_TOTAL_ALPHA3",
            "next_requirement": "parent-sign stationary/source-support hypotheses",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_1_Delta_w_eff",
            "symbol": "Delta_w_eff",
            "reduction_result": "RETAINED",
            "source_basis": "1889/2513 relative source-weight guard",
            "status": "MISSING_LABEL_FORGETTING_AND_NO_PREFACTOR",
            "next_requirement": "prove no source-prefactor/no spurion return",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_2_J_NH",
            "symbol": "J_NH",
            "reduction_result": "RETAINED",
            "source_basis": "2642 JNH component pack",
            "status": "MISSING_NONHILBERT_ZERO_OR_BOUND",
            "next_requirement": "derive no non-Hilbert source channel or source-backed coefficient",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_3_Q_edge",
            "symbol": "Q_edge",
            "reduction_result": "RETAINED",
            "source_basis": "2642/2918 boundary alpha3 head",
            "status": "MISSING_BOUNDARY_NOFLUX_OR_PRODUCT",
            "next_requirement": "prove boundary alpha3 flux zero or fill K_boundary*Phi boundary product",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_4_domain_projector",
            "symbol": "Q_domain_projector",
            "reduction_result": "RETAINED",
            "source_basis": "2918/2919 domain alpha3 head",
            "status": "MISSING_DOMAIN_PROJECTOR_NOLEAK",
            "next_requirement": "derive no preferred vector/domain leakage",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_5_kappa",
            "symbol": "Dln(kappa_MTS)",
            "reduction_result": "RETAINED",
            "source_basis": "2918/2919 coupling owner gates",
            "status": "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE",
            "next_requirement": "source parent constant-coupling theorem or finite projection",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_6_ellJ",
            "symbol": "Dln(ell_J)",
            "reduction_result": "RETAINED",
            "source_basis": "2918/2919 source-current scale head",
            "status": "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE",
            "next_requirement": "source ell_J owner theorem or finite projection",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_7_dR",
            "symbol": "d_R_vector",
            "reduction_result": "RETAINED",
            "source_basis": "2918 no-disformal-slot audit",
            "status": "MISSING_NO_DISFORMAL_SLOT_OR_D_R_VALUE",
            "next_requirement": "prove no preferred-vector/disformal current slot",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_8_readout_tail",
            "symbol": "endpoint_domain_readout_tail",
            "reduction_result": "RETAINED",
            "source_basis": "2918/2642 readout and DqZ tails",
            "status": "MISSING_FIXED_BEFORE_READOUT_AND_DQZ",
            "next_requirement": "lock observed map before variation or retain explicit tail",
            "target_bound_abs": "4e-20",
        }
    ),
    base(
        {
            "head_id": "A3H3017_9_total_abs",
            "symbol": "Delta_alpha3_abs",
            "reduction_result": "RETAINED_NONCLAIM",
            "source_basis": "3016 total alpha3 gate plus 2918/2919 heads",
            "status": "TOTAL_ALPHA3_NOT_ZERO_NOT_SCORE_READY",
            "next_requirement": "every head theorem-zero or source-backed finite with no cancellation",
            "target_bound_abs": "4e-20",
        }
    ),
]

gamma_fill = [
    base(
        {
            "fill_id": "GCF3017_0_A_T",
            "quantity": "A_T",
            "definition": "time-time weak-field coefficient in g00=-1+2 A_T U/c^2+O(c^-4)",
            "needed_source": "source-normalized parent field equation and measured-GM convention before readout",
            "current_status": "MISSING_PARENT_SOURCE_NORMALIZATION",
            "claim_use": "denominator of gamma_eff=A_S/A_T",
        }
    ),
    base(
        {
            "fill_id": "GCF3017_1_A_S",
            "quantity": "A_S",
            "definition": "spatial weak-field coefficient in gij=(1+2 A_S U/c^2)delta_ij+O(c^-4)",
            "needed_source": "metric/coframe spatial response from parent normal-form or residual kernel",
            "current_status": "MISSING_SPATIAL_METRIC_RESPONSE",
            "claim_use": "numerator of gamma_eff=A_S/A_T",
        }
    ),
    base(
        {
            "fill_id": "GCF3017_2_s_R",
            "quantity": "s_R",
            "definition": "common conformal residual coefficient with A_T=1-s_R and A_S=1+s_R",
            "needed_source": "parent-signed common-frame Weyl coefficient or theorem-zero",
            "current_status": "MISSING_s_R_VALUE_OR_ZERO_THEOREM",
            "claim_use": "special-case gamma_minus_1=2 s_R/(1-s_R)",
        }
    ),
    base(
        {
            "fill_id": "GCF3017_3_readout_gauge",
            "quantity": "PPN readout gauge",
            "definition": "map from parent observed coframe/source normalization to PPN gamma extraction",
            "needed_source": "DObs/source-frame lock and no post-fit GM/readout absorption",
            "current_status": "MISSING_READOUT_GAUGE",
            "claim_use": "prevents fake gamma closure by calibration",
        }
    ),
    base(
        {
            "fill_id": "GCF3017_4_gamma_bound_row",
            "quantity": "gamma prediction row",
            "definition": "abs((A_S-A_T)/A_T) <= 2.3e-05 or abs(2s_R/(1-s_R)) <= 2.3e-05",
            "needed_source": "A_T/A_S/s_R values or theorem-zero plus readout gauge and no full-vector overclaim",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "claim_use": "first executable PPN component only, not local-GR pass",
        }
    ),
]

noether_links = [
    base(
        {
            "link_id": "NCL3017_0_formula",
            "object": "Noether current formula",
            "status": "EXACT_CONDITIONAL",
            "evidence": "2939/3006/1008 agree on J_tau=theta_MTS(L_tau Phi)-i_tau L_parent",
            "claim_effect": "not enough without parent sector ownership",
        }
    ),
    base(
        {
            "link_id": "NCL3017_1_owner_gap",
            "object": "single parent action",
            "status": "MISSING",
            "evidence": "3006 CCA rows keep single action, field list and sector variations missing",
            "claim_effect": "blocks Ward-owner alpha3 proof",
        }
    ),
    base(
        {
            "link_id": "NCL3017_2_sector_gap",
            "object": "sector theta/Q_tau pieces",
            "status": "MISSING_OR_REFERENCE_ONLY",
            "evidence": "EH core is baseline only; extra/projector/boundary/matter-source pieces remain unowned",
            "claim_effect": "prevents total C_tau silence",
        }
    ),
    base(
        {
            "link_id": "NCL3017_3_source_glue_gap",
            "object": "Hilbert source and worldtube source measure glue",
            "status": "MISSING",
            "evidence": "2939 C_matter_source and 3006 source_bridge remain unsigned",
            "claim_effect": "blocks Delta_w_eff and gamma A_T source normalization",
        }
    ),
    base(
        {
            "link_id": "NCL3017_4_alpha3_consequence",
            "object": "alpha3 theorem-zero",
            "status": "BLOCKED",
            "evidence": "Ward is a necessary bridge, not a proof that all alpha3 heads vanish",
            "claim_effect": "keep alpha3 residual nonclaim",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3017_0_sources_exist",
            "gate": "all cited local source paths exist",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "3017 cites only local private ledgers",
        }
    ),
    base(
        {
            "gate_id": "GATE3017_1_Ward_bridge",
            "gate": "Ward bridge is written as conditional theorem",
            "result": True,
            "notes": "Ward conservation applies to the current chosen by the action",
        }
    ),
    base(
        {
            "gate_id": "GATE3017_2_Ward_owner",
            "gate": "Ward owner proves alpha3=0",
            "result": False,
            "notes": "label-forgetting, no-prefactor, non-Hilbert, boundary/domain, disformal, coupling and current-chain clauses are unsigned",
        }
    ),
    base(
        {
            "gate_id": "GATE3017_3_alpha3_claim",
            "gate": "alpha3 4e-20 pass claim allowed",
            "result": False,
            "notes": "total alpha3 head matrix remains nonclaim and not score-ready",
        }
    ),
    base(
        {
            "gate_id": "GATE3017_4_gamma_fill",
            "gate": "gamma coefficient fill contract exists",
            "result": True,
            "notes": "A_T/A_S/s_R/readout-gauge slots are staged for next concrete PPN component fill",
        }
    ),
    base(
        {
            "gate_id": "GATE3017_5_local_GR_claim",
            "gate": "local GR/Newton claim allowed",
            "result": False,
            "notes": "alpha3, beta, source normalization, and parent-current chain remain open",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3017_0_Ward_result",
            "decision": "Ward is retained as a necessary bridge but not promoted as alpha3 zero proof",
            "rationale": "Ward conservation does not choose the GR-safe current, erase source prefactors, or kill boundary/domain/non-Hilbert heads",
            "consequence": "alpha3 remains a nonclaim source-current residual vector",
        }
    ),
    base(
        {
            "decision_id": "DEC3017_1_partial_win",
            "decision": "stationary q_loc Hilbert head remains a useful conditional partial zero",
            "rationale": "2919 kills one exterior Hilbert-current head under fixed stationary/support hypotheses",
            "consequence": "do not throw it away, but do not call it total alpha3 silence",
        }
    ),
    base(
        {
            "decision_id": "DEC3017_2_gamma_fallback",
            "decision": "gamma coefficient fill is now the cleanest next executable PPN move",
            "rationale": "gamma has an algebraic kernel and explicit missing coefficient slots; alpha3 needs a much larger parent-current theorem",
            "consequence": "stage A_T/A_S/s_R/readout-gauge fill before broad PPN scoring",
        }
    ),
    base(
        {
            "decision_id": "DEC3017_3_beta_reminder",
            "decision": "beta square-law remains the next deep GR-reduction gate after gamma coefficient fill",
            "rationale": "2919 already identified beta_eff=B_source/A_source^2 as the second-order source-normalization test",
            "consequence": "3018 should choose gamma coefficient fill while preserving beta square-law as the following target",
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3017_0_3018",
            "target_doc": "3018-Y5-R2FR-gamma-coefficient-fill-AST-or-beta-square-law-branch-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_gamma_coefficient_fill_AST_or_beta_square_law_branch_under_AX1090_3018.py",
            "mission": "fill or theorem-zero the gamma coefficient inputs A_T, A_S, s_R and readout gauge from parent/source-normalized evidence; if those cannot be filled, route directly to the beta square-law B_source=A_source^2 gate without claiming gamma/local-GR",
            "success_condition": "gamma gets a source-backed nonclaim prediction row or a precise blocker ledger strong enough to hand off to beta square-law; no gamma-only, alpha3, PPN, Newton, or local-GR claim",
            "forbidden": "no Ward-only alpha3 proof; no fitted-GM gamma closure; no gamma-only local-GR claim; no EH import as MTS proof; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["ward_owner"], ward_owner)
write_csv(OUTPUTS["alpha3_heads"], alpha3_heads)
write_csv(OUTPUTS["gamma_fill"], gamma_fill)
write_csv(OUTPUTS["noether_links"], noether_links)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("ward_copy", "ward_owner"),
    ("alpha3_copy", "alpha3_heads"),
    ("gamma_copy", "gamma_fill"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3017_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = (
    source_register
    + ward_owner
    + alpha3_heads
    + gamma_fill
    + noether_links
    + promotion_gates
    + decision
    + next_target
)

validation_rows = [
    {
        "validation_id": "VAL3017_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3017_01_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3017_02_Ward_not_promoted",
        "passed": any(row["ward_id"] == "WARD3017_9_verdict" and row["current_result"] == "THEOREM_ZERO_NOT_SIGNED" for row in ward_owner),
        "requirement": "Ward bridge is not promoted as alpha3 zero proof",
        "evidence": OUTPUTS["ward_owner"].name,
    },
    {
        "validation_id": "VAL3017_03_alpha3_heads_complete",
        "passed": len(alpha3_heads) >= 10 and any(row["head_id"] == "A3H3017_9_total_abs" for row in alpha3_heads),
        "requirement": "alpha3 head reduction matrix includes total no-cancellation residual",
        "evidence": OUTPUTS["alpha3_heads"].name,
    },
    {
        "validation_id": "VAL3017_04_gamma_fill_contract",
        "passed": {"A_T", "A_S", "s_R"}.issubset({row["quantity"] for row in gamma_fill}),
        "requirement": "gamma coefficient fill contract includes A_T, A_S and s_R",
        "evidence": OUTPUTS["gamma_fill"].name,
    },
    {
        "validation_id": "VAL3017_05_claims_blocked",
        "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows)
        and any(row["gate_id"] == "GATE3017_5_local_GR_claim" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "alpha3/PPN/local-GR claims remain blocked",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3017_06_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all 3017 generated ledgers",
    },
    {
        "validation_id": "VAL3017_07_branch_copies_exist",
        "passed": all(boolish(row["exists"]) for row in branch_rows),
        "requirement": "branch copies and acquisition queue exist",
        "evidence": OUTPUTS["branches"].name,
    },
    {
        "validation_id": "VAL3017_08_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3017_09_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3017_10_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3018-Y5-R2FR-gamma-coefficient-fill"),
        "requirement": "next target selects gamma coefficient fill or beta square-law handoff",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3017_99_overall",
        "passed": overall_pass,
        "requirement": "all 3017 validation checks pass",
        "evidence": "aggregate of VAL3017_00 through VAL3017_10",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3017 - Source-Current Ward Owner for Alpha3 or Gamma Coefficient Fill under AX1090

Status: `Y5_R2FR_3017_Ward_bridge_retained_alpha3_zero_not_signed_gamma_fill_next`

## Verdict

3017 takes the best shot at the `alpha3` Ward route and refuses the overclaim.

The Ward bridge is real:

`delta_xi S_parent=0 -> conserved current for the current chosen by the action`.

But that is not the same as proving the action chose the GR-safe source current. A Ward identity can conserve a weighted, hidden, boundary-shifted, non-Hilbert, disformal, or readout-contaminated source unless the parent action forbids those channels.

So `alpha3=0` is not signed here. The exact theorem contract is now:

`alpha3=0` only if Ward conservation, label-forgetting, no pre-action source prefactors, same-frame matter descent, no non-Hilbert current, no boundary/domain alpha3 flux, no preferred-vector/disformal slot, fixed `kappa_MTS`, fixed `ell_J`, and parent theta/Q_tau/H_tau current ownership all hold together.

Current MTS does not sign that full stack. The partial stationary `q_loc` head from 2919 remains useful, but total `Delta_alpha3_abs` stays live and nonclaim.

The productive fallback is now the lower-dimensional PPN component: fill the `gamma` coefficient slots `A_T`, `A_S`, `s_R`, and the readout gauge. That can produce the first source-backed component row without pretending it is a full local-GR pass.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Ward Owner Attempt

{md_table(ward_owner, ["ward_id", "clause", "current_result", "alpha3_effect", "missing_for_claim"])}

## Alpha3 Head Reduction Matrix

{md_table(alpha3_heads, ["head_id", "symbol", "reduction_result", "status", "next_requirement", "target_bound_abs"])}

## Gamma Coefficient Fill Contract

{md_table(gamma_fill, ["fill_id", "quantity", "definition", "current_status", "claim_use"])}

## Noether Current-Chain Links

{md_table(noether_links, ["link_id", "object", "status", "evidence", "claim_effect"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["ward_owner"]}`
- `{OUTPUTS["alpha3_heads"]}`
- `{OUTPUTS["gamma_fill"]}`
- `{OUTPUTS["noether_links"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["ward_copy"]}`
- `{BRANCH_OUTPUTS["alpha3_copy"]}`
- `{BRANCH_OUTPUTS["gamma_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No Ward-only `alpha3=0` proof.
- No `alpha3` 4e-20 pass claim.
- No fitted-`GM` gamma closure.
- No gamma-only local-GR claim.
- No EH import as MTS proof.
- No hidden cancellation across alpha3 heads.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
