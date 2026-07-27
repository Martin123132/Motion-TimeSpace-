from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1665"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1665-Y5-R2FR-response-normal-form-parent-signature-or-live-GammaKhat-adoption.md"

EPSILON_FRAME_LEAK_M1 = 2.43238775e-13

SOURCE_FILES = {
    "1664_doc": ROOT / "1664-Y5-R2FR-Gamma-Khat-metric-response-source-formula-or-Helmholtz-obstruction.md",
    "1664_validation": OUT / "P8_Y5_BRR545_1664_VALIDATION.csv",
    "1011_response_doublet": OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
    "516_doublet_contract": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
    "517_doublet_variation": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
    "517_metric_response": OUT / "P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv",
    "517_euler_source": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "1282_component_map": OUT / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
    "1620_quotient_verticality": OUT / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv",
    "1505_dq_verticality": OUT / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
    "1038_vertical_field_map": OUT / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv",
    "590_dcdagger_map": OUT / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
    "781_minimal_coupling_action": OUT / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
    "783_coupling_field_map": OUT / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv",
    "1597_coupling_zero": OUT / "P8_Y5_PARENT_QLOC_1597_COUPLING_ZERO_PROOF_AUDIT.csv",
    "1229_source_coupling": OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
    "1473_coupling_double_zero": OUT / "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv",
    "1287_khat_component": OUT / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
    "1526_symbol_match": OUT / "P8_Y5_PARENT_QLOC_1526_SYMBOL_MATCH_AUDIT.csv",
    "1527_khat_adoption": OUT / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
    "1624_no_vertical_metric": OUT / "P8_Y5_PARENT_QLOC_1624_NO_VERTICAL_METRIC_DECISION.csv",
}

