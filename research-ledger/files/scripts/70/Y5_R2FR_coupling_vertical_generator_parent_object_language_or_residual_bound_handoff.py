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
QUARANTINE = MICROSCOPE / "quarantine" / "1666"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1666-Y5-R2FR-coupling-vertical-generator-parent-object-language-or-residual-bound-handoff.md"

EPSILON_FRAME_LEAK_M1 = 2.43238775e-13

SOURCE_FILES = {
    "1665_doc": ROOT / "1665-Y5-R2FR-response-normal-form-parent-signature-or-live-GammaKhat-adoption.md",
    "1665_validation": OUT / "P8_Y5_BRR545_1665_VALIDATION.csv",
    "1665_coupling_vertical": OUT / "P8_Y5_PARENT_QLOC_1665_COUPLING_VERTICAL_GENERATOR_AUDIT.csv",
    "703_coupling_lock": OUT / "P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv",
    "715_bottleneck": OUT / "P8_Y5_R10_715_COUPLING_BOTTLENECK_AUDIT.csv",
    "716_matter_coupling": OUT / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
    "759_coupling_owner": OUT / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv",
    "727_dcdagger": OUT / "P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv",
    "727_field_action": OUT / "P8_Y5_R10_727_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
    "670_vertical_certificate": OUT / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv",
    "938_vertical_contract": OUT / "P8_Y5_R10_938_VERTICAL_THEOREM_CONTRACT.csv",
    "781_minimal_action": OUT / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
    "783_field_map": OUT / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv",
    "1505_dq_tests": OUT / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
    "1229_source_coupling": OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
    "1473_double_zero": OUT / "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv",
}

