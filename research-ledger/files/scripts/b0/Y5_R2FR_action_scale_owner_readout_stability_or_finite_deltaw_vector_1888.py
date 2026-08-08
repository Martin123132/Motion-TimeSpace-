from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1888"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1888-Y5-R2FR-action-scale-owner-readout-stability-or-finite-deltaw-vector.md"

INPUTS = {
    "1887_doc": ROOT / "1887-Y5-R2FR-parent-object-language-typing-or-finite-source-weight-vector.md",
    "1887_validation": OUT / "P8_Y5_BRR545_1887_VALIDATION.csv",
    "1887_action_scale": OUT / "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv",
    "1887_vector_contract": OUT / "P8_Y5_PARENT_QLOC_1887_FINITE_SOURCE_WEIGHT_VECTOR_INTAKE_CONTRACT.csv",
    "1887_next": OUT / "P8_Y5_PARENT_QLOC_1887_NEXT_TARGET.csv",
    "1055_parent_contract": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1067_owner": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1067_hbar_measure": OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
    "1067_consequence": OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv",
    "1079_current_owner": OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1113_readout_contract": OUT / "P8_Y5_R10_1113_PARENT_OWNED_READOUT_DESCENT_CONTRACT.csv",
    "1113_signature": OUT / "P8_Y5_R10_1113_SIGNATURE_AUDIT.csv",
    "1220_signature": OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
    "1338_theorem": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "967_readout_schema": OUT / "P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
    "967_countermodel": OUT / "P8_Y5_R10_967_READOUT_COUNTERMODEL_AUDIT.csv",
    "950_source_norm": OUT / "P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
    "955_matter_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "1694_variation": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
    "1762_deltaw": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1491_delta_w_pack": OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1887_doc": ["ACTION_SCALE_OWNER_UNSIGNED", "SELECT_1888_ACTION_SCALE_OWNER_READOUT_STABILITY_OR_FINITE_DELTAW_VECTOR"],
    "1887_validation": ["VAL1887_OVERALL,PASS"],
    "1887_action_scale": ["ASN1887_5_verdict", "ACTION_SCALE_OWNER_UNSIGNED"],
    "1887_vector_contract": ["FSV1887_5_tau_arena", "FSV1887_6_K_Qbar_projection"],
    "1887_next": ["NEXT1887_0_primary", "do not absorb relative weights into G_N/GM"],
    "1055_parent_contract": ["PAC1055_5_radiative_readout_closure", "PAC1055_6_single_parent_action"],
    "1067_owner": ["ASO1067_2_path_integral_measure", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1067_hbar_measure": ["HMO1067_4_verdict", "OWNER_NOT_DERIVED"],
    "1067_consequence": ["SWC1067_1_relative_action_scale", "SWC1067_4_verdict"],
    "1079_current_owner": ["PR1079_4_no_pre_action_species_weight", "NOT_SIGNED"],
    "1107_exhaustion": ["EXH1107_5_radiative_readout", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
    "1113_readout_contract": ["POC1113_6_radiative_closure", "UNSIGNED_CRITICAL"],
    "1113_signature": ["SIG1113_0_contract_sufficiency", "NO_HIDDEN_VISIBLE_COEFFICIENT_MORPHISM"],
    "1220_signature": ["PTOL1220_4_action_scale_measure_owner", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
    "1338_theorem": ["OLT1338_4_action_scale_owner", "NOT_DERIVED_CURRENT_CORPUS"],
    "967_readout_schema": ["RAV967_5_verdict", "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED"],
    "967_countermodel": ["RCM967_0_reduced_EFT", "RCM967_4_hidden_marker_return"],
    "950_source_norm": ["SNL950_4_countermodel", "SNL950_5_verdict"],
    "955_matter_lemma": ["MMA955_3_relative_prefactor", "MMA955_6_verdict"],
    "1694_variation": ["VAR1694_1_Hilbert_source", "VAR1694_5_identity_verdict"],
    "1762_deltaw": ["DW1762_0_zero_condition", "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO"],
    "1491_delta_w_pack": ["DWI1491_0_core_model", "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED"],
    "local_bounds": ["R1_WEP_source_charge", "2.8e-15"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1888_SOURCE_REGISTER.csv",
    "action_owner_attempt": OUT / "P8_Y5_PARENT_QLOC_1888_ACTION_SCALE_OWNER_PROOF_ATTEMPT.csv",
    "readout_attempt": OUT / "P8_Y5_PARENT_QLOC_1888_READOUT_STABILITY_PROOF_ATTEMPT.csv",
    "combined_contract": OUT / "P8_Y5_PARENT_QLOC_1888_COMBINED_ZERO_THEOREM_CONTRACT.csv",
    "finite_intake": OUT / "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1888_DELTAW_VECTOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1888_DELTAW_VECTOR_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1888_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1888_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1888_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1888_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1888_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1888_VALIDATION.csv",
}

SOURCE_WEIGHT_TEMPLATE_COPY = SOURCE_WEIGHT_DOCS / "DELTAW_VECTOR1888_ROW_INTAKE_NONCLAIM.csv"


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def is_placeholder(value: Any) -> bool:
    text = str(value).strip().upper()
    return not text or any(marker in text for marker in ("MISSING", "PLACEHOLDER", "TBD", "UNSIGNED", "BLOCKED"))


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_status": "PASS" if ok else "FAIL",
                "needle_detail": detail,
                "required_needles": "; ".join(SOURCE_NEEDLES[source_id]),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def action_owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_0_target",
            "claim": "one parent action-scale/measure owner removes relative species weights",
            "formal_statement": "S_parent/hbar_parent contains one ordinary matter functor sum_A S_A with no species-dependent w_A and no species-dependent measure Jacobian J_A",
            "attempt_result": "TARGET_EXACT",
            "missing_for_claim": "parent derivation of hbar_parent, common measure, current owner, and species-blind measure descent",
            "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_0_target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_1_classical_eom_not_enough",
            "claim": "constant species prefactors are removable because EOM divide by w_A",
            "formal_statement": "delta(w_A S_A)/delta Psi_A=w_A E_A can leave classical matter equations unchanged, while delta(w_A S_A)/delta g_obs=w_A T_A",
            "attempt_result": "FALSE_POSITIVE_REJECTED",
            "missing_for_claim": "source variation must be owned, not inferred from classical EOM shape",
            "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_0_matter_EOM;VAR1694_1_Hilbert_source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_2_path_integral_measure",
            "claim": "relative action weights are gauge in the quantum/statistical measure",
            "formal_statement": "exp(i sum_A w_A S_A/hbar_parent) is equivalent to exp(i sum_A S_A/hbar_parent) only if the parent measure quotients all relative w_A",
            "attempt_result": "MEASURE_OWNER_REQUIRED_NOT_DERIVED",
            "missing_for_claim": "single hbar_parent plus species-blind path-integral/statistical measure theorem",
            "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_2_path_integral_measure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_3_field_redefinition_limit",
            "claim": "field rescaling removes source-only action weights",
            "formal_statement": "canonical rescaling must preserve interactions, measured nongravitational constants, composite material parameters, Hilbert source, and the quantum measure simultaneously",
            "attempt_result": "NOT_CLOSED_BY_RESCALING",
            "missing_for_claim": "explicit parent field-normalization quotient compatible with currents, material readout, and source variation",
            "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_3_field_redefinition_limit;P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv:MMA955_4_field_rescaling_limit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_4_common_mode_guard",
            "claim": "calibrating G_N or GM removes source-weight residuals",
            "formal_statement": "only w_A=w_common with partial_X w_common=0 is common calibration; Delta_w_AB or beta_w,A remains after calibration",
            "attempt_result": "COMMON_MODE_ONLY_GUARDED",
            "missing_for_claim": "relative modes need theorem-zero or source-backed finite vector rows",
            "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_3_common_mode;VAR1694_4_relative_mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_5_current_owner",
            "claim": "single Hilbert/current owner blocks later source rescaling",
            "formal_statement": "variation before readout plus no post-variation current rescale would block J_A -> c_A J_A and source-only w_A",
            "attempt_result": "CURRENT_OWNER_PARTIAL_NO_PRE_ACTION_WEIGHT_UNSIGNED",
            "missing_for_claim": "PR1079_4 no-pre-action species weight is not signed",
            "source_anchor": "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv:PR1079_3_no_later_current_rescale;PR1079_4_no_pre_action_species_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_6_countermodel",
            "claim": "covariance/additivity/Ward symmetry forbid relative source weights",
            "formal_statement": "S_matter=sum_A w_A S_A is covariant and additive and can conserve total stress, while changing relative Hilbert source weights",
            "attempt_result": "COUNTERMODEL_SURVIVES",
            "missing_for_claim": "parent object-language/action-scale no-slot theorem or finite coefficient bound",
            "source_anchor": "P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv:SNL950_4_countermodel;P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv:MMA955_3_relative_prefactor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ASO1888_7_verdict",
            "claim": "action-scale owner proves Delta_w=beta_w=w_R=0",
            "formal_statement": "single hbar/action measure + species-blind Jacobian + current owner + no pre-action species weight => all relative source weights are absent or pure common mode",
            "attempt_result": "ACTION_SCALE_OWNER_NOT_DERIVED",
            "missing_for_claim": "hbar/action-measure owner, current owner, and species-blind measure descent remain unsigned",
            "source_anchor": "ASO1888_0 through ASO1888_6",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def readout_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ROS1888_0_target",
            "claim": "readout cannot regenerate source/action weights after variation",
            "formal_statement": "R_read: Sol(S_parent)->Obs is not an argument of S_parent; S_eff/readout maps preserve quotient-generated coefficient domains",
            "attempt_result": "TARGET_EXACT",
            "missing_for_claim": "global parent action domain exclusion plus radiative/readout closure",
            "source_anchor": "P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv:RAV967_0_domain_separation;P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_5_radiative_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ROS1888_1_domain_separation",
            "claim": "readout-after-variation is variationally silent",
            "formal_statement": "if readout variables are not in Conf_parent, no variational derivative with respect to them exists",
            "attempt_result": "CONDITIONAL_SCHEMA_THEOREM",
            "missing_for_claim": "corpus-wide parent schema must exclude readout variables and reduced-action backreaction",
            "source_anchor": "P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv:RAV967_1_no_variation_slot;RAV967_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ROS1888_2_reduced_action_tax",
            "claim": "a readout-reduced action can still be counted as parent-zero",
            "formal_statement": "S_red[P_read Phi] defines a different EFT branch and must pay residual/variation tax",
            "attempt_result": "COUNTERMODEL_RETAINED_AS_EFT_BRANCH",
            "missing_for_claim": "no-cheat rule must be applied: varied reduced actions are not theorem-zero evidence",
            "source_anchor": "P8_Y5_R10_967_READOUT_COUNTERMODEL_AUDIT.csv:RCM967_0_reduced_EFT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ROS1888_3_hidden_marker_return",
            "claim": "readout labels cannot reintroduce material/source markers",
            "formal_statement": "hidden marker/domain/readout labels must not enter S_parent before readout or be retyped as coefficient arguments",
            "attempt_result": "NO_MARKER_STILL_REQUIRED",
            "missing_for_claim": "primitive no-marker theorem or finite marker/readout coefficient rows",
            "source_anchor": "P8_Y5_R10_967_READOUT_COUNTERMODEL_AUDIT.csv:RCM967_4_hidden_marker_return",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ROS1888_4_radiative_closure",
            "claim": "loops/EFT/readout preserve source-weight exclusion",
            "formal_statement": "S_vis^eff and clock/WEP/R10 readouts remain in Alg[q_loc,Theta_rep,Level_EM] with no generated C_hid -> Coeff_source morphisms",
            "attempt_result": "UNSIGNED_CRITICAL",
            "missing_for_claim": "radiative/readout theorem or explicit finite transfer priors",
            "source_anchor": "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv:PAC1055_5_radiative_readout_closure;P8_Y5_R10_1113_PARENT_OWNED_READOUT_DESCENT_CONTRACT.csv:POC1113_6_radiative_closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ROS1888_5_no_hidden_visible_morphism",
            "claim": "hidden representatives cannot feed visible/source coefficients",
            "formal_statement": "Hom(C_hid,Coeff(O_vis/source)) is constant or absent, so hidden invariants cannot become w_A, beta_w, alpha/mass, or readout coefficients",
            "attempt_result": "BEST_DERIVATION_NEEDLE_NOT_SIGNED",
            "missing_for_claim": "no-hidden-visible coefficient morphism theorem",
            "source_anchor": "P8_Y5_R10_1113_SIGNATURE_AUDIT.csv:SIG1113_2_best_derivation_needle",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ROS1888_6_verdict",
            "claim": "readout/radiative stability preserves action-scale zero",
            "formal_statement": "readout-after-variation plus S_eff domain preservation prevents relative source weights from regenerating downstream",
            "attempt_result": "READOUT_STABILITY_NOT_PARENT_DERIVED",
            "missing_for_claim": "readout domain is conditional and radiative closure/no-hidden-visible morphism remain unsigned",
            "source_anchor": "ROS1888_0 through ROS1888_5",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def combined_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "ZTH1888_0_parent_action_domain",
            "zero_clause": "Conf_parent excludes readout/reduced-action knobs and contains one ordinary matter functor",
            "required_signature": "S_parent = S_geom + S_hidden + S_EM[q,A_Q,theta] + sum_A S_A[Psi_A,e_obs(q),A_Q,theta_A] + S_boundary[q]",
            "if_signed": "post-hoc source/readout closures cannot be inserted into theorem-zero proof",
            "current_status": "SCHEMA_WRITTEN_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZTH1888_1_action_measure_owner",
            "zero_clause": "one hbar/action measure/Jacobian owner for all ordinary species",
            "required_signature": "hbar_parent and Dmu_parent are universal or species-blind; no J_A source-only measure factor",
            "if_signed": "relative w_A cannot hide in quantum/statistical normalization",
            "current_status": "OWNER_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZTH1888_2_current_owner",
            "zero_clause": "variation before readout and no post-variation current/source rescale",
            "required_signature": "T_total and source current are the Hilbert/coframe variation of the same matter action",
            "if_signed": "J_A -> c_A J_A and post-readout source masks are barred",
            "current_status": "NO_PRE_ACTION_SPECIES_WEIGHT_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZTH1888_3_no_hidden_visible_morphism",
            "zero_clause": "hidden/marker/readout labels cannot target source coefficient spaces",
            "required_signature": "Hom(C_hid or Marker, Coeff_active_source) is absent or constant",
            "if_signed": "w_A(I_hid), beta_w(I_hid), and marker source weights are ill-typed",
            "current_status": "UNSIGNED_CRITICAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZTH1888_4_readout_radiative_closure",
            "zero_clause": "S_eff and observational readouts preserve the parent-generated coefficient domain",
            "required_signature": "loops, thresholds, clocks, WEP/R10 projections and local readouts do not create new source coefficient arguments",
            "if_signed": "tree-level source silence survives actual tests",
            "current_status": "READOUT_RADIATIVE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZTH1888_5_zero_consequence",
            "zero_clause": "Delta_w=beta_w_source=beta_w_test=w_R=0 after common-mode calibration",
            "required_signature": "ZTH1888_0 through ZTH1888_4 all parent-signed",
            "if_signed": "source-side local GR/Newton branch can advance to left-hand EH/Bianchi gates",
            "current_status": "CONDITIONAL_ZERO_NOT_CLAIMED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_intake_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FDV1888_0_core_vector",
            "arena": "core",
            "symbol": "Delta_w_vector",
            "required_input": "dimensionless source-weight component vector with declared basis and common-mode projection",
            "current_value": "MISSING_PARENT_COMPONENT_BASIS",
            "units": "dimensionless",
            "formula": "w_A=w_common(1+sum_i Q_Ai Delta_w_i); common mode projected out",
            "source_path": str(INPUTS["1762_deltaw"]),
            "source_anchor": "DW1762_1_delta_w_A",
            "missing_for_claim": "component basis, norm, no-cancellation convention, parent coefficient origin",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FDV1888_1_beta_w_source_test",
            "arena": "R10_PPN_finite_exchange",
            "symbol": "beta_w_source; beta_w_test",
            "required_input": "partial_X ln w_source and partial_X ln w_test in canonical Xhat convention",
            "current_value": "MISSING_CANONICAL_SOURCE_TEST_LEGS",
            "units": "canonical_X_inverse_or_dimensionless_declared",
            "formula": "A_exchange <= K(lambda)(|beta_w_source|+|beta_w_test|+||Delta_w||)",
            "source_path": str(INPUTS["1887_vector_contract"]),
            "source_anchor": "FSV1887_3_beta_w_source_test",
            "missing_for_claim": "Xhat normalization, source/test split, K(lambda), product law",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FDV1888_2_WEP_MICROSCOPE",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "Delta_w_TiPt_projection",
            "required_input": "DeltaQ_TiPt dot Delta_w times tau_WEP with official material/source/readout tensor",
            "current_value": "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
            "units": "dimensionless_eta",
            "formula": "|eta_TiPt| <= |DeltaQ_TiPt dot Delta_w| |tau_WEP|",
            "source_path": str(INPUTS["local_bounds"]),
            "source_anchor": "R1_WEP_source_charge; 2.8e-15",
            "missing_for_claim": "official readout arrays, Earth/source worldtube, full material tensor, tau_WEP, parent Delta_w",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FDV1888_3_R10",
            "arena": "R10_short_range",
            "symbol": "alpha_delta_w(lambda)",
            "required_input": "K_R10(lambda), Qbar_source_test(lambda), tau_R10(lambda), Delta_w vector",
            "current_value": "SYMBOLIC_ANCHOR_ONLY_CURVE_KERNEL_MISSING",
            "units": "alpha(lambda)",
            "formula": "alpha_delta_w(lambda)=K_R10(lambda) Qbar_source_test(lambda).Delta_w",
            "source_path": str(INPUTS["1491_delta_w_pack"]),
            "source_anchor": "DWI1491_3_R10",
            "missing_for_claim": "digitized bound curve, Yukawa/non-Yukawa kernel convention, source/test geometry, parent vector",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FDV1888_4_clock",
            "arena": "clock_alpha_mass",
            "symbol": "Delta_w_clock_product",
            "required_input": "clock readout kernel that maps source-weight vector into alpha/mass drift product",
            "current_value": "PRODUCT_BOUND_AVAILABLE_PROJECTION_BLOCKED",
            "units": "yr^-1_or_declared",
            "formula": "|clock product| <= |K_clock dot Delta_w| |tau_clock|",
            "source_path": str(INPUTS["1491_delta_w_pack"]),
            "source_anchor": "DWI1491_4_clock",
            "missing_for_claim": "tau_clock, alpha/mass split, clock readout kernel, no cross-arena transfer shortcut",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FDV1888_5_orbital",
            "arena": "orbital_GM_time_drift",
            "symbol": "Delta_w_orbital",
            "required_input": "source body composition/worldtube projection from Delta_w to measured GM convention",
            "current_value": "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
            "units": "yr^-1_or_declared",
            "formula": "|d ln GM/dt| <= |K_orbital dot Delta_w| |tau_orbital|",
            "source_path": str(INPUTS["1491_delta_w_pack"]),
            "source_anchor": "DWI1491_5_orbital",
            "missing_for_claim": "source body composition, worldtube/Gauss bridge, measured GM convention, orbital residual projection",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1888_0_parent_zero_unsigned",
            "route_type": "combined_zero_theorem",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": False,
            "parent_vector_present": False,
            "tau_present": False,
            "K_projection_present": False,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_ZERO_THEOREM_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_1_action_owner_only",
            "route_type": "combined_zero_theorem",
            "action_owner_signed": True,
            "readout_stability_signed": False,
            "component_basis_present": False,
            "parent_vector_present": False,
            "tau_present": False,
            "K_projection_present": False,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_READOUT_STABILITY_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_2_bound_anchor",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": False,
            "parent_vector_present": False,
            "tau_present": False,
            "K_projection_present": False,
            "uses_bound_anchor_as_prediction": True,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_3_missing_basis",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": False,
            "parent_vector_present": True,
            "tau_present": True,
            "K_projection_present": True,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_MISSING_COMPONENT_BASIS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_4_missing_parent_vector",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": True,
            "parent_vector_present": False,
            "tau_present": True,
            "K_projection_present": True,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_MISSING_PARENT_DELTAW_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_5_missing_tau",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": True,
            "parent_vector_present": True,
            "tau_present": False,
            "K_projection_present": True,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_MISSING_TAU_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_6_missing_K_projection",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": True,
            "parent_vector_present": True,
            "tau_present": True,
            "K_projection_present": False,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_MISSING_K_QBAR_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_7_G_absorption",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": True,
            "parent_vector_present": True,
            "tau_present": True,
            "K_projection_present": True,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": True,
            "uses_cancellation": False,
            "schema_only": False,
            "expected_status": "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_8_cancellation",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": True,
            "parent_vector_present": True,
            "tau_present": True,
            "K_projection_present": True,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": True,
            "schema_only": False,
            "expected_status": "REFUSED_CANCELLATION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1888_9_schema_only",
            "route_type": "finite_deltaw_vector",
            "action_owner_signed": False,
            "readout_stability_signed": False,
            "component_basis_present": True,
            "parent_vector_present": True,
            "tau_present": True,
            "K_projection_present": True,
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "uses_cancellation": False,
            "schema_only": True,
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if row["route_type"] == "combined_zero_theorem" and bool_string(row["action_owner_signed"]) != "true":
        status = "REFUSED_ZERO_THEOREM_UNSIGNED"
        detail = "action-scale owner is not parent-signed"
    elif row["route_type"] == "combined_zero_theorem" and bool_string(row["readout_stability_signed"]) != "true":
        status = "REFUSED_READOUT_STABILITY_UNSIGNED"
        detail = "readout/radiative stability is not parent-signed"
    elif bool_string(row["uses_bound_anchor_as_prediction"]) == "true":
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
        detail = "experimental bound is not a parent Delta_w vector"
    elif bool_string(row["component_basis_present"]) != "true":
        status = "REFUSED_MISSING_COMPONENT_BASIS"
        detail = "finite Delta_w vector lacks declared basis"
    elif bool_string(row["parent_vector_present"]) != "true":
        status = "REFUSED_MISSING_PARENT_DELTAW_VECTOR"
        detail = "component basis without parent-predicted coefficients is not score-ready"
    elif bool_string(row["tau_present"]) != "true":
        status = "REFUSED_MISSING_TAU_PROJECTION"
        detail = "arena projection/readout tau is missing"
    elif bool_string(row["K_projection_present"]) != "true":
        status = "REFUSED_MISSING_K_QBAR_PROJECTION"
        detail = "K/Qbar/material projection is missing"
    elif bool_string(row["uses_G_absorption"]) == "true":
        status = "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"
        detail = "relative source weights cannot be hidden in calibrated G"
    elif bool_string(row["uses_cancellation"]) == "true":
        status = "REFUSED_CANCELLATION_ONLY"
        detail = "finite vector cancellation requires a parent identity"
    elif bool_string(row["schema_only"]) == "true":
        status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
        detail = "schema math can be exercised but not claimed"
    else:
        status = "REFUSED_UNCLASSIFIED_NONCLAIM"
        detail = "case remains nonclaim"
    return {
        **row,
        "observed_status": status,
        "status_detail": detail,
        "status_matches_expected": status == row["expected_status"],
        "valid_prediction_row": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def dryrun_result_rows() -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in dryrun_case_rows()]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1888_0_combined_zero",
            "input_kind": "combined_zero_theorem",
            "runner_status": "REFUSED_ACTION_SCALE_AND_READOUT_UNSIGNED",
            "reason": "ZTH1888 clauses are exact but not parent-signed",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1888_1_finite_Delta_w",
            "input_kind": "finite_deltaw_vector",
            "runner_status": "REFUSED_MISSING_PARENT_VECTOR_AND_PROJECTIONS",
            "reason": "FDV1888 rows lack component basis, parent coefficients, tau, and K/Qbar projections",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1888_2_bound_anchors",
            "input_kind": "MICROSCOPE_R10_clock_orbital_bounds",
            "runner_status": "REFUSED_BOUND_ANCHORS_NOT_PREDICTIONS",
            "reason": "bounds are useful pressure but not MTS coefficient predictions",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE1888_0_action_scale_owner",
            "claim": "relative action/source weights are gauge or forbidden",
            "required": "single hbar/action measure, species-blind Jacobian, current owner, no pre-action species weight",
            "current_status": "BLOCKED_ACTION_SCALE_OWNER_NOT_DERIVED",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1888_1_readout_stability",
            "claim": "readout/radiative maps cannot regenerate source weights",
            "required": "domain separation, reduced-action tax, no hidden-visible morphism, radiative closure",
            "current_status": "BLOCKED_READOUT_STABILITY_NOT_PARENT_DERIVED",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1888_2_finite_vector_score",
            "claim": "finite Delta_w vector scores WEP/R10/PPN/clock/orbital branches",
            "required": "basis, parent Delta_w, beta_w legs, w_R, tau, K/Qbar/material projections, source paths",
            "current_status": "BLOCKED_MISSING_PARENT_VECTOR_AND_ARENA_PROJECTIONS",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1888_3_local_GR",
            "claim": "local GR/Newton source-side reduction",
            "required": "combined zero theorem or all finite residuals below local bounds with no hidden cancellation",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1888_0_action_scale_route",
            "question": "can action-scale owner alone prove w_A impossible?",
            "answer": "no",
            "basis": "relative weights survive classical EOM, rescaling, covariance, and Ward-style checks unless measure/current owner is parent-signed",
            "decision": "RETAIN_AS_CONDITIONAL_ZERO_CONTRACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1888_1_readout_route",
            "question": "can readout-after-variation alone protect the zero?",
            "answer": "no",
            "basis": "domain separation is clean but reduced EFT, hidden marker return, and radiative closure remain unsigned",
            "decision": "RETAIN_READOUT_STABILITY_AS_REQUIRED_CLAUSE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1888_2_finite_route",
            "question": "can finite Delta_w rows score now?",
            "answer": "no",
            "basis": "current rows are source-ready ledgers, not predictions; parent vector and projection kernels are missing",
            "decision": "STAGE_FINITE_DELTAW_INTAKE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1888_3_next_attack",
            "question": "what is the best next narrow theorem?",
            "answer": "source-current Ward owner plus real component-basis fallback",
            "basis": "the remaining wound is exactly the owner of T_total/J_source and whether later or earlier source rescaling is impossible",
            "decision": "SELECT_1889_SOURCE_CURRENT_WARD_OWNER_OR_REAL_DELTAW_COMPONENT_BASIS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1888_0_primary",
            "selection_status": "selected",
            "target_doc": "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md",
            "target_script": "scripts/Y5_R2FR_source_current_Ward_owner_or_real_deltaw_component_basis_1889.py",
            "objective": "try to derive the parent source-current Ward owner that makes T_total/J_source species-blind before and after readout; if it fails, build a real nonclaim Delta_w component-basis acquisition pack for WEP/R10/PPN/clock/orbital projections",
            "success_condition": "parent-signed source-current owner/no-rescale theorem, or strict sourced component-basis rows with no bound-anchor shortcut and no G absorption",
            "do_not": "do not claim local GR, do not use Ward conservation of the total current as species-blindness, do not set tau=1, and do not treat MICROSCOPE/R10 bounds as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS1888_0_progress",
            "area": "derivation spine",
            "status": "combined zero theorem contract sharpened",
            "detail": "we now know exactly which signed clauses would turn source weights into theorem-zero rather than closure",
            "risk_level": "USEFUL_PROGRESS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1888_1_main_bottleneck",
            "area": "source-current/action-measure owner",
            "status": "unsigned",
            "detail": "relative action/source weights survive unless hbar/measure/current owner and no pre-action species weight are parent-derived",
            "risk_level": "MAIN_BOTTLENECK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1888_2_fallback",
            "area": "finite Delta_w testing",
            "status": "source-ready but not score-ready",
            "detail": "the finite branch has clear input slots but still lacks parent vector and arena projections",
            "risk_level": "BLOCKED_FOR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "action_owner_attempt": action_owner_attempt_rows(),
        "readout_attempt": readout_attempt_rows(),
        "combined_contract": combined_contract_rows(),
        "finite_intake": finite_intake_rows(),
        "dryrun_cases": dryrun_case_rows(),
        "dryrun_results": dryrun_result_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
        except Exception as exc:  # noqa: BLE001
            return False, f"{path.name}:{exc}"
        details.append(f"{path.name}:{len(rows)}")
    return True, "; ".join(details)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    for path in paths:
        for row in csv_rows(path):
            for field in ("valid_for_claim", "claim_allowed"):
                if field in row and bool_string(row[field]) == "true":
                    return False, f"{path.name}:{field}=true"
    return True, "all claim flags false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            joined = " ".join(row.values()).upper()
            if any(marker in joined for marker in ("MISSING", "UNSIGNED", "BLOCKED", "NOT_DERIVED")):
                if bool_string(row.get("score_ready", "false")) == "true" or bool_string(row.get("valid_for_claim", "false")) == "true":
                    return False, f"{path.name}:row{index}:blocked marker marked ready"
    return True, "blocked-marker rows are not claim-ready"


def copy_branch_artifacts() -> None:
    shutil.copy2(OUTPUTS["action_owner_attempt"], MICROSCOPE_RESIDUALS / OUTPUTS["action_owner_attempt"].name)
    shutil.copy2(OUTPUTS["readout_attempt"], QUEUE / "JR1888_READOUT_STABILITY_PROOF_ATTEMPT_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["combined_contract"], QUEUE / "JR1888_COMBINED_ZERO_THEOREM_CONTRACT_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["finite_intake"], SOURCE_WEIGHT_TEMPLATE_COPY)
    shutil.copy2(OUTPUTS["dryrun_results"], QUARANTINE / OUTPUTS["dryrun_results"].name)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    source_rows = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1888_0_sources_exist",
            "status": "PASS" if all(bool_string(row["exists"]) == "true" for row in source_rows) else "FAIL",
            "detail": f"{sum(bool_string(row['exists']) == 'true' for row in source_rows)}/{len(source_rows)} sources exist",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1888_1_needles_found",
            "status": "PASS" if all(row["needle_status"] == "PASS" for row in source_rows) else "FAIL",
            "detail": f"{sum(row['needle_status'] == 'PASS' for row in source_rows)}/{len(source_rows)} source needles found",
            "valid_for_claim": False,
        }
    )

    action_rows = csv_rows(OUTPUTS["action_owner_attempt"])
    checks.append(
        {
            "validation_id": "VAL1888_2_action_owner_not_promoted",
            "status": "PASS"
            if any(row["attempt_id"] == "ASO1888_7_verdict" and row["attempt_result"] == "ACTION_SCALE_OWNER_NOT_DERIVED" for row in action_rows)
            else "FAIL",
            "detail": "action-scale owner remains conditional, not claim",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1888_3_countermodel_retained",
            "status": "PASS" if any(row["attempt_result"] == "COUNTERMODEL_SURVIVES" for row in action_rows) else "FAIL",
            "detail": "relative source-weight countermodel remains explicit",
            "valid_for_claim": False,
        }
    )

    readout_rows = csv_rows(OUTPUTS["readout_attempt"])
    checks.append(
        {
            "validation_id": "VAL1888_4_readout_not_promoted",
            "status": "PASS"
            if any(row["attempt_id"] == "ROS1888_6_verdict" and row["attempt_result"] == "READOUT_STABILITY_NOT_PARENT_DERIVED" for row in readout_rows)
            else "FAIL",
            "detail": "readout/radiative stability remains conditional",
            "valid_for_claim": False,
        }
    )

    contract_rows = csv_rows(OUTPUTS["combined_contract"])
    checks.append(
        {
            "validation_id": "VAL1888_5_combined_zero_contract",
            "status": "PASS"
            if any(row["contract_id"] == "ZTH1888_5_zero_consequence" and row["current_status"] == "CONDITIONAL_ZERO_NOT_CLAIMED" for row in contract_rows)
            else "FAIL",
            "detail": "combined zero theorem contract written but not claimed",
            "valid_for_claim": False,
        }
    )

    intake_rows = csv_rows(OUTPUTS["finite_intake"])
    checks.append(
        {
            "validation_id": "VAL1888_6_finite_intake_nonclaim",
            "status": "PASS"
            if all(bool_string(row["score_ready"]) == "false" and bool_string(row["valid_for_claim"]) == "false" for row in intake_rows)
            else "FAIL",
            "detail": f"finite_intake_rows={len(intake_rows)} all nonclaim",
            "valid_for_claim": False,
        }
    )

    dryrun_rows = csv_rows(OUTPUTS["dryrun_results"])
    expected_statuses = {
        "REFUSED_ZERO_THEOREM_UNSIGNED",
        "REFUSED_READOUT_STABILITY_UNSIGNED",
        "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
        "REFUSED_MISSING_COMPONENT_BASIS",
        "REFUSED_MISSING_PARENT_DELTAW_VECTOR",
        "REFUSED_MISSING_TAU_PROJECTION",
        "REFUSED_MISSING_K_QBAR_PROJECTION",
        "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    observed_statuses = {row["observed_status"] for row in dryrun_rows}
    checks.append(
        {
            "validation_id": "VAL1888_7_dryrun_failure_modes",
            "status": "PASS"
            if expected_statuses.issubset(observed_statuses) and all(bool_string(row["status_matches_expected"]) == "true" for row in dryrun_rows)
            else "FAIL",
            "detail": "dryrun_statuses=" + ",".join(row["observed_status"] for row in dryrun_rows),
            "valid_for_claim": False,
        }
    )

    runner_rows = csv_rows(OUTPUTS["runner_refusal"])
    checks.append(
        {
            "validation_id": "VAL1888_8_runner_refusal",
            "status": "PASS" if all(bool_string(row["score_ready"]) == "false" for row in runner_rows) else "FAIL",
            "detail": "all runners refuse claim scoring",
            "valid_for_claim": False,
        }
    )

    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1888_9_claim_gates",
            "status": "PASS" if all(bool_string(row["pass_gate"]) == "false" for row in gate_rows) else "FAIL",
            "detail": "all claim gates remain blocked",
            "valid_for_claim": False,
        }
    )

    decision_rows_loaded = csv_rows(OUTPUTS["decision"])
    checks.append(
        {
            "validation_id": "VAL1888_10_decision",
            "status": "PASS"
            if any(row["decision"] == "SELECT_1889_SOURCE_CURRENT_WARD_OWNER_OR_REAL_DELTAW_COMPONENT_BASIS" for row in decision_rows_loaded)
            else "FAIL",
            "detail": "decision selects source-current Ward owner or real Delta_w component basis next",
            "valid_for_claim": False,
        }
    )

    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1888_11_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1888_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1889 source-current Ward owner/component basis selected",
            "valid_for_claim": False,
        }
    )

    status_rows = csv_rows(OUTPUTS["project_status"])
    checks.append(
        {
            "validation_id": "VAL1888_12_project_status",
            "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows) else "FAIL",
            "detail": "project status snapshot keeps source-current/action-measure owner as main bottleneck",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1888_13_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1888_14_blocked_markers_not_ready",
            "status": "PASS" if blocked_ok else "FAIL",
            "detail": blocked_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1888_15_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["action_owner_attempt"].name,
        QUEUE / "JR1888_READOUT_STABILITY_PROOF_ATTEMPT_NONCLAIM.csv",
        QUEUE / "JR1888_COMBINED_ZERO_THEOREM_CONTRACT_NONCLAIM.csv",
        SOURCE_WEIGHT_TEMPLATE_COPY,
        QUARANTINE / OUTPUTS["dryrun_results"].name,
    ]
    checks.append(
        {
            "validation_id": "VAL1888_16_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1888_17_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1888*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1888_18_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1888_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1888_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1888 action-scale owner/readout stability or finite Delta_w vector",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1888 - Action-Scale Owner Readout Stability Or Finite Delta_w Vector

**Private status:** derivation-first local-GR source-side checkpoint; no WEP/R10/PPN/local-GR claim.

## Result

1888 tried the cleanest theorem route:

```text
single parent action scale + species-blind measure/current owner
+ readout-after-variation + radiative/readout domain stability
=> Delta_w = beta_w_source = beta_w_test = w_R = 0
```

The theorem is mathematically sharp as a contract, but it still does not close from the present corpus. The obstruction is not vague anymore:

```text
delta(w_A S_A)/delta Psi_A may look ordinary,
but delta(w_A S_A)/delta g_obs = w_A T_A
and exp(i sum_A w_A S_A/hbar_parent) is not equivalent without a parent measure theorem.
```

So the source-side GR/Newton path is alive but conditional. The finite `Delta_w` fallback is also now sharply typed: it needs a real component basis, a parent coefficient vector, source/test legs, `tau`, `K/Qbar`, material projections, and source paths. Bounds remain pressure only.

## Action-Scale Owner Proof Attempt

{markdown_table(rows_by_name["action_owner_attempt"])}

## Readout Stability Proof Attempt

{markdown_table(rows_by_name["readout_attempt"])}

## Combined Zero Theorem Contract

{markdown_table(rows_by_name["combined_contract"])}

## Finite Delta_w Vector Row Intake

{markdown_table(rows_by_name["finite_intake"])}

## Delta_w Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Delta_w Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