NEEDLES = {
    "1664_doc": ["NEXT_1665_PARENT_SIGN_OR_DEMOTE", "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED"],
    "1664_validation": ["VAL1664_OVERALL", "PASS"],
    "1011_response_doublet": ["RDT1011_7_verdict", "fail_current_claim"],
    "516_doublet_contract": ["RD516_4_zero_odd_source", "not_derived_hard_block"],
    "517_doublet_variation": ["AV517_4_Euler_equation", "blocked_by_source_current_rows"],
    "517_metric_response": ["MR517_2_Z_metric_lock", "PPN_lock_open"],
    "517_euler_source": ["Y5_source_normalization", "hard_fail_current"],
    "1282_component_map": ["RCM1282_6_verdict", "COMPONENT_MAP_NOT_CLOSED"],
    "1620_quotient_verticality": ["QVM1620_4_normal_form_Z", "MISSING_COMPUTATION"],
    "1505_dq_verticality": ["DQT1505_8_acceptance", "BLOCKED"],
    "1038_vertical_field_map": ["Gamma_Khat_qloc_sector", "CONDITIONAL_NOT_INTEGRATED_WITH_DCX"],
    "590_dcdagger_map": ["DVM590_3_precise_map", "conditional_map_theorem"],
    "781_minimal_coupling_action": ["MPC781_7_contract_verdict", "candidate_only_requires_782_consistency_gate"],
    "783_coupling_field_map": ["FM783_7_q_loc", "residual_not_quotient"],
    "1597_coupling_zero": ["CZP1597_2_coupling_zero_verdict", "COUPLING_ZERO_PROOF_NOT_DERIVED"],
    "1229_source_coupling": ["THM1229_1_iff", "EXACT_CONTRACT_WRITTEN_NOT_PROVED"],
    "1473_coupling_double_zero": ["DZ1473_4_verdict", "NOT_PARENT_DERIVED_EMIT_EXECUTABLE_RESIDUAL_VECTOR"],
    "1287_khat_component": ["KTC1287_0_flat_Ricci_scalar_KL00", "FORMAL_COMPONENT_ROW_FILLED_NONCLAIM"],
    "1526_symbol_match": ["SYM1526_5_verdict", "NOT_MATCHED"],
    "1527_khat_adoption": ["KAD1527_4_verdict", "STAGED_NOT_PROMOTED"],
    "1624_no_vertical_metric": ["NVD1624_4_verdict", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED_FINAL_CURRENT_AUDIT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1665_SOURCE_REGISTER.csv"
PARENT_SIGNATURE_CLAUSES = OUT / "P8_Y5_PARENT_QLOC_1665_PARENT_SIGNATURE_CLAUSE_AUDIT.csv"
Z_ROUTE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1665_Z_ROUTE_SIGNATURE_AUDIT.csv"
PHI_ROUTE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1665_PHI_ROUTE_SIGNATURE_AUDIT.csv"
COUPLING_VERTICAL_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1665_COUPLING_VERTICAL_GENERATOR_AUDIT.csv"
ADOPTION_DEMOTION = OUT / "P8_Y5_PARENT_QLOC_1665_ADOPTION_OR_DEMOTION_DECISION.csv"
RETAINED_RESIDUALS = OUT / "P8_Y5_PARENT_QLOC_1665_RETAINED_RESIDUALS.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1665_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1665_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1665_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PARENT_SIGNATURE_CLAUSES,
    Z_ROUTE_AUDIT,
    PHI_ROUTE_AUDIT,
    COUPLING_VERTICAL_AUDIT,
    ADOPTION_DEMOTION,
    RETAINED_RESIDUALS,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    PARENT_SIGNATURE_CLAUSES,
    Z_ROUTE_AUDIT,
    PHI_ROUTE_AUDIT,
    COUPLING_VERTICAL_AUDIT,
    ADOPTION_DEMOTION,
    RETAINED_RESIDUALS,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    PARENT_SIGNATURE_CLAUSES: [
        QUARANTINE / "PARENT_SIGNATURE_CLAUSE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_signature_clause_audit_nonclaim_1665.csv",
        QUEUE / "JR1665_PARENT_SIGNATURE_CLAUSE_AUDIT_NONCLAIM.csv",
    ],
    Z_ROUTE_AUDIT: [
        QUARANTINE / "Z_ROUTE_SIGNATURE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_z_route_signature_audit_nonclaim_1665.csv",
        QUEUE / "JR1665_Z_ROUTE_SIGNATURE_AUDIT_NONCLAIM.csv",
    ],
    PHI_ROUTE_AUDIT: [
        QUARANTINE / "PHI_ROUTE_SIGNATURE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_phi_route_signature_audit_nonclaim_1665.csv",
        QUEUE / "JR1665_PHI_ROUTE_SIGNATURE_AUDIT_NONCLAIM.csv",
    ],
    COUPLING_VERTICAL_AUDIT: [
        QUARANTINE / "COUPLING_VERTICAL_GENERATOR_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_coupling_vertical_generator_audit_nonclaim_1665.csv",
        QUEUE / "JR1665_COUPLING_VERTICAL_GENERATOR_AUDIT_NONCLAIM.csv",
    ],
    RETAINED_RESIDUALS: [
        QUARANTINE / "RETAINED_RESIDUALS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_retained_residuals_nonclaim_1665.csv",
        QUEUE / "JR1665_RETAINED_RESIDUALS_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1665.csv",
        QUEUE / "JR1665_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "local_gr_claim_allowed",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "theorem_closed",
        "theorem_closed_for_claim",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1665 response-normal-form parent signature or live Gamma/Khat adoption input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_signature_clause_rows() -> list[dict[str, object]]:
    rows = [
        ("PSC1665_0_parent_field_chart", "Phi_parent is explicitly listed with quotient variables, residual variables, matter/readout variables, and boundary variables.", "MPC781/FM783 provide a candidate bundle, but q and ker(Dq) are not parent-defined.", "CONTRACT_ONLY_NOT_PARENT_SIGNED", "needed before Z or phi can be called actual MTS variables"),
        ("PSC1665_1_quotient_map", "q(Phi_parent) and Dq are computable on the proposed Z/phi directions.", "QVM1620 and DQT1505 retain missing computation/unified basis.", "MISSING_DQ_COMPUTATION", "blocks vertical/gauge deletion and beta-zero shortcuts"),
        ("PSC1665_2_vertical_generator", "the generator is v=Omega^{-1} DC^dagger with field-by-field action on metric/coframe, extra, matter, readout, and boundary blocks.", "DVM590 gives the exact map shape; 1038 says MTS field actions remain unmapped.", "MAP_SHAPE_KNOWN_PARENT_OMEGA_AND_FIELD_ACTION_MISSING", "this is the true coupling/vertical-generator bottleneck"),
        ("PSC1665_3_matter_even_descent", "ordinary matter, clocks, photons, sources, and orbit readouts descend through the same even quotient/coframe.", "RDT1011, RD516, THM1229, and MPC781 keep matter/source descent conditional.", "MISSING_MATTER_SOURCE_DESCENT", "without this, source-current zero is not derivable"),
        ("PSC1665_4_live_GammaKhat_adoption", "Gamma_eff and K_hat are adopted as the metric-response sector of the same live parent action.", "1664, SYM1526, and KAD1527 say live adoption is not made.", "NOT_LIVE", "blocks q_loc zero and local GR promotion"),
        ("PSC1665_5_source_current_zero", "J_Z=0 and all source-normalization/source-current channels are either even quotient data or theorem-zero.", "Y5 source-normalization is hard-fail current route; coupling-zero proof not derived.", "SOURCE_CURRENT_ZERO_NOT_DERIVED", "this is where GR/Newton source recovery fails if left open"),
        ("PSC1665_6_boundary_projector_no_flux", "boundary, domain, projector, and symplectic flux terms vanish or are retained with source-backed projection.", "RD516_6, MR517_3, and 1038 keep boundary/projector pieces open.", "BOUNDARY_PROJECTOR_OPEN", "prevents silent alpha3/source-measure leakage"),
        ("PSC1665_7_residual_vector_lock", "Z=0 or phi-fixed implies q_loc=Y5=Y6=DeltaPPN=q_H=DeltaCoupling=0 through a full-rank response map.", "RCM1282 verdict says component map is not closed.", "PHYSICAL_LOCK_NOT_DERIVED", "formal normal form does not yet cover the observed residual vector"),
        ("PSC1665_8_verdict", "all parent-signature clauses close together.", "multiple required clauses are missing or conditional only.", "PARENT_SIGNATURE_NOT_CLOSED", "cannot adopt response-normal-form or trace-free improvement as live local-GR proof"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "required_clause": clause,
            "current_evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause, evidence, status, effect in rows
    ]


def z_route_rows() -> list[dict[str, object]]:
    rows = [
        ("ZRA1665_0_formal_action", "S_GK[Z] normal form", "positive response-doublet action supplies formal action, metric response, Helmholtz, and double-zero", "PASS_FORMAL_NORMAL_FORM_ONLY", "CAL1619/NF1619 support but current MTS signature is open"),
        ("ZRA1665_1_doublets_exist", "R_+^A,R_-^A for every physical local residual channel", "RDT1011_0 and RD516_0 say component coverage is partial/conditional", "NOT_DERIVED", "cannot assert Z spans all local leakage"),
        ("ZRA1665_2_exchange_symmetry", "exact parent exchange R_+ <-> R_- forbids linear Z terms", "RDT1011_1 says exchange exactness is only a conditional template", "CONDITIONAL_TEMPLATE", "linear source terms are not killed in live MTS"),
        ("ZRA1665_3_even_matter", "S_matter and readout depend only on R_even/q(Phi)", "RDT1011_2 and THM1229 say source/matter descent is not parent-signed", "NOT_DERIVED_HARD_FOR_Y5", "measured source normalization can remain exchange-even and nonzero"),
        ("ZRA1665_4_source_current", "J_Z=0 on compact local branch", "RDT1011_3 and AV517_4 are blocked by source-current rows", "FAIL_CURRENT_CLAIM", "homogeneous positive operator theorem cannot activate"),
        ("ZRA1665_5_boundary_zero", "B_Z=0/no odd boundary charge", "RDT1011_4 and RD516_6 keep boundary no-flux conditional/open", "CONDITIONAL_NOT_CLOSED", "boundary/collar force can survive"),
        ("ZRA1665_6_positive_operator", "L_AB positive after gauge/constraint removal", "formal candidate exists but depends on source and boundary zero", "FORMAL_CANDIDATE_ONLY", "mass gap suppresses; it does not prove zero by itself"),
        ("ZRA1665_7_physical_residual_lock", "Z controls q_loc/PPN/source-normalization/coupling residual vector", "RCM1282_6 says component map not closed", "COMPONENT_MAP_NOT_CLOSED", "formal Z could be a shadow variable"),
        ("ZRA1665_8_verdict", "adopt Z normal form as live MTS local sector", "Z route remains best derivation target but not parent-signed", "DO_NOT_ADOPT_LIVE_NONCLAIM", "retain as primary derivation path only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "z_route_id": route_id,
            "target": target,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, evidence, status, effect in rows
    ]


def phi_route_rows() -> list[dict[str, object]]:
    rows = [
        ("PRA1665_0_tracefree_algebra", "TF metric response of int sqrt(-g) phi R gives K_L shape", "VAR1526_3/KTC1287 show exact formal component match", "PASS_CONDITIONAL_ALGEBRA_ONLY", "real algebraic clue, not live K_hat"),
        ("PRA1665_1_phi_owner", "phi is a local parent auxiliary field with action/constraint", "KTC1287 and VAR1526 keep parent origin for phi/A_nu missing", "PHI_OWNER_MISSING", "inverse-Box shorthand would be nonlocal/closure-only"),
        ("PRA1665_2_coefficient_sign", "sigma_resp*c_I and sign/volume convention are source-owned", "KAD1527 stages sigma_resp*c_I=1 only as adoption row", "COEFFICIENT_SIGN_UNSIGNED", "cannot compare to live K_hat tensor"),
        ("PRA1665_3_boundary_domain", "Green inverse, boundary conditions, Ricci/Einstein branch, and multiplier stress are owned", "KTC1287 marks Green inverse/boundary/domain missing", "BOUNDARY_DOMAIN_UNSIGNED", "DeltaK can re-enter through boundary/domain terms"),
        ("PRA1665_4_live_adoption", "current K_hat is defined as this trace-free improvement response", "SYM1526_5 says current symbol match is not matched; KAD1527_4 says staged not promoted", "STAGED_NOT_PROMOTED", "do not use K_L as live K_hat in local tests"),
        ("PRA1665_5_source_coupling", "phi route also kills ordinary matter/source/readout coupling residues", "THM1229/CZP1597/DZ1473 keep coupling/source zero open", "DOES_NOT_SOLVE_COUPLING_BY_ITSELF", "Khat shape alone is not GR reduction"),
        ("PRA1665_6_verdict", "adopt phi improvement as live MTS K_hat route", "exact shape match exists, but owner/adoption/coupling clauses fail", "DO_NOT_ADOPT_LIVE_NONCLAIM", "retain as secondary K_hat construction path"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "phi_route_id": route_id,
            "target": target,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, evidence, status, effect in rows
    ]


def coupling_vertical_rows() -> list[dict[str, object]]:
    rows = [
        ("CVG1665_0_dcdagger_map", "DC^dagger epsilon = Omega^flat(v)", "DVM590_3 gives clean conditional map theorem", "FORMAL_MAP_SHAPE_EXISTS", "useful: the vertical generator is not mystical; it is the symplectic dual of the constraint variation"),
        ("CVG1665_1_parent_omega", "parent symplectic form Omega and reduced inverse exist", "DVM590_4 says actual generator needs Omega inverse; 1038 says parent symplectic potential missing", "PARENT_OMEGA_MISSING", "cannot compute actual v for MTS extra sectors"),
        ("CVG1665_2_field_action", "v acts field-by-field on metric/coframe, extra, matter, readout, and boundary variables", "1038 marks extra, matter/readout, and boundary blocks unmapped/not derived", "FIELD_MAP_INCOMPLETE", "putative gauge direction can leak into observed charges"),
        ("CVG1665_3_Dq_verticality", "Dq[Z] or Dq[phi] is zero or constraint-eliminated before matter sees it", "QVM1620/DQT1505 say Dq computation and unified basis are missing", "Dq_VERTICALITY_NOT_CLOSED", "visible residual cannot be deleted as gauge"),
        ("CVG1665_4_source_coupling_zero", "ordinary matter/source coupling has no representative/source-weight leakage", "CZP1597 says coupling-zero proof not derived; THM1229 iff is exact but unproved", "COUPLING_ZERO_NOT_DERIVED", "this is the live GR/Newton source-side blocker"),
        ("CVG1665_5_double_zero_couplings", "every non-EH observed coupling C_i has C_i(Phi0)=0 and partial_A C_i(Phi0)=0", "DZ1473 gives exact Taylor lemma but parent list/proof missing", "EXACT_LEMMA_NOT_PARENT_DERIVED", "fixed point alone does not kill couplings"),
        ("CVG1665_6_no_vertical_metric", "vertical representative has no legal kinetic/source operator", "NVD1624 final audit says no-vertical-metric theorem not derived for current corpus", "THEOREM_ZERO_NOT_AVAILABLE", "finite branch remains live"),
        ("CVG1665_7_verdict", "coupling/vertical generator parent-signature", "formal map shapes exist, but parent Omega, Dq, field action, matter descent, and source zero are unsigned", "COUPLING_VERTICAL_SIGNATURE_NOT_CLOSED", "next work should attack this directly, not loop over Khat shape"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, obj, evidence, status, effect in rows
    ]


def adoption_demotion_rows() -> list[dict[str, object]]:
    rows = [
        ("ADD1665_0_Z_live_adoption", "adopt positive response-doublet normal form as live MTS sector", "REJECT_LIVE_ADOPTION_NOW", "Z component map/source-current/matter descent/boundary/coupling clauses fail", "retain as primary derivation target"),
        ("ADD1665_1_phi_live_adoption", "adopt trace-free phi R improvement as live K_hat", "REJECT_LIVE_ADOPTION_NOW", "phi owner/coefficient/boundary/live Khat/coupling clauses fail", "retain as secondary Khat construction target"),
        ("ADD1665_2_current_q_loc_zero", "treat q_loc=0/local GR as derived from existing files", "DEMOTE_TO_CLOSURE_ONLY_FOR_CLAIMS", "current route is formal mechanism plus missing parent signature, not a theorem", "no local GR/Newton/PPN/R10/WEP claim"),
        ("ADD1665_3_best_route", "continue derivation-first attack", "SELECT_COUPLING_VERTICAL_GENERATOR_PARENT_OBJECT_LANGUAGE", "coupling/vertical generator is the common missing premise behind Z, phi, source-current, and Dq routes", "build one parent object-language/field-action packet or retain residuals"),
        ("ADD1665_4_fallback", "if parent object-language cannot be built", "RETAIN_RESIDUAL_BOUND_BRANCH", "finite coupling/source/boundary coefficients must remain explicit", "keeps theory testable without smuggling GR"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "proposal": proposal,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, proposal, decision, reason, next_action in rows
    ]


def retained_residual_rows() -> list[dict[str, object]]:
    rows = [
        ("RR1665_0_epsilon_frame_leak", "epsilon_frame_leak", f"{EPSILON_FRAME_LEAK_M1:.8e}", "m^-1", "retained from 1662/1663/1664", "Gamma/Khat adoption and apparatus transfer not parent-signed"),
        ("RR1665_1_q_loc_unmatched", "q_loc_unmatched", "MISSING_GAMMA_OWNER + MISSING_KHAT_RESPONSE + MISSING_HELMHOLTZ + MISSING_PLOC_TRANSFER", "symbolic", "retained from 1664", "current q_loc cannot be reduced to parent-signed variational zero"),
        ("RR1665_2_Z_parent_signature_gap", "Z_signature_gap", "MISSING_DOUBLETS + MISSING_Dq + MISSING_SOURCE_ZERO + MISSING_COMPONENT_LOCK", "symbolic", "1665 Z-route audit", "response-normal-form remains formal only"),
        ("RR1665_3_phi_parent_owner_gap", "phi_owner_gap", "MISSING_PHI_ACTION + MISSING_BOUNDARY_DOMAIN + MISSING_LIVE_ADOPTION", "symbolic", "1665 phi-route audit", "trace-free improvement remains nonclaim"),
        ("RR1665_4_coupling_vertical_gap", "coupling_vertical_gap", "MISSING_OMEGA + MISSING_FIELD_ACTION + MISSING_MATTER_DESCENT + MISSING_SOURCE_COUPLING_ZERO", "symbolic", "1665 coupling/vertical audit", "GR/Newton source side cannot be declared derived"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "residual": residual,
            "value_or_marker": value,
            "units": units,
            "source": source,
            "reason_retained": reason,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for residual_id, residual, value, units, source, reason in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1665_0_Z_live_sector", "positive response-doublet normal form is actual MTS local sector", False, "BLOCKED", "Z route not parent-signed"),
        ("CG1665_1_phi_live_Khat", "trace-free phi R improvement is actual current K_hat", False, "BLOCKED", "phi route not parent-signed"),
        ("CG1665_2_coupling_zero", "all first-order non-EH coupling/source/readout residuals vanish", False, "BLOCKED", "coupling-zero and double-zero premises not parent-derived"),
        ("CG1665_3_vertical_generator", "actual vertical generator is computed and lies in ker(Dq) or is constraint-eliminated", False, "BLOCKED", "Omega/DC/Dq/field action missing"),
        ("CG1665_4_q_loc_zero", "q_loc^nu -> 0 locally", False, "NO_CLAIM", "current route demoted to closure-only for claims"),
        ("CG1665_5_local_GR_Newton", "local GR/Newton reduction is derived", False, "NO_CLAIM", "source side and q_loc residuals retained"),
        ("CG1665_6_PPN_R10_WEP_clock_orbit", "PPN/R10/WEP/clock/orbital passes follow", False, "NO_CLAIM", "no arena claim until parent signature or source-backed bounds exist"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "local_gr_claim_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1666-Y5-R2FR-coupling-vertical-generator-parent-object-language-or-residual-bound-handoff.md",
            "script": "scripts/Y5_R2FR_coupling_vertical_generator_parent_object_language_or_residual_bound_handoff.py",
            "objective": "construct the minimal parent object language that could sign the coupling/vertical-generator route: parent field chart, quotient q, Dq on Z/phi, Omega/DCdagger vertical action, matter/readout descent, source-current zero, and boundary/projector handling; if this cannot be sourced, hand off to explicit residual-bound rows",
            "success_condition": "either the common coupling/vertical-generator parent-signature packet closes, or every missing clause is emitted as a retained residual/source-bound input",
            "forbidden_shortcuts": "no q_loc=0 claim; no formal Z-as-live claim; no phi Khat adoption without owner; no coupling-zero by intuition; no GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def validation_rows(
    source_rows: list[dict[str, object]],
    clauses: list[dict[str, object]],
    z_route: list[dict[str, object]],
    phi_route: list[dict[str, object]],
    coupling_vertical: list[dict[str, object]],
    decisions: list[dict[str, object]],
    retained: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    generated_name_markers = (
        "1665-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1665",
        "P8_Y5_BRR545_1665",
        "JR1665",
        "R2FR_",
        "Y5_R2FR_response_normal_form_parent_signature",
    )
    formalization_dirty = (
        any(
            "1665" in path.name
            and any(marker in path.name for marker in generated_name_markers)
            for path in FORMALIZATION.rglob("*1665*")
        )
        if FORMALIZATION.exists()
        else False
    )
    parent_signature_failed = any(row["clause_id"] == "PSC1665_8_verdict" and row["status"] == "PARENT_SIGNATURE_NOT_CLOSED" for row in clauses)
    z_not_adopted = any(row["z_route_id"] == "ZRA1665_8_verdict" and row["status"] == "DO_NOT_ADOPT_LIVE_NONCLAIM" for row in z_route)
    phi_not_adopted = any(row["phi_route_id"] == "PRA1665_6_verdict" and row["status"] == "DO_NOT_ADOPT_LIVE_NONCLAIM" for row in phi_route)
    coupling_blocked = any(row["audit_id"] == "CVG1665_7_verdict" and row["status"] == "COUPLING_VERTICAL_SIGNATURE_NOT_CLOSED" for row in coupling_vertical)
    closure_demoted = any(row["decision"] == "DEMOTE_TO_CLOSURE_ONLY_FOR_CLAIMS" for row in decisions)
    retained_nonclaim = all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in retained)
    next_target_selected = next_targets[0]["next_target"] == "1666-Y5-R2FR-coupling-vertical-generator-parent-object-language-or-residual-bound-handoff.md"

    checks = [
        ("VAL1665_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1665 source paths exist and needles are present"),
        ("VAL1665_1_parent_signature_failed", parent_signature_failed, "parent-signature clause audit remains closed against live adoption"),
        ("VAL1665_2_Z_not_adopted", z_not_adopted, "Z normal form retained as formal/nonclaim only"),
        ("VAL1665_3_phi_not_adopted", phi_not_adopted, "phi trace-free route retained as formal/nonclaim only"),
        ("VAL1665_4_coupling_vertical_blocked", coupling_blocked, "coupling/vertical-generator signature is identified as the common blocker"),
        ("VAL1665_5_closure_demoted_for_claims", closure_demoted, "current q_loc zero route demoted to closure-only for claims"),
        ("VAL1665_6_retained_residuals_nonclaim", retained_nonclaim, "all retained residual rows remain nonclaim"),
        ("VAL1665_7_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS local claims false"),
        ("VAL1665_8_next_target_selected", next_target_selected, "next target selects coupling/vertical-generator parent object-language or residual handoff"),
        ("VAL1665_9_csv_parse", generated_csv_parse, "all generated 1665 CSVs parse"),
        ("VAL1665_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1665 generated rows keep MTS claim/no-score flags false"),
        ("VAL1665_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1665_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1665_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1665_14_formalization_untouched", not formalization_dirty, "no 1665 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1665_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1665 response-normal-form parent signature or live Gamma/Khat adoption validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    clauses: list[dict[str, object]],
    z_route: list[dict[str, object]],
    phi_route: list[dict[str, object]],
    coupling_vertical: list[dict[str, object]],
    decisions: list[dict[str, object]],
    retained: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1665 - Response Normal Form Parent Signature Or Live Gamma/Khat Adoption

**Private status:** parent-signature/adoption gate. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The attempt to adopt the response-normal-form or trace-free-improvement route as live MTS fails at the current-corpus level.

```text
Z route: real formal mechanism, not parent-signed.
phi route: real Khat-shape algebra, not parent-signed.
coupling/vertical generator: common missing object.
current q_loc=0 route: demoted to closure-only for claims.
```

This is progress, not retreat. It says the next useful fight is not another vague "maybe K_hat is like this" pass. It is the parent object-language/coupling pass:

```text
Phi_parent, q(Phi), Dq[Z/phi], Omega, DCdagger, v, matter/readout descent, source-current zero, boundary/projector silence.
```

Until that packet closes:

```text
epsilon_frame_leak = {EPSILON_FRAME_LEAK_M1:.8e} m^-1 remains retained.
Z_signature_gap, phi_owner_gap, and coupling_vertical_gap remain retained symbolic residuals.
```

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Parent Signature Clauses

{markdown_table(clauses, ["clause_id", "required_clause", "current_evidence", "status", "effect"])}

## Z Route Signature Audit

{markdown_table(z_route, ["z_route_id", "target", "evidence", "status", "effect"])}

## Phi Route Signature Audit

{markdown_table(phi_route, ["phi_route_id", "target", "evidence", "status", "effect"])}

## Coupling / Vertical Generator Audit

{markdown_table(coupling_vertical, ["audit_id", "object", "evidence", "status", "effect"])}

## Adoption Or Demotion Decision

{markdown_table(decisions, ["decision_id", "proposal", "decision", "reason", "next_action"])}

## Retained Residuals

{markdown_table(retained, ["residual_id", "residual", "value_or_marker", "units", "reason_retained"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

The coupling was not a side issue. It is the shared hinge between local GR recovery, Newton source universality, q_loc silence, Khat adoption, and R10/PPN safety. The formal machinery is good enough to be worth pursuing, but it must be tied to actual parent variables and actual matter/source/readout descent. If that tying fails, the correct scientific move is not to bin MTS; it is to run the residual-bound branch honestly.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    clauses = parent_signature_clause_rows()
    z_route = z_route_rows()
    phi_route = phi_route_rows()
    coupling_vertical = coupling_vertical_rows()
    decisions = adoption_demotion_rows()
    retained = retained_residual_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (PARENT_SIGNATURE_CLAUSES, clauses),
        (Z_ROUTE_AUDIT, z_route),
        (PHI_ROUTE_AUDIT, phi_route),
        (COUPLING_VERTICAL_AUDIT, coupling_vertical),
        (ADOPTION_DEMOTION, decisions),
        (RETAINED_RESIDUALS, retained),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, clauses, z_route, phi_route, coupling_vertical, decisions, retained, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, clauses, z_route, phi_route, coupling_vertical, decisions, retained, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1665 validation failed; see P8_Y5_BRR545_1665_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1665 validation PASS")


if __name__ == "__main__":
    main()