NEEDLES = {
    "1665_doc": ["SELECT_COUPLING_VERTICAL_GENERATOR_PARENT_OBJECT_LANGUAGE", "DEMOTE_TO_CLOSURE_ONLY_FOR_CLAIMS"],
    "1665_validation": ["VAL1665_OVERALL", "PASS"],
    "1665_coupling_vertical": ["CVG1665_7_verdict", "COUPLING_VERTICAL_SIGNATURE_NOT_CLOSED"],
    "703_coupling_lock": ["PAL703_8_verdict", "fail_current_corpus"],
    "715_bottleneck": ["CBA715_6_no_mode_theorem", "not_proved"],
    "716_matter_coupling": ["MCD716_6_current_corpus_verdict", "zero_not_derived"],
    "759_coupling_owner": ["COA759_6_verdict", "coupling_owner_not_parent_signed"],
    "727_dcdagger": ["DVM727_3_precise_map", "conditional_map_theorem"],
    "727_field_action": ["Gamma_Khat_qloc_sector", "conditional_from_513_not_integrated_with_CX"],
    "670_vertical_certificate": ["VGC670_0_parent_Omega", "missing"],
    "938_vertical_contract": ["VTC938_6_total_theorem", "conditional_theorem_not_current_claim"],
    "781_minimal_action": ["MPC781_7_contract_verdict", "candidate_only_requires_782_consistency_gate"],
    "783_field_map": ["FM783_1_Q", "needed_but_not_owned"],
    "1505_dq_tests": ["DQT1505_8_acceptance", "BLOCKED"],
    "1229_source_coupling": ["THM1229_1_iff", "EXACT_CONTRACT_WRITTEN_NOT_PROVED"],
    "1473_double_zero": ["DZ1473_4_verdict", "NOT_PARENT_DERIVED_EMIT_EXECUTABLE_RESIDUAL_VECTOR"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1666_SOURCE_REGISTER.csv"
OBJECT_LANGUAGE_PACKET = OUT / "P8_Y5_PARENT_QLOC_1666_OBJECT_LANGUAGE_PACKET.csv"
CONDITIONAL_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1666_CONDITIONAL_THEOREM_ATTEMPT.csv"
BLOCKER_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1666_BLOCKER_MATRIX.csv"
RESIDUAL_HANDOFF = OUT / "P8_Y5_PARENT_QLOC_1666_RESIDUAL_BOUND_HANDOFF.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1666_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1666_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1666_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1666_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OBJECT_LANGUAGE_PACKET,
    CONDITIONAL_THEOREM,
    BLOCKER_MATRIX,
    RESIDUAL_HANDOFF,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    OBJECT_LANGUAGE_PACKET,
    CONDITIONAL_THEOREM,
    BLOCKER_MATRIX,
    RESIDUAL_HANDOFF,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    OBJECT_LANGUAGE_PACKET: [
        QUARANTINE / "OBJECT_LANGUAGE_PACKET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_object_language_packet_nonclaim_1666.csv",
        QUEUE / "JR1666_OBJECT_LANGUAGE_PACKET_NONCLAIM.csv",
    ],
    CONDITIONAL_THEOREM: [
        QUARANTINE / "CONDITIONAL_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_conditional_theorem_attempt_nonclaim_1666.csv",
        QUEUE / "JR1666_CONDITIONAL_THEOREM_ATTEMPT_NONCLAIM.csv",
    ],
    BLOCKER_MATRIX: [
        QUARANTINE / "BLOCKER_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_blocker_matrix_nonclaim_1666.csv",
        QUEUE / "JR1666_BLOCKER_MATRIX_NONCLAIM.csv",
    ],
    RESIDUAL_HANDOFF: [
        QUARANTINE / "RESIDUAL_BOUND_HANDOFF_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_residual_bound_handoff_nonclaim_1666.csv",
        QUEUE / "JR1666_RESIDUAL_BOUND_HANDOFF_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1666.csv",
        QUEUE / "JR1666_NEXT_TARGET_NONCLAIM.csv",
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
                "role": "1666 coupling/vertical-generator parent object-language or residual-bound handoff input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def object_language_rows() -> list[dict[str, object]]:
    rows = [
        ("OLP1666_0_parent_field_chart", "Phi_parent=(g/e_obs, Gamma/Khat/q_loc sector, Z_or_phi sector, memory/domain/projector fields, matter/readout fields, boundary/edge data)", "write the minimal domain where every local variation is typed before variation", "MPC781/FM783 candidate bundle only; no parent-signed field chart", "CONTRACT_WRITTEN_NOT_PARENT_SIGNED"),
        ("OLP1666_1_quotient_map", "Q=q(Phi_parent)=(e_obs,g_obs,source/readout data, constants theta_owned)", "ordinary matter and readout must see Q only, not representative residuals", "FM783 says Q is needed but not owned; DQT1505 says q is partial prior contract", "Q_NOT_OWNED"),
        ("OLP1666_2_residual_coordinates", "R_phys={q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling}; Z or phi may be an auxiliary coordinate only if mapped to R_phys", "prevents formal auxiliary variables becoming shadow wins", "RCM1282 and 1665 show residual-vector lock is not closed", "RESIDUAL_LOCK_MISSING"),
        ("OLP1666_3_vertical_generator", "v_X=Omega^{-1}[(DC_X)^dagger X] on reduced nondegenerate parent phase space", "turns vertical motion into a calculable generator, not intuition", "DVM727 gives formal map; VGC670 says Omega/DC/field action missing", "FORMAL_MAP_NOT_PARENT_OWNED"),
        ("OLP1666_4_matter_descent", "S_matter[Phi,Psi]=Sbar_matter[q(Phi),Psi,theta] with no species/source/readout multiplier outside Q", "would make Lie_v S_matter=0 for v in ker(Dq)", "COA759/MCD716/THM1229 keep descent and source weights unsigned", "MATTER_DESCENT_NOT_SIGNED"),
        ("OLP1666_5_same_frame_stack", "e_source=e_clock=e_photon=e_orbit=e_boundary=e_obs through tested order", "keeps Newton source side, clocks, photons, and orbits in one frame", "PAL703 and COA759 keep same-frame/source lock conditional", "SAME_FRAME_NOT_SIGNED"),
        ("OLP1666_6_boundary_projector", "boundary charge Q_X, projector P_loc, and compact collar terms are zero, exact, or retained", "prevents edge charge from reappearing as alpha3/source mass leakage", "VGC670/VTC938 keep boundary differentiability and compact flux open", "BOUNDARY_PROJECTOR_OPEN"),
        ("OLP1666_7_packet_verdict", "OLP1666_0 through OLP1666_6 parent-signed jointly", "would allow local residual theorem attempts to be meaningful", "current corpus supplies a precise contract, not parent signatures", "OBJECT_LANGUAGE_PACKET_CONTRACT_ONLY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "packet_id": packet_id,
            "object_language_clause": clause,
            "purpose": purpose,
            "current_evidence": evidence,
            "status": status,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for packet_id, clause, purpose, evidence, status in rows
    ]


def conditional_theorem_rows() -> list[dict[str, object]]:
    rows = [
        ("THM1666_0_statement", "If Phi_parent, q, Dq, Omega/DCdagger/v, matter descent, same-frame readout, and boundary/projector silence are all parent-signed, then any Z/phi direction with Dq[v]=0 and zero source/boundary charge is locally unobservable to first order.", "chain rule gives delta_v S_matter=(delta Sbar/delta q)Dq[v]=0; proper generator gives no boundary charge; double-zero gives C_i=O(deltaPhi^2)", "EXACT_CONDITIONAL_THEOREM_WRITTEN"),
        ("THM1666_1_Newton_GR_source_side", "Under the same premises, ordinary Hilbert source current is universal up to one common G_ref calibration.", "S_matter descends through one e_obs and one action scale, so species/source weights are absent or common", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"),
        ("THM1666_2_q_loc_side", "If Gamma/Khat sector is the same parent variational stress and Z/phi maps to R_phys with source/boundary zero, q_loc begins at second order or retained residual terms.", "Ward identity plus metric response and double-zero; not valid if Gamma/Khat remain bookkeeping", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"),
        ("THM1666_3_no_mode_branch", "If the relevant residual direction is a proper presymplectic gauge/topological direction with no boundary charge, finite source/test charges vanish.", "Omega(delta,v)=dB+E terms and int_boundary dB=0", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"),
        ("THM1666_4_countermodel_guard", "If any representative source weight, frame transfer, boundary charge, or physical finite mode survives, local GR/Newton is not derived and the branch must be bounded.", "MCD716 and CBA715 give explicit scalar/source charge countermodel structure", "COUNTERMODEL_ACTIVE"),
        ("THM1666_5_verdict", "The parent object-language theorem is mathematically coherent but not current-MTS derived.", "clauses are missing: q, Dq, Omega/DC, field action, source descent, boundary, same frame", "CONDITIONAL_THEOREM_ONLY_NO_CLAIM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "proof_sketch": proof,
            "status": status,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, proof, status in rows
    ]


def blocker_rows() -> list[dict[str, object]]:
    rows = [
        ("BLK1666_0_q_map", "q(Phi_parent) and Dq on Z/phi", "FM783_1_Q; DQT1505_8_acceptance", "MISSING_COMPUTABLE_Q_AND_DQ", "source/readout sees representative motion unless bounded"),
        ("BLK1666_1_parent_Omega", "Omega, DC_X, and reduced inverse", "DVM727_3; VGC670_0", "MISSING_PARENT_OMEGA_AND_DCX", "vertical generator cannot be computed"),
        ("BLK1666_2_field_action", "field-by-field v action", "727 field action map; 1038 field map", "FIELD_ACTION_INCOMPLETE", "hidden extra/matter/boundary sector may carry charge"),
        ("BLK1666_3_matter_descent", "ordinary matter descends through q only", "COA759_6; MCD716_6", "MATTER_DESCENT_NOT_PARENT_SIGNED", "source/test charges remain finite"),
        ("BLK1666_4_source_weights", "single action scale/source current before calibration", "THM1229_1; PAL703_8", "SOURCE_WEIGHT_LOCK_OPEN", "Newton source side remains not derived"),
        ("BLK1666_5_coupling_double_zero", "complete C_i list with C_i(Phi0)=partial_A C_i(Phi0)=0", "DZ1473_4", "DOUBLE_ZERO_NOT_PARENT_DERIVED", "first-order non-EH coupling slopes may survive"),
        ("BLK1666_6_boundary_projector", "Q_X, P_loc, compact collar, edge terms", "VGC670_4; VTC938_3", "BOUNDARY_PROJECTOR_OPEN", "edge/source-measure residuals survive"),
        ("BLK1666_7_mode_absence", "no physical finite local mode or source charge", "CBA715_6", "NO_MODE_THEOREM_NOT_PROVED", "finite Yukawa/PPN/WEP branch remains live"),
        ("BLK1666_8_verdict", "all blockers closed", "1666 combined audit", "NOT_CLOSED_CURRENT_CORPUS", "must emit residual-bound handoff rows"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "missing_object": missing_object,
            "source_anchor": source_anchor,
            "status": status,
            "if_open": if_open,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, missing_object, source_anchor, status, if_open in rows
    ]


def residual_handoff_rows() -> list[dict[str, object]]:
    rows = [
        ("RBH1666_0_epsilon_frame_leak", "epsilon_frame_leak", f"{EPSILON_FRAME_LEAK_M1:.8e}", "m^-1", "frame/apparatus transfer", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1665_RETAINED_RESIDUALS.csv", "retain until apparatus/Fermi transfer is parent-signed"),
        ("RBH1666_1_Dq_leak", "Dq_Z_or_phi_leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "arena dependent", "quotient/readout leakage", "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv:DQT1505_8_acceptance", "needed for q/Phi visibility into matter/readout"),
        ("RBH1666_2_source_charge", "b_A_I_or_beta_source_test", "MISSING_NUMERIC_OR_THEOREM_ZERO", "dimensionless", "source/test matter coupling", "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv:MCD716_2_charge_definition", "needed for R10/WEP/PPN if source descent does not close"),
        ("RBH1666_3_frame_transfer_charge", "f_frame_a_I", "MISSING_NUMERIC_OR_THEOREM_ZERO", "dimensionless", "frame transfer charge", "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv:MCD716_3_frame_transfer", "apparent matter-blindness can fail through frame convention"),
        ("RBH1666_4_boundary_charge", "Q_X_or_B_X", "MISSING_NUMERIC_OR_THEOREM_ZERO", "charge/surface units by arena", "boundary/edge flux", "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv:VGC670_4_boundary_differentiability", "needed for alpha3/source-measure/orbital projections"),
        ("RBH1666_5_coupling_slope", "C_i(Phi0), partial_A_C_i(Phi0)", "MISSING_NUMERIC_OR_THEOREM_ZERO", "by coupling", "non-EH coupling double-zero", "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv:DZ1473_4_verdict", "needed to show first-order local residuals vanish"),
        ("RBH1666_6_mode_operator", "Z_X, M_X^2, lambda_X, K_X", "MISSING_NUMERIC_OR_THEOREM_ZERO", "by mode", "finite local mode branch", "P8_Y5_R10_715_COUPLING_BOTTLENECK_AUDIT.csv:CBA715_6_no_mode_theorem", "needed if no-mode theorem fails"),
        ("RBH1666_7_q_loc_unmatched", "q_loc_unmatched", "MISSING_GAMMA_OWNER + MISSING_KHAT_RESPONSE + MISSING_PLOC_TRANSFER", "symbolic", "local residual vector", "P8_Y5_PARENT_QLOC_1665_RETAINED_RESIDUALS.csv", "needed until Gamma/Khat/P_loc adoption closes"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "handoff_id": handoff_id,
            "residual_or_input": residual,
            "value_or_marker": value,
            "units": units,
            "arena_or_channel": channel,
            "source_anchor": source_anchor,
            "why_needed": why_needed,
            "status": "RETAINED_NONCLAIM_BOUND_INPUT",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for handoff_id, residual, value, units, channel, source_anchor, why_needed in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1666_0_packet", "MINIMAL_OBJECT_LANGUAGE_PACKET_WRITTEN", "the packet is now explicit enough to prevent hand-wavy coupling zero claims", "try to source q(Phi_parent) and Dq first"),
        ("DEC1666_1_theorem", "EXACT_CONDITIONAL_THEOREM_ONLY", "chain-rule/vertical-generator route is mathematically coherent but every key premise is unsigned", "do not promote local GR/Newton"),
        ("DEC1666_2_handoff", "RESIDUAL_BOUND_HANDOFF_EMITTED", "missing clauses are converted into explicit bound/source inputs", "future tests can bound rather than hide them"),
        ("DEC1666_3_best_next", "NEXT_Q_AND_DQ_FIELD_CHART", "q and Dq are the first domino: without them Z/phi cannot be gauge, matter descent cannot be checked, and coupling zero cannot be derived", "build parent field chart and quotient map or retain Dq leak"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1666_0_object_language_signed", "parent object-language packet is signed into MTS", False, "BLOCKED", "contract only; not parent-derived"),
        ("CG1666_1_q_Dq_closed", "q(Phi_parent) and Dq on Z/phi are computable and close", False, "BLOCKED", "q/Dq missing"),
        ("CG1666_2_vertical_generator_computed", "Omega/DCdagger gives actual vertical generator", False, "BLOCKED", "Omega/DC/field action missing"),
        ("CG1666_3_matter_source_coupling_zero", "ordinary matter/source/readout coupling vanishes to first order", False, "BLOCKED", "matter descent and source weights unsigned"),
        ("CG1666_4_boundary_projector_silence", "boundary/projector terms are zero or source-backed", False, "BLOCKED", "boundary/projector open"),
        ("CG1666_5_local_GR_Newton", "GR/Newton source and local q_loc reduction are derived", False, "NO_CLAIM", "conditional theorem only; residual handoff emitted"),
        ("CG1666_6_empirical_passes", "PPN/R10/WEP/clock/orbital passes follow", False, "NO_CLAIM", "no arena pass without theorem-zero or numeric residual bounds"),
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
            "next_target": "1667-Y5-R2FR-parent-field-chart-and-quotient-map-Dq-on-Zphi-or-retained-Dq-leak.md",
            "script": "scripts/Y5_R2FR_parent_field_chart_and_quotient_map_Dq_on_Zphi_or_retained_Dq_leak.py",
            "objective": "attempt the first domino of the coupling/vertical route: define the parent field chart and quotient q(Phi_parent), compute or explicitly fail Dq on Z/phi/residual directions, and emit retained Dq leak rows if the computation cannot be sourced",
            "success_condition": "either Z/phi directions become computably quotient-vertical/constraint-eliminated, or Dq leak becomes an explicit residual input for local tests",
            "forbidden_shortcuts": "no calling a visible residual gauge; no deleting Z/phi post-readout; no local GR/Newton/PPN/R10 claim; no GitHub action",
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
    packet: list[dict[str, object]],
    theorem: list[dict[str, object]],
    blockers: list[dict[str, object]],
    handoff: list[dict[str, object]],
    decisions: list[dict[str, object]],
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
        "1666-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1666",
        "P8_Y5_BRR545_1666",
        "JR1666",
        "Y5_R2FR_coupling_vertical_generator_parent_object_language",
    )
    formalization_dirty = (
        any(
            "1666" in path.name
            and any(marker in path.name for marker in generated_name_markers)
            for path in FORMALIZATION.rglob("*1666*")
        )
        if FORMALIZATION.exists()
        else False
    )
    packet_contract_only = any(row["packet_id"] == "OLP1666_7_packet_verdict" and row["status"] == "OBJECT_LANGUAGE_PACKET_CONTRACT_ONLY" for row in packet)
    theorem_conditional_only = any(row["theorem_id"] == "THM1666_5_verdict" and row["status"] == "CONDITIONAL_THEOREM_ONLY_NO_CLAIM" for row in theorem)
    blockers_not_closed = any(row["blocker_id"] == "BLK1666_8_verdict" and row["status"] == "NOT_CLOSED_CURRENT_CORPUS" for row in blockers)
    handoff_nonclaim = all(row["claim_allowed"] is False and row["valid_for_claim"] is False and row["valid_prediction_row"] is False for row in handoff)
    next_target_selected = next_targets[0]["next_target"] == "1667-Y5-R2FR-parent-field-chart-and-quotient-map-Dq-on-Zphi-or-retained-Dq-leak.md"

    checks = [
        ("VAL1666_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1666 source paths exist and needles are present"),
        ("VAL1666_1_packet_contract_only", packet_contract_only, "object-language packet is written but not parent-signed"),
        ("VAL1666_2_conditional_theorem_only", theorem_conditional_only, "conditional theorem is recorded without claim promotion"),
        ("VAL1666_3_blockers_not_closed", blockers_not_closed, "blocker matrix records current-corpus failure to close"),
        ("VAL1666_4_residual_handoff_nonclaim", handoff_nonclaim, "residual-bound handoff rows remain nonclaim and unscored"),
        ("VAL1666_5_decision_next_q_Dq", any(row["decision"] == "NEXT_Q_AND_DQ_FIELD_CHART" for row in decisions), "decision selects q/Dq as first domino"),
        ("VAL1666_6_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS local claims false"),
        ("VAL1666_7_next_target_selected", next_target_selected, "next target selects parent field chart and Dq on Z/phi"),
        ("VAL1666_8_csv_parse", generated_csv_parse, "all generated 1666 CSVs parse"),
        ("VAL1666_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1666 generated rows keep MTS claim/no-score flags false"),
        ("VAL1666_10_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1666_11_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1666_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1666_13_formalization_untouched", not formalization_dirty, "no 1666 outputs found under formalization-workbench"),
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
            "check_id": "VAL1666_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1666 coupling/vertical-generator parent object-language or residual-bound handoff validation",
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
    packet: list[dict[str, object]],
    theorem: list[dict[str, object]],
    blockers: list[dict[str, object]],
    handoff: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1666 - Coupling Vertical Generator Parent Object Language Or Residual Bound Handoff

**Private status:** object-language contract plus residual handoff. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The coupling/vertical-generator route is mathematically coherent, but not parent-signed in the current corpus.

```text
Good news:
DCdagger -> Omega-flat vertical-generator map is the right mathematical object.
The conditional chain-rule theorem is clean.
The minimal object-language packet is now explicit.

Bad news:
q(Phi_parent), Dq[Z/phi], parent Omega, field action, matter/source descent, and boundary/projector silence are still not sourced.
```

So `1666` does **not** claim local GR/Newton. It converts the missing pieces into an explicit residual-bound handoff. The first domino is now `q` and `Dq`: if we cannot compute whether `Z/phi` are quotient-vertical or constraint-eliminated, everything downstream is fog.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Object Language Packet

{markdown_table(packet, ["packet_id", "object_language_clause", "purpose", "current_evidence", "status"])}

## Conditional Theorem Attempt

{markdown_table(theorem, ["theorem_id", "statement", "proof_sketch", "status"])}

## Blocker Matrix

{markdown_table(blockers, ["blocker_id", "missing_object", "source_anchor", "status", "if_open"])}

## Residual Bound Handoff

{markdown_table(handoff, ["handoff_id", "residual_or_input", "value_or_marker", "units", "arena_or_channel", "why_needed"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is the cleanest route of attack now. We are not trying to “hammer” GR by declaration; we are asking for the same kind of structural reduction GR gave Newton: what are the parent variables, what is observable, what is gauge/representative, and what survives as a physical source? If `Dq[Z/phi]=0` or a constraint-first branch can be proved, the formal normal form becomes serious. If not, the residual-bound branch is already laid out without shame or sleight of hand.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    packet = object_language_rows()
    theorem = conditional_theorem_rows()
    blockers = blocker_rows()
    handoff = residual_handoff_rows()
    decisions = decision_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (OBJECT_LANGUAGE_PACKET, packet),
        (CONDITIONAL_THEOREM, theorem),
        (BLOCKER_MATRIX, blockers),
        (RESIDUAL_HANDOFF, handoff),
        (DECISION, decisions),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, packet, theorem, blockers, handoff, decisions, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, packet, theorem, blockers, handoff, decisions, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1666 validation failed; see P8_Y5_BRR545_1666_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1666 validation PASS")


if __name__ == "__main__":
    main()
