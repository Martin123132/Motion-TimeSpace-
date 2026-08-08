from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1886"
WEP_SOURCE_WEIGHT_ANCHOR = 2.8e-15

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md"

INPUTS = {
    "1885_doc": ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
    "1885_validation": OUT / "P8_Y5_BRR545_1885_VALIDATION.csv",
    "1885_source_coupling": OUT / "P8_Y5_PARENT_QLOC_1885_SOURCE_COUPLING_ZERO_AUDIT.csv",
    "1885_beta_contract": OUT / "P8_Y5_PARENT_QLOC_1885_BETA_RESIDUAL_VECTOR_CONTRACT.csv",
    "1883_full_vector": OUT / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
    "1064_label_forgetting": OUT / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "1064_slot_audit": OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv",
    "1065_parent_grammar": OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
    "1065_zero_clauses": OUT / "P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1079_current_owner": OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv",
    "1088_minimal_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1104_parent_signature": OUT / "P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
    "1105_master_morphism": OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv",
    "1105_subcase_map": OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_SUBCASE_MAP.csv",
    "1694_variation_identity": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
    "1694_current_rows": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
    "1702_wep_product": OUT / "P8_Y5_PARENT_QLOC_1702_WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv",
    "1703_wep_fill": OUT / "P8_Y5_PARENT_QLOC_1703_WEP_SOURCE_WEIGHT_FILL_AUDIT.csv",
    "1762_deltaw_interface": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1491_delta_w_pack": OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1885_doc": [
        "NEXT1885_0_primary",
        "NO_SOURCE_ONLY_SLOT_IS_NEXT_BEST_ATTACK",
    ],
    "1885_validation": [
        "VAL1885_OVERALL,PASS",
    ],
    "1885_source_coupling": [
        "SCZ1885_1_no_source_only_slot",
        "SOURCE_COUPLING_ZERO_NOT_CLOSED",
    ],
    "1885_beta_contract": [
        "BRC1885_0_delta_beta_source",
        "Delta_beta_total_abs",
    ],
    "1883_full_vector": [
        "PPNV1883_4_wR_source_normalization",
        "MISSING_SOURCE_PREFACTOR_ZERO_OR_BOUND",
    ],
    "1064_label_forgetting": [
        "PLF1064_2_no_source_only_slot",
        "COUNTEREXAMPLE_SURVIVES",
    ],
    "1064_slot_audit": [
        "NSS1064_2_relative_weight",
        "live_countermodel_if_not_forbidden",
    ],
    "1065_parent_grammar": [
        "PGG1065_5_verdict",
        "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED",
    ],
    "1065_zero_clauses": [
        "WTZ1065_4_verdict",
        "THEOREM_ZERO_NOT_PARENT_SIGNED",
    ],
    "1066_source_scalar": [
        "SSE1066_5_verdict",
        "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
    ],
    "1079_current_owner": [
        "PR1079_4_no_pre_action_species_weight",
        "NOT_SIGNED",
    ],
    "1088_minimal_signature": [
        "MOMS1088_4_no_species_weights",
        "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
    ],
    "1104_parent_signature": [
        "SIG1104_4_source_weight_exclusion",
        "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
    ],
    "1105_master_morphism": [
        "MHM1105_6_verdict",
        "MASTER_THEOREM_NOT_DERIVED_DEMOTE_TO_EXPLICIT_CLOSURE",
    ],
    "1105_subcase_map": [
        "SUB1105_2_source_weight",
        "RETAINED_RESIDUAL",
    ],
    "1694_variation_identity": [
        "VAR1694_1_Hilbert_source",
        "VAR1694_5_identity_verdict",
    ],
    "1694_current_rows": [
        "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor",
        "NONCLAIM_ONLY",
    ],
    "1702_wep_product": [
        "WEP1702_4_refusal",
        "REFUSAL_ACTIVE",
    ],
    "1703_wep_fill": [
        "WFA1703_5_verdict",
        "HARD_BLOCKED_TO_PARSER_SHELL",
    ],
    "1762_deltaw_interface": [
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
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1886_SOURCE_REGISTER.csv",
    "no_source_slot_audit": OUT / "P8_Y5_PARENT_QLOC_1886_NO_SOURCE_ONLY_SLOT_PROOF_AUDIT.csv",
    "matter_signature_contract": OUT / "P8_Y5_PARENT_QLOC_1886_COMMON_MATTER_SIGNATURE_CONTRACT.csv",
    "finite_wr_contract": OUT / "P8_Y5_PARENT_QLOC_1886_FINITE_WR_BETAW_ROW_CONTRACT.csv",
    "candidate_template": OUT / "P8_Y5_PARENT_QLOC_1886_WR_BETAW_CANDIDATE_TEMPLATE_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1886_WR_BETAW_VALIDATOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1886_WR_BETAW_VALIDATOR_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1886_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1886_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1886_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1886_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1886_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1886_VALIDATION.csv",
}

SOURCE_WEIGHT_TEMPLATE_COPY = SOURCE_WEIGHT_DOCS / "WR_BETAW1886_SOURCE_WEIGHT_TEMPLATE_NONCLAIM.csv"


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def is_placeholder(value: Any) -> bool:
    text = str(value).strip()
    if not text:
        return True
    return any(marker in text.upper() for marker in ("MISSING", "PLACEHOLDER", "TBD", "UNSIGNED", "HYPOTHETICAL"))


def finite_float(value: Any) -> tuple[bool, float | None]:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


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
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1886": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def no_source_slot_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_0_target",
            "route": "no-source-only-slot theorem",
            "formal_statement": "Allowed ordinary matter action has no independent w_A(X)S_A, kappa_A(X)T_A, or source-only material multiplier before variation.",
            "attempt_result": "TARGET_SHARP",
            "blocker": "must be parent action grammar, not our preference after seeing WEP/PPN constraints",
            "consequence": "would set Delta_w_AB=0 and beta_w_source=beta_w_test=0 after common calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_1_total_hilbert_variation",
            "route": "same action Hilbert source",
            "formal_statement": "If S_matter=sum_A S_A with no weights, T_total=2/sqrt(-g) delta S_matter/delta g=sum_A T_A.",
            "attempt_result": "EXACT_GIVEN_COMMON_ACTION",
            "blocker": "common action assumption itself is unsigned; pre-action weights can be inserted before this step",
            "consequence": "useful ingredient but not a no-slot proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_2_counterexample",
            "route": "relative source/action weight",
            "formal_statement": "S_matter=sum_A w_A S_A gives E_A weighted by w_A but T_source=sum_A w_A T_A, so source strength changes while covariance/additivity survive.",
            "attempt_result": "COUNTEREXAMPLE_SURVIVES",
            "blocker": "classical-looking equations and same visible coframe are not enough",
            "consequence": "w_R/beta_w/Delta_w residual rows remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_3_object_language",
            "route": "typed parent object language",
            "formal_statement": "Arg(S_parent) subset geometry, matter fields, observed connections, measured representation constants, and universal constants; inert source-only scalars are not typed objects.",
            "attempt_result": "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
            "blocker": "object-language/action-scale normalization is an exact contract, not derived from deeper MTS primitives",
            "consequence": "cannot promote Delta_w=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_4_common_mode_guard",
            "route": "measured G common-mode absorption",
            "formal_statement": "A universal derivative-silent common w can be calibration only; relative, time-dependent, range-dependent, species-dependent, or frame-dependent w cannot be absorbed into G_N.",
            "attempt_result": "GUARDED_CALIBRATION_ONLY",
            "blocker": "common-mode status must be proven before absorption",
            "consequence": "relative source weights cannot be swept into measured GM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_5_master_morphism",
            "route": "master no-hidden-visible coefficient morphism",
            "formal_statement": "Hom(C_hid,Coeff(source)) is absent or constant, so hidden invariants cannot feed w_A or kappa_A.",
            "attempt_result": "MASTER_THEOREM_NOT_DERIVED",
            "blocker": "one surviving hidden invariant scalar can still feed a visible coefficient map unless product/sequester/radiative closure is signed",
            "consequence": "closure pack remains private discipline, not proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_6_variation_identity",
            "route": "source-weight variation identity",
            "formal_statement": "delta(w_A S_A)/delta Psi_A=w_A E_A but T_obs=sum_A w_A T_A and J_phi contains partial_phi w_A terms.",
            "attempt_result": "DERIVED_ALGEBRAIC_SEAM",
            "blocker": "the seam is real; it must be forbidden or bounded",
            "consequence": "finite beta_w and Delta_w channels are the right fallback variables",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NSS1886_7_verdict",
            "route": "common matter no-source-only-slot proof",
            "formal_statement": "Current MTS parent derives no hidden source-only/action-weight slot for ordinary matter.",
            "attempt_result": "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED",
            "blocker": "grammar, current owner, object-language typing, no hidden morphism, action-scale normalization and readout/radiative closure are not all parent-signed",
            "consequence": "build finite w_R/beta_w/Delta_w contract; no local GR/Newton promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def matter_signature_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "CMS1886_0_action_form",
            "clause": "ordinary matter action factors through observed quotient geometry",
            "required_statement": "S_matter=sum_A S_A[Psi_A;e_obs(q(Phi)),omega[e_obs],A_obs(q),theta_A]",
            "if_signed": "vertical hidden/source variation cannot hit ordinary matter through geometry",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_unsigned": "representative/shadow/source marker can re-enter",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CMS1886_1_no_source_only_weight",
            "clause": "no independent source/action weight",
            "required_statement": "Allowed[S_matter] excludes w_A(X)S_A, kappa_A(X)T_A, and material-only source multipliers",
            "if_signed": "Delta_w_AB=0 and beta_w,A=0 unless a measured matter parameter carries the effect",
            "current_status": "EXACT_CLAUSE_NOT_PARENT_DERIVED",
            "if_unsigned": "relative source weights survive covariance/additivity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CMS1886_2_variation_order",
            "clause": "variation before readout/projection",
            "required_statement": "Hilbert/current source is extracted from S_parent before material/readout projection or empirical fitting",
            "if_signed": "post-variation selector F(T_A,A) cannot manufacture a source residual",
            "current_status": "CONDITIONAL_READOUT_CONTRACT",
            "if_unsigned": "readout can mimic composition-dependent source residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CMS1886_3_common_mode_guard",
            "clause": "common weight is only calibration",
            "required_statement": "w_A=w_common is universal, constant, range-independent, time-independent, species-blind and hidden-direction derivative silent",
            "if_signed": "only then can it be absorbed into measured G_N/GM",
            "current_status": "GUARDED_NOT_CLAIM",
            "if_unsigned": "G_N absorption is a hidden fit/cancellation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CMS1886_4_current_owner",
            "clause": "one current/source owner",
            "required_statement": "one parent Noether/Hilbert owner fixes matter dynamics, charges, source normalization and test coupling",
            "if_signed": "no separate source selector can choose species labels",
            "current_status": "OWNER_CANDIDATE_MISSING",
            "if_unsigned": "beta_source_alpha and relative source weights remain free finite-branch debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CMS1886_5_no_hidden_morphism",
            "clause": "no hidden-visible coefficient morphism",
            "required_statement": "Hom(C_hid,Coeff(source))=Const/0 and radiative/readout closure preserves it",
            "if_signed": "source weights cannot reappear through hidden invariants or loops/readout",
            "current_status": "MASTER_THEOREM_NOT_DERIVED",
            "if_unsigned": "source weight returns as retained residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CMS1886_6_verdict",
            "clause": "common matter/source signature",
            "required_statement": "all previous clauses are parent-signed in one action package",
            "if_signed": "common matter/source slot closes for local GR/Newton tests",
            "current_status": "SIGNATURE_NOT_DERIVED",
            "if_unsigned": "finite w_R/beta_w/Delta_w rows remain mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_wr_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "FWR1886_0_route_type",
            "field_name": "route_type",
            "required_for": "all_rows",
            "accepted_content": "parent_no_source_slot_zero | finite_source_weight_vector | bound_anchor_nonclaim",
            "reject_if": "closure, G_absorption, comparator_only, unity_tau, or cancellation",
            "reason": "forces proof-vs-finite-vs-anchor distinction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FWR1886_1_wR",
            "field_name": "w_R_or_w_A",
            "required_for": "finite_source_weight_vector",
            "accepted_content": "numeric source/action weight coefficient or theorem-zero",
            "reject_if": "missing, symbolic unity, common-mode absorption without guards, or no source path",
            "reason": "source normalization must be a prediction input, not a fitted denominator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FWR1886_2_beta_w",
            "field_name": "beta_w_source;beta_w_test",
            "required_for": "finite_source_weight_vector",
            "accepted_content": "partial_phi ln w_source and partial_phi ln w_test in a declared canonical phi/Xhat convention",
            "reject_if": "no Xhat/phi normalization, no source/test split, or product-only shortcut",
            "reason": "finite exchange/R10/PPN products need source and test legs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FWR1886_3_delta_w",
            "field_name": "Delta_w_AB",
            "required_for": "WEP/Newton/source-normalization rows",
            "accepted_content": "dimensionless material/source contrast after common-mode calibration",
            "reject_if": "basis missing, tau missing, composition pair missing, or no material map",
            "reason": "WEP/source-charge rows depend on relative, not common, weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FWR1886_4_tau_projection",
            "field_name": "tau_WEP;tau_PPN;tau_R10;tau_clock;tau_orbital",
            "required_for": "arena_score",
            "accepted_content": "arena-specific projection/readout factor with units and source",
            "reject_if": "tau set to 1 by convenience or arena omitted",
            "reason": "bound anchors cannot become MTS predictions without projection kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FWR1886_5_source_path",
            "field_name": "source_path;source_anchor;extraction_method",
            "required_for": "all_rows",
            "accepted_content": "existing local path or explicit provenance for theorem/value/bound",
            "reject_if": "MISSING marker, docs-only template as evidence, or comparator bound used as prediction",
            "reason": "keeps the branch auditable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FWR1886_6_no_cancellation",
            "field_name": "no_cancellation_policy",
            "required_for": "local_gr_or_arena_score",
            "accepted_content": "sum absolute active source-weight components unless parent identity proves cancellation",
            "reject_if": "source/test/product terms tuned to cancel",
            "reason": "prevents a hidden source slot from being hidden twice",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "FWR1886_7_flags",
            "field_name": "valid_prediction_row;score_ready;valid_for_claim;claim_allowed",
            "required_for": "all_rows",
            "accepted_content": "false in this checkpoint except schema dryrun may set valid_prediction_row=true for math-only nonclaim",
            "reject_if": "claim flags true or score_ready with missing/unsigned markers",
            "reason": "1886 is private proof/contract work",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def candidate_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "WR1886_TEMPLATE_PARENT_ZERO",
            "branch_id": BRANCH_ID,
            "route_type": "parent_no_source_slot_zero",
            "arena": "WEP;PPN;Newton;R10;clock;orbital",
            "w_R_or_w_A": "0",
            "beta_w_source": "0",
            "beta_w_test": "0",
            "Delta_w_AB": "0",
            "tau_projection": "0_or_not_required_after_parent_zero",
            "product_value": "0",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_NO_SOURCE_ONLY_SLOT_THEOREM",
            "source_anchor": "MISSING_PARENT_SOURCE",
            "extraction_method": "theorem_zero_required",
            "parent_zero_status": "MISSING_PARENT_INPUT",
            "matter_signature_status": "MISSING_COMMON_MATTER_SIGNATURE",
            "current_owner_status": "MISSING_CURRENT_OWNER",
            "readout_radiative_status": "MISSING_READOUT_RADIATIVE_CLOSURE",
            "common_mode_guard_status": "not_applicable_after_zero",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "WR1886_TEMPLATE_FINITE_SOURCE_WEIGHT",
            "branch_id": BRANCH_ID,
            "route_type": "finite_source_weight_vector",
            "arena": "MISSING_ARENA",
            "w_R_or_w_A": "MISSING_NUMERIC_SOURCE_WEIGHT",
            "beta_w_source": "MISSING_NUMERIC_BETA_W_SOURCE",
            "beta_w_test": "MISSING_NUMERIC_BETA_W_TEST",
            "Delta_w_AB": "MISSING_NUMERIC_DELTA_W_AB",
            "tau_projection": "MISSING_NUMERIC_TAU_PROJECTION",
            "product_value": "MISSING_NUMERIC_PRODUCT",
            "units": "dimensionless_or_declared_arena_units",
            "source_path": "MISSING_SOURCE_PATH_OR_EXTERNAL_PROVENANCE",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "extraction_method": "MISSING_EXTRACTION_METHOD",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "finite_row_required",
            "current_owner_status": "finite_row_required",
            "readout_radiative_status": "finite_row_required",
            "common_mode_guard_status": "MISSING_COMMON_MODE_GUARD",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "WR1886_TEMPLATE_WEP_BOUND_ANCHOR",
            "branch_id": BRANCH_ID,
            "route_type": "bound_anchor_nonclaim",
            "arena": "WEP_MICROSCOPE_TiPt",
            "w_R_or_w_A": "not_a_prediction",
            "beta_w_source": "not_a_prediction",
            "beta_w_test": "not_a_prediction",
            "Delta_w_AB": "MISSING_DELTA_W_TIPT",
            "tau_projection": "MISSING_TAU_WEP",
            "product_value": f"{WEP_SOURCE_WEIGHT_ANCHOR:.2e}",
            "units": "dimensionless",
            "source_path": str(INPUTS["local_bounds"]),
            "source_anchor": "R1_WEP_source_charge",
            "extraction_method": "MICROSCOPE source-charge bound anchor only",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "bound_anchor_not_matter_signature",
            "current_owner_status": "MISSING_CURRENT_OWNER",
            "readout_radiative_status": "MISSING_READOUT_RADIATIVE_CLOSURE",
            "common_mode_guard_status": "not_a_common_mode",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": True,
            "cancellation_only": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    template_path = str(OUTPUTS["candidate_template"])
    return [
        {
            "case_id": "CASE1886_0_closure_no_slot",
            "route_type": "parent_no_source_slot_zero",
            "arena": "all",
            "w_R_or_w_A": "0",
            "beta_w_source": "0",
            "beta_w_test": "0",
            "Delta_w_AB": "0",
            "tau_projection": "0",
            "product_value": "0",
            "source_path": str(INPUTS["1065_parent_grammar"]),
            "source_anchor": "PGG1065_5_verdict",
            "extraction_method": "closure grammar import",
            "parent_zero_status": "CLOSURE_ONLY",
            "matter_signature_status": "UNSIGNED",
            "current_owner_status": "UNSIGNED",
            "readout_radiative_status": "UNSIGNED",
            "common_mode_guard_status": "not_applicable",
            "closure_used": True,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1886_1_G_absorption",
            "route_type": "finite_source_weight_vector",
            "arena": "Newton_PPN",
            "w_R_or_w_A": "1.0",
            "beta_w_source": "0",
            "beta_w_test": "0",
            "Delta_w_AB": "MISSING_COMMON_MODE_GUARD",
            "tau_projection": "not_applicable",
            "product_value": "0",
            "source_path": template_path,
            "source_anchor": "schema_test",
            "extraction_method": "absorbed into measured G",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "schema_test",
            "current_owner_status": "schema_test",
            "readout_radiative_status": "schema_test",
            "common_mode_guard_status": "MISSING_SPECIES_RANGE_TIME_FRAME_GUARD",
            "closure_used": False,
            "G_absorption_used": True,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1886_2_bound_anchor_only",
            "route_type": "bound_anchor_nonclaim",
            "arena": "WEP_MICROSCOPE_TiPt",
            "w_R_or_w_A": "not_a_prediction",
            "beta_w_source": "not_a_prediction",
            "beta_w_test": "not_a_prediction",
            "Delta_w_AB": "MISSING_DELTA_W_TIPT",
            "tau_projection": "MISSING_TAU_WEP",
            "product_value": f"{WEP_SOURCE_WEIGHT_ANCHOR:.2e}",
            "source_path": str(INPUTS["local_bounds"]),
            "source_anchor": "R1_WEP_source_charge",
            "extraction_method": "source-backed bound anchor",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "not_a_theorem",
            "current_owner_status": "MISSING_CURRENT_OWNER",
            "readout_radiative_status": "MISSING_READOUT_RADIATIVE_CLOSURE",
            "common_mode_guard_status": "not_applicable",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": True,
            "cancellation_only": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1886_3_missing_finite",
            "route_type": "finite_source_weight_vector",
            "arena": "MISSING_ARENA",
            "w_R_or_w_A": "MISSING",
            "beta_w_source": "MISSING",
            "beta_w_test": "MISSING",
            "Delta_w_AB": "MISSING",
            "tau_projection": "MISSING",
            "product_value": "MISSING",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "extraction_method": "MISSING_EXTRACTION_METHOD",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "MISSING",
            "current_owner_status": "MISSING",
            "readout_radiative_status": "MISSING",
            "common_mode_guard_status": "MISSING",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1886_4_unsigned_zero",
            "route_type": "parent_no_source_slot_zero",
            "arena": "all",
            "w_R_or_w_A": "0",
            "beta_w_source": "0",
            "beta_w_test": "0",
            "Delta_w_AB": "0",
            "tau_projection": "0",
            "product_value": "0",
            "source_path": str(INPUTS["1066_source_scalar"]),
            "source_anchor": "SSE1066_5_verdict",
            "extraction_method": "conditional source scalar exclusion",
            "parent_zero_status": "UNSIGNED_PARENT_CHAIN",
            "matter_signature_status": "UNSIGNED",
            "current_owner_status": "UNSIGNED",
            "readout_radiative_status": "UNSIGNED",
            "common_mode_guard_status": "not_applicable",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1886_5_symbolic_beta_w",
            "route_type": "finite_source_weight_vector",
            "arena": "R10_PPN",
            "w_R_or_w_A": "0.0",
            "beta_w_source": "beta_symbolic",
            "beta_w_test": "1.0e-05",
            "Delta_w_AB": "0.0",
            "tau_projection": "1.0",
            "product_value": "1.0e-05",
            "source_path": template_path,
            "source_anchor": "schema_test",
            "extraction_method": "symbolic beta_w source leg",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "schema_test",
            "current_owner_status": "schema_test",
            "readout_radiative_status": "schema_test",
            "common_mode_guard_status": "schema_test",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1886_6_cancellation_tuned",
            "route_type": "finite_source_weight_vector",
            "arena": "PPN_Newton",
            "w_R_or_w_A": "0.0",
            "beta_w_source": "1.0e-04",
            "beta_w_test": "-1.0e-04",
            "Delta_w_AB": "0.0",
            "tau_projection": "1.0",
            "product_value": "0.0",
            "source_path": template_path,
            "source_anchor": "schema_test",
            "extraction_method": "cancellation test",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "schema_test",
            "current_owner_status": "schema_test",
            "readout_radiative_status": "schema_test",
            "common_mode_guard_status": "schema_test",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1886_7_schema_complete_nonclaim",
            "route_type": "finite_source_weight_vector",
            "arena": "WEP_MICROSCOPE_TiPt",
            "w_R_or_w_A": "1.0e-06",
            "beta_w_source": "1.0e-06",
            "beta_w_test": "1.0e-06",
            "Delta_w_AB": "1.0e-06",
            "tau_projection": "1.0e-06",
            "product_value": "1.0e-12",
            "source_path": template_path,
            "source_anchor": "schema_test",
            "extraction_method": "schema math only",
            "parent_zero_status": "not_applicable",
            "matter_signature_status": "schema_test_signed",
            "current_owner_status": "schema_test_signed",
            "readout_radiative_status": "schema_test_signed",
            "common_mode_guard_status": "schema_test_signed",
            "closure_used": False,
            "G_absorption_used": False,
            "bound_anchor_only": False,
            "cancellation_only": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    route_type = str(row.get("route_type", "")).strip()
    closure_used = bool_string(row.get("closure_used", "")) == "true"
    g_absorption_used = bool_string(row.get("G_absorption_used", "")) == "true"
    bound_anchor_only = bool_string(row.get("bound_anchor_only", "")) == "true"
    cancellation_only = bool_string(row.get("cancellation_only", "")) == "true"
    numeric_fields = ["w_R_or_w_A", "beta_w_source", "beta_w_test", "Delta_w_AB", "tau_projection", "product_value"]
    parsed = {field: finite_float(row.get(field, "")) for field in numeric_fields}
    all_numeric = all(ok for ok, _ in parsed.values())
    product_ok = False
    product_residual = "not_evaluated"
    valid_prediction_row = False
    score_ready = False

    if bool_string(row.get("valid_for_claim", "")) != "false" or bool_string(row.get("claim_allowed", "")) != "false":
        status = "REFUSED_CLAIM_FLAG"
    elif closure_used:
        status = "REFUSED_CLOSURE_NOT_EVIDENCE"
    elif g_absorption_used:
        status = "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"
    elif bound_anchor_only:
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    elif cancellation_only:
        status = "REFUSED_CANCELLATION_ONLY"
    elif route_type not in {"parent_no_source_slot_zero", "finite_source_weight_vector", "bound_anchor_nonclaim"}:
        status = "REFUSED_BAD_ROUTE_TYPE"
    elif route_type == "parent_no_source_slot_zero":
        if not all_numeric or any(abs(value or 0.0) > 1e-12 for _, value in parsed.values()):
            status = "REFUSED_PARENT_ZERO_NUMERIC_MISMATCH"
        elif str(row.get("parent_zero_status", "")) != "PARENT_SIGNED_NO_SOURCE_ONLY_SLOT":
            status = "REFUSED_PARENT_NO_SOURCE_SLOT_UNSIGNED"
        elif any("MISSING" in str(row.get(field, "")).upper() or "UNSIGNED" in str(row.get(field, "")).upper() for field in ("matter_signature_status", "current_owner_status", "readout_radiative_status")):
            status = "REFUSED_MISSING_MATTER_SIGNATURE_PREMISES"
        else:
            valid_prediction_row = True
            score_ready = True
            product_ok = True
            status = "SCHEMA_READY_PARENT_ZERO_NONCLAIM"
    elif route_type == "bound_anchor_nonclaim":
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    else:
        if not all_numeric:
            status = "REFUSED_MISSING_OR_NONNUMERIC_SOURCE_WEIGHT_INPUTS"
        elif is_placeholder(row.get("arena", "")) or is_placeholder(row.get("source_path", "")) or is_placeholder(row.get("source_anchor", "")) or is_placeholder(row.get("extraction_method", "")):
            status = "REFUSED_MISSING_SOURCE_OR_ARENA"
        elif any("MISSING" in str(row.get(field, "")).upper() or "UNSIGNED" in str(row.get(field, "")).upper() for field in ("matter_signature_status", "current_owner_status", "readout_radiative_status", "common_mode_guard_status")):
            status = "REFUSED_MISSING_SIGNATURE_OR_READOUT_PREMISES"
        else:
            delta_w = parsed["Delta_w_AB"][1] or 0.0
            tau = parsed["tau_projection"][1] or 0.0
            product = parsed["product_value"][1] or 0.0
            product_residual_value = abs(product - delta_w * tau)
            product_residual = f"{product_residual_value:.12g}"
            product_ok = product_residual_value <= 1e-12
            valid_prediction_row = True
            if not product_ok:
                status = "REFUSED_PRODUCT_LAW_MISMATCH"
            elif "schema" in str(row.get("extraction_method", "")).lower():
                score_ready = False
                status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
            else:
                score_ready = True
                status = "SCHEMA_READY_NONCLAIM"

    result = dict(row)
    result.update(
        {
            "product_residual": product_residual,
            "product_law_pass": product_ok,
            "validator_status": status,
            "valid_prediction_row": valid_prediction_row,
            "score_ready": score_ready,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return result


def dryrun_result_rows() -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in dryrun_case_rows()]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1886_0_no_source_slot_proof_checker",
            "runner": "parent no-source-only-slot proof checker",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "the no-slot theorem is exact conditional but not parent-signed by object-language/current-owner/readout package",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1886_1_wr_betaw_validator",
            "runner": "finite w_R/beta_w/Delta_w row validator",
            "current_status": "ALLOW_SCHEMA_DRYRUN_NONCLAIM",
            "reason": "schema catches closure, G absorption, bound-anchor-only, missing, unsigned and cancellation routes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1886_2_local_gr_source_scorer",
            "runner": "local GR/Newton source-coupling scorer",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "no parent zero theorem and no live finite source-weight prediction row exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1886_0_conditional_no_slot",
            "claim": "if parent grammar excludes source-only weights, Delta_w and beta_w vanish",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "mathematical consequence is sharp but premise is unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1886_1_parent_no_slot",
            "claim": "MTS parent derives no source-only/action-weight slot",
            "status": "BLOCKED",
            "reason": "object-language/current-owner/action-scale/readout-radiative clauses are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1886_2_G_absorption",
            "claim": "relative source weights can be absorbed into measured G or GM",
            "status": "BLOCKED",
            "reason": "only universal derivative-silent common mode can be calibration; relative weights are observable residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1886_3_finite_wr_row",
            "claim": "finite w_R/beta_w/Delta_w row is score-ready",
            "status": "BLOCKED",
            "reason": "only templates and WEP bound anchors exist; no MTS prediction row is sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1886_4_local_gr_newton",
            "claim": "source side of local GR/Newton is derived",
            "status": "BLOCKED",
            "reason": "source-weight loophole remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1886_0_no_slot_not_derived",
            "decision": "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED",
            "because": "the current corpus has exact contracts but also retains the w_A counterexample",
            "next_action": "do not claim common matter/source coupling or local GR from source-side closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1886_1_keep_seam",
            "decision": "SOURCE_WEIGHT_SEAM_IS_REAL",
            "because": "variation identity shows classical EOM can look harmless while Hilbert source and beta_w legs change",
            "next_action": "carry w_R/beta_w/Delta_w in the residual vector unless parent-signed zero closes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1886_2_next_object_language",
            "decision": "PARENT_OBJECT_LANGUAGE_TYPING_OR_FINITE_VECTOR_NEXT",
            "because": "the missing proof is not more bounds; it is why w_A is not an allowed parent object",
            "next_action": "attack parent object-language/action-scale normalization or fill a real finite source-weight vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1886_0_primary",
            "selection_status": "selected",
            "target_file": "1887-Y5-R2FR-parent-object-language-typing-or-finite-source-weight-vector.md",
            "target_script": "scripts/Y5_R2FR_parent_object_language_typing_or_finite_source_weight_vector_1887.py",
            "objective": "try to derive the parent object-language/action-scale rule that makes w_A impossible; if it fails, stage a real finite source-weight vector intake with WEP/PPN/Newton/R10 arena hooks",
            "success_condition": "parent-signed object-language exclusion of source-only coefficients, or a strict finite Delta_w/beta_w/w_R vector validator with no G-absorption or bound-anchor shortcuts",
            "do_not_do": "do not use WEP bound anchors as predictions, do not set tau=1, do not absorb relative weights into G_N, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PSTAT1886_0_gain",
            "topic": "source-side local GR",
            "status": "NO_SOURCE_ONLY_SLOT_CONTRACT_SHARP",
            "risk_level": "ROBUSTNESS_GAIN",
            "detail": "we now have the exact parent clause needed to silence source-weight leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "PSTAT1886_1_bottleneck",
            "topic": "parent ownership",
            "status": "OBJECT_LANGUAGE_TYPING_UNSIGNED",
            "risk_level": "MAIN_BOTTLENECK",
            "detail": "no current file derives why w_A is not an allowed parent object rather than a forbidden-by-choice term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "PSTAT1886_2_next",
            "topic": "next route",
            "status": "OBJECT_LANGUAGE_OR_FINITE_SOURCE_WEIGHT_VECTOR",
            "risk_level": "NEXT_BEST_MOVE",
            "detail": "either sign the object-language rule, or produce actual finite source-weight vector rows with arena projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "no_source_slot_audit": no_source_slot_audit_rows(),
        "matter_signature_contract": matter_signature_contract_rows(),
        "finite_wr_contract": finite_wr_contract_rows(),
        "candidate_template": candidate_template_rows(),
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
    ok = True
    for path in paths:
        try:
            rows = csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in ("valid_for_claim", "claim_allowed"):
                if field in row and bool_string(row[field]) != "false":
                    bad.append(f"{path.name}:line{index}:{field}={row[field]}")
    return not bad, "all claim flags false" if not bad else "; ".join(bad)


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    blocked_markers = ("MISSING", "UNSIGNED", "CLOSURE", "ABSORPTION", "BOUND_ANCHOR", "COUNTEREXAMPLE")
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            row_text = " ".join(str(value) for value in row.values()).upper()
            if any(marker in row_text for marker in blocked_markers):
                if bool_string(row.get("valid_for_claim", "false")) != "false" or bool_string(row.get("claim_allowed", "false")) != "false":
                    bad.append(f"{path.name}:line{index}:claim flag with blocked marker")
                if bool_string(row.get("score_ready", "false")) == "true":
                    bad.append(f"{path.name}:line{index}:score_ready with blocked marker")
    return not bad, "blocked-marker rows are not claim-ready" if not bad else "; ".join(bad)


def copy_branch_artifacts() -> None:
    copy_pairs = [
        (OUTPUTS["no_source_slot_audit"], MICROSCOPE_RESIDUALS / OUTPUTS["no_source_slot_audit"].name),
        (OUTPUTS["matter_signature_contract"], QUEUE / "JR1886_COMMON_MATTER_SIGNATURE_CONTRACT_NONCLAIM.csv"),
        (OUTPUTS["finite_wr_contract"], QUEUE / "JR1886_FINITE_WR_BETAW_ROW_CONTRACT_NONCLAIM.csv"),
        (OUTPUTS["candidate_template"], SOURCE_WEIGHT_TEMPLATE_COPY),
        (OUTPUTS["dryrun_results"], QUARANTINE / OUTPUTS["dryrun_results"].name),
    ]
    for src, dst in copy_pairs:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    sources = csv_rows(OUTPUTS["source_register"])
    source_count = len(sources)
    source_ok = sum(1 for row in sources if bool_string(row["source_exists"]) == "true")
    needle_ok = sum(1 for row in sources if row["needle_check"] == "OK")
    checks.append(
        {
            "validation_id": "VAL1886_0_sources_exist",
            "status": "PASS" if source_ok == source_count else "FAIL",
            "detail": f"{source_ok}/{source_count} sources exist",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1886_1_needles_found",
            "status": "PASS" if needle_ok == source_count else "FAIL",
            "detail": f"{needle_ok}/{source_count} source needles found",
            "valid_for_claim": False,
        }
    )

    audit = csv_rows(OUTPUTS["no_source_slot_audit"])
    checks.append(
        {
            "validation_id": "VAL1886_2_counterexample_retained",
            "status": "PASS"
            if any(row["audit_id"] == "NSS1886_2_counterexample" and row["attempt_result"] == "COUNTEREXAMPLE_SURVIVES" for row in audit)
            else "FAIL",
            "detail": "relative source/action weight counterexample remains explicit",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1886_3_no_slot_not_promoted",
            "status": "PASS"
            if any(row["audit_id"] == "NSS1886_7_verdict" and row["attempt_result"] == "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED" for row in audit)
            else "FAIL",
            "detail": "no-source-only-slot theorem is not promoted",
            "valid_for_claim": False,
        }
    )

    signature = csv_rows(OUTPUTS["matter_signature_contract"])
    checks.append(
        {
            "validation_id": "VAL1886_4_signature_clauses",
            "status": "PASS"
            if any(row["clause_id"] == "CMS1886_1_no_source_only_weight" for row in signature)
            and any(row["current_status"] == "MASTER_THEOREM_NOT_DERIVED" for row in signature)
            else "FAIL",
            "detail": "matter signature contract includes no-slot and no-hidden-morphism clauses",
            "valid_for_claim": False,
        }
    )

    contract = csv_rows(OUTPUTS["finite_wr_contract"])
    required_fields = {"w_R_or_w_A", "beta_w_source;beta_w_test", "Delta_w_AB", "tau_WEP;tau_PPN;tau_R10;tau_clock;tau_orbital"}
    checks.append(
        {
            "validation_id": "VAL1886_5_finite_contract_fields",
            "status": "PASS" if required_fields.issubset({row["field_name"] for row in contract}) else "FAIL",
            "detail": f"finite_contract_fields={len(contract)}",
            "valid_for_claim": False,
        }
    )

    templates = csv_rows(OUTPUTS["candidate_template"])
    checks.append(
        {
            "validation_id": "VAL1886_6_templates_nonclaim",
            "status": "PASS"
            if len(templates) == 3
            and all(bool_string(row["valid_for_claim"]) == "false" and bool_string(row["claim_allowed"]) == "false" for row in templates)
            and any("MISSING" in " ".join(row.values()).upper() for row in templates)
            else "FAIL",
            "detail": "parent-zero, finite, and WEP anchor templates remain nonclaim",
            "valid_for_claim": False,
        }
    )

    dryruns = csv_rows(OUTPUTS["dryrun_results"])
    expected_statuses = {
        "REFUSED_CLOSURE_NOT_EVIDENCE",
        "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD",
        "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
        "REFUSED_MISSING_OR_NONNUMERIC_SOURCE_WEIGHT_INPUTS",
        "REFUSED_PARENT_NO_SOURCE_SLOT_UNSIGNED",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    checks.append(
        {
            "validation_id": "VAL1886_7_dryrun_failure_modes",
            "status": "PASS" if expected_statuses.issubset({row["validator_status"] for row in dryruns}) else "FAIL",
            "detail": f"dryrun_statuses={','.join(row['validator_status'] for row in dryruns)}",
            "valid_for_claim": False,
        }
    )

    runners = csv_rows(OUTPUTS["runner_refusal"])
    checks.append(
        {
            "validation_id": "VAL1886_8_runner_refusal",
            "status": "PASS"
            if any(row["current_status"] == "ALLOW_SCHEMA_DRYRUN_NONCLAIM" for row in runners)
            and sum(1 for row in runners if row["current_status"] == "REFUSE_CLAIM_RUN") == 2
            else "FAIL",
            "detail": "claim runs refuse while finite-row schema dryrun is allowed nonclaim",
            "valid_for_claim": False,
        }
    )

    claims = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1886_9_claim_gates",
            "status": "PASS"
            if any(row["status"] == "PASS_CONDITIONAL_NONCLAIM" for row in claims)
            and sum(1 for row in claims if row["status"] == "BLOCKED") == 4
            else "FAIL",
            "detail": "only conditional no-slot consequence passes; all claim gates block",
            "valid_for_claim": False,
        }
    )

    decisions = csv_rows(OUTPUTS["decision"])
    checks.append(
        {
            "validation_id": "VAL1886_10_decision",
            "status": "PASS"
            if any(row["decision"] == "PARENT_OBJECT_LANGUAGE_TYPING_OR_FINITE_VECTOR_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision selects object-language typing or finite vector next",
            "valid_for_claim": False,
        }
    )

    next_targets = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1886_11_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1886_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1887 parent object-language typing or finite source-weight vector selected",
            "valid_for_claim": False,
        }
    )

    status_rows = csv_rows(OUTPUTS["project_status"])
    checks.append(
        {
            "validation_id": "VAL1886_12_project_status",
            "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows) else "FAIL",
            "detail": "project status snapshot keeps object-language typing as main bottleneck",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1886_13_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1886_14_blocked_markers_not_ready",
            "status": "PASS" if blocked_ok else "FAIL",
            "detail": blocked_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1886_15_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["no_source_slot_audit"].name,
        QUEUE / "JR1886_COMMON_MATTER_SIGNATURE_CONTRACT_NONCLAIM.csv",
        QUEUE / "JR1886_FINITE_WR_BETAW_ROW_CONTRACT_NONCLAIM.csv",
        SOURCE_WEIGHT_TEMPLATE_COPY,
        QUARANTINE / OUTPUTS["dryrun_results"].name,
    ]
    checks.append(
        {
            "validation_id": "VAL1886_16_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1886_17_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1886*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1886_18_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1886_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1886_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1886 common matter no-source-only slot proof or finite w_R row",
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
    content = f"""# 1886 - Common Matter No-Source-Only Slot Proof Or Finite w_R Row

**Private status:** derivation-first source-coupling gate; no local-GR claim.

## Result

1886 sharpens the source-side problem to one exact seam:

```text
S_matter = sum_A w_A(X) S_A
```

can preserve ordinary-looking covariance/additivity while changing the Hilbert/coframe source:

```text
T_obs = sum_A w_A T_A
J_X contains sum_A (partial_X w_A) S_A
```

So the desired local-GR route is clear but unsigned:

```text
Allowed[S_matter] excludes w_A(X)S_A, kappa_A(X)T_A, and source-only material multipliers.
```

If that parent grammar is signed, `Delta_w_AB`, `beta_w_source`, `beta_w_test`, and `w_R` vanish after common-mode calibration. Current corpus does not derive that grammar. It has exact contracts and good counterexample discipline, not a theorem.

1886 therefore builds the fallback contract: any finite source-weight route must supply real `w_R/beta_w/Delta_w/tau` rows with arena projections. WEP/MICROSCOPE bound anchors are pressure only; they are not MTS predictions.

## No-Source-Only Slot Proof Audit

{markdown_table(rows_by_name["no_source_slot_audit"])}

## Common Matter Signature Contract

{markdown_table(rows_by_name["matter_signature_contract"])}

## Finite w_R / beta_w Row Contract

{markdown_table(rows_by_name["finite_wr_contract"])}

## Candidate Template

{markdown_table(rows_by_name["candidate_template"])}

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
