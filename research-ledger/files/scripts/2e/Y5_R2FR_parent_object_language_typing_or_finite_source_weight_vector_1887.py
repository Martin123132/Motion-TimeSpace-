from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1887"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1887-Y5-R2FR-parent-object-language-typing-or-finite-source-weight-vector.md"

INPUTS = {
    "1886_doc": ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
    "1886_validation": OUT / "P8_Y5_BRR545_1886_VALIDATION.csv",
    "1886_no_slot": OUT / "P8_Y5_PARENT_QLOC_1886_NO_SOURCE_ONLY_SLOT_PROOF_AUDIT.csv",
    "1886_signature": OUT / "P8_Y5_PARENT_QLOC_1886_COMMON_MATTER_SIGNATURE_CONTRACT.csv",
    "1886_finite_contract": OUT / "P8_Y5_PARENT_QLOC_1886_FINITE_WR_BETAW_ROW_CONTRACT.csv",
    "1886_next": OUT / "P8_Y5_PARENT_QLOC_1886_NEXT_TARGET.csv",
    "1066_typing": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1078_proof": OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1338_theorem": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1676_no_marker": OUT / "P8_Y5_PARENT_QLOC_1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT.csv",
    "1867_radial_cell": OUT / "P8_Y5_PARENT_QLOC_1867_OBJECT_LANGUAGE_DERIVATION_ATTEMPT.csv",
    "1694_variation": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
    "1762_deltaw": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1491_delta_w_pack": OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1886_doc": [
        "Allowed[S_matter] excludes w_A(X)S_A",
        "WEP/MICROSCOPE bound anchors are pressure only",
    ],
    "1886_validation": [
        "VAL1886_OVERALL,PASS",
    ],
    "1886_no_slot": [
        "NSS1886_7_verdict",
        "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED",
    ],
    "1886_signature": [
        "CMS1886_1_no_source_only_weight",
        "SIGNATURE_NOT_DERIVED",
    ],
    "1886_finite_contract": [
        "FWR1886_4_tau_projection",
        "bound anchors cannot become MTS predictions without projection kernels",
    ],
    "1886_next": [
        "NEXT1886_0_primary",
        "do not use WEP bound anchors as predictions",
    ],
    "1066_typing": [
        "OLT1066_4_inert_source_scalar",
        "conditional_not_parent_derived",
    ],
    "1078_proof": [
        "OL1078_3_counterexample",
        "OBJECT_LANGUAGE_NOT_SIGNED",
    ],
    "1107_exhaustion": [
        "EXH1107_1_chain_rule",
        "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
    ],
    "1236_certificate": [
        "CERT1236_5_source_label_forgetting",
        "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
    ],
    "1338_theorem": [
        "OLT1338_4_action_scale_owner",
        "NOT_DERIVED_CURRENT_CORPUS",
    ],
    "1676_no_marker": [
        "NSS1676_5_verdict",
        "NO_SOURCE_ONLY_SLOT_THEOREM_NOT_PROVED",
    ],
    "1867_radial_cell": [
        "OLA1867_5_verdict",
        "OBJECT_LANGUAGE_CONSTRAINT_NOT_DERIVED_CURRENT_CORPUS",
    ],
    "1694_variation": [
        "VAR1694_1_Hilbert_source",
        "VAR1694_5_identity_verdict",
    ],
    "1762_deltaw": [
        "DW1762_0_zero_condition",
        "FALSE_PARENT_UNSIGNED",
    ],
    "1491_delta_w_pack": [
        "DWI1491_1_MICROSCOPE_TiPt",
        "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
    ],
    "local_bounds": [
        "R1_WEP_source_charge",
        "2.8e-15",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1887_SOURCE_REGISTER.csv",
    "typing_audit": OUT / "P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv",
    "action_scale_audit": OUT / "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv",
    "finite_vector_contract": OUT / "P8_Y5_PARENT_QLOC_1887_FINITE_SOURCE_WEIGHT_VECTOR_INTAKE_CONTRACT.csv",
    "vector_template": OUT / "P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_TEMPLATE_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_VALIDATOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_VALIDATOR_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1887_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1887_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1887_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1887_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1887_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1887_VALIDATION.csv",
}

SOURCE_WEIGHT_TEMPLATE_COPY = SOURCE_WEIGHT_DOCS / "SOURCE_WEIGHT_VECTOR1887_TEMPLATE_NONCLAIM.csv"


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


def typing_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_0_target",
            "claim": "derive parent object-language typing that makes source-only weights untypeable",
            "formal_sentence": "Arg(S_parent) subset {geometry, matter fields, owned gauge/current data, measured representation constants, universal constants}; Hom(SpeciesLabel,Coeff_active_source)=empty",
            "source_anchor": "P8_Y5_PARENT_QLOC_1886_NEXT_TARGET.csv:NEXT1886_0_primary",
            "result": "TARGET_SHARP",
            "gap": "must be parent-derived from MTS primitives, not imposed after WEP/PPN pressure",
            "effect_if_parent_signed": "Delta_w_AB=0, beta_w_source=0, beta_w_test=0, and w_R=0 after common calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_1_exact_conditional_certificate",
            "claim": "typed parent object language forbids w_A S_A",
            "formal_sentence": "if every coefficient owner is parent-generated and variation precedes readout, then a bare w_A has no owner, no transformation law, and no admissible target sort",
            "source_anchor": "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_0..CERT1236_6",
            "result": "EXACT_IF_PARENT_SIGNED",
            "gap": "certificate schema is present but not derived from motion/time/space primitives",
            "effect_if_parent_signed": "no-source-only slot becomes a theorem-zero rather than a closure axiom",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_2_candidate_typing",
            "claim": "inert source scalar is rejected by object-language typing",
            "formal_sentence": "w_A multiplying only active gravitational source strength has no independent observable, gauge, representation, or geometry role",
            "source_anchor": "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv:OLT1066_4_inert_source_scalar",
            "result": "CANDIDATE_REJECTION_NOT_PARENT_SIGNED",
            "gap": "candidate typing is discipline, not a proof of impossibility",
            "effect_if_parent_signed": "kills the simplest source-weight seam",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_3_direct_sum_counterexample",
            "claim": "ordinary matter category has no disconnected constants",
            "formal_sentence": "direct-sum matter sectors can still carry independent constants c_A or w_A unless the parent functor forbids them",
            "source_anchor": "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv:OL1078_3_counterexample",
            "result": "COUNTEREXAMPLE_SURVIVES",
            "gap": "connectedness/naturality alone does not erase species-family constants",
            "effect_if_parent_signed": "would turn naturality from helpful taste into proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_4_parent_generated_image",
            "claim": "visible/source coefficients are exhausted by the parent-generated image",
            "formal_sentence": "c_vis(Phi)=cbar(q(Phi),theta_rep) and Dq[v]=0 imply Lie_v c_vis=0 once membership in Image(ParentGenerate) is proved",
            "source_anchor": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_1_chain_rule",
            "result": "CHAIN_RULE_EXACT_MEMBERSHIP_NOT_DERIVED",
            "gap": "Image(ParentGenerate) exhaustion and readout/radiative stability remain unsigned",
            "effect_if_parent_signed": "hidden/source drift cannot re-enter through coefficient maps",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_5_source_label_forgetting",
            "claim": "gravitational source functor forgets per-species source weights",
            "formal_sentence": "source functor returns total Hilbert stress-energy, not per-species source weights or source-only labels",
            "source_anchor": "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_5_source_label_forgetting",
            "result": "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED",
            "gap": "matter category and variation/readout order are not yet parent-signed",
            "effect_if_parent_signed": "connects typed object language directly to WEP/R10/local-GR source-side reduction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_6_action_scale_and_readout",
            "claim": "one action scale plus stable readout makes source-only weights impossible",
            "formal_sentence": "all species action multipliers are quotient redundancies after quantum/path-integral/readout normalization and loops cannot regenerate source-only coefficients",
            "source_anchor": "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv:OLT1338_4_action_scale_owner;OLT1338_5_readout_stability",
            "result": "ACTION_SCALE_AND_READOUT_UNSIGNED",
            "gap": "classical EOM rescaling does not remove Hilbert-source weighting",
            "effect_if_parent_signed": "would close the most dangerous source-side loophole",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_7_no_marker_protection",
            "claim": "no hidden marker/domain/boundary scalar may be retyped as source coefficient",
            "formal_sentence": "no material marker, hidden frame, source-only constant, or readout-only label may alter source strength",
            "source_anchor": "P8_Y5_PARENT_QLOC_1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT.csv:NSS1676_2_no_hidden_marker;NSS1676_5_verdict",
            "result": "NO_MARKER_THEOREM_NOT_PROVED",
            "gap": "marker morphisms remain a retained residual unless parent grammar excludes them",
            "effect_if_parent_signed": "prevents source weights from coming back under another name",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_8_category_route_consistency",
            "claim": "category/object-language route is coherent in local radial-cell work",
            "formal_sentence": "C_R can be typed as compatibility data, not a propagating scalar, but the category rule is not parent-signed",
            "source_anchor": "P8_Y5_PARENT_QLOC_1867_OBJECT_LANGUAGE_DERIVATION_ATTEMPT.csv:OLA1867_5_verdict",
            "result": "COHERENT_CONTRACT_NOT_THEOREM",
            "gap": "repeated object-language bottleneck is structural, not an isolated R10 issue",
            "effect_if_parent_signed": "same parent grammar could suppress local radial-cell and source-weight residuals together",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OLT1887_9_verdict",
            "claim": "parent object-language typing derives no source-only coefficient slot",
            "formal_sentence": "NoSourceOnlySpeciesSlot follows from parent primitives without adding an external closure grammar",
            "source_anchor": "OLT1887_0 through OLT1887_8",
            "result": "OBJECT_LANGUAGE_TYPING_NOT_PARENT_DERIVED",
            "gap": "constructor list, current owner, action-scale owner, no hidden morphism, no marker theorem, and readout/radiative closure are not simultaneously signed",
            "effect_if_parent_signed": "local source-coupling route would become serious theorem-zero territory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def action_scale_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ASN1887_0_target",
            "scale_clause": "one parent action scale for ordinary matter",
            "test": "does a universal normalization make all relative w_A unphysical?",
            "result": "TARGET_SHARP",
            "gap": "relative source weights are not removed by merely choosing units",
            "source_anchor": "P8_Y5_PARENT_QLOC_1886_COMMON_MATTER_SIGNATURE_CONTRACT.csv:CMS1886_3_common_mode_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ASN1887_1_classical_eom_false_positive",
            "scale_clause": "weighted matter equations can look ordinary",
            "test": "delta(w_A S_A)/delta Psi_A = w_A E_A may be divided by constant w_A",
            "result": "FALSE_POSITIVE_FOR_SOURCE_UNIVERSALITY",
            "gap": "Hilbert/coframe source remains T_obs=sum_A w_A T_A",
            "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_0_matter_EOM;VAR1694_1_Hilbert_source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ASN1887_2_common_mode_guard",
            "scale_clause": "only a universal derivative-silent common mode can be calibration",
            "test": "w_A=w_common constant, range-independent, time-independent, species-blind and hidden-direction derivative silent",
            "result": "COMMON_MODE_ONLY_GUARDED",
            "gap": "Delta_w_AB != 0 or partial_phi w_A != 0 survives G_N/GM calibration",
            "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_3_common_mode;VAR1694_4_relative_mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ASN1887_3_quantum_path_integral_scale",
            "scale_clause": "path-integral/action-weight owner",
            "test": "relative species action prefactors must be proven to be gauge or forbidden before quantization/readout",
            "result": "OWNER_UNSIGNED",
            "gap": "action-scale owner was explicitly not parent-signed in 1338",
            "source_anchor": "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv:OLT1338_4_action_scale_owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ASN1887_4_radiative_readout_stability",
            "scale_clause": "no regenerated source coefficients after matching/readout",
            "test": "loops, spectroscopy, clocks, source-worldtube readouts and local projections preserve the same sorted domains",
            "result": "READOUT_RADIATIVE_UNSIGNED",
            "gap": "tree-level object-language typing would not be claim-grade without this",
            "source_anchor": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_5_radiative_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ASN1887_5_verdict",
            "scale_clause": "action-scale normalization proves w_A impossible",
            "test": "all source/action weights are common-mode calibration or theorem-zero",
            "result": "ACTION_SCALE_OWNER_UNSIGNED",
            "gap": "the current corpus can write the exact required contract, but cannot yet derive the scale owner",
            "source_anchor": "ASN1887_0 through ASN1887_4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_vector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "FSV1887_0_route_type",
            "required_field": "route_type",
            "arena_scope": "all_rows",
            "accepted_form": "parent_object_language_zero | finite_source_weight_vector | bound_anchor_nonclaim | schema_math_only_nonclaim",
            "refused_form": "closure, comparator_only, G_absorption, unity_tau, syntax_by_decree, or cancellation",
            "reason": "forces proof-vs-finite-vs-anchor distinction before any score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_1_component_basis",
            "required_field": "component_basis",
            "arena_scope": "finite_source_weight_vector",
            "accepted_form": "declared basis over source-relevant ordinary matter sectors with norm and common-mode subtraction",
            "refused_form": "MISSING_COMPONENT_BASIS, species labels without map, or hidden marker basis without no-marker theorem",
            "reason": "Delta_w has no meaning until its vector space and common mode are fixed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_2_delta_w_vector",
            "required_field": "Delta_w_i",
            "arena_scope": "WEP;Newton;PPN;R10;clock;orbital",
            "accepted_form": "numeric dimensionless source-weight vector or theorem-zero with source path",
            "refused_form": "symbolic Delta_w, bound-only eta, or fitted denominator",
            "reason": "MTS must predict source-weight content, not borrow the comparator bound as the prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_3_beta_w_source_test",
            "required_field": "beta_w_source; beta_w_test",
            "arena_scope": "finite exchange; R10; PPN",
            "accepted_form": "partial_X ln w_source and partial_X ln w_test in a declared canonical Xhat/phi convention",
            "refused_form": "product-only shortcut, no source/test split, or undeclared scalar normalization",
            "reason": "finite-exchange amplitudes require both legs and their normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_4_wR_source_normalization",
            "required_field": "w_R_or_source_norm",
            "arena_scope": "local Newton; PPN; orbital",
            "accepted_form": "numeric source normalization residual after common-mode calibration, or parent theorem-zero",
            "refused_form": "absorbed into G_N/GM without common-mode guard",
            "reason": "relative source normalization is not hidden by calibrating one gravitational constant",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_5_tau_arena",
            "required_field": "tau_WEP; tau_PPN; tau_R10; tau_clock; tau_orbital",
            "arena_scope": "arena_score",
            "accepted_form": "arena-specific projection/readout factor with units, source path, and extraction method",
            "refused_form": "tau=1 by convenience, arena omitted, or bound anchor used as projection",
            "reason": "same Delta_w can project differently into each local test",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_6_K_Qbar_projection",
            "required_field": "K_arena; Qbar_source_test; material_projection",
            "arena_scope": "WEP;R10;clock;orbital",
            "accepted_form": "source-backed material/source/readout tensors or theorem-zero",
            "refused_form": "MICROSCOPE eta, R10 alpha, or clock bound alone treated as K/Qbar",
            "reason": "bounds constrain products; they are not the parent coefficient vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_7_source_path",
            "required_field": "source_path; source_anchor; extraction_method",
            "arena_scope": "all_rows",
            "accepted_form": "existing local path or explicit web provenance for theorem/value/bound",
            "refused_form": "MISSING marker, private guess, unsourced coefficient, or old closure prose",
            "reason": "keeps the finite branch auditable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_8_product_law",
            "required_field": "product_formula; no_cancellation_policy",
            "arena_scope": "arena_score",
            "accepted_form": "sum-absolute active components unless parent identity proves signed cancellation",
            "refused_form": "source/test terms tuned to cancel or omitted because bound is small",
            "reason": "prevents hidden source slots being hidden twice",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FSV1887_9_flags",
            "required_field": "valid_prediction_row; score_ready; valid_for_claim; claim_allowed",
            "arena_scope": "all_rows",
            "accepted_form": "all false in this checkpoint except schema math may set valid_prediction_row=false/true only as nonclaim",
            "refused_form": "claim flags true or score_ready with missing/unsigned markers",
            "reason": "1887 is proof/contract work, not local-GR evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def vector_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "FSV1887_PARENT_ZERO_TEMPLATE",
            "branch_id": BRANCH_ID,
            "route_type": "parent_object_language_zero",
            "arena": "WEP;PPN;Newton;R10;clock;orbital",
            "component_basis": "not_required_after_parent_zero",
            "Delta_w_i": "0",
            "beta_w_source": "0",
            "beta_w_test": "0",
            "w_R_or_source_norm": "0",
            "tau_arena": "0_or_not_required_after_parent_zero",
            "K_arena": "0_or_not_required_after_parent_zero",
            "material_projection": "0_or_not_required_after_parent_zero",
            "product_formula": "NoSourceOnlySpeciesSlot => all finite source-weight residuals vanish",
            "source_path": "MISSING_PARENT_OBJECT_LANGUAGE_THEOREM",
            "source_anchor": "OLT1887_9_verdict",
            "current_status": "MISSING_PARENT_INPUT",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "FSV1887_MICROSCOPE_ANCHOR_NONCLAIM",
            "branch_id": BRANCH_ID,
            "route_type": "bound_anchor_nonclaim",
            "arena": "WEP_MICROSCOPE_TiPt",
            "component_basis": "MISSING_COMPONENT_BASIS",
            "Delta_w_i": "MISSING_PARENT_VECTOR",
            "beta_w_source": "not_applicable_for_eta_anchor",
            "beta_w_test": "not_applicable_for_eta_anchor",
            "w_R_or_source_norm": "MISSING_SOURCE_NORMALIZATION",
            "tau_arena": "MISSING_TAU_WEP",
            "K_arena": "MISSING_MATERIAL_PROJECTION",
            "material_projection": "MISSING_TiPt_SOURCE_TEST_TENSOR",
            "product_formula": "|eta_TiPt| <= |DeltaQ_TiPt dot Delta_w| |tau_WEP|",
            "source_path": str(INPUTS["local_bounds"]),
            "source_anchor": "R1_WEP_source_charge; 2.8e-15",
            "current_status": "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "FSV1887_R10_SOURCE_VECTOR_NONCLAIM",
            "branch_id": BRANCH_ID,
            "route_type": "finite_source_weight_vector",
            "arena": "R10_short_range",
            "component_basis": "MISSING_COMPONENT_BASIS",
            "Delta_w_i": "MISSING_PARENT_VECTOR",
            "beta_w_source": "MISSING_SOURCE_LEG",
            "beta_w_test": "MISSING_TEST_LEG",
            "w_R_or_source_norm": "MISSING_SOURCE_NORMALIZATION",
            "tau_arena": "MISSING_TAU_R10(lambda)",
            "K_arena": "MISSING_K_R10(lambda)",
            "material_projection": "MISSING_SOURCE_TEST_GEOMETRY",
            "product_formula": "alpha_delta_w(lambda)=K_R10(lambda) * Qbar_source_test(lambda) dot Delta_w",
            "source_path": str(INPUTS["1491_delta_w_pack"]),
            "source_anchor": "DWI1491_3_R10",
            "current_status": "SYMBOLIC_ANCHOR_ONLY_CURVE_KERNEL_MISSING",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "FSV1887_PPN_BETA_SOURCE_NONCLAIM",
            "branch_id": BRANCH_ID,
            "route_type": "finite_source_weight_vector",
            "arena": "PPN_beta_gamma",
            "component_basis": "MISSING_COMPONENT_BASIS",
            "Delta_w_i": "MISSING_PARENT_VECTOR",
            "beta_w_source": "MISSING_CANONICAL_PARTIAL_X_LN_W_SOURCE",
            "beta_w_test": "MISSING_CANONICAL_PARTIAL_X_LN_W_TEST",
            "w_R_or_source_norm": "MISSING_W_R",
            "tau_arena": "MISSING_TAU_PPN",
            "K_arena": "MISSING_PPN_OPERATOR_NORM",
            "material_projection": "MISSING_SOURCE_BODY_COMPOSITION",
            "product_formula": "Delta_beta_source <= K_PPN * (|beta_w_source|+|beta_w_test|+||Delta_w||)",
            "source_path": str(INPUTS["1886_finite_contract"]),
            "source_anchor": "FWR1886_2_beta_w;FWR1886_3_delta_w;FWR1886_4_tau_projection",
            "current_status": "MISSING_PARENT_SOURCE_WEIGHT_INPUTS",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "FSV1887_SCHEMA_MATH_ONLY_NONCLAIM",
            "branch_id": BRANCH_ID,
            "route_type": "schema_math_only_nonclaim",
            "arena": "unit_test_only",
            "component_basis": "toy_basis_declared",
            "Delta_w_i": "1.0e-20",
            "beta_w_source": "2.0e-20",
            "beta_w_test": "3.0e-20",
            "w_R_or_source_norm": "4.0e-20",
            "tau_arena": "sourced_toy_tau_nonphysical",
            "K_arena": "sourced_toy_K_nonphysical",
            "material_projection": "sourced_toy_projection_nonphysical",
            "product_formula": "toy product validates schema only",
            "source_path": str(OUTPUTS["finite_vector_contract"]),
            "source_anchor": "FSV1887_0_route_type",
            "current_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1887_0_closure_phrase",
            "route_type": "finite_source_weight_vector",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": False,
            "component_basis": "MISSING_COMPONENT_BASIS",
            "tau_status": "MISSING_TAU",
            "source_path_status": "MISSING_SOURCE_PATH",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": True,
            "expected_status": "REFUSED_CLOSURE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_1_parent_zero_unsigned",
            "route_type": "parent_object_language_zero",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": False,
            "component_basis": "not_required_after_parent_zero",
            "tau_status": "not_required_after_parent_zero",
            "source_path_status": "MISSING_PARENT_THEOREM_SOURCE",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "REFUSED_PARENT_OBJECT_LANGUAGE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_2_syntax_by_decree",
            "route_type": "parent_object_language_zero",
            "syntax_only": True,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": False,
            "component_basis": "declared_by_decree",
            "tau_status": "not_required_after_parent_zero",
            "source_path_status": "PRIVATE_CLOSURE_DOC",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "REFUSED_SYNTAX_BY_DECREE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_3_action_scale_unowned",
            "route_type": "action_scale_zero",
            "syntax_only": False,
            "object_language_signed": True,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": False,
            "component_basis": "not_required_after_zero",
            "tau_status": "not_required_after_zero",
            "source_path_status": "MISSING_ACTION_SCALE_OWNER_SOURCE",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "REFUSED_ACTION_SCALE_UNOWNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_4_bound_anchor_prediction",
            "route_type": "bound_anchor_nonclaim",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": False,
            "component_basis": "MISSING_COMPONENT_BASIS",
            "tau_status": "MISSING_TAU_WEP",
            "source_path_status": "SOURCE_EXISTS",
            "uses_bound_anchor_as_prediction": True,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_5_missing_component_basis",
            "route_type": "finite_source_weight_vector",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": True,
            "component_basis": "MISSING_COMPONENT_BASIS",
            "tau_status": "SOURCE_BACKED_TAU",
            "source_path_status": "SOURCE_EXISTS",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "REFUSED_MISSING_COMPONENT_BASIS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_6_tau_set_to_one",
            "route_type": "finite_source_weight_vector",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": True,
            "component_basis": "declared_component_basis",
            "tau_status": "UNITY_BY_CONVENIENCE",
            "source_path_status": "SOURCE_EXISTS",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "REFUSED_TAU_SET_TO_ONE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_7_G_absorption",
            "route_type": "finite_source_weight_vector",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": True,
            "component_basis": "declared_component_basis",
            "tau_status": "SOURCE_BACKED_TAU",
            "source_path_status": "SOURCE_EXISTS",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": True,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_8_cancellation_only",
            "route_type": "finite_source_weight_vector",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": True,
            "component_basis": "declared_component_basis",
            "tau_status": "SOURCE_BACKED_TAU",
            "source_path_status": "SOURCE_EXISTS",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": True,
            "closure_used": False,
            "expected_status": "REFUSED_CANCELLATION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "DRY1887_9_schema_math_only",
            "route_type": "schema_math_only_nonclaim",
            "syntax_only": False,
            "object_language_signed": False,
            "action_scale_owner_signed": False,
            "finite_numeric_inputs": True,
            "component_basis": "declared_component_basis",
            "tau_status": "SOURCE_BACKED_TOY_TAU",
            "source_path_status": "SOURCE_EXISTS",
            "uses_bound_anchor_as_prediction": False,
            "uses_G_absorption": False,
            "cancellation_only": False,
            "closure_used": False,
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["closure_used"]) == "true":
        status = "REFUSED_CLOSURE_NOT_EVIDENCE"
        detail = "closure text is not a parent theorem or finite prediction row"
    elif bool_string(row["syntax_only"]) == "true":
        status = "REFUSED_SYNTAX_BY_DECREE"
        detail = "object-language syntax must be derived from parent primitives"
    elif row["route_type"] == "parent_object_language_zero" and bool_string(row["object_language_signed"]) != "true":
        status = "REFUSED_PARENT_OBJECT_LANGUAGE_UNSIGNED"
        detail = "NoSourceOnlySpeciesSlot is not parent-signed"
    elif row["route_type"] == "action_scale_zero" and bool_string(row["action_scale_owner_signed"]) != "true":
        status = "REFUSED_ACTION_SCALE_UNOWNED"
        detail = "relative action/source scale owner remains unsigned"
    elif bool_string(row["uses_bound_anchor_as_prediction"]) == "true":
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
        detail = "comparator bound is pressure, not an MTS coefficient"
    elif is_placeholder(row["component_basis"]):
        status = "REFUSED_MISSING_COMPONENT_BASIS"
        detail = "Delta_w vector has no declared source-relevant basis"
    elif row["tau_status"] == "UNITY_BY_CONVENIENCE":
        status = "REFUSED_TAU_SET_TO_ONE"
        detail = "arena projection tau cannot be set to unity by convenience"
    elif bool_string(row["uses_G_absorption"]) == "true":
        status = "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"
        detail = "relative weights cannot be absorbed into one measured G"
    elif bool_string(row["cancellation_only"]) == "true":
        status = "REFUSED_CANCELLATION_ONLY"
        detail = "cancellations require a parent identity, not a tuned vector"
    elif row["route_type"] == "schema_math_only_nonclaim":
        status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
        detail = "schema paths and algebra work, but coefficients are toy nonclaim rows"
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
            "runner_id": "RUN1887_0_live_parent_zero",
            "input_kind": "parent_zero_template",
            "source_rows": "P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_TEMPLATE_NONCLAIM.csv:FSV1887_PARENT_ZERO_TEMPLATE",
            "runner_status": "REFUSED_PARENT_OBJECT_LANGUAGE_UNSIGNED",
            "reason": "NoSourceOnlySpeciesSlot remains exact conditional grammar, not parent theorem",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1887_1_MICROSCOPE_anchor",
            "input_kind": "bound_anchor_nonclaim",
            "source_rows": "local_bound_claims.csv:R1_WEP_source_charge",
            "runner_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
            "reason": "2.8e-15 eta bound is not a Delta_w vector, tau projection, or material tensor",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1887_2_candidate_finite_vector",
            "input_kind": "finite_source_weight_vector",
            "source_rows": "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv:DWI1491_0..DWI1491_5",
            "runner_status": "REFUSED_MISSING_COMPONENT_BASIS_AND_ARENA_PROJECTIONS",
            "reason": "real source-weight vector rows lack parent component basis, tau, K/Qbar, and source/test projection kernels",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1887_3_schema_math_only",
            "input_kind": "schema_math_only_nonclaim",
            "source_rows": "P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_TEMPLATE_NONCLAIM.csv:FSV1887_SCHEMA_MATH_ONLY_NONCLAIM",
            "runner_status": "SCHEMA_VALID_NONCLAIM_NO_EVIDENCE",
            "reason": "toy numbers can exercise parser/math only; they do not score local physics",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE1887_0_object_language_zero",
            "claim": "NoSourceOnlySpeciesSlot theorem zero",
            "required": "parent-signed constructor list, source-label forgetting, no marker theorem, current owner, readout/radiative closure",
            "current_status": "BLOCKED_OBJECT_LANGUAGE_TYPING_NOT_PARENT_DERIVED",
            "allowed_next": "derive action-scale owner/readout stability or demote to explicit closure",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1887_1_action_scale_zero",
            "claim": "relative action/source weights are gauge or common calibration",
            "required": "one parent action-scale owner plus quantum/path-integral/readout stability",
            "current_status": "BLOCKED_ACTION_SCALE_OWNER_UNSIGNED",
            "allowed_next": "prove owner or retain finite Delta_w/beta_w/w_R rows",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1887_2_finite_vector",
            "claim": "finite source-weight vector predicts WEP/PPN/R10/local residuals",
            "required": "component basis, Delta_w, beta_w legs, w_R, tau/K/Qbar/material projections, source paths",
            "current_status": "BLOCKED_MISSING_PARENT_INPUTS_AND_ARENA_PROJECTIONS",
            "allowed_next": "source real coefficients and projections without bound-anchor shortcut",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1887_3_local_GR",
            "claim": "local GR/Newton source-coupling reduction",
            "required": "object-language zero or finite vector below all local arenas with no edge/cancellation dependence",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "allowed_next": "continue derivation-first; test only after source seam is signed or bounded",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1887_0_derivation_attempt",
            "question": "can parent object-language typing alone prove w_A impossible?",
            "answer": "not from current corpus",
            "basis": "counterexample survives and action-scale/readout owner remain unsigned",
            "decision": "DEMOTE_OBJECT_LANGUAGE_ZERO_TO_CONDITIONAL_CONTRACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1887_1_finite_branch",
            "question": "can finite Delta_w/beta_w/w_R rows score now?",
            "answer": "no",
            "basis": "missing component basis, parent coefficient vector, tau/K/Qbar projections, source paths",
            "decision": "STAGE_FINITE_VECTOR_INTAKE_BUT_KEEP_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1887_2_next_attack",
            "question": "what is the best next seam?",
            "answer": "action-scale owner and readout stability",
            "basis": "this is the narrowest route that could convert the closure grammar into a theorem-zero without immediately needing all bound inputs",
            "decision": "SELECT_1888_ACTION_SCALE_OWNER_READOUT_STABILITY_OR_FINITE_DELTAW_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1887_0_primary",
            "selection_status": "selected",
            "target_doc": "1888-Y5-R2FR-action-scale-owner-readout-stability-or-finite-deltaw-vector.md",
            "target_script": "scripts/Y5_R2FR_action_scale_owner_readout_stability_or_finite_deltaw_vector_1888.py",
            "objective": "try to derive the parent action-scale owner and readout/radiative stability that make relative source weights gauge/forbidden; if it fails, build the first real finite Delta_w vector row intake with WEP/PPN/R10/local hooks",
            "success_condition": "parent-signed owner/readout theorem, or strict nonclaim Delta_w/beta_w/w_R vector rows with component basis, tau, K/Qbar, material projections, and real source paths",
            "do_not": "do not absorb relative weights into G_N/GM, do not set tau=1, do not use MICROSCOPE/R10/clock bounds as predictions, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS1887_0_good_news",
            "area": "source-coupling seam",
            "status": "exact seam located",
            "detail": "w_A S_A is the right obstruction because EOM can look ordinary while Hilbert source changes",
            "risk_level": "USEFUL_PROGRESS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1887_1_main_bottleneck",
            "area": "parent grammar/action scale",
            "status": "unsigned",
            "detail": "object-language typing, action-scale owner and readout/radiative stability are conditional contracts, not derived theorem-zero clauses",
            "risk_level": "MAIN_BOTTLENECK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1887_2_testing_readiness",
            "area": "local data branches",
            "status": "not score-ready",
            "detail": "WEP/R10/clock/orbital bounds are useful pressure but need parent coefficient vectors and arena projections before scoring",
            "risk_level": "BLOCKED_FOR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "typing_audit": typing_audit_rows(),
        "action_scale_audit": action_scale_audit_rows(),
        "finite_vector_contract": finite_vector_contract_rows(),
        "vector_template": vector_template_rows(),
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
            if any(marker in joined for marker in ("MISSING", "UNSIGNED", "BLOCKED")):
                if bool_string(row.get("score_ready", "false")) == "true" or bool_string(row.get("valid_for_claim", "false")) == "true":
                    return False, f"{path.name}:row{index}:blocked marker marked ready"
    return True, "blocked-marker rows are not claim-ready"


def copy_branch_artifacts() -> None:
    shutil.copy2(OUTPUTS["typing_audit"], MICROSCOPE_RESIDUALS / OUTPUTS["typing_audit"].name)
    shutil.copy2(
        OUTPUTS["action_scale_audit"],
        QUEUE / "JR1887_ACTION_SCALE_NORMALIZATION_AUDIT_NONCLAIM.csv",
    )
    shutil.copy2(
        OUTPUTS["finite_vector_contract"],
        QUEUE / "JR1887_FINITE_SOURCE_WEIGHT_VECTOR_CONTRACT_NONCLAIM.csv",
    )
    shutil.copy2(OUTPUTS["vector_template"], SOURCE_WEIGHT_TEMPLATE_COPY)
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
            "validation_id": "VAL1887_0_sources_exist",
            "status": "PASS" if all(bool_string(row["exists"]) == "true" for row in source_rows) else "FAIL",
            "detail": f"{sum(bool_string(row['exists']) == 'true' for row in source_rows)}/{len(source_rows)} sources exist",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1887_1_needles_found",
            "status": "PASS" if all(row["needle_status"] == "PASS" for row in source_rows) else "FAIL",
            "detail": f"{sum(row['needle_status'] == 'PASS' for row in source_rows)}/{len(source_rows)} source needles found",
            "valid_for_claim": False,
        }
    )

    typing_rows = csv_rows(OUTPUTS["typing_audit"])
    checks.append(
        {
            "validation_id": "VAL1887_2_counterexample_retained",
            "status": "PASS" if any(row["result"] == "COUNTEREXAMPLE_SURVIVES" for row in typing_rows) else "FAIL",
            "detail": "direct-sum/source-weight counterexample remains explicit",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1887_3_object_language_not_promoted",
            "status": "PASS"
            if any(row["audit_id"] == "OLT1887_9_verdict" and row["result"] == "OBJECT_LANGUAGE_TYPING_NOT_PARENT_DERIVED" for row in typing_rows)
            else "FAIL",
            "detail": "object-language typing is retained as conditional contract, not claim",
            "valid_for_claim": False,
        }
    )

    action_rows = csv_rows(OUTPUTS["action_scale_audit"])
    checks.append(
        {
            "validation_id": "VAL1887_4_action_scale_unsigned",
            "status": "PASS"
            if any(row["audit_id"] == "ASN1887_5_verdict" and row["result"] == "ACTION_SCALE_OWNER_UNSIGNED" for row in action_rows)
            else "FAIL",
            "detail": "action-scale owner remains unsigned",
            "valid_for_claim": False,
        }
    )

    contract_rows = csv_rows(OUTPUTS["finite_vector_contract"])
    required_contract_ids = {
        "FSV1887_1_component_basis",
        "FSV1887_2_delta_w_vector",
        "FSV1887_3_beta_w_source_test",
        "FSV1887_4_wR_source_normalization",
        "FSV1887_5_tau_arena",
        "FSV1887_6_K_Qbar_projection",
        "FSV1887_8_product_law",
    }
    checks.append(
        {
            "validation_id": "VAL1887_5_finite_contract_fields",
            "status": "PASS" if required_contract_ids.issubset({row["contract_id"] for row in contract_rows}) else "FAIL",
            "detail": f"finite_contract_fields={len(contract_rows)}",
            "valid_for_claim": False,
        }
    )

    template_rows = csv_rows(OUTPUTS["vector_template"])
    checks.append(
        {
            "validation_id": "VAL1887_6_templates_nonclaim",
            "status": "PASS"
            if all(bool_string(row.get("score_ready", "false")) == "false" and bool_string(row.get("valid_for_claim", "false")) == "false" for row in template_rows)
            else "FAIL",
            "detail": "parent-zero, WEP, R10, PPN, and schema templates remain nonclaim",
            "valid_for_claim": False,
        }
    )

    dryrun_rows = csv_rows(OUTPUTS["dryrun_results"])
    expected_statuses = {
        "REFUSED_CLOSURE_NOT_EVIDENCE",
        "REFUSED_PARENT_OBJECT_LANGUAGE_UNSIGNED",
        "REFUSED_SYNTAX_BY_DECREE",
        "REFUSED_ACTION_SCALE_UNOWNED",
        "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
        "REFUSED_MISSING_COMPONENT_BASIS",
        "REFUSED_TAU_SET_TO_ONE",
        "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    observed_statuses = {row["observed_status"] for row in dryrun_rows}
    checks.append(
        {
            "validation_id": "VAL1887_7_dryrun_failure_modes",
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
            "validation_id": "VAL1887_8_runner_refusal",
            "status": "PASS" if all(bool_string(row["score_ready"]) == "false" for row in runner_rows) else "FAIL",
            "detail": "all live/candidate runner branches refuse claim scoring",
            "valid_for_claim": False,
        }
    )

    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1887_9_claim_gates",
            "status": "PASS" if all(bool_string(row["pass_gate"]) == "false" for row in gate_rows) else "FAIL",
            "detail": "all local/source-coupling claim gates remain blocked",
            "valid_for_claim": False,
        }
    )

    decision_rows_loaded = csv_rows(OUTPUTS["decision"])
    checks.append(
        {
            "validation_id": "VAL1887_10_decision",
            "status": "PASS"
            if any(row["decision"] == "SELECT_1888_ACTION_SCALE_OWNER_READOUT_STABILITY_OR_FINITE_DELTAW_VECTOR" for row in decision_rows_loaded)
            else "FAIL",
            "detail": "decision selects action-scale owner/readout stability or finite Delta_w vector next",
            "valid_for_claim": False,
        }
    )

    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1887_11_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1887_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1888 action-scale owner/readout stability selected",
            "valid_for_claim": False,
        }
    )

    status_rows = csv_rows(OUTPUTS["project_status"])
    checks.append(
        {
            "validation_id": "VAL1887_12_project_status",
            "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows) else "FAIL",
            "detail": "project status snapshot keeps source object-language/action-scale as main bottleneck",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1887_13_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1887_14_blocked_markers_not_ready",
            "status": "PASS" if blocked_ok else "FAIL",
            "detail": blocked_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1887_15_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["typing_audit"].name,
        QUEUE / "JR1887_ACTION_SCALE_NORMALIZATION_AUDIT_NONCLAIM.csv",
        QUEUE / "JR1887_FINITE_SOURCE_WEIGHT_VECTOR_CONTRACT_NONCLAIM.csv",
        SOURCE_WEIGHT_TEMPLATE_COPY,
        QUARANTINE / OUTPUTS["dryrun_results"].name,
    ]
    checks.append(
        {
            "validation_id": "VAL1887_16_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1887_17_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1887*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1887_18_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1887_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1887_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1887 parent object-language typing or finite source-weight vector",
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
    content = f"""# 1887 - Parent Object-Language Typing Or Finite Source-Weight Vector

**Private status:** derivation-first source-coupling checkpoint; no WEP/R10/PPN/local-GR claim.

## Result

1887 attacks the exact seam left by 1886:

```text
S_matter = sum_A w_A S_A
T_source = sum_A w_A T_A
```

The good news is that the target theorem is now clean:

```text
Arg(S_parent) subset {{geometry, matter fields, owned gauge/current data,
measured representation constants, universal constants}}
Hom(SpeciesLabel, Coeff_active_source) = empty
```

If the parent action derives that typed object language, then a bare source-only `w_A` is not merely small; it is untypeable. That would set `Delta_w_AB`, `beta_w_source`, `beta_w_test`, and `w_R` to zero after common-mode calibration.

The bad news is the same sharp honesty as before: the current corpus has not yet derived the parent constructor list, action-scale owner, no-marker theorem, or readout/radiative stability from MTS primitives. So 1887 does **not** claim local GR. It converts the route into a precise theorem contract and a strict finite-vector intake contract.

## Object-Language Typing Proof Audit

{markdown_table(rows_by_name["typing_audit"])}

## Action-Scale Normalization Audit

{markdown_table(rows_by_name["action_scale_audit"])}

## Finite Source-Weight Vector Intake Contract

{markdown_table(rows_by_name["finite_vector_contract"])}

## Source-Weight Vector Template

{markdown_table(rows_by_name["vector_template"])}

## Validator Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Validator Dry-Run Results

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
